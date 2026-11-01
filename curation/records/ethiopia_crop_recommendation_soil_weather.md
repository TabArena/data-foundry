---
unique_name: ethiopia_crop_recommendation_soil_weather
name: Crop Recommendation using Soil Properties and Weather Prediction Dataset (Ethiopia)
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 2
tags:
- AI-Filled (Verify)
original_source: Other
year: '2024'
domain: environmental science & climate
problem_type: Multiclass Classification
original_data_state: One Table
source_links:
- https://doi.org/10.17632/8v757rr4st.1
- https://data.mendeley.com/datasets/8v757rr4st/1
- https://arxiv.org/abs/2603.25070
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> 2nd Tier`, priority 2: 3,867 Ethiopian soil tests (colour, pH, K, P, N, Zn, S) from the Agricultural Transformation Agency joined to seasonal NASA POWER climate and labelled with the crop (mostly cereals); a real multiclass agronomy table, but the label is the crop grown rather than the best one, the climate repeats per location block, and in a short preview the number formats differ between crop blocks.
- Source: Sltanu Alemu (Addis Ababa Science and Technology University), "Crop Recommendation using Soil Properties and Weather Prediction Dataset", Mendeley Data v1, 2024-09-04, doi 10.17632/8v757rr4st.1, CC BY-NC-ND 4.0 (a note, EV-4); one CSV of 861,663 bytes. The description: soil properties and crop type "procured from the Ethiopian Agricultural Transformation Agency (ATA)", climate "sourced from the National Aeronautics and Space Administration's (NASA) cloud infrastructure" and "collected based on specific years and geographical coordinates (latitude and longitude), with an emphasis on anticipating the conditions for the upcoming season", production data from the Ethiopian Statistics Service. As published (the CSV header): `Soilcolor, Ph, K, P, N, Zn, S`, 16 seasonal NASA POWER aggregates (`QV2M`, `T2M_MAX`, `T2M_MIN`, `PRECTOTCORR` for winter, spring, summer, autumn), `WD10M, GWETTOP, CLOUD_AMT, WS2M_RANGE, PS`, `label` (Barley, Maize, Teff and Wheat seen in the preview); 29 columns, no latitude or longitude despite the description, no year.
- Use case: an extension officer recommends a crop for a plot from its soil test and the expected season (the publisher's "crop recommendation system"); fit approximate (the label is the crop grown, not the best crop, USE-5; the climate's year against the planting decision is not stated, USE-3). Regime: grouped by location block (rows share one climate vector per location, so an IID split puts a location on both sides), to decide at add time.
- Siblings and duplicates: no other record of this upload, and the semi-synthetic Kaggle crop-recommendation set has no record (grep); crop records of other tasks: `crop_type_classification_challenge`, `cy_bench_subnational_crop_yield`, `amini_soil_prediction_challenge`, `open_soil_data`. External collections: none found.
- Better data: from the curator's Zotero collection (item 151); no search for better data in this run.
- Papers and pages: Masud et al., arXiv 2603.25070 (2026): 3,867 x 29, SMOTE, 98.80% accuracy, precision, recall and F1 for an ensemble; no paper by the publisher found.
- Metric: none deliberate: the paper reports accuracy, precision, recall and F1 together; fallback `log_loss` for the multiclass task (MET-1, MET-5, MET-6); inputs none.
- Risks for /add-dataset: in a preview of four small byte ranges, Barley and Wheat rows carry K, P and S with three decimals (738.231, 5.401) and Maize and Teff rows integers (61, 384), and `N` is 0.23 in many Barley rows: a recording that may differ by crop block (LEAK-13 to LEAK-15; measure before any `Class-dependent Recording` marker); the climate vector identifies the location block and with it much of the label (a spatial leak; the paper's 98.8% fits it); the label is the crop grown (USE-5); the climate's year against planting (LEAK-10); the class balance not seen.
- Priority: gap + (multiclass classification is thin), use case 0 (approximate fit), source 0 (a data deposit with a description, no paper by the publisher), shape + (3,867 rows, 28 mixed features), risk - (the recording and the spatial leak to measure).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the curator's Zotero collection, item 151: "An Explainable Ensemble Learning Framework for Crop Classification with Optimized ...".
- as published: 3,867 rows x 29 columns (per the paper; 2,963 after its cleaning), one 0.86 MB CSV; years not stated; target: Crop type grown at the soil-sample location (multiclass, mostly cereals); access: open (CC BY-NC-ND 4.0).
- Why: Real soil-test data with a crop label, unlike the semi-synthetic Kaggle crop-recommendation set Risks: the label is the crop grown, not the best crop; 98.8% accuracy in the paper suggests location leakage; NC-ND licence; near Too Small.
- Adds: Agricultural multiclass task from Africa
