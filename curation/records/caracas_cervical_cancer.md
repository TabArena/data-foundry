---
unique_name: caracas_cervical_cancer
name: Caracas Cervical Cancer
checked_by:
- Lennart
data_foundry_status:
- WIP (DF)
claimed_by: Lennart
suggestion: 'Yes'
tags:
- New IID
collections:
- New (BeyondArena)
- TabSTAR
original_source: UCI
year: '2017'
domain: medical & healthcare
required_split:
- Random (IID)
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://doi.org/10.24432/C5Z310
- https://www.openml.org/search?type=data&id=46592
- http://vcmi.inescporto.pt/reproducible research/ibpria2017/CervicalCancer/
v2_path: datasets/_dev/tabarena-v0pt2/caracas_cervical_cancer/dataset.py
source_row: 688
type_adapter_id: curation-record-v1
---

## Comments

Some features are multi-categoricals as one-hot encoding. Might want to reverse this.

Has 4 target variables, unsure which one to use. Likely want to use Biopsy as the real ground truth (not just an indicator).

**Assessment (AI, 2026-10-07):** Target: Biopsy. The creators predict it "where only behavioral and demographic information is observable" (Fernandes et al., PeerJ Comput. Sci. 2018, Results), so Hinselmann, Schiller and Citology are dropped as results of the same work-up (Schiller alone: ROC AUC 0.92). The STD and Dx columns are multi-label (43 of 740 patients have 2-4 STD types) and stay binary flags. The 108 patients who skipped the contraceptive question are dropped: they have no positive biopsy, Hinselmann or Schiller result where 8, 5 and 11 are expected, although their answers show no lower risk. Their results look unrecorded. All 55 positives stay. The folder ships the biopsy only; the Multi-target tag stays.

CC (2026-10-15, Lennart): No `Multi-target` tag: the four test results come from one work-up and the dataset predicts the biopsy alone (review page, issue 5).

**Assessment (AI, 2026-10-15):** The STD flags are one questionnaire question each and multi-label (9 patients have two or three types; `std_condylomatosis` is the parent of two subtypes, which `stds_number` counts twice), so they stay yes/no categories rather than one combined category. Impossible answers become missing (2 first intercourses after the current age, 2 STD diagnoses longer ago than the patient's age); the other contradictions (5 `dx_*` flags with `dx` 0, 7 STDs with no diagnosis counted) are not impossible and stay.

## Reference

@inproceedings{fernandes2017transfer,
  title={Transfer learning with partial observability applied to cervical cancer screening},
  author={Fernandes, Kelwin and Cardoso, Jaime S and Fernandes, Jessica},
  booktitle={Iberian conference on pattern recognition and image analysis},
  pages={243--250},
  year={2017},
  organization={Springer}
}
