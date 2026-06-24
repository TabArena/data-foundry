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
type_adapter_id: curation-record-v1
---

# MIC

## Comments

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
