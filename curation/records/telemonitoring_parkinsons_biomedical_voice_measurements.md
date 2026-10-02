---
unique_name: telemonitoring_parkinsons_biomedical_voice_measurements
name: Parkinsons
checked_by:
- Lennart
data_foundry_status:
- 'DF: Yes'
- BeyondArena
suggestion: No (Retired)
decision_markers:
- Wrong Domain / Source Modality
- No Good Target  / Scientific Discovery
tags:
- Tiny Data
- Non-IID (Grouped)
collections:
- TabArena Reject
original_source: UCI
year: '2009'
domain: medical & healthcare
required_split:
- Grouped (NON-IID)
problem_type: Regression
original_data_state: One Table
source_links:
- https://doi.org/10.24432/C5ZS3N
notebook_path: datasets/beyond_iid/grouped/telemonitoring_parkinsons_biomedical_voice_measurements/telemonitoring_parkinsons_biomedical_voice_measurements.ipynb
source_row: 638
type_adapter_id: curation-record-v1
---

## Comments

Same source as Parkinsons and saved in the same repo under telemonitoring/, but here we only have data from cases that already have Parkinson's. The task is to predict the progression of a patient at the next time interval (so non-iid grouped), that is we have a different target per time point per patient. 

It was used to monitor the progression. 

Moreover, it was technically a correlation analysis / for scientific discovery. We keep it as we can clearly frame this as a task for predicting future UPDRS scores

AT: It seems as if repeated observations per time stamp are present. We might need to groupby and summarize them, because the target is unique. That way we would end up with just 124 samples -> real problem but solve in the future?

CC (2026-10-02, Lennart): Retired from TabArena v0.2: the voice features carry almost no information about UPDRS across subjects. 88% of the target's variance lies between the 42 subjects (sd 10.5), so a held-out subject's level has to come from its voice, and the features track it weakly (Spearman 0.43 between a subject's mean NHR and its mean UPDRS; 5 of the 18 features at p < 0.05, against 0.9 expected by chance). With about 28 training subjects per fold, flexible models learn subject identity: on the grouped splits the best result is a ridge with alpha 1000 at RMSE 10.98 against 11.19 for the training mean (60 splits), and on BeyondArena the best model (CatBoost, 11.09) is no better than the mean (about 11.00). Recast as tracking a known patient (the source's setting: the baseline visit in training, the 3- and 6-month visits predicted), the baseline score does the work: carrying it forward gives RMSE 6.98, adding the training subjects' mean drift 6.48, a ridge on voice plus baseline 6.33 and LightGBM 7.32. In both framings the benchmark would rank models by how little they lose to a constant, not by what they learn from the data. The UPDRS labels between the clinic visits are interpolated (Tsanas et al. 2010), which is why the v2 definition kept only the test days nearest the three visits.

## Reference

If you use this dataset, please cite the following paper:
A Tsanas, MA Little, PE McSharry, LO Ramig (2009)
'Accurate telemonitoring of Parkinson.s disease progression by non-invasive 
speech tests',
IEEE Transactions on Biomedical Engineering (to appear).
