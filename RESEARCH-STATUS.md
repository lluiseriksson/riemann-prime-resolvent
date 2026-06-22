# Research status

Version: `v0.1.0-seed`

## Lean modules prepared for immediate verification

The following modules are written with complete proofs and no placeholders; the first agent must still compile them under the pinned toolchain:

- `Basic.lean`: three-step triangle inequality and error budget;
- `Convergence.lean`: componentwise convergence of the total budget;
- `FiniteStieltjes.lean`: positivity of finite Stieltjes/squared-resolvent sums;
- `PrimeTail.lean`: sign properties of the closed-form tail majorant;
- `RateOptimization.lean`: scalar exponent threshold and saturation;
- `SpectralDefect.lean`: sign properties of Rayleigh/gap and residual/gap defects.

The packaging environment used to create this ZIP did not contain Lean, so the
first agent must run `./scripts/verify.sh` and commit the resulting log.  The
files were statically scanned for `sorry`, `admit`, and project `axiom`
declarations.

## Defined but not proved

- equivalence of `XiOnlyRealZeros` with Mathlib's `RiemannHypothesis`;
- evenness, entireness, and nonvanishing facts for `riemannXi` needed downstream;
- the slit-plane extension criterion;
- normal-family compactness for Stieltjes transforms from one-point control;
- the von Mangoldt tail inequality leading to the closed-form majorant;
- the concrete Connes–Consani–Moscovici spectral construction;
- the spectral alignment estimate and the limit `E_{λ,N} → 0`.

These are tracked in `docs/THEOREM-LEDGER.md`.

## Most valuable next theorem

The next genuine formal brick is the abstract analytic implication:

```text
holomorphic extension of the Xi resolvent target to C \ (-∞,0]
    ⇒ Xi has no non-real zero
    ⇒ RiemannHypothesis.
```

It is independent of the concrete operator construction and can be developed
against Mathlib's complex-analysis API.

## Most valuable mathematical brick

Prove a non-circular quantitative estimate of the form

\[
\eta_{\lambda,N(\lambda)}=O(\lambda^{-q}),\qquad q>1/2,
\]

where `η` measures alignment between the certified lowest spectral vector and
the candidate model.  A proof must not import global Weil positivity or any
statement equivalent to RH.
