# Resumen en español

Este repositorio desarrolla una formulación de la hipótesis de Riemann basada en el observable

\[
\mathcal S_\Xi(x)=\frac{1}{2\sqrt{x}}\frac{\xi'}{\xi}\left(\frac12+\sqrt{x}\right).
\]

Fijado un único punto \(x_0>1/4\), se define

\[
b_n=x_0^n\frac{(-1)^n}{n!}\mathcal S_\Xi^{(n)}(x_0).
\]

El paper demuestra que RH equivale a que \((b_n)\) sea una sucesión de momentos de Hausdorff sobre \([0,1]\). Esto produce desigualdades de diferencias finitas y certificados matriciales positivos. La transformación

\[
\lambda\mapsto\frac{x_0}{\lambda+x_0}
\]

convierte el espectro no acotado en puntos de un intervalo compacto.

El código Lean 4 actual verifica la parte algebraica finita: momentos atómicos, diferencias de Hausdorff, compactificación resolvente y certificados de suma de cuadrados. Todavía falta formalizar el argumento analítico completo y, sobre todo, demostrar la convergencia de una familia espectral concreta construida desde los primos.

Por tanto, el artefacto es un repositorio de investigación publicable y reproducible, no una demostración de RH.
