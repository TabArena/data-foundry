---
unique_name: liberty_mutual_fire_peril_loss_cost
name: 'Liberty Mutual Group: Fire Peril Loss Cost (Kaggle 2014)'
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
tags:
- AI-Filled (Verify)
- Two-Regime Zeros
- Larger IID Data
original_source: Kaggle
year: '2014'
domain: insurance
required_split:
- Random (IID)
problem_type: Regression
original_data_state: One Table
source_links:
- https://www.kaggle.com/competitions/liberty-mutual-fire-peril
- https://nycdatascience.com/blog/student-works/property-casualty-loss-cost-data-type-case-study
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. Drafted by an AI assistant on 2026-10-20 from a web search for zero-inflated regression candidates, the source pages and, where the notes say so, the downloaded data. A human must verify the suggestion, the metadata and the notes before relying on them.**

Liberty Mutual's Kaggle competition on commercial fire losses: 452,061 labelled policies (the test half was
never labelled publicly) with 300 normalized, anonymised features in four blocks (17 policy, 9 crime, 37
geodemographic, 236 weather variables) plus `dummy`, a declared "nuisance variable" that recodes `var9`. The target is
"the transformed ratio of loss to total insured value" (data page; the transform is not disclosed), and `var11` is the
weight of the competition's normalized weighted Gini. Measured on the downloaded `train.csv` (2026-10-20): 99.74%
exact zeros, 1,188 positives (0.006 to 25.9), no negatives or missing targets. The blocks are coarse (2,588 distinct
geodemographic vectors, 327 crime vectors) and full of near copies (KazAnova's post in thread 10194).

Split random, as in the competition ("The train and test sets are split randomly"). A 2014 thread suspected a leak in
`id`; Kaggle had randomised the ids (Will Cukierski, thread 10026), and the loss rate is flat over id deciles (0.25-0.28%).
Drop `id` and `dummy`. Untuned LightGBM, 3-fold stratified random CV: AUC 0.70 for a loss, normalized weighted Gini
0.27 (0.20-0.31 by fold; the winner scored 0.332 on the private board), R^2 0.16 on log1p among the ~400 test positives
per fold. The signal is real, but everything the target holds sits in 1,188 positives under an unknown transform, so
the regression is close to rare-event ranking and the 2014 leaderboard reshuffled strongly (thread 10187: "With only
1188 non-zero training examples (<0.3%), overfitting seems inevitable"). Hence 2nd tier. Terms: Kaggle competition
rules. To check: classification of any loss versus weighted regression with `var11`, and whether the geodemographic
vectors (locations) call for a grouped split.

## Reference

Kaggle (2014). Liberty Mutual Group: Fire Peril Loss Cost. https://www.kaggle.com/competitions/liberty-mutual-fire-peril

Lead: web search 2026-10-20 for zero-inflated regression candidates (not in the v4 workbook).
