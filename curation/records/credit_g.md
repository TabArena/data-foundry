---
unique_name: credit_g
name: credit-g
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
- 'Target: Varying Delay'
- Database Snapshot
original_source: UCI
year: '1994'
required_split:
- Random (IID)
problem_type: Binary Classification
source_links:
- https://www.openml.org/search?type=data&id=31
- https://doi.org/10.24432/C5NC77
notebook_path: datasets/beyond_iid/old_iid/credit_g/credit_g.ipynb
v2_path: datasets/_dev/tabarena-v0pt2/credit_g/dataset.py
type_adapter_id: curation-record-v1
---

## Comments

Clean canonical entry bootstrapped from the TabArena curation workbook ('Tabular' row). Shipped in TabArena (v0.1) / BeyondArena.

TabArena curation verdict: Tabular.

Comes with a cost matrix. TabRed says that task requires time based split, but no time feature given. However, if time-invariant features are used that might not matter. Also might be outdated as nowadays other features might be used; only time dependency could be the bank's and the world's financial state as a confounding factor

Potential issue: Outdated (Deutsche Mark)

Lennart: Temporal impact unclear and not resolvable, otherwise ok and not too old

Andrej: Fits criteria, but honestly this dataset with only 1000 samples from 1994 is not representative of a credit scoring task anymore. If no better dataset is available I would not use it

**Assessment (AI, 2026-10-21):** Metric declared under MET-1..13: source cost_matrix {"labels":["good","bad"],"matrix":[[0,1],[5,0]],"prediction":"proba"} — the Statlog cost matrix (5 for a bad customer predicted good, 1 for the reverse; UCI german.doc, Michie et al. 1994), from probabilities by least expected cost.

CC (2026-10-21, Lennart): Unsure whether the cost matrix should score probabilities or labels (TabArena tunes thresholds); the AI's choice, probabilities with the least expected cost, is applied.

**Assessment (AI, 2026-10-30):** Dtype review (branch ordinal-and-censored-levels; the column decisions with their codebook evidence are on the review board): 2 ordinal scales typed as ordered categories in the codebook's order (CLEAN-14, amended): `employment_since`, `job` (the README lists their levels); left unordered: `checking_status` (a level outside the scale is a state of its own); `savings_status` (a level outside the scale is a state of its own); `property` (a level outside the scale is a state of its own); ordinal scales shipped as numbers, left as numbers for the curator's review: `installment_rate_percent`, `residence_since`, `existing_credits_count`; labels relabelled by the corrected code table (Groemping 2019, UCI 573 South German Credit): Statlog's german.doc is wrong for checking_status, credit_history, credit_purpose, savings_status, personal_status_sex, property, housing and foreign_worker; matched on duration, amount and age, the codes correspond one to one (990 rows). UCI 573 also corrects a few values (34 rows of other_installment_plans, 10 of foreign_worker, 1 of housing), not applied: a question for the curator..

CC (2026-10-31, Lennart): marks on the review board of PR #37 (ordinal scales in the codebook's order, also when shipped as numbers; a state outside a scale missing when the column has no other missing value, else the lowest level; cycles ordered; codes shipped as numbers as categories): 3 ordinal scales shipped as numbers are ordered categories (point 3); 3 columns with a state outside the scale ordered, the state placed by the rule; the source is UCI 573 (South German Credit, the corrected Statlog data): every code labelled by its code table, 57 coded values and 10 typos in amount or age corrected; 9 ordinal scales, the account and property states missing by the state rule.

CC (2026-11-17, Andrej): the declared split (random, 10x3 folds, `ForcedIIDFromTemporal`) is checked: the split decision tree, walked without the current split, reaches the split it ships (blind split review, cross-dataset item).

CC (2026-11-18, Andrej): the forced tag stays (Review issue 1, A; stationarity reasoning, SPLIT-32 as amended today): no reason to take later samples as interchangeable. A 1973-1975 bank sample scored for later applicants spans decades of changed currency, products and rules; no domain reason holds.

