#!/usr/bin/env python3
"""Check the direct-answer quality of a page's opening content.

Extracts the first 200 words after the H1, analyzes for direct-answer
patterns vs meandering intros, checks for anaphoric references, and
scores on the 0-8 GEO per-section rubric from references/geo-formatting.md.

Scoring criteria (0-2 each, total 0-8):
  - Direct answer present
  - Self-contained
  - Specific data
  - Source attribution

Usage:
    python check-direct-answer.py --url https://example.com/page
    python check-direct-answer.py --url https://example.com/page --tools tools.json

Output: JSON with first 200 words, score breakdown, issues, and patterns found.
"""

import argparse
import json
import re
import sys
from html.parser import HTMLParser
from typing import Optional


# ---------------------------------------------------------------------------
# Content extractor
# ---------------------------------------------------------------------------

class ContentExtractor(HTMLParser):
    """Extract text content from the main/article area after the first H1."""

    SKIP_TAGS = {"nav", "header", "footer", "aside", "script", "style", "noscript"}

    def __init__(self):
        super().__init__()
        self._found_h1 = False
        self._after_h1 = False
        self._skip_depth = 0
        self._text_parts: list[str] = []
        self._in_main = False
        self._main_depth = 0

    def handle_starttag(self, tag: str, attrs):
        if tag in ("main", "article"):
            self._in_main = True
            self._main_depth += 1
        if tag in self.SKIP_TAGS:
            self._skip_depth += 1
        if tag == "h1" and not self._found_h1:
            self._found_h1 = True
        elif self._found_h1 and not self._after_h1 and tag != "h1":
            self._after_h1 = True

    def handle_endtag(self, tag: str):
        if tag in ("main", "article"):
            self._main_depth -= 1
            if self._main_depth <= 0:
                self._in_main = False
        if tag in self.SKIP_TAGS and self._skip_depth > 0:
            self._skip_depth -= 1

    def handle_data(self, data: str):
        if self._after_h1 and self._skip_depth == 0:
            self._text_parts.append(data)

    def get_text(self) -> str:
        raw = " ".join(self._text_parts)
        return re.sub(r"\s+", " ", raw).strip()


# ---------------------------------------------------------------------------
# Analysis patterns
# ---------------------------------------------------------------------------

MEANDERING_PATTERNS = [
    (r"\bIn today'?s\b", "In today's..."),
    (r"\bAs we all know\b", "As we all know..."),
    (r"\bWhen it comes to\b", "When it comes to..."),
    (r"\bIt'?s no secret that\b", "It's no secret that..."),
    (r"\bIn this (comprehensive|complete|ultimate) guide\b", "In this comprehensive guide..."),
    (r"\bBefore we dive in\b", "Before we dive in..."),
    (r"\bLet'?s take a step back\b", "Let's take a step back..."),
    (r"\bThe world of .+ has changed\b", "The world of X has changed..."),
    (r"\bWelcome to\b", "Welcome to..."),
    (r"\bWe'?re (proud|excited|thrilled) to\b", "We're proud/excited to..."),
]

ANAPHORIC_PATTERNS = [
    (r"\bAs mentioned above\b", "As mentioned above"),
    (r"\bAs we discussed\b", "As we discussed"),
    (r"\bThis approach\b", "This approach"),
    (r"\bThe above\b", "The above"),
    (r"\bSee (the )?previous section\b", "See previous section"),
    (r"\bUsing the same (method|approach|technique)\b", "Using the same method"),
    (r"\bBuilding on this\b", "Building on this"),
    (r"^It\b", "Starts with 'It' (potentially anaphoric)"),
]

# Patterns indicating specific data
DATA_PATTERNS = [
    r"\d+%",                          # Percentages
    r"\$[\d,.]+",                     # Dollar amounts
    r"\d{4}",                         # Years
    r"\d+\.\d+",                      # Decimal numbers
    r"\d+,\d{3}",                     # Thousands
    r"\d+ (seconds?|minutes?|hours?|days?|weeks?|months?|years?)",  # Durations
    r"\d+x\b",                        # Multipliers
]

# Patterns indicating source attribution
SOURCE_PATTERNS = [
    r"according to",
    r"(a |the )?\d{4} .+ (study|survey|report|analysis|research)",
    r"(Ahrefs|Semrush|Moz|HubSpot|Gartner|Forrester|McKinsey|Deloitte|Google|Bing)",
    r"(study|survey|report) (of|by|from) \d+",
    r"\b(published|reported) (in|by)\b",
]


