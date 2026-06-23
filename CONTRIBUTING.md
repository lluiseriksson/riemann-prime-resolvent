# Contributing

Contributions are welcome when they preserve the claim boundary and repository ownership.

1. Construction/operator estimates belong at the repository root; abstract Hausdorff and slit-plane results belong in `subprojects/riemann-one-point-resolvent`.
2. State exact hypotheses, primary sources, normalization conventions and the non-circularity argument.
3. Do not add `sorry`, `admit`, project axioms or theorem-shaped placeholders to publication targets.
4. Add headline declarations to `oracle_check.lean` and update the theorem/status ledgers when claims change.
5. Numerical changes must export deterministic data and state whether they are illustrative or exactly certified.
6. Keep `docs/contracts/resolvent-interface.json` byte-identical to the mirrored criterion contract.
7. Keep shared release/audit tooling byte-identical across the two project roots; the release audit enforces this invariant.
8. Keep every third-party GitHub Action pinned to a full commit SHA and disable checkout credential persistence.
9. Review generated changes before running `make manifest`; never use manifest regeneration to conceal unexplained drift.
10. Run `./scripts/verify.sh`, `make audit` and `mkdocs build --strict` before a pull request.

A pull request should be narrow enough that reviewers can identify exactly which mathematical status, generated artifact or engineering invariant changed.
