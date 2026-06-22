# Formal proof plan for the analytic criterion

The next formalization should preserve the following dependency order.

## 1. Xi conventions

```lean
noncomputable def riemannXi (z : ℂ) : ℂ := ...
noncomputable def xiResolventTarget (x : ℝ) : ℝ := ...

theorem riemannHypothesis_iff_riemannXi_realZeros : ...
```

The proof must audit Mathlib’s normalization of the completed zeta function. No theorem should be stated until the exact factors `s(s-1)/2`, `π^{-s/2}`, and `Γ(s/2)` are matched.

## 2. Slit-plane geometry

```lean
def slitPlane : Set ℂ := {z | z ∉ Set.Iic (0 : ℝ)} -- exact coercion to be settled

theorem neg_sq_mem_slitPlane_of_im_pos
    {z : ℂ} (hz : 0 < z.im) : -z^2 ∈ slitPlane := ...
```

A robust implementation may define the removed ray explicitly as `{z : ℂ | z.im = 0 ∧ z.re ≤ 0}`.

## 3. Logarithmic-derivative poles

```lean
theorem hasPole_logDeriv_at_zero
    (hf : AnalyticAt ℂ f z0)
    (hzero : f z0 = 0)
    (hnonzero : f ≠ᶠ[𝓝 z0] 0) : ...
```

Prefer a local factorization theorem with multiplicity over informal manipulation of meromorphic functions.

## 4. Slit-plane criterion

```lean
theorem riemannHypothesis_of_slitPlaneExtension
    (I : Set ℝ) (hIopen : IsOpen I) (hInonempty : I.Nonempty)
    (hI : I ⊆ Set.Ioi (1 / 4 : ℝ))
    (S : ℂ → ℂ)
    (hShol : HolomorphicOn S slitPlane)
    (hSaxis : ∀ x ∈ I, S x = xiResolventTarget x) :
    RiemannHypothesis := ...
```

## 5. Hausdorff theorem interface

```lean
def IsHausdorffMomentSequence (b : ℕ → ℝ) : Prop :=
  ∃ μ : Measure ℝ,
    IsFiniteMeasure μ ∧ μ (Set.Icc 0 1)ᶜ = 0 ∧
    ∀ n, b n = ∫ x, x^n ∂μ

theorem hausdorff_iff_signedDiff_nonneg : ...
```

Search Mathlib first for an existing theorem before adding a new general moment library.

## 6. One-point theorem

```lean
def xiJetMoment (x0 : ℝ) (n : ℕ) : ℝ :=
  x0^n * ((-1 : ℝ)^n / n.factorial) * iteratedDeriv n xiResolventTarget x0

theorem riemannHypothesis_iff_onePointHausdorff
    (hx0 : 1 / 4 < x0) :
    RiemannHypothesis ↔ IsHausdorffMomentSequence (xiJetMoment x0) := ...
```

The reverse direction must construct the explicit integral extension and prove its holomorphy on the slit plane.

## 7. Prime tail

Formalize the completed-zeta logarithmic derivative, the von Mangoldt Dirichlet series, and the integral majorant. The statement should expose all cutoff and domain assumptions rather than bury them in notation.

## 8. Publication oracle

Add every headline theorem to `PrimeResolvent/Oracle.lean` and require the standard Mathlib kernel footprint only. No open research statement may be introduced as an axiom or opaque theorem.
