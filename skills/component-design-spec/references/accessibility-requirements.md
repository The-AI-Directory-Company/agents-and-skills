# Accessibility Requirements Reference

Quick-reference for the accessibility requirements in component design specs. All thresholds target **WCAG 2.1 Level AA** compliance.

## Contrast Ratios

| Element | Minimum Ratio | Measured Against |
|---------|---------------|------------------|
| Normal text (< 18px / < 14px bold) | 4.5:1 | Adjacent background |
| Large text (>= 18px / >= 14px bold) | 3:1 | Adjacent background |
| Interactive component borders | 3:1 | Adjacent background |
| Focus indicator | 3:1 | Adjacent colors on both sides |
| Non-text graphics (icons, chart segments) | 3:1 | Adjacent background |
| Disabled elements | No minimum | Exempted by WCAG, but 2:1 recommended for readability |

Tools: use Chrome DevTools color picker, axe DevTools, or Stark plugin to verify. Do not eyeball contrast.

## ARIA Role Inventory

Map each component type to its correct role:

| Component Pattern | Role | Notes |
|-------------------|------|-------|
| Clickable non-button | `role="button"` | Must also handle `Enter` and `Space` keypress |
| Toggle button | `role="button"` + `aria-pressed` | `aria-pressed="true"` or `"false"` |
| Link styled as button | `role="link"` | Keep the `<a>` tag; do not override with `role="button"` |
| Text input | `role="textbox"` (implicit on `<input>`) | Add `aria-invalid` for error state |
| Checkbox | `role="checkbox"` + `aria-checked` | Use `"mixed"` for indeterminate |
| Radio group | `role="radiogroup"` wrapping `role="radio"` items | Arrow keys navigate within group |
| Dropdown select | `role="listbox"` + `role="option"` children | `aria-expanded` on the trigger |
| Combobox (autocomplete) | `role="combobox"` + `aria-expanded` + `aria-controls` | Announce suggestion count with `aria-live` |
| Modal dialog | `role="dialog"` + `aria-modal="true"` | Trap focus inside; return focus on close |
| Non-modal dialog (popover) | `role="dialog"` | Do not trap focus; `Escape` closes |
| Tab set | `role="tablist"` > `role="tab"` + `role="tabpanel"` | Arrow keys move between tabs |
| Accordion | Use `<details>`/`<summary>` or `role="button"` + `aria-expanded` | One section or multiple open — document which |
| Tooltip | `role="tooltip"` + `aria-describedby` | Must be dismissible with `Escape` |
| Alert/toast | `role="alert"` or `role="status"` | `role="alert"` is assertive; `role="status"` is polite |
| Progress bar | `role="progressbar"` + `aria-valuenow` | Include `aria-valuemin` and `aria-valuemax` |
| Slider | `role="slider"` + arrow key support | `aria-valuenow`, `aria-valuemin`, `aria-valuemax`, `aria-valuetext` |
| Breadcrumb | `role="navigation"` + `aria-label="Breadcrumb"` | Current page link gets `aria-current="page"` |
| Navigation menu | `role="navigation"` + `aria-label` | Distinguish multiple navs with unique labels |

When a native HTML element provides the semantics (e.g., `<button>`, `<input type="checkbox">`), use the native element. Only add ARIA roles when no native element fits.

## Required State Attributes

Every interactive component must expose its current state to assistive technology:

| State | Attribute | Values |
|-------|-----------|--------|
| Disabled | `aria-disabled="true"` | Preferred over HTML `disabled` when you need the element to remain focusable |
| Expanded/collapsed | `aria-expanded` | `"true"` / `"false"` |
| Selected | `aria-selected` | `"true"` / `"false"` (within `listbox`, `tablist`, `grid`) |
| Checked | `aria-checked` | `"true"` / `"false"` / `"mixed"` |
| Pressed (toggle) | `aria-pressed` | `"true"` / `"false"` |
| Invalid | `aria-invalid` | `"true"` / `"grammar"` / `"spelling"` |
| Busy/loading | `aria-busy="true"` | Set on the container being updated |
| Current | `aria-current` | `"page"` / `"step"` / `"location"` / `"date"` / `"true"` |

## Screen Reader Output Patterns

Document expected announcements for each component state. Format:

```
State: Default
  Announced: "[Accessible name], button"

State: Loading
  Announced: "[Accessible name], button, loading"
  (Requires aria-label update or aria-live region)

State: Disabled
  Announced: "[Accessible name], button, dimmed"
  (VoiceOver) / "button, unavailable" (NVDA)

State: Expanded (e.g., dropdown trigger)
  Announced: "[Accessible name], button, expanded"
  Then: focus moves to first option, announced as "[Option text], option, 1 of N"

State: Error (e.g., invalid input)
  Announced: "[Accessible name], edit text, invalid entry, [error message]"
  (Requires aria-describedby pointing to the error message element)
```

Test with at least two screen readers: VoiceOver (macOS/iOS) and NVDA or JAWS (Windows). Announcements vary between screen readers -- document differences when they affect comprehension.

## Focus Management Rules

1. **Tab order follows DOM order.** Do not use `tabindex` values greater than 0.
2. **Skip links**: Provide a "skip to main content" link as the first focusable element.
3. **Focus trapping**: Required inside modal dialogs. `Tab` from last element wraps to first; `Shift+Tab` from first wraps to last.
4. **Focus restoration**: When a dialog or popover closes, return focus to the element that opened it.
5. **Programmatic focus**: Use `element.focus()` only when the user's context shifts (opening a dialog, navigating to a new section). Never auto-focus on page load unless the page is a single-purpose form.
6. **Visible focus indicator**: Minimum 2px solid outline with 3:1 contrast. Never suppress with `outline: none` unless replacing with an equally visible custom indicator.

## Motion and Animation

- Wrap all animations in a `prefers-reduced-motion` media query.
- When reduced motion is preferred: replace slide/fade transitions with instant display, disable parallax, stop auto-playing carousels.
- Animation duration should not exceed 500ms for UI transitions.
- Never use animation as the sole means of communicating a state change.
