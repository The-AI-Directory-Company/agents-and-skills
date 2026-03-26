# Contributing to Agents & Skills

Thank you for contributing to the AI Directory! This guide covers how to submit agents and skills via pull requests.

## Before You Start

- Read the authoring guide for your content type:
  - **Agents**: [`agents/CLAUDE.md`](agents/CLAUDE.md)
  - **Skills**: [`skills/CLAUDE.md`](skills/CLAUDE.md)
- Browse existing entries at [ai-directory.company](https://ai-directory.company) to understand the quality bar

## PR Process

1. **Fork** this repository
2. **Create a branch** from `main` (e.g., `add-agent-devops-engineer`)
3. **Add your content** following the spec below
4. **Open a pull request** with a clear title and description
5. A maintainer will review your submission

## Agent Spec

Each agent is a single markdown file in `agents/`:

- **Filename**: `<slug>.md` — lowercase, hyphenated (e.g., `devops-engineer.md`)
- **Required frontmatter**:
  - `name` — must match the filename slug
  - `description` — one-line summary of what the agent does
  - `metadata.displayName` — human-readable name
  - `metadata.categories` — at least one category
- **Body**: The agent's system prompt — behavioral instructions, expertise, decision frameworks

## Skill Spec

Each skill is a folder in `skills/`:

- **Folder name**: `<slug>/` — lowercase, hyphenated
- **Required file**: `SKILL.md` with frontmatter:
  - `name` — must match the folder slug
  - `description` — one-line summary of what the skill does
  - `metadata.displayName` — human-readable name
  - `metadata.categories` — at least one category
- **Body**: Step-by-step instructions, templates, checklists
- **Optional**: Supporting files (templates, examples) in the same folder

## Quality Bar

Submissions should meet these standards:

- **Specificity**: Agents should encode real domain expertise and mental models, not generic instructions. Skills should provide concrete steps, not vague guidance.
- **Completeness**: All required frontmatter fields must be present. The body should be comprehensive enough to be useful standalone.
- **Accuracy**: Domain-specific claims should be correct. Framework references should be real.
- **Formatting**: Valid markdown, consistent frontmatter structure, no broken references.

## Cross-References

Use `metadata.worksWellWithAgents` and `metadata.worksWellWithSkills` to link related entries. Reference by slug. Cross-references should be bidirectional — if agent A references skill B, skill B should reference agent A.

## Review Expectations

- Maintainers may request changes to improve quality or consistency
- We may edit frontmatter (categories, tags, cross-references) for consistency
- Large PRs adding many entries at once are welcome but may take longer to review
