from __future__ import annotations

import sys
from pathlib import Path

import pytest

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPOSITORY_ROOT / "scripts"))

from check_no_placeholders import LeanLexError, audit_text, mask_lean_source  # noqa: E402


def labels(text: str) -> list[str]:
    return [finding.label for finding in audit_text(text)]


def test_comments_and_plain_strings_are_ignored() -> None:
    text = '''
/- outer sorry
   /- nested axiom hidden : Prop -/
-/
-- admit
#check "unsafe theorem fake : True"
theorem safe : True := by trivial
'''
    assert audit_text(text) == []


def test_escaped_quote_does_not_end_string_early() -> None:
    text = 'def message := "not a \\"sorry\\" proof"\ntheorem safe : True := by trivial\n'
    assert audit_text(text) == []


def test_interpolated_expression_remains_auditable() -> None:
    text = 'def bad := s!"value: {by sorry}"\n'
    findings = audit_text(text, path="Demo.lean")
    assert [(finding.path, finding.line, finding.label) for finding in findings] == [
        ("Demo.lean", 1, "sorry")
    ]


@pytest.mark.parametrize(
    ("source", "expected"),
    [
        ("theorem t : True := by sorry\n", "sorry"),
        ("theorem t : True := by admit\n", "admit"),
        ("axiom hidden : False\n", "axiom"),
        ("unsafe lemma hidden : True := by trivial\n", "unsafe theorem"),
    ],
)
def test_forbidden_constructs_are_reported(source: str, expected: str) -> None:
    findings = audit_text(source)
    assert [finding.label for finding in findings] == [expected]
    assert findings[0].line == 1
    assert findings[0].column > 0


def test_identifier_substrings_are_not_false_positives() -> None:
    assert labels("def sorryFree := True\ndef axiomatic := True\n") == []


def test_mask_preserves_newlines_and_length() -> None:
    text = 'def x := "sorry"\n/- axiom\n   /- admit -/\n-/\ntheorem ok : True := by trivial\n'
    masked = mask_lean_source(text)
    assert len(masked) == len(text)
    assert masked.count("\n") == text.count("\n")


def test_unterminated_nested_comment_is_rejected() -> None:
    with pytest.raises(LeanLexError, match="unterminated block comment"):
        mask_lean_source("/- outer /- inner -/")


def test_unterminated_string_is_rejected() -> None:
    with pytest.raises(LeanLexError, match="unterminated string"):
        mask_lean_source('def x := "unterminated')
