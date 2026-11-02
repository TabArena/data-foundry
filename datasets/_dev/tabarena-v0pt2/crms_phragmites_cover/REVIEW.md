# crms_phragmites_cover

**Outcome:** added; recommended `No` (`Time-series (Forecasting)`) under TP-10 as written, which you kept on
2026-11-02 (the record is now `No`). The data are the vegetation plots of Louisiana's Coastwide
Reference Monitoring System (CPRA with USGS), from CPRA's CIMS downloads: 69,161 surveyed visits of 4,099 stations at
394 sites, 2007-2025. The target is the percent cover of common reed (Phragmites australis) in a 4 m^2 plot at the
station's next annual survey (zero in 94% of visits), scored by RMSE (fallback; no source defines a metric). The split
is temporal: each of the nine seasons 2017-2025 is a test window, trained on all earlier seasons, at stations already
monitored. Most of the skill is last season's cover: the models beat it raw by 10%, but a three-number shrinkage of it
comes within 1.1% of the best model.

Changed after the panel, no decision needed: the mediator's changes 1-10 are in the definition (named under validity
and quality below). On the changed definition the random forest scores 6.97 (6.93 before), so its margin over the
fitted curves narrowed from 1.6% to 1.0-1.1%. The record keeps the marker `No Good Target / Scientific Discovery`,
which you kept on 2026-10-30, until your mark: the panel finds the decision real (fit approximate, USE-8), and the
same marker is open on four other `Yes` records of this run (pennsylvania's issue 1 asks it for all five).

Validity:
* SEL-10/SEL-11 via TP-10 leg 1 (Must): not met as the rule is written and was applied; TP-10 stays as written
  (2026-11-02).
* USE-1 and MET-1 triggered (the use case said "flag emerging hotspots for control", but about 91% of the squared
  error sits on plots that already hold reed, and a third of the plots with reed are in the delta); fixed in the text,
  `rmse` kept (MET-7). USE-3 triggered, fixed (prediction point before the season, once the last one is in CIMS);
  USE-6 triggered, fixed (a flag and the crew's estimate for an unentered dense-stand visit, also counted in the site's
  nearby share). USE-8: fit approximate (no source makes the prediction, a manager acts on sites, CRMS does not tell
  the invasive lineage).
* LEAK-10 holds for every feature except the soil cores, which CIMS posts 1-2.5 years after sampling; lagged (LEAK-7).
  SPLIT-1, SPLIT-3, USE-10 hold (temporal; 97.9-100% of test rows at known stations). SPLIT-10: no gap, measured (the
  last season is 91-100% in CIMS by January-June).
* PROV holds for the data: the blind reviewer's rebuild of the target from the raw file matches every row (the 11 that
  differ are trace codes set to 0.5). The paper (Guo et al. 2026) was read from its abstract only (issue 2).

Value: TP-4, not `Trivial` (the raw last value loses in 9 of 9 windows); TP-9 holds (220-345 plots with reed per
window); MET-2 holds; TP-1 open (no tuned results; an early-stopped LightGBM did not widen the margin). Quality:
CLEAN-1 (soil joined per variable, species count without bare ground and water), CLEAN-11 (four impossible values set
missing), CLEAN-22 (three heights shipped, the other drops named) fixed; SPLIT-20 note on the 2017 window.

Weighed: a state program's own target at its own stations +; honest evaluation +; approximate fit -; most of the skill
is persistence -.

Left for Andrej: issue 2, moot with the `No`. The numbers are untuned (the panel's random forest and LightGBM), measured
again on the changed definition; those marked "panel" were not re-run.

**Main points:** TP-10 stays as written (2026-11-02), so the record is `No` (`Time-series (Forecasting)`) and the
folder leaves with your verdict; the Guo et al. PDF (issue 2) is moot with it.

**Record fields that disagree with the definition:**

- `year`: record `2006`, definition `2026`.
- `required_split`: record `Grouped (NON-IID)`, definition `Temporal (NON-IID)`.

**Issues for Andrej:**

2. **Can you get the Guo et al. (2026) PDF?** The paper (Ecological Applications, doi:10.1002/eap.70246) anchors the
   use case, the fallback metric and the lineage note, but every claim from it rests on the USGS abstract: Wiley
   answered 403 twice and no free copy turned up. If its text holds a per-plot model or a score, the metric and the use
   case reopen (MET-5).
   * Rule: PROV-16 and PROV-17 (Must): a paywalled paper that matters is asked for; until then its claims are marked
     unverified.
   * Implemented: the claims are marked "read from the USGS abstract only" and quoted verbatim.
   * Alternative: you send the PDF and we check the use case, the metric and the lineage note against its text. Cost:
     a re-read, and a rebuild only if it holds a per-plot score. Moot if issue 1 ends in (b).

   Recommendation: send the PDF. Decision: send it, or accept the abstract-only marks?

**Review panel:** don't ship under TP-10 as written; ship after changes only if Andrej amends TP-10 to the per-station
reading (issue 1) (mediator). Claim audit: 44 claims, 32 hold, 6 refuted (TP-10 leg 1, now issue 1; the use case against
RMSE, fixed; four slips in quotes, counts and the record's range wording, fixed in the definition, the record's two at
hand-over), 3 refuted in part (fixed), 1 superseded by a measurement (the publication gap), the record's fields stale
(field rows above), 1 tested in part (the hash of an older copy). Blind review: would include with changes; its main
concerns were the soil join's missingness (fixed) and that about 90% of the squared error sits on the plots that already
hold reed. Debate: agreed on the temporal split, no leak beyond the soil timing (lagged), the zeros kept, `rmse` with
the use case reworded, the dense-stand flag and the cleaning; disputed: which forecast is TP-10's bar (issue 1).

<details><summary>Mediator</summary>

**Mediator: crms_phragmites_cover (2026-11-01)**

**Recommendation**

```text
Verdict: don't ship under TP-10 as written; ship after changes only if Andrej amends TP-10 to the per-station
  reading (issue 1); otherwise No (Time-series (Forecasting)), after first testing the site hydrology if he wants.
Validity: SEL-10/SEL-11 via TP-10 leg 1 (Must) not met as written: the random forest is 1.6% below a three-number
  persistence of the station's own cover (6 of 9 windows, mean gain 1.5 SE over windows; LightGBM ties it); met
  against unfitted per-station forecasts (6.4%, 9 of 9) and the raw last value (10.5%, 9 of 9). Leg 2 holds (wording
  fixed). USE-1/MET-1 triggered, fixed (use case reworded to what RMSE scores; rmse kept, MET-7). USE-3 triggered,
  fixed (prediction point before the season). USE-6 triggered, fixed (dense-stand flag and estimate). LEAK-10 weak
  (soil cores used before CIMS posts them), fixed by a lag (LEAK-7). SPLIT-1/3, USE-10 hold (temporal). SPLIT-9/10
  hold (no gap, measured). PROV holds for the data (target rebuilt on 99.98% of rows); PROV-16/17 open for the paper.
Value: TP-4 not Trivial (raw last value loses 9 of 9); TP-9 holds (220-345 positive rows per window); MET-2 holds;
  TP-1 open (no tuned results; a stronger LightGBM did not widen the margin).
Quality: CLEAN-1 (soil joined per variable, species count), CLEAN-11 (four impossible values), CLEAN-22 (drops named):
  fixed. SPLIT-20 note on the 2017 window.
Weighed: a state program's own target at its own stations +; honest evaluation +; approximate fit -; most of the
  skill is last season's cover -.
For the curator: issue 1, the TP-10 comparator (an amendment of a Must, or retire); issue 2, the Guo et al. PDF.
```

The panel agrees on everything except one reading. Which forecast is TP-10's bar decides scope, and nothing ranked
above SEL-10 lifts it. The rule's text and its cases support the critic's reading: the bar is the best forecast
built only from the station's own series, and fitting a few parameters of it on the training seasons does not take it
out of that class. Under that reading leg 1 is not "clearly" met. The per-station reading that keeps the dataset is an
amendment of a Must, so it is Andrej's decision, not an exception.

No experiment was run. Four independent runs (claim auditor, precedent checker, advocate, critic) agree on every
comparator within 0.02 RMSE; the dispute is the reading, not a number.

**Agreed facts**

* Source and rows: CPRA's CIMS export, 594,288 species records of 75,418 visits at 4,619 stations of 401 sites
  (2006-07 to 2026-07). 69,161 rows (4,099 stations, 394 sites, 2007-2025). The blind reviewer rebuilt the target from
  the raw CSV: 69,150 rows match, the other 11 are trace codes set to 0.5.
* Zeros: 94.1%; 95.9% of them at stations that never had reed in or near the plot. They are absence from habitat
  inside the species' range, not outside it (claim 42). Andrej's policy 2 (2026-10-30) keeps them; nobody asks to cut
  them now.
* No leak beyond the soil timing. Every feature comes from before season Y; no exact copies cross the split; the
  missingness indicators move R^2 by -0.001 to -0.007.
* Regime: temporal. 97.9-100% of each window's test rows are at a station seen in training. Grouped by site, a
  cold-start mapping keeps 1-6% of the variance (R^2 0.01-0.06).
* Publication timing: season Y-1 is 91-100% in CIMS by January-June of Y (Wayback copies 2021-2025), so no gap is
  needed. Soil cores reach CIMS 1 to 2.5 years after sampling; 15.2% of test rows use cores of Y-1. A lag to Y-3
  costs nothing (RMSE 7.050 against 7.054).
* Dense-stand visits: 633 (2012-2016) have no measured cover in today's download. In the November 2016 download 518
  of them were in-plot data (mean 98.7%); by April 2021 the program had moved them to "Out" with empty cover. "The
  estimates overstate" is not shown: the nearest earlier measurement averages 73.9%, and 2017 follows the roseau cane
  scale die-back. In the 2017 window, 99 re-entered plots carry about two thirds of the squared error.
* What RMSE scores: the 7.8% of test rows with reed at the last visit carry 90.8-92.6% of the squared error;
  colonisations about 7%. 34.9% of the test rows with reed lie in the Bird's Foot Delta, where cover falls and the
  reed is protected. Plot RMSE ranks eight models as site-year RMSE does (Kendall tau 0.93). No source metric exists
  in the abstract, the CRMS pages or the metadata.
* TP-4: the raw carried-forward cover loses to the models in 9 of 9 windows. TP-9: 220-345 positive rows per window.
* The comparator ladder (untuned RF and LightGBM; RMSE averaged over the nine windows; RF 6.930, LightGBM 7.025):

  | bar | RMSE | RF lower by | RF windows won | RF above 2 SE / below -2 SE |
  |---|---|---|---|---|
  | raw last value | 7.746 | 10.5% | 9 of 9 | 8 / 0 |
  | last value + training mean drift (telemonitoring's form) | 7.747 | 10.5% | 9 of 9 | 8 / 0 |
  | pooled linear shrinkage of the last value (2 numbers) | 7.512 | 7.7% | 9 of 9 | 6 / 0 |
  | best of nine per-station forecasts (EWMA 0.7, picked on the test windows) | 7.401 | 6.4% | 9 of 9 | 3 / 0 |
  | two-regime persistence: 0.08 where the last cover was 0, else 16 + 0.62 x last (3 numbers) | 7.045 | 1.6% | 6 of 9 | 3 / 0 |
  | isotonic curve of the last value | 7.042 | 1.6% | 5 of 9 | 3 / 0 |

  Over the windows, the RF's mean MSE gain is 3.4 SE against the EWMA, 1.5 SE against the two-regime rule and 1.3 SE
  against the isotonic curve. LightGBM is 0.25% below the isotonic curve (4 of 9, one window below -2 SE). The RF
  loses the 2024 window to both fitted curves. An early-stopped LightGBM (3 seeds) scores 7.05-7.13. The three-number
  rule reaches 86% of the RF's gain over the raw last value; its parameters barely move between windows (slope
  0.62-0.68, intercept 15.4-17.6).
* Cleaning: the soil join blanks known pH and salinity (59% coverage, 96% joined per variable); the species count
  includes "Bare Ground" and "Water"; one herb height (1,219.2 cm) and three porewater salinities (90, 71, 57 ppt)
  contradict their own records; some drops are not named. Blank shrub and tree covers mean "not recorded" and stay
  missing. None of these moves the score.
* Record: year 2026 (PROV-9), required split Temporal, and the marker `No Good Target / Scientific Discovery`
  contradicts the approximate fit. Guo et al. 2026 was read from the USGS abstract only; the quote in the notes is not
  verbatim and "native" should read "long-established noninvasive". The three warnings are acceptable.

**Changes to make now (no decision needed)**

1. TP-10 bullet (EV-7, TP-10): replace "the first leg of TP-10 ... holds" with the ladder above and state that leg 1
   holds against unfitted per-station forecasts and not clearly against a fitted curve of the last value (issue 1).
   Leg 2 wording: "the last observation and trailing summaries of the station's series" (claim 19). Re-run the
   ladder on the changed definition.
2. Use case and fit (USE-1, MET-1, Must; MET-7): `use_case` becomes "Between seasons, a CPRA manager forecasts each
   monitored station's reed cover at next summer's survey, averaged to sites, to track spread in the western and
   central basins and die-back in the delta." `fit_reason` adds that the delta's reed is protected, not controlled,
   and that plot and site-year rankings agree (tau 0.93). Keep `rmse`.
3. Prediction point (USE-3): "before each season, once the last season is in CIMS (it arrives over the winter)" in
   the question, the use case and the first bullet; `known` says the visit's scheduled date, not the exact day.
4. Dense-stand history (USE-6, Must): a flag for an unmeasured dense-stand visit since the latest measured one, with
   the crew's estimate as its own column; those visits counted in `site_share_phragmites_nearby`; still out of the
   rows and of `previous_phragmites_cover`. Rest the drop on the program's own revision (in-plot in 2016, "Out" by
   2021) and its words ("may not be representative"); remove "the estimates overstate" (EV-6); name the scale
   die-back; update decision 3's text.
5. Soil (LEAK-10 weak, remedy LEAK-7; CLEAN-1): cores sampled three seasons back or earlier, one as-of join per soil
   column; correct the coverage figures. This follows rain_in_australia's guard (inputs from other rows only where
   known by then). CPRA staff seeing lab results earlier is unsourced (EV-2), so the lag is the safe default.
6. Splits comment (SPLIT-10, SPLIT-20, SPLIT-21): replace "not checked" with the measured no-gap finding; add the 2017
   re-entry note; keep the nine windows. "Labels unchanged since first publication" holds for 2019-2023, not for the
   2012-2016 dense-stand visits (EV-7).
7. Cleaning (CLEAN-1, CLEAN-11, CLEAN-22): species count without "Bare Ground" and "Water"; the herb height and the
   three porewater salinities set missing; name each dropped column with its reason (Braun-Blanquet rank: a recoding
   of the cover; Group: empty), or ship the previous tree, shrub and carpet heights.
8. Wording (EV-2, EV-7, PROV-16): the Guo et al. abstract quoted verbatim, still marked "abstract only";
   "long-established noninvasive"; 60 station-years with two visits, not 63; `visits_with_phragmites_before` counts
   station-years.
9. `download_description`: the SHA-256 of the porewater and soil files next to the vegetation one (CIMS revises past
   records).
10. Warnings accepted with their reasons: `meta_time_horizon_mismatch` (one survey season per window; zillow_prize,
    perth_house_prices), `meta_license_unknown` (CPRA disclaimer only; diabetes_3, mobile_churn),
    `task_target_value_dominant` (real absence; Andrej, policy 2 of 2026-10-30).
11. Record (no mark needed): remove the marker `No Good Target / Scientific Discovery` (USE-8, fit approximate;
    thyroid_discordant, ghcn_daily_precipitation), replaced by `Time-series (Forecasting)` only if issue 1 ends in
    `No`; add the porewater and soil zips to `source_links`; "4,476" to 4,488; zeros as absence from habitat inside
    the range. The year and `required_split` go to the field rows; the tag `Non-IID (Temporal)` follows
    `required_split` if Andrej updates it.

**Changes that need the curator**

1. TP-10 leg 1: which forecast is the bar (P2 via SEL-10/SEL-11, Must). Problem: a panel of yearly cover per station
   is in scope only if a model on the features clearly beats what the series itself forecasts. The features hold
   last season's cover; a three-number shrinkage of it comes within 1.6% of the random forest. Effect: under the
   fitted bar the benchmark ranks methods by a 1-2% edge over persistence, which the RF loses in the 2024 window and
   LightGBM does not have.
   * Advocate's best evidence: SEL-11 and leg 1 say "naive profile" / "naive forecast", and the Methods name "its
     last value". Against every unfitted forecast of the station's own series the RF is 6.4% lower, 9 of 9, 3.4 SE
     over windows. On telemonitoring_parkinsons' own bar (carry + mean drift) crms is 10.5% ahead, the opposite of
     that case.
   * Critic's best evidence: the 2026-10-26 sentence "the model must clearly beat the forecasts built from the series
     itself" governs when the last observation is kept, as here. The three-number rule reads only the station's last
     value, with stable parameters; the RF beats it by 1.6% at 1.5 SE, LightGBM ties, and a stronger model does not
     help. rain_in_australia's bar was fitted.
   * Decision: (a) amend TP-10 to the per-station reading and ship after the changes; (b) keep TP-10 as applied and
     retire as `No` + `Time-series (Forecasting)`; (c) first add CRMS site hydrology, elevation and basin and re-test
     against the fitted bar, then (b) if the margin stays small. Recommendation: (c), then (b). Whatever is chosen,
     the amendment should say what "clearly" means (for example a paired gain above 2 SE over the windows).
2. The Guo et al. 2026 PDF (P5, PROV-17, Must; low effect). Every claim from the paper rests on the abstract (Wiley
   answered 403 twice). If its text holds a per-plot model or a score, MET-5 reopens the metric and the use case.
   Decision: send the PDF, or accept the abstract-only marks.

