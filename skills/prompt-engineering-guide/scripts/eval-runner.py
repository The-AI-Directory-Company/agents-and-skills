#!/usr/bin/env python3
"""
Prompt Evaluation Runner

Runs a test set of input/expected-output pairs against an LLM prompt and
prints an evaluation table covering format compliance, accuracy, and latency.

Usage:
    python eval-runner.py \
        --test-set test_cases.json \
        --provider openai \
        --model gpt-4 \
        --system-prompt prompt.txt \
        [--output results.md]

Test set format (JSON):
    [
        {
            "input": "The product crashed twice today.",
            "expected_output": {"sentiment": "negative", "urgency": "high"},
            "tags": ["negative", "edge-case"]
        },
        ...
    ]

Supported providers: openai, anthropic, google.
Set the corresponding API key as an environment variable:
    OPENAI_API_KEY, ANTHROPIC_API_KEY, or GOOGLE_API_KEY.
"""

import argparse
import json
import sys
import time
from pathlib import Path


# ---------------------------------------------------------------------------
# Provider adapters
# ---------------------------------------------------------------------------

def call_openai(model, system_prompt, user_input):
    """Call OpenAI API. Returns (response_text, latency_seconds)."""
    from openai import OpenAI
    client = OpenAI()
    start = time.time()
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_input},
        ],
        temperature=0,
    )
    latency = time.time() - start
    return response.choices[0].message.content, latency


def call_anthropic(model, system_prompt, user_input):
    """Call Anthropic API. Returns (response_text, latency_seconds)."""
    import anthropic
    client = anthropic.Anthropic()
    start = time.time()
    response = client.messages.create(
        model=model,
        max_tokens=2048,
        system=system_prompt,
        messages=[{"role": "user", "content": user_input}],
        temperature=0,
    )
    latency = time.time() - start
    return response.content[0].text, latency


def call_google(model, system_prompt, user_input):
    """Call Google Gemini API. Returns (response_text, latency_seconds)."""
    import google.generativeai as genai
    gen_model = genai.GenerativeModel(model, system_instruction=system_prompt)
    start = time.time()
    response = gen_model.generate_content(user_input)
    latency = time.time() - start
    return response.text, latency


PROVIDERS = {
    "openai": call_openai,
    "anthropic": call_anthropic,
    "google": call_google,
}


# ---------------------------------------------------------------------------
# Evaluation helpers
# ---------------------------------------------------------------------------

def check_json_format(response_text):
    """Check if the response is valid JSON. Returns (is_valid, parsed_or_None)."""
    try:
        parsed = json.loads(response_text.strip())
        return True, parsed
    except (json.JSONDecodeError, ValueError):
        # Try extracting JSON from markdown code blocks
        text = response_text.strip()
        if "```" in text:
            blocks = text.split("```")
            for block in blocks:
                cleaned = block.strip().removeprefix("json").strip()
                try:
                    parsed = json.loads(cleaned)
                    return True, parsed
                except (json.JSONDecodeError, ValueError):
                    continue
        return False, None


def check_accuracy(expected, actual_parsed):
    """
    Compare expected output with actual parsed output.
    Returns a score between 0.0 and 1.0.
    """
    if actual_parsed is None:
        return 0.0

    if isinstance(expected, dict) and isinstance(actual_parsed, dict):
        if not expected:
            return 1.0
        matches = 0
        for key, value in expected.items():
            if key in actual_parsed:
                if isinstance(value, str) and isinstance(actual_parsed[key], str):
                    if value.lower().strip() == actual_parsed[key].lower().strip():
                        matches += 1
                elif actual_parsed[key] == value:
                    matches += 1
        return matches / len(expected)

    if isinstance(expected, str) and isinstance(actual_parsed, str):
        return 1.0 if expected.strip().lower() == actual_parsed.strip().lower() else 0.0

    # Fallback: exact match
    return 1.0 if expected == actual_parsed else 0.0


def run_evaluation(test_cases, provider_fn, model, system_prompt):
    """Run all test cases and return results list."""
    results = []

    for i, case in enumerate(test_cases):
        user_input = case["input"]
        expected = case.get("expected_output")
        tags = case.get("tags", [])

        print(f"  Running case {i + 1}/{len(test_cases)}...", end=" ", flush=True)

        try:
            response_text, latency = provider_fn(model, system_prompt, user_input)
            is_valid_json, parsed = check_json_format(response_text)
            accuracy = check_accuracy(expected, parsed) if expected else None
            error = None
        except Exception as e:
            response_text = ""
            latency = 0
            is_valid_json = False
            parsed = None
            accuracy = 0.0
            error = str(e)

        status = "PASS" if (is_valid_json and (accuracy is None or accuracy >= 0.8)) else "FAIL"
        print(f"{status} ({latency:.2f}s)")

        results.append({
            "index": i + 1,
            "input_preview": user_input[:60] + ("..." if len(user_input) > 60 else ""),
            "tags": tags,
            "format_valid": is_valid_json,
            "accuracy": accuracy,
            "latency": latency,
            "response": response_text,
            "error": error,
        })

    return results


