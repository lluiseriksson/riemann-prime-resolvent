#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

mkdir -p paper/figures data/demo data/certificates

if [[ ! -f data/demo/resolvent_comparison.pdf ]]; then
  python3 scripts/numerical_demo.py --output-dir data/demo
fi
if [[ ! -f data/certificates/exact_atomic_certificate.json ]]; then
  python3 scripts/exact_atomic_certificate.py --output-dir data/certificates
fi

cp data/demo/resolvent_comparison.pdf paper/figures/resolvent_comparison.pdf
cp data/demo/resolvent_errors.pdf paper/figures/resolvent_errors.pdf

mkdir -p logs
if ! latexmk -pdf -interaction=nonstopmode -halt-on-error -cd paper/main.tex > logs/paper-build.txt 2>&1; then
  cat logs/paper-build.txt
  exit 1
fi
cp paper/main.pdf paper/one_point_resolvent_hausdorff.pdf
latexmk -c -cd paper/main.tex >/dev/null
rm -f paper/main.pdf
printf 'Built %s\n' "$ROOT/paper/one_point_resolvent_hausdorff.pdf"
