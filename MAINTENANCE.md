# Maintenance and archive policy

After `v0.3.0-docs-integrated`, this repository is feature-complete for its documented
0.3.x scope.

## Accepted maintenance

Changes should normally be limited to:

- security fixes;
- broken reproducibility caused by toolchain or hosting changes;
- corrections to false, ambiguous or overstated claims;
- preservation and citation metadata;
- rigorous progress on RF-1 through RF-4.

New presentation features, speculative operator variants and unrelated
experiments belong in a successor repository or fork.

## Research changes

A research change must name a frontier ID, state which acceptance criterion it
advances, and preserve the no-RH-claim boundary. Numerical evidence must remain
clearly separated from proof.

## Archive gate

Archive the repository only when all of the following hold:

1. `v0.3.0-docs-integrated` and both deterministic source archives are published.
2. Provenance attestations and checksums are externally retrievable.
3. RF-1 through RF-4 are solved, rejected, or migrated with durable links.
4. Open pull requests and issues are triaged.
5. The citation metadata points to the final preserved artifact.
6. A final CI run is green at the archived commit.

Until then, leave the repository unarchived and describe it as
**maintenance-only, research frontier open**.
