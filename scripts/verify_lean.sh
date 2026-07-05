#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
command -v lake >/dev/null 2>&1 || { echo "lake not found" >&2; exit 1; }

root_report="$(mktemp)"
criterion_report="$(mktemp)"
trap 'rm -f "$root_report" "$criterion_report"' EXIT

lake exe cache get
lake build
lake env lean oracle_check.lean 2>&1 | tee "$root_report"
python3 scripts/check_oracle_coverage.py --report "$root_report"

(
  cd subprojects/riemann-one-point-resolvent
  lake exe cache get
  lake build
  lake env lean OnePointResolvent/Oracle.lean 2>&1 | tee "$criterion_report"
  python3 scripts/check_oracle_coverage.py --report "$criterion_report"
)

echo "Lean build and admitted-axiom oracle passed"
