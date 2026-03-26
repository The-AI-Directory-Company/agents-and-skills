# Full-Text Search for Product Catalog — Technical Specification

## 1. Problem Statement

Customers currently find products only by browsing categories or filtering by exact attribute matches. The product catalog has grown to 340,000 SKUs, and support tickets mentioning "can't find product" have increased 40% quarter-over-quarter. Users expect to type natural queries like "waterproof hiking boots size 11" and get ranked results. The existing SQL `LIKE` queries against the `products` table are too slow (P99 > 3s) and lack relevance ranking.

## 2. Context

The product catalog is stored in PostgreSQL (RDS). The frontend is a Next.js SPA calling a REST API. We evaluated PostgreSQL full-text search (`tsvector`) in Q1 but rejected it due to limited relevance tuning and poor performance beyond 100k rows with complex queries. The team has no prior experience operating Elasticsearch but has budget for a managed service.

## 3. Proposed Solution

Introduce OpenSearch (AWS managed) as a read-optimized search index alongside PostgreSQL as the system of record. A sync worker streams product changes from PostgreSQL to OpenSearch via CDC (Debezium). The API adds a `GET /v1/products/search?q=` endpoint that queries OpenSearch and returns product IDs, which are hydrated from PostgreSQL.

**Alternatives considered:**
- **PostgreSQL tsvector**: Rejected — relevance tuning insufficient, P99 > 2s at our data volume.
- **Algolia**: Rejected — cost prohibitive at 340k documents with projected query volume (~50 req/s).
- **Typesense**: Viable but less mature managed offering; revisit if OpenSearch operational cost is too high.

## 4. Data Model Changes

New OpenSearch index (no PostgreSQL schema changes):

```json
{
  "products": {
    "mappings": {
      "properties": {
        "id":          { "type": "keyword" },
        "name":        { "type": "text", "analyzer": "english" },
        "description": { "type": "text", "analyzer": "english" },
        "category":    { "type": "keyword" },
        "brand":       { "type": "keyword" },
        "price_cents": { "type": "integer" },
        "attributes":  { "type": "object" },
        "in_stock":    { "type": "boolean" },
        "updated_at":  { "type": "date" }
      }
    }
  }
}
```

Changes are fully additive. PostgreSQL schema is unchanged. OpenSearch index can be rebuilt from PostgreSQL at any time.

## 5. API Changes

**New endpoint:**

`GET /v1/products/search?q={query}&category={cat}&page={n}&per_page={n}`

Response — `200 OK`:
```json
{
  "data": [
    { "id": "prod_482", "name": "TrailMax Waterproof Boot", "score": 12.4 }
  ],
  "meta": { "total": 237, "page": 1, "per_page": 20, "query_time_ms": 45 }
}
```

Error — `400` if `q` is empty or exceeds 200 characters. Error — `503` if OpenSearch is unreachable (fallback: return empty results with `degraded: true` flag).

## 6. Migration Plan

1. **Day 1**: Deploy OpenSearch cluster (2 data nodes, 1 master) in staging
2. **Day 2**: Deploy Debezium connector; run initial full sync of 340k products (~15 min)
3. **Day 3**: Validate index completeness — count match, spot-check 500 random products
4. **Day 4**: Deploy search API behind feature flag (`search_v2`), internal testing
5. **Day 5**: Enable flag for 10% of users, monitor latency and relevance feedback
6. **Day 6-7**: Ramp to 100% if P99 < 200ms and no critical bugs

No downtime required. CDC ensures ongoing sync after initial load.

## 7. Rollback Plan

- **Feature flag**: Disable `search_v2` flag to revert to category browsing (instant)
- **Infrastructure**: OpenSearch cluster can be torn down independently; no PostgreSQL changes to reverse
- **Data**: No data migration to roll back — OpenSearch is a derived index
- **Decision criteria**: Roll back if P99 > 500ms for 5 minutes, error rate > 2%, or index drift > 100 documents

## 8. Monitoring & Alerting

| Metric | Threshold | Alert |
|--------|-----------|-------|
| Search P99 latency | > 300ms for 5 min | PagerDuty to @search-team |
| OpenSearch cluster health | Yellow or Red | PagerDuty to @platform |
| Index drift (PG count - OS count) | > 50 documents for 10 min | Slack to #search-alerts |
| CDC consumer lag | > 60s | Slack to #search-alerts |

Dashboard: "Product Search" in Datadog, linked from service catalog.

## 9. Open Questions

| Question | Owner | Blocks? |
|----------|-------|---------|
| Do we need search analytics (popular queries, zero-result queries)? | @product | No — can add post-launch |
| Should search results include out-of-stock products? | @product | Yes — affects index filter |
| Synonym support (e.g., "sneakers" = "trainers") — V1 or later? | @search-team | No |

## 10. Out of Scope

- Search autocomplete / typeahead (follow-up spec SEARCH-102)
- Personalized ranking based on user history (requires ML pipeline, Q2)
- Admin UI for managing synonyms and boost rules
