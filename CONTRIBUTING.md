# Contributing

Contributions are welcome when they preserve the claim boundary and repository ownership.

1. Construction/operator estimates belong here; abstract Hausdorff and slit-plane results belong in the companion repository.
2. State exact hypotheses, primary sources and the non-circularity argument.
3. Do not add `sorry`, `admit`, project axioms or theorem-shaped placeholders to publication targets.
4. Add headline declarations to `oracle_check.lean`.
5. Numerical changes must export deterministic data and state whether they are illustrative or certified.
6. Keep `docs/contracts/resolvent-interface.json` byte-identical to the companion repository.
7. Run `./scripts/verify.sh` and `mkdocs build --strict` before a pull request.
