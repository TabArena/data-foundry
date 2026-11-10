# noaa_afsc_bottom_trawl_survey_cpue

**Outcome:** added. The AI recommends shipping it: the re-review of 2026-11-06 under the exposure rules corrected the
notes and added one assert, with rows, target, features, split and metric unchanged, and left two questions that
change neither the data nor the score, both settled on 2026-11-08 (issue 5: a restated CC; issue 6: a rule file's
wording). The data are NOAA
AFSC's summer bottom-trawl hauls from the public FOSS tables: 35,561 hauls of 1982-2026 in five survey regions, one row
per haul and taxon for 11 groundfish taxa (391,044 rows, 52.0% zero catches). The target is the catch in numbers per
km^2 swept, shipped as log1p and scored after the inverse by `mean_group_normalized_rmse`, the source's RMSE taken per
taxon over the spread of its catches in the window and averaged, so that each species' habitat map counts once; the
score is unweighted, with no sample weight. The prediction is for a species at a place in a survey year, from the taxon,
the region, the design stratum, the position, the date, the depth and that year's temperatures there; `taxon_group`, a
copy of `taxon`, is the metric's group and no feature. The split is temporal: nine two-year windows (2025-2026 back to
2009-2010), each trained on every earlier survey, without a gap.

Validity:
* USE-3 holds: the realized effort (tow length, distance, net width and height, area swept, end position) is dropped,
  as a place in a survey year has no tow. USE-8: fit approximate (one table of 11 taxa scored at the hauls' own
  readings; no habitat layers such as sediment or currents).
