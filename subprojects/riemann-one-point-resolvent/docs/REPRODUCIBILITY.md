# Reproducibility

## Static layer

```bash
python3 -m pip install -r requirements.txt -r requirements-docs.txt
./scripts/verify_static.sh
```

This regenerates exact data and figures, runs tests, checks local documentation links, builds the site when MkDocs is installed, rejects standalone paper/PDF artifacts and **checks** the committed manifest without rewriting it. Generated or source drift therefore fails CI.

After deliberately reviewing a change, update and audit the manifest explicitly:

```bash
make manifest
make audit
```

The audit requires a complete, sorted inventory of regular files and rejects unlisted files, missing files, duplicate or unsafe manifest paths and included symlinks.

## Workflow supply-chain policy

The preserved subproject workflows are kept SHA-pinned like the root workflows. The root monorepo static verification runs `scripts/check_workflows.py`, which scans both workflow trees and rejects mutable action tags, `pull_request_target`, and network installers piped directly to interpreters. Release workflows also request OIDC provenance attestations for generated source archives.

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

## Deterministic source archive

```bash
make package
(cd release && sha256sum -c *.zip.sha256)
```

The archive is built directly from the validated manifest with fixed timestamps, canonical permissions, sorted uncompressed entries and a versioned top-level directory. The release workflow builds it twice, requires an identical SHA-256 before upload, and emits a provenance attestation for the ZIP.
