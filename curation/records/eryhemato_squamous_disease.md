---
unique_name: eryhemato_squamous_disease
name: dermatology
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
collections:
- TabArena Reject
original_source: UCI
year: '1998'
domain: medical & healthcare
required_split:
- Random (IID)
problem_type: Multiclass Classification
original_data_state: One Table
source_links:
- https://github.com/EpistasisLab/pmlb/blob/master/datasets/dermatology/metadata.yaml
- https://doi.org/10.24432/C5FK5P
notebook_path: datasets/beyond_iid/new_iid/eryhemato_squamous_disease/eryhemato_squamous_disease.ipynb
v2_path: datasets/_dev/tabarena-v0pt2/eryhemato_squamous_disease/dataset.py
source_row: 753
type_adapter_id: curation-record-v1
---

## Comments

Looks like an old but reasonable task

If we use the Histopathological, this means we assume the patient may or may not be given a biopsy

CC (2026-10-06, Lennart): Changed to the clinical features only after the task-probe review (flag `solved`). The source evaluates in two steps: "Patients were first evaluated clinically with 12 features. Afterwards, skin samples were taken for the evaluation of 22 histopathological features." With all 34 features the task is close to solved (logistic regression: macro ROC AUC 0.999, 97% accuracy on the 60 shipped splits; BeyondArena's best log loss 0.044), so v0.2 asks for the diagnosis before the biopsy: the 11 clinical findings, family history and age. Same six classes. On the shipped splits this gives macro ROC AUC 0.98 and 87% accuracy for logistic regression (log-loss skill +0.76; random forest +0.72, LightGBM +0.65), with seborrheic dermatitis, pityriasis rosea and chronic dermatitis as the hard cases, which is the differential the source describes. No probe flags on the rebuilt container. One pair of patients shares all clinical findings with different diagnoses.

**Assessment (AI, 2026-10-14):** The count above is off by one: the clinical features are 10 findings graded 0 to 3 (erythema to scalp involvement), family history and age, the source's 12 clinical features (UCI variable list); the definition keeps exactly these.

**Assessment (AI, 2026-10-21):** Metric declared under MET-1..13: fallback log_loss — Guevenir et al. 1998 report cross-validated accuracy of VFI5 without costs between the six diagnoses, and we use the 12 clinical features only (MET-6).

**Assessment (AI, 2026-10-27):** evidence for the Selection Bias marker of PR #16, checked on dermatology.data: 67 of the 72 lichen planus patients (93%) have oral mucosal involvement and none of the other 294 patients do, against 19% to 63% in clinic series of cutaneous lichen planus (56% of 91 biopsy-confirmed patients, https://jpad.com.pk/index.php/jpad/article/view/1817; 19% of 131, https://diposit.ub.edu/dspace/handle/2445/171919). All 20 pityriasis rubra pilaris patients are aged 7 to 22. The rows look like typical cases of each disease rather than a clinic's patients. The definition's fit_reason does not name this yet.

CC (2026-10-27, Lennart): fit approximate (was direct): a dermatologist's lichen planus patients do not show the selection of these rows, so it is a known gap (USE-8, amended on the review of PR #16); the Selection Bias marker stays.

**Assessment (AI, 2026-10-30):** Dtype review (branch ordinal-and-censored-levels; the column decisions with their codebook evidence are on the review board): 10 ordinal scales typed as ordered categories in the codebook's order (CLEAN-14, amended): `erythema`, `scaling`, `definite borders`, `itching`, `koebner phenomenon`, `polygonal papules`, `follicular papules`, `oral mucosal involvement`, `knee and elbow involvement`, `scalp involvement` (the README lists their levels).

## Reference

@article{guvenir1998learning,
  title={Learning differential diagnosis of erythemato-squamous diseases using voting feature intervals},
  author={G{\"u}venir, H Altay and Demir{\"o}z, G{\"u}l{\c{s}}en and Ilter, Nilsel},
  journal={Artificial intelligence in medicine},
  volume={13},
  number={3},
  pages={147--165},
  year={1998},
  publisher={Elsevier}
}
