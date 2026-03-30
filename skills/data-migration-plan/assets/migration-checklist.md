# Pre-Migration Assessment Checklist

Complete every section before writing migration code. Blank fields indicate gaps that must be resolved first.

---

## 1. Migration Summary

| Field | Value |
|-------|-------|
| Migration name | |
| Owner | |
| Target date | |
| Downtime tolerance | Zero / Maintenance window: ______ |
| Rollback deadline (point of no return) | |

---

## 2. Schema Change Description

**Current state**:

```
-- Paste current schema (CREATE TABLE or relevant DDL)
```

**Target state**:

```
-- Paste target schema
```

**What changes**: (renamed columns, type changes, new tables, split tables, etc.)

---

## 3. Service Catalog

List every service, job, and query that reads or writes the affected tables.

| Service / Job | Read / Write / Both | Owner | Migration needed? | Status |
|---------------|---------------------|-------|-------------------|--------|
| | | | | |
| | | | | |
| | | | | |
| | | | | |

---

## 4. Foreign Key Dependencies

| Table | FK Column | References | Cascade behavior | Impact |
|-------|-----------|------------|-------------------|--------|
| | | | | |
| | | | | |

---

## 5. Data Volume

| Table | Row count | Size on disk | Growth rate (rows/day) |
|-------|-----------|--------------|------------------------|
| | | | |
| | | | |

---

## 6. Baseline Performance

Measure before migration. Compare after cutover.

| Query / Operation | p50 (ms) | p99 (ms) | Measured on |
|-------------------|----------|----------|-------------|
| | | | |
| | | | |

---

## 7. Backfill Estimates

| Parameter | Value |
|-----------|-------|
| Total rows to backfill | |
| Batch size | |
| Estimated batches | |
| Estimated duration (production-scale replica) | |
| Throttle threshold (replica lag) | |

---

## 8. Backup Verification

| Check | Status | Verified by | Date |
|-------|--------|-------------|------|
| Backup exists for affected tables | | | |
| Backup restore tested on staging | | | |
| Restore time measured | | | |
| Restored data spot-checked for correctness | | | |

---

## 9. Readiness Sign-Off

| Role | Name | Approved? | Date |
|------|------|-----------|------|
| Migration owner | | | |
| Data owner | | | |
| DBA / SRE | | | |
| Dependent service owner(s) | | | |
