# Why this is a separate repository

The uploaded starting package belongs to a large Yang–Mills formalization.  The
Riemann prime–resolvent programme has unrelated mathematical dependencies,
reviewers, release cadence, and risk profile.  It is therefore packaged as a
standalone Lean project rather than added to the Yang–Mills tree.

The new repo reuses only the pinned Lean/Mathlib environment and the user's
reproducibility conventions.  No Yang–Mills theorem is imported.
