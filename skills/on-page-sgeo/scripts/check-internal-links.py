#!/usr/bin/env python3
"""Analyze internal links on a page.

Extracts all <a> tags with internal hrefs, evaluates anchor text quality,
counts links per 1000 words, and checks for broken links (sampling first 20).

Usage:
    python check-internal-links.py --url https://example.com/page
    python check-internal-links.py --url https://example.com/page --tools tools.json

Output: JSON with link inventory, anchor text analysis, and issues.
"""

import argparse
import json
import re
import sys
from html.parser import HTMLParser
from urllib.parse import urlparse, urljoin
from typing import Optional


# ---------------------------------------------------------------------------
# HTML Parser
# ---------------------------------------------------------------------------

class LinkExtractor(HTMLParser):
    """Extract links and body text from HTML."""

    NAV_TAGS = {"nav", "header", "footer", "aside"}

    def __init__(self, base_url: str):
        super().__init__()
        self.base_url = base_url
        self.base_domain = urlparse(base_url).netloc.lower()
        self.links: list[dict] = []
        self._text_parts: list[str] = []
        self._in_anchor = False
        self._anchor_text = ""
        self._anchor_href = ""
        self._nav_depth = 0
        self._skip_tags = {"script", "style", "noscript"}
        self._skip_depth = 0

    def handle_starttag(self, tag: str, attrs):
        attr_dict = {k: v for k, v in attrs}

        if tag in self._skip_tags:
            self._skip_depth += 1
        if tag in self.NAV_TAGS:
            self._nav_depth += 1

        if tag == "a" and self._skip_depth == 0:
            href = attr_dict.get("href", "")
            if href:
                self._in_anchor = True
                self._anchor_text = ""
                self._anchor_href = href

    def handle_data(self, data: str):
        if self._skip_depth > 0:
            return
        self._text_parts.append(data)
        if self._in_anchor:
            self._anchor_text += data

    def handle_endtag(self, tag: str):
        if tag in self._skip_tags and self._skip_depth > 0:
            self._skip_depth -= 1
        if tag in self.NAV_TAGS and self._nav_depth > 0:
            self._nav_depth -= 1

        if tag == "a" and self._in_anchor:
            self._in_anchor = False
            href = self._anchor_href.strip()
            text = re.sub(r"\s+", " ", self._anchor_text).strip()

            # Resolve relative URLs
            absolute = urljoin(self.base_url, href)
            parsed = urlparse(absolute)
            link_domain = parsed.netloc.lower()

            # Only keep internal links
            if link_domain == self.base_domain:
                self.links.append({
                    "href": absolute,
                    "anchor_text": text,
                    "in_nav": self._nav_depth > 0,
                })

    def get_body_text(self) -> str:
        return re.sub(r"\s+", " ", " ".join(self._text_parts)).strip()


# ---------------------------------------------------------------------------
# Anchor text classification
# ---------------------------------------------------------------------------

GENERIC_ANCHORS = {
    "click here", "here", "learn more", "read more", "more",
    "link", "this", "read this", "see more", "view more",
    "continue reading", "go", "visit",
}


def classify_anchor(text: str) -> str:
    """Classify anchor text type."""
    lower = text.lower().strip()
    if not lower:
        return "empty"
    if lower in GENERIC_ANCHORS:
        return "generic"
    word_count = len(lower.split())
    if word_count > 8:
        return "over_optimized"
    return "descriptive"


# ---------------------------------------------------------------------------
# Link checking
# ---------------------------------------------------------------------------

def check_link_status(url: str) -> int:
    """HEAD request to check if link is alive. Returns status code or -1."""
    from urllib.request import Request, urlopen
    from urllib.error import HTTPError, URLError
    try:
        req = Request(url, method="HEAD",
                      headers={"User-Agent": "Mozilla/5.0 (compatible; on-page-sgeo-audit/1.0)"})
        with urlopen(req, timeout=10) as resp:
            return resp.status
    except HTTPError as e:
        return e.code
    except (URLError, Exception):
        return -1


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def analyze(url: str, html: str, check_broken: bool = True) -> dict:
    parser = LinkExtractor(url)
    parser.feed(html)

    body_text = parser.get_body_text()
    word_count = len(body_text.split())

    body_links = [l for l in parser.links if not l["in_nav"]]
    nav_links = [l for l in parser.links if l["in_nav"]]

    links_per_1000 = round((len(body_links) / max(word_count, 1)) * 1000, 2)

    # Anchor analysis
    anchor_counts = {"descriptive": 0, "generic": 0, "over_optimized": 0, "empty": 0}
    generic_anchors = []
    for link in parser.links:
        cls = classify_anchor(link["anchor_text"])
        anchor_counts[cls] = anchor_counts.get(cls, 0) + 1
        if cls == "generic":
            generic_anchors.append({"text": link["anchor_text"], "href": link["href"]})

    # Check first 20 links for broken status
    broken_links = []
    if check_broken:
        sample = parser.links[:20]
        for link in sample:
            status = check_link_status(link["href"])
            if status != 200 and status != -1:
                broken_links.append({"href": link["href"], "status": status})
            elif status == -1:
                broken_links.append({"href": link["href"], "status": "unreachable"})

    issues: list[str] = []
    if links_per_1000 < 2:
        issues.append(f"Under-linked: {links_per_1000} body links per 1000 words (target 3-5)")
    elif links_per_1000 > 8:
        issues.append(f"Over-linked: {links_per_1000} body links per 1000 words (target 3-5)")

    if anchor_counts["generic"] > 0:
        issues.append(f"{anchor_counts['generic']} generic anchor(s) found ('click here', 'learn more')")

    if broken_links:
        issues.append(f"{len(broken_links)} broken internal link(s) found")

    return {
        "url": url,
        "total_internal_links": len(parser.links),
        "body_links": len(body_links),
        "nav_links": len(nav_links),
        "word_count": word_count,
        "links_per_1000_words": links_per_1000,
        "anchor_analysis": anchor_counts,
        "generic_anchors": generic_anchors[:10],  # Cap output
        "broken_links": broken_links,
        "issues": issues,
    }


def fetch_html(url: str) -> str:
    from urllib.request import Request, urlopen
    req = Request(url, headers={"User-Agent": "Mozilla/5.0 (compatible; on-page-sgeo-audit/1.0)"})
    with urlopen(req, timeout=15) as resp:
        return resp.read().decode("utf-8", errors="replace")


def main():
    ap = argparse.ArgumentParser(description="Analyze internal links on a page")
    ap.add_argument("--url", required=True, help="Page URL to analyze")
    ap.add_argument("--tools", default=None, help="Path to tools.json inventory file")
    ap.add_argument("--skip-broken-check", action="store_true", help="Skip link status checks")
    args = ap.parse_args()

    try:
        html = fetch_html(args.url)
    except Exception as e:
        print(json.dumps({"error": f"Failed to fetch URL: {e}", "url": args.url}), file=sys.stderr)
        sys.exit(1)

    result = analyze(args.url, html, check_broken=not args.skip_broken_check)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
