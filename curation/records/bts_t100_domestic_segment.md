---
unique_name: bts_t100_domestic_segment
name: T-100 Domestic Segment (U.S. Carriers), Air Carrier Statistics
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 2
decision_markers:
- No Good Target (yet)
tags:
- AI-Filled (Verify)
- Non-IID (Temporal)
original_source: GOV Website
required_split:
- Temporal (NON-IID)
original_data_state: One Table
source_links:
- https://www.transtats.bts.gov/Fields.asp?gnoyr_VQ=FIM
- https://www.transtats.bts.gov/Tables.asp?QO_VQ=EEE
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 2: the official BTS monthly route statistics behind the Kaggle `usa_airport_dataset`, with 17 more years and carrier and aircraft detail; the target is still open, as on that record, and the obvious one sits next to near-leaks.
- Source: Bureau of Transportation Statistics, US DOT, Air Carrier Statistics (Form 41 Traffic), table "T-100 Domestic Segment (U.S. Carriers)" (field list https://www.transtats.bts.gov/Fields.asp?gnoyr_VQ=FIM). As published: one row per carrier, origin, destination, aircraft type, service class and month; measures DepScheduled, DepPerformed, Payload, Seats, Passengers, Freight, Mail, Distance, RampTime, AirTime (the all-carriers table adds LoadFactor); carrier, airport, city-market and state codes; Year, Quarter, Month. Monthly since 1990 per the run's assessment (the TranStats pages read state no coverage); rows not counted (millions).
- Use case: BTS publishes statistics, not a task. The run's candidate: an airline or airport planning a route estimates its monthly passengers from distance, the city markets, carrier, aircraft and the scheduled capacity; fit approximate. Regime temporal (a monthly panel of routes).
- Siblings and duplicates: `usa_airport_dataset` (`TBD -> Yes`, `No Good Target (yet)`, Lennart): its Kaggle file (3.5 million rows, 1990-2009, credited to OpenFlights) looks like an aggregation of T-100 segments, inferred and not stated on its page; if confirmed, this is a newer release of the same source (PROV-6), and the curator decides which one enters. The verdict follows that record. BTS on-time records (`airlines`, `airlines_depdelay_10m`, `aeolus_rebuilt`) are other tables and tasks (PROV-7). External collections: none found.
- Better data: from the run's search, found as better data for `usa_airport_dataset`; no further search this round.
- Papers and pages: the TranStats table and field pages.
- Metric: none found (a statistics table; looked at the TranStats pages); fallback `rmse` once the target is fixed, likely on a log scale for counts (MET-3, MET-8).
- Risks for /add-dataset: the target is open (`No Good Target (yet)`, USE-1, USE-5); Seats, DepPerformed, Payload and LoadFactor nearly give Passengers away (LEAK-10), DepScheduled is the honest capacity input (USE-3); a route's future passengers are a series, so the task must pass TP-10 or be framed as a fixed task (SEL-10, SEL-11); cargo-only and charter rows with zero passengers (USE-7); a period and a row cap; the 2020 shock in a test window (SPLIT).
- Priority: gap 0 (temporal regression is not thin), use case 0 (BTS names none), source + (a federal agency with field definitions), shape + (millions of route-months, codes and measures over time), risk - (an open target with near-leaks beside it).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through better data for `usa_airport_dataset`.
- as published: one row per carrier, origin, destination, aircraft type and month; fields Passengers, Seats, DepPerformed, DepScheduled, Payload, Freight, Mail, Distance, AirTime and carrier/airport ids; millions ...; target: passengers carried on an airport pair in a month (the record's candidate target); access: open.
- Why: the Kaggle file (3.5 million rows, 1990-2009, credited to Jacob Perkins via OpenFlights, with Census populations) has the T-100 segment fields (passengers, seats, flights, distance per airport pair and month) and appears to aggregate T-100 (lineage inferred, not stated on the Kaggle page); this is the official, ...
- Adds: 17 more years (2010-2026, including the 2020 shock), carrier and aircraft type, scheduled departures, freight and mail; traceable to the agency instead of a Kaggle re-upload. The target question of the record stays open.
- A newer release of the same source as the record(s) named above (PROV-6): the curator decides which one enters.
