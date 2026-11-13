---
unique_name: horse_colic_survival
name: horse_colic_*
checked_by:
- Lennart
- Andrej
data_foundry_status:
- 'DF: Yes'
- BeyondArena
suggestion: 'Yes'
decision_markers:
- Outdated
- Class-dependent Recording
tags:
- Tiny Data
- Non-IID (Grouped)
- 'Samples: Over Time'
- 'Time: Inferred'
- 'Target: Varying Delay'
- 'Entities: Recur'
collections:
- TabArena Reject
- TabSTAR
original_source: UCI
year: '1989'
domain: biology & life sciences
required_split:
- Grouped (NON-IID)
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://github.com/EpistasisLab/pmlb/blob/master/datasets/horse_colic_lesion_type/metadata.yaml
- https://www.openml.org/search?type=data&id=25
- https://doi.org/10.24432/C58W23
notebook_path: datasets/beyond_iid/new_iid/horse_colic_survival/horse_colic_survival.ipynb
v2_path: datasets/_dev/tabarena-v0pt2/horse_colic_survival/dataset.py
source_row: 761
type_adapter_id: curation-record-v1
---

## Comments

Has multiple possible classes (lesion or others). Decide for one that is reasonable

**Assessment (AI, 2026-10-21):** Metric declared under MET-1..13: fallback log_loss — The UCI donation (McLeish & Cecile, 1989) defines no metric; its stated class attribute is the surgical lesion (attr 24), not the outcome we predict, and no paper defines an evaluation for the outcome task.

**Assessment (AI, 2026-10-30):** Dtype review (branch ordinal-and-censored-levels; the column decisions with their codebook evidence are on the review board): 8 ordinal scales typed as ordered categories in the codebook's order (CLEAN-14, amended): `temperature_of_extremities`, `peripheral_pulse`, `capillary_refill_time`, `peristalsis`, `abdominal_distension`, `nasogastric_tube`, `nasogastric_reflux`, `rectal_exam_feces` (the README lists their levels); their codes that mean unknown (don't know, refused, not asked) are missing in `capillary_refill_time` (CLEAN-10); left unordered: `mucous_membranes` (a partial order); `pain` (a partial order).

CC (2026-10-21, Andrej): 344 horses with colic (abdominal pain) from the University of Guelph, Canada, donated in 1989; the label is whether the horse lived, died or was euthanized (put down). I disagree with keeping it.
- **Died vs euthanized follows the admission period, and a feature gives the period away:** among non-survivors, earlier case numbers are 58 died / 14 euthanized, later ones (above about 530,560) 4 / 34, with similar clinical findings. `total_protein` (a blood value) switches from g/dL to g/L at the same time: in g/L rows 1 of 28 non-survivors died, in g/dL rows 64 of 80. Severe: one class split reflects when the horse came in, not its condition, and models use the unit (TabPFN log loss 0.68 vs 0.72 with one unit).
- Suggest excluding, or reframing as lived vs not. Evidence: the curation notes (target, recording change).

CC (2026-11-01, Lennart): marks on the review board of PR #37: pain and mucous_membranes stay unordered as partial orders, noted in the definition.

CC (2026-11-01, Lennart): the decode rule (a code whose codebook says in words what each level is carries the words; a score without them is a number): 13 coded columns carry their words.

**Assessment (AI, 2026-11-05):** marker `Class-dependent Recording`: `total_protein` (a blood value) is written in g/L for 95 horses (1 died, 27 euthanized) and in g/dL for 209 (64 died, 16 euthanized). The unit switch follows the hospital number, that is the admission period, so the unit alone tells died from euthanized (ROC AUC 0.79). Not harmonised yet: one unit for all rows raises TabPFN 3.5's log loss from 0.682 to 0.724. Noted in the definition's curation comments; data unchanged.

