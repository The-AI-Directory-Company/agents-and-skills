# Design Token Conventions

Reference for naming, organizing, and applying design tokens in component specs. Tokens ensure components adapt to theming, dark mode, and brand changes without hardcoded values.

## Token Naming Pattern

Use a three-tier hierarchy: **category-element-modifier-state**.

```
{category}.{element}.{modifier}.{state}
```

Examples:

```
color.background.primary.default
color.background.primary.hover
color.text.secondary.disabled
spacing.padding.md
sizing.icon.sm
border.radius.lg
shadow.elevation.2
```

Rules:

- Lowercase, dot-separated (CSS custom properties use kebab-case: `--color-background-primary-default`)
- No abbreviations except universally understood ones: `sm`, `md`, `lg`, `xl`
- States always come last: `default`, `hover`, `focus`, `active`, `disabled`
- Never include color values in names: `color.brand.primary` not `color.blue-500`

## Token Categories

| Category | What It Covers | Examples |
|----------|----------------|----------|
| `color` | All color values — backgrounds, text, borders, icons | `color.background.surface`, `color.text.primary` |
| `spacing` | Margins, paddings, gaps | `spacing.padding.sm`, `spacing.gap.md` |
| `sizing` | Widths, heights, icon sizes | `sizing.icon.md`, `sizing.input.height.lg` |
| `border` | Radius, width, style | `border.radius.md`, `border.width.thin` |
| `shadow` | Box shadows, elevation levels | `shadow.elevation.1`, `shadow.elevation.3` |
| `typography` | Font family, size, weight, line height, letter spacing | `typography.fontSize.body`, `typography.fontWeight.bold` |
| `motion` | Duration, easing, delay | `motion.duration.fast`, `motion.easing.standard` |
| `opacity` | Opacity levels | `opacity.disabled`, `opacity.overlay` |
| `z-index` | Stacking layers | `zIndex.dropdown`, `zIndex.modal`, `zIndex.tooltip` |

## Semantic vs. Hardcoded Values

**Hardcoded** (primitive) tokens define the raw scale:

```
color.blue.500: #3B82F6
color.blue.600: #2563EB
spacing.4: 16px
spacing.6: 24px
```

**Semantic** tokens reference primitives and carry meaning:

```
color.background.primary.default: {color.blue.500}
color.background.primary.hover: {color.blue.600}
spacing.padding.button.md: {spacing.4}
```

### Rules

1. **Component specs must use only semantic tokens.** Never reference `color.blue.500` in a spec -- reference `color.background.primary.default`.
2. **Semantic tokens enable theming.** Swapping the light theme for dark means remapping semantic tokens to different primitives. If specs use primitives directly, theming breaks.
3. **One semantic token, one purpose.** Do not reuse `color.background.primary.default` for both button backgrounds and link underlines. Create separate semantic tokens even if they resolve to the same primitive today.
4. **Document the intent.** Each semantic token should have a one-line description of when to use it.

## Standard Scales

### Spacing

Based on a 4px base unit:

| Token | Value | Use Case |
|-------|-------|----------|
| `spacing.0` | 0px | Reset |
| `spacing.1` | 4px | Tight inline spacing |
| `spacing.2` | 8px | Between related elements |
| `spacing.3` | 12px | Small padding |
| `spacing.4` | 16px | Default padding, standard gap |
| `spacing.5` | 20px | Medium padding |
| `spacing.6` | 24px | Section spacing |
| `spacing.8` | 32px | Large section spacing |
| `spacing.10` | 40px | Page-level spacing |
| `spacing.12` | 48px | Hero spacing |
| `spacing.16` | 64px | Major layout divisions |

### Typography

| Token | Value | Use Case |
|-------|-------|----------|
| `typography.fontSize.xs` | 12px / 0.75rem | Captions, badges |
| `typography.fontSize.sm` | 14px / 0.875rem | Secondary text, labels |
| `typography.fontSize.body` | 16px / 1rem | Body text |
| `typography.fontSize.lg` | 18px / 1.125rem | Emphasized body |
| `typography.fontSize.xl` | 20px / 1.25rem | Subheadings |
| `typography.fontSize.2xl` | 24px / 1.5rem | Section headings |
| `typography.fontSize.3xl` | 30px / 1.875rem | Page headings |
| `typography.fontSize.4xl` | 36px / 2.25rem | Display headings |

### Border Radius

| Token | Value | Use Case |
|-------|-------|----------|
| `border.radius.none` | 0px | Sharp corners |
| `border.radius.sm` | 4px | Subtle rounding (badges, chips) |
| `border.radius.md` | 8px | Default (buttons, inputs, cards) |
| `border.radius.lg` | 12px | Prominent rounding (modals, panels) |
| `border.radius.xl` | 16px | Large containers |
| `border.radius.full` | 9999px | Pills, circular avatars |

### Shadow / Elevation

| Token | Value | Use Case |
|-------|-------|----------|
| `shadow.elevation.0` | none | Flat surface |
| `shadow.elevation.1` | `0 1px 2px rgba(0,0,0,0.05)` | Cards, subtle lift |
| `shadow.elevation.2` | `0 4px 6px rgba(0,0,0,0.07)` | Dropdowns, popovers |
| `shadow.elevation.3` | `0 10px 15px rgba(0,0,0,0.10)` | Modals, dialogs |
| `shadow.elevation.4` | `0 20px 25px rgba(0,0,0,0.15)` | Full-screen overlays |

## Applying Tokens in Specs

When writing the Visual Variants section of a component spec, map every visual property to a semantic token:

```
Variant: Primary
  Background: color.background.primary.default → hover: color.background.primary.hover
  Text: color.text.on-primary
  Border: none
  Shadow: shadow.elevation.0 → focus: shadow.elevation.1

Size: md
  Height: sizing.input.height.md (40px)
  Padding: spacing.3 horizontal (12px)
  Font size: typography.fontSize.sm (14px)
  Icon size: sizing.icon.sm (16px)
```

If a token does not exist for a property, propose a new semantic token name and flag it for the design system team. Never invent a hardcoded value.
