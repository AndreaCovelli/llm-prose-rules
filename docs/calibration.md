# Rule calibration

`prose-harness` is a writing cleanup profile, not an authorship classifier.
Rules should stay narrow enough that a writer can act on each alert without
debating intent.

## Maintenance process

Review vocabulary warnings on a schedule, not as blocking rules. Word choice
changes with model releases, team style, and domain language, so fixed word
lists need more drift review than structural commit or prose rules.

Promote a pattern to blocking only when it is structural, low-noise, and covered
by a fixture in `tests/rules/expected-errors.yml`. A blocking rule needs a clear
rewrite path and should not depend on guessing who wrote the text.

Treat academic word-frequency studies as corpus evidence, not proof for a
single document. Use them to guide review candidates, then validate each rule
against project prose before changing its level.

Record each review in `docs/rules.yml`. Update `last_reviewed`, risk fields, and
the rationale when a rule level changes, coverage changes, or drift review
leaves the rule unchanged.
