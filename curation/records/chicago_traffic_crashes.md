---
unique_name: chicago_traffic_crashes
name: Chicago Traffic Crashes - Crashes (CPD E-Crash)
checked_by:
- Myunghwan
data_foundry_status:
- WIP (Triage)
claimed_by: Myunghwan
suggestion: 'Yes'
priority: 3
tags:
- Non-IID (Temporal)
collections:
- New (BeyondArena)
original_source: GOV Website
year: '2017'
domain: social science
required_split:
- Temporal (NON-IID)
problem_type: Multiclass Classification
original_data_state: One Table
source_links:
- https://data.cityofchicago.org/Transportation/Traffic-Crashes-Crashes/85ca-t3if
- https://data.cityofchicago.org/resource/85ca-t3if.json
v2_path: datasets/_dev/tabarena-v0pt2/chicago_traffic_crashes_1m/dataset.py
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

CC (2026-10-29, Myunghwan): Issue 1: It's fine. Historical label is fine. This is a reasonable approximation. Issue 2: Yes, this is fine. We are now predicting more based on "closer to fact" information than "timely avaialbe" information. OK for this approximation. Issue 3: What decision do we need? does it matter? Issue 4: OK Issues 1/2/4 accepted; issue 3 remains discussion, not a final ship or build request.

**Exception to SPLIT-10 (2026-10-29, Myunghwan):** accept final-snapshot police injury labels as a reasonable retrospective approximation because no historical label versions or amendment times are available. Serves P3/USE-8: faithfully state the accepted approximate task rather than fabricate a maturation gap. Strict notification eligibility remains; this does not reproduce labels available at historical refits or use the training-floor rationale of alfa/lending.

**Assessment (AI, 2026-10-29):** Applied accepted historical-label and closer-to-fact framing, preserved injury/report outcome exclusions, and accepted only dataset_missing_value_label for physical DEVICE_CONDITION=MISSING. Executable cleaning, features, labels, metric and split methods are unchanged. The speed question is whether to retain the posted road limit or remove/reconstruct it; recommend retaining it without guessed 99/default conversion. Recent matched zero rates weaken the specific proposed default mechanism; incremental predictive effect of dropping speed was not measured. Its coding caveat is not a demonstrated leakage defect. Issue 3 and overall inclusion remain open; settled choices are not reopened.

**Assessment (AI, 2026-10-29):** Review answers 1/2/4 applied and rechecked: closer-to-fact scene approximation and final-snapshot labels accepted, with the bounded SPLIT-10 exception recorded. Physical-MISSING warning accepted with its exact source reason; regenerated native report has 0 errors, 0 unaccepted warnings, 1 accepted warning and 2 informational findings. Independent module-AST review confirms unchanged model inputs, labels, cleaning, metric and all split/model-determining code; prior native model and data-identity evidence reused without refitting. Current issue 3 contains the speed question and answer, recommending retention without guessed code conversions. It is not an item-3 acceptance or overall ship mark. Final inclusion/build/commit remain undecided; actual human answers and before/after application evidence retained.

CC (2026-10-29, Myunghwan): "for 3, then leave as it is. then ship". Keep the posted road speed limit exactly as implemented, with the historical-code caveat, and accept `chicago_traffic_crashes_1m` for shipping. Prior accepted final-snapshot labels, closer-to-fact scene approximation, five-condition-field retention and physical-MISSING warning remain in force. This is the final scientific inclusion verdict; build, commit and publication are separate workflow steps.

**Assessment (AI, 2026-10-29):** All numbered dataset review issues are resolved. Accepted recipe: 1,097,209 crashes, 21 predictors, five original police injury classes, log loss and nine quarterly tests. Speed values, unknowns, features, cleaning, label mapping and splits remain unchanged. Existing source, data-identity, model and panel evidence remains applicable; historical availability and recording-risk limitations stay explicit. Resolved REVIEW.md and all panel reports are archived locally before removal. Claim remains held until authorized repository integration; no build or commit is performed here.

CC (2026-10-29, Myunghwan): "now move to the build". Build the accepted Chicago dataset; the scientific ship decision and all settled treatments remain in force.

**Assessment (AI, 2026-10-29):** Built `chicago_traffic_crashes_1m` as format 2, UUID `01a18a0b-6aa8-726f-a33a-75044860edbf`, with 1,097,209 rows, 21 predictors and nine quarterly tests. Saved container reloads with its expected checksum, and a check-only reconstruction from only traced raw inputs produces the same checksum. Zero errors or unaccepted warnings; accepted physical-MISSING reason and both informational reduced-profile findings unchanged. Definition bytes, labels, predictors and splits match the accepted recipe; no new model sweep was needed. Raw inputs are backed up locally with a SHA-256 manifest. Build provenance records the current uncommitted working tree; the exact accepted source snapshot/patch is retained locally. Commit, push, publication and claim release remain unperformed.

CC (2026-10-29, Myunghwan): "add this to the current PR". Add the accepted and verified Chicago dataset to the existing PR #33, keeping its prior ten datasets and all settled scientific choices.

**Assessment (AI, 2026-10-29):** Integrating the exact accepted definition and built report into the existing eleven-dataset PR. Preserved native build UUID 01a18a0b-6aa8-726f-a33a-75044860edbf and its truthful original working-tree provenance. The saved container verifies and reproduces from the frozen input; raw data and containers remain outside Git. The source addition preserves prior datasets, checks and build metadata.

## Reference

City of Chicago Data Portal, Traffic Crashes - Crashes, dataset 85ca-t3if.
