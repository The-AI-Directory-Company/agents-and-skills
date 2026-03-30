# WCAG 2.1 AA Success Criteria — Condensed Reference

Quick-reference table of WCAG 2.1 Level A and AA success criteria most frequently violated in web audits. Use this when mapping findings to specific criteria.

## 1. Perceivable

| Criterion | Name | Level | What it means | Common failure | Standard fix |
|-----------|------|-------|---------------|----------------|--------------|
| 1.1.1 | Non-text Content | A | Every non-text element (image, icon, chart) has a text alternative | `<img>` without `alt`; icon buttons with no label; decorative images not hidden from AT | Add `alt` text describing purpose. Use `alt=""` and `aria-hidden="true"` for decorative images. Add `aria-label` to icon-only buttons. |
| 1.2.1 | Audio-only and Video-only | A | Pre-recorded audio has a transcript; pre-recorded video has a transcript or audio description | Podcast episode with no transcript; background video with no alternative | Provide text transcript for audio. Provide transcript or audio description track for video. |
| 1.2.2 | Captions (Prerecorded) | A | Pre-recorded video with audio has synchronized captions | Auto-generated captions with no human review; captions missing for non-speech audio cues | Add accurate synchronized captions including speaker identification and significant sounds. |
| 1.2.3 | Audio Description or Media Alternative | A | Pre-recorded video has audio description or full text alternative | Video relies on visuals to convey meaning but only has dialogue audio | Add audio description track narrating important visual information between dialogue. |
| 1.2.5 | Audio Description (Prerecorded) | AA | Pre-recorded video has audio description (no text alternative option) | Same as 1.2.3 but stricter — text alternative alone is insufficient at AA | Add audio description track for all pre-recorded video content. |
| 1.3.1 | Info and Relationships | A | Structure and relationships conveyed visually are also conveyed programmatically | Visual heading styled with CSS but using `<div>` not `<h1>`-`<h6>`; table without `<th>`; form fields without `<label>` | Use semantic HTML: headings, lists, `<table>` with `<th>`, `<label>` associated with `<input>`. Use ARIA landmarks for page regions. |
| 1.3.2 | Meaningful Sequence | A | Reading order in DOM matches the visual presentation order | CSS `float` or `order` rearranges content so screen reader order makes no sense | Ensure DOM order reflects logical reading order. Use CSS for visual positioning without changing source order. |
| 1.3.3 | Sensory Characteristics | A | Instructions don't rely solely on shape, size, position, or sound | "Click the round button on the right" with no other identifier | Supplement sensory references with text labels: "Click the Submit button (round button on the right)." |
| 1.3.4 | Orientation | AA | Content is not restricted to a single display orientation | App force-locks to portrait via CSS or JS | Remove `orientation: portrait` locks. Allow both orientations unless essential (e.g., piano app). |
| 1.3.5 | Identify Input Purpose | AA | Input fields collecting user data identify their purpose programmatically | Checkout form fields lack `autocomplete` attribute | Add `autocomplete` attributes: `autocomplete="given-name"`, `autocomplete="email"`, etc. |
| 1.4.1 | Use of Color | A | Color is not the only visual means of conveying information | Error fields highlighted only in red with no icon or text; required fields marked only by color | Add text labels, icons, or patterns alongside color. "Required" text or error icon + red border. |
| 1.4.2 | Audio Control | A | Audio playing >3 seconds can be paused, stopped, or volume-controlled | Background music autoplays with no stop button | Add pause/stop/volume controls. Better: do not autoplay audio. |
| 1.4.3 | Contrast (Minimum) | AA | Text has at least 4.5:1 contrast ratio (3:1 for large text) | Light gray placeholder text on white; disabled-looking but active buttons | Increase foreground/background contrast. Use tools like WebAIM Contrast Checker. Large text (18pt+ or 14pt+ bold) needs 3:1 minimum. |
| 1.4.4 | Resize Text | AA | Text can be resized to 200% without loss of content or function | Text overflow hidden on zoom; fixed-height containers clip enlarged text | Use relative units (`rem`, `em`, `%`). Ensure containers grow with content. Test at 200% browser zoom. |
| 1.4.5 | Images of Text | AA | Text is used instead of images of text (except logos) | Navigation items or headings rendered as PNG/SVG images of text | Replace images of text with styled HTML text. Exception: logos and branding. |
| 1.4.10 | Reflow | AA | Content reflows at 320px CSS width (400% zoom) without horizontal scrolling | Fixed-width layout breaks at narrow viewports; horizontal scroll required | Use responsive design. Single-column layout at 320px. No horizontal scrolling except for data tables, maps, diagrams. |
| 1.4.11 | Non-text Contrast | AA | UI components and graphical objects have 3:1 contrast against adjacent colors | Form field borders too light; custom checkbox invisible against background; chart lines indistinguishable | Ensure borders, icons, focus indicators, and chart elements meet 3:1 contrast ratio. |
| 1.4.12 | Text Spacing | AA | Content works when user overrides text spacing (line-height 1.5x, paragraph spacing 2x, letter spacing 0.12em, word spacing 0.16em) | Text overflows container; content gets clipped or overlaps | Do not use fixed heights on text containers. Avoid `overflow: hidden` on text elements. Test with text spacing bookmarklet. |
| 1.4.13 | Content on Hover or Focus | AA | Content triggered by hover/focus is dismissible, hoverable, and persistent | Tooltip disappears when mouse moves toward it; no way to dismiss tooltip without moving focus | Tooltip must stay visible while hovered. Must be dismissible (Escape key). Must persist until user dismisses, hovers away, or info becomes invalid. |

