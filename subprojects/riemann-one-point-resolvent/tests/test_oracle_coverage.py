from __future__ import annotations

import sys
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

from check_oracle_coverage import audit  # noqa: E402


def _construction(tmp_path: Path) -> Path:
    root = tmp_path / "project"
    (root / "RiemannPrimeResolvent").mkdir(parents=True)
    (root / "docs").mkdir()
    (root / "RiemannPrimeResolvent/Basic.lean").write_text(
        "namespace RiemannPrimeResolvent\n\n"
        "theorem alpha : True := by trivial\n\n"
        "namespace Space\n"
        "@[simp] lemma beta : True := by trivial\n"
        "private theorem helper : True := by trivial\n"
        "end Space\n\n"
        "end RiemannPrimeResolvent\n",
        encoding="utf-8",
    )
    (root / "oracle_check.lean").write_text(
        "import RiemannPrimeResolvent\n\n"
        "#print axioms RiemannPrimeResolvent.alpha\n"
        "#print axioms RiemannPrimeResolvent.Space.beta\n",
        encoding="utf-8",
    )
    (root / "docs/THEOREM-LEDGER.md").write_text(
        "# Ledger\n\n"
        "| Declaration | Status | Meaning |\n"
        "|---|---|---|\n"
        "| `RiemannPrimeResolvent.alpha` | verified | a |\n"
        "| `RiemannPrimeResolvent.Space.beta` | verified | b |\n",
        encoding="utf-8",
    )
    return root


def test_exact_oracle_ledger_sequence_passes(tmp_path: Path) -> None:
    assert audit(_construction(tmp_path)) == []


def test_missing_oracle_declaration_is_rejected(tmp_path: Path) -> None:
    root = _construction(tmp_path)
    ledger = root / "docs/THEOREM-LEDGER.md"
    ledger.write_text(ledger.read_text(encoding="utf-8").replace(
        "| `RiemannPrimeResolvent.Space.beta` | verified | b |\n", ""
    ), encoding="utf-8")
    assert any("missing from ledger" in failure for failure in audit(root))


def test_wildcard_verified_entry_is_rejected(tmp_path: Path) -> None:
    root = _construction(tmp_path)
    ledger = root / "docs/THEOREM-LEDGER.md"
    ledger.write_text(ledger.read_text(encoding="utf-8").replace(
        "RiemannPrimeResolvent.Space.beta", "RiemannPrimeResolvent.Space.*"
    ), encoding="utf-8")
    assert any("must be exact" in failure for failure in audit(root))


def test_order_drift_is_rejected(tmp_path: Path) -> None:
    root = _construction(tmp_path)
    ledger = root / "docs/THEOREM-LEDGER.md"
    text = ledger.read_text(encoding="utf-8")
    first = "| `RiemannPrimeResolvent.alpha` | verified | a |\n"
    second = "| `RiemannPrimeResolvent.Space.beta` | verified | b |\n"
    ledger.write_text(text.replace(first + second, second + first), encoding="utf-8")
    assert any("oracle declaration order" in failure for failure in audit(root))


def test_comments_do_not_create_oracle_entries(tmp_path: Path) -> None:
    root = _construction(tmp_path)
    oracle = root / "oracle_check.lean"
    oracle.write_text(
        oracle.read_text(encoding="utf-8")
        + "/- #print axioms RiemannPrimeResolvent.hidden -/\n",
        encoding="utf-8",
    )
    assert audit(root) == []


def test_unlisted_public_source_declaration_is_rejected(tmp_path: Path) -> None:
    root = _construction(tmp_path)
    hidden = root / "support/Hidden.lean"
    hidden.parent.mkdir()
    hidden.write_text(
        "namespace RiemannPrimeResolvent\n"
        "theorem hidden : True := by trivial\n"
        "end RiemannPrimeResolvent\n",
        encoding="utf-8",
    )

    assert any("public source declarations missing from oracle" in failure
               and "RiemannPrimeResolvent.hidden" in failure
               for failure in audit(root))


def test_stale_oracle_declaration_is_rejected(tmp_path: Path) -> None:
    root = _construction(tmp_path)
    source = root / "RiemannPrimeResolvent/Basic.lean"
    source.write_text(
        source.read_text(encoding="utf-8").replace(
            "@[simp] lemma beta : True := by trivial\n", ""
        ),
        encoding="utf-8",
    )

    assert any("missing from public source" in failure
               and "RiemannPrimeResolvent.Space.beta" in failure
               for failure in audit(root))


def test_dependency_cache_theorems_are_not_treated_as_project_source(
    tmp_path: Path,
) -> None:
    root = _construction(tmp_path)
    cached = root / ".lake/packages/dependency/Injected.lean"
    cached.parent.mkdir(parents=True)
    cached.write_text(
        "namespace RiemannPrimeResolvent\n"
        "theorem dependencyOnly : True := by trivial\n"
        "end RiemannPrimeResolvent\n",
        encoding="utf-8",
    )

    assert audit(root) == []
