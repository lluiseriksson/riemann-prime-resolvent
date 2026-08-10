# No form-level differential propagation in the support

## Candidate and verdict

The certificate at \(a=0.7\) suggests trying to propagate positivity by a
Gronwall inequality such as

\[
 \partial_a q_a(w)\ge-C(a)\bigl(q_a(w)+\|w\|_2^2\bigr)
 \tag{G}
\]

on the common scaled form domain.  If valid with locally integrable \(C\),
this would prevent the lowest eigenvalue from reaching zero.  The candidate is
false already inside the first prime window, away from every activation
threshold.

## Exact witness

Suzuki's scaled formula on \((-1,1)\) contains

\[
 -c_2\langle T_h w,w\rangle,
 \qquad c_2=\frac{\log2}{\sqrt2},\qquad h=\frac{\log2}{a},
\]

where \(T_h\) is the compressed symmetric translation.  Take

\[
 \chi(x)=(1-x^2)^2\mathbf1_{(-1,1)}(x),
 \qquad w_\nu(x)=\chi(x)e^{i\nu x}.
\]

For \(0<h<2\), put

\[
 C(h)=\int_{-1}^{1-h}\chi(x+h)\chi(x)\,dx>0.
\]

Directly,

\[
 \langle T_hw_\nu,w_\nu\rangle=2C(h)\cos(\nu h)
\]

and

\[
 \partial_h\langle T_hw_\nu,w_\nu\rangle
 =2C'(h)\cos(\nu h)-2\nu C(h)\sin(\nu h).
\]

Choose

\[
 \nu_k=\frac{\pi/2+2\pi k}{h}.
\]

Then the translation itself vanishes while its derivative is exactly
\(-2\nu_kC(h)\).  Since \(h'(a)=-h/a\), the derivative of the negative prime
term has magnitude proportional to \(\nu_k\), with a choice of phase giving
the negative sign required to violate (G).

Although this notation uses a complex modulation, the obstruction is also
real: the form and its derivative split over the real and imaginary parts, so
if their sum violates (G), at least one of the two real components does.

On the other hand, modulation of a fixed compactly supported function obeys

\[
 E_{\log}(w_{\nu_k})=O(\log(1+\nu_k^2)).
\]

Indeed,

\[
 1+(\eta+\nu)^2\le2(1+\eta^2)(1+\nu^2)
\]

inside the Fourier integral.  The scalar and smooth-kernel derivatives are
bounded on \(L^2\), and the scale-free dominant form is independent of
\(a\).  Thus the negative derivative grows linearly while the entire available
form control grows only logarithmically.  No finite \(C(a)\) can make (G)
hold on the form domain.

## Scope of the obstruction

This does **not** show that \(\lambda_a\) crosses zero, and it does not refute
an eigenfunction-specific differential argument.  It proves that such an
argument cannot follow merely from the common \(H^{\log}\) form bound.  A
surviving propagation theorem must first prove extra regularity or phase
control for the actual ground state and justify a Hellmann--Feynman formula
despite the moving compressed translations.

The executable witness is `support_derivative_no_go.py`.  Its overlap and
overlap derivative are evaluated by polynomial antiderivatives, not numerical
quadrature.
