# Migration Plan: User Accounts Schema Restructuring

## Overview

Restructure the `users` table into separate `accounts` and `profiles` tables to support multi-tenant access. PostgreSQL 15, ~8.2M rows, zero-downtime requirement.

## Pre-Migration Assessment

- **Affected services**: auth-service, billing-api, admin-dashboard, analytics-etl, email-worker
- **Foreign keys**: `orders.user_id`, `sessions.user_id`, `audit_logs.actor_id` (12 tables total)
- **Baseline performance**: P50 = 2ms, P99 = 18ms on `users` table lookups
- **Estimated backfill duration**: 47 minutes (tested against production replica at 10k rows/batch)
- **Backup verified**: Full pg_dump restore tested on 2026-03-12 — 22 minutes to restore

## Phase 1: Dual-Write (Days 1-3)

**Entry criteria**: All CI checks pass, backup verified within 7 days.

1. Deploy additive schema: create `accounts` and `profiles` tables alongside `users`
2. Update auth-service and billing-api write paths to insert into both `users` and `accounts`/`profiles`
3. Deploy dual-write consistency logger — compare row-by-row on every write

**Integrity check**: `SELECT count(*) FROM accounts a LEFT JOIN users u ON a.legacy_user_id = u.id WHERE u.id IS NULL;` must return 0.

**Rollback trigger**: Dual-write error rate > 0.1% over any 10-minute window. Action: revert auth-service deploy, drop `accounts` and `profiles` tables.

## Phase 2: Backfill (Day 4)

**Entry criteria**: Dual-write running 48+ hours with zero divergences.

1. Run backfill in batches of 5,000 rows with 200ms delay between batches
2. Monitor replica lag — pause if lag exceeds 5 seconds
3. Use `INSERT INTO accounts (...) SELECT ... FROM users ON CONFLICT (legacy_user_id) DO UPDATE`

**Integrity check**: Row count match + spot-check 2,000 random rows for field equality:
```sql
SELECT count(*) FROM users u
JOIN accounts a ON a.legacy_user_id = u.id
WHERE u.email != a.email OR u.created_at != a.created_at;
-- Must return 0
```

**Rollback trigger**: Replica lag > 30s sustained, or any data mismatch detected. Action: pause backfill, investigate, reduce batch size to 1,000.

## Phase 3: Cutover (Days 5-9)

**Entry criteria**: Backfill complete, 100% row parity confirmed.

| Stage | Read traffic % | Duration | Gate |
|-------|---------------|----------|------|
| Canary | 1% | 4 hours | Error rate < 0.01%, P99 < 22ms |
| Partial | 10% | 12 hours | Error rate < 0.01%, P99 < 20ms |
| Majority | 50% | 24 hours | Error rate < 0.005% |
| Full | 100% | 48 hours soak | P99 within 10% of baseline |

**Rollback trigger**: Error rate or latency exceeds gate thresholds. Action: set feature flag `use_new_accounts_schema` to false — immediate revert to `users` table reads.

## Phase 4: Verification (Days 10-12)

1. Final consistency check: row counts, checksums on email and created_at columns
2. Verify analytics-etl output matches pre-migration baseline report (< 0.01% variance)
3. Confirm no queries hit `users` table directly (check `pg_stat_user_tables` for seq/idx scans)
4. Sign-off from data-eng lead and product-eng lead

## Phase 5: Cleanup (Days 20-25)

1. Remove dual-write code from auth-service and billing-api
2. Drop `users` table after 2 release cycles (grace period through Day 25)
3. Update schema diagrams, ERD docs, and runbooks
4. Archive migration scripts in `migrations/2026-03-archive/`

## Rollback Summary

| Phase | Rollback action | Data loss risk |
|-------|----------------|----------------|
| 1 — Dual-Write | Revert deploy, drop new tables | None |
| 2 — Backfill | Stop backfill, truncate new tables | None |
| 3 — Cutover | Flip feature flag to 0% | None |
| 4+ — Post-cleanup | Restore from backup (point of no return) | Up to RPO window |
