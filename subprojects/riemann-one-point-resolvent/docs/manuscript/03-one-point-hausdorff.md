# One-point Hausdorff criterion

Fix \(x_0>1/4\) and define

\[
b_n(x_0)=x_0^n\frac{(-1)^n}{n!}\mathcal S_\Xi^{(n)}(x_0).
\]

For a sequence \(b\), define recursively

\[
D^0b_n=b_n,
\qquad
D^{k+1}b_n=D^kb_n-D^kb_{n+1}.
\]

The classical Hausdorff theorem says that

\[
b_n=\int_0^1v^n\,d\mu(v)
\]

for a finite positive measure \(\mu\) if and only if \(D^kb_n\ge0\) for all \(k,n\ge0\).

## Equivalence

**Theorem (documented, not yet fully formalized).** For every fixed \(x_0>1/4\), the following are equivalent:

1. RH;
2. \((b_n(x_0))\) is a Hausdorff moment sequence;
3. \(D^kb_n(x_0)\ge0\) for all \(k,n\).

### RH implies moments

Under RH,

\[
\frac{(-1)^n}{n!}\mathcal S_\Xi^{(n)}(x_0)
=\sum_{j\ge1}\frac1{(\gamma_j^2+x_0)^{n+1}}.
\]

Set

\[
u_j=\frac1{\gamma_j^2+x_0},
\qquad
v_j=\frac{x_0}{\gamma_j^2+x_0}\in(0,1).
\]

Then

\[
b_n(x_0)=\sum_j u_jv_j^n,
\]

represented by the finite positive measure \(\mu_{x_0}=\sum_j u_j\delta_{v_j}\), whose total mass is \(\mathcal S_\Xi(x_0)\).

### Moments imply a slit-plane extension

Given a representing measure, define for \(w\in\Omega\)

\[
F(w)=\int_0^1
\frac{d\mu(v)}{1+((w-x_0)/x_0)v}.
\]

For \(v>0\), the denominator can vanish only at \(w=x_0(1-v^{-1})\in(-\infty,0]\); for \(v=0\) it is one. Thus standard parameterized integration makes \(F\) holomorphic on \(\Omega\).

Near \(x_0\), geometric expansion gives

\[
F(x_0+h)=\sum_{n\ge0}(-1)^n\frac{h^n}{x_0^n}b_n(x_0),
\]

the Taylor series of \(\mathcal S_\Xi(x_0+h)\). Therefore the functions agree on a neighborhood, and the slit-plane criterion applies.

## Falsifiability

A certified negative signed difference would contradict RH. Positivity of any finite collection is only a passed truncation test, never a proof of all inequalities.
