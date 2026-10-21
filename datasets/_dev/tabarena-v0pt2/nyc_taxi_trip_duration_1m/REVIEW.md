# nyc_taxi_trip_duration

**Outcome:** added as `nyc_taxi_trip_duration_1m`. The Kaggle sample of the 2016 NYC yellow-cab trips, target the log
trip duration (regression, an ETA at pickup with the drop-off point taken as the destination), temporal with three
weekly test windows in June 2016 and a one-day gap. The review panel's changes are in dataset.py (not built yet).
Under the row budget it ships only as `nyc_taxi_trip_duration_1m` (the curator, 2026-10-21): train sides of 1M, a
frame of 1,166,477 trips.

```text
Verdict: ship (the panel's changes are in dataset.py; not built yet).
Validity: SEL-1/SEL-2 hold; USE-1/USE-3 hold; USE-7 triggered, fixed (4,539 trips whose drop-off coordinates equal
  the pickup coordinates dropped); USE-8 approximate (the drop-off point stands in for the destination named at
  pickup, as in pkdd_15); LEAK-10 holds (dropoff_datetime and store_and_fwd_flag dropped); SPLIT-1 holds (temporal,
  weekly windows, SPLIT-12); SPLIT-9 triggered, fixed by a one-day gap (77/119/127 train trips per window end after
  the window start without it, 0 with it); SPLIT-20 (Should) departed from, with a note (the source holds January-June 2016 only);
  PROV-1 holds (13 of 13 sampled rows match NYC Open Data); PROV-13 holds (86 trips across the daylight-saving
  switch repaired).
Value: TP-2 holds (task probe: LightGBM skill 0.62 over predicting the mean before the changes, no flags; RMSE
  0.357-0.381 on the weekly windows with the hour kept, against a test standard deviation of 0.75).
Quality: CLEAN-10/CLEAN-11 passenger_count 0, 8 and 9 set missing; the 30 s / 3 h cuts rest on evidence outside the
  target (CLEAN-11, CLEAN-15; pkdd_15 CC).
Weighed: size +, source +, consistency with the ETA siblings +, half a year of history -, no routing estimate -.
For the curator: nothing on the row budget (settled 2026-10-21: the `_1m` version). The datetime
  encoding of v0.2 is a cross-dataset item; the bibtex cites the TLC next to the Kaggle competition (PROV-10; the curator, 2026-10-21).
```

**Main points:** Settled 2026-10-21: the dataset ships as `nyc_taxi_trip_duration_1m` under the row budget. The datetime
encoding of the v0.2 runs (it decides whether models see the hour of day) is decided across datasets in the working
copy's REVIEW.md. Settled 2026-10-21: the bibtex cites the TLC, the original publisher, next to the Kaggle competition.

**Record fields that disagree with the definition:**

- `domain`: record `Other`, definition `industry & manufacturing`.

**Record judgment:** valid. A real ETA-at-pickup task on the TLC's own trip records (Kaggle's sample; sampled rows
match NYC Open Data to the second). The fit is approximate: the recorded drop-off point stands in for the destination
named at pickup. The CC of 2026-09-21 says the TLC Parquet files hold coordinates up to mid-2016; the 2016 files hold
zone IDs only; NYC Open Data (uacg-pexx) still serves the coordinates.

**Review panel:** ship after changes (mediator). Claim audit: two claims refuted, the split
note's scores and cause (fixed in dataset.py) and the CC's TLC coordinates (record judgment); licence and two source
routes untested, the rest hold. Blind review: include with changes; main concerns the row filter on the target and the
datetime encoding. Debate: agreed on the source, the 30 s / 3 h cuts, the weekly windows, the dropped flag, the
daylight-saving repair, dropping the one-point trips, the one-day gap and passenger_count; disputed: the fit label
(settled by the mediator as approximate), the hour of day (cross-dataset) and whether the budget warning can stay
accepted (issue 5). The reports number the issues of an earlier draft 1-8 (called REVIEW_before) and the mediator's
list 1-2: the mediator's issue 1, the datetime encoding, is a cross-dataset item, and its issue 2 is issue 5 here. Their counts are those
of the definition before the changes.

<details><summary>Mediator</summary>

**nyc_taxi_trip_duration: mediator (2026-10-20, re-check, full tier)**

Agents: claim-auditor, column-auditor, split-auditor, domain-practitioner, blind-reviewer, precedent-checker, advocate and critic (one rebuttal each), mediator.

**Judgment record**

```text
Verdict: ship after changes.
Validity: SEL-1/SEL-2 hold; USE-1/USE-3 hold; USE-7 triggered (4,539 trips with identical pickup and drop-off), fixed
by a filter; USE-8 approximate (the drop-off point stands in for the named destination, as in pkdd); LEAK-10 fixed
(dropoff_datetime, store_and_fwd_flag dropped); SPLIT-1 holds (temporal, weekly, SPLIT-12); SPLIT-9 triggered
(77/119/127 eligible train rows end after the window start), fixed by gap=1 (measured: 0/0/0); SPLIT-20 kept with a
note (only Jan-Jun 2016 exists); PROV-1 holds (13 of 13 rows match uacg-pexx); PROV-13 DST repair holds.
Value: TP-2, strong real signal (LightGBM skill 0.62; RMSE 0.36-0.38 against test std 0.75).
Quality: CLEAN-10/11 passenger_count 0, 8, 9 to missing; 30 s / 3 h cuts via CLEAN-11 -> CLEAN-15 (pkdd CC).
Weighed: size +, source +, sibling consistency +, half-year history -, no router input -.
For the curator: issue 1, the datetime pipeline of v0.2 (collection-wide); issue 2, the budget house rule
(rename to _1m or amend definitions.md).
```

**Changes to make now (no decision needed)**

1. **Drop the trips whose pickup and drop-off coordinates are identical** (4,539 rows, 0.31%; test 184/185/181 per window). Rule: USE-7 (Must), applied as in the bias_correction case. Keep the trips that are within 10 m but not identical as unusual values (CLEAN-11). Update the "Anomaly" bullet and `_decisions`.
   - Effect: RMSE 0.353/0.341/0.360 → 0.346/0.330/0.354.
   - Also removes post-trip information: the mean target is 5.77 on these trips against 6.48 on the rest.
2. **`TemporalSplits(window=7, unit="days", n_windows=3, gap=1)`** and state the gap in `splits_comment` as part of the task. Rules: SPLIT-9 (Must), SPLIT-10. Measured by me after change 1:

   | Window | Eligible train, gap 0 | Eligible train, gap 1 | Train rows ending after the start, gap 0 | Same, gap 1 |
   |---|---|---|---|---|
   | 06-24 | 1,394,388 | 1,386,337 | 77 | 0 |
   | 06-17 | 1,341,439 | 1,332,953 | 119 | 0 |
   | 06-10 | 1,286,907 | 1,278,640 | 127 | 0 |

   - Every train side still exceeds 1M, so the cap and issue 2 remain.
   - The test windows are unchanged in place (52,779 / 52,949 / 54,532 after change 1).
   - The split audit's 58/90/99 were the same rows counted on the capped 1M samples.
3. **passenger_count 0 (24 rows), 8 and 9 (2 rows) to missing; keep the rows.** Rules: CLEAN-10/CLEAN-11 (Should). This follows the heart_disease_va_long_beach, house_sales and zillow_prize precedents.
4. **`fit = "approximate"`**, with `fit_reason` naming the gap: the drop-off point stands in for the destination named at pickup, and there is no routing estimate. Rule: USE-8 (Must). It lists "a stand-in with a known gap, named as such" as approximate, and the current `fit_reason` itself says "stands in". Settled in the next section.
5. **Text (EV-8, EV-6):**
   - In `splits_comment`, name the encoding and the setup (300 trees, lr 0.1, 63 leaves, random 200k).
   - Give the scores for both encodings:

     | Split | Hour kept | AutoGluon date parts |
     |---|---|---|
     | Weekly windows | 0.365-0.379 | 0.414-0.434 |
     | By-day | 0.362-0.364 | 0.405-0.411 |
     | Random | 0.357-0.360 | 0.394-0.395 |

   - Replace "probably because trips of one day share traffic and weather" with: day-sharing explains about 0.01; the rest is temporal distance.
   - Reword `use_case` from "refit every week on the latest trips" to "on the trips since January".
   - Re-measure the RMSE in curation_comments and splits_comment after changes 1-2.
6. **Record:**
   - Set `domain` to `industry & manufacturing` (agreed; matches the definition and the ETA family).
   - The 2026-09-21 CC claim that the TLC Parquet files hold coordinates to mid-2016 is refuted (the 2016 files hold zone IDs only). Note this in an `Assessment (AI, ...)` line, not a CC line: a CC line is the curator's.

**Disputed points, settled**

**A. Fit label: direct or approximate (USE-8, Must, P3). Settled: approximate**

- **Advocate:**
  - The 200 m rounding test shows the model uses no GPS detail of the disengagement (0.382/0.364/0.375 vs 0.379/0.365/0.375).
  - Once the one-point rows go, "the drop-off equals the destination for every real ride".
  - A missing router is not a stand-in (USE-6).
- **Critic:**
  - The definition's own `fit_reason` calls the drop-off a stand-in.
  - pkdd writes `approximate` for the same stand-in under the same-day CC.
  - A recorded endpoint differs from the named destination when a passenger changes the destination or gets out early.
- **Ruling:**
  - This is applying a Must's definitions, not weighing factors, so it is mine to settle.
  - The advocate's fact that sets nyc apart ("equals the destination for every real ride") is asserted and cannot be measured on this data (EV-6).
  - pkdd's stated reason (the driver does not enter the destination in the system) holds for NYC yellow cabs in 2016 too: mostly street hails, and the use case says "the taxi's system estimates".
  - With no fact that sets the two apart, treat like cases alike: `approximate`.
  - The advocate is right that a missing router alone would not make the fit approximate. Name it in `fit_reason` as the task's framing ("without a routing estimate"), not as the reason.
  - The curator may keep `direct` only by recording such a fact (consistency check below).

**B. Hour of day under the `default` pipeline (CLEAN-2, Must). Settled: not a gate for this folder; a collection-wide question**

