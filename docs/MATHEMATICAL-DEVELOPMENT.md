# Mathematical development

## 0. Epistemic labels

This note uses four labels:

- **PROVED-ABSTRACTLY:** a complete conventional proof is supplied here;
- **LEAN-SEED:** a corresponding elementary theorem is already encoded;
- **CANDIDATE:** a derivation is plausible but still needs source/convention audit;
- **OPEN:** the argument is missing.

Nothing in this note proves the Riemann hypothesis.

---

## 1. Critical-line coordinate

Let

\[
\xi(s)=\frac12s(s-1)\pi^{-s/2}\Gamma(s/2)\zeta(s),
\qquad
\Xi(z)=\xi\!\left(\frac12+iz\right).
\]

Then `RH` is equivalent to every zero of `Xi` being real.  Mathlib already
contains `riemannZeta`, `completedRiemannZeta₀`, its functional equation, and a
formal proposition `RiemannHypothesis`.  The project definition

\[
\xi(s)=\frac{s(s-1)\Lambda_0(s)+1}{2}
\]

uses the identity between the pole-removed completed zeta `Λ₀` and the usual
completed zeta.  Formalizing the exact equivalence with Mathlib is the first
number-theoretic milestone.

**Status:** definition in Lean; equivalence OPEN.

---

## 2. The target resolvent observable

For `x > 1/4`, define

