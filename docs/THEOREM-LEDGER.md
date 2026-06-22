# Theorem ledger

Status codes:

- `LEAN`: complete Lean proof intended to compile;
- `PAPER`: full conventional proof written, Lean pending;
- `CANDIDATE`: requires independent checking/source audit;
- `OPEN`: missing;
- `BLOCKED`: depends on a prior open theorem.

| ID | Statement | Status | Lean declaration / next action |
|---|---|---:|---|
| L001 | Three-step scalar triangle inequality | LEAN | `three_step_triangle` |
| L002 | Error bounded by three-component budget | LEAN | `error_le_budget` |
| L003 | Component limits imply total-budget limit | LEAN | `ErrorBudget.tendsto_total_zero` |
| L004 | Finite Stieltjes transform is nonnegative | LEAN | `finiteStieltjes_nonneg` |
| L005 | Finite squared resolvent is nonnegative | LEAN | `finiteSquaredResolvent_nonneg` |
| L006 | Paired-spectrum `1/2` normalization | LEAN | `half_finitePairedTrace` |
| L007 | Closed-form prime-tail majorant nonnegative | LEAN | `primeTailMajorant_nonneg` |
| L008 | Rayleigh/gap scalar defect nonnegative | LEAN | `rayleighGapDefect_nonneg` |
| L009 | Residual/gap scalar defect nonnegative | LEAN | `residualGapDefect_nonneg` |
| L010 | Proposed rate positive iff `q>1/2` (sufficient direction) | LEAN | `rateExponent_pos` |
| X001 | Project `riemannXiS` equals conventional `xi` | OPEN | unfold Mathlib completed-zeta identity |
| X002 | Functional equation `riemannXiS (1-s)=riemannXiS s` | OPEN | use `completedRiemannZeta₀_one_sub` |
| X003 | Evenness `riemannXi (-z)=riemannXi z` | BLOCKED | X002 |
| X004 | `XiOnlyRealZeros -> RiemannHypothesis` | OPEN | analyze trivial/nontrivial zero factors |
| S001 | `-z^2` maps upper half-plane to `slitPlane` | PAPER | formalize complex real/imag algebra |
| S002 | Log derivative has a nonremovable pole at a zero | PAPER | use analytic local factorization/order API |
| S003 | Upper half-plane minus discrete zeros connected | OPEN | seek Mathlib theorem or prove path connectedness |
| S004 | Slit-plane extension implies `XiOnlyRealZeros` | PAPER | combine S001–S003 and identity theorem |
| T001 | One-point bound gives local boundedness of Stieltjes family | PAPER | measure/integral inequality |
| T002 | Normal-family subsequence on slit plane | OPEN | Montel infrastructure likely missing |
| T003 | Stieltjes interval convergence implies slit-plane extension | BLOCKED | T001–T002 |
| P001 | `Lambda(n) <= log n` in the needed form | OPEN | locate existing von Mangoldt API or define it |
| P002 | Discrete tail bounded by decreasing integral | PAPER | formalize cutoff `X>=3` |
| P003 | Explicit von Mangoldt tail bound | BLOCKED | P001–P002 |
| P004 | Prime-side formula for `S_Xi` on `sigma>1` | OPEN | zeta log derivative + Gamma/digamma API |
| H001 | Finite Hermitian Rayleigh/gap alignment theorem | PAPER | matrix/inner-product proof |
| H002 | Residual/separation certificate theorem | CANDIDATE | exact Davis–Kahan/Kato statement and constants |
| H003 | Galerkin tail to transform error | CANDIDATE | exact transform convention required |
| C001 | Concrete quadratic form/operator in Lean | OPEN | source transcription and domains |
| C002 | Lower-bounded self-adjoint realization | OPEN | unbounded-operator infrastructure |
| C003 | Simple isolated even lowest eigenstate | OPEN | major mathematical frontier |
| C004 | Squared resolvent is trace class | OPEN | trace ideal infrastructure absent |
| C005 | Prime–resolvent convergence | BLOCKED | C001–C004 plus rate theorem |
| R001 | Candidate prolate/model strip enlargement | CANDIDATE | source audit before any theorem claim |
| R002 | Optimized `rho(q)` is the true total rate | CANDIDATE | depends on R001 and explicit constants |

## Rule for updating

When an item becomes `LEAN`, add it to `oracle_check.lean`, run
`./scripts/verify.sh`, and record the exact commit in `verification/LEDGER.md`.
