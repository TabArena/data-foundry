---
unique_name: musk
name: musk
checked_by:
- Lennart
- Andrej
data_foundry_status:
- 'DF: Yes'
- BeyondArena
- WIP (DF)
claimed_by: Andrej
suggestion: 'Yes'
priority: 3
tags:
- Tiny Data
- Non-IID (Grouped)
- 'Samples: No Time Dimension'
- 'Entities: Recur'
collections:
- TabArena Reject
original_source: UCI
year: '1994'
domain: chemistry & material science
required_split:
- Grouped (NON-IID)
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://archive.ics.uci.edu/dataset/75/musk+version+2
- https://www.openml.org/search?type=data&sort=runs&id=1116&status=active
- https://doi.org/10.24432/C51608
- https://doi.org/10.24432/C5ZK5B
notebook_path: datasets/beyond_iid/grouped/musk/musk.ipynb
v2_path: datasets/_dev/tabarena-v0pt2/musk/dataset.py
source_row: 5
type_adapter_id: curation-record-v1
---

## Comments

CC: "multiple instance problem - multiple instances of the same molecule are in the data. The classifier should classify as 1 if any of the instances is 1 (0 if none). Leak if used with random splits. Classic Physics/Chemistry application, definitely worth including. Not in TabRepo, but likely due to leak; Could be used after preprocessing to reduce to the original (very small) dataset of 102 molecules. When done, the dataset is however too small for our selection size"

We use musk version 2 as a starting point and treat it as a grouped prediction task

AT: No disagreement, but we should discuss how to treat the multi-instance problem

CC (2026-10-06, Lennart): Kept in TabArena v0.2 as a valid tiny-data task after the task-probe review (flags `no_spread`, `unstable`). v2 scores per molecule (`any` over its conformations): 102 molecules, 39 musk and 63 non-musk, so each grouped test fold scores 34 molecules (13 musk, 21 non-musk; 273 pairs per ROC AUC). That is small, like other tiny tasks, but not a handful: parkinsons was retired for 2-3 healthy people per fold out of 8 in total. The probe's three untuned families reach skill +0.61 to +0.72 (standard deviation 0.11-0.13 over 5 splits); on BeyondArena (scored per conformation) the best method (Causilo) reaches AUC 0.892 and the median 0.850, with 8 of 29 methods tied with the best and ranks that vary from fold to fold (Kendall's W 0.17), as expected at this size.

**Assessment (AI, 2026-10-21):** Metric declared under MET-1..13: fallback roc_auc — Dietterich et al. 1997 report per-molecule accuracy (10-fold CV), as all multiple-instance work does: a habit without costs; 34 molecules per test fold, so accuracy moves in steps of about 3% (MET-10). Original rejected: accuracy. roc_auc is the binary fallback, per molecule (aggregation any).

**Assessment (AI, 2026-10-27):** The open questions for the curator are in the record's Review (review of the Tiny Data datasets, written from the earlier findings, no review panel); the AI recommends shipping it. Priority 4: gap +, use case + (Dietterich et al. 1997 name the use), source +, shape -, risk +.
**Assessment (AI, 2026-10-31):** better data: the data-scouting run of 2026-10-30/31 found better data for the same task: `leffingwell_odor_musk` (TBD -> Yes, priority 2). Each is screened in its own record; this record's verdict stays the curator's.

**Assessment (AI, 2026-11-04):** reviewed for the BeyondArena v0.2 review page, without a panel, from the gathered evidence (this record, earlier experiments, model runs on the shipped data); the open questions are in the record's Review. Ship as defined: the source's multiple-instance task scored per molecule, 13 musk molecules per test fold (tiny, not too small), and the methods spread, with a molecule-level model well ahead of all benchmark methods. Priority 3: gap 0, use case 1, source 1, shape 0, risk -0.

CC (2026-11-06, Andrej): time basis `Timeless` accepted on the BeyondArena v0.2 review page (issue 2, B, through the cross-dataset item on routine `Timeless` issues): the shapes are computed from each molecule's structure and the label is an expert's judgement of the molecule, with no date. The `Time basis:` line is in the definition's notes, ending with what the split cannot test; the tag enters `data_tags` once PR #50 is in the working copy.

CC (2026-11-09, Andrej): ship as defined (review page issue 1, A), scored per molecule; the declared split and metric checked and kept.

## Review

