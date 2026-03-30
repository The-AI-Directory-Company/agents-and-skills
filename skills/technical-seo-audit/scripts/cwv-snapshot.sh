#!/usr/bin/env bash
#
# cwv-snapshot.sh — Core Web Vitals snapshot via PageSpeed Insights API
#
# Usage:
#   ./cwv-snapshot.sh <URL> [API_KEY]
#
# If API_KEY is omitted, the script uses the PAGESPEED_API_KEY environment variable.
# Without an API key, the script still works but is subject to stricter rate limits.
#
# Output:
#   Prints a summary table of CWV metrics (field + lab data) for the given URL.
#
# Requirements:
#   - curl
#   - jq (https://jqlang.github.io/jq/)
#
# Examples:
#   ./cwv-snapshot.sh https://example.com
#   ./cwv-snapshot.sh https://example.com AIzaSy...
#   PAGESPEED_API_KEY=AIzaSy... ./cwv-snapshot.sh https://example.com

set -euo pipefail

# --- Arguments ---
URL="${1:-}"
API_KEY="${2:-${PAGESPEED_API_KEY:-}}"

if [[ -z "$URL" ]]; then
  echo "Usage: $0 <URL> [API_KEY]"
  echo ""
  echo "Fetches Core Web Vitals data from PageSpeed Insights API."
  echo ""
  echo "Options:"
  echo "  URL       The page URL to analyze (required)"
  echo "  API_KEY   Google PageSpeed Insights API key (optional, or set PAGESPEED_API_KEY)"
  exit 1
fi

# --- Dependency check ---
for cmd in curl jq; do
  if ! command -v "$cmd" &>/dev/null; then
    echo "Error: '$cmd' is required but not installed."
    exit 1
  fi
done

# --- Build API URL ---
API_BASE="https://www.googleapis.com/pagespeedonline/v5/runPagespeed"
PARAMS="url=$(jq -rn --arg u "$URL" '$u | @uri')&strategy=mobile&category=performance"

if [[ -n "$API_KEY" ]]; then
  PARAMS="${PARAMS}&key=${API_KEY}"
fi

API_URL="${API_BASE}?${PARAMS}"

echo "Fetching CWV data for: $URL"
echo "Strategy: mobile"
echo "---"

# --- Fetch data ---
RESPONSE=$(curl -s -f "$API_URL") || {
  echo "Error: API request failed. Check the URL and API key."
  exit 1
}

# --- Extract field data (CrUX) ---
echo ""
echo "=== FIELD DATA (Chrome UX Report — real users, 75th percentile) ==="
echo ""

FIELD_LCP=$(echo "$RESPONSE" | jq -r '.loadingExperience.metrics.LARGEST_CONTENTFUL_PAINT_MS.percentile // "N/A"')
FIELD_INP=$(echo "$RESPONSE" | jq -r '.loadingExperience.metrics.INTERACTION_TO_NEXT_PAINT.percentile // "N/A"')
FIELD_CLS=$(echo "$RESPONSE" | jq -r '.loadingExperience.metrics.CUMULATIVE_LAYOUT_SHIFT_SCORE.percentile // "N/A"')

FIELD_LCP_CAT=$(echo "$RESPONSE" | jq -r '.loadingExperience.metrics.LARGEST_CONTENTFUL_PAINT_MS.category // "N/A"')
FIELD_INP_CAT=$(echo "$RESPONSE" | jq -r '.loadingExperience.metrics.INTERACTION_TO_NEXT_PAINT.category // "N/A"')
FIELD_CLS_CAT=$(echo "$RESPONSE" | jq -r '.loadingExperience.metrics.CUMULATIVE_LAYOUT_SHIFT_SCORE.category // "N/A"')

OVERALL_CAT=$(echo "$RESPONSE" | jq -r '.loadingExperience.overall_category // "N/A"')

# Format values
if [[ "$FIELD_LCP" != "N/A" ]]; then
  FIELD_LCP_FMT=$(echo "scale=1; $FIELD_LCP / 1000" | bc)s
else
  FIELD_LCP_FMT="N/A"
fi

if [[ "$FIELD_INP" != "N/A" ]]; then
  FIELD_INP_FMT="${FIELD_INP}ms"
else
  FIELD_INP_FMT="N/A"
fi

