# Implement typeahead autocomplete for product search bar

**Ticket ID**: SEARCH-289
**Type**: Feature
**Epic**: SEARCH-200 — Search Experience Improvements
**Priority**: High
**Labels**: frontend, search, ux

---

## Context

Product search currently requires users to type a full query and press Enter before seeing results. Analytics show 38% of searches are abandoned after the first attempt — users misspell product names or don't know exact terms. Competitor benchmarking (Algolia, Typesense demos) shows autocomplete reduces search abandonment by 20-30%.

This ticket adds typeahead autocomplete to the existing search bar, showing suggestions as the user types. The search API already supports prefix matching via the `?prefix=true` parameter (added in SEARCH-245), so this is primarily a frontend change with minor API work for a dedicated suggestions endpoint.

---

## Acceptance Criteria

- [ ] Given a user focuses the search bar and types at least 2 characters, when 150ms have elapsed since the last keystroke, then up to 8 autocomplete suggestions appear in a dropdown below the search bar
- [ ] Given suggestions are visible, when the user clicks a suggestion or presses Enter on a highlighted suggestion, then the app navigates to the search results page with that term pre-filled
- [ ] Given suggestions are visible, when the user presses the up/down arrow keys, then the highlight moves between suggestions and the highlighted text is readable at WCAG AA contrast
- [ ] Given the API returns zero suggestions, when the dropdown would render, then no dropdown appears (no empty state or "no results" message at this stage)
- [ ] Given the user clears the search bar or presses Escape, when suggestions are visible, then the dropdown closes
- [ ] Given a slow network (>500ms API response), when the user is typing, then a subtle loading indicator appears in the search bar without blocking input
- [ ] Given the user types a query that was fetched in the last 60 seconds, when suggestions are requested, then the cached result is used without a network call
- [ ] The suggestions endpoint responds in under 100ms at p95 for the production dataset (~120K products)

---

## Technical Notes

**Relevant files:**
- `src/components/SearchBar.tsx` — current search bar component
- `src/hooks/useDebounce.ts` — existing debounce hook (150ms default)
- `src/api/routes/search.ts` — search route handler with prefix support
- `src/services/search/index.ts` — Typesense client wrapper

**Considerations:**
- Use the existing `useDebounce` hook for keystroke debouncing — do not add a new dependency
- The suggestions endpoint should return `{ suggestions: [{ text: string, category: string, resultCount: number }] }` to support future category grouping
- Typesense supports search-as-you-type natively via the `query_by` parameter; avoid building a custom prefix index
- Use `aria-combobox` pattern for the dropdown to meet accessibility requirements (see WAI-ARIA combobox spec)
- Cache suggestions in a `Map<string, Result>` in the hook; no need for Redux or global state

---

## Effort Estimate

**Size**: M (3 days)
**Reasoning**: The search bar component exists, the debounce hook exists, and Typesense supports prefix search. The work is: create the `/api/search/suggestions` endpoint (~0.5 day), build the dropdown UI with keyboard navigation and accessibility (~1.5 days), add client-side caching (~0.5 day), and write tests (~0.5 day). No database migration or backend architecture changes.

---

## Dependencies

- **Blocked by**: None (SEARCH-245 prefix search support already merged)
- **Blocks**: SEARCH-301 (recent searches in dropdown — needs the dropdown component from this ticket)
- **Related**: SEARCH-290 (search analytics tracking — will add impression events to autocomplete later)

---

## Out of Scope

- Recent searches or trending queries in the dropdown (covered by SEARCH-301)
- Search result previews or rich suggestion cards (future enhancement, not in this sprint)
- Personalized suggestions based on user history (requires ML pipeline, separate epic)
