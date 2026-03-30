#!/usr/bin/env python3
"""On-Page SGEO Audit — orchestrator script.

Runs all on-page-sgeo sub-scripts against a single URL and aggregates
results into the On-Page SGEO Audit Table format from SKILL.md Section 10.

Usage:
    python audit-page.py --url https://example.com/page
    python audit-page.py --url https://example.com/page --format md
    python audit-page.py --url https://example.com/page --tools tools.json

Flags:
    --url       Required. The page URL to audit.
    --format    Output format: 'json' (default) or 'md' (markdown table).
    --tools     Path to tools.json inventory file (passed through to sub-scripts).

Output: JSON audit report (default) or markdown table matching SKILL.md Section 10.
"""

import argparse
import importlib.util
import json
import os
import sys
from pathlib import Path
from typing import Optional


# ---------------------------------------------------------------------------
# Script loader — import sibling scripts as modules
# ---------------------------------------------------------------------------

SCRIPT_DIR = Path(__file__).parent


def load_script(name: str):
    """Import a sibling Python script as a module."""
    path = SCRIPT_DIR / name
    if not path.exists():
        return None
    spec = importlib.util.spec_from_file_location(name.replace(".py", ""), path)
    if spec is None or spec.loader is None:
        return None
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


# ---------------------------------------------------------------------------
# Sub-script runners
# ---------------------------------------------------------------------------

def fetch_html(url: str) -> str:
    from urllib.request import Request, urlopen
    req = Request(url, headers={"User-Agent": "Mozilla/5.0 (compatible; on-page-sgeo-audit/1.0)"})
    with urlopen(req, timeout=20) as resp:
        return resp.read().decode("utf-8", errors="replace")


def safe_run(label: str, fn, *args, **kwargs) -> dict:
    """Run a function, catching exceptions and returning error dict on failure."""
    try:
        return fn(*args, **kwargs)
    except Exception as e:
        return {"error": f"{label}: {e}"}


def run_meta_tags(html: str, url: str) -> dict:
    mod = load_script("extract-meta-tags.py")
    if mod is None:
        return {"error": "extract-meta-tags.py not found"}
    return mod.analyze(url, html)


def run_headings(html: str, url: str) -> dict:
    mod = load_script("analyze-headings.py")
    if mod is None:
        return {"error": "analyze-headings.py not found"}
    parser = mod.HeadingParser()
    parser.feed(html)
    result = mod.analyze_headings(parser.headings, parser.title)
    result["url"] = url
    return result


def run_direct_answer(html: str, url: str) -> dict:
    mod = load_script("check-direct-answer.py")
    if mod is None:
        return {"error": "check-direct-answer.py not found"}
    extractor = mod.ContentExtractor()
    extractor.feed(html)
    text = extractor.get_text()
    if not text:
        return {"url": url, "error": "No text content found after H1", "score": 0}
    result = mod.score_section(text)
    result["url"] = url
    return result


def run_internal_links(html: str, url: str) -> dict:
    mod = load_script("check-internal-links.py")
    if mod is None:
        return {"error": "check-internal-links.py not found"}
    return mod.analyze(url, html, check_broken=False)  # Skip broken check for speed


def run_images(html: str, url: str) -> dict:
    mod = load_script("check-images.py")
    if mod is None:
        return {"error": "check-images.py not found"}
    parser = mod.ImageExtractor(url)
    parser.feed(html)
    result = mod.analyze_images(parser.images, check_sizes=False)  # Skip HEAD requests for speed
    result["url"] = url
    result["has_picture_elements"] = parser.has_picture_elements
    return result


def run_structured_data(html: str, url: str) -> dict:
    mod = load_script("extract-structured-data.py")
    if mod is None:
        return {"error": "extract-structured-data.py not found"}
    return mod.analyze(url, html)


def run_freshness(html: str, url: str) -> dict:
    mod = load_script("check-freshness.py")
    if mod is None:
        return {"error": "check-freshness.py not found"}
    parser = mod.FreshnessExtractor()
    parser.feed(html)
    full_text = parser.get_text()
    visible_dates = mod.find_visible_dates(full_text)
    schema_dates = mod.extract_schema_dates(parser.jsonld_blocks)
    author = mod.find_author(full_text, parser.author_links)
    score, days_ago, issues = mod.compute_freshness_score(visible_dates, schema_dates, author)
    return {
        "url": url,
        "visible_dates": visible_dates[:5],
        "schema_dates": schema_dates,
        "author": author,
        "days_since_update": days_ago,
        "freshness_score": score,
        "issues": issues,
    }


