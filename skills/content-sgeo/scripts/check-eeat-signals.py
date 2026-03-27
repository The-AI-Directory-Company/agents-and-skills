#!/usr/bin/env python3
"""
check-eeat-signals.py — Check E-E-A-T signal presence on a page.

Evaluates author byline, author page, bio/credentials, external citations,
visible dates, editorial policy, and contact information. Outputs an
E-E-A-T checklist with per-signal pass/fail.

Usage:
    python check-eeat-signals.py --url https://example.com/article
    python check-eeat-signals.py --url https://example.com/article --tools tools.json

Free path: WebFetch + HTML parsing. No paid extension needed.
"""

import argparse
import json
import re
import sys
import urllib.request
import urllib.parse
from html.parser import HTMLParser
from typing import Any


def load_tools(tools_path: str | None) -> dict[str, Any]:
    """Load tool inventory from JSON file if provided."""
    if tools_path:
        try:
            with open(tools_path, "r") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Warning: Could not load tools file: {e}", file=sys.stderr)
    return {}


def fetch_page(url: str) -> str:
    """Fetch a page's HTML content."""
    try:
        req = urllib.request.Request(url, headers={
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                          "AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/120.0.0.0 Safari/537.36"
        })
        with urllib.request.urlopen(req, timeout=15) as resp:
            return resp.read().decode("utf-8", errors="replace")
    except Exception as e:
        print(f"Error: Failed to fetch {url}: {e}", file=sys.stderr)
        return ""


class EEATParser(HTMLParser):
    """Parse HTML to extract E-E-A-T signals."""

    def __init__(self):
        super().__init__()
        self.links: list[dict[str, str]] = []
        self.author_candidates: list[dict[str, Any]] = []
        self.json_ld_blocks: list[str] = []
        self.in_json_ld = False
        self.json_ld_buffer: list[str] = []
        self.in_script = False
        self.in_style = False
        self.text_parts: list[str] = []
        self.current_attrs: dict[str, str] = {}

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]):
        tag_lower = tag.lower()
        attr_dict = {k: v or "" for k, v in attrs}

        if tag_lower == "script":
            if attr_dict.get("type") == "application/ld+json":
                self.in_json_ld = True
                self.json_ld_buffer = []
            else:
                self.in_script = True
        elif tag_lower == "style":
            self.in_style = True
        elif tag_lower == "a":
            href = attr_dict.get("href", "")
            rel = attr_dict.get("rel", "")
            self.links.append({"href": href, "rel": rel, "tag": "a"})
            # Check for author link patterns
            if "author" in rel or "author" in href.lower():
                self.author_candidates.append({
                    "href": href,
                    "source": "rel_author" if "author" in rel else "url_pattern",
                })

    def handle_endtag(self, tag: str):
        tag_lower = tag.lower()
        if tag_lower == "script":
            if self.in_json_ld:
                self.json_ld_blocks.append("".join(self.json_ld_buffer))
                self.in_json_ld = False
            self.in_script = False
        elif tag_lower == "style":
            self.in_style = False

    def handle_data(self, data: str):
        if self.in_json_ld:
            self.json_ld_buffer.append(data)
        elif not self.in_script and not self.in_style:
            stripped = data.strip()
            if stripped:
                self.text_parts.append(stripped)


def check_author_byline(html: str, text: str) -> dict[str, Any]:
    """Check for author byline on the page."""
    result: dict[str, Any] = {"present": False, "name": None}

    # Pattern 1: "by [Name]" or "By [Name]"
    by_match = re.search(
        r'(?:^|\s)(?:by|By|BY)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+){1,3})',
        text
    )
    if by_match:
        result["present"] = True
        result["name"] = by_match.group(1).strip()
        return result

    # Pattern 2: class="author" with text content
    author_class = re.search(
        r'class="[^"]*author[^"]*"[^>]*>([^<]+)',
        html, re.IGNORECASE
    )
    if author_class:
        name = author_class.group(1).strip()
        if len(name) > 2 and len(name) < 60:
            result["present"] = True
            result["name"] = name
            return result

    # Pattern 3: itemprop="author"
    itemprop = re.search(
        r'itemprop="author"[^>]*>([^<]+)',
        html, re.IGNORECASE
    )
    if itemprop:
        result["present"] = True
        result["name"] = itemprop.group(1).strip()
        return result

    return result


