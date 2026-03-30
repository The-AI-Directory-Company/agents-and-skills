#!/usr/bin/env python3
"""
Threat Scoring Tool

Reads a CSV of threats with Likelihood and Impact scores,
calculates Risk Score (Likelihood x Impact), assigns Priority bands,
and outputs a sorted table.

Usage:
    python score-threats.py threats.csv
    python score-threats.py threats.csv --output scored.csv
    python score-threats.py threats.csv --format markdown

Input CSV format:
    ID,Likelihood,Impact
    S-1,3,5
    T-1,4,4
    E-1,4,5

Priority bands:
    Critical: 15-25
    High:     8-14
    Medium:   4-7
    Low:      1-3
"""

import argparse
import csv
import sys
from pathlib import Path


PRIORITY_BANDS = [
    (15, 25, "Critical"),
    (8, 14, "High"),
    (4, 7, "Medium"),
    (1, 3, "Low"),
]


def get_priority(score: int) -> str:
    """Map a risk score to a priority band."""
    for low, high, label in PRIORITY_BANDS:
        if low <= score <= high:
            return label
    if score > 25:
        return "Critical"
    return "Low"


def read_threats(filepath: str) -> list[dict]:
    """Read threat CSV and return list of threat dicts."""
    threats = []
    path = Path(filepath)

    if not path.exists():
        print(f"Error: file not found: {filepath}", file=sys.stderr)
        sys.exit(1)

    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)

        # Validate headers
        required = {"ID", "Likelihood", "Impact"}
        if not required.issubset(set(reader.fieldnames or [])):
            print(
                f"Error: CSV must have columns: {', '.join(sorted(required))}",
                file=sys.stderr,
            )
            print(f"Found: {', '.join(reader.fieldnames or [])}", file=sys.stderr)
            sys.exit(1)

        for row_num, row in enumerate(reader, start=2):
            try:
                likelihood = int(row["Likelihood"])
                impact = int(row["Impact"])
            except ValueError:
                print(
                    f"Error: row {row_num} has non-integer Likelihood or Impact: {row}",
                    file=sys.stderr,
                )
                sys.exit(1)

            if not (1 <= likelihood <= 5):
                print(
                    f"Warning: row {row_num} Likelihood={likelihood} outside 1-5 range",
                    file=sys.stderr,
                )
            if not (1 <= impact <= 5):
                print(
                    f"Warning: row {row_num} Impact={impact} outside 1-5 range",
                    file=sys.stderr,
                )

            score = likelihood * impact
            threats.append(
                {
                    "ID": row["ID"].strip(),
                    "Likelihood": likelihood,
                    "Impact": impact,
                    "Risk Score": score,
                    "Priority": get_priority(score),
                }
            )

    return threats


def sort_threats(threats: list[dict]) -> list[dict]:
    """Sort threats by Risk Score descending, then by ID."""
    priority_order = {"Critical": 0, "High": 1, "Medium": 2, "Low": 3}
    return sorted(
        threats,
        key=lambda t: (-t["Risk Score"], priority_order.get(t["Priority"], 99), t["ID"]),
    )


def format_table(threats: list[dict]) -> str:
    """Format threats as a plain-text table."""
    headers = ["ID", "Likelihood", "Impact", "Risk Score", "Priority"]
    widths = {h: len(h) for h in headers}

    for t in threats:
        for h in headers:
            widths[h] = max(widths[h], len(str(t[h])))

    header_line = " | ".join(h.ljust(widths[h]) for h in headers)
    separator = "-+-".join("-" * widths[h] for h in headers)
    rows = []
    for t in threats:
        rows.append(" | ".join(str(t[h]).ljust(widths[h]) for h in headers))

    return "\n".join([header_line, separator] + rows)


def format_markdown(threats: list[dict]) -> str:
    """Format threats as a Markdown table."""
    headers = ["ID", "Likelihood", "Impact", "Risk Score", "Priority"]
    header_line = "| " + " | ".join(headers) + " |"
    separator = "| " + " | ".join("---" for _ in headers) + " |"
    rows = []
    for t in threats:
        row = "| " + " | ".join(str(t[h]) for h in headers) + " |"
        rows.append(row)

    return "\n".join([header_line, separator] + rows)


def format_csv_output(threats: list[dict]) -> str:
    """Format threats as CSV."""
    headers = ["ID", "Likelihood", "Impact", "Risk Score", "Priority"]
    lines = [",".join(headers)]
    for t in threats:
        lines.append(",".join(str(t[h]) for h in headers))
    return "\n".join(lines)


def print_summary(threats: list[dict]) -> None:
    """Print a summary of threat counts by priority."""
    counts = {"Critical": 0, "High": 0, "Medium": 0, "Low": 0}
    for t in threats:
        counts[t["Priority"]] = counts.get(t["Priority"], 0) + 1

    print("\nSummary:")
    for priority in ["Critical", "High", "Medium", "Low"]:
        count = counts[priority]
        if count > 0:
            print(f"  {priority}: {count}")
    print(f"  Total: {len(threats)}")


def main():
    parser = argparse.ArgumentParser(
        description="Score and prioritize threats from a CSV file."
    )
    parser.add_argument("input", help="Path to input CSV (columns: ID, Likelihood, Impact)")
    parser.add_argument(
        "--output", "-o", help="Path to write scored output (default: stdout)"
    )
    parser.add_argument(
        "--format",
        "-f",
        choices=["table", "markdown", "csv"],
        default="table",
        help="Output format (default: table)",
    )

    args = parser.parse_args()

    threats = read_threats(args.input)

    if not threats:
        print("No threats found in input file.", file=sys.stderr)
        sys.exit(1)

    sorted_threats = sort_threats(threats)

    if args.format == "markdown":
        output = format_markdown(sorted_threats)
    elif args.format == "csv":
        output = format_csv_output(sorted_threats)
    else:
        output = format_table(sorted_threats)

    if args.output:
        Path(args.output).write_text(output + "\n", encoding="utf-8")
        print(f"Scored threats written to {args.output}")
    else:
        print(output)

    if args.format != "csv":
        print_summary(sorted_threats)


if __name__ == "__main__":
    main()
