# Section-by-Section Guide

Detailed guidance for writing each section of an agent definition file.

## Section ordering and purpose

The section order is intentional. It follows how experts actually think about their work:

1. **Identity** (opening paragraph) — Who am I?
2. **Perspective** — How do I see the world?
3. **Method** — How do I work?
4. **Communication** — How do I interact with others?
5. **Decision-making** — How do I handle tradeoffs?
6. **Boundaries** — What do I refuse to do?
7. **Scenarios** — How do I handle specific situations?

This mirrors Anthropic's "right altitude" principle: start with the high-level mental model, then add specificity layer by layer. The agent loads identity first, then progressively applies more detailed guidance.

## 1. Opening paragraph

**Length:** 1-3 sentences
**Purpose:** Establish identity, experience level, and core worldview in the most token-efficient way possible

**Structure:** `You are a [role] with [experience qualifier]. You [core perspective].`

The experience qualifier matters because it sets the tone for everything that follows. "A junior developer" and "a staff engineer with 15 years across multiple codebases" produce dramatically different agent behaviors.

**Effective openers by domain:**

| Domain | Example |
|--------|---------|
| Engineering | "You are a senior security auditor who has reviewed hundreds of production systems. You think like an attacker first, then a defender." |
| Product | "You are a VP of Product with 15+ years at high-growth startups. You obsess over user problems and business impact, not feature checklists." |
| Leadership | "You are an Engineering Manager who was a senior IC before moving to management. You understand code deeply but your job is now people and systems, not pull requests." |
| Data | "You are a data engineer who builds pipelines that other teams depend on. You think in terms of data contracts, not just schemas." |

## 2. "Your perspective" section

**Length:** 3-5 bullet points
**Purpose:** Install the agent's mental models — the lenses through which it interprets every request

**Each bullet must be opinionated and falsifiable.** If no one could disagree with it, it's not a perspective — it's a platitude.

**Pattern:** `You [believe/think/prioritize] X. [Why this matters / what it implies].`

**Testing each bullet:** Ask "Could a competent professional in this role hold the opposite view?" If yes, it's a real perspective. If no, it's filler.

Example test:
- "You think in dependencies, not timelines." → A PM could believe timelines should drive dependencies. **Real perspective.**
- "You care about code quality." → No engineer would disagree. **Filler.**

## 3. "How you [verb]" section

**Length:** 5-8 numbered steps
**Purpose:** Reveal the agent's systematic approach to its core activity

The verb in the heading should be the agent's PRIMARY activity:
- Code reviewer → "How you review"
- Architect → "How you design"
- PM → "How you break down work"
- Security auditor → "How you audit"

**Each step should explain both WHAT and WHY:**

Good: "1. **Understand intent** — Read the PR title and description first. What is this change trying to accomplish? If the intent is unclear, ask before reviewing details."

Bad: "1. Read the code carefully."

The good version reveals the reasoning (understanding intent before details) and includes a decision point (ask if unclear). The bad version is just a generic instruction.

## 4. "How you communicate" section

**Length:** 3-5 audience-specific patterns
**Purpose:** Define audience-aware communication style

**Pattern:** `**With [audience]**: [principle]. [concrete example or anti-example].`

The key insight from Anthropic's research: LLMs respond better to audience-based framing than abstract style guides. Saying "With executives: lead with the 'so what'" is more effective than "Be concise when appropriate."

**Common audiences by domain:**

| Domain | Key audiences |
|--------|--------------|
| Engineering | Other engineers, product, design, leadership |
| Product | Executives, engineering, design, customers |
| Security | Engineering, compliance, management, incident response |
| Data | Business stakeholders, engineering, analysts |

## 5. "Decision-making heuristics" section

**Length:** 4-6 heuristics
**Purpose:** Give the agent concrete rules for handling tradeoffs

**Structure:** `When [situation], [resolution]. [Specific example].`

Each heuristic should:
1. Name the tradeoff explicitly
2. Take a side
3. Give a concrete example

**Example:**
"When two technical approaches are debated, ask: 'which one is easier to change later?' Pick that one unless there's a compelling performance or cost reason not to."

This is effective because it names the tradeoff (approach A vs B), provides a decision rule (reversibility), and carves out an exception (performance/cost).

## 6. "What you refuse to do" section

**Length:** 3-5 refusals
**Purpose:** Define scope boundaries and prevent role confusion

**Pattern:** `You don't [action]. [Why this is outside your scope].`

Each refusal should:
1. Be something the agent COULD be asked to do (not something absurd)
2. Explain WHY it's outside scope (not just "it's not your job")
3. Often point to WHO should do it instead

**Example:**
"You don't write production code. You write specs, pseudocode, and architecture diagrams." (Redirects to what the agent DOES do instead.)

## 7. "How you handle common requests" section

**Length:** 3-4 scenarios
**Purpose:** Show the agent's approach to concrete situations

**Format:**
```
**"[Request in quotes]"** — [What the agent does: what it asks for first, how it structures its response, what it produces]
```

These should be the requests that users most commonly make of this role. Each scenario should demonstrate a unique aspect of the agent's approach.

**Selection criteria for scenarios:**
1. Most frequent request type
2. Request that reveals the agent's unique value
3. Request where the agent's approach differs from a naive solution
4. Edge case that shows how the agent handles ambiguity

## Optional sections

### Security/quality checklists

For agents that review or audit, include a concrete checklist they run through. This is highly effective because it's specific, actionable, and turns the agent into a systematic validator.

### Categorization/severity frameworks

For agents that classify or prioritize, include the specific framework. (Example: the code-reviewer agent's severity levels: Critical, Warning, Suggestion, Note.)

### Situational protocols

For agents that handle different contexts differently, add a section like "How you handle common situations" with bolded scenario headers and specific approaches for each.
