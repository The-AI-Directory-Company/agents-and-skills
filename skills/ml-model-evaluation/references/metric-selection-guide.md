# Metric Selection Guide

## Selection Matrix by Problem Type

### Classification

| Scenario | Primary Metric | Secondary Metrics | Avoid |
|----------|---------------|-------------------|-------|
| Balanced classes | F1 (macro) | Accuracy, AUC-ROC | — |
| Imbalanced classes (rare positive) | Precision-Recall AUC | F1, Recall@k | Accuracy |
| Imbalanced + high FP cost (spam, fraud alerts) | Precision at fixed recall | F1, FPR | Accuracy, AUC-ROC alone |
| Imbalanced + high FN cost (disease, fraud loss) | Recall at fixed precision | F1, FNR | Accuracy |
| Multi-class | Macro F1 | Per-class F1, confusion matrix | Micro F1 (hides minority class failures) |
| Multi-label | Subset accuracy, Hamming loss | Per-label AUC | Single-label metrics |
| Probabilistic output needed | Log loss (cross-entropy) | Brier score, calibration curve | Hard-label metrics alone |

### Regression

| Scenario | Primary Metric | Secondary Metrics | Avoid |
|----------|---------------|-------------------|-------|
| General purpose | MAE | RMSE, R-squared | R-squared alone |
| Large errors are costly | RMSE | MAE, max error | MAE alone (masks outlier errors) |
| Outlier-tolerant | MAE or Median AE | RMSE (for monitoring) | RMSE as primary |
| Relative errors matter (revenue, prices) | MAPE or sMAPE | MAE | MAPE when actuals near zero |
| Heteroscedastic data | Weighted MAE or quantile loss | Prediction intervals | Unweighted metrics |

### Ranking

| Scenario | Primary Metric | Secondary Metrics | Avoid |
|----------|---------------|-------------------|-------|
| Full ranking quality | NDCG | MAP, MRR | Precision@k alone |
| Only top results matter | Precision@k, NDCG@k | Recall@k, MRR | Full-list metrics |
| Single best result matters | MRR (Mean Reciprocal Rank) | Hit Rate@k | NDCG (over-weights deep ranks) |
| Pairwise correctness | Kendall tau, concordance index | AUC | — |

## Imbalanced Class Guidance

### When to suspect imbalance is distorting metrics

- Accuracy > 90% but the model predicts the majority class almost exclusively
- AUC-ROC looks strong (> 0.90) but Precision-Recall AUC is weak (< 0.50)
- Confusion matrix shows near-zero true positives for the minority class

### Recommended approach

1. **Always report the class distribution** in train, validation, and test sets.
2. **Use Precision-Recall AUC** as the primary discriminative metric when the positive class is < 10% of the data.
3. **Set the classification threshold using the validation set**, not the default 0.5. Choose the threshold that optimizes the business-relevant tradeoff (e.g., maximize F1, or fix recall at 95% and report resulting precision).
4. **Do not resample the test set.** Oversampling/undersampling is a training strategy. The test set must reflect the true distribution.
5. **Report metrics at multiple thresholds** using the precision-recall curve, not a single point.

## AUC-ROC vs Precision-Recall AUC

| Property | AUC-ROC | PR AUC |
|----------|---------|--------|
| Sensitive to class imbalance | No --- can look good even when minority class performance is poor | Yes --- directly reflects minority class prediction quality |
| Best for | Balanced datasets, threshold-independent comparison | Imbalanced datasets, when positive class is rare and important |
| Interpretation | Probability that a random positive ranks above a random negative | Area under precision-recall tradeoff curve |
| Weakness | Flatters models on imbalanced data because TNR dominates | Harder to interpret; baseline depends on prevalence |

### Decision rule

- **Use AUC-ROC** when classes are roughly balanced (positive rate > 20%) or when you need a threshold-independent comparison across models.
- **Use PR AUC** when the positive class is rare (< 10%) and the cost of missing positives is high (fraud, disease, defect detection).
- **Report both** when stakeholders need the full picture --- but make clear which one drives the model selection decision.

## Business Metric Alignment

Technical metrics alone are insufficient. Always include at least one metric that maps to a business outcome:

| Business Goal | Technical Proxy | Business Metric |
|--------------|----------------|-----------------|
| Reduce fraud losses | Precision at 95% recall | Dollar amount of fraud caught vs. false block cost |
| Improve recommendations | NDCG@10 | Click-through rate, revenue per session |
| Speed up support triage | Classification accuracy | Average resolution time, escalation rate |
| Detect manufacturing defects | Recall at 99% | Defective units shipped, inspection cost |

If the technical metric improves but the business metric does not, the model improvement is not real.
