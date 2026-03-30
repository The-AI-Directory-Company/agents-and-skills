---
name: cloud-cost-analysis
description: Analyze and optimize cloud infrastructure costs — identifying waste, right-sizing resources, evaluating reserved vs on-demand pricing, and producing savings roadmaps with ROI projections.
metadata:
  displayName: "Cloud Cost Analysis"
  categories: ["operations", "engineering"]
  tags: ["cloud", "cost-optimization", "FinOps", "AWS", "infrastructure"]
  worksWellWithAgents: ["ci-cd-engineer", "cloud-architect", "devops-engineer"]
  worksWellWithSkills: ["system-design-document"]
---

# Cloud Cost Analysis

## Before you start

Gather the following from the user:

1. **Which cloud provider(s)?** (AWS, GCP, Azure, or multi-cloud)
2. **Current monthly spend** (total and by service if available)
3. **Cost breakdown access** (billing console exports, Cost Explorer data, or CSV dumps)
4. **Growth trajectory** (expected traffic or workload changes over 6-12 months)
5. **Commitment constraints** (existing reserved instances, savings plans, or enterprise agreements)

If the user says "our cloud bill is too high," push back: "What's your current monthly spend, which services make up the top 80%, and do you have any existing reservations or savings plans?"

## Cost analysis template

### 1. Spend Summary

Break down current spend into the top cost categories. Cover at least 80% of total spend.

```
| Service          | Monthly Cost | % of Total | Trend (3mo) |
|------------------|-------------|------------|-------------|
| EC2 / Compute    | $42,300     | 38%        | +12%        |
| RDS / Databases  | $28,100     | 25%        | +5%         |
| S3 / Storage     | $15,200     | 14%        | +8%         |
| Data Transfer    | $9,800      | 9%         | +22%        |
| Other            | $15,600     | 14%        | flat        |
| **Total**        | **$111,000**| **100%**   | **+11%**    |
```

### 2. Waste Identification

Audit each category for idle, oversized, or orphaned resources. Use this checklist:

- **Idle resources**: Instances, load balancers, or databases with <5% average utilization over 14 days
- **Orphaned storage**: Unattached EBS volumes, old snapshots, unused S3 buckets
- **Oversized instances**: CPU/memory utilization consistently below 30% — candidates for right-sizing
- **Zombie environments**: Dev/staging environments running 24/7 that could use scheduling
- **Unused reservations**: Reserved capacity for instance types no longer in use

For each finding, document the resource, its current cost, and the estimated savings.

### 3. Right-Sizing Recommendations

For every oversized resource, propose a specific target:

```
| Resource         | Current Type | Avg CPU | Avg Memory | Recommended  | Monthly Savings |
|------------------|-------------|---------|------------|-------------|-----------------|
| api-prod-1       | m5.2xlarge  | 12%     | 28%        | m5.large     | $180            |
| worker-batch     | c5.4xlarge  | 8%      | 15%        | c5.xlarge    | $310            |
| analytics-db     | r5.4xlarge  | 22%     | 45%        | r5.2xlarge   | $520            |
```

### 4. Pricing Model Optimization

Evaluate the mix of on-demand, reserved, savings plans, and spot:

- **Stable baseline workloads**: Recommend 1-year or 3-year reservations. Calculate break-even point (typically 7-9 months for 1-year RI).
- **Variable workloads**: Recommend savings plans with a commitment level matching the floor of historical usage.
- **Fault-tolerant batch jobs**: Recommend spot instances with interruption handling. Document the spot vs on-demand discount (typically 60-80%).
- **Dev/test environments**: Recommend scheduling (stop nights/weekends) or spot-based environments.

### 5. Architecture-Level Optimizations

Identify structural changes that reduce cost:

- **Data transfer**: Move cross-AZ traffic to same-AZ where possible. Use VPC endpoints instead of NAT gateways for AWS service calls.
- **Storage tiering**: Move infrequently accessed data to cheaper tiers (S3 Infrequent Access, Glacier, or equivalent).
- **Compute model**: Evaluate containers (ECS/EKS) vs VMs for better bin-packing and utilization.
- **Caching**: Add caching layers to reduce database and API call volume.
- **Serverless migration**: Identify low-traffic services where serverless would eliminate idle compute costs.

### 6. Savings Roadmap

Prioritize recommendations by effort and impact. Use this format:

```
| Priority | Action                           | Monthly Savings | Effort   | Timeline  |
|----------|----------------------------------|----------------|----------|-----------|
| P0       | Delete orphaned EBS volumes      | $1,200         | 1 day    | This week |
| P0       | Schedule dev environments        | $3,800         | 2 days   | This week |
| P1       | Right-size top 10 instances      | $4,500         | 1 week   | 2 weeks   |
| P1       | Purchase 1-year RIs for baseline | $8,200         | 1 day    | 30 days   |
| P2       | Migrate logs to S3 IA tier       | $2,100         | 1 sprint | 60 days   |
| P2       | Move batch jobs to spot          | $5,600         | 2 sprints| 90 days   |
```

### 7. ROI Projection

Summarize the total opportunity:

- **Quick wins (0-2 weeks)**: Total monthly savings from P0 items
- **Medium-term (1-3 months)**: Cumulative savings including P1 items
- **Full realization (3-6 months)**: Total annual savings with all recommendations implemented
- **Implementation cost**: Engineering hours required, expressed in estimated cost

## Quality checklist

Before delivering the analysis, verify:

- [ ] Top 80% of spend is broken down by service with 3-month trends
- [ ] Every waste finding references a specific resource or resource group
- [ ] Right-sizing recommendations include current utilization data
- [ ] Pricing model recommendations include break-even calculations
- [ ] Savings roadmap has priorities, effort estimates, and timelines
- [ ] ROI projection includes implementation cost, not just savings
- [ ] Recommendations account for existing commitments and growth trajectory

## Common mistakes to avoid

- **Optimizing without utilization data.** Right-sizing based on instance type alone is guessing. Always require at least 14 days of CPU/memory metrics before recommending a downsize.
- **Ignoring data transfer costs.** These are often the fastest-growing line item and the hardest to spot. Always check cross-AZ, cross-region, and internet egress charges.
- **Recommending 3-year reservations without growth context.** A 3-year RI saves more per month but locks you in. If the workload might migrate to containers or serverless, prefer 1-year or convertible RIs.
- **Listing savings without effort estimates.** "$50K/year savings" means nothing if it requires 6 months of engineering work. Always pair savings with implementation cost.
- **Forgetting about non-production environments.** Dev, staging, and QA environments often run 24/7 but are only used during business hours. Scheduling alone can cut their cost by 65%.
