# chicago_taxi_trip_duration

**Outcome:** added as `chicago_taxi_trip_duration_1m`. The AI recommends shipping it: the review panel's changes are made, and one call is left to you, the short end (issue 1), where the AI recommends what is implemented: dropping the 7,893 records of 61 to 119 s that log no mile and end in their pickup community area, by a rule that reads the target and trip_miles (the meter's distance, known only after the trip). Changes made, needing no decision: every trip is now placed by its community area: the City hides a census tract depending on the trip's own arrival quarter hour, so the hidden flag reads the outcome; over 5 seeds it gained 0.0028 to 0.0039 RMSLE in 15 of 15 fits (3.6 to 6.6 SDs of the paired gain). LEAK-10 keeps such a blank only when its worth is within noise, so the advocate conceded (the tracts are dropped and their centroids replaced by the area's, at a cost of 0.024 RMSLE of real location detail; keeping the tracts would need an amendment of LEAK-10, which nobody argued); the location filter reads the community area, which the City never hides, instead of the centroid, which kept trips at one tract outside the city by O'Hare only when that tract was shown, and the selection of trips with both ends in Chicago is named (8.3% of the rides and 24% of the O'Hare pickups leave); two protocol lines forbid reading other test rows (the same taxi's next pickup among them bounds a trip's end, worth 0.005 RMSLE to a method that reads it) and training on rows outside a split; the 24 trips that start in the first quarter hour after the spring clock change (2026-03-08) lose the hour their meter counted (20 kept, all in training); 1,094 trips that would need more than 120 km/h on the straight line between their area centroids (3 km of slack per end) are dropped, the rule of pkdd_15_taxi_trip_time_prediction_ii_1m; the 60 s cut, where the siblings cut at 30 s, now states why (the systems that record whole minutes write a non-ride as 0 s or 60 s, and with area centroids no rule on the inputs can remove non-rides), and a note says why the siblings' rule on ends within 100 m of the start cannot apply to centroids; the notes on late reports, the hiding mechanism and the metric are rewritten from the panel's measurements; the record's year (2026), name, source links and Metric line are fixed. The task is the arrival estimate at pickup of nyc_taxi_trip_duration_1m and pkdd_15_taxi_trip_time_prediction_ii_1m, on the City of Chicago's register of taxi trips (Taxi Trips 2024-, September 2025 to September 2026): 6,631,275 trips after cleaning (1,371,608 shipped), 9 features (the pickup time to the quarter hour, the pickup and drop-off community area with its centroid, the taxi and its company); three weekly test windows in September 2026 (118,581 to 126,382 trips), each training on a random 1M of the trips picked up at least a day earlier; `rmsle` from context.
Verdict: ship after changes (made).
Validity: SEL-1, SEL-2 hold; USE-1 holds, fit approximate (the drop-off area stands in for the destination, times to 15 minutes, places by community area, only trips with both ends in Chicago); USE-7 triggered and fixed (the filter reads the community area), and weighed with CLEAN-11 on the short end (issue 1); USE-8 triggered and fixed (the in-city selection named in `fit_reason` and `row`); LEAK-10 holds for the 8 post-trip columns (dropped), triggered by the hidden-tract flag (0.0028 to 0.0039 RMSLE over 5 seeds, a gain in 15 of 15 fits) and fixed by placing every trip by its community area; LEAK-9 triggered twice (the next pickup among the test rows, the later windows' labels in the frame) and closed by protocol lines; USE-10, LEAK-34, SPLIT-13 hold (`taxi_id` a feature); SPLIT-1, SPLIT-10, SPLIT-14, SPLIT-20, SPLIT-21 hold; LEAK-24 holds (later monthly updates added at most 94 trips to a published month); PROV-7, PROV-9 hold.
Value: TP-1 to TP-3 hold on the final definition (LightGBM 0.437 RMSLE against the dummy's 0.777, better on 3 of 3 windows, 0.237 over linear, no flag); MET-11 `context` rmsle holds (RMSLE and RMSE in seconds rank two fits in opposite order in 3 of 3 windows).
Quality: CLEAN-1 and USE-5 (24 spring-forward targets repaired, 20 kept, all in training); CLEAN-11 then CLEAN-15 (1,094 impossible straight-line speeds dropped, on the area centroids with 3 km of slack per end); the 60 s cut kept with the facts that set it apart from the siblings' 30 s; the 100 m rule cannot apply to centroids (a note and a decision table).
Weighed (priority 3): gap 0 (no thin domain, problem type or regime among the 151 accepted definitions); use case 0 (the City names no actor; the ETA framing is the siblings'); source + (the regulator's documented table); shape + (1,371,608 rows shipped, 9 features, categorical and datetime, temporal); risk 0 (the leaks found are fixed in the definition or closed by the protocol lines, and issue 1 moves 7,893 of 6.6M rows).
For the curator: issue 1 (the 61 to 119 s records with no mile within one area: drop, as implemented and recommended, extend the rule to any length, or keep them with a note; a weighing call under USE-7 and CLEAN-11). The bundle check leaves no warning to accept (two infos: 49 exact repeats and 2,564 rows that share every feature with another and differ in duration, trips of one taxi in one quarter hour between the same areas).

**Main points:** Drop the 61 to 119 s records that log no mile and end in their pickup community area (issue 1: implemented and recommended), extend the rule to any length, or keep them with a note; everything else the panel raised is fixed.

**Record judgment:** valid. The City of Chicago's own register of taxi trips (ajtu-isnz), a third city for the ETA task beside New York and Porto. The screening holds, with three corrections now made in the record: the definition uses only the 2024- table (name and source links), the year is the pinned snapshot's (2026, as chicago_traffic_crashes on the same portal), and the metric is `rmsle` from context, not the provisional fallback `rmse`. The screening's "Taxi ID is a grouping column" is superseded: the taxi is known at pickup and 99.9% of the test trips are by a taxi seen in training, so it is a feature, as in pkdd_15_taxi_trip_time_prediction_ii_1m. The open point on `chicago_rideshare_trip_duration` (one Chicago trip record or two) stays on that record.

**Issues for Lennart:**

1. **Drop the 61 to 119 s records that log no mile and end in their pickup community area, extend the rule to any length, or keep them with a note?**

   * **Problem:**
     - Records of 61 to 119 s that log no mile on the meter and end in the community area where they started look like a meter switched on and off without a ride, and no rule on the inputs can remove them here, since the places are area centroids and the siblings' rule on ends within 100 m of the start cannot apply.
     - The definition now drops them (7,893 trips, 0.12% of the kept trips) by a rule that reads two things a model never sees: the target itself (the record must last 61 to 119 s) and trip_miles, the meter's distance, known only after the trip and dropped as a feature; so whether a row stays depends on its own outcome, and the 2-minute bound is a choice.
     - The other options are the same rule at any length in the reporting systems that record seconds (32,962 trips), or keeping the records with a note, as the advocate argues; whether the rule that drops records which are no instance of the task (here, no ride) may reach through such a column is a weighing call for you[^use7].
   * **Background:**
     - "No mile" means the meter's trip_miles is 0; "the same area" means the trip ends in the community area where it started, and with area centroids a return to the start cannot be told from a short ride within the area.
     - The 60 s cut stays in any case (436,222 records of a minute or less, no rides); the systems that record whole minutes have no records between 61 and 119 s, so this rule acts on the systems that record seconds, where the no-mile share falls with the duration: 26.7% at 61 to 89 s, 13.9% at 90 to 119 s, 5.8% at 121 to 179 s, 2.9% and 1.8% up to 5 minutes, 1.0% at 5 to 10 minutes.
     - In the systems that record whole minutes, a record without a mile is no sign of a non-ride: their 120 s records with no mile within one area pay like their 120 s rides with a mile ($4.18 against $4.25, 57% paid in cash in both), which is why option B leaves those systems out.
   * **Effect on the task:** these records are no ride a dispatcher estimates, yet under RMSLE a 70-second record weighs like a large miss on a ride: in the first draft the band's records with no mile held 2.3 to 2.8% of the test squared error on 0.11 to 0.14% of the test rows, so a model gains score by fitting meters switched on and off rather than rides.
   * **Experiments:**
     - What the records of 61 to 119 s paid, trips kept by the other filters (decision table 3 of the definition):

       | Records of 61 to 119 s | Trips | Median fare | Paid in cash | Tipped |
       |---|---|---|---|---|
       | No mile, the same area (dropped in A) | 7,893 | $3.56 | 82% | 9% |
       | No mile, another area | 378 | $3.50 | 97% | 2% |
       | A mile, the same area | 27,027 | $4.00 | 54% | 23% |
       | A mile, another area | 5,859 | $4.18 | 61% | 24% |
       | For reference: 2 to 5 minutes with a mile | 420,475 | $5.42 | 32% | 35% |

     - The median fare of the dropped records is the flag drop plus about a minute and a half of waiting, and 36% of their cabs start again from the same place in the same or the next quarter hour, against 12% for the band's rides with a mile to another place (mediator, by the published centroid).
     - In the systems that record distance to 0.01 mile, 6,772 records of 61 to 119 s show 0.00 mile, against 884 at 0.01 and 571 to 787 at each step from 0.02 to 0.08: about 85% of the zeros stand out from the run of small distances (mediator).
     - Against each company's own no-mile rate on its 5 to 60 minute trips, the band's 8,370 no-mile records are 13 times the 643 expected, and 70 times (6,825 against 96) in the systems whose rate is under 5% (critic, first draft).
     - The same records go on past 2 minutes: in the systems that record seconds, 9,075 no-mile records within one area at 121 to 299 s and 7,533 at 5 to 10 minutes, 91 to 92% paid in cash and 4 to 6% tipped; option A keeps them (mediator).
     - A model trained and tested without the whole 61 to 119 s band scores 0.336 RMSLE on the rows that score 0.338 when it trains with them, so the band barely changes the fit on the other rows (domain practitioner, newest window, first draft).
   * **Consistency:**
     - Every short-end cut of the siblings was your call: pkdd_15_taxi_trip_time_prediction_ii_1m's 30 s together with the 100 m rule, chosen over the AI's 45 s[^pkdd], and sendy_logistics_challenge's pickup legs of 60 s or less, on the source's words[^sendy].
     - No precedent the panel found drops rows on the meter's miles or another column known only after the trip: protein_model_quality_rf_pcp's filter of rows that are no task was kept "on the file name, never the label"[^protein], and the precedent checker offered a rule on the meter's miles only as your option.
     - A would be the first such rule, applied inside a band of the target, and B the first at any length; C follows the siblings, whose short-end cuts read only the duration and the inputs.
   * **Panel:**
     - Drop (critic): the no-mile records far exceed each company's own rate, 93% of them end at their pickup centroid, the definition's own sign of a non-ride, and the siblings' 30 s held only because a rule on the inputs removed their non-rides, which no rule can do here.
     - Keep with a note (advocate): no mile is no clean sign (Tac - Yellow Cab Association logs no mile on 25% of its 5 to 60 minute trips), the 60 s cut already meets the rule on rows that are no task, and the one model check shows the band barely changes the fit on other rows.
     - Mediator: the records are non-rides by every measure, but the rule reads the target's band and a column known only after the trip and its bound is a choice, so it is your call; the advocate's objection is weaker than stated, since only 15% of the dropped records come from systems that log no mile on 5% or more of their longer trips, and those look even less like rides (median fare $1.00, 2.5% tipped); leans to A.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Drop 61 to 119 s, no mile, the same area (implemented) | 7,893 trips leave (0.12%) | removes most of the measured harm where non-rides are most of the no-mile records; the definition's own sign of a non-ride, measured on fare, payment and the next pickup | reads the target (61 to 119 s) and trip_miles, known only after the trip; leaves the same records at 2 to 10 minutes (about 16,600 in the systems that record seconds) |
     | B | The same rule at any length, in the systems that record seconds | 32,962 trips leave (0.5%), the 7,893 of A among them | no bound on the target; one rule over every duration | still reads trip_miles, known only after the trip; new and wide, argued by no panel member; a long record with no mile may be a meter fault on a real ride; a rebuild of the definition |
     | C | Keep them, with a note (the advocate) | no trip leaves; the note gives the band's weight | no rule on a column known only after the trip; no new rule to defend | keeps about 6,700 measured non-rides; the band's records with no mile held 2.3 to 2.8% of the test squared error |

   * **Recommendation:** A, the mediator's lean: by fare, payment, the next pickup and the meter's zeros these records are no rides, and the mildest rule that removes most of the harm beats a note; its reason is already in the definition's notes and decision table 3. C if you hold that a row filter must rest on the inputs, as your 100 m rule did. **Decision:** A, B or C?

   **Notes for the AI:**
   - A: nothing to change in `dataset.py`; add `CC (<date>, Lennart)` with the reason to the record; if Lennart wants one answer for every duration task, propose a Cases row under USE-7 in use_case.md (a rule on a column known only after the trip, inside a band of the target).
   - B: in `row_filters`, replace the last mask by `trip_miles == 0 & pickup area == drop-off area` for every duration, restricted to the companies whose share of whole-minute durations among their kept trips of 61 s to 3 h is at most 0.5 (the definition's `whole_systems` test in `_decisions`, a share of whole-minute durations above 0.5; re-count, the panel's split gave 32,962 trips); rename `SHORT_NO_MILE_SECONDS`, rewrite the curation bullet, `task_summary.changes` and decision table 3; re-run `dataset check`, the leak and task probes.
   - C: remove the last filter of `row_filters` and `SHORT_NO_MILE_SECONDS`; replace the curation bullet by a note: the 61 to 119 s band held 0.6% of the test rows and 10.0 to 10.7% of the test squared error, and its 8,370 records with no mile, in any area, 0.11 to 0.14% and 2.3 to 2.8% (first draft); turn decision table 3 into "kept, with a note"; update `task_summary.changes` and the row counts (6,639,168 after cleaning); re-run `dataset check`, the leak and task probes.

   [^use7]: **USE-7** (Must): "A row that lacks the input the prediction acts on is no task row: drop it rather than keep it as missing." Its Cases row for nyc_taxi_trip_duration_1m and pkdd_15_taxi_trip_time_prediction_ii_1m (Lennart, 2026-10-26): a recorded end within 100 m of the start is no destination anyone names; "the cut rests on the inputs, not on the travel time". **CLEAN-11** (Should): a row leaves only when it is no task row (USE-7) or a copy.
   [^pkdd]: pkdd_15_taxi_trip_time_prediction_ii_1m (Lennart, 2026-10-26, issue 2 (c)): trips under 30 s dropped together with those ending within 100 m; the 30 s cut "replaces a 1-minute cut on the recorded time, which sat on a smooth slope and also dropped short rides that moved".
   [^sendy]: sendy_logistics_challenge (Lennart, 2026-11-05, issue 4): the 740 pickup legs of 60 s or less dropped with the winners' page (the rider "forgot to mark that he took the order"); the 82 legs of 61 to 120 s stay; CLEAN-11's clause for a target the source names as not the task's quantity.
   [^protein]: protein_model_quality_rf_pcp (Lennart, 2026-11-05): the relaxed natives leave by identity under USE-7 through CLEAN-11; "the filter is on the file name, never the label".

**Review panel:** ship after changes (mediator). Tier full: claim auditor, column auditor, split auditor, domain practitioner, blind reviewer, task gamer, precedent checker, advocate and critic with one rebuttal each, mediator. The panel worked on the first draft (census tracts as the City shows them, a location filter on the centroid, 11 features, 1,374,514 rows shipped); the final definition places every trip by its community area and ships 9 features and 1,371,608 rows. The reports' counts are the first draft's: 6,672,865 trips after cleaning (now 6,631,275); test weeks of 119,351 to 127,478 (now 118,581 to 126,382); the in-city selection at 7.4% of raw trips and 22% of O'Hare pickups (now 8.3% and 24% of the records of 61 s to 3 h); 1,183 impossible speeds on the published centroids (now 1,094 on the area centroids); 8,370 short records with no mile, 7,765 at one centroid (now 7,893 within one area); 557,128 trips at one centroid (now 1,115,514 within one area); 1,199 conflicting and 24 repeated rows (now 2,564 and 49); LightGBM 0.362 to 0.367 with the tracts (0.388 to 0.393 with areas only). The phase-A reports number the first draft's issues (1 location filter, 2 hidden tract, 3 metric, 4 the 60 s cut, 5 taxi id); the mediator's issue 1 is this file's. Claim audit: 41 claims and 6 implied ones, most hold; refuted and now fixed: the hiding mechanism (it reads the trip's own arrival quarter hour, not trips "later that day or month"), the location filter's wording (it read the centroid), the spring-forward durations ("we cannot tell which field is wrong"), and the silence on the siblings' 100 m rule and daylight-saving fix; late reports untested, then measured by the split audit. Column audit: the hidden flag follows the trip's own end slot (-0.198 against +0.006 to +0.014 for the neighbouring slots); the same taxi's next pickup among the test rows (0.007 to 0.008 RMSLE); 20 spring-forward targets an hour too long; 1,183 impossible straight-line speeds; the 61 to 119 s band holds 10% of the test squared error; some taxi ids are reporting ids. Split audit: right with notes; later monthly updates added at most 94 trips to a published month, and September is no atypical season. Domain practitioner: fit approximate; keep rmsle (mae in seconds if a second metric is wanted); name the in-city selection; a 2-minute cut or a note on the short end. Blind review: include with changes; its density step at 2026-09-10 is the v2 protocol's full test windows, and its ask for hour and weekday columns departs from the siblings' precedent. Task gamer: the same taxi's next pickup among the test rows (0.0051 to 0.0056 RMSLE per window) and training on later weeks (out of protocol), both now closed by protocol lines. Precedent check: the metric, `taxi_id` and the year consistent; four departures without a written reason (location filter, 100 m rule, daylight saving, speed), now fixed; the hidden-tract keep not reasonable as an exception to a Must. Debate: agreed on placing every trip by its community area once the critic's 5-seed test put the flag's worth at 3.6 to 6.6 SDs of the paired gain, and on the area filter, the protocol lines, the daylight-saving and speed fixes and the notes; disputed: the short end (issue 1).

<details><summary>Mediator</summary>

MEDIATOR: chicago_taxi_trip_duration (folder chicago_taxi_trip_duration_1m), 2026-11-09

Panel: full tier. Phase A: claim, column and split auditors, domain practitioner, blind reviewer, task gamer, precedent
checker. Then the advocate and the critic with one rebuttal each, and this report. Read: principles.md, the rules each
side cites (USE-7, USE-8, LEAK-6, LEAK-7, LEAK-9, LEAK-10, LEAK-34, CLEAN-1, CLEAN-2, CLEAN-11, CLEAN-15), dataset.py,
the record, builder_report.md and every report. My runs (4 threads, on the claim auditor's
raw.parquet of 7,689,970 trips): m1_short_end, m2_bands, m3_speed_coarse (.py with .txt beside each).

**1. RECOMMENDATION**

Verdict: ship after changes.
Validity:
- SEL-1, SEL-2 hold.
- USE-1 holds, fit approximate: the drop-off area stands in for the destination, times are rounded to 15 min, places
  are community areas after the fix, and only trips with both ends in Chicago are in.
- USE-7 triggered, fixed: filter on the community area.
- USE-8 triggered, fixed: name the in-city selection and the coarsening.
- LEAK-10 holds for the 8 post-trip columns (dropped). It is triggered by the hidden-tract flag, which reads the trip's
  own arrival quarter hour: worth 0.0028-0.0039 RMSLE over 5 seeds, a gain in 15 of 15 fits. Fixed by coarsening every
  trip to its community area.
- LEAK-9 triggered twice: the same taxi's next pickup among the test rows, and the later windows' labels in the
  shipped frame. Both fixed by protocol lines.
- USE-10, LEAK-34, SPLIT-13 hold (taxi_id).
- SPLIT-1, SPLIT-10, SPLIT-14, SPLIT-20, SPLIT-21 hold.
- LEAK-24 holds: late reports measured, +60 to +94 trips per monthly update.
- PROV-7 holds. PROV-9 holds in the definition; the record needs fixing.
Value: TP-2, TP-3 hold after the coarsening (LightGBM 0.38-0.39 against dummies of 0.76-0.79). MET-11 `context` rmsle
  holds: RMSE and RMSLE rank two fits in opposite order on 3 of 3 windows.
Quality:
- CLEAN-1, USE-5: 20 DST targets repaired.
- CLEAN-11, then CLEAN-15: 1,094 impossible straight-line speeds dropped, measured on the area centroids.
- The 60 s cut stays, with the fact that sets it apart from the siblings' 30 s.
- The 100 m rule cannot apply to centroids; that is written down.
Weighed: nothing left open except issue 1.
For the curator: issue 1, the short end. Either drop the 61-119 s records with no mile and the same place at both
  ends, or keep them with a note. This is a weighing call under USE-7 and CLEAN-11.

**2. AGREED FACTS**

Nobody disputes these, and no measurement contradicts them.
F1  The task is real: an ETA at pickup, the task of nyc_taxi_trip_duration_1m and pkdd_15. Every evidence agent says
    ship or include.
F2  All 8 dropped columns are post-trip. Alone they score fare R^2 0.80, trip_miles 0.75 and trip_total 0.72. No kept
    feature is recorded after pickup.
F3  Hidden-tract mechanism: the City counts the drop-off tract in the trip's own end slot, which is start plus target.
    - Claim audit C7: among shown tracts, the drop-off is alone in its end slot for 1.2% of trips and in its start slot
      for 5.4%. The null on community areas shows no gap (6.68% against 6.75%).
    - Column audit A: within cells, the own end slot regresses at -0.198 (SE 0.003). The neighbouring slots give
      +0.006 to +0.014.
    - The hiding is joint, and the centroids repeat the flag. So nothing short of coarsening removes it (LEAK-7).
F4  Flag worth (critic, 5 seeds, a random 700k per train side): 0.0034 / 0.0039 / 0.0028 RMSLE.
    - That is 4-13 SDs of one score, or 3.6-6.6 SDs of the paired gain. The smallest single gain is 0.0015.
    - The builder (one seed, 0.0016-0.0024) and the gamer (0.003) agree with it.
    - Coarsening costs 0.024-0.025 of legitimate tract signal.
F5  Location filter: the code reads the centroid, but the notes say area.
    - 32,850 kept trips at tract 17031770700 (outside the city, next to O'Hare) stay only when that tract is shown.
      Meanwhile 6,334 shown suburban trips leave.
    - Filtering on the area drops 32,603 more trips, leaving 6,640,262.
    - The in-city selection is 7.4% of raw trips, 22% of O'Hare pickups and 11.2% of rides over 45 minutes.
    - The 82,914 trips with neither area come mostly from three reporting systems.
F6  The next pickup among the test rows.
    - 97.8% of the newest week's test trips have a later pickup of the same taxi in that week.
    - Its worth: 0.0051-0.0056 in protocol (gamer), 0.007-0.008 with a full week of chains (column audit), and a ceiling
      of about 0.009.
    - A deployed model never has it.
F7  taxi_id is known at pickup, and 99.88-99.98% of test trips are by a known taxi. Its worth is +0.0018 / +0.0016 /
    -0.0008, and pkdd keeps it as a feature.
F8  The random 1M per window: a newest 1M would score 0.002-0.005 better but lose the season of the year before, and
    SPLIT-21 bars choosing it from the test windows. The 6.6x density step is this design (v2 protocol), not a fault.
F9  Late reports: later monthly updates added +84, +60 and +94 trips to months already published (at most 0.016%).
F10 Metric.
    - Trips over 1 h are 3.8-4.8% of test trips and hold 38-45% of the squared error in seconds.
    - RMSE and RMSLE rank two fits in opposite order on 3 of 3 windows.
    - RMSLE, MAE, MAPE and the within-25% share all put the seconds-L2 model last. RMSE alone puts it first.
F11 DST: all 45 duration anomalies fall on 2026-03-08. 24 start at 03:00 and are one hour too long (2.8 mph as
    recorded, 17.9 mph without the hour). 20 of them are kept, all in training.
F12 1,183 kept trips need over 120 km/h between centroids, even with 1 km of slack per tract end and 3 km per area end
    (13-15 per test week).
F13 Short end.
    - The 61-119 s band holds 41,665 kept trips: 0.6% of test rows and 10.0-10.7% of the test squared error.
    - 71-86% of the band log a mile, so a plain 2-minute cut is out (conceded by both).
    - Its no-mile records (8,370) hold 2.3-2.8% of the test squared error on 0.11-0.14% of test rows. 7,765 of them also
      share the centroid at both ends.
F14 Same centroid at both ends: 557,128 kept trips (8.35%), 92% of which log a mile (median 5-7 min). Centroids cannot
    locate a return to the start.

**3. CHANGES TO MAKE NOW (no decision needed)**

C1  Coarsen every trip to its community area (LEAK-10 Must, LEAK-6 Must, LEAK-7).
    - Drop both tract columns. Set both centroids to the area's centroid, the value the City publishes in the same column
      whenever it hides the tract. This is no outside geocoding, so CLEAN-2 holds.
    - Replace the `Potential leak, kept on purpose` bullet with the reason for the coarsening: the end-slot mechanism
      (F3), the 5-seed table (F4), the cost of 0.024-0.025 and the score left (F4, TP-2).
    - Rewrite fit_reason, `known`, `changes` and decision table 5 to match.
    Why no decision: LEAK-10 lists "missingness that encodes the outcome" at Must strength, with no weak grade. Its one
    keep route, the second clause as applied to medical_facility_operational_data, needs the whole field's worth within
    noise, and F4 closes that route. A Must has no exceptions (principles, Strengths). The tension "a real task against
    a leak" says to fix the leak and keep the task. Both sides agree.
    Keeping the tracts would take an amendment of LEAK-10 for disclosure-controlled sources. That is a rule change the
    curator can always open, not an option for this dataset, and no panel member argues for it. It would also be the
    first kept outcome-reading missingness, against the curator's recent direction (2_month_survival 2026-10-26,
    bank_marketing 2026-11-08). The facts for it, if wanted: the shown tract is worth ten times the flag, and the hiding
    is the City's disclosure control.
C2  Filter on the community area at both ends, not the centroid (USE-7 Must, with its Cases row "the cut rests on the
    inputs").
    - 32,603 more trips leave. No row's presence follows the flag any more.
    - Correct the location bullet and decision 4: the filter is "no area", and the blanks have a second cause (three
      reporting systems).
C3  Name the in-city selection, with its shares (F5), in fit_reason and `row` (USE-8 Must, amended 2026-10-27;
    lt_vehicle_loan_default_prediction).
C4  LEAK-9 protocol lines in splits_comment, a note, and a benchmark-side check (LEAK-9 Should, its own remedy):
    (a) "Each test trip is predicted from the training rows and its own features only; no feature or model step may
        use other test rows, and a method that does is called out and not benchmarked." This follows
        medical_facility_operational_data, azure_vm_lifetime_resource_central_1m, fremtpl2 and bank_marketing.
    (b) "A model sees only its split's rows." This follows chile_school_dropout_mineduc_1m and
        backblaze_hard_drive_failure_1m. It covers the gamer's exploit 2 (section 6).
    (c) A `Potential leak, kept on purpose (LEAK-9)` bullet with the numbers of F6 and of exploit 2.
    (d) The check goes into BENCHMARK_CHANGES_TODO.md.
    taxi_id stays in the test rows (USE-10, LEAK-34; the critic withdrew his data-side fallback). pkdd_15 gets its own
    REVIEW.md issue for the same channel (per-dataset rule, Lennart 2026-11-08).
C5  DST repair (CLEAN-1 Should, USE-5; the nyc_taxi_trip_duration_1m precedent):
    - Subtract 3,600 s from trips that start 2026-03-08 03:00 and whose trip_seconds exceed end minus start by more than
      3,000 s.
    - Do it before the duration filters, guarded at 24 raw rows (20 kept).
    - Rewrite "we cannot tell which field is wrong" and "the daylight-saving switches do not change it".
C6  Straight-line speed filter (CLEAN-11 then CLEAN-15; pkdd's MAX_STRAIGHT_LINE_KMH, 2024_lusaka_mobility_prediction_
    hackathon). It must read the community-area centroids with 3 km of slack per end. That gives 1,094 trips, 11 / 11
    / 14 per test week, and the slack must be stated.
    On the published centroids it would be 1,164. 70 trips would leave only because their tract was shown, which is a
    selection by the flag C1 removes (m3_speed_coarse.txt). Everything in the 1,094 is also in the published version.
C7  Keep the 60 s cut and complete its reason (USE-7, CLEAN-11; the precedent departure needs the fact that sets it
    apart).
    - Whole-minute systems write non-rides as 0 s or 60 s (80,861 at 0 s and 26,044 at 60 s).
    - No rule on the inputs can remove non-rides when places are centroids.
    - The 30-59 s band sits on a smooth slope.
    - Give the 61-119 s band's weight (F13). Record these as the facts that set the case apart from nyc and pkdd's 30 s.
C8  The 100 m rule: add a note and a decision row (USE-7 Cases; sendy_logistics_challenge, "rests on exact
    coordinates"). Recount the same-place trips on the community area after C1.
C9  Notes refuted or out of date (EV-2; MET-10):
    - Replace the late-report note with F9 (the split audit's three snapshot comparisons, SPLIT-10).
    - Lead the metric reason with F10, ahead of the siblings' competitions.
    - Note that some taxi_ids are shared reporting ids (column audit F).
    - Recount the 1,199 conflicting and 24 repeated rows after C1 (LEAK-18).
C10 Record fixes:
    - year 2026 (PROV-9; chicago_traffic_crashes);
    - the name and source_links (the 2024- table only);
    - the screening's Metric line (principles, Stages: the screening was provisional).
    Also fix claims.md item 32's order and the builder report's "Features (10)" (there are 11).

**4. NEEDS THE CURATOR**

Issue 1 (P3; USE-7 Must applied through a proxy; CLEAN-11 Should): drop the 61-119 s records that log no mile and share
the place at both ends, or keep them with a note. Detail in section 5.
No other issue. pkdd_15's own LEAK-9 issue is for its own REVIEW.md, not this one.

**5. DISPUTED POINTS**

Settled by measurement: the hidden-tract keep. The advocate's brief made the keep conditional on the flag's worth sitting
within about two seed SDs. The critic ran the test and the flag failed it (F4), and the advocate conceded in full. So
this becomes C1.

Open: the short end (issue 1)
Question: is the critic's narrowed rule label-free and well founded enough to be a change with no decision?
Answer: no. The fact behind it holds, now measured, but the rule is not label-free and its 2-minute bound is a choice.
So it goes to the curator. I lean to (a) below.

Each side's best evidence:
- Critic (USE-7 Must, CLEAN-11's "unless it is no task row"):
  - 8,370 no-mile records against 643 expected from each company's own no-mile rate on 5-60 min trips, 13x.
  - In the systems whose background rate is under 5%: 6,825 against 96, 70x.
  - 93% of them end at their pickup centroid, which is the definition's own non-ride marker.
  - They hold 2.3-2.8% of the test squared error on 0.11-0.14% of test rows.
  - pkdd's 30 s cut held only because a rule on the inputs (100 m) removed its non-rides. No such rule exists here.
- Advocate (CLEAN-11 Should; USE-7 met by the 60 s cut; pkdd's move off a longer cut that "dropped short rides that
  moved"):
  - No mile is not a clean marker. TAC Yellow logs no mile on 25% of its 5-60 min trips.
  - Such systems supply about a third of the no-mile marker.
  - It is a weighing call, not a breach.
  - The one model check points the same way: trained without the band, a model scores 0.336 on the rows that score
    0.338 when it is trained with them.

My measurement (m1, m2; trips with an area at both ends):
- The zero is a separate state, not the end of a smooth run.
  - In systems that log distance to 0.01 mile, 61-119 s: 6,772 records at 0.00 mile, against 884 at 0.01 and 571-787
    at each step from 0.02 to 0.08.
  - So at most about 900 of the 6,772 fit the run of small distances. About 85% are excess, which agrees with the
    critic's 92%.
- They pay like a meter that ran without a ride (61-119 s, no mile, same centroid; 7,713 trips):
    measure                                   these     61-119 s, mile, other centroid   2-5 min with a mile
    median fare                               $3.56     $4.18                             $5.42
    paid in cash                              82%       54%                               32%
    tipped                                    9%        27%                               35%
    same cab starts again from the same       36%       12%                               17%
    centroid within this or the next 15 min
  The median fare is the flag drop plus about a minute and a half of waiting.
- The advocate's objection is weaker for this rule than stated.
  - Only 1,161 of the 7,713 (15%) come from systems with a background no-mile rate of 5% or more. The "about a third"
    belongs to the column audit's wider marker, which covered all durations.
  - Those 1,161 look even less like rides (median fare $1.00, 2.5% tipped).
  - Whole-minute systems have no records between 61 and 119 s, so in this band the rule does not split by precision.
- The rule is not label-free. It reads the target band and trip_miles, a post-trip column dropped as a feature.
  - The 2-minute bound is not where the state ends. In the seconds systems the no-mile share runs 26.7% (61-89 s),
    13.9% (90-119 s), 5.8% (121-179 s), 2.9%, 1.8%, then 1.0% (5-10 min).
  - The no-mile, same-area records keep the non-ride signature past 2 minutes, at 91-92% cash and 4-6% tipped:
    9,075 trips at 121-299 s and 7,533 at 5-10 min.
  - In whole-minute systems no mile is no marker. Their no-mile 120 s records ($4.18, 57% cash) look like their
    120 s rides with a mile ($4.25, 57%).
- After C1 the tracts are gone, so "the same centroid as published" would make a row's presence follow the hidden
  flag. The rule must read the community area: 7,893 trips instead of 7,713.

Why it is the curator's call:
- Every short-end threshold of the siblings was the curator's: pkdd's 30 s with the 100 m rule (Lennart chose it over
  the AI's 45 s, 2026-10-26), and sendy's 60 s legs (issue 4, 2026-11-05).
- No precedent drops rows on the meter's miles. The precedent checker offered one (prompt 4 (c)) only as a curator
  option. And protein_model_quality_rf_pcp's USE-7 filter was kept "on the file name, never the label".

Options:

  | | Option | Rows | Pro | Con |
  |---|---|---|---|---|
  | a | 61-119 s, no mile, the same community area at both ends | 7,893 | removes most of the measured harm where the non-ride state is the bulk of the no-mile records; the definition's own marker | reads the target and a post-trip column; leaves the same state at 2-10 min, about 16,600 seconds-system trips of less weight each |
  | b | No mile and the same community area at any length, in the systems that record seconds | 32,962 | label-free on the target; consistent over durations | new and wide, argued by nobody; a no-mile long record may be a meter fault on a real ride |
  | c | Keep, with a note giving the band's weight (the advocate) | 0 | no rule on a post-trip column; the 60 s cut as built | keeps about 6,700 measured non-rides that hold 2.3-2.8% of the test squared error |

Lean: (a). The data shows they are no task rows (USE-7, a validity rule), so the mildest fix that removes most of the
harm beats a note. Record the facts above as the rule's reason.
What would settle it: no further measurement. The open question is how far USE-7 reaches through a post-trip proxy and
a bound on the target. If the curator wants one answer for every duration task, that is a USE-7 Cases row or an
amendment.

**6. TASK GAMER'S EXPLOITS, MAPPED**

  | # | Exploit (gain) | Rule | In the definition's notes? | New or known | Action |
  |---|---|---|---|---|---|
  | 1 | Same taxi's next pickup read from the test rows (0.0051-0.0056 per split, about 7x noise; ceiling about 0.009) | LEAK-9 (evaluation leak: other test rows) | no | new | C4 (a), (c), (d); taxi_id stays (USE-10, LEAK-34) |
  | 1b | The same chain over every row of data.parquet (0.0044-0.0141; out of protocol) | LEAK-9 | no | new, covered by #1 and #2 | C4 (b) caps it at #1 |
  | 2 | Training on later windows' labelled weeks (r1 0.0055, r2 0.0145; out of protocol) | LEAK-9, protocol "a model sees only its split's rows" | no | new for this definition; a standing line elsewhere (chile_school_dropout_mineduc_1m, backblaze_hard_drive_failure_1m) | C4 (b) |
  | - | Looking trips up in the public source (untested, API down) | none of this dataset; true of every open register | no | general | none |
  | flaw | Hidden-tract flag (0.003) | LEAK-10 | yes: the `Potential leak, kept on purpose` bullet, 0.0016-0.0024, wrong mechanism | known, and its size differs (0.0028-0.0039 over 5 seeds) | C1 removes it |
  | flaw | Train thinned to 1M; density mismatch costs honest previous-trip features 0.0008 | SPLIT-20, SPLIT-21; the v2 row budget | version_comment | known, agreed | none |

**7. CONSISTENCY WITH PRECEDENT (from the precedent checker's report)**

Followed:
- C1: removes outcome-linked missingness, as chicago_traffic_crashes (same portal), 2_month_survival_rate_prediction,
  kick, expresso_churn_prediction, santander and bank_marketing did. The keep route of
  medical_facility_operational_data is closed by F4.
- C2, C3: USE-7's nyc/pkdd case and lt_vehicle_loan_default_prediction (a selection named).
- C4: medical_facility_operational_data, azure_vm_lifetime_resource_central_1m, fremtpl2, bank_marketing,
  chile_school_dropout_mineduc_1m, backblaze_hard_drive_failure_1m. pkdd goes in its own REVIEW.md (Lennart,
  2026-11-08).
- C5: nyc_taxi_trip_duration_1m.
- C6: pkdd and 2024_lusaka_mobility_prediction_hackathon.
- C8: sendy_logistics_challenge.
- C10: chicago_traffic_crashes.
- rmsle from context: sf_permit_time, brazilian_ecommerce, video_transcoding_time_prediction, and the siblings' RMSLE.
- taxi_id: pkdd.
- No hour column: CLEAN-2's nyc/pkdd case.
- The random 1M: nyc_taxi_trip_duration_1m.
Departures, each with the fact that sets this case apart:
- 60 s against the siblings' 30 s: whole-minute systems write non-rides as 0 s or 60 s, and centroids allow no input
  rule (C7).
- The 100 m rule not applied: centroids cannot place a return to the start (C8, as sendy).
- C6 on area centroids rather than exact points: the coordinates are centroids, so the slack is stated.
No precedent: issue 1, a filter on the meter's miles inside a target band. It goes to the curator.
Register flags: none bear on these calls; the precedent checker read each against its cases. No third exception of one
kind arises.

</details>

<details><summary>Claim audit</summary>

CLAIM AUDITOR: chicago_taxi_trip_duration (folder chicago_taxi_trip_duration_1m), 2026-11-09

Verdict: ship after changes. Most claims hold. Four are refuted (one P4 validity, two P3 precision or consistency,
one P3/P7 target quality). One stays untested. None of them blocks the task.

  Validity: LEAK-10 triggered, weak and now measured. The City's tract suppression reads each trip's drop-off end slot,
            which is start + target (issue 2 changes). USE-7: the location filter drops trips that have no centroid,
            which is not the same set as trips "outside Chicago" (wording). The siblings' 100 m same-place rule is not
            discussed (consistency check). PROV-7 and PROV-9 hold.
  Value:    the metric call matters. RMSLE and RMSE in seconds rank two LightGBM fits in opposite order on all 3 folds.
            The stated reason for rmsle holds on the data. MET-2 and MET-3 hold.
  Quality:  the 45 "inconsistent" durations are the spring-forward switch of 2026-03-08. 24 of them are one hour too long
            (the NYC precedent fixes them).

Scratch: the run's work files:
  raw_load.py: the 13 raw CSVs cached as raw.parquet (7,689,970 rows)
  a1_filters.py/.txt: filters, duration bands, whole-minute systems, locations, DST, companies
  a2_details.py/.txt: the 45 rows, tracts without a centroid, taxi ids
  a3_suppression.py/.txt and a4_suppression_null.py/.txt: tract-suppression mechanism and its null
  a5_completeness.py/.txt: newest test week by company, day and taxi
  a6_container.py/.txt/.json: the container built in memory, scorer on every fold, RMSLE against RMSE, same-centroid trips
  a7_misc.py/.txt: DST speeds, exact both-ends check, tracts without a centroid
  saved copies of the portal metadata of 2026-11-09 and of the community-area names

**1. TABLE: claim | source | test | result | evidence | rule**

Claim numbers follow claims.md. "def" = dataset.py. "notes" = curation_comments. "BR" = builder_report.md.

C1 Use case "for example" (the City names none) | def task_summary.use_case; notes | portal description | HOLDS |
   The metadata says only "reported to the City of Chicago in its role as a regulatory agency"; no use case, no metric. | USE-1, EV-2

C2 6,672,865 after cleaning; 1,374,514 rows shipped | def row; README | filters re-run in polars; container built |
   HOLDS | My filters give 6,672,865. The container has 1,374,514 rows. | -

C3 Target is the meter's duration in seconds, log1p | def; notes | trip_seconds against end - start | HOLDS, with a DST
   exception (C14/C28) | It matches within the 15-min rounding on all rows except 45, all on 2026-03-08. | USE-5

C4 Known at prediction time: quarter-hour start, tract or community area and centroid, taxi, company | def
   task_summary.known | feature_columns(c); mechanism of the tract suppression (C7) | PARTLY REFUTED | None of the 11
   features is post-trip. But whether a tract is shown (pickup and drop-off together) depends on the drop-off's end
   slot. See C7. | LEAK-10

C5 Split: 3 weekly windows, random 1M train at least 1 day before | def temporal, splits_comment | container splits |
   HOLDS | Test spans run 09-24..30, 09-17..23 and 09-10..16 (23:45). The train sides end on 09-22, 09-15 and 09-08
   at 23:45. Each train side has 1,000,000 rows. | SPLIT-1, SPLIT-14

C6 Changes: post-trip columns dropped; <=60 s, >3 h and "trips without a pickup or drop-off area" dropped | def
   changes | counts; what the location filter actually reads | HOLDS for the counts. The location wording is REFUTED
   in detail (C20). | See C20. | USE-7

C7 The tract is hidden for 50.7% of trips "by a rule that may look past the pickup (a weak potential leak, kept)" |
   def fit_reason; notes "Potential leak, kept on purpose"; BR issue 2 | Singleton test by key on the 3,516,759 raw
   trips with both tracts shown, against a null where nothing is suppressed (community areas, all trips) | REFUTED as
   "may". The rule reads the drop-off END slot. The 50.7% holds (0.50724, exact on the kept rows). |
   Share of shown trips that are alone in their group:
     (pickup tract, start slot)   1.5%
     (pickup tract, end slot)     4.3%
     (dropoff tract, end slot)    1.2%
     (dropoff tract, start slot)  5.4%
   Null on community areas (never suppressed): 5.81% against 5.86% at the pickup, 6.68% against 6.75% at the
   drop-off. A random 10% thinning to tract-like density gives 21.47% against 21.50% and 26.09% against 26.20%.
   So without selection, grouping by start slot or by end slot makes no difference. Among shown tracts the drop-off
   is 4.6 times less often alone by its end slot than by its start slot, and the pickup mirrors this (2.9 times).
   Pair keys do not fit: (pair, start slot) leaves 54% singletons, so it is not the "same tract pair later that day or
   month" mechanism the note guesses. The third-party reading (Schneider) says tracts are shown only when several
   trips share a tract in a 15-minute interval. That matches the data, applied per end: the pickup tract counted by
   start slot and the drop-off tract counted by end slot.
   Size: O'Hare airport pickups (tract 17031980000 on 550,342 of the 550,397 shown pickup tracts) isolate the
   drop-off side. Within (destination area, start slot):
     O'Hare -> Loop:            hidden trips' mean log deviation -0.009 (shown +0.002), SD 0.187 (shown 0.161),
                                hidden share by duration decile 0.233 ... 0.151, 0.203
     O'Hare -> Near North Side: mean -0.002 (shown 0.000), SD 0.175 (0.163), U-shaped by decile (0.244 ... 0.196 ...
                                0.223)
   Trips with an unusual arrival slot at either tail are the hidden ones. The mean moves little, so the information
   a point prediction can take is small. This fits the builder's bound: the flags add 0.0016-0.0024 RMSLE over
   community areas only. | LEAK-10 ("missingness that encodes the outcome"), LEAK-30, EV-6

C8 Source ajtu-isnz, data owner BACP | def source_url, bibtex | portal metadata 2026-11-09 | HOLDS | "Data Owner":
   "Department of Business Affairs & Consumer Protection"; attribution "City of Chicago". | PROV-8

C9 year = 2026, the pinned snapshot of a growing table; the record says 2016 | def year; record | PROV-9 text;
   metadata | HOLDS for the definition | The metadata says "Data are updated monthly" and "Time Period 2024 - current".
   PROV-9: "A source that grows over time ... takes the year of the snapshot we pin". The chicago_traffic_crashes
   precedent also uses 2026. The record's 2016 is the 2013-2023 table's year and is wrong for this definition (a
   record fix). | PROV-9

C10 Licence "See Terms of Use", no named licence | def license | metadata | HOLDS | license {"name": "See Terms of
   Use"}, licenseId SEE_TERMS_OF_USE. | EV-4

C11 13 monthly SODA files; rows equal the API's count(*) (623,661 ... 597,323; 7,689,970) | def
   download_description | line counts of the 13 CSVs; every start inside its file's month | HOLDS | All 13 counts
   are equal, total 7,689,970, and every row's start falls in its file's month. | PROV-13

C12 The bulk export is deprecated, sunset 2026-12-22 | def download_description | HTTP HEAD on 2026-11-09 | HOLDS |
   "Deprecation: @1791331200", "Sunset: Tue, 22 Dec 2026 00:00:00 GMT". | -

C13 trip_id unique; rows in no fixed order | def | n_unique | HOLDS (unique). The order was not tested. | 7,689,970 unique. | -

C14 trip_seconds disagrees with end - start on 45 rows (max 4,370 s); "we cannot tell which field is wrong" | notes
   Anomaly | list of the 45 rows | Count HOLDS, interpretation REFUTED | All 45 are on 2026-03-08, the spring-forward
   switch.
     Group A, 21 rows: start 01:15-01:45, end "03:00". The seconds are right (median 13 mph); the end time is wall-clock.
     Group B, 24 rows: start "03:00", trip_seconds 3,722-36,078. These are one hour too long: median 2.8 mph as
     recorded, 17.9 mph with an hour removed. Trips from 1 to 4 am in March run at a median 26 mph.
   38 of the 45 are in kept rows (18 A, 20 B). All are in training, none in a test window. The NYC sibling subtracts
   3,600 s for exactly this case. | USE-5, CLEAN-1, precedent nyc_taxi_trip_duration_1m

C15 Post-trip columns dropped (LEAK-10); trip_id dropped; location points not downloaded | def POST_TRIP | features
   of the container | HOLDS | The 11 features are taxi_id, the 2 tracts, the 2 community areas, company, the 4
   centroids and trip_start. No column of POST_TRIP, trip_seconds or trip_id is among them. | LEAK-10

C16 Filters in order: 1,347; 2,140; 436,222; 6,355; 571,041 | notes; decision 1 | re-run in polars | HOLDS | The same
   five numbers. | -

C17 <=60 s are no rides: no mile on 85% (0-29 s), 49% (30-59 s), 81% (60 s), against 2.3% (5-60 min) | MIN_SECONDS
   docstring; decision 2 | duration bands | HOLDS | 0.848, 0.489, 0.806, 0.023. | USE-7, CLEAN-1

C18 Over 3 h is a broken clock | MAX_SECONDS docstring | decision table 2 | HOLDS | Median speed 4.4 mph (3-6 h), 0.7
   (6-12 h), 0.35 (12-24 h). Note that 2-3 h, which is kept, already runs at 7.8 mph with 16% same centroid. 3 h is
   the siblings' cut. | CLEAN-1

C19 Whole-minute systems write a non-ride as 60 s (28,871 at 60 s, 81% no mile; spike against 59/61 s) | notes;
   claims 19 | exact-second counts by system | HOLDS with a correction | Full year: 843 at 59 s, 28,871 at 60 s, 802
   at 61 s. But the whole-minute systems (Transit Administrative Center, "Taxicab Insurance Agency  LLC", Chicago City
   Taxi Association, U Taxicab, 312 Medallion and the owner-operators) write most non-rides as 0 s: 80,861 at 0 s with
   95% no mile, against 26,044 at 60 s with 82% no mile. Their 120 s records (13,512, 32% no mile) are kept, which
   matches the seconds systems at 61-89 s (29%). The cut stands; the sentence should say "as 0 s or 60 s". | CLEAN-1

C20 Trips without a pickup or drop-off area: 571,041 (7.9%) lack the origin or destination; the City leaves the area
   blank "for locations outside Chicago"; 69% of the no-drop-off trips leave O'Hare, median 13 miles | notes; decision
   4; BR issue 1 | location table; what the filter reads | Numbers and quote HOLD. "Lack the origin or destination" is
   PARTLY REFUTED. |
   423,717 / 64,410 / 82,914; O'Hare share 0.690; median 13.34 miles.
   7.9% is the share of the rows left after the duration filters; it is 7.4% of the raw rows.
   The quote is verbatim for the community-area columns. The tract and centroid columns say "often will be blank".
   The filter reads the centroid, not the area:
     (a) 6,387 dropped trips carry a published suburban tract at the missing end (for example 17031804603 on 2,105
         and 17031806600 on 880 drop-offs). They have no centroid and no community area, but their destination is
         published.
     (b) 32,850 kept trips are outside Chicago: 31,945 drop-offs and 905 pickups, all at tract 17031770700 by O'Hare
         (centroid 41.9828, -87.8773, community area blank). That is why 0.51% of shipped rows have no drop-off area.
   So the "outside Chicago" segment is kept for one tract and dropped for the others. A trip there stays only when
   its tract is shown, which ties back to C7. The filter also removes 22% of all O'Hare pickups (61 s-3 h). |
   USE-7, USE-8

C21 The tract is hidden at both ends together (100% of cleaned rows), by a rule the City does not publish | notes |
   exact check; portal text | HOLDS | It is exact on the kept rows. Portal: "For privacy, this Census Tract is not
   shown for some trips"; "Census Tracts are suppressed in some cases". Outside the kept rows it is not joint: 23.9% of
   the dropped no-drop-off trips show their pickup tract. | -

C22 "The hidden tract is no measurable leak" (LightGBM: shipped 0.3669/0.3615/0.3658, community areas only
   0.3918/0.3876/0.3934, plus flags 0.3899/0.3860/0.3910) | claims 22; notes | read the builder's location experiment; mechanism
   test of C7 | Numbers HOLD (the file matches). "No measurable leak" is REFUTED in mechanism. The magnitude bound
   holds. | The flag is measurable (0.0016-0.0024) and C7 shows it reads the outcome's end slot. It is small, but it is
   a leak and not merely a "potential" one. | LEAK-10, EV-6

C23 Hidden trips run 0.088 longer in log1p within (area pair, quarter hour); 2,937,584 trips in mixed cells | decision
   5 | recomputed | HOLDS | +0.063 against -0.025, n = 2,937,584 exactly. Also: the hidden SD is 0.367 against 0.384
   for shown trips across all cells, and the hidden share rises by duration decile from 0.193 to 0.373. | -

C24 Community areas decoded to the City's 77 names | def COMMUNITY_AREAS | SODA igwz-8jzy (area_numbe, community)
   2026-11-09 | HOLDS | 77 against 77. The only difference is "O'Hare" against the portal's "OHARE"; everything else
   matches ignoring case. | CLEAN-12

C25 taxi_id kept (pkdd precedent); 99.88-99.98% of test trips by a known taxi; RMSLE +0.0018/+0.0016/-0.0008 without
   it; 6 trips without one; 3,077 taxis | notes; BR issue 5 | container: taxi seen per fold; probes file;
   pkdd_15_taxi_trip_time_prediction_ii_1m definition | HOLDS | Seen shares 0.9988 / 0.9992 / 0.9998. The pkdd
   precedent keeps taxi_id ("known at pickup"). The missing ones are 10 raw rows with the 2-character id "NA", read
   as null by pyarrow. A taxi is known at pickup, and the use case serves a known fleet. | USE-10, SPLIT-13

C26 company as reported, 33 values; "Taxicab Insurance Agency  LLC" 94% whole minutes against "...Llc" 1.6% | notes;
   decision 3 | recomputed | HOLDS | 0.936 against 0.0156; 33 values kept. | CLEAN-12

C27 Four owner-operators coded, 4,342 trips (5 raw values) | notes | regex on the kept rows | HOLDS | 4 values, 4,342
   trips, 5 raw values. "6574 - Babylon Express Inc." (174 raw trips) has one number, so it does not match the regex
   and stays as reported (a firm name). | CLEAN-4

C28 trip_start is local time; "the daylight-saving switches do not change" the target (not tested) | notes | DST
   nights on the data | REFUTED for 24 trips, HOLDS otherwise | 2026-03-08 has no starts in the 02:00 hour, so the
   times are local. Fall back on 2025-11-02: the 502 trips starting 00:30-02:00 have |d| <= 780 s, no anomaly. Spring
   forward: see C14; 20 kept trips carry the skipped hour. | USE-5

C29 1,199 conflicting and 24 exact repeats in the shipped frame | notes | bundle checks; cross-split copy test |
   HOLDS | No test row has an exact full-row copy in its train side (0 / 0 / 0). | LEAK-18, LEAK-19

C30 The test weeks hold 4.4% fewer trips than 2025; the newest week 4-6% fewer than the two before; no sign of late
   reports | notes Note; BR "cannot verify" | test that could refute completeness: per company, per day, distinct taxis
   per day, the last days against the same weekdays | HOLDS as far as one snapshot can tell |
   371,606 against 388,738 trips (-4.4%); 119,351 against 124,777 / 127,478.
   The newest week sits within the five Thu-Wed weeks before it (112,652 to 127,478).
   The 14 largest companies run at 0.96 to 1.05 of their mean over the five weeks before. No company falls off.
   The last three days are above the same weekdays a week earlier: 17,349 against 15,780; 18,296 against 17,420;
   20,080 against 18,872.
   Distinct taxis per weekday hold steady: 2,342-2,423 against 2,296-2,433.
   The portal's rowsUpdatedAt is still 2026-10-08 (read 2026-11-09), so no second snapshot exists yet. | LEAK-24, EV-7

C31 Metric rmsle from context; the City gives none; the sibling competitions scored RMSLE; RMSE would rank by the few
   long trips; the screening proposed the fallback rmse | def metric; README Metric; BR issue 3 | portal metadata;
   sibling definitions (Metric.source rmsle, Kaggle evaluation references); BlueTaxi paper (arXiv 1509.05257) for PKDD;
   decisive experiment on the container (LightGBM on log1p against on seconds, 300k train rows, 300 trees) scored with
   the scorer and with RMSE in seconds | HOLDS; the call is consequential |
   No metric is on the portal. Both siblings declare Metric.source("rmsle"); BlueTaxi confirms RMSLE for PKDD.
   Both metrics rank the two fits in opposite order on all 3 folds:
     RMSLE: on-log wins, 0.3727 / 0.3673 / 0.3727 against 0.4037 / 0.3980 / 0.4181
     RMSE (s): on-seconds wins, 482.4 / 457.9 / 476.8 against 500.5 / 476.0 / 478.1
   Trips over 1 h (3.8-4.8% of the test trips) hold 38-45% of the squared error in seconds.
   Precedents for "context" rmsle on a duration from a register: sf_permit_time (City of SF open data),
   brazilian_ecommerce, video_transcoding_time_prediction. food_delivery_time went to the fallback. MET-10's
   diversity factor points to rmse only if the call stays in doubt. | MET-1, MET-10, MET-11

C31-MET-2 Computable on every fold | metric spec | scorer(c) on a dummy per fold | HOLDS | Dummy (train mean of the
   log) RMSLE 0.7925 / 0.7840 / 0.7646. It equals RMSE on the log1p scale to 4 decimals (the MET-3 identity). No inputs
   or scoring columns are needed. | MET-2, MET-3

C32 Windows of 127,478 / 124,777 / 119,351 trips; train sides 6.28M-6.53M; >= 94% | splits_comment; claims 32 |
   container | HOLDS | n_test 119,351 (09-24), 124,777, 127,478. Note: claims.md writes "(127,478 / 124,777 /
   119,351), newest first", which is oldest first. The definition's text is right. | SPLIT-14

C33 One-day gap; without it 42/41/30 trips would cross | splits_comment | the builder's gap check; container train_max |
   HOLDS | Train sides end 1 day before each window. | SPLIT-10

C34 History from 2025-09-01, so every test week has its 2025 weeks in training | notes; splits_comment | container
   train_start | HOLDS | Train starts 2025-09-01 in every split. | SPLIT-20

C35 The 2013-2023 table and January 2024 to August 2025 are left out | notes | raw date range | HOLDS | Starts range
   from 2025-09-01 00:00 to 2026-09-30 23:45. | SPLIT-20

C36 Temporal, not grouped; known taxis | splits_comment; notes | taxi seen per fold | HOLDS | 99.88-99.98%. | USE-10,
   SPLIT-13

C37-C41 Probe readings (task, leak, raw, hidden groups, dtype, generated) | claims 37-41 | read the probe files;
   cross-checked by my container fits | HOLDS | My LightGBM (more rows, an hour feature) scores 0.367-0.373 RMSLE
   against the probe's 0.422. That is consistent: the probe caps rows at 200k. | TP-1..3

IMPLIED (nobody wrote them down):
I1 Every feature is known at the pickup | LEAK-10 | C7 | REFUTED, weakly | Whether a tract is shown is a function of
   the drop-off end slot, and so of the target and of other trips' end slots. | LEAK-10
I2 No row is a copy across the split | container merge test | HOLDS | 0 exact copies in all 3 splits. | LEAK-19
I3 The split is the one the use case needs (weekly refit, known fleet) | container | HOLDS | 3 windows, a gap of 1
   day, train sides of 94% or more. | SPLIT-1, SPLIT-14
I4 The target is the real-world target | C3, C14, C28 | HOLDS except the 24 DST trips | - | USE-5
I5 The siblings' cleaning precedents are followed except the 60 s cut (README: "The cuts follow
   nyc_taxi_trip_duration_1m ... and pkdd_15_...") | sibling definitions | REFUTED twice:
     (i) The 100 m same-place rule (USE-7; Lennart, CC 2026-10-26, applied in both siblings) is neither applied nor
         discussed. The record's own size check flagged it ("(3) ... trips whose drop-off centroid equals the pickup
         centroid (the NYC and pkdd 100 m rule, USE-7) need counting on the data"). In the shipped frame 8.2% of rows
         have identical centroids: 2.2% the same tract (shown) and 6.0% the same community area (hidden). Their
         median is 5.0 and 6.7 min against 15.0 for the rest, and they hold 17.6% of the log target's squared spread.
         pkdd measured 17% for its 100 m trips.
     (ii) The NYC DST fix is not followed (C14).

   | USE-7, principles "treat like cases alike"

I6 No duplicate with the siblings (PROV-7) | records, definitions | HOLDS | nyc (NYC 2016, GPS points, exact times)
   and pkdd (Porto 2013-14, GPS polylines) are other cities and other sources. chicago_rideshare_trip_duration is the
   City's TNP table: other trips, the same portal (a sibling; its "one Chicago record or two" point is a record-level
   call). Under the "same task, another source" tension none is better data (Chicago has coarser locations and times,
   no passenger count, and adds taxi and company), so all enter. | PROV-4, PROV-7

Minor wording, no effect: the builder report says "Features (10)", but the README ships 11 (the README is right).
The order in claims.md item 32 is backwards.

**2. REFUTED AND UNTESTED, RANKED (validity first, Must first)**

1. P4, LEAK-10 (Must): the tract suppression reads the drop-off's end slot (C4, C7, C22, I1).
   What it changes: issue 2 is no longer about a "potential" leak with a guessed mechanism ("same tract pair later
   that day or month", which the data rejects). It is a measured outcome-reading missingness. Whether both tracts are
   shown depends on the drop-off tract having other trips in the trip's own arrival slot, which is start + target.
   The magnitude is still bounded by the builder's experiment: the flags are worth 0.0016-0.0024 RMSLE, about 0.6%
   of LightGBM's error. Within O'Hare cells the hidden trips' mean moves only -0.011 / -0.002 log; the reading shows
   mostly in the dispersion. So it is weak.
   Rule reading: LEAK-10 lists "missingness that encodes the outcome" as out, at Must strength, with no weak grade.
   LEAK-30's weak grade covers all-row scaling, which this is not.
   Remedies, mildest first:
     (a) Keep it, but only by an explicit curator call. Change the note and fit_reason from "may look past the pickup"
         to the measured mechanism and its size. This is a departure from a Must, so it needs either the curator's
         call or an amendment (for example: a source's privacy suppression that reads the outcome, measured below a
         stated size, is kept with a note).
     (b) The rule-faithful fix: coarsen every trip to its community area (the builder's option b). It costs about
         0.024 RMSLE (6.5% of the error) of legitimate tract information.
   Option (c), dropping only the tract columns, does not remove the reading (the centroid still differs). Neither does
   dropping only the drop-off tract (the hiding is joint).

2. P3, USE-7 (Must) / consistency with the siblings: the 100 m same-place rule is not discussed (I5-i).
   What it changes: a precedent departure with no written reason (consistency check, case 2). The fact that sets the
   case apart is real: centroids of tracts or areas cannot tell a ride under 100 m from a ride within the tract
   (median 5.0 min) or the community area (median 6.7 min). These trips hold 17.6% of the target's spread.
   Mildest remedy: keep them, and write the reason into curation_comments plus a decision row (counts by shown and
   hidden, minutes, share of spread). Do not drop same-tract trips only: that selects on the shown flag of item 1.
   The curator decides whether "same community area while hidden" should go.

3. P3, USE-7 (Must), precision of the location filter (C6, C20).
   What it changes: the filter is "no centroid", not "outside Chicago" or "no destination". 6,387 dropped trips have
   a published suburban tract at the missing end. 32,850 kept trips are outside Chicago at tract 17031770700 (O'Hare
   or Rosemont), and the shipped frame has 0.51% / 0.01% missing drop-off / pickup areas because of them. Keeping a
   suburban trip requires its tract to be shown (item 1).
   Mildest remedy: correct the note and the label of decision 4 (and tell the curator in issue 1). Optional: keep the
   6,387 with the tract as a category and the centroid missing (their destination is published), or drop the 7707
   trips for one consistent "inside Chicago" rule. Issue 1's recommendation (a) still stands for the 98.9% without
   any location.

4. P3/P7, USE-5 / CLEAN-1, the spring-forward trips (C14, C28, I5-ii).
   What it changes: "we cannot tell which field is wrong" and "DST does not change the target" are both wrong for 24
   trips (20 kept, all in training). Their trip_seconds include the skipped hour (2.8 mph as recorded against 26 mph
   for March night trips; 17.9 mph with the hour removed).
   Mildest remedy: subtract 3,600 s from trips whose start shows "2026-03-08 03:00" and whose trip_seconds exceed end
   - start by more than 3,000 s, as nyc_taxi_trip_duration_1m does. Rewrite both notes. The effect on scores is nil
   (20 rows of 6.67M, none in a test window).

5. UNTESTED: late reports in the newest test week (C30; LEAK-24, EV-7).
   Why untested: the portal has not updated since 2026-10-08, so no second snapshot exists. Every test on the single
   snapshot that could have refuted completeness came out clean: by company, by day, by taxi, and the final days.
   What it changes: nothing now. Keep it as "cannot verify" for the curator, and recount the three test weeks after
   the next monthly update.

6. Weighing call, not refuted (C31, issue 3).
   The metric choice is consequential (the rankings flip on all 3 folds). The data supports the stated reason: 4% of
   trips hold 38-45% of the squared error in seconds. The record's screening line (fallback rmse) and its year 2016
   should follow the curator's call and the definition (record fixes).

Sources read: portal metadata https://data.cityofchicago.org/api/views/ajtu-isnz.json (2026-11-09); community areas
https://data.cityofchicago.org/resource/igwz-8jzy.json; HTTP headers of api/views/ajtu-isnz/rows.csv; Todd Schneider,
https://toddwschneider.com/posts/chicago-taxi-data/ (tracts shown when multiple trips share a tract and a 15-minute
interval, third-party); findingspress.org/article/34191 (the TNP pair rule "two or fewer trips within a 15-minute
window", rideshare and uncited, not used); BlueTaxi, arXiv 1509.05257 (PKDD RMSLE). The Kaggle NYC evaluation page did
not render; the sibling definition's Metric.source with that reference stands in for it.

</details>

<details><summary>Column audit</summary>

COLUMN AUDITOR REPORT: chicago_taxi_trip_duration (folder chicago_taxi_trip_duration_1m), 2026-11-09

Verdict: ship after changes.
Validity: LEAK-10 triggered (weak). The City's tract suppression reads the trip's own drop-off time slot, so the
  hidden flag (a blank tract plus the community area's centroid) is partly set by the outcome. This is measured, not
  just suspected. Worth at most 0.0016 to 0.0024 RMSLE (the builder's experiment). The rules point to coarsening to
  community areas; keeping it is the curator's call (issue A).
  LEAK-9 triggered: the same taxi's next pickup among the test week's rows limits the duration. It is worth -0.007
  RMSLE and there is no protocol line (issue B).
  USE-8 approximate holds: the recorded drop-off stands in for the named destination, as in the two sibling datasets.
Quality: CLEAN-11 broken: 20 kept targets are one hour too long at the 2026-03-08 clock change, and the notes say this
  cannot be told (issue C). CLEAN-11/USE-7: 1,183 trips are kept although they would need more than 120 km/h in a
  straight line, which the precedent drops (issue D). The leftover non-rides between 61 and 119 s and the long tail
  hold 10-13% of the test squared error (issue E, issue 4). Some taxi_ids cover more than one cab (issue F). CLEAN-14:
  the dtype probe's two flags are answered (tract GEOIDs are codes, so categorical is right).
Weighed: the tract's real signal (0.024 RMSLE) against a confirmed but small leak (<= 0.0024).

Inputs read: dataset.py, the record, builder_report.md, claims.md, the builder's probes (dtype, leak, the location experiment), the City's
column metadata (the portal's, saved by the claim auditor) and the knowledge files (principles, use_case, leak_checks,
cleaning_features). I ran the dtype probe again (same result as the builder's). Every number below comes from
scripts in the run folder: load_kept.py (the raw table through the definition's own _load_raw and
row_filters, 7,689,970 rows, 6,672,865 kept), a1_basics.py, a2_hidden.py, a3_endslot.py, a4_target.py, a5_sse.py,
a6_misc.py and a7_nextpickup.py (the shipped frame of the participant kit). LightGBM runs use one seed unless stated.

**1. COLUMN TABLE (11 inputs, the target, then the dropped source columns)**

column | meaning (City portal, ajtu-isnz) | known at pickup? | dtype and cleaning | verdict | rule

trip_start | "When the trip started, rounded to the nearest 15 minutes"; naive local Chicago time | yes. Rounding
  to the nearest quarter hour can place the start up to 7.5 minutes after the real pickup, but it carries no
  information about the duration. The 1-day gap covers it | datetime64, 37,269 values. The quarter hours repeated
  when the clocks went back on 2025-11-02 fold two hours into one (twice the usual trips per slot). No slots exist
  between 02:00 and 02:45 on 2026-03-08 | fine | USE-3, CLEAN-14, CLEAN-2

pickup_census_tract | "The Census Tract where the trip began. For privacy, ... not shown for some trips" | the tract
  is known at pickup. Whether it is SHOWN is not: the City hides both ends together, and the hiding depends on the
  trip's drop-off time slot (issue A) | category, 312 levels in the shipped frame, 11-digit GEOID read as text.
  50.64% missing (hidden). The dtype probe's `numeric_levels` flag is answered: these are codes, so a category
  (CLEAN-14, last bullet; the zillow_prize census_tract precedent). Their digits repeat the community area, which
  ships as its own column | leak in its missingness (weak) | LEAK-10, LEAK-38 (last clause), LEAK-6

dropoff_census_tract | "The Census Tract where the trip ended", hidden as above | recorded when the meter stops. It
  stands in for the named destination, as in nyc and pkdd (USE-8 approximate, named in fit_reason). Its shown or
  hidden status depends on the end slot (issue A) | category, 415 levels, GEOID text, 50.64% missing; the same answer
  to the dtype flag | stand-in fine; leak in its missingness (weak) | USE-8, LEAK-10

pickup_community_area | "The Community Area where the trip began. ... blank for locations outside Chicago" | yes |
  category of the City's 77 names (CLEAN-12 decode). I checked the mapping on the data: CA 76 has its centroid at
  41.980,-87.914 (O'Hare), 32 at 41.879,-87.625 (Loop), 56 at the Midway side, 77 Edgewater, 1 Rogers Park, 55
  Hegewisch. Missing 0.01% (905 trips): all in tract 17031770700, outside the city next to O'Hare (41.983,-87.877).
  There a blank means "outside Chicago", and the tract carries that (lossless) | fine; a documentation gap (issue G)

  | CLEAN-12, CLEAN-10

dropoff_community_area | "The Community Area where the trip ended" | stand-in for the destination | category, 77
  names; 0.51% missing (31,945 trips, all to tract 17031770700) | fine; documentation gap (issue G) | USE-8,
  CLEAN-10

pickup_centroid_latitude, pickup_centroid_longitude | "center of the pickup census tract or the community area if the
  census tract has been hidden" | yes for the location. The shift to the community area's centroid when the tract is
  hidden repeats the hidden flag (issue A) | float64. One value per tract and one per community area (checked: at
  most 1 distinct centroid per key). A coordinate, so numeric. Not an exact copy of another column (CLEAN-5) | fine;
  carries the flag of issue A | CLEAN-14, LEAK-10

dropoff_centroid_latitude, dropoff_centroid_longitude | as above, for the drop-off | stand-in for the destination |
  float64, as above | fine; carries the flag of issue A | USE-8, LEAK-10

company | "The taxi company" | yes (the cab's affiliation) | category, 33 values. The four "<n> - <n> <owner's name>"
  owner-operators are coded (CLEAN-4, stable code). "6574 - Babylon Express Inc." and "312 Medallion Management
  Corp" are firms and are left alone, which is right. The two spellings of Taxicab Insurance Agency stay apart
  because they are two reporting systems (94% against 1.6% whole minutes). That a company encodes the target's
  precision is a property of the reporting system, known at pickup. No class, so no LEAK-13 | fine | CLEAN-4,
  USE-6

taxi_id | "A unique identifier for the taxi", "consistent for any given taxi medallion number" | yes. It is also the
  key for an evaluation-level leak through the test week's other rows (issue B) | category, 3,062 levels shipped
  (3,078 kept). The City's 128-character hash is cut to a stable 12-character code (CLEAN-4). High cardinality, but
  it is an entity id that a model uses as a category (the pkdd precedent). 6 missing. Some ids are not one cab
  (issue F) | fine as a feature; LEAK-9 protocol line missing; quality note | LEAK-34, LEAK-9, CLEAN-14

log1p_trip_seconds (target) | "Time of the trip in seconds", log1p | n/a (the outcome) | float64, 61 s to 3 h. RMSLE
  is computed after the log1p inverse (CLEAN-16). Twenty kept values are one hour too long (issue C). Residual
  non-rides at the short end and broken clocks at the long end (issue E) | cleaning problems | CLEAN-11, CLEAN-15,
  USE-7

Dropped source columns (all checked against the portal's 23 columns, so none is missing from the review):
  trip_end_timestamp: start plus the target, so it is post-trip. Dropped (LEAK-10), right.
  trip_miles: "Distance of the trip", the meter's distance (alone R^2 0.75). Post-trip. Dropped, right.
  fare, tips, tolls, extras, trip_total: charges of the finished trip (R^2 0.80, 0.36, -, 0.29, 0.72). Post-trip.
    Dropped, right. Some extras (an airport surcharge) follow from the pickup, which stays an input.
  payment_type: chosen when the trip is paid (R^2 0.06). It may be known at booking for app or account rides, but the
    drop is the conservative call. Right.
  trip_id: a unique identifier with no meaning. Dropped (CLEAN-3), right.
  pickup_centroid_location, dropoff_centroid_location: points that repeat the coordinates. Not downloaded (CLEAN-5),
    right.
  All the dropped fields are post-pickup or identifiers. No column that a pickup-time model could use was dropped
  (CLEAN-22).

**2. PROBLEMS, RANKED (P4 before P7; within a rank, Must before Should, then by effect)**

A. [P4, LEAK-10 Must, weak; refines the builder's issue 2] The City hides the tracts depending on the trip's own
   drop-off time slot. The hidden flag is missingness that partly encodes the outcome.

   The builder kept the hidden flag as a "LEAK-30-like" source step that "may look past the pickup (other trips of the
   same tract pair later that day or month)". The data shows a more direct mechanism. Third-party accounts of the
   taxi release say tracts are "only included when there are multiple trips within the same tract ... over the same
   15-minute interval" (Todd Schneider, toddwschneider.com/posts/chicago-taxi-data). For the City's rideshare table,
   academic work reports that tracts of a tract pair with two or fewer trips in a 15-minute window are suppressed at
   both ends. At the drop-off end the 15-minute interval is the END slot, which equals start + trip_seconds.

   Test (a3_endslot.py). I took 2,733,684 kept trips in 296,104 cells (pickup CA, drop-off CA, start slot) that hold
   both hidden and shown trips and more than one end slot. Within each cell, I regressed the hidden indicator on:
     - the number of trips from OTHER cells (cell-mates excluded) that end in the trip's drop-off CA in its own end
       slot (log1p);
     - the same counts 15 and 30 minutes earlier and later (placebos);
     - the count at the end slot in the PICKUP CA (placebo);
     - controls: the within-cell deviation of log seconds and of log meter miles, their absolute values and squares.
   Results (SE over 10 random folds of cells):
     own end slot             -0.198 (SE 0.003)
     slots -30/-15/+15/+30 min +0.014 / +0.006 / +0.006 / +0.008 (SE 0.003)
     pickup-CA placebo        +0.012 to +0.015
   The trip's exact drop-off slot decides, and its neighbours do not. Hidden share by fifth of the end slot's
   relative busyness: 33.8% in the quietest fifth, 24.8-27.2% in the other four. So whether a trip's tracts are shown
   depends on when it ended, that is on trip_seconds. This is LEAK-10 ("missingness that encodes the outcome"), not
   LEAK-30 (a transform over all rows). LEAK-38's last clause applies: a conditional test, given the covariates known
   at the prediction point, shows the missingness differs by outcome. The kick WheelType and expresso REGION
   precedents were dropped under LEAK-10.

   What the builder's reading still gets right (a2_hidden.py). In the mixed cells, hidden trips run +0.063 in log1p
   seconds and +0.066 in log1p miles against shown trips at -0.025 and -0.027. The mean gap of 0.088 is distance, so
   hidden pairs are farther apart (rarer tract pairs), and hidden trips are faster (median 11.3 against 9.0 mph). The
   end-slot channel comes on top of that geography and is a minority of the flag.

   Strength. The builder's experiment bounds the whole flag's worth at 0.0016 / 0.0024 / 0.0019 RMSLE (community
   areas plus the hidden flags against community areas only, 3 windows, one seed). The outcome-driven part is smaller
   still. Weak, but measured.

   Side effect on the rows. The "no pickup or drop-off centroid" filter keeps drop-offs outside the city (tract
   17031770700, 31,945 trips; 905 pickups) only when their tract is shown. Hidden ones have no centroid and leave, so
   this filter also selects on the flag.

   Remedies (the curator's call):
   (b) Coarsen every trip to its community area: drop both tracts and replace the centroids by the community area's,
       as the builder's option (b). This is the only fix that removes the flag (LEAK-7: nothing smaller removes it,
       because the hiding is joint, so a shown pickup tract reveals the drop-off's status). It costs the shown tract's
       real signal, 0.024-0.025 RMSLE (0.3669 to 0.3918, etc.). The rows of tract 17031770700 then have no community
       area, so they leave with the other trips outside Chicago, which also removes the side effect. This is where
       LEAK-10, LEAK-6 ("a confirmed leak goes even when small") and the kick/expresso precedent point.
   (a) Keep, with the note rewritten: name the end-slot mechanism and the numbers above, under LEAK-10 (not LEAK-30),
       with fit_reason saying "kept". The closest support is LEAK-10's third clause: the source's rule lets the outcome
       draw a minority of the flags, and the tract keeps its worth on the rows the outcome did not draw. That clause
       was written for spans and is a curator's judgment ("the size of the worth alone never decides"), so keeping
       needs the curator's explicit call. Without it, it is a departure from a Must.
   Either way, the current text is wrong on the mechanism. These passages need correcting:
     - curation_comments "Potential leak" bullet;
     - fit_reason "a rule that may look past the pickup";
     - the decision table 5 title and caption ("fits rarer tract pairs being hidden");
     - builder issue 2's "LEAK-30-like".

B. [P4, LEAK-9 Should] Evaluation-level leak: the same taxi's next pickup in the test week limits the duration. There
   is no protocol line.
   Every test window keeps all of its trips, and taxi_id and trip_start are inputs. A method that reads the other
   test rows learns that a trip ended before the same cab's next pickup: duration <= next start - start + 900 s.
   That value does not exist at pickup.
   - 97.8% of the newest week's test trips have a next pickup of the same taxi in the week, 62.2% of them within 60
     minutes.
   - Spearman 0.50 with the duration where the gap is at most 2 h.
   - Measured (a7_nextpickup.py: LightGBM on the complete week 2026-09-10..16, tested on 2026-09-24..30, gaps
     computed within each week from features only): RMSLE 0.3677 / 0.3697 without the gaps, 0.3609 / 0.3616 with
     them (two seeds), a gain of about 0.007-0.008 in one week of training. Three times the hidden-flag's worth.
   Mildest remedy, as medical_facility_operational_data and azure_vm_lifetime_resource_central_1m do:
   - a protocol line in splits_comment: "Each test trip is predicted from the training rows and its own features
     only; no feature or model step may use other test rows";
   - a curation_comments bullet "Potential leak, kept on purpose (LEAK-9, an evaluation leak)" with these numbers;
   - the benchmark-side check (BENCHMARK_CHANGES_TODO.md).
   Consistency: pkdd_15_taxi_trip_time_prediction_ii_1m keeps taxi_id with exact start timestamps, so its version of
   this channel is sharper, and I found no protocol line there. That is a per-dataset choice, so it goes into pkdd's
   REVIEW.md as its own issue, not across datasets. nyc has no cab id.

C. [P7, CLEAN-11 Should] 20 kept targets are one hour too long at the spring clock change. The notes say this cannot
   be told.
   The 45 "anomalies" (|trip_seconds - (end - start)| > 900 s) all start on 2026-03-08 between 01:15 and 03:00
   (a1_basics.py). They fall into two groups:
   - 21 start at 01:15-01:45 and "end" at 03:00. Their trip_seconds are right (365 s for 1.08 mi, 720 s for 2.3 mi).
     Only end - start includes the skipped hour.
   - 24 start at 03:00. Their trip_seconds are 3,722-5,490 s against end - start of 0-1,800 s and 1-18 meter miles
     (3.28 mi in "4,224 s" is 2.8 mph at 3 a.m.; minus 3,600 s it is 19 mph). The meter counted the skipped hour,
     so the target is 3,600 s too long. 20 of these 24 are kept.
   The fall-back day (2025-11-02) has no such record.
   So two statements are refuted for the spring switch: "We keep them, as we cannot tell which field is wrong" and
   "the daylight-saving switches do not change it" (EV-2: a measurement outranks the reading of the column).
   Remedy:
   - set those 20 targets missing (start 2026-03-08 03:00 and trip_seconds > end - start + 900), so the rows leave
     (CLEAN-15), guarded at 20;
   - rewrite both bullets.
   The effect on scores is nil (March, training side only, about 3 rows in the shipped frame), but the notes are
   wrong.

D. [P7, CLEAN-11 Should, with a precedent] Trips kept although their straight-line speed between centroids is
   impossible.
   1,183 kept trips need more than 120 km/h in a straight line between the pickup and drop-off centroids, even after
   allowing 1 km of slack per tract end and 3 km per community-area end (a4_target.py).
   - Median 169 s and 0.45 meter miles, mostly with an O'Hare end. Example: 137 s, 1.67 mi, Near South Side to O'Hare
     27 km away.
   - The meter's time and miles agree on a short ride, so the endpoint or the duration is wrong.
   - 13-15 per test week, 0.4-0.7% of the test squared error (a5_sse.py).
   Precedent: 2024_lusaka_mobility_prediction_hackathon dropped 19 trips over 120 km/h in a straight line as
   impossible ("a wrong duration or endpoint"), as pkdd's MAX_STRAIGHT_LINE_KMH does. The siblings' rule is not
   applied here, and the notes do not say why.
   Remedy: add this filter to row_filters with the slack stated, or write in curation_comments why it is not applied.
   (Separately, 387 kept trips run over 80 mph on the meter, median 17.6 mi in 420 s. Duration or miles is wrong;
   miles is no input, so I would only note them.)

E. [P7 / P3, USE-7 and CLEAN-11; the builder's issue 4] The target's tails inside the kept range. Most of the excess
   error sits at the short end, not the long end.
   Squared-error shares from LightGBM on the shipped features, 400k training rows, three windows (a5_sse.py):
   - 61-119 s: 41,665 kept trips. No mile on the meter in 27% (61-89 s) and 14% (90-119 s); the same centroid at
     both ends in 76% and 66%. 0.59-0.63% of test rows, 10.0-10.7% of the test squared error. RMSLE 0.367 becomes
     0.348 without them.
   - 61-119 s with no mile: 0.11-0.14% of rows, 2.3-2.8% of the squared error.
   - The siblings' USE-7 rule (an end within 100 m of the start is no named destination) cannot be applied with
     tract or community-area points, and the definition does not say so. The nearest marker, the same centroid with
     under 0.1 meter mile, covers 57,094 kept trips (0.86%) and 7.9-8.2% of the squared error. It is not a clean
     non-ride marker: 21% come from Transit Administrative Center and 10.5% from Tac - Yellow Cab Association, whose
     systems often record no miles (25% no-mile on trips of 5-60 min for TAC Yellow), and its 90th percentile is
     1,339 s.
   - 2-3 h: 5,915 kept trips. 16-21% under 2 mph and 18-28% with the same centroid at both ends; 1.9% are overlapped
     by the same taxi's next pickup (a meter left running). 0.07% of test rows, 1.2-1.7% of the squared error; under
     2 mph 0.3-0.6%. The 3 h cut is right and the long tail does little harm.
   Recommendation:
   - keep the 60 s cut (issue 4 (a));
   - add to curation_comments the size of the leftover non-rides, and why the siblings' 100 m rule does not apply
     (coarse points);
   - give the curator the option to drop records of under 2 minutes with no mile on the meter (about 0.1% of rows,
     2.5% of the squared error), which is a USE-7 non-ride rule on a column used only for cleaning, as the 60 s cut
     uses the target.

F. [P7, a note] Some taxi_ids are not one cab.
   - 47,017 kept trips (0.70%) are overlapped by the same taxi's next pickup by more than the rounding allows
     (a4_target.py, a6_misc.py).
   - 27 ids have more than 5% of their trips overlapped (47,455 trips; 879 in the newest test week); one has 42%.
   - One id records 27 O'Hare pickups, all cash, in one quarter hour. Another reports under four companies and has
     14 trips in one slot.
   - Overlap is concentrated in the TAC dispatch companies (5.2-7.4% of their trips) and Transit Administrative
     Center (1.8%), the whole-minute reporting systems.
   For those systems taxi_id is a reporting id, sometimes shared, rather than a cab (or their durations run long).
   Remedy: one line in curation_comments. The feature stays (known at pickup, LEAK-34).

G. [P7, documentation] Trips outside the city are partly kept.
   The definition says that trips without a pickup or drop-off area (outside Chicago) leave. In fact 32,850 kept
   trips have a blank community area at one end (tract 17031770700, next to O'Hare, outside the city), kept because
   that tract has a centroid. Say so in the location bullet. Under issue A (b) they leave.

**3. ANSWERS TO THE MAIN SESSION'S SPECIFIC QUESTIONS**

- Drop-off area: recorded when the meter stops (the portal: "where the trip ended"), not a stated destination. Taking
  it as the destination named at pickup is the nyc/pkdd stand-in, named in fit_reason (USE-8 approximate). No new
  action, except that its tract's visibility depends on the drop-off time (issue A).
- 15-minute rounding: harmless for trip_start (no target information). The end timestamp is dropped. The rounding
  of the END is what drives the leak: the City counts trips per tract and 15-minute interval, and at the drop-off
  that interval is the end slot (issue A).
- Centroid shift on hidden tracts: the centroid moves to the community area's (one value per area, checked), so the
  four centroid columns repeat the hidden flag. Any remedy for issue A has to cover them too.
- LEAK-30 for the suppression flag: LEAK-30 covers transforms over all rows (scaling, ranks, PCA). The suppression
  counts other trips, which is a transductive element, but the measured channel is the trip's own end slot, so the
  rule is LEAK-10 (issue A).
- Areas and tracts as codes: tracts are categorical GEOID codes, which is right, and the dtype probe's two flags are
  answered. Community areas are decoded to the 77 names (CLEAN-12), and the mapping checks out on the centroids.
  CLEAN-10: the blank community area means "outside Chicago" per the City. For the 32,850 kept trips the tract
  carries it; for the dropped ones see the builder's issue 1. Even so, 82,914 trips blank at both ends (a median of
  4.7 miles in the builder's one-month look) suggest some blanks are unrecorded rather than outside Chicago, which
  supports the drop (issue 1 (a)).
- taxi_id: 3,062 shipped levels, a stable code, categorical, which is right. 99.9% of test trips are by a known taxi
  (LEAK-34 legitimate history). See issues B and F.
- Dropped fields: all post-pickup or identifiers (section 1).
- Target: log1p of the meter's seconds; RMSLE on the inverse. Beyond the 60 s and 3 h cuts:
  - the short end holds most of the excess error (issue E);
  - the long tail is small (issue E);
  - 20 DST values are wrong by an hour (issue C);
  - 1,183 trips have impossible straight-line speeds (issue D).

</details>

<details><summary>Split audit</summary>

Split audit: chicago_taxi_trip_duration (folder chicago_taxi_trip_duration_1m), 2026-11-09

VERDICT: right with notes. Temporal by pickup time, three weekly windows, a one-day gap and a year of history fit the
use case (an ETA at pickup from the company's dispatch, refit weekly; SPLIT-1, SPLIT-6, SPLIT-12). No problem needs a
re-split, a gap or a filter. The builder's one open point (late reports in the newest test week, LEAK-24 / SPLIT-10)
is now measured and settled: the City's later monthly updates do not add trips to months already published, so the
newest week is as complete as a later read would make it. Every note below changes documentation only.

Judgment record
  Validity: SPLIT-1, SPLIT-2, SPLIT-3 hold (temporal; known taxis, USE-10); SPLIT-9 holds (no shortcut: 0 training
  trips end after a window start); SPLIT-10 holds (1-day gap, label delay at most 3 h; newest period complete as a
  later read, measured); SPLIT-11, SPLIT-14, SPLIT-15 hold (3 windows, each its own expanding train side on 94.2% /
  96.0% / 97.9% of the cleaned rows); SPLIT-13 holds (taxis recur; the use case predicts for the known fleet);
  SPLIT-20 holds (one year, no break, the 2025 weeks of the test season in training; September is not atypical);
  LEAK-24 not triggered (measured below).
  Weighed: the random 1M train side against the newest 1M (costs 0.002-0.005 RMSLE, keeps the year: kept).

How it was checked
  Frame and splits rebuilt from the definition (ds.process(), ds.make_splits(); 6,672,865 cleaned rows, plan frame
  1,374,514 rows, identical to the builder's). Scripts and logs in the run folder (build_frames.py,
  split_facts.py/.log, history_breaks.py/.log, alt_windows.py/.log/.json, api_counts.sh/.log). Thread caps 4. The
  City's API was read live (count(*) queries) and the Wayback Machine's copies of the portal's column statistics
  (web.archive.org .../api/views/ajtu-isnz/columns.json at 20241217045311, 20260420173458, 20260930151531).

FINDINGS, in rank order (all P4; none is a violation)

1. Late reports in the newest test week: measured, none (LEAK-24 Must, SPLIT-10 Should; P4). Settles the builder's
   "What could not be checked" item and the "Target: concern" checklist row.
   Evidence. The table is updated monthly ("Data are updated monthly"; rowsUpdatedAt 2026-10-08 21:19 UTC, latest
   trip start 2026-10-01 00:00, unchanged on 2026-11-09), so September 2026 was first published 8 days after its last
   trip. Whether a later update adds trips to a published month was measured by comparing archived column statistics
   (the count of trips at a moment, with the newest start time then present) with today's counts of the same span:
     - snapshot 2024-12-17: 5,976,344 trips with start <= 2024-12-01 00:00; live today: 5,976,428 (+84 after 23
       monthly updates, 0.0014%);
     - snapshot 2026-04-20: 14,802,849 with start <= 2026-04-01 00:00; today 14,802,909 (+60, from the cached
       total 18,658,792 minus the live monthly counts of Apr-Sep 2026, plus 109 trips at 04-01 00:00 and minus 37 at
       10-01 00:00, both counted live);
     - snapshot 2026-09-30 (after the update that published August): 18,061,493 with start <= 2026-09-01 00:00;
       today 18,061,587 live (+94; the same method gives the same number: cached total minus the live September
       count 597,323, minus 37 at 10-01 00:00, plus 155 at 09-01 00:00). So the update after August's first
       publication added at most 94 trips (0.016% of August's 598,559, a live count equal to the builder's).
   In the data: the newest week's company shares lie within 0.008 of the five weeks before (Flash Cab 0.204-0.212,
   Taxicab Insurance Agency Llc 0.137-0.145, ...), so no reporting system is missing at the end; the duration's mean,
   p50 and p90 do not fall (probe 13, |z| <= 1.3). The newest week's lower count is real or permanent, not late:
   cleaned trips against the same weekdays 364 days earlier are 1.028, 0.963 and 0.881 (oldest to newest window),
   and the newest week (119,351) sits inside the August weeks' range (116,120 to 119,449).
   Remedy: none in the split. Replace the note "late reports cannot be ruled out ... a second download after the
   City's next monthly update would settle it" (curation_comments, last bullet; builder report P3/P4 Target row) with
   this measurement (the three snapshot comparisons), citing SPLIT-10's "the newest period is as complete as a later
   read of it".

2. The gap: one day is right for the stated actor (SPLIT-10, SPLIT-9; P4). The last training trip starts 24.25 h
   before each window (train ends 2026-09-08 / 09-15 / 09-22 23:45); 0 training trips end after a window start
   (42 / 41 / 30 would without the gap, the builder's count, reproduced); trips over 3 h are dropped, so the label
   delay is at most 3 h. Same mechanism and remedy as the precedent row (nyc_taxi_trip_duration_1m, pkdd_15,
   maps_router_eta_1m: a one-day gap). Note: the gap holds because the actor is the taxi company, whose dispatch has
   each trip when the meter stops. A user of the City's open data (a third-party app) would refit on data published
   monthly about 8 days after the month ends, a delay of 1 to 5 weeks; the use case rules this out, but one clause in
   splits_comment ("the company's own trip records, not the City's monthly publication") would make the gap's
   premise explicit. Remedy: optional wording only.

3. Windows and season (SPLIT-12, SPLIT-14, SPLIT-15, SPLIT-20; P4). Three contiguous 7-day windows, 2026-09-10..16,
   17..23, 24..30 (127,478 / 124,777 / 119,351 trips, all kept, under the 500k cap); every window holds each weekday
   once (Sat 13,723-15,239 and Sun 12,689-14,931 trips per window); no public holiday inside (Labor Day 2026-09-07
   and its week fall in training for all three windows; the next holiday is 10-12). One season only (late
   September), as nyc_taxi_trip_duration_1m's three June weeks. History: 2025-09-01 on, a full year with each test
   week's 2025 weeks in training; no break in the collection: per month 2,419-2,821 taxis, 29-33 companies (four
   small ones leave), whole-minute share 0.164-0.188, hidden-tract share 0.468-0.563, the winter dip in counts and
   median duration seasonal. Is September typical? LightGBM (300 trees, 127 leaves, 1M random train rows, the 10
   features with minute of day, weekday and days as numbers) on one-week windows spread over the testable half:
     window start      train share  LightGBM RMSLE  pair-hour median lookup  dummy
     2026-09-24 (ship)   0.979        0.3567          0.4169                   0.7926
     2026-09-17 (ship)   0.960        0.3521          0.4127                   0.7842
     2026-09-10 (ship)   0.942        0.3614          0.4158                   0.7648
     2026-08-20          0.890        0.3565          0.4182                   0.7602
     2026-07-16          0.794        0.3570          0.4208                   0.7380
     2026-06-11          0.691        0.3475          0.4133                   0.7371
     2026-05-07          0.589        0.3556          0.4231                   0.7678
     2026-04-02          0.495        0.3617          0.4287                   0.7402
   The September weeks score inside the April-August range and the order of the two models never changes (gap
   0.054-0.067), so the test season is not atypical. Winter cannot be tested: with one year of history a window
   before April trains on less than 50% (2026-04-02 is already 49.5%, below SPLIT-14's floor). Per SPLIT-21 this
   table does not choose the windows; it only answers SPLIT-20's "atypical season" check. Remedy: none. (If the
   curator wanted a winter window, the mildest route is downloading 2024-01..2025-08 from the same table and spacing
   the windows; not recommended: the precedent is three contiguous weeks, and the test would still be one city's
   autumn weeks plus one.)

4. The 1M sampling keeps the newest months at the same share (SPLIT-20, SPLIT-11; P4, weighed). In every window the
   train side takes 15.2-16.0% of every full month, 2025-09 through 2026-08 (newest window: 0.153 of each month from
   2025-09 to 2026-08; the four weeks before the gap 0.153 too); September 2026 is lower (0.040-0.113) only because
   the windows cut it. Alternative measured: the newest 1M trips before the gap (from 2026-07-14 / 07-20 / 07-27)
   score RMSLE 0.3579 / 0.3504 / 0.3516 (oldest to newest window) against 0.3614 / 0.3521 / 0.3567 for a random 1M
   of the year: the year-long sample costs 0.002-0.005 and keeps the season of the year before. Matches the use
   case ("refit every week on the past year") and the precedent (nyc_taxi_trip_duration_1m, random 1M); SPLIT-21
   bars deciding the history from these three windows. Remedy: none; the numbers may go into version_comment.

5. Taxis and companies across the split (SPLIT-13, USE-10; the builder's issue 5; P4). 99.88% / 99.93% / 99.98% of
   the test trips (newest first) are by a taxi in the 1M train side, the same as in the whole earlier pool; a test
   trip's taxi has a median of 430 training trips (p10 170, p90 870); 1-3 taxis per window are new (of about 2,640).
   Every test company is in every train side (29 active; 33 over the year). The use case is the company's dispatch,
   which knows its fleet, so recurrence is part of the task (SPLIT-13), the split stays temporal (SPLIT-3) and
   taxi_id is a legitimate feature known at pickup (USE-10: for a known entity its history is legitimate). A split
   grouped by taxi would test a new medallion, 0.02-0.12% of the test trips here, not the use case; the builder's
   measurement (without taxi_id RMSLE +0.0018 / +0.0016 / -0.0008) bounds what such a variant could change.
   Issue 5 option (a) (keep) is consistent with the split. Remedy: none.

Smaller checks, no finding
  - Time column: trip_start is the City's start time "rounded to the nearest 15 minutes", local time; a trip
    starting 23:53 before a cutoff lands in the window, as it would at deployment. No DST switch near the windows.
  - Copies across the split: 57.7% of test rows share every feature but the datetime with a training row, 0.0% with
    it (leak probe 5); natural repeats of coarse inputs (LEAK-18), no hidden group in a temporal task (probe: no hits).
  - The splits_comment, task_summary.split and version_comment numbers match the rebuilt plan (test sizes, 94%
    floor, 42/41/30, 1,374,514 rows, training "at least a day before").

Not checked
  - Whether the November 2026 update (not out on 2026-11-09) adds September trips; the three earlier reads say at most
    about 100 trips per update.
  - The live count for start <= 2026-04-01 (the API timed out); the +60 uses the cached table total, which the live
    count for start <= 2026-09-01 (18,061,587) confirms to the trip.

</details>

<details><summary>Domain practitioner</summary>

DOMAIN PRACTITIONER REPORT: chicago_taxi_trip_duration (folder chicago_taxi_trip_duration_1m), 2026-11-09
Role: the actor of the use case. I take the clearest version of it: a Chicago taxi company's dispatch, or the e-hail app
(Curb or Arro) that books its cabs, estimating the ride time when the passenger has named the destination.
Read-only. Scripts and outputs in the run folder (d1_raw.py/.txt, d2_models.py/.txt/.csv, d3_short.py/.txt),
on the claim auditor's cached raw frame (7,689,970 rows) and the participant kit's shipped frame and splits.

VERDICT
Fit: approximate (agree with the builder). Everything the model sees is known at pickup, but the City gives me
centroids of a census tract (49%) or a community area (51%) and a pickup time rounded to the quarter hour. In practice
I have the exact addresses, a routing engine's distance and ETA, and live traffic. The rows also cover only trips
with both ends inside Chicago. USE-8: a coarsened stand-in with a known gap. USE-9 considered and rejected: a planner's
zone-to-zone travel-time table would fit the zones and quarter hours, but not the taxi and company inputs or one row
per trip, and rephrasing the use case to excuse the gap is the factor against it.
Metric: partly. RMSLE scores the relative error of my arrival estimate and picks models the way MAE and MAPE do. RMSE in
seconds (the screening's fallback) does not. Keep rmsle (issue 3 (a)). If the curator wants another metric for
diversity (MET-10), take mae in seconds, the ETA industry's yardstick, not rmse.
Use: as a benchmark of learners on a coarsened real task, yes. As my passenger-facing ETA, no; at most as a prior
behind a routing engine (below).

1. AT PICKUP, DO I HAVE THESE INPUTS?
- The pickup time rounded to 15 minutes: I have the exact minute. This is a City privacy step, already named in
  fit_reason. It loses some of the rush-hour edges.
- Pickup and drop-off tract or community area, with centroids: I have the exact pickup point (GPS) and the
  destination address. For an e-hail booking the address is typed into the app. BACP lets only the e-hail apps (CURB,
  ARRO) quote a fare before the trip, and Curb has offered upfront fares in Chicago since July 2021. For a street
  hail the passenger names the destination to the driver once in the cab, so the company's system knows it only if
  the driver enters it. The use case's "gets in or books a cab and names the destination" covers both channels.
  - 40% of the kept trips were paid through an app (payment_type Mobile), so the booked channel is large.
  - The data cannot tell a booking from a hail. payment_type is recorded at the end and rightly dropped (LEAK-10).
  - The trips with a hidden tract are the long ones: median 18.8 min and 5.5 miles, against 11.3 min and 1.7 miles
    where the tract is shown.
  - The straight line between the centroids correlates 0.90 (tract shown) and 0.80 (tract hidden) with the meter's
    log distance.
- The taxi and its company: known once the cab is assigned. Fine (USE-10: a known fleet, and 99.9% of the test trips
  are by a taxi seen in training).
- Inputs I would always have but the data lacks:
  - a routing-engine distance and ETA. Uber's DeepETA predicts only the residual over the routing engine's ETA.
  - live traffic and weather.
  - the hire channel: app, airport stand or hail. pkdd ships it as call type; here it is not in the source.
  None can be added from this source. All of them belong to the approximate fit, not to a defect of the build.

2. IS trip_seconds WHAT I ACT ON?
Yes. The meter's duration is the time in the cab, which an arrival estimate predicts. It is also the time part of a
metered or upfront fare, which BACP says may not exceed the quote by more than 20%. A number (a point estimate) is
what I show. The log1p shipping scale is the modelling choice (MET-3).

3. ONE ROW, ONE DECISION; IS THE TEST WHAT I FACE?
- One trip is one estimate. A weekly refit predicting next week's trips by a known fleet matches my operation
  (SPLIT-20 with a year of history).
- The test is not everything I face. Trips with a pickup or drop-off outside the city are out:
  - 7.9% of all 61 s to 3 h records;
  - 22.0% of O'Hare pickups (292k of 1,326,053) and 11.7% of the Midway-area pickups;
  - 11.2% of the rides over 45 minutes.
  My app quotes these trips every day with a suburban address. The data has no destination for them, so USE-7 drops
  them, which is right (issue 1 (a)). But this is a selection the real setting does not share. USE-8's selection
  paragraph asks fit_reason to name it, and fit_reason does not (it names the destination stand-in, the coarsening
  and the hidden tract). The `row` field should also say "with both ends in Chicago".
- The 82,914 trips with neither area are not out-of-city trips:
  - median 4.9 miles, 88% with a distance;
  - concentrated in three reporting systems: Chicago City Taxi Association loses 18.8% of its rides,
    "Taxicab Insurance Agency  LLC" 12.1%, Choice Taxi 5.0% (Flash Cab 2.5%).
  The filter's label already says "or not recorded". The curation_comments justify the whole filter by "outside
  Chicago" only and could name this second cause.

4. WOULD I USE THIS MODEL? (LightGBM, 400 trees, on the shipped splits, mean of 3 windows)
- Main model: RMSLE 0.351, MAE 4.21 min, median absolute error 17% of the trip. 66% of trips land within +/-25%,
  and 15.9% run more than 5 minutes over the estimate.
- Baselines: a lookup of the median per community-area pair and hour scores 0.407; a distance-and-hour line 0.423.
- Trust: it learns what a zone-level history can tell. Distrust: no addresses, no traffic, and one trip in six late by
  over 5 minutes. I would not show it to a passenger on its own.
- The benchmark question (which learner extracts the most from these inputs) stays meaningful: the spread from the
  lookup to LightGBM is 0.056.
- Hidden against shown tract in the test: RMSLE 0.36 against 0.34. The coarse half is not much worse.

5. DOES THE METRIC SCORE MY DECISION? (issue 3; MET-1, MET-3, MET-10, MET-11)
- I judge an ETA by its relative error: 5 minutes off on a 10-minute ride is worse than on an hour's. RMSLE measures
  that. Uber's DeepETA blog evaluates by MAE across segments (short against long trips) and trains an asymmetric
  Huber loss (late costs more than early).
- On the shipped splits, three LightGBM variants:

  | model                 | RMSLE  | MAE (min) | MAPE  | within +/-25% | RMSE (s) |
  | log1p target, L2      | 0.3506 | 4.208     | 0.260 | 0.660         | 451      |
  | seconds target, L1    | 0.3538 | 4.206     | 0.262 | 0.665         | 457      |
  | seconds target, L2    | 0.3732 | 4.342     | 0.309 | 0.636         | 443      |

  RMSLE, MAE, MAPE and the share within 25% all put the seconds-L2 model last. RMSE alone puts it first.
- Where the squared error comes from:
  - Under RMSE, the 11.5-13.2% of test trips over 40 minutes carry 65-72% of the squared error, and O'Hare pickups
    32-40%. RMSE ranks models by the long airport rides, exactly what the reason in dataset.py says.
  - Under RMSLE, the 7% of rides of 1-5 minutes carry 27% of the squared log error.
- So RMSLE scores my decision partly: relative and symmetric, where I would weigh lateness more. No source fixes an
  asymmetry weight, so none should be invented (MET-7). context/rmsle is defensible and matches the two siblings.
- If MET-10's diversity factor is invoked, mae in seconds (Uber's metric, closer to a fare quote) is the
  practitioner's alternative. rmse is the worst of the three for this decision.

THE BUILDER'S ISSUES, FROM THE ACTOR'S CHAIR
- Issue 1 (no drop-off area): (a) drop. With the area blank I have no destination, and option (b) asks for an estimate
  "to somewhere outside Chicago", which I never make. Add the selection to fit_reason and `row` (USE-8, above).
- Issue 2 (hidden tract, weak potential leak): (a) keep.
  - In my world the tract is never hidden. Coarsening every trip to its community area (b) moves the inputs further
    from mine, at a cost of 0.024.
  - The City's rule is unpublished for taxis. For the ride-hail (TNP) table, Findings (2021) describes it as "two or
    fewer trips" per census-tract pair "within a 15-minute window", with both ends suppressed. The City's 2019 TNP
    release says "fewer than 3 trips in a given time period".
  - If the taxi table works the same way, the look-ahead covers only other trips of the same quarter hour, weaker than
    the "later that day or month" the note allows. The builder's finding that shown tract pairs form groups of 1 per
    15-minute slot does not fit a taxi-only count. A count that includes the ride-hail trips of the same tract pair
    would explain it; this is unverified, but worth one sentence in the note.
- Issue 4 (60 s cut): right direction. 60 s beats the siblings' 30 s for the reason the builder gives (the whole-minute
  systems write non-rides as 60 s). But the 61-119 s band left in still looks mostly like non-rides:
  - median meter distance 0.10 and 0.25 mile;
  - 29% and 15% with no mile;
  - 68% and 62% with the same centroid at both ends.
  Nobody hires a cab to go 160 m. Under RMSLE it carries real weight. In the newest window, its 744 test trips (0.62%)
  carry 10.6% of the squared log error: RMSLE 0.356 with them, 0.338 without. A model trained and tested with a
  2-minute cut scores 0.336 on the same rows.
  - My preference: (c) 2 minutes, the analogue of the siblings' "nobody names a destination within 100 m" (USE-7
    precedent).
  - (a) is acceptable if the note states the weight. This is the curator's call, not a Must.
- Issue 5 (taxi_id): (a) keep. I know the cab at pickup, and the gain is within noise (+0.0018, +0.0016, -0.0008). A
  medallion is shared by drivers on different shifts, so it carries the cab's reporting system and fleet, little of a
  driver.

GAPS, RANKED BY HOW MUCH THEY CHANGE THE TASK
1. Location resolution: tract or community-area centroids instead of addresses and a route. It halves what a real ETA
   knows, and the long trips are the coarse ones. Named in fit_reason. Cannot be fixed (City privacy).
2. In-city selection: 7.9% of rides, 22% of O'Hare pickups and 11% of rides over 45 minutes are out. Needs naming in
   fit_reason and `row` (USE-8). Not yet done.
3. No routing distance, traffic, weather or hire channel at pickup. Not in the source. Covered by "approximate".
4. Time rounded to 15 minutes. Named.
5. Residual non-rides at 61-119 s, which weigh 17 times their share under RMSLE (issue 4).
6. Same-centroid trips: 557,128 kept trips (8.3%) have the same centroid at both ends.
   - 147,523 share a shown tract: median 5.0 min, 0.51 mile, 13% with no mile; 7,278 of them run over 40 minutes
     (median 4.6 miles, round trips or waits).
   - 409,605 share a hidden community area: median 6.6 min, 0.99 mile, mostly real short rides.
   The siblings drop ends within 100 m (USE-7 precedent of 2026-10-26). The record's size check (point 3) asked for
   this count. The centroids cannot locate a return to the start, so the rule cannot be applied here, but the notes
   should say so: a departure from a precedent, with the fact that sets it apart.

WHAT AN EXPERT WOULD CHANGE (none is a blocker)
- fit_reason and `row`: name the in-city selection, with the O'Hare and long-ride shares (USE-8).
- curation_comments: say why the 100 m rule is not applied (the same-centroid counts above), and that the trips
  without either area come mostly from three reporting systems.
- Issue 4: consider the 2-minute cut, or state the RMSLE weight of the 61-119 s rows.
- Issue 2 note: cite the TNP rule as the nearest public description and narrow the leak's reach to the quarter hour if
  the curator accepts it.
- use_case wording (optional): name the e-hail booking (Curb or Arro, where BACP allows a quoted fare) as the cleanest
  moment the destination is known before the meter starts.
- Keep: the post-trip drops (LEAK-10), the 3 h cut, the weekly refit with its 1-day gap, taxi_id, company as
  reported, and rmsle.

SOURCES
- City of Chicago, Taxi Trips (2024-), ajtu-isnz: https://data.cityofchicago.org/Transportation/Taxi-Trips-2024-/ajtu-isnz
  (description via https://catalog.data.gov/dataset/taxi-trips-2024): "Census Tracts are suppressed in some cases",
  times "rounded to the nearest 15 minutes".
- Findings (2021), "Ride-hailing data suppression and exclusion strategies can lead to biased outcomes":
  https://findingspress.org/article/34191 (the TNP rule, two or fewer trips per tract pair in a 15-minute window,
  both ends suppressed; not stated for taxis).
- City of Chicago press release on the TNP data (2019, "fewer than 3 trips in a given time period"):
  https://www.chicago.gov/city/en/depts/mayor/press_room/press_releases/2019/april/TransportationNetworkProviderData.html
- Todd W. Schneider on the Chicago taxi data ("multiple trips within the same tract over the same 15-minute
  interval"): https://toddwschneider.com/posts/chicago-taxi-data/
- BACP public chauffeur reminders (2024, 2025): only passengers from a taxi e-hail app (CURB or ARRO) may pay a quoted
  fare; dynamic pricing only through an e-hail app; the final fare at most 20% above the quote. Read from the search
  index; the PDFs returned 403 to a direct fetch.
  https://chicago.gov/content/dam/city/depts/bacp/publicvehicleinfo/publicvehicleindustrynotices/2025/publicchauffeurreminders.pdf
- CBS Chicago (2021-07-13), Curb upfront pricing for Chicago taxis:
  https://www.cbsnews.com/chicago/news/curb-app-taxis-uprfont-pricing
- Uber Engineering, "DeepETA: How Uber predicts arrival times":
  https://www.uber.com/us/en/blog/deepeta-how-uber-predicts-arrival-times/ (the residual over the routing-engine ETA,
  traffic and request type as inputs, an asymmetric Huber loss, MAE across segments).
- Rules: use_case.md USE-1, USE-3, USE-5, USE-7 (with the nyc/pkdd 100 m case), USE-8 (selection paragraph), USE-9,
  USE-10. metrics.md MET-1, MET-3, MET-7, MET-10, MET-11.

</details>

<details><summary>Blind review</summary>

BLIND REVIEW: chicago_taxi_trip_duration
Inputs used: the clean room's data.parquet (200,000-row sample of 1,374,514), its task.md, the City of Chicago portal
metadata for wrvz-psew and ajtu-isnz, and public web pages. I opened no other file on this machine.
Scratch script: model.py

VERDICT
Include with changes. This is a real, well-known pre-trip ETA task. The prepared columns do not leak the target, and
the signal is solid (LightGBM R2 about 0.77 against about 0.67 for an origin-destination mean). But the rows are
sampled at very different rates over time: the table jumps 6.6x in density at 2026-09-10. That should be fixed and
documented, the test windows should be set by calendar time, and hour and day-of-week should be explicit columns.

WHAT THE TASK IS
The task predicts log1p(trip seconds) for a Chicago taxi trip. The inputs are known when the trip starts: taxi (hashed),
company, pickup and dropoff census tract and community area, their centroid lat/lon, and the start time (rounded to
15 minutes). The source is the city's regulator feed, "Taxi Trips (2024-)" (ajtu-isnz). The covered span is
2025-09-01 to 2026-09-30. A dispatcher, a fare or ETA quote for a passenger, or a city planner would make this
prediction at pickup, once the destination is known. This is the same setup as the well-known NYC taxi-duration task,
with coarser locations. It is a real use.
Leakage check passed: fare, tips, tolls, extras, trip_total, payment_type, trip_miles and trip_end_timestamp are all
removed. Fare is computed from time and distance, and trip_end directly gives the duration, so dropping them was
necessary.
Size: 1.37M rows and 11 features, plenty to score. The target range is 61 to 10,787 s (median 840 s). Missing values:
census tracts 50.5% (pickup and dropoff are always missing together, from privacy suppression), pickup community area
0.01%, dropoff community area 0.5%. No other column has missing values.

SIGNAL (LightGBM 2000 trees with early stopping. Train = all sample rows before the window. Test = the window.)
  window              n_test  OD-area-mean R2  LGBM raw cols  LGBM +dist/hour/dow  dist only
  2026-09-10..16      18,559  0.665            0.711          0.765 (RMSE 0.370)   0.692
  2026-09-17..23      18,051  0.692            0.720          0.786                0.717
  2026-09-24..30      17,323  0.694            0.705          0.787                0.711
  2026-06 (month)     14,480  0.646            0.707          0.763                0.682
  Feature importance (gain): centroid distance 57%, pickup area 11%, dropoff area 6%, hour 5%, taxi_id 3%.
  Dropping taxi_id costs about 0.006 R2.
The task is not trivial and has room for better models, but distance dominates. Expect modest gaps between strong
methods.

CONCERNS, MOST TO LEAST SERIOUS

1. Rows are sampled at very different rates over time, and task.md does not say so (high).
   Evidence: per day, the sample holds about 391 rows from 2025-09-01 to 2026-09-09. From 2026-09-10 to 09-30 it
   holds about 2,568 per day, 6.6x more. The step is sharp at midnight: 09-09 has 426 rows and 09-10 has 2,766.
   September 2026 is 57,496 of the 200k sample rows (29%), against 9-14k for every other month. Scaled to the full
   table, that is about 2,700 trips per day before the step and about 17,600 per day after. The later rate looks
   like full coverage of Chicago taxi volume, so the earlier year looks like a ~15% subsample.
   The step is an artefact, not a real change: nothing else changes across it. The top-5 company shares, the O'Hare
   share (15.6% vs 17.7%), the target mean (6.79 vs 6.82) and the tract-missing rate (52.6% vs 50.7%) all stay about
   the same. There is no duplication either: 1 exact duplicate row in 54k post-step rows.
   Effect: about 27% of all rows fall in the last 21 days. Any test windows sized by row count therefore all fall
   inside Sept 10-30, 2026: one season, no holidays, and three windows that are strongly correlated. The training
   set also misstates the real time-density of trips.
   CONFIRMED FROM THE SOURCE (a late API reply, saved in api_monthly_3.json): the portal's daily
   trip counts have no step. 2026-09-08: 19,295; 09-09: 20,636; 09-10: 21,436; 09-11: 20,813; 08-25..09-30: about
   14.6k-25.3k per day. So the jump was introduced when the table was prepared, not by the source. After the step,
   the table keeps about 85% of the source's daily trips (the rest are presumably the dropped short or out-of-city
   trips). Before it, the table keeps only about 13%.
   Fix: re-pull so the sampling rate is the same over the whole span, either all trips over a shorter span or a
   uniform random sample over the whole span. Set the 3 test windows by calendar time (for example the last three
   months, one each), and document how the data was pulled.

2. Time-of-day and day-of-week exist only inside a datetime column (medium).
   Evidence: with trip_start given to LightGBM as a raw timestamp, R2 is 0.705-0.720. With hour and day-of-week
   (plus centroid distance) added, it is 0.763-0.787. Hour alone carries 5% of the gain. A numeric timestamp is also
   useless under a temporal split, because the test times all lie beyond the training range.
   Fix: add an hour (or 15-minute slot) column and a day-of-week column, and optionally a holiday flag. All are known
   at pickup. Keep trip_start only as the split key, unless the harness reliably expands datetime columns.

3. Target noise and filters that task.md does not document (medium-low).
   Evidence:
   - 17.0% of durations are exact multiples of 60 s. This depends on the company: Transit Administrative Center Inc
     100%, Chicago City Taxi Association 100%, "Taxicab Insurance Agency  LLC" 100%, Choice Taxi 34%, Flash Cab 1.7%.
     So some meters report in whole minutes.
   - 149 rows (0.07%) imply straight-line speeds above 100 km/h. For example, Loop to Morgan Park, 21.3 km in 158 s.
   - O'Hare-to-O'Hare trips (0.9% of rows) range from 61 s to 3 h.
   - The target was clearly filtered to 61 s <= duration < 3 h. All rows have centroids, so trips starting or ending
     outside Chicago were dropped. task.md mentions neither filter.
   Fix: document both filters. Drop the rows with physically impossible speeds. Keep company as a feature, since it
   lets models learn the minute rounding.

4. Coarse inputs make this a lower-fidelity stand-in for a real ETA system (low; inherent).
   Evidence:
   - 50.5% of rows have only a community-area centroid (77 areas), because the tract is privacy-suppressed.
   - 8.2% of trips have identical pickup and dropoff centroids, so their distance is 0.
   - Times are rounded to the nearest 15 minutes. The portal says: "times are rounded to the nearest 15 minutes".
   - Tracts are shown only when several trips share a tract and 15-minute interval (Schneider's description of the
     feed). So whether a tract is missing is decided after the fact and acts as a weak busyness signal. It does not
     leak this trip's duration.
   Change: none needed. State the coarseness in the task card.

5. Cross-row signal through taxi_id plus trip_start (low).
   Evidence: in the dense test period, the full table holds nearly every trip of every taxi, and the same taxi's next
   start time bounds this trip's end. Even in the 14.6% sample, the gap to the next same-taxi trip (within 1 h)
   correlates 0.21 with the target. Standard row-wise models cannot use this. Transductive or feature-engineering
   pipelines that look across test rows could.
   Change: forbid cross-row features in the benchmark protocol, or drop taxi_id. Dropping it costs only about 0.006 R2.

6. Minor preparation points (low).
   - Centroid lat/lon are a one-to-one recoding of tract or area: 253 unique pickup points = 176 tracts + 77 areas.
     Redundant but harmless, and useful as numeric geography.
   - Company name variants exist: "Taxicab Insurance Agency Llc" (27,123 rows, 1.5% minute-rounded) and
     "Taxicab Insurance Agency  LLC" (1,309 rows, 100% minute-rounded). They behave differently, so leave them
     unmerged.
   - 583 of 3,038 taxi_ids appear under more than one company.
   - Census tracts are stored correctly as categorical strings, not numbers.
   - 1 exact duplicate row and 42 rows that match on all features (same taxi, same 15-minute slot, same origin and
     destination, different durations). Both are negligible.

WHAT I COULD NOT CHECK
- The Socrata API was mostly down (503/500). One daily-count query for 2026-08-25..09-30 finally succeeded (see
  concern 1) and confirmed the jump comes from the preparation. I could not get monthly counts for 2025-09..2026-08,
  so the exact retained fraction per earlier month is estimated from the sample.
- The exact boundaries and sizes of the "3 test windows". task.md does not give them, so I emulated weekly and monthly
  windows.
- The full 1.37M rows. I worked only on the 200k sample.
- How the benchmark harness treats datetime and high-cardinality categorical columns.
- Why the span starts at 2025-09-01, given the source covers 2024 onward.

</details>

<details><summary>Task gamer</summary>

TASK GAMER REPORT: chicago_taxi_trip_duration (target log1p_trip_seconds, RMSLE = RMSE on the log1p scale, 3 one-week temporal test windows)

Verdict: the task can only be gamed a little. The one in-protocol exploit, using the same taxi's next pickup among the test rows, takes 0.0053 off the RMSLE (1.5%, about 7x the noise). Larger gains come only from rows of data.parquet outside a split's train set.

Setup. Kit: 1,374,514 rows, 11 features (taxi_id hash, pickup/dropoff census tract and community area, company, centroid lat/lon, trip_start rounded to 15 min). data.parquet is a thinned sample (about 2.8k trips/day) up to 2026-09-09, then every trip (about 18k/day) from 2026-09-10 to 2026-09-30. The three test weeks are 09-10..16 (r2), 09-17..23 (r1) and 09-24..30 (r0). Each split's training set has 1,000,000 rows, thinned to about 2.8k/day on every day, including the full-density September days. There is a one-day gap before each test window. No training row is dated after its test window.
Every number below is LightGBM with 500 rounds, lr 0.1, 127 leaves and 4 threads, scored with score.py on the shipped splits. Scripts are in the kit's work folder.

HONEST BASELINES (baseline.py)
  raw features (trip_start as a number)         r0 0.39463  r1 0.38778  r2 0.39535  mean 0.39259
  + hour, dow, hour-of-week, haversine and Manhattan distance, same-area flag, tract-missing flag ("better honest")
                                                r0 0.35296  r1 0.34726  r2 0.35865  mean 0.35296   <- the reference below
  Noise: the better model plus a column of random numbers, 3 seeds (more.py noise): means 0.35356, 0.35360 and 0.35321.
  A per-split move of up to 0.0007 is noise.

EXPLOITS RANKED BY GAIN

| # | Exploit | Script | Honest score | Exploited score | Gain (per split) | A deployed model has it? | Fix |
|---|---|---|---|---|---|---|---|
| 1 | Same taxi's NEXT pickup time and place, read from the test rows (time to the next pickup, the one after it, whether the next pickup is at this drop-off area, distance from this drop-off to the next pickup, the taxi's trips in the same 15-min slot) | chain.py (leak_next) | 0.35296 | 0.34770 | r0 0.00556, r1 0.00510, r2 0.00513 | No: at pickup the taxi's next pickup is in the future | Hide taxi_id in the test rows (or replace it with a per-row random id). Or thin the test windows to the training density, which breaks the chains. |
| 1b | Same as 1, computed over every row of data.parquet and trained on every pre-cutoff row (out of protocol) | more.py chain_allrows | 0.35296 | 0.34298 | r0 0.0141, r1 0.0114, r2 0.0044 | No | As 1. A harness that passes only the split's rows already caps it at #1. |
| 2 | Train on data.parquet rows dated AFTER the test window (the later folds' full-density test weeks, with labels). Out of protocol. | more.py outofprotocol | r1 0.34637, r2 0.35865 (honest, with every past row) | r1 0.34090, r2 0.34418 | r1 0.0055, r2 0.0145 (r0 has no later rows) | No: future labels | Pass a model only the train and test rows of its split. Do not ship later weeks' labels with an earlier fold. |

Not ranked: looking rows up in the published source (Socrata ajtu-isnz). The API returned "service unavailable" during this run, so I did not test it. By construction it would return trip_seconds for any row matched on trip_start, area and taxi.

FLAWS THAT HURT AN HONEST MODEL

| What is wrong | Honest choice that avoids it | Shipped score | Honest-choice score | Fix |
|---|---|---|---|---|
| The training set is capped at 1M rows by thinning every day to about 2.8k trips. r0 and r1 lose 236k and 109k past rows that a deployed model would have, most of them from the full-density September days just before the test week. | Train on every row dated before the cutoff (past only; out of protocol) | 0.35296 (r0 0.35296, r1 0.34726, r2 0.35865) | 0.35125 (r0 0.34873, r1 0.34637, r2 0.35865) | Keep the most recent days at full density in training, or raise the cap. |
| Density mismatch: training chains are 15%-thinned, test chains are complete. Honest history features (time since the same taxi's previous pickup, whether the previous drop-off area equals this pickup area), which a dispatcher knows at pickup, get worse instead of better. | None inside the protocol | 0.35296 | 0.35371 with the honest previous-trip features (worse) | Sample training and test the same way: both thinned or both complete. |
| Census tracts are hidden by a count-based privacy rule in the source. A deployed model knows the exact pickup and requested drop-off tract on every trip; the benchmark hides them on 51% of rows. | None (comes from the source) | 0.35296 | n/a. For scale: dropping all tract information gives 0.38097, which shows how much location precision is worth. | None needed in the task. Document it. |

FINDINGS IN DETAIL

1. Next-pickup chain (exploit #1).
   In the full-density test weeks, 98% of test rows have a later trip of the same taxi in the test window. The median time to the next pickup is 45 min. 25% of trips end less than 9 min before the taxi's next pickup.
   Duration is at most the time to the next pickup plus 15 min (the start-time rounding). Only 0.7% of rows break this bound.
   A LightGBM fit on the thinned training chains improves every split by 0.0051-0.0056. Applying the bound on top as a hard cap adds nothing (r0 0.34763).
   The gain stays small for two reasons. The 15-min rounding of trip_start makes the bound loose for the typical 10-15 min trip. The training chains are 15%-thinned, so the model learns the relation from few tight cases.
   Using the honest prediction plus the bound as a truncated-normal posterior, with no training, gains only 0.0007 (chain_stack.py: 0.35224).
   A stacker cross-validated inside the test week (it uses test labels, so it is a ceiling only) reaches 0.34398. That puts the full value of the chain at about 0.009.
   Mildest fix: give test rows a taxi_id that cannot be linked to the taxi's other test rows.

2. Rows outside the split (exploit #2, and #1b).
   data.parquet ships every week with labels, including the full-density weeks after r2's and r1's test windows. Training r2 on them (future labels) gives 0.34418 against 0.35865 with every past row.
   This is only possible if a submission can read rows outside its split. score.py's protocol passes train and test positions, so under that protocol it is not open.
   Fix: give each fold only its own train and test rows.

3. Tract suppression (artefact, not an exploit; already in features()).
   Pickup and drop-off tracts are hidden together on 51% of rows. Visibility rises with the number of trips in the same (pickup area, drop-off area, 15-min slot): from 0.09 for a lone trip to 0.85 for 10 or more. It also rises with the hour of day: about 0.05 at 3-4 am and about 0.9 in the daytime. So the rule counts trips that happen at the same time.
   Within one (area pair, slot), the shown share falls from 0.83 for the shortest-duration decile to 0.63 for the longest. That pattern could come from location (busy central tracts give short trips) or from a rule that counts drop-off-window trips. One fact would decide it: whether the city's rule counts trips by end window.
   The visibility flag alone is worth 0.003 (no tract information 0.38097 → flag added 0.37804; ablation_tract.py). It is in the baseline already.

ATTACKS THAT FOUND NOTHING
- Row order. The file is sorted by trip_start; inside a 15-min slot the order is random. Correlation of position-in-slot with the target minus its slot mean: 0.0001. Lag-1 correlation of de-meaned targets: -0.026. (explore1.py)
- Formats. Every centroid comes from a fixed tract or community-area centroid; decimals (6-9) carry no target information. trip_start is always on :00/:15/:30/:45 with seconds 0.
  trip_seconds is a multiple of 60 for 17% of rows. That comes from 11 companies that record whole minutes (share 1.0) against about 0.017 for the others. It is a company recording format known at pickup, worth nothing beyond the company column.
  The company name has two spellings ("Taxicab Insurance Agency Llc" and "... Agency  LLC" with a double space), both used over the whole year. They act like two companies, which is legitimate. (explore4.py, explore5.py)
- Target range. 61 to 10,787 s: trips of 60 s or less and of 3 h or more are filtered out of train and test alike. Not exploitable.
- Statistics of the test rows: per-day and per-slot trip shares (city, pickup area, drop-off area, area pair) and mean slot distance, each computed per side. r0 +0.0012, r1 +0.0028, r2 -0.0031 (mean 0.35328). Mixed signs: nothing. (more.py teststats)
- Train-vs-test classifier without the time column: AUC 0.67-0.68, driven by taxi_id (the active fleet drifts). Only 0.02-0.12% of test rows have a taxi never seen in training. (adv.py)
- Copies across the split: impossible by construction (disjoint weeks). The same taxi on the same route earlier is legitimate history.
- Honest training-window choices (the opposite flaw): last 12 months 0.35384, last 6 months 0.35768, last 3 months 0.36593, time-decay weights with a 120-day half-life 0.35616. All are worse than training on everything (0.35296), so the full shipped history is not hurting.
- Public "magic features": the web searches found no competition, leak thread or write-up for Chicago taxi duration. The 2024- dataset page states only "tracts suppressed in some cases, times rounded to 15 min".

WHAT I COULD NOT CHECK
- The source lookup (the Socrata API was unavailable).
- The exact tract-suppression rule of the 2024- taxi dataset, so I could not settle whether the visibility flag encodes the end window (finding 3).
- Whether the full-density weeks are the complete source or a filtered version (rows outside Chicago without a centroid look dropped). Median gap 45 min and 7.8 trips per taxi-day suggest near-complete.

Scripts: common.py, baseline.py, chain.py, chain_dense.py, chain_stack.py, more.py (noise | teststats | window | outofprotocol | chain_allrows), ablation_tract.py, adv.py, explore1-7.py, explore_chain.py. Logs beside them.

</details>

<details><summary>Precedent check</summary>

PRECEDENT CHECKER: chicago_taxi_trip_duration (folder chicago_taxi_trip_duration_1m), 2026-11-09

Verdict
  Consistent: the metric (rmsle from context), taxi_id as a feature, year 2026, one Chicago record or two (nothing
  here decides it), and the smaller calls (3 h cut, copies, fit approximate, domain, no hour column, per-window
  sampling).
  Departs with a stated reason that covers only part of the cut: the 60 s short-record cut (issue 4).
  Departs without a written reason, though a fact or a cheap fix is at hand: the location filter's mechanism
  (issue 1), the siblings' 100 m rule, the siblings' daylight-saving fix, the siblings' 120 km/h straight-line rule.
  Not reasonable as an exception under the ranking: the hidden tract kept with a `Potential leak, kept on purpose`
  note (issue 2). The claim and column audits measured that the City's suppression reads the trip's own arrival slot.
  LEAK-10 is a Must and has no weak grade for "missingness that encodes the outcome". So a keep needs one of two
  things: the medical_facility_operational_data measurement (the flag's worth within seed noise, under LEAK-10's
  second clause by analogy) or an amendment. Otherwise the remedy is coarsening.
  Six reflection prompts follow (section 3), one per departure without a full reason.

Inputs read: PANEL_COMMON.md; the precedent-checker brief and principles.md (df-large); builder_report.md; the
claim_auditor, column_auditor, domain_practitioner, split_auditor and blind_reviewer reports; register.json (flags and
decisions); dataset.py of chicago_taxi_trip_duration_1m, nyc_taxi_trip_duration_1m,
pkdd_15_taxi_trip_time_prediction_ii_1m, sendy_logistics_challenge, 2024_lusaka_mobility_prediction_hackathon,
chicago_traffic_crashes, delivery_eta_1m, maps_router_eta_1m, cooking_time_1m, food_delivery_time, sf_permit_time,
brazilian_ecommerce, video_transcoding_time_prediction; the records of these, of chicago_taxi_trip_duration,
chicago_rideshare_trip_duration, meituan_food_delivery_time, bank_marketing, 2_month_survival_rate_prediction,
noaa_storm_events_damage, santander; leak_checks.md, use_case.md, metrics.md, provenance.md, cleaning_features.md,
splits.md, selection.md (risk factor); pkdd's REVIEW.md before the 2026-10-26 marks (git 1f6c61c0^).
All paths are in the repository unless stated.
My own numbers come from p1_location.py/.txt and p2_same_centroid.py/.txt. Both run on the
claim auditor's raw.parquet (7,689,970 trips), with the definition's filters re-applied.

**1. PER DECISION**

D1. Trips without a pickup or drop-off area dropped (builder issue 1; USE-7)
  Status: the drop CONSISTENT; its implementation DEPARTS WITHOUT A REASON (prompt 2).
  Precedents:
   - USE-7 Cases row, nyc_taxi_trip_duration_1m and pkdd_15_taxi_trip_time_prediction_ii_1m (Lennart, 2026-10-26):
     "the cut rests on the inputs, not on the travel time".
     Files: .claude/skills/knowledge-curation/references/use_case.md; curation/records/pkdd_15_taxi_trip_time_prediction_ii.md.
   - pkdd: drops "fewer than 2 GPS points (no travel time or no destination)" and keeps ends outside Porto (only
     the start must lie in Greater Porto).
   - nyc: keeps destinations outside the city inside a wide box (airports, NJ, Long Island, Westchester, CT) and
     drops only 38 GPS errors.
   - lt_vehicle_loan_default_prediction (Lennart, 2026-11-05): a population the actor faces but the data lacks is
     named as a selection. Also USE-8, amended 2026-10-27: fit_reason names a selection.
  Facts compared:
   - A trip with no destination at all is no task row (USE-7), as in pkdd. This is consistent.
   - The code reads the centroid. The notes, the decision table and `changes` say "area".
   - Outside Chicago, the centroid exists only for tract 17031770700 next to O'Hare, and only when the City shows
     that tract. A hidden tract gets the community area's centroid, and this tract has none. So 31,945 drop-offs
     and 905 pickups (32,850; 0.49% of kept rows) are kept because of a flag that reads the arrival slot (D2).
   - 6,334 trips to 220 other suburban tracts are dropped although their tract is shown.
   - A filter on the community area (never suppressed) would drop 32,603 more trips. Every row it keeps has a
     centroid (p1_location.txt).
   - fit_reason does not name the dropped O'Hare-to-suburbs segment: 7.4% of raw trips, 22% of O'Hare pickups
     (claim audit).
  Fact that sets it apart from nyc's out-of-city keep: Chicago publishes no point for suburban destinations. That
  fact supports the drop. It does not support keeping 7707 only when shown.

D2. The hidden tract kept as published (builder issue 2; LEAK-10, LEAK-30)
  Status: NOT REASONABLE AS AN EXCEPTION UNDER THE RANKING (prompt 1).
  The audits' fact:
   - Claim audit C7: among shown tracts, the drop-off is alone by its end slot in 1.2% of trips against 5.4% by its
     start slot. The null on the community areas shows no difference.
   - Column audit A: within cells, the hidden indicator regresses on the own end-slot count at -0.198 (SE 0.003),
     against +0.006 to +0.014 for the neighbouring slots.
   - So this is LEAK-10's listed "missingness that encodes the outcome", measured.
  The builder's label does not fit:
   - LEAK-30's weak grade covers scaling over all rows (bioresponse, cooking_time, delivery_eta, maps_router_eta,
     credit_card_customers, taiwanese_bankruptcy_prediction, lung_cancer_epithelial_genexp; Lennart, 2026-10-19).
     None of these reads the outcome.
   - LEAK-38's keep covers fields of a host's own competition whose timing cannot be tested. Its last clause sends a
     measured mechanism to LEAK-10's drop. Chicago is a City register, and the mechanism is measured.
   - PROV-3 (framingham, Lennart, 2026-10-21) keeps disclosure control as published. It is a P5 rule on real data
     and does not outrank P4.
  Precedents that removed missingness or recording tracking the outcome:
   - chicago_traffic_crashes, the same City portal: five condition fields dropped, whose filled-in flags carried 72%
     of their 0.0039 log-loss gain (Lennart, 2026-11-04). `dooring_i` dropped at a cost of 0.00011 (Lennart,
     2026-11-05). The 0.00098 row-order leak fixed (Lennart, 2026-11-05).
   - 2_month_survival_rate_prediction: `edu` and `income`, missing more often among deaths, dropped (Lennart,
     2026-10-26). This superseded his keep of 2026-10-12.
   - kick `WheelType` and expresso_churn_prediction `REGION` (Lennart, 2026-10-22).
   - mic (the prediction point moved).
   - santander `has_*` (+0.003 AUC; LEAK-6: "a confirmed leak goes even when small").
   - bank_marketing `campaign`: kept with a note 2026-11-06, then dropped 2026-11-08 (worth 0.0013-0.0016 ROC AUC).
  Precedents that kept a value set after the prediction point:
   - onlinenewspopularity (2026-10-26): the traced part shows no gain.
   - medical_facility_operational_data (2026-11-05): late cells not locatable row by row; the whole field's worth is
     an upper bound and sits within about two seed SDs.
   - noaa_storm_events_damage, Flash Flood duration (2026-11-08, X4): spans only. Kept when the outcome draws a
     minority and the field keeps its worth elsewhere. "The size of the worth alone never decides".
   - digicow `topics_list` (2026-10-21): a known input, which the flag is not.
  Fact that sets Chicago apart:
   - The missingness is the City's disclosure control.
   - It hides a field whose shown values carry ten times the flag's worth (0.024-0.025 against 0.0016-0.0024 RMSLE).
   - No remedy short of coarsening removes it, because the hiding is joint.
   - Every removal precedent gave up at most a small legitimate part (crashes: 28% of 0.0039).
   - This is an argument from the remedy's cost. X4 says size alone cannot decide. So it supports an amendment
     (prompt 1, d), not an exception to a Must.
   - One existing route keeps the flag: the medical_facility measurement. Its seed noise is not measured yet: the
     builder ran one seed per window, with the same sign on 3 of 3 windows.
  Drift and third exception:
   - The curator's own LEAK-10 calls on outcome-linked values moved toward removal: 2_month_survival (2026-10-12 to
     2026-10-26) and bank_marketing (2026-11-06 to 2026-11-08). Each is recorded with "supersedes", so it is a
     deliberate correction, not drift.
   - A keep here would be the first kept outcome-reading missingness, so no amendment is due by count.
   - The note's mechanism ("other trips of the same tract pair later that day or month") is refuted. Under any option
     the note, fit_reason and decision table 5 need the end-slot wording.

D3. Metric rmsle from context instead of the screening's fallback rmse (builder issue 3; MET-1, MET-10, MET-11)
  Status: CONSISTENT.
  Precedents:
   - MET-11 `context` was born on diamonds (Lennart, 2026-10-21): "a price's error matters relative to the price".
   - Durations from a register or a dataset without a metric:
     - sf_permit_time: City of San Francisco register, waiting time, rmsle from context. Lennart accepted the scoring
       on 2026-10-21.
     - brazilian_ecommerce: delivery time, same day.
     - video_transcoding_time_prediction: rmsle checked by Lennart, 2026-11-08.
   - The same task scored RMSLE as its source's metric: nyc_taxi_trip_duration_1m (checked 2026-10-21) and
     pkdd_15_taxi_trip_time_prediction_ii_1m (checked 2026-10-26).
  Not contrary:
   - 2024_lusaka_mobility_prediction_hackathon (RMSE minutes, Lennart, 2026-11-04) and sendy_logistics_challenge
     (RMSE seconds, 2026-11-05) score their sources' own metrics (MET-4).
   - food_delivery_time's fallback rmse is an AI declaration (2026-10-21), never argued from context or checked by a
     curator. It is no precedent, but it is a pair with brazilian_ecommerce worth a look on its own record.
   - noaa_storm_events_damage left RMSLE because its actor sums dollars (2026-11-08). The ETA actor judges each trip.
  One wording point (MET-10):
   - The metric is chosen per dataset, never for a family. The reason now leans on the siblings' competitions.
   - Lead with this dataset's own measurement instead (claim audit C31): trips over 1 h (3.8-4.8% of test trips) hold
     38-45% of the squared error in seconds, and the two metrics rank two fits in opposite order on 3 of 3 folds.
   - Diversity decides only in doubt. If the curator wants diversity anyway, the domain practitioner proposes mae in
     seconds, not rmse.
   - The screening's fallback was provisional (principles, Stages).

D4. Short-record cut at 60 s against the siblings' 30 s (builder issue 4; USE-7, CLEAN-1, CLEAN-11)
  Status: DEPARTS WITH A STATED REASON THAT COVERS PART OF THE CUT (prompt 3).
  Precedents:
   - pkdd: Lennart chose 30 s together with the 100 m rule (2026-10-26, issue 2 (c)). The AI had recommended 45 s,
     and 60 s was implemented. The definition says the 30 s cut "replaces a 1-minute cut on the recorded time, which
     sat on a smooth slope and also dropped short rides that moved". It holds "once [the trips within 100 m] are
     gone".
   - nyc: 30 s with the 100 m rule (2026-10-26).
   - sendy_logistics_challenge: pickup legs of 60 s or less dropped on the source's words (Lennart, 2026-11-05).
  Facts:
   - The stated reason covers the 28,871 records of exactly 60 s. Whole-minute systems wrote 26,044 of them at 82%
     without a mile; seconds systems wrote 2,827 at 67% without a mile, a spike against about 850 at 59 s and 61 s.
   - It does not cover the 39,118 records of 30-59 s: 19,119 without a mile, 19,999 with one. The seconds systems
     there sit on a smooth slope: 38-42% without a mile at 55-59 s, 34-36% at 61-64 s. This is pkdd's situation.
   - The fact that sets the band apart is evident but unwritten: centroids allow no 100 m rule, and pkdd's 30 s rested
     on that rule.
  Correction to builder issue 4: option (b)'s "keeps 68k non-ride-like records" counts every record of 30-60 s.
  42,387 of them have no mile and 25,598 have one.

D5. taxi_id kept as a feature (builder issue 5; USE-10, SPLIT-13)
  Status: CONSISTENT.
  Precedents:
   - pkdd: `taxi_id` is a categorical feature, and the decision table says "the taxi stays a feature, not a group"
     (panel 2026-10-20, shipped by Lennart 2026-10-26).
   - USE-10 known entity; LEAK-34; SPLIT-13 (split audit: holds).
   - The screening's "grouping column" is superseded by the measured 99.88-99.98% seen share (principles, Stages).
  Related panel points that follow precedent:
   - Column audit B, a LEAK-9 protocol line, as in medical_facility_operational_data (2026-11-04),
     azure_vm_lifetime_resource_central_1m, fremtpl2, frempl_french_motor_personal_line and
     ppnn_ecmwf_t2m_postprocessing_germany_1m.
   - pkdd has the same channel (taxi_id with exact starts) and no line. Under Lennart's rule of 2026-11-08 (a
     per-dataset choice is a per-dataset issue), that goes into pkdd's own REVIEW.md, not into a cross-dataset item.
   - Column audit F (shared reporting ids): a note; the feature stays (LEAK-34).

D6. Year 2026 against the record's 2016 (PROV-9)
  Status: CONSISTENT.
   - PROV-9: "A source that grows over time (a public register ...) takes the year of the snapshot we pin."
   - chicago_traffic_crashes, on the same portal, ships `year = "2026"` for its pinned snapshot (wording of 2026-11-04,
     shipped by Lennart 2026-11-05).
   - The record's 2016 is the 2013-2023 table's year. The record needs fixes: year, the name (it names both tables),
     source_links, and the Metric line.

D7. One Chicago trip record or two (chicago_rideshare_trip_duration; PROV-6, PROV-7)
  Status: CONSISTENT (no departure in this definition; the call stays on the rideshare record).
   - Tension row "same task, another source" (Lennart, 2026-11-08): both enter when neither is better data, e.g.
     nyc_motor_vehicle_collisions next to chicago_traffic_crashes.
   - The TNP table holds other trips for another actor (a ride-hail app against taxi dispatch). It has more rows and
     shared-trip flags but no taxi or company inputs. So neither is better data.
   - PROV-7 holds: a shared publisher with distinct trips is no duplicate. PROV-6 does not apply: no cut of one cohort.
   - The rideshare record's risk point "the task already covered" is no factor of selection.md. Its risk factor
     counts "better data found for the same task", which this is not. Fix it at that record's review. The curator's
     `Yes` here (2026-11-08) does not decide rideshare (`TBD -> 2nd Tier`).

D8. The siblings' 100 m same-place rule not applied (claim audit I5-i; USE-7)
  Status: DEPARTS WITHOUT A WRITTEN REASON. The fact that sets it apart exists and has a precedent (prompt 4).
  Precedents:
   - nyc and pkdd (Lennart, 2026-10-26).
   - 2024_lusaka_mobility_prediction_hackathon (Lennart, 2026-11-04): on the source's straight line from unmasked
     points.
   - sendy_logistics_challenge (shipped by Lennart, 2026-11-05) keeps two orders 89-90 m apart: "The 100 m radius of
     nyc, pkdd and Lusaka rests on exact coordinates."
  Facts (p2_same_centroid.txt):
   - 557,128 kept trips (8.35%) share a centroid: 147,523 in one shown tract and 409,605 in one community area with the
     tract hidden.
   - 514,679 of them (92%) record a mile: median 0.59 mile in a tract and 1.03 in an area, median 5-7 minutes.
   - 42,433 record no mile.
   - The record's size check asked for this count (2026-11-08).

D9. Daylight-saving trips kept (claim audit C14, C28; column audit C; USE-5, CLEAN-1)
  Status: DEPARTS WITHOUT A REASON (prompt 5).
  - Precedent: nyc_taxi_trip_duration_1m takes 3,600 s off its 86 trips across the switch. That was the panel's
    change of 2026-10-20, shipped by Lennart 2026-10-22.
  - The definition's reasons ("we cannot tell which field is wrong"; "the daylight-saving switches do not change it")
    are refuted for 24 trips. 20 of them are kept, all in training.
  - The fix is cheap and safe (principles step 3, quality).

D10. Straight-line speed between centroids not checked (column audit D; CLEAN-11)
  Status: DEPARTS WITHOUT A REASON (prompt 6).
  - Precedents: pkdd's `MAX_STRAIGHT_LINE_KMH` (shipped 2026-10-26) and 2024_lusaka_mobility_prediction_hackathon (19
    trips, Lennart, 2026-11-05: "the duration or the endpoint is wrong").
  - The column audit finds 1,183 kept trips above 120 km/h even with 1 km of slack per tract end and 3 km per area end.

Other calls, consistent:
  - 3 h cut: nyc, pkdd; Lusaka, 2026-11-05.
  - 2,140 copies dropped: nyc's 7 copies; LEAK-19.
  - Fit approximate with the drop-off as the destination: pkdd issue 1 (a), Lennart 2026-10-26; nyc.
  - Domain "industry & manufacturing": Lusaka, "align it", 2026-11-04.
  - No hour or weekday column: CLEAN-2 case, nyc and pkdd, Lennart 2026-10-21. The blind reviewer's ask for explicit
    hour and weekday columns departs from this precedent, not the definition.
  - Random 1M per window: v2 split protocol, as nyc_1m (2026-10-21). The blind reviewer's "6.6x density jump" is
    this design.

**2. REGISTER FLAGS (candidates, read against the cases)**
  - exception_to_must LEAK-10 (loan_default_prediction_imperial_college, Andrej, 2026-11-03): an exception that drops
    more, not a keep. A keep here would be the first LEAK-10 departure in the other direction.
  - drift "post-outcome feature" (Lennart: keep to 2026-11-05, exclude from 2026-11-08): the exclude side is the two
    nfip duplicate CCs, misread by keyword, so it is no drift on this rule. The real later calls (bank_marketing
    2026-11-08, noaa X4 2026-11-08) tighten keeps, as noted under D2.
  - drift "scaling over all rows" (coad 2026-10-16, keeps from 2026-10-19): the LEAK-30 amendment, not drift. It made
    the LEAK-30 keeps the builder cited, whose mechanism this is not.
  - opposite_outcomes USE-8 and LEAK-38 (sendy's "exclude"): a relabel, misread. No pair.
  - opposite_outcomes PROV-6, PROV-4: duplicate cuts of one source. No bearing beyond D7.
  - amendment_due flags (CLEAN-19, MET-1, SPLIT-10, SPLIT-14): none touches these calls. No third exception of one kind
    arises here.

**3. REFLECTION PROMPTS (issue-turn shape; numbering for the REVIEW.md is the main session's)**

Prompt 1 (D2, builder issue 2)

Consistency check: Keep the hidden-tract flag, now measured to depend on the trip's own arrival quarter hour, although every earlier missingness that tracked the outcome was removed?

- **Problem:**
  - The City shows a drop-off tract only when other trips end in it in the trip's own arrival quarter hour, which is the start plus the target[p1-leak10].
  - The flag is worth 0.0016 to 0.0024 RMSLE on all three windows (one seed each), against 0.024 for the shown tract, and only coarsening every trip to its community area removes it.
  - The note files it as a weak all-row step that looks "later that day or month", a mechanism the data rejects, and no earlier keep covers a measured missingness of this kind[p1-leak30].
- **Consistency:** removed on the same portal: chicago_traffic_crashes's five condition fields, whose filled-in flags carried 72% of their 0.0039 log-loss gain (2026-11-04), and `dooring_i` at a cost of 0.00011 (2026-11-05); removed elsewhere: 2_month_survival_rate_prediction's `edu` and `income`, missing more often among deaths (2026-10-26), kick's `WheelType` and expresso_churn_prediction's `REGION` (2026-10-22), santander's `has_*` at +0.003 ROC AUC[p1-leak6]; kept with a note: medical_facility_operational_data, whose late cells cannot be located and whose whole worth sits within about two seed SDs (2026-11-05), and noaa_storm_events_damage's Flash Flood duration, where the outcome draws a minority of the spans and "the size of the worth alone never decides" (2026-11-08)[p1-must].
- **What sets it apart:** the missingness is the City's disclosure control of a field whose shown values carry ten times the flag's worth, and the only remedy gives that up, where the removals above gave up at most a small legitimate part (28% of 0.0039 at chicago_traffic_crashes).
- **Unknown:** the flag's noise over seeds and training samples, the measurement on which medical_facility_operational_data was kept.
- **Options:**

  | | Option | What it does | Pro | Con |
  |---|---|---|---|---|
  | a | Measure, then decide | the flag's worth over 5 seeds and training samples per window; kept with the rewritten note if within about two seed SDs, else (b) | follows the one clause that keeps values set after the prediction point that cannot be located; settles the fact before the rule | one more experiment; the sign agrees on 3 of 3 windows, so (b) may follow |
  | b | Coarsen to community areas | both tracts dropped, the centroids replaced by the area's | removes the reading, as on the same portal; the outside-Chicago rows of the location filter leave with it | costs 0.024 to 0.025 RMSLE of a location the dispatcher knows; a coarser task |
  | c | Keep with the note (implemented) | the note, `fit_reason` and decision table rewritten to the arrival-slot mechanism | keeps the tract's signal; the flag is about 0.6% of the error | a departure from a rule without a weak grade for this mechanism, and no amendment; the first keep of its kind |
  | d | Amend the rule | a source's disclosure control that the outcome draws in part stays with a note giving its worth, when it hides a field that keeps its worth where shown | a deliberate rule for the City and census tables still to come | loosens the rule two days after it was tightened; rests on the remedy's cost |

- **Recommendation:** a, and b if the worth is above noise, unless you want d as a standing rule for disclosure-controlled sources. **Decision:** a, b, c or d?

[p1-leak10]: **LEAK-10** (Must): out, among others, "missingness that encodes the outcome"; fixed the smallest way, else dropped. Its second clause keeps values set after the prediction point that cannot be located row by row only when the part that can be traced shows no gain (onlinenewspopularity, medical_facility_operational_data); its third clause (2026-11-08) covers spans.
[p1-leak30]: **LEAK-30** (Must when strong, Should when weak): the weak grade is for scaling over all rows. **LEAK-38** (Should): fields of a host's own competition whose timing cannot be tested; a conditional test that measures the mechanism sends the field to LEAK-10.
[p1-leak6]: **LEAK-6** (Must): measure before acting; a confirmed leak goes even when small.
[p1-must]: principles.md, Strengths and Exceptions: a Must has no exceptions; only a higher-ranked Must overrides it, anything else is an amendment. **PROV-3**'s keep of disclosure control as published is a P5 rule on real data and does not outrank P4.

Prompt 2 (D1, builder issue 1)

Consistency check: Filter on the community area, as the notes say, rather than on the centroid, whose presence outside Chicago follows the hidden tract?

- **Problem:**
  - The code drops trips without a centroid, while the notes, the decision table and the summary say trips without a pickup or drop-off area.
  - 32,850 kept trips start or end at tract 17031770700 next to O'Hare, outside the city, and stay only when the City shows that tract, while 6,334 trips to 220 other suburban tracts leave though their tract is shown.
  - The siblings' row cuts rest on the inputs, not on the travel time, and the hidden tract reads the travel time[p2-use7].
- **Consistency:** dropping trips with no destination at all follows pkdd_15_taxi_trip_time_prediction_ii_1m (fewer than 2 GPS points); nyc_taxi_trip_duration_1m keeps destinations outside the city because its points record them, which no Chicago column does for the suburbs; a segment the actor faces but the data lacks is named as a selection, as for lt_vehicle_loan_default_prediction (2026-11-05)[p2-use8].
- **Options:**

  | | Option | What it does | Pro | Con |
  |---|---|---|---|---|
  | a | Filter on the community area | trips without an area at either end leave (32,603 more, 0.49%); every kept row has a centroid | one inside-Chicago rule; the area is never suppressed, so no row's presence follows the hidden tract; matches the notes | drops 32,850 trips whose destination tract is known |
  | b | Filter on the centroid (implemented) | trips without a centroid leave | keeps 32,850 trips by O'Hare | their presence follows the hidden-tract flag; the notes describe another rule |
  | c | Keep every trip with a tract or an area | the 6,334 suburban trips stay with the centroid missing | closest to nyc's out-of-city keep | every suburban trip enters only when its tract is shown, a wider selection by the flag |

- **Recommendation:** a, with the dropped O'Hare-to-suburbs segment (7.4% of the raw trips, 22% of O'Hare pickups) named in `fit_reason` as a selection. **Decision:** a, b or c?

[p2-use7]: **USE-7** (Must): a row that lacks the input the prediction acts on is no task row; its Cases row for nyc_taxi_trip_duration_1m and pkdd_15_taxi_trip_time_prediction_ii_1m (2026-10-26): "the cut rests on the inputs, not on the travel time".
[p2-use8]: **USE-8** (Must, amended 2026-10-27): `fit_reason` names a selection, whether or not it makes the fit approximate.

Prompt 3 (D4, builder issue 4)

Consistency check: Keep the short-record cut at 60 s, with the fact that sets it apart from the siblings' 30 s written down in full?

- **Problem:**
  - The cut drops 39,118 records of 30 to 59 s, 19,999 of which record a mile, besides the 28,871 records of exactly 60 s (81% without a mile).
  - The stated reason, that whole-minute systems write a non-ride as 60 s, covers the 28,871 but not the 30 to 59 s band, where the seconds systems run on a smooth slope (38-42% without a mile at 55-59 s, 34-36% at 61-64 s).
  - You moved pkdd from 60 s to 30 s because the longer cut "sat on a smooth slope and also dropped short rides that moved", but there the 100 m rule removed the non-rides, which centroids cannot do here[p3-clean11].
- **Consistency:** pkdd_15_taxi_trip_time_prediction_ii_1m and nyc_taxi_trip_duration_1m cut at 30 s with the 100 m rule (2026-10-26); sendy_logistics_challenge drops legs of 60 s or less on the source's words (2026-11-05).
- **Background:** issue 4's "keeps 68k non-ride-like records" counts every record of 30 to 60 s, of which 42,387 have no mile and 25,598 have one; the column audit finds the kept 61 to 119 s records already hold about 10% of the test squared error.
- **Options:**

  | | Option | What it does | Pro | Con |
  |---|---|---|---|---|
  | a | 60 s or less (implemented), reason completed | the notes add that centroids allow no 100 m rule | follows the reason of the pkdd call: non-rides go where no rule on the inputs removes them | drops about 25,600 records that moved |
  | b | Under 30 s, as the siblings | keeps 30 to 60 s | the siblings' number; keeps every short ride that moved | keeps about 42,400 records without a mile that no other rule removes |
  | c | Under 30 s and exactly 60 s | drops the 60 s default value on top of the siblings' cut | keeps the 19,999 moving records of 30 to 59 s | keeps 19,119 records of 30 to 59 s without a mile |

- **Recommendation:** a, recorded as an exception to the sibling precedent with both facts (the 60 s default value and no rule on the inputs). **Decision:** a, b or c?

[p3-clean11]: **CLEAN-11** (Should): a row leaves only when it is no task row (**USE-7**, Must) or a copy; pkdd's CC of 2026-10-26: "drop the trips that end within 100 m of their start, with a time cut at 30 s".

Prompt 4 (D8, claim audit I5-i)

Consistency check: Keep the trips whose pickup and drop-off share a centroid, and write why the siblings' 100 m rule does not apply?

- **Problem:**
  - 557,128 kept trips (8.35%) share a centroid at both ends: 147,523 in one shown tract and 409,605 in one community area with the tract hidden.
  - They are short rides that moved: 92% record a mile (median 0.59 mile within a tract, 1.03 within an area) and their median is 5 to 7 minutes.
  - The notes neither apply nor mention the siblings' rule, which the record's size check asked to count[p4-use7].
- **Consistency:** nyc_taxi_trip_duration_1m and pkdd_15_taxi_trip_time_prediction_ii_1m (2026-10-26) and 2024_lusaka_mobility_prediction_hackathon (2026-11-04, on the source's straight line from unmasked points) drop ends within 100 m; sendy_logistics_challenge (shipped 2026-11-05) keeps two orders 89 to 90 m apart because "the 100 m radius of nyc, pkdd and Lusaka rests on exact coordinates".
- **Options:**

  | | Option | What it does | Pro | Con |
  |---|---|---|---|---|
  | a | Keep, with the reason | a note and a decision row (trips by shown and hidden tract, minutes, miles) | follows sendy; keeps real short rides | 42,433 same-centroid trips record no mile, some of them returns to the start |
  | b | Keep without a note (implemented) | nothing changes | none found | a silent departure from three siblings |
  | c | Drop same-centroid trips under 0.1 meter mile | 57,094 trips (0.86%), the nearest stand-in the column audit found | removes most returns to the start | rests on a column known only after the trip; some systems record no miles on a quarter of their 5 to 60 min trips |
  | d | Drop every same-centroid trip | 557,128 trips leave | the siblings' wording | drops about 515,000 rides that moved; same-tract trips leave only when shown, a selection by the hidden-tract flag |

- **Recommendation:** a. **Decision:** a, b, c or d?

[p4-use7]: **USE-7** (Must), Cases row nyc_taxi_trip_duration_1m and pkdd_15_taxi_trip_time_prediction_ii_1m (2026-10-26): an end within 100 m of the start is no destination anyone names.

Prompt 5 (D9, claim audit C14 and C28, column audit C)

Consistency check: Take the skipped hour off the spring-forward trips, as nyc_taxi_trip_duration_1m does?

- **Problem:**
  - 24 trips that start in the 03:00 slot of 2026-03-08 record a trip_seconds one hour too long (median 2.8 mph as recorded, 17.9 mph without the hour), and 20 of them are kept, all in training.
  - The notes say "we cannot tell which field is wrong" and that the daylight-saving switches do not change the target, both refuted for these trips by the claim and column audits.
  - nyc_taxi_trip_duration_1m takes 3,600 s off its 86 trips across the switch, a fix you shipped on 2026-10-22[p5-clean].
- **Options:**

  | | Option | What it does | Pro | Con |
  |---|---|---|---|---|
  | a | Subtract 3,600 s before the duration filters, as nyc | trips starting 2026-03-08 03:00 whose trip_seconds exceed end minus start by more than 3,000 s, guarded at 24 | the precedent; the target becomes the ride's duration | a rule for one night of one year |
  | b | Keep (implemented) | the rows unchanged, both notes rewritten | no score moves (20 training rows of 6.67M) | 20 wrong targets kept although a repair is known |
  | c | Set the 20 targets missing | the rows leave, guarded at 20 | simple | drops rides whose duration can be repaired |

- **Recommendation:** a. **Decision:** a, b or c?

[p5-clean]: **CLEAN-1** (Should): clean to the state an expert would ship; principles.md, How to decide, step 3: a quality problem is fixed when the fix is cheap and safe; **USE-5**: the target is the real-world quantity.

Prompt 6 (D10, column audit D)

Consistency check: Drop the trips whose centroids lie too far apart for their duration, as pkdd and Lusaka drop straight lines faster than 120 km/h?

- **Problem:**
  - 1,183 kept trips need more than 120 km/h between their centroids even with 1 km of slack per tract end and 3 km per area end (median 169 s, most with an O'Hare end).
  - The meter's time and miles agree on a short ride there, so the end point or the duration is wrong.
  - The notes do not mention the siblings' rule[p6-clean11].
- **Consistency:** pkdd_15_taxi_trip_time_prediction_ii_1m drops straight lines faster than 120 km/h (shipped 2026-10-26); 2024_lusaka_mobility_prediction_hackathon dropped 19 such trips because "the duration or the endpoint is wrong" (2026-11-05).
- **Options:**

  | | Option | What it does | Pro | Con |
  |---|---|---|---|---|
  | a | Add the filter with the slack stated | 1,183 trips leave (13 to 15 per test week) | the siblings' rule, adapted to centroids | the slack is a choice of ours |
  | b | Keep them (implemented) | nothing changes; a note says why | none found beyond the coarse centroids, which the slack already allows for | a silent departure; 0.4 to 0.7% of the test squared error on impossible trips |

- **Recommendation:** a. **Decision:** a or b?

[p6-clean11]: **CLEAN-11** (Should): impossible values become missing and the row stays, unless it is no task row; the Lusaka CC of 2026-11-05 dropped its 19 trips under CLEAN-11, then CLEAN-15, as pkdd's `MAX_STRAIGHT_LINE_KMH`.

</details>

<details><summary>Advocate</summary>

ADVOCATE, OPENING BRIEF: chicago_taxi_trip_duration (folder chicago_taxi_trip_duration_1m), 2026-11-09

Position: ship. Nothing the panel found is a reason to exclude. One validity problem (the hidden-tract flag, LEAK-10)
must be measured or fixed, and either way the dataset ships. Every other finding is fixed by a sibling precedent or a
note and needs no decision.

Verdict: ship after changes.
Validity: SEL-1, SEL-2 hold; USE-1 holds (approximate, named); USE-7 holds once the location filter reads the
  community area, as the notes already say; LEAK-10 holds for the 8 dropped post-trip columns and is triggered (weak,
  measured) by the hidden-tract flag: measure, else coarsen; LEAK-9 (evaluation leak): protocol line; SPLIT-1,
  SPLIT-10, SPLIT-14, SPLIT-20, LEAK-24 hold (late reports measured: none); PROV-7, PROV-9 hold.
Value: TP-2, TP-3 hold (skill 0.707); MET-11 context rmsle, backed by a measurement on this data.
Quality: the DST and 120 km/h fixes follow nyc, pkdd and Lusaka; notes corrected.

1. Nothing found is a reason to withhold the dataset.
   Evidence. Every evidence agent's verdict is ship or include: claim audit "ship after changes ... None of them blocks
   the task"; column audit "ship after changes"; split audit "right with notes ... No problem needs a re-split";
   domain practitioner "as a benchmark of learners on a coarsened real task, yes"; blind reviewer "include with
   changes ... It is a real use"; task gamer "can only be gamed a little".
   - Every post-trip column is dropped (probe 20: fare R^2 0.80, trip_miles 0.75, trip_total 0.72), and no remaining
     feature is recorded after pickup (column audit, all 11).
   - No row is copied across the split (0 / 0 / 0). The gap holds: 0 train trips end after a window start.
   - The late-report doubt is settled by measurement: later monthly updates added +84, +60 and +94 trips to months
     already published (at most 0.016%) (split audit). The September windows score inside the April-August range.
   - Worth: LightGBM 0.422 against a dummy of 0.780 (skill 0.707, SE 0.009), 0.245 over linear.
   Rules: SEL-2, USE-1 (Must), USE-8 (approximate, named), SPLIT-1, SPLIT-10, LEAK-24, TP-2, TP-3.
   Why it wins: the tension "a real task against a leak" says fix the leak and keep the task; exclusion, the last
   rung of the remedy ladder, is for a Must that cannot be fixed. Every finding below has a fix.

2. The hidden-tract flag. I concede the mechanism. The dataset ships under either remedy.
   Conceded. The City's suppression counts the drop-off tract in the trip's own end slot, which is start + target:
   - own end-slot coefficient -0.198 (SE 0.003) against +0.006 to +0.014 for the neighbouring slots (column audit A);
   - a shown drop-off is alone by its end slot in 1.2% of trips, by its start slot in 5.4%; the null on community
     areas shows no such difference (claim audit C7).
   That is LEAK-10's "missingness that encodes the outcome" (Must, no weak grade), not LEAK-30. The note's "may look
   past the pickup ... later that day or month", the fit_reason, decision table 5 and the "LEAK-30-like" label are
   wrong and get rewritten whatever the call.
   What bounds it. The whole flag is worth 0.0019 / 0.0016 / 0.0024 RMSLE (builder) or 0.003 (gamer), about 0.6% of
   the error, and that is an upper bound on the leak: most of the flag is geography. In the same cell, hidden trips run
   +0.066 log miles against -0.027 for shown ones, and within O'Hare cells the hidden trips' mean moves only -0.009 and
   -0.002 log. The shown tract carries 0.024-0.025, ten times the flag.
   The mildest remedy the rules allow:
   (a) First, the decisive measurement (EV-1, Must): the flag's worth over 5 seeds and training samples per window.
       Keep it with the rewritten note only if the worth sits within about two seed SDs, as for
       medical_facility_operational_data (LEAK-10's second clause by analogy). I do not hide the risk: the gamer's
       noise band (per-split moves up to 0.0007) makes the whole-flag upper bound likely to fail unless the end-slot
       part is isolated from the geography.
   (b) Otherwise, coarsen every trip to its community area. This is LEAK-7's smallest fix that removes the leak: the
       hiding is joint, so nothing smaller works. The task still scores 0.39 against a dummy of 0.78, well worth
       benchmarking, and the O'Hare-tract rows of point 6 leave with it.
   Keeping the flag without (a) passing would be an amendment (precedent checker's d), not an exception. A Must has no
   exceptions, and no higher-ranked Must is at stake (PROV-3 is P5).
   Why it outranks "do not ship": LEAK-27's exclusion covers a leak that cannot be undone. This one is undone in the
   definition.

3. The same taxi's next pickup among the test rows is an evaluation leak. It is fixed by a protocol line, not in the
   data.
   Evidence. 97.8% of the newest week's test trips have a later pickup of the same taxi in the week. Reading it is worth
   0.0053 (gamer, in protocol) to 0.007-0.008 (column audit), and only to a method that reads other test rows. A
   deployed model never has it, and row-wise models cannot use it (blind reviewer).
   Rule. LEAK-9 (Should, amended 2026-11-05): when "a model can read other test rows", the leak is fixed "by a protocol
   line the benchmark checks, not in the data". Cases: medical_facility_operational_data,
   azure_vm_lifetime_resource_central_1m, fremtpl2, bank_marketing.
   Why the gamer's data fixes lose:
   - Hiding taxi_id in test rows removes, from the test only, a feature known at pickup (USE-10, LEAK-34, both Must),
     and breaks the train-test match.
   - Thinning the test windows throws away test rows that the v2 protocol keeps (119k-127k, under the 500k cap).
   The protocol line plus a `Potential leak, kept on purpose (LEAK-9)` bullet with these numbers is the rule's own
   remedy and needs no decision. pkdd's same channel goes into pkdd's own REVIEW.md (Lennart, 2026-11-08: a per-dataset
   choice is a per-dataset issue).

4. rmsle from context is the right metric, and the data shows it.
   Evidence. The City defines no metric (portal metadata). Both sibling competitions scored RMSLE on this task (Kaggle
   NYC 2017; ECML/PKDD 2015, confirmed by BlueTaxi). The same context call was made for sf_permit_time (a City
   register), brazilian_ecommerce and video_transcoding_time_prediction. On this data:
   - trips over 1 h (3.8-4.8% of the test trips) hold 38-45% of the squared error in seconds;
   - RMSLE and RMSE rank two LightGBM fits in opposite order on 3 of 3 folds (claim audit);
   - RMSLE, MAE, MAPE and the share within +/-25% all put the seconds-L2 model last, and RMSE alone puts it first
     (domain practitioner).
   Rules: MET-11 (Must) `context`. MET-10 (Weigh): diversity decides only in doubt, and if invoked the practitioner's
   choice is mae in seconds, not rmse.
   Changes with no decision: lead the reason with this dataset's measurement rather than the siblings' (MET-10: one
   metric per dataset, not per family); align the record's screening Metric line and its year 2016 (PROV-9: 2026, as
   chicago_traffic_crashes).

5. taxi_id and the 1M sample are consistent with the rules and measured.
   taxi_id:
   - known at pickup; 99.88 / 99.93 / 99.98% of the test trips are by a taxi seen in training, with a median of 430
     training trips per test taxi;
   - pkdd ships it as a feature (Lennart, 2026-10-26). Rules: USE-10 (Must), LEAK-34 (Must), SPLIT-13 (split audit:
     holds);
   - shared reporting ids (column audit F) need one note line only.
   The sample:
   - each train side is a random 1M, 15.2-16.0% of every full month;
   - the newest 1M would score 0.002-0.005 better but would drop the season of the year before (SPLIT-20, Should: "at
     least one full season"), and SPLIT-21 (Must) forbids choosing the history from three test windows;
   - it is the nyc_taxi_trip_duration_1m precedent and the v2 split protocol. The blind reviewer's "6.6x density
     jump" is this protocol (the test windows keep every trip), not an artefact of the preparation.
   The blind reviewer's ask for hour and weekday columns departs from CLEAN-2 (Must) and its nyc/pkdd case (Lennart,
   2026-10-21). The gamer's "density mismatch" costs honest previous-trip features 0.0008 (0.35371 against 0.35296),
   about one noise band, and SPLIT-21 again bars redesigning the train side from it.

6. The row cuts: keep 60 s, write why the 100 m rule cannot apply, and make the location filter read the area, as the
   notes already say.
   60 s against 2 min. CLEAN-11 (Should) drops a row only when it is no task row (USE-7) or a copy.
   - 71-73% of the 61-89 s records and 85-86% of the 90-119 s records log a mile: most are rides.
   - The siblings' USE-7 case says "the cut rests on the inputs, not on the travel time". Lennart moved pkdd from 60 s
     to 30 s because the longer cut "sat on a smooth slope and also dropped short rides that moved"; a 2-minute cut on
     the target goes further the wrong way.
   - That 0.6% of the rows hold 10% of the test squared error says they are hard, not that they are no task rows.
   - "No mile" is no clean non-ride marker: TAC Yellow records no mile on 25% of its 5-60 min trips.
   Change with no decision: complete the reason (the 60 s default value, and no rule on the inputs can remove
   non-rides here; precedent checker's prompt 3 (a)), and state the 61-119 s weight (domain practitioner: (a)
   acceptable if the note states it). Also correct the sentence on whole-minute systems to "as 0 s or 60 s" (C19).
   100 m rule. Centroids cannot locate a return to the start. 92% of the 557,128 same-centroid trips log a mile
   (median 0.59 mile within a tract, 1.03 within an area; 5-7 min). sendy_logistics_challenge (shipped 2026-11-05)
   kept sub-100 m pairs because "the 100 m radius of nyc, pkdd and Lusaka rests on exact coordinates". A note and a
   decision row, no row change.
   Location filter. Conceded. The code reads the centroid: 32,850 trips at tract 17031770700, outside the city, stay
   only when that tract is shown, and 6,334 shown suburban trips leave. Filter on the community area, which is what the
   notes, `changes` and decision 4 already say: 32,603 more rows (0.49%) leave, and a row's presence no longer follows
   the flag. That is USE-7 (Must) as the definition states it. Name the in-city selection (7.4% of the raw trips, 22%
   of O'Hare pickups) in fit_reason and `row` (USE-8, Must, amended 2026-10-27). Under point 2 (b) the same rows leave
   anyway.

7. The two quality slips are fixed cheaply with the siblings' own rules.
   - DST: 20 kept trips that start 2026-03-08 03:00 carry the skipped hour (2.8 mph as recorded, 17.9 mph without it),
     all in training. Subtract 3,600 s, as nyc_taxi_trip_duration_1m does (shipped 2026-10-22), and rewrite the two
     refuted bullets ("cannot tell which field is wrong", "the switches do not change it").
   - Speed: 1,183 trips need over 120 km/h between centroids even with 1 km of slack per tract end and 3 km per area
     end (13-15 per test week, 0.4-0.7% of the test squared error). Drop them, as pkdd's MAX_STRAIGHT_LINE_KMH and
     Lusaka (2026-11-05) do, with the slack stated.
   Rules: CLEAN-1 (Should), CLEAN-11 and CLEAN-15, principles step 3 (a quality problem is fixed when cheap and safe),
   "treat like cases alike".
   Why they do not touch shipping: a P7 problem "makes the benchmark a little worse", and step 4 says independent
   failures are not conflicts. None of these breaks a Must.
   Other note fixes, no decision: replace the late-report note with the split audit's three snapshot comparisons; say
   that the 82,914 trips with neither area come mostly from three reporting systems; fix claims.md item 32's order and
   the builder's "Features (10)" (11).

Sources: the seven phase-A reports and builder_report.md in this run; dataset.py of chicago_taxi_trip_duration_1m
(df-large); principles.md, leak_checks.md (LEAK-6, 7, 9, 10, 30, 34, 38), use_case.md (USE-7, 8),
cleaning_features.md (CLEAN-1, 2, 11, 15), splits.md (SPLIT-20, 21), metrics.md (MET-10, 11).

</details>

<details><summary>Advocate rebuttal</summary>

ADVOCATE, REBUTTAL: chicago_taxi_trip_duration (folder chicago_taxi_trip_duration_1m), 2026-11-09

We agree on the verdict (ship after changes) and on six of the critic's seven points. The one dispute left is the
2-minute cut (point 4). Point 2 is conceded in full: the test my brief asked for has been run, and the flag failed it.

1. Location filter (USE-7, USE-8): conceded, as in my point 6. Filter on the community area at both ends (32,603 more
   trips leave), name the in-city selection in fit_reason and `row`, and add the second cause of blanks (three
   reporting systems) to the notes. Under the coarsening of point 2 these rows leave anyway.

2. The hidden-tract flag (LEAK-10, LEAK-6, both Must): conceded. The critic ran the test my brief named first (EV-1),
   and the flag fails it.
   - Its measurement (flag_noise_summary.txt): over 5 seeds with a random 700k of each train side, the flag
     gains 0.0034 / 0.0039 / 0.0028 RMSLE. The smallest single gain is 0.0015, and all 15 of 15 fits gain.
   - A precision, not a dispute: the critic divides by the SD of one score. The fairer yardstick is the SD of the
     paired gain, which is 0.0006 to 0.0008. On that yardstick the gain is still 3.6 to 6.6 SDs, far beyond the "about
     two seed SDs" on which medical_facility_operational_data was kept.
   What follows:
   - The one route that keeps a value set after the prediction point is closed. The end-slot part cannot be located row
     by row, so LEAK-10's second clause sends the values out once they may carry a gain
     (distribution_transformers_at_cauca_department).
   - My remaining argument, that most of the flag is geography, is the argument this clause rejects, and "the size of
     the worth alone never decides" (X4).
   - The remedy is (b): coarsen every trip to its community area. Drop both tract columns and set both centroids to the
     area's.
   - This costs 0.024-0.025 RMSLE. The task still scores 0.38-0.39 against dummies of 0.76-0.79, so it stays worth
     benchmarking (TP-2).
   - fit_reason then names the coarsened location instead of a kept leak.
   I do not argue the amendment (d). The curator tightened LEAK-10 calls in this direction on 2026-10-26 and
   2026-11-08 (2_month_survival, bank_marketing), and this would be the first kept missingness that reads the outcome.
   The facts for (d), if the curator wants it as a standing rule, are in the record: the shown tract is worth ten times
   the flag, and the hiding is the City's disclosure control.

3. Next pickup among the test rows (LEAK-9): agreed. The protocol line and the `Potential leak, kept on purpose
   (LEAK-9)` bullet are the remedy, and pkdd gets its own REVIEW.md issue. I accept the gamer's data-side fixes only as
   the critic frames them, a fallback if the benchmark cannot check the line. LEAK-9 puts the fix "not in the data".

4. The short end: partly disputed.
   Conceded:
   - Write the 60 s reason in full: whole-minute systems write non-rides as 0 s or 60 s, and no rule on the inputs can
     remove non-rides with centroids.
   - Write the 61-119 s weight.
   - Write the same-centroid counts as the fact that sets this case apart from the siblings' 100 m rule. These are note
     changes.
   Disputed, the 2-minute cut on the target:
   - About 80% of the 61-119 s band logs a mile on the meter (no mile on 0.11-0.14% of the test rows, out of the band's
     0.59-0.63%). So a 2-minute cut drops about 33,000 records that moved.
   - That is what Lennart moved pkdd off when he went from 60 s to 30 s: the longer cut "also dropped short rides that
     moved" (USE-7 Cases, 2026-10-26).
   - CLEAN-11 (Should) drops a row only when it is no task row, and a short ride that moved is a task row. That 0.6% of
     the rows hold 10% of the squared error says they are hard under RMSLE, a metric both sides accept. It does not
     say they are no task rows.
   - The critic's "a model's rank can turn on how it treats meter on/off records" is not measured. The one measurement
     points the other way: trained and tested with the 2-minute cut, a model scores 0.336 on the same rows that score
     0.338 when it is trained with them (domain practitioner). The band barely changes the fit on the other rows.
   The narrower rule, under 2 minutes with no mile (0.11-0.14% of the test rows, 2.3-2.8% of the squared error):
   - I do not oppose it as the curator's call. It applies the definition's own non-ride marker, as the critic says.
   - But it is not a clean marker. Transit Administrative Center and TAC Yellow log no mile on many real rides (TAC
     Yellow on 25% of its 5-60 min trips) and supply about a third of the column audit's no-mile marker, so the rule
     selects by reporting system.
   - It is a P3 weighing call under USE-7, not a breach. The 60 s cut as built satisfies USE-7 without it.

5. The 20 DST targets: conceded. Subtract 3,600 s as nyc does, guarded at 24, and rewrite both notes.

6. The 1,183 trips over 120 km/h: conceded. Add the filter with the stated slack, as pkdd and Lusaka do (CLEAN-11,
   then CLEAN-15).

7. Refuted or outdated notes: conceded, the same list as my points 4 and 7. Replace the late-report note with the split
   audit's measurement, lead the metric reason with this dataset's measurement, and fix the record's year and Metric
   line.

The case after rebuttal:
Verdict: ship after changes.
Validity:
- USE-7 holds with the area filter.
- USE-8: name the in-city selection and the coarsened location.
- LEAK-10 triggered, fixed by coarsening to community areas (the seed-noise test closed the keep).
- LEAK-9 triggered, fixed by a protocol line.
- SPLIT-1, SPLIT-10, SPLIT-20 and LEAK-24 hold.
Value: TP-2 holds (0.38-0.39 against 0.76-0.79); MET-11 rmsle from context.
Quality: DST repaired; impossible speeds dropped; the 60 s cut kept with its full reason.
For the curator: the no-mile rule under 2 minutes, a weighing call; LEAK-10 amendment (d) only as a deliberate
standing rule.

</details>

<details><summary>Critic</summary>

CRITIC, OPENING BRIEF: chicago_taxi_trip_duration (folder chicago_taxi_trip_duration_1m), 2026-11-09

Position: ship only after changes. The task is real (a pickup-time ETA, as nyc and pkdd) and I do not argue to
exclude it. But as defined it carries one measured Must breach (the hidden-tract flag reads the trip's own arrival
slot), a row filter whose presence test follows that flag, an unnamed selection, an unguarded evaluation leak, and
four cheap repairs the siblings already made. None needs exclusion; one needs a coarser location.

Verdict: ship after changes.
Validity: USE-7 / USE-8 triggered (filter on the centroid, selection not named: point 1); LEAK-10 triggered, not
  fixable by a note (point 2); LEAK-9 triggered, protocol line missing (point 3); USE-7 weighing on the short end
  (point 4). SPLIT-1, SPLIT-10, SPLIT-14, SPLIT-20 hold (split audit). LEAK-24 settled (split audit).
Value: TP holds; rmsle from context holds (conceded).
Quality: CLEAN-1 / USE-5 (20 DST targets, point 5); CLEAN-11 (1,183 impossible speeds, point 6); refuted notes (point 7).

New evidence of my own (flag_noise.py, flag_noise_seed0-4.json, flag_noise_summary.txt): the worth of
the hidden flag over seeds and training samples, the measurement the precedent checker said was missing.

1. The location filter reads the centroid, not the area, and the selection it makes is not named
   (P3; USE-7 Must with its Cases row, USE-8 Must amended 2026-10-27)
   Problem. row_filters drops trips without a centroid. The notes, decision 4 and `changes` say "without a pickup or
   drop-off area (outside Chicago)". The two differ:
   - 32,850 kept trips (31,945 drop-offs, 905 pickups; 0.49% of kept rows) end or start at tract 17031770700, outside
     the city by O'Hare. They have no community area and stay only because the City showed that tract; hidden, they
     would have no centroid and leave. So their presence follows the flag of point 2, which reads the arrival slot.
   - 6,334 trips to 220 other suburban tracts are dropped although their tract is shown (precedent checker,
     p1_location.txt).
   - The dropped segment is not named in fit_reason or `row`: 7.4% of raw trips, 22% of O'Hare pickups (292k of
     1,326,053), 11.2% of rides over 45 minutes (domain practitioner). The actor quotes these trips every day.
   - The 82,914 trips with neither area are mostly not out-of-city: median 4.9 miles, concentrated in three
     reporting systems (Chicago City Taxi Association loses 18.8% of its rides). The notes give only "outside Chicago".
   Effect. A test row's presence for the O'Hare-adjacent segment depends on when it ended; the benchmark reads as a
   whole-city ETA while it covers only trips with both ends in the city.
   Rule. USE-7's Cases row (nyc, pkdd; Lennart 2026-10-26): "the cut rests on the inputs, not on the travel time".
   USE-8 (Must): fit_reason names a selection whether or not it changes the fit (lt_vehicle_loan_default_prediction).
   Remedy (fix the definition, mildest). Filter on the community area at both ends (32,603 more trips leave; every
   kept row then has a centroid). Name the in-city selection with its shares in fit_reason and `row`. Correct the
   location bullet and decision 4 (centroid vs area; the second cause of blanks). Under point 2's coarsening these
   rows leave anyway.

2. The hidden-tract flag is missingness drawn in part by the outcome, and the note cannot keep it
   (P4; LEAK-10 Must, LEAK-6 Must; LEAK-30 does not apply)
   Problem. The City hides both tracts unless the drop-off tract has other trips in the trip's own END quarter hour,
   which is start + target. fit_reason and the note file it as a rule that "may look past the pickup" over "the same
   tract pair later that day or month", a weak LEAK-30-like step. The data rejects that mechanism and shows a direct
   one:
   - claim audit C7: among shown tracts the drop-off is alone in its end slot for 1.2% of trips against 5.4% in its
     start slot; on community areas (never hidden) the two keys give the same share (6.68% vs 6.75%);
   - column audit A: within (pickup area, drop-off area, start slot) cells, the hidden indicator regresses on the
     count of other trips ending in the drop-off area in the trip's own end slot at -0.198 (SE 0.003); the slots 15
     and 30 minutes either side give +0.006 to +0.014;
   - the four centroid columns repeat the flag (they jump to the area's centroid), and the hiding is joint, so no
     column drop short of coarsening removes it (LEAK-7: nothing smaller works).
   Size, over noise (my measurement). Community areas only (centroids coarsened, the gamer's honest extras) against
   the same plus the flag; 5 seeds, each a random 700k of the 1M train side, bagging 0.8:
     window (newest first)   flag's worth (RMSLE)   seed SD of the score   worth / SD   fits with a gain
     2026-09-24              0.0034                 0.0003                 12.8         5 of 5
     2026-09-17              0.0039                 0.0005                  8.5         5 of 5
     2026-09-10              0.0028                 0.0007                  4.1         5 of 5 (min 0.0015)
   The builder's one-seed 0.0016-0.0024 and the gamer's 0.003 agree. The whole worth is 4 to 13 seed SDs, so the one
   route that keeps a value set after the prediction point (medical_facility_operational_data: the whole-field worth,
   an upper bound on the late part, within about two seed SDs) is closed. The outcome part cannot be located row by
   row, and LEAK-10's second clause then says the values go when they may carry a gain
   (distribution_transformers_at_cauca_department).
   Effect. A model learns a disclosure process that the City runs on arrival times; a dispatcher never sees the
   flag (domain practitioner: "in my world the tract is never hidden"). The benchmark rewards reading it.
   Rule. LEAK-10 (Must) lists "missingness that encodes the outcome" with no weak grade; LEAK-6 (Must): "a confirmed
   leak goes even when small". LEAK-30's weak grade is for scaling over all rows. The third clause (spans, noaa X4)
   does not cover a flag, and X4 says "the size of the worth alone never decides". Precedents removed smaller
   outcome-linked missingness or recording: chicago_traffic_crashes on the same portal (filled-in flags, 72% of
   0.0039; `dooring_i` at 0.00011), santander `has_*` (+0.003 AUC), kick `WheelType`, expresso `REGION`,
   2_month_survival `edu`/`income`, bank_marketing `campaign` (0.0013-0.0016 AUC, dropped 2026-11-08). The
   tension row "a real task against a leak": fix the leak and keep the task. A Must has no exceptions.
   Remedy (fix the definition). Coarsen every trip to its community area: drop both tract columns, set both
   centroids to the area's. Cost 0.024-0.025 RMSLE of real location detail; the task stays well worth benchmarking
   (LightGBM 0.38-0.39 against the dummy's 0.76-0.79; gamer, no tract information: 0.381). Keeping the tracts needs a
   deliberate amendment of LEAK-10 by the curator for disclosure-controlled sources (precedent checker option d),
   not a `Potential leak, kept on purpose` note. Under either, rewrite the note, fit_reason and decision 5 to the
   end-slot mechanism.

3. The same taxi's next pickup sits among the test rows, and no protocol line guards it
   (P4; LEAK-9 Should, amended 2026-11-05)
   Problem. Each test week keeps all its trips with taxi_id and the quarter-hour start. A trip ends before the same
   cab's next pickup: 98% of test trips have one in the window, median gap 45 minutes, Spearman 0.50 with the
   duration where the gap is under 2 h. That value does not exist at pickup.
   Evidence. Task gamer, in protocol (passes only split rows): 0.35296 to 0.34770, a gain of 0.0051-0.0056 per split
   against noise of at most 0.0007 (about 7x); ceiling about 0.009. Column audit: 0.007-0.008 with a full week of
   training chains. The chain is worth 1.5 to 3 times the hidden flag (point 2), and more than taxi_id's own legitimate
   worth (+0.0018 / +0.0016 / -0.0008).
   Effect. A transductive pipeline wins by reading tomorrow's dispatch log, not by estimating a ride.
   Rule. LEAK-9: an evaluation leak where a model can read other test rows is fixed by a protocol line the benchmark
   checks, not in the data; precedents medical_facility_operational_data, azure_vm_lifetime_resource_central_1m,
   fremtpl2, bank_marketing.
   Remedy (fix the definition: text). A protocol line in splits_comment ("each test trip is predicted from the
   training rows and its own features; no feature or model step may read other test rows") and a `Potential leak,
   kept on purpose (LEAK-9)` bullet with these numbers. pkdd_15 has the same channel with exact starts and no line:
   its own REVIEW.md issue (per-dataset rule, Lennart 2026-11-08). Only if the benchmark cannot check the line:
   the gamer's data-side fixes (unlinkable taxi_id in test rows, or test windows thinned to the training density)
   are the curator's fallback.

4. The short end: the 60 s reason covers part of the cut, the 61-119 s band left in weighs 17x its share, and the
   siblings' 100 m rule is departed from in silence
   (P3; USE-7 Must applied as a weighing call; CLEAN-11 Should; precedent consistency). Placed after the P4 points
   because the USE-7 reading here is a judgment, not a measured breach.
   Evidence.
   - 61-119 s: 41,665 kept trips, 0.6% of test rows, 10.0-10.7% of the test squared error; RMSLE 0.367 becomes 0.348
     without them (column audit E). Newest window: 744 trips carry 10.6% (domain practitioner). 27% / 14% record no
     mile and 76% / 66% the same centroid at both ends, against 2.3% / 5.4% for 5-60 min trips: the definition's own
     non-ride marker.
   - Under 2 min with no mile: 0.11-0.14% of test rows, 2.3-2.8% of the squared error.
   - The stated 60 s reason ("whole-minute systems write a non-ride as 60 s") covers the 28,871 records at 60 s; the
     whole-minute systems write most non-rides as 0 s (80,861), and the 30-59 s band (19,999 of 39,118 with a mile)
     sits on the smooth slope pkdd was moved off (claim audit C19; precedent checker D4).
   - 557,128 kept trips (8.35%) share a centroid; 92% record a mile (median 5-7 min), so they are mostly real short
     rides, and the 100 m rule cannot be applied to centroids. Neither fact is written; the record's size check
     asked for the count.
   Effect. Under RMSLE a model's rank can turn on how it treats meter on/off records, not on ETA skill.
   Rule. USE-7: a row without a destination anyone names is no task row (nyc, pkdd 100 m, 2026-10-26); CLEAN-11.
   Remedy (fix the definition, mildest). Drop records under 2 minutes with no mile on the meter (trip_miles used for
   cleaning only, as the 60 s cut uses the target); or the 2-minute cut (domain practitioner's preference), the
   curator's call. Write the 60 s reason in full (0 s and 60 s defaults; no rule on the inputs is possible with
   centroids) and the same-centroid counts as the fact that sets this case apart from the siblings, recorded as an
   exception.

5. Twenty kept targets are one hour too long, and two notes say otherwise (P7; CLEAN-1 Should, USE-5)
   Evidence. All 45 "anomalies" fall on 2026-03-08. 24 start in the 03:00 slot with trip_seconds one hour too long
   (median 2.8 mph as recorded, 17.9 mph without the hour; March night trips run at 26 mph); 20 are kept, all in
   training. "We cannot tell which field is wrong" and "the daylight-saving switches do not change it" are refuted
   (claim audit C14, C28; column audit C).
   Rule. nyc_taxi_trip_duration_1m takes 3,600 s off its 86 trips across the switch (shipped 2026-10-22). Principles,
   step 3: a quality problem is fixed when the fix is cheap and safe.
   Remedy (repair). Subtract 3,600 s from trips starting 2026-03-08 03:00 whose trip_seconds exceed end minus start
   by more than 3,000 s, guarded at 24, before the duration filters; rewrite both notes. No score moves.

6. 1,183 kept trips are impossible in a straight line (P7; CLEAN-11 Should, then CLEAN-15)
   Evidence. Over 120 km/h between the centroids even with 1 km of slack per tract end and 3 km per area end; median
   169 s and 0.45 meter mile, mostly with an O'Hare end (137 s, 1.67 mi, Near South Side to O'Hare 27 km away).
   13-15 per test week, 0.4-0.7% of the test squared error (column audit D; blind review found the same class).
   Rule. pkdd's MAX_STRAIGHT_LINE_KMH (shipped 2026-10-26) and 2024_lusaka_mobility_prediction_hackathon (19 trips,
   "the duration or the endpoint is wrong", 2026-11-05). Not mentioned here.
   Remedy (fix the definition). Add the filter with the slack stated, or one sentence on why not.

7. Notes refuted or out of date (procedure; writing, EV-2)
   - Late reports: replace "a second download ... would settle it" with the split audit's measurement (later monthly
     updates added +84, +60 and +94 trips to published spans; the newest week is as complete as a later read).
   - The hidden-tract mechanism (point 2), the location wording (point 1), the 60 s reason (point 4), DST (point 5).
   - Metric reason: lead with this dataset's own measurement (trips over 1 h, 3.8-4.8% of test trips, hold 38-45% of
     the squared error in seconds; the two metrics rank two fits in opposite order on 3 of 3 folds; MET-10), not
     with the siblings' competitions.
   - Record: year 2016 and the screening's Metric line (fallback rmse) disagree with the definition.

Not argued (conceded or dropped for want of evidence)
- rmsle from context: the claim audit and the domain practitioner back it on the data (MET-11).
- taxi_id as a feature: known at pickup, USE-10, pkdd precedent; its risk is point 3, fixed by the protocol line.
- The random 1M per window, uniform over the year: matches the use case's "past year", nyc precedent, the v2
  protocol; the newest-1M alternative gains 0.002-0.005, and SPLIT-21 bars choosing history by the test windows.
  The blind reviewer's "6.6x density jump" is this design.
- The split (three weekly windows, one-day gap, a year of history), the 3 h cut, the company spellings, the year
  2026, hour and weekday columns (CLEAN-2 precedent).

</details>

<details><summary>Critic rebuttal</summary>

CRITIC, REBUTTAL: chicago_taxi_trip_duration (folder chicago_taxi_trip_duration_1m), 2026-11-09

We agree on the verdict (ship after changes) and on most remedies. Two disputes are left: point 2, where my
measurement settles the advocate's option (a), and point 6, where I narrow my request and keep it. One new fact,
measured in reply to point 6 (short_end.py, short_end.txt).

A1 (nothing is a reason to withhold). Conceded. I never argued exclusion. But the changes in points 2 and 6 are
   conditions, not options: a measured Must breach does not ship with a note (principles, Strengths).

A2 (hidden flag: measure, else coarsen). Conceded as a frame. The measurement is done, and under the advocate's own
   test it fails. Over 5 seeds and 5 training samples per window (each a random 700k), the flag is worth 0.0034 /
   0.0039 / 0.0028 RMSLE against a seed SD of 0.0003-0.0007: 4 to 13 SDs, a gain in 15 of 15 fits. The advocate
   hopes the end-slot part could be isolated from the geography, but no rule offers that route. LEAK-10's second
   clause keeps values that cannot be located row by row only when the traceable part shows no gain, and then the
   values "go when they may carry a gain". The end-slot rows cannot be located (column audit A finds the mechanism
   only per cell), so the whole-field worth is the bound, as it was for medical_facility_operational_data. That
   bound is not within noise. So (b): coarsen to community areas. The only way to keep the tracts is the curator's
   amendment (d), which the advocate also names. Rule: LEAK-10, LEAK-6 (Must).

A3 (next pickup: protocol line; hiding taxi_id breaks USE-10/LEAK-34). Conceded, and I withdraw my fallback.
   USE-10 and LEAK-34 (both Must) make a known taxi's history a legitimate input. Blanking taxi_id in the test rows
   only would take that input from the test side alone, a train-test mismatch made in the data, which LEAK-9 says
   not to do. Thinning the test windows loses rows the v2 protocol keeps. What remains, and we agree on it: the
   protocol line, the LEAK-9 note with the 0.0051-0.0056 / 0.007-0.008 numbers, a benchmark-side check (LEAK-9
   says "a protocol line the benchmark checks"), and a separate issue in pkdd's own REVIEW.md.

A4 (rmsle). Conceded. We agree that the metric's reason should lead with this dataset's own measurement.

A5 (taxi_id; the random 1M; hour columns; density mismatch). Conceded on all of it, as in my "Not argued" list.

A6 (row cuts).
   - Location filter on the community area, with the selection named: agreed (my point 1).
   - 100 m rule: agreed. A note and a decision row recorded as an exception, with sendy as the precedent.
   - 60 s against 2 min: I concede the 2-minute cut. 71-86% of the 61-119 s records log a mile, and pkdd moved off a
     longer time cut because it "dropped short rides that moved". I dispute that a note settles the rest. The
     records without a mile are not system noise:
       61-119 s, kept: 41,665 records; 8,370 log no mile. Each company's own no-mile rate on its 5-60 min trips
       predicts 643. That is 13 times fewer, so about 92% of these records are excess.
       In the systems whose 5-60 min no-mile rate is under 5% (39,134 of the 41,665): 6,825 no-mile records
       against 96 expected (70x).
       7,765 of the 8,370 (93%) also end at their pickup centroid.
     So the TAC Yellow objection (25% no-mile on 5-60 min trips) explains about 600 records, not 8,370. These are
     the cab not moving and ending where it started. That is the definition's own non-ride marker: it justifies the
     60 s cut with "no mile, the same area at both ends". They carry 2.3-2.8% of the test squared error on
     0.11-0.14% of the rows (column audit E). The pkdd precedent does not cover them. There the 30 s cut held "once
     [the trips within 100 m] are gone", because a rule on the inputs removed the non-rides. Here no such rule
     exists, so without a filter they stay. The filter I ask for rests on the recorded drop-off (an input, as in the
     100 m rule) and the meter, not on the travel time.
     Narrowed remedy: drop the 61-119 s records that log no mile and share the centroid at both ends (7,765 trips,
     0.12% of the kept rows). Keep the rest of the band, and state its weight in the notes. Rule: USE-7 (Must),
     its nyc/pkdd case; CLEAN-11 (Should), whose "unless it is no task row" this is.

A7 (DST, 120 km/h, notes). Agreed. These are P7 fixes; none of them is a reason to withhold.

Where the panel stands after this rebuttal: ship after these changes.
  - Coarsen to community areas (LEAK-10), unless the curator amends the rule.
  - Filter on the community area and name the in-city selection.
  - The LEAK-9 protocol line and note.
  - Drop the 7,765 short no-mile same-centroid records.
  - The DST repair and the 120 km/h filter.
  - The rewritten notes.

</details>
