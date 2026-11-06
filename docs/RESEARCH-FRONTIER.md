# Research frontier after `v0.3.0-docs-integrated`

The `v0.3.0-docs-integrated` release closes the repository's **engineering and
reproducibility phase**. It does not claim the Riemann hypothesis, a
Hilbert–Pólya construction, or the missing analytic implications.

The four items below are research programmes, not release blockers. Their
machine-readable source is [`research-frontier.json`](research-frontier.json).

## RF-1 — Integer-cutoff prime tail

The integer-tail theorem is now verified in `PrimeTail.lean`: for every
`N ≥ 3`, `δ > 0`, `σ ≥ 1 + δ`, the actual von Mangoldt tail is summable and
bounded by `primeTailMajorant δ N`. The scaled theorem keeps `N`; using the
continuous formula requires `(N : ℝ) = lam²`. Numerical boundary regressions
and the standard-axiom oracle accompany it. No RH premise is used.

The issue remains available for integration review. This result does not
identify a concrete model's error with that tail or discharge RF-3/RF-4.
See [the exact statement and proof boundary](programme/arithmetic-side.md).

## RF-2 — Slit-plane Stieltjes criterion

Prove the implication

```text
XiStieltjesExtensionTarget → XiOnlyRealZeros
```

with the branch, domain, zero multiplicities and logarithmic-derivative
singularities stated explicitly. The theorem must remain separate from the
existence of the extension and from any concrete spectral model.

## RF-3 — Concrete spectral model

Define the Hilbert space, operator domain and finite approximants, then prove
the self-adjointness, compactness/resolvent and approximation properties used
by the programme. Every imported result must pass a no-circularity audit.

Numerical spectral agreement alone does not complete this item.

## RF-4 — Defect rate and convergence

For the concrete model, prove a quantified defect rate `q > 1/2`, discharge the
gap/tail hypotheses, and combine all error terms into the concrete
prime-resolvent convergence endpoint. This item depends on RF-1 and RF-3.

The typed `PublicationGate` in `RiemannPrimeResolvent.PublicationFrontier`
is the machine-readable meeting point for this work: RF-3/RF-4 must eventually
instantiate its `defect : ℕ → ℝ` and `budget : ℕ → ErrorBudget` fields with the
certified construction data, not with standalone placeholder propositions.

## Dependency order

```text
RF-1 ─┐
      ├── RF-4
RF-3 ─┘

RF-2 is logically independent of the construction branch.
```

## Repository state

The repository should remain **unarchived but maintenance-only** while these
issues are open. Archiving would make the research records read-only. Archive
only after the four items are solved, rejected, or migrated to a successor
repository and the final release artifacts have a durable preservation target.
