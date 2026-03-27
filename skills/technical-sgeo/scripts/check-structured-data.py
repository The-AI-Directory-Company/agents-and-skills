#!/usr/bin/env python3
"""
check-structured-data.py — Extract and validate JSON-LD structured data from a page.

Fetches a page, finds all <script type="application/ld+json"> blocks, parses the
JSON-LD, identifies schema types, and validates required/recommended properties
per type. Flags common errors and checks rich result eligibility.

Usage:
    python3 check-structured-data.py --url https://example.com
    python3 check-structured-data.py --url https://example.com/product/widget

AI Agent Usage:
    Agents should use WebFetch to get the page HTML, then search for all
    <script type="application/ld+json"> blocks, parse the JSON content, and
    validate against the property requirements in references/structured-data.md.
"""

import argparse
import json
import sys
import urllib.request
import urllib.error
import re


# Required and recommended properties per schema type
SCHEMA_PROPERTIES = {
    "Organization": {
        "required": ["name", "url"],
        "recommended": ["logo", "sameAs", "contactPoint", "description"],
        "rich_result": "Knowledge Panel",
    },
    "Product": {
        "required": ["name", "image", "offers"],
        "recommended": ["description", "brand", "sku", "aggregateRating", "review"],
        "rich_result": "Product snippet",
    },
    "Article": {
        "required": ["headline", "datePublished", "author", "image"],
        "recommended": ["dateModified", "publisher", "description"],
        "rich_result": "Article snippet",
    },
    "NewsArticle": {
        "required": ["headline", "datePublished", "author", "image"],
        "recommended": ["dateModified", "publisher", "description"],
        "rich_result": "News article snippet",
    },
    "BlogPosting": {
        "required": ["headline", "datePublished", "author", "image"],
        "recommended": ["dateModified", "publisher", "description"],
        "rich_result": "Article snippet",
    },
    "FAQPage": {
        "required": ["mainEntity"],
        "recommended": [],
        "rich_result": "FAQ rich result (limited eligibility since 2023)",
    },
    "HowTo": {
        "required": ["name", "step"],
        "recommended": ["totalTime", "image", "description"],
        "rich_result": "How-to snippet",
    },
    "LocalBusiness": {
        "required": ["name", "address"],
        "recommended": ["telephone", "openingHoursSpecification", "geo", "image"],
        "rich_result": "Local pack",
    },
    "Service": {
        "required": ["name"],
        "recommended": ["description", "provider", "areaServed", "serviceType"],
        "rich_result": None,
    },
    "BreadcrumbList": {
        "required": ["itemListElement"],
        "recommended": [],
        "rich_result": "Breadcrumb trail",
    },
    "WebSite": {
        "required": ["name", "url"],
        "recommended": ["potentialAction"],
        "rich_result": "Sitelinks searchbox",
    },
}


def fetch_page(url, timeout=15):
    """Fetch page HTML. Returns (html_string, error)."""
    try:
        req = urllib.request.Request(url)
        req.add_header("User-Agent", "Mozilla/5.0 (compatible; check-structured-data/1.0)")
        response = urllib.request.urlopen(req, timeout=timeout)
        html = response.read().decode("utf-8", errors="replace")
        return html, None
    except urllib.error.HTTPError as e:
        return None, f"HTTP {e.code}"
    except Exception as e:
        return None, str(e)


def extract_jsonld_blocks(html):
    """Extract all JSON-LD script blocks from HTML."""
    pattern = re.compile(
        r'<script[^>]*type=["\']application/ld\+json["\'][^>]*>(.*?)</script>',
        re.DOTALL | re.IGNORECASE
    )
    matches = pattern.findall(html)
    blocks = []
    for match in matches:
        try:
            data = json.loads(match.strip())
            blocks.append({"parsed": True, "data": data, "raw_length": len(match.strip())})
        except json.JSONDecodeError as e:
            blocks.append({"parsed": False, "error": f"Invalid JSON: {str(e)}", "raw": match.strip()[:200]})
    return blocks


def get_schema_type(data):
    """Extract @type from a JSON-LD object. Handles string and list types."""
    schema_type = data.get("@type", "Unknown")
    if isinstance(schema_type, list):
        return schema_type[0] if schema_type else "Unknown"
    return schema_type


def get_properties(data):
    """Get all top-level property names from a JSON-LD object."""
    return [k for k in data.keys() if not k.startswith("@")]


