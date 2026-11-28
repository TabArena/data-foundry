---
unique_name: body_density_prediction
name: bodyfat
checked_by:
- Lennart
- Andrej
data_foundry_status:
- 'DF: Yes'
- BeyondArena
suggestion: Yes (Disagreement)
priority: 2
decision_markers:
- Outdated
- Not Representative
- Too Small
tags:
- Tiny Data
- 'Samples: No Time Dimension'
- Experimental Results
collections:
- TabArena Reject
original_source: Other
year: '1995'
collection_period: Unknown
domain: medical & healthcare
required_split:
- Random (IID)
problem_type: Regression
original_data_state: One Table
source_links:
- https://www.openml.org/d/560
- https://www.kaggle.com/datasets/fedesoriano/body-fat-prediction-dataset
notebook_path: datasets/beyond_iid/new_iid/body_density_prediction/body_density_prediction.ipynb
v2_path: datasets/_dev/tabarena-v0pt2/body_density_prediction/dataset.py
source_row: 750
type_adapter_id: curation-record-v1
---

## Comments

Looking good, might be trivial or easy

original source is UCI, now gone. Found on OpenML and on Kaggle

Data looks good but is a bit old. There should be more/newer data with the same task as this is still done by models in machines in gyms.

Note, the task is not about bodyfat prediction as this is determined by a deterministic formula. Instead, the task is to estimate the density (which can be used to get the body fat via the deterministic formula). However, density requires a test. So we aim to predict from data the density such that we can skip this test.

Discussion: In general a valid task, but if someone would actually want to build a serious predictive model for that it would be possible to collect a lot more data.

Also, I think that the use from this is limited unless we actually embed the density prediction into the body fat formula and evaluate on that. Better alternatives for this task (ChatGPT):
1) NHANES https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2021/DataFiles/BMX_L.htm
2) UK Biobank (restricted access): https://www.ukbiobank.ac.uk/about-our-data/types-of-data/physical-measurements/

CC (2026-10-15, Andrej): Replacement candidate: `nhanes_dxa_body_fat` (NHANES DXA percent fat from anthropometry, thousands of people of both sexes; see that record).

**Assessment (AI, 2026-10-21):** Metric declared under MET-1..13: source rmse — the standard error of estimate of the prediction equation in Penrose, Nelson & Fisher 1985 and Johnson 1996.

**Assessment (AI, 2026-10-27):** The open questions for the curator are in the record's Review (review of the Tiny Data datasets, written from the earlier findings, no review panel); the AI recommends shipping it until better data replace it. Priority 2: gap -, use case + (Penrose et al. 1985 build equations to replace underwater weighing), source +, shape -, risk - (better data in triage would make it a near-duplicate).
**Assessment (AI, 2026-10-31):** better data: the data-scouting run of 2026-10-30/31 found better data for the same task: `nhanes_dxa_body_fat` (TBD -> Yes, priority 4). Each is screened in its own record; this record's verdict stays the curator's.

**Assessment (AI, 2026-11-04):** reviewed for BeyondArena v0.2, without a panel, from the gathered evidence (this record, earlier experiments, model runs on the shipped data); the open questions are in the record's Review. Keep until nhanes_dxa_body_fat (the same task on about 21,800 people) is added, then retire as replaced; meanwhile set the impossible 29.5-inch height to missing. Priority 2: gap 0, use case 1, source 1, shape 0, risk -1.

CC (2026-11-06, Andrej): time basis `Timeless` accepted (Review  3, B, through the cross-dataset item on routine `Timeless` issues): each man was measured once in one study session, so density and features describe the same body at one time. It holds if issue 1 keeps the dataset. The `Time basis:` line is in the definition's notes, ending with what the split cannot test; the tag enters `data_tags`.

CC (2026-11-18, Andrej): collection type stays `Experimental Results` (Review issue 5, A as implemented; full-information split check, 2026-11-18). Supersedes the Clinical Study mark of 2026-11-17 (issue 4):
- the type rules call volunteers measured by a study protocol experimental results;
- the split is random under either type.

