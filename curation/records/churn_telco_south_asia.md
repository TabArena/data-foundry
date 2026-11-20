---
unique_name: churn_telco_south_asia
name: CHURN_TELCO_SOUTH_ASIA
checked_by:
- Lennart
- Andrej
data_foundry_status:
- 'DF: Yes'
suggestion: 'Yes'
tags:
- New IID
- 'Samples: One Moment'
- 'Target: Later'
- Database Snapshot
collections:
- TabSTAR
original_source: Kaggle
year: '2017'
collection_period: Aug 2015 - Sep 2015
domain: business & marketing
required_split:
- Random (IID)
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://www.openml.org/search?type=data&id=44227
- https://www.kaggle.com/datasets/mahreen/sato2015
v2_path: datasets/_dev/tabarena-v0pt2/churn_telco_south_asia/dataset.py
source_row: 674
type_adapter_id: curation-record-v1
---

## Comments

"operator, with 13 features and 2000 records, collected between Aug 2015 to Sep 2015"

"To overcome the class imbalance problem in
churn data sets, an equal amount of churners and active
subscribers were collected from the carrier. So the data has 50% churner's information."

**Assessment (AI, 2026-10-07):** The DSN Telecoms Churn 2018 competition files (record churn_telco_south_asia_duplicate; OpenML 44229, 44230) are this file with the networks renamed (mobilink Mango, ufone Uxaa, ...): all 2,000 rows match on the nine numeric columns and all 1,400 labelled rows agree, so that record is the duplicate. Not trivial: random forest ROC AUC 0.815 against 0.729 for the raw total revenue (30 splits). The 50% churn rate is set by design; ROC AUC does not depend on it. Open: whether churn was observed after the Aug-Sep 2015 window or inside it (then the aggregates end at the churn, as iranian_churn). The paper (doi:10.1109/IntelliSys.2017.8324367) is closed access, and the data do not settle it.

Open (2026-10-12): a paper to get. IntelliSys 2017, doi 10.1109/IntelliSys.2017.8324367 (closed access; no free copy found in the 2026-10-07 run), would settle when churn was observed in this data, which decides whether the usage columns describe the time before the churn.

**Assessment (AI, 2026-10-15):** The authors' journal paper (Ahmed et al., Neural Computing and Applications 32:3237-3251, doi 10.1007/s00521-018-3678-8) does not say when churn was observed either: "The subscriber data is extracted from the time interval of two months, i.e., August and September 2015" (Sec. 3.1, p. 3241); "class labeling (for SATO dataset)" is listed as a preprocessing step without a definition (Sec. 3.2). Nor does the IntelliSys 2017 paper (Sec. III, p. 680, the source of the quotes above; "class labeling" is a preprocessing step, Sec. IV), so no source settles it; the definition keeps churn after the window, with fit `approximate`. Both papers list "Package Name" as a feature (among the top five in the journal paper, Sec. 4), which the public file lacks.

CC (2026-10-15, Lennart): ship, kept for now although the task may be problematic: neither paper says when churn was observed, and if the churners left inside August-September, the usage totals end at the outcome (the iranian_churn reason). The definition states this as a potential leak kept on purpose; revisit if the churn can be dated. The impossible negative `network_age` values and the undocumented `aug_fav_a` "0" are missing; the other anomalies stay as published.

CC (2026-10-21, Lennart): option (a) of the consistency check on one-snapshot churn sets: tagged `ForcedIIDFromTemporal`; SPLIT-8 now covers a release with one stock month or one undated snapshot.

**Assessment (AI, 2026-10-21):** tag and one note line added; a dated earlier window would test the model across shifts in usage and the network mix; not measurable on one two-month window.

**Assessment (AI, 2026-10-21):** Metric declared under MET-1..13: fallback roc_auc — The first publication (closed access, abstract elided) could not be read; no metric verified. Cohort is 50/50 by design, so accuracy (the likely reported number) would be close in spirit, but AUC is insensitive to the artificial base rate as the curation notes say.

CC (2026-10-21, Lennart): the fallback metric stays (`roc_auc`; the first publication could not be read, so no metric is known; cross-dataset item "Metrics still to settle").

**Assessment (AI, 2026-10-30):** Dtype review (branch ordinal-and-censored-levels; the column decisions with their codebook evidence are on the review board): left unordered: `aug_user_type` (low confidence); `sep_user_type` (low confidence).

CC (2026-10-31, Lennart): marks on the review board of PR #37: the user types left unordered with a note (Other is undocumented and not 4G).

**Assessment (AI, 2026-10-31):** better data: the data-scouting run of 2026-10-30/31 found better data for the same task: `orange_belgium_churn_uplift` (TBD -> Yes, priority 2); a related task: `bulgarian_telecom_business_churn` (TBD -> Yes, priority 2). Each is screened in its own record; this record's verdict stays the curator's.

CC (2026-11-13, Andrej): collection fact `Target: Later` (Review issue 1, B): whether the subscriber churns after the two months of usage, so it arrives after the features; the forced tag and the split stay.

CC (2026-11-13, Andrej): time basis `DelayedTarget` instead of `ForcedIIDFromTemporal`: the subscribers are scored after the same two months of usage, the shared prediction moment, and churn follows it (`Target: Later`); its window is taken as closed, as for mobile_churn. The random split stays.

