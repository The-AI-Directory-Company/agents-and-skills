#!/usr/bin/env python3
"""
Runway Model

Takes monthly revenue and cost data, prints quarter-by-quarter cash flow
with runway-in-months. Supports bear, base, and bull scenarios.

Usage:
    python runway-model.py \
        --starting-cash 500000 \
        --monthly-revenue 20000 \
        --monthly-costs 65000 \
        --revenue-growth-pct 8 \
        --cost-growth-pct 2 \
        --months 36

    For scenario comparison:
    python runway-model.py \
        --starting-cash 500000 \
        --monthly-revenue 20000 \
        --monthly-costs 65000 \
        --scenarios
"""

import argparse
import math
import sys


def project_cash_flow(
    starting_cash: float,
    monthly_revenue: float,
    monthly_costs: float,
    revenue_growth_pct: float,
    cost_growth_pct: float,
    months: int,
) -> list[dict]:
    """Project month-by-month cash flow and return quarterly summaries."""
    cash = starting_cash
    revenue = monthly_revenue
    costs = monthly_costs
    rev_growth = revenue_growth_pct / 100.0
    cost_growth = cost_growth_pct / 100.0

    monthly_data = []
    for m in range(1, months + 1):
        net = revenue - costs
        cash += net
        monthly_data.append({
            "month": m,
            "revenue": round(revenue, 2),
            "costs": round(costs, 2),
            "net_cash_flow": round(net, 2),
            "cumulative_cash": round(cash, 2),
        })
        revenue *= (1 + rev_growth)
        costs *= (1 + cost_growth)

    # Aggregate to quarters
    quarters = []
    for q_start in range(0, len(monthly_data), 3):
        q_months = monthly_data[q_start:q_start + 3]
        if not q_months:
            break
        q_num = (q_start // 3) + 1
        q_revenue = sum(m["revenue"] for m in q_months)
        q_costs = sum(m["costs"] for m in q_months)
        q_net = sum(m["net_cash_flow"] for m in q_months)
        q_ending_cash = q_months[-1]["cumulative_cash"]

        # Runway: months of cash remaining at current burn rate
        last_month_net = q_months[-1]["net_cash_flow"]
        if last_month_net < 0:
            runway_months = max(0, q_ending_cash / abs(last_month_net))
        else:
            runway_months = float("inf")

        quarters.append({
            "quarter": f"Q{q_num}",
            "revenue": round(q_revenue, 2),
            "costs": round(q_costs, 2),
            "net_cash_flow": round(q_net, 2),
            "ending_cash": round(q_ending_cash, 2),
            "runway_months": runway_months,
            "monthly_burn": round(abs(last_month_net), 2) if last_month_net < 0 else 0,
        })

    return quarters


def format_currency(value: float) -> str:
    """Format a number as currency."""
    if abs(value) >= 1_000_000:
        return f"${value / 1_000_000:,.1f}M"
    elif abs(value) >= 1_000:
        return f"${value / 1_000:,.1f}K"
    else:
        return f"${value:,.0f}"


def format_runway(months: float) -> str:
    """Format runway months."""
    if months == float("inf"):
        return "Profitable"
    elif months <= 0:
        return "DEPLETED"
    else:
        return f"{months:.1f} months"


def print_scenario(name: str, quarters: list[dict]) -> None:
    """Print a single scenario's quarterly cash flow."""
    print(f"\n  {name}")
    print(f"  {'-' * 56}")
    print(f"  {'Quarter':<10} {'Revenue':>10} {'Costs':>10} {'Net':>10} {'Cash':>10} {'Runway':>12}")
    print(f"  {'-' * 56}")

    for q in quarters:
        runway_str = format_runway(q["runway_months"])
        warning = ""
        if q["runway_months"] != float("inf") and q["runway_months"] < 6:
            warning = " <-- CRITICAL"
        elif q["runway_months"] != float("inf") and q["runway_months"] < 12:
            warning = " <-- LOW"

        print(
            f"  {q['quarter']:<10} "
            f"{format_currency(q['revenue']):>10} "
            f"{format_currency(q['costs']):>10} "
            f"{format_currency(q['net_cash_flow']):>10} "
            f"{format_currency(q['ending_cash']):>10} "
            f"{runway_str:>12}{warning}"
        )

    print(f"  {'-' * 56}")

    # Find zero-cash quarter
    for q in quarters:
        if q["ending_cash"] <= 0:
            print(f"\n  Cash depleted in {q['quarter']}.")
            break
    else:
        last = quarters[-1]
        if last["runway_months"] == float("inf"):
            print(f"\n  Company reaches profitability. No runway concern.")
        elif last["runway_months"] < 6:
            print(f"\n  CRITICAL: Runway is {last['runway_months']:.1f} months at end of projection.")
        else:
            print(f"\n  Runway at end of projection: {last['runway_months']:.1f} months.")


def run_scenarios(starting_cash: float, monthly_revenue: float, monthly_costs: float, months: int) -> None:
    """Run bear, base, and bull scenarios with preset growth assumptions."""
    scenarios = {
        "BEAR CASE (revenue +4%/mo, costs +4%/mo)": {
            "revenue_growth_pct": 4.0,
            "cost_growth_pct": 4.0,
        },
        "BASE CASE (revenue +8%/mo, costs +2%/mo)": {
            "revenue_growth_pct": 8.0,
            "cost_growth_pct": 2.0,
        },
        "BULL CASE (revenue +12%/mo, costs +1.5%/mo)": {
            "revenue_growth_pct": 12.0,
            "cost_growth_pct": 1.5,
        },
    }

    print()
    print("=" * 64)
    print("  RUNWAY MODEL -- SCENARIO COMPARISON")
    print("=" * 64)
    print(f"\n  Starting cash:     {format_currency(starting_cash)}")
    print(f"  Monthly revenue:   {format_currency(monthly_revenue)}")
    print(f"  Monthly costs:     {format_currency(monthly_costs)}")
    print(f"  Projection:        {months} months ({months // 12} years)")

    for name, params in scenarios.items():
        quarters = project_cash_flow(
            starting_cash=starting_cash,
            monthly_revenue=monthly_revenue,
            monthly_costs=monthly_costs,
            months=months,
            **params,
        )
        print_scenario(name, quarters)

    print()
    print("=" * 64)
    print("  Note: Bear case should inform fundraising timeline.")
    print("  If bear-case runway < 6 months, begin fundraising now.")
    print("=" * 64)
    print()


def main():
    parser = argparse.ArgumentParser(
        description="Quarter-by-quarter cash flow projection with runway calculation.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Single scenario:
  python runway-model.py --starting-cash 500000 --monthly-revenue 20000 \\
      --monthly-costs 65000 --revenue-growth-pct 8 --cost-growth-pct 2 --months 36

  # Three-scenario comparison:
  python runway-model.py --starting-cash 500000 --monthly-revenue 20000 \\
      --monthly-costs 65000 --scenarios
        """,
    )
    parser.add_argument("--starting-cash", type=float, required=True, help="Current cash on hand in dollars")
    parser.add_argument("--monthly-revenue", type=float, required=True, help="Current monthly revenue in dollars")
    parser.add_argument("--monthly-costs", type=float, required=True, help="Current total monthly costs in dollars")
    parser.add_argument("--revenue-growth-pct", type=float, default=8.0, help="Monthly revenue growth rate %% (default: 8)")
    parser.add_argument("--cost-growth-pct", type=float, default=2.0, help="Monthly cost growth rate %% (default: 2)")
    parser.add_argument("--months", type=int, default=36, help="Projection horizon in months (default: 36)")
    parser.add_argument("--scenarios", action="store_true", help="Run bear/base/bull scenario comparison instead of single projection")

    args = parser.parse_args()

    if args.scenarios:
        run_scenarios(args.starting_cash, args.monthly_revenue, args.monthly_costs, args.months)
    else:
        print()
        print("=" * 64)
        print("  RUNWAY MODEL")
        print("=" * 64)
        print(f"\n  Starting cash:       {format_currency(args.starting_cash)}")
        print(f"  Monthly revenue:     {format_currency(args.monthly_revenue)}")
        print(f"  Monthly costs:       {format_currency(args.monthly_costs)}")
        print(f"  Revenue growth:      {args.revenue_growth_pct}%/month")
        print(f"  Cost growth:         {args.cost_growth_pct}%/month")
        print(f"  Projection:          {args.months} months")

        quarters = project_cash_flow(
            starting_cash=args.starting_cash,
            monthly_revenue=args.monthly_revenue,
            monthly_costs=args.monthly_costs,
            revenue_growth_pct=args.revenue_growth_pct,
            cost_growth_pct=args.cost_growth_pct,
            months=args.months,
        )
        print_scenario("PROJECTION", quarters)
        print()


if __name__ == "__main__":
    main()