# ---------------------------------------------------------------------------
# Audit table mapping
# ---------------------------------------------------------------------------

AUDIT_ROWS = [
    # (Element, SEO Impact, GEO Impact, extractor_fn)
    ("Title tag", "High", "Medium", "meta"),
    ("Meta description", "Medium", "Medium", "meta"),
    ("URL structure", "Medium", "Low", "manual"),
    ("H1 tag", "High", "Medium", "headings"),
    ("Heading hierarchy", "Medium", "High", "headings"),
    ("Direct-answer opening", "Low", "High", "direct_answer"),
    ("Knowledge blocks", "Low", "High", "direct_answer"),
    ("Internal links", "High", "Medium", "links"),
    ("Image alt text", "Medium", "Low", "images"),
    ("Image file size & format", "Medium", "Low", "images"),
    ("Image dimensions", "Medium", "Low", "images"),
    ("Structured data", "Medium", "High", "structured"),
    ("FAQPage schema", "Medium", "High", "structured"),
    ("dateModified in schema", "Low", "High", "freshness"),
    ("Visible last-updated date", "Low", "Medium", "freshness"),
    ("Author & credentials", "Medium", "High", "freshness"),
]


def derive_status(element: str, results: dict) -> tuple[str, str]:
    """Derive PASS/WARN/FAIL and a finding summary for an audit row."""
    meta = results.get("meta", {})
    headings = results.get("headings", {})
    direct = results.get("direct_answer", {})
    links = results.get("links", {})
    images = results.get("images", {})
    structured = results.get("structured", {})
    freshness = results.get("freshness", {})

    if element == "Title tag":
        t = meta.get("title", {})
        if t.get("valid"):
            return "PASS", f"{t.get('length', '?')} chars, valid"
        elif t.get("length", 0) == 0:
            return "FAIL", "Missing title tag"
        else:
            return "WARN", f"{t.get('length', '?')} chars (limit 60)"

    if element == "Meta description":
        d = meta.get("meta_description", {})
        if d.get("valid"):
            return "PASS", f"{d.get('length', '?')} chars, valid"
        elif d.get("length", 0) == 0:
            return "FAIL", "Missing meta description"
        else:
            return "WARN", f"{d.get('length', '?')} chars (limit 155)"

    if element == "URL structure":
        return "INFO", "Manual check required"

    if element == "H1 tag":
        count = headings.get("h1_count", 0)
        if count == 1:
            return "PASS", f"1 H1: \"{headings.get('h1_text', '')[:40]}\""
        elif count == 0:
            return "FAIL", "No H1 found"
        else:
            return "WARN", f"{count} H1 tags (should be 1)"

    if element == "Heading hierarchy":
        if headings.get("hierarchy_valid"):
            return "PASS", f"Valid hierarchy, {headings.get('total_headings', 0)} headings"
        else:
            skips = headings.get("skipped_levels", [])
            return "WARN", f"Skipped levels: {len(skips)} issue(s)"

    if element == "Direct-answer opening":
        score = direct.get("score", 0)
        interp = direct.get("interpretation", "unknown")
        if score >= 6:
            return "PASS", f"Score {score}/8 — {interp}"
        elif score >= 3:
            return "WARN", f"Score {score}/8 — {interp}"
        else:
            return "FAIL", f"Score {score}/8 — {interp}"

    if element == "Knowledge blocks":
        # Same as direct answer — we score the opening as proxy
        score = direct.get("score", 0)
        if score >= 6:
            return "PASS", "Opening section is self-contained"
        elif score >= 3:
            return "WARN", "Partially self-contained — check other H2 sections manually"
        else:
            return "FAIL", "Opening is not self-contained"

    if element == "Internal links":
        ratio = links.get("links_per_1000_words", 0)
        if 2 <= ratio <= 8:
            return "PASS", f"{ratio} per 1000 words"
        elif ratio < 2:
            return "WARN", f"{ratio} per 1000 words (target 3-5)"
        else:
            return "WARN", f"{ratio} per 1000 words (high — target 3-5)"

    if element == "Image alt text":
        img_issues = [i for i in images.get("issues", []) if i.get("type") in ("missing_alt", "keyword_stuffed_alt", "generic_alt")]
        if not img_issues:
            return "PASS", f"All {images.get('total_images', 0)} images have valid alt text"
        else:
            return "WARN", f"{len(img_issues)} image(s) with alt text issues"

    if element == "Image file size & format":
        size_issues = [i for i in images.get("issues", []) if i.get("type") in ("large_file", "legacy_format")]
        if not size_issues:
            return "PASS", "No oversized or legacy-format images detected"
        else:
            return "WARN", f"{len(size_issues)} image(s) need optimization"

    if element == "Image dimensions":
        dim_issues = [i for i in images.get("issues", []) if i.get("type") == "missing_dimensions"]
        if not dim_issues:
            return "PASS", "All images have width/height set"
        else:
            return "WARN", f"{len(dim_issues)} image(s) missing dimensions (CLS risk)"

    if element == "Structured data":
        count = structured.get("total_schemas", 0)
        if count > 0:
            types = [s.get("type", "?") for s in structured.get("schemas", [])]
            return "PASS", f"{count} schema(s): {', '.join(types)}"
        else:
            return "FAIL", "No JSON-LD structured data found"

    if element == "FAQPage schema":
        if structured.get("has_faq_schema"):
            return "PASS", "FAQPage schema present"
        else:
            return "INFO", "No FAQPage schema (add if page has Q&A content)"

    if element == "dateModified in schema":
        dm = freshness.get("schema_dates", {}).get("dateModified")
        if dm:
            return "PASS", f"dateModified: {dm}"
        else:
            return "FAIL", "No dateModified in schema"

    if element == "Visible last-updated date":
        vd = freshness.get("visible_dates", [])
        if vd:
            return "PASS", f"Found: {vd[0].get('text', '')[:40]}"
        else:
            return "WARN", "No visible date found on page"

    if element == "Author & credentials":
        auth = freshness.get("author", {})
        if auth.get("found") and auth.get("has_author_page_link"):
            return "PASS", f"{auth.get('name', 'Unknown')} (linked author page)"
        elif auth.get("found"):
            return "WARN", f"{auth.get('name', 'Unknown')} (no author page link)"
        else:
            return "FAIL", "No author byline found"

    return "INFO", "Unable to evaluate"


