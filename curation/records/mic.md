---
unique_name: mic
name: MIC
checked_by:
- Lennart
- Andrej
data_foundry_status:
- 'DF: Yes'
- TabArena (v0.1)
- BeyondArena
suggestion: 'Yes'
original_source: UCI
year: '2020'
required_split:
- Random (IID)
source_links:
- https://www.openml.org/search?type=data&id=45648
- https://doi.org/10.24432/C53P5M
notebook_path: datasets/beyond_iid/old_iid/mic/mic.ipynb
v2_path: datasets/_dev/tabarena-v0pt2/mic/dataset.py
type_adapter_id: curation-record-v1
---

## Comments

CC (2026-09-30, Lennart): **Leak fixed: predict at admission, dropping the 9 ICU day-1..3 columns.** The dataset description (Golovenkin et al., Leicester data 2020, doi 10.25392/leicester.data.12045261.v3, "Problems to solve") defines four prediction times; at admission all inputs except columns 93-95 and 100-105 (R_AB_1..3_n, NA_R_1..3_n, NOT_NA_1..3_n) may be used, at the end of day 3 all of them. The notebook used day 3, but LET_IS ("Lethal outcome (cause)", column 124) counts any in-hospital death, so a patient who died before day 2 or 3 has no records for those days: 126 of the 138 rows missing a day-3 field died (91%, base rate 16%); 74 of the 110 cardiogenic-shock deaths miss day-2 and day-3 fields, against 10 of 1,428 survivors. Golovenkin et al. 2020 (GigaScience 9:giaa128) list these variables as "in the ICU in the second/third day of the hospital period" (Table 1) and refer to the Leicester description for the task. Dropping them: death AUC 0.93 -> 0.91 (leak audit 2026-09-24). ZSN_A (chronic heart failure, anamnesis) is missing for 54 rows, 93% of them deaths (flag AUC 0.59): an admission-time field, kept.

Clean canonical entry bootstrapped from the TabArena curation workbook ('Tabular' row). Shipped in TabArena (v0.1) / BeyondArena.

TabArena curation verdict: Tabular.

Myocardial infarction complications Database - Almost no description or source info on OpenML. Likely from: https://scholar.google.de/citations?view_op=view_citation&hl=de&user=Gms_lDcAAAAJ&citation_for_view=Gms_lDcAAAAJ:olpn-zPbct0C;

Seems to be a preprocessed version from 10.24432/C53P5M UCI
Contains EEG data? Several outputs

Hospital mortality prediction at different time points with details which (time-invariant) features are allowed. Relevant task.

Potential issue: EEG data?

Lennart: Maybe a valid predictive task but might contain non-tabular source data

Andrej: use UCI versionNeeds some preprocessing and is rather small, but otherwise is a good dataset.

## Reference

Trajectories, bifurcations, and pseudo-time in large clinical datasets: applications to myocardial infarction and diabetes data
By S. E. Golovenkin, Jonathan Bac, A. Chervov, E. M. Mirkes, Y. Orlova, E. Barillot, A. Gorban, A. Zinovyev. 2020

Published in GigaScience
