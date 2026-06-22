#!/usr/bin/env bash
set -euo pipefail

VERSION="${1:-dev}"
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PARENT="$(dirname "$ROOT")"
NAME="$(basename "$ROOT")"
OUT="$PARENT/${NAME}-${VERSION}.zip"

cd "$PARENT"
rm -f "$OUT"
zip -qr "$OUT" "$NAME" \
  -x "$NAME/.git/*" "$NAME/.lake/*" "$NAME/paper/*.pdf" \
     "$NAME/paper/*.aux" "$NAME/paper/*.log" "$NAME/verification/latest.log"
sha256sum "$OUT" > "$OUT.sha256"
echo "$OUT"
