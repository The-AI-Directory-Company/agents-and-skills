# How AI Coding Tools Read Prompts Differently

Each tool has a different interface, context model, and set of strengths. The same prompt text produces different results depending on where you send it. Tailor your prompts to the tool.

---

## Claude Code

**Interface**: CLI agent that runs in your terminal with full filesystem access.

**How it reads prompts**:
- Has direct access to your project files. You can reference files by path — it reads them from disk.
- Maintains conversation context across a session. Earlier instructions carry forward.
- Executes shell commands, reads/writes files, and runs tests as part of its workflow.
- Processes the full file when you point to it — no need to paste code into the prompt.

**Prompt implications**:
- **Reference files by path** instead of pasting content: "See `src/hooks/useAuth.ts` for the pattern to follow."
- **Ask it to verify its own work**: "After making the change, run `pnpm test src/lib/__tests__/auth.test.ts` and fix any failures."
- **Use constraint stacking**: Claude Code handles multi-step instructions well. You can say "refactor X, then update the tests, then run them" in one prompt.
- **Leverage project-level instructions**: `.claude/` rules and `CLAUDE.md` files provide persistent context — put conventions there instead of repeating them in every prompt.

**Watch out for**:
- Long sessions can accumulate stale context. If responses drift, start a new conversation.
- It may propose file-level changes when you only wanted a function-level fix. Scope explicitly.

---

## GitHub Copilot

**Interface**: Inline autocomplete + chat panel inside VS Code / JetBrains / Neovim.

**How it reads prompts**:
- **Autocomplete mode**: Reads the current file, open tabs, and surrounding code to predict the next line or block. No explicit prompt needed.
- **Chat mode**: Reads selected code, the current file, and optionally referenced files via `@workspace` or `#file` mentions.
- Context window is smaller than agent-based tools. It prioritizes the current file and nearby code.

**Prompt implications**:
- **For autocomplete**: Write a clear function signature and a descriptive comment above it. Copilot completes based on what it sees immediately before the cursor.
- **For chat**: Select the relevant code before asking. Use `#file:path/to/file.ts` to explicitly include files in context.
- **Keep prompts short and focused**: One task per prompt. Copilot chat works best with single-step instructions.
- **Use comments as prompts**: `// TODO: add input validation for email format` in the code itself is often enough for autocomplete to generate the implementation.

**Watch out for**:
- Copilot does not run code or verify output. It suggests — you verify.
- It has limited awareness of files you haven't opened. If a pattern lives in a file Copilot can't see, paste the relevant snippet.

---

## Cursor

**Interface**: VS Code fork with integrated AI chat, inline editing, and multi-file context.

**How it reads prompts**:
- Reads your entire project structure (file tree) and can index the full codebase for retrieval.
- `@file`, `@folder`, `@codebase` mentions let you control what context is included.
- Inline edit mode (Cmd+K) applies changes directly to the file at your cursor position.
- Composer mode works across multiple files simultaneously.

**Prompt implications**:
- **Use `@` mentions deliberately**: `@file:src/types.ts` to include a type definition, `@codebase` to let it search for relevant code.
- **Inline edits for small changes**: Select code, press Cmd+K, describe the change. Best for single-function modifications.
- **Composer for multi-file tasks**: "Update the hook, its tests, and the component that uses it" — Composer handles cross-file changes.
- **Add rules in `.cursorrules`**: Project conventions go here so you don't repeat them. Similar to Claude Code's `.claude/` rules.

**Watch out for**:
- `@codebase` searches can include irrelevant files. Be specific with `@file` when you know exactly what context matters.
- Inline edits replace selected code. If the selection is wrong, the edit will be too.

---

## Gemini CLI

**Interface**: CLI agent (similar to Claude Code) with filesystem access and tool use.

**How it reads prompts**:
- Reads files from disk when pointed to paths. Can navigate the project structure.
- Executes shell commands and can run tests.
- Supports multi-step workflows within a single session.
- Uses Google's Gemini models with large context windows.

**Prompt implications**:
- **Reference files by path**, same as Claude Code. "Read `src/server/routes/users.ts` and refactor the `getUsers` handler."
- **Be explicit about output location**: "Write the result to `src/hooks/useUsers.ts`" — tell it where to put the file.
- **Verify with commands**: "Run `npm test` after the change and report the results."
- **Provide structure**: Gemini handles structured prompts well. Use numbered steps, bullet lists, and explicit section headers.

**Watch out for**:
- May be more verbose in explanations than other tools. Add "Do not explain the changes — only output the code" if you want concise output.
- Check that file writes landed correctly. Verify the output file matches expectations.

---

## Quick Comparison

| Dimension | Claude Code | Copilot | Cursor | Gemini CLI |
|---|---|---|---|---|
| Interface | CLI agent | IDE autocomplete + chat | IDE chat + inline edit | CLI agent |
| File access | Full filesystem | Current file + open tabs + #file | Full project via @mentions | Full filesystem |
| Runs commands | Yes | No | No (except terminal) | Yes |
| Multi-file edits | Yes (sequential) | No (one file at a time in chat) | Yes (Composer mode) | Yes (sequential) |
| Best for | Complex multi-step tasks, refactors, debugging with test verification | Quick inline completions, single-file chat questions | Multi-file edits with visual context, inline tweaks | Multi-step tasks, code generation with verification |
| Context control | File paths, .claude/ rules | #file mentions, open tabs | @file, @folder, @codebase, .cursorrules | File paths, direct reads |
| Prompt style | Detailed, multi-step, constraint-rich | Short, single-task, comment-driven | @-mention-heavy, mixed inline and chat | Structured, step-by-step |

## General Rule

**Match the prompt to the tool's interface.** A prompt that works well in Claude Code (multi-step, references files by path, asks to run tests) will produce mediocre results in Copilot (which cannot read arbitrary files or run commands). Adapt.
