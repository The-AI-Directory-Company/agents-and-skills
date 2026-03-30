# Rollback Plan

Fill in for each phase before starting the migration. This document should be ready before Phase 1 begins.

## Migration Summary

| Field | Value |
|-------|-------|
| Migration name | |
| Owner | |
| Point of no return | Phase ___ (after this, rollback requires restore from backup) |

---

## Rollback Summary by Phase

| Phase | Rollback Action | Data Loss Risk | Estimated Time | Owner |
|-------|-----------------|----------------|----------------|-------|
| Phase 1: Dual-Write | Revert deployment, drop new columns/tables | None | | |
| Phase 2: Backfill | Stop backfill, truncate new tables, disable dual-write | None (old data untouched) | | |
| Phase 3: Cutover | Flip feature flag to route reads back to old schema | None (old schema still populated) | | |
| Phase 4: Verification | Same as Phase 3 (old schema still exists) | None | | |
| Phase 5: Cleanup | Restore from backup (old schema dropped) | Data written after cleanup started | | |

---

## Phase 1 Rollback: Dual-Write

**Trigger**: Dual-write error rate exceeds 0.1%, or new write path causes application errors.

**Steps**:
1.
2.
3.

**Verification**:
- [ ] Application error rate returns to baseline
- [ ] No writes reaching new columns/tables

---

## Phase 2 Rollback: Backfill

**Trigger**: Backfill causes replica lag > 30 seconds, data corruption detected, or error rate spikes.

**Steps**:
1.
2.
3.

**Verification**:
- [ ] Replica lag returns to normal
- [ ] Old schema data is intact (spot-check)
- [ ] Dual-write disabled

---

## Phase 3 Rollback: Cutover

**Trigger**: Error rate or latency degrades at any ramp stage, or data correctness issues found.

**Steps**:
1.
2.
3.

**Verification**:
- [ ] All reads using old schema
- [ ] Metrics return to baseline within 10 minutes

---

## Phase 4 Rollback: Verification

**Trigger**: Downstream consumers report incorrect data, or consistency check fails.

**Steps**:
1.
2.
3.

**Verification**:
- [ ] Downstream consumers confirmed healthy
- [ ] Read path on old schema

---

## Phase 5 Rollback: Cleanup (Emergency)

**Trigger**: Only if old schema was dropped and a critical issue is discovered.

**Steps**:
1.
2.
3.

**Verification**:
- [ ] Backup restored successfully
- [ ] Row counts match pre-cleanup snapshot
- [ ] Application healthy on restored schema

**Data at risk**: Any data written between cleanup start and restore completion.