- **Facts (agreed, re-run):** LightGBM RMSE is 0.379/0.365/0.375 when the hour is kept (skrub encoding in `tabarena_default`) and 0.425/0.414/0.434 with AutoGluon date parts (`default`). The gap is 0.04-0.06, against a test std of 0.75.
- **Ruling:**
  - CLEAN-2 tells the definition to leave encoding to the pipeline, and it does, so the Must holds here.
  - The pipeline choice is a harness setting that touches every dataset whose only time feature is a datetime (pkdd the same; precedents #5).
  - The critic's worry (the scores would measure the encoding) is real, but it belongs to the collection, not to this dataset. Tying it to nyc alone would treat like cases unlike.
  - Kept in the curation_comments note. It goes to the curator as issue 1.

**C. Train sides over the 1M budget (house rule, definitions.md; never weighed). Settled on status: open, not "accepted"**

- An accepted check warning cannot stand as an exception to a house rule.
- **Fact both briefs missed:** the temporal `_1m` path in definitions.md ("A temporal `_1m` version whose windows all fit is an error") and the code (`default_splits`) both accept a temporal `_1m` whenever a train side exceeds 1M, whatever the frame size. That holds here: 1.28M-1.39M eligible even after `gap=1`.
- So a compliant option exists without an amendment: rename to `nyc_taxi_trip_duration_1m` with `version_of` and `subsample_to_budget = True`. This gives one random order with overlapping train sides, as in delivery_eta_1m, and the frame keeps only the rows used.
- The "frame above 1.5M rows" wording in the check table of definitions.md contradicts that bullet and should be aligned whichever way the curator chooses.
- A rename touches the folder, README table, CHANGELOG and record `v2_path`, so it goes to the curator as issue 2.

**Issues for the curator, ranked**

1. **Which datetime encoding v0.2 runs (collection-wide; benchmark validity of the time signal).**
   - **Problem:** `pickup_datetime` is the only time feature. Under `default` the hour is lost.
   - **Effect:** 0.04-0.06 RMSE of this task's signal depends on the encoding (0.379/0.365/0.375 vs 0.425/0.414/0.434).
   - **Critic:** confirm the pipeline before scores are compared. The practitioner calls hour-of-week the first feature of any ETA.
   - **Advocate:** this is one harness call for the whole datetime-only family. The definition follows CLEAN-2.
   - **Rule:** CLEAN-2 (Must) bars a hand-made hour column, so the fix can only be in the harness.
   - **Decision:** `tabarena_default`, or a harness change for every datetime-only dataset (nyc, pkdd and others). Not a reason to hold this folder.
2. **Budget house rule (definitions.md).**
   - **Problem:** `cap_splits` draws an independent 1M per window under a name without `_1m`. 129,675 trips (8.9%) are in no split.
   - **Effect:** none on validity (SPLIT-14 holds; latest-1M and random-1M score alike, and SPLIT-21 bars deciding from that anyway).
   - **Options:**
     - (a) rename to `nyc_taxi_trip_duration_1m`, compliant today with the temporal `_1m` path;
     - (b) amend definitions.md to allow per-window capping under the full name when the frame is under 1.5M rows.
   - Align the check-table wording either way. House rules are not weighed, so one of the two is needed.

The REVIEW_before issues not listed here (1 Kaggle sample vs TLC rebuild, 2 the 30 s / 3 h cuts, 3 weekly windows, 6 the flag dropped, 7 DST repair, 8 licence) are agreed by both sides and follow the rules and precedents (precedents #1, #3, #4, #7, #8, #9). No decision is needed beyond the curator closing them.

**Agreed facts**

- **Frame:** 1,451,706 trips, 2016-01-01 to 06-30, from Kaggle train.csv (1,458,644 rows; the sha256 matches). 13 of 13 sampled rows match NYC Open Data uacg-pexx. The TLC 2016 Parquet files hold zone IDs only.
- **Target:** log1p(seconds); RMSE on it equals the competition's RMSLE.
- **Duration cuts:** 4,782 trips under 30 s and 2,111 over 3 h are dropped (0.47%).
  - Under 30 s, 63% start and end within 10 m.
  - Over 3 h, 1,900 sit at 22-24 h: 100% VeriFone, median 0.10 km/h, TLC fares $13-$52 for 2-18 miles.
  - These are data errors shown by evidence outside the target (CLEAN-11 → CLEAN-15; pkdd CC). The practitioner accepts the cuts.
- **Dropped columns:** `dropoff_datetime` (equals pickup + target) and `store_and_fwd_flag` (sent after the trip; Y on 8,045 trips, all CMT; worth 0.001-0.003 RMSE) are correctly dropped (LEAK-10).
- **DST repair:** 86 kept trips repaired. Trips recorded at 60 min or more in the 01:00 hour: 0 / 87 / 0 on Mar 6 / 13 / 20 (PROV-13).
- **Split:**
  - 3 weekly windows of 52,963-54,713 test rows, strictly after train.
  - Random hold-out is optimistic by 0.013-0.029, so temporal is right.
  - No hidden groups; 0.0% near or exact copies across the split; no end censoring.
  - Weekly windows match the stated refit (SPLIT-12) and the shipped ETA siblings. SPLIT-21 bars choosing the window length from RMSE.
- **Drop-off as destination:** the drop-off at 200 m resolution carries the full skill (0.382/0.364/0.375 vs exact 0.379/0.365/0.375; no drop-off 0.693/0.684/0.700).
- **Keep as unusual values:** the 46 trips over 100 km/h. Unlike pkdd, nyc has no trajectory that would show the label is broken (CLEAN-11).
- **Signal:** the task probe flags nothing (LightGBM skill 0.622 ± 0.018). The blind reviewer also finds strong signal and rates it would-benchmark, with changes that the notes and changes 1-5 cover.
- **Already agreed before this report:** the changes 1-3, 5 and 6 above.

**Consistency with precedent**

- **Followed:**
  - Kaggle sample without a rebuild: rebuilds so far answered damage (corporate_credit_rating, coad, hr_analytics, ashrae); nyc has none.
  - Licence is never evidence (lucas_topsoil).
  - Cuts follow the pkdd CC and the TabReD lower cuts. zillow_prize differs on a stated fact: nyc has evidence outside the target.
  - Weekly windows follow delivery_eta_1m, maps_router_eta_1m and cooking_time_1m.
  - Flag dropped follows kickstarter and hotel (LEAK-10).
  - passenger_count follows heart_disease_va_long_beach, house_sales and zillow_prize.
  - The one-point drop follows bias_correction (USE-7).
  - `fit = approximate` follows pkdd.
- **Departure, pending the curator:** the budget handling (issue 2). Fact that sets it apart: the frame is under 1.5M while its train sides exceed 1M. The compliant `_1m` path exists, so absent an amendment, treat it like delivery_eta_1m.
- **Sibling to align (no curator precedent exists; both are AI drafts):** pkdd keeps its one-point trips (its issue 3, open). Once nyc drops them under USE-7, pkdd's should be reviewed the same way. The two taxi folders cite each other on five issues and are best settled in one sitting.
- **If the curator keeps `direct`:**

  ```text
  **Consistency check (AI, 2026-10-20):** keeping nyc_taxi_trip_duration at fit direct differs from
  pkdd_15_taxi_trip_time_prediction_ii_1m (approximate, the same drop-off stand-in, CC of the same day). What sets nyc
  apart? (a) a fact recorded as the reason for direct; (b) treat nyc like pkdd: approximate; (c) reopen pkdd as direct;
  (d) amend USE-8 to say how a recorded endpoint used as a named destination is rated.
  ```

**Experiment run by the mediator**

The script ran with thread caps of 2 on the claim auditor's frame (rebuilt from the definition). It uses `temporal_window_splits` of `src/data_foundry/v2/splits.py`, where a gap moves the train end back and leaves the test windows in place. Results are in the change 2 table.


</details>

<details><summary>Claim audit</summary>

**nyc_taxi_trip_duration: claim audit (claim-auditor, 2026-10-20)**

Frame and splits rebuilt from the definition; NYC Open Data look-ups for sampled rows. Thread caps 2 on every run. Licence never used as evidence (EV-4).

**Result per claim (numbers = claims.md)**

| # | Claim (short) | Test | Result | Evidence | Rule |
|---|---|---|---|---|---|
| 1-2 | ETA at pickup, weekly refit | read with 22, 35 | holds | see 22, 36 | USE-1 |
| 3 | 1,451,706 trips, Jan-Jun 2016 | rebuild frame | holds | 1,451,706; 2016-01-01 00:00:17 .. 2016-06-30 23:59:39 | EV-1 |
| 4, 23 | log1p target; RMSE = RMSLE | definition code | holds | `np.log1p(trip_duration)` | USE-5 |
| 5, 22, 8 | features known at pickup; dropoff point stands in for named destination (fit direct) | refit with dropoff coords rounded to ~200 m / ~1 km / ~2 km and dropped (300 trees, 63 leaves, 200k train, skrub-like encoding) | holds (given the curator's premise) | exact 0.379/0.365/0.375; ~200 m 0.382/0.364/0.375; ~1 km 0.399/0.386/0.396; ~2 km 0.436/0.424/0.432; no dropoff 0.693/0.684/0.700. A block-level destination gives the full skill; no GPS detail of the disengagement is used. Residual: 5,621 one-point trips (4,539 identical coordinates) have mean y 5.77 vs 6.48: "drop-off = pickup" is post-trip information, 0.4% of rows | USE-3, LEAK-1 |
| 6, 37 | test = last 3 weeks; train = random 1M of earlier trips per window | splits from definition | holds | test 52,963/53,134/54,713; train 1M each; earlier trips 1,398,743/1,345,609/1,290,896 | SPLIT-1 |
| 7 | changes list | code + counts | holds | see 25, 27-30 | |
| 9 | domain as delivery_eta_1m, maps_router_eta_1m | grep siblings | holds | both "industry & manufacturing" | |
| 12 | 1,458,644 rows, sha256 | sha256sum | holds | fc8c777a...99927 | PROV-1 |
| 14 | under 30 s mostly one point | haversine < 10 m | holds | 63.0% (< 10 s 72.1%, 10-29 s 56.5%) | CLEAN-11 |
| 15 | smooth fall to 18 trips/20 min at 3 h; 22-24 h VeriFone cluster with fares of short trips | 20-min histogram; 3 of the 22-24 h trips looked up on NYC Open Data uacg-pexx | holds | bin 2:40-3:00 = 18; 1,427 trips in 23:40-24:00; fares $31.5 (8.9 mi), $13 (2.3 mi), $52 JFK flat (18 mi) | CLEAN-15 |
| 16 | box ~80 km W/N/S, 170 km E | geometry at lat 40.75 | holds | 84 km W, 169 km E, 83 km N/S | |
| 17, 25, 42 | TLC dictionary quotes (vendors, flag) | data: flag by vendor; PDF text not extractable here | holds on data, wording untested | Y on 8,045 trips, 100% vendor 1; 7,951 Y in the shipped rows | LEAK-10 |
| 18, 19, 28, 43 | wall-clock times; DST trips 3,600 s too long | dropoff-pickup vs trip_duration; 01:00-01:59 pickups on 3 Sundays | holds | equality 100%; recorded >= 60 min: 0 / 87 / 0 (Mar 6/13/20); median 11.85 -> 10.58 min after fix. Note: 1 pickup and 2 dropoffs fall in the non-existent 02:00-02:59 hour | PROV-13 |
| 20, 27 | 7 exact copies; 86 DST trips kept of 97 | recount | holds | 7; 97 fixed, 86 kept | LEAK-16 |
| 21, 51 | rows are TLC records | 5 more train rows looked up in uacg-pexx | holds | 5 of 5 match to the second and 1e-6 deg | PROV-1, SEL-16 |
| 29 | 4,782 + 2,111 = 0.47%; 1,900 in 22-24 h, all vendor 2 | recount | holds | 0.4726%; 1,900, 100% vendor 2, median 0.10 km/h. 3-4 h band: 63% under 2 km/h; 2-3 h: 27%, so 38 kept trips > 2 h at walking speed remain | CLEAN-15 |
| 30 | 38 out of box, median 580 s | recount | holds | 38, 579.5 s | |
| 31 | 5,621 / 46 / 24 | recount | holds | 5,621 / 46 / 24 | CLEAN-10 |
| 32, 36, 39 | weekly windows; train >= 89% | recount | holds | 88.92% (rounds to 89%) to 96.35% | SPLIT-11 |
| 33 | LightGBM 0.380/0.365/0.378 (hour kept, skrub) vs 0.425/0.414/0.434 (AG parts) | re-run; TabArena code uses `DatetimeEncoder(add_weekday=True, periodic_encoding="circular")` | holds under the 2026-10-07 script's setup, setup not stated | 300 trees, lr 0.1, 63 leaves, random 200k of each train side: 0.379/0.365/0.375 and 0.425/0.414/0.434. LightGBM package defaults on the full 1M: 0.430/0.421/0.431 vs 0.457/0.447/0.463 (the hour gap is real, the levels are config-bound) | EV-8 |
| 38 | random 3-fold 0.396-0.399 vs weekly 0.419-0.440; "probably because trips of one day share traffic and weather" | re-run random 3-fold and a by-day grouped 3-fold, both encodings | numbers hold; encoding unstated and conflicts with 33; mechanism refuted in part | AG parts: random 0.394-0.395, by-day 0.405-0.411, weekly 0.414-0.434. Hour kept: random 0.357-0.360, by-day 0.362-0.364, weekly 0.365-0.379. Day-sharing explains about 0.01 of the gap, the rest is temporal distance. With the shipped encoding (hour kept) the weekly windows score 0.365-0.379, not 0.419-0.440 | EV-8, EV-6 |
| 40 | 129,675 rows unused, all before 2016-06-10 | recount | holds | 129,675 (8.93%), latest 2016-06-09 23:47:27 | SPLIT-15 |
| 46 | OpenML 42729 is another cut | OpenML API | holds | green cabs, Dec 2016, target tip_amount, zone IDs: no row overlap possible | PROV-4 |
| 47 | TLC Parquet has coordinates up to mid-2016 | downloaded yellow_tripdata_2016-06.parquet schema | refuted (already corrected by the 2026-10-07 assessment, the CC line stands) | columns PULocationID, DOLocationID, no coordinates | EV-2 |
| 52 | test labels leaked through public TLC records | look-up of train rows works by pickup second + vendor | holds | exact matches returned (opendata_lookup.txt); irrelevant to our splits | |
| 56 | domain disagreement | record field | holds | record Other vs definition industry & manufacturing | |
| unwritten | no copy across the split | feature hashes per window | holds | exact feature copies 0.0%; ignoring time 0.002% (1 row) | LEAK-16 |
| 10, 13, 34, 48 | licence, citation, Kaggle Sec. 7 | not tested | untested (licence is never evidence) | | EV-4 |
| 45, 49 | BigQuery route; jeffreycbw scores | not tested | untested (no bearing on validity) | | |
| 50, 53-55 | assessments restating the above | covered by rows above | holds | | |

**Refuted, ranked (principles.md)**

1. Claim 38 (splits_comment, procedure EV-8 / EV-6): "0.419-0.440 on the weekly windows" is measured with AutoGluon date
   parts, while claim 33 gives 0.365-0.380 for the shipped (hour-keeping) encoding; the cause "trips of one day share
   traffic and weather" explains only ~0.01 of the 0.02-0.04 gap (by-day split 0.405-0.411 vs random 0.394 vs weekly
   0.414-0.434). Remedy: name the encoding and the setup (300 trees, 63 leaves, 200k) in both notes, and say the
   random-split optimism is mostly temporal distance, partly day-sharing.
2. Claim 47 (record CC 2026-09-21, P5): TLC 2016 Parquet files hold zone IDs only. Remedy: a CC line superseding it
   (the assessment already says so).

**Untested**

Licence/Kaggle Sec. 7 (EV-4, never evidence); TLC dictionary wording (PDF not extractable; the data agree); BigQuery
route and jeffreycbw scores; test.csv per-day share (file not in the raw folder).

</details>

<details><summary>Column audit</summary>

**Column audit: nyc_taxi_trip_duration (2026-10-20, re-check, full tier)**

Prediction point (curation_comments bullet 1): the meter is engaged and the passenger has named the destination; the
recorded dropoff point stands in for the destination (Lennart, 2026-09-21). Frame: definition rebuilt from
the raw train.csv (no build path in README), 1,451,706 x 8,
sorted by `pickup_datetime` (CLEAN-23 holds). Codebook: TLC yellow-trip data dictionary (as quoted in dataset.py).

**Column table**

| column | meaning | known at prediction? | dtype and cleaning | verdict | rule |
|---|---|---|---|---|---|
| vendor_id | TLC: provider of the meter system, 1=Creative Mobile Technologies, 2=VeriFone | yes (fixed per cab) | category, 2 levels mapped to dictionary names, no NA | fine | CLEAN-12, CLEAN-14 |
| pickup_datetime | TLC: date and time the meter was engaged (wall-clock) | yes, defines the point | datetime64, 2016-01-01..06-30, 98% have non-zero seconds; 1 raw pickup (id0253317, CMT) lies in the non-existent hour 02:00-02:59 on 2016-03-13 and is kept | fine (the 1 impossible time is negligible) | CLEAN-14, CLEAN-11 |
| passenger_count | TLC: number of passengers, driver-entered | yes (entered at the start) | int64; 0 in 24 rows (driver did not enter it: a proxy missing value), 8 and 9 in 1 row each (above a yellow cab's legal capacity); all kept as numbers. 5 and 6 are 99.5% VeriFone (a vendor recording habit, no target shift: mean target 6.48/6.47 vs 6.46 for 1) | cleaning problem, minor: 0 -> NA, 8/9 -> NA | CLEAN-10, CLEAN-11 (Should) |
| pickup_longitude | GPS longitude at meter engage | yes | float64 (float32 origin precision), box -75..-72 filter, no NA | fine | CLEAN-11 |
| pickup_latitude | GPS latitude at meter engage | yes | float64, box 40..41.5, no NA | fine | |
| dropoff_longitude | GPS longitude at meter disengage | no, recorded at the outcome; kept as the stand-in for the named destination (curator decision) | float64, box filter | approved stand-in; see problem 1 for the rows where it cannot be a destination | USE-3, USE-7, USE-8 |
| dropoff_latitude | GPS latitude at meter disengage | as above | float64, box filter | as above | as above |
| log1p_trip_duration | target: log1p(dropoff - pickup seconds), DST-corrected for 86 trips | outcome | float64, 30 s..3 h filter on the target, no NA | fine (log named after transform; DST fix plausible for both vendors: corrected medians 13-16 min, 15 km/h) | CLEAN-15, CLEAN-16 |

Dropped columns: `id` (identifier `id` + 7 digits, 100% match; no meaning, CLEAN-3, right), `dropoff_datetime`
(pickup + target, LEAK-10, right), `trip_duration` (raw target), `store_and_fwd_flag` (sent after the trip; Y only on
CMT, 8,045 trips; LEAK-10 conservative, effect 0.001-0.003 RMSE, right).

**Problems ranked (principles.md)**

1. **USE-7 / USE-3 (P3, Must), weak-to-moderate: 4,539 trips (0.31%) whose dropoff equals the pickup exactly.** A named
   destination is never the pickup point; these records lack the input the ETA acts on (a stuck or failed GPS at
   drop-off; 73% VeriFone, 0.29-0.34% every month). Measured (LightGBM 400 trees, hour/dow/doy, weekly windows): they
   are 181-185 test rows per window with RMSE 1.08-1.15 against 0.336-0.355 elsewhere, carrying 3.1-3.7% of the squared
   error; overall RMSE 0.353 / 0.341 / 0.360 shipped vs 0.346 / 0.330 / 0.354 when dropped from train and test. The
   definition keeps them as "cannot be told from real trips"; equal float32 coordinates (about 1 m) make a real round
   trip implausible. Mildest remedy: drop the rows with identical pickup and dropoff (USE-7: a row without the input is
   no task row), or, if the curator prefers, set their dropoff to missing with a note. Question for the curator, since
   the comment calls it an anomaly kept on purpose.
2. **USE-8 (P3, Must), question: fit "direct" with a stand-in.** The task summary says the recorded dropoff "stands in"
   for the named destination; USE-8 lists a stand-in with a known gap as approximate. Problem 1 is the measured gap.
   Remedy: either fit `approximate` with the gap named, or keep `direct` with the reason that the dropoff equals the
   destination for every real ride once problem 1's rows are gone.
3. **CLEAN-10 / CLEAN-11 (P7, Should), minor: passenger_count 0 (24 rows) and 8/9 (2 rows).** 0 is "not entered", 8-9
   exceed the cab's capacity. Remedy: set to missing, keep the rows; or keep with the note already present.
4. **CLEAN-11 (P7, Should), negligible: 1 pickup in the non-existent DST hour** (id0253317, 624 s, CMT). Note only.

No leak found in the shipped features beyond the curator-approved dropoff stand-in; no identifier, no copy column, no
untyped object column; target-selected row filters (30 s / 3 h) are REVIEW issue 2 and for the claim and split
auditors.

</details>

<details><summary>Split audit</summary>

**Split audit: nyc_taxi_trip_duration (2026-10-20, re-check, full tier)**

**Verdict: right with notes.** Temporal, 3 weekly windows (Fri-Thu) over the last 3 weeks of June 2016, expanding
train side trimmed to a random 1M of the earlier trips per window.

Frame from the definition; LightGBM 400 trees, lr 0.1, 255 leaves, features: the 6 columns + hour, weekday,
day of year, days since start; one fit per split, untuned, EV-8.

**Checks that pass**

| Check | Evidence | Rule |
|---|---|---|
| Regime | ETA at pickup for a new trip; a stream over time; no taxi, medallion or driver id in the data, so no recurring entity to hold out | SPLIT-1, SPLIT-6, SPLIT-13, USE-10 |
| Time column | `pickup_datetime` (datetime64), the prediction point itself; 2016-01-01 00:00:17 to 2016-06-30 23:59:39 | SPLIT-2 |
| Windows | tests 2016-06-24..30 (52,963), 06-17..23 (53,134), 06-10..16 (54,713); newest first; strictly after train | SPLIT-11, SPLIT-14, SPLIT-15 |
| Train side | eligible earlier trips 1,290,896-1,398,743 (89-96% of the frame); each trimmed to 1M (71-77% of eligible) | SPLIT-14 |
| End censoring | the Kaggle sample is not cut at the drop-off: 127 raw trips drop off on 2016-07-01 (109 under 1 h); 23:00 pickups on 06-30 average 936 s vs 760-805 s on 06-28/29, so long late trips are not missing | SPLIT-9 |
| Sampling over time | 228k-255k trips per month; the last-window days hold 7,037-8,186 trips each | - |
| Hidden groups / near copies | probe: 0 candidates, 0 composite keys, near copies 0.0% of test rows seen | SPLIT-29, SPLIT-30 |
| Alternative IID split | random hold-out of the same sizes: RMSE 0.320 / 0.322 / 0.328 vs 0.349 / 0.335 / 0.345 on the weekly windows (std of y in test 0.75). Random is optimistic by 0.013-0.029; temporal is right | SPLIT-1, SPLIT-5 |
| Season of test | late June, no public holiday inside (Memorial Day 05-30 and July 4 are outside) | SPLIT-20 |

**Problems, ranked (principles.md: P4, then strength, then order)**

1. **Training rows whose label is not known at the refit (P4, SPLIT-9 Must, SPLIT-10).** 58 / 90 / 99 train rows per
   window are picked up before the window start and drop off after it (label delay up to the 3 h cap). Effect:
   training only on rows dropped off before the start gives RMSE 0.346 / 0.333 / 0.345 vs 0.349 / 0.335 / 0.345,
   within single-fit noise. Mildest remedy: a filter (train rows with pickup + duration < window start) or a gap of
   3 h; or keep with a note, since it is under 0.01% of train and changes no score. The mediator decides.
2. **Train history vs the use-case text (P3/P4, SPLIT-20 Should).** `task_summary.use_case` says "refit every week on
   the latest trips", but each train side is a random 1M of all trips since January. Latest 1M instead: 0.349 /
   0.335 / 0.353 vs 0.349 / 0.335 / 0.345, no consistent difference (and SPLIT-21 bars deciding from it). Mildest
   remedy: rephrase the use case ("on the trips since January") or keep; no re-split. The 129,675 rows in no sample
   are REVIEW issue 5 (framework), not a split error.
3. **No full season before the windows (SPLIT-20 Should).** The source holds only January-June 2016, so a full year is
   impossible; the history includes the 2016-01-23 blizzard (1,635 trips, the lowest day; 01-24 3,359). Keep with a
   note; no remedy available from this source.
4. **Test rows selected on the label (P4, cross-reference).** The 30 s / 3 h duration filter also removes test rows
   by their target, so the windows score only "normal" trips. Owned by REVIEW issue 2 (column / claim auditors); the
   split itself is unaffected.

Window length (7 vs 28 days, REVIEW issue 3) is a weighing call: weekly matches the stated refit cadence (SPLIT-12)
and gives 53k-55k test rows per window; nothing here argues for a change.

</details>

<details><summary>Domain practitioner</summary>

**nyc_taxi_trip_duration: domain practitioner (2026-10-20)**

Actor: the ETA/upfront-price team of a NYC taxi e-hail app (Arro is run by Creative Mobile Technologies, Curb by
VeriFone, the two meter vendors in the data). A passenger enters pickup and destination; the app quotes an arrival
time (and since the TLC's upfront pricing, a fare built on it). Inputs read: dataset.py (task_summary, first
curation_comments bullet, splits_comment), the record, REVIEW.md, claims.md, use_case.md.

**Fit: direct (borderline approximate)**

One row is one ride whose pickup time, pickup point, destination, passenger count and vendor I have when the quote is
made, its label is the duration I quote, and the weekly windows match a weekly refit (USE-1, USE-3, USE-8). The
drop-off point standing in for the named destination is a small stand-in named in fit_reason; the larger gap is an
input I would always have and the data lacks (gap 1), which makes the task harder than mine, not different.

**1. Inputs at the prediction point**

Have: pickup_datetime, pickup and destination coordinates, passenger_count (driver keys it at meter start), vendor
(which app/meter stack). store_and_fwd_flag and dropoff_datetime are correctly dropped (USE-3, LEAK-10).

Missing that I would always have:
- the routing engine's estimate (route distance and free-flow or traffic-aware time). Production ETA systems are a
  post-processing model over the router (Uber DeepETA/DeeprETA predicts the residual of the routing-engine ETA). By
  USE-6 a company's own estimate made before the outcome is an input; here it does not exist, so the model must learn
  the street network from four coordinates. Kaggle's strong entries added OSRM fastest-route features for this reason.
- live traffic: speeds of trips completed in the last minutes/hour in the area (I have the live feed; a frozen tabular
  row cannot carry it without a time-aware feature build).
- weather and calendar events (known at pickup; second-order).

Would not have: nothing in the shipped features.

**2. Target**

Duration from meter on to meter off: what I quote. Log scale (RMSE = RMSLE) suits a quote judged in relative error;
a point estimate is what the app shows, though I would also want a quantile (P80) for the upfront price risk. Proxy
issue: none beyond the destination stand-in (USE-5 satisfied).

**3. Rows and test data**

- One row = one quote: yes, except the 5,621 kept trips that start and end at one point (lost GPS or round trips):
  nobody quoting names the pickup as destination, so these rows are not decisions I make (minor, 0.4%).
- Test = next week's trips: yes, matches a weekly refit. All trips are street hails and e-hails mixed; durations do
  not depend on how the cab was hailed, so the population is fine.
- The 30 s / 3 h filter selects on the label, but in deployment these records are meter faults that my monitoring would
  also exclude from training and evaluation; a quote never targets a 23 h clock error. I accept the cut (REVIEW issue 2).
- Training on a random 1M of earlier trips rather than the most recent trips: a real refit uses all or the latest data;
  harmless for a benchmark.

**4. Would I use it**

Not as my production model without a router feature, but as a benchmark of "learn travel time from origin, destination
and time" it is a fair, realistic tabular regression. I would trust it more because the split is temporal and the
post-trip flag is gone; I would distrust a score that depends on whether the harness keeps the hour of day (REVIEW issue
4): any ETA practitioner treats hour-of-week as the first feature.

**Gaps, ranked by how much they change the task**

1. No routing-engine estimate or route distance (USE-6): turns "correct the router" into "learn the city's road
   network from coordinates"; changes the task most, but toward harder rather than unreal.
2. No live traffic or weather features: the real system conditions on them; the weekly split leaves this unmodelled.
3. Hour of day lost under the `default` pipeline (REVIEW issue 4): not a data gap, but it removes my strongest signal.
4. Drop-off point as destination, and 5,621 one-point trips kept (USE-8 stand-in): small.
5. Random 1M train sample per window instead of the latest trips: negligible.

**What an expert would change**

- Add a route feature if a reproducible one exists (OSRM distance and duration on a pinned OSM extract), or at minimum
  keep the task explicitly named "without a router" in the use case; do not invent a live-traffic feature.
- Make sure the hour (and day of week) reaches the model in every pipeline: an explicit hour column if `default` is used.
- Drop trips whose pickup and drop-off coincide (no named destination equals the pickup) under USE-7: the input the
  prediction acts on, the destination, is missing.
- Keep the 30 s / 3 h cuts and the weekly windows.

**Sources**

- Uber, DeepETA: How Uber predicts arrival times, https://www.uber.com/en-CA/blog/deepeta-how-uber-predicts-arrival-times/
- DeeprETA: An ETA Post-processing System at Scale, https://arxiv.org/pdf/2206.02127
- OSRM route API, https://project-osrm.org/docs/v5.22.0/api ; OSRM durations caveat,
  https://lists.openstreetmap.org/pipermail/osrm-talk/2017-November/001557.html
- Curb app listing (destination entered, upfront price), https://apps.apple.com/app/id299226386
- Arro app listing (destination, fare estimate, ETA), https://appshunter.io/ios/app/arro/id979943889
- TLC trip record page and data dictionary, https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page
- Kaggle competition, https://www.kaggle.com/c/nyc-taxi-trip-duration

</details>

<details><summary>Blind review</summary>

**Blind review: nyc_taxi_trip_duration**

**Verdict: include with changes.** It is a real, well-known ETA regression task with strong, non-trivial signal and an honest temporal split. The changes are small: document the row filter and check how the raw datetime column is handled.

**Task and use**
A taxi or ride-hailing operator, or a dispatch app, predicts how long a trip will take at the moment it is booked, from the pickup time and the pickup and dropoff points. The prediction is used for ETA quotes, pricing and dispatch. This is a real use. The data is the Kaggle 2016 competition train set (Jan to Jun 2016 Yellow Cab, derived from the NYC TLC records). The target is log1p(seconds), which matches the competition's RMSLE metric.

**What I checked (200k sample)**
- Columns: vendor_id (category, 2 levels), pickup_datetime, passenger_count, and pickup/dropoff lat/lon. There are no missing values and no duplicate rows, including duplicates on the features alone. The data is sorted by time.
- Leakage: none found. The dropoff location is known at booking for ETA use. dropoff_datetime and store_and_fwd_flag were correctly dropped.
- Signal: I trained LightGBM on the first 80% of rows by time and scored it on the last 20%. The test target has a standard deviation of 0.755.
  - With raw features only, RMSE is 0.420.
  - Adding hour, day of week, day of year and straight-line distance brings RMSE to 0.357. This is close to the top Kaggle scores (about 0.37).
  - So the task is far from trivial, and feature engineering matters.

**Concerns (most serious first)**
1. **The rows were filtered on the target without saying so.** Kaggle's train set has 1,458,644 rows; this one has 1,451,706, so 6,938 rows are gone. The durations now run from 30 s to 10,207 s, while the raw data has trips of up to about 3.5M s. Trimming obviously bad labels is defensible, but the rule is not stated in task.md. Changes:
   - State the rule.
   - Make sure it is applied identically to the test windows. A trimmed test set looks easier than real deployment, where models also meet bad rows.
2. **pickup_datetime is a raw datetime64 column.** A model that cannot use datetimes will either drop it or be handicapped. In my test the hour and day features were worth about 0.06 RMSE. Change: confirm how the benchmark encodes this column, or add calendar features.
3. **Minor data oddities.**
   - 0.4% of trips start and end at the same point.
   - 4 rows have passenger_count = 0.
   - A few coordinates are far outside NYC (latitude 40.32 to 41.15).
   - Kaggle states the data was "sampled and cleaned".
   These are plausible real noise and can be kept.
4. **Overlap with other benchmarks.** NYC taxi data is already widespread (for example, the OpenML taxi datasets). This is low concern, because the task here (trip duration) differs from those.

**What I could not check**
- The full 1.45M rows and the exact definitions of the three test windows.
- The exact filter rule.
- Whether the Kaggle data has synthetic noise added to it relative to the TLC records.

</details>

<details><summary>Precedent check</summary>

**nyc_taxi_trip_duration: consistency against the precedents (panel phase A, 2026-10-20)**

Scope: the choices of `datasets/_dev/tabarena-v0pt2/nyc_taxi_trip_duration/dataset.py`, the record's CC line
(`curation/records/nyc_taxi_trip_duration.md`, 2026-09-21) and issues 1-8 of `REVIEW_before.md`.

The run's register: none of its 4 flags touches nyc_taxi_trip_duration. Flag 3 (drift on "scaling over all
rows") names the sibling ETA tasks delivery_eta and maps_router_eta (kept 2026-10-19), but nyc has no all-row scaling,
so it does not apply here. Entries for this dataset: the PROV-12 Cases row (Porto PKDD-15 moved to the comments,
2026-10-12) and the CC of 2026-09-21. No curator decision on nyc other than that CC, so no drift, and no exception
recorded for it, so no third exception.

Status of the precedents: only CC lines and dated Cases rows are curator decisions. The closest sibling,
pkdd_15_taxi_trip_time_prediction_ii_1m, is an AI draft with 10 open issues, but its processing list comes from
Lennart's CC of 2026-09-21. delivery_eta_1m, maps_router_eta_1m and cooking_time_1m (TabReD) ship. zillow_prize and
house_sales are AI drafts from this run. The two taxi sets cite each other (pkdd issues 1, 2, 3, 6; nyc issues 2, 3), so
answer them together.

**Summary**

| # | Decision | Rule | Result |
|---|---|---|---|
| 1 | Ship the Kaggle `train.csv` sample, not a rebuild from uacg-pexx (issue 1) | PROV-8, PROV-11, PROV-13 | consistent |
| 2 | `source` TLC, `year` 2016, bibtex the Kaggle competition; `domain` | PROV-8 to PROV-10 | consistent (one minor gap) |
| 3 | Drop trips < 30 s and > 3 h, a cut on the target (issue 2) | CLEAN-11, CLEAN-15, USE-7, LEAK-26 | consistent |
| 4 | 3 x 7-day windows (issue 3) | SPLIT-15, SPLIT-19 to SPLIT-21 | consistent (two notes) |
| 5 | Hour of day left to the harness (issue 4) | CLEAN-2, CLEAN-19 | consistent with pkdd; family call open |
| 6 | Train sides trimmed per window without `_1m` (issue 5) | definitions.md (house rule) | departs, reason stated; needs an amendment |
| 7 | `store_and_fwd_flag` dropped (issue 6) | LEAK-10, USE-3 | consistent |
| 8 | DST hour repaired, not dropped (issue 7) | PROV-13, remedy ladder | consistent |
| 9 | Licence noted only (issue 8) | EV-4 | consistent |
| 10 | `fit = "direct"` with the recorded dropoff as the named destination | USE-8, USE-9 | departs from pkdd (approximate), no reason given |
| 11 | 46 trips at more than 100 km/h kept | CLEAN-11, USE-7 | pair decided differently (pkdd drops > 120 km/h) |
| 12 | 24 trips with `passenger_count` 0 kept as 0 | CLEAN-10, CLEAN-11 | departs, the stated reason does not cover the value |
| 13 | 38 out-of-box trips dropped; 5,621 one-point trips kept | USE-7, CLEAN-11 | consistent (wording) |
| 14 | Temporal only, `Spatial` as a tag | SPLIT-3, USE-10 | consistent |

**Per decision**

**1. The Kaggle sample, not a rebuild from the TLC records (issue 1): consistent**

Every rebuild from the origin so far was prompted by damage in the copy:

* corporate_credit_rating, rebuilt as corporate_issuer_credit_rating (Lennart, 2026-10-16): wrong labels;
* coad_colon_adenocarcinoma, rebuilt as tcga_coad_molecular_subtype (Lennart, 2026-10-16): scaling over all rows;
* hr_analytics (Cases, 2026-10-14): Kaggle's copy had added mislabelled test rows;
* ashrae_great_energy_predictor_iii (Lennart, 2026-10-15): mixed units.

The nyc sample is not damaged: 8 of 8 rows match uacg-pexx (record, 2026-10-07), and it is the task that was
published. Shipping it follows those precedents. The alternative (a `_1m` from uacg-pexx) would be a rebuild with no
damage behind it. Its other argument, the Kaggle no-redistribution clause, is a licence point, and lucas_topsoil
(Lennart, 2026-09-23) says a licence is not a reason for a verdict. aeolus (Lennart, 2026-10-12, recent flights out of
the full BTS release) is not a counter-precedent: there the source we ship already holds every flight. To choose the
rebuild, name a fact other than the licence, for example that the sample cuts the data in a way the task needs undone.

**2. Source, year, citation and domain: consistent, one minor gap**

`source = "GOV Website"` with the TLC URL follows PROV-8 (a re-upload of a government release takes the original's
source; Lennart, 2026-10-12). The record's own remark that `original_source` "could read Kaggle" (the sample first
appeared there) would hold only if the sample counted as a new dataset. It is a sample of the same records, so PROV-8
gives the TLC. `year = "2016"` follows PROV-9 for that source. The bibtex cites the Kaggle competition, which published
this sample (PROV-10 holds). house_sales was revised in this run to cite both the publisher of the sample (the UW
course) and the origin (King County). nyc cites only the sample. Adding a TLC entry would align the two; this is not a
departure from a rule.

`domain`: the record says `Other`, and every definition in the ETA and transport family says `industry &
manufacturing` (delivery_eta_1m, maps_router_eta_1m, cooking_time_1m, pkdd_15_..._1m, aeolus_1m). The definition is
consistent, and the record field is stale, as it is for pkdd.

**3. Target cuts: < 30 s and > 3 h dropped (issue 2): consistent**

* Upper cut: Lennart's CC on pkdd (2026-09-21) asks to drop "meter-left-on outliers", and pkdd drops trips over 3 h.
  This is the same mechanism (a broken meter or clock) with the same threshold, so nyc follows it. In nyc the evidence
  is stronger: 1,900 of the 2,111 trips over 3 h sit between 22 and 24 h, all VeriFone, at 0.1 km/h, and the TLC fares
  of the sampled ones are for trips of minutes.
* Lower cut: delivery_eta_1m and cooking_time_1m (both ship) drop times under one minute, following TabReD. pkdd drops
  trips under 60 s and states why its threshold differs: nyc's clock has 1-s resolution, pkdd's points are 15 s apart.
* Rule chain: an impossible duration is an impossible target value. Under CLEAN-11 it becomes missing, and under
  CLEAN-15 (Must) a row with a missing target is dropped. A record of under 30 s that starts and ends at one point is no
  ride, so it is no task row (USE-7, the bias_correction case). LEAK-26 (a target cap) does not apply.
* Counter-case: zillow_prize (AI draft, this run) keeps its extreme log errors (miskeyed prices). The fact that sets
  the two apart: nyc has evidence per row that does not come from the target (speed from the coordinates, TLC fares),
  while zillow's extremes can be found only through the target. REVIEW_before cites zillow as the alternative; that
  holds only if this fact is set aside. Keeping all trips "as the competition did" would depart from the pkdd CC.

**4. Weekly windows (issue 3): consistent, with two notes**

7-day windows follow the shipped ETA tasks: delivery_eta_1m, maps_router_eta_1m and cooking_time_1m, all with
`TemporalSplits(window=7, unit="days", n_windows=3)`. pkdd's monthly windows rest on a stated fact (the challenge
tested 1.5 to 6 months after its training year, SPLIT-19). nyc's source sets no horizon (its test set is a random
sample of the same days), so the two taxi sets can differ consistently.

