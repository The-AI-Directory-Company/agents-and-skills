#!/usr/bin/env python3
"""
inventory-tools.py — Probe which tools, APIs, and MCPs are available.

Outputs a JSON inventory that other scripts consume to decide which code paths
to take. Every script in this skill accepts a --tools flag pointing to the
JSON output of this script.

Usage:
    python3 inventory-tools.py
    python3 inventory-tools.py --output tools.json
    python3 inventory-tools.py --dataforseo-user USER --dataforseo-pass PASS
    python3 inventory-tools.py --ahrefs-key KEY
    python3 inventory-tools.py --semrush-key KEY

AI Agent Usage:
    When an agent reads this script, it should understand the tool discovery
    pattern: probe each tool, record availability, and pass the inventory to
    subsequent scripts. Agents can replicate this logic using their native
    capabilities (WebFetch, WebSearch, etc.) without running this script directly.
"""

import argparse
import json
import sys
import urllib.request
import urllib.error


def check_url(url, timeout=10):
    """Try fetching a URL. Return True if we get a response (any status)."""
    try:
        req = urllib.request.Request(url, method="HEAD")
        req.add_header("User-Agent", "inventory-tools/1.0")
        urllib.request.urlopen(req, timeout=timeout)
        return True
    except urllib.error.HTTPError:
        # Got a response (even if 4xx/5xx), server is reachable
        return True
    except Exception:
        return False


def check_webfetch():
    """Check if we can fetch a public URL (proxy for WebFetch availability)."""
    return check_url("https://example.com")


def check_websearch():
    """
    WebSearch is an agent-provided tool — cannot be probed from a script.
    Mark as 'unknown' unless the agent confirms availability.
    """
    return "unknown"


def check_psi_api():
    """Check Google PageSpeed Insights API availability (free, no key needed)."""
    url = "https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url=https://example.com&strategy=mobile&category=performance"
    try:
        req = urllib.request.Request(url)
        req.add_header("User-Agent", "inventory-tools/1.0")
        response = urllib.request.urlopen(req, timeout=30)
        data = response.read()
        return len(data) > 0
    except Exception:
        return False


def check_dataforseo(user, password):
    """Check DataForSEO API access with provided credentials."""
    if not user or not password:
        return False
    try:
        import base64
        url = "https://api.dataforseo.com/v3/serp/google/organic/live"
        credentials = base64.b64encode(f"{user}:{password}".encode()).decode()
        req = urllib.request.Request(url)
        req.add_header("Authorization", f"Basic {credentials}")
        req.add_header("Content-Type", "application/json")
        # Send a minimal test request
        req.data = json.dumps([{"keyword": "test", "location_code": 2840, "language_code": "en"}]).encode()
        response = urllib.request.urlopen(req, timeout=15)
        result = json.loads(response.read())
        return result.get("status_code") == 20000
    except Exception:
        return False


def check_ahrefs(api_key):
    """Check Ahrefs API access with provided key."""
    if not api_key:
        return False
    try:
        url = f"https://apiv2.ahrefs.com?token={api_key}&from=subscription_info&output=json"
        req = urllib.request.Request(url)
        response = urllib.request.urlopen(req, timeout=15)
        data = json.loads(response.read())
        return "subscription" in data or "rows" in data
    except Exception:
        return False


def check_semrush(api_key):
    """Check Semrush API access with provided key."""
    if not api_key:
        return False
    try:
        url = f"https://api.semrush.com/?type=domain_ranks&key={api_key}&export_columns=Dn&domain=example.com"
        req = urllib.request.Request(url)
        response = urllib.request.urlopen(req, timeout=15)
        data = response.read().decode()
        # Semrush returns CSV. An error response contains "ERROR"
        return "ERROR" not in data
    except Exception:
        return False


def check_playwright_mcp():
    """
    Playwright MCP is an agent-provided tool — cannot be probed from a script.
    Mark as 'unknown' unless the agent confirms availability.
    """
    return "unknown"


def check_chrome_devtools_mcp():
    """
    Chrome DevTools MCP is an agent-provided tool — cannot be probed from a script.
    Mark as 'unknown' unless the agent confirms availability.
    """
    return "unknown"


def main():
    parser = argparse.ArgumentParser(
        description="Probe which tools, APIs, and MCPs are available for technical SGEO checks.",
        epilog="Output: JSON inventory of tool availability. Other scripts consume this to decide code paths."
    )
    parser.add_argument("--output", "-o", help="Write inventory to file instead of stdout")
    parser.add_argument("--dataforseo-user", help="DataForSEO API username")
    parser.add_argument("--dataforseo-pass", help="DataForSEO API password")
    parser.add_argument("--ahrefs-key", help="Ahrefs API key")
    parser.add_argument("--semrush-key", help="Semrush API key")
    parser.add_argument("--tools", help="Path to existing tools.json (ignored — this script creates the inventory)")
    args = parser.parse_args()

    inventory = {
        "webfetch": check_webfetch(),
        "websearch": check_websearch(),
        "psi_api": check_psi_api(),
        "dataforseo": check_dataforseo(args.dataforseo_user, args.dataforseo_pass),
        "ahrefs": check_ahrefs(args.ahrefs_key),
        "semrush": check_semrush(args.semrush_key),
        "playwright_mcp": check_playwright_mcp(),
        "chrome_devtools_mcp": check_chrome_devtools_mcp(),
    }

    # Add metadata
    result = {
        "tool_inventory": inventory,
        "notes": {
            "unknown": "Tools marked 'unknown' are agent-provided and cannot be probed from a script. The agent should update these values based on its own capabilities.",
            "free_baseline": "webfetch and psi_api are sufficient for all checks in this skill. Paid tools enhance output but are never required.",
        }
    }

    output = json.dumps(result, indent=2)

    if args.output:
        with open(args.output, "w") as f:
            f.write(output + "\n")
        print(json.dumps({"status": "ok", "output_file": args.output}))
    else:
        print(output)


if __name__ == "__main__":
    main()
