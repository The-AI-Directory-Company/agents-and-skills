# Agents & Skills

Community-maintained agent and skill definitions for [The AI Directory](https://ai-directory.company).

[![Validate PR Content](https://github.com/The-AI-Directory-Company/agents-and-skills/actions/workflows/validate-pr.yml/badge.svg)](https://github.com/The-AI-Directory-Company/agents-and-skills/actions/workflows/validate-pr.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

---

## What Is This?

This repository is the open content layer for [ai-directory.company](https://ai-directory.company). It contains two types of content:

### Agents

AI persona definitions — markdown files that describe a specialized role, its expertise, decision frameworks, and behavioral patterns. Each agent file gives an AI assistant the context it needs to perform as a domain expert.

Browse agents: [ai-directory.company/agents](https://ai-directory.company/agents)

### Skills

Reusable prompt-driven procedures — step-by-step instructions that guide an AI assistant through a specific task. Skills can include templates, checklists, and worked examples. They are designed to be installed into tools like Claude Code, Cursor, or any AI coding assistant.

Browse skills: [ai-directory.company/skills](https://ai-directory.company/skills)

All content follows the **[Agent Skills specification](https://agentskills.io)** — the open standard adopted by Claude Code, OpenAI Codex, Cursor, GitHub Copilot, Gemini CLI, and 25+ other AI tools.

---

## Repository Structure

```
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

We welcome contributions from anyone! Whether you are adding a new agent, creating a skill, or improving an existing entry — your expertise makes this directory better for everyone.

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

---

## License

[MIT](LICENSE) — The AI Directory Company
