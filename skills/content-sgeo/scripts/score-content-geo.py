#!/usr/bin/env python3
"""
score-content-geo.py — Score a URL against the 8-element GEO Content Framework.

Analyzes content for: TLDR first, question-format headers, data density,
self-contained sections, expert quotations, source citations, original value,
and author attribution. Outputs a 0-40 score with element-by-element breakdown.

This is the key feedback loop for content SGEO: run before optimization to
get a baseline score, then run again after changes to measure improvement.

Usage:
    python score-content-geo.py --url https://example.com/article
    python score-content-geo.py --url https://example.com/article --tools tools.json

Free path: WebFetch + HTML parsing. No paid extension needed.
Scoring rubric: see references/geo-content-framework.md
"""

import argparse
import json
import re
import sys
import urllib.request
import urllib.parse
from html.parser import HTMLParser
from typing import Any


def load_tools(tools_path: str | None) -> dict[str, Any]:
    """Load tool inventory from JSON file if provided."""
    if tools_path:
        try:
            with open(tools_path, "r") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Warning: Could not load tools file: {e}", file=sys.stderr)
    return {}


def fetch_page(url: str) -> str:
    """Fetch a page's HTML content."""
    try:
        req = urllib.request.Request(url, headers={
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                          "AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/120.0.0.0 Safari/537.36"
        })
        with urllib.request.urlopen(req, timeout=15) as resp:
            return resp.read().decode("utf-8", errors="replace")
    except Exception as e:
        print(f"Error: Failed to fetch {url}: {e}", file=sys.stderr)
        sys.exit(1)


class ContentParser(HTMLParser):
    """Parse HTML to extract structured content for GEO scoring."""

    def __init__(self):
        super().__init__()
        self.headings: list[dict[str, Any]] = []
        self.current_heading: dict[str, Any] | None = None
        self.sections: list[dict[str, Any]] = []
        self.current_section_text: list[str] = []
        self.title: str = ""
        self.in_title = False
        self.in_script = False
        self.in_style = False
        self.in_main = False
        self.in_article = False
        self.main_depth = 0
        self.text_parts: list[str] = []
        self.links: list[dict[str, str]] = []
        self.blockquotes: list[str] = []
        self.in_blockquote = False
        self.blockquote_text: list[str] = []
        self.json_ld_blocks: list[str] = []
        self.in_json_ld = False
        self.json_ld_buffer: list[str] = []
        self.found_h1 = False

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]):
        tag_lower = tag.lower()
        attr_dict = dict(attrs)

        if tag_lower == "title":
            self.in_title = True
        elif tag_lower == "main":
            self.in_main = True
            self.main_depth += 1
        elif tag_lower == "article":
            self.in_article = True
        elif tag_lower == "script":
            if attr_dict.get("type") == "application/ld+json":
                self.in_json_ld = True
                self.json_ld_buffer = []
            else:
                self.in_script = True
        elif tag_lower == "style":
            self.in_style = True
        elif tag_lower == "blockquote":
            self.in_blockquote = True
            self.blockquote_text = []
        elif tag_lower == "a":
            href = attr_dict.get("href", "")
            if href and href.startswith("http"):
                self.links.append({"href": href, "text": ""})
        elif tag_lower in ("h1", "h2", "h3", "h4", "h5", "h6"):
            level = int(tag_lower[1])
            # Save previous section
            if self.current_heading and self.current_section_text:
                self.sections.append({
                    "heading": self.current_heading,
                    "text": " ".join(self.current_section_text),
                })
            if level == 1:
                self.found_h1 = True
            self.current_heading = {"level": level, "text": ""}
            self.current_section_text = []

    def handle_endtag(self, tag: str):
        tag_lower = tag.lower()
        if tag_lower == "title":
            self.in_title = False
        elif tag_lower == "main":
            self.main_depth -= 1
            if self.main_depth <= 0:
                self.in_main = False
        elif tag_lower == "article":
            self.in_article = False
        elif tag_lower == "script":
            if self.in_json_ld:
                self.json_ld_blocks.append("".join(self.json_ld_buffer))
                self.in_json_ld = False
            self.in_script = False
        elif tag_lower == "style":
            self.in_style = False
        elif tag_lower == "blockquote":
            self.in_blockquote = False
            self.blockquotes.append(" ".join(self.blockquote_text))
        elif tag_lower in ("h1", "h2", "h3", "h4", "h5", "h6"):
            if self.current_heading:
                self.headings.append(self.current_heading)

    def handle_data(self, data: str):
        if self.in_json_ld:
            self.json_ld_buffer.append(data)
        elif self.in_title:
            self.title += data
        elif self.in_blockquote:
            self.blockquote_text.append(data.strip())
        elif self.current_heading is not None and not data.strip():
            pass
        elif self.current_heading is not None:
            self.current_heading["text"] += data
        elif not self.in_script and not self.in_style:
            stripped = data.strip()
            if stripped:
                self.text_parts.append(stripped)
                self.current_section_text.append(stripped)

    def finalize(self):
        """Call after feeding all HTML to save the last section."""
        if self.current_heading and self.current_section_text:
            self.sections.append({
                "heading": self.current_heading,
                "text": " ".join(self.current_section_text),
            })


