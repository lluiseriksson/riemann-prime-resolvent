# Development candidates

Files in this directory are intentionally excluded from the root Lean import.
They are proposed next-step patches, not release theorems.

Promotion rule:

1. copy the candidate into `RiemannPrimeResolvent/`;
2. add the module to `RiemannPrimeResolvent.lean`;
3. run the pinned `lake build`;
4. add every theorem to `oracle_check.lean`;
5. update the theorem ledger and verification ledger;
6. commit only with a green exact-tag log.
