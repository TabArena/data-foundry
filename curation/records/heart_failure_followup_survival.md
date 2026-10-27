---
unique_name: heart_failure_followup_survival
name: Heart Failure Clinical Records
checked_by:
- Lennart
data_foundry_status:
- 'DF: Yes'
- BeyondArena
suggestion: 'Yes'
tags:
- Tiny Data
collections:
- New (BeyondArena)
original_source: Other
year: '2017'
domain: medical & healthcare
required_split:
- Random (IID)
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://doi.org/10.24432/C5Z89R
notebook_path: datasets/beyond_iid/new_iid/heart_failure_followup_survival/heart_failure_followup_survival.ipynb
v2_path: datasets/_dev/tabarena-v0pt2/heart_failure_followup_survival/dataset.py
source_row: 766
type_adapter_id: curation-record-v1
---

## Comments

CC (2026-09-30, Lennart): **Leak fixed: dropped `time` (follow-up days), which is only known after the outcome.** Chicco & Jurman 2020 (BMC Med Inform Decis Mak 20:16), Table 1: "Time | Follow-up period | Days | [4,...,285]" and "death event | If the patient died during the follow-up period"; the source study (Ahmad et al. 2017, PLOS ONE 12:e0181001) is a survival analysis with "dead and censored patients at the end of follow up period". Follow-up ends at death or censoring, so early deaths get short times (Chicco & Jurman, Fig. 4: 88.6% of month-0 patients died). Alone it gives ROC AUC 0.84; LightGBM 0.90 -> 0.75 without it (leak audit 2026-09-24). The label is still "died within a patient-specific follow-up of 4-285 days", so some censored patients may have died later.

Looks good

**Assessment (AI, 2026-10-14):** whether follow-up ended on one date for all patients cannot be determined: Ahmad et al. 2017 and Chicco & Jurman 2020 do not say, and neither file has dates. The censored follow-ups (12 to 285 days) fit a common end around mid-January 2016 but do not prove it. Each patient's window starts at their own admission, so the task stays as it is (Lennart's instruction).

**Assessment (AI, 2026-10-21):** Metric declared under MET-1..13: fallback roc_auc — Ahmad et al. 2017 (first publication) score a Cox model by time-dependent ROC AUC, which needs the follow-up time we drop (leak); Chicco & Jurman 2020 (the binary task we ship) rank by MCC at threshold 0.5, a default threshold, not a decision (MET-6). roc_auc is the binary fallback.

## Reference

@article{chicco2020machine,
  title={Machine learning can predict survival of patients with heart failure from serum creatinine and ejection fraction alone},
  author={Chicco, Davide and Jurman, Giuseppe},
  journal={BMC medical informatics and decision making},
  volume={20},
  number={1},
  pages={16},
  year={2020},
  publisher={Springer}
}
