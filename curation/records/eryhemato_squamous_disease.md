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
- https://doi.org/10.1016/S0933-3657(98)00028-1
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

CC (2026-10-20, Andrej): Audit of the clinical-only version: no reason to exclude it or to change the splits or metric (TabPFN 3.5 vs logistic regression on the 60 shipped splits).
- Two classes follow from one sign each: polygonal papules (flat, angular bumps) or mouth involvement mark all 72 lichen planus patients and no one else, and follicular papules (bumps around hair follicles) mark pityriasis rubra pilaris. Not circular, since the label is the biopsy diagnosis and these are signs seen before it, and the model ranking is the same on the three hard classes alone (TabPFN better on 55/60 folds).
- The patients look selected: 93% of lichen planus patients have mouth involvement (56% of 91 biopsy-confirmed patients in Samreen A, Luqman N, Asgher R, Khalid M, Shaheen JA. Frequency of oral involvement in cutaneous lichen planus patients. J Pak Assoc Dermatol. 2021;31(3):454-458. doi:10.66344/jpad.v31i3.1817), and all 20 pityriasis rubra pilaris patients are aged 7 to 22, though the disease is most common in adults. This makes two classes easier than in a clinic but does not affect the model comparison.

Done (2026-10-20): `fit_reason` in `dataset.py` names the selected cases.

## Reference

@article{guvenir1998learning,
  title={Learning differential diagnosis of erythemato-squamous diseases using voting feature intervals},
  author={G{\"u}venir, H Altay and Demir{\"o}z, G{\"u}l{\c{s}}en and Ilter, Nilsel},
  journal={Artificial intelligence in medicine},
  volume={13},
  number={3},
  pages={147--165},
  year={1998},
  publisher={Elsevier},
  doi={10.1016/S0933-3657(98)00028-1}
}
