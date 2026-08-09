# One-prime moment model

## Primary input

Connes--Consani--Moscovici, *On q-series and the moment problem associated to
local factors*, [arXiv:2403.01247](https://arxiv.org/abs/2403.01247), treats
exactly (S=\{\infty,p\}). The measure

\[
 d\mu_S(s)=\left|\prod_{v\in S}L_v\!\left(\frac12-is\right)\right|^2ds
\]

is positive and its moment problem is determinate. Multiplication by (s)
therefore has a canonical self-adjoint Jacobi representation.

This positivity is unconditional and does not contain RH: its spectral measure
is built from the absolute square of **local factors**, not from the zeros of
(\Xi). The model is a semilocal scaffold, not a Hilbert--Pólya operator.

## Exact one-prime expansion

For (S=\{\infty,p\}), define

\[
 \alpha_\ell=(-4)^{-\ell}\binom{2\ell}{\ell},
 \qquad q=p^{-1},
\]

and

\[
 \Sigma_p(t)=e^{-t/2}\sum_{\ell\ge0}
 \alpha_\ell e^{-2\ell t}\frac{q^{2\ell+1}}{1-q^{2\ell+1}}.
\tag{L1}
\]

The unnormalised even moments are

\[
 c(2k,p)=c_0(2k)+(-1)^kL_{f_k}(q),
\]

where

\[
 f_k(2\ell+1)=2\left(\frac12+2\ell\right)^{2k}\alpha_\ell,
 \qquad f_k(2\ell)=0.
\tag{L2}
\]

The Lambert series converges geometrically for every prime (p). These
identities give an exact, inexpensive implementation oracle for the first
finite place.

## Rank-one and Catalan structure

The paper further expresses the (q)-deformation of the finite moment matrices
as Lambert series of rank-one operators. Its integrality theorem uses central
binomial/Catalan identities and places the coefficients in
(\mathbb Z[1/\sqrt2]). This is the precise bridge to the rooted-tree and
Catalan repositories: those repositories may formalize the combinatorial
identities in the deformation, but positivity of this local-factor measure is
already known and must not be advertised as progress on RH.

## Role in the active programme

The model supplies three things to each one-prime block of the first arithmetic
window:

1. an exact Jacobi basis adapted to the one-prime semilocal Hilbert space;
2. rapidly convergent Lambert-series coefficients for certified truncations;
3. a structured basis in which to represent the support-restricted Weil form.

The new matrix to study is **not** the positive Hankel moment matrix. It is the
compression of the signed form (W-S) to the two-constraint support space. Its
smallest eigenvalue is only a falsifier until a uniform operator theorem is
proved.
