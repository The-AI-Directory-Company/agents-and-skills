# Engine-Specific DDL Notes

## PostgreSQL

### Column Addition

- **`ADD COLUMN ... NULL`**: Metadata-only operation. No table rewrite. Fast regardless of table size.
- **`ADD COLUMN ... DEFAULT value`**: Metadata-only in PostgreSQL 11+ if the default is a constant (non-volatile). Prior versions rewrite the entire table.
- **`ADD COLUMN ... NOT NULL DEFAULT value`**: Same as above in PG 11+ -- metadata-only for constant defaults.

### Index Creation

- **`CREATE INDEX`**: Acquires a `SHARE` lock -- blocks writes for the duration. On large tables this can be minutes to hours.
- **`CREATE INDEX CONCURRENTLY`**: Does not block writes. Takes longer (two table scans instead of one) but allows normal operations to continue.
  - Cannot run inside a transaction block (`BEGIN ... COMMIT`).
  - If it fails partway, leaves an `INVALID` index. Check with `\di+` and drop it before retrying.
  - Migration tools that wrap statements in transactions (e.g., some ORM migration runners) need special handling.
- **Recommendation**: Always use `CONCURRENTLY` for production tables with active traffic.

### Column Type Changes

- **`ALTER COLUMN TYPE`**: Rewrites the entire table for most type changes. Acquires `ACCESS EXCLUSIVE` lock (blocks reads and writes).
- **Safe in-place changes** (no rewrite): `varchar(N)` to `varchar(M)` where M > N, `varchar(N)` to `text`, `numeric(P,S)` to `numeric(P2,S2)` where P2 >= P and S2 >= S.
- **For large tables**: Use the multi-phase expand/dual-write/backfill/cutover/contract pattern instead of `ALTER COLUMN TYPE`.

### Column Rename

- **`ALTER TABLE RENAME COLUMN`**: Metadata-only, instant. But all queries, views, functions, and triggers referencing the old name break immediately.
- **Recommendation**: Use multi-phase migration for zero-downtime renames on tables with multiple consumers.

### Column Drop

- **`ALTER TABLE DROP COLUMN`**: Metadata-only in PostgreSQL (marks column as dropped; space reclaimed on future writes). Fast.
- The column data is not immediately removed from disk. `VACUUM FULL` reclaims space but requires `ACCESS EXCLUSIVE` lock.

### Table Locking Summary

| Operation | Lock Type | Blocks Reads? | Blocks Writes? |
|-----------|-----------|---------------|----------------|
| ADD COLUMN (nullable) | ACCESS EXCLUSIVE (brief) | Momentary | Momentary |
| ADD COLUMN (constant default, PG 11+) | ACCESS EXCLUSIVE (brief) | Momentary | Momentary |
| CREATE INDEX | SHARE | No | Yes |
| CREATE INDEX CONCURRENTLY | SHARE UPDATE EXCLUSIVE | No | No |
| ALTER COLUMN TYPE (rewrite) | ACCESS EXCLUSIVE | Yes | Yes |
| DROP COLUMN | ACCESS EXCLUSIVE (brief) | Momentary | Momentary |

---

## MySQL (InnoDB)

### Online DDL

MySQL 5.6+ supports online DDL with `ALGORITHM` and `LOCK` clauses:

```sql
ALTER TABLE t ADD COLUMN c INT NULL, ALGORITHM=INPLACE, LOCK=NONE;
```

- **`ALGORITHM=INPLACE`**: Avoids full table copy when possible. Falls back to `COPY` if the change requires it.
- **`LOCK=NONE`**: Allows concurrent reads and writes. Fails if the operation cannot be done without locking.
- If MySQL rejects `ALGORITHM=INPLACE, LOCK=NONE`, the operation requires a table copy and will lock the table.

### Column Addition

- **`ADD COLUMN ... NULL`** (MySQL 8.0.12+): `INPLACE` with `LOCK=NONE`. Does not rewrite the table. Instant for nullable columns.
- **`ADD COLUMN ... DEFAULT value`** (MySQL < 8.0.12): Rewrites the entire table. Use `pt-online-schema-change` or `gh-ost` for large tables.
- **`ADD COLUMN ... DEFAULT value`** (MySQL 8.0.12+): Instant metadata change for most types. Check `ALGORITHM=INSTANT` support.

### Index Creation

- **`ADD INDEX`**: Online in MySQL 5.6+ (`ALGORITHM=INPLACE, LOCK=NONE`). Allows reads and writes during index build.
- No equivalent of PostgreSQL's `CONCURRENTLY` keyword -- MySQL handles it via the online DDL algorithm.

### Column Type Changes

- Typically requires `ALGORITHM=COPY` -- full table rewrite with write lock.
- **For large tables**: Use `gh-ost` or `pt-online-schema-change` (pt-osc) to avoid locking.

### Column Rename

- **`ALTER TABLE RENAME COLUMN`** (MySQL 8.0+): `ALGORITHM=INPLACE, LOCK=NONE`. Instant.
- **MySQL 5.7**: Use `CHANGE COLUMN` (requires restating the column definition).

### gh-ost vs pt-online-schema-change

| Feature | gh-ost | pt-osc |
|---------|--------|--------|
| Trigger-based | No (uses binlog stream) | Yes (creates triggers on table) |
| Pausable | Yes (built-in throttle) | Limited |
| Replication-safe | Yes (monitors lag natively) | Yes (with `--max-lag`) |
| FK support | Limited (no FK to the altered table) | Better FK support |
| Recommended for | Most cases, especially large tables | Tables with FKs referencing them |

**General guidance**:
- Prefer `gh-ost` for most large-table DDL changes. It avoids triggers and gives better operational control.
- Use `pt-online-schema-change` when foreign keys reference the table being altered.
- Always test on a staging replica of production size before running in production.
- Monitor replication lag during the operation and configure throttle thresholds.

### MySQL Locking Summary

| Operation | Algorithm | Locks? | Notes |
|-----------|-----------|--------|-------|
| ADD COLUMN (nullable, 8.0.12+) | INSTANT | No | Metadata-only |
| ADD COLUMN (with default, < 8.0.12) | COPY | Yes (writes) | Full table rewrite |
| ADD INDEX | INPLACE | No | Online, concurrent reads/writes |
| CHANGE COLUMN TYPE | COPY | Yes (writes) | Use gh-ost/pt-osc for large tables |
| RENAME COLUMN (8.0+) | INPLACE | No | Instant |
| DROP COLUMN | INPLACE | Brief | Rebuilds clustered index |
