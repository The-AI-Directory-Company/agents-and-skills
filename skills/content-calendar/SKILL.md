---
name: content-calendar
description: Plan and manage content production with editorial calendars — defining themes, channels, cadence, ownership, and measurement for consistent, strategic content delivery.
metadata:
  displayName: "Content Calendar"
  categories: ["communication", "business"]
  tags: ["content", "editorial", "calendar", "planning", "publishing"]
  worksWellWithAgents: ["content-strategist", "developer-advocate", "email-marketer", "social-media-manager", "technical-writer"]
  worksWellWithSkills: ["content-sgeo", "email-campaign-writing", "prd-writing", "social-media-content-plan", "stakeholder-interview"]
---

# Content Calendar

## Before you start

Gather the following from the user:

1. **What are the business goals for content?** (Lead generation, brand awareness, developer adoption, SEO, customer education)
2. **Who is the target audience?** (Personas, job titles, experience levels)
3. **What channels will you publish on?** (Blog, newsletter, social media, YouTube, docs, podcast)
4. **What is the publishing cadence?** (Weekly, biweekly, monthly — per channel)
5. **Who creates and approves content?** (Writers, reviewers, editors, subject matter experts)
6. **What planning horizon?** (Monthly, quarterly)

If the user says "we need to post more content," push back: "More content without a theme or audience in mind creates noise, not value. What specific outcome should content drive in the next quarter?"

## Content calendar template

### 1. Content Strategy Summary

Anchor the calendar to strategy before filling in dates.

```
Planning period:    Q2 2025 (April - June)
Primary goal:       Increase developer signups by 25%
Target audience:    Backend engineers evaluating API platforms
Channels:           Blog (2x/month), Newsletter (weekly), Twitter (daily)
Content pillars:    1. Technical tutorials  2. Case studies  3. Engineering culture
Success metrics:    Blog traffic, newsletter open rate, signup conversions
```

### 2. Content Pillars and Themes

Define 3-5 pillars that all content maps to. Each pillar supports the business goal.

```
| Pillar               | Description                              | % of Content | Goal Alignment           |
|----------------------|------------------------------------------|-------------|--------------------------|
| Technical tutorials  | Step-by-step guides solving real problems | 40%         | Developer trust + SEO    |
| Case studies         | Customer stories with measurable results | 25%         | Social proof + leads     |
| Engineering culture  | How we build — process, values, lessons  | 20%         | Employer brand + trust   |
| Product updates      | Feature launches, changelog highlights   | 15%         | Retention + adoption     |
```

### 3. Monthly Calendar View

For each month, plan content at the title level with key metadata.

```
## April 2025

| Week | Date       | Channel    | Title                                      | Pillar     | Owner       | Status   |
|------|------------|------------|-------------------------------------------|------------|-------------|----------|
| 1    | Apr 1      | Blog       | "Building a Rate Limiter in Go"           | Tutorial   | @alice      | Draft    |
| 1    | Apr 3      | Newsletter | Weekly digest: rate limiting + API news   | Mixed      | @bob        | Planned  |
| 2    | Apr 8      | Blog       | "How Acme Cut API Latency by 60%"         | Case study | @carol      | Outline  |
| 2    | Apr 10     | Newsletter | Weekly digest: performance case study     | Mixed      | @bob        | Planned  |
| 3    | Apr 15     | Blog       | "Our Approach to On-Call Rotations"       | Culture    | @dave       | Idea     |
| 3    | Apr 17     | Newsletter | Weekly digest: on-call + community recap  | Mixed      | @bob        | Planned  |
| 4    | Apr 22     | Blog       | "v2.3 Release: Batch Endpoints"           | Product    | @eve        | Planned  |
| 4    | Apr 24     | Newsletter | Weekly digest: new features roundup       | Mixed      | @bob        | Planned  |
```

### 4. Content Production Workflow

Define the stages every piece of content moves through, with owners and SLAs.

```
Stage 1: Idea          → Proposed in content backlog with pillar tag and audience
Stage 2: Outline       → Structured outline approved by editor (2 business days)
Stage 3: Draft         → Full draft written by author (5 business days)
Stage 4: Review        → Technical review by SME + editorial review (3 business days)
Stage 5: Final edits   → Author incorporates feedback (2 business days)
Stage 6: Publish       → Scheduled and published on target date
Stage 7: Promote       → Shared on social channels, newsletter, community
Stage 8: Measure       → Performance reviewed 14 days after publish
```

Total lead time: **14 business days** from outline approval to publish. Work backwards from the publish date to set deadlines.

### 5. Measurement Framework

Define how you'll evaluate content performance. Review metrics monthly.

```
| Metric                    | Target        | Measured At      |
|---------------------------|---------------|------------------|
| Blog pageviews            | 10K/month     | Google Analytics |
| Newsletter open rate      | >40%          | Email platform   |
| Newsletter click rate     | >8%           | Email platform   |
| Content → signup rate     | >2%           | Attribution tool |
| Social engagement rate    | >3%           | Social analytics |
| Publish consistency       | 100% on-time  | Calendar audit   |
```

## Quality checklist

Before finalizing the calendar, verify:

- [ ] Every piece of content maps to a content pillar
- [ ] Each pillar is connected to a business goal, not just "it'd be nice to write about"
- [ ] Every item has an owner and a status
- [ ] The production workflow has realistic SLAs that work backwards from publish dates
- [ ] Publish cadence is sustainable given the team's capacity
- [ ] Measurement metrics are defined and attributed to specific tools
- [ ] The backlog is prioritized, not just a dumping ground of ideas
- [ ] At least one month is planned at the title level, not just themes

## Common mistakes to avoid

- **Planning content without a strategy.** A calendar full of titles with no content pillars or audience definition is just a to-do list. Start with goals and pillars, then fill in titles.
- **Overcommitting on cadence.** Publishing daily when you have one writer guarantees burnout and declining quality. Set a cadence the team can sustain for 6+ months, then increase.
- **No owner per piece.** "The marketing team" is not an owner. Every content item needs one person responsible for moving it from idea to published.
- **Skipping the measurement step.** If you never review what performed well, you'll keep producing content that doesn't work. Build a monthly review into the calendar itself.
- **Treating all channels the same.** A blog post is not a tweet is not a newsletter. Adapt format, tone, and length to each channel — don't just cross-post the same text everywhere.