# ---------------------------------------------------------------------------
# Output formatting
# ---------------------------------------------------------------------------

def build_audit_table(results: dict) -> list[dict]:
    """Build audit rows from collected results."""
    rows = []
    for element, seo_impact, geo_impact, _source in AUDIT_ROWS:
        status, finding = derive_status(element, results)
        rows.append({
            "element": element,
            "seo_impact": seo_impact,
            "geo_impact": geo_impact,
            "status": status,
            "finding": finding,
        })
    return rows


def format_markdown(rows: list[dict], url: str) -> str:
    """Format audit rows as a markdown table."""
    lines = [
        f"# On-Page SGEO Audit: {url}",
        "",
        "| Element | SEO Impact | GEO Impact | Status | Finding |",
        "|---------|------------|------------|--------|---------|",
    ]
    for r in rows:
        lines.append(
            f"| {r['element']:<26} | {r['seo_impact']:<10} | {r['geo_impact']:<10} "
            f"| {r['status']:<6} | {r['finding']} |"
        )

    # Summary
    counts = {}
    for r in rows:
        s = r["status"]
        counts[s] = counts.get(s, 0) + 1

    lines.append("")
    parts = [f"**{k}:** {v}" for k, v in sorted(counts.items())]
    lines.append(f"**Summary:** {' | '.join(parts)}")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser(
        description="Run a complete On-Page SGEO audit against a URL"
    )
    ap.add_argument("--url", required=True, help="Page URL to audit")
    ap.add_argument("--format", choices=["json", "md"], default="json", help="Output format")
    ap.add_argument("--tools", default=None, help="Path to tools.json inventory file")
    args = ap.parse_args()

    # Fetch page once, share HTML across all scripts
    try:
        html = fetch_html(args.url)
    except Exception as e:
        print(json.dumps({"error": f"Failed to fetch URL: {e}", "url": args.url}), file=sys.stderr)
        sys.exit(1)

    # Run all analyses
    results = {
        "meta": safe_run("meta-tags", run_meta_tags, html, args.url),
        "headings": safe_run("headings", run_headings, html, args.url),
        "direct_answer": safe_run("direct-answer", run_direct_answer, html, args.url),
        "links": safe_run("internal-links", run_internal_links, html, args.url),
        "images": safe_run("images", run_images, html, args.url),
        "structured": safe_run("structured-data", run_structured_data, html, args.url),
        "freshness": safe_run("freshness", run_freshness, html, args.url),
    }

    # Build audit table
    rows = build_audit_table(results)

    if args.format == "md":
        print(format_markdown(rows, args.url))
    else:
        output = {
            "url": args.url,
            "audit_table": rows,
            "details": results,
            "summary": {},
        }
        for r in rows:
            s = r["status"]
            output["summary"][s] = output["summary"].get(s, 0) + 1
        print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
