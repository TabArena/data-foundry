# pkdd_15_taxi_trip_time_prediction_ii

**Outcome:** added as `pkdd_15_taxi_trip_time_prediction_ii_1m`; the AI recommends shipping it with the changes made
in this review. Not built: the README's build record is empty.
Validity: USE-8 (Must) approximate, the realised drop-off stands in for a destination named at pickup; USE-7 (Must)
triggered and fixed by dropping the trips that end at their start point (90 in the cleaned data, 76 of them in the
sampled frame the panel counted); SPLIT-9 (Must) triggered and fixed by a one-day gap (48 / 36 / 8 train trips per
window ended after the window start, now none); SPLIT-3 holds (temporal, the taxi a feature); SPLIT-20 departed from
with a note (one year of data, so the April to June test season has no earlier copy in train).
Value: the task probe's LightGBM reaches R² 0.37 against 0.04 for a linear model, a larger LightGBM with the local
hour 0.51 to 0.54; over 130k test trips per window.
Quality: the short-trip cut stays at 60 s with its slope written down (issue 2); the ORIGIN_CALL reason is reworded
(CLEAN-22); the quoted scores are re-measured.
Weighed: size +, source +, consistency with nyc_taxi_trip_duration +; destination not recorded at pickup in the
source -, no routing estimate -, one year of history -.
Open: the reason for the destination framing (issue 1; the AI and both sides of the panel recommend keeping it, as
approximate like nyc) and the short-trip cut (issue 2; the panel left it open, the AI recommends 45 s).

**Main points:** Keep the destination as a feature for a reason the rules accept, and choose the short-trip cut (60,
45 or 30 s). The hour-of-day encoding is decided in the cross-dataset item "Which datetime encoding the v0.2 runs
use".

**Record fields that disagree with the definition:**

- `domain`: record `Other`, definition `industry & manufacturing`.

**Issues for Lennart:**

1. **Framing: the reason for keeping the destination as a feature.**
   - Problem: the task predicts the travel time at pickup from the start, the destination and the time. The
     destination is the trip's last GPS point, recorded when the trip ends. The source says the drivers do not enter
     the destination in the dispatch system: the challenge overview (geolink.pt) says "In most cases, taxi drivers
     operating through an electronic dispatch system do not indicate the final destination of the ride"; that wording
     could not be re-fetched in this review, but Lam et al. 2015 (https://arxiv.org/abs/1509.05257), Sec. 1, confirm
     the meaning: "busy taxi drivers do not report the final destination of the ride".
   - Effect: the task stands for an ETA once the passenger names the destination (an app booking, a quote at
     pickup). The realised drop-off is more exact than a named one, so the scores are somewhat optimistic for that
     use. The definition marks the fit `approximate` and names this gap (USE-8, Must).
   - Rule: your CC of 2026-09-21 kept the destination because the pickup-only task has a weak signal (R² 0.14). TP-2
     (Should, 2026-10-06) no longer accepts a weak signal as a reason to choose a framing. TP-6 (Must) says a version
     the source itself defines replaces ours; the source defines only partial-trajectory tasks, so TP-6 does not force
     pickup-only.
   - Evidence: LightGBM (800 trees, learning rate 0.08, 255 leaves, local hour, weekday and day of year, one fit per
     split) reaches R² 0.54 / 0.51 / 0.53 with the destination and 0.13 / 0.12 / 0.15 without it (June / May / April
     windows).
   - Implemented: (a) your framing, `fit="approximate"`, with the gap as the reason and the pickup-only score as a
     stated fact. `nyc_taxi_trip_duration` ships the same framing as `approximate` (its review panel of 2026-10-20,
     not yet decided by you). Cost: the scores rest on a destination more exact than a named one.
   - Alternatives: (b) pickup-only for pkdd, and reopen nyc, since both rest on the same fact; cost: `end_lon` and
     `end_lat` go, R² falls to 0.12 to 0.15, nyc must be decided again, and the dropped ORIGIN_CALL comes back into
     question (pickup-only it adds +0.005 to +0.007 R², same setup). (c) pickup-only for pkdd alone; cost: it needs
     a fact that sets pkdd apart from nyc, and none is known. (d) amend USE-8 or TP-6; cost: a rule change for every
     dataset.
   - The advocate and the critic both say keep the framing; the blind reviewer, who had no notes, read the task as a
     real origin-destination ETA.
   - Recommendation: (a), with the reason "an ETA once the passenger names the destination, approximate as nyc".
   - Decision: the framing and its reason, (a), (b), (c) or (d).

2. **Short trips: cut at 60 s, 45 s or 30 s?**
   - Problem: trips whose recorded travel time is under 60 s are dropped, in test too, as a meter switched on and off
     without a ride. The travel time is (GPS points - 1) x 15 s, so a recorded 45 s is about 45 to 75 s of real time
     (the meter can run up to 15 s before the first and after the last point). A cut on the target cannot be applied
     in deployment, so it has to rest on evidence outside the target (USE-7, Must: only rows that are no task leave;
     CLEAN-11, Should: unusual values stay).
   - Effect: the dropped trips are 0.9% of the rows but carry 20% of the target's squared spread around its mean, so
     they would weigh heavily in the RMSE. A real short ride dropped from test makes the benchmark easier than the
     task.
   - Evidence, measured with all other filters on, the identical-endpoint filter included, so the counts are slightly
     below the mediator's table (1.9% of all trips end within 100 m of their start):

     | Recorded time | Trips | End within 100 m | Median straight line |
     |---|---|---|---|
     | 15 s | 6,945 | 71% | 32 m |
     | 30 s | 4,270 | 53% | 84 m |
     | 45 s | 3,367 | 41% | 157 m |
     | 60 s (kept) | 3,148 | 32% | 250 m |
     | 120 s | 4,279 | 7% | 714 m |

     Among the trips each cut drops, 71% end within 100 m at 30 s (6,945 trips), 64% at 45 s (11,215) and 59% at
     60 s (14,582). Two taxis (20000080, 20000066) record 3,313 of the 14,582; without them each share moves by 4
     points at most. The slope is smooth, with no break, so no rule fixes the threshold.
   - Implemented: (a) 60 s. Cost: it drops the 45-s bin too, where most trips moved; about 6,000 of the 14,582
     dropped trips do not end within 100 m and may be real rides.
   - Alternatives: (b) 45 s, which drops only the 15-s and 30-s bins, where most trips end within 100 m, and keeps the
     45-s bin; (c) 30 s, which drops only the 15-s bin, closest to nyc's evidence level (63% of nyc's dropped trips
     start and end within 10 m, on a 1-s clock; a different clock, which the precedent check accepted as a
     difference).
   - The advocate argues for 60 s (at 45 s, 41% still end within 100 m, about 20 times the base rate); the critic
     argues for a lower cut (in the 45-s bin most trips moved). The mediator left it open. No score decides it (TP-2).
   - Recommendation (the AI's, not the panel's): (b) 45 s, reading bin by bin: each bin it drops has a majority of
     trips that did not move, and the first bin with a majority of moving trips stays. Its weak point is the 30-s
     bin, where only 53% end within 100 m, so about 2,000 real short rides may still leave test.
   - Decision: the threshold, (a) 60 s, (b) 45 s or (c) 30 s.

