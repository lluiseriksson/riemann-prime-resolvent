# Reproducibility

Install both monorepo dependency sets before running the integrated static layer:

```bash
python3 -m pip install \
  -r requirements.txt \
  -r requirements-docs.txt \
  -r subprojects/riemann-one-point-resolvent/requirements.txt \
  -r subprojects/riemann-one-point-resolvent/requirements-docs.txt
./scripts/verify_static.sh
lake exe cache get
./scripts/verify_lean.sh
```

The static layer regenerates SVG/PNG figures, CSV data and exact certificates, runs the tests, checks local links, builds the documentation when MkDocs is available, and then **checks** the committed source manifests without rewriting them. A stale generated artifact or an unlisted source file therefore fails verification instead of being silently absorbed into a new manifest.

## Manifest workflow

```bash
# Deliberate update after reviewing source/generated changes
make manifest

# Read-only validation used by CI and release jobs
make audit
```

The root audit also requires the two copies of `docs/contracts/resolvent-interface.json` to be byte-identical and rejects included symlinks, unsafe manifest paths, duplicate rows, PDFs and standalone `paper/` directories.

## Deterministic source archive

```bash
make package
(cd release && sha256sum -c *.zip.sha256)
```

`package_release.py` uses only the Python standard library. It packages exactly the manifest inventory beneath one versioned top-level directory, uses sorted members, fixed timestamps, canonical permissions and uncompressed ZIP entries. Running it twice over identical source bytes produces an identical archive byte for byte; the release workflow verifies that invariant before uploading the artifact.
