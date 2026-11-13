---
unique_name: online_shoppers_purchasing_intention_dataset
name: Online Shoppers Purchasing Intention Dataset
checked_by:
- Lennart
- Andrej
data_foundry_status:
- 'DF: Yes'
- TabArena (v0.1)
- BeyondArena
suggestion: 'Yes'
tags:
- 'Samples: Over Time'
- 'Time: Dated'
- 'Target: Later'
original_source: UCI
year: '2018'
required_split:
- Random (IID)
source_links:
- https://doi.org/10.24432/C5F88Q
notebook_path: datasets/beyond_iid/old_iid/online_shoppers_purchasing_intention_dataset/online_shoppers_purchasing_intention_dataset.ipynb
v2_path: datasets/_dev/tabarena-v0pt2/online_shoppers_purchasing_intention_dataset/dataset.py
type_adapter_id: curation-record-v1
---

## Comments

Clean canonical entry bootstrapped from the TabArena curation workbook ('Tabular' row). Shipped in TabArena (v0.1) / BeyondArena.

TabArena curation verdict: Tabular.

Shopping prediction (also like a recommender system task); special preprocessing to avoid impact of time; sloved with an LSTM; 

available on OpenML

Click stream data. Study title is Real-time prediction of online shoppers’ purchasing intention using multilayer perceptron and LSTM - so original data was time-series or at least temporal. dataset consists of feature vectors belonging to 12,330 sessions. 

The dataset was formed so that each session would belong to a different user in a 1-year period to avoid any tendency to a specific campaign, special day, user profile, or period. Although there is a temporal component, the task is conceptualized s.t. the samples are iid. However, I am unsure whether the task is conceptualized correctly regarding the delayed target prediction. The features and the target should have a delay - otherwise it is meaningless to predict a purchase after it already happened

Potential issue: Temporal Task?

Lennart: very likely a temporal task and maybe even grouped

Andrej: temporal task, but the features used for the tabular task are time-invariant. If the task was conceptualized correctly, a temporal split is not needed

CC (2026-10-01, Lennart): Leak audit: kept `PageValues`, dropped the February-May sessions instead (12,330 -> 6,875 rows).
- `PageValues` is meant as a historical Google Analytics page metric, "stored in the application database ... and updated automatically at regular intervals", averaged over the pages a session visits (Sakar et al. 2019, Sec. 2.1 and Sec. 3). Used that way it is a valid real-time feature.
- But the data has two regimes. February-May (5,455 rows): all 560 buyers have PageValues > 0, PageValues alone gives AUC 0.974 (LightGBM 0.981, 0.823 without it). June-December (6,875 rows): 370 of 1,348 buyers (27%) have PageValues = 0, PageValues alone gives AUC 0.814 (LightGBM 0.875, 0.739 without it). Most likely the page-value table was computed over the early period, so the early buyers' own purchases credited their pages; the later values behave like the intended historical metric. A change in site tracking could leave a similar pattern, so this is not proven.
- `SpecialDay` is non-zero only in February and May and is dropped as constant.
- Split: IID (required_split set to Random (IID)): each session belongs to a different user sampled over one year (Sec. 2.1) and only the month is known, so a temporal split would mainly test extrapolation to unseen months.

**Assessment (AI, 2026-10-19):** open since the leak audit of 2026-10-01: 40 exact duplicate rows remain after the February-May sessions were dropped. To decide in the next pass: drop them as collection copies (with the share in the notes) or keep them as natural repeats.

**Assessment (AI, 2026-10-21):** Metric declared under MET-1..13: fallback roc_auc — Sakar et al. 2019 report accuracy, TPR, TNR and F1 (F1 stressed over accuracy, full text paywalled); no fixed threshold or costs. Original rejected: F1. roc_auc is the binary fallback.

**Assessment (AI, 2026-10-30):** Dtype review (branch ordinal-and-censored-levels; the column decisions with their codebook evidence are on the review board): 1 ordinal scales typed as ordered categories in the codebook's order (CLEAN-14, amended): `Month` (the README lists their levels).

**Assessment (AI, 2026-10-31):** better data: the data-scouting run of 2026-10-30/31 found better data for the same task: `ga_merchandise_store_sessions` (TBD -> Yes, priority 2). Each is screened in its own record; this record's verdict stays the curator's.

CC (2026-11-01, Lennart): the target rule (CLEAN-25) and the cut-end rule (CLEAN-14): the target ships as No/Yes, Yes the event (True means revenue).

CC (2026-11-13, Andrej): collection fact `Target: Later` (Review issue 4, B): whether the visit ends in a purchase, which closes the session the features describe, so it arrives after the features; the forced tag and the split stay.

## Review

**Outcome:** added. The AI asks which time basis fits now that `CrossSectional` names a present state (2026-11-13).

**Main points:** Nothing open: issue 4 resolved on 2026-11-13 (`Target: Later` recorded).

**Issues for Andrej:**

4. **Record `Target: Later`?**

   * **Problem:**
     - The record names no `Target:` fact, which reads as a target measured with the features.
     - The label is whether the visit ends in a purchase, which closes the session the features describe: it arrives after the features, and the forced tag already treats the use case as forward.
   * **Background:** asked on 2026-11-13 together with `CrossSectional`, which was dropped the same day; the fact stays useful, since the `Target:` facts decide between `DelayedTarget` and a forced tag and start the leak checks.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Leave as is (implemented) | no `Target:` fact | no change | the record contradicts the label's timing |
     | B | Record `Target: Later` | the record gains the fact; tag and split stay | the record says when the label arrives; the facts guard can check it | none found |

   * **Recommendation:** B. **Decision:** A or B?

   **Notes for the AI:** on B, add `Target: Later` to the record with a CC line; the definition does not change.

   **Andrej (2026-11-13, change):** Option B: Record Target: Later.

   **Resolved (2026-11-13, Andrej):** B. The record has `Target: Later`; the forced tag and the split stay.

## Reference

Real-time prediction of online shoppers’ purchasing intention using multilayer perceptron and LSTM recurrent neural networks
By C. O. Sakar, S. Polat, Mete Katircioglu, Yomi Kastro. 2019

Published in Neural computing & applications (Print)