def get_first_n_words(text: str, n: int = 200) -> str:
    words = text.split()
    return " ".join(words[:n])


def find_patterns(text: str, patterns: list[tuple[str, str]]) -> list[str]:
    found = []
    for regex, label in patterns:
        if re.search(regex, text, re.IGNORECASE):
            found.append(label)
    return found


def count_matches(text: str, patterns: list[str]) -> int:
    count = 0
    for p in patterns:
        count += len(re.findall(p, text, re.IGNORECASE))
    return count


# ---------------------------------------------------------------------------
# Scoring (0-8 rubric)
# ---------------------------------------------------------------------------

def score_section(text: str) -> dict:
    """Score the first 200 words on the 0-8 GEO per-section rubric."""
    first_200 = get_first_n_words(text, 200)
    words = first_200.split()

    meandering = find_patterns(first_200, MEANDERING_PATTERNS)
    anaphoric = find_patterns(first_200, ANAPHORIC_PATTERNS)
    data_count = count_matches(first_200, DATA_PATTERNS)
    source_count = count_matches(first_200, SOURCE_PATTERNS)

    # --- Direct answer present (0-2) ---
    if meandering:
        direct_answer = 0
    elif len(words) < 20:
        direct_answer = 0  # Too short to evaluate
    else:
        # Heuristic: if no meandering patterns and text starts with a
        # substantive statement (not a question), likely direct.
        first_sentence = first_200.split(".")[0] if "." in first_200 else first_200
        if len(first_sentence.split()) >= 8:
            direct_answer = 2
        else:
            direct_answer = 1

    # --- Self-contained (0-2) ---
    if len(anaphoric) >= 2:
        self_contained = 0
    elif len(anaphoric) == 1:
        self_contained = 1
    else:
        self_contained = 2

    # --- Specific data (0-2) ---
    if data_count >= 3:
        specific_data = 2
    elif data_count >= 1:
        specific_data = 1
    else:
        specific_data = 0

    # --- Source attribution (0-2) ---
    if source_count >= 2:
        source_attribution = 2
    elif source_count >= 1:
        source_attribution = 1
    else:
        source_attribution = 0

    total = direct_answer + self_contained + specific_data + source_attribution

    issues = []
    if direct_answer < 2:
        issues.append("Opening does not start with a direct answer")
    if self_contained < 2:
        issues.append("Contains anaphoric references that reduce standalone readability")
    if specific_data < 2:
        issues.append("Lacks specific data points (numbers, percentages, dates)")
    if source_attribution < 2:
        issues.append("No named source citations in opening")

    return {
        "first_200_words": first_200,
        "word_count": len(words),
        "score": total,
        "breakdown": {
            "direct_answer": direct_answer,
            "self_contained": self_contained,
            "specific_data": specific_data,
            "source_attribution": source_attribution,
        },
        "interpretation": (
            "citation_ready" if total >= 6
            else "partially_citable" if total >= 3
            else "not_citable"
        ),
        "issues": issues,
        "meandering_patterns": meandering,
        "anaphoric_references": anaphoric,
    }


# ---------------------------------------------------------------------------
# Fetch
# ---------------------------------------------------------------------------

def fetch_html(url: str) -> str:
    from urllib.request import Request, urlopen
    req = Request(url, headers={"User-Agent": "Mozilla/5.0 (compatible; on-page-sgeo-audit/1.0)"})
    with urlopen(req, timeout=15) as resp:
        return resp.read().decode("utf-8", errors="replace")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser(
        description="Check direct-answer quality and GEO readiness of a page's opening content"
    )
    ap.add_argument("--url", required=True, help="Page URL to analyze")
    ap.add_argument("--tools", default=None, help="Path to tools.json inventory file")
    args = ap.parse_args()

    try:
        html = fetch_html(args.url)
    except Exception as e:
        print(json.dumps({"error": f"Failed to fetch URL: {e}", "url": args.url}), file=sys.stderr)
        sys.exit(1)

    extractor = ContentExtractor()
    extractor.feed(html)
    text = extractor.get_text()

    if not text:
        print(json.dumps({
            "url": args.url,
            "error": "Could not extract text content after H1",
            "score": 0,
        }))
        sys.exit(0)

    result = score_section(text)
    result["url"] = args.url
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