CC (2026-11-16, Andrej): time basis `ForcedIIDFromTemporal` instead of `DelayedTarget`, which is retired:
- A shared scoring date with a target window closed for every row makes the random split valid within that date only; one date is one period, too few for three windows, so the split is forced (SPLIT-8).
- The random split stays.

CC (2026-11-17, Andrej): the declared split (random, 10x3 folds, `ForcedIIDFromTemporal`) is checked: the split decision tree, walked without the current split, reaches the split it ships (blind split review, cross-dataset item).

CC (2026-11-18, Andrej): the forced tag stays (Review issue 2, A; stationarity reasoning, SPLIT-32 as amended today): no reason to take later samples as interchangeable. Telecom churn is driven by a competitive market and the data already show a network-mix shift; the closest measured churn set is not flat.

## Review

**Outcome:** added. The record gained `Target: Later` on 2026-11-13.

**Main points:** Nothing open: issue 1 resolved on 2026-11-13 (`Target: Later` recorded).

**Issues for Andrej:**

1. **Record `Target: Later`?**

   * **Problem:**
     - The record names no `Target:` fact, which reads as a target measured with the features.
     - The label is whether the subscriber churns after the two months of usage: it arrives after the features, and the forced tag already treats the use case as forward.
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

2. **Keep `ForcedIIDFromTemporal`, or tag `AssumedStationaryRelation`?**

   * **Problem:**
     - Time: One scoring of 2,000 subscribers after August-September 2015 usage; the two months are feature columns of every row, not periods, and the authors released no other window.
     - Use: The operator scores subscribers after a usage window to target retention, i.e. on later windows than the one collected.
     - Mechanism: Usage, revenue and complaints relate to leaving through prices, competitor offers and network mix; these change month to month (the release itself shows a September move to ufone as the most-called other network).
   * **Background:** similar datasets[^asr].

     | Similar dataset or source | What was measured | Verdict | Why similar |
     |---|---|---|---|
     | mobile_churn (SPLIT-8 Cases) | train on June base, test the 1,533 July/August joiners: ROC AUC 0.661 vs 0.690 IID (gap 0.028, 95% CI 0.004-0.056, LightGBM), cohort and time mixed | shift of 0.028 ROC AUC | prepaid telecom churn scored at month end |
     | Gama et al. 2014, 'A survey on concept drift adaptation', ACM Computing Surveys 46(4) | review of drift in deployed predictors; customer profiling, marketing and telecom are named application areas with changing populations and behaviour | not flat (domain-level) | same use: scoring customers of a later period |
     | account_debt_south_africa (SPLIT-8 Cases) | held out by file block: ROC AUC 0.877 -> 0.843 / 0.786 | not flat | customer-behaviour outcome of one firm's book |

   * **For a stationary use case:**
     - Low usage and complaints preceding churn is a general behavioural pattern.
   * **Against:**
     - Competing operators' offers and prices drive churn (opponents who adapt, markets).
     - The data show a shift in network mix within the two months (September move to ufone).
     - 1,000/1,000 design-balanced sample; churn timing undocumented.
     - mobile_churn, the nearest measured telecom churn set, loses 0.028 ROC AUC forward (CI excludes 0).
   * **Earlier views:**
     - CC (2026-10-21, Lennart): tagged ForcedIIDFromTemporal for one-snapshot churn sets (SPLIT-8).
     - CC (2026-11-16, Andrej): back to ForcedIIDFromTemporal from DelayedTarget: one date is one period.
     - CC (2026-11-17, Andrej): blind split walk reaches the shipped split.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep `ForcedIIDFromTemporal` (implemented) | The folds stay; the Time basis line names the reasoning below | Claims only what is known | The split stands for later samples only as far as the use case is stationary |
     | B | `AssumedStationaryRelation` | The folds stay; you give the reason (eight words or more) | Documents why random folds stand for later samples | Competing operators' offers and prices drive churn (opponents who adapt, markets).; The data show a shift in network mix within the two months (September move to ufone). |

   * **Recommendation:** A, telecom churn is driven by a competitive market and the data already show a network-mix shift; the closest measured churn set is not flat. Confidence: high. **Decision:** A or B?

   [^asr]: **SPLIT-32** (Should; amended 2026-11-18, Andrej): "where it holds none, the review reasons whether the use case can be taken as stationary, from the domain's mechanism and from similar datasets ..., where the AI offers `AssumedStationaryRelation` with a recommendation for a person to decide." `AssumedStationaryRelation` keeps the forced split's folds and replaces only the tag; its line opens `AssumedStationaryRelation (<person>, <date>): <reason>`.

   **Andrej (2026-11-18, ok):** as implemented.

   **Resolved (2026-11-18, Andrej):** A, as implemented: the forced tag stays; the `Time basis:` line gives the reasoning (Telecom churn is driven by a competitive market and the data already show a network-mix shift; the closest measured churn set is not flat.)

## Reference

@inproceedings{ahmed2017mcs,
  title={MCS: Multiple classifier system to predict the churners in the telecom industry},
  author={Ahmed, Mehreen and Siddiqi, Imran and Afzal, Hammad and Khan, Behram},
  booktitle={2017 Intelligent Systems Conference (IntelliSys)},
  pages={678--683},
  year={2017},
  organization={IEEE}
}
