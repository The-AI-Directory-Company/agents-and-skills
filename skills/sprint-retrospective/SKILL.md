---
name: sprint-retrospective
description: Run effective sprint retrospectives that produce actionable improvements — with facilitation formats, data gathering techniques, and experiment-based follow-through.
metadata:
  displayName: "Sprint Retrospective"
  categories: ["project-management"]
  tags: ["retrospective", "agile", "sprint", "continuous-improvement", "facilitation"]
  worksWellWithAgents: ["scrum-master"]
  worksWellWithSkills: ["ticket-writing"]
---

# Sprint Retrospective

## Before you start

Gather the following from the facilitator. If anything is missing, ask before proceeding:

1. **Sprint duration and dates** — What period are we reflecting on?
2. **Team size and composition** — How many participants? Are there remote members?
3. **Sprint goal and outcome** — Was the goal met, partially met, or missed?
4. **Key events** — Any incidents, launches, scope changes, or team changes during the sprint?
5. **Previous action items** — What did the team commit to last retro? Were they completed?
6. **Known tensions** — Any interpersonal or process friction the facilitator is aware of?

## Retrospective template

### 1. Review Previous Action Items (5 minutes)

Start every retro by reviewing last sprint's commitments. For each item:

```
Action Item: [Description]
Owner: [Name]
Status: Completed / In Progress / Not Started / Abandoned
Result: [What happened — measurable outcome if available]
```

If more than half of previous action items were not completed, address that pattern before gathering new data. Chronic non-completion means the team is overcommitting or under-prioritizing retro outcomes.

### 2. Choose a Facilitation Format

Select one format based on the team's current needs:

**Start/Stop/Continue** — Best for teams new to retros or when things are generally stable.
- Start: What should we begin doing?
- Stop: What should we stop doing?
- Continue: What is working and should not change?

**4Ls (Liked, Learned, Lacked, Longed For)** — Best when the team needs to reflect on growth. Four quadrants: what went well, what was discovered, what was missing, what was wished for.

**Mad/Sad/Glad** — Best when there is emotional tension or team morale is a concern. Surfaces feelings before jumping to process fixes.

**Timeline** — Best after a complex sprint with many events. Plot events chronologically, then annotate with energy levels and observations.

Rotate formats every 3-4 sprints to prevent staleness. Never use the same format more than 3 times in a row.

### 3. Gather Data (10 minutes)

Rules for data gathering:

- Silent writing first — 5 minutes of individual brainstorming before any discussion
- One observation per sticky note or card — no compound statements
- Facts over feelings where possible: "Deploys took 45 minutes on average" beats "deploys were slow"
- Include specific examples: "The payments API had 3 unplanned outages" not "reliability was bad"

### 4. Group and Discuss (15 minutes)

Cluster related observations into themes. Common theme categories:

- **Process**: Planning, estimation, standup effectiveness, deployment workflow
- **Technical**: Code quality, testing, tooling, tech debt, architecture
- **Communication**: Cross-team coordination, documentation, handoffs, meetings
- **People**: Workload distribution, skill gaps, onboarding, morale

For each theme, facilitate discussion with these questions:
- What is the root cause, not just the symptom?
- Is this within our control to change?
- How would we know if it got better?

### 5. Vote and Prioritize (5 minutes)

Each team member gets 3 votes (dot voting). Vote on themes, not individual observations.

Take the top 2-3 themes only. Teams that try to fix everything fix nothing.

### 6. Define Experiments (10 minutes)

Convert each prioritized theme into a concrete experiment using this format:

```
Theme: [The problem area]
Hypothesis: If we [specific change], then [expected outcome], measured by [metric].
Experiment: [Exact action to take]
Owner: [Single person responsible — not "the team"]
Duration: [How long to run the experiment — usually 1-2 sprints]
Success Criteria: [How we will know it worked]
```

**Good experiment**: "If we add a 15-minute deploy verification step after each release, then we will catch issues before users do, measured by reducing user-reported post-deploy bugs from 4/sprint to 1/sprint. Owner: Sarah. Duration: 2 sprints."

**Bad experiment**: "We should deploy better." (No hypothesis, no metric, no owner, no timeline.)

### 7. Document and Share

Record the retro output covering: sprint name/dates, participants, sprint goal status, previous action item outcomes, top themes with discussion summaries, and new experiments in full format from Step 6.

Share with the team within 24 hours. Stale retro notes lose their impact.

## Quality checklist

Before closing the retrospective, verify:

- [ ] Previous action items were reviewed with explicit status updates
- [ ] Data gathering included silent individual writing before group discussion
- [ ] Themes are based on specific observations, not vague feelings
- [ ] No more than 3 experiments were committed to
- [ ] Each experiment has a single owner (not "the team"), a duration, and a measurable success criterion
- [ ] The retro document is written and ready to share within 24 hours
- [ ] The team agreed on when experiments will be reviewed (usually next retro)

## Common mistakes

- **Skipping the review of previous action items.** If last sprint's commitments are never revisited, the team learns that retro outcomes do not matter. Always start with accountability.
- **Letting one voice dominate.** Silent writing before discussion ensures introverts contribute. If one person talks for 5 minutes straight, the facilitator must redirect.
- **Turning themes into blame.** "Deploys were slow because DevOps did not prioritize our tickets" is blame. "Our deploy pipeline averages 45 minutes — what can WE change?" is actionable.
- **Committing to too many actions.** Three experiments is the maximum. Teams that commit to seven items complete zero. Fewer commitments, higher follow-through.
- **Vague action items without owners.** "Improve documentation" will not happen. "Sarah will write a deployment runbook for the payments service by March 28" will.
- **Running the same format every sprint.** Repetition causes autopilot. Rotate formats to surface different kinds of observations.
