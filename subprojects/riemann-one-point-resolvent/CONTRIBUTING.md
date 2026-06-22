# Contributing

Contributions are welcome when they preserve the project’s claim boundary.

1. Open an issue describing the exact theorem, source, and dependency graph.
2. Keep each pull request mathematically narrow.
3. Add tests and `#print axioms` for headline Lean theorems.
4. Do not introduce `sorry`, `admit`, or project axioms into publication targets.
5. Mark conjectural statements as `Conjecture`, `ResearchTarget`, or documentation—not as proved theorems.
6. Numerical work must export reproducible data or certificates.
7. Cite primary literature and pin version-dependent API claims.

Run `./scripts/verify.sh` before submitting.
