# Reproducibility

Install both monorepo dependency sets before running the integrated static layer:

```bash
python3 -m pip install   -r requirements.txt   -r requirements-docs.txt   -r subprojects/riemann-one-point-resolvent/requirements.txt   -r subprojects/riemann-one-point-resolvent/requirements-docs.txt
./scripts/verify_static.sh
lake exe cache get
./scripts/verify_lean.sh
```

The static layer runs the repository hygiene audit, audits workflow/installer surfaces, release metadata and Lean source placeholders; regenerates SVG/PNG figures, CSV data and exact certificates; runs isolated root and criterion tests; checks local links; builds documentation when MkDocs is available; and then **checks** the committed source manifests without rewriting them. A stale generated artifact or an unlisted source file therefore fails verification instead of being silently absorbed into a new manifest.

## Lean source audit

`scripts/check_no_placeholders.py` masks nested Lean comments and ordinary string contents while retaining line positions. Interpolated expressions remain visible. It rejects `sorry`, `admit`, project `axiom` declarations and unsafe theorem/lemma declarations with file/line/column diagnostics. This is a policy guard in addition to—not a replacement for—the Lean build and `#print axioms` oracle.

## Workflow and container policy

All third-party `uses:` entries in root and preserved criterion workflows are pinned to full 40-character commit SHAs, with the human-readable major version kept only as a comment. `scripts/check_workflows.py` requires fixed hosted-runner labels, top-level least-privilege permissions and `persist-credentials: false`; it rejects mutable Action refs, `pull_request_target`, mutable raw GitHub branch URLs and network installers executed directly by interpreters.

The Dockerfile downloads a versioned Elan release to disk before execution, installs both Python dependency roots in a virtual environment and is built by `.github/workflows/container.yml` whenever its inputs change.

When updating an Action, resolve the new tag to a commit, replace the SHA, keep the version comment current, and run:

```bash
python3 scripts/check_workflows.py
make manifest
make audit
```

## Metadata coherence

`python3 scripts/check_metadata.py` cross-checks VERSION, CFF, CodeMeta, changelog sections, Python package metadata, Lean toolchains and exact 40-character Mathlib revisions across both project roots. Tagged releases additionally require the exact tag `v$(cat VERSION)`.

## Oracle/ledger traceability

`scripts/check_oracle_coverage.py` masks Lean comments and strings, reads the exact `#print axioms` sequence from `oracle_check.lean`, and requires the verified rows in `docs/THEOREM-LEDGER.md` to match it one-for-one and in the same order. Wildcards and prose-only verified entries are rejected. The Lean build remains the source of kernel evidence; this check prevents the human-facing ledger from drifting away from the oracle.

## Generated-artifact reproducibility

`scripts/check_generated_reproducibility.py` runs the project generators twice with fresh Matplotlib configuration directories and deterministic environment variables. Every generated SVG, PNG and CSV must be byte-identical between runs. The criterion check applies the same rule to its exact atomic certificate. The subsequent manifest check still proves that the reproducible output equals the committed output.

## Documentation asset pinning

`scripts/check_docs_assets.py` requires remote MkDocs assets to use HTTPS and exact jsDelivr npm semantic versions. MathJax is pinned to `3.2.2`; mutable major-only, `latest`, `main` and `master` references fail verification.

## Manifest workflow

```bash
# Deliberate update after reviewing source/generated changes
make manifest

# Read-only validation used by CI and release jobs
make audit
```

The root audit requires the two interface contracts and shared release/audit scripts to be byte-identical. It rejects included symlinks, unsafe or non-NFC paths, case-fold collisions, Windows-reserved names, duplicate rows, PDFs and standalone `paper/` directories.

## Deterministic source archives

```bash
make package
(cd release && sha256sum -c -- *.zip.sha256)
(cd subprojects/riemann-one-point-resolvent && make package)
```

`package_release.py` uses only the Python standard library. After policy and manifest validation it reads each file into an immutable, size/hash-verified snapshot. The ZIP is built exclusively from those bytes beneath one versioned top-level directory, with sorted members, fixed timestamps, canonical permissions, empty extra fields and uncompressed entries. The source tree and committed manifest are checked again before the temporary archive is atomically published.

The active root release workflow builds both the canonical monorepo archive and a separately reusable criterion-subproject archive twice, requires byte-identical SHA-256 output, verifies each checksum file and creates OIDC provenance attestations.

## Canonical Pages layout

The Pages workflow regenerates and validates both documentation trees. The construction site is deployed at the repository root and the criterion manuscript beneath `/criterion/`, avoiding two competing Pages deployments for one monorepo.


## Cross-platform hygiene

`check_repo_hygiene.py` rejects CRLF drift in normalized text files, case-insensitive path collisions, symlinks in the source inventory and accidentally committed local cache files. `generate_figures.py` also removes Graphviz version comments from SVG output so runner-image upgrades do not create irrelevant manifest churn.
