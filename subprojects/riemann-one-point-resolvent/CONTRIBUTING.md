# Contributing

1. Abstract slit-plane, Hausdorff and certificate results belong here; concrete operator estimates belong in the companion prime repository.
2. State exact hypotheses and primary references.
3. Do not add `sorry`, `admit`, project axioms or theorem-shaped placeholders.
4. Add headline declarations to `OnePointResolvent/Oracle.lean`.
5. Mark conventional but unformalized arguments as documented, not kernel checked.
6. Numerical data must be deterministic and clearly non-probative unless an exact verifier checks it.
7. Keep the interface contract byte-identical to the companion repository.
8. Run `./scripts/verify.sh` and `mkdocs build --strict` before a pull request.
