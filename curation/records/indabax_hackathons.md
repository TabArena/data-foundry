---
unique_name: indabax_hackathons
name: indabax-hackathons
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 1
decision_markers:
- Needs extensive data wrangling
- Duplicate
tags:
- AI-Filled (Verify)
collections:
- New (BeyondArena)
original_source: Zindi
domain: Other
required_split:
- '?'
problem_type: TBD
original_data_state: Other
source_links:
- https://zindi.africa/competitions/indabax-benin-republic-hackathon/data
- https://zindi.africa/competitions/indabax-madagascar-hackathon
- https://zindi.africa/competitions/indabax-mozambique-2023
- https://zindi.africa/competitions/la-detection-des-fraudes/data
- https://zindi.africa/competitions/indabax-equatorial-guinea-hackathon
- https://zindi.africa/competitions/indabax-tunisia-2025-challenge-1
- https://zindi.africa/competitions/indabax-tunisia-2025-challenge-2/data
- https://zindi.africa/competitions/indabax-south-africa-2025-hackathon-with-instadeep
- https://zindi.africa/competitions/grand-hackathon-dindabax-togo-2023/data
- https://zindi.africa/competitions/isazi-indabax-2024-hackathon-challenge/data
- https://zindi.africa/competitions/indabax-kenya-pwani-ai-summit-challenge-2024
- https://zindi.africa/competitions/indabax-togo-2022/data
source_row: 936
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-22):** `TBD -> 2nd Tier`, priority 1: not one dataset but twelve IndabaX-type Zindi hackathons; most are re-runs of recorded competitions or out of scope, one (Tunisia 2025 Challenge 1) may deserve its own record.
- Source: the Zindi API for each linked competition (2022-2025, all private hackathons). As published, per link: Benin Republic 2024, cryptojacking detection, parent `indabax-rwanda-2024-hacktathon` (recorded under `ai_national_summit_2024_competition`); Madagascar 2023, data type NLP, accuracy; Mozambique 2023, weekly product sales per store, parent `grocery-store-product-forecasting-challenge` (record `grocery_store_product_forecasting_challenge`, a forecast, SEL-10); `la-detection-des-fraudes` 2023, Xente fraud, parent `indabax-benin-2022`, same training.csv (17,071,505 B) as `grand-hackathon-dindabax-togo-2023` (record `xente_fraud_detection_challenge`); Equatorial Guinea 2025, CO2 emissions, parent `umojahack-africa-2023-beginner-challenge` (record `carbon_dioxide_prediction_challenge`); Tunisia 2025 Challenge 1, LTE cell KPIs, multi-label anomaly flags ("Bad Congestion", "Very Low Throughput", ...), Hamming loss, Train.csv 687 MB, no parent; Tunisia 2025 Challenge 2, BLEU (text generation, SEL-12); South Africa 2025 with InstaDeep, interatomic potentials from .xyz files (molecular structures, not tabular); Isazi 2024, daily product sales volume "forecasts the future sales volumes" (SEL-10); Kenya Pwani 2024, coral images, data type Image (SEL-12); Togo 2022, Financial Inclusion in Africa re-run, parent `financial-inclusion-in-africa` (see `financial_inclusion_in_africa_for_botswana`).
- Use case: per competition; none for the bundle. Regime: per competition.
- Siblings and duplicates: listed above; `indabax_drc_2022` and `indabax_eswatini_2022` were set to `Duplicate` by the curator (2026-10-12) on the same kind of evidence (parent competition, identical file sizes).
- Papers and pages: the twelve Zindi pages; none read beyond the API text.
- Metric: per competition (F1, accuracy, RMSE, Hamming loss, BLEU); none for the bundle.
- Risks for /add-dataset: the record cannot be added as is. Recommend: split `indabax-tunisia-2025-challenge-1` into its own record (telecom KPIs, check whether it is a per-cell time series, `Time-series (Classification)`, and the 687 MB size), keep the duplicate links as notes on their canonical records, and retire this bundle as `No` + `Duplicate` once that is done; the curator decides.
- Priority: gap 0, use case 0, source 0 (a bundle), shape 0, risk - (mostly duplicates and out-of-scope tasks); floor 1.

This record is not a single dataset but an aggregation of roughly a dozen distinct IndabaX hackathon competitions (Benin, Madagascar, Mozambique, Equatorial Guinea, multiple Tunisia, South Africa, Togo, Isazi, Kenya, etc.), each with its own task, target, and modality. It cannot be triaged as one dataset and several entries may be fraud/marketing/classification while others could be out of scope. The right move is to split this into individual candidate records and assess each separately. A human must enumerate each linked competition, deduplicate against existing records, and decide per-task.
