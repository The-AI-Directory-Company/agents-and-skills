---
name: ml-model-evaluation
description: Evaluate machine learning models rigorously — with train/test splits, cross-validation, business metric alignment, bias detection, and production readiness assessment.
metadata:
  displayName: "ML Model Evaluation"
  categories: ["data"]
  tags: ["machine-learning", "evaluation", "metrics", "bias", "model-selection"]
  worksWellWithAgents: ["data-scientist", "ml-engineer", "product-analyst"]
  worksWellWithSkills: ["experiment-design", "metrics-framework"]
---

# ML Model Evaluation

## Before you start

Gather the following from the user. If anything is missing, ask before proceeding:

1. **What problem is the model solving?** — Classification, regression, ranking, recommendation, generation
2. **What is the business objective?** — The real-world outcome (reduce churn, detect fraud, recommend products)
3. **What data is available?** — Dataset size, feature count, label quality, class balance, time range
4. **What are the constraints?** — Latency, model size, interpretability needs, regulatory obligations
5. **What is the baseline?** — Current system performance (rule-based, human, or previous model)
6. **What is the cost of errors?** — False positive vs false negative impact in business terms

## Evaluation template

### 1. Define Success Metrics

Map business objectives to technical metrics. Never evaluate on technical metrics alone.

```
Business Objective:     Detect fraudulent transactions before settlement
Primary Metric:         Precision at 95% recall
Secondary Metrics:      AUC-ROC, F1 score, false positive rate
Business Constraint:    <50ms inference latency
Baseline Performance:   Rule-based system: 72% precision at 95% recall
Target Performance:     >85% precision at 95% recall
```

Metric selection rules:
- **Classification**: Use precision/recall/F1 for imbalanced classes. Accuracy is misleading when 98% of data is one class.
- **Regression**: MAE for outlier-tolerant, RMSE when large errors are disproportionately costly.
- **Ranking**: NDCG/MAP when order matters, precision@k when only top results matter.
- Always include a business metric: revenue impact, time saved, error cost reduction.

### 2. Data Splitting Strategy

**Random split** — Default for i.i.d. data: Train 70% / Validation 15% / Test 15%.

**Temporal split** — Required for time-dependent data: Train before T1 / Validation T1-T2 / Test after T2.

**Stratified split** — Required for imbalanced classification: maintain class proportions across splits.

**Group split** — Required when one entity has multiple samples: split by entity ID, not by row.

Critical rules:
- Never use test data for any decision — tuning, feature selection, or threshold setting
- For small datasets (<5000 samples), use k-fold cross-validation instead of a fixed split
- Always check for data leakage: features encoding the label, future data in training

### 3. Model Comparison

Evaluate all candidates on the same validation set with identical preprocessing:

| Model | Primary Metric | Latency | Model Size | Training Time |
|-------|---------------|---------|------------|---------------|
| Logistic Regression | 0.78 | 2ms | 1MB | 30s |
| XGBoost | 0.86 | 8ms | 50MB | 10min |
| Neural Net | 0.85 | 25ms | 500MB | 2hr |

Always include a simple baseline. If a complex model does not meaningfully beat a simple one, choose the simpler model.

### 4. Error Analysis

Do not stop at aggregate metrics. Examine where the model fails:

- **Confusion matrix**: Inspect false positive and false negative examples manually
- **Segment analysis**: Break down performance by key dimensions (user type, region, value tier). If performance varies >10% across segments, investigate.
- **Error distribution**: For regression, plot residuals — are errors uniform or concentrated?

### 5. Bias Detection

Check for disparities across protected groups:

- **Demographic parity**: Does positive prediction rate differ across groups?
- **Equal opportunity**: Does true positive rate differ across groups?
- **Calibration**: Does a predicted 80% probability mean 80% actual positive rate for all groups?

If disparities exceed acceptable thresholds, investigate data representation, feature encoding, and model architecture.

### 6. Production Readiness

Verify before deployment: meets primary metric target, meets latency constraint, model size within limits, bias assessment passed, monitoring plan defined (prediction drift, feature drift, business metric tracking), fallback strategy documented, A/B test plan prepared, data pipeline validated, model versioning in place.

## Quality checklist

Before delivering a model evaluation, verify:

- [ ] Business objective is mapped to technical metrics with a stated target
- [ ] Data split strategy matches data characteristics (temporal, imbalanced, grouped)
- [ ] Test set was never used for model selection or tuning
- [ ] At least one simple baseline is included for comparison
- [ ] Error analysis examines specific failure cases, not just aggregates
- [ ] Performance is broken down by relevant segments
- [ ] Bias detection covers protected attributes and business segments
- [ ] Production readiness includes latency, monitoring, and fallback

## Common mistakes

- **Evaluating on accuracy alone.** A model predicting "not fraud" for everything achieves 99.5% accuracy on a 0.5% fraud dataset. Use precision/recall for imbalanced problems.
- **Leaking test data.** Using the test set for feature selection or tuning inflates results and breaks the generalization guarantee.
- **Ignoring the simple baseline.** A logistic regression at 90% in 30 seconds often beats a deep learning model at 92% after two weeks of engineering.
- **Reporting only aggregate metrics.** 90% overall accuracy that drops to 50% on a critical segment is not a 90%-accurate model for those users.
- **Skipping the cost analysis.** False positives and false negatives rarely cost the same. The evaluation must reflect the asymmetry.
- **No production monitoring plan.** Models degrade as distributions shift. An evaluation without monitoring is incomplete.