* SPLIT-21 (Must; aeolus, Lennart 2026-10-12): the RMSE comparison in issue 3 (0.422-0.430 against 0.419-0.440) may not
  decide the window length. Decide it from the use case (how often an ETA model is refit).
* SPLIT-20 (Should; aeolus, Lennart 2026-10-12: two-week windows, one of three in the holiday peak): all three weekly
  windows fall in June. Neither the definition nor issue 3 checks whether late June is atypical (the start of summer,
  the end of school). The 28-day alternative spans April to June. This is a check still to do, not a departure.

**5. Hour of day left to the harness (issue 4): consistent with pkdd; family call open**

pkdd's issue 7 is the same question, implemented the same way (raw datetime, no extra column). aeolus_1m adds
minute-of-day columns, but the fact sets it apart: its source holds `hhmm` integers, which it decodes as the authors'
code does. No curator decision exists yet. Answer it once for every dataset whose only time feature is a datetime.

**6. Train sides trimmed per window without `_1m` (issue 5): departs with a stated reason; an amendment is due**

definitions.md, house rule (check table, `splits_train_over_budget`): "a `_1m` version for a frame above 1.5M rows,
otherwise narrower windows". Narrower windows do not shrink the train side, so the rule has no remedy for a frame under
1.5M rows whose train sides exceed 1M. The definition states that fact.

