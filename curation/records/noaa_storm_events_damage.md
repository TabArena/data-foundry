---
unique_name: noaa_storm_events_damage
name: NOAA NCEI Storm Events Database, property damage per storm event
checked_by:
- Andrej
data_foundry_status:
- WIP (DF)
claimed_by: Andrej
suggestion: 'Yes'
priority: 2
decision_markers:
- No Good Target / Scientific Discovery
tags:
- Two-Regime Zeros
- Non-IID (Temporal)
original_source: GOV Website
year: '2026'
domain: environmental science & climate
required_split:
- Temporal (NON-IID)
problem_type: Regression
original_data_state: Database (or multiple to-be-joined tables)
source_links:
- https://www.ncei.noaa.gov/pub/data/swdi/stormevents/csvfiles/
- https://www.ncei.noaa.gov/access/storm-events-database/
v2_path: datasets/_dev/tabarena-v0pt2/noaa_storm_events_damage/dataset.py
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. Drafted by an AI assistant on 2026-10-20 from a web search for zero-inflated regression candidates, the source pages and, where the notes say so, the downloaded data. A human must verify the suggestion, the metadata and the notes before relying on them.**

**Screening (AI, 2026-10-27):** `TBD -> 2nd Tier`, priority 2: the property damage of a reported storm event from its
type, magnitude, place and time is learnable (earlier probe ROC AUC 0.95 for any damage), but the archive was published
to describe events, and a $0 cannot be told apart from "no estimate made".
- Source: NOAA NCEI Storm Events Database, the archive of the NWS publication Storm Data from 1950, as yearly bulk CSV
  files (details, fatalities, locations). NWSI 10-1605 (26 July 2021), Sec. 1, p. 3: "the primary purpose of Storm Data
  is to accurately describe events, regardless of the impact on verification scores". As published (earlier AI triage,
  2026-10-20, measured): 468,514 events x 51 columns in the 2018-2024 details files, one row per event and county or
  zone; `DAMAGE_PROPERTY` coded like "10.00K", blank for 21.4% and $0 for 75.8% of the reported values.
- Target and zeros: NWSI 10-1605 Sec. 2.7, p. 11: "If this estimate is not available, then the preparer has two
  choices: either check the "no information available" box, or make an estimate. The lone exception is for flood
  events."; p. 12: "If the dollar amount of damage is unknown, or not available, check the "no information available"
  box." How that box is exported (blank or $0) is not documented in what was read. The $0 share is partly office
  practice: for Thunderstorm Wind it is 4% at the 10th percentile of 96 offices and 98% at the 90th (earlier triage,
  measured), and a StormTrack forum post reports a printed dash that became 0 in the database (third-party).
- Use case: none from the source; for example an insurer's catastrophe desk or a state emergency manager estimating
  the property damage of a reported event before claims or assessments arrive. Fit approximate: the label is the
  preparer's estimate, often from emergency managers, utilities and newspapers ("If the values provided are rough
  estimates, then this should be stated as such in the narrative", Sec. 2.7). Regime temporal: events are dated and a
  model serves later events (SPLIT-6); offices and counties recur (SPLIT-13).
- Siblings and duplicates: no other record of this database (searched storm, NCEI, tornado, hail);
  `ghcn_daily_precipitation` is another NCEI archive (rejected as having no target, pending the check). The closest
  precedents are event registers with an outcome column: `thailand_road_accident_register_2019_2022` and
  `chicago_traffic_crashes` (TBD -> Yes, AI drafts) against `us_accidents` (`No`, Lennart: "Just survey data for
  insights, not a predictive task"). External collections: none found; Hugging Face mirrors (e.g.
  `hydros-ou/ncei-storm-events`).
- Papers and pages: the NCEI database pages and the bulk CSV format document; NWSI 10-1605 (read).
- Metric: none found (NCEI database page, NWSI 10-1605, the bulk CSV format document): the fallback `rmse` (MET-1,
  MET-11), with the target's scale to settle when adding (MET-3).
