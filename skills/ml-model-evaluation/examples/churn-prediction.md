# Model Evaluation — Customer Churn Predictor, StreamVault

## Problem Definition

**Business objective:** Identify subscribers likely to cancel within 30 days so the retention team can intervene with targeted offers. Current rule-based system (usage drop >50%) achieves 61% precision at 44% recall.

**Cost of errors:** False negative (missed churn) costs ~$480 in lost annual revenue. False positive (unnecessary outreach) costs ~$8 per call.

## Success Metrics

| | Metric | Target | Rationale |
|---|---|---|---|
| Primary | Recall | > 70% | Missed churn costs 60x more than false outreach |
| Secondary | Precision at 70% recall | > 55% | Keep volume manageable for 4-person retention team |
| Business | Net saves per month | > 120 | Currently ~55 saves/month with rule-based approach |

## Data & Splitting

**Dataset:** 214,000 subscriber-months (Jan 2024 - Jun 2025), 34 features (usage, account, engagement), 8.3% positive class. Temporal split (required -- churn is seasonal):

| Split | Period | Rows | Churn Rate |
|-------|--------|------|-----------|
| Train | Jan - Dec 2024 | 142,800 | 8.1% |
| Validation | Jan - Mar 2025 | 35,600 | 8.4% |
| Test | Apr - Jun 2025 | 35,600 | 8.6% |

## Model Comparison (Validation Set)

| Model | AUC-ROC | Precision @70% Recall | Latency | Training |
|-------|---------|----------------------|---------|----------|
| Logistic Regression | 0.79 | 0.48 | 0.3ms | 12s |
| Random Forest | 0.83 | 0.56 | 1.2ms | 45s |
| XGBoost | 0.87 | 0.63 | 0.8ms | 3 min |
| LightGBM | 0.86 | 0.61 | 0.6ms | 2 min |
| Rule-based (current) | 0.68 | 0.61* | — | — |

**Selected: XGBoost.** Highest AUC and precision at target recall. Test set results: AUC 0.85, precision 0.59 at 72% recall. Slight validation-to-test degradation (0.87 to 0.85) is within expected range for temporal shift.

## Error Analysis

**False negatives:** Long-tenure users (>24mo) who churn abruptly after price increases -- no gradual usage decline to detect (23% of FNs). Annual plan users who disengage mid-cycle but cancel at renewal (18% of FNs).

**False positives:** Seasonal users whose low-activity periods mimic churn signals (31% of FPs). Users who contacted support about billing but resolved the issue (14% of FPs).

## Segment Performance

| Segment | Recall | Precision @70% | Gap |
|---------|--------|----------------|-----|
| Monthly plan | 74% | 0.62 | — |
| Annual plan | 58% | 0.41 | Under-served |
| Tenure < 6mo | 78% | 0.67 | — |
| Tenure > 24mo | 61% | 0.44 | Under-served |
| International users | 68% | 0.55 | 5-pt TPR gap vs. US |

Annual-plan and long-tenure segments rely on usage-decline features that manifest differently for these groups. International TPR gap traced to timezone and connectivity differences in usage features.

## Production Readiness

| Criterion | Status | Notes |
|-----------|--------|-------|
| Primary metric | PASS | 72% recall exceeds 70% target |
| Precision | PASS | 59% at target recall (target >55%) |
| Latency | PASS | Full 214K-user batch in <3 min |
| Bias assessment | CONDITIONAL | International TPR gap flagged; monitor, fix in v2 |
| Monitoring | DEFINED | Weekly AUC on rolling window; alert if <0.80 |
| Fallback | DEFINED | Revert to rules if AUC <0.78 for 2 consecutive weeks |
| A/B test | DEFINED | 50/50 split vs. rule-based, measure save rate over 8 weeks |

**Recommendation:** Approve for A/B test. Schedule v2 feature work for annual-plan and long-tenure blind spots.
