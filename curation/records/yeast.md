---
unique_name: yeast
name: yeast
checked_by:
- Lennart
- Andrej
suggestion: 'No'
decision_markers:
- Data Quality Issue
collections:
- TabArena Reject
- TabSTAR
source_links:
- https://www.openml.org/search?type=data&id=181
- https://doi.org/10.24432/C5KG68
source_row: 347
type_adapter_id: curation-record-v1
---

## Comments

CC: "Data already preprocessed (discriminant analysis). This likely introduced data leaks"

CC (2026-07-27, Lennart): **Confirmed leak — stays No.** One feature is *"Score of discriminant analysis
of the amino acid content of vacuolar and extracellular proteins"* — a supervised discriminant analysis
fit on the whole dataset and baked into every row. That transform needs a train/test split to be
leak-free, but the data was already processed once and cannot be recomputed per split, so it
irreversibly leaks the test distribution (`Data Quality Issue`, crit. 4D).

## Review

**Outcome:** not added; `No` (2026-07-27) for one label-fitted column, which the amended rule on fitted scores now drops
while keeping the task.

**Main points:** Re-check yeast as ecoli_proteins was decided?

**Issues for Andrej:**

1. **Re-check yeast under the amended rule on fitted scores?**

   * **Problem:**
     - yeast's `No` rests on one column, `vac`, a discriminant score of vacuolar and extracellular proteins fit on
       the whole labelled set.
     - The rule now drops such a column and keeps the task when the other columns still make a real one[^1].
     - ecoli_proteins, the same authors' sibling, was kept with its `aac` score dropped (2026-11-11, Andrej).
   * **Unknown:** whether mcg, gvh, alm, mit, erl, pox and nuc make a real task without `vac` (TabPFN against logistic
     regression, per-class recall), not measured.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep `No` (implemented) | the record as it is | nothing to do | departs from ecoli under the amended rule |
     | B | Re-check | screen again without `vac`; add it if the rest makes a real task | consistent with ecoli | work for a 1996 dataset with `Outdated` scores |

   * **Recommendation:** B. **Decision:** A or B?

   [^1]: **LEAK-27** (Must): a feature fit by a supervised transform on the whole labelled set cannot be refitted per
     split: drop it, and keep the task when the other columns still make a real one; `No` when the transform runs
     through the columns the task needs or the task rests on it.
