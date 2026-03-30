# Good vs. Bad Prompts

Side-by-side comparisons for four common task types. Each pair shows the same intent — the bad version gets vague or noisy results, the good version gets usable output.

---

## 1. Code Generation

### Bad

> Make a React component for user settings.

**Why it fails**: No framework version, no styling approach, no data source, no specification of which settings. The AI will invent all of these, and the output won't match your project.

### Good

> Create a React 19 component at `src/components/settings/NotificationPreferences.tsx`.
>
> It should:
> - Display 3 toggles: email notifications, push notifications, weekly digest
> - Use the existing `Switch` component from `src/components/ui/switch.tsx`
> - Read initial values from the `useUser()` hook (see `src/hooks/use-user.ts`)
> - Call `updatePreferences()` from `src/lib/api.ts` on each toggle change
> - Show a toast on success using `sonner` (already installed)
>
> Follow the pattern in `src/components/settings/ProfileSettings.tsx`.
> Use named exports, no default export.
> Do not add new dependencies.

**Why it works**: Specifies the file path, the exact UI elements, the data source, the mutation function, a reference file for patterns, and constraints. Two different AI tools would produce very similar output.

---

## 2. Refactoring

### Bad

> Clean up this file, it's messy.

**Why it fails**: "Messy" is not actionable. The AI might rename variables, restructure everything, add comments, split files — all at once, with no way to verify behavior is preserved.

### Good

> Refactor `src/lib/analytics.ts` to reduce the `trackEvent` function from 85 lines to under 30.
>
> The function currently has a switch statement with 12 cases that each format an event payload differently. Extract each case into a separate formatter function in the same file.
>
> Constraints:
> - The existing tests in `src/lib/__tests__/analytics.test.ts` must pass without changes.
> - Do not change the `trackEvent` function signature.
> - Do not change the event payload shapes (downstream systems depend on them).
> - Keep all formatter functions in the same file for now.

**Why it works**: Names the specific problem (85-line function with a 12-case switch), states the specific solution (extract formatter functions), and anchors correctness to existing tests.

---

## 3. Debugging

### Bad

> My app is broken. Here's the code. Fix it.
> [pastes 400 lines]

**Why it fails**: No symptom, no reproduction steps, no expected vs. actual behavior. The AI reads 400 lines looking for anything that could be wrong and guesses.

### Good

> Bug: The `/api/users` endpoint returns 500 when the `role` query parameter is missing.
>
> Expected: Return all users (no filter) when `role` is omitted.
> Actual: `TypeError: Cannot read properties of undefined (reading 'toLowerCase')` at line 23 of `src/server/routes/users.ts`.
>
> The relevant code:
> ```ts
> // src/server/routes/users.ts, lines 20-30
> const filteredUsers = users.filter(
>   (u) => u.role.toLowerCase() === role.toLowerCase() // line 23
> );
> ```
>
> Root cause hypothesis: `role` is undefined when the query param is missing, and `.toLowerCase()` is called on it without a null check.
>
> Fix this without changing the function signature. If `role` is undefined, return all users unfiltered.

**Why it works**: Includes the exact error, the exact line, the exact file, the expected behavior, and a hypothesis. The AI has everything it needs to write a correct 2-line fix.

---

## 4. Code Review

### Bad

> Review my code.
> [pastes entire file]

**Why it fails**: No review criteria, no context about what changed, no severity framework. The AI produces a mix of praise, nitpicks, and vague suggestions with no way to prioritize.

### Good

> Review this diff for correctness bugs and security concerns only. Skip style nits.
>
> Context: This adds rate limiting to the `/api/auth/login` endpoint. It uses a Redis-backed sliding window counter.
>
> For each issue found, report:
> - File and line
> - Severity: critical / warning
> - What is wrong (1 sentence)
> - Specific fix
>
> Do not comment on things that are correct. Do not summarize what the code does.
>
> ```diff
> [paste the diff]
> ```

**Why it works**: Scopes the review to two categories (correctness, security), provides context about intent, defines the output format, and explicitly excludes filler ("do not comment on things that are correct").

---

## Pattern Summary

| What makes bad prompts bad | What makes good prompts good |
|---|---|
| No task statement up front | Task in the first 1-2 sentences |
| Zero constraints | 2+ specific constraints (scope, style, exclusions) |
| No reference to project patterns | Points to a reference file or existing implementation |
| Dumps entire files without context | Includes only relevant code, with file path and line numbers |
| No output format specified | States exactly what the output should look like |
| No "do not" statements | Includes at least one exclusion to prevent scope creep |
