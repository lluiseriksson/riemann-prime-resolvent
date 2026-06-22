#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
./scripts/verify_static.sh
./scripts/verify_lean.sh
echo "Complete verification passed"
