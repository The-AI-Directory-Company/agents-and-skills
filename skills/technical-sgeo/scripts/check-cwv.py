#!/usr/bin/env python3
"""
check-cwv.py — Check Core Web Vitals via Google PageSpeed Insights API.

Fetches LCP, INP, CLS, and TTFB data (field + lab) for a URL. Identifies the
LCP element, CLS-causing elements, and overall performance score. Distinguishes
between field data (CrUX — what Google uses for ranking) and lab data (Lighthouse).

Usage:
    python3 check-cwv.py --url https://example.com
    python3 check-cwv.py --url https://example.com --strategy desktop
    python3 check-cwv.py --url https://example.com --strategy both
    python3 check-cwv.py --url https://example.com --api-key YOUR_KEY

AI Agent Usage:
    Agents can call the PageSpeed Insights API directly via WebFetch:
    GET https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url={url}&strategy=mobile&category=performance
    Parse loadingExperience.metrics for field data and lighthouseResult.audits for lab data.
    Field data is what Google uses for ranking — always prefer it over lab data.
"""

import argparse
import json
import sys
import urllib.request
import urllib.error
import time


PSI_ENDPOINT = "https://www.googleapis.com/pagespeedonline/v5/runPagespeed"

# CWV thresholds
THRESHOLDS = {
    "lcp": {"good": 2500, "needs_work": 4000},      # milliseconds
    "inp": {"good": 200, "needs_work": 500},          # milliseconds (field only)
    "cls": {"good": 0.1, "needs_work": 0.25},         # unitless
    "ttfb": {"good": 800, "needs_work": 1800},        # milliseconds
}


def classify_metric(value, metric_name):
    """Classify a metric value as good/needs_work/poor."""
    if value is None:
        return "no_data"
    t = THRESHOLDS.get(metric_name, {})
    if not t:
        return "unknown"
    if value <= t["good"]:
        return "good"
    elif value <= t["needs_work"]:
        return "needs_work"
    else:
        return "poor"


def fetch_psi(url, strategy="mobile", api_key=None):
    """Fetch PageSpeed Insights data. Returns (data_dict, error)."""
    params = f"url={urllib.request.quote(url, safe='')}&strategy={strategy}&category=performance"
    if api_key:
        params += f"&key={api_key}"

    request_url = f"{PSI_ENDPOINT}?{params}"

    try:
        req = urllib.request.Request(request_url)
        req.add_header("User-Agent", "check-cwv/1.0")
        response = urllib.request.urlopen(req, timeout=60)
        data = json.loads(response.read())
        return data, None
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        try:
            error_data = json.loads(body)
            msg = error_data.get("error", {}).get("message", f"HTTP {e.code}")
        except Exception:
            msg = f"HTTP {e.code}: {body[:200]}"
        return None, msg
    except Exception as e:
        return None, str(e)


def extract_field_data(data):
    """Extract field (CrUX) data from PSI response."""
    loading_exp = data.get("loadingExperience", {})
    metrics = loading_exp.get("metrics", {})
    available = loading_exp.get("overall_category") is not None

    field = {"available": available}

    # LCP
    lcp = metrics.get("LARGEST_CONTENTFUL_PAINT_MS", {})
    if lcp.get("percentile"):
        field["lcp_ms"] = lcp["percentile"]
        field["lcp_status"] = classify_metric(lcp["percentile"], "lcp")

    # INP (only available in field data)
    inp = metrics.get("INTERACTION_TO_NEXT_PAINT", {})
    if inp.get("percentile"):
        field["inp_ms"] = inp["percentile"]
        field["inp_status"] = classify_metric(inp["percentile"], "inp")

    # CLS
    cls_data = metrics.get("CUMULATIVE_LAYOUT_SHIFT_SCORE", {})
    if cls_data.get("percentile"):
        # CLS percentile is reported as an integer (multiply by 0.01)
        cls_value = cls_data["percentile"] / 100.0 if cls_data["percentile"] > 1 else cls_data["percentile"]
        field["cls"] = cls_value
        field["cls_status"] = classify_metric(cls_value, "cls")

    # TTFB
    ttfb = metrics.get("TIME_TO_FIRST_BYTE") or metrics.get("EXPERIMENTAL_TIME_TO_FIRST_BYTE", {})
    if ttfb.get("percentile"):
        field["ttfb_ms"] = ttfb["percentile"]
        field["ttfb_status"] = classify_metric(ttfb["percentile"], "ttfb")

    field["overall_category"] = loading_exp.get("overall_category")

    return field