def check_author_page(html: str, base_url: str) -> dict[str, Any]:
    """Check if author name links to a dedicated author page."""
    result: dict[str, Any] = {
        "present": False,
        "url": None,
        "has_bio": False,
        "has_photo": False,
        "has_credentials": False,
        "has_social_links": False,
    }

    # Find author page link
    author_link_patterns = [
        r'<a[^>]*href="([^"]*(?:/author/|/team/|/people/|/about/)[^"]*)"',
        r'rel="author"[^>]*href="([^"]*)"',
        r'href="([^"]*)"[^>]*rel="author"',
    ]

    author_url = None
    for pattern in author_link_patterns:
        match = re.search(pattern, html, re.IGNORECASE)
        if match:
            author_url = match.group(1)
            break

    if not author_url:
        return result

    # Resolve relative URL
    if author_url.startswith("/"):
        parsed = urllib.parse.urlparse(base_url)
        author_url = f"{parsed.scheme}://{parsed.netloc}{author_url}"

    result["present"] = True
    result["url"] = author_url

    # Fetch author page to check quality
    author_html = fetch_page(author_url)
    if not author_html:
        return result

    author_text = re.sub(r'<[^>]+>', ' ', author_html)
    author_words = len(author_text.split())

    # Check for bio (>50 words of content)
    result["has_bio"] = author_words > 100

    # Check for photo
    result["has_photo"] = bool(re.search(
        r'<img[^>]*(?:author|avatar|headshot|photo|profile)',
        author_html, re.IGNORECASE
    ))

    # Check for credentials
    result["has_credentials"] = bool(re.search(
        r'(?:CEO|CTO|VP|Director|Head|Chief|Professor|Dr\.|PhD|'
        r'Founder|Manager|Lead|Senior|Principal|Analyst|Consultant|'
        r'Engineer|Architect|Editor)',
        author_html
    ))

    # Check for social links
    social_domains = ["linkedin.com", "twitter.com", "x.com", "github.com"]
    result["has_social_links"] = any(
        domain in author_html.lower() for domain in social_domains
    )

    return result


def check_external_citations(links: list[dict], base_url: str) -> dict[str, Any]:
    """Count external citations (excluding social/nav links)."""
    parsed_base = urllib.parse.urlparse(base_url)
    base_domain = parsed_base.netloc.lower()

    excluded_domains = [
        "twitter.com", "x.com", "facebook.com", "instagram.com",
        "youtube.com", "tiktok.com", "pinterest.com",
    ]

    external = []
    for link in links:
        href = link.get("href", "")
        if not href.startswith("http"):
            continue
        parsed = urllib.parse.urlparse(href)
        domain = parsed.netloc.lower()
        if domain == base_domain:
            continue
        if any(d in domain for d in excluded_domains):
            continue
        external.append(domain)

    unique_domains = list(set(external))

    return {
        "count": len(external),
        "unique_domains": len(unique_domains),
        "domains": unique_domains[:10],
    }


def check_visible_dates(html: str, json_ld_blocks: list[str]) -> dict[str, Any]:
    """Check for visible publication and modification dates."""
    result: dict[str, Any] = {
        "published": None,
        "modified": None,
        "visible_date_text": None,
    }

    # Check JSON-LD for dates
    for block in json_ld_blocks:
        try:
            data = json.loads(block)
            if isinstance(data, dict):
                if "datePublished" in data:
                    result["published"] = data["datePublished"]
                if "dateModified" in data:
                    result["modified"] = data["dateModified"]
        except json.JSONDecodeError:
            pass

    # Check for visible date text
    date_patterns = [
        r'(?:last\s+)?(?:updated|modified)\s*:?\s*(?:on\s+)?'
        r'(\d{4}[-/]\d{1,2}[-/]\d{1,2}|'
        r'(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{1,2},?\s+\d{4})',

        r'(?:published|posted)\s*:?\s*(?:on\s+)?'
        r'(\d{4}[-/]\d{1,2}[-/]\d{1,2}|'
        r'(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{1,2},?\s+\d{4})',
    ]

    for pattern in date_patterns:
        match = re.search(pattern, html, re.IGNORECASE)
        if match:
            result["visible_date_text"] = match.group(0).strip()
            break

    return result


