# Publication gate — “10/10+” standard

A polished repository is not the same thing as a solved open problem. The following gates prevent presentation from outrunning mathematics.

## Gate 1 — formalization paper

Required:

- [ ] Slit-plane criterion fully formalized in Lean.
- [ ] Exact Mathlib RH bridge.
- [ ] Infinite Hausdorff moment theorem instantiated.
- [ ] Prime-tail theorem formalized.
- [ ] Finite certificate checker and test vectors.
- [ ] Clean CI, no project `sorry` or project axioms.
- [ ] Independent Lean reviewer reproduces from a fresh clone.

Target assessment: strong formalization paper.

## Gate 2 — analysis/spectral paper

In addition to Gate 1:

- [ ] A new, unconditional estimate for a concrete operator family.
- [ ] Uniform trace-resolvent control.
- [ ] Domain and trace-class theorems.
- [ ] Certified numerical examples tied to the infinite model.
- [ ] Specialist novelty audit.

Target assessment: substantive research paper.

## Gate 3 — RH claim

In addition to Gates 1–2:

- [ ] Full convergence on an interval.
- [ ] No use of RH-equivalent positivity hidden in hypotheses.
- [ ] Multiplicity and normalization audit.
- [ ] Independent proofs or verification by several experts.
- [ ] Public immutable source, logs, certificates, and archival DOI.

Only Gate 3 supports a claim of proving RH.
