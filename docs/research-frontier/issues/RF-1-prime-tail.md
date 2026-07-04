# [RF-1] Prove the integer-cutoff von Mangoldt prime-tail bound

<!-- frontier-id: RF-1 -->

## Goal

Replace the current closed-form majorant interface with an unconditional
integer-cutoff theorem for the omitted prime/von Mangoldt contribution.

## Acceptance criteria

- [ ] Exact sum, normalization, integer cutoff and parameter range are stated.
- [ ] The bound is compatible with `primeTailMajorant` and
      `resolventPrimeTailMajorant`.
- [ ] No RH-equivalent estimate is used.
- [ ] A placeholder-free Lean theorem is added.
- [ ] Numerical boundary and regression tests are added.

## Non-goals

Optimizing every constant; importing the desired spectral conclusion.
