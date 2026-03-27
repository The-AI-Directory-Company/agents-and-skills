#!/usr/bin/env python3
"""
check-robots-txt.py — Fetch and analyze robots.txt for search engine and AI bot rules.

Parses all User-agent/Allow/Disallow directives. Reports per-bot access status,
blocked paths, sitemap declarations, and missing bot entries. Flags configurations
that harm AI visibility.

Usage:
    python3 check-robots-txt.py --domain example.com
    python3 check-robots-txt.py --domain example.com --tools tools.json

AI Agent Usage:
    Agents can replicate this by using WebFetch to retrieve {domain}/robots.txt,
    then parsing the directives. Key checks: are GPTBot, ClaudeBot, PerplexityBot
    explicitly allowed? Are there wildcard Disallow rules that block AI bots?
"""

import argparse
import json
import sys
import urllib.request
import urllib.error
import re


# Bots to check — search engines and AI crawlers
SEARCH_BOTS = ["Googlebot", "Bingbot"]
AI_BOTS = ["GPTBot", "ChatGPT-User", "OAI-SearchBot", "ClaudeBot", "PerplexityBot", "Google-Extended"]
ALL_BOTS = SEARCH_BOTS + AI_BOTS


def fetch_robots_txt(domain):
    """Fetch robots.txt from the domain. Returns (content, error)."""
    url = f"https://{domain}/robots.txt"
    try:
        req = urllib.request.Request(url)
        req.add_header("User-Agent", "check-robots-txt/1.0")
        response = urllib.request.urlopen(req, timeout=15)
        content = response.read().decode("utf-8", errors="replace")
        return content, None
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return None, "robots.txt not found (404). All bots are allowed by default."
        return None, f"HTTP error {e.code} fetching robots.txt"
    except Exception as e:
        return None, f"Error fetching robots.txt: {str(e)}"


def parse_robots_txt(content):
    """
    Parse robots.txt into a dict of user-agent -> list of (directive, path).
    Handles multi-bot blocks and wildcard user-agents.
    """
    rules = {}
    sitemaps = []
    current_agents = []

    for line in content.split("\n"):
        line = line.strip()
        # Remove comments
        if "#" in line:
            line = line[:line.index("#")].strip()
        if not line:
            continue

        # Sitemap directive (not agent-specific)
        if line.lower().startswith("sitemap:"):
            sitemaps.append(line.split(":", 1)[1].strip())
            continue

        # User-agent directive
        if line.lower().startswith("user-agent:"):
            agent = line.split(":", 1)[1].strip()
            current_agents.append(agent)
            if agent not in rules:
                rules[agent] = []
            continue

        # Allow/Disallow directives
        for directive in ["allow", "disallow", "crawl-delay"]:
            if line.lower().startswith(directive + ":"):
                path = line.split(":", 1)[1].strip()
                for agent in current_agents:
                    rules[agent].append((directive.lower(), path))
                break
        else:
            # Non-directive line resets the current agent block
            if not line.lower().startswith(("user-agent:", "allow:", "disallow:", "crawl-delay:", "sitemap:")):
                current_agents = []

    return rules, sitemaps


def evaluate_bot_access(bot_name, rules):
    """
    Determine a bot's access status based on robots.txt rules.
    Returns a dict with status, allowed_paths, blocked_paths, and recommendation.
    """
    # Check for specific rules for this bot
    bot_rules = rules.get(bot_name, [])
    wildcard_rules = rules.get("*", [])

    # Determine which rule set applies
    if bot_rules:
        active_rules = bot_rules
        rule_source = "specific"
    elif wildcard_rules:
        active_rules = wildcard_rules
        rule_source = "wildcard"
    else:
        return {
            "status": "allowed",
            "rule_source": "none",
            "blocked_paths": [],
            "allowed_paths": ["/"],
            "recommendation": None
        }

    allowed = []
    blocked = []

    for directive, path in active_rules:
        if directive == "allow" and path:
            allowed.append(path)
        elif directive == "disallow" and path:
            blocked.append(path)
        elif directive == "disallow" and not path:
            # Empty Disallow means allow all
            allowed.append("/")

    # Determine overall status
    if "/" in blocked and "/" not in allowed:
        status = "fully_blocked"
    elif blocked:
        status = "partially_blocked"
    else:
        status = "allowed"

    # Generate recommendation for AI bots
    recommendation = None
    if bot_name in AI_BOTS:
        if status == "fully_blocked":
            recommendation = f"Remove 'Disallow: /' for {bot_name} to enable AI visibility."
        elif status == "allowed" and rule_source == "wildcard":
            recommendation = f"Add explicit 'User-agent: {bot_name}\\nAllow: /' for clear intent documentation."
        elif rule_source == "none":
            recommendation = f"{bot_name} has no rules — allowed by default. Consider adding explicit Allow for documentation."

    return {
        "status": status,
        "rule_source": rule_source,
        "blocked_paths": blocked,
        "allowed_paths": allowed if allowed else ["/"] if not blocked else [],
        "recommendation": recommendation
    }


def main():
    parser = argparse.ArgumentParser(
        description="Fetch and analyze robots.txt for search engine and AI bot access rules.",
        epilog="Output: JSON report with per-bot access status, blocked paths, sitemaps, and recommendations."
    )
    parser.add_argument("--domain", required=True, help="Domain to check (e.g., example.com)")
    parser.add_argument("--tools", help="Path to tools.json from inventory-tools.py (unused — this script uses direct HTTP)")
    args = parser.parse_args()

    # Normalize domain
    domain = args.domain.replace("https://", "").replace("http://", "").rstrip("/")

    # Fetch robots.txt
    content, error = fetch_robots_txt(domain)

    if error and content is None:
        result = {
            "domain": domain,
            "robots_txt_url": f"https://{domain}/robots.txt",
            "status": "not_found" if "404" in error else "error",
            "error": error,
            "bots": {},
            "sitemaps": [],
            "recommendation": "Create a robots.txt file with explicit rules for search engines and AI crawlers."
        }
        print(json.dumps(result, indent=2))
        return

    # Parse robots.txt
    rules, sitemaps = parse_robots_txt(content)

    # Evaluate each bot
    bots = {}
    for bot in ALL_BOTS:
        bots[bot] = evaluate_bot_access(bot, rules)

    # Count AI bots that are blocked
    ai_blocked = [bot for bot in AI_BOTS if bots[bot]["status"] == "fully_blocked"]
    ai_not_mentioned = [bot for bot in AI_BOTS if bots[bot]["rule_source"] == "none"]

    # Overall assessment
    if ai_blocked:
        overall = f"{len(ai_blocked)} AI bot(s) fully blocked: {', '.join(ai_blocked)}. This prevents AI visibility from those platforms."
    elif ai_not_mentioned:
        overall = f"All AI bots allowed (by default or wildcard). {len(ai_not_mentioned)} bot(s) not explicitly mentioned — consider adding explicit Allow rules."
    else:
        overall = "All AI bots explicitly allowed. robots.txt configuration is optimal for AI visibility."

    result = {
        "domain": domain,
        "robots_txt_url": f"https://{domain}/robots.txt",
        "status": "ok",
        "bots": bots,
        "sitemaps": sitemaps,
        "ai_blocked_count": len(ai_blocked),
        "ai_blocked_bots": ai_blocked,
        "overall_assessment": overall,
        "raw_content_length": len(content),
    }

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
