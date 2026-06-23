#!/usr/bin/env python3
"""Open the four research-frontier issues idempotently through the GitHub API.

Dry-run is the default. Use --apply with a GITHUB_TOKEN that has Issues write
permission. Existing issues are identified by their stable frontier marker.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_REPOSITORY = "lluiseriksson/riemann-prime-resolvent"
ISSUE_FILES = (
    "docs/research-frontier/issues/RF-1-prime-tail.md",
    "docs/research-frontier/issues/RF-2-slit-plane.md",
    "docs/research-frontier/issues/RF-3-spectral-model.md",
    "docs/research-frontier/issues/RF-4-convergence.md",
)

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")


def issue_payload(path: Path) -> dict[str, object]:
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    if not lines or not lines[0].startswith("# "):
        raise ValueError(f"{path}: first line must be a Markdown title")
    return {"title": lines[0][2:].strip(), "body": "\n".join(lines[2:]).strip() + "\n"}


def request_json(url: str, token: str, *, method: str = "GET", payload=None):
    data = None if payload is None else json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(
        url,
        data=data,
        method=method,
        headers={
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {token}",
            "X-GitHub-Api-Version": "2022-11-28",
            "User-Agent": "riemann-prime-resolvent-closeout",
        },
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.loads(response.read().decode("utf-8"))


def existing_markers(repository: str, token: str) -> dict[str, str]:
    result: dict[str, str] = {}
    page = 1
    while True:
        query = urllib.parse.urlencode({"state": "all", "per_page": 100, "page": page})
        values = request_json(f"https://api.github.com/repos/{repository}/issues?{query}", token)
        if not values:
            break
        for item in values:
            if "pull_request" in item:
                continue
            body = item.get("body") or ""
            for frontier_id in ("RF-1", "RF-2", "RF-3", "RF-4"):
                if f"<!-- frontier-id: {frontier_id} -->" in body:
                    result[frontier_id] = item["html_url"]
        if len(values) < 100:
            break
        page += 1
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repository", default=DEFAULT_REPOSITORY)
    parser.add_argument("--apply", action="store_true", help="create missing issues")
    args = parser.parse_args()

    payloads = [issue_payload(ROOT / relative) for relative in ISSUE_FILES]
    if not args.apply:
        print(json.dumps(payloads, indent=2, ensure_ascii=False))
        print("\nDry-run only. Re-run with --apply and GITHUB_TOKEN to create issues.")
        return 0

    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        print("GITHUB_TOKEN is required with --apply", file=sys.stderr)
        return 2
    try:
        existing = existing_markers(args.repository, token)
        for payload in payloads:
            body = str(payload["body"])
            frontier_id = next(
                value for value in ("RF-1", "RF-2", "RF-3", "RF-4")
                if f"<!-- frontier-id: {value} -->" in body
            )
            if frontier_id in existing:
                print(f"{frontier_id}: already exists at {existing[frontier_id]}")
                continue
            created = request_json(
                f"https://api.github.com/repos/{args.repository}/issues",
                token,
                method="POST",
                payload=payload,
            )
            print(f"{frontier_id}: created {created['html_url']}")
    except (OSError, ValueError, urllib.error.HTTPError, json.JSONDecodeError) as exc:
        print(f"Issue creation FAILED: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
