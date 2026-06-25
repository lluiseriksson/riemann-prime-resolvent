# Lean map

| Module | Verified content |
|---|---|
| `OnePointResolvent.Basic` | finite atomic moments, recursive signed differences and complete-monotonicity predicate |
| `OnePointResolvent.HausdorffFinite` | exact finite difference formula and positivity on `[0,1]` |
| `OnePointResolvent.ResolventCompactification` | positive weights and compactified points in `[0,1]` |
| `OnePointResolvent.StieltjesLocalBound` | abstract denominator-consumer API plus the factor-two finite-disk theorem |
| `OnePointResolvent.StieltjesCompactBound` | compactification identity, positive minimum on compact slit-plane sets and cutoff-uniform compact bounds |
| `OnePointResolvent.StieltjesResolventBridge` | exact identification of finite positive sums with Mathlib's `resolventTransform` under `a = -z` |
| `OnePointResolvent.CompactifiedMeasure` | exact one-point mass, `[0,1]` support, common-family compactness and compact weak closure of indexed approximants |
| `OnePointResolvent.FiniteCertificates` | finite Hankel/localizing sum-of-squares nonnegativity |
| `OnePointResolvent.ErrorBudget` | three-stage triangle inequality |
| `OnePointResolvent.Examples` | exact finite toy consequences |
| `OnePointResolvent.Oracle` | `#print axioms` audit entry point |

## Namespace migration

Version 0.2 used the misleading namespace and directory `PrimeResolvent`. Version 0.3 canonicalizes the library as `OnePointResolvent`, leaving prime/operator construction to the companion repository. This is an intentional source-level breaking change.

## What is absent on purpose

There is no theorem named “Riemann hypothesis” whose proof is an open assumption, no structure field disguising the missing convergence theorem, and no analytic statement promoted merely because it has a complete prose proof. Compact local boundedness, finite-measure compactness and weak relative compactness are now verified; kernel integration against a limit, compact-open extraction, interval uniqueness and identification of the limiting target remain separate obligations.
