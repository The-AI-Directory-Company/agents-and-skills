#!/usr/bin/env bash
#
# pre-release-check.sh
# Validates pre-release readiness: CI status, feature flags, health endpoints.
#
# Usage:
#   ./pre-release-check.sh \
#     --repo "org/repo" \
#     --branch "release/v2.4.0" \
#     --health-urls "https://api.example.com/health,https://auth.example.com/health" \
#     --flag-api "https://flags.example.com/api/v1/flags" \
#     --flag-token "$FLAG_API_TOKEN" \
#     --required-flags "enable-new-checkout,enable-payment-v2"
#
# Exit codes:
#   0 = all checks passed
#   1 = one or more checks failed

set -euo pipefail

# --- Defaults ---
REPO=""
BRANCH=""
HEALTH_URLS=""
FLAG_API=""
FLAG_TOKEN=""
REQUIRED_FLAGS=""
PASSED=0
FAILED=0

# --- Parse arguments ---
while [[ $# -gt 0 ]]; do
  case "$1" in
    --repo)       REPO="$2"; shift 2 ;;
    --branch)     BRANCH="$2"; shift 2 ;;
    --health-urls) HEALTH_URLS="$2"; shift 2 ;;
    --flag-api)   FLAG_API="$2"; shift 2 ;;
    --flag-token) FLAG_TOKEN="$2"; shift 2 ;;
    --required-flags) REQUIRED_FLAGS="$2"; shift 2 ;;
    *) echo "Unknown argument: $1"; exit 1 ;;
  esac
done

# --- Helpers ---
pass() { PASSED=$((PASSED + 1)); echo "  PASS: $1"; }
fail() { FAILED=$((FAILED + 1)); echo "  FAIL: $1"; }
section() { echo ""; echo "=== $1 ==="; }

# --- Check 1: CI status on release branch ---
section "CI Status"

if [[ -z "$REPO" || -z "$BRANCH" ]]; then
  fail "Missing --repo or --branch. Cannot check CI status."
else
  if command -v gh &>/dev/null; then
    CI_STATUS=$(gh api "repos/${REPO}/commits/${BRANCH}/status" --jq '.state' 2>/dev/null || echo "error")
    case "$CI_STATUS" in
      success) pass "CI status for ${BRANCH}: success" ;;
      pending) fail "CI status for ${BRANCH}: pending (not yet green)" ;;
      failure) fail "CI status for ${BRANCH}: failure" ;;
      error)   fail "CI status for ${BRANCH}: could not retrieve (check repo/branch name)" ;;
      *)       fail "CI status for ${BRANCH}: unexpected state '${CI_STATUS}'" ;;
    esac
  else
    fail "GitHub CLI (gh) not installed. Cannot check CI status."
  fi
fi

# --- Check 2: Feature flag readiness ---
section "Feature Flags"

if [[ -z "$FLAG_API" || -z "$REQUIRED_FLAGS" ]]; then
  echo "  SKIP: No --flag-api or --required-flags provided."
else
  IFS=',' read -ra FLAGS <<< "$REQUIRED_FLAGS"
  for flag in "${FLAGS[@]}"; do
    flag=$(echo "$flag" | xargs)  # trim whitespace
    RESPONSE=$(curl -sf -H "Authorization: Bearer ${FLAG_TOKEN}" "${FLAG_API}/${flag}" 2>/dev/null || echo "error")
    if [[ "$RESPONSE" == "error" ]]; then
      fail "Flag '${flag}': could not retrieve (check API URL and token)"
    elif echo "$RESPONSE" | grep -qi '"enabled"\s*:\s*true'; then
      pass "Flag '${flag}': enabled"
    else
      fail "Flag '${flag}': not enabled in target environment"
    fi
  done
fi

# --- Check 3: Health endpoints ---
section "Health Endpoints"

if [[ -z "$HEALTH_URLS" ]]; then
  echo "  SKIP: No --health-urls provided."
else
  IFS=',' read -ra URLS <<< "$HEALTH_URLS"
  for url in "${URLS[@]}"; do
    url=$(echo "$url" | xargs)  # trim whitespace
    HTTP_CODE=$(curl -so /dev/null -w "%{http_code}" --max-time 10 "$url" 2>/dev/null || echo "000")
    if [[ "$HTTP_CODE" == "200" ]]; then
      pass "${url} -> HTTP ${HTTP_CODE}"
    else
      fail "${url} -> HTTP ${HTTP_CODE}"
    fi
  done
fi

# --- Summary ---
section "Summary"
echo "  Passed: ${PASSED}"
echo "  Failed: ${FAILED}"
echo ""

if [[ "$FAILED" -gt 0 ]]; then
  echo "RESULT: NO-GO -- ${FAILED} check(s) failed. Resolve before proceeding."
  exit 1
else
  echo "RESULT: GO -- All checks passed."
  exit 0
fi
