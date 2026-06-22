# Publication gate

The project may be released as a **research programme / formalization paper**
when all items in Gate A pass.  It may be advertised as a new mathematical
advance only when Gate B also passes.  It may be advertised as a proof of RH
only when Gate C passes and independent experts confirm it.

## Gate A — formalized research-programme paper

- [ ] Clean build from the public tag on Linux.
- [ ] No `sorry`, `admit`, project `axiom`, or hidden binary dependency.
- [ ] `#print axioms` reviewed for all headline Lean theorems.
- [ ] `riemannXi` connected rigorously to Mathlib's `RiemannHypothesis`.
- [ ] Abstract slit-plane/Stieltjes implication fully proved in Lean.
- [ ] Prime-tail estimate fully proved in Lean.
- [ ] Source-claim audit reviewed by a number theorist and an analyst.
- [ ] Paper states all operator convergence assumptions explicitly.
- [ ] DOI/archive, tag, logs, hashes, and Git bundle published.

## Gate B — substantive research paper

Everything in Gate A, plus at least one genuinely new, independently checked
result such as:

- [ ] a sharper strip/domain theorem with exact source conventions;
- [ ] a nontrivial Galerkin/resolvent error theorem applicable to the concrete
      operator;
- [ ] a certified lower bound on the spectral gap over a growing regime;
- [ ] a non-circular rate for the lowest-state alignment;
- [ ] a theorem reducing the full convergence to verifiable finite certificates
      with explicit constants.

## Gate C — RH claim

- [ ] Concrete self-adjoint operator constructed with all domains checked.
- [ ] Simplicity/parity hypotheses proved uniformly.
- [ ] Trace-class squared resolvent and correct spectral multiplicities proved.
- [ ] Full prime–resolvent convergence proved on a nonempty interval.
- [ ] No assumption equivalent to RH or global Weil positivity used.
- [ ] Lean theorem concludes Mathlib's `RiemannHypothesis` with an acceptable
      axiom oracle.
- [ ] Independent line-by-line review by several specialists.

Until Gate C is complete, the repository and paper must display the no-claim
notice prominently.
