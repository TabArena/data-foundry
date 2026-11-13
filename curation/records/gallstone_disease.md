---
unique_name: gallstone_disease
name: Gallstone
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
- New (BeyondArena)
original_source: UCI
year: '2025'
domain: medical & healthcare
required_split:
- Random (IID)
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://archive.ics.uci.edu/dataset/1150/gallstone-1
- https://doi.org/10.1097/md.0000000000037258
notebook_path: datasets/beyond_iid/new_iid/gallstone_disease/gallstone_disease.ipynb
v2_path: datasets/_dev/tabarena-v0pt2/gallstone_disease/dataset.py
source_row: 768
type_adapter_id: curation-record-v1
---

## Comments

looks good

CC (2026-10-06, Lennart): Kept after the task-probe review: the `no_spread` flag does not hold. The three untuned families differ by 0.036 in skill (+0.683 to +0.719), which the probe compared, unpaired, with twice their typical standard error over 5 splits (0.054). Tuned methods spread clearly: on BeyondArena TabPFN-3.5 reaches ROC AUC 0.911 and the median method 0.883, with 8 of 29 methods tied with the best.

**Assessment (AI, 2026-10-21):** Metric declared under MET-1..13: fallback roc_auc — Esen et al. 2024 report accuracy, precision, recall, F-measure and AUC side by side, none named as the criterion (MET-5).

CC (2026-10-27, Lennart): keep it as Andrej marked it: the Selection Bias marker and fit direct (USE-8, amended on the review of PR #16); how the patients were chosen is not stated.

**Assessment (AI, 2026-10-30):** Dtype review (branch ordinal-and-censored-levels; the column decisions with their codebook evidence are on the review board): ordinal scales shipped as numbers, left as numbers for the curator's review: `Hepatic Fat Accumulation (HFA)`.

CC (2026-10-31, Lennart): marks on the review board of PR #37 (ordinal scales in the codebook's order, also when shipped as numbers; a state outside a scale missing when the column has no other missing value, else the lowest level; cycles ordered; codes shipped as numbers as categories): 1 ordinal scales shipped as numbers are ordered categories (point 3); Comorbidity's three undocumented 2 and 3 (each with one listed disease) recoded to 1, the rows kept (CLEAN-11); the fat-accumulation grade an ordered category.

**Assessment (AI, 2026-10-31):** better data: the data-scouting run of 2026-10-30/31 found better data for the same task: `nhanes_iii_gallstones` (TBD -> Yes, priority 2). Each is screened in its own record; this record's verdict stays the curator's.

CC (2026-11-01, Lennart): the decode rule (a code whose codebook says in words what each level is carries the words; a score without them is a number): 3 coded columns carry their words; the target keeps its codes.

CC (2026-11-01, Lennart): the target rule (CLEAN-25) and the cut-end rule (CLEAN-14): the target ships as No/Yes, Yes the event (0 means gallstones present (UCI)).

CC (2026-11-13, Andrej): the time basis is `ForcedIIDFromTemporal` instead of `StationaryRelation`:
- `StationaryRelation` asks for a measurement on dated data, and the file keeps no visit date (`Time: Lost`), so the stationary relation was argued, not measured.
- The random split stays; the forced tag says what it is: random patients standing in for later ones, with the drift along the file's order and what a dated release would test in the `Time basis:` line.

## Review

**Outcome:** added. The AI asks which time basis fits now that `CrossSectional` names a present state (2026-11-13).

**Main points:** `CrossSectional` instead of `ForcedIIDFromTemporal`?

**Issues for Andrej:**

1. **`CrossSectional` instead of `ForcedIIDFromTemporal`?**

   * **Problem:**
     - The definition is tagged `ForcedIIDFromTemporal`, a forward use case whose time was lost[^fo-1].
     - The target is a present state measured with the features: the diagnosis at the visit, read from the same visit's laboratory values and body composition, and the use case reads it for new units at their own present[^cs-1].
     - The tag alone changes: the split stays random.
   * **Background:** you made the tag `ForcedIIDFromTemporal` on 2026-11-13, before `CrossSectional` existed, because `StationaryRelation` cannot be measured without dates. The use case is screening at the visit where the diagnosis is made, a present state, which `CrossSectional` now names without claiming a measurement.
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

@article{esen2024early,
  title={Early prediction of gallstone disease with a machine learning-based method from bioimpedance and laboratory data},
  author={Esen, {\.I}rfan and Arslan, Hilal and Esen, Selin Akt{\"u}rk and G{\"u}l{\c{s}}en, Mervenur and K{\"u}ltekin, Nimet and {\"O}zdemir, O{\u{g}}uzhan},
  journal={Medicine},
  volume={103},
  number={8},
  pages={e37258},
  year={2024},
  publisher={LWW}
}
