# Changelog

## Unreleased

- Parsed the emitted `#print axioms` evidence and admitted only Lean's standard classical kernel axioms; direct `sorryAx` use or any new project axiom now fails the criterion verification.
- Closed theorem-oracle coverage over all 17 public finite-layer `theorem`/`lemma` declarations and expanded placeholder scanning beyond the conventional library directory.
- Added an exact theorem ledger synchronized automatically with `OnePointResolvent/Oracle.lean`.
- Added two-clean-run byte reproducibility checks for generated figures, data and the exact atomic certificate.
- Pinned MathJax to an exact version and audited remote documentation assets for immutable references.
- Added a cross-platform repository hygiene audit for CRLF drift, case-insensitive path collisions and generated cache files.
- Scrubbed Graphviz SVG generator-version comments to prevent manifest churn across runner images.
- Replaced regex-only placeholder checks with a nested-comment/string-aware Lean source scanner.
- Added portable path/collision checks and manifest-verified immutable snapshots to deterministic source packaging.
- Added coherent release metadata, toolchain and exact Mathlib-pin validation.
- Isolated and hardened pytest discovery and configuration.
- Published the criterion manuscript beneath the canonical monorepo Pages `/criterion/` path.
- Added a separately reusable criterion source archive to the active root release workflow.
- Pinned all preserved subproject GitHub Actions to immutable commit SHAs.
- Added source-release provenance attestations for the preserved subproject workflow.
- Documented the inherited workflow supply-chain policy from the root monorepo audit.
- Made manifest verification read-only in CI and added complete inventory/path/symlink checks.
- Replaced the external ZIP command with a manifest-driven byte-reproducible Python archive.
- Added release-tooling regression tests and reproducibility documentation.

## 0.3.0-docs-integrated — 2026-06-22

- Integrated the complete scholarly exposition into `docs/manuscript/`.
- Removed the standalone paper tree, PDFs and paper-only workflow.
- Canonicalized the Lean library and namespace as `OnePointResolvent`.
- Added strict MkDocs/GitHub Pages documentation.
- Added a cross-repository interface contract shared with `riemann-prime-resolvent`.
- Corrected the arithmetic tail statement to use an integer cutoff.
- Added no-PDF/no-paper-directory release checks and local Markdown link validation.
- Added exact certificate, deterministic figures, tests and source-only release tooling.

## 0.2.0 — 2026-06-22

- Initial publication-oriented artifact with finite Lean certificate layer and standalone manuscript.