**Outcome:** added. The AI recommends shipping it as defined; nothing is open beyond the verdict (issue 1). Reviewed
without a review panel, from the gathered evidence: the record, Lennart's task-probe review of 2026-10-06 and the
model runs on the shipped data. The data are UCI's Musk version 2 (Dietterich et al. 1997): 6,598 low-energy
conformations (3D shapes) of 102 molecules, 39 judged musk by human experts, each described by 166 shape numbers.
Validity: a molecule is a musk if any of its conformations is, as the source defines it; molecules are held out whole
and scored once each; the molecule names, which gave the label away, are replaced and the conformation names dropped;
the fit is direct. Value: tiny (34 molecules per test fold, 13 of them musk) but not too small; on the shipped data
the benchmark methods spread from 1-AUC 0.11 to 0.23, and a simple model that summarises each molecule by the mean of
its conformations beats them all (0.045 on the 9 splits it ran on, best benchmark 0.110), so the task rewards methods
that treat the molecule as the unit. Quality:
nothing open. Weighed: a documented source and a classic multiple-instance task +, methods that spread +, ranks that
vary from fold to fold at this size -.

**Main points:** Ship as defined, scored per molecule (issue 1, resolved 2026-11-09); the molecule split is named
`Timeless` (issue 2, resolved 2026-11-06).

**Record judgment:** valid. The multiple-instance question raised early ("how to treat the multi-instance problem") is
answered by the molecule grouping and the per-molecule scoring, and Lennart's comment of 2026-10-06 settles the size.
The Assessment of 2026-10-31 names `leffingwell_odor_musk` as better data for the same task; that record's own
screening counts 20 musk molecules among 3,522, so it is no better data for this label. The README's warning that
`feature_52` holds the sentinel-looking value -1 in 4.9% of rows is a false alarm: it is a ray distance, and UCI says
"the distances may be negative or positive, since they are actually measured relative to an origin placed along each
ray". No record field disagrees with the definition.

**Issues for Andrej:**

1. **Ship in TabArena v0.2 as defined?**

   * **Problem:**
     - Lennart kept musk on 2026-10-06 after the task-probe review: scored per molecule (musk if any of its
       conformations is), each grouped test fold holds 34 molecules (13 musk, 21 not), small but not a handful.
     - At this size the ranks of methods vary from fold to fold, and many methods tie with the best.
     - Ship as defined, go back to scoring every conformation as BeyondArena did, or retire as too small?
   * **Background:**
     - A dataset is too small only when a class has a handful of units per test fold and in total, counted in the
       unit the task is scored on; a small dataset as such is a tiny-data task like the others, with musk as the
       rule's own case[^1a]. parkinsons was retired for 2 to 3 healthy people per fold out of 8 in total.
     - The unit of prediction follows the source's use case[^1b]: UCI's instructions say a molecule is musk if "ANY
       of its conformations is classified as a musk", and Dietterich et al. score molecules in a 10-fold
       cross-validation over the 102. The metric is ROC AUC per molecule (checked 2026-10-21), as accuracy on 34
       molecules moves in steps of about 3%.
     - The multiple-instance question Andrej raised early ("how to treat the multi-instance problem") is answered by
       this per-molecule scoring and the grouping by molecule.
   * **Effect on the task:** scoring per conformation, as BeyondArena does, weighs each molecule by its number of
     conformations: three non-musk molecules hold 1,044, 1,010 and 911 rows (45% of the table), the largest musk
     molecule 215.
   * **Experiments:**
     - Lennart's task-probe review (2026-10-06): three untuned model families reach skill +0.61 to +0.72 (standard
       deviation 0.11 to 0.13 over 5 splits). On BeyondArena, scored per conformation, the best method reaches ROC
       AUC 0.892 and the median 0.850; 8 of 29 methods tie with the best, and ranks vary from fold to fold (Kendall's
       W 0.17).
     - Model runs on the shipped data (per-conformation 1-AUC): the benchmark methods range from 0.108 (Causilo,
       21 splits) to 0.234 (CatBoost default, 60 splits). On the 9 splits the run used, TabICLv2 0.110 is best and
       CatBoost default 0.229 worst, and a logistic regression on the similarity of a molecule's mean conformation to
       the training molecules scores 0.045, first of 38. A molecule-level view is worth more than any benchmark method
       gets from the rows.
   * **Consistency:** musk is the case the size rule names as kept; parkinsons_biomedical_voice_measurements is the
     retired counter-case.
   * **Sources:** the UCI page, <https://doi.org/10.24432/C51608>; Dietterich TG, Lathrop RH, Lozano-Pérez T,
     "Solving the multiple instance problem with axis-parallel rectangles", Artificial Intelligence
     1997;89(1-2):31-71, <https://doi.org/10.1016/S0004-3702(96)00034-3>.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Ship as defined (implemented) | molecules held out whole; one prediction per molecule (any of its conformations), ROC AUC over 34 test molecules | the source's multiple-instance task; every molecule counts once | ranks vary from fold to fold at this size |
     | B | Score every conformation | rows scored one by one, as BeyondArena does | more test units per fold | three non-musk molecules carry 45% of the score; not the source's unit |
     | C | Retire as `Too Small` | record `No (Retired)`, folder removed | no noisy tiny task | 13 musk molecules per fold is no handful; departs from the rule's own case |

   * **Recommendation:** A, the source's task at the source's unit, and not too small by the rule.
     **Decision:** ship as defined (A), score per conformation (B), or retire (C)?

   **Notes for the AI:** on A, a `CC (<date>, Andrej):` line in the record and `Andrej` added to `checked_by`. On B,
   `Grouping(prediction_unit="row", aggregation=None)` and the metric reason updated. On C, the retirement steps:
   record `No (Retired)` with `Too Small`, folder removed, `v2_path` cleared, CHANGELOG entry, and the musk case row
   of the size rule revised.

   [^1a]: **TP-5** (Must): `Too Small` means a handful of units of a class, per test fold and in total, counted in
     the unit the task is scored on (parkinsons: 8 healthy people, 2-3 per fold; retired). A small dataset as such is
     a tiny-data task like the others (musk: 102 molecules, 13 musk per fold; kept).
   [^1b]: **SPLIT-23** (Must): the source's use case, cited, decides what one prediction is (a row, or a whole group:
     any instance positive, ...) and what is known about a new group when predicting.

   **Resolved (2026-11-09, Andrej):** ship as defined (A), scored per molecule; the declared split and metric checked
   and kept.

