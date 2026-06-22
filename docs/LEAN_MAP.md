# Lean 4 theorem map

| Module | Main declarations | Role |
|---|---|---|
| `Basic.lean` | `atomicMoment`, `hausdorffDiff`, `IsHausdorffCompletelyMonotone` | Definitions |
| `HausdorffFinite.lean` | `hausdorffDiff_atomicMoment`, `atomicMoment_isHausdorffCompletelyMonotone` | Exact finite identity and positivity |
| `ResolventCompactification.lean` | `resolventWeight`, `compactifiedPoint`, `finiteResolventMoment_isHausdorffCompletelyMonotone` | Spectral-to-Hausdorff bridge |
| `FiniteCertificates.lean` | `atomicHankelCertificate_nonneg`, `atomicLocalizingCertificate_nonneg` | Finite PSD/SOS certificates |
| `ErrorBudget.lean` | `primeResolvent_errorBudget` | Three-error comparison glue |
| `Examples.lean` | `demoSpectrum` examples | Exact regression examples |
| `Oracle.lean` | `#print axioms ...` | Kernel dependency audit |

## Planned analytic modules

```text
PrimeResolvent/Xi.lean
PrimeResolvent/SlitPlane.lean
PrimeResolvent/LogDerivative.lean
PrimeResolvent/HausdorffInfinite.lean
PrimeResolvent/PrimeTail.lean
PrimeResolvent/NormalFamily.lean
PrimeResolvent/SpectralCriterion.lean
PrimeResolvent/CertifiedMatrix.lean
```

The publication gate forbids presenting these planned modules as completed work.
