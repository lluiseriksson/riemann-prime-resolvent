# Exact Legendre matrix and mode-resolved Feshbach diagnostic

## Closed boundary-potential matrix

Let

\[
 e_n(x)=\sqrt{\frac{2n+1}{2}}P_n(x),\qquad -1<x<1.
\]

For the logarithmic boundary potential the following integrals are exact:

\[
 I_{mn}:=\int_{-1}^1P_m(x)P_n(x)\log(1-x^2)\,dx=0
 \quad(m+n\text{ odd}),
\]

\[
 I_{mn}=-\frac4{|m-n|(m+n+1)}
 \quad(m\ne n,\ m+n\text{ even}),
\]

and

\[
 I_{nn}=\frac4{2n+1}\left(\log2-D_n\right),\qquad
 D_n=1+\sum_{k=1}^n\frac1{k(2k-1)(2k+1)}.
\]

Consequently, in the orthonormal Legendre basis the matrix of
\(V=-\tfrac12\log(1-x^2)\) is

\[
 V_{nn}=D_n-\log2,
\qquad
 V_{mn}=\frac{\sqrt{(2m+1)(2n+1)}}{|m-n|(m+n+1)}
\]

when \(m\ne n\) have the same parity, and zero otherwise. Since the regional
logarithmic Laplacian satisfies \(A_2P_n=H_nP_n\), this gives the entire
dominant matrix \(\mathcal L=A_2+V\) without endpoint quadrature.

For completeness, the off-diagonal identity follows directly from the
Legendre Sturm--Liouville equations. With
\(\lambda_j=j(j+1)\), integration by parts gives

\[
 (\lambda_n-\lambda_m)I_{mn}
 =-2\int_{-1}^1x(P_mP_n'-P_nP_m')\,dx.
\]

For \(n>m\) of equal parity, the derivative expansion
\(P_n'=\sum_{j<n,\ n-j\text{ odd}}(2j+1)P_j\) and the three-term recurrence
for \(xP_m\) make the last integral equal to (2); the reversed term is zero
by degree. This yields the displayed rational formula. The diagonal formula
follows from the base integral \(I_{00}=4(\log2-1)\) and the recurrence

\[
 (2n+1)I_{nn}-(2n-1)I_{n-1,n-1}
 =-\frac4{n(2n-1)(2n+1)}.
\]

The implementation is independently checked against adaptive endpoint
quadrature through degree (21), including both parity blocks.

## Why the scalar Schur estimate fails

Write the scaled Weil--Suzuki finite section as

\[
 A^{(d)}=\begin{pmatrix}A_{00}&B\\B^*&C\end{pmatrix}.
\]

The earlier tail theorem proves coercivity of (C), but the scalar estimate

\[
 \lambda_{\min}(A_{00})-\frac{\lVert B\rVert^2}{\lambda_{\min}(C)}
\]

throws away the modal structure of (B). At (a=0.4), (d=256), and a
74-mode low block, it gives (-1.97\times10^{-2}), even though the full Ritz
value is positive.

The exact finite-dimensional Feshbach complement retains that structure:

\[
 S^{(d)}=A_{00}-BC^{-1}B^*.
\]

Representative values, using the exact dominant matrix and independent Gauss
quadrature only for the bounded perturbation, are:

| dimension (d) | low modes | full Ritz | scalar Schur | finite Feshbach Ritz |
|---:|---:|---:|---:|---:|
| 32 | 16 | (1.81652\cdot10^{-4}) | (-2.617\cdot10^{-2}) | (1.81695\cdot10^{-4}) |
| 96 | 48 | (1.81303\cdot10^{-4}) | (-3.072\cdot10^{-2}) | (1.81309\cdot10^{-4}) |
| 192 | 74 | (1.81270\cdot10^{-4}) | (-1.941\cdot10^{-2}) | (1.81273\cdot10^{-4}) |
| 256 | 128 | (1.81261\cdot10^{-4}) | (-1.730\cdot10^{-2}) | (1.81262\cdot10^{-4}) |

This identifies the loss precisely: a one-number norm estimate destroys a
positive margin that a mode-resolved inverse preserves.

## A stronger diagonal-tail test

The analytic tail estimate also yields, in Legendre coordinates,

\[
 C\ge D=\operatorname{diag}_{n\ge N}
 \bigl(H_n-\lVert K_a\rVert\bigr).
\]

Whenever (D>0), inverse monotonicity gives

\[
 BC^{-1}B^*\le BD^{-1}B^*.
\]

This bound still fails at the first admissible cutoff (N=74), because its
first denominator is only (0.00896). But enlarging the low block changes the
result sharply. Truncating the correction at (d=512) gives

| low modes (N) | first tail denominator | lowest value of (A_{00}-BD^{-1}B^*) |
|---:|---:|---:|
| 74 | 0.00896 | (-48.50) |
| 96 | 0.26770 | (1.80786\cdot10^{-4}) |
| 128 | 0.55409 | (1.81080\cdot10^{-4}) |

This is the first version of the reduction whose *analytic* tail majorant
retains a positive numerical margin at (a=0.4). It is not yet a proof:

1. the displayed correction stops at mode 511;
2. the bounded perturbation matrices still need interval enclosures;
3. the omitted infinite weighted cross-tail must be bounded below the roughly
   (1.8\cdot10^{-4}) margin.

Those are now quantitative approximation obligations, rather than an
unstructured positivity assumption. The next decisive calculation is a
rigorous decay bound for the Legendre coefficients of the prime translation
and the smooth remainder.

