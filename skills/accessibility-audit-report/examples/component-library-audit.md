# Example: Design System Component Library Audit

## Executive Summary

This audit evaluated 8 reusable components in the Acme Design System (v3.2) against WCAG 2.1 AA. We identified 19 issues: 3 critical, 5 major, 8 minor, and 3 best-practice recommendations. The most critical finding is that the DatePicker component is entirely inaccessible to keyboard and screen reader users — it cannot be opened, navigated, or operated without a mouse.

## Scope & Methodology

```
Tested components: Button, Modal, DatePicker, Dropdown (Select), Tabs, Toast, Tooltip, DataTable
Not tested: Layout primitives (Grid, Stack, Container), typography components, icon set
Testing context: Components rendered in Storybook isolation (v7.6) with default props and key variant combinations
Methods: axe-core 4.9 on Storybook stories, NVDA 2024.1 + Chrome 124, VoiceOver + Safari 17.4, manual keyboard navigation through all interactive states
```

**Key difference from a flow audit**: This audit tests components in isolation and across all variant combinations. Each component is evaluated independently, then common cross-component patterns (focus management, announcement patterns, color usage) are assessed for consistency.

## Summary of Findings

| # | Issue | WCAG Criterion | Severity | Component |
|---|-------|---------------|----------|-----------|
| 1 | DatePicker calendar grid not keyboard-operable | 2.1.1 Keyboard | Critical | DatePicker |
| 2 | DatePicker selected date not announced to screen readers | 4.1.2 Name, Role, Value | Critical | DatePicker |
| 3 | Modal does not return focus to trigger on close | 2.4.3 Focus Order | Critical | Modal |
| 4 | Dropdown options have insufficient contrast in dark mode | 1.4.3 Contrast (Minimum) | Major | Dropdown |
| 5 | Toast messages not announced to screen readers | 4.1.3 Status Messages | Major | Toast |
| 6 | DataTable sort controls have no accessible labels | 4.1.2 Name, Role, Value | Major | DataTable |
| 7 | Tooltip not dismissible with Escape key | 1.4.13 Content on Hover or Focus | Major | Tooltip |
| 8 | Tabs panel content not associated with tab via aria-controls | 1.3.1 Info and Relationships | Major | Tabs |
| 9 | Button focus indicator contrast below 3:1 | 2.4.7 Focus Visible | Minor | Button |
| 10 | Modal heading not programmatically set as dialog label | 1.3.1 Info and Relationships | Minor | Modal |
| 11 | Dropdown placeholder text contrast is 3.8:1 | 1.4.3 Contrast (Minimum) | Minor | Dropdown |
| 12 | DataTable empty state uses color alone to convey "no data" | 1.4.1 Use of Color | Minor | DataTable |
| 13 | Tabs do not support arrow key navigation between tabs | 2.1.1 Keyboard | Minor | Tabs |
| 14 | Toast close button has no visible label | 4.1.2 Name, Role, Value | Minor | Toast |
| 15 | Tooltip has 200ms delay that cannot be configured | 1.4.13 Content on Hover or Focus | Minor | Tooltip |
| 16 | Button disabled state uses opacity alone (no cursor or text change) | 1.4.1 Use of Color | Minor | Button |
| 17 | Modal should use `<dialog>` element for native behavior | Best Practice | Note | Modal |
| 18 | DataTable should announce sort state changes | Best Practice | Note | DataTable |
| 19 | All components should support `prefers-reduced-motion` | Best Practice | Note | Global |

## Detailed Findings

### Finding #1: DatePicker calendar grid not keyboard-operable

- **WCAG Criterion**: 2.1.1 Keyboard
- **Severity**: Critical
- **Affected Element**: `DatePicker > .calendar-grid`
- **Description**: The calendar grid renders day cells as `<span>` elements with only `onClick` handlers. Keyboard users cannot tab into the grid, and once the popover opens, there is no keyboard mechanism to navigate between days, weeks, or months. The input field accepts typed dates, but the calendar picker — which is the primary interaction pattern — is mouse-only.
- **Remediation**: Implement the calendar as a grid of `<button>` elements (or `<td>` with `role="gridcell"` and `tabindex`) following the WAI-ARIA APG Date Picker pattern. Support arrow keys for day navigation, Page Up/Down for month navigation, and Home/End for first/last day of the month.
- **Code Example**:

```html
<!-- Before (inaccessible) -->
<div class="calendar-grid">
  <span class="day" onclick="selectDay(15)">15</span>
  <span class="day" onclick="selectDay(16)">16</span>
</div>

<!-- After (accessible) -->
<table role="grid" aria-label="March 2026">
  <tr>
    <td>
      <button tabindex="-1" aria-label="March 15, 2026">15</button>
    </td>
    <td>
      <button tabindex="0" aria-selected="true" aria-label="March 16, 2026, selected">16</button>
    </td>
  </tr>
</table>
```

