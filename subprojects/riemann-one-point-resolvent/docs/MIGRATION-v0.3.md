# Migration from v0.2

- `PrimeResolvent/` became `OnePointResolvent/`.
- the Lean namespace `PrimeResolvent` became `OnePointResolvent`;
- `PrimeResolvent.lean` became `OnePointResolvent.lean`;
- the standalone `paper/` tree was removed;
- mathematical exposition moved to `docs/manuscript/`;
- paper CI became strict documentation/Pages CI;
- releases are source and web-documentation artifacts only.

Downstream Lean imports must be updated explicitly. No compatibility namespace is provided because retaining `PrimeResolvent` here would conflict conceptually with the construction repository.
