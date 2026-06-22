import PrimeResolvent

/-!
# Axiom audit entry point

Run with:

`lake env lean PrimeResolvent/Oracle.lean`
-/

#print axioms PrimeResolvent.hausdorffDiff_atomicMoment
#print axioms PrimeResolvent.atomicMoment_isHausdorffCompletelyMonotone
#print axioms PrimeResolvent.finiteResolventMoment_isHausdorffCompletelyMonotone
#print axioms PrimeResolvent.finiteResolventHankelCertificate_nonneg
#print axioms PrimeResolvent.finiteResolventLocalizingCertificate_nonneg
#print axioms PrimeResolvent.primeResolvent_errorBudget
