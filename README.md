# AI Agent Templates & Skill Definitions

70+ AI agent templates and 55+ skill definitions for [Claude Code](https://code.claude.com), [Cursor](https://cursor.com), [Windsurf](https://windsurf.com), and other AI coding tools. Community-maintained, MIT licensed.

[![Validate PR Content](https://github.com/The-AI-Directory-Company/agents-and-skills/actions/workflows/validate-pr.yml/badge.svg)](https://github.com/The-AI-Directory-Company/agents-and-skills/actions/workflows/validate-pr.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

> **Browse the full directory:** [AI Agent Templates](https://ai-directory.company/agents) | [AI Skill Definitions](https://ai-directory.company/skills)

---

## What Are AI Agent Templates?

AI agent templates are structured Markdown files that give AI coding assistants a specialized role. Each template defines a complete persona — expertise, decision-making frameworks, behavioral patterns, and communication style. When loaded into Claude Code, Cursor, or Windsurf, the AI assistant adopts that role and operates with domain-specific judgment.

Examples include:

- **[Code Reviewer](https://ai-directory.company/agents/code-reviewer)** — catches bugs, security issues, and style violations with actionable feedback
- **[Product Manager](https://ai-directory.company/agents/product-manager)** — writes PRDs, prioritizes features, and defines acceptance criteria
- **[Data Scientist](https://ai-directory.company/agents/data-scientist)** — analyzes datasets, builds models, and explains statistical results
- **[Security Engineer](https://ai-directory.company/agents/security-engineer)** — audits code for vulnerabilities and recommends mitigations
- **[Technical Writer](https://ai-directory.company/agents/technical-writer)** — creates documentation, API references, and developer guides

[Browse all 70+ agents →](https://ai-directory.company/agents)

## What Are AI Skill Definitions?

Skill definitions are composable, task-focused prompt templates for specific workflows. Unlike agents (which define *who* the AI becomes), skills define *what* the AI does — step-by-step instructions for a concrete task. Skills can include templates, checklists, scripts, and reference material.

Examples include:

- **[PRD Writing](https://ai-directory.company/skills/prd-writing)** — product requirements with user stories and acceptance criteria
- **[Code Review Checklist](https://ai-directory.company/skills/code-review-checklist)** — structured review covering security, performance, and readability
- **[Incident Postmortem](https://ai-directory.company/skills/incident-postmortem)** — post-incident review with timeline, root cause, and action items
- **[Architecture Decision Record](https://ai-directory.company/skills/architecture-decision-record)** — document decisions with context, options, and consequences
- **[System Design Document](https://ai-directory.company/skills/system-design-document)** — architecture documentation with trade-offs and diagrams

[Browse all 55+ skills →](https://ai-directory.company/skills)

## How to Install

### Claude Code Skills

Install any skill directly into your project:

```bash
npx skills add code-review-checklist
```

Or install manually — copy the skill folder into `.claude/skills/` in your project:

```bash
cp -r skills/code-review-checklist .claude/skills/
```

### Claude Code Agents

Copy the agent file into your project as a system prompt or CLAUDE.md context:

```bash
cp agents/code-reviewer.md .claude/agents/code-reviewer.md
```

### Cursor & Windsurf

Agent and skill files are standard Markdown. Copy them into your project's AI configuration directory — `.cursor/` for Cursor, `.windsurf/` for Windsurf, or wherever your tool reads system prompts.

## Specification

All content follows the **[Agent Skills specification](https://agentskills.io)** — the open standard adopted by Claude Code, OpenAI Codex, Cursor, GitHub Copilot, Gemini CLI, and 25+ other AI tools.

---

## Repository Structure

```text
agents/
  CLAUDE.md              # Authoring guide for agent definitions
  *.md                   # One file per agent (filename = slug)
skills/
  CLAUDE.md              # Authoring guide for skill definitions
  <skill-name>/          # One folder per skill
    SKILL.md             # Required entrypoint (frontmatter + body)
    examples/            # Optional example outputs
    references/          # Optional reference material
    scripts/             # Optional automation scripts
    assets/              # Optional static files
```

---

## Contributing

We welcome contributions from anyone. Whether you are adding a new agent, creating a skill, or improving an existing entry — your expertise makes this directory better for everyone.

**Quick start:**

1. Fork this repo
2. Read the authoring guide for your content type:
   - Agents: [`agents/CLAUDE.md`](agents/CLAUDE.md)
   - Skills: [`skills/CLAUDE.md`](skills/CLAUDE.md)
3. Create your content following the spec
4. Open a pull request — CI will validate your submission automatically

See [CONTRIBUTING.md](CONTRIBUTING.md) for the full guide, frontmatter spec, and quality bar.

### Good First Contributions

New to open source or to this project? Look for issues labeled [`good first issue`](../../labels/good%20first%20issue) — they include clear instructions and pointers to similar existing entries.

---

## How Validation Works

Every pull request is automatically checked by CI:

- **Frontmatter schema** — Required fields present, correct types, valid categories
- **File structure** — Filename/folder matches `name` field, skill folders contain `SKILL.md`
- **Cross-references** — `worksWellWith*` slugs point to entries that exist
- **Markdown lint** — Basic formatting consistency

If a check fails, click the details link to see exactly what needs to be fixed. No local setup required.

---

## Community

- [Code of Conduct](CODE_OF_CONDUCT.md)
- [Security Policy](SECURITY.md)
- [Getting Help](SUPPORT.md)
- [Community Forum](https://ai-directory.company/forum)

---

## License

[MIT](LICENSE) — The AI Directory Company
