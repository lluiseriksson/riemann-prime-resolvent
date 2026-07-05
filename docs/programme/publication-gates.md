# Publication gates

## Current level: integrated research blueprint

The repository is suitable for public collaboration as an honest programme with reproducible finite results and an explicit frontier.

## Machine-readable frontier

`RiemannPrimeResolvent.PublicationFrontier` exposes a typed `PublicationGate`.
It is intentionally not a checklist of free-standing `Prop` fields: the gate
carries the concrete spectral-defect sequence and three-part error budget as
data, then requires `BeatsHalfThreshold defect` and `VanishingBudget budget`.

The old shape of this interface was too weak: process items such as "Lean build
green" and "oracle reviewed" belong in CI/docs, while bare proposition fields
can be instantiated by `True`.  The current gate therefore records only
mathematical data and proofs tied to that data.  Its consumer,
`publicationGate_delivers`, still documents the honest boundary: the gate does
not manufacture `XiStieltjesExtensionTarget`; it only applies the supplied
criterion bridge once that target is actually proved.

## Formalization milestone

A formalization-focused publication would require the abstract criterion, convention bridge and prime-tail theorem to be closed in Lean and independently reviewed. It would not constitute an RH proof.

## Substantive analytic milestone

A research advance requires a new unconditional estimate for a concrete prime-built spectral family: domain, gap/alignment, trace resolvent or interval convergence.

## RH-level claim

An RH claim requires the entire shared contract to be discharged without circular assumptions, plus independent mathematical and formal review. No finite computation or documentation wording can substitute for that chain.
