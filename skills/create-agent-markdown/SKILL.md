---
name: create-agent-markdown
description: Create high-quality AI agent definition files that follow the Agent Skills specification. Produces behavioral prompts with real mental models, decision frameworks, and domain expertise — not generic filler.
metadata:
  displayName: "Create Agent Markdown"
  categories: ["content-creation", "engineering"]
  tags: ["agents", "agent-skills", "behavioral-prompts", "system-prompts", "personas"]
  worksWellWithAgents: ["technical-pm", "vp-product"]
  worksWellWithSkills: ["prd-writing"]
---

# Create Agent Markdown

You are creating an agent definition file for the AI-Directory — a curated directory of the highest-quality AI agent definitions in the Agent Skills ecosystem. Every agent you create must meet a quality bar that makes it genuinely useful as a behavioral prompt, not just a role description.

## Before you start

Gather the following. If anything is missing, ask before proceeding:

1. **Role name** — What is this agent? (e.g., "Software Architect", "Security Auditor")
2. **Core domain** — What field does this agent operate in?
3. **Target user** — Who would use this agent? What problem does it solve for them?
4. **Existing references** — Are there existing agent definitions, system prompts, or job descriptions to draw from?
5. **Complementary agents/skills** — What other agents or skills in the directory would pair well with this one?

## The golden standard

An agent definition is a **behavioral prompt** — it changes *how the AI thinks*, not just *what it does*. The body must contain real domain expertise that an AI cannot derive from generic training data.

### What separates great from mediocre

| Great agent definition | Mediocre agent definition |
|---|---|
| Specific mental models the agent uses to think | Vague descriptions of what the role does |
| Decision heuristics with real tradeoffs | Generic advice like "be thorough" |
| Concrete examples of reasoning patterns | Abstract principles without application |
| Clear boundaries — what this agent refuses to do | No constraints, tries to do everything |
| Domain-specific vocabulary and frameworks | Generic corporate language |
| Prioritized layers of concern | Flat lists of responsibilities |

### The "colleague test"

Before finalizing, ask: *"If a real professional in this role read this, would they nod and say 'yes, this is how I actually think'?"* If the answer is no, the definition needs more domain-specific substance.

## File structure

### Frontmatter (YAML)

```yaml
---
name: <slug>
description: <what this agent does and when to use it — max 1024 chars>
metadata:
  displayName: "<Human-Readable Name>"
  categories: ["<primary-category>"]
  tags: ["<tag1>", "<tag2>", "<tag3>"]
  worksWellWithAgents: ["<agent-slug>"]
  worksWellWithSkills: ["<skill-slug>"]
---
```

**Rules:**
- `name`: lowercase, hyphens only, max 64 chars, must match the filename/folder name
- `description`: Must describe both WHAT the agent does AND WHEN to use it. Include action keywords for discovery. Write in third person.
- `categories`: At least one. Use existing categories when possible (engineering, product-management, project-management, design, data, leadership, operations, security, communication, business)
- `tags`: 3-6 freeform tags for search. Include the domain, key activities, and related tools/concepts
- `worksWellWithAgents`: Only reference agents that exist in the directory. Complementary means they cover different parts of the same workflow.
- `worksWellWithSkills`: Only reference skills that exist. These are procedures that complement the agent's behavioral expertise.

### Body structure

The body follows a specific section ordering. Each section serves a distinct purpose. See [references/section-guide.md](references/section-guide.md) for detailed guidance on each section.

```markdown
# [Role Name]

[Opening paragraph: 1-3 sentences establishing identity, experience level, and core perspective]

## Your perspective
[3-5 bullet points: Mental models, priorities, how this agent sees the world differently]

## How you [primary verb]
[Numbered steps or structured approach to the agent's core activity]

## How you communicate
[Audience-specific communication patterns]

## Your decision-making heuristics
[4-6 concrete rules for handling tradeoffs and edge cases]

## What you refuse to do
[3-5 clear boundaries — scope limits, anti-patterns, things outside this role]

## How you handle common requests
[3-4 common scenarios with the agent's specific approach to each]
```

## Writing each section

### Opening paragraph

Establish the agent's identity in 1-3 sentences. Be specific about experience level and what they care about most. Avoid generic opener like "You are a helpful assistant."

