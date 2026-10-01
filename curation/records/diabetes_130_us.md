---
unique_name: diabetes_130_us
name: Diabetes130US
checked_by:
- Lennart
- Andrej
data_foundry_status:
- 'DF: Yes'
- TabArena (v0.1)
- BeyondArena
suggestion: 'Yes'
original_source: UCI
year: '2014'
required_split:
- Random (IID)
problem_type: Multiclass Classification
source_links:
- https://www.openml.org/search?type=data&id=4541
- https://doi.org/10.24432/C5230J
notebook_path: datasets/beyond_iid/old_iid/diabetes_130_us/diabetes_130_us.ipynb
v2_path: datasets/_dev/tabarena-v0pt2/diabetes_130_us/dataset.py
type_adapter_id: curation-record-v1
---

## Comments

CC (2026-09-30, Lennart): **Cleaned to the paper's cohort: first encounter per patient, no deaths or hospice discharges.** Strack et al. 2014 (BioMed Research International, 781670), Sec. 2.3: "we considered only the first encounter for each patient as the primary admission" and "we removed all encounters that resulted in either discharge to a hospice or patient death, to avoid biasing our analysis", leaving 69,984 encounters. Our definition already kept the first encounter per patient (each patient's encounters appear in encounter_id order in the raw file; the sort is now explicit) but kept 1,084 "Expired" encounters (all "No": the dead cannot be readmitted; pure-value scan 2026-09-30) and 461 hospice discharges (16 readmitted). Now: discharge codes 11, 13, 14, 19, 20, 21 removed; 69,973 rows (paper: 69,984). Also "?" and "NULL" are now missing values.

Clean canonical entry bootstrapped from the TabArena curation workbook ('Tabular' row). Shipped in TabArena (v0.1) / BeyondArena.

TabArena curation verdict: Tabular.

Not sure if date is available, encounter_id might be sorted by date. Generally an interesting tabular data task. Same patients are in the dataset - need to account for that with preprocessing. Task has temporal nature, but features should be time invariant

Lennart: After preprocessing (handling duplicated patiens, handling one-hot encoded categories, ...)

Andrej: Requires proper preprocessing and handling of duplicate patients before inclusion

## Reference

Beata Strack, Jonathan P. DeShazo, Chris Gennings, Juan L. Olmo, Sebastian Ventura, Krzysztof J. Cios, and John N. Clore, “ Impact of HbA1c Measurement on Hospital Readmission Rates: Analysis of 70,000 Clinical Database Patient Records,” BioMed Research International, vol. 2014, Article ID 781670, 11 pages, 2014.
