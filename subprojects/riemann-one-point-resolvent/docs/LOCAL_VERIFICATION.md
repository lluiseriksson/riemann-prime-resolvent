# Local verification record

Construction environment audit completed on **2026-06-22 UTC**.

| Check | Result |
|---|---|
| Lean placeholder/project-axiom scan | Passed |
| Static Lean delimiter/import/declaration sanity | Passed; 25 declarations scanned |
| Python regression tests | Passed; 4 tests |
| Exact rational certificate generation | Passed |
| Numerical demonstration | Passed |
| LaTeX paper build | Passed; 12 pages |
| PDF preflight | Passed; openable, unencrypted, text PDF |
| PDF visual render inspection | Passed on title, theorem/figure, and references pages |
| Lean compiler build | **Not run locally:** Lean/Lake absent from this container |

The Lean toolchain is pinned to `leanprover/lean4:v4.31.0`; GitHub Actions makes `lake build` and `lake env lean PrimeResolvent/Oracle.lean` mandatory. The absence of a local Lean compiler is therefore recorded as an outstanding CI check rather than reported as success.

See `logs/verification.log` for the executed local commands and outputs.
