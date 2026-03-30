---
name: knowledge-base-article
description: Write self-service knowledge base articles that resolve customer issues without support contact — with clear titles, step-by-step solutions, troubleshooting trees, and SEO-friendly structure.
metadata:
  displayName: "Knowledge Base Article"
  categories: ["communication", "business"]
  tags: ["knowledge-base", "support", "self-service", "help-center", "troubleshooting"]
  worksWellWithAgents: ["code-explainer", "codebase-onboarder", "customer-success-manager", "support-engineer", "technical-writer"]
  worksWellWithSkills: ["bug-report-writing"]
---

# Knowledge Base Article

## Before you start

Gather the following from the user before writing:

1. **What question or problem does this article answer?** (Exact customer phrasing, not internal jargon)
2. **Who is the reader?** (End user, admin, developer, or mixed audience)
3. **What product area does this cover?** (Feature name, settings page, API endpoint)
4. **What is the current resolution path?** (Steps support agents follow today, existing macros or scripts)
5. **Are there multiple causes or variations?** (Different root causes that produce the same symptom)

If the user says "write an article about billing," push back: "Which billing problem? A KB article solves one specific issue. 'Why was I charged twice' is a different article from 'How to update my payment method.'"

## Article template

### Title

Use the format customers would type into a search bar. Start with "How to," "Why," or the symptom itself.

**Good**: "How to reset your password when the reset email does not arrive"
**Bad**: "Password Reset Functionality" or "Authentication Troubleshooting Guide"

Test: if a customer pastes the title into Google, it should match their intent exactly.

### Overview

1-2 sentences confirming the reader is in the right place. Restate the problem in plain language and preview the solution. Include the product area and approximate time to resolve.

```
If you requested a password reset email and it has not arrived after 5 minutes,
this article walks you through three checks to resolve it (about 2 minutes).
```

### Applies to

State the product version, plan tier, platform, or role this article covers. Customers who do not match should know immediately that this article is not for them.

### Step-by-Step Solution

Number every step. Each step must include:

- One action per step (click, navigate, enter, select)
- The exact UI label or menu path: **Settings > Account > Security**
- What the user should see after completing the step (confirmation message, changed state)
- A screenshot or annotated image reference where the UI is not obvious

Use conditional branches when the problem has multiple causes:

```
3. Check your spam/junk folder for an email from noreply@example.com.
   - IF the email is in spam: Mark it as "Not spam," then click the reset link.
     You are done — skip to Verification below.
   - IF the email is not in spam: Continue to step 4.
```

Every branch must end at a resolution or route to the next diagnostic step. Never leave the reader stranded.

### Troubleshooting

Use a decision-tree format for cases where the primary solution does not work. Structure as symptom-then-action pairs:

| Still seeing this? | Try this |
|---|---|
| Reset link says "expired" | Request a new reset — links expire after 30 minutes |
| "Email not found" error | Verify you are using the email tied to your account under **Profile > Email** |
| No error but no email after 15 min | Contact support with your account email and the timestamp of your last attempt |

### Related articles

Link 2-4 articles covering adjacent topics. Customers who landed on the wrong article should find the right one without going back to search.

## Quality checklist

Before delivering the article, verify:

- [ ] Title matches the phrase a customer would search for, not internal terminology
- [ ] Overview confirms the reader has the right article within the first two sentences
- [ ] Every step contains one action, the exact UI path, and the expected result
- [ ] Conditional branches resolve to a next step, a solution, or a support escalation
- [ ] Troubleshooting covers the top 3 failure modes after the primary solution
- [ ] "Applies to" section scopes the article to specific versions, plans, or roles
- [ ] No internal jargon remains — every term is one the customer would use or is defined on first use
- [ ] Related articles link to adjacent problems, not random content

## Common mistakes

- **Writing for internal teams, not customers.** "Clear the OAuth token cache and re-authenticate via SSO" means nothing to a non-technical user. Write "Log out, close your browser, open it again, and log back in."
- **Combining multiple problems in one article.** "Billing FAQ" with 12 questions gets poor search rankings and forces readers to scroll. One article, one problem.
- **Skipping the 'Applies to' section.** Customers on the free plan waste time following steps that require a paid feature. State the scope upfront.
- **Instructions without verification.** "Click Save" is incomplete. "Click Save. A green banner reading 'Settings updated' appears at the top of the page" lets the reader confirm success.
- **Using screenshots as the only instruction.** Screenshots go stale when the UI changes. Write the text instructions first; screenshots supplement, never replace.
- **Forgetting the dead-end reader.** If every troubleshooting path fails, the article must tell the reader exactly how to contact support and what information to include.
