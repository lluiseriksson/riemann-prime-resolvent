# Reproducibility

## Static layer

```bash
python3 -m pip install -r requirements.txt -r requirements-docs.txt
./scripts/verify_static.sh
```

This audits release metadata, workflow policy and Lean placeholder usage; regenerates exact data and figures; runs the criterion tests; checks local documentation links; builds the site when MkDocs is installed; rejects standalone paper/PDF artifacts; and **checks** the committed manifest without rewriting it. Generated or source drift therefore fails CI.

After deliberately reviewing a change, update and audit the manifest explicitly:

```bash
make manifest
make audit
```

The audit requires a complete, sorted inventory of regular files. It rejects unlisted/missing files, duplicate or unsafe paths, Unicode/case collisions, Windows-reserved path segments and included symlinks. Shared release/audit tooling and the interface contract are also checked byte-for-byte by the monorepo root audit.

## Workflow and metadata policy

The preserved subproject workflows remain SHA-pinned like the active root workflows. The root audit scans both workflow trees, requires fixed runner labels and non-persistent checkout credentials, and rejects mutable refs or network installers executed directly by interpreters.

`scripts/check_metadata.py` checks CFF, CodeMeta, VERSION, changelog, Python package version, Lean toolchain and exact Mathlib revision coherence. The criterion Python package uses the PEP 440 local version `0.3.0+docs.integrated` for repository VERSION `0.3.0-docs-integrated`.

## Oracle/ledger traceability and axiom boundary

`scripts/check_oracle_coverage.py` requires every public `OnePointResolvent` theorem/lemma, the exact ordered declarations in `OnePointResolvent/Oracle.lean` and the verified rows in `docs/THEOREM_LEDGER.md` to agree. Wildcards, duplicates, unqualified names and documentation/oracle drift fail the static layer.

The Lean verification captures the emitted `#print axioms` messages and invokes the checker with `--report`. Only `Classical.choice`, `Quot.sound` and `propext` are admitted. A project axiom, direct `sorryAx`, a missing/reordered report or a declaration-uses-sorry warning fails verification.

## Generated artifacts and documentation assets

`scripts/check_generated_reproducibility.py` regenerates the exact atomic certificate, finite-difference data and all SVG/PNG figures twice with clean Matplotlib state, requiring byte-identical output. `scripts/check_docs_assets.py` additionally requires HTTPS and exact semantic versions for jsDelivr npm assets; MathJax is pinned to `3.2.2`.

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
(cd release && sha256sum -c -- *.zip.sha256)
```

The archive is produced from a manifest-verified immutable byte snapshot with fixed timestamps, canonical permissions, sorted uncompressed entries and a versioned top-level directory. The active root release workflow builds this criterion archive twice, requires identical SHA-256 output, uploads it beside the monorepo archive and emits a provenance attestation.

The canonical rendered criterion site is built by the active root Pages workflow beneath `https://lluiseriksson.github.io/riemann-prime-resolvent/criterion/`.

## Cross-platform hygiene

`check_repo_hygiene.py` rejects CRLF drift in normalized text files, case-insensitive path collisions, symlinks in the source inventory and accidentally committed local cache files. `generate_figures.py` also removes Graphviz version comments from SVG output so runner-image upgrades do not create irrelevant manifest churn.
