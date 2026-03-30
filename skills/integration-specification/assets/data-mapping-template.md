# Data Mapping Template

Use this table to document field-by-field transformations between source and target systems. Every field in the integration must have a row. Do not leave implicit transformations undocumented.

---

## Mapping Table

| # | Source Field | Source Type | Required | Target Field | Target Type | Required | Transform | Default | Notes |
|---|-------------|------------|----------|-------------|------------|----------|-----------|---------|-------|
| 1 | `user.id` | integer | Yes | `external_user_id` | string | Yes | Convert to string, prefix with `src_` | — | Target system requires string IDs |
| 2 | `user.email` | string | Yes | `contact_email` | varchar(255) | Yes | Lowercase, trim whitespace | — | Target validates email format |
| 3 | `user.full_name` | string | Yes | `first_name`, `last_name` | varchar(100) each | Yes | Split on first space. If no space, `first_name` = full value, `last_name` = empty | — | Handle single-word names |
| 4 | `created_at` | Unix epoch (ms) | Yes | `creation_date` | ISO 8601 string | Yes | Divide by 1000, convert to UTC ISO 8601 (`2024-06-23T10:30:00Z`) | — | Source is milliseconds, target expects seconds-precision |
| 5 | `status` | enum (1, 2, 3) | Yes | `order_status` | string | Yes | Map: `1` = `"pending"`, `2` = `"active"`, `3` = `"closed"` | `"pending"` | Unmapped values default to `"pending"` and trigger a warning log |
| 6 | `address.zip` | string | No | `postal_code` | varchar(20) | No | Strip non-alphanumeric characters, uppercase | `null` | Nullable in both systems |
| 7 | `phone` | string | No | `phone_number` | varchar(30) | No | Normalize to E.164 format (`+1XXXXXXXXXX`) | `null` | Use libphonenumber or equivalent |
| 8 | `tags` | array of strings | No | `labels` | comma-separated string | No | Join with commas, trim each tag, deduplicate | `""` | Target does not support arrays |
| 9 | — | — | — | `imported_at` | ISO 8601 string | Yes | Set to current UTC timestamp at processing time | — | Generated field, no source equivalent |
| 10 | `currency` | string (ISO 4217) | Yes | `currency_code` | char(3) | Yes | Uppercase, validate against ISO 4217 | — | Reject if invalid |

---

## Blank Template

Copy and fill in for your integration:

| # | Source Field | Source Type | Required | Target Field | Target Type | Required | Transform | Default | Notes |
|---|-------------|------------|----------|-------------|------------|----------|-----------|---------|-------|
| 1 | | | | | | | | | |
| 2 | | | | | | | | | |
| 3 | | | | | | | | | |
| 4 | | | | | | | | | |
| 5 | | | | | | | | | |

---

## Column Definitions

| Column | Description |
|--------|-------------|
| **#** | Row number for reference in discussions and code comments |
| **Source Field** | Dot-notation path in the source payload (e.g., `user.address.city`) |
| **Source Type** | Data type in the source system (string, integer, boolean, array, enum, timestamp format) |
| **Required** | Whether the field is always present in source data |
| **Target Field** | Field name in the target system |
| **Target Type** | Data type expected by the target system |
| **Required** | Whether the target system requires this field (reject if missing) |
| **Transform** | Exact transformation logic. Be specific: "lowercase" not "normalize" |
| **Default** | Value to use when the source field is missing or null |
| **Notes** | Edge cases, validation rules, known issues |

---

## Common Transform Patterns

| Pattern | Description | Example |
|---------|-------------|---------|
| **Type cast** | Convert between types | `integer 42` to `string "42"` |
| **Format conversion** | Change representation | Unix epoch to ISO 8601 |
| **Enum mapping** | Map source values to target values | `1` to `"active"`, `2` to `"inactive"` |
| **String normalization** | Clean up text | Trim, lowercase, strip special characters |
| **Split** | One field to many | `"Alice Smith"` to `first_name: "Alice"`, `last_name: "Smith"` |
| **Merge** | Many fields to one | `first_name` + `last_name` to `full_name` |
| **Lookup** | Enrich with external data | Source `country_code: "US"` to `country_name: "United States"` |
| **Generated** | No source; computed at processing time | `imported_at: NOW()` |
| **Passthrough** | No transformation | Copy value as-is |
| **Conditional** | Transform depends on another field | If `type == "business"`, use `company_name`; else use `full_name` |

---

## Validation Rules

Document validation that must pass before writing to the target:

| Rule | Fields | Action on Failure |
|------|--------|-------------------|
| Email format | `contact_email` | Reject record, log error |
| Phone E.164 | `phone_number` | Set to null, log warning |
| Enum in allowed set | `order_status` | Default to `"pending"`, log warning |
| String max length | All varchar fields | Truncate to max length, log warning |
| Required field missing | All required target fields | Reject record, send to DLQ |
| Date in valid range | `creation_date` | Reject if before 2000-01-01 or in the future |

---

## Handling Nulls

Document the null strategy for each field:

| Scenario | Strategy |
|----------|----------|
| Source field is `null`, target is required | Use default value if defined; otherwise reject the record |
| Source field is `null`, target is optional | Pass `null` to target (or omit the field, depending on target API) |
| Source field is missing (key absent) | Same as `null` unless the source schema guarantees presence |
| Source field is empty string `""` | Treat as `null` for most fields; document exceptions |
