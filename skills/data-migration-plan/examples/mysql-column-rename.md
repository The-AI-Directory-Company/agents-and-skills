# Example: MySQL Column Rename (5-Phase Migration)

Renaming `users.email_address` to `users.email` in a MySQL 8.0 production table with 2M rows, zero-downtime requirement.

This example demonstrates the 5-phase template scaled down to a straightforward column rename.

---

## Pre-Migration Assessment

- **Affected table**: `users` (2M rows, 450 MB)
- **Services that read `email_address`**: auth-service, notification-service, analytics ETL
- **Services that write `email_address`**: auth-service, admin-api
- **Downtime tolerance**: Zero
- **Estimated backfill duration**: ~3 minutes (2M rows at 10K/batch)

---

## Phase 1: Expand (Add New Column)

```sql
-- Migration: 20240620_001_add_email_column_to_users
-- UP
ALTER TABLE users ADD COLUMN email VARCHAR(255) NULL;
CREATE INDEX idx_users_email ON users (email);

-- DOWN
DROP INDEX idx_users_email ON users;
ALTER TABLE users DROP COLUMN email;
```

**Deploy code change**: All write paths populate both `email_address` and `email`.

```python
# Dual-write in auth-service
def create_user(email_value):
    db.execute(
        "INSERT INTO users (email_address, email, ...) VALUES (%s, %s, ...)",
        (email_value, email_value, ...)
    )
```

**Integrity check**: Confirm dual-write is working.

```sql
SELECT COUNT(*) FROM users
WHERE email IS NOT NULL AND NOT (email_address <=> email);
-- Expected: 0
```

---

## Phase 2: Backfill (Historical Data)

```sql
-- Backfill in batches of 10,000
SET @batch_start = 0;
SET @batch_size = 10000;

UPDATE users
SET email = email_address
WHERE id > @batch_start AND id <= @batch_start + @batch_size
  AND email IS NULL;

-- Repeat, incrementing @batch_start by @batch_size each iteration.
-- Monitor replica lag between batches; pause if lag > 5 seconds.
```

**Integrity check after backfill**:

```sql
-- Row count comparison
SELECT
  COUNT(*) AS total,
  SUM(CASE WHEN email IS NULL THEN 1 ELSE 0 END) AS missing_email
FROM users;
-- Expected: missing_email = 0

-- Spot-check
SELECT id, email_address, email
FROM users
ORDER BY RAND()
LIMIT 100;
-- Every row: email_address = email
```

---

## Phase 3: Cutover (Switch Reads)

Deploy read path changes behind a feature flag:

1. **1% of reads** use `email` column. Compare results against `email_address` in shadow mode.
2. **10% of reads** -- monitor latency and error rate.
3. **50% of reads** -- hold for 1 hour.
4. **100% of reads** -- soak for 24 hours.

**Rollback trigger**: If error rate increases or latency degrades at any stage, set flag to 0%.

---

## Phase 4: Verification

```sql
-- Final consistency check
SELECT COUNT(*) FROM users WHERE NOT (email_address <=> email);
-- Expected: 0
```

- Confirm auth-service, notification-service, and analytics ETL all read from `email`.
- Check query logs: no queries reference `email_address`.
- Get sign-off from data owner.

---

## Phase 5: Contract (Remove Old Column)

Wait one full release cycle after cutover, then:

```sql
-- Migration: 20240704_001_drop_email_address_from_users
-- UP
ALTER TABLE users DROP COLUMN email_address;

-- DOWN (requires restore from backup if needed)
-- ALTER TABLE users ADD COLUMN email_address VARCHAR(255) NULL;
-- UPDATE users SET email_address = email;
```

Remove dual-write code from auth-service and admin-api. Remove the feature flag. Update documentation and schema diagrams.

---

## Timeline Summary

| Phase | Duration | Risk |
|-------|----------|------|
| Phase 1: Expand | 1 deploy cycle | Low |
| Phase 2: Backfill | ~3 minutes | Low |
| Phase 3: Cutover | 2-3 days (ramp + soak) | Medium |
| Phase 4: Verification | 1 day | Low |
| Phase 5: Contract | 1 deploy cycle (after grace period) | Low |

**Total elapsed**: ~1-2 weeks including soak and grace periods.
