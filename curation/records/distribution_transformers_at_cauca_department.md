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
- 'download link (down for me): https://data.mendeley.com/datasets/yzyj46xpmy/4'
- 'data proof: https://ieee-dataport.org/documents/data-driven-predictive-maintenance-distribution-transformers'
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

**Assessment (AI, 2026-10-20):** re-check by the review panel; recommend shipping after the changes now in the definition (the curator has the call). Facts: the files hold 15,873 rows (15,869 is the paper's count, which the authors' MATLAB table also has); the attributes are one static inventory, identical in the 2019 and 2020 files, not yearly averages; the one typo the definition corrects is the 2020 file's mounting category `POLE WITH ANTI-FRAU NET`, not a target label. LEAK-10 (Must): power_kva changed on replacement (none of the 163 self-protected first burns of 2020 is 5 kVA, against 9% of the other 277), so power_kva and installation_type are dropped and the energy not supplied is kept only as outage hours (EENS / (1.08 x kVA)); lightning densities of 0.0 (one area, 487 rows) are set to missing. LightGBM ROC AUC is now 0.639 on the shipped random folds and 0.648 trained on 2019 and tested on 2020. Open for the curator: an amendment of LEAK-10 to keep the two columns, and the shared split amendment for tasks with too few periods. Priority 2: gap -, use case - (fit approximate: forced random split, label coverage of 2020 not stated), source + (Mendeley v4 with the Data in Brief article), shape + (15,873 units, 12 features), risk - (the source's dropped zeros in lv_network_km cannot be repaired row by row).

CC (2026-10-21, Lennart): LEAK-10 stays as written (option (a) of the cross-dataset item "Amend LEAK-10 for a looked-up attribute that changed for an unknown subset of positives?"): power_kva and installation_type stay dropped, no definition change.

CC (2026-10-21, Lennart): option (a) of the cross-dataset item on tasks with too few periods: the closest regime that keeps the rows, tagged as forced from temporal, with the cost measured against the valid windows (SPLIT-8 amended).

**Assessment (AI, 2026-10-21):** keeps one year, IID, `ForcedIIDFromTemporal`; the notes cite the amended SPLIT-8. Cost: LightGBM ROC AUC 0.648 trained on 2019 and tested on 2020 against 0.639 on the random folds. REVIEW.md issue 2 settled.

CC (2026-10-21, Lennart): "yes we should have one clear way to treat 0/1 flags": every 0/1 flag (a feature holding only 0 and 1, plus missing values; booleans too) is categorical (CLEAN-14, amended). Typed categorical here: urban, keraunic_criticality, removable_connectors, overhead_lv_network, circuit_end.

**Assessment (AI, 2026-10-21):** Metric declared under MET-1..13: fallback roc_auc — a data article with no prediction benchmark or score.

## Reference

[1] L. Alvarez, Predictive Maintenance of Distributions. Transformers. Case Study: Department of Cauca (Colombia), first ed., Our Knowledge Publishing, 2021. ISBN 978-620-3-93390-1
https://www.researchgate.net/publication/355264319_Dataset_of_Distribution_Transformers_for_Predictive_Maintenance
