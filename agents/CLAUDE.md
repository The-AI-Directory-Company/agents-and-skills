# Agent Markdown Files — Reference

Each `.md` file in this directory represents a single agent. Files follow the **Agent Skills specification** (agentskills.io) — the open standard adopted by Claude Code, OpenAI Codex, Cursor, GitHub Copilot, Gemini CLI, and 25+ other AI tools.

## What Is an Agent File?

An agent file is a **behavioral prompt**. The markdown body defines how an AI should think, act, and respond when embodying a specific role or persona. It is not a marketing page or feature list — it is the actual instructions an AI agent reads to become that agent.

Think of it as a system prompt that gives an AI the contextualization needed to act in a particular way. A `vp-product.md` agent file should make an AI behave like a VP of Product — with the right mental models, decision frameworks, communication style, and domain expertise.

### What the body should contain

- **Identity & role** — Who is this agent? What is its perspective, expertise, and mandate?
- **Mental models & frameworks** — How does this agent think? What frameworks does it apply?
- **Behavioral guidelines** — How should it communicate? What tone, level of detail, and format?
- **Decision-making heuristics** — When faced with tradeoffs, how does it decide?
- **Constraints & boundaries** — What should it NOT do? Where does its role end?
- **Interaction patterns** — How should it respond to different types of requests?
- **Examples of reasoning** — Concrete examples of how it would approach specific situations

### What the body should NOT contain

- Feature lists or marketing copy ("What It Does", "How to Use")
- Configuration/setup instructions (those belong in docs, not in the agent prompt)
- Generic best practices that aren't specific to the agent's behavior
- API references or CLI commands

---

## File Structure

The file has two parts:

1. **Frontmatter** — YAML between `---` fences, following the Agent Skills spec with our extensions in `metadata`.
2. **Body** — The behavioral prompt that defines the agent's persona, reasoning, and expertise.

---

## Frontmatter Fields

### Agent Skills Spec Fields (top-level)

#### `name` (string, required)

Spec-compliant identifier. Lowercase letters, digits, and hyphens only (must start with a letter). Max 64 chars. **Must match the filename** (without `.md`).

```yaml
name: code-reviewer
```

#### `description` (string, required)

What the agent does and when to use it. Max 1024 chars. Shown on listing cards and used by compatible agents for discovery.

```yaml
description: An AI code reviewer that catches bugs, security issues, and style violations — with actionable, context-aware feedback.
```

### Directory-Specific Fields (inside `metadata`)

#### `metadata.displayName` (string, required)

Human-readable name for the UI.

#### `metadata.categories` (string array, 1-2 required)

Filterable categories. See [`categories.yml`](../categories.yml) for the allowed list. Max 2 per entry.

#### `metadata.tags` (string array)

Freeform tags for search/discovery.

#### `metadata.author` (string, optional)

Convex `_id` of the member who proposed this agent. **Leave this field empty when submitting.** Maintainers assign this after your first merged PR.

#### `metadata.refURL` (string, optional)

URL crediting the original source.

#### `metadata.worksWellWithAgents` (string array, optional)

Slugs of complementary agents in `agents/`.

#### `metadata.worksWellWithSkills` (string array, optional)

Slugs of complementary skills in `skills/`.

---

## Full Example

```yaml
---
name: code-reviewer
description: An AI code reviewer that catches bugs, security issues, and style violations — with actionable, context-aware feedback.
metadata:
  displayName: "Code Reviewer Agent"
  categories: ["engineering"]
  tags: ["code-review", "security", "best-practices"]
  worksWellWithAgents: ["technical-pm"]
  worksWellWithSkills: ["ticket-writing"]
---

# Code Reviewer

You are a senior code reviewer. Your job is to review code changes
with the rigor and judgment of a staff engineer who cares deeply
about code quality, security, and maintainability.

## Your approach

When reviewing code, you work through these layers in order:
1. Correctness — does it do what it claims?
2. Security — does it introduce vulnerabilities?
3. ...

## How you communicate

- Lead with the most important finding
- Be direct but not harsh
- ...
```

---

## How It Gets Processed

1. **Build time** (`pnpm build:content`): `scripts/build-content-index.ts` reads all `.md` files (excluding `CLAUDE.md`), parses frontmatter, validates fields, resolves cross-references, and writes `content/generated/agents-index.json`.
2. **Listing page** (`/agents`): Server component reads the index JSON for search and filtering.
3. **Detail page** (`/agents/[slug]`): Statically generated. Renders the markdown body with `react-markdown` + `remark-gfm` + Tailwind Typography.

## File Naming

The filename **must** match the `name` field (per the Agent Skills spec):

```
agents/vp-product.md      → name: vp-product
agents/code-reviewer.md   → name: code-reviewer
```

All paths are relative to the repository root.

## Compatibility

These files are valid Agent Skills spec files — compatible AI tools can discover and use them directly.
