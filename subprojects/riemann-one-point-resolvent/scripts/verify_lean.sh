#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
command -v lake >/dev/null 2>&1 || { echo "lake not found" >&2; exit 1; }

report="$(mktemp)"
trap 'rm -f "$report"' EXIT

lake exe cache get
lake build
lake env lean OnePointResolvent/Oracle.lean 2>&1 | tee "$report"
python3 scripts/check_oracle_coverage.py --report "$report"
echo "Lean build and admitted-axiom oracle passed"
