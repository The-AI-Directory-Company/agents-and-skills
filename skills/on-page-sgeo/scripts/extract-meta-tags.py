#!/usr/bin/env python3
"""Extract and validate meta tags from a URL.

Fetches the page HTML and extracts title tag, meta description, canonical,
robots meta, Open Graph tags, and Twitter Card tags. Validates lengths,
checks for keyword stuffing, and flags common issues.

Usage:
    python extract-meta-tags.py --url https://example.com/page
    python extract-meta-tags.py --url https://example.com/page --tools tools.json

Output: JSON with extracted tags, validation results, and issues.
"""

import argparse
import json
import re
import sys
from html.parser import HTMLParser
from urllib.parse import urlparse
from typing import Optional

# ---------------------------------------------------------------------------
# HTML Parser — lightweight, no external dependencies
# ---------------------------------------------------------------------------

class MetaTagParser(HTMLParser):
    """Extract meta-relevant tags from HTML <head>."""

    def __init__(self):
        super().__init__()
        self.title = ""
        self._in_title = False
        self.meta_description = ""
        self.meta_robots = ""
        self.canonical = ""
        self.og_tags: dict[str, str] = {}
        self.twitter_tags: dict[str, str] = {}

    def handle_starttag(self, tag: str, attrs: list[tuple[str, Optional[str]]]):
        attr_dict = {k.lower(): v for k, v in attrs if v is not None}

        if tag == "title":
            self._in_title = True
            return

        if tag == "meta":
            name = attr_dict.get("name", "").lower()
            prop = attr_dict.get("property", "").lower()
            content = attr_dict.get("content", "")

            if name == "description":
                self.meta_description = content
            elif name == "robots":
                self.meta_robots = content
            elif prop.startswith("og:"):
                self.og_tags[prop] = content
            elif name.startswith("twitter:"):
                self.twitter_tags[name] = content

        if tag == "link":
            rel = attr_dict.get("rel", "").lower()
            href = attr_dict.get("href", "")
            if rel == "canonical":
                self.canonical = href

    def handle_data(self, data: str):
        if self._in_title:
            self.title += data

    def handle_endtag(self, tag: str):
        if tag == "title":
            self._in_title = False


# ---------------------------------------------------------------------------
# Validation helpers
# ---------------------------------------------------------------------------

def check_keyword_stuffing(text: str) -> list[str]:
    """Flag words repeated more than twice in the title."""
    words = re.findall(r"[a-z]+", text.lower())
    from collections import Counter
    counts = Counter(words)
    # Ignore very common short words
    stop = {"the", "a", "an", "and", "or", "in", "of", "to", "for", "is", "on", "at", "by", "with", "from"}
    return [w for w, c in counts.items() if c > 2 and w not in stop]


def validate_canonical(canonical: str, page_url: str) -> dict:
    """Check canonical is absolute and self-referencing."""
    parsed = urlparse(canonical)
    is_absolute = bool(parsed.scheme and parsed.netloc)
    # Normalize for comparison (strip trailing slash, fragment)
    def norm(u: str) -> str:
        p = urlparse(u)
        path = p.path.rstrip("/") or "/"
        return f"{p.scheme}://{p.netloc}{path}"
    self_ref = norm(canonical) == norm(page_url) if is_absolute else False
    return {"href": canonical, "is_absolute": is_absolute, "self_referencing": self_ref}


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def fetch_html(url: str, tools_path: Optional[str] = None) -> str:
    """Fetch HTML from URL.

    In an agent context the caller would use WebFetch MCP. When running
    standalone we fall back to urllib.
    """
    from urllib.request import Request, urlopen

    req = Request(url, headers={"User-Agent": "Mozilla/5.0 (compatible; on-page-sgeo-audit/1.0)"})
    with urlopen(req, timeout=15) as resp:
        return resp.read().decode("utf-8", errors="replace")


def analyze(url: str, html: str) -> dict:
    parser = MetaTagParser()
    parser.feed(html)

    title_len = len(parser.title.strip())
    desc_len = len(parser.meta_description.strip())

    issues: list[str] = []

    # Title checks
    title_valid = 0 < title_len <= 60
    if title_len == 0:
        issues.append("Missing title tag")
    elif title_len > 60:
        issues.append(f"Title tag too long ({title_len} chars, max 60)")

    stuffed = check_keyword_stuffing(parser.title)
    if stuffed:
        issues.append(f"Possible keyword stuffing in title: {', '.join(stuffed)} repeated >2x")

    # Description checks
    desc_valid = 0 < desc_len <= 155
    if desc_len == 0:
        issues.append("Missing meta description")
    elif desc_len > 155:
        issues.append(f"Meta description too long ({desc_len} chars, max 155)")

    # Canonical checks
    canonical_info = validate_canonical(parser.canonical, url) if parser.canonical else {"href": "", "is_absolute": False, "self_referencing": False}
    if not parser.canonical:
        issues.append("Missing canonical tag")
    elif not canonical_info["is_absolute"]:
        issues.append("Canonical URL is relative — must be absolute")
    elif not canonical_info["self_referencing"]:
        issues.append("Canonical URL does not match page URL (not self-referencing)")

    # OG checks
    if "og:image" not in parser.og_tags:
        issues.append("Missing og:image — social shares will have no image")
    if "og:title" not in parser.og_tags:
        issues.append("Missing og:title")
    if "og:description" not in parser.og_tags:
        issues.append("Missing og:description")

    # Robots meta
    robots_lower = parser.meta_robots.lower()
    if "noindex" in robots_lower:
        issues.append("Page has noindex — it will not appear in search results")

    return {
        "url": url,
        "title": {
            "content": parser.title.strip(),
            "length": title_len,
            "valid": title_valid,
            "keyword_stuffing": stuffed,
        },
        "meta_description": {
            "content": parser.meta_description.strip(),
            "length": desc_len,
            "valid": desc_valid,
        },
        "meta_robots": parser.meta_robots or None,
        "canonical": canonical_info,
        "og_tags": parser.og_tags or None,
        "twitter_tags": parser.twitter_tags or None,
        "issues": issues,
    }


def main():
    parser = argparse.ArgumentParser(description="Extract and validate meta tags from a URL")
    parser.add_argument("--url", required=True, help="Page URL to analyze")
    parser.add_argument("--tools", default=None, help="Path to tools.json inventory file")
    args = parser.parse_args()

    try:
        html = fetch_html(args.url, args.tools)
    except Exception as e:
        print(json.dumps({"error": f"Failed to fetch URL: {e}", "url": args.url}), file=sys.stderr)
        sys.exit(1)

    result = analyze(args.url, html)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
