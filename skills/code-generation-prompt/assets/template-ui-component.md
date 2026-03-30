# Template C: UI Component

Prompt template for generating a UI component with props, visual output, interaction behavior, state handling, and accessibility. Best for React, Vue, Svelte, or any component-based framework.

---

## The Template

```
Write a [FRAMEWORK] component called [NAME] that:

- Props: [LIST EACH PROP WITH TYPE AND DEFAULT]
- Renders: [DESCRIBE THE VISUAL OUTPUT]
- Interactions: [CLICK, HOVER, FOCUS BEHAVIORS]
- States: loading, error, empty, populated
- Accessibility: [ARIA LABELS, KEYBOARD NAVIGATION]
- Use [STYLING APPROACH] for styles.
```

---

## Slot Reference

| Slot | What to write | Example |
|------|--------------|---------|
| `[FRAMEWORK]` | Component framework and version | React 19 with TypeScript, Vue 3 SFC, Svelte 5 |
| `[NAME]` | PascalCase component name | `FileUploadDropzone`, `PricingCard`, `CommandPalette` |
| `[PROPS]` | Each prop with type, required/optional, default, and example | `maxFiles: number (optional, default 5). accept: string[] (optional, default ["image/*"]). onUpload: (files: File[]) => Promise<void> (required).` |
| `[VISUAL OUTPUT]` | What the user sees, described in terms of layout and content | "A dashed-border drop zone with an upload icon, primary text 'Drag files here', secondary text showing accepted formats, and a 'Browse' button. When files are dropped, shows a list of file names with size and a remove button." |
| `[INTERACTIONS]` | User actions and what happens | "Drag over: border turns blue, background fades to blue-50. Drop: files are validated and onUpload is called. Click Browse: opens native file picker. Click remove on a file: removes it from the list." |
| `[STATES]` | What each state looks like | "Loading: progress bar replaces the file list, upload icon animates. Error: red border, error message below the drop zone, files that failed shown with red X. Empty: default drop zone. Populated: file list with names, sizes, and remove buttons." |
| `[ACCESSIBILITY]` | ARIA attributes and keyboard behavior | "Drop zone: role='button', aria-label='Upload files, drag and drop or press Enter to browse'. Browse button: standard button, focus-visible ring. File list: ul with li, remove button has aria-label='Remove {filename}'. Announce upload progress with aria-live region." |
| `[STYLING APPROACH]` | How styles are applied | Tailwind CSS, CSS Modules, styled-components, inline styles |

---

## Filled Example

```
Write a React 19 TypeScript component called CommandPalette that:

- Props:
  - isOpen: boolean (required) — controls visibility
  - onClose: () => void (required) — called when user dismisses
  - commands: Array<{ id: string, label: string, icon?: ReactNode, shortcut?: string, onSelect: () => void }> (required)
  - placeholder: string (optional, default "Type a command...")
  - emptyMessage: string (optional, default "No results found")
  - maxVisible: number (optional, default 8) — max items before scrolling

- Renders: A centered modal overlay with a search input at the top and a scrollable list of command items below. Each item shows an icon (if provided), the command label, and a keyboard shortcut badge (if provided). The currently highlighted item has a distinct background.

- Interactions:
  - Type in search input: filters commands by label (case-insensitive substring match)
  - Arrow Up/Down: moves highlight through the filtered list, wrapping at boundaries
  - Enter: executes the highlighted command's onSelect and closes the palette
  - Escape: closes the palette without executing
  - Click on a command: executes its onSelect and closes
  - Click outside the palette: closes without executing

- States:
  - Loading: not applicable (commands are passed as props)
  - Error: not applicable
  - Empty: search has no matches — show emptyMessage centered in the list area
  - Populated: command list with highlight on the first item by default

- Accessibility:
  - Dialog: role="dialog", aria-modal="true", aria-label="Command palette"
  - Search input: role="combobox", aria-expanded="true", aria-controls="command-list", aria-activedescendant points to highlighted item
  - Command list: role="listbox", id="command-list"
  - Each command: role="option", aria-selected on highlighted item
  - Focus trapped inside the dialog when open
  - Screen reader announcement when filtered results count changes (aria-live polite region)

- Use Tailwind CSS for styles. Support dark mode via dark: variants.
```

---

## When to Use This Template

- Interactive UI components (dropdowns, modals, pickers, palettes)
- Display components (cards, lists, tables, badges)
- Form components (custom inputs, file uploaders, multi-selects)
- Layout components with interactive behavior

## When NOT to Use This Template

- Pure data-fetching or business logic -- use Template A (Standalone Function)
- API routes or server-side handlers -- use Template B (API Endpoint)
- Full page layouts -- break into individual components and generate each one
