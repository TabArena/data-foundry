---
unique_name: pnwflights14
name: pnwflights14
checked_by:
- AI (UNVERIFIED)
suggestion: 'No'
decision_markers:
- Duplicate
tags:
- AI-Filled (Verify)
year: '2014'
domain: Other
required_split:
- Temporal (NON-IID)
problem_type: TBD
original_data_state: Database (or multiple to-be-joined tables)
source_links:
- https://github.com/ismayc/pnwflights14
source_row: 1027
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-22):** `TBD -> 2nd Tier`, priority 1: a 2014 teaching cut of the BTS on-time table for SEA and PDX, likely a duplicate of the flight-delay task aeolus already covers (PROV-6).
- Source: the R data package pnwflights14 by Chester Ismay and Hadley Wickham (GitHub, created 2015-08-13, CC0), "a modified version of Hadley Wickham's `nycflights13` package"; upstream the US DOT BTS on-time data and hourly airport weather; as published: `flights` (162,049 flights departing SEA and PDX in 2014) plus `weather`, `planes`, `airports`, `airlines` to join; no target named (the README: "To help understand what causes delays").
- Use case: an airline or passenger before departure predicts the arrival delay (the use case of aeolus); fit approximate (two airports, one year, a teaching package); regime temporal (one year of dated flights).
- Siblings and duplicates: `aeolus` (`Yes`, shipped as `aeolus_1m`, BTS 2016-2024 with weather), `airlines` (TBD -> Yes, CC asks whether it duplicates aeolus), `airlines_depdelay_10m` (assessment of 2026-10-22: a cut of the same BTS source); all end at the BTS on-time table; external collections: none known.
- Papers and pages: the package README and DESCRIPTION; used in ModernDive teaching material (not read); no paper.
- Metric: none found (README, DESCRIPTION; BTS publishes no prediction task), so the fallback (`rmse` for an arrival-delay regression or `roc_auc` for a 15-minute delay flag).
- Risks for /add-dataset: PROV-6 against aeolus first (a different year and region is not a distinct task by itself); `dep_delay`, `dep_time`, `air_time` and `arr_time` are known only after departure (LEAK); weather joined by the scheduled hour; the aeolus notes found delay minutes a weak regression target.
- Priority: gap 0, use case 0 (no actor named by the source), source 0 (a teaching package over BTS), shape + (162k flights, joins and a temporal structure), risk - (likely duplicate of aeolus).

Pacific Northwest 2014 flights data (analogous to the well-known nycflights13 teaching dataset), distributed as flights plus auxiliary tables (airlines/airports/weather). It supports standard tabular tasks such as flight delay classification or arrival-delay regression with a natural temporal split, and is large and real-world. Some joining and target definition is needed, and the standard departure-time leakage must be avoided. Suggest TBD -> Yes; a human must pick the non-leaking target (e.g. arrival delay) and confirm usable size after cleaning.

**Assessment (AI, 2026-10-21):** aeolus (BTS on-time flights 2016-2024 with hourly weather at both airports, a temporal task in the TabArena v0.2 working copy as `aeolus_1m`) covers US flight delays, and pnwflights14 ends at the same BTS on-time table (aeolus review panel, precedent check, 2026-10-20). When this record is processed, judge it against aeolus under PROV-6: a second flight-delay task, or a duplicate of aeolus (a cut of one source without a distinct task), as for airlines and airlines_depdelay_10m.

CC (2026-10-26, Lennart): mark it a duplicate too (of aeolus, same source as airlines).

**Assessment (AI, 2026-10-26):** the R teaching package's flights of the two Pacific Northwest airports (Seattle, Portland) in 2014 come from the same BTS on-time table, a cut of one source without a distinct task. aeolus (`aeolus_1m`) and its rebuild aeolus_rebuilt take their flights from the same BTS Reporting Carrier On-Time Performance table and predict the delay from the schedule (PROV-6). `No` + `Duplicate`.
