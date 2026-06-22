#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
mkdir -p verification
LOG="verification/latest.log"

exec > >(tee "$LOG") 2>&1

echo "RIEMANN PRIME-RESOLVENT VERIFICATION"
echo "===================================="
date -u --iso-8601=seconds || date -u
uname -a
printf 'PWD: %s\n' "$PWD"

if git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  printf 'GIT_HEAD: %s\n' "$(git rev-parse HEAD)"
  echo "GIT_STATUS_BEGIN"
  git status --short
  echo "GIT_STATUS_END"
else
  echo "GIT_HEAD: not-initialized"
fi

lean --version
lake --version
sha256sum lean-toolchain lakefile.lean lake-manifest.json

python3 scripts/check_consistency.py
lake build
lake env lean oracle_check.lean

echo "VERIFICATION_EXIT=0"
