# Template A: Standalone Function

Prompt template for generating a single, isolated function with clear inputs, outputs, and edge case handling. Best for utility functions, data transformations, and pure logic under ~50 lines.

---

## The Template

```
Write a [LANGUAGE] function called [NAME] that:

- Takes: [PARAM1: TYPE], [PARAM2: TYPE]
- Returns: [RETURN_TYPE]
- Behavior: [EXACT DESCRIPTION]
- Edge cases: [LIST EACH CASE AND EXPECTED BEHAVIOR]
- Do not use external dependencies.
- Include JSDoc/docstring with parameter descriptions.
```

---

## Slot Reference

| Slot | What to write | Example |
|------|--------------|---------|
| `[LANGUAGE]` | Language and version if relevant | TypeScript, Python 3.11, Go 1.22 |
| `[NAME]` | Descriptive function name following language conventions | `parseRelativeDate`, `calculate_compound_interest` |
| `[PARAM: TYPE]` | Each parameter with its type and a concrete example value | `dateString: string` (e.g., "2 days ago", "next Friday") |
| `[RETURN_TYPE]` | Return type with an example of the returned value | `Date` (e.g., `2026-03-28T00:00:00Z` for "2 days ago" when today is March 30) |
| `[EXACT DESCRIPTION]` | What the function does, not how it does it | "Parses human-readable relative date strings and returns an absolute Date" |
| `[EDGE CASES]` | Each edge case with the expected behavior | "Empty string: throw InvalidDateError. Unrecognized format: throw InvalidDateError. Negative values ('minus 3 days'): treat same as '3 days ago'." |

---

## Filled Example

```
Write a TypeScript function called calculateCompoundInterest that:

- Takes: principal: number (e.g., 10000), annualRate: number (e.g., 0.05 for 5%), compoundsPerYear: number (e.g., 12 for monthly), years: number (e.g., 10)
- Returns: { finalAmount: number, totalInterest: number } (e.g., { finalAmount: 16470.09, totalInterest: 6470.09 })
- Behavior: Calculates compound interest using the formula A = P(1 + r/n)^(nt). Returns the final amount rounded to 2 decimal places and the total interest earned.
- Edge cases:
  - principal <= 0: throw Error("Principal must be positive")
  - annualRate < 0: throw Error("Rate cannot be negative")
  - compoundsPerYear <= 0: throw Error("Compounds per year must be positive")
  - years < 0: throw Error("Years cannot be negative")
  - years === 0: return { finalAmount: principal, totalInterest: 0 }
  - Very large numbers: use standard JS Number precision (no BigInt needed)
- Do not use external dependencies.
- Include JSDoc with parameter descriptions and a usage example.
```

---

## When to Use This Template

- Isolated utility functions that can be tested independently
- Data transformation or formatting functions
- Mathematical or algorithmic functions
- Validation functions
- String parsing or formatting

## When NOT to Use This Template

- Functions that depend on framework context (HTTP request/response, database connection) -- use Template B (API Endpoint)
- Functions that render UI -- use Template C (UI Component)
- Complex modules with multiple interconnected functions -- use the scaffold-then-fill strategy from the main SKILL.md
