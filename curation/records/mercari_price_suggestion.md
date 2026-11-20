---
unique_name: mercari_price_suggestion
name: mercari_price
checked_by:
- Lennart
- Alex
- Mustafa
- Andrej
data_foundry_status:
- 'DF: Yes'
- BeyondArena
suggestion: 'Yes'
tags:
- Larger IID Data
- Free Text (Sentences)
- 'Samples: Over Time'
- 'Time: Lost'
- 'Target: Varying Delay'
- Database Snapshot
collections:
- TexTabBench
- TabSTAR
- MulTaBench
- STRABLE
original_source: Kaggle
year: '2017'
domain: business & marketing
required_split:
- Random (IID)
problem_type: Regression
original_data_state: One Table
source_links:
- https://www.kaggle.com/datasets/elizabethsam/mercari-price-suggestion-challenge https://www.kaggle.com/competitions/mercari-price-suggestion-challenge/overview
notebook_path: datasets/beyond_iid/new_iid/mercari_price_suggestion/mercari_price_suggestion_1m.ipynb
v2_path: datasets/_dev/tabarena-v0pt2/mercari_price_suggestion/dataset.py
source_row: 658
type_adapter_id: curation-record-v1
---

## Comments

Mercari (Japanese shopping app); a lot of signal from text preprocessing (plus be aware of censoring), maybe create a version after text embeddings to use for benchmarking; likely temporal but all features are IID, so we can use as is; likely many categoricals.

Not sure how useful the name is given the existence of the description, also not sure about category — it could be split into categorical columns but would maybe have way too many.

CC (2026-10-06, Lennart): Kept after the task-probe review: the `no_spread` flag is an artefact of the probe, which leaves text columns out (R^2 0.06 for every family without the 4 text columns). With its text, on BeyondArena (the shipped `_1m` version, one holdout split) the best method (TabPFN-3.5) reaches R^2 0.670 and the median 0.603.

**Assessment (AI, 2026-10-21):** Metric declared under MET-1..13: source rmse — the competition's RMSLE, as RMSE on the shipped log1p(price) (Kaggle evaluation page).

**Assessment (AI, 2026-10-21):** metric now `Metric.source("rmsle", target_transform="log1p")` instead of rmse on the log1p target: the competition's RMSLE on the price, computed after the inverse of the shipped log1p (MET-3); the score is the same number as before. Needs a rebuild to reach the container.

**Assessment (AI, 2026-10-30):** Dtype review (branch ordinal-and-censored-levels; the column decisions with their codebook evidence are on the review board): 1 ordinal scales typed as ordered categories in the codebook's order (CLEAN-14, amended): `item_condition_id` (the README lists their levels).

**Assessment (AI, 2026-11-01):** the benchmark MulTaBench (https://arxiv.org/abs/2605.10616) carries this record's data as "Mercari Marketplace": Text-tabular; AutoML Multimodal 100K subsample (OpenML 46660) of the 2017 Mercari Kaggle competition. Tagged MulTaBench on 2026-11-01.

**Assessment (AI, 2026-11-01):** the benchmark STRABLE (https://arxiv.org/abs/2605.12292) carries this record's data as "Mercari Price Prediction": Raw file mercari_train.tsv from TextTabBench. Subsampled by STRABLE to 75,000 rows. Tagged STRABLE on 2026-11-01.

CC (2026-11-01, Lennart): the decode rule (a code whose codebook says in words what each level is carries the words; a score without them is a number): 2 coded columns carry their words.

CC (2026-11-17, Andrej): the declared split (random, 1x3 folds, `ForcedIIDFromTemporal`) is checked: the split decision tree, walked without the current split, reaches the split it ships (blind split review, cross-dataset item).

CC (2026-11-18, Andrej): the forced tag stays (Review issue 1, A; stationarity reasoning, SPLIT-32 as amended today): no reason to take later samples as interchangeable. A price target in a consumer marketplace is the plainest case against ASR.

## Review

**Outcome:** added. Stationarity reasoning of 2026-11-18: the definition reaches the forced step with no time to measure; decided below.

**Main points:** Keep `ForcedIIDFromTemporal`, or tag `AssumedStationaryRelation`?

**Issues for Andrej:**

1. **Keep `ForcedIIDFromTemporal`, or tag `AssumedStationaryRelation`?**

   * **Problem:**
     - Time: No listing has a date and train_id is a shuffle (every dated product flat across its tenths); product mentions only bound the extract to 2017 before September.
     - Use: The app suggests a price for listings made after the extract (2017), years later in any use today.
     - Mechanism: Second-hand prices are a market: product generations age (iPhone 7 vs 8 already visible), fads come and go (fidget spinners), and price levels move with inflation and supply; time directly changes the feature-to-price relation.
   * **Background:** similar datasets[^asr].

     | Similar dataset or source | What was measured | Verdict | Why similar |
     |---|---|---|---|
     | california_house_prices_2020 / perth_house_prices | split by time in the collection because prices move | temporal splits shipped | a price target |
     | sendy_logistics_challenge | stationary-relation test (v3) | not flat | a marketplace operational target |

   * **For a stationary use case:**
     - Used within the extract's months, item text and condition price similarly.
   * **Against:**
     - Prices and markets.
     - Product cycles: named products in the text lose value as new generations ship.
     - Target: Varying Delay (price known at the sale).
     - An extract of a few months used years later.
   * **Earlier views:**
     - CC (2026-11-17, Andrej): blind walk reaches the shipped random split with ForcedIIDFromTemporal.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep `ForcedIIDFromTemporal` (implemented) | The folds stay; the Time basis line names the reasoning below | Claims only what is known | The split stands for later samples only as far as the use case is stationary |
     | B | `AssumedStationaryRelation` | The folds stay; you give the reason (eight words or more) | Documents why random folds stand for later samples | Prices and markets.; Product cycles: named products in the text lose value as new generations ship. |

   * **Recommendation:** A, a price target in a consumer marketplace is the plainest case against ASR. Confidence: high. **Decision:** A or B?

   [^asr]: **SPLIT-32** (Should; amended 2026-11-18, Andrej): "where it holds none, the review reasons whether the use case can be taken as stationary, from the domain's mechanism and from similar datasets ..., where the AI offers `AssumedStationaryRelation` with a recommendation for a person to decide." `AssumedStationaryRelation` keeps the forced split's folds and replaces only the tag; its line opens `AssumedStationaryRelation (<person>, <date>): <reason>`.

   **Andrej (2026-11-18, ok):** as implemented.

   **Resolved (2026-11-18, Andrej):** A, as implemented: the forced tag stays; the `Time basis:` line gives the reasoning (A price target in a consumer marketplace is the plainest case against ASR.)
