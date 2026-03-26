---
name: ux-copy-guidelines
description: Create UX copy guidelines — defining voice, tone, microcopy patterns, error messages, empty states, CTAs, and terminology standards that make interfaces clear and consistent.
metadata:
  displayName: "UX Copy Guidelines"
  categories: ["design", "communication"]
  tags: ["UX-copy", "microcopy", "voice-tone", "error-messages", "CTAs", "guidelines"]
  worksWellWithAgents: ["copywriter", "product-designer", "ui-designer"]
  worksWellWithSkills: ["brand-guidelines", "component-design-spec", "prd-writing"]
---

# UX Copy Guidelines

## Before you start

Gather the following from the user before writing:

1. **What product or feature does this cover?** (Entire product, a specific flow, or a new feature launch)
2. **Who are the users?** (Technical developers, non-technical consumers, enterprise admins — vocabulary differs drastically)
3. **Does a brand voice already exist?** (Brand guidelines, tone documentation, or "we have nothing")
4. **What are the top usability complaints?** (Confusing error messages, unclear CTAs, inconsistent terminology)
5. **What platforms does the UI span?** (Web, mobile, CLI, email — constraints differ per surface)

If the user says "make our copy better," push back: "Better how? Are users confused by error messages, dropping off at specific steps, or contacting support because the UI does not explain what to do next?"

## UX copy guidelines template

### 1. Voice and tone principles

Define 3-5 voice attributes that stay constant, then show how tone shifts by context.

Voice is the personality (constant). Tone is the mood (varies by situation).

```Voice attributes:
- Clear over clever — say it plainly, skip the wordplay
- Confident, not arrogant — guide without lecturing
- Helpful, not hand-holdy — respect the user's intelligence
- Human, not corporate — write like a knowledgeable colleague
```

Tone shifts by context:

| Context | Tone | Example |
|---|---|---|
| Success state | Warm, brief | "Project created. You're ready to invite your team." |
| Error state | Direct, calm, solution-first | "That email is already registered. Try signing in instead." |
| Destructive action | Serious, specific about consequences | "This will permanently delete 12 projects and all their data. This cannot be undone." |
| Empty state | Encouraging, action-oriented | "No projects yet. Create your first project to get started." |
| Loading/waiting | Reassuring, informative | "Setting up your workspace. This takes about 30 seconds." |

### 2. Microcopy patterns

Define reusable patterns for common UI elements:

**Buttons and CTAs**
- Use specific verbs: "Save changes," "Send invite," "Create project" — not "Submit," "OK," or "Done"
- Primary action matches the page title: if the page says "Create project," the button says "Create project"
- Destructive buttons state the action: "Delete account" not "Continue" or "Confirm"

**Form labels and help text**
- Labels state what to enter: "Work email address" not "Email"
- Help text answers the question the user is about to ask: "We'll use this to send login codes" not "Enter your email"
- Placeholder text is an example, never an instruction: placeholder "jane@company.com" not "Enter your email here"

**Confirmation dialogs**
- Title states the action: "Delete this project?"
- Body states the consequence: "This will permanently delete 'Acme Dashboard' and its 47 files."
- Buttons are the action and the escape: "Delete project" and "Keep project" — never "Yes" and "No"

### 3. Error message framework

Every error message must answer three questions:

1. **What happened?** (State the problem in plain language)
2. **Why did it happen?** (Brief cause, if it helps the user)
3. **What should the user do next?** (Specific action to resolve it)

**Bad**: "Error 422: Validation failed" / **Good**: "That password is too short. Use at least 8 characters."
**Bad**: "Something went wrong. Please try again later." / **Good**: "We couldn't save your changes because the connection dropped. Check your internet and try again."

Rules:
- Never blame the user: "Invalid email" becomes "That doesn't look like an email address."
- Never use technical jargon: no HTTP codes, no stack traces, no database field names
- Always include a next step: even if it is "Contact support at help@example.com"

### 4. Empty states

Every empty state must include:

- **What this area will contain** once there is data
- **Why it is empty** (first use vs filtered to zero vs error)
- **A CTA to create the first item** or adjust filters

- **First-use**: Heading "No team members yet" / Body "Invite your team to collaborate on projects together." / CTA "Invite team members"
- **Filtered-to-zero**: Heading "No results match your filters" / Body "Try adjusting your date range or removing some filters." / CTA "Clear all filters"

### 5. Terminology standards

Create a terminology table for every domain-specific term. Enforce it across all surfaces.

| Preferred term | Avoid | Reason |
|---|---|---|
| Project | Workspace, repo, space | One word for one concept |
| Team member | User, collaborator, colleague | Consistent across UI and docs |
| Sign in | Log in, login, authenticate | "log in" is the verb, "login" is the noun — avoid ambiguity |
| Delete | Remove, destroy, erase | Unambiguous and expected by users |

Rules: one concept, one word — never alternate. If a term needs explanation on first encounter, add a tooltip. Maintain the terminology table in a shared location and update it when new concepts are introduced.

## Quality checklist

Before delivering the guidelines, verify:

- [ ] Voice attributes are defined with do/don't examples, not abstract adjectives
- [ ] Tone shifts are documented for at least: success, error, destructive action, empty state, and loading
- [ ] Button and CTA patterns use specific verbs, not generic "Submit" or "OK"
- [ ] Error message framework requires what happened, why, and what to do next
- [ ] Empty states distinguish first-use from filtered-to-zero and include a CTA
- [ ] Terminology table lists preferred terms with rejected alternatives and rationale
- [ ] Every pattern includes a concrete before/after or good/bad example
- [ ] Guidelines are specific enough that two writers would produce similar copy for the same screen

## Common mistakes

- **Defining voice with vague adjectives.** "Friendly and professional" describes every brand. Show the boundary: "We say 'Couldn't save your file' not 'Oopsie! Something went wrong.'"
- **Ignoring destructive actions.** "Are you sure?" with "OK" and "Cancel" buttons is a dark pattern. Name the action in the button and state what will be lost.
- **Placeholder text as instructions.** Placeholders disappear on focus — users who tabbed into a field cannot see them. Use labels and help text for instructions; placeholders for format examples only.
- **Inconsistent terminology.** Calling it "project" on one page and "workspace" on another doubles cognitive load. Pick one term and enforce it everywhere.
- **Writing error messages after development.** Copy guidelines must be part of the design process, not a polish pass after the UI is built. Retrofit copy is always worse than designed copy.
- **Skipping the tone spectrum.** Voice without tone guidance means writers default to one register everywhere. A success message and a data-deletion warning should not sound the same.
