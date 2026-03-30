# Onboarding Plan Example: B2B SaaS Customer Onboarding

This example applies the onboarding plan template to a non-engineering context — onboarding a new B2B customer onto a SaaS platform. The same milestone-based structure and feedback loops apply, with dimensions shifted to product adoption, stakeholder alignment, and time-to-value.

---

## Onboarding Overview

```
Onboardee type:   New customer — mid-market account (50-200 employees)
Product:          WorkflowPro (project management SaaS)
Timeline:         60 days (Week 1-2 setup, Week 3-6 adoption, Week 7-8 optimization)
Onboarding owner: Customer Success Manager (CSM) + assigned Technical Implementation Specialist
Success measure:  80% of licensed users active weekly by Day 45; customer-defined primary workflow running in production by Day 30
```

## Pre-Start Preparation

Complete before the customer's kickoff call:

- **Account provisioning:** Workspace created, SSO configured (if applicable), admin accounts set up. Do not make the customer wait on Day 1 for access.
- **Data migration assessment:** Review what data the customer needs to import (projects, users, historical records). Identify format, volume, and any cleanup required.
- **Stakeholder map:** Identify the executive sponsor, project lead (day-to-day contact), IT admin (SSO/integrations), and end-user champions. Document each person's role in the onboarding.
- **Success criteria alignment:** Before kickoff, confirm the customer's definition of success. "Rolled out to the team" is not specific enough — push for measurable outcomes like "all active projects tracked in WorkflowPro" or "weekly status reports generated from the platform."
- **Kickoff materials:** Prepare a customized agenda, a pre-configured demo workspace that mirrors their use case, and a timeline document the customer can share internally.

## Milestone-Based Progression

### Milestone 1: Setup & Configuration (Days 1-14)

| Day | Activity | Owner | Success Criterion |
|-----|----------|-------|--------------------|
| 1 | Kickoff call — align on goals, timeline, success criteria, stakeholder roles | CSM | Written success criteria signed off by executive sponsor |
| 1-3 | Workspace configuration — custom fields, project templates, permission roles | Tech Specialist | Configuration matches customer's workflow requirements |
| 3-5 | SSO and integration setup (Slack, Jira, email, calendar) | Tech Specialist + IT Admin | Users can log in via SSO; integrations send/receive data correctly |
| 5-7 | Data migration — import existing projects, users, and historical data | Tech Specialist | Customer verifies imported data accuracy and completeness |
| 7-10 | Admin training — workspace management, user provisioning, reporting | CSM | Admin can add users, create projects, and pull a report independently |
| 10-14 | Pilot group launch — 5-10 users begin using the platform for one real workflow | CSM + Project Lead | Pilot users complete at least one full workflow cycle in the platform |

**Day 14 checkpoint:** CSM and project lead review pilot feedback. Adjust configuration before wider rollout. Blockers must be resolved before proceeding.

### Milestone 2: Adoption & Rollout (Days 15-45)

| Week | Activity | Owner | Success Criterion |
|------|----------|-------|--------------------|
| 3 | End-user training sessions (2-3 cohorts based on team size) | CSM | Each cohort completes hands-on exercises; can perform core tasks |
| 3-4 | Full team rollout — all licensed users invited and onboarded | Project Lead + CSM | 90% of users have logged in at least once |
| 4 | Customer-defined primary workflow running in production | Project Lead | Workflow is actively used for real work, not just test data |
| 4-5 | Integration verification — confirm data flowing correctly at scale | Tech Specialist | No sync errors or data mismatches in production usage |
| 5-6 | Usage monitoring — identify inactive users and adoption blockers | CSM | Inactive users contacted; blockers documented and addressed |
| 6 | **Day 45 checkpoint with executive sponsor** | CSM | 80% weekly active user target met; sponsor confirms value |

### Milestone 3: Optimization & Handoff (Days 46-60)

| Week | Activity | Owner | Success Criterion |
|------|----------|-------|--------------------|
| 7 | Advanced feature training — reporting, automations, custom dashboards | CSM | Project lead can build a custom report and set up an automation |
| 7 | Best practices review — workflow refinements based on 30 days of usage data | CSM | At least 2 workflow adjustments identified and implemented |
| 8 | Onboarding retrospective — what worked, what didn't, NPS survey | CSM + Project Lead | Written feedback collected; NPS score recorded |
| 8 | Handoff to ongoing CSM relationship — transition from onboarding to BAU | CSM | Recurring check-in cadence established (monthly or quarterly) |
| 8 | **Day 60 formal review with executive sponsor** | CSM | Success criteria from kickoff reviewed; sponsor confirms production use |

## Feedback Loops

- **Daily (Week 1):** Slack channel or email thread with the project lead. One question: "What's blocking your team today?"
- **Weekly (Weeks 2-6):** 30-minute call with the project lead. Review adoption metrics, address user feedback, adjust the rollout plan.
- **Milestone checkpoints:** Formal written review at Day 14 (post-pilot), Day 45 (adoption target), and Day 60 (completion).
- **End-user pulse:** Short (3-question) survey sent to all users at Day 21 and Day 45. Questions: (1) Can you do your core work in the platform? (2) What's the most frustrating part? (3) What would make you use it more?

At each checkpoint, ask the project lead: "If a colleague at another company asked whether they should buy this product, what would you say right now?" The answer reveals unspoken friction that formal surveys miss.

## Common Failure Modes in Customer Onboarding

- **Skipping executive sponsor alignment.** If the sponsor does not define success criteria and check in at milestones, the project lead lacks organizational authority to drive adoption. Always get the sponsor on the kickoff and the Day 45 review.
- **Training without real workflows.** Training on demo data does not stick. Train users on their actual projects in their configured workspace. If the workspace is not ready, delay training.
- **Ignoring inactive users.** A 60% adoption rate at Day 30 will not fix itself. Proactively reach out to inactive users — they often have a fixable blocker (permissions, confusion, missing integration) that nobody reported.
- **Declaring success at launch.** Launch is Day 14. Success is Day 45 when users are actively working in the platform without being asked to. The period between launch and habit formation is where most onboardings fail.
