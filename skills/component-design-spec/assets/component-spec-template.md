# Component Spec Template

Copy this template to start a new component design specification.

---

## 1. Component Overview

```
Name:           [PascalCase component name]
Purpose:        [One sentence — what it does and why it exists]
Category:       [Primitive / Composite / Pattern]
Status:         [Proposed / In Review / Approved / Implemented]
Design system:  [Name of design system, or "standalone"]
```

## 2. Props API

```typescript
interface [ComponentName]Props {
  // Required props
  children: React.ReactNode;

  // Variant / appearance
  variant: '[variant1]' | '[variant2]';
  size?: '[sm]' | '[md]' | '[lg]';   // default: 'md'

  // State
  disabled?: boolean;                  // default: false
  loading?: boolean;                   // default: false

  // Callbacks
  onClick?: (event: React.MouseEvent) => void;
}
```

**Prop rules applied:**
- [ ] Names describe what they control, not visual output
- [ ] Booleans default to `false`
- [ ] String literal unions for constrained values
- [ ] `onAction` naming convention for callbacks
- [ ] Fewer than 10 props (consider composition otherwise)

## 3. States

| State | Trigger | Visual Change | Behavior Change |
|-------|---------|---------------|-----------------|
| Default | Initial render | [Describe] | [Describe] |
| Hover | Mouse enter | [Describe] | [Describe] |
| Focus | Keyboard tab | [Describe] | [Describe] |
| Active | Mouse down / Enter | [Describe] | [Describe] |
| Disabled | `disabled={true}` | [Describe] | [Describe] |
| Loading | `loading={true}` | [Describe] | [Describe] |
| Error | [Trigger] | [Describe] | [Describe] |

**Verification:**
- [ ] Every state is visually distinguishable
- [ ] Focus is visible without hover
- [ ] Disabled and loading look different from each other

## 4. Visual Variants

For each variant, map to semantic design tokens:

| Variant | Background Token | Text Token | Border Token | Usage Guidance |
|---------|-----------------|------------|--------------|----------------|
| [variant1] | `color.background.[...]` | `color.text.[...]` | `[...]` | [When to use] |
| [variant2] | `color.background.[...]` | `color.text.[...]` | `[...]` | [When to use] |

**Size scale:**

| Size | Height | Horizontal Padding | Font Size | Icon Size |
|------|--------|-------------------|-----------|-----------|
| sm | [token] | [token] | [token] | [token] |
| md | [token] | [token] | [token] | [token] |
| lg | [token] | [token] | [token] | [token] |

**Verification:**
- [ ] No hardcoded color, spacing, or size values — all tokens

## 5. Interaction Behavior

**Keyboard:**
- `Tab`: [Behavior]
- `Enter` / `Space`: [Behavior]
- `Escape`: [Behavior]
- `Arrow keys`: [Behavior, if applicable]

**Mouse:**
- Single click: [Behavior]
- Double click: [Behavior, or "same as single click"]

**Touch:**
- Tap: [Behavior]
- Minimum touch target: 44x44px

**Focus management:**
- Tab order: [Follows DOM / custom order]
- After activation: [Where does focus go?]
- Popover/modal: [Focus moves to opened content]

## 6. Accessibility Requirements

- [ ] ARIA role: `role="[...]"` (or native element: `<[element]>`)
- [ ] Accessible name: [visible label / `aria-label` / `aria-labelledby`]
- [ ] State announcements: [`aria-disabled`, `aria-expanded`, `aria-pressed`, etc.]
- [ ] Color contrast: 4.5:1 text, 3:1 borders (WCAG 2.1 AA)
- [ ] Focus indicator: 3:1 contrast against adjacent colors
- [ ] Motion: respects `prefers-reduced-motion`

**Screen reader output per state:**

```
State: Default
  Announced: "[Accessible name], [role]"

State: Loading
  Announced: "[Accessible name], [role], loading"

State: Disabled
  Announced: "[Accessible name], [role], dimmed" (VoiceOver)
              "[Accessible name], [role], unavailable" (NVDA)

State: [Other relevant states]
  Announced: "[...]"
```

## 7. Composition Examples

**Basic usage:**

```jsx
<[ComponentName] variant="[variant1]">[Label]</[ComponentName]>
```

**With loading state:**

```jsx
<[ComponentName] variant="[variant1]" loading>
  [Label]
</[ComponentName]>
```

**With icon:**

```jsx
<[ComponentName] variant="[variant1]">
  <Icon name="[icon]" />
  [Label]
</[ComponentName]>
```

**Most complex supported composition:**

```jsx
{/* Describe the scenario */}
```

**Anti-pattern:**

```jsx
{/* WRONG: [Explain why this is wrong] */}
<[ComponentName] [bad prop usage]>[Label]</[ComponentName]>

{/* Correct: [Explain the right approach] */}
<[ComponentName] [good prop usage]>[Label]</[ComponentName]>
```
