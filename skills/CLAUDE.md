# Skill Folders — Reference

Each **folder** in this directory represents a single skill. Folders follow the **Agent Skills specification** (agentskills.io) — the open standard adopted by Claude Code, OpenAI Codex, Cursor, GitHub Copilot, Gemini CLI, and 25+ other AI tools.

## What Is a Skill?

A skill is a **procedural reference**. The `SKILL.md` entrypoint contains step-by-step instructions, templates, edge cases, and concrete examples that teach an AI agent how to perform a specific task. It is not a description of the skill — it is the actual knowledge an agent needs to execute it.

Think of it as a detailed how-to guide written for an AI. A `prd-writing/SKILL.md` file should contain everything an agent needs to produce a high-quality PRD — the exact template, section-by-section instructions, quality criteria, common mistakes to avoid, and examples of good vs. bad output.

### What the body should contain

- **Step-by-step procedures** — Numbered steps for the core workflow
- **Templates & formats** — Exact output structures the agent should produce
- **Quality criteria** — What makes the output good vs. bad, with concrete examples
- **Edge cases & gotchas** — Common pitfalls and how to handle them
- **Input requirements** — What information the agent needs to ask for before starting
- **Examples** — Concrete before/after or good/bad comparisons
- **Checklists** — Validation steps to run before delivering output

### What the body should NOT contain

- Marketing copy or feature descriptions ("This skill helps you...")
- Vague advice without actionable specifics
- Configuration/setup instructions for tools
- Behavioral or persona instructions (those belong in agent files)

---

## Folder Structure

Each skill lives in its own folder under `content/skills/`:

```
content/skills/
  <skill-name>/
    SKILL.md              ← required entrypoint (frontmatter + body)
    references/           ← optional reference material
    examples/             ← optional example outputs
    scripts/              ← optional executable scripts
    assets/               ← optional static assets
```

The `SKILL.md` file has two parts:

1. **Frontmatter** — YAML between `---` fences, following the Agent Skills spec with our extensions in `metadata`.
2. **Body** — Procedural instructions, templates, and reference material for performing the skill.

---

## Supporting Files

Skill folders support **progressive disclosure**:

- `SKILL.md` is always loaded — it is the primary content rendered on the detail page and delivered to AI agents.
- Files in `references/`, `examples/`, `scripts/`, and `assets/` are loaded on-demand when a user browses the skill's detail page and interacts with the file tree browser.

Use supporting files when your skill benefits from:

- **references/** — Background material, specs, or standards the skill draws from.
- **examples/** — Concrete example outputs showing what "good" looks like.
- **scripts/** — Executable scripts (shell, Python, etc.) that automate parts of the workflow.
- **assets/** — Static files (images, diagrams, config templates) referenced by the skill.

A minimal skill only needs `SKILL.md`. Add supporting files when they make the skill meaningfully more useful — not to pad it out.

---

## Frontmatter Fields

### Agent Skills Spec Fields (top-level)

#### `name` (string, required)

Spec-compliant identifier. Lowercase, hyphens only. Max 64 chars. **Must match the folder name**.

```yaml
name: prd-writing
```

#### `description` (string, required)

What the skill does and when to use it. Max 1024 chars. Shown on listing cards and used by compatible agents for discovery.

```yaml
description: A skill for writing clear, comprehensive Product Requirements Documents — from problem statement to success metrics.
```

### Directory-Specific Fields (inside `metadata`)

#### `metadata.displayName` (string, required)

Human-readable name for the UI.

#### `metadata.categories` (string array, min 1 required)

Filterable categories. A skill can belong to multiple.

#### `metadata.tags` (string array)

Freeform tags for search/discovery.

#### `metadata.author` (string, optional)

Convex `_id` of the member who proposed this skill.

#### `metadata.refURL` (string, optional)

URL crediting the original source.

#### `metadata.worksWellWithAgents` (string array, optional)

Slugs of complementary agents in `content/agents/`.

#### `metadata.worksWellWithSkills` (string array, optional)

Slugs of complementary skills in `content/skills/`.

---

## Full Example

```
content/skills/
  prd-writing/
    SKILL.md
    examples/
      good-prd.md
      bad-prd.md
    references/
      prd-checklist.md
```

`prd-writing/SKILL.md`:

```yaml
---
name: prd-writing
description: Write clear, comprehensive PRDs with problem statements, success metrics, and scope boundaries.
metadata:
  displayName: "PRD Writing"
  categories: ["product-management"]
  tags: ["prd", "requirements", "documentation"]
  worksWellWithAgents: ["vp-product", "technical-pm"]
  worksWellWithSkills: ["user-story-mapping", "ticket-writing"]
---

# PRD Writing

## Before you start

Gather the following from the user:
1. What problem are we solving? (user pain or business need)
2. Who is affected? (user segments)
3. What constraints exist? (timeline, budget, tech stack)
...

## PRD template

### 1. Problem Statement
Write 2-3 sentences. State the problem from the user's perspective...

### 2. Success Metrics
Define 2-4 measurable outcomes...
...
```

---

## How It Gets Processed

1. **Build time** (`pnpm build:content`): `scripts/build-content-index.ts` scans skill folders (not flat `.md` files), reads each `SKILL.md` entrypoint, parses frontmatter, validates fields, resolves cross-references, generates file tree metadata for the UI, pre-builds zip files per skill for download, and writes `content/generated/skills-index.json`.
2. **Listing page** (`/skills`): Server component reads the index JSON for search and filtering.
3. **Detail page** (`/skills/[slug]`): Statically generated. Renders the `SKILL.md` body with `react-markdown` + `remark-gfm` + Tailwind Typography. For multi-file skills, a file tree browser lets users explore supporting files.

## Folder Naming

The folder name **must** match the `name` field (per the Agent Skills spec):

```
content/skills/prd-writing/SKILL.md         → name: prd-writing
content/skills/user-story-mapping/SKILL.md  → name: user-story-mapping
```

## Compatibility

These folders produce valid Agent Skills spec files — compatible AI tools can discover and use them directly. The folder-based format extends the spec by allowing supporting files alongside the primary `SKILL.md` entrypoint.