* LEAK-41 holds as a leak rule: the shipped features carry the realized effort only through place and year (the
  realized area swept over its region-year median at R^2 0.10, short tows told apart at ROC AUC 0.75), the risk
  selection the rule allows. Its reporting clause was not met and is fixed in the notes: under a Poisson fit the effort
  columns gain +0.013 in the panel's rerun (better in 4 of 5 windows), not nothing, and the score of a model on 1/area
  swept is stated (a gain of 0.007-0.013 over the taxon alone, against the honest model's 0.90-0.93).
* LEAK-10 holds: no feature carries the tow cut. EV-1 triggered on the notes' cut claim, fixed in the text: against an
  area-only null Pacific cod's short tows stand above it too, and among the tows with a catch those of four more taxa;
  Lennart's CC of 2026-11-08 claims the cut for walleye pollock and, to a lesser degree, Pacific cod (issue 5).
* SPLIT-1, SPLIT-3, SPLIT-9, SPLIT-11, SPLIT-12, SPLIT-13, SPLIT-14 and SPLIT-23 hold: no haul straddles a cutoff, and
  the training sides hold 54.0-95.4% of the rows. SPLIT-20 is a note: pollock's cut sits mostly in the EBS hauls of
  1989-2008, training rows in every window, and in the test years shows in the Aleutians and the Gulf of Alaska;
  dropping the short tows from training moves the score by -0.0013, noise. EV-2 triggered on the splits text, which
  said every window holds every region; corrected (the slope survey ended in 2016, the northern Bering Sea runs in
  some years, and 2019 has no Aleutian survey).

Value: MET-2 holds: `taxon_group` equals `taxon` on all 391,044 rows, and the 11 taxa are scorable in 9 of 9 windows
with at least 71 positives each. MET-15 holds and decides "unweighted, no sample weight", as the decision is per cell
of an equal-area map; MET-16 holds, no design weight, as EFH is not a population estimate (a stratum-area design
weight ranks 7 untuned models alike, Kendall tau 0.81-1.00, the same winner in 4 of 4 windows). The stated reason,
"cells of equal area", misdescribed the scored hauls (the Aleutians have about 8 times the EBS shelf's hauls per
km^2) and is reworded. The task probe raises no flag (random forest skill +0.786 ± 0.012; on the metric 0.919 against
the dummy's 1.092). The time-on-risk row of the leak rules' cases records this dataset by a clause in its remedy
(issue 6, 2026-11-08).

Quality: MET-14 departure fixed: `_clean` asserts that the CPUE times the area swept rebuilds the count (201,731
counted catches, to 1.6e-4); the frame and the splits are unchanged. CLEAN-15 holds: the 128 catches weighed but not
counted are dropped, not zero-filled. EV-8 triggered on the Poisson range, corrected to 0.88-1.24 (two runs, five
windows each). The check warning `task_target_value_dominant` (52.0% zeros) is accepted with Andrej's reason of
2026-11-03.

Weighed: NOAA's documented tables +; a use case set by law +; an approximate fit -. None open (the mediator).

Settled on 2026-11-08 (Lennart): issue 5, the claim of the CC of 2026-11-06 restated by a new CC (B); issue 6, this
dataset's entry in the time-on-risk row of the leak rules' cases as a clause in the row's remedy (B). Across datasets, this dataset's evidence goes
to two items of the working copy's REVIEW.md ("From PR #47"), and no change here hangs on them: X2, rewording LEAK-41's
"ceiling" (under this level-sensitive metric the model on 1/area swept beside the taxon scores 1.031-1.046, worse than
the honest model's 0.90-0.93, while the free effort columns gain up to 0.033 in single windows, more than its
0.007-0.013); X3, MET-14's rebuild check only when the source releases the count (this dataset now asserts the rebuild
and leaves X3's list, so X3 rests on two cases, boreal_postfire_lichen_biomass and wadden_sea_sibes_macoma_abundance,
and no amendment is due).

The first panel (2026-11-01) reviewed the rex sole table with three five-year windows; its reports are in this file's
git history. Andrej's marks of 2026-11-02 made the table 11 taxa with the taxon as a feature (issue 1), the split nine
two-year windows without a gap (issue 2) and the metric the RMSE per taxon over its spread (issues 1 and 3); on
2026-11-06 issue 4 added the copy `taxon_group` and settled the tow's effort. The re-review of the same day (full
tier) made the nine changes that need no decision (Mediator, "Changes to make now"). One figure differs from the
panel's: Greenland turbot's spread, which the metric takes per test window, is 12-35 per km^2 from 2017 on against
162-543 before (the panel's 8-38 and 47-639 are per survey year). `dataset check`: 0 errors, 0 warnings.

**Main points:** Nothing is open. Settled on 2026-11-09 (Andrej): the two-year windows stay, their text reworded to
a refit after each two-year survey cycle (10), and the 2026 catches stay, with the build check (11). Settled: the 11
taxa (issue 1), the temporal split (2) and RMSE (3) on 2026-11-02; the copy
`taxon_group` and the dropped effort (4) on 2026-11-06; the cut claimed for walleye pollock and, to a lesser degree,
Pacific cod (5) and a clause in the remedy of the leak rules' time-on-risk row (6) on 2026-11-08. Across datasets: X2
and X3.

**Verdict (2026-11-09, Andrej):** ship (review page of 2026-11-09).

**Verdict (2026-11-02, Andrej):** ship. The metric is marked as declared (`mean_group_normalized_rmse`). The
dataset joins the accepted set; a build waits for your ask.

**Issues for Andrej and Lennart:**

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
     and `taxon` stays a model input. The notes now claim the cut where the data shows it; the re-review of 2026-11-06
     found it for Pacific cod too, to a lesser degree (issue 5).
   * **Experiments:** Short tows are those under 0.75 of the median duration of their region and year (1,699 of
     35,561 hauls); each is set against the mean of its stratum and year, on log1p numbers per km^2 (the new decision
     table of the README). The text below is corrected after the re-review of 2026-11-06 (the review panel below).
     - Over all hauls, pollock's short tows lie 0.36 above their cells, the other taxa -0.36 to +0.08. On the EBS
       shelf, pollock tows under 0.4 h (831) average 8.33 log1p kg per km^2 against 7.35 at full length. Against an
       area-only null (each short tow redrawn from a full tow of its cell, thinned by the ratio of the areas swept),
       pollock stands far above it (+0.357 against -0.070) and Pacific cod above it too (about 4 standard deviations of
       the null): a stop on a large catch is the likely reading, not isolated from where short tows land within a
       cell (issue 5).
     - Where a short tow catches a taxon, its density is higher for 9 of 11 taxa by the plain means and for all 11
       within their cells (pollock 0.55, the others 0.00 to 0.25). The smaller area swept explains this for
       Atheresthes, Dover sole, Greenland turbot, Hippoglossoides and rex sole, not for pollock, Pacific cod, Pacific
       halibut, sablefish, shortspine thornyhead or rock sole, which sit above the null.
     - As free features the effort columns gain 0.0028 of the metric under an L2 fit on log1p (1.9% of untuned
       LightGBM's skill, better in 3 of the 5 windows tested; 0.0004 in the panel's rerun) and, under a Poisson fit,
       -0.006 in the exposure study (better in 1 of 5 windows) and +0.013 in the panel's rerun (4 of 5), so about
       0.013 on the worse fit. A model on 1/area swept beside the taxon scores 1.031-1.046 against 1.039-1.057 for the
       taxon alone (the honest model 0.90-0.93). An RMSE on counts ranks the models as the density RMSE does (Kendall
       tau 0.80 to 1.00, the same winner in 5 of 5 windows; exposure study).
   * **Consistency:** The same copy as liberty_mutual_fire_peril_loss_cost's `var11_weight`, asked in the same review
     comment. The density is scored unweighted, as wadden_sea_sibes_macoma_abundance and
     boreal_postfire_lichen_biomass score theirs[^unweighted]; they match on an unweighted rate per unit area, not on
     the cut: boreal's quadrat area is fixed by its protocol, and wadden's effort, set after the sample is seen, is not
     released, while this dataset's area swept is (issue 6). NOAA's design-based index averages the hauls' CPUE with
     equal weight in each stratum
     ([gapindex](https://afsc-gap-products.github.io/gapindex/articles/background_equations.html)), so it carries the
     same bias of the cut tows.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Copy; cut claimed for pollock (implemented) | `taxon_group` a scoring column, `taxon` a feature; effort dropped; the notes claim the cut for pollock only | the rule's shape; claims what the data shows; scores unchanged | one more column in the frame |
     | B | Read `taxon` directly | no copy; the warning accepted | no change | against the reworded rule |
     | C | Weight the density by the area swept | the area swept a weight scoring column and the training weight | an actuarial convention | the map's decision is per cell of equal area, though the scored hauls are not; ranks models as the density score does |

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

5. **Restate Lennart's CC claim that the tow cut shows for walleye pollock alone?**

   * **Problem:**
     - Your CC of 2026-11-06 claims the cut for walleye pollock only, on the reading that for the other taxa a smaller
       area swept explains the higher densities of short tows.
     - A test of that reading, which redraws each short tow from a full tow of its cell thinned by the ratio of the
       areas swept, finds Pacific cod's short tows higher than the smaller area explains, and among the tows with a
       catch also those of Pacific halibut, sablefish, shortspine thornyhead and rock sole.
     - The AI does not edit a CC[^5a], so the claim stays as written until you restate it or name the fact that sets
       cod apart.
   * **Background:** A short tow is one under 0.75 of the median duration of its region and year (1,699 of 35,561
     hauls). A tow hauled back early on a large catch records a high density for the taxa it caught; a short tow also
     sweeps a smaller area, so one fish gives a higher density, which needs no stop. The test separates the two: it
     redraws each short tow's count 20 times as a binomial thinning of a random full tow of the same stratum and year,
     by the ratio of their areas swept, and sets the measured gaps (the README's decision "The tow's effort is
     dropped") against the redrawn ones.
   * **Effect on the task:** None on the scores or the features: the realized effort is dropped, no feature carries
     the cut, and the short tows stay, since no model is trained or scored on rows selected by the realized
     effort[^5b]. What changes is the reason the record gives for your decision, which a measurement now
     contradicts[^5c].
   * **Experiments:** claim auditor, from the raw tables, 20 draws of the null; log1p numbers per km^2 against the mean
     of the stratum and year:
     - Walleye pollock: +0.357 against the null's -0.070 over all hauls, 0.551 against 0.070 with a catch.
     - Pacific cod: +0.077 against -0.084 over all hauls and 0.229 against 0.051 with a catch, about 4 and 9 standard
       deviations of the null; its gap is largest on the EBS shelf and the slope (+0.18, +0.36), where pollock's is.
     - With a catch, Pacific halibut, sablefish, shortspine thornyhead and rock sole sit 2.4 to 3.9 standard
       deviations above the null; for Atheresthes, Dover sole, Greenland turbot, Hippoglossoides and rex sole the
       smaller area explains the gap.
     - Over all hauls the flatfish fall below the null (Hippoglossoides -0.360 against -0.039, rex sole -0.276 against
       -0.063), so short tows land at other places within their cells than full tows, and a stop on a large catch is
       the likely reading for pollock and cod, not isolated.
   * **Panel:** The advocate: no feature carries the cut and the rows cannot be filtered, so the decision stands either
     way. The critic: the CC's reason is refuted for five taxa besides pollock, and cod's gap is largest exactly where
     pollock's is. The mediator: a fact correction, not a weighing; restate the CC.
   * **Consistency:** Your CC of 2026-11-06 replaced a note that read pollock's measurement for every taxon; the test,
     which could have confirmed pollock alone, puts cod with it. The notes, the decision's caption and issue 4 state
     the test since the re-review; the decision's title still reads "the cut is claimed for walleye pollock only", as
     your CC does.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | The CC as written (implemented) | the CC and the decision's title claim the cut for pollock alone; the notes give the test | no new CC | the CC's reason is refuted for cod and four more taxa; the CC and the notes disagree |
     | B | Pollock and, to a lesser degree, Pacific cod | a new CC: "the cut claimed for pollock and, to a lesser degree, Pacific cod; the stop is the likely reading, not isolated"; the decision's title follows | claims what the test measured; the notes already say so | a second taxon named; the stop not isolated from where the tows land; halibut, sablefish, shortspine thornyhead and rock sole, above the null only among tows with a catch, left unnamed |
     | C | Pollock alone, with the fact that sets cod apart | a new CC keeps pollock alone and names why cod's excess is no stop | one taxon claimed, as decided | no such fact is measured: cod sits 4 and 9 standard deviations above the null, largest where pollock's gap is |

   * **Recommendation:** B, as the mediator recommends: it claims what the test measured and moves no score.
     **Decision:** A, B or C?

   **Notes for the AI:** the CC of 2026-11-06 stays word for word, in `curation_comments` and in the record. On B or C,
   append the curator's new CC (dated, in their words) after it in `curation_comments` and to the record through the
   store API. On B, retitle the fourth decision in `_decisions` "The tow's effort is dropped; the cut is claimed for
   walleye pollock and, to a lesser degree, Pacific cod" and drop "(the CC of 2026-11-06 below claims the cut for
   pollock only; REVIEW.md issue 5)" from the tow-cut bullet of the notes. On C, put the curator's fact into the
   tow-cut bullet and the caption. Then `dataset check` (README). Optional, the mediator's extra: a column with the
   null's gap in `_short_tows`, so the decision table shows the test.

   [^5a]: principles.md, "Arguing a call": a documented decision is not a correct one; when the evidence contradicts
     the stated reasoning, say so and argue the case, surface it and do not override it: the curator has the call.
   [^5b]: **LEAK-10** (Must): a feature holds only what existed at the prediction point. **LEAK-41** (Must;
     2026-11-06, Lennart): a rate's denominator set or cut after the prediction point is never a model input, and no
     model is trained or scored on rows selected by the realized weight.
   [^5c]: **EV-1** (Must): facts before rules; settle a disputed fact with the decisive experiment, and test a claim
     the same way wherever it comes from, a curator's intuition included.

   **Resolved (2026-11-08, Lennart):** B. A new CC claims the cut for walleye pollock and, to a lesser degree, Pacific
   cod, with the stop the likely reading, not isolated; it supersedes the claim of the CC of 2026-11-06, which stays as
   written. The fourth decision is retitled to match and the tow-cut bullet no longer points to this issue; features,
   rows and scores are unchanged (`dataset check`: 0 errors, 0 warnings).

6. **Record this unweighted dataset in the leak rules' worked case for a cut-short time on risk by a clause in its remedy, or only as a listed case?**

   * **Problem:**
     - The leak rules keep a table of worked cases (how a rule was applied to past datasets); its row for an amount at
       risk cut short by the outcome says that where the cut cannot be located row by row and the amount is a rate's
       denominator, the recorded amount ships as the metric's row weight and the training weight[^6a].
     - This dataset falls in that branch, yet ships unweighted with no sample weight under the rule for rates, which
       scores a decision per cell of an equal-area map unweighted[^6b].
     - An entry is required, since a decided dataset that contradicts its row is recorded in it, and it applies the
       rule for rates rather than departing from it[^6c]; only its wording is open.
   * **Background:** The area swept is the density's denominator, and which short tows the catch cut cannot be told
     row by row: 149 of the 256 tows under half the median duration carry the performance code of a tow without a
     noted problem. The rule for rates outranks a row of cases, which records how the rules were applied[^6c]. The
     precedent checker found this dataset the first case where a denominator the outcome cuts is released and left out
     as a weight on purpose: wadden_sea_sibes_macoma_abundance, also scored unweighted, has an effort its outcome sets
     (a subsample fraction chosen after the sample is seen) but does not release it.
   * **Effect on the task:** None on this dataset, which stays unweighted with no sample weight. The entry decides
     what the row tells the next dataset with a released effort that the outcome cuts and an equal-area decision: as
     written, it would ship that effort as a weight.
   * **Experiments:** Weighting would not change the ranking here: scoring the counts (the density times the area
     swept) ranks the models as the density score does (Kendall tau 0.80-1.00, the same winner in 5 of 5 windows;
     exposure study of 2026-11-05), and a stratum-area design weight ranks 7 untuned models alike (tau 0.81-1.00, the
     same winner in 4 of 4 windows; domain practitioner).
   * **Panel:** The advocate: an application of the rule for rates, not an exception, so the entry has the kind
     "application". The critic: the entry is required, not optional, since without it the row asks for a weight. The
     mediator: the advocate wins on the kind and the critic on requiring it; weighting by the area swept is out, as it
     breaks the rule for rates.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | The row as written (implemented) | no entry for this dataset | no edit | a case that reads against its row; the next survey table would ship a weight |
     | B | A clause in the row's remedy | the remedy adds: where the decision is per unit of an equal-area map, the rate is scored unweighted and no sample weight is declared, the notes naming the cut's bias; this dataset and wadden listed as its cases | the row and the rule for rates agree in writing; the next survey table finds the case | one more clause in a long row |
     | C | A listed case only | this dataset listed under the row's cases, the remedy unchanged | shorter | the row's text still reads as asking for a weight |

   * **Recommendation:** B, as the mediator and the precedent checker recommend: the row then states the equal-area
     case itself. **Decision:** A, B or C?

   **Notes for the AI:** the main session edits `.claude/skills/knowledge-curation/references/leak_checks.md` after the
   mark (the Cases row "Time on risk or another amount at risk cut short by the outcome", LEAK-10, LEAK-7, LEAK-41),
   as an entry of kind "application", not "exception". On B, add to the row's remedy: "where the decision is per unit
   of an equal-area map, the rate is scored unweighted and no sample weight is declared (MET-15); the notes name the
   cut's bias", and list noaa_afsc_bottom_trawl_survey_cpue (the area swept released and left out as a weight; the
   cut not located row by row: 149 of the 256 tows under half the median duration carry performance code 0) and
   wadden_sea_sibes_macoma_abundance (the subsample fraction, set after the sample is seen, not released). On C, list
   noaa_afsc_bottom_trawl_survey_cpue alone, with the same facts. Nothing changes in this folder.

   [^6a]: **LEAK-10, LEAK-7, LEAK-41**, Cases row "Time on risk or another amount at risk cut short by the outcome"
     (Andrej, 2026-11-02; amended 2026-11-06, Lennart): where the cut cannot be located and the amount is the
     denominator of a count or amount target, the target ships as the rate and the recorded amount as its weight
     scoring column and the task's sample weight, never as a feature.
   [^6b]: **MET-15** (Must; 2026-11-06, Lennart): when the decision is per unit of an equal-area map, per loan or per
     contract, the rate is scored unweighted and no sample weight is declared.
   [^6c]: principles.md, "Conflicts between rules": rules win over patterns and over precedents (how they were
     applied), and a precedent that contradicts a rule is flagged, not followed; "Exceptions and amendments": a Must
     has no exceptions.

   **Resolved (2026-11-08, Lennart):** B. The remedy of the time-on-risk row of the leak rules' cases gains the clause
   for a decision per unit of an equal-area map (the rate scored unweighted, no sample weight, the notes naming the
   cut's bias), with this dataset and wadden_sea_sibes_macoma_abundance as its cases, an application of the rule for
   rates; the notes' Effort bullet cites it. Nothing else changes in this folder.

10. **Test each survey year with every earlier season in training, or keep the two-year windows fitted once?**

   * **Problem:**
     - Each two-year window is fitted once, on the seasons before its first year, so the 6,969 hauls of each window's
       second year, 42.6% of the 16,359 test hauls, are predicted without the season just before them (counted on the
       raw file).
     - The split text says a model refit after each season is tested on the next cycle (dataset.py:229-230, :383-384),
       and that refit is the fact behind issue 2's call for no gap, while the use case is the five-yearly habitat
       review (dataset.py:206-209), so the windows follow neither actor[^10a].
     - Should the windows become one year long, or should the split text name a refit after each two-year survey cycle
       as the actor's cadence?
   * **Background:**
     - Two years is the survey cycle since 2005 (the Gulf of Alaska in odd years, the Aleutians in even years, the
       eastern Bering Sea shelf every year), so each window holds every region (dataset.py:377-380); that was the
       reason given for the two years Andrej asked for in issue 2.
     - Of the 6,969 second-year hauls, 3,241 are eastern and northern Bering Sea hauls whose own region was surveyed
       the year before; for the other 3,728 (Aleutians and slope) the region's previous survey, two years back, is in
       training, and what they miss is the neighbouring regions' newest season (counted on the raw file).
     - Nine one-year windows, the number the window rule gives for this size, would test the survey years 2026 back
       to 2017 (none ran in 2020): 8,183 hauls, the oldest window training on 77% of the hauls; each window holds the
       eastern Bering Sea shelf and either the Gulf or the Aleutians, and every taxon still has catches in every year,
       Dover sole and Greenland turbot in at least 29 hauls (counted on the raw files)[^10c].
   * **Effect on the task:** the second year's hauls are predicted from data a season older than a model refit each
     season would have, so they are scored somewhat harder than the split text's actor would be, and easier than the
     review's five-year horizon; the size is not measured, and the windows may not be chosen by such a
     comparison[^10c].
   * **Consistency:**
     - Issue 2's exception to the gap rests on a season being published before the next one (Andrej,
       2026-11-02)[^10a].
     - Each window trains on what is known before it starts (a rule of 2026-11-02, reframed 2026-11-05): with one-year
       windows this holds for every test year, with two-year windows only for the first year of each (an AI reading
       of a sentence written about windows)[^10b].
     - noaa_storm_events_damage refits once a year and tests one calendar year per window.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Two-year windows (implemented) | nine windows, 2025-2026 back to 2009-2010, one fit each | Andrej's call of 2026-11-02; each window holds every region; 16,359 test hauls | 42.6% of the test hauls lack the season before them, which the text's refit and the no-gap reason assume |
     | B | One-year windows | nine windows, the survey years 2026 back to 2017 (none in 2020), each trained on every earlier season | every test haul has every earlier season, as the split text and the no-gap call say | 8,183 test hauls and no test year before 2017; each window holds only one of the Gulf and the Aleutians |
     | C | Keep the windows, rewrite the text | the split text and the splits comment name a refit after each two-year survey cycle as the cadence | no data or split change | the cadence is ours, neither the review's five years nor a refit each season; the no-gap reason needs rewording, as the second year sits a season after its training data |

   * **Recommendation:** B: it gives every test year the history the split text and issue 2's no-gap call describe, at
     the cost of fewer test hauls and a region mix that alternates by year; C if you want each window to keep holding
     every region. **Decision:** A, B or C?

   **Notes for the AI:** On B: `TemporalSplits(window=1, unit="years", cutoffs=(2017, 2018, 2019, 2021, 2022, 2023,
   2024, 2025, 2026))` (check that the empty 2020 needs no cutoff); seventeen windows (2009 to 2026) would keep the old
   test span but exceed the nine of SPLIT-15. Rewrite `task_summary.split`, `splits_comment` (the cycle sentences; the
   oldest train share goes from 54% to 77%), the notes' Greenland turbot spread and the Metric bullet's "scorable in 9
   of 9 windows with at least 71 positives" (recount: the minimum becomes 29, Dover sole and Greenland turbot); re-run
   `dataset check`, the task probe and the leak probes on the cluster; CHANGELOG and a CC line. With issue 11's B the
   2026 window goes. On C: rewrite `task_summary.split` and `splits_comment` ("a model refit after each two-year
   survey cycle is tested on the next cycle") and the no-gap reason. The rules: SPLIT-10 (issue 2's exception),
   SPLIT-12, SPLIT-14, SPLIT-15, SPLIT-21.

   **Andrej (2026-11-09, as implemented):** A, as implemented.

   **Consistency check (AI, 2026-11-09): Keep the two-year windows and reword the three sentences that describe a refit after each season?**
   * **Problem:**
     - Kept as they stand, three sentences become untrue: the split text, the no-gap reason and your exception to the
       gap rule of 2026-11-02 say a model is refit after each season, while 42.6% of the test hauls, each window's
       second year, are predicted without the season before them[^10d].
     - The two-year windows themselves follow your call of 2026-11-02 and your pricing_game_2016 rule of the same day,
       one fit per test set; only the text is at odds.
   * **Background:** the three places are `task_summary.split` (dataset.py about line 229), the no-gap sentence of
     `splits_comment` (about line 383), and the record's exception of 2026-11-02, whose "as a model refit after each
     season would" becomes "after each survey cycle"; the exception's fact, a delay shorter than the windows' step,
     still holds.

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | a | Two-year windows, the text reworded | the windows as now; the three sentences say "a model refit after each two-year survey cycle is tested on the next cycle" (option C's text) | no data or split change; the text true again | the cadence is ours, not the source's |
     | b | One-year windows | option B | every test haul has every earlier season | fewer test hauls; no test year before 2017 |

   * **Recommendation:** a: it keeps your windows and only makes the text say what they do. **Decision:** a or b?

   **Andrej (2026-11-09, ok):** Go ahead

   **Resolved (2026-11-09, Andrej):** a: the nine two-year windows stay, each fitted once; `task_summary.split`, the
   no-gap sentence of `splits_comment` and the record's exception to SPLIT-10 now say "a model refit after each
   two-year survey cycle", and the splits comment adds that each window's second year (42.6% of the test hauls) is
   predicted a season after the model's newest data. Rows, split and score unchanged.

   [^10a]: Issue 2 (Andrej, 2026-11-02): "Temporal is good, but there is no need to do five years. Also no planning
     gap is required. Instead of five years, I suggest 2."; resolved as nine two-year windows without a gap, an
     exception to **SPLIT-10** (Should), the fact being that "the source states no delay and a season is published
     before the next one". **SPLIT-12** (Should): the horizon is a judgment from the source, including "the refit
     cadence".
   [^10b]: **SPLIT-14** (Must, in main): "As time moves on, a refit sees the data that arrived since, so each window
     trains on what is known before it starts (Andrej, 2026-11-02; reframed 2026-11-05, Lennart)." Applying it within
     a window is an AI reading.
   [^10c]: **SPLIT-15** (Should): "as many windows as an IID or grouped task of that size would get folds".
     **SPLIT-21** (Must): "Decide neither the training history nor the windows from a comparison over a few test
     windows."
   [^10d]: **USE-8** (Must): "Write how closely the data mirrors the use case, its fit"; a split text naming a refit
     the windows do not have misstates it. The exception to **SPLIT-10** (Should) of
     2026-11-02 rests on the delay being shorter than the windows' step, which holds under either wording.

11. **Keep the 2026 catches, which FOSS has not yet rated, in the newest test window?**

   * **Problem:**
     - FOSS has not yet rated the 2026 catches: all 3,968 catches of the 11 taxa lack a `taxon_confidence`
       (dataset.py:314), while every catch of 2021-2025 has one (counted on the raw files).
     - The 722 hauls of 2026 are 44% of the newest window, so its score rests in part on catches not yet through the
       survey's own identification check.
     - Keep them, end the newest window at 2025, or download FOSS again right before the build and keep 2026 only
       once it is rated?
   * **Background:**
     - `taxon_confidence` grades how sure the identification of a catch is (High, Moderate, Low); in 2021-2025 every
       catch of the 11 taxa is High (82% to 86% per year) or Moderate (counted on the raw files); it is no feature.
     - The 2025 catches were rated in the download of 2 November 2026, so a season's rating seems to arrive within
       about a year (inferred from one season).
     - Three of the 11 taxa are already groups of species the survey does not tell apart reliably (Atheresthes,
       Lepidopsetta, Hippoglossoides), where a re-identification would most likely fall (an AI reading).
     - The notes already ask to compare with a fresh download before a build, and to build from it or end the window
       at 2025 if the 2026 rows change (dataset.py:314).
   * **Effect on the task:** the review scores its models on checked catches, years after the survey; if rating
     changes some 2026 counts or species codes, the newest window is scored on labels the review would not use, and if
     it changes nothing the score is the same.
   * **Consistency:** noaa_storm_events_damage compared two downloads of its 2024 file, 16 months apart, and found
     99.83% of the damage values unchanged (its notes); no rule in main covers a provisional season, so this is a
     weighing call[^11a].
   * **Unknown:** whether rating changes counts or only adds the grade (FOSS's documentation was not read for this),
     and when FOSS will rate 2026.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep 2026, checked at the build (implemented) | the 2026 hauls stay; before a build a fresh download is compared and used if the 2026 rows changed | keeps 44% of the newest window; the check is already in the notes | until FOSS rates 2026, part of the window is scored on unchecked identifications |
     | B | End the newest window at 2025 | the 722 hauls of 2026 (7,942 rows) leave; the newest window holds 2025 alone | every scored catch is rated | loses the newest season; one window of one year among two-year windows |
     | C | Keep 2026 only once rated | at the build, download FOSS again; build from it if 2026 is rated, otherwise end at 2025 for that build | rated catches always, and the newest season once it is rated | what a build holds depends on FOSS's timing; a fresh download can change older rows too, so the notes' counts are restated |

   * **Recommendation:** A: a rating grades how sure an identification is, every catch of these taxa was High or
     Moderate in five seasons, the taxa most open to re-identification are already merged into groups, and the build
     check in the notes catches any change to the 2026 rows; C if you want no unrated catch in any build.
     **Decision:** A, B or C?

   **Notes for the AI:** On B: drop the 2026 hauls in `_clean` by the date's year, with a note, or with issue 10's B
   drop the 2026 window; restate the window counts. On C: at the build, re-run the FOSS download of
   `download_description`, check `taxon_confidence` for 2026, and restate every count the notes take from FOSS (hauls,
   catches, positives per window, the GOA 2025 note); CHANGELOG entry. On A: nothing; the note at dataset.py:314
   stays.

   **Andrej (2026-11-09, as implemented):** A, as implemented.

   **Resolved (2026-11-09, Andrej):** A: the 2026 hauls stay in the newest test window; before a build a fresh FOSS
   download is compared, and if the 2026 rows changed the build uses it or ends the newest window at 2025 (the notes'
   check).

   [^11a]: The curator's standard for the information audit of 2026-11-09: every piece of information actually
     available at a point is available to the benchmark there, and nothing more; when the review scores, it has the
     checked catches.

**Review panel:** ship after changes (mediator); the changes (text and one assert) are made. Tier full, a re-review of
2026-11-06 under LEAK-41 and MET-14 to MET-16 after issue 4 was resolved: claim auditor, column auditor, split auditor,
domain practitioner, precedent checker, blind reviewer, task gamer, advocate, critic and mediator. Claims: 25; 16 hold,
4 refuted and 3 refuted in part, all fixed in the notes or by the assert, 2 untested (whether pollock's gap is a stop or
where the short tows land; TM-459's wording, held at the audit of 2026-11-01). Blind review: include with small changes;
its main concerns are the long format (11 rows per haul with shared features, safe as no haul straddles a cutoff) and
the temperatures read during the haul (the prediction point takes them as that year's field, settled after the first
panel), and its worry about false zeros is answered (the 128 uncounted catches are dropped, not zero-filled). Task
gamer: no exploit above the noise of about 0.01 (six attacks; all effort proxies together +0.005, worse). Agreed: no
leak (the realized effort reaches the features only through place and year), the copy `taxon_group`, every window
scorable, the unweighted score with its reworded reason, the split, the MET-14 assert and the text fixes. Disputed: the
scope of the cut claim (settled for the critic: the area reading is refuted for six taxa, pollock included; the CC is
issue 5), the train and test sides (settled for the advocate: both sides, different regions), the 1/weight score
(settled for the critic: two labelled comparisons), whether the squared-deviation shares are required (added either
way), and the kind and need of the time-on-risk Cases-row entry (settled: an application, and required; its wording is
issue 6).

<details><summary>Mediator</summary>

The mediator's issue 1 is issue 5 of this file and its issue 2 is issue 6; its cross-cutting evidence goes to X2 and X3 of the working copy's REVIEW.md. One figure of change 7 differs in the definition: Greenland turbot's spread, which the metric takes per test window, is 12-35 per km^2 from 2017 on against 162-543 before; 8-38 and 47-639 are its spreads per survey year.

MEDIATOR REPORT: noaa_afsc_bottom_trawl_survey_cpue (exposure re-review, 2026-11-06, full tier)

I ran no new model. The one disputed number, the Poisson range, I checked against the exposure study's own output (its model summary of 2026-11-05). Every other disputed fact is already settled by a measurement in the panel's reports.

**1. Recommendation (judgment record)**

```text
Verdict: ship after changes (text, one assert; rows, target, features, split and metric unchanged).
Validity: USE-3 holds (realized effort out: an untowed cell has no tow). LEAK-41 holds as a leak rule (the shipped
  features carry the realized effort only through place and year: area ratio R^2 0.10, short tows AUC 0.75, risk
  selection under USE-6). LEAK-41's reporting clause is not met, fixed in text (Poisson gain +0.013, not "nothing";
  the 1/weight score stated). LEAK-10 holds (no feature carries the cut). EV-1 triggered on the cut claim, fixed in
  text (cod and four other taxa sit above the area-only null). SPLIT-1/3/9/11/12/13/14/23 hold; SPLIT-20 a note.
Value: MET-2 holds (taxon_group exact copy, 11 taxa scorable in 9/9 windows, >=71 positives). MET-15 holds and
  decides "unweighted, no sample weight" (the decision is per cell of an equal-area map); MET-16 holds (no design
  weight: EFH is no population estimate; a design weight ranks 7 models alike, tau 0.81-1.00, same winner 4/4). The
  stated reason is reworded. TP: RF skill +0.786, no flags.
Quality: MET-14 departure fixed (assert the count rebuild in _clean; holds to 1.6e-4). Splits comment corrected.
  Poisson range corrected.
Weighed: none open.
For the curator: issue 1 (restate the CC's cut claim, a fact correction), issue 2 (wording of the LEAK-41
  Cases-row entry, kind "application"), cross-cutting X2 and X3 evidence from this dataset.
```

**2. Changes to make now (no decision needed)**

The file is the dataset's `dataset.py`. The same text also goes into REVIEW.md issue 4, where it repeats the claims.

1. **LEAK-41 reporting clause (Must, P4).** In the Effort bullet:
   - Replace "nothing under a Poisson fit" with the two runs: mean -0.006 (study, 1 of 5 windows better) and +0.013 (claim auditor, 4 of 5 better), per window -0.007 to +0.033.
   - LEAK-41 decides on the worse fit, which is about 0.013. The drop stands on timing ("whatever it scores").
2. **LEAK-41, the 1/weight score.** State two labelled comparisons. Do not merge them (EV-8).
   - Taxon + 1/area swept: 1.031-1.046, against the taxon alone at 1.039-1.057 (gain 0.007-0.013).
   - Beyond srvy and year: 1.016-1.034 against 1.027-1.041 (gain 0.004-0.012).
   - The honest LightGBM scores 0.90-0.93.
   - Do not call it a bound on the leak. The free effort columns under Poisson gain more in single windows (+0.0325, +0.0204), so here the figure is no ceiling (EV-1, EV-2). This text holds whichever way X2 is decided.
   - Ruling: the critic wins on form (two labelled numbers). The advocate's merged "1.016-1.046 ... 0.004-0.014" mixes two bases.
3. **The cut claim (EV-1 Must, LEAK-10 context): Effort bullet and the decision caption at lines 499-500.** This is the text only; the CC is issue 1 below.
   - Pollock's short tows stand far above an area-only null: +0.357 against -0.070 over all hauls; 0.551 against 0.070 among catches.
   - Pacific cod also stands above it, at about 4 and 9 null SDs; its gap is largest where pollock's is (EBS, BSS).
   - Among catches, halibut, sablefish, shortspine thornyhead and rock sole sit above the null at 2.4-3.9 SDs.
   - For Atheresthes, Dover sole, Greenland turbot, Hippoglossoides and rex sole, the smaller area swept explains the gap.
   - The flatfish fall below the null, so short tows are not exchangeable within cells. A catch-triggered stop is "the likely reading, not isolated" (EV-3).
   - The caption's "its tows end early on a large catch" becomes that hedged reading.
   - Ruling: the critic wins on scope. Row 12 measured all taxa, and "which a smaller area swept explains" is refuted for six of them, not one.
4. **Train side against test side (EV-1).** Both sides' facts are true and fit in one sentence (split auditor):
   - Pooled, the cut reads alike: training sides +0.35 to +0.40, the nine test windows +0.30.
   - By region it does not. The notes' EBS figures (+0.36 overall; 831 tows under 0.4 h) are mostly 1989-2008 training rows (EBS +0.71). Since 2009 the EBS shows +0.07, and in the test years the excess is in the AI (+0.39) and GOA (+0.73).
   - Ruling: the advocate's "both sides, different regions" is the accurate reading. The critic's "training side only" overstates.
5. **Short tows' weight in the score.** Add a note, labelled as weight in the score, not as the bias of a stop:
   - In the test years, short tows are 3.4% of each taxon's rows. They hold 14.0% of pollock's squared deviation, 10.1% of Greenland turbot's and 7.0% of shortspine thornyhead's.
   - Ruling on labelling: a share of squared deviation measures influence, not bias. Turbot's gap is within the area effect (row 12), and short tows are commoner at depth (6.7% at 500 m and deeper against 3.3% at 0-50 m).
   - Ruling on "required": MET-16 requires the notes to name outcome-dependent sampling. They already name pollock's cut, and change 3 extends this to cod. MET-16 does not require these shares. Add them anyway: both sides want the sentence, and nothing argues against it (P7, cheap and safe).
6. **The reason for scoring unweighted (MET-15, MET-16).** Keep the decision and reword the reason, as both sides agreed:
   - Wording: "scored unweighted over the hauls, as the source's RMSE over stations (TM-459 p. 21). No area-swept weight, since the decision is per cell of an equal-area map (MET-15). No design weight, since EFH is not a population estimate (MET-16). The hauls are not equal-area (AI about 8x the EBS per km^2), and a stratum-area design weight ranks the models alike (tau 0.81-1.00, same winner 4/4)."
   - Ruling: MET-15 governs the area-swept weight, and its premise holds. What was false is the description of the scored rows, which concerns the design weight under MET-16. Both rules point to unweighted.
7. **Splits comment (EV-2).** The comment is at line 228 (`split=`) and line 359. Change it to: "each window holds the EBS shelf, the GOA and, except 2019, the AI; the slope survey ended in 2016, the NBS runs in some years". Add one Greenland-turbot sentence to the Metric bullet: from 2017 on it is scored without the slope survey, on a spread of 8-38 per km^2 against 47-639 before.
8. **The Poisson range in the Metric bullet (EV-8).** "0.86-1.11" is refuted.
   - Both sides propose "0.86-1.24", but neither run gives 0.86: the study gives 0.879-1.243 and the claim auditor 0.996-1.179.
   - Write "0.88-1.24 (two runs, five windows each)", unless the builder names the run that gave 0.86.
9. **MET-14 assert (Should, P6/P7).** In `_clean`, merge `area_swept_km2` into `catch` and assert on the counted rows, per species code and before summing:
   ```python
   np.allclose(cpue_nokm2 * area_swept_km2, count, rtol=1e-3)
   ```
   - The data rebuilds the count to 1.6e-4 on 201,731 catches, and the frame does not change.
   - This does not wait for X3. FOSS releases the count, so the check applies under either outcome of X3.

**3. Issues for the curator (ranked)**

**Issue 1 (P4, EV-1 Must; fact correction, not a weighing): the CC of 2026-11-06 claims the cut "for walleye pollock only".**
- Problem: the CC rests on "which a smaller area swept explains". The null test refutes that for cod (4 and 9 SDs) and, among catches, for four more taxa.
- Effect: no score or feature moves. The record's reason for a curator decision is contradicted by a measurement.
- Advocate's best evidence: no feature carries the cut, and LEAK-41 bars filtering the rows, so the decision is unchanged.
- Critic's best evidence: claim auditor row 12, and the cod gap is largest exactly where pollock's is (EBS +0.18, BSS +0.36).
- Rule: EV-1. principles.md "Arguing a call": the AI surfaces and never edits a CC.
- Decision needed:
  - (a) a new CC: "the cut claimed for pollock and, to a lesser degree, Pacific cod; the stop is the likely reading, not isolated" (recommended);
  - (b) keep "pollock only" and name the fact that sets cod apart.

**Issue 2 (P4/P6, LEAK-41 Cases row against MET-15 Must): how to record noaa in the time-on-risk Cases row.**
- Settled by rank, and not open:
  - The entry is an application, not an exception. A Must has no exceptions. Cases are applications, and rules win over cases. MET-15's equal-area clause decides this case directly, and its premise (a per-cell map decision) holds.
  - The entry is required, not optional. As written, the row's second branch gives the opposite answer for noaa, and the precedent checker says noaa is the first case with an outcome-cut denominator that is released and deliberately left out. A case that reads against the rule is flagged and fixed, and a curator decision goes in with its case (principles.md, Conflicts; Keeping the rules current).
  - Ruling: the advocate wins on the kind of entry, the critic wins on requiring it.
- Open: only the wording.
  - (a) Add a clause to the row's remedy: "where the decision is per unit of an equal-area map, the rate is scored unweighted and no sample weight is declared (MET-15); the notes name the cut's bias", with noaa (and wadden as the unreleased-effort case) listed. This is the precedent checker's option a, and I recommend it.
  - (b) List noaa under the row's cases only and leave the remedy text. This is shorter, but the row still reads as asking for a weight.
- Out: weighting by area swept would break MET-15's Must clause.

**Cross-cutting evidence (for the X items in the working copy's REVIEW.md; no noaa change hangs on them):**
- **X2 (rewording "ceiling").** noaa adds a case. Under this level-sensitive metric, a fitted taxon + 1/area model scores 1.031-1.046, worse than the honest model (0.90-0.93). The free effort columns gain up to 0.033 in single windows, more than the "ceiling" gain of 0.007-0.013. This supports X2's proposal: report a fitted weight-alone score for a level-sensitive metric, without the word "ceiling".
- **X3 (MET-14 only when the count is released).** With change 9, noaa meets MET-14 and leaves X3's list. X3 then rests on two cases (boreal, wadden), not three, so the "third exception calls for an amendment" trigger (principles.md, consistency case 4) is not reached. X3 stays a plain wording proposal.

**Optional extras (the curator's preference, P7; neither side's ask):**
- a null column in `_short_tows` for the decision table;
- a note that log1p fits, inverted, predict 34-51% of the test mean density, which RMSE barely penalises.

**4. Agreed facts**

- `taxon_group` equals `taxon` on all 391,044 rows. It is not a feature, no sample weight is declared, and the scorer matches an independent computation to 4 decimals in 9/9 windows. `dataset check` gives 0 errors and 0 warnings.
- The realized effort is dropped. From the features, area swept reaches R^2 0.85-0.91, but only -0.11 to +0.18 against the region-year means. The realized area ratio reaches R^2 0.103, and short tows are told apart at AUC 0.749.
- L2 gain of the effort columns: +0.0004 to +0.0028.
- Poisson gain: +0.013 in one run, -0.006 in the other.
- 1/area with the taxon gains 0.007-0.013 over the taxon alone.
- Hauls are not equal-area: AI 5.99, EBS 0.75 hauls per 1000 km^2 per year; strata within a survey and year differ up to 22.1x (AI) and 9.5x (GOA).
- A design weight and a taxon x region score rank 7 models alike (tau 0.81-1.00, same winner 4/4).
- Splits: 0 hauls straddle a cutoff; training shares 54.0-95.4%.
- Dropping short tows from training moves the score -0.0013, and dropping the 30-minute era -0.0011, both noise. LEAK-41 bars a filter anyway.
- The 128 uncounted catches are dropped, not zero-filled (CLEAN-15).
- Region coverage: BSS is absent from 6 windows, NBS from 3, and AI from 2019.
- Task probe: RF skill +0.786 ± 0.012; the blind reviewer says "include with small changes".
- The task gamer found nothing above the noise floor of about 0.01.

**Task gamer's exploits, mapped.** The definition has no `Potential leak, kept on purpose:` notes. Its one accepted warning (52% zeros) is unrelated, so every exploit is new. None is an issue: all are below noise and none touches a note.

| # | Exploit | Gain | Rule | Reading |
|---|---|---|---|---|
| 1 | Hauls per survey-year or stratum-year over the test window | -0.009 | LEAK-30 (test-set statistics); LEAK-37/USE-6 | The design is known in advance |
| 2 | Station history using first-test-year labels | -0.0035 over honest history | SPLIT-12 (the two-year horizon), LEAK-34 | A deployed model lacks these labels |
| 3 | Hauls per survey day, a pace proxy | -0.005 | LEAK-41 (an effort encoding) | Below noise |
| 4 | Distance to the nearest same-day haul | -0.006 | LEAK-30 | Below noise |
| 5 | Rows per haul, marking a dropped taxon row | +0.001 | LEAK-10 (a missingness marker), CLEAN-15 | No signal |
| 6 | Day rank within the survey year | -0.001 | LEAK-30 | Below noise |

All effort proxies together: +0.005, so they hurt.

**5. Consistency with precedent**

- The `taxon_group` copy follows liberty_mutual's `var11_weight` (MET-2). There is no drift.
- Dropping the realized effort follows fremtpl2, bemtpl97 and wadden (USE-3, LEAK-41).
- The unweighted density departs from the wording of the LEAK-41 time-on-risk Cases row.
  - It rests on MET-15's own Must clause, which outranks a Cases row.
  - The fact that sets it apart: the decision is per cell of an equal-area map, not a sum over the amount at risk. The difference from wadden: noaa's denominator is released.
  - So it is consistent with the rules, and the row needs the entry in issue 2.
- The boreal and wadden precedents match on "unweighted per unit area", not on the cut. The issue's Consistency bullet should say so.
- The register flags no third exception on MET-14, MET-15 or LEAK-41. With change 9, X3 drops to two cases.
- Panel file only: CHANGES.md headlines +0.55, the among-catches figure. The figure that carries the claim is +0.36 over all hauls. The definition, the CC and REVIEW.md already use +0.36.

</details>

<details><summary>Claim audit</summary>

CLAIM AUDITOR: noaa_afsc_bottom_trawl_survey_cpue (exposure re-review, 2026-11-06, full tier)

Verdict: today's change holds where it matters. The copy `taxon_group` is exact, it is not a feature, and it scores
the same as `taxon`. The effort columns stay out, no sample weight is declared, and the shipped features do not carry
the realized effort beyond the region and year. No validity claim is refuted. Five of the exposure paragraph's
supporting statements are refuted or refuted in part. The fixes are to the text, plus one assert and one ceiling
number. Rows, target, split and metric do not change.

CLAIMS TABLE (today's change first)

| # | claim | source | test | result | evidence | rule |
|---|---|---|---|---|---|---|
| 1 | `taxon_group` is a copy of `taxon` | _clean step 5; ScoringColumn description; issue 4 | compare the two columns on all 391,044 rows | holds | identical on every row | MET-2 |
| 2 | `taxon` stays a feature and `taxon_group` is never one | issue 4; README scoring-column table | feature_columns(c) | holds | features: taxon, srvy, stratum, latitude, bottom_temperature_c, surface_temperature_c, depth_m, date, longitude_east (9); taxon_group left out; sample_weight None | MET-2 |
| 3 | "the scores do not change: the copy holds the same values" | CC 2026-11-06; issue 4 | scorer(c) on a permuted prediction against my own per-taxon computation through `taxon`, nine windows | holds | equal to 4 decimals in all 9 windows (e.g. 77.9831 / 77.9831) | MET-2 |
| 4 | metric = mean over taxa of sqrt(1 - R^2) on counts | metric.definition | computed both ways on the nine windows | holds | identical in all 9 | MET-11 |
| 5 | "A taxon whose catches do not vary is left out; none is in the nine windows"; every fold scorable | metric.definition; notes | units per taxon per test window | holds | 11 of 11 taxa in every window; at least 1,056 rows and 71 positives per taxon (Greenland turbot, newest windows); smallest spread 8-19 per km^2 | MET-2 |
| 6 | the source folds the area swept into CPUE ("catch per km^2 swept ... distance fished times net width") | notes, Effort bullet; issue 4 Background | cpue_nokm2 x area_swept_km2 against count on 201,731 catches; distance x width / 1000 against area_swept_km2 on 35,561 hauls | holds | median relative gap 6.8e-6, max 1.6e-4; area: max 1.6e-4; every count an integer | MET-14 |
| 7 | MET-14 also says `_clean` asserts that target x denominator rebuilds the count | MET-14 (Should), implied by the declaration of a rate | read _clean | refuted in part (absent) | `_clean` asserts cpue_kgkm2 > 0 but never cpue_nokm2 x area_swept_km2 == count. The identity holds on the data (row 6) | MET-14 |
| 8 | standard tow 30 min in the Bering Sea (medians 0.50-0.52 h in each of its three surveys), 15 min in the GOA from 1996 and AI from 1997 | notes; CHANGES | median duration_hr by survey and year | holds | all-year medians EBS 0.504, NBS 0.518, BSS 0.519 (year medians 0.50-0.53); GOA 0.50 to 1993, 0.278 in 1996; AI 0.50 to 1994, 0.294 in 1997; 0.26-0.28 since | USE-3 |
| 9 | the planned effort reaches the models through region and date; realized effort is excluded and not carried by the features | notes; issue 4 | LightGBM of area_swept_km2 and duration_hr on the shipped features (one row per haul), trained on each of 5 windows, scored on its test hauls; R^2 also against the region-year means | holds | R^2 0.85-0.91 (area) and 0.87-0.94 (duration), all from region and year: against the region-year means R^2 -0.11 to +0.18 (area) and -0.38 to +0.08 (duration). No hidden carrier | LEAK-41, USE-3 |
| 10 | 1,699 of 35,561 tows are short (< 0.75 x the median of their region and year) | issue 4 Experiments | recount | holds | 1,699 (AI 423, BSS 109, EBS 813, GOA 316, NBS 38) | EV-1 |
| 11 | over all hauls, pollock's short tows sit +0.36 above their cells, the others -0.36 to +0.08; among hauls with a catch, pollock 0.55, the others 0.00 to 0.25; EBS pollock tows under 0.4 h 8.33 against 7.35 log1p kg | notes; decision 4; CHANGES | recomputed from the raw tables | holds (the numbers) | 0.357; -0.360 to +0.077; 0.551; 0.002 to 0.249; 831 tows, 8.33 against 7.35 | EV-1 |
| 12 | "which a smaller area swept explains without any stop on the catch, so the cut is claimed for pollock alone"; "Over all hauls walleye pollock alone stands well above its cells" | notes, Effort bullet; decision 4 caption; issue 4 Resolved | NULL TEST: each short tow's count redrawn as a binomial thinning (ratio of the areas swept) of a random full tow of its cell, 20 draws, then the definition's two gaps recomputed | REFUTED IN PART | null gap over all hauls -0.02 to -0.19, among hauls with a catch +0.03 to +0.16. Above the null: pollock +0.357 vs -0.070 (sd 0.041), 0.551 vs 0.070 (0.029); PACIFIC COD +0.077 vs -0.084 (0.040), 0.229 vs 0.051 (0.020), about 4 and 9 null SDs; Pacific halibut all -0.102 vs -0.194 (0.034), positive 0.249 vs 0.159 (0.023); sablefish positive 0.199 vs 0.099 (0.039); shortspine thornyhead all 0.023 vs -0.019 (0.015), positive 0.183 vs 0.072 (0.047); rock sole positive 0.124 vs 0.041 (0.032). Explained by the smaller area: Atheresthes, Dover, Greenland turbot, Hippoglossoides, rex (positive). Cod's gap is largest where pollock's is (EBS +0.18, BSS +0.36) | LEAK-10, EV-1 |
| 13 | "its tows end early on a large catch" (the stop causes pollock's gap) | decision 4 caption; notes | the same null on the taxa that should not drive a stop | untested as a cause (not settled) | short tows are not exchangeable within their cells: the flatfish fall far BELOW the area-only null (Hippoglossoides -0.360 vs -0.039, rex -0.276 vs -0.063, Atheresthes -0.188 vs -0.063). So short tows also land at different places within a stratum, and pollock's +0.43 above the null mixes a stop with where the tow was. A catch-triggered stop is the likely reading but this design does not isolate it | LEAK-10, EV-3 |
| 14 | "The unweighted CPUE keeps the bias of the cut pollock tows, as NOAA's design-based index does, which averages the hauls' CPUE with equal weight in each stratum (gapindex)" | notes; issue 4 | gapindex "Background equations" | holds (the index part); "bias" untested | stratum mean = sum R_ij / n_i (each haul once), then x stratum area. Whether a cut tow's CPUE is biased, or the tow was cut in a dense patch and its CPUE is right, is not measured (row 13) | MET-15 |
| 15 | "the score is unweighted on this density, as the review maps it over cells of equal area" (CHANGES: "unweighted scoring over equal-area cells") | notes, Effort bullet; issue 4 Option C Con; CHANGES | hauls per 1000 km^2 per stratum and year, from the strata areas in GAP's GeoPackage (AREA_M2, latest design no later than the year) | REFUTED as a description of what is scored | the scored units are hauls, not equal-area cells. Hauls per 1000 km^2 per year (2015-2025): AI 5.99, BSS 5.33, GOA 1.75, EBS 0.75, NBS 0.69, so a km^2 of the Aleutians counts 8x one of the EBS shelf. Within a survey and year the stratum density varies up to max/min 22.1 (AI, CV 0.70) and 9.5 (GOA, CV 0.53); EBS 1.9 and NBS 1.0 are near equal-area. AI holds 16.5% of rows and 5.8% of the surveyed area. The conclusion stands (no area-swept weight: MET-15; a design weight only for a population estimate: MET-16). Only the reason is wrong | MET-15, MET-16, MET-2 |
| 16 | effort columns as free features: +0.0028 under L2 on log1p (better in 3 of 5 windows), "nothing under a Poisson fit" | notes; issue 4 Experiments | LightGBM (400 trees, 2 seeds) with and without duration, distance, width, height and area swept; newest five windows; L2 on log1p and Poisson on density | L2 holds; Poisson REFUTED as a general statement | L2 gain +0.0016, -0.0008, -0.0075, +0.0042, +0.0047 (mean +0.0004, 3 of 5 better). Poisson gain +0.0325, +0.0052, +0.0150, -0.0071, +0.0204 (mean +0.0132, 4 of 5 better; seeds agree in windows 2025-26 and 2017-18). The study's own Poisson run, on other windows, had -0.0061, 1 of 5. Under LEAK-41 "decides on the worse", so the worse is now about 0.013, not 0.0028. The drop stands | LEAK-41, EV-8 |
| 17 | LEAK-41: "states the score of 1/weight alone as the ceiling a leak would reach" | LEAK-41 (Must, on the reporting) | LightGBM on taxon alone against taxon + 1/area_swept, and the same with srvy and year added, five windows | refuted in part (not stated); now measured | taxon alone 1.039-1.057; with 1/area 1.031-1.046 (gain 0.007-0.013). Beyond srvy and year: 1.027-1.041 against 1.016-1.034 (gain 0.004-0.012). The honest LightGBM scores 0.90-0.93 | LEAK-41 |
| 18 | LightGBM on log1p scores 0.90-0.93 and beats the taxon means (1.01-1.23) in all nine windows | notes, Metric bullet | t1 (taxon means, nine windows), t3 (LightGBM, five windows) | holds | taxon means on counts 1.005-1.226 (on log1p 1.031-1.057); LightGBM L2 0.900-0.948 per seed, means 0.900-0.929 | MET-2 |
| 19 | "Poisson LightGBM scores 0.86-1.11" | notes, Metric bullet | t3; the exposure study's afsc_models_summary.txt | refuted (range) | mine 0.996-1.179 on five windows (2021-2022: 1.157 and 1.179); the study's run 0.879-1.243 (2021: 1.243). Two runs exceed 1.11 in the same window, and there Poisson loses to the taxon count mean (1.226) | EV-8 |
| 20 | pooled RMSE: pollock and rock sole hold 79-93% of an untuned model's squared error | metric.reason; notes | share under the taxon log1p-mean baseline, nine windows | holds roughly (model-dependent) | 76.8-92.2% for the baseline (2009-2010: 76.8%) | MET-2 |
| 21 | the source scores models by cross-validated RMSE on numerical abundance and weights them by it | metric.original | reopened the reference (TM-459, repository.library.noaa.gov/view/noaa/48659): the PDF is 119 MB, and no extractor here (no pdftotext, pypdf or poppler; the Read tool refuses >100 MB) | untested today; held at the 2026-11-01 audit | the earlier audit quotes p. 21 "the model with the lowest RMSE was considered to be the best performer" and RMSE^-2 weights. The record page confirms the title, authors and year (TM-459, 2022) | MET-1, MET-11 |
| 22 | "each window holds one survey of every region" | splits_comment | hauls by region and year | REFUTED | BSS ran 2002-2016 only, so it is absent from the 6 windows 2013-14 and 2017-18 to 2025-26. NBS is absent from 2011-12, 2013-14 and 2015-16. The 2019 window has no AI (no 2020 survey). Only 2009-2010 holds all five. Greenland turbot (BSS presence 0.70) has a spread of 8-38 per km^2 in the windows from 2017 on, against 47-639 before | SPLIT-14, EV-2 |
| 23 | no row is a copy across the split; a haul's taxa stay on one side | implied; splits_comment | leak probe; date split | holds | 0.0% exact feature copies in 9 splits; the split is by date and all rows of a haul share it | LEAK, SPLIT |
| 24 | counts in the notes (35,561 hauls, 201,859 catches, 128 not counted, 2,659 positive codes, 52.0% zeros, 391,044 rows) | notes | recount from the raw tables and the frame | holds | all equal | PROV |
| 25 | `dataset check`: 0 errors, 0 warnings; the MET-2 warning is gone | issue 4 Resolved | check_before.txt / check_after.txt | holds | before: task_metric_input_is_feature ['taxon']; after: 0 warnings | MET-2 |

THE METRIC CLAIM (MET-1, MET-2, MET-11, MET-14, MET-15)
- MET-1: the original is the source's (row 21, held at the earlier audit). The per-taxon normalization and the equal
  vote per taxon are ours (stand_in), with the reason given. Not re-read today.
- MET-2 holds. The unit (taxon x window) exists in every fold with at least 71 positives. The metric's extra input
  ships as a scoring column that is not a feature. The copy reads exactly what `taxon` read. The meaning carries one
  note (row 22): in the windows from 2017 on, Greenland turbot is scored without its main habitat (the slope survey
  ended in 2016), on a spread of 8-38 per km^2, and keeps one eleventh of the score.
- MET-11 holds: stand_in, original named, closeness argued by identity (a fixed divisor within a taxon).
- MET-14 holds on the data (row 6). The count is not in the frame. `_clean` lacks the assert (row 7, Should).
- MET-15 holds in what it decides: no sample weight, unweighted. The stated reason ("equal-area cells") is wrong for
  the scored rows (row 15).

REFUTED AND UNTESTED, RANKED (validity first, Must first)

1. Row 16, the Poisson gain (P4, LEAK-41 Must, reporting part). "Nothing under a Poisson fit" does not replicate:
   +0.013 mean, 4 of 5 windows. What it changes: the number the decision rests on (LEAK-41 decides on the worse fit),
   not the decision: the effort is still dropped, on timing (a place in a survey year has no tow). Mildest remedy: in
   the Effort bullet and issue 4 say "under a Poisson fit -0.006 to +0.013 by windows and seeds (two runs)".
2. Row 17, the 1/weight ceiling (P4, LEAK-41 Must, reporting part). Not stated. Measured now: 1/area swept with the
   taxon gains 0.007-0.013 over the taxon alone (0.004-0.012 beyond region and year). Mildest remedy: add one clause
   with the ceiling.
3. Row 12, "pollock alone" (P4, LEAK-10, text). Against an area-only null, Pacific cod's short tows also stand above
   their cells (+0.16 over all hauls, +0.18 with a catch, 4 and 9 null SDs). Halibut, sablefish, thornyhead and rock
   sole exceed the null among hauls with a catch at 2.4-3.9 SDs. What it changes: the claim "the cut is claimed for
   pollock alone" and "a smaller area swept explains" the positive gap. Neither feeds a feature (the effort is out), so
   no score changes. Mildest remedy: claim the cut for pollock "and, to a lesser degree, Pacific cod caught in the
   same tows" and say the area explains the gap for the flatfish, not for cod and halibut. Or test against the null
   and report it in decision 4 (_short_tows could add a null column).
4. Row 15, "unweighted over equal-area cells" (P6, MET-15/MET-16, reason only). Hauls are not equal-area: the
   Aleutians are sampled 8x as densely per km^2 as the EBS shelf, and strata within GOA and AI up to 9x and 22x.
   The unweighted score matches the source's own RMSE over stations, which is the right reason. Mildest remedy:
   reword to "scored unweighted over the hauls, as the source's RMSE over stations is (the hauls are not equal-area:
   AI about 8x the EBS per km^2); no area-swept weight, as the decision is per map cell (MET-15)". Optionally name
   the stratum design weight under MET-16 (GOA and AI allocate stations by stratum).
5. Row 22, "each window holds one survey of every region" (P4, SPLIT text). False for BSS (6 windows), NBS (3) and
   AI (2019). Mildest remedy: reword the splits_comment ("each holds the EBS shelf, the GOA and, except 2019, the
   AI; the slope survey ended in 2016, the NBS runs in some years") and add a Greenland-turbot line to the metric note.
6. Row 19, "Poisson LightGBM 0.86-1.11" (P6, text). Two runs give up to 1.18 and 1.24 in 2021-2022, worse than the
   taxon count mean there. Mildest remedy: "0.86-1.24 (two runs)".
7. Row 7, the MET-14 assert (P6, Should). Mildest remedy: in `_clean`, assert that cpue_nokm2 x area_swept_km2
   rebuilds count (rtol 1e-3) before the effort columns leave. It holds today to 1.6e-4.
8. Untested: row 13, whether pollock's gap is a catch-triggered stop or where the short tows land (the flatfish
   residuals show the tows are not exchangeable within cells). Row 14, whether a cut tow's CPUE is biased at all. Row
   21, the TM-459 wording (the PDF could not be read here; held at the 2026-11-01 audit). And whether GOA/AI station
   allocation depends on earlier surveys' catches (MET-16's note).

Sources: https://afsc-gap-products.github.io/gapindex/articles/background_equations.html ;
https://repository.library.noaa.gov/view/noaa/48659 ; the 2026-11-05 exposure study's model summary.

</details>

<details><summary>Column audit</summary>

COLUMN AUDIT (column-auditor, 2026-11-06, exposure re-review, full tier): noaa_afsc_bottom_trawl_survey_cpue

Verdict: ship. No leak. The new rules (LEAK-41, MET-14, MET-15, MET-16, CLEAN-16 as amended) hold, with one Should gap
and one note:
- MET-14 (Should): `_clean` does not assert that the target times the area swept rebuilds the count. The data rebuilds
  it, so the fix is one assertion.
- P6 note (MET-15): the unweighted density gives walleye pollock's cut tows four times their share of pollock's
  squared error. Put the number in the effort bullet.
`taxon_group` is an exact copy of `taxon` and stays out of the features. This audit builds on the column audit of
2026-11-01 in REVIEW.md. Its settled points (the temperatures note, the 2026 season, the 1993-95 depths, the stratum
repair, the drop reasons) are not reopened.

Frame: dataset_io.from_definition, 391,044 rows. Features: taxon, srvy, stratum, latitude, longitude_east, date, depth_m,
bottom_temperature_c, surface_temperature_c. Target: log1p_cpue_no_km2. Scoring column: taxon_group (role group).
No sample_weight, so probe 22 does not apply (probes/p22 is empty).
dtype probe (dtype_probes.py, --no-fetch): 0 of 8 columns flagged.

PREDICTION POINT
A species at a place in a given survey year, under that year's conditions (first curation_comments bullet,
task_summary.known). Neither a place nor a year has a tow, so any column whose value depends on how this haul's tow
went is not known at that point (USE-3).

COLUMN TABLE (column | meaning | known at prediction? | dtype and cleaning | verdict | rule)

log1p_cpue_no_km2 (target)
  meaning: log1p of FOSS cpue_nokm2, the count over the area swept; a group's taxon is the sum over its codes;
    zero-filled
  known at prediction? the outcome
  dtype and cleaning: float, 0 to 14.05. The rebuild holds on all 201,731 counted catches (count / area_swept_km2 =
    cpue_nokm2, max relative error 1.6e-4, from the rounding of the area). area_swept_km2 = distance_fished_km x
    net_width_m to 1.6e-4 on all 35,561 hauls. The 128 catches weighed but not counted have no cpue_nokm2 (count and
    CPUE are missing together) and leave (CLEAN-15). No assertion of the rebuild in `_clean` (problem 1). log1p is
    allowed: the metric is an RMSE, not a deviance (CLEAN-16 as amended), and the denominator is not a feature
  verdict: fine; MET-14 gap
  rule: MET-14, CLEAN-15, CLEAN-16

taxon
  meaning: the row's taxon, one of 11 (three of them groups of species codes)
  known at prediction? yes; the question is asked per species
  dtype and cleaning: nominal category, 11 levels, none missing
  verdict: fine
  rule: MET-2 (feature kept)

taxon_group (scoring)
  meaning: a copy of taxon, the group of mean_group_normalized_rmse
  known at prediction? metric input only
  dtype and cleaning: category. Identical to taxon in all 391,044 rows, with the same 11 categories in the same order.
    Not in feature_cols, not a weight. `_feature_types` also lists it as categorical, which is harmless
  verdict: fine
  rule: MET-2 (reworded 2026-11-05)

srvy
  meaning: survey region (EBS, NBS, BSS, GOA, AI)
  known at prediction? yes (survey design)
  dtype and cleaning: category, 5 levels. With date, it carries the planned tow (30 min, or 15 min in GOA from 1996
    and AI from 1997)
  verdict: fine
  rule: MET-14 (planned part), USE-6

stratum
  meaning: srvy plus design stratum number; GOA 2025 placed in the 1984 strata
  known at prediction? yes (set before the tow)
  dtype and cleaning: category, 149 levels after the repair
  verdict: fine
  rule: CLEAN-21 (settled)

latitude
  meaning: start latitude of the haul
  known at prediction? yes (start, not end)
  dtype and cleaning: float, 51.19 to 65.34
  verdict: fine
  rule: LEAK-41 (the end position, which carries the tow length, is dropped)

longitude_east
  meaning: start longitude, 0 to 360 east
  known at prediction? yes
  dtype and cleaning: float, 170.60 to 227.23
  verdict: fine
  rule: CLEAN-12

date
  meaning: local date of the haul (the time of day dropped)
  known at prediction? yes (survey schedule)
  dtype and cleaning: datetime, 1982-05-29 to 2026-08-04; the time key of the split
  verdict: fine
  rule: (settled)

depth_m
  meaning: bottom depth; headrope depth in 1993-95
  known at prediction? yes (the place's bathymetry)
  dtype and cleaning: int, 9 to 1200, no sentinels
  verdict: fine (1993-95 note settled)
  rule: CLEAN-21 (settled)

bottom_temperature_c
  meaning: bottom temperature during the haul (point values to 1992, tow means after)
  known at prediction? yes, as that year's field at the place (settled 2026-11-02)
  dtype and cleaning: float, -2.1 to 15.3, 4.5% missing. One decimal everywhere, so no precision marks the tow.
    Missing in 10.4% of short tows against 4.2% of full tows, but within survey and year -0.009: the gap comes from
    the years, not the cut
  verdict: fine
  rule: LEAK-41 (no encoding of effort), LEAK-10

surface_temperature_c
  meaning: surface temperature during the haul
  known at prediction? as above
  dtype and cleaning: float, -1.1 to 18.1, 2.4% missing. Within survey and year, short tows -0.004
  verdict: fine
  rule: LEAK-41, LEAK-10

DROPPED HAUL COLUMNS THAT CARRY THE AMOUNT AT RISK (judged again under LEAK-41)

duration_hr
  meaning: realized tow duration
  known at prediction? no: realized, and cut early on large pollock catches
  verdict: drop right
  rule: LEAK-41, LEAK-10, USE-3

distance_fished_km
  meaning: realized distance towed
  known at prediction? no: a factor of the denominator
  verdict: drop right
  rule: LEAK-41

net_width_m
  meaning: realized net spread
  known at prediction? no: a factor of the denominator (correlation 0.26 with log depth)
  verdict: drop right
  rule: LEAK-41

area_swept_km2
  meaning: the target's denominator
  known at prediction? no
  verdict: drop right; never a weight either (MET-15: the decision is per cell of an equal-area map)
  rule: LEAK-41, MET-15

net_height_m
  meaning: realized net opening
  known at prediction? no
  verdict: drop right
  rule: LEAK-10

latitude_dd_end, longitude_dd_end
  meaning: end position
  known at prediction? no: with the start position, it encodes the distance towed
  verdict: drop right
  rule: LEAK-41 ("a column that encodes it")

performance
  meaning: post-tow code
  known at prediction? no: 20.6% of hauls with a positive code are short tows, against 3.5% with code 0
  verdict: drop right
  rule: LEAK-10, LEAK-41

CATCH count, weight_kg, cpue_kgkm2, taxon_confidence
  meaning: parts of the target, and the identification rating
  known at prediction? no
  verdict: never merged into the frame; right
  rule: MET-14, LEAK-10

Other dropped columns (vessel, hour, identifiers, survey copies): settled on 2026-11-01 and 2026-11-02. Nothing new.

THE EFFORT AS AN AMOUNT AT RISK (MET-14, LEAK-41): planned or realized, and does any feature carry the realized part

Planned part. The protocol sets the standard tow by region and era: median 0.50 h everywhere before 1996, then 0.27 h
in GOA and AI and 0.51 to 0.52 h in EBS, NBS and BSS. With the stratum's net and depth, this is the planned area
swept. Cross-fitted LightGBM with folds by year, from the shipped features (srvy, stratum, place, depth, temperatures,
year, day of year), predicts log(area_swept_km2) at R^2 0.819. The gain is stratum 0.59, srvy 0.22 and year 0.14.
So the planned part reaches the models through the region, stratum and date, as the notes say.

Realized part. The realized area swept over the median of its survey and year is predicted at R^2 0.103, and the
realized duration over that median at R^2 0.076. The 1,699 short tows (under 0.75 of the median duration of their
survey and year) are told apart at ROC AUC:
  all features              0.749
  without the temperatures  0.757
  the schedule alone        0.694  (srvy, year, day of year)
  the place alone           0.667  (srvy, stratum, latitude, longitude, depth)
  Short-tow share by depth: 3.3% at 0-50 m, 6.7% at 500 m and deeper.
The features predict the cut only through the place (rough or deep ground, more cut tows) and the year. Both are known
at the prediction point. This is risk selection, which LEAK-41 and USE-6 allow ("a feature known at the prediction
point that predicts the weight through risk selection stays"). No feature is set or cut after the prediction point:
- The temperatures add nothing to the AUC.
- No column marks the cut by its precision or missingness: one decimal everywhere, and the missingness gap is between
  years, not between short and full tows.
- The start position is kept and the end position dropped.
No column that encodes the realized effort ships.

The rule paths are consistent with the definition. The cut is located row by row (duration_hr), so the "fix it to the
length known at the start or remove it" branch of the LEAK-41 Cases row applies:
- Fixing it to the planned length needs no column: the planned length is a constant of region and era, already
  carried by srvy and date.
- Removing the cut rows is barred: LEAK-41 says no model is trained or scored on rows selected by the realized weight.
  Keeping all of FOSS's satisfactory hauls is therefore right.
- Declaring the area swept as the weight is barred by MET-15's equal-area clause, which the definition cites.
- MET-16: no design weight ships. The task is a habitat map, not a population estimate, so it is rightly unweighted.

PROBLEMS, RANKED BY principles.md

1. P7 quality, MET-14 (Should): `_clean` does not assert that the target times the denominator rebuilds the count.
   MET-14 asks for an assertion in `_clean`, and the definition reads cpue_nokm2 without one.
   Evidence: the rebuild holds on all 201,731 counted catches (max relative error 1.6e-4; area_swept_km2 = distance
   x width to 1.6e-4). The 128 uncounted catches lack both count and cpue_nokm2.
   Mildest remedy: in `_clean`, before the taxa are summed, merge area_swept_km2 into `catch` and assert the rebuild
   on the counted rows:
     np.allclose(cpue_nokm2 * area_swept_km2, count, rtol=1e-3)
   The frame does not change.

2. P6 meaning of the metric, MET-15/MET-2 (note): the unweighted density puts walleye pollock's cut tows into the
   score at four times their share of the rows. In the test years (2009 on), short tows are 3.4% of each taxon's rows
   and hold this share of the taxon's squared deviation from its mean:
     walleye pollock         14.0%  (11.0% of its top 1% of densities)
     Greenland turbot        10.1%
     shortspine thornyhead    7.0%
     the other eight taxa    3% or less
   Tows under half the median duration (256 hauls, 24 under 0.1 h, the shortest 1.5 minutes; 149 of the 256 have
   performance code 0) hold 2.2% of pollock's squared deviation.
   This is the bias of the cut that the notes accept, as NOAA's index does. It is not a reason to change the rows
   (LEAK-41) or the weighting (MET-15).
   Mildest remedy: one sentence with these shares in the "Effort, the survey's exposure" bullet, so a reader knows
   how much of pollock's (and Greenland turbot's) vote rests on short tows.

3. No other problem. The claims of issue 4 hold on the raw tables (verify_effort.out, rerun here):
   - pollock's short tows sit +0.357 over all hauls, against -0.360 to +0.077 for the other taxa;
   - among hauls with a catch, the within-cell residual is +0.551 for pollock and 0.002 to 0.249 for the others;
   - 9 of 11 taxa are higher by the raw means, 11 of 11 within the cells;
   - on the EBS shelf, pollock tows under 0.4 h: 831, mean 8.33 against 7.35 log1p kg/km^2.
   The planned-effort medians in the notes match the data.

Judgment record
  Validity: no leak. LEAK-41 holds: the realized effort is predicted only through place and year
    (realized area ratio R^2 0.10; short tows AUC 0.75, 0.757 without the temperatures). USE-6 risk selection.
  Value: MET-15 unweighted is right (equal-area map). MET-16: no design weight. Pollock's cut tows hold 14% of its
    squared deviation (note).
  Quality: MET-14: assert the rebuild in _clean (holds to 1.6e-4). CLEAN-16: log1p fine under RMSE. Dtype probe
    clean. taxon_group an exact copy.

</details>

<details><summary>Split audit</summary>

Split auditor: noaa_afsc_bottom_trawl_survey_cpue (exposure re-review, 2026-11-06, full tier)

VERDICT: right with notes. The 2026-11-06 change (taxon_group copy, tow cut claimed for pollock only, effort kept out,
unweighted density) does not touch the split, and nothing new breaks a Must of P4. One note is new: the tow cut does
not read the same on both sides in the eastern Bering Sea. It is a training-history effect of 1989-2008 and costs
nothing measurable, so the remedy is one sentence in the notes, not a filter.

How measured: the definition's frame and its nine splits, loaded with dataset_io.from_definition.
The dropped haul columns (hauljoin, station, duration_hr, area swept, performance) were joined back one-to-one from
_clean with the drop list emptied, keyed on taxon, position, date, depth, target and stratum (0 duplicate keys).
"Short tow" is the definition's own cut: under 0.75 of the median duration of its region and year. The model is
untuned LightGBM (400 trees, lr 0.05, 63 leaves, one seed) on log1p, with the shipped features plus year and day of
year. It is scored with mean_group_normalized_rmse, reimplemented from the spec (expm1, clip at 0, RMSE per taxon over
the taxon's std, mean). These are probe numbers, not leaderboard numbers (EV-8).

JUDGMENT RECORD
Validity: SPLIT-1/SPLIT-3 hold (temporal, Andrej's pick of 2026-11-02, settled). SPLIT-9 holds: no training row is
  admitted by its cut, and no weight ships. SPLIT-10 exception, settled: no gap. SPLIT-11 and SPLIT-14 hold: expanding,
  train 54.0%-95.4%. SPLIT-12 holds (the two-year survey cycle). SPLIT-13 holds (stations recur; known waters).
  SPLIT-20: note (the cut's history differs by era). SPLIT-23 holds (no haul is split across a cutoff).
  LEAK-41 is not a split issue here.
For the curator: nothing to decide. One optional sentence for the effort note (problem 1).

WINDOWS (re-verified on today's frame, 391,044 rows)
window  train years  test   train rows (share)  test rows  test hauls  regions in test
0       1982-2024    25-26  373,005 (95.4%)     18,039     1,640       EBS 700, GOA 431, AI 372, NBS 137
1       1982-2022    23-24  354,619 (90.7%)     18,386     1,672       EBS 726, GOA 523, AI 307, NBS 116
2       1982-2019    21-22  333,018 (85.2%)     21,601     1,964       EBS 752, GOA 526, AI 398, NBS 288
3       1982-2018    2019   321,394 (82.2%)     11,624     1,057       GOA 537, EBS 376, NBS 144 (no AI)
4       1982-2016    17-18  301,045 (77.0%)     20,349     1,850       EBS 752, GOA 535, AI 420, NBS 143
5       1982-2014    15-16  277,802 (71.0%)     23,243     2,113       GOA 767, EBS 752, AI 419, BSS 175
6       1982-2012    13-14  259,007 (66.2%)     18,795     1,709       EBS 752, GOA 547, AI 410
7       1982-2010    11-12  236,723 (60.5%)     22,284     2,026       EBS 752, GOA 665, AI 420, BSS 189
8       1982-2008    09-10  211,119 (54.0%)     25,604     2,328       GOA 817, EBS 752, AI 418, BSS 200, NBS 141
- Hauls split across train and test: 0 in every window, so a haul's 11 taxa stay together (the hidden group of one
  haul holds).
- Gap: 0 years everywhere except window 2, where the missing 2020 survey makes a de facto one-year gap. This matches
  splits_comment.
- Stations revisited, as part of the task (SPLIT-13). Test hauls at a station id seen in training: 72.4% / 91.1% /
  92.3% / 84.5% / 89.2% / 86.5% / 87.4% / 85.0% / 72.9%. The EBS is 100% in every window. GOA is 0% in window 0
  because the 2025 redesign renamed its stations, and 52-75% elsewhere. NBS is 0% in window 8 (its first survey,
  2010).
  By place, test hauls within 5 km of a training haul: window 0 97.9% (GOA 2025: 94.4%), window 1 98.7%, window 8
  86.3%. The splits_comment line "most test hauls are at a station seen in training" holds on both readings.

PROBLEMS, RANKED (principles.md: P4 first; nothing here reaches a Must)

1. The tow cut reads differently on the two sides in the EBS (P4, SPLIT-20 Should: a break in the history; new, from
   today's claim). Rows here are hauls x 11 taxa.
   Share of hauls that are short tows:
   - training sides: 4.8% (window 0) to 6.0% (window 8);
   - test windows: 2.4% to 5.2%.
   The excess sits in old training-only years:
   - EBS 1989-1992: 15.8-22.8% of tows short, against 1-5% since 2009; 13.8% of those years' tows ran 0.3-0.4 h;
   - GOA 1990: 15.7%; AI 1991: 24.8%.
   Pollock's short tows against their stratum-year cell (log1p numbers per km^2, cells holding both short and full
   tows):
   - pooled: every training side +0.35 to +0.40 (1,120-1,589 tows); the test windows -0.24 to +0.92 on only 25-87
     tows each, +0.30 pooled over the nine. So pooled, the cut reads alike on both sides;
   - by region it does not. EBS 1989-1992 +0.71 (269 tows) and 1993-2008 +0.71 (330), against +0.07 since 2009
     (156 tows, the only EBS short tows any test window holds). In the test years the pollock excess comes from AI
     (+0.39, 218 tows) and GOA (+0.73, 75 tows).
   The dataset.py figures "+0.36 over all hauls" and "EBS tows under 0.4 h (831) average 8.33 against 7.35" are
   therefore mostly the training history of 1989-2008.
   Effect on the score:
   - dropping every short tow from the training sides: mean metric 0.9049 -> 0.9036 (-0.0013; better in 5 of 9
     windows; per-window swings of +/-0.02 are single-seed noise);
   - scoring the shipped model on the full-length test tows only: 0.9019 against 0.9049 (lower in 8 of 9 windows).
   So the cut rows add a little irreducible error to the test windows. Training on them neither helps nor hurts.
   Rule: SPLIT-20 (check the history for a change in the data collection). The cut is a property of the label (LEAK-10,
   resolved as claimed for pollock), not of which rows a window admits.
   Mildest remedy: none to the split. Optionally, one clause in the effort bullet, for the claim auditor and the
   mediator to word: "the pollock cut sits mostly in the EBS hauls of 1989-2008 (+0.71 on log1p within their cells),
   training rows in every window; in the test years it shows in the Aleutians and the Gulf (+0.39, +0.73), not on the
   EBS shelf (+0.07)". A filter on short tows is not warranted (no gain, and it would cut the label the review itself
   uses, as NOAA's index keeps those tows).

2. Per-region tow lengths: the 30-minute era is on the training side only (P4, SPLIT-20; holds, a note at most).
   - GOA 1990 and 1993 and AI 1991 and 1994: 2,186 hauls (24,046 rows) of 30-minute tows. They are training rows in
     every window and appear in no test window. The 15-minute standard started in GOA 1996 and AI 1997.
   - Median tow length by side: GOA train 0.272-0.280 h, test 0.263-0.276. AI train 0.270-0.271, test 0.262-0.273.
     EBS train 0.500-0.502, test 0.512-0.528 (EBS tows have lengthened slightly since about 2009: medians 0.506-0.528
     against 0.500-0.510 before). BSS 0.519 against 0.511; NBS 0.512 against 0.518.
   - Share of training hauls at 30 minutes in GOA/AI: 15.5% (GOA) and 14.1% (AI), averaged over windows; 0.1% and 0%
     on the test sides.
   Effect: training without the 30-minute-era rows changes the mean metric from 0.9049 to 0.9037 (-0.0011; better in
   5 of 9), which is noise.
   The density folds the area swept in, and the date and region carry the era. The definition's "the planned effort
   reaches the models through the region and the date" holds on the split.
   Rule: SPLIT-20 (the source itself trains on 1982-2019 with both tow lengths, TM-459 p. 5).
   Remedy: none. Optionally say in the effort bullet that the 30-minute GOA/AI tows are training rows only.

3. Time on risk and window cutoffs (SPLIT-9, LEAK-41; holds). No training weight ships, and the realized effort is no
   feature. A tow is cut at sea on the haul's own date, so a training side admits a haul by its survey date, never by
   its length or its early end. Each window holds whole summer seasons. Unlike pricing_game_2016_french_fleet, no
   window admits rows by their early end. No training row's label was unknown at its window's start: FOSS publishes a
   season before the next one, as settled in issue 2. The unrated 2026 season (722 hauls, 44% of window 0) is test-only
   and already a note (EV-7).

4. Settled points re-checked; still hold, no new evidence:
   - the regime (temporal over grouped by station, issue 2);
   - no gap (the SPLIT-10 exception);
   - the window floor: the oldest window trains on 54.0%, and a tenth window (2007-2008) would train on 49%;
   - window 3 holds only 2019 and no Aleutian survey;
   - the slope survey (BSS) is tested in windows 5, 7 and 8 only;
   - the EBS grid fell from 376 to 350 stations in 2024, and all 350 were sampled before;
   - the GOA 2025 stratum repair (window 0's GOA hauls carry 1984-design strata, as the training rows do).

CANNOT VERIFY
- Why 14-23% of EBS tows of 1989-1992 ran 0.3-0.4 h (a cut on catch, or a protocol or gear trial of those years).
  The pollock excess there (+0.71) reads like a cut, but the source documents were not re-read for it.

</details>

<details><summary>Domain practitioner</summary>

Domain practitioner, noaa_afsc_bottom_trawl_survey_cpue, exposure re-review (2026-11-06, full tier)
Actor: an AFSC habitat analyst fitting the five-year EFH species distribution models. Builds on the panel block of
2026-11-01 in REVIEW.md. Only what is new, changed or still open under MET-14/15/16, LEAK-41 and the issue 4
resolution is reported here.

VERDICT
- Fit: approximate (unchanged; agree with fit="approximate"). This is the review's model-selection step: haul
  densities scored against the next survey cycle. It is not the review's per-region, per-life-stage map from
  long-term habitat rasters (USE-8; no other use case makes it direct, USE-9).
- The exposure decision (issue 4, option A) is right for my use. I map a density, I score hauls unweighted, and I keep
  the short tows as GAP does. One stated reason is wrong (finding 2) and the LEAK-41 ceiling is not stated (finding 4).
  Both are text fixes.
- Metric: scores my decision MOSTLY / partly, an upgrade from the "partly" of 2026-11-01. The 11-taxon mean of
  RMSE/sd is the source's RMSE taken per species, one vote per species map (MET-1, MET-5). Scoring it per taxon x
  region or with design weights picks the same winner in 4 of 4 windows (tau 0.81-1.00). Keep it, no change.

ANSWERS TO THE QUESTIONS ASKED
1. Inputs for a species at a place in a survey year (USE-3, USE-6)
   - I have these: the taxon, region, design stratum, position, date (set by the survey schedule) and depth.
   - The year's temperatures come from the haul's own readings. They stand in for the year's field, as settled
     2026-11-01; they carried no measured gain.
   - I do not have the realized effort at a cell nobody towed: tow duration, distance, net width and height, area
     swept, end position. Leaving them out is right (USE-3, LEAK-41).
   - The planned effort is the standard tow: 30 min in the Bering Sea, 15 min in the GOA from 1996 and the Aleutians
     from 1997. It is fixed by region and era, so region and date carry it. Nothing is missing that I would always
     have, beyond the habitat rasters already named in fit_reason.
2. Is the CPUE with the area swept folded in the quantity I map? Yes (MET-14, USE-5).
   - Every AFSC product works on catch per area swept:
     - the design-based index (gapindex: R_ijk = W_ijk / E_ij, numbers S = N / E);
     - the 2022 EFH models (numerical abundance with an area-swept offset, TM-459 pp. 16-17);
     - the model-based indices (an area-swept offset).
   - The map is predicted abundance per raster cell, so it is a density times the cell area.
   - The target is the right quantity. Dropping the count as part of the target is correct (LEAK-10).
3. Weight hauls by effort, or score them unweighted? Unweighted (MET-15, MET-16).
   - Weighting by area swept has no decision meaning for me.
     - Within a region the area swept barely varies, apart from the cuts.
     - Across regions it would only halve the weight of every GOA and Aleutian haul, because their tows are 15 min.
       That regional reweighting is not a choice any EFH memo makes.
     - The exposure study found that count RMSE and density RMSE rank models alike (tau 0.80-1.00, same winner 5/5).
   - The other candidate is the design weight: stratum area / hauls in the stratum, the gapindex expansion. It turns
     haul means into area means.
     - EFH is not a population estimate, so MET-16 says unweighted, and the source's RMSE is unweighted over stations
       (TM-459 p. 21).
     - My probe: a design-weighted per-taxon normalized RMSE ranks 7 models like the declared score, tau 0.905 /
       1.000 / 1.000 / 0.810 on the 4 newest windows, same winner in all 4. So unweighted costs nothing in ranking.
4. A tow cut short (the pollock note; LEAK-10, LEAK-41)
   - I keep short tows, as GAP does. They are satisfactory hauls, standardized by area swept, and enter the stratum
     mean with equal weight.
   - Dropping them would remove the densest pollock aggregations and bias pollock density down. LEAK-41 also forbids
     training or scoring on rows selected by the realized weight.
   - The tow length is a stop on the catch only for pollock: +0.36 log1p over all hauls in its cells, against -0.36 to
     +0.08 for the other taxa. That matches survey practice (a tow on a dense pollock sign is hauled back early to
     spare the net).
   - The README table shows the other taxa's +0.00 to +0.25 among hauls with a catch. A smaller area turning one
     caught fish into a higher density explains that.
   - For scoring:
     - short pollock tows are 25-84 of 1,057-1,964 pollock test rows per window (1.5-5.1%);
     - they are true high densities with a small stopping-rule bias, which the design-based index carries too;
     - keeping them unweighted is what I would do.
5. Does the metric, scored per taxon group, score my decision? Mostly.
   - What is right:
     - The review selects and weights its models by the RMSE of abundance at stations, one species (and life stage
       and region) at a time (TM-459 pp. 20-21).
     - Per-taxon RMSE over the taxon's spread, averaged, gives each species map one vote. Within a taxon it ranks as
       the source's RMSE does.
     - Moving the group to the scoring column taxon_group changed no score: my re-implementation equals the declared
       scorer to 4 decimals on 4 windows (MET-2, MET-13).
   - Still open, but small:
     - The source scores per region. Inside a taxon one region often holds the error. Newest window, LightGBM L2 on
       log1p, share of the squared error:
         - Dover sole: 100% GOA;
         - Lepidopsetta: 100% EBS;
         - rex sole: 86% GOA;
         - Atheresthes: 90% GOA;
         - pollock: 47% EBS and 47% GOA.
     - A taxon x region mean ranks the 7 models at tau 0.905 / 0.905 / 1.000 / 0.905 against the declared score,
       with the same winner 4/4. The concern of 2026-11-01 (GOA holding 71-92% of a pooled rex sole RMSE) no longer
       changes the ranking once the score is taken per taxon.
   - Metric I would choose: the declared one. A taxon x region average would be closer to the memos (MET-1, MET-2),
     but it ranks the same and needs srvy as a second scoring column. Not worth the change.

FINDINGS (ranked by how much they change the task)
1. [settled, not reopened] The decision unit is a per-region, per-life-stage percentile map from 38-year mean
   rasters. The task scores the model-selection step at hauls (USE-8). Already in fit_reason.
2. [new, wording; MET-15] The exposure note and REVIEW issue 4 justify the unweighted score "as the review maps it
   over cells of equal area". Test hauls are not equal-area cells. In 2015-2026 the hauls per 1,000 km^2 per
   stratum-year are:

     | Region | p10 | p50 | p90 | p90/p10 |
     |---|---|---|---|---|
     | EBS | 0.67 | 0.73 | 1.08 | 1.6 |
     | GOA | 0.91 | 1.66 | 3.64 | 4.0 |
     | AI | 1.55 | 5.22 | 14.63 | 9.4 |

   GOA and AI allocate stations by stratum, not by area. The right reasons for an unweighted score:
   - the source's station RMSE is unweighted (TM-459 p. 21);
   - EFH is not a population estimate (MET-16);
   - the stratum-area design weight ranks the models the same (tau 0.81-1.00, same winner 4/4).
   Mildest remedy: reword the clause to "scored unweighted over hauls, as the source's RMSE at the stations; a
   stratum-area design weight ranks the models the same".
3. [carried over, trust] Models fit on log1p and inverted predict only 34-51% of the test mean density (LightGBM L2,
   4 windows). The declared RMSE still prefers them to a Tweedie fit on counts in 2 of 4 windows:
   - newest window: 0.932 against 0.859 (Tweedie better);
   - window 3: 0.917 against 0.931 (log1p better).
   The EFH encounter threshold, 1 - exp(-lambda) >= 5%, uses the absolute mean. A method's mean bias therefore matters
   to me even where RMSE is mild about it (MET-3, MET-8). This is a property of the source's metric, not a data error.
   No change; a note would help users.
4. [new, LEAK-41 Must, report gap] LEAK-41 asks the definition to state the score of 1/weight alone as the ceiling a
   leak would reach. The notes give the L2 and Poisson gains of the effort columns (0.0028 and none), but not the
   ceiling. My measurement (LightGBM on taxon + 1/area_swept, haul join matched 99.7%):

     | Window | taxon + 1/area | taxon mean |
     |---|---|---|
     | 1 | 1.0319 | 1.0394 |
     | 2 | 1.0311 | 1.0418 |
     | 3 | 1.0317 | 1.0453 |
     | 4 | 1.0452 | 1.0568 |

   The honest LightGBM scores 0.92-0.93. The ceiling is tiny (0.007-0.014), and part of it is region, since GOA and
   AI tows are half as long. Add one sentence with these numbers; no other change.
5. [settled] Life stages are pooled (FOSS has no lengths), and 11 taxa sit in one table with taxon as a feature.
   Unchanged.

WHAT AN EXPERT WOULD CHANGE
- Reword the reason for the unweighted score (finding 2). Add the 1/area ceiling sentence (finding 4).
- Keep:
  - the density target;
  - the dropped effort;
  - the short tows in the data;
  - the unweighted per-taxon score;
  - taxon_group as the scoring copy.
- Optional: a note in the metric block that log1p fits inverted underpredict the mean 2-3x, which matters for the
  EFH encounter threshold.

SOURCES
- gapindex "Background equations": unweighted haul mean of CPUE within a stratum, stratum-area expansion, area swept
  only as the CPUE denominator.
  https://afsc-gap-products.github.io/gapindex/articles/background_equations.html
- Laman et al. 2022, NOAA-TM-AFSC-459 (pp. 3, 8, 16-21, 27-28), as cited in the definition and read by the
  2026-11-01 panel. https://repository.library.noaa.gov/view/noaa/48659
- Barnes, Essington, Pirtle et al. 2022, Ecography e06189 (retrospective skill tests).
- AFSC survey reports found by web search: the standard 30-min tow at 3 knots on the shelf. No public text on early
  haulback for pollock was found, so that practice is my judgement and is backed by the data (README decision 4).
- Definition, README and REVIEW.md issue 4. Rules: use_case.md (USE-3, USE-5, USE-6, USE-8, USE-9),
  metrics.md (MET-1, MET-2, MET-3, MET-5, MET-8, MET-13 to MET-16), leak_checks.md (LEAK-10, LEAK-41).
- My probes (untuned LightGBM, 4 newest windows):
  - probe.py / probe.out: declared vs taxon x region vs design-weighted scores, sampling intensity, region shares of
    error;
  - probe2.py / probe2.out: the 1/area ceiling and the short pollock tows in test.

</details>

<details><summary>Blind review</summary>

BLIND REVIEW: noaa_afsc_bottom_trawl_survey_cpue
Reviewer worked only from the clean-room data and task card (data.parquet, task.md) and the public web. No other local files were opened.

VERDICT: Include with small changes. This is a real, honest, non-trivial species-distribution regression task, but the card should state the haul-by-taxon structure and the "in-situ covariates" framing, and the 2026 rows should be flagged as possibly provisional.

WHAT THE TASK IS
The data come from NOAA AFSC groundfish bottom-trawl survey hauls (FOSS haul, catch and species tables). Each haul is zero-filled over 11 groundfish taxa: pollock, cod, halibut, sablefish, Dover sole, rex sole, Greenland turbot, shortspine thornyhead, and the Atheresthes, Hippoglossoides and Lepidopsetta groups. The surveys are EBS, NBS, GOA, AI and BSS, from 1982 to 2026.
- Target: log1p(numbers per km2 swept).
- Features: taxon, survey, stratum, latitude, longitude, depth, bottom and surface temperature measured during the haul, and date.
- Use: a species-distribution model (SDM) that predicts a taxon's density at a station from habitat covariates in a later survey year. Such models feed essential-fish-habitat maps, distribution-shift studies and model-based abundance indices (sdmTMB/VAST style). This is a real use, but it is spatial-temporal SDM transfer, not an operational forecast made before the survey.

KEY NUMBERS (200k-row sample)
- 35,544 distinct haul keys, about 5.6 rows each in the sample. The full data has 391,044 rows / 11 = about 35,549 hauls, so every haul has all 11 taxa.
- No duplicate rows and no duplicate haul-taxon pairs.
- 52% of target values are zero. The zero share is stable across years: EBS 0.47-0.55, GOA 0.42-0.51, AI 0.56-0.63, NBS 0.66-0.74.
- Smallest positive CPUE: 13.5 no/km2, which fits one fish over about 0.07 km2. Largest log1p value is 14.0 (pollock).
- Strata are all survey-prefixed (e.g. EBS-31), 149 levels. No experimental stratum 0. Every stratum seen at test time from 2019 on also appears in training.
- Depth runs 9-1200 m (BSS reaches 1200, consistent with the slope survey). Latitude 51-65 N, longitude east 170.6-227.2. Both are plausible.
- Temperatures: bottom NaN 4.5%, surface NaN 2.4%. Missingness is concentrated in 1990-91 (about 45%, early GOA/AI years) and is near 0 after 2010.
- LightGBM with year and day-of-year added, trained on years before the cut and scored on the cut year onward:

  | Cut  | LightGBM R2 | RMSE | taxon mean R2 | taxon x stratum mean R2 |
  |------|-------------|------|---------------|-------------------------|
  | 2015 | 0.734       | 1.82 | 0.31          | 0.66                    |
  | 2019 | 0.768       | 1.70 | 0.33          | 0.68                    |
  | 2023 | 0.778       | 1.65 | 0.34          | 0.69                    |

  Dropping taxon: R2 falls to about 0.04. Dropping srvy and stratum: R2 is about unchanged (lat/lon/depth stand in for them).
  So there is clear signal and a non-trivial gain over a strong lookup baseline (about +0.09 R2). Room for methods to differ.

CONCERNS (most to least serious)

1. Long format: 11 rows per haul with identical covariates, and taxon dominates. (moderate)
   Evidence:
   - Each haul appears as 11 rows that differ only in taxon. Without taxon, R2 is about 0.04.
   - A taxon x stratum mean lookup already gets R2 0.68.
   Effects:
   - The effective number of independent sampling units is about 35.5k hauls, not 391k rows.
   - Errors are correlated within a haul. A cluster of very large or zero catches in one haul moves 11 rows together.
   - The temporal split keeps whole hauls on one side, so this is not leakage. It does inflate the apparent size and makes the benchmark mostly a test of taxon-by-habitat interactions.
   Change:
   - Say so in the task card.
   - Keep a haul identifier (not as a feature) so that any non-temporal resampling can group by haul.
   - Alternatively, consider a wide multi-output version. Keeping the long form is defensible: it is a joint SDM.

2. Prediction-time framing: the temperatures are measured during the same tow as the catch. (moderate, mostly documentation)
   Evidence: FOSS metadata defines BOTTOM_TEMPERATURE_C as "Bottom temperature (tenths of a degree Celsius); NA indicates removed or missing values". It is recorded at the haul, as are depth and date.
   - For SDM use (predicting density given observed habitat) these are legitimately known.
   - For a "forecast next year's catch before the survey" use they are not. You would only have climatology or ocean-model output.
   This is not target leakage, but the task should be framed as habitat-conditional prediction in future years, not as a forecast.
   Change: state the framing. Optionally provide a variant without in-situ temperatures.

3. Possible confusion of "count not recorded" with zero. (low-moderate; could not verify)
   The FOSS catch COUNT field is described as "Total whole number of individuals caught in haul or samples collected". The documentation found does not say how missing counts are handled. The public zero-fill example sets null CPUE to 0.
   - If a haul had weight but no count for a taxon, zero-filling would turn it into a false zero.
   - Indirect evidence against a systematic problem: zero rates are flat across 1982-2026 within each survey, and positive values start at a one-fish level.
   Change: when preparing the data, drop or flag haul-taxon rows where CPUE_KGKM2 > 0 but CPUE_NOKM2 is null, instead of setting them to 0. Confirm this was done.

4. Survey composition shifts over time, so test windows differ in mix. (low)
   - BSS (slope) exists only in 2002-2016.
   - NBS appears only in 2010, 2017, 2019 and 2021-2025.
   - GOA is surveyed in odd years and AI in even years from 1991/1990 on.
   - No 2020 survey (COVID).
   With 9 temporal windows, the late windows have no BSS and alternate GOA and AI. Per-window scores therefore differ partly by region mix, not only by method skill.
   This is acceptable and realistic. Just know that window-to-window variance includes this.

5. 2026 rows may be provisional. (low)
   The 2026 hauls (AI and EBS, 2026-06-01 to 2026-08-04) are three months old. FOSS data from the current year can be revised after final QA.
   Change: record the download date or version. Consider ending at 2025, or re-pull before freezing.

6. Minor preparation notes. (low)
   - Types are sensible: taxon, srvy and stratum are categorical; date is datetime; NaN is kept natively for temperatures.
   - longitude_east is converted to 0-360 sensibly, so it does not jump at the dateline (AI spans 170.6-194.9).
   - Time of day was dropped. It could matter for diel behaviour (pollock, cod) but is not essential.
   - stratum is nested in srvy (100% prefix match), so srvy is partly redundant. That is harmless.
   - Area swept, vessel, gear and haul performance are not included. CPUE is already area-standardised, so this is fine.

WHAT I COULD NOT CHECK
- The full 391,044 rows. I only had the 200k sample, so the haul completeness of 11 rows each is inferred from 391,044 / 11 and the sample.
- The exact boundaries of the 9 test windows (my cuts were by year, as a stand-in).
- The raw FOSS pull. I could not see whether weight-only or null-count rows were zero-filled, or whether haul-performance / standard-haul filtering was applied.
- Whether the 2026 values match the current FOSS release.
- The akgfmaps strata geopackage was not inspected.

SOURCES READ
- https://afsc-gap-products.github.io/gap_products/content/product-metadata-column.html
- https://github.com/afsc-gap-products/gap_products
- Web search results describing FOSS zero-filled data and zero-fill join code (afsc-gap-products.github.io foss-oracle-r / foss-api-r pages).

</details>

<details><summary>Task gamer</summary>

TASK GAMER REPORT - noaa_afsc_bottom_trawl_survey_cpue (log1p catch numbers per km2, 11 taxa, 9 temporal windows,
metric = mean over taxa of count-scale RMSE / SD, lower is better)

VERDICT: I could not game it. No exploit beat the noise floor. The kit has no effort columns (area swept, duration,
performance), no haul id, and no haul spans the train/test cut. The rows that share a haul carry no label at test time.

Honest baselines (LightGBM, 300 trees, lr 0.05, 63 leaves; date as day number + year + day of year; 01_baseline.py)
  log1p L2, predicted then expm1 ........ 0.9112  (per split 0.879-0.935)
  Tweedie(1.5) on counts ................ 0.8976  (0.837-1.027)
  L2 on raw counts ...................... 1.4108  (unstable; dominated by huge pollock hauls)
Noise floor (Tweedie): + random column 0.8938 (-0.004); other seed + subsampling 0.9032 (+0.006); per-split swings up
to 0.08. The metric is count-scale RMSE, so a few extreme hauls dominate it. Treat any mean change under ~0.01 as noise.

EXPLOITS RANKED BY GAIN (none clears noise)
| # | Exploit | Script | Honest | Exploited | Gain (mean; per split) | Deployed model has it? | Fix |
| 1 | Hauls per survey-year / per stratum-year counted over the test window | 03_attacks.py | 0.8976 tw / 0.9112 log | 0.8882 / 0.9104 | -0.009 / -0.001; splits -0.06..+0.02 | Mostly yes (survey design is known in advance) | none needed |
| 2 | Station history that uses labels of the first test year for second-year rows | 06_history.py | 0.8699 tw (honest history) | 0.8664 | -0.0035 over honest history | No (labels from within the test window) | not needed; the gain is noise |
| 3 | Hauls per survey day (effort/pace proxy) | 03_attacks.py | 0.8976 / 0.9112 | 0.8930 / 0.9086 | -0.005 / -0.003 | Yes once the survey is done | none |
| 4 | Distance to nearest haul the same day | 03_attacks.py | 0.8976 / 0.9112 | 0.8917 / 0.9112 | -0.006 / 0.000 | Yes | none |
| 5 | Rows per haul (10 vs 11 taxa; a taxon row dropped) | 03_attacks.py | 0.8976 / 0.9112 | 0.8962 / 0.9126 | -0.001 / +0.001 | n/a | none |
| 6 | Day rank within survey year | 03_attacks.py | 0.8976 / 0.9112 | 0.8965 / 0.9080 | -0.001 / -0.003 | Yes | none |
| - | All haul/effort features together | 03_attacks.py | 0.8976 / 0.9112 | 0.9025 / 0.9107 | +0.005 / -0.001 | | |

FLAWS THAT HURT AN HONEST MODEL (small)
| What | Honest choice | Baseline | Honest choice score | Fix |
| Old training years (1980s-90s; gear/survey changes) dilute the fit | train on the last 15 years only | 0.9112 log / 0.8976 tw | 0.9054 / 0.8732 (-0.006 / -0.024; tweedie per split mixed) | none; it is a modelling choice, not a task defect |
| Train >=1990 | | 0.9112 / 0.8976 | 0.9088 / 0.8885 | |
| Train only on regions present in the test window | | 0.9112 / 0.8976 | 0.9098 / 0.8849 | |
Better honest model: a station-history feature (mean same-taxon catch at the 8 nearest hauls of the previous 6 survey
years, capped at the last training year) gives 0.8985 log (-0.013) and 0.8699 Tweedie (-0.028). That is signal: a
deployed model has past survey catches. Fitting on the count scale (Tweedie) instead of log1p L2 is also honest. It
gives -0.014 on average but is unstable per split.

MECHANISMS
- Shared hauls: each haul gives 11 rows (one per taxon) with identical lat/lon/date/depth/temps (35,561 hauls;
  389,928 rows in complete hauls, 1,116 rows in hauls with 7-10 taxa). The split is by date, and every haul lies on one
  side of the cut (train ends 2024-08-05, test starts 2025-05-27, and so on), so a test row never sees a co-haul label.
  Rows per haul does not predict the target: positive rate 0.48 for 10- and 11-row hauls, with smaller groups too
  small to read.
- Effort columns: area_swept_km2, duration_hr, performance and the haul id are absent from the kit. Hauls per day,
  distance to the same-day neighbour and day rank are the only effort proxies left. They shift the mean by 0.001-0.006,
  which is inside the noise.
- Test-window history: a 2-year test window lets the second year's rows use the first year's labels. That gains only
  0.0035 over the honest history feature, which is noise.

NOTHING FOUND
- Formats: temperatures always 1 decimal; depth always integer; lat/lon decimal count (1-5) vs target: positive rate
  0.46-0.53 with no trend (small groups at 1-2 decimals).
- Missing temperatures: bottom NA 17,571 rows, positive rate 0.484 vs 0.480; surface NA 9,436 rows, 0.486 vs 0.480.
- Row order: rows are sorted by date and shuffled within date. Corr(position, y) = -0.010; next-row agreement 0.510 vs
  0.501 by chance, the same within a date (shared haul conditions). Within-date position vs residual: corr -0.0006.
- Copies across the split: only 1 coordinate pair recurs on two dates; no exact duplicate hauls across train/test.
- Transforms over all rows: none; raw units throughout.
- Train vs test: separated only by date (temporal by design).
- Source lookup: the rows could be joined back to the public FOSS haul/catch tables (lat/lon/date are exact), which
  would recover the catches. Every public dataset allows that, so it is not ranked and was not done.
- Web: no competition, forum or leak thread exists for this dataset. FOSS docs confirm that cpue_nokm2 = count /
  area_swept_km2 and that the catch table is zero-filled. The kit drops area_swept, duration and performance, so the
  effort leak is closed.

COULD NOT CHECK
- Whether the 1,116 rows in incomplete hauls were dropped because the count was NA while weight was present. The kit
  has no weight column. It does not matter for scoring: dropped rows are not scored, and nrows gives no gain.
- Whether the source positions are tow start or midpoint. A "tow cut short" signal would need both ends.

</details>

<details><summary>Precedent check</summary>

Precedent check: noaa_afsc_bottom_trawl_survey_cpue, issue 4 (resolved 2026-11-06, Lennart).

**Verdict**
None of today's three decisions departs from a rule without giving a reason, so no reflection prompt is needed.

- **The copy of `taxon`:** consistent with the precedent.
- **Dropping the tow's effort:** consistent with the precedent.
- **Scoring the density unweighted:** departs from the wording of the LEAK-41 time-on-risk Cases row, and gives a reason. The reason is MET-15's own equal-area-map clause. That clause is a Must and is more specific than the Cases row, so the exception is reasonable. It is not written into the Cases row yet (optional recording question at the end).
- **The pollock-only cut claim:** argued from the data, and the numbers check out. Two links in the argument are asserted, not tested (section 4).

**1. `taxon_group`, the metric's copy of the feature `taxon` (MET-2): consistent**
- **Precedent:** liberty_mutual_fire_peril_loss_cost. `var11` stays a feature and its copy `var11_weight` is the weight scoring column. Andrej decided this on 2026-11-02 and Lennart added the copy on 2026-11-05 (metrics.md Patterns row; liberty_mutual_fire_peril_loss_cost's `dataset.py`). MET-2 as reworded on 2026-11-05 names this dataset's taxon itself.
- **Differences:** none that matter. The role is `group` instead of `weight`, and the rule covers both.
- **Siblings without a copy:** huesken `target_gene`, micro_mass `Strain`, protein_model_quality `protein_id`, numerai `era` and sat11 `instance_id` all read their task's own split group, which MET-2 allows. Here the split is temporal, so `taxon` is not the task's group and the copy is needed.
- **Drift:** none. The CC explicitly supersedes Andrej's 2026-11-02 reading under the older MET-2.

**2. Realized effort dropped from the features (USE-3, LEAK-41, LEAK-10): consistent**
The dropped columns are duration, distance, net width and height, area swept and the end position.
- **Precedents:**
  - fremtpl2 and bemtpl97 (LEAK-41 Cases, 2026-11-06): the denominator is never a feature.
  - wadden_sea_sibes_macoma_abundance: `total_surface_m2` dropped under USE-3, an unsampled place has no core (column table).
  - boreal_postfire_lichen_biomass: quadrat area, nothing to drop (REVIEW.md, 2026-11-06).
- **Panel evidence (column auditor):** the features predict the realized area swept only at R^2 0.10, and short tows at ROC AUC 0.749 (0.757 without the temperatures), through place and year only. That is risk selection, which LEAK-41 and USE-6 allow.

**3. Unweighted score on the density (MET-15): departs with a stated reason, reasonable under the ranking**
- **The rule text it departs from:** the LEAK-41 Cases row on time on risk (amended 2026-11-06, Lennart) has three branches:
  - the cut can be located row by row: fix it to the planned length or remove it;
  - it cannot be located and the amount is the target's denominator: ship the rate, with the recorded amount as weight scoring column and sample weight;
  - it cannot be located and is no denominator: LEAK-10.
- **Where noaa falls:** short tows can be found by duration, but which of them the catch cut cannot (149 of the 256 tows under half the median duration carry performance code 0). So the second branch applies, and as written it asks for a weight.
- **Why that is defensible:** the definition instead applies MET-15's clause "when the decision is per unit of an equal-area map ... scored unweighted, no sample weight". MET-15 is a Must and that clause is specific, so it governs over a Cases row. A second fact supports the choice: NOAA's design-based index (gapindex) also weights hauls equally within a stratum.
- **The cited precedents fit less well than the issue's Consistency bullet implies:**
  - boreal: the sampled area is a protocol constant (1 m^2 in NT, 4 m^2 in SK), with no realized denominator (its REVIEW.md: "MET-15 not triggered as a weight rule"). It matches on "unweighted per unit area", not on the cut.
  - wadden (CC 2026-11-06, Lennart, D13): the closer case. Its subsample fraction is chosen after the lab sees the sample, so the effort depends on the outcome, and it is scored unweighted. The difference is that wadden's fraction is not released and could not be a weight anyway. noaa's area swept is released.
  - So noaa is the first case where an outcome-cut denominator is available as a weight and is deliberately left out.
- **Third exception / amendment due:** no. There is one prior case of this kind (wadden), no third. The register has no flag on MET-2, MET-14, MET-15 or LEAK-41; its only amendment-due flag (SPLIT-10) comes from issue 2, not from today's change.
- **The cost, measured by the panel:**
  - The column auditor finds pollock's short tows are 3.4% of rows but hold 14.0% of pollock's squared deviation; Greenland turbot 10.1%, shortspine thornyhead 7.0%.
  - The domain practitioner finds a design-weighted score ranks models as the declared one does (tau 0.81 to 1.0, same winner on 4 of 4 folds).
  - The bias is accepted on purpose and named in the notes.

**4. Is the pollock-only cut claim argued from the data? Yes, with two gaps**
- **What replicates:** the column auditor reran it on the raw tables.
  - Over all hauls, within stratum-year cells: pollock +0.357, the other taxa -0.360 to +0.077.
  - Among hauls with a catch: pollock +0.551, the others 0.002 to 0.249.
  - 9 of 11 taxa higher by raw means, 11 of 11 within cells.
  - On the EBS shelf, 831 pollock tows under 0.4 h average 8.33 log1p kg/km^2 against 7.35 at full length.
  - The contrast that carries the claim is the all-hauls one, and the notes use it correctly.
- **Gap (a): "which a smaller area swept explains" is asserted, not tested.** A cheap test exists: compute each taxon's expected log1p shift among positives from shrinking the area alone (Poisson thinning at the taxon's own count distribution).
  - That mechanical inflation should be largest for sparse taxa with singleton counts and close to 0 for large counts.
  - Pollock's large counts should then show almost none, so its +0.55 is if anything stronger evidence than the notes say.
  - Running this check would turn the assertion into a measurement.
- **Gap (b): the causal phrase "its tows end early on a large catch" has no source statement and no named control.**
  - Pacific cod is the natural control: almost as widespread on the EBS shelf (4.0% zeros there) and inside the -0.36 to +0.08 range.
  - The notes could name cod's value, or cite an AFSC protocol on shortened tows if one exists (not verified here).
  - The turbot and thornyhead squared-deviation shares above are a separate point (score effect, not offset). Short tows are more common at depth (6.7% at 500 m and deeper against 3.3% at 0-50 m), which may explain them; they do not contradict the claim.
- **CHANGES.md misstates the evidence (the panel's file only; the definition, README CC and REVIEW.md use the right number):** it headlines "+0.55 log1p above, the others 0.00 to +0.25". That is the among-positives measure, which the notes themselves say shows up for every taxon. The number that carries the claim is +0.36 against -0.36 to +0.08 over all hauls.
- **Smaller points:**
  - The column auditor's MET-14 note: `_clean` does not assert that density times area swept rebuilds the count. The siblings (wadden, boreal) take a density from the source and do not assert this either, so it is a fix on MET-14's wording, not a consistency departure.
  - The README says "Not built yet", so the generated decision table has not been rendered from a build.

**Optional recording question (not a reflection prompt; the departure has its reason)**
Record noaa's unweighted density as the equal-area exception in the LEAK-41 time-on-risk Cases row?

**Problem:**
- As written, the row's second branch (denominator, cut not locatable) asks for a weight scoring column and a sample weight.
- noaa ships none, on MET-15's equal-area clause; neither the row nor its cases say so.
- wadden (2026-11-06) is the only earlier case with outcome-set effort scored unweighted, and its effort is not released. noaa's is.

| | Option | Pro | Con |
|---|---|---|---|
| a | Add noaa to the row as the equal-area case: "where the decision is per unit of an equal-area map, the rate is scored unweighted (MET-15), the bias of the cut named in the notes" | the next survey table finds the case; the row and MET-15 agree in writing | one more clause in a long row |
| b | Leave the row; MET-15's clause is enough | no edit | the row as written still asks for a weight in noaa's situation |
| c | Weight noaa by the area swept (follow the row) | follows the row's wording | against MET-15's equal-area clause and NOAA's own index; ranks models the same |

Recommendation: (a).

Footnotes:
- [^1] LEAK-41 (Must, 2026-11-06, Lennart), time-on-risk Cases row.
- [^2] MET-15 (Must, 2026-11-06, Lennart), equal-area clause.
- [^3] MET-14 (Should).
- [^4] LEAK-10 (Must).

</details>

<details><summary>Advocate</summary>

ADVOCATE OPENING BRIEF: noaa_afsc_bottom_trawl_survey_cpue (exposure re-review, 2026-11-06, full tier)

Position: ship as defined. Rows, target, features, split and metric stay as they are. Every problem the panel found is in the notes, the stated reasons or one missing assert. Each one has a fix at the "fix the definition text" or "keep with a note" step of the remedy ladder (principles.md, How to decide 5). None of them needs a change to the data or the task.

1. No leak. The realized effort is out, and no shipped feature carries it (P4; LEAK-41 Must, LEAK-10 Must, USE-3, USE-6).
   - Evidence, column auditor:
     - duration, distance, net width and height, area swept, end position and performance are all dropped.
     - From the shipped features, the realized area-swept ratio is predicted at R^2 0.103 and the duration ratio at 0.076.
     - Short tows are told apart at ROC AUC 0.749 (0.757 without the temperatures), through place (0.667) and schedule (0.694) only. That is risk selection, which LEAK-41 allows in so many words.
     - No precision or missingness marker: one decimal everywhere, and the missingness gap within survey and year is -0.009.
   - Evidence, claim auditor: the shipped features predict area swept at R^2 0.85-0.91, but against the region-year means R^2 is -0.11 to +0.18. So it all comes from the planned effort (region and era), which is known at the prediction point.
   - Evidence, task gamer: no exploit beat the noise floor (best gain -0.009, noise about 0.01; all effort proxies together +0.005).
   - Evidence, leak probe: 0.0% exact copies across 9 splits, and 0 hauls split across a cutoff.
   - Why it outranks: P4 is the highest-ranked rule this dataset could fail on, and it holds. Every other finding sits below it.

2. Today's change is exact. Every fold can be scored (MET-2 Must, P6).
   - `taxon_group` is identical to `taxon` on all 391,044 rows. It is not a feature, and no sample weight is declared.
   - The scorer equals an independent per-taxon computation to 4 decimals in all 9 windows (claim auditor rows 1-4; domain practitioner).
   - `dataset check`: the MET-2 warning is gone, 0 errors, 0 warnings.
   - All 11 taxa are present in every window, with at least 1,056 rows and 71 positives per taxon.
   - Precedent: liberty_mutual's `var11_weight` copy (precedent checker: consistent, no drift).

3. Scoring the density unweighted is the right decision, even though the stated reason is wrong (MET-15 Must equal-area clause; MET-16 Should).
   - Concede: "unweighted over equal-area cells" does not describe the scored hauls. The Aleutians have about 8x the hauls per km^2 of the EBS, and within GOA and AI the strata differ up to 9.5x and 22x (claim auditor row 15; domain practitioner finding 2).
   - What still holds:
     - The decision is a per-cell EFH map, which is exactly MET-15's "per unit of an equal-area map" clause.
     - EFH is not a population estimate (MET-16).
     - The source's RMSE is unweighted over stations (TM-459 p. 21).
     - NOAA's gapindex weights hauls equally within a stratum.
   - Measured cost of the choice is nil: a stratum-area design weight and a taxon x region mean both rank 7 models like the declared score (tau 0.81-1.00, same winner 4/4).
   - The precedent checker finds the LEAK-41 Cases row's second branch would ask for a weight. MET-15's specific Must clause governs over a Cases row, since the Cases are applications of the rule (Conflicts: rules win over precedents). The precedent checker calls the exception reasonable.
   - Mildest remedy:
     - Reword the reason to "unweighted over hauls, as the source's station RMSE; a stratum-area design weight ranks the models the same".
     - Record noaa in the LEAK-41 Cases row (the precedent checker's option a).
     - No change to the metric.

4. A real, non-trivial task with clear headroom (P3, P6; TP).
   - Task probe: random forest skill +0.786 ± 0.012, beats the dummy on 100% of splits, spread over linear +0.434 (paired SE 0.011). Flags: none.
   - Blind reviewer (from the data and public pages only): "Include with small changes".
     - LightGBM R^2 0.73-0.78 against a taxon x stratum lookup at 0.66-0.69.
     - The use (EFH species distribution models, model-based indices) is real.
   - Domain practitioner (AFSC habitat analyst):
     - Fit approximate, already settled (USE-8).
     - The metric now scores the decision "mostly", up from "partly".
     - Keep the density target, the dropped effort, the short tows, the unweighted per-taxon score and the copy.

5. The refuted exposure statements need text and numbers only. None changes a decision (LEAK-41 reporting part, Must; EV-1, EV-8).
   - Poisson gain:
     - Concede: "nothing under a Poisson fit" does not replicate (+0.013 mean, better in 4 of 5 windows).
     - The effort still goes, on timing: an untowed cell has no tow. LEAK-41 says "whatever it scores".
   - The 1/weight ceiling:
     - Concede: it is not stated, and LEAK-41 requires it.
     - It is now measured twice: 1/area swept beside the taxon reaches 1.016-1.046 against the honest 0.90-0.93. The leak would gain 0.004-0.014.
   - "Pollock alone":
     - Concede: against an area-only null, Pacific cod also sits above (4 and 9 null SDs).
     - The causal phrase "its tows end early on a large catch" is untested.
     - Neither statement feeds a feature, so no score moves.
   - The Poisson range "0.86-1.11" becomes "0.86-1.24".
   - Why this is not a reason to hold the dataset: these are reporting failures. The Must is met by writing the measured numbers into the Effort bullet and issue 4, which is the mildest remedy. They are independent of the validity in point 1, which holds.

6. The split holds. The short-tow history is a note, not a filter (P4; SPLIT-1/3/9/11/12/13/14/23 hold; SPLIT-20 Should).
   - Split auditor: no new Must is broken. Training covers 54.0-95.4% of rows. 0 hauls straddle a cutoff. Most test hauls are within 5 km of a training haul (SPLIT-13, known waters).
   - The EBS cut sits in 1989-2008 training years.
     - Dropping short tows from training changes the score by -0.0013.
     - Dropping the 30-minute GOA/AI era changes it by -0.0011.
     - Both are noise.
   - LEAK-41 bars training or scoring on rows selected by the realized effort, so a filter is ruled out anyway.
   - Concede: the splits_comment "each window holds one survey of every region" is false.
     - The slope survey (BSS) ended in 2016, the NBS is missing from 3 windows, and 2019 has no AI.
     - Remedy: reword the comment, and add the Greenland-turbot note to the metric note (its spread is 8-38 per km^2 from 2017 on).

7. The quality gaps are cheap and safe (P7; MET-14 Should, CLEAN-15).
   - The MET-14 assert is missing.
     - The data rebuilds the count on all 201,731 counted catches (max relative error 1.6e-4).
     - Remedy: one `np.allclose(cpue_nokm2 * area_swept_km2, count, rtol=1e-3)` in `_clean`. The frame does not change.
   - The blind reviewer's false-zero worry is answered.
     - The 128 catches weighed but not counted are dropped, not zero-filled (CLEAN-15).
     - That is why the task gamer saw 1,116 rows in incomplete hauls, and the row count does not predict the target.
   - The long format with 11 rows per haul is safe under a date split, because hauls stay whole.
   - The 2026 season's provisional status is already a note (EV-7, settled).
   - Optional notes (they serve P6/P7 and change no decision):
     - Pollock's short tows hold 14% of its squared deviation; Greenland turbot 10.1%, shortspine thornyhead 7.0%.
     - log1p fits underpredict the mean by 2-3x.

Judgment record (advocate)
Verdict: ship after text changes.
Validity: LEAK-41 and LEAK-10 hold (risk selection only, R^2 0.10, AUC 0.75). The LEAK-41 reporting Must is fixed by stating the Poisson gain (up to +0.013) and the 1/area ceiling (0.004-0.014). SPLIT-1/3/9/14/23 hold; SPLIT-20 is a note. USE-3 holds.
Value: MET-2 holds (exact copy, every fold scorable). MET-15/16: unweighted is right, but the stated reason must be reworded (design weight tau 0.81-1.00). TP: skill +0.786.
Quality: MET-14 assert to add. Notes for the splits_comment, the pollock/cod cut wording and the Greenland turbot spread.
For the curator: the optional recording of noaa in the LEAK-41 time-on-risk Cases row (precedent checker, option a).

Sources: the panel's reports (claim auditor, column auditor, split auditor, domain practitioner, precedent checker, blind reviewer, task gamer) and the task and leak probes. Rules: principles.md, leak_checks.md, metrics.md.

</details>

<details><summary>Critic</summary>

CRITIC'S OPENING BRIEF: noaa_afsc_bottom_trawl_survey_cpue (exposure re-review, 2026-11-06, full tier)

Position: ship only after changes. I am not asking for exclusion. No evidence agent found a leak in the shipped features or a split that breaks a Must. The task gamer found no exploit above the noise floor. The column auditor found the realized effort predicted only through place and year: realized area ratio R^2 0.10, short tows told apart at AUC 0.75. What I do find is that the definition's own account of the exposure decision gets wrong the very facts that decision rests on. One of these is the reporting part of a Must (LEAK-41). One is the stated premise for setting aside the LEAK-41 Cases row (MET-15). One is a LEAK-10 claim that is refuted in part. Each fix is to the text or one assert. Rows, target, split and metric stay as they are.

Definition: `dataset.py` (Effort bullet at line 305, Metric bullet at 314, CC at 318, splits comment at 228/359, `_clean` asserts at 398-401, decision caption at 499-500).

1. LEAK-41's required report is wrong in one number and missing another (P4, LEAK-41 Must, reporting part).
   - Problem: LEAK-41 says the definition "reports its gain ... with an L2 fit on the shipped scale and with the weighted actuarial fit, and decides on the worse; it states the score of 1/weight alone as the ceiling a leak would reach." The Effort bullet says the effort columns gain 0.0028 under L2 and "nothing under a Poisson fit". It gives no ceiling.
   - Evidence: the claim auditor reran LightGBM on the newest five windows, 2 seeds. The Poisson gain is +0.0325, +0.0052, +0.0150, -0.0071, +0.0204: mean +0.013, better in 4 of 5, seeds agreeing in two windows. The study's own Poisson run gave -0.006 (1 of 5). L2 replicates at about +0.0004 (3 of 5). So "the worse" that LEAK-41 decides on is about 0.013, roughly five times the stated number.
   - Ceiling: not stated. Measured by two agents. Taxon + 1/area swept scores 1.031-1.046 against taxon alone 1.039-1.057, a gain of 0.007-0.013, and 0.004-0.012 beyond region and year. The domain practitioner gets 0.007-0.014.
   - Effect on the task: the decision to drop the effort stands, on timing (USE-3). But the record understates what the leak is worth by about 5x, and a later reader weighing a "free feature" variant would read the wrong number.
   - Remedy (text): "under a Poisson fit -0.006 to +0.013 by windows and seeds (two runs); 1/area swept with the taxon alone gains 0.007-0.013 over the taxon alone (the ceiling)". Put it in the Effort bullet and REVIEW issue 4.

2. The stated reason for scoring unweighted is false, and it is the only thing that licenses departing from the LEAK-41 Cases row (P4/P6; LEAK-41 Cases row, MET-15 Must, MET-16 Should).
   - Problem: the Effort bullet and the CC justify "unweighted on this density, as the review maps it over cells of equal area (MET-15)". The precedent checker shows where noaa falls in the LEAK-41 time-on-risk row. The cut cannot be located row by row: 149 of the 256 tows under half the median duration carry performance code 0. The amount is the target's denominator. That is the second branch, which asks for the area swept as weight scoring column and sample weight. The definition sets that aside on MET-15's equal-area clause.
   - Evidence: the scored units are hauls, and hauls are not equal-area. The claim auditor counts hauls per 1000 km^2 per year (2015-2025): AI 5.99, BSS 5.33, GOA 1.75, EBS 0.75, NBS 0.69. So a km^2 of the Aleutians counts about 8x one of the EBS shelf. Within a survey and year, stratum densities differ by up to 22.1x (AI) and 9.5x (GOA). AI holds 16.5% of rows on 5.8% of the area. The domain practitioner's p90/p10 agrees (AI 9.4, GOA 4.0).
   - Effect: the conclusion can stand on better grounds. The source's RMSE over stations is unweighted (TM-459 p. 21). EFH is not a population estimate (MET-16). A design-weighted score ranks 7 models alike (tau 0.81-1.00, same winner 4/4). But as written, the record cites a false premise for an exception to a Must-backed row. Precedent checker: noaa is "the first case where an outcome-cut denominator is available as a weight and is deliberately left out", and the row does not say so.
   - Remedy (fix the text, record the exception): reword to "scored unweighted over the hauls, as the source's RMSE over stations is; the hauls are not equal-area (AI about 8x the EBS per km^2), and a stratum-area design weight ranks the models the same (tau 0.81-1.00)". Add noaa to the LEAK-41 time-on-risk Cases row as the per-map-unit case (precedent checker's option a).

3. "The cut is claimed for pollock alone" is refuted in part, and so is "a smaller area swept explains" the rest (P4, LEAK-10 Must; EV-1 Must).
   - Problem: the LEAK-10 finding (which taxa's labels carry a catch-triggered stop) rests on two things. One is a contrast across taxa. The other is an asserted mechanism that was never tested.
   - Evidence: the claim auditor ran a null test. It redrew each short tow as a binomial thinning of a random full tow in its cell, with the ratio of the areas swept, 20 draws.
     - Pacific cod's short tows stand above the null: +0.077 vs -0.084 over all hauls (about 4 null SDs) and 0.229 vs 0.051 among catches (about 9 SDs). Cod's gap is largest where pollock's is (EBS +0.18, BSS +0.36).
     - Halibut, sablefish, shortspine thornyhead and rock sole exceed the null among catches at 2.4-3.9 SDs.
     - The flatfish fall far below the null (Hippoglossoides -0.360 vs -0.039). So short tows are not exchangeable within cells, and pollock's gap mixes a stop with where the tow was. The causal clause "its tows end early on a large catch" (line 499-500) is untested (EV-3).
   - Effect on the score: no feature carries it, so no score changes. But these labels enter the score. The column auditor finds short tows are 3.4% of rows yet hold 14.0% of pollock's squared deviation, 10.1% of Greenland turbot's and 7.0% of shortspine thornyhead's.
   - Split auditor: the pollock excess is mostly the training history of EBS 1989-2008 (+0.71). In the test years it shows in the GOA and AI (+0.73, +0.39), not on the EBS shelf (+0.07). So the headline figures (+0.36, the 831 EBS tows) describe the training side, not what is scored.
   - Remedy (text, no rows change): claim the cut for pollock "and, to a lesser degree, Pacific cod". Say the smaller area explains the gap for the flatfish, not for cod, halibut, sablefish, thornyhead or rock sole. Call the stop "the likely reading, not isolated". Add the squared-deviation shares (14.0 / 10.1 / 7.0%) and the region and era split of the pollock gap. Optionally add the null column to `_short_tows` so the decision table shows the test. Fix the decision caption at lines 499-500 to match.

4. The splits comment is false about region coverage, which hides a weak vote in the metric (P4 text, SPLIT-14 / EV-2; P6, MET-2).
   - Problem: line 228 says "two years hold one survey of every region", and line 359 says "one survey of every region each".
   - Evidence (claim auditor; split auditor table):
     - BSS ran 2002-2016 only, so it is absent from 6 of 9 windows.
     - NBS is absent from 3 windows.
     - Window 3 (2019) has no AI.
     - Only 2009-2010 holds all five regions.
   - Effect on the metric: each taxon has one equal vote. From 2017 on, Greenland turbot (BSS presence 0.70) is scored without its main habitat, on a spread of 8-38 per km^2 against 47-639 before. Turbot's normalized RMSE there divides by a tiny spread, yet keeps 1/11 of the score. The blind reviewer also notes that window-to-window variance partly reflects the region mix.
   - Remedy (text): "each holds the EBS shelf, the GOA and, except 2019, the AI; the slope survey ended in 2016, the NBS runs in some years". Add one Greenland-turbot sentence to the Metric bullet.

5. The MET-14 rebuild assert is missing (P6/P7, MET-14 Should).
   - Problem: MET-14 says "`_clean` asserts that target x denominator rebuilds it". `_clean` asserts only cpue_kgkm2 > 0 (line 401).
   - Evidence: the identity holds on all 201,731 counted catches (max relative error 1.6e-4), and area = distance x width to 1.6e-4 on 35,561 hauls. Both the claim auditor and the column auditor found this.
   - Remedy (repair, one line): merge area_swept_km2 into `catch` and assert np.allclose(cpue_nokm2 * area_swept_km2, count, rtol=1e-3) on the counted rows before the effort columns leave. The frame does not change. The siblings (wadden, boreal) lack it too, but that does not excuse a Should with a cheap fix and no departure reason.

6. The metric note's numbers are out of range, and it omits a property that matters to the actor (P6, EV-8 Should; MET-3/MET-8 note).
   - Problem: "Poisson LightGBM scores 0.86-1.11".
   - Evidence: the claim auditor gets 0.996-1.179 (2021-22: 1.157, 1.179). The study's own run gave 0.879-1.243. In 2021-22 Poisson loses to the taxon count mean (1.226).
   - Domain practitioner: log1p fits, inverted, predict only 34-51% of the test mean density. The EFH encounter threshold uses the absolute mean, and the declared RMSE still prefers these fits to Tweedie in 2 of 4 windows.
   - Remedy (text): "0.86-1.24 (two runs)". Add one sentence saying log1p fits underpredict the mean 2-3x, which RMSE barely penalizes.

What I do not argue:
- The 2026 provisional season, the in-situ temperatures, the pooled life stages and the haul-x-taxon long format are settled in REVIEW.md, and today's change does not reopen them.
- The 30-minute GOA/AI era sits on the training side only. It costs -0.0011, which is noise (split auditor).
- CHANGES.md headlines +0.55 instead of the +0.36 that carries the claim. That is a panel-file error, not the definition's.
- I do not count points 5 and 6 as reasons to hold a real task. They are cheap fixes.

Ask, in order:
- (1) Correct the LEAK-41 Poisson gain and state the ceiling.
- (2) Replace the equal-area reason and record the exception in the LEAK-41 Cases row.
- (3) Restate the LEAK-10 cut claim (cod, the null test, the squared-error shares, train-side vs test-side).
- (4) Fix the splits comment and add the turbot note.
- (5) Add the MET-14 assert.
- (6) Fix the Poisson range and add the mean-bias note.

Evidence: the claim auditor (rows 7, 12, 13, 15, 16, 17, 19, 22), the column auditor (problems 1-2), the split auditor (problem 1), the domain practitioner (findings 2-4), the precedent checker (sections 3-4), the task gamer and the blind reviewer. Rules: leak_checks.md (LEAK-41 at line 103, Cases row at ~441) and metrics.md (MET-14/15/16 at lines 232-256).

</details>

<details><summary>Advocate rebuttal</summary>

ADVOCATE REBUTTAL: noaa_afsc_bottom_trawl_survey_cpue (exposure re-review, 2026-11-06)

The critic and I agree on the verdict: ship after changes to the text and one added assert. We also agree that the rows, target, split and metric stay as they are, and that there is no leak and no broken split Must. Of the critic's six points I concede five in substance. I dispute how points 2 and 3 are framed, and qualify how point 4 reads, because each framing would set a wrong precedent or overstate what is scored. No new points.

1. The LEAK-41 report: one number wrong, the ceiling missing. CONCEDE.
   - This is the reporting part of a Must, so it must be fixed before shipping, not merely noted.
   - The fix is the critic's text: Poisson -0.006 to +0.013 by windows and seeds (two runs), and the ceiling 0.007-0.013 (0.004-0.012 beyond region and year).
   - What follows: the decision to drop the effort stands on timing. LEAK-41 says "whatever it scores", and USE-3 applies because an untowed cell has no tow. The ceiling (1.016-1.046) stays far above the honest models (0.90-0.93), so even the corrected leak is small.

2. The reason for scoring unweighted. CONCEDE the wording, DISPUTE the framing.
   - Conceded: "over cells of equal area" misdescribes the scored hauls (AI about 8x the EBS per km^2; strata within a region up to 22x). The reason must be replaced.
   - Disputed:
     - The critic calls this "a false premise for an exception to a Must-backed row". A Must has no exceptions (principles.md, Exceptions).
     - The clause the definition relies on is MET-15's. It is a Must and keys on the decision: "when the decision is per unit of an equal-area map ... scored unweighted, no sample weight". That premise is true here. The EFH decision is a per-cell map of equal-area raster cells (domain practitioner; fit_reason). What was false is only the sentence describing the scored rows.
     - So the license stands. MET-15's specific clause applies within LEAK-41's scope. The case is an application of a rule, not an exception, and the remedy is a reword plus a Cases-row entry.
   - What follows:
     - Adopt the critic's wording, which adds the true supporting facts: the source's station RMSE is unweighted (TM-459 p. 21), MET-16 applies because EFH is not a population estimate, and the design weight gives tau 0.81-1.00, same winner 4/4.
     - Record noaa in the LEAK-41 time-on-risk Cases row (precedent checker, option a) as the per-map-unit application of MET-15, of kind "application", not "exception".

3. The pollock cut claim. CONCEDE the text, DISPUTE two readings.
   - Conceded:
     - Cod stands above the area-only null (4 and 9 SDs).
     - The mechanism "a smaller area swept explains" is not tested for cod, halibut, sablefish, thornyhead or rock sole.
     - "Ends early on a large catch" is the likely reading but is not isolated (EV-3).
     - Reword as the critic says and fix the caption.
   - Disputed (a): the critic says "the headline figures describe the training side, not what is scored".
     - The split auditor's own numbers show the cut on both sides. Pooled, the training sides are +0.35 to +0.40 and the nine test windows +0.30, with AI +0.39 and GOA +0.73 in the test years.
     - The EBS shelf moved; the effect did not vanish from what is scored.
     - The right text is "mostly EBS 1989-2008 on the training side; GOA and AI in the test years", not "training side only".
   - Disputed (b): the critic presents Greenland turbot's (10.1%) and thornyhead's (7.0%) squared-deviation shares as the bias of a cut.
     - The column auditor ties short tows to depth (6.7% at 500 m and deeper against 3.3% at 0-50 m).
     - The null test does not put the turbot gap above the area effect; turbot is among the taxa the area explains (claim auditor row 12).
     - Report those two shares as "short tows' weight in the score", not as a stop.
   - Rule: EV-1 (state only what was measured). LEAK-10 is untouched because no feature carries the cut, and LEAK-41 bars removing the rows.

4. The splits comment on region coverage. CONCEDE the text; the metric stays sound.
   - The comment is false: BSS is absent from 6 windows, NBS from 3, and AI from 2019. Reword it and add the turbot sentence.
   - On "a weak vote": MET-2 holds in every window. Turbot has at least 1,056 rows and 71 positives in every window, and a spread of 8-38 per km^2. Dividing by the taxon's own spread is the normalization's purpose (MET-11: a fixed divisor within a taxon). It does not inflate one taxon's vote beyond 1/11.
   - What follows: a note, no change to the metric or the split (SPLIT-14 holds, training share 54-95%).

5. The MET-14 assert. CONCEDE.
   - It is a Should with a cheap, safe fix (P7 remedy: fix when cheap). Add the one-line np.allclose. The frame does not change.

6. The Poisson range and the mean-bias note. CONCEDE.
   - The range becomes "0.86-1.24 (two runs)".
   - The underprediction note (log1p fits invert to 34-51% of the mean density) helps users.
   - It describes the source's metric, RMSE on numbers (MET-1, MET-11), and is not a reason to change the metric (MET-4 order: the source's deliberate choice stands).

Net
- The critic's six asks, in its own order, are all text or one assert, and I support all of them.
- On ask 2, the record should state that the dataset applies MET-15 rather than claiming an exception to a Must. On ask 3, the claim should be "both sides, different regions", with the turbot and thornyhead shares reported as score weight, not as stop bias.

Sources: the critic's brief and the panel's reports (split_auditor problem 1, column_auditor problem 2, claim_auditor rows 12, 15-17, 22). Rules: principles.md, leak_checks.md, metrics.md.

</details>

<details><summary>Critic rebuttal</summary>

CRITIC'S REBUTTAL: noaa_afsc_bottom_trawl_survey_cpue (exposure re-review, 2026-11-06)

The advocate and I reach the same verdict: ship after text changes, with no exclusion and no change to rows, target, features, split or metric. We differ on three things. Two notes the advocate calls optional are required by rule. The cut-claim concession is too narrow. And the ceiling should be stated as two separate numbers rather than one merged range. I raise no new points.

1. No leak (advocate point 1): concede. The realized effort is predicted only through place and year: area ratio R^2 0.103, short tows AUC 0.749, region-year R^2 -0.11 to +0.18. That is risk selection, which LEAK-41 and USE-6 allow. My brief never claimed a feature leak.

2. Today's change is exact (advocate point 2): concede. `taxon_group` is identical on all 391,044 rows, the scorer matches to 4 decimals in 9 of 9 windows, and every taxon has at least 71 positives per window (MET-2).

3. Unweighted scoring (advocate point 3): concede the decision and the reworded reason. I dispute calling the Cases-row record optional.
   - The advocate's own judgment record calls recording noaa in the LEAK-41 time-on-risk Cases row "optional". It should be required.
   - As written, the row's second branch asks for the area swept as the weight scoring column and the sample weight. The only written ground for not doing that was "equal-area cells", and both of us now agree it is false.
   - principles.md: a departure "needs the fact that sets the case apart and the higher principle it serves, and is recorded as an exception". Maintenance order: amendment > exception > precedent.
   - Precedent checker: noaa is "the first case where an outcome-cut denominator is available as a weight and is deliberately left out".
   - Without the Cases-row entry, the next survey table follows the row's wording and ends up weighted.
   - Remedy: the reword the advocate proposes, plus the Cases-row clause (option a) as part of the change, not left to the curator's discretion.

4. A real task with headroom (advocate point 4): concede. RF skill is +0.786, the blind reviewer says include, and the fit is approximate (settled, USE-8). I argued value only through the turbot vote (point 6 below).

5. The refuted exposure statements (advocate point 5): concede that these are reporting failures fixed in text. I dispute two parts of the proposed remedy.
   - (a) The ceiling. The advocate writes "1.016-1.046 ... would gain 0.004-0.014", which merges two different comparisons. LEAK-41 asks for "the score of 1/weight alone".
     - Claim auditor row 17: taxon + 1/area is 1.031-1.046 against taxon alone at 1.039-1.057, a gain of 0.007-0.013.
     - Beyond srvy and year the gain is 0.004-0.012 (1.016-1.034 against 1.027-1.041).
     - Domain practitioner: 0.007-0.014.
     - Remedy: state both comparisons, labelled, so the ceiling is the figure LEAK-41 defines.
   - (b) The cut claim. The advocate concedes cod only, and says no score moves, so the rest can be dropped. Both points are too narrow.
     - Against the area-only null, more taxa sit above it among hauls with a catch: halibut 0.249 vs 0.159, sablefish 0.199 vs 0.099, shortspine thornyhead 0.183 vs 0.072, rock sole 0.124 vs 0.041, at 2.4-3.9 SDs (claim auditor row 12).
     - So "which a smaller area swept explains" is refuted for these taxa as well as for cod. EV-1 (Must) settles the fact before the LEAK-10 reading is written, and the decision caption at dataset.py lines 499-500 repeats the refuted claim.
     - The figures in the notes describe the training side, not the scored windows. The pollock excess is EBS 1989-2008 (+0.71); in the test years it is AI and GOA (+0.39, +0.73) and the EBS shelf shows only +0.07 (split auditor).
     - No feature moves, but scored labels carry the cut: pollock's short tows hold 14.0% of its squared deviation, Greenland turbot's 10.1% and shortspine thornyhead's 7.0% (column auditor).
     - MET-16 (Should) says "the notes name it when sampling depends on the outcome". The CC itself accepts "the bias of the cut", and the shares are the measured size of that bias.
     - Remedy: the restated claim (pollock and, to a lesser degree, cod; area explains the flatfish only; the stop is the likely reading, not isolated), the train-versus-test split of the gap, the corrected caption, and the squared-deviation shares as a required note, not an optional one.

6. The split holds (advocate point 6): concede. SPLIT-20 is a note. Dropping the short tows from training moves the score -0.0013 and dropping the 30-minute era -0.0011, both noise, and LEAK-41 bars a filter anyway. We agree on the splits_comment reword and the Greenland turbot note.

7. Quality gaps (advocate point 7): concede in full.
   - The MET-14 assert is a one-liner.
   - The blind reviewer's false-zero worry is answered: the 128 uncounted catches are dropped (CLEAN-15).
   - The long format is safe under the date split.
   - The 2026 season is settled (EV-7).
   - I accept that the log1p mean-bias note is optional (it is a property of the source's metric, MET-3/MET-8, and not a defect).

Remaining ask, beyond what the advocate already accepts:
- (i) Record noaa in the LEAK-41 Cases row as part of the change (principles.md, exception recording).
- (ii) State the ceiling as LEAK-41 defines it: taxon + 1/area against taxon alone, 0.007-0.013, plus 0.004-0.012 beyond region and year.
- (iii) Widen the cut claim to the null-test results for all taxa, fix the caption at dataset.py lines 499-500, and give the train-versus-test era split (EV-1, LEAK-10).
- (iv) Make the 14.0 / 10.1 / 7.0% squared-deviation shares a required note (MET-16).

Sources: the definition's `dataset.py`; the claim auditor (rows 12, 17), the column auditor (problem 2), the split auditor (problem 1) and the precedent checker (section 3); rules: leak_checks.md and metrics.md.

</details>
