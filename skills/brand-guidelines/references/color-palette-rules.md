# Color Palette Rules

## WCAG Contrast Requirements

All color pairings used for text must meet **WCAG 2.1 AA** minimum contrast ratios:

| Element | Minimum Ratio | Example |
|---|---|---|
| Body text on background | 4.5:1 | #111827 on #FFFFFF = 16.8:1 |
| Large text (18px+ bold or 24px+) on background | 3:1 | #1A56DB on #FFFFFF = 6.1:1 |
| UI components and graphical objects | 3:1 | Icon color against its container |
| Disabled elements | No minimum | But must still be distinguishable from enabled |

**AAA target** (recommended for body text): 7:1 contrast ratio.

Test every pairing with a tool such as WebAIM Contrast Checker, Stark, or Polypane before adding it to the palette.

## The 60/30/10 Rule

Distribute brand colors across layouts using this proportion:

| Share | Role | Typical Usage |
|---|---|---|
| 60% | Dominant / Neutral | Backgrounds, large surfaces, body text containers |
| 30% | Secondary / Brand | Headers, navigation, cards, section dividers |
| 10% | Accent | CTAs, active states, badges, key highlights |

Functional colors (success, warning, error, info) live outside the 60/30/10 split. They appear only when conveying system status and must never be repurposed for decoration.

## Color Specification Format

Every color in the palette must be documented in three formats:

| Format | When to Use | Example |
|---|---|---|
| HEX | Web CSS, design tools | `#1A56DB` |
| RGB | CSS `rgb()`, programmatic use | `rgb(26, 86, 219)` |
| HSL | Deriving tints/shades, CSS custom properties | `hsl(222, 79%, 48%)` |

Additionally record:

- **Opacity variants** — If the color is used at reduced opacity (e.g., overlays, disabled states), document the specific alpha values.
- **Tint/shade scale** — For primary and secondary colors, provide a 50-950 scale (9 steps minimum) so designers can pick lighter or darker variants without eyeballing.

## Dark Mode Coverage

If the product supports dark mode, every palette entry must have a dark-mode counterpart:

| Token Name | Light Value | Dark Value | Notes |
|---|---|---|---|
| `--color-bg-primary` | #FFFFFF | #0F172A | Main surface |
| `--color-text-primary` | #111827 | #F1F5F9 | Body text |
| `--color-brand-primary` | #1A56DB | #3B82F6 | Lightened in dark mode to maintain contrast |
| `--color-border-default` | #E5E7EB | #334155 | Subtle divider |

Rules for dark mode colors:

1. **Re-check contrast** — A color that passes AA on white may fail on dark backgrounds. Test every pairing again.
2. **Do not simply invert** — Inverting HEX values produces garish results. Adjust lightness in HSL space instead.
3. **Reduce saturation slightly** — Highly saturated colors on dark backgrounds cause eye strain. Drop saturation 5-15% for dark variants.
4. **Elevation = lightness** — In dark mode, higher-elevation surfaces are lighter (not shadowed). Use progressively lighter background tones for cards, modals, and popovers.

## Anti-Patterns

- Using brand blue for both CTAs and informational text — dilutes the signal that blue means "clickable."
- Defining colors by name only ("our blue") without exact values — every screen renders it differently.
- Skipping functional colors — borrowing brand red for errors conflates branding with system feedback.
- Having a light-mode palette but no dark-mode mapping — forces dark-mode implementers to guess.
