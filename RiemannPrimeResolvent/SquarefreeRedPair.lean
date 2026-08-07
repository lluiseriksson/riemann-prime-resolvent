import Mathlib.Data.Nat.Squarefree

/-!
# Squarefree black core and red square pairs

This file records only the finite arithmetic decomposition behind the
black/red interpretation.  It makes no analytic-continuation or RH claim.
-/

namespace RiemannPrimeResolvent

/-- Every natural number is a squarefree black core times a red square.

This is a namespace-stable wrapper around Mathlib's
`Nat.sq_mul_squarefree`; uniqueness and any Dirichlet-series consequence are
outside the scope of this finite theorem. -/
theorem exists_squarefreeCore_mul_sq (n : ℕ) :
    ∃ core root : ℕ, Squarefree core ∧ n = core * root ^ 2 := by
  obtain ⟨core, root, hfactor, hcore⟩ := Nat.sq_mul_squarefree n
  exact ⟨core, root, hcore, by simpa [mul_comm] using hfactor.symm⟩

end RiemannPrimeResolvent
