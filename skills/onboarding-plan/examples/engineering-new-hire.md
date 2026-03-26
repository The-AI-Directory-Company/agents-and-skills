# 90-Day Onboarding Plan: Software Engineer — Notifications Team

## Overview

```
Onboardee type:   New hire — Software Engineer (mid-level, L4)
Team:             Notifications, Consumer Product org
Timeline:         90 days (30-60-90 structure)
Onboarding owner: Priya Sharma (Engineering Manager) + Leo Park (buddy)
Success measure:  Ships a user-facing notification feature independently by Day 80
```

## Pre-Start Preparation

- **Access:** GitHub org, Datadog, PagerDuty, Slack (add to #notif-eng, #notif-oncall, #eng-all), Jira, Figma (view-only), AWS console (read-only). Provisioned by: IT — ticket INFRA-4821.
- **Equipment:** MacBook Pro 16", external monitor, headset — ordered via IT, ships to home address by Day -3.
- **Welcome packet:** Org chart, team README, architecture diagram link, calendar invites for all recurring meetings (standup, sprint planning, retro, 1:1).
- **Buddy:** Leo Park (senior engineer, same team). Available for daily questions, first 2 weeks.
- **First-week calendar:** Pre-scheduled — no empty blocks on Day 1.

## Milestone 1: Orientation (Days 1-7)

| Day   | Activity                                                  | Owner  | Success Criterion                              |
|-------|-----------------------------------------------------------|--------|-------------------------------------------------|
| 1     | Welcome 1:1 with Priya — role expectations, 90-day goals  | Priya  | Goals documented in shared doc                  |
| 1     | Dev environment setup with Leo                            | Leo    | Can build and run the notification service locally |
| 2     | Architecture walkthrough — event bus, delivery pipeline    | Leo    | Can whiteboard the notification delivery flow    |
| 3     | Codebase tour — repo structure, CI/CD, deploy process     | Leo    | Deploys a test change to staging successfully    |
| 4-5   | Read team docs — ADRs, runbooks, on-call playbook          | Self   | Notes 3+ questions for Leo                       |
| 5     | Meet with PM (Aya) and Designer (Marcus) — team priorities | Priya  | Understands current sprint goals                 |

## Milestone 2: Guided Contribution (Days 8-30)

| Week  | Activity                                                  | Owner  | Success Criterion                              |
|-------|-----------------------------------------------------------|--------|-------------------------------------------------|
| 2     | Pick up first "good-first-issue" — fix flaky test          | Priya  | PR submitted with passing CI                    |
| 2-3   | Pair programming with Leo (3 sessions/week)               | Leo    | New hire drives by session 4                     |
| 3     | Attend sprint planning and retro — observe, ask questions  | Self   | Can explain team's sprint process                |
| 4     | Ship first bug fix to production — email template rendering| Self   | Code reviewed, merged, monitored post-deploy     |
| 4     | **30-day check-in with Priya**                            | Priya  | Written feedback exchanged both directions       |

**30-day check-in questions:** What is going well? What is confusing? Is the pace right? What should we change for the next 30 days?

## Milestone 3: Independent Contribution (Days 31-60)

| Week  | Activity                                                  | Owner  | Success Criterion                              |
|-------|-----------------------------------------------------------|--------|-------------------------------------------------|
| 5-6   | Own a medium feature: add push notification opt-out preferences | Priya | Writes technical approach doc, gets feedback    |
| 6-7   | Review PRs for teammates (2-3 per week)                   | Self   | Provides substantive comments, not just approvals|
| 7-8   | Shadow on-call rotation — join Leo for 1 weekend shift     | Leo    | Can triage and respond to a low-severity alert   |
| 8     | **60-day check-in with Priya**                            | Priya  | Aligned on remaining ramp goals                  |

## Milestone 4: Full Ramp (Days 61-90)

| Week  | Activity                                                  | Owner  | Success Criterion                              |
|-------|-----------------------------------------------------------|--------|-------------------------------------------------|
| 9-10  | Ship push notification preferences feature end-to-end     | Self   | Scoped, built, tested, deployed independently    |
| 11    | Present "Notification Delivery Pipeline" to eng team       | Self   | Demonstrates understanding of system architecture|
| 12    | Join on-call rotation                                     | Priya  | Added to PagerDuty schedule                      |
| 12    | **90-day review with Priya**                              | Priya  | Formal assessment against 90-day goals           |

## Feedback Loops

- **Daily (Week 1):** 15-min sync with Leo. One question: "What is blocking you?"
- **Weekly (Weeks 2-4):** 30-min 1:1 with Priya. Review milestones, adjust pace.
- **Biweekly (Weeks 5-12):** Standard 1:1 cadence. Shift from onboarding to regular work topics.
- **Formal checkpoints:** Written feedback at Days 30, 60, and 90 from both sides.

At each checkpoint, ask: "What is one thing about this onboarding that should change for the next person?"
