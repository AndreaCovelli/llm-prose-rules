# Evidence notes

This repo is a prose cleanup harness, not an authorship detector.

Kobak et al., arXiv:2406.07016, show that excess style-word usage can estimate LLM influence across large corpora. That supports warning-level vocabulary rules, especially for words that spike across many papers.

Geng, Dong, and Poibeau, arXiv:2603.25638, show that word preferences shift across models and over time. Older markers can fade while newer markers appear. That supports a small, editable rule set instead of a fixed detector score.

The practical rule is simple: hard-fail patterns that usually make prose worse, and warn on patterns that need human judgment.

