---
unique_name: numerai28_6
name: numerai28.6
checked_by:
- Lennart
suggestion: 'Yes'
priority: 1
tags:
- Non-IID (Temporal)
collections:
- TabArena Reject
- TabSTAR
year: '2017'
source_links:
- https://www.kaggle.com/datasets/numerai/encrypted-stock-market-data-from-numerai
- https://www.openml.org/search?type=data&id=23517
source_row: 719
type_adapter_id: curation-record-v1
---

## Comments

CC: ""I heard there are many people interested in this dataset. Also, I think there are newer more extensive versions available. However stock market predictions might also be seen as time-series; 
We have roughly 1k unique values per ""numeric"" attribute across the 100k samples. Some weird preprocessing or lag-based behavior might have happened here""

It is stock data, but the decision function we are predicting is independent of the features and thus it is a valid non-iid temporal task

We need to find a version with a timestamp (or treat it as forced IID), but official data or test data from somewhere should be in the future

**Assessment (AI, 2026-10-07):** An older release of the data in `numerai_v5_2` (added as `numerai_v5_2_1m`), so a `Duplicate` of it. The Kaggle file (owner `numerai`: "a sample of the training data used in the Numerai machine learning competition", CC0-1.0) holds 96,320 rows, 21 features and a binary target, with no era or id column, and the file order holds no era blocks (a split on the file order scores ROC AUC 0.526, random splits 0.525-0.528). The timestamp this record asks for exists only in v5.2. OpenML 23517 is the Kaggle sample re-encoded: same shape, class counts (48,658 / 47,662) and feature-target rank correlations; values and row order differ.

**Open issues (AI, 2026-10-07):** not added; duplicate. An older release of the data in `numerai_v5_2`, without
eras.

1. **Mark the record `No` + `Duplicate` of `numerai_v5_2`** (`numerai_v5_2_duplicate` under the `_duplicate`
   convention)? Nothing was implemented. The alternative is a forced-IID definition (`ForcedIIDFromTemporal`,
   binary, 96,320 x 21, ROC AUC about 0.53). A random split there mixes rows of the same unknown weeks, which share
   the market state.

   **Lennart (2026-10-22, discuss):** Is this a duplicate? It is different data from a different release and likely a
   somewhat different task? Can you double check and see if we cannot add it? In general the source data from that
   point in time is good and likely still cool to add, and as far as I recall different enough.
   **Answer (AI, 2026-10-22):** checked: not a duplicate under the rules; it can be added as a forced-IID task. It is
   Numerai's 2016 Kaggle sample (owner `numerai`, CC0-1.0; OpenML 23517 is a re-upload): 96,320 rows, 21 encrypted
   continuous features in [0, 1], a binary target, no era, id or date column. numerai_v5_2 differs in features (780
   of 2,748 five-level bins), target (20-day return ranked within each week) and shape, and no row can be matched,
   so PROV-6 (a cut or version of one table with no distinct task) does not apply; it is a distinct task from the
   same source (PROV-7). The risk was hidden weeks, which inflated numerai_v5_2's IID scores; none shows here: the
   file order is shuffled (block target means 0.494-0.521, lag-1 autocorrelation of every feature at most 0.007, a
   row's position block predicted at chance 0.1005), 1-NN target agreement 0.501 against 0.502 at random (v5.2:
   0.618), the hidden-group probe finds nothing, and grouping by k-means clusters as stand-in weeks moves LightGBM's
   ROC AUC by at most 0.0055. The signal is small but real: ROC AUC 0.531 (logistic regression) and 0.524 (LightGBM)
   on 5 random folds (fold SD about 0.003), the same on file-order blocks. Proposal: add it as an IID binary task
   tagged `ForcedIIDFromTemporal`, scored by ROC AUC, the unmeasurable shared weekly market state named in the notes.
   Alternative: keep `No` + `Duplicate` if one Numerai use case should enter once. Decision: add (it goes to
   /add-dataset), or keep `No`.

2. **Noted only (a licence is never a verdict reason):** the 2016 Kaggle sample is CC0-1.0, while v5.2 falls under
   Numerai's Terms of Service, section 4.2 (see `numerai_v5_2`, issue 1).

**Assessment (AI, 2026-10-20):** priority 1 for the review of the added dataset: gap -, use case -, source -, shape -, risk - (Open issue 1: Duplicate of numerai_v5_2; not added). Older eraless release of numerai_v5_2 with encrypted numeric features; a duplicate with no added benchmark value.

## Reference

Kaggle
