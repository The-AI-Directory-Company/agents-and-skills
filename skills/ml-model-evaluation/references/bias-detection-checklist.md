# Bias Detection Checklist

## Core Fairness Definitions

### 1. Demographic Parity (Statistical Parity)

**Definition:** The probability of a positive prediction is the same across all protected groups.

```
P(Y_hat = 1 | Group = A) = P(Y_hat = 1 | Group = B)
```

**When to use:** When the selection rate itself must be equal (e.g., hiring, loan approvals where legal or policy requirements mandate equal opportunity of selection).

**Limitation:** Does not account for differences in base rates. If Group A has a genuinely higher positive rate than Group B, enforcing demographic parity may reduce overall accuracy.

**Threshold guidance:**
- Acceptable disparity: < 5 percentage points difference in positive prediction rate across groups.
- Four-fifths rule (EEOC guideline): The selection rate for any group should be at least 80% of the rate for the group with the highest selection rate.
- Example: If Group A has a 50% positive prediction rate, Group B must be at least 40%.

---

### 2. Equal Opportunity (Equalized True Positive Rate)

**Definition:** The true positive rate (recall) is the same across all protected groups.

```
P(Y_hat = 1 | Y = 1, Group = A) = P(Y_hat = 1 | Y = 1, Group = B)
```

**When to use:** When it matters that qualified individuals are equally likely to be correctly identified regardless of group (e.g., disease detection, fraud detection, recidivism prediction).

**Limitation:** Only considers the positive class. A model can satisfy equal opportunity while having vastly different false positive rates across groups.

**Threshold guidance:**
- Acceptable disparity: < 5 percentage points difference in TPR across groups.
- If one group's TPR is below 80% of the highest group's TPR, investigate data representation and feature encoding.
- Always pair with equalized false positive rate analysis for a complete picture.

---

### 3. Equalized Odds

**Definition:** Both the true positive rate AND false positive rate are equal across groups.

```
P(Y_hat = 1 | Y = y, Group = A) = P(Y_hat = 1 | Y = y, Group = B)  for y in {0, 1}
```

**When to use:** When both types of errors have significant consequences across groups (e.g., criminal justice, credit scoring).

**Limitation:** Strictly harder to satisfy than equal opportunity alone. May require accuracy tradeoffs.

**Threshold guidance:**
- TPR disparity < 5pp AND FPR disparity < 5pp across groups.
- If one constraint can be relaxed, decide based on cost asymmetry: relax FPR constraint if false positives are cheap, relax TPR constraint if false negatives are cheap.

---

### 4. Calibration (Sufficiency)

**Definition:** Among individuals assigned a predicted probability p, the actual positive rate is p, and this holds across all groups.

```
P(Y = 1 | Score = s, Group = A) = P(Y = 1 | Score = s, Group = B) = s
```

**When to use:** When the model outputs probabilities used for downstream decisions (e.g., risk scores, insurance pricing, medical diagnosis confidence).

**Limitation:** A calibrated model can still have different selection rates across groups. Calibration and demographic parity are generally incompatible when base rates differ (Chouldechova's impossibility theorem).

**Threshold guidance:**
- Plot calibration curves per group. For each decile bin, the predicted probability and observed frequency should differ by < 5 percentage points.
- Use the Hosmer-Lemeshow test or Expected Calibration Error (ECE) per group. ECE > 0.05 for any group warrants investigation.

---

## Evaluation Procedure

### Step 1: Identify protected attributes

List all attributes that define protected groups in your context. Common examples:
- Age, gender, race/ethnicity, disability status
- Geographic region (as proxy for socioeconomic status)
- Language, nationality

If protected attributes are not in the dataset, check for proxies: ZIP code correlates with race, name correlates with gender/ethnicity, school correlates with socioeconomic status.

### Step 2: Compute group-level metrics

For each protected group, compute:

| Metric | Group A | Group B | Group C | Disparity |
|--------|---------|---------|---------|-----------|
| Positive prediction rate | | | | Max - Min |
| True positive rate (recall) | | | | Max - Min |
| False positive rate | | | | Max - Min |
| Precision | | | | Max - Min |
| Calibration (ECE) | | | | Max across groups |

### Step 3: Apply thresholds

Flag any metric where:
- Disparity exceeds 5 percentage points, OR
- The four-fifths rule is violated (any group < 80% of the best group), OR
- Calibration ECE > 0.05 for any group

### Step 4: Investigate root causes

For flagged disparities:
1. **Data representation:** Is the underperforming group underrepresented in training data?
2. **Label quality:** Are labels equally reliable across groups (e.g., differential reporting rates)?
3. **Feature encoding:** Do features encode group membership directly or through proxies?
4. **Model architecture:** Does the model have sufficient capacity to learn group-specific patterns?

### Step 5: Document and decide

Record:
- Which fairness criteria were evaluated and why
- Which disparities were found and their magnitude
- Root cause analysis for each disparity
- Decision: accept the disparity (with justification), mitigate (with method), or reject the model
- Any legal or regulatory requirements that apply

---

## Impossibility Constraints

It is mathematically impossible to simultaneously satisfy demographic parity, equal opportunity, and calibration when base rates differ across groups (Chouldechova 2017, Kleinberg et al. 2016).

**Practical implication:** You must choose which fairness criterion to prioritize based on the application context. Document the choice and its consequences explicitly in the evaluation report.

| Application | Prioritize | Rationale |
|-------------|-----------|-----------|
| Hiring / admissions | Demographic parity or four-fifths rule | Legal requirements (EEOC) |
| Medical diagnosis | Equal opportunity (TPR parity) | Missing a disease in one group is unacceptable |
| Credit scoring | Calibration | Predicted risk must be accurate for pricing |
| Criminal justice | Equalized odds | Both FP and FN have severe consequences |
