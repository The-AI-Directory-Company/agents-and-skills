# Sales Playbook: CloudSecure (Enterprise SaaS — Cloud Security Posture Management)

## Ideal Customer Profile

```
Firmographic Fit:
- Company size:   500-5,000 employees, $50M-$500M revenue
- Industry:       FinTech, HealthTech, SaaS — regulated or compliance-sensitive
- Tech stack:     AWS or GCP, Kubernetes in production, 3+ engineering teams

Behavioral Signals:
- Hiring for "Cloud Security Engineer" or "DevSecOps" roles
- Recently failed an audit or received SOC 2 findings
- Using open-source scanners (Prowler, ScoutSuite) but lacking centralized dashboards
- Visited pricing page twice or requested a demo

Disqualification Criteria:
- Fewer than 50 cloud workloads (below $30K ACV threshold)
- Locked into Wiz or Palo Alto Prisma contract with 18+ months remaining
- No compliance driver — security is deprioritized
```

## Qualification Framework (MEDDIC)

| Element          | Question to Answer                          | Evidence Required                        |
|------------------|---------------------------------------------|------------------------------------------|
| Metrics          | What compliance or security KPIs do they track? | "Reduce mean-time-to-remediate from 14 days to 48 hours" |
| Economic Buyer   | Who approves $30K-$150K security tooling?   | CISO or VP Engineering name confirmed    |
| Decision Criteria| What will they evaluate on?                 | Coverage, time-to-value, compliance mapping |
| Decision Process | What steps from eval to signed contract?    | POC, security review, legal, procurement |
| Identify Pain    | What is the cost of not solving this?       | "$200K audit remediation" or "2 engineers full-time on manual checks" |
| Champion         | Who is selling internally on our behalf?    | Can articulate why CloudSecure wins vs. build-your-own |

## Discovery Question Bank

**Pain:**
- "Walk me through what happens today when a misconfigured S3 bucket is detected."
- "How many hours per week does your team spend on manual compliance evidence collection?"
- "What happened during your last audit — were there findings that surprised you?"

**Decision Process:**
- "Who else needs to sign off on a security tool at this price point?"
- "What does your procurement timeline look like — is there a fiscal year deadline?"
- "Have you evaluated other CSPM tools before? What happened?"

**Budget:**
- "Is there budget allocated for cloud security tooling this year, or would this need a new request?"
- "Where does this rank against other security priorities this quarter?"

**Competition:**
- "Are you evaluating Wiz, Lacework, or Orca alongside us?"
- "Has your team considered building this with open-source scanners and a custom dashboard?"

## Objection Handling

**"Wiz covers everything you do."**
Acknowledge Wiz is a strong platform. Reframe: "Teams that switch to us from Wiz typically cite two gaps — Wiz's remediation workflows require manual Jira ticket creation, and their Kubernetes runtime coverage lags behind agentless scans by 6-12 hours. Would it be useful to run a side-by-side on your staging cluster?"

**"We can build this with Prowler + Grafana."**
Acknowledge the team's engineering strength. Reframe to total cost: "We see teams spend 3-4 months building a dashboard that covers 60% of compliance frameworks, then 1 FTE maintaining it ongoing. At $180K fully loaded, that is 3x our annual contract. Would it help to see a case study from a team that made the switch?"

**"Not a priority this quarter."**
Acknowledge timing. Ask: "What would move this up — a failed audit, a security incident, or a board-level mandate?" Quantify cost of waiting: "Each quarter without automated remediation is roughly 400 engineer-hours on manual checks." Set a reconnect tied to their audit cycle.

**"Your price is too high."**
Acknowledge pricing is a factor. Reframe to ROI: "You mentioned 2 engineers spending 20 hours/week on compliance checks — that is $190K/year. Our platform costs $85K and automates 80% of that work. Most customers see payback in 5 months." Offer a phased rollout to reduce year-one cost.

## Competitive Positioning

| Dimension       | CloudSecure             | Wiz                      | Orca Security            |
|-----------------|-------------------------|--------------------------|--------------------------|
| Best for        | Mid-market, compliance-first | Enterprise, broad coverage | Agentless-first orgs   |
| Pricing         | $30K-$150K/yr           | $100K-$500K+/yr          | $50K-$200K/yr            |
| Key strength    | Automated remediation + compliance mapping | Breadth of coverage | Agentless scanning speed |
| Key weakness    | Smaller partner ecosystem | High cost, long sales cycle | Weaker Kubernetes runtime |
| Landmine Q      | —                       | "How quickly can Wiz auto-remediate a finding without manual intervention?" | "How does Orca handle runtime threats in Kubernetes pods?" |
