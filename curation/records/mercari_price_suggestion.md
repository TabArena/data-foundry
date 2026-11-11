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

CC (2026-11-11, Andrej): BeyondArena v0.2 review page, mercari_price_suggestion:
- Issue 1 (price $0), B: the 874 listings priced $0 are dropped; the price is what the item sold for, no sale is free, and no other listing is below $3; 1,481,612 listings remain.
- Issue 2 (time basis), B: the random split is tagged `ForcedIIDFromTemporal`; the listings came in over a period of 2017 and the app prices later ones, but no listing has a date and `train_id` is a shuffle. The leak test across the split passes (0.01% of test rows have a twin in training). The `Time basis:` line is in the curation notes, and the task summary names the forced split.

## Review

**Outcome:** added. Mercari's Kaggle competition (2017): 1,482,486 listings of second-hand items on the Mercari app
with their name, condition, category, brand, shipping and the seller's description; the target is the log price,
scored by the competition's RMSLE, with a random split as in the competition (the release has no dates). The AI
recommends shipping it after dropping the listings priced $0 (issue 1). Reviewed without a panel, from the gathered
evidence (the record, the definition, the task-probe review) and two checks of the rows; there is no model run on
it. Validity: the host's own task with a direct fit (the app suggests a price when an item is listed); prices written
in the text are masked by the host as "[rm]" (in 9% of descriptions), so the text gives no price away; about 870
listings carry a price of $0, which no sale has (issue 1). Value: with its text the methods separate (on the shipped
1M version, R² 0.670 for the best method, 0.603 for the median; Lennart, 2026-10-06); the `no_spread` flag came from
probes that leave the text out. Quality: no other open point. Weighed: a host's documented task, a real decision,
text-heavy rows that test encoders +; no dates, so the split cannot follow time -.

**Main points:** Both issues resolved (2026-11-09): the 874 listings priced $0 are dropped, 1,481,612 remain (1); the
random split is tagged as forced from temporal (2).

**Record judgment:** valid. The record's notes are settled: the text columns stay strings, the full table is taken
(about 1.48M rows, so no sub-sample), and the metric is the competition's RMSLE on the price.

**Issues for Andrej:**