### Finding #2: DatePicker selected date not announced to screen readers

- **WCAG Criterion**: 4.1.2 Name, Role, Value
- **Severity**: Critical
- **Affected Element**: `DatePicker > input.date-display`
- **Description**: When a date is selected via the calendar, the input field value updates visually, but the change is not announced to screen readers. The input lacks `aria-live` or a mechanism to notify assistive technology that the value changed programmatically. Screen reader users selecting a date hear nothing and cannot confirm their selection without navigating away and back.
- **Remediation**: Add `aria-live="polite"` to a visually hidden status region that announces the selected date. Alternatively, ensure the input fires a change event that screen readers detect.
- **Code Example**:

```html
<!-- Before -->
<input class="date-display" value="03/16/2026" readonly />

<!-- After -->
<input class="date-display" value="03/16/2026" readonly aria-describedby="date-status" />
<span id="date-status" role="status" class="sr-only">Selected date: March 16, 2026</span>
```

### Finding #3: Modal does not return focus to trigger on close

- **WCAG Criterion**: 2.4.3 Focus Order
- **Severity**: Critical
- **Affected Element**: `Modal` component, close handler
- **Description**: When a Modal is closed (via close button, Escape key, or overlay click), focus moves to the top of the page (`<body>`) instead of returning to the element that triggered the modal. Keyboard users lose their place in the page and must tab through the entire document to return to where they were. This is disorienting for sighted keyboard users and completely disruptive for screen reader users.
- **Remediation**: Store a reference to `document.activeElement` when the modal opens. On close, call `.focus()` on the stored element. If the trigger element has been removed from the DOM, focus the nearest logical ancestor.
- **Code Example**:

```jsx
// Before
function closeModal() {
  setIsOpen(false);
}

// After
function openModal() {
  triggerRef.current = document.activeElement;
  setIsOpen(true);
}

function closeModal() {
  setIsOpen(false);
  triggerRef.current?.focus();
}
```

### Finding #4: Dropdown options have insufficient contrast in dark mode

- **WCAG Criterion**: 1.4.3 Contrast (Minimum)
- **Severity**: Major
- **Affected Element**: `Dropdown > .option-item` (dark mode variant)
- **Description**: In dark mode, dropdown option text renders as `#9CA3AF` (gray-400) on `#1F2937` (gray-800), producing a contrast ratio of 3.6:1. WCAG AA requires 4.5:1 for normal text. The hover state improves to 5.2:1, but the default (non-hovered) state fails. Users with low vision or in bright ambient light cannot reliably read option text.
- **Remediation**: Change option text color in dark mode to `#D1D5DB` (gray-300) or lighter, achieving at least 4.5:1 against the dark background.

### Finding #5: Toast messages not announced to screen readers

- **WCAG Criterion**: 4.1.3 Status Messages
- **Severity**: Major
- **Affected Element**: `Toast` container
- **Description**: Toast notifications (success, error, info) appear visually but are not placed in an ARIA live region. Screen reader users are unaware that a toast has appeared. For error toasts especially, users may not know an action failed.
- **Remediation**: Render toasts inside a persistent `aria-live="polite"` region for informational toasts and `role="alert"` for error toasts. The live region container must exist in the DOM before content is injected.
- **Code Example**:

```html
<!-- Container exists at mount time, empty -->
<div aria-live="polite" class="toast-announcer sr-only"></div>

<!-- When toast appears, inject announcement -->
<div aria-live="polite" class="toast-announcer sr-only">
  Settings saved successfully.
</div>
```

### Finding #6: DataTable sort controls have no accessible labels

- **WCAG Criterion**: 4.1.2 Name, Role, Value
- **Severity**: Major
- **Affected Element**: `DataTable > th > .sort-icon`
- **Description**: Column headers contain a clickable sort icon (up/down chevron SVG) that toggles ascending/descending sort. The icon has no `aria-label`, the current sort direction is not exposed, and the `<th>` element is not marked as interactive. Screen reader users hear the column name but have no indication that it is sortable or what the current sort state is.
- **Remediation**: Make the column header a `<button>` (or add `role="button"` with `tabindex="0"`). Add `aria-sort="ascending"`, `"descending"`, or `"none"` to the `<th>`. Add `aria-label` to describe the action: "Sort by Name, currently ascending."

### Finding #7: Tooltip not dismissible with Escape key

- **WCAG Criterion**: 1.4.13 Content on Hover or Focus
- **Severity**: Major
- **Affected Element**: `Tooltip` component
- **Description**: When a tooltip appears on hover or focus, pressing Escape does nothing. Users must move their mouse or shift focus to dismiss it. This fails WCAG 1.4.13 which requires that additional content triggered by hover/focus is dismissible without moving pointer or focus.
- **Remediation**: Add a `keydown` listener for Escape that hides the tooltip while maintaining current focus position.

