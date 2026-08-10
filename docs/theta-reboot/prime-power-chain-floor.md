# Separable prime-power chain floor

## Why a second complement architecture is useful

Below \(a=\log2\), both active displacements \(h_2\) and \(h_3\) exceed one,
and their common refinement closes after seven intervals.  Immediately above
the threshold the refinement still closes, but it jumps to thirteen
intervals; later windows grow again.  A proof intended to cross arbitrary
prime-power thresholds should therefore not depend exclusively on one
hand-derived common partition.

## Separable form inequality

Write

\[
 V(x)=-\frac12\log(1-x^2)\ge0
\]

and let \(T_n\) be the symmetric translation of displacement
\(h_n=\log n/a\) and weight \(-\Lambda(n)/\sqrt n\).  For numbers
\(\theta_n\ge0\) with \(\sum_n\theta_n\le1\),

\[
 V+\sum_nT_n
 =\sum_n(\theta_nV+T_n)
   +(1-\sum_n\theta_n)V.
\]

Each single operator \(\theta_nV+T_n\) fibers over residues modulo \(h_n\).
Every fiber is a finite path

\[
 r,\ r+h_n,\ldots,r+(q-1)h_n
\]

and hence a finite tridiagonal matrix with diagonal \(\theta_nV\) and
off-diagonal \(-\Lambda(n)/\sqrt n\).  Interval subdivision in the residue
variable plus Arb/Rump eigenvalue isolation gives a rigorous lower bound.
No common prime partition and no zeta zero enters this inequality.

## First post-threshold gate

At \(a=0.7>\log2\), the active prime powers are \(2,3,4\).  The registered
allocation

\[
 (\theta_2,\theta_3,\theta_4)=(0.325,0.5,0.175)
\]

makes the prime-two fibers paths of length at most three and the other two
fibers paths of length at most two.  Together with the scalar term, the
order-39 smooth loss and the harmonic tail floor \(H_{16}\), the executable
certificate gives

\[
 D\succeq0.3279505723647819I>0.
\]

This crosses the prime-power-four threshold for the **high-degree complement
only**.  It is not yet a certificate for the complete operator \(A_{0.7}\):
the low source block and its exact tail coupling still have to be assembled
in a basis that does not assume a finite common cut closure.

The executable proof is `prime_power_chain_floor.py`.  The stronger joint
thirteen-block floor for this particular window is recorded separately in
`third-window-partition.md`.
