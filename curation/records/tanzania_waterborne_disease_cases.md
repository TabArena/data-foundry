---
unique_name: tanzania_waterborne_disease_cases
name: 'Tanzania Climate-Sensitive Waterborne Diseases Dataset for Predictive Machine Learning: A Comprehensive Five-Year Analysis of Health, ...'
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 2
tags:
- AI-Filled (Verify)
original_source: Other
year: '2025'
domain: medical & healthcare
problem_type: Regression
original_data_state: Database (or multiple to-be-joined tables)
source_links:
- https://doi.org/10.5281/zenodo.14744372
- https://zenodo.org/records/14744372
- https://zindi.africa/competitions/outsmarting-outbreaks-challenge
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> 2nd Tier`, priority 2: Sokoine University's Zenodo release (2025, CC BY 4.0) of monthly waterborne-disease cases per health facility in anonymised Tanzanian districts, with water-source, toilet, waste and climate tables; very likely the data behind the Zindi challenge of `outsmarting_outbreaks_challenge`, with the same forecasting doubt (TP-10) and heavy joins.
- Source: Fue, Lyimo, Telemala, Materu and Kilatu (Sokoine University of Agriculture), "Tanzania Climate-Sensitive Waterborne Diseases Dataset for Predictive Machine Learning: A Comprehensive Five-Year Analysis of Health, Infrastructure, and Weather Data (2019-2023)", Zenodo 10.5281/zenodo.14744372, v1.0 of 2025-01-27, CC BY 4.0, funded by Wellcome and the Lacuna Fund. As published: 34 CSV files: disease cases per district for districts 1 to 4 (no case file listed for district 5), one row per facility (UUID), disease and month, with counts by sex (ME, KE, JUMLA) and age band and masked coordinates; water-source, toilet and waste-facility tables per district, raw and "climate embedded" ("Each data point ... was expanded to include a minimum of 60 entries to align with weather conditions over the 60 months", Copernicus variables). A preview of district 3 shows month codes YYMM from 1901 to 2404 (into 2024, past the title's 2023), some months with repeated rows, and malaria counts next to the waterborne diseases. No column dictionary on the page.
- Use case: as `outsmarting_outbreaks_challenge`: a district health office plans interventions and supplies per facility for the coming month; the Zenodo page names no actor (the Zindi page does); fit approximate, since the climate of the target month is not known ahead. Regime temporal (Zindi: train 2019-2022, test 2023).
- Siblings and duplicates: `outsmarting_outbreaks_challenge` (`TBD -> 2nd Tier`, priority 2): the same diseases, side tables and university; Zindi masked the locations and withheld the 2023 targets, Zenodo names the data managers and ships the targets. Neither page states the link. A newer release of the same source (PROV-6): the curator decides which one enters. External collections: none found.
- Better data: found as better data for `outsmarting_outbreaks_challenge`.
- Papers and pages: the Zenodo record; the Zindi challenge pages (SUA with IRCAI and AWS, December 2024 to January 2025); Lyimo et al. 2025, Front. Artif. Intell. (10.3389/frai.2025.1597727), the same group's survey of environmental health officers on ML for these diseases, not a model on this data.
- Metric: none on the Zenodo page; the Zindi challenge on the same task scored mean absolute error (its Evaluation page, as read for `outsmarting_outbreaks_challenge`), a competition metric (MET-4) if the task is kept as Zindi framed it; inputs none.
- Risks for /add-dataset: monthly counts per facility are forecasting unless a model on the features beats each facility's naive profile (SEL-10, SEL-11, TP-10); joins by masked coordinates and month across many files; the month codes, repeated months and the missing district 5 case file to explain; the climate of the target month is a future value (LEAK); zero-heavy counts; the target to define (which diseases, a total or per disease).
- Priority: gap 0 (medical, regression and temporal not thin), use case 0 (not named by this source), source + (a university release with named data managers and a licence, no codebook), shape + (a facility-month panel with side tables), risk - (forecasting doubt, joins).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through better data for `outsmarting_outbreaks_challenge`.
- as published: 5 anonymised Tanzanian districts, monthly 2019-2023 (60 months); per-district disease-case files (typhoid, amoebiasis/dysentery, diarrhoea by dehydration severity, schistosomiasis, intestinal worms) ...; target: monthly waterborne-disease case count per health facility (and disease); access: open.
- Why: Same diseases, the same side tables (water sources, toilets, waste management, climate) and the same SUA team as the Zindi SUA Outsmarting Outbreaks challenge. It is very likely the data behind the challenge, published by its collectors under CC-BY-4.0. The link between the two was not confirmed on either page
- Adds: A traceable first publication with named authors and a licence; the 2023 targets, which Zindi withholds in Test.csv; five districts over 2019-2023. The forecasting doubt (TP-10) and the heavy joins stay
- A newer release of the same source as the record(s) named above (PROV-6): the curator decides which one enters.
