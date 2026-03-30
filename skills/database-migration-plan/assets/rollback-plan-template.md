# Rollback Plan Template

Complete one block per migration phase. This document must be ready before executing any migration.

## Migration Summary

| Field | Value |
|-------|-------|
| Migration name | |
| Database engine | |
| Affected table(s) | |
| Owner | |

---

## Rollback Blocks

### Phase: Expand

**Trigger**: Schema change causes application errors, locking exceeds acceptable duration, or replication lag spikes.

**Steps**:
1.
2.
3.

**Time estimate**:

**Data impact**: None -- additive change only, no data modified or removed.

---

### Phase: Dual-Write

**Trigger**: Dual-write error rate > 0.1%, write latency degrades, or data divergence detected between old and new columns.

**Steps**:
1.
2.
3.

**Time estimate**:

**Data impact**: New column data discarded. Old column data intact.

---

### Phase: Backfill

**Trigger**: Replication lag > threshold, lock contention on production queries, or data corruption detected in spot-check.

**Steps**:
1.
2.
3.

**Time estimate**:

**Data impact**: Incomplete backfill data in new column. Old column data intact.

---

### Phase: Cutover

**Trigger**: Read errors from new column, latency regression at any ramp stage, or business metrics degrade.

**Steps**:
1.
2.
3.

**Time estimate**:

**Data impact**: None -- feature flag routes reads back to old column immediately.

---

### Phase: Contract

**Trigger**: Post-cleanup issue discovered (old column already dropped).

**Steps**:
1.
2.
3.

**Time estimate**:

**Data impact**: Data written after column drop may be lost if restoring from backup. Document the gap window.

---

## Rollback Verification Checklist

After any rollback, confirm:

- [ ] Application error rate returns to pre-migration baseline
- [ ] Query latency (p50, p99) returns to baseline
- [ ] Schema matches expected pre-migration state (`\d table` or `DESCRIBE table`)
- [ ] No orphaned data in new columns/tables
- [ ] Downstream services confirmed healthy
- [ ] Stakeholders notified of rollback and reason
