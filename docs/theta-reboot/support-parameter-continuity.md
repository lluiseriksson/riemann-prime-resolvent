# Quantitative support continuity: the logarithmic-modulus barrier

## Question

The certificate at \(a=21/50\) gives a positive spectral margin.  Can one
propagate it to a neighboring interval by a bound of the form

\[
 \|A_a-A_b\|\le C|a-b|?
\]

No.  The obstruction is already present in one prime term and is independent
of RH.

Suzuki's scaled Rayleigh formula on \([-1,1]\) contains, for each active
prime power \(n\), the compressed translations with displacement

\[
 h_n(a)=\frac{\log n}{a}.
\]

The exact formula and the identification of the common form domain with a
subspace of \(H^{\log}(-1,1)\) are equations (4.5)--(4.6) of the primary
source.  The argument below quantifies the compactness mechanism used in its
continuity theorem.

## Operator-norm continuity fails

Let \(U_h=P\tau_hP\), where \(P\) restricts zero-extended functions to
\([-1,1]\).  For every \(0<h<2\), \(\|U_h\|=1\): choose a unit function
supported wholly in the nonempty overlap interval.  At \(h=2\), \(U_2=0\).
Consequently the prime term is not norm-continuous when it activates at a
support threshold.  High-frequency localized functions give the analogous
failure for moving cuts inside a fixed prime window.  A bounded-perturbation
Lipschitz argument cannot continue a spectral certificate.

## An explicit \(H^{\log}\) modulus

For a zero-extended \(f\), use the Fourier convention
\(\widehat f(\xi)=\int f(x)e^{i\xi x}\,dx\), and set

\[
 E_{\log}(f)=\frac1{2\pi}\int_{\mathbb R}
       \log(1+\xi^2)|\widehat f(\xi)|^2\,d\xi.
\]

If \(\delta=|h-k|>0\), then

\[
 |e^{i\xi h}-e^{i\xi k}|^2
 \le \min(4,\delta^2\xi^2)
 \le \frac{4\log(1+\xi^2)}{\log(1+\delta^{-2})}.
\]

Plancherel therefore gives

\[
 \|\tau_hf-\tau_kf\|_2^2
 \le\frac{4E_{\log}(f)}{\log(1+\delta^{-2})},
\]

and for the symmetric translation \(T_h=U_h+U_h^*\),

\[
 \boxed{
 |\langle f,(T_h-T_k)f\rangle|
 \le\frac{4\|f\|_2\sqrt{E_{\log}(f)}}
          {\sqrt{\log(1+\delta^{-2})}}.}
\]

This is a rigorous quantitative strengthening of strong continuity on the
natural form domain.

## Relating the modulus to Suzuki's dominant form

Suzuki's scale-free form is

\[
 \mathcal L(f)=\frac1{2\pi}\int
 (\log|\xi|+\gamma)|\widehat f(\xi)|^2\,d\xi.
\]

For \(f\) supported in \([-1,1]\), Cauchy--Schwarz gives
\(|\widehat f(\xi)|^2\le2\|f\|_2^2\).  Hence the negative logarithmic
moment on \(|\xi|<1\) is at most \(2\|f\|_2^2/\pi\), and

\[
 \boxed{
 E_{\log}(f)\le2\mathcal L(f)+
 \left(\frac4\pi-2\gamma+\log2\right)\|f\|_2^2,}
\]

where the displayed constant is \(0.8119553954920423\).

## Numerical consequence at the certified anchor

For a normalized ground state near \(a=0.42\), the existing source-side
perturbation budget gives

\[
 \mathcal L(f)\le
 5.047850307074702+7.42373609443714\cdot10^{-5}.
\]

Thus \(E_{\log}(f)\le10.907804484363336\).  The prime-2 coefficient is
\(c_2=\log2/\sqrt2\).  Asking the prime modulus alone to stay below the
certified global margin \(m=7.117220758560887\cdot10^{-5}\) requires

\[
 \log(1+\delta^{-2})>
 \frac{(4c_2)^2E_{\log}}{m^2}
 =8.276703173296081\cdot10^9.
\]

Equivalently,

\[
 \delta<10^{-1.797263258\cdot10^9}.
\]

The scalar and smooth terms are better behaved, so omitting them only makes
this diagnosis more favorable.  The general \(H^{\log}\) continuity theorem
is therefore far too weak to propagate the localized certificate by any
practical covering argument.

## Revised target

An effective continuation theorem must use regularity of the *ground-state
equation*, not merely membership in the form domain.  Two concrete options
remain:

1. prove a uniform stronger Fourier moment for the lowest eigenfunction and
   replace the logarithmic modulus by a power modulus;
2. find a ground-state transform or positivity-improving comparison that
   controls the sign without subtracting nearby operators in norm.

This is a no-go for one proof architecture, not a no-go for RH.