## Review

**Outcome:** added. Johnson's StatLib bodyfat file of the 252 men of Penrose et al. 1985: body density measured by
underwater weighing, predicted from age, weight, height and ten tape measurements; the body-fat percentage, computed
from the density, is dropped. Reviewed without a panel, from the gathered evidence: the record, the replacement
candidate's record, model runs on the shipped BeyondArena data (the same rows) and a check of 2026-11-04.
The AI recommends shipping it until `nhanes_dxa_body_fat` is added and then deciding whether it is retired as
replaced (issue 1). Validity: a direct fit (USE-8): the features are the cheap measurements a gym or clinic has, the
label the costly test they replace; the metric is the source's standard error of estimate (RMSE). Value: the 40
benchmark methods lie within 15% of each other (RMSE 0.0102 to 0.0118, median 0.0105) and tuned linear regression is
within 4% of the best, so the dataset separates methods little. Quality: one man is recorded 29.5 inches tall, and
one density implies negative body fat (issue 2); `Outdated`, `Not Representative` and `Too Small` are on the record,
none tested. Weighed: a direct, still common use case against a small, dated sample with a much larger public one in
triage.

**Main points:** Parked (2026-11-11) on Andrej's note until it is decided whether better suited datasets replace this task: `nhanes_dxa_body_fat` as replacement (issue 1) and the impossible height (issue 2) wait. The `Timeless` split is settled (issue 3), and the type stays `Experimental Results` (issues 4 and 5, 2026-11-18).

**Record judgment:** valid task, better data available. The Discussion calls the task valid but limited, since much
more data could be collected; Andrej's CC of 2026-10-15 names the replacement, and the data-scouting run of
2026-10-31 rated it `TBD -> Yes`, priority 4. The suggestion is `Yes (Disagreement)`.

**Issues for Andrej:**

1. **Keep body density until `nhanes_dxa_body_fat` is added, or retire it now?**

   * **Problem:**
     - The task is real and still done (gyms and clinics estimate body fat from simple measurements), but the data
       are 252 men of one study published in 1985.
     - `nhanes_dxa_body_fat` (CC 2026-10-15, Andrej) is the same task on a US survey, percent fat from a DXA scan
       predicted from tape and scale measurements for about 21,800 people of both sexes aged 8 to 85, still in triage
       with no folder.
     - Keep this dataset until the replacement is added, retire it now, or keep both?
   * **Background:** a small or dated dataset whose task is still done is not rejected when better data turn up: the
     better data become their own record, and the old one keeps the verdict its own data earn until a curator
     decides[^1a]. This pair is the case the rule names. The tag `Better Data Available` that the earlier file
     proposed no longer exists; the record already carries the pointer (CC 2026-10-15) and the Assessment line of
     2026-10-31.
   * **Effect on the task:** none on this definition. Retiring it now leaves the benchmark without this use case until
     the NHANES dataset is added; keeping both puts one use case in it twice, once much smaller.
   * **Experiments:**
     - The nhanes_dxa_body_fat record (5-fold, R² on percent fat, linear / gradient boosting): NHANES 1999-2006 with
       all tape and scale measurements 0.80 / 0.87; this file's body-fat percentage with the same check 0.71 / 0.65.
     - Model runs on the shipped data (20 x 3 splits, RMSE on the density, standard deviation 0.0190): the
       40 benchmark methods 0.0102 to 0.0118 (median 0.0105; TabPFN 3.5 FAST 0.0103, tuned linear regression 0.0106),
       and a regularised linear model of abdominal girth against frame size and age 0.0101, ahead of all of them.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep until replaced (implemented) | ships as defined; retired as replaced once `nhanes_dxa_body_fat` is accepted | the use case stays in the benchmark meanwhile | a small, dated sample ships in the meantime |
     | B | Retire now | `No (Retired)`; the folder leaves the working copy | no small, dated sample | the use case is missing until the replacement is added |
     | C | Keep both | both ship once NHANES is added | two populations | one use case twice, once at 1% of the size |

   * **Recommendation:** A: the old record keeps the verdict its data earn until the replacement is decided.
     **Decision:** keep until replaced (A), retire now (B) or keep both (C)?

   **Notes for the AI:** on A, add a dated CC line "keep until `nhanes_dxa_body_fat` is accepted, then retire as
   replaced"; when that record is accepted, retire this one (`No (Retired)`, folder removed, CHANGELOG entry). On B,
   retire now the same way.

   [^1a]: Pattern "Small or dated, and the task is still done today" (selection.md): a hit from another source is its
     own record, not a `Duplicate`; the old record is not rejected automatically. Cases: body_density_prediction and
     NHANES DXA body fat. **TP-6** (Must): a valid task stays.

   **Deferred (2026-11-11):** parked on Andrej's note ("Park it until we decide on checking in with better suited datasets for this task.").

