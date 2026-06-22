# Reproducibility

```bash
python3 -m pip install -r requirements.txt -r requirements-docs.txt
./scripts/verify_static.sh
lake exe cache get
./scripts/verify_lean.sh
```

The static layer regenerates SVG/PNG figures and CSV data, validates exact certificates, checks links, runs tests, builds the docs when MkDocs is available and verifies the source manifest. The Lean layer compiles the root library and runs `oracle_check.lean`.