# ─── Scoring Functions ────────────────────────────────────────────────

def score_tldr_first(text_parts: list[str], sections: list[dict]) -> tuple[int, list[str]]:
    """
    Score Element 1: TLDR First (0-5).
    Check if first 200 words directly answer the primary question.
    """
    recommendations = []

    # Get text after first H1 (or all text if no H1)
    full_text = " ".join(text_parts)
    words = full_text.split()
    first_200 = " ".join(words[:200]).lower()

    if len(words) < 50:
        recommendations.append("Content is very short — insufficient for scoring")
        return 0, recommendations

    score = 0

    # Check for meandering patterns (negative signals)
    meandering = [
        "in today's", "as we all know", "when it comes to",
        "it's no secret", "in the ever-changing", "in recent years",
        "it goes without saying", "in this article we will",
        "welcome to our", "thank you for visiting",
    ]
    has_meandering = any(p in first_200 for p in meandering)

    # Check for direct answer signals (positive signals)
    direct_answer_patterns = [
        r'\d+%',  # Percentages
        r'\$[\d,]+',  # Dollar amounts
        r'\d+\.\d+',  # Decimal numbers
        r'(?:is|are|means|refers to)\s',  # Definitions
    ]
    has_data = sum(1 for p in direct_answer_patterns if re.search(p, first_200))

    # Check for specific, sourced data
    has_source = bool(re.search(
        r'\((?:[A-Z][a-z]+\s?)+,?\s*\d{4}\)', first_200  # (Source Name, 2025)
    ))

    if has_meandering:
        score = max(score, 1)
        recommendations.append("Opening uses meandering patterns — start with the answer")
    elif has_data >= 2 and has_source:
        score = 5
    elif has_data >= 2:
        score = 4
        recommendations.append("Add source attribution to opening statistics")
    elif has_data >= 1:
        score = 3
        recommendations.append("Add more specific data to the opening paragraph")
    else:
        score = 2
        recommendations.append("First 200 words lack specific data — add statistics or concrete facts")

    return score, recommendations


