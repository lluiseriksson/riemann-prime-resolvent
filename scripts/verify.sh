#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
mkdir -p logs

echo "=== environment ==="
date -u --iso-8601=seconds
uname -a
python3 --version
latexmk -v | head -2 || true
cat lean-toolchain

echo "=== static Lean audit ==="
python3 scripts/check_no_placeholders.py
python3 scripts/static_lean_sanity.py

echo "=== Python tests ==="
python3 -m pytest -q

echo "=== exact certificates ==="
python3 scripts/exact_atomic_certificate.py --output-dir data/certificates

echo "=== numerical illustration ==="
python3 scripts/numerical_demo.py --output-dir data/demo

echo "=== paper ==="
./scripts/build_paper.sh

echo "=== Lean ==="
if command -v lake >/dev/null 2>&1 && command -v lean >/dev/null 2>&1; then
  lean --version
  lake --version
  lake exe cache get
  lake build
  lake env lean PrimeResolvent/Oracle.lean
  LEAN_STATUS="passed"
else
  LEAN_STATUS="not-run: Lean/lake absent in this environment"
  echo "$LEAN_STATUS"
  if [[ "${REQUIRE_LEAN:-0}" == "1" ]]; then
    exit 1
  fi
fi

echo "=== manifest ==="
python3 scripts/generate_manifest.py
python3 scripts/check_release.py

echo "Verification complete. Lean status: $LEAN_STATUS"