The other 7 accepted `splits_rows_unused` warnings (alfa_battle_2_0_task_2, african_credit_scoring_challenge,
college_scorecard, brazilian_ecommerce, hotel_booking_demand, rosbank1, sf_permit_time) are all by design: a label gap
or labels that were not yet known. nyc is the first case of rows that no split uses because of the budget. It also
samples differently from delivery_eta_1m: an independent 1M per window (`cap_splits`) instead of one random order that
makes the train sides overlap. House rules are never weighed, so the way out is an amendment, not an exception.

```text
**Consistency check (AI, 2026-10-20):** nyc_taxi_trip_duration trims its train sides per window with cap_splits
(129,675 trips in no split), unlike every other accepted splits_rows_unused (label gaps) and unlike the _1m rule of
definitions.md, which delivery_eta_1m follows (one random order, the frame reduced to the rows used). What sets it
apart?
(a) the frame is under 1.5M rows while its train sides exceed 1M, a case the rule does not cover, recorded as a
one-off; (b) treat it like delivery_eta_1m: allow subsample_to_budget / sample_temporal_splits under its own name;
(c) rename it nyc_taxi_trip_duration_1m with version_of; (d) amend definitions.md: temporal frames under 1.5M rows with
train sides over 1M use sample_temporal_splits.
```

