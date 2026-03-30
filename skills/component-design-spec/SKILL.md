---
name: component-design-spec
description: Write component design specifications — defining props, states, interactions, accessibility requirements, and visual variants for design system components.
metadata:
  displayName: "Component Design Spec"
  categories: ["design", "engineering"]
  tags: ["components", "design-systems", "specifications", "UI", "accessibility"]
  worksWellWithAgents: ["frontend-engineer", "product-designer", "ui-designer", "vibe-coder"]
  worksWellWithSkills: ["accessibility-audit-report", "brand-guidelines", "ux-copy-guidelines"]
---

# Component Design Spec

## Before you start

Gather the following from the user. If anything is missing, ask before proceeding:

1. **What component is being specified?** — Name and one-sentence purpose
2. **Where does it appear?** — Pages, layouts, or parent components that will consume it
3. **What design system does it belong to?** — Existing system with tokens, or standalone
4. **What are the usage scenarios?** — The 2-5 most common ways this component will be used
5. **Are there existing implementations?** — Current components being replaced or extended
6. **What are the constraints?** — Framework, browser support, performance budgets, package size limits

## Spec template

### 1. Component Overview

```
Name:           [PascalCase component name]
Purpose:        [One sentence — what it does and why it exists]
Category:       [Primitive / Composite / Pattern]
Status:         [Proposed / In Review / Approved / Implemented]
```

Categories: **Primitive** (low-level, no domain logic: Button, Input), **Composite** (combines primitives: SearchField, DatePicker), **Pattern** (opinionated layout: DataTable, NavigationBar).

### 2. Props API

Define every prop with type, default, and description. Example format:

```typescript
interface ComponentProps {
  children: React.ReactNode;
  variant: 'primary' | 'secondary' | 'ghost' | 'danger';
  size?: 'sm' | 'md' | 'lg';   // default: 'md'
  disabled?: boolean;            // default: false
  loading?: boolean;             // default: false
  onClick?: (event: React.MouseEvent) => void;
}
```

Rules: name props after what they control (`variant="danger"` not `color="red"`), default booleans to `false`, use string literal enums, follow `onAction` callback convention. If >10 props, consider composition.

### 3. States

| State | Trigger | Visual Change | Behavior Change |
|-------|---------|---------------|-----------------|
| Default | Initial render | Base styling | Fully interactive |
| Hover | Mouse enter | Background darkens | Tooltip may appear |
| Focus | Keyboard tab | Focus ring visible | Accepts Enter/Space |
| Active | Mouse down / Enter | Scale down slightly | Action fires on release |
| Disabled | `disabled={true}` | Opacity reduced | No events fire |
| Loading | `loading={true}` | Spinner replaces icon | No events fire |
| Error | Validation failure | Red border, error icon | Error message shown |

Every interactive state must be visually distinguishable. Focus must be visible without hover. Disabled and loading must look different from each other.

### 4. Visual Variants

Map each variant to design tokens (never hardcoded values). For each variant, specify: background token, text token, border token, and usage guidance (e.g., "primary: one per view," "danger: destructive actions only"). Define a size scale mapping each size to height, horizontal padding, font size, and icon size.

### 5. Interaction Behavior

**Keyboard**: `Tab` to focus (skip if disabled), `Enter`/`Space` to activate, `Escape` to close associated popover.

**Mouse**: Single click activates. Double click behaves as single click unless specified otherwise.

**Touch**: Tap activates. Minimum 44x44px touch target.

**Focus management**: Focus follows DOM order. After activation, focus stays unless navigation occurs. Opening a popover/modal moves focus to the opened content.

### 6. Accessibility Requirements

Non-negotiable minimums:

- [ ] Correct ARIA role (e.g., `role="button"` for non-button elements acting as buttons)
- [ ] Accessible name via visible label, `aria-label`, or `aria-labelledby`
- [ ] State changes announced: `aria-disabled`, `aria-expanded`, `aria-pressed`
- [ ] Color contrast WCAG 2.1 AA: 4.5:1 text, 3:1 interactive borders
- [ ] Focus indicator with 3:1 contrast against adjacent colors
- [ ] Motion respects `prefers-reduced-motion`

Document expected screen reader output for each state (default, loading, disabled).

### 7. Composition Examples

Show common usage and at least one anti-pattern:

```jsx
{/* Correct: semantic variant */}
<Button variant="danger" onClick={handleDelete}>Delete Account</Button>

{/* WRONG: visual prop instead of semantic */}
<Button color="red" onClick={handleDelete}>Delete</Button>
```

Include examples for: basic usage, loading state, with icon, and the most complex supported composition.

## Quality checklist

Before delivering a component design spec, verify:

- [ ] Props API uses semantic names, not visual descriptions
- [ ] Every prop has a type, default value (if optional), and description
- [ ] All interactive states are documented with visual and behavioral changes
- [ ] Keyboard interactions are specified for every supported action
- [ ] Accessibility includes ARIA attributes, contrast ratios, and screen reader output
- [ ] Visual variants reference design tokens, not hardcoded values
- [ ] Examples show common use cases and at least one anti-pattern

## Common mistakes

- **Specifying visuals without states.** A spec showing only the default appearance is incomplete. Every component has hover, focus, active, disabled, and loading states at minimum.
- **Hardcoding colors instead of tokens.** `background: #3B82F6` breaks when the theme changes. Use token references.
- **Ignoring keyboard interaction.** Mouse-only components are broken for keyboard and screen reader users. Keyboard support is not optional.
- **Prop APIs that leak implementation.** Props like `className` or `style` break encapsulation. Expose semantic props instead.
- **Missing anti-pattern examples.** Developers learn from what NOT to do. Show incorrect usage alongside correct usage.
- **No screen reader verification.** Listing ARIA attributes is not enough. Document what the screen reader announces per state.
