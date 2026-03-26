# Accessibility Audit Report: Signup Flow

## 1. Executive Summary

This audit evaluated 5 screens across the signup flow (`/signup`, `/verify-email`, `/create-org`, `/invite-team`, `/onboarding-complete`) against WCAG 2.1 AA. We identified 11 issues: 2 critical, 4 major, 3 minor, and 2 best-practice recommendations. The most critical finding is that the email verification code input is built with non-semantic `<div>` elements, making it completely inaccessible to screen reader and keyboard-only users.

## 2. Scope & Methodology

```
Tested: /signup, /verify-email, /create-org, /invite-team, /onboarding-complete
Not tested: Login, password reset, account settings
Methods: axe-core 4.10, NVDA 2025.1 + Chrome 124, VoiceOver + Safari 17.4,
         manual keyboard navigation, colour contrast analyzer (CCA)
Date: March 2026
```

## 3. Summary of Findings

| # | Issue | WCAG Criterion | Severity | Page |
|---|-------|---------------|----------|------|
| 1 | Verification code input not keyboard accessible | 2.1.1 Keyboard | Critical | /verify-email |
| 2 | Form errors not announced to screen readers | 4.1.3 Status Messages | Critical | /signup |
| 3 | Password requirements not programmatically associated | 1.3.1 Info and Relationships | Major | /signup |
| 4 | "Create organization" button has no accessible name | 4.1.2 Name, Role, Value | Major | /create-org |
| 5 | Stepper component not conveyed to assistive tech | 1.3.1 Info and Relationships | Major | All |
| 6 | Low contrast on placeholder text | 1.4.3 Contrast (Minimum) | Major | /signup, /create-org |
| 7 | Focus not moved to error summary on submission | 3.3.1 Error Identification | Minor | /signup |
| 8 | Decorative icons missing `aria-hidden` | 1.1.1 Non-text Content | Minor | /invite-team |
| 9 | Link text "Click here" is ambiguous | 2.4.4 Link Purpose | Minor | /verify-email |
| 10 | No skip-to-content link | 2.4.1 Bypass Blocks | Best Practice | All |
| 11 | Success animation ignores `prefers-reduced-motion` | 2.3.3 Animation from Interactions | Best Practice | /onboarding-complete |

## 4. Detailed Findings

### Finding #1: Verification code input not keyboard accessible

- **WCAG Criterion**: 2.1.1 Keyboard
- **Severity**: Critical
- **Affected Element**: `.verify-code-input` on `/verify-email`
- **Description**: The 6-digit verification code input is built with styled `<div>` elements that capture click events via JavaScript. Keyboard users cannot tab into the fields or type a code. Screen readers announce nothing. This blocks all keyboard and screen reader users from completing signup.
- **Remediation**: Replace the `<div>` elements with six `<input type="text" inputmode="numeric" maxlength="1">` elements, grouped within a `<fieldset>` with a `<legend>`. Manage focus to auto-advance on input.
- **Code Example**:
```html
<!-- Before -->
<div class="verify-code-input">
  <div class="code-digit" onclick="focusDigit(0)"></div>
  <div class="code-digit" onclick="focusDigit(1)"></div>
</div>

<!-- After -->
<fieldset>
  <legend>Enter your 6-digit verification code</legend>
  <input type="text" inputmode="numeric" maxlength="1" aria-label="Digit 1 of 6">
  <input type="text" inputmode="numeric" maxlength="1" aria-label="Digit 2 of 6">
</fieldset>
```

### Finding #2: Form errors not announced to screen readers

- **WCAG Criterion**: 4.1.3 Status Messages
- **Severity**: Critical
- **Affected Element**: `.form-error-message` on `/signup`
- **Description**: When the signup form is submitted with invalid data, error messages appear visually below each field but are not announced by screen readers. Users relying on NVDA or VoiceOver do not know their submission failed or why.
- **Remediation**: Add `role="alert"` to the error container, or use `aria-live="assertive"` so messages are announced on appearance. Associate each error with its field using `aria-describedby`.

### Finding #6: Low contrast on placeholder text

- **WCAG Criterion**: 1.4.3 Contrast (Minimum)
- **Severity**: Major
- **Affected Element**: `input::placeholder` on `/signup` and `/create-org`
- **Description**: Placeholder text uses `#C4C4C4` on `#FFFFFF`, yielding a contrast ratio of 1.6:1 (requires 4.5:1). Users with low vision cannot read the placeholder examples.
- **Remediation**: Change placeholder color to `#717171` or darker to achieve at least 4.5:1 contrast.

## 5. Remediation Priority Matrix

| | Low Effort | High Effort |
|---|-----------|-------------|
| **High Impact** | #2 (add `role="alert"`), #4 (add `aria-label`), #6 (fix color), #8 (`aria-hidden`) | #1 (rebuild verification input), #5 (rebuild stepper with ARIA) |
| **Low Impact** | #9 (rewrite link text), #10 (add skip link) | #3 (restructure password hints), #7 (focus management), #11 (motion query) |

## 6. Recommended Timeline

```
Week 1:    Critical findings #1, #2
Week 2-3:  Major findings #3, #4, #5, #6
Week 4:    Minor findings #7, #8, #9
Ongoing:   Best-practice items #10, #11 integrated into design system
```

**Regression prevention**: Add `axe-core` to the CI pipeline. Require all new form components to pass keyboard navigation and screen reader smoke tests before merge.
