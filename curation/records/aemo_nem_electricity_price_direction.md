---
unique_name: aemo_nem_electricity_price_direction
name: 'AEMO National Electricity Market data: aggregated price and demand, and the MMSDM archive (NEMWEB)'
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 2
decision_markers:
- Time-series (Forecasting)
- Needs extensive data wrangling
tags:
- Non-IID (Temporal)
- AI-Filled (Verify)
required_split:
- Temporal (NON-IID)
problem_type: Binary Classification
source_links:
- https://nemweb.com.au/Data_Archive/Wholesale_Electricity/MMSDM/
- https://www.aemo.com.au/energy-systems/electricity/national-electricity-market-nem/data-nem/aggregated-data
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> 2nd Tier`, priority 2: AEMO's half-hourly NSW price and demand continue the Elec2 market from December 1998, so the label of `electricity` (the price up or down against its 24-hour moving average) could be rebuilt over 27 years; but no source defines a task on these data, and the label is a direction of the price series (SEL-10), the open question of `electricity` too.
- Source: Australian Energy Market Operator (AEMO; NEMMCO before 2009): aggregated price and demand per region (NSW1, VIC1, QLD1, SA1, TAS1), every 30 minutes from December 1998 and every 5 minutes since 2021 (from the scout: the AEMO page returned 403 here as it did for the scout); the MMSDM archive on NEMWEB (year folders 2009 to 2026, checked) holds the market tables, interconnector flows included. As published: time series, no prediction target.
- Use case: Harries (1999) motivates Elec2 with a market participant deciding when to buy or sell; the label "identifies the change of the price (UP or DOWN) in New South Wales" "relative to a moving average of the last 24 hours" (OpenML 151); fit approximate; regime temporal.
- Siblings and duplicates: `electricity` (Elec2, OpenML 151, May 1996 to December 1998; TBD -> Yes with `Time-series (Forecasting)` and `Wrong Domain / Source Modality`, Lennart) has the same market and quantities but another period and publisher, so it is no duplicate (PROV-4); its verdict decides this one. External collections: none for the AEMO data (Elec2 is in TabSTAR and a TabArena reject).
- Better data: found as better data for `electricity`; no further search this round.
- Papers and pages: Harries 1999 (UNSW report on Elec2); Zliobaite 2013, "How good is the Electricity benchmark for evaluating concept drift adaptation" (arXiv 1301.3524), on "a problem with testing adaptive classifiers on autocorrelated data".
- Metric: none found (AEMO publishes data, not a task; the Elec2 literature reports accuracy out of habit), so the fallback `roc_auc` if it is built (MET-1, MET-6).
- Risks for /add-dataset: scope first: a label computed from the price series against its own past moving average is either the next move of the series (forecasting, SEL-10) or, with the current price as a feature as in Elec2, close to a function of the inputs (SEL-5, TP-4); as a forecasting-like panel it needs TP-10 against the "same as the last period" profile, given the autocorrelation Zliobaite's note raises for Elec2; the target and the features are ours to build from raw tables (`Needs extensive data wrangling`); 5-minute settlement and market changes are real drift.
- Priority: gap 0, use case 0 (no source defines the task), source +, shape + (about 470,000 half-hours for NSW alone, from the scout), risk - (SEL-10 open, a constructed target).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through better data for `electricity`.
- as published: per NEM region (NSW1, VIC1, QLD1, SA1, TAS1): regional reference price and total demand every 30 minutes from December 1998 and every 5 minutes since 2021; interconnector flows in the MMSDM tables; ...; target: Elec2's label rebuilt: whether the NSW price goes up or down relative to its 24-hour moving average; the inputs of the same kind (NSW and VIC price and ...; access: open.
- Why: the same market, quantities and target as electricity, continued from where Elec2 stops (Elec2 covers May 1996 to December 1998)
- Adds: 27 more years, the raw (not hand-normalised) values with a documented source, the market expansion and later regime changes (5-minute settlement, renewables) as real drift; the record's Time-series (Forecasting) marker applies equally, so the curator's view of that task decides; the AEMO page returned 403 here, ...
