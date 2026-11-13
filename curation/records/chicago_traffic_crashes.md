---
unique_name: chicago_traffic_crashes
name: Chicago Traffic Crashes - Crashes (CPD E-Crash)
checked_by:
- Myunghwan
- Lennart
data_foundry_status:
- WIP (Triage)
claimed_by: Myunghwan
suggestion: 'Yes'
priority: 3
decision_markers:
- Class-dependent Recording
tags:
- Non-IID (Temporal)
- 'Samples: Over Time'
- 'Time: Dated'
- 'Target: Revised Later'
- 'Features: Revised Later'
collections:
- New (BeyondArena)
original_source: GOV Website
year: '2026'
domain: social science
required_split:
- Temporal (NON-IID)
problem_type: Multiclass Classification
original_data_state: One Table
source_links:
- https://data.cityofchicago.org/Transportation/Traffic-Crashes-Crashes/85ca-t3if
- https://data.cityofchicago.org/resource/85ca-t3if.json
v2_path: datasets/_dev/tabarena-v0pt2/chicago_traffic_crashes/dataset.py
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-22):** `TBD -> Yes`, priority 3: Chicago Police crash reports (E-Crash) on the city portal, 1.1M crashes with the officer's injury classification, a thin domain; the target is ours to pick and many fields are recorded after the crash.
- Source: City of Chicago Data Portal, "Traffic Crashes - Crashes" (85ca-t3if), published by the City of Chicago, portal entry created 2017-10: "Data are shown as is from the electronic crash reporting system (E-Crash) at CPD"; "citywide data are not available until September 2017"; "About half of all crash reports, mostly minor crashes, are self-reported at the police district"; fields follow the IDOT Traffic Crash Report SR1050 (manual linked from the page). As published: one table, one row per crash, API count on 2026-10-22: 1,106,184 rows; sibling tables Vehicles and People join on CRASH_RECORD_ID. Targets on offer: MOST_SEVERE_INJURY ("Most severe injury sustained by any person involved in the crash") or CRASH_TYPE ("Injury and/or Tow Due to Crash or No Injury / Drive Away").
- Use case: no actor named by the source; the closest decision is dispatch or triage from the reported scene (location, time, road, weather, first crash type), or a city safety team prioritising locations; fit approximate. Regime temporal (SPLIT-6): yearly drift and the 2017 citywide roll-out break.
- Siblings and duplicates: `nyc_motor_vehicle_collisions` (AI `TBD -> Yes`, priority 3, same family), `nhtsa_crss_crash_severity` (AI `TBD -> Yes`, national sample), `us_accidents` (Lennart `No`: its Severity is a traffic-delay code; this record was opened as its injury counterpart). No duplicate found. External collections: none found.
- Papers and pages: the portal page and the SR1050 manual; Kaggle copies and notebooks, no competition or paper that defines a task.
- Metric: none found (the portal page, the SR1050 manual, no competition, no defining paper), so the fallback (`roc_auc` for injury vs none, `log_loss` for the injury classes) (MET-1, MET-8, MET-11).
- Risks for /add-dataset: INJURIES_*, DAMAGE, CRASH_TYPE (when the injury is the target), REPORT_TYPE, DATE_POLICE_NOTIFIED, PHOTOS_TAKEN_I, STATEMENTS_TAKEN_I are recorded after the crash and may encode the outcome (LEAK-10); PRIM/SEC_CONTRIBUTORY_CAUSE are the officer's judgement after the fact; self-reported desk reports are mostly minor crashes, so REPORT_TYPE nearly gives the class; records are amended later; pick one target and one regime (USE-5, SPLIT-6).
- Priority: gap + (social science thin, as for `nyc_motor_vehicle_collisions`), use case 0 (no actor named by the source), source + (the City documents the table and the form), shape + (1.1M rows, mixed categorical and numeric, temporal), risk - (post-crash fields, target to choose).

Chicago Data Portal, Chicago Police Department E-Crash system: "Data are shown as is from the electronic crash reporting system (E-Crash) at CPD, excluding any personally identifiable information"; citywide from September 2017, some districts from 2015. Socrata API on 2026-09-23: 1,096,581 crashes, 2013-03 to 2026-09-22. MOST_SEVERE_INJURY: no indication 935,239; nonincapacitating 88,254; reported not evident 51,886; incapacitating 17,675; fatal 1,142; missing 2,385. CRASH_TYPE: "INJURY AND / OR TOW DUE TO CRASH" 297,837 vs "NO INJURY / DRIVE AWAY" 798,744. Rich scene descriptors: posted speed limit, traffic control device, weather, lighting, first crash type, trafficway type, road surface, road defect, primary/secondary contributory cause, lat/lon, hit-and-run, intersection flag.

Task: MOST_SEVERE_INJURY (5 classes, heavy imbalance; collapse to injury vs none, 15%) or CRASH_TYPE (27% positive, but it mixes injury with tow-away). Drop outcome fields: DAMAGE, INJURIES_*, CRASH_TYPE when MOST_SEVERE_INJURY is the target, and the report/date-police-notified stamps. Best documented of the city registers; sibling Vehicles / People tables exist for a join. Temporal split, with the 2017 citywide roll-out as a reporting break. Data inspected only through API aggregates.

Opened 2026-09-23 as the injury-severity counterpart to `us_accidents` (rejected: its Severity is a traffic-delay code). Police crash reports carry the injury outcome the first-responder / crash-severity use case needs; the target is the standard one in road-safety research, unlike the gender target that sank `road_safety`.

CC (2026-10-29, Myunghwan): Myunghwan said "proceed" after the screening review: qualify MOST_SEVERE_INJURY as five source classes with log loss and chronological evaluation, using only defensible prediction-time inputs. Investigate newly reported crash prediction before injury status is established FIRST. Final inclusion/build are later decisions; return if validity requires a material task change.

CC (2026-10-29, Myunghwan): Investigate an explicitly approximate five-class injury task. Actual instruction: "let's investigate approximate. as far as features are not later reports or consequences of injuries, they might be acceptable. also clarify which features are timestamps". Underlying contemporaneous scene facts may be investigated despite retrospective collection; later administrative/reporting activity, injury consequences and outcome encodings remain excluded. Retain log loss and chronological evaluation. This supersedes the prior wait for proxy-investigation authorization; it is not final inclusion, warning acceptance, a direct dispatch claim or build authority.

**Assessment (AI, 2026-10-29):** Verdict: prepared as `chicago_traffic_crashes_1m` for curator review; recommend the repaired approximate five-class probability task, subject to final acceptance of its specific surrogate gaps. Validity: explicit initial-scene approximation, not validated dispatch or medical triage. Report/outcome/investigation fields excluded; weather, lighting, surface, control device and device condition withheld after independently replicated conditional completeness concerns (LEAK-10/38), without claiming injury caused every blank. Crash-date predictor uniformly floored to hours; original times define source copies and quarter cohorts (LEAK-13). Training notification eligibility precedes native 1M sampling; auxiliary notification is absent from predictors/scoring (SPLIT-9/LEAK-12). Finalization and amendment histories remain unavailable (USE-8/SPLIT-10). Provenance: official 2026-10-29 export,1,108,024 rows / 49 fields; all cached source cells independently matched. Source-key dedup removes 63 raw extras (62 labeled pre-October, 1 missing target), not every reduced-feature repeat. Returned frame 1,097,209 rows / 16 inputs; 453 exact reduced extras and 53 conflicting profiles are retained with source distinctions rather than invented entity keys. Value: all 9 quarters score five-class log loss,18–34 fatalities per test; three newest capped untuned probes give linear loss 0.508065 versus prior 0.613934, no flags. These are preliminary diagnostics, not tuned nine-fold or fatal-response validation. Quality: preserve sparse blanks, make impossible zero coordinates missing, retain qualified speed after recent zero-default refutation; historical N/Y requirements and 2015 codes remain uncertain. Bundle checks: 0 errors, 0 warnings, 2 information findings; no warning was accepted. Panel repairs and remaining decisions are documented in the folder review; final inclusion/build/publication remain undecided. This measured assessment supersedes earlier AI-unverified schema/target alternatives, while preserving their historical text and both attributed curator instructions. Priority 3: gap + (thin social science and multiclass), use case 0 (plausible approximate actor, not source-validated response workflow), source + (official documented City release), shape + (1,097,209 mixed-type temporal rows), risk - (retrospective scene/label history and historical coding).

CC (2026-10-29, Myunghwan): Keep the five discussed crash-condition fields in the approximate task. "This is a bit leaky in practice, but not "defintive". It seems OK to include?" Followed by "OK" and an explicit request to complete add-dataset and return for review-added-datasets. This settles these five fields only; final inclusion, other open issues, warning acceptance and build remain undecided.

**Assessment (AI, 2026-10-29):** Restored weather, lighting, road surface, traffic control device and device condition by curator direction. Availability-only any-injury AUC 0.555; three-quarter paired log loss 0.554416 with other 16 inputs, 0.551600 plus availability flags, 0.550105 plus actual fields. Association is real, causality and initial availability remain unverified. Earlier LEAK-10/38 exclusion recommendation remains historical evidence; retention is a directed dataset-specific departure, not causal clearance or a standing rule amendment. Affected checks and independent review are being refreshed before final scientific review.

**Assessment (AI, 2026-10-29):** Revised 21-input package qualified for added-review. The saved curator direction retains five condition fields with measured recording risk and a disclosed departure from the pinned LEAK-38/LEAK-10 treatment; no standing amendment is inferred. All 1,097,209 rows and all nine train/test identities match the previous recipe; original source-copy, notification and hourly-time repairs remain. Three newest native capped task probes: linear log loss 0.507504, prior 0.613934; flags []. Bundle checks: 0 errors, 1 unaccepted warning (physical DEVICE_CONDITION=MISSING), 2 informational reduced-profile findings. Reduced-frame exact extras are now 221, conflicting profiles 21; earlier453/53 counts belong to the 16-input recipe. Focused independent claim/column/precedent/mediator/editor review and refreshed probes preserved. Final inclusion and issues1-4 remain undecided. Priority 3: gap + (thin social science/multiclass), use case 0 (approximate response assessment), source + (official documented release), shape + (large mixed temporal task), risk - (recording, label-version and historical-code uncertainty).

CC (2026-10-29, Myunghwan): Issue 1: It's fine. Historical label is fine. This is a reasonable approximation. Issue 2: Yes, this is fine. We are now predicting more based on "closer to fact" information than "timely avaialbe" information. OK for this approximation. Issue 3: What decision do we need? does it matter? Issue 4: OK Issues 1/2/4 accepted; issue 3 remains discussion, not a final ship or build request. (Superseded 2026-11-05 for the actor: the use case is now a city road-safety analyst, issue 7; the closer-to-fact finalized inputs stay, as what that analyst works from.)

**Assessment (AI, 2026-10-29):** Applied accepted historical-label and closer-to-fact framing, preserved injury/report outcome exclusions, and accepted only dataset_missing_value_label for physical DEVICE_CONDITION=MISSING. Executable cleaning, features, labels, metric and split methods are unchanged. The speed question is whether to retain the posted road limit or remove/reconstruct it; recommend retaining it without guessed 99/default conversion. Recent matched zero rates weaken the specific proposed default mechanism; incremental predictive effect of dropping speed was not measured. Its coding caveat is not a demonstrated leakage defect. Issue 3 and overall inclusion remain open; settled choices are not reopened.

**Assessment (AI, 2026-10-29):** Review answers 1/2/4 applied and rechecked: closer-to-fact scene approximation and final-snapshot labels accepted, with the bounded SPLIT-10 exception recorded. Physical-MISSING warning accepted with its exact source reason; regenerated native report has 0 errors, 0 unaccepted warnings, 1 accepted warning and 2 informational findings. Independent module-AST review confirms unchanged model inputs, labels, cleaning, metric and all split/model-determining code; prior native model and data-identity evidence reused without refitting. Current issue 3 contains the speed question and answer, recommending retention without guessed code conversions. It is not an item-3 acceptance or overall ship mark. Final inclusion/build/commit remain undecided; actual human answers and before/after application evidence retained.

CC (2026-10-29, Myunghwan): "for 3, then leave as it is. then ship". Keep the posted road speed limit exactly as implemented, with the historical-code caveat, and accept `chicago_traffic_crashes_1m` for shipping. Prior accepted final-snapshot labels, closer-to-fact scene approximation, five-condition-field retention and physical-MISSING warning remain in force. This is the final scientific inclusion verdict; build, commit and publication are separate workflow steps.

**Assessment (AI, 2026-10-29):** All numbered dataset review issues are resolved. Accepted recipe: 1,097,209 crashes, 21 predictors, five original police injury classes, log loss and nine quarterly tests. Speed values, unknowns, features, cleaning, label mapping and splits remain unchanged. Existing source, data-identity, model and panel evidence remains applicable; historical availability and recording-risk limitations stay explicit. Resolved the Review and all panel reports are archived locally before removal. Claim remains held until authorized repository integration; no build or commit is performed here.

CC (2026-10-29, Myunghwan): "now move to the build". Build the accepted Chicago dataset; the scientific ship decision and all settled treatments remain in force.

**Assessment (AI, 2026-10-29):** Built `chicago_traffic_crashes_1m` as format 2, UUID `01a18a0b-6aa8-726f-a33a-75044860edbf`, with 1,097,209 rows, 21 predictors and nine quarterly tests. Saved container reloads with its expected checksum, and a check-only reconstruction from only traced raw inputs produces the same checksum. Zero errors or unaccepted warnings; accepted physical-MISSING reason and both informational reduced-profile findings unchanged. Definition bytes, labels, predictors and splits match the accepted recipe; no new model sweep was needed. Raw inputs are backed up locally with a SHA-256 manifest. Build provenance records the current uncommitted working tree; the exact accepted source snapshot/patch is retained locally. Commit, push, publication and claim release remain unperformed.

CC (2026-10-29, Myunghwan): "add this to the current PR". Add the accepted and verified Chicago dataset to the existing PR #33, keeping its prior ten datasets and all settled scientific choices.

**Assessment (AI, 2026-10-29):** Integrating the exact accepted definition and built report into the existing eleven-dataset PR. Preserved native build UUID 01a18a0b-6aa8-726f-a33a-75044860edbf and its truthful original working-tree provenance. The saved container verifies and reproduces from the frozen input; raw data and containers remain outside Git. The source addition preserves prior datasets, checks and build metadata.

CC (2026-11-04, Lennart): a one-month gap between train and test for labels amended after a refit ("yes follow the recommendation"; SPLIT-10), which replaces Myunghwan's exception of 2026-10-29; the injury classes are an ordered target on the KABCO scale ("Yes order them"; CLEAN-25); the `Class-dependent Recording` marker is set ("add it"): the crash time is floored to the hour because exact-hour recording differs by injury (LEAK-13: 8.21% of injured against 13.07% of uninjured on-scene reports). The metric is checked as declared.

**Assessment (AI, 2026-11-04):** the changes were checked on a fresh export of the portal (2026-11-04, 1,097,215 rows against the 1,097,209 of 2026-10-29); the export URL stops working on 2026-12-22, so a rebuild should pin a snapshot. Leak probe 13 finds no fall at the release end; the share of "REPORTED, NOT EVIDENT" rises in 2026Q2-Q3 (z +3.3 to +3.5), read as drift. The probe does not measure the amendment delay, so the gap rests on the 30-day convention for counting traffic deaths.

CC (2026-11-04, Lennart): the five condition fields (weather, lighting, road surface, traffic control device and device condition) are dropped (LEAK-10), and training starts on 2017-09-01, when citywide coverage starts (SPLIT-20). No training side then exceeds one million rows, so the dataset ships unsampled as `chicago_traffic_crashes` (the folder is renamed from `chicago_traffic_crashes_1m`; 998,117 crashes). The note on `lighting_condition`'s partial order (issue 6) falls away with the field.

**Assessment (AI, 2026-11-04):** review panel (none): no panel ran for this dataset; its issues came from the light static review of the PR #33 page and the measurements behind each mark (log loss on the three newest windows: 0.4960 without the five fields, 0.4921 with them; 0.49201 from 2017-09 against 0.49214 from 2013), and all are settled.

**Assessment (AI, 2026-11-04):** review panel (full, second pass after Lennart's PR #33 review): ship after changes (applied as wording: year 2026 under PROV-9, the 2026-11-04 snapshot and its hash, the measured update delay; the C-class step is in 2023Q4, not 2026Q2-Q3 as the assessment above says); disputed: USE-1, USE-5, LEAK-10/LEAK-38 (`dooring_i`); for the curator: issues 7-11. Priority 3: gap +, use case 0, source +, shape +, risk - (gap: social science and multiclass are thin among the accepted definitions; use case: the source names no actor and the curation's actor fits approximately; source: the City documents the table and the SR1050 form; shape: 998,117 mixed-type temporal rows; risk: the row-order leak of issue 9 and the open framing of issue 7).

CC (2026-11-05, Lennart): the use case is a city road-safety analyst who estimates each reported crash's injury level to rank sites by expected people killed or seriously injured (issue 7, A; USE-1, USE-9: the blind reviewer named the same actor without our notes). It supersedes the emergency-response framing accepted on 2026-10-29: 50.9% of the rows are desk reports nobody was dispatched to (5.3% injured against 25.5% on scene). Every row stays. The fit stays approximate: police reports catch about half of serious injuries in trauma-registry linkage, the 'reported, not evident' share steps up in 2023Q4, and the road facts recorded more completely for injury crashes are dropped.

CC (2026-11-05, Lennart): the 2023Q4 step in 'reported, not evident' (4.09-4.71% of crashes before, 6.07-6.74% from 2024Q2) is accepted as drift, with its note in the splits comment (issue 8, as implemented; USE-5 fails only when the label is shown to be another quantity, SPLIT-20).

CC (2026-11-05, Lennart): the crash time is floored to the hour in `_clean`, not in `_make_splits` (issue 9, B; LEAK-13, as hepatitis_c_prediction and gallstone_disease). The framework sorts the rows by time between the two steps, so each hour kept its minute order, and a row's rank in its hour lowered log loss by 0.00098 on all 9 splits. The windows do not change; the one crash notified before its recorded time stays unused through a flag computed from the source minute.

