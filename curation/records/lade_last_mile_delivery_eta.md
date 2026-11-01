---
unique_name: lade_last_mile_delivery_eta
name: 'LaDe: The First Comprehensive Last-mile Delivery Dataset from Industry'
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 2
tags:
- AI-Filled (Verify)
original_source: Company
year: '2023'
domain: industry & manufacturing
problem_type: Regression
source_links:
- https://arxiv.org/abs/2306.10675
- https://huggingface.co/datasets/Cainiao-AI/LaDe
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 2: Cainiao's six months (May to October 2022) of last-mile parcel deliveries in five Chinese cities, about 10.7M packages by 21k couriers, published with a KDD 2024 paper that benchmarks an ETA task; named features, but the per-package framing at acceptance differs from the paper's route-level ETA, and the courier's same-day load has to be built.
- Source: Wu et al., "LaDe: The First Comprehensive Last-mile Express Dataset from Industry", KDD 2024 (arXiv 2306.10675, v1 2023-06-19); data on Hugging Face `Cainiao-AI/LaDe` (Apache-2.0 on the card; "LaDe can be used for research purposes"). As published: LaDe-D (delivery) and LaDe-P (pickup), one CSV per city (Shanghai, Hangzhou, Chongqing, Jilin, Yantai); LaDe-D columns `package_id`, `lng`/`lat`, `city`, `region_id`, `aoi_id`, `aoi_type`, `courier_id`, `accept_time`, `accept_gps_time`, `accept_gps_lng`/`lat`, `delivery_time`, `delivery_gps_time`, `delivery_gps_lng`/`lat`, `ds`; plus courier trajectories and a road network; "10,677k packages of 21k couriers over 6 months of real-world operation"; time range 2022-05-01 to 2022-10-31 (GitHub README).
- Use case: a parcel platform tells the recipient when the courier will arrive and plans courier load; the paper benchmarks ETA next to route prediction and spatio-temporal graph forecasting. Fit approximate: the paper's ETA predicts arrival times of a courier's unfinished packages at a query time; a per-package `delivery_time - accept_time` at acceptance is our framing. Regime temporal (a delay, SEL-11, SPLIT-6), with couriers and cities as groups inside it (SPLIT-13).
- Siblings and duplicates: `delivery_eta` (Yes, `Anonymized`; food or grocery delivery time); no record of LaDe (grep lade, cainiao, last mile). External collections: none found.
- Better data: from the scout of `delivery_eta`, as a related task (parcels rather than food orders, older data), not as better data for it.
- Papers and pages: the KDD 2024 paper and its GitHub (wenhaomin/LaDe, `time_prediction` folder for ETA).
- Metric: the card's ETA leaderboard reports MAE, RMSE and ACC@30 side by side, no unique one (MET-5), so the fallback `rmse` (MET-8).
- Risks for /add-dataset: the delivery time depends on the courier's route and load that day, of which only the part accepted before the package is known at acceptance (other packages' delivery times are later events; LEAK-10); the delivery GPS fields go; 10.7M rows need one city or a sample; AOI and region ids are documented codes (no `Anonymized` marker).
- Priority: gap 0 (industry & manufacturing, regression and temporal are covered), use case 0 (tasks named, no actor; fit approximate), source + (Cainiao with a KDD paper), shape + (millions of packages, named mixed features, dates and groups), risk - (the per-package framing and the same-day features to build).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through a related task next to `delivery_eta`.
- as published: about 10.68M packages by 21k couriers over six months in five Chinese cities (Shanghai, Hangzhou, Chongqing, Jilin, Yantai); LaDe-D (delivery) and LaDe-P (pickup) CSVs per city, plus courier ...; target: package delivery time from the courier's acceptance (delivery_time - accept_time), the paper's ETA task (MAE, RMSE, ACC@30; LightGBM among the baselines); access: open (Apache-2.0 on the card; the card asks for research use).
- Why: the delivery-time task of delivery_eta, but for last-mile parcels rather than food or grocery orders and from older data (2022 operations), so it is listed as related, not better
- Adds: named, non-anonymised features (coordinates, AOI id and type, region, courier, acceptance time), where delivery_eta carries the Anonymized marker and its feature timing cannot be checked; a grouped (courier or city) or temporal split is possible
