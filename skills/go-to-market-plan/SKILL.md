---
name: go-to-market-plan
description: Write go-to-market plans with positioning, target segments, channel strategy, pricing context, launch timeline, and success metrics — connecting product value to market execution.
metadata:
  displayName: "Go-to-Market Plan"
  categories: ["business"]
  tags: ["go-to-market", "launch", "positioning", "channels", "marketing", "strategy"]
  worksWellWithAgents: ["marketing-strategist", "pricing-strategist", "vp-product"]
  worksWellWithSkills: ["metrics-framework", "prd-writing", "product-launch-brief"]
---

# Go-to-Market Plan

## Before you start

Gather the following from the user. If anything is missing, ask before proceeding:

1. **What are you launching?** (New product, feature, pricing change, market expansion)
2. **Who is the target customer?** (Persona, company size, industry, current alternatives)
3. **What problem does it solve?** (Pain point in the customer's words, not your feature list)
4. **What is the competitive landscape?** (Direct competitors, indirect alternatives, status quo)
5. **What is the pricing model?** (Free, freemium, paid tiers, enterprise — even if tentative)
6. **What is the launch timeline?** (Hard date, flexible window, phased rollout)
7. **What resources are available?** (Budget, team size, existing channels)

If the user says "we just need to get the word out," push back: getting the word out without positioning, segments, and channels defined is noise, not strategy.

## Go-to-market plan template

### 1. Positioning Statement

Write the positioning in this format. If you cannot fill every field, the positioning is not ready.

```
For [target customer]
who [need or pain point],
[Product name] is a [category]
that [key benefit].
Unlike [primary alternative],
we [key differentiator].
```

Test the positioning by asking: could a competitor copy this statement word-for-word? If yes, the differentiator is too generic. Sharpen it until it describes only your product.

### 2. Target Segments

Define 2-3 segments ranked by priority. Do not launch to everyone at once.

```
| Priority | Segment              | Size Estimate | Why First?                         |
|----------|-----------------------|---------------|------------------------------------|
| P0       | DevOps teams (50-200) | ~8,000 cos    | Highest pain, shortest sales cycle |
| P1       | Platform engineers    | ~3,000 cos    | High ACV, strong word-of-mouth     |
| P2       | Freelance developers  | ~50,000 ind   | Volume play, lower priority        |
```

For each segment: How do they discover tools? What do they evaluate? Who signs the check?

### 3. Channel Strategy

Map channels to segments. Not every channel works for every segment.

```
| Channel              | Segment | Goal        | Tactic                          | Budget  |
|----------------------|---------|-------------|---------------------------------|---------|
| Content marketing    | P0, P1  | Awareness   | Technical posts, comparison guides| $5K/mo|
| Developer communities| P0      | Adoption    | HN, Reddit, Discord engagement  | Time    |
| Outbound sales       | P1      | Pipeline    | Targeted outreach to leads      | $15K/mo |
| Product Hunt         | P0, P2  | Launch spike| Coordinated launch day          | $2K     |
```

For each channel, define: content/action, owner, expected volume, and success measure.

### 4. Pricing Context

Summarize the pricing approach and how it connects to the GTM motion. Full pricing analysis is a separate skill — here you need enough to align the launch.

```
Model:              Freemium with usage-based upgrade triggers
Free tier:          Up to 3 projects, 1 user, community support
Paid tier:          $49/user/month — unlimited projects, team features
Enterprise:         Custom — SSO, audit logs, dedicated support, SLAs
Competitive anchor: Competitor A at $65/user, Competitor B open-source + paid cloud
```

### 5. Launch Timeline

Break the launch into phases with owners and milestones.

```
| Phase        | Dates      | Key Activities                                  | Owner     | Milestone              |
|--------------|------------|------------------------------------------------|-----------|------------------------|
| Pre-launch   | Weeks 1-4  | Positioning, landing page, beta onboarding     | Marketing | 500 waitlist signups   |
| Soft launch  | Weeks 5-6  | Open waitlist, gather feedback, fix issues      | Product   | 100 active, NPS > 30   |
| Public launch| Week 7     | PH, blog, email, social, outbound to P1        | Marketing | 1,000 signups in week 1|
| Post-launch  | Weeks 8-12 | Content cadence, sales ramp, funnel iteration  | Sales     | 50 SQLs, 10% conversion|
```

### 6. Success Metrics

Define metrics for each launch phase. Separate leading indicators (activity) from lagging indicators (outcomes).

```
| Metric                    | Phase        | Target           | Measured By     |
|---------------------------|-------------|------------------|-----------------|
| Waitlist signups          | Pre-launch  | 500              | Landing page    |
| Activation rate           | Soft launch | 60% complete setup| Product analytics|
| Week-1 signups            | Public launch| 1,000           | Analytics       |
| Free-to-paid conversion   | Post-launch | 10% within 30 days| Billing data   |
| Sales qualified leads     | Post-launch | 50 in first month| CRM             |
| Customer acquisition cost | Post-launch | < $150           | Finance         |
```

Review metrics weekly during launch, monthly afterward. If activation rate is below target, fix onboarding before spending more on acquisition — pouring users into a leaky funnel wastes budget.

## Quality checklist

Before delivering a go-to-market plan, verify:

- [ ] Positioning is specific enough that a competitor cannot reuse it verbatim
- [ ] Target segments are prioritized with clear reasons for ranking
- [ ] Channel strategy maps channels to segments with owners and budgets
- [ ] Pricing context is included so the launch plan is internally consistent
- [ ] Launch timeline has phases, owners, and measurable milestones
- [ ] Success metrics separate leading indicators from lagging outcomes
- [ ] Every channel and phase has a named owner — a person, not a team
- [ ] The plan addresses what happens if early metrics miss targets

## Common mistakes to avoid

- **Positioning by feature list.** "We have SSO, audit logs, and a CLI" is not positioning. Positioning answers why a customer should choose you — features are evidence, not the argument.
- **Targeting everyone.** A GTM plan for "all developers" will reach no one. Narrow the initial segment until it feels uncomfortably small.
- **Channel strategy without capacity.** Listing 8 channels with a 2-person team guarantees all 8 done poorly. Pick 2-3, execute well, then expand.
- **Skipping pre-launch validation.** Launching without beta feedback means debugging product-market fit in public.
- **Metrics without action triggers.** Define what number is good, what is bad, and what changes if you hit the bad number.
- **Confusing launch with growth.** A launch plan covers weeks 1-12. Growth is what happens after. Plan the transition to steady-state channels.
