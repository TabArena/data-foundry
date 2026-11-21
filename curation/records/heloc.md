---
unique_name: heloc
name: heloc
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
- 'Time: Lost'
- 'Target: Later'
- Database Snapshot
original_source: Other
year: '2018'
collection_period: Unknown
required_split:
- Random (IID)
problem_type: Binary Classification
source_links:
- https://www.kaggle.com/datasets/averkiyoliabev/home-equity-line-of-creditheloc
notebook_path: datasets/beyond_iid/old_iid/heloc/heloc.ipynb
v2_path: datasets/_dev/tabarena-v0pt2/heloc/dataset.py
type_adapter_id: curation-record-v1
---

## Comments

Clean canonical entry bootstrapped from the TabArena curation workbook ('Tabular' row). Shipped in TabArena (v0.1) / BeyondArena.

TabArena curation verdict: Tabular.

Default prediction

Potential issue: preprocessing

Lennart: Likely include a version of the original data; likely time invariant

Andrej: Use the most extensive data version

**Assessment (AI, 2026-10-19):** open since the leak audit of 2026-10-01 (no leak): 588 rows are -9 in every feature, the source's code for no bureau record; the open `dataset_missing_value_sentinel` warning comes from them. To decide in the next pass: keep them as applicants without a credit file (the real population) or drop them as empty records, and say which in the notes.

**Assessment (AI, 2026-10-21):** Metric declared under MET-1..13: fallback roc_auc — The challenge defined no predictive scoring rule: judging criteria were not announced in advance and mixed an empirical evaluation with qualitative judging of explanations; only accuracy figures (~72-74%) were reported for entries.

**Assessment (AI, 2026-10-30):** Dtype review (branch ordinal-and-censored-levels; the column decisions with their codebook evidence are on the review board): ordinal scales shipped as numbers, left as numbers for the curator's review: `MaxDelq2PublicRecLast12M`, `MaxDelqEver`.

CC (2026-10-31, Lennart): marks on the review board of PR #37 (ordinal scales in the codebook's order, also when shipped as numbers; a state outside a scale missing when the column has no other missing value, else the lowest level; cycles ordered; codes shipped as numbers as categories): 2 ordinal scales shipped as numbers are ordered categories (point 3); the two delinquency scales ordered (FICO data dictionary), their unknown, all-other and no-record codes missing.

CC (2026-11-01, Lennart): the decode rule (a code whose codebook says in words what each level is carries the words; a score without them is a number): 2 coded columns carry their words.

CC (2026-11-17, Andrej): the declared split (random, 3x3 folds, `ForcedIIDFromTemporal`) is checked: the split decision tree, walked without the current split, reaches the split it ships (blind split walk, cross-dataset item).

CC (2026-11-18, Andrej): the forced tag stays (Review issue 1, A; stationarity reasoning, SPLIT-32 as amended today): no reason to take later samples as interchangeable. HELOC default is tied to house prices and rates, the period is unknown, and the sample is constructed; the file-order check is not a time measurement and 'no drift seen' is no reason.

## Review

**Outcome:** added. Stationarity reasoning of 2026-11-18: the forced tag stays (issue 1, A, Andrej).

**Main points:** Nothing open: `ForcedIIDFromTemporal` stays, not `AssumedStationaryRelation` (issue 1 resolved on 2026-11-18).

**Issues for Andrej:**

1. **Keep `ForcedIIDFromTemporal`, or tag `AssumedStationaryRelation`?**

   * **Problem:**
     - Time: FICO's 2018 challenge release has no date; the order is the assembly of a balanced sample (first 80% -> last 20%: 0.819 vs 0.794-0.815 random), not time.
     - Use: A lender scores later HELOC applications and follows them for 24 months; period and lender unstated, use years later.
     - Mechanism: Serious delinquency on a home-equity line depends on the credit report and on house prices and rates (equity is the collateral); those markets move, and the balanced sampling by FICO is itself an unrecorded selection.
   * **Background:** similar datasets[^asr].

     | Similar dataset or source | What was measured | Verdict | Why similar |
     |---|---|---|---|
     | lending_club (this collection, matched-v2 stationary-relation test) | 36-month LendingClub loans, issue years 2013-2015 each tested forward vs contemporaneous on the same test half (LightGBM, whole half) | not flat: forward worse by 0.0043-0.0059 ROC AUC (2.4-4.2 floors, beyond 2 SD) in all three years; default rate 10.0-15.2% by year | consumer credit default from application/bureau data, outcome over months after the grant |
     | Kelly, Hand & Adams, 'The impact of changing populations on classifier performance', KDD 1999 (doi 10.1145/312129.312285); Hand, 'Classifier technology and the illusion of progress', Statistical Science 2006 (arXiv math/0606452) (literature, cited from memory: check) | scorecard performance on UK bank unsecured personal loans 1993-1998 as the applicant population drifts | not flat: population drift degrades scorecards; Hand names drift as a particular concern in credit scoring because defaults arrive long after the grant | application scoring of consumer credit |

   * **For a stationary use case:**
     - Bureau-report variables have a stable direction of effect; the file-order holdout is not worse than random (0.819 vs 0.794-0.815).
   * **Against:**
     - Home-equity credit depends on house prices and interest rates: prices and markets.
     - Unknown period and lender: no use within the collected period can be argued.
     - The release is a constructed (balanced) sample, an intake the source does not describe.
     - Similar measured credit data (lending_club) is not flat.
   * **Earlier views:**
     - splits.md SPLIT-32 Cases: heloc named as ForcedIIDFromTemporal example.
     - CC (2026-11-17, Andrej): blind split walk: the decision tree, walked without the current split, reaches the forced split it ships.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep `ForcedIIDFromTemporal` (implemented) | The folds stay; the Time basis line names the reasoning below | Claims only what is known | The split stands for later samples only as far as the use case is stationary |
     | B | `AssumedStationaryRelation` | The folds stay; you give the reason (eight words or more) | Documents why random folds stand for later samples | Home-equity credit depends on house prices and interest rates: prices and markets.; Unknown period and lender: no use within the collected period can be argued. |

   * **Recommendation:** A, hELOC default is tied to house prices and rates, the period is unknown, and the sample is constructed; the file-order check is not a time measurement and 'no drift seen' is no reason. Confidence: high. **Decision:** A or B?

   [^asr]: **SPLIT-32** (Should; amended 2026-11-18, Andrej): "where it holds none, the review reasons whether the use case can be taken as stationary, from the domain's mechanism and from similar datasets ..., where the AI offers `AssumedStationaryRelation` with a recommendation for a person to decide." `AssumedStationaryRelation` keeps the forced split's folds and replaces only the tag; its line opens `AssumedStationaryRelation (<person>, <date>): <reason>`.

   **Andrej (2026-11-18, ok):** as implemented.

   **Resolved (2026-11-18, Andrej):** A, as implemented: the forced tag stays; the `Time basis:` line gives the reasoning (HELOC default is tied to house prices and rates, the period is unknown, and the sample is constructed; the file-order check is not a time measurement and 'no drift seen' is no reason.)

## Reference

https://www.kaggle.com/datasets/averkiyoliabev/home-equity-line-of-creditheloc
