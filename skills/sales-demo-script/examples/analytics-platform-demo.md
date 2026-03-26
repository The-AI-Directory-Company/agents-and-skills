# Sales Demo Script: Clarion Analytics Platform

## Demo Context

- **Product:** Clarion — a product analytics platform for B2B SaaS companies
- **Audience:** VP of Product and a Senior PM at a Series C fintech (200 employees, 12-person product team)
- **Current tool:** Amplitude (dissatisfied with cost at scale and query complexity)
- **Time slot:** 30 minutes
- **Desired next step:** 14-day trial with their production data

---

## 1. Opening (2 minutes)

"Thanks for making the time, Sarah and James. Before I show you anything — from our last call, I understand your product team is spending significant time building custom Amplitude charts just to answer basic retention questions, and the cost has scaled faster than your user base. Is that still the core frustration?"

[Wait for confirmation or correction.]

"Great. I'll show you three things today:

1. How Clarion answers retention and funnel questions without writing queries
2. How our pricing works at your scale versus what you're paying now
3. Our B2B-specific account analytics — which is something Amplitude does not do natively

Then we'll talk about getting you a trial with your actual data. Sound good?"

## 2. Discovery Questions (3 minutes)

If Sarah or James raise new context, use these to dig deeper:

- **Current state:** "Walk me through what happens when a PM on your team needs to answer a retention question today."
- **Pain:** "When a PM needs a chart they haven't built before, how long does that take end to end?"
- **Impact:** "How many hours per week would you estimate your PMs spend building and maintaining dashboards?"
- **Decision criteria:** "If you switched tools, what would success look like in the first 30 days?"
- **Stakeholders:** "Beyond your team, would engineering or data need to evaluate this?"
- **Timeline:** "You mentioned your Amplitude renewal is in Q3 — is that a hard deadline?"

## 3. Product Walkthrough (20 minutes)

### Section 1: Self-Serve Retention Analysis (8 min)

**Problem:** "You mentioned PMs wait 2-3 days for a data analyst to build retention charts in Amplitude. Let me show you what that looks like in Clarion."

**Solution:** [Live in demo environment with fintech sample data]
- Open Clarion, navigate to Retention Explorer
- Type natural language: "Show me 7-day retention for users who completed onboarding in March, grouped by plan tier"
- Chart renders in under 3 seconds
- Click a cohort segment to drill into individual user journeys
- Save as a reusable template with one click

**Proof:** "Pipe, the fintech payments company, cut their time-to-insight from 2 days to about 15 minutes after switching. Their PMs now self-serve 90% of retention questions."

[Pause] "Does this match the kind of question your PMs are asking?"

### Section 2: B2B Account-Level Analytics (7 min)

**Problem:** "You mentioned Amplitude treats everything as individual users, but your customers are companies with multiple seats. That makes account health hard to measure."

**Solution:**
- Switch to Account Analytics view
- Show account-level metrics: DAU per account, feature adoption by account tier, expansion signals
- Demo the "Account Health Score" — a composite metric combining usage depth, breadth, and trend
- Show the alert: "Account X usage dropped 40% this week" with drill-down to specific users

**Proof:** "This is why B2B SaaS companies like Lattice and Census moved to Clarion. Amplitude's user-level model requires workarounds for account analytics. Ours is built for it."

### Section 3: Pricing Transparency (5 min)

**Problem:** "You mentioned your Amplitude bill grew 60% last year while your user base grew 25%."

**Solution:**
- Open Clarion's pricing calculator (publicly available)
- Enter their approximate MTU count: 150K
- Show the price: $1,450/month on the Growth plan, flat rate, no event-volume penalties
- Compare side-by-side with their current Amplitude spend (~$3,800/month estimated)

**Proof:** "We price on monthly tracked users, not event volume. That means your cost scales linearly with your user base, not with how many events each user fires. For a fintech product with high event density, that difference is significant."

## 4. Objection Handling

**Objection: "Amplitude has a bigger ecosystem — integrations, community, templates."**
- Acknowledge: "Amplitude's ecosystem is mature, no question."
- Reframe: "The question is whether your team uses that ecosystem or builds custom charts anyway. From what you described, your PMs are building from scratch most of the time."
- Evidence: "We have native integrations with Segment, Snowflake, and dbt — which covers most B2B data stacks. Pipe's team found they needed fewer integrations because the core analytics covered more out of the box."

**Objection: "Migration seems painful — we have hundreds of saved charts."**
- Acknowledge: "Migration is a real cost, and I would not minimize it."
- Reframe: "How many of those saved charts are actively used? Most teams find that 15-20% of dashboards drive 90% of decisions."
- Evidence: "We offer a guided migration where we rebuild your top 20 dashboards in week one of the trial. Census migrated 400 charts — their team rebuilt the 30 that mattered, and nobody missed the rest."

**Objection: "We need to run this by our data engineering team."**
- Acknowledge: "Absolutely — data eng buy-in is critical."
- Reframe: "What specific concerns would they have? Usually it is SDK implementation and data warehouse compatibility."
- Evidence: "Our SDK is a drop-in replacement for Amplitude's — same event structure. I can set up a 30-minute technical session with your data lead."

## 5. Close and Next Steps (2 minutes)

"Based on what we covered, Clarion solves two things for your team: PMs self-serving retention and funnel analysis without analyst bottlenecks, and account-level analytics that Amplitude does not support natively — at roughly 60% lower cost.

Here is what I would suggest: a 14-day trial connected to your production data. We handle the SDK setup and rebuild your top 20 dashboards in the first week so your PMs can compare side-by-side with Amplitude.

Could we kick that off next Tuesday? I would need 30 minutes with your data engineering lead to get the SDK configured."