def score_question_headers(headings: list[dict]) -> tuple[int, list[str]]:
    """
    Score Element 2: Question-Format Headers (0-5).
    Calculate % of H2s that are question-format.
    """
    recommendations = []
    h2s = [h for h in headings if h["level"] == 2]

    if not h2s:
        recommendations.append("No H2 headings found — add section headings")
        return 0, recommendations

    question_count = sum(
        1 for h in h2s
        if re.match(
            r'^(what|how|why|when|where|is|can|does|will|should|which|do)',
            h["text"].strip().lower()
        ) or h["text"].strip().endswith("?")
    )

    ratio = question_count / len(h2s)

    if ratio > 0.6:
        score = 5
    elif ratio > 0.5:
        score = 4
    elif ratio > 0.3:
        score = 3
    elif ratio > 0.15:
        score = 2
    elif question_count > 0:
        score = 1
    else:
        score = 0
        recommendations.append("No question-format H2s — convert declarative headings to questions")

    if ratio < 0.4:
        declarative = [h["text"].strip() for h in h2s
                       if not re.match(r'^(what|how|why|when|where|is|can|does|will|should|which)',
                                       h["text"].strip().lower())
                       and not h["text"].strip().endswith("?")]
        if declarative:
            recommendations.append(
                f"Consider converting these H2s to questions: {', '.join(declarative[:3])}"
            )

    return score, recommendations


def score_data_density(text_parts: list[str]) -> tuple[int, list[str]]:
    """
    Score Element 3: Data Density (0-5).
    Count statistics/numbers per 500 words.
    """
    recommendations = []
    full_text = " ".join(text_parts)
    word_count = len(full_text.split())

    if word_count < 100:
        return 0, ["Content too short to evaluate data density"]

    # Count data points: percentages, dollar amounts, specific numbers with context
    data_patterns = [
        r'\d+(?:\.\d+)?%',  # Percentages
        r'\$[\d,]+(?:\.\d+)?',  # Dollar amounts
        r'\d+(?:,\d{3})+',  # Large numbers with commas
        r'\d+x\b',  # Multipliers (3x, 10x)
        r'(?:increased|decreased|grew|dropped|rose|fell)\s+(?:by\s+)?\d+',
    ]

    total_data_points = 0
    for pattern in data_patterns:
        matches = re.findall(pattern, full_text, re.IGNORECASE)
        total_data_points += len(matches)

    # Check for sourced data
    source_pattern = r'\((?:[A-Z][a-z]+[\s,]*)+\d{4}\)'
    sourced_count = len(re.findall(source_pattern, full_text))

    # Calculate density per 500 words
    density = (total_data_points / word_count) * 500 if word_count > 0 else 0

    if density > 3 and sourced_count >= 3:
        score = 5
    elif density > 3:
        score = 4
        recommendations.append("Good data density — add source citations to statistics")
    elif density > 1:
        score = 3
        recommendations.append("Moderate data density — add more specific statistics")
    elif density > 0.5:
        score = 2
        recommendations.append("Low data density — content needs more specific numbers and statistics")
    elif total_data_points > 0:
        score = 1
        recommendations.append("Very few data points — add percentages, dollar amounts, specific numbers")
    else:
        score = 0
        recommendations.append("No data found — add specific statistics with sources")

    return score, recommendations


def score_self_contained(sections: list[dict]) -> tuple[int, list[str]]:
    """
    Score Element 4: Self-Contained Sections (0-5).
    Check for anaphoric references in H2 sections.
    """
    recommendations = []
    h2_sections = [s for s in sections if s["heading"]["level"] == 2]

    if not h2_sections:
        return 0, ["No H2 sections to evaluate"]

    anaphoric_patterns = [
        r'\bas mentioned\b', r'\bas discussed\b', r'\bas noted\b',
        r'\bsee (?:above|previous|earlier)\b', r'\bthe above\b',
        r'\bas we (?:saw|discussed|mentioned|noted)\b',
        r'^(?:furthermore|additionally|moreover)\b',
        r'^(?:this|these|it|they)\s+(?:is|are|was|were|has|have)\b',
    ]

    sections_with_issues = 0
    problem_sections = []

    for section in h2_sections:
        text = section["text"].lower()
        # Check first 50 words of each section
        first_words = " ".join(text.split()[:50])
        has_anaphoric = any(
            re.search(p, first_words, re.IGNORECASE)
            for p in anaphoric_patterns
        )
        if has_anaphoric:
            sections_with_issues += 1
            problem_sections.append(section["heading"]["text"].strip())

    if not h2_sections:
        return 0, ["No sections to evaluate"]

    issue_ratio = sections_with_issues / len(h2_sections)

    if issue_ratio == 0:
        score = 5
    elif issue_ratio < 0.1:
        score = 4
    elif issue_ratio < 0.25:
        score = 3
    elif issue_ratio < 0.5:
        score = 2
        recommendations.append(
            f"Sections with context dependencies: {', '.join(problem_sections[:3])}"
        )
    elif issue_ratio < 0.75:
        score = 1
        recommendations.append("Most sections depend on prior context — restructure for independence")
    else:
        score = 0
        recommendations.append("Sections read as continuous narrative — each must stand alone")

    return score, recommendations