## 2. Operable

| Criterion | Name | Level | What it means | Common failure | Standard fix |
|-----------|------|-------|---------------|----------------|--------------|
| 2.1.1 | Keyboard | A | All functionality is operable via keyboard | Custom dropdown opens only on click; drag-and-drop with no keyboard alternative; `<div onclick>` not focusable | Use native interactive elements (`<button>`, `<a>`, `<select>`). Add `tabindex="0"` + keyboard event handlers to custom widgets. Provide keyboard alternatives for drag-and-drop. |
| 2.1.2 | No Keyboard Trap | A | User can navigate away from every component using keyboard | Modal dialog with no Escape key handler; focus cycles but cannot exit a widget | Ensure focus can leave every component. Modal: trap focus inside but allow Escape to close. Non-modal: do not trap focus at all. |
| 2.1.4 | Character Key Shortcuts | A | Single-character shortcuts can be turned off or remapped | App uses "S" to save, triggering accidentally during text input | Only activate single-char shortcuts when focus is not in a text field, or allow users to remap/disable them. |
| 2.2.1 | Timing Adjustable | A | Time limits can be turned off, adjusted, or extended | Session timeout with no warning; timed quiz with no extension option | Warn before timeout. Allow extension (at least 10x). Provide option to disable time limit. Exception: real-time events. |
| 2.2.2 | Pause, Stop, Hide | A | Moving, blinking, scrolling, or auto-updating content can be paused | Auto-scrolling carousel with no pause; live feed that cannot be stopped | Add pause/stop controls for all auto-moving content. Content that starts automatically and lasts >5 seconds must be pausable. |
| 2.3.1 | Three Flashes or Below | A | No content flashes more than 3 times per second | Video with strobe effects; animated loading spinner with rapid flash | Keep flash rate below 3 per second. Avoid large flashing areas. If unavoidable, keep flash area under 25% of display. |
| 2.4.1 | Bypass Blocks | A | A mechanism exists to skip repeated blocks of content | No "skip to main content" link; no landmark regions | Add skip navigation link as first focusable element. Use ARIA landmarks: `<nav>`, `<main>`, `<aside>`. |
| 2.4.2 | Page Titled | A | Pages have descriptive titles | All pages titled "Home" or share the same generic title | Each page gets a unique, descriptive `<title>` reflecting its content: "Checkout - Payment | Store Name". |
| 2.4.3 | Focus Order | A | Focus order is logical and meaningful | Tab order jumps randomly due to `tabindex` values >0 or CSS layout mismatch | Remove positive `tabindex` values. Let DOM order drive focus order. Ensure visual layout matches DOM order. |
| 2.4.4 | Link Purpose (In Context) | A | Link purpose is clear from link text or its surrounding context | "Click here" and "Read more" links with no distinguishing context | Use descriptive link text: "Read the accessibility audit guide" not "Click here." If surrounding context clarifies, ensure it is programmatically determinable. |
| 2.4.5 | Multiple Ways | AA | More than one way to find each page (except process steps) | Site has no search, no sitemap, no secondary navigation | Provide at least two of: navigation menu, search, sitemap, table of contents, A-Z index. |
| 2.4.6 | Headings and Labels | AA | Headings and labels describe topic or purpose | Headings like "Section 1" or labels like "Field 1" | Write descriptive headings: "Shipping Address" not "Step 2." Labels should describe the input: "Email address" not "Field 3." |
| 2.4.7 | Focus Visible | AA | Keyboard focus indicator is visible | `outline: none` in CSS with no replacement focus style | Ensure all interactive elements have a visible focus indicator. Use `:focus-visible` with a high-contrast outline (3:1 contrast, 2px minimum). |
| 2.5.1 | Pointer Gestures | A | Multi-point or path-based gestures have single-pointer alternatives | Pinch-to-zoom with no button alternative; swipe-to-delete with no fallback | Provide button alternatives for every gesture: zoom +/- buttons, delete button alongside swipe. |
| 2.5.2 | Pointer Cancellation | A | For single-pointer actions, at least one: down-event doesn't trigger, up-event triggers/can undo, up-event reverses | Action fires on `mousedown` instead of `mouseup`/`click` | Use `click` events (fire on up-event). If using `mousedown`, provide undo or allow abort by moving pointer off target. |
| 2.5.3 | Label in Name | A | Visible text label is contained in the accessible name | Button reads "Search" visually but `aria-label="Find products"` | Ensure `aria-label`/`aria-labelledby` contains the visible text. Best: omit custom ARIA labels when visible text suffices. |
| 2.5.4 | Motion Actuation | A | Functionality triggered by device motion can be disabled and has UI alternative | Shake-to-undo with no button; tilt-to-scroll | Provide button/UI control as alternative. Allow motion features to be disabled in settings. |

