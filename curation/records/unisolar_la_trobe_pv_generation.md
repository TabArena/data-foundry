---
unique_name: unisolar_la_trobe_pv_generation
name: UNISOLAR (La Trobe University multi-campus PV generation, 2020-2022)
checked_by:
- Andrej
suggestion: TBD -> 2nd Tier
priority: 2
decision_markers:
- Time-series (Forecasting)
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
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. Drafted by an AI assistant on 2026-10-19 from the two-regime-zero workbook (`curation/inputs/two_regime_zero_datasets_v4.xlsx`), the source pages and papers, and the data itself where the notes say it was downloaded and measured. A human must verify the suggestion, the metadata and the notes before relying on them.**

**Screening (AI, 2026-10-27):** `TBD -> 2nd Tier`, priority 2: 15-minute PV generation of 42 sites on five campuses
with irradiance, weather and site details, a panel with an outside driver whose forecasting test (TP-10) has not been
run; the claimed night-time zeros do not exist.
- Source: Wimalaratne et al. (2022), "UNISOLAR: An Open Dataset of Photovoltaic Solar Energy Generation in a Large
  Multi-Campus University Setting", HSI 2022 (La Trobe University; https://doi.org/10.1109/HSI55341.2022.9869474).
  GitHub (CDAC-lab/UNISOLAR, `data/`) ships a generation subset, a weather subset, `Solar_Irradiance.csv` (hourly GHI
  and cloud opacity per campus, 2019-12-31 to 2022-05-01), `Solar_Site_Details.csv` (kWp, panels, inverter, latitude
  and longitude; kWp filled for 25 of 42 sites, per the reject check) and a monthly summary; Kaggle
  (cdaclab/unisolar, November 2022, CC BY-NC-SA 4.0) holds the full generation and weather files. The earlier AI
  triage (2026-10-19) measured 2,731,946 generation rows (`CampusKey`, `SiteKey`, `Timestamp`, `SolarGeneration`),
  2020-01-01 to 2022-04-23.
- Target and zeros: `SolarGeneration` per site and 15 minutes. Night is coded missing (99.97% of the 21:00-05:00
  rows), and the smallest value is 0.1, so there are no zeros (earlier triage, measured).
- Use case: the abstract: "This dataset can be used to forecast, benchmark, and enhance operational outcomes in solar
  sites"; the README lists the "technical validation of the dataset for forecasting" and, per the reject check, to
  "analyse, predict and optimize". Either a campus energy manager forecasts site output (fit approximate: the
  observed weather and irradiance stand in for forecasts) or checks each site against its expected yield from the
  measured irradiance (monitoring, fit direct); the source names no actor. Regime temporal (SPLIT-6), sites recur
  (SPLIT-13).
- Scope doubt (SEL-10, SEL-11, TP-10): the earlier pass and this screening proposed `No` as forecasting; the reject
  check refuted it, since a site panel with an outside driver goes to TP-10 and the source cannot settle TP-10 (no
  competition, the validation notebook fits no model, the paper is unread). `combined_cycle_power_plant` and
  `appliances_energy_prediction` (SEL-10 cases) are single units; the closer precedent is
  `ashrae_great_energy_predictor_iii`, a building panel with concurrent weather that passed TP-10.
- Siblings and duplicates: `solar_power_generation_data` and `electricity_demand_and_solar_generation_data_uk` (`No`,
  Lennart, markers `Wrong Domain / Source Modality` and `Time-series (Classification)`, no reason written; other
  plants), `utility_scale_pv_generation_2017_2022_unidentified` (no source). No external collection found.
- Papers and pages: the HSI paper (closed access, not read), the GitHub README and notebook, the Kaggle data card;
  papers that use the data are forecasting studies (CapsNet, LSTM and Transformer comparisons).
- Metric: none found (abstract, README, Kaggle data card; the paper's validation section was not read), so the
  fallback, `rmse` (MET-8).
- Risks for /add-dataset: (1) TP-10 leg 1, a model on GHI, cloud opacity, weather, site details and calendar against
  each site's naive profile on temporal windows; (2) leg 2, read the HSI paper's validation and whether the CapsNet,
  LSTM and Transformer papers use lags of generation; (3) TP-4, whether GHI x kWp alone matches the models
  (`one_feature`); (4) the prediction point: with the measured GHI it is monitoring or expected yield (direct), as a
  forecast it is approximate (USE-3, USE-8); (5) no zeros at all, so whether the `Two-Regime Zeros` tag stays; (6) a
  consistency check against `solar_power_generation_data` (`No`, Lennart). Joins of generation (15 min), weather
  (1 min) and irradiance (hourly) per campus.
- Priority: gap 0, use case 0 (no actor named), source + (paper, README, site details), shape + (42 sites, 2.7
  million dated rows, weather, irradiance and site features), risk - (scope doubt, joins across three resolutions).
- Reject check (AI, 2026-10-27): does not stand. The release ships hourly GHI and cloud opacity per campus and site
  details (https://github.com/CDAC-lab/UNISOLAR/tree/main/data), so it is a 42-site panel with an outside driver that
  SEL-11 sends to TP-10, which the source cannot settle.

**Assessment (AI, 2026-10-30):** tag `Two-Regime Zeros` removed under the curator's definition of the tag (Andrej,
2026-10-30, policy question 4 of the zero-inflated review: "If the low value is by far the most frequent one and
independent of the remaining target distribution, then we can treat it as two regime zero, otherwise not"). Measured on
`Solar_Energy_Generation.csv`: night is missing (56.2% of the rows); among the 1.2 million readings the smallest value,
0.1, almost never occurs, and the most frequent (0.125) holds 0.4%. No low-value regime.

CC (2026-10-30, Andrej): `TBD -> 2nd Tier`, priority 2, as screened (verified on the zero-inflated screening review
page).

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
