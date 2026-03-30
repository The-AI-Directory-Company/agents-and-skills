#!/usr/bin/env python3
"""
Unit Economics Calculator

Computes LTV, LTV:CAC ratio, and CAC payback period from CLI inputs.
Flags metrics against standard SaaS benchmarks.

Usage:
    python unit-economics-calculator.py --cac 340 --arpu 100 --gross-margin-pct 72 --monthly-churn-pct 3.2
"""

import argparse
import sys


BENCHMARKS = {
    "ltv_cac_ratio": {"healthy": 3.0, "strong": 5.0, "label": "LTV:CAC Ratio"},
    "cac_payback_months": {"healthy": 12, "strong": 6, "label": "CAC Payback (months)"},
    "gross_margin_pct": {"healthy": 65, "strong": 75, "label": "Gross Margin (%)"},
}


def compute_unit_economics(cac: float, arpu: float, gross_margin_pct: float, monthly_churn_pct: float) -> dict:
    """Compute core unit economics metrics."""
    if monthly_churn_pct <= 0:
        print("Error: Monthly churn must be greater than 0%. A 0% churn implies infinite LTV.")
        sys.exit(1)
    if cac <= 0:
        print("Error: CAC must be greater than 0.")
        sys.exit(1)

    gross_margin_frac = gross_margin_pct / 100.0
    monthly_churn_frac = monthly_churn_pct / 100.0

    # Gross-margin-based LTV (not revenue-based -- see SKILL.md common mistakes)
    avg_customer_lifetime_months = 1.0 / monthly_churn_frac
    monthly_gross_profit = arpu * gross_margin_frac
    ltv = monthly_gross_profit * avg_customer_lifetime_months

    ltv_cac_ratio = ltv / cac
    cac_payback_months = cac / monthly_gross_profit

    annual_churn_pct = (1 - (1 - monthly_churn_frac) ** 12) * 100

    return {
        "cac": cac,
        "arpu": arpu,
        "gross_margin_pct": gross_margin_pct,
        "monthly_churn_pct": monthly_churn_pct,
        "annual_churn_pct": round(annual_churn_pct, 1),
        "avg_lifetime_months": round(avg_customer_lifetime_months, 1),
        "monthly_gross_profit": round(monthly_gross_profit, 2),
        "ltv": round(ltv, 2),
        "ltv_cac_ratio": round(ltv_cac_ratio, 1),
        "cac_payback_months": round(cac_payback_months, 1),
    }


def flag_benchmark(label: str, value: float, healthy: float, strong: float, higher_is_better: bool = True) -> str:
    """Return a benchmark status string."""
    if higher_is_better:
        if value >= strong:
            return f"  STRONG (benchmark: >{strong})"
        elif value >= healthy:
            return f"  HEALTHY (benchmark: >{healthy})"
        else:
            return f"  WARNING -- below healthy threshold of {healthy}"
    else:
        if value <= strong:
            return f"  STRONG (benchmark: <{strong})"
        elif value <= healthy:
            return f"  HEALTHY (benchmark: <{healthy})"
        else:
            return f"  WARNING -- above healthy threshold of {healthy}"


def print_results(metrics: dict) -> None:
    """Print formatted results with benchmark flags."""
    print()
    print("=" * 60)
    print("  UNIT ECONOMICS REPORT")
    print("=" * 60)
    print()
    print("  INPUTS")
    print(f"  CAC (blended):           ${metrics['cac']:,.2f}")
    print(f"  ARPU (monthly):          ${metrics['arpu']:,.2f}")
    print(f"  Gross Margin:            {metrics['gross_margin_pct']}%")
    print(f"  Monthly Churn:           {metrics['monthly_churn_pct']}%")
    print()
    print("  DERIVED METRICS")
    print(f"  Annual Churn:            {metrics['annual_churn_pct']}%")
    print(f"  Avg Lifetime:            {metrics['avg_lifetime_months']} months")
    print(f"  Monthly Gross Profit:    ${metrics['monthly_gross_profit']:,.2f}")
    print()
    print("  KEY RESULTS")
    print(f"  LTV (gross-margin):      ${metrics['ltv']:,.2f}")
    print(flag_benchmark("LTV:CAC", metrics["ltv_cac_ratio"], 3.0, 5.0))
    print()
    print(f"  LTV:CAC Ratio:           {metrics['ltv_cac_ratio']}x")
    print(flag_benchmark("LTV:CAC", metrics["ltv_cac_ratio"], 3.0, 5.0))
    print()
    print(f"  CAC Payback:             {metrics['cac_payback_months']} months")
    print(flag_benchmark("CAC Payback", metrics["cac_payback_months"], 12, 6, higher_is_better=False))
    print()
    print(f"  Gross Margin:            {metrics['gross_margin_pct']}%")
    print(flag_benchmark("Gross Margin", metrics["gross_margin_pct"], 65, 75))
    print()
    print("=" * 60)

    # Summary verdict
    warnings = []
    if metrics["ltv_cac_ratio"] < 3.0:
        warnings.append(f"LTV:CAC ratio ({metrics['ltv_cac_ratio']}x) is below 3x -- unit economics are unsustainable")
    if metrics["cac_payback_months"] > 12:
        warnings.append(f"CAC payback ({metrics['cac_payback_months']}mo) exceeds 12 months -- cash flow risk")
    if metrics["gross_margin_pct"] < 65:
        warnings.append(f"Gross margin ({metrics['gross_margin_pct']}%) is below 65% SaaS benchmark")

    if warnings:
        print()
        print("  WARNINGS:")
        for w in warnings:
            print(f"  - {w}")
        print()
    else:
        print()
        print("  All metrics within healthy SaaS benchmarks.")
        print()


def main():
    parser = argparse.ArgumentParser(
        description="Compute SaaS unit economics: LTV, LTV:CAC, CAC payback.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python unit-economics-calculator.py --cac 340 --arpu 100 --gross-margin-pct 72 --monthly-churn-pct 3.2
  python unit-economics-calculator.py --cac 1200 --arpu 250 --gross-margin-pct 80 --monthly-churn-pct 1.5
        """,
    )
    parser.add_argument("--cac", type=float, required=True, help="Customer acquisition cost in dollars")
    parser.add_argument("--arpu", type=float, required=True, help="Average revenue per user per month in dollars")
    parser.add_argument("--gross-margin-pct", type=float, required=True, help="Gross margin percentage (e.g., 72 for 72%%)")
    parser.add_argument("--monthly-churn-pct", type=float, required=True, help="Monthly churn rate percentage (e.g., 3.2 for 3.2%%)")

    args = parser.parse_args()
    metrics = compute_unit_economics(args.cac, args.arpu, args.gross_margin_pct, args.monthly_churn_pct)
    print_results(metrics)


if __name__ == "__main__":
    main()
