#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import sys
from collections import Counter
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[1]
EXPECTED_PATH = ROOT / "tests" / "rules" / "expected-alerts.yml"
RULE_DIRECTORIES = (
    ROOT / "styles" / "llm-prose-rules",
    ROOT / "styles" / "llm-prose-rules-commits",
    ROOT / "styles" / "llm-prose-rules-experimental",
    ROOT / "styles" / "voice-dna",
)


def load_expected() -> dict[str, list[dict[str, str]]]:
    with EXPECTED_PATH.open(encoding="utf-8") as handle:
        data = yaml.safe_load(handle) or {}
    if not isinstance(data, dict):
        raise SystemExit(f"{EXPECTED_PATH} must contain a mapping.")

    expected: dict[str, list[dict[str, str]]] = {}
    for path, entries in data.items():
        if not isinstance(entries, list):
            raise SystemExit(f"{path}: expected alerts must be a list.")

        alerts: list[dict[str, str]] = []
        for index, entry in enumerate(entries, start=1):
            if not isinstance(entry, dict):
                raise SystemExit(f"{path}[{index}]: expected alert must be a mapping.")
            if set(entry) != {"check", "severity", "match"}:
                raise SystemExit(
                    f"{path}[{index}]: expected alert fields are check, severity, and match."
                )
            if not all(isinstance(entry[field], str) for field in entry):
                raise SystemExit(f"{path}[{index}]: expected alert values must be strings.")
            if entry["severity"] not in {"suggestion", "warning", "error"}:
                raise SystemExit(f"{path}[{index}]: invalid severity {entry['severity']!r}.")
            alerts.append(entry)
        expected[str(path)] = alerts
    return expected


def alert_key(alert: dict[str, Any]) -> tuple[str, str, str]:
    return (
        str(alert.get("Check", "")),
        str(alert.get("Severity", "")),
        str(alert.get("Match", "")),
    )


def format_alerts(alerts: Counter[tuple[str, str, str]]) -> list[str]:
    return [
        f"{count}x {check} ({severity}) matching {match!r}"
        for (check, severity, match), count in sorted(alerts.items())
    ]


def validate_span(path: str, alert: dict[str, Any]) -> str | None:
    span = alert.get("Span")
    line = alert.get("Line")
    match = alert.get("Match")
    if (
        not isinstance(span, list)
        or len(span) != 2
        or not all(isinstance(column, int) for column in span)
        or not isinstance(line, int)
        or not isinstance(match, str)
    ):
        return "alert has an invalid Line, Span, or Match field"

    start_column, end_column = span
    if line < 1 or start_column < 1 or end_column < start_column or not match:
        return f"alert has an invalid location: line={line}, span={span}, match={match!r}"

    lines = (ROOT / path).read_text(encoding="utf-8").splitlines(keepends=True)
    if line > len(lines):
        return f"alert line {line} is beyond the fixture's {len(lines)} lines"

    source_from_span = "".join(lines[line - 1 :])[start_column - 1 :]
    if not source_from_span.startswith(match):
        return (
            f"reported span line={line}, columns={span} does not point to match {match!r}"
        )

    # Vale reports inclusive columns for single-line matches. Check the exact
    # endpoint when possible; multi-line raw matches use the final-line column.
    if "\n" not in match and end_column - start_column + 1 != len(match):
        return f"reported span {span} has the wrong width for match {match!r}"
    return None


def expected_rule_checks() -> set[str]:
    return {
        f"{directory.name}.{path.stem}"
        for directory in RULE_DIRECTORIES
        for path in directory.glob("*.yml")
    }


def missing_experimental_pass_fixtures() -> list[str]:
    pass_directory = ROOT / "tests" / "rules" / "experimental-pass"
    experimental_directory = ROOT / "styles" / "llm-prose-rules-experimental"
    return [
        path.stem
        for path in sorted(experimental_directory.glob("*.yml"))
        if not (pass_directory / f"{path.stem}.md").is_file()
    ]


def main() -> int:
    expected = load_expected()
    paths = sorted(expected)
    missing = [path for path in paths if not (ROOT / path).is_file()]
    if missing:
        for path in missing:
            print(f"Missing fixture: {path}", file=sys.stderr)
        return 1

    fixture_paths = {
        str(path.relative_to(ROOT))
        for path in (ROOT / "tests" / "rules").rglob("*.md")
    }
    unlisted = sorted(fixture_paths - set(paths))
    if unlisted:
        for path in unlisted:
            print(f"Fixture is missing from {EXPECTED_PATH}: {path}", file=sys.stderr)
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

    ok = True
    for path in paths:
        expected_counter = Counter(
            (entry["check"], entry["severity"], entry["match"])
            for entry in expected[path]
        )
        actual_alerts = alerts_by_file.get(path, [])
        actual_counter = Counter(alert_key(alert) for alert in actual_alerts)
        if actual_counter != expected_counter:
            ok = False
            print(
                f"{path}: expected {format_alerts(expected_counter)}, "
                f"got {format_alerts(actual_counter)}",
                file=sys.stderr,
            )
        for alert in actual_alerts:
            span_error = validate_span(path, alert)
            if span_error:
                ok = False
                print(f"{path}: {span_error}", file=sys.stderr)

    unexpected_files = sorted(set(alerts_by_file) - set(paths))
    for path in unexpected_files:
        ok = False
        print(f"Unexpected Vale output for {path}", file=sys.stderr)

    covered_checks = {
        entry["check"]
        for alerts in expected.values()
        for entry in alerts
    }
    rule_checks = expected_rule_checks()
    missing_rule_fixtures = sorted(rule_checks - covered_checks)
    for check in missing_rule_fixtures:
        ok = False
        print(f"Missing positive fixture for {check}", file=sys.stderr)
    unknown_checks = sorted(covered_checks - rule_checks)
    for check in unknown_checks:
        ok = False
        print(f"Fixture references unknown rule {check}", file=sys.stderr)
    for rule_name in missing_experimental_pass_fixtures():
        ok = False
        print(f"Missing experimental threshold near-miss fixture for {rule_name}", file=sys.stderr)

    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
