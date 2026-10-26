# aeolus

**Outcome:** added as `aeolus_1m`. US domestic flights from 2023 on (1,785,316 rows), target `ARR_DEL15` (arrival 15
minutes or more late), three two-week test windows at the end of 2024, with the hourly weather at both airports as the
authors' release joined it. Review panel: full tier, 2026-10-20. The changes that needed no decision are made (the PROV-6 note on pnwflights14 is filed across datasets): the fit
is `approximate` (stale weather, no inbound aircraft, operated flights only), `known` and the notes give the weather's
real lag (3.5 to 11 hours, about a day for overnight arrivals), impossible temperatures and wind speeds become
missing, the sign-flipped coordinates of Guam and Pago Pago are repaired, the domain follows nyc_taxi_trip_duration,
and the notes correct the target wording, the probe numbers, the paper's split and the flight-number meaning. 

```text
Verdict: ship after changes, provided you confirm the weather call under PROV-13 (issue 8); if you follow
  ashrae/coad instead, retire for a rebuild as a new record (PROV-14).
Validity: SEL-1/SEL-2 hold; USE-1/USE-2 hold (airline or airport, before departure, which flights will be late);
  USE-5 holds (DOT ARR_DEL15); USE-8 triggered, fixed (fit "approximate"); LEAK-10 triggered (Guam origin weather
  about 10 h after departure; 1.94% of destination readings after departure, at most 4.4 h), kept under your CC of
  2026-10-12, mask recommended (issue 7, LEAK-6); LEAK-22 holds (the paper's cohort); LEAK-4 recorded (R2 0.01-0.02
  on the minutes); SPLIT-1/9/10/11/13/14 hold on measurement; SPLIT-19 departure from the paper's split stated
  (SPLIT-14, SPLIT-20); PROV-13 triggered (UTC hours joined to local clocks), in-place repair barred by LEAK-10
  (P4 over P5), a leak-free rebuild is a new dataset (PROV-14): issue 8.
Value: TP-1/TP-2 hold, `no_spread` kept as for amex_non_iid_1m (LightGBM over linear +0.036, paired SE 0.019, 50k train;
  every window scorable); all windows in early winter, noted.
Quality: CLEAN-11 impossible weather to missing; GUM/PPG coordinate signs repaired; 23:59, year-end gap, four block
  times and the flight-number meaning as notes.
Weighed: size +, source +, real task +, signal - (ROC AUC 0.61-0.63), weather timing -.
For the curator: issue 7, mask the readings after the departure (against your CC line); issue 8, a rule-scope
  call (does PROV-13 cover true but mis-timed values?); the domain field.
```

**Main points:** Make the weather read after the departure missing (issue 7); keep the release's mis-timed
weather under a narrowed PROV-13, or retire the dataset for a rebuild from BTS and Meteostat (issue 8; (b) makes
issue 7 moot); take the definition's domain.

**Record fields that disagree with the definition:**

- `domain`: record `business & marketing`, definition `industry & manufacturing`.

**Record judgment:** valid. A real delay-prediction task with a temporal split, from the authors' release (Xu et al.,
NeurIPS 2025) of the US DOT on-time flights (BTS) joined to Meteostat's hourly weather. The weather join is damaged
(issue 8); the rest of the release is as documented, with March 2024 missing.

**Issues for Lennart:**

