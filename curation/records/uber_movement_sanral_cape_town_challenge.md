---
unique_name: uber_movement_sanral_cape_town_challenge
name: uber-movement-sanral-cape-town-challenge
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 2
decision_markers:
- Time-series (Forecasting)
tags:
- AI-Filled (Verify)
collections:
- New (BeyondArena)
original_source: Zindi
domain: technology & internet
required_split:
- Temporal (NON-IID)
problem_type: Regression
source_links:
- https://zindi.africa/competitions/uber-movement-sanral-cape-town-challenge
source_row: 931
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-22):** `TBD -> 2nd Tier`, priority 2: the proposed fast reject (SEL-10) did not hold in the reject check, so it stays a candidate with the doubt listed.
- Proposed reject (refuted): `No` (`Time-series (Forecasting)`, SEL-10): forecast, for every hour of a coming quarter and every 500 m freeway segment of Cape Town, whether an incident occurs, from the incident log of the three years before.
- Source: Zindi "Uber Movement SANRAL Cape Town Challenge" (2019-10-11 to 2020-02-10, 865 participants), incident data of SANRAL's Cape Town Freeway Management System and Uber Movement travel times, read through the Zindi API: "The aim of this challenge is to forecast if an incident will occur for each hour of each day per 500m road segment along the major roadways in Cape Town for 1 January 2019 to 31 March 2019". As published: `train.csv`, "all reported incidents from 1 January 2016 to 31 December 2018" (6 MB), road-segment shapefiles, a SANRAL zip (injuries, vehicles, vehicle-detector counts), Uber Movement aggregates; the submission grid is every hour x segment of the quarter (a 36 MB sample file).
- Use case: the authorities pre-position response "to anticipate where they will be needed next"; the rows to score are future hour-by-segment cells with no features of their own besides the segment, the time and aggregates; the target grid is built from the event log. That is a series of event counts per segment forecast over a three-month horizon (SEL-10), not a fixed task on rows with their own attributes (SEL-11).
- Siblings and duplicates: `uber_nairobi_ambulance_perambulation_challenge` (the same Uber Movement series, crash data of Nairobi; proposed `No` in this batch); `accra_mobility_prediction_hackathon` (AI, 2nd Tier, priority 1, a speed panel left to TP-10 because its page decided nothing).
- Metric: F1 on the 0/1 predictions per hour and segment (Zindi Evaluation page).
- Counterpoint for the checker: SEL-11 lets a forecasting-like panel in when it passes TP-10, which was not run here; what sets this apart from the accra precedent is the source's own words ("forecast ... for 1 January 2019 to 31 March 2019") and a training file that is only the event log, so the rows to predict exist only as a calendar grid.
- Reject check (AI, 2026-10-22): does not stand. The source publishes a fixed classification on rows ("forecast if an incident will occur for each hour of each day per 500m road segment", F1 on 0/1 per datetime x segment_id; api.zindi.world/v1/competitions/uber-movement-sanral-cape-town-challenge), with per-segment attributes (lanes, surface, length, condition), SANRAL vehicle counts, Uber travel times and weather. That is a forecasting-like panel, which SEL-11 lets in when TP-10 holds, and TP-10 was not run. The organiser-linked tutorial (datasciencecastnet.home.blog/2019/10/21/zindi-uberct-part-2-stepping-up/) builds a tabular model from segment and weather features without the incident records (no lag of the target), so TP-10 leg 2 is plausible. Unlike stock and appliances_energy_prediction, this is not a single series' next values. Deciding it needs the data, as for the accra_mobility_prediction_hackathon precedent.
- For /add-dataset: TBD -> 2nd Tier, priority 2 (use case + authorities pre-positioning response; shape + large segment x hour grid with segment attributes; risk - forecasting-like panel, very sparse positives, joins across shapefiles, SANRAL and Uber files). The add stage must run TP-10: does a model on the segment, time, weather and SANRAL features clearly beat each segment's naive incident rate (same hour/weekday profile from the year before) by F1 or a probabilistic metric on the shipped temporal windows? Check the winners' features for lagged incident counts per segment (leg 2). Also check the target is buildable from train.csv (incidents to hour x segment cells) and that the positive rate is not too thin for a stable metric; if TP-10 fails, `No` (SEL-10).

A Zindi challenge based on Uber Movement travel-time / traffic data for Cape Town (with SANRAL road sensor data), aimed at predicting traffic conditions / travel times over time. This is a spatio-temporal forecasting task over a horizon rather than a fixed predictive classification/regression problem, placing it out of scope as time-series forecasting. A human should confirm the precise target, but the forecasting nature makes a No appropriate.
