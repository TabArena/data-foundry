---
unique_name: nigeria_property_centre_house_prices
name: Nigeria Houses and prices dataset (nigeria_houses_data.csv)
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 1
tags:
- AI-Filled (Verify)
original_source: Kaggle
year: '2021'
domain: business & marketing
required_split:
- Random (IID)
problem_type: Regression
original_data_state: One Table
source_links:
- https://www.kaggle.com/datasets/abdullahiyunus/nigeria-houses-and-prices-dataset
- '# a copy of the same file (nigeria_houses_data.csv, same size), re-uploaded 2024'
- https://www.kaggle.com/datasets/michaelanietie/nigerian-house-price-dataset
- '# a copy of the same file (nigeria_houses_data.csv, same size), re-uploaded 2026'
- https://www.kaggle.com/datasets/abbas829/nigeria-real-estate-and-housing-market-dataset
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> 2nd Tier`, priority 1: 24,326 house listings scraped from Nigeria Property Centre with seven attributes and the asking price; a real scrape that the generated Zindi table seems modelled on, but undated, undocumented and in a crowded task.
- Source: Kaggle, Abdullahi Yunus, "Nigeria Houses and prices dataset", uploaded 2021-06-17 (licence "copyright-authors", empty description); its info.txt: "Datashape (24326, 8)", columns bedrooms, bathrooms, toilets, parking_space, title (house type), town, state and price ("the target column"), "Source: https://nigeriapropertycentre.com/", and the uploader's scraping project on GitHub (Abdulkbk/Nigerian-Real-Estate-Project, not opened). No scrape date, no listing date, and no listing type (sale or rent) stated.
- Use case: a seller or agent sets an asking price, or a buyer checks one, from house type, rooms and location; fit approximate: an asking price, not a sale price, and the scrape time is unknown (PROV-2); regime IID within the one scrape, noting that a missing timestamp does not make the data a random draw (SPLIT-7).
- Siblings and duplicates: `free_ai_classes_in_every_city_hackathon_2023` (`No`, AHDS: the generated Zindi table with the same columns minus toilets and town). Copies of this file: michaelanietie (2024, MIT) and abbas829 (2026, CC BY-SA; its card describes a `crib.csv` with listing dates, but its file is `nigeria_houses_data.csv` of the same 1,434,704 bytes). Not this data, moved from the source links to here (PROV-12): thedevastator's Lagos listings from another scrape (https://www.kaggle.com/datasets/thedevastator/investigating-housing-prices-in-lagos-nigeria) and the paper Nwankwo et al. 2023, "Prediction of House Prices in Lagos-Nigeria Using Machine Learning Models" (https://zenodo.org/records/8344787), which may have used this file (not checked). External collections: none known (not searched: the run's web search budget was used up).
- Better data: found as better data for `free_ai_classes_in_every_city_hackathon_2023`; no further search this round.
- Papers and pages: the Kaggle card and info.txt; the paper above.
- Metric: none found (no competition or paper defines the task on this file), so the fallback `rmse` on the Naira price (MET-8); inputs none.
- Risks for /add-dataset: repeated listings (a portal scrape often lists one house several times; not checked, no download); price outliers and possible rentals among sales; town names to clean; seven features only; the scrape date to look for in the GitHub project.
- Priority: gap 0 (business, regression and IID are not thin), use case 0, source 0 (a named uploader and portal, no documentation), shape + (24,326 listings, mixed types), risk - (undated scrape, likely repeated listings).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through better data for `free_ai_classes_in_every_city_hackathon_2023`.
- as published: one CSV, 1.43 MB, 8 columns: bedrooms, bathrooms, toilets, parking_space, title (house type), town, state, price (Naira); about 24k listings judging by the file size (not counted: no download); no ...; target: price, the listed price of the house in Naira; access: open.
- Why: The generated Zindi 2023 table (loc, title, bedroom, bathroom, parking_space, price) has the same columns as this real scrape minus toilets and town, so it looks like a synthetic copy of this data. Same target (house price in Nigeria) and the same kind of features, here as real listings.
- Adds: Real listings in place of generated rows (the Zindi rows are uniform over states, have prices with three decimals and injected missing values). Adds town-level location and toilets, with about 24k rows against 14k. Caveats: the scrape date and the portal are named only by re-uploaders (PROV-2), the licence is ...
