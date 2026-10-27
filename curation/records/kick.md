---
unique_name: kick
name: kick / CAR_BAD_BUY_KICK
checked_by:
- Andrej
- Lennart
data_foundry_status:
- 'DF: Yes'
- BeyondArena
suggestion: 'Yes'
tags:
- Non-IID (Temporal)
collections:
- TabArena Reject
- TabSTAR
original_source: Kaggle
year: '2011'
domain: business & marketing
required_split:
- Temporal (NON-IID)
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://www.kaggle.com/c/DontGetKicked/overview
- https://www.openml.org/search?type=data&id=41162&sort=runs&status=active
notebook_path: datasets/beyond_iid/temporal/kick/kick.ipynb
v2_path: datasets/_dev/tabarena-v0pt2/kick/dataset.py
source_row: 723
type_adapter_id: curation-record-v1
---

## Comments

CC: "Is from a competition, nice tabular data task. Might require temporal split or some time-invariant feature engineering; original data has more features that are interesting (like KickDate) but unclear if this makes it temporal; kickdate only in description in data. Need to check original data for more, but likely we could ignore time and group-based problems after preprocessing the original data; likely we can ignore temporal impact. No (after preprocessing)."

Old competition without clear restriction on data usage. Can assume public domain

The competition used a random split

CC (2026-10-01, Lennart): Leak audit:
- **Split:** the temporal split stays. The Kaggle train/test split was neither temporal nor grouped: both cover Jan 2009 - Dec 2010 (test is 36-44% of every quarter), and 78.9% of test rows sit at an auction location (Auction + VNZIP1) that is also in train (72 of 128 test locations). The earlier claim that the competition grouped by Auction and VNZIP1 came from a notebook check that compared train "Auction + VNZIP1" with test "VNZIP1" only (0 overlap by construction); the curation comments are corrected. A grouped split would test unseen auctions, but a model is deployed on future purchases at mostly known auctions.
- **WheelType, potential leak kept on purpose:** missing WheelType is likely blanked when a car is kicked back: missing for 24.9% of bad buys in every month vs 1.5% of good cars, erratically (Sep-Oct 2010: 1 good vs 218 bad). Dropping WheelType/WheelTypeID: LightGBM AUC on our temporal splits 0.757 -> 0.691. Kept because the company released the data this way for the competition (missing in 4.5% of Kaggle test rows vs 4.3% of train) and the recording process is not documented. Revisit if it is.
- The note above that "the competition used a random split" is closer to the truth than the old curation comment.

CC (2026-10-21, Lennart): "Reopen kick here": the LEAK-38 consistency check of WheelType against expresso's REGION drop (LEAK-10) is reopened; the open question is issue 1 of the folder's REVIEW.md.

**Assessment (AI, 2026-10-21):** expresso's conditional test on WheelType (training.csv, 72,983 cars): missing for 1.2-1.7% of good buys in every band of age, odometer and price, 21-39% of bad buys; a model fit on good buys from the auction-time covariates predicts 1.2% missing for bad buys, 24.9% observed (expresso: 11% vs 94%). The missing flag alone gives ROC AUC 0.617 overall, 0.60-0.63 in each shipped test window, pooled within auction 0.573, within auction and purchase date 0.572; by auction ADESA 0.734 (47.7% of bad vs 1.0% of good missing), OTHER 0.712, MANHEIM 0.522; Trim's and the MMR prices' missing flags stay at 0.49-0.54. LightGBM on the 9 shipped windows: 0.677 without WheelType/WheelTypeID, 0.750 with the flag only, 0.750 with both columns. Recommend dropping both under LEAK-10, as expresso dropped REGION; the curator has the call. Fit set to direct under the amended USE-8 (the fit_reason named only this kept leak); it stays direct if the columns are dropped. Aside: PRIMEUNIT/AUCGUART are filled from Oct 2010 mostly for good buys (Dec 2010: 51.9% of good, 12.4% of bad; the host's test file 46.0%), so their missing flag separates bad buys at 0.57-0.70 in the last months.

CC (2026-10-21, Lennart): the declared metric documents the original use case's metric; overrule it only when it is biased or wrong (evidence from the paper); keep the note of the original metric (TP-6 amended).

**Assessment (AI, 2026-10-21):** metric stays the default `roc_auc`: the competition scored the Gini index (Kaggle API: "Gini Index"), which for a binary target is a linear function of ROC AUC and ranks models the same. The notes now name the Gini. Needs a rebuild to reach the container (notes only).

CC (2026-10-21, Lennart): ok on the follow-up item: a strong kept leak does not make the fit approximate (USE-8 amended); the kept leak is named in `fit_reason` as kept, not as a gap.

**Assessment (AI, 2026-10-21):** fit stays `direct` (set earlier today); the kept missing WheelType is worth ROC AUC +0.066 (0.757 with, 0.691 without).

CC (2026-10-21, Lennart): "yes we should have one clear way to treat 0/1 flags": every 0/1 flag (a feature holding only 0 and 1, plus missing values; booleans too) is categorical (CLEAN-14, amended). Typed categorical here: IsOnlineSale.

**Assessment (AI, 2026-10-21):** Metric declared under MET-1..13: source roc_auc — Gini index (Kaggle normalized Gini) (https://www.kaggle.com/competitions/DontGetKicked/overview/evaluation).

CC (2026-10-22, Lennart): issue 1: (a), drop `WheelType` and `WheelTypeID` under LEAK-10, consistent with expresso's REGION, and note it clearly. Issue 2: follow issue 1, so drop `PRIMEUNIT` and `AUCGUART` as well.

**Assessment (AI, 2026-10-22):** the four fields are dropped in `_clean`, with the conditional tests in the notes (WheelType: 1.2% predicted missing for bad buys, 24.9% observed; PRIMEUNIT/AUCGUART from October 2010: 42.3% predicted filled for bad buys, 7.8% observed) and why the host's test file does not keep them. LEAK-38's scope is amended (only fields whose timing cannot be tested) and a LEAK-10 mechanisms row names kick and expresso. LightGBM on the 9 windows: ROC AUC 0.750 with WheelType, 0.677 without (2026-10-21 run). REVIEW.md removed. Not built yet.

## Reference

faysal, Will Adams, and Will Cukierski. Don't Get Kicked!. https://kaggle.com/competitions/DontGetKicked, 2011. Kaggle.
