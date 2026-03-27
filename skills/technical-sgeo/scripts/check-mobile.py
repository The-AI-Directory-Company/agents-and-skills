#!/usr/bin/env python3
"""
check-mobile.py — Check mobile-friendliness of a page.

Fetches page HTML, checks viewport meta tag, scans for mobile-unfriendly CSS
patterns (fixed widths, small fonts), and reports potential issues. When
Playwright MCP is available, agents can extend this with visual rendering checks.

Usage:
    python3 check-mobile.py --url https://example.com
    python3 check-mobile.py --url https://example.com --tools tools.json

AI Agent Usage:
    Agents should use WebFetch to get the page HTML and check for:
    1. <meta name="viewport" content="width=device-width, initial-scale=1">
    2. Fixed-width containers in inline styles or <style> blocks
    3. Font sizes below 16px in CSS
    If Playwright MCP is available, render at 375px width to visually verify
    mobile layout, check for horizontal scrollbar, and measure tap targets.
"""

import argparse
import json
import sys
import urllib.request
import urllib.error
import re


def fetch_page(url, timeout=15):
    """Fetch page HTML with a mobile User-Agent. Returns (html, error)."""
    mobile_ua = "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1"
    try:
        req = urllib.request.Request(url)
        req.add_header("User-Agent", mobile_ua)
        response = urllib.request.urlopen(req, timeout=timeout)
        html = response.read().decode("utf-8", errors="replace")
        return html, None
    except urllib.error.HTTPError as e:
        return None, f"HTTP {e.code}"
    except Exception as e:
        return None, str(e)


