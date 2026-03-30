# Pagination Patterns: Cursor vs Offset

Tradeoffs, implementation details, and edge cases for the two primary pagination strategies.

---

## Offset-Based Pagination

### How It Works

```
GET /v1/orders?page=3&per_page=20
```

Translates to: `SELECT * FROM orders ORDER BY id LIMIT 20 OFFSET 40`

### Response Shape

```json
{
  "data": [...],
  "meta": {
    "total": 4280,
    "page": 3,
    "per_page": 20,
    "total_pages": 214
  },
  "links": {
    "first": "/v1/orders?page=1&per_page=20",
    "prev": "/v1/orders?page=2&per_page=20",
    "next": "/v1/orders?page=4&per_page=20",
    "last": "/v1/orders?page=214&per_page=20"
  }
}
```

### Advantages

- Simple to implement and understand
- Clients can jump to any page directly (`page=100`)
- Total count and page numbers are straightforward
- Works well with UI pagination controls (page 1, 2, 3 ...)

### Disadvantages

- **Performance degrades at high offsets.** `OFFSET 100000` forces the database to scan and discard 100,000 rows. Cost is O(offset + limit).
- **Inconsistent results when data changes.** If a row is inserted or deleted between page requests, items shift — causing duplicates or missed records.
- **COUNT(*) can be expensive.** Total count on large tables with complex filters may timeout.

### When to Use

- Small to medium datasets (under 100K rows)
- UI requires page numbers and "jump to page" navigation
- Data changes infrequently between requests
- Sorting is on indexed columns

---

## Cursor-Based Pagination

### How It Works

```
GET /v1/orders?limit=20&cursor=eyJpZCI6MTAwfQ
```

The cursor is an opaque token (typically base64-encoded) that encodes the position of the last item returned. The server decodes it and queries:

```sql
SELECT * FROM orders WHERE id > 100 ORDER BY id LIMIT 20
```

### Response Shape

```json
{
  "data": [...],
  "meta": {
    "per_page": 20,
    "next_cursor": "eyJpZCI6MTIwfQ",
    "has_more": true
  },
  "links": {
    "next": "/v1/orders?limit=20&cursor=eyJpZCI6MTIwfQ"
  }
}
```

### Advantages

- **Consistent performance.** Query uses an indexed `WHERE` clause — O(limit) regardless of position.
- **Stable pagination.** Inserts and deletes do not cause duplicates or skipped items.
- **Works for real-time feeds.** Ideal for infinite scroll, activity feeds, and event streams.

### Disadvantages

- Cannot jump to arbitrary pages (no "go to page 50")
- No total count (or requires a separate query)
- Cursor encoding adds complexity
- Sorting must be on a unique, sequential column (or compound key)

### When to Use

- Large datasets (100K+ rows)
- Real-time or frequently changing data
- Infinite scroll UI pattern
- Event streams, activity logs, feeds

---

## Implementation Details

### Cursor Encoding

Encode the sort key(s) as a JSON object, then base64url-encode it:

```
Last item: { id: 120, created_at: "2024-06-01T12:00:00Z" }
Cursor:    eyJpZCI6MTIwLCJjcmVhdGVkX2F0IjoiMjAyNC0wNi0wMVQxMjowMDowMFoifQ
```

For multi-column sorting, include all sort columns in the cursor:

```sql
WHERE (created_at, id) > ('2024-06-01T12:00:00Z', 120)
ORDER BY created_at, id
LIMIT 20
```

### Default and Maximum Page Size

| Parameter | Default | Maximum | Rationale |
|-----------|---------|---------|-----------|
| `limit` / `per_page` | 20 | 100 | Balances response time and client usability |

Return 400 if the client requests above the maximum.

---

## Edge Cases

### Empty Pages

**Offset:** Page 215 of 214 pages returns `{ "data": [], "meta": { "total": 4280, "page": 215 } }`. Client checks `page > total_pages` to stop.

**Cursor:** Response returns `{ "data": [], "has_more": false, "next_cursor": null }`. Client stops when `has_more` is false or `data` is empty.

### Deleted Rows Between Requests

**Offset problem:** Client fetches page 1 (items 1-20). Before page 2, item 5 is deleted. Page 2 now starts at what was item 22, and item 21 is never seen.

**Cursor solution:** Client's cursor points to the last item they saw (item 20). The next query returns items after 20 regardless of deletions — item 21 is included.

### Inserted Rows Between Requests

**Offset problem:** Client fetches page 1 (items 1-20). A new item is inserted at position 3. Page 2 now includes item 20 again (shifted forward) — a duplicate.

**Cursor solution:** The cursor anchors to the last seen item, so new inserts before that point do not affect the next page. New inserts after the cursor appear naturally.

### Concurrent Modifications During Full Scan

When a client must iterate through all records (e.g., data export):

- **Offset:** Use a snapshot/read-replica or `SELECT ... FOR SHARE` to prevent drift. Alternatively, accept eventual consistency.
- **Cursor:** Naturally stable for forward-only iteration. For strict consistency, combine with a timestamp watermark.

### Sorting on Non-Unique Columns

If sorting by `created_at` (non-unique), multiple rows may share the same value. Without a tiebreaker, cursor pagination breaks.

**Fix:** Always include a unique column as a secondary sort: `ORDER BY created_at, id`. Encode both in the cursor.

### Client Sends an Expired or Invalid Cursor

Return 400 with a clear message:

```json
{
  "error": {
    "code": "INVALID_CURSOR",
    "message": "The cursor is invalid or has expired. Start from the beginning by omitting the cursor parameter."
  }
}
```

---

## Quick Decision Matrix

| Factor | Use Offset | Use Cursor |
|--------|-----------|------------|
| Dataset size | < 100K rows | 100K+ rows |
| Data volatility | Low (changes rarely) | High (real-time) |
| UI pattern | Page numbers, "jump to" | Infinite scroll, "load more" |
| Performance at depth | Degrades at high pages | Consistent |
| Total count needed | Yes (built-in) | No (or separate query) |
