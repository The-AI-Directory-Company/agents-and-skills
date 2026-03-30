# Anti-Patterns and Vanity Metrics

A metrics framework fails not because of missing metrics but because of wrong ones. This reference catalogs the most common anti-patterns, with examples and remediation strategies.

---

## 1. Vanity Metrics

A vanity metric moves in only one direction (usually up), feels good to report, and informs no decisions.

### Examples

| Vanity Metric | Why It's Vanity | Better Alternative |
|---|---|---|
| Total registered users | Only goes up. Says nothing about engagement or value. | Monthly active users (MAU) or 30-day retention rate |
| Cumulative revenue | Monotonically increasing by definition. | Monthly recurring revenue (MRR) or net revenue retention |
| Total page views | Includes bots, accidental clicks, and rage-refreshes. | Pages per session or task completion rate |
| App downloads | Downloads without activation are noise. | Day-7 activation rate |
| Number of features shipped | Measures output, not outcome. | Feature adoption rate (% of target users who used the feature within 30 days) |

### How to detect vanity metrics

Ask three questions:
1. **Can this metric go down?** If not, it is vanity.
2. **Would a change in this metric alter our priorities?** If not, it is decoration.
3. **Does this metric distinguish between good and bad outcomes?** "Total signups" does not distinguish between users who activate and users who bounce.

---

## 2. Proxy Divergence

A proxy metric is a stand-in for something harder to measure. Proxies are useful until they diverge from the real outcome.

### Classic example: DAU as a proxy for engagement

- **Original intent:** Daily Active Users (DAU) approximated how many people found value in the product each day.
- **Divergence:** Push notifications and dark patterns inflate DAU. Users open the app, see nothing relevant, close it. DAU is high. Actual engagement (completing a meaningful action) is flat or declining.
- **Resolution:** Replace DAU with "Daily Active Users who completed at least one core action" -- sometimes called "meaningful DAU" or "engaged DAU."

### Classic example: Lines of code as a proxy for productivity

- **Original intent:** More code written = more work done.
- **Divergence:** Incentivizes verbose code, discourages refactoring (which removes lines), and penalizes efficient solutions.
- **Resolution:** Measure outcomes (features delivered, bugs resolved, cycle time) not output volume.

### Classic example: Time-on-site as a proxy for engagement

- **Original intent:** Users spending more time on the site are more engaged.
- **Divergence:** Users who cannot find what they need also spend more time. Confusion and engagement produce the same signal.
- **Resolution:** Pair time-on-site with task completion rate. High time + high completion = deep engagement. High time + low completion = frustration.

### How to detect proxy divergence

Run this test quarterly: look at the proxy metric and the real outcome side by side. If they have moved in opposite directions at any point in the last two quarters, the proxy has diverged and should be replaced or supplemented with guardrails.

---

## 3. Composite Score Pitfalls

Composite scores blend multiple inputs into a single number (e.g., "Health Score = 0.4 * NPS + 0.3 * Usage + 0.3 * Support Tickets"). They are popular because they simplify reporting. They are dangerous because they obscure signal.

### Problems with composite scores

1. **Offsetting signals.** NPS drops 20 points but usage increases, so the composite score barely moves. The team misses a satisfaction crisis because the number looks stable.

2. **Arbitrary weighting.** The weights (0.4, 0.3, 0.3) are usually chosen by gut feel, not validated against outcomes. Changing weights changes the narrative without changing reality.

3. **Unactionable.** When a composite score drops, the first question is always "which component caused it?" -- which means the team needs the components anyway. The composite adds a layer of indirection without adding insight.

4. **False precision.** A "Health Score of 72.4" implies a level of measurement accuracy that does not exist when the inputs are a survey (NPS), a count (usage), and a rate (tickets per user).

### When composite scores are acceptable

- As a **screening metric** for triage (e.g., identifying accounts that need attention), not as a primary metric.
- When the components are published alongside the composite, so the team can always drill down.
- When the weighting has been validated empirically (e.g., regression analysis shows these weights predict churn).

### Better alternative

Report the components individually. Use the primary/guardrail/diagnostic framework: pick one component as the primary metric and demote the others to guardrail or diagnostic status.

---

## 4. Goodhart's Law

> "When a measure becomes a target, it ceases to be a good measure."
> -- Charles Goodhart (paraphrased)

Goodhart's Law is not a theoretical risk. It is the default outcome of any metric without guardrails.

### Examples in practice

| Primary Metric (Target) | Perverse Behavior | Missing Guardrail |
|---|---|---|
| Call center handle time (minimize) | Agents hang up on complex calls to keep averages down. | Customer satisfaction score (CSAT) per call |
| Lines of code per sprint | Developers pad code, avoid refactoring, copy-paste instead of abstracting. | Defect rate, code review rejection rate |
| Time-to-first-response (support) | Team sends a canned "We're looking into it" response within 60 seconds, then takes 3 days to actually resolve. | Time-to-resolution, first-contact resolution rate |
| Number of experiments run per quarter | Teams run trivial, low-impact experiments to hit the count. | Revenue impact per experiment, statistical power of experiments |
| Deployment frequency | Teams ship tiny, inconsequential changes to inflate the count. | Change failure rate, mean time to recovery |

### How to defend against Goodhart's Law

1. **Always pair a primary metric with guardrails.** The guardrail catches the perverse incentive before it causes damage.
2. **Rotate metrics periodically.** If the same metric has been the primary target for 4+ quarters, audit whether the team is optimizing the metric or the outcome.
3. **Watch for "teaching to the test."** If the team's work increasingly focuses on the specific behaviors that move the metric rather than the broader objective, the metric has become the goal.
4. **Inspect the mechanism, not just the number.** When a metric improves, ask how. If the answer is a process change that does not improve the user's experience, you have a Goodhart problem.

---

## Quick-Reference Decision Table

| Symptom | Likely Anti-Pattern | Remedy |
|---|---|---|
| Metric only goes up | Vanity metric | Replace with a rate or ratio that can decline |
| Metric improves but users are not happier | Proxy divergence | Validate proxy against real outcome; add guardrails |
| Single number hides conflicting signals | Composite score pitfall | Break into components; assign primary/guardrail roles |
| Team games the metric | Goodhart's Law | Add guardrail metrics; rotate primary metric periodically |
| Nobody acts when metric changes | Irrelevant metric | Remove it from the framework entirely |
