# Microcopy Patterns Reference

A one-page cheat sheet for the five most common microcopy surfaces. Use this when writing or reviewing UI text.

---

## 1. Buttons and CTAs

| Rule | Do | Don't |
|---|---|---|
| Use specific verbs | "Save changes", "Send invite", "Create project" | "Submit", "OK", "Done", "Continue" |
| Match page title | Page: "Create project" -> Button: "Create project" | Button: "Submit" on a "Create project" page |
| Name destructive actions | "Delete account", "Remove member" | "Continue", "Confirm", "Yes" |
| Front-load the verb | "Export as CSV" | "CSV export action" |
| One primary CTA per view | Single prominent button for the main action | Two equal-weight buttons competing for attention |
| Disabled state explains why | Tooltip: "Add a title to publish" | Greyed-out button with no explanation |

**Sizing rule**: If the label exceeds 3 words, shorten it. If you cannot shorten it below 4 words, the UI flow may need redesigning.

---

## 2. Form Labels and Help Text

| Element | Purpose | Example |
|---|---|---|
| Label | States what to enter | "Work email address" |
| Help text | Answers the question the user is about to ask | "We'll send a login code to this address" |
| Placeholder | Shows the expected format (example, not instruction) | `jane@company.com` |
| Validation error | States what's wrong and how to fix it | "Enter an email address (e.g., jane@company.com)" |

**Rules**:
- Labels are not optional. Every input must have a visible label — do not rely on placeholders alone.
- Help text goes below the input, not above. Users scan top-to-bottom: label, input, help.
- Placeholders disappear on focus. Never put instructions in placeholder text.
- Required vs. optional: Mark the minority. If most fields are required, mark the few that are optional. If most are optional, mark the required ones.
- Group related fields with a fieldset heading. "Billing address" groups street, city, state, zip.

---

## 3. Confirmation Dialogs

Every confirmation dialog has three parts:

| Part | Rule | Example |
|---|---|---|
| Title | State the action as a question | "Delete this project?" |
| Body | State the specific consequence | "This will permanently delete 'Acme Dashboard' and its 47 files. This cannot be undone." |
| Buttons | Action verb + escape verb | "Delete project" / "Keep project" |

**Anti-patterns to avoid**:
- "Are you sure?" as the title — it does not state what action is being confirmed.
- "Yes" / "No" as button labels — the user must re-read the title to understand what "Yes" means.
- "OK" / "Cancel" — "OK" does not communicate what will happen when clicked.
- Missing consequence — "Delete this project?" without stating that files, data, or history will be lost.

**Severity escalation**: For irreversible actions, require the user to type the item name to confirm. Add: "Type 'Acme Dashboard' to confirm deletion."

---

## 4. Empty States

Every empty state answers three questions:

| Question | What to Write | Example |
|---|---|---|
| What goes here? | Describe what this area will contain | "This is where your projects will appear" |
| Why is it empty? | Distinguish first-use from filtered-to-zero | "You haven't created any projects yet" vs. "No projects match your filters" |
| What should I do? | Provide a CTA | "Create your first project" vs. "Clear all filters" |

**First-use empty state template**:
- Heading: "No [items] yet"
- Body: "[Action] to [benefit]."
- CTA button: "[Action] [item]"
- Example: "No projects yet. Create a project to start collaborating with your team." Button: "Create project"

**Filtered-to-zero template**:
- Heading: "No results match your filters"
- Body: "Try adjusting your [specific filter name] or removing some filters."
- CTA button: "Clear all filters"

**Error-driven empty state**: If the area is empty because a fetch failed, show the error pattern instead (see section 5).

---

## 5. Error Messages

Every error message answers three questions:

| Question | Rule | Bad Example | Good Example |
|---|---|---|---|
| What happened? | Plain language, no jargon | "Error 422" | "That password is too short." |
| Why? | Brief cause, only if it helps | "Validation failed" | "Passwords must be at least 8 characters." |
| What next? | Specific action | "Please try again later" | "Add more characters and try again." |

**Rules**:
- Never blame the user: "Invalid input" becomes "That doesn't look like an email address. Check the format and try again."
- Never expose technical details: No HTTP status codes, no stack traces, no database field names.
- Always include a recovery action: Even if the action is "Contact support at help@example.com."
- Match severity to tone: A form validation error is matter-of-fact. A data loss risk is serious and specific.

**Error message templates by type**:

| Type | Template |
|---|---|
| Validation | "[Field] [what's wrong]. [How to fix]." |
| Network | "Couldn't [action] because [cause]. [Recovery step]." |
| Permission | "You don't have access to [resource]. [Who to contact or what to do]." |
| Not found | "[Resource] wasn't found. It may have been deleted or moved. [Next step]." |
| Rate limit | "Too many requests. Wait [time] and try again." |
| Server error | "Something went wrong on our end. Try again in a few minutes. If this keeps happening, contact support." |

---

## Quick-Scan Checklist

Use this when reviewing any screen for microcopy quality:

- [ ] Every button uses a specific verb (not "Submit", "OK", "Done")
- [ ] Destructive buttons name the action ("Delete project", not "Confirm")
- [ ] Every form input has a visible label (not just a placeholder)
- [ ] Help text answers "why do I need this?" or "what format?"
- [ ] Confirmation dialogs state the action in the title and the consequence in the body
- [ ] Empty states have a heading, explanation, and CTA
- [ ] Error messages state what happened, why, and what to do next
- [ ] No technical jargon visible to the user (no error codes, no field names)
