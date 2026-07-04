#!/usr/bin/env bash
set -euo pipefail

root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$root"

vale --config=.vale-test.ini tests/prose/pass

if vale --config=.vale-test.ini tests/prose/fail; then
  echo "Expected tests/prose/fail to produce blocking Vale alerts." >&2
  exit 1
fi

vale --config=.vale-test.ini --ext=.md tests/commits/pass/COMMIT_EDITMSG

if vale --config=.vale-test.ini --ext=.md tests/commits/fail/COMMIT_EDITMSG; then
  echo "Expected tests/commits/fail/COMMIT_EDITMSG to produce blocking Vale alerts." >&2
  exit 1
fi

vale --config=.vale-messages.ini styles/llm-prose-rules styles/llm-prose-rules-commits styles/llm-prose-rules-experimental styles/voice-dna

if command -v pre-commit >/dev/null 2>&1 && pre-commit --version >/dev/null 2>&1; then
  pre-commit run --all-files
else
  echo "Skipping pre-commit check: pre-commit is not installed or not configured."
fi
