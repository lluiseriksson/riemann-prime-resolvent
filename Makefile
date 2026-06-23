.PHONY: all lean figures docs static verify metadata workflow-audit hygiene manifest manifest-check audit package clean

all: verify

lean:
	./scripts/verify_lean.sh

figures:
	python3 scripts/generate_figures.py

docs: figures
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

manifest:
	python3 scripts/generate_manifest.py

manifest-check:
	python3 scripts/generate_manifest.py --check

audit: metadata workflow-audit hygiene manifest-check
	python3 scripts/check_release.py

package: audit
	python3 scripts/package_release.py

clean:
	rm -rf .lake/build site release .pytest_cache .mypy_cache .ruff_cache \
		scripts/__pycache__ tests/__pycache__ .coverage