### Finding #8: Tabs panel content not associated with tab via aria-controls

- **WCAG Criterion**: 1.3.1 Info and Relationships
- **Severity**: Major
- **Affected Element**: `Tabs > [role="tab"]` and `Tabs > [role="tabpanel"]`
- **Description**: Tab elements have `role="tab"` and panels have `role="tabpanel"`, but the relationship between them is not established. Tabs are missing `aria-controls` pointing to the panel ID, and panels are missing `aria-labelledby` pointing to the tab ID. Screen reader users cannot programmatically determine which panel belongs to which tab.
- **Remediation**: Add `id` to each tab and panel. Set `aria-controls="panel-{n}"` on each tab and `aria-labelledby="tab-{n}"` on each panel.

### Finding #9: Button focus indicator contrast below 3:1

- **WCAG Criterion**: 2.4.7 Focus Visible
- **Severity**: Minor
- **Affected Element**: `Button` component, all variants
- **Description**: The Button's focus ring uses a 1px `box-shadow` with `rgba(59, 130, 246, 0.5)` (semi-transparent blue). Against a white background, the effective contrast is approximately 2.1:1. Against colored button variants, contrast drops further. Keyboard users have difficulty identifying which button is focused.
- **Remediation**: Use a solid 2px outline with `outline-offset: 2px` in a color that achieves 3:1 against all adjacent backgrounds. Example: `outline: 2px solid #2563EB; outline-offset: 2px`.

### Finding #10-16: Minor Findings (abbreviated)

**#10 — Modal heading not set as dialog label**: Add `aria-labelledby` on the `<div role="dialog">` pointing to the heading element's `id`.

**#11 — Dropdown placeholder contrast**: Placeholder text "Select an option" at 3.8:1 is below the 4.5:1 requirement. Darken to `#6B7280` or darker.

**#12 — DataTable empty state uses color alone**: The "No data available" message uses gray text with no icon. Add a visual indicator (icon or illustration) alongside the text.

**#13 — Tabs lack arrow key navigation**: Per the WAI-ARIA Tabs pattern, Left/Right arrow keys should move between tabs. Currently only Tab key works, which exits the tab list entirely.

**#14 — Toast close button has no visible label**: The X icon button needs `aria-label="Dismiss notification"`.

**#15 — Tooltip delay not configurable**: The hardcoded 200ms hover delay may be too short for users with motor impairments. Expose a `delay` prop.

**#16 — Button disabled state uses opacity alone**: Disabled buttons use `opacity: 0.5` with no other visual change. Add `cursor: not-allowed` and consider a text label or pattern to reinforce the disabled state beyond opacity.

### Finding #17-19: Best Practice Recommendations

**#17 — Modal should use native `<dialog>`**: The current `<div role="dialog">` implementation requires manual focus trapping and backdrop handling. The native `<dialog>` element with `showModal()` handles focus trapping, backdrop, and Escape key natively.

**#18 — DataTable should announce sort changes**: After sorting, add a polite live region announcement: "Table sorted by Name, ascending." This helps screen reader users confirm their action took effect.

**#19 — Support `prefers-reduced-motion`**: Several components (Modal open/close, Toast slide-in, Tooltip fade) use CSS transitions. Wrap animations in `@media (prefers-reduced-motion: no-preference)` so users who have requested reduced motion get instant state changes.

## Remediation Priority Matrix

| | Low Effort | High Effort |
|---|-----------|-------------|
| **High Impact** | #3 Focus return on modal close, #5 Toast live region, #6 DataTable sort labels, #7 Tooltip Escape key, #8 Tabs aria-controls, #10 Modal aria-labelledby | #1 DatePicker keyboard nav rebuild, #2 DatePicker screen reader announce |
| **Low Impact** | #9 Button focus ring, #11 Dropdown placeholder contrast, #12 DataTable empty state, #14 Toast close label, #16 Button disabled state | #4 Dropdown dark mode contrast (requires design token update), #13 Tabs arrow key pattern, #15 Tooltip delay prop |

## Recommended Timeline

```
Week 1:   Critical findings — DatePicker keyboard + screen reader (#1, #2), Modal focus return (#3)
Week 2:   Major findings — Toast live region (#5), DataTable sort labels (#6), Tooltip Escape (#7), Tabs aria-controls (#8)
Week 3:   Major findings — Dropdown dark mode contrast (#4)
Week 4-6: Minor findings, prioritized by the matrix above
Ongoing:  Best-practice recommendations integrated into component contribution guidelines
```

**Regression prevention**: Add `@axe-core/playwright` checks to every component's Storybook test. Gate PR merges on zero critical/major axe violations. Document the expected ARIA pattern (from WAI-ARIA APG) in each component's README.
