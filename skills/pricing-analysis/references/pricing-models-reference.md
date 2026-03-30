# Pricing Research Models Reference

Three established methods for measuring willingness-to-pay, with procedural detail for each.

---

## 1. Van Westendorp Price Sensitivity Meter (PSM)

### What it is

A survey-based method that identifies an acceptable price range by asking four questions about price perception. Developed by Dutch economist Peter Van Westendorp in 1976.

### When to use

- Early-stage pricing for a new product or tier
- Repricing when you have access to target customers for a survey
- Quick directional signal (can run with as few as 50-100 responses)

### The four questions

Ask respondents to name a price for each:

1. **Too cheap** -- "At what price would you consider this product to be so inexpensive that you would question its quality?"
2. **Cheap / Good value** -- "At what price would you consider this product to be a bargain -- a great buy for the money?"
3. **Expensive / Getting expensive** -- "At what price would you consider this product to be starting to get expensive -- not out of the question, but you would have to think about it?"
4. **Too expensive** -- "At what price would you consider this product to be so expensive that you would not consider buying it?"

### How to analyze

1. Plot cumulative frequency distributions for all four price points on a single chart.
2. Identify four intersection points:

| Intersection | Lines Crossing | Meaning |
|---|---|---|
| **Point of Marginal Cheapness (PMC)** | "Too cheap" and "Expensive" | Below this, too many people question quality |
| **Point of Marginal Expensiveness (PME)** | "Too expensive" and "Cheap" | Above this, too many people reject the price |
| **Indifference Price Point (IDP)** | "Cheap" and "Expensive" | Equal numbers find it cheap vs. expensive |
| **Optimal Price Point (OPP)** | "Too cheap" and "Too expensive" | Minimizes the share of people with extreme reactions |

3. The **acceptable price range** is between PMC and PME.
4. The **IDP** is a strong candidate for your base price -- it is where customers are most neutral.

### Procedure

1. Define the target segment clearly (do not survey everyone).
2. Describe the product/feature with consistent framing before asking questions.
3. Collect responses (minimum 50 for directional signal, 200+ for statistical confidence).
4. Clean data: remove respondents where "too cheap" > "too expensive" (they misunderstood).
5. Plot the four cumulative distributions.
6. Read the intersection points.
7. Report the acceptable range and recommended price with confidence interval.

### Limitations

- Does not capture purchase intent -- someone may say $50 is "cheap" but still not buy.
- No competitive context -- respondents answer in a vacuum.
- Sensitive to product description -- vague framing produces vague results.
- Works best for single products, not multi-tier pricing.

---

## 2. Gabor-Granger Method

### What it is

A direct price-demand measurement that shows what percentage of respondents would buy at each price point. Produces a demand curve you can use to estimate revenue-maximizing price.

### When to use

- You have a shortlist of candidate prices (typically 4-6 price points)
- You want to estimate conversion/take-rate at each price
- Repricing an existing product where you need to quantify volume impact

### The procedure

1. **Select 4-6 price points** spanning your expected range (e.g., $29, $39, $49, $59, $79).
2. **Randomize the starting price** for each respondent to avoid anchoring bias.
3. **Ask a binary question** at each price:
   - "Would you buy [product] at [$X]/month?" (Yes / No)
4. **Sequential logic:**
   - If respondent says "Yes" at $X, show the next higher price.
   - If respondent says "No" at $X, show the next lower price.
   - Stop when you find the boundary (highest price they accept).
5. **Aggregate results** into a demand curve: % of respondents who would buy at each price.

### How to analyze

| Price Point | % Would Buy | Est. Customers (of 10,000 prospects) | Revenue |
|---|---|---|---|
| $29 | 78% | 7,800 | $226,200/mo |
| $39 | 62% | 6,200 | $241,800/mo |
| $49 | 45% | 4,500 | $220,500/mo |
| $59 | 28% | 2,800 | $165,200/mo |
| $79 | 12% | 1,200 | $94,800/mo |

The **revenue-maximizing price** is the price point where (% Would Buy x Price) is highest. In this example, $39.

### Procedure

1. Define the target segment and ensure the sample matches your buyer profile.
2. Select price points that span from "definitely below" to "definitely above" your expected price.
3. Randomize starting price for each respondent.
4. Collect at least 100 responses per segment.
5. Plot the demand curve (% would buy vs. price).
6. Compute revenue at each price point: (% buy) x (price) x (addressable population).
7. Identify the revenue-maximizing price.
8. Sensitivity check: if two price points are close in revenue, prefer the lower one (higher volume provides more data and reduces churn risk).

### Limitations

- Stated intent vs. actual behavior gap -- people overstate willingness to buy in surveys.
- Limited to pre-selected price points -- you may miss the true optimum between two tested points.
- No packaging context -- respondents evaluate price in isolation from feature bundles.
- Anchoring effects if starting price is not randomized.

---

## 3. Conjoint Analysis (Choice-Based)