def validate_schema(data):
    """Validate a single JSON-LD schema object. Returns validation result dict."""
    schema_type = get_schema_type(data)
    properties = get_properties(data)
    context = data.get("@context", "")

    errors = []
    warnings = []

    # Check @context
    if not context:
        errors.append("Missing @context — must be 'https://schema.org'")
    elif "schema.org" not in str(context):
        errors.append(f"Invalid @context: {context} — should be 'https://schema.org'")

    # Check @type
    if schema_type == "Unknown":
        errors.append("Missing @type property")

    # Validate against known schema types
    type_spec = SCHEMA_PROPERTIES.get(schema_type)
    missing_required = []
    missing_recommended = []

    if type_spec:
        for prop in type_spec["required"]:
            if prop not in properties:
                missing_required.append(prop)
                errors.append(f"Missing required property: {prop}")

        for prop in type_spec["recommended"]:
            if prop not in properties:
                missing_recommended.append(prop)
                warnings.append(f"Missing recommended property: {prop}")

    # Check common issues
    # Author should be Person object, not string
    author = data.get("author")
    if isinstance(author, str):
        warnings.append("Author should be a Person object with name, jobTitle, and url — not a plain string")

    # Check for nested types
    if schema_type in ("Article", "BlogPosting", "NewsArticle"):
        publisher = data.get("publisher")
        if publisher and not isinstance(publisher, dict):
            warnings.append("Publisher should be an Organization object, not a string")
        elif publisher and publisher.get("@type") != "Organization":
            warnings.append("Publisher @type should be 'Organization'")

    # Offer inside Product
    if schema_type == "Product":
        offers = data.get("offers")
        if offers and isinstance(offers, dict):
            if "price" not in offers and "lowPrice" not in offers:
                warnings.append("Offer is missing price or lowPrice")
            if "priceCurrency" not in offers:
                warnings.append("Offer is missing priceCurrency")

    result = {
        "type": schema_type,
        "valid": len(errors) == 0,
        "properties_found": properties,
        "missing_required": missing_required,
        "missing_recommended": missing_recommended,
        "errors": errors,
        "warnings": warnings,
        "rich_result": type_spec["rich_result"] if type_spec else None,
        "rich_result_eligible": len(errors) == 0 and type_spec is not None and type_spec.get("rich_result") is not None,
    }

    return result


def process_jsonld(block_data):
    """Process a JSON-LD block which may contain a single object or @graph array."""
    results = []

    if isinstance(block_data, list):
        for item in block_data:
            results.append(validate_schema(item))
    elif isinstance(block_data, dict):
        if "@graph" in block_data:
            for item in block_data["@graph"]:
                if isinstance(item, dict):
                    results.append(validate_schema(item))
        else:
            results.append(validate_schema(block_data))

    return results


def main():
    parser = argparse.ArgumentParser(
        description="Extract and validate JSON-LD structured data from a web page.",
        epilog="Output: JSON report with schema types found, validation results, and rich result eligibility."
    )
    parser.add_argument("--url", required=True, help="URL to check")
    parser.add_argument("--tools", help="Path to tools.json from inventory-tools.py")
    args = parser.parse_args()

    # Fetch page
    html, error = fetch_page(args.url)
    if error:
        print(json.dumps({
            "url": args.url,
            "error": error,
            "schemas_found": [],
            "recommendation": "Could not fetch page. Verify URL is accessible and returns HTML."
        }, indent=2))
        return

    # Extract JSON-LD blocks
    blocks = extract_jsonld_blocks(html)

    if not blocks:
        print(json.dumps({
            "url": args.url,
            "schemas_found": [],
            "total_blocks": 0,
            "recommendation": "No JSON-LD structured data found. Add schema markup per references/structured-data.md."
        }, indent=2))
        return

    # Validate each block
    all_results = []
    parse_errors = 0

    for block in blocks:
        if not block["parsed"]:
            parse_errors += 1
            all_results.append({
                "type": "ParseError",
                "valid": False,
                "errors": [block["error"]],
                "raw_preview": block.get("raw", "")[:100],
            })
        else:
            results = process_jsonld(block["data"])
            all_results.extend(results)

    # Summary
    types_found = [r["type"] for r in all_results if r.get("type") != "ParseError"]
    has_errors = any(not r["valid"] for r in all_results)
    rich_result_eligible = any(r.get("rich_result_eligible") for r in all_results)

    output = {
        "url": args.url,
        "total_blocks": len(blocks),
        "parse_errors": parse_errors,
        "schemas_found": all_results,
        "types_present": list(set(types_found)),
        "has_errors": has_errors,
        "rich_result_eligible": rich_result_eligible,
        "validation_url": f"https://search.google.com/test/rich-results?url={urllib.request.quote(args.url, safe='')}",
    }

    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
