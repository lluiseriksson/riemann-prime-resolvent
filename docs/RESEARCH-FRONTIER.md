# Research frontier after `v0.3.0-docs-integrated`

## 2026-08 theta-pencil reboot

A separate zero-based research track is documented under
[`theta-reboot/`](theta-reboot/index.md). Its first audit starts from
Hedenmalm's explicit theta-function differential pencil. Two obstructions rule
out local weights and bounded global ambient metrics, so the active track has
moved to the first source-faithful semilocal window carrying a finite-prime
term, \(4<q\le5\) and \(S_q=\{\infty,2,3\}\). The reboot is exploratory and
does not discharge RF-1--RF-4 or prove RH.

The `v0.3.0-docs-integrated` release closes the repository's **engineering and
reproducibility phase**. It does not claim the Riemann hypothesis, a
Hilbert–Pólya construction, or the missing analytic implications.

The four items below are research programmes, not release blockers. Their
machine-readable source is [`research-frontier.json`](research-frontier.json).

## RF-1 — Integer-cutoff prime tail

Prove an unconditional bound for the omitted von Mangoldt/prime contribution
with an integer cutoff and connect it to `primeTailMajorant` and
`resolventPrimeTailMajorant`.

Completion requires a precise sum and parameter range, explicit constants, a
Lean theorem with no project axioms or placeholders, and numerical boundary
tests. No RH-equivalent estimate may be imported.

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
