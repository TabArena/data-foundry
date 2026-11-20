---
unique_name: polish_companies_bankruptcy
name: Polish Companies Bankruptcy
checked_by:
- Lennart
- Andrej
data_foundry_status:
- 'DF: Yes'
- TabArena (v0.1)
- BeyondArena
suggestion: 'Yes'
decision_markers:
- Selection Bias
tags:
- 'Samples: Over Time'
- 'Time: Lost'
- 'Target: Later'
- Database Snapshot
original_source: UCI
year: '2016'
required_split:
- Random (IID)
source_links:
- https://doi.org/10.24432/C5F600
notebook_path: datasets/beyond_iid/old_iid/polish_companies_bankruptcy/polish_companies_bankruptcy.ipynb
v2_path: datasets/_dev/tabarena-v0pt2/polish_companies_bankruptcy/dataset.py
type_adapter_id: curation-record-v1
---

## Comments

Clean canonical entry bootstrapped from the TabArena curation workbook ('Tabular' row). Shipped in TabArena (v0.1) / BeyondArena.

TabArena curation verdict: Tabular.

Data from companies from 2000-2012, predict for them from 2007 to 2013, likely temporal but could be made time invariant (as one has a dataset per year). features were already engineered - mostly through arithmetic interactions.

Potential issue: Temporal

Lennart: Could be used without temporal connection

Andrej: task can be conceptualized s.t. the features are time-invariant. Only need to think about whether it is feasible to combine the year datasets or to choose one. If the latter I would use the year with the most observations. Also might reverse the feature engineering.

**Assessment (AI, 2026-10-21):** Metric declared under MET-1..13: source roc_auc — AUC, as reported by Zieba, Tomczak & Tomczak (2016), Expert Systems with Applications 58, 93-101.

**Assessment (AI, 2026-10-31):** better data: the data-scouting run of 2026-10-30/31 found better data for the same task: `american_companies_bankruptcy` (TBD -> Yes, priority 2), `v4finbench_corporate_distress` (TBD -> Yes, priority 2). Each is screened in its own record; this record's verdict stays the curator's.

CC (2026-11-17, Andrej): the declared split (random, 3x3 folds, `ForcedIIDFromTemporal`) is checked: the split decision tree, walked without the current split, reaches the split it ships (blind split review, cross-dataset item).

CC (2026-11-18, Andrej): the forced tag stays (Review issue 1, A; stationarity reasoning, SPLIT-32 as amended today): no reason to take later samples as interchangeable. The class/period confounding is explicit in the source, and bankruptcy-ratio relations are documented as non-stationary across economic periods.

## Review

**Outcome:** added. Stationarity reasoning of 2026-11-18: the definition reaches the forced step with no time to measure; decided below.

**Main points:** Keep `ForcedIIDFromTemporal`, or tag `AssumedStationaryRelation`?

**Issues for Andrej:**

1. **Keep `ForcedIIDFromTemporal`, or tag `AssumedStationaryRelation`?**

   * **Problem:**
     - Time: The 5year.arff file has no dates; the source's 'years' are forecasting horizons, not calendar years; bankrupt firms are from 2000-2012, operating ones from 2007-2013, so no period can be rebuilt.
     - Use: A lender or investor reads a new annual statement and assesses bankruptcy within a year, after the collected period.
     - Mechanism: Ratio-based failure prediction depends on the business cycle and accounting/insolvency rules; here the two classes come from different periods, so part of the signal may be the period itself.
   * **Background:** similar datasets[^asr].

     | Similar dataset or source | What was measured | Verdict | Why similar |
     |---|---|---|---|
     | Mensah, 'An examination of the stationarity of multivariate bankruptcy prediction models', Journal of Accounting Research 22(1):380-395, 1984 (literature, cited from memory: check) | accuracy and structure of ratio-based bankruptcy models across economic periods | not flat: the ratio-failure relation shifts with the economic environment; models need re-estimation | financial-ratio bankruptcy prediction |
     | taiwanese_bankruptcy_prediction (this collection) | nothing over time (time lost) | unmeasured | ratio-based bankruptcy |

   * **For a stationary use case:**
     - Financial ratios have an accounting-identity link to solvency that does not depend on the date.
   * **Against:**
     - Classes drawn from different periods (2000-2012 vs 2007-2013): structure tied to time, the signal may be the period.
     - The span includes the 2008-2009 crisis; the ratio-failure relation shifts with the economy (Mensah 1984).
     - Insolvency law and accounting rules change (a change of rules).
   * **Earlier views:**
     - CC (2026-11-17, Andrej): blind split review: the decision tree, walked without the current split, reaches the forced split it ships.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep `ForcedIIDFromTemporal` (implemented) | The folds stay; the Time basis line names the reasoning below | Claims only what is known | The split stands for later samples only as far as the use case is stationary |
     | B | `AssumedStationaryRelation` | The folds stay; you give the reason (eight words or more) | Documents why random folds stand for later samples | Classes drawn from different periods (2000-2012 vs 2007-2013): structure tied to time, the signal may be the period.; The span includes the 2008-2009 crisis; the ratio-failure relation shifts with the economy (Mensah 1984). |

   * **Recommendation:** A, the class/period confounding is explicit in the source, and bankruptcy-ratio relations are documented as non-stationary across economic periods. Confidence: high. **Decision:** A or B?

   [^asr]: **SPLIT-32** (Should; amended 2026-11-18, Andrej): "where it holds none, the review reasons whether the use case can be taken as stationary, from the domain's mechanism and from similar datasets ..., where the AI offers `AssumedStationaryRelation` with a recommendation for a person to decide." `AssumedStationaryRelation` keeps the forced split's folds and replaces only the tag; its line opens `AssumedStationaryRelation (<person>, <date>): <reason>`.

   **Andrej (2026-11-18, ok):** as implemented.

   **Resolved (2026-11-18, Andrej):** A, as implemented: the forced tag stays; the `Time basis:` line gives the reasoning (The class/period confounding is explicit in the source, and bankruptcy-ratio relations are documented as non-stationary across economic periods.)

## Reference

Ensemble boosted trees with synthetic features generation in application to bankruptcy prediction
By Maciej Ziȩba, S. Tomczak, Jakub M. Tomczak. 2016

Published in Expert systems with applications
