---
unique_name: unisolar_la_trobe_pv_generation
name: UNISOLAR (La Trobe University multi-campus PV generation, 2020-2022)
checked_by:
- AI (UNVERIFIED)
suggestion: 'No'
decision_markers:
- Time-series (Forecasting)
tags:
- AI-Filled (Verify)
- Two-Regime Zeros
original_source: Kaggle
year: '2022'
domain: environmental science & climate
required_split:
- Temporal (NON-IID)
problem_type: Regression
original_data_state: Database (or multiple to-be-joined tables)
source_links:
- https://www.kaggle.com/datasets/cdaclab/unisolar
- https://github.com/CDAC-lab/UNISOLAR
- https://doi.org/10.1109/HSI55341.2022.9869474
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. Drafted by an AI assistant on 2026-10-19 from the two-regime-zero workbook (`curation/inputs/two_regime_zero_datasets_v4.xlsx`), the source pages and papers, and the data itself where the notes say it was downloaded and measured. A human must verify the suggestion, the metadata and the notes before relying on them.**

Solar generation of 42 sites on 5 La Trobe campuses (Victoria, Australia) at 15-minute resolution, 2020-01-01 to
2022-04-23, with weather by campus. The full data is on Kaggle (`cdaclab/unisolar`); the GitHub repository the
workbook links holds a 1 MB subset. Downloaded and measured on 2026-10-19: 2,731,946 rows (`CampusKey`, `SiteKey`,
`Timestamp`, `SolarGeneration`). The abstract positions it for forecasting ("This dataset can be used to forecast,
benchmark, and enhance operational outcomes in solar sites"; the IEEE paper text was not read). Site-by-time
generation is series forecasting, like the siblings `solar_power_generation_data` and
`electricity_demand_and_solar_generation_data_uk` (different plants, Lennart: No).

Zero mechanism: the data contradict the workbook, which calls the night-time zero regime "very explicit". The release
has no zeros at all: night is coded as missing (99.97% of the 21:00-05:00 rows are NA, 56.2% of all rows), and the
smallest value is 0.1. Licence: CC BY-NC-SA 4.0 on Kaggle ("only for Research purposes").

## Reference

Wimalaratne S., Haputhanthri D., Kahawala S., Gamage G., Alahakoon D., Jennings A. (2022). UNISOLAR: An Open Dataset
of Photovoltaic Solar Energy Generation in a Large Multi-Campus University Setting. 15th International Conference on
Human System Interaction (HSI 2022). doi:10.1109/HSI55341.2022.9869474.

Lead: curation/inputs/two_regime_zero_datasets_v4.xlsx, Master row 8 (PV generation / UNISOLAR).