2. **Only if kept: set the impossible height to missing?**

   * **Problem:**
     - One man of 205 pounds is recorded 29.5 inches tall (a BMI of 166), which cannot be right.
     - One density, 1.1089, implies a body fat of -3.6% by Siri's formula, the one the use case applies to the
       density, and two more imply under 1% (1.0991 and 1.0983).
     - Set the height to missing, also drop the man with the impossible density, or keep the file as published?
   * **Background:** Siri's formula turns a density into body fat (495 / density - 450); a density above 1.100 means
     less than no fat, so 1.1089 is either a misrecorded weighing or a man the formula does not fit. The density is
     the target, so its row would go, not the value. The best model found treated heights under 50 inches as
     missing.
   * **Effect on the task:** small; one feature value and at most one target value of 252.
   * **Experiments:** check of 2026-11-04 on the shipped data (the same rows as v0.2): every other height is 60
     inches or more (up to 77.75); densities 0.995 to 1.1089; BMI 18 to 49 apart from the 29.5-inch man.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep as published (implemented) | 252 rows unchanged | the file as published | an impossible height stays a feature value |
     | B | Height to missing | the 29.5-inch height missing, the row stays | the impossible value goes; the row's density stays | none found |
     | C | B, and drop the 1.1089 row | 251 rows | no target outside the formula's range | a measured target dropped on a judgment |

   * **Recommendation:** B: the height is impossible and the row's other values are not; the density is unusual
     rather than impossible, so it stays with a note[^2a]. **Decision:** keep (A), height to missing (B) or also drop
     the density row (C)?

   **Notes for the AI:** on B, in `_clean` set `Height` to missing where it is below 50 inches, add a
   `curation_comments` bullet (and one on the two densities that imply under 1% fat and the one above 1.1, kept), re-run
   `dataset check`, CHANGELOG entry. On C, also drop the row with `Density` above 1.1.

   [^2a]: **CLEAN-11** (Should; amended 2026-10-21): impossible values become missing, and the row stays; values that
     are only unusual stay.

   **Deferred (2026-11-11):** parked on Andrej's note ("Park it until we decide on checking in with better suited datasets for this task.").

