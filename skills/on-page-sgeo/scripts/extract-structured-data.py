#!/usr/bin/env python3
"""Extract and validate JSON-LD structured data from a URL.

Parses all <script type="application/ld+json"> blocks, identifies schema
types, and validates required properties against a page-type mapping.

Usage:
    python extract-structured-data.py --url https://example.com/page
    python extract-structured-data.py --url https://example.com/page --tools tools.json

Output: JSON with extracted schemas, validation results, and issues.
"""

import argparse
import json
import re
import sys
from html.parser import HTMLParser
from typing import Optional


# ---------------------------------------------------------------------------
# Required/recommended properties per schema type
# ---------------------------------------------------------------------------

SCHEMA_REQUIREMENTS: dict[str, dict] = {
    "Article": {
        "required": ["headline", "author", "datePublished"],
        "recommended": ["dateModified", "image", "publisher"],
    },
    "BlogPosting": {
        "required": ["headline", "author", "datePublished"],
        "recommended": ["dateModified", "image", "publisher"],
    },
    "NewsArticle": {
        "required": ["headline", "author", "datePublished"],
        "recommended": ["dateModified", "image", "publisher"],
    },
    "Product": {
        "required": ["name", "offers"],
        "recommended": ["description", "image", "aggregateRating", "review", "brand"],
    },
    "FAQPage": {
        "required": ["mainEntity"],
        "recommended": [],
    },
    "Organization": {
        "required": ["name", "url"],
        "recommended": ["logo", "sameAs", "contactPoint"],
    },
    "LocalBusiness": {
        "required": ["name", "address"],
        "recommended": ["telephone", "openingHoursSpecification", "geo"],
    },
    "HowTo": {
        "required": ["name", "step"],
        "recommended": ["image", "totalTime"],
    },
    "Person": {
        "required": ["name"],
        "recommended": ["jobTitle", "worksFor", "sameAs", "url"],
    },
    "Event": {
        "required": ["name", "startDate", "location"],
        "recommended": ["endDate", "offers", "performer", "image"],
    },
    "BreadcrumbList": {
        "required": ["itemListElement"],
        "recommended": [],
    },
    "WebSite": {
        "required": ["name", "url"],
        "recommended": ["potentialAction"],
    },
    "Service": {
        "required": ["name"],
        "recommended": ["description", "provider", "areaServed", "serviceType"],
    },
}


# ---------------------------------------------------------------------------
# HTML Parser
# ---------------------------------------------------------------------------

class JsonLdExtractor(HTMLParser):
    """Extract JSON-LD script blocks from HTML."""

    def __init__(self):
        super().__init__()
        self.blocks: list[str] = []
        self._in_jsonld = False
        self._current = ""

    def handle_starttag(self, tag: str, attrs):
        if tag == "script":
            attr_dict = {k: (v or "").lower() for k, v in attrs}
            if attr_dict.get("type") == "application/ld+json":
                self._in_jsonld = True
                self._current = ""

    def handle_data(self, data: str):
        if self._in_jsonld:
            self._current += data

    def handle_endtag(self, tag: str):
        if tag == "script" and self._in_jsonld:
            self._in_jsonld = False
            if self._current.strip():
                self.blocks.append(self._current.strip())


# ---------------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------------

def get_type(obj: dict) -> Optional[str]:
    """Extract @type from a JSON-LD object."""
    t = obj.get("@type", "")
    if isinstance(t, list):
        return t[0] if t else None
    return t or None


def get_flat_keys(obj: dict) -> set[str]:
    """Get top-level keys of a JSON-LD object (excluding @context, @type)."""
    return {k for k in obj.keys() if not k.startswith("@")}


def validate_schema(obj: dict) -> dict:
    """Validate a single JSON-LD object against known requirements."""
    schema_type = get_type(obj)
    if not schema_type:
        return {
            "type": None,
            "valid": False,
            "error": "Missing @type",
            "properties": {},
            "missing_required": [],
            "missing_recommended": [],
        }

    keys = get_flat_keys(obj)
    reqs = SCHEMA_REQUIREMENTS.get(schema_type, {"required": [], "recommended": []})

    missing_required = [p for p in reqs["required"] if p not in keys]
    missing_recommended = [p for p in reqs["recommended"] if p not in keys]

    # Extract key property values for display
    props = {}
    for k in ["name", "headline", "datePublished", "dateModified", "url"]:
        if k in obj and isinstance(obj[k], str):
            props[k] = obj[k]

    return {
        "type": schema_type,
        "valid": len(missing_required) == 0,
        "properties": props,
        "missing_required": missing_required,
        "missing_recommended": missing_recommended,
    }


def analyze(url: str, html: str) -> dict:
    parser = JsonLdExtractor()
    parser.feed(html)

    schemas = []
    issues: list[str] = []

    if not parser.blocks:
        issues.append("No JSON-LD structured data found on this page")

    for i, block in enumerate(parser.blocks):
        try:
            data = json.loads(block)
        except json.JSONDecodeError as e:
            issues.append(f"JSON-LD block {i + 1}: Invalid JSON — {e}")
            schemas.append({"type": None, "valid": False, "error": f"Invalid JSON: {e}"})
            continue

        # Handle @graph arrays
        if isinstance(data, dict) and "@graph" in data:
            for item in data["@graph"]:
                if isinstance(item, dict):
                    result = validate_schema(item)
                    schemas.append(result)
        elif isinstance(data, list):
            for item in data:
                if isinstance(item, dict):
                    result = validate_schema(item)
                    schemas.append(result)
        elif isinstance(data, dict):
            if "@context" not in data:
                issues.append(f"JSON-LD block {i + 1}: Missing @context")
            result = validate_schema(data)
            schemas.append(result)

    # Check for dateModified in Article schemas
    for s in schemas:
        if s.get("type") in ("Article", "BlogPosting", "NewsArticle"):
            if "dateModified" in s.get("missing_recommended", []):
                issues.append(
                    f"{s['type']} schema missing dateModified — "
                    "critical for freshness signals in both SEO and GEO"
                )

    # Check for FAQPage (GEO opportunity)
    has_faq = any(s.get("type") == "FAQPage" for s in schemas)

    return {
        "url": url,
        "total_schemas": len(schemas),
        "schemas": schemas,
        "has_faq_schema": has_faq,
        "issues": issues,
    }


# ---------------------------------------------------------------------------
# Fetch
# ---------------------------------------------------------------------------

def fetch_html(url: str) -> str:
    from urllib.request import Request, urlopen
    req = Request(url, headers={"User-Agent": "Mozilla/5.0 (compatible; on-page-sgeo-audit/1.0)"})
    with urlopen(req, timeout=15) as resp:
        return resp.read().decode("utf-8", errors="replace")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser(description="Extract and validate JSON-LD structured data")
    ap.add_argument("--url", required=True, help="Page URL to analyze")
    ap.add_argument("--tools", default=None, help="Path to tools.json inventory file")
    args = ap.parse_args()

    try:
        html = fetch_html(args.url)
    except Exception as e:
        print(json.dumps({"error": f"Failed to fetch URL: {e}", "url": args.url}), file=sys.stderr)
        sys.exit(1)

    result = analyze(args.url, html)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
