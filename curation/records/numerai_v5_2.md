---
unique_name: numerai_v5_2
name: numerai v5.2
checked_by:
- Lennart
data_foundry_status:
- WIP (DF)
claimed_by: Lennart
suggestion: 'Yes'
priority: 2
decision_markers:
- Needs extensive data wrangling
tags:
- Non-IID (Temporal)
- Review Prio 1 (Atlas)
collections:
- New (BeyondArena)
original_source: Company
year: '2025'
domain: finance
required_split:
- Temporal (NON-IID)
problem_type: Regression
original_data_state: One Table
source_links:
- https://github.com/numerai/example-scripts/tree/master/numerai
v2_path: datasets/_dev/tabarena-v0pt2/numerai_v5_2_1m/dataset.py
source_row: 706
type_adapter_id: curation-record-v1
---

## Comments

temporal split on era, likely need to add feature neutralization: https://github.com/numerai/example-scripts/blob/master/numerai/feature_neutralization.ipynb?

**Assessment (AI, 2026-10-07):** Added as `numerai_v5_2_1m`: eras 1-1235 (6.88M stock-weeks), target `target_ender_20` (the `target` of v5.2), Numerai's 780 `medium` features, three 52-era test windows after Numerai's 4-era embargo. The signal is real but tiny: a LightGBM shaped like Numerai's example model correlates 0.006-0.018 per era with the target (t = 3-9), yet its R² stays at or below 0.0003, so RMSE mostly ranks shrinkage towards 0.5. The 75 Faith features were designed over two test windows (+0.002-0.004 per era; noted). Feature neutralization post-processes predictions, not data. Licence: Numerai's Terms of Service §4.2 allow use "solely for the purpose of participating in Tournaments" and forbid redistribution. numerai28_6 is an older, era-less release.

**Assessment (AI, 2026-10-20):** priority 2 for the review of the added dataset: gap -, use case -, source +, shape +, risk - (Issue 3: 75 Faith features designed with test-era targets, kept as a potential leak). Large anonymised temporal finance panel with real but tiny signal; RMSE mostly ranks shrinkage.

## Reference

Website https://numer.ai/data/v5.2
