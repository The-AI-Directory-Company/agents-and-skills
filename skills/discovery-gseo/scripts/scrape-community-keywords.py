#!/usr/bin/env python3
"""
scrape-community-keywords.py — Extract keyword candidates from community discussions.

Searches Reddit, Hacker News, and other platforms for a topic, extracts post titles,
popular comment phrases, and pain point language. Maps community language patterns
to keyword candidates.

Usage:
    python3 scrape-community-keywords.py --topic "invoicing software" --platforms reddit,hn
    python3 scrape-community-keywords.py --topic "form builder" --no-browser
    python3 scrape-community-keywords.py --topic "invoicing software" --platforms reddit,hn,quora

AI Agent Usage (Playwright MCP — primary path):
    For Reddit:
    1. browser_navigate to https://www.reddit.com/search/?q={topic}&sort=relevance&t=year
    2. Wait 3 seconds for dynamic content to load
    3. browser_snapshot — extract post titles and upvote counts from top 50 results
    4. For top 10-20 posts: browser_click to open, browser_snapshot to extract
       top comments (focus on pain points, questions, comparison language)
    5. Wait 3-5 seconds between page loads

    For Hacker News:
    1. browser_navigate to https://hn.algolia.com/?q={topic}&type=story&sort=byPopularity&dateRange=pastYear
    2. browser_snapshot — extract story titles and point counts
    3. For top 10 stories: click through, extract top comments

    For Quora:
    1. browser_navigate to https://www.quora.com/search?q={topic}
    2. browser_snapshot — extract question titles

    Anti-detection: 3-5s between page loads, respectful scraping.

AI Agent Usage (--no-browser fallback):
    Use WebSearch with site: operator:
    - WebSearch("site:reddit.com {topic}")
    - WebSearch("site:news.ycombinator.com {topic}")
    - WebSearch("site:quora.com {topic}")
    Parse titles and snippets. No comment extraction possible.
"""

import argparse
import json
import sys
import re
import random
import time
from collections import Counter


SUPPORTED_PLATFORMS = ["reddit", "hn", "quora", "producthunt"]

# Common question patterns found in community discussions
QUESTION_PATTERNS = [
    r"(?:how|How)\s+(?:do|can|should|would)\s+(?:I|you|we)\s+(.+?)[\?\.]",
    r"(?:what|What)\s+(?:is|are)\s+(?:the\s+)?(?:best|top|recommended)\s+(.+?)[\?\.]",
    r"(?:is|Is)\s+there\s+(?:a|an)\s+(.+?)[\?\.]",
    r"(?:looking|Looking)\s+for\s+(?:a|an)\s+(.+?)[\?\.]",
    r"(?:need|Need)\s+(?:a|an|help\s+with)\s+(.+?)[\?\.]",
]


def extract_keyword_phrases(text):
    """Extract potential keyword phrases from community text."""
    phrases = []
    # Extract 2-4 word noun phrases (simplified)
    words = re.findall(r"\b[a-z][a-z\-]+\b", text.lower())
    for i in range(len(words)):
        for length in range(2, 5):
            if i + length <= len(words):
                phrase = " ".join(words[i : i + length])
                if len(phrase) > 5:  # Skip very short phrases
                    phrases.append(phrase)
    return phrases


def scrape_with_browser(topic, platforms):
    """
    Browser-based community scraping via Playwright MCP.
    Agent executes tool calls per module docstring.
    """
    all_keywords = []
    question_patterns = []

    for platform in platforms:
        if platform not in SUPPORTED_PLATFORMS:
            print(f"Warning: unsupported platform '{platform}', skipping.", file=sys.stderr)
            continue

        # --- Agent: platform-specific Playwright MCP calls ---
        # Reddit:
        #   browser_navigate(url=f"https://www.reddit.com/search/?q={topic}&sort=relevance&t=year")
        #   Wait 3s, browser_snapshot() → extract post titles
        #   Click into top posts, browser_snapshot() → extract comments
        # HN:
        #   browser_navigate(url=f"https://hn.algolia.com/?q={topic}&type=story&sort=byPopularity")
        #   browser_snapshot() → extract story titles and comments
        # Quora:
        #   browser_navigate(url=f"https://www.quora.com/search?q={topic}")
        #   browser_snapshot() → extract question titles

        # Placeholder — agent fills with real community data
        placeholder = {
            "phrase": topic,
            "frequency": 1,
            "source": platform,
            "context": f"Placeholder — agent extracts from {platform} via browser",
            "suggested_keyword": topic,
        }
        all_keywords.append(placeholder)

        delay = random.uniform(3.0, 5.0)
        time.sleep(delay)

    return all_keywords, question_patterns


def scrape_without_browser(topic, platforms):
    """
    Fallback: community keyword extraction via WebSearch site: queries.

    Agent: WebSearch("site:reddit.com {topic}"), parse titles and snippets.
    Agent: WebSearch("site:news.ycombinator.com {topic}"), parse titles.
    Agent: WebSearch("site:quora.com {topic}"), parse question titles.
    """
    all_keywords = []
    question_patterns = []

    for platform in platforms:
        site_map = {
            "reddit": "reddit.com",
            "hn": "news.ycombinator.com",
            "quora": "quora.com",
            "producthunt": "producthunt.com",
        }
        site = site_map.get(platform)
        if not site:
            continue

        # Agent: WebSearch(query=f"site:{site} {topic}")
        # Parse result titles and snippets for keyword phrases
        placeholder = {
            "phrase": topic,
            "frequency": 1,
            "source": platform,
            "context": f"Placeholder — agent extracts from WebSearch site:{site}",
            "suggested_keyword": topic,
        }
        all_keywords.append(placeholder)

    return all_keywords, question_patterns


def main():
    parser = argparse.ArgumentParser(
        description="Extract keyword candidates from community discussions."
    )
    parser.add_argument(
        "--topic", type=str, required=True, help="Topic to search for in communities"
    )
    parser.add_argument(
        "--platforms",
        type=str,
        default="reddit,hn",
        help="Comma-separated platforms to scrape (default: reddit,hn)",
    )
    parser.add_argument(
        "--no-browser",
        action="store_true",
        help="Use WebSearch fallback instead of Playwright MCP",
    )
    parser.add_argument("--tools", type=str, help="Path to tools.json inventory file")

    args = parser.parse_args()

    platforms = [p.strip() for p in args.platforms.split(",") if p.strip()]

    if args.no_browser:
        keywords, patterns = scrape_without_browser(args.topic, platforms)
        method = "fallback"
    else:
        keywords, patterns = scrape_with_browser(args.topic, platforms)
        method = "playwright"

    result = {
        "topic": args.topic,
        "platforms_scraped": platforms,
        "method": method,
        "keywords": keywords,
        "total_extracted": len(keywords),
        "question_patterns": patterns,
    }

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
