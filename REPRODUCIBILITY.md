# Reproducibility

## Exact environment

- Lean toolchain: see `lean-toolchain`.
- Mathlib revision: see `lakefile.lean` and `lake-manifest.json`.
- Supported baseline: Linux x86_64.

## Complete verification command

```bash
./scripts/verify.sh
```

The script records:

- UTC timestamp;
- OS and architecture;
- Git SHA and dirty status;
- Lean and Lake versions;
- SHA-256 of lock/config files;
- full build output;
- axiom-oracle output;
- consistency-scan result.

## Clean rebuild

```bash
rm -rf .lake/build
lake exe cache get
lake build
lake env lean oracle_check.lean
python3 scripts/check_consistency.py
```

## Release bundle

```bash
./scripts/package_release.sh v0.1.0
```

This creates a source archive and SHA-256 manifest while excluding `.git`,
`.lake`, and generated logs.

## Current packaging caveat

The seed ZIP was produced in an environment without a Lean executable.  LaTeX
and static source checks were run, but the first external agent must run the
Lean build and preserve the resulting log before public launch.
