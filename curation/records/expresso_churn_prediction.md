---
unique_name: expresso_churn_prediction
name: expresso-churn-prediction
checked_by:
- Lennart
- Andrej
data_foundry_status:
- 'DF: Yes'
suggestion: 'Yes'
priority: 3
tags:
- Review Prio 1 (Atlas)
- New IID
- Larger IID Data
- 'Samples: One Moment'
- 'Target: Later'
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

CC (2026-10-21, Lennart): the declared metric stays as it is (`roc_auc`), although the first competition (UmojaHack Ghana 2020) scored log loss and its 2021 re-run on the same files ROC AUC (cross-dataset item "Metrics still to settle").

CC (2026-10-22, Lennart): issue 5: keep ARPU_SEGMENT as released (CLEAN-5 not triggered, as `dzclass`). Issue 6: ships with the start of the 90-day churn period as a stated risk (inferred, the other reading named in the notes).

CC (2026-10-22, Lennart): issue 1: confirm the REGION drop (LEAK-10).

**Assessment (AI, 2026-10-22):** all issues settled (REGION dropped, ARPU_SEGMENT kept, churn timing a stated risk); REVIEW.md removed. kick's `WheelType`, marked keep the same day on the same test, is put back to the curator as a consistency check in kick's Review; if it is kept by an amendment, REGION is reopened. Not built yet.

CC (2026-10-26, Lennart): verdict ship.

**Assessment (AI, 2026-10-30):** Dtype review (branch ordinal-and-censored-levels; the column decisions with their codebook evidence are on the review board): 1 ordinal scales typed as ordered categories in the codebook's order (CLEAN-14, amended): `TENURE` (the README lists their levels).

## Review

**Outcome:** added as `expresso_churn_prediction_1m`. The AI asks to retag the time basis after the one-moment rule was sharpened (2026-11-13).

**Main points:** Retag `DelayedTarget` instead of `ForcedIIDFromTemporal`?

**Issues for Andrej:**

1. **Retag `DelayedTarget` instead of `ForcedIIDFromTemporal`, now that a one-moment release is forced only when its target is of that moment?**

   * **Problem:**
     - The definition is tagged `ForcedIIDFromTemporal` (the review panel, 2026-10-20), from when every release with too few periods was forced[^8a-x].
     - Every row is predicted at one shared moment, the end of one observation window of about three months, and the target arrives after it, with the 90 days without activity after it that define churn, a window that has closed for every customer, which is a `DelayedTarget`[^32a-x].
     - The tag alone changes: the split stays random.
   * **Background:** every row is a different customer active in that one window, and Zindi releases no earlier or later window.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep `ForcedIIDFromTemporal` (implemented) | the tag and its line stay | the decision of 2026-10-20 stands | the tag says time was lost, which the one shared moment contradicts |
     | B | `DelayedTarget` | the tag and its `Time basis:` line name the shared moment and the target's window | follows the record's facts and the sharpened rule; no window was ever available to measure | changes a decided tag |

   * **Recommendation:** B. **Decision:** A or B?

   **Notes for the AI:** on B, swap the tag in `data_tags` and write the `Time basis:` line as SPLIT-32 asks for a `DelayedTarget` (the moment, the window, closed for every row, what the split cannot test: the next moment); add a CC line; the split code does not change.

   [^8a-x]: **SPLIT-8** (Must, sharpened 2026-11-13): a release that is one moment, every row predicted at the same point, is forced only when its use case looks forward from a target of that moment or of unknown timing; otherwise SPLIT-32 gives it `Retrospective` or `DelayedTarget`.
   [^32a-x]: **SPLIT-32** (Should): `DelayedTarget` is one shared prediction moment with the target arriving after it, in a window closed for every row; a random or grouped split then draws train and test from that one moment and window.

## Reference

Zindi
