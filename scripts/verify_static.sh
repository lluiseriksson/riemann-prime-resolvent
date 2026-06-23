#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."

python3 scripts/check_workflows.py
python3 scripts/check_repo_hygiene.py
python3 scripts/check_metadata.py
python3 scripts/check_docs_assets.py
python3 scripts/check_no_placeholders.py
python3 scripts/check_oracle_coverage.py
python3 scripts/check_generated_reproducibility.py
python3 scripts/validate_certificate.py experiments/examples/demo_exact_rational.json
python3 scripts/check_markdown_links.py
python3 -m pytest -q
(cd subprojects/riemann-one-point-resolvent && ./scripts/verify_static.sh)
# Check, never rewrite: generated-artifact or source drift must fail CI.
python3 scripts/generate_manifest.py --check
python3 scripts/check_release.py

if command -v mkdocs >/dev/null 2>&1; then
  mkdocs build --strict
else
  echo "mkdocs not installed; strict docs build is enforced in CI"
fi

echo "Static verification passed"
