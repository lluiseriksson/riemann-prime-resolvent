# Exact certificate format

`data/certificates/exact_atomic_certificate.json` is generated with rational arithmetic. It records:

- base point `x0`;
- finite nonnegative squared spectrum;
- resolvent weights and compactified points;
- exact rational moments;
- a rectangular family of signed finite differences;
- exact Hankel and localizing matrices;
- exact leading principal minors and ranks.

The current JSON is a toy regression certificate. A future spectral certificate must additionally contain matrix provenance, Hermitian checks, residual bounds, spectral separation, interval trace bounds, and a theorem connecting the finite matrix to the infinite operator.
