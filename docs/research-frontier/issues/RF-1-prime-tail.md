# [RF-1] Prove the integer-cutoff von Mangoldt prime-tail bound

<!-- frontier-id: RF-1 -->

## Goal

Implemented by `primeTail_summable_and_le` in `PrimeTail.lean`, with the
integer cutoff and scaled equality guard documented in the arithmetic page.
The issue remains open for integration review; RF-3/RF-4 are not discharged.

## Acceptance criteria

- [x] Exact sum, normalization, integer cutoff and parameter range are stated.
- [x] The bound is compatible with `primeTailMajorant` and
      `resolventPrimeTailMajorant`.
- [x] No RH-equivalent estimate is used.
- [x] A placeholder-free Lean theorem is added.
- [x] Numerical boundary and regression tests are added.

## Non-goals

Optimizing every constant; importing the desired spectral conclusion.
