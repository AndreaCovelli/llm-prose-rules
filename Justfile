set positional-arguments := true

default: test

test:
  uv run ./scripts/test.sh

vale-prose:
  vale --config=.vale.ini --minAlertLevel=error .

vale-commit-fixtures:
  vale --config=.vale-test.ini --ext=.md tests/commits/pass/COMMIT_EDITMSG
  ! vale --config=.vale-test.ini --ext=.md tests/commits/fail/COMMIT_EDITMSG

vale-rule-messages:
  vale --config=.vale-messages.ini styles/llm-prose-rules styles/llm-prose-rules-commits styles/llm-prose-rules-experimental styles/voice-dna

package-release:
  ./scripts/package-release.sh

pre-commit-install:
  uv run pre-commit install --hook-type pre-commit --hook-type commit-msg
