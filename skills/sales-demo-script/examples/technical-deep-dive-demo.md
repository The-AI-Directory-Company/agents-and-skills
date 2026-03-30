# Sales Demo Script: Clarion Analytics — Technical Deep Dive

## Demo Context

- **Product:** Clarion — a product analytics platform for B2B SaaS companies
- **Audience:** Staff Engineer and Data Engineering Lead at a Series B dev tools company (80 employees, 6-person data team)
- **Current tool:** Self-hosted Metabase + custom event pipeline on Snowflake
- **Time slot:** 15 minutes (carved out of a 30-minute technical evaluation call)
- **Desired next step:** POC with production data connected via Snowflake integration
- **Why this audience is different:** This is an engineering audience evaluating architecture, data model, and integration — not business outcomes. They care about how it works, not what it does for their VP.

---

## 1. Opening (1 minute)

"Alex, Priya — thanks for the time. I know you have 15 minutes and you're evaluating whether Clarion can replace your Metabase + custom pipeline setup without adding operational burden to your data team.

I'll focus on three things:
1. How Clarion ingests events and where the data lives
2. How the query engine works under the hood — latency, scale limits, and what happens at 10x your current volume
3. The Snowflake integration — what stays in your warehouse versus what we process

Then we can talk about setting up a POC. I'll skip the product tour — you can click through the UI on your own. Fair?"

No company history. No slides. Engineers evaluate by probing architecture, not watching marketing walkthroughs.

## 2. Discovery Questions (2 minutes)

These should feel like a technical conversation, not a sales qualification.

- **Architecture:** "Walk me through your current pipeline — are you using a CDP like Segment, or shipping events directly to Snowflake?"
- **Pain:** "When a PM asks for a new funnel analysis, what does that look like? Is the data team building dbt models, or querying raw events?"
- **Scale:** "Roughly how many events per day are you processing? And what's the query latency your team considers acceptable?"
- **Constraints:** "Are there hard requirements around data residency or keeping raw data in your own warehouse?"
- **Evaluation criteria:** "What would make you confident enough to run a POC? Is there a specific technical concern you want me to address?"

Listen for: event volume, latency expectations, data residency requirements, and whether they want Clarion to be a warehouse replacement or a query layer on top of their existing warehouse.

## 3. Product Walkthrough (10 minutes)

### Section 1: Event Ingestion Architecture (4 min)

**Problem:** "You mentioned your custom pipeline handles event ingestion into Snowflake, and the maintenance overhead is the main pain — schema migrations, failed batches, dedup logic."

**Solution:** [Show architecture diagram — whiteboard or shared screen]
- Walk through the ingestion path: SDK sends events via HTTPS to Clarion's collection endpoint
- Events are validated against a schema registry — malformed events are quarantined, not dropped
- Data lands in Clarion's columnar store (ClickHouse-based) within 3 seconds for real-time queries
- For customers who require raw data in their own warehouse: a continuous export streams events to Snowflake in 60-second micro-batches via a managed connector

**Proof:** "Our P99 ingestion latency is 1.2 seconds across all customers. At your volume — roughly 50M events/day — you'd be well within our standard tier. We have customers processing 2B events/day on the same architecture."

[Pause] "Does this architecture create any concerns for your data residency or compliance requirements?"

### Section 2: Query Engine and Performance (3 min)

**Problem:** "You said Metabase queries on Snowflake take 15-30 seconds for complex funnels, and your PMs complain about the wait. Let me show you what happens under the hood in Clarion."

**Solution:** [Live in demo environment — open the query inspector, not the dashboard]
- Run a 7-step funnel query across 90 days of data (120M events in the demo dataset)
- Show the query plan: how Clarion partitions by time, prunes segments, and parallelizes across shards
- Result returns in 1.4 seconds
- Open the query inspector: show the ClickHouse query that ran underneath, the rows scanned, and the cache state
- Run the same query again — 200ms from cache
- Show the "Explain" view that breaks down where time was spent

**Proof:** "At 120M events, cold query was 1.4 seconds. At your current 50M events/day with a 90-day window — roughly 4.5B events — our median query latency is under 3 seconds. Here is a latency histogram from a customer at similar scale."

[Show the histogram — not a marketing chart, but actual P50/P95/P99 numbers]

### Section 3: Snowflake Integration (3 min)

**Problem:** "Your data team has built dbt models and downstream reporting on Snowflake. You cannot rip that out — you need Clarion to work alongside it."

**Solution:**
- Show the Snowflake connector configuration: point Clarion at a Snowflake database, and it reads your existing event tables
- Clarion can operate in two modes:
  - **Warehouse-native:** Query your Snowflake tables directly via Clarion's UI (higher latency, your data never leaves your warehouse)
  - **Hybrid:** Ingest through Clarion SDK for real-time, continuous export to Snowflake for your dbt models and existing dashboards
- Show the schema sync: Clarion detects schema changes in Snowflake and auto-updates the query engine — no manual mapping

**Proof:** "Census runs hybrid mode — Clarion handles real-time product analytics, and their data team still uses dbt + Snowflake for business reporting. Both query the same underlying events. No duplication, no pipeline to maintain."

## 4. Objection Handling

**Objection: "We don't want another managed service — we've been burned by vendor lock-in."**
- Acknowledge: "Vendor lock-in is a legitimate concern, especially for a data team that built their own pipeline for exactly that reason."
- Reframe: "Clarion exports your raw events in Parquet to S3 or your Snowflake warehouse in real time. If you leave, your data leaves with you — same schema, same format."
- Evidence: "I can show you the export format right now. It is the same columnar structure you would write yourself. No proprietary encoding."

**Objection: "ClickHouse is open source — why not self-host it?"**
- Acknowledge: "It is, and your team could absolutely set it up."
- Reframe: "The query engine is one piece. The value is the semantic layer on top — funnels, retention, cohorts, account-level metrics — plus the ingestion pipeline, schema registry, and managed scaling. Self-hosting ClickHouse for analytics is a 2-3 month project, and then you are maintaining it."
- Evidence: "Netlify evaluated self-hosting ClickHouse versus Clarion. They estimated 3 engineer-months to build and 0.5 FTE ongoing maintenance. They chose Clarion and reallocated that time to their core product."

**Objection: "Your latency numbers look good in a demo, but what about at our scale with our query patterns?"**
- Acknowledge: "Demo data is always cleaner than production. Fair question."
- Reframe: "That is exactly what the POC is for. We connect to your Snowflake, run your actual queries, and you measure latency in your environment."
- Evidence: "The POC takes 2-3 days to set up. You will have real latency numbers on your data by the end of week one."

## 5. Close and Next Steps (2 minutes)

"Based on what we covered: Clarion's ingestion handles your volume with headroom, query latency is 10-20x faster than your Metabase + Snowflake setup, and the hybrid mode means your dbt models and existing reporting keep working.

The best next step is a POC. Here is what that looks like:
- Day 1: I set up the Snowflake connector to read your existing event tables
- Days 2-3: Your team runs 5-10 of your most common queries in Clarion and measures latency against Metabase
- End of week 1: We review results together and you decide if the numbers justify moving forward

Can we start the connector setup on Thursday? I will need 30 minutes with whoever manages your Snowflake access."