\[
\mathcal S_\Xi(x)
 = \frac{1}{2\sqrt{x}}
   \frac{\xi'}{\xi}\!\left(\frac12+\sqrt{x}\right).
\]

The point `sigma = 1/2 + sqrt(x)` lies in `Re(s)>1`, where the Euler product is
absolutely convergent and nonzero.

Under RH, writing the positive zeros of `Xi` as `gamma_k`, the even Hadamard
product suggests

\[
\mathcal S_\Xi(x)=\sum_{k\ge1}\frac{1}{\gamma_k^2+x}.
\]

This is a Stieltjes transform of the positive measure

\[
\nu=\sum_{k\ge1}\delta_{\gamma_k^2}.
\]

A publication proof must check the canonical-product normalization and
multiplicities explicitly.  The project does not rely on this identity for the
one-way extension criterion below.

**Status:** under-RH representation CANDIDATE until canonical-product details
are audited; finite analogues LEAN-SEED.

---

## 3. Slit-plane extension criterion

Let

\[
\Omega=\mathbb C\setminus(-\infty,0].
\]

### Proposed theorem A

Assume there exists a holomorphic function `S : Omega -> C` such that on a
nonempty open interval `I subset (1/4,infinity)`,

\[
S(x)=\mathcal S_\Xi(x).
\]

Then every zero of `Xi` is real.

### Proof (PROVED-ABSTRACTLY, pending Lean encoding)

For `Im(z)>0`, set

\[
M(z)=2zS(-z^2).
\]

The map `z -> -z^2` sends the open upper half-plane into `Omega`: if `Re(z)=0`,
then `-z^2` is positive real; otherwise its imaginary part is nonzero.

For `z=iy` with `y^2 in I`, use the functional equation `xi(s)=xi(1-s)` and its
derivative to obtain

\[
M(iy)=i\frac{\xi'}{\xi}\!\left(\frac12+y\right)
      =-\frac{\Xi'(iy)}{\Xi(iy)}.
\]

The upper half-plane minus the discrete zero set of `Xi` is connected.  By the
identity theorem,

\[
M(z)=-\frac{\Xi'(z)}{\Xi(z)}
\]

away from those zeros.  If `z_0` were a zero of multiplicity `m>0`, local
factorization gives

\[
-\frac{\Xi'(z)}{\Xi(z)}=-\frac{m}{z-z_0}+h(z),
\]

which has a pole, whereas `M` is holomorphic.  Contradiction.  Conjugation
symmetry excludes lower-half-plane zeros.

### Lean decomposition

1. prove `-z^2 in slitPlane` for `0 < z.im`;
2. formalize the local factorization/log-derivative pole lemma;
3. prove connectedness of the upper half-plane minus a discrete set, or avoid a
   global connectedness theorem by analytic continuation along polygonal paths;
4. apply identity and removable-singularity arguments;
5. connect `XiOnlyRealZeros` to `RiemannHypothesis`.

**Status:** PAPER-PROVED / Lean OPEN.

---

## 4. Compactness of positive spectral approximants

Let `nu_j` be positive measures on `[0,infinity)` and

\[
S_j(w)=\int_0^\infty\frac{d\nu_j(t)}{t+w},
\qquad w\in\Omega.
\]

Suppose for one `x_0>0`,

\[
\sup_j S_j(x_0)<\infty.
\]

For every compact `K subset Omega`, there is `C_K` such that

\[
\frac1{|t+w|}\le \frac{C_K}{t+x_0}
\]

for all `t>=0` and `w in K`.  Consequently the family is locally bounded, hence
normal by Montel.  If `S_j(x)` converges to `S_Xi(x)` on a nonempty interval,
any compact-open subsequential limit supplies the extension required by theorem
A.

### Proposed theorem B

One-point Stieltjes control plus pointwise convergence on a real interval
implies RH.

### Important subtlety

For a finite or discrete spectral model, positive measures are automatic only
after proving:

- the operator is self-adjoint;
- the relevant spectrum is real;
- the chosen normalization counts multiplicities correctly;
- the squared resolvent is trace class in the infinite model.

**Status:** PAPER-PROVED at abstract measure level / Lean OPEN.

---

## 5. Prime side and explicit tail

For `sigma>1`,

\[
\frac{\xi'}{\xi}(\sigma)
 =\frac1\sigma+\frac1{\sigma-1}
  -\frac12\log\pi
  +\frac12\psi(\sigma/2)
  -\sum_{n\ge2}\frac{\Lambda(n)}{n^\sigma}.
\]

Let `y=sqrt(x)`, `sigma=1/2+y`, and truncate at `X`:

\[
P_X(x)=\frac1{2y}\left[
\frac1\sigma+\frac1{\sigma-1}-\frac12\log\pi
+\frac12\psi(\sigma/2)
-\sum_{2\le n\le X}\frac{\Lambda(n)}{n^\sigma}
\right].
\]

Fix `delta>0` and `sigma>=1+delta`.  Since
`0 <= Lambda(n) <= log(n)`, for `X>=3` the decreasing-integral comparison gives

\[
\sum_{n>X}\frac{\Lambda(n)}{n^\sigma}
\le X^{-\delta}
\left(\frac{\log X}{\delta}+\frac1{\delta^2}\right).
\]

After division by `2y`, this yields an explicit uniform error on any interval
`y in [a,b]` with `a>1/2`.

The Lean seed currently formalizes only the sign of the closed-form expression.
The next formal task is the sum/integral comparison, including the exact
integer cutoff and monotonicity range.

**Status:** elementary theorem PAPER-PROVED / Lean partial.

---

## 6. Three-part error decomposition

For a concrete spectral observable `S_{lambda,N}`, a model observable
`S^model_lambda`, the exact target `S_Xi`, and the truncated prime expression
`P_{lambda^2}`, the triangle inequality gives

\[
\begin{aligned}
|S_{\lambda,N}-P_{\lambda^2}|
&\le |S_{\lambda,N}-S^\mathrm{model}_\lambda|\\
&\quad+|S^\mathrm{model}_\lambda-\mathcal S_\Xi|\\
&\quad+|\mathcal S_\Xi-P_{\lambda^2}|.
\end{aligned}
\]

We call these terms

\[
E_\mathrm{spectral},\qquad
E_\mathrm{model},\qquad
E_\mathrm{prime}.
\]

This inequality and addition of component limits are already in Lean.

**Status:** LEAN-SEED.

---

## 7. Candidate spectral-alignment inequality

Let `A_{lambda,N}` be a finite Hermitian approximation, with lowest two
eigenvalues `epsilon_0 < epsilon_1`, gap

\[
g=\epsilon_1-\epsilon_0>0.
\]

For a normalized trial vector `v`, define Rayleigh excess

\[
r=\langle Av,v\rangle-\epsilon_0.
\]

Expanding in an orthonormal eigenbasis gives

\[
\sum_{j\ge1}|c_j|^2\le r/g.
\]

After optimizing phase, one obtains a distance estimate of the form

\[
\|v-e^{i\theta}\xi_0\|\le \sqrt{2r/g}.
\]

Adding the projection/Galerkin tail `tau` motivates

\[
\eta_{\lambda,N}
=\|k_\lambda\|\sqrt{2r/g}+2\tau.
\]

A residual/separation certificate can replace exact knowledge of `epsilon_0`.
The Lean seed defines these scalar defects and proves nonnegativity, but does
not yet formalize the Hilbert-space perturbation theorem.

**Status:** standard perturbation lemma CANDIDATE pending exact reference and
Lean proof; applicability to the concrete operator OPEN.

---

## 8. Candidate quantitative rate

A previous exploratory derivation suggested that if

\[
\eta_{\lambda,N(\lambda)}=O(\lambda^{-q}),\qquad q>1/2,
\]

then one may choose a nonempty vertical interval so that the total error tends
to zero, with an optimized exponent

\[
\rho(q)=\min\left\{\frac{2q-1}{3},\frac23\right\}.
\]

The scalar properties of `rho(q)` are formalized in Lean.  The analytic
premises behind the `2/3` ceiling depend on a **candidate extension of the
prolate/model estimate** and have not yet been checked against the source
paper's exact transform conventions and constants.

Therefore:

- the formula is a research target, not a theorem of this repository;
- no paper should advertise it as new until a line-by-line source audit and
  independent derivation are complete;
- the rate must be rewritten with explicit constants before formalization.

**Status:** CANDIDATE.

---

## 9. Concrete operator integration

The primary source `Zeta Spectral Triples` constructs self-adjoint operators
from rank-one perturbations of a scaling spectral triple on
`[lambda^{-1},lambda]`, using Euler products over primes up to `lambda^2`.
It reports numerical convergence of spectra to low Riemann zeros and states
that a rigorous convergence proof would establish RH.  A companion real-zero
theorem shows that under lower-bounded self-adjointness plus a simple isolated
lowest eigenvalue with an even eigenfunction, the Fourier transform of that
eigenfunction has only real zeros.

The project must not compress those hypotheses into a single informal phrase.
The concrete layer needs:

1. exact quadratic-form and domain definitions;
2. lower boundedness and closure;
3. self-adjoint realization;
4. compact resolvent/discrete spectrum;
5. lowest-state existence, simplicity, isolation, and parity;
6. determinant/Fourier-transform normalization;
7. squared-resolvent trace-class property;
8. convergence with explicit multiplicity control.

**Status:** OPEN.

---

## 10. Non-circularity audit

Global positivity of the Weil quadratic form is closely tied to RH.  It cannot
be inserted as an assumption to prove the spectral rate and then presented as
an unconditional argument.  Every future proof must identify exactly which
restricted or semilocal positivity statement is used and why it is weaker than
RH.

Likewise, numerical agreement of finitely many eigenvalues is evidence but
cannot control all zeros or the high-energy resolvent tail without a theorem.

---

## 11. Recommended research order

1. Complete the Lean `Xi` bridge.
2. Formalize theorem A.
3. Formalize the explicit prime tail.
4. Build finite Stieltjes certificate infrastructure.
5. Prove the finite Rayleigh/gap alignment theorem.
6. Audit the candidate model/prolate estimate against the source.
7. Only then instantiate the concrete spectral operator.

This order maximizes publishable mathematical infrastructure while keeping the
open RH-strength step visible.
