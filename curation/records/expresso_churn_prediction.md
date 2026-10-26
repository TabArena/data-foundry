---
unique_name: expresso_churn_prediction
name: expresso-churn-prediction
checked_by:
- Lennart
data_foundry_status:
- 'DF: Yes'
suggestion: 'Yes'
priority: 3
tags:
- Review Prio 1 (Atlas)
- New IID
- Larger IID Data
collections:
- New
original_source: Zindi
year: '2020'
domain: business & marketing
required_split:
- Random (IID)
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://zindi.africa/competitions/expresso-churn-prediction/data
- https://zindi.africa/competitions/dsn-pre-bootcamp-hackathon-expresso-churn-prediction-challenge
- https://zindi.africa/competitions/customer-churn-prediction-learning-experience/data
- https://zindi.africa/competitions/expresso-churn-prediction-challenge
- https://zindi.africa/competitions/microsoft-x-dsn-free-ai-classes-in-every-city-hackathon-expresso-churn-prediction/data
v2_path: datasets/_dev/tabarena-v0pt2/expresso_churn_prediction_1m/dataset.py
source_row: 912
type_adapter_id: curation-record-v1
---

## Comments

Expresso (telecom operator in Senegal & Mauritania) customer churn prediction (Zindi). One row per customer (~2.5M) with usage/tenure features aggregated over a 90-day window; target is binary churn. No explicit per-row time index, so a random split is plausible; verify there is no hidden temporal leakage from the aggregation window. Real telco data with a clear task → likely usable for the benchmark, pending verification of size after cleaning and of the split regime.

Lennart: solved with IID in the competition, and all features are set up to be IID. Need to check train-test region drift or similar, otherwise likely a valid task in this setting with all features being well-defined

**Assessment (AI, 2026-10-07):** There is no train-test drift. user_id is the SHA-1 hash of the extract's row number, and Zindi's Test.csv is a uniform random 15% of the extract. A model separating the two files scores ROC AUC 0.500, so the IID split stands.

REGION is dropped. Among churners it is missing for 92-95% at every level of activity (1 to 62 active days), while among stayers the share falls from 67% to 7%. The field looks filled after the observation window. Without it, ROC AUC falls from 0.93 to 0.90.

The Azubian (1,077,024 rows) and DSN (400,000 rows) cuts are rows of this Train.csv. On Zindi, indabax_eswatini_2022 lists the Azubian file and has this competition as its parent.

**Assessment (AI, 2026-10-20):** priority 3 for the review of the added dataset: gap -, use case -, source +, shape +, no known risk. Large real telco churn file from the operator's own competition, leaky REGION removed; churn tasks are common and the fit approximate.

**Assessment (AI, 2026-10-20):** review panel (full): ship after changes, no data change; applied the `ForcedIIDFromTemporal` tag (SPLIT-8, cost of the missing time axis not measurable), REGION's drop reasoned by the measured mechanism (its missing flag separates churners at ROC AUC 0.936 among customers active on all 62 days, no window column above 0.59), the start of the 90-day churn period written as inferred, the fit text (80.9% of churners had no revenue in the window; no tenure under 3 months), the citation moved to the first release (UmojaHack Ghana, 27 June 2020, https://zindi.africa/competitions/umojahack-ghana-expresso-churn-prediction-challenge, same Train.csv), LEAK-18 cited for the duplicates, wording. Priority 3: gap -, use case -, source +, shape +, risk 0 (no thin domain, problem type or regime; approximate fit; Zindi page and codebook by the operator; 1.5M customers with categorical features; the open label-timing question is a stated uncertainty, no leak shown).

**Assessment (AI, 2026-10-21):** Metric declared under MET-1..13: source roc_auc — the Zindi challenge's evaluation metric, Area Under the Curve (AUC).

CC (2026-10-22, Lennart): issue 5: keep ARPU_SEGMENT as released (CLEAN-5 not triggered, as `dzclass`). Issue 6: ships with the start of the 90-day churn period as a stated risk (inferred, the other reading named in the notes).

CC (2026-10-22, Lennart): issue 1: confirm the REGION drop (LEAK-10).

**Assessment (AI, 2026-10-22):** all issues settled (REGION dropped, ARPU_SEGMENT kept, churn timing a stated risk); REVIEW.md removed. kick's `WheelType`, marked keep the same day on the same test, is put back to the curator as a consistency check in kick's REVIEW.md; if it is kept by an amendment, REGION is reopened. Not built yet.

CC (2026-10-26, Lennart): verdict ship.

## Reference

Zindi