CC (2026-11-05, Lennart): `dooring_i` is dropped (issue 10, B; LEAK-10 through LEAK-38's measured clause, as the five condition fields of 2026-11-04); it costs 0.00011 log loss (three newest windows). If the LEAK-38 amendment opened on 2026-11-05 takes the any-source scope, `dooring_i` falls under it too.

CC (2026-11-05, Lennart): the one-month gap stays (issue 11, as implemented; SPLIT-10 as amended 2026-11-04): it covers 99.4% of last updates, and two months would cover 4 of the 5 late fatal updates for about 1% of each training side.

CC (2026-11-05, Lennart): the declared metric (the fallback multiclass log loss over the five police injury classes) is checked and stays as declared.

CC (2026-11-05, Lennart): ship. Every issue of the second-pass review page is settled, and a record with no open issue ships by default; the definition joins the accepted set, built on the curator's ask (the export URL stops working on 2026-12-22). The claim stays until the PR that takes it to `main` sets `DF: Yes`.

CC (2026-11-11, Lennart): Review issue 12, B ("Option B: Nine spread over four years."), at the one-month length of the horizon sign-off: nine one-month test windows, September 2026, April 2026, October 2025, May 2025, November 2024, June 2024, December 2023, July 2023 and January 2023, five and six months apart in turn, so each falls in another calendar month, every season appears at least twice and the windows lie on both sides of the 2023Q4 step in "reported, not evident"; they replace the nine newest quarters. The custom split keeps the notification filter, now at each month start.

CC (2026-11-11, Lennart): the declared horizon (1 month, a one-month gap, windows starting 2026-09-01, 2026-04-01, 2025-10-01, 2025-05-01, 2024-11-01, 2024-06-01, 2023-12-01, 2023-07-01 and 2023-01-01) is checked, as the one documented cycle of the road-safety analyst's work is the city's monthly review of fatal crashes, while the quarter was a convention of the build that no source names (Review horizon, b: "Reply (b): One month").

**Assessment (AI, 2026-11-11):** applied the horizon (b) and issue 12 (B) at one month: `_make_splits` builds `TemporalSplits(window=1, unit="months", gap=1, cutoffs=TEST_MONTHS)` and filters each training side by notification before the window's month start; `temporal` declares a one-month horizon with the one-month gap. Test crashes 9,641, 8,961, 9,031, 10,079, 8,924, 10,120, 9,095, 9,499 and 8,091 (83,441), fatal 6, 10, 7, 6, 9, 10, 12, 8 and 15 (83); train after the notification filter 978,937, 931,711, 879,272, 830,229, 777,987, 727,880, 675,888, 627,408 and 574,344 (98.1%, 93.3%, 88.1%, 83.2%, 77.9%, 72.9%, 67.7%, 62.9% and 57.5% of 998,117), so no window trains on less than half; 53 monthly windows keep half (May 2022 to September 2026). "Reported, not evident" is 4.0% and 4.8% of January and July 2023, 5.2% of December 2023 and 6.0-6.8% of the six newer windows. The gap month is 0.9-1.6% of a training side. 9,539 crashes are in no split (the 9,529 of August 2026, the newest window's gap month; 9 notified after 1 September 2026; 1 notified before its event), the accepted `splits_rows_unused` now says so. `dataset check`: 0 errors, 0 warnings.

## Review

**Outcome:** added. The second review panel (2026-11-04) recommended shipping after changes, and issues 7-11 were
settled on 2026-11-05. On 2026-11-11 you chose one-month windows with the one-month gap (H, b) and nine of them spread
over four years (issue 12, B), September 2026 back to January 2023, each in another calendar month; both are applied.
Left: the rebuild from the 2026-11-04 export before its URL stops working on 2026-12-22, which needs your ask.

**Main points:** Settled on 2026-11-11: nine one-month test windows from January 2023 to September 2026, on both sides
of the 2023Q4 step, each trained on the crashes up to a month before it, as the city reviews its fatal crashes monthly.

**Horizon:**

* **Verdict:** keep the three-month windows with a one-month gap (low to medium confidence): the quarter is a convention
  of the build, and the analyst's documented cycles are a month for fatal crashes and a year for the report.
