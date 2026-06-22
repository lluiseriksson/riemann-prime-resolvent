# One-Point Resolvent–Hausdorff Programme

[![Lean CI](https://github.com/lluiseriksson/riemann-one-point-resolvent/actions/workflows/ci.yml/badge.svg)](https://github.com/lluiseriksson/riemann-one-point-resolvent/actions/workflows/ci.yml)
[![Paper](https://img.shields.io/badge/paper-PDF-blue)](paper/one_point_resolvent_hausdorff.pdf)
[![License: Apache-2.0](https://img.shields.io/badge/code-Apache--2.0-green.svg)](LICENSE)
[![Paper: CC BY 4.0](https://img.shields.io/badge/paper-CC%20BY%204.0-lightgrey.svg)](paper/LICENSE)

A publication-oriented research repository for a **one-point resolvent–Hausdorff criterion** associated with the Riemann \(\Xi\)-function.

> **Status:** this repository does **not** claim a proof of the Riemann hypothesis. It separates a rigorous abstract reduction from the genuinely open spectral-convergence problem.

## Mathematical core

For \(x>1/4\), set

\[
\mathcal S_\Xi(x)=\frac{1}{2\sqrt{x}}\frac{\xi'}{\xi}\!\left(\frac12+\sqrt{x}\right).
\]

Fix \(x_0>1/4\) and define

\[
b_n(x_0)=x_0^n\frac{(-1)^n}{n!}\,\mathcal S_\Xi^{(n)}(x_0).
\]

The paper proves the abstract equivalence

\[
\mathrm{RH}
\iff
\{b_n(x_0)\}_{n\ge 0}\text{ is a Hausdorff moment sequence on }[0,1],
\]

and connects it to:

- signed finite differences \((-1)^k\Delta^k b_n\ge0\);
- finite Hankel and localizing certificates;
- the compactifying map \(\lambda\mapsto x_0/(\lambda+x_0)\);
- squared-resolvent traces \(\tfrac12\operatorname{Tr}(D^2+xI)^{-1}\);
- an explicit prime-side target and elementary prime-tail bound.

The **Lean 4 source encodes the finite algebraic layer**, with compilation and axiom audit enforced by CI: finite atomic moments, signed Hausdorff differences, resolvent compactification, positive Gram/localizing certificates, and deterministic error-budget glue. The complex-analytic criterion is stated and proved in the paper but remains on the formalization roadmap.

## Repository map

```text
PrimeResolvent/                 Lean 4 finite verified core
paper/                          LaTeX source, bibliography, figures, PDF
scripts/                        numerical, exact-certificate, release tools
tests/                          Python regression tests
data/                           generated reproducibility data
docs/                           claims, roadmap, Lean map, publication gate
.github/workflows/              Lean, Python, and paper CI
```

## Quick start

```bash
git clone https://github.com/lluiseriksson/riemann-one-point-resolvent.git
cd riemann-one-point-resolvent

lake exe cache get
lake build
lake env lean PrimeResolvent/Oracle.lean

python3 -m pip install -r requirements.txt
python3 -m pytest -q
python3 scripts/numerical_demo.py --output-dir data/demo
python3 scripts/exact_atomic_certificate.py --output-dir data/certificates

make paper
```

Or run the complete audit:

```bash
./scripts/verify.sh
```

## Reproducibility policy

The CI must fail on project `sorry`, `admit`, or declarations of new project axioms. Headline Lean theorems are audited through `#print axioms`. Numerical output is evidence and regression data only; it is never promoted to a theorem without a certificate checked by Lean.

See [MATHEMATICAL_STATUS.md](docs/MATHEMATICAL_STATUS.md), [PUBLICATION_GATE.md](docs/PUBLICATION_GATE.md), and [REPRODUCIBILITY.md](docs/REPRODUCIBILITY.md).

## Citation

Use [CITATION.cff](CITATION.cff). The current artifact version is **0.2.0**.
