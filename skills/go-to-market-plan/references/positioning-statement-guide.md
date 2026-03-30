# Positioning Statement Guide

The positioning statement is the foundation of a go-to-market plan. Every channel, message, and metric flows from it. If the positioning is wrong, everything downstream is wasted effort.

## The Format

```
For [target customer]
who [need or pain point],
[Product name] is a [category]
that [key benefit].
Unlike [primary alternative],
we [key differentiator].
```

Every field is required. If you cannot fill a field, the positioning is not ready — go back to discovery.

---

## Field-by-Field Guidance

### For [target customer]

Be specific enough that you could build a list of these people. "Businesses" is too broad. "Series A-C B2B SaaS companies with 10-50 engineers" is targetable.

### Who [need or pain point]

State this in the customer's language, not your feature vocabulary. The customer says "I waste 3 hours a week on status updates" — they do not say "I need asynchronous standup tooling."

### [Product name] is a [category]

Pick a category the buyer already understands. Creating a new category is a multi-year, multi-million-dollar effort. If you are a startup, anchor to a known category and differentiate within it.

### That [key benefit]

One benefit, not three. The benefit should be an outcome (saves time, reduces cost, increases revenue) — not a feature (has an API, supports SSO).

### Unlike [primary alternative]

Name the most common thing your target customer does today. This is often not a competitor — it is a spreadsheet, a manual process, or doing nothing.

### We [key differentiator]

This must be true only of your product. If a competitor could honestly make the same claim, the differentiator is too generic.

---

## Good vs. Bad Examples

### Example 1: Developer Tool

**Bad:**
```
For developers
who need better tooling,
DevKit is a developer platform
that improves productivity.
Unlike other tools,
we are easy to use.
```

Why it fails: "Developers" is everyone. "Better tooling" is vague. "Improves productivity" is generic. "Easy to use" is what every tool claims.

**Good:**
```
For backend engineers at companies shipping microservices
who lose hours debugging distributed traces across 5+ services,
TraceKit is a distributed tracing tool
that pinpoints the failing service in under 30 seconds.
Unlike Jaeger or Zipkin,
we auto-instrument without code changes — one YAML file, zero SDK integration.
```

Why it works: The target is specific (backend engineers, microservices). The pain is concrete (hours debugging). The benefit is measurable (30 seconds). The differentiator is verifiable (no code changes).

---

### Example 2: HR Software

**Bad:**
```
For HR teams
who want to modernize,
PeopleSync is an HR platform
that streamlines HR processes.
Unlike legacy systems,
we are cloud-native.
```

Why it fails: Every HR tool made after 2015 claims to be cloud-native. "Streamlines processes" means nothing specific.

**Good:**
```
For HR directors at remote-first companies with 100-500 employees
who spend 10+ hours per month reconciling PTO across time zones and local labor laws,
PeopleSync is a leave management system
that auto-calculates PTO balances across 40+ country-specific labor regulations.
Unlike Deel or Remote.com,
we handle the leave-payroll reconciliation natively — no CSV exports to your payroll provider.
```

Why it works: Specific audience (remote-first, 100-500). Quantified pain (10+ hours/month). Concrete benefit (auto-calculates across 40+ countries). Verifiable differentiator (native payroll reconciliation).

---

### Example 3: Security Product

**Bad:**
```
For companies
who care about security,
ShieldAI is a security solution
that keeps your data safe.
Unlike competitors,
we use AI.
```

Why it fails: Everyone "cares about security." "Keeps data safe" is table stakes. "We use AI" is not a differentiator in 2026.

**Good:**
```
For SOC analysts at mid-market companies (500-5,000 employees)
who triage 200+ alerts per day and miss critical threats buried in noise,
ShieldAI is an alert correlation engine
that reduces triage volume by 85% by clustering related alerts into incidents.
Unlike Splunk SOAR or Palo Alto XSOAR,
we require zero playbook authoring — correlation rules learn from analyst behavior in the first 2 weeks.
```

Why it works: Specific persona (SOC analysts, mid-market). Quantified pain (200+ alerts/day). Measurable benefit (85% reduction). Differentiator describes a mechanism (learns from behavior, no playbooks).

---

### Example 4: E-Commerce SaaS

**Bad:**
```
For online stores
who want to grow,
CartBoost is an e-commerce tool
that increases conversions.
Unlike Shopify apps,
we are more powerful.
```

Why it fails: "More powerful" is subjective and unverifiable. No specificity on what kind of store or what conversion problem.

**Good:**
```
For DTC brands on Shopify doing $1M-$20M in annual revenue
who lose 68% of carts at checkout because shipping costs surprise customers,
CartBoost is a dynamic shipping incentive engine
that shows personalized free-shipping thresholds that increase AOV by 15-22%.
Unlike static free-shipping bars,
we adjust thresholds per customer based on cart contents, margin, and purchase history.
```

Why it works: Specific segment (DTC, Shopify, $1M-$20M). Specific pain with data (68% cart loss). Benefit with range (15-22% AOV increase). Mechanism as differentiator (dynamic per-customer thresholds).

---

### Example 5: Data Infrastructure

**Bad:**
```
For data teams
who need a better pipeline,
FlowPipe is a data tool
that moves data faster.
Unlike open-source alternatives,
we are enterprise-ready.
```

Why it fails: "Enterprise-ready" is a checkbox list, not a differentiator. "Moves data faster" does not specify from where to where.

**Good:**
```
For data engineers at companies running 50+ dbt models
who spend 40% of their time debugging broken pipelines caused by upstream schema changes,
FlowPipe is a schema-aware data pipeline orchestrator
that detects breaking schema changes before they propagate downstream.
Unlike Airflow or Dagster,
we validate column-level lineage at deploy time — broken models fail in CI, not in production at 3 AM.
```

Why it works: Precise audience (data engineers, 50+ dbt models). Quantified pain (40% of time). Clear benefit (detect before propagation). Mechanism-based differentiator (column-level lineage at deploy time).

---

## Validation Questions

After writing a positioning statement, test it with these:

1. **Specificity:** Could you build a prospect list from the target customer description alone?
2. **Pain reality:** Have you heard a real customer describe this pain in these words?
3. **Benefit measurability:** Can the customer verify the benefit within 30 days?
4. **Differentiator exclusivity:** Is this true only of your product right now?
5. **Competitor test:** Could your top competitor paste their name into this statement and have it still be accurate? If yes, rewrite.
