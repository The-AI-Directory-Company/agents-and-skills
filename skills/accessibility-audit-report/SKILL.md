---
name: accessibility-audit-report
description: Write structured accessibility audit reports with findings mapped to WCAG criteria, severity levels, affected components, remediation steps, and a prioritized fix timeline.
metadata:
  displayName: "Accessibility Audit Report"
  categories: ["design", "engineering"]
  tags: ["accessibility", "a11y", "WCAG", "audit-report", "remediation", "compliance"]
  worksWellWithAgents: ["accessibility-auditor", "code-reviewer", "ux-researcher"]
  worksWellWithSkills: ["component-design-spec", "ticket-writing"]
---

# Accessibility Audit Report

## Before you start

Gather the following from the user. If anything is missing, ask before proceeding:

1. **Scope** — Which pages, flows, or components are being audited? (e.g., "checkout flow", "marketing site", "design system")
2. **Target conformance level** — WCAG 2.1 AA (most common), WCAG 2.2 AA, or AAA?
3. **Testing methods used** — Automated tools (axe, Lighthouse), manual keyboard/screen reader testing, user testing with disabled participants?
4. **Tech stack** — Framework, component library, and any existing a11y tooling in the pipeline
5. **Audience context** — Is there a legal compliance deadline, a known user complaint, or a proactive audit?

If the user says "just audit everything," push back: "Which user flows are highest traffic or highest risk? Start there — a focused audit produces actionable results, a broad audit produces a backlog nobody reads."

## Audit report template

### 1. Executive Summary

3-5 sentences. State the overall conformance status, the number of issues found by severity, and the single most critical finding. This section is for stakeholders who will not read the full report.

```
This audit evaluated 12 screens across the checkout flow against WCAG 2.1 AA.
We identified 23 issues: 4 critical, 7 major, 9 minor, and 3 best-practice
recommendations. The most critical finding is that the payment form is entirely
inaccessible to keyboard-only users, blocking approximately 8% of users from
completing purchases.
```

### 2. Scope & Methodology

List what was tested, what was not, and how. Be explicit about tools and versions.

```
Tested: /cart, /checkout/shipping, /checkout/payment, /checkout/confirmation
Not tested: Account settings, admin dashboard
Methods: axe-core 4.9, NVDA 2024.1 + Chrome, VoiceOver + Safari, manual
keyboard navigation, color contrast analyzer
```

### 3. Summary of Findings

Provide a scannable table. Every issue in the report must appear here.

| # | Issue | WCAG Criterion | Severity | Component/Page |
|---|-------|---------------|----------|----------------|
| 1 | Payment form not keyboard accessible | 2.1.1 Keyboard | Critical | /checkout/payment |
| 2 | Images missing alt text | 1.1.1 Non-text Content | Major | /cart |
| 3 | Insufficient color contrast on helper text | 1.4.3 Contrast (Minimum) | Minor | Global |

### 4. Detailed Findings

Write one section per issue. Every finding must include all six fields below — no exceptions.

#### Finding #[N]: [Short description]

- **WCAG Criterion**: [Number + Name] (e.g., 2.1.1 Keyboard)
- **Severity**: Critical / Major / Minor / Best Practice
- **Affected Element**: [CSS selector, component name, or page URL]
- **Description**: What the problem is, who it affects, and what the user experiences. Be specific — "screen reader users cannot determine the purpose of this button" not "button is inaccessible."
- **Remediation**: Step-by-step fix. Include the specific ARIA attribute, HTML element, or CSS property needed.
- **Code Example**:

```html
<!-- Before (inaccessible) -->
<div onclick="submit()">Pay Now</div>

<!-- After (accessible) -->
<button type="submit">Pay Now</button>
```

Severity definitions:

| Severity | Meaning |
|----------|---------|
| **Critical** | Blocks a user group from completing a core task. Fix immediately. |
| **Major** | Causes significant difficulty but a workaround exists. Fix within current sprint. |
| **Minor** | Causes inconvenience but does not block functionality. Fix within the quarter. |
| **Best Practice** | Not a WCAG violation but improves the experience. Schedule as capacity allows. |

### 5. Remediation Priority Matrix

Group findings by effort and impact to help the team sequence work.

| | Low Effort | High Effort |
|---|-----------|-------------|
| **High Impact** | Fix first (e.g., missing alt text, missing labels) | Plan next (e.g., rebuild inaccessible custom widget) |
| **Low Impact** | Quick wins (e.g., skip-to-content link) | Backlog (e.g., ARIA live region for non-critical notifications) |

### 6. Recommended Timeline

Map findings to concrete timeframes tied to severity.

```
Week 1-2:  All Critical findings (#1, #4)
Week 3-4:  All Major findings (#2, #5, #7, #8, #10, #11, #12)
Week 5-8:  Minor findings, prioritized by the matrix above
Ongoing:   Best-practice recommendations integrated into component library
```

Include a note on regression prevention: "Add axe-core to CI. Every new component must pass automated a11y checks before merge."

## Quality checklist

Before delivering the report, verify:

- [ ] Every finding maps to a specific WCAG success criterion, not just a general principle
- [ ] Severity levels are consistent — same type of issue gets the same severity throughout the report
- [ ] Remediation steps are specific enough for a developer to implement without further research
- [ ] Code examples show before AND after, not just the correct version
- [ ] The summary table matches the detailed findings exactly — no orphaned or missing entries
- [ ] The executive summary includes a concrete number of issues and highlights the worst one
- [ ] The timeline is realistic given the severity distribution and team capacity
- [ ] Testing methodology is documented — another auditor could reproduce the findings

## Common mistakes to avoid

- **Listing the tool output as the report.** axe-core output is raw data, not a report. Every automated finding needs human interpretation: who is affected, how badly, and what to do about it.
- **Missing the keyboard test.** Automated tools catch roughly 30% of accessibility issues. If you only ran axe and Lighthouse, say so — and note that keyboard and screen reader testing is still needed.
- **Vague remediation.** "Make this accessible" is not a remediation step. "Add `aria-label="Close dialog"` to the `<button>` element at `.modal-close`" is.
- **Inconsistent severity.** If a missing alt text on a decorative image is "Critical" but a missing alt text on a product image is "Minor," your severity framework is broken. Define it once, apply it uniformly.
- **No prioritization.** A flat list of 40 findings paralyzes teams. The priority matrix and timeline exist to prevent this — always include them.
