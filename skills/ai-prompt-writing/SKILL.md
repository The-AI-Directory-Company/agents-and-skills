---
name: ai-prompt-writing
description: Write effective prompts for AI coding tools — structure task context, specify constraints, provide examples, and iterate based on output quality. Targets developers using Claude Code, Copilot, Cursor, and similar tools.
metadata:
  displayName: "AI Prompt Writing"
  categories: ["communication", "engineering"]
  tags: ["ai-prompts", "prompt-templates", "AI", "coding-assistant", "Claude-Code", "Copilot", "Cursor"]
  worksWellWithAgents: ["ai-engineer", "developer-experience-engineer", "prompt-engineer"]
  worksWellWithSkills: ["code-review-checklist", "prompt-engineering-guide", "technical-spec-writing"]
---

# AI Prompt Writing

## Before you start

Gather the following from the user. If anything is missing, ask before proceeding:

1. **What tool are you prompting?** — Claude Code, GitHub Copilot, Cursor, Gemini CLI, ChatGPT, or another AI coding tool
2. **What task should the prompt accomplish?** — Code generation, refactoring, debugging, review, documentation, or explanation
3. **What is the codebase context?** — Language, framework, project conventions, relevant files
4. **What does a good result look like?** — Expected output format, quality criteria, or a reference example
5. **What has gone wrong so far?** — Previous prompt attempts and how the output missed the mark

## Prompt writing procedure

### 1. State the Task Before the Context

Lead with what you want, then provide supporting information. AI tools process instructions sequentially — burying the task after paragraphs of context reduces accuracy.

**Structure:**
```
[What to do] — 1-2 sentences
[Constraints] — format, style, boundaries
[Context] — relevant code, files, architecture
[Examples] — input/output pairs if helpful
```

Bad: "Here is my React component that uses useState and useEffect to fetch data from /api/users and display it in a table. The table has sorting and pagination. I want you to..."

Good: "Refactor this React component to replace useState+useEffect data fetching with React Query. Keep the existing sorting and pagination behavior. Here is the component: ..."

### 2. Be Specific About Constraints

Vague prompts get vague results. Constrain the output to match your project's conventions:

- **Language/framework version**: "Use TypeScript 5, React 19, Next.js 15 App Router"
- **Style conventions**: "Follow the existing pattern in src/hooks/ — named exports, no default exports"
- **What NOT to do**: "Do not add new dependencies. Do not change the public API."
- **Scope boundaries**: "Only modify the fetchUsers function. Do not touch the rendering logic."

Each constraint eliminates a category of wrong answers.

### 3. Provide Concrete Examples

When the task involves a pattern, show the pattern instead of describing it:

```
Convert this REST endpoint to the project's tRPC pattern.

Existing tRPC endpoint for reference:
// src/server/routers/posts.ts
export const postsRouter = router({
  list: publicProcedure
    .input(z.object({ limit: z.number().default(10) }))
    .query(async ({ input, ctx }) => {
      return ctx.db.post.findMany({ take: input.limit });
    }),
});

REST endpoint to convert:
// src/pages/api/users.ts
[paste the code]
```

One concrete example communicates format, naming, error handling, and style better than a paragraph of instructions.

### 4. Scope the Context Window

AI tools have limited context. Include only what matters for the task:

- **Include**: Files the tool needs to read or modify, type definitions it must conform to, test files that show expected behavior
- **Exclude**: Unrelated modules, boilerplate, configuration files unless they affect the task
- **Reference, do not paste**: For large files, describe the relevant section instead of pasting 500 lines — "The User type is defined in src/types.ts with fields: id, email, name, role"

When using file-aware tools (Claude Code, Cursor), point to files by path instead of pasting content. The tool reads them with full context.

### 5. Specify the Output Format

Tell the tool exactly how to deliver the result:

- "Output only the modified function, not the entire file"
- "Return a unified diff I can apply with `git apply`"
- "Create the file at src/hooks/useUsers.ts with the complete implementation"
- "List each change as: file path, line range, description of change"

Unspecified format leads to incomplete snippets, unnecessary explanations, or code wrapped in markdown when you wanted a raw file.

### 6. Use Iterative Refinement

First-attempt prompts rarely produce perfect results. Iterate systematically:

1. **Run the prompt** and examine the output
2. **Identify the gap** — wrong format, missing edge case, incorrect assumption, or style mismatch
3. **Add a constraint** that addresses the specific gap — do not rewrite the entire prompt
4. **Re-run** and compare to the previous output
5. **Repeat** until the output meets your quality criteria. Save effective prompts as reusable templates.

### 7. Prompt Templates for Common Tasks

**Bug fix:**
```
Fix this bug: [describe the symptom and reproduction steps].
The relevant code is in [file path]. The expected behavior is [X], but the actual behavior is [Y].
Root cause hypothesis: [your guess, if any].
Do not change the function signature or public API.
```

**Code review:**
```
Review this diff for: correctness bugs, performance issues, security concerns, and style violations against [project conventions].
For each issue, state: file, line, severity (critical/warning/nit), and a specific fix.
Do not comment on things that are correct.
```

**Refactoring:**
```
Refactor [function/component] to [specific goal: extract hook, split component, reduce complexity].
Preserve all existing behavior — the existing tests must still pass without modification.
Follow the pattern established in [reference file].
```

## Quality checklist

Before sending a prompt to an AI coding tool, verify:

- [ ] The task statement comes first, before context and examples
- [ ] At least 2 specific constraints narrow the output (format, style, scope, exclusions)
- [ ] Concrete examples are provided for pattern-based tasks
- [ ] Only relevant files and context are included — no unrelated code
- [ ] Output format is explicitly specified
- [ ] The prompt has been tested and refined at least once based on initial output

## Common mistakes

- **Dumping an entire codebase and saying "fix it."** Without a specific task and scope, the tool guesses what you want. Narrow the ask.
- **Describing the pattern instead of showing it.** "Use our standard hook pattern" means nothing to the tool. Paste a reference implementation.
- **Omitting what NOT to do.** AI tools are eager to help. Without exclusions, they add dependencies, change APIs, or refactor code you did not ask about.
- **Giving up after one attempt.** The first output is a draft. Add a constraint, re-run, and compare. Most prompts need 2-3 iterations.
- **Treating all AI tools identically.** Claude Code reads files from disk. Copilot autocompletes inline. Cursor uses file context. Tailor the prompt to the tool's interface and reference files by path when the tool can read them directly.
