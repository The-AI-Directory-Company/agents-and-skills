# RPO/RTO Tier Definitions

## Core Concepts

**RPO (Recovery Point Objective)**: The maximum acceptable amount of data loss measured in time. An RPO of 5 minutes means you can lose at most 5 minutes of data.

**RTO (Recovery Time Objective)**: The maximum acceptable duration of downtime. An RTO of 30 minutes means the system must be operational within 30 minutes of a failure.

RPO determines your **backup strategy**. RTO determines your **recovery infrastructure**.

---

## Tier Definitions

### Tier 1: Mission-Critical

| Parameter | Target |
|-----------|--------|
| RPO | 0 (zero data loss) to 1 minute |
| RTO | < 15 minutes |

**Characteristics**: Business stops entirely without this system. Revenue loss is immediate and measurable per minute of downtime. May have regulatory or contractual SLA requirements.

**Typical systems**: Payment processing, authentication/authorization, primary transaction database, real-time trading platforms.

**Required infrastructure**:
- Synchronous replication (multi-AZ or multi-region)
- Hot standby with automatic failover
- Sub-minute health checks and failover triggers
- Dedicated runbooks tested monthly

**Business justification**: Calculate per-minute revenue loss. If 15 minutes of downtime costs more than the annual cost of Tier 1 infrastructure, the investment is justified.

---

### Tier 2: Business-Critical

| Parameter | Target |
|-----------|--------|
| RPO | 5 minutes to 1 hour |
| RTO | 30 minutes to 4 hours |

**Characteristics**: Degraded operations are tolerable short-term but cause measurable business impact within hours. Internal productivity drops significantly. Customer experience degrades but core transactions still work (via Tier 1 systems).

**Typical systems**: Email/communication platforms, CRM, order management, internal APIs, search indexes, notification services.

**Required infrastructure**:
- Asynchronous replication (cross-AZ minimum)
- Warm standby or automated restore from recent snapshot
- Point-in-time recovery capability
- Failover runbooks tested quarterly

**Business justification**: Estimate hourly productivity loss across affected teams, plus customer support cost increase. Compare against Tier 1 infrastructure cost -- if the gap is significant, Tier 2 is the right tradeoff.

---

### Tier 3: Business-Operational

| Parameter | Target |
|-----------|--------|
| RPO | 1 hour to 24 hours |
| RTO | 4 hours to 24 hours |

**Characteristics**: No immediate revenue impact. Work can continue using alternative methods. Data can be reprocessed or reconstructed from other sources.

**Typical systems**: Analytics pipelines, reporting dashboards, internal wikis, CI/CD systems, staging environments, batch processing jobs.

**Required infrastructure**:
- Daily snapshots or periodic backups
- Cold standby or manual restore process
- Documented restore procedure (does not need to be automated)
- Tested semi-annually

**Business justification**: The cost of faster recovery exceeds the cost of the downtime. Teams have workarounds. Data is reconstructable.

---

### Tier 4: Non-Critical

| Parameter | Target |
|-----------|--------|
| RPO | 24 hours to 7 days |
| RTO | 24 hours to 72 hours |

**Characteristics**: Convenience systems. Downtime is inconvenient but has no business impact. Can be rebuilt from scratch if needed.

**Typical systems**: Development environments, sandbox databases, internal tools with manual fallbacks, archived data.

**Required infrastructure**:
- Weekly backups or infrastructure-as-code rebuild capability
- No standby required
- Restore procedure documented but manual

---

## Industry Standards Reference

| Industry | System Type | Typical RPO | Typical RTO | Driver |
|----------|-------------|-------------|-------------|--------|
| Financial services | Trading platform | 0 | < 5 min | Regulatory (MiFID II, SEC) |
| Financial services | Core banking | < 1 min | < 15 min | Revenue, regulatory |
| Healthcare | EHR / patient records | < 5 min | < 1 hour | HIPAA, patient safety |
| Healthcare | Medical imaging | 1 hour | 4 hours | Clinical workflow |
| E-commerce | Checkout / payments | 0 | < 15 min | Revenue |
| E-commerce | Product catalog | 1 hour | 1 hour | Customer experience |
| SaaS (B2B) | Primary application | < 5 min | < 30 min | SLA commitments |
| SaaS (B2B) | Analytics / reporting | 24 hours | 4 hours | Low urgency |
| Media / streaming | Content delivery | 1 hour | < 30 min | Subscriber retention |
| Government | Citizen-facing services | < 15 min | < 4 hours | Public trust, mandate |

---

## Business Justification Framework

Use this framework to justify tier classification to stakeholders:

### Step 1: Quantify Downtime Cost

```
Hourly revenue impact     = [direct revenue lost per hour]
Hourly productivity impact = [affected employees] x [avg hourly cost] x [% productivity loss]
Reputation / churn cost   = [estimated customer loss] x [customer LTV]
Regulatory penalty risk   = [fine amount] x [probability if SLA breached]
---
Total hourly cost of downtime = sum of above
```

### Step 2: Quantify Recovery Infrastructure Cost

| Tier | Annual infrastructure cost (typical range) |
|------|---------------------------------------------|
| Tier 1 | 2-5x base infrastructure cost |
| Tier 2 | 1.3-2x base infrastructure cost |
| Tier 3 | 1.05-1.2x base infrastructure cost |
| Tier 4 | No additional cost |

### Step 3: Compare

```
Break-even hours = Annual Tier N cost / Hourly downtime cost
```

If the system is likely to experience more downtime than the break-even hours without the investment, the tier is justified.

### Step 4: Present

Frame the recommendation as risk management, not infrastructure spending:

> "Payment processing downtime costs $X/minute. Tier 1 DR infrastructure costs $Y/year. We break even if we prevent more than Z hours of downtime annually. Given our incident history of N hours/year, Tier 1 reduces expected annual loss by $W."
