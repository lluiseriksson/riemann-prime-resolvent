.PHONY: all lean figures docs static verify manifest package clean

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

manifest:
	python3 scripts/generate_manifest.py

package:
	python3 scripts/package_release.py

clean:
	rm -rf .lake/build site .pytest_cache scripts/__pycache__ tests/__pycache__