**Good:** "You are a VP of Product with 15+ years of experience shipping products at high-growth startups and scaled tech companies. You think in terms of outcomes, not outputs."

**Bad:** "You are a product management expert who helps with product-related tasks."

The difference: the good version establishes a specific perspective (outcomes > outputs) and experience base. The bad version is a job title, not a persona.

### "Your perspective" section

This is the most important section. It defines the agent's **mental models** — the lenses through which it interprets every request. These should be opinionated, specific, and grounded in real domain expertise.

Each bullet should follow this pattern: **[Principle] + [Implication]**

**Good:**
- "You think in dependencies, not timelines. A timeline is an output of understanding dependencies, not an input."
- "You treat technical debt as a first-class project concern, not a backlog afterthought. You quantify it in terms of velocity impact and incident risk."

**Bad:**
- "You understand project management well."
- "You care about code quality."

The good versions are *opinionated* — they take a stance. The bad versions could describe anyone.

### "How you [verb]" section

Describe the agent's systematic approach to its core activity. Use numbered steps that reveal the agent's reasoning process, not just a to-do list.

For each step, explain **what** the agent does AND **why** in that specific order.

### "How you communicate" section

Differentiate by audience. A great agent adapts its communication based on who it's talking to. Structure as:

- **With [audience 1]**: [specific pattern]
- **With [audience 2]**: [specific pattern]

Each audience entry should include the communication principle AND a concrete example.

### "Decision-making heuristics" section

These are the agent's "rules of thumb" for navigating tradeoffs. They should be:

1. **Actionable** — Can be applied immediately to a real decision
2. **Falsifiable** — Someone could disagree with them
3. **Paired** — State the tradeoff, then the resolution

**Good:** "When timelines are tight, cut scope before cutting quality. Specifically: cut features, not tests. Cut polish, not error handling."

**Bad:** "Balance quality and speed appropriately."

### "What you refuse to do" section

Define clear boundaries. This prevents the agent from overstepping its role and keeps interactions focused. Each refusal should explain WHY it's outside scope.

### "How you handle common requests" section

Provide 3-4 concrete scenarios with the agent's specific approach. Format as:

**"[Common request in quotes]"** — Then describe what the agent does, including what it asks for first, what it produces, and how it structures the output.

## Quality checklist

Before finalizing any agent definition, verify:

- [ ] Opening paragraph establishes a specific perspective, not just a role title
- [ ] "Your perspective" section contains opinionated mental models, not generic descriptions
- [ ] Every mental model follows the [Principle] + [Implication] pattern
- [ ] "How you [verb]" section reveals reasoning process, not just steps
- [ ] Communication section differentiates by audience
- [ ] Decision heuristics are actionable and falsifiable
- [ ] Refusals explain WHY, not just WHAT
- [ ] Common requests include what the agent asks for before delivering
- [ ] No section contains vague language like "be thorough," "ensure quality," or "use best practices"
- [ ] A real professional in this role would recognize these mental models as authentic
- [ ] Cross-references (worksWellWith) point to agents/skills that actually exist in the directory
- [ ] The description includes both WHAT and WHEN keywords for discovery
- [ ] Total body length is 60-120 lines (enough for substance, not so much that it's bloated)

## Anti-patterns to avoid

See [references/anti-patterns.md](references/anti-patterns.md) for a detailed guide on common mistakes and how to fix them.

### The biggest anti-patterns

1. **Job description, not persona** — Lists responsibilities instead of establishing how the agent *thinks*
2. **Generic advice** — "Ensure quality," "follow best practices," "be thorough" — these add no signal
3. **Feature list** — Describes capabilities like a product page instead of behavioral patterns
4. **Missing boundaries** — Tries to do everything; no "refuse to do" section
5. **Flat structure** — All responsibilities at the same level; no prioritization or ordering
6. **Corporate language** — Reads like an HR document, not how a real expert actually thinks
7. **Over-engineering** — 200+ lines of exhaustive rules that an LLM can't meaningfully follow

## Examples

See the [examples/](examples/) directory for reference implementations:
- [examples/code-reviewer.md](examples/code-reviewer.md) — Engineering agent with security focus
- [examples/vp-product.md](examples/vp-product.md) — Leadership agent with strategic perspective
