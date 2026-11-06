# noaa_afsc_bottom_trawl_survey_cpue

**Outcome:** added. The AI recommends shipping it; after the panel one column was repaired from the origin and the
text fixed, with rows, target, split and metric unchanged. The data are NOAA AFSC's summer bottom-trawl hauls from the
public FOSS tables: 35,549 hauls of 1982-2026 in five survey regions. The target is the haul's rex sole catch in
numbers per km^2 swept (62% zero), scored by RMSE, the rule by which the 2022 essential fish habitat (EFH) review
picks and weights its models. The prediction is for a place in a survey year, from the region, design stratum,
position, date, depth and that year's temperatures there. The split is temporal: three five-year windows, as the EFH
review recurs every five years, each trained on the surveys up to two years before it.

**Changed (2026-11-02, on Andrej's marks):** the table now holds 11 taxa, one row per haul and taxon (391,048 rows,
52.5% zero), with `taxon` as a feature (issue 1). The split has nine two-year windows without a gap (issue 2). The
metric is the source's RMSE taken per taxon over the taxon's spread and averaged (`mean_group_normalized_rmse`,
issues 1 and 3); flathead sole is grouped with Bering flounder. The panel's reports below were written for the
rex sole table and the five-year windows.

Validity:
* USE-1 holds: the EFH review is set by law. USE-5 holds for any managed species of the surveys, so the species is a
  weighing call (issue 1). USE-8: fit approximate (no habitat layers such as sediment or currents; regions and life
  stages pooled).
* USE-3 was broken in the text, which described a review forecasting later hauls while feeding it each haul's own
  temperatures. Fixed by naming one prediction point, a place in a survey year under that year's conditions: the
  temperatures stay (no measured gain; to be decided with wadden_sea_sibes_macoma_abundance issue 5, where sediment
  measured at the visit carried a gain and was replaced by interpolated values), the date stays because the survey
  schedule sets it, and the vessel and the hour leave because a place-year has neither, so USE-6 holds without an
  exception.
* LEAK-10 holds for all 8 features.
* SPLIT-1 and SPLIT-3 wait for your pick of the regime (issue 2). SPLIT-15 is departed from (three windows, not nine),
  forced by SPLIT-12 and SPLIT-14: a fourth window would train on 43.6% of the hauls.
* SPLIT-20 triggered: the Gulf of Alaska survey got new stratum numbers in 2025, so its 431 hauls of that year (10% of
  the newest test window) carried codes no training row had. Repaired from the origin with GAP's polygons of the old
  strata (newest window R^2 0.607 to 0.726; CLEAN-21, as college_scorecard).
* PROV holds: every target was rebuilt exactly from the API, and the haul counts match the 2022 memo. EV-7: FOSS has
  not yet rated the 2026 season (17% of the newest window); a fresh download is compared before a build.

Value: MET-5 and MET-11 hold. MET-2 is met with a note: the Gulf of Alaska holds 71-93% of the squared error with
23-40% of the test hauls. A region-averaged RMSE, the critic's and the domain practitioner's option, still leaves the
Gulf 45-63% of it (the mediator's measure, before the repair), and a scale-free score per region would be a metric of
our own (TP-6), so the mediator kept the note.

Quality: CLEAN-22, each drop reason now says what the column is; CLEAN-8, the notes say the species was screened on all
years, test windows included; CLEAN-21, a note on the 1993-95 depths.

Weighed: NOAA's documented tables +; a real use case +; an approximate fit -; a strong spatial baseline (k-NN on
position alone scores close to LightGBM) -.

Left for Andrej: issues 1 and 2. The mediator closed the precedent checker's two consistency checks (`stratum`, and the
vessel and hour). Not verified: whether FOSS revises the 2026 season, Pirtle et al. 2020 and the 2023 Gulf of Alaska
memo. The numbers of the notes and of issue 2 were measured again on the repaired frame, so some differ from the
panel's (temporal mean R^2 0.694 in the split auditor's setup, not 0.652).

**Main points:** All four issues are settled (1 to 3 on 2026-11-02, 4 on 2026-11-06).

**Verdict (2026-11-02, Andrej):** ship. The metric is marked as declared (`mean_group_normalized_rmse`). The
dataset joins the accepted set; a build waits for your ask.

**Issues for Andrej:**

