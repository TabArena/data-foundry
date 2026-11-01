---
unique_name: turkcell_radio_link_failure_prediction
name: Turkcell Radio Link Failure Prediction (ITU AI/ML in 5G Challenge 2021, ITU-ML5G-PS-012)
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 3
decision_markers:
- Needs extensive data wrangling
tags:
- AI-Filled (Verify)
- Non-IID (Temporal)
year: '2020'
domain: technology & internet
required_split:
- Temporal (NON-IID)
problem_type: Binary Classification
original_data_state: Database (or multiple to-be-joined tables)
source_links:
- https://github.com/Turkcell/ITU-AIMLin5GChallenge-2021
- https://github.com/ITU-AI-ML-in-5G-Challenge/Challenge_Archive/tree/main/2021
- https://doi.org/10.1016/j.compeleceng.2022.107742
- https://arxiv.org/abs/2407.05197
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 3: Turkcell's own microwave-link KPIs and weather forecasts, released for the ITU AI/ML in 5G Challenge, with a failure flag for each link on the next day (and the next five days); real operator data and a direct reliability decision, but six tables to join and about 0.06% positives.
- Source: Turkcell for the ITU AI/ML in 5G Challenge, first as ITU-ML5G-PS-036 "Radio Link Failure Prediction Challenge" (deck by Salih Ergüt, Turkcell, 22 July 2020: "Given the region-wise, historical data sets on radio link (RL) performance and weather forecast predict the RL failures to assess risks"), then on GitHub (Turkcell/ITU-AIMLin5GChallenge-2021: "we have compiled and anonymised region-wise data which corresponds to weather forecasts, and RLFs derived from our networks"); data paper Aktaş, Alemdar and Ergüt, Computers & Electrical Engineering 99:107742, 2022. As published: `RegionA.zip` with `rl-kpis.tsv` (daily KPIs and configuration per link: datetime, site_id, mlid, type, tip, card_type, freq_band, severaly_error_second, error_second, unavail_second, bbe, rxlevmax, capacity, modulation, rlf, ...), `rl-sites.tsv`, `met-forecast.tsv` (5-day forecasts, "Recorded twice a day"), `met-real.tsv` (hourly observations), `met-stations.tsv`, `distances.tsv` (station-to-site distances); a test archive for 2021-01-25 to 2021-02-13 with a query file for 2021-02-13 whose labels are not shipped. Turkcell's example notebook (`TurkcellExampleProject.ipynb`) builds the labels from `rlf`: 1,992,986 link-days from 2018-12-31, 1,204 positive for "1-day-predict" (rlf at T+1) and 5,159 for "5-day-predict" (any rlf in T+1 to T+5). RLF is "an anomalous condition of microwave LOS links defined by Turkcell using thresholds on standardized BBE and Unavailable Seconds" KPIs (IEC_Research slides, ITU 2020).
- Use case: Turkcell's network operations, each day, flag backhaul links likely to fail from the weather forecast and the link's KPIs, to assess the risk; the deck leaves the action open ("What actions can we take when we know the failures ahead of time? Tilt, modulation, redundancy, etc.?"); fit direct for the prediction; regime temporal: known links predicted for the coming days (USE-10), with the link as the unit of repeated rows.
- Siblings and duplicates: `row_1040` (the ITU challenge archive, `TBD -> 2nd Tier`, priority 1, whose screening names this challenge as the first worth a record of its own); `qos_prediction_challenge` (`TBD -> Yes`) and `5g_energy_consumption` (`Yes`) are other ITU challenges with other tasks. No duplicate. External collections: none found.
- Better data: found as a related task next to `row_1040` (the run's Assessment); no further search this round.
- Papers and pages: Aktaş et al. 2022 (the data paper; not read, paywalled); the 2020 deck (itu.int, ITU-AI-Challenge-Turkcell-RLF-Salih-Ergüt-v1.0.pdf) and the IEC_Research team's 2020 slides (a depth-7 decision tree with class weights; F1 of the RLF class 0.09 and 0.01 on two sets); arXiv 2407.05197 (a transformer RLF framework on Turkcell data).
- Metric: Turkcell's example notebook scores the F1 of the RLF class (`precision_recall_fscore_support(..., average="binary")`, "focus only True class") for the 1-day and the 5-day label; the 2020 deck's evaluation slide says "average squared-root error obtained along with all the predictions compared to the actual result in each type of deployment", which does not fit a binary label (it reads as template text). If the 2021 rules confirm F1, it is the competition's metric (MET-4), on hard labels with the threshold left to the model (MET-6); inputs none.
- Risks for /add-dataset: six tables and a spatial join (site to the nearest weather station through `distances.tsv`; only forecasts issued before the predicted day, LEAK); today's `rlf`, `bbe` and `unavail_second` are the lagged target, so the panel needs the naive-profile test (TP-10, SEL-11); about 0.06% positives for the 1-day label (TP-5, TP-9 per test window); two horizons, one to ship (CLEAN-18); the query day's labels are not public, so the split comes from the labelled history; whether the 2020 and 2021 releases hold the same region and period is not settled.
- Not checked: the Computers & Electrical Engineering paper's text; the 2021 problem statement and its scoring page (not found; the web search budget ran out); the row count of the test archive.
- Priority: gap 0 (technology & internet has 4 accepted, binary and temporal not thin), use case + (the operator publishes its own failure-risk task, fit direct), source + (the operator's release with a data paper), shape + (about 2 million link-days, mixed types, dated), risk - (heavy joins, rare positives, lagged target).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through a related task next to `row_1040`.
- as published: Anonymised region-wise live-network data: rl-kpis.tsv (daily radio link KPIs and configuration), rl-sites.tsv, met-forecast.tsv (5-day weather forecasts), met-real.tsv, met-stations.tsv, ...; target: Whether a radio link has at least one failure in the next day (and in the following 5 days); scored with F1; access: open.
- Why: row_1040 is the ITU archive, not a dataset; its screening names Radio Link Failure Prediction as the first challenge worth a record of its own. Real operator data, a binary target acted on, ex-ante inputs (weather forecasts), traceable to a paper
- Adds: A telecom reliability task with real network data, temporal and grouped by link; no record yet. Risks: joins across six tables and region alignment (wrangling), the F1 threshold, and the forecasting question (event per link-day from forecasts, not a series)
