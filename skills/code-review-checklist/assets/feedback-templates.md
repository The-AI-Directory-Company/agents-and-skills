# Code Review Feedback Templates

Copy-paste templates for each severity level. Each template includes the severity label, a description of the issue, why it matters, and a specific fix. Adapt the content — keep the structure.

---

## Blocker Template

```
**Blocker**: [DESCRIPTION OF THE DEFECT]

**What**: [Precise description of the incorrect behavior or security flaw]
**Impact**: [Who is affected and what happens — data loss, unauthorized access, crash, wrong output]
**Fix**: [Specific code change or approach to resolve the issue]

Example:
> This endpoint (`POST /api/orders`) reads `req.body.userId` and uses it directly
> in the database query without verifying it matches the authenticated user.
> Any authenticated user can create orders on behalf of other users.
>
> Fix: Replace `req.body.userId` with `req.auth.userId` from the session,
> or add a check that `req.body.userId === req.auth.userId` before proceeding.
```

**When to use**: The code will cause a bug, security flaw, data corruption, or outage in production. Must be fixed before merge.

---

## Major Template

```
**Major**: [DESCRIPTION OF THE ISSUE]

**What**: [What the code does or fails to do]
**Risk**: [What could go wrong in production — performance, reliability, user experience]
**Suggestion**: [Recommended approach with enough detail to implement]

Example:
> This loop queries the database once per item in the cart (`getProductById`
> inside a `.map()`). With the current average cart size of 12 items, this is
> 12 queries per checkout. At scale this will cause latency spikes.
>
> Suggestion: Collect all product IDs first, then use a single
> `WHERE id IN (...)` query. The `productRepository.findByIds()` method
> already supports this.
```

**When to use**: The code has a real quality, performance, or reliability issue that should be fixed before merge. Author can push back with justification.

---

## Minor Template

```
**Minor**: [DESCRIPTION]

[Brief explanation of the improvement and why it helps readability or maintainability.]

Example:
> `handleStuff()` does not describe what this function does. Based on the
> implementation, `validateAndFormatPhoneNumber()` would communicate the intent
> to future readers without requiring them to read the function body.
```

**When to use**: Code quality improvement — naming, structure, documentation, duplication. Does not affect production behavior. Author can defer.

---

## Nit Template

```
**Nit**: [SUGGESTION]

[Optional: one sentence of reasoning. Keep it brief.]

Example:
> I would extract this ternary into a named variable:
> `const displayLabel = isVerified ? 'Verified' : 'Pending'`
> Makes the JSX below slightly easier to scan. Up to you.
```

**When to use**: Personal preference or style suggestion. Author decides whether to adopt. Do not discuss further.

---

## Usage Guidelines

1. **Always lead with the severity label.** The first word of every review comment should be the severity. This lets the author scan the review and triage immediately.

2. **Blockers require a fix suggestion.** "This is wrong" without a path forward is not helpful. If you cannot suggest a fix, describe the correct behavior so the author can implement it.

3. **One issue per comment.** Do not combine a Blocker and a Nit in the same comment. File separate comments so each can be resolved independently.

4. **Use the inline comment feature.** Attach each comment to the specific line in the diff. Generic top-level comments like "there are several issues" force the author to hunt for them.

5. **Acknowledge good work.** If a section is particularly well-written, clear, or handles an edge case you would have missed, say so. Code review is not exclusively about finding problems.
