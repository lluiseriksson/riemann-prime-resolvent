## Scope and claim boundary

- [ ] Exact statement, hypotheses and ownership layer documented
- [ ] No open claim hidden in a structure, theorem assumption or generated artifact
- [ ] Primary sources and normalization/convention bridges checked
- [ ] The description explains why this does not overstate progress toward RH

## Verification evidence

- [ ] `./scripts/verify_static.sh`
- [ ] `./scripts/verify_lean.sh`
- [ ] `make audit`
- [ ] `mkdocs build --strict`
- [ ] interface contract unchanged or synchronized byte-for-byte
- [ ] generated files reviewed before `make manifest`

Paste the relevant command output or link the green checks. State any verification not run and why.

## Reproducibility and security

- [ ] Third-party Actions remain pinned to full commit SHAs
- [ ] No network installer is piped directly to an interpreter
- [ ] Release/metadata changes keep VERSION, CFF, CodeMeta and changelog coherent
- [ ] New paths are portable across case-sensitive and case-insensitive filesystems

## Reviewer notes

List the declarations, files and publication/status entries that deserve the closest review.
