---
unique_name: tadpole
name: tadpole
checked_by:
- Andrej
suggestion: TBD -> 2nd Tier
decision_markers:
- Needs extensive data wrangling
tags:
- New IID
collections:
- New (BeyondArena)
original_source: Website
year: '2019'
domain: medical & healthcare
required_split:
- Random (IID)
problem_type: TBD
original_data_state: Other
source_links:
- https://tadpole.grand-challenge.org/Data/
source_row: 525
type_adapter_id: curation-record-v1
---

## Comments

Multimodal data, but the main challenge combines extracted features from multiple clinical modalities into one tabular dataset. If we could get the data and invest some time in understanding the task, we would likely obtain an awesome dataset. But there are license concerns, access is not easy and it might be hard to really do everything right with this complex data. Challenge has multiple tasks

Maybe we could use the data from: https://github.com/ecabanerof/TadpoleChallengeAdapt

Could also ask authors of this study: https://arxiv.org/pdf/2508.17649

**Assessment (AI, 2026-10-31):** better data: the data-scouting run of 2026-10-30/31 found better data for the same task: `nacc_uds_dementia_conversion` (TBD -> Yes, priority 3). Each is screened in its own record; this record's verdict stays the curator's.

## Reference

Marinescu, R. V., Oxtoby, N. P., Young, A. L., Bron, E. E., Toga, A. W., Weiner, M. W., ... & Alexander, D. C. (2019, October). TADPOLE Challenge: Accurate Alzheimer’s disease prediction through crowdsourced forecasting of future data. In International workshop on predictive intelligence in medicine (pp. 1-10). Cham: Springer International Publishing.