- Risks for /add-dataset: the family's open policy question on coded zeros decides the target ($0 against blank,
  offices that rarely estimate); event narratives and the tornado EF rating and path are written from the damage and
  leak (LEAK-10); injuries, deaths and crop damage are recorded with it; the details and locations files to join.
  Earlier probe (train 2018-2022, test 2023-2024): event type and office alone give AUC 0.934 of the 0.950.
- Doubt: SEL-3, the archive was not published for a predictive task, which the earlier pass read as `No`; kept as a
  candidate on the event-register precedent, and its two markers stay as the open concerns.
- Priority: gap 0, use case 0 (no actor from the source), source + (NWS directive and format document), shape +
  (468,514 dated events, mixed feature types), risk - (coded zeros in the target, narrative and rating leaks).

**Assessment (AI, 2026-10-30):** The family's open question on coded and censored zeros is settled (Andrej, 2026-10-30,
policy question 2 of the zero-inflated review: "We don't care. We want to add any relevant predictive task, independent
if it is zero inflated or not"), so how the source codes its zeros is no reason for a No or a lower priority. $0 against
a blank damage field is a cleaning choice at /add-dataset. The verdict and priority stay: the narrative and rating leaks
are the screening's other risks.

CC (2026-10-30, Andrej): `Yes`, priority 2 (the AI screening had `TBD -> 2nd Tier`, priority 2; zero-inflated screening
review page).

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

**Assessment (AI, 2026-11-01):** added as `datasets/_dev/tabarena-v0pt2/noaa_storm_events_damage/` by /add-dataset with the full review panel; the open questions are in its `REVIEW.md`. Recommend `No` under LEAK-25 as written; the AI recommends amending LEAK-25 and shipping it as changed (its issue 1: a $0 entry mixes no damage with no estimate). Changes after the panel: wind speeds estimated from damage and tornado durations blanked, `hurricane_category` dropped, a 3-month gap. Corrections to the screening above: Diaz and Joseph (2019) exist ("Metric: none found" does not hold); the R^2 of 0.48 on the positives had `SOURCE` and the estimated speeds as inputs, 0.28-0.45 without; Flood and Flash Flood have 26 blanks, all in 2007. `year` is 2026 (the snapshot pinned; set now). Priority 2: gap 0, use case 0, source + (NOAA NCEI), shape +, risk - (recommendation not to ship).

CC (2026-11-02, Andrej): LEAK-25 amended as issue 1 proposed, and the dataset ships as changed: a mix whose recording follows a reporting unit shipped as a feature may be kept, case by case, with a note giving the unit's spread and drift and fit approximate, when the task keeps a measured signal beyond the reporting unit, the period and the place; the source's own 'not recorded' flag is dropped where it is used. `Data Quality Issue` leaves the record (nothing left to mark); the `Yes` stands.

CC (2026-11-03, Andrej): the hazards no one sends a damage assessor for are dropped (issue 2 (B), the domain practitioner's list: marine types, drought, heat, cold, fog, rip current, funnel cloud, waterspout, high surf): "I go with your suggested change". RMSLE stays (issue 3 (A)).

CC (2026-11-03, Andrej): no storm-level input (issue 4 (A)); counts of a storm's entries added no measurable signal and partly carry the label.

CC (2026-11-03, Andrej): issue 5, B ("I go with your change"): the use case is the planner's, as in Diaz and Joseph (2019): the damage of storm events estimated for disaster planning, not the triage of a storm's counties; data, split and metric unchanged.

CC (2026-11-03, Andrej): ship (review page verdict) with the planning use case of issue 5; the declared metric, RMSLE from context, checked.

## Reference

NOAA National Centers for Environmental Information. Storm Events Database, bulk CSV files 1950-2026.
https://www.ncei.noaa.gov/pub/data/swdi/stormevents/csvfiles/ (format: Storm-Data-Bulk-csv-Format.pdf in the same directory).

National Weather Service (2021). Storm Data Preparation, NWSI 10-1605, 26 July 2021.
https://www.weather.gov/media/directives/010_pdfs/pd01016005curr.pdf

Lead: web search 2026-10-20 for zero-inflated regression candidates (not in the v4 workbook).
