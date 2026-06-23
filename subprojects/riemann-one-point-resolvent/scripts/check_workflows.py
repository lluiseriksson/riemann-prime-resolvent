#!/usr/bin/env python3
"""Audit CI and installer surfaces for reproducible, least-privilege usage.

Remote GitHub Actions must use immutable 40-character commit SHAs. Workflows
must declare permissions, avoid mutable hosted-runner aliases, and disable
checkout credential persistence. Repository shell/Docker surfaces are also
checked for network downloads piped directly to interpreters.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORKFLOW_GLOBS = (".github/workflows/*.yml", ".github/workflows/*.yaml")
FULL_SHA_RE = re.compile(r"\A[0-9a-f]{40}\Z")
USES_RE = re.compile(r"^\s*-?\s*uses:\s*([^\s#]+)")
FORBIDDEN_EVENT_RE = re.compile(r"^\s*pull_request_target\s*:", re.MULTILINE)
NETWORK_PIPE_RE = re.compile(
    r"\b(?:curl|wget)\b[^\n|]*\|\s*(?:sudo\s+)?(?:sh|bash|dash|zsh|python|python3)\b"
)
PROCESS_SUBSTITUTION_RE = re.compile(
    r"\b(?:sh|bash|python|python3)\s+<\([^\n]*(?:curl|wget)\b"
)
MUTABLE_RAW_REF_RE = re.compile(
    r"raw\.githubusercontent\.com/[^/]+/[^/]+/(?:main|master)/"
)
MUTABLE_RUNNER_RE = re.compile(
    r"^\s*runs-on:\s*(?:ubuntu|windows|macos)-latest\s*(?:#.*)?$", re.MULTILINE
)
TOP_LEVEL_PERMISSIONS_RE = re.compile(r"^permissions\s*:", re.MULTILINE)
WRITE_ALL_RE = re.compile(r"^\s*permissions\s*:\s*write-all\s*(?:#.*)?$", re.MULTILINE)
PERSIST_FALSE_RE = re.compile(r"^\s*persist-credentials\s*:\s*false\s*(?:#.*)?$")
RUNS_ON_RE = re.compile(r"^(\s*)runs-on\s*:")
TIMEOUT_RE = re.compile(r"^\s*timeout-minutes\s*:\s*([0-9]+)\s*(?:#.*)?$")


def workflow_files(root: Path) -> list[Path]:
    files: list[Path] = []
    for directory in [root, root / "subprojects/riemann-one-point-resolvent"]:
        if directory.is_dir():
            for pattern in WORKFLOW_GLOBS:
                files.extend(directory.glob(pattern))
    return sorted(set(path.resolve() for path in files))


def installer_policy_files(root: Path) -> list[Path]:
    files: set[Path] = set()
    for directory in [root, root / "subprojects/riemann-one-point-resolvent"]:
        if not directory.is_dir():
            continue
        dockerfile = directory / "Dockerfile"
        if dockerfile.is_file():
            files.add(dockerfile.resolve())
        scripts = directory / "scripts"
        if scripts.is_dir():
            files.update(path.resolve() for path in scripts.glob("*.sh") if path.is_file())
    return sorted(files)


def _relative(path: Path, root: Path) -> str:
    try:
        return path.resolve().relative_to(root.resolve()).as_posix()
    except ValueError:
        return path.as_posix()


def _is_workflow(path: Path) -> bool:
    return path.suffix.lower() in {".yml", ".yaml"} and ".github" in path.parts and "workflows" in path.parts


def _checkout_step_body(lines: list[str], start: int) -> list[str]:
    line = lines[start]
    base_indent = len(line) - len(line.lstrip())
    body: list[str] = []
    for following in lines[start + 1 :]:
        if not following.strip() or following.lstrip().startswith("#"):
            body.append(following)
            continue
        indent = len(following) - len(following.lstrip())
        if indent <= base_indent:
            break
        body.append(following)
    return body


def audit_text(path: Path, text: str, root: Path) -> list[str]:
    failures: list[str] = []
    rel = _relative(path, root)
    executable_text = "\n".join(
        "" if line.lstrip().startswith("#") else line for line in text.splitlines()
    )

    if NETWORK_PIPE_RE.search(executable_text) or PROCESS_SUBSTITUTION_RE.search(executable_text):
        failures.append(f"{rel}: network download piped/executed by an interpreter is forbidden")
    if MUTABLE_RAW_REF_RE.search(executable_text):
        failures.append(f"{rel}: raw.githubusercontent.com main/master references are forbidden")

    if not _is_workflow(path):
        return failures

    if FORBIDDEN_EVENT_RE.search(text):
        failures.append(f"{rel}: pull_request_target is forbidden")
    if TOP_LEVEL_PERMISSIONS_RE.search(text) is None:
        failures.append(f"{rel}: workflow must declare top-level permissions")
    if WRITE_ALL_RE.search(text):
        failures.append(f"{rel}: permissions: write-all is forbidden")
    if MUTABLE_RUNNER_RE.search(text):
        failures.append(f"{rel}: hosted runner must use a fixed image label, not *-latest")

    lines = text.splitlines()
    for index, line in enumerate(lines):
        runner_match = RUNS_ON_RE.match(line)
        if runner_match:
            base_indent = len(runner_match.group(1))
            timeout: int | None = None
            for following in lines[index + 1 :]:
                if not following.strip() or following.lstrip().startswith("#"):
                    continue
                indent = len(following) - len(following.lstrip())
                if indent < base_indent:
                    break
                match_timeout = TIMEOUT_RE.match(following)
                if match_timeout and indent == base_indent:
                    timeout = int(match_timeout.group(1))
                    break
            if timeout is None:
                failures.append(f"{rel}:{index + 1}: job must declare timeout-minutes")
            elif timeout < 1 or timeout > 120:
                failures.append(
                    f"{rel}:{index + 1}: timeout-minutes must be between 1 and 120"
                )

    for index, line in enumerate(lines):
        match = USES_RE.match(line)
        if not match:
            continue
        lineno = index + 1
        reference = match.group(1).strip('"\'')
        if reference.startswith("./"):
            continue
        if "@" not in reference:
            failures.append(f"{rel}:{lineno}: action reference has no @ ref: {reference}")
            continue
        action, ref = reference.rsplit("@", 1)
        if not action or not ref:
            failures.append(f"{rel}:{lineno}: malformed action reference: {reference}")
            continue
        if FULL_SHA_RE.fullmatch(ref) is None:
            failures.append(
                f"{rel}:{lineno}: action must be pinned by 40-char commit SHA, not {ref!r}"
            )
            continue

        if action == "actions/checkout":
            body = _checkout_step_body(lines, index)
            if not any(PERSIST_FALSE_RE.match(candidate) for candidate in body):
                failures.append(
                    f"{rel}:{lineno}: actions/checkout must set persist-credentials: false"
                )
    return failures


def audit_repository(root: Path) -> tuple[list[Path], list[str]]:
    root = root.resolve()
    workflows = workflow_files(root)
    policy_files = sorted(set(workflows + installer_policy_files(root)))
    failures: list[str] = []
    if not workflows:
        failures.append("no GitHub workflow files found")
    for path in policy_files:
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError) as exc:
            failures.append(f"{_relative(path, root)}: cannot read as UTF-8: {exc}")
            continue
        failures.extend(audit_text(path, text, root))
    return policy_files, failures


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    args = parser.parse_args()
    files, failures = audit_repository(args.root)
    if failures:
        print("Workflow/supply-chain audit FAILED:", file=sys.stderr)
        print("\n".join(f"- {failure}" for failure in failures), file=sys.stderr)
        return 1
    print(f"Workflow/supply-chain audit passed for {len(files)} policy files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
