---
name: user-story-mapping
description: Create user story maps that break down complex features into shippable slices with clear user journeys, activities, tasks, and release planning.
metadata:
  displayName: "User Story Mapping"
  categories: ["product-management"]
  tags: ["user-stories", "story-mapping", "agile", "planning"]
  worksWellWithAgents: ["business-analyst", "product-designer", "scrum-master", "ui-designer", "ux-researcher"]
  worksWellWithSkills: ["prd-writing", "sprint-planning-guide", "stakeholder-interview", "ticket-writing"]
---

# User Story Mapping

## Before you start

Gather the following from the user:

1. **What product/feature area** are we mapping?
2. **Who are the users?** (List specific personas or segments, not "users")
3. **What is the goal?** (Are we mapping for an MVP? A new feature? A redesign?)
4. **What constraints exist?** (Timeline, team size, technical limitations)

If the user gives you a vague scope ("map our product"), narrow it: "Which user journey should we focus on first?"

## Step 1: Identify the backbone (Activities)

Activities are the high-level things users do. They read left-to-right as a narrative.

Rules for activities:
- Use verb phrases: "Discover agents", "Configure workspace", "Monitor performance"
- Keep to 4-8 activities for a single feature area
- Order them chronologically as the user would experience them
- Each activity should be completable in one session

```
[Discover agents] → [Evaluate agent] → [Install agent] → [Configure agent] → [Monitor usage]
```

## Step 2: Break activities into tasks

Each activity contains 2-5 tasks. Tasks are the steps a user takes within an activity.

Rules for tasks:
- Tasks are smaller verb phrases: "Search catalog", "Read reviews", "Compare options"
- Order them top-to-bottom by typical sequence
- Every task should map to an observable user action

```
Activity: Discover agents
├── Search catalog
├── Browse categories
├── View trending
└── Read recommendations
```

## Step 3: Generate stories under each task

Stories are the specific, implementable items. Write them in standard format:

> As a [persona], I want [action] so that [outcome].

Rules for stories:
- Each story must be independently deliverable
- Each story must be testable (you can write an acceptance criterion)
- Avoid technical stories at this stage — frame everything from the user's perspective
- It's okay to have 3-10 stories per task

```
Activity: Discover agents
├── Task: Search catalog
│   ├── As a developer, I want to search agents by keyword so that I can find relevant tools quickly
│   ├── As a developer, I want to filter search results by category so that I can narrow down options
│   └── As a developer, I want to see search results ranked by relevance so that the best matches appear first
```

## Step 4: Draw the release slices

Slice the map horizontally. Each slice is a shippable release.

**Slice 1 (Walking Skeleton / MVP)**:
- Pick the ONE story from each task that delivers the minimum end-to-end experience
- The user should be able to complete the entire journey, even if each step is bare-bones
- This slice should be shippable in 1-2 sprints

**Slice 2 (v1.0)**:
- Add the stories that make the experience good, not just functional
- Better search, richer detail pages, smoother flows

**Slice 3+ (Future)**:
- Everything else. Nice-to-haves, power user features, optimizations

Rules for slicing:
- Every slice must be independently shippable and valuable
- The walking skeleton must include at least one story from each critical activity
- Don't put all the "easy" stories in slice 1 — put the most valuable ones

## Output format

Present the final story map in this structure:

```
# Story Map: [Feature/Product Name]

## Personas: [List them]

---

### Activity: [Name]

#### Task: [Name]
- [MVP] Story description
- [v1.0] Story description
- [Future] Story description

#### Task: [Name]
- [MVP] Story description
- [v1.0] Story description

---

### Activity: [Name]
...
```

## Quality checklist

Before delivering a story map, verify:

- [ ] Activities read left-to-right as a coherent user narrative
- [ ] Every activity has 2-5 tasks
- [ ] Every story is independently deliverable and testable
- [ ] The MVP slice delivers a complete (if minimal) end-to-end journey
- [ ] No slice contains only backend/technical work with no user-facing value
- [ ] Stories are framed from the user's perspective, not technical tasks
- [ ] The map has been reviewed against the stated personas — does each persona have a clear path?

## Common mistakes to avoid

- **Starting with stories instead of activities**. Always build the backbone first. Stories without a backbone are just a flat backlog.
- **MVP that's too thick**. The walking skeleton should be embarrassingly thin. If your MVP has more than 2 stories per task, you're not cutting enough.
- **Confusing tasks with stories**. "Search catalog" is a task. "As a developer, I want to search by keyword" is a story. Tasks are categories; stories are deliverables.
- **Leaving out the "return" journey**. Users don't just complete a flow once. Map what happens when they come back: re-evaluate, update, remove, monitor.
