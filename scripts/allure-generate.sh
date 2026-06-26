#!/usr/bin/env bash
# Generates a self-contained HTML Allure report in reports/html.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
RESULTS="$ROOT/reports/allure-results"
OUTPUT="$ROOT/reports/html"

if [[ ! -d "$RESULTS" ]]; then
  echo "No Allure results at $RESULTS. Run 'pytest' first." >&2
  exit 1
fi

if ! command -v allure >/dev/null 2>&1; then
  echo "Allure CLI not found. Install from https://allurereport.org/docs/install/" >&2
  exit 1
fi

allure generate "$RESULTS" --clean --single-file -o "$OUTPUT"
echo "Report written to $OUTPUT/index.html"