3. **Only if kept: name the random split `Timeless`, or `StationaryRelation`, for one measurement session per man?**

   * **Problem:**
     - Each man was measured once, tape, scale and underwater weighing in one study session before 1985, so the
       density and every feature describe the same body at the same time, and no study date or measurement order is
       recorded.
     - The record carries `Samples: No Time Dimension` and no time or target fact, which fits; the split is random
       over men and has no time-basis tag yet.
     - The density is a physical property of the body as measured, read through anatomy, which reads as `Timeless`
       like a material's strength; read strictly, a man's density is not the same whenever it is measured, which puts
       it under `StationaryRelation`, argued from the source[^3a].
   * **Background:** the arrival study found nothing that arrives after the session and no repeated man. The body-fat
     percentage, computed from the density, is already dropped. The deployed population (today's gym and clinic
     clients, women) differs from 252 men of the early 1980s; that is representativeness, which issue 1 weighs.
   * **Experiments:** the StatLib file, model-free: the first 143 cases, from which Penrose et al. derived their
     equations, match the other 109 on every column (Mann-Whitney p 0.13 to 0.94; mean density 1.056 against
     1.055); along the file only age rises (Spearman 0.33), the density does not (-0.10, p 0.10). The order is no
     period that moves the target.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Random split, no time-basis tag (implemented) | as now | nothing to change | the definition does not say why a random split is safe in time |
     | B | Random split, `Timeless` | as now; the tag and a `Time basis:` line naming the one session per man | the target is a physical measurement of the body it describes; matches the study and the record's `No Time Dimension` | a person's density changes over the years, which the prototype's wording ("the same whenever it is measured") does not cover |
     | C | Random split, `StationaryRelation` | as now; the line argues from the source that the relation of shape to density does not move | names a present state read through a fixed relation | the prototype is meant for samples that arrive over time from a practice, which a one-off lab study is not |

   * **Recommendation:** B, if issue 1 keeps the dataset: one session per man, nothing measured later, and the target
     is physics of the body that the features describe at the same moment. **Decision:** A, B or C?

   **Notes for the AI:** on B: `data_tags = ("Timeless",)` (the class adds `IID`), a curation
   bullet `- Time basis: Timeless: each man was measured once (tape, scale and underwater weighing in one study at
   BYU, before 1985), so density and features describe the same body at one time; no date or order is recorded, and
   the derivation block of the first 143 cases does not differ from the rest.`; on C the same fact with the tag
   `StationaryRelation`; `splits_comment` unchanged; `dataset check`. Nothing applies if issue 1 retires the dataset.

   [^3a]: **SPLIT-32** (Should): how the data was collected is information for the split; a definition can name the
     use-case prototype it follows with a `Time basis:` line. `Timeless`: the target is a fixed property of the
     item, the same whenever it is measured (a material's strength, a molecule's activity, a species, the outcome of
     a designed run). `StationaryRelation`: the samples arrive over time, and the target is a present state read
     through a relation that time does not move (a diagnosis, a tissue type), measured on a dated source and argued
     from the source where the time is lost.

   **Resolved (2026-11-06, Andrej):** B, accepted through the cross-dataset item "Accept the routine `Timeless` time
   issues with one mark?" The `Time basis: Timeless:` bullet is in `curation_comments`, ending with what the split
   cannot test (bodies measured in another study, such as women); the split and `data_tags` are unchanged. It holds if
   issue 1 keeps the dataset. The tag `Timeless` enters `data_tags`.

