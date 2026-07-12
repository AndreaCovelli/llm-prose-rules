# Evidence notes

This repo is a prose cleanup harness, not an authorship detector.

Kobak et al. show that excess style-word usage can estimate LLM influence across large corpora. That supports warning-level vocabulary rules, especially for words that spike across many papers. The reference below now points to the peer-reviewed publication rather than its earlier preprint.

Geng, Dong, and Poibeau show that word preferences shift across models and over time. Older markers can fade while newer markers appear. That supports a small, editable rule set instead of a fixed detector score.

Wikipedia's maintained editorial guide catalogs practical artifacts such as AI
self-reference, response cutoffs, unfinished placeholders, follow-up offers,
formulaic headings, and bold-label lists. It is useful as a candidate-pattern
catalog, not as proof of authorship; this repo keeps ambiguous formatting cases
at warning level.

Corpus studies also report grammatical tendencies such as information-dense noun
phrases, participial clauses, nominalizations, and phrasal coordination. These
are population-level tendencies that vary by genre, so they support experimental
density checks rather than per-instance blocking rules.

The practical rule is simple: hard-fail patterns that usually make prose worse,
and warn on patterns that need human judgment. Calibration fixtures should use
ordinary project prose as negative evidence, not only generated examples as
positive evidence.

## References

- Dmitry Kobak, Rita Gonzalez-Marquez, Emoke-Agnes Horvat, and Jan Lause. "Delving into LLM-assisted writing in biomedical publications through excess vocabulary." *Science Advances*, 2025. https://www.science.org/doi/10.1126/sciadv.adt3813
- Alex Reinhart, Ben Markey, Michael Laudenbach, Kachatad Pantusen, Ronald Yurko, Gordon Weinberg, and David West Brown. "Do LLMs write like humans? Variation in grammatical and rhetorical styles." *Proceedings of the National Academy of Sciences*, 2025. https://www.pnas.org/doi/10.1073/pnas.2422455122
- Mingmeng Geng, Yuhang Dong, and Thierry Poibeau. "Beyond Via: Analysis and Estimation of the Impact of Large Language Models in Academic Papers." arXiv:2603.25638, 2026. https://arxiv.org/abs/2603.25638
- Wikipedia contributors. "Signs of AI writing." https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing
