.PHONY: all lean python demo certificates paper verify clean release

all: verify

lean:
	lake exe cache get
	lake build
	lake env lean PrimeResolvent/Oracle.lean

python:
	python3 -m pytest -q

certificates:
	python3 scripts/exact_atomic_certificate.py --output-dir data/certificates

demo:
	python3 scripts/numerical_demo.py --output-dir data/demo

paper: demo certificates
	./scripts/build_paper.sh

verify:
	./scripts/verify.sh

release:
	python3 scripts/generate_manifest.py
	python3 scripts/make_release.py

clean:
	rm -rf .lake .pytest_cache __pycache__ tests/__pycache__ data/demo data/certificates
	latexmk -C -cd paper/main.tex || true