1. **Drop the listings with a price of $0?**

   * **Problem:**
     - About 870 listings (0.06%) have a price of $0, while no other listing is below $3; the competition calls the
       price "the price that the item was sold for", and no sale is free.
     - In log terms each such row is about 8.4 squared units away from a typical prediction, so these rows carry
       about 2.6% of the squared error of a good model and score how methods miss a price no listing explains.
     - Drop them, or keep the source's rows?
   * **Background:** the counts come from the shipped 1.25M-row sample (735 rows at $0, 15,752 at the minimum of $3,
     none in between), scaled to the full table. A public script of the competition ("Mercari code golf",
     https://gist.github.com/pjankiewicz/8b0e9ea3238252c169574c524da67cde) drops them before training with
     `train[train['price'] > 0]`. An impossible target value is a missing target, and a row without a target goes[^1a].
   * **Experiments:** for a model at R² 0.67, the $0 rows raise the RMSLE from 0.431 to 0.436 (computed from the
     sample's price distribution).
   * **Unknown:** whether the competition's hidden test set held $0 prices; its labels were never published.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep them (implemented) | 1,482,486 listings | the host's rows as released | scores a price no sale has; about 2.6% of a good model's error |
     | B | Drop them | about 870 listings go | every row a real sale price; follows the competition's public code | departs from the release by 0.06% of rows |

   * **Recommendation:** B, drop them: a price of $0 is no sale price the app would suggest. **Decision:** drop (B),
     or keep (A)?

   **Notes for the AI:** on B, `df = df[df["price"] > 0]` in `_clean` before the log, a curation note with the count,
   and `changes` in the task summary; re-run `dataset check`.

   [^1a]: **CLEAN-11** (Should): impossible values become missing; a row whose target is not the task's quantity may
     leave. **CLEAN-15** (Must): drop rows with a missing target. **CLEAN-1** (Should): read what the source's top
     solutions did and adopt the rules that hold for the train and the test period alike.

   **Resolved (2026-11-09, Andrej):** B, drop them. `_clean` keeps `df["price"] > 0` before the log, which drops 874
   listings (0.06%; all 874 priced $0 in train.tsv, none of them a duplicate), so 1,481,612 remain. A curation note
   gives the count and the reason, and the task summary's `changes` and row count say so; the record has a CC line.
   `dataset check` 0 errors; not rebuilt.

   **Andrej (2026-11-11, change):** Option B: Drop them.

   **Resolved (2026-11-11, Andrej):** B again. The working copy's definition did not carry the change yet, so it
   was applied here: `_clean` keeps `df["price"] > 0` before the log (874 listings, 0.06%), `row` reads 1,481,612
   listings and `changes` names the drop. `dataset check`: 0 errors, 0 warnings, 1 info (94 conflicting duplicate
   rows, 0.0%).

2. **Time basis: tag the random split as forced from temporal?**

   * **Problem:**
     - Sellers listed items over a period the host never states and each price is known when the item sold; the text dates the listings to 2017 before September (the iPhone 8 in 10 of 1.48M listings, against 9,281 for the iPhone 7), but no listing carries a date and `train_id` is a shuffle, so the time is lost.
     - The record's collection facts hold (`Samples: Over Time`, `Time: Lost`, `Target: Varying Delay`); the definition splits at random, as the competition did, and names no time basis.
     - The app suggests prices for listings made after its training data, and prices and fashions move within months, so the five questions give the forced tag[^2a].
   * **Background:**
     - Products with known dates bound the period: Galaxy S8 (April 2017) in 729 listings, Nintendo Switch (March
       2017) in 245, fidget spinners (the craze of spring 2017) in 2,637, the iPhone 8 (September 2017) in 10, the
       iPhone X (November 2017) in 1.
     - Each of these products takes the same share in every tenth of `train_id` (fidget spinners 1.7 to 2.0 per
       1,000 listings, Christmas 9.9 to 10.5), and the mean log price is flat (2.977 to 2.982), so the id order is no
       time axis.
     - No prototype fits: the use case prices new listings rather than filling in a past period, and the listings
       share no prediction moment.
   * **Experiments:** the leak test across the split, on Kaggle's train.tsv (1,482,535 listings): 280 listings
     (0.02%) repeat another listing's name, condition, category, brand, shipping and description, and only 35% of
     those groups share one price; under a random 3-fold split 0.01% of test rows have such a twin in training. No
     seller id ships, so repeat sellers cannot be checked.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | No time basis (implemented) | as now | nothing to write | `dataset check` notes a split that is not temporal without a basis; the drift a deployed model meets unstated |
     | B | Forced from temporal | `ForcedIIDFromTemporal` and a `Time basis:` line with the period markers and the leak test | says that new listings are the use and the dates are missing; the leak test passes | none found |
     | C | Snapshot | `Snapshot` and its line | the extract is probably a few months of 2017 | the app prices new listings, not a past period |

   * **Recommendation:** B. **Decision:** A, B or C?

   **Notes for the AI:** once PR #50 is in this working copy, on B: `data_tags = ("ForcedIIDFromTemporal",)` and in
   `curation_comments` the bullet `- Time basis: ForcedIIDFromTemporal: listings made over a period the host does not
   state, each price known at the sale; the app prices listings made later. Product mentions date the extract to 2017
   before September (Galaxy S8 729 listings, fidget spinners 2,637, the iPhone 8 10 against 9,281 for the iPhone 7),
   but no listing has a date and train_id is a shuffle (every dated product flat across its tenths) (Time: Lost). Leak
   test across the split: 280 listings (0.02%) repeat another's fields and text, 0.01% of test rows have such a twin in
   training. Listing dates would allow a split by time.`; the `split` sentence names the forced split; `dataset
   check`. Scripts of the time review of 2026-11-06: `markers.py`, `dups.py`.

   [^2a]: **SPLIT-32** (Should): the record's collection facts and the five questions; a `Snapshot` only fills in a
     time the data covers; samples over time whose period moves the target, with the time lost, get a forced split.
     **SPLIT-8** (Must): the closest regime, tagged as forced from temporal, after a leak test across the split.

   **Resolved (2026-11-09, Andrej):** B, forced from temporal. `data_tags = ("ForcedIIDFromTemporal",)`, the drafted
   `Time basis: ForcedIIDFromTemporal:` bullet is in `curation_comments`, and the task summary's `split` names the
   forced split (the listings came in over a period but carry no dates, so the test data stands for other listings of
   the same period, not later ones). The record has a CC line. `dataset check` 0 errors; not rebuilt.

   **Andrej (2026-11-11, change):** Option B: Forced from temporal.

   **Resolved (2026-11-11, Andrej):** B again. Applied in the working copy's definition: `data_tags =
   ("ForcedIIDFromTemporal",)`, the `Time basis: ForcedIIDFromTemporal:` bullet in `curation_comments`, and the
   task summary's `split` names the forced split. `dataset check`: 0 errors.
