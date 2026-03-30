#!/usr/bin/env python3
"""
A/B Test Sample Size Calculator

Computes per-variant sample sizes for a two-proportion z-test and estimates
experiment runtime based on daily traffic.

Usage:
    python sample-size-calculator.py \
        --baseline 0.032 \
        --mde 0.005 \
        --alpha 0.05 \
        --power 0.80 \
        --daily-traffic 4200

    python sample-size-calculator.py \
        --baseline 0.032 \
        --mde-relative 0.15 \
        --alpha 0.05 \
        --power 0.80 \
        --daily-traffic 4200 \
        --variants 3
"""

import argparse
import math
import sys

try:
    from statsmodels.stats.power import NormalIndPower
    from statsmodels.stats.proportion import proportion_effectsize
except ImportError:
    print("Required package: statsmodels")
    print("Install with: pip install statsmodels")
    sys.exit(1)


def compute_sample_size(baseline_rate, mde_absolute, alpha, power):
    """
    Compute per-variant sample size for a two-proportion z-test.

    Parameters
    ----------
    baseline_rate : float
        Current conversion rate (e.g., 0.032 for 3.2%).
    mde_absolute : float
        Minimum detectable effect in absolute terms (e.g., 0.005 for +0.5pp).
    alpha : float
        Significance level (two-sided).
    power : float
        Statistical power (1 - beta).

    Returns
    -------
    int
        Required sample size per variant (rounded up).
    """
    treatment_rate = baseline_rate + mde_absolute
    effect_size = proportion_effectsize(treatment_rate, baseline_rate)
    analysis = NormalIndPower()
    n = analysis.solve_power(
        effect_size=abs(effect_size),
        alpha=alpha,
        power=power,
        alternative="two-sided",
    )
    return math.ceil(n)


def estimate_runtime(sample_per_variant, num_variants, daily_traffic):
    """
    Estimate experiment runtime in days.

    Parameters
    ----------
    sample_per_variant : int
        Required sample size per variant.
    num_variants : int
        Total number of variants (including control).
    daily_traffic : int
        Daily eligible traffic (users entering the experiment).

    Returns
    -------
    dict
        Runtime estimates.
    """
    total_sample = sample_per_variant * num_variants
    traffic_per_variant = daily_traffic / num_variants
    raw_days = sample_per_variant / traffic_per_variant
    full_weeks = math.ceil(raw_days / 7)
    recommended_days = full_weeks * 7

    return {
        "total_sample": total_sample,
        "raw_days": math.ceil(raw_days),
        "full_weeks": full_weeks,
        "recommended_days": recommended_days,
        "minimum_days": max(recommended_days, 14),  # at least 2 weeks for seasonality
    }


def main():
    parser = argparse.ArgumentParser(
        description="A/B test sample size calculator using statsmodels."
    )
    parser.add_argument(
        "--baseline", type=float, required=True,
        help="Baseline conversion rate (e.g., 0.032 for 3.2%%)"
    )

    mde_group = parser.add_mutually_exclusive_group(required=True)
    mde_group.add_argument(
        "--mde", type=float,
        help="Absolute MDE (e.g., 0.005 for +0.5pp)"
    )
    mde_group.add_argument(
        "--mde-relative", type=float,
        help="Relative MDE (e.g., 0.15 for +15%% relative lift)"
    )

    parser.add_argument("--alpha", type=float, default=0.05, help="Significance level (default: 0.05)")
    parser.add_argument("--power", type=float, default=0.80, help="Statistical power (default: 0.80)")
    parser.add_argument("--daily-traffic", type=int, default=None, help="Daily eligible traffic for runtime estimate")
    parser.add_argument("--variants", type=int, default=2, help="Total variants including control (default: 2)")

    args = parser.parse_args()

    # Resolve absolute MDE
    if args.mde is not None:
        mde_absolute = args.mde
    else:
        mde_absolute = args.baseline * args.mde_relative

    treatment_rate = args.baseline + mde_absolute

    # Compute sample size
    n_per_variant = compute_sample_size(args.baseline, mde_absolute, args.alpha, args.power)

    # Print results
    print("=" * 55)
    print("  A/B TEST SAMPLE SIZE CALCULATION")
    print("=" * 55)
    print()
    print(f"  Baseline rate:            {args.baseline:.4f} ({args.baseline*100:.2f}%)")
    print(f"  Treatment rate (target):  {treatment_rate:.4f} ({treatment_rate*100:.2f}%)")
    print(f"  MDE (absolute):           {mde_absolute:.4f} ({mde_absolute*100:.2f}pp)")
    print(f"  MDE (relative):           {mde_absolute/args.baseline*100:.1f}%")
    print(f"  Significance (alpha):     {args.alpha} (two-sided)")
    print(f"  Power (1 - beta):         {args.power}")
    print(f"  Number of variants:       {args.variants}")
    print()
    print(f"  Sample size per variant:  {n_per_variant:,}")
    print(f"  Total sample needed:      {n_per_variant * args.variants:,}")
    print()

    if args.daily_traffic:
        rt = estimate_runtime(n_per_variant, args.variants, args.daily_traffic)
        print("-" * 55)
        print("  RUNTIME ESTIMATE")
        print("-" * 55)
        print()
        print(f"  Daily eligible traffic:   {args.daily_traffic:,}")
        print(f"  Raw days to fill:         {rt['raw_days']} days")
        print(f"  Rounded to full weeks:    {rt['full_weeks']} weeks ({rt['recommended_days']} days)")
        print(f"  Recommended minimum:      {rt['minimum_days']} days (captures weekly seasonality)")
        print()

        if rt["minimum_days"] > 28:
            print("  WARNING: Runtime exceeds 4 weeks. Consider:")
            print("    - Increasing the MDE (detect a larger effect)")
            print("    - Reducing the number of variants")
            print("    - Increasing eligible traffic (broader targeting)")
            print()

    # Bonferroni note for multi-variant
    if args.variants > 2:
        adjusted_alpha = args.alpha / (args.variants - 1)
        print("-" * 55)
        print("  MULTIPLE COMPARISONS NOTE")
        print("-" * 55)
        print()
        print(f"  With {args.variants} variants ({args.variants - 1} comparisons vs. control),")
        print(f"  apply Bonferroni correction: alpha = {args.alpha} / {args.variants - 1} = {adjusted_alpha:.4f}")
        print(f"  Re-run with --alpha {adjusted_alpha:.4f} for corrected sample sizes.")
        print()

    print("=" * 55)


if __name__ == "__main__":
    main()