## 3. Understandable

| Criterion | Name | Level | What it means | Common failure | Standard fix |
|-----------|------|-------|---------------|----------------|--------------|
| 3.1.1 | Language of Page | A | Default human language of the page is programmatically set | `<html>` tag missing `lang` attribute | Add `lang="en"` (or appropriate code) to `<html>` element. |
| 3.1.2 | Language of Parts | AA | Language changes within content are identified | French quote in English page not marked as French | Wrap content in different language with `lang` attribute: `<span lang="fr">Bonjour</span>`. |
| 3.2.1 | On Focus | A | Receiving focus does not trigger a change of context | Dropdown that navigates on focus; tab lands on element and page scrolls away | Do not trigger navigation, form submission, or major layout changes on focus alone. Use explicit activation (click/Enter). |
| 3.2.2 | On Input | A | Changing a form control does not automatically cause a change of context | Selecting a radio button submits the form; changing a dropdown navigates immediately | Require explicit action (submit button) for context changes. If auto-change is essential, warn users in advance. |
| 3.2.3 | Consistent Navigation | AA | Navigation is consistent across pages | Nav items change order between pages; some pages have different menu structure | Keep navigation order identical across all pages within a site section. |
| 3.2.4 | Consistent Identification | AA | Components with the same function are identified consistently | Search icon labeled "Search" on one page and "Find" on another | Use the same labels and icons for the same functionality throughout the site. |
| 3.3.1 | Error Identification | A | Input errors are identified and described in text | Red border only (no text message); error message does not indicate which field | Display text error message adjacent to the field. Identify the field and describe the error: "Email address: enter a valid email (e.g., user@example.com)." |
| 3.3.2 | Labels or Instructions | A | Form fields have labels or instructions | Placeholder text as only label (disappears on input); radio group with no group label | Use visible `<label>` elements. Supplement with instructions for complex fields. Use `<fieldset>`/`<legend>` for radio/checkbox groups. |
| 3.3.3 | Error Suggestion | AA | When an error is detected, a correction suggestion is provided (if known) | "Invalid input" with no hint about correct format | Suggest the correct format: "Date must be MM/DD/YYYY" or "Password must be at least 8 characters with one number." |
| 3.3.4 | Error Prevention (Legal, Financial, Data) | AA | Submissions involving legal/financial/data commitments are reversible, verifiable, or confirmable | One-click purchase with no confirmation; data deletion with no undo | Provide confirmation step, review page, or undo mechanism before irreversible actions. |

## 4. Robust

| Criterion | Name | Level | What it means | Common failure | Standard fix |
|-----------|------|-------|---------------|----------------|--------------|
| 4.1.1 | Parsing | A | HTML is well-formed (no duplicate IDs, proper nesting) | Duplicate `id` attributes; unclosed tags; improper nesting (`<a>` inside `<a>`) | Validate HTML. Remove duplicate IDs. Ensure proper tag nesting. Use an HTML validator in CI. |
| 4.1.2 | Name, Role, Value | A | All UI components expose name, role, and value to assistive technology | Custom toggle has no role; custom select exposes no selected value; dynamic content updates not announced | Use native HTML elements when possible. For custom widgets, add ARIA: `role`, `aria-label`, `aria-checked`, `aria-expanded`, `aria-selected`. |
| 4.1.3 | Status Messages | AA | Status messages are programmatically announced without receiving focus | "Item added to cart" message appears visually but screen reader is silent; form success message not announced | Use `role="status"` (polite) or `role="alert"` (assertive) for dynamic status messages. Use `aria-live` regions for content that updates without page reload. |

## How to Use This Reference

1. **During audits**: Match each finding to a specific criterion number. Never report "inaccessible" without a criterion.
2. **During remediation**: Use the "Standard fix" column as a starting point, then adapt to your tech stack.
3. **During planning**: Sort by level (A first, then AA) to establish a priority baseline. Within each level, prioritize by user impact.
4. **For automated testing**: Criteria marked with common failures involving missing attributes are typically catchable by axe-core. Manual testing is required for criteria involving user experience quality (e.g., 1.3.2, 2.4.3).

Note: This reference covers WCAG 2.1 AA. WCAG 2.2 adds criteria 2.4.11 (Focus Not Obscured), 2.4.12 (Focus Not Obscured Enhanced), 2.4.13 (Focus Appearance), 2.5.7 (Dragging Movements), 2.5.8 (Target Size Minimum), and 3.3.7-3.3.9 (Accessible Authentication and Redundant Entry). Consult the W3C specification for those.
