# Category Evolution System — Design Spec

**Goal:** Replace the hardcoded category list with a single source-of-truth file (`categories.yml`) at the repo root, enabling contributors to propose new categories (or remove obsolete ones) via PR. CI enforces full bidirectional integrity and file sync.

**Architecture:** `categories.yml` is the authority. The Python validator in `validate-pr.yml` reads it at runtime. CI checks that all downstream files (CONTRIBUTING.md, issue templates) stay in sync. Contributors propose changes via PR with justification in the PR description.

---

## Source of Truth: `categories.yml`

Location: repo root (`/categories.yml`).

Format:

```yaml
categories:
  - slug: engineering
    displayName: Engineering
    description: Software development, infrastructure, DevOps, and technical architecture

  - slug: business
    displayName: Business
    description: Sales, marketing, finance, legal, and business operations

  - slug: product-management
    displayName: Product Management
    description: Product strategy, requirements, roadmaps, and user research

  - slug: project-management
    displayName: Project Management
    description: Scrum, sprint planning, program management, and delivery coordination

  - slug: design
    displayName: Design
    description: UI/UX design, accessibility, visual design, and design systems

  - slug: data
    displayName: Data
    description: Data science, analytics, machine learning, and data engineering

  - slug: communication
    displayName: Communication
    description: Technical writing, content strategy, developer advocacy, and training

  - slug: security
    displayName: Security
    description: Application security, compliance, auditing, and threat modeling

  - slug: leadership
    displayName: Leadership
    description: Engineering management, people ops, hiring, and executive advisory

  - slug: operations
    displayName: Operations
    description: SRE, incident management, release management, and cloud operations
```

### Self-validation rules

- Each entry must have `slug`, `displayName`, and `description` (all non-empty strings)
- `slug` must match pattern `^[a-z][a-z0-9-]*$` (same as entry `name` fields)
- No duplicate slugs
- File must parse as valid YAML

---

## CI Validation: 6 Checks

### Check 1: Entry categories exist in categories.yml (adapted from existing)

Every category in every agent/skill frontmatter must exist as a slug in `categories.yml`.

Error: `Invalid category: 'ai-ml'. Not found in categories.yml. See categories.yml for the allowed list, or propose a new category by adding it in the same PR.`

### Check 2: Max 2 categories per entry (new)

Each entry's `categories` array must have at most 2 items.

Error: `Too many categories: found 3 (max 2). Pick the 1-2 categories where this entry fits best.`

### Check 3: Every category in categories.yml is used (new)

Every slug in `categories.yml` must be referenced by at least one agent or skill. Prevents speculative categories and catches stale categories after entries are re-categorized or removed.

Error: `Category 'ai-ml' is defined in categories.yml but not used by any agent or skill. Either add an entry that uses it or remove it from categories.yml.`

### Check 4: CONTRIBUTING.md lists match categories.yml (new)

The categories listed in the Frontmatter Rules table row for `metadata.categories` in CONTRIBUTING.md must exactly match the slugs in `categories.yml` (order-independent).

Error: `CONTRIBUTING.md categories are out of sync with categories.yml. Missing: ai-ml. Extra: none. Update the metadata.categories row in CONTRIBUTING.md to match.`

### Check 5: Issue template dropdowns match categories.yml (new)

The dropdown options in `.github/ISSUE_TEMPLATE/propose-agent.yml` and `propose-skill.yml` must exactly match the slugs in `categories.yml` (order-independent).

Error: `propose-agent.yml category dropdown is out of sync with categories.yml. Missing: ai-ml. Update the options list to match.`

### Check 6: categories.yml self-validation (new)

The file itself is validated for structure, slug patterns, no duplicates, and required fields.

Error: `categories.yml: entry 3 is missing required field 'description'.`

---

## Trigger Scope

The `validate-pr.yml` workflow trigger paths expand to:

```yaml
on:
  pull_request_target:
    paths:
      - "agents/**"
      - "skills/**"
      - "categories.yml"
      - "CONTRIBUTING.md"
      - ".github/ISSUE_TEMPLATE/**"
```

