# Contributing to Agents & Skills

Thank you for contributing to the AI Directory! Every agent and skill you submit helps teams work better with AI. This guide has everything you need to get a pull request merged.

## Before You Start

- Read the authoring guide for your content type:
  - **Agents**: [`agents/CLAUDE.md`](agents/CLAUDE.md)
  - **Skills**: [`skills/CLAUDE.md`](skills/CLAUDE.md)
- Browse existing entries at [ai-directory.company](https://ai-directory.company) to understand the quality bar and avoid duplicates

## Quick Start Templates

Copy the relevant template, fill in the placeholders, and delete any sections that don't apply.

### New Agent

Create `agents/<your-agent-slug>.md`:

````markdown
---
name: your-agent-slug
description: One sentence describing what this agent does and who it helps.
metadata:
  displayName: Your Agent Name
  categories:
    - engineering
  tags:
    - optional
    - freeform
    - search-terms
  worksWellWithAgents:
    - other-agent-slug
  worksWellWithSkills:
    - related-skill-slug
---

## Approach

Describe the agent's core philosophy, priorities, and how it thinks about its domain. This section shapes the agent's worldview.

## Communication

Explain how the agent communicates — tone, format preferences, how it handles ambiguity, when it asks clarifying questions.

## Refusals

List things this agent explicitly does not do, and why. Clear boundaries make the agent more useful and trustworthy.
````

### New Skill

Create `skills/<your-skill-slug>/SKILL.md`:

````markdown
---
name: your-skill-slug
description: One sentence describing what this skill teaches or enables.
metadata:
  displayName: Your Skill Name
  categories:
    - engineering
  tags:
    - optional
    - freeform
    - search-terms
  worksWellWithAgents:
    - related-agent-slug
  worksWellWithSkills:
    - other-skill-slug
---

## Before You Start

List any prerequisites, required access, tools, or context the user needs before following this skill.

## Procedure

Step-by-step instructions.

1. **First step** — Explain what to do and why.
2. **Second step** — Be specific. Vague guidance is not useful.
3. **Third step** — Include decision points and how to handle them.

## Quality Checklist

- [ ] Criterion one is met
- [ ] Criterion two is met
- [ ] Output has been verified against the goal

## Common Mistakes

- **Mistake name**: What goes wrong and how to avoid it.
- **Another mistake**: What goes wrong and how to avoid it.
````

## PR Process

1. **Fork** this repository
2. **Create a branch** from `main` (e.g., `add-agent-devops-engineer`)
3. **Add your content** following the spec below
4. **Open a pull request** with a clear title and description explaining what the entry does and why it is valuable
5. **CI validates** frontmatter structure, required fields, and slug consistency automatically
6. A **maintainer reviews** your submission for quality, accuracy, and fit

## Frontmatter Rules

| Field | Required | Rules |
|---|---|---|
| `name` | Yes | Lowercase hyphens only, max 64 chars, must match filename (agents) or folder name (skills) |
| `description` | Yes | Max 1024 characters |
| `metadata.displayName` | Yes | Human-readable name shown in the UI |
| `metadata.categories` | Yes | At least one from: `engineering`, `product-management`, `project-management`, `design`, `data`, `business`, `communication`, `security`, `leadership`, `operations` |
| `metadata.tags` | No | Freeform search terms to aid discoverability |
| `metadata.worksWellWithAgents` | No | Slugs of related agents; should be bidirectional |
| `metadata.worksWellWithSkills` | No | Slugs of related skills; should be bidirectional |
| `metadata.author` | No | User ID assigned by maintainers after your first merged PR |
| `metadata.refURL` | No | URL crediting the original source if this entry is adapted from public work |

## Quality Bar

Submissions are evaluated on five dimensions:

- **Specificity**: Agents must encode real domain expertise and mental models, not generic instructions anyone could write. Skills must provide concrete, actionable steps — not vague guidance. If the content could apply to any domain, it is too generic.
- **Completeness**: All required frontmatter fields must be present. The body must be comprehensive enough to be useful without any additional context. Stubs and placeholders will be rejected.
- **Accuracy**: Domain-specific claims must be correct. Framework and tool references must be real. If you cite a methodology or process, it should be accurate to how practitioners actually use it.
- **Formatting**: Valid markdown throughout. Consistent frontmatter structure. No broken internal references. Headers should follow a logical hierarchy.
- **No marketing copy**: Describe what the agent or skill does, not how amazing it is. Avoid superlatives, hype, and promotional language.

## Cross-References

Use `metadata.worksWellWithAgents` and `metadata.worksWellWithSkills` to link related entries. Reference entries by their slug.

Cross-references should be **bidirectional**: if agent A references skill B, skill B should also reference agent A. CI will warn on orphaned references (where the target does not link back) but will not block the PR. Maintainers may add the reverse reference during review.

## Skill Supporting Files

A skill folder can contain supporting files alongside `SKILL.md`:

- `examples/` — Worked examples demonstrating the skill in practice
- `references/` — Reference material, cheat sheets, or lookup tables
- `scripts/` — Automation scripts referenced by the skill procedure
- `assets/` — Images, diagrams, or other binary assets

A minimal skill only needs `SKILL.md`. Add supporting files only when they meaningfully improve the skill's usefulness.

## Review Expectations

- Maintainers may request changes to improve quality, accuracy, or consistency — this is normal and expected, not a rejection
- We may edit frontmatter (categories, tags, cross-references) for consistency with the broader directory without requesting your approval
- Large PRs adding many entries at once are welcome but may take longer to review
- First-time contributors will receive a welcome message; we appreciate you taking the time to contribute
