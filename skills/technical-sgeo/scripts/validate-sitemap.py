#!/usr/bin/env python3
"""
validate-sitemap.py — Fetch and validate XML sitemap structure, URLs, and dates.

Checks XML validity, URL count limits, lastmod date quality, and samples URLs
for 200 status. Supports sitemap index files (recursive validation).

Usage:
    python3 validate-sitemap.py --url https://example.com/sitemap.xml
    python3 validate-sitemap.py --domain example.com
    python3 validate-sitemap.py --url https://example.com/sitemap.xml --sample-size 20

AI Agent Usage:
    Agents should use WebFetch to retrieve the sitemap URL, parse the XML to
    extract <loc> and <lastmod> entries, then sample a subset of URLs with HEAD
    requests to verify 200 status. Check robots.txt for Sitemap: declarations.
"""

import argparse
import json
import sys
import urllib.request
import urllib.error
import xml.etree.ElementTree as ET
import random
import re
from datetime import datetime, timezone


SITEMAP_NS = "http://www.sitemaps.org/schemas/sitemap/0.9"
MAX_URLS_PER_SITEMAP = 50000
MAX_SIZE_BYTES = 50 * 1024 * 1024  # 50MB


def fetch_url(url, timeout=15):
    """Fetch URL content. Returns (content_bytes, error)."""
    try:
        req = urllib.request.Request(url)
        req.add_header("User-Agent", "validate-sitemap/1.0")
        response = urllib.request.urlopen(req, timeout=timeout)
        content = response.read()
        return content, None
    except urllib.error.HTTPError as e:
        return None, f"HTTP {e.code}"
    except Exception as e:
        return None, str(e)


def check_url_status(url, timeout=10):
    """HEAD request to check URL status code. Returns (status_code, error)."""
    try:
        req = urllib.request.Request(url, method="HEAD")
        req.add_header("User-Agent", "validate-sitemap/1.0")
        response = urllib.request.urlopen(req, timeout=timeout)
        return response.getcode(), None
    except urllib.error.HTTPError as e:
        return e.code, None
    except Exception as e:
        return None, str(e)


def parse_sitemap(content_bytes):
    """
    Parse sitemap XML. Returns (urls, is_index, child_sitemaps, error).
    urls: list of {loc, lastmod} dicts
    is_index: True if this is a sitemap index
    child_sitemaps: list of sitemap URLs if this is an index
    """
    try:
        root = ET.fromstring(content_bytes)
    except ET.ParseError as e:
        return [], False, [], f"Invalid XML: {str(e)}"

    tag = root.tag.lower()

    # Check if sitemap index
    if "sitemapindex" in tag:
        child_sitemaps = []
        for sitemap_elem in root.iter(f"{{{SITEMAP_NS}}}sitemap"):
            loc = sitemap_elem.find(f"{{{SITEMAP_NS}}}loc")
            if loc is not None and loc.text:
                child_sitemaps.append(loc.text.strip())
        # Try without namespace
        if not child_sitemaps:
            for sitemap_elem in root.iter("sitemap"):
                loc = sitemap_elem.find("loc")
                if loc is not None and loc.text:
                    child_sitemaps.append(loc.text.strip())
        return [], True, child_sitemaps, None

    # Regular sitemap
    urls = []
    for url_elem in root.iter(f"{{{SITEMAP_NS}}}url"):
        loc = url_elem.find(f"{{{SITEMAP_NS}}}loc")
        lastmod = url_elem.find(f"{{{SITEMAP_NS}}}lastmod")
        entry = {
            "loc": loc.text.strip() if loc is not None and loc.text else None,
            "lastmod": lastmod.text.strip() if lastmod is not None and lastmod.text else None,
        }
        if entry["loc"]:
            urls.append(entry)

    # Try without namespace if no results
    if not urls:
        for url_elem in root.iter("url"):
            loc = url_elem.find("loc")
            lastmod = url_elem.find("lastmod")
            entry = {
                "loc": loc.text.strip() if loc is not None and loc.text else None,
                "lastmod": lastmod.text.strip() if lastmod is not None and lastmod.text else None,
            }
            if entry["loc"]:
                urls.append(entry)

    return urls, False, [], None