7. **Make the weather read after the departure missing?** The prediction point is shortly before the scheduled
   departure. For 1.94% of the flights the release reads the destination weather after it (a median 0.7 hours, at
   most 4.4 hours later), and for the 106 Guam departures in the frame (14 per test window) the origin weather about
   10 hours after it. A value from after the prediction point is a leak, here a confirmed one: the claim audit timed
   every reading with one time zone per airport.
   - Effect: small. About 1% of each test window is affected, mostly eastbound transcontinental flights. Making the
     late destination readings missing in the test windows costs 0.0003-0.0004 ROC AUC per window (untuned LightGBM,
     1M training rows).
   - Implemented: kept, with a `Potential leak, kept on purpose:` note, under your CC of 2026-10-12 ("the weather as
     released"). The old reason ("re-joining it would be our own fix") is gone.
   - Alternative: set O_TEMP/O_PRCP/O_WSPD to missing for ORIGIN == GUM, and D_TEMP/D_PRCP/D_WSPD where the
     reading's hour falls after the scheduled departure. Cost: a table of one time zone per airport (310) in the
     definition.
   - Rule: LEAK-6 (Must), "a confirmed leak goes even when small"; LEAK-7 (Should), the smallest fix, here a mask.
     Precedent: follows santander (a confirmed small leak dropped at +0.003); kick and onlinenewspopularity kept
     suspected leaks, not confirmed ones. In the rebuttals the two sides swapped: the advocate accepted the mask and the critic accepted keeping the
     readings. The mediator chose the mask on LEAK-6's wording. Both sides agreed on the Guam part. Neither part was
     applied because both go against your CC of 2026-10-12.
     Moot if issue 8 goes to (b).
   - Recommendation: mask.
   - Decision: mask the readings after the departure, or keep them as released with the note.

8. **Keep the release's mis-timed weather, or rebuild?** The release looked up Meteostat's hourly weather (an open
   archive of station readings, time-stamped in UTC, the universal clock) by the flights' local scheduled clock
   times read as if they were UTC. So the origin weather is 3.5 to 11.4 hours old at departure, depending on the
   airport's time zone (median 5.2 hours), and for the 3.6% of flights that arrive after midnight the destination
   weather is the reading of the day before, a median 25 hours before departure. The values are real observations,
   attached to the wrong hour. Your CC of 2026-10-12 kept the weather as released; ashrae, SUPPORT2, coad and
   corporate_credit_rating were repaired or retired later under the same rule.
   - Effect: the only input that is not schedule is older than an operations desk would see (most at western
     and Pacific airports), so scores understate what weather adds; nothing is made easier than in practice. As released, all
     destination weather adds 0.008-0.016 ROC AUC per window. No leak beyond issue 7.
   - Implemented: the weather as released, with the real lags stated in `known`, `fit_reason` and two `Anomaly:`
     notes.
   - Alternative: retire `aeolus_1m` and rebuild as a new record from the BTS on-time table and Meteostat, joined in
     UTC at the last hour before the scheduled departure. It could add the tail number (the inbound aircraft, about
     40% of delay by BTS's cause data) and the cancelled flights. Cost: a new build from about 13 million flights and
     the station files; a new record and review.
   - Rule: PROV-13 (Must, P5): repair or rebuild a damaged release from the origin when the origin has the clean
     data. The advocate: restoring what the release intended (destination weather at the scheduled arrival) would
     put post-departure weather into every row (LEAK-10; P4, no leaks, outranks P5, provenance), and a leak-free re-join is a new dataset
     (PROV-14), so it is no condition on this one. The critic: PROV-13 says "repair or rebuild"; P4 bars one form of
     repair, not the rule, and the overnight pairing attributes values to the wrong time as in the ashrae cases.
     The mediator: the rule's text reaches this case, so keeping is a Must departure unless you narrow the rule;
     that is an amendment, yours to make. Precedent: departs from ashrae, SUPPORT2, coad and
     corporate_credit_rating; the distinguishing fact offered is that the values are true and earlier, not later.
   - Recommendation: keep (option a below), with the rebuild opened as a new record if you want the better task; what would settle it
     on evidence is the ROC AUC of a correctly timed weather join on the same splits against the 0.008-0.016 of the
     released one.
   - Decision: (a) keep, recorded as an amendment that narrows PROV-13 to damage that makes values false (aeolus as
     its case); or (b) treat it like coad: retire `aeolus_1m` for a rebuild as a new record.

**Review panel:** ship after changes, provided the curator confirms the weather call under PROV-13 (mediator).
Full tier. Claim audit: 69 claims, most hold; 5 refuted or partly refuted (the weather lag, the late-reading
wording, the probe bullet, the paper's threshold, the record's lag), all corrected in the notes; 1 untested (the
record's ROC AUC 0.64-0.67, an older set-up). Blind review: include with changes; its main concern, the uneven
sampling over time, is the v2 protocol (each test window whole, a uniform 1M train side). Debate: agreed on the split,
the `approximate` fit, the text fixes and the cleaning; disputed: PROV-13 (the mediator's issue 1, here issue 8); on the mask of the readings after the departure, each side took the other's position in the
rebuttals, and the mediator chose the mask (its change 2, here issue 7, not applied: it goes against the curator's CC). The frame was redrawn by the cleaning change
(1,785,316 rows); the panel's numbers are from the earlier draw.

<details><summary>Mediator</summary>

No experiment run: no fact is disputed. The only crossed point (the late destination weather) is a question of how a
rule reads, settled below by LEAK-6's text.

**Recommendation (judgment record)**

```text
Verdict: ship after changes, provided the curator confirms the weather call under PROV-13 (issue 1); if the curator
  follows ashrae/coad instead, retire for a rebuild as a new record (PROV-14).
Validity: SEL-1/SEL-2 hold; USE-1/USE-2 hold (airline or airport, before departure, which flights will be late);
  USE-5 holds (DOT ARR_DEL15); USE-8 triggered, fixed (fit "approximate": stale weather stands in for current
  weather, no inbound aircraft, operated flights only); LEAK-10 triggered (Guam origin weather ~10 h after departure;
  1.94% destination readings after departure, max 4.35 h), fixed by masking (LEAK-6 "a confirmed leak goes even when
  small", LEAK-7); LEAK-22 holds (paper's cohort); LEAK-4 open, procedure only (record the probe on ARR_DELAY);
  SPLIT-1/9/10/11/13/14 hold on measurement; SPLIT-19 departure from the paper's split kept, reason to be written
  (SPLIT-14, SPLIT-20); PROV-13 triggered (UTC hours joined to local clocks; overnight destinations a day early),
  in-place repair to the release's intended alignment barred by LEAK-10 (P4 over P5); the leak-free rebuild is a new
  dataset (PROV-14): curator issue 1. PROV-6 open on the sibling records' side.
Value: TP-1/TP-2, `no_spread` is a question to check on tuned results like every flagged dataset (keep; skill +0.219,
  >= 8,231 minority rows per window); all windows early winter, noted.
Quality: CLEAN-11 impossible weather to missing, GUM/PPG coordinate signs repaired; 23:59, year-end gap, 4 block
  times, flight-number meaning as notes.
Weighed: size +, source +, real task +, signal - (AUC 0.61-0.63), weather timing -.
For the curator: issue 1, a rule-scope call (does PROV-13 cover true but mis-timed values?).
```

**Changes to make now (no decision needed)**

1. `fit="approximate"`; fit_reason names the gaps: weather observed 3.5-11 h before departure (about a day early for
   overnight destinations), no inbound aircraft, operated flights only (USE-8; both sides agree; kick).
2. Mask O_TEMP/O_PRCP/O_WSPD for ORIGIN == GUM, and D_* where the reading's UTC hour falls after the scheduled
   departure, using one time zone per airport (as the claim audit built). Replace the `Potential leak, kept on
   purpose:` bullet by a note of the mask and its cost (0.0003-0.0004 AUC). Rule: LEAK-10 (Must), LEAK-6 (confirmed
   leak goes even when small; santander `has_*` dropped at +0.003), LEAK-7 (mask is the smallest fix). Settles the
   crossed concessions: the readings are confirmed post-departure, not suspected, so kick/onlinenewspopularity
   ("potential" leaks) are not the precedent. Moot if issue 1 goes to (b).
3. `known`: "weather observed 3.5 to 11 hours before departure, about a day early for overnight arrivals"; decision 2
   title the same range (EV-7, writing.md).
4. `Anomaly:` bullet: 460,592 overnight arrivals (3.6%) carry the destination reading of the departure date, a median
   25 h before departure; the origin lag varies by time zone (PROV-15 note; claim audit 6, 36).
5. Task-probe bullet: `no_spread` (LightGBM - linear +0.025, paired SE 0.015), linear 0.597, plus the 1M-train
   LightGBM 0.629-0.630; a new dated Assessment line in the record marking the 2026-10-07 "0.64-0.67" as the
   superseded all-years set-up, and the 2026-10-20 "direct fit" as stale (EV-7, EV-8).
6. Target wording: "the DOT definition (>= 15); the paper uses > 15 (0.68% of flights differ)" (USE-5, doc).
7. splits_comment: the paper splits 1-15 June 2024 chronologically 6:2:2 (Sec. 4.1); that gives one short window and
   no season (SPLIT-14, SPLIT-20), hence the departure (SPLIT-19 needs the reason); and "the windows measure
   late-November to December delays" (SPLIT-20 note; SPLIT-21 forbids re-choosing them).
8. `_clean`: *_WSPD > 120 km/h and *_TEMP < -50 C to missing (about 0.001% of rows; CLEAN-11); flip GUM longitude and
   PPG latitude to their true signs (repair, PROV-13/CLEAN-1). Notes for the 23:59 midnight, the 2024-12-31 late-hour
   weather gap, the four implausible block times.
9. OP_CARRIER_FL_NUM note: a service is carrier plus number (92.8% of numbers are shared across carriers). Keep the
   column as the paper types it (CLEAN-14); a combined category is optional, not required (CLEAN-3 is a Should and
   trees can interact the two).
10. LEAK-4: record the probe on the source label (ARR_DELAY), or cite the 2026-10-07 LightGBM R² 0.01-0.02 as that
    check in the notes.
11. `domain = "industry & manufacturing"` (and the record field), following nyc_taxi_trip_duration, delivery_eta_1m,
    maps_router_eta_1m; no fact sets aeolus apart (treat like cases alike). The curator may veto.
12. REVIEW.md: drop the licence issue (EV-4 Must: a one-line note, never an issue); keep the no-pinned-version point
    as a note (consistent with numerai_v5_2_1m).
13. `curation/records/pnwflights14.md`: a dated note that it is to be judged against aeolus for uniqueness, as the two
    `airlines` records already carry (PROV-6).

**Issues for the curator**

**1. P5, PROV-13 (Must): weather kept as released, while Meteostat (the origin) is public.**
- Problem: the release joined UTC hours to local clock times; origin readings are 3.5-11.4 h old (by time zone),
  overnight destinations about 25 h. Your CC of 2026-10-12 kept it; ashrae, SUPPORT2, coad and corporate_credit_rating
  were repaired or retired later on the same rule (drift, consistency case 3).
- Effect: the only non-schedule input is degraded (destination weather adds 0.008-0.016 AUC as released); no leak
  beyond what change 2 masks.
- Advocate: the values are true observations made before departure; the repair the release intended (destination
  weather at scheduled arrival) would put post-departure weather in every row (LEAK-10, P4 over P5); a leak-free
  re-join does not match the release, so PROV-14 makes it a new dataset, not a condition on this one.
- Critic: PROV-13 says "repair **or rebuild**"; P4 bars one form, not the rule; the overnight pairing and the
  zone-varying lag attribute values to the wrong time, which is the kind of falseness the ashrae/SUPPORT2 cases meant.
- Both agree: the definition's reason ("our own fix") is the wrong rule and goes; keeping needs your recorded answer.
- Mediator: the text of PROV-13 reaches this case (critic's reading is the closer one); the P4 conflict removes only
  the in-place repair. So keeping is a Must departure unless you narrow the rule. That is an amendment, yours to make.
- Decision: (a) keep, recorded as an amendment narrowing PROV-13 to damage that makes values false (aeolus as its
  case), with the rebuild optionally opened as a new record; or (b) treat like coad: retire `aeolus_1m` for a rebuild
  (BTS + Meteostat in UTC at the last hour before departure; could add tail number and cancellations) as a new record.
  What would settle it on evidence: the AUC of a correctly timed weather join on the same splits against the 0.008-0.016
  of the released one.

**Agreed facts**

- Temporal on FL_DATE, three 14-day windows (2024-11-20..12-31), one-day gap: 456-509 leaking flights without it,
  0-1 with it; a random split adds 0.08-0.09 AUC. 100% of test airports and 99.9% of flight numbers seen in train.
- 1,785,315 rows; train a uniform random 1M from 2023 on; each window keeps all its rows (258,551 / 256,013 / 269,272);
  the blind reviewer's "uneven sampling" is this v2 protocol. March 2024 missing at the source.
- Target ARR_DELAY >= 15 (DOT); paper uses > 15; authors' code abs(ARR_DELAY) > 15 (44% positive, wrong).
- Weather: station files match as UTC at 99.6-100%; origin lead 3.5-11.4 h (median 5.15); destination median 3.0 h;
  3.6% overnight destinations ~25 h early; 1.94% destination readings after departure (median 0.7 h, max 4.35 h,
  ~1% per test window); Guam origin ~10 h after departure (106 frame rows, 14 per window).
- Masking the late destination readings costs 0.0003-0.0004 AUC; all destination weather adds 0.008-0.016.
- Probes: LightGBM 0.609 (50k), 0.629-0.630 (1M), linear 0.597, single feature 0.584; `no_spread` (paired SE 0.015);
  skill +0.219; smallest test class 8,231 rows. No exact copies across the split; no feature alone above 0.585.
- No cancelled or diverted flights in the release; no inbound-aircraft field.
- Impossible values: O_TEMP -60.6 C (SRQ, May), wind 120-232 km/h without rain; GUM/PPG coordinate signs flipped.
- Licence: Kaggle Apache-2.0, paper CC BY-NC 4.0; no versioned Kaggle download; nine SHA-256 prefixes match.

**Consistency with precedent**

- PROV-13: departs from ashrae, SUPPORT2, coad, corporate_credit_rating; distinguishing fact offered (true values,
  earlier not later; the intended repair is a leak) but it is a reading of the rule's scope, so issue 1.
- USE-8 approximate: follows kick. zillow_prize stayed direct because its kept part was measured to change nothing;
  here the stale weather snapshot remains a stand-in even after the mask, so the fit is approximate either way.
- LEAK-6 masking: follows santander (confirmed small leak removed); kick and onlinenewspopularity kept suspected,
  not confirmed, leaks.
- `no_spread` keep: follows acquire_valued_shoppers_challenge and amex_non_iid_1m; tension "right split against the
  score".
- Split: aeolus is itself the case of SPLIT-20/21; the gap follows brazilian_ecommerce, sf_permit_time.
- CLEAN-11: follows heart_disease_va_long_beach, thyroid_discordant, sdss_17.
- Domain: follows nyc_taxi_trip_duration (change 11).
- Licence: EV-4 over the working-copy habit of raising it as an issue (numerai_v5_2_1m); a note.

</details>

<details><summary>Claim audit</summary>

Adversarial test of the 69 claims of the definition and the record plus the implied ones. Time zones from
timezonefinder 9.0.0 on the release's airport coordinates, GUM/PPG/SPN set by hand; Meteostat bulk station files 72530
ORD, 91182 HNL, 72278 PHX downloaded on 2026-10-20.

Model set-up for the leak and score tests (`model.py`): the built container through `dataset_io.load(built=True)`
(origin reported "rebuilt"), the three shipped temporal splits, LightGBM 400 trees, lr 0.05, 127 leaves, the full 1M
train side unless noted (EV-8: these are untuned single runs, not leaderboard numbers).

**Table**

| # | Claim | Source | Test | Result | Evidence | Rule |
|---|---|---|---|---|---|---|
| 1-4 | ARR_DEL15 >= 15 min, DOT definition, completed flights 2023-24 | task_summary | `_clean` code; raw counts | holds | `late = ARR_DELAY >= 15`; BTS ARR_DEL15 is ARR_DELAY_NEW >= 15 | USE-5 |
| 5 | about one in five late | task_summary | raw late share 2023+ | holds | 20.67% (2023 20.5%, 2024 20.8%) | - |
| 6 | weather at both airports "a few hours before departure" | task_summary.known | real UTC offsets per airport; lead = true departure UTC minus weather hour | **refuted (tail)** | origin lead 3.5-11.4 h (median 5.15); destination lead median 3.0 h but 3.5% of flights (the 460,592 overnight arrivals) have destination weather a median 25 h before departure (max 33.7 h): the release dates CRS_ARR_TIME on FL_DATE, and the overnight destination reading equals the departure-date reading at that hour at 100% of 272,624 matched flights against 9.6% for the next date | PROV-13, USE-3 (doc) |
| 7-8 | two-week windows at end of 2024; random 1M from 2023 on | task_summary | the split facts | holds | windows 12-18..31, 12-04..17, 11-20..12-03; train 1,000,000, 45-47% from 2024 | SPLIT-1 |
| 9-10 | history from 2023; one window in holiday peak | task_summary | raw weekly late shares | holds | weeks of 12-16 and 12-23: 23.2%, 27.8%; the earlier weeks 16.5-18.2% | SPLIT-4 |
| 11-12 | fit direct; "destination weather of 2%... read up to about an hour later" | fit_reason | lateness distribution of late readings | **partly refuted** | 1.94% holds; median 0.7 h holds; but 31.5% of the late readings are more than 1 h late, 90th pct 1.67 h, max 4.35 h; the Guam origin weather (10 h after departure) is not named in fit_reason | USE-8/USE-9 (doc), LEAK-10 |
| 13, 45 | no cancelled or diverted flights | fit_reason, notes | null ARR_DELAY / ARR_TIME, FLIGHTS != 1 | holds | 0 nulls in all 54.7M rows, FLIGHTS always 1 | USE-5 |
| 14, 26, 61 | 54,674,003 flights; 12,930,302 from 2023 | version_comment | raw count | holds | exactly 54,674,003 and 12,930,302 | - |
| 15, 52 | each window keeps all its rows (258,551 / 256,013 / 269,272); 1M train | version_comment, splits_comment | built container | holds | same sizes in model.py | - |
| 16 | metadata | dataset.py | read | holds (not a fact test) | - | - |
| 17 | Apache-2.0 on Kaggle, CC BY-NC 4.0 in paper A.3 | license | Kaggle API metadata; arXiv HTML | holds | `"licenses": [{"name": "apache-2.0"}]`; paper: "Our code and dataset follow the CC BY-NC 4.0 International License." | EV-4 (note only) |
| 19-21 | 15.2 GB, files dated 2025-10-17, SHA-256 prefixes | download_description | file listing; checklist re-hash | holds | CSVs dated Oct 17 2025; prefixes re-hashed by checklist run | - |
| 22 | bibtex | dataset.py | arXiv | holds | authors and title match | PROV-16 |
| 23 | DOT 15-minute rule | constant | BTS definition | holds | - | - |
| 24, 42 | block time < 15 min are errors; shortest real hop WRG-PSG 18 min; 3 rows | constant, notes | raw block times per route | holds, but incomplete | 3 rows < 15 in 2023+ (FLL-TPA 1, JFK-PWM -5, IND-ORD 6); WRG-PSG 18 min in 2016 (20 min from 2023); 4 more impossible times stay: PSP-SFO 17 (route median 99), ORF-LGA 24 (90), CLT-BOS 55 (133), MDT-ATL 60 (124) | CLEAN (P7, 4 of 12.9M rows) |
| 25, 35 | dropped columns are post-departure, FLIGHTS = 1, one index per airport | constants | raw | holds | ORIGIN_INDEX: 1 value per code; leak probes: no feature alone > 0.585 | LEAK-1 |
| 27, 43 | paper Table 9 features; flight number categorical | notes | arXiv HTML Table 9 | holds | OP_CARRIER_FL_NUM in the 8 categorical features; "Unique flight number assigned by the carrier" | - |
| 28-29 | 2020 9.7% late, others 17-21% | notes | raw per-year | holds | 2020 9.73%; others 17.1-21.0% | - |
| 30 | authors' benchmarks use 2024 alone (Sec. 4.1) | notes | arXiv HTML | holds, imprecise | Sec. 4.1: "287,845 flight samples between June 1 and June 15, 2024"; Sec. 4.2 "the full-year 2024 data" | PROV-16 |
| 31 | 2018 duplicate falls before history | notes | duplicate keys 2023+ | holds | 0 duplicate (date, carrier, number, origin, CRS_DEP) keys from 2023 | LEAK-16 |
| 32 | ARR_DEL15 is "the paper's classification task" | notes, decision 3 | paper App. B.2; raw counts | **refuted (minor)** | paper: "more than 15 minutes is considered a delay" (strict >); we use >= 15; 0.68% of 2023+ flights have ARR_DELAY exactly 15 | USE-5 (doc) |
| 33, 57, 63 | top 1% hold 66-68% (2023-24), 56-71% all years | notes, record | raw variance shares | holds | 2023 0.678, 2024 0.655; all years 0.562-0.714 | - |
| 34 | authors' code labels abs(ARR_DELAY) > 15 | notes | GitHub Flnny/Delay-data `exp/Tab_exp/Deep_Model_Classifier.py` line 18 | holds | `df['ARR_DELAY'].apply(lambda x: 1 if abs(x) > 15.0 else 0)`; that label is positive for 44.0% of flights against 20.7% | - |
| 36 | CRS times are local clock times dated on the flight date | notes | raw | holds, consequence unstated | CRS_DEP and CRS_ARR date always equal FL_DATE; 460,592 (3.6%) arrive clock-before-departure; see claim 6 | PROV-13 |
| 37, 55, 56 | weather joined by UTC hour to local clock; station files match as UTC at 99.6-100%, 2-8% at true offsets | notes, decision 2 | re-downloaded Meteostat station files, 2024 origin temperature per (airport, rounded CRS_DEP hour) | holds | ORD 99.94% as-UTC vs 6.8% true; HNL 100% vs 3.9%; PHX 99.97% vs 2.3% | EV-2 |
| 38, 62 | origin weather median 5.2 h before, destination 3.0 h | notes, record | tz_lead.py | holds (median) | 5.15 h and 3.0 h; tail see claim 6 | - |
| 39 | 1.94% of destination readings after departure, median 0.7 h; 0.9-1.0% per test window | notes | tz_lead.py, model.py | holds (rounding) | 1.94% (250,799 flights), median 0.7 h; windows 1.03%, 1.05%, 0.93% (1.05% rounds to 1.1%) | LEAK-10 |
| 40 | 686 Guam departures get weather after departure | notes | raw count | holds | 686 in 2023+; 106 in the frame, 14 per test window. Also: GUM is stored at longitude -144.80 (true +144.80) and PPG at latitude +14.33 (true -14.33): sign-flipped coordinates in the release | PROV-13, CLEAN (P7) |
| 41 | destination weather adds 0.006-0.024 AUC per window | notes | LightGBM 1M train, with vs without D_TEMP/D_PRCP/D_WSPD | holds | +0.010, +0.008, +0.016. The late part: masking the dest weather of the late rows at test costs 0.0003-0.0004 AUC; on the late rows the dest weather adds 0.020-0.041 against 0.008-0.016 on the other rows | LEAK-10, LEAK-30 |
| 44 | probes "no flags; LightGBM 0.609, linear 0.594, single 0.584" | notes | the task probes; model.py | **refuted** | today: flag `no_spread` (TP-3), linear 0.597; LightGBM 0.609 and single 0.584 hold. With the shipped 1M train LightGBM reaches 0.6295 / 0.6301 / 0.6292 (50k: 0.592 / 0.609 / 0.590) | EV-7, EV-8 |
| 46 | March 2024 missing; test windows unaffected | notes | raw month counts | holds | 2024 months 1,2,4-12 | PROV-13 |
| 47-53 | split design, 1-day gap, late shares 25.8/16.7/17.3, 20.8% in 2024 | splits_comment | split facts; raw | holds | train ends 12-16, 12-02, 11-18; shares match | SPLIT-1, SPLIT-9 |
| 54 | weather keyed by scheduled times | decision 1 | overnight.py (same-key match) | holds | destination readings match the release's reading at the scheduled (airport, hour) at 100% | - |
| 58 | 0 errors, 0 warnings | check | the dataset check | holds | "0 error(s), 0 warning(s)" | - |
| 63 | record: LightGBM ROC AUC 0.64-0.67 for the indicator | record 2026-10-07 | model.py | **untested / not reproduced** | the shipped splits give 0.629-0.630 with 1M training; the record's set-up is not named | EV-8 |
| 64 | weather "4-10 hours early" | record 2026-10-12 | tz_lead.py | partly refuted | origin 3.5-11.4 h; destination 25 h early for overnight flights | doc |
| 59-60, 65-69 | front matter, CC lines, priority | record | read | not facts to test | - | - |

**Implied claims**

| Claim | Test | Result | Evidence | Rule |
|---|---|---|---|---|
| Every feature is known at the prediction point | real time zones for the weather; leak probes | holds except the stated late readings | 1.94% destination late (median 0.7 h, max 4.35 h), Guam origin 10 h late; together worth at most 0.0004 AUC; actual-time columns all dropped | LEAK-10, LEAK-30 (weak, kept with note) |
| The split is the one the use case needs | split facts, gap | holds | temporal on FL_DATE, 1-day gap covers overnight landings; 100% of test airports and 99.9% of flight numbers seen in train (the deployed model sees known services) | SPLIT-1, SPLIT-13 |
| The target is the real-world target | DOT definition | holds | ARR_DEL15 = BTS definition; cancelled/diverted flights absent (an operating-flight task, stated) | USE-5 |
| No row is a copy across the split | leak probes, split facts | holds | 0.0% exact feature copies; 0.002-0.003% without FL_DATE; 0 duplicate keys | LEAK-16 |
| The weather columns describe the weather of each airport near the flight | overnight.py, coordinates | **refuted for 3.6% (destination) and 2 airports (coordinates)** | overnight destination weather is a day-early reading; GUM and PPG coordinates sign-flipped | PROV-13 (damage in the release; not a leak) |
| Flight number as one categorical names one service | gain shares | holds with caveat | OP_CARRIER_FL_NUM takes 46% of LightGBM gain; the same number across carriers is one category (the model must interact it with OP_CARRIER) | CLEAN (P7, weigh) |

**Refuted and untested, ranked (validity first, Must first)**

1. **Claim 6 / implied weather claim (P5, PROV-13; doc under USE-3).** The overnight 3.6% of flights carry destination
   weather from about a day before departure (median 25 h, max 33.7 h), because the release dates the scheduled
   arrival on FL_DATE. Not a leak (it is earlier, not later), so P4 is untouched; it is damage in the release, of the
   same kind as the UTC/local join already noted. Changes: the `known` sentence and the decision 2 title ("3.5 to 10
   hours earlier") are wrong for these rows. Mildest remedy: an `Anomaly:` bullet with the number (keep as released,
   as the curator decided for the UTC join); repairing from Meteostat would be the PROV-13 rebuild already declined.
2. **Claim 12 (P4, LEAK-10, documentation).** "read up to about an hour later": 31.5% of the late readings are more
   than an hour late (max 4.35 h), and fit_reason omits the Guam origin weather (10 h after departure, 14 test rows
   per window). Effect is negligible (masking the late part costs 0.0003-0.0004 AUC), so the keep stands
   (LEAK-30 weak). Remedy: reword to "a median 0.7 hours and at most about 4 hours later" and name Guam.
3. **Claim 44 (procedure, EV-7/EV-8).** "no flags" and "linear 0.594" are refuted by today's probe (`no_spread`,
   linear 0.597). Also: the probe numbers are 50k-row numbers; the shipped 1M train gives LightGBM 0.629-0.630, and
   the record's 0.64-0.67 (claim 63) is not reproduced on the shipped splits. Remedy: update the bullet to the
   current probe, state the 1M-train figure, and mark the record's number as from another set-up.
4. **Claim 32 (P3, USE-5, documentation).** The paper's task is "more than 15 minutes" (strict), not >= 15; 0.68% of
   flights differ. The target choice is fine (DOT); only "the paper's classification task" is inexact. Remedy: say
   "the DOT definition; the paper uses > 15".
5. **Coordinates of GUM and PPG sign-flipped (P5/P7, CLEAN).** Longitude -144.8 for Guam, latitude +14.33 for Pago
   Pago; affects a few hundred rows. Remedy: an `Anomaly:` note, or fix the two airports' signs (cheap, safe).
6. **Claim 24/42 (P7).** The < 15 min rule leaves 4 impossible block times (17, 24, 55, 60 min on routes with medians
   90-133). Negligible; a note at most.
7. **Untested:** claim 63 set-up (not named in the record); the licence for redistribution (EV-4, note only); the
   weekly-window holiday share 25.1-26.5% in CC 2026-10-12 (not recomputed with the exact 7-day windows).

</details>

<details><summary>Column audit</summary>

Prediction point (curation_comments, first bullet; task_summary): shortly before the scheduled departure, an airline or
airport estimates which coming flights will arrive 15+ minutes late, from the schedule and the weather. Frame rebuilt
from the definition through `dataset_io.from_definition` (1,785,315 rows, 18 features + target, sorted by FL_DATE,
3 splits: train ends 2024-11-18 / 12-02 / 12-16, test 11-20..12-03 / 12-04..17 / 12-18..31). Raw checks on the kept
history (12,930,302 rows of `aeolus_flights.parquet` from 2023 on). Units of the weather follow Meteostat's hourly schema (temp °C, prcp mm in
the hour, wspd km/h, mean); the paper's Table 9 was not re-read in this run.

**Column table**

| Column | Meaning | Known at prediction? | Dtype and cleaning | Verdict | Rule |
|---|---|---|---|---|---|
| FL_DATE | Scheduled flight date (local) | yes | datetime64, time-only parts all 00:00; MONTH/DAY_OF_MONTH/DAY_OF_WEEK not read (pipeline derives them) | fine | CLEAN-12, CLEAN-14 |
| OP_CARRIER | Operating carrier code (15) | yes | category, sorted categories | fine | CLEAN-14 |
| OP_CARRIER_FL_NUM | Flight number of the operating carrier | yes | category with 6,715 int levels (float 4814.0 cast to int). 92.8% of the numbers are used by more than one carrier; a carrier+number pair flies a median of 4 origins. The note "a flight number names a recurring service of its carrier" holds only jointly with OP_CARRIER | question for the curator | CLEAN-3, CLEAN-14 |
| ORIGIN | Origin airport IATA code (309) | yes | category | fine | CLEAN-14 |
| DEST | Destination airport IATA code (310) | yes | category | fine | CLEAN-14 |
| CRS_ELAPSED_TIME | Scheduled block time, minutes | yes | float64; < 15 min to missing (3 rows of the kept history: 1, -5 and one more; none in the frame); frame range 20-707, plausible (WRG-PSG 24 min) | fine | CLEAN-11 |
| CRS_DEP_TIME_MIN | Scheduled local departure, minutes after midnight | yes | int64 0-1439 built from CRS_DEP_TIME. No 00:00 in 12.9M rows, 23:59 holds 22,782 (in the frame 3,187 against 181 at 23:58): BTS's "2400" apparently stored as 23:59 by the release | fine (note only) | CLEAN-10 |
| CRS_ARR_TIME_MIN | Scheduled local arrival, minutes after midnight | yes | int64; same 23:59 spike (8,814 against 2,622 at 23:58; 00:00 occurs once in 12.9M) | fine (note only) | CLEAN-10 |
| O_TEMP | Origin air temperature, °C, Meteostat hour = local scheduled departure clock read as UTC | yes (a median 5.2 h before departure) | float64; 211 missing (GUM 106, PPG 38: no station; plus year-end rows, below). Impossible: -60.6 °C at SRQ (Sarasota) on 2024-05-14, 7 rows in the history, 1 in the frame | cleaning problem | CLEAN-11 |
| O_PRCP | Origin precipitation in the hour, mm | yes | float64, 0-73.2; 269 history rows > 50 mm/h (Florida/Gulf storms: plausible, kept) | fine | CLEAN-11 |
| O_WSPD | Origin mean wind speed, km/h | yes | float64; 39 history rows > 120 km/h, frame max 174.2 (ACY 2024-02-09 at 161 and 174 km/h, 0 mm rain; ACY has 22 such rows). WYS reads 0 in 74% of rows (calm or a stuck sensor; kept) | cleaning problem | CLEAN-11 |
| D_TEMP | Destination temperature, °C, hour = local scheduled arrival clock read as UTC | mostly (a median 3.0 h before departure); about 1% of test rows read after the scheduled departure (re-measured roughly: 1.0%, 7,844 rows over the three windows, LAX/SFO to JFK/BOS/EWR) | float64; 472 missing; FAI -41 °C plausible | leak, weak, kept on purpose with a note | LEAK-10, LEAK-6, LEAK-7 |
| D_PRCP | Destination precipitation, mm | as D_TEMP | float64, 0-97.7 | leak (as D_TEMP) | LEAK-10 |
| D_WSPD | Destination mean wind speed, km/h | as D_TEMP | float64; 35 history rows > 120 km/h, frame max 232.0 (ATW 2023-02-16), 207 (HOU), ACY 18 rows | leak (as D_TEMP) and cleaning problem | LEAK-10, CLEAN-11 |
| O_LATITUDE, O_LONGITUDE | Origin airport coordinates | yes | float64, one value per airport (0 airports with two) | fine (spatial attribute of ORIGIN, not an exact copy) | CLEAN-5 |
| D_LATITUDE, D_LONGITUDE | Destination airport coordinates | yes | as above | fine | CLEAN-5 |
| ARR_DEL15 (target) | ARR_DELAY >= 15 (US DOT) | outcome | category No/Yes; ARR_DELAY has 0 missing in the kept history (so no NaN silently becomes "No"); ARR_DELAY equals ARR_TIME - CRS_ARR_TIME (mod 1440) in 99.9995% of rows | fine | CLEAN-15, USE-5 |

Dropped columns checked: DEP_TIME, DEP_DELAY, TAXI_OUT, WHEELS_OFF/ON, TAXI_IN, ACTUAL_ELAPSED_TIME, AIR_TIME, ARR_TIME,
ARR_DELAY are all post-departure (LEAK-10, correctly gone); FLIGHTS constant (CLEAN-5); ORIGIN_INDEX/DEST_INDEX are
storage codes of ORIGIN/DEST (CLEAN-3). No id encodes the label. No column is computed over all rows; category sets
from the whole table are CLEAN-8 ordinary cleaning.

Missingness: not caused by the outcome. Besides GUM/PPG, the weather is missing for every 2024-12-31 flight scheduled
at 23:30 or later (302 of 302 destination lookups; also 2023-12-31): the release rounds to the nearest hour, which
falls in the next year, outside its yearly weather file. Late share of those rows 22%, the window's average. O-missing
rows are 7% late (GUM/PPG), 211 rows; the missing indicator alone scores AUC 0.5 (leak probes).

**Problems, ranked by principles.md**

1. **P3, USE-8 (Must): the fit says `direct` but the definition keeps a potential leak on purpose.** USE-8 lists "a
   potential leak kept on purpose" under approximate (case: kick), and the weather is also a stand-in (read 3-10 h
   early because of the UTC/local join, not what the actor would see "shortly before departure"). The fit_reason itself
   names the late destination weather. Mildest remedy: `fit="approximate"`, fit_reason unchanged; or the curator
   records a USE-9 argument for direct.
2. **P4, LEAK-10 (weak, kept on purpose): D_TEMP / D_PRCP / D_WSPD read after the scheduled departure for about 1% of
   test rows.** Re-measured with rough longitude time zones: 1.0% of test rows (claim: 0.9-1.0%), concentrated on
   eastbound transcontinental flights; late share 21.8% against 19.9%. Strength: weak (all destination weather adds
   0.006-0.024 AUC, an upper bound). Documented as a `Potential leak, kept on purpose:` bullet, which LEAK-6 allows.
   Mildest stronger remedy (LEAK-7), for the curator: mask the three D columns where their hour falls after the
   scheduled departure (needs one time zone per airport), milder than a re-join from Meteostat.
3. **P7, CLEAN-11 (Should): impossible weather values.** O_TEMP -60.6 °C at Sarasota in May (7 history rows, 1 in the
   frame); wind speeds above 120 km/h with no rain at ACY, HOU, BTV, ATW, FSM (39 origin, 35 destination rows in the
   history; up to 232 km/h in the frame). Remedy: set to missing, e.g. `*_WSPD > 120` and `*_TEMP < -50` (no US airport
   outside Alaska reaches it; Alaska's minimum in the frame is -41). About 0.001% of rows; no effect on scores, only on
   the expert state.
4. **P7, CLEAN-3 / CLEAN-14 (question): OP_CARRIER_FL_NUM.** As shipped it is a number shared across carriers (92.8% of
   the numbers), so the stated meaning ("a recurring service of its carrier") is only recovered jointly with
   OP_CARRIER; a carrier+number pair is not a fixed route either (median 4 origins). Options: keep (trees can interact;
   hidden-groups probe s_id 0.089) and correct the note, or replace it by one `OP_CARRIER`+number category (CLEAN-3
   "process an identifier into its meaning"). Not a leak: known services under a temporal split are history
   (LEAK-34, USE-10).
5. **Notes only (no change needed):** (a) scheduled midnight stored as 23:59 in the release (CRS_*_TIME_MIN = 1439,
   one minute off); (b) the year-end weather gap (nearest-hour rounding into the next year), which puts about 300
   missing destination readings into the newest test window; (c) the cohort without cancelled and diverted flights
   follows the DOT on-time statistics, which leave ARR_DEL15 empty for them (LEAK-22), already stated.

Not found: post-outcome fields among the kept columns, outcome-caused missingness, windows ending at the outcome,
ids encoding the label, all-row statistics, untyped object columns.

</details>

<details><summary>Split audit</summary>

Definition `datasets/_dev/tabarena-v0pt2/aeolus_1m/dataset.py`; frame and splits rebuilt from the definition through
`dataset_io.from_definition` (origin `definition`, 1,785,315 rows, 3 temporal splits).

**Verdict: right with notes**

Validity: USE-10 holds (known entities: recurring services); SPLIT-1/2/3 hold (temporal on FL_DATE); SPLIT-9 and
SPLIT-10 hold (1-day gap covers the label delay, measured); SPLIT-11 holds (expanding train, subsampled to 1M at
random); SPLIT-13 holds (recurring entities are part of the task); SPLIT-14 holds (3 windows, train 1M against 256-269k
test); SPLIT-18 holds (two-week windows); SPLIT-20/21 applied as the curator decided on 2026-10-12.
Notes: SPLIT-19/SPLIT-5 departure from the paper's own split is not written down correctly (issue 1); all three
windows fall in one season, late Nov to Dec (issue 2, by design); March 2024 missing in the training history (issue 3).

**Regime**

* Use case: an airline or airport, shortly before departure, flags the coming flights that will arrive late. The model
  predicts for known airports, carriers and recurring flight numbers (USE-10, known entity); the data is a stream over
  time with a refit cadence. Temporal is the right regime, grouped would test a new airport or service, which is not
  the use case.
* Probes agree: ORIGIN 100% / DEST 100% / OP_CARRIER_FL_NUM 99.9% of test rows seen in train (hidden-groups probe),
  carrier + flight number 98.8% (split facts). Reading 2 of `test_rows_seen` (evidence.md): part of the task, SPLIT-13.
* Alternative split, quick LightGBM (300k train rows, 400 trees, untuned, same features plus day of year / week):

  | split | temporal (shipped) | IID over the same rows | half of the window's rows in train |
  |---|---|---|---|
  | 0 (12-18..12-31) | 0.630 | 0.717 | 0.769 |
  | 1 (12-04..12-17) | 0.627 | 0.706 | 0.713 |
  | 2 (11-20..12-03) | 0.632 | 0.708 | 0.734 |

  A random split would add 0.08-0.09 ROC AUC: delays cluster by day (shared weather and traffic events), and a random
  hold-out lets the model read the day's delay level from its neighbours on the same day. The temporal split with a
  gap removes that; the choice is clearly right (SPLIT-1).

**Temporal checks**

* Time column: FL_DATE is the scheduled (local) flight date, the day of the prediction point. Its meaning fits.
* Windows (measured): split 0 test 2024-12-18..12-31 (258,551 rows, 25.78% late), train 2023-01-01..2024-12-16;
  split 1 test 12-04..12-17 (256,013, 16.67%), train to 12-02; split 2 test 11-20..12-03 (269,272, 17.34%), train to
  11-18. Exactly one empty gap day before each window; no index overlap. Numbers match `splits_comment` and claims
  48-53.
* Label delay against the gap (raw parquet, actual arrival = scheduled arrival + ARR_DELAY, overnight schedules
  rolled to the next day): in the kept history (12.1-12.7M flights before each window), flights dated before the
  window whose arrival falls at or after the window start: gap 0 would leave 456 / 509 / 476 (3.8-4.1e-5, 26-33% late
  among them); the shipped gap 1 leaves 0 / 1 / 1 (one flight with a delay over 24 h, about 0.08 expected rows in a
  1M sample). SPLIT-9 holds; SPLIT-10's gap is the right size, not longer than needed. (The actor's own operations data
  has the outcome at landing; the public BTS release lags by about two months, which does not apply to an airline.)
* Train side: a random 1M of all flights from 2023-01-01 to the gap; 23 months present (March 2024 missing), 38-50k
  rows per month, 45-47% from 2024; train late share 20.6-20.7%. SPLIT-11 (expanding) holds; the subsample is
  uniform over the history, so the newest two weeks are about 3.5% of it.
* Training history: from 2023 on, two full seasonal cycles including the previous holidays, after the COVID-19 break
  (SPLIT-20, curator's CC 2026-10-12). Not re-decided here (SPLIT-21).
* Season: monthly late shares in the history run from 13.2% (Oct 2024) to 29.8% (Jul 2024). The three windows cover
  late November to the end of December; the holiday window's daily late share runs from 9.0% (Dec 25) to 40.8%
  (Dec 29), window 1 9.8-24.5%, window 2 8.4-25.3% (Thanksgiving, Nov 28, is in window 2 at 8.4%: a travel peak, not a
  delay peak). One window of three in the delay peak, as SPLIT-20 asks.

**Problems, ranked (principles.md: P4 first, then strength, then effect)**

1. **P4, SPLIT-19 / SPLIT-5 (Should): the paper's own split is not stated, and the departure from it is not argued.**
   The curation bullet says "The authors' benchmarks use 2024 alone (Sec. 4.1)". The paper (arXiv 2510.26616, Sec.
   4.1) uses 287,845 flights of 2024-06-01 to 06-15 with a chronological 6:2:2 split: one test stretch of about three
   days. Following it would break SPLIT-14 (Must, at least 3 windows) and SPLIT-18/20 (a two-week sample has no
   season), so the departure is right; it is only undocumented, and claim 30 is imprecise. Remedy (mildest): one
   sentence in `splits_comment` or the History bullet: "The authors split 1-15 June 2024 chronologically 6:2:2
   (Sec. 4.1); a three-day test from two weeks of data gives one window and no season (SPLIT-14, SPLIT-20)." No
   re-split.
2. **P4, SPLIT-20 (Should) with a P6 consequence: all test windows lie in one season.** The windows roll back from the
   newest data (SPLIT-15) and so cover only late November-December; summer thunderstorm delays (Jun-Jul, 25-30% late)
   are never tested. Delays cluster by day, so each window is in effect 14 day-level draws (daily late shares 8-41%),
   which is why the task probe's paired SE is 0.015 and `no_spread` was raised. This is the curator's documented
   choice of 2026-10-12, and SPLIT-21 forbids re-choosing windows from test-window scores. Remedy: none required; a
   note in `splits_comment` that the score measures early-winter delays only. If the curator wants more season
   coverage, more or longer windows (e.g. 4-6 two-week windows back to September) are the option, decided on the use
   case, not on scores.
3. **P5/P4 note: March 2024 is missing from the training history** of every split (documented anomaly; no test window
   affected). The model learns March only from 2023. Remedy: none (kept as released; noted already).

Not a split problem, for the leak auditor: the destination weather read after the scheduled departure (1.94% of rows)
is a feature-timing question (LEAK-10), unaffected by the split.

**Checked and holding**

* Not grouped, not IID; no similarity cluster or hash in use. Near-copy clusters (4.4% of test rows near a train row)
  are recurring services, part of a known-entity task.
* Exact feature copies across the split 0.0% (2-3e-5 without FL_DATE).
* Each window has 8,231+ rows of the smaller class (task probe): every window scorable.

</details>

<details><summary>Domain practitioner</summary>

Role I took: a delay analyst in an airline's operations control centre (OCC). A few hours before a bank of
departures, I rank the day's flights by the risk of arriving 15+ minutes late, to decide where to put spare aircraft,
standby crews and connection protection. A second actor is checked at the end: a passenger app or a delay-insurance
pricer.

**Fit: approximate (the definition says direct)**

One sentence: the rows, the target and the rolling two-week split mirror the OCC's decision, but the definition keeps
a potential leak on purpose (2% of destination weather read after departure) and the weather snapshot is a mis-timed
stand-in (UTC hours joined to local clock times, so 3.5-10 h stale by time zone), which USE-8 lists as approximate
(the case kick: "a potential leak kept on purpose").

USE-9 does not rescue "direct": no other well-defined use case has exactly "schedule + weather from a time-zone-dependent
3.5-10 h earlier, without the inbound aircraft". A day-ahead planning task would not have observed weather from the
day itself; a day-of task would have far fresher and richer inputs. Rephrasing to fit would hit the weighed factor
"a use case rephrased only to excuse a gap".

**1. Inputs at the prediction point (USE-3, USE-6)**

Inputs I have and the dataset gives me: date, carrier, flight number, origin, destination, scheduled times and block
time, airport coordinates (constants per airport), observed weather at both airports. All are known before departure
except the late destination weather of 1.94% of flights (claim 39) and the Guam departures (claim 40; 106 in the shipped
frame, checklist). Nothing recorded after departure remains (SKIPPED_COLUMNS, drops; leak probes show no feature
above 0.585 alone).

Inputs I would always have and the dataset lacks, ranked by how much they drive the outcome:

1. The inbound aircraft (tail number and its current leg's status/ETA). BTS attributes about 40% of delay to the
   late-arriving aircraft (2010-2019 and again largest in 2023). The BTS on-time table carries the tail number; the
   Aeolus tabular release does not (paper Table 9), and its flight chains group by carrier + flight number + date, not
   by aircraft. This is the single biggest gap between the dataset and the real decision.
2. Today's operation so far: departure delays already realised at the origin this morning, FAA ground delay programs
   and ground stops, airport arrival rates. A model refit every two weeks would be fed these daily.
3. Weather forecasts (TAF/convective outlooks) for the destination at the scheduled arrival time, rather than an
   observation from 3 h before departure. What I act on is the weather when the flight lands.
4. Load factor, crew connections, the aircraft type: secondary.

Inputs given that I would have in a different form: the weather. Because the release read Meteostat's UTC hours as
local clock time, the staleness is not "a few hours" uniformly but an airport-dependent offset (East coast about 4-5 h,
Hawaii about 10 h; decision 2). A real system reads the latest METAR. The model can partly learn this per-airport
offset since ORIGIN/DEST are features, but the information is systematically degraded at western and Pacific airports.

None of the missing inputs is a leak; they make the task "delay risk from schedule and stale weather only", a
restricted version of the OCC task. USE-6 frames dropping a known input as changing the task; here the source, not
the curation, dropped it, so it is a gap to name, not a fix to make (repair would need the BTS table re-joined: PROV-13).

**2. Target (USE-5)**

`ARR_DEL15` (arrival 15+ min late, DOT definition) is what airlines are measured on (A14 on-time performance) and the
paper's task. The curation corrected the authors' `abs(ARR_DELAY) > 15` labelling, which a practitioner would also
reject. In operations I act on a probability (rank flights, set thresholds per resource), so a binary target scored by
ROC AUC fits the ranking use; calibration (log loss) matters as much for allocating spares, and ROC AUC ignores it.
For crew legality and connections I would want minutes (or P(delay > 60 min)), but the decision 3 argument against an
RMSE on minutes is sound. Target: what I act on, not a proxy.

Population problem: cancelled and diverted flights are absent (claim 45). At the prediction point I do not know which
flights will be cancelled, and cancellations cluster on the same storm and ATC days that drive delays. The test set is
thus filtered on a future outcome (the flight operated). The BTS cancellation rate is on the order of 1-2% a year but
much higher on bad days, so the effect concentrates in exactly the rows that matter most. The definition names it in
fit_reason; a practitioner would want cancelled = "late" (or a separate class) to score the decision as faced.

**3. Rows and test data (USE-10, SPLIT)**

One row = one operated flight = one decision of mine: matches. The entity is known (recurring flight numbers, 99.9% of
test flight numbers seen; all airports seen): correct per USE-10, temporal split. The test windows (the next two weeks
after a refit, 1-day gap for overnight arrivals) are what I would face, including one holiday-peak window (25.8% late),
which is the hardest and most valuable period. The random 1M sample of 2023-on flights is a reasonable stand-in for
"train on recent history". March 2024 missing is a minor hole in training. Three windows give a paired SE of 0.015
between families: few windows for a stable ranking, but each window is large.

**4. Would I use it?**

Not as an OCC tool: ROC AUC 0.61, and 77% of LightGBM's skill comes from the scheduled arrival time alone
(single feature 0.584), i.e. "late-day flights are later", which every dispatcher already knows. Without the inbound
aircraft I would distrust any ranking within the day. I would trust it more if it showed the weather features mattered
on storm days (they add 0.006-0.024 AUC per window, claim 41) and if cancelled flights were scored.

For the second actor (a passenger app or delay-insurance pricer quoting a few hours before departure from public
schedule + weather) the input set is closer to what they have, though they too would pull the inbound aircraft from
FlightAware/ADS-B. This does not make the fit direct (USE-9 weighed factor), but it shows the task is real (USE-2
satisfied) and the benchmark is legitimate as a "low-signal, large, temporal, high-cardinality categorical" task.

**Gaps ranked by how much they change the task**

1. No inbound-aircraft / tail-number input (the largest single delay cause, ~40%): the task becomes delay risk without
   propagation. Source limitation; name it in fit_reason/known. (USE-3, USE-6, USE-8)
2. Potential leak kept on purpose (late destination weather, 1.94%; Guam): by USE-8's own list this makes the fit
   approximate, contradicting `fit="direct"`. (USE-8, USE-12, LEAK-10)
3. Mis-timed weather (UTC misjoin): the "a few hours before departure" snapshot is 3.5-10 h stale by time zone and an
   observation, not a forecast for the arrival. A stand-in. (USE-3, USE-8)
4. Cancelled and diverted flights excluded: the test population is filtered on a future outcome, concentrated on the
   worst days. (USE-5, USE-8)
5. ROC AUC ignores calibration that resource allocation needs: minor, a metric choice. (USE-5)
6. March 2024 missing from training: minor.

**What a domain expert would change**

- Set `fit="approximate"` and rewrite fit_reason to name the stand-ins: weather observed 3.5-10 h before departure
  (time-zone dependent) instead of current/forecast weather, a potential leak kept on purpose, no inbound aircraft,
  operated flights only. `known` should say "weather observed 3.5 to 10 hours before departure" rather than
  "a few hours".
- If a rebuild from the origin is ever on the table (PROV-13): take the BTS on-time table directly (it has
  Tail_Number, Cancelled, Diverted), add the inbound leg's scheduled arrival and its previous-leg delay as known at
  the prediction point (for a prediction point some hours ahead, only the inbound's delay known by then), re-join
  Meteostat in UTC at a fixed lead time, and count cancelled flights as late or drop them consistently with the stated
  use case. That would be a different, direct dataset.
- Report log loss alongside ROC AUC when discussing results (calibration matters to the OCC).

**Sources**

- The definition and the record; the panel's claim list, checklist and probes.
- Xu et al., Aeolus (arXiv 2510.26616, HTML v2): Table 9 features (no tail number), chains grouped by
  (OP_CARRIER, OP_CARRIER_FL_NUM, DATE), no mention of cancellations, no stated prediction point.
  https://arxiv.org/html/2510.26616v2
- BTS, percent of flight delay by cause (late-arriving aircraft about 40%, the largest cause 2010-2019 and in 2023):
  https://www.bts.gov/browse-statistical-products-and-data/info-gallery/percent-flight-delay-delay-cause-2010-2023
- Gopalakrishnan and Balakrishnan (MIT, ATM 2017): nearly 40% of delays from the late incoming aircraft; value of
  forecasts a few hours ahead. https://www.mit.edu/~hamsa/pubs/GopalakrishnanBalakrishnanATM2017.pdf
- Birolini et al. (Bergamo, Vueling): day-ahead primary delay prediction for routing.
  https://aisberg.unibg.it/handle/10446/283950
- Li (Purdue thesis 2018): departure delay and late-aircraft delay the most important features.
  https://docs.lib.purdue.edu/open_access_theses/1415
- FSU/Copa Airlines: probabilistic inbound-delay risk presented to operations managers.
  https://eng.famu.fsu.edu/node/10546
- Rules: .claude/skills/knowledge-curation/references/use_case.md (USE-2, USE-3, USE-5, USE-6, USE-8, USE-9, USE-10,
  USE-12).

</details>

<details><summary>Blind review</summary>

**Verdict: include with changes.** It is a real, large, honestly framed task with modest but real signal. However, the sampling across time is uneven in a way the source does not explain: about 44% of all rows fall in the last 6 weeks and March 2024 is missing. As a result, every temporal test window is a December-holiday, full-density slice, and that should be fixed before use.

**Task**
- The data is US domestic flights (BTS on-time data) with Meteostat weather at the origin and destination. The binary target is arrival delay of 15 minutes or more. Positive rate: 20.4% overall; by month it ranges from 12.9% (Oct 2024) to 29.5% (Jul 2024), which matches BTS seasonality.
- Who would use this: airlines, airports or travel apps scoring scheduled flights for delay risk, for passenger notification, buffer planning or rebooking. This is a real use. The features are schedule fields (carrier, flight number, origin and destination, scheduled times, scheduled elapsed time, coordinates) plus weather.
- The source is the Aeolus paper (arXiv 2510.26616, NeurIPS 2025 D&B), repo github.com/Flnny/Delay-data, Kaggle `flnny123/mfddmulti-modal-flight-delay-dataset`. The paper warns that random splits cause "significant temporal leakage". The Kaggle files are full-year CSVs, `flight_with_weather_2016.csv` to `..._2024.csv` (about 1.75 GB per year), with no license field on Kaggle.

**Concerns, most serious first**

1. **Uneven sampling over time; all test windows come from one special period.**
   - In the 200k sample, rows from 2024-11-20 onward have about 2,000-2,400 per day. Before that date there are about 110-200 per day.
   - The period 2024-11-20 to 2024-12-31 holds 43.8% of the rows (about 783k of 1.785M). That is roughly the full BTS volume (about 19-20k flights per day). The other 22.5 months hold only about 8% of their flights.
   - March 2024 is missing entirely: the data jumps from 2024-02-29 to 2024-04-01.
   - With 3 temporal test windows at the end, all test data is Thanksgiving through Christmas 2024 at full density. Training data is mostly a thin sample of other seasons. This looks like an artifact of preparation, not of the source: the source has complete yearly files.
   - **Change:** sample uniformly over time from the 2023 and 2024 files (or use a contiguous span), restore March 2024, and spread or space the test windows. At minimum, document the stratum.

2. **Weather is observed, not forecast, at scheduled times; destination weather is at the scheduled arrival time.**
   - Weather varies within an airport-day (median 1, up to 17 distinct O_TEMP values per airport-day) and follows the scheduled hour. A pre-departure prediction would only have forecasts, so this is optimistic.
   - It is not a leak of the outcome. D_* values match the origin weather of the destination airport at the scheduled arrival hour equally often for delayed and on-time flights (60.6% vs 60.1%). So the join uses scheduled times, not actual ones.
   - Weather adds about +0.03 AUC (0.601 without it, 0.631 with it, Dec-2024 test).
   - **Change:** acceptable as a nowcast setting, but document it.

3. **Weak signal; most of the variance is daily shocks.**
   - LightGBM (400 trees, with date features added) gets these AUCs on the temporal windows: 0.609 (Dec 1-10), 0.639 (Dec 11-20) and 0.631 (Dec 21-31).
   - A random 80/20 split gets 0.693. The gap confirms day-level clustering and that the temporal split is the right one.
   - This matches the paper (Table 3 AUCs about 0.56-0.77; flight-chain AUC about 0.69).
   - The task is not trivial and not noise. It is useful for telling methods apart at large n, but the differences will be small.
   - Flights that were cancelled or diverted (target undefined) seem to be dropped. This is standard, but note it.

4. **Preparation details (minor).**
   - FL_DATE is kept as a datetime and there are no day-of-week or month columns. Dropping the date gives 0.626 vs 0.631 with them. Make sure the benchmark harness turns the date into features, or add DAY_OF_WEEK and MONTH (the source has them).
   - OP_CARRIER_FL_NUM is stored as an int. It is an identifier, so integer order means nothing, but tree models cope.
   - The lat/lon columns duplicate ORIGIN and DEST (307 and 306 categories); harmless.
   - Missing values: weather is missing in 0.015-0.023% of rows.
   - There are no exact duplicates, not even with the target excluded, and no duplicate (date, carrier, flight number, origin) keys.
   - Leaky source columns (DEP_DELAY, DEP_TIME, TAXI_*, ACTUAL_ELAPSED_TIME, AIR_TIME, ARR_TIME) are correctly removed.
   - The CRS_*_TIME_MIN conversion looks right: range 1-1439, and 3.5% of flights arrive after midnight.

5. **License.** No license is shown on Kaggle or in the repo README. The data comes from public US-government data plus Meteostat (CC BY-NC 4.0), so non-commercial terms may apply. Check before redistributing.

**Could not check**
- I could not download the original 2023 and 2024 CSVs (they need a Kaggle login), so I could not confirm whether the March-2024 gap and the dense tail come from the source or from preparation.
- I could not see the exact boundaries of the 3 test windows. I approximated them as Dec 1-10, 11-20 and 21-31.
- I could not check the weather units (O_PRCP up to 97.7; D_WSPD up to 207 looks like an outlier) or the exact hour-matching and time-zone logic.
- I only saw the 200k sample, not the full 1.785M rows.

</details>

<details><summary>Precedent check</summary>

Scope: the definition's choices (`datasets/_dev/tabarena-v0pt2/aeolus_1m/dataset.py`), the curator's CC of 2026-10-12
in `curation/records/aeolus.md`, the open questions in `REVIEW_before.md`. Sources: the decision register
(the decision register; none of its four flags touches aeolus), the Cases tables of the knowledge files, the sibling
records (`airlines`, `airlines_depdelay_10m`, `pnwflights14`) and the other definitions of the working copy. No file
was edited.

Summary: two real departures for the curator (PROV-13 against "weather as released"; USE-8 `fit="direct"` with a
leak kept on purpose, where the precedents split), one procedure gap (LEAK-6/LEAK-7: the late part of the destination
weather never measured on its own, Guam fixable), the rest consistent. aeolus is itself the case of SPLIT-20, SPLIT-21
and EV-1, so its split choices are the precedent rather than a departure from one.

**Per decision**

| # | Decision (who, date) | Rule | Verdict | Closest precedents |
|---|---|---|---|---|
| 1 | Weather kept as released, UTC hours joined to local clock times (CC Lennart 2026-10-12; definition: "re-joining it would be our own fix") | PROV-13 (Must, P5); tension "Repair against cleaning around damage" | **departs; the stated reason does not fit the rule** (it cites the TP-6 idea "a fix of our own invention", which is about better versions, not repair of damage). PROV-13 is a Must: no exception, only a higher Must or an amendment | ashrae (2026-10-15, readings put in kWh from the owners' raw files), SUPPORT2 (restored from ICPSR 2957), coad_colon_adenocarcinoma (retired for rebuild, CC 2026-10-16), corporate_credit_rating (retired for rebuild, CC 2026-10-16); LEAK-30 tension row (Lennart 2026-10-19: "rebuild from unprocessed values when the source has them"). All later than aeolus's CC; PROV-13 itself was written 2026-10-20 (commit 58ee235). Meteostat hourly data, the origin, is public and was read for decision 2 |
| 2 | `fit="direct"` while the notes keep a `Potential leak, kept on purpose:` (late destination weather) and the cohort lacks cancelled/diverted flights (AI draft; the 2026-10-14 task-summary marks could not be read) | USE-8 (Must): "Approximate: ... a potential leak kept on purpose", case kick | **departs without a stated reason**; the precedents themselves split | approximate: kick (leak audit, CC Lennart 2026-10-01; wheel-type missingness kept), onlinenewspopularity (same-day articles published hours later, kept), african_credit_scoring_challenge, credit_card_customers (Lennart 2026-10-19). direct: zillow_prize (tax-delinquency snapshot after some training sales; "kept since dropping it changes nothing", measured R² 0.0069 vs 0.0068). LEAK-30 scaling keeps (bioresponse, cooking_time, delivery_eta, maps_router_eta, lung_cancer_epithelial_genexp, all direct) are a different mechanism |
| 3 | Late destination weather (1.94% of flights, median 0.7 h after the scheduled departure) and Guam origin weather kept (CC 2026-10-12 "weather as released") | LEAK-10 (Must), LEAK-6 (Must: slight optimism with a known cause may stay; a confirmed leak goes even when small), LEAK-7 (Should: smallest fix) | **consistent with kick and onlinenewspopularity on the keep**, but the evidence is weaker than theirs: only an upper bound for all destination weather (0.006-0.024 AUC) was measured, never the late 1.94% alone (onlinenewspopularity and zillow measured the kept part itself). The Guam case (106 rows in the frame; origin read about 10 h later at UTC+10) has a cheap LEAK-7 fix (origin weather missing for GUM) that nothing in the notes declines | kick (2026-10-01), onlinenewspopularity, zillow_prize; santander `has_*` (CC 2026-09-30, dropped at +0.003) is label-derived, so not the same mechanism |
| 4 | Target `ARR_DEL15` (arrival >= 15 min late, ROC AUC) instead of the minutes (CC 2026-10-12) | USE-5 (Must), TP-7, LEAK-4 (Must), CLEAN-16 | **consistent**: the DOT definition is the field's convention and the paper's classification task; departing from the authors' `abs(ARR_DELAY) > 15` follows USE-5 (corporate_credit_rating, cirrhosis: redefine a badly built label). One gap: LEAK-4 asks for the probes on the source label (ARR_DELAY) too; only the 2026-10-07 LightGBM R² 0.01-0.02 is on record. Low risk (the threshold column is not a feature) | corporate_credit_rating, audiology_diagnosis (LEAK-4); sibling records `airlines`, `airlines_depdelay_10m` are regression, unprocessed |
| 5 | History from 2023-01-01, two-week windows, one in the holiday peak (CC 2026-10-12) | SPLIT-20 (Should), SPLIT-21 (Must), SPLIT-18, EV-1 | **consistent**: aeolus is the case of SPLIT-20, SPLIT-21 and EV-1 (splits.md Cases row, evidence.md row 252). If the paper's Sec. 4.1 prescribes periods (2024 alone), SPLIT-19 (Should) is departed from **with a stated reason** (the previous holidays and a two-week refit, SPLIT-20); the paper text was not re-read in this run | climate_model_weather_forecasting (SPLIT-18, weather windows of 1-2 weeks) |
| 6 | One-day gap between train and test | SPLIT-10 (Should), LEAK-12 | **consistent** | brazilian_ecommerce, sf_permit_time |
| 7 | Known airports and flight numbers across the cutoff | USE-10, SPLIT-13, SPLIT-30 | **consistent** (reading 2 of `test_rows_seen`, no action) | |
| 8 | No cancelled or diverted flights (as in the release) | LEAK-22 (Must: follow the paper's cohort) | **consistent**; it is a second named gap in `fit_reason`, which bears on item 2 | |
| 9 | Scheduled block time < 15 min made missing (3 rows) | CLEAN-11 (Should) | **consistent** | heart_disease_va_long_beach (chol 0), thyroid_discordant (age 455), sdss_17 (-9999) |
| 10 | `OP_CARRIER_FL_NUM` categorical (CC 2026-10-12) | CLEAN-14 (Should), CLEAN-3 | **consistent** with the source's typing (paper Table 9). Not a departure, a note: the number alone (8,819 categories) pools different carriers' services; the service is carrier + number (98.8% seen in train) | |
| 11 | Task probes: `no_spread` today (LightGBM 0.609, linear 0.597, SE 0.015); notes say "no flags", linear 0.594 | TP-1, TP-2 (Should), TP-3; EV-7/EV-8 | keep is **consistent**; the note is stale (a writing fix, not a curator decision). The 2026-10-07 assessment's "0.64-0.67" is the all-years set-up (CHANGELOG 2026-10-12: all nine years 0.632/0.609/0.620) and is superseded | acquire_valued_shoppers_challenge (no_spread, best AUC 0.654, kept 2026-10-06), amex_non_iid_1m (no_spread, large, kept 2026-10-06) |
| 12 | REVIEW issue 5, licence conflict raised as an issue | EV-4 (Must: a licence is a one-line note, "none of them is an issue for the curator"); selection.md | AI drafting **departs from EV-4's wording**, but follows the working-copy practice (numerai_v5_2_1m issue 1, corporate_credit_rating_cat_data_set_ratings_raitings issue 5). Not a curator decision; suggest a note, or EV-4 be amended to allow "redistribution" questions as issues. The definition's `license` string follows force_2020 / stroke_prediction (both terms named) | |
| 13 | REVIEW issue 6, no pinned version | definitions.md ("pin a DOI or an archived release where one exists") | **consistent**: none exists; SHA-256 prefixes in `download_description` as numerai_v5_2_1m (no versioned URL, date and sizes noted) | numerai_v5_2_1m |
| 14 | Release problems "noted only, not reported" (CC 2026-10-12) | PROV-15 (note in the record so it can be reported later) | **consistent** | OpenML 43838, SUPPORT2 |
| 15 | Uniqueness against other BTS cuts | PROV-4, PROV-6 (Must), PROV-7 | **open, not a departure**: the CC of 2026-10-12 on `airlines` and `airlines_depdelay_10m` defers it ("decide whether it is a second flight-delay task or a duplicate of aeolus"). `pnwflights14` (BTS 2014, AI-unverified) has no such note. All three end at BTS on-time data; under PROV-6 a cut without a distinct task is a duplicate, so the later-processed record decides, and the note should reach pnwflights14 too | arsenic_male_lung (PROV-6), amex_iid/amex_non_iid (PROV-7) |
| 16 | `domain = "business & marketing"` | (metadata) | **departs without a stated reason** from the working-copy convention "transport has no value of its own" -> `industry & manufacturing` (nyc_taxi_trip_duration, delivery_eta_1m, maps_router_eta_1m). It follows the record and the `airlines` record. Lowest rank; one line for the curator | nyc_taxi_trip_duration |

Drift (case 3): Lennart, PROV-13 mechanism "damaged release, origin reachable": kept as released on 2026-10-12
(aeolus), repaired or retired from 2026-10-15 on (ashrae, coad, corporate_credit_rating; LEAK-30 row 2026-10-19
"rebuild when the source has them"). The aeolus call is the earlier one. Mechanisms differ (a timing join, not units or
scaling), which is the open point.

Third exception (case 4): none reached. Timing leaks kept with `fit="direct"`: zillow_prize and aeolus (two).

**Consistency prompts**

**Consistency check (AI, 2026-10-20):** your call on aeolus (weather kept as released, CC 2026-10-12; a departure from
PROV-13, a Must) differs from ashrae (2026-10-15), SUPPORT2, coad_colon_adenocarcinoma and corporate_credit_rating
(2026-10-16), where a damaged release was repaired or retired once the origin had the clean data; Meteostat's hourly
station data are public. What sets aeolus apart?
(a) the misjoined weather is genuine weather observed before departure, so the columns stay true and P4-safe once the
lag is stated, while the alignment the release claims would put the destination weather at the scheduled arrival,
after the prediction point (P4 outranks P5): a repair would have to be a new design (both airports at the last hour
before departure), which PROV-14 makes a new dataset with its own record. Recorded as PROV-13 not applying (or as an
amendment narrowing PROV-13 to damage that makes values false); (b) treat aeolus like ashrae: re-join Meteostat at the
last hour before the scheduled departure, as a new record (PROV-14); (c) reopen ashrae and the others to match aeolus;
(d) amend PROV-13.

**Consistency check (AI, 2026-10-20):** aeolus is `fit="direct"` with a `Potential leak, kept on purpose:` (late
destination weather) and no cancelled or diverted flights; USE-8 names "a potential leak kept on purpose" as
approximate, as decided for kick (leak audit, 2026-10-01) and onlinenewspopularity, while zillow_prize (direct) kept
its timing leak because dropping it changed nothing. What sets aeolus apart?
(a) the late readings are within about an hour of the departure, where a short-range weather forecast known at the
prediction point carries the same information (USE-6: a forecast is an input), and masking the 1.94% changes the score
by no more than noise, to be measured as zillow did; recorded as an exception to USE-8; (b) treat aeolus like kick:
`fit="approximate"`; (c) reopen zillow_prize to `approximate`; (d) amend USE-8 so a kept leak shown to change nothing
stays direct.

**Consistency check (AI, 2026-10-20):** the definition calls the transport domain `business & marketing`, while
nyc_taxi_trip_duration, delivery_eta_1m and maps_router_eta_1m use `industry & manufacturing` ("transport has no value
of its own"). What sets aeolus apart?
(a) airline operations are a business service, as the `airlines` record has it; recorded with a code comment;
(b) treat aeolus like nyc_taxi_trip_duration; (c) move the three to `business & marketing`; (d) add a rule for
transport tasks.

**For the panel (not curator decisions)**

- LEAK-6 / LEAK-7: measure the late part alone (destination weather made missing for the 1.94% read after the
  scheduled departure, same untuned LightGBM, per window) and fix Guam (origin weather missing for GUM, 106 rows):
  the smallest fix exists and is cheap, and the keep should rest on a measurement of the kept part.
- EV-7: update the task-probe bullet (`no_spread`, linear 0.597) and drop or reconcile the stale 0.64-0.67.
- LEAK-4: record a probe on ARR_DELAY (the source label) or state why it is not needed.
- PROV-6: add the dated aeolus note to `curation/records/pnwflights14.md` as was done for the two airlines records.

</details>

<details><summary>Advocate</summary>

Position: ship, after documentation fixes, `fit="approximate"`, and two cheap cleaning fixes. Nothing the panel found
is a Must that the definition cannot meet.

**1. The split is right, and that is the main validity question (P4, SPLIT-1/9/10/11/14 hold)**

Evidence: split audit. Temporal on FL_DATE, three two-week windows, a one-day gap. The gap is measured: with no gap,
456-509 earlier flights per window land inside the test window; with the one-day gap, 0-1. A random split over the same
rows would add 0.08-0.09 ROC AUC (0.630 -> 0.717 on window 0) because delays cluster by day. 100% of test airports and
99.9% of flight numbers are seen in train: a known-entity task (USE-10, SPLIT-13), so temporal is the one regime.
Why it outranks objections: this is P4 working as intended. The blind reviewer reached the same conclusion on its own
(random 0.693 against temporal 0.61-0.64).

**2. The UTC weather join does not trigger a repair under PROV-13, because the "repair" would break P4 (P4 > P5)**

The objection (precedents item 1): PROV-13 (Must, P5) says repair damaged releases from the origin; Meteostat is public;
ashrae, SUPPORT2, coad and corporate_credit_rating were repaired or retired.
Evidence: decision 2 and the claim audit confirm the join (station files match as UTC at 99.6-100%). Every reading is
real weather, observed before departure, except 1.94% of destination rows and Guam (item 3).
Rule: the release *intended* the destination weather at the scheduled arrival time. That is after the prediction point
for every flight, so a faithful repair would build a LEAK-10 (Must, P4) violation into 100% of rows. P4 outranks P5.
Any leak-free re-join (both airports at the last hour before departure) does not match the release, so under PROV-14
(Must) it is a new dataset with its own record, not a repair of this one. The ashrae/SUPPORT2/coad cases differ: there
the damage made the values false (wrong patient, wrong units). Here the values are true; only the lag is wrong in the
docs. Remedy: write the lag correctly (point 5), and record it as the curator's answer (a) to the PROV-13 consistency
prompt, or as an amendment narrowing PROV-13 to damage that makes values false. The overnight 3.6% (destination
weather about 25 h early) is the same kind: earlier, not later, so it is not a leak. It needs an `Anomaly:` bullet.

**3. The kept leak is measured and negligible; Guam gets the cheap fix (LEAK-10/LEAK-6 weak, LEAK-7, LEAK-30 tension)**

The objection (precedents item 3): the keep rested only on an upper bound.
Evidence: the claim audit has now measured the late part alone. Masking the destination weather of the late rows at
test costs 0.0003-0.0004 AUC per window. All destination weather adds +0.008 to +0.016. The late rows are 0.93-1.05%
of each window.
Rule: LEAK-6 allows slight optimism with a known cause to stay. The principles tension row ("a weak ... leak against the
data as published") keeps it with a `Potential leak, kept on purpose:` note, and kick, onlinenewspopularity and
zillow_prize are the precedents.
Concession and fix: Guam's origin weather (106 frame rows, about 10 h after departure) has a one-line LEAK-7 fix: set
O_* to missing for ORIGIN == GUM. Take it. Also reword fit_reason: "a median 0.7 h and at most about 4.4 h after".

**4. Concede the fit: `approximate`, not `direct` (USE-8, Must)**

USE-8 lists "a potential leak kept on purpose" as approximate. kick is the precedent, and the weather is a stale
snapshot as well. I do not argue USE-9: the practitioner showed that no actor has exactly these inputs. The mildest
remedy is to set `fit="approximate"` and name the stand-ins in fit_reason: weather observed 3.5-11 h before departure
(a day early for overnight destinations), the kept late readings, no inbound aircraft, operated flights only. This
is a metadata change and keeps the dataset. A real task with a named gap is what "approximate" exists for.

**5. The documentation errors are real and each has a one-line fix (EV-7, USE-5 doc; not validity)**

- The probe bullet should read `no_spread`, linear 0.597, plus the 1M-train LightGBM 0.629-0.630. Drop the record's
  0.64-0.67, which comes from the all-years set-up.
- "The paper's classification task": the paper uses > 15. Write "the DOT definition (>= 15); the paper uses > 15"
  (0.68% of flights differ).
- `known`: "a few hours" becomes "3.5 to 11 hours, about a day for overnight destinations".
- splits_comment: name the paper's split (1-15 June 2024, 6:2:2) and why we depart from it. One window and no
  season would break SPLIT-14 (Must) and SPLIT-20, so the departure is required (SPLIT-19 Should, reason stated).
- `domain`: follow nyc_taxi/delivery_eta (`industry & manufacturing`), or have the curator record why not.

**6. Value holds: large, real signal, every window scorable (P6, TP-2/TP-3)**

Evidence: LightGBM skill +0.219 over the baseline. With 1M train the AUC is 0.629-0.630. Each window has at least
8,231 rows of the minority class. The `no_spread` flag (paired SE 0.015) comes from day-level clustering under the
correct split. acquire_valued_shoppers and amex_non_iid_1m were kept with the same flag, and the tension row "right
split against the score" says a small signal under the right split is no reason to retire. The practitioner's "0.61
is too weak for an OCC" is a P3 usefulness remark, not a P6 failure. The paper's own AUCs are 0.56-0.77.

**7. The blind reviewer's top concern is the v2 protocol, not damage; the rest is P7 notes**

"44% of rows in the last 6 weeks" is the documented v2 sampling. Each test window keeps all of its rows, and the train
side is a uniform random 1M (38-50k per month, split audit). The splits never mix the two. March 2024 is missing in
the raw release (claim audit: 2024 months 1, 2, 4-12), not in our preparation. FL_DATE as a datetime is expanded by
the pipeline (CLEAN-12).
Missing inbound aircraft and cancelled flights are limits of the source. LEAK-22 says to follow the paper's cohort,
and USE-6 says to name a gap the source dropped, not invent one. Both go in fit_reason (point 4).
P7 fixes that are cheap and safe:
- set O_TEMP < -50 and *_WSPD > 120 to missing (about 0.001% of rows);
- note the GUM/PPG sign-flipped coordinates (or flip them back);
- correct the OP_CARRIER_FL_NUM note: a service is carrier plus number.
The licence conflict is a one-line note (EV-4). PROV-6 against the `airlines` records is for those records to decide.
They are processed later and already carry the deferral.

Judgment record (proposed):
Verdict: ship after changes.
Validity: USE-5 holds (DOT target); USE-8 changed to approximate; LEAK-10 weak, kept with a note (late part measured
at 0.0003-0.0004 AUC), Guam fixed (LEAK-7); SPLIT-1/9/10/14 hold; PROV-13 does not apply (P4 over P5, PROV-14), or an
amendment if the curator prefers.
Value: TP-2 real signal, `no_spread` kept as for amex_non_iid_1m.
Quality: CLEAN-11 impossible weather made missing; notes for coordinates, 23:59, flight number.
For the curator: the PROV-13 consistency prompt (answer (a)), the domain line.

**Rebuttal**

We agree on the verdict ("ship after changes", nothing asks for exclusion). One dispute remains: whether point 1 blocks
shipping this definition.

**Critic 1 (PROV-13): disputed in part**

What I accept:
- The overnight fact: destination weather for 3.6% of flights is about 25 h old. It gets an `Anomaly:` bullet.
- The stated reason, "our own fix", is the wrong rule. It must go.
- A keep needs a recorded curator answer. Without one it is a Must departure.

What I dispute: that the definition cannot ship until a rebuild.

PROV-13 asks to "repair or rebuild from the origin". A repair restores what the release meant to hold. Here that is
destination weather at the scheduled arrival, which falls after the departure for every flight: a LEAK-10 Must
violation (P4) in 100% of rows. P4 outranks P5, so that repair is barred.

The critic's own remedy is a different thing. A re-join at the last hour before departure is a new design, and under
PROV-14 (Must) it is a new dataset with its own record, as the critic agrees. That is a second dataset, not a
condition on this one.

The values themselves are true. They are real observations made before departure (the late readings are covered under
point 3), unlike ashrae (wrong units) and SUPPORT2 (wrong patient).

Outcome: ship once the curator records answer (a) to the PROV-13 prompt, either as "PROV-13 does not apply" or as an
amendment narrowing PROV-13 to damage that makes values false. The PROV-14 rebuild can go to the curator as an
optional new record.

**Critic 2 (USE-8): conceded**

Set `fit="approximate"`. fit_reason names all four gaps: stale weather, the kept late readings, no inbound aircraft,
operated flights only. `known` gets the critic's wording.

**Critic 3 (LEAK-6/LEAK-7): conceded**

I had kept the late destination readings as a weak leak. The critic is right that they are confirmed post-departure
values, not suspected ones, and LEAK-6 says a confirmed leak goes even when small.

The fix is the mildest one and keeps the dataset:
- set O_* to missing for Guam;
- mask D_* where the reading's hour falls after the scheduled departure. This uses the per-airport time zones the
  claim audit already built, and the measured cost is 0.0003-0.0004 AUC.

This replaces the "kept on purpose" bullet, so one of the reasons for `approximate` falls away. Approximate still
holds for the stale snapshot.

**Critic 4 (procedure): conceded**

All five text fixes, as in my point 5.

**Critic 5 (TP-3, one season): conceded as a note, disputed as an open Must**

Agreed: a `no_spread` note, and a note that the windows test early-winter delays.

Disputed: that TP-3 is unsettled in a way specific to aeolus. Tuned results do not exist for any dataset in the copy.
acquire_valued_shoppers and amex_non_iid_1m were kept on the same flag before tuning. The probe skill is +0.219, and
each window has at least 8,231 rows of the minority class.

Settling TP-3 on tuned results is the collection-wide step before the freeze. It is no condition for this dataset
alone.

**Critic 6 (CLEAN-11): conceded**

Cheap fixes in `_clean`:
- *_WSPD > 120 and O_TEMP < -50 to missing;
- flip the GUM and PPG signs;
- note the four block times.

**Critic 7 (PROV-6): conceded**

Add a dated note to `curation/records/pnwflights14.md`. aeolus is the reference task; the other cuts are judged
against it.

</details>

<details><summary>Critic</summary>

Position: **do not ship as defined; ship after changes.** The task is real (an operated US flight, DOT ARR_DEL15,
temporal two-week windows with a measured 1-day gap), so nothing here asks for exclusion. But the only non-schedule
signal, the weather, is damaged in the release and kept under a reason that does not fit a Must, the fit is labelled
`direct` against USE-8's own list, a confirmed post-departure input (Guam) has a one-line fix nobody declined, and
several shipped statements are refuted by measurement. Points in rank order.

**1. P5, PROV-13 (Must): damaged weather kept "as released" while the origin is public**

- Problem: the release joined Meteostat's UTC hours to local clock times. Origin weather is 3.5-11.4 h old (median
  5.15 h), not "shortly before departure". New fact from the claim audit: the release dates CRS_ARR_TIME on FL_DATE,
  so for the 460,592 overnight arrivals (3.6%) the destination weather is a median 25 h before departure (max 33.7 h);
  the reading equals the departure-date reading at 100% of 272,624 matched flights against 9.6% for the next date.
- Effect: the weather columns do not describe the weather the actor sees; western and Pacific airports are degraded
  most. Weather is the task's only non-schedule input (destination weather alone +0.008 to +0.016 AUC, claim audit).
- Evidence: decision 2 (station files match as UTC at 99.6-100%, 2-8% at real offsets), re-confirmed today for ORD,
  HNL, PHX (claim_audit.md claims 6, 37, 64); precedents.md decision 1.
- Rule: PROV-13 (Must) says repair or rebuild from the origin when it has the clean data. Meteostat hourly station
  files are public and were downloaded for decision 2 and again today. The stated reason ("re-joining it would be our
  own fix") is the TP-6/USE-4 idea about better versions, not PROV-13. Drift: ashrae, SUPPORT2, coad,
  corporate_credit_rating were repaired or retired on the same mechanism class after 2026-10-15 (principles,
  consistency case 3). A Must has no exceptions.
- Remedy: repair from the origin: re-join Meteostat in UTC at the last full hour before the scheduled departure for
  both airports (time zones per airport, as the claim audit computed). Under PROV-14 that is a new version with its
  own record; this definition should not ship meanwhile. The only alternative that satisfies the rules is a curator
  amendment narrowing PROV-13 to damage that makes values false, recorded as such; a keep without one is a Must
  departure.

**2. P3, USE-8 (Must): `fit="direct"` contradicts the definition's own notes**

- Problem: USE-8 lists "a potential leak kept on purpose" and "one snapshot standing in for a forecast" as approximate.
  The definition keeps both (the late destination weather; stale observations standing in for the weather at the
  flight), and also lacks the inbound aircraft (about 40% of delay by BTS cause data) and the cancelled and diverted
  flights, which cluster on the worst days.
- Effect: the label tells a model user this is the real OCC decision; it is "delay risk from schedule and stale
  weather, operated flights only".
- Evidence: practitioner.md (fit approximate; USE-9 does not rescue it), column_audit.md problem 1, precedents.md
  decision 2 (kick approximate for the same mechanism; zillow_prize direct only because the kept part was measured
  to change nothing).
- Remedy: fix the definition: `fit="approximate"`, fit_reason naming the four gaps, `known` saying "weather observed
  3.5 to 11 hours before departure (up to a day for overnight arrivals)".

**3. P4, LEAK-6 (Must) and LEAK-7 (Should): Guam origin weather after departure, a confirmed leak with a cheap fix**

- Problem: all 686 Guam departures (106 in the frame, 14 per test window) get origin weather about 10 h after the
  departure; 1.94% of flights get destination weather after the scheduled departure, 31.5% of those more than an hour
  late (max 4.35 h). fit_reason says "up to about an hour" and omits Guam.
- Effect: small on the score (masking the late destination part costs 0.0003-0.0004 AUC), but it is information from
  after the prediction point, and a later re-join or a model that keys on GUM can exploit it.
- Evidence: claim_audit.md claims 11-12, 40, 41; column_audit.md problem 2; precedents.md decision 3 (nothing in the
  notes declines the Guam fix).
- Rule: LEAK-6 lets slight optimism with a known cause stay, but "a confirmed leak goes even when small"; Guam is
  confirmed for every row. LEAK-7: the smallest fix (mask) beats keeping or dropping the columns.
- Remedy: fix the definition: set the origin weather of GUM to missing; mask D_* where its hour falls after the
  scheduled departure (needs one time zone per airport). If point 1 is repaired, both disappear.

**4. Procedure (EV-7, writing.md): shipped statements refuted by measurement**

- `known`: "a few hours before departure" (refuted: up to 11.4 h origin, ~25 h for overnight destinations).
- Decision 2 title "3.5 to 10 hours earlier" (origin to 11.4 h; overnight destinations ~25 h).
- "ARR_DEL15 ... the paper's classification task": the paper uses > 15, we use >= 15 (0.68% of flights differ).
- Task-probe bullet "no flags; linear 0.594": today `no_spread` (TP-3), linear 0.597; the shipped 1M train gives
  LightGBM 0.629-0.630; the record's 0.64-0.67 is the superseded all-years set-up.
- "The authors' benchmarks use 2024 alone": Sec. 4.1 is 2024-06-01..06-15 with a 6:2:2 chronological split; the
  departure is right (SPLIT-14, SPLIT-20) but unargued (SPLIT-19).
- Remedy: correct the text; add an `Anomaly:` bullet for the overnight destination weather.
- Evidence: claim_audit.md claims 6, 30, 32, 44, 63; split_audit.md problem 1.

**5. P6, TP-3 (Must) with SPLIT-20 (Should): value unsettled, one season tested**

- Problem: `no_spread` flag (LightGBM - linear +0.025, paired SE 0.015); the scheduled arrival time alone reaches 77%
  of the best skill; all three windows are late November-December, so summer convective delays (25-30% late) are never
  tested, and day-level clustering makes each window about 14 effective draws.
- Effect: the benchmark may not separate methods, and what it measures is early-winter delays only.
- Evidence: the task probes; checklist.md P6 row; split_audit.md problem 2.
- Rule: TP-3 keeps on a tuned spread; there are no tuned results yet. SPLIT-21 forbids re-choosing windows on scores,
  and the split follows the application (tension P4 over P6), so this is no reason to exclude.
- Remedy: a note now (the score measures early-winter delays; `no_spread` with its reading); settle TP-3 on tuned
  results before the collection is frozen. More windows only if the curator decides it on the use case.

**6. P7, CLEAN-11 (Should): impossible values left in**

- O_TEMP -60.6 C at Sarasota in May (7 history rows, 1 in the frame); wind 120-232 km/h with no rain at ACY, HOU,
  ATW and others (74 history rows); GUM longitude and PPG latitude sign-flipped; four block times of 17-60 min on
  routes with medians 90-133 min.
- Evidence: column_audit.md problem 3; claim_audit.md claims 24, 40.
- Remedy: cheap and safe fixes in `_clean` (to missing; flip the two signs), or a note. Quality only: not a reason
  against shipping.

**7. P5, PROV-6 (Must, open): uniqueness against the other BTS cuts**

- `airlines` and `airlines_depdelay_10m` carry a deferred "duplicate of aeolus?" note; `pnwflights14` (BTS 2014) has
  none. Not a defect of aeolus, but the record should state it is the flight-delay task the others are judged
  against. Remedy: a dated note in `curation/records/pnwflights14.md` (precedents.md decision 15).

Dropped: the blind review's "uneven sampling over time" (the frame keeps all test-window rows and a uniform 1M train
side by the v2 protocol, by design); the licence conflict (EV-4: a one-line note, not an issue); the domain label
(metadata, no effect on the task).

**Rebuttal**

We now agree on the verdict (ship after changes), on the fit (`approximate`), on the Guam fix, on the text fixes
and on the P7 fixes. One point is still disputed: PROV-13.

**Advocate 1 (split): concede**
SPLIT-1/9/10/11/14 hold on measurement (gap 456-509 to 0-1 leaking flights; random split +0.08-0.09 AUC). I raised
no objection to the regime.

**Advocate 2 (PROV-13 does not apply, P4 over P5): partly concede, partly dispute**
- Conceded: restoring the alignment the release intended (destination weather at the scheduled arrival) would put
  post-departure weather into every row, against LEAK-10 (Must, P4). P4 outranks P5, so that repair is ruled out. A
  leak-free re-join does not match the release, so PROV-14 makes it a new record.
- Disputed: that does not make PROV-13 inapplicable. Its remedy is "repair **or rebuild** from the origin when it has
  the clean data". A rebuild under PROV-14 is that remedy, not a way around it. P4 rules out one form of repair, not
  the rule.
- Disputed: "the values are true; only the lag is wrong in the docs". For the 3.6% overnight arrivals, the column is
  the destination's weather at that clock hour on the **previous** date, a median 25 h before departure. That pairing
  was never intended. It is false in the sense the ashrae cases meant: the value is attributed to the wrong time.
  The origin lag also differs by time zone (3.5 to 11.4 h), so it is an error that varies with ORIGIN, not one stated
  lag.
- What decides it: keeping the data as released without a recorded amendment is a departure from a Must. The
  advocate also offers "or an amendment". I accept either (a) a curator amendment narrowing PROV-13 to damage that
  makes values false, with aeolus as its case, or (b) the rebuild as a new record. I withdraw "this definition should
  not ship meanwhile" **if** (a) is recorded. Without (a) or (b), my point 1 stands.

**Advocate 3 (kept leak, Guam): concede, with one point kept**
Masking the late destination weather costs 0.0003-0.0004 AUC, which is measured slight optimism with a known cause.
LEAK-6 allows a keep with a note, as for kick and onlinenewspopularity. I drop the demand to mask the D_* late
readings. Masking stays an optional LEAK-7 step. The Guam fix is agreed. I keep one point: the fit_reason should give
the maximum ("at most about 4.4 h"), as the advocate also proposes.

**Advocate 4 (fit approximate): concede**
Agreed on the remedy and on naming the four gaps.

**Advocate 5 (documentation): concede**
It matches my point 4. The domain line is a matter for the curator.

**Advocate 6 (value): concede the keep, keep the note**
The precedents acquire_valued_shoppers and amex_non_iid_1m kept the same `no_spread` flag, and the tension row "right
split against the score" applies, so this is no reason to exclude. Still not settled: TP-3 has no tuned results.
Also, all three windows fall in one season (split_audit.md problem 2). I ask only for the note "the score measures
early-winter delays" in splits_comment. No change to the split (SPLIT-21).

**Advocate 7 (blind review, P7, PROV-6): concede**
The uneven sampling is v2 protocol; I had already set it aside. March 2024 is missing at the source. The P7 fixes are
agreed. On PROV-6, the deferral sits in the `airlines` records. The one gap is that `pnwflights14` has no note, and
that is a record edit outside this definition. I leave it to the curator.

Proposed judgment record (what still differs from the advocate's): Validity: PROV-13 triggered. Remedy: a curator
amendment (narrow to value-falsifying damage) or a rebuild as a new record (PROV-14). Not "does not apply". Add an
`Anomaly:` bullet for the overnight destination weather. Value: TP-3 open until tuned results exist; add a note on
the single season.

</details>
