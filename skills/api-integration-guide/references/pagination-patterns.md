# Pagination Consumption Patterns

How to consume paginated APIs: offset, cursor, and GraphQL Relay strategies with stop conditions and implementation details.

---

## 1. Offset-Based Pagination

### Request Pattern

```
GET /v1/items?limit=100&offset=0
GET /v1/items?limit=100&offset=100
GET /v1/items?limit=100&offset=200
...
```

Some APIs use `page` and `per_page` instead:

```
GET /v1/items?page=1&per_page=100
GET /v1/items?page=2&per_page=100
...
```

### Response Shape

```json
{
  "data": [...],
  "meta": {
    "total": 4280,
    "limit": 100,
    "offset": 0
  }
}
```

### Stop Conditions

Stop fetching when ANY of these is true:

1. `len(data) < limit` -- the last page returned fewer items than requested
2. `offset >= total` -- the offset exceeds the total count (if total is provided)
3. `data` is empty -- no more items to fetch
4. `links.next` is null/absent (if the API provides navigation links)

### Pseudocode

```python
all_items = []
offset = 0
limit = 100

while True:
    response = client.get("/v1/items", params={"limit": limit, "offset": offset})
    items = response["data"]
    all_items.extend(items)

    if len(items) < limit:
        break  # Last page

    offset += limit
```

### Pitfalls

- **High offset performance:** `OFFSET 100000` is expensive. If you need all records, consider asking the API provider for a bulk export endpoint instead.
- **Data drift:** Items inserted or deleted between pages cause duplicates or gaps. Offset pagination is not stable for frequently changing datasets.
- **COUNT overhead:** If the API returns `total`, it runs a COUNT query on every request. Some APIs omit total for performance.

---

## 2. Cursor-Based Pagination

### Request Pattern

```
GET /v1/items?limit=100                          # First page (no cursor)
GET /v1/items?limit=100&cursor=eyJpZCI6MTAwfQ    # Subsequent pages
GET /v1/items?limit=100&cursor=eyJpZCI6MjAwfQ
...
```

### Response Shape

```json
{
  "data": [...],
  "meta": {
    "limit": 100,
    "next_cursor": "eyJpZCI6MjAwfQ",
    "has_more": true
  }
}
```

### Stop Conditions

Stop fetching when ANY of these is true:

1. `has_more` is `false`
2. `next_cursor` is `null` or absent
3. `data` is empty
4. `links.next` is null/absent (if the API provides navigation links)

### Pseudocode

```python
all_items = []
cursor = None

while True:
    params = {"limit": 100}
    if cursor:
        params["cursor"] = cursor

    response = client.get("/v1/items", params=params)
    items = response["data"]
    all_items.extend(items)

    cursor = response["meta"].get("next_cursor")
    has_more = response["meta"].get("has_more", True)

    if not cursor or not has_more or not items:
        break
```

### Pitfalls

- **Expired cursors:** Some APIs expire cursors after a time window (e.g., 5 minutes). For large datasets, ensure you fetch the next page before the cursor expires.
- **Cannot parallelize:** Cursor-based pagination is inherently sequential — you need the current cursor to request the next page.
- **Cursor format varies:** Some APIs use opaque tokens, others use base64-encoded JSON, some use the last item's ID directly. Treat cursors as opaque strings regardless.

---

## 3. GraphQL Relay-Style Pagination

### Request Pattern

```graphql
query {
  items(first: 100) {
    edges {
      node {
        id
        name
      }
      cursor
    }
    pageInfo {
      hasNextPage
      endCursor
    }
  }
}
```

Subsequent pages:

```graphql
query {
  items(first: 100, after: "cursor_from_endCursor") {
    edges {
      node {
        id
        name
      }
      cursor
    }
    pageInfo {
      hasNextPage
      endCursor
    }
  }
}
```

### Response Shape

```json
{
  "data": {
    "items": {
      "edges": [
        { "node": { "id": "1", "name": "Item A" }, "cursor": "c1" },
        { "node": { "id": "2", "name": "Item B" }, "cursor": "c2" }
      ],
      "pageInfo": {
        "hasNextPage": true,
        "endCursor": "c2"
      }
    }
  }
}
```

### Stop Conditions

Stop fetching when:

1. `pageInfo.hasNextPage` is `false`
2. `edges` is empty
3. `pageInfo.endCursor` is `null`

### Pseudocode

```python
all_items = []
end_cursor = None

while True:
    variables = {"first": 100}
    if end_cursor:
        variables["after"] = end_cursor

    response = client.query(ITEMS_QUERY, variables=variables)
    connection = response["data"]["items"]

    items = [edge["node"] for edge in connection["edges"]]
    all_items.extend(items)

    page_info = connection["pageInfo"]
    if not page_info["hasNextPage"]:
        break

    end_cursor = page_info["endCursor"]
```

### Backward Pagination

Relay also supports backward pagination:

```graphql
query {
  items(last: 100, before: "cursor") {
    edges { ... }
    pageInfo {
      hasPreviousPage
      startCursor
    }
  }
}
```

---

## Comparison

| Factor | Offset | Cursor | Relay |
|--------|--------|--------|-------|
| Jump to arbitrary page | Yes | No | No |
| Performance at depth | Degrades | Constant | Constant |
| Stable across mutations | No | Yes | Yes |
| Parallelizable | Yes (pages are independent) | No | No |
| Total count available | Usually | Rarely | Optional (`totalCount` field) |
| API type | REST | REST | GraphQL |

---

## Safety: Preventing Infinite Loops

Regardless of pagination strategy, always add a safety limit:

```python
MAX_PAGES = 1000  # Safety valve

for page_num in range(MAX_PAGES):
    response = fetch_next_page(...)

    if should_stop(response):
        break
else:
    # Reached MAX_PAGES without stopping — something is wrong
    raise PaginationError(f"Exceeded {MAX_PAGES} pages. Possible infinite loop.")
```

Common causes of infinite loops:
- API returns the same cursor repeatedly (bug in the API)
- Stop condition is not checked correctly (e.g., checking `len(data) == 0` but the API returns an empty `data` with `has_more: true`)
- Off-by-one in offset calculation (e.g., not incrementing offset)
