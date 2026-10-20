---
unique_name: noaa_storm_events_damage
name: NOAA NCEI Storm Events Database, property damage per storm event
checked_by:
- AI (UNVERIFIED)
suggestion: 'No'
decision_markers:
- No Good Target  / Scientific Discovery
- Data Quality Issue
tags:
- AI-Filled (Verify)
- Two-Regime Zeros
- Non-IID (Temporal)
original_source: GOV Website
domain: environmental science & climate
required_split:
- Temporal (NON-IID)
problem_type: Regression
original_data_state: Database (or multiple to-be-joined tables)
source_links:
- https://www.ncei.noaa.gov/pub/data/swdi/stormevents/csvfiles/
- https://www.ncei.noaa.gov/access/storm-events-database/
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. Drafted by an AI assistant on 2026-10-20 from a web search for zero-inflated regression candidates, the source pages and, where the notes say so, the downloaded data. A human must verify the suggestion, the metadata and the notes before relying on them.**

NOAA NCEI's Storm Events Database, the archive of NWS Storm Data: one row per event and county or zone, 1950-2026, in
yearly details, fatality and location files. The 2018-2024 details files hold 468,514 events x 51 columns. Candidate
target `DAMAGE_PROPERTY` (coded like "10.00K"): blank for 21.4%, $0 for 75.8% of the reported values; direct injuries
are 0 for 99.5%. The zeros are not observed absences. NWSI 10-1605 (July 2021), Sec. 2.7, p. 11: without an estimate
"the preparer has two choices: either check the "no information available" box, or make an estimate", except for
floods, which always get an amount (Flood and Flash Flood have no blanks here). A $0 thus mixes "no damage" with "not
estimated", and it depends on the office: for Thunderstorm Wind the share of $0 among reported values is 4% at the
10th percentile of 96 forecast offices and 98% at the 90th.

No: a reporting archive whose damage figure is a rough estimate by the preparer, with no exposure data, and whose zero
part is mostly reporting practice. Probe (temporal: train 2018-2022, test 2023-2024, reported events, 75.2% zero in
test): type, magnitude, place, month, hour, duration and source give ROC AUC 0.950 and R^2 0.48 on log1p among
positives, but event type and office alone give AUC 0.934. The narratives and the tornado EF rating and path (the
format notes rate tornadoes "based on the amount and type of damage") would leak. Licence: NOAA public data (not
re-read).

## Reference

NOAA National Centers for Environmental Information. Storm Events Database, bulk CSV files 1950-2026.
https://www.ncei.noaa.gov/pub/data/swdi/stormevents/csvfiles/ (format: Storm-Data-Bulk-csv-Format.pdf in the same directory).

National Weather Service (2021). Storm Data Preparation, NWSI 10-1605, 26 July 2021.
https://www.weather.gov/media/directives/010_pdfs/pd01016005curr.pdf

Lead: web search 2026-10-20 for zero-inflated regression candidates (not in the v4 workbook).