2. **Time basis: name the molecule split `Timeless`?**

   * **Problem:**
     - Every row is a shape computed from a molecule's structure, all of a molecule's shapes at once, and the label is
       an expert's judgement of the molecule's smell, made before 1993 and not dated; no row comes before another.
     - The record carries `Samples: No Time Dimension` and no time or target fact, which fits; the split holds out
       whole molecules and names no time basis yet.
     - Whether a molecule smells of musk is a fixed property of the molecule, the case the `Timeless` prototype
       names[^2a].
   * **Background:** the 102 molecules come from decades of fragrance chemistry, and the order in which they were made
     is not in the release. The names that gave the label away were replaced and no structure ships, so neither a
     date nor a chemical series can be recovered. The grouping already keeps every shape of a test molecule out of
     training, the only rows that share its label.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Molecule split, no time basis (implemented) | as now | nothing to change | the definition does not say why a split that is not temporal is safe in time |
     | B | Molecule split, `Timeless` | as now; the tag and a `Time basis:` line naming the computed shapes and the fixed label | states the fact the split rests on; as the other designed and property datasets | none found |

   * **Recommendation:** B: the label is a property of the molecule and the shapes are computed, so time plays no
     part. **Decision:** A or B?

   **Notes for the AI:** on B, once PR #50 is in: `data_tags = ("Timeless",)` (the class adds `Non-IID`, `Grouped`),
   a curation bullet `- Time basis: Timeless: the shapes are computed from each molecule's structure, all at once,
   and the label is an expert's judgement of the molecule's smell (Dietterich et al. 1997); no row is dated, and every
   shape of a test molecule is held out with it.`, `splits_comment` unchanged; `dataset check`.

   [^2a]: **SPLIT-32** (Should): how the data was collected is information for the split; the record carries the
     source's collection facts, and a definition can name the use-case prototype it follows with a `Time basis:`
     line. `Timeless`: the target is a fixed property of the item, the same whenever it is measured (a material's
     strength, a molecule's activity, a species, the outcome of a designed run); the split is random or grouped by
     item family.

   **Resolved (2026-11-06, Andrej):** B, accepted through the cross-dataset item "Accept the routine `Timeless` time
   issues with one mark?" The `Time basis: Timeless:` bullet is in `curation_comments`, ending with what the split
   cannot test (a new chemical class outside the 102 molecules); the split and `data_tags` are unchanged. The tag
   `Timeless` enters `data_tags` once PR #50 is in the working copy.

## Reference

10.24432/C51608
