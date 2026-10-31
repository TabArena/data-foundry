---
unique_name: london_passenger_mode_choice
name: London Passenger Mode Choice (LPMC)
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 5
tags:
- AI-Filled (Verify)
original_source: Website
year: '2018'
problem_type: Multiclass Classification
original_data_state: One Table
source_links:
- https://doi.org/10.1680/jsmic.17.00018
- https://transp-or.epfl.ch/data/lpmc.dat
- https://transp-or.epfl.ch/documents/technicalReports/CS_LPMC.pdf
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 5: the London Passenger Mode Choice dataset, 81,086 trips of 31,954 people in 17,616 households from Transport for London's travel diary survey (April 2012 to March 2015), each with the chosen mode (walk, cycle, public transport, drive) and the level of service of all four alternatives; a documented multiclass task built for the planner's mode-choice models, with survey years and households for a non-IID split.
- Source: Hillel, Elshafie and Jin, "Recreating passenger mode choice-sets for transport simulation: A case study of London, UK", Proceedings of the ICE, Smart Infrastructure and Construction 171(1):29-42 (2018, https://doi.org/10.1680/jsmic.17.00018; not readable here, ICE and CORE answered 403 or a bot wall); data and case study at EPFL's transport lab (https://transp-or.epfl.ch/data/lpmc.dat, file of 2019-10-24, previewed; https://transp-or.epfl.ch/documents/technicalReports/CS_LPMC.pdf, read). As published: one tab-separated table of 32 columns: ids (`trip_id`, `household_id`, `person_n`, `trip_n`), `travel_mode` (1 walk, 2 cycle, 3 public transport, 4 drive), purpose, fuel type, fare type, bus fare scale, `survey_year` and the travel date and start time, age, sex, licence, car ownership, straight-line distance, and the predicted durations, interchanges, costs and traffic variability of the four alternatives. "The approach uses an online journey planner to generate the routes for four transport modes"; "Expansion factors are provided for using the data for forecasting, though are not provided with the LPMC."
- Use case: the case study: "The objective was to be able to predict how people will react to changes to the transport network and conditions, to allow for more efficient transport network management and investment planning"; a transport planner, before a change to the network, predicts each traveller's mode from the options' times and costs. Fit direct for trip-level mode prediction (the level-of-service values are modelled, as in practice). Regime: temporal by survey year (the run's Assessment says Hillel's protocol trains on the first two years; not verified, paper unreadable), with households kept whole inside it (SPLIT-13); to settle.
- Siblings and duplicates: none (grep: mode choice, swissmetro, lpmc, travel mode). External collections: Biogeme's example data (https://biogeme.epfl.ch/) and the Zotero paper arXiv 2605.26559 ("Auditing and Fixing Economic Validity in Tabular Foundation Models for Discrete Choice", 2026, one of its two transport datasets), both moved here from the source links (PROV-12).
- Better data: from the curator's Zotero collection (item 201); no further search this round.
- Papers and pages: Hillel et al. 2018 (the data fusion and the models built on it); the case-study PDF (variable table, descriptive statistics); arXiv 2605.26559.
- Metric: none found in what could be read (the case-study PDF states none; the paper's evaluation section was not reachable), so the fallback `log_loss` for four classes (MET-1, MET-8), which also matches the log-likelihood that choice models are fit and compared on; check the paper's own criterion before adding. Inputs: none.
- Risks for /add-dataset: the paper's split and metric not read; trips of one person and household are correlated (SPLIT-29, keep households whole); level-of-service values come from a journey planner, not observation (a known approximation, no leak); licence "research and education" with a citation request (EV-4: no reason for a verdict).
- Priority: gap + (multiclass is thin; transport is a new domain), use case + (the source names the planner's decision), source + (a peer-reviewed paper and a variable codebook), shape + (81,086 trips, mixed features, years and households), no known risk.

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the curator's Zotero collection, item 201: "Auditing and Fixing Economic Validity in Tabular Foundation Models for Discrete Choice".
- as published: 81,086 trips by 31,954 people in 17,616 households, April 2012 - March 2015 (three survey years); 32 columns: trip purpose, date and start time, age, sex, licence, car ownership, fare type, distance ...; target: chosen travel mode: walk, cycle, public transport, drive (4 classes); access: open.
- Why: revealed-preference choices with level-of-service features known before the trip; the standard ML benchmark for mode choice; no record
- Adds: a transport mode-choice domain; household ids for grouped splits and survey years for a temporal split (Hillel's own protocol trains on the first two years). Level-of-service values are modelled from a journey planner, not observed; licence is 'research and education' with a citation request
