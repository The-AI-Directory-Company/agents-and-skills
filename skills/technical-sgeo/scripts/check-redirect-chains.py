#!/usr/bin/env python3
"""
check-redirect-chains.py — Follow redirect chains and report chain length, status codes, and issues.

Accepts a single URL (--url) or multiple URLs from stdin (one per line). For each
URL, follows all redirects up to 10 hops, recording each hop's status code and
destination. Flags chains >2 hops, redirect loops, and mixed protocol redirects.

Usage:
    python3 check-redirect-chains.py --url https://example.com/old-page
    echo "https://example.com/page1\nhttps://example.com/page2" | python3 check-redirect-chains.py
    python3 check-redirect-chains.py --url http://example.com --url https://www.example.com/old

AI Agent Usage:
    Agents should use WebFetch with redirect-following disabled to manually trace
    each hop in a redirect chain. For each URL:
    1. Fetch the URL, note the status code
    2. If 3xx, read the Location header and fetch that URL
    3. Repeat until a non-redirect status or 10 hops
    4. Flag chains >2 hops — update internal links to point to final destination
"""

import argparse
import json
import sys
import urllib.request
import urllib.error
import time
from urllib.parse import urlparse


MAX_HOPS = 10


class NoRedirectHandler(urllib.request.HTTPRedirectHandler):
    """Custom handler that prevents automatic redirect following."""
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def follow_chain(url, timeout=10):
    """
    Follow a redirect chain from the given URL.
    Returns (hops, final_url, final_status, issues).
    """
    opener = urllib.request.build_opener(NoRedirectHandler)
    hops = []
    visited = set()
    current_url = url
    issues = []

    for i in range(MAX_HOPS):
        if current_url in visited:
            issues.append("Redirect loop detected")
            break
        visited.add(current_url)

        try:
            req = urllib.request.Request(current_url)
            req.add_header("User-Agent", "check-redirect-chains/1.0")

            try:
                response = opener.open(req, timeout=timeout)
                status = response.getcode()
                hops.append({
                    "hop": i + 1,
                    "url": current_url,
                    "status": status,
                })
                # Non-redirect response — chain ends here
                final_url = current_url
                final_status = status
                break

            except urllib.error.HTTPError as e:
                if e.code in (301, 302, 303, 307, 308):
                    location = e.headers.get("Location", "")
                    redirect_type = {301: "permanent", 302: "temporary", 303: "see_other", 307: "temporary_strict", 308: "permanent_strict"}.get(e.code, "unknown")

                    if not location:
                        hops.append({
                            "hop": i + 1,
                            "url": current_url,
                            "status": e.code,
                            "error": "Redirect with no Location header",
                        })
                        issues.append(f"Hop {i + 1}: Redirect ({e.code}) with no Location header")
                        final_url = current_url
                        final_status = e.code
                        break

                    # Handle relative redirects
                    if location.startswith("/"):
                        parsed = urlparse(current_url)
                        location = f"{parsed.scheme}://{parsed.netloc}{location}"

                    # Check for protocol downgrade
                    if current_url.startswith("https://") and location.startswith("http://"):
                        issues.append(f"Hop {i + 1}: HTTPS to HTTP redirect (protocol downgrade)")

                    hops.append({
                        "hop": i + 1,
                        "url": current_url,
                        "status": e.code,
                        "redirect_type": redirect_type,
                        "location": location,
                    })

                    current_url = location
                else:
                    hops.append({
                        "hop": i + 1,
                        "url": current_url,
                        "status": e.code,
                    })
                    final_url = current_url
                    final_status = e.code
                    break

        except Exception as e:
            hops.append({
                "hop": i + 1,
                "url": current_url,
                "error": str(e),
            })
            issues.append(f"Hop {i + 1}: Connection error — {str(e)}")
            final_url = current_url
            final_status = None
            break
    else:
        issues.append(f"Redirect chain exceeds {MAX_HOPS} hops — likely a loop or misconfiguration")
        final_url = current_url
        final_status = None

    # Count actual redirects (hops with Location header)
    redirect_count = sum(1 for h in hops if "location" in h)

    if redirect_count > 2:
        issues.append(f"Chain has {redirect_count} redirects — exceeds recommended maximum of 2. Update internal links to point directly to {final_url}")

    # Check for 302 where 301 would be better
    for hop in hops:
        if hop.get("status") == 302 and hop.get("redirect_type") == "temporary":
            issues.append(f"Hop {hop['hop']}: Using 302 (temporary) redirect. If this is a permanent move, use 301 to pass link equity.")

    return {
        "original_url": url,
        "chain_length": redirect_count,
        "total_hops": len(hops),
        "hops": hops,
        "final_url": final_url,
        "final_status": final_status,
        "issues": issues,
        "status": "ok" if not issues else "has_issues",
    }


def main():
    parser = argparse.ArgumentParser(
        description="Follow redirect chains for URLs, reporting chain length, status codes, and issues.",
        epilog="Output: JSON with redirect chain details per URL. Accepts --url flags or URLs from stdin."
    )
    parser.add_argument("--url", action="append", help="URL(s) to check (can specify multiple times)")
    parser.add_argument("--delay", type=float, default=0.5,
                        help="Delay between URL checks in seconds (default: 0.5)")
    parser.add_argument("--tools", help="Path to tools.json from inventory-tools.py")
    args = parser.parse_args()

    urls = []

    # Collect URLs from --url flags
    if args.url:
        urls.extend(args.url)

    # Collect URLs from stdin if not a TTY
    if not sys.stdin.isatty():
        for line in sys.stdin:
            line = line.strip()
            if line and line.startswith("http"):
                urls.append(line)

    if not urls:
        parser.error("No URLs provided. Use --url or pipe URLs via stdin.")

    results = []
    for i, url in enumerate(urls):
        if i > 0:
            time.sleep(args.delay)
        result = follow_chain(url)
        results.append(result)

    # Summary
    chains_with_issues = [r for r in results if r["issues"]]
    long_chains = [r for r in results if r["chain_length"] > 2]

    output = {
        "total_urls_checked": len(results),
        "urls_with_issues": len(chains_with_issues),
        "long_chains": len(long_chains),
        "results": results,
    }

    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