def format_report(results, model, provider):
    """Format evaluation results as a markdown report."""
    lines = []
    lines.append(f"# Prompt Evaluation Report\n")
    lines.append(f"**Model:** {model}")
    lines.append(f"**Provider:** {provider}")
    lines.append(f"**Test cases:** {len(results)}")
    lines.append("")

    # Summary
    format_pass = sum(1 for r in results if r["format_valid"])
    accuracy_scores = [r["accuracy"] for r in results if r["accuracy"] is not None]
    avg_accuracy = sum(accuracy_scores) / len(accuracy_scores) if accuracy_scores else None
    latencies = [r["latency"] for r in results if r["latency"] > 0]
    avg_latency = sum(latencies) / len(latencies) if latencies else 0
    p95_latency = sorted(latencies)[int(len(latencies) * 0.95)] if latencies else 0
    errors = sum(1 for r in results if r["error"])

    lines.append("## Summary\n")
    lines.append(f"| Metric | Value |")
    lines.append(f"|--------|-------|")
    lines.append(f"| Format compliance | {format_pass}/{len(results)} ({format_pass/len(results)*100:.0f}%) |")
    if avg_accuracy is not None:
        lines.append(f"| Average accuracy | {avg_accuracy:.2f} |")
    lines.append(f"| Avg latency | {avg_latency:.2f}s |")
    lines.append(f"| P95 latency | {p95_latency:.2f}s |")
    lines.append(f"| API errors | {errors} |")
    lines.append("")

    # Detail table
    lines.append("## Per-Case Results\n")
    lines.append("| # | Input | Tags | Format | Accuracy | Latency | Status |")
    lines.append("|---|-------|------|--------|----------|---------|--------|")

    for r in results:
        fmt = "OK" if r["format_valid"] else "FAIL"
        acc = f"{r['accuracy']:.2f}" if r["accuracy"] is not None else "N/A"
        lat = f"{r['latency']:.2f}s" if r["latency"] > 0 else "ERR"
        tags = ", ".join(r["tags"]) if r["tags"] else "-"
        status = "PASS" if (r["format_valid"] and (r["accuracy"] is None or r["accuracy"] >= 0.8)) else "FAIL"
        lines.append(f"| {r['index']} | {r['input_preview']} | {tags} | {fmt} | {acc} | {lat} | {status} |")

    lines.append("")

    # Failures detail
    failures = [r for r in results if not r["format_valid"] or (r["accuracy"] is not None and r["accuracy"] < 0.8)]
    if failures:
        lines.append("## Failure Details\n")
        for r in failures:
            lines.append(f"### Case {r['index']}")
            lines.append(f"**Input:** {r['input_preview']}")
            if r["error"]:
                lines.append(f"**Error:** {r['error']}")
            else:
                lines.append(f"**Response (first 200 chars):** `{r['response'][:200]}`")
            lines.append("")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Run prompt evaluation against a test set.")
    parser.add_argument("--test-set", required=True, help="Path to test cases JSON file")
    parser.add_argument("--provider", required=True, choices=PROVIDERS.keys(), help="LLM provider")
    parser.add_argument("--model", required=True, help="Model name (e.g., gpt-4, claude-sonnet-4-20250514)")
    parser.add_argument("--system-prompt", required=True, help="Path to system prompt text file")
    parser.add_argument("--output", default=None, help="Output file path (default: stdout)")

    args = parser.parse_args()

    # Load test set
    test_path = Path(args.test_set)
    if not test_path.exists():
        print(f"Error: Test set not found: {args.test_set}", file=sys.stderr)
        sys.exit(1)

    with open(test_path) as f:
        test_cases = json.load(f)

    # Load system prompt
    prompt_path = Path(args.system_prompt)
    if not prompt_path.exists():
        print(f"Error: System prompt not found: {args.system_prompt}", file=sys.stderr)
        sys.exit(1)

    system_prompt = prompt_path.read_text().strip()

    # Run evaluation
    provider_fn = PROVIDERS[args.provider]
    print(f"\nEvaluating {len(test_cases)} cases with {args.provider}/{args.model}...\n")
    results = run_evaluation(test_cases, provider_fn, args.model, system_prompt)

    # Generate report
    report = format_report(results, args.model, args.provider)

    if args.output:
        Path(args.output).write_text(report)
        print(f"\nReport written to {args.output}")
    else:
        print("\n" + report)


if __name__ == "__main__":
    main()
