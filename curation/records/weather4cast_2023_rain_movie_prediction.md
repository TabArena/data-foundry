---
unique_name: weather4cast_2023_rain_movie_prediction
name: Weather4cast 2023 (super-resolution rain movie prediction, NeurIPS 2023 competition)
checked_by:
- AI (UNVERIFIED)
suggestion: 'No'
decision_markers:
- Image
- Time-series (Forecasting)
tags:
- AI-Filled (Verify)
- Two-Regime Zeros
original_source: Website
year: '2023'
domain: environmental science & climate
required_split:
- Custom
problem_type: Regression
original_data_state: Other
source_links:
- https://github.com/agruca-polsl/weather4cast-2023
- https://weather4cast.net/get-the-data/
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. Drafted by an AI assistant on 2026-10-19 from the two-regime-zero workbook (`curation/inputs/two_regime_zero_datasets_v4.xlsx`), the source pages and papers, and the data itself where the notes say it was downloaded and measured. A human must verify the suggestion, the metadata and the notes before relying on them.**

Weather4cast 2023 (IARAI and Silesian University of Technology): from four time slots of 11-band EUMETSAT satellite
images, "predict the exact amount of rainfall for the next 8 hours in 32 time slots" on 252 x 252 OPERA radar crops
(README). Training inputs are HDF5 tensors of shape (20308, 11, 252, 252) per region, released after registration
(not downloaded). Image-sequence nowcasting: `Image` and `Time-series (Forecasting)`.

Zero mechanism: no-rain radar pixels, not confirmed. Workbook pushback: its Kaggle URL does not exist (the Kaggle API
returns 404 for that competition), and the README does not frame the task as zero-inflated regression.

## Reference

Weather4cast 2023 competition repository and README, https://github.com/agruca-polsl/weather4cast-2023. Earlier
edition: Gruca A. et al. (2023). Weather4cast at NeurIPS 2022: Super-Resolution Rain Movie Prediction under
Spatio-temporal Shifts. PMLR 220:292-313.

Lead: curation/inputs/two_regime_zero_datasets_v4.xlsx, Master row 54 (Weather4cast 2023).
