# 2024_lusaka_mobility_prediction_hackathon

**Outcome:** added. A second-pass review panel (full) after Lennart's review of PR #33 on 2026-11-04 recommends
shipping after changes. Validity: LEAK-10 triggered and fixed for the distance actually driven (dropped; Zindi's
Test.csv shipped it), SPLIT-1, SPLIT-9 and SPLIT-14 hold (three four-day windows, a one-day gap against a longest trip
of 788 minutes), USE-7 is applied (the 100 m cut, as nyc and pkdd), and USE-8 stays approximate, now naming that no
routing-engine route or ETA ships. USE-3/LEAK-1 is weak: the recorded endpoint is sometimes the actual drop-off, so the
straight-line distance carries some post-trip location in those rows; kept with a note, since a filter on driven
distance would select on the outcome. SPLIT-20: the windows hold different weekday mixes, kept with a note. The weather
clock is a weak LEAK-10 question (issue 3). Value: MET-4 holds (Zindi's RMSE, re-read twice), MET-2 holds with the
tail written into the notes, and an untuned LightGBM's RMSE is about 18% below a constant prediction's (TP: a real,
non-trivial signal). Quality: CLEAN-11 on long and impossibly fast trips (issues 4 and 5). The wording fixes the panel
agreed on are in `dataset.py`; the three changes to the rows or the join wait for your decision.

**Main points:** Lag the weather join by 3 hours instead of 1 (issue 3)? Drop the 20 trips over 3 hours (issue 4)
and the 19 trips faster than 120 km/h in a straight line (issue 5)?

**Issues for Lennart:**

3. **Lag the weather join by 3 hours instead of 1?**

   * **Problem:**
     - Each trip gets the weather row stamped one hour before its start hour, and the source dictionary calls the
       weather stamp "Local date and time", like the trip start.
     - The weather's own daily curve points to UTC stamps instead (Lusaka is UTC+2).
     - If the stamps are UTC, a trip at 10:30 local gets the row stamped 09:00, which is 11:00 local, and that row's
       "precipitation in the past hour" overlaps the ride: a look past the prediction point a deployed model would not
       have[^3-point].
   * **Evidence:** Mean temperature is flat at stamps 02 to 04 (18.80 to 18.82 °C), rises 1.09 °C at stamp 05, about
     50 minutes before the 05:50 local sunrise, and peaks at stamps 12 to 13: read as local time, that is solar noon
     (about 12:17), two hours before the usual mid-afternoon peak; read as UTC, it is 14 to 15 local, the usual time;
     rain peaks at stamp 14. The trip file also runs from 02:03 local on 1 January to 02:09 local on 1 February, a
     calendar month in UTC.
   * **Effect on the task:** Nothing that can be measured. Each weather column alone scores about 0 skill (−0.021 to
     0.00003); the correlation of hourly trip pace with precipitation stays between −0.019 and 0.023 at every shift
     from −4 to +4 hours; a participant model given the weather of the following 1 to 2 hours improved RMSE by at most
     0.04, inside the ±0.05 noise.
   * **Consistency:** None on this question; no earlier dataset questioned the clock of a weather file against its
     source. The nearest, ashrae_great_energy_predictor_iii_1m, shifts its weather from UTC to the readings' local time
     because its source states the weather is UTC; here the source states local.
   * **Panel:** The mediator and the critic favour the 3-hour lag: fixing the definition beats a note when the fix is
     cheap and safe[^3-fix], and the measurement on the data outranks the dictionary[^3-ev], though only by inference.
     The advocate holds that the note is enough, since the source's own dictionary says local and the effect is zero.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | 1-hour lag with the note (implemented) | the join on the stamps as published; the notes say the clock is unverified, with this evidence, and no longer claim the join "never" uses the current hour | the source's dictionary says local; the effect is zero | a look past the prediction point if the stamps are UTC |
     | B | 3-hour lag | `floor(trip_start) - 3h`; the join changes, so the container is rebuilt | safe on either clock; no measured cost | rests on the data's curve against the dictionary, by inference |

   * **Recommendation:** B, the 3-hour lag. **Decision:** 3-hour lag (B), or 1 hour with the note (A)?

   **Notes for the AI:** on B, change the weather key in `dataset.py` to `floor(trip_start) - 3h`; it changes the join,
   so the container is rebuilt.

   [^3-point]: **LEAK-10** (Should here, weak): a feature holds only what existed at the prediction point; a validity
     question.
   [^3-fix]: **P7** of the principles.
   [^3-ev]: **EV-2** (Must): evidence ranks; when two pieces of evidence disagree, the higher one wins.

4. **Keep the 20 trips over 3 hours, or drop them as nyc and pkdd do?**

   * **Problem:**
     - 20 kept trips last over 3 hours: the longest, 788 minutes, drove 20.2 km and ended 1.1 km in a straight line from
       its start (1.54 km/h over the driven distance), and others ran at 0.31 and 0.32 km/h for 304 and 240 minutes.
     - They look like trips never closed in the app, but the source says nothing about how a trip is closed.
     - The cleaning rules turn an impossible value into a missing one (the row then leaves) and keep a value that is
       only unusual[^4-clean].
   * **Effect on the task:** The largest effect on the score. RMSE on minutes squares these errors.
     The 20 rows hold 11.8% of the target's squared spread, and 8 of them fall in test windows. In the window from
     2023-01-25 the 788-minute trip alone holds 21% of a constant prediction's squared error (RMSE 13.33 with it, 11.85
     without), so that window's ranking of models depends partly on one trip. Trips over 120 minutes hold 16.9%, 28.8%
     and 15.7% of the three windows' squared deviation.
   * **Consistency:** nyc_taxi_trip_duration_1m drops trips over 3 hours on a measured fact, a cluster of broken clocks
     just under 24 hours whose fares are those of few-minute trips. pkdd_15_taxi_trip_time_prediction_ii_1m drops them
     too (`MAX_TRAVEL_TIME_S = 3*3600`, "a meter left running") without such a cluster. Lusaka has no cluster and no
     fare field.
   * **Panel:** For keeping (advocate): nyc's fact is absent here, and dropping training rows over 120 minutes gains
     only 0.03 to 0.10 RMSE, about the ±0.05 noise; the source scored these trips in its own RMSE. For dropping (critic,
     mediator): the values point to unclosed trips, the effect that matters is on the test scores rather than on
     training, nothing sets Lusaka apart from pkdd, and a raw-minute RMSE weights the tail more than the RMSLE of nyc
     and pkdd.
   * **Unknown:** What would settle it: a source statement on how Yango closes a trip.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep (implemented) | kept, with the numbers in the notes (the sentence that "neither the source nor the inspected values proves they are errors" is gone); the keep is recorded as an exception to the pkdd cap | nyc's fact is absent here; dropping training rows over 120 minutes gains about the noise; the source scored these trips | one trip holds 21% of a window's constant-prediction squared error; nothing sets Lusaka apart from pkdd |
     | B | Drop as unclosed | trips over 3 hours get a missing target and leave, with a Decision table: 20 rows, a rebuild | follows pkdd; the values point to unclosed trips | the impossibility rests on a reading of the values, not on a source statement; 8 rows are test rows, so the cut changes what the test windows score |

   * **Recommendation:** B, drop (critic, mediator). **Decision:** drop the 20 trips (B), or keep them as an exception
     (A)?

   **Notes for the AI:** on B, drop trips over 3 hours as unclosed (target missing, CLEAN-11 then CLEAN-15) with a
   Decision table (20 rows) and rebuild. On A, record the keep as an exception to the pkdd cap, naming the fact (no
   broken-clock cluster, a positive driven distance on every trip).

   [^4-clean]: **CLEAN-11** (Should): impossible values become missing; values that are only unusual stay. **CLEAN-15**
     (Must): drop rows with a missing target. A quality question and a consistency check with precedent.

5. **Drop the 19 trips faster than 120 km/h in a straight line, as pkdd does?**

   * **Problem:**
     - 19 kept trips imply a straight-line speed from start to end over 120 km/h, 10 over 150 km/h, the fastest 416 km/h
       (8.9 km in 1.28 minutes).
     - The straight-line distance comes from the unmasked points, so these speeds are exact: the duration or the
       endpoint is wrong[^5-clean].
     - pkdd_15_taxi_trip_time_prediction_ii_1m drops such trips as "a GPS jump or a gap"
       (`MAX_STRAIGHT_LINE_KMH = 120`).
   * **Effect on the task:** Almost nothing. The trips are short and hold under 0.1% of the squared spread; 4 of them
     are in test windows. It is a consistency point.
   * **Panel:** The advocate, the critic and the mediator all lean to dropping (the pkdd precedent, a cheap and safe
     fix[^5-fix]); it changes the rows, so it is your call.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep with the note (implemented) | kept, named in the notes as an anomaly | no change to the rows | departs from pkdd |
     | B | Drop | 19 rows leave, with a Decision table; a rebuild | follows pkdd; a cheap and safe fix | changes the rows |

   * **Recommendation:** B, drop. **Decision:** drop (B), or keep with the note (A)?

   [^5-clean]: **CLEAN-11** (Should), then **CLEAN-15** (Must): an impossible value becomes missing, and a row with a
     missing target is dropped. A quality question.
   [^5-fix]: **P7** of the principles.

**Review panel:** ship after changes (mediator). Tier full, a second pass after Lennart's review of PR #33
(2026-11-04): seven evidence agents, the advocate and the critic with one rebuttal each, and the mediator. Claims: 25
audit rows over claims 1 to 58 and the metric; 18 hold, 6 refuted or overstated (the long durations "not errors", the
cut "on an input known at booking", the byte sizes, and three stale or misread lines; all reworded in the notes or
superseded), 1 row untested (claims 33, 44 and 51). Blind review: include; its main concern is RMSE on a target with
heavy outliers. Task gamer: no exploit beats the ±0.05 RMSE noise; its best try, the weather of the following hours,
improved RMSE by at most 0.04. Agreed: the driven-distance leak is gone, the split, RMSE in minutes, the 100 m cut,
and the wording fixes now in the notes. Disputed: the weather lag (LEAK-10, issue 3) and the trips over 3 hours
(CLEAN-11, issue 4); the speed cut (CLEAN-11, issue 5) was agreed but changes rows.

<details><summary>Mediator</summary>

**Recommendation**

```text
Verdict: ship after changes.
Validity: SEL holds. USE-5 holds. USE-8 approximate (accepted CC 2026-10-29); fit_reason gains the no-router gap.
  USE-7 applied (100 m cut, as nyc/pkdd); its "known at booking" reason is reworded. USE-3/LEAK-1 weak: the
  endpoint means two things, kept with a note. LEAK-10 holds for the driven distance (dropped). LEAK-10 is weak for the
  weather clock: the data favour UTC stamps, so lag the join 3 h. LEAK-16 holds (no copies). SPLIT-1, SPLIT-9 and
  SPLIT-14 hold (3 windows, 1-day gap, max trip 788 min, 4th window 0.478). SPLIT-20 departure kept with a note
  (weekday mix). PROV-8 calendar conflict already stated. PROV-10 wording overstated, reword.
Value: MET-4 holds (Zindi RMSE re-read twice). MET-2 holds with the tail written down (f1: one row = 21% of the dummy
  squared error). TP: skill about 0.18, not trivial.
Quality: CLEAN-11. Trips over 120 km/h are dropped as in pkdd. Trips over 3 h go to the curator (rule against the
  nyc and pkdd caps).
Weighed: none.
For the curator: issue 1, a consistency check (20 trips over 3 h, 11.8% of the squared spread, 8 in test windows).
```

**Changes to make now (no decision needed)**

1. **Weather join: lag 3 h instead of 1 h.** Use `key = floor(trip_start) - 3h`. Rules: LEAK-10 (weak, so a Should), and the remedy ladder (fixing the definition beats a note), with EV-2 deciding the fact.
   - Decisive experiment:
     - The mean temperature jumps +1.09 °C at stamp 05, about 50 min before the 05:50 local sunrise. Stamps 02 to 04 are flat (18.80 to 18.82).
     - The maximum falls at stamps 12 to 13 (24.94 to 24.98), which is solar noon (about 12:17 local), not the usual 14 to 15.
     - Rain peaks at stamp 14.
     - Read as UTC+2, all three points are physical. The trip file is a UTC calendar month (02:03 local Jan 1 to 02:09 local Feb 1), while the weather is a calendar month on its own stamps.
   - On the other side, the dictionary labels the weather stamp "Local date and time". The measurement on the data outranks it (EV-2), but only by inference, so it is weak.
   - The effect is nil either way:
     - The correlation of hourly median pace with precipitation stays between −0.019 and 0.023 at every shift from −4 to +4 h.
     - The task gamer's future-weather exploit stayed within the ±0.05 noise.
     - The weather columns' single-feature skill is about 0.
   - So the 3 h lag costs nothing. It is safe on either clock, and under UTC it reproduces the intended "hour before the start hour".
   - If the curator prefers to keep 1 h, the word "never" must go in the same edit, with a note on the clock. Both sides accepted that fallback.
   - Rebuild only on the curator's ask.
