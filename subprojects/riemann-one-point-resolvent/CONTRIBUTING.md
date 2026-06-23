# Contributing

1. Abstract slit-plane, Hausdorff and certificate results belong here; concrete operator estimates belong at the monorepo root.
2. State exact hypotheses, primary references and normalization conventions.
3. Do not add `sorry`, `admit`, project axioms or theorem-shaped placeholders.
4. Add headline declarations to `OnePointResolvent/Oracle.lean` and update the status/Lean-map documentation.
5. Mark conventional but unformalized arguments as documented, not kernel checked.
6. Numerical data must be deterministic and clearly non-probative unless an exact verifier checks it.
7. Keep the interface contract and shared release/audit tooling byte-identical to the monorepo root copies.
8. Keep third-party Actions SHA-pinned; the active root workflow audits the preserved subproject workflows too.
9. Review generated changes before running `make manifest`.
10. Run `./scripts/verify.sh`, `make audit` and `mkdocs build --strict` before a pull request.
