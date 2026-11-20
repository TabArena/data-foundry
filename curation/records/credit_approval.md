---
unique_name: credit_approval
name: Credit Approval
checked_by:
- Lennart
- Andrej
data_foundry_status:
- 'DF: Yes'
- BeyondArena
suggestion: Yes (Disagreement)
decision_markers:
- Outdated
- Not Representative
- Anonymized
tags:
- Tiny Data
- 'Samples: Over Time'
- 'Time: Lost'
- Database Snapshot
collections:
- New (BeyondArena)
original_source: UCI
year: '1987'
collection_period: Unknown
domain: finance
required_split:
- Random (IID)
problem_type: Binary Classification
original_data_state: Database (or multiple to-be-joined tables)
source_links:
- https://doi.org/10.24432/C5FS30
- https://doi.org/10.24432/C5259N
notebook_path: datasets/beyond_iid/new_iid/credit_approval/credit_approval.ipynb
v2_path: datasets/_dev/tabarena-v0pt2/credit_approval/dataset.py
source_row: 775
type_adapter_id: curation-record-v1
---

## Comments

The UCI source contains two datasets, this is the crx dataset in the data

Credit Approval (690 rows), From a Japanese

**Assessment (AI, 2026-10-14):** The 690 rows are `crx.data`, Quinlan's Credit Approval (UCI 27; the source is "confidential", so the lender and country are not stated), not Japanese data. The same UCI zip holds the Japanese Credit Screening data (UCI 28, `credit.lisp`, 125 examples, Chiharu Sano 1992; the second source link, 10.24432/C5259N), which we do not use. Statlog (Australian Credit Approval) (UCI 143) is the same 690 applications with recoded values and filled-in missing values: its rows are those of `crx.data` in another order (four numeric columns and the label match as a multiset).

**Assessment (AI, 2026-10-21):** Metric declared under MET-1..13: fallback roc_auc — Quinlan 1987 and the Statlog Australian study score error rate without costs or a threshold; accuracy rejected.

**Assessment (AI, 2026-10-31):** better data: the data-scouting run of 2026-10-30/31 found better data for the same task: `hmda_mortgage_application_decision` (TBD -> Yes, priority 2). Each is screened in its own record; this record's verdict stays the curator's.

CC (2026-11-17, Andrej): the declared split (random, 20x3 folds, `ForcedIIDFromTemporal`) is checked: the split decision tree, walked without the current split, reaches the split it ships (blind split review, cross-dataset item).

CC (2026-11-18, Andrej): the forced tag stays (Review issue 2, A; stationarity reasoning, SPLIT-32 as amended today): no reason to take later samples as interchangeable. A lender's approval decision follows credit policy and markets, the data is decades old and anonymized; there is no domain reason for interchangeability.

## Review

**Outcome:** added. A question on `CrossSectional` (2026-11-13) was withdrawn when the prototype was dropped.

**Main points:** Nothing open: issue 1 was withdrawn on 2026-11-13.

**Issues for Andrej:**

1. **`CrossSectional` instead of `ForcedIIDFromTemporal`?**

   * **Problem:**
     - The definition is tagged `ForcedIIDFromTemporal`, a forward use case whose time was lost[^fo-1].
     - The target is a present state measured with the features: the application's decision, read from the application itself, and the use case reads it for new units at their own present[^cs-1].
     - The tag alone changes: the split stays random.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Stay `ForcedIIDFromTemporal` (implemented) | the tag and its line stay | the decision stands | the tag claims a forecast the use case does not make |
     | B | `CrossSectional` | the tag and a `Time basis:` line naming the present state, the untested drift for later units and what a dated release would show | names the use case; no claim of a lost forward split | a new prototype on a decided tag |

   * **Recommendation:** B. **Decision:** A or B?

   **Notes for the AI:** on B, swap the tag, write the line, add a CC line; the split does not change.

   [^cs-1]: **SPLIT-32** (Should, 2026-11-13): a target measured together with the features, which the use case reads for new units at their own present, is `CrossSectional`, whether the dates survive or not; its line says whether the drift of the relation was measured or is untested. A label that only arrives later is no present state.
   [^fo-1]: **SPLIT-8** (Must): a forward use case without usable time ships in the closest regime, tagged forced from temporal, with a `Time basis:` line naming the reason.

   **Resolved (2026-11-13, Andrej):** withdrawn: `CrossSectional` was dropped the same day (it named no split the existing prototypes do not give: a present state used later is forced or a measured `StationaryRelation`, used within the covered time `Retrospective`). The tag stays.