def extract_lab_data(data):
    """Extract lab (Lighthouse) data from PSI response."""
    lighthouse = data.get("lighthouseResult", {})
    audits = lighthouse.get("audits", {})
    categories = lighthouse.get("categories", {})

    lab = {}

    # Performance score
    perf = categories.get("performance", {})
    if perf.get("score") is not None:
        lab["performance_score"] = int(perf["score"] * 100)

    # LCP
    lcp_audit = audits.get("largest-contentful-paint", {})
    if lcp_audit.get("numericValue"):
        lab["lcp_ms"] = round(lcp_audit["numericValue"])
        lab["lcp_status"] = classify_metric(lcp_audit["numericValue"], "lcp")
        lab["lcp_display"] = lcp_audit.get("displayValue", "")

    # LCP element identification
    lcp_element_audit = audits.get("largest-contentful-paint-element", {})
    if lcp_element_audit.get("details", {}).get("items"):
        items = lcp_element_audit["details"]["items"]
        if items:
            lab["lcp_element"] = items[0].get("node", {}).get("snippet", "unknown")

    # CLS
    cls_audit = audits.get("cumulative-layout-shift", {})
    if cls_audit.get("numericValue") is not None:
        lab["cls"] = round(cls_audit["numericValue"], 4)
        lab["cls_status"] = classify_metric(cls_audit["numericValue"], "cls")

    # CLS sources
    cls_items = audits.get("layout-shift-elements", {}).get("details", {}).get("items", [])
    if cls_items:
        lab["cls_elements"] = [
            {"element": item.get("node", {}).get("snippet", ""), "score": item.get("score", 0)}
            for item in cls_items[:5]
        ]

    # TTFB
    ttfb_audit = audits.get("server-response-time", {})
    if ttfb_audit.get("numericValue"):
        lab["ttfb_ms"] = round(ttfb_audit["numericValue"])
        lab["ttfb_status"] = classify_metric(ttfb_audit["numericValue"], "ttfb")

    # Total Blocking Time (proxy for INP in lab)
    tbt_audit = audits.get("total-blocking-time", {})
    if tbt_audit.get("numericValue") is not None:
        lab["tbt_ms"] = round(tbt_audit["numericValue"])
        lab["tbt_note"] = "TBT is a lab proxy for INP. INP is only measured in field data."

    # Speed Index
    si_audit = audits.get("speed-index", {})
    if si_audit.get("numericValue"):
        lab["speed_index_ms"] = round(si_audit["numericValue"])

    return lab


def run_check(url, strategy, api_key):
    """Run a single PSI check. Returns result dict."""
    data, error = fetch_psi(url, strategy, api_key)
    if error:
        return {"strategy": strategy, "error": error}

    field = extract_field_data(data)
    lab = extract_lab_data(data)

    # Build recommendation list
    recommendations = []
    if field.get("available"):
        if field.get("lcp_status") in ("needs_work", "poor"):
            recommendations.append(f"LCP is {field.get('lcp_ms')}ms (field) — optimize hero image, reduce TTFB, eliminate render-blocking resources.")
        if field.get("inp_status") in ("needs_work", "poor"):
            recommendations.append(f"INP is {field.get('inp_ms')}ms (field) — break long tasks, reduce JS bundle size, defer third-party scripts.")
        if field.get("cls_status") in ("needs_work", "poor"):
            recommendations.append(f"CLS is {field.get('cls')} (field) — add image dimensions, reserve space for dynamic content.")
        if field.get("ttfb_status") in ("needs_work", "poor"):
            recommendations.append(f"TTFB is {field.get('ttfb_ms')}ms (field) — enable CDN caching, optimize server response, use HTTP/2+.")
    else:
        recommendations.append("No field data available (site may lack sufficient Chrome traffic). Lab data used as proxy — note this limitation.")
        if lab.get("lcp_status") in ("needs_work", "poor"):
            recommendations.append(f"LCP is {lab.get('lcp_ms')}ms (lab) — optimize hero image, reduce TTFB.")
        if lab.get("cls_status") in ("needs_work", "poor"):
            recommendations.append(f"CLS is {lab.get('cls')} (lab) — add image dimensions, reserve space for dynamic content.")

    return {
        "strategy": strategy,
        "field_data": field,
        "lab_data": lab,
        "recommendations": recommendations,
    }


def main():
    parser = argparse.ArgumentParser(
        description="Check Core Web Vitals via Google PageSpeed Insights API.",
        epilog="Output: JSON with field (CrUX) and lab (Lighthouse) CWV data, LCP element, and recommendations."
    )
    parser.add_argument("--url", required=True, help="URL to check")
    parser.add_argument("--strategy", choices=["mobile", "desktop", "both"], default="mobile",
                        help="Device strategy (default: mobile — matches Google's mobile-first indexing)")
    parser.add_argument("--api-key", help="Google API key for higher rate limits (optional)")
    parser.add_argument("--tools", help="Path to tools.json from inventory-tools.py")
    args = parser.parse_args()

    strategies = ["mobile", "desktop"] if args.strategy == "both" else [args.strategy]

    results = {"url": args.url, "checks": []}

    for i, strategy in enumerate(strategies):
        if i > 0:
            time.sleep(2)  # Rate limiting between requests
        result = run_check(args.url, strategy, args.api_key)
        results["checks"].append(result)

    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