4. **Collection type: `Clinical Study` instead of `Experimental Results`?**

   * **Problem:**
     - The record's collection type is `Experimental Results`, the root the walk started from.
     - The walk reads the data as `Clinical Study`: The men were measured in one study at one lab, closer to a clinical study at one site than to designed experimental runs; walked under Experimental Results as recorded..
     - The walk followed the recorded type and reached Random · Timeless.
   * **The doubt:** The men were measured in one study at one lab, closer to a clinical study at one site than to designed experimental runs; walked under Experimental Results as recorded.
   * **What changes:** the record's collection-type tag only. The split follows from it, so the tree must be re-walked under the new type; where that gives the same leaf, nothing else changes.
   * **Blindness:** what the walker saw of the shipped split before deciding: saw: split_tree.md lists body_density_prediction as an example under 'Random · Timeless'; ignored as evidence.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep `Experimental Results` (implemented) | no change to the record | the type as the taxonomy assigned it | the doubt stays on the record |
     | B | Tag `Clinical Study` | changes the record's type tag and re-walks the tree from it | The men were measured in one study at one lab, closer to a clinical study at one site than to designed experimental runs; walked under Experimental… | the type rules must agree; the leaf may change |

   * **Recommendation:** discuss: the collection-type rules decide this, the walk only raises it. **Decision:** A or B?

   **Notes for the AI:** blind walk of 2026-11-17 (split tree at cd3877cb). On B: change the record's type tag to `Clinical Study`, re-walk the tree from it and check whether the leaf changes; update the type rules' examples.

   **Andrej (2026-11-17, change):** Option B: Tag Clinical Study.

   **Answer (AI, 2026-11-17):** Clinical Study needs the men to have arrived over time, and the record says they did not:
   change that fact as well?

   * **Problem:**
     - The type rules sort undated data on people by how it arrived: a clinical study when the people arrived over
       time, experimental results when the data has no time dimension[^bd1].
     - The record's fact is `Samples: No Time Dimension`, and the source (Penrose, Nelson and Fisher 1985) dates no
       measurement; nothing shows the 252 men were measured over a period that matters to the use case.
     - The split stays random under either type; as a clinical study its tag becomes `ForcedIIDFromTemporal` in place
       of `Timeless` (accepted 2026-11-06).
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | a | `Clinical Study` and `Samples: Over Time` | both record tags change; the tag becomes `ForcedIIDFromTemporal` | the walk's reading: men measured one after another for one study | no source says when or over how long |
     | b | `Clinical Study` only | the type changes, the fact stays | as marked | breaks the rule on undated people data; needs a written exception |
     | c | Keep `Experimental Results` (implemented) | no change | the rule and the record's fact agree | the walk's reading is not taken up |

   * **Recommendation:** c: the rule rests on arrival over time, which nothing documents here, and the split is
     random under every option. **Decision:** a, b or c?

   [^bd1]: **SPLIT-34** (Should), rule 5: patient data without dates is a clinical study when the patients arrived
     over time, and experimental results when the data has no time dimension.

   **Resolved (2026-11-18, Andrej):** superseded by issue 5, where `Experimental Results` is kept as implemented (A).

5. **Keep the type `Experimental Results`?**

   * **Problem:**
     - You marked `Clinical Study` (2026-11-17); the type rules call a closed set of volunteers measured by a study protocol experimental results, and a clinical study patients labelled by a diagnosis or a follow-up outcome[^s34t].
     - The 252 men were measured once by underwater weighing; body density is neither a diagnosis nor an outcome, and the record dates no arrival.
     - The split stays random under either type; only the tag and the type rules' examples change.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | `Experimental Results` (implemented) | No change | What the type rules say | |
     | B | `Clinical Study` | The type definitions are amended so measured volunteers count as clinical | Your mark | The tree's clinical branch then asks for a site or an arrival order the data does not hold |

   * **Recommendation:** A, because the type rules describe this case and the split does not change. **Decision:** A or B?

   [^s34t]: **SPLIT-34** (Should): "`Experimental Results`: ... a closed set of specimens, molecules or volunteers measured by a laboratory or a study protocol. `Clinical Study`: patients of a clinical study, a clinic's case series or a registry, labelled by a diagnosis or a follow-up outcome."

   **Andrej (2026-11-18, ok):** As implemented (A).

   **Resolved (2026-11-18, Andrej):** A, as implemented: `Experimental Results` (252 volunteers measured once by a study protocol; body density is neither a diagnosis nor a follow-up outcome). The split stays random, `Timeless`. Nothing changes.

## Reference

@article{penrose1985generalized,
  title={Generalized body composition prediction equation for men using simple measurement techniques},
  author={Penrose, Keith W and Nelson, Arnold G and Fisher, Arnold Garth},
  journal={Medicine \& Science in Sports \& Exercise},
  volume={17},
  number={2},
  pages={189},
  year={1985},
  publisher={Ovid Technologies (Wolters Kluwer Health)}
}
