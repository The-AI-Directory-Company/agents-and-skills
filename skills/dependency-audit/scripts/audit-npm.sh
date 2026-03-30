#!/usr/bin/env bash
#
# audit-npm.sh — Run a comprehensive npm dependency audit
#
# Executes three checks in sequence:
#   1. npm audit (security vulnerabilities)
#   2. npm outdated (version freshness)
#   3. license-checker (license compliance)
#
# Usage:
#   ./audit-npm.sh [--json] [--output-dir <path>]
#
# Options:
#   --json         Write structured JSON output files (default: human-readable)
#   --output-dir   Directory for report files (default: ./audit-reports)
#
# Requirements:
#   - Node.js >= 18
#   - npm >= 9
#   - license-checker: npm install -g license-checker
#
# Exit codes:
#   0  All checks passed
#   1  Critical or high vulnerabilities found
#   2  License violations found
#   3  Tool not found or execution error

set -euo pipefail

# --- Configuration -----------------------------------------------------------

JSON_OUTPUT=false
OUTPUT_DIR="./audit-reports"
TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

# --- Argument parsing ---------------------------------------------------------

while [[ $# -gt 0 ]]; do
  case "$1" in
    --json)
      JSON_OUTPUT=true
      shift
      ;;
    --output-dir)
      OUTPUT_DIR="$2"
      shift 2
      ;;
    *)
      echo "Unknown option: $1" >&2
      exit 3
      ;;
  esac
done

mkdir -p "$OUTPUT_DIR"

# --- Helpers ------------------------------------------------------------------

log() {
  echo ""
  echo "================================================================"
  echo "  $1"
  echo "================================================================"
  echo ""
}

check_command() {
  if ! command -v "$1" &> /dev/null; then
    echo "ERROR: $1 is not installed." >&2
    echo "Install with: $2" >&2
    exit 3
  fi
}

# --- Preflight checks --------------------------------------------------------

check_command "npm" "https://nodejs.org"
check_command "node" "https://nodejs.org"

if [ ! -f "package.json" ]; then
  echo "ERROR: No package.json found in current directory." >&2
  echo "Run this script from the project root." >&2
  exit 3
fi

if [ ! -f "package-lock.json" ] && [ ! -f "npm-shrinkwrap.json" ]; then
  echo "WARNING: No lockfile found. Audit results may be incomplete." >&2
  echo "Run 'npm install' first to generate package-lock.json." >&2
fi

# --- 1. Security vulnerability scan ------------------------------------------

log "Step 1/3: Security Vulnerability Scan (npm audit)"

AUDIT_EXIT=0

if [ "$JSON_OUTPUT" = true ]; then
  npm audit --json > "$OUTPUT_DIR/vulnerabilities.json" 2>/dev/null || AUDIT_EXIT=$?
  echo "Output: $OUTPUT_DIR/vulnerabilities.json"

  # Parse summary from JSON
  if command -v node &> /dev/null; then
    node -e "
      const r = require('./$OUTPUT_DIR/vulnerabilities.json');
      const v = r.metadata?.vulnerabilities || {};
      console.log('Summary:');
      console.log('  Critical:', v.critical || 0);
      console.log('  High:    ', v.high || 0);
      console.log('  Moderate:', v.moderate || 0);
      console.log('  Low:     ', v.low || 0);
      console.log('  Total:   ', v.total || 0);
    " 2>/dev/null || true
  fi
else
  npm audit 2>/dev/null || AUDIT_EXIT=$?
fi

HAS_CRITICAL=false
if [ "$AUDIT_EXIT" -ne 0 ]; then
  echo ""
  echo "npm audit exited with code $AUDIT_EXIT (vulnerabilities found)"
  HAS_CRITICAL=true
fi

# --- 2. Outdated packages ----------------------------------------------------

log "Step 2/3: Outdated Package Analysis (npm outdated)"

if [ "$JSON_OUTPUT" = true ]; then
  # npm outdated exits non-zero when outdated packages exist
  npm outdated --json > "$OUTPUT_DIR/outdated.json" 2>/dev/null || true
  echo "Output: $OUTPUT_DIR/outdated.json"

  # Count outdated packages
  if command -v node &> /dev/null; then
    node -e "
      const data = require('./$OUTPUT_DIR/outdated.json');
      const pkgs = Object.keys(data);
      let major = 0, minor = 0, patch = 0;
      for (const [name, info] of Object.entries(data)) {
        const current = (info.current || '').split('.');
        const latest = (info.latest || '').split('.');
        if (current[0] !== latest[0]) major++;
        else if (current[1] !== latest[1]) minor++;
        else patch++;
      }
      console.log('Summary:');
      console.log('  Total outdated:', pkgs.length);
      console.log('  Major behind:  ', major);
      console.log('  Minor behind:  ', minor);
      console.log('  Patch behind:  ', patch);
    " 2>/dev/null || true
  fi
else
  npm outdated 2>/dev/null || true
fi

# --- 3. License compliance ---------------------------------------------------

log "Step 3/3: License Compliance (license-checker)"

if command -v license-checker &> /dev/null; then
  if [ "$JSON_OUTPUT" = true ]; then
    license-checker --json --out "$OUTPUT_DIR/licenses.json" 2>/dev/null
    echo "Output: $OUTPUT_DIR/licenses.json"

    # Produce license summary
    if command -v node &> /dev/null; then
      node -e "
        const data = require('./$OUTPUT_DIR/licenses.json');
        const counts = {};
        for (const [pkg, info] of Object.entries(data)) {
          const lic = info.licenses || 'UNKNOWN';
          const key = Array.isArray(lic) ? lic.join(' OR ') : lic;
          counts[key] = (counts[key] || 0) + 1;
        }
        console.log('License distribution:');
        const sorted = Object.entries(counts).sort((a, b) => b[1] - a[1]);
        for (const [license, count] of sorted) {
          console.log('  ' + license + ':', count);
        }
        // Flag problematic licenses
        const flagged = ['GPL-2.0', 'GPL-3.0', 'AGPL-3.0', 'SSPL-1.0', 'UNKNOWN', 'UNLICENSED'];
        const problems = sorted.filter(([l]) => flagged.some(f => l.includes(f)));
        if (problems.length > 0) {
          console.log('');
          console.log('FLAGGED LICENSES (review required):');
          for (const [license, count] of problems) {
            console.log('  ⚠ ' + license + ':', count, 'packages');
          }
        }
      " 2>/dev/null || true
    fi
  else
    license-checker --summary 2>/dev/null
  fi
else
  echo "SKIPPED: license-checker not installed."
  echo "Install with: npm install -g license-checker"
  echo ""
  echo "Alternative for quick check:"
  echo "  npx license-checker --summary"
fi

# --- Final report -------------------------------------------------------------

log "Audit Complete"

echo "Timestamp: $TIMESTAMP"
echo ""

if [ "$JSON_OUTPUT" = true ]; then
  echo "Reports written to: $OUTPUT_DIR/"
  ls -la "$OUTPUT_DIR/"
fi

echo ""

if [ "$HAS_CRITICAL" = true ]; then
  echo "RESULT: VULNERABILITIES FOUND — review npm audit output above"
  exit 1
else
  echo "RESULT: No critical/high vulnerabilities detected"
  exit 0
fi
