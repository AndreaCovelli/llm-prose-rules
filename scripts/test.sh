#!/usr/bin/env bash
set -euo pipefail

root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$root"

vale --config=.vale-test.ini --minAlertLevel=error tests/prose/pass

if vale --config=.vale-test.ini --minAlertLevel=error tests/prose/fail; then
  echo "Expected tests/prose/fail to produce blocking Vale alerts." >&2
  exit 1
fi

vale --config=.vale-test.ini --ext=.md --minAlertLevel=error tests/commits/pass/COMMIT_EDITMSG

if vale --config=.vale-test.ini --ext=.md --minAlertLevel=error tests/commits/fail/COMMIT_EDITMSG; then
  echo "Expected tests/commits/fail/COMMIT_EDITMSG to produce blocking Vale alerts." >&2
  exit 1
fi

python3 scripts/check-rule-fixtures.py
python3 scripts/check-metadata.py
./scripts/package-release.sh >/dev/null
./scripts/check-package-parity.sh

vale --config=.vale-messages.ini styles/llm-prose-rules styles/llm-prose-rules-commits styles/llm-prose-rules-experimental styles/voice-dna

if command -v uv >/dev/null 2>&1 && uv --version >/dev/null 2>&1; then
  uv run pre-commit run --all-files
elif command -v pre-commit >/dev/null 2>&1 && pre-commit --version >/dev/null 2>&1; then
  pre-commit run --all-files
else
  echo "Skipping pre-commit check: uv and pre-commit are not installed or not configured."
fi