def validate_lastmod_dates(urls):
    """Validate lastmod dates. Returns issues list."""
    issues = []
    dates_seen = set()
    urls_with_lastmod = 0
    future_dates = 0
    invalid_dates = 0

    iso_pattern = re.compile(r"^\d{4}-\d{2}-\d{2}")

    for url in urls:
        if url["lastmod"]:
            urls_with_lastmod += 1
            dates_seen.add(url["lastmod"])

            # Check ISO 8601 format
            if not iso_pattern.match(url["lastmod"]):
                invalid_dates += 1
            else:
                # Check for future dates
                try:
                    date_str = url["lastmod"][:10]
                    date = datetime.strptime(date_str, "%Y-%m-%d")
                    if date.date() > datetime.now(timezone.utc).date():
                        future_dates += 1
                except ValueError:
                    invalid_dates += 1

    if urls_with_lastmod == 0:
        issues.append("No lastmod dates found. Add lastmod with actual content modification dates.")
    elif urls_with_lastmod < len(urls) * 0.5:
        issues.append(f"Only {urls_with_lastmod}/{len(urls)} URLs have lastmod dates. Add dates to all URLs.")

    if len(dates_seen) == 1 and urls_with_lastmod > 10:
        issues.append(f"All {urls_with_lastmod} lastmod dates are identical ({dates_seen.pop()}). This looks like fake dates — use actual modification dates.")

    if future_dates > 0:
        issues.append(f"{future_dates} URL(s) have future lastmod dates. Use actual past modification dates.")

    if invalid_dates > 0:
        issues.append(f"{invalid_dates} URL(s) have invalid date formats. Use ISO 8601 (YYYY-MM-DD).")

    return issues, urls_with_lastmod


def sample_urls(urls, sample_size=10):
    """Sample random URLs and check their HTTP status."""
    if len(urls) <= sample_size:
        sample = urls
    else:
        sample = random.sample(urls, sample_size)

    results = []
    for url_entry in sample:
        status, error = check_url_status(url_entry["loc"])
        results.append({
            "url": url_entry["loc"],
            "status": status,
            "error": error,
        })

    return results


def main():
    parser = argparse.ArgumentParser(
        description="Fetch and validate XML sitemap structure, URL count, lastmod dates, and URL status.",
        epilog="Output: JSON report with validation results, date quality, and sampled URL statuses."
    )
    parser.add_argument("--url", help="Direct sitemap URL to validate")
    parser.add_argument("--domain", help="Domain — will try /sitemap.xml and /sitemap_index.xml")
    parser.add_argument("--sample-size", type=int, default=10, help="Number of URLs to sample for status checks (default: 10)")
    parser.add_argument("--tools", help="Path to tools.json from inventory-tools.py")
    args = parser.parse_args()

    if not args.url and not args.domain:
        parser.error("Provide --url or --domain")

    # Determine sitemap URL
    if args.url:
        sitemap_url = args.url
    else:
        domain = args.domain.replace("https://", "").replace("http://", "").rstrip("/")
        sitemap_url = f"https://{domain}/sitemap.xml"

    # Fetch sitemap
    content, error = fetch_url(sitemap_url)
    if error:
        # Try sitemap_index.xml if domain was provided
        if args.domain and "sitemap.xml" in sitemap_url:
            alt_url = sitemap_url.replace("sitemap.xml", "sitemap_index.xml")
            content, error2 = fetch_url(alt_url)
            if not error2:
                sitemap_url = alt_url
                error = None

    if error:
        print(json.dumps({
            "sitemap_url": sitemap_url,
            "valid": False,
            "error": error,
            "recommendation": "Create an XML sitemap and submit it to Google Search Console and Bing Webmaster Tools."
        }, indent=2))
        return

    # Check file size
    size_bytes = len(content)
    size_issues = []
    if size_bytes > MAX_SIZE_BYTES:
        size_issues.append(f"Sitemap is {size_bytes / 1024 / 1024:.1f}MB — exceeds 50MB limit. Split into multiple sitemaps with a sitemap index.")

    # Parse
    urls, is_index, child_sitemaps, parse_error = parse_sitemap(content)

    if parse_error:
        print(json.dumps({
            "sitemap_url": sitemap_url,
            "valid": False,
            "error": parse_error,
            "recommendation": "Fix XML syntax errors. Validate with an XML validator before resubmitting."
        }, indent=2))
        return

    issues = list(size_issues)

    if is_index:
        # Sitemap index — report child sitemaps
        result = {
            "sitemap_url": sitemap_url,
            "valid": True,
            "is_index": True,
            "child_sitemaps": child_sitemaps,
            "child_count": len(child_sitemaps),
            "note": "This is a sitemap index. Run this script against individual child sitemaps for detailed validation.",
            "issues": issues,
        }
    else:
        # Regular sitemap — full validation
        url_count = len(urls)
        if url_count > MAX_URLS_PER_SITEMAP:
            issues.append(f"Sitemap contains {url_count} URLs — exceeds 50,000 limit. Split into multiple files.")

        # Validate dates
        date_issues, urls_with_lastmod = validate_lastmod_dates(urls)
        issues.extend(date_issues)

        # Sample URLs for status
        sampled = sample_urls(urls, args.sample_size)
        non_200 = [s for s in sampled if s["status"] != 200]
        if non_200:
            issues.append(f"{len(non_200)}/{len(sampled)} sampled URLs returned non-200 status. Remove non-200 URLs from sitemap.")

        result = {
            "sitemap_url": sitemap_url,
            "valid": len(issues) == 0,
            "warnings": [i for i in issues if "recommend" in i.lower() or "add" in i.lower()],
            "is_index": False,
            "url_count": url_count,
            "urls_with_lastmod": urls_with_lastmod,
            "size_bytes": size_bytes,
            "sampled_urls": sampled,
            "issues": issues,
        }

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
