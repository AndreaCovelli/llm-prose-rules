# prose-harness

`prose-harness` is a small Vale profile for cleaning up LLM-assisted prose and commit messages.

It is not an AI detector. It does not produce an authorship score. It flags patterns that often make generated writing vague, padded, or over-styled.

## Layout

```text
styles/
  prose-harness/              # blocking prose cleanup rules
  prose-harness-commits/      # blocking commit-message rules
  voice-dna/                  # warning-level personal taste rules
  prose-harness-experimental/ # opt-in structural checks
```

The default config enables `prose-harness` and `voice-dna` for Markdown. Commit messages use only `prose-harness-commits`.

## Install hooks

```bash
pre-commit install --hook-type pre-commit --hook-type commit-msg
```

The pre-commit config runs Vale at `error` level, so warnings do not block commits.

## Run checks

```bash
./scripts/test.sh
python3 scripts/check-rule-fixtures.py
python3 scripts/check-metadata.py
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
review prompts, not merge blockers.

If you use `just`:

```bash
just test
```

## Rule policy

Hard-fail rules should catch high-confidence patterns: generic openings, filler, metacommentary, fake conclusions, chat leakage, contrast formulas, vague attributions, and commit-message boilerplate.

Warning rules cover context-sensitive choices such as broad vocabulary, punctuation, rhythm, and personal voice.

Rule calibration lives in `docs/rules.yml`. Review process notes live in
`docs/calibration.md`.

Review vocabulary and voice warnings periodically for drift. LLM-preferred words
change over time, so fixed vocabulary tells should remain advisory unless corpus
review and fixtures justify a blocking rule.

The goal is better writing, not a cleaner detector score.
