# Mathematical status

## Kernel checked here

The Lean source establishes only finite and scalar statements independent of RH: triangle inequalities, convergence glue, positivity of finite Stieltjes sums, paired-spectrum normalization, nonnegativity of a closed-form tail expression, defect estimates and scalar rate identities.

## Documented reduction

The integrated documentation explains how a positive Stieltjes limit agreeing with the completed-zeta target on one interval would imply that all zeros of \(\Xi\) are real. The canonical criterion lives in the companion repository and is not yet fully closed in Lean.

## Open construction frontier

A valid input to the criterion still requires:

1. a precise concrete self-adjoint family;
2. domain and multiplicity control;
3. positivity and trace/resolvent well-definedness;
4. a uniform bound at one positive point;
5. convergence on a nonempty real interval;
6. a proof that no step assumes RH or an equivalent zero-location statement;
7. exact agreement of Fourier/Mellin and completed-zeta conventions.

Passing finite numerical tests does not discharge these obligations.
