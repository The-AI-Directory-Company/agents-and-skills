#!/usr/bin/env bash
#
# failover-validation-checklist.sh
# Post-failover data validation checks.
# Run after completing a failover to verify the recovery environment is healthy.
#
# Usage:
#   ./failover-validation-checklist.sh \
#     --health-urls "https://api.example.com/health,https://auth.example.com/health" \
#     --db-host "replica-db.example.com" \
#     --db-port 5432 \
#     --db-name "appdb" \
#     --db-user "readonly_user" \
#     --expected-table "users" \
#     --min-row-count 1000
#
# Environment variables:
#   PGPASSWORD  — PostgreSQL password (or use .pgpass)
#
# Exit codes:
#   0 = all checks passed
#   1 = one or more checks failed

set -euo pipefail

# --- Defaults ---
HEALTH_URLS=""
DB_HOST=""
DB_PORT="5432"
DB_NAME=""
DB_USER=""
EXPECTED_TABLE=""
MIN_ROW_COUNT=0
PASSED=0
FAILED=0

# --- Parse arguments ---
while [[ $# -gt 0 ]]; do
  case "$1" in
    --health-urls)    HEALTH_URLS="$2"; shift 2 ;;
    --db-host)        DB_HOST="$2"; shift 2 ;;
    --db-port)        DB_PORT="$2"; shift 2 ;;
    --db-name)        DB_NAME="$2"; shift 2 ;;
    --db-user)        DB_USER="$2"; shift 2 ;;
    --expected-table) EXPECTED_TABLE="$2"; shift 2 ;;
    --min-row-count)  MIN_ROW_COUNT="$2"; shift 2 ;;
    *) echo "Unknown argument: $1"; exit 1 ;;
  esac
done

# --- Helpers ---
pass() { PASSED=$((PASSED + 1)); echo "  PASS: $1"; }
fail() { FAILED=$((FAILED + 1)); echo "  FAIL: $1"; }
section() { echo ""; echo "=== $1 ==="; }

# =========================================================================
# Check 1: Health endpoint verification
# =========================================================================
section "Health Endpoints"

if [[ -z "$HEALTH_URLS" ]]; then
  echo "  SKIP: No --health-urls provided."
else
  IFS=',' read -ra URLS <<< "$HEALTH_URLS"
  for url in "${URLS[@]}"; do
    url=$(echo "$url" | xargs)
    HTTP_CODE=$(curl -so /dev/null -w "%{http_code}" --max-time 10 "$url" 2>/dev/null || echo "000")
    if [[ "$HTTP_CODE" == "200" ]]; then
      pass "${url} -> HTTP ${HTTP_CODE}"
    else
      fail "${url} -> HTTP ${HTTP_CODE} (expected 200)"
    fi
  done
fi

# =========================================================================
# Check 2: Database connectivity
# =========================================================================
section "Database Connectivity"

if [[ -z "$DB_HOST" || -z "$DB_NAME" || -z "$DB_USER" ]]; then
  echo "  SKIP: No --db-host, --db-name, or --db-user provided."
else
  if command -v psql &>/dev/null; then
    DB_RESULT=$(psql -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -d "$DB_NAME" -t -c "SELECT 1;" 2>/dev/null || echo "error")
    DB_RESULT=$(echo "$DB_RESULT" | xargs)
    if [[ "$DB_RESULT" == "1" ]]; then
      pass "Database connection to ${DB_HOST}:${DB_PORT}/${DB_NAME}"
    else
      fail "Database connection to ${DB_HOST}:${DB_PORT}/${DB_NAME} (got: ${DB_RESULT})"
    fi
  else
    fail "psql not installed. Cannot check database connectivity."
  fi
fi

# =========================================================================
# Check 3: Row count validation
# =========================================================================
section "Data Row Count"

if [[ -z "$DB_HOST" || -z "$EXPECTED_TABLE" ]]; then
  echo "  SKIP: No --db-host or --expected-table provided."
