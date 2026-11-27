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
- 'Target: Fixed Delay'
- Database Snapshot
collections:
- New
original_source: Zindi
year: '2020'
collection_period: Unknown
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

CC (2026-11-13, Andrej): time basis `DelayedTarget` instead of `ForcedIIDFromTemporal` (Review issue 1, B):
- One observation window scored at its end, churn in the 90 days after it: one shared moment and a closed window, which the sharpened one-moment rule names a `DelayedTarget`.
- The random split stays.

CC (2026-11-16, Andrej): time basis `ForcedIIDFromTemporal` instead of `DelayedTarget`, which was dropped before it shipped:
- A shared scoring date with a target window closed for every row makes the random split valid within that date only; one date is one period, too few for three windows, so the split is forced (SPLIT-8).
- The random split stays.

CC (2026-11-17, Andrej): the declared split (random, 1x3 folds, `ForcedIIDFromTemporal`) is checked: the split decision tree, walked without the current split, reaches the split it ships (blind split walk, cross-dataset item).

CC (2026-11-18, Andrej): the forced tag stays (Review issue 2, A; stationarity reasoning, SPLIT-32 as amended today): no reason to take later samples as interchangeable. The dormancy signal is partly mechanical, but packages, prices and competition shape churn and the nearest measured churn set shifts; mixed at best.