def score_expert_quotations(text_parts: list[str],
                             blockquotes: list[str]) -> tuple[int, list[str]]:
    """
    Score Element 5: Expert Quotations (0-5).
    Check for attributed quotes from named sources.
    """
    recommendations = []
    full_text = " ".join(text_parts)

    # Count blockquotes
    quote_count = len(blockquotes)

    # Check for inline attribution patterns
    attribution_patterns = [
        r'(?:according to|says?|said|notes?|noted|explains?|explained)\s+[A-Z][a-z]+\s+[A-Z][a-z]+',
        r'[A-Z][a-z]+\s+[A-Z][a-z]+,\s+(?:CEO|CTO|VP|Director|Head|Chief|Professor|Dr\.)',
        r'"[^"]{20,}"[\s—\-]+[A-Z][a-z]+\s+[A-Z][a-z]+',
        r'\u201c[^\u201d]{20,}\u201d',  # Smart quotes
    ]

    attributed_quotes = 0
    for pattern in attribution_patterns:
        matches = re.findall(pattern, full_text)
        attributed_quotes += len(matches)

    total_quotes = quote_count + attributed_quotes

    if total_quotes >= 3 and attributed_quotes >= 2:
        score = 5
    elif total_quotes >= 2 and attributed_quotes >= 1:
        score = 4
    elif total_quotes >= 1 and attributed_quotes >= 1:
        score = 3
    elif total_quotes >= 1:
        score = 2
        recommendations.append("Quotes present but lack named attribution — add expert names and credentials")
    elif quote_count > 0:
        score = 1
        recommendations.append("Blockquotes found but no attribution — add expert names")
    else:
        score = 0
        recommendations.append("No expert quotations — add quotes from named industry authorities")

    return score, recommendations


def score_source_citations(links: list[dict], text_parts: list[str]) -> tuple[int, list[str]]:
    """
    Score Element 6: Source Citations (0-5).
    Count outbound links to external sources.
    """
    recommendations = []
    full_text = " ".join(text_parts)

    # Count external links (excluding social media, navigation)
    excluded_domains = [
        "twitter.com", "x.com", "facebook.com", "linkedin.com/in/",
        "instagram.com", "youtube.com/channel", "github.com",
    ]
    external_links = [
        link for link in links
        if not any(d in link["href"] for d in excluded_domains)
    ]

    # Also check for inline citation patterns (Source, Year)
    inline_citations = len(re.findall(
        r'\((?:[A-Z][a-z]+[\s,]*)+\d{4}\)', full_text
    ))

    total_citations = len(external_links) + inline_citations

    if total_citations >= 5:
        score = 5
    elif total_citations >= 3:
        score = 4
    elif total_citations >= 2:
        score = 3
    elif total_citations >= 1:
        score = 2
        recommendations.append("Only 1 external citation — add 3-5 primary source references")
    else:
        score = 0
        recommendations.append("No source citations — add links to studies, reports, or official documentation")

    return score, recommendations