1. **Keep rex sole as the species?** The target is one species' catch, and the source names none: the EFH memos
   model 31 to 36 species each. The definition takes rex sole, chosen from 22 species probed on these hauls.
   * What it changes: the species decides what a model has to learn. Rex sole is caught in 19.5% of eastern Bering
     Sea shelf hauls, 49.1% on the slope, 66.8% in the Gulf of Alaska and 38.7% in the Aleutians, and never in the
     northern Bering Sea (2.7% of the rows). So a model must find where inside each region it lives, the habitat
     question the review asks. For Pacific cod (4% zeros on the eastern Bering Sea shelf) the region carries most of
     the presence signal, and walleye pollock's absences are mostly whole regions.
   * For rex sole:
     * it is modelled in the 2017 Bering Sea memo (hurdle model, pp. 48-49) and again in the 2022 Bering Sea and
       Aleutian memos;
     * every catch of 1982-2025 is rated high confidence, and presence is steady over the years, so the early zeros
       are absences;
     * both parts can be learned: ROC AUC 0.94-0.96 for a catch and R^2 0.30-0.38 among catches (untuned, three
       windows).
   * Your call of 2026-10-30 (policy 2 of the zero-inflated review) makes zero inflation no criterion, and these
     reasons stand without it. The species was screened on the whole table, test years included; the notes now say
     so (CLEAN-8).
   * Rule: USE-5 (Must) holds for any managed species of these surveys, so which one ships is a weighing call. The
     same-run siblings take the species their source names; this source has no primary one.
   * Implemented: rex sole. Cost: a smaller fishery than cod or pollock, picked with the test years in view (now
     in the notes).
   * Alternatives: Pacific cod or walleye pollock, the larger fisheries, each with its own EFH maps (one constant and
     a new catch download). Or a second species as a sibling dataset, a distinct task on the same hauls (PROV-6,
     PROV-7).

   Recommendation: rex sole. Decision: rex sole, another species, or rex sole plus a second species as a sibling
   dataset?

   **Andrej (2026-11-02, discuss):** Is this actually a multi-target regression if we would use multiple species?

   **Answer (AI, 2026-11-02):** Yes. One haul with the catch of several species is one row with several targets, a
   multi-output regression, and it is what the EFH memos fit species by species (31 to 36 models per review). Data
   Foundry has no multi-target task: `problem_type` is binary, multiclass or regression, one target column, and the
   benchmark scores one prediction per row. So several species can ship in two ways. (a) One dataset per species, each a
   regression on the same hauls (the sibling option above): distinct tasks under PROV-6 and PROV-7, since each species'
   habitat is its own question, though the inputs are shared. (b) A long table, one row per haul and species, the
   species a feature: a joint species distribution model, which the memos do not fit; the hauls' rows then repeat across
   species, so the split must keep a haul's rows together. (a) stays closest to the source. The recommendation is
   unchanged: rex sole now; a second species, if you want one, as a sibling dataset.

   **Andrej (2026-11-02, change):** Instead of a single species or a multi-target problem, add species as a feature
   and use multiple species as samples. Which species should we use, which exclude or group in such a setup?

   **Answer (AI, 2026-11-02):** A long table, one row per haul and species with `species` as a categorical feature,
   fits the API (one target) and has a precedent: sat11_hand_algo_runtime ships instance x algorithm rows as "an
   alternative to multi-target modelling" (Lennart). The temporal windows keep a haul's rows together (SPLIT-23).
   Four criteria pick the species, none of them a model score, so the choice does not look at the test windows
   (CLEAN-8): the survey identified the taxon the same way over 1982-2026; the bottom trawl samples it as the
   survey intends; it is a managed groundfish with an EFH map; it is caught in more than one region.
   * Use (11 taxa, 391,000 rows): walleye pollock, Pacific cod, sablefish, Pacific halibut, flathead sole, rex sole,
     Dover sole, Greenland turbot, shortspine thornyhead, and two groups below.
   * Group: arrowtooth and Kamchatka flounder as *Atheresthes* (codes 10110, 10111, 10112), told apart only from
     about 1992 (Laman et al. 2017, p. 7); northern and southern rock sole as *Lepidopsetta* (10260, 10261, 10262),
     split from 1996. As groups their early zeros are absences.
   * Exclude:
     * Pacific ocean perch and Atka mackerel: schooling, off-bottom fish whose catch sits in a few hauls (10 hauls
       hold 41% and 40% of each one's squared deviation). Together they are 79% of the variance of the 22 probed
       species on counts per km^2.
     * Alaska, Aleutian and Bering skate: named to species only from 1999, so the earlier zeros are not absences.
     * Big skate (3.7% of hauls) and giant octopus (6.4%, octopus identification uneven).
     * The sculpins and yellow Irish lord: no fishery, kept only if you want breadth over management relevance.
   * The metric changes with the table (issue 3). Pooled over the 11 taxa, RMSE on counts per km^2 is 60% walleye
     pollock and 29% rock sole by variance; on the log1p scale each taxon holds 3-16%. The source scores RMSE per
     species and never pools them, so a pooled RMSE on counts would no longer mean what the source's means (MET-2,
     Must). Options: (a) RMSE on the shipped log1p target, no inverse: every taxon counts; (b) RMSE on counts with a
     note, as the Gulf of Alaska share is noted now: in effect a pollock and rock sole score; (c) RMSE per species,
     averaged: a metric of our own (TP-6).
   * Pair to decide alike: nantucket_sound_sea_duck_aerial_survey_counts issue 3 (the long-tailed duck alone; the
     source models three groups apart and names none first) cites this issue as its precedent. A long table there
     too, or the difference written down: three groups only, and the eider scores R^2 -0.08 held out.

   Recommendation: the 11 taxa above, scored by (a). Decision: this list (or which taxa to add or drop), and (a), (b)
   or (c)? Then I rebuild the definition, rerun the checks and probes, and measure the windows of issue 2 on it.

   **Andrej (2026-11-02, change):** I go with the 11 taxa you suggest. Regarding rmse on log1p, I am not so sure.
   Explain what the decision value function of the use case would be and how it would align with the metric.

   **Answer (AI, 2026-11-02):** Implemented: the 11 taxa, one row per haul and taxon (391,048 rows, 52.5% zeros),
   `taxon` a feature, the nine windows of issue 2. `dataset check` is clean, and the probes raise no flag (random
   forest skill +0.79; each haul's 11 rows stay on one side). Mean R^2 on log1p per taxon runs from 0.46 (walleye
   pollock) to 0.76 (shortspine thornyhead), untuned LightGBM over the nine windows. The metric is still RMSE on counts
   after the inverse, pending your call.

   *The decision value function.* The 2022 review draws one map per species and life stage (TM-459, pp. 25-28):
   * Occupied habitat: the places where the predicted chance of a catch is at least 5%.
   * The EFH area: the part of it holding 95% of the species' predicted abundance, the legal definition ("the area
     inhabited by 95% of a species' population", NMFS 2005, quoted p. 1). Inside it, the areas with the top 75%, 50%
     and 25% (principal, core, hot spots).

   So what a prediction is worth has three parts:
   * Each species' map counts on its own. Errors on pollock do not trade against errors on Dover sole.
   * Within a species, the cut depends on where the abundance is. Misplacing a dense area moves the 95% line more
     than missing a sparse one, so large catches matter more, in proportion to their share of the species' total.
   * At the low end, only telling presence (a 5% chance) from absence matters, not the size of a small catch.

   The memo itself notes that "the EFH maps produced in this project are based on ranked percentiles of abundance"
   (p. 24).

   *How each option fits it* (untuned models on the nine windows):
   * (b) RMSE on counts, pooled. It fits the within-species weighting. It does not fit across species: walleye
     pollock and rock sole hold 79-93% of the squared error in every window, and seven taxa hold under 1% each. It
     picks the model that is worst for the other maps: LightGBM fit on raw counts scores best under it (8,795 against
     9,487 for LightGBM on log1p), yet its error per taxon is 1.69 times the taxon's spread, against 0.91 for the
     log1p model and 1.08 for each taxon's training mean.
   * (a) RMSE on log1p. It fits across species, as each taxon holds 3-16% of the error. It fits the presence part. It
     misses the within-species weighting: a dense area misjudged by a factor of 2 costs as much as a sparse one, while
     the 95% line is set by the dense ones. It also departs from MET-3 (Must: score on the source's scale), so it
     would need an exception.
   * (c) RMSE on counts per taxon, divided by that taxon's spread in the test window, averaged over the 11 taxa
     (equivalently the mean over taxa of sqrt(1 - R^2) on counts). Each map counts once, and inside each map the
     source's own RMSE on counts weighs the dense hauls. It fits all three parts. It ranks the four probe models
     log1p LightGBM (0.91), Poisson LightGBM (0.96), taxon mean (1.08), raw LightGBM (1.69); its ranking of
     the four against (b) has a Kendall tau of -0.33 to 0.67 per window. Cost: a metric of our own. It would need:
     * the code in the metric library with tests (MET-13);
     * the taxon as the metric's group while it is also a feature, which MET-2 allows today only for the time column
       and for a weight (an amendment like the one for liberty_mutual_fire_peril_loss_cost);
     * a rule for a taxon with no catch in a window (none so far: every taxon is caught in every window).
   * (d) Spearman's rho per taxon, averaged. The review reports it because the maps rank abundance (p. 24). It fits
     the ranking part, but ignores the presence cut and how far off a prediction is. The review selects by RMSE, not
     by rho.

   Recommendation: (c), the review's RMSE taken per species and given one vote per map. It changes my earlier (a).

   *One more point on the list.* FOSS rates flathead sole only "moderate" confidence in every eastern and northern
   Bering Sea catch (12,309 of 12,576; "high" in the Gulf, the Aleutians and on the slope). There it is told apart
   from Bering flounder (*Hippoglossoides robustus*, 4,296 catches, all "moderate", not in the set). This is the case
   the first criterion (the same identification over the years) groups, as for *Atheresthes*. Suggestion: flathead
   sole with Bering flounder and unidentified *Hippoglossoides* (codes 10130, 10140, 10129), still 11 taxa. Not done,
   since you accepted the list as it was.

   Decision: (a), (b), (c) or (d); and flathead sole alone or as *Hippoglossoides*?

   **Andrej (2026-11-02, change):** I follow your suggestions. Please don't forget to properly document.

   **Resolved (2026-11-02, Andrej):** (c) and *Hippoglossoides*, implemented and re-measured:
   * Metric: `mean_group_normalized_rmse`, a new library metric (tested against a per-group scikit-learn RMSE to
     1e-9, by hand, 0.06 s on 1M rows), declared a stand-in for TM-459's RMSE per species, with `taxon` as its group
     and a feature. MET-2 now allows that: its two exceptions of today merged into one at this third case (metrics.md,
     with a Cases row). On the nine windows LightGBM on log1p scores 0.90-0.93 and beats each taxon's training mean
     (1.01-1.23) in all nine.
   * Taxa: flathead sole, Bering flounder and unidentified *Hippoglossoides* form one taxon; still 11 taxa, 391,044
     rows, 52.0% zeros. `dataset check` clean (the zero-share warning); the probes raise no flag.
   * Documented: `dataset.py` (taxa, metric, prediction point, split and their reasons), the generated README, the
     record (CC and Assessment of 2026-11-02), metrics.md and splits.md (Cases), the working copy's CHANGELOG.

2. **Confirm the temporal split over a split by station?** SPLIT-1 leaves the regime to you. Your CC of 2026-10-30
   records only `Yes`, priority 5, and the screening named temporal by survey year with grouped by station as the
   alternative.
   * What it changes: the temporal windows test later survey years, mostly at places sampled before. 85% of the test
     hauls are at a station seen in training: all eastern Bering Sea test hauls, and 40-65% in the Gulf of Alaska,
     whose stations are drawn anew for each survey. A split by station would test unsampled places in the same
     years. Mean R^2 on log1p (untuned LightGBM, the split auditor's setup, all three re-run with the repaired
     `stratum`): 0.694 temporal, 0.687 by station, 0.732 random (the source's own cross-validation). Before the
     repair the temporal windows scored 0.652, the figure the panel reports.
   * For temporal: a review's maps stand for the five years until the next review (50 CFR 600.815(a)(10)). The 2022
     review "assessed the forecasting accuracy of the 2017 SDM approach"
     ([Laman et al. 2022, TM-459](https://repository.library.noaa.gov/view/noaa/48659), p. 3). The same team tests
     its models by retrospective forecasts
     ([Barnes et al. 2022](https://repository.library.noaa.gov/view/noaa/49312)).
   * For grouped: the review's own skill test is random 10-fold cross-validation, "a test of prediction skill at
     unsampled locations" (TM-459, p. 21). wadden_sea_sibes_macoma_abundance (same run, not yet reviewed) groups by
     station for a map drawn between the stations of one surveyed year.
   * What sets this case apart from wadden_sea_sibes_macoma_abundance: each map here stands for five future years
     and is checked against them.
   * The advocate, the split auditor and the domain practitioner prefer temporal; the critic does not contest it.
   * Rule: SPLIT-1 and SPLIT-3 (Must): one regime, the one the use case implies.
   * Implemented: temporal, three five-year windows (2022-2026, 2017-2021, 2012-2016), each trained on the surveys up
     to two years before it. A fourth window would train on 43.6% of the hauls, below SPLIT-14's floor. Cost: only
     15% of the test hauls are at unsampled stations.
   * Alternative: grouped by station, 3 folds. Cost: the test no longer checks later years, the check the next review
     makes.

   Recommendation: temporal. Decision: temporal or grouped by station?

   **Andrej (2026-11-02, discuss):** Temporal sounds good. But why did you choose these exact windows? Which other
   windows could be good?

   **Answer (AI, 2026-11-02):** The windows copy the review the task serves. Each test window is five years because a
   review's maps stand for five years until the next review (50 CFR 600.815(a)(10)); the two-year gap is the lag between
   the last survey a review used and the review (the 2017 review used surveys to 2014, the 2022 review to 2019). Three
   windows because SPLIT-14 needs every training side to hold at least 50% of the hauls, and a fourth five-year window
   would train on 43.6%. Other windows that would be defensible: (b) the two real reviews only, train to 2014 and test
   2017-2021, train to 2019 and test 2022-2026: closest to the source, but two windows, below SPLIT-14's three. (c)
   One-year windows, each survey year tested on all hauls up to two years before it: the yearly survey's own question
   (next summer's catch at a place), and as many windows as SPLIT-15 asks (nine for this size), but no review uses a
   one-year horizon, and adjacent windows share almost all their training rows. (d) Five-year windows without the gap:
   more training data, but the model would see surveys the review could not. The recommendation stays the implemented
   windows; (c) is the one worth measuring if you want more, shorter windows.

   **Andrej (2026-11-02, change):** Temporal is good, but there is no need to do five years. Also no planning gap is
   required. Instead of five years, I suggest 2.

   **Answer (AI, 2026-11-02):** Two-year windows fit the survey's own cycle: since 2005 the Gulf of Alaska is
   surveyed in odd years and the Aleutians in even years, so two years is the shortest window that holds every
   region once. Without a gap, nine windows keep half the hauls for training (2025-26 back to 2009-10, trained on
   95% to 54%; 2007-08 would train on 49%), the nine of SPLIT-15 (corrected 2026-11-02: first counted as eight). The
   2019-20 window holds only 2019 (no survey in 2020). With the two-year gap, 2009-10 would fall below the floor,
   leaving eight. Not yet implemented,
   for two reasons:
   * The consistency check (below) on the gap.
   * The definition is rebuilt for issue 1 first; the windows are then set and measured on the new table.

   This also changes the reason given above against grouping by station ("each map here stands for five future
   years"). With two-year windows it reads: the model is refit as each survey cycle closes and is tested on the next
   cycle.

   **Consistency check (AI, 2026-11-02):** no gap departs from SPLIT-10, which counts "a planning gap the use case
   has" as a gap. The earlier no-gap exceptions rest on other facts:
   * SPLIT-14's floor: pricing_game_2016_french_fleet, spanish_homeowners_motor_insurance_2010_2014, lending_club,
     alfa_battle_2_0_task_2.
   * A delay shorter than the time column's resolution: ames_housing, perth_house_prices.

   Two-year windows with the gap would still meet SPLIT-14 (eight windows). What sets this case apart?
   * (a) The prediction point is a place in a survey year under that year's temperatures, not a map made at a
     review, so the review's lag is no part of the task. FOSS publishes a season's hauls within months, before the
     next summer survey, so a model refit after each season has every earlier season. This is the
     shorter-than-resolution reason of ames_housing and perth_house_prices (seasons are yearly). As its third case it
     would trigger the amendment proposed in splits.md.
   * (b) Keep the two-year gap.
   * (c) Another reason.

   Recommendation: (a).

   **Andrej (2026-11-02, change):** We need to discuss this, I believe the use case has no planning gap. Unless the
   original paper says so, we should go with no planning gap for this use case.

   **Answer (AI, 2026-11-02):** The paper does not say so. The 2022 review states only which surveys it used
   ("summer bottom trawl surveys 1982–2019", TM-459, p. 3) and names no delay between a survey and its use; the lag
   to 2022 is the review's own timetable, which the two-year windows no longer copy. The data side has no delay at the
   windows' resolution either: FOSS held the hauls of the 2026 summer by 30 October 2026, before the next season. So
   your condition holds, and the definition now has nine two-year windows without a gap.

   **Resolved (2026-11-02, Andrej):** temporal, nine two-year windows (2025-2026 back to 2009-2010), each trained on
   every earlier survey, no gap: an exception to SPLIT-10 (record and splits.md Cases), the fact being that the source
   states no delay and a season is published before the next one. It is the third no-gap case resting on a delay
   shorter than the time column's step (after ames_housing and perth_house_prices), so the amendment proposed in
   splits.md is now due; that call is open for you and Lennart.

3. **Keep RMSE as the metric?** Asked on the review page's metric row. The definition scores RMSE of the rex sole catch
   per km^2 swept, as the 2022 EFH review selects and weights its models (MET-5: the source's metric).

   **Andrej (2026-11-02, discuss):** Why rmse? What would be other options?

   **Answer (AI, 2026-11-02):** RMSE because it is the source's choice: the 2022 review picks and weights its habitat
   models by cross-validated RMSE of predicted against observed abundance (TM-459, pp. 16-21), and MET-4 and MET-5 keep
   a source's deliberate metric. Its cost is measured: the Gulf of Alaska holds 71-93% of the squared error with 23-40%
   of the test hauls, so RMSE mostly scores the Gulf's large catches. The review also reports three other measures, each
   an option: (a) Poisson deviance explained, the fit measure of its count models (the library's
   `mean_poisson_deviance`), which weighs a large catch less and suits the 62% zeros; (b) Spearman's rho, how well the
   predictions order the hauls by catch, close to the Gini of the insurance tables; (c) ROC AUC for presence, which
   scores only the zero-or-not part and drops the catch size. A fourth, our own: RMSE averaged per region, which still
   leaves the Gulf 45-63% of the error and is a metric of our own (TP-6). Recommendation: keep RMSE (the source's
   selection metric); Poisson deviance is the closest alternative, and it can be measured on the three windows before
   you decide. Decision: RMSE, Poisson deviance, or Spearman's rho?

   **Andrej (2026-11-02, as implemented):** Let's do RMSE.

   **Resolved (2026-11-02, Andrej):** RMSE, the source's selection metric (MET-5); record CC of 2026-11-02. The scale
   it is taken on (counts after the inverse, or the log1p target) is open under issue 1, since pooling several
   species brings it up.

4. **Ship a copy of `taxon` as the metric's group, and claim the tow cut for walleye pollock only?**

   * **Problem:**
     - The metric read the feature `taxon` as its group, while the scoring rule as reworded on 2026-11-05 wants every
       column a metric reads, other than the task's own group or time column, to ship as a scoring column, a copy
       where the column is also a feature[^copy], so `dataset check` warned `task_metric_input_is_feature`.
     - The notes said the tow length responds to the catch, measured on walleye pollock and read for every taxon,
       and the exposure study of 2026-11-05 asked whether that holds for the other ten taxa.
   * **Background:** The target is a density, the catch per km^2 swept, into which the source folds the area swept
     (distance fished times net width). The standard tow is 30 minutes in the Bering Sea and 15 minutes in the Gulf
     of Alaska from 1996 and the Aleutians from 1997, so the planned effort reaches the models through the region and
     the date. The realized effort (tow length, distance, net width, area swept) is dropped: a place in a survey year
     has no tow[^use3], and the area swept is the target's denominator[^weight].
   * **Effect on the task:** None on the scores: the copy holds the same values (identical scores on three windows),
     and `taxon` stays a model input. The notes now claim the cut only where the data shows it.
   * **Experiments:** Short tows are those under 0.75 of the median duration of their region and year (1,699 of
     35,561 hauls); each is set against the mean of its stratum and year, on log1p numbers per km^2 (the new decision
     table of the README).
     - Over all hauls, pollock's short tows lie 0.36 above their cells, the other taxa -0.36 to +0.08: a pollock tow
       ends early on a large catch. On the EBS shelf, pollock tows under 0.4 h (831) average 8.33 log1p kg per km^2
       against 7.35 at full length.
     - Where a short tow catches a taxon, its density is higher for 9 of 11 taxa by the plain means and for all 11
       within their cells (pollock 0.55, the others 0.00 to 0.25): a positive count over a smaller area swept is a
       higher density, with no stop on the catch.
     - As free features the effort columns gain 0.0028 of the metric under an L2 fit on log1p (1.9% of untuned
       LightGBM's skill, better in 3 of the 5 windows tested) and nothing under a Poisson fit; an RMSE on counts ranks
       the models as the density RMSE does (Kendall tau 0.80 to 1.00, the same winner in 5 of 5 windows; exposure
       study).
   * **Consistency:** The same copy as liberty_mutual_fire_peril_loss_cost's `var11_weight`, asked in the same review
     comment. The density is scored unweighted, as wadden_sea_sibes_macoma_abundance and
     boreal_postfire_lichen_biomass score theirs[^unweighted]. NOAA's design-based index averages the hauls' CPUE with
     equal weight in each stratum
     ([gapindex](https://afsc-gap-products.github.io/gapindex/articles/background_equations.html)), so it carries the
     same bias of the cut pollock tows.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Copy; cut claimed for pollock (implemented) | `taxon_group` a scoring column, `taxon` a feature; effort dropped; the notes claim the cut for pollock only | the rule's shape; claims what the data shows; scores unchanged | one more column in the frame |
     | B | Read `taxon` directly | no copy; the warning accepted | no change | against the reworded rule |
     | C | Weight the density by the area swept | the area swept a weight scoring column and the training weight | an actuarial convention | the maps are per cell of equal area; ranks models as the density score does |

   * **Recommendation:** A, as the review asked: the copy keeps the scoring columns complete, and the cut is claimed
     where it shows. **Decision:** A, B or C?

   [^copy]: **MET-2** (Must), reworded 2026-11-05 (Lennart): a metric reads the task's own group or time column where it
     is; a feature the metric also needs stays a feature and ships a copy as a scoring column.
   [^use3]: **USE-3** (Must): a value that did not exist at the prediction point is a leak.
   [^weight]: **LEAK-41** (Must): a rate's denominator set or cut after the prediction point is never a model input;
     **LEAK-10** (Must) for the cut itself.
   [^unweighted]: **MET-15** (Must): when the decision is per unit of an equal-area map, the rate is scored unweighted
     and no sample weight is declared.

   **Lennart (2026-11-05, PR #47):** MET-2 as reworded in #44: "A feature the metric also needs stays a feature and
   ships a copy as a scoring column, so the scoring columns are the complete set of a metric's extra data." For this
   dataset: "the same for `taxon` as the group of `mean_group_normalized_rmse` (`taxon_group`, `role="group"`)".

   **Resolved (2026-11-06, Lennart):** A. `_clean` copies `taxon` into `taxon_group`, a scoring column of role `group`
   that `mean_group_normalized_rmse` reads; `taxon` stays a feature, and a random prediction scores the same through
   the copy as through `taxon` on three windows. The tow's effort stays out (USE-3; the area swept is the target's
   denominator, LEAK-41), the cut is claimed for walleye pollock only (LEAK-10: +0.36 over all hauls, the other taxa
   -0.36 to +0.08; the densities of short tows that catch a taxon are higher for every taxon, which the smaller area
   swept explains), and the score stays unweighted on the density (MET-15), carrying the bias of the cut pollock tows
   as NOAA's index does. Supersedes the metric's reading of the feature (Andrej, 2026-11-02, under MET-2 as amended
   then) and the note that read the pollock measurement for every taxon. `dataset check`: 0 errors, 0 warnings.

**Review panel:** ship after changes (mediator). Claim audit: 34 claims, 27 hold, 3 refuted and 2 refuted in part
(four fixed in the definition; the record's lines are corrected at hand-over), 1 concern (the Gulf of Alaska share of
the metric, now a note), 1 untested (the regime, issue 2). Blind review: would include with changes; its main concerns
were the `stratum` break in the newest window (repaired) and the undocumented species (the blind reviewer saw no task
summary, which names the species). Debate: agreed on the stratum repair, the temporal split, the metric and the
wording fixes; disputed the wording of the prediction point (settled for the critic: a place in a survey year) and a
region-averaged RMSE as an option for the curator (settled: a note only).

<details><summary>Mediator</summary>

**Mediator (2026-11-01): noaa_afsc_bottom_trawl_survey_cpue**

**Recommendation**

```text
Verdict: ship after changes (one column repaired from the origin, the rest text in dataset.py and the record; rows,
  target, split and metric unchanged).
Validity: SEL-2 holds (CC `Yes`, priority 5; species-abundance mapping judged per dataset, Andrej 2026-10-30).
  USE-1 holds (the EFH review, 50 CFR 600.815(a)(10)). USE-3 broken in the text (a review forecasting later hauls,
  fed each haul's own temperatures), fixed by naming one prediction point: a place in a survey year under that year's
  conditions. The temperatures stay (mean R^2 0.652 with, 0.651 without); the vessel and the hour stay out under
  USE-3, so USE-6 holds without an exception. USE-5 holds; the species is a weighing call (issue 1). USE-8
  approximate, fit_reason's split claim corrected. LEAK-10 holds for all 8 features (gear, effort, end position and
  performance code are LEAK-10 drops). SPLIT-1 / SPLIT-3: temporal, not yet the curator's pick (issue 2); SPLIT-10,
  SPLIT-12, SPLIT-14 hold; SPLIT-15 departed, forced by SPLIT-12 and SPLIT-14. SPLIT-20: the 2025 GOA
  restratification breaks `stratum` in the newest window, repaired (CLEAN-21). PROV holds (35,549 targets rebuilt
  exactly; haul counts match TM-459 p. 6). EV-7: the 2026 catches are not yet rated; reworded, second download
  compared at build.
Value: MET-5 holds (TM-459 p. 21 selects and weights models by RMSE); MET-11 `source` holds (RMSE on density and on
  counts rank seven models alike, tau 1.0); MET-2 met with a note (GOA holds 71-92% of the squared error; the source
  pools shelf, slope and NBS itself; a region-averaged RMSE ranks the models as the pooled one does). TP probes: no
  flag (RF skill +0.694).
Quality: CLEAN-21 `stratum` of the 2025 GOA hauls put on the pre-2025 design with GAP's published polygons (newest
  window R^2 0.607 to 0.726); CLEAN-22 drop reasons reworded; CLEAN-8 species note; CLEAN-21 depth 1993-95 note.
Weighed: source + (NOAA tables and memos, rebuilt exactly); use case + (EFH set by law, models picked by RMSE);
  fit - (no habitat rasters; regions and life stages pooled); strong spatial baseline - (k-NN on position close to
  LightGBM, far above the stratum mean).
For the curator: issue 1 (rex sole as the species, a weighing call); issue 2 (confirm temporal, SPLIT-1).
```

The advocate and the critic reach the same verdict and agree on every change except two wordings, settled below.
Neither asks for exclusion, and no Must is left unmet once the changes are made.

Two decisive checks were run (scripts and outputs in the run folder). First, a region-averaged RMSE on seven untuned
models over the shipped windows. Second, a point-in-polygon join of the 2025 GOA hauls onto GAP's pre-2025 strata,
with LightGBM over 3 seeds.

**Agreed facts**

* 35,561 standard hauls 1982-2026 (no 2020) and 13,557 rex sole catches. The 12 catches weighed but not counted leave,
  so 35,549 rows ship, 61.9% of them zero. CATCH has no zero-weight row, and the zero fill is GAP's own recipe
  (gap_products sec. 10.2). The blind reviewer rebuilt every target from the API (maximum difference 0.0). Haul
  counts match TM-459: 14,517 against 14,514 on the shelf and NBS, 1,136 against 1,136 on the slope.
* Rex sole presence: EBS 19.5%, slope 49.1%, GOA 66.8%, AI 38.7%, NBS 0% (969 hauls). EBS presence is steady by
  period (19.7 / 17.0 / 20.3 / 20.6%). All 13,331 catches of 1982-2025 are rated high confidence; the 226 catches of
  2026 carry no rating yet. The 722 hauls of 2026 are 17% of the newest window, and their counts match a full season
  (EBS 350 of 350).
* No leak among the 8 features: exact copies across the split 0%, and missing temperatures do not track the catch.
  Effort, gear, end position and performance code were rightly dropped (LEAK-10): EBS pollock tows under 0.4 h
  average 8.33 against 7.35 log1p kg/km^2.
* The review trains on haul temperatures and maps from "Rasterized 38-year averages" (TM-459 pp. 8-9). The
  temperatures give no gain: mean R^2 on log1p is 0.652 with them and 0.651 without, and a training-years climatology
  in their place moves each window by -0.004 to +0.012. Barnes et al. 2022 (same team) forecast later years with
  year-specific bottom temperature kriged onto the tow locations and onto a 1-km grid.
* Windows 2022-26 / 2017-21 / 2012-16, trained to 2019 / 2014 / 2009, on 85.2 / 71.0 / 57.3% of the hauls. A fourth
  window would train on 43.6%. The two-year gap is the source's lag from the last survey used to the review.
  84.7-85.3% of the test hauls sit at a station seen in training. Mean R^2: temporal 0.652, grouped by station
  0.687, IID 0.732. The source skill-tests by random 10-fold CV (TM-459 pp. 20-21) and checked the 2017 models
  forward (p. 3).
* GOA was restratified for 2025: 23 new stratum numbers, none shared with the 59 of 1990-2023. They cover 431 hauls,
  10.2% of the newest window. The source's models have no stratum covariate (TM-459 Table 3).
* TM-459 picks and weights models by RMSE (p. 21). RMSE on density and on counts rank seven models at tau 1.000 in
  every window. GOA is 23-40% of the test hauls but holds 71-92% of the squared error.
* Rex sole is modelled in TM-357 (hurdle GAM, pp. 48-49), TM-459 (pp. 150-152) and TM-458 (pp. 131-132). FOSS has no
  length table (404), so the target counts all sizes.

**Changes to make now (no decision needed)**

1. `stratum` (CLEAN-21 Should, SPLIT-20; remedy ladder, repair from the origin). Put every GOA haul of the 2025
   design (GOA from 2025 on) into the pre-2025 strata by its start position. Use GAP's own polygons: akgfmaps
   `inst/extdata/afsc_bts_strata.gpkg`, layer `survey_strata`, `SURVEY_DEFINITION_ID` 47, `DESIGN_YEAR` 1984
   (EPSG:3338). It holds 59 strata with exactly the IDs of the 59 FOSS GOA strata of 1990-2023. Pin commit
   1fcc7fa598e66a13cdca95be407e1f93c11f50d3 (sha256 1319eb3485c9ee75be96dcbfa5cba44c9d43374d1a8e6a74b7dadfdd62e6fb27;
   package licence GPL (>= 2); only the derived codes ship). Add the file to `download_description` and
   `source_links`.
   * Checked: every one of the 431 hauls falls inside a 1984 polygon. On the 10,868 earlier GOA hauls the join
     returns FOSS's stratum for 95.5% (the start position lies near a boundary for the rest). The nearest pre-2025
     haul gives the same stratum for 92.1% of the 2025 hauls.
   * Effect (LightGBM, 3 seeds): newest window R^2 on log1p 0.607 to 0.726; on the 2025 GOA hauls -0.57 to 0.52;
     older windows unchanged. Dropping the column instead gives 0.715 / 0.711 / 0.628, against 0.726 / 0.723 / 0.634.
   * Implementation: no geometry library is installed; `matplotlib.path` (build extras) plus the Alaska Albers
     formulas do it.
   * Do not map the old hauls onto the 2025 design, which was built on survey densities that overlap the test
     windows.
   * Rewrite the anomaly bullet. Its reason "a model fit at a review meets the redesign too" goes, because the source
     uses no stratum.
2. Prediction point (USE-3, USE-6, Must). `known`, `split` and the first note name one point: a place in a given
   survey year under that year's conditions. Known: the region and design stratum, the position, the date, the
   depth, and that year's bottom and surface temperatures at the place, given by the readings taken during the haul.
   * Say that the readings stand in for the year's temperature field (Barnes et al. 2022) and that the review's
     maps use long-term means (TM-459 p. 8). Give the no-gain numbers above.
   * `split`: "as the next review checks the model of the previous one against the surveys that followed it"
     (TM-459 p. 3; Barnes et al. 2022).
3. Drop reasons (CLEAN-22 Must; LEAK-10; USE-3). In `changes` and the two "Dropped" bullets, replace "which the
   habitat models do not use" with what each column is:
   * effort and gear: the label's denominator, and a tow length that responds to the catch;
   * vessel and hour: a place in a survey year has neither.
   * Remove the R^2 numbers given as reasons. Surface temperature stays.
   * Replace "the covariates the source trains on" with: "position, depth and bottom temperature are the source's
     trawl-model covariates (TM-459 Table 3); region, stratum, date and surface temperature are ours".
4. `fit_reason` (USE-8). "The rows and target follow the review's models; the split follows the review cycle and the
   next review's forecast check, not the review's random cross-validation." Add the gap that the temperatures are
   the haul's readings where a map uses long-term means.
5. `splits_comment` (SPLIT-13, SPLIT-14). Add: 85% of test hauls at a station seen in training (EBS 100%, GOA
   40-65%); a fourth window would train on 43.6%. Cite Barnes, Essington, Pirtle et al. 2022 (Ecography e06189)
   beside the unread Pirtle et al. 2020. Say the 2023 GOA memo was not read.
6. Species bullet (CLEAN-8 Must; EV-2).
   * The species was screened on the whole table, test windows included: a pipeline choice that approximates the
     task.
   * "Its zeros are not one region's" becomes: zeros fall inside four of the five regions; NBS has no catch.
   * "Since 1982" becomes "1982-2025; the 226 catches of 2026 are not yet rated".
   * The comparison with cod and pollock does not rest on zero inflation (Andrej, 2026-10-30, policy 2).
7. 2026 season (EV-7; LEAK-24's two-download check by analogy). Add a note that the newest season is provisional. At
   build, compare with a fresh download. If the 2026 rows change, build from the newer download or end the newest
   window at 2025. A presence of 0.169 alone is no reason to cut (SPLIT-21).
8. Metric (MET-2, MET-11). In `definition` and the metric note:
   * RMSE on counts (density x area swept) ranks the probe models as RMSE on density does (tau 1.0);
   * GOA holds 71-92% of the squared error;
   * TM-459 itself pools shelf, NBS and slope (two gears) under one RMSE (p. 6);
   * the tau of raw against log1p RMSE is 0.14-0.33 over reruns.
9. `depth_m` note (CLEAN-21). The 1993-95 depths are headrope depths (TM-459 p. 8), a median 1.25 m shallower at the
   EBS stations. They are training rows in every window and are kept.
10. Optional:
    * the oracle bound of the zero-inflated pattern next to the hurdle numbers (every same-run sibling gives it);
    * half a sentence on the performance code (within strata, 45.9% presence with code 0 against 40.8%);
    * cite GAP's column metadata (AKDT) for the local times instead of inferring them.
11. Record (PROV-12 Must; PROV-9). Add an `Assessment (AI, 2026-11-01)` line that records: rex sole and its reasons;
    `source` rmse from TM-459, which supersedes the screening's fallback; the temporal windows; year 2026, which
    supersedes "stays empty"; AI stations repeat a median 7 times, not "once or twice".
    * Move the Laman 2017 DOI from `source_links` to the comments: related work is not a source.
    * Cite TM-459, TM-458 and Barnes et al. 2022 in the comments too. The builder's item 5, adding TM-459 to
      `source_links`, would break PROV-12.
    * Add the akgfmaps file to `source_links`: it is a data source of the definition.

**Changes that need the curator**

1. **Rex sole as the species** (P3, USE-5 Must holds; which species to ship is a weighing call).
   * Problem: the EFH memos model 31-36 species with no primary one, so the choice is ours.
   * Effect: the species sets what the zeros mean. Rex sole's zeros fall inside regions. Cod has 4% zeros on the EBS
     shelf, and most of its presence signal is the region. Pollock's zeros are mostly whole regions.
   * For rex sole (both sides):
     * modelled in both reviews;
     * high-confidence identification 1982-2025, with steady presence;
     * both parts learnable (AUC 0.94-0.96, R^2 0.30-0.38 among catches).
   * Against: cod and pollock are the larger fisheries, each with its own EFH maps. Andrej's policy 2 removes zero
     inflation as a reason.
   * Decision: rex sole, another species, or a second species as a sibling. Recommendation: rex sole.
2. **Temporal over grouped by station** (P4, SPLIT-1 and SPLIT-3, Must: the curator picks the regime).
   * Problem: the only CC line is `Yes`, priority 5, and the screening left grouped by station as the alternative.
   * Effect: the windows test later years at mostly sampled places (85% of test hauls at seen stations). Mean R^2
     0.652 temporal, 0.687 grouped, 0.732 IID.
   * For temporal: the five-year review cycle; the 2022 forecast check of the 2017 models (TM-459 p. 3); Barnes et
     al. 2022.
   * For grouped: the source's CV is "a test of prediction skill at unsampled locations" (TM-459 p. 21);
     wadden_sea_sibes (same run) is grouped.
   * Every panel member who addressed it prefers temporal.
   * Decision: temporal or grouped. Recommendation: temporal.

**Disputed points**

| Point | Advocate | Critic | Rule and rank | Settled |
|---|---|---|---|---|
| Which prediction point to name | "abundance at a haul, given the habitat measured there" (the skill test); vessel and hour out per 2_month_survival_rate_prediction, else restored | "a place in a survey year under that year's conditions"; the haul's readings stand in for the year's field | USE-3 and USE-6, both Must, P3; not a conflict, both must hold | Critic. At a haul the vessel and the hour are known, so USE-6 would make them inputs. 2_month_survival's fact (a physician's estimate set beside the model as its comparator) is not this one. Under the place-year point, both rules hold with the current columns, by a wording fix (mildest remedy). The advocate is right that the scored unit is the haul, the source's model-selection step; `fit_reason` names it as a gap (USE-8) |
| Region-averaged RMSE as a curator option | no: MET-5 holds, TP-6, uneven region mix per window | yes: a MET-1 weighing call; MET-13 does not bar it | MET-5 Should, MET-2 Must (P6); EV-1 | Advocate on the outcome, critic on MET-13. Measured: the region-averaged RMSE ranks seven models at tau 0.81 / 0.81 / 0.90 with the pooled one (1.00 / 1.00 / 0.90 without NBS), and GOA still holds 45-63% of it, because RMSE keeps each region's scale (GOA 2,100-2,900 per km^2, EBS 120-880). It does not make each region count once. A scale-free per-region score would be a metric of our own invention (TP-6). TM-459 already pools shelf, NBS and slope. Note only (change 8) |
| Surface temperature | keep (CLEAN-22) | keep | CLEAN-22 Must; claim auditor wanted it dropped (no source model uses it) | Keep: "not used by the source" is no CLEAN-22 reason; under the place-year point it is that year's condition |
| `stratum` remedy | map the 2025 hauls (polygons, else nearest haul) | same; drop fallback withdrawn | CLEAN-21 Should; remedy ladder | Repair from the origin: GAP's 1984-design polygons exist and match FOSS's IDs (change 1). The split auditor's and blind reviewer's drop is the next rung and scores lower |
| When to cut 2026 | only if a later download changes the counts | compare before build | EV-7, LEAK-24 by analogy; SPLIT-21 | Both: reword now, compare at build, cut only if the rows change |

**Consistency with precedent**

* `stratum`: follows college_scorecard (CLEAN-21: the measuring body's conversion; Lennart 2026-10-16). Because GAP
  publishes the boundaries, no exception is needed, unlike zillow_prize's map from the data. This answers the
  precedent checker's consistency check with its option (b).
* Vessel and hour: a USE-3 drop under the place-year point, as in wadden_sea_sibes (same run, unreviewed). This does
  not depart from brazilian_ecommerce: its inputs were known at the prediction point, while these are not attributes
  of the predicted place-year. The precedent checker's check closes with its option (a), and no exception to USE-6 is
  recorded.
* Temperatures at their measured values: wadden_sea keeps station-measured sediment on the same reading (same run).
* Temporal where wadden_sea is grouped: the distinguishing fact is written (a map stands for five future years and
  is checked against them). Issue 2.
* Effort and gear dropped, against fremtpl2's exposure kept (Andrej 2026-10-20): set apart by written facts (area
  swept is the label's denominator; tow length responds to the catch).
* Metric: follows forest_fires (MET-5), zillow_prize (concentration is no ground to overrule), porto_seguro (MET-11
  identity) and TP-6 as amended.
* Windows: the house family (SPLIT-12) and rain_in_australia (Lennart 2026-10-26); no exception.
* Year 2026: rain_in_australia (PROV-9). The 12 uncounted catches: qsar_tid_11 (CLEAN-15).
* Species: departs from the same-run siblings, which take their source's species. Here the source has none. Issue 1.
* No new exception, no third exception of one reason, no drift in Andrej's calls.

</details>

<details><summary>Claim audit</summary>

**Claim auditor: noaa_afsc_bottom_trawl_survey_cpue (2026-11-01)**

Verdict: ship after changes (small ones).
Validity: USE-3 / LEAK-10 refuted as written for the two measured temperatures: a review cannot know them for later hauls, but they add nothing measurable (drop them, or rewrite the prediction point). SPLIT-3 is open: no CC line names the regime, and the windows test later years at places already sampled. PROV holds: our hauls match the review's counts.
Value: MET-5 holds (RMSE is the review's one selection and weighting criterion). MET-11: density stands in for the source's count and ranks the probe models the same (tau 1.0). MET-2: the pooled score is mostly a Gulf of Alaska score (needs a note).
Quality: wording fixes (which covariates are the source's, taxon confidence in 2026, fit_reason).

Every number below was recomputed from the raw FOSS JSON pages or from the definition's frame and splits (`workbench` + `make_splits`), with untuned models (LightGBM 400 trees, random forest 200 trees) on the three shipped windows. The scripts and outputs are in the run folder (not committed). The papers are the memo texts in the run folder. Pages are the printed ones.

**Claims table**

| # | Claim | Source | Test | Result | Evidence | Rule |
|---|---|---|---|---|---|---|
| 1 | 35,561 standard hauls 1982-2026; 13,557 rex sole catches; 12 weighed but not counted leave; 35,549 rows; 62% zero | notes intro, Target bullet, `row`, builder claims | raw recount | holds | 35,561 unique `hauljoin`, 1982-2026, no 2020; 13,557 catches, 12 with `cpue_nokm2` and `count` missing; zero share 0.619 | CLEAN-15 |
| 2 | CATCH holds positive catches only, so a missing row is a zero; this is the source's own zero fill (gap_products sec. 10.2) | Zeros bullet; the warning proposed for acceptance | rows with weight <= 0; the gap_products page | holds | 0 rows with `cpue_kgkm2` <= 0; sec. 10.2 is titled "Create zero-filled data" and its code sets missing CPUE to 0 | EV-2 |
| 3 | `task_target_value_dominant`: the zeros are observed absences (zero-inflated), not placeholders | builder, warning | EBS presence by period: an early stretch of non-identification would show as a dip | holds | EBS presence 19.7% / 17.0% / 20.3% / 20.6% (1982-92 / 93-02 / 03-12 / 13-26) | TP, CLEAN |
| 4 | "identified with high confidence in every catch since 1982" | Species bullet | `taxon_confidence` in CATCH | refuted (minor) | 13,331 High; 226 have none, all from 2026 (AI 167, EBS 59). The 2026 season is not yet rated: 722 hauls, 17.1% of the newest test window | EV-7, PROV-9 |
| 5 | Presence 38.1% overall; EBS 19.5%, slope 49.1%, GOA 66.8%, AI 38.7%, NBS 0% | Species bullet; Decision 1 | recount | holds | identical. Rex sole is absent from a whole region too (NBS, 969 hauls), which the notes hold against sablefish and the others | EV-2 |
| 6 | The 2017 memo uses its hurdle GAM, kept for species in 10-30% of hauls, on rex sole (pp. 15, 48-49); the 2022 Bering Sea and AI memos model it again | Species bullet | read TM-357, TM-459, TM-458 | holds | TM-357 p. 15 "between 10% and 30%, a hurdle model (hGAM)"; pp. 48-49 hGAM for juvenile and adult rex sole; TM-459 pp. 150-152 three life stages; TM-458 pp. 131-132 subadult and adult | EV-2 |
| 7 | Hurdle probe numbers (AUC 0.94-0.96, 0.86-0.91 from survey and depth; R^2 0.30-0.38 among catches); the other species' shares and identification history | Species bullet | the builder's hurdle probe and species screen tables | holds | 10200 rows: AUC 0.947/0.962/0.941, 0.872/0.913/0.861; R^2 0.337/0.305/0.382; cod 22.2% zeros (EBS 4.0%), pollock 17.6% | EV-8 |
| 8 | Every haul is satisfactory (codes 0 or positive); the 2,659 with a positive code stay; presence differs by code; the code is dropped | Hauls bullet; Decision 2 | recount; presence within strata | holds, with a nuance | minimum code 0, 2,659 positive; within strata, presence is 45.9% with code 0 and 40.8% with a positive code, so part of the gap is the tow, not the place; adding the code gives R^2 0.6505 against 0.6516 | LEAK-10 |
| 9 | Effort and gear dropped: pollock tows under 0.4 h on the EBS shelf, 831 of them, 8.33 against 7.35; rex sole R^2 0.636 with them, 0.652 without | Dropped bullet | recomputed from CATCH 21740; probe file | holds | 831, 8.33, 7.35 reproduced; the builder's probe file: 0.6355 / 0.6516 | LEAK-10, USE-6 |
| 10 | Vessel and hour dropped: R^2 0.643 and 0.646 against 0.652 | Dropped bullet | probe file | holds | 0.6434 / 0.6462 / 0.6516 | USE-6 |
| 11 | `survey`, `survey_name` and `survey_definition_id` are copies of `srvy` | Dropped bullet | values per `srvy` | holds | 1 value each per `srvy` | CLEAN |
| 12 | 26 of the 141 stratum numbers are used by two surveys | stratum bullet | recount | holds | 26 of 141 | CLEAN |
| 13 | GOA restratified for 2025: 23 new strata, 431 hauls, 10.2% of the newest window; R^2 0.598 with stratum and 0.719 without (0.722/0.720, 0.635/0.623) | Anomaly bullet | recount; LightGBM rerun | holds | 23 of 23 strata in 2025 unseen, 431 hauls (10.19%); rerun 0.598/0.719, 0.722/0.720, 0.635/0.623 exactly | CLEAN-22 |
| 14 | The AI survey crosses 180 degrees (2,567 hauls west of it); R^2 0.598 against 0.562 with the signed longitude | longitude bullet | recount; probe file | holds | 2,567, all AI; 0.5976 / 0.5623 | CLEAN |
| 15 | Bottom temperature missing for 4.5% of hauls, surface for 2.4% | Missing bullet | recount | holds | 4.50% / 2.42% | CLEAN |
| 16 | The "Z" timestamps are local times (hauls from 05:00 to 23:00) | Anomaly bullet | hour distribution | holds (inference) | hours 5 to 23, median 12; read as UTC they would put the tows at 21:00-15:00 Alaska time | EV-2 (rank 5) |
| 17 | The EBS shelf survey has 350 stations from 2024 (376 before) | Anomaly bullet | stations per year | holds | 376 through 2023, 350 in 2024-2026 | EV-2 |
| 18 | "Known for a haul: the region and stratum, the position, the date, and the depth and temperatures ..., the covariates the source trains on" | Prediction point bullet | TM-459 Table 3; TM-357 Fig. 4 | partly refuted | The trawl models use bottom temperature, depth and position plus rasters. Surface temperature appears only in the 2017 ichthyoplankton models (TM-357 Fig. 3). Neither memo uses stratum or date as a covariate | USE-6, EV-2 |
| 19 | `known`: the bottom and surface temperature measured during the haul are known at the prediction point, where "a model fit at a review predicts the surveys of the years it is used" | `task_summary.known` and `split` | TM-459 pp. 8-9; the shipped features against no temperatures and against a training-side climatology (30-NN mean of training hauls) | refuted as written; no measured gain | TM-459 p. 8: "Rasterized 38-year averages of habitat covariates ... were input into the best-fitting SDMs when predicting"; p. 9: trained on haul temperatures, predicted from a raster. LightGBM R^2 0.598/0.722/0.635 shipped, 0.572/0.723/0.659 without; declared RMSE 1,472/1,652/1,315 against 1,461/1,642/1,286. Random forest RMSE 1,420/1,599/1,302 against 1,403/1,565/1,266 without. The source's procedure (train on measured, test on climatology): R^2 0.595/0.721/0.647 | USE-3, LEAK-10 (Must) |
| 20 | 2017 review used 1982-2014 (Laman 2017 p. 5); 2022 used 1982-2019 (TM-459 p. 3); review "at least every 5 years" (50 CFR 600.815(a)(10), TM-459 p. 2) | Prediction point bullet; splits_comment | read | holds | TM-357 p. 5 "from 1982 through 2014"; TM-459 p. 3 "1982-2019"; p. 2 "at least every 5 years (50 CFR 600.815(a)(10))" | SPLIT-12 |
| 21 | `fit_reason`: "The rows, target and split follow the review's models" | `task_summary.fit_reason` | TM-459 pp. 20-21; distance from each test haul to the nearest training haul | refuted (the split part) | The review skill-tested its models by random 10-fold CV, "a test of prediction skill at unsampled locations" (p. 21). In our windows, 1.8% / 4.6% / 4.2% of test hauls lie more than 5 km from any training haul (median 0.38 / 0.55 / 0.48 km), so the windows ask about later years at sampled places | SPLIT-3, USE-8 |
| 22 | splits_comment: windows 2022-26 / 2017-21 / 2012-16, trained to 2019 / 2014 / 2009, no survey in 2020, oldest train side 57% | splits_comment | recount | holds | 30,273/4,230; 25,253/3,953; 20,384/4,806; train ends 2019-08-20, 2014-08-08, 2009-07-29; 20,384/35,549 = 57.3% | SPLIT-14 |
| 23 | "the 2022 review assessed the forecasting accuracy of the 2017 SDM approach (TM-459, p. 3; Pirtle et al. 2020, not read), the question these windows ask" | splits_comment | TM-459 p. 3; web search | holds as a quote; Pirtle 2020 untested | Not found. Barnes, Essington, Pirtle, Rooper, Laman et al. 2022 (Ecography, doi:10.1111/ecog.06189; abstract only, unverified) ran retrospective forecast skill tests on Bering Sea groundfish SDMs: time-varying covariates "did not improve or decreased forecast skill". This supports the temporal question and agrees with row 19 | SPLIT-12, EV-2 |
| 24 | Metric `source` `rmse`, original: cross-validated RMSE on numerical abundance by which the 2022 review "selects and weights" its models; also reported rho, AUC, PDE | `metric` | TM-459 pp. 16-24 | holds | p. 21 "the model with the lowest RMSE was considered to be the best performer"; weights RMSE^-2 (p. 21); p. 24 calls rho, AUC and PDE three reported "fit metrics". One deliberate criterion | MET-1, MET-5 |
| 25 | `definition`: RMSE on numbers per km^2, where the source scores the count per station | `metric.definition` | RMSE on counts (density x `area_swept_km2`) against RMSE on density for seven probe models | holds: same ranking | Kendall tau 1.000 in all three windows; `count / area_swept_km2` equals `cpue_nokm2` (ratio 1.000 at p1 and p99) | MET-3, MET-11 |
| 26 | The metric can be computed on every fold | implied (MET-2) | `data_foundry.v2.metrics.score` with the declared spec on dummies; units per window | holds | 4,230 / 3,953 / 4,806 test hauls, 1,537 / 1,737 / 1,863 catches; the raw-mean dummy scores 1,580.1 / 1,804.2 / 1,461.2 (as the builder found); the spec inverts log1p | MET-2 |
| 27 | The metric means on our task what it meant on the source's | implied (MET-2) | share of the squared error by region; rank agreement of pooled and Bering-only RMSE | concern, not in the notes | GOA is 23% / 40% / 27% of the test hauls but holds 76% / 91% / 71% of LightGBM's squared error (mean predictor 71% / 89% / 71%). GOA mean density is 1,060 per km^2 against 85 on the EBS shelf. The reference memo scores Bering Sea models, per life stage. Kendall tau between pooled and Bering-only RMSE: 0.81 / 0.81 / 0.62 | MET-2 |
| 28 | 10-31 test hauls hold half the squared error; every model beats the training mean; ranking against RMSE on log1p, Kendall tau 0.14-0.24 | Note bullet | rerun of the seven models | holds; tau fragile | 10-31 and every model beating the mean reproduced; my rerun gives tau 0.14 / 0.14 / 0.33 (with 21 pairs, one swap moves tau by 0.095) | EV-8 |
| 29 | Implied: no row is a copy across the split | implied | leak probe 5 | holds | 0.0%, also with the date | LEAK-16 |
| 30 | Implied: these are the review's hauls | implied | TM-459 p. 6 counts against ours | holds (strong) | EBS shelf + NBS 1982-2019: 14,517 here against 14,514 in TM-459; slope 1,136 against 1,136 | PROV |
| 31 | "FOSS's CATCH has no lengths", so all sizes are counted | Note bullet | CATCH columns; FOSS endpoints | holds | CATCH has no length column; `/afsc_groundfish_survey_length/` and `/afsc_groundfish_survey_specimen/` return 404 | USE-5 |
| 32 | Record: "GOA and AI stations are mostly sampled once or twice" | record, paragraph under the CC line | hauls per station id; distance | partly refuted | median hauls per station id: GOA 1, AI 7, EBS 44; 94.7% of GOA hauls in the newest window lie within 5 km of a training haul | EV-2 |
| 33 | Record Assessment: the curator settled the species-abundance question without a new rule (SEL-2) | record | grep | holds | the same quote dated 2026-10-30 is in five sibling records | SEL-2 |
| 34 | Record screening: temporal regime, "grouped by station the alternative (SPLIT-3: one, the curator's pick)" | record | the CC lines | untested | the only CC line is "`Yes`, priority 5"; `required_split: Temporal` comes from the AI draft of 2026-10-20 | SPLIT-3 |

**Refuted and untested claims, ranked (validity first, Must first)**

1. **Measured temperatures known at the review (row 19; P4, USE-3 / LEAK-10, Must).** `known` and `split` place the prediction point at a review that predicts later surveys. A review two or more years ahead cannot know a future haul's own bottom and surface temperature: the source predicts from a 38-year climatology raster (TM-459 pp. 8-9). Measured effect: none. Without both temperatures, both model families score better in all three windows (LightGBM RMSE -11 / -10 / -29, random forest -17 / -34 / -36). With the source's own procedure (train on measured, test on climatology) R^2 is within 0.012 of the shipped one. What it changes: the definition's prediction point, not the scores. Mildest remedy, the curator's call between two options. (a) Drop `bottom_temperature_c` and `surface_temperature_c`: no measured cost, and the task becomes "abundance from place, depth and date", which is what a review knows. (b) Keep `bottom_temperature_c` and rewrite the prediction point as the source's skill test: abundance at a haul given the habitat measured there (TM-459 p. 9: trained and skill-tested on haul temperatures). Say so in `known`, `split` and the notes, and drop `surface_temperature_c` either way, since no source model uses it (row 18). Under (b) the value is known at the stated point, so no exception to a Must is needed.
2. **The split "follows the review's models", and the regime is "the curator's pick" (rows 21 and 34; P4, SPLIT-3, Must).** The review validated by random station CV, a test at unsampled locations. Our windows test later years at places already sampled: 95-98% of test hauls lie within 5 km of a training haul. The temporal question has support (TM-459 p. 3; Barnes et al. 2022), but no CC line records the regime choice that SPLIT-3 leaves to the use case. What it changes: the `fit_reason` wording, and the curator confirms the regime. Mildest remedy: reword `fit_reason` to "the rows and target follow the review's models; the split follows the review cycle and the 2022 forecast check, not the review's random cross-validation". Add the 5 km share to splits_comment, and ask the curator for a CC line on temporal against grouped by place. (This overlaps the split auditor's brief.)
3. **The metric means what it meant (row 27; P6, MET-2).** RMSE pooled over five regions is mostly a GOA score: GOA hauls are 23-40% of the test hauls and carry 71-91% of the squared error. The source scores each region's models apart, per life stage, and the cited memo covers the Bering Sea only. Pooled and Bering-only RMSE rank the probe models at tau 0.62-0.81. What it changes: what a reader takes the score to mean; the metric stays. Mildest remedy: a Note bullet with these shares (also that the GOA memo of the 2023 review was not read).
4. **Density for count (row 25; P6, MET-11).** This holds, and it settles the builder's draft issue 2 ("source or stand-in?") in favour of `source`. Mildest remedy: add the measured closeness to `metric.definition`: "RMSE on counts (density x area swept) ranks the seven probe models the same in all three windows (Kendall tau 1.0)".
5. **"The covariates the source trains on" (row 18; P3 / P7 wording).** Surface temperature, stratum and date are not covariates of the source's trawl models. Mildest remedy: reword the prediction-point bullet ("position, depth and bottom temperature are the source's covariates; region, stratum, date and surface temperature are ours"). This also backs dropping surface temperature (item 1).
6. **Taxon confidence and the 2026 season (row 4; P5, PROV-9).** The 2026 catches carry no confidence rating yet, so the 2026 rows (17.1% of the newest window) come from a season FOSS has not finished checking. What it changes: wording, and a stability caveat for the newest window. Mildest remedy: "rated high confidence in every catch 1982-2025; the 2026 catches are not yet rated", plus a note that the snapshot's newest season is provisional.
7. **Kendall tau 0.14-0.24 (row 28; EV-8).** The value moves by 0.1 per swap among seven models; a rerun gives 0.14-0.33. Mildest remedy: write "agrees weakly (Kendall tau 0.14-0.33 over reruns)", or drop the range.
8. **Record line on station repeats (row 32).** AI station ids repeat about 7 times, and GOA places recur within 5 km even though the ids do not. Mildest remedy: correct the record paragraph.
9. **Performance code (row 8, nuance).** Within strata, positive-code hauls catch rex sole less often (40.8% against 45.9%), so part of the gap is the tow's catch efficiency. Keeping the hauls follows TM-459 p. 6 ("satisfactory trawl performance"). Mildest remedy: optional, half a sentence in the Hauls bullet.

Untested: Pirtle et al. 2020, the 2022 forecast check (not found; Barnes et al. 2022 read from its abstract only); the 2023 GOA EFH memo (whether its RMSE matches the Bering Sea and AI memos'; TM-458 matches TM-459); what the positive performance codes mean (gap_products not reopened); whether a later FOSS download changes the 2026 rows.

</details>

<details><summary>Column audit</summary>

**Column audit (column-auditor, 2026-11-01): noaa_afsc_bottom_trawl_survey_cpue**

**Verdict: ship after one change.** I found no leak. All 8 features existed before the catch was counted, none is the
outcome in another form, and the missing temperatures do not track the catch. The gear, effort and performance columns
were rightly dropped under LEAK-10. One cleaning problem has a large effect: the Gulf of Alaska was restratified in 2025,
so all 431 GOA hauls of 2025 carry stratum codes no training row has. On those hauls untuned LightGBM scores R^2 -0.82
on log1p. If each one is given the pre-2025 stratum of its nearest earlier haul, it scores +0.51, and the newest window
goes from 0.577 to 0.726 (CLEAN-21). Three smaller items need a note or a question: the test hauls' temperatures (gain
measured: none), the unfinished 2026 season, and the stated reason for dropping the vessel and the hour.

Prediction point (first `curation_comments` bullet): at an EFH review, which fits on surveys up to two years earlier
and whose maps stand for five years. Known for a haul: the region, stratum, position, date, depth and the temperatures
measured during the tow. Codebook: GAP's "Universal Column Metadata" (gap_products docs) and the methods of the EFH
memos (TM-357, TM-458, TM-459). Frame: `dataset_io.from_definition` (no build record), 35,549 x 9, sorted
by `date` (checked monotonic), with the three shipped windows. My numbers come from untuned LightGBM (400 trees, learning
rate 0.05, 3 seeds, `date` as year plus day of year) on those windows, listed as 2012-16 / 2017-21 / 2022-26, unless
cited as the builder's. Scripts and CSVs: in the run folder (not committed).

**Column table: the shipped frame**

| column | meaning (codebook) | known at prediction? | dtype and cleaning | verdict | rule |
|---|---|---|---|---|---|
| `log1p_cpue_no_km2` (target) | log1p of `cpue_nokm2`, "numerical catch per unit effort (area swept by the net...)"; equals `count / area_swept_km2` to within 4e-5 for all 13,545 counted catches | outcome | float, 0-10.98; 61.9% zeros from the source's zero fill (CATCH has no row with count 0 or weight 0). The 12 catches weighed but never counted (count null; 10 GOA 1990-2013, 1 EBS 1992, 1 AI 1991) leave. Named after the transform | fine; one question on 2026 (problem 2) | CLEAN-15, CLEAN-16 |
| `srvy` | survey region (EBS, NBS, BSS, GOA, AI); maps 1:1 to `survey` and `survey_definition_id` (checked by crosstab) | yes (survey design) | category, 5 levels. NBS: 969 hauls, every one zero. BSS ends in 2016, so the newest window has none | fine | CLEAN-14 |
| `stratum` | "RACE database statistical area for analyzing data"; built as `srvy-number` because 26 numbers repeat across surveys | yes (a station's design stratum, set before the tow); no experimental stratum 0 in the data | category, 172 levels (9 with under 10 rows). **GOA 2025: 23 new numbers, 0 overlap with the 59 GOA strata of 1990-2023; all 431 GOA hauls of 2025 (10.2% of the newest window) carry one** | **cleaning problem: a code change over time** | CLEAN-21 |
| `latitude` | "Latitude ... of the start of the haul" (vessel position) | yes | float, 51.19-65.34. The source uses the net's midpoint, corrected for the net's distance behind the vessel (TM-459 Table 3). Taking the start avoids the tow length the end position would carry | fine | |
| `longitude_east` | start longitude mapped to 0-360 east | yes | float, 170.60-227.23. `% 360` is a per-row transform that joins the 2,567 Aleutian hauls west of 180 degrees to the rest | fine (CLEAN-12-style restoration) | CLEAN-12 |
| `date` | date of the haul; GAP: "All dates and times are in Alaska time (AKDT)", so the trailing "Z" is wrong and the local date is right | yes (survey schedule) | datetime `YYYY-MM-DD`; the time of day is dropped (see below) | fine. The notes could cite the GAP doc instead of inferring local time from the 05:00-23:00 hours | CLEAN-14 |
| `depth_m` | "Bottom depth (meters)"; "Gear depth plus net height equals bottom depth" | yes. The source trains on haul depth and predicts from a bathymetry raster; depth does not change between years | int, 9-1200, no sentinel values. **1993-95: headrope depth without the net height** (TM-459 p. 8). At the 376 EBS stations, 1993-95 depths are a median 1.25 m (mean 1.66 m) shallower than from 1996 on | minor cleaning note | CLEAN-21 |
| `bottom_temperature_c` | "Bottom temperature ...; NA indicates removed or missing values"; XBT point values 1982-92, tow averages from 1993 | at the haul, yes. At the review, no, for the years it predicts: the source trains on haul values and predicts from a mean raster for 1982-2019 (problem 1) | float, -2.1 to 15.3. The 37 hauls above 12 C are NBS/GOA hauls at 12-36 m with a similar surface temperature: plausible. 2 EBS hauls in 1984 are 3.3-4.4 C warmer at the bottom than at the surface: unusual, they stay. 4.5% missing, mostly AI 1991 (81%), GOA 1990 (60%), EBS 1994 (22%). Within 38 survey-year cells, 41.4% of hauls with a missing value caught rex sole, against 43.8% with a value. The missing indicator alone scores R^2 -0.009 (builder) | fine; note on the timing | LEAK-10 holds; LEAK-6 |
| `surface_temperature_c` | "Surface temperature ...; NA indicates removed or missing values" | same as bottom temperature. Not a covariate of the trawl SDMs in TM-357 (where it is used only by the ichthyoplankton models) or TM-459 (Table 3) | float, -1.1 to 18.1, 2.4% missing. Within 27 cells: 45.5% caught with a missing value, 46.0% with a value | fine. The note "the covariates the source trains on" does not cover it (wording) | LEAK-10 holds |

**Column table: the dropped HAUL columns**

| column | meaning | known at prediction? | verdict | rule |
|---|---|---|---|---|
| `performance` | "what, if any, issues arose during the haul" | no: recorded after the tow, about the tow; the builder's Decision table shows the catch rate differs by code | drop is right; the rows stay (all codes >= 0, satisfactory) | LEAK-10 |
| `duration_hr`, `distance_fished_km`, `latitude_dd_end`, `longitude_dd_end` | tow length and end position | the length is chosen during the tow and can respond to the catch (the builder's EBS pollock tows under 0.4 h) | drop is right | LEAK-10 |
| `area_swept_km2`, `net_width_m`, `net_height_m` | area swept = distance x net width, the target's denominator; net geometry | measured during the tow | drop is right: the measurement that defines the label's scale (CLEAN-22 lists that reason). The stated reason, "the EFH models use none of them", is not one of CLEAN-22's | LEAK-10, CLEAN-22 |
| `vessel_id`, `vessel_name` | the charter vessel | yes, before the haul. Every test haul's vessel appears in training in the two newer windows; 51.8% do not in 2012-16 | drop is fine in substance (the target is abundance at a place, and a map cell has no vessel), but the stated reason is not a CLEAN-22 reason (problem 4) | USE-3, CLEAN-22 |
| time of day (from `date_time`) | AKDT clock time | yes | same as the vessel. Note: on the slope (BSS), 35% of hauls before 08:00 caught rex sole against 58% after 16:00, a diel catchability effect; the other regions show none | USE-3, CLEAN-22 |
| `station` | design station id; EBS stations fixed (44 visits each), GOA mostly visited once | yes | drop is fine: the start position pins the place to within about 1 km, and the use case predicts places | CLEAN-3 |
| `hauljoin`, `cruisejoin`, `cruise`, `haul`, `survey`, `survey_name`, `survey_definition_id`, `year` | keys, a sequence number within the cruise, copies of `srvy`, copies of the date's year (`year` matches the date in all rows) | | drop is right | CLEAN-3, CLEAN-5 |

**Problems, ranked by principles.md**

**1. P4/P3, note only (LEAK-10 timing, LEAK-6 measured): the test hauls carry their own measured temperatures, which a
review does not have.** The prediction point is the review: models are fit on surveys up to two years earlier, and the
maps stand for five years. The source trains on haul temperatures but predicts from "Rasterized 38-year averages of
habitat covariates in each raster cell" (TM-459 pp. 8-10, Table 3: "Training: ... Prediction: raster"). TM-357 p. 12
did the same: "a single temperature raster layer that reflects the average temperature conditions ... from 1982 to
2014. This raster layer of average temperature was used for prediction." A 2024 haul's bottom temperature did not exist
at the 2022 review. Measured: I replaced the test hauls' temperatures with a climatology from the training
years only (the mean of the 10 nearest training-period hauls). The model is still trained on measured values, as the
source does. R^2 on log1p: 0.644 / 0.725 / 0.569 against 0.633 / 0.726 / 0.573 shipped. RMSE on raw density: 1,307 /
1,668 / 1,466 against 1,320 / 1,675 / 1,471. Dropping both temperatures gives 0.656 / 0.726 / 0.582. So the haul's own
values give no optimism; the shipped version scores slightly worse. **Mildest remedy:** keep them, and add one
sentence to the prediction-point bullet or to `fit_reason`. It should say that the source predicts from mean-temperature
rasters while the test hauls carry their own readings, and that swapping in a training-years climatology changes R^2 by
-0.004 to +0.012. Optional, for the curator: a climatology column is the source's own prediction covariate, and with it
in both training and test the model scores best (0.666 / 0.733 / 0.575). It would have to be built from the history
before the oldest test window (LEAK-29), so I do not propose it as a change.

**2. P5, question (PROV, in the spirit of LEAK-24's two-download check): the 2026 season is not finished in FOSS.**
All 226 rex sole catches of 2026 (AI 167, EBS 59) have `taxon_confidence` null. No catch of any earlier year does
(2024: 0 of 205; 2025: 0 of 377). The note "identified with high confidence in every catch since 1982" therefore holds
through 2025. The 722 hauls of 2026 are 17% of the newest test window. The EBS rex sole presence of 2026 is 0.169,
against 0.209-0.293 in 2018-2025: suggestive, not shown to be an artefact. **Mildest remedy:** reword the note to
"since 1982, 2026 not yet rated". Then either compare with a download after GAP finalizes 2026, or end the newest
window at 2025 if the counts move. The builder's second download two days later cannot show a revision.

**3. P7, CLEAN-21 (Should), the largest effect: `stratum` changes coding in GOA in 2025.** GOA had 59 strata in
1990-2023 and 23 in 2025, with no number in common. All 431 GOA hauls of 2025 carry a code no training row has (EBS and
BSS each gained one number in the 1980s/2000s; AI and NBS none). Effect (window 2022-26):

| variant | window R^2 log1p | GOA-2025 R^2 | window RMSE raw |
|---|---|---|---|
| shipped | 0.577 | -0.816 | 1,468 |
| GOA-2025 stratum set to missing | 0.577 | -0.816 | 1,468 |
| `stratum` dropped | 0.717 | 0.474 | 1,443 |
| GOA-2025 hauls given the pre-2025 stratum of their nearest pre-2025 GOA haul (position, log depth; median 2.2 km away) | 0.726 | 0.511 | 1,405 |

LightGBM routes the new codes like low-density strata: it predicts a mean log1p of 1.19 where the observed mean is 4.42
(70.5% of those hauls caught rex sole). On the older windows, dropping `stratum` costs 0.003 and 0.010 R^2, so the
column carries a little signal before 2025. The definition keeps the column "as a model fit at a review meets the
redesign too". The source's models have no stratum covariate (TM-459 Table 3), so the actor never meets the redesign.
What the newest window measures is how a model handles 431 unseen codes. **Mildest remedy:** put the 2025 GOA hauls on
the pre-2025 coding. The published pre-2025 GOA stratum polygons (GAP's akgfmaps) give the exact assignment; the nearest
pre-2025 haul is the map the data shows (zillow_prize's CLEAN-21 exception). That direction uses only a design that
existed before every test window. Do not map the historical hauls onto the 2025 design instead. That design was
optimized on historical survey densities of 14 groundfish species (Oyafuso et al. 2022; Stevenson et al. 2023
presentation; whether rex sole was one of them I did not verify), which overlap the 2012-21 test windows. Next rung:
drop `stratum` (position, depth and `srvy` hold most of what it means). Keeping it with the note is the last rung. The
college_scorecard precedent (a section with no conversion table stays dropped) argues against keeping a column whose
coding changed.

**4. P7, CLEAN-22 (Must on the reason, not on the outcome): the stated reason for the drops is not a CLEAN-22 reason,
and it is applied unevenly.** The vessel, the hour and the gear columns leave as "sampling details the habitat models do
not use". `stratum`, `date` and `surface_temperature_c` are not in the habitat models either (TM-459 Table 3) and stay.
CLEAN-22 accepts what a column is (a leak, an identifier, a copy, the measurement that defines the label), not whether
the source used it. Each drop holds under such a reason: the effort and gear columns define or respond to the catch
(LEAK-10, the label's denominator). The vessel and the hour describe the sampling event, not the place whose abundance
the map gives (USE-3, USE-5). **Mildest remedy:** reword the two curation bullets to these reasons; no change to the
frame.

**5. P7, CLEAN-21, minor: `depth_m` for 1993-95 is headrope depth.** TM-459 p. 8: "In 1993-1995, mean gear depth
measured at the headrope was equated with bottom depth. Since 1996, mean gear depth has been added to mean net height."
At the 376 EBS stations, 1993-95 depths are a median 1.25 m shallower than from 1996 on (1982-92 XBT: 1.0 m). All of
these rows are training rows in every fold, and the bias is about 1-2% of a typical depth. **Mildest remedy:** a note.
The fix, adding `net_height_m` for 1993-95, is cheap, but net height is missing for 22% of those EBS hauls.

**Claims touched**

- "Known for a haul: ... the depth and temperatures measured during the tow, the covariates the source trains on": true
  of the training side. The source predicts from mean rasters (problem 1), and surface temperature is not a trawl-SDM
  covariate in either memo.
- "it was identified with high confidence in every catch since 1982": true through 2025; 2026 is not rated yet
  (problem 2).
- "the timestamps end in 'Z' but are local times": true. The GAP column metadata says so directly (AKDT).
- "26 of the 141 stratum numbers are used by two surveys", "431 GOA hauls of 2025, 10.2% of the newest test window",
  "23 new stratum numbers": hold. "Kept, as a model fit at a review meets the redesign too" does not hold for the
  source's models (problem 3).
- "Missing bottom (4.5%) and surface (2.4%) temperatures stay missing": holds, and the missingness is not outcome-driven.
- The target's construction (zero fill; count / area swept; the 12 uncounted catches) holds.

**Judgment record**

```text
Verdict: ship after changes (stratum), notes otherwise.
Validity: LEAK-10 holds for all 8 features; drops of performance, effort and gear are LEAK-10 drops and hold.
  USE-3/LEAK-10 timing of the test hauls' temperatures: measured no gain (LEAK-6), keep with a note.
  P5: 2026 season unrated in FOSS, a question (reword; compare a later download).
Quality: CLEAN-21 stratum 2025 GOA recoding, fix (map 2025 hauls to pre-2025 strata; else drop).
  CLEAN-22 drop reasons reworded (vessel, hour: USE-3; gear: label denominator). CLEAN-21 depth 1993-95, note.
For the curator: whether to map, drop or keep `stratum` (problem 3); the 2026 season (problem 2).
```

Sources: [GAP Universal Column Metadata](https://afsc-gap-products.github.io/gap_products/content/product-metadata-column.html),
[gap_products docs](https://afsc-gap-products.github.io/gap_products/),
[Oyafuso et al. 2022](https://repository.library.noaa.gov/view/noaa/38939),
[Stevenson et al. 2023 presentation](https://groundfish.psmfc.org/wp-content/uploads/2023/05/8_3_Stevenson_Apr27_0910.pdf),
[2025 GOA survey data report](https://repository.library.noaa.gov/view/noaa/73915),
[2026 AFSC GTC report](https://groundfish.psmfc.org/wp-content/uploads/2026/04/2026-NOAA-AFSC-GTC-Report.pdf); memo texts
in the run folder (TM-357, TM-458, TM-459).

</details>

<details><summary>Split audit</summary>

**Split auditor: noaa_afsc_bottom_trawl_survey_cpue (2026-11-01)**

**Verdict: right with notes.** Temporal by survey year, three five-year windows with a two-year gap, fits the use case
(maps fit at a review stand for the years until the next one) and every Must of P4 holds. One change is recommended:
the 2025 Gulf of Alaska restratification breaks the newest window through the `stratum` column. The regime still needs
the curator's explicit pick (SPLIT-1, SPLIT-3).

Numbers come from the definition's frame and splits loaded through `dataset_io.from_definition`, with station ids
re-joined from the raw HAUL pages; models are untuned LightGBM (400 trees, learning rate 0.05) on log1p, features
`srvy`, `stratum`, latitude, `longitude_east`, depth, both temperatures, year and day of year. These are probe numbers,
not leaderboard numbers (EV-8). Scripts: in the run folder (not committed).

**Judgment record**

```text
Verdict: right with notes.
Validity: SPLIT-1, SPLIT-3 hold (temporal, one regime; the curator's pick not yet recorded); SPLIT-9, SPLIT-10 hold
  (labels known within the season, gap 2 years); SPLIT-11, SPLIT-14 hold (expanding, train 85% / 71% / 57%);
  SPLIT-12 holds (window = the 5-year review cycle, sourced); SPLIT-13 holds (stations recur, known waters);
  SPLIT-15 departed, forced by SPLIT-12 and SPLIT-14; SPLIT-20 concern (a design break in the newest window).
For the curator: confirm temporal over grouped-by-station; drop `stratum` (or blank the 2025 GOA design).
```

**Problems, ranked**

1. **The newest window scores how a model treats an unseen category (P4, SPLIT-20, Should: a break in the data
   collection; remedy at P7, CLEAN-22).** All 431 GOA hauls of 2025 (10.2% of the 2022-2026 window) carry a stratum of
   the new GOA design that no training row has; the definition keeps `stratum` "as a model fit at a review meets the
   redesign too". The source's models do not meet it: TM-459's Table 3 (pp. 35-36) lists bottom temperature, bottom
   currents and their variability, tidal current, position, depth, slope, bathymetric position index, aspect,
   curvature, sediment grain size and coral, sponge and sea-whip presence, and "strata" appears only in the
   survey-design description (TM-458 p. 5), so the reason given does not hold. Measured on the newest window (train to 2019):

   | test hauls | with `stratum` | without `stratum` |
   |---|---|---|
   | GOA 2025 (431) | R^2 log1p -0.639; mean prediction 1.51 against 4.42 observed; 39.3% of the window's raw squared error | R^2 0.481; mean prediction 4.61; 34.3% |
   | GOA 2023 (523) | R^2 0.611 | R^2 0.598 |
   | the other 3,799 | R^2 0.735 | R^2 0.729 |

   Window R^2 is 0.598 with and 0.719 without (the builder's 0.598 and 0.719 reproduced); a random forest on integer codes is
   not hurt (0.735 and 0.742, builder's probe). Split 0 (SPLIT-11: the most representative window) would rank models
   partly by their unseen-category handling (with LightGBM's native categories the new levels get low-density predictions, mean 1.51 against 4.42).
   The hidden-group line on unseen stations shows the same: in 2022-2026, test hauls at stations seen in training score
   R^2 0.732, the 645 unseen ones -0.213; 431 of them are GOA 2025. Re-splitting does not help, because any window holding
   2025 has the break. Mildest remedies, in order: drop `stratum` (mean R^2 over the three windows 0.687 against 0.652;
   the leak probe's "without stratum" 0.690 against 0.632; position and depth carry the place; the GOA and AI strata are
   depth bands, TM-458 p. 5), or set the stratum of the post-2025 GOA design to missing. If the curator keeps it, the
   anomaly bullet should say the source's models use no stratum and give the GOA 2025 effect (R^2 -0.64, 39% of the
   squared error). Shared with the column auditor.

**Notes (no change needed unless stated)**

2. **The regime: temporal is the right reading, but it is not yet the curator's recorded pick (P4, SPLIT-1, SPLIT-3,
   Must; USE-10).** `required_split: Temporal` came from the AI triage of 2026-10-20; the screening says "grouped by
   station the alternative ... (SPLIT-3: one, the curator's pick)", and the CC of 2026-10-30 records only `Yes`,
   priority 5. For temporal: EFH is reviewed "at least every 5 years" (50 CFR 600.815(a)(10), TM-459 p. 2) and a
   review's maps stand until the next one, and the source tested forward in time itself ("we assessed the forecasting accuracy of the 2017 SDM
   approach", TM-459 p. 3; Pirtle et al. 2020 not read). For grouped: the source's own CV is random 10-fold over hauls,
   described as "a test of prediction skill at unsampled locations" (TM-459 pp. 20-21), and wadden_sea_sibes_macoma_abundance
   (same run) took grouped by station for a map drawn between the stations of a surveyed year. What sets this case apart
   from wadden_sea is the five future years each map stands for. The three regimes on the same model:

   | split | R^2 log1p per fold or window | mean | raw RMSE |
   |---|---|---|---|
   | shipped: temporal, gap 2 | 0.598 / 0.722 / 0.635 | 0.652 | 1,472 / 1,652 / 1,315 |
   | grouped by station, 3 folds | 0.700 / 0.682 / 0.679 | 0.687 | 1,300 / 1,447 / 1,478 |
   | IID, 3 folds (the source's protocol) | 0.727 / 0.743 / 0.725 | 0.732 | 1,355 / 1,456 / 1,355 |

   The source's random CV is optimistic by about 0.08 R^2 against the shipped windows (SPLIT-5: a prescribed split is a
   claim). The temporal split does not drop the spatial question: 84.7-85.3% of test hauls are at a station sampled in
   training (EBS 100%, AI 93-97%, GOA 40-65%, slope 66%), so 15% of each window (mostly GOA, whose stations are drawn
   anew each survey) tests new locations, scoring R^2 0.50 in the two older windows against 0.65-0.74 at seen stations.
   Recurring stations are part of the task (SPLIT-13): the maps cover the surveyed waters. Remedy: a one-line CC
   confirming temporal.

3. **The gap and late labels (SPLIT-9, SPLIT-10, hold).** A catch is recorded at sea and FOSS is updated after every
   season, so labels arrive within months; the two-year gap is a planning gap, the lag from the last survey a review
   uses to the review (TM-357 p. 5: "We included trawl survey data from 1982 through 2014"; TM-459 p. 3: surveys
   1982-2019). No training row has a label unknown at its window's start. The 2017 maps were approved on 5 July 2018
   (83 FR 31340, TM-459 p. 3), so a gap of three (test from the year after the review) is a defensible reading too; it
   changes little: mean R^2 0.664 with no gap, 0.652 with 2, 0.644 with 3. Keep.

4. **Windows and their sizes (SPLIT-12, SPLIT-14, SPLIT-15, SPLIT-17).** Test 4,230 / 3,953 / 4,806 hauls, train
   30,273 / 25,253 / 20,384 (85.2%, 71.0%, 57.3% of 35,549). "Nine" for an IID task of this size holds
   (`recommended_dimensions`: 3 x 3). Nine five-year windows cannot be had: a fourth window (2007-2011) would train on
   hauls to 2004, 43.6% of the rows, below SPLIT-14's floor. So the departure from SPLIT-15 is forced by SPLIT-12
   (earlier, same strength) and SPLIT-14 (Must); `splits_comment` could give the 43.6%. Every window holds whole summer
   seasons (May-September). Composition differs by window: the slope survey ended in 2016, so it is tested only in
   2012-2016 (364 hauls); 2017-2021 holds one Aleutian survey (2018, 420 hauls; none in 2020); NBS hauls, where rex sole
   was never caught, are 9.4% and 10.9% of the two newest windows. None of this needs a change.

5. **Training history (SPLIT-19, SPLIT-20, hold apart from problem 1).** Expanding from 1982, as the source ("we include
   trawl survey data from 1982 to 2019 in our analyses", TM-459 p. 5). FOSS starts GOA in 1990 and the Aleutians in 1991,
   so the early foreign-vessel GOA years are not in. Breaks in the history: XBT temperatures 1982-1992 (TM-459 p. 8;
   temperatures add little, note 6), the EBS grid from 376 to 350 stations in 2024, and the GOA redesign of 2025 (problem
   1). The windows were set from the review cycle, not from scores (SPLIT-21 holds).

6. **The temporal story against the measured temperatures (USE-3; for the column auditor and the domain
   practitioner).** "A model fit at a review predicts the surveys of the years it is used" implies inputs known at the
   review, but each test haul carries its own measured bottom and surface temperature, while the source predicts from
   "a raster layer of average temperature" (TM-357 p. 12). Measured on the shipped windows, the temperatures give the
   test no material advantage: mean R^2 0.652 with both, 0.651 without (newest 0.598 to 0.572, oldest 0.635 to 0.659),
   raw RMSE 1,472 / 1,652 / 1,315 with and 1,461 / 1,642 / 1,286 without. No change to the split.

7. **Hidden groups and copies.** Exact copies across the split 0% (leak probe); near copies not run (7 columns, no
   evidence either way). `stratum` seen in training for 96.6% of test rows (hidden-group probe), stations for 85%: both
   part of the task in a temporal split (SPLIT-13). Under an IID split the station would be a hidden group (EBS: 43
   hauls per station), costing 0.045 R^2 (0.732 IID, 0.687 grouped).

**Cannot verify**

* Pirtle et al. (2020), the 2022 review's forecast test (which years trained and which were tested): not found; the
  NPFMC page returned 403. `splits_comment` already marks it "not read".
* Whether FOSS's 2026 values are final: the counts match a full season (EBS 350 of 350; Aleutians 372 hauls ending
  2026-08-04, against 307 ending 2024-07-30 and 398 ending 2022-08-13), but finality is not stated.
* GOA's own review cycle (2023 memo, TM-468, not read): GOA maps may run a year behind the Bering Sea and Aleutians,
  while the windows put all regions on the 2017/2022 cycle. Minor at a five-year window.

**Split claims checked**

| claim | result |
|---|---|
| windows 2022-2026, 2017-2021, 2012-2016; no survey in 2020; trained to 2019, 2014, 2009 | holds (README split table; no 2020 rows) |
| gap = lag from last survey to review (2017: to 2014; 2022: to 2019) | holds (TM-357 p. 5; TM-459 p. 3) |
| oldest training side keeps 57% | holds (57.3%) |
| nine windows for an IID task of this size | holds (3 x 3) |
| source scored on hauls held out at random | holds (TM-459 pp. 20-21: random 90% in-bag partitions, 10-fold) |
| 431 GOA 2025 hauls, 10.2% of the newest window, stratum unseen in training | holds (431 of 4,230, all unseen) |
| "kept, as a model fit at a review meets the redesign too" | refuted in substance: the source's covariates include no stratum |
| R^2 0.598 with `stratum`, 0.719 without on the newest window | holds (reproduced) |
| 96.6% of test rows have a stratum seen in training | holds (probe) |
| the 2022 review "assessed the forecasting accuracy of the 2017 SDM approach" | holds as a quote (TM-459 p. 3); the method behind it is unverified |

</details>

<details><summary>Domain practitioner</summary>

**Domain practitioner (the actor: an AFSC habitat analyst preparing the five-year EFH review), 2026-11-01**

**Verdict.** Fit **approximate** (I agree with `fit="approximate"`). The haul rows, the density target and the
five-year forward windows follow how AFSC's habitat team skill-tests its EFH models on these same surveys. The decision
itself is a percentile map of 1-km raster cells, made per region and per life stage from long-term habitat layers that
FOSS does not hold, so the pooled all-sizes score per haul stands in for it (USE-8). The use case is real and strong
(P3): the actor, the moment fixed in law (50 CFR 600.815(a)(10), "at least every 5 years", TM-459 p. 2), the decision
and the model-selection rule are all written in the source. No other use case makes the fit direct (USE-9). The
metric scores my decision **partly** (MET-1, MET-2).

**How the decision is made today (TM-459, Laman et al. 2022; Barnes et al. 2022)**
- For each species, life stage and region (separate memos: Bering Sea TM-459, Aleutians TM-458, Gulf of Alaska 2023),
  five SDMs (MaxEnt, paGAM, hurdle GAM, Poisson GAM, NB GAM) are fit to numerical abundance with an area-swept offset.
  They are fit on the haul's measured depth and temperature plus habitat rasters averaged along the tow path:
  sediment phi, slope, BPI, tidal maximum, ROMS bottom currents, presence of structure-forming invertebrates (pp. 7-15).
- Models are kept and weighted by the lowest RMSE of abundance at the stations under 10-fold random CV
  (pp. 3, 16, 20-21). Spearman's rho, AUC and Poisson deviance explained are reported next to it, scored on a rubric
  (pp. 24-27).
- The map is predicted from "Rasterized 38-year averages of habitat covariates" (p. 8), not from yearly conditions.
  EFH is the area holding 95% of the predicted abundance, counting only the cells with an encounter probability of at
  least 5%, computed as 1 - exp(-predicted abundance) (pp. 27-28). The principal (75%), core (50%) and hot-spot (25%)
  areas are cut the same way.
- At the next review, the team checks the old model against the surveys that came after it. TM-459 p. 3 "assessed the
  forecasting accuracy of the 2017 SDM approach". Barnes et al. 2022 (same team, EBS trawl data) run retrospective
  skill tests (fit to 1982..t, forecast t+1..2018) and score them by **Spearman's rho** "because it is a rank-based ...
  measure" that "emphasizes a model's ability to identify relative differences" (pp. 3, 6).

**1. Inputs at the moment of prediction**
- I have them: region (`srvy`), the design stratum (known before the survey, including the 2025 GOA restratification,
  which a model cannot learn), the position (I have every cell's position; the source uses the tow midpoint, the
  dataset the start, about 1.4 km apart for a 30-minute tow), the date, and depth (from the bathymetry raster at map
  time, close to the measured value).
- I would not have them for a future haul: the measured bottom and surface temperatures. At map time I use the
  long-term mean raster. Strictly, under USE-3 these values did not exist at the review. They carry almost no signal,
  so the gap is a wording issue, not a leak worth acting on. LightGBM over the three windows:
  - R^2 on log1p: 0.652 with the measured temperatures, 0.651 without them, 0.644 with each stratum's training-period
    mean in their place;
  - Poisson-objective RMSE: 1,385, 1,384 and 1,372.

  The source itself trains and tests on the measured values (TM-459 pp. 8-9), so keeping them is right. Surface
  temperature is a covariate for eggs and larvae only (TM-357), harmless here.
- I always have these and they are missing: the habitat rasters. The Bering Sea rex sole ensembles keep ROMS bottom
  current, tidal maximum and pennatulacean presence besides position, depth and temperature (TM-459 pp. 150-152,
  Table 23). On the fixed EBS grid (each station sampled about 44 times) position stands in for the static layers. In
  GOA and the Aleutians, where stations move each survey, sediment, rockiness and slope would matter more (not
  measurable from FOSS).

**2. Target**
- What I act on is the expected numerical abundance per life stage per raster cell, turned into percentile areas.
- Numbers per km^2 per haul is the observed quantity the models are fit to, so it is the right target. It counts all
  sizes, while EFH must be described per life stage (50 CFR 600.815(a)(1), TM-459 p. 2). The source pools life stages
  only when lengths cannot split a catch (pp. 6-7), and rex sole's subadult and adult EFH differ (the adults extend into
  Bristol Bay, p. 152).
- I need a number on the **mean** scale. The encounter probability (1 - exp(-lambda)) and the cumulative percentiles
  both use the absolute mean. Shipping log1p is allowed (MET-3), but untuned models fit on log1p and inverted predict
  only 33-49% of the observed mean density on the test windows. I would not accept that without a bias correction.

**3. Row and test data**
- One row is one haul, the unit at which the source selects and weights models (TM-459 p. 21: "a test of prediction
  skill at unsampled locations"). It is not the unit of the map.
- The test windows (the next five survey years after a two-year lag) are the comparison the next review makes, and the
  retrospective skill test the team recommends (Barnes et al. 2022). They are real and arguably closer to the use than
  the source's random CV.
- Their region mix moves with the survey calendar:
  - 2022-2026: EBS 1,802, AI 1,077, GOA 954, NBS 397;
  - 2017-2021: GOA 1,598, EBS 1,504, NBS 431, AI 420;
  - 2012-2016: EBS 1,880, GOA 1,313, AI 1,249, slope 364.

  The slope survey has not run since 2016. The NBS hauls (9-11% of two windows) are all zeros, a true absence that
  `srvy` predicts.

**4. Would I use the model?** As one more constituent of the ensemble, yes, if it beat the GAMs on RMSE **within my
region** and passed the source's filter (predictions no more than 10 times the highest observed abundance, p. 22).
- What builds trust: skill holds within each region. Untuned models reach within-region Spearman rho of 0.60-0.69 on
  EBS, 0.61-0.75 on GOA and 0.58-0.80 on the Aleutians, "excellent" on TM-459's rubric. For comparison, the source's
  ensembles reach 0.52 (subadult) and 0.56 (adult) under random CV on the Bering Sea (Table 22); the two are not
  directly comparable.
- What makes me distrust it: a single pooled number. It cannot tell the Bering Sea analyst whether the model is good
  for the Bering Sea, and nothing in the task checks for patchy step-function maps or life-stage structure.

**5. Does `rmse` on numbers per km^2 score my decision? Partly.**
- What is right: it is the source's deliberate selection rule (MET-5; TM-459 pp. 3, 16, 21: "the model with the lowest
  RMSE was considered to be the best performer"). It is scored on the mean scale the map needs (MET-3, MET-8), and its
  `original` and `definition` state the offset and density difference correctly (MET-11).
- What is not: the source scores one region (and one life stage) at a time; the dataset pools four regions (MET-2: the
  meaning changes). My probe (a script in the run folder, not committed) shows the effect:
  - GOA hauls are 23-40% of each test window but hold **71-92% of the squared error**.
  - EBS hauls are 38-43% of the test hauls and hold 0.4-13% of it.
  - So the declared score is mostly a Gulf of Alaska score, and its 10-31 decisive hauls are mostly GOA hauls (22-28 of
    the top 30). Over five untuned models, the pooled ranking agrees with the EBS-only RMSE ranking at Kendall tau 0.8,
    1.0 and 0.2 across the three windows.
  - It barely agrees with the Spearman rho that the same team uses for forecast skill: tau -0.2, -0.4 and 0.2.
- Switching to Poisson deviance would not fix the region weighting: GOA still holds 52-84% of it for the fitted
  models. It would also make the log1p-inverted LightGBM lose to the constant mean in the newest window (deviance
  1,917 against 1,718).
- **Metric I would choose:** the source's RMSE on numbers per km^2, **computed per survey region and averaged**, so each
  region's review counts once (MET-1: the unit I act on is a region's map; MET-2). The alternative is to keep the
  pooled RMSE and state in the metric note that GOA holds 71-92% of it. Restricting the table to one memo's study area
  (EBS shelf, slope and NBS, as TM-459) would make the source's RMSE exact in meaning, but it gives up the
  zeros-in-every-region rationale for rex sole.
- Not Spearman rho as the declared metric. It is the forecast-skill measure of Barnes et al. 2022 and the closest to
  the percentile map, but it ignores the absolute scale that sets the 5% encounter threshold, and with 62% tied zeros
  it mostly scores presence. MET-8 prefers a score of the mean.
- A region-averaged RMSE is a custom metric with `srvy` as a scoring column. `stratum` already encodes the region,
  so dropping `srvy` as a feature loses nothing. MET-12 and MET-13 ship it only if other definitions use it; the
  curator decides.

**Gaps between the dataset and the real decision, most consequential first**
1. All regions are pooled under one mean-scale RMSE. The review fits and selects per region, and the score is 71-92%
   GOA (MET-1, MET-2; above).
2. The unit of decision is a map of raster cells from long-term habitat layers (sediment, currents, tides, terrain,
   invertebrates), and FOSS ships none of them. The task reproduces the model-selection step at hauls, not the map
   (USE-8, already in `fit_reason`).
3. Life stages are pooled into one all-sizes count, while EFH is described per life stage (USE-5; already in the
   notes).
4. The target ships as log1p, but the decision needs the mean. Inverted log models underpredict by a factor of 2-3,
   which RMSE punishes only mildly (MET-3; a trap for methods, not a data error).
5. The prediction point overstates what is known: a future haul's measured temperatures do not exist at the review.
   Measured: no signal (USE-3; wording only).
6. The split rationale says "a model fit at a review predicts the surveys of the years it is used". The review's map
   uses 38-year means and is not a forecast of particular hauls. The windows instead mirror the next review's check of
   the previous model (TM-459 p. 3; Barnes et al. 2022). The design is real; only the reason needs rewording.

**What an expert in the domain would change**
- Score per region (or restrict to one region). At minimum, write in the metric note that GOA hauls hold 71-92% of the
  squared error, next to the existing "10-31 test hauls" sentence.
- Reword `task_summary.known` and the first `curation_comments` bullet so the prediction point reads as a habitat
  model scored at a haul's measured conditions, as the source's skill test does. Keep the temperatures and add the
  no-signal numbers above.
- Reword `task_summary.split` and `splits_comment` to give the forecast-check reason (TM-459 p. 3; Barnes et al. 2022,
  retrospective skill testing, Ecography e06189). Cite TM-459 p. 8 for the long-term-mean maps.
- Optional and beyond FOSS: public rasters (EBSSED-2 sediment, Bering10K ROMS currents, AFSC bathymetry and terrain)
  would close part of gap 2. That would be a rebuild, not a requirement.

**Sources**
- Laman et al. 2022, NOAA-TM-AFSC-459, <https://repository.library.noaa.gov/view/noaa/48659> (pp. 2-3, 5-9, 16-28,
  149-153, 494-502).
- Laman et al. 2017, NOAA-TM-AFSC-357, for the surface-temperature use.
- Barnes, Essington, Pirtle et al. 2022, "Climate-informed models benefit hindcasting but present challenges when
  forecasting species-habitat associations", Ecography 2022(10) e06189; NOAA copy
  <https://repository.library.noaa.gov/view/noaa/49312> (pp. 2-3, 6, 8-9).
- My probes on the shipped splits: scripts and outputs in the run folder (not committed). All models are
  untuned, so the numbers are indicative.

</details>

<details><summary>Blind review</summary>

**Verdict: include with changes.** The data is real, the target matches the source exactly, and the task (haul-level species-distribution prediction, scored forward in time) is a genuine one. But the `stratum` column breaks in the newest test window, and the task card does not say which species the target is. Both need fixing before scoring.

**What the task is**

The target is zero-filled numerical CPUE (fish per km² swept), as log1p, of **rex sole (*Glyptocephalus zachirus*, FOSS species_code 10200)**. Each row is one survey tow from the NOAA AFSC bottom trawl surveys: EBS shelf 1982-2026, AI 1991-2026, GOA 1990-2025, EBS slope 2002-2016 and NBS 2010-2025. task.md never names the species. I identified it myself: I took 4 random positive rows, matched them to the FOSS catch table, and only code 10200 fit all four. I then pulled every FOSS haul (35,561) and every rex sole catch record (13,557), and rebuilt the target with zero-filling. **All 35,549 rows match exactly (max absolute difference 0.0).** Depth and temperatures also match the FOSS haul table exactly.

Who uses this: AFSC assessment and essential-fish-habitat (EFH) scientists, and anyone forecasting distribution shifts. They model density at a tow from location, depth and temperature. They use it to build abundance indices, to map EFH, and to check whether next year's survey catch is in line with past years. Training on past surveys and testing on later ones fits that use.

**Concerns, most to least serious**

1. **`stratum` breaks in the latest test window (GOA 2025 redesign).** The GOA survey was redesigned in 2025. The data report says it "was redesigned in 2025 to be more flexible to changes in survey effort and species distributions", moving from 59 historical strata to about 30 depth- and NMFS-area-based strata. All 23 GOA stratum codes in 2025 (431 rows) never occur in earlier years. I trained LightGBM on years before 2024 and tested on 2024-2026:
   - GOA 2025 RMSE is 4.24 with `stratum` and 2.24 without it.
   - The mean prediction is 1.22 against a true mean of 4.42.
   - The whole window's RMSE rises from 1.57-1.63 to 2.24 (R² 0.42 instead of about 0.74 in the earlier windows).

   The column adds nothing elsewhere. In the 2019-21 and 2022-23 windows, location+depth without stratum scores 1.697 and 1.549, against 1.706 and 1.540 with it. So the benchmark would mostly be testing how each method handles unseen categories. **Change:** drop `stratum`, since latitude, longitude and depth already carry the stratum information. The other option is to assign every haul to one consistent stratification, such as the legacy GOA polygons, using its position.

2. **The target species is not documented.** Without the species name a reader cannot judge whether the values make sense, why NBS is all zeros, or which stock the task represents. **Change:** add "rex sole, species_code 10200, cpue_nokm2 zero-filled across all FOSS hauls, log1p" to task.md. If other species from the same survey are in the benchmark, they share every feature row and the same station grid. They should be treated as one family of related datasets, not as independent tasks.

3. **Mostly spatial memory, and temperature adds little.** Stations are revisited: the 376 EBS grid stations every year, and 98% of AI rows are at stations sampled more than once. A distance-weighted k-NN on latitude and longitude alone scores RMSE 1.73, 1.52 and 1.54 across the three windows. That is about the same as the best LightGBM (1.63, 1.50, 1.57-1.63). Adding the two temperatures did not help: 1.728 vs 1.697, 1.543 vs 1.549, 1.616 vs 1.568. Adding year and day-of-year helps a little (1.633, 1.496). The weak baselines are much worse:

   | Baseline | RMSE range across windows |
   |---|---|
   | Global mean | 2.94-3.42 |
   | Survey mean | 2.62-2.74 |
   | Stratum mean | 2.10-2.25 |
   | Spline ridge | 2.07-2.13 |

   So there is real signal and the task is not trivial. But strong methods will probably be hard to tell apart. For EBS, the leave-one-out station mean already gives RMSE 1.05, and the same station's value from the previous survey has correlation 0.82 with the current one. I would keep the dataset, knowing it rewards spatial interpolation rather than rich feature interactions.

4. **Zeros and survey-specific dead weight.**
   - 61.9% of targets are 0. The smallest positive value is log1p(15.8) = 2.82, so the target has two humps with a gap between them, and RMSE is dominated by getting presence or absence right.
   - All 969 NBS rows are 0 (rex sole does not occur there). They are trivial once `srvy` is known, yet they appear in every test window (NBS in 2021, 2022, 2023 and 2025).
   - The 1,136 EBS slope (BSS) rows end in 2016, so they only ever appear in training.

   This is acceptable, but the task card should say so. Dropping NBS would remove free points. The metric should be chosen knowing the target is a hurdle-type (zero-or-positive) quantity.

5. **Temperatures are measured during the tow.** Bottom and surface temperature are recorded on the same tow as the catch. That is fine for a habitat model or a same-season prediction. It is not information you would have *before* a survey, unless it came from an ocean model (e.g., ROMS hindcasts). It is not leakage of the target: it does not encode the catch, and it adds no skill (point 3). The task card should describe the use as "habitat model / same-season prediction", not "pre-survey forecast".

6. **12 hauls were dropped.** These are tows with positive rex sole weight but no recorded count (cpue_nokm2 null), mostly GOA 1993. Dropping them rather than filling them with 0 is the right call. Since all 12 are positive catches the bias is tiny (12 of 13,557 positives). Using cpue_kgkm2 as the target would avoid the gap entirely.

7. **Different gear across surveys.** EBS and NBS use the 83-112 eastern otter trawl; GOA, AI and the slope use other nets, so catchability differs. `srvy` is a feature, so models can learn the offset. This is minor.

**Preparation checks that passed**

- Longitude is shifted to 0-360 east, which correctly handles the Aleutians crossing the date line.
- Missing temperatures are left as NaN: 4.5% for bottom and 2.4% for surface, worst in 1990-91 at about 45%.
- `srvy` and `stratum` are categorical; depth is an integer.
- No duplicate feature rows; only 1 latitude/longitude pair repeats.
- Year coverage matches the survey history: no 2020 (COVID), EBS drops to 350 stations from 2024, GOA has 431 stations in 2025.
- Values are plausible. The bottom temperatures up to 15.3 °C are shallow NBS tows in the 2019 heat-wave year.

**What I could not check**

- The exact boundaries of the three test windows. I assumed year blocks 2019-21, 2022-23 and 2024-26. If the last window does not contain GOA 2025, concern 1 shrinks but does not go away: the next GOA survey will again have only new codes.
- Whether `date` is given to models as a feature, and which metric is used.
- Whether the 2025-2026 FOSS records are final or will still be revised.
- Whether other species from this survey are also in the benchmark.

I used only the clean-room folder, the public FOSS API, the gap_products documentation and a web search. I did not open any other local files.

Sources: FOSS haul/catch/species APIs (apps-st.fisheries.noaa.gov/ods/foss/...); https://github.com/afsc-gap-products/gap_products; https://afsc-gap-products.github.io/gap_products/content/product-metadata.html ("CPUE_NOKM2: Numerical catch per unit effort (area swept by the net, units square kilometers)"); 2025 GOA data report https://repository.library.noaa.gov/view/noaa/73915; https://groundfish.psmfc.org/wp-content/uploads/2023/05/8_3_Stevenson_Apr27_0910.pdf (59 historical strata to 30).

</details>

<details><summary>Precedent check</summary>

**Precedent checker: noaa_afsc_bottom_trawl_survey_cpue (2026-11-01)**

**Verdict: mostly consistent; two decisions need the curator.** I checked 18 decisions. 14 follow a precedent, or the
order of the rules, or a written fact that sets them apart. Two depart from a sibling with a reason that holds: the
species, and temporal where wadden_sea_sibes is grouped. Two need the curator:

* the vessel and time-of-day drop is written as a departure from USE-6. USE-6 is a Must and allows no exceptions; read
  under USE-3, as wadden_sea_sibes_macoma_abundance does, the drop is consistent.
* `stratum` holds two GOA survey designs in one column. The CLEAN-21 precedents (college_scorecard, zillow_prize) put a
  coding that changes at a date back on one scale or drop it.

I found no drift in Andrej's decisions and no third exception, and none of the register's 14 flags touches this
dataset. Two of the builder's draft issues need no decision: issue 1 is settled by rule order and SPLIT-14, and the
"source or stand-in?" part of issue 2 by the claim auditor's measurement.

```text
Consistency: follows SPLIT-12 (house family, Lennart 2026-10-21), MET-3 and MET-5 (forest_fires, 2026-10-21), TP-6 as
  amended (Lennart 2026-10-21), MET-11 (porto_seguro identity), PROV-9 (rain_in_australia, Lennart 2026-10-26),
  CLEAN-15 (qsar_tid_11), CLEAN-14 (zillow_prize census_tract); fremtpl2's exposure call (Andrej 2026-10-20) by a
  written distinguishing fact.
Departs, reason stated and holding: the species (the siblings take the source's species; this source has no primary
  one); temporal where wadden_sea_sibes is grouped (each map stands for five future years).
Departs, not reasonable as written: vessel and hour "depart from USE-6" (a Must, no exceptions): reframe as USE-3.
Departs, reason contested: `stratum` across the 2025 GOA redesign, against the CLEAN-21 precedents.
Process: the regime is still the AI's pick; the screening left it to the curator.
```

**What counts as a precedent here.** A precedent is a curator's decision: Lennart's in the rule files' Cases tables
and the register, and Andrej's CC lines, including the policy calls of 2026-10-30 in
the zero-inflated triage summary (no longer in the repository; each call is in its record's Assessment of 2026-10-30). The same run's definitions are AI drafts that no curator has
reviewed yet: wadden_sea_sibes_macoma_abundance, cape_floristic_region_family_cover, crms_phragmites_cover and the
insurance siblings. They are siblings that should be decided alike, not precedents, and I mark them "same run". The
run's register (in the run folder) holds three decisions on this
record: the screening, the Assessment line on species-abundance mapping (SEL-2), and Andrej's CC `Yes`, priority 5,
of 2026-10-30.

**Decisions at a glance**

| # | Decision | Rule | Closest precedents | Status |
|---|---|---|---|---|
| D1 | rex sole as the species | USE-5, CLEAN-8 | wadden_sea, cape_floristic (same run: the source's species); Andrej 2026-10-30, policy 2 | departs, reason stated |
| D2 | numbers per km^2, zero fill, shipped as log1p | USE-5, CLEAN-16, MET-3 | forest_fires; Andrej 2026-10-30, policies 2 and 4; wadden_sea (same run) | consistent |
| D3 | `Metric.source("rmse")` on numbers per km^2 after the inverse | MET-3, MET-5, MET-11, TP-6 | forest_fires, zillow_prize, numerai_v5_2_1m, porto_seguro (2026-10-21) | consistent |
| D4 | temporal regime | SPLIT-1, SPLIT-3 | the temporal-against-grouped tension (Lennart 2026-10-12); wadden_sea (same run, grouped); covertype (Lennart 2026-10-01) | departs from the sibling, reason stated; curator's pick not recorded |
| D5 | three five-year windows | SPLIT-12, SPLIT-14, SPLIT-15 | house family (Lennart 2026-10-21); rain_in_australia (Lennart 2026-10-26) | consistent, no exception needed |
| D6 | two-year gap | SPLIT-10 | house_sales, zillow_prize (label delays); the rule's planning-gap clause | consistent |
| D7 | effort, gear and end position dropped | CLEAN-22, LEAK-10 | fremtpl2 (Andrej 2026-10-20); the insurance calls of 2026-10-30 | consistent by a written fact |
| D8 | vessel and time of day dropped | USE-3, USE-6, CLEAN-22 | 2_month_survival_rate_prediction (Lennart 2026-10-26); wadden_sea (same run); against: brazilian_ecommerce (2026-10-15) | not reasonable as written; consistent under USE-3 |
| D9 | performance code dropped, its hauls kept | LEAK-10 | the rule text ("a column recorded after the outcome") | consistent |
| D10 | `stratum` kept across the 2025 GOA redesign | CLEAN-21, CLEAN-22, SPLIT-20 | college_scorecard (Lennart 2026-10-16); zillow_prize (Lennart 2026-10-26) | departs, reason contested |
| D11 | identifiers and `station` dropped, `srvy` and `stratum` kept | CLEAN-3, CLEAN-5, CLEAN-14 | zillow_prize census_tract (Lennart 2026-10-26) | consistent |
| D12 | `longitude_east` (0-360) | CLEAN-21, CLEAN-2 | none in the register | consistent with the rules |
| D13 | 12 catches weighed but not counted dropped | CLEAN-15 | qsar_tid_11 (Lennart 2026-10-21) | consistent |
| D14 | other species' catch not shipped | LEAK-10, USE-3 | cape_floristic, wadden_sea (same run) | consistent |
| D15 | `year = "2026"` | PROV-9 | rain_in_australia (Lennart 2026-10-26); wadden_sea 2024 (same run) | consistent; the record still says "stays empty" |
| D16 | fit approximate | USE-8 | wadden_sea (same run) | consistent |
| D17 | warning `task_target_value_dominant` accepted | definitions.md, warning table; the task_probes zero-inflated pattern | wadden_sea, frempl, spanish_2022, pg17 (same run) report the oracle bound | consistent; oracle bound missing |
| D18 | missing temperatures stay missing | CLEAN-2 | | consistent |

**D1. Species: rex sole (USE-5, Must; CLEAN-8, Must). Departs from the siblings, with a reason stated.**

* The same-run siblings take the species or family their source names: wadden_sea_sibes takes Macoma balthica,
  "the paper's species" (Lyashevska et al. 2016), and cape_floristic takes Crassulaceae, the family the paper
  analyses. The EFH memos model 31 to 36 species with no primary one, so here the choice had to be ours.
* The reasons are written down: zeros inside every surveyed region, not whole-region absences; high-confidence
  identification since 1982, so early zeros are absences; modelled in the 2017 hurdle class and again in 2022.
* Two points for the curator (builder issue 3):
  1. Part of the stated reasoning is the zero structure (cod is rejected for "4% zeros on the EBS shelf"). Andrej's
     call of 2026-10-30, policy question 2, makes zero inflation no criterion in itself: "We want to add any relevant
     predictive task, independent if it is zero inflated or not." The reasons that stand without it are the
     identification history and the fact that the zeros are habitat outcomes rather than a region code. By that call
     Pacific cod, a managed species with its own EFH maps, would be just as valid.
  2. CLEAN-8 (Lennart 2026-10-19; rosbank1, alfa_battle_2_0_task_2, anes_voting_2026) treats a choice made by counts
     over the whole table as ordinary cleaning, but in a temporal task the notes must say it approximates the task.
     The species was screened on 1982-2026 prevalence, test windows included (the builder's species screen), and on
     test-window hurdle scores (the builder's hurdle probe). One sentence in the species bullet would cover this.

**D2. Target: numbers per km^2, zero fill, shipped as log1p. Consistent.**

* Zero fill follows the source's own recipe (gap_products sec. 10.2), like wadden_sea's descriptor recipe. Andrej's
  policy call 2 (2026-10-30) makes coded zeros a cleaning choice.
* The `Two-Regime Zeros` tag meets Andrej's definition (policy call 4: the low value dominates and is separate):
  62% zeros, with continuous positives above them.
* Numbers rather than kg: the 2022 review's RMSE is on "numerical abundance at trawl station i" (TM-459 pp. 20-21,
  read).
* Shipping the target as log1p and scoring the raw scale is the MET-3 pattern: forest_fires (2026-10-21) and every
  same-run zero-inflated sibling.

**D3. Metric (MET-5, MET-3, MET-11; TP-6 as amended). Consistent.**

* **MET-5 holds.** TM-459 uses the lowest cross-validated RMSE of numerical abundance to pick, drop and weight its
  models (pp. 3, 20-23), and reports Spearman's rho, AUC and PDE only "in addition". That is one deliberate
  criterion, as in forest_fires (ranked by MAD, kept). The screening's fallback (AI, 2026-10-27, from the 2017 memo
  alone) is superseded by this later reading.
* **Concentration is no ground to overrule.** zillow_prize (2026-10-21) cited "0.38% of the rows hold 49.9% of the
  squared error" to move *to* the competition's metric. TP-6 as amended (Lennart 2026-10-21, on 17 definitions)
  overrules a source's metric only "when it is biased or wrong (evidence from the paper)". The Kendall tau of
  0.14-0.24 between raw and log1p RMSE compares against a metric the source never used, so it is not that evidence.
  numerai's tau argument also went towards the source's metric, not away from it.
* **Source or stand-in (builder issue 2).** The claim auditor's test T3
  gives Kendall tau 1.000 between RMSE on density and RMSE on counts (density x area swept) in all three windows. The
  declared metric therefore ranks models as the source's quantity would, and `source` holds under MET-11's identity
  clause (porto_seguro: Gini = 2 x AUC - 1).
* **The insurance siblings differ.** Their Gini suggestion (AI, 2026-10-30) rests on raw RMSE ranking every model
  near the mean. Here every probed model beats the training mean in every window (RMSE 1,300-1,652 against
  1,461-1,804), and the source has its own metric.
* **One note (MET-2).** The source scores each region and life stage separately, while we pool them. Tau against a
  Bering-only RMSE is 0.81, 0.81 and 0.62 (claim auditor). This is a note, not an issue.

**D4. Regime: temporal (SPLIT-1, SPLIT-3; tension "Temporal against grouped", Lennart 2026-10-12). Departs from the
sibling with a reason stated; the curator's pick is not recorded.**

* wadden_sea_sibes (same run) groups by station because its map covers "a surveyed year between stations".
  covertype (Lennart 2026-10-01) is IID for a cover map with no time axis. The source's own CV draws random stations,
  "a test of prediction skill at unsampled locations" (TM-459 p. 21).
* What sets this case apart is written in `splits_comment`: a review's maps stand for the five years until the next
  review (50 CFR 600.815(a)(10)), and the 2022 review "assessed the forecasting accuracy of the 2017 SDM approach"
  (TM-459 p. 3; Pirtle et al. 2020 not read). The split auditor adds that 15% of each window's test hauls are at new
  stations, so the spatial question stays in.
* Process: the screening (AI, 2026-10-27) wrote "grouped by station the alternative ... (SPLIT-3: one, the curator's
  pick)". Andrej's CC of 2026-10-30 records only `Yes`, priority 5, so the regime is still the AI's choice. One CC
  line would settle it.

**D5. Windows: three of five years (SPLIT-12, SPLIT-14, SPLIT-15). Consistent; no exception needed.**

* At equal strength the earlier rule wins (principles.md). SPLIT-12 sets the window to the source's review cycle, as
  in the house family (Lennart 2026-10-21: each task keeps its own source's horizon, "we dont need to force the same
  split").
* SPLIT-14 (Must) caps the count: a fourth window would train on 43.6% of the rows (split auditor). The three windows
  already use the whole test pool from 2012, which is what rain_in_australia's call (Lennart 2026-10-26, "follows
  SPLIT-15; no exception needed") was after.
* Builder issue 1 therefore changes no decision and can become a note. Its USE-3 temperature point is measured by
  the split auditor: R^2 0.652 with the temperatures, 0.651 without.
* crms_phragmites_cover (same run) takes nine one-year windows because no review cycle sets its horizon. The two are
  alike by rule.

**D6. Gap of two years (SPLIT-10). Consistent.**

* SPLIT-10 counts "a planning gap the use case has" as a gap. Here it is the source's own lag from the last survey
  to the review (TM-357 p. 5; TM-459 p. 3).
* It is an application, not an exception, so it adds nothing to the register's `amendment_due` flag on SPLIT-10
  (five exceptions so far).

**D7. Effort, gear and end position dropped (CLEAN-22, LEAK-10). Consistent by a written distinguishing fact.**

* The pair: fremtpl2 (Andrej 2026-10-20) kept `Exposure` as "a feature, not a divisor. The contracted period is known
  at pricing". The insurance calls of 2026-10-30 repeat this and add that "a target that is already a ratio to the
  insured value holds its exposure".
* What sets this case apart is written in the definition:
  * CPUE per km^2 swept is the source's own unit, and area swept is the target's denominator, which is CLEAN-22's
    "the measurement that defines the label";
  * the tow length is set during the tow, in response to the catch: walleye pollock tows under 0.4 h average 8.33
    against 7.35 log1p kg/km^2 for full-length tows. It is not known before the outcome (LEAK-10).
* wadden_sea (same run) drops its core area the same way.
* Two wording points:
  1. `task_summary.changes` gives "which the habitat models do not use" as the reason, but CLEAN-22 lets a column
     leave only for what it is. The denominator and the leak are the reasons to name there.
  2. The leak was measured on pollock, not rex sole. That is enough, since the tow length is a property of the haul,
     but the notes could say so.

**D8. Vessel and time of day dropped (USE-3, USE-6, CLEAN-22). Not reasonable as written; consistent under USE-3.**

* Builder issue 4 calls this a departure from USE-6. USE-6 is a Must, and a Must has no exceptions: only a
  higher-ranked Must overrides it (principles.md). None is named here.
* Read under USE-3, the drop matches the precedents. The use case predicts for a place and year without a haul,
  where no vessel or tow hour exists:
  * wadden_sea (same run) drops platform, sampling type and core area because "an unsampled place has no visit
    (USE-3)";
  * 2_month_survival_rate_prediction (Lennart 2026-10-26, a USE-6 case) leaves out inputs known at the prediction
    point when the source's task is defined without them.
* The definition's own reasons are neither a CLEAN-22 reason nor decisive: "sampling details the habitat models do
  not use", and R^2 0.643 and 0.646 against 0.652.
* One point about the definition's own logic: the measured temperatures also exist only where a haul was made. They
  stay because the source trains on them (Laman 2017, p. 5). wadden_sea keeps station-measured sediment on the same
  reading and puts the measured gap in `fit_reason`. The split auditor has measured this gap here (R^2 0.652 with the
  temperatures, 0.651 without), but the definition does not report it.

**Consistency check (AI, 2026-11-01):** the draft drops `vessel_id`, `vessel_name` and the time of day and calls it a
departure from USE-6 (Must: anything known at the prediction point is an input), which allows no exceptions.
brazilian_ecommerce (2026-10-15) and bias_correction_r_bias_correction_r_2 kept inputs known at the prediction point.
What sets this case apart?
(a) The prediction is for the map cell of an EFH review, a place and year without a haul, where no vessel or tow hour
exists. That is a USE-3 drop: word it as wadden_sea_sibes_macoma_abundance does, following
2_month_survival_rate_prediction (Lennart 2026-10-26), and drop the R^2 numbers as the reason.
(b) Treat it like brazilian_ecommerce: the row is a haul, its vessel and hour are known, and they carry no leak, so
keep both.
(c) Reopen wadden_sea_sibes_macoma_abundance's sampling-detail drop to match (b).
(d) Amend USE-6: inputs outside the source's task definition may leave.

**D9. Performance code dropped, its hauls kept (LEAK-10). Consistent.**

* The code is recorded after the tow and is about the tow, which is LEAK-10's "a column recorded after the outcome".
* The 2,659 positive-code hauls stay, as the survey keeps them (performance >= 0 counts as satisfactory).
* The register has no closer case.

**D10. `stratum` across the 2025 GOA redesign (CLEAN-21, Should; CLEAN-22, Must; SPLIT-20). Departs from the
precedents; the stated reason is contested.**

* CLEAN-22 keeps a column for what it is. Keeping `stratum` is therefore consistent in itself, and dropping it
  because it scores badly on one window would be the kind of choice SPLIT-21 bars for windows.
* The problem is that the column changes its coding at a date: from 2025 the GOA hauls carry 23 numbers from a new
  design. The closest precedents measured such a change and left one coding per column:
  * college_scorecard (CLEAN-21, Lennart 2026-10-16) put the redesigned SAT back on one scale with the measuring
    body's concordance, and "a section without a conversion table stays dropped";
  * zillow_prize (CLEAN-21 exception, Lennart 2026-10-26) mapped the 2017 `buildingqualitytypeid` onto the 2016 scale
    with the map the data shows.
* The stated reason ("a model fit at a review meets the redesign too") is contested by the split auditor:
  * no stratum appears among the source's covariates (TM-459 Table 3);
  * on GOA 2025, R^2 is -0.64 with `stratum` and 0.48 without, and these hauls hold 39% of the window's squared
    error.
* Untested: whether AFSC publishes the pre-2025 GOA hauls under the new strata, or the old strata's polygons for a
  spatial join. The answer decides between the two branches of (b) below.
* If (a) is chosen, it would be the second exception to CLEAN-21, after zillow_prize. Its reason differs (zillow
  converted, this case would not), so it does not count towards an amendment.

**Consistency check (AI, 2026-11-01):** the draft keeps both GOA survey designs, the old one and the 2025 one, in
`stratum`. college_scorecard (2026-10-16, Lennart: the redesigned SAT put back on one scale, a section without a
conversion dropped) and zillow_prize (2026-10-26, Lennart: the 2017 quality codes mapped onto the 2016 scale) both
left one coding per column. What sets this case apart?
(a) A model fit at a review meets the redesigned strata too, so unseen levels are part of the task. Record an
exception to CLEAN-21 that serves SPLIT-1; note that the split auditor contests it, since the source's models use no
stratum.
(b) Treat it like college_scorecard: put the 2025 GOA hauls on the old design if AFSC publishes the mapping or the old
polygons; otherwise drop `stratum`, or set the post-2025 GOA design to missing.
(c) Reopen college_scorecard and zillow_prize to match (a).
(d) Amend CLEAN-21 to cover category codes that a survey redesign replaces.

**D11. Identifiers dropped (CLEAN-3, CLEAN-5, CLEAN-14). Consistent.**

* zillow_prize (Lennart 2026-10-26) kept the census tract as a category and dropped the block group and block as
  near-identifiers. Here the coarse code `stratum` stays and the fine code `station` goes (GOA and Aleutian stations
  are mostly sampled once or twice).
* If `stratum` leaves (D10), only `srvy` and the coordinates carry the place.

**D12. `longitude_east` (0-360; CLEAN-21, CLEAN-2). Consistent with the rules.**

* The register has no precedent. This re-expresses one coordinate so it does not jump at the antimeridian; it is not
  a scaling or a built feature.
* The R^2 gain is support for the change, not its reason.

**D13. 12 catches weighed but not counted (CLEAN-15, Must). Consistent.**

* Same rule as qsar_tid_11 (Lennart 2026-10-21).
* All 12 are positive catches, but the drop rests on a missing field (the LEAK-25 reading wadden_sea cites), and 12
  of 13,557 is negligible.

**D14. Other species' catch not shipped (LEAK-10, USE-3). Consistent.**

* Same as the same-run siblings: cape_floristic drops Restionaceae, recorded in the same survey; wadden_sea leaves
  out the other taxa of the core.
* The source's use of concurrent coral and sponge presence (Laman 2017 p. 14) is named in the notes.

**D15. Year 2026 (PROV-9, Must). Consistent.**

* A growing source takes the year of the pinned snapshot: rain_in_australia (Lennart 2026-10-26, "the year is the
  definition's 2026"); wadden_sea pins 2024 (same run).
* The record's screening still says "`year` stays empty", written before the snapshot was pinned. The record update
  (builder issue 5) should add the year.

**D16. Fit approximate (USE-8). Consistent with wadden_sea.**

**D17. Warning `task_target_value_dominant` accepted (definitions.md warning table: name the zero inflation).
Consistent.**

* The task_probes pattern for a zero-inflated target (forest_fires) asks for the oracle bound and the two hurdle
  stages. The stages are reported (AUC 0.94-0.96; R^2 0.30-0.38 among catches); the oracle bound is not.
* Every same-run sibling reports the oracle bound (wadden_sea: R^2 0.04 raw, 0.93 log1p; frempl; spanish_2022; pg17).
  It is one number to add. This is a pattern, not a rule.

**D18. Missing temperatures stay missing (CLEAN-2). Consistent.**

**Drift, amendments, register flags**

* **Drift.** Andrej's decisions on the rules this dataset touches are fremtpl2 (2026-10-20), the eight policy calls
  (2026-10-30) and this record's CC (2026-10-30). I see no drift: the fremtpl2 exposure call and the per-area target
  agree once the timing of the effort (D7) is counted.
* **Third exception.** None proposed. This definition adds no exception to SPLIT-10 or CLEAN-19, the two rules with
  an `amendment_due` flag.
* **Register flags.** None of the 14 flags names this dataset or its same-run siblings.

**The builder's draft issues, against the precedents**

1. SPLIT-12 against SPLIT-15: settled by rule order and SPLIT-14 (D5). It becomes a note, not an issue.
2. Metric: `source` holds (tau 1.000 between density and count RMSE), and concentration is no evidence against the
   source's metric (TP-6 as amended, zillow_prize) (D3). It becomes a note; the pooled regions are an aside.
3. Species: the curator's pick, with Andrej's 2026-10-30 line on zero inflation beside it (D1).
4. `stratum`: a consistency check (D10). Vessel and hour: reframe as USE-3, or settle with the check (D8).
5. Record: also add `year` 2026 (D15).

</details>

<details><summary>Advocate</summary>

**Advocate, opening brief: noaa_afsc_bottom_trawl_survey_cpue (2026-11-01)**

```text
Verdict: ship. The rows, target, split, metric and feature set stand; one column recoding, the rest wording.
Validity: USE-1, USE-8 hold (approximate, gaps named); LEAK-10 holds for all 8 features; USE-3 met once the
  prediction point is worded as the source's skill test; SPLIT-1, -10, -12, -14, -21 hold; PROV holds (rebuilt exactly).
Value: MET-5 and MET-11 hold (source RMSE; density and count rank alike, tau 1.0); TP probes no flag.
Quality: CLEAN-21, `stratum` of the 2025 GOA design put on the pre-2025 coding; CLEAN-8 and CLEAN-22 wording.
For the curator: a CC line confirming temporal (SPLIT-3); the vessel and hour consistency check (option a).
```

**1. A real use case on the source's own data, reproduced exactly (P3, P5; USE-1, USE-8, PROV, all Must).**
- Evidence: the actor, moment and decision are written in law and in the source: EFH reviewed "at least every 5
  years" (50 CFR 600.815(a)(10), TM-459 p. 2), maps from SDMs fit to these hauls, models chosen by RMSE (TM-459 p. 21).
  The domain practitioner calls the use case "real and strong (P3)" and agrees with `fit="approximate"`. The blind
  reviewer rebuilt all 35,549 targets from the public API with a maximum absolute difference of 0.0. Our hauls match
  the review's counts (EBS shelf and NBS 1982-2019: 14,517 against 14,514 in TM-459 p. 6; slope 1,136 against 1,136).
  The zero fill is the source's recipe (gap_products sec. 10.2), and CATCH has no row with weight 0. EBS presence holds
  at 19.7 / 17.0 / 20.3 / 20.6% across four periods, so the early zeros are absences, not gaps in identification.
- Against "only a stand-in": USE-8 lets an approximate fit ship when its gaps are named. `fit_reason` already names
  all three the practitioner lists (habitat rasters, per-region and per-life-stage models, raster cells).

**2. No leak. The temperature objection is fixed in the wording, not by dropping columns (P4; LEAK-10, LEAK-6, USE-3,
all Must).**
- Evidence: the column auditor finds LEAK-10 holds for all 8 features, the missing temperatures do not track the
  catch, and exact copies across the split are 0%. Effort, gear, end position and the performance code leave as
  LEAK-10 drops. One example: EBS pollock tows under 0.4 h average 8.33 against 7.35 log1p kg/km^2.
- The claim auditor's Must finding is real as written: a review cannot know a future haul's own temperatures. But
  LEAK-6 says measure before acting, and the measurement shows no gain. Without both temperatures, LightGBM RMSE is
  1,461 / 1,642 / 1,286 against 1,472 / 1,652 / 1,315 shipped. The random forest gets better without them too. Run the
  source's own way (train on measured values, test on a climatology), R^2 is 0.595 / 0.721 / 0.647 against
  0.598 / 0.722 / 0.635 shipped.
- Fix: the claim auditor's option (b), which the domain practitioner also asks for. Word the prediction point as the
  source's skill test: abundance at a haul, given the habitat measured there. Both parts are in the source:
  - TM-459 p. 9 trains and skill-tests on haul temperatures;
  - Barnes, Essington, Pirtle et al. 2022 (the AFSC habitat team, EBS trawl data) forecast later years with
    "year-specific" bottom temperatures paired to the tow locations (dynamic SDMs, pp. 3-4).
  Under that point the values exist, so USE-3 holds with no exception. On the remedy ladder this is a fix to the
  definition, worded, before any drop.
- Surface temperature stays. CLEAN-22 (Must) lets a column leave only for what it is, and "no source trawl model uses
  it" is not one of its reasons. The column auditor makes the same argument against the vessel drop.
- The vessel and hour drop stays, reworded under USE-3 and USE-5. It is the precedent checker's option (a), as in
  wadden_sea_sibes. The actor acts on abundance at a place (USE-5), the temperatures describe that habitat, and the
  vessel and hour describe the sampling event, which no map cell has. The cost is nil either way (R^2 0.643 and 0.646
  with them, 0.652 without).

**3. The split mirrors the review cycle, and every Must of P4 holds (SPLIT-1, SPLIT-10, SPLIT-12, SPLIT-14, SPLIT-21).**
- Evidence: the split auditor finds the split "right with notes":
  - window = the five-year cycle (SPLIT-12);
  - gap = the sourced lag from the last survey to the review (surveys to 2014 for 2017, TM-357 p. 5; to 2019 for
    2022, TM-459 p. 3), a planning gap under SPLIT-10;
  - a fourth window would train on 43.6%, so SPLIT-14 forces three;
  - the windows were set from the cycle, not from scores (SPLIT-21).
- Against "the source used random CV" (claim auditor, row 21): SPLIT-5 (Must) treats a prescribed split as a claim to
  check. Random CV scores 0.732 R^2 against 0.652 on the windows, so it is optimistic. The source itself checks
  forward: TM-459 p. 3 "assessed the forecasting accuracy of the 2017 SDM approach", and Barnes et al. 2022 recommend
  retrospective skill testing. The practitioner calls the windows "arguably closer to the use than the source's random
  CV". The spatial question is still tested: 15% of each window's hauls are at stations unseen in training (SPLIT-13).
  What sets this case apart from wadden_sea_sibes (grouped) is that each map stands for five future years.
- Concede two items. `fit_reason` should say the split follows the review cycle and the next review's forecast check,
  not the review's CV. The regime needs the curator's CC line (SPLIT-3; the curator decides). Neither changes the
  definition's splits.

**4. The metric is the source's one deliberate criterion and ranks models as the source's quantity would (P6; MET-5
Should, MET-11 Must, TP-6 Must).**
- Evidence: TM-459 p. 21, "the model with the lowest RMSE was considered to be the best performer", with ensemble
  weights of RMSE^-2. That is one deliberate choice (MET-5). RMSE on density and RMSE on counts (density x area swept)
  rank the seven probe models at Kendall tau 1.000 in all three windows, so `source` holds under MET-11's identity
  clause. Every probed model beats the training mean (RMSE 1,300-1,652 against 1,461-1,804).
- Against "pooled over regions, GOA holds 71-92% of the squared error" (MET-2; claim auditor, domain practitioner):
  - TP-6 as amended overrules a source's metric only when it is biased or wrong by the paper's own evidence;
  - concentration is not such evidence: zillow_prize kept a metric where 0.38% of the rows hold 49.9% of the squared
    error;
  - pooled RMSE and Bering-only RMSE rank the models at tau 0.62-0.81, so the meaning largely survives;
  - a region-averaged RMSE would be a custom metric, which MET-12 and MET-13 ship only when other definitions use it.
- Mildest remedy: a Note bullet with GOA's share and the Bering tau, next to the existing "10-31 test hauls" sentence.

**5. The `stratum` break is real. The fix keeps the column and the dataset (P7; CLEAN-21 Should, CLEAN-22 Must).**
- Concede: the stated reason, "a model fit at a review meets the redesign too", does not hold, because no stratum is
  among the source's covariates (TM-459 Table 3). The 431 GOA hauls of 2025 (10.2% of the newest window) carry codes
  no training row has. On them LightGBM scores R^2 -0.64 to -0.82, and they hold 39% of the window's squared error.
- Fix: put the 2025 GOA hauls on the pre-2025 coding (college_scorecard, zillow_prize). Use GAP's pre-2025 polygons
  if they are published, which is a repair from the origin. Otherwise use each haul's nearest pre-2025 haul (median
  2.2 km), which is zillow's "map the data shows". The column auditor measures window R^2 0.577 -> 0.726 and GOA-2025
  -0.82 -> 0.51.
- Why not drop the column: mapping scores better than dropping (0.726 against 0.717). `stratum` carries signal before
  2025 (dropping it costs 0.003 and 0.010 R^2 on the older windows). CLEAN-22 does not list "it breaks in one window"
  as a reason to drop. Principles step 3: a P7 problem is fixed when the fix is cheap and safe, and this one is.

**6. Rex sole is a sourced, documented choice. The blind reviewer's "species not documented" is a clean-room artefact
(P3; USE-5 Must, CLEAN-8 Must).**
- Evidence: `task_summary` names rex sole in `question`, `row` and `predicted` (16 mentions in the README). The
  clean-room `task.md` carries no task_summary. The reasons stand without zero inflation, which Andrej's policy call
  of 2026-10-30 rules out as a criterion:
  - both reviews model the species (TM-357 pp. 48-49; TM-459 pp. 150-152; TM-458 pp. 131-132);
  - every catch from 1982 to 2025 is rated high confidence (13,331);
  - it has zeros inside every region but NBS.
- Concede three wording fixes:
  - CLEAN-8: one sentence saying the species was screened on the whole table, test years included, a pipeline
    choice that approximates the task;
  - "since 1982" becomes "1982-2025; the 226 catches of 2026 are not yet rated";
  - a note that the 2026 season is provisional. The counts match a full season (EBS 350 of 350), so the remedy is to
    compare against a later download and end the newest window at 2025 only if the counts move.

**7. Worth benchmarking: large, scorable, not trivial (P6; TP rules; P4 over P6).**
- Evidence: 35,549 rows. Each window has 3,953-4,806 test hauls, of which 1,537-1,863 caught rex sole. The leak and
  task probes raise no flag (RF skill +0.694). In RMSE on log1p, the global mean scores 2.94-3.42, the stratum mean
  2.10-2.25 and LightGBM 1.50-1.63. The blind reviewer: "real signal and the task is not trivial". Within-region
  Spearman rho is 0.58-0.80, "excellent" on TM-459's rubric.
- Against "mostly spatial memory" (k-NN on position comes close to LightGBM): the maps cover the surveyed waters, so
  recurring stations are part of the task (SPLIT-13). The right split wins over the score (P4 over P6; forest_fires),
  and a strong simple baseline is not triviality while it stays well above the weak ones.

Changes I accept, all of which keep the dataset: the GOA-2025 stratum recoding (point 5), plus wording in `known`,
`split`, `fit_reason`, the species, vessel and gear bullets, the metric note and the 2026 caveat. One optional note:
the 1993-95 depths are headrope depths (column auditor, problem 5).

</details>

<details><summary>Critic</summary>

**Critic: noaa_afsc_bottom_trawl_survey_cpue, opening brief (2026-11-01)**

**Verdict: ship only after changes.** The use case is real: the EFH review is set by law (50 CFR 600.815(a)(10)), and
our hauls match the review's (14,517 against 14,514 Bering hauls, claim auditor row 30). Nothing below calls for
exclusion. But three things are wrong as defined. The definition states a prediction point that its inputs contradict.
It keeps a column whose coding breaks in the newest window. Its pooled metric is mostly a Gulf of Alaska score. Each
can be fixed in the definition.

**1. The definition mixes two prediction points (P3/P4; USE-3, LEAK-10, USE-6, all Must).**
- Problem: `known`, `split` and the first note put the prediction point at a review that predicts the next five years
  of surveys. At that point a future haul's bottom and surface temperatures do not exist. The source maps from
  "Rasterized 38-year averages of habitat covariates" (TM-459 p. 8; TM-357 p. 12). The temperatures stay anyway. The
  vessel and the hour leave, on the map reading that a cell has no visit. The builder calls that drop "a departure
  from USE-6", but USE-6 is a Must and allows no exceptions (precedent checker D8).
- Effect: the text says "forecast", while the inputs describe the habitat at a measured haul. The scores do not move.
  Without both temperatures, LightGBM RMSE is 1,461 / 1,642 / 1,286 against 1,472 / 1,652 / 1,315 shipped, and the
  random forest 1,403 / 1,565 / 1,266 against 1,420 / 1,599 / 1,302 (claim auditor row 19). A
  training-years climatology changes R^2 by -0.004 to +0.012 (column auditor problem 1); mean R^2 is 0.652 with the
  temperatures and 0.651 without (split auditor). So the defect is in the definition, not in the scores, and the fix is
  cheap.
- Remedy (fix the definition by choosing one reading):
  - (a) The review's map. Drop `bottom_temperature_c` and `surface_temperature_c` as unknown at the prediction point
    (a CLEAN-22 reason: a leak, LEAK-10). The vessel and the hour stay out under USE-3. No measured cost.
  - (b) The next review's skill test at measured conditions (TM-459 pp. 8-9; Barnes et al. 2022). Rewrite `known`,
    `split`, `fit_reason` and the first note. Then the vessel and the hour are known at the haul too: bring them back
    (USE-6, as in brazilian_ecommerce), or the curator amends USE-6.
- I ask for (a). It is the actor's decision (the map), and it is the only reading under which the current drops
  already hold.

**2. The regime is not the curator's pick, and `fit_reason` misstates the split (P4; SPLIT-1, SPLIT-3, USE-8, Must).**
- Problem: under SPLIT-1 the curator picks the regime. The screening left it open ("grouped by station the
  alternative ... (SPLIT-3: one, the curator's pick)"), and the only CC line is `Yes`, priority 5. `fit_reason` says
  "the rows, target and split follow the review's models". The review skill-tested by random 10-fold CV, "a test of
  prediction skill at unsampled locations" (TM-459 pp. 20-21). The same-run sibling wadden_sea_sibes took grouped by
  station for its map.
- Effect: the three regimes give different scores. Mean R^2 is 0.652 temporal, 0.687 grouped by station and 0.732 IID
  (split auditor). In each window, 85% of the test hauls sit at a station seen in training (EBS 100%), and 95-98% lie
  within 5 km of a training haul (claim auditor row 21). The windows test later years at known places, not unsampled
  ones.
- The case for temporal holds and I do not contest it: the five-year cycle, the 2017 model's forecast check (TM-459
  p. 3), and the retrospective forecasts of Barnes et al. 2022.
- Remedy:
  - a CC line that records temporal;
  - `fit_reason` reworded to "the split follows the review cycle and the next review's forecast check, not the
    source's random CV";
  - `splits_comment` adds the 85% seen-station share and the 43.6% a fourth window would train on, and cites Barnes et
    al. 2022 (read by the domain practitioner, NOAA copy) beside the unread Pirtle 2020.

**3. `stratum` holds two GOA designs, and the newest window scores unseen codes (P4, SPLIT-20, Should; P7, CLEAN-21,
Should).**
- Problem: GOA was restratified for 2025. Its 23 new stratum numbers share none with the 59 of 1990-2023, so all 431
  GOA hauls of 2025 (10.2% of split 0) carry a code no training row has. The stated reason to keep the column is "a
  model fit at a review meets the redesign too". It does not hold: the source's models have no stratum covariate
  (TM-459 Table 3; split and column auditors).
- Effect: split 0 is the most representative window (SPLIT-11). On the GOA-2025 hauls, untuned LightGBM scores R^2
  -0.64 to -0.82 and predicts a mean of 1.2-1.5 against 4.42 observed. Those hauls hold 39% of the window's squared
  error. Window R^2 by variant:

  | variant | window R^2 |
  |---|---|
  | shipped | 0.598 |
  | without `stratum` | 0.719 |
  | the 2025 hauls mapped to their nearest earlier haul's stratum | 0.726 |
  | random forest on the codes, shipped | 0.735 |
  | random forest on the codes, without `stratum` | 0.742 |

  The random forest is barely hurt, so the window partly ranks models by how they treat unseen categories. The blind
  reviewer found this on its own (concern 1). Setting the 2025 codes to missing does not help (-0.816, unchanged;
  column auditor).
- Rule: departing from a Should needs a fact that sets the case apart, and the stated fact does not hold. Precedents:
  college_scorecard (CLEAN-21: put back on one scale with the published concordance; "a section without a conversion
  table stays dropped") and zillow_prize (2017 codes mapped onto the 2016 scale from the data).
- Remedy, repair first:
  - map the 2025 GOA hauls onto the pre-2025 strata, with GAP's polygons or else each haul's nearest pre-2025 haul, as
    zillow_prize did;
  - only if no mapping can be built, drop `stratum` (college_scorecard), for its broken coding, not for its score;
  - not the reverse: the 2025 design was built on survey densities that overlap the test windows (column auditor).

**4. The newest season is not finished, and the notes say it is (P5; EV-7, Must; LEAK-24's two-download check, Must,
by analogy).**
- Problem: "identified with high confidence in every catch since 1982" is false for 2026. All 226 rex sole catches of
  2026 have a null `taxon_confidence`; none of the 205 catches of 2024 or the 377 of 2025 does (claim auditor row 4,
  column auditor problem 2).
- Effect: the 722 hauls of 2026 are 17% of split 0. EBS presence in 2026 is 0.169, against 0.209-0.293 in 2018-2025.
  That is suggestive, not shown to be an artefact. The species was chosen partly on its identification record.
- Remedy:
  - reword to "1982-2025; the 2026 catches are not yet rated", and add a note that the newest season is provisional;
  - before `build`, compare with a download made after GAP rates 2026;
  - if the 2026 counts move, rebuild from that settled download, or end the newest window at 2025.

**5. The pooled RMSE is mostly a Gulf of Alaska score (P6; MET-2 and MET-1, Must).**
- Problem: the source scores each region and life stage separately, and the reference memo (TM-459) is the Bering Sea
  memo. We pool five regions under one RMSE on density. MET-2: a changed task keeps the source's metric "only when its
  meaning survives the change".
- Effect: GOA hauls are 23-40% of the test hauls but hold 71-92% of the squared error. GOA's mean density is 1,060 per
  km^2, against 85 on the EBS shelf, and EBS hauls hold 0.4-13% of the error. The pooled RMSE and a Bering-only RMSE
  rank the probe models with Kendall tau 0.62-0.81 (claim auditor) or 0.2-1.0 (domain practitioner, five models). A
  Bering Sea analyst cannot read the score as Bering skill.
- Remedy:
  - at least, a note in `metric.definition` and in the notes that gives these shares;
  - the curator weighs a region-averaged RMSE with `srvy` as a scoring column (the domain practitioner's choice; a
    custom metric under MET-12 and MET-13);
  - I do not ask to drop `rmse`. It is the source's selection rule (MET-5 holds, TM-459 p. 21), and density ranks the
    models as counts do (tau 1.0).

**6. The species was picked on the whole table, test windows included, and partly by a criterion the curator set
aside (P7; CLEAN-8, Must, a note).**
- Problem: rex sole was chosen from 22 species by prevalence over 1982-2026 (the builder's species screen) and by
  hurdle scores on the three shipped test windows (the builder's hurdle probe). In a temporal task, CLEAN-8 asks the
  notes to call such a choice a pipeline choice that approximates the task. Part of the stated reason is the zero
  structure: cod is rejected for its "4% on the EBS shelf". Andrej's call of 2026-10-30 (policy question 2) makes zero
  inflation no criterion. The note says "its zeros are not one region's", yet NBS has 0% presence over 969 hauls. That
  is the same whole-region absence the note holds against sablefish (claim auditor row 5).
- Effect: small. A reader cannot see that the species choice saw the test years.
- Remedy: one sentence for each point in the species bullet. The curator confirms the species (builder issue 3) on the
  reasons that stand without zero inflation: the identification history, and a managed species modelled in both
  reviews.

**7. Drop reasons and claims that the evidence contradicts (P7 and writing; CLEAN-22, Must, on reasons; EV-2, EV-7).**
- Effort, gear, vessel and hour leave because "the habitat models do not use" them (`task_summary.changes`, two notes).
  That is not a CLEAN-22 reason. The valid reasons: for gear and effort, the label's denominator and a tow length that
  responds to the catch (LEAK-10); for vessel and hour, point 1. The reason is also applied unevenly: `stratum`, `date`
  and `surface_temperature_c` are not model covariates either, and they stay (column auditor problem 4).
- "The covariates the source trains on" is wrong in part. Surface temperature is a covariate of the ichthyoplankton
  models only (TM-357 Fig. 3), and stratum and date are covariates in neither memo (claim auditor row 18).
- The Kendall tau of 0.14-0.24 (raw against log1p RMSE) gives 0.14-0.33 on reruns; one swap among seven models moves
  it by 0.095 (row 28).
- `depth_m` for 1993-95 is headrope depth, a median 1.25 m shallower at the EBS stations (TM-459 p. 8). It needs a
  note (CLEAN-21).
- Two record lines are wrong:
  - "GOA and AI stations are mostly sampled once or twice": the AI median is 7 hauls per station id (row 32);
  - "`year` stays empty": the definition pins 2026 (PROV-9).
- Remedy: reword. The frame does not change.

**Judgment record**

```text
Verdict: ship after changes.
Validity: USE-3 / LEAK-10 / USE-6 triggered (two prediction points); fix the definition (drop both temperatures, or
  rewrite as the skill test and follow USE-6 for the vessel and the hour). SPLIT-1 / SPLIT-3: the curator's CC is
  missing; USE-8: `fit_reason`'s split claim refuted, reword. SPLIT-20 / CLEAN-21: `stratum` departs without a reason
  that holds; repair by mapping the 2025 GOA hauls, else drop. P5: 2026 not yet rated; reword, two-download check
  before build.
Value: MET-5 holds; MET-2, pooled regions: a note at least, a region-averaged RMSE for the curator.
Quality: CLEAN-8 note on the species; CLEAN-22 reasons reworded; wording fixes.
Exclusion: not asked; every point has a fix in the definition or a note.
```

</details>

<details><summary>Advocate rebuttal</summary>

**Advocate, rebuttal: noaa_afsc_bottom_trawl_survey_cpue (2026-11-01)**

The critic and I agree on the verdict ("ship after changes", no exclusion) and on five of the seven remedies. We
still differ on two points: which prediction point the definition should state (critic 1), and whether the curator
should be offered a custom metric (critic 5).

**Critic 1, two prediction points: concede the defect, dispute the remedy. Option (b), not (a).**
- Conceded: as written, `known` and `split` describe a review forecasting the next five years, while the inputs are a
  measured haul's. One reading has to be chosen (USE-3, Must). Calling the vessel and hour drop "a departure from
  USE-6" is wrong, because a Must has no exceptions.
- Disputed: (a) is the wrong reading to choose, for two reasons.
  - The task does not score the map. The row is a haul and the metric is RMSE at the stations, which is the step
    where the source selects and weights its models (TM-459 pp. 20-21, MET-1). The domain practitioner says the task
    "reproduces the model-selection step at hauls, not the map", and `fit_reason` already names the map as a gap
    (USE-8). Putting the prediction point at the map would leave the stated point and the scored unit disagreeing.
  - Under (b) the measured values are exactly what the source scores at. The review trains and skill-tests on haul
    temperatures (TM-459 p. 9). The next review's forward check is the split, and in Barnes, Essington, Pirtle et al.
    2022 (the same team, EBS trawl hauls) the dynamic SDMs forecast later years with "year-specific" bottom
    temperatures paired to the tow locations (pp. 3-4).
- Under (b) the temperatures are no leak. CLEAN-22 (Must) then gives no reason to drop bottom temperature, which is a
  covariate of the source's model (TM-459 Table 3). Dropping it under (a) would remove the source's habitat driver to
  repair a wording problem. The measured cost is nil either way (RMSE 1,461 / 1,642 / 1,286 without, 1,472 / 1,652 /
  1,315 with), so the scores do not decide this. The rule order does: the mildest remedy is a fix to the definition's
  wording, before any drop (remedy ladder; LEAK-7, Should).
- The critic says (a) "is the only reading under which the current drops already hold". That is not so.
  - Under (b) the vessel and hour drop holds as USE-6 has been applied. 2_month_survival_rate_prediction (Lennart,
    2026-10-26) left out the physicians' estimates, known at the prediction point, because the source's task is
    defined without them.
  - Here the source's task is abundance as a function of habitat (Laman et al. 2017 p. 5: "habitat covariates ...
    collected in association with the catch"). The vessel and hour describe the sampling event, which the per-area
    target already standardizes, not the habitat (USE-5).
  - If the curator does not accept that reading, the fallback is the critic's own (b) branch: restore the vessel and
    hour (R^2 0.643 and 0.646 against 0.652). That still beats (a), because it keeps the source's covariate.

**Critic 2, regime and `fit_reason`: concede in full.** The fixes are a CC line recording temporal, `fit_reason`
reworded as the critic proposes, and in `splits_comment` the 85% seen-station share, the 43.6% a fourth window would
train on, and Barnes et al. 2022 beside the unread Pirtle 2020 (SPLIT-1, SPLIT-3, USE-8). The critic does not contest
temporal, so the splits stay.

**Critic 3, `stratum`: concede in full; same remedy as my point 5.** Map the 2025 GOA hauls onto the pre-2025
strata, with GAP's polygons or else the nearest pre-2025 haul (window R^2 0.726). Drop the column only if no mapping
can be built. Never map in the reverse direction (CLEAN-21; college_scorecard, zillow_prize).

**Critic 4, the 2026 season: concede the wording and the check; one limit on the remedy.**
- Agreed: reword to "1982-2025; the 2026 catches are not yet rated", add a note that the newest season is provisional,
  and compare with a later download before `build` (EV-7).
- The limit: a null `taxon_confidence` is a missing rating, not missing catches. The 2026 hauls look complete (EBS 350
  of 350; Aleutians 372 hauls to 2026-08-04, split auditor). So the newest window should be ended at 2025 only if a
  settled download actually changes the 2026 counts. A presence of 0.169 against 0.209-0.293 is not that evidence,
  and cutting windows on such comparisons is what SPLIT-21 bars.

**Critic 5, pooled RMSE: concede the note, dispute offering the custom metric.**
- Agreed: `metric.definition` and the notes should give GOA's 23-40% of the test hauls against its 71-92% of the
  squared error, and the Bering-only rank agreement (MET-2).
- Disputed: the region-averaged RMSE.
  - The meaning survives the pooling: the same target, unit and formula as TM-459's selection rule. Pooled and
    Bering-only RMSE rank seven models at tau 0.81 / 0.81 / 0.62. The practitioner's 0.2 comes from five models,
    where one swap moves tau by 0.2 (EV-8).
  - TP-6 as amended overrules a source's metric only when the paper shows it biased or wrong. Concentration is not
    that evidence (zillow_prize kept a metric where 0.38% of the rows hold 49.9% of the squared error).
  - A region average would weigh different regions in each window, which is an untested side effect. NBS hauls, all
    zero, sit in two windows, and the slope survey in one (split auditor note 4). The NBS term would be a near-free
    quarter of the score in those windows.
  - MET-12 and MET-13 ship a custom metric only when other definitions use it.
- If the curator weighs it anyway, it is a weighing call, not a fix this definition needs.

**Critic 6, the species: concede.**
- CLEAN-8 needs a sentence saying the species was screened on the whole table and the test windows, a pipeline
  choice that approximates the task.
- "Its zeros are not one region's" overstates the case: NBS is a whole-region absence (969 hauls, 2.7% of the rows).
  The species bullet should say zeros fall inside four of the five regions and NBS is absent.
- The curator confirms the species on the reasons that stand without zero inflation: a high-confidence
  identification history and a managed species modelled in both reviews (Andrej, 2026-10-30, policy 2).

**Critic 7, drop reasons and claims: concede, and it supports my point 2.** "The habitat models do not use it" goes
everywhere. Each column then stands or leaves for what it is (CLEAN-22):
- gear and effort leave as the label's denominator and a tow length that responds to the catch (LEAK-10);
- vessel and hour follow critic 1;
- surface temperature, `stratum` and `date` stay as inputs known at the haul.
The covariate sentence, the tau range (0.14-0.33 over reruns), the depth note for 1993-95 and the two record lines
are wording fixes. The frame does not change.

```text
Agreed with the critic: ship after changes. Stratum mapping (the one frame change); CC line for temporal; fit_reason,
  splits_comment, species, 2026 and drop-reason wording; metric note on GOA's share.
Still disputed, for the mediator: critic 1, (b) over (a): the scored unit is the source's skill test, and CLEAN-22
  keeps bottom temperature once it is no leak; vessel and hour per 2_month_survival (USE-6 as applied), else restored.
  Critic 5: no custom metric (TP-6, MET-12/13; it weighs regions unevenly across windows).
```

</details>

<details><summary>Critic rebuttal</summary>

**Critic: rebuttal to the advocate (2026-11-01)**

**Summary.** I concede advocate points 1, 3, 5, 6 and 7, and I drop my preference for dropping the temperatures. Two
points stay open, both about wording or a curator option and neither about a change to the frame:
- **Advocate 2:** the prediction point has to be named so that the temperatures stay and the vessel and hour leave
  under the same reading.
- **Advocate 4:** a region-averaged RMSE should stay on the table for the curator.

After this round, the changes both sides accept are:
- the GOA-2025 stratum recoding;
- a CC line confirming temporal;
- rewording of `known`, `split` and `fit_reason`;
- the CLEAN-8 sentence on the species;
- the 2026 caveat and the check against a second download;
- the CLEAN-22 reasons for the drops;
- the metric note;
- the note on the 1993-95 depths.

**Advocate 1 (real use case, data rebuilt exactly; USE-1, USE-8, PROV). Concede.** I never disputed it. The blind
reviewer rebuilt all 35,549 targets with zero difference, and the haul counts match TM-459 p. 6.

**Advocate 2 (no leak; the temperatures are fixed by wording; the vessel and hour stay dropped). Concede the substance,
dispute the wording.**
- **I concede that the temperatures stay.** The advocate's source holds up. Barnes et al. 2022 (pp. 3-4) fit dynamic SDMs to "year-specific BT", kriged from the BERING10K
  hindcast onto both the tow locations and "a uniform 1-km2 prediction grid", and test them by retrospective
  forecasts. So a year's bottom temperature exists for every place, not only where a haul was made. The measurement
  (LEAK-6) shows no gain from the haul's own values. My option (a) is not needed.
- **I dispute the wording "abundance at a haul, given the habitat measured there".**
  - At a haul, the vessel and the tow hour are known as well. Under that prediction point, USE-6 (Must, no exceptions)
    makes them legitimate inputs.
  - The advocate's own reason for dropping them is "the sampling event, which no map cell has". That is a reason about
    a place, not about a haul. Taken together, the advocate's temperatures follow the haul and its drops follow the
    map: the same two prediction points my point 1 objected to.
  - USE-3 (Must) asks for one named prediction point.
- **The wording that makes both choices hold:** abundance at a place in a given survey year, given that year's
  depth and bottom conditions there. The haul's measured temperatures stand in for the year-specific field of Barnes
  et al. 2022. Under that point:
  - the temperatures exist, so USE-3 and LEAK-10 hold;
  - the vessel and the hour are not attributes of a place-year, so they leave under USE-3 and USE-6 is not breached.
    This is the precedent checker's option (a), as in wadden_sea_sibes.
- **Apply the same wording to:**
  - `known`;
  - `split`, so that it reads as the next review's forecast check of later years under their own conditions, not "a
    model fit at a review predicts the surveys";
  - the first note, citing TM-459 p. 8 for the long-term-mean maps, the no-gain numbers, and Barnes et al.'s finding
    that year-specific temperatures "did not improve or decreased forecast skill".
- **Surface temperature.** I agree it stays (CLEAN-22). It is a year-specific condition under the same reading.

**Advocate 3 (the split). Concede.** The advocate concedes the `fit_reason` wording and the CC line, which were my
point 2. I ask only that `splits_comment` also give the 85% seen-station share and the 43.6% for a fourth window. The
advocate does not contest either.

**Advocate 4 (the metric). Agreed on the note; I dispute that the region-averaged option is closed.**
- **Agreed.** `rmse` stays. MET-5 holds (TM-459 p. 21), and MET-11 holds (tau 1.0 between density and count). The
  minimum is a note in `metric.definition` giving GOA's share of the squared error (71-92%) and the Bering-only tau.
- **The zillow_prize precedent does not apply.** There, the error was concentrated inside the competition's own task.
  Here we pooled five regions that the source scores separately. MET-2 (Must) keeps the source's metric on a changed
  task "only when its meaning survives the change". The evidence on that is mixed:
  - pooled RMSE and Bering-only RMSE rank the models with Kendall tau 0.62-0.81 (claim auditor) and 0.2 / 0.8 / 1.0
    (domain practitioner);
  - EBS hauls carry 0.4-13% of the error while making up 38-43% of the test hauls.
- **MET-13 does not bar the option.** It asks for a reference implementation in the shared library ("a metric only
  one definition holds is never shipped" means its code cannot live in one definition file). It does not require
  other users. A mean of per-group RMSE takes a general name under MET-12, as `mean_group_pearsonr` already does.
- **Where it stands.** This is a weighing call under MET-1 (the actor acts on one region's map) and goes to the
  curator with both sides' evidence. It does not block shipping.

**Advocate 5 (`stratum`). Concede.** We agree on the remedy: polygons where GAP publishes them, otherwise each haul's
nearest pre-2025 haul. The nearest-haul mapping can always be built, so my fallback (drop the column) never comes into
play. I withdraw it. The mapping beats dropping (0.726 against 0.717), and the column carries signal before 2025.

**Advocate 6 (rex sole, the 2026 season). Concede, with one point on timing.**
- The advocate accepts the CLEAN-8 sentence, the "1982-2025; the 2026 catches are not yet rated" wording, and the
  provisional-season note. That covers my points 4 and 6.
- I agree that the blind reviewer's "species not documented" comes from the clean room and is not a fault of the
  definition.
- Timing: LEAK-24 says "compare two downloads first". The comparison belongs before `build`, because the shipped
  container freezes the snapshot. If the 2026 counts move, rebuild from the rated download, or end the newest window
  at 2025.

**Advocate 7 (worth benchmarking). Concede.** I raised no value objection. Each window has 3,953-4,806 test hauls, and
LightGBM beats the stratum mean well. The spatial-memory concern is the blind reviewer's, not mine, and SPLIT-13
answers it.

```text
Rebuttal: conceded A1, A3, A5, A6, A7; withdrew the temperature drop (Barnes et al. 2022 year-specific BT on the full
  grid) and the stratum-drop fallback.
Disputed: A2 wording only. The prediction point is a place-year under that year's conditions, not "at a haul"
  (USE-3, USE-6 Must). A4: a region-averaged RMSE stays a curator option (MET-1, MET-2; MET-13 does not bar it).
Exclusion: not asked.
```

</details>
