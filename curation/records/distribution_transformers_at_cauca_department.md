---
unique_name: distribution_transformers_at_cauca_department
name: Distribution Transformers at Cauca Department
checked_by:
- Lennart
suggestion: 'Yes'
tags:
- Non-IID (Temporal)
- New IID
collections:
- New (BeyondArena)
source_links:
- 'data proof: https://ieee-dataport.org/documents/data-driven-predictive-maintenance-distribution-transformers'
- 'download link (down for me): https://data.mendeley.com/datasets/yzyj46xpmy/4'
source_row: 741
type_adapter_id: curation-record-v1
---

# Distribution Transformers at Cauca Department

## Comments

paper: https://www.researchgate.net/publication/355264319_Dataset_of_Distribution_Transformers_for_Predictive_Maintenance

used svms

No time stamp, might be able to do only one split. Unclear if it would have a temporal impact, data seems very time-independent. Features are average across year

15.869 transformers -> might have grouped/temporal leakage if we split take data from both years at once? need to check. For just one year, it is IID, for two years it is not.

## Reference

[1] L. Alvarez, Predictive Maintenance of Distributions. Transformers. Case Study: Department of Cauca (Colombia), first ed., Our Knowledge Publishing, 2021. ISBN 978-620-3-93390-1
https://www.researchgate.net/publication/355264319_Dataset_of_Distribution_Transformers_for_Predictive_Maintenance
