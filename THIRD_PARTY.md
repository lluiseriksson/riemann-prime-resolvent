# Third-party dependencies

This repository does not vendor third-party source. It declares dependencies on:

- Lean 4 and Mathlib;
- Python;
- mpmath, NumPy, Matplotlib, SymPy, and pytest;
- a TeX Live installation for the paper.

Each dependency remains under its own license. GitHub Actions are referenced by immutable major-version tags in the workflow files; release publication should periodically audit those tags and, for archival releases, may pin full commit SHAs.