### What it is

A statistical method that measures how customers trade off between product attributes (features, brand, price) to reveal the implicit value of each attribute. The most rigorous WTP method, widely used in enterprise and consumer pricing.

### When to use

- Pricing a product with multiple attributes that interact (features, service level, brand)
- Designing tier packaging (which features go in which tier)
- Need to measure the relative value of specific features to justify pricing differences
- Have budget for a larger study (typically 300+ respondents)

### Core concept

Instead of asking "What would you pay?", conjoint asks respondents to choose between product bundles that vary across attributes. Statistical analysis then decomposes choices into the implicit value (utility) of each attribute level.

### Procedure

1. **Define attributes and levels.**

   | Attribute | Levels |
   |---|---|
   | Price | $29/mo, $49/mo, $79/mo |
   | Storage | 10 GB, 50 GB, Unlimited |
   | Support | Email only, Chat + Email, Dedicated CSM |
   | Integrations | 5 integrations, 20 integrations, Unlimited |
   | SSO | No, Yes |

2. **Design choice tasks.** Use a fractional factorial design to create product profiles. Each task shows 2-4 product bundles (combinations of attribute levels) and asks: "Which would you choose?" Include a "none of these" option.

   Example task:
   ```
   Option A                  Option B                  Option C
   $49/mo                    $29/mo                    $79/mo
   50 GB storage             10 GB storage             Unlimited storage
   Chat + Email support      Email only                Dedicated CSM
   20 integrations           5 integrations            Unlimited integrations
   SSO included              No SSO                    SSO included

   [ ] I would choose A      [ ] I would choose B      [ ] I would choose C      [ ] None
   ```

3. **Collect data.** Each respondent completes 8-12 choice tasks. Minimum 300 respondents for reliable results; 500+ for segment-level analysis.

4. **Run statistical analysis.** Hierarchical Bayesian (HB) estimation is the standard method. This produces part-worth utilities for each attribute level for each respondent.

5. **Interpret results.**
   - **Relative importance:** Which attributes drive the most variation in choice? If price accounts for 40% of importance and support accounts for 10%, price sensitivity is high and support tier matters less.
   - **Willingness-to-pay per feature:** Convert utility differences to dollar values. If "Unlimited storage" has 15 more utility points than "10 GB" and the utility difference between $29 and $49 is 20 points, then unlimited storage is worth approximately $15/month to the average respondent.
   - **Optimal bundles:** Simulate market share for any combination of attribute levels at any price.

6. **Design tiers.** Use the utility data to package features into tiers that maximize willingness-to-pay at each tier. Assign high-value features to higher tiers. Ensure each tier has a clear upgrade driver.

### How to read results

| Attribute | Level | Avg. Utility | Implied WTP vs. Base |
|---|---|---|---|
| Storage | 10 GB (base) | 0 | -- |
| Storage | 50 GB | +8.2 | +$8/mo |
| Storage | Unlimited | +14.7 | +$15/mo |
| Support | Email (base) | 0 | -- |
| Support | Chat + Email | +5.1 | +$5/mo |
| Support | Dedicated CSM | +18.9 | +$19/mo |
| SSO | No (base) | 0 | -- |
| SSO | Yes | +11.3 | +$11/mo |

**Interpretation:** Dedicated CSM support ($19/mo implied value) and SSO ($11/mo) are the highest-value features. These belong in the premium tier. Storage upgrades have moderate value. Chat support has low incremental value -- bundling it into the mid tier adds perceived value at low cost.

### Limitations

- Requires specialized software (Sawtooth, Conjointly, etc.) and statistical expertise.
- Expensive and time-consuming (typically $15K-50K for a full study with analysis).
- Hypothetical bias -- respondents choose between hypothetical bundles, not real purchases.
- Attribute overload: more than 6-7 attributes or 4 levels per attribute degrades response quality.
- Results are segment-specific -- you need enough sample per segment for reliable estimates.

---

## Choosing a Method

| Factor | Van Westendorp | Gabor-Granger | Conjoint |
|---|---|---|---|
| **Cost** | Low ($0-2K) | Low-Medium ($1-5K) | High ($15-50K) |
| **Sample size** | 50-200 | 100-300 | 300-500+ |
| **Time to results** | 1-2 weeks | 2-3 weeks | 4-8 weeks |
| **Best for** | Finding acceptable price range | Demand curve at specific prices | Feature-level valuation and tier design |
| **Outputs** | Price range, optimal price | Revenue-maximizing price | Utility per feature, optimal bundles |
| **When to use** | New product, early exploration | Repricing, A/B test planning | Packaging design, complex products |
| **Limitation** | No purchase intent | Fixed price points only | Expensive, needs expertise |

**Practical recommendation:** Start with Van Westendorp to identify the range, use Gabor-Granger to test specific price points within that range, and invest in conjoint only when designing multi-tier packaging for a product with 4+ differentiating attributes.
