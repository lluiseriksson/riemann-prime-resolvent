# Numerical certification

The `experiments/` tree contains exact structural certificates and schemas. Floating-point plots test conventions and regressions; they are not evidence of infinite spectral convergence.

A promoted certificate must record exact inputs, versioned generation code, deterministic verification, interval/rational enclosures and a statement of the theorem it certifies. The verifier must not trust values merely because they appear in the certificate file.
