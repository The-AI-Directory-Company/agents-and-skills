#!/usr/bin/env bash
#
# pre-pr-check.sh
#
# Run this before opening a pull request. Checks:
#   1. Linting passes
#   2. Type checking passes
#   3. Tests pass
#   4. Branch is up to date with the base branch
#
# Usage:
#   ./scripts/pre-pr-check.sh
#   ./scripts/pre-pr-check.sh --base-branch develop
#
# Exit codes:
#   0 = All checks passed
#   1 = One or more checks failed

set -euo pipefail

# ── Configuration ─────────────────────────────────────────
# Override these with environment variables or flags

BASE_BRANCH="${BASE_BRANCH:-main}"
LINT_CMD="${LINT_CMD:-}"
TYPECHECK_CMD="${TYPECHECK_CMD:-}"
TEST_CMD="${TEST_CMD:-}"

# ── Parse arguments ───────────────────────────────────────

while [[ $# -gt 0 ]]; do
    case $1 in
        --base-branch)
            BASE_BRANCH="$2"
            shift 2
            ;;
        --help)
            echo "Usage: $0 [--base-branch <branch>]"
            echo ""
            echo "Runs lint, typecheck, test, and branch-freshness checks before a PR."
            echo ""
            echo "Options:"
            echo "  --base-branch <branch>  Base branch to check freshness against (default: main)"
            echo ""
            echo "Environment variables:"
            echo "  LINT_CMD       Override the lint command"
            echo "  TYPECHECK_CMD  Override the typecheck command"
            echo "  TEST_CMD       Override the test command"
            echo "  BASE_BRANCH    Override the base branch (same as --base-branch)"
            exit 0
            ;;
        *)
            echo "Unknown option: $1"
            echo "Run $0 --help for usage"
            exit 1
            ;;
    esac
done

# ── Helpers ───────────────────────────────────────────────

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BOLD='\033[1m'
RESET='\033[0m'

pass_count=0
fail_count=0
skip_count=0

run_check() {
    local name="$1"
    local cmd="$2"

    if [[ -z "$cmd" ]]; then
        printf "${YELLOW}SKIP${RESET}  %s (no command configured)\n" "$name"
        ((skip_count++))
        return 0
    fi

    printf "${BOLD}RUN${RESET}   %s: %s\n" "$name" "$cmd"

    if eval "$cmd"; then
        printf "${GREEN}PASS${RESET}  %s\n\n" "$name"
        ((pass_count++))
    else
        printf "${RED}FAIL${RESET}  %s\n\n" "$name"
        ((fail_count++))
    fi
}

# ── Auto-detect commands ──────────────────────────────────

detect_commands() {
    # Lint
    if [[ -z "$LINT_CMD" ]]; then
        if [[ -f "pyproject.toml" ]] && command -v ruff &>/dev/null; then
            LINT_CMD="ruff check ."
        elif [[ -f "package.json" ]] && grep -q '"lint"' package.json 2>/dev/null; then
            LINT_CMD="npm run lint"
        elif [[ -f "Cargo.toml" ]] && command -v cargo &>/dev/null; then
            LINT_CMD="cargo clippy -- -D warnings"
        elif [[ -f "Makefile" ]] && grep -q '^lint:' Makefile 2>/dev/null; then
            LINT_CMD="make lint"
        fi
    fi

    # Typecheck
    if [[ -z "$TYPECHECK_CMD" ]]; then
        if [[ -f "pyproject.toml" ]] && command -v mypy &>/dev/null; then
            TYPECHECK_CMD="mypy src/"
        elif [[ -f "tsconfig.json" ]] && command -v tsc &>/dev/null; then
            TYPECHECK_CMD="tsc --noEmit"
        elif [[ -f "package.json" ]] && grep -q '"typecheck"' package.json 2>/dev/null; then
            TYPECHECK_CMD="npm run typecheck"
        fi
    fi

    # Test
    if [[ -z "$TEST_CMD" ]]; then
        if [[ -f "pyproject.toml" ]] && command -v pytest &>/dev/null; then
            TEST_CMD="pytest"
        elif [[ -f "package.json" ]] && grep -q '"test"' package.json 2>/dev/null; then
            TEST_CMD="npm test"
        elif [[ -f "Cargo.toml" ]] && command -v cargo &>/dev/null; then
            TEST_CMD="cargo test"
        elif [[ -f "Makefile" ]] && grep -q '^test:' Makefile 2>/dev/null; then
            TEST_CMD="make test"
        fi
    fi
}

