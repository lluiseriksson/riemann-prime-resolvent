# Changelog

## Unreleased

- Added a cross-platform repository hygiene audit for CRLF drift, case-insensitive path collisions and generated cache files.
- Scrubbed Graphviz SVG generator-version comments to prevent manifest churn across runner images.
- Replaced regex-only Lean placeholder scans with a position-preserving scanner for nested comments, strings and interpolated expressions.
- Closed the release-packaging audit/read race by archiving a manifest-verified immutable byte snapshot and rechecking the tree before publication.
- Rejected source paths that collide by case or Unicode normalization or are unsafe on Windows filesystems.
- Added metadata audits for VERSION, release tags, CFF, CodeMeta, Python package versions, Lean toolchains and exact Mathlib revisions.
- Isolated root and criterion pytest discovery and enabled strict pytest configuration/marker handling.
- Added a reproducible container build, fixed Ubuntu runner labels, disabled persisted checkout credentials and smoke-tested the image in CI.
- Published the criterion documentation beneath the canonical Pages site and emitted separately reusable root and criterion source archives.
- Expanded contribution, review, security and issue-reporting guidance around claim boundaries and reproducible release evidence.
- Pinned all GitHub Actions in root and criterion-subproject workflows to immutable commit SHAs.
- Added a workflow supply-chain audit that rejects mutable action refs, `pull_request_target`, and network installers piped to interpreters.
- Added release provenance attestations for root and criterion-subproject source ZIPs.
- Added `.gitattributes` to normalize source/doc line endings and protect binary artifacts from newline conversion.
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
