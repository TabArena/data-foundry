---
unique_name: ljubljana_primary_tumor
name: Ljubljana Primary Tumor
checked_by:
- Lennart
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
year: '1988'
domain: medical & healthcare
required_split:
- Random (IID)
problem_type: Multiclass Classification
original_data_state: One Table
source_links:
- https://doi.org/10.24432/C5WK5Q
notebook_path: datasets/beyond_iid/new_iid/ljubljana_primary_tumor/ljubljana_primary_tumor.ipynb
v2_path: datasets/_dev/tabarena-v0pt2/ljubljana_primary_tumor/dataset.py
source_row: 770
type_adapter_id: curation-record-v1
---

## Comments

Need to resolve ordinal encoding, otherwise looks good!

Has a lot of classes, need to see there are enough labels per class or if I need to group some cases / remove some samples

CC (2026-10-12, Lennart): Kept in TabArena v0.2 after the task-probe review (flag `few_minority`, multiclass). Prostate has 10 rows (3-4 per test fold), colon and thyroid 14 each (4-5). Together they are 13% of the test rows and 22% of a random forest's log loss (1.43 against 2.20 for the class shares). The definition already drops the classes with fewer than 10 rows. Too Small is for a task whose scored units are a handful; one rare class of the source's own labels that does not decide the score is part of the task.

**Assessment (AI, 2026-10-21):** Metric declared under MET-1..13: fallback log_loss — The 1986-1987 papers report accuracy only; we drop the classes with fewer than 10 rows (MET-2). Original rejected: accuracy. log_loss is the multiclass fallback.

**Assessment (AI, 2026-10-27):** evidence for the Selection Bias marker of PR #16, checked on primary-tumor.data: all 20 head and neck patients have neck nodes and 21 of the 24 breast patients have armpit nodes (8% and 4% of the other patients). The rows are patients whose primary was found, with the spread typical of it, not the patients with metastases of unknown origin the use case is about. The definition's fit_reason does not name this yet.

CC (2026-10-27, Lennart): fit approximate (was direct): patients with metastases of unknown origin do not show the selection of these rows, so it is a known gap (USE-8, amended on the review of PR #16); the Selection Bias marker stays.

**Assessment (AI, 2026-10-30):** Dtype review (branch ordinal-and-censored-levels; the column decisions with their codebook evidence are on the review board): 2 ordinal scales typed as ordered categories in the codebook's order (CLEAN-14, amended): `age`, `degree-of-diffe` (the README lists their levels).

**Assessment (AI, 2026-10-31):** better data: the data-scouting run of 2026-10-30/31 found better data for the same task: `seer_primary_site_from_metastases` (TBD -> Yes, priority 3). Each is screened in its own record; this record's verdict stays the curator's.

## Review

**Outcome:** added. The AI asks which time basis fits now that `CrossSectional` names a present state (2026-11-13).

**Main points:** `CrossSectional` instead of `ForcedIIDFromTemporal`?

**Issues for Andrej:**

6. **`CrossSectional` instead of `ForcedIIDFromTemporal`?**

   * **Problem:**
     - The definition is tagged `ForcedIIDFromTemporal`, a forward use case whose time was lost[^fo-6].
     - The target is a present state measured with the features: the site of the primary tumour, read from the findings at diagnosis, and the use case reads it for new units at their own present[^cs-6].
     - The tag alone changes: the split stays random.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Stay `ForcedIIDFromTemporal` (implemented) | the tag and its line stay | the decision stands | the tag claims a forecast the use case does not make |
     | B | `CrossSectional` | the tag and a `Time basis:` line naming the present state, the untested drift for later units and what a dated release would show | names the use case; no claim of a lost forward split | a new prototype on a decided tag |

   * **Recommendation:** B. **Decision:** A or B?

   **Notes for the AI:** on B, swap the tag, write the line, add a CC line; the split does not change.

   [^cs-6]: **SPLIT-32** (Should, 2026-11-13): a target measured together with the features, which the use case reads for new units at their own present, is `CrossSectional`, whether the dates survive or not; its line says whether the drift of the relation was measured or is untested. A label that only arrives later is no present state.
   [^fo-6]: **SPLIT-8** (Must): a forward use case without usable time ships in the closest regime, tagged forced from temporal, with a `Time basis:` line naming the reason.

## Reference

UCI