def score_original_value(text_parts: list[str]) -> tuple[int, list[str]]:
    """
    Score Element 7: Original Value (0-5).
    Check for indicators of original data, frameworks, or case studies.
    """
    recommendations = []
    full_text = " ".join(text_parts).lower()

    original_indicators = [
        (r'\bour (?:data|research|study|survey|analysis|benchmark)\b', "original_research"),
        (r'\bwe (?:tested|surveyed|analyzed|measured|benchmarked|found)\b', "first_hand_testing"),
        (r'\bour (?:framework|methodology|model|approach|system)\b', "proprietary_framework"),
        (r'\bcase study\b', "case_study"),
        (r'\b(?:our|my) (?:experience|client|project|team)\b', "direct_experience"),
        (r'\b(?:we|i) (?:built|created|developed|designed|implemented)\b', "built_something"),
        (r'\bproprietary\b', "proprietary"),
        (r'\bfirst-hand\b', "first_hand"),
    ]

    found_indicators: list[str] = []
    for pattern, indicator_type in original_indicators:
        if re.search(pattern, full_text):
            found_indicators.append(indicator_type)

    unique_types = set(found_indicators)

    if len(unique_types) >= 3:
        score = 5
    elif len(unique_types) >= 2:
        score = 4
    elif len(unique_types) >= 1:
        score = 3
    elif "case_study" in found_indicators or "first_hand_testing" in found_indicators:
        score = 3
    else:
        score = 1
        recommendations.append(
            "No original value detected — add your own data, case study, "
            "or proprietary framework. Flag for human review."
        )

    if score < 3:
        recommendations.append(
            "Consider adding: original data, a case study with specific results, "
            "or a unique framework"
        )

    return score, recommendations


def score_author_attribution(html: str, json_ld_blocks: list[str]) -> tuple[int, list[str]]:
    """
    Score Element 8: Author Attribution (0-5).
    Check for author byline, author page link, and credentials.
    """
    recommendations = []
    html_lower = html.lower()

    # Check for author byline patterns
    author_patterns = [
        r'(?:by|author[:\s])\s*<a[^>]*>([^<]+)</a>',
        r'class="[^"]*author[^"]*"[^>]*>([^<]+)',
        r'rel="author"',
        r'itemprop="author"',
    ]

    has_author = any(re.search(p, html, re.IGNORECASE) for p in author_patterns)

    # Check for author page link
    has_author_link = bool(re.search(
        r'<a[^>]*href="[^"]*(?:/author/|/team/|/about/|/people/)[^"]*"',
        html, re.IGNORECASE
    ))

    # Check schema for author
    has_schema_author = False
    for block in json_ld_blocks:
        try:
            data = json.loads(block)
            if isinstance(data, dict):
                author = data.get("author", {})
                if isinstance(author, dict) and author.get("name"):
                    has_schema_author = True
                elif isinstance(author, list) and author:
                    has_schema_author = True
        except json.JSONDecodeError:
            pass

    # Check for credentials near author
    has_credentials = bool(re.search(
        r'(?:CEO|CTO|VP|Director|Head|Chief|Professor|Dr\.|PhD|Editor|'
        r'Founder|Manager|Lead|Senior|Principal)',
        html
    ))

    # Check for visible date
    has_date = bool(re.search(
        r'(?:updated|modified|published)\s*:?\s*(?:on\s+)?'
        r'(?:\d{4}[-/]\d{1,2}[-/]\d{1,2}|'
        r'(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{1,2})',
        html, re.IGNORECASE
    ))

    # Calculate score
    signals = sum([has_author, has_author_link, has_schema_author,
                   has_credentials, has_date])

    if signals >= 5:
        score = 5
    elif signals >= 4:
        score = 4
    elif signals >= 3:
        score = 3
    elif signals >= 2:
        score = 2
    elif signals >= 1:
        score = 1
    else:
        score = 0

    if not has_author:
        recommendations.append("No author byline found — add a named author")
    if not has_author_link:
        recommendations.append("No author page link — link author name to a bio page")
    if not has_schema_author:
        recommendations.append("No author in structured data — add Person to Article schema")
    if not has_credentials:
        recommendations.append("No credentials visible — show why the author is qualified")
    if not has_date:
        recommendations.append("No visible date — add 'Last updated' with a date")

    return score, recommendations


