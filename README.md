# Agents & Skills

Community-maintained agent and skill definitions for [The AI Directory](https://theaidirectory.com).

## What are Agents?

Agents are AI persona definitions — markdown files that describe a specialized role, its expertise, decision frameworks, and behavioral patterns. Each agent file gives an AI assistant the context it needs to perform as a domain expert.

Browse agents: [theaidirectory.com/agents](https://theaidirectory.com/agents)

## What are Skills?

Skills are reusable prompt-driven procedures — step-by-step instructions that guide an AI assistant through a specific task. Skills can include templates, checklists, and worked examples. They're designed to be installed into tools like Claude Code, Cursor, or any AI coding assistant.

Browse skills: [theaidirectory.com/skills](https://theaidirectory.com/skills)

## Repository Structure

```
agents/
  CLAUDE.md          # Authoring guide for agent definitions
  *.md               # One file per agent (filename = slug)
skills/
  CLAUDE.md          # Authoring guide for skill definitions
  <skill-name>/      # One folder per skill
    SKILL.md          # Skill definition (frontmatter + body)
    ...               # Optional supporting files
```

## Contributing

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for the full guide.

**Quick start:**

1. Fork this repo
2. Create a new agent `.md` file in `agents/` or a new skill folder in `skills/`
3. Follow the frontmatter spec in the relevant `CLAUDE.md` guide
4. Open a pull request

## License

See [LICENSE](LICENSE).
