---
unique_name: hepatitis_survival_prediction
name: hepatitis
checked_by:
- Lennart
- Andrej
data_foundry_status:
- 'DF: Yes'
- BeyondArena
suggestion: No (Retired)
decision_markers:
- Outdated
tags:
- Tiny Data
collections:
- TabArena Reject
original_source: UCI
year: '1988'
domain: medical & healthcare
required_split:
- Random (IID)
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://github.com/EpistasisLab/pmlb/blob/master/datasets/hepatitis/metadata.yaml
- https://doi.org/10.24432/C5Q59J
- https://www.kaggle.com/datasets/abdelazizsami/hepatitis
notebook_path: datasets/beyond_iid/new_iid/hepatitis_survival_prediction/hepatitis_survival_prediction.ipynb
source_row: 760
type_adapter_id: curation-record-v1
---

## Comments

Already preprocessed data but otherwise looks like a good task, need to check group and cost files but would add!

**Assessment (AI, 2026-10-21):** Metric declared under MET-1..13: fallback roc_auc — Efron & Gong 1981/1986 study how to estimate the error rate of Gregory's logistic rule on these 155 patients: a statistics-methods paper, not a decision; 32 deaths, so accuracy is coarse. Original rejected: error rate. roc_auc is the binary fallback.

CC (2026-10-21, Lennart): the metric is the roc_auc fallback; Efron & Gong's error rate is the object of a resampling study on 155 patients, not the task's metric.

CC (2026-10-21, Andrej): The rows are 155 patients with hepatitis (liver inflammation) from Stanford Medical School, collected before 1982; the label is death from the disease. I disagree with keeping it.
- **The UCI file is an altered copy of the original:** Efron & Gong print the original values of the last 11 patients (UCI rows 145-155). Histology is missing for 4 of them (3 died), but UCI codes all 4 as `2`; three lab values differ (e.g. SGOT, a liver enzyme, 193 vs 173), and the paper counts 33 deaths against 32 in UCI. The other 144 rows cannot be checked.
- Reference: Efron B, Gong G. A leisurely look at the bootstrap, the jackknife, and cross-validation. Am Stat. 1983;37(1):36-48. doi:10.1080/00031305.1983.10483087
**Assessment (AI, 2026-10-31):** better data: the data-scouting run of 2026-10-30/31 found better data for the same task: `optn_liver_waitlist_90day_mortality` (TBD -> Yes, priority 3). Each is screened in its own record; this record's verdict stays the curator's.

CC (2026-11-01, Lennart): the target rule (CLEAN-25) and the cut-end rule (CLEAN-14): the target ships as No/Yes, Yes the event (1 means the patient died (UCI: 1 DIE, 2 LIVE)).

## Reference

@article{efron1983leisurely,
  title={A leisurely look at the bootstrap, the jackknife, and cross-validation},
  author={Efron, Bradley and Gong, Gail},
  journal={The American Statistician},
  volume={37},
  number={1},
  pages={36--48},
  year={1983},
  publisher={Taylor \& Francis},
  doi={10.1080/00031305.1983.10483087}
}