def interpret_score(total: int) -> str:
    """Interpret the total GEO score."""
    if total <= 10:
        return "not_citable"
    elif total <= 20:
        return "partially_citable"
    elif total <= 30:
        return "good"
    else:
        return "excellent"


def main():
    parser = argparse.ArgumentParser(
        description="Score content against the 8-element GEO Content Framework (0-40).",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Scoring: 8 elements x 0-5 points = 0-40 total
  0-10: Not citable — major rework needed
  11-20: Partially citable — significant gaps
  21-30: Good — citation-ready, focus on weak elements
  31-40: Excellent — high citation potential

Examples:
    python score-content-geo.py --url https://example.com/article
    python score-content-geo.py --url https://example.com/article --tools tools.json
        """,
    )
    parser.add_argument(
        "--url",
        required=True,
        help="URL to score",
    )
    parser.add_argument(
        "--tools",
        help="Path to tools.json inventory file",
    )
    args = parser.parse_args()

    tools = load_tools(args.tools)

    # Fetch and parse the page
    print(f"Fetching: {args.url}", file=sys.stderr)
    html = fetch_page(args.url)

    content = ContentParser()
    try:
        content.feed(html)
        content.finalize()
    except Exception as e:
        print(f"Error parsing HTML: {e}", file=sys.stderr)
        sys.exit(1)

    # Score each element
    all_recommendations = []

    tldr_score, tldr_recs = score_tldr_first(content.text_parts, content.sections)
    all_recommendations.extend(tldr_recs)

    headers_score, headers_recs = score_question_headers(content.headings)
    all_recommendations.extend(headers_recs)

    data_score, data_recs = score_data_density(content.text_parts)
    all_recommendations.extend(data_recs)

    self_contained_score, sc_recs = score_self_contained(content.sections)
    all_recommendations.extend(sc_recs)

    quotes_score, quotes_recs = score_expert_quotations(
        content.text_parts, content.blockquotes
    )
    all_recommendations.extend(quotes_recs)

    citations_score, citations_recs = score_source_citations(
        content.links, content.text_parts
    )
    all_recommendations.extend(citations_recs)

    original_score, original_recs = score_original_value(content.text_parts)
    all_recommendations.extend(original_recs)

    author_score, author_recs = score_author_attribution(html, content.json_ld_blocks)
    all_recommendations.extend(author_recs)

    # Calculate total
    total = (tldr_score + headers_score + data_score + self_contained_score +
             quotes_score + citations_score + original_score + author_score)

    rating = interpret_score(total)

    # Interpretation text
    interpretations = {
        "not_citable": "Content is too vague, unsourced, or poorly structured for AI citation. Major rework needed.",
        "partially_citable": "Some elements present but significant gaps. AI may cite if no better source exists.",
        "good": "Citation-ready for most queries. Focus on weak elements to push higher.",
        "excellent": "Well-structured, data-rich, authoritative content. Top-tier citation candidate.",
    }

    output = {
        "url": args.url,
        "total_score": total,
        "max_score": 40,
        "rating": rating,
        "breakdown": {
            "tldr_first": tldr_score,
            "question_headers": headers_score,
            "data_density": data_score,
            "self_contained": self_contained_score,
            "expert_quotations": quotes_score,
            "source_citations": citations_score,
            "original_value": original_score,
            "author_attribution": author_score,
        },
        "recommendations": [r for r in all_recommendations if r],
        "interpretation": interpretations.get(rating, ""),
        "tools_used": {
            "webfetch": True,
        },
    }
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
