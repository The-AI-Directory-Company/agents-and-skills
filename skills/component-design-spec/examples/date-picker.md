# Component Spec: DatePicker

## 1. Component Overview

```
Name:           DatePicker
Purpose:        Lets users select a single date or date range via a calendar popover or direct text input.
Category:       Composite (combines Input, Calendar, Popover primitives)
Status:         Approved
```

## 2. Props API

```typescript
interface DatePickerProps {
  /** Currently selected date(s) */
  value?: Date | DateRange;
  /** Callback when selection changes */
  onChange?: (value: Date | DateRange) => void;
  /** Single date or range selection */
  mode?: 'single' | 'range';                    // default: 'single'
  /** Earliest selectable date */
  minDate?: Date;
  /** Latest selectable date */
  maxDate?: Date;
  /** Dates that cannot be selected */
  disabledDates?: Date[] | ((date: Date) => boolean);
  /** Display size */
  size?: 'sm' | 'md' | 'lg';                    // default: 'md'
  /** Placeholder text for the input */
  placeholder?: string;                          // default: 'Select date'
  /** Disable the entire component */
  disabled?: boolean;                            // default: false
  /** Mark the field as required */
  required?: boolean;                            // default: false
  /** Error message to display below the input */
  error?: string;
  /** Date display format */
  format?: string;                               // default: 'MMM d, yyyy'
  /** Accessible label when no visible label is present */
  'aria-label'?: string;
}

type DateRange = { start: Date; end: Date };
```

## 3. States

| State | Trigger | Visual Change | Behavior Change |
|-------|---------|---------------|-----------------|
| Default | Initial render | Input with calendar icon | Click or Enter opens popover |
| Hover | Mouse enters input | Border color changes to `border.hover` | Cursor becomes pointer |
| Focus | Tab into input | Focus ring (2px, `focus.ring` token) | Accepts typed date, arrow keys |
| Open | Click input or press Enter | Calendar popover appears below | Focus moves to current/today date |
| Date Hover | Mouse over calendar day | Day cell background `surface.hover` | -- |
| Selected | User picks a date | Selected day uses `primary.solid` fill | Popover closes, input shows formatted date |
| Range Active | First date selected in range mode | Start date highlighted | Hovering other dates shows preview range |
| Disabled | `disabled={true}` | Opacity 0.5, no focus ring | No events fire, excluded from tab order |
| Error | `error` prop is set | Red border, error icon, error text below | Popover still functional |
| Read-only | `readOnly={true}` | Standard styling, no calendar icon | Displays value but cannot change it |

## 4. Visual Variants

**Sizes**

| Size | Input Height | Font Size | Icon Size | Calendar Cell |
|------|-------------|-----------|-----------|---------------|
| sm | 32px | `text.sm` (14px) | 16px | 28x28px |
| md | 40px | `text.md` (16px) | 20px | 36x36px |
| lg | 48px | `text.lg` (18px) | 24px | 44x44px |

All colors reference design tokens: `primary.solid`, `surface.default`, `border.default`, `text.error`, `surface.hover`.

## 5. Interaction Behavior

**Keyboard**
- `Tab`: Focus the input (skip if disabled)
- `Enter` / `Space`: Toggle calendar popover open/closed
- `Arrow keys`: Navigate days within the calendar grid
- `Page Up` / `Page Down`: Navigate to previous/next month
- `Home` / `End`: Jump to first/last day of the current month
- `Escape`: Close popover, return focus to input

**Mouse**: Click input to toggle popover. Click a day cell to select. In range mode, first click sets start, second click sets end.

**Touch**: Tap to open. Minimum 44x44px touch targets on all calendar cells (enforced by the `lg` size mapping).

**Focus management**: Opening the popover moves focus to the currently selected date, or today if no selection. Closing the popover returns focus to the input trigger.

## 6. Accessibility Requirements

- **Role**: Input has `role="combobox"` with `aria-haspopup="dialog"`. Calendar grid uses `role="grid"` with `role="gridcell"` for each day.
- **Accessible name**: Requires a visible `<label>` or `aria-label` prop.
- **State announcements**: `aria-expanded` on the input reflects popover state. Selected date announced via `aria-live="polite"` region.
- **Disabled dates**: Cells use `aria-disabled="true"` and are skipped by arrow key navigation.
- **Contrast**: All text meets 4.5:1 against its background. Focus ring meets 3:1 against adjacent colors.
- **Motion**: Calendar open/close animation respects `prefers-reduced-motion`.

**Screen reader output**:
- Default: "Select date, combo box, collapsed"
- Open: "March 2026, grid, 19 selected"
- Disabled: "Select date, combo box, dimmed"

## 7. Composition Examples

```jsx
{/* Basic single date */}
<DatePicker value={dueDate} onChange={setDueDate} aria-label="Due date" />

{/* Range selection with constraints */}
<DatePicker
  mode="range"
  value={dateRange}
  onChange={setDateRange}
  minDate={new Date('2026-01-01')}
  maxDate={new Date('2026-12-31')}
  placeholder="Select date range"
/>

{/* With error state */}
<DatePicker value={startDate} onChange={setStartDate} error="Start date must be in the future" />

{/* WRONG: using visual props instead of semantic */}
{/* <DatePicker borderColor="red" /> */}

{/* WRONG: no accessible name */}
{/* <DatePicker value={date} onChange={setDate} /> */}
{/* Always pair with a <label> or provide aria-label */}
```
