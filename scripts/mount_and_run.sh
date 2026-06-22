#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

if command -v docker >/dev/null 2>&1; then
  docker build -t riemann-prime-resolvent:seed .
  docker run --rm -it -v "$ROOT:/workspace" -w /workspace \
    riemann-prime-resolvent:seed ./scripts/verify.sh
else
  echo "Docker not found; running directly on the host." >&2
  ./scripts/bootstrap.sh
  ./scripts/verify.sh
fi