The year and `required_split` (Grouped to Temporal) are field rows for the review file, not issues.

**Disputed points**

1. TP-10 leg 1 comparator. Advocate: SEL-11 (Part 1, Must) names "each entity's naive profile" and Part 1 wins over a
   sentence in Part 6; the isotonic curve is learning across entities, the "tabular forecasting" TP-10 admits.
   Critic: TP-10's amended sentence names "the forecasts built from the series itself", and a three-number persistence
   is such a forecast. Ruling, by the text and the cases:
   * There is no conflict between parts. SEL-11 says a panel "is in scope when it passes TP-10" and hands the test to
     it. Its gloss also says "the source's top solutions used no lagged target", the wording from before the
     amendments; read as governing it would fail crms outright, so neither side can use it as the operative text.
   * The 2026-10-26 sentence ("Leg 1 then carries the test") applies when the last observation stays in the features.
     Then any model can learn a curve of that value, and beating the raw value shows only that. If the sentence meant
     the same as "each entity's naive forecast" it would add nothing.
   * rain_in_australia, the case behind the sentence, measured leg 1 against forecasts fitted across locations on
     each location's own series: its split audit used LightGBM on the station's rain series, station and calendar
     (0.743), and its Cases row lists "the best forecast from the location's own rain series 0.752 (a regression of
     the amount with a > 1 mm rule)". Its record calls that "a naive forecast". So in this rulebook "naive" has not
     excluded a fitted forecast, and the advocate's point that the record does not say whether it was fitted across
     locations is answered by the split audit. Persistence (0.661) was the weakest comparator there, not the bar.
   * telemonitoring_parkinsons (Lennart, 2026-10-02) used a pooled parameter (the training subjects' mean drift) in
     its bar and judged 2.3% over it as "how little they lose to a constant".
   * The advocate's other supports answer other questions. Colonisation AUC (0.956 against 0.896) is not the declared
     metric, and TP-10 measures leg 1 "by the task's declared metric". TP-4 decides the `Trivial` marker, not scope.
     The forest_fires row settles P4 against P6, not a P2 Must (principles, step 4). P3 informs P2, but here the use
     case is itself "forecast next season's cover at known stations", the situation SEL-10 describes, so it confirms
     the rule applies.
   * g_research_crypto_forecasting (Lennart, 2026-10-22) points the advocate's way in one respect: a model on
     trailing summaries of the series passed against the coin's mean. It kept no lag of the target column, so the
     2026-10-26 condition did not apply there.

   Result: the critic's reading is the rule as written; under it leg 1 is not clearly met (1.6%, 1.3-1.5 SE over
   windows, a tie for LightGBM, below telemonitoring's retired 2.3%). Keeping crms needs an amendment, so it is issue
   1. The remedy ladder offers one definition fix before exclusion, the site hydrology (option (c)); re-targeting to
   colonisation (about 25 new plots per window, and a three-term field-sheet rule reaches AUC 0.951 against 0.964)
   and a split by site (1-6% of the variance, against USE-10) do not fix it.
2. Whether the dense-stand drop inflates the margin. Both are right in part: it matters against the fitted bar only.
   Without 2017 the RF is 1.2% below the isotonic curve (4 of 8) and 5.0% below the EWMA (8 of 8). Settled as fact;
   the 2017 note goes into the splits comment, and the nine windows stay (SPLIT-21).
3. Whether PROV holds. For the data, yes (target rebuilt, counts confirmed, the drop follows the program's own
   revision and CLEAN-15). For the paper, PROV-16 and PROV-17 stay open: the work goes on with the claims marked
   unverified, and the PDF is asked for (issue 2).
4. "Labels unchanged since first publication". The critic's narrowing holds (EV-7): true for 2019-2023, not for the
   2012-2016 dense-stand visits. Written that way (change 6).
5. telemonitoring_parkinsons as the like case. On its own bar crms is the opposite case (10.5% against 2.3%); its
   reason applies to crms only if the bar is the fitted curve. So the precedent follows from point 1 and does not
   decide it alone.

**Consistency with precedent**

* Temporal over the record's Grouped: follows the USE-10 cases and the Tensions row of Lennart, 2026-10-12. The
  record's Grouped is an AI triage value (commit 137c1694); the measured stage supersedes it.
* Dense-stand rows dropped: CLEAN-15 and the eryhemato row (no target of our own invention). Their history kept as a
  flag and estimate: USE-6 (brazilian_ecommerce, bias_correction).
* Soil lag: follows rain_in_australia's guard (precedent checker, prompt 2, option b). Measured no gap: follows
  melbourne_housing_market, so no SPLIT-10 exception (prompt 3, option a). Both prompts are closed.
* Fallback rmse with the use case reworded: churn_telco_south_asia, melbourne_housing_market; MET-7 and the Tensions
  row on metrics (no invented threshold or k).
* Year 2026: PROV-9, sf_permit_time, rain_in_australia (Lennart, 2026-10-26).
* Marker removal: thyroid_discordant (Lennart, 2026-10-22), ghcn_daily_precipitation (Andrej, 2026-10-30). Decide
  alike in the same-run records that carry the marker open (boreal_postfire_lichen_biomass,
  pennsylvania_oak_hickory_regeneration_experiment, noaa_storm_events_damage,
  rand_health_insurance_experiment_doctor_visits).
* TP-10 (prompt 1): option (b) follows rain_in_australia's bar and telemonitoring's margin. Option (a) reopens neither
  (telemonitoring stays retired on its own bar and its grouped failure; rain passes either way) but narrows the
  sentence Lennart wrote on 2026-10-26, so it is an amendment. walmart_sales_in_stormy_weather (same run, AI draft)
  keeps no lag of its target, so the conditional sentence does not apply and its bar stands under either reading.
  nantucket_sound (same run) went grouped when leg 1 failed; that route does not transfer, since crms's grouped task
  is nearly empty and the use case is known stations. Andrej's calls in this family (walmart, metro_manila) defer
  TP-10 to the measured leg; the ladder is that measurement. TP-10 has no exceptions; none is added.

</details>

<details><summary>Claim audit</summary>

**Claim auditor: crms_phragmites_cover (2026-11-01)**

**Verdict.** Most of the definition's facts hold on the data: counts, how the target is built, the trace codes, the drop counts, coverage, model numbers, the windows and the metric's computability. One claim that carries the scope decision is refuted. "The first leg of TP-10 holds" was measured against the raw carried-forward cover only. TP-10 as amended on 2026-10-26 asks for more ("the model must clearly beat the forecasts built from the series itself"; rain_in_australia compared against a forecast fitted on the location's own series). Against an isotonic curve of the previous reed cover, fitted on each training side, the random forest on all features is 1.5% lower in RMSE. It wins 5 of 9 windows, and by more than 2 paired SE in only 3. That puts SEL-10 back in front of the curator (P2, Must). Second, the use case says "flag emerging hotspots", but RMSE puts 93% of its weight on plots that already hold reed (USE-1, MET-1). The rest is wording, and record fields that have gone stale.

All numbers below are mine unless marked otherwise. They come from the definition rebuilt with `dataset_io.definition(...).to_container()` on 2026-11-01 (checksum v2:6c6da396...), the raw CIMS files of the pinned download, and untuned models: RF with 300 trees, min_samples_leaf 5, max_features 0.5; LightGBM with 400 trees, 3 seeds; settings as in the builder's TP-10 check. Scripts and logs are in the run folder.

**Claims table**

| # | Claim | Source | Test | Result | Evidence | Rule |
|---|---|---|---|---|---|---|
| 1 | Plot is 4 m^2 (question); "the plot size (4 m^2 everywhere)" dropped | task_summary.question; comments "Dropped" | `Plot Size (m2)` over the raw records | holds | 4.00 in all 594,288 records and all 75,418 visits | USE-5 |
| 2 | Raw table: 594,288 records, 75,418 visits, 4,619 stations, 401 sites, July 2006 to July 2026 | comments, first line | recount from the raw CSV | holds | 594,288 / 75,418 / 4,619 / 401; 2006-07-31 to 2026-07-30 | PROV-13 |
| 3 | Rows: 69,161; 4,099 stations at 394 sites; first visit leaves (USE-7) | task_summary.row; comments "Row" | measured visits up to 2025 that have an earlier measured year, recounted from raw ids | holds | 69,161 rows, 4,099 stations, 394 sites | USE-7 |
| 4 | "The 63 station-years with two visits keep both, with the same history" | comments "Row" | station-years with two shipped rows | refuted (trivial) | 60 among the shipped rows; 63 among all kept visits (3 fall in a station's first year and leave) | EV-7 |
| 5 | Target = summed in-plot cover of the names starting "Phragmites australis" (species + 2 subspecies, at most 1 row per visit) | comments "Target" | names, rows per visit, In/Both cover missing | holds | 7,049 + 13 (ssp. australis) + 2 (ssp. berlandieri) rows, no other Phragmites name; at most 1 reed row per visit; 0 In/Both reed rows without cover | USE-5 |
| 6 | "<1" (9) and "Solitary" (3) are below the 1% resolution, set to 0.5 | comments "Target" | Braun-Blanquet rank of every trace code | holds | all 6,081 "<1" are rank "+", all 1,431 "Solitary" rank "r"; 9 and 3 among reed | CLEAN |
| 7 | "Out" rows carry no cover by the metadata (quoted) | comments "Target" | metadata XML, and Out rows' cover | holds | quote verbatim in `Herbaceous_Marsh_Veg.xml` (In_Out attrdef); all 2,576 reed Out rows have empty cover | USE-5 |
| 8 | Zero in 94%, "mostly at stations where it was never recorded" | task_summary.predicted; comments "Zeros" | frame | holds | 94.08% zeros; 95.9% of zeros at stations that never had reed in or near the plot | - |
| 9 | 56,295 rows never near reed, 13 with reed (0.02%); 18.7% of 1,709 when reed grew near the plot | comments "Zeros"; decision 1 | decision table, builder's number check | holds | reproduced by the definition's own decision table | - |
| 10 | Dense-stand drop: 633 visits, 2012-2016, 171 stations, 32 sites; 584 at 100%, 48 at 70-95%, 1 at 10% | comments "Dropped, the plots..."; changes | regex on the raw comments | holds | 633 (95/122/120/135/161 by year); 171 stations, 32 sites; 100%: 584; 90: 21, 80: 15, 70: 6, 85: 3, 95: 3; 10: 1; every visit that mentions "dense stand" is parsed | USE-5 |
| 11 | "The estimates overstate: the same stations measured 57% on average in 2011 and 47% in 2017 (medians 70% and 50%)" | comments "Dropped, the plots..."; decision 3 | each estimated visit against the same station's nearest measured visit; visit comments by year | the numbers hold, the inference is not shown | Per estimated visit, the nearest earlier measurement averages 73.9% (median 80; 37% at 90% or more), not 57%. The 2017 values are confounded: "scale present" (roseau cane scale) appears in 201 visit comments in 2017 and in none in 2006-2016. 72 of the 171 stations were never measured again and were replaced by 105 new stations at the same sites | EV-6 (Should) |
| 12 | The cost: reed share 3.2-3.6% in 2012-2016, 6.0-7.3% with estimates, 3.3-5.7% in 2007-2011, 5.9-9.2% from 2017 | comments "Dropped, the plots..." | season table, adding the estimated visits back | holds | e.g. 2012: (134 + 95) / 3,814 = 6.0%; 2016: (117 + 161) / 3,825 = 7.3% | - |
| 13 | 325 unmeasured visits without an estimate dropped; 2,586 total-cover-0 visits kept | comments | raw | holds | 958 unmeasured − 633 = 325; 2,586 (2,542 without species), builder's verify | USE-7 |
| 14 | The 677 visits of 2026 (June-July only) dropped | comments | raw months | holds | 2026: June 187, July 490 | LEAK-24 |
| 15 | Porewater = mean of 10 and 30 cm at the station that day; 74% of rows | comments "Features" | hydro depths, join | holds | depths 0.328 ft (168,377) and 0.984 ft (172,418); 54,706 of 75,418 visits have a same-day reading at the vegetation station; 73.6% of rows | CLEAN |
| 16 | Soil: top 24 cm; N and P in 15% of rows, pH in 59% | comments "Soil" | depth strings; README | holds | "0 to 4"…"20 to 24" kept, "24 to 32" left out; 14.6% / 14.5% / 58.9% | CLEAN |
| 17 | RF 6.93, LGB 7.02 (7.08 without env, 7.88 without station reed history), carried forward 7.75, train mean 13.9; RF 9/9, LGB 8/9, 10% | comments "On the nine shipped windows" | rerun on the shipped splits | holds (numbers) | RF 6.930, LGB 7.025, carried forward 7.746; RF wins 9/9, mean relative RMSE 0.896 | EV-8 |
| 18 | "The first leg of TP-10 … holds" | comments "On the nine shipped windows"; builder | full models against forecasts built from the station's own reed series (TP-10 as amended 2026-10-26; rain_in_australia) | **refuted** | isotonic curve of `previous_phragmites_cover`, fitted per training side: RMSE 7.042. RF 6.930 wins 5/9 windows (mean relative 0.985); paired MSE gain > 2 SE in 3/9 (2017, 2020, 2022), mean gain 1.55 with SE 1.21 over windows. LightGBM 7.025 wins 4/9 (relative 1.000). RF on the 4 history columns alone: 7.29 | TP-10, SEL-10 (Must) |
| 19 | "Every feature is known at the prediction point, and the only lag of the target is its last observation" | comments, same bullet | read `_clean` | holds in substance, wording refuted | `highest_phragmites_cover_before` (running maximum) and `visits_with_phragmites_before` (running count) summarise the target series, and `site_phragmites_cover_mean` averages the station's own last value with its neighbours'. TP-10 allows trailing summaries, so leg 2 holds | TP-10 |
| 20 | Previous cover alone, fitted, reaches 98% of the best family's skill; depth-2 tree 0.753 against 0.746; "not `Trivial` by TP-4" since the raw carried-forward value loses | comments "Note: the previous reed cover…" | probes; per window: fitted curve against the models | holds by the letter of TP-4 | Raw value loses 9/9. The fitted curve beats RF in 4/9 and LightGBM in 5/9 windows, so it does not match the models in every window. Against tuned methods: not run | TP-4, TP-1 |
| 21 | Sample type Transect, vegetation type Natural in 99.9% | comments "Dropped" | raw shares | holds | Transect 0.999, Natural 1.000 | CLEAN |
| 22 | CRMS does not tell the invasive lineage from the native ones | comments note; fit_reason | USGS abstract; raw names | holds | Abstract: "...long-established noninvasive and (since ~2000) invasive European P. australis lineages, but CRMS cannot distinguish them". 15 of 7,064 reed records do carry a subspecies (13 ssp. australis, 2 ssp. berlandieri). "Native" should read "long-established noninvasive" | PROV-16 |
| 23 | Guo et al. 2026: 2006-2023, 390 sites, MRD falling, four basins rising, linked to soil nutrients, pH, salinity; no per-plot prediction | comments "Prediction point"; metric reason | USGS page (publisher 403 again) | holds (abstract only) | 2006-2023, 390 sites, nine basins; increases in Calcasieu-Sabine, Mermentau, Teche-Vermilion, Terrebonne; no model or forecast | PROV-16, EV-7 |
| 24 | The quote "cover trends, native plant cover, and soil and pore-water indicators" | comments "Prediction point" | USGS page wording | **refuted (not verbatim)** | The page reads "integrates Phragmites cover trends (expanding/stable/declining), concurrently measured native plant cover, and key soil and pore-water indicators to flag emerging hotspots and prioritize adaptive management" | EV-2, PROV-16 |
| 25 | Nine windows 2017-2025, 3,578-3,830 rows, the 2017 window trains on 51% | splits_comment | splits | holds | 3,578-3,830; 35,169 / 69,161 = 50.85% | SPLIT-14 |
| 26 | "One season is the horizon: the network surveys once a year" | splits_comment | days since the previous visit; months | holds | median 364 days; 96.7% of rows in June-September; no visits in January-April | SPLIT-1 |
| 27 | "No gap … how soon a season's data reach CIMS was not checked" | splits_comment | newest dates in the pinned downloads | checked; supports no gap | Vegetation zip of 2026-10-25 ends 2026-07-30, with no August visits (August holds 41% of a season's visits). Porewater of 2026-11-01 ends 2026-09-09. A visit reaches CIMS within about 3 months, so the season is public long before the next one starts in May-June | SPLIT-10 |
| 28 | Stations recur across windows on purpose (known stations) | splits_comment | design | holds | every row has a station history by construction | USE-10, SPLIT-3 |
| 29 | Implied: each window is a regular test one season ahead | split design | the 2017 window's error by gap | partly refuted | 86 rows of 2017 (2.3%) have their previous measured visit more than 2 years back (84 with reed, mostly the dense-stand stations). They carry 71.6% of the window's carried-forward squared error, so this window largely measures the gap the drop leaves, plus the scale die-back. In 2024, 84 such rows (the 2023 "no access" year) carry 15.2% | SPLIT-1, USE-5 |
| 30 | Implied: no copy across the split | - | leak probe 5 | holds | 0.0% exact copies, with and without the datetime column | LEAK-16 |
| 31 | Implied: every feature is known at the prediction point ("end of a survey season") | task_summary.known | read the joins | holds; the wording is loose | All history comes from years before Y. The site porewater mean and max use the whole previous calendar year (8% of readings fall in Nov-Dec, after the season ends). That is before the target, so it is harmless, but "before the next season" is the exact point | LEAK-10 |
| 32 | Metric: fallback `rmse`; no source metric | `Metric.fallback` reason | Wiley full text (403 on 2026-11-01), USGS abstract, CRMS home page, metadata XML | holds (full text unread) | no metric, model or score in the abstract, CRMS pages or metadata | MET-1, MET-11 |
| 33 | MET-2: computable on every test fold | metric | `scorer(container)` on each fold, dummy predictions | holds | train mean scored 11.92-17.39; zero 12.20-17.85; 220-345 positive rows and 93-193 rows of 50% or more per window | MET-2 |
| 34 | MET-1: the metric scores the use case "ranks … to flag emerging hotspots" | task_summary.use_case vs metric | where the squared error sits | **refuted as worded** | 7.8% of test rows already had reed in the plot. They carry 92.6% of the carried-forward and 90.8% of the RF's squared error. Colonisations (no reed at the last visit, reed now) are 18-32 rows per window, and RF's MSE gain on them over the fitted curve is about 0, although RF ranks them at AUC 0.956 (series-only RF 0.896) | MET-1, USE-1 |
| 35 | MET-3: percent cover, identity transform | metric spec | spec | holds | `target_transform='identity'` | MET-3 |
| 36 | Warning `meta_time_horizon_mismatch`: one season per window | builder | window spans | holds, accept | the windows span 99-203 days of one season | SPLIT-1 |
| 37 | Warning `meta_license_unknown`: only a disclaimer | builder | XML `useLimit`, `othConsts`; RESTORE note | holds, accept | disclaimer and "originator makes no claims as to the data's suitability"; no licence | EV-4 |
| 38 | Warning `task_target_value_dominant`: zero inflation, real absence | builder | claim 8 | holds, accept | 95.9% of zeros at stations that never had reed in or near the plot | - |
| 39 | Record: "Approximately 390 sites", "designed to monitor the effectiveness of restoration actions at multiple spatial scales" | record screening | lacoast.gov/crms/Home.aspx | holds | both phrases on the page | PROV-16 |
| 40 | Record: 97 of 401 sites ever have reed; 80% of zero visits at sites that never had it | record | raw | holds | 97 of 401; 79.8% | - |
| 41 | Record: "4,476 visits with cover" | record CC paragraph | raw | refuted (trivial) | 4,488; the 12 trace-code visits were missed | EV-7 |
| 42 | Record: most zeros at sites "outside its range" / "outside the species' range" | record screening and risks | site longitudes and marsh types | **refuted** | The 304 sites without reed span longitudes −93.83 to −89.22, the 97 with reed −93.70 to −89.13. Visits at never-reed sites are 20.5% freshwater, 22.3% intermediate and 15.9% brackish marsh (24.3% saline, 17.0% swamp). This is absence from habitat inside the range, not outside it | EV-2 |
| 43 | Record fields: year 2006, `required_split` Grouped, marker `No Good Target / Scientific Discovery` with `Yes` | record front matter | definition, PROV-9, USE-10 | stale | The definition's 2026 follows PROV-9 (a growing source takes the year of the pinned snapshot). The use case (known stations, next season) implies temporal (USE-10, SPLIT-3). The marker contradicts the `Yes` | PROV-9, SPLIT-3 |
| 44 | Vegetation CSV of 2026-10-25 identical to a copy of 2026-10-18 (SHA-256 3cb2a0d3...19bd) | download_description; builder | hash of the CSV inside the zip re-downloaded 2026-10-30 | partly tested | the zip of 2026-10-30 holds the CSV stamped 2026-10-25 with SHA-256 3cb2a0d3...19bd, the same as the local file; no hash of the 2026-10-18 copy is kept | PROV |

**Refuted claims, ranked (validity first, Must first)**

1. **TP-10 leg 1 (claim 18; P2 scope, SEL-10 via TP-10, Must).** The definition shows the models beat the raw carried-forward cover by 10%, 9 of 9. TP-10 as amended on 2026-10-26 says that when the last observation is kept, "leg 1 then carries the test: the model must clearly beat the forecasts built from the series itself", and rain_in_australia compared against a forecast fitted on the location's own series (0.849 against 0.754). Here the forecast fitted on the station's own reed cover (an isotonic curve, no tuning) reaches 7.042 against RF 6.930. The margin is 1.5%, the RF wins 5 of 9 windows, and only 3 of 9 by 2 paired SE. LightGBM ties the curve (relative 1.000). A precedent with similar facts: telemonitoring_parkinsons was retired with a warm start 6.33 against 6.48 carried forward (2.3%). *What it changes:* the scope verdict, the builder's draft issue 1, now with the decisive number. *Mildest remedy:* the curator decides whether 1.5% and 5 of 9 "clearly beats". If not, re-target before excluding. Colonisation at stations without reed is where the features add something (RF AUC 0.956 against 0.896 for history only), but it has only 18-32 positives per window (TP-9 to check). Otherwise `No` + `Time-series (Forecasting)`. The decision should also be checked against tuned methods (TP-1).
2. **Use case against metric (claim 34; P3 USE-1 and P6 MET-1, Must).** The use case ranks stations "to flag emerging hotspots". RMSE scores something else: 92.6% of the naive's squared error and 90.8% of the RF's sits on the 7.8% of rows that already hold reed, and colonisations do not move it. *What it changes:* the use-case text, and it explains why claim 18 fails. *Mildest remedy:* reword the use case to what RMSE scores, for example "forecasts next season's reed cover at each monitored station, to plan control and monitoring effort". Keep the fallback: no source fixes a ranking metric, and MET-7 forbids inventing one. Only a re-target (remedy 1) would make "emerging" the task.
3. **The 2017 window (claim 29; P4 SPLIT-1, Should-level as a note).** The oldest window is dominated by 86 rows whose previous measured visit is 2011-2015. Behind them are the dense-stand drop and the roseau cane scale die-back. They hold 71.6% of its naive squared error, and 2017 carries the largest gain over carried forward (30.2 MSE units, builder; 5.0 over the fitted curve). *What it changes:* how far the mean margin can be read as one-season-ahead skill. Without 2017, RF against the fitted curve is 6.891 against 6.975 (1.2%). *Mildest remedy:* say so in `splits_comment` (or the dense-stand bullet). Dropping the window is not needed.
4. **"The estimates overstate" (claim 11; evidence, EV-6, Should).** Per estimated visit, the nearest earlier measurement is 73.9% on average (median 80, 37% at 90% or more). The 2017 values follow the scale outbreak (201 comments in 2017, none before). So the bias is circumstantial: stands too dense to enter may well be near 100%. *What it changes:* the stated reason for the drop, not the drop. All affected seasons train only, and the builder measured estimates as history as worse (2017 naive 8.86 to 10.39). *Mildest remedy:* rest the drop on the program's choice (cover fields left empty, estimated from outside "based on … previous year's data", "may not be representative"), quote the per-visit comparison, and name the scale die-back.
5. **Leg 2 wording (claim 19; TP-10).** "The only lag of the target is its last observation" is wrong: there are also a running maximum, a running count and a site mean that includes the station. They are allowed as trailing summaries. *Mildest remedy:* reword ("the last observation and trailing summaries of the station's series").
6. **Quotes and small numbers (claims 24, 22, 4, 41; EV-2, EV-7).** The Guo et al. phrase in quotation marks is condensed, not verbatim. "Native" should be "long-established noninvasive", and the data does carry 15 subspecies records. Two-visit station-years are 60, not 63, among the rows. The record's 4,476 should be 4,488. *Mildest remedy:* fix the wording.
7. **Record screening (claims 42, 43).** "Outside the species' range" is refuted by the site longitudes and marsh types. The record's year, `required_split` and marker are stale against the definition. *Mildest remedy:* update the record (the builder's draft issue 7) and reword the zero mechanism as absence from habitat the reed has not colonised.

**Untested, and why**

* The Guo et al. full text (MET-1, PROV-16): Wiley answered 403 again on 2026-11-01 and the search found no free PDF. Every Guo statement rests on the USGS abstract and is marked so in the definition.
* TP-4 and TP-1 against tuned methods: no tuned results exist for this dataset yet. The untuned picture is mixed by window (claim 20).
* The SHA-256 of the 2026-10-18 copy: no hash of it is kept (claim 44).
* "2,504 stations change type" and the 2,586 / 2,542 total-cover-0 visits: the builder's number check counted these and I did not rerun them.

</details>

<details><summary>Column audit</summary>

**Column audit: crms_phragmites_cover (column-auditor, 2026-11-01)**

**Verdict:** no leak. Every one of the 30 features is known at the prediction point (the end of season Y-1; in practice
the calendar boundary of the test window, since next season's visits start in May). There are four cheap cleaning fixes,
none of which moves the score, and one question that belongs with decision 3.

```text
Verdict: ship after small cleaning changes.
Validity: LEAK-1/USE-3 holds (prediction point written); LEAK-2 sweep holds (every same-visit field and the
  Braun-Blanquet rank stay out); LEAK-10 holds for all 30 features (no post-outcome value; missingness carries no
  outcome: probe missing indicators -0.001 to -0.007 R^2); LEAK-34/USE-10: station history and position legitimate.
Quality: CLEAN-1 soil join blanks known pH and salinity (fix); CLEAN-1 species count counts "Bare Ground"/"Water"
  (fix); CLEAN-11 three impossible values (fix or note); CLEAN-22 undocumented drops (document or ship).
For the curator: the dense-stand visits' reed-nearby observation in the site shares (question, tied to decision 3).
```

Codebooks read: the FGDC metadata in the downloads (`Herbaceous_Marsh_Veg.xml`, `HydroMonthly.xml`,
`SoilProperties.xml`). The frame was loaded through `dataset_io.from_definition` (69,161 rows, 31 columns, rebuilt
from the raw files). Scripts and outputs are in the run folder.

**Column table**

| column | meaning (codebook) | known at prediction? | dtype and cleaning | verdict | rule |
|---|---|---|---|---|---|
| `visit_date` | date of the target visit ("Month, day, and year that the data were collected") | the year and the station's usual survey window are known; the exact day is set during the season. The day-of-year pattern follows which stations are visited when, not the outcome: visits before day 180 have reed in 10.7% (mean 4.12) against a previous-visit mean of 4.07; after day 240, 3.3% (1.48 against 1.23) | datetime64, time column and feature | fine | USE-3, LEAK-10 |
| `latitude` | station latitude, decimal degrees | yes: constant per station (4,098 coordinate pairs for 4,099 stations) | float64, 29.04-30.41, inside the metadata's bounding box | fine; it acts as a station key, which is legitimate for a known entity | LEAK-34, USE-10 |
| `longitude` | station longitude | yes, same | float64, -93.83 to -89.13 | fine | LEAK-34 |
| `days_since_previous_visit` | built: the visit date minus the latest earlier measured visit | yes. Gaps over 1,500 days (60 rows, all in 2017) are the dense-stand stations whose 2012-2016 visits were dropped: 84% have reed (mean 39%). Their cause (a plot in dense reed) is written in the 2016 comment, so the manager knows it | int64, 204-5,884 | fine. Dropping it together with the day of year: LightGBM RMSE 7.020 to 7.089 (paired SE 0.053; better without in 4 of 9 windows) | LEAK-37, USE-6 |
| `previous_community` | marsh type at the latest earlier visit (assigned per visit) | yes | category, 5 levels; 20 missing (258 raw records without a community) | fine | CLEAN-14 |
| `previous_cover_total` | % cover of all emergent vegetation | yes | float64, 0-100; "<1" set to 0.5 (9 raw values) | fine | CLEAN-10 |
| `previous_cover_herb` | herb layer cover | yes | float64, 3.5% missing, mostly plots with total cover 0 (median total 0 where herb is blank) | fine | CLEAN-10 |
| `previous_cover_shrub` | shrub layer cover | yes | float64, 88.7% missing; never 0 in the raw file (min 0.25), so blank means no layer or not recorded | fine: missing is the honest coding, no 0-fill | CLEAN-2 |
| `previous_cover_tree` | tree layer cover | yes | float64, 99% missing; blank even in 100% of swamp plots with 6-30 m dominant heights, so it means "not recorded", not 0 | fine | CLEAN-2 |
| `previous_cover_carpet` | carpet layer cover | yes | float64, 96.5% missing | fine | |
| `previous_height_dominant_cm` | average height of the dominant species | yes | float64, 0-3,048. Values over 600 cm are 152 swamp rows (trees) and 28 others. Feet entries converted (609.6 = 20 ft), one unit | fine | CLEAN-21 |
| `previous_height_herb_cm` | average herb layer height | yes | float64, one impossible value: 1,219.2 cm (40 ft) at a brackish plot whose dominant height is 61 cm (CRMS0684-V29, 2021; 1 frame row) | cleaning problem, minor | CLEAN-11 |
| `previous_species_count` | built: in-plot records of the species list | yes | int64, 0-30. It counts "Bare Ground" (1,634 in-plot records) and "Water" (36), all at 1,643 visits of 2006, when the program listed bare ground as a species (from 2009 it goes into the comment template). Inflated by 1 in 1,615 rows (2007-2008, training only); 26 plant-free plots read 1 | cleaning problem | CLEAN-1 |
| `previous_phragmites_cover` | the target at the latest earlier visit | yes | float64, coded like the target | fine; the core of the task | LEAK-34, USE-10 |
| `previous_phragmites_nearby` | reed recorded "Out" or "Both" at the latest visit | yes | category yes/no. "Both" is the code on 99.6% of in-plot records (357,214 of 358,555), so the flag is "yes" in 3,922 of 3,924 rows with reed in the plot; the new information is the 1,709 rows with reed outside only | fine (it reads "in or near the plot") | CLEAN-14 |
| `previous_porewater_salinity_ppt` | porewater salinity at the station on the latest visit's day (sipper probe, 10 and 30 cm) | yes | float64, 26.4% missing, and the missingness is not tied to the target (6.6% have reed when missing, 5.7% when present). One reading of 57.0 ppt (CRMS3650-V26, 2015-09-22) whose conductance implies about 5.8 ppt | fine; one reading minor | CLEAN-11 |
| `highest_phragmites_cover_before` | highest reed cover over the station's earlier years | yes | float64 | fine | LEAK-34 |
| `visits_with_phragmites_before` | number of earlier years with reed in the plot | yes | int64 count. It counts station-years (the latest visit of each year), not visits; 63 station-years have two visits | fine (wording) | CLEAN-14 |
| `phragmites_nearby_before` | reed ever recorded "Out" or "Both" | yes | category yes/no | fine | CLEAN-14 |
| `site_phragmites_cover_mean` | mean reed cover of the site's measured visits in the season of the latest visit | yes (a season before Y) | float64 | fine (leaves out the dense-stand visits, as decision 3 does) | LEAK-34 |
| `site_share_with_phragmites` | share of those visits with reed in the plot | yes | float64 | fine | |
| `site_share_phragmites_nearby` | share of those visits with reed in or near the plot | yes | float64. It loses the dense-stand visits, though all 633 recorded reed outside the plot, the one thing the crews observed directly | question (problem 5) | CLEAN-1 |
| `site_porewater_salinity_mean_ppt` | mean of all the site's porewater readings in that calendar year | yes (readings up to 31 December of an earlier year) | float64, 2.5% missing | fine | |
| `site_porewater_salinity_max_ppt` | highest of those readings | yes | float64. The maximum, 90 ppt, is one reading (CRMS0181-P01, 2021-06-17) whose conductance of 22,014 uS/cm implies about 12.6 ppt; another is 71 ppt at CRMS0647-P02 in 2008 (about 7.1 implied). 257 of 340,850 readings disagree with their own conductance by more than 2.5x | cleaning problem, minor | CLEAN-11 |
| `soil_ph` | dry soil pH, site mean of the top 24 cm, latest cores before the season | yes | float64, 3.97-7.56. pH was analysed only in the 2006-2015 cores, and the join takes all six soil values from the site's latest sampling year, so a later resampling (N, P, bulk density only) blanks a known pH. Coverage: 88-100% of rows in 2009-2018, 13% in 2019-2021, 1% in 2022-2025 | cleaning problem | CLEAN-1 |
| `soil_salinity_ppt` | soil salinity, same | yes | the same pattern as pH (59% coverage, 96% if each variable is joined on its own) | cleaning problem | CLEAN-1 |
| `soil_bulk_density` | g/cm3 | yes | float64; 92.5% coverage (95.7% joined per variable) | fine, same fix | CLEAN-1 |
| `soil_organic_matter_pct` | % organic matter | yes | float64; as bulk density | fine, same fix | CLEAN-1 |
| `soil_total_nitrogen` | g/kg, cores of 2016-2021 only | yes | float64; 14.6% coverage (17.2% per variable) | fine, same fix | CLEAN-1 |
| `soil_total_phosphorus` | mg/kg | yes | float64; 14.5% (17.1% per variable) | fine, same fix | CLEAN-1 |
| `phragmites_cover_pct` (target) | summed in-plot % cover of the Phragmites australis records | target | float64, 0-100. All 4,488 in-plot reed records have a cover, no visit has two reed records, and "<1"/"Solitary" (12) are 0.5, matching Braun-Blanquet "+"/"r" | fine | USE-5, CLEAN-15 |

**Raw columns not shipped (LEAK-2 sweep).** The target visit's covers, heights, species list, marsh type and comment are
co-measurements of the target, and they are correctly out. The Braun-Blanquet rank is a recoding of `% Cover`, so for
the reed rows it is the target in another form, and it is correctly out. Organisation and personnel are out (fine).
Group (100% missing), plot size (constant) and the planting counts (all missing) are out. Not named in the drop bullet:
the previous visit's tree, shrub and carpet heights, the Braun-Blanquet rank, Group, the names as originally observed
and the species descriptions (problem 4).

**Test-window row drops.** 277 visits of 2017-2025 have no measured plot, 228 of them because of the 2023 drought. Only
one has any reed record: an open-water plot with reed "Out". So no test rows are selected on the outcome.

**Problems, ranked (principles.md: all P7, then by effect; no P1-P6 column problem found)**

1. **Soil join blanks known pH and salinity in the test windows (CLEAN-1, Should).** `_soil` plus one `merge_asof` per
   site takes every soil column from the latest sampling year. The 2016-2023 cores carry no pH or salinity (0% in each
   of those years), while the 2006-2015 cores carry them in 100%. Effect: `soil_ph` and `soil_salinity_ppt` are present
   in 88-100% of rows in 2009-2018 but in 13% in 2019-2021 and 1% in 2022-2025. The source names these indicators, yet
   they are nearly absent from five of the nine test windows. The missingness codes the period: the reed share is 8.4%
   where pH is missing and 4.2% where present, which is drift, not outcome. The bullet "pH in 59%; missing stays
   missing" presents as the source's gap what is our join's. Joined per variable (the latest non-missing value of each
   soil column before the season), coverage is pH and salinity 96%, bulk density and organic matter 95.7%, N and P
   17.2%. Score: LightGBM 7.020 to 7.039 (paired SE 0.017), unchanged. **Remedy:** one `merge_asof` per soil column
   (cheap, safe, no leak: soil_year stays below Y), and correct the bullet's numbers.
2. **`previous_species_count` counts bare ground and water (CLEAN-1, Should).** These are two non-taxa of the 2006
   species list (1,634 + 36 in-plot records at 1,643 visits). Effect: 1,615 rows of 2007-2008 count one species too
   many, and 26 plant-free plots read 1 instead of 0. **Remedy:** leave "Bare Ground" and "Water" out of
   `in_plot_species` ("Unknown #n" are real unidentified plants and stay).
3. **Three impossible values (CLEAN-11, Should).** One herb height of 1,219.2 cm (40 ft; dominant height 61 cm). Three
   porewater salinities of 90, 71 and 57 ppt that contradict their own specific conductance (about 12.6, 7.1 and 5.8
   ppt at the bulk ratio of 0.57 ppt per mS/cm, 1st-99th percentile 0.50-0.65); they set `site_porewater_salinity_max_ppt`
   for their site-years and one `previous_porewater_salinity_ppt`. **Remedy:** set them missing (salinity above 50 ppt
   that disagrees with conductance; herb height above 600 cm), or keep them with a one-line note. Effect on scores
   negligible: a handful of rows.
4. **Undocumented drops (CLEAN-1; CLEAN-22 asks that a column leave for what it is, so the reason should be written; a documentation gap, not a drop for width).** The previous visit's tree, shrub and carpet heights are left
   out, though their covers ship (shrub height is present in 99.4% of visits with a shrub cover). The Braun-Blanquet
   rank, Group, the originally observed names and the species descriptions leave without being named. **Remedy:** ship
   `previous_height_{tree,shrub,carpet}_cm` next to the covers, or name each in the "Dropped" bullet with its reason
   (Braun-Blanquet: a recoding of the cover; Group: empty).
5. **Question for the curator, tied to decision 3: the dense-stand visits' "Out" record.** Decision 3 drops the 633
   unmeasured dense-stand visits because the crews' cover estimates overstate. That reason covers the cover, not the
   presence: every one of them recorded reed outside the plot. Dropping them as history lowers
   `site_share_phragmites_nearby` at the 24 such sites with 2016 visits, from 0.57 to 0.40 on average, which 159 rows of
   the 2017 window read (23% of them with reed). **Mildest remedy, if the curator agrees:** count those visits in the
   site nearby share only, and keep them out of the rows, the cover features and `previous_*`.

**Notes, no action**

* The visit's own date is a scheduled quantity, and its day-of-year pattern follows the station mix (see the table).
  The effective prediction point is the window's calendar boundary, as site porewater and late visits run to
  December. That is honest for this split (next season starts in May), but the first bullet's "end of a survey season"
  could say so.
* Tested and left out: the water level above the marsh and the open-water, bare-ground and dead-vegetation shares that
  the program templates into the comment (present in 99% of visits from 2009, 100% from 2012). Added as previous-visit
  features they change LightGBM RMSE from 7.020 to 7.028 (SE 0.041), so they add nothing.
* `previous_phragmites_nearby` is implied by reed in the plot in 99.9% of those rows ("Both" is the default code). This
  is correct by the codebook; the description could read "in or near".

Evidence files (in the run folder): the frame, the soil coverage, the ablations (soil per variable, no soil, no
date and gap) and the comment template fields.

</details>

<details><summary>Split audit</summary>

**Split auditor: crms_phragmites_cover (2026-11-01)**

**Verdict: right with notes.** The use case is a known station predicted one season ahead (USE-10), and the expanding
calendar-year windows 2017-2025 fit it. Every Must of P4 holds except one weak feature-timing slip that costs nothing
to fix: the soil cores of season Y-1 are joined before CIMS publishes them. Two texts need changing, one about when the
data are known and one about the 2017 window. The regime also needs the curator's explicit pick, because the record
still says `Grouped (NON-IID)`.

How the numbers were made: the definition's frame and splits come from `dataset_io.from_definition` (69,161 rows, the
same rows and target as the scratch rebuild with station and site ids kept). Models are untuned LightGBM (400 trees,
learning rate 0.03, 31 leaves, as in the builder's TP-10 check, one seed) and one random forest. These are probe
numbers, not leaderboard numbers (EV-8). The publication timing comes from the Wayback Machine's copies of the three
CIMS bulk zips, 2016-11 to 2025-06. Scripts, outputs and the archived zips are in the run folder.

**Judgment record**

```text
Verdict: right with notes.
Validity: SPLIT-1, SPLIT-3, USE-10 hold (temporal, known stations; the record's Grouped field disagrees, curator's pick);
  LEAK-10 triggered, weak: soil cores of season Y-1 used before CIMS publishes them (15% of test rows, effect 0.004 RMSE),
  fix: lag the soil join; SPLIT-9 holds (season Y-1 is 91-100% in CIMS before season Y starts, measured);
  SPLIT-10 holds with no gap (measured, replaces "not checked"); SPLIT-11, SPLIT-14 hold (expanding, train 50.9%-94.6%);
  SPLIT-12 holds (one season, the annual survey); SPLIT-13 holds (97.9-100% of test rows at a station seen in training);
  SPLIT-20 concern: the 2017 window is the re-entry after a 2012-2016 collection break (a note).
For the curator: confirm Temporal over Grouped; the soil lag (2 or 3 seasons).
```

**Problems, ranked**

1. **Soil cores are joined before they are published (P4; LEAK-10, Must, weak here; this is the feature side of the
   gap; remedy LEAK-7: lag).** The join takes the site's latest cores sampled up to season Y-1. In every case the
   archived downloads can show, cores reached CIMS 1 to 2.5 years after sampling:

   | cores sampled in | in the download of | not in the download of |
   |---|---|---|
   | 2019 (29 sites) | 2022-05-13 | 2021-04-29 (the 2021 prediction point) |
   | 2020 (38 sites) | 2022-05-13 (37 of 38) | 2021-04-29 |
   | 2021 (82 sites) | 2023-04-20 | 2022-05-13 (the 2022 prediction point) |

   So no case shows cores from season Y-1 published by the start of season Y. 5,157 test rows (15.2%) take cores from
   season Y-1. That includes 3,260 of the 3,827 rows of the 2019 window, which use the 2018 campaign (326 sites); its
   publication date cannot be observed, because no snapshot falls between 2016-11 and 2021-04. Another 4,701 rows take
   cores from Y-2. Cores from Y-2 would have been published in 2 of the 3 observable cases, and cores from Y-3 in all
   3. The effect on the score is nil. Mean window RMSE: 7.050 as shipped, 7.054 with cores up to Y-2, 7.054 up to Y-3,
   7.044 with no soil at all. Remedy: one line, `df["season_before"] = (df["year"] - 3).astype("int64")` (the column
   feeds only the soil join), plus the curation_comments soil bullet changed to "the latest cores published before
   the season (sampled three seasons back or earlier; CIMS posts soil analyses 1-2.5 years after sampling)". This is a
   "maybe": a CPRA manager may see the lab results before public CIMS does. If the curator reads the actor that way,
   keeping the soil as it is with a note is defensible. The fix costs nothing measurable either way.

2. **The record's regime is Grouped and the definition's is Temporal (P4; SPLIT-1, SPLIT-3, USE-10, Must; the
   curator's pick).** The screening named both: grouped by site for mapping, temporal for an early warning. The
   definition's use case is the early warning at monitored stations. CRMS is a fixed network, and 97.9-100% of each
   window's test rows are at a station with an earlier training row. The other framings, measured on the same
   2017-2025 rows:

   | split (all on the 2017-2025 rows) | RMSE | R^2 |
   |---|---|---|
   | temporal, as shipped (mean of the 9 windows) | 7.05 | |
   | carried-forward reed cover | 7.78 | |
   | IID 5-fold, all features | 5.78 | 0.829 |
   | grouped by station 5-fold, all features | 5.78 | |
   | grouped by site 5-fold, all features | 6.81 | 0.763 |
   | grouped by site, cold-start mapping (position, date, soil), LightGBM | 13.91 | 0.010 |
   | the same plus site porewater, LightGBM / random forest | 13.75 / 13.56 | 0.033 / 0.059 |
   | grouped by site, training mean | 14.02 | |

   The IID and grouped folds mix seasons, so a training row of season Y+1 carries its site's reed shares of season Y.
   Those shares contain the test row's own target, and IID's 18% lower RMSE is partly that. Under the temporal split
   this cannot happen. The cold-start mapping the record's `Grouped` stands for keeps 1-6% of the variance. That is not
   the SPLIT-28 case (all models below the mean), but it would be a very weak task, and the use case decides anyway
   (SPLIT-4). Recommendation: confirm Temporal and change the record's `required_split` to Temporal (the builder's
   draft issue 7).

3. **The prediction point and the publication delay are worded wrong, and the delay can be measured (P4; SPLIT-10,
   Should; USE-3).** splits_comment says "how soon a season's data reach CIMS was not checked", and the task places the
   prediction "after each summer's survey" / "at the end of a survey season". Measured on the archived vegetation
   downloads:

   | download | the season just ended | the season under way |
   |---|---|---|
   | 2021-04-29 | 2020: 3,923 of 3,950 visits (99.3%) | 2021: 0 |
   | 2022-01-13 | 2021: 3,553 of 3,913 (90.8%) | |
   | 2022-05-13 | 2021: 3,912 of 3,913 (100%) | 2022: 0 |
   | 2023-04-20 | 2022: 3,814 of 3,832 (99.5%) | 2023: 0 |
   | 2023-08-26 | | 2023: 70 of 3,824 (1.8%) |
   | 2024-06-08 | 2023: 3,823 of 3,824 (100%) | 2024: 0 |
   | 2025-02-02 and 2025-06-03 | 2024: 3,804 of 3,806 (99.9%) | 2025: 0 |
   | 2026-10-25 (ours) | | 2026: 677 visits, all June-July, 68 sites |

   Season Y-1 is in CIMS before the first visits of season Y (late May; no shipped visit falls in January-April).
   Training on every visit up to 31 December of Y-1 is therefore what a refit before the season sees: SPLIT-9 holds and
   no gap is needed. The porewater behaves the same way: 99.5-100% of season Y-1's readings are in the May-June
   downloads of 2022, 2024 and 2025. The labels as first published equal today's: no reed cover of the 19,408 visits of 2019-2023
   changed between the 2022 and 2024 downloads and now. But at the end of a season its data are mostly not in CIMS yet
   (1.8% on 2023-08-26; 677 visits on 2026-10-25). So the prediction point is the winter or spring before the next
   season, not the end of the last one. Remedy, text only: the task_summary `question` and `use_case` and the
   prediction-point bullet should say "before each season, once the last season's survey is in CIMS (it arrives over
   the winter)". splits_comment should replace "not checked" with the table's finding: "the previous season is
   91-100% in CIMS by January-June of the next (archived downloads 2021-2025), so no gap".

4. **The 2017 window is the re-entry after a collection break (P4; SPLIT-20, Should; a note, no re-split).** In 2017,
   99 plots of the dense-stand stations were measured again. That is 2.7% of the window, but they carry 66% of
   LightGBM's squared error and 74% of the carried-forward cover's. Without them the window scores 3.97 against 4.59.
   62 of them have their latest measured visit in 2011 (target mean 40.2, carried-forward 73.7, model 58.8), and only
   3 training rows before 2017 have such a gap. 2017 is the window with the largest gain over persistence (paired MSE
   gain 30.2 against 10.9 on average) and part of the "9 of 9" in the TP-10 bullet. The random forest also wins the
   other 8 windows, so TP-10 does not depend on it. A second fact belongs here. In the November 2016 CIMS download,
   518 of the dense-stand visits of 2012-2016 were entered as data, with in-plot reed cover averaging 98.7% (93% at
   100%) and a total cover. By the April 2021 download they had been moved to "Out" with the cover fields empty (0 of
   518 measured). So a manager predicting 2017 had the estimates as data. The curation_comments sentence "The program
   left the cover fields empty" is true of today's download only (handed to the claim auditor). The model gets less
   than that manager had, not more, so this is no leak. Remedy: a sentence in splits_comment ("the 2017 window holds
   the first measurements since 2011 of 99 plots in dense reed; they carry about two thirds of its squared error") and
   the corrected history sentence. Keep the nine windows. Only one of nine is atypical, so SPLIT-20's "most windows"
   holds, and dropping it because of its score would break SPLIT-21. If the curator prefers clean windows,
   `n_windows=8` keeps a 56% floor.

**What holds, with the check run**

* Time column and windows: `visit_date` is the collection date. The windows are calendar years, not 365-day rolls back
  from the last date (`_calendar_end`; the 2021 window holds a visit of 2021-12-21). Each window is one whole season:
  shipped visits fall in May-December (164 in May, 237 in November-December, none in January-April), so the windows
  are season-shaped. Test sizes are 3,578-3,830 rows with 220-345 reed-positive (SPLIT-17).
* Train side: expanding from 2007 (SPLIT-11). Train fractions run 94.6% for 2025 down to 50.9% for 2017 (SPLIT-14). 9
  windows (SPLIT-15). The horizon is one season, matching the annual survey (SPLIT-12).
* Features from earlier seasons only, asserted on all 69,161 rows: `previous_year < year` and `previous_date <
  visit_date` (at least 204 days). Site features come from the station's previous season and soil from `soil_year <=
  Y-1` (but see problem 1). 99.5-100% of test rows have their previous visit one season back, except 2017 (97.6%) and
  2024 (93.5%: stations not surveyed in 2023).
* Recurring entities: stations recur by design (USE-10, SPLIT-13). The hidden-group and group probes do not apply to
  a temporal task. No exact copies cross the split (leak probe 5: 0.0%).
* Small claim for the claim auditor: the shipped frame has 60 station-years with two visits, not the 63 the Row bullet
  states (63 may count before the first visits leave).

</details>

<details><summary>Domain practitioner</summary>

**Domain practitioner (actor: a CPRA coastal manager or analyst who, between two CRMS survey seasons, decides which marsh sites to watch or treat for Phragmites next season)**

**Verdict: fit approximate (I agree with `fit="approximate"`); metric partly.** The rows, the target and the temporal split are CRMS's own and match a next-season forecast at monitored stations. But four gaps keep the fit from direct. No source makes the prediction. I act on sites and basins, not on one 4 m^2 plot. CRMS does not tell the lineage. And a third of the reed rows are die-back in the delta, where the decision is to protect the reed, not to control it (USE-1, USE-5, USE-8). USE-9 does not lift the fit to direct: no decision is made per plot. The decision exists, so USE-2 does not apply, and the record's marker `No Good Target / Scientific Discovery` should go.

**How the job is done today.** CRMS samples ten 2 x 2 m stations per marsh site. They are drawn at random from 85 points on a 283 m diagonal transect across the site's 200 m square. Sampling runs once a year between June 1 and August 31: brackish and saline sites from June 1, fresh and intermediate from July 1. Two people estimate cover to the nearest whole percent and take porewater at 10 and 30 cm (CRMS/SWAMP SOP 2023, 7.1.1). Each site also has hourly water level and salinity recorders, soil cores every 5-10 years, and RSET elevation (CRMSInfo).

Guo et al. 2026 use these data to classify basin trajectories. Cover falls in the Mississippi River Delta (from above 25%) and rises from below 5% in Calcasieu-Sabine, Mermentau, Teche-Vermilion and Terrebonne. They propose a two-step monitoring framework of cover trends, native cover, and soil and porewater indicators "to flag emerging hotspots and prioritize adaptive management in other estuarine and deltaic systems". That is a monitoring template, not a per-plot forecast.

In Louisiana the reed is not simply a pest. The Delta-type lineage (M1) dominates the low coastal marshes and "is considered beneficial for marsh stabilization and contributing to elevation gain" (Hurley 2025, LSU). Its die-off in the delta since 2016 is the state's main reed problem: the roseau cane scale, rising salinity (USGS, LSU AgCenter, Louisiana Illuminator 2024). Control of the invasive European lineage matters in the western and central basins and in restored marshes (USGS 2008, Bayou Dupont).

**1. Inputs at the moment of prediction**
- What the last survey recorded at the station (marsh type, layer covers, heights, species count, reed in and near the plot), its reed history, its site's reed and porewater that season, and the latest soil cores: I have all of these. They are the CRMS tables, and CPRA staff see the CIMS buffer before public release, so the unverified publication delay (SPLIT-10) matters less for CPRA than for an outside user.
- The visit date and `days_since_previous_visit`: I know the window (June 1 to August 31) and that brackish and saline sites come first, not the exact day. The effect is small, since the schedule is regular, but the task_summary's "known: ... the date of the visit" overstates it (USE-3).
- The site's porewater is aggregated over the whole calendar year of the previous visit. That includes readings from October to December, so the prediction point is really the winter before the next season, not "the end of a survey season". This is a wording fix to the first curation_comments bullet.
- Inputs I would always have and that are missing:
  - The site's continuous hydrology: flood duration and growing-season salinity from the hourly recorders. These are CRMS's core measurement, and salinity drives the delta die-back. The bulk download `CRMS_Continuous_Hydrographic.zip` was live on 2026-11-01 (1.29 GB).
  - Surface elevation and accretion: `CRMS_Surface_Elevation.zip`, 4 MB.
  - Hurricane passage (Laura and Delta 2020, Ida 2021).
  - The hydrologic basin, Guo et al.'s own unit. It can be derived from position.

  Their gain is not measured. Porewater and soil moved LightGBM only from RMSE 7.08 to 7.02, so the gain on RMSE may be small. This is a Should, not a blocker.
- The 633 plots in dense reed (2012-2016): dropping them as rows is right. Dropping them from the history is not. I would know that "last season the crew could not enter this plot for dense Phragmites, estimated 100%". That is the program's own estimate, made before the outcome: a legitimate input (USE-6). The builder rejected using the estimate as the previous cover, which raised carried-forward RMSE in the 2017 window from 8.86 to 10.39. A separate flag (and the estimate as its own column), leaving `previous_phragmites_cover` at the last measured visit, was not tested. It touches 171 stations, mostly in the 2017 window.

**2. The target.** The percent reed cover in the plot is the quantity CRMS records and Guo et al. analyse, so it is not a proxy (USE-5). I want a number, the expected cover, which squared error scores.

Two limits:
- The cover is that of the species, not the invasive lineage (already in `fit_reason`).
- The values are ocular estimates: 89.7% of the positive targets are multiples of 5. In plots with reed at both visits, the year-to-year change has a median of 15 points (IQR 5-30, 2,481 test rows). Much of that is observer noise no model can predict.

**3. Row and test data.** One row is one station visit with an earlier measured visit. The test windows are the next season at stations already monitored. That is the situation I face (USE-10, SPLIT-3), and the builder's choice of temporal over the record's `Grouped` is right. A grouped-by-site mapping task would answer a question I solve with imagery, not with a plot model that has only position and soil.

The unit differs: I decide per site or basin, and the plot is the program's sampling unit. Averaging plot predictions per site serves me. Over eight models, site-year RMSE ranks the same as plot RMSE: Kendall tau 0.93, only the two LightGBMs swap (RF 6.92 / 4.02, LightGBM 7.05 / 4.13, carried forward 7.75 / 4.38). So the plot rows do not distort my decision. The use_case should say the manager aggregates plots to sites.

**4. Would I use it?** As a forecast of next season's cover at monitored sites, yes. It beats last year's cover at the site level in the pooled windows, and the random forest beats it in all nine plot windows.

What makes me distrust it as an early warning:
- 28% of the random forest's gain over carried-forward is a single linear shrinkage of last year's cover: carried forward 7.75, `prev_ols` 7.51, RF 6.92.
- For expansion (an increase of 10 points or more, 1,000 test rows), the ROC AUC of predicted minus previous is only 0.70.
- New colonisation is rare: 229 plots in nine windows, 0.73% of the plots without reed.
  - A dedicated colonisation classifier reaches ROC AUC 0.964 and AP 0.215.
  - A three-term rule I can read off the field sheets reaches 0.951 and 0.225 (reed near the plot x 2 + any reed earlier + the site's share with reed).
  - The RMSE-trained regression ranks colonisation at 0.915, below the rule.

  So the "emerging hotspot" flag is mostly what I already read on the sheet.

What would build trust: wins in the windows after shocks. LightGBM lost the 2018 window (6.99 against 6.78), the first after the delta die-off began; the RF won it.

**5. The metric: partly.** `rmse` on plot cover is the right fallback. No source scores a prediction, since Guo et al. report trajectories (MET-1, MET-5, MET-11). Squared error is consistent for the expected cover I want (MET-8). At my unit it ranks models as site-year RMSE does (tau 0.93), so a custom per-site metric is not worth its cost (MET-2, MET-12, MET-13).

It does not score the use case as worded, though. Colonisation holds 7.4% of the model's squared error and plots with reed at both visits 82.6% (carried forward: 7.4% and 85.7%). Ranking colonisation by ROC AUC would score the early warning, but no source fixes a k or threshold (MET-7: never invent one). There are only about 25 positives per window (MET-10, resolution), and a hand rule nearly ties the best model.

I would keep `rmse` and reword the use case to what it scores: next-season cover at monitored stations, spread in the west and die-back in the delta. Then the metric scores the decision.

**Gaps between the dataset and the real decision, ranked by how much they change the task**
1. **Direction of the decision (USE-1, USE-5).** An approximate box around the Bird's Foot Delta (longitude east of -89.7, latitude south of 29.45) holds 4.9% of the test rows but 34.9% of the test rows with reed. There, reed plots changed by -3.2 points on average, against +1.6 elsewhere. "Flag emerging hotspots for control" misreads a third of the signal: there the manager protects the reed.
2. **The early warning is a small slice (USE-1, MET-1).** 229 colonisations hold 7.4% of the squared error. The shipped task is cover forecasting at known stations. The use_case should say so, not "flag emerging hotspots".
3. **Missing inputs I would always have (USE-3).** Continuous hydrology, elevation, hurricanes, basin. Their gain is unmeasured.
4. **Dense-stand history dropped (USE-6).** A flag for "the previous visit was unmeasured in dense reed", with the crew's estimate as a separate column, would carry what the manager knows. 171 stations, mostly the 2017 window.
5. **Plot against site (USE-5).** Measured: model rankings agree (tau 0.93), so it needs only a sentence.
6. **Lineage not recorded (USE-8).** Already named.
7. **Timing wording (USE-3).** The exact visit date is not known ahead, and the site porewater runs to December. The prediction point is the winter before the season.

**What an expert would change**
- Reword `use_case` and `fit_reason`. Proposed `use_case`: "between seasons, a CPRA manager forecasts each monitored station's reed cover at next summer's survey, averaged to sites, to track spread in the western and central basins and die-back in the delta". Add to `fit_reason`: the delta's reed is protected, not controlled.
- Add a flag (and the estimate) for a previous visit inside an unentered dense reed stand.
- Test the CRMS continuous hydrographic summaries (growing-season mean salinity, percent time flooded) as site features before shipping, or name them in the notes as left out.
- Drop the record's `No Good Target / Scientific Discovery` marker, and set the record's required split to temporal.
- Keep `rmse`.

**Claims checked**
- The `use_case` cites Guo et al.'s "flag emerging hotspots". The phrase is in the abstract, but it presents the framework as a template "in other estuarine and deltaic systems". The citation is fair; "control" is the part that does not hold for the delta.
- `fit_reason`: "a manager acts on sites rather than 4 m^2 plots" is true, but measured, it does not change the model ranking. I would say so.
- The first `curation_comments` bullet ("prediction point: the end of a survey season"): see the porewater point in section 1.
- The builder's TP-10 numbers were reproduced within rounding: carried forward 7.746, RF 6.92-6.93, LightGBM 7.02-7.05.

**Sources**
- CRMS data collection and schedule: https://www.lacoast.gov/crms/CRMSInfo.aspx
- CRMS/SWAMP SOP, August 2023, sections 7.1.1-7.1.3 (station layout, June 1-August 31 window, cover estimation, QA/QC): https://www.lacoast.gov/reports/project/CRMS_SWAMP_SOP_2023_Final_compressed.pdf
- Guo et al. 2026, USGS abstract: https://www.usgs.gov/publications/expansion-trends-and-impacts-phragmites-australis-louisiana-gulf-coast
- Hurley 2025, LSU thesis (Delta-type M1, beneficial in coastal Louisiana): https://repository.lsu.edu/gradschool_theses/6137
- USGS on the delta die-off: https://www.usgs.gov/news/featured-story/invasive-pest-may-not-be-only-cause-recent-louisiana-marsh-die
- LSU AgCenter: https://www.lsuagcenter.com/profiles/lbenedict/articles/page1544476198066
- Louisiana Illuminator 2024: https://lailluminator.com/2024/06/13/marsh-grass/
- USGS 2008 (Eurasian haplotype in a restored marsh): https://pubs.usgs.gov/publication/70032108
- CIMS bulk downloads (HEAD on 2026-11-01): https://cims.coastal.la.gov/RequestedDownloads/ZippedFiles/CRMS_Continuous_Hydrographic.zip
- My probes on the definition's frame and shipped windows, in the run folder (site ids joined from the builder's scratch frame, all 69,161 rows matched): error by transition class, colonisation ranking and site level; the colonisation classifier against the rule and the delta box; plot against site-year RMSE rankings.


</details>

<details><summary>Blind review</summary>

**Verdict: include with changes.** The table is real CRMS data and I rebuilt it from source: the target matches on 99.98% of rows, and every feature I could trace uses only information from before the visit. Before it goes in, fix the soil-feature join (its missingness shifts with time) and remove the structurally-zero swamp rows. Scoring should allow for the fact that about 90% of the squared error comes from the 8% of rows where Phragmites was already present.

**What the task is**

- Each row is one plot visit. A plot is a 4 m² vegetation plot at a CRMS site in coastal Louisiana (394 sites, 4,098 plots, 2007-2025). The target is the cover of *Phragmites australis* inside the plot, in percent, at the current annual survey. The features describe the previous visit to the same plot, the site's survey in the previous calendar year, porewater salinity at the site in the previous calendar year, and the most recent soil core taken before the visit.
- Who would use it: a monitoring or management agency (CPRA, USGS) forecasting where Phragmites cover will rise or fall ahead of the next survey, to target surveillance or herbicide treatment. The cited paper (Guo et al. 2026, *Ecological Applications*, doi 10.1002/eap.70246, "Expansion trends and impacts of Phragmites australis on the Louisiana Gulf Coast") is descriptive, not a forecasting study. Per the USGS summary, it finds cover "declined in the Mississippi River Delta" and expanded in four western basins, and it recommends "basin-specific early-warning monitoring." So the one-visit-ahead forecast is a task built from the data, but a plausible one.

**What I verified (no problems found)**

- **Real data and the right target.** I downloaded `CRMS_Marsh_Vegetation.csv` (594,288 species-by-visit rows, all 4 m² plots). I rebuilt plot-visit Phragmites cover by summing `% Cover` over rows marked In or Both, and joined on coordinates and date. 69,150 of 69,161 rows match exactly. The other 11 rows are 0.5 in the table, where the source has the strings "<1" or "Solitary" (12 such source records). The 0.5 coding is reasonable.
- **No leakage in the plot-history features.**
  - `highest_phragmites_cover_before` is never below `previous_phragmites_cover`, and the target exceeds it in 1,180 rows. So it does not include the current visit.
  - `phragmites_nearby` corresponds to the source's "Out" flag ("species is present... outside of the sample plot").
  - `previous_porewater_salinity_ppt` equals the plot's porewater salinity at the previous visit (averaged over the two depths) in every row where both exist. It matches the current visit's value in only 3% of rows.
- **No leakage in the site features.**
  - `site_phragmites_cover_mean` and `site_share_with_phragmites` equal the site's previous-calendar-year survey statistic in 98.97% of rows. Of the 715 rows that differ, none equals a nonzero same-year value; the differences come from years without a survey.
  - `site_porewater_salinity_mean/max_ppt` equal the mean and max of all porewater rows at the site in the previous calendar year (from `CRMS_Discrete_Hydrographic.csv`) in 96.6% of rows. Same-year windows match in under 5%.
- **No leakage in the soil features.** The soil columns come from a backward as-of join on `CRMS_Soil_Properties.csv`. 0 of 63,998 non-null soil rows use a site whose first soil core was taken after the visit date.
- **No copies.** There are no exact duplicate rows and no duplicate feature vectors. The same plots appear in train and test, which matches how the model would be used: forecasting next year at monitored plots under a temporal split.
- **There is signal, but not much beyond persistence.** I ran an expanding-window evaluation (train on years before Y, test on year Y, for Y = 2017-2025, which approximates the 9 windows). Mean R² across windows:

  | Method | Mean R² | RMSE | MAE |
  |---|---|---|---|
  | Persistence (target = `previous_phragmites_cover`) | 0.671 | 7.75 | 1.66 |
  | Linear model on previous cover | 0.695 | n/a | n/a |
  | LightGBM | 0.725 | 7.13 | 1.71 |

  Per-window R² for LightGBM ranges from 0.56 (2020) to 0.82 (2019). Previous cover and the historical maximum carry 74% of LightGBM's gain. Correlation between target and previous cover is 0.855.

**Concerns, most serious first**

1. **Extreme zero inflation, so the score rests on a small subset.**
   - Evidence: 94.1% of targets are 0. Only 13% of plots ever have Phragmites.
   - 58,622 rows (85%) have no Phragmites in the plot's history, none at the site last year, and none nearby. Only 20 of those rows turn positive.
   - All 8,994 Swamp rows are 0, which makes sense: Phragmites does not grow in forested swamp.
   - Rows with prior presence are 7.8% of the test rows but carry 90.5% of LightGBM's squared error. Each test window has only 220-345 positive rows.
   - Method rankings will therefore be decided by a few hundred plots per window, and MAE rewards predicting near zero (LightGBM's MAE is worse than persistence).
   - Change: drop the Swamp rows (or plots with `previous_community == Swamp`). Label the task as zero-inflated so it is scored with RMSE or R² rather than MAE. Optionally restrict to sites with any Phragmites record before the visit (`site_share_with_phragmites > 0` or `phragmites_nearby_before == yes` or `highest_phragmites_cover_before > 0`), which removes the trivial zeros without leakage.
2. **The soil join creates missingness that changes over time and differs between train and test.**
   - Evidence: the join takes the most recent soil sampling event as a whole. When a later event did not measure pH or soil salinity, those columns become NaN instead of keeping the earlier value.
   - `soil_ph` is non-null in 98-100% of rows for 2010-2016, but in 13% for 2019-2021 and about 1% from 2022 on. Over the whole period from 2017 it is non-null in 25% of rows, against 92% before 2017.
   - `soil_total_nitrogen` and `soil_total_phosphorus` are 0% non-null before 2017 and about 35% after.
   - So a model trained on early windows sees pH almost always, and the late test windows almost never have it.
   - Change: carry forward the last non-missing value per soil variable within a site. Or drop `soil_ph`, `soil_salinity_ppt`, `soil_total_nitrogen` and `soil_total_phosphorus` (41%, 41%, 85% and 85% missing overall).
3. **Little headroom beyond persistence.**
   - Evidence: LightGBM beats persistence by only 0.054 R² on average, and in 2018 persistence wins (0.802 against 0.776).
   - The rest is mostly year-to-year change in a visual cover estimate recorded in 5% steps. That change is partly observer noise I cannot measure.
   - Still worth including, because it is a realistic and hard ecological forecasting setting. But expect small, noisy gaps between strong methods.
   - Change: none required. Keep persistence as a reference baseline when reporting.
4. **Population drift across the test windows.**
   - Evidence: the share of positive rows is about 3.3% for 2007-2016 and 7.9-9.2% for 2018-2025.
   - Part of the jump comes from about 90 plots added in 2016-2018 that are Phragmites-heavy (64-70 positive rows per year from them). The rest is real expansion in old plots.
   - The paper describes opposite trends by basin, including dieback in the Mississippi River Delta.
   - This is realistic for a temporal benchmark. Document it, because the early windows have short training histories.
5. **Minor preparation issues.**
   - **Ambiguous NaNs:** `previous_cover_shrub`, `previous_cover_tree` and `previous_cover_carpet` are NaN in 89%, 99% and 97% of rows. In the source a blank most likely means the layer is absent, so 0 is the probable meaning. Fill with 0, or document.
   - **Shared coordinates:** four coordinate pairs are shared by two distinct plots (for example 30.304725, -90.387794), giving 18 plot-date pairs that look duplicated. There is no plot or site ID column, so latitude and longitude act as an implicit ID. Consider adding a site ID, for grouping only.
   - **Repeat visits:** 79 plot-years have two visits.
   - **Large revisit gaps:** `days_since_previous_visit` is above 730 days in 311 rows (max 5,884). Those "previous" values are stale; this is acceptable, since the gap is given as a feature.
   - **Tall heights:** `previous_height_dominant_cm` reaches 3,048. These are tree heights in swamp plots, plausible once swamp rows are understood.
   - **Unlabelled nearby share:** `site_share_phragmites_nearby` matches the previous-year share of plots with Phragmites recorded in or out (98.9%), not the "Out-only" share. That is fine, but the column name should say so.

**What I could not check**

- The exact boundaries of the 9 test windows, and whether `visit_date` itself is offered as a feature. I approximated the windows with calendar years 2017-2025.
- The paper's full text (Wiley returned 403). I relied on the USGS publication page summary.
- The roughly 3% of rows where the site porewater statistics do not match my reconstruction, and the roughly 7% of soil rows that differ from my backward join. These are probably differences in depth averaging or data revisions. Nothing pointed to future information.
- Observer error in the Braun-Blanquet-style cover estimates.

**Sources**

- CRMS portal: https://www.lacoast.gov/crms2/
- Vegetation data: https://cims.coastal.la.gov/RequestedDownloads/ZippedFiles/CRMS_Marsh_Vegetation.zip
- Porewater data, used for verification: https://cims.coastal.la.gov/RequestedDownloads/ZippedFiles/CRMS_Discrete_Hydrographic.zip
- Soil data, used for verification: https://cims.coastal.la.gov/RequestedDownloads/ZippedFiles/CRMS_Soil_Properties.zip
- Paper record: https://www.usgs.gov/publications/expansion-trends-and-impacts-phragmites-australis-louisiana-gulf-coast (doi 10.1002/eap.70246)

I did not open any files outside the clean room and these downloads.

</details>

<details><summary>Precedent check</summary>

**Verdict.** Most choices follow precedent: the temporal regime, the dense-stand drop, the history and site features, the dropped ids, the fallback metric, the year, and the proposed warnings. One decision departs from the closest curator precedents without a stated fact: the claim that TP-10 leg 1 holds. Two smaller departures each have a fact or remedy at hand: the soil join ignores CIMS's publication delay, and the "no gap" says the delay "was not checked" when it can be measured. Same-run definitions (walmart, nantucket_sound, wadden_sea, noaa_afsc, basque_offshore_bivalve) are AI drafts no curator has reviewed. I list them as siblings to decide alike, not as precedents.

**Evidence.** The decision register (1,620 decisions; flags 1, 3, 6 and 10 bear on this dataset). The Cases tables of `task_probes.md`, `splits.md`, `use_case.md`, `metrics.md`, `cleaning_features.md` and `provenance.md`. The records named below and the same-run definitions. Git history of the record: `required_split: Grouped` came from the AI triage commit 137c1694 (2026-10-19). The only curator line is CC 2026-10-30 (Andrej, `Yes`, priority 4), which sets no regime. My own test of TP-10 leg 1 is in the run folder. It agrees with the claim auditor's claim 18.

**Per decision**

| Decision | Standing | Precedents | Note |
|---|---|---|---|
| 1. Temporal, not the record's Grouped (SPLIT-1, SPLIT-3, USE-10) | consistent, if decision 2 holds | corporate_credit_rating, USE-10 Cases (known entity, previous outcome as a feature); Tensions row "Temporal against grouped" (Lennart, 2026-10-12); same run: basque_offshore_bivalve_biotoxins and noaa_afsc temporal; nantucket_sound grouped *because* TP-10 leg 1 failed there (R^2 0.04 against 0.025) | The Grouped field is an AI triage value, not a curator decision. A later measured stage supersedes it (principles, "Stages"). The temporal choice stands or falls with decision 2. If leg 1 fails, nantucket_sound is the sibling to follow (grouped mapping or a re-target). |
| 2. Persistence-heavy task in scope (SEL-10/SEL-11 via TP-10, Must) | **departs without a stated reason** | telemonitoring_parkinsons (Lennart, 2026-10-02, retired; SPLIT-28 Cases); rain_in_australia (Lennart, 2026-10-26, TP-10 amended); walmart_sales_in_stormy_weather (same run); ashrae_great_energy_predictor_iii (2026-10-15) | See below and prompt 1. |
| 2b. Not `Trivial` (TP-4) | consistent | california_house_prices_2020, aps_failure (Lennart, 2026-10-06, kept: the raw feature loses to the methods); fitness_club retired (2026-10-05: raw feature above every configuration) | The raw carried-forward cover (RMSE 7.75) loses to RF (6.93) in 9 of 9 windows. TP-4 tests the raw feature, so the reading is right. It does not settle TP-10. |
| 3. Dense-stand plots dropped as rows and as history | consistent (the rule cited in the builder's draft issue 3 is off) | CLEAN-15 (Must: drop rows with a missing target): the program left `% Cover` empty; Tensions row "a better version against our own fix" (eryhemato: a fix of our own invention is not a better version) rules out parsing comment estimates into targets; alfa_battle_2_0_task_2 (Lennart, 2026-10-26: "keep the newest months with the note on possible right-censoring"), a training-side selection kept with a note | The draft files this as USE-5/LEAK-22 (Must). LEAK-22 covers cohort rows that *cannot* have the outcome, and framingham's rows had a label. Neither fits. The fault differs from consumer_complaints and sf_permit_time (Lennart, 2026-10-01: censored *test* windows, fixed): every dropped visit (2012-2016) precedes every test window. The cost is a SPLIT-20 history-break note, as written. |
| 4a. Site-season reed and porewater features | consistent | CLEAN-19 bullet 4 (rain_in_australia, Lennart, 2026-10-26: other rows' readings, "kept only where they are known by then") | The split auditor measured season Y-1's vegetation and porewater as 91-100% in CIMS before season Y starts. |
| 4b. Soil join on cores up to season Y-1 | **departs, no reason given; remedy at hand** | the same rain_in_australia guard (features from other rows kept only where known at the prediction point); LEAK-7 (lag) | The split auditor found that CIMS posts cores 1 to 2.5 years after sampling. 15.2% of test rows use cores from Y-1, and the effect is nil (7.050 against 7.054 RMSE). Prompt 2. |
| 4c. History aggregates (highest cover, visits with reed, reed nearby) | consistent | CLEAN-19 bullet 3 (a history aggregated to one row per prediction; no published baseline exists, so "a reasonable combination") | Not of the kind behind the CLEAN-19 amendment flag (amex_non_iid, fraud_detection: raw history kept as rows), so it adds no third exception. |
| 4d. Station and site ids dropped (CLEAN-3, Should) | consistent | noaa_afsc (same run: `station` dropped, "the position columns hold the place"); walmart keeps store and item ids and rain_in_australia keeps `Location`, but neither ships coordinates | crms ships each station's latitude and longitude, which is what sets it apart from those two. |
| 4e. Same-visit vegetation dropped (LEAK-10) | consistent | LEAK-10 co-measurement cases; the screening's risk note | |
| 5. `Metric.fallback` rmse, identity scale | consistent | MET-11 fallback; churn_telco_south_asia (Lennart, 2026-10-21: fallback kept when the first publication could not be read); same run: cape_floristic_region_family_cover (plant cover, fallback, no transform) | The use case's "rank ... to flag emerging hotspots" is not what RMSE scores (claim auditor, claim 34). By precedent the fix goes in the wording, not the metric. The Tensions row says we never invent a cost or threshold, and melbourne_housing_market (2026-10-20) had its use-case wording fixed in the definition. If the Guo et al. full text names a prediction metric (PROV-16 open), MET-5 reopens this. |
| 6a. No gap (SPLIT-10, Should) | departs as written; the fact exists | melbourne_housing_market (Lennart, 2026-10-21: "no gap, measured", applied, not an exception); ames_housing and perth_house_prices (exceptions; amendment due, flag 10) | Measured, it is the melbourne kind and needs no exception. The split auditor's Wayback series shows season Y-1 in CIMS before the first visits of Y. In our own download of 2026-10-25, which is byte-identical to the one of 2026-10-18, visits run to 2026-07-30 and none from August-October 2026 appear (2025 had 1,051 visits in those months). The lag is about 2-3 months, against roughly 7 months between a season's last visit (October) and the next season's first (June). Prompt 3. |
| 6b. Year 2006 -> 2026 (PROV-9) | consistent | PROV-9 growing-source clause; sf_permit_time; same run: noaa_afsc, noaa_storm_events_damage, thailand_road_accident_register (2026), wadden_sea (snapshot 2024) | |
| 6c. Record: required_split Temporal, tag `Non-IID (Temporal)`, porewater and soil zips in `source_links` | consistent, once decision 2 is settled | the tag is in use on 190 records | |
| 6d. Warnings proposed for acceptance | consistent | `meta_time_horizon_mismatch`: zillow_prize, perth_house_prices (calendar windows whose data span reads shorter); `meta_license_unknown`: diabetes_3, mobile_churn; `task_target_value_dominant`: australian_vehicle_insurance_2004_2005 and frempl in this run, and Andrej's policy question 2 (2026-10-30: "We don't care. We want to add any relevant predictive task, independent if it is zero inflated or not") | |
| 6e. Marker `No Good Target / Scientific Discovery` on a `Yes` record | open; precedent points to removal if decision 2 holds | USE-8 makes it the marker for fit None, and the definition says approximate; markers refuted by a test have been removed: thyroid_discordant (Lennart, 2026-10-22), ames_housing and house_prices_nominal (2026-10-26), ghcn_daily_precipitation (Andrej, 2026-10-30) | selection.md allows a concern marker on a `Yes`. Decide alike with the same-run records that carry it open: boreal_postfire_lichen_biomass, pennsylvania_oak_hickory_regeneration_experiment, noaa_storm_events_damage, rand_health_insurance_experiment_doctor_visits. If decision 2 goes to `No`, the fitting marker is `Time-series (Forecasting)`, not this one. |

**Decision 2 in detail.** The definition claims TP-10 leg 1 because the random forest beats the *raw* carried-forward cover by 10%, 9 of 9. The precedents measured leg 1 against a stronger bar:

* rain_in_australia (Lennart, 2026-10-26) is the amendment that lets the last observation stay, with "leg 1 then carries the test: the model must clearly beat the forecasts built from the series itself". The bar was a forecast fitted on the location's own series (ROC AUC 0.752-0.754). The full model reached 0.849, ahead in 9 of 9, and the last observation added 0.0027. Raw persistence (0.661) was the weakest comparator, not the bar.
* walmart_sales_in_stormy_weather (same run) used the best of 13 own-series forecasts. LightGBM was 3.5% lower (paired SE 0.0067), ahead in 7 of 9.
* telemonitoring_parkinsons (Lennart, 2026-10-02, retired; the SPLIT-28 case) is the case with the most similar facts: a known entity tracked over visits, with the last value doing the work. Carried forward scored 6.98 and carried forward with the mean drift 6.48. The best model scored 6.33 (2.3% lower) and LightGBM 7.32. The reason: "the benchmark would rank models by how little they lose to a constant, not by what they learn from the data."
* crms on the shipped windows (my own run): previous cover alone, fitted by LightGBM as in the task probe, scores 7.062. The RF scores 6.930 (1.9% lower). It is ahead in 5 of 9 windows, its paired gain is above 2 SE in 4 (2017, 2019, 2020, 2022) and below -2 SE in none, and the mean MSE gain is 1.80 with SE 1.17 over the windows. LightGBM (the builder's configuration, 3 seeds) scores 7.025 (0.5% lower), ahead in 4 of 9, with one window clearly worse (2018). In the two newest windows the fitted last value beats both models. Without the station's reed history, LightGBM falls from 7.02 to 7.88. The claim auditor's isotonic curve gives 7.042.
* ashrae (2026-10-15) passed against a raw naive profile. Its features held no lag of the target, so the fitted comparator was never needed there.

Against the bar rain_in_australia and walmart used, crms's margin (1.9%, 5 of 9) sits at or below the margin telemonitoring_parkinsons was retired with (2.3%). The definition names no fact that sets it apart. Pointing in the other direction is the Tensions row "the right split against the score" (forest_fires): a small signal under the right split is no reason to retire. The rule text itself is ambiguous. The TP-10 Methods say "the best naive forecast (... or its last value)", while the 2026-10-26 text says "the forecasts built from the series itself". crms is the first case where that choice changes the outcome. TP-10 is a Must, so a reading that keeps crms is an amendment, not an exception.

A lead for the column auditor, not tested further: a LightGBM on all five reed-history columns scores worse than on the previous cover alone (7.65 against 7.06). The cumulative `visits_with_phragmites_before` may drift with calendar time.

**Drift and third exceptions.** I found no drift. Andrej's calls in this family (walmart: "Do yes and then we can see what happens"; metro_manila: "Test the leg, then decide") both defer TP-10 to the measured leg. Lennart's TP-10 outcomes that look opposite carry their reasons (stock and appliances: "context and data"). Third exceptions: SPLIT-10 already has its amendment due (flag 10), and crms adds none if the measured lag is written. CLEAN-19 (flag 6) is a different kind. TP-10 has no prior exception of this kind.

**Consistency prompts**

1. **Consistency check (AI, 2026-11-01):** the draft says crms passes TP-10 leg 1 because its models beat the raw carried-forward cover (RMSE 6.93 against 7.75, 9 of 9). rain_in_australia (2026-10-26) was judged against forecasts fitted on the series itself, and walmart (same run) against the best of 13 own-series forecasts. Against previous cover alone, fitted (7.06), crms's RF is 1.9% lower and ahead in 5 of 9 windows, and LightGBM 0.5% and 4 of 9. telemonitoring_parkinsons was retired (2026-10-02) with a 2.3% warm-start margin. What sets crms apart?
   (a) crms is a known-station early warning by its use case (USE-10), not a warm start recast after a failed grouped task. With about 3,800 test visits per window, the RF's small gain is measured: 4 windows above 2 SE, none below. So the forest_fires row applies, and TP-10's comparator is the raw last value the manager reads. This needs an amendment of TP-10's wording, since TP-10 is a Must.
   (b) Treat crms like telemonitoring_parkinsons: leg 1 fails. Re-target first (colonisation at reed-free stations, where the claim auditor finds RF AUC 0.956 against 0.896 for history only; check TP-9's 18-32 positives per window), or take the grouped mapping as nantucket_sound did, else `No` + `Time-series (Forecasting)`.
   (c) Reopen telemonitoring_parkinsons to match crms.
   (d) Amend TP-10 to name the comparator (the raw last value, or the best forecast fitted on the series itself) and what "clearly" means (for example a paired margin over the windows).

2. **Consistency check (AI, 2026-11-01):** the soil join takes cores sampled up to season Y-1, but CIMS posts them 1 to 2.5 years after sampling (split auditor). rain_in_australia's other-row inputs were "kept only where they are known by then". What sets crms's soil apart?
   (a) A CPRA manager sees the lab results before the public download does, recorded as the actor's knowledge in the soil bullet.
   (b) Treat it like rain_in_australia: lag the join to cores of Y-3 or earlier. It costs nothing measurable (7.050 against 7.054).
   (c) Reopen rain_in_australia's guard.
   (d) Change the rule.

3. **Consistency check (AI, 2026-11-01):** the splits comment ships no gap and says how soon a season reaches CIMS "was not checked". The SPLIT-10 departures so far rest on a measured fact (melbourne_housing_market applied; ames_housing and perth_house_prices as exceptions). What sets crms apart?
   (a) The fact is measured now: season Y-1 is 91-100% in CIMS before season Y's first visits (split auditor, Wayback), and the 2026-10-25 download lags the field by about 2-3 months, against a 7-month off-season. Write it into the splits comment, as melbourne_housing_market's measured no-gap was, and move the prediction point to "before the next season". That makes it no exception.
   (b) Add a gap of one season.
   (c) Reopen melbourne_housing_market.
   (d) Change the rule (the ames_housing/perth_house_prices amendment already proposed would cover it).

</details>

<details><summary>Advocate</summary>

**Advocate: crms_phragmites_cover, opening brief (2026-11-01)**

**Position: ship after changes.** The target is the program's own, measured at its own monitored stations. It is rebuilt
faithfully and evaluated without a leak, and the features beat every forecast a station's own reed series can make.
Each real problem the evidence agents found has a fix in the definition or its text. One call belongs to the curator:
which comparator leg 1 of TP-10 uses.

```text
Verdict: ship after changes.
Validity: SEL-11/TP-10 leg 1 holds against each station's own series (RF 6.4% lower, 9 of 9), not clearly against a
  pooled curve of the last value (1.5%): the curator's reading; USE-1 holds once the use case is reworded (MET-1);
  LEAK-10 holds, one weak slip fixed (soil lag, LEAK-7); SPLIT-1/3, USE-10 hold (temporal); PROV holds (target
  rebuilt from source on 99.98% of rows); USE-6: add the dense-stand flag.
Value: TP-4 not Trivial; TP-9 holds (220-345 positives per window); MET-2 holds; fallback rmse kept.
Quality: CLEAN-1 soil join and species count, CLEAN-11 three impossible values: fix; CLEAN-22 drops: document.
For the curator: issue 1, the TP-10 comparator (an amendment either way).
```

New evidence of mine (untuned, probe numbers, EV-8; scripts and logs in the run folder): per-station forecasts,
a paired test against them, and an early-stopped LightGBM against the pooled curve, which went against me.

**1. Leg 1 of TP-10 holds against the forecasts a station's own series can make (P2: SEL-11, Must, tested by TP-10, Must).**

* Evidence. The raw last value scores RMSE 7.746. RF scores 6.930 (10.5% lower, 9 of 9 windows) and LightGBM 7.025
  (8 of 9); the builder's numbers, reproduced by the claim auditor and the precedent checker.
* New: I scored nine forecasts built only from each station's own reed series: the last value, the mean, the mean
  and median of the last three, EWMA 0.3/0.5/0.7, a linear trend and the last value plus drift.
  * The best is EWMA 0.7, picked on the test windows themselves, at 7.401.
  * RF is 6.4% lower and wins 9 of 9 windows. It also wins 9 of 9 against the best of the nine picked per window
    (7.380). The mean paired MSE gain is 6.94, SE 2.03 over the windows, and no window is below -2 SE.
  * LightGBM is 5.1% lower and wins 8 of 9 (gain 5.68, SE 2.65).
  * Without 2017 the RF still wins all eight windows.
  * The margin is wider than walmart's in this run (3.5%, 7 of 9, against the best of 13 own-series forecasts).
* Rule. SEL-11 (Part 1, Must) names the comparator: "a model on the features clearly beats each entity's naive
  profile". selection.md calls it "the naive-profile test". TP-10's Methods say: "the best naive forecast (each
  entity's profile ... or its last value)". In rain_in_australia (Lennart, 2026-10-26) leg 1 was read against
  persistence and the location-by-month climatology, and the record calls its 0.75 comparator "a naive forecast"
  (Assessment, 2026-10-26).
* Against the objection (claim auditor, claim 18; precedent checker, decision 2):
  * The isotonic curve of the previous cover (7.042) is not a forecast from "the series itself". Its shape is learned
    from 35,000-65,000 rows of about 4,000 other stations. That pooled shrinkage is the learning across entities that
    TP-10 says puts "tabular forecasting" in scope ("where people want to generalise across entities").
  * A one-feature fitted model is the `one_feature` flag, and TP-4 settles that flag with the raw feature. The raw
    feature loses in 9 of 9 windows, and even the fitted curve beats the RF in only 4 of 9.
  * Where the wording differs, Part 1 (SEL-11) wins over a reading of a sentence in Part 6.
* The features also add what no series can. At stations with no reed so far, every own-series forecast is 0. There
  the RF ranks colonisation at AUC 0.956, against 0.896 from the station's history alone (claim auditor). The domain
  practitioner's three-term rule (0.951) leans on the site's share with reed, which comes from other stations.
* This is not telemonitoring_parkinsons. There, LightGBM lost to the raw carried-forward value (7.32 against 6.98),
  and only one model beat a drift-adjusted carry, by 2.3%, after the grouped task had failed (SPLIT-28). Here every
  family beats the raw value by 9-10%, and the known-station use case came first (USE-10).
* Concession. Against the pooled curve the margin is small: RF 1.5% (5 of 9), LightGBM a tie. I tried a stronger
  model to widen it: LightGBM early-stopped on the last training season, 3 seeds. It scored 7.05-7.13, no better than
  the curve, so I do not lean on TP-1. If the curator names the pooled curve as the bar, leg 1 is not clearly met. The
  precedent checker is right that this is an amendment either way (prompt 1, option d). I ask for the per-entity
  reading, written into TP-10 by that amendment.

**2. A real decision on the program's own target; the metric gap is a wording fix (P3: USE-1 and USE-8, Must; P6: MET-1).**

* Evidence. The domain practitioner, writing as the actor, agrees with fit approximate. The decision exists (USE-2
  does not apply), and they would keep rmse. Plot rows rank eight models as site-year RMSE does (Kendall tau 0.93), so
  the plot unit does not distort a manager's site decision. The target is what CRMS records and Guo et al. analyse
  (USE-5, not a proxy).
* Concede: "flag emerging hotspots for control" is not what RMSE scores. 92.6% of the naive forecast's squared error
  sits on the 7.8% of plots that already hold reed, and 34.9% of the test rows with reed are in the delta, where reed
  is protected, not controlled.
* Mildest remedy: reword `use_case` to the domain practitioner's text ("between seasons, a CPRA manager forecasts each
  monitored station's reed cover at next summer's survey, averaged to sites, to track spread in the western and
  central basins and die-back in the delta"), and add the delta to `fit_reason`. Keep the fallback. MET-7 and the
  Tensions row forbid inventing a k or a threshold no source fixed, and melbourne_housing_market had its use-case
  wording fixed the same way.
* Why this outranks a re-target: the remedy ladder. Fix the text before re-targeting, and re-target before excluding.
  A colonisation target would rest on 18-32 positives per window (a TP-9 risk).

**3. The evaluation is honest (P4: LEAK-10, SPLIT-1, SPLIT-3, SPLIT-9, Must; SPLIT-10, Should).**

* Three agents found no leak:
  * every one of the 30 features is known at the prediction point, and missingness indicators move R^2 by only
    -0.001 to -0.007 (column auditor);
  * the history excludes the current visit, and the site features match the previous year in 98.97% of rows (blind
    reviewer, rebuilt from source);
  * no exact copies cross the split (leak probe 5).
* Temporal follows USE-10: 97.9-100% of each window's test rows are at a station seen in training. The record's
  `Grouped` is an AI triage value (commit 137c1694), and the later measured stage supersedes it. A cold-start mapping
  keeps 1-6% of the variance (split auditor).
* "No gap" is now measured. Season Y-1 is 91-100% in CIMS before season Y starts (Wayback copies, 2021-2025), and the
  labels have not changed since first publication. That is melbourne_housing_market's "no gap, measured", not an
  exception.
* The one slip: soil cores of season Y-1 are joined before CIMS posts them (15.2% of test rows). LEAK-10 is weak here.
  The remedy is a lag (LEAK-7): one line, RMSE 7.050 against 7.054. Adopt it. Also reword the prediction point to
  "before each season, once the last season is in CIMS".

**4. The data is faithful to its origin (P5: PROV, Must).**

* The blind reviewer rebuilt the target from the raw CSV: 69,150 of 69,161 rows match, and the other 11 are the trace
  codes set to 0.5.
* The claim auditor confirms the counts, codes, drops, coverage, windows and model numbers (claims 1-3, 5-10, 12-17,
  25-28 and 30-33). The refuted claims are wording (4, 22, 24, 41, 42), stale record fields (43) or points 1 and 2
  above.
* The dense-stand drop follows CLEAN-15 (Must): there is no target, because the program left `% Cover` empty. It also
  follows the eryhemato row: no target of our own invention.
* The program itself moved those visits out of the plot. In the November 2016 download they were in-plot cover (98.7%
  on average); by April 2021 they were "Out" with empty cover (split auditor). The current table is the program's own
  revision.
* Concede claim 11: "the estimates overstate" is not shown. The nearest earlier measurement averages 73.9%, and the
  2017 values follow the roseau cane scale die-back. Remedy: rest the drop on the program's revision and its own words
  ("may not be representative"), and name the die-back.
* Concede the USE-6 (Must) point the domain practitioner raises: the crew's estimate in the comment was known before
  the next season. Mildest fix:
  * add a flag "previous visit in an unentered dense stand", with the estimate as its own column;
  * leave `previous_phragmites_cover` at the last measured visit;
  * count those visits in `site_share_phragmites_nearby` (column auditor, problem 5).

  It touches 171 stations, mostly in the 2017 window.

**5. The task is worth benchmarking (P6: TP-4, TP-9, MET-2, Must).**

* Not Trivial: the raw carried-forward value loses in 9 of 9 windows. california_house_prices_2020 and aps_failure
  were kept on the same test (TP-4).
* Every window can be scored: 220-345 positive rows and 93-193 rows at 50% or more per window (claim auditor, claim
  33), far above TP-9's handful.
* Zero inflation is no reason to cut rows. Andrej, 2026-10-30: "We don't care. We want to add any relevant predictive
  task, independent if it is zero inflated or not." So the blind reviewer's drop of the swamp rows, or of the stations
  that never had reed, is not needed. Those zeros are the program's observations at stations a manager monitors.
* Modest headroom is no reason to retire (TP-2, forest_fires; the Tensions row "the right split against the score").

**6. The cleaning gaps are cheap and do not move the score (P7: CLEAN-1, CLEAN-11, CLEAN-22, Should).**

* Fix all of these, since each is cheap and safe (principles, step 3):
  * join the soil per variable: pH and salinity coverage goes from 59% to 96%, and LightGBM from 7.020 to 7.039,
    within SE 0.017;
  * leave "Bare Ground" and "Water" out of the species count;
  * set the three impossible values missing;
  * name the dropped columns.
* Keep the shrub and tree covers missing, not 0. A blank tree cover in 100% of swamp plots with 6-30 m heights means
  "not recorded" (column auditor, against the blind reviewer's 0-fill).
* Keep the 2017 window, with a SPLIT-20 note. Dropping a window for its score breaks SPLIT-21 (Must).

**7. Record housekeeping (no rule against the dataset).**

* Remove `No Good Target / Scientific Discovery`. USE-8 makes it the marker for fit None, and the fit is approximate.
  Refuted markers have been removed before (thyroid_discordant; ghcn_daily_precipitation, Andrej, 2026-10-30).
* Set `required_split` to Temporal and the year to 2026 (PROV-9; noaa_afsc, sf_permit_time). Accept the three
  warnings on their precedents (zillow_prize, diabetes_3 and the zero-inflation policy above).
* Replace "outside the species' range" with absence from habitat inside the range (claim 42).

</details>

<details><summary>Critic</summary>

**Critic: crms_phragmites_cover (opening brief, 2026-11-01)**

**Verdict: do not ship as defined.** The dataset's scope claim (TP-10 leg 1) was tested against the wrong comparator. Against the one the rule names, the margin is 1.5-1.9% and the model wins 5 of 9 windows. That is at or below the margin telemonitoring_parkinsons was retired with. The dataset can ship only if the decisive test in point 1 passes or the curator amends TP-10. Otherwise it is `No` with `Time-series (Forecasting)`. If it ships, points 2-4 are definition fixes needed first. Points 5-7 are notes and cheap fixes, and none of them is a reason to exclude.

```text
Verdict: don't ship as defined; ship after changes if point 1 passes, else No (Time-series (Forecasting)).
Validity: SEL-10/SEL-11 via TP-10 not shown (Must; 1.5-1.9% over the fitted own-series forecast, 5 of 9 windows);
  USE-1/MET-1 triggered, fix the use-case text; USE-6 triggered, fix the definition (dense-stand history);
  USE-3 wording and LEAK-10 weak (soil cores used before publication), fix by a lag; SPLIT-1/3, USE-10 hold
  (temporal); PROV-16/17 open (Guo et al. read from the abstract only).
Value: TP-4 holds (the raw last value loses 9 of 9); TP-1 open (no tuned or stronger model run).
Quality: CLEAN-1 soil join and species count, CLEAN-11 three values, undocumented drops: cheap fixes.
For the curator: point 1 is a Must; keeping crms at this margin is an amendment of TP-10, not an exception.
```

**1. The task is not shown to be tabular rather than forecasting (P2; SEL-10 and SEL-11 via TP-10, Must; TP-1, Must).**
- *Problem.* The definition says leg 1 holds because the random forest beats the raw carried-forward cover (6.93 against 7.75, 9 of 9 windows). TP-10 as amended on 2026-10-26 (rain_in_australia) lets the last observation stay only on one condition: "Leg 1 then carries the test: the model must clearly beat the forecasts built from the series itself". The Methods line "or its last value" is the older pattern, and a rule wins over a pattern (principles, Conflicts). In rain_in_australia the raw last value was the weakest comparator (0.661), not the bar (0.754).
- *Evidence.* Two independent runs on the shipped windows agree:
  - Claim auditor, claim 18: an isotonic curve of `previous_phragmites_cover`, fitted on each training side, scores 7.042. The RF (6.930) is 1.5% lower, ahead in 5 of 9 windows and above 2 paired SE in 3. LightGBM (7.025) ties the curve (mean relative RMSE 1.000).
  - Precedent checker, own run: previous cover alone, fitted by LightGBM, scores 7.062. The RF is 1.9% lower, ahead in 5 of 9, above 2 SE in 4. LightGBM is 0.5% lower, ahead in 4 of 9, and clearly worse in 2018 (gain -8.98, SE 3.01).
  - In the two newest windows, the most representative ones (SPLIT-11), the fitted last value scores as well as or better than both models: 2024, 7.75 against RF 7.94 and LightGBM 7.88; 2025, 8.15 against 8.15 and 8.19.
  - Domain practitioner: 28% of the RF's gain over the raw value comes from one linear shrinkage of last year's cover (7.51).
  - Without the station's reed history, LightGBM scores 7.88, worse than the raw carried-forward value (7.75).
  - Without the 2017 window, itself an artefact (point 3), the RF scores 6.891 against 6.975 for the fitted curve (1.2%).
- *Precedent.* telemonitoring_parkinsons was retired (Lennart, 2026-10-02). It also tracked a known entity: the best model scored 6.33 against 6.48 for the carried-forward value with drift, 2.3% lower. The reason: "the benchmark would rank models by how little they lose to a constant". crms sits at or below that margin and names no fact that sets it apart. The forest_fires row (TP-2) settles the split against the score (P4 over P6). It does not lift a P2 Must.
- *Also.* The leg 2 sentence "the only lag of the target is its last observation" is wrong. A running maximum, a running count and a site mean that includes the station also summarise the series (claim 19). Trailing summaries are allowed, so leg 2 holds, but the sentence needs fixing.
- *Effect.* As shipped, the benchmark would rank methods by a 1-2% edge over a fitted persistence curve. The RF loses that edge in 4 of the 9 windows, including the newest.
- *Remedy, mildest first.* Remove the claim that leg 1 holds. Then run the decisive test that the Methods ask for and the build skipped: a stronger gradient-boosting model (ashrae passed only with 1,000 trees), plus tuned results when the benchmark has them (TP-1). Compare them per window, paired, against the best forecast fitted on the station's own series. If they clearly beat it, ship. If not:
  - (a) Add the inputs the actor always has that are not persistence: continuous hydrology summaries, elevation, basin (domain practitioner; the bulk zips are live; gain untested). Then test again.
  - (b) The curator amends TP-10 to name the comparator and what "clearly" means.
  - (c) `No` + `Time-series (Forecasting)`, as for telemonitoring_parkinsons.

  Re-targeting to colonisation is not a ready fix. A three-term hand rule reaches ROC AUC 0.951 and AP 0.225, against the classifier's 0.964 and 0.215, with about 25 positives per window (dp2).

**2. The use case is not what RMSE scores (P3; USE-1, Must; P6; MET-1, Must).**
- *Problem.* The use case ranks stations "to flag emerging hotspots for control or closer monitoring". RMSE puts 82.6% of the model's squared error (85.7% of carried forward's) on plots that had reed at both visits, and 7.4% on colonisations (dp1). The claim auditor finds that the 7.8% of rows with reed at the last visit carry 90.8-92.6% of it. On colonisations, the RF's MSE gain over the fitted curve is about 0 (claim 34). And 34.9% of test rows with reed lie in the Bird's Foot Delta box. There cover fell 3.2 points on average, and the manager protects the reed (Delta-type lineage, die-back since 2016; domain practitioner). "For control" is wrong for a third of the signal.
- *Effect.* A reader of the leaderboard believes it measures an early warning. It measures next-season cover at plots that already hold reed, with spread and die-back mixed.
- *Remedy (text only, no metric change).* Reword `use_case` to what RMSE scores. The domain practitioner's wording: "between seasons, a CPRA manager forecasts each monitored station's reed cover at next summer's survey, averaged to sites, to track spread in the western and central basins and die-back in the delta". Add to `fit_reason` that the reed in the delta is protected. Keep `rmse`: no source fixes a threshold or k (MET-7), and site-year RMSE ranks eight models the same way plot RMSE does (Kendall tau 0.93). Precedent: melbourne_housing_market, whose use-case wording was fixed in the definition.

**3. The dense-stand visits are dropped from the history, though the manager had them (P3; USE-6, Must; SPLIT-20 and EV-6, Should).**
- *Problem.* In 2012-2016 crews could not enter 633 plots in dense reed. The definition drops these visits as rows, which is right since they have no measured target. It also drops them as history. But the crews' record that the plot sat in reed too dense to enter, with their estimate, existed before the outcome. Moreover, the November 2016 CIMS download held 518 of these visits as data, with in-plot cover averaging 98.7% (93% at 100%). By April 2021 the program had moved them to "Out" and emptied the covers (split auditor, Wayback copies). So the manager predicting 2017 had them as data. "The program left the cover fields empty" is true of today's download only.
- *The stated reason does not hold up.* The definition says "the estimates overstate: 57% in 2011, 47% in 2017". Per estimated visit, the nearest earlier measurement averages 73.9% (median 80; 37% at 90% or more). The 2017 values follow the roseau cane scale outbreak: "scale present" appears in 201 visit comments in 2017 and in none in 2006-2016 (claim 11).
- *Effect.*
  - In the 2017 window, 86-99 rows at these stations have their last measured visit in 2011-2015. They carry 66% of LightGBM's and 72-74% of carried forward's squared error (claim 29; split auditor).
  - 2017 is the window with the largest gain over persistence (30.2 MSE against 10.9 on average), so the drop inflates the margin in point 1.
  - The site nearby share loses the reed these crews saw outside the plot: it falls from 0.57 to 0.40 at 24 sites, and 159 rows of 2017 read it (column auditor).
- *Remedy (fix the definition).*
  - Keep the visits out of the rows and out of `previous_phragmites_cover`.
  - Add a flag for an unmeasured dense-stand visit since the last measured one, and the crew's estimate as its own column. The estimate is a number the program wrote and once published as data, not a text feature. USE-6: "a company's own estimate made before the outcome is an input".
  - Count those visits' reed-outside record in `site_share_phragmites_nearby`.
  - Base the drop on the program's own revision and the per-visit comparison, and name the scale die-back.
  - Add the 2017 re-entry note to `splits_comment`, and keep the nine windows (SPLIT-21).

  The builder tested only one alternative, the estimate as the previous cover, which is a different design.

**4. The prediction point, the soil timing and the gap are stated wrong (P3; USE-3, Must; P4; LEAK-10, Must, weak here; SPLIT-10, Should).**
- *Problem.*
  - The definition puts the prediction "after each summer's survey" / "at the end of a survey season". At the end of a season its data are mostly not in CIMS yet: 1.8% of 2023's visits were there on 2023-08-26, and our download of 2026-10-25 stops at 2026-07-30. The data arrive over the winter (91-100% by January-June), and the site porewater runs to 31 December.
  - The soil join takes cores sampled up to season Y-1, but CIMS posts cores 1 to 2.5 years after sampling. The 2019 and 2020 cores are absent from the 2021-04-29 download, and the 2021 cores from the 2022-05-13 one. 5,157 test rows (15.2%) use cores from Y-1, including 3,260 of the 3,827 rows in 2019 (split auditor).
- *Effect.* No effect on the score (7.050 against 7.054 with cores up to Y-3). But the text puts the moment of use in the wrong place, and the soil features give a slight look into the future.
- *Remedy.*
  - Text: the prediction point becomes "before each season, once the last season is in CIMS". `splits_comment` replaces "not checked" with the measured finding that no gap is needed (as in melbourne_housing_market; no exception needed).
  - Code: lag the soil join (`season_before = year - 3`, one line), as rain_in_australia keeps inputs from other rows "only where they are known by then".
  - If the curator reads the actor as a CPRA analyst who sees lab results before release (the domain practitioner says so, without a source), keep the soil as it is with a note.

**5. The paper behind the use case was read from its abstract only (P5; PROV-16 and PROV-17, Must; EV-2).**
- *Problem.* Every claim attributed to Guo et al. 2026 rests on the USGS abstract (Wiley answered 403, twice). The paper anchors the use case, the reason for the fallback metric and the lineage note. The phrase the definition quotes is not the abstract's wording (claim 24). The abstract says it "integrates Phragmites cover trends (expanding/stable/declining), concurrently measured native plant cover, and key soil and pore-water indicators to flag emerging hotspots and prioritize adaptive management". The definition's "native ones" should read "long-established noninvasive" lineages (claim 22).
- *Effect.* If the full text holds a per-plot model or a score, MET-5 reopens the metric and the wording of point 2.
- *Remedy.* Ask the curator for the PDF (PROV-17); no record shows that anyone asked. Until then, keep the "abstract only" marks, quote verbatim, and fix the lineage wording. One small ask with no Must behind it: write the SHA-256 of the porewater and soil files (in the run's hash list) into `download_description` next to the vegetation one. CIMS revises past records (point 3), so a later download is different data.

**6. Cleaning gaps an expert would fix (P7; CLEAN-1 and CLEAN-11, Should). Not a reason to exclude.**
- *Soil join.* It takes all six values from the latest sampling year, so later cores without pH blank a known pH. `soil_ph` and `soil_salinity_ppt` cover 1% of the rows in 2022-2025, against 96% when each variable is joined on its own. The missingness codes the period (column auditor; the blind reviewer found the same independently). Fix: one as-of join per soil column, together with the lag of point 4. The score does not change (7.020 to 7.039).
- *Species count.* `previous_species_count` counts "Bare Ground" and "Water" from the 2006 species list, so 1,615 rows count one species too many and 26 plant-free plots read 1. Leave those two names out of the count.
- *Impossible values.* One herb height of 1,219.2 cm, and three porewater salinities (90, 71 and 57 ppt) that contradict their own conductance (about 12.6, 7.1 and 5.8 ppt). Set them missing or add a note.
- *Undocumented drops.* The tree, shrub and carpet heights, the Braun-Blanquet rank, Group and the observed names are dropped without a word. Ship them or name each with its reason.

**7. Wording and record fields the data refute (EV-2, EV-7; PROV-9, SPLIT-3, USE-2/USE-8).**
- *Definition.* The rows hold 60 station-years with two visits, not 63. `visits_with_phragmites_before` counts station-years, not visits.
- *Record text.* "4,476 visits with cover" should be 4,488. "Outside the species' range" is refuted: sites that never had reed span the same longitudes, and 58.7% of their visits are in fresh, intermediate or brackish marsh. The zeros are absence from habitat the reed has not colonised.
- *Record fields.*
  - year: 2006 to 2026 (PROV-9, the snapshot year).
  - `required_split`: Grouped to Temporal (USE-10, SPLIT-3). Every report agrees; the curator picks.
  - The marker `No Good Target / Scientific Discovery` contradicts `Yes` and fit approximate. Remove it if point 1 passes; otherwise replace it with `Time-series (Forecasting)`.

**Dropped from my case.**
- The blind reviewer's swamp-row drop and restriction to sites with reed: the zeros are real absence, they cost RMSE nothing, and the curator's policy of 2026-10-30 keeps them.
- Filling the shrub, tree and carpet blanks with 0: tree cover is blank even in swamp plots with tall trees, so a blank means "not recorded", not zero, and CLEAN-2 forbids imputation.
- The licence warning: there is no evidence of an objection (P1).
- The regime: temporal is right, and all six reports agree.

</details>

<details><summary>Advocate rebuttal</summary>

**Advocate: crms_phragmites_cover, rebuttal (2026-11-01)**

**Where we stand.** I concede points 2-7 of the critic's brief, with two narrowings. Point 1 comes down to one fact:
which forecast is the bar. I ran a check for it: the comparator ladder (script and
log in the run folder). The critic's bar, a curve of the last value fitted across all stations, is the only one on which crms
fails. On the bar the curator used in the closest precedent, crms passes clearly.

**1. TP-10 leg 1: narrowed to the comparator; conceded on the critic's bar.**

* The check. These are the auditors' untuned RF and LightGBM, scored paired over the nine shipped windows against
  each candidate bar:

  | bar (RMSE over the 9 windows) | RF lower by | RF windows won | windows above 2 SE / below -2 SE | without 2017 |
  |---|---|---|---|---|
  | raw last value, 7.747 | 10.5% | 9 of 9 | 8 / 0 | 9.4%, 8 of 8 |
  | last value plus the training rows' mean drift, 7.747 (telemonitoring_parkinsons' bar) | 10.5% | 9 of 9 | 8 / 0 | 9.4%, 8 of 8 |
  | pooled linear shrinkage of the last value, 7.512 | 7.7% | 9 of 9 | 6 / 0 | 7.0%, 8 of 8 |
  | best of nine forecasts from each station's own series (EWMA 0.7, picked on the windows), 7.401 | 6.4% | 9 of 9 | 3 / 0 | 5.0%, 8 of 8 |
  | isotonic curve of the last value fitted across stations, 7.042 | 1.6% | 5 of 9 | 3 / 0 | 1.2%, 4 of 8 |

  LightGBM is lower by 9.3%, 6.5% and 5.1% on the middle three bars (8, 7 and 8 of 9 windows), and by 0.25% on the
  isotonic curve (4 of 9).
* Contested: the precedent. The critic cites telemonitoring_parkinsons as the like case. Its record (CC 2026-10-02,
  Lennart) names the bar: "carrying it forward gives RMSE 6.98, adding the training subjects' mean drift 6.48, a ridge
  on voice plus baseline 6.33 and LightGBM 7.32".
  * Applied to crms, that bar is 7.747. The RF beats it by 10.5% in 9 of 9 windows, and LightGBM by 9.3%. There, the
    margin was 2.3% and LightGBM lost to the carried value.
  * Treat like cases alike (principles, Conflicts): on the precedent's own bar, crms is the opposite case.
  * The other facts differ too. telemonitoring was retired because "the voice features carry almost no information
    about UPDRS across subjects", with 42 subjects. It was recast as warm start only after the grouped task failed
    (SPLIT-28).
* Contested: "the comparator the rule names". SEL-11 (Part 1, Must) names "each entity's naive profile". TP-10's
  amended sentence says "the forecasts built from the series itself". Every bar in rows 1-4 is that, and crms clears
  each one in 9 of 9 windows.
  * The isotonic curve is a nonparametric model learned from 35,000-65,000 rows of about 4,000 stations. No curator
    precedent used a bar that strong.
  * rain_in_australia's 0.75 forecast is "a naive forecast" in its record. The record does not say whether it was
    fitted across locations. Its 0.10 AUC margin decided the case either way, so it does not settle this one.
* Conceded: on the isotonic bar, leg 1 is not clearly met.
  * The RF is 1.6% lower, wins 5 of 9 windows and loses the two newest (2024: 7.94 against 7.76; 2025: 8.15 against
    8.13). LightGBM ties.
  * The decisive test the critic asks for is already run, and it went against crms. LightGBM early-stopped on the last
    training season (3 seeds) scores 7.05-7.13 against the curve's 7.04. The stronger model does not
    widen the margin, so TP-1 rescues nothing on current evidence.
* Narrowed: "without the reed history LightGBM scores 7.88" is not the leg 1 test. TP-4 expects the natural core to
  dominate. Leg 1 asks whether the full model beats the series forecasts. On the question of what the other features
  add, the RF goes from 7.29 on the station's history alone to 6.93 with all features (claim auditor).
* Leg 2 wording (claim 19): conceded. Change it to "the last observation and trailing summaries of the station's
  series".
* What follows. This is the curator's call and an amendment of TP-10 either way (we agree). My ask is TP-10 option
  (d), naming the comparator as the entity's own-series forecasts, with telemonitoring's mean-drift bar as the floor.
  If the curator names the fitted curve instead, I accept the critic's ladder in its order:
  * (a) add the hydrology, elevation and basin inputs and test again (mildest, it keeps the dataset);
  * (b) the amendment;
  * (c) `No` + `Time-series (Forecasting)`.

**2. The use case against RMSE: conceded.** The remedy is the same as in my opening point 2: reword `use_case` to the
domain practitioner's text, add the delta to `fit_reason`, and keep `rmse` (MET-7; melbourne_housing_market).

**3. The dense-stand history: conceded, with one narrowing.**

* Conceded:
  * the USE-6 flag, with the crew's estimate as its own column;
  * those visits counted in `site_share_phragmites_nearby`;
  * the drop based on the program's own revision (in-plot at 98.7% in the November 2016 download, "Out" by April
    2021);
  * the scale die-back named;
  * the 2017 note in `splits_comment`, with all nine windows kept (SPLIT-21).
* Narrowed: "the drop inflates the margin in point 1" holds against the isotonic curve only. Without 2017, the RF still
  beats the own-series bar by 5.0% and pooled linear shrinkage by 7.0%, in 8 of 8 windows (table above).

**4. Prediction point, soil timing, gap: conceded.**

* Text: "before each season, once the last season is in CIMS".
* `splits_comment`: the measured no-gap finding, as in melbourne_housing_market.
* Code: the soil lag, `year - 3` (LEAK-7; RMSE 7.050 against 7.054).

**5. The paper read from its abstract only: conceded as an action, narrowed as an obstacle.**

* Ask the curator for the PDF (PROV-17), quote the abstract verbatim (claim 24), and write "long-established
  noninvasive" (claim 22). Add the SHA-256 of the porewater and soil files to `download_description`.
* Narrowed: PROV-17 itself lets the work go on with the claims marked unverified, and the definition marks every Guo
  et al. statement "read from the USGS abstract only". The data's first publication is CPRA's CIMS, not the paper, so
  P5 faithfulness of the data does not rest on it. MET-5 reopens only if the full text shows a score.

**6. Cleaning gaps: conceded.** Join the soil per variable, take "Bare Ground" and "Water" out of the species count,
set the three impossible values missing, and name the dropped columns. None moves the score.

**7. Wording and record fields: conceded.**

* Wording: 60 station-years, not 63; `visits_with_phragmites_before` counts station-years; 4,488, not 4,476; the
  zeros are absence from habitat inside the range.
* Record fields: year 2026, `required_split` Temporal.
* The marker `No Good Target / Scientific Discovery` goes. If point 1 ends in `No`, it is replaced by
  `Time-series (Forecasting)`, as the critic says.

**Agreed by both sides:**

* temporal is the right regime;
* there is no leak beyond the soil timing;
* the zeros and swamp rows stay;
* the blanks stay missing;
* the licence warning is accepted;
* the fallback `rmse` stays.

The panel's one open question for the curator is the TP-10 comparator.

</details>

<details><summary>Critic rebuttal</summary>

**Critic: rebuttal to the advocate (2026-11-01)**

**Where we stand.** The advocate and I agree in substance on points 2-7 of both briefs: the use-case rewording, the soil lag and the prediction-point text, the dense-stand flag (USE-6), the cleaning fixes and the record fields. The one dispute is TP-10 leg 1. A new check settles the advocate's factual claim there: the bar the advocate calls "learning across entities" is a persistence rule with three numbers. My verdict stays. Ship only if the curator amends TP-10 to the per-entity reading; otherwise `No` + `Time-series (Forecasting)`.

**New check.** Mine, untuned, so these are probe numbers (EV-8); script and log in the run folder. It runs on the claim auditor's cached frame and the shipped windows, with the RF configured as the claim auditor configured it.

| forecast from the station's own last reed cover | pooled parameters | mean RMSE | RF lower by | RF wins | RF > 2 paired SE | RF < -2 SE |
|---|---|---|---|---|---|---|
| raw last value | 0 | 7.746 | 10.5% | 9 of 9 | | |
| last value + training mean change (telemonitoring's form) | 1 | 7.747 | 10.5% | 9 of 9 | | |
| a + b x last | 2 | 7.512 | 7.7% | 9 of 9 | 6 | 0 |
| about 0.08 where the last cover was 0, else about 16 + 0.62 x last | 3 | 7.045 | 1.6% | 6 of 9 | 3 | 0 |
| isotonic curve of the last value (claim auditor) | step function | 7.042 | 1.5% | 5 of 9 | 3 | 0 |
| best per-station forecast: EWMA 0.7, picked on the test windows (advocate) | 0 | 7.401 | 6.4% | 9 of 9 | 3 | 0 |
| RF on all features | | 6.930 | | | | |

The three parameters of the two-regime rule barely move between windows (slope 0.62-0.68, intercept 15.4-17.6, zero level 0.08-0.09).

**Advocate 1 (TP-10 leg 1): dispute, narrowed to the comparator.**
- *Concede the facts.* The RF is 6.4% below the best unshrunk per-station forecast, 9 of 9 windows.
- *"The isotonic curve is learning across entities": refuted.* A damped persistence with a zero regime meets the same bar (7.045). It has three numbers that barely move between windows, and it reads only the station's own last value. That makes it a forecast built from the series: AR(1)-like mean reversion, the standard forecasting baseline, with a plot that had no reed kept near zero, as any forecaster would do on this target.
  - The advocate's 6.4% is mostly regression to the mean of ocular estimates. About 76% of the RF's gain over the EWMA (0.36 of 0.47 RMSE) is reached by this rule.
  - What the other 29 features add over the station's last value is 1.5-1.6%. The RF is ahead in 5-6 of 9 windows, and above 2 SE in 3.
- *Pooling a parameter is not what TP-10 rules out.* The curator's own bar in telemonitoring_parkinsons was "carrying it forward ... adding the training subjects' mean drift" (CC 2026-10-02, Lennart). That is a parameter pooled over entities. In fairness: that exact form scores 7.747 here, and the RF beats it by 10.5%. On a bounded, zero-heavy cover the form that matters is the shrinkage, not a drift.
- *"Naive" in SEL-11.* The advocate cites rain_in_australia's 0.75 comparator as "a naive forecast". It was "a regression of the amount" from the location's own rain series with a > 1 mm rule (TP-10 Cases; rain_in_australia `dataset.py`). So the curator used "naive" for a fitted forecast from the series.
- *SEL-11 against TP-10: there is no conflict for the higher part to win.* SEL-11 says a panel "is in scope when it passes TP-10", so it hands the test to TP-10. Its summary also says "the source's top solutions used no lagged target", the wording from before the 2026-10-26 amendment. Read as the governing text, that clause would fail crms outright: the previous cover, its running maximum and its count are lags of the target. The amendment that lets the last observation stay sets the condition: "Leg 1 then carries the test: the model must clearly beat the forecasts built from the series itself."
- *Colonisation AUC 0.956.* TP-10 measures leg 1 "by the task's declared metric". Under RMSE, the RF gains about nothing on colonisations over the fitted curve (claim 34). A ranking skill the metric does not score cannot carry leg 1.
- *TP-4 and `one_feature`.* Agreed, the task is not `Trivial`. But TP-4 decides a retirement marker, not scope, so it does not answer TP-10.
- *The telemonitoring distinction: concede in part.* Here every family beats the raw value, while there LightGBM lost to it. But the curator's stated reason was the margin over the adjusted carry ("rank models by how little they lose to a constant"). Here LightGBM ties the fitted curve (0.5%, 4 of 9 windows). The advocate's own stronger LightGBM (early-stopped, 3 seeds) scored 7.05-7.13, worse than the three-number rule, and fell below -2 SE in 2 windows. The stronger test that TP-1 and the TP-10 Methods ask for went against the task.
- *Where we agree.* This is the curator's call, by amendment (precedent checker, prompt 1 (d)).
- *Where we differ: what holds until then.* TP-10 is a Must, and the reading the definition needs is not written into it. A Must takes no exception (principles, "Exceptions and amendments"). Until an amendment names unfitted per-entity forecasts as the bar, leg 1 is not met and the verdict is `No`. My remedy is unchanged:
  - (a) try the inputs the actor has that are not persistence (continuous hydrology, elevation);
  - (b) the amendment;
  - (c) `No` + `Time-series (Forecasting)`.

**Advocate 2 (use case and metric): concede.** We propose the same rewording and keep `rmse`. One note: the rewording drops the "early warning" Guo et al. recommend, which is the use case's only anchor in the source. The fit stays approximate (USE-8), and PROV-17 stays open (my point 5).

**Advocate 3 (honest evaluation): concede** the no-leak findings, the temporal regime, the measured no-gap finding, the soil lag and the prediction-point text. I narrow one sentence. "The labels have not changed since first publication" holds for 2019-2023 (split auditor). It does not hold for the 2012-2016 dense-stand visits: between 2016 and 2021 the program moved them from in-plot cover to "Out" with empty cover. Write the sentence that way (EV-7).

**Advocate 4 (faithful data): concede** the target rebuild (99.98% of rows) and the CLEAN-15 row drop, and accept the advocate's concessions on claim 11 and USE-6. I narrow "PROV holds": it holds for the data. For the paper, PROV-16 and PROV-17 (Must) stay open: the quote is not verbatim, every Guo et al. claim rests on the abstract, and no record shows the PDF was asked for (my point 5). The advocate did not address this.

**Advocate 5 (worth benchmarking): concede** TP-4, TP-9 (220-345 positives per window), MET-2 and the zero policy. **Dispute** one citation. TP-2 and the Tensions row "the right split against the score" settle P4 against P6; they do not lift a P2 Must (principles, step 4: independent failures are not conflicts). My point 1 is about scope, not headroom.

**Advocate 6 (cleaning): concede.** These are the same fixes as my point 6.

**Advocate 7 (record): concede** the year, `required_split` and the range wording. I narrow the marker. Remove `No Good Target / Scientific Discovery` in any case (USE-8: the fit is approximate, not None). If point 1 fails, the marker is `Time-series (Forecasting)`.

**For the mediator.**
- *Fact, settled.* The bar is a three-number persistence of the station's own cover (7.045). The features beat it by 1.6%: ahead in 6 of 9 windows, above 2 SE in 3, below -2 SE in none.
- *Open, a weighing call for the curator.* Does TP-10's "forecasts built from the series itself" include a fitted shrinkage of the last value? Then the margin is not "clearly". Or does it mean only unfitted per-entity forecasts? Then leg 1 holds at 6.4%, 9 of 9. Either answer is an amendment of TP-10.

</details>
