# A second certified two-prime support interval

The full seven-block Schur calculation at \(a=0.56\), with the same registered
parameters used at \(a=0.551\), proves

\[
 A_{0.56}\succeq8.267012903894029\cdot10^{-10}I.
\]

Applying the common two-prime continuation theorem on the neighbourhood
\(0.555\le a\le0.57\) gives the explicit consequence

\[
 |a-0.56|\le
 10^{-521\,082\,215\,147\,536\,318\,464}
 \quad\Longrightarrow\quad
 \boxed{A_a\succeq1.6534025807788056\cdot10^{-10}I>0}.
\]

The registered continuity data are

| quantity | certified value |
|---|---:|
| \(p_2+p_3\) | `< 1.1244131723318378` |
| bounded perturbation at the centre | `< 6.485856281782037` |
| relative Young parameter | `2.5492433207505097e-11` |
| required logarithm | `2.3996722816460663e21` |
| ordinary-term radius | `> 2.1630077035354888e-11` |

The enormous decimal exponent is caused by the logarithmic translation
modulus, not by uncertainty in the point certificate.  In particular, the
two certified intervals around 0.551 and 0.56 do not overlap.  This proves a
second open set of localized positivity but does not supply an interval
covering argument and does not prove RH.

For positivity itself, domain monotonicity makes the non-overlap irrelevant:
the endpoint theorem at \(a=0.60\) proves \(\lambda_a>0\) simultaneously for
all \(0<a\le0.60\).  This local continuation certificate is retained because
it quantifies continuity after prime three enters, not because it is needed
to fill support gaps.

The executable certificate is
`experiments/theta_pencil/support_056_interval_certificate.py`.