# ── Branch freshness check ────────────────────────────────

check_branch_freshness() {
    local name="Branch freshness"

    # Verify we are in a git repo
    if ! git rev-parse --is-inside-work-tree &>/dev/null; then
        printf "${YELLOW}SKIP${RESET}  %s (not a git repository)\n" "$name"
        ((skip_count++))
        return 0
    fi

    local current_branch
    current_branch=$(git branch --show-current 2>/dev/null || echo "")

    if [[ -z "$current_branch" ]]; then
        printf "${YELLOW}SKIP${RESET}  %s (detached HEAD)\n" "$name"
        ((skip_count++))
        return 0
    fi

    if [[ "$current_branch" == "$BASE_BRANCH" ]]; then
        printf "${YELLOW}SKIP${RESET}  %s (already on %s)\n" "$name" "$BASE_BRANCH"
        ((skip_count++))
        return 0
    fi

    printf "${BOLD}RUN${RESET}   %s: checking if %s is up to date with %s\n" "$name" "$current_branch" "$BASE_BRANCH"

    # Fetch latest from remote (suppress output)
    git fetch origin "$BASE_BRANCH" --quiet 2>/dev/null || true

    local behind
    behind=$(git rev-list --count "HEAD..origin/$BASE_BRANCH" 2>/dev/null || echo "unknown")

    if [[ "$behind" == "unknown" ]]; then
        printf "${YELLOW}SKIP${RESET}  %s (could not determine; remote '%s' may not exist)\n" "$name" "$BASE_BRANCH"
        ((skip_count++))
    elif [[ "$behind" -eq 0 ]]; then
        printf "${GREEN}PASS${RESET}  %s (up to date with origin/%s)\n\n" "$name" "$BASE_BRANCH"
        ((pass_count++))
    else
        printf "${RED}FAIL${RESET}  %s (%s is %d commit(s) behind origin/%s)\n" "$name" "$current_branch" "$behind" "$BASE_BRANCH"
        printf "       Run: git rebase origin/%s\n\n" "$BASE_BRANCH"
        ((fail_count++))
    fi
}

# ── Uncommitted changes check ─────────────────────────────

check_uncommitted_changes() {
    local name="Uncommitted changes"

    if ! git rev-parse --is-inside-work-tree &>/dev/null; then
        return 0
    fi

    printf "${BOLD}RUN${RESET}   %s\n" "$name"

    if git diff --quiet && git diff --cached --quiet; then
        printf "${GREEN}PASS${RESET}  %s (working tree clean)\n\n" "$name"
        ((pass_count++))
    else
        printf "${YELLOW}WARN${RESET}  %s (you have uncommitted changes)\n\n" "$name"
        # This is a warning, not a failure
    fi
}

# ── Main ──────────────────────────────────────────────────

echo ""
printf "${BOLD}Pre-PR Check${RESET}\n"
echo "════════════════════════════════════════════════════"
echo ""

detect_commands

check_uncommitted_changes
run_check "Lint" "$LINT_CMD"
run_check "Type check" "$TYPECHECK_CMD"
run_check "Tests" "$TEST_CMD"
check_branch_freshness

# ── Summary ───────────────────────────────────────────────

echo "════════════════════════════════════════════════════"
printf "${BOLD}Summary:${RESET} "
printf "${GREEN}%d passed${RESET}, " "$pass_count"
printf "${RED}%d failed${RESET}, " "$fail_count"
printf "${YELLOW}%d skipped${RESET}\n" "$skip_count"
echo ""

if [[ "$fail_count" -gt 0 ]]; then
    printf "${RED}${BOLD}Fix the failures above before opening a PR.${RESET}\n"
    exit 1
else
    printf "${GREEN}${BOLD}All checks passed. Ready to open a PR.${RESET}\n"
    exit 0
fi
