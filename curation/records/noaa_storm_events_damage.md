---
unique_name: noaa_storm_events_damage
name: NOAA NCEI Storm Events Database, property damage per storm event
checked_by:
- Andrej
data_foundry_status:
- WIP (DF)
claimed_by: Lennart
suggestion: 'Yes'
priority: 2
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

CC (2026-11-06, Lennart): decision D13 of the exposure study (#51; issue 6 of the folder's REVIEW.md): `duration_hours` is blank for Strong Wind and Heavy Rain, whose span NWSI 10-1605 App. A draws by the damage (Sec. 45, 21), and kept with a `Potential leak, kept on purpose:` note for Thunderstorm Wind, High Wind, Coastal Flood, Lakeshore Flood and Storm Surge/Tide, which it times by the damage or a wind or flooding criterion (Sec. 46, 24, 4, 27, 44), under the new LEAK-10 / LEAK-37 Cases row on spans the outcome sets. Supersedes the definition Andrej shipped on 2026-11-03 (lines above), which blanked only the tornado durations, as the column audit of 2026-11-01 had read the begin and end of Thunderstorm Wind alone and judged the other spans first-report facts: the study of 2026-11-05 read App. A for every type and measured the column's worth on the seven damage-timed types (+0.02 to +0.04 RMSLE, trained from 2016). On the shipped splits (untuned LightGBM, 4 bagging seeds) it is +0.013 to +0.021 on those rows, all of it on the five kept types (+0.012 to +0.021) and none on Strong Wind and Heavy Rain (-0.009 to -0.046). The notes gain the exposure paragraph: no exposure in the source; county population does not scale with the damage (Spearman -0.14 to +0.05 among positive entries), so no offset; storms whose entries share one figure hold round office values, not split totals.

**Assessment (AI, 2026-11-06):** the re-review panel's changes that need no decision are in the definition (`dataset check`: 0 errors, 0 warnings). The 51 Seiche durations are blank by type (NWSI 10-1605 App. A, Sec. 41, begins a seiche at shoreline flooding "resulting in a fatality, injury or damage"). The kept-span note gives the measured worth, -0.01 to +0.08 RMSLE on the five kept types' test rows depending on the model (15 fits on the shipped splits, median about +0.03), and the share `magnitude_type` locates (241,523 of the 318,813 rows: the EG and ES wind entries and Thunderstorm Wind measured under 50 kt; open as issue 7 of the folder's REVIEW.md); it names Dust Storm and Volcanic Ashfall as kept with a note and records Flood, Flash Flood, Hurricane (Typhoon) and Tropical Storm as judged outcome-free (a threat to life or property; the storm's direct effects, Sec. 25 and 49; the "damage or" wording the panel quoted for the last two is that of their marine types, Sec. 34 and 39). The metric reason and the reason for dropping the unassessed hazards name the planner; the task summary says the rows are the events with a damage entry (an office leaves 0% to 98% of its events blank) and gives 4.5-5.0% of the test rows for the types entered only with damage; the counts left from before issue 2's drop are restated on the shipped rows. In the CC line of 2026-11-06 above, "the study of 2026-11-05 read App. A for every type" is superseded (that reading missed Seiche, Dust Storm and Volcanic Ashfall), and its +0.012 to +0.021 on the five kept types is the low end of the measured range, the mean of 4 bagging seeds of untuned LightGBM, not an upper bound.

**Assessment (AI, 2026-11-06):** review panel (full, re-review under LEAK-41, MET-14 to MET-16): ship after changes (the text changes and the Seiche blank are made, line above); disputed: issue 7, blank `duration_hours` on the 241,523 wind entries `magnitude_type` locates as timed by the damage (the advocate keeps them as first-report times, the critic blanks them as Strong Wind's; the mediator's 4-seed rerun met the tie-breaker both set, +0.023 to +0.031 RMSLE on those rows under a stronger LightGBM with 12 of 12 seeds, so B, the blank, is recommended), and issue 8, RMSLE or the mean Tweedie deviance at power 1.5 on the dollars (they pick different models in 3 of 3 windows; A, RMSLE, recommended, a weighing call); for the curator: issues 7, 8 and 9 (the leftover `No Good Target / Scientific Discovery` marker). The LEAK-10 amendment for spans that the panel asked for is cross-dataset item X4; Andrej's release of D13 is not needed, as Lennart decided D13 as the main reviewer of this round.

**Assessment (AI, 2026-11-06):** the `No Good Target / Scientific Discovery` marker is removed: screening left it as an open concern, and review issue 5 (Andrej, 2026-11-03) settled it (the task is real, the planner's use case of Diaz and Joseph 2019). The review editor's pass withdrew review issue 9, which asked about it, before the curator saw it; for the curator: review issues 7 and 8.

CC (2026-11-08, Lennart): review issue 7, B ("Blank these rows"): `duration_hours` is blank also on the EG and ES entries of Thunderstorm Wind and High Wind and on the Thunderstorm Wind entries measured under 50 kt (241,523 rows), whose span only the damage can have timed, as for Strong Wind; the note keeps the measured-wind, dust, ash and flood spans, with their worth measured again. Supersedes in part Lennart's D13 (CC of 2026-11-06 above), which kept the duration of every Thunderstorm Wind and High Wind entry with a note.

**Assessment (AI, 2026-11-08):** issue 7, B is in the definition. The issue's count holds: 241,523 rows (241,088 EG or ES entries of Thunderstorm Wind and High Wind, 435 Thunderstorm Wind entries measured under 50 kt); `duration_hours` is now blank on 304,268 rows (36.1%), exactly where `event_type`, `magnitude_type` and `wind_speed_kt` say so. Measured on the shipped splits with the issue's models (LightGBM of 400 trees and of 1,500 trees with 127 leaves, 4 bagging seeds each) and the re-review's 5 set-ups: the blank costs +0.023 to +0.036 RMSLE on its rows under the larger model (12 of 12 seeds) and +0.008 to +0.032 under the smaller, close to the issue's table. What stays with the note (78,843 rows: the measured wind entries, Coastal Flood, Lakeshore Flood, Storm Surge/Tide, Dust Storm, Volcanic Ashfall) is worth -0.02 to +0.12 RMSLE on its test rows (15 fits, median about +0.04). By type, the measured Thunderstorm Wind spans gain in 30 of 30 fits (+0.03 to +0.18 on their rows, more than the blanked spans carried); High Wind and Coastal Flood show no consistent sign, Dust Storm no gain, and Lakeshore Flood, Storm Surge/Tide and Volcanic Ashfall have too few test rows; on Flood and Flash Flood the column is worth -0.09 to +0.09, positive in 2023-2024 and negative in 2025. Leak probes: all features R^2 0.352 (0.362 before), 0.348 without the column; the duration's missing indicator alone 0.192, `event_type` alone 0.185; test rows with an exact feature copy in training 16.2% (14.8% before). `dataset check`: 0 errors, 0 warnings; README regenerated (5,402 duplicate rows, from 5,370). `changes` names the new blank; `known` keeps "unless damage alone timed it", which covers it (the field is at its 70-word limit). Also corrected: the note's example of the longest spans, Drought (dropped by issue 2), is now Flood and Wildfire.

CC (2026-11-08, Lennart): review issue 8, B ("The Tweedie deviance on the dollars"): the target ships in dollars (`property_damage_usd`) and is scored by the mean Tweedie deviance at power 1.5, since the planner sums expected dollars, which RMSLE does not score; start from the right metric for the task and set aside earlier calls that do not match it. Supersedes Andrej's RMSLE: issue 3 (A) of 2026-11-03, kept for the earlier triage actor, and "the declared metric, RMSLE from context, checked" (CC of 2026-11-03 above), given when issue 5 made the planner the actor.

**Assessment (AI, 2026-11-08):** issue 8, B is in the definition: the target in dollars with no `target_transform` (CLEAN-16), `Metric.from_context("mean_tweedie_deviance")` at power 1.5 with `min_prediction` $1. The floor follows MET-13: the smallest positive training mean per event type on the shipped splits is $909 (Dense Smoke, 143 entries, 2 with damage; 33 of the 34 types have a positive mean, Volcanic Ashfall is $0 in every entry), two orders below it is $9.09, rounded down to a power of ten as the collection's other floors: $1, which is also more than two orders below every type with at least 500 entries (Astronomical Low Tide, $1,526). Under the declared metric the task probe flags `no_signal`, `drift_baseline` and `unstable`: its families, fitted by squared error on the dollars, lose to the training mean (3,866; random forest 5,796; linear and LightGBM above 100,000 with 43.8% of their predictions at the floor). LightGBM fitted with the Tweedie loss at 100 trees scores 4,108-5,327, 2,048-2,453 and 788-838 (2023, 2024, 2025) against 4,453, 4,216 and 2,929 for the training mean and 2,660, 2,301 and 1,740 for the mean per event type; 400 and 1,500 trees score worse; 0% of its predictions sit at the floor (5.6-8.1% at 400 trees). The duration kept with a note (78,843 rows) has no consistent worth under the deviance (-41% to +99% of the deviance on its rows over the 15 fits of the re-review's set-ups, median -5%; the measured Thunderstorm Wind spans positive in 35 of 45 fits), while the Flood and Flash Flood durations carry much of a model's skill (blanking them raises the deviance on those rows in 44 of 45 fits, by 24% to 80% under 100 trees). The scorer of the definition matches the measurement's deviance exactly. `dataset check`: 0 errors, 0 warnings; README regenerated.

**Assessment (AI, 2026-11-08):** issue 8's option C measured after the change, for the curator's signal question (two new open issues in the folder's REVIEW.md). LightGBM with the Tweedie loss at power 1.5, tuned per window (24 configurations, early stopping on the last 12 months of the training side, refit, 3 seeds), scores the declared deviance 3,463, 2,044 and 962 (2023, 2024, 2025) against 4,453, 4,216 and 2,929 for the training mean and 2,660, 2,301 and 1,740 for the mean per event type: it beats the per-type mean in 2024 (-11%, 2.0 bootstrap SEs over test rows, 0.8 over test days) and 2025 (-45%, 26 and 18 SEs) and loses in 2023 within noise (+30%, SE 1,580 for a difference of +802); a Tweedie GLM on event type and month beats the per-type mean in all three windows (-4%, -7%, -8%). Alternatives on their own scores: with the damage capped at $10M (the cap binds on 1,761 entries and removes 87% of the dollars) the tuned model beats the per-type mean in every window and seed (-18% to -32%); at power 1.7 or 1.9 the signal stays uneven; under RMSLE untuned LightGBM scores 2.72 to 2.96 against 3.62 to 3.85 for the per-type mean of the log. Issue 10 asks whether the task keeps the deviance on the dollars (A, recommended under TP-2), returns to RMSLE, caps the damage, or retires. The Flash Flood duration carries much of the skill under the deviance (blanking it raises the deviance on its rows by 102%, 93% and 31%, and on all rows by 9%, 27% and 16%; Flood 43%, 0% and 9%), and one of its four onsets in NWSI 10-1605 Sec. 14 is water that "comes in contact, flowing into, or causes damage to" a residence or public building; 6.8% of the Flash Flood narratives name water at or damage to a building. Issue 11 asks whether it moves to the kept-with-note spans (B, recommended) or is blanked.

CC (2026-11-08, Lennart): the declared metric (`mean_tweedie_deviance`, power 1.5, floor $1) is checked: his choice in issue 8 (B); issue 10 asks whether it leaves enough signal.

CC (2026-11-08, Lennart): review issue 10, A (as implemented): the mean Tweedie deviance on the dollars stays as shipped, with the signal stated in the notes; tuned Tweedie LightGBM beats the mean per event type in 2024 and 2025, and in 2023 the difference is within noise. The capped target ($10M) is a note, not shipped.

CC (2026-11-08, Lennart): review issue 11, B ("Option B: Flash Flood kept with a note."): the Flash Flood duration is no longer read as outcome-free but kept with a `Potential leak, kept on purpose:` note giving its worth on the declared metric, since one of its onsets in NWSI 10-1605 Sec. 14 is damage to a building; Flood, Hurricane (Typhoon) and Tropical Storm stay read as outcome-free. Supersedes, for Flash Flood, the reading recorded at the re-review of 2026-11-06 (AI, made without a decision).

**Assessment (AI, 2026-11-08):** issues 10 and 11 applied in the notes, no data change. The signal bullet gives the tuned results (3,463, 2,044 and 962 against 2,660, 2,301 and 1,740 for the mean per event type; bootstrap SE of the difference 1,580, 129 and 30 over test rows) and the capped variant as a note. The new Flash Flood bullet gives the Sec. 14 onset, the narrative shares (6.8% name water at or damage to a building, 36% a road, 10% a rescue or evacuation) and the worth on the declared metric (+102%, +93% and +31% of the deviance on its rows when blanked, +9%, +27% and +16% on all rows); the Flood worth (+43%, +0% and +9% on its rows) is stated with the outcome-free reading. `dataset check`: 0 errors, 0 warnings. No issue is open in the folder's REVIEW.md.

## Reference

NOAA National Centers for Environmental Information. Storm Events Database, bulk CSV files 1950-2026.
https://www.ncei.noaa.gov/pub/data/swdi/stormevents/csvfiles/ (format: Storm-Data-Bulk-csv-Format.pdf in the same directory).

National Weather Service (2021). Storm Data Preparation, NWSI 10-1605, 26 July 2021.
https://www.weather.gov/media/directives/010_pdfs/pd01016005curr.pdf

Lead: web search 2026-10-20 for zero-inflated regression candidates (not in the v4 workbook).
