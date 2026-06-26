#!/usr/bin/env bash
# Opens an interactive Allure report from reports/allure-results.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
RESULTS="$ROOT/reports/allure-results"

if [[ ! -d "$RESULTS" ]]; then
  echo "No Allure results at $RESULTS. Run 'pytest' first." >&2
  exit 1
fi

if command -v allure >/dev/null 2>&1; then
  exec allure serve "$RESULTS"
fi

echo "Allure CLI not found. Install from https://allurereport.org/docs/install/" >&2
exit 1
