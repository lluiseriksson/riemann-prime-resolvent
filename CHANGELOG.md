# Changelog

## Unreleased

- Made manifest verification read-only in CI so stale generated/source files can no longer be silently accepted.
- Added complete inventory checks, canonical-path validation, symlink rejection and byte-identical contract-mirror enforcement.
- Replaced the external, timestamp-sensitive `zip -r` release with a manifest-driven byte-reproducible Python archive.
- Added regression tests for manifest drift, unlisted files, mirrored contracts, symlinks and reproducible archives.
- Fixed the root release workflow to install the criterion subproject's Python dependencies.

## 0.3.0-docs-integrated — 2026-06-22

- Reframed the repository as the construction layer of a single-repository programme with an imported criterion subproject.
- Integrated the full scholarly exposition into `docs/programme/`.
- Removed the standalone paper tree, PDF manuscript artifacts and paper-only workflow.
- Added strict MkDocs documentation and GitHub Pages deployment.
- Added a byte-identical monorepo resolvent interface contract.
- Added no-PDF/no-paper-directory release checks and Markdown link validation.
- Standardized web-native figures to SVG/PNG.
- Corrected the three-step triangle proof to the current `abs_add_le` API.
- Clarified that the prime cutoff in the sum–integral bound is an integer.

## 0.2.0-blueprint — 2026-06-22

- Publication blueprint with Lean seed, source audits, figures and release tooling.
