---
unique_name: weather4cast_2023_rain_movie_prediction
name: Weather4cast 2023 (super-resolution rain movie prediction, NeurIPS 2023 competition)
checked_by:
- Andrej
suggestion: 'No'
decision_markers:
- Image
- Time-series (Forecasting)
tags:
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
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. Drafted by an AI assistant on 2026-10-19 from the two-regime-zero workbook (`curation/inputs/two_regime_zero_datasets_v4.xlsx`), the source pages and papers, and the data itself where the notes say it was downloaded and measured. A human must verify the suggestion, the metadata and the notes before relying on them.**

**Screening (AI, 2026-10-27):** `No` (`Image`, `Time-series (Forecasting)`; SEL-12, SEL-10): a movie of radar rain
rates for the next 8 hours, predicted from sequences of 11-band satellite images, is an image task whose organisers
ship an image model as the baseline; SEL-12 holds on its own, and the 32-frame horizon makes it a forecast too.
- Source: Weather4cast 2023, a NeurIPS 2023 competition (IARAI and the Silesian University of Technology), README of
  https://github.com/agruca-polsl/weather4cast-2023: "The input sequence consists of four 11-band spectral satellite
  images", "Each satellite image covers a 15 minute period and its pixels correspond to a spatial area of about 12km x
  12km", training inputs "a tensor of shape `(20308, 11, 252, 252)`"; "The prediction output is a sequence of 32
  images representing rain rates from ground-radar reflectivities" (OPERA), where "the 252x252 pixel ground radar
  patch corresponds to a 42x42 pixel center region in the coarser satellite resolution"; the organisers' baseline is a
  "Unet-3D baseline model". The task: "predict the exact amount of rainfall for the next 8 hours in 32 time slots".
  Data after registration; not downloaded.
- SEL-12 first: raw multi-band image tensors in and image sequences out, with image models as the tool (the U-Net
  baseline; 2023 participant papers such as arXiv:2311.18806 use the U-Net family). A per-pixel recast would feed raw
  spectra (SEL-13, as `satimage`) and be a task of our own (PROV-11). SEL-10 second: future frames of a rain field
  over a horizon; "no satellite radiances are provided for the future, so this is a true prediction task" (README).
- Use case: precipitation nowcasting for a weather service. Regime temporal, with held-out regions for transfer.
- Siblings and duplicates: the 2021 and 2022 editions are not in the records; `how_much_did_it_rain` and
  `how_much_did_it_rain_ii` estimate gauge rain from radar summaries, another task. External collections: Hugging Face
  mirrors (e.g. `elskow/Weather4cast`).
- Papers and pages: Gruca et al. (2023), PMLR 220:292-313 (the 2022 edition); 2023 participant papers.
- Metric: the 2023 participant papers report the mean CSI over the thresholds 0.2, 1, 5, 10 and 15 (arXiv:2311.18806);
  the organisers' page was not read.
- Workbook pushback: its Kaggle link does not exist (Kaggle API 404, earlier AI triage 2026-10-19).
- Reject check (AI, 2026-10-27): stands. SEL-12 (Must). The README states the inputs are "four 11-band spectral
  satellite images" and the output "a sequence of 32 images", with a "Unet-3D baseline model"
  (https://github.com/agruca-polsl/weather4cast-2023).

CC (2026-10-30, Andrej): `No`, as screened (verified on the zero-inflated screening review page).

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
