# Resumen en español

Este repositorio trabaja un único programa matemático con dos interfaces del
mismo resolvente.

## Interfaz primo-resolvente

La capa principal intenta construir aproximantes espectrales positivos a partir
de datos primos y compararlos con el objetivo

\[
\mathcal S_\Xi(x)=\frac{1}{2\sqrt{x}}
\frac{\xi'}{\xi}\!\left(\frac12+\sqrt{x}\right).
\]

La cadena buscada es:

\[
\text{aproximantes construidos con primos}
\longrightarrow
\text{resolventes positivos}
\longrightarrow
\text{extensión de Stieltjes}
\longrightarrow
\text{ceros reales de }\Xi.
\]

La dificultad abierta es demostrar, sin usar RH de forma circular, que una
familia concreta construida con primos satisface las cotas y convergencias
necesarias.

## Interfaz de un punto

La capa `subprojects/riemann-one-point-resolvent` codifica el mismo resolvente
en un punto fijo \(x_0\) mediante la sucesión

\[
b_n(x_0)=x_0^n\frac{(-1)^n}{n!}\mathcal S_\Xi^{(n)}(x_0).
\]

La ruta correspondiente es:

\[
\text{derivadas en }x_0
\longrightarrow
\text{momentos de Hausdorff}
\longrightarrow
\text{certificados finitos}
\longrightarrow
\text{misma extensión de Stieltjes}.
\]

Esta segunda interfaz no es otro paper ni otro programa independiente. Es la
capa abstracta de criterio y certificados dentro del repositorio canónico
`riemann-prime-resolvent`.

## Estado actual

La parte verificada en Lean es finita y elemental: presupuestos de error,
positividad de sumas de Stieltjes finitas, compactificación de espectros
finitos, diferencias de Hausdorff y certificados racionales exactos. Siguen
abiertos el puente exacto con las convenciones de \(\Xi\), la extensión
holomorfa, el teorema infinito de momentos de Hausdorff, la cota prima completa
y la convergencia del operador espectral concreto.

Por tanto, el repositorio es un programa reproducible y falsable, no una
demostración de la hipótesis de Riemann.
