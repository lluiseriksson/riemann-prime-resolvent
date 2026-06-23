from __future__ import annotations

import sys
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

from check_oracle_coverage import (  # noqa: E402
    ALLOWED_AXIOMS,
    audit,
    parse_axiom_report,
)


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


def _valid_report() -> str:
    return (
        "oracle_check.lean:3:0: information: "
        "'RiemannPrimeResolvent.alpha' does not depend on any axioms\n"
        "oracle_check.lean:4:0: information: "
        "'RiemannPrimeResolvent.Space.beta' depends on axioms: "
        "[Classical.choice, Quot.sound, propext]\n"
    )


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


def test_runtime_axiom_report_accepts_only_standard_kernel_axioms(
    tmp_path: Path,
) -> None:
    root = _construction(tmp_path)
    assert ALLOWED_AXIOMS == frozenset({"Classical.choice", "Quot.sound", "propext"})
    assert audit(root, report_text=_valid_report()) == []


def test_runtime_axiom_report_rejects_project_axioms(tmp_path: Path) -> None:
    root = _construction(tmp_path)
    report = _valid_report().replace(
        "[Classical.choice, Quot.sound, propext]",
        "[Classical.choice, RiemannPrimeResolvent.hiddenAxiom]",
    )
    failures = audit(root, report_text=report)
    assert any("non-admitted axioms" in failure
               and "RiemannPrimeResolvent.hiddenAxiom" in failure
               for failure in failures)


def test_runtime_axiom_report_rejects_sorry_ax_and_sorry_warning(
    tmp_path: Path,
) -> None:
    root = _construction(tmp_path)
    report = _valid_report().replace(
        "[Classical.choice, Quot.sound, propext]", "[sorryAx]"
    ) + "warning: declaration uses 'sorry'\n"
    failures = audit(root, report_text=report)
    assert any("sorry warning" in failure for failure in failures)
    assert any("sorryAx" in failure for failure in failures)


def test_runtime_axiom_report_requires_exact_order_and_coverage(
    tmp_path: Path,
) -> None:
    root = _construction(tmp_path)
    lines = _valid_report().splitlines(keepends=True)
    failures = audit(root, report_text="".join(reversed(lines)))
    assert any("report order" in failure for failure in failures)

    missing = audit(root, report_text=lines[0])
    assert any("missing from Lean report" in failure for failure in missing)


def test_axiom_report_parser_tolerates_ansi_and_rejects_duplicates() -> None:
    report = "\x1b[1m'x' depends on axioms: [propext]\x1b[0m\n"
    assert parse_axiom_report(report)[0].axioms == frozenset({"propext"})

    duplicate = "'x' depends on axioms: [propext, propext]\n"
    try:
        parse_axiom_report(duplicate)
    except RuntimeError as exc:
        assert "duplicate axiom" in str(exc)
    else:
        raise AssertionError("duplicate axiom report was accepted")
