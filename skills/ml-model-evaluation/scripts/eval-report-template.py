#!/usr/bin/env python3
"""
ML Model Evaluation Report Generator

Takes model predictions + ground truth from a CSV and generates a comparison
table with accuracy, precision, recall, F1, and AUC broken down by segment.

Usage:
    python eval-report-template.py --input predictions.csv \
        --label-col label --pred-col prediction \
        --segment-col region \
        [--prob-col probability] \
        [--output report.md]

CSV format:
    Must contain at minimum a ground-truth label column and a prediction column.
    Optionally include a probability column (for AUC) and a segment column
    (for per-segment breakdown).

Example CSV:
    label,prediction,probability,region
    1,1,0.92,US
    0,0,0.15,EU
    1,0,0.38,US
    0,1,0.61,EU
"""

import argparse
import sys
from pathlib import Path

try:
    import pandas as pd
    from sklearn.metrics import (
        accuracy_score,
        precision_score,
        recall_score,
        f1_score,
        roc_auc_score,
        confusion_matrix,
    )
except ImportError:
    print("Required packages: pandas, scikit-learn")
    print("Install with: pip install pandas scikit-learn")
    sys.exit(1)


def compute_metrics(y_true, y_pred, y_prob=None):
    """Compute classification metrics for a single segment."""
    metrics = {
        "n": len(y_true),
        "positives": int(y_true.sum()),
        "accuracy": accuracy_score(y_true, y_pred),
        "precision": precision_score(y_true, y_pred, zero_division=0),
        "recall": recall_score(y_true, y_pred, zero_division=0),
        "f1": f1_score(y_true, y_pred, zero_division=0),
    }

    if y_prob is not None and len(y_true.unique()) > 1:
        try:
            metrics["auc"] = roc_auc_score(y_true, y_prob)
        except ValueError:
            metrics["auc"] = None
    else:
        metrics["auc"] = None

    cm = confusion_matrix(y_true, y_pred, labels=[0, 1])
    metrics["tn"] = int(cm[0, 0])
    metrics["fp"] = int(cm[0, 1])
    metrics["fn"] = int(cm[1, 0])
    metrics["tp"] = int(cm[1, 1])

    return metrics


def format_pct(value):
    """Format a float as a percentage string."""
    if value is None:
        return "N/A"
    return f"{value:.3f}"