if [[ "$FIELD_CLS" != "N/A" ]]; then
  FIELD_CLS_FMT=$(echo "scale=2; $FIELD_CLS / 100" | bc)
else
  FIELD_CLS_FMT="N/A"
fi

printf "%-8s %-12s %-20s %-10s\n" "Metric" "Value" "Rating" "Threshold"
printf "%-8s %-12s %-20s %-10s\n" "------" "-----" "------" "---------"
printf "%-8s %-12s %-20s %-10s\n" "LCP" "$FIELD_LCP_FMT" "$FIELD_LCP_CAT" "<= 2.5s"
printf "%-8s %-12s %-20s %-10s\n" "INP" "$FIELD_INP_FMT" "$FIELD_INP_CAT" "<= 200ms"
printf "%-8s %-12s %-20s %-10s\n" "CLS" "$FIELD_CLS_FMT" "$FIELD_CLS_CAT" "<= 0.1"
echo ""
echo "Overall: $OVERALL_CAT"

if [[ "$FIELD_LCP" == "N/A" && "$FIELD_INP" == "N/A" && "$FIELD_CLS" == "N/A" ]]; then
  echo ""
  echo "Note: No field data available. This URL may not have enough traffic for CrUX data."
  echo "Lab data below is the only available measurement."
fi

# --- Extract lab data (Lighthouse) ---
echo ""
echo "=== LAB DATA (Lighthouse — simulated, single run) ==="
echo ""

PERF_SCORE=$(echo "$RESPONSE" | jq -r '.lighthouseResult.categories.performance.score // "N/A"')
if [[ "$PERF_SCORE" != "N/A" ]]; then
  PERF_SCORE_FMT=$(echo "scale=0; $PERF_SCORE * 100 / 1" | bc)
else
  PERF_SCORE_FMT="N/A"
fi

LAB_LCP=$(echo "$RESPONSE" | jq -r '.lighthouseResult.audits["largest-contentful-paint"].displayValue // "N/A"')
LAB_INP=$(echo "$RESPONSE" | jq -r '.lighthouseResult.audits["interaction-to-next-paint"].displayValue // "N/A"')
LAB_CLS=$(echo "$RESPONSE" | jq -r '.lighthouseResult.audits["cumulative-layout-shift"].displayValue // "N/A"')
LAB_FCP=$(echo "$RESPONSE" | jq -r '.lighthouseResult.audits["first-contentful-paint"].displayValue // "N/A"')
LAB_TBT=$(echo "$RESPONSE" | jq -r '.lighthouseResult.audits["total-blocking-time"].displayValue // "N/A"')
LAB_SI=$(echo "$RESPONSE" | jq -r '.lighthouseResult.audits["speed-index"].displayValue // "N/A"')

printf "%-8s %-15s\n" "Metric" "Value"
printf "%-8s %-15s\n" "------" "-----"
printf "%-8s %-15s\n" "Score" "$PERF_SCORE_FMT / 100"
printf "%-8s %-15s\n" "FCP" "$LAB_FCP"
printf "%-8s %-15s\n" "LCP" "$LAB_LCP"
printf "%-8s %-15s\n" "TBT" "$LAB_TBT"
printf "%-8s %-15s\n" "CLS" "$LAB_CLS"
printf "%-8s %-15s\n" "SI" "$LAB_SI"

# --- LCP element ---
echo ""
echo "=== LCP ELEMENT ==="
echo ""
LCP_ELEMENT=$(echo "$RESPONSE" | jq -r '.lighthouseResult.audits["largest-contentful-paint-element"].details.items[0].node.snippet // "N/A"')
echo "$LCP_ELEMENT"

# --- Top opportunities ---
echo ""
echo "=== TOP OPPORTUNITIES (estimated savings) ==="
echo ""

echo "$RESPONSE" | jq -r '
  .lighthouseResult.audits
  | to_entries
  | map(select(.value.details.type? == "opportunity" and (.value.details.overallSavingsMs? // 0) > 0))
  | sort_by(-.value.details.overallSavingsMs)
  | .[:5]
  | .[]
  | "\(.value.title): \(.value.details.overallSavingsMs)ms"
' 2>/dev/null || echo "No opportunities found."

echo ""
echo "---"
echo "Data fetched: $(date -u '+%Y-%m-%d %H:%M UTC')"
echo "API docs: https://developers.google.com/speed/docs/insights/v5/get-started"
