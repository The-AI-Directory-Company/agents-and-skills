-- integrity-check.sql
-- Parameterized data migration integrity checks.
-- Replace markers before execution:
--   {{OLD_TABLE}}      -- Source table name
--   {{NEW_TABLE}}      -- Target table name
--   {{OLD_COLUMN}}     -- Source column name
--   {{NEW_COLUMN}}     -- Target column name
--   {{JOIN_KEY}}       -- Primary key or join column (e.g., id)
--   {{SAMPLE_SIZE}}    -- Number of rows for spot-check (e.g., 1000)


-- =============================================================================
-- 1. Dual-Write Divergence Check
-- Run during Phase 1 (dual-write). Count must be zero before proceeding.
-- =============================================================================

SELECT COUNT(*) AS divergent_rows
FROM {{OLD_TABLE}} o
JOIN {{NEW_TABLE}} n ON o.{{JOIN_KEY}} = n.{{JOIN_KEY}}
WHERE o.{{OLD_COLUMN}} IS DISTINCT FROM n.{{NEW_COLUMN}};

-- MySQL equivalent (no IS DISTINCT FROM):
-- SELECT COUNT(*) AS divergent_rows
-- FROM {{OLD_TABLE}} o
-- JOIN {{NEW_TABLE}} n ON o.{{JOIN_KEY}} = n.{{JOIN_KEY}}
-- WHERE NOT (o.{{OLD_COLUMN}} <=> n.{{NEW_COLUMN}});


-- =============================================================================
-- 2. Backfill Row-Count Comparison
-- Run after Phase 2 (backfill). Counts must match.
-- =============================================================================

SELECT
  (SELECT COUNT(*) FROM {{OLD_TABLE}}) AS old_count,
  (SELECT COUNT(*) FROM {{NEW_TABLE}}) AS new_count,
  (SELECT COUNT(*) FROM {{OLD_TABLE}}) -
  (SELECT COUNT(*) FROM {{NEW_TABLE}}) AS difference;


-- =============================================================================
-- 3. Spot-Check Random Sample
-- Run after backfill. Verify value equality on a random sample.
-- =============================================================================

-- PostgreSQL:
SELECT
  o.{{JOIN_KEY}},
  o.{{OLD_COLUMN}} AS old_value,
  n.{{NEW_COLUMN}} AS new_value,
  CASE
    WHEN o.{{OLD_COLUMN}} IS DISTINCT FROM n.{{NEW_COLUMN}} THEN 'MISMATCH'
    ELSE 'OK'
  END AS status
FROM {{OLD_TABLE}} o
JOIN {{NEW_TABLE}} n ON o.{{JOIN_KEY}} = n.{{JOIN_KEY}}
ORDER BY RANDOM()
LIMIT {{SAMPLE_SIZE}};

-- MySQL equivalent:
-- SELECT
--   o.{{JOIN_KEY}},
--   o.{{OLD_COLUMN}} AS old_value,
--   n.{{NEW_COLUMN}} AS new_value,
--   CASE
--     WHEN NOT (o.{{OLD_COLUMN}} <=> n.{{NEW_COLUMN}}) THEN 'MISMATCH'
--     ELSE 'OK'
--   END AS status
-- FROM {{OLD_TABLE}} o
-- JOIN {{NEW_TABLE}} n ON o.{{JOIN_KEY}} = n.{{JOIN_KEY}}
-- ORDER BY RAND()
-- LIMIT {{SAMPLE_SIZE}};


-- =============================================================================
-- 4. Checksum Verification
-- Run after backfill for full-table integrity. Checksums must match.
-- =============================================================================

-- PostgreSQL (using md5 aggregate):
SELECT
  md5(string_agg(o.{{OLD_COLUMN}}::text, ',' ORDER BY o.{{JOIN_KEY}})) AS old_checksum
FROM {{OLD_TABLE}} o;

SELECT
  md5(string_agg(n.{{NEW_COLUMN}}::text, ',' ORDER BY n.{{JOIN_KEY}})) AS new_checksum
FROM {{NEW_TABLE}} n;

-- MySQL equivalent (using GROUP_CONCAT + MD5):
-- SELECT MD5(GROUP_CONCAT(o.{{OLD_COLUMN}} ORDER BY o.{{JOIN_KEY}} SEPARATOR ',')) AS old_checksum
-- FROM {{OLD_TABLE}} o;
--
-- SELECT MD5(GROUP_CONCAT(n.{{NEW_COLUMN}} ORDER BY n.{{JOIN_KEY}} SEPARATOR ',')) AS new_checksum
-- FROM {{NEW_TABLE}} n;

-- NOTE: For very large tables, GROUP_CONCAT/string_agg may exceed memory limits.
-- In that case, checksum in batches by range on {{JOIN_KEY}} and compare per-batch.


-- =============================================================================
-- 5. Orphan Detection
-- Find rows in the new table with no match in the old table (and vice versa).
-- =============================================================================

-- Rows in new but not in old:
SELECT n.{{JOIN_KEY}}
FROM {{NEW_TABLE}} n
LEFT JOIN {{OLD_TABLE}} o ON n.{{JOIN_KEY}} = o.{{JOIN_KEY}}
WHERE o.{{JOIN_KEY}} IS NULL
LIMIT 100;

-- Rows in old but not in new (missing from backfill):
SELECT o.{{JOIN_KEY}}
FROM {{OLD_TABLE}} o
LEFT JOIN {{NEW_TABLE}} n ON o.{{JOIN_KEY}} = n.{{JOIN_KEY}}
WHERE n.{{JOIN_KEY}} IS NULL
LIMIT 100;
