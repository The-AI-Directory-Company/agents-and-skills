#!/usr/bin/env python3
"""
check-indexation.py — Estimate indexation status by comparing site: search results against sitemap count.

Uses WebSearch (site:domain.com) to estimate how many pages are indexed, then
compares against the sitemap URL count. Flags discrepancies that indicate
duplicate content or indexation problems.

Usage:
    python3 check-indexation.py --domain example.com
    python3 check-indexation.py --domain example.com --sitemap-count 847
    python3 check-indexation.py --domain example.com --sections /blog /products /docs

AI Agent Usage:
    Agents should use WebSearch to run "site:domain.com" and extract the
    approximate result count. Then compare against the sitemap URL count
    (from validate-sitemap.py output). Large discrepancies indicate problems:
    - indexed >> sitemap = duplicate content, parameter URLs being indexed
    - indexed << sitemap = indexation issues, thin content, crawl budget problems
"""

import argparse
import json
import sys
import urllib.request
import urllib.error
import re
import time


def search_site(query, timeout=15):
    """
    Search for a query and try to extract result count.
    This is a simplified implementation — real agents should use WebSearch tool.
    Returns (estimated_count, raw_response_snippet, error).

    WARNING: The HTML scraping path below (fetching google.com/search and
    parsing "About X results") is unreliable. Google frequently changes its
    markup, serves CAPTCHAs, and rate-limits automated requests. Agents
    should prefer the WebSearch-based approach: run WebSearch with
    "site:<domain>" and read the result count from the tool output. The
    fallback_instructions in main() describe this path. This function
    exists only as a best-effort fallback when no WebSearch tool is
    available.
    """
    # URL-encode the query
    encoded = urllib.request.quote(query)
    url = f"https://www.google.com/search?q={encoded}&num=10"

    try:
        req = urllib.request.Request(url)
        req.add_header("User-Agent", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36")
        req.add_header("Accept-Language", "en-US,en;q=0.9")
        response = urllib.request.urlopen(req, timeout=timeout)
        html = response.read().decode("utf-8", errors="replace")

        # Try to extract result count from "About X results" text
        count_patterns = [
            r'About ([\d,]+) results',
            r'about ([\d,]+) results',
            r'"resultStats">About ([\d,]+)',
            r'([\d,]+) results',
        ]

        for pattern in count_patterns:
            match = re.search(pattern, html, re.IGNORECASE)
            if match:
                count_str = match.group(1).replace(",", "")
                return int(count_str), match.group(0), None

        # If no count found, check if there are any results at all
        if "did not match any documents" in html.lower():
            return 0, "No results found", None

        return None, "Could not extract result count from search page", "extraction_failed"

    except urllib.error.HTTPError as e:
        if e.code == 429:
            return None, None, "Rate limited by Google. Use WebSearch tool or wait and retry."
        return None, None, f"HTTP {e.code}"
    except Exception as e:
        return None, None, str(e)


def assess_ratio(indexed, sitemap_count):
    """Assess the indexed/sitemap ratio and provide diagnosis."""
    if not indexed or not sitemap_count or sitemap_count == 0:
        return "unknown", "Cannot compute ratio without both counts."

    ratio = indexed / sitemap_count

    if ratio > 2.0:
        return "over_indexed", (
            f"Ratio {ratio:.1f}x — significantly more pages indexed ({indexed}) than in sitemap ({sitemap_count}). "
            "Likely causes: duplicate content from URL parameters, faceted navigation, "
            "www/non-www or trailing slash variations being indexed separately. "
            "Check canonical tags and robots.txt."
        )
    elif ratio > 1.3:
        return "slightly_over", (
            f"Ratio {ratio:.1f}x — somewhat more pages indexed ({indexed}) than in sitemap ({sitemap_count}). "
            "Minor duplicate content or parameter URLs may be indexed. Review canonical tags."
        )
    elif ratio > 0.7:
        return "healthy", (
            f"Ratio {ratio:.1f}x — indexed count ({indexed}) approximately matches sitemap ({sitemap_count}). "
            "Indexation appears healthy."
        )
    elif ratio > 0.3:
        return "under_indexed", (
            f"Ratio {ratio:.1f}x — fewer pages indexed ({indexed}) than in sitemap ({sitemap_count}). "
            "Check GSC index coverage for 'Discovered - not indexed' and 'Crawled - not indexed' entries. "
            "Common causes: thin content, crawl budget exhaustion, internal linking gaps."
        )
    else:
        return "severely_under_indexed", (
            f"Ratio {ratio:.1f}x — far fewer pages indexed ({indexed}) than in sitemap ({sitemap_count}). "
            "Serious indexation problem. Check for: robots.txt blocking, noindex tags, "
            "server errors, JavaScript rendering issues, or a recent migration without redirects."
        )


def main():
    parser = argparse.ArgumentParser(
        description="Estimate indexation status by comparing site: search results against sitemap count.",
        epilog="Output: JSON report with estimated indexed pages, sitemap comparison, and indexation diagnosis."
    )
    parser.add_argument("--domain", required=True, help="Domain to check (e.g., example.com)")
    parser.add_argument("--sitemap-count", type=int, help="Known sitemap URL count (from validate-sitemap.py)")
    parser.add_argument("--sections", nargs="*", help="URL path sections to check individually (e.g., /blog /products)")
    parser.add_argument("--tools", help="Path to tools.json from inventory-tools.py")
    args = parser.parse_args()

    domain = args.domain.replace("https://", "").replace("http://", "").rstrip("/")

    # Check overall site indexation
    query = f"site:{domain}"
    estimated, raw, error = search_site(query)

    if error == "extraction_failed":
        # Provide fallback instructions for agents
        result = {
            "domain": domain,
            "query": query,
            "estimated_indexed": None,
            "error": "Could not extract result count from Google search page.",
            "fallback_instructions": [
                "Use WebSearch tool to search 'site:{domain}' and note the result count.",
                "Or check Google Search Console > Pages > Indexing for exact indexed page count.",
                "Or use DataForSEO SERP API if available.",
            ]
        }
        print(json.dumps(result, indent=2))
        return
    elif error:
        result = {
            "domain": domain,
            "query": query,
            "estimated_indexed": None,
            "error": error,
            "fallback_instructions": [
                "Use WebSearch tool to search 'site:{domain}' and note the result count.",
                "Google Search Console > Pages > Indexing provides exact counts.",
            ]
        }
        print(json.dumps(result, indent=2))
        return

    # Assess ratio if sitemap count is known
    status = "unknown"
    diagnosis = ""
    if args.sitemap_count:
        status, diagnosis = assess_ratio(estimated, args.sitemap_count)

    result = {
        "domain": domain,
        "estimated_indexed": estimated,
        "sitemap_count": args.sitemap_count,
        "ratio": round(estimated / args.sitemap_count, 2) if estimated and args.sitemap_count else None,
        "status": status,
        "diagnosis": diagnosis,
    }

    # Check sections if requested
    if args.sections:
        section_results = []
        for section in args.sections:
            time.sleep(2)  # Rate limiting
            section_query = f"site:{domain}{section}"
            sec_estimated, sec_raw, sec_error = search_site(section_query)
            section_results.append({
                "path": section,
                "query": section_query,
                "estimated_indexed": sec_estimated,
                "error": sec_error,
            })
        result["section_checks"] = section_results

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
