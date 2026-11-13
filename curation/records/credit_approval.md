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
collections:
- New (BeyondArena)
original_source: UCI
year: '1987'
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

## Review

**Outcome:** added. The AI asks which time basis fits now that `CrossSectional` names a present state (2026-11-13).

**Main points:** `CrossSectional` instead of `ForcedIIDFromTemporal`?

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
