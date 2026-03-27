#!/usr/bin/env python3
"""
check-ai-crawler-access.py — Test whether AI crawlers can access a page.

Fetches a URL with different User-Agent strings (browser baseline, GPTBot,
ClaudeBot, PerplexityBot) and compares responses. A significantly different
response (403, 503, empty body, captcha page) indicates CDN/WAF blocking.

Usage:
    python3 check-ai-crawler-access.py --url https://example.com
    python3 check-ai-crawler-access.py --url https://example.com/blog/article

AI Agent Usage:
    Agents should use WebFetch with custom User-Agent headers to replicate this
    check. Fetch the same URL with a browser UA and each AI bot UA. Compare
    status codes and response sizes. If an AI bot gets a different status code
    or a much smaller response, it is likely being blocked by CDN/WAF settings.
    See references/ai-crawler-access.md for the full user-agent table.
"""

import argparse
import json
import sys
import urllib.request
import urllib.error
import time


# User-agent strings for testing
BROWSER_UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"

AI_BOTS = {
    "GPTBot": "Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko; compatible; GPTBot/1.0; +https://openai.com/gptbot)",
    "ClaudeBot": "ClaudeBot/1.0 (Anthropic; +https://www.anthropic.com/research)",
    "PerplexityBot": "Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko; compatible; PerplexityBot/1.0; +https://perplexity.ai/bot)",
    "ChatGPT-User": "Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko; compatible; ChatGPT-User/1.0; +https://openai.com/bot)",
}

# Patterns that indicate a challenge/captcha page instead of real content
CHALLENGE_PATTERNS = [
    "cf-challenge",           # Cloudflare challenge
    "cf-chl-bypass",          # Cloudflare challenge
    "challenge-platform",     # Generic challenge
    "captcha",                # CAPTCHA
    "please verify",          # Verification page
    "access denied",          # Access denied page
    "just a moment",          # Cloudflare waiting page
    "checking your browser",  # Bot detection page
    "ray id",                 # Cloudflare block page
]


def fetch_with_ua(url, user_agent, timeout=15):
    """Fetch a URL with a specific User-Agent. Returns (status, body_size, has_content, challenge_detected, error)."""
    try:
        req = urllib.request.Request(url)
        req.add_header("User-Agent", user_agent)
        req.add_header("Accept", "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8")
        req.add_header("Accept-Language", "en-US,en;q=0.9")

        response = urllib.request.urlopen(req, timeout=timeout)
        body = response.read()
        body_text = body.decode("utf-8", errors="replace").lower()

        status = response.getcode()
        body_size = len(body)
        has_content = body_size > 500  # Minimal content threshold

        # Check for challenge patterns
        challenge_detected = any(pattern in body_text for pattern in CHALLENGE_PATTERNS)

        return status, body_size, has_content, challenge_detected, None

    except urllib.error.HTTPError as e:
        body = e.read()
        body_text = body.decode("utf-8", errors="replace").lower() if body else ""
        challenge_detected = any(pattern in body_text for pattern in CHALLENGE_PATTERNS)
        return e.code, len(body) if body else 0, False, challenge_detected, None

    except Exception as e:
        return None, 0, False, False, str(e)


def compare_responses(baseline, bot_result):
    """Compare a bot response against the browser baseline."""
    issues = []
    likely_blocked = False

    if bot_result["status"] != baseline["status"]:
        issues.append(f"Status code differs: browser={baseline['status']}, bot={bot_result['status']}")
        if bot_result["status"] in (403, 503, 429):
            likely_blocked = True

    if baseline["body_size"] > 0 and bot_result["body_size"] > 0:
        size_ratio = bot_result["body_size"] / baseline["body_size"]
        if size_ratio < 0.3:
            issues.append(f"Response size is {size_ratio:.0%} of browser response — likely serving a different page")
            likely_blocked = True

    if bot_result["challenge_detected"]:
        issues.append("Challenge/captcha page detected in response")
        likely_blocked = True

    if not bot_result["has_content"] and baseline["has_content"]:
        issues.append("Bot received empty or minimal response while browser got content")
        likely_blocked = True

    return {
        "content_match": len(issues) == 0,
        "likely_blocked": likely_blocked,
        "issues": issues,
    }


def main():
    parser = argparse.ArgumentParser(
        description="Test whether AI crawlers can access a page by comparing responses across User-Agent strings.",
        epilog="Output: JSON report with per-bot access status, blocking detection, and CDN recommendations."
    )
    parser.add_argument("--url", required=True, help="URL to test")
    parser.add_argument("--delay", type=float, default=1.0,
                        help="Delay between requests in seconds (default: 1.0)")
    parser.add_argument("--tools", help="Path to tools.json from inventory-tools.py")
    args = parser.parse_args()

    # Fetch baseline with browser UA
    status, body_size, has_content, challenge, error = fetch_with_ua(args.url, BROWSER_UA)

    baseline = {
        "user_agent": "Chrome browser",
        "status": status,
        "body_size": body_size,
        "has_content": has_content,
        "challenge_detected": challenge,
        "error": error,
    }

    # Fetch with each AI bot UA
    bots = {}
    blocked_bots = []

    for bot_name, bot_ua in AI_BOTS.items():
        time.sleep(args.delay)  # Rate limiting

        status, body_size, has_content, challenge, error = fetch_with_ua(args.url, bot_ua)

        bot_result = {
            "status": status,
            "body_size": body_size,
            "has_content": has_content,
            "challenge_detected": challenge,
            "error": error,
        }

        comparison = compare_responses(baseline, bot_result)
        bot_result.update(comparison)

        bots[bot_name] = bot_result

        if comparison["likely_blocked"]:
            blocked_bots.append(bot_name)

    # Build recommendation
    if blocked_bots:
        recommendation = (
            f"{', '.join(blocked_bots)} {'is' if len(blocked_bots) == 1 else 'are'} likely blocked. "
            "Check CDN bot management settings: "
            "Cloudflare (Security > Bots > Bot Fight Mode), "
            "AWS WAF (Bot Control rule groups), "
            "or your server's bot detection configuration. "
            "See references/ai-crawler-access.md for provider-specific instructions."
        )
    elif baseline.get("error"):
        recommendation = f"Could not establish browser baseline: {baseline['error']}. Verify URL is accessible."
    else:
        recommendation = "All tested AI bots can access this page. No CDN/WAF blocking detected."

    result = {
        "url": args.url,
        "baseline": baseline,
        "bots": bots,
        "blocked_bots": blocked_bots,
        "blocked_count": len(blocked_bots),
        "recommendation": recommendation,
    }

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
