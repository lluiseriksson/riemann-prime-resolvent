#!/usr/bin/env bash
set -euo pipefail

if [[ $# -ne 1 ]]; then
  echo "Usage: $0 OWNER/REPOSITORY" >&2
  exit 2
fi

REPO="$1"
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

command -v gh >/dev/null || { echo "GitHub CLI (gh) is required." >&2; exit 127; }
gh auth status

test -d .git || { echo "Initialize git and create the seed commit first." >&2; exit 1; }
test -z "$(git status --porcelain)" || { echo "Working tree is dirty; aborting." >&2; exit 1; }

./scripts/verify.sh

test -z "$(git status --porcelain --untracked-files=no)" || {
  echo "Tracked files changed during verification; inspect before publishing." >&2
  exit 1
}

gh repo create "$REPO" --public --source=. --remote=origin --push
printf 'Created and pushed https://github.com/%s\n' "$REPO"
