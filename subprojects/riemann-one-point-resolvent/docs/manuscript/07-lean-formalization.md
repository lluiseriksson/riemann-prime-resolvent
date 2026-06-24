# Lean 4 formalization

The repository pins Lean 4.31.0 and Mathlib commit `fabf563a7c95a166b8d7b6efca11c8b4dc9d911f`.

## Verified source boundary

```lean
theorem finitePositiveStieltjes_family_norm_le_two
    (s : κ → Finset ι)
    (weight spectrum : κ → ι → ℝ)
    (x₀ M : ℝ)
    ... :
  ‖finitePositiveStieltjes (s j) (weight j) (spectrum j) z‖ ≤ 2 * M
```

The omitted hypotheses require nonnegative weights and spectrum, `0 < x₀`, a
uniform one-point bound by `M`, and `‖z - x₀‖ ≤ x₀ / 2`. The theorem is
parametric in the cutoff family and contains no atom-count or spectral-size
constant. The source also proves the exact finite Hausdorff difference formula,
complete monotonicity of finite resolvent moments and positive finite
Gram/localizing certificates.

## Mandatory checks

```bash
lake build
lake env lean OnePointResolvent/Oracle.lean
python3 scripts/check_no_placeholders.py
```

The oracle prints axioms for every public theorem or lemma. CI must be green before any release claims that the pinned formal layer is reproduced.

## Analytic frontier

The exact completed-zeta bridge, slit-plane criterion, Hausdorff measure theorem,
parameterized holomorphic integral, arbitrary-compact Stieltjes domination and
Montel/uniqueness packaging remain to be formalized. The finite-disk theorem is
a verified local input, not the completed normal-family argument.
