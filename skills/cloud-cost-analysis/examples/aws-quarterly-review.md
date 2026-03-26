# Q4 2025 AWS Cost Analysis — Relay Logistics

## Spend Summary

Analysis period: October-December 2025. Account: relay-prod (ID 481923756012).

| Service          | Monthly Cost | % of Total | Trend (3mo) |
|------------------|-------------|------------|-------------|
| EC2 / Compute    | $67,400     | 41%        | +18%        |
| RDS (PostgreSQL) | $34,200     | 21%        | +6%         |
| S3 / Storage     | $19,800     | 12%        | +14%        |
| Data Transfer    | $16,500     | 10%        | +31%        |
| ElastiCache      | $11,300     | 7%         | flat        |
| Other            | $14,800     | 9%         | +4%         |
| **Total**        | **$164,000**| **100%**   | **+14%**    |

Data transfer is the fastest-growing category. Cross-AZ traffic between the API tier and RDS accounts for $9,200/mo of the $16,500.

## Waste Identification

| Resource | Type | Issue | Monthly Cost | Est. Savings |
|----------|------|-------|-------------|-------------|
| 14 unattached EBS volumes | gp3 | Orphaned after Nov migration | $840 | $840 |
| staging-api (3 instances) | m5.xlarge | Running 24/7, used Mon-Fri 9-6 | $1,620 | $1,050 |
| qa-db-cluster | db.r5.2xlarge | 4% avg CPU, <1 GB data | $2,100 | $1,680 |
| route-optimizer-snapshots | EBS snapshots | 340 daily snapshots, no lifecycle policy | $1,900 | $1,520 |
| demo-environment | Full stack | Last accessed Sept 12, running since July | $3,200 | $3,200 |

**Total identifiable waste: $8,290/month ($99,480/year)**

## Right-Sizing Recommendations

Based on 30-day CloudWatch metrics (Nov 15 - Dec 15):

| Resource | Current | Avg CPU | Avg Mem | Recommended | Monthly Savings |
|----------|---------|---------|---------|-------------|-----------------|
| api-prod-1 through api-prod-4 | m5.2xlarge | 14% | 31% | m5.xlarge | $720 (x4 = $2,880) |
| shipment-worker-1..3 | c5.4xlarge | 11% | 18% | c5.xlarge | $460 (x3 = $1,380) |
| analytics-db-replica | db.r5.4xlarge | 19% | 42% | db.r5.2xlarge | $1,040 |
| cache-routing | cache.r5.2xlarge | 8% | 22% | cache.r5.large | $680 |

**Total right-sizing opportunity: $5,980/month**

## Pricing Model Optimization

Current mix: 92% on-demand, 8% reserved (legacy 1-year RIs expiring March 2026).

- **Compute Savings Plan (1-year):** Commit $28/hr based on floor utilization across all regions. Projected savings: $8,400/mo (31% discount vs. on-demand).
- **RDS Reserved Instances (1-year):** Reserve the primary db.r5.2xlarge (recommended post-downsize) and two read replicas. Break-even at month 8. Savings: $4,100/mo.
- **Spot for batch workers:** The route-optimizer fleet (6 c5.2xlarge) is fault-tolerant with checkpointing. Spot discount at current pricing: 68%. Savings: $3,800/mo with 2-minute interruption handling already in place.
- **Staging scheduling:** Stop staging-api and staging-worker nightly 7 PM - 7 AM and weekends. Savings: $1,050/mo.

## Savings Roadmap

| Priority | Action | Monthly Savings | Effort | Timeline |
|----------|--------|----------------|--------|----------|
| P0 | Delete 14 orphaned EBS volumes | $840 | 1 hour | This week |
| P0 | Shut down demo environment | $3,200 | 1 hour | This week |
| P0 | Add snapshot lifecycle policy (keep 7 days) | $1,520 | 2 hours | This week |
| P0 | Schedule staging environments | $1,050 | 1 day | This week |
| P1 | Right-size api-prod instances (m5.xlarge) | $2,880 | 3 days | 2 weeks |
| P1 | Purchase 1-year Compute Savings Plan | $8,400 | 1 day | 30 days |
| P1 | Reserve downsized RDS instances | $4,100 | 1 day | 30 days |
| P2 | Move route-optimizer to spot fleet | $3,800 | 1 sprint | 60 days |
| P2 | Right-size remaining instances | $3,100 | 1 week | 60 days |
| P2 | Move cross-AZ traffic to same-AZ placement | $4,600 | 2 sprints | 90 days |

## ROI Projection

- **Quick wins (week 1):** $6,610/mo savings, 0 engineering days
- **Medium-term (30 days):** $21,890/mo cumulative, ~5 engineering days ($4,000 implementation cost)
- **Full realization (90 days):** $33,490/mo = **$401,880/year**, ~22 engineering days ($17,600 implementation cost)
- **Net first-year savings:** $384,280 (after implementation cost)
- **Spend reduction:** 20.4% of current monthly bill
