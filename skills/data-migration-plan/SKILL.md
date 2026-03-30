---
name: data-migration-plan
description: Plan and execute data migrations with phased rollout — dual-write, backfill, cutover, and verification stages with rollback triggers and data integrity checks at every step.
metadata:
  displayName: "Data Migration Plan"
  categories: ["engineering", "data"]
  tags: ["migration", "data", "schema", "rollback", "database", "ETL"]
  worksWellWithAgents: ["code-migrator", "data-engineer", "database-architect", "database-migrator"]
  worksWellWithSkills: ["system-design-document", "ticket-writing"]
---

# Data Migration Plan

## Before you start

Gather the following from the user. If any is missing, ask before proceeding:

1. **Current schema** — Tables, columns, relationships, and storage engine. Include indexes and constraints.
2. **Target schema** — The desired end state. What changes: renamed columns, split tables, new relationships, type changes?
3. **Data volume** — Row counts for affected tables, total size on disk, and growth rate.
4. **Downtime tolerance** — Zero-downtime required? Maintenance window available? If so, how long?
5. **Rollback requirements** — How quickly must you revert? Is data loss during rollback acceptable? What is the point-of-no-return?

If the user says "just rename a column," push back: What reads from this column? Are there cached references? Is the column in any API contract, event payload, or downstream ETL?

## Migration plan template

Use the following structure. Every phase includes explicit entry criteria, steps, and exit criteria.

### Pre-Migration Assessment

Before writing any migration code:

- Catalog every service, job, and query that reads or writes the affected tables
- Identify foreign key dependencies and cascade behavior
- Measure current query performance on affected tables (baseline P50/P99)
- Estimate migration duration: run the backfill query against a production-sized replica
- Confirm backup and restore procedures work — test the restore, not just the backup

### Phase 1: Dual-Write

**Goal**: New writes go to both old and new schema without affecting reads.

1. Deploy schema changes additively (new columns, new tables) — never drop or rename yet
2. Update write paths to populate both old and new locations
3. Add logging to confirm dual-write consistency (compare old vs. new on every write)
4. **Integrity check**: Query for rows where old and new values diverge. Count must be zero before proceeding.

**Rollback trigger**: If dual-write error rate exceeds 0.1%, disable new write path and revert deployment.

### Phase 2: Backfill

**Goal**: Migrate all historical data from old schema to new schema.

1. Run backfill in batches (1,000–10,000 rows per batch, tuned to avoid lock contention)
2. Throttle to keep replica lag under your threshold (e.g., < 5 seconds)
3. Use idempotent upserts so the backfill can be safely restarted at any point
4. Log progress: batch number, rows processed, elapsed time, estimated time remaining
5. **Integrity check**: After backfill completes, run a full-table comparison — old source vs. new target. Row count must match. Spot-check 1,000 random rows for value equality.

**Rollback trigger**: If backfill causes replica lag > 30 seconds or error rate spikes, pause and reduce batch size. If data corruption is detected, stop and revert to Phase 1 state.

### Phase 3: Cutover

**Goal**: Switch reads from old schema to new schema.

1. Deploy read path changes behind a feature flag — route a small percentage of reads to new schema first (1%, 10%, 50%, 100%)
2. Compare read results between old and new paths during the ramp (shadow reads or dual-read with comparison logging)
3. Monitor latency, error rate, and correctness at each ramp stage
4. At 100%, hold for a soak period (minimum 24 hours in production) before proceeding
5. **Integrity check**: P99 latency on new read path must be within 10% of the old path baseline.

**Rollback trigger**: If error rate or latency degrades at any ramp stage, set feature flag back to 0% immediately.

### Phase 4: Verification

**Goal**: Confirm the migration is complete and correct before cleanup.

1. Run final consistency check: compare row counts and checksums between old and new schema
2. Verify all downstream consumers (reports, analytics, ETL jobs, APIs) produce correct output
3. Confirm no service is still reading from or writing to the old schema (check query logs)
4. Document any data that was intentionally dropped, transformed, or defaulted during migration
5. Get sign-off from the data owner before proceeding to cleanup

### Phase 5: Cleanup

**Goal**: Remove old schema and dual-write code.

1. Remove dual-write code paths and feature flags
2. Drop old columns or tables (after a grace period — typically 1–2 release cycles)
3. Update documentation, runbooks, and schema diagrams
4. Archive the migration scripts for audit trail

**Do not skip cleanup.** Leftover dual-write code becomes a maintenance burden and a source of subtle bugs.

### Rollback Plan

Document the full rollback procedure upfront, not during an incident:

- **Phase 1 rollback**: Revert deployment, remove new columns/tables. No data loss.
- **Phase 2 rollback**: Stop backfill, truncate new tables. Dual-write code still active — disable it.
- **Phase 3 rollback**: Flip feature flag to route all reads back to old schema. Immediate.
- **Phase 4+ rollback**: If old schema is already dropped, you need a restore from backup. This is the point of no return — make sure you are past it before cleanup.

## Quality checklist

Before delivering the migration plan, verify:

- [ ] Every phase has explicit entry criteria, steps, and exit criteria
- [ ] Rollback triggers are defined with specific thresholds (not "if something goes wrong")
- [ ] Data integrity checks exist at every phase boundary
- [ ] Backfill is idempotent and restartable
- [ ] Downstream consumers are cataloged and their migration path is documented
- [ ] The rollback plan covers every phase, including the point of no return
- [ ] Migration duration has been estimated against production-scale data

## Common mistakes to avoid

- **Skipping the dual-write phase**. Going straight from old schema to new schema forces a big-bang cutover. Dual-write lets you validate incrementally and roll back safely.
- **Non-idempotent backfills**. If your backfill crashes at row 500,000, you need to restart from the beginning unless your upsert logic is idempotent. Always use `INSERT ... ON CONFLICT UPDATE` or equivalent.
- **Ignoring downstream consumers**. The migration is not done when the database is updated. Every ETL job, cache layer, search index, and analytics pipeline that reads the old schema needs a migration path too.
- **No production-scale test**. A backfill that takes 2 minutes on staging may take 14 hours on production. Always benchmark against a production-sized dataset before scheduling the migration window.
- **Cleaning up too early**. Dropping the old schema the day after cutover leaves no safety net. Keep the old schema readable for at least one full release cycle.
