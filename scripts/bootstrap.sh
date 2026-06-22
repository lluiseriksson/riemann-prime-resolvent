#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt

if ! command -v elan >/dev/null 2>&1; then
  echo "Elan is not installed. Install it from https://github.com/leanprover/elan and rerun."
else
  elan show
  lake exe cache get
fi

echo "Bootstrap complete. Run ./scripts/verify.sh"
