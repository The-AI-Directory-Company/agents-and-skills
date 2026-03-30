---
name: onboarding-plan
description: Design structured onboarding plans — for new hires, new customers, or new users — with milestone-based progression, success criteria, and feedback loops.
metadata:
  displayName: "Onboarding Plan"
  categories: ["leadership", "business"]
  tags: ["onboarding", "new-hire", "ramp-up", "training", "customer-onboarding"]
  worksWellWithAgents: ["codebase-onboarder", "customer-success-manager", "instructional-designer", "people-ops-manager", "technical-writer"]
  worksWellWithSkills: ["employee-handbook-section", "one-on-one-coaching", "training-curriculum"]
---

# Onboarding Plan

## Before you start

Gather the following from the user:

1. **Who is being onboarded?** (New hire, new customer, or new user — and their role/persona)
2. **What does "fully ramped" look like?** (3-5 concrete outcomes that indicate onboarding is complete)
3. **What is the expected ramp timeline?** (30 days, 60 days, 90 days)
4. **Who is responsible for the onboarding?** (Manager, buddy, CSM, or self-guided)
5. **What existing resources are available?** (Documentation, training videos, sandbox environments, mentors)

If the user says "we just need a checklist," push back: "A checklist gets tasks done but doesn't ensure understanding. What should this person be able to do independently by the end of onboarding?"

## Onboarding plan template

### 1. Onboarding Overview

Define the onboarding scope in a brief summary.

```
Onboardee type:   New hire — Senior Frontend Engineer
Team:             Consumer Products
Timeline:         90 days (30-60-90 structure)
Onboarding owner: Engineering Manager + assigned buddy
Success measure:  Ships first production feature independently by Day 75
```

### 2. Pre-Start Preparation

Complete before the onboardee's first day:

- **Access provisioning**: List every system, tool, and repo they need access to. Include account names and who provisions each one.
- **Equipment setup**: Laptop, monitors, peripherals — ordered and configured.
- **Welcome packet**: Team org chart, key contacts, calendar invites for recurring meetings, links to onboarding docs.
- **Buddy assignment**: Assign a peer (not the manager) who is available for daily questions during the first two weeks.
- **First-week calendar**: Pre-schedule all Day 1-5 meetings and activities. An empty calendar on Day 1 signals disorganization.

### 3. Milestone-Based Progression

Structure the plan into milestones, not a flat task list. Each milestone has a clear success criterion.

**Milestone 1: Orientation (Days 1-7)**

| Day | Activity | Owner | Success Criterion |
|-----|----------|-------|--------------------|
| 1 | Welcome meeting with manager — role expectations, 90-day goals | Manager | Goals documented and shared |
| 1 | Dev environment setup with buddy | Buddy | Can build and run the app locally |
| 2 | Architecture walkthrough — system overview, key services | Tech lead | Can draw the high-level architecture from memory |
| 3 | Codebase tour — repo structure, CI/CD pipeline, deployment process | Buddy | Successfully deploys a test change to staging |
| 4-5 | Read team docs — ADRs, runbooks, on-call playbook | Self | Completes reading, notes questions for buddy |

**Milestone 2: Guided Contribution (Days 8-30)**

| Week | Activity | Owner | Success Criterion |
|------|----------|-------|--------------------|
| 2 | Pick up first "good first issue" ticket | Manager | PR submitted with tests |
| 2-3 | Pair programming sessions (2-3 per week) | Buddy | Onboardee drives, buddy observes |
| 3 | Attend sprint planning and retro — observe, don't commit yet | Self | Understands team process |
| 4 | Ship first bug fix or small feature to production | Self | Code reviewed and merged |
| 4 | **30-day check-in with manager** | Manager | Written feedback exchanged both ways |

**Milestone 3: Independent Contribution (Days 31-60)**

| Week | Activity | Owner | Success Criterion |
|------|----------|-------|--------------------|
| 5-6 | Own a medium-sized feature end-to-end | Manager | Writes own technical approach, gets feedback |
| 6-7 | Participate in code review for others | Self | Provides substantive review comments |
| 7-8 | Shadow on-call rotation (if applicable) | On-call lead | Can handle a low-severity alert independently |
| 8 | **60-day check-in with manager** | Manager | Aligned on remaining ramp goals |

**Milestone 4: Full Ramp (Days 61-90)**

| Week | Activity | Owner | Success Criterion |
|------|----------|-------|--------------------|
| 9-10 | Ship a production feature independently | Self | Scoped, built, tested, deployed without hand-holding |
| 10-11 | Present a technical topic to the team | Self | Demonstrates domain understanding |
| 12 | Join on-call rotation (if applicable) | Manager | Added to rotation schedule |
| 12 | **90-day review** | Manager | Formal assessment against 90-day goals |

### 4. Feedback Loops

Build feedback into the plan — don't wait for the end.

- **Daily (Week 1)**: 15-minute buddy check-in. One question: "What's blocking you?"
- **Weekly (Weeks 2-4)**: 30-minute 1:1 with manager. Review progress against milestones.
- **Biweekly (Weeks 5-12)**: Standard 1:1 cadence. Shift from onboarding topics to regular work.
- **Formal checkpoints**: Written feedback at 30, 60, and 90 days. Both sides share what's working and what isn't.

At each checkpoint, ask the onboardee: "What's one thing about the onboarding that should change for the next person?"

## Quality checklist

Before delivering the plan, verify:

- [ ] Every milestone has measurable success criteria, not just activities
- [ ] Pre-start preparation is complete — no "figure it out on Day 1" gaps
- [ ] A buddy is assigned and their responsibilities are documented
- [ ] Feedback checkpoints are scheduled at 30, 60, and 90 days
- [ ] The plan distinguishes between "do this task" and "be able to do this independently"
- [ ] Access provisioning lists specific systems, not "request access as needed"
- [ ] The 90-day completion criteria define what "fully ramped" means concretely

## Common mistakes to avoid

- **Task lists without success criteria.** "Read the architecture docs" is a task. "Can draw the system architecture from memory and explain data flow" is a success criterion. Every activity needs a way to verify understanding.
- **No buddy assignment.** Managers are too busy for daily questions. A buddy at the same level provides low-friction support. Assign one explicitly and protect their time.
- **Information firehose on Day 1.** Spreading 8 hours of presentations across the first day guarantees nothing is retained. Limit Day 1 to setup, one key meeting, and one hands-on activity.
- **No feedback until 90 days.** If something is off at Week 2, waiting until Day 90 wastes everyone's time. Build in explicit checkpoints at 30 and 60 days with written feedback.
- **Treating onboarding as one-size-fits-all.** A senior hire needs less hand-holding on tools but more context on team dynamics and decision history. Adjust the plan to the person's level and background.
