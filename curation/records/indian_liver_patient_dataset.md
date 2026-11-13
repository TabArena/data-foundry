---
unique_name: indian_liver_patient_dataset
name: ilpd
checked_by:
- Lennart
- Andrej
data_foundry_status:
- 'DF: Yes'
- BeyondArena
suggestion: 'Yes'
decision_markers:
- Selection Bias
tags:
- Tiny Data
- 'Samples: Over Time'
- 'Time: Lost'
collections:
- TabArena Reject
- TabSTAR
original_source: UCI
year: '2012'
domain: medical & healthcare
required_split:
- Random (IID)
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://doi.org/10.24432/C5D02C
notebook_path: datasets/beyond_iid/new_iid/indian_liver_patient_dataset/indian_liver_patient_dataset.ipynb
v2_path: datasets/_dev/tabarena-v0pt2/indian_liver_patient_dataset/dataset.py
source_row: 747
type_adapter_id: curation-record-v1
---

## Comments

CC: "There was a custom train/test split. Task might be rather a toy task and not of practical use. Unclear current SOTA for the domain but in itself fine and not too old"

Make sure to add indicator variable for clipping of 90

CC (2026-10-06, Lennart): Kept after the task-probe review: the `no_spread` flag (untuned skills +0.47 to +0.50) does not hold for tuned methods. On BeyondArena LimiX-2 reaches ROC AUC 0.771 and the median method 0.750, with 4 of 29 methods tied with the best.

**Assessment (AI, 2026-10-21):** Metric declared under MET-1..13: fallback roc_auc — The UCI page defines no task metric and the cited paper (Ramana et al. 2012) is a statistical comparison of the USA and India patient groups, not a benchmark with a declared score; later uses report accuracy only.

**Assessment (AI, 2026-10-31):** better data: the data-scouting run of 2026-10-30/31 found better data for the same task: `nhanes_liver_elastography_fibrosis` (TBD -> Yes, priority 2). Each is screened in its own record; this record's verdict stays the curator's.

CC (2026-11-01, Lennart): the target rule (CLEAN-25) and the cut-end rule (CLEAN-14): the target ships as No/Yes, Yes the event (1 means a liver patient (UCI)).

## Review

**Outcome:** added. The AI asks which time basis fits now that `CrossSectional` names a present state (2026-11-13).

**Main points:** `CrossSectional` instead of `ForcedIIDFromTemporal`?

**Issues for Andrej:**

1. **`CrossSectional` instead of `ForcedIIDFromTemporal`?**

   * **Problem:**
     - The definition is tagged `ForcedIIDFromTemporal`, a forward use case whose time was lost[^fo-1].
     - The target is a present state measured with the features: whether the record is of a liver patient, read from the same laboratory panel, and the use case reads it for new units at their own present[^cs-1].
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

The original dataset was first proposed by Ramana et al. (2012) as a critical comparison of patients across USA and India:
Ramana, Bendi & Surendra, M & Babu, Prasad & Bala Venkateswarlu, Nagasuri. (2012). A Critical Comparative Study of Liver Patients from USA and INDIA: An Exploratory Analysis. International Journal of Computer Science. 9.
