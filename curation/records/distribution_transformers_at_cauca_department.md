---
unique_name: distribution_transformers_at_cauca_department
name: Distribution Transformers at Cauca Department
checked_by:
- Lennart
data_foundry_status:
- WIP (DF)
claimed_by: Lennart
suggestion: 'Yes'
priority: 2
tags:
- New IID
collections:
- New (BeyondArena)
original_source: Other
required_split:
- Random (IID)
problem_type: Binary Classification
source_links:
- 'data proof: https://ieee-dataport.org/documents/data-driven-predictive-maintenance-distribution-transformers'
- 'download link (down for me): https://data.mendeley.com/datasets/yzyj46xpmy/4'
v2_path: datasets/_dev/tabarena-v0pt2/distribution_transformers_at_cauca_department/dataset.py
source_row: 741
type_adapter_id: curation-record-v1
---

## Comments

paper: https://www.researchgate.net/publication/355264319_Dataset_of_Distribution_Transformers_for_Predictive_Maintenance

used SVMs

No time stamp, might be able to do only one split. Unclear if it would have a temporal impact, data seems very time-independent. Features are averages across year

15,869 transformers -> might have grouped/temporal leakage if we split and take data from both years at once? need to check. For just one year, it is IID, for two years it is not.

**Assessment (AI, 2026-10-07):** Source: Mendeley Data v4 (doi:10.17632/yzyj46xpmy.4, public API) with the Data in Brief article (doi:10.1016/j.dib.2021.107454); the IEEE DataPort link is a processed 2025 copy. Both yearly files hold the same 15,873 transformers and one inventory, taken after the 2020 burns. Added as IID on 2020 (629 burned): two years cannot give three temporal windows. SELF-PROTECTION (an internal switch, item C) behaves in the data as a mark of replacement units: self-protected units without an earlier burn burned at 42% in 2019 and 2020, those with one at 13% and 9%. It is dropped. burn_rate counts only earlier years. Open: power_kva may show replacement units.

**Assessment (AI, 2026-10-20):** priority 2 for the review of the added dataset: gap -, use case -, source +, shape +, risk - (Issue 4: power_kva/installation_type may describe replacement units (post-outcome leak); issue 3 unrepairable source bug). Real utility predictive-maintenance task with a documented source, but the post-outcome inventory makes leaks hard to rule out.

## Reference

[1] L. Alvarez, Predictive Maintenance of Distributions. Transformers. Case Study: Department of Cauca (Colombia), first ed., Our Knowledge Publishing, 2021. ISBN 978-620-3-93390-1
https://www.researchgate.net/publication/355264319_Dataset_of_Distribution_Transformers_for_Predictive_Maintenance
