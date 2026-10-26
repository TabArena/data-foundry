---
unique_name: numerai28_6
name: numerai28.6
checked_by:
- Lennart
data_foundry_status:
- WIP (DF)
claimed_by: Lennart
suggestion: 'Yes'
priority: 2
tags:
- New IID
collections:
- TabArena Reject
- TabSTAR
year: '2017'
source_links:
- https://www.kaggle.com/datasets/numerai/encrypted-stock-market-data-from-numerai
- https://www.openml.org/search?type=data&id=23517
v2_path: datasets/_dev/tabarena-v0pt2/numerai28_6/dataset.py
source_row: 719
type_adapter_id: curation-record-v1
---

## Comments

CC: ""I heard there are many people interested in this dataset. Also, I think there are newer more extensive versions available. However stock market predictions might also be seen as time-series; 
We have roughly 1k unique values per ""numeric"" attribute across the 100k samples. Some weird preprocessing or lag-based behavior might have happened here""

It is stock data, but the decision function we are predicting is independent of the features and thus it is a valid non-iid temporal task

We need to find a version with a timestamp (or treat it as forced IID), but official data or test data from somewhere should be in the future

**Assessment (AI, 2026-10-07):** An older release of the data in `numerai_v5_2` (added as `numerai_v5_2_1m`), so a `Duplicate` of it. The Kaggle file (owner `numerai`: "a sample of the training data used in the Numerai machine learning competition", CC0-1.0) holds 96,320 rows, 21 features and a binary target, with no era or id column, and the file order holds no era blocks (a split on the file order scores ROC AUC 0.526, random splits 0.525-0.528). The timestamp this record asks for exists only in v5.2. OpenML 23517 is the Kaggle sample re-encoded: same shape, class counts (48,658 / 47,662) and feature-target rank correlations; values and row order differ.

**Assessment (AI, 2026-10-20):** priority 1 for the review of the added dataset: gap -, use case -, source -, shape -, risk - (Open issue 1: Duplicate of numerai_v5_2; not added). Older eraless release of numerai_v5_2 with encrypted numeric features; a duplicate with no added benchmark value.

CC (2026-10-22, Lennart): add as forced IID. Not a duplicate of numerai_v5_2: a different release (Numerai's 2016 Kaggle sample, CC0) with different features (21 continuous against 2,748 five-level bins), target (binary against a weekly-ranked 20-day return) and shape, and no row can be matched, so PROV-6 does not apply and it is a distinct task from the same source (PROV-7). The risk of hidden weeks was checked and not found; the source data of that time is worth adding. Added as an IID binary task tagged `ForcedIIDFromTemporal`.

**Assessment (AI, 2026-10-22):** added as `datasets/_dev/tabarena-v0pt2/numerai28_6/` (IID binary, 96,320 x 21, `ForcedIIDFromTemporal` + `Anonymized`, year 2016). Metric: Numerai's 2016 rules rank models "by accuracy (logloss)" (numer.ai/rules, Wayback 2016-08-30), so `Metric.source("log_loss")`; under it untuned LightGBM (0.6945) and random forest (0.6966) lose to the dummy (0.6931), the linear model wins on all 9 splits (0.6916). Bundle checks 0 errors, 0 warnings; leak probes clean (all features ROC AUC 0.516, no exact copies, 1-NN agreement 0.501); hidden-group probe no hit; task probe no flag (linear ROC AUC 0.531). Correction to the 2026-10-07 assessment: OpenML 23517 is not a re-encoding of the Kaggle file but another 2016 sample of the same design (72,404 rows, 36,605 / 35,798, no shared feature row); the record's `year` (2017) should be 2016 (Kaggle dataset id 485, OpenML copy uploaded 2016-07-07). Priority 1: gap -, use case -, source -, shape -, risk 0 (finance binary IID is well covered; the fit is approximate; the Kaggle page is one paragraph; 21 numeric features only; no likely leak).

**Assessment (AI, 2026-10-22):** review panel (focused tier: claim audit, split audit) refuted no validity claim; its text fixes are in the notes (prediction point unstated in 2016; the LEAK-30 quantile bins kept on purpose; the hidden-week residual test; the IID ROC AUC read as an upper bound). dataset check: 0 errors, 0 warnings. Open in REVIEW.md: issue 1 (log loss, the source's metric, against ROC AUC) and the record fields `year` and `tags`. Priority 2: gap 0, use case -, source +, shape +, risk - (no thin domain or regime; encrypted features and a forced IID split; the data owner's CC0 release; 96,320 rows of 21 numeric features; log loss sits within 0.002 of the dummy). Not built yet.

**Assessment (AI, 2026-10-22):** tag `Non-IID (Temporal)` replaced by `New IID`, following the decision to add it as forced IID (the definition carries `ForcedIIDFromTemporal`).

## Reference

Kaggle
