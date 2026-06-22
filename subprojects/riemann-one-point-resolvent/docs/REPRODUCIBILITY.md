# Reproducibility

## Static layer

```bash
python3 -m pip install -r requirements.txt -r requirements-docs.txt
./scripts/verify_static.sh
```

This regenerates exact data and figures, runs tests, checks local documentation links, builds the site when MkDocs is installed, rejects standalone paper/PDF artifacts and verifies the release manifest.

## Lean layer

```bash
lake exe cache get
./scripts/verify_lean.sh
```

The repository pins Lean 4.31.0 and Mathlib commit `fabf563a7c95a166b8d7b6efca11c8b4dc9d911f`.

## Full layer

```bash
./scripts/verify.sh
```

The ZIP construction environment did not contain Lean. The source was statically audited here; the publishing agent must preserve a green CI build before tagging the release.