def generate_report(df, label_col, pred_col, prob_col, segment_col):
    """Generate the full evaluation report as a markdown string."""
    lines = []
    lines.append("# Model Evaluation Report\n")

    # --- Overall metrics ---
    y_true = df[label_col]
    y_pred = df[pred_col]
    y_prob = df[prob_col] if prob_col and prob_col in df.columns else None

    overall = compute_metrics(y_true, y_pred, y_prob)

    lines.append("## Overall Performance\n")
    lines.append(f"- **Total samples:** {overall['n']}")
    lines.append(f"- **Positive samples:** {overall['positives']} ({overall['positives']/overall['n']*100:.1f}%)")
    lines.append(f"- **Accuracy:** {format_pct(overall['accuracy'])}")
    lines.append(f"- **Precision:** {format_pct(overall['precision'])}")
    lines.append(f"- **Recall:** {format_pct(overall['recall'])}")
    lines.append(f"- **F1 Score:** {format_pct(overall['f1'])}")
    lines.append(f"- **AUC-ROC:** {format_pct(overall['auc'])}")
    lines.append("")

    lines.append("### Confusion Matrix\n")
    lines.append("|  | Predicted 0 | Predicted 1 |")
    lines.append("|--|------------|------------|")
    lines.append(f"| **Actual 0** | {overall['tn']} (TN) | {overall['fp']} (FP) |")
    lines.append(f"| **Actual 1** | {overall['fn']} (FN) | {overall['tp']} (TP) |")
    lines.append("")

    # --- Per-segment breakdown ---
    if segment_col and segment_col in df.columns:
        lines.append("## Performance by Segment\n")

        segments = sorted(df[segment_col].unique())
        header = "| Segment | N | Pos Rate | Accuracy | Precision | Recall | F1 | AUC |"
        sep = "|---------|---|----------|----------|-----------|--------|----|----|"
        lines.append(header)
        lines.append(sep)

        segment_metrics = []
        for seg in segments:
            mask = df[segment_col] == seg
            seg_true = df.loc[mask, label_col]
            seg_pred = df.loc[mask, pred_col]
            seg_prob = df.loc[mask, prob_col] if prob_col and prob_col in df.columns else None

            m = compute_metrics(seg_true, seg_pred, seg_prob)
            segment_metrics.append((seg, m))

            pos_rate = f"{m['positives']/m['n']*100:.1f}%"
            lines.append(
                f"| {seg} | {m['n']} | {pos_rate} | {format_pct(m['accuracy'])} "
                f"| {format_pct(m['precision'])} | {format_pct(m['recall'])} "
                f"| {format_pct(m['f1'])} | {format_pct(m['auc'])} |"
            )

        lines.append("")

        # --- Flag segments with significant performance gaps ---
        if len(segment_metrics) > 1:
            f1_values = [m["f1"] for _, m in segment_metrics]
            f1_range = max(f1_values) - min(f1_values)

            if f1_range > 0.10:
                lines.append("### Segment Performance Alerts\n")
                best_seg = max(segment_metrics, key=lambda x: x[1]["f1"])
                worst_seg = min(segment_metrics, key=lambda x: x[1]["f1"])
                lines.append(
                    f"- **F1 spread across segments:** {f1_range:.3f} "
                    f"(best: {best_seg[0]} = {best_seg[1]['f1']:.3f}, "
                    f"worst: {worst_seg[0]} = {worst_seg[1]['f1']:.3f})"
                )
                lines.append(
                    "- Performance varies >10% across segments. "
                    "Investigate data representation and feature quality per segment."
                )
                lines.append("")

    # --- Checklist ---
    lines.append("## Evaluation Checklist\n")
    lines.append("- [ ] Business objective mapped to primary metric")
    lines.append("- [ ] Test set was held out from all model selection decisions")
    lines.append("- [ ] Simple baseline included for comparison")
    lines.append("- [ ] Error analysis reviewed specific failure cases")
    lines.append("- [ ] Bias detection run across protected attributes")
    lines.append("- [ ] Production readiness verified (latency, monitoring, fallback)")
    lines.append("")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Generate an ML model evaluation report from predictions CSV."
    )
    parser.add_argument("--input", required=True, help="Path to predictions CSV")
    parser.add_argument("--label-col", required=True, help="Ground truth label column name")
    parser.add_argument("--pred-col", required=True, help="Prediction column name")
    parser.add_argument("--prob-col", default=None, help="Probability column name (for AUC)")
    parser.add_argument("--segment-col", default=None, help="Segment column for breakdown")
    parser.add_argument("--output", default=None, help="Output file path (default: stdout)")

    args = parser.parse_args()

    input_path = Path(args.input)
    if not input_path.exists():
        print(f"Error: Input file not found: {args.input}", file=sys.stderr)
        sys.exit(1)

    df = pd.read_csv(input_path)

    for col_name, col_val in [("label", args.label_col), ("prediction", args.pred_col)]:
        if col_val not in df.columns:
            print(f"Error: {col_name} column '{col_val}' not found in CSV.", file=sys.stderr)
            print(f"Available columns: {list(df.columns)}", file=sys.stderr)
            sys.exit(1)

    report = generate_report(df, args.label_col, args.pred_col, args.prob_col, args.segment_col)

    if args.output:
        Path(args.output).write_text(report)
        print(f"Report written to {args.output}")
    else:
        print(report)


if __name__ == "__main__":
    main()
