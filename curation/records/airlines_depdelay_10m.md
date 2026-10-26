---
unique_name: airlines_depdelay_10m
name: Airlines_DepDelay_10M
checked_by:
- AI (UNVERIFIED)
suggestion: 'Yes'
priority: 2
tags:
- Non-IID (Temporal)
- AI-Filled (Verify)
original_source: GOV Website
year: '2013'
domain: Other
required_split:
- Temporal (NON-IID)
problem_type: Regression
original_data_state: One Table
source_links:
- https://www.openml.org/search?type=data&id=42728
- https://www.transtats.bts.gov/
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Assessment (AI, 2026-10-22):** the `Yes` stays (it was written by the AI pass of 2026-06-24 from the workbook's "Temporal Tabular", commit bf95b671, so the curator may want to confirm it); priority 2. Recommend `TBD -> 2nd Tier` or `Duplicate` of the BTS flight-delay source already covered by aeolus; the curator has the call.
- Source: US DOT BTS on-time performance data (transtats.bts.gov); the OpenML upload 42728 (2020-11-18, no creator, no citation) says: "This is the first 10 million rows (and a subset of the columns) of this CSV file" of the raw data "years 1987-2013"; as published: 10,000,000 rows x 10 columns, target `DepDelay` ("in seconds" per the page), features Month, DayofMonth, DayOfWeek, CRSDepTime, CRSArrTime, UniqueCarrier, Origin, Dest, Distance; no missing values; one table.
- Use case: an airline or airport predicting a scheduled flight's departure delay before departure; the source names no actor or decision; fit approximate; regime temporal (a delay as a fixed task, SEL-11), but no Year column ships, and the first 10M rows of a file starting in October 1987 span about two years, so the order within a month is not recoverable across years (SPLIT-7).
- Siblings and duplicates: `airlines` (OpenML 1169, Data Expo 2009 / BTS, TBD -> Yes, CC "Requires temporal split ... only 7 features"); `aeolus` (`Yes`, shipped as `aeolus_1m`, BTS 2016-2024 with weather; its notes found the delay minutes a poor regression target: R² 0.01-0.02); `pnwflights14`. All end at the BTS on-time table, so this is a third cut of one source (PROV-6) unless it adds a distinct task; the Lennart CC of 2026-10-12 asks exactly this. External collections: OpenML (used in large-scale AutoML/GBDT benchmarks of the h2o airline data).
- Papers and pages: <https://www.openml.org/search?type=data&id=42728>; the 2009 ASA Data Expo for the 1987-2008 file.
- Metric: none found (the OpenML page states no task metric; BTS publishes no prediction task), so the fallback `rmse`.
- Risks for /add-dataset: no year column (SPLIT-7, SPLIT-8); the minutes target is dominated by a long tail (aeolus notes); 1987-1989 schedule data is outdated next to aeolus (`Outdated` worth considering); duplicate by source (PROV-6).
- Priority: gap - (domain Other, regression, temporal not thin), use case - (none named), source + (BTS), shape + (10M rows, mixed types), risk - (duplicate by source, no year).

The well-known OpenML 'Airlines_DepDelay_10M' dataset from US BTS flight records, predicting departure delay (regression) over ~10M rows. This is a large, genuine real-world tabular task already imported from the TabArena workbook with a verdict of 'Temporal Tabular' and multiple curators (Lennart, Andrej) agreeing a temporal split is required. It is clearly representative tabular ML with a meaningful target. A human should confirm it is not an unwanted duplicate of the smaller 'airlines' dataset and that the temporal split is correctly applied.

---

Imported from the TabArena curation workbook.

TabArena curation verdict: Temporal Tabular.

Might be an extended version of the airlines dataset (need to verify). For sure requires temporal split; might be a newer version as the data is younger

Potential issue: temporal

Lennart: temporal

Andrej: Temporal split

CC (2026-10-12, Lennart): aeolus (BTS on-time flights 2016-2024 with hourly weather at both airports, a temporal task in the TabArena v0.2 working copy as `aeolus_1m`) covers US flight delays. When this record is processed, decide whether it is a second flight-delay task or a duplicate of aeolus.
