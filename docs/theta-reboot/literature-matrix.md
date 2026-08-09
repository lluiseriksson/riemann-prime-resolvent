# Primary-literature matrix

## Selection rule

Only primary papers are used to define mathematical inputs. A paper is scored
by the new object it constructs, the exact theorem it proves, and the remaining
obligation. Numerical agreement and reformulations equivalent to RH receive no
credit as a discharged implication.

| Source | Unconditional content used here | Remaining obstruction | Decision |
|---|---|---|---|
| [Hedenmalm, *Spectral interpretation of Riemann zeta zeros* (2026)](https://arxiv.org/abs/2606.17494) | An explicit theta density and a second-order boundary-value pencil whose admissible eigenvalues are exactly the zeros of \(\Xi\); real and complex parameters are both treated. | Construct a positive sesquilinear form making the operator pair self-adjoint and nondegenerate. | **Audited and narrowed.** Local metrics and bounded ambient metrics are ruled out below; only singular or restricted-domain forms survive. |
| [Connes, Consani, Moscovici, *Zeta Spectral Triples* (2025)](https://arxiv.org/abs/2511.22755) | Prime-cutoff self-adjoint finite operators and strong numerical spectral agreement. | Rigorous convergence of the spectra or normalized determinants to the true \(\Xi\) data. | Retain as a comparison and possible discretization of TP-M; do not reuse convergence as an assumption. |
| [Connes and van Suijlekom, *Quadratic Forms, Real Zeros and Echoes of the Spectral Action* (2025)](https://arxiv.org/abs/2511.23257) | A real-zero theorem for the Fourier transform of a simple isolated even ground state of a lower-bounded self-adjoint convolution form. | Construct the required form and prove ground-state simplicity for the Riemann kernel. | Use its Toeplitz and quadratic-form mechanism as a candidate source for the nonlocal metric. |
| [Connes and Consani, *Weil positivity and Trace formula, the archimedean place* (2020)](https://arxiv.org/abs/2006.13771) | Operator-theoretic positivity at the archimedean place, with prolate projections and explicit trace identities. | The semilocal finite-place positivity that is equivalent to the full Weil criterion. | **Active input.** Start with the first source-faithful arithmetic support window; never promote the archimedean result to global positivity. |
| [Connes and Consani, *The Scaling Hamiltonian* (2019)](https://arxiv.org/abs/1910.14368) | Exact semilocal trace identity, the two Weil constraints, and a support-indexed finite-place conjecture; it also proves why the naive inner-function/compression argument fails. | Prove the support-restricted semilocal inequality; the first window with a finite-prime value already has \(S_q=\{\infty,2,3\}\). | **Equation-level target extracted.** Work with the restricted quadratic form, not pointwise local signs. |
| [Connes, Consani, Moscovici, *On q-series and the moment problem associated to local factors* (2024)](https://arxiv.org/abs/2403.01247) | For \(S=\{\infty,p\}\), a determinate positive moment problem, exact Lambert-series moments, Jacobi matrices, rank-one expansions, and Catalan/integrality structure. | Its positive local-factor measure is not the signed Weil form and does not encode the zeros of \(\Xi\). | **Implementation scaffold.** Use the \(p=2\) Jacobi basis to discretize and falsify the restricted Weil form. |
| [Burnol, *Two complete and minimal systems associated with the zeros of the Riemann zeta function* (2002)](https://arxiv.org/abs/math/0203120) | Sonine/de Branges Hilbert-space systems attached to zeta zeros. | Completeness and spectral realization do not themselves force all zeros to be real. | Use for domain and model-space comparisons. |
| [Alouges, Darses, Hillion, *Polynomial approximations in a generalized Nyman-Beurling criterion* (2020)](https://arxiv.org/abs/2006.02953) | An unconditional approximation component and structured Gram matrices in a generalized Nyman-Beurling setting. | Coefficient control contains the hard zero-free information. | Baseline for detecting when a metric construction merely relocates RH into a Gram bound. |
| [Rodgers and Tao, *The De Bruijn-Newman constant is non-negative* (2018)](https://arxiv.org/abs/1801.05914) | The complementary inequality \(\Lambda\ge 0\) and a dynamical description of zero motion under heat flow. | RH is the opposite inequality \(\Lambda\le0\). | Negative control: heat smoothing alone points in the wrong logical direction. |
| [Griffin et al., *Jensen Polynomials for the Riemann Xi Function* (2019)](https://arxiv.org/abs/1910.01227) | Effective eventual hyperbolicity for fixed-degree Jensen polynomials and finite-degree information. | Uniform hyperbolicity over every degree and shift remains equivalent to RH. | Use only as an asymptotic diagnostic, not as the main route. |

## Comparative conclusion

The theta-pencil was the right first audit because it begins with an exact
boundary-value characterization rather than a fitted spectrum. That audit also
exposes a global metric obstruction: the natural ambient Hilbert-space class is
empty. The active construction track is therefore semilocal Weil positivity,
beginning with one finite prime. CCM and Connes--van Suijlekom remain useful
finite operator models. Nyman--Beurling, Hausdorff moments, and Jensen
polynomials remain anti-circularity comparators: if the semilocal construction
merely renames their unresolved global positivity, the track has not advanced.

## Source-fidelity requirements

1. The normalization of \(\Xi\), the logarithmic coordinate, and the Fourier
   convention must be recorded beside every derived formula.
2. The real-parameter theorem and complex-parameter theorem in Hedenmalm must
   not be conflated; RH needs exclusion of the complex branch.
3. A metric defined using a basis indexed by the zeros is circular, even if it
   is positive by construction.
4. A finite positive matrix is evidence only for the registered discretization
   and parameter range.
