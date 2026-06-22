import Lake
open Lake DSL

package «RiemannPrimeResolvent» where

@[default_target]
lean_lib «RiemannPrimeResolvent» where

require mathlib from git
  "https://github.com/leanprover-community/mathlib4.git" @
    "fabf563a7c95a166b8d7b6efca11c8b4dc9d911f"