**Review panel:** ship after changes (mediator). Claim audit: 45 claims, 2 refuted (the destination is recorded after the trip,
disclosed, issue 1; the taxi_id score, now corrected), 2 record counts that do not reproduce, 4 untested (the zip
size, the challenge page's exact wording, the Kaggle test statistics, the priority weighing). Column and split
audits: trips that end at their start point and late labels without a gap, both fixed in this review. Blind review:
include with changes; main concern the destination as the last GPS point. Debate: agreed on the framing, the monthly
windows with a one-day gap and the USE-7 drop; disputed whether `fit_reason` may argue from the score (settled:
rewritten) and the short-trip cut (left open, issue 2); left to the curator: the reason for the framing (issue 1).
Issues 1 and 2 of the earlier file keep their numbers; its issues 3-6 and 8-10 are settled by the mediator's changes,
and issue 7 moved to the cross-dataset item on the datetime encoding.

<details><summary>Claim audit</summary>

**Claim audit: pkdd_15_taxi_trip_time_prediction_ii_1m (2026-10-20, re-check)**

Tests: s1 raw counts, s2 splits, s3 LightGBM per config, s4 polylines, s5/s6 sampling, s7 sha256, s8 DST with
placebo, s9 importance. Frame and splits rebuilt from the definition through
`dataset_io.from_definition` (1,436,885 rows, 3 splits, identical to the README). LightGBM in s3/s9: 800 trees, lr
0.08, 255 leaves, hour/day-of-week/day-of-year from `start_time`, 2 threads, the shipped splits (repeat 0/1/2 = June /
May / April). Licence and pretraining overlap are not evidence (EV-4).

**Per claim**

| # | claim (source) | test | result | evidence | rule |
|---|---|---|---|---|---|
| 1-2 | question; ETA at pickup (D task_summary) | framing; see implied I1 | holds as framing | target and features match the question | USE-1 |
| 3 | one trip, Jul 2013 - Jun 2014 (D) | UTC range of raw | holds | 2013-07-01 00:00:53 to 2014-06-30 23:59:56 UTC | PROV-13 |
| 4 | travel time from GPS points, 15 s, log (D) | UCI page; `_clean` | holds | UCI: "one pair of coordinates for each 15 seconds"; target log1p((n-1)*15) | USE-5 |
| 5 | known: start time, start, end point, call type, stand, taxi (D) | column list | holds (the end point is the disclosed assumption, I1) | 8 features exactly these | USE-3 |
| 6 | Apr/May/Jun test months; random 1M earlier trips (D) | s2, s6 | holds | test windows complete (131,659 / 156,990 / 148,236 = cleaned month counts); train 1M each, sampled share flat per month (0.661-0.665, 0.737-0.742, 0.819-0.822) | SPLIT-1 |
| 7 | changes vs challenge (D) | code read | holds | ORIGIN_CALL dropped, filters as listed | writing |
| 8-9 | fit approximate; pickup-only R² 0.11-0.15 (D) | s3 pickup_only | holds | R² 0.127 / 0.124 / 0.152 (Jun/May/Apr) | USE-8, EV-8 |
| 10 | year 2015, domain, source, licence, tags (D) | UCI page | holds; licence read but not evidence | UCI cites 2013, donated 2015; competition 2015. Record domain `Other` vs definition `industry & manufacturing` (disagreement stands) | PROV-8, EV-4 |
| 11 | 1,655,983 cleaned; train side > 1M per window; all test rows kept; one random order; frame only used rows (D version_comment) | s1, s5, s6 | holds | 1,655,983; smallest pool (April) 1,219,098 > 1M; May-train rows before April are 100% in April-train, June-train rows before May 100% in May-train (one order); frame 1,436,885 = union | SPLIT-27 |
| 12 | UCI id 339, 1,710,670 trips, sha256, zip 533,605,607 bytes (D download_description) | sha256sum, wc -l | holds except zip size untested | sha256 2891d03e...efff6d matches; 1,710,671 lines (header + 1,710,670). Zip deleted, Kaggle 403: byte size untested | PROV-1 |
| 13 | bibtex creators, DOI (D) | UCI page | holds | creators Moreira-Matias, Ferreira, Mendes-Moreira; DOI as cited | PROV-10 |
| 14 | constants: 15 s, Porto box, 60 s / 3 h, 120 km/h, local July, A/B/C (D) | s1, UCI page, s4 | holds | A/B/C verbatim on UCI; ORIGIN_CALL only on A (364,770/364,770), stand only on B (806,579 of 817,881); 725 of 741 speed-dropped trips have a step > 1 km (GPS jump) | CLEAN-11 |
| 15 | 1,710,670 trips 2013-07-01..2014-06-30 (D) | s1 | holds | as 3, 12 | |
| 16 | prediction point = meter on (D) | source read | holds as framing | TIMESTAMP "identifies the trip's start" (UCI) | USE-3 |
| 17 | challenge page: drivers "do not indicate the final destination of the ride" (D) | fetch geolink via Wayback (blocked), arXiv 1509.05257 | meaning holds; exact quote untested | Lam et al. Sec. 1: "busy taxi drivers do not report the final destination of the ride"; the geolink wording not re-fetched (web.archive.org unreachable) | EV-7 |
| 18 | target log1p, RMSE = RMSLE (D) | code | holds | | USE-5 |
| 19 | route not a feature (D) | columns | holds | only first/last points kept | LEAK-10 |
| 20, 33 | TIMESTAMP is UTC; DST shift (D) | s8 with placebo and wrong-direction shift | holds | same-hour corr 0.920 / 0.901, shifted 0.992 / 0.994, wrong direction 0.739 / 0.697; placebo fortnights without a switch: 0.995 unshifted, 0.896 shifted | PROV-14 |
| 21 | rows dropped, counts (D decision table) | s1 rerun of `_row_filters` | holds | 36,510 / 21 / 937 / 15,533 / 827 / 741 / 118, left 1,655,983 | CLEAN-15 |
| 22 | 70% / 31% / 7% of 15 / 60 / 120-s trips within 100 m (D) | s1 | holds | 69.7% / 30.5% / 6.9% (30 s 49.8%, 45 s 39.9%) | CLEAN-11 |
| 23 | TRIP_ID = start second + taxi; DAY_TYPE constant and "not correctly calculated"; MISSING_DATA erroneous per Lam (D) | s1, UCI, Lam | holds | TRIP_ID == TIMESTAMP + "6" + TAXI_ID on 100% of rows; DAY_TYPE all "A"; UCI "This field has not been correctly calculated"; Lam "the missing value column ... was erroneous"; MISSING_DATA True on 10 rows | CLEAN-6 |
| 24 | ORIGIN_CALL does not help with destination: R² -0.001 to +0.002 (D) | s3 all vs all_plus_call | holds (range a bit off) | delta -0.0026 / -0.0008 / -0.0012; pickup-only +0.004 / +0.009 / +0.005 | TP-2, EV-8 |
| 25 | call_type mapping; origin_stand empty unless stand (D) | s1 | holds | see 14 | CLEAN-2 |
| 26, 32 | fleet same every month; 99.93-100% of test trips by seen taxis (D) | s2 on shipped train sides | holds | 0.9993 / 1.0000 / 1.0000 of test rows' taxis in the 1M train side; 0-1 new taxi per month | SPLIT-24, USE-10 |
| 27 | 1.2% jump > 1 km; drive-backs; 65,708 (4.0%) within 500 m (D) | s4 polylines | holds | 19,673 (1.19%) with a step > 1 km; 65,708 (3.97%) within 500 m; 48% of those drive > 2 km along the polyline (drive-backs); within 100 m median 16.25 min vs 5.5 min at 0.5-1 km. On the shipped frame it is 56,962 (checklist) | USE-7 |
| 28-30 | TemporalSplits 1 month x 3; test 131,659-156,990; 1M random train (D) | s2 | holds | see 6, 11; no train/test index overlap | SPLIT-1 |
| 31 | challenge tested on 320 trips 1.5-6 months later (D) | de Brebisson quote via search; date arithmetic | holds | "320 partial trajectories ... five snapshots"; 2014-08-14 to 12-21 = 1.5-5.7 months after 2014-06-30 | PROV-9 |
| 34 | check: 0/0/0 (D) | read dataset_check.txt / checklist | holds (not rerun) | | |
| 35-36 | not a duplicate; 442 taxis; CC BY 4.0 (R) | UCI page | holds | UCI "all the 442 taxis"; file has 448 TAXI_IDs, 441 in the shipped frame | PROV-4 |
| 37 | Task II = remaining time from a prefix; 320 test trips (R) | search | holds | as 31 | |
| 38 | grouped structure by taxi (R) | s2 | holds as structure; resolved by the temporal split | | SPLIT-24 |
| 39 | investigation counts (R 2026-09-21) | s1 | mostly holds; two counts not reproduced | 80 ids / 81 surplus rows duplicated; 3 identical rows; 448 taxis; DAY_TYPE "A"; MISSING_DATA 10; 5,901 empty; 30,609 one point; median 600 s; p95 1,530 s; 10,094 > 1 h; 135 > 6 h; 125,861-162,107 per month; 57,105 call ids; 63 stands; 11,302 B without stand. NOT reproduced: "1,459 start outside Porto" (1,084 with the definition's box) and "1,672,071 rows after the filters" (1,672,375 with the same filters and box); the record's box is unknown | EV-8 |
| 40 | Kaggle test stats (corr 0.84, RMSLE 0.636 vs 0.794, 0.3%) (R) | needs test.csv | untested | Kaggle 403; no local test file | EV-7 |
| 41 | pickup-only R² 0.14, with drop-off 0.50; TAXI_ID top feature in both (R) | s3, s9 gain | holds | 0.12-0.15 / 0.52-0.54; taxi_id top gain share (0.207 with destination, 0.385 pickup-only) | EV-8 |
| 42 | verdict: temporal split, taxi as group (R CC) | v2 constraint | holds as a decision; the definition took temporal only (claim 32) | | SPLIT-24 |
| 43 | Assessment: 0.48-0.50 with destination (R, also REVIEW issue 1) | s3 | holds as a lower bound; setup-dependent | 0.535 / 0.516 / 0.533 here; 0.377 in the leak probe (50k sample, untuned); state the setup with the number | EV-8 |
| 44 | priority 2 grades (R) | judgment | untestable (a weighing) | | |
| 45 | front matter: Temporal, Regression, One Table (R) | definition | holds; `domain` disagrees (as 10) | | PROV-8 |

**Implied claims**

| # | claim | test | result | evidence | rule |
|---|---|---|---|---|---|
| I1 | every feature is known at the prediction point | source read, ablation | REFUTED for end_lat / end_lon as a fact of the source; disclosed (fit=approximate) | UCI: the last polyline point "corresponds to the trip's destination" (recorded by GPS at the end); Lam et al.: drivers "do not report the final destination". The end point carries R² 0.52-0.54 vs 0.12-0.15 without (it supplies ~0.39 of R²). Taxi, stand, call type and start are known at pickup | USE-8, LEAK-10 (Must) |
| I2 | the split is the one the use case needs | s2 overrun | holds, minor | train trips ending after the test start: 33 / 27 / 6 of 1M; longest overrun 34 min of a 1-month horizon; no gap declared | SPLIT-9 (Should) |
| I3 | the target is the real-world travel time | s4 | holds with disclosed noise | 1.19% of trips have a GPS step > 1 km in 15 s (>= 240 km/h), where (n-1)*15 undercounts; median path speed 24 km/h, p99.9 107 km/h | USE-5 |
| I4 | no row is a copy across the split | leak probe, hidden-groups probe | holds | 0.0% exact copies, 0.0% near copies | LEAK-16 |

**Side claims in the earlier REVIEW.md (tested because they argue a decision)**

| claim | test | result | evidence |
|---|---|---|---|
| issue 4: "taxi_id changes LightGBM R² by only -0.004 to +0.003" | s3 all vs all_no_taxi | REFUTED | +0.010 / +0.008 / +0.014 (Jun/May/Apr), taxi_id the top gain feature (0.207); the claim's setup is unstated (EV-8) |
| issue 2: two taxis record 3,352 sub-minute trips (35%, 23% of own); 21% of variance | s1 rerun after the first three filters | holds | 1,819 + 1,533 = 3,352; 34.9% / 22.7%; 20.9% of the SS |
| issue 3: within-100 m median 16.2 vs 5.5 min | s4 | holds | 16.25 / 5.5 |

**Refuted, ranked (principles.md: validity first, Must first)**

1. I1 (USE-8 / LEAK-10, Must): the destination is not known at pickup in the source; the end point is recorded after
   the trip and carries most of the signal (R² 0.53 vs 0.13). Already disclosed (`fit="approximate"`, REVIEW issue 1),
   so no new fact, but it stays the top open item. Mildest remedy: keep the disclosure and let the curator choose
   (destination ETA vs pickup-only, the source's own question); no code change from this audit.
2. REVIEW issue 4 number (EV-8, Should): taxi_id adds +0.008 to +0.014 R², not -0.004 to +0.003, and is the top gain
   feature. It does not change the decision (taxi stays a feature, temporal split), it strengthens it; remedy: replace
   the number and state the model setup.
3. Record investigation line (EV-8, Should): "1,459 outside Porto" and "1,672,071 after filters" do not reproduce with
   the definition's box (1,084 / 1,672,375); superseded by the decision table. Remedy: none needed beyond reading the
   decision table as authoritative; optionally a CC note.

**Untested**

1. Claim 17 exact quote from the challenge page (Wayback unreachable); the meaning is confirmed by Lam et al.
2. Claim 12 zip byte size (zip deleted; Kaggle 403).
3. Claim 40 Kaggle test-set statistics (no test.csv).
4. Claim 44 priority grades (a weighing, not a fact).

</details>

<details><summary>Column audit</summary>

**Column audit: pkdd_15_taxi_trip_time_prediction_ii_1m (2026-10-20)**

Frame: the container rebuilt from the definition through `dataset_io.load(..., built=True)` (origin `rebuilt`),
1,436,885 rows x 9 columns, sorted by `start_time` (CLEAN-23 holds). Prediction point (first `curation_comments` bullet): the start of the trip, meter switched on,
with the destination assumed known (curator framing, CC 2026-09-21; `fit="approximate"`).

Codebook: UCI 339 / challenge data page (TRIP_ID, CALL_TYPE A/B/C, ORIGIN_CALL, ORIGIN_STAND, TAXI_ID, TIMESTAMP Unix
s, DAY_TYPE, MISSING_DATA, POLYLINE one [lon, lat] every 15 s, "the last list item corresponds to the trip's
destination").

**Column table**

| column | meaning | known at prediction? | dtype and cleaning | verdict | rule |
|---|---|---|---|---|---|
| `call_type` | how the taxi was hired: A dispatch central, B taxi stand, C street (data page) | yes, at hire | category, 3 levels, mapped to the page's labels, 0 missing | fine | CLEAN-12, CLEAN-14 |
| `origin_stand` | id of the stand where a B trip started (63 stands) | yes | category, 63 levels; empty string set missing (748,832 missing: every A and C trip, plus 9,829 B trips without a stand id; B without stand mean log target 6.49 vs 6.36). Missing means "no stand / not recorded", not a proxy left behind | fine; optional: the challenge's stand metadata file gives names and GPS, not needed since the start point carries the location | CLEAN-10, CLEAN-3 |
| `taxi_id` | anonymised taxi (driver) id, 441 levels (`20000xxx`) | yes | category (string codes, not parsed as numbers), 0 missing | fine (known entity, USE-10, LEAK-34). Leak probe: dropping it raises R² 0.377 to 0.391 on 50k rows; a feature that does not help is no reason to drop it (CLEAN-22). Note: taxi 20000969 (19 trips, 2 in test) ends every trip within 100 m of its start; taxi 20000205 (1,069 trips, 201 in test) 33% | fine, note | USE-10, LEAK-34, CLEAN-22 |
| `start_time` | trip start, TIMESTAMP (UTC) converted to Europe/Lisbon wall clock, naive | yes | datetime64, whole seconds, 2013-07-01 01:00:53 to 2014-06-30 23:59:58. Local naive time cannot hit the spring-forward gap; the fall-back hour (2013-10-27 01:00-02:00) interleaves two UTC hours, train only, harmless. Hour of day depends on the harness encoding (cross-dataset item with nyc) | fine; encoding is the open cross-dataset question | PROV-13, CLEAN-14, CLEAN-2 |
| `start_lon`, `start_lat` | first GPS point of the polyline: the pickup | yes (meter on) | float64, ~6 decimals; filtered to Greater Porto (lat 41.0-41.3, lon -8.8 to -8.4); top point 41.1486, -8.5856 (Campanhã station stand, ~470 trips per exact point) | fine | CLEAN-11 |
| `end_lon`, `end_lat` | last GPS point of the polyline: where the meter went off | **no** in the source: recorded at the end of the trip; the challenge says drivers do not enter the destination. Yes only under the curator's framing (passenger names it at pickup) | float64; no filter on the end point except the 120 km/h straight-line cut; 4,198 end lat and 1,670 end lon outside the Porto box, extremes 38.57 (Lisbon area) and 42.14 (Vigo), 804 trips > 50 km, max implied straight-line speed 119.9 km/h: plausible long trips, kept | question for the curator (open REVIEW issue 1); strength: R² 0.377 all, 0.269 without end_lat, 0.231 without end_lon, 0.11-0.15 without both (definition's own LightGBM) | USE-3, USE-8, LEAK-10 |
| `log1p_travel_time` (target) | log1p((GPS points - 1) x 15 s), the challenge's definition; RMSE on it is RMSLE | outcome | float64; every value a multiple of 15 s, 60 to 10,800 s; rows under 60 s, over 3 h and over 120 km/h dropped, in test too (REVIEW issue 2) | fine; the 120 km/h cut combines the target and the end point, so a deployment could not apply it (741 trips; noted in issue 2) | CLEAN-15, CLEAN-16, LEAK-26 |

Source columns dropped before the frame:

| column | meaning | known at prediction? | verdict | rule |
|---|---|---|---|---|
| `TRIP_ID` | start second + taxi | encodes start time and taxi (both kept) | drop is right | CLEAN-3, CLEAN-5 |
| `ORIGIN_CALL` | anonymised phone id of a dispatch customer (57k) | yes | drop defensible: measured uninformative with the destination (R² -0.001 to +0.002), and a personal pseudonym. The stated reason should read "uninformative identifier", not its count (CLEAN-22). Open issue 5 | CLEAN-3, CLEAN-22, USE-10 |
| `DAY_TYPE` | day type, constant "A", "not correctly calculated" (data page) | yes | drop is right | CLEAN-5, PROV-13 |
| `MISSING_DATA` | GPS stream incomplete flag | no: describes the trajectory, known after the trip; also unreliable (10 True) | drop is right | LEAK-10 |
| `POLYLINE` | the GPS trajectory | no, after the trip | reduced to start point, end point and the target; nothing else derived | LEAK-10 |

**Problems, ranked by principles.md**

1. **P3/P4, USE-3 and LEAK-10 (Must) vs USE-8: `end_lat` / `end_lon` are recorded after the trip.** Evidence: the
   last GPS point (data page); the challenge overview and Lam et al. 2015 say drivers do not report the destination;
   the end point carries most of the signal (R² 0.377 to 0.11-0.15 without it). Under the curator's framing it stands
   in for a destination named at pickup and the fit is `approximate`, as already written. Not a new finding; it stays
   the curator's question (REVIEW issue 1). Mildest remedy: keep as framed (done); the alternative is to drop both.
2. **P3, USE-7 (Must), by the nyc precedent: 76 trips whose end point equals the start point** (5 / 9 / 11 in the
   June / May / April test windows; mean log target 5.46, median 135 s, sd 1.37). nyc_taxi_trip_duration drops its
   identical-coordinate trips under USE-7 (no destination a passenger would name); pkdd keeps them, and its REVIEW issue
   3 still says nyc kept its one-point trips (out of date). Remedy: drop the 76 rows in `_row_filters` (a filter on
   features, applicable in deployment). The wider band is a curator call: 20,516 trips end within 100 m but not at the
   same point (median 960 s vs 330 s at 0.5-1 km, sd 1.15 vs 0.64): there the end point records a return or a meter
   left on, information a passenger's stated destination would not give. nyc kept its within-10 m trips as unusual
   values (CLEAN-11); following it, keep them with the note, or drop the 100 m band as REVIEW issue 3 offers.
3. **P4, target filters applied to test (LEAK-22 family, Should-level note):** the 60 s / 3 h cuts and the 120 km/h cut
   select test rows on the label (the last also on the end point). Small (15,533 + 827 + 741 before the subsample) and
   documented as REVIEW issue 2; no new remedy beyond stating that a deployment cannot apply them.
4. **P7, CLEAN-22 wording on ORIGIN_CALL:** the code comment's "57k phone ids" reads as a width argument. The drop holds
   as an uninformative, personal identifier (CLEAN-3); reword only.
5. **P7, notes:** taxi 20000969 (every trip within 100 m) and taxi 20000205 (33%) look like a stuck GPS or a meter used
   while parked; covered by item 2's band, no separate action. `origin_stand` could be joined to the stand names from
   the challenge's metadata file (CLEAN-12, optional, low value).

No other column is post-outcome, and none encodes the label or has a proxy value left. Every dtype matches its
meaning (CLEAN-9, CLEAN-14). No statistic over all rows enters any feature (LEAK-29).

</details>

<details><summary>Split audit</summary>

**Split audit: pkdd_15_taxi_trip_time_prediction_ii_1m (2026-10-20, re-check)**

Inputs: `datasets/_dev/tabarena-v0pt2/pkdd_15_taxi_trip_time_prediction_ii_1m/dataset.py` (frame and splits rebuilt
from the definition through `dataset_io.from_definition`; README has `build: null`), the panel's probes. LightGBM 300 trees, lr 0.1, 63 leaves, 2 threads; features = the shipped columns plus
local hour, weekday and time as a number (what a datetime encoder gives).

**Verdict: right, with notes**

Validity: USE-10 holds (known fleet, warm start); SPLIT-1/2/3 hold (temporal); SPLIT-6 holds; SPLIT-9 triggered in
letter (6-33 of 1M train trips per window end after the window start), no measurable effect; SPLIT-11, SPLIT-14 hold;
SPLIT-12 open choice (monthly vs weekly); SPLIT-13 checked (taxi recurs, part of the task); SPLIT-29/30 no hits.

**The regime against the use case**

- Use case: at pickup, the company estimates the duration to plan when the taxi is free (task_summary). The fleet is
  the company's own: the taxis recur. Test trips by a taxi seen in train: 100.000% / 99.997% / 99.932% (June / May /
  April), 0 / 1 / 1 new taxi. Stands: 100% of stand trips at a stand seen in train. Known-entity regime, a stream
  over time: temporal is right (USE-10, SPLIT-3, SPLIT-13). A taxi-grouped split would test a new driver, which the
  use case rarely meets.
- Cold-start cost, measured (models2/control; 20% of taxis held out of train, taxi_id dropped from the features,
  scored on the held-out taxis' test trips, against a random-row removal of the same size): R^2 0.452 vs 0.466
  (June), 0.435 vs 0.454 (May), 0.419 vs 0.448 (April): 0.014-0.029 R^2. Taxi identity carries some signal, so the
  warm-start choice is not neutral, but the use case decides it (SPLIT-4), not the gap. Side note for the column
  auditor: with taxi_id as a LightGBM categorical, the score on those taxis' trips was 0.508 / 0.469 / 0.501 (no
  bagging) vs 0.467 / 0.457 / 0.448 without taxi_id (bagged): taxi_id may matter more than REVIEW issue 4's
  "-0.004 to +0.003" on that subset; different model settings, indicative only.

**Temporal checks**

- Time column: `start_time`, the local (Europe/Lisbon) start of the trip, the prediction point. Correct axis.
- Windows (calendar months, newest first): June 148,236, May 156,990, April 131,659 test trips; no index overlap.
  Train side a random 1M of all earlier trips (expanding, SPLIT-11); 11 / 10 / 9 months of history, 81k-123k per month,
  every month represented. Train side >= 50% of the frame (SPLIT-14).
- Training history (SPLIT-20): the data covers one year, so no earlier April-June exists for any window; no break in
  the history (monthly target mean 6.35-6.44, sd 0.59-0.61). Test months are busier (132k-157k trips vs 100k-123k),
  a spring rise the train side only partly sees (July-September 2013). Not fixable inside this release.
- Season-shaped windows: Easter (18-20 April, daily mean 6.27-6.35) and Sao Joao (24 June, 6,431 trips, mean 6.35)
  fall inside the windows; each is 1-2 days of a month, daily means within the range. No atypical window.
- Gap and late labels (SPLIT-9, SPLIT-10): no gap. Train trips whose end (start + travel time) is after the window
  start: 33 / 27 / 6 of 1M; their mean target 6.64 / 6.88 / 6.63 against 6.41 (the long trips, as SPLIT-10 predicts).
  Effect, 3 seeds, bagged LightGBM: a 1-day gap changes R^2 by -0.002 to +0.005 per window (June 0.491-0.493 vs
  0.492-0.495; May 0.465-0.469 vs 0.468-0.471; April 0.494-0.496 vs 0.494-0.495), within seed noise.
- Horizon (SPLIT-12): R^2 by week of the test month, June 0.527 / 0.495 / 0.497 / 0.475, May 0.462 / 0.468 / 0.453 /
  0.476, April 0.520 / 0.518 / 0.476 / 0.486: a mild decay over the month in 2 of 3 windows. Monthly windows are
  defensible from the challenge's 1.5-6 month test gap; weekly (nyc) is the sibling convention (REVIEW issue 6).
- IID reference: random 150k test / 1M train, R^2 0.506-0.517 vs 0.47-0.50 temporal: a random split would be
  optimistic by about 0.02-0.03.
- Hidden groups / near copies: hidden-group probe, no hits (origin_stand 47% "seen" is the 52% missing; among stand
  trips 100%); near-copy clusters 0.0%; leak probe 0.0% exact copies. Nothing for SPLIT-29/30.

**Problems, ranked (principles.md)**

1. P4, SPLIT-9 (Must, graded by severity) / SPLIT-10 (Should): no gap; 6-33 train trips per window carry a label not
   known at the window start, biased long. Effect within noise (above). Departs from the sibling
   nyc_taxi_trip_duration, which took a 1-day gap for 77-127 such trips (treat like cases alike). Mildest remedy:
   a gap of 1 day. The API counts `gap` in the window's unit, so `months` cannot take a 1-day gap (gap=1 would drop a
   whole month). Options: (a) `TemporalSplits(window=30, unit="days", cutoffs=("2014-04-01", "2014-05-01",
   "2014-06-01"), gap=1)` (31 May falls out of the May window, about 5k trips), (b) a gap unit in the API, (c) keep
   with a documented note quoting the 6-33 rows and the null effect. (a) or (c); the curator's call.
2. P4, SPLIT-12 (Should): monthly vs weekly windows, open (REVIEW issue 6). Measured: mild decay within the month in
   2 of 3 windows; no rule violated. Keep with the reasoning written, or switch to 3 x 7 days with gap=1 (31.7k-34.8k
   trips a week), which also solves problem 1 in the API as it is.
3. P4, SPLIT-20 (Should), note only: one year of data, so the test season (April-June) has no earlier copy in train;
   say it in `splits_comment`.
4. Procedure: `splits_comment` should state the gap decision either way (the README now shows `time_gap: null`).

Not problems: the regime (temporal, warm start, taxi a feature); windows sizes and history; hidden groups.

</details>

<details><summary>Domain practitioner</summary>

**Domain practitioner: pkdd_15_taxi_trip_time_prediction_ii_1m (2026-10-20)**

Actor played: the operations lead of a Porto taxi fleet / dispatch central (in 2013-14 a radio-taxi cooperative on
Geolink's dispatch system; today also an app-booking operator). Moment: the meter goes on at pickup. Decision: when
will this taxi be free again (dispatch planning), or, for an app booking, what duration to quote upfront.

**Fit: approximate (USE-8)**

The rows, target, timing and monthly temporal split mirror an ETA-at-pickup decision, but the one input that carries
the signal, the destination, is read from the trip's last GPS point and the source says the dispatch system never
receives it, so the task is a stand-in for a fleet that captures the destination at pickup.

USE-9 check: is there another use case where the shipped data is direct? Yes, partly: upfront duration/fare quoting
in ride-hailing apps, where the rider enters origin and destination before the ride (Uber's upfront-pricing page lists
"estimated trip time, distance from origin to destination, time of day, route"). But that actor's rows are booked
trips, not street hails and stand hires, and it would always have a routing-engine estimate. Moving to it to call the
fit direct would be "a use case rephrased only to excuse a gap" (Weighed factors). Approximate stays, as labelled.

**1. Inputs at the prediction point (USE-3, USE-6)**

| Input | Do I have it at pickup? |
|---|---|
| start_time (local), start point | yes, from the meter and the GPS |
| call_type, origin_stand | yes, the dispatch system records them |
| taxi_id | yes (known entity, USE-10; 99.9-100% of test trips by taxis seen before) |
| end_lat / end_lon | **not in the system.** The passenger tells the driver, but drivers do not key it in (challenge overview; Lam et al. 2015 Sec. 1: "busy taxi drivers do not report the final destination"). It is the last GPS point, so it is also the *actual* drop-off, not the *stated* destination: detours, round trips and the 4% of trips that end within 500 m of the start are things a stated destination would not show. |

What I would always have and the dataset lacks:
- a routing estimate (road distance and free-flow time from OSRM/Google/HERE) between start and destination. Every
  ETA system starts from it; the model would learn the residual. Here the model must learn Porto's road network
  from two lat/lon pairs (the probe's linear model reaches R² 0.04, LightGBM 0.37: the geometry is the task). That is
  a fair tabular benchmark but not how I would deploy.
- live state: current traffic, weather, events, the fleet's recent trip times this hour. Absent; the source has none.
- ORIGIN_CALL (dropped): for a dispatch-central booking I do know the caller; dropping it is defensible on the
  measured gain (R² ±0.002), not on availability.

**2. Target (USE-5)**

What I act on is the minute the taxi is free again, i.e. the trip duration in seconds; (points - 1) x 15 s is that
duration at 15-s resolution, with GPS-gap noise in ~1.2% of trips. A point estimate is what dispatch uses; for a
quote I would also want an upper quantile (late arrival costs more than early). Log target + RMSLE scores relative
error, which matches how a dispatcher reads "10 vs 12 min" and "40 vs 48 min" as similar misses. Fine.

The 60-s and 3-h cuts remove non-trips and meters left running, which my system would also flag. The < 60-s cut is
on the target, though, and is applied to test as well; in deployment I cannot know at pickup that a hire will be a
30-s cancel. Small (0.9%), but it is a target filter on test (CLEAN / LEAK-22 territory, already issue 2).

**3. Rows and test data (USE-1, USE-10)**

One row = one hire = one decision. Test = next calendar month's trips by the same fleet, model refit monthly: what I
would face. Monthly refit is realistic for a fleet ETA model; weekly windows (issue 6) would also be realistic. The
known-entity framing (taxi as feature, temporal split) is right under USE-10: I never predict for an unseen taxi.

**4. Would I use it?**

As a 2014 Porto dispatcher, no: I would not have the destination for most hires, and pickup-only accuracy (R² 0.11 to
0.15) does not beat "median trip ~10 min" by enough to change a dispatch. As an operator that captures the
destination (app booking, or a tablet where the driver taps it), yes in shape, but I would trust it only after
adding a routing estimate and checking it on stated (not realised) destinations. Distrust: trips that end at their
start; a model trained on realised drop-offs looks better than one fed typed-in destinations.

**Gaps ranked by how much they change the task**

1. **Destination availability (largest).** Not entered in the source system; R² 0.11-0.15 without, ~0.50 with. Also
   realised drop-off vs stated destination (round trips, detours, end-near-start 4%). Changes the task from a
   weak-signal planning estimate to an ETA. Named in fit_reason; open as issue 1.
2. **No routing/road-distance input.** A real ETA starts from it; here the model learns the network from coordinates.
   Changes what the benchmark measures (spatial learning vs residual correction) but not whether it is a real task.
3. **No live traffic / weather / events.** Every ETA system has some; the source has none. Moderate; the time of day
   carries part of it.
4. **Target-based filter on test (< 60 s, > 3 h).** Small (1%), but unknowable at pickup.
5. **Population mix.** Street and stand hires (about half the rows have a stand) are the hires where a destination
   is least likely to be captured; app-booking actors see mostly booked trips.

**What a domain expert would change**

- Keep the approximate label and the destination framing only with the gap stated (it is); the alternative the
  source supports is pickup-only, which is the source's own decision but nearly no signal (task_probes TP rule 2
  says weak but real is no reason to drop; the curator decides, issue 1).
- If shipping the destination framing, consider dropping trips ending within ~100 m of their start (no passenger
  states that destination; filter is on a feature, so applicable at deployment, USE-7 spirit).
- Possibly restrict the destination framing to dispatch-central hires (call_type A), where an operator could ask
  for the destination, to tighten the stand-in. That loses ~a fifth to a quarter of the rows; I would only suggest
  it, not require it.
- No change to the split, the taxi-as-feature choice or the log target.

**Sources**

- Lam et al. 2015, "(Blue) Taxi Destination and Trip Time Prediction from Partial Trajectories", arXiv:1509.05257
  (dispatch motivation; Sec. 1 on drivers not reporting destinations)
- de Brébisson et al. 2015, arXiv:1508.00021 (challenge setup, 320 partial test trajectories)
- UCI 339 dataset page, https://archive.ics.uci.edu/dataset/339/ ("The last list item corresponds to the trip's destination")
- Uber upfront pricing (Portugal), https://www.uber.com/pt/en/ride/how-uber-works/upfront-pricing/ (inputs to a pickup-time estimate)
- The panel's claim list, checklist and task probes (LightGBM R² 0.37, linear 0.04, single feature end_lat)
- The geolink.pt challenge overview quote was not re-fetched (Wayback blocked for the agent); relied on REVIEW.md issue 1 and Lam et al.

Rules cited: USE-1, USE-3, USE-5, USE-6, USE-7, USE-8, USE-9, USE-10, Weighed factors.

</details>

<details><summary>Blind review</summary>

**Blind review: pkdd_15_taxi_trip_time_prediction_ii**

**Verdict: include with changes** - a real origin-destination ETA task for Porto taxis (Jul 2013-Jun 2014) with clear signal and a sensible temporal split, but the framing differs from the source competition and the target/filtering need documenting.

**Task**
Predict trip duration (log1p seconds) from call type, stand, taxi id, start time, start and end coordinates. User: a dispatcher or ride-hailing app quoting an ETA at pickup once the passenger names the destination. Real use (same shape as NYC taxi trip duration).

**Concerns (most to least serious)**
1. **End coordinates are the realised last GPS point, not a stated destination.** In the source, the trip is a POLYLINE of 15-s GPS points; end_lon/end_lat are its last point, known only when the trip ends. Fine as a proxy for "destination given", but it is cleaner than any real stated address (exact drop-off, includes detours ending far away: 114/200k rows >50 km straight-line, end_lat down to 38.77 = Lisbon). Signal depends heavily on it: LightGBM on a temporal holdout (train < 2014-04, test after) gives R2 0.46 with end point + distance, 0.07 without. Change: document the framing ("ETA given known destination"); it is not the Kaggle Task II setup (which gives a partial trajectory and asks the remaining time).
2. **Target is derived, quantised and filtered.** All times are multiples of 15 s ((n_points-1)*15), min 60 s, max 10,740 s; 1,436,885 of ~1.71M source trips remain, and no row has straight-line speed >120 km/h, so rows were filtered. The rules (MISSING_DATA flag, short trips, speed caps) are not stated in task.md. Change: state them; consider also dropping physically implausible far-away endpoints (GPS glitches).
3. **taxi_id as a 439-level category** with temporal split: fine (fleet is stable), but a per-driver effect can be memorised; acceptable.
4. **origin_stand missing 52%** - structurally (only for taxi_stand calls; 1,314 taxi_stand rows lack it). Fine as NaN; day_type column from the source dropped (it is constant "A" in the source, OK).
5. No duplicates found (0 exact duplicates excluding taxi_id; 12 trips with start = end).

**Could not check**
Full 1.44M rows (only 200k sample), the exact filtering code, whether the 3 test windows are of equal length, and the source pages themselves (relied on knowledge of the public ECML/PKDD 2015 data description).

</details>

<details><summary>Precedent check</summary>

**pkdd_15_taxi_trip_time_prediction_ii: consistency against the precedents (precedent-checker, 2026-10-20)**

Scope: `datasets/_dev/tabarena-v0pt2/pkdd_15_taxi_trip_time_prediction_ii_1m/dataset.py`, the record
`curation/records/pkdd_15_taxi_trip_time_prediction_ii.md` (two CC lines of Lennart, 2026-09-21; AI assessments of
2026-10-07 and 2026-10-20), issues 1-10 of the REVIEW.md before this run and the checklist's draft issues.

Register (the decision register, run of 2026-10-20): none of its 4 flags touches pkdd. Flag 3 (drift on "scaling over
all rows") names the TabReD ETA siblings (delivery_eta, maps_router_eta, cooking_time, kept 2026-10-19); pkdd has no
all-row transform, so it does not apply. pkdd's entries: the two CCs of 2026-09-21, the two AI assessments, the 10 open
issues, and two Cases rows of LEAK/EV on the competition's prefix snippet (no bearing on this definition). No curator
decision on pkdd after 2026-09-21, so no drift by the curator on this dataset and no third exception.

Status of the precedents: only CC lines and dated Cases rows are curator decisions. nyc_taxi_trip_duration's review of
today is an AI panel (mediator's changes applied, not yet decided by the curator, its issue 5 open); the TabReD ETA
sets (delivery_eta_1m, maps_router_eta_1m, cooking_time_1m) ship.

**Summary**

| # | Decision | Rules | Result |
|---|---|---|---|
| 1 | Destination (last GPS point) as a feature, `fit = approximate` (issue 1) | USE-8, USE-9, TP-2, TP-6 | consistent with nyc; the CC's stated reason is superseded by TP-2 |
| 2 | No gap: 33 / 27 / 6 train trips per window end after the window start (checklist, new) | SPLIT-9, SPLIT-10 | **departs from nyc, no reason given; SPLIT-9 is a Must** |
| 3 | 76 trips with identical start and end coordinates kept (issue 3) | USE-7, CLEAN-11 | **departs from nyc, no reason given (the stated reason is out of date); USE-7 is a Must** |
| 3b | Trips ending within 100 m / 500 m but not identical kept (issue 3) | CLEAN-11 | consistent with nyc (keeps near-but-not-identical) |
| 4 | Under 60 s and over 3 h dropped (issue 2a) | CLEAN-11, CLEAN-15, USE-7 | consistent in kind; threshold reason stated; one note |
| 5 | Straight line > 120 km/h dropped (issue 2b); GPS-jump trips otherwise kept (issue 8) | CLEAN-11, CLEAN-1 | consistent (nyc keeps its 46 fast trips for a stated reason) |
| 6 | Temporal only, taxi_id a feature (issue 4) | SPLIT-3, USE-10 | consistent (the CC's "taxi as group" predates SPLIT-3) |
| 7 | ORIGIN_CALL dropped, taxi_id kept, both with a near-zero measured gain (issue 5) | CLEAN-3, CLEAN-22, CLEAN-24 | pair decided differently inside the definition; reason partly stated |
| 8 | Monthly windows (issue 6) | SPLIT-12, SPLIT-19, SPLIT-21 | consistent, reason stated (departs from the weekly ETA family on a stated fact) |
| 9 | Hour of day left to the harness (issue 7) | CLEAN-2 | consistent with nyc; cross-dataset item already open |
| 10 | UTC converted to Lisbon wall-clock time (issue 9) | PROV-13 | consistent with nyc's DST repair |
| 11 | `year = "2015"` (issue 10) | PROV-9, PROV-10 | consistent; the alternative (2013) would break PROV-9 |
| 12 | `_1m` with `subsample_to_budget` | definitions.md row budget | consistent (delivery_eta_1m path; frame 1.66M > 1.5M) |
| 13 | Record `domain` Other vs definition `industry & manufacturing` | | consistent definition; record stale, as nyc's |

**Per decision**

**1. The destination as a feature, fit approximate (issue 1): consistent with nyc; the CC's reason needs replacing**

* nyc_taxi_trip_duration (AI mediator, 2026-10-20) keeps the drop-off point as the destination and rates the fit
  `approximate` on pkdd's own fact ("the driver does not enter the destination in the system", which the mediator
  found holds for 2016 yellow cabs too). pkdd is the same framing with the same label. The two are alike now.
* The curator's CC (2026-09-21) chose the destination framing because pickup-only "does not" carry signal (R^2 0.14).
  TP-2 (Should, 2026-10-06, forest_fires: R^2 0.013 kept) came later and says a small real signal is no reason to drop
  a framing; pickup-only has R^2 0.11-0.15 on 3 of 3 windows. The decision may stand, but not on that reason: a
  precedent whose reason contradicts a later rule is flagged, not followed.
* TP-6 (Must) does not settle it on its own: the source defines Task II (remaining time given a partial trajectory)
  and Task I (destination given a partial trajectory). Pickup-only is not one of them; it is the shortest prefix of
  Task II. Calling it "the source's own question" (the earlier REVIEW.md) is an argument, not a defined stage like
  eryhemato's (2026-10-06).
* Whichever way the curator decides, nyc must follow, or a fact must set them apart: the source's explicit statement
  that drivers do not enter the destination is pkdd's; nyc's source (TLC) is silent, but the nyc mediator found the
  same gap. A switch to pickup-only also reopens decision 7 (ORIGIN_CALL adds +0.002 to +0.005 pickup-only).

```text
**Consistency check (AI, 2026-10-20):** the destination framing of pkdd_15_taxi_trip_time_prediction_ii rests on
your CC of 2026-09-21 ("the pickup-only one does not" carry signal), a reason TP-2 (2026-10-06, forest_fires) no
longer accepts. What decides the framing? (a) the destination-known ETA is the task an actor runs (the dispatcher or
an app once the passenger names the destination), rated approximate as nyc_taxi_trip_duration is: record that as the
reason; (b) switch to the pickup-only task, and then reopen nyc_taxi_trip_duration the same way; (c) ship pickup-only
for pkdd only, naming what sets pkdd apart (its source states the destination is not entered); (d) amend USE-8 / TP-6
to say whether an endpoint recorded after the trip may stand in for a destination named at the start.
```

**2. No gap (SPLIT-9): departs from nyc without a reason; not reasonable under the ranking**

* nyc_taxi_trip_duration (AI mediator, 2026-10-20) found 77 / 119 / 127 train trips per weekly window ending after
  the window start and fixed it with `gap=1` (day), measured 0 / 0 / 0 after. Same mechanism here: a trip lasts up to
  3 h, so at a monthly refit the last trips before it have no travel time yet; pkdd has 33 / 27 / 6 such trips of 1M
  (checklist, P4) and `time_gap: null`.
* SPLIT-9 is a Must: a Must has no exceptions, and the size of the effect is not a fact that sets a case apart (the
  tension row "the right split against the score", forest_fires; the house_prices_nominal item of today applies the
  same). Cases of the rule: hotel_booking_demand (SPLIT-9), brazilian_ecommerce (SPLIT-10, Lennart 2026-10-15),
  sf_permit_time (SPLIT-10).
* Counter-precedent to note: delivery_eta_1m, maps_router_eta_1m and cooking_time_1m (shipped, weekly windows) take no
  gap, though SPLIT-10 names "a delivery time" as its first example. No measurement of their late labels is recorded,
  so they are an unchecked precedent, not a decision on this mechanism. Worth a cross-dataset item: check SPLIT-9 on
  the three TabReD ETA sets the way nyc did.
* Mechanics, not a reason: `TemporalSplits(gap=...)` counts in the window's unit, so `unit="months"` allows only a
  whole month of gap. The mildest remedy is a gap of a few hours or a day built in `_make_splits` (or the `Temporal`
  `gap`/`gap_unit` route the API documents), not a one-month gap and not a filter on the trip's end time (that filter
  uses the target and keeps only the fast late trips, which SPLIT-10's "Why" warns against).

```text
**Consistency check (AI, 2026-10-20):** pkdd_15_taxi_trip_time_prediction_ii_1m takes no gap although 33 / 27 / 6
train trips per window end after the window start, while nyc_taxi_trip_duration took a one-day gap for 77 / 119 / 127
such trips (SPLIT-9, Must; review panel 2026-10-20). What sets pkdd apart? (a) the monthly windows make 6-33 of 1M
late labels negligible (an effect size, which the tensions table does not accept as the fact, and SPLIT-9 is a Must, so
this would need an amendment); (b) treat pkdd like nyc: a gap of about the 3-h maximum trip, e.g. one day; (c) reopen
nyc's gap; (d) amend SPLIT-9 with a share of late labels below which no gap is needed (then delivery_eta_1m,
maps_router_eta_1m and cooking_time_1m are checked against it).
```

**3. Trips with identical start and end coordinates kept (USE-7): departs from nyc without a reason**

* nyc_taxi_trip_duration (AI mediator, 2026-10-20) drops its 4,539 trips whose drop-off equals the pickup under USE-7
  (Must: "a named destination is never the pickup point", so the row lacks the input the ETA acts on), following
  bias_correction_r_bias_correction_r_2 (Lennart, 2026-10-15), and keeps trips within 10 m but not identical as unusual
  values (CLEAN-11).
* pkdd keeps 76 trips with identical coordinates (5 / 9 / 11 in the June / May / April test windows; mean target 5.46
  against 6.41). the earlier REVIEW.md issue 3 gives as its reason "NYC kept its 0.4% of one-point trips", which is out of date:
  nyc now drops them. The working copy's REVIEW.md ("Decide pkdd_15's trips that end where they start like nyc's")
  asks for this alignment.
* A candidate distinguishing fact exists in pkdd's data and not in nyc's: pkdd has the polyline, so a trip of 60 s or
  more with identical endpoints may show the taxi moving (a round trip with the meter on), whereas nyc's records are
  two points. Even so, a round trip's named destination is not the pickup point, so USE-7's reason still applies;
  the fact would need a measurement (path length of the 76 trips) to carry an exception, and USE-7 is a Must.
* 3b. The 20,592 trips within 100 m (and 56,962 within 500 m) that are not identical: nyc keeps its near-but-not-identical
  trips as unusual values, so keeping them follows nyc. Dropping them would be a new filter on a feature without a
  precedent.

```text
**Consistency check (AI, 2026-10-20):** pkdd_15_taxi_trip_time_prediction_ii_1m keeps 76 trips whose end point equals
the start point, while nyc_taxi_trip_duration drops its 4,539 such trips under USE-7 (Must; review panel 2026-10-20,
after bias_correction, Lennart 2026-10-15). What sets pkdd apart? (a) its polylines show these taxis moving (round
trips), measured on the 76 trips, recorded as the reason; (b) treat pkdd like nyc: drop the 76; (c) reopen nyc and keep
its identical-endpoint trips; (d) amend USE-7 for a recorded endpoint that equals the start.
```

**4. Under 60 s and over 3 h dropped (issue 2a): consistent in kind, threshold reason stated, one note**

* Over 3 h follows the curator's CC (2026-09-21: "meter-left-on outliers") and nyc's 3-h cut (same threshold).
* Under 60 s: delivery_eta_1m and cooking_time_1m drop under one minute (TabReD), nyc under 30 s; pkdd states why its
  threshold differs (15-s GPS resolution against nyc's 1-s clock). Rule chain as in nyc's precedent check: an
  impossible duration is a missing target (CLEAN-11 to CLEAN-15), and a non-ride is no task row (USE-7).
* Note (not a departure): nyc's cut rests on evidence outside the target (63% of its sub-30-s records start and end
  within 10 m). pkdd's own evidence is weaker at its threshold: 31% of 60-s trips end within 100 m, so most trips cut
  near 45-60 s moved. The dropped 15,533 trips hold 21% of the log-target variance. zillow_prize (AI, today) keeps
  target extremes because it has no evidence outside the target; pkdd has some, but it thins out at the cut. The
  curator may want the cut where the outside evidence holds (about 30 s: 50% within 100 m), which would also match nyc.

**5. 120 km/h dropped; GPS-jump trips otherwise kept (issues 2b, 8): consistent**

nyc keeps its 46 trips over 100 km/h; its mediator set the two apart explicitly: nyc "has no trajectory that would show
the label is broken", pkdd does (725 of 741 fast trips have a jump of over 1 km). The 19,673 other trips with a jump
stay, on CLEAN-1 (the challenge's own label definition) and CLEAN-11 (unusual, not impossible). Coherent: the 120 km/h
cut drops trips whose endpoint itself is implausible, the kept jumps only shorten the label.

**6. Temporal only, taxi_id a feature (issue 4): consistent**

The CC (2026-09-21) asked for "temporal split, taxi as group". SPLIT-3 (Must, Lennart 2026-10-12) came later: one
regime, the one the use case implies. A newer decision of the curator beats an older one; the definition follows it.
nyc likewise ships temporal only. Not a departure from the curator.

**7. ORIGIN_CALL dropped, taxi_id kept (issue 5): pair decided differently inside the definition; reason partly stated**

* Both are identifiers that carry meaning (CLEAN-3: keep "a group id"): the customer and the taxi. Both have a
  near-zero measured gain with the destination: ORIGIN_CALL -0.001 to +0.002 R^2, taxi_id -0.004 to +0.003. One is
  dropped for that gain, the other kept.
* CLEAN-22 (Must): columns leave for what they are (a leak, an identifier, a copy), not for how many there are. A
  drop for a measured null gain is closest to the CLEAN-24 case (apistox, drug_induced_autoimmunity_prediction,
  qsar_bioconcentration, 2026-10-14: the SMILES string dropped next to the descriptors, -0.025 to +0.010), where the
  fact was redundancy: the descriptors encode the same molecule. The analogue here: with the destination known, a
  repeat customer's id is largely redundant with where they go. The definition says "with the destination known", so
  the reason is half-stated; it does not say why taxi_id, equally null, stays.
* Personal data (CLEAN-4, P1) is not the reason: the ids are anonymised by the organisers.

```text
**Consistency check (AI, 2026-10-20):** pkdd_15 drops ORIGIN_CALL for a null gain once the destination is known
(-0.001 to +0.002 R^2) but keeps taxi_id with the same null gain (-0.004 to +0.003). What sets them apart? (a)
ORIGIN_CALL is redundant with the destination (the customer's usual trip), as the SMILES was with the descriptors
(CLEAN-24 case, 2026-10-14), while taxi_id stands for the driver, which the destination does not encode: recorded as
the reason; (b) keep ORIGIN_CALL as a categorical like taxi_id; (c) drop taxi_id too; (d) revisit after issue 1, since
pickup-only it adds +0.002 to +0.005.
```

**8. Monthly windows (issue 6): consistent, reason stated**

The ETA family (delivery_eta_1m, maps_router_eta_1m, cooking_time_1m) and nyc take 3 x 7 days. pkdd's months rest on a
fact of its source (the challenge tested 1.5 to 6 months after its training year; SPLIT-12, SPLIT-19), which nyc's
precedent check (2026-10-20, decision 4) already accepted as setting the two apart. SPLIT-21 (Must; aeolus, Lennart
2026-10-12): the choice must not be made from scores over the windows; issue 6 does not, keep it that way.

**9. Hour of day (issue 7): consistent with nyc; collection-wide**

Same question and same implementation as nyc (no extra column, CLEAN-2). The working copy's REVIEW.md item "Which
datetime encoding the v0.2 runs use" covers both; close pkdd's issue 7 with it.

**10. UTC to Lisbon wall-clock (issue 9): consistent**

nyc repaired its 86 trips across the DST switch (PROV-13) so that the times are local wall-clock times; pkdd's
conversion serves the same end, on measured evidence (profile correlation 0.92 / 0.90 to 0.99).

**11. Year 2015 (issue 10): consistent; the alternative breaks a Must**

PROV-9 (Must) takes the year of first publication, "a competition's launch", "not the collection period"; the
curator applied it three times today (airfoil_self_noise, first_principles_tully_fisher, nikuradse_1/2). The
ECML/PKDD 2015 challenge launched in 2015; the record and kick (2011), rossmann_store_sales (2015) and
acquire_valued_shoppers_challenge (2014) follow the same reading. The alternative `2013` (UCI's year of creation, the
start of the collection) would be the collection period. Minor: the BibTeX year `{2013}` follows UCI's citation and
differs from `year`; nyc has the same kind of difference (year 2016, Kaggle BibTeX 2017). Not a departure.

**12-13. Row budget and domain: consistent**

pkdd already uses the temporal `_1m` path (`version_of`, `subsample_to_budget = True`, one random order) of
delivery_eta_1m, the path nyc's mediator recommends for nyc (its issue 5, a). The frame (1,655,983) exceeds 1.5M, so
both readings of definitions.md hold. `domain`: every ETA definition reads `industry & manufacturing`; the record field
`Other` is stale, as nyc's record is (nyc's change 6 asks to set it).

**Third exceptions and drift**

* No exception is recorded for pkdd, so none counts toward a third.
* Related cross-dataset pattern (not pkdd's to decide): the gap. nyc (gap 1 day) and the three TabReD ETA sets (no gap,
  unmeasured) differ on the same mechanism; if pkdd takes no gap, the family has two unmeasured and one measured
  answer. A check of SPLIT-9 on delivery_eta_1m, maps_router_eta_1m and cooking_time_1m would settle the family.
* The CC of 2026-09-21 holds two reasons later rules replaced (pickup-only's weak signal by TP-2; taxi as group by
  SPLIT-3). That is a rule change, not drift; decision 1 asks for the reason to be restated.

**Files**

* `datasets/_dev/tabarena-v0pt2/pkdd_15_taxi_trip_time_prediction_ii_1m/dataset.py`
* `curation/records/pkdd_15_taxi_trip_time_prediction_ii.md`
* `datasets/_dev/tabarena-v0pt2/nyc_taxi_trip_duration/REVIEW.md` (mediator, precedent check)
* `datasets/_dev/tabarena-v0pt2/REVIEW.md` ("Rules from the nyc_taxi_trip_duration review")
* `datasets/_dev/tabarena-v0pt2/{delivery_eta_1m,maps_router_eta_1m,cooking_time_1m}/dataset.py`
* `.claude/skills/knowledge-curation/references/{use_case,splits,cleaning_features,provenance,task_probes}.md`

</details>

<details><summary>Checklist</summary>

**Checklist: pkdd_15_taxi_trip_time_prediction_ii_1m (re-check, 2026-10-20)**

Folder `datasets/_dev/tabarena-v0pt2/pkdd_15_taxi_trip_time_prediction_ii_1m/`. Measurements on the shipped frame
(1,436,885 rows) and its 3 splits.

**Automated**

- `dataset list`: imports and validates (temporal_non_iid, checked). `uvx ruff@0.15.15 check`: clean; `format --check`: clean.
- `dataset check`: 0 errors, 0 warnings, 0 info (26 checks); no accepted warnings. Checksum unchanged
  (`v2:c2fcc81b...921da2`); the README diff is template-only (`time_gap: null`, `time_gap_unit: null`, a `REVIEW.md`
  row in the file table). No code change was needed.
- `sync-notebooks --check`: clean (record `v2_path` points at this dataset.py).
- Probes: leak (no copies, no single-feature shortcut), task (no flags), hidden groups (no hits), generated (no flags).
  Group probes not run: the task is temporal.

**The checks, in rank order**

| Rank | Check | Result | Evidence | Rules |
|---|---|---|---|---|
| P1 | Ethics | pass | Taxi ids and caller phone ids anonymised by the organisers; ORIGIN_CALL dropped; data published CC BY 4.0 by its creators. Start/end points at ~10 m precision are passenger locations, but already public in the source. | SEL-1 |
| P2 | Scope | pass (framing is ours) | Source task (Task II) is the remaining time of a partial trajectory, a sequence task; the definition reframes it as ETA at pickup (curator CC 2026-09-21). Regression on a real decision; the GPS modality is reduced to two endpoints. | SEL-2 to SEL-15, TP-10 |
| P2, P5 | Real data | pass | Every trip of 442 taxis in Porto, UCI 339 (creators Moreira-Matias et al.). generated_probes: no flags (exact-formula 0.8% vs shuffled 0.8%, 0 of 6 uniform columns). | SEL-16, PROV-3 |
| P3 | Use case and fit | concern | `fit="approximate"`, fit_reason names the gap. The end point (last GPS point) is the destination; the UCI page says only "The last list item corresponds to the trip's destination"; the "drivers do not indicate the final destination" quote is from the challenge overview (geolink.pt via Wayback) and Lam et al. 2015, not re-fetched today (cannot verify the quote this run). Open as issue 1 of the earlier REVIEW.md. Leak probe: R² 0.377 with all features, 0.269 without end_lat, 0.231 without end_lon. | USE-1, USE-2, USE-8, USE-9 |
| P3, P4 | Target and metric | concern (open choice) | Target = log1p((points-1)·15 s), the challenge's definition (UCI: "one pair of coordinates for each 15 seconds"); RMSE on log1p = RMSLE, the challenge metric. Windows complete: trips are indexed by start, the last local day (118 trips) trimmed. Filters on the target: 15,533 trips < 60 s and 827 > 3 h dropped, also from test (the earlier REVIEW.md issue 2). | USE-5, LEAK-22 to LEAK-26, EV-5, CLEAN-11, CLEAN-15 |
| P4 | Available at prediction time | concern | (a) end_lat/end_lon are the trip's last GPS point, recorded after the trip (see P3). (b) SPLIT-9: train rows whose trip ends after the test window start: 33 / 27 / 6 of 1M (June / May / April windows), no gap declared (`time_gap: null`). Differs from nyc_taxi_trip_duration, which added a 1-day gap for 77/119/127 such rows (weekly windows). Here the effect is at most 3 h of a 1-month horizon; the mildest remedy would be a gap of a few hours/1 day. Not raised in the earlier REVIEW.md. | USE-3, USE-6, LEAK-10, LEAK-12, SPLIT-9, SPLIT-10 |
| P4 | Irreversible and all-row leakage | pass | No all-row or label-aware transform: every filter and the target are per row (`_row_filters`, `_clean`). | LEAK-13 to LEAK-15, LEAK-27 to LEAK-31 |
| P4 | Copies across the split | pass | Leak probe: 0.0% test rows with an exact feature copy in train (also with datetime/string columns). Hidden groups: near-copy clusters 0.0%. Duplicate TRIP_IDs (21 rows among trips with ≥ 2 points) dropped. | LEAK-16 to LEAK-21, SPLIT-29 |
| P4 | Split regime | pass, with open choices | Temporal, 3 monthly windows Apr-Jun 2014, expanding train capped to a random 1M (one random order, subsample_to_budget). taxi_id: 99.9-100% of test rows seen in train (hidden_groups), so a grouped split would test a case deployment rarely meets. origin_stand 47% seen (a location attribute, not an entity). Window length (monthly vs nyc's weekly) is the earlier REVIEW.md issue 6; no gap (see P4 above). | SPLIT-1 to SPLIT-31, USE-10, USE-11 |
| P5 | Source | pass | source_url Kaggle Task II; bibtex UCI 339, DOI 10.24432/C55W25, creators match the UCI page. year 2015 vs UCI 2013 is the earlier REVIEW.md issue 10. Record `domain` Other vs definition `industry & manufacturing` (as for nyc). | PROV-1, PROV-2, PROV-8 to PROV-12, PROV-16 to PROV-18 |
| P5 | Uniqueness | pass | Only folder on this data in the working copy (porto_seguro is an unrelated insurance set). Kaggle Task I and II share the same train.csv (533,605,607-byte zip per download_description); one task ships. Not the NYC data (other city, other operator). | PROV-4 to PROV-7 |
| P5 | Damage and repair | pass | TIMESTAMP is UTC: DST decision table, profile correlation 0.92 / 0.90 unshifted vs 0.992 / 0.994 shifted; converted to Europe/Lisbon. DAY_TYPE ("has not been correctly calculated", UCI) and MISSING_DATA (unreliable) dropped. | PROV-13 to PROV-15 |
| P6 | Worth benchmarking | pass | Task probe, 3/3 splits: LightGBM skill +0.373 ± 0.018 (R² 0.37, RMSE 0.470 vs dummy 0.593), beats dummy on 100% of splits; RF +0.365; linear +0.044; best single feature end_lat +0.098; flags none. Note: the probe's R² (0.37) is below the 0.48-0.50 the definition quotes (its own LightGBM with the local hour); the panel should not read the gap as a contradiction without matching the setup. Leak probe: dropping taxi_id raises R² 0.377 → 0.391 (50k-row sample), consistent with the earlier REVIEW.md issue 4 (taxi_id adds ~nothing). | TP-1 to TP-10 |
| P7 | Dtypes and cleaning | pass, cross-dataset item | call_type, origin_stand (63 levels, 52.1% missing = not a stand hire), taxi_id (441) categorical; start_time datetime; coordinates float. Empty ORIGIN_STAND set missing. The hour of day depends on the harness's datetime encoding (the earlier REVIEW.md issue 7; the same question as nyc, now a cross-dataset item in `tabarena-v0pt2/REVIEW.md`). | CLEAN-1 to CLEAN-24, CLEAN-2 |
| procedure | Notes match the code | pass, minor concerns | Filters, drops, renames and mappings all match `_row_filters` / `_clean`; decision-table counts match the bullets (1,655,983 after filters). Minor: "65,708 (4.0%) end within 500 m" is on the cleaned 1,655,983, not the shipped 1,436,885 frame (56,962, 3.96%; within 100 m 20,592; identical coordinates 76). "1.2% jump > 1 km" and "70% / 31% / 7% of 15/60/120-s trips within 100 m" need the polylines; nothing in the code computes them (cannot verify from the frame). | writing.md |
| procedure | Licence and citation | pass | UCI page: "licensed under a Creative Commons Attribution 4.0 International (CC BY 4.0) license"; DOI 10.24432/C55W25. | EV-4, PROV-10 |
| procedure | Reproducibility | pass | UCI zip URL returns HTTP 200 (not re-downloaded); local train.csv sha256 2891d03e...efff6d matches the definition; 1,710,670 data lines. | |

**Where pkdd differs from nyc_taxi_trip_duration (re-reviewed today)**

- **One-point / identical-endpoint trips (USE-7, the cross-dataset item):** nyc dropped 4,539 trips (0.31%) with
  identical pickup and drop-off coordinates. In pkdd the < 2-point and < 60-s filters already remove most of them:
  76 kept trips (0.005%) have identical start and end coordinates (5 / 9 / 11 in the June / May / April test windows;
  mean target 5.46 vs 6.41). The open question here is wider: 20,592 shipped trips (1.4%) end within 100 m and 56,962
  (4.0%) within 500 m (the earlier REVIEW.md issue 3, which says "NYC kept its 0.4% of one-point trips": out of date now that nyc
  drops them).
- **Datetime encoding:** same question as nyc (the earlier REVIEW.md issue 7); the cross-dataset item proposes to close it
  together.
- **Gap (SPLIT-9/10):** nyc now has a 1-day gap; pkdd has none, with 6-33 train rows of 1M per window ending after the
  window start (monthly windows).
- **Fit label:** both `approximate` now (nyc's mediator aligned nyc with pkdd).
- **Row budget:** pkdd already follows the `_1m` path (`version_of`, `subsample_to_budget`), the path nyc's mediator
  recommended (nyc issue 5, option a).
- **Short-trip cut:** pkdd 60 s (15-s GPS resolution), nyc 30 s (1-s clock).

**Draft issues (rank order)**

1. P3/P4 USE-8, LEAK-10: the destination (last GPS point) as a feature, the source says drivers do not enter it (the earlier REVIEW.md 1, open).
2. P4 SPLIT-9/SPLIT-10: no gap; 6-33 train trips per window end after the window start (new; nyc took a 1-day gap).
3. P3/P4 USE-7: trips ending at/near their start, now to be decided like nyc (the earlier REVIEW.md 3; its nyc comparison is out of date).
4. P3 CLEAN-11/15: 60-s and 120 km/h filters, the first on the target (the earlier REVIEW.md 2).
5. P4 SPLIT: monthly vs weekly windows (the earlier REVIEW.md 6).
6. P7 CLEAN-2: datetime encoding (the earlier REVIEW.md 7, cross-dataset).
7. procedure: notes give counts on the pre-subsample frame (65,708 / 4.0%), and two numbers not reproducible from the code.
8. the earlier REVIEW.md 4, 5, 8, 9, 10 (taxi group, ORIGIN_CALL, label noise, local time, year) stand as before; nothing new measured against them except the leak probe's taxi_id drop (+0.014 R²).

**Cannot verify (this run)**

- The "do not indicate the final destination" quote (challenge overview, Wayback) and Lam et al. 2015: not re-fetched.
- The 1.2% GPS-jump share and the 70/31/7% slope: need the polylines (not in trips.parquet).
- The UCI zip content (not re-downloaded; only HTTP 200 checked).

</details>

<details><summary>Advocate</summary>

**Advocate: ship pkdd_15_taxi_trip_time_prediction_ii_1m as defined (opening brief, 2026-10-20)**

Position: ship. Two problems the auditors found are real and each has a definition-level fix that keeps the dataset
(points 3 and 4); I concede them rather than deny them. Nothing found reaches exclusion on the remedy ladder.

**1. The destination framing is a real, disclosed task, and it matches the sibling (P3: USE-1, USE-8 Must, USE-12 Must)**

- Claim: an ETA at pickup with the destination known is a task actors run (dispatch planning; upfront quotes in
  ride-hailing apps, practitioner sec. "USE-9 check"), and the definition states its gap: `fit="approximate"`, with
  the fit_reason quoting the source ("drivers do not enter the destination") and the pickup-only R² 0.11-0.15.
- Evidence: claim audit I1 and claims 8-9 (holds: 0.127 / 0.124 / 0.152 without, 0.535 / 0.516 / 0.533 with); the blind
  reviewer, with no notes, read the task the same way ("a real origin-destination ETA task ... same shape as NYC") and
  said include. nyc_taxi_trip_duration (panel today) ships the same framing with the same label, on the same fact.
- Rule: USE-8 (Must) asks that the fit be written; it is. USE-8 lists "a potential leak kept on purpose" as an
  approximate stand-in, which is what the end point is under the curator's framing (CC 2026-09-21). USE-12 (Must): a
  leak is no reason to reject a real task.
- Against the expected objection (LEAK-10/USE-3, Must: the end point is recorded after the trip): the prediction point
  is set by the use case, and under it the destination is named at pickup; the realised drop-off is the stand-in,
  named as such. TP-6 (Must) does not force pickup-only: the source defines Task I and Task II on partial
  trajectories, and pickup-only is neither (precedents, decision 1). Treat like cases alike: switching pkdd alone would
  need a fact that sets it apart from nyc. What I concede: the CC's stated reason (weak pickup-only signal) no longer
  holds under TP-2; the record should state reason (a) of the precedent checker's consistency check instead. That is a
  wording fix, not a change of the task. The framing stays the curator's call.

**2. The evaluation mirrors the application (P4: SPLIT-1, SPLIT-3 Must, USE-10, SPLIT-11, SPLIT-14)**

- Evidence (split audit): known fleet, 99.93-100% of test trips by taxis in train, 0-1 new taxi per month; stands 100%
  seen. Temporal, expanding history (11 / 10 / 9 months), complete monthly test windows of 131,659-156,990 trips, no
  index overlap. A random split would be optimistic by 0.02-0.03 R²; the temporal one is not. No copies (0.0% exact
  and near), no hidden groups.
- Rule: SPLIT-3 (one regime, the one the use case implies; Lennart 2026-10-12) supersedes the CC's "taxi as group";
  USE-10 weighs for the known entity. Monthly windows rest on a source fact (the challenge tested 1.5-6 months after
  its training year), which nyc's precedent check already accepted as setting the two apart (SPLIT-12, SPLIT-19);
  SPLIT-21 (Must) forbids choosing windows by score, so the weekly alternative needs a reason other than decay.

**3. SPLIT-9 (Must): conceded in letter; the fix is a one-day gap, as nyc**

- Evidence: 33 / 27 / 6 of 1M train trips per window end after the window start (claim audit I2, split audit). Their
  effect: a 1-day gap changes R² by -0.002 to +0.005, within seed noise.
- Remedy (ladder rung 2, fix the definition): a one-day gap, like nyc's. Since `TemporalSplits` counts the gap in
  months, use day units with the three month-start cutoffs and `gap=1` (split audit option a; loses about 5k trips of
  31 May), or the `Temporal` gap unit the API documents. Not exclusion, not a filter on the trip's end time (that
  uses the target, SPLIT-10's "Why"). Effect size is not a reason to skip a Must, so I do not argue (c).

**4. USE-7 (Must): conceded for the 76 identical-endpoint trips; the near-start band stays**

- Evidence: 76 trips whose end equals the start (5 / 9 / 11 in test), column audit problem 2; nyc drops its 4,539 under
  USE-7 (bias_correction precedent, Lennart 2026-10-15). the earlier REVIEW.md issue 3's "nyc kept them" is out of date.
- Remedy: drop the 76 in `_row_filters` (a filter on features, applicable in deployment).
- The 20,516 trips within 100 m but not identical stay: unusual, not impossible (CLEAN-11 Should), and nyc keeps its
  near-but-not-identical trips. Dropping the band would be a new filter without precedent; the curator may weigh it,
  but it is not a validity problem (it raises R² by about 0.05 by removing noise, the earlier REVIEW.md issue 3: noise, not a
  leak).

**5. The data is faithful and every count reproduces (P5: PROV-1, PROV-9, PROV-13, PROV-14)**

- Evidence (claim audit): sha256 matches, 1,710,670 trips, UTC range exact; every filter count reproduces (36,510 / 21
  / 937 / 15,533 / 827 / 741 / 118, left 1,655,983); TRIP_ID = TIMESTAMP + "6" + TAXI_ID on 100% of rows; the UTC
  claim survives a placebo (shifted correlation 0.992 / 0.994 at the switches, 0.896 in fortnights without a switch);
  725 of 741 speed-dropped trips have a GPS jump over 1 km. `year = "2015"` follows PROV-9 (Must), as applied three
  times today. Only the zip byte size and one quote's exact wording are untested; Lam et al. confirms its meaning.

**6. Worth benchmarking (P6: TP-2, TP-3)**

- 1,436,885 rows, 8 mixed-type features (categorical, datetime, coordinates); LightGBM R² 0.47-0.54 on the shipped
  windows against a linear model's 0.04 (task probe): the geometry has to be learned, which separates models. Every
  window has over 130k test rows, so every fold is scorable.

**7. The cleaning is minimal and documented; its gaps are P7 notes (CLEAN-11, CLEAN-15, CLEAN-16, CLEAN-22)**

- The 60 s / 3 h / 120 km/h cuts remove non-trips, meters left running and GPS jumps, with evidence outside the target
  for each (70% / 31% of 15 s / 60 s trips end within 100 m; 725 of 741 GPS jumps) and the same 3 h threshold as nyc.
  That they also apply to test is written (REVIEW issue 2); 1% of rows. Lowering the short cut to 30 s (nyc's, where
  outside evidence is 50%) is a weighing call for the curator, not a validity problem.
- Conceded wording fixes: ORIGIN_CALL's reason should read "an identifier redundant with the destination" (CLEAN-24
  analogue), not its 57k count (CLEAN-22); REVIEW issue 4's taxi_id number is refuted (+0.008 to +0.014 R², top gain
  feature), which strengthens keeping taxi_id and answers the pair question (precedents, decision 7: the taxi is the
  driver, which the destination does not encode). `splits_comment` should state the gap and that the one year of data
  has no earlier April-June (SPLIT-20 note).

Judgment I argue for:

```text
Verdict: ship after changes.
Validity: USE-1 holds; USE-8 approximate (realised drop-off stands in for the named destination, as nyc); USE-7
  triggered, fixed (76 identical-endpoint trips dropped); SPLIT-3 holds (temporal, taxi a feature); SPLIT-9 triggered,
  fixed (one-day gap); PROV-1/9/13 hold.
Value: TP-2/TP-3, R² 0.47-0.54, linear 0.04.
Quality: CLEAN-11 target cuts kept with a note; ORIGIN_CALL reason reworded.
Weighed: size +, source +, consistency with nyc +, destination not captured in the source -, no routing estimate -.
For the curator: the framing (issue 1, restate the CC's reason); the 60 s vs 30 s cut.
```

</details>

<details><summary>Critic</summary>

**Critic: pkdd_15_taxi_trip_time_prediction_ii_1m (opening brief, 2026-10-20)**

**Position: ship only after changes.** The task is real (an ETA at pickup, approximate) and I do not ask to exclude it.
Two Musts are broken in ways that nyc_taxi_trip_duration, reviewed today on the same mechanisms, fixed; the framing
rests on a reason the rules no longer accept; and two stated numbers are wrong. All fixes are in the definition or
its text.

**1. The destination framing stands on a rejected reason (P3; USE-8 Must, TP-2 Should, USE-3 Must)**

- Problem: `end_lat`/`end_lon` are the last GPS point, recorded when the meter goes off; the source says drivers do
  not enter the destination (data page; Lam et al. 2015 Sec. 1). They carry most of the signal: R^2 0.52-0.54 with,
  0.12-0.15 without (claim audit s3, I1 REFUTED as a fact of the source). The definition's `fit_reason` justifies the
  feature by the score: "Without it the signal is weak (R^2 0.11 to 0.15)", the same reason as the curator's CC of
  2026-09-21. TP-2 (2026-10-06, forest_fires) says a small real signal is no reason to change a framing; the
  precedent checker flags the CC's reason as superseded.
- Effect: the benchmark measures an ETA given the realised drop-off, which is cleaner than any stated destination
  (detours, round trips, 4% end within 500 m; practitioner gap 1). Fine as an approximate stand-in, but the written
  reason for it is invalid.
- Remedy (fix the text, curator's call on the framing): rewrite `fit_reason` to name the gap, not the score: "the
  realised drop-off stands in for a destination named at pickup, which the source's dispatch system did not record;
  no routing estimate". Put the precedent checker's consistency check (decision 1) to the curator, and record the
  answer as the reason, aligned with nyc (same framing, same label).

**2. 76 trips whose end point is the start point are kept (P3; USE-7 Must)**

- Problem: for these rows the input the ETA acts on, a destination, does not exist: no passenger names the pickup as
  destination. 76 trips, 5/9/11 in the June/May/April test windows, mean target 5.46 vs 6.41 (column audit 2;
  precedents 3).
- Evidence of inconsistency: nyc drops its 4,539 such trips under USE-7, after bias_correction (Lennart, 2026-10-15).
  pkdd's REVIEW issue 3 gives "NYC kept its 0.4% of one-point trips", now false.
- Remedy (fix the definition): add an "end point equals start point" filter to `_row_filters` (a filter on features,
  usable in deployment); correct issue 3. A Must has no exception; "the polyline shows the taxi moving" was not
  measured and would not give a stated destination either. The 100 m band stays the curator's call (nyc keeps its
  near-but-not-identical trips, CLEAN-11).

**3. No gap although train holds labels not known at the window start (P4; SPLIT-9 Must, SPLIT-10 Should)**

- Problem: 33/27/6 of 1M train trips per window end after the window start, their mean target 6.64-6.88 vs 6.41: the
  long trips (split audit, problem 1). `time_gap: null`, and `splits_comment` says nothing about it.
- Effect: measured within seed noise (a 1-day gap moves R^2 by -0.002 to +0.005). But SPLIT-9 is a Must, and the
  size of the effect is not a fact that sets a case apart (tension row "the right split against the score").
- Inconsistency: nyc took `gap=1` (day) for 77/119/127 such trips today.
- Remedy (fix the definition): a gap of one day. `TemporalSplits` counts the gap in the window's unit, so either
  `window=30, unit="days"` with explicit month cutoffs and `gap=1`, or the weekly windows of issue 6 with `gap=1`.
  State the gap in `splits_comment` as part of the task. If the curator wants months and no gap, that is an amendment
  of SPLIT-9 (a share of late labels below which no gap is needed), which then has to be checked on delivery_eta_1m,
  maps_router_eta_1m and cooking_time_1m, not a silent departure.

**4. The 60-s cut drops test rows on the label where the outside evidence has thinned (P4/P7; CLEAN-11, CLEAN-15 Should; USE-7)**

- Problem: 15,533 trips under 60 s are dropped from train and test; they hold 21% of the log-target variance. The
  evidence that they are non-rides is outside the target only for the shortest: 70% of 15-s trips end within 100 m,
  50% at 30 s, 40% at 45 s, 31% at 60 s (claim 22 holds). Most trips cut between 45 and 60 s moved. A deployment
  cannot apply a label cut (practitioner gap 4).
- Effect: the test set is cleaner than what the model meets, and real short rides are removed.
- Remedy (fix the definition, or a note): move the cut to 30 s, where at least half end within 100 m, which also
  matches nyc's 30 s; or keep 60 s with the reason written as a choice on the slope. Not a reason to exclude.

**5. Two stated numbers are wrong (procedure; EV-8 Should)**

- REVIEW issue 4: "taxi_id changes LightGBM R^2 by only -0.004 to +0.003". Refuted: +0.010/+0.008/+0.014, and
  taxi_id is the top gain feature (claim audit, side claims; split audit's cold-start test 0.014-0.029). The precedent
  checker's consistency check 7 (ORIGIN_CALL dropped vs taxi_id kept "with the same null gain") rests on that false
  number: with the right number the two are set apart by measurement, and the check should be withdrawn.
- `curation_comments` ORIGIN_CALL: "R^2 -0.001 to +0.002"; re-measured -0.0026 to -0.0008 (claim 24). The code
  comment "ORIGIN_CALL (57k phone ids)" reads as a width argument (CLEAN-22 Must forbids that reason); reword to "an
  identifier that adds nothing once the destination is known".
- Remedy: correct both numbers with the model setup stated; reword the comment.

**6. Notes the definition owes (P4/P5; SPLIT-20 Should, PROV-8)**

- `splits_comment`: one year of data, so the test season (April-June) has no earlier copy in train (split audit 3).
- Record `domain` `Other` vs definition `industry & manufacturing`: set the record, as for nyc.
- Record investigation counts "1,459 outside Porto" and "1,672,071 after filters" do not reproduce (1,084 /
  1,672,375); add a CC line pointing to the decision table.
- Remedy: notes only.

**Not argued**

The temporal regime with taxi as a feature (USE-10, SPLIT-3), monthly windows (SPLIT-12, reason stated), local time
(PROV-13), the 120 km/h and 3-h cuts, the row budget and the year hold on the evidence; I do not contest them.

</details>

<details><summary>Advocate rebuttal</summary>

**Advocate: rebuttal of the critic (2026-10-20)**

The critic and I agree on the verdict: ship after changes, with no exclusion. The two briefs ask for the same fixes on
SPLIT-9 and USE-7. We differ on one weighing call, the 60-s cut, and on one window choice that belongs in the fix for
critic point 3.

**Critic 1 (the framing's written reason): conceded**

- The `fit_reason` justifies the end point with the score ("Without it the signal is weak"). That is the CC's reason,
  and TP-2 no longer accepts it. My brief point 1 conceded this for the record. It applies to `fit_reason` too.
- What follows: rewrite `fit_reason` to name the gap. The critic's wording works: the realised drop-off stands in for
  a destination named at pickup, which the source's dispatch system did not record, and there is no routing estimate.
  The pickup-only R² can stay as a fact, but not as the reason. Then put precedent decision 1 to the curator, aligned
  with nyc.
- Both sides agree that the framing itself is valid (USE-8 approximate, USE-12).

**Critic 2 (USE-7, 76 identical-endpoint trips): conceded**

- Drop them in `_row_filters` and correct REVIEW issue 3's sentence about nyc. We agree that the 100 m band stays
  (CLEAN-11, nyc).

**Critic 3 (SPLIT-9, no gap): conceded; one part disputed**

- Conceded: a one-day gap, stated in `splits_comment`. This is the same remedy as my brief point 3.
- Disputed: the gap is no reason to switch to the weekly windows of issue 6. The monthly windows rest on a source fact:
  the challenge tested 1.5-6 months after its training year (SPLIT-12, SPLIT-19), and nyc's precedent check accepted
  it. The critic itself does not contest them ("Not argued"). Switching would break nothing, but using the gap API to
  pick a window length makes the mechanics decide the task, and the split follows the application (SPLIT-4).
- So use `window=30, unit="days"` with the three month-start cutoffs and `gap=1` (split audit option a). That loses
  about 5k trips of 31 May.

**Critic 4 (the 60-s cut): partly disputed; a weighing call for the curator**

- Conceded: the cut is on the label, it also applies to test, and a deployment cannot apply it. The dropped trips hold
  21% of the log-target variance. The note should say all of this (REVIEW issue 2).
- Disputed: the claim that "the outside evidence has thinned" at 60 s. Against the base rate, it has not. Of all
  cleaned trips, 23,712 of 1,655,983 (1.4%) end within 100 m of their start. At 60 s the share is 31%, about 20 times
  that; at 45 s it is 40% (claim 22, holds). A 45-60-s hire with a real destination is barely a ride a dispatcher
  plans for (USE-7 spirit).
- On nyc: its 30 s sits on a 1-s clock. Here 60 s is four 15-s GPS points, so travel times are coarse at the bottom:
  a recorded 45 s can be anything from about 45 to 74 s of real time. Equal seconds are not like cases (the precedent
  checker, decision 4, accepts the stated difference).
- What follows: keep 60 s with the reason written as a choice on the slope, the critic's own second option. The
  curator may move it to 30 s. Neither choice is a validity problem (CLEAN-11, Should). This is a weighing call; the
  mediator should not settle it.

**Critic 5 (two wrong numbers): conceded**

- Correct REVIEW issue 4 to +0.008 to +0.014 R² for taxi_id, and the ORIGIN_CALL range to -0.0026 to -0.0008. State
  the model setup with each (EV-8). Reword the "57k phone ids" comment (CLEAN-22).
- I also agree to withdraw precedent check 7: once measured, the two columns are set apart. My brief point 7 reached
  the same place.

**Critic 6 (notes): conceded**

- Add the SPLIT-20 note in `splits_comment`, set the record's `domain`, and add a CC line pointing to the decision
  table for the two investigation counts that do not reproduce.

**Net**

Changes now:
- the `fit_reason` text;
- drop the 76 trips;
- the one-day gap on monthly cutoffs;
- the corrected numbers and wording;
- the notes.

For the curator:
- the framing (decision 1);
- 60 s or 30 s.

</details>

<details><summary>Critic rebuttal</summary>

**Critic: rebuttal of the advocate (2026-10-20)**

We now agree on the verdict, ship after changes, and on the two Must fixes. One dispute is left (point 1, the
wording of the definition's own `fit_reason`), and one point (7) where we differ only on how strong the evidence is.
No new facts.

| Advocate's point | Answer | Evidence and rule |
|---|---|---|
| 1. Destination framing is real, disclosed, matches nyc | **Concede the framing; dispute "a wording fix in the record" as the whole remedy.** The definition repeats the rejected reason, not just the CC: `fit_reason` ends "Without it the signal is weak (R² 0.11 to 0.15)". That argues from the score, which TP-2 rejects as a reason to choose a framing. USE-8 (Must) asks for the gap to be named. The gap is the realised drop-off standing in for a destination the source's dispatch system never received, with no routing estimate (practitioner gaps 1-2). | USE-8 (Must) over TP-2 (Should). Remedy: rewrite `fit_reason` in the definition, and add the restated CC reason (precedents, check 1, option a) to the record. The task stays as it is. |
| 2. Split mirrors the application | **Concede.** Temporal with a known fleet is right. I also concede the SPLIT-21 point: weekly windows may be used only to get the gap working in the API, not chosen by score. | USE-10, SPLIT-3, SPLIT-21 |
| 3. SPLIT-9 conceded; one-day gap | **Agree.** Both of us reject option (c) and the end-time filter. Add: state the gap in `splits_comment`. | SPLIT-9 (Must), SPLIT-10 |
| 4. USE-7: drop the 76; keep the 100 m band | **Agree.** Correct REVIEW issue 3's out-of-date nyc sentence. | USE-7 (Must); CLEAN-11 for the band |
| 5. Data faithful, counts reproduce | **Concede.** The two record counts that don't reproduce (1,459 / 1,672,071) are superseded by the decision table, so a CC note is enough. | PROV-1/9/13/14, EV-8 |
| 6. Worth benchmarking | **Concede.** | TP-2, TP-3 |
| 7. Cleaning minimal; 60 s vs 30 s a weighing call | **Concede it is a curator call, not validity. Dispute "evidence outside the target for each".** At the 60 s threshold only 31% of trips end within 100 m. Most of the trips cut between 45 and 60 s moved, and the cut removes 21% of the log-target variance from test too. The curator should see that slope with the choice, and nyc's 30 s is where the outside evidence is still at least 50%. | CLEAN-11, CLEAN-15 (Should); treat like cases alike (nyc) |
| 7. ORIGIN_CALL wording, taxi_id number, SPLIT-20 note | **Agree.** The corrected taxi_id number (+0.008 to +0.014) settles precedents check 7, so withdraw it. | CLEAN-22 (Must, wording), CLEAN-24, EV-8 |

**Left for the mediator:** whether `fit_reason` in `dataset.py` must drop the score argument (I say yes, under USE-8
and TP-2), and how the 60 s cut is presented to the curator.

</details>

<details><summary>Mediator</summary>

**pkdd_15_taxi_trip_time_prediction_ii_1m: mediator (2026-10-20, re-check)**

**Judgment record**

```text
Verdict: ship after changes.
Validity: USE-1 holds; USE-8 approximate (the realised drop-off stands in for a destination named at pickup, which
  the source's dispatch system never received; no routing estimate), fit_reason rewritten to name the gap, not the
  score; USE-7 triggered, fixed (76 trips with identical start and end dropped); SPLIT-3 holds (temporal, taxi a
  feature, USE-10); SPLIT-9 triggered (47/32/6 late labels per window on the frame), fixed by a one-day gap on the
  month-start cutoffs (measured 0/0/0); SPLIT-12 holds (monthly, from the challenge's 1.5-6-month test gap);
  SPLIT-20 kept with a note (one year, no earlier April-June); PROV-1/9/13/14 hold.
Value: TP-2/TP-3, R² 0.47-0.54 (LightGBM, setup-dependent) against linear 0.04; >130k test rows per window.
Quality: CLEAN-11/USE-7 short-trip cut kept for now with its slope written (threshold open, issue 2); ORIGIN_CALL
  reason reworded (CLEAN-22/CLEAN-24); two numbers corrected (EV-8).
Weighed: size +, source +, consistency with nyc +, destination not captured in the source -, no routing estimate -,
  one year of history -.
For the curator: issue 1, restate the reason for the destination framing (P3); issue 2, the short-trip cut at 60 s
  or 30 s (weighing).
```

**Changes to make now (no decision needed)**

1. **Drop the 76 trips whose end point equals their start point** (5/9/11 in the June/May/April test windows). Add the filter to `_row_filters`. It is a filter on features, so a deployment can apply it. Update the decision table, and correct the sentence in REVIEW issue 3 that says nyc kept these trips. Keep the 20,516 trips that end within 100 m but not at the same point, as nyc does (CLEAN-11).
   - Rule: USE-7 (Must). Precedents: bias_correction (Lennart, 2026-10-15) and nyc (today).
2. **One-day gap, monthly cutoffs.** Use `Temporal(on="start_time", splits=TemporalSplits(window=30, unit="days", cutoffs=("2014-04-01", "2014-05-01", "2014-06-01"), gap=1))`, and state the gap in `splits_comment` as part of the task.
   - Rules: SPLIT-9 (Must), SPLIT-10, SPLIT-12, SPLIT-4.
   - Measured with the v2 API on the shipped frame. `Temporal` accepts the declaration.

     | Window | Test, now | Test, new | Late labels, now | Late labels, new |
     |---|---|---|---|---|
     | June | 148,236 | 148,236 | 47 | 0 |
     | May | 156,990 | 151,415 (31 May leaves) | 32 | 0 |
     | April | 131,659 | 131,659 | 6 | 0 |

   - The audit's 33/27/6 were counted on the capped 1M samples. The 47/32/6 above are on the frame.
   - The stored horizon becomes 30 days.
   - The April train pool stays above 1M: 1,219,098 eligible before the change, minus about 4k for 31 March.
3. **Rewrite `fit_reason`.** Name the gap: "the realised drop-off (last GPS point) stands in for a destination named at pickup, which the source's dispatch system did not record; no routing estimate". Keep the pickup-only R² 0.12-0.15 as a stated fact, not as the reason.
   - Rule: USE-8 (Must) asks for the gap to be named. TP-2 (Should) does not accept a weak signal as a reason to choose a framing.
   - Both rebuttals agree. The advocate conceded the definition text too, so this is no longer disputed.
4. **Numbers and wording.**
   - REVIEW issue 4: taxi_id adds +0.010/+0.008/+0.014 R² and is the top-gain feature. The stated -0.004 to +0.003 is refuted.
   - ORIGIN_CALL: the measured change is -0.0026 to -0.0008. State the model setup with each number.
   - Code comment: replace "ORIGIN_CALL (57k phone ids)" with "an identifier redundant with the destination".
   - Withdraw precedent check 7: the two columns are now set apart by measurement.
   - Re-measure the R² quoted in `curation_comments` and REVIEW after changes 1-2.
   - Rules: EV-8, CLEAN-22 (Must, a column does not leave for its count), CLEAN-24 analogue.
5. **Notes.**
   - `splits_comment`: one year of data, so the April-June test season has no earlier copy in train (SPLIT-20).
   - Record: set `domain` to `industry & manufacturing` (PROV-8, as nyc).
   - Record: the investigation counts "1,459 outside Porto" and "1,672,071 after the filters" do not reproduce (1,084 and 1,672,375; the decision table is authoritative). Add an `Assessment (AI, 2026-10-20)` line saying so. Both sides asked for a CC line, but a CC line is the curator's (records.md; nyc mediator).
   - REVIEW issue 1: "nyc's source kept the dropoff coordinates on purpose" no longer sets the two apart. nyc is now `approximate` on pkdd's own fact.
6. **Cross-dataset item, not pkdd's to fix.** Check SPLIT-9 on delivery_eta_1m, maps_router_eta_1m and cooking_time_1m. They ship weekly windows with no gap, and their late labels were never measured (precedent check 2).

**Disputed points, settled**

**A. Weekly windows against monthly windows with a one-day gap (SPLIT-12 Should, SPLIT-9 Must, P4). Settled: monthly.**
- This is not a conflict. Both window lengths can carry the Must fix: a gap of 1 is legal with day units.
- SPLIT-12 bases the horizon on the source: the challenge tested 1.5-6 months after its training year. nyc's precedent check accepted that fact as setting the two apart.
- Switching to weekly windows only to fit the API would let the mechanics choose the task (SPLIT-4). The critic conceded this in its rebuttal, and neither side contests the monthly windows on the merits.
- Remedy ladder: the declarative 30-day windows on the month-start cutoffs are the mildest fix (cost: 31 May).
- A custom `_make_splits` could keep exact calendar months, declaring `Temporal(gap=1, gap_unit="days", horizon=1, horizon_unit="months")`. But `subsample_to_budget` is refused with `_make_splits`, so the 1M sampling would have to be rewritten by hand. That is more code for 5.6k test rows. Not recommended.

**B. Whether the score argument may stay in `fit_reason`.** Settled under change 3: USE-8 (Must) and TP-2. The task stays as it is.

**Issues for the curator (ranked)**

1. **Reason for the destination framing (P3; USE-8 Must, TP-2 Should, TP-6). Validity.**
   - Problem: your CC of 2026-09-21 kept the destination because pickup-only has a weak signal (R² 0.14). TP-2 (2026-10-06) no longer accepts that reason.
   - Effect: the task is unchanged. The record and REVIEW carry a reason the rules reject.
   - Advocate's best evidence:
     - the blind reviewer read the task as a real origin-destination ETA;
     - nyc ships the same framing as `approximate`;
     - TP-6 does not force pickup-only, because the source defines only partial-trajectory tasks.
   - Critic's best evidence: the source says drivers do not enter the destination (Lam et al. 2015). The end point is recorded after the trip and carries R² 0.53 against 0.13 without it.
   - Both sides say keep the framing.
   - Decision: precedent check 1.
     - (a) Keep it, with the reason "an ETA once the passenger names the destination, approximate as nyc" (recommended).
     - (b) Pickup-only for pkdd, and reopen nyc.
     - (c) Pickup-only for pkdd alone, naming the fact that sets it apart.
     - (d) Amend USE-8/TP-6.
   - A switch to pickup-only also reopens ORIGIN_CALL, which adds +0.002 to +0.005 pickup-only.
2. **Short-trip cut: 60 s or 30 s (USE-7 Must, CLEAN-11 Should, CLEAN-15; P3/P7). A weighing call.**
   - What the rules settle: a row leaves only when it is no task row (USE-7). Otherwise unusual values stay (CLEAN-11). So the cut has to rest on evidence outside the target, as nyc's does.
   - What the rules leave open: how much evidence is enough. Nothing fixes a threshold, so the threshold is yours.
   - Effect: the cut applies to test too, and a deployment cannot apply it. The trips under 60 s are 0.9% of rows and 20.6% of the log-target sum of squares.
   - Measured by me before the short cut, all other filters on. Each bin is the travel time as recorded. Within 100 m of the start (base rate 1.95% of all trips):

     | Recorded time | Trips | Within 100 m | Median straight line |
     |---|---|---|---|
     | 15 s | 7,134 | 72% | 28 m |
     | 30 s | 4,310 | 53% | 82 m |
     | 45 s | 3,407 | 42% | 153 m |
     | 60 s (kept now) | 3,169 | 33% | 249 m |
     | 120 s | 4,280 | 7% | |

     - Within 100 m among all trips dropped by each cut: drop under 30 s (15-s bin only), 72% of 7,134; drop under 45 s, 65% of 11,444; drop under 60 s (now), 60% of 14,851.
     - The two taxis 20000080 and 20000066 record 3,349 of the 14,851 trips under 60 s, and 18-25% of each short bin. Without them the within-100 m shares change by at most 3-4 points.
   - Advocate's best evidence: at 45 s, 42% end within 100 m, about 20 times the base rate. A recorded 45 s spans roughly 45-75 s of real time on a 15-s clock, so nyc's 30 s is not a like case. The precedent check accepted that difference.
   - Critic's best evidence: in the 45-s bin most trips moved, so the cut removes real short rides from test. nyc's cut sits where most dropped rows show evidence outside the target.
   - The slope is smooth, with no break. Every option keeps a majority of non-moving trips among the rows it drops, so no rule tips it.
   - Decision:
     - (a) Keep 60 s, writing the slope down as a choice. This is the current state.
     - (b) 45 s: drop the 15-s and 30-s bins, where the majority ends within 100 m.
     - (c) 30 s: drop only the 15-s bin, closest to nyc's evidence level.
   - Do not choose by comparing scores (SPLIT-21 spirit, TP-2).

**Agreed facts**

- Source and provenance:
  - sha256 matches; 1,710,670 trips, July 2013 to June 2014 UTC.
  - Every filter count reproduces (left 1,655,983); the frame has 1,436,885 rows.
  - TRIP_ID is the start second plus taxi on 100% of rows.
  - TIMESTAMP is UTC (DST placebo holds), so local Lisbon time is right.
  - `year = 2015` follows PROV-9.
- The end point is the last GPS point, recorded after the trip. The source says drivers do not enter the destination.
- Scores:
  - R² 0.52-0.54 with the end point against 0.12-0.15 without it (claim audit setup); linear model 0.04.
  - taxi_id: +0.008 to +0.014, the top-gain feature.
  - ORIGIN_CALL: -0.0026 to -0.0008 with the destination.
- Regime:
  - Known fleet: 99.93-100% of test trips are by taxis seen in train.
  - Temporal is right; a random split would be optimistic by 0.02-0.03.
  - No copies and no hidden groups.
- 76 trips have identical endpoints (5/9/11 in test). nyc drops its equivalents under USE-7.
- With no gap, some train trips end after the window start (6-47 per window). The effect is within seed noise, but SPLIT-9 is a Must and effect size is no exception. nyc took `gap=1`.
- The API counts the gap in the window's unit. Option (a) works and is measured above.
- The 120 km/h cut is sound (725 of 741 trips have a GPS jump) and differs from nyc for a stated reason. The 3-h cut equals nyc's.

**Consistency with precedent**

- nyc_taxi_trip_duration (AI panel today, not yet decided by the curator):
  - followed on USE-7 (drop identical endpoints, keep the near band), the one-day gap and `approximate`;
  - not followed on the window length, for a stated source fact (the challenge's 1.5-6-month test gap), which nyc's precedent check accepted;
  - the short-cut threshold differs on clock resolution, which is accepted and left to issue 2.
  - If the curator later changes nyc on any of the shared points, pkdd follows.
- The TabReD ETA sets (no gap, unmeasured) are an unchecked counter-precedent, not a decision. They go to the cross-dataset item (change 6).
- Your CC of 2026-09-21 asked for "taxi as group". SPLIT-3 (2026-10-12) is the newer decision and replaces it: no drift.
- The CC's signal reason is superseded by TP-2 (issue 1).
- No exceptions are recorded for pkdd, so none counts toward a third.

I measured the short-trip bins and the split options with 2 threads on the shipped frame and the raw trips table.

</details>
