---
unique_name: seismic_bumps
name: seismic-bumps
checked_by:
- Lennart
- Andrej
data_foundry_status:
- 'DF: Yes'
- TabArena (v0.1)
- BeyondArena
suggestion: No (Retired)
decision_markers:
- Too Small
tags:
- Non-IID (Temporal)
original_source: UCI
year: '2013'
required_split:
- Temporal (NON-IID)
source_links:
- https://doi.org/10.24432/C5W902
notebook_path: datasets/beyond_iid/old_iid/seismic_bumps/seismic_bumps.ipynb
type_adapter_id: curation-record-v1
---

## Comments

CC (2026-09-30, Lennart): **Retired: the honest split is temporal, and as a temporal task the data is too small.** Each row is one 8-hour shift of one longwall in the Wesola coal mine and the label is a bump above 10^4 J in the next shift (ARFF header; Sikora & Wrobel 2010, Archives of Mining Sciences 55(1), Sec. 2.1: data "aggregated in the hourly and shift periods", "prediction horizon amounted to one ... shift"; Sec. 4.1: "consecutive shifts"). The file is in shift order: row t's label equals "row t+1 recorded a bump >= 10^4 J" in 2,583 of 2,583 consecutive pairs (0.877 when shuffled), and the sequence is non-stationary (positive rate per tenth of the file 0.04, 0.28, 0.13, 0.01, ...). The shipped IID shuffle lets training see every period (ROC AUC 0.75 IID vs about 0.6 forward; leak audit 2026-09-24). Following our temporal convention (as many splits as an IID task of this size, 10 x 3 = 30, never less than 50% of the data for training), all test windows come from the newest half, which holds only 49 of the 170 positives: 30 windows of 43 shifts have 0-5 positives each (6 have none). Even 3 or 2 windows (14-26 positives each) give ROC AUC intervals of about +-0.1 to +-0.14 per window. The UCI file (2,584 shifts, threshold 10^4 J) is a later export than the paper's (1,961 shifts from longwalls SC508 and SC503, threshold 5*10^5 J). TabArena v0.1 dataset.

Clean canonical entry bootstrapped from the TabArena curation workbook ('Tabular' row). Shipped in TabArena (v0.1) / BeyondArena.

TabArena curation verdict: Temporal Tabular.

forecasting seismic bumps in a coal mine from longwalls in a Polish mine; used for clusterting. 

Description highlights practical importance of the taskl. each row contains a summary statement about seismic activity in the rock mass within one shift (8 hours). If decision 
attribute has the value 1, then in the next shift any seismic bump with an energy higher than 10^4 J was 
registered. Hence, the task might be time-invariant.

Potential issue: Temporal

Lennart: temporal data

Andrej: unsure whether the features are extracted from time-series. even if yes, they are extracted from 8h windows and I think this is rather a tabular task. BUT: Temporal correlations need to be investigated. unsure whether the extracted features are time-invariant

## Reference

See some of the papers on UCI