## Review

**Outcome:** added. Stationarity reasoning of 2026-11-18: the definition reaches the forced step with no time to measure; decided below.

**Main points:** Keep `ForcedIIDFromTemporal`, or tag `AssumedStationaryRelation`?

**Issues for Andrej:**

1. **Keep `ForcedIIDFromTemporal`, or tag `AssumedStationaryRelation`?**

   * **Problem:**
     - Time: Consumer credits granted 1973-1975 (South German Credit, Groemping 2019); neither UCI 573's file (sorted by class) nor Statlog's keeps a grant date.
     - Use: A bank decides on later applications; any use today is about 50 years after collection.
     - Mechanism: Good/bad repayment follows the applicant's finances, the bank's grant policy and the economy; Deutsche Mark amounts, 1970s products and a stratified (oversampled bad) sample tie it to its time and selection.
   * **Background:** similar datasets[^asr].

     | Similar dataset or source | What was measured | Verdict | Why similar |
     |---|---|---|---|
     | lending_club (this collection, matched-v2 stationary-relation test) | 36-month LendingClub loans, issue years 2013-2015 each tested forward vs contemporaneous on the same test half (LightGBM, whole half) | not flat: forward worse by 0.0043-0.0059 ROC AUC (2.4-4.2 floors, beyond 2 SD) in all three years; default rate 10.0-15.2% by year | consumer credit default from application/bureau data, outcome over months after the grant |
     | Kelly, Hand & Adams, 'The impact of changing populations on classifier performance', KDD 1999 (doi 10.1145/312129.312285); Hand, 'Classifier technology and the illusion of progress', Statistical Science 2006 (arXiv math/0606452) (literature, cited from memory: check) | scorecard performance on UK bank unsecured personal loans 1993-1998 as the applicant population drifts | not flat: population drift degrades scorecards; Hand names drift as a particular concern in credit scoring because defaults arrive long after the grant | application scoring of consumer credit |

   * **For a stationary use case:**
     - Basic credit risk factors (checking account status, duration, history) keep their direction.
   * **Against:**
     - Old one-time study used today: a 50-year span in a market domain (currency, products, rules changed).
     - Bank grant policy decides who is in the data (only granted loans observed) and changes over time.
     - The original Statlog coding had errors corrected only in 2019: coding changes.
     - Credit-scoring literature and lending_club show drift over far shorter spans.
   * **Earlier views:**
     - CC (2026-11-17, Andrej): blind split review: the decision tree, walked without the current split, reaches the forced split it ships.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep `ForcedIIDFromTemporal` (implemented) | The folds stay; the Time basis line names the reasoning below | Claims only what is known | The split stands for later samples only as far as the use case is stationary |
     | B | `AssumedStationaryRelation` | The folds stay; you give the reason (eight words or more) | Documents why random folds stand for later samples | Old one-time study used today: a 50-year span in a market domain (currency, products, rules changed).; Bank grant policy decides who is in the data (only granted loans observed) and changes over time. |

   * **Recommendation:** A, a 1973-1975 bank sample scored for later applicants spans decades of changed currency, products and rules; no domain reason holds. Confidence: high. **Decision:** A or B?

   [^asr]: **SPLIT-32** (Should; amended 2026-11-18, Andrej): "where it holds none, the review reasons whether the use case can be taken as stationary, from the domain's mechanism and from similar datasets ..., where the AI offers `AssumedStationaryRelation` with a recommendation for a person to decide." `AssumedStationaryRelation` keeps the forced split's folds and replaces only the tag; its line opens `AssumedStationaryRelation (<person>, <date>): <reason>`.

   **Andrej (2026-11-18, ok):** as implemented.

   **Resolved (2026-11-18, Andrej):** A, as implemented: the forced tag stays; the `Time basis:` line gives the reasoning (A 1973-1975 bank sample scored for later applicants spans decades of changed currency, products and rules; no domain reason holds.)

## Reference

10.24432/C5NC77
