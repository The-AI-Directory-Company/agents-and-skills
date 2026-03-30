-- =============================================================================
-- Migration: YYYYMMDD_NNN_description_of_change
-- =============================================================================
--
-- Author:      [Name]
-- Created:     [Date]
-- Table(s):    [Affected tables]
-- Risk:        [Low / Medium / High]
-- Estimated execution time: [Duration on production-scale data]
--
-- Description:
--   [What this migration does and why. 1-3 sentences.]
--
-- Pre-conditions:
--   - [ ] Tested on production-scale replica
--   - [ ] DOWN script tested and verified
--   - [ ] Dependent services identified and notified
--   - [ ] Backup verified within last 24 hours
--
-- =============================================================================


-- ---------------------
-- UP Migration
-- ---------------------

-- TODO: Add your forward migration SQL here.
--
-- Guidelines:
--   - One logical change per migration file
--   - Use IF NOT EXISTS / IF EXISTS guards where supported
--   - For large tables, note expected lock duration
--   - Add comments explaining non-obvious decisions


-- Example: Add a nullable column (low risk, metadata-only in PG 11+)
-- ALTER TABLE orders ADD COLUMN IF NOT EXISTS status VARCHAR(32) NULL;

-- Example: Add an index concurrently (PostgreSQL only, cannot run in transaction)
-- CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_orders_status ON orders (status);

-- Example: Add a column with default (check engine-specific behavior)
-- ALTER TABLE orders ADD COLUMN priority INTEGER NOT NULL DEFAULT 0;


-- ---------------------
-- DOWN Migration
-- ---------------------

-- TODO: Add your rollback SQL here.
--
-- Guidelines:
--   - Must produce the exact prior schema state
--   - Test by running UP then DOWN then UP again
--   - Document any data loss (e.g., dropping a column loses its data)
--   - If rollback is destructive, note what is lost


-- Example: Drop the column added above
-- ALTER TABLE orders DROP COLUMN IF EXISTS status;

-- Example: Drop the index added above
-- DROP INDEX IF EXISTS idx_orders_status;


-- =============================================================================
-- Naming Convention
-- =============================================================================
--
-- Format: YYYYMMDD_NNN_verb_object
--
-- Examples:
--   20240115_001_add_status_to_orders
--   20240115_002_create_index_orders_status
--   20240120_001_drop_legacy_email_column
--   20240201_001_rename_user_name_to_display_name
--   20240201_002_change_amount_type_to_bigint
--
-- Rules:
--   - Date is the date the migration was authored
--   - NNN is a sequential number within the same date (001, 002, ...)
--   - Use lowercase with underscores
--   - Verb should describe the action: add, drop, rename, change, create, split
-- =============================================================================
