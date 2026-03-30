# Competitive Positioning Guide

Competitive positioning is how you differentiate in the buyer's mind when they are comparing options. It is not about being better at everything — it is about being clearly better at the thing the buyer cares about most.

---

## Building a Competitive Comparison Table

A competitive table is the foundation of positioning. It should be honest, specific, and useful for reps on live calls — not a marketing asset that exaggerates strengths and hides weaknesses.

### Table Structure

| Dimension | Us | Competitor A | Competitor B | Status Quo (Do Nothing) |
|-----------|-----|-------------|-------------|------------------------|
| Best for | [Segment/use case where we win] | [Their sweet spot] | [Their sweet spot] | [When inaction is rational] |
| Pricing model | [Model and range] | [Model and range] | [Model and range] | [Cost of current process] |
| Key strength | [Our real differentiator] | [Their real strength] | [Their real strength] | [Familiarity, no migration] |
| Key weakness | [Our honest limitation] | [Their real gap] | [Their real gap] | [Growing cost/risk over time] |
| Implementation | [Timeline and effort] | [Timeline and effort] | [Timeline and effort] | [No implementation needed] |
| Ideal customer | [Size, industry, tech stack] | [Size, industry, tech stack] | [Size, industry, tech stack] | [Companies with low urgency] |
| Landmine question | — | [Question exposing their gap] | [Question exposing their gap] | [Question exposing cost of inaction] |

### Rules for Building the Table

1. **Include "Status Quo" as a competitor.** Most deals are lost to "do nothing," not to a named competitor. Positioning against inaction is as important as positioning against products.

2. **Be honest about your weaknesses.** If your product is weaker in an area, say so. Reps will discover it in competitive deals anyway — better to arm them with a truthful response than let them get surprised. A rep who admits a weakness and reframes it is more credible than one who claims perfection.

3. **Use specific facts, not adjectives.** "Faster" is not a competitive position. "Median query latency of 1.4 seconds vs. their 12 seconds on the same dataset" is a competitive position.

4. **Source your competitor data.** Use their public documentation, pricing pages, customer reviews on G2/TrustRadius, and information from prospects who have evaluated them. Do not rely on assumptions or outdated information.

5. **Limit to 3-4 competitors.** If your reps encounter more than 4 competitors regularly, your ICP is too broad. The table should cover the competitors that appear in 80%+ of competitive deals.

---

## Landmine Questions

A landmine question is a question the rep asks the prospect that surfaces a competitor's weakness — without directly criticizing the competitor. The prospect discovers the gap themselves, which is far more persuasive than you pointing it out.

### How to Build Landmine Questions

1. Identify a specific, verifiable weakness of the competitor.
2. Frame it as a neutral question about the prospect's requirements.
3. Let the prospect realize the competitor cannot meet that requirement.

### Examples

**Competitor weakness: Does not support SSO on their mid-tier plan.**
```
Landmine: "Is single sign-on a requirement for your security team?
           Some vendors only include it at their enterprise tier —
           worth checking what's included at the plan you're evaluating."
```

**Competitor weakness: Implementation takes 8-12 weeks with professional services.**
```
Landmine: "What is your target timeline for getting this live?
           I'd recommend asking each vendor you're evaluating for
           their average time-to-value with a customer your size."
```

**Competitor weakness: No native integration with [platform the prospect uses].**
```
Landmine: "You mentioned you're running [platform]. How important is
           a native integration versus building a custom connector?
           Worth asking each vendor about their integration approach."
```

### Anti-Patterns

- **Do not trash-talk.** "Competitor X is terrible at [thing]" destroys your credibility. Let the question do the work.
- **Do not ask leading questions.** "Aren't you worried about Competitor X's security issues?" is transparent and makes you look desperate.
- **Do not lie or exaggerate.** If the competitor has fixed the weakness you are referencing, your landmine backfires and you lose trust.

---

## Honest Self-Assessment

Your competitive table must include an honest view of where you lose and why. This section is for internal use — it helps reps know when to compete hard and when to walk away.

### How to Document Weaknesses

For each weakness, document:

1. **The limitation:** What specifically is weaker than the competition?
2. **When it matters:** In what deals or segments does this become a deciding factor?
3. **Reframe:** How should reps position this when it comes up?
4. **Roadmap status:** Is this being addressed? If yes, when? If no, why not?

### Example

```
Limitation:     No native mobile app — web only, responsive but not native.
When it matters: Deals where field workers need offline access on mobile devices.
                 Estimated 15% of competitive deals lost to this gap.
Reframe:        "Our responsive web app works on any device without app store
                 deployment. For teams that need offline, we have a PWA with
                 local caching. If native offline is a hard requirement, I want
                 to be upfront — [Competitor A] has a native app that handles
                 that better today."
Roadmap:        Native app in development, beta Q3 2026. Do not promise this
                 in deals — reference only if asked and only as "in development."
```

### When to Concede

Not every deal is winnable. Teach reps to concede gracefully when:

- The prospect's #1 requirement is the competitor's #1 strength and your known weakness.
- The prospect is already deep in evaluation with a competitor and your entry point is late.
- The deal size does not justify the competitive effort.

Conceding well preserves the relationship: "Based on what you've described, [Competitor A] may be a better fit for [specific requirement]. If that changes, or if you need [our differentiator] down the line, I'm here."

---

## Refresh Cadence

Competitive positioning decays. Competitors ship features, change pricing, and enter or exit segments. A competitive table that is 6 months old is dangerous — reps will make claims that are no longer true.

### Recommended Cadence

| Activity | Frequency | Owner | Source |
|----------|-----------|-------|--------|
| Full competitive table review | Quarterly | Product Marketing | Competitor docs, pricing pages, G2 reviews, win/loss data |
| Pricing check | Monthly | Sales Ops | Competitor pricing pages, prospect feedback |
| Win/loss analysis (competitive deals) | After every competitive loss | Sales Manager | CRM loss reasons, post-loss interviews |
| New competitor assessment | As identified | Product Marketing | Sales team flagging, market monitoring |
| Landmine question refresh | Quarterly | Sales Enablement | Updated competitor weaknesses, sales feedback |

### Signals That Your Positioning Needs an Update

- A competitor launches a feature that eliminates one of your landmine questions.
- Your win rate against a specific competitor drops by more than 10 points in a quarter.
- Reps report hearing a new competitor name in 3+ deals within a month.
- Your pricing is referenced as "expensive" more frequently than the prior quarter.
- A competitor changes their pricing model or packaging.

### How to Distribute Updates

- Do not send a 10-page competitive brief and expect reps to read it.
- Update the competitive table directly in the playbook or sales wiki.
- Highlight changes in a 3-bullet summary at the top: what changed, what it means, and what reps should do differently.
- Run a 15-minute "competitive flash update" in the weekly sales team meeting when significant changes occur.
