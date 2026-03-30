---
name: database-migration-plan
description: Plan database schema migrations (DDL changes) with backward-compatible strategies, migration scripts, rollback procedures, and zero-downtime deployment patterns. Covers column additions, type changes, index management, and table restructuring.
metadata:
  displayName: "Database Migration Plan"
  categories: ["engineering"]
  tags: ["database", "migration", "schema", "ddl", "zero-downtime", "rollback", "postgresql", "mysql"]
  worksWellWithAgents: ["database-architect", "database-migrator", "devops-engineer"]
  worksWellWithSkills: ["release-checklist", "system-design-document"]
---

# Database Migration Plan

## Before you start

Gather the following from the user:

1. **What schema change is needed?** (Add column, rename column, change type, add/drop index, create/drop table, split table)
2. **Which database engine?** (PostgreSQL, MySQL, SQL Server, or engine-agnostic)
3. **Is zero-downtime required?** (Can the application tolerate maintenance windows?)
4. **What is the table size?** (Row count and data size — this determines strategy)
5. **Are there dependent applications?** (Other services reading/writing this table)
6. **What ORM or migration tool is in use?** (Prisma, Drizzle, Knex, Flyway, Alembic, ActiveRecord, raw SQL)

If the user says "add a column to the users table," push back: "How many rows? Is the app deployed with zero-downtime requirements? Is the column nullable or does it need a default? Other services reading this table?"

This skill covers **schema-level DDL changes**. For moving data between systems or ETL pipelines, see the `data-migration-plan` skill instead.

## Procedure

### Step 1: Classify the migration risk

| Change type | Lock risk | Data risk | Typical approach |
|------------|-----------|-----------|------------------|
| Add nullable column | Low | None | Single migration |
| Add column with default | Medium (engine-dependent) | None | Check engine behavior |
| Add index | Medium-High | None | CREATE INDEX CONCURRENTLY |
| Drop column | Low | High (data loss) | Multi-phase |
| Rename column | High | Medium | Multi-phase with alias |
| Change column type | High | High | Multi-phase with dual-write |
| Drop table | Low | High (data loss) | Multi-phase with grace period |
| Split/merge tables | High | High | Multi-phase with dual-write |

For medium or high risk changes, use the multi-phase approach in Step 3.

### Step 2: Write the migration script

Every migration must have an **up** and **down** script:

```sql
-- Migration: 20240115_001_add_status_to_orders
-- Description: Add status column to orders table for fulfillment tracking

-- UP
ALTER TABLE orders ADD COLUMN status VARCHAR(32) NULL;

-- DOWN
ALTER TABLE orders DROP COLUMN status;
```

Rules for migration scripts:

- Name with timestamp prefix and sequential number: `YYYYMMDD_NNN_description`
- One logical change per migration file — never bundle unrelated changes
- DOWN script must be tested and produce the exact prior schema
- Include comments stating what the migration does and why
- For large tables, include estimated execution time

### Step 3: Multi-phase migration pattern

For changes that require zero-downtime on production tables:

1. **Expand** — Add the new structure alongside the old (e.g., `ALTER TABLE ADD COLUMN status_new NULL`).
2. **Dual-write** — Deploy code that writes to both old and new. Reads prefer new, fall back to old.
3. **Backfill** — Migrate existing data in batches (5,000-50,000 rows per commit). Monitor replication lag between batches.
4. **Cutover** — Switch all reads and writes to the new structure. Verify no queries reference the old column in production logs.
5. **Contract** — Drop the old structure (`ALTER TABLE DROP COLUMN`).

Each phase is a separate deployment. Never combine phases into one release.

### Step 4: Handle engine-specific concerns

**PostgreSQL:** `ADD COLUMN` with non-volatile default is metadata-only in PG 11+. Use `CREATE INDEX CONCURRENTLY` (cannot run inside a transaction). `ALTER COLUMN TYPE` rewrites the table on large tables — use multi-phase.

**MySQL (InnoDB):** Use `ALGORITHM=INPLACE, LOCK=NONE` where supported. Adding a column with default rewrites the table in MySQL < 8.0.12 — use `pt-online-schema-change` or `gh-ost` for large tables.

### Step 5: Write the rollback plan

For each migration phase, document:

```
Phase: [N]
Rollback trigger: [What condition triggers rollback]
Rollback steps:
  1. [Exact SQL or deployment step]
  2. [Verify step]
Time estimate: [How long rollback takes]
Data impact: [What data is lost on rollback, if any]
```

Rollback must be tested in staging before production deployment. If the DOWN migration involves data loss, document what is lost and whether it is recoverable from backups.

### Step 6: Define the verification plan

After each phase, verify three areas:

- **Schema:** Run `\d table_name` (PG) or `DESCRIBE table_name` (MySQL). Compare against expected state.
- **Data:** Row count matches pre-migration. Null check on new columns shows 0 after backfill. Spot check sample rows.
- **Application:** Health checks return 200, error rates unchanged, query latency p99 within baseline.

## Quality checklist

Before delivering the migration plan, verify:

- [ ] Every migration has both UP and DOWN scripts
- [ ] High-risk changes use the multi-phase expand/migrate/contract pattern
- [ ] Backfill runs in batches with commit points, not one massive UPDATE
- [ ] Rollback plan exists for each phase with explicit triggers and time estimates
- [ ] Engine-specific locking behavior is accounted for
- [ ] Verification queries are included for schema, data integrity, and performance
- [ ] The plan distinguishes between schema changes (this skill) and data movement (data-migration-plan)

## Common mistakes

- **Running ALTER TABLE on a large table without checking lock behavior.** A table-rewriting ALTER on a 100M-row table locks writes for minutes. Check your engine version's online DDL support first.
- **Combining expand and contract in one deployment.** If the new schema has a bug, you cannot roll back without data loss. Always separate by at least one deployment cycle.
- **Backfilling without batching.** `UPDATE orders SET x = y` on 50M rows creates a massive transaction, bloats WAL/binlog, and may cause replication lag or OOM. Batch in chunks of 5,000-50,000.
- **Skipping the DOWN migration.** "We will never roll back" is not a plan. Write and test the rollback script before running the forward migration.
- **Forgetting dependent services.** Another team's service may query the column you are renaming. Check for cross-service dependencies before dropping or renaming.
- **Not monitoring replication lag during backfill.** On replicated databases, large writes increase replication lag. Pause between batches if lag exceeds your threshold.
