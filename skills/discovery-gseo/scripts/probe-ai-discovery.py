#!/usr/bin/env python3
"""
probe-ai-discovery.py — GEO backbone: test queries on AI platforms, record citations, find gaps.

The GEO differentiator script. For each query, probes AI platforms (Perplexity, cached
AI answers) to assess which brands get cited, what sources are used, and where gaps
exist. Identifies GEO-validated topics and citation opportunities.

Usage:
    python3 probe-ai-discovery.py --queries queries.txt
    python3 probe-ai-discovery.py --queries queries.txt --brand "AcmeInvoice"
    python3 probe-ai-discovery.py --queries queries.txt --brand "AcmeInvoice" --api dataforseo

AI Agent Usage:
    For each query in the queries file:
    1. Check Perplexity:
       - WebFetch("https://www.perplexity.ai/search?q={url_encoded_query}")
       - Extract: cited sources (URLs), brands mentioned, answer quality
       - Record source quality: strong (high-DA, authoritative) / medium / weak
    2. Check cached AI answers:
       - WebSearch("{query} site:perplexity.ai") → find cached Perplexity results
       - WebSearch("{query} AI answer") → find AI-generated content about this topic
    3. If --brand provided:
       - Check if brand appears in any AI response
       - Record brand citation rate across queries
    4. Score each query:
       - ai_answers: true/false (does AI provide a substantive answer?)
       - gap_opportunity: high (weak/few sources) / medium (strong sources) / low (no AI answer)
    5. Aggregate: brand_citation_rate, high_gap_queries count, geo_validated_topics list

    Optional paid path (DataForSEO AI endpoints):
    - Use DataForSEO AI visibility API for structured citation data
"""

import argparse
import json
import sys
import urllib.parse


def probe_queries(queries, brand=None, api="websearch"):
    """
    Probe AI platforms for each query to assess GEO opportunity.

    The AI agent executes WebFetch/WebSearch calls to check AI platform responses.
    """
    results = []
    brand_citations = 0
    high_gap_count = 0
    geo_validated_topics = []

    for query in queries:
        query = query.strip()
        if not query:
            continue

        encoded = urllib.parse.quote_plus(query)

        # --- Agent execution steps ---
        # 1. WebFetch(url=f"https://www.perplexity.ai/search?q={encoded}")
        #    Parse response for: cited sources, brands mentioned, answer substance
        # 2. WebSearch(query=f"{query} site:perplexity.ai")
        #    Check for cached Perplexity results
        # 3. WebSearch(query=f"'{query}' AI answer OR AI overview")
        #    Check for AI-generated content on this topic
        # 4. If brand: check if brand name appears in any response

        query_result = {
            "query": query,
            "ai_answers": False,  # Agent sets True if AI gives substantive answer
            "brands_cited": [],  # Agent fills from Perplexity response
            "user_brand_cited": False,  # Agent checks if brand appears
            "sources": [],  # [{"url": "...", "quality": "strong|medium|weak"}]
            "gap_opportunity": "unknown",  # Agent scores: high/medium/low
            "topic": query,  # Topic extracted from query
        }

        # Agent scoring logic:
        # - If AI answers with weak/few sources → gap_opportunity = "high"
        # - If AI answers with strong sources → gap_opportunity = "medium"
        # - If AI doesn't answer substantively → gap_opportunity = "low"

        if brand and query_result.get("user_brand_cited"):
            brand_citations += 1

        if query_result.get("gap_opportunity") == "high":
            high_gap_count += 1

        if query_result.get("ai_answers"):
            # Extract topic from query for geo_validated_topics
            topic = query.replace("best ", "").replace("how to ", "").replace("what is ", "")
            geo_validated_topics.append(topic)

        results.append(query_result)

    total = len(results)
    summary = {
        "brand_citation_rate": (brand_citations / total) if total > 0 else 0,
        "high_gap_queries": high_gap_count,
        "geo_validated_topics": list(set(geo_validated_topics)),
    }

    return results, summary


def main():
    parser = argparse.ArgumentParser(
        description="GEO backbone: test queries on AI platforms, record citations, find gaps."
    )
    parser.add_argument(
        "--queries",
        type=str,
        required=True,
        help="Path to file with queries to test, one per line",
    )
    parser.add_argument(
        "--brand",
        type=str,
        help="Brand name to check for in AI citations (e.g., 'AcmeInvoice')",
    )
    parser.add_argument(
        "--api",
        type=str,
        choices=["websearch", "dataforseo"],
        default="websearch",
        help="Data source for AI probing (default: websearch)",
    )
    parser.add_argument("--tools", type=str, help="Path to tools.json inventory file")

    args = parser.parse_args()

    try:
        with open(args.queries, "r") as f:
            queries = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(json.dumps({"error": f"Queries file not found: {args.queries}"}))
        sys.exit(1)

    if not queries:
        print(json.dumps({"error": "No queries found in file."}))
        sys.exit(1)

    results, summary = probe_queries(queries, brand=args.brand, api=args.api)

    output = {
        "queries_tested": len(results),
        "brand": args.brand,
        "method": args.api,
        "results": results,
        "summary": summary,
    }

    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
