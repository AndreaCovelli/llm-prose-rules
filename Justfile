set positional-arguments := true

default: test

test:
  ./scripts/test.sh

vale-prose:
  vale --config=.vale.ini --minAlertLevel=error .

vale-commit-fixtures:
  vale --config=.vale-test.ini --ext=.md tests/commits/pass/COMMIT_EDITMSG
  ! vale --config=.vale-test.ini --ext=.md tests/commits/fail/COMMIT_EDITMSG

pre-commit-install:
  pre-commit install --hook-type pre-commit --hook-type commit-msg