def check_editorial_policy(html: str) -> dict[str, Any]:
    """Check for editorial policy link."""
    patterns = [
        r'href="[^"]*(?:editorial[- ]?policy|about/editorial|our-process|'
        r'fact[- ]?check|methodology|how-we-review)',
    ]
    found = any(re.search(p, html, re.IGNORECASE) for p in patterns)
    return {"found": found}


def check_contact_page(html: str) -> dict[str, Any]:
    """Check for contact page link or visible contact info."""
    has_contact_link = bool(re.search(
        r'href="[^"]*(?:/contact|/about|/support)',
        html, re.IGNORECASE
    ))
    has_email = bool(re.search(
        r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}',
        html
    ))
    return {
        "found": has_contact_link or has_email,
        "has_contact_link": has_contact_link,
        "has_email": has_email,
    }


def assess_eeat(signals: dict) -> str:
    """Assess overall E-E-A-T strength."""
    score = 0

    if signals["author_byline"]["present"]:
        score += 2
    if signals["author_page"]["present"]:
        score += 1
        if signals["author_page"].get("has_bio"):
            score += 1
        if signals["author_page"].get("has_credentials"):
            score += 1
        if signals["author_page"].get("has_social_links"):
            score += 1
    if signals["external_citations"]["count"] >= 3:
        score += 2
    elif signals["external_citations"]["count"] >= 1:
        score += 1
    if signals["visible_dates"]["published"] or signals["visible_dates"]["visible_date_text"]:
        score += 1
    if signals["visible_dates"]["modified"]:
        score += 1
    if signals["editorial_policy"]["found"]:
        score += 1
    if signals["contact_page"]["found"]:
        score += 1

    if score >= 10:
        return "strong"
    elif score >= 6:
        return "moderate"
    elif score >= 3:
        return "weak"
    else:
        return "missing"


def main():
    parser = argparse.ArgumentParser(
        description="Check E-E-A-T signal presence on a page.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Checks:
  - Author byline (name visible near content)
  - Author page (linked bio with photo, credentials, social links)
  - External citations (outbound links to authoritative sources)
  - Visible dates (published, modified, last updated)
  - Editorial policy (link to methodology/process page)
  - Contact information (contact page or email)

Examples:
    python check-eeat-signals.py --url https://example.com/article
        """,
    )
    parser.add_argument(
        "--url",
        required=True,
        help="URL to check for E-E-A-T signals",
    )
    parser.add_argument(
        "--tools",
        help="Path to tools.json inventory file",
    )
    args = parser.parse_args()

    tools = load_tools(args.tools)

    # Fetch the page
    print(f"Fetching: {args.url}", file=sys.stderr)
    html = fetch_page(args.url)
    if not html:
        output = {"url": args.url, "error": "Failed to fetch page"}
        print(json.dumps(output, indent=2))
        sys.exit(1)

    # Parse HTML
    content = EEATParser()
    try:
        content.feed(html)
    except Exception:
        pass

    full_text = " ".join(content.text_parts)

    # Run all checks
    signals = {
        "author_byline": check_author_byline(html, full_text),
        "author_page": check_author_page(html, args.url),
        "external_citations": check_external_citations(content.links, args.url),
        "visible_dates": check_visible_dates(html, content.json_ld_blocks),
        "editorial_policy": check_editorial_policy(html),
        "contact_page": check_contact_page(html),
    }

    eeat_score = assess_eeat(signals)

    # Identify missing signals
    missing = []
    if not signals["author_byline"]["present"]:
        missing.append("author_byline")
    if not signals["author_page"]["present"]:
        missing.append("author_page")
    elif not signals["author_page"].get("has_bio"):
        missing.append("author_bio")
    elif not signals["author_page"].get("has_credentials"):
        missing.append("author_credentials")
    if signals["external_citations"]["count"] < 3:
        missing.append("external_citations (need 3+)")
    if not signals["visible_dates"]["published"] and not signals["visible_dates"]["visible_date_text"]:
        missing.append("visible_dates")
    if not signals["editorial_policy"]["found"]:
        missing.append("editorial_policy")
    if not signals["contact_page"]["found"]:
        missing.append("contact_page")

    output = {
        "url": args.url,
        "signals": signals,
        "eeat_score": eeat_score,
        "missing": missing,
        "tools_used": {
            "webfetch": True,
        },
    }
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
