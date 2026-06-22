# Risk register

| Risk | Severity | Mitigation |
|---|---:|---|
| Repackaging a known criterion as novel | High | systematic literature review; title as research programme until novelty confirmed |
| Hidden circular use of Weil positivity/RH | Critical | explicit assumption graph and non-circularity audit |
| Incorrect transform sign or normalization | Critical | source theorem transcription with test cases and symbolic checks |
| Lowest eigenvalue not uniformly simple/even | Critical | treat as separate theorem; numerical evidence is not proof |
| Resolvent not trace class or wrong multiplicity factor | High | prove trace ideal and paired-spectrum normalization explicitly |
| Montel theorem absent in Mathlib | Medium | contribute normal-family infrastructure or use measure compactness alternative |
| `completedRiemannZeta₀` normalization misunderstood | High | prove algebraic relation in Lean before downstream work |
| Numerical certificates depend on untrusted floats | High | interval/rational certificates checked in Lean |
| Build pin becomes obsolete | Medium | preserve tag/bundle; upgrade only on a dedicated branch |
| Premature public RH claim | Critical | `NO-RH-CLAIM.md`, gated release checklist, independent review |
