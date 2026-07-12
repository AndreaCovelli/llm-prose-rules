# llm-prose-rules

`llm-prose-rules` is a small Vale profile for cleaning up LLM-assisted prose and commit messages.

It is not an AI detector. It does not produce an authorship score. It flags patterns that often make generated writing vague, padded, or over-styled.

## Layout

```text
styles/
  llm-prose-rules/              # core prose cleanup rules (errors and warnings)
  llm-prose-rules-commits/      # commit-message rules (errors and warnings)
  voice-dna/                    # context-sensitive advisory style rules
  llm-prose-rules-experimental/ # opt-in structural checks
```

The default config enables `llm-prose-rules` and `voice-dna` for Markdown. Commit messages use only `llm-prose-rules-commits`.

## Install hooks

```bash
uv run pre-commit install --hook-type pre-commit --hook-type commit-msg
```

The pre-commit config runs Vale at `error` level, so warnings do not block commits.

## Use as a Vale package

Add the release asset to another repository's `.vale.ini`:

```ini
StylesPath = .styles
Packages = https://github.com/AndreaCovelli/llm-prose-rules/releases/latest/download/llm-prose-rules.zip
```

Then run:

```bash
vale sync
```

The package installs `llm-prose-rules`, `llm-prose-rules-commits`,
`llm-prose-rules-experimental`, `voice-dna`, and the shared Vale `config/`
directory.

## Run checks

```bash
uv run ./scripts/test.sh
uv run python scripts/check-rule-fixtures.py
uv run python scripts/check-metadata.py
./scripts/package-release.sh
./scripts/check-package-parity.sh
vale --config=.vale-messages.ini styles/llm-prose-rules styles/llm-prose-rules-commits styles/llm-prose-rules-experimental styles/voice-dna
vale --config=.vale.ini .
vale --config=.vale.ini --ext=.md --minAlertLevel=error .git/COMMIT_EDITMSG
```

Use the default config for blocking checks. It enables the prose and voice
profiles, while the hooks and test config only fail on `error` alerts.

For a deeper advisory review, run the opt-in profile:

```bash
vale --config=.vale-experimental.ini .
```

The experimental profile adds structural warning rules. Treat those results as
review prompts, not merge blockers. Its grammar-density and structure thresholds
are calibrated for technical prose; recalibrate them against a representative
local corpus before using them for another genre.

If you use `just`:

```bash
just test
just package-release
```

## Rule policy

Hard-fail rules should catch high-confidence patterns: generic openings, directly
removable filler, conversational metacommentary, explicit conclusions, chat
leakage, vague attributions, and commit-message boilerplate.

Warning rules cover context-sensitive choices such as contrast formulas, copula
alternatives, generic transitions, broad vocabulary, punctuation, rhythm, and
personal voice.

Rule calibration lives in `docs/rules.yml`. Review process notes live in
`docs/calibration.md`.

Review vocabulary and voice warnings periodically for drift. LLM-preferred words
change over time, so fixed vocabulary tells should remain advisory unless corpus
review and fixtures justify a blocking rule.

The goal is better writing, not a cleaner detector score.