**7. `store_and_fwd_flag` dropped (issue 6): consistent**

This is the LEAK-10 Cases row "a column recorded after the outcome, drop it" (kickstarter `staff_pick` and `profile`,
hotel `BookingChanges`). The competition keeping the flag in its test.csv is the source's own choice. It does not
override the prediction point (USE-1, the kickstarter lesson).

**8. DST hour repaired, not dropped (issue 7): consistent**

The remedy ladder puts repair before dropping, and PROV-13 says to repair from the origin. Similar cases: ashrae
(units repaired) and pkdd issue 9 (UTC converted to local time, the same kind of clock repair).

**9. Licence noted only (issue 8): consistent**

lucas_topsoil (Lennart, 2026-09-23) and zillow_prize issue 7 handle the licence the same way: noted, never a reason for
a verdict.

**10. `fit = "direct"` with the recorded dropoff as the destination: departs from pkdd, no reason given**

Both taxi sets use the same stand-in: the point where the trip ended is taken as the destination named at pickup. Both
framings come from Lennart's CCs of 2026-09-21. pkdd writes `fit="approximate"`, nyc writes `fit="direct"`. USE-8 lists
"a stand-in with a known gap" as approximate. The difference pkdd names (its source says drivers do not enter the
destination) is a statement about Porto's dispatch system. NYC yellow cabs in 2016 also had no destination entry, and
nyc's `task_summary` says "the taxi's system estimates the arrival time". The checklist already notes this (P3, "a
panel may weigh whether that is direct or approximate").

