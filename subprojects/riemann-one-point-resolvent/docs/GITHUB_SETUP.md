# GitHub setup

## First publication

```bash
git init
git add .
git commit -m "research artifact v0.2.0"
git branch -M main
git remote add origin git@github.com:lluiseriksson/riemann-one-point-resolvent.git
git push -u origin main
```

## Recommended repository settings

- Require the `lean`, `python`, and `build-paper` checks before merging.
- Protect `main`; require pull requests and one approving review.
- Enable Dependabot and secret scanning.
- Disable force pushes and branch deletion.
- Use annotated tags for releases.

## Release

```bash
git tag -a v0.2.0 -m "One-point resolvent–Hausdorff research artifact v0.2.0"
git push origin v0.2.0
```

The release workflow rebuilds Lean, Python checks, exact data, and the paper before producing an archive.
