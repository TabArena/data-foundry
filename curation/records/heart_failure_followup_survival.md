---
unique_name: heart_failure_followup_survival
name: Heart Failure Clinical Records
checked_by:
- Lennart
- Andrej
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

CC (2026-10-21, Andrej): The rows are 299 heart-failure patients (Faisalabad, 2015); the source label is death during a follow-up of 4-285 days that differs by patient. Keep, with the label and three lab columns fixed in `dataset.py` (not built).
- **Problems found:**
  - Creatinine filled with the outcome's group mean: serum creatinine (a blood marker of kidney function) is exactly 1.18 in 11 rows, all survivors, and 1.83 in 8 rows, all deaths, the two group means in Ahmad et al. 2017, Table 1. Models use it: TabPFN 3.5 log loss on these rows is 0.27, against 0.41 once the values are neutralised.
  - Undocumented mean filling: creatine phosphokinase (CPK, a muscle enzyme) is the column mean 582 in 47 rows, and platelets the column mean 263358.03 in 25 rows. Neither paper mentions missing values.
  - "Survived" often meant "not followed long enough": 55 of the 203 survivors were followed for under 100 days. A Kaplan-Meier estimate (the standard survival curve) puts about 31 deaths within 285 days among them.
  - Minor: anaemia among deaths is 46 in the file, 54 in the paper.
- **Fixed:**
  - The target is death within 60 days; the 8 survivors followed less than 60 days are dropped (291 rows, 54 deaths). 30 days would leave 35 deaths, 90 days would drop 45 survivors.
  - The 91 filled-in values are missing again.
  - The citation is Ahmad et al. 2017, which published the data, instead of the later re-analysis by Chicco & Jurman 2020.
  - The fixed task keeps its signal: TabPFN 3.5 ROC AUC about 0.72, logistic regression about 0.68 (20 x 3 splits).
- Reference: Ahmad T, Munir A, Bhatti SH, Aftab M, Raza MA. Survival analysis of heart failure patients: A case study. PLoS One. 2017;12(7):e0181001. doi:10.1371/journal.pone.0181001

## Reference

@article{ahmad2017survival,
  title={Survival analysis of heart failure patients: A case study},
  author={Ahmad, Tanvir and Munir, Assia and Bhatti, Sajjad Haider and Aftab, Muhammad and Raza, Muhammad Ali},
  journal={PLOS ONE},
  volume={12},
  number={7},
  pages={e0181001},
  year={2017},
  publisher={Public Library of Science},
  doi={10.1371/journal.pone.0181001}
}