CC (2026-11-10, Andrej): decisions on the BeyondArena v0.2 review page.
- **Target: did the horse survive (lived against died or euthanized).** Died against euthanized follows the admission period, not the horse's condition; survival does not (Fisher p = 0.16 against the recording route). This is the usual survival-to-discharge outcome (Bishop et al. 2022, Vet Surg 51:891, https://doi.org/10.1111/vsu.13839).
- **Split: three windows of 57 horses in case-number order**, each trained on all earlier horses: a vet scores later admissions with a model built on earlier ones. A random split mixes both recording periods into every training fold.

**Assessment (AI, 2026-11-10):** collection, from the creators' papers: one hospital, the teaching hospital of the Ontario Veterinary College, Guelph; rows from its patient information system, lab values largely written by the lab equipment (Cecile & McLeish, https://arxiv.org/abs/1304.2344; McLeish et al., https://arxiv.org/abs/1304.1519). No admission dates; the case number orders the admissions. The first 229 case numbers (60% lived) match the 231 teaching-hospital horses of Pascoe et al. 1990 (Can J Vet Res, https://pmc.ncbi.nlm.nih.gov/articles/PMC1255672/, 61% survivors); the later 115 (67% lived) mostly follow the second recording route. A reading of the counts, not stated by the source. Records sometimes "ended because euthanasia was chosen as a solution for cost reasons", so missing values can follow the outcome. UCI's 300/68 files are not a time split.

CC (2026-11-10, Andrej): review page, issues 2, 4 and 5.
- **Both recordings kept as a shift between earlier and later admissions** (an exception to CLEAN-21, withdrawn on 2026-11-12), not harmonised.
- **Return visits kept:** the 10 later visits of 9 cases stay; a returning horse is an admission to score, and the time order keeps each later visit after its first. The use case and row now name admissions, first or return.
- **`Class-dependent Recording` stays:** the shipped target does not have it, but the source file does, so it stays in the curation record.

CC (2026-11-12, Andrej): review page, issues 7 and 8 (reopened after Lennart's comment on PR #55).
- **Recording harmonised, the exception to CLEAN-21 of 2026-11-10 withdrawn:** `total_protein` above 15 (g/L, 95 horses) is divided by 10 to the codebook's g/dL, and the 55 cells of 1/2 codes the later recording writes in `abdominocentesis_total_protein` and `nasogastric_reflux_ph` are missing. An analyst at the hospital knows its lab's unit, and the codes cannot be read as measurements. Kept as recorded, the unit only broke logistic regression in the window that first meets it (log loss 2.126 against 0.761 harmonised).
- **The evidence pointer of 2026-10-21** now names the curation notes instead of a folder on one machine.

CC (2026-11-12, Andrej): review page, issue 6, answering Lennart's question on PR #55 (back to a random split?): random horses grouped by case, 20 x 3 folds, in place of the three windows of case number.
- Along the case-number order, the only time order the data has, survival is flat (62.2% against 62.8%, Fisher p = 1.0), and a horse trained on its history scores like one trained on as many random horses (TabPFN 3.5, harmonised recording: +0.020 log loss, 95% interval -0.034 to +0.080, 60 horses).
- So the relation does not move with time (a stationary relation) and random horses stand for later admissions; grouping by `case_number` keeps the 10 return visits of 9 horses on the side of their first visit.
- `Temporal` removed, `case_number` is split metadata only (20 features); `required_split` `Grouped (NON-IID)`, tag `Non-IID (Grouped)` in place of `Non-IID (Temporal)`.

**Assessment (AI, 2026-11-12):** applied in `dataset.py` (`_clean`, the recording note, `changes`, the split); `dataset check` 0 errors, 0 warnings. Runs of 2026-11-12 (untuned LightGBM, logistic regression, TabPFN 3.5): random 3 x 20 against 3 x 57 windows, and single horses 200-259 trained on their history against as many random horses; no time dependence beyond the recording measurable (TabPFN, harmonised: +0.020 log loss [-0.034, +0.080]).

## Reference

McLeish, M. & Cecile, M. (1989). Horse Colic [Dataset]. UCI Machine Learning Repository. https://doi.org/10.24432/C58W23