---

## Contributor Flow: Adding a Category

1. Create a PR that:
   - Adds the new category to `categories.yml` (slug, displayName, description)
   - Updates the `metadata.categories` row in `CONTRIBUTING.md`
   - Adds the category to the dropdown in `.github/ISSUE_TEMPLATE/propose-agent.yml`
   - Adds the category to the dropdown in `.github/ISSUE_TEMPLATE/propose-skill.yml`
   - Includes at least one agent or skill that uses the new category
2. PR description explains why existing categories are insufficient
3. CI validates all 6 checks
4. Maintainers review justification, category definition, and entry fit

## Contributor Flow: Removing a Category

1. Create a PR that:
   - Removes the category from `categories.yml`
   - Re-categorizes all agents and skills that used it
   - Updates the `metadata.categories` row in `CONTRIBUTING.md`
   - Removes the category from both issue template dropdowns
2. PR description explains why the category is being removed
3. CI validates all 6 checks (no orphaned references, no missing categories)
4. Maintainers review

---

## CONTRIBUTING.md: New Section

A new section titled **"Proposing Category Changes"** is added after the "Cross-References" section.

Content:

### Proposing Category Changes

Categories are defined in [`categories.yml`](categories.yml) at the repo root. To add or remove a category, submit a PR that updates all synced files. CI enforces that everything stays in sync.

**Adding a category checklist:**

- [ ] Add the category to `categories.yml` with `slug`, `displayName`, and `description`
- [ ] Update the `metadata.categories` row in the Frontmatter Rules table in this file
- [ ] Add the category to the dropdown in `.github/ISSUE_TEMPLATE/propose-agent.yml`
- [ ] Add the category to the dropdown in `.github/ISSUE_TEMPLATE/propose-skill.yml`
- [ ] Include at least one agent or skill that uses the new category in the same PR
- [ ] Explain in the PR description why existing categories are insufficient

**Removing a category checklist:**

- [ ] Remove the category from `categories.yml`
- [ ] Re-categorize all agents and skills that used it
- [ ] Update the `metadata.categories` row in this file
- [ ] Remove the category from both issue template dropdowns
- [ ] Explain in the PR description why the category is being removed

CI enforces that all 4 files stay in sync and that every category has at least one entry. Your PR will fail if any file is missed.

---

## CLAUDE.md Updates

Both `agents/CLAUDE.md` and `skills/CLAUDE.md` currently describe `metadata.categories` as "Filterable categories. An agent/skill can belong to multiple." They should be updated to:

- Reference `categories.yml` as the source of truth for allowed values
- State the max 2 categories constraint
- Example: "Filterable categories. See [`categories.yml`](../categories.yml) for the allowed list. Max 2 per entry."

---

## Sync Check Parsing Approach

**Check 4 (CONTRIBUTING.md):** The validator extracts category slugs from the `metadata.categories` row by finding the line containing `metadata.categories` in a markdown table and parsing the backtick-delimited slugs from that row (e.g., `` `engineering`, `business`, ... ``).

**Check 5 (issue templates):** The validator reads the YAML `options:` list under the dropdown field with `id: primary-category` in each issue template file.

Both checks compare the extracted set against the slugs in `categories.yml` and report any differences (missing or extra).

---

## What Doesn't Change

- Tags remain freeform (the two-tier system stays)
- Existing 10 categories become the initial content of `categories.yml`
- Cross-reference validation is unaffected
- Markdown linting is unaffected

---

## Files to Create or Modify

```
Create: categories.yml
Modify: .github/workflows/validate-pr.yml (read categories.yml, add checks 2-6, expand trigger paths)
Modify: CONTRIBUTING.md (reference categories.yml in frontmatter table, add "Proposing Category Changes" section)
Modify: agents/CLAUDE.md (reference categories.yml instead of inline list)
Modify: skills/CLAUDE.md (reference categories.yml instead of inline list)
```
