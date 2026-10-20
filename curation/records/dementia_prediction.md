---
unique_name: dementia_prediction
name: Dementia Prediction Dataset
checked_by:
- Lennart
- Andrej
data_foundry_status:
- 'DF: Yes'
- BeyondArena
suggestion: Yes (Disagreement)
decision_markers:
- Wrong Domain / Source Modality
- Time-series (Classification)
- Not Representative
- Selection Bias
tags:
- Tiny Data
- Non-IID (Grouped)
collections:
- New (BeyondArena)
original_source: Other
year: '2010'
domain: medical & healthcare
required_split:
- Grouped (NON-IID)
problem_type: Multiclass Classification
original_data_state: One Table
source_links:
- https://www.kaggle.com/datasets/shashwatwork/dementia-prediction-dataset/data
- https://data.mendeley.com/datasets/tsy6rbc5d4/1
notebook_path: datasets/beyond_iid/grouped/dementia_prediction/dementia_prediction.ipynb
v2_path: datasets/_dev/tabarena-v0pt2/dementia_prediction/dataset.py
source_row: 4
type_adapter_id: curation-record-v1
---

## Comments

need to figure out how to use the data, source seems likely image data?

the version of this dataset is created from the study and taken from another one

Grouped data

AT: No objection, but we need to quickly talk about how we proceed with medical image data

CC (2026-10-19, Andrej): Keep; no reason to exclude after review. Fixed licence and notes in `dataset.py`.

- **MMSE dominates** (a 30-point cognitive test; log loss 0.62 alone vs 0.94 prior), but all features do better (0.59). Not circular: the dementia rating ignores test scores (Marcus et al. 2010).
- **Licence:** `CC BY NC 3.0` was a Mendeley re-uploader's; now the OASIS terms (non-commercial, academic only).
- **Volunteer cohort, few borderline cases:** documented; the split by person stays.
- **Missing SES/MMSE only in demented visits** (21 rows): small effect, documented, kept.

Marcus DS, Fotenos AF, Csernansky JG, Morris JC, Buckner RL. Open Access Series of Imaging Studies: longitudinal MRI data in nondemented and demented older adults. J Cogn Neurosci. 2010;22(12):2677-2684. doi:10.1162/jocn.2009.21407

## Reference

Rel source paper: Open Access Series of Imaging Studies: Longitudinal MRI Data in Nondemented and Demented Older Adults  https://direct.mit.edu/jocn/article/22/12/2677/4983/Open-Access-Series-of-Imaging-Studies-Longitudinal