CC (2026-11-27, Andrej): the declared metric (ROC AUC of the churn probability against CHURN, the competition's metric) is checked and stays as declared.

CC (2026-11-27, Andrej): ship as defined (review of 2026-11-27).

## Review

**Outcome:** added as `expresso_churn_prediction_1m`. Re-audited on 2026-11-26 against the shipped frame: no leak
beyond the region column already dropped (its missing flag rises from 0.665 to 0.936 with activity, so it is filled
after the outcome), and the split tree's leaf matches what ships. No issue is open (issue 3 decided 2026-11-27, A). Two things need no decision:
the committed README still reports the old 1,500,000-row sample against the 2,154,048 rows that ship, so it is
regenerated at the next build; and the source's own terms forbid the Kaggle upload our download instruction names,
which is a note on the record rather than a curation issue and is raised across datasets, since another Zindi record
is fetched the same way. The time basis is `ForcedIIDFromTemporal`: `DelayedTarget` (2026-11-13) was retired on 2026-11-16.

**Main points:** The time basis is `ForcedIIDFromTemporal` (Andrej, 2026-11-16); issue 1 was resolved on 2026-11-13 as
`DelayedTarget`.

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

   **Andrej (2026-11-13, change):** Option B: DelayedTarget.

   **Resolved (2026-11-13, Andrej):** B. The tag is `DelayedTarget`, with its `Time basis:` line in the definition; the split does not change.

2. **Keep `ForcedIIDFromTemporal`, or tag `AssumedStationaryRelation`?**

   * **Problem:**
     - Time: One undated Zindi snapshot of one ~3-month window; user_id is a SHA-1 of the row number and the extract order is a customer sort (thirds 0.9026 vs random 0.9028), not time.
     - Use: Expresso scores customers at the end of each observation window for 90-day churn, so the model is used on later windows.
     - Mechanism: Window activity (top-ups, revenue, active days) predicts 90 days of inactivity; 80.9% of churners already had no revenue, so much of the signal is dormancy, but tariffs, packages and competition (Orange, Free in Senegal) move the rest.
   * **Background:** similar datasets[^asr].

     | Similar dataset or source | What was measured | Verdict | Why similar |
     |---|---|---|---|
     | mobile_churn (SPLIT-8 Cases) | train on June base, test the 1,533 July/August joiners: ROC AUC 0.661 vs 0.690 IID (gap 0.028, 95% CI 0.004-0.056, LightGBM), cohort and time mixed | shift of 0.028 ROC AUC | prepaid telecom churn scored at month end |
     | Gama et al. 2014, 'A survey on concept drift adaptation', ACM Computing Surveys 46(4) | review of drift in deployed predictors; customer profiling, marketing and telecom are named application areas with changing populations and behaviour | not flat (domain-level) | same use: scoring customers of a later period |

   * **For a stationary use case:**
     - Most churners are already dormant SIMs in the window; 'dormant stays dormant' is a mechanical relation unlikely to change quickly.
     - Use is right after a window, and the release is one window of a large base (2.15M).
   * **Against:**
     - Prepaid telecom in a competitive market: packages and prices change (markets, opponents).
     - The 90-day start is inferred, not published.
     - The most-used package is a feature whose categories are the operator's offers, which change by window.
     - mobile_churn forward gap 0.028 ROC AUC (CI excludes 0).
   * **Earlier views:**
     - Assessment (AI, 2026-10-20): ForcedIIDFromTemporal applied, cost not measurable.
     - CC (2026-11-16, Andrej): ForcedIIDFromTemporal in place of DelayedTarget (one window is one period).
     - CC (2026-11-17, Andrej): blind split walk reaches the shipped split.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep `ForcedIIDFromTemporal` (implemented) | The folds stay; the Time basis line names the reasoning below | Claims only what is known | The split stands for later samples only as far as the use case is stationary |
     | B | `AssumedStationaryRelation` | The folds stay; you give the reason (eight words or more) | Documents why random folds stand for later samples | Prepaid telecom in a competitive market: packages and prices change (markets, opponents).; The 90-day start is inferred, not published. |

   * **Recommendation:** A, the dormancy signal is partly mechanical, but packages, prices and competition shape churn and the nearest measured churn set shifts; mixed at best. Confidence: medium. **Decision:** A or B?

   [^asr]: **SPLIT-32** (Should; amended 2026-11-18, Andrej): "where it holds none, the review reasons whether the use case can be taken as stationary, from the domain's mechanism and from similar datasets ..., where the AI offers `AssumedStationaryRelation` with a recommendation for a person to decide." `AssumedStationaryRelation` keeps the forced split's folds and replaces only the tag; its line opens `AssumedStationaryRelation (<person>, <date>): <reason>`.

   **Andrej (2026-11-18, ok):** as implemented.

   **Resolved (2026-11-18, Andrej):** A, as implemented: the forced tag stays; the `Time basis:` line gives the reasoning (The dormancy signal is partly mechanical, but packages, prices and competition shape churn and the nearest measured churn set shifts; mixed at best.)

3. **The codebook several claims quote cannot be opened today. Re-read it, or mark the claims as not re-read?**

   * **Problem:**
     - The variable definitions file several claims rest on is not in the Kaggle copy we fetch and is listed on the Zindi page behind a login, so nobody can re-read it from here.
     - Six claims depend on it: the three-month observation window, reading the activity count's ceiling of 62 as the last 62 days, the two quoted definitions, the meaning of one flag, and the country, where the text says Senegal but the record says Senegal and Mauritania.
     - An open question on the challenge's own forum asks exactly whether the activity count means a 62-day window, and it is unresolved there.
   * **Effect on the task:** None on the data. The definition states as sourced fact things that currently rest on a file somebody read once, and the one timing question that remains open turns on it: whether the activity count reaches into the 90 days the label covers.
   * **Experiments:** what the data settles without the codebook.

     | Claim | Measured |
     |---|---|
     | ARPU segment is revenue divided by three | holds, rounded, in all 1,428,000 non-missing rows |
     | churn rate | 18.75% |
     | churners with no revenue, against stayers | 80.9% against 22.8% |
     | rows repeating another row | 678,270, of which 75.3% carry no activity value |
     | smallest activity count | 1, so no churner has zero active days; 612 churners sit at 62 |

     The minimum of 1 argues against the activity count overlapping the label period, since an overlap with a no-transaction label would produce zeros; but that holds only if "active" means a transaction, which only the codebook says.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Leave the claims as written (implemented) | nothing changes | no work | six statements rest on a file nobody can reopen |
     | B | Mark the codebook-based statements as not re-read | each says it rests on the variable definitions, not re-read on 2026-11-26 | cheap and honest | clutters the notes |
     | C | Someone with a Zindi login re-reads the codebook and pastes the eight definitions into the record | closes the gap and settles the timing question | real verification | needs a person with a login |
     | D | Rewrite the text to what the data shows alone | no dependence on the codebook | robust | loses the operator's own meaning of each column |

   * **Recommendation:** C, with B in the meantime, since C is the only option that settles whether the activity count reaches into the label period. **Decision:** A, B, C or D?

   **Andrej (2026-11-27, ok):** As implemented (A).

   **Resolved (2026-11-27, Andrej):** A, as implemented: the claims that rest on the codebook stay as written; `dataset.py` is unchanged.

## Reference

Zindi
