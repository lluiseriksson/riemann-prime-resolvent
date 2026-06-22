# Copy-paste prompt for the next agent

You are taking over the repository `riemann-prime-resolvent`.

Start by reading `NO-RH-CLAIM.md`, `RESEARCH-STATUS.md`,
`AGENT-ONBOARDING.md`, `docs/MATHEMATICAL-DEVELOPMENT.md`, and
`docs/THEOREM-LEDGER.md`.  Then run `./scripts/verify.sh`.

Your first objective is to make the seed build green on the pinned Lean/Mathlib
version without introducing `sorry`, `admit`, `axiom`, or unsafe shortcuts.
Record any compatibility fixes in `verification/LEDGER.md`.

After the build is green, work on the smallest genuine theorem in this order:

1. prove the functional symmetry/evenness of the project `riemannXi`;
2. prove that `z ↦ -z^2` maps the upper half-plane into `slitPlane`;
3. formulate and prove the local log-derivative pole lemma at a zero;
4. prove the abstract slit-plane extension criterion implying
   `XiOnlyRealZeros`;
5. connect `XiOnlyRealZeros` to Mathlib's `RiemannHypothesis`.

Keep the concrete spectral model abstract until the analytic chain is complete.
All source-dependent prolate estimates remain `CANDIDATE` until checked against
arXiv:2511.22755 line by line.  Update the theorem ledger and oracle on every
completed brick.