2. **Drop the 19 trips over 120 km/h in a straight line**, with a Decision table. Rules: CLEAN-11 (impossible value), CLEAN-15 (Must), and the pkdd precedent (`MAX_STRAIGHT_LINE_KMH = 120`), followed because the facts are alike.
   - `str_distance_km` comes from the unmasked points, so these speeds are exact.
   - 10 trips exceed 150 km/h. The maximum is **416.2 km/h** (8.879 km in 1.28 min), found by two independent recounts. The precedent checker's "206 km/h" is wrong.
   - The effect is about 0. Both sides lean to this.
3. **`fit_reason` and `use_case` (USE-8, USE-6).**
   - Add: "no routing-engine route or ETA ships; an in-ride arrival estimate at pickup, from geometry, time and weather."
   - Evidence: the realised route distance, as an upper-bound proxy, cuts RMSE by 18 to 27%.
4. **Endpoint wording in `curation_comments` (USE-3, LEAK-1, Should).**
   - Replace "The cut is on an input known at booking" with "a cut on the recorded endpoint, which for these rows is not a booked destination".
   - Add that the endpoint means two things:
     - In some rows it is the realised drop-off: the 2,364 dropped trips ended within 0.1 km of their start but drove a median 4.5 km.
     - In others it is a requested destination: 1,756 kept trips drove under 0.9× the straight line, and 290 under 0.5×.
   - Say plainly that in the first case `str_distance_km` carries some post-trip location. On this reading the critic is right: the counts show the meaning is mixed, not that the stand-in works.
   - Do not filter on driven distance.
   - `Decision.why` and the `MIN_STRAIGHT_LINE_KM` docstring use the same wording as nyc and pkdd and can stay.
5. **Long-trip sentence (CLEAN-11, P4 consistency).** Delete "neither the source nor the inspected values proves they are errors". The 788.07-min trip drove 20.2 km at 1.54 km/h, and kept trips ran at 0.31 and 0.32 km/h for 304 and 240 min. Its replacement depends on issue 1.
6. **Metric note (MET-4, MET-2).** MET-4 requires a measured weakness to be written in the notes with its numbers. Add:
   - the top 1% of errors hold 54 to 66% of LightGBM's squared error;
   - trips over 120 min hold 16.9%, 28.8% and 15.7% of each window's squared deviation;
   - one row holds 21% of window f1 (dummy RMSE 13.331, or 11.848 without it).
   - The decision to keep RMSE in minutes stands.
7. **Correct the reason given in the CC line.** Add an Assessment line, without editing the CC: the basis is MET-4, not "as the other RMSE-scored ETA datasets". No shipped ETA dataset scores RMSE on raw time: delivery_eta and maps_router_eta use RMSE on log targets; nyc and pkdd use RMSLE.
8. **`splits_comment` (SPLIT-20, a note).** Add that the windows hold unequal weekday mixes (f1 has no Sunday) and that the Sunday drop is weekly, not drift. All five Sundays sit at 11.07 to 12.11 min, against 13.70 to 14.67 on other days.
9. **`download_description` and the record (PROV-10).** "Byte lengths match" becomes "sizes match the listing's rounded sizes" (15,620,473 B against 15.6 MB, and so on).
10. **Record bookkeeping.**
    - A new Assessment line supersedes "no panel ran for this dataset" and "no public solution found".
    - Add Lusaka as an `applied` row of USE-7 in `.claude/skills/knowledge-curation/references/use_case.md`: the Cases table near line 165 and the Cases line near line 55.
    - Correct the panel notes: the "2023-01-27 dip" is Sunday 2023-01-29, a weekly pattern. The prep report and the practitioner both carried the wrong date.

**For the curator**

**1. The 20 trips over 3 h: keep, or drop like nyc and pkdd? (P7, CLEAN-11 Should; consistency check 2. The largest effect on the score.)**

- **Problem:** CLEAN-11 says values that are only unusual stay. Both ride-time precedents still cap at 3 h:
  - nyc, on a measured broken-clock cluster;
  - pkdd, `MAX_TRAVEL_TIME_S = 3*3600`, "a meter left running", with no cluster. No panel agent cited the pkdd cap.
- **Effect:** these 20 rows hold 11.8% of the target's squared spread, and 8 fall in test windows. Window f1's ranking leans on one row, the 788-min trip.
- **Advocate's best case:** nyc's cap rests on a fact Lusaka lacks (no cluster near 24 h, no fare field). A 13 h, 20 km ride is unusual, not impossible. Dropping training rows over 120 min gains only 0.03 to 0.10, about the noise.
- **Critic's best case:** the inspected values point to unclosed trips (0.31 to 1.54 km/h over 4 to 13 h), which makes them impossible targets (CLEAN-11 to missing, then CLEAN-15). The effect that matters is on scoring, not on training: f1 is 21% one row.
- **Rule:** rules win over precedents. A precedent that conflicts with a rule is flagged, not followed. So either these rows are impossible, as in pkdd's "meter left running" reading, or the precedent caps need their own impossibility fact.
- **What would settle it:** a source statement on how Yango closes a trip, or the driven-distance-to-time profile of the 20 rows against pkdd's.

```text
**Consistency check (AI, 2026-11-04):** keeping the 20 Lusaka trips over 3 h (up to 788 min at 1.54 km/h; 11.8% of
the squared spread, 8 in test windows) differs from pkdd_15_taxi_trip_time_prediction_ii_1m and
nyc_taxi_trip_duration_1m, which drop trips over 3 h (a meter left running; broken clocks). What sets Lusaka apart?
(a) no clock-error cluster and a positive driven distance on every such trip: kept as unusual, recorded as an
    exception with the tail shares; (b) treat Lusaka like pkdd: trips over 3 h are unclosed, target missing, dropped;
(c) reopen pkdd's 3 h cap to match Lusaka; (d) amend CLEAN-11 to name a meter left running.
```

My lean is (b): no distinguishing fact holds against pkdd, and a raw-minute RMSE weights the tail more heavily than RMSLE does. This is the curator's call.

**Agreed facts**

- **Rows:** 112,760 raw; 21 without a start; 2,364 under 0.1 km; 110,375 kept, 9 features.
- **Calendar:** 2023-01-01 02:03 to 2023-02-01 02:09, against "January 2024" on the source page.
- **Leak:** driven distance (`transporting_distance_fact_km`) dropped. Zindi's Test.csv shipped it.
- **Copies:** 0 duplicate rows, 0 duplicate coordinates, 0 shared ids.
- **Splits:** train/test rows 94,929/11,141, 79,929/16,059 and 65,901/13,635. A 4th window would hold 0.478 of the rows.
- **Gap:** with the 1-day gap, 0 training trips end after a window starts (24/6/13 without it). The gap moves RMSE by at most 0.021.
- **Weather join:** 23 rows have no weather, all on Feb 1 after the file ends.
- **Partial Feb 1:** 70 rows; moves RMSE by 0.002.
- **Scores:** dummy RMSE 11.203 / 13.331 / 11.030; LightGBM about 8.95 / 11.2 / 8.96; IID skill 0.198 against 0.182 temporal.
- **Masking:** masked haversine is within ±0.12 km of `str_distance_km`.
- **Task gamer** (no `Potential leak, kept on purpose:` notes and no accepted warnings, so all three are new, and none is an issue):
  - future trip density (LEAK-30 class): no gain;
  - future weather (LEAK-10/LEAK-1): within the ±0.05 noise;
  - whole-day count (LEAK-30): within the noise.
- **Blind reviewer:** "Jan 1 has only 70 trips" is Feb 1; this is not material.

**Consistency with precedent**

