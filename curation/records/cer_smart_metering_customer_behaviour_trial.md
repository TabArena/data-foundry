---
unique_name: cer_smart_metering_customer_behaviour_trial
name: 'CER Smart Metering Project: Electricity Customer Behaviour Trial, 2009-2010 (Ireland)'
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 2
decision_markers:
- No Good Target (yet)
- Needs extensive data wrangling
tags:
- AI-Filled (Verify)
original_source: Other
original_data_state: Database (or multiple to-be-joined tables)
source_links:
- https://www.ucd.ie/issda/data/commissionforenergyregulationcer/
- https://doi.org/10.1049/ic.2010.0051
- https://doi.org/10.7929/ISSDA/BX59EU
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> 2nd Tier`, priority 2: a real randomized tariff trial of about 5,000 Irish homes and businesses, run to measure the average effect of time-of-use tariffs; no prediction target ships, and either possible task must be built from half-hourly meter series.
- Source: Commission for Energy Regulation (CER), Smart Metering Electricity Customer Behaviour Trials, 2009-2010, archived by ISSDA (UCD), doi 10.7929/ISSDA/BX59EU (DataCite lists ISSDA, 2025). DataCite: "The purpose of the trials was to assess the impact on consumer's electricity consumption in order to inform the cost-benefit analysis for a national rollout", with "over 5,000 Irish homes and businesses participating". As published (b2find and DataCite; the ISSDA page answered 403): half-hourly smart-meter readings, pre- and post-trial surveys (socio-demographics, dwelling, appliances) and the allocation to tariff and stimulus groups with a control group; files and row counts not checked.
- Use case: the record's framing (a supplier, before enrolling a household in a time-of-use tariff, predicts how much it will cut) is ours; a household's change mixes the tariff effect with ordinary year-to-year variation, an uplift question the trial answers only on average. The established ML use of this data predicts survey answers (occupants, employment, dwelling type) from the household's load curve, so a utility can target efficiency offers (Beckel et al. 2014; Applied Sciences 8(9):1654, 2018), a time-series classification on features extracted from the meter series. Fit approximate either way; regime IID over households.
- Siblings and duplicates: `personalized_energy_marketing_analytics_dataset` (`No`, AHDS: generated rows) is the record it was found for; no other record holds the CER trial (grep over curation/records for CER, ISSDA, Ireland, smart meter). External collections: none known.
- Better data: found as better data for `personalized_energy_marketing_analytics_dataset`; no further search this round.
- Papers and pages: Mannion, "Smart metering project", IET Seminar on Smart Metering 2010 (doi 10.1049/ic.2010.0051); the CER trial findings reports (2011, not read); Beckel et al. 2014 and the Applied Sciences 2018 study (accuracy about 90%, AUC 0.82), both known from a search summary only.
- Metric: none found for a prediction task (DataCite description; the ISSDA page answered 403). The household-characteristic papers report accuracy, a threshold metric with no fixed threshold (MET-6), so the fallback: `rmse` for a consumption change, `roc_auc` or `log_loss` for a survey attribute; inputs none.
- Risks for /add-dataset: the target has to be chosen and built (SEL-3, USE-5); features come from half-hourly series, so the time-series concern applies (SEL-12); post-trial survey answers come after the enrolment decision (USE-3); access is by application, and "ISSDA may only supply data for use in the EEA and adequacy decision countries" (b2find), a note and no criterion (EV-4).
- Priority: gap 0, use case 0 (the source names no actor or prediction), source +, shape + (about 4,000 residential households with survey and allocation), risk - (target to build from series, heavy wrangling).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through better data for `personalized_energy_marketing_analytics_dataset`.
- as published: about 5,000 Irish homes and businesses (some 4,000+ residential) with half-hourly meter readings over a benchmark period (Jul-Dec 2009) and the trial year (2010), residential pre- and post-trial ...; target: per-household change in consumption (total or peak, %) from the benchmark period to the trial, derived from the meter readings; access: request.
- Why: the fake ziya07 set has 'Energy Usage Reduction (%)' as target with demographics, consumption, pricing plan and marketing-engagement features; the CER trial is the real randomized trial of exactly those levers, widely used in research
- Adds: real households in a randomized trial with controls, real survey demographics and tariff/stimulus assignment, instead of generated rows
