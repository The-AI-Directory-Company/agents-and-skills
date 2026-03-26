# Go-to-Market Plan: Launchpad API (Developer Tool)

## Positioning Statement

```
For backend engineering teams at mid-market SaaS companies (50-500 employees)
who spend 15+ hours per sprint building and maintaining internal deployment pipelines,
Launchpad API is a deployment orchestration API
that lets teams ship to any cloud provider with a single API call and built-in rollback.
Unlike Terraform and Pulumi, which require dedicated infrastructure engineers,
we eliminate the IaC learning curve so application developers deploy directly.
```

## Target Segments

| Priority | Segment                          | Size Estimate  | Why First?                                    |
|----------|----------------------------------|----------------|-----------------------------------------------|
| P0       | Backend teams at Series B-C SaaS | ~6,000 cos     | Acute pain, budget authority, fast eval cycle  |
| P1       | Platform engineering teams       | ~2,500 cos     | High ACV ($25K+), strong community influence   |
| P2       | Solo developers & indie hackers  | ~80,000 ind    | Volume for brand awareness, low ACV            |

**P0 discovery:** Technical blog posts, Hacker News, engineering podcasts. Evaluate via docs and free tier. Engineering manager or VP Eng signs off.
**P1 discovery:** Conference talks, peer referrals, infrastructure Slack communities. Evaluate via POC with solutions engineer. Director of Platform signs off.

## Channel Strategy

| Channel               | Segment | Goal       | Tactic                                          | Budget   |
|------------------------|---------|------------|-------------------------------------------------|----------|
| Technical content      | P0, P1  | Awareness  | Weekly blog: deployment patterns, migration guides | $4K/mo  |
| Developer communities  | P0, P2  | Adoption   | Hacker News launches, Reddit r/devops, Discord   | Time     |
| Conference sponsorships| P1      | Pipeline   | KubeCon, PlatformCon — booth + talk submission   | $18K/qtr |
| Outbound sales         | P1      | Pipeline   | Targeted outreach to platform eng hiring signals | $12K/mo  |
| Product Hunt           | P0, P2  | Launch spike| Coordinated launch with demo video               | $1.5K    |

**Content owner:** Sarah M. (DevRel Lead)
**Outbound owner:** James T. (Head of Sales)

## Pricing Context

```
Model:              Freemium with usage-based pricing
Free tier:          Up to 500 deployments/month, 1 environment, community support
Pro tier:           $0.05/deployment + $99/mo base — unlimited environments, Slack support
Enterprise:         Custom — SSO, audit logs, SLAs, dedicated solutions engineer
Competitive anchor: Vercel ($20/user/mo for teams), Render ($19/service/mo), Terraform Cloud (free to $70/user)
```

## Launch Timeline

| Phase         | Dates         | Key Activities                                       | Owner    | Milestone                  |
|---------------|---------------|------------------------------------------------------|----------|----------------------------|
| Pre-launch    | Mar 3 - Mar 28| Positioning finalized, docs site, beta invites sent  | Sarah M. | 400 waitlist signups       |
| Private beta  | Mar 31 - Apr 11| 50 beta teams onboarded, feedback collected          | Product  | 30 active teams, NPS > 35  |
| Public launch | Apr 14        | PH, blog post, HN, email blast, social               | Sarah M. | 800 signups in first week  |
| Post-launch   | Apr 15 - Jun 6| Content cadence, outbound to P1, funnel optimization | James T. | 40 SQLs, 8% free-to-paid   |

## Success Metrics

| Metric                     | Phase         | Target              | Measured By        |
|----------------------------|---------------|----------------------|--------------------|
| Waitlist signups           | Pre-launch    | 400                  | Landing page       |
| Beta activation rate       | Private beta  | 60% complete first deployment | Product analytics |
| Week-1 signups             | Public launch | 800                  | Analytics          |
| Free-to-paid conversion    | Post-launch   | 8% within 30 days    | Billing data       |
| Sales qualified leads      | Post-launch   | 40 in first 8 weeks  | CRM                |
| Customer acquisition cost  | Post-launch   | < $200               | Finance            |

**If activation rate falls below 40%:** Pause acquisition spend and run 10 user interviews to identify onboarding friction. Fix before resuming.
**If free-to-paid conversion is below 5%:** Test value-gating strategies — e.g., limit free-tier rollback history to 7 days.
