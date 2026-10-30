---
unique_name: horse_colic_survival
name: horse_colic_*
checked_by:
- Lennart
data_foundry_status:
- 'DF: Yes'
- BeyondArena
suggestion: 'Yes'
decision_markers:
- Outdated
tags:
- Tiny Data
collections:
- TabArena Reject
- TabSTAR
original_source: UCI
year: '1989'
domain: biology & life sciences
required_split:
- Random (IID)
problem_type: TBD
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

## Reference

?
