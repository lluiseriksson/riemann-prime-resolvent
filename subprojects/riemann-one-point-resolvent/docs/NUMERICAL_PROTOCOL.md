# Numerical protocol

Numerical scripts serve three purposes only:

1. test signs and normalization conventions;
2. produce deterministic documentation figures;
3. exercise certificate and release pipelines.

They do not establish infinite Hausdorff positivity or spectral convergence.

## Exact certificates

`exact_atomic_certificate.py` uses rational arithmetic for a finite toy spectrum. The verifier recomputes compactified points, moments, signed differences, Hankel and localizing matrices. Exact toy certificates validate code paths and finite theorems only.

## Floating-point figures

The figures show finite resolvent moments, compactification and finite signed differences. Generated CSV data accompany the images. Any future interval-arithmetic claim must state precision, rounding mode, external library versions and a machine-checkable enclosure format.
