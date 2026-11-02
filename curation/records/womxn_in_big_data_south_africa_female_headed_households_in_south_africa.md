---
unique_name: womxn_in_big_data_south_africa_female_headed_households_in_south_africa
name: womxn-in-big-data-south-africa-female-headed-households-in-south-africa
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 3
tags:
- AI-Filled (Verify)
collections:
- New (BeyondArena)
original_source: Zindi
year: '2019'
domain: social science
required_split:
- '?'
problem_type: Regression
original_data_state: One Table
source_links:
- https://zindi.africa/competitions/womxn-in-big-data-south-africa-female-headed-households-in-south-africa/data
- https://zindi.africa/competitions/indabax-sa-2022-beginner/data
- https://zindi.africa/competitions/dsa-2021
source_row: 932
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-22):** `TBD -> Yes`, priority 3: the ward-level share of poor female-headed households from 2011 South African census aggregates; the first publication of data Zindi re-ran at least four times; social science is thin, and 2,822 labelled wards refute the old `Too Small`.
- Source: Zindi competition "Womxn in Big Data South Africa: Female-Headed Households in South Africa", 25 Nov 2019 to 24 Feb 2020, sponsored by Women in Big Data South Africa and Microsoft with HERE Technologies (page read through Zindi's API); as published: "We have aggregated the target indicator and the other predictive variables from the 2011 census across all the households within each ward"; target "the percentage of households per ward that are both female-headed and earn an annual income that is below R19,600"; "2,822 wards in the train set" (labelled) and "1,013 wards in the test set" (no labels); Train.csv 2,049,620 bytes, Test.csv 1,113,085, variable_descriptions.csv 4,393. Named columns: ward centre `lat`, `lon`, ward code `ADM4_PCODE`, nightlights `NL`; the other columns not read (login).
- Use case: "it is important for policymakers and other actors to have accurate estimates of these statistics even in between census years ... by using data points that can be collected through other means without an intensive household survey like the census" (Description). Fit approximate: the features are themselves 2011 census aggregates, not the between-census sources the use case names (only `NL` is). Regime grouped (spatial): neighbouring wards share their municipality (in the ward code), so a random split lets neighbours inform each other; one census, no time axis.
- Siblings and duplicates: re-runs with the same text and byte sizes, proposed `No` (`Duplicate`) in this re-screen: `international_womens_day_challenge` (2025), `atf_2023_hackathon` (2023); `be_a_trailblazer` carries the same target text (likely a re-run, not checked). The record's second and third links (indabax-sa-2022-beginner, Dec 2022; dsa-2021, Oct 2021) are Zindi children of this competition (the API's parent field), same data description and metric. External collections: none found.
- Papers and pages: no paper; the Description, Data and Evaluation pages; the winners' solutions were promised public (not read).
- Metric: RMSE ("The error metric for this competition is the Root Mean Squared Error", Evaluation page); a competition's leaderboard metric (MET-4); inputs none.
- Risks for /add-dataset: the column list is unread: census aggregates close to the target's parts (share of female heads, income bands) would make it near-deterministic (SEL-5, LEAK); only the 2,822 train wards are labelled; the spatial grouping key to choose (municipality from `ADM4_PCODE`; SPLIT); the rules forbid redistribution (no criterion, EV-4).
- Priority: gap + (social science, 1 accepted dataset), use case 0 (named by the source, but the fit is approximate), source 0 (a competition page on Stats SA's census, no codebook read), shape + (2,822 wards, spatial structure), risk 0.

Womxn in Big Data (Zindi) asks to predict the percentage of female-headed households per area, a regression on census/survey-derived aggregate features (the original-source modality is often satellite/aggregate covariates). It is a real predictive regression task with a clear target, but such aggregate-area datasets tend to be small with limited rows. The record gives no size or feature details and the split regime (likely grouped/spatial) is unknown. A human must check row count after cleaning, feature provenance, and whether it is representative tabular ML; provisionally 2nd Tier.

---

Predict the percentage of female-headed households
