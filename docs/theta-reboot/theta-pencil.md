# The theta-pencil and the first structural obstruction

## 1. Logarithmic-coordinate form

Write \(t=e^x\) and define the positive even function

\[
 \psi(x)=\Theta_{00}(i e^{2x}),\qquad \Phi(x)=-\log\psi(x).
\]

Hedenmalm's operators become

\[
 D=-i\partial_x,\qquad L=D-i a(x),\qquad a(x)=\Phi'(x),
\]

and the generalized eigenvalue equation is

\[
 A u+\alpha B u=0,\qquad A=LD,\quad B=L.
\]

The theta density satisfies

\[
 \Xi(\alpha)=\int_{\mathbb R}\psi(x)e^{i\alpha x}\,dx,
\]

up to the fixed Fourier convention. The boundary-value eigenfunction can be
written

\[
 u_\alpha(x)=e^{-i\alpha x}\int_{-\infty}^{x}
 e^{i\alpha y}\psi(y)\,dy,
\]

and obeys

\[
 (D+\alpha)u_\alpha=-i\psi,\qquad L\psi=0.
\]

This last rank-one forcing term is important. Dropping it turns the pencil into
the free dilation generator and creates a false proof.

## 2. Metric equation

Let \(C\) be a positive operator representing a candidate second inner
product. Formal self-adjointness of the pair means

\[
 A^*CB=B^*CA.
\]

Since \(A=LD\), this is equivalent on a common invariant core to

\[
 [D,Q]=0,\qquad Q=L^*CL.
\tag{TPQ}
\]

Thus the metric problem has a rigid normal form: after conjugation by \(L\),
the positive operator must commute with translations in logarithmic
coordinates. Under the usual spectral hypotheses, \(Q\) must therefore be a
nonnegative Fourier multiplier \(m(D)\).

This observation does not solve TP-M. The kernel of \(L\), the unbounded
inverse, the form domain, and nondegeneracy on the complex-zero
eigenfunctions are precisely where a circular construction can hide.

## 3. No local weighted metric

**Theorem (local-metric obstruction).** Let \(w\in C^2(\mathbb R)\) be strictly
positive, and equip the target of \(L\) with the local form

\[
 \langle f,g\rangle_w=\int_{\mathbb R}f(x)\overline{g(x)}w(x)\,dx.
\]

If the theta-pencil is formally self-adjoint on \(C_c^\infty(\mathbb R)\) for
this form, then \(w\) is constant and

\[
 a(x)^2-a'(x)=\frac{\psi''(x)}{\psi(x)}
\]

is constant. For the Riemann theta density this is impossible. Hence no
strictly positive local weighted \(L^2\) metric symmetrizes the pencil on that
core.

### Proof

Let \(M_w\) denote multiplication by \(w\). In ordinary \(L^2(dx)\),

\[
 Q=L^*M_wL=(D+ia)M_w(D-ia).
\]

Applied to a test function \(f\), this is

\[
 Qf=-wf''-w'f'+\left(w(a^2-a')-aw'\right)f.
\]

The pencil symmetry is equivalent to \([D,Q]=0\). Comparing the coefficient
of \(f''\) in the commutator gives \(w'=0\). With \(w\) constant, comparison
of the zeroth-order coefficient gives \((a^2-a')'=0\).

Because \(a=-(\log\psi)'\), direct differentiation gives

\[
 a^2-a'=\frac{\psi''}{\psi}.
\]

For the Riemann theta density, Hedenmalm's asymptotic formula yields

\[
 \Phi(x)=\pi e^{2x}-\frac92x-\log(2\pi^2)+O(e^{-2x})
 \quad(x\to+\infty).
\]

Consequently \(a^2-a'\sim4\pi^2e^{4x}\), so it is not constant. This
contradicts the necessary condition. \(\square\)

## 4. Consequence for the search

The required metric, if it exists, must be nonlocal. The next candidate class
is a positive integral operator

\[
 (Cf)(x)=\int_{\mathbb R}c(x,y)f(y)\,dy
\]

whose kernel is defined from \(\psi\), satisfies the distributional form of
(TPQ), and has a coercive closed form on every admissible eigenfunction. The
equation alone is insufficient: formally setting
\(C=(L^*)^{-1}m(D)L^{-1}\) hides all of the kernel and domain problems in the
two inverses.

## 5. Global bounded-metric obstruction

The local theorem is part of a broader obstruction.

**Theorem (cyclic-vector obstruction).** Assume that \(C\ge0\) is such that
\(Q=L^*CL\) extends to a bounded positive operator on \(L^2(\mathbb R)\), that
the pencil identity holds on a common \(D\)-invariant core, and that \(\psi\)
belongs to the relevant domains. Then \(Q=0\).

### Proof

The pencil identity gives \([D,Q]=0\). Hence, under the Fourier transform,
\(Q\) is multiplication by an essentially bounded function \(m(\xi)\ge0\).
Since \(L\psi=0\),

\[
 0=L^*CL\psi=Q\psi.
\]

The Fourier transform of \(\psi\) is \(\Xi\), up to the fixed convention, so

\[
 m(\xi)\Xi(\xi)=0\quad\text{for almost every real }\xi.
\]

The entire function \(\Xi\) is not identically zero and therefore its real
zero set is discrete and has Lebesgue measure zero. Thus \(m=0\) almost
everywhere and \(Q=0\). \(\square\)

Equivalently, \(\psi\) is a cyclic vector for the dilation generator \(D\):
its Fourier transform is nonzero almost everywhere. An operator commuting with
\(D\) and annihilating this cyclic vector must vanish.

This theorem closes bounded ambient metrics, including bounded convolution
kernels. It also explains why a formal kernel PDE is not enough: boundary and
domain terms must prevent the congruence from extending to all of logarithmic
\(L^2\). Any surviving metric is necessarily singular, unbounded, or defined
only on a restricted space. Such a restricted space must be constructed
without using the zeros themselves; otherwise the metric is circular.

## 6. Candidate sources for nonlocality

Three existing repositories supply reusable mechanisms, not conclusions:

- `lean-os-positivity`: reflection-positive sesquilinear forms and their
  Cauchy--Schwarz consequences;
- `lean-transfer-matrix`: positive finite transfer operators and spectral
  ordering;
- `lean-gaussian-field`: Gaussian covariance and heat-kernel structures.

The next derivation must produce an explicit kernel equation before importing
any of these abstractions. Otherwise "reflection positivity" would merely
rename the desired metric.

## 7. Decision

The theta-pencil remains valuable as an exact characterization and as a source
of the two obstruction theorems above. It is not retained as the main proof
track: the surviving singular-domain problem is at least as hard to construct
non-circularly as the spectral object sought by Hilbert--Polya. The active
programme now moves to finite-place Weil positivity, where the first new case
the first source-faithful arithmetic window \(S_q=\{\infty,2,3\}\) is
independently falsifiable.
