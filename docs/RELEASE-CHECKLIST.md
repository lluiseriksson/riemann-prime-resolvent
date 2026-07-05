# Release checklist

- [ ] `python3 scripts/check_metadata.py --tag "v$(cat VERSION)"`
- [ ] `python3 scripts/check_workflows.py`
- [ ] `python3 scripts/check_docs_assets.py`
- [ ] `python3 scripts/check_oracle_coverage.py`
- [ ] `python3 scripts/check_generated_reproducibility.py`
- [ ] `./scripts/verify_static.sh`
- [ ] `./scripts/verify_lean.sh`
- [ ] root and criterion `mkdocs build --strict`
- [ ] Container workflow builds and `python -m pip check` passes
- [ ] no `paper/` directory, committed PDF or included symlink
- [ ] interface contract byte-identical to the criterion subproject mirror
- [ ] shared release/audit tooling byte-identical between project roots
- [ ] theorem ledger matches the ordered `#print axioms` oracle exactly
- [ ] status pages and claim map updated
- [ ] source audit and novelty wording reviewed
- [ ] generated artifacts reviewed, then `make manifest`
- [ ] read-only metadata/inventory/policy check passes with `make audit`
- [ ] root and criterion `make package` each succeed twice with identical ZIP SHA-256
- [ ] all `.zip.sha256` files verify
- [ ] Pages workflow publishes root and `/criterion/` sites
- [ ] source-only monorepo and criterion artifacts uploaded
- [ ] provenance attestations created for both ZIPs

## Final closeout gate

- [ ] `python3 scripts/check_research_frontier.py`
- [ ] Four RF issue drafts reviewed and opened or deliberately migrated
- [ ] Final tag `v0.3.0-docs-integrated` published
- [ ] Both deterministic source archives and attestations published
- [ ] Repository left unarchived while RF issues remain active