```text
**Consistency check (AI, 2026-10-20):** your framing of nyc_taxi_trip_duration (fit direct, the recorded dropoff
standing in for the destination named at pickup) differs from pkdd_15_taxi_trip_time_prediction_ii_1m (fit approximate,
the same stand-in, the same CC date 2026-09-21). What sets nyc apart?
(a) a street-hail passenger in NYC names the destination to the driver, and the Kaggle organisers kept the dropoff
coordinates on purpose as that destination, recorded as the reason for direct; (b) treat nyc like pkdd: approximate;
(c) reopen pkdd as direct; (d) amend USE-8 to say how a recorded endpoint used as a named destination is rated.
```

**11. 46 trips at more than 100 km/h kept: pair decided differently**

nyc keeps them as anomalies ("cannot be told from real trips with certainty"). pkdd drops 741 trips with a straight
line faster than 120 km/h (its issue 2b, open). pkdd gives a fact: 725 of the 741 have a GPS jump of more than 1 km
between two 15-s points, so the label is broken. nyc has no trajectory to show this. Both are open AI drafts, so this
is a pair to settle together, not a curator departure.

```text
**Consistency check (AI, 2026-10-20):** nyc_taxi_trip_duration keeps its 46 trips faster than 100 km/h;
pkdd_15_taxi_trip_time_prediction_ii_1m drops its 741 faster than 120 km/h. What sets them apart?
(a) pkdd can show the error on each trip (a GPS jump between consecutive points), nyc cannot, so nyc keeps them under
CLEAN-11 ("values that are only unusual stay"), recorded on both; (b) treat nyc like pkdd: drop them; (c) treat pkdd
like nyc: keep them; (d) amend CLEAN-11 with a speed rule for trip data.
```

**12. `passenger_count` 0 kept as 0: departs, the stated reason does not cover the value**

CLEAN-10 and CLEAN-11 (Should) turn a proxy-missing or impossible value into missing and keep the row. The Cases
include heart_disease_va_long_beach (`chol == 0`: missing). In this run house_sales and zillow_prize make 0 bedrooms or
0 bathrooms missing. The definition's reason ("cannot be told from real trips") is an argument for keeping the row,
which CLEAN-11 also does. It is not an argument for keeping the value 0. The effect is small (24 rows, P7).

```text
**Consistency check (AI, 2026-10-20):** nyc_taxi_trip_duration keeps passenger_count 0 on 24 trips, unlike
heart_disease_va_long_beach (chol 0 made missing) and house_sales and zillow_prize (0 bedrooms made missing). What sets
it apart?
(a) 0 is what the driver keyed in and a model in deployment would see the same entry, recorded as an exception to
CLEAN-10 (serves P3); (b) treat it like the precedents: passenger_count 0 becomes missing; (c) reopen the precedents;
(d) amend CLEAN-10.
```

**13. 38 out-of-box trips dropped; 5,621 one-point trips kept: consistent (wording)**

Dropping rows with impossible coordinates would go against CLEAN-11 ("the row stays"). Here the dropoff point is the
input the ETA acts on (the destination), so a trip without a plausible one is no task row under USE-7 (bias_correction,
Lennart 2026-10-15). pkdd drops out-of-city starts on Lennart's CC. The definition gives "GPS errors" as the reason;
citing USE-7 would make the link to the rule explicit. Keeping the one-point trips matches pkdd issue 3 (kept, open):
a filter on a feature that a deployment could apply, with no evidence that the label is broken.

**14. Temporal only, `Spatial` as a tag: consistent**

This follows the Temporal-against-grouped tension (one regime, the one the use case implies; Lennart, 2026-10-12) and
house_sales (temporal, spatial as a tag).

**For the curator**

Four prompts above: #6 (an amendment of the budget rule is due), #10 (fit, nyc against pkdd), #11 (the speed filter,
nyc against pkdd), #12 (passenger_count 0). Issues 1, 2, 3, 6, 7 and 8 follow the precedents. For issue 3, decide
without the RMSE comparison (SPLIT-21) and check June for an atypical season (SPLIT-20). For issue 4, one call covers
the whole family. pkdd and nyc point to each other on five issues, so settle them in one sitting.

</details>

<details><summary>Advocate</summary>

**nyc_taxi_trip_duration: advocate's opening brief (ship as defined), 2026-10-20**

Position: ship. Every validity rule (P1-P5) holds or is fixed by a one-line change to the definition; nothing calls
for a rebuild or for retiring the dataset. Where the auditors found a real problem I concede it and name the mildest
fix (remedy ladder: fix the definition before keeping with a note, keep with a note before excluding).

**1. A real use case, and the dropoff stand-in costs nothing measurable (P3; USE-1, USE-3, USE-8 Must)**

- Evidence: the practitioner rates the fit direct (borderline approximate): "one row is one ride whose pickup time,
  pickup point, destination, passenger count and vendor I have when the quote is made". The blind reviewer, who read
  none of our files, independently calls it "a real, well-known ETA regression task" and says the dropoff "is known at
  booking for ETA use". The claim audit tested the stand-in: dropoff rounded to ~200 m gives RMSE 0.382/0.364/0.375
  against 0.379/0.365/0.375 exact. A destination at block level carries all the skill, so the model uses no GPS detail
  of the disengagement.
