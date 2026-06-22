# Instrucciones para montar y lanzar la repo

## Opción A: usar la carpeta incluida en el ZIP

```bash
unzip riemann-prime-resolvent-lean4-v0.1.0.zip
cd riemann-prime-resolvent

git init
git add .
git commit -m "chore: seed prime-resolvent Lean research programme"
git branch -M main

chmod +x scripts/*.sh
./scripts/bootstrap.sh
./scripts/verify.sh
```

## Opción B: clonar el `git bundle` incluido

Desde la carpeta exterior del paquete:

```bash
git clone riemann-prime-resolvent-v0.1.0.bundle riemann-prime-resolvent
cd riemann-prime-resolvent
git checkout main
./scripts/bootstrap.sh
./scripts/verify.sh
```

## Crear la repo pública cuando el build sea verde

Autentica primero GitHub CLI:

```bash
gh auth login
```

Después, desde la raíz:

```bash
./scripts/create_github_repo.sh lluiseriksson/riemann-prime-resolvent
```

El script no se ejecuta automáticamente y aborta si el árbol está sucio.

## Primera tarea del agente

1. Confirmar que `lake build` termina sin errores.
2. Corregir únicamente problemas de compatibilidad con la versión fijada.
3. No añadir `sorry`, `admit` ni `axiom`.
4. Registrar el log completo.
5. Formalizar primero la equivalencia entre la función `riemannXi` del proyecto
   y la formulación `RiemannHypothesis` de Mathlib.
6. Continuar con el criterio de extensión holomorfa al plano cortado.

## Importante

La repo no afirma una demostración de RH. El límite espectral concreto sigue
abierto. Toda estimación procedente de los cálculos anteriores está marcada
como candidata hasta comprobar convenciones, hipótesis y referencias exactas.
