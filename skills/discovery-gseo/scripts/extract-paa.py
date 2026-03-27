#!/usr/bin/env python3
"""
extract-paa.py — Extract People Also Ask questions from Google SERPs.

Searches Google for each seed keyword, locates the PAA box, click-expands every
question to reveal answers and trigger new related questions. Captures 20-50+
questions per seed with answer snippets and source URLs.

Usage:
    python3 extract-paa.py --seeds "invoicing software,billing software"
    python3 extract-paa.py --seeds "invoicing software" --no-browser
    python3 extract-paa.py --seeds-file seeds.txt

AI Agent Usage (Playwright MCP — primary path):
    For each seed keyword:
    1. browser_navigate to https://www.google.com/search?q={seed}&gl=us&hl=en&pws=0
    2. Wait 2-3 seconds for full SERP load
    3. browser_snapshot — locate PAA box in the page content
    4. For each PAA question found:
       a. browser_click on the question to expand it
       b. Wait 1-2 seconds for answer + new questions to load
       c. browser_snapshot — capture: question text, answer snippet, source URL
       d. Note any newly appeared questions
    5. Repeat step 4 for newly revealed questions until no new ones appear or 50+ captured
    6. Wait 5-8 seconds (randomized) before searching next seed
    Anti-detection: 1-2s between PAA clicks, 5-8s between seeds, max 15 seeds per session.

AI Agent Usage (--no-browser fallback):
    Use WebSearch for each seed. Some search APIs return PAA data in results.
    Quality is significantly lower — typically 4-8 questions vs 20-50+ with browser.
"""

import argparse
import json
import sys
import random
import time


MAX_QUESTIONS_PER_SEED = 50
MAX_SEEDS_PER_SESSION = 15


def extract_with_browser(seeds):
    """
    Browser-based PAA extraction via Playwright MCP.

    The AI agent should execute the tool calls described in the module docstring.
    For each seed, the agent clicks through PAA questions, capturing the expanding
    tree of related questions.
    """
    all_questions = []
    seen_questions = set()

    for i, seed in enumerate(seeds):
        if i >= MAX_SEEDS_PER_SESSION:
            print(
                f"Warning: session limit ({MAX_SEEDS_PER_SESSION}) reached.",
                file=sys.stderr,
            )
            break

        seed = seed.strip()
        if not seed:
            continue

        # --- Agent: execute these Playwright MCP calls ---
        # 1. browser_navigate(url=f"https://www.google.com/search?q={seed}&gl=us&hl=en&pws=0")
        # 2. Wait 2-3 seconds for page load
        # 3. browser_snapshot() → find PAA section
        # 4. For each PAA question visible:
        #      browser_click(element="PAA question text", ref="...")
        #      Wait 1-2 seconds
        #      browser_snapshot() → extract:
        #        - question text
        #        - answer snippet (first paragraph of expanded answer)
        #        - source URL (link in the expanded answer)
        #        - newly revealed questions (appeared below the clicked question)
        # 5. Continue clicking new questions until MAX_QUESTIONS_PER_SEED or no new ones
        # 6. Wait random 5-8 seconds before next seed

        seed_questions = _placeholder_paa(seed)
        for q in seed_questions:
            if q["question"] not in seen_questions:
                seen_questions.add(q["question"])
                all_questions.append(q)

        delay = random.uniform(5.0, 8.0)
        time.sleep(delay)

    return all_questions


def extract_without_browser(seeds):
    """
    Fallback: extract PAA data from WebSearch results.

    AI Agent: Use WebSearch for each seed. Some APIs return PAA-like data.
    Also try WebSearch for "people also ask [seed]" to find cached PAA data.
    Expect 4-8 questions per seed instead of 20-50+.
    """
    all_questions = []
    seen_questions = set()

    for seed in seeds:
        seed = seed.strip()
        if not seed:
            continue

        # Agent: WebSearch(query=seed) → parse any PAA data from results
        # Agent: WebSearch(query=f"people also ask {seed}") → additional questions
        placeholder = {
            "question": f"How do I {seed}?",
            "answer_snippet": "Placeholder — use browser mode for real data.",
            "source_url": "",
            "source_seed": seed,
        }
        if placeholder["question"] not in seen_questions:
            seen_questions.add(placeholder["question"])
            all_questions.append(placeholder)

    return all_questions


def _placeholder_paa(seed):
    """
    Placeholder for browser-extracted PAA questions.
    In real execution, the agent collects questions from browser_snapshot parsing.
    """
    return [
        {
            "question": f"How do I {seed}?",
            "answer_snippet": "Placeholder — agent fills with real data from SERP.",
            "source_url": "",
            "source_seed": seed,
        }
    ]


def main():
    parser = argparse.ArgumentParser(
        description="Extract People Also Ask questions from Google SERPs."
    )
    parser.add_argument(
        "--seeds",
        type=str,
        help="Comma-separated seed keywords",
    )
    parser.add_argument(
        "--seeds-file",
        type=str,
        help="Path to file with seed keywords, one per line",
    )
    parser.add_argument(
        "--no-browser",
        action="store_true",
        help="Use WebSearch fallback instead of Playwright MCP",
    )
    parser.add_argument(
        "--tools",
        type=str,
        help="Path to tools.json inventory file",
    )

    args = parser.parse_args()

    seeds = []
    if args.seeds:
        seeds = [s.strip() for s in args.seeds.split(",") if s.strip()]
    elif args.seeds_file:
        try:
            with open(args.seeds_file, "r") as f:
                seeds = [line.strip() for line in f if line.strip()]
        except FileNotFoundError:
            print(json.dumps({"error": f"Seeds file not found: {args.seeds_file}"}))
            sys.exit(1)

    if not seeds:
        print(json.dumps({"error": "No seeds provided. Use --seeds or --seeds-file."}))
        sys.exit(1)

    if args.no_browser:
        questions = extract_without_browser(seeds)
        method = "fallback"
    else:
        questions = extract_with_browser(seeds)
        method = "playwright"

    result = {
        "seeds_processed": min(len(seeds), MAX_SEEDS_PER_SESSION),
        "total_questions": len(questions),
        "questions": questions,
        "method": method,
    }

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
