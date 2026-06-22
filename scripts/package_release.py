#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VERSION = (ROOT / 'VERSION').read_text(encoding='utf-8').strip()
RELEASE = ROOT / 'release'
NAME = f'riemann-prime-resolvent-{VERSION}'


def main() -> None:
    subprocess.run(['python3', 'scripts/generate_manifest.py'], cwd=ROOT, check=True)
    subprocess.run(['python3', 'scripts/check_release.py'], cwd=ROOT, check=True)
    RELEASE.mkdir(exist_ok=True)
    archive = RELEASE / f'{NAME}.zip'
    if archive.exists():
        archive.unlink()
    subprocess.run([
        'zip', '-q', '-X', '-r', str(archive), '.',
        '-x', '.git/*', '.lake/*', 'site/*', 'release/*', '__pycache__/*', '*.pyc'
    ], cwd=ROOT, check=True)
    digest = hashlib.sha256(archive.read_bytes()).hexdigest()
    (archive.with_suffix(archive.suffix + '.sha256')).write_text(
        f'{digest}  {archive.name}\n', encoding='utf-8')
    print(archive)


if __name__ == '__main__':
    main()
