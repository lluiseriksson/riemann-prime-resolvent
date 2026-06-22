# Artifact status — v0.2.0

## Completed in this archive

- 12-page publication-style paper with full abstract proofs and explicit claim boundary.
- Lean 4 finite theorem layer, pinned to Lean/Mathlib v4.31.0.
- Kernel axiom audit entry point.
- Exact rational Hausdorff/Hankel/localizing toy certificate.
- Reproducible prime and finite-zero numerical illustration.
- Python regression tests.
- GitHub Actions for Lean, Python, paper, and release artifacts.
- Versioning, licenses, citation metadata, manifest, and SHA-256 release tooling.

## Verified in the construction environment

- Python tests: 4 passed.
- Placeholder/project-axiom scan: clean.
- Exact certificate generation: passed.
- Numerical demonstration: passed.
- LaTeX build: passed.
- PDF preflight and visual render inspection: passed.

## Not locally verified here

Lean and Lake were not installed in the artifact-construction container, so the Lean source was not compiled locally. The repository pins the toolchain and makes the Lean build and `#print axioms` audit mandatory in GitHub Actions. This is an explicit remaining release check, not hidden success.

## Scientific status

This is not a proof of RH. The one-point analytic reduction is presented as a theorem in the manuscript; the concrete spectral convergence problem remains open, and novelty relative to existing Hausdorff-moment criteria requires expert review.