else
  if command -v psql &>/dev/null; then
    ROW_COUNT=$(psql -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -d "$DB_NAME" -t -c "SELECT COUNT(*) FROM ${EXPECTED_TABLE};" 2>/dev/null || echo "error")
    ROW_COUNT=$(echo "$ROW_COUNT" | xargs)
    if [[ "$ROW_COUNT" == "error" ]]; then
      fail "Could not query row count for table ${EXPECTED_TABLE}"
    elif [[ "$ROW_COUNT" -ge "$MIN_ROW_COUNT" ]]; then
      pass "Table ${EXPECTED_TABLE}: ${ROW_COUNT} rows (minimum: ${MIN_ROW_COUNT})"
    else
      fail "Table ${EXPECTED_TABLE}: ${ROW_COUNT} rows (expected >= ${MIN_ROW_COUNT})"
    fi
  fi
fi

# =========================================================================
# Check 4: Replication lag (if applicable)
# =========================================================================
section "Replication Status"

if [[ -z "$DB_HOST" ]]; then
  echo "  SKIP: No --db-host provided."
else
  if command -v psql &>/dev/null; then
    # PostgreSQL: check if this is a replica and its lag
    IS_RECOVERY=$(psql -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -d "$DB_NAME" -t -c "SELECT pg_is_in_recovery();" 2>/dev/null || echo "error")
    IS_RECOVERY=$(echo "$IS_RECOVERY" | xargs)

    if [[ "$IS_RECOVERY" == "t" ]]; then
      LAG=$(psql -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -d "$DB_NAME" -t -c \
        "SELECT COALESCE(EXTRACT(EPOCH FROM (now() - pg_last_xact_replay_timestamp()))::int::text, 'unknown');" 2>/dev/null || echo "error")
      LAG=$(echo "$LAG" | xargs)
      if [[ "$LAG" == "error" || "$LAG" == "unknown" ]]; then
        fail "Could not determine replication lag"
      elif [[ "$LAG" -le 5 ]]; then
        pass "Replication lag: ${LAG}s (acceptable: <= 5s)"
      else
        fail "Replication lag: ${LAG}s (exceeds 5s threshold)"
      fi
    elif [[ "$IS_RECOVERY" == "f" ]]; then
      pass "Database is primary (not a replica) -- no lag check needed"
    else
      echo "  SKIP: Could not determine recovery status."
    fi
  fi
fi

# =========================================================================
# Check 5: Recent data freshness
# =========================================================================
section "Data Freshness"

if [[ -z "$DB_HOST" || -z "$EXPECTED_TABLE" ]]; then
  echo "  SKIP: No --db-host or --expected-table provided."
else
  if command -v psql &>/dev/null; then
    # Check if the table has an updated_at or created_at column with recent data
    HAS_TIMESTAMP=$(psql -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -d "$DB_NAME" -t -c \
      "SELECT column_name FROM information_schema.columns
       WHERE table_name = '${EXPECTED_TABLE}'
         AND column_name IN ('updated_at', 'created_at')
       ORDER BY column_name DESC LIMIT 1;" 2>/dev/null || echo "")
    HAS_TIMESTAMP=$(echo "$HAS_TIMESTAMP" | xargs)

    if [[ -n "$HAS_TIMESTAMP" ]]; then
      LATEST=$(psql -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -d "$DB_NAME" -t -c \
        "SELECT MAX(${HAS_TIMESTAMP}) FROM ${EXPECTED_TABLE};" 2>/dev/null || echo "error")
      LATEST=$(echo "$LATEST" | xargs)
      if [[ "$LATEST" == "error" || -z "$LATEST" ]]; then
        fail "Could not determine latest ${HAS_TIMESTAMP} in ${EXPECTED_TABLE}"
      else
        echo "  INFO: Latest ${HAS_TIMESTAMP} in ${EXPECTED_TABLE}: ${LATEST}"
        echo "        Verify this timestamp is recent enough given your RPO."
      fi
    else
      echo "  SKIP: No updated_at/created_at column found in ${EXPECTED_TABLE}."
    fi
  fi
fi

# =========================================================================
# Summary
# =========================================================================
section "Summary"
echo "  Passed: ${PASSED}"
echo "  Failed: ${FAILED}"
echo ""

if [[ "$FAILED" -gt 0 ]]; then
  echo "RESULT: FAILOVER VALIDATION FAILED -- ${FAILED} check(s) need attention."
  echo "Review failures above before routing production traffic to the recovery environment."
  exit 1
else
  echo "RESULT: FAILOVER VALIDATION PASSED -- All checks healthy."
  exit 0
fi
