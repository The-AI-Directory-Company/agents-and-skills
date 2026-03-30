# Example: Vague Prompt vs. Structured Prompt

Side-by-side comparison showing how the same requirement, prompted two different ways, produces drastically different output quality.

---

## The Requirement

Build a function that validates and normalizes phone numbers for a user profile form. The app stores US phone numbers in E.164 format (`+1XXXXXXXXXX`).

---

## The Vague Prompt

```
Write a function that validates phone numbers.
```

### What You Get

```typescript
function validatePhone(phone) {
  const regex = /^\d{10}$/;
  return regex.test(phone);
}
```

### What Is Wrong With This Output

| Problem | Impact |
|---------|--------|
| No types — parameter and return type are implicit `any` | TypeScript compiler cannot catch misuse |
| Only accepts exactly 10 digits — rejects `(555) 123-4567`, `+1-555-123-4567`, `555.123.4567` | Users get unexplained validation failures |
| Returns boolean only — caller does not get the normalized value | Caller must normalize separately, leading to inconsistency |
| No error messages — just `true`/`false` | UI cannot show the user what to fix |
| No documentation | Next developer must read the regex to understand what formats are accepted |
| No edge cases handled | Empty string, `null`, `undefined`, non-string inputs all produce unexpected behavior |
| Hardcoded to 10-digit assumption | No country code handling, no E.164 output |

This function is throwaway code. It will be rewritten within days of integration.

---

## The Structured Prompt

```
Write a TypeScript function called normalizePhoneNumber that:

- Takes: input: string (e.g., "(555) 123-4567", "555.123.4567", "+1 555 123 4567", "5551234567")
- Returns: { valid: true, normalized: string } | { valid: false, error: string }
  - normalized format: E.164 US number "+1XXXXXXXXXX" (e.g., "+15551234567")
- Behavior: Strips all non-digit characters except leading +. If the result is 10 digits, prepends +1. If 11 digits starting with 1, prepends +. Rejects everything else.
- Edge cases:
  - Empty string or whitespace only: return { valid: false, error: "Phone number is required" }
  - Non-string input: TypeScript types prevent this, but add a runtime guard returning { valid: false, error: "Phone number must be a string" }
  - Letters mixed in ("555-ABC-4567"): return { valid: false, error: "Phone number contains invalid characters" }
  - Too few digits (< 10 after stripping): return { valid: false, error: "Phone number is too short — expected 10 digits" }
  - Too many digits (> 11 after stripping): return { valid: false, error: "Phone number is too long" }
  - 11 digits not starting with 1: return { valid: false, error: "11-digit numbers must start with country code 1" }
- Do not use external dependencies.
- Include JSDoc with parameter descriptions and 3 usage examples.
```

### What You Get

```typescript
/**
 * Validates and normalizes a US phone number to E.164 format (+1XXXXXXXXXX).
 *
 * Accepts common formats: (555) 123-4567, 555.123.4567, +1-555-123-4567,
 * 5551234567, 1-555-123-4567.
 *
 * @param input - Raw phone number string from user input
 * @returns Object with `valid: true` and `normalized` E.164 string,
 *          or `valid: false` and descriptive `error` message
 *
 * @example
 * normalizePhoneNumber("(555) 123-4567")
 * // => { valid: true, normalized: "+15551234567" }
 *
 * @example
 * normalizePhoneNumber("+1 555 123 4567")
 * // => { valid: true, normalized: "+15551234567" }
 *
 * @example
 * normalizePhoneNumber("555-ABC")
 * // => { valid: false, error: "Phone number contains invalid characters" }
 */
export function normalizePhoneNumber(
  input: string
): { valid: true; normalized: string } | { valid: false; error: string } {
  // Runtime guard for non-string input (defense against JS callers)
  if (typeof input !== "string") {
    return { valid: false, error: "Phone number must be a string" };
  }

  const trimmed = input.trim();

  if (trimmed.length === 0) {
    return { valid: false, error: "Phone number is required" };
  }

  // Check for letters or invalid characters before stripping
  // Allow digits, spaces, hyphens, dots, parentheses, and leading +
  if (/[a-zA-Z]/.test(trimmed)) {
    return {
      valid: false,
      error: "Phone number contains invalid characters",
    };
  }

  // Strip everything except digits and leading +
  const stripped = trimmed.replace(/[^0-9+]/g, "");

  // Remove leading + for digit counting
  const digitsOnly = stripped.replace(/^\+/, "");

  // Reject non-digit characters that survived (shouldn't happen, but safety net)
  if (!/^\d+$/.test(digitsOnly)) {
    return {
      valid: false,
      error: "Phone number contains invalid characters",
    };
  }

  if (digitsOnly.length < 10) {
    return {
      valid: false,
      error: "Phone number is too short — expected 10 digits",
    };
  }

  if (digitsOnly.length > 11) {
    return { valid: false, error: "Phone number is too long" };
  }

  if (digitsOnly.length === 11 && !digitsOnly.startsWith("1")) {
    return {
      valid: false,
      error: "11-digit numbers must start with country code 1",
    };
  }

  // Normalize to E.164
  const normalized =
    digitsOnly.length === 10 ? `+1${digitsOnly}` : `+${digitsOnly}`;

  return { valid: true, normalized };
}
```

### Why This Output Is Production-Ready

| Quality | How the structured prompt produced it |
|---------|--------------------------------------|
| Full TypeScript types with discriminated union return | The prompt specified the exact return type with both branches |
| 6 specific error messages | The prompt listed every edge case with the expected error string |
| Handles all common US formats | The prompt provided example inputs in different formats |
| No external dependencies | The prompt explicitly prohibited them |
| Complete JSDoc with examples | The prompt requested it |
| Defensive runtime guard | The prompt called for it even though TypeScript types should prevent misuse |
| E.164 normalization | The prompt specified the exact output format with an example |

---

## Key Differences

| Aspect | Vague prompt | Structured prompt |
|--------|-------------|-------------------|
| Inputs specified | No | Yes, with example values |
| Output format defined | No (implicit boolean) | Yes, discriminated union with examples |
| Edge cases listed | No | Yes, 6 cases with expected behavior |
| Error messages defined | No | Yes, specific strings per case |
| Dependency constraints | No | Yes, "no external dependencies" |
| Documentation requested | No | Yes, JSDoc with examples |
| **Lines of output** | 4 | 65 |
| **Time to production** | Hours of rewriting | Minutes of integration testing |

## The Lesson

The vague prompt produces code that matches the words in the prompt ("validates phone numbers" -> returns boolean). The structured prompt produces code that matches the actual requirement (normalize US phone numbers for E.164 storage with user-facing error messages). The 2 minutes spent writing a structured prompt saves hours of back-and-forth refinement and rewriting.