def check_viewport_meta(html):
    """Check for viewport meta tag. Returns (found, content, issues)."""
    pattern = re.compile(
        r'<meta[^>]*name=["\']viewport["\'][^>]*content=["\']([^"\']*)["\']',
        re.IGNORECASE
    )
    match = pattern.search(html)

    if not match:
        # Try alternate attribute order
        pattern2 = re.compile(
            r'<meta[^>]*content=["\']([^"\']*)["\'][^>]*name=["\']viewport["\']',
            re.IGNORECASE
        )
        match = pattern2.search(html)

    if not match:
        return False, None, ["Missing viewport meta tag. Add: <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">"]

    content = match.group(1)
    issues = []

    if "width=device-width" not in content:
        issues.append("Viewport meta tag missing 'width=device-width'")

    if "initial-scale=1" not in content and "initial-scale=1.0" not in content:
        issues.append("Viewport meta tag missing 'initial-scale=1'")

    if "maximum-scale=1" in content or "user-scalable=no" in content:
        issues.append("Viewport disables user zooming (maximum-scale=1 or user-scalable=no) — this is an accessibility issue")

    return True, content, issues


def check_fixed_widths(html):
    """Scan CSS for fixed-width containers that may break mobile layout."""
    issues = []

    # Check inline styles and <style> blocks for fixed widths
    style_blocks = re.findall(r'<style[^>]*>(.*?)</style>', html, re.DOTALL | re.IGNORECASE)
    inline_styles = re.findall(r'style=["\']([^"\']*)["\']', html, re.IGNORECASE)

    all_css = "\n".join(style_blocks + inline_styles)

    # Find fixed widths > 500px (likely desktop-only layouts)
    fixed_width_pattern = re.compile(r'width\s*:\s*(\d+)px', re.IGNORECASE)
    for match in fixed_width_pattern.finditer(all_css):
        width = int(match.group(1))
        if width > 500:
            # Try to find the selector or element
            context_start = max(0, match.start() - 100)
            context = all_css[context_start:match.start()]
            selector_match = re.search(r'([.#\w][\w-]*)\s*\{[^}]*$', context)
            selector = selector_match.group(1) if selector_match else "unknown"
            issues.append(f"Fixed width {width}px found (selector: {selector}) — may cause horizontal scroll on mobile")

    # Check for table layout without responsive wrapper
    table_count = len(re.findall(r'<table', html, re.IGNORECASE))
    if table_count > 0:
        responsive_table = re.search(r'overflow-x\s*:\s*auto|overflow\s*:\s*auto|table-responsive', all_css, re.IGNORECASE)
        if not responsive_table:
            issues.append(f"Found {table_count} <table> element(s) without visible responsive overflow handling — may cause horizontal scroll")

    return issues


def check_font_sizes(html):
    """Check for font sizes below 16px that are hard to read on mobile."""
    issues = []

    style_blocks = re.findall(r'<style[^>]*>(.*?)</style>', html, re.DOTALL | re.IGNORECASE)
    all_css = "\n".join(style_blocks)

    font_size_pattern = re.compile(r'font-size\s*:\s*(\d+)px', re.IGNORECASE)
    small_fonts = []
    for match in font_size_pattern.finditer(all_css):
        size = int(match.group(1))
        if size < 14 and size > 0:
            small_fonts.append(size)

    if small_fonts:
        issues.append(f"Found font sizes below 14px in CSS: {sorted(set(small_fonts))}px — may be too small on mobile. Base font should be >= 16px.")

    return issues


def check_content_parity(html):
    """Check for mobile-hidden content patterns."""
    issues = []

    # Check for elements hidden on mobile via common CSS classes
    hidden_patterns = [
        (r'class=["\'][^"\']*hidden-mobile[^"\']*["\']', "hidden-mobile"),
        (r'class=["\'][^"\']*d-none d-md-block[^"\']*["\']', "d-none d-md-block (Bootstrap)"),
        (r'class=["\'][^"\']*hide-on-mobile[^"\']*["\']', "hide-on-mobile"),
        (r'class=["\'][^"\']*desktop-only[^"\']*["\']', "desktop-only"),
    ]

    for pattern, name in hidden_patterns:
        matches = re.findall(pattern, html, re.IGNORECASE)
        if matches:
            issues.append(f"Found {len(matches)} element(s) with '{name}' class — verify these don't hide critical content from mobile users and Googlebot (mobile-first indexing)")

    # Check for display:none in media queries
    style_blocks = re.findall(r'<style[^>]*>(.*?)</style>', html, re.DOTALL | re.IGNORECASE)
    all_css = "\n".join(style_blocks)

    # Simplified check: look for mobile media queries with display:none
    mobile_hide = re.findall(r'@media[^{]*max-width[^{]*\{[^}]*display\s*:\s*none', all_css, re.IGNORECASE)
    if mobile_hide:
        issues.append(f"Found {len(mobile_hide)} CSS rule(s) hiding content in mobile media queries — verify content parity")

    return issues


def check_touch_targets(html):
    """Basic check for potentially small touch targets."""
    issues = []

    # Check for very small links (common pattern: links with no padding or small text)
    # This is a heuristic — real analysis requires rendering
    small_link_patterns = re.findall(r'<a[^>]*style=["\'][^"\']*font-size\s*:\s*(\d+)px', html, re.IGNORECASE)
    small_links = [int(s) for s in small_link_patterns if int(s) < 12]
    if small_links:
        issues.append(f"Found links with very small font sizes ({min(small_links)}px) — touch targets should be at least 48x48px with 8px spacing")

    return issues


def main():
    parser = argparse.ArgumentParser(
        description="Check mobile-friendliness: viewport tag, fixed widths, font sizes, content parity, touch targets.",
        epilog="Output: JSON report with mobile issues and recommendations. For visual checks, use Playwright MCP."
    )
    parser.add_argument("--url", required=True, help="URL to check")
    parser.add_argument("--tools", help="Path to tools.json from inventory-tools.py")
    args = parser.parse_args()

    # Load tools inventory
    tools = {}
    if args.tools:
        try:
            with open(args.tools) as f:
                tools = json.load(f).get("tool_inventory", {})
        except Exception:
            pass

    # Fetch page
    html, error = fetch_page(args.url)
    if error:
        print(json.dumps({
            "url": args.url,
            "error": error,
            "recommendation": "Could not fetch page. Verify URL is accessible."
        }, indent=2))
        return

    # Run checks
    viewport_found, viewport_content, viewport_issues = check_viewport_meta(html)
    fixed_width_issues = check_fixed_widths(html)
    font_issues = check_font_sizes(html)
    parity_issues = check_content_parity(html)
    touch_issues = check_touch_targets(html)

    all_issues = viewport_issues + fixed_width_issues + font_issues + parity_issues + touch_issues

    # Determine Playwright availability
    playwright_available = tools.get("playwright_mcp") is True

    result = {
        "url": args.url,
        "viewport_meta": {
            "found": viewport_found,
            "content": viewport_content,
            "issues": viewport_issues,
        },
        "fixed_width_issues": fixed_width_issues,
        "font_size_issues": font_issues,
        "content_parity_issues": parity_issues,
        "touch_target_issues": touch_issues,
        "total_issues": len(all_issues),
        "all_issues": all_issues,
        "playwright_available": playwright_available,
        "note": "This script performs static HTML analysis. For visual rendering checks (layout at 375px, tap target measurement, horizontal scroll detection), use Playwright MCP or Chrome DevTools MCP." if not playwright_available else "Playwright MCP available — agent can extend with visual rendering checks.",
    }

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
