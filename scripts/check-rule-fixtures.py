#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
EXPECTED_PATH = ROOT / "tests" / "rules" / "expected-errors.yml"


def load_expected() -> dict[str, set[str]]:
    with EXPECTED_PATH.open(encoding="utf-8") as handle:
        data = yaml.safe_load(handle) or {}
    if not isinstance(data, dict):
        raise SystemExit(f"{EXPECTED_PATH} must contain a mapping.")

    expected: dict[str, set[str]] = {}
    for path, checks in data.items():
        if isinstance(checks, str):
            checks = [checks]
        if not isinstance(checks, list) or not all(isinstance(check, str) for check in checks):
            raise SystemExit(f"{path}: expected checks must be a string or list of strings.")
        expected[str(path)] = set(checks)
    return expected


def main() -> int:
    expected = load_expected()
    paths = sorted(expected)
    missing = [path for path in paths if not (ROOT / path).is_file()]
    if missing:
        for path in missing:
            print(f"Missing fixture: {path}", file=sys.stderr)
        return 1

    command = ["vale", "--output=JSON", "--config=.vale-test.ini", *paths]
    result = subprocess.run(command, cwd=ROOT, text=True, capture_output=True, check=False)
    if result.returncode not in (0, 1):
        print(result.stderr, file=sys.stderr, end="")
        print(result.stdout, file=sys.stderr, end="")
        return result.returncode

    try:
        alerts_by_file = json.loads(result.stdout or "{}")
    except json.JSONDecodeError as exc:
        print(f"Vale did not return valid JSON: {exc}", file=sys.stderr)
        print(result.stdout, file=sys.stderr, end="")
        print(result.stderr, file=sys.stderr, end="")
        return 1

    actual = {
        path: {
            alert["Check"]
            for alert in alerts_by_file.get(path, [])
            if alert.get("Severity") == "error"
        }
        for path in paths
    }

    ok = True
    for path in paths:
        if actual[path] != expected[path]:
            ok = False
            print(
                f"{path}: expected {sorted(expected[path])}, got {sorted(actual[path])}",
                file=sys.stderr,
            )

    unexpected_files = sorted(set(alerts_by_file) - set(paths))
    for path in unexpected_files:
        ok = False
        print(f"Unexpected Vale output for {path}", file=sys.stderr)

    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
