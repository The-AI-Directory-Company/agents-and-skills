# Brand Guidelines: Launchpad (Developer Platform)

## 1. Brand Foundation

```
Brand Mission:     Make deploying production software as simple as pushing code.
Brand Values:
  - Developer-first — every decision is judged by whether it saves a developer time
  - Transparent — pricing, status, and architecture are always visible
  - Reliable — uptime is not a feature, it is the product
Brand Personality:  Technical, direct, dependable, quietly confident
Positioning:       The deployment platform that gets out of your way.
```

**Personality axes**:

| Axis | Left End | Position | Right End |
|------|----------|----------|-----------|
| Tone | Formal | [  X  ] | Casual |
| Energy | Calm | [ X   ] | Energetic |
| Approach | Traditional | [    X] | Innovative |
| Warmth | Professional | [X    ] | Friendly |

## 2. Logo Usage

- **Primary logo**: Launchpad wordmark + rocket glyph. Use on light backgrounds.
- **Logo mark**: Rocket glyph only. Use when the brand name is already visible in context (favicons, app icons, social avatars).
- **Wordmark**: "Launchpad" text only. Use in documentation headers and partner co-branding where the glyph competes with other logos.
- **Minimum size**: 24px height (digital), 10mm (print).
- **Clear space**: Equal to the height of the "L" in the wordmark on all sides.
- **Approved variations**: Full color (dark background), full color (light background), monochrome white, monochrome black.

**Do not**: rotate, add drop shadows, stretch, recolor with non-brand colors, place on busy photographic backgrounds, or recreate from fonts.

## 3. Color Palette

| Color Name | Role | HEX | RGB | Usage |
|------------|------|-----|-----|-------|
| Launch Blue | Primary | #2563EB | 37, 99, 235 | CTAs, links, primary actions |
| Midnight | Primary | #0F172A | 15, 23, 42 | Backgrounds, hero sections, code blocks |
| Slate 50 | Neutral (light) | #F8FAFC | 248, 250, 252 | Page backgrounds, cards |
| Slate 400 | Neutral (mid) | #94A3B8 | 148, 163, 184 | Secondary text, borders |
| Slate 900 | Neutral (dark) | #0F172A | 15, 23, 42 | Body text |
| Green 500 | Functional | #22C55E | 34, 197, 94 | Deploy success, healthy status |
| Red 500 | Functional | #EF4444 | 239, 68, 68 | Build failures, error states |
| Amber 500 | Functional | #F59E0B | 245, 158, 11 | Warnings, degraded status |

**Rules**: Primary colors cover 70% of surface area. Functional colors are reserved for status indicators only — never for decoration. All text/background combinations meet WCAG 2.1 AA (4.5:1 body text, 3:1 large text and UI elements).

## 4. Typography

| Use Case | Typeface | Weight | Size Range | Line Height |
|----------|----------|--------|------------|-------------|
| H1 headings | Inter | Bold (700) | 36-48px | 1.1 |
| H2 headings | Inter | Semibold (600) | 24-32px | 1.2 |
| Body text | Inter | Regular (400) | 16-18px | 1.6 |
| Code / CLI | JetBrains Mono | Regular (400) | 14-16px | 1.6 |
| Labels / UI | Inter | Medium (500) | 12-14px | 1.4 |

**Fallback stack**: `Inter, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif`. Code: `'JetBrains Mono', 'Fira Code', 'Courier New', monospace`.

Never skip heading levels. Maintain 24px minimum spacing between sections.

## 5. Voice and Tone

**Voice (constant)**:
- Technical and precise — use correct terminology, never dumb it down
- Direct and concise — respect the reader's time; say it in fewer words
- Confident but humble — state capabilities without superlatives

**Tone by context**:

| Context | Tone | Example |
|---------|------|---------|
| Marketing | Direct, aspirational | "Deploy in 30 seconds. Scale to millions." |
| Documentation | Precise, neutral | "Run `launchpad deploy` from your project root." |
| Status page | Factual, empathetic | "API latency elevated in us-east-1. Investigating. Last updated 2 min ago." |
| Error message | Calm, actionable | "Build failed: missing `start` script in package.json. Add it and redeploy." |
| Changelog | Informative, brief | "Added: branch-based preview deployments with automatic SSL." |

**We say / We don't say**:

| We say | We don't say |
|--------|-------------|
| "Deploy in seconds" | "Blazingly fast deployments" |
| "99.99% uptime SLA" | "We never go down" |
| "Scales automatically" | "Infinite scale" |
| "Something went wrong" | "Oops! Our bad!" |
| "See the docs" | "It's easy, just..." |
| "Requires Node 18+" | "Simply install the latest Node" |

## 6. Application Rules

| Touchpoint | Logo Variant | Background | Typography |
|------------|-------------|------------|------------|
| Website header | Primary (wordmark + glyph) | Slate 50 | Inter |
| Documentation | Wordmark only | White | Inter + JetBrains Mono |
| CLI output | None (text only) | Terminal default | Monospace |
| Email signature | Logo mark + wordmark | White | System sans-serif |
| Social avatar | Logo mark only | Midnight | -- |
| Conference slides | Primary on dark | Midnight | Inter |
