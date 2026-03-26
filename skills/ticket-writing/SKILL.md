---
name: ticket-writing
description: Write clear, well-scoped engineering tickets with acceptance criteria, technical context, effort estimates, and dependency mapping.
metadata:
  displayName: "Ticket Writing"
  categories: ["engineering"]
  tags: ["tickets", "jira", "linear", "project-management"]
  worksWellWithAgents: ["accessibility-auditor", "code-reviewer", "data-engineer", "database-architect", "debugger", "devops-engineer", "technical-pm"]
  worksWellWithSkills: ["accessibility-audit-report", "bug-report-writing", "code-review-checklist", "data-migration-plan", "incident-postmortem", "one-on-one-coaching", "prd-writing", "program-status-report", "release-checklist", "runbook-writing", "sprint-planning-guide", "sprint-retrospective", "test-plan-writing", "user-story-mapping"]
---

# Ticket Writing

## Before you start

Gather the following from the user:

1. **What needs to be built/changed?** (Feature, fix, refactor, or chore)
2. **Why?** (Link to PRD, user report, incident, or business goal)
3. **What's the tech stack?** (Languages, frameworks, database, hosting)
4. **What's the team context?** (How familiar is the team with this area of the codebase?)

If the user gives you a vague request ("write tickets for search"), push back: "What specific behavior should search have? What does the user see today vs. what should they see?"

## Ticket template

Use the following template for every ticket:

---

### Title

Use the format: `[Action verb] [specific thing] [context]`

**Good**: "Add rate limiting to /api/search endpoint (10 req/s per user)"
**Bad**: "Fix search" or "Search improvements" or "Rate limiting"

### Context

2-3 sentences explaining WHY this work matters. Link to the parent epic, PRD, or incident. The engineer should understand the business motivation without reading another document.

```
The /api/search endpoint currently has no rate limiting, which allowed a single
user to generate 50k requests in an hour last Tuesday (INC-234), degrading
search performance for all users. This ticket adds per-user rate limiting to
prevent abuse while maintaining normal usage patterns.
```

### Acceptance Criteria

Write specific, testable conditions. Use the format:

```
- [ ] Given [precondition], when [action], then [expected result]
- [ ] Given a user has made 10 requests in the last second,
      when they make an 11th request,
      then they receive a 429 response with a Retry-After header
- [ ] Given a user has been rate-limited,
      when the rate limit window expires,
      then their next request succeeds normally
- [ ] Rate limit configuration (requests per second, window size)
      is stored in environment variables, not hardcoded
```

Rules for acceptance criteria:
- Every criterion must be independently verifiable
- Include both the happy path AND edge cases
- Include error/failure states explicitly
- If there are performance requirements, state them with numbers

### Technical Notes

Point the engineer in the right direction without dictating the implementation:

```
Relevant files:
- `src/api/routes/search.ts` — endpoint handler
- `src/middleware/` — existing middleware patterns

Considerations:
- We use Redis for session storage; consider using it for rate limit
  counters too
- The existing auth middleware in `src/middleware/auth.ts` follows a
  pattern that could be adapted
- Check if the API gateway already provides rate limiting before
  implementing at the application level
```

### Effort Estimate

Provide a t-shirt size with reasoning:

```
Size: M (2-3 days)
Reasoning: The rate limiting logic itself is straightforward, but this
requires adding Redis counter logic, a new middleware, tests, and
updating API documentation. No schema changes needed.
```

### Dependencies

```
Blocked by: None
Blocks: SEARCH-456 (search performance monitoring — needs rate limiting in place first)
Related: SEARCH-123 (search index optimization — separate work, but same area)
```

---

## Ticket sizing guide

| Size | Duration | Characteristics |
|------|----------|----------------|
| **XS** | < 1 day | Config change, copy update, one-line fix with existing test coverage |
| **S** | 1-2 days | Single file/component change, clear implementation path, tests exist |
| **M** | 2-4 days | Multiple files, possibly new patterns, tests needed |
| **L** | 1-1.5 weeks | Crosses system boundaries, needs design decisions, may need migration |
| **XL** | > 1.5 weeks | **Should be broken down further.** If a ticket is XL, split it. |

## Splitting rules

A ticket should be split when:
- It has more than 5 acceptance criteria
- It crosses more than 2 system boundaries (e.g., frontend + API + database + background job)
- The estimate is L or larger
- Different parts could be worked on by different people in parallel

How to split:
1. **By layer**: Backend ticket + Frontend ticket + Migration ticket
2. **By behavior**: Happy path ticket + Error handling ticket + Edge cases ticket
3. **By user flow**: Create ticket + Read ticket + Update ticket + Delete ticket

Each sub-ticket must be independently deployable and valuable.

## Quality checklist

Before delivering tickets, verify:

- [ ] Title starts with an action verb and is specific enough to be understood without reading the body
- [ ] Context explains WHY, not just WHAT
- [ ] Every acceptance criterion is testable with a clear pass/fail condition
- [ ] Technical notes point to relevant files/patterns without dictating implementation
- [ ] Estimate includes reasoning, not just a size
- [ ] Dependencies are bidirectional (if A blocks B, B should note it's blocked by A)
- [ ] No ticket is estimated larger than L — split XL tickets
- [ ] Error states and edge cases are covered in acceptance criteria, not just happy paths

## Common mistakes to avoid

- **Acceptance criteria that are actually tasks**. "Implement the search function" is a task. "Given a query, when the user submits it, then results appear within 200ms" is a criterion.
- **Missing the "not" cases**. Always include what should NOT happen. "The system must NOT return results from deleted records" is as important as what it should return.
- **Context-free tickets**. If an engineer needs to read the PRD, the Slack thread, AND talk to the PM to understand the ticket, the ticket is missing context.
- **Implicit acceptance criteria**. "It should work like the existing search" is not a criterion. Spell out the specific behaviors, even if they match existing patterns.
- **Coupling unrelated work**. "Add rate limiting AND update the search algorithm" is two tickets. Don't bundle work that could fail independently.
