# Reviewer guide

A reviewer can audit the artifact in four passes.

## Pass 1 — claim boundary

Read `STATUS.md`, `docs/MATHEMATICAL_STATUS.md`, and the red status box on page 1 of the paper. Confirm that no text claims RH or concrete spectral convergence.

## Pass 2 — mathematics

Check, in order:

1. the sign in the identity relating `-Xi'(iy)/Xi(iy)` to `xi'/xi(1/2+y)`;
2. the image of the upper half-plane under `z -> -z^2`;
3. the pole contradiction at a non-real zero;
4. the scaling `b_n = x0^n (-1)^n S^(n)(x0)/n!`;
5. the singular set of the reconstructed integral extension;
6. the prime-tail constants.

## Pass 3 — formal artifact

```bash
lake exe cache get
lake build
lake env lean PrimeResolvent/Oracle.lean
python3 scripts/check_no_placeholders.py
python3 scripts/static_lean_sanity.py
```

The static script is not a substitute for Lean; it is only a quick failure detector.

## Pass 4 — reproducibility

```bash
python3 -m pytest -q
python3 scripts/exact_atomic_certificate.py --output-dir data/certificates
python3 scripts/numerical_demo.py --output-dir data/demo
./scripts/build_paper.sh
python3 scripts/generate_manifest.py
python3 scripts/check_release.py
```

Compare `SHA256SUMS`, inspect the figures, and verify that generated data is labelled non-probative.
