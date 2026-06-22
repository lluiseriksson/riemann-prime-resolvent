# Formalization boundary

## Present Lean layer

The formal source contains source-independent elementary statements. Every headline theorem appears in `oracle_check.lean`, and the CI scans project source for `sorry`, `admit`, new project axioms and unsafe shortcuts.

## Companion layer

The one-point repository maintains finite Hausdorff identities and the roadmap for:

- the exact Mathlib \(\xi/\Xi\) convention bridge;
- the slit-plane mapping lemma;
- analytic continuation and the logarithmic-derivative pole argument;
- the Hausdorff moment theorem interface;
- normal-family compactness.

## Promotion rule

A prose theorem is not “formalized” until its Lean declaration compiles at the pinned toolchain and the axiom oracle reports only accepted foundational axioms. Open inputs remain documentation or named target propositions, never theorem assumptions disguised as a completed package.
