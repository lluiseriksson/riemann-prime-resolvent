# Next session

## Mandatory first action

Run `./scripts/verify.sh` on the pinned environment. Fix only compatibility
errors. Do not change the theorem scope during the first build pass.

## First mathematical target

Prove the project Xi functional equation and evenness:

```lean
theorem riemannXiS_one_sub (s : ℂ) :
    riemannXiS (1 - s) = riemannXiS s := by
  ...

theorem riemannXi_neg (z : ℂ) :
    riemannXi (-z) = riemannXi z := by
  ...
```

Use `completedRiemannZeta₀_one_sub` and ring normalization. Add both to the
axiom oracle.

## Second target

Prove the geometry lemma mapping the upper half-plane into `slitPlane`.

## Research audit target

Read the full source of arXiv:2511.22755 and record exact equation numbers for:

- the candidate/prolate function;
- support and transform convention;
- approximation norm and constants;
- lowest-state comparison explicitly left open by the authors.

Do not promote the candidate strip/rate calculation before this audit.
