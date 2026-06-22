/-
Copyright (c) 2026 Lluís Eriksson.
Released under the GNU Affero General Public License v3.0.
-/

import RiemannPrimeResolvent.Basic

/-!
# Abstract convergence bookkeeping

The analytic work of the project is deliberately represented by separate
component limits.  This module proves only that the three limits add.
-/

namespace RiemannPrimeResolvent

open Filter Topology

/-- If the three error components tend to zero, their total tends to zero. -/
theorem ErrorBudget.tendsto_total_zero {E : ℕ → ErrorBudget}
    (hs : Tendsto (fun n => (E n).spectral) atTop (𝓝 0))
    (hp : Tendsto (fun n => (E n).prolate) atTop (𝓝 0))
    (hprime : Tendsto (fun n => (E n).prime) atTop (𝓝 0)) :
    Tendsto (fun n => (E n).total) atTop (𝓝 0) := by
  simpa [ErrorBudget.total] using (hs.add hp).add hprime

/-- The exact convergence statement sought for a sequence of scalar errors. -/
def ConvergesToZero (u : ℕ → ℝ) : Prop :=
  Tendsto u atTop (𝓝 0)

/-- Componentwise convergence packaged as a reusable research interface. -/
structure VanishingBudget (E : ℕ → ErrorBudget) : Prop where
  spectral : Tendsto (fun n => (E n).spectral) atTop (𝓝 0)
  prolate : Tendsto (fun n => (E n).prolate) atTop (𝓝 0)
  prime : Tendsto (fun n => (E n).prime) atTop (𝓝 0)

/-- A `VanishingBudget` implies convergence of the total budget. -/
theorem VanishingBudget.total {E : ℕ → ErrorBudget} (hE : VanishingBudget E) :
    Tendsto (fun n => (E n).total) atTop (𝓝 0) :=
  ErrorBudget.tendsto_total_zero hE.spectral hE.prolate hE.prime

end RiemannPrimeResolvent
