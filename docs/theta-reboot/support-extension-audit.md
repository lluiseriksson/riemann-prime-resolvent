# Support-extension audit beyond \(a=2/5\)

## Purpose

The interval certificate at \(a=2/5\) crosses the first arithmetic threshold
\(2a=\log 2\). It does not supply a uniform lower bound as \(a\) grows. This
note records the first attempted extension before any additional large Arb
calculation is authorized.

Suzuki proves unconditionally that the lowest localized eigenvalue is positive
for *sufficiently small* \(a\), but does not provide a numerical endpoint in
Theorem 1.4. The certified value \(a=2/5\) is therefore a concrete quantitative
support result, not a restatement of that asymptotic theorem.

## Direct finite-section scan

The following 192-mode values are diagnostics, not enclosures:

| \(a\) | lowest even | lowest odd |
|---:|---:|---:|
| 0.40 | \(1.8129\cdot10^{-4}\) | \(1.4707\cdot10^{-2}\) |
| 0.42 | \(7.4243\cdot10^{-5}\) | \(7.5731\cdot10^{-3}\) |
| 0.44 | \(2.7569\cdot10^{-5}\) | \(3.6128\cdot10^{-3}\) |
| 0.46 | \(9.2349\cdot10^{-6}\) | \(1.5549\cdot10^{-3}\) |
| 0.48 | \(2.8784\cdot10^{-6}\) | \(5.8750\cdot10^{-4}\) |
| 0.50 | \(9.3354\cdot10^{-7}\) | \(1.9376\cdot10^{-4}\) |

No crossing is observed. Both relevant scales decay rapidly, however, so the
fixed floor \(\beta=0.005\) used at \(a=0.4\) cannot be transported to
\(a=0.5\).

## Two failed extensions and what they measure

At \(a=0.5\), the perturbation lower bound requires the diagonal Schur tail to
start after mode 168. Reusing 88 modes makes some tail denominators negative
and is invalid. With 256 or more low modes the spurious extra directions
disappear, but the actual odd eigenvalue is only about
\(1.94\cdot10^{-4}\). A Temple proof must therefore resolve a residual of
order \(10^{-5}\), rather than the \(10^{-3}\) scale available at \(a=0.4\).

At \(a=0.42\), a 512-mode trial with \(\beta=0.003\) initially failed only
because all residual pieces were added by a triangle inequality. The finite
range \([d,N)\) and tail \([N,\infty)\) are orthogonal Legendre blocks. The
valid improved budget

\[
 \varepsilon\le
 \sqrt{\|r_{<d}\|^2+
 \left(\sqrt{\|r_{d:N}\|^2+\|r_{N:\infty}\|^2}
       +\|r_{\rm smooth,\ge d}\|\right)^2}
\]

changes the descriptive Temple lower bound at \(a=0.42\) from negative to
\(1.91\cdot10^{-5}\). This is useful but does not yet certify the second
spectral floor: the diagonal-tail Schur correction remains too coarse.

Subtracting more endpoint Taylor jets does not solve that second obstruction.
For 192 low modes, the seventh-derivative variation is already of order
\(10^{25}\). Orders 28--32 eventually control the continuous remainder, but
the leading step tail still decays only as \(N^{-1/2}\), and the explicit
finite-rank correction grows in rank. Increasing derivative order without a
new representation is therefore a conditioning exchange, not a uniform
argument.

## Consequence for the RH programme

The localized theorem is robust, but the current proof architecture is not
uniform in support. A genuine next step must replace at least one of:

1. the scalar high-block lower bound \(H_n-\mathrm{loss}\) by a
   mode-sensitive positive comparison retaining the logarithmic boundary
   potential;
2. the endpoint Taylor decomposition by a basis adapted to the internal
   translation cut, so that the \(N^{-1/2}\) jump is represented exactly in
   the infinite Schur complement;
3. the fixed positive gap in Temple by a two-dimensional eigenvalue inclusion
   that certifies the ground state and first odd state simultaneously.

Repeating the \(a=0.4\) calculation at denser grids without one of these
changes is not an RH strategy.

## Update: the staircase certificate at \(a=0.42\)

The first two obstructions above can nevertheless be overcome at the single
support \(a=0.42\) by using parity-specific floors and larger low blocks.
An odd Schur certificate at shift \(0.5\), followed by an odd Temple bound,
gives \(\lambda_1^{\rm odd}>0.0075459987\).  An independent even Schur
certificate at shift \(0.1\), followed by an even Temple bound, gives
\(\lambda_1^{\rm even}>0.0000711722\).  See the
[full certificate](support-042-certificate.md).

This repairs the particular \(a=0.42\) failure recorded above, but not the
uniform-support objection: the dimensions, number of endpoint jets, spectral
floors, and residual tolerances were all changed for this support.  The three
structural alternatives remain the next proof targets.
