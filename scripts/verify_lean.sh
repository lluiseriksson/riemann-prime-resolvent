#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
command -v lake >/dev/null 2>&1 || { echo "lake not found" >&2; exit 1; }
lake build
lake env lean oracle_check.lean
(cd subprojects/riemann-one-point-resolvent && lake build && lake env lean OnePointResolvent/Oracle.lean)
echo "Lean build and axiom oracle passed"
