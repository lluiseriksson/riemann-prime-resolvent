# Reviewer guide

Review the project in independent mathematical, formal and engineering passes.

1. Run `./scripts/verify_static.sh`, `./scripts/verify_lean.sh` and `make audit` at the exact commit under review.
2. Verify that every headline claim occurs in the theorem ledger with the correct verified/documented/open/numerical status.
3. Audit the integer cutoff, completed-zeta normalization, operator domains, trace-class assumptions and non-circularity separately from finite numerics.
4. Inspect `oracle_check.lean` and the Lean build output; the text scanner is only an additional policy guard.
5. Compare the shared interface contract and mirrored release/audit tooling byte-for-byte.
6. Treat manifest updates as evidence requiring explanation: inspect every generated/source diff before accepting a regenerated hash.
7. Check VERSION/CFF/CodeMeta/changelog coherence, exact toolchain/Mathlib pins and the release tag.
8. Confirm all Action references are immutable, checkout credentials are not persisted, both archives reproduce and provenance attestations target the resulting ZIPs.
9. Reject any RH-level wording until every publication gate is closed.
