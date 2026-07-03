# Evidence notes

This repo is a prose cleanup harness, not an authorship detector.

Kobak et al. show that excess style-word usage can estimate LLM influence across large corpora. That supports warning-level vocabulary rules, especially for words that spike across many papers.

Geng, Dong, and Poibeau show that word preferences shift across models and over time. Older markers can fade while newer markers appear. That supports a small, editable rule set instead of a fixed detector score.

The practical rule is simple: hard-fail patterns that usually make prose worse, and warn on patterns that need human judgment.

## References

- Dmitry Kobak, Rita Gonzalez-Marquez, Emoke-Agnes Horvat, and Jan Lause. "Delving into LLM-assisted writing in biomedical publications through excess vocabulary." arXiv:2406.07016, 2024. https://arxiv.org/abs/2406.07016
- Mingmeng Geng, Yuhang Dong, and Thierry Poibeau. "Beyond Via: Analysis and Estimation of the Impact of Large Language Models in Academic Papers." arXiv:2603.25638, 2026. https://arxiv.org/abs/2603.25638
