#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
METADATA_PATH = ROOT / "docs" / "rules.yml"
RULE_GLOB = "styles/*/*.yml"
REQUIRED_FIELDS = {
    "path",
    "level",
    "category",
    "confidence",
    "false_positive_risk",
    "drift_risk",
    "source",
    "last_reviewed",
    "rationale",
}
LEVELS = {"suggestion", "warning", "error"}
CATEGORIES = {"prose", "commit", "voice", "experimental"}
RISK_VALUES = {"low", "medium", "high"}
CONFIDENCE_VALUES = {"low", "medium", "high"}


def main() -> int:
    with METADATA_PATH.open(encoding="utf-8") as handle:
        data = yaml.safe_load(handle) or {}

    entries = data.get("rules") if isinstance(data, dict) else None
    if not isinstance(entries, list):
        print(f"{METADATA_PATH} must contain a top-level 'rules' list.", file=sys.stderr)
        return 1

    ok = True
    by_path: dict[str, dict[str, object]] = {}
    for index, entry in enumerate(entries, start=1):
        if not isinstance(entry, dict):
            print(f"rules[{index}] must be a mapping.", file=sys.stderr)
            ok = False
            continue

        missing = REQUIRED_FIELDS - set(entry)
        extra = set(entry) - REQUIRED_FIELDS
        path = entry.get("path", f"rules[{index}]")
        if missing:
            print(f"{path}: missing fields: {', '.join(sorted(missing))}", file=sys.stderr)
            ok = False
        if extra:
            print(f"{path}: unsupported fields: {', '.join(sorted(extra))}", file=sys.stderr)
            ok = False

        if not isinstance(entry.get("path"), str):
            print(f"rules[{index}]: path must be a string.", file=sys.stderr)
            ok = False
            continue

        path = str(entry["path"])
        if path in by_path:
            print(f"{path}: duplicate metadata entry.", file=sys.stderr)
            ok = False
        by_path[path] = entry

        rule_file = ROOT / path
        if not rule_file.is_file():
            print(f"{path}: metadata references a missing rule file.", file=sys.stderr)
            ok = False
            continue

        with rule_file.open(encoding="utf-8") as handle:
            rule = yaml.safe_load(handle) or {}
        actual_level = rule.get("level")
        if entry.get("level") != actual_level:
            print(
                f"{path}: metadata level {entry.get('level')!r} does not match rule level {actual_level!r}.",
                file=sys.stderr,
            )
            ok = False

        if entry.get("level") not in LEVELS:
            print(f"{path}: unsupported level {entry.get('level')!r}.", file=sys.stderr)
            ok = False
        if entry.get("category") not in CATEGORIES:
            print(f"{path}: unsupported category {entry.get('category')!r}.", file=sys.stderr)
            ok = False
        if entry.get("confidence") not in CONFIDENCE_VALUES:
            print(f"{path}: unsupported confidence {entry.get('confidence')!r}.", file=sys.stderr)
            ok = False
        for field in ("false_positive_risk", "drift_risk"):
            if entry.get(field) not in RISK_VALUES:
                print(f"{path}: unsupported {field} {entry.get(field)!r}.", file=sys.stderr)
                ok = False

        if not isinstance(entry.get("source"), str) or not entry["source"].strip():
            print(f"{path}: source must be a non-empty string.", file=sys.stderr)
            ok = False
        if not isinstance(entry.get("last_reviewed"), str) or not entry["last_reviewed"].strip():
            print(f"{path}: last_reviewed must be a non-empty string.", file=sys.stderr)
            ok = False
        if not isinstance(entry.get("rationale"), str) or not entry["rationale"].strip():
            print(f"{path}: rationale must be a non-empty string.", file=sys.stderr)
            ok = False

    rule_paths = {str(path.relative_to(ROOT)) for path in sorted(ROOT.glob(RULE_GLOB))}
    metadata_paths = set(by_path)
    for path in sorted(rule_paths - metadata_paths):
        print(f"{path}: missing metadata entry.", file=sys.stderr)
        ok = False
    for path in sorted(metadata_paths - rule_paths):
        print(f"{path}: metadata does not correspond to a rule file.", file=sys.stderr)
        ok = False

    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
