from __future__ import annotations

import json
import subprocess
import sys
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_generator_and_verifier(tmp_path: Path) -> None:
    output = tmp_path / 'certificate.json'
    subprocess.run([sys.executable, str(ROOT / 'scripts/exact_atomic_certificate.py'), '--output', str(output)], check=True)
    subprocess.run([sys.executable, str(ROOT / 'scripts/check_certificate.py'), str(output)], check=True)
    data = json.loads(output.read_text(encoding='utf-8'))
    assert data['status'].startswith('exact-finite')
    assert all(Fraction(v) >= 0 for v in data['signed_differences'].values())
