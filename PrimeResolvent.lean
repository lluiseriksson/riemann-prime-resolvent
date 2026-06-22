/-!
# PrimeResolvent

Machine-checked finite algebra for the one-point resolvent--Hausdorff programme.

The analytic slit-plane criterion and its specialization to the Riemann xi
function are research targets, not claimed theorems in this Lean seed.  The
verified core proves the finite atomic moment identities, Hausdorff finite-
difference positivity, resolvent compactification into `[0,1]`, Gram-type
positive certificates, and the three-part error-budget inequality.
-/

set_option autoImplicit false

import PrimeResolvent.Basic
import PrimeResolvent.HausdorffFinite
import PrimeResolvent.ResolventCompactification
import PrimeResolvent.FiniteCertificates
import PrimeResolvent.ErrorBudget
import PrimeResolvent.Examples
