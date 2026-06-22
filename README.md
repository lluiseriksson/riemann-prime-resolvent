# Riemann Prime–Resolvent Lean 4 Programme

> **Status:** research seed repository; no proof of the Riemann hypothesis is claimed.

This repository turns a spectral/Stieltjes strategy into a reproducible Lean 4
research programme. Its intended long-term endpoint is a theorem of the form

\[
\text{prime--resolvent convergence}
\Longrightarrow
\text{holomorphic Stieltjes extension}
\Longrightarrow
\text{all zeros of }\Xi\text{ are real}.
\]

The seed release already contains a small, axiom-free Lean core for the safe
algebraic bookkeeping: the three-part error budget, finite positive Stieltjes
models, scalar spectral-defect quantities, and rate optimization.  The hard
analytic and operator-theoretic statements are represented as named
**propositions and publication gates**, not as axioms.

## Start here

```bash
./scripts/bootstrap.sh
./scripts/verify.sh
```

For a new coding or research agent, read in this order:

1. `AGENT-ONBOARDING.md`
2. `RESEARCH-STATUS.md`
3. `docs/MATHEMATICAL-DEVELOPMENT.md`
4. `docs/THEOREM-LEDGER.md`
5. `docs/LEAN-ROADMAP.md`
6. `PUBLICATION-GATE.md`

A copy-paste task prompt is available in `HANDOFF-PROMPT.md`.

## Honest scope

The source papers propose self-adjoint spectral approximants built from primes
up to \(\lambda^2\), report striking numerical agreement with low Riemann
zeros, and state that a rigorous convergence proof would imply RH.  This repo
does **not** silently assume that convergence.  The central missing quantity is
a quantitative comparison between the concrete lowest spectral state and the
candidate/prolate model.

The proposed decomposition is

\[
E_{\lambda,N}
\le E_{\mathrm{spectral}}+E_{\mathrm{model}}+E_{\mathrm{prime}}.
\]

The current Lean files verify only generic consequences of such a decomposition.

## Repository policy

- No `sorry`, `admit`, or project `axiom` declarations in Lean sources.
- Every headline claim appears in `docs/SOURCE-CLAIM-AUDIT.md`.
- Conjectural calculations are labelled `CANDIDATE`, never `THEOREM`.
- A public paper is gated by `PUBLICATION-GATE.md`.
- Numerical work must export interval/rational certificates that Lean can check.

## Pinned environment

- Lean: `v4.29.0-rc6`
- Mathlib commit: `07642720480157414db592fa85b626dafb71355b`

The pin is inherited from the supplied reproducible Lean project so an agent can
reuse the same toolchain and cache.

## Language

The formal source and paper draft are in English.  Spanish launch instructions
are in `INSTRUCCIONES-AGENTE.md`.
