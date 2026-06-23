# Release checklist

- [ ] `python3 scripts/check_metadata.py --tag "v$(cat VERSION)"`
- [ ] `python3 scripts/check_workflows.py`
- [ ] `./scripts/verify_static.sh`
- [ ] `./scripts/verify_lean.sh`
- [ ] root and criterion `mkdocs build --strict`
- [ ] Container workflow builds and `python -m pip check` passes
- [ ] no `paper/` directory, committed PDF or included symlink
- [ ] interface contract byte-identical to the criterion subproject mirror
- [ ] shared release/audit tooling byte-identical between project roots
- [ ] theorem ledger, status pages and claim map updated
- [ ] source audit and novelty wording reviewed
- [ ] generated artifacts reviewed, then `make manifest`
- [ ] read-only metadata/inventory/policy check passes with `make audit`
- [ ] root and criterion `make package` each succeed twice with identical ZIP SHA-256
- [ ] all `.zip.sha256` files verify
- [ ] Pages workflow publishes root and `/criterion/` sites
- [ ] source-only monorepo and criterion artifacts uploaded
- [ ] provenance attestations created for both ZIPs
