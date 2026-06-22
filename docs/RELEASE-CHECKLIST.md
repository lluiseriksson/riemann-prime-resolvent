# Release checklist

- [ ] `./scripts/verify_static.sh`
- [ ] `./scripts/verify_lean.sh`
- [ ] `mkdocs build --strict`
- [ ] no `paper/` directory, committed PDF or included symlink
- [ ] interface contract byte-identical to the criterion subproject mirror
- [ ] theorem ledger and status pages updated
- [ ] source audit and novelty wording reviewed
- [ ] generated artifacts reviewed, then `make manifest`
- [ ] read-only inventory/policy check passes with `make audit`
- [ ] `make package` succeeds twice with the same ZIP SHA-256
- [ ] Pages workflow green
- [ ] source-only release artifact and `.sha256` file generated
