# Final 0.3.x release closeout

## Release identity

- Version file: `0.3.0-docs-integrated`
- Intended tag: `v0.3.0-docs-integrated`
- Closeout prepared from: `c57e4727c3ffd3dca43627c3a4c1494ada3af1d2`
- State: engineering-complete, research-open

No version bump is needed. The existing version already names the integrated
0.3.x artifact and is the value expected by the repository's metadata and
release checks.

## What this release establishes

The release provides:

- reproducible source archives and SHA-256 manifests;
- pinned Lean, Mathlib, Python and GitHub Actions inputs;
- successful root and criterion Lean builds;
- complete public theorem/lemma coverage by `#print axioms` oracles;
- enforcement of the emitted axiom reports;
- deterministic generated data, figures and exact certificates;
- strict documentation, workflow, metadata and repository-hygiene checks.

## What this release does not establish

It does **not** prove:

1. the full integer-cutoff prime-tail theorem;
2. the slit-plane criterion or the existence of its Stieltjes extension;
3. a concrete spectral operator satisfying the proposed interfaces;
4. the defect rate and operator convergence needed for the final argument;
5. the Riemann hypothesis.

These boundaries are tracked in
[`RESEARCH-FRONTIER.md`](RESEARCH-FRONTIER.md).

## Final release procedure

Run from a clean checkout:

```bash
./scripts/verify.sh
make package
(cd release && sha256sum -c -- *.zip.sha256)
git tag -a v0.3.0-docs-integrated -m "Final integrated 0.3.x research artifact"
git push origin v0.3.0-docs-integrated
```

The tag-triggered release workflow should then publish both deterministic
source archives and provenance attestations. Record the workflow URLs and
archive checksums in the GitHub release notes.

## Archive decision

Do not archive immediately. Keep the repository in maintenance-only mode so
the four research-frontier issues remain writable. Archive only when the gate
in [`../MAINTENANCE.md`](../MAINTENANCE.md) is satisfied.
