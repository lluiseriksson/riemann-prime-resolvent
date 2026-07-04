from __future__ import annotations

import sys
from pathlib import Path

import pytest

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

from check_generated_reproducibility import (  # noqa: E402
    GeneratedArtifactError,
    verify_reproducible,
)


def _generator(tmp_path: Path, source: str) -> tuple[Path, tuple[tuple[str, ...], ...]]:
    root = tmp_path / "project"
    (root / "generated").mkdir(parents=True)
    script = root / "generate.py"
    script.write_text(source, encoding="utf-8")
    return root, ((sys.executable, "generate.py"),)


def test_deterministic_generator_passes(tmp_path: Path) -> None:
    root, commands = _generator(
        tmp_path,
        "from pathlib import Path\nPath('generated/result.txt').write_text('stable\\n')\n",
    )
    snapshot = verify_reproducible(root, commands, ("generated/*.txt",))
    assert list(snapshot) == ["generated/result.txt"]


def test_nondeterministic_generator_is_rejected(tmp_path: Path) -> None:
    root, commands = _generator(
        tmp_path,
        "from pathlib import Path\n"
        "counter = Path('counter.txt')\n"
        "value = int(counter.read_text()) + 1 if counter.exists() else 1\n"
        "counter.write_text(str(value))\n"
        "Path('generated/result.txt').write_text(str(value))\n",
    )
    with pytest.raises(GeneratedArtifactError, match="not byte reproducible"):
        verify_reproducible(root, commands, ("generated/*.txt",))


def test_missing_artifact_pattern_is_rejected(tmp_path: Path) -> None:
    root, commands = _generator(tmp_path, "pass\n")
    with pytest.raises(GeneratedArtifactError, match="matched nothing"):
        verify_reproducible(root, commands, ("generated/*.txt",))


def test_generator_failure_is_reported(tmp_path: Path) -> None:
    root, commands = _generator(tmp_path, "raise SystemExit(7)\n")
    with pytest.raises(GeneratedArtifactError, match=r"generator failed \(7\)"):
        verify_reproducible(root, commands, ("generated/*.txt",))
