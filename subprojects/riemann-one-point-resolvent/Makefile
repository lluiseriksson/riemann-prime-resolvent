.PHONY: all lean figures certificates docs static verify metadata workflow-audit hygiene docs-assets oracle-coverage generated-reproducibility manifest manifest-check audit package clean

all: verify

lean:
	./scripts/verify_lean.sh

figures:
	python3 scripts/generate_figures.py

certificates:
	python3 scripts/exact_atomic_certificate.py --output docs/assets/data/exact_atomic_certificate.json

docs: figures certificates
	mkdocs build --strict

static:
	./scripts/verify_static.sh

verify:
	./scripts/verify.sh

metadata:
	python3 scripts/check_metadata.py

workflow-audit:
	python3 scripts/check_workflows.py

hygiene:
	python3 scripts/check_repo_hygiene.py

docs-assets:
	python3 scripts/check_docs_assets.py

oracle-coverage:
	python3 scripts/check_oracle_coverage.py

generated-reproducibility:
	python3 scripts/check_generated_reproducibility.py

manifest:
	python3 scripts/generate_manifest.py

manifest-check:
	python3 scripts/generate_manifest.py --check

audit: metadata workflow-audit hygiene docs-assets oracle-coverage manifest-check
	python3 scripts/check_release.py

package: audit
	python3 scripts/package_release.py

clean:
	rm -rf .lake/build site release .pytest_cache .mypy_cache .ruff_cache \
		scripts/__pycache__ tests/__pycache__ .coverage
