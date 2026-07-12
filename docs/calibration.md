# Rule calibration

`llm-prose-rules` is a writing cleanup profile, not an authorship classifier.
Rules should stay narrow enough that a writer can act on each alert without
debating intent.

## Maintenance process

Review vocabulary warnings on a schedule, not as blocking rules. Word choice
changes with model releases, team style, and domain language, so fixed word
lists need more drift review than structural commit or prose rules.

Promote a pattern to blocking only when it is structural, low-noise, and covered
by an exact alert fixture in `tests/rules/expected-alerts.yml`. A blocking rule
needs a clear rewrite path and should not depend on guessing who wrote the text.

Every rule needs a positive fixture at its configured severity. Calibration
fixtures also include ordinary or near-miss prose, and the harness rejects extra
matches, duplicate matches, incorrect severities, and invalid source spans.
Experimental script fixtures should exercise both sides of each threshold before
a threshold changes.

The grammar-density and structure thresholds are calibrated for technical prose,
not as universal genre baselines. Keep them in the experimental profile, and
recalibrate against representative local documents before using them in another
genre. A corpus-level tendency is not evidence that any individual sentence was
machine-written.

Treat academic word-frequency studies as corpus evidence, not proof for a
single document. Use them to guide review candidates, then validate each rule
against project prose before changing its level.

Record each review in `docs/rules.yml`. Update `last_reviewed`, risk fields, and
the rationale when a rule level changes, coverage changes, or drift review
leaves the rule unchanged.