* **Length:** three months, a model refit at the start of each quarter that scores the next quarter's crashes. The
  City's crash table states no use or cadence, and the quarter was set at the build as "an evaluation/refit cadence,
  not a medical outcome window" (splits comment). The analyst's documented cycles: CDOT's fatality list is "compiled
  ... after monthly reviews of fatal traffic crash information" and "updated monthly"
  ([Vision Zero Chicago Traffic Fatalities](https://catalog.data.gov/dataset/traffic-crashes-vision-zero-chicago-traffic-fatalities)),
  and its annual Chicago Traffic Crashes report "looks at data from the past several years" and lists its improvement
  projects ([Streetsblog Chicago, 2025-11-25](https://chi.streetsblog.org/2025/11/25/key-findings-from-cdots-annual-chicago-traffic-crashes-report)).
  A quarter lies between the two; no source names it.
* **Gap:** one month (your call of 2026-11-05, issue 11): a report can be amended after a later death, a traffic death
  counts within 30 days, and 99.4% of the crashes of June-August 2026 were last updated within 30 days (5 of 32 fatal
  ones later, 33-102 days). Training also keeps only the crashes notified to the police before the quarter starts.
* **Time frame:** crashes from 1 September 2017 (citywide coverage) to 30 September 2026 (October 2026 cut as
  incomplete). Quarters with the gap that keep half the crashes for training: 17, from July-September 2022 to
  July-September 2026. Today's nine cover July 2024 to September 2026, all after the 2023Q4 step in "reported, not
  evident" (4.1-4.7% of the crashes before, 5.6-6.7% from 2023Q4), which you accepted as drift (issue 8).
* **Options:**

  | | Option | What it does | Test windows | Pro | Con |
  |---|---|---|---|---|---|
  | A | Three months, one-month gap (implemented) | quarters, each trained on the crashes up to a month before it: 17 candidates above the floor, from July-September 2022 | 9 windows of 24,682 to 30,068 crashes (issue 12's B; today's nine: 24,682 to 29,258), before the split's own filter (it drops training crashes only) | between the analyst's monthly and yearly cycles; nine windows | a convention of the build; no source names it |
  | B | One year, October to September | the cycle of the annual report: four candidates keep half the crashes for training, from October 2022 (88.1%, 77.0%, 65.8% and 54.7%), about 110,000 crashes each | 4 candidates of 109,796 to 112,160 crashes, before the split's own filter | the annual report's cycle; every season in a window | three windows instead of nine; a model up to 13 months old by a window's end |
  | C | One month | the cycle of the fatality review: 53 candidates of 7,752 to 10,719 crashes | 53 candidates of 7,752 to 10,719 crashes, before the split's own filter | the fatality list's monthly cycle | only about 6 to 11 fatal crashes per window |

* **Recommendation:** A: a quarter lies between the analyst's monthly and yearly cycles, and keeps nine windows where a
  year gives three. **Decision:** A, B or C?

**Lennart (2026-11-11, discuss):** Three months seems a lot, what would make sense from a use case pov? If we refit
monthly, this could be more reasonable here?

**Answer (AI, 2026-11-11):** One-month windows, the cycle of the city's fatal-crash review?

* **Problem:**
  - The quarter was set when the dataset was built; no source names it.
  - The one documented cycle of the analyst's work is monthly: CDOT's list of traffic fatalities is compiled "after
    monthly reviews of fatal traffic crash information" and "updated monthly"; the yearly report is the other cycle.
  - A month with the one-month gap gives 53 windows that keep half the crashes for training (7,752 to 10,719 crashes
    each), so nine months can be spread over 2022 to 2026 as issue 12 spreads nine quarters.
* **Background:** the score is the multiclass log loss over five severity classes; fatal crashes are about 0.1% of a
  window, 6 to 11 in a month against 20 to 30 in a quarter, so a month's score leans less on them than a quarter's,
  which the log loss over all five classes allows. The gap stays a month: a report is final within 30 days.
* **Options:**

  | | Option | What it does | Test windows | Pro | Con |
  |---|---|---|---|---|---|
  | a | Three months (implemented) | issue 12's nine quarters | 9 windows of 24,682 to 30,068 crashes | three times the crashes per window | a length no source gives |
  | b | One month | nine months spread over 2022 to 2026, proposed again in issue 12 | 9 windows of 7,752 to 10,719 crashes | the city's monthly review cycle; a refit as often as the list is updated | a third of the test crashes; 6 to 11 fatal crashes per window |

* **Recommendation:** b: the monthly review is the analyst's documented cycle, and nine months still test about 80,000
  crashes. **Decision:** a or b?

**Lennart (2026-11-11, change):** Reply (b): One month

**Resolved (2026-11-11, Lennart):** b, one-month windows with the one-month gap, the cycle of the city's monthly
review of fatal crashes, in place of the quarter, a convention of the build. `temporal` declares a one-month horizon,
and the custom `_make_splits` builds `TemporalSplits(window=1, unit="months", gap=1, cutoffs=TEST_MONTHS)` with issue
12's nine months, keeping the notification filter at each month start. `task_summary.split`, `splits_comment` (the
length's reason from this block, the windows and their counts, the gap, the drift paragraph), the metric reason (its
figures now dated to July-September 2026), the late-label note and the accepted `splits_rows_unused` (9,539 crashes in
no split, 9,529 of them in August 2026, the newest window's gap month) are rewritten. Every window trains on 57.5% to
98.1% of the crashes. The record has the horizon CC line. `dataset check`: 0 errors, 0 warnings (README not
regenerated).

**Issues for Lennart:**

7. **Reword the use case to a road-safety analyst?**

   * **Problem:**
     - `use_case` names an emergency-response analyst who assesses response needs, but 50.9% of the rows (508,086)
       are desk reports: crashes reported later at a police district, with nobody dispatched.
     - Desk reports are 5.3% injured against 25.5% for on-scene reports, so part of the score comes from recognising
       a minor desk report.
     - Whichever reading of the rules holds, the fix is an edit to the definition's text, and it would replace the
       framing Myunghwan accepted on 2026-10-29.
   * **Background:**
     - The definition has the dispatch framing: `fit_reason` and `known` are written for timely initial-call
       information.
     - The source does not have the dispatcher's main input, the caller's account of injuries[^known].
   * **Experiments:** a quick LightGBM on Jul-Sep 2026:
     - beats the class prior by 18.0% on all rows, but by only 11.9% on on-scene rows;
     - has an AUC for killed or seriously injured (KSI) of 0.842 on all rows and 0.787 on on-scene rows.
   * **Option A in full:** a city road-safety analyst estimates, for each reported crash, the probability of each
     KABCO level (the police injury scale), to estimate expected KSI per site and rank sites for countermeasures.
     `fit_reason` and `known` would then name that actor's gaps:
     - police KABCO finds about half of serious injuries in trauma-registry linkage studies
       ([Traffic Injury Prevention 2024](https://informahealthcare.com/doi/full/10.1080/15389588.2024.2361052));
     - the coding of the C class drifts (issue 8);
     - the road facts were dropped because injury-crash reports record them more completely.

     The fit stays approximate[^fit], every row stays, and the data does not change.
   * **Panel:**
     - The advocate says the use case is met and only asks for a rewording[^use][^rephrase].
     - The critic and the mediator say the use-case rule is triggered, because the rows fail the stated use case.
     - The blind reviewer named the road-safety analyst without seeing our notes.
     - A KSI-only binary target (the domain practitioner's option) would match the analyst's decision directly but
       changes the target[^target]; the panel does not propose it.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Road-safety analyst | new use-case text | every row stays; data unchanged | fit stays approximate |
     | B | Dispatcher, on-scene only | on-scene rows only | keeps the dispatcher | 54% fewer rows; no caller's account |
     | C | Dispatcher (implemented) | as now | accepted 2026-10-29 | half the rows not dispatched |

   * **Recommendation:** A, the panel's choice; the blind reviewer named the same actor without seeing our notes.
     **Decision:** A, B, or C (keep the dispatch framing)?

   [^use]: **USE-1** (Must): a use case is an actor, a moment and a decision. The advocate says USE-1 is met; the
     critic and the mediator say USE-1 is triggered, because the rows fail the stated use case.
   [^fit]: **USE-8** (Must): write how closely the data mirrors the use case, its fit.
   [^rephrase]: **USE-9** (Should; narrows USE-8): before settling on approximate, ask whether the data as shipped
     mirrors another well-defined use case. The advocate says USE-9 asks for a rewording.
   [^known]: **USE-6** (Must): anything known at the prediction point is a legitimate input.
   [^target]: **USE-5** (Must): predict what the actor would act on, at the resolution they act on it.

   **Lennart (2026-11-05, change):** Option A: Road-safety analyst.

   **Resolved (2026-11-05, Lennart):** A. The actor is a city road-safety analyst ranking sites by expected people
   killed or seriously injured; `use_case`, `known` and `fit_reason` are rewritten (fit approximate: police reports
   catch about half of serious injuries, the C-class step of late 2023, the dropped road facts). Myunghwan's framing of
   2026-10-29 is marked superseded. A USE-9 Cases row.

8. **Accept the 2023Q4 step in "reported, not evident" as drift?**

   * **Problem:**
     - "REPORTED, NOT EVIDENT" (C) is the class for an injury that someone reports but the officer cannot see, and its
       share of crashes steps up in 2023Q4.
     - Every test window (2024Q3-2026Q3) lies after the step and most of the training history before it, while C
       carries about 35% of the log loss, so the score leans on the class whose coding moved.
     - No cause has been found; it looks like a change in how officers record C injuries.
   * **Background:** the share of C over time:

     | Period | Share of C |
     |---|---|
     | 2022Q1-2023Q3 | 4.09-4.71% |
     | 2023Q4 | 5.56% |
     | 2024Q1 | 5.66% |
     | 2024Q2-2026Q1 | 6.07-6.54% |
     | 2026Q2-Q3 | 6.64-6.74% |

     - Over the same time, incapacitating plus fatal falls from about 2.0% to 1.4%.
     - The step shows in both report types (desk 2.49% to 3.07%, on scene 7.00% to 7.97%), and the desk share stays
       at 50-53%, so the mix of report types did not change.
     - The label fails only when it is shown to be another quantity, and that has not happened[^label]; the rule on
       breaks in the training history also applies[^history].
   * **Panel:**
     - The advocate calls it a question, not a failure, and notes that the temporal split measures what the drift
       costs: skill is 0.162-0.171 on a random split and 0.165-0.169 on the temporal split.
     - The critic answers that the split measures the cost in score, not whether C still means the same thing.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Drift (implemented) | shares in `splits_comment` | split measures the cost | not what C means |
     | B | Search first | look for a late-2023 coding change | would settle what C means | shipping waits |

   * **Recommendation:** A, accept it as drift with the note (the panel's). **Decision:** A (accept it) or B (look
     for the coding change first)?

   **Notes for the AI:** on B, look for a change to CPD's or IDOT's E-Crash coding in late 2023; a documented change
   would settle what C means after the step.

   [^label]: **USE-5** (Must) fails only when the label is shown to be another quantity.
   [^history]: **SPLIT-20** (Should): decide what the train side holds from the use case, and check the history for
     breaks (a change of rules or of the data collection).

   **Resolved (2026-11-05, Lennart):** as implemented.

9. **Floor the crash time in `_clean`, so the row order no longer carries the minute?**

   * **Problem:**
     - The hour floor of 2026-11-04[^precision] runs in `_make_splits`, after the framework's `order_rows` has sorted
       the frame by the full `crash_date`, so inside each hour the rows stay in minute order.
     - The minute carries the recording difference the floor was meant to remove: rows at minute :00 or :30 are about
       70% desk reports and 8.7-10.1% injured, rows at odd minutes 19-26% injured.
     - This is a new finding, and no `Potential leak, kept on purpose:` note covers it.
   * **Effect on the task:** a deployed model sees the minute, but not where a crash ranks among all crashes of that
     hour.
   * **Experiments:**
     - The task gamer turned each row's rank within its hour into a feature: it lowers log loss by 0.00098 (0.00008
       to 0.00202 per split), on all 9 splits; a random column moves the score by -0.0007 to +0.0009.
     - The mediator traced the order to `order_rows`: the source CSV is not in minute order (within an hour, the
       median Spearman correlation of row position and minute is 0.00).
   * **Panel:** both briefs proposed shuffling the rows within each hour; the mediator showed that a shuffle in
     `_clean` is undone by the sort, and a shuffle in `_make_splits` breaks the split positions.
   * **Option B in full:**
     - Within each hour the rows then follow the framework's content order (a hash of each row's values), which
       carries no minute.
     - The window and gap bounds fall on midnight, so no cohort changes.
     - It changes the row order, so the container changes at the next rebuild, as it already does for the year.
   * **Consistency:** the rule is a Must, so keeping the order with a note would need a higher-ranked Must, and none
     applies[^precision]; precedents: hepatitis_c_prediction and gallstone_disease (precision harmonised).
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Floor in `_make_splits` (implemented) | minute order kept | none found | order carries the minute |
     | B | Floor in `_clean` | content order per hour | no minute in order; same cohorts | new row order |

   * **Recommendation:** B, the panel's. **Decision:** B (apply the floor in `_clean` now; it takes effect at the
     rebuild) or A (overrule the mediator's finding that the order brings the minute back)?

   **Notes for the AI:** on B, floor `crash_date` in `_clean`, and keep the original timestamp only for the
   notification check (so the one crash notified before its recorded time stays unused, as the accepted warning
   describes). Any definition that coarsens its time column in `_make_splits` has the same problem, which needs a
   note for the framework.

   [^precision]: **LEAK-13** (Must; amended 2026-10-26): class-specific recording conventions are harmonised: write
     every row at the precision of the measured values. LEAK-13 is a Must, so keeping the order with a note would need
     a higher-ranked Must, and none applies.

   **Lennart (2026-11-05, change):** Option B: Floor in _clean.

   **Resolved (2026-11-05, Lennart):** B. `crash_date` is floored to the hour in `_clean`, before the framework orders
   the rows; the notification check still reads the source minute through a flag computed before the floor. The injury
   share by tenth of each hour is now flat (15.1-15.5%, 9.9-18.6% before), and `dataset check` no longer warns that the
   split changes the time column. No other definition changes its time column in `_make_splits`. A LEAK-13 Cases row.

10. **Keep `dooring_i` or drop it?**

   * **Problem:**
     - `dooring_i` says whether a car door opened into a cyclist's path, and it is blank on 99.68% of the rows.
     - On 2026-11-04 the five condition fields were dropped because whether they were filled in followed the
       injury[^fill], and the claim auditor found a similar pattern here.
     - Measured more closely, whether it is filled in shows no consistent difference by outcome and no gain, so the
       mechanism is not confirmed here.
   * **Experiments:**
     - The claim auditor: within the same first crash type, injured crashes have `dooring_i` filled in 4-8 times as
       often (parked vehicle 0.24% against 0.06%), and a recorded "N" is 55% injured, against a 16% base rate.
     - The mediator split the two values: a "Y" is a scene fact (a door hit a cyclist), and an "N" alone is the
       form-filling signal; reweighted so injured and uninjured crashes have the same mix of crash types, the N rate
       goes both ways:
       - on the injured crashes' mix of types: 0.38% of injured against 0.44% of uninjured crashes;
       - on the uninjured crashes' mix: 0.100% against 0.061%;
       - among cyclist crashes, where most N values are: 2.66% against 2.71%.
     - Flags saying whether each sparse column is filled in change log loss by -0.0004, and dropping `dooring_i`
       costs +0.0001; for the five fields, their fill flags won back 72% of a 0.0039 gain.
   * **Panel:** the advocate and the critic say drop it, and the advocate argues that the measured clause leaves no
     option to keep it[^fill]; the mediator finds both choices consistent with the rules.
   * **Consistency:** if you keep it, the fact that sets it apart from the five fields is that the N fill shows no
     consistent difference by outcome and no gain.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep (implemented) | kept, no note yet[^note] | no fill difference, no gain | needs the note |
     | B | Drop | the column leaves | costs nothing measurable; no exception; like the five fields | +0.0001 log loss |

   * **Recommendation:** B, drop it: it costs nothing measurable, needs no exception and treats it like the five
     fields; the advocate and the critic agree, and the mediator finds keeping it consistent too. **Decision:** B
     (drop it) or A (keep it with a note quoting these numbers)?

   **Notes for the AI:** on A, add the LEAK-6 note quoting these numbers.

   [^fill]: **LEAK-38** (Should; narrows LEAK-10): a field whose fill, among comparable crashes, is shown to differ
     by outcome goes under **LEAK-10** (Must). The five fields were dropped under LEAK-10, under LEAK-38's measured
     clause; the advocate argues that LEAK-38's measured clause leaves no option to keep `dooring_i`.
   [^note]: **LEAK-6** (Must) asks for a note on any suspect kept (to be added if you keep it).

   **Lennart (2026-11-05, change):** Option B: Drop.

   **Resolved (2026-11-05, Lennart):** B. `dooring_i` left (15 features; cost +0.00011 log loss). Should the open
   LEAK-38 amendment take the any-source scope, this field would fall under it.

11. **Keep the one-month gap?**

   * **Problem:**
     - The gap between training and test is one month, and it now has a measurement: the portal's `:updated_at` field
       gives the date of each row's last update.
     - For crashes of June-August 2026, 99.4% of the last updates fall within 30 days of the crash (median 16.1 days),
       but 5 of the 32 fatal crashes were last updated at 33-102 days.
     - With one month, a training side holds about 0.6% of rows whose last update a real refit at the quarter start
       would not yet have seen, among them late updates to a few fatal crashes.
   * **Background:** `:updated_at` changes when any field changes, not only the label. Where the source documents late
     labels, the gap is about the label's delay[^gap]; both sizes fit that.
   * **Consistency:** zillow_prize has one month; lt_vehicle_loan_default_prediction has no gap only because of the
     floor on the training side's size[^floor].
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | One month (implemented) | 1.0-1.4% of each train side | as zillow_prize | ~0.6% of train rows updated later |
     | B | Two months | covers 4 of 5 late fatal records | fewer late updates | ~0.0001 worse log loss; ~1% less train |

   * **Recommendation:** A, the panel's. **Decision:** A (one month) or B (two months)?

   [^gap]: **SPLIT-10** (Should), as amended on 2026-11-04: where the source documents late labels, the gap is about
     the label's delay.
   [^floor]: **SPLIT-14** (Must): no window's train side holds less than 50% of the data.

   **Resolved (2026-11-05, Lennart):** as implemented. The record's `year` is 2026 (PROV-9, a growing source).

12. **Which quarters should the nine test windows be?**

   * **Problem:**
     - The nine test windows are the nine quarters from July 2024 to September 2026, one after the other, while
       quarters that keep half the crashes for training reach back to July-September 2022, 17 in all[^ct-split14].
     - Since 2026-11-10 the newest window always stays and the others are chosen from the use case and statistics of
       the data, preferring other years over the windows just before the newest, and walking back needs its own
       reason[^ct-split15].
     - The candidates straddle the 2023Q4 step in "reported, not evident" (4.1-4.7% of the crashes before, 5.6-6.7%
       from 2023Q4), which you accepted as drift (issue 8), while every window today lies after it.
   * **Background:**
     - Today's nine quarters already span three calendar years and every season at least twice; the season shows in
       the label (no indication of injury 81.9-84.2% in July-September, 84.5-86.5% in January-March).
     - The features hardly drift: the largest PSI is 0.02 to 0.07 in every candidate (trafficway type, first crash
       type), and at most 0.2% of a window's crashes carry a category its train side lacks. PSI, the population
       stability index, compares a feature's distribution in the window with its train side; above 0.25 is usually read
       as a large shift. So the candidates differ in the season, the year and the side of the step.
     - B spreads nine quarters over the 17, about every other one, shifted by a quarter halfway so that every season
       appears at least twice (every other quarter alone would test only summers and winters); it holds the step
       quarter 2023Q4 and three quarters before it. C takes every third quarter, six windows that rotate through the
       seasons.
     - The candidate table counts the training crashes before `_make_splits` drops those notified after the quarter's
       start, so the train shares below are slightly high.
   * **Statistics:** from the candidate table (every crash; the train side's "reported, not evident" share from a
     100,000-row sample); fatal crashes are 0.1% in every quarter (0.2% in 2023Q1).

     | Quarter | In | Test crashes | No injury | Reported, not evident: test / train side | Incapacitating | Train share | Largest PSI |
     |---|---|---|---|---|---|---|---|
     | 2026Q3 | A, B, C | 28,987 | 81.9% | 6.7% / 4.9% | 1.5% | 96.1% | 0.025 |
     | 2026Q2 | A | 28,742 | 82.8% | 6.6% / 4.8% | 1.4% | 93.3% | 0.020 |
     | 2026Q1 | A, B | 25,920 | 84.9% | 6.3% / 4.7% | 1.0% | 90.8% | 0.029 |
     | 2025Q4 | A, C | 26,147 | 84.1% | 6.2% / 4.7% | 1.4% | 88.1% | 0.031 |
     | 2025Q3 | A, B | 29,011 | 82.0% | 6.5% / 4.7% | 1.6% | 85.1% | 0.033 |
     | 2025Q2 | A | 29,055 | 83.8% | 6.1% / 4.6% | 1.4% | 82.3% | 0.027 |
     | 2025Q1 | A, B, C | 24,682 | 84.5% | 6.2% / 4.6% | 1.1% | 79.8% | 0.038 |
     | 2024Q4 | A | 27,564 | 83.8% | 6.2% / 4.5% | 1.3% | 77.0% | 0.046 |
     | 2024Q3 | A | 29,258 | 82.3% | 6.2% / 4.4% | 1.7% | 74.0% | 0.048 |
     | 2024Q2 | B, C | 30,068 | 83.2% | 6.1% / 4.4% | 1.5% | 71.1% | 0.052 |
     | 2024Q1 | none | 24,915 | 84.9% | 5.7% / 4.4% | 1.3% | 68.6% | 0.060 |
     | 2023Q4 | B | 27,919 | 84.1% | 5.6% / 4.2% | 1.5% | 65.8% | 0.067 |
     | 2023Q3 | C | 28,833 | 83.9% | 4.7% / 4.2% | 1.9% | 62.9% | 0.065 |
     | 2023Q2 | B | 28,680 | 85.0% | 4.3% / 4.3% | 1.9% | 60.1% | 0.064 |
     | 2023Q1 | none | 25,042 | 86.5% | 4.1% / 4.4% | 1.6% | 57.5% | 0.072 |
     | 2022Q4 | B, C | 27,561 | 85.2% | 4.3% / 4.3% | 1.8% | 54.7% | 0.056 |
     | 2022Q3 | B | 28,015 | 84.2% | 4.3% / 4.3% | 2.1% | 51.9% | 0.046 |

   * **Effect on the task:** A ranks models only after the step, on refits whose training lies mostly before it, and
     only on 2024-2026. B adds 2022 and 2023: the step quarter itself, where a refit trained on the earlier coding
     meets the new one, and three quarters of the earlier coding, which a model deployed now no longer meets but which
     issue 8 read as the same task. C spreads six windows evenly with a third fewer test crashes (166,278 against
     249,366) and skips the step quarter.
   * **Consistency:** the nine quarters came with the build of 2026-10-29; no curator call has set which quarters.
     Issue 8 (2026-11-05) accepted the step as drift, not as another label, so windows on both sides of it test the
     same task.
   * **Sources:** the definition `datasets/_dev/tabarena-v0pt2/chicago_traffic_crashes/dataset.py` (`_make_splits`,
     `splits_comment`, its drift paragraph); the record `curation/records/chicago_traffic_crashes.md`; the candidate
     table `.venv/bin/python -m data_foundry.curation.cli dataset windows chicago_traffic_crashes --root
     datasets/_dev/tabarena-v0pt2 --window 3 --unit months --gap 1 --gap-unit months` (17 quarters; the splits are
     custom, so the length and gap are given).
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Nine newest quarters (implemented) | tests 2024Q3 to 2026Q3 | only the coding after the step, which a deployed model meets; each refit trains on 74.0% or more | walks back without a stated reason; nothing from 2022-2023 or the step quarter |
     | B | Nine spread over four years | tests 2026Q3, 2026Q1, 2025Q3, 2025Q1, 2024Q2, 2023Q4, 2023Q2, 2022Q4 and 2022Q3 | the same count over the whole eligible history; every season at least twice; a refit across the step | three windows on the coding before the step; the oldest refit trains on 51.9% |
     | C | Every third quarter | tests 2026Q3, 2025Q4, 2025Q1, 2024Q2, 2023Q3 and 2022Q4 | an even spread that rotates through the seasons; the oldest refit on 54.7% | six windows, a third fewer test crashes; skips the step quarter |

   * **Recommendation:** B: it keeps nine windows and their test crashes and spreads them over the four years open,
     every season twice or more, with the step quarter in; A's one reason, testing only the newest coding, would need
     the step read as a change of label, which issue 8 did not do. **Decision:** A, B or C?

   **Notes for the AI:** the split stays custom. On B, in `_make_splits` replace `TemporalSplits(window=3,
   unit="months", n_windows=9, min_train_fraction=0.5, gap=1)` with `TemporalSplits(window=3, unit="months", gap=1,
   cutoffs=("2026-07-01", "2026-01-01", "2025-07-01", "2025-01-01", "2024-04-01", "2023-10-01", "2023-04-01",
   "2022-10-01", "2022-07-01"))` (`cutoffs` excludes `n_windows`; drop `min_train_fraction`, which would silently cut
   the older cutoffs). Each window still starts on a quarter's first day, so the notification filter
   (`to_period("Q").start_time`) is unchanged, and so is `temporal` (`horizon=3, gap=1`). From the candidate table:
   test 28,987, 25,920, 29,011, 24,682, 30,068, 27,919, 28,680, 27,561 and 28,015 crashes (250,843); train before the
   notification filter 959,335, 905,864, 849,226, 796,799, 709,773, 656,271, 599,463, 546,159 and 518,149 (96.1% to
   51.9%). On C, `cutoffs=("2026-07-01", "2025-10-01", "2025-01-01", "2024-04-01", "2023-07-01", "2022-10-01")`: test
   28,987, 26,147, 24,682, 30,068, 28,833 and 27,561 (166,278), train 959,335, 879,292, 796,799, 709,773, 627,446 and
   546,159 (96.1% to 54.7%). Then rewrite `task_summary.split` ("Nine later three-month crash cohorts"),
   `splits_comment` ("Nine consecutive three-month windows"; the drift paragraph's "Every test window lies after the
   2023Q4 step"), a CC line in the record, a dated CHANGELOG entry, `dataset check` and the eligibility table of
   `_decisions` (its rows follow the windows).

   [^ct-split14]: **SPLIT-14** (Must): a temporal task has at least 3 windows, and no window's train side holds less
     than 50% of the data.
   [^ct-split15]: **SPLIT-15** (Must for the newest window, Should for the others; amended 2026-11-10, Lennart and
     Andrej): "The newest window is always a test window ... which periods a deployed model must handle (other years,
     seasons, holidays, events, a change of rules or of the data collection) ... Prefer windows in other years, then
     other seasons, then other months, weeks or days, over the windows just before the newest. Walking back from the
     newest is one choice among others and needs its reason too."

   **Lennart (2026-11-11, change):** Option B: Nine spread over four years.

   **Resolved (2026-11-11, Lennart):** B, at the one-month length of the horizon (b): nine months spread over the 53
   monthly windows that keep half the crashes for training (May 2022 to September 2026), five and six months apart in
   turn, so each falls in another calendar month and every season appears at least twice: September 2026, April 2026,
   October 2025, May 2025, November 2024, June 2024, December 2023, July 2023 and January 2023 (`TEST_MONTHS`;
   `n_windows` and `min_train_fraction` are gone). Test 9,641, 8,961, 9,031, 10,079, 8,924, 10,120, 9,095, 9,499 and
   8,091 crashes (83,441; 6, 10, 7, 6, 9, 10, 12, 8 and 15 fatal, 83 in all); train after the notification filter
   978,937, 931,711, 879,272, 830,229, 777,987, 727,880, 675,888, 627,408 and 574,344 (98.1%, 93.3%, 88.1%, 83.2%,
   77.9%, 72.9%, 67.7%, 62.9% and 57.5% of 998,117): no window under half. January and July 2023 lie before the 2023Q4
   step ("reported, not evident" 4.0% and 4.8%), December 2023 in its quarter (5.2%) and the six newer windows after it
   (6.0-6.8%), as the drift paragraph now says. The eligibility table of `_decisions` follows the months. The record
   has the CC line. `dataset check`: 0 errors, 0 warnings.

**Review panel:** ship after changes (mediator). The tier was full, as a second pass after Lennart's review of PR #33
on 2026-11-04: seven evidence agents, the advocate and the critic with one rebuttal each, and the mediator. Claims: 27
in all; 21 hold (one citing the wrong recipe), 4 were refuted, 1 is untested and 1 was superseded. Three of the
refuted claims are fixed in the notes (the year, the snapshot, the metric reason), as are the C9 numbers; the fourth,
`dooring_i`, is issue 10. The untested one
is whether `first_crash_type` was known at first notification. Blind review: include with changes. Its concerns were
the name `not_right_of_way_i` (the bulk file's own header, documented), the dropped condition fields (dropped under
LEAK-10 on 2026-11-04) and the rare top classes (18-34 fatal crashes per window, enough to score). Task gamer: its best
exploit is the row order within the hour, +0.00098 log loss on 9 of 9 splits (issue 9). It found nothing that hurts an
honest model. Agreed: the temporal split, the excluded outcome columns, the five-field drop, the log-loss fallback, PROV-9
and the wording fixes. Disputed: whether USE-1 is triggered (issue 7), whether the C step fails USE-5 (issue 8), and
`dooring_i` under LEAK-38 (issue 10). Both briefs left the ranked probability score over the ordered classes (proposed
by the domain practitioner) to you; the mediator ruled it out: no source, and the context is not clear enough for
MET-11. The mediator's issues 1, 2, 3 and 4 are issues 7, 8, 10 and 11 here, and its change 1 is issue 9.

<details><summary>Mediator</summary>

**Verdict: ship after changes.** The required fixes are edits to the definition. The four calls below are the curator's.

```text
Verdict: ship after changes.
Validity: USE-1 triggered (the stated responder does not meet 50.9% of rows); fix by rewording the definition (issue 1).
USE-5 open question (C-class step in 2023Q4, issue 2). USE-8: rewrite fit_reason/known with issue 1.
LEAK-13 triggered: the framework re-sorts by the full timestamp, so row order brings back the minute (+0.00098, 9/9 splits); fix in _clean.
LEAK-10 holds for all inputs except dooring_i, a borderline call (issue 3). SPLIT-1..4/9/11/14/20/21 hold.
SPLIT-10 holds: a 1-month gap, with the delay now measured (issue 4 is the gap size). PROV-9 triggered: fix the year to 2026.
P5: the provenance text names bytes that are gone; repin to the 2026-11-04 export.
Value: TP-9 holds (18-34 fatal per fold, all 5 classes in every fold). MET-1/8/11: fallback log_loss holds.
Quality: stale wording in C7, C9 and the metric reason.
Weighed: size +, real signal (skill about 0.17) +, label noise and drift -.
For the curator: issues 1-4.
```

**Changes to make now (no decision needed)**

1. **LEAK-13 (Must): floor `crash_date` in `_clean`, not in `_make_splits`.** I checked the cause.
   - The source CSV is not in minute order: within each hour, the Spearman correlation of row position and minute has median 0.00.
   - The order comes from the framework. `order_rows` (`src/data_foundry/v2/preprocessing.py:235`) runs after `_clean` and stable-sorts by the full-precision `crash_date`. `_make_splits` then floors it, so rows within an hour stay in minute order.
   - On the kit, the injury share rises with relative rank in the hour: 9.9% in the first tenth, 18.6% in the last.
   - Neither side's "shuffle within the hour" works as proposed. A shuffle in `_clean` is undone by that sort, and a shuffle in `_make_splits` breaks the split positions.
   - Flooring in `_clean` leaves each hour in content-hash order. Window and gap bounds fall on midnight, so no cohort changes.
   - Keep the original timestamp for the notification check only, so the accepted `splits_rows_unused` row stays as described.
   - This is a new exploit: there is no `Potential leak, kept on purpose:` note, and the only accepted warning is `splits_rows_unused`.
   - Any definition that coarsens its time column in `_make_splits` has the same problem. That is a framework note for later.
2. **PROV-9 (Must):** `year = "2026"  # the snapshot we pin` and bibtex `year = {2026}`. This matches consumer_complaints_1m, sf_permit_time and kickstarter.
3. **P5 provenance:**
   - Rewrite `download_description` to name the 2026-11-04 export and its sha256 `4bf63b07d869d992887c08d70bc017a357f731e6bf563dd6098546417b29027b`.
   - Mark C3's 889,076 rows and 0.550174→0.550105, and C10's sub-counts (36 and 26), as 10-29 figures, or recompute them at the rebuild.
   - The rebuild needs the curator's ask (house rule). The export URL stops working on 2026-12-22. Add a CHANGELOG entry for the new UUID.
4. **SPLIT-10 note:** replace "not measured" in `splits_comment` and in the C2 bullet with the `:updated_at` figures:
   - median last update 16.1 days after the crash;
   - 99.4% of rows last updated within 30 days;
   - 5 of 32 fatal crashes last updated at 33-102 days;
   - no shift in injury shares across the update.

   Add its three limits: the field changes when any field changes, not only the label; history before the 2026-05-21 reload is hidden; 1,904 older crashes were rewritten in one batch on 2026-11-03. Add one clause naming the contrast with lt_vehicle_loan_default_prediction (SPLIT-14 floor, measured effect), and one saying the windows are calendar quarters only because of the 2026-10-01 cut.
5. **SPLIT-20 drift note:** date the step correctly in `splits_comment` and the record. Measured on the kit, "REPORTED, NOT EVIDENT" goes:
   - 4.09-4.71% (2022Q1-2023Q3);
   - 5.56% (2023Q4);
   - 6.07-6.54% (2024Q2-2026Q1);
   - 6.64% and 6.74% (2026Q2-Q3).

   The record's "2026Q2-Q3, z +3.3" and the prep report's "from 2025Q1" are both wrong.
6. **MET-1 note and writing:**
   - Replace "approved for investigation" in the metric reason.
   - State that K+A carries about 10% of the loss and C about 35%.
   - State that skill on on-scene rows is 11.9% against 18.0% overall.
   - Keep `log_loss`. RPS has no source and no clear context under MET-11, and would need a MET-13 implementation.
7. **C7 (writing):**
   - Remove the code-99 sentence: 0 such rows are in the frame.
   - Replace the "recent matched" zero-speed rates. On the frame a zero is 0.548% of uninjured against 0.280% of injured crashes, and within parking lots it is 3.00% against 2.80%.
8. **C9 (writing):** cite 0.49609 vs 0.49600 for the shipped 16 inputs.
9. **Optional, cosmetic:** remove `date_police_notified` from the datetime declaration.

**Issues for the curator, ranked**

**1. Framing (P3; USE-1 Must, USE-8 Must, USE-9 Should).**
- **Problem:** the use case names an emergency-response analyst. 50.9% of rows are desk reports, where nobody was dispatched (5.3% injured against 25.5% on scene).
- **Effect:** skill on on-scene rows is 11.9% against 18.0% overall, and KSI AUC 0.787 against 0.842.
- **Advocate:** USE-1 is met and USE-9 gives a wording fix.
- **Critic:** USE-1 and USE-3 are triggered, and `fit_reason` and `known` must change too.
- **Ruling:** USE-1 asks that every filter be checked against the use case, and here the rows fail that check, so it is triggered. The fix is either way an edit to the definition.
- **Why it is yours:** choosing between the fixes is a framing call, and the change replaces the framing Myunghwan accepted on 2026-10-29.
- **Decision:**
  - (a) Reword to a road-safety analyst estimating KABCO per crash to rank sites by expected KSI. Rewrite `fit_reason` and `known` to name that actor's gaps: KABCO misses about 50% of serious injuries, C-class drift, road facts dropped. Fit stays approximate. Recommended: it is the milder fix, keeps every row, and the whole panel agrees.
  - (b) Keep the dispatcher and filter to on-scene reports: 54% fewer rows, and the caller's account is still missing (USE-6).

**2. What the C class means in the test windows (P3; USE-5 Must, open).**
- **Problem:** the C share steps up in 2023Q4. All nine test windows lie after the step; their spread is 0.67 pp. K+A falls from 2.0% to 1.4%.
- **New measurement:** the step is in both report types (desk 2.49%→3.07%, on scene 7.00%→7.97%). The on-scene rate keeps rising to about 9.5%, and desk reports jump again in 2026Q2 (3.10%→3.92%). The desk share stays flat at 50-53%, so this is not a change in report mix. It looks like a change in recording practice, but no cause has been found.
- **Advocate:** a question, not a failed Must; the split already measures what the drift costs.
- **Critic:** the split measures the score cost, not whether the label still means the same thing.
- **Ruling:** both say it does not block shipping. USE-5 fails only when a label is shown to be another quantity, which has not happened.
- **Decision:** accept it as drift with a note (recommended), or look for a CPD or IDOT E-Crash coding change in late 2023 first. That documentation would settle it.

**3. `dooring_i`: drop or keep (P4; LEAK-10 Must via LEAK-38's measured clause, LEAK-6 Must).**
- **Both briefs say drop.** That rests on the claim auditor's 4-8x "recorded" ratio, which mixes Y, a scene fact, with the N fill.
- **My test:** I separated N, the pure form-filling signal (2023-07 onward, within crash type).
  - Standardised to the injured crashes' type mix: N recorded 0.38% injured vs 0.44% uninjured (ratio 0.88).
  - Standardised to the uninjured mix: 0.100% vs 0.061%.
  - The direction varies by type. In PEDALCYCLIST, where most N values are, it is 2.66% vs 2.71%.
- **Gain tests:** fill flags gain −0.0004 (column auditor); dropping the column costs +0.0001.
- **So the mechanism is not confirmed.** That sets it apart from the five fields, whose flags won back 72% of a measured 0.0039 gain.
- **Decision:** keep with a LEAK-6 note quoting these numbers, or drop for uniformity at zero cost. Both are consistent with the rules.
- **Related:** `not_right_of_way_i` needs no LEAK-11 note. Its difference is the Y value (private property, mostly parking lots; ratio 0.61). N fill is equal (ratio 0.95).

**4. Gap size (P4; SPLIT-10 Should, weighing).**
- 1 month covers 99.4% of last updates.
- 2 months would cover 4 of the 5 late fatal records, at about 0.0001 log loss and about 1% of each training side.
- The amended rule sets the gap at "about the label's delay", and both sizes fit that.
- **Recommendation:** keep 1 month.

**Agreed facts**

- **Frame:** 998,117 rows, 15 inputs, 9 calendar-quarter windows (2024Q3-2026Q3).
- **Training sides:** 74-96% of rows, a 30-31-day gap in every split, 0% exact copies across the split once the hour is included.
- **Test windows:** 18-34 fatal crashes each; all five classes in every fold.
- **Notification filter:** removes 16-32 training rows per split.
- **Regime:** temporal is right (USE-10). Skill under a random hold-out is 0.162-0.171, under the temporal split 0.165-0.169. 82% of test coordinates appear in training.
- **Outcome columns:** none of them reaches the frame. `crash_type` alone would take log loss from 0.46 to 0.29.
- **Five condition fields:** dropping them is correct (curator, 2026-11-04, measured).
- **`not_right_of_way_i`:** the bulk CSV header really is `NOT_RIGHT_OF_WAY_I` (column 18 of `crashes.csv`). The blind reviewer's naming objection fails.
- **`first_crash_type`:** carries most of the signal (AUC 0.765 alone) and is an accepted approximation (USE-8).
- **Notification delay:** at most 0.157% of crashes are notified more than 30 days late; the release end selects almost nothing by outcome.
- **Train vs test classifier:** AUC 0.516.
- **Exploit 2:** counts over train and test together gain +0.00025, which is noise.
- **Blind reviewer:** "about 100 fatal per window" is wrong.

**Consistency with precedent**

- No register flag involves this dataset.
- These follow their precedents:
  - the LEAK-13 fix (hepatitis_c_prediction, gallstone_disease);
  - PROV-9 (consumer_complaints_1m, sf_permit_time);
  - the gap (zillow_prize; the contrast with lt is named in change 4);
  - the 2017-09 start (aeolus, perth_house_prices);
  - KABCO ordinal (PR #37);
  - the five-field drop (kick, expresso_churn_prediction);
  - the speed keep, whose separating fact is a zero speed marking a place with no posted limit.
- Keeping `dooring_i` would depart from the five-field drop. The separating fact is no consistent N-fill difference and no gain.
- The chicago SPLIT-10 decision (first gap set on documented late labels alone) and the LEAK-38 measured-clause drop should each get a Cases row.

</details>

<details><summary>Claim audit</summary>

**Focus question (P/focus.md: "none beyond the standard panel").** The dataset is ready to ship after two small edits and a rebuild. None of the claims that affect validity (target, split, notification filter, metric scorability) was refuted. What I refuted is in metadata, provenance and consistency: PROV-9 year, the snapshot claim, and `dooring_i` being kept while the five condition fields were dropped for the same reason.

Everything below was rebuilt from the definition on the warehouse's `crashes.csv`. That file is the **2026-11-04** export, not the 10-29 one.

**Claims table**

| Claim | Source | Test | Result | Evidence | Rule |
|---|---|---|---|---|---|
| 998,117 rows, 16 features, 9 splits, no side over 1M | README, C9, R13 | ds.df / make_splits | holds | 998,117 × 16. Largest train side 959,318. 1 row in no split | SPLIT-20 |
| T6/S1/S3: nine 3-month windows, newest first, train ends one month before the window, expanding history | dataset.py splits_comment | train max vs test min per split | holds | Test windows are calendar quarters, 2024Q3 to 2026Q3. Gap is 30–31 days in all 9. No train/test overlap. Train starts 2017-09-01 | SPLIT-10, SPLIT-11 |
| S2: October 2026 excluded, newest test Jul–Sep 2026 | splits_comment | max date | holds | max 2026-09-30 23:00 | — |
| S4: notification strictly before quarter start, and not before the event | splits_comment | eligibility evidence | holds | 18–32 rows removed per split, plus the 1 "before event" row | SPLIT-9, LEAK-12 |
| C2: the gap is about 1% of a training side | curation_comments | gap-month rows ÷ prior rows | holds | 8,604–10,120 ÷ 738k–960k = 0.9–1.4% | SPLIT-10 |
| C2/S3: amendments exist, gap unmeasured | curation_comments | crashes notified before 2026-09-23 in today's export, against the record's 09-23 API counts | holds (gap harmless) | FATAL 1,143 vs 1,142, INCAP 17,680 vs 17,675. Of the +392 rows, 317 are no-injury. At most about 1 net upgrade to fatal in 6 weeks. Monthly fatal share at the release end (Sep 2026: 0.062%) is inside the range of the prior year | SPLIT-10 (amended 2026-11-04: documented late labels justify the gap) |
| W1: one crash notified before its event, unused | accepted warning | lookup | holds | 2018-03-11 03:58 crash, notified 03:01. That is the DST change night, a wall-clock artefact | — |
| C3: hour floor applied to every row | dataset.py | minute/second ≠ 0 | holds | 0 rows | LEAK-13 |
| C3: exact-hour recording 8.21% vs 13.07% on-scene, 18.86% vs 25.09% desk | CC 2026-11-04 | recomputed on the 11-04 export | holds | 8.18% vs 13.02%, and 18.79% vs 25.03% | LEAK-13 |
| Implied: the residual hour signal is not a recording artefact | — | injury share by hour, for exact-time vs other rows | holds | Exact-time rows are less injured (6–10% vs 15–22%) and are most common at night (23–25% at 01–03h), when injury is most common. So the artefact flattens the hour signal rather than inflating it. Raw "12:00" is 1.24% of uninjured rows vs 0.52% of injured, and flooring absorbs it | LEAK-11, LEAK-13 |
| C9: 7.3% vs 15.3% any injury; 4,000–7,000 vs 9,000–10,000 crashes a month | curation_comments | raw counts | holds, approximately | 7.28% vs 15.26%. 2016-01 to 2017-08: 2,539–7,685 a month. 2018–19: 8,625–10,714 a month | SPLIT-20 |
| C9: about 99,100 rows per training side | curation_comments | raw count | holds | 99,101 labeled rows before 2017-09 | — |
| C9: "score unchanged (0.49201 vs 0.49214)" | curation_comments | marks results2.csv | holds, wrong recipe cited | Those numbers are for the retired 21-input set. On the shipped 16 inputs it is 0.49609 (from 2017) vs 0.49600 (from 2013) | SPLIT-21 |
| C8: dropping the five fields costs 0.0039, recorded-flags win back 72%, log loss 0.4960 vs prior 0.6140 | curation_comments | results2.csv | holds | 0.49600 − 0.49214 = 0.00386; flags give 0.49318, so 73% won back. The prior figure is the 2013-history prior; with the 2017 history it is 0.6130 | LEAK-10 |
| C7: all 66 speed values of 99 are in 2015 | curation_comments | raw | holds | 66, all in 2015 (rows before 2017-09, so not shipped) | CLEAN |
| C10: 63 extra source copies on the broad key | curation_comments | raw dedup | holds | 63. Only 1 if control number and report type are also in the key. I did not retest the "36" and "26" sub-counts | LEAK-19 |
| C12/T5: kept "scene facts" do not carry outcome-dependent completeness (implied by the reason the five were dropped) | C1, C5, C8 | share of rows where each kept field is recorded, by injury, within first_crash_type, 2023-07 to 2026-09 | **refuted for `dooring_i`** | `dooring_i` recorded: PARKED MOTOR VEHICLE 0.06% uninjured vs 0.24% injured, SIDESWIPE SAME 0.06% vs 0.47%, OTHER OBJECT 0.54% vs 3.17%, PEDALCYCLIST 9.3% vs 13.7%. A recorded "N" (not dooring) is 55% injured against a 16% base. Dropping it changes log loss by +0.00010, which is noise. `not_right_of_way_i` is recorded more often for uninjured crashes (4.3% vs 2.4%; drop +0.00018). `work_zone_*` show no material difference | LEAK-10 ("missingness that encodes the outcome"), LEAK-6, treat like cases alike |
| C5/T5: first_crash_type is an initial-collision fact | curation_comments | injury share per category | untested (no timeline); accepted approximation | PEDESTRIAN 88% injured, PEDALCYCLIST 72%. Dropping it costs +0.081 log loss. These are physical categories, and none is defined by severity. Whether the value was known at dispatch cannot be checked | USE-3, USE-8, LEAK-10 |
| R12: "REPORTED, NOT EVIDENT" rise is drift, not censoring | record, prep | quarterly shares by report type; notification delay by class | holds | The share rises steadily, 4.1% (2023Q1) to 6.7% (2026Q3). On-scene reports are flat at about 9.5–9.7% since 2024. Desk reports jump from 3.1% to 3.9–4.0% in 2026Q2–Q3. Rows notified more than 33 days after the crash are ≤0.14% in every class, so the release end selects almost nothing by outcome | LEAK-22..26, SPLIT-10 |
| Implied: no row is a copy across the split | — | prep probe; overlap check | holds | 0% exact copies once the hour is included. 22% of test rows match a train row on the coarse non-time features, which is natural (LEAK-18) | LEAK-16..18 |
| Metric: fallback log_loss, no source metric | dataset.py, README | MET-1 look once more (web search) | holds | Only student and case-study projects (accuracy, F1, varied class mappings, varied splits). No competition or defining paper | MET-1, MET-8, MET-11 |
| Metric computable on every fold | MET-2 | `scorer()` with the train-prior dummy on each test fold | holds | All 5 classes in every fold. Fatal 18–34 per fold (the checklist's "20" is wrong: split 6 has 18). Prior log loss 0.567–0.648; uniform 1.609 | MET-2, EV-5 |
| Metric means what it meant | MET-2 | target and classes vs source | holds | Same 5 classes. Only dedup and the 2017-09 start changed. No metrics.md rule asks for an order-aware metric on an ordinal target | MET-2 |
| Metric reason: "…task approved for investigation" | dataset.py metric reason | read | **refuted (stale wording)** | The task was accepted for shipping on 10-29 and re-reviewed on 11-04 | writing.md |
| year = "2017", bibtex year 2017 | dataset.py | the portal grows over time | **refuted** | PROV-9 says a growing register takes the year of the pinned snapshot. Precedents: consumer_complaints_1m and sf_permit_time use `year = "2026"  # the snapshot we pin` | PROV-9 (Must) |
| download_description: "inspected snapshot acquired 2026-10-29; preserve its receipt and hash" | dataset.py | warehouse receipts | **refuted** | `crashes.csv` was downloaded 2026-11-04 10:52Z (Last-Modified 2026-11-03), sha256 `4bf63b07…027b`, 1,109,972 rows. The 10-29 bytes and the container `chicago_traffic_crashes/versions/01a18a0b…` (README build path) are not in the warehouse, and README shows `build_stale: true`. The comment numbers reproduce on 11-04 within 0.07 pp. Sunset header: 2026-12-22 | PROV-9, reproducibility |
| R14: "no panel ran" | record | — | superseded by this panel | — | — |

**Refuted, ranked (validity first, Must first)**

1. **PROV-9 (P5, Must): `year = "2017"` for a growing register.** This sets the wrong year in the collection metadata and is inconsistent with the precedents.
   - Mildest remedy: `year = "2026"  # the snapshot we pin`, and bibtex `year = {2026}`.
2. **Snapshot/provenance claim (P5/procedure).** `download_description` names a 10-29 snapshot whose bytes and hash are no longer in the warehouse. The data that gets rebuilt is the 11-04 export. Nothing scientific changes, since every measured number reproduces, but the stated provenance is false. The export URL also stops working on 2026-12-22.
   - Mildest remedy: rewrite `download_description` to name the 2026-11-04 export and its sha256 `4bf63b07d869d992887c08d70bc017a357f731e6bf563dd6098546417b29027b`, then rebuild before 12-22.
   - The rebuild will produce a new UUID; add a CHANGELOG entry.
3. **`dooring_i` kept while the five fields were dropped (P4, LEAK-10, consistency).** Within the same first_crash_type, injured crashes are 4–8 times as likely to have `dooring_i` recorded. A recorded "N" is 55% injured. This is the mechanism Lennart dropped the five fields for on 2026-11-04. The measured gain is +0.0001, so the score barely moves.
   - Mildest remedy: drop `dooring_i` (consistent, and costs nothing), or keep it with a note that quotes these numbers. Keeping it is a curator weighing call under LEAK-6.
   - Lighter instance: `not_right_of_way_i` is recorded more often for uninjured crashes, which weakens the signal. Keep it with a note (LEAK-11).
4. **Metric reason wording (writing).** "approved for investigation" is stale.
   - Remedy: "…for the accepted five-class probability task."
5. **C9 cites the retired 21-input numbers (writing).** The comment should give 0.49609 vs 0.49600 (shipped 16 inputs). The decision rests on coverage, not on this comparison (SPLIT-21), so it stands.

**Untested, ranked**

1. **Whether first_crash_type, num_units and posted speed were available at first notification (USE-3, LEAK-10).** There is no field-level timeline. first_crash_type carries 80% of the signal. Myunghwan accepted it on 10-29 as an approximation, and `fit = "approximate"` names the gap (USE-8). Leave as is.
2. **Amendment delay (SPLIT-10).** The source has no label versions. My crude bound (at most about 1 net upgrade to fatal in 6 weeks) suggests amendments are rare. The 1-month gap is documented by SR1050 and costs about 1% of each training side, so keep it.
3. **C10 sub-counts (36 matching with control number, 26 additional removed) and C3's 889,076-row / 0.550174 diagnostic.** These belong to the 10-29 snapshot and the 21-input recipe, and cannot be redone on the bytes now in the warehouse.

Sources:
- [Chris Kucewicz, traffic crash prediction case study](https://ckucewicz.github.io/traffic_crash_prediction)
- [NCI thesis, Chicago crash severity (norma.ncirl.ie/7484)](https://norma.ncirl.ie/7484/)
- [GWU capstone report, Giraldo and Ferguson](https://datasci.columbian.gwu.edu/sites/g/files/zaxdzs4746/files/downloads/Capstones/Capstone%20-%20Final%20Report%20-%20Cristina%20Giraldo%20and%20Taisha%20Ferguson%20%282%29.pdf)
- [deepthiab/CarCrashes-Chicago](https://github.com/deepthiab/CarCrashes-Chicago)

</details>

<details><summary>Column audit</summary>

**Column audit: chicago_traffic_crashes (column-auditor, second pass, 2026-11-04)**

**Answer to focus.md.** focus.md asks for nothing beyond the standard panel. My answer: no column of the shipped frame has to leave. There is no LEAK-10 leak and no Must-level cleaning fault. What remains is one stale note, one question about the target's drift, and three weak recording observations. I measured those three; none carries a gain, so they stay.

The frame was loaded from the definition through `dataset_io.from_definition`: 998,117 rows, 15 inputs, 9 temporal splits. The prediction point (C1) is "an approximate scene-based injury assessment from finalized crash and road facts, before using the injury classification itself". Meanings come from the portal field dictionary (Socrata metadata of 85ca-t3if).

**Column table**

| column | meaning | known at prediction? | dtype and cleaning | verdict | rule |
|---|---|---|---|---|---|
| most_severe_injury (target) | most severe injury of anyone involved | label | ordered category O<C<B<A<K (no indication < reported not evident < nonincap. < incap. < fatal), which matches KABCO; 5 classes kept; missing labels dropped | fine. "REPORTED, NOT EVIDENT" share z +8.6 to +11.4 from 2025Q1: question below | CLEAN-25, CLEAN-17, CLEAN-15 |
| crash_date | date and time of the crash as entered by the officer | yes (event time) | datetime floored to the hour; 0 rows with nonzero minutes remain; 2017-09-01 to 2026-09-30 23:00 | fine; the class-dependent exact-hour recording is harmonised | LEAK-13 |
| posted_speed_limit | posted limit as determined by the officer | yes | float, 46 values, 0 to 70. 0 occurs 5,060 times (0.51%, 39% of them in parking lots, 8.4% injured vs 15.3% base). 621 values are not multiples of 5 (3 mph ×238, 39 ×100) | fine as settled ("leave as it is", 2026-10-29); the C7 note is stale (problem 2) | CLEAN-10/11 (settled), writing |
| first_crash_type | type of the first collision | yes (scene fact) | category, 18 levels, no unknown code | fine. Strongest real signal (AUC 0.765 alone; all features 0.730, 0.594 without it). It names *which* event came first, not its severity (PEDESTRIAN 88% injured is the physics of the crash) | LEAK-10 holds; C5 |
| trafficway_type | trafficway type per officer | yes | category, 18 levels. UNKNOWN (11,918; 6.9% injured) and NOT REPORTED (976; 32.9%) both become missing (1.29%). Missing share in desk reports (2023+): 2.45% uninjured vs 1.59% injured | fine. The dtype flag (`ordinal_like`/`open_end` on "FIVE POINT, OR MORE") is a false alarm: the column is a nominal road layout. The missingness pattern carries no gain (probe below) | CLEAN-14, LEAK-10/38 tested |
| not_right_of_way_i | first contact outside the public right-of-way (API `private_property_i`) | yes | category Y/N, 95.6% blank. Y 40,183 (8.9% injured), N 4,167 (15.2%), blank 15.5%. In practice blank means N | fine | CLEAN-14 |
| street_no | street address number per officer | yes | float, 0 to 13,799, integers only. 1 occurs 4,160 times, mostly real addresses (TERMINAL ST 649, parking-lot streets); 0 occurs 8 times (valid on the Chicago grid) | fine: a position on the address grid, kept numeric | CLEAN-14 |
| street_direction | N/E/S/W of the address | yes | category, 1 missing | fine | |
| street_name | street name per officer | yes | category, 1,627 levels (a closed set of city streets) | fine. Locations recur across windows; that is legitimate for a known location under a temporal split | CLEAN-14, USE-10, LEAK-34 |
| beat_of_occurrence | CPD beat ID | yes | category, 278 codes (31 to 6100) | fine. The `numeric_levels` flag is a false alarm: an administrative code (district + sector + beat), and lat/lon already carry the location | CLEAN-14 (code) |
| dooring_i | a door opened into a cyclist's path | yes | category Y/N, 99.68% blank. Y 76% injured, N 54%. N is filled mostly in cyclist crashes (504 of 1,016). The ~300 N rows in other crash types are injured more often (parked vehicle 12.3% vs 3.9%, n=130) | fine (fill gain measured as none) | LEAK-10/38 tested |
| work_zone_i | crash in an active work zone | yes | category Y/N, 99.49% blank. N 22.1% injured vs Y 17.0% (n=1,264) | fine (as above) | same |
| work_zone_type | type of work zone | yes | category, 3 levels; UNKNOWN (544) becomes missing | fine | CLEAN-10 |
| workers_present_i | workers present in the zone | yes | category Y/N, 99.86% blank | fine | |
| num_units | number of units (vehicles, pedestrians, cyclists) | yes (scene count) | float, 1 to 18; a count, so numeric is right | fine | CLEAN-14 |
| latitude / longitude | geocoded from the reported address | yes | float. Zeros become missing (0.82% missing); no point left outside the Chicago box. Missing rows are 12.6% injured vs 15.3% | fine (weak; probe below) | CLEAN-11 |

The exclusions match LEAK-2's sibling sweep: injury counts, CRASH_TYPE, DAMAGE, REPORT_TYPE, photo/statement flags, contributory causes, INTERSECTION_RELATED_I, HIT_AND_RUN_I, DATE_POLICE_NOTIFIED, CRASH_DATE_EST_I, the five condition fields, LANE_CNT/ALIGNMENT/ROAD_DEFECT, the redundant hour/day/month/LOCATION columns and the ids. None of these reaches the frame.

**Decisive experiment for the LEAK-2 sweep (EV-1)**

The five condition fields were dropped because 72% of their gain was whether the field was filled in. So I tested the same mechanism on the remaining sparse or missing-bearing columns: trafficway_type, lat/lon, the 4 Y/N flags and work_zone_type. Setup: untuned LightGBM (lr 0.1, 200 rounds), the three newest shipped splits, mean log loss.

| variant | mean log loss | splits 0 / 1 / 2 |
|---|---|---|
| core (the 8 suspect columns dropped) | 0.51723 | 0.5437 / 0.5236 / 0.4844 |
| core + 7 "is filled" flags | 0.51762 (−0.0004 vs core) | 0.5429 / 0.5253 / 0.4847 |
| full shipped inputs | 0.51506 (+0.0022 vs core) | 0.5399 / 0.5204 / 0.4849 |
| full, N of the 4 Y/N flags set to missing | 0.51619 | 0.5441 / 0.5208 / 0.4838 |

Recording state alone adds nothing; what these columns add comes from their values. That separates them from the five dropped fields, so LEAK-10/LEAK-38 do not trigger. Absolute losses sit above the record's 0.496 (different, untuned model), and the split-to-split noise is about ±0.003, so only the comparisons between variants are meaningful.

**Problems, ranked (principles.md: P-rank, then strength, then size)**

1. **P3/P4, question for the curator (USE-5, LEAK-24; Should).** The target's meaning may be shifting in the test windows. "REPORTED, NOT EVIDENT" stands at 6.07% to 6.74% in each of the 7 newest quarters (z +8.3 to +11.4; pooled z up to +42), while incapacitating falls (pooled z −6.5). There is no fall at the release end, so this is not right-censoring. The probe already reads it as drift. A jump of this size starting in 2025Q1 may also be a change in how officers code C-injuries; four of the nine test windows (2025Q3 to 2026Q3) sit inside it. Mildest remedy: note it in `splits_comment`, or check for a 2025 change in the SR1050 form or CPD practice. It does not block shipping.

2. **Writing/procedure: stale note (C7).** The bullet still says "All 66 source values of 99 occur in 2015 ... keep speed with this historical-code uncertainty". Since SPLIT-20 (training starts 2017-09-01) none of those rows is in the frame: the maximum is 70. The remaining speed oddity is the 5,060 zeros (0.51%, 39% in parking lots, injury rate 8.4%) plus 621 values that are not multiples of 5. The treatment itself was settled on 2026-10-29 and should not be reopened. Remedy: reword C7 so it says the 2015 code-99 rows now fall outside the frame, and give the zero count.

3. **P4, weak; keep with or without a note (LEAK-10 tested, LEAK-6).** Missingness differs by class in three columns:
   - trafficway_type: missing in 2.45% vs 1.59% of desk reports, uninjured vs injured;
   - dooring_i and work_zone_i: N filled more often on injury reports (about 1,500 rows);
   - lat/lon: missing rows 12.6% vs 15.3% injured.

   The experiment above shows no gain from any of this (−0.0004). LEAK-10 is not triggered. Remedy: none, or one line with these numbers so the sweep shows on record.

4. **P7, minor (CLEAN-10).** NOT REPORTED (976 rows, 32.9% injured) and UNKNOWN (11,918, 6.9%) in trafficway_type are merged into one missing value. Both are recording states, not road facts, so CLEAN-10 makes them missing. Merging them blurs a small outcome-related signal, which is the safer direction. Fine as is.

5. **Procedure, cosmetic.** `_feature_types` declares `date_police_notified` as a datetime although `_make_splits` drops it before the frame ships. The check passes. No action needed, or drop it from the declaration.

**Dtype probe, answered**

- `trafficway_type`: false alarm. It is a nominal layout, and "FIVE POINT, OR MORE" is not a count band of this column.
- `beat_of_occurrence`: false alarm. It is an administrative code, and categorical is right under CLEAN-14.
- Unflagged columns: counts and measured quantities are numeric (num_units, posted_speed_limit, street_no, lat/lon). Codes are categorical. The only ordinal is the target, and its KABCO order matches the codebook.

**Judgment record**

Verdict: ready with the column set as shipped.
- Validity: LEAK-10 holds for all 15 inputs; LEAK-2 sweep extended and measured (fill-state gain −0.0004); LEAK-13 holds (hour floor; no minutes remain).
- Value: first_crash_type carries most of the signal, and it is real (TP).
- Quality: CLEAN-14 and CLEAN-25 hold; C7 wording is stale.
- For the curator: issue 1, a question (what the target means in the 2025-2026 windows); issue 2, a wording fix.

</details>

<details><summary>Split audit</summary>

**Verdict: right with notes.** The temporal split fits the use case. The one-month gap can now be backed by a measurement instead of the 30-day convention. Nothing in the split needs to change.

**focus.md** asks nothing beyond the standard panel, so the standard question is the one to answer: is the temporal split right? Yes. Each prediction is a new crash at a known place in a continuing stream of crashes. In the newest window, 82.2% of test crashes have a latitude/longitude seen in training and 75.1% an address seen in training. So location is a feature that new rows keep, not an entity to hold out (USE-10, SPLIT-4). A random split scores no better than the temporal one (numbers in section 2).

**Checks that hold (numbers from the definition's own frame and splits, 998,117 rows)**

- **Regime (SPLIT-1/2/3, USE-10).** Time-ordered events, so temporal is right. Grouping by location or beat would be wrong: new crashes keep those values. No group or hidden-group probe is needed.
- **Time column.** `crash_date` is the event time. Cohorts use the original timestamp; only the returned predictor is floored to the hour. Data runs from 2017-09-01 00:01 to 2026-09-30 23:55.
- **Windows (SPLIT-11/14/15/17).**
  - Nine contiguous calendar quarters, from 2024-07 to 2026-09.
  - Test windows hold 24,682 to 29,258 rows each, with 18 to 34 fatal crashes (TP-9 holds).
  - Train sides are expanding and hold 74.0% to 96.1% of all rows, so no side falls below 50%.
  - No row is in both train and test.
  - Train always ends one month before the window: for window 0, the last training crash is 2026-05-31 23:50 and the test starts 2026-07-01.
- **Seasons (SPLIT-20).** No test set is season-shaped. Q3 appears three times, the other quarters twice each. Q3 is the injury peak (17.7% to 18.1% any injury) and Q1 the low (15.1% to 15.5%).
- **Unknown label at the prediction point (SPLIT-9).** The notification filter removes only 16 to 32 training rows per window. Notification delay: median 0.02 days, 99th percentile 9.05 days, 0.157% over 30 days. One row is notified before its crash; it is the accepted `splits_rows_unused` warning.
- **Training history (SPLIT-20/21).** Training starts at 2017-09-01, the citywide coverage break (7.3% against 15.3% any injury). The start was set from that break, not from the 0.49201 vs 0.49214 score comparison, so SPLIT-21 holds.
- **Copies across the split (LEAK-16..21).**
  - With the hour included, 0% of test rows have an exact copy in train.
  - The 22.2% copy rate without time comes from coarse scene features.
  - Rows identical down to the hour share a timestamp, so they cannot end up on opposite sides; the gap month separates the sides further.

**Alternative splits fitted (quick LightGBM, 150 rounds, 4 threads)**

| Split | Window | Log loss | Prior | Skill |
|---|---|---|---|---|
| Shipped (gap 1), seeds 0/1/2 | w0 (2026Q3) | 0.5388 / 0.5370 / 0.5356 | 0.6481 | 0.169 to 0.174 |
| Gap 0, seeds 0/1/2 | w0 | 0.5344 / 0.5338 / 0.5350 | 0.6480 | 0.174 to 0.176 |
| Gap 2, seeds 1/2 | w0 | 0.5386 / 0.5361 | 0.6482 | 0.169 to 0.173 |
| Gap 0 / 1 / 2, without the time-as-number feature | w0 | 0.53453 / 0.53463 / 0.53468 | | 0.175 |
| Shipped / gap 0, seeds 0/1/2 | w4 (2025Q3) | 0.5377, 0.5361, 0.5353 / 0.5371, 0.5368, 0.5362 | 0.6442 | 0.165 to 0.169 |
| Shipped / gap 0 | w8 (2024Q3) | 0.5349 / 0.5339 | 0.6404 | 0.165 / 0.166 |
| IID, random hold-out of the same size, 2 draws | whole period | 0.4740 / 0.4845 | 0.5715 / 0.5779 | 0.171 / 0.162 |

What this shows:

- **Random split.** Skill under a random hold-out (0.162 to 0.171) is the same as under the temporal split (0.165 to 0.169). Its lower raw log loss only reflects a different class mix. The temporal split costs nothing measurable, and the regime is decided by the use case anyway (SPLIT-4).
- **The gap's cost is negligible.** Without a numeric time feature, each month of gap costs 0.0001 log loss. With it, gap 0 is about 0.003 better on w0, which is the same size as the seed spread (0.003), and there is no difference on w4. The apparent cost is a tree model extrapolating the time feature, not lost information.
- **The gap cannot hide a shortcut here.** All labels come from the final snapshot, so there is no unmatured-label shortcut for a gap to remove. It only simulates refit realism.

**Problems, ranked by `principles.md`**

**1. P4, SPLIT-10 (Should): the gap is called "not measured", but it can be measured.**

- **Where the text says it.** `splits_comment` ("the gap is set by that 30-day convention, not measured"), the late-labels bullet of `curation_comments`, and the 2026-11-04 assessment.
- **Where the measurement comes from.** The portal's row system field `:updated_at`. I pulled it for 1,010,730 rows on 2026-11-04. The table was bulk-reloaded on 2026-05-21 (1,041,566 rows share that `:updated_at`), and rows since then are written one by one.
- **Results for crashes from June to August 2026 (29,220 rows):**
  - First publication: median 1.3 days after the crash, 99th percentile 14.1 days.
  - 99.2% of rows are rewritten after publication.
  - Last update: median 16.1 days after the crash, 99th percentile 22.0 days. Only 0.63% are updated after 30 days, and 0.34% after 45 days.
  - Fatal crashes, May 22 to Sep 14 (32 rows): 5 were last updated after 30 days (at 32.6, 39.7, 43.3, 50.5 and 101.9 days).
- **The roughly 16-day rewrite does not shift the label.** Injury shares in the API pull by crash age:
  - Before the update (ages 0 to 17 days): any injury 18.4% to 19.8%, fatal or incapacitating 1.7% to 2.0%.
  - After it (17 to 120 days): any injury 17.5% to 18.9%, fatal or incapacitating 1.5% to 2.0%.
  - So there is no right-censoring at the release end, which matches leak probe 13.
- **Limits of the measurement.**
  - `:updated_at` records an update to any field, not specifically the label.
  - History before 2026-05-21 is hidden by the reload.
  - 2,186 crashes from before April 2026 were rewritten after the reload, 1,904 of them in one batch on 2026-11-03; whether their labels changed is unknown.
- **What follows.**
  - The source documents late amendments (SR1050), so the amended SPLIT-10 keeps the gap.
  - The measurement shows one month covers 99.4% of rows' last updates. It does not cover the long tail of fatal-report amendments; a 2- to 3-month gap would cover 4 of those 5 late fatal records at a training cost near zero.
  - The record says the gap costs "about 1%" of a training side; the measured share is 1.0% to 1.4% (8,604 to 10,120 rows against 738,598 to 959,318).
- **Mildest remedy: a note only.** Replace "not measured" with these figures and keep the one-month gap. Optional, the curator's call: widen to 2 months. Either way, write down that `:updated_at` is a field-agnostic proxy.

**2. P4, SPLIT-20 (Should): drift in the training history is described with the wrong date.**

- **What the shares show.** The share of "REPORTED, NOT EVIDENT" stepped up in 2023Q4 (from 4.71% in 2023Q3 to 5.56%) and then rose slowly. All nine test windows sit in the new level (6.07% to 6.74%). Most of the training history, 2017 to 2023Q3, sits at the old level (about 4.1% to 4.7%).
- **Where it is misdated.** The prep report and checklist date the rise "from 2025Q1"; the record's 2026-11-04 assessment has it in 2026Q2 to Q3. The quarterly shares put the step at 2023Q4, before every test window.
- **Is it a split problem?** No. It is real drift that a refit model would face, and the temporal split already measures it: random and temporal skill are equal. The citywide-coverage start date is still the right choice.
- **Mildest remedy:** a sentence in `splits_comment` noting the 2023Q4 recording-level step and that every test window falls after it. Its cause (a change in reporting practice?) stays a question for the curator under USE-5, not the split.

**3. P7 and procedure, robustness (no rule broken): the notification cutoff assumes calendar quarters.**

- **What the code does.** The cutoff is `event.iloc[test].min().to_period("Q").start_time`. It equals the window start only because the data is cut at 2026-10-01, which makes the windows calendar quarters.
- **What happens if the cut moves.** If a rebuild cuts at another month (the export URL stops working on 2026-12-22 and a new snapshot may be used), windows shift off quarters. The cutoff would then fall before the window start: stricter than needed, so still safe, but it would no longer match `splits_comment` ("actual calendar-quarter start").
- **Mildest remedy:** a note in `splits_comment` that windows align with calendar quarters only because of the 2026-10-01 cut.

**4. Not a split defect (a modelling note for the benchmark notes, optional): the hour-floored `crash_date` read as a number costs 0.001 to 0.004 log loss on w0.** With it, gap-1 runs score 0.5356 to 0.5388; without it, 0.5346. This is model-side extrapolation of the time feature; the split is fine.

**Judgment record**

```text
Verdict: split right with notes.
Validity: USE-10 holds (known locations, new crashes); SPLIT-1/2/3/4 hold (temporal; IID skill 0.162-0.171 vs temporal 0.165-0.169);
SPLIT-9 holds (16-32 late-notified rows filtered); SPLIT-10 holds, its "not measured" text now measurable (99.4% of rows last updated
within 30 days, median 16.1 days; fatal tail 5/32 at 33-102 days; no label shift at the update); SPLIT-11/14/15/17 hold
(9 quarters, 74-96% train, 24.7-29.3k test rows, 18-34 fatal); SPLIT-20/21 hold (start at the coverage break; drift step 2023Q4
noted); copies across the split 0% with the hour.
For the curator: issue 1 (gap text, optionally a 2-month gap for the fatal tail); issue 2 (date of the recording-level step).
```

</details>

<details><summary>Domain practitioner</summary>

**chicago_traffic_crashes: domain-practitioner review (second pass, 2026-11-04)**

**Focus question.** `focus.md` sets no question beyond the standard panel. My direct answer: the task is a real use case at fit **approximate**, and the metric scores the decision only **partly**. Neither blocks shipping. Gap 1 should change the wording of the use case.

**Fit: approximate.** No dispatcher faces these rows. About half are crashes that no one was dispatched to, the input a dispatcher always has (the caller's account of injuries) is absent, and the label is the officer's later KABCO judgment (the five-level police scale: K fatal, A incapacitating, B nonincapacitating, C possible, O none). The shipped data fits a second actor better, a city road-safety analyst, but some gaps remain for that actor too (USE-8, USE-9).

**1. Do I have each input at the moment of prediction? (as a CFD/OEMC dispatcher at the 911 call)**

- **Have:** location (lat/lon, street, beat), hour, roughly the number of units, and whether a pedestrian or cyclist was struck.
- **Have only roughly:** `first_crash_type`. The officer codes it after investigating, following the manual's rules for the first damage or injury event. It is the strongest feature (AUC 0.765 alone; all features without it reach 0.594). At call time I know "ped struck" or "rear end", not the coded value. This is accepted as an approximation (C1, record R9).
- **Missing, though I would always have it:** the caller's statement ("someone is down", "bleeding", "trapped"), the protocol determinant code, and vehicle telematics for connected cars. Real triage rests on these (USE-6). The model gets less information than the human it would support.
- **Have but dropped:** posted speed is kept. As a safety analyst I would have lane count, alignment, traffic control device and lighting from the city's road and signal inventory, independent of the crash. They were dropped (C6, C8) because the crash report fills them in more completely for injury crashes. That was the right call for the report fields, but the underlying facts are legitimate.

**2. Is the target what I act on?**

It is a proxy. As a dispatcher I act on "send ALS/BLS, how many units". As a safety analyst I act on KSI (killed or seriously injured, K+A) per site. The officer's KABCO label is the standard input for both, but it is noisy:
- A North Carolina study (2024) linking crashes to the trauma registry found police KABCO catches only about 50% of serious injuries.
- Linkage studies in Hong Kong (2009) and England (2012) also report misclassification, in both directions depending on the reference standard.

I would want a probability, ideally P(KSI) and P(any injury needing transport). The five classes are acceptable because they are ordered (CLEAN-25) and can be collapsed.

The label also drifts, measured on the raw export (2017-09 to 2026-09, 998,177 labeled rows):
- C ("reported, not evident") rises from 4.2% (2018-2022) to 4.7% (2023), 6.0% (2024) and 6.6% (2026).
- K+A falls from 2.0% to 1.4%.
- The on-scene share stays flat at about 46%, so this is not a shift in report mix.

This looks like a change in how officers record injuries (USE-5, LEAK-22..26), and it lands in the newest test windows. I found no IDOT form change after 2019 that explains it.

**3. Does one row match one decision? Is the test data what I would face?**

**Row vs decision: no for half the rows.**

| Report type | Share of rows | Any injury | K+A | Notified within 1 h of crash |
|---|---|---|---|---|
| Desk report (filed at the district, no dispatch) | 50.9% (508,086) | 5.3% | 0.31% | 40% |
| On scene | 45.4% (453,527) | 25.5% | 3.27% | 91% |

A dispatcher never sees a desk report. Mixing the two populations inflates the measured skill. My quick LightGBM, trained before 2026-06 and tested on Jul-Sep 2026, on roughly the shipped features:

| Rows scored | Model log loss | Prior log loss (report-type-specific) | Skill | KSI AUC |
|---|---|---|---|---|
| All 28,987 | 0.531 | 0.648 | 18.0% | 0.842 |
| On scene, 12,535 (the dispatcher's population) | 0.797 | 0.904 | 11.9% | 0.787 |

Part of the headline score is "recognise a parked-car desk report".

**Test data: yes.** The next quarter in the same city, refit quarterly with a one-month gap for amended labels, is how I would deploy. Recurring locations are correct for a known road network (USE-10). There is no unseen-site evaluation, and I would not need one.

**4. Would I use this model?**

- **As a dispatcher: no.** It lacks the caller's injury report, and I could not trust a score that is partly fitted on crashes I never handle.
- **As a Vision Zero / CDOT analyst: yes, as a crash-level severity model** for screening sites and estimating expected KSI.
  - What would make me trust it: calibration of P(K+A) within the on-scene population and for pedestrian and cyclist crashes. In my test, the top 5% of crashes by P(K+A) hold 33% of the 474 KSI crashes.
  - What would make me distrust it: the C-class drift, and log loss that improves mainly by sorting O/C/B.

**5. Does the declared metric score my decision? **Partly.****

Multiclass log loss is a strictly proper rule (MET-8), at the unit I score (a crash), and preferred over multiclass AUC (MET-11). The fallback origin is honest: no source metric exists (MET-1).

On the newest window, the per-class shares of the 0.531 loss are:

| Class | Loss contributed | Share |
|---|---|---|
| C (reported, not evident) | 0.186 | 35% |
| B (nonincapacitating) | 0.177 | 33% |
| O (no injury) | 0.112 | 21% |
| A + K | 0.056 | 10.5% |

So the score is mostly about telling O, C and B apart. C is the least reliable class and the one drifting. K+A, which I act on, carries about a tenth of the score. Log loss also ignores the class order: a fatal crash predicted as O costs the same as one predicted as A.

**The metric I would choose:** the ranked probability score over the ordered KABCO classes. It is strictly proper, uses the CLEAN-25 order, and penalises mass far from the true class. That makes K+A errors count more without inventing a cost matrix (MET-7 forbids invented costs). It is not in `data_foundry.v2.metrics`, so adding it falls under MET-13, and declaring it would be a "context" origin, which MET-11 allows only when the context is clear. If not adopted, keep `log_loss`, and say in the reason that K+A carries about 10% of it.

A KSI-only binary score (`roc_auc` on K+A) would match the safety analyst's decision directly, but it changes the target. That is the curator's call (USE-5).

**Gaps ranked by how much they change the task**

1. **Population mismatch for the stated actor (USE-1, USE-3):** 50.9% desk reports, never dispatched. On-scene skill is 11.9% against 18.0% overall. Fix: re-word the use case (gap 1 under "What an expert would change").
2. **The dispatcher's main input is absent (USE-6):** the caller's injury report and determinant code. Not repairable from this source. It makes the dispatch actor a weak framing.
3. **Label quality and drift (USE-5, LEAK-22..26):** KABCO sensitivity for serious injury is about 50% in linkage studies. C rose from 4.2% to 6.6% and K+A fell from 2.0% to 1.4% in the test period. The notes call it drift (record R12, checklist P3/P4) but do not name it as a possible change in recording practice.
4. **`first_crash_type` is coded by the officer (LEAK-10, accepted, C5):** it carries most of the signal, and at call time only a coarse version exists. Accepted, and correctly named in the notes.
5. **Metric weight is on the unreliable classes (MET-1):** see question 5.
6. **Road facts dropped for the analyst framing (C6, C8):** lane count, alignment, control device and lighting exist independently in city inventories. Dropping them is safe but loses legitimate signal for that actor.
7. **Smaller items:** the label snapshot is final and the one-month gap is set by convention, not measured (SPLIT-10, documented). The metric reason still says "approved for investigation", which is stale wording.

**What an expert would change**

1. Rewrite `use_case` under USE-9 to the safety analyst: "a city road-safety analyst estimates, for each reported crash, the probability of each KABCO level from the road and crash facts, to estimate expected KSI by site and rank sites for countermeasures". This matches every row, the finalized-report inputs and the quarterly refit. Fit stays approximate because of the label quality and the road facts the crash report records less completely for minor crashes. Keep the dispatch sentence only as a secondary reading, or drop it.
2. If the dispatch actor is kept instead, add a filter "on-scene reports only". REPORT_TYPE is known to the dispatcher, because a police response happened. That accepts a 54% smaller frame.
3. Name the C/K+A drift from 2023 onward in `curation_comments` as a possible change in recording practice, with the yearly shares above.
4. Consider the ranked probability score over KABCO (MET-1, MET-8, MET-11 context, MET-13), or at least state in the metric reason that K+A carries about 10% of the loss. Replace "approved for investigation".
5. Longer term (a new task, not this one): join the CDOT signal and centerline inventories by location to restore the road facts without report-dependent completeness.

**Sources**

- [City of Chicago portal, Traffic Crashes - Crashes](https://data.cityofchicago.org/Transportation/Traffic-Crashes-Crashes/85ca-t3if)
- [IDOT SR1050 instruction manual (2013)](https://www.nhtsa.gov/document/illinois-sr-1050-instruction-manual-2013)
- [IDOT training page (2019 SR1050 updates)](https://idot.Illinois.gov/transportation-system/local-transportation-partners/law-enforcement/training.html)
- [North Carolina trauma-registry linkage, Traffic Injury Prevention 2024](https://informahealthcare.com/doi/full/10.1080/15389588.2024.2361052)
- [SWOV, misclassification of injury severity in police reports](https://swov.nl/en/publicatie/misclassification-injury-severity-among-road-casualties-police-reports)
- [Hong Kong police/hospital linkage](https://research.polyu.edu.hk/en/publications/misclassification-of-injury-severity-among-road-casualties-in-pol/)
- [UK DfT police/hospital (HES) linkage](https://assets.publishing.service.gov.uk/media/60d05871d3bf7f4bcfe765e7/hes-linkage.pdf)
- [Madison HIN methodology (KSI weighting)](https://www.cityofmadison.com/transportation/documents/vision-zero/HIN%20Methodology.pdf)
- [WPRDC High Injury Network](https://data.wprdc.org/dataset/high-injury-network)

</details>

<details><summary>Blind review</summary>

**Verdict:** Include with changes. This is a real, large, leakage-free crash-severity task with modest but real signal under an honest temporal split. Before it goes in, the mislabeled `not_right_of_way_i` column needs fixing, the dropped pre-crash condition columns should come back, and the metric has to cope with very rare top classes.

**What the task is.** Each row is one crash report from the Chicago Police E-Crash system. The target is `most_severe_injury`, with 5 ordered levels from no indication of injury up to fatal. The people who would make this prediction are city safety analysts (Vision Zero), insurers and EMS planners: given the crash setting and the collision type, how likely is a serious injury? Most crash-severity papers do exactly this. It is a real use, but more for risk analysis than a live decision. The collision type (`first_crash_type`, `num_units`) is only known once the crash has happened, so the honest framing is "at the time the report is filed, before injuries are assessed".

**Leakage, split and duplicates.** The preparer dropped every outcome column: `injuries_*`, `crash_type` ("Injury and/or Tow Due to Crash" vs "No Injury / Drive Away"), `damage`, `prim_contributory_cause`, `report_type`, `hit_and_run_i`, `photos_taken_i` and `statements_taken_i`. That was right. On API data, adding `crash_type` cuts log loss from 0.46 to 0.29, so it is a near-copy of the target.

`crash_date` is rounded to the hour (0 rows have non-zero minutes). That is fine, and it also removes the "estimated time on the hour" artifact of desk reports. The data are sorted by time and run from 2017-09-01 to 2026-09-30. This matches the source note that "citywide data are not available until September 2017". A temporal split is the right regime. There are 18 exact duplicate rows in the 200k sample, which is negligible and plausibly separate crashes.

**Ranked concerns**

1. **`not_right_of_way_i` is most likely the source's `private_property_i` under a name that does not exist in the source, and that name suggests the wrong meaning.**
   - The public API rejects the name: "No such column: not_right_of_way_i".
   - The rates match `private_property_i` exactly: Y 4.06% / N 0.42% in the sample, against Y 44,721 / N 4,559 of 1,110,250 (4.03% / 0.41%) in the source.
   - The source defines `private_property_i` as "Whether the crash begun or first contact was made outside of the public right-of-way". A reader would take "not right of way" to mean a right-of-way violation, which is a fault or cause variable.
   - Fix: restore the source name, or document the mapping.

2. **Legitimate pre-crash conditions were dropped with no reason given.**
   - Removed: `weather_condition`, `lighting_condition`, `traffic_control_device`, `device_condition`, `roadway_surface_cond`, `road_defect`, `alignment`, `lane_cnt`, `intersection_related_i`.
   - These are officer-recorded in the same way as the kept `posted_speed_limit` and `trafficway_type`. None is an outcome.
   - On 399k API rows from 2023 to 2026 (train before 2025-07, test after), adding them lowers test log loss from 0.4980 to 0.4924. That is a small but real gain, and it makes the table richer and more typical of the task.
   - Fix: restore them. Their "UNKNOWN" levels can stay as a category.

3. **The top classes are very rare and the classes are ordered.**
   - Sample class shares: no injury 84.8%, non-incapacitating 8.5%, reported-not-evident 4.9%, incapacitating 1.7%, fatal 0.107% (214 rows).
   - Full data: about 1,086 fatal over 9 years. Spread over 9 test windows, each window holds only on the order of 100 fatal rows.
   - Majority-class accuracy is 0.84, and a LightGBM model only reaches 0.843 accuracy and 0.255 balanced accuracy. Accuracy and F1 would therefore be meaningless.
   - Fix: score with multiclass log loss or one-vs-rest AUC. Alternatively, merge FATAL and INCAPACITATING into one "KSI" (killed or seriously injured) class, which is the standard road-safety grouping.

4. **The signal is modest, and the label is noisy and depends on how the crash was reported.**
   - LightGBM trained before 2025 and tested on 2025–2026 (sample, all columns): log loss 0.570 vs 0.607 for the class prior. One-vs-rest AUC is 0.756; "any injury" AUC is 0.776.
   - Most of the signal comes from `first_crash_type`: PEDESTRIAN has only 12% no-injury and PEDALCYCLIST 29%, against 96% for PARKED MOTOR VEHICLE.
   - The source says "About half of all crash reports, mostly minor crashes, are self-reported at the police district". The injury level is the officer's judgment, and "REPORTED, NOT EVIDENT" means claimed pain. The labels are therefore noisy, with a different noise level for desk and on-scene reports. That is acceptable for a benchmark, but should be documented.
   - The task is not trivial, has learnable structure and is well above the size needed to score it.

5. **Drift over time.**
   - The no-injury share falls from 0.860 (2017) to 0.831 (2026). The fatal share swings between 0.05% and 0.14% by year.
   - The temporal windows handle this honestly. It also makes the early windows, which have little training history, noisier.

6. **Minor preparation issues.**
   - `posted_speed_limit` has 1,021 rows (0.5%) equal to 0 and odd values such as 1, 3 and 39. These are likely unknown placeholders or typos; leave them or set 0 to NaN.
   - `street_name` (1,441 levels) and `beat_of_occurrence` (276) are stored as categories. Native LightGBM categorical handling overfits on them: adding `street_name`/`street_no` worsens log loss from 0.521 to 0.537. That is a fair challenge for methods rather than a preparation error, but `beat_of_occurrence` could be stored as a code.
   - The work-zone and dooring flags are 99.5–99.9% missing. That is how the source records them (NaN means not flagged). Encoding NaN as "N" would be clearer.
   - `latitude`/`longitude` are missing in 0.8% of rows; the rest fall within Chicago.
   - Calendar features (hour, day of week, month) were removed as redundant with `crash_date`. That is fine provided the benchmark derives them from `crash_date` and does not drop the datetime column.

**What I could not check**
- How the 9 test windows are placed and sized. Only the regime is stated, so I could not confirm how many FATAL rows each window holds.
- Why the full table has 998,117 rows when the API filter gives 998,177 (1,000,427 rows from 2017-09 to 2026-09, minus 2,250 with no target). The 60-row gap is probably extra deduplication or a different snapshot date.
- Whether reports amended later change the target after the fact. The source says amendments are folded in, so a few labels may reflect follow-up information.
- Whether `report_type` (desk vs on-scene) was dropped on purpose. It is known when the report is filed but strongly tied to severity. I would keep it out, but the decision should be written down.

Sources:
- https://data.cityofchicago.org/Transportation/Traffic-Crashes-Crashes/85ca-t3if
- https://data.cityofchicago.org/api/views/85ca-t3if.json (column metadata)
- https://data.cityofchicago.org/resource/85ca-t3if.json (API queries)

</details>

<details><summary>Task gamer</summary>

The task is close to clean. The only exploit that holds up is one ordering artifact, and it gains about 0.001 log loss (0.2%). Nothing I found hurts an honest model.

**Setup.** The task has 998,117 rows and 9 temporal splits. Each test window is 3 months, with a 1-month gap after the training data. The untuned LightGBM, with time expanded into hour, day of week, month and day index, averages log loss **0.5140**. A more regularised honest LightGBM averages **0.4927** (from 0.4622 to 0.5206 per split). It codes street_name and beat as integers plus their frequency, uses min_child_samples=200 and subsampling, and is in `better.py`. The untuned model overfits the 1,627-level `street_name` categorical. Adding a random column to it moves the score by -0.0017 to +0.0030 per split, so I measured the exploits against the regularised model. A random column there moves the score by **-0.0007 to +0.0009** per split (two seeds).

| # | Exploit | Script | Honest score | Exploited score | Gain (per split, range) | A deployed model has it? | Fix |
|---|---|---|---|---|---|---|---|
| 1 | Row order within the hour stands in for the crash minute: `crash_date` was rounded to the hour but rows keep the source's minute order. Features: rank in the hour, row count in the hour, relative rank | `better.py B_order` (and `exploit_order.py order` on the untuned model) | 0.49269 | 0.49171 | +0.00098 mean (+0.00008 to +0.00202; positive on all 9 splits; random column -0.0007 to +0.0009). Untuned model: +0.0017 (-0.0002 to +0.0034) | Partly. The police record the minute, but not where a crash ranks among every crash of that hour, including reports filed later. | Shuffle rows within each `crash_date` hour, or sort the file by a random key. |
| 2 | Counts over train and test together: crashes in the hour, in the day, relative to nearby days, and at the same address in the same hour | `better.py B_comp`, `exploit_composition.py` | 0.49269 | 0.49244 | +0.00025 (-0.00025 to +0.00086): noise | No. These are final counts that include crashes after the prediction. | None needed. |

**Finding 1.** In the published source, the 17 crashes from 2026-07-01 00:00 to 03:00 appear in exactly the kit's row order, sorted by minute. The source's own minute is a strong signal:

| Minute | Injury rate | Desk-report share |
|---|---|---|
| :00 | 8.7% | 70% |
| :30 | 10.1% | 70% |
| odd minutes (:01, :29, :31, :59) | 19% to 26% | 25% to 45% |

Desk reports are filed later and their times are estimated. Rank within the hour recovers this only roughly. The injury rate runs from 10.1% in the first 10% of an hour to 19.7% in the last row. Alone, the rank improves log loss over the class prior by about 0.002, and inside the full model by 0.001. The deeper issue is that rounding the time to the hour hid the minute without shuffling the rows. The mildest fix is to shuffle rows within each hour.

**Flaws that hurt an honest model**
None found.
- **Training only from 2019, when `trafficway_type` gained new intersection categories:** 0.49343 vs 0.49269, worse on 7 of 9 splits.
- **Last 3 years only (untuned model):** about 0.02 worse on each of the first 5 splits; I stopped the run there.
- **Dropping the time-index feature (untuned model):** +0.0029 (-0.0001 to +0.0093). That mostly sits inside that model's noise range, and it is a modelling choice, not a flaw in the task.

The injury rate does drift upward, from 0.139 in 2019 to 0.17 in 2025–26 on non-null rows, but the models handle it.

**Attacks that found nothing**
- **Number formats:**
  - Latitude decimals (5 to 10 digits) are float printing, with no label pattern.
  - The last digit of `street_no` (12% to 17% injury) and `street_no` being a multiple of 100 (19.1% vs 14.0%) are address signal the model already sees.
  - Speed values like 0, 1 and 3 have tiny counts.
- **Missing-value patterns:** for `not_right_of_way_i`, `dooring_i`, `work_zone_*`, `trafficway_type` and lat/lon, the shares are stable by year. A filled-in `dooring_i` (65% to 77% injury) is recorded at the scene, so it is signal. Missing lat/lon has 12.6% injury vs 15.3%.
- **Next-row label agreement within the hour:** 0.7444 against 0.7414 expected by chance.
- **Copies:**
  - Rows identical on all features: 881. Same hour and address: 5,576 rows (2,765 groups). Same day and address: 17,743 rows.
  - All of these fall inside one window, and the 1-month gap means none cross from training to test. Same-hour address groups agree on the label 85% of the time, against roughly 81% expected from the base rate. A count feature for them is in exploit 2, which is noise.
- **Train vs test classifier:** last 3 months of training vs the r0f0 test window, AUC 0.516.
- **Training rows:** no training row is dated at or after its test window; each split has a 1-month gap.
- **Rows the preparation changed:** compared with the source, only rows with a null target were dropped (about 0.2% per year; the 2018 count matches the source to within 3 rows).
- **Transforms over all rows:** none present (raw coordinates, codes and counts).
- **Columns after the prediction point:**
  - The source's post-outcome columns (`injuries_*`, `crash_type`, `damage`, `report_type`, `prim_contributory_cause`, `date_police_notified`) were all dropped.
  - The remaining columns are scene facts.
  - The test set mixes in desk reports, which are 56% of rows with 5% injury and do not fit the stated "police recorded scene facts" prediction point. But they are in training too, at the same share, so this is not exploitable.
- **Looking rows up in the published source** works: hour plus `street_no` plus `street_name` matched 17 of 17 rows. Not ranked.
- **Web:** I found no competition, leak thread or critique of this dataset beyond blog-level models ([Silge](https://juliasilge.com/blog/chicago-traffic-model), [Kucewicz](https://ckucewicz.github.io/traffic_crash_prediction)).

**What I could not check**
- How rows sharing the same minute were ordered in the kit; ids are dropped, so I could not tell.
- Whether recent labels get amended later (the source has an AMENDED report type). Training labels may be more final than labels in the newest test window.
- I did not tune any model beyond `better.py`.

</details>

<details><summary>Precedent check</summary>

**Precedent check: `chicago_traffic_crashes` (second-pass panel, 2026-11-04)**

**Focus question.** `focus.md` sets no specific question ("none beyond the standard panel"). The direct answer for the standard pass: every decision of 2026-11-04 follows its rule and its closest precedent. I found no departure without a reason, no exception to a Must, no drift by one curator and no third exception of the same kind. None of the register's 19 flags involves this dataset. The findings below are about stale or thin evidence, ranked.

**1. `POSTED_SPEED_LIMIT` kept (Myunghwan, 2026-10-29; still in force). Departs from a pair in the same dataset, with a stated reason. The reason is narrower than it needs to be, and its 2015 caveat no longer applies.**
- The pair inside this dataset has the same mechanism: an IDOT dictionary field required only for injury and tow reports.
  - `LANE_CNT`, `ALIGNMENT`, `ROAD_DEFECT` (elements 80, 81, 84) were dropped on the source alone.
  - The five condition fields were dropped on 2026-11-04 (Lennart; LEAK-10, under LEAK-38's clause for a measured mechanism).
  - Speed (element 50) is kept.
- The stated reason is "recent matched zero-speed rates 0.0755% without injury vs 0.0931% with injury". On the shipped frame the plain comparison goes the other way. Measured on the shipped frame (998,117 rows):
  - A zero speed is 0.548% of uninjured crashes against 0.280% of injured ones.
  - Injured crashes have the lower rate in every year from 2017 to 2026 (2024: 0.194% against 0.054%).
- Most of that gap is mix, not recording. 39% of the zeros are `PARKING LOT` crashes, and given `trafficway_type` the gap mostly closes: parking lot 3.00% against 2.80%, not divided 0.21% against 0.13%. So the fact that sets speed apart is evident from the data: a zero mostly marks a place with no posted limit, which is a scene fact. It is not a field left blank because the report was minor, unlike the five fields, whose recorded-or-not flags gave back 72% of their gain.
- **Stale caveat:** "All 66 source values of 99 occur in 2015" no longer matters, because the frame now starts on 2017-09-01. I counted 0 rows with 99. The curation comment (C7) and `focus.md` still carry it. The `lighting_condition` note (issue 6) was dropped for the same kind of reason.
- **Verdict:** consistent once the evidence is stated. Suggest replacing the "recent matched" numbers with these numbers given trafficway type, and removing the 99 sentence. No consistency prompt is needed.

**2. Five condition fields dropped (LEAK-10; Lennart, 2026-11-04). Consistent.**
- Precedent: `leak_checks.md` Mechanisms row "LEAK-10, LEAK-38 (precedent, Lennart, 2026-10-22)":
  - kick: `WheelType`, `WheelTypeID`, `PRIMEUNIT`, `AUCGUART` dropped.
  - expresso_churn_prediction: `REGION` dropped.
  - The same mechanism: whether a field is filled, given the inputs known at the prediction point, differs by outcome.
- Chicago's effect is much weaker (recorded-or-not flags win back 0.0028 of a 0.0039 log-loss gain). Expresso's flag reached AUC 0.936. LEAK-38 sets no size threshold, and LEAK-11 does not apply because these fields add signal rather than weaken it. So the drop follows the rule.
- It replaces Myunghwan's keep of 2026-10-29. That keep departed from a Must (LEAK-10) without a written exception, and a Must cannot have one. The newer curator decision wins (principles.md, "Precedence in the process"). These are two different curators, so this is not drift. Lennart's own LEAK-10 line is the same on 2026-10-22 (kick) and 2026-11-04.
- The "smallest fix" step (LEAK-7) is met: the outcome sits in whether the field is filled at all, so blanking values cannot remove it, and dropping the field is the smallest fix.

**3. One-month gap (SPLIT-10; Lennart, 2026-11-04). Consistent with SPLIT-10 as amended the same day.**
- It meets the amended rule's first condition: "a gap is set where the source or the context documents late labels". SR1050 pp. 2-3 and 9 let a report be amended after a later death, and traffic deaths are counted within 30 days.
- Precedents:
  - zillow_prize, one month (review of 2026-10-20). Zillow's gap also had a measured shortfall in its two newest months. Chicago's gap is set by the convention only, and the definition says so.
  - brazilian_ecommerce (2026-10-15) and sf_permit_time: the gap is about the label's delay.
- **Pair worth naming:** lt_vehicle_loan_default_prediction, the same curator on the same day, also has a label delay of about a month and no censoring measured at the release end, yet it got no gap. The deciding facts are on record in its own file:
  - In lt, the gap's effect was measured (+0.0018 ROC AUC at equal training size), and a 30-day gap would leave 20-53% of rows for training, against SPLIT-14's 50% floor (a Must).
  - In chicago, the gap cannot be measured (no label versions), costs about 1% of a training side, and the floor holds (`min_train_fraction=0.5`).
  - These facts separate the cases, but chicago's notes do not name the contrast. Suggest one clause in `splits_comment`.
- The change removes Myunghwan's 2026-10-29 SPLIT-10 exception, so it lowers the exception count. The register's `amendment_due SPLIT-10` flag (6 datasets) does not list chicago.
- **Numbers to reconcile (not a consistency issue):** the record's 2026-11-04 assessment gives the rise of "REPORTED, NOT EVIDENT" as 2026Q2-Q3 at z +3.3 to +3.5. This panel's period probe (the prep report) gives it from 2025Q1 at z +8 to +11. Late amendments would add FATAL rows over time, not shift mild injury against no injury, so reading it as drift holds either way. The record's figures should match the probe.

**4. Training from 2017-09-01 (SPLIT-20; Lennart, 2026-11-04). Consistent.**
- SPLIT-20 names "a change of ... the data collection" as a break, and citywide coverage starting is one.
- Precedents in the `splits.md` Cases table:
  - aeolus: flights from 2023 on (2026-10-12, Lennart).
  - perth_house_prices: "chosen from counts, not scores" (2026-10-26, Lennart).
- SPLIT-21 (Must) is met. The basis is the source's coverage note plus counts and class rates (7.3% against 15.3% with any injury; 4-7k against 9-10k crashes a month). The score comparison (0.49201 against 0.49214) is reported, not used to decide.
- Shipping unsampled is a consequence, not the reason. 998,117 rows confirmed, `crash_date` from 2017-09-01 to 2026-09-30 23:00.

**5. Ordered KABCO target (CLEAN-25; Lennart, 2026-11-04). Consistent.**
- `INJURY_SEVERITY` lists the classes lowest first (no indication < reported, not evident < nonincapacitating < incapacitating < fatal), ordered by meaning.
- Precedents with an ordered multiclass target and a fallback metric: cardiotocography, dementia_prediction, hepatitis_c_prediction (PR #37 ordinal typing, merged 2026-11-01).

**6. Crash time floored to the hour and the `Class-dependent Recording` marker (LEAK-13; Lennart, 2026-11-04). Consistent.**
- LEAK-13 says to harmonise precision after measuring what the fix removes. That was done: minutes removed for 889,076 rows, mean log loss 0.550174 to 0.550105, no quarter moved.
- Precedents: hepatitis_c_prediction (lab columns rounded) and gallstone_disease (Andrej, 2026-10-26).
- The marker on a kept dataset matches `selection.md` line 421: "on kept datasets once fixed, as on retired ones".
- Register artefact: the register tags all of Myunghwan's 2026-10-29 decisions with this marker because it reads the record's current frontmatter. That is not a finding.

**7. Metric "checked as declared" (fallback log loss). Consistent with MET-8 and MET-11.**
- The `nhtsa_crss_crash_severity` screening line chose the same: log loss for the KABCO classes.
- Wording only: the fallback reason still says "approved for investigation" (checklist), which is now stale.

**Bookkeeping**
- `chicago_traffic_crashes` is in no Cases table under `.claude/skills/`. The 2026-11-04 decisions are applications, so rows are optional. The SPLIT-10 decision is the first gap set under the amended rule's "documented late labels, not measured" condition, so a cases row would help later checks. The same goes for a LEAK-38 measured-clause row (a weak effect, still dropped).
- `HIT_AND_RUN_I` is withheld with a stated reason (behaviour after the collision). It departs from no rule, so it is not flagged.

</details>

<details><summary>Advocate</summary>

**Opening brief (proponent): ship `chicago_traffic_crashes` after small definition fixes and a rebuild**

My case is that the task is valid as defined. No validity rule fails in a way that a definition edit cannot fix. Each real problem the panel found has a fix that keeps the dataset, so exclusion does not apply.

**1. Honest evaluation holds: the inputs carry no measured outcome information (P4; LEAK-10 Must, LEAK-2, LEAK-6 Must).**
- **Outcome fields are out.** Injury counts, CRASH_TYPE, DAMAGE, REPORT_TYPE, causes, photo and statement flags, HIT_AND_RUN_I and DATE_POLICE_NOTIFIED never reach the frame (column auditor's sweep). The blind reviewer confirms this was the right call: adding `crash_type` cuts log loss from 0.46 to 0.29.
- **Fill-state test on the sparse columns.** The column auditor extended the sweep to every remaining sparse column: trafficway_type, lat/lon, the four Y/N flags and work_zone_type. Seven "is filled" flags change log loss by −0.0004, which is inside the ±0.003 split noise. What these columns add comes from their values, not from whether they were filled in.
- **The task gamer finds no flaw that hurts an honest model.**
  - The best exploit is +0.00098 log loss (point 6).
  - Composition counts give +0.00025, which is noise.
  - A classifier separating train from test reaches only AUC 0.516.
- **The 11-04 drop follows precedent.** Dropping the five condition fields applies LEAK-38's measured-mechanism clause the same way as kick and expresso_churn_prediction (precedent checker, finding 2).
- **Against the blind reviewer's "restore the conditions":** that reviewer did not know the mechanism. Recorded-or-not flags win back 72% of those fields' 0.0039 gain. The curator's newer decision and a measurement both outrank a blind preference (Precedence: who decides; EV-2).

**2. The split mirrors the application (P4; SPLIT-1..4, USE-10 Must, SPLIT-9/14 Must, SPLIT-10 Should).**
- **Temporal is the right regime.** Each prediction is a new crash at a known place: 82% of test coordinates already appear in training.
- **The windows and training sides are sound.**
  - Nine quarterly windows of 24.7k to 29.3k rows.
  - Training sides hold 74–96% of all rows, above the 50% floor.
  - 0% exact copies across the split once the hour is included.
  - The notification filter removes 16–32 rows per split (SPLIT-9).
- **The split costs no skill.** IID skill (0.162–0.171) equals temporal skill (0.165–0.169), so the temporal split does not cost a measurable amount of score.
- **The gap is now backed by a measurement.**
  - The split auditor measured it from `:updated_at`: 99.4% of rows are last updated within 30 days (median 16.1 days).
  - The update shows no label shift.
  - Each month of gap costs about 0.0001 log loss.
- **Remedy (lowest rung, a note):** replace "not measured" in `splits_comment` with these figures. Widening to 2 months for the 5 of 32 late fatal records is optional and is the curator's call. It is not required: SPLIT-10 as amended is met by the documented late labels.

**3. The use case is real and honestly labelled approximate (P3; USE-1 Must, USE-8 Must, USE-9 Should).**
- **Two reviewers agree on the actor.** The domain practitioner would use the model "as a Vision Zero / CDOT analyst: yes". The blind reviewer, without seeing our notes, named the same actor (city safety analysts).
- **The fit is stated honestly.** `fit = "approximate"` names the gaps: first_crash_type's timing, final-snapshot labels and officer judgment.
- **I concede the population mismatch for the dispatch framing.** 50.9% of rows are desk reports, and on-scene skill is 11.9% against 18.0% overall.
- **Mildest fix: change the wording, not the data.** USE-9 asks for exactly this: rewrite `use_case` to the road-safety analyst. Every row is then a crash that analyst scores, and the inputs and the quarterly refit match. This beats filtering to on-scene reports, which would remove 54% of the rows for an actor (the dispatcher) who also lacks the caller's injury report (USE-6). Fit stays approximate.

**4. Worth benchmarking, and the metric is the right fallback (P6; TP-9, MET-1, MET-2 Must, MET-8, MET-11 Must).**
- **Size and signal.** 998,117 rows, 15 inputs and a real signal. Skill is 0.165–0.175 over the class prior. first_crash_type alone has AUC 0.765, and its signal is physical: pedestrian crashes are 88% injured.
- **Every fold can be scored.** All 5 classes appear in every fold, with 18–34 fatal crashes per fold.
- **The metric has no better source.** None exists (claim auditor's search: student projects only), so multiclass log loss is the declared fallback. The same choice was made on the screening of `nhtsa_crss_crash_severity`.
- **The ranked probability score falls short.** It would need a MET-13 custom implementation and a "context" origin, which MET-11 allows only "when the context is clear". A practitioner's preference is not that.
- **Remedy (a note):** say in the metric reason that K+A carries about 10% of the loss. Replace the stale "approved for investigation".

**5. Concede: PROV-9 (Must) and the snapshot claim are wrong. Both are fixed in the definition (P5; remedy ladder, "independent failures are not conflicts").**
- **The year.** `year = "2017"` breaks PROV-9: "A source that grows over time … takes the year of the snapshot we pin."
  - Fix: `year = "2026"  # the snapshot we pin`, with bibtex `year = {2026}`.
  - This matches consumer_complaints_1m, kickstarter and sf_permit_time.
- **The download description.**
  - It names a 2026-10-29 snapshot whose bytes are gone from the warehouse.
  - Fix: name the 2026-11-04 export and its sha256 `4bf63b07…027b`, rebuild before the URL stops working on 2026-12-22, and add a CHANGELOG entry.
  - Every measured number reproduces on that export within 0.07 pp, so the science does not change.

**6. Concede two small P4 fixes, both definition edits that cost nothing (LEAK-38/LEAK-10, LEAK-13, LEAK-7 Should).**
- **Drop `dooring_i`.**
  - Within the same first_crash_type, injured crashes are 4–8 times as likely to have the field recorded.
  - LEAK-38 says: "When a conditional test measures the mechanism … LEAK-10 applies and the field is dropped."
  - Treating like cases alike with the five fields requires the drop. It costs +0.0001.
- **Keep `not_right_of_way_i` with a note under LEAK-11.** Its fill runs the other way: it is recorded more often for uninjured crashes, so it weakens the signal.
- **Keep work_zone with no action.** The within-type test found no material difference.
- **Shuffle rows within each `crash_date` hour.**
  - The source's minute order survives the hour floor, which partly undoes the LEAK-13 fix (+0.00098, positive on all 9 splits).
  - Shuffling is cheap and safe.

**7. The remaining objections are notes, not changes (P7 and writing; remedy ladder: note < definition change).**
- **The drift in "REPORTED, NOT EVIDENT."** It is real, and the temporal split already measures it.
  - Fix: one sentence in `splits_comment` dating the step to 2023Q4 (the split auditor's dating, which replaces the 2025Q1 and 2026Q2–Q3 dates in the probe and the record).
  - The possible change in recording practice is a USE-5 question for the curator, not a reason to hold the dataset.
- **The `not_right_of_way_i` name.** The curation comments already document the mapping to `private_property_i` (C "bulk header … corresponds to API alias private_property_i").
- **Stale wording.**
  - C7: the 2015 code-99 values are outside the frame now.
  - C9: cite 0.49609 vs 0.49600 for the shipped inputs.
  - Speed: replace the "recent matched" zero-speed rates with the precedent checker's numbers given trafficway type.
- **The `date_police_notified` datetime declaration.** It is cosmetic.

```text
Verdict: ship after changes.
Validity: P3 USE-1/USE-8 hold (approximate; USE-9 rewording to the safety analyst); P4 LEAK-10 holds after dropping
dooring_i (LEAK-38 measured clause), LEAK-13 holds after shuffling within the hour, SPLIT-1..4/9/14 hold, SPLIT-10 holds
(gap now measured: 99.4% within 30 days); P5 PROV-9 triggered, fixed (year 2026), provenance pinned to the 2026-11-04 export.
Value: TP holds (skill ~0.17 over prior; 18-34 fatal per fold); MET-1/8/11 fallback log_loss holds.
Quality: stale notes (C7, C9, metric reason, speed evidence) reworded.
For the curator: optional 2-month gap (SPLIT-10); recording-practice drift from 2023Q4 (USE-5); RPS vs log_loss (MET-11).
```

</details>

<details><summary>Critic</summary>

**Opposing brief: `chicago_traffic_crashes`**

**My position:** ship only after the changes below. Three rules are Musts with cheap fixes: USE-1/USE-3, LEAK-13 and PROV-9. Each is fixed in the definition, so none of them justifies excluding the dataset. The other points are notes or calls for the curator.

**1. The stated actor does not match half of the rows (P3; USE-1 Must, USE-3 Must, USE-9 Should)**
- **Problem:** `use_case` names an emergency-response analyst who assesses response needs. But 50.9% of the rows are desk reports (508,086), filed at the district with nobody dispatched. Desk reports are 5.3% injured, against 25.5% for on-scene reports.
- **Effect:** part of the headline skill comes from recognising a minor desk report.
  - All rows of 2026Q3: skill 18.0% over the prior.
  - On-scene rows only, the dispatcher's real population: 11.9%, and KSI (killed or seriously injured) AUC 0.787 against 0.842.
  - The dispatcher's main input, the caller's account of injuries, is absent (USE-6).
- **Evidence:** domain practitioner (table by report type, LightGBM by population). The task gamer independently notes that desk reports do not fit the "scene facts" prediction point.
- **Remedy (fix the definition, text only):** rewrite `use_case` to the actor every row fits under USE-9: a city road-safety analyst who estimates KABCO probabilities per crash to rank sites by expected KSI. Keep fit `approximate`, because of label quality and the road facts the report records less completely for minor crashes. Drop the dispatch framing or mark it as secondary.

**2. The label's meaning shifts across every test window (P3; USE-5 Must, SPLIT-20 Should; a question for the curator)**
- **Problem:** the share of "REPORTED, NOT EVIDENT" steps from 4.71% (2023Q3) to 5.56% (2023Q4), then rises to 6.07–6.74% in all nine test quarters (z +8.3 to +11.4). K+A falls from 2.0% to 1.4%. The on-scene share is flat at about 46%, so this is not a change in report mix.
- **Effect:** the C class carries 35% of the log loss (domain practitioner), so the score leans most on the class whose coding moves.
- **The record misdates it.** The 2026-11-04 assessment puts the rise in 2026Q2–Q3 at z +3.3 to +3.5. The prep report says from 2025Q1. The split auditor's quarterly shares put the step at 2023Q4.
- **Remedy (note):** correct the date and numbers in the record and in `splits_comment`. Name a possible change in recording practice as an open USE-5 question. This does not block shipping.

**3. The hour floor is undone by row order (P4; LEAK-13 Must)**
- **Problem:** `crash_date` is floored to the hour, but rows keep the source's minute order within each hour. This brings back the class-dependent recording that the 2026-11-04 decision removed:
  - rows at minute :00 or :30 are 8.7–10.1% injured;
  - rows at odd minutes are 19–26% injured;
  - injury rate by rank within the hour runs from 10.1% in the first tenth to 19.7% in the last row.
- **Evidence:** task gamer, regularised LightGBM. The rank feature gains +0.00098 mean, positive on all 9 splits. A random column moves the score by −0.0007 to +0.0009. The gain is small but systematic, and it defeats a fix the curator ordered under a Must.
- **Remedy (fix the definition):** shuffle rows within each floored hour with a fixed seed, before the frame is returned. The cost is zero.

**4. `dooring_i` is kept on the mechanism the five condition fields were dropped for (P4; LEAK-38 Should, LEAK-10; treat like cases alike)**
- **Problem:** within the same `first_crash_type`, injured crashes are 4–8 times as likely to have `dooring_i` recorded. A recorded "N" is 55% injured against a 16% base. The 2026-11-04 drop of the five fields followed the kick and expresso precedents, at a weak effect and with no size threshold.
- **Steelman for keeping it:** the column auditor's joint test of the "is filled" flags across the seven sparse columns finds no gain (−0.0004).
- **But:** the column's whole contribution is noise. Dropping it changes log loss by +0.00010 (claim auditor). Keeping it saves nothing and leaves an unexplained inconsistency.
- **Remedy:** drop `dooring_i`, the consistent choice at zero cost. If the curator keeps it, add a note with these numbers (LEAK-6).

**5. The gap is called "not measured", but it now has a measurement (P4; SPLIT-10 Should)**
- **What was measured:** the portal's `:updated_at` field, for crashes of June–August 2026:
  - last update median 16.1 days after the crash;
  - 99.4% of rows are last updated within 30 days;
  - 5 of 32 fatal crashes were last updated after 30 days (32.6 to 101.9 days);
  - injury shares do not shift across the update (split auditor).
- **Contrast to name:** `lt_vehicle_loan_default_prediction` (same curator, same day) got no gap. The facts that separate the two cases are SPLIT-14's floor and the measured effect there; chicago's notes should name them (precedent checker).
- **Remedy (note):** replace "not measured" in `splits_comment` and in the C2 bullet with these figures, and say that `:updated_at` covers any field, not only the label. Optional, the curator's call: a 2-month gap covers 4 of the 5 late fatal records at a cost near zero (0.0001 log loss per month of gap without the time feature).

**6. Year and snapshot are wrong (P5; PROV-9 Must)**
- **Year:** `year = "2017"` and the bibtex year 2017 break PROV-9 for a growing register. The precedents (`consumer_complaints_1m`, `sf_permit_time`) use the year of the pinned snapshot.
- **Snapshot:** `download_description` names a 2026-10-29 snapshot whose bytes and hash are no longer in the warehouse. The data a rebuild reads is the 2026-11-04 export (sha256 `4bf63b07d869d992887c08d70bc017a357f731e6bf563dd6098546417b29027b`). The README shows `build_stale: true`, and the export URL stops working on 2026-12-22 (claim auditor).
- **Remedy (fix the definition):**
  - set `year = "2026"  # the snapshot we pin` and bibtex `year = {2026}`;
  - name the 2026-11-04 export and its hash in `download_description`;
  - rebuild before 2026-12-22 and add a CHANGELOG entry for the new UUID.

**7. The metric mostly scores the drifting middle classes; several notes are stale (P6; MET-1 Must, MET-8, MET-11; writing)**
- **Metric:** K+A, the classes the analyst acts on, carry 10.5% of the loss. C and B carry 68% between them (domain practitioner).
  - Log loss is still a defensible fallback, because no source metric exists (claim auditor's web search).
  - The ranked probability score would use the KABCO order, but MET-13 requires a reference implementation, so adopting it is the curator's call.
- **Stale text:**
  - the metric reason says "task approved for investigation";
  - C7's 2015 code-99 sentence no longer applies (0 such rows remain);
  - C7's "recent matched" zero-speed rates should give way to the rates given trafficway type;
  - C9 cites the retired 21-input scores (0.49201 vs 0.49214) where the shipped 16 inputs give 0.49609 vs 0.49600.
- **Remedy (note):** state in the metric reason that K+A carry about 10% of the loss, and replace the stale wording.

**Dropped:** these points from the panel lack the evidence to carry them.
- **`not_right_of_way_i` naming (blind reviewer):** that is the bulk header's own name, and C5 documents the mapping to `private_property_i`.
- **Restoring the condition fields:** settled under LEAK-10, with 72% of their gain shown to come from whether the field was filled.
- **About 100 fatal crashes per window:** wrong; there are 18–34 per window, and all folds are scorable.

```text
Verdict: ship after changes.
Validity: USE-1/USE-3 triggered, fix the use_case text (USE-9); USE-5 question on the C-class step at 2023Q4;
LEAK-13 triggered, fix: shuffle within the hour; LEAK-38 dooring_i, drop or note; SPLIT-10 note with the measured
update delay; PROV-9 triggered, fix the year, pin the 11-04 snapshot, rebuild before 2026-12-22.
Value: MET-1 note (K+A carry about 10% of the loss).
Quality: stale C7/C9 wording and metric reason.
```

</details>

<details><summary>Advocate rebuttal</summary>

**Rebuttal (proponent): `chicago_traffic_crashes`**

The critic and I reach the same verdict: ship after changes. Neither of us proposes exclusion. Of the critic's seven points, I concede five in full and two in substance. I dispute only how strong two of the rule citations are and one phrase of overstatement. None of these disputes changes a remedy.

**1. Actor mismatch (USE-1/USE-3 Must, USE-9 Should): concede the fix, dispute that USE-1/USE-3 are triggered.**
- **Conceded:** 50.9% of rows are desk reports. On-scene skill is 11.9% against 18.0% overall. The dispatch framing does not fit these rows. Rewrite `use_case` to the road-safety analyst, keep `fit = "approximate"`, and drop the dispatch sentence.
- **Disputed:** USE-1 is not failed. It needs an actor, a moment and a decision, and the definition names all three. The actor does not match half of the rows. That is USE-9's question ("does the data as shipped mirror another well-defined use case"), and USE-9's remedy is a rewording.
- **Why the rewording stands:** use_case.md weighs "a use case rephrased only to excuse a gap" against claiming a *direct* fit. We keep the fit approximate, so that factor does not apply.
- **The 18.0% figure is not inflated for this actor.** The analyst scores every reported crash, desk reports included. The 11.9% figure belongs only to the dispatcher.
- **What follows:** the same text edit either way. Rule strength only decides whether the record lists it as "triggered, fixed" or as "Should, applied".

**2. Label meaning shifts (USE-5 Must, SPLIT-20 Should): concede the note, dispute "across every test window".**
- **Conceded:**
  - Three dates are in circulation: the record's 2026Q2–Q3 (z +3.3 to +3.5), the prep report's 2025Q1, and the split auditor's 2023Q4 step (4.71% to 5.56%).
  - They have to be reconciled to 2023Q4 in the record and in `splits_comment`.
  - A possible change in recording practice goes to the curator as a USE-5 question.
- **Disputed:**
  - The step falls before every test window. All nine windows sit at the new level, 6.07–6.74%, a spread of 0.67 pp. So the class's meaning is close to stable within the test period. The shift is between the early training history and the test.
  - A refit model faces exactly that shift, and the temporal split measures it: IID skill is 0.162–0.171 against temporal 0.165–0.169 (split auditor).
  - USE-5 is triggered only by "a label checked and found to be another quantity" (diabetes_3). Nothing has been found yet, only a step whose cause is open. So it is a question for the curator, not a failed Must. The critic agrees it does not block shipping.

**3. Hour floor undone by row order (LEAK-13 Must): concede in full.**
- The gain is +0.00098, positive on all 9 splits.
- One split's gain sits at the edge of the random-column noise (−0.0007 to +0.0009), but the sign on 9 of 9 splits makes it systematic.
- It partly undoes a fix the curator ordered under a Must. Shuffle within each floored hour with a fixed seed. The cost is zero.

**4. `dooring_i` (LEAK-38, LEAK-10): concede the drop, and correct the strength.**
- **Conceded:** drop it.
  - Injured crashes are 4–8 times as likely to have the field recorded within the same first_crash_type.
  - A recorded "N" is 55% injured against a 16% base.
  - The drop costs +0.0001.
- **Correction, which strengthens the critic's case:** this is not a Should-level weighing. LEAK-38's own text says "When a conditional test measures the mechanism … LEAK-10 applies and the field is dropped." The operative rule is LEAK-10 (Must), and the measured clause leaves no keep-with-note option. So I would remove the critic's "or note" alternative.
- **The column auditor's −0.0004 does not save it.** That test was a joint check of fill flags. It does not refute the within-type conditional test that LEAK-38 names.
- `not_right_of_way_i` stays with a LEAK-11 note, and the critic does not contest that.

**5. Gap "not measured" (SPLIT-10 Should): concede in full.**
- Replace the text with the split auditor's figures:
  - median last update 16.1 days after the crash;
  - 99.4% of rows last updated within 30 days;
  - 5 of 32 fatal crashes last updated at 33–102 days;
  - no label shift across the update.
- Add the caveats: `:updated_at` covers any field, not only the label, and history before 2026-05-21 is hidden by the bulk reload.
- I accept the critic's added clause naming the lt_vehicle_loan_default_prediction contrast (SPLIT-14 floor, measured effect). It is the precedent checker's finding, and it costs one clause.
- A 2-month gap stays optional and is the curator's call.

**6. Year and snapshot (PROV-9 Must): concede in full.**
- Set `year = "2026"  # the snapshot we pin` and bibtex `year = {2026}`.
- Name the 2026-11-04 export and its sha256 `4bf63b07…027b`.
- Rebuild before 2026-12-22 and add a CHANGELOG entry for the new UUID.
- One point from the evidence belongs here: the split auditor notes that the windows are calendar quarters only because of the 2026-10-01 cut. The rebuild should keep that cut, or `splits_comment` should say why the windows are quarters.

**7. Metric and stale notes (MET-1/8/11, writing): concede the notes, dispute one phrase.**
- **Conceded:**
  - State in the metric reason that K+A carries about 10% of the loss.
  - Replace "approved for investigation".
  - Fix the stale text: C7's code-99 sentence, the C7 zero-speed rates (give them by trafficway type), and C9's numbers (use 0.49609 vs 0.49600).
  - RPS stays the curator's call, since it needs MET-13 and a "context" origin under MET-11.
- **Disputed:** "the metric mostly scores the drifting middle classes" overstates it. Only C (35% of the loss) is shown to drift. B (33%) has no drift finding in any report. The defensible wording is "about a third of the loss is in the drifting C class".

**Dropped items:** I agree with all three (the `not_right_of_way_i` name, restoring the conditions, "about 100 fatal" per window).

```text
Verdict: ship after changes (agreed with the critic).
Validity: P3 USE-1/USE-3 hold; USE-9 rewording to the road-safety analyst, fit approximate. USE-5 open question
(C-class step dated 2023Q4, before all test windows). P4 LEAK-13 triggered, fix: shuffle within the hour.
LEAK-10 (through LEAK-38's measured clause) triggered for dooring_i, fix: drop (no note option).
SPLIT-10 holds, note with the measured update delay and the lt contrast. P5 PROV-9 triggered, fix: year 2026,
pin the 11-04 export, rebuild before 2026-12-22 keeping the 2026-10-01 cut.
Value: MET-1/8/11 log_loss fallback holds; note that K+A carry ~10% and C ~35% of the loss.
Quality: C7/C9/metric-reason wording.
For the curator: optional 2-month gap; recording-practice question (USE-5); RPS (MET-11/13).
```

</details>

<details><summary>Critic rebuttal</summary>

**Rebuttal (critic): `chicago_traffic_crashes`**

The advocate concedes my three Must fixes (USE-9 rewording, LEAK-13 shuffle, PROV-9 year and snapshot) and the `dooring_i` drop. Our briefs now differ only on how precise four points are. My verdict stays the same: ship after the changes below.

**A1. "Honest evaluation holds" (LEAK-10, LEAK-13): concede, with a correction.**
- Point 1 says "the inputs carry no measured outcome information". Point 6 then concedes two measured channels: `dooring_i` fill, 4–8 times as common on injured crashes within a crash type, and the row order within the hour, +0.00098 and positive on all 9 splits.
- So LEAK-10 and LEAK-13 hold only after the definition edits, not as shipped. The record must not carry point 1's wording.
- The order channel is not neutral. Minute :00 and :30 rows are about 70% desk reports (task gamer), so row order partly brings back REPORT_TYPE, a field dropped as outcome-linked.
- I agree that the blind reviewer's "restore the conditions" stays overruled, by LEAK-10 and the newer curator decision.

**A2. Split (SPLIT-1..4/9/14, SPLIT-10): concede, but the note must state the limits.**
- I agree the split is right and the 1-month gap holds under the amended SPLIT-10.
- "The update shows no label shift" goes further than the measurement does. The split auditor names three limits:
  - `:updated_at` changes when any field changes, not only the label;
  - history before the 2026-05-21 reload is hidden;
  - 1,904 older crashes were rewritten in one batch on 2026-11-03, with unknown label effect.
- The `splits_comment` note should give the figures and these three limits (EV-2: say what a measurement does not show).
- The 2-month gap stays the curator's call.

**A3. Use case (USE-1, USE-8, USE-9): concede the remedy. One gap remains.**
- Rewording `use_case` alone is not enough. `fit_reason` (dataset.py lines 47–49) and `known` (line 41) are written for dispatch: "timely initial-call information" and "operational dispatch performance remains unvalidated".
- After the USE-9 rewording, `fit_reason` must name the analyst's real gaps (USE-8):
  - KABCO misses about half of serious injuries in linkage studies;
  - C-class coding drift;
  - road facts dropped because the report fills them in more completely for injury crashes.
- Otherwise the fit is approximate for the wrong reasons.

**A4. Value and metric (TP-9, MET-1/2/8/11): concede.**
- I agree on MET-11 and the ranked probability score. I already left it to the curator.
- One point to add to the skill claim: "0.165–0.175 over the prior" includes recognising desk reports. On-scene rows alone give 11.9%.
- Under the analyst framing that is legitimate, because desk reports are crashes the analyst scores. The metric note should still give both figures, so a reader does not take 17% as triage skill (MET-1 note).

**A5. PROV-9 and snapshot: concede the fix, dispute "every measured number reproduces".**
- The claim auditor says the comment numbers reproduce within 0.07 pp. It also says three figures cannot be redone on the bytes now in the warehouse:
  - the C10 sub-counts (36 and 26);
  - C3's 889,076 rows;
  - C3's 0.550174 → 0.550105 diagnostic.
- At the rebuild, recompute those three on the 2026-11-04 export, or mark them as 10-29 figures (reproducibility, P5).
- The kickstarter precedent checks out: its `year = "2026"  # the snapshot we pin`.

**A6. `dooring_i`, `not_right_of_way_i`, work zone, shuffle: concede all.**
- `not_right_of_way_i` keeps a LEAK-11 note: it is recorded 4.3% vs 2.4% for uninjured vs injured crashes, which weakens the signal.

**A7. Drift and stale notes: concede, with the dating checked.**
- I recomputed the quarterly "REPORTED, NOT EVIDENT" share from the participant kit:

  | Period | Share |
  |---|---|
  | 2022Q1–2023Q3 | 4.09–4.71% |
  | 2023Q4 | 5.56% |
  | 2024Q1 | 5.66% |
  | 2024Q2–2026Q1 | 6.07–6.54% |
  | 2026Q2 | 6.64% |
  | 2026Q3 | 6.74% |

- So the step is at 2023Q4, and every test window (2024Q3–2026Q3) lies after it.
- There is a further small rise in 2026Q2–Q3. The claim auditor traces it to desk reports, 3.1% → 3.9–4.0%. That is what the record's "2026Q2–Q3" saw.
- The column auditor's "from 2025Q1" is wrong.
- The note should give both: the 2023Q4 step and the later rise in desk reports.
- I dispute "the temporal split already measures it". The split measures what the drift costs in score, not whether the C label still means the same thing. That is why it stays an open USE-5 question, which the advocate also accepts.

```text
Verdict: ship after changes (agreed with advocate).
Validity: USE-9 rewrite of use_case AND fit_reason/known (USE-8); LEAK-13 shuffle within hour; LEAK-10/38 drop dooring_i;
SPLIT-10 note with :updated_at figures and their three limits; PROV-9 year 2026, 11-04 export + sha256, rebuild before
2026-12-22, recompute or mark the C3/C10 figures from the 10-29 snapshot.
Value: MET-1 note (K+A ~10% of loss; on-scene skill 11.9% vs 18.0% overall).
Quality: C7/C9/metric-reason/speed wording; drift note: step 2023Q4 (4.71%->5.56%) plus 2026Q2-Q3 desk rise; USE-5 question.
```

</details>

## Reference

City of Chicago Data Portal, Traffic Crashes - Crashes, dataset 85ca-t3if.
