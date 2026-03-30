# Worked Example: API Endpoint Optimization

Full optimization walkthrough for a slow `/api/orders` endpoint -- from baseline through profiling, fixes, and verification.

## Context

- **Stack:** Node.js (Express), PostgreSQL, Redis
- **Endpoint:** `GET /api/orders?userId=123`
- **Complaint:** "Order history page takes 6 seconds to load"

---

## Step 1: Baseline

Three measurements taken on staging with production-like data (1.2M orders, 85K users):

| Run | p50 | p95 | p99 |
|-----|-----|-----|-----|
| 1 | 2,100 ms | 5,800 ms | 8,200 ms |
| 2 | 2,050 ms | 5,900 ms | 8,400 ms |
| 3 | 2,200 ms | 5,750 ms | 8,100 ms |
| **Avg** | **2,117 ms** | **5,817 ms** | **8,233 ms** |

**Target:** p95 under 200 ms.

**Tool:** `k6` with 50 concurrent users over 60 seconds.

---

## Step 2: Profiler Output

### 2a. Distributed trace (OpenTelemetry / Jaeger)

```
GET /api/orders (total: 5,820 ms)
  |-- auth middleware:         12 ms
  |-- parseQuery:               1 ms
  |-- db.getOrders:         3,400 ms  <-- 58% of total
  |-- db.getOrderItems:     2,200 ms  <-- 38% of total
  |-- serialize response:     180 ms
  |-- send response:           27 ms
```

Two database calls account for 96% of latency.

### 2b. Database query analysis

**Query 1 -- `db.getOrders`:**

```sql
EXPLAIN (ANALYZE, BUFFERS) SELECT * FROM orders WHERE user_id = 123 ORDER BY created_at DESC;
```

```
Sort  (cost=45230..45280 rows=198 width=412) (actual time=3380.12..3380.45 rows=198 loops=1)
  Sort Key: created_at DESC
  ->  Seq Scan on orders  (cost=0..41520 rows=198 width=412) (actual time=0.05..3370.22 rows=198 loops=1)
        Filter: (user_id = 123)
        Rows Removed by Filter: 1199802
        Buffers: shared read=18420
```

**Problem:** Sequential scan on 1.2M rows. No index on `user_id`.

**Query 2 -- `db.getOrderItems`:**

```javascript
// Application code
for (const order of orders) {
  order.items = await db.query('SELECT * FROM order_items WHERE order_id = $1', [order.id]);
}
```

**Problem:** N+1 query pattern. 198 orders = 198 individual queries.

---

## Step 3: One Fix at a Time

### Fix 1: Add index on `orders.user_id`

```sql
CREATE INDEX CONCURRENTLY idx_orders_user_id ON orders (user_id, created_at DESC);
```

**Measurement after Fix 1:**

| Metric | Before | After | Change |
|--------|--------|-------|--------|
| db.getOrders | 3,400 ms | 8 ms | -99.8% |
| Endpoint p95 | 5,817 ms | 2,450 ms | -57.9% |

The index eliminated the sequential scan. Endpoint p95 is now dominated by the N+1 queries.

### Fix 2: Eliminate N+1 with batch query

Replace the loop:

```javascript
// Before: N+1
for (const order of orders) {
  order.items = await db.query('SELECT * FROM order_items WHERE order_id = $1', [order.id]);
}

// After: single batch query
const orderIds = orders.map(o => o.id);
const allItems = await db.query(
  'SELECT * FROM order_items WHERE order_id = ANY($1)',
  [orderIds]
);
const itemsByOrder = groupBy(allItems.rows, 'order_id');
for (const order of orders) {
  order.items = itemsByOrder[order.id] || [];
}
```

**Measurement after Fix 2:**

| Metric | Before | After | Change |
|--------|--------|-------|--------|
| db.getOrderItems | 2,200 ms | 15 ms | -99.3% |
| Endpoint p95 | 2,450 ms | 230 ms | -90.6% |

Close to target but still above 200 ms. The trace now shows `serialize response: 180 ms` as the bottleneck.

### Fix 3: Paginate and select only needed columns

```javascript
// Before: SELECT * with all 198 orders
const orders = await db.query('SELECT * FROM orders WHERE user_id = $1 ORDER BY created_at DESC', [userId]);

// After: SELECT specific columns, limit 20
const orders = await db.query(
  'SELECT id, status, total, currency, created_at FROM orders WHERE user_id = $1 ORDER BY created_at DESC LIMIT 20 OFFSET $2',
  [userId, offset]
);
```

**Measurement after Fix 3:**

| Metric | Before | After | Change |
|--------|--------|-------|--------|
| Response payload | 142 KB | 8 KB | -94.4% |
| serialize response | 180 ms | 6 ms | -96.7% |
| Endpoint p95 | 230 ms | 45 ms | -80.4% |

---

## Step 4: Final Before/After Comparison

| Metric | Before (baseline) | After (all fixes) | Change |
|--------|-------------------|-------------------|--------|
| Endpoint p50 | 2,117 ms | 28 ms | -98.7% |
| Endpoint p95 | 5,817 ms | 45 ms | -99.2% |
| Endpoint p99 | 8,233 ms | 82 ms | -99.0% |
| Response size | 142 KB | 8 KB | -94.4% |
| DB queries per request | 199 | 2 | -99.0% |

**Target (p95 < 200 ms): ACHIEVED at 45 ms.**

## Optimization Log (Summary)

| # | Fix Applied | Metric | Before | After | Change |
|---|-------------|--------|--------|-------|--------|
| 1 | Index on orders.user_id | db.getOrders | 3,400 ms | 8 ms | -99.8% |
| 2 | Batch order_items query | db.getOrderItems | 2,200 ms | 15 ms | -99.3% |
| 3 | Paginate + select columns | serialize response | 180 ms | 6 ms | -96.7% |

## Regression Prevention

- Added `LIMIT` enforcement in the query layer (max 100 per page).
- Added p95 latency alert on `/api/orders` at 150 ms threshold.
- Added integration test verifying the endpoint uses <= 3 SQL queries per request.
