---
name: brand-guidelines
description: Create brand guidelines documents — defining logo usage, color palettes, typography, voice/tone, imagery style, and application rules that maintain brand consistency across all touchpoints.
metadata:
  displayName: "Brand Guidelines"
  categories: ["design", "communication"]
  tags: ["brand", "guidelines", "identity", "visual-design", "voice-tone", "consistency"]
  worksWellWithAgents: ["brand-manager", "content-strategist", "copywriter"]
  worksWellWithSkills: ["component-design-spec", "ux-copy-guidelines"]
---

# Brand Guidelines

## Before you start

Gather the following from the user. If anything is missing, ask before proceeding:

1. **What is the brand?** (Company name, product name, or sub-brand)
2. **Does a brand exist already?** (Existing assets, logos, colors, or greenfield)
3. **Who is the target audience?** (Demographics, psychographics, B2B vs. B2C)
4. **What are the brand values?** (3-5 core values the brand should communicate)
5. **Who will use these guidelines?** (Internal team, agencies, partners, community)
6. **What touchpoints must be covered?** (Web, mobile, print, social, email, packaging)

If the user only provides a logo and says "write guidelines around this," push back: guidelines without defined brand values and audience produce rules without rationale.

## Brand guidelines template

### 1. Brand Foundation

```
Brand Mission:     [One sentence — what the brand exists to do]
Brand Values:      [3-5 values with one-line descriptions]
Brand Personality: [3-5 adjectives that describe how the brand feels]
Positioning:       [One sentence — how the brand differs from alternatives]
```

Place the brand on each personality axis:

```
| Axis       | Left End      | Position   | Right End     |
|------------|---------------|------------|---------------|
| Tone       | Formal        | [  X  ]    | Casual        |
| Energy     | Calm          | [    X]    | Energetic     |
| Approach   | Traditional   | [X    ]    | Innovative    |
| Warmth     | Professional  | [  X  ]    | Friendly      |
```

### 2. Logo Usage

Define the logo system: primary logo, logo mark (icon only), wordmark (text only). Specify minimum size, clear space (defined by a unit like "height of the letter X"), and approved variations (full color, single color, reversed, monochrome).

Document what is not allowed: do not rotate, skew, recolor, add effects, place on busy backgrounds, or recreate the logo. Use provided files only.

### 3. Color Palette

```
| Color Name   | Role       | HEX     | RGB           | Usage                           |
|--------------|------------|---------|---------------|---------------------------------|
| Brand Blue   | Primary    | #1A56DB | 26, 86, 219   | CTAs, headings, key UI elements |
| Brand Navy   | Primary    | #0B1F45 | 11, 31, 69    | Backgrounds, text               |
| Neutral 900  | Neutral    | #111827 | 17, 24, 39    | Body text                       |
| Neutral 100  | Neutral    | #F3F4F6 | 243, 244, 246 | Backgrounds                     |
| Success Green| Functional | #059669 | 5, 150, 105   | Success states only             |
| Error Red    | Functional | #DC2626 | 220, 38, 38   | Error states only               |
```

Rules: primary colors dominate (60-70%), secondary accent (20-30%), functional colors reserved for UI states only. All text-on-background combinations must meet WCAG 2.1 AA contrast ratios (4.5:1 body, 3:1 large text).

### 4. Typography

```
| Use Case     | Typeface | Weight     | Size Range | Line Height |
|--------------|----------|------------|------------|-------------|
| H1 headings  | Inter    | Bold (700) | 36-48px    | 1.1         |
| H2 headings  | Inter    | Semibold   | 28-32px    | 1.2         |
| Body text    | Inter    | Regular    | 16-18px    | 1.5         |
| Code         | JetBrains Mono | Regular | 14-16px | 1.6         |
```

Specify fallback font stacks. Define hierarchy rules: never skip heading levels, maintain consistent spacing.

### 5. Voice and Tone

Voice is constant; tone adjusts by context.

```
Voice (always):
- Clear over clever — say what we mean without jargon
- Confident but not arrogant — know our strengths without belittling alternatives
- Helpful first — every communication leaves the reader better informed

Tone by context:
| Context         | Tone                          | Example                           |
|-----------------|-------------------------------|-----------------------------------|
| Marketing       | Energetic, aspirational       | "Ship faster with confidence"     |
| Error message   | Calm, helpful, blame-free     | "Something went wrong. Try again."|
| Documentation   | Precise, neutral              | "Run the following command to..."  |
| Crisis comms    | Direct, empathetic, factual   | "Here is what happened and..."    |
```

Include a "We say / We don't say" table with 4-6 concrete examples.

### 6. Application Rules

Show how elements combine across touchpoints: website header, email signature, social avatar, presentations, print. Specify which logo variant, colors, and typography apply to each.

## Quality checklist

Before delivering brand guidelines, verify:

- [ ] Brand values and personality are defined before visual rules
- [ ] Logo usage includes minimum size, clear space, approved variations, and don'ts
- [ ] Color palette includes exact values (HEX, RGB) and usage rules
- [ ] All text/background combinations meet WCAG 2.1 AA contrast ratios
- [ ] Typography specifies typeface, weights, sizes, and fallback stacks
- [ ] Voice is defined as constants and tone adjusts by context with examples
- [ ] Guidelines are usable by someone outside the core team without additional context

## Common mistakes

- **Rules without rationale.** "Use Brand Blue for CTAs" is a rule. "Use Brand Blue for CTAs because it provides the highest contrast" is a guideline. Explain why.
- **Colors without exact values.** "Our blue" means different things on every screen. Provide HEX, RGB, and HSL.
- **Ignoring dark mode and accessibility.** If your product has dark mode, guidelines must cover both themes.
- **Voice guidelines as personality traits.** "We are innovative" tells a writer nothing. Show before/after copy examples.
- **Static PDF nobody updates.** Brand guidelines in a PDF from 2019 are not followed. Make them accessible and maintained.
- **No don'ts.** Guidelines that only show correct usage leave room for creative misinterpretation.
