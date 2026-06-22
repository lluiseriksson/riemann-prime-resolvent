# Lean 4 formalization

The repository pins Lean 4.31.0 and Mathlib commit `fabf563a7c95a166b8d7b6efca11c8b4dc9d911f`.

## Verified source boundary

```lean
theorem hausdorffDiff_atomicMoment
    (weight point : ι → ℝ) (k n : ℕ) :
  hausdorffDiff k (atomicMoment weight point) n =
    ∑ i, weight i * point i ^ n * (1 - point i) ^ k
```

The source also proves support/weight inequalities, complete monotonicity of finite resolvent moments and positive finite Gram/localizing certificates.

## Mandatory checks

```bash
lake build
lake env lean OnePointResolvent/Oracle.lean
python3 scripts/check_no_placeholders.py
```

The oracle prints axioms for all headline finite theorems. CI must be green before any release claims that the pinned formal layer is reproduced.

## Analytic frontier

The exact completed-zeta bridge, slit-plane criterion, Hausdorff measure theorem, parameterized holomorphic integral and normal-family theorem remain to be formalized. Their prose proofs do not change the kernel-checked boundary.
