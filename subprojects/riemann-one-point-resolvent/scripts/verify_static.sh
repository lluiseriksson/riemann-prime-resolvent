#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."

python3 scripts/check_no_placeholders.py
python3 scripts/exact_atomic_certificate.py --output docs/assets/data/exact_atomic_certificate.json
python3 scripts/check_certificate.py docs/assets/data/exact_atomic_certificate.json
python3 scripts/generate_figures.py
python3 scripts/check_markdown_links.py
python3 -m pytest -q
python3 scripts/generate_manifest.py
python3 scripts/check_release.py

if command -v mkdocs >/dev/null 2>&1; then
  mkdocs build --strict
else
  echo "mkdocs not installed; strict docs build is enforced in CI"
fi

echo "Static verification passed"
