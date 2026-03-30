# Example: Multi-Phase Column Rename

Renaming `orders.shipping_addr` to `orders.shipping_address` on a PostgreSQL 15 table with 12M rows. Zero-downtime requirement. Two services read/write this table: `order-service` and `fulfillment-service`.

---

## Risk Classification

| Change type | Lock risk | Data risk | Approach |
|-------------|-----------|-----------|----------|
| Rename column | High | Medium | Multi-phase (expand/dual-write/backfill/cutover/contract) |

A direct `ALTER TABLE RENAME COLUMN` is metadata-only in PostgreSQL, but it instantly breaks every query referencing the old name. With two services deployed independently, a direct rename causes downtime. Multi-phase avoids this.

---

## Phase 1: Expand

Add the new column alongside the old one.

```sql
-- Migration: 20240310_001_add_shipping_address_to_orders
-- UP
ALTER TABLE orders ADD COLUMN shipping_address TEXT NULL;

-- DOWN
ALTER TABLE orders DROP COLUMN IF EXISTS shipping_address;
```

**Execution notes**:
- `ADD COLUMN ... NULL` is metadata-only in PostgreSQL. No table rewrite, sub-second execution.
- No index needed yet (will copy the existing index in Phase 3).

**Verification**:
```sql
\d orders
-- Confirm shipping_address column exists, type TEXT, nullable
```

---

## Phase 2: Dual-Write

Deploy code changes so both columns are populated on every write.

**order-service** (handles inserts and updates):
```sql
-- Every INSERT now writes both columns
INSERT INTO orders (shipping_addr, shipping_address, ...)
VALUES ($1, $1, ...);

-- Every UPDATE writes both columns
UPDATE orders
SET shipping_addr = $1, shipping_address = $1
WHERE id = $2;
```

**fulfillment-service** (updates shipping info):
```sql
UPDATE orders
SET shipping_addr = $1, shipping_address = $1
WHERE id = $2;
```

**Reads still use `shipping_addr`** -- no read path changes yet.

**Integrity check** (run after deploying dual-write to both services):
```sql
-- All new writes should have matching values
SELECT COUNT(*) FROM orders
WHERE shipping_address IS NOT NULL
  AND shipping_addr IS DISTINCT FROM shipping_address;
-- Expected: 0
```

**Rollback trigger**: If dual-write error rate > 0.1%, revert both service deployments. The new column exists but is unused -- harmless.

---

## Phase 3: Backfill

Copy historical data from `shipping_addr` to `shipping_address` for rows written before dual-write was deployed.

```sql
-- Backfill in batches of 10,000
UPDATE orders
SET shipping_address = shipping_addr
WHERE id BETWEEN $start AND $start + 9999
  AND shipping_address IS NULL;
```

Run with a script that:
1. Iterates from `MIN(id)` to `MAX(id)` in increments of 10,000.
2. Pauses 500ms between batches to limit replication lag.
3. Logs progress: batch number, rows updated, elapsed time.
4. Is idempotent -- the `WHERE shipping_address IS NULL` guard makes re-runs safe.

**Estimated duration**: 12M rows / 10K per batch = 1,200 batches. At ~50ms per batch + 500ms pause = ~11 minutes.

**Integrity check after backfill**:
```sql
-- No nulls remaining
SELECT COUNT(*) FROM orders WHERE shipping_address IS NULL;
-- Expected: 0

-- No value mismatches
SELECT COUNT(*) FROM orders
WHERE shipping_addr IS DISTINCT FROM shipping_address;
-- Expected: 0

-- Spot-check
SELECT id, shipping_addr, shipping_address
FROM orders ORDER BY RANDOM() LIMIT 100;
-- Every row: values match
```

**Rollback trigger**: If replication lag > 30 seconds, pause backfill and reduce batch size. If data corruption detected, stop and investigate.

---

## Phase 4: Cutover

Switch reads from `shipping_addr` to `shipping_address` using a feature flag.

**Ramp schedule**:

| Stage | Traffic % | Duration | Metric check |
|-------|-----------|----------|--------------|
| Shadow | 1% | 30 min | Compare old vs new column reads; log mismatches |
| Partial | 25% | 1 hour | Error rate, p99 latency |
| Majority | 75% | 2 hours | Same |
| Full | 100% | 24 hour soak | Same |

**order-service read path**:
```python
if feature_flag("use_shipping_address"):
    query = "SELECT shipping_address FROM orders WHERE id = $1"
else:
    query = "SELECT shipping_addr FROM orders WHERE id = $1"
```

**Add index on the new column** (before ramping to 100%):
```sql
CREATE INDEX CONCURRENTLY idx_orders_shipping_address
ON orders (shipping_address);
```

**Rollback trigger**: If error rate or latency degrades at any stage, set feature flag to 0%. Immediate -- no deployment needed.

**Verification at 100%**:
```sql
-- Confirm no queries use the old column (check pg_stat_statements)
SELECT query FROM pg_stat_statements
WHERE query LIKE '%shipping_addr%'
  AND query NOT LIKE '%shipping_address%';
-- Expected: no rows (after soak period)
```

---

## Phase 5: Contract

Remove the old column after a one-release-cycle grace period.

```sql
-- Migration: 20240324_001_drop_shipping_addr_from_orders
-- UP
DROP INDEX IF EXISTS idx_orders_shipping_addr;
ALTER TABLE orders DROP COLUMN IF EXISTS shipping_addr;

-- DOWN (requires backup restore for data recovery)
ALTER TABLE orders ADD COLUMN shipping_addr TEXT NULL;
-- Data must be restored from backup or copied from shipping_address:
-- UPDATE orders SET shipping_addr = shipping_address;
```

**Code cleanup**:
- Remove dual-write logic from order-service and fulfillment-service.
- Remove the feature flag.
- Update schema documentation and any ORM model definitions.

---

## Timeline Summary

| Phase | When | Duration | Risk |
|-------|------|----------|------|
| Expand | Day 1 | Minutes | Low |
| Dual-Write | Day 1 (after expand deploy) | 1 deploy cycle | Low |
| Backfill | Day 2 | ~11 minutes | Low |
| Cutover | Days 2-5 (ramp + 24h soak) | 3-4 days | Medium |
| Contract | Day 12+ (after grace period) | Minutes | Low |

**Total elapsed**: ~2 weeks including soak and grace periods.
