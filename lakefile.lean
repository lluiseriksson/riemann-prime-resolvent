import Lake
open Lake DSL

package «RiemannPrimeResolvent» where
  -- The research code is deliberately small; Mathlib is pinned below.

lean_lib «RiemannPrimeResolvent» where
  -- Root module: RiemannPrimeResolvent.lean

require mathlib from git
  "https://github.com/leanprover-community/mathlib4.git" @
    "07642720480157414db592fa85b626dafb71355b"
