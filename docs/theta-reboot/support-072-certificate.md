# Certified localized positivity through support 0.72

## Theorem and scope

For Suzuki's localized Weil operator in the conventions fixed by this
repository, interval arithmetic now proves

\[
 \boxed{A_{0.72}\succeq
 9.86850102990163\cdot10^{-17}I>0}.
\]

Extension by zero of the test space therefore gives

\[
 \lambda_a>0\qquad(0<a\le0.72).
\]

This is an unconditional bounded-support theorem. It is not RH: Suzuki's
criterion requires nonnegativity for every support radius.

## Why the former calculation did not close

The first support-0.72 run charged the whole degree band
\(12\le n<176\) against the single complement denominator \(d_{12}\).
That comparison produced five negative directions even though the finite
source matrix remained positive. The failure belonged to the comparison,
not to the operator.

Let \(P_j\) be the orthogonal projections onto degree bands beginning at
\(m_j\). The complement form satisfies

\[
 D\succeq\sum_j d_{m_j}P_j,
 \qquad
 D^{-1}\preceq\sum_j d_{m_j}^{-1}P_j.
\]

Hence the source correction is bounded by

\[
 BD^{-1}B^*\preceq
 \sum_j d_{m_j}^{-1}(BP_j)(BP_j)^*.
\]

The successful split is only

\[
 [12,16),\qquad[16,176),\qquad[176,\infty),
\]

with certified denominators

\[
 d_{12}\ge0.2209732158977950,
 \quad d_{16}\ge0.4984915309161100,
 \quad d_{176}\ge2.8683004164715744.
\]

The second finite Gram is obtained as an **Arb interval subtraction** of the
registered \([12,16)\) Gram from the independently enclosed aggregate
\([12,176)\) Gram. No subtraction of midpoint-only floating matrices is used.

## Certified output

| sector | negative | positive | unresolved | Schur lower | full coercive lower |
|---|---:|---:|---:|---:|---:|
| even | 0 | 78 | 0 | `2.5975024696255643e-14` | `9.86850102990163e-17` |
| odd | 0 | 78 | 0 | `4.3738281652034125e-11` | `1.655088623229461e-13` |

Both sectors use `congruence-gershgorin`. A floating midpoint eigenbasis is
only a proposal. Arb then proves that its Gram matrix is positive, hence the
change of basis is invertible, and that the congruent Schur interval is
strictly Gershgorin positive. The bound is transported back using an Arb
upper bound for the squared norm of the change of basis. Thus no unverified
floating eigenvalue supplies the sign.

## Reproduction and hashes

The support-dependent aggregate component cache has SHA-256

```text
c5cff9fba1684a5822e1544a2a96f91aa843d9b0074e239df6e81a51875ecad4
```

The independently generated \([12,16)\) band artifact has SHA-256

```text
cd023221e138c3a6110202f0adec84364ea659f3061c1cc3638d658fb9d78836
```

and was built with

```powershell
python -m experiments.theta_pencil.run_arb_third_window_near_tail_checkpointed `
  --half-width 0.72 --degree 12 --boundaries 12 16 `
  --precision 512 --maximum-smooth-power 47 `
  --cross-map-cache-dir theta-cross-maps `
  --output theta-near-band-a072-d12-12-16-p512.npz
```

The cross-map directory is a resumable performance cache. Each smooth or
Legendre--\(Q\) matrix is stored as parseable Arb balls with exact metadata;
a mismatch cannot be silently reused.

The final JSON output has SHA-256

```text
ac469626e37a70ab5c4ac4dce0a157254bb7dbc4c5eccfdc62ef8a4acc97afe0
```

and is reproduced from the two component artifacts by

```powershell
python -m experiments.theta_pencil.third_window_multiband_schur_certificate `
  --component-cache theta-schur-a072-d12-p47-tail8192.npz `
  --band-cache theta-near-band-a072-d12-12-16-p512.npz `
  --output theta-schur-a072-multiband-12-16-176.json
```

As before, the caches are performance artifacts rather than axioms: every
entry has a source-level Arb generator, and all proof parameters are checked
on load.

## Remaining global gate

This advances the unconditional frontier from \(0.7\) to \(0.72\), but an
unbounded sequence of isolated certificates cannot prove RH. The next
mathematical target remains a support-uniform stratification law, with
constants that survive the entry of further prime-power translations.
