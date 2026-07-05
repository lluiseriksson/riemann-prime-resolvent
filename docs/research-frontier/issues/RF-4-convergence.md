# [RF-4] Prove the spectral defect rate and operator convergence

<!-- frontier-id: RF-4 -->

## Goal

Prove a quantified defect rate above one half and combine all components into
the concrete prime-resolvent convergence theorem.

## Dependencies

RF-1 and RF-3.

## Acceptance criteria

- [ ] An explicit `q > 1/2` rate and constants are proved.
- [ ] Gap, residual/Rayleigh and Galerkin-tail hypotheses are discharged.
- [ ] All error components are combined without hidden asymptotics.
- [ ] The concrete convergence endpoint is proved in Lean.
- [ ] The proof has a documented no-circularity audit.

## Non-goals

Fitted exponents without rigorous enclosure; treating an abstract gate as a
proof that its fields hold.
