---
unique_name: global_data_on_sustainable_energy_2000_2020
name: Global Data on Sustainable Energy (2000-2020)
checked_by:
- AI (UNVERIFIED)
suggestion: 'No'
decision_markers:
- No Good Target / Scientific Discovery
- Time-series (Forecasting)
tags:
- 2nd Tier / Scientific Discovery
- Non-IID (Temporal)
- AI-Filled (Verify)
collections:
- New (BeyondArena)
domain: environmental science & climate
required_split:
- Temporal (NON-IID)
problem_type: TBD
original_data_state: One Table
source_links:
- https://www.kaggle.com/datasets/anshtanwar/global-data-on-sustainable-energy
source_row: 851
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-22):** `No` (`No Good Target / Scientific Discovery`, `Time-series (Forecasting)`; SEL-3, SEL-10): a country-year panel compiled for exploration; the source names no target, and the predictive uses it lists are forecasts of a series.
- Source: Kaggle `anshtanwar/global-data-on-sustainable-energy`, uploaded 2023-08-19 by Ansh Tanwar; one CSV (514 KB), one row per country and year 2000-2020 (about 176 countries, so about 3,600 rows) x 21 indicators (access to electricity, clean cooking fuels, renewable capacity per capita, financial flows, renewable share, electricity by source, energy per capita, energy intensity, CO2 per capita, GDP growth, GDP per capita, density, land area, latitude, longitude). The card names no upstream source; the indicators are World Bank / IEA / IRENA / Our World in Data series (PROV-8: the first publishers are those agencies, not this upload).
- The card: "Explore 20-year Insights on Sustainable Energy", "gain profound insights into global energy consumption patterns over time"; its "Potential Use cases" are "Energy Consumption Prediction: Predict future energy usage" and "Carbon Emission Forecasting: Forecast CO2 emissions", plus analysis and tracking items (SDG 7 tracking, equity analysis).
- Use case: none with an actor and a decision at a prediction point; any target picked from the indicators is an identity or near-identity of others (electricity from renewables vs low-carbon share vs renewables share).
- Siblings and duplicates: none among the records (checked by name and slug); `sustainable_development_goals_sdgs_text_classification_challenge` is unrelated. External collections: none found.
- If the checker refutes it: `TBD -> 2nd Tier`, priority 1 (gap -, use case -, source -, shape -; risk: targets that are sums or shares of other columns).
- Reject check (AI, 2026-10-22): stands. SEL-3: the card is an exploration compilation ("Explore 20-year Insights on Sustainable Energy") with no target, and its only predictive uses are SEL-10 forecasts ("Predict future energy usage", "Forecast CO2 emissions") (https://www.kaggle.com/datasets/anshtanwar/global-data-on-sustainable-energy); any target picked from the indicators would be ours, and several are shares/sums of others.

Kaggle country-year panel of sustainable-energy indicators (2000-2020), already tagged 2nd Tier / Scientific Discovery and Non-IID (temporal). It is an aggregated descriptive panel with no canonical predictive target, and it is small (roughly a couple thousand country-year rows), so it leans toward scientific-discovery rather than a genuine predictive task. One could contrive a target (e.g. renewable share, CO2), but this risks leakage among the indicators and is not clearly representative. A human must decide whether any non-leaky target and adequate size exist; keep in 2nd tier.