- The stand-in rests on the curator's CC (2026-09-21), which outranks an AI assessment (Precedence: who decides).
- Against "fit should be approximate, as pkdd" (precedents #10): the measured gap is the one-point rows (point 6);
  once those go, the recorded dropoff equals the destination for every real ride, which is USE-8's "direct". If the
  curator still wants pkdd's word, it is a one-field change; the data and split stay. Not a reason to hold the
  dataset.
- The practitioner's gap 1 (no router estimate, USE-6) makes the task harder, not unreal: USE-6 says such an input is
  legitimate when it exists; it does not here, and inventing one is not cleaning (practitioner: "do not invent").

**2. The split mirrors the application (P4; SPLIT-1 Must, SPLIT-11, SPLIT-12)**

- Evidence (split audit): weekly windows match the stated weekly refit and the shipped ETA siblings
  (delivery_eta_1m, maps_router_eta_1m, cooking_time_1m all `window=7`, precedents #4); test windows 52,963-54,713 rows,
  strictly after train; the random hold-out is optimistic by 0.013-0.029 RMSE, so temporal is the right regime;
  hidden groups 0, near copies 0.0% of test rows seen; exact feature copies across the split 0.0% (claim audit); no
  end censoring (127 raw trips drop off on 07-01).
- Against "3 x 28 days" (REVIEW issue 3): SPLIT-21 (Must) bars deciding from the RMSE comparison; the use case (weekly
  refit, SPLIT-12) decides, and it says 7 days.
- Conceded, SPLIT-9 (Must): 58 / 90 / 99 train rows per window were still running at the window start. Effect within
  noise (0.346/0.333/0.345 vs 0.349/0.335/0.345), so no shortcut, but a Must holds on its own. Mildest fix: `gap=1`
  in `TemporalSplits` (supported by the API) or a filter on pickup + duration; no re-design.
- SPLIT-20 (Should; no full season): the source holds only January-June 2016, so no remedy exists; keep with the
  note. The "latest trips" wording in `use_case` vs a random 1M since January: reword the text (split audit 2), no
  re-split (latest 1M scores the same, and SPLIT-21 bars deciding from it anyway).

**3. No leak in the shipped features (P4; LEAK-10 Must, LEAK-16)**

- Evidence: `dropoff_datetime` (= pickup + target) and `store_and_fwd_flag` (sent after the trip; Y only on CMT
  meters, 8,045 trips) are dropped; column audit: "No leak found in the shipped features beyond the curator-approved
  dropoff stand-in"; blind review: "Leakage: none found". Dropping the flag follows the LEAK-10 Cases (kickstarter
  `staff_pick`, hotel `BookingChanges`); the competition keeping it in test.csv does not override the prediction
  point (USE-1).
- Against REVIEW issue 6 (keep the flag): its effect is 0.001-0.003 RMSE, and P4 outranks fidelity to the
  competition's columns.

**4. Faithful data from the origin, repaired where it was wrong (P5; PROV-1, PROV-8, PROV-13)**

- Evidence: sha256 matches; 5 of 5 further train rows (and 8 of 8 earlier) match the TLC records on NYC Open Data
  uacg-pexx to the second and 1e-6 degrees. The DST repair is confirmed on the data: trips recorded >= 60 min in the
  01:00 hour are 0 / 87 / 0 on Mar 6 / 13 / 20; median 11.85 -> 10.58 min after the fix. Repair before drop is the
  remedy ladder's first rung.
- Against REVIEW issue 1 (rebuild from uacg-pexx): every rebuild so far answered damage in the copy (corporate_credit
  _rating, coad, hr_analytics, ashrae; precedents #1); this sample is undamaged and is the published task. The other
  argument, the Kaggle no-redistribution clause, is a licence point and never evidence (EV-4; lucas_topsoil).
- Conceded: claim 47 (TLC Parquet has 2016 coordinates) is refuted; a CC line superseding it (the 2026-10-07
  assessment already says so). Record text only.

**5. The target filters remove data errors, shown by evidence other than the target (P7 serving P3; CLEAN-11, CLEAN-15 Must, USE-7)**

- Evidence: under 30 s, 63% of trips start and end within 10 m (72% under 10 s); over 3 h, 1,900 of 2,111 sit at
  22-24 h, 100% VeriFone, median 0.10 km/h, and the TLC fares of looked-up trips are $13-$52 for 2-18 miles; the trip
  count falls smoothly to 18 per 20 min at 3 h. Together 0.47% of rows.
- Rule chain: an impossible duration is an impossible target (CLEAN-11), so the row goes (CLEAN-15); a non-ride is no
  task row (USE-7). Follows the curator's own pkdd CC (2026-09-21: drop "meter-left-on outliers", 3 h cap) and the
  shipped delivery_eta_1m / cooking_time_1m lower cuts (precedents #3).
- Against "the test windows then score only normal trips" (blind review 1, split audit 4): the practitioner,
  playing the actor, says "a quote never targets a 23 h clock error" and his monitoring would exclude these records
  too. Against zillow_prize keeping its extremes: nyc has per-row evidence outside the target (speed, fare, vendor),
  zillow does not, which sets the cases apart.
- The blind reviewer's "the rule is not stated" holds only for its clean room; the definition states it in
  `curation_comments` and a decision table.

**6. Worth benchmarking (P6; TP-2) and the hour question is the harness's, not the data's**

- Evidence: 1,451,706 rows, three test windows of 53k-55k, test std 0.75 against RMSE 0.36-0.43 for untuned LightGBM;
  the blind reviewer's own model moves from 0.420 to 0.357 with engineered time and distance features: "far from
  trivial, and feature engineering matters". A large, real, strongly structured regression the collection otherwise
  lacks at this size.
- Against REVIEW issue 4 (hour lost under `default`): the definition ships the raw datetime as the source has it, as
  pkdd does (precedents #5); `tabarena_default` keeps the hour (0.380/0.365/0.378). It is one call for every
  datetime-only dataset, at harness level, and changes no row of this one.

**7. The remaining findings are small, and each has a cheap fix that keeps the dataset**

- USE-7 (Must), one-point trips: 4,539 trips (0.31%) with identical pickup and dropoff coordinates lack a usable
  destination (column audit: 3.1-3.7% of squared error; RMSE 0.353/0.341/0.360 -> 0.346/0.330/0.354 without them).
  Conceded: drop the exact-identity rows, a one-line filter, as bias_correction dropped its days without the LDAPS
  run. This also settles the fit question of point 1.
- CLEAN-10 / CLEAN-11 (Should), passenger_count 0 (24 rows) and 8/9 (2 rows): conceded, set to missing and keep the
  rows, as heart_disease_va_long_beach, house_sales, zillow_prize (precedents #12). P7, negligible effect.
- 46 trips over 100 km/h: keep. CLEAN-11 keeps values that are only unusual; nyc has no trajectory to show the label
  is broken, which is the fact that sets it apart from pkdd's 741 GPS jumps (precedents #11).
- EV-8 (Should), splits_comment numbers: name the encoding and setup, give 0.365-0.379 (hour kept) next to
  0.414-0.434 (date parts), and say the random-split optimism is mostly temporal distance, about 0.01 day-sharing
  (claim audit refuted 1). Text only.
- House rule on the 1M budget (REVIEW issue 5, precedents #6): a gap in the rule, not in the data; the definition
  states the reason. House rules are never weighed, so the curator amends the rule (option d) or renames to `_1m`; the
  data and windows stay either way. The record's `domain` (`Other`) is stale; the definition matches the family.

**Judgment record (advocate)**

```text
Verdict: ship after small changes to the definition.
Validity: SEL holds; USE-1/USE-3 hold, USE-8 direct (CC 2026-09-21, stand-in measured at block level), USE-7 triggered
on 4,539 one-point rows, fixed by a filter; LEAK-10 fixed (flag and dropoff time dropped); SPLIT-1 holds; SPLIT-9
triggered on 58-99 rows per window, fixed by gap=1; PROV-1 holds (rows match uacg-pexx), PROV-13 DST repaired.
Value: TP-2, strong signal, not trivial.
Quality: CLEAN-10/11 passenger_count 0 and 8/9 to missing; target cuts follow CLEAN-11 -> CLEAN-15 and the pkdd CC.
Weighed: size +, source +, sibling consistency +, half-year history -.
For the curator: the 1M-budget house rule amendment; fit word (direct vs pkdd's approximate); harness hour (family call).
```

**nyc_taxi_trip_duration: advocate's rebuttal (2026-10-20)**

The critic and I agree on the verdict (ship after changes, no exclusion, no rebuild). We also agree on its "not
argued" list: the Kaggle sample, the 30 s / 3 h cuts, the weekly windows, the dropped flag, the DST repair and the
licence. What is left is points 2, 4 and 5, and only in how far they reach.

**1. One-point trips (USE-7 Must): conceded**

Agreed in full: drop the 4,539 rows whose pickup and drop-off are identical, keep the ones within 10 m but not
identical as unusual values (CLEAN-11), and say so in curation_comments. The critic adds that "drop-off = pickup" is
post-trip information (mean target 5.77 vs 6.48, claim audit row 5). That makes the fix stronger, not optional.

**2. `fit = "direct"` (USE-8 Must): disputed in part**

- Conceded: while the one-point rows stay, there is a known gap, so `direct` needs point 1 fixed first. The critic
  says the same ("with point 1 fixed, `direct` becomes more defensible").
- Disputed: that the missing router estimate or live traffic makes the fit approximate. USE-8's list of stand-ins
  covers what the rows *carry*: a snapshot for a forecast, a leak kept on purpose, a reconstructed time axis, one
  judge for the market. A legitimate input the source never held is none of these. USE-6 says such an input may be
  used when it exists. It does not say a task without it is a stand-in. The practitioner, who raised the gap, still
  rates the fit direct and calls the gap "harder rather than unreal". The drop-off as destination is measured to carry
  no detail of the disengagement: rounded to 200 m it scores 0.382/0.364/0.375 against 0.379/0.365/0.375 (claim audit
  row 5).
- What follows: once point 1 is fixed, keep `direct`. Record the fact that sets nyc apart from pkdd in fit_reason
  (once the GPS failures are gone, the recorded drop-off is the destination of every ride; the router is named as
  absent), answering the consistency check of precedents #10. If the curator prefers pkdd's word, it is a one-field
  change. It is the curator's weighing call, not a Must failure.

**3. Unknown labels in train (SPLIT-9 Must): conceded**

Agreed: fix it in the definition. One detail: the gap of `TemporalSplits` is counted in the unit, here days, so the
smallest gap is `gap=1` (1 day). It removes about 7-8k train trips per window from 1.29M-1.40M eligible (the train
side is still capped at 1M), so it costs nothing. The train filter on pickup + duration < window start is the
tighter alternative if the API takes it. Either is the mildest rung. State the gap in splits_comment.

**4. Hour of day under `default` (CLEAN-2 Must): disputed as a condition for shipping this dataset**

- Agreed on the facts (0.379/0.365/0.375 vs 0.425/0.414/0.434) and on the remedy: no change to the definition.
- Disputed: CLEAN-2 is not broken here. CLEAN-2 says to leave the encoding to the pipeline, and the definition does
  exactly that. A rule that the definition meets cannot make shipping depend on it. The question is which pipeline
  v0.2 runs. That is a harness setting, and it touches every dataset whose only time feature is a datetime (pkdd in
  the same way, precedents #5). Tying it to nyc alone would treat like cases unlike.
- What follows: it goes to the curator as one call for the whole family, listed in REVIEW.md. It is not a gate on
  this folder.

**5. Train sides trimmed outside the house rule: conceded on process, disputed on reach**

- Conceded: house rules are never weighed, and an accepted warning cannot stand as an exception to one. This needs
  the curator's amendment of definitions.md, or a rename to `_1m`.
- Disputed: "open, not accepted" applies to the rule's text, not to the data. Every way out (amend for
  `sample_temporal_splits`, rename to `_1m`, keep cap_splits) leaves the same frame, the same windows and a random 1M
  of earlier trips. No P3 to P5 rule is touched, and the split audit finds the train side right (SPLIT-14). So it
  holds no validity change. It is an item for the curator next to the dataset, not a reason to hold it.

**6. Notes misstate the scores and the cause (EV-8, EV-6): conceded**

The same as my point 7. Rewrite splits_comment with the encoding and the setup, and give the hour-kept numbers
(0.365-0.379) next to the date-part numbers. Say the random-split optimism is mostly temporal distance and about 0.01
day-sharing. Reword the use case to "trips since January". Add a superseding CC line for the Parquet claim. Text only.

**7. passenger_count 0, 8, 9 (CLEAN-10 / CLEAN-11 Should): conceded**

Set them to missing and keep the rows, as the precedents did (precedents #12). This is P7 and negligible.

**Net**

Changes to make now, agreed by both sides: point 1, point 3, point 6, point 7. For the curator: the fit word
(point 2, a weighing call once point 1 is fixed), the harness pipeline (point 4, one call for the whole family) and
the budget rule amendment (point 5, a house rule). None of them is a reason not to ship.

</details>

<details><summary>Critic</summary>

**nyc_taxi_trip_duration: critic, opening brief (2026-10-20)**

**Position: ship only after changes.** The task is real (an ETA at pickup) and the temporal split is right; nothing
here argues for exclusion. Two Musts of P3 and one of P4 are broken in small but fixable ways, and the notes misstate
what the shipped encoding scores. Points in rank order (P3, P4, then house rule, procedure, P7).

**1. Rows with no destination are kept (P3, USE-7 Must)**

* **Problem.** 4,539 trips (0.31%) have dropoff coordinates identical to the pickup (5,621 within 10 m). The prediction
  acts on the named destination; nobody names the pickup point as destination, so these rows lack the input (a GPS
  fault at drop-off, 73% VeriFone). The definition keeps them as "cannot be told from real trips", but identical
  float32 coordinates (about 1 m) are not a real round trip.
* **Effect.** 181-185 test rows per window with RMSE 1.08-1.15 against 0.336-0.355 elsewhere; 3.1-3.7% of the squared
  error. Worse, "dropoff = pickup" is itself post-trip information (mean target 5.77 vs 6.48), so the model is scored
  partly on recognising a recording fault, not on an ETA.
* **Evidence.** column_audit.md problem 1 (LightGBM 400 trees, weekly windows: 0.353/0.341/0.360 shipped vs
  0.346/0.330/0.354 without them); claim_audit.md row 5 (residual); practitioner.md section 3 and "What an expert would
  change".
* **Remedy.** Fix the definition: drop the rows whose pickup and dropoff coordinates are identical (USE-7, as
  bias_correction drops the days without the forecast), and say so in curation_comments. Rows within 10 m but not
  identical can stay as unusual values (CLEAN-11).

**2. `fit = "direct"` with a stand-in named in the fit reason (P3, USE-8 Must)**

* **Problem.** fit_reason says the recorded dropoff point "stands in" for the destination. USE-8 lists "a stand-in with
  a known gap" as approximate. The sibling pkdd_15_taxi_trip_time_prediction_ii_1m uses the same stand-in from the same
  CC (Lennart, 2026-09-21) and writes `approximate`. The practitioner rates it "direct (borderline approximate)" and
  names a larger gap: no router estimate or live traffic, which every production ETA has (USE-6).
* **Effect.** The fit field tells benchmark users this mirrors deployment; it does not quite.
* **Evidence.** precedents.md decision 10 (consistency check drafted); column_audit.md problem 2; practitioner.md gaps
  1-2; checklist P3 row.
* **Remedy.** Set `fit = "approximate"` and name the gap ("the drop-off point stands in for the named destination; no
  routing estimate"), or, if the curator keeps `direct`, record the fact that sets nyc apart from pkdd (consistency
  check, principles.md). With point 1 fixed, `direct` becomes more defensible; without it, it is not.

**3. Training rows whose label is not known at the window start (P4, SPLIT-9 Must)**

* **Problem.** 58 / 90 / 99 train rows per window are picked up before the window start and drop off after it.
* **Effect.** Negligible on the score (0.346/0.333/0.345 vs 0.349/0.335/0.345, within single-fit noise), but SPLIT-9 is
  a Must and an independent failure is not rescued by its size (principles.md, How to decide, step 4).
* **Evidence.** split_audit.md problem 1.
* **Remedy.** Fix the definition at no cost: a gap of the label's maximum delay (3 h, or the smallest unit the
  `TemporalSplits` gap takes), or a train filter on pickup + duration < window start (SPLIT-10). State the gap in
  splits_comment. Keeping it with a note is the fallback only if the API cannot express it.

**4. The hour of day reaches the model only under one pipeline (benchmark validity of the time signal; CLEAN-2 Must)**

* **Problem.** pickup_datetime is the only time feature. Under `tabarena_default` (skrub, keeps the hour) LightGBM
  scores 0.379/0.365/0.375; under `default` (AutoGluon date parts, loses the hour) 0.425/0.414/0.434. The practitioner
  calls hour-of-week the first feature of any ETA.
* **Effect.** Under `default` the benchmark measures the datetime encoding more than the methods. CLEAN-2 forbids
  adding a hand-made hour column, so the definition cannot fix it.
* **Evidence.** claim_audit.md row 33 (re-run, setup stated); blind_review.md concern 2 (about 0.06 RMSE from hour and
  day features); practitioner.md gap 3; REVIEW_before issue 4.
* **Remedy.** No definition change. A condition for shipping: the curator confirms which pipeline v0.2 runs; if
  `default`, a harness change for the whole family of datetime-only datasets (precedents.md decision 5), not an extra
  column here.

**5. Train sides trimmed per window outside the house rule (house rule, definitions.md; never weighed)**

* **Problem.** cap_splits draws an independent 1M per window; 129,675 trips (8.9%) are in no split. The `_1m` rule of
  definitions.md has no remedy for a frame under 1.5M rows whose train sides exceed 1M; nyc is the first such case and
  samples differently from delivery_eta_1m. An `accepted_check_warnings` entry is in effect an exception to a house
  rule, which house rules do not admit.
* **Evidence.** precedents.md decision 6; claim_audit.md row 40; REVIEW_before issue 5.
* **Remedy.** An amendment of definitions.md by the curator (option d of the drafted consistency check), then apply it
  here. Until then this is open, not accepted.

**6. The notes misstate the scores and the cause (procedure, EV-8 Should, EV-6; SPLIT-20 Should for the wording)**

* **Problem.** splits_comment says random 3-fold 0.396-0.399 vs weekly 0.419-0.440 "probably because trips of one day
  share traffic and weather". Those are AutoGluon-date-part numbers, not the shipped encoding (hour kept: weekly
  0.365-0.379), with no setup named. A by-day grouped split shows day-sharing explains about 0.01 of the gap; the rest
  is temporal distance. The use case says "refit every week on the latest trips", but train is a random 1M of all
  trips since January. The record's CC of 2026-09-21 says TLC Parquet serves 2016 coordinates; it does not.
* **Evidence.** claim_audit.md refuted 1 and 2; split_audit.md problem 2.
* **Remedy.** Rewrite the notes: name the encoding and the setup (300 trees, 63 leaves, random 200k), give the
  hour-kept numbers, say the random-split optimism is mostly temporal distance. Reword the use case to "on the trips
  since January" (no re-split). A superseding line in the record for the Parquet claim.

**7. Proxy-missing and impossible passenger counts (P7, CLEAN-10 / CLEAN-11 Should)**

* **Problem.** passenger_count 0 on 24 trips (not entered), 8 and 9 on 2 trips (above a yellow cab's capacity), kept
  as numbers. The stated reason ("cannot be told from real trips") argues for keeping the rows, which CLEAN-11 also
  does, not for keeping the values. heart_disease_va_long_beach, house_sales and zillow_prize made such values missing.
* **Effect.** Negligible on the score; a quality point, no reason to hold the dataset.
* **Evidence.** column_audit.md problem 3; precedents.md decision 12.
* **Remedy.** Set 0, 8 and 9 to missing and keep the rows; or the curator records an exception (the driver's entry is
  what a deployed model would see, P3).

**Not argued**

The Kaggle sample over a TLC rebuild (precedents.md 1, no damage), the 30 s / 3 h cuts (decision table, fares checked,
precedent pkdd CC; the practitioner accepts them), the weekly windows (SPLIT-12; SPLIT-21 bars deciding from RMSE),
dropping store_and_fwd_flag, the DST repair, and the licence (EV-4): the evidence supports the definition on each.

**nyc_taxi_trip_duration: critic, rebuttal (2026-10-20)**

The two briefs now agree on the verdict (ship after changes to the definition) and on most of the changes: drop the
one-point rows (USE-7), add a gap (SPLIT-9), make passenger_count 0, 8 and 9 missing (CLEAN-10/11), rewrite the
splits_comment numbers (EV-8), reword "latest trips", supersede the record's Parquet CC line, and leave the house rule
to a curator amendment. Two points stay open, and both are about wording or process, not about the data.

**Advocate 1. Use case and fit: partly disputed**

* Conceded: the use case is real (USE-1, USE-3). The 200 m rounding test (claim_audit.md row 5: 0.382/0.364/0.375 vs
  0.379/0.365/0.375) shows that the model takes no GPS detail from the disengagement point. Missing router and traffic
  inputs make the task harder, not unreal (USE-6). I do not ask to invent them.
* Disputed: "once the one-point rows go, the dropoff equals the destination for every real ride, so direct". That is
  asserted, not measured. A recorded endpoint differs from the named destination whenever a passenger changes the
  destination or gets out early, and the data cannot show how often that happens (EV-6: a claim without a test is a
  question). USE-8 (Must) lists "a stand-in with a known gap" as approximate, and the definition's own fit_reason
  calls the dropoff a stand-in. pkdd writes `approximate` for the same stand-in under the same CC (precedents.md
  decision 10). Treating like cases alike (principles.md, Conflicts) means one of the two changes, or the curator
  records the fact that sets them apart.
* The advocate's appeal to the CC (2026-09-21) does not settle this. The CC set the framing (the dropoff stands in for
  the destination), and both briefs accept that framing. It did not set the fit word, and the pkdd CC of the same day
  produced `approximate`.
* What I ask: a curator call between `approximate` (my preference, matching pkdd and the fit_reason text) and `direct`
  with the distinguishing fact recorded. The data and the split stay either way. Not a reason to hold the dataset.

**Advocate 2. Split: conceded**

* Weekly windows, the temporal regime and SPLIT-21 against deciding from RMSE: agreed.
* SPLIT-9 is fixed by `gap=1`. One note: a 1-day gap removes about 7-8k trips per window from the train candidates.
  This is harmless under the 1M cap, but the gap has to be stated in splits_comment as part of the task (SPLIT-10).
* SPLIT-20 kept with a note, and the use-case wording reworded: agreed.

**Advocate 3. No leak in the shipped features: conceded, with one qualification**

* The qualification: the one-point rows carried post-trip information (mean target 5.77 vs 6.48; claim_audit.md
  row 5). The advocate's own point 7 removes them, so the claim holds after the fix and not before it.

**Advocate 4. Provenance and DST repair: conceded**

* Ship the Kaggle sample (precedents.md decision 1).
* Keep the DST repair (PROV-13, remedy ladder).
* Add a superseding CC line for claim 47.

**Advocate 5. Target filters: conceded**

* I did not argue against the filters. The per-row evidence outside the target (speed, fares, vendor) sets nyc apart
  from zillow_prize.

**Advocate 6. Value and the hour of day: agreed in substance, one difference**

* TP-2 holds.
* On the hour, I agree it is a harness call and no definition change (CLEAN-2 Must forbids a hand-made hour column).
  The difference is in status. The advocate treats it as a family question with no effect on shipping. I hold that
  the curator confirms the pipeline before this dataset's scores are compared. Under `default`, 0.04-0.06 RMSE of the
  task's signal depends on the encoding (claim_audit.md row 33; blind_review.md concern 2), so the benchmark would
  measure the encoding, not the methods. The advocate lists it under "For the curator", so the gap between us is
  wording.

**Advocate 7. Small findings**

* One-point rows (USE-7), passenger_count, the EV-8 text: conceded on both sides.
* 46 trips over 100 km/h: conceded. I did not raise them, and CLEAN-11 keeps values that are only unusual when the data
  cannot show that the label is broken (precedents.md decision 11).
* House rule: partly disputed. "The definition states the reason" does not make the accepted warning sufficient: house
  rules are never weighed (principles.md), so the warning stays open until the curator amends definitions.md or
  renames the dataset to `_1m`. The advocate names the same two ways out, so only the status differs (open, not
  accepted).
* Record `domain`: conceded. It is stale; set it to `industry & manufacturing`.

**Remaining for the mediator**

1. Fit word: approximate vs direct with a recorded fact (USE-8 Must, consistency with pkdd).
2. The hour pipeline as a pre-ship confirmation vs a family note (CLEAN-2).
3. The budget warning: open until amended vs accepted with a reason (house rule).

</details>