2. **Keep `ForcedIIDFromTemporal`, or tag `AssumedStationaryRelation`?**

   * **Problem:**
     - Time: crx.data (Quinlan 1987) has no date or id and is ordered in class blocks (assembly, not time); no dated parent exists.
     - Use: A lender imitates its past approve/decline decisions on new applications; any use today is almost four decades after collection.
     - Mechanism: The label is a lender's decision (meaning not even documented), so it follows that lender's credit policy and the market at the time; policy and applicant populations change, and an old one-time study used today is a long span.
   * **Background:** similar datasets[^asr].

     | Similar dataset or source | What was measured | Verdict | Why similar |
     |---|---|---|---|
     | lending_club (this collection, matched-v2 stationary-relation test) | 36-month LendingClub loans, issue years 2013-2015 each tested forward vs contemporaneous on the same test half (LightGBM, whole half) | not flat: forward worse by 0.0043-0.0059 ROC AUC (2.4-4.2 floors, beyond 2 SD) in all three years; default rate 10.0-15.2% by year | consumer credit default from application/bureau data, outcome over months after the grant |
     | Kelly, Hand & Adams, 'The impact of changing populations on classifier performance', KDD 1999 (doi 10.1145/312129.312285); Hand, 'Classifier technology and the illusion of progress', Statistical Science 2006 (arXiv math/0606452) (literature, cited from memory: check) | scorecard performance on UK bank unsecured personal loans 1993-1998 as the applicant population drifts | not flat: population drift degrades scorecards; Hand names drift as a particular concern in credit scoring because defaults arrive long after the grant | application scoring of consumer credit |

   * **For a stationary use case:**
     - None found beyond the absence of dates (no reason under the rule).
   * **Against:**
     - The target is a lending decision: changed rules and credit policy move it directly.
     - Old one-time study (1987 or earlier) used today: a long span for a market domain.
     - Anonymized features and undocumented label leave no mechanism to argue stability from.
     - Similar measured credit data (lending_club) and credit-scoring literature show drift.
   * **Earlier views:**
     - Resolved (2026-11-13, Andrej): CrossSectional withdrawn, the forced tag stays.
     - CC (2026-11-17, Andrej): blind split review: the decision tree, walked without the current split, reaches the forced split it ships.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep `ForcedIIDFromTemporal` (implemented) | The folds stay; the Time basis line names the reasoning below | Claims only what is known | The split stands for later samples only as far as the use case is stationary |
     | B | `AssumedStationaryRelation` | The folds stay; you give the reason (eight words or more) | Documents why random folds stand for later samples | The target is a lending decision: changed rules and credit policy move it directly.; Old one-time study (1987 or earlier) used today: a long span for a market domain. |

   * **Recommendation:** A, a lender's approval decision follows credit policy and markets, the data is decades old and anonymized; there is no domain reason for interchangeability. Confidence: high. **Decision:** A or B?

   [^asr]: **SPLIT-32** (Should; amended 2026-11-18, Andrej): "where it holds none, the review reasons whether the use case can be taken as stationary, from the domain's mechanism and from similar datasets ..., where the AI offers `AssumedStationaryRelation` with a recommendation for a person to decide." `AssumedStationaryRelation` keeps the forced split's folds and replaces only the tag; its line opens `AssumedStationaryRelation (<person>, <date>): <reason>`.

   **Andrej (2026-11-18, ok):** as implemented.

   **Resolved (2026-11-18, Andrej):** A, as implemented: the forced tag stays; the `Time basis:` line gives the reasoning (A lender's approval decision follows credit policy and markets, the data is decades old and anonymized; there is no domain reason for interchangeability.)

## Reference

@article{quinlan1987simplifying,
  title={Simplifying decision trees},
  author={Quinlan, J. Ross},
  journal={International journal of man-machine studies},
  volume={27},
  number={3},
  pages={221--234},
  year={1987},
  publisher={Elsevier}
}