- The 100 m cut, the domain `industry & manufacturing`, the temporal design and keeping one city (PROV-6/PROV-7) are consistent with nyc and pkdd. The register raises no flag.
- RMSE in minutes is consistent with MET-4 (each precedent keeps its own source's metric). Lusaka now sets the precedent for the Zindi ETA siblings (yassir, Accra, Maputo).
- The speed cut (change 2) follows pkdd.
- The 3 h cap departs from nyc and pkdd: issue 1.
- Follow-on, not this dataset: four sibling records still say `technology & internet`. Align them when they are promoted.

</details>

<details><summary>Claim audit</summary>

**Claim audit: 2024_lusaka_mobility_prediction_hackathon (second-pass panel, 2026-11-04)**

**The points the panel was asked to look at.**

1. **Partial last day (2023-02-01).** It does not matter. It has 70 rows, all between 00:00 and 02:09. Removing them moves LightGBM's window-0 RMSE from 8.944 to 8.942.
2. **The "2023-01-27 dip".** It is on the wrong date. Day 01-27 has a mean of 14.42 minutes. The low day is Sunday 2023-01-29, with a mean of 11.26, and it is a weekly pattern rather than drift: every Sunday sits between 11.07 and 12.11 (01-01, 01-08, 01-15, 01-22, 01-29), against 13 to 15 on other days.
3. **`str_distance_km`.** It is available at booking only under the accepted approximation (claim 20 below). It is not a crutch: dropping it costs LightGBM only 0.19 to 0.25 RMSE per window, because the masked coordinates carry it. Masked haversine minus `str_distance_km` is within ±0.095 km at p1 and p99.
4. **Metric reference.** I re-read the Zindi page API. It says "The evaluation metric for this competition is Root Mean Squared Error", with no transform. The metric holds.

**Tests run:** raw counts, weather, masking and Test.csv; per-fold scoring with `data_foundry.v2.metrics.scorer`, LightGBM and the weekday pattern; the weight of a single row in each fold's RMSE; the mirror's Test.csv, SampleSubmission.csv and VariableDefinitions.csv at the pinned commit, read as data only.

| # | Claim (source) | Test | Result | Evidence | Rule |
|---|---|---|---|---|---|
| 23 | "Keep all durations… neither the source nor the inspected values proves they are errors" (curation_comments) | Speed (driven km / hours) of the longest kept trips; compared with the nyc_taxi precedent | **Refuted (the inspected values do point to errors)** | 788.07 min for 20.2 km driven and 1.12 km straight-line (1.54 km/h). 303.6 min for 1.58 km (0.31 km/h). 239.5 min for 1.26 km (0.32 km/h). 20 kept trips run over 180 min, and 67 trips are under 2 km/h. nyc_taxi_trip_duration_1m dropped trips over 3 h as "broken clocks… at walking speed". | CLEAN outliers; P4 consistency (principles §Consistent judgement 2); MET-2 |
| 25 / Metric (MET-2 meaning) | RMSE on minutes means on our folds what it meant on the source's | Share of fold squared error held by one row | **Holds with a caveat** | In window 1, one trip (788 min) holds 21% of the dummy squared error: dummy RMSE is 13.331, and 11.848 without that row. In the other windows the largest row holds 4.2% and 4.1%. Across windows the top 0.1% of rows hold 25%, 43% and 26% of LightGBM's squared error. | MET-2, TP-6 |
| 20 | "The cut is on an input known at booking" (curation_comments) | Is the recorded end point the booked destination? | **Refuted as worded** | The 2,364 dropped trips end within 0.1 km of their start in a straight line but drove a median 4.5 km. So the recorded end is the drop-off point, not a booked destination. The cut is exact on `str_distance_km`: on masked coordinates, 109 kept rows fall under 0.1 km and 455 dropped rows fall over it. But it conditions on where the trip actually ended, which the app does not know at booking. | USE-3, USE-7, LEAK-1 (Should within the accepted approximation) |
| 49 | "no public solution found" (screening) | Look at the pinned mirror | Refuted (minor, superseded) | Mwandamena/yango-hackathon is a participant repository with a starter notebook, as the definition itself says. | EV-2 |
| prep_report | "2023-01-27 dips… drift" | Daily means by weekday | Refuted (date and cause) | The dip is on 01-29. All five Sundays have means from 11.07 to 12.11. | LEAK-22 to LEAK-26 (probe reading) |
| 57 | "no panel ran for this dataset" | – | Stale | This panel is that run. | writing.md |
| 1, 2, 5 | Target is ride minutes; trip-start ETA | VariableDefinitions.csv, speed check | Holds | Target is "Actual travel time in minutes". Median speed is 18.5 km/h (p5 8.1, p95 31.8). | USE-5 |
| 3, 22, 39 | 112,760 raw, 21 missing, 2,364 under 0.1 km, 110,375 kept, minimum 01-01 02:03:12, maximum 02-01 02:09:45 | Recount from Train.csv | Holds | Exact match. Exactly one trip has a zero distance. | – |
| 4, 17 | Files are January 2023, not 2024 | Ranges of Train, Test and weather | Holds | Weather runs 2023-01-01 00:00 to 01-31 23:00 (744 hours). The Zindi page says "January 2024". | PROV-8 |
| 6, 24 | Earlier-hour weather, local time | Dictionary; temperature and trip-volume curves | Holds | `prev_hour_precipitation_mm` is "precipitation in the past hour", so the floor−1h key covers the hour ending one hour before the start. Temperature peaks at 13:00 and bottoms at 04:00. Trips peak 16:00 to 18:00. The dictionary says "Local date and time". | LEAK-1 |
| 28, 40 | 110,352 weather matches; 23 missing | Join recount | Holds | All 23 missing rows start on 2023-02-01 between 01:05 and 02:09, after the weather file ends. | – |
| 19 | 2.1%, 1.3 to 2.9% of every day | Per-day share | Holds | Min 1.29% (01-01), max 2.92% (01-11). | – |
| 21, 55 | Dropped trips: median 22.1 vs 10.8 min, 93% over 5 min, 4.5 km driven, 16% of the squared spread | Recompute | Holds | 22.14 / 10.78 min, 93.2%, 4.547 km, 15.8%. | – |
| 26, 32, 40 | Under 1 day per trip, so training trips end before the refit; the source's test interpolates the month | Latest training-trip end per fold; Test.csv dates | Holds | Maximum duration is 788 min across all raw rows. Latest training trip end is 01-28 00:23, 01-24 00:15 and 01-20 00:37, each about a day before its test start. Test.csv covers 01-01 02:04 to 02-01 02:02 and shares all 32 days with Train. | SPLIT-9 |
| 8, 9, 30, 35 | Windows start 01-21, 01-25, 01-29 with a 1-day gap; partial final day | `make_splits` | Holds | Train/test rows: 94,929/11,141, 79,929/16,059, 65,901/13,635. | SPLIT-1 |
| 34 | A fourth window breaks the 0.5 floor | Share of kept rows before 2023-01-16 | Holds | 0.478. | SPLIT-14 |
| 10, 15 | Driven distance removed | `feature_cols` | Holds | Nine features: no `transporting_distance_fact_km`, `trip_id` or day-only date. Test.csv ships the driven distance, so the source's task was not a trip-start ETA. The definition's change is right. | LEAK-10 |
| implied | No copies across the split | Duplicate coordinates, trip-id overlap | Holds | 0 duplicate coordinate tuples, 0 duplicate ids, 0 Train ids in Test. | LEAK-16 |
| 43 | Byte lengths match the organizer listing | File sizes | Holds only to the listing's precision | 15,620,473 B, 6,433,913 B and 48,742 B against the listing's 15.6 MB, 6.4 MB and 49 KB. That matches at MB/KB precision, not byte for byte. | PROV-10 |
| Metric (MET-1, MET-3, MET-4) | `Metric.source("rmse")`, identity, reference #evaluation | Zindi API page | Holds | "The evaluation metric for this competition is Root Mean Squared Error"; submission is `trip_id`, `Target`; no transform. | MET-4, MET-3 |
| Metric (MET-2 computable) | Scorable on every fold, no scoring columns | Dummy mean scored by `scorer` per fold | Holds | Dummy 11.203 / 13.331 / 11.030; LightGBM 8.944 / 11.211 / 8.967. Every fold has 11k or more rows. | MET-2 |
| 54 | Domain aligned with other ride-time datasets | grep of the siblings | Holds | nyc_taxi, pkdd_15, maps_router_eta and delivery_eta all use `industry & manufacturing`. | – |
| 29 | Partial final day | Hour profile on Feb 1 | Holds and does not matter | Rows by hour on Feb 1: 47 / 20 / 3. RMSE moves by 0.002. | – |
| 7, 13, 16, 27, 41 | Approximate fit; capture time and latency unverified | – | Holds as documented | The curator accepted it on 2026-10-29. | USE-8 |
| 33, 51, 44 | Reporting delay; access restrictions; 112,716 matches before the filter | – | Untested | Not decidable from the data. 112,716 follows from 112,739 − 23 because no dropped trip starts on Feb 1 after 01:00; I did not run it separately. | EV-4 |

**Refuted and untested claims, ranked (validity first, Must first)**

1. **Claim 23, long durations kept as plausible (P4/P7 consistency and MET-2; a Should and weighing call, the highest effect).**
   - What the data shows: the inspected values do show trips at standing or walking speed. Four kept trips over 239 min travelled under 2 km/h, the slowest at 0.31 km/h. 20 trips run over 3 h.
   - The precedent this cut followed (nyc_taxi_trip_duration_1m, cited for the 100 m radius) also drops trips over 3 h as broken clocks. Lennart took one cut from that precedent and not the other, with no fact recorded that sets the case apart.
   - What it changes: window 1's RMSE is 21% one row, the 788-min trip. Model rankings in that window are partly decided by whether a model chases one probable meter error.
   - Mildest remedy: a consistency check to the curator. Either (a) drop trips over 3 h, or under about 2 km/h, as nyc does, with a Decision table (about 20 to 67 rows); or (b) keep them, with an exception naming the fact, for example that the source kept them in its RMSE. In both cases, correct the sentence "neither … the inspected values proves".
2. **Claim 20, "a cut on an input known at booking" (P4, LEAK-1/USE-7; Should within the approximation).**
   - The dropped rows show the recorded end is the realised drop-off point, so the filter selects on the trip's outcome location.
   - The effect is bounded: 2.1% of rows, 15.8% of the squared spread. The curator's reason, that a round trip has no meaningful booked destination, stands.
   - What it changes: the wording, and an honest note that deployment would still see these bookings with some other destination.
   - Mildest remedy: reword the sentence to "a cut on the recorded endpoint, which for these rows is not a booked destination". No code change.
3. **Prep report's drift reading of the "01-27 dip" (a probe interpretation, not a definition claim).**
   - It is the Sunday effect on 01-29. Window 0 starts on a Sunday, but every window contains a Sunday, so nothing changes in the definition.
   - Remedy: correct the checklist row only.
4. **Claim 43, wording.** "Byte lengths match" holds only at MB/KB precision. Remedy: reword to "sizes match the listing's rounded sizes".
5. **Claims 49 and 57, stale record text.** Superseded by later entries and by this panel. No action beyond the record's next assessment line.
6. **Untested: claims 33 and 51, the 112,716 count, and organizer byte identity.** None of these is decidable from the files. They are already documented as cannot-verify.

**Verdict for the curator.**
- Validity: SPLIT-1 and SPLIT-9 hold (1-day gap against a maximum trip of 788 min). LEAK-10 is fixed (driven distance removed). USE-7 and LEAK-1 hold under the accepted approximation, with claim 20 to be reworded.
- Metric: MET-4, MET-3 and MET-2 hold. RMSE is confirmed on the source page and scorable on all three windows.
- Open: one weighing call on long, slow trips (issue 1), which is the only finding that moves a score materially.

</details>

<details><summary>Column audit</summary>

**Column audit: `2024_lusaka_mobility_prediction_hackathon` (second pass, 2026-11-04)**

The frame was rebuilt from the definition through `dataset_io.from_definition`: 110,375 × 10, 9 features. The panel's pointers were `str_distance_km` and the partial last day; both are answered under "Focus" below. The dtype probe flagged 0 of 8 columns, and I agree: no column has a cleaning problem in its dtype.

**Column table**

| column | meaning | known at prediction? | dtype and cleaning | verdict | rule |
|---|---|---|---|---|---|
| Target | trip duration in minutes (source target) | it is the outcome | float64, range 1.02 to 788.07, no missing values, unchanged | fine, but the long tail drives RMSE (problem 3) | CLEAN-15, CLEAN-16 (curator kept minutes on 11-04) |
| trip_start | `lcl_start_transporting_dttm`, local time when the pickup starts | yes, it is the prediction point | datetime64; 21 rows without a start were dropped; day-only copy dropped | fine | USE-3, CLEAN-5 |
| origin_lat / origin_lon | pickup coordinates, geomasked | yes | float64, all values unique, no missing values | fine | LEAK-10 |
| destination_lat / destination_lon | end coordinates, geomasked; the source does not say whether this is the requested or the actual end | partly: a stand-in (problem 1) | float64, no missing values | fine as the accepted approximation; see problem 1 | USE-3, LEAK-10 |
| str_distance_km | straight-line km between the original (unmasked) endpoints | same status as the destination | float64, 0.1 to 21.6; this column defines the 100 m filter | fine (the approximation); see problem 1 | USE-3, USE-7 |
| precipitation_type | weather category (Rain / No precipitation) at weather hour floor(start) − 1 h | yes if the timestamps are local (problem 2) | category with 2 levels, 23 missing values from coverage | fine; the possible timezone shift is weak (problem 2) | CLEAN-14, LEAK-10 |
| prev_hour_precipitation_mm | precipitation over the hour before the weather stamp | same | float64, 0 to 11.78, 23 missing | same | LEAK-10 |
| temperature_C | temperature at the weather stamp | same | float64, 23 missing | same | LEAK-10 |
| (dropped) transporting_distance_fact_km | distance actually driven, measured over the completed trip | no, measured after the outcome | removed | removal correct | LEAK-10 |
| (dropped) trip_id, lcl_start_transporting_dt, weather row counter, lcl_date | an id and copies of other columns | n/a | removed | removal correct | CLEAN-3, CLEAN-5 |

Other checks on the frame:
- No duplicate rows, and no duplicate feature rows.
- The 23 rows without weather all start between 2023-02-01 01:05 and 02:09, after the weather file's last hour (2023-01-31 23:00). That missingness comes from time coverage, not from the outcome.
- Precipitation type and amount disagree in 6,666 + 545 rows. That fits a type reported for the moment against an amount accumulated over the hour, so it is not a coding error.

**Focus answers**

**Is `str_distance_km` known at booking?** Only as the accepted stand-in, and the data points both ways on what the destination is:
- Recorded end = actual drop-off in some trips. These are the round trips just dropped: under 100 m straight line, a median 4.5 km driven.
- Recorded end = requested destination in others. 1,756 kept trips (1.59%) drove less than 0.9× the straight line, which is impossible if the endpoint is the drop-off. Their median duration is 4.05 min against 10.9 for the rest; 290 trips drove under 0.5× the straight line. These look like riders who got out early, with the requested destination kept.

**Does masking change the signal?** No:
- The straight-line distance computed from the masked coordinates differs from `str_distance_km` by at most ±0.12 km (sd 0.046), so the jitter is about 60 m per point.
- Correlation with Target: 0.49003 from the masked coordinates against 0.49002 for `str_distance_km`.
- `str_distance_km` therefore adds almost nothing a model could not compute from the coordinates. That kind of field is plausibly what an app has at the moment of booking.

**Is the partial last day 2023-02-01 censoring?** No:
- The file ends at 02:09: 70 rows, mean 9.8 min, all in the night hours.
- Every observed duration is under 24 h, and the one-day gap covers it.
- I agree with the prep report: a partial day, not censoring.

**Problems, ranked by `principles.md`**

**1. P3/P4 (USE-3, LEAK-10): the meaning of the destination is mixed. This is a note, not a leak to remove.**
- Evidence: 1,756 trips (1.6%) drove shorter than the straight line, and round trips existed before the filter. So the recorded end is sometimes the requested destination and sometimes the actual drop-off.
- In the "actual drop-off" case, the destination is a weak post-outcome value. NYC taxi precedent accepts it.
- In the "requested" case, the target for the rows where the rider got out early is not the time to that destination. These rows are short and add little RMSE.
- Mildest remedy: add one sentence to the endpoint bullet saying both cases occur, with the 1,756 / 290 counts. Do not filter on the driven distance: it is measured after the outcome, so filtering on it would select rows on the outcome (LEAK-22 spirit).
- Fit stays `approximate`.

**2. P4 (LEAK-10, weak): the weather clock may be UTC labelled as local, which would turn the 1 h lag into a lookahead of about 1 h.**
- The temperature curve over the day, by weather label:
  - The minimum falls at labels 02 to 04, and the temperature jumps at label 05 (18.8 to 19.9), before the January sunrise in Lusaka at about 05:50.
  - The maximum falls at labels 12 to 13.
  - Read as UTC (+2 h), that becomes a minimum at 04 to 06, a rise at 07 and a peak at 14 to 15, which is more physical.
  - The values look like reanalysis data (float32 precision).
- Against it: the trip-hour pickup pattern looks local (peaks at 07–08 and 16–17), and the cross-correlation of hourly trip-pace residual with precipitation is flat at every shift from −4 to +4 h (0.025 to 0.062). So nothing proves a shift.
- Strength: weak. The single-feature skill of each weather column is about zero or negative (temperature −0.014, precipitation −0.021, type 0.00003; leak probe).
- Mildest remedy: question for the curator. Either add a note that the timezone of the weather file is unverified, with this diurnal evidence, or lag the weather by 3 h instead of 1 h, which is safe under either clock and costs no measured skill.

**3. P6 (MET, CLEAN-11, CLEAN-16): a few very long trips dominate RMSE. Question for the curator; the minutes/RMSE decision of 11-04 stands unless reopened.**
- Trips over 120 min: 92 rows (over 180 min: 20; over 300 min: 5).
- Their share of each test window's squared deviation: 16.9%, 28.8% and 15.7%.
- One row in the 2023-01-25 window holds 21% of that window's squared deviation: started 2023-01-28 18:26, Target 788.07 min, 1.1 km straight line, about 20 km driven. That looks like a trip never closed in the app, not a real ride.
- CLEAN-11 lets a single extreme target leave only from the training period, and this one is in a test window. Dropping it is the curator's case-by-case call.
- Mildest remedy: add a note in `curation_comments` with these shares. The alternative, a log target (CLEAN-16), was already declined on 11-04 ("ok keep minutes").

**4. P7 (CLEAN-11): some straight-line speeds are impossible.**
- 41 trips exceed 100 km/h in straight line (85 exceed 80; maximum 416 km/h, e.g. 8.9 km in 1.28 min).
- The impossible value is the target or the endpoint, and the data cannot tell which. A missing target would mean the row is dropped (CLEAN-15).
- Effect on RMSE is negligible (small targets).
- Remedy: keep the rows; optionally note them next to the existing "long rides kept" sentence.

No other column problem: no target encoding, no id that encodes the label, no missingness caused by the outcome, no feature computed over all rows.

</details>

<details><summary>Split audit</summary>

**Verdict: the split is right, with notes.** Nothing needs a re-split.

**The 2023-02-01 flag and the "2023-01-27 dip":** neither is censoring.
- **The dip is on the wrong date.** The prep report reads the probe's dip as 2023-01-27, but it is 2023-01-29: 3,952 rows, mean 11.26. That day is a Sunday. All five Sundays sit at 11.07 to 12.11 minutes (Jan 1, 8, 15, 22, 29). The other weekdays sit at 13.70 to 14.67. It is the weekly cycle, not drift.
- **2023-02-01 is a partial day.** Its 70 rows all start between 00:00 and 02:09.
  - The same 00:00 to 02:10 slice on the other 31 days has means of 9.42 to 14.99 (n = 18 to 203). Feb 1's 9.82 is inside that range, and so is its p90 (15.48).
  - Feb 1 shows no sign that the extract cut trips by their end time. 5.7% of its trips end after 02:10, against 6.8% for the same slice on other days. Four end after the file's last start, the latest at 03:28.
  - The file runs from 2023-01-01 02:03 to 2023-02-01 02:09 local. That looks like a calendar-month extract by start time in UTC, with local time two hours ahead (UTC+2; this is my inference).
  - The partial day is 0.6% of the newest window and needs no cut.

**Regime: temporal is right.**
- The use case is an ETA for any passenger at trip start, from a model refit on completed trips. That is the SPLIT-6 delivery or trip-time case.
- There is no rider or driver id. The places that recur are coordinates, and the deployed model sees known places too, so no grouping is needed (SPLIT-13 does not bite).
- The source's random train/test interpolation within the month was rightly not followed (SPLIT-5, SPLIT-19 departure, stated in `curation_comments`).

**Windows and their sizes.** All three meet SPLIT-14 (at least 3 windows, train side at least 50%), and the train side expands (SPLIT-11).

| Window | Test rows | Test dates | Train rows (share) | Last train start |
|---|---|---|---|---|
| f0 | 11,141 | Jan 29 to Feb 1 02:09 | 94,929 (86.0%) | Jan 27 23:59 |
| f1 | 16,059 | Jan 25 to Jan 28 | 79,929 (72.4%) | Jan 23 23:59 |
| f2 | 13,635 | Jan 21 to Jan 24 | 65,901 (59.7%) | Jan 19 23:59 |

**Gap against label delay (SPLIT-9, SPLIT-10).**
- The longest trip is 788 minutes; 92 trips exceed 120 minutes and 2 exceed 360. Every label is known within a day.
- Without a gap, 24 / 6 / 13 training trips (f0 / f1 / f2) would end after the window start. With the one-day gap there are 0.
- The gap costs 4,305 / 3,246 / 3,639 training rows, one whole day per window.

**Quick models.** I fit LightGBM (400 trees, without the absolute-time feature) under each split. Skill is 1 - RMSE / RMSE of a constant at the training mean.

| Split | f0 | f1 | f2 | Mean skill |
|---|---|---|---|---|
| Shipped, 1-day gap | 8.953 (0.201) | 11.218 (0.158) | 8.972 (0.187) | 0.182 |
| No gap | 8.941 (0.202) | 11.210 (0.159) | 8.951 (0.189) | 0.183 |
| IID 5-fold, all rows | | | | 0.198 (RMSE 9.43) |

- Dropping the gap changes RMSE by at most 0.021, so the gap hides no shortcut.
- A random split would be mildly optimistic: skill 0.198 against 0.182.

**Ranked notes.** None is blocking.

1. **The weekday mix differs between windows (P4; SPLIT-20, the season-shaped-window check; Should).**
   - Evidence: the 4-day windows cut across a weekly cycle with a 3-minute Sunday drop. f0 holds Sun, Mon, Tue and 70 Wednesday rows. f1 holds Wed to Sat with no Sunday. f2 holds Sat to Mon plus Tuesday.
   - Every train side covers at least 2.7 full weeks, so the cycle is learned. f1's higher RMSE is not the weekday mix: its spread falls from 13.31 to 11.27 without its top-10 rows (it holds the 788-minute trip).
   - 7-day windows are not possible: the oldest train side would hold 31.8%, under SPLIT-14's 50% floor. 5-day windows (cutoffs Jan 18, 23, 28) would just pass at 50.9%, but they do not align with the week either.
   - SPLIT-21 forbids choosing windows by score, and SPLIT-12 has no source horizon to follow, so 4 days is a defensible design choice.
   - Remedy: one sentence in `splits_comment` that the windows hold unequal weekend shares and that the Sunday drop is a weekly pattern, not drift. No re-split.

2. **The prep report puts the dip on 2023-01-27; the dip is 2023-01-29, a Sunday (EV, procedure).**
   - Evidence: probe 13 lists the newest periods as Jan 27, 28, 29, 30, 31 and Feb 1, so the mean of 11.26 belongs to Jan 29 (3,952 rows).
   - Remedy: correct the date in the panel notes and REVIEW text if it is carried forward. Nothing in the repository changes.

3. **The one-day gap is stricter than the measurement needs (SPLIT-10 as amended 2026-11-04; Should).**
   - Evidence: the delay is under a day, and only 6 to 24 rows per window cross the cutoff.
   - The ride-time precedent family set a one-day gap wherever any training trip ends after the window start: nyc_taxi_trip_duration_1m, pkdd_15_taxi_trip_time_prediction_ii_1m, maps_router_eta_1m (`splits.md` cases table, 2026-10-21). Keep the gap for consistency.
   - A milder alternative only if the curator wants the day back: an as-of filter on trip end (start plus Target before the cutoff), which would add 3,200 to 4,300 rows per training side. Not recommended.

4. **The partial final day stays (SPLIT-10, no selection at the release end).**
   - Evidence: as above, 70 rows (0.6% of f0); the share ending after 02:10 is 5.7% against 6.8% on other days; the mean is in the band for its hours. It is already disclosed in `splits_comment`.
   - Remedy: none. If anything is added, it is the measurement in one clause.

5. **The f1 RMSE is driven by the target's tail. This is not a split problem.**
   - Evidence: f1 holds the 788-minute trip, its spread is 13.31 against 11.0 to 11.2 in the other windows, and 10 to 11 trips per window exceed 120 minutes.
   - This belongs to the metric reviewer (MET: RMSE on minutes was kept by Lennart on 2026-11-04). No split action.

**Not testable:** groups hidden inside the temporal task (SPLIT-13). There is no entity id, and the near-copy probe could not run (no row has 10 informative columns), so this is neither a pass nor a fail (SPLIT-30).

</details>

<details><summary>Domain practitioner</summary>

**Domain-practitioner report: `2024_lusaka_mobility_prediction_hackathon`**

**The standard items:**

- **Is `str_distance_km` known at booking?** Yes, in substance. When I order on Yango I enter a destination, so the app holds both endpoints and their straight-line distance before the ride starts. The masked endpoints plus the distance between the original points are a degraded copy of what the app has, not a leak. Our app has exact coordinates, which is better. The one residual risk: the "destination" is the recorded drop-off, not the requested one (gap 2).
- **Partial day 2023-02-01** (70 rows, 0.6% of the newest window). This is a file truncation, not censoring, and it does not move the task. I read the 2023-01-27 dip as normal weekday-to-weekend demand drift. A live ETA model faces that drift too, so it should stay in the test.
- **Metric reference.** I re-read the Zindi API page today: "The evaluation metric for this competition is Root Mean Squared Error." The record's quote is confirmed.

**Fit: approximate (I agree with the declared fit)**

It is a real in-ride ETA ("arrive at hh:mm" from pickup), one trip per row. It is scored on the next days' trips. But it is learned without the one input every ride-hailing ETA always has: the router's route and its own ETA estimate (USE-6, USE-8).

**My answers as the Yango ETA owner in Lusaka**

1. **Inputs at the prediction point.** The target is clocked from `lcl_start_transporting_dttm`, the pickup. So my moment is "the driver starts the ride", not the order. At pickup I have:
   - start time;
   - pickup and destination (exact in my system, masked here);
   - straight-line distance;
   - recent weather (I would have the current hour too; the one-hour lag is conservative and minor).

   What I would always have but the dataset lacks: the routing engine's planned route length, its traffic-aware ETA, live segment speeds, the tariff/car class and driver id. The routing engine is my baseline; any ML ETA corrects it (precedent `maps_router_eta`). I measured an upper bound on its value by adding the realised `transporting_distance_fact_km` (not a legitimate input, only a stand-in for the planned route) to a LightGBM on the declared windows. RMSE fell 8.96 → 6.57, 11.09 → 9.08 and 8.86 → 6.76 (−18 to −27%). MAE fell 4.62 → 3.42. So the shipped task is "ETA without the router". That is a real but secondary use: a fallback, a sanity check, or a new city before the router is tuned. Nothing I would lack at pickup is in the features: travelled distance is correctly dropped (LEAK-10, USE-3).
2. **Target.** Ride minutes are what I act on: the displayed arrival time, ride-pricing checks, driver dispatch chaining. I want a number, ideally with an interval. It is the real target, not a proxy (USE-5).
3. **Row, decision and test.**
   - One row is one trip, which is one ETA I display: the unit matches.
   - The test is later days on a model refit with a one-day gap. That is the deployment shape. A real refit would use months of history, not 8 to 16 days, but that is a scope limit, not a mismatch.
   - Same city, no new-site test: fine for this use case.
4. **Would I use it, and what would make me distrust it?**
   - I would trust it as a benchmark of tabular ETA from geometry, time and weather. I would not ship it over a router-based model.
   - The median relative error is about 28% (my LightGBM). For a passenger ETA, an error over 20% is a complaint.
   - Distrust comes from the tail. The ratio of travelled to straight-line distance has p50 1.43 but p99 11.6, and implied speeds reach 5 km/h at the 1st percentile. These are multi-stop rides, changed destinations or long waits: trips whose real destination was not the one that ships. Those rows decide most of the score (point 5).
5. **Metric: partly.**
   - RMSE in minutes is the competition's leaderboard metric. MET-4 says to declare it, and Lennart confirmed it on 2026-11-04 ("ok keep minutes"). It is a proper score for the conditional mean, so it is not wrong (MET-1).
   - But on these splits the 1% largest errors make up 53.9 to 65.7% of the test squared error (LightGBM with and without the route-distance proxy). In the data, the top 1% of trips by duration hold 43% of the target's squared spread.
   - So RMSE ranks models mostly on predicting about 1% of anomalous rides: round trips over 100 m, rides with stops, and an extreme of 788 min. A passenger-facing ETA owner picks models on per-trip absolute or relative error.
   - The metric I would choose: MAE in minutes. Second choice: RMSLE or the median relative error. That is what the sibling ETA tasks in this repo use (MET-3 cases: `nyc_taxi_trip_duration_1m`, `pkdd_15_taxi_trip_time_prediction_ii_1m` on RMSLE).
   - Under MET-4 a competition metric is overruled only on evidence that it is biased or wrong. Tail dominance is a measured weakness, not a bias: neither the source nor the forum shows the metric was gamed. I would keep RMSE as declared and record the tail share in the notes (MET-10, resolution factor).

**Gaps, ranked by how much they change the task**

1. **No router or route estimate (USE-6, USE-8).** RMSE is −18 to −27% with a route-distance proxy. This changes the task from "refine the routing engine's ETA" to "ETA from geometry". It cannot be fixed from this source. It is not yet named in `fit_reason`, which names only the endpoint and weather stand-ins, and it should be.
2. **Recorded drop-off instead of requested destination (USE-3, USE-7).** The under-100 m cut removes 2,364 obvious round trips correctly, following the nyc/pkdd precedent. Destination changes and multi-stop rides farther than 100 m remain (detour p99 11.6×). They inflate the RMSE tail and carry a little post-trip information through `str_distance_km`. They cannot be removed without filtering on post-trip information (forbidden). Already named as unverified in `curation_comments`.
3. **Masked coordinates.** Random displacement of unknown size blurs the spatial signal my production model has. This underestimates achievable skill but does not distort the ranking much.
4. **Prediction point is pickup, not order.** In-ride ETA is a valid decision. An order-time quote would also need driver arrival time, which is absent. It should be stated as the in-ride ETA in `use_case` ("at trip start" is already close).
5. **Short history (one month, 8 to 16 days of training).** Weekly seasonality is barely learnable, and there is drift around 01-27. This is a scope limit, already stated.
6. **Provenance (2023 vs. 2024, participant mirror) and one-hour weather lag.** Neither changes the decision; both are accepted by the curator.

**What an expert would change**

- Add to `fit_reason` and `use_case`: "no routing-engine route or ETA ships; the task is an ETA from geometry, time and weather" (USE-8). This is the gap that matters most to a practitioner, and the record does not yet name it.
- Name the prediction point as pickup (`lcl_start_transporting_dttm`) in `use_case`: "an in-ride arrival estimate".
- Keep RMSE under MET-4. Note in the metric block or the notes that about 1% of test trips carry 54 to 66% of the squared error, so the ranking leans on the tail. Name MAE as the practitioner's alternative.
- Do not filter long or slow rides: any such cut reads the target or the post-trip distance.

**Sources**

- Zindi API page: https://api.zindi.world/v1/competitions/2024-lusaka-mobility-prediction-hackathon (metric quote; "predict travel and arrival times of its partners' drivers").
- Raw `Train.csv` columns (`lcl_start_transporting_dttm`, `transporting_distance_fact_km`).
- Rules: `.claude/skills/knowledge-curation/references/use_case.md` (USE-3, USE-5, USE-6, USE-7, USE-8) and `metrics.md` (MET-1, MET-3, MET-4, MET-10).
- Precedents: `nyc_taxi_trip_duration_1m`, `pkdd_15_taxi_trip_time_prediction_ii_1m`, `maps_router_eta`.
- My measurement uses the three declared cutoffs with a one-day gap, with hour and weekday added and no weather, so its baseline is not the panel's.

</details>

<details><summary>Blind review</summary>

**Verdict:** include. It is a real ride-hailing travel-time task on real Yango trip data, with no leaking column and an honest time-ordered split, and it carries useful signal. Two things to fix: the dataset description should state that the dates are January 2023, not 2024, and the panel should decide whether RMSE is right for a target with heavy outliers.

**What the task is.** A ride-hailing platform (Yango, in Lusaka) estimates how long a trip will take when it starts. That estimate drives the arrival time shown to the rider, fare checks and dispatch. The source defines the target as "Actual travel time in minutes" (VariableDefinitions.csv). The Zindi page says "predict ride times based on the provided trip and weather data", scored by RMSE. This is a real and common use.

**Concerns, most serious first**

1. **The target has heavy noise and outliers, and RMSE is sensitive to them.**
   - Target: median 10.8 min, 99th percentile 55 min, 99.9th percentile 112 min, maximum 788 min. 92 trips are over 120 min.
   - Implied straight-line speed: 1st percentile 1 km/h, 0.1th percentile 0.17 km/h, and 41 trips above 100 km/h. Some "trips" probably include waiting time or detours.
   - The source also moved every coordinate by a random amount: "Start and end coordinates were geomasked … each point was moved a random distance in a random direction." So location carries extra noise by design.
   - Effect: a LightGBM baseline (all features plus hour and day of week, first 80% in time to train, last 20% to test) gets RMSE 10.65 and R² 0.30. A constant prediction gets RMSE 12.70. Straight-line distance alone gets R² 0.23.
   - So the task is not trivial, but the room between methods is narrow, and a few outliers could swing the RMSE ranking.
   - Change: either score with MAE or RMSLE, or cap or flag targets above about 180 min and document it. Do not drop them silently.

2. **The year in the description is wrong.** The Zindi page says the data is "trips via the Yango platform from January 2024". The raw Train.csv and Lusaka_weather.csv, and this table, all run 2023-01-01 to 2023-02-01. The data itself is consistent, so this is a documentation error. Change: record the dates as January 2023 in the metadata.

3. **The leaking column was removed correctly; keep it that way.**
   - The raw Train.csv and Test.csv include `transporting_distance_fact_km`, defined as "Actual travel distance". That is only known after the trip ends, yet the competition supplied it as an input even in Test.csv.
   - The prepared table has dropped it, which is the right call for honest arrival-time prediction. Note that published Zindi leaderboard scores used this column, so they are not comparable with scores on this table.
   - Also removed: 2,385 of 112,760 training rows (110,375 kept). All of them have straight-line distance under 0.1 km (median 0.03 km), and their median target is 22 min, so they are essentially round trips. Dropping them is sensible but should be documented as a filter.

4. **The time-ordered split covers only one month.**
   - The data spans 32 days at about 3,450 trips per day; the first day (Jan 1) has only 70 trips. With 3 test windows, each covers a few days.
   - This matches real use (train on the past, predict the next days) but cannot capture seasonal drift. With roughly 20k+ rows per window, there is enough data to score.
   - The Zindi test file (48k rows) has no labels, so it cannot be used. Only the labelled train file is here. That is correct.

5. **Weather join: honest, but weak signal.**
   - Weather is hourly and the same for every trip in a given hour. I checked the alignment: a trip at 02:03 gets the 01:00 weather record (temp 19.14, previous-hour rain 0.0372 mm). The join looks backward, so nothing from the future leaks in.
   - The 23 missing weather values are all trips on Feb 1 at 01:00–02:00, which fall after the weather file ends (Jan 31 23:00). That is a genuine gap and is correctly left as NaN.
   - `precipitation_type` reads "Rain" in 87% of rows, often with tiny amounts (0.04 mm). This looks like model or reanalysis data rather than a rain gauge, so it carries little information. Acceptable.

6. **Preparation details (minor).**
   - Data types are sensible: float coordinates, a 2-level categorical, and a datetime.
   - `trip_start` is a raw datetime. Methods need hour of day and day of week derived from it, so the harness must handle datetimes consistently, or those features should be added up front.
   - `trip_id` was dropped (good).
   - No duplicates: 0 exact duplicate rows, 0 duplicates on features alone, 0 duplicate coordinate quadruples.

**Is the data real?** Yes. The raw file has realistic coordinates around Lusaka, a daily volume pattern, and a target and distance spread typical of ride-hailing. Nothing suggests generated data.

**What I could not check**
- Whether trip time includes pickup or waiting time. The definition only says "actual travel time", so the slowest trips cannot be explained.
- How far the coordinates were moved by geomasking.
- The exact boundaries of the 3 test windows used by the harness (I used a single 80/20 time split instead).
- Licensing: the page says the data is "Private property of Yango", so redistribution terms should be confirmed.

To compare the clean-room table with the source, I downloaded the public Train.csv, Test.csv and Lusaka_weather.csv from the GitHub mirror. I opened no files outside the clean room and the public web.

</details>

<details><summary>Task gamer</summary>

**Verdict:** I found no exploit that beats the noise floor. Nothing in the kit gains more than about ±0.05 RMSE over an untuned LightGBM, so this task is hard to game.

**Honest baseline:** untuned LightGBM on the 9 features, with `trip_start` expanded to hour, day of week and a timestamp. RMSE on r0f0 / r1f0 / r2f0 is **8.949 / 11.305 / 8.961**. I refit it three times with a column of random numbers added, which gives 8.917–8.933 / 11.253–11.318 / 8.989–9.021. That puts the noise at about ±0.05 per split.

**Exploits**

| # | Exploit | Script | Honest score | Exploited score | Gain (per split, range) | A deployed model has it? | Fix |
|---|---|---|---|---|---|---|---|
| 1 | Trip counts in the next 15 and 60 min, which need test rows from after the prediction point | density.py | 8.949 / 11.305 / 8.961 | 8.948 / 11.356 / 9.009 | +0.00 to −0.05 (no gain) | No | None needed |
| 2 | Weather of the following 1–2 hours, read off later test rows | futweather.py | same | 8.937 / 11.269 / 9.018 | −0.06 to +0.04 (noise) | No | None needed |
| 3 | Whole-day trip count, using the test day's total | density.py | same | 8.932 / 11.292 / 8.986 | ±0.03 (noise) | No | None needed |

None of the three is a real gain; they are listed so the next reader knows what was tried.

**Flaws that hurt an honest model**

| What | Honest choice | Baseline | Honest variant | Gain |
|---|---|---|---|---|
| A heavy target tail: up to 788 min, with 10–11 test trips per split over 120 min that make up 16–29% of the test squared error | Drop training rows with Target > 120 | 8.949 / 11.305 / 8.961 | 8.874 / 11.207 / 8.935 | 0.03–0.10 (borderline against ±0.05 noise) |

These trips look real (very slow or abandoned rides), and a deployed model would train on them too. I don't count this as a task flaw. Two other filters scored worse:
- Dropping training rows with Target > 240 changed little (8.923 / 11.286 / 8.990).
- Dropping trips slower than 1 km/h made all three splits worse (9.094 / 11.374 / 9.114).

**How the kit compares with the published source**

I compared the kit with `Train.csv` from the GitHub mirror.
- **Row lookup:** looking rows up in the published file works. All 110,375 kit rows match it exactly on coordinates, time and Target.
- **Dropped column:** the kit removes `transporting_distance_fact_km`, the actual distance driven. It is only known once the trip ends, and the original Zindi `Test.csv` shipped it. Dropping it closes the competition's main post-outcome leak.
- **Dropped rows:** the kit removes 2,385 trips with `str_distance_km` < 0.1. These are near-round trips, with median Target 30.8 min against 14.2 overall. The cut uses a feature value, so it applies equally to train and test and is not a leak.
- **Unchanged:** values are not rounded, and the coordinates are already masked in the source.
- **Weather join:** checked against `Lusaka_weather.csv`, a trip in hour h gets the record stamped h−1 in 99.7% of hours. That matches "the previous hour's weather".

**Attacks that found nothing**

- **Formats**
  - Target is a whole number of seconds divided by 60 and rounded to 2 decimals. Its last digit is uniform over {0,2,3,5,7,8}. Target means for 1 vs 2 decimals are 13.70 vs 13.82.
  - The second of the end time (start + Target) is uniform. The start second is uniform; its share of :00 is 1.7%, close to the 1/60 expected.
  - Coordinates have 10–15 decimals (masked floats) and every one is unique. The last digit of `str_distance_km` is uniform.
  - Missing values: the 3 weather columns are null together on 23 rows only.
- **Masked coordinates:** `str_distance_km` minus the haversine of the masked points is uniform noise of ±0.12 km. Its correlation with the target is 0.007.
- **Order and ids:** rows are sorted by `trip_start`. Lag-1 target correlation is 0.037. There are no ids.
- **Driver or rider chains** (a later origin near this trip's destination, used to bound the duration). With search radii of 50, 100 and 200 m, the correlation between the gap and Target is −0.01 to −0.06. The gap is at least Target in only 78–88% of cases, so these are random neighbours, not chains.
- **Copies across the split:**
  - No exact duplicates of coordinates or origins.
  - The nearest training route within 100 m covers 14–18% of test rows. Its label correlates 0.39–0.47 with the test label, with RMSE 9.8–10.7. That is ordinary repeat-route signal a deployed model has, and it is weaker than the model.
  - About 3–5% of test rows have a near copy elsewhere in the test window, a median of about 1 day apart.
- **Training rows:**
  - Each split leaves a one-day gap before the test window. The longest trip is 13 h, so every training label is known before the test starts.
  - The daily mean target is flat on weekdays (about 14–15) and lower on Sundays (about 11). The test windows don't differ in level.
  - The 70 trips from 1 Feb (mean 9.8) fall in the r0f0 test window only.
- **Test composition:** the past 15 and 60 min trip counts (8.909 / 11.265 / 9.017) are deployable signal and also within noise.
- **Timestamp:** dropping it gives 8.964 / 11.253 / 8.985, within noise.
- **Transforms over all rows, lookups:** no standardised, ranked or binned columns. No formula reproduces the target; the best features (distance, hour) leave about 9 min of RMSE.

**Not checked**

- I did not tune the honest model, so the honest ceiling may be somewhat below 8.9 / 11.2 / 8.9.
- I did not fit a train-vs-test classifier. With a temporal split it would only find the timestamp.
- Zindi's leaderboard and winning code were not reachable. Press coverage says the winner used a random forest on weather and distance features, and mentions no leak.

Sources:
- [Zindi competition page](https://zindi.africa/competitions/2024-lusaka-mobility-prediction-hackathon)
- [TechTrends: winners announcement](https://techtrends.co.zm/?p=94334)
- [GitHub mirror of the data](https://github.com/Mwandamena/yango-hackathon/tree/2fa7817be0740ea1739143ea6e61a28d6cf1462d/data)

</details>

<details><summary>Precedent check</summary>

**Precedent check: 2024_lusaka_mobility_prediction_hackathon (2026-11-04)**

**Summary.** Siblings (Accra 2025, Maputo) and ride-time precedents (NYC taxi, PKDD-15, maps_router_eta, yassir): against all of them, the 2026-11-04 decisions are consistent: the 100 m cut, the domain, and RMSE on minutes. There is one real departure with no stated reason, which is minor: trips with an impossible straight-line speed are kept, while pkdd drops them. One kept tail needs the curator to see it: 20 trips over 3 h, which NYC caps and which hold 11.8% of the target's squared spread. One recorded reason is slightly inaccurate (the metric analogy). The decision register raises no flag on this dataset. It parses 6 decisions, and only the 100 m cut carries a rule ID (USE-7).

**Per decision, ranked**

**1. 100 m cut (CC 2026-11-04, Lennart, USE-7 Must): consistent.**
- Precedents:
  - `nyc_taxi_trip_duration_1m`: reopened 2026-10-26 to drop trips ending within 100 m, `MIN_STRAIGHT_LINE_KM = 0.1`.
  - `pkdd_15_taxi_trip_time_prediction_ii_1m`: issue 2, 2026-10-26.
  - Both are listed in the USE-7 Cases table at `.claude/skills/knowledge-curation/references/use_case.md:165`.
- The facts match:
  - The cut rests on an input, not on the target.
  - The dropped trips are round trips, not short rides. Lusaka: median 22.1 min, 93% over 5 min, 16% of squared spread. pkdd: median 555 s, 57% over 5 min, 17% of squared spread.
- One difference strengthens the call. Lusaka cuts on `str_distance_km`, which the source computes from the original, unmasked points. So the cut is exact even though the coordinates are geomasked. NYC and pkdd use haversine on recorded coordinates. This is written in the curation_comments.
- No drift: all of Lennart's USE-7 calls since 2026-10-26 use the same radius. The 2026-10-20 nyc panel had kept these trips, but the 2026-10-26 reopen explicitly superseded that.
- Bookkeeping gap: Lusaka is not yet in the USE-7 Cases table (use_case.md:165) or in the rule's Cases line (use_case.md:55). Adding it there makes it an `applied` row.

**2. Domain `industry & manufacturing` (CC 2026-11-04): consistent.**
- Matches `nyc_taxi_trip_duration_1m` (CC 2026-10-22), `pkdd_15` (CC 2026-10-26), `maps_router_eta_1m`, `delivery_eta_1m` and `chicago_taxi_trip_duration`. The nyc dataset.py says "transport has no value of its own".
- Follow-on: four unbuilt sibling or precedent records still say `technology & internet`: `2025_accra_mobility_prediction_hackathon_powered`, `2025_maputo_mobility_prediction_hackathon_powered_by_yango`, `yassir_eta_prediction_challenge` and `yassir_eta_prediction_challenge_for_azubian`. All are AI-filled and unverified, so this is not a conflict yet. They should be aligned whenever they are promoted ("Would I decide the same for its siblings?").

**3. Target in minutes, RMSE, identity transform (CC 2026-11-04, MET-4 Should / MET-3 Must): consistent, but the recorded reason is inaccurate.**
- MET-4 says to declare the competition's metric. Zindi's Evaluation tab says RMSE. This matches how nyc and pkdd keep their competitions' RMSLE (2026-10-21) and the "zillow_prize mae kept" row of Tensions.
- MET-3 allows a log1p target but does not require one, so raw minutes is fine.
- The record's reason ("as the other RMSE-scored ETA datasets") does not hold. No shipped ETA dataset scores RMSE on raw time:

  | Dataset | Metric |
  |---|---|
  | `delivery_eta_1m` | RMSE on log minutes (TabReD) |
  | `maps_router_eta_1m` | RMSE on log seconds per km (TabReD) |
  | `nyc_taxi_trip_duration_1m`, `pkdd_15` | RMSLE |

- The real reason is MET-4: the source's metric on the source's scale, as each precedent follows its own source.
- The closest same-kind case is Zindi ETA with RMSE on raw seconds: `yassir_eta_prediction_challenge`, Accra and Maputo (all screened, MET-4). Lusaka now sets the precedent for them.
- Suggested fix: reword the CC's reason. No change to the decision.

**4. Long trips kept (curation_comments, written 2026-10-29, not touched on 2026-11-04): departs from NYC with a stated reason; reasonable under CLEAN-11 (Should, amended 2026-10-21).**
- `nyc_taxi_trip_duration_1m` drops trips over 3 h (`MAX_SECONDS`), but on measured evidence that they are impossible: a broken-clock cluster just under 24 h with few-minute fares. Lusaka shows no such evidence and states "neither the source nor the inspected values proves they are errors". CLEAN-11 keeps unusual values, so this is not a departure.
- I measured the effect on the raw files:
  - 20 of 110,375 kept trips last over 180 min, up to 788 min for 1.1 km in a straight line.
  - They hold **11.8% of the target's squared spread**, comparable to the 16% the 100 m cut removed.
  - 8 of them start on or after 2023-01-21, inside the test windows.
- Because the metric is raw-minute RMSE, not RMSLE as in NYC, they weigh far more here than they would there.
- This is informational for the curator. It is not a consistency failure.

**5. Impossible straight-line speeds kept: departs from pkdd without a reason.**
- `pkdd_15_taxi_trip_time_prediction_ii_1m` drops trips whose straight line from start to end implies over 120 km/h (`MAX_STRAIGHT_LINE_KMH = 120`: "a GPS jump or a gap").
- In Lusaka, 19 kept trips exceed 120 km/h and 10 exceed 150 km/h, for example 3.67 km in 1.07 min (206 km/h). Because `str_distance_km` uses the original points, these speeds are exact.
- Under CLEAN-11 an impossible target becomes missing, and a row with a missing target leaves. Nothing in the definition or record addresses these rows.
- The effect is tiny: about 0.000 of the squared spread, with 4 of the trips in the test windows.

**6. Other decisions: consistent.**
- 21 rows without a start time dropped; 23 rides with no weather kept as missing. This matches USE-7's second sentence ("Missing values of the other inputs stay missing").
- Temporal split: 3 windows with a 1-day gap and `min_train_fraction=0.5`. This matches nyc (3 weekly windows, 1-day gap) and pkdd (monthly windows, 1-day gap) and the SPLIT-14 floor. The window is 4 days instead of 7 because the extract covers only one month, which is stated in splits_comment.
- One city of three kept: Accra and Maputo are marked `2nd Tier` with "one city is enough". This matches PROV-6 and PROV-7 (same task and publisher, no distinct task). Neither sibling contradicts the Lusaka acceptance.
- Myunghwan's 2026-10-29 calls ("approximate version is fine"; keep the calendar) are not contradicted by Lennart's 2026-11-04 calls. There is no curator drift.
- Stale line: the record's AI line of 2026-11-04 says "no panel ran for this dataset". This pass is that panel, so the line will need superseding.

**No third exception or amendment is due.** USE-7 has its third and fourth applied cases (bias_correction, nyc, pkdd, lusaka), but none is an exception. CLEAN-11 is unchanged.

**Reflection prompt (one, for decision 5)**

```text
**Consistency check (AI, 2026-11-04):** your call on 2024_lusaka_mobility_prediction_hackathon (keep the 19 trips
whose straight-line distance over the ride time exceeds 120 km/h, up to 206 km/h; computed on the unmasked
`str_distance_km`) differs from pkdd_15_taxi_trip_time_prediction_ii_1m (drops trips faster than 120 km/h in a
straight line as a GPS jump or gap, 2026-10-20/26, the same mechanism: an impossible start-to-end speed, CLEAN-11).
What sets Lusaka apart?
(a) the source already removed "excessively short trips" and records an app-side duration, not GPS points, so a
    fast trip may be a timing error the source chose to keep; the 19 rows hold ~0.0% of the squared spread,
    recorded as kept with a note; (b) treat Lusaka like pkdd: drop trips over 120 km/h in a straight line;
(c) reopen pkdd to match Lusaka; (d) change CLEAN-11 (an amendment).
```

For decision 4, the curator's own question is whether to keep the 20 trips over 3 h (11.8% of the squared spread, 8 in the test windows) under CLEAN-11's "unusual values stay". That stated reason is reasonable, so I give no prompt. The curator should still weigh it against nyc's 3 h cap, because raw-minute RMSE is the metric here.

</details>

<details><summary>Advocate</summary>

Opening brief (advocate). Verdict sought: **ship after wording changes.** No re-split, no re-target, no new row filter is needed for validity.

**1. The competition's leak is gone, and nobody could game what is left (P4; LEAK-10 Must, LEAK-16, SPLIT-9 Must).**
- **Evidence for the fix.** Zindi's Test.csv ships `transporting_distance_fact_km`, the distance actually driven, which is known only after the trip. The definition drops it (claim, column and blind audits all agree). The practitioner measured what it was worth: RMSE falls 18 to 27% when it is added back. So the source task really was leaky, and ours is not.
- **No exploit found.** The task gamer tried future trip density, future weather, whole-day counts, driver chains, near copies, format artifacts and the timestamp. None beat the ±0.05 RMSE noise floor.
- **Labels are mature.** With the 1-day gap, 0 training trips end after a window starts (without it: 24 / 6 / 13). Removing the gap moves RMSE by at most 0.021, so the gap hides no shortcut either way.
- **No copies.** Duplicate coordinates, duplicate ids and train/test id overlap are all 0.
- This is the top-ranked block, every Must here holds, and no agent disputes it.

**2. The use case is real, and the curator has already accepted its approximate fit (P3; USE-5, USE-8; curator CC 2026-10-29).**
- The target is "Actual travel time in minutes" (VariableDefinitions.csv), which is what an ETA owner acts on.
- The practitioner, speaking as the Yango ETA owner, agrees with `fit="approximate"`. One row is one displayed ETA, and the test is later days after a refit.
- **The real gap:** no router route or router ETA ships. Mildest remedy: one sentence in `fit_reason` and `use_case`: "no routing-engine route or ETA; an in-ride ETA from geometry, time and weather". That is a note, not grounds to reject. The Tensions row "a real task against imperfect cleaning" says keep the task, and USE-8 lets an approximate fit stand.

**3. The split mirrors deployment and meets the floor exactly (P4; SPLIT-6, SPLIT-11, SPLIT-14 Must, SPLIT-21).**
- **Shape.** Three expanding windows. The train shares are 86.0%, 72.4% and 59.7%. A fourth window would hold 0.478, under the 0.5 floor, so three is the maximum.
- **Regime.** Temporal, with no entity id. A random split would be mildly optimistic: skill 0.198 against 0.182.
- **Precedents.** It matches nyc and pkdd (1-day gap, ≥3 windows).
- **Concede (split auditor):** the windows hold unequal weekend shares. Remedy: one sentence in `splits_comment`. 7-day windows would break SPLIT-14, and choosing windows by score is forbidden by SPLIT-21.
- **The "01-27 dip" is a misread.** It is the Sunday cycle on 01-29 (all five Sundays sit at 11.07 to 12.11). Two auditors measured this. The practitioner's "drift" reading inherits the prep report's error. Only the checklist note needs correcting.
- **The partial last day (70 rows) moves RMSE by 0.002.**

**4. RMSE on minutes is the right declared metric; only the recorded reason is wrong (P6; MET-4 Should, MET-2 Must, MET-10 Weigh; CC 2026-11-04).**
- Zindi's page says "The evaluation metric for this competition is Root Mean Squared Error". It was re-read twice, and every fold can be scored (dummy 11.2 / 13.3 / 11.0).
- MET-4 overrules a competition's metric only on evidence that it is "biased or wrong". Tail dominance (the top 1% of errors hold 54 to 66% of squared error) is a measured weakness, not a bias. Even the practitioner who prefers MAE says to keep RMSE.
- **Concede (precedent checker):** the CC's reason "as the other RMSE-scored ETA datasets" is false. No shipped ETA dataset scores RMSE on raw time. Fix: reword the reason to MET-4. Add the tail share to the notes as the MET-10 resolution factor. The decision itself stays.

**5. Long, slow trips: keep them, but correct the sentence that says nothing points to errors (P7; CLEAN-11 Should; P4 consistency, check 2).**
- **Concede (claim auditor):** "neither … the inspected values proves they are errors" overstates. The 788-min trip covered 20.2 km driven and 1.12 km straight-line (1.54 km/h). It holds 21% of window f1's dummy squared error. The sentence must change.
- **What sets this case apart from nyc's 3 h cap.** That cap rests on a measured fact: "a cluster just below 24 h … whose metered fares are those of trips of a few minutes" (nyc `dataset.py`, `MAX_SECONDS`). Lusaka has no such cluster. There are 20 trips over 3 h, spread out, the longest at 13 h, and all have positive driven distances. So the nyc fact is absent, and CLEAN-11's "values that are only unusual stay" applies.
- **Effect check.** The task gamer found that dropping training rows over 120 min gains only 0.03 to 0.10, which is borderline against noise. Dropping trips under 1 km/h made all three splits worse. The practitioner adds that any cut on duration or speed reads the target or the post-trip distance. The precedent checker classes this as "not a consistency failure".
- **The narrow residual point.** The 788-min row is in the f1 test window, so CLEAN-11's "training period only" route does not apply. Dropping it would need a finding that the value is impossible (CLEAN-11 → missing → CLEAN-15). That is a curator weighing call on one row, not a reason to hold the dataset.
- **Mildest remedy:** reword the sentence, record the tail shares (11.8% of squared spread; 16.9 / 28.8 / 15.7% per window), and put the one-row question to the curator.

**6. The 100 m cut is right, but its wording needs fixing (P3; USE-7 Must, applied as in nyc and pkdd).**
- **Concede (claim auditor):** "a cut on an input known at booking" is wrong as worded. For the round trips the recorded end is the drop-off.
- **Why the cut still holds.** It is on a feature value applied equally to train and test, not on the target. It is consistent with the precedents (median 22.1 min, 16% of spread, against pkdd's 17%). It is exact on unmasked distances.
- **The approximation is supported by the data.** The column auditor found 1,756 kept trips that drove shorter than the straight line. For those, the recorded end is a requested destination, not the drop-off, which supports the accepted stand-in.
- **Remedy (wording only):**
  - say "a cut on the recorded endpoint, which for these rows is not a booked destination";
  - add the mixed-meaning sentence with the 1,756 / 290 counts;
  - add Lusaka to the USE-7 Cases table.

**7. Small consistency and wording items; none blocks shipping.**
- **Impossible straight-line speeds (CLEAN-11, consistency with pkdd).** 19 trips exceed 120 km/h, and their effect is about 0.000 of the spread. I concede pkdd dropped the same mechanism. The cheapest consistent fix is to drop these rows as pkdd did (P7: "fixed when the fix is cheap and safe"), or keep them with a note under the precedent checker's option (a). The curator picks.
- **Weather timezone (LEAK-10, weak).** The diurnal curve hints at UTC, but the trip curve looks local. Cross-correlation is flat from −4 h to +4 h, and the weather columns' single-feature skill is about 0. Remedy: a note saying the timezone is unverified, or a 3 h lag, which costs no measured skill.
- **Wording fixes:**
  - "byte lengths match" becomes "sizes match the listing's rounded sizes" (PROV-10);
  - the stale lines "no public solution found" and "no panel ran" get superseded.
- The 2023/2024 date conflict the blind reviewer raised is already stated in `row` and `curation_comments`.

**Judgment record.**
- **Verdict:** ship after changes (wording only, plus an optional cut of 19 rows).
- **Validity:** LEAK-10 triggered and fixed; SPLIT-9 and SPLIT-14 hold; USE-7 applied; USE-8 approximate fit accepted.
- **Value:** MET-4 holds; TP shows real, non-trivial skill (0.18).
- **Quality:** CLEAN-11 keeps the long trips with a note.
- **For the curator:**
  - one weighing call on the 788-min row;
  - one consistency prompt on speeds over 120 km/h.

</details>

<details><summary>Critic</summary>

**Opening brief (opponent): `2024_lusaka_mobility_prediction_hackathon`**

My position: do not ship it as defined. It can ship after the changes below. None of them calls for exclusion. I re-ran two counts on the pinned Train.csv and Lusaka_weather.csv, and I name the results where they settle a disagreement between the reports.

**1. The fit does not name the gap that matters most to the task. P3, USE-8 (Must), informed by USE-6.**
- Problem: every production ETA has a routing engine's route and ETA at pickup. This data has neither, so the task is "an ETA from geometry, time and weather", not "refine the router". `fit_reason` names only the endpoint and weather stand-ins.
- Evidence: the domain practitioner used realised `transporting_distance_fact_km` as an upper-bound stand-in for the planned route. RMSE fell by 18 to 27% per window (8.96→6.57, 11.09→9.08, 8.86→6.76). The prediction point is pickup (`lcl_start_transporting_dttm`), not the order.
- Remedy (fix the text): add to `fit_reason` and `use_case` that no route or router ETA ships, and call the task an in-ride arrival estimate at pickup.

**2. The 100 m filter is justified with a false sentence, and the destination means two different things. P3/P4, USE-3 and LEAK-1 (Should here, within the accepted approximation).**
- Problem: `curation_comments` says the cut "is on an input known at booking". That is refuted. The 2,364 dropped trips end within 0.1 km in a straight line but drove a median 4.5 km. So for those rows the recorded end is the drop-off point, which is known only after the ride.
- The other meaning also occurs: 1,756 kept trips (1.6%) drove less than 0.9× the straight line, and 290 drove less than 0.5×. There the end looks like a requested destination the rider never reached.
- `str_distance_km` therefore carries some post-trip location in some rows. The amount is small (2.1% of rows were dropped, and the destination is otherwise a fair stand-in), so this is not a leak to remove. Filtering on driven distance would select rows on the outcome, which is worse.
- Remedy (note and rewording, no code change):
  - Reword to "a cut on the recorded endpoint, which for these rows is not a booked destination".
  - Add one sentence to the endpoint bullet saying both meanings occur, with the 1,756 and 290 counts.
  - Fix the `Decision.why` text "no destination a passenger would book" the same way.

**3. The weather may be on UTC, which would make the one-hour lag look up to about 1.5 h ahead. P4, LEAK-10 (weak, so Should) and LEAK-1.**
- Problem: the definition joins the weather stamped floor(start) − 1 h and says it "never" uses the current hour. That holds only if the weather stamps are local time.
- Evidence (my recount of the weather file):
  - Mean temperature bottoms at stamps 02 to 04 (18.80 to 18.82). It jumps to 19.89 at stamp 05, before the January sunrise in Lusaka at about 05:50. It peaks at 12 to 13 (24.94 to 24.97). Shifted to UTC+2, the curve looks physical.
  - The two files cover different spans. The trips run 2023-01-01 02:03 to 2023-02-01 02:09, which is a UTC calendar month shown in local time. The weather runs 00:00 Jan 1 to 23:00 Jan 31 on its own stamps. That fits stamps in UTC (inference).
  - On UTC, a trip at 10:30 local gets the 09:00 stamp, which is 11:00 local. Its "precipitation in the past hour" then overlaps the ride.
- Against it: the trip-hour pattern is local, and the column auditor measured no skill from the weather columns (−0.014 to 0.00003). The task-gamer found future weather gives no gain beyond noise. So this is weak, not a Must.
- Remedy (the cheapest safe fix): lag the weather by 3 h, which is safe on either clock and costs no measured skill. The fallback is a note that the weather timezone is unverified, with this evidence, plus dropping the word "never" from the claim.

**4. RMSE on raw minutes is decided by a few rows, and two stated reasons for keeping it are false. P6, MET-2 (Must check) and MET-4 (Should), with the principles' consistency check 2.**
- Effect:
  - In window f1 (2023-01-25), one trip holds 21% of the dummy model's squared error: 788.07 min for 20.2 km driven and 1.12 km straight-line, 1.54 km/h over 13 h. Dummy RMSE is 13.331 with that row and 11.848 without it.
  - The top 0.1% of rows hold 25 to 43% of LightGBM's squared error, and the top 1% hold 54 to 66%.
  - 20 kept trips run over 3 h, holding 11.8% of the target's squared spread, and 8 of them fall in test windows.
- First false sentence: `curation_comments` keeps all durations because "neither the source nor the inspected values proves they are errors". The inspected values say otherwise: four kept trips over 239 min ran under 2 km/h, the slowest at 0.31 km/h.
- Precedent: nyc_taxi_trip_duration_1m dropped trips over 3 h as broken clocks at walking speed, the same mechanism. Lusaka took nyc's 100 m radius but not its 3 h cap, with no fact recorded that sets it apart.
- Second false sentence: the CC reason "as the other RMSE-scored ETA datasets" is wrong. delivery_eta and maps_router_eta score RMSE on log targets, and nyc and pkdd score RMSLE. The real basis is MET-4.
- Remedy (I do not ask for a metric change, since MET-4 holds without proof the metric was gamed or is biased):
  - Correct both sentences.
  - MET-4 requires a measured weakness to be written in the notes with its numbers, so record the tail shares.
  - Put a consistency prompt to the curator: (a) drop trips over 3 h as nyc does, or (b) keep them as a recorded exception naming the fact. One candidate fact: the source scored them in its own RMSE.
- CLEAN-11 lets a single extreme target leave only from the training period, so option (a) has to rest on "impossible value" reasoning (an unclosed trip), not on the single-extreme clause.

**5. Trips with impossible straight-line speeds are kept, unlike in pkdd. P7, CLEAN-11 (Should), with CLEAN-15 (Must) once a target is made missing.**
- Evidence (my recount): 19 kept trips exceed 120 km/h, 10 exceed 150 km/h, and the maximum is 416.2 km/h (8.879 km in 1.28 min). The precedent-checker's prompt says "up to 206 km/h", which is wrong and should be corrected before it goes to the curator.
- Because `str_distance_km` uses the original points, these speeds are exact. Either the target or the endpoint is wrong. pkdd drops trips over 120 km/h in a straight line.
- Effect on the score is about 0.
- Remedy: a consistency prompt with the corrected maximum. Either drop them as pkdd does, or keep them with a note. This is a quality point only.

**6. Evidence and record text overstate or are stale. P5, PROV (Should, wording); writing.md.**
- `download_description` and the record say the files' "byte lengths match the organizer listing". The files are 15,620,473 B, 6,433,913 B and 48,742 B. The listing says 15.6 MB, 6.4 MB and 49 KB, so they match only to rounded precision. Reword to that.
- Supersede stale text:
  - "no panel ran for this dataset" (2026-11-04).
  - "no public solution found" (screening).
- Where the panel or REVIEW text carries the "2023-01-27 drift dip", correct it: the dip is Sunday 2023-01-29, part of a weekly cycle (all five Sundays 11.07 to 12.11 min against 13.70 to 14.67 on other days). The practitioner's "drift around 01-27" rests on the same error.

**7. The windows hold unequal weekend shares. P4, SPLIT-20 (Should; a note only).**
- f1 contains no Sunday. f0 has Sunday to Tuesday plus 70 Wednesday rows, and f2 has Saturday to Tuesday. No 7-day window design passes SPLIT-14's 0.5 training floor, so a re-split is not available.
- Remedy: one sentence in `splits_comment` that the windows hold different weekday mixes and the Sunday drop is weekly, not drift.

**Judgment record**
```text
Verdict: ship after changes.
Validity: USE-8 triggered (fit_reason misses the no-router gap), fix text; USE-3/LEAK-1 claim "known at booking" refuted, reword + note (mixed endpoint meaning); LEAK-10 weak (weather clock may be UTC), fix: 3 h lag; SPLIT-1/SPLIT-9 hold; LEAK-10 driven distance fixed.
Value: MET-4 holds; MET-2 meaning holds only with the tail documented (f1: one row 21%).
Quality: CLEAN-11 departures from nyc (3 h) and pkdd (120 km/h) need the curator's answer; wording fixes (bytes, stale lines).
For the curator: issue 4 and 5, consistency prompts; issue 3, the lag.
```

</details>

<details><summary>Advocate rebuttal</summary>

**Rebuttal (advocate): `2024_lusaka_mobility_prediction_hackathon`**

**Where we stand.** The critic and I agree on the verdict ("ship after changes") and on what is wrong. Neither of us asks for a re-split, a new target, a metric change or exclusion. Points 1, 2, 6 and 7 are full concessions. Points 4 and 5 are concessions with a dispute over which option the curator should be steered to. Point 3 is a dispute: there is a new fact from the source's own dictionary.

**1. The fit text does not name the missing router (USE-8): conceded.**
- This is my point 2. The practitioner's measurement backs it: adding the driven-distance proxy cuts RMSE by 18 to 27% (8.96→6.57, 11.09→9.08, 8.86→6.76).
- What follows: a text fix to `fit_reason` and `use_case`. Name the task "an in-ride arrival estimate at pickup, from geometry, time and weather; no routing-engine route or ETA ships".
- `fit="approximate"` stays (USE-8 lets an approximate fit stand; curator decision 2026-10-29).

**2. "Known at booking" is false, and the endpoint means two things (USE-3, LEAK-1, Should): conceded.**
- This is my point 6. I also accept the critic's extra item: reword `Decision.why` ("no destination a passenger would book") the same way.
- The cut itself stays (USE-7 Must, the nyc/pkdd radius):
  - It is on a feature, applied equally to train and test.
  - It is exact on unmasked `str_distance_km`.
  - Filtering on driven distance instead would select rows on the outcome, as both the critic and the column auditor say.
- Also add Lusaka to the USE-7 Cases table (use_case.md:165).

**3. Weather on UTC, so lag it 3 h (LEAK-10, weak): disputed. A note is enough, and the 1 h lag stays.**
- **New fact.** The source's own VariableDefinitions.csv labels the weather stamp `Weather,lcl_datetime,Local date and time`. It uses the same "Local" wording as the trip start (`lcl_start_transporting_dt`). So the publisher says the two clocks match. The critic's case rests on inference only: a diurnal curve from reanalysis-like values, and file spans.
- **Evidence weighed against that statement:**
  - The trip-hour pattern is local (peaks 07–08 and 16–17).
  - Cross-correlation of trip-pace residuals with precipitation is flat from −4 h to +4 h (0.025 to 0.062).
  - Single-feature skill of the weather columns is −0.021 to 0.00003.
  - The task gamer's real future-weather feature (+1 to 2 h) moved RMSE only within ±0.05 noise.
  - So even if the critic is right, the lookahead carries no measurable signal.
- **Rule.** P4 needs a mechanism plus evidence. Here the source's statement contradicts the mechanism, and the effect is measured at zero.
- **Remedy ladder.** The mildest remedy that resolves this is a note. Write: "weather stamps are local per the source dictionary; the diurnal temperature curve suggests UTC; unverified; weather carries no measured skill". Change "never the current-hour record" to "never the current-hour record by the source's local stamps".
- **Concession.** The 3 h lag is also cheap and safe (P7). I do not oppose it if the curator prefers it. But it is a definition change and a rebuild to fix a risk the source denies and the data shows no effect from. It should not be a condition for shipping.

**4. RMSE tail and the two false sentences (MET-2, MET-4, CLEAN-11): sentences conceded, option (a) disputed.**
- **Conceded:**
  - "neither … the inspected values proves they are errors" must go. The 788-min trip covered 20.2 km driven at 1.54 km/h, and four trips over 239 min ran under 2 km/h.
  - The CC reason "as the other RMSE-scored ETA datasets" is false. Reword it to MET-4.
  - Record the tail shares: the top 1% of errors hold 54 to 66% of squared error; trips over 3 h hold 11.8% of the squared spread; one row holds 21% of f1.
- **Disputed: whether nyc's cap applies here.** nyc's `MAX_SECONDS` rests on a measured fact: "a cluster just below 24 h follows (VeriFone meters) whose metered fares are those of trips of a few minutes" (nyc `dataset.py`, lines 27–28). Lusaka has no such cluster and no fare field that would make the duration impossible:
  - There are 20 trips over 3 h, spread out, the longest 13 h, all with positive driven distance.
  - A 13 h, 20 km ride is unusual, not impossible (waits, an abandoned meter). CLEAN-11: "Values that are only unusual stay."
  - The critic agrees that option (a) needs "impossible value" reasoning, and neither of us has a source statement for it.
- **Effect also favours keeping:**
  - Dropping training rows over 120 min gains 0.03 to 0.10, which is borderline against the ±0.05 noise.
  - Dropping rows over 240 min gains nothing.
  - Dropping trips under 1 km/h makes all three splits worse.
  - The practitioner warns that any cut on duration or speed reads the target.
- **What follows.** Put the prompt to the curator as the critic frames it, but with (b), keep with a recorded exception, as the rule-backed default. The distinguishing fact: there is no broken-clock cluster, and the source scored these trips in its own RMSE. Dropping the single 788-min test row stays a separate weighing call under CLEAN-11 → CLEAN-15.

**5. Impossible straight-line speeds (CLEAN-11, pkdd consistency): conceded, with the critic's correction.**
- The precedent checker's "up to 206 km/h" is wrong. The maximum is 416.2 km/h (8.879 km in 1.28 min), confirmed by the column auditor. The prompt must say that before it goes to the curator.
- Unlike point 4, these values are impossible. With exact `str_distance_km`, either the target or the endpoint is wrong. pkdd drops the same mechanism. The effect is about 0.000 of the spread.
- So the consistent fix is cheap and safe (P7): drop the 19 rows as pkdd does, with a Decision table. I lean to (b), drop, over my opening's either/or. A prompt still goes to the curator.

**6. Byte lengths and stale lines (PROV-10, writing): conceded.**
- "Sizes match the listing's rounded sizes" (15,620,473 B against 15.6 MB, and so on).
- Supersede "no public solution found" and "no panel ran".
- The 2023/2024 conflict is already stated in `row` and `curation_comments`.

**7. Unequal weekday mix (SPLIT-20, Should): conceded as a note.**
- Add the sentence to `splits_comment`. The dip is Sunday 2023-01-29: all five Sundays sit at 11.07 to 12.11 min, against 13.70 to 14.67 on other days.
- No re-split: 7-day windows give a 31.8% train side, which breaks SPLIT-14, and SPLIT-21 forbids choosing windows by score.
- Correct the practitioner's "drift around 01-27" in the panel notes.

**Updated judgment record**
```text
Verdict: ship after changes (wording; optional 19-row speed cut).
Validity: LEAK-10 driven distance fixed (Must holds); SPLIT-9/SPLIT-14 hold; USE-7 cut stands, wording fixed;
  USE-8 approximate, fit_reason gains the no-router sentence; weather clock: note citing the source's
  "Local date and time" against the diurnal hint (3 h lag optional, not required).
Value: MET-4 holds; CC reason reworded to MET-4; tail shares recorded (MET-10).
Quality: CLEAN-11 long trips kept as unusual (no nyc-style cluster), sentence corrected;
  >120 km/h trips (19, max 416.2 km/h) dropped as in pkdd, curator confirms.
For the curator: (1) the 788-min test row; (2) speed-cut consistency prompt with the corrected maximum;
  (3) lag 1 h + note or 3 h.
```

</details>

<details><summary>Critic rebuttal</summary>

**Rebuttal (opponent): `2024_lusaka_mobility_prediction_hackathon`**

The advocate and I now ask for nearly the same remedies. Only three questions are still open:
- whether the weather join keeps the word "never" or gets a 3 h lag (issue 3);
- whether the long, slow trips need a prompt to the curator or only a note (issue 4);
- how the speed prompt is worded (issue 5).

My verdict stays: ship after changes, with no exclusion.

**A1. The competition's leak is gone and no exploit was found (LEAK-10, LEAK-16, SPLIT-9).** Concede. Dropping `transporting_distance_fact_km` is correct, the 1-day gap leaves 0 training trips ending after a window starts, and the task gamer found nothing above the ±0.05 noise floor. One limit on "nobody could game what is left": the gamer tested shortcuts a participant could use. Mixed endpoint meaning (A6) and the weather clock (A7) are questions about what a feature means, and they stay open.

**A2. The use case is real; the no-router gap gets one sentence (USE-8).** Concede. We ask for the same sentence in `fit_reason` and `use_case`, naming pickup as the prediction point.

**A3. The split mirrors deployment and meets the floor (SPLIT-14, SPLIT-21).** Concede. Three windows is the maximum (a fourth would have a 0.478 training share), and the 01-29 Sunday correction and the `splits_comment` sentence match my point 7.

**A4. RMSE on minutes stays; only the reason is wrong (MET-4, MET-2).** Concede that the decision stays and the reason is reworded to MET-4. One addition to the advocate's remedy: MET-2 asks whether the score means on our folds what it meant on the source's. In f1, one row holds 21% of the dummy squared error (13.331 with it, 11.848 without). So the note must give the per-window figure for that row, not only the pooled tail share. Otherwise a reader cannot see that the f1 ranking depends partly on one trip.

**A5. Keep the long trips; nyc's cap rests on a fact Lusaka lacks (CLEAN-11).** Partly concede, partly dispute.
- Concede: nyc's `MAX_SECONDS` docstring rests on "a cluster just below 24 h … whose metered fares are those of trips of a few minutes". Lusaka has no such cluster, so "the same mechanism" in my point 4 overstated the precedent. I withdraw the claim that this is a consistency failure against nyc.
- Dispute: CLEAN-11 decides on the value, not on the precedent. Its first sentence turns impossible values into missing ones, and only unusual values stay.
  - The 788-min row covers 20.2 km driven against 1.12 km straight-line in 13 h.
  - Kept trips run at 0.31 and 0.32 km/h for 304 and 240 min.
  - These may be unclosed trips. That is a real question of impossibility, not just an unusual value, and only the curator can settle it. A note alone does not put it to the curator.
- Dispute: the task gamer's "0.03 to 0.10" measures what happens when training rows are dropped. That is not the effect in question. The effect is on scoring: 16.9%, 28.8% and 15.7% of each window's squared deviation sit in trips over 120 min. The practitioner's warning that any cut "reads the target" applies to outcome-based filters. It does not apply to a row whose target is judged impossible (CLEAN-11, then CLEAN-15).
- Remedy, close to the advocate's:
  - correct the sentence;
  - record the shares;
  - put one curator question: is the 788-min row, and possibly the sub-1 km/h rows over 3 h, an impossible target (CLEAN-11 to CLEAN-15), or does it stay as unusual?
  - Drop the nyc-consistency framing from that prompt.

**A6. The 100 m cut is right; only its wording is wrong (USE-7).** Concede the cut and the remedy, including adding Lusaka to the USE-7 Cases table at use_case.md:165. Dispute one reading: the 1,756 trips show that the endpoint has two meanings. They do not show that the stand-in works. On rows where the end is the drop-off, `str_distance_km` carries a post-trip location. The note must say so plainly (LEAK-1, Should), not present the counts as support for the approximation.

**A7. Speeds, weather and wording.**
- **Speeds (CLEAN-11 against pkdd).** Concede: drop or keep with a note, and the curator picks. One thing needs fixing before the prompt goes out: the precedent checker's draft says "up to 206 km/h", but my recount on the pinned Train.csv gives a maximum of 416.2 km/h (8.879 km in 1.28 min). The column auditor found the same maximum independently. The prompt needs the true maximum.
- **Weather clock (LEAK-10, weak).** Concede that it is weak, given the flat cross-correlation and about zero single-feature skill. But "a note saying the timezone is unverified" contradicts the definition's claim that it "never" uses the current hour. A note alone leaves a false statement in the definition.
  - My preferred fix is the 3 h lag. It is safe on either clock and costs no measured skill, which fits P7's "fixed when the fix is cheap and safe".
  - If the curator prefers the note, the word "never" must go in the same edit.
  - I hold this as a choice for the curator, not as a condition for shipping.
- **Wording (PROV-10, writing.md).** Concede "sizes match the listing's rounded sizes", and that the lines "no public solution found" and "no panel ran" get superseded. The 2023/2024 date conflict is already stated, so I drop nothing and add nothing there.

**Judgment record (updated)**
```text
Verdict: ship after changes (text fixes; 3 h weather lag or drop "never"; two curator prompts).
Validity: LEAK-10 (driven distance) fixed; SPLIT-9/SPLIT-14 hold; USE-8 gap named in fit_reason; USE-3/LEAK-1 reworded + mixed-endpoint note (1,756 / 290).
Value: MET-4 holds, reason reworded; MET-2 note gives f1 one-row share (21%) and window tail shares (16.9/28.8/15.7%).
Quality: CLEAN-11 prompts: (1) 788-min and sub-1 km/h trips as impossible targets, nyc framing withdrawn; (2) 19 trips >120 km/h, max 416.2 km/h, against pkdd.
```

</details>
