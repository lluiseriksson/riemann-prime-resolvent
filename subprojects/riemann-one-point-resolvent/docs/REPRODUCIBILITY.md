# Reproducibility

## Pinned environment

- Lean: `leanprover/lean4:v4.31.0`
- Mathlib: tag `v4.31.0`
- Python dependencies: `requirements.txt`
- LaTeX dependencies: documented in `paper/README.md`

## Full verification

```bash
./scripts/verify.sh
```

The script records system metadata, runs Python tests, regenerates deterministic exact certificates, builds the paper, scans Lean sources for placeholders, and—when Lean is installed—runs:

```bash
lake exe cache get
lake build
lake env lean PrimeResolvent/Oracle.lean
```

Set `REQUIRE_LEAN=1` to make absence of Lean a hard failure.

## Release creation

```bash
python3 scripts/generate_manifest.py
python3 scripts/make_release.py
```

A release contains source, paper, generated data, manifest, and SHA-256 checksums. Numerical plots are reproducible within normal floating-point and library-version tolerances; exact certificate JSON uses rational arithmetic.
