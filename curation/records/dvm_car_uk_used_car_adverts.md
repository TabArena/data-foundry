---
unique_name: dvm_car_uk_used_car_adverts
name: 'DVM-CAR: A large-scale automotive dataset (Ad table of UK used-car adverts)'
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 3
tags:
- AI-Filled (Verify)
collections:
- MulTaBench
original_source: Other
year: '2021'
domain: business & marketing
problem_type: Regression
original_data_state: Database (or multiple to-be-joined tables)
source_links:
- https://arxiv.org/abs/2109.00881
- https://deepvisualmarketing.github.io/
- https://doi.org/10.6084/m9.figshare.19586296.v2
- https://doi.org/10.1109/BigData55660.2022.10020634
- https://eprints.gla.ac.uk/286245/
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 3: the UK used-car advert table of DVM-CAR, a documented research dataset (IEEE Big Data 2022, figshare DOI) with more than a quarter million adverts and their asking price; the canonical record of this data.
- Source: Huang, Chen, Luo, Yue and Ounis, "DVM-CAR: A large-scale automotive dataset for visual marketing research and applications", arXiv 2109.00881 (v1 2021-08-10), IEEE Big Data 2022, pp. 4130-4137; project page https://deepvisualmarketing.github.io/; figshare doi:10.6084/m9.figshare.19586296 (v2, 2023-01-07, `tables_V2.0.zip`, 198 MB; CC BY 4.0 on figshare, while the project page says CC BY-NC 4.0, "only for non-commercial research and educational purposes"). As published: six CSV tables (Basic, Sales, Price, Trim, Ad, Image) joined on `Genmodel_ID`. The Ad table "contains more than 0.27 million used car advertisements information posted on the automotive classified advertising platforms" (paper, Table II; the project page says "more than 0.25 million"): `Maker`, `Genmodel`, `Genmodel_ID`, `Adv_ID`, `Adv_year`, `Adv_month`, `Color`, `Reg_year`, `Bodytype`, `Runned_Miles`, `Engin_size`, `Gearbox`, `Fuel_type`, `Price`, `Seat_num`, `Door_num`. The adverts come from "the popular automotive classified advertising platforms ... in the UK" (Sect. II), which the paper does not name.
- Use case: a seller, a dealer or the platform values a used car when the advert is created, from model, registration year, mileage and specification; fit approximate: the target is the asking price, not the sale price, and the paper uses the data for design and sales research (Sect. V), not for pricing; regime temporal (`Adv_year` and `Adv_month` ship, and a valuation is made for new adverts), with model-level grouping as the alternative (USE-10 decides).
- Siblings and duplicates: `dvm_car_prices` (MulTaBench's 100,000-row cut with photos, from a Kaggle re-upload; proposed `Duplicate` of this record, PROV-6, in screening batch 07); used-car price records from other sources (PROV-7, not duplicates): `used_cars_24`, `used_cars_benz_italy`, `used_cars_dataset_cardekho`, `used_cars_saudi_arabia`, `exploreml_funaab_hackathon_nigerian_cars_price_prediction`, `free_ai_classes_in_every_city_hackathon`. External collections: MulTaBench (extended image release, through the Kaggle copy; added to `collections`).
- Better data: found as better data for `exploreml_funaab_hackathon_nigerian_cars_price_prediction`, `free_ai_classes_in_every_city_hackathon`, `used_cars_24`, `used_cars_benz_italy`, `used_cars_dataset_cardekho` and `used_cars_saudi_arabia` (the data-scouting run of 2026-10-30/31); no further search.
- Papers and pages: the DVM-CAR paper (arXiv 2109.00881: Sect. II collection, Table II tables, Sect. V applications); the project page; MulTaBench (https://arxiv.org/abs/2605.10616).
- Metric: none found (the paper defines no price task: Sect. V shows modernity scoring, generated designs and sales forecasting; the project page and figshare state none), so the fallback `rmse`, on log price if the definition ships it (MET-3); inputs none.
- Risks for /add-dataset: use the Ad table; the Trim and Price tables hold new-car prices by model and year (joinable on `Genmodel_ID` and year; check that a join adds nothing dated after the advert, LEAK-10); the same car may be advertised more than once (LEAK-16: check `Adv_ID` and repeated rows); placeholder and outlier asking prices; the advert years are not stated on the page or in the paper (read them from the table); the advertising platforms are not named (PROV-2 note).
- Priority: gap 0 (business & marketing, regression and temporal are not thin), use case 0 (no pricing use named by the source), source + (peer-reviewed dataset paper, DOI), shape + (about 270k adverts, mixed types, advert dates).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through better data for `exploreml_funaab_hackathon_nigerian_cars_price_prediction`, `free_ai_classes_in_every_city_hackathon`, `used_cars_24`, `used_cars_benz_italy`, `used_cars_dataset_cardekho`, `used_cars_saudi_arabia`.
- as published: Ad table: 'more than 0.25 million used car advertisements' in the UK (project page), with maker, model, advert year and month, registration year, mileage, body type, engine size, gearbox, fuel, ...; target: advertised used-car price (GBP); access: open, open (CC BY 4.0 on figshare; the project page says CC BY-NC 4.0, non-commercial research and education).
- Why: Same target and the same kind of features as the two Nigerian hackathon tables (make, model, year, mileage, fuel, gearbox, engine size, colour), another market. No larger or traceable Nigerian set was found: the 2026 UNILAG paper's 8,000-listing scrape is not public as far as its page shows, and the Zindi upstream ...
- Adds: A traceable first publication (a peer-reviewed dataset paper with a DOI) instead of unnamed scrapes, about 35 times the 7,205 rows of the larger Nigerian table, advert dates for a temporal split, linked specification and new-price tables. | Over 250,000 adverts against 6,019 (used_cars_24, source unconfirmed), 5,508 ...
