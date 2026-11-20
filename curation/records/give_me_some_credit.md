---
unique_name: give_me_some_credit
name: Give Me Some Credit / credit
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
original_source: Kaggle
year: '2011'
required_split:
- Random (IID)
source_links:
- https://www.openml.org/search?type=data&id=44089
- https://www.kaggle.com/competitions/GiveMeSomeCredit/overview
notebook_path: datasets/beyond_iid/old_iid/give_me_some_credit/give_me_some_credit.ipynb
v2_path: datasets/_dev/tabarena-v0pt2/give_me_some_credit/dataset.py
type_adapter_id: curation-record-v1
---

## Comments

Clean canonical entry bootstrapped from the TabArena curation workbook ('Tabular' row). Shipped in TabArena (v0.1) / BeyondArena.

TabArena curation verdict: Tabular.

Predict credit delay.

Potential issue: -

Lennart: No objection

Andrej: Time-invariant features, may not be representative anymore, but still valid

**Assessment (AI, 2026-10-21):** Metric declared under MET-1..13: source roc_auc — Kaggle's evaluation: AUC.

CC (2026-11-17, Andrej): the declared split (random, 3x3 folds, `ForcedIIDFromTemporal`) is checked: the split decision tree, walked without the current split, reaches the split it ships (blind split review, cross-dataset item).

CC (2026-11-18, Andrej): the forced tag stays (Review issue 1, A; stationarity reasoning, SPLIT-32 as amended today): no reason to take later samples as interchangeable. A two-year delinquency outcome in an unknown, likely crisis-era period moves with the credit climate; the rule itself cites this dataset as forced for lack of known collection facts.

## Review

**Outcome:** added. Stationarity reasoning of 2026-11-18: the definition reaches the forced step with no time to measure; decided below.

**Main points:** Keep `ForcedIIDFromTemporal`, or tag `AssumedStationaryRelation`?

**Issues for Andrej:**

1. **Keep `ForcedIIDFromTemporal`, or tag `AssumedStationaryRelation`?**

   * **Problem:**
     - Time: Kaggle 2011 release keeps no date; row id is no time order (ROC AUC 0.502); scoring dates unstated, before about September 2009.
     - Use: A bank scores later applicants and follows them for two years; use today is 15+ years after the scoring dates.
     - Mechanism: 90-day delinquency within two years depends on the borrower's credit file and the credit climate; two-year windows ending by 2009 likely span the 2007-2009 financial crisis, when delinquency rose broadly in the US.
   * **Background:** similar datasets[^asr].

     | Similar dataset or source | What was measured | Verdict | Why similar |
     |---|---|---|---|
     | lending_club (this collection, matched-v2 stationary-relation test) | 36-month LendingClub loans, issue years 2013-2015 each tested forward vs contemporaneous on the same test half (LightGBM, whole half) | not flat: forward worse by 0.0043-0.0059 ROC AUC (2.4-4.2 floors, beyond 2 SD) in all three years; default rate 10.0-15.2% by year | consumer credit default from application/bureau data, outcome over months after the grant |
     | Kelly, Hand & Adams, 'The impact of changing populations on classifier performance', KDD 1999 (doi 10.1145/312129.312285); Hand, 'Classifier technology and the illusion of progress', Statistical Science 2006 (arXiv math/0606452) (literature, cited from memory: check) | scorecard performance on UK bank unsecured personal loans 1993-1998 as the applicant population drifts | not flat: population drift degrades scorecards; Hand names drift as a particular concern in credit scoring because defaults arrive long after the grant | application scoring of consumer credit |

   * **For a stationary use case:**
     - Credit-file variables (utilisation, past delinquencies, debt ratio) have a stable direction of effect across lenders.
   * **Against:**
     - The outcome windows likely overlap the 2007-2009 crisis: credit climate, prices and markets.
     - Unknown lender, place and period: no fact supports stationarity (the forced tag claims only what is known, splits.md cites this dataset).
     - Similar measured credit data (lending_club) is not flat; credit-scoring literature documents population drift.
   * **Earlier views:**
     - splits.md SPLIT-32 names this dataset as the example of a forced tag that 'claims only what is known (no scoring date stated)'.
     - CC (2026-11-17, Andrej): blind split review: the decision tree, walked without the current split, reaches the forced split it ships.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep `ForcedIIDFromTemporal` (implemented) | The folds stay; the Time basis line names the reasoning below | Claims only what is known | The split stands for later samples only as far as the use case is stationary |
     | B | `AssumedStationaryRelation` | The folds stay; you give the reason (eight words or more) | Documents why random folds stand for later samples | The outcome windows likely overlap the 2007-2009 crisis: credit climate, prices and markets.; Unknown lender, place and period: no fact supports stationarity (the forced tag claims only what is known, splits.md cites this dataset). |

   * **Recommendation:** A, a two-year delinquency outcome in an unknown, likely crisis-era period moves with the credit climate; the rule itself cites this dataset as forced for lack of known collection facts. Confidence: high. **Decision:** A or B?

   [^asr]: **SPLIT-32** (Should; amended 2026-11-18, Andrej): "where it holds none, the review reasons whether the use case can be taken as stationary, from the domain's mechanism and from similar datasets ..., where the AI offers `AssumedStationaryRelation` with a recommendation for a person to decide." `AssumedStationaryRelation` keeps the forced split's folds and replaces only the tag; its line opens `AssumedStationaryRelation (<person>, <date>): <reason>`.

   **Andrej (2026-11-18, ok):** as implemented.

   **Resolved (2026-11-18, Andrej):** A, as implemented: the forced tag stays; the `Time basis:` line gives the reasoning (A two-year delinquency outcome in an unknown, likely crisis-era period moves with the credit climate; the rule itself cites this dataset as forced for lack of known collection facts.)

## Reference

https://www.kaggle.com/competitions/GiveMeSomeCredit/overview
