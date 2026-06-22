# Certified finite experiments

Exploratory notebooks and floating-point plots must not be treated as proof
artifacts. The accepted trust path is:

```text
external interval computation
    -> JSON certificate
    -> deterministic structural checker
    -> Lean rational theorem
    -> finite-to-infinite analytic theorem
```

## Demo

```bash
python3 scripts/validate_certificate.py \
  experiments/examples/demo_exact_rational.json
```

The bundled demo is deliberately trivial and unrelated to zeta zeros. The
checker recomputes its finite half squared-resolvent trace exactly over the
rationals; this tests the certificate format, not any infinite-dimensional claim.

See `docs/NUMERICAL-CERTIFICATION.md` for the future concrete data requirements.
