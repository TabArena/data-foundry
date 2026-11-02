# pennsylvania_oak_hickory_regeneration_experiment

**Outcome:** added. The AI recommends shipping it as now defined: a CC0 Dryad deposit of a randomised field experiment
of the Penn State Deer-Forest Study (261 microplots at 24 sites, each site holding every combination of deer fence, lime
and herbicide once beside 2-4 controls), predicting the 2021 count of tree seedlings of any species over 15 cm from the
2014 inventory and the planned treatment, with whole sites held out, scored by RMSE on the count (the fallback).

Validity:
* SEL-3 and USE-2 hold: a treatment choice made from a pre-treatment inventory fits, your `Yes` of 2026-10-30. The
  score mostly measures a forecast of the plot's regeneration rather than the treatment choice (issue 1).
* USE-1 and USE-8 triggered, fixed in the text: the use case now describes the forecast that is scored, and
  `fit_reason` names the gaps (every tree species counted, a weakly identified treatment contrast, treatments applied
  per plot rather than per stand, no overstory, deer impact or fern cover in the file, two forests and one cohort).
  Fit approximate.
* USE-5 holds: the 2021 level rather than the paper's 2014-2021 change, as your accepted screening asked. With the
  2014 count as an input, the two carry the same information on the count.
* LEAK-10 triggered, fixed: the 11 columns measured after the treatments are dropped. The 2014 soil values stay: with
  site fixed effects, lime moves the 2014 pH by at most +0.12, against +1.18 for the 2016 pH.
* SPLIT-1 and SPLIT-3 hold: grouped by the source's own site; random microplots would overrate R^2 by 0.14-0.16
  (SPLIT-29). Balance of the folds by forest is issue 2.
* PROV-8 and PROV-13 hold: Dryad's own deposit, its SHA-256 equal to Dryad's digest. PROV-2 (Should) triggered, fixed
  in the notes: the deposit's README describes the file only in part; the notes say how the 7 undescribed columns
  were read and flag the stated manganese unit as likely mg/kg, and the laurel "volume" is renamed
  `mountain_laurel_volume_index_2014`. PROV-17: the paper was read only in the methods Dryad reproduces (the
  publisher blocks scripts); it is open access at
  [doi:10.1139/cjfr-2024-0034](https://doi.org/10.1139/cjfr-2024-0034) if you want its results checked.

Value: TP-5 holds (85-88 scored microplots per test fold; accepting the check's warning is issue 3). TP-2, a small
real signal: random forest R^2 0.27-0.34 on log1p at unseen sites, against at most 0.006 with the target shuffled; the
treatment flags add 0.018 (SE 0.003). MET-11: the fallback `rmse` on the count, kept by your call of 2026-11-02.

Quality: nothing beyond the cosmetic (P7: counts stored as floats, the file's `BaldEagle` spelling). In the record,
the `Two-Regime Zeros` tag goes under your rule of 2026-10-30: 48 zeros against 38 ones, and the zeros follow the 2014
count (39% of the plots empty in 2014 stay empty, against 12% of the others).

Weighed: a CC0 deposit of a randomised experiment +; 24 sites -; the treatment, which is the decision, barely moves
the score -. Left for Andrej: issues 1 to 3.

**Main points:** Keep `Yes` on the reworded use case and drop the `No Good Target / Scientific Discovery` marker
(issue 1); stratify the site folds by state forest (2); accept the few-groups warning, whose numbers follow 2 (3).
Settled on 2026-11-02: RMSE on the count stays (issue 4, closed).

**Issues for Andrej:**

1. **Drop the `No Good Target / Scientific Discovery` marker from this `Yes`, although the treatment, which is the
   decision, barely moves the score?** The use case is a forester choosing among deer fence, lime and herbicide from
   a pre-treatment inventory. The data holds that inventory beside randomised treatments, which sets it apart from
   the experiments you rejected (inputs that are only the design). But with one microplot per treatment at each site,
   the score rewards forecasting how many seedlings a new site's plots will hold far more than choosing the
   treatment.
   * What it changes: models are ranked on forecasting a plot's regeneration from its 2014 inventory. A model that
     ignored the treatment would rank almost as high.
   * Evidence: the 2014 count alone gives R^2 0.22 of the random forest's 0.27; the treatment flags add 0.018 (SE
     0.003). Within a site the random forest explains R^2 0.037, and it picks the observed best treatment of a site
     30.8% of the time with the flags and 30.0% without (chance 14%). SILVAH, the US Forest Service's prescription
     system for these forests, calls a plot stocked when its seedlings pass a threshold that rises with deer
     pressure. On that call at held-out sites (a diagnostic; nothing is declared), carrying the 2014 count forward
     does as well as every untuned model or better: best in the mediator's and the critic's runs, 0.124 against 0.123
     for the best model in the advocate's. The target counts every tree species, red maple and black birch included,
     where a forester acts on desirable oak and hickory; the deposit has no species split.
   * For keeping `Yes` and dropping the marker: USE-2 (Must) excludes only a task no decision fits, and one fits.
     The funders, the Game Commission and DCNR's Bureau of Forestry, state a management aim
     ([Penn State release](https://www.psu.edu/news/research/story/deer-seedlings-and-soil-ph-influence-local-forest-regeneration)),
     and the abstract's main finding, that outcomes depended on initial seedling abundance, is the kind of effect a
     treatment model needs. USE-8 makes the marker the one for fit None, and the fit is approximate. Markers whose
     concern a test refuted were removed before (thyroid_discordant, Lennart, 2026-10-22; ames_housing and
     house_prices_nominal, 2026-10-26; ghcn_daily_precipitation, yours, 2026-10-30). Here the test bears the concern
     out in part, so these are not like cases. The like cases are the four `Yes` records under "Rule": boreal, rand
     and noaa keep the marker, while crms's REVIEW.md removes it as a record change without a mark (USE-8, fit
     approximate). Your answer here settles all five. The advocate and the critic both keep `Yes`.
   * For keeping the marker: your accepted screening kept it "as the marker of the concern", and the concern is
     borne out in part, since the decision is barely scored. `selection.md` allows a concern marker on a `Yes`.
   * Rule: SEL-3 and USE-2 (Must, hold); USE-1 and USE-8 (Must, met by the reworded text); the rest is a weighing of
     the fit. Decide alike with boreal_postfire_lichen_biomass, rand_health_insurance_experiment_doctor_visits,
     noaa_storm_events_damage and crms_phragmites_cover, which carry the same marker on a `Yes`.
   * Implemented: `Yes`, the use case reworded to the forecast that is scored, fit approximate; the marker still on
     the record.
   * Alternative (a): keep the marker as the concern. Alternative (b): `No` with the marker, if a forecast with the
     treatment as a weak input is not the task you accepted. No agent argues for (b).
   * A repair, if wanted later: the crews counted every species by height class (Sec. 2.3), so the authors hold the
     tallies for a target of desirable stems, and the 2014 basal area. No request was sent (your policy call 8).

   Recommendation: keep `Yes` and drop the marker. Decision: drop the marker, keep it (a), or `No` (b)?

2. **Stratify the site folds by state forest?** Each fold holds out 8 whole sites, drawn without regard to forest.
   The forests differ: Rothrock has about three times the deer (7.9-9.2 against 2.8-3.3 per km^2) and both sites
   with very many seedlings.
   * What it changes: in 15 of 60 test folds one forest has at most 2 of the 8 sites, and in one fold none, so that
     model trains on 12 sites of one forest and 4 of the other; a deployed model trains on 12 and 12. A fold's count
     RMSE is 13.8 when neither dense site is in it and 35.3 when both are (10 of 60 folds).
   * With `stratify_on = "state_forest"` every test fold holds 3-5 sites of each forest. The standard deviation of
     count RMSE across folds falls from 8.24 to 4.97 (across repeats from 2.30 to 1.81), and the two dense sites
     share a test fold 2 times in 60.
   * For: the training sides come closer to the 12 and 12 sites the deployed model sees (the advocate; SPLIT-1,
     Must, holds either way, so this is a weighing). Against: no rule asks for it, no grouped regression of the
     working copy uses it yet, and the critic calls it optional. The score rises; that is no reason either way
     (SPLIT-21).
   * Implemented: the default grouped folds.
   * Alternative: `stratify_on = "state_forest"`. Cost: a first for a grouped regression; the probe numbers in the
     notes are measured again.

   Recommendation: stratify. Decision: stratify, or keep the default folds?

3. **Accept `groups_test_groups_few` with the reason below?** The check warns that a test fold holds only 8 sites, so
   a score rests on few independent units. TP-5 (Must) holds: this is a regression with 85-88 scored microplots per
   test fold, and several model families beat the baseline at unseen sites (SPLIT-27; SPLIT-28 not triggered). The
   reason proposed for `accepted_check_warnings`: "All 24 sites of the study; holding out a site stands for a stand
   never followed. Each test fold scores 85-88 microplots of 8 sites, each site holding every treatment combination
   once beside 2-4 controls. The signal across sites is real: ridge, random forest, LightGBM and kNN reach R^2 0.148,
   0.336, 0.272 and 0.223 on log1p at unseen sites; the random forest beats the mean count on 56 of 60 shipped splits
   and scores 0.354 against at most 0.006 with the target shuffled. On the count, one site of the 8 holds about half
   of a fold's squared error."
   * Precedents: airfoil_self_noise (33 setups, 11 per fold) and open_university_learning_analytics_dataset (22
     presentations, 6-9 per fold), accepted on 2026-10-20 on the same evidence.
     south_nation_riparian_birds_insect_emergence, which the record's Assessment cites, is no size precedent: it had
     one row per site, and your reason for its `No` was "No good target".
   * If issue 2 changes the folds, the numbers in the reason follow.
   * What it changes: nothing in the data or the score; the reason tells a reader that each fold's score rests on 8
     sites, one of which carries about half the count-scale error.
   * Implemented: `accepted_check_warnings` left empty, as the add stage leaves it for you.
   * Alternative: leave the warning open (the check keeps flagging it), or `No` with `Too Small`, which TP-5 does not
     support here.

   Recommendation: accept. Decision: accept with this reason?

**Review panel:** ship after changes (mediator). Claim audit: 41 claims, 31 hold, 3 hold only in part (wording, now
fixed), 5 refuted (four record readings the add stage superseded, passed to the record, and the README's Mn unit,
now flagged as likely mg/kg), 1 contested (the metric, issue 4), 1 open (every tree species counted, now named).
Blind review: include with changes; its main concerns were the small size (our rules set no row floor; TP-5 holds)
and three columns it could not trace without the file (the file has them: the two all-height columns read by an
identity, `AL` by its missing pattern). Debate: agreed on the leak drops, the split by site, the reworded use case
and `fit_reason`, the notes and the laurel rename; disputed: the metric (after their checks the advocate argued for
`rmsle`, the critic for `rmse`; the mediator keeps `rmse`, issue 4); left to you as weighings: stratifying the folds
by forest, which both call optional (issue 2), and the marker (issue 1).

<details><summary>Mediator</summary>

**Mediator: pennsylvania_oak_hickory_regeneration_experiment (mediator, 2026-11-01)**

**Recommendation**

```text
Verdict: ship after changes.
Validity: SEL-3 and USE-2 hold (a treatment choice made from a pre-treatment inventory fits; Andrej's Yes of
  2026-10-30). USE-1 and USE-8 triggered, fixed in the text (the use case reworded to the regeneration forecast that is
  scored; fit_reason names its gaps; fit approximate). USE-5 holds, the all-species gap named (the 2021 level, not the
  paper's change). LEAK-10 triggered, fixed (11 post-treatment columns dropped; lime moves the 2014 pH by at most
  +0.12 against +1.18 for the 2016 pH). SPLIT-1, SPLIT-3, SPLIT-24 hold (grouped by the source's site; SPLIT-29:
  random microplots would overrate R^2 by 0.14-0.16); SPLIT-30, no hidden group. PROV-8 and PROV-13 hold (Dryad's own
  deposit, SHA-256 equal); PROV-2 notes corrected (7 undescribed columns, the Mn unit, the laurel index).
Value: TP-5 holds (8 sites, 85-88 scored microplots per test fold); TP-2, a small real signal (random forest R^2
  0.27-0.34 on log1p at unseen sites; the treatment flags add 0.018, SE 0.003); SPLIT-27 holds, SPLIT-28 not
  triggered; MET-3 holds; MET-11: the fallback rmse on the count stays, since the context for rmsle is not clear
  (decisive experiment below).
Quality: EV-8 wording fixed; the laurel column renamed as an index (PROV-2).
Weighed: source + (CC0 deposit of a randomised experiment, pinned by checksum); size - (24 sites); decision signal -
  (the treatment barely moves the score); gap 0 (screening).
For the curator: issue 1, a weighing call (keep Yes on the reworded use case and drop the marker); issue 2, a
  weighing call (stratify the folds by forest); issue 3, accept groups_test_groups_few; issue 4, the metric, decided
  with wadden and nantucket.
```

No validity Must fails on its own. Every point the panel raised has a remedy in the text, one rename, or a curator call.

**Agreed facts** (no agent disputes these after the rebuttals)

- Data: Dryad's deposit doi:10.5061/dryad.z8w9ghxnk (2024-09-25, CC0), fetched by script through the version download,
  SHA-256 equal to Dryad's digest. 261 microplots at 24 sites (22 with 11, one with 10, one with 9), 12 sites per
  forest. Every site holds each of the 7 treatment combinations once beside 2-4 controls.
- Timing: fences and lime went in after the 2014 inventory, herbicide in August 2015 (Sec. 2.2). The 11 dropped
  columns are later readings. The kept inputs show no treatment effect: with site fixed effects, lime moves `PH14` by
  +0.05 (CI -0.02 to +0.12) and `PH16` by +1.18. `AL` is missing exactly where `PH14` is, so it belongs to the 2014
  sample.
- File against README: 28 columns, 7 without a README entry (the notes say 2). The two all-height 2014 inputs are
  settled by an identity: each extra stem adds 0.0762 m, the midpoint of the 0-6 in class, in every row. The README's
  "262 rows" counts the header. `MN` in cmol(+)/kg is implausible (206 would be 5.7% of the soil's mass); mg/kg
  fits. 78 of 261 laurel values exceed the 15.4 m3 a plot can hold up to 1.8 m, so the "volume" is an index.
- Target: the 2021 count over 15 cm of "any live, arborescent, woody species" (Sec. 2.3), red maple and black birch
  included; the deposit has no species split. 48 zeros (18.4%) against 38 ones; zero in 39% of the plots empty in
  2014 against 12% of the others; a negative binomial on the inventory expects 48.2 zeros. The `Two-Regime Zeros` tag
  fails policy call 4.
- Split: grouped by site, 20 x 3; 8 test sites and 85-88 rows per fold; all 8 flag cells in every training side.
  Random microplots overrate R^2 (random forest 0.428 against 0.270; LightGBM 0.433 against 0.294). Site means hold
  52% of the log target's variance. No hidden group.
- Signal: ridge, random forest, LightGBM and kNN reach R^2 0.148, 0.336, 0.272 and 0.223 at unseen sites; the random
  forest scores 0.354 against at most 0.006 with the target shuffled and beats the mean count on 56 of 60 shipped
  splits. The 2014 count alone gives 0.22. The flags add 0.018 (SE 0.003). Within a site the random forest explains
  0.037; it picks the observed best treatment of a site 30.8% of the time with the flags and 30.0% without (chance
  14%). On stocking calls at held-out sites, carrying the 2014 count forward beats every untuned model (critic; my
  run below confirms it).
- Metric: the scorer computes RMSE on the count after expm1 (60 of 60 folds). On the count, one test site of 8 holds
  a median 50% of the random forest's squared error (up to 76%; 21% on log1p); 14 of 60 test folds hold no microplot
  with 69 or more seedlings; a ridge model on log1p scores a count RMSE of 2,543 after the inverse (30 splits). The
  two scales order 8 models at Kendall tau 0.21. TabArena's adapter scores `rmse` on the shipped log1p scale today,
  whatever is declared (definitions.md, "What the benchmark harness does").
- Folds by forest: 15 of 60 test folds hold at most 2 sites of one forest, one holds none. With
  `stratify_on="state_forest"` every fold holds 3-5 per forest. The two dense sites (`site_110`, `site_120`, both
  Rothrock) share a test fold in 10 of 60 folds, 2 of 60 when stratified.
- Record: "not downloaded", "about 5 sites (55 rows) per test fold in 5 folds", "south_nation ... confirmed
  `Too Small`" (its recorded reason was "No good target") and the change-score zero paragraph are superseded by the
  add stage; "Domoto M.E." is Emily J. Domoto (Crossref).

**The decisive experiment on the metric** (script, output and rows in the run folder)

The two sides crossed. The advocate (SILVAH thresholds, each misclassified plot counted the same) found that RMSLE
orders models like the forester's stocking decision. The critic (thresholds 1-50 stems, balanced accuracy) found
count RMSE closer per plot and RMSLE closer per site. I ran both designs on one set of 10 models (two dummies,
carrying the 2014 count forward, random forest on log1p with and without the flags, random forest on raw counts,
LightGBM on log1p and with a Poisson loss, ridge, kNN) over all 60 shipped splits, and resampled the splits 500
times. It is a diagnostic only; no threshold is declared (MET-7).

| Decision loss (60 splits, 10 models) | tau with count RMSE | tau with RMSLE | resamples where RMSLE is closer |
|---|---|---|---|
| plots misclassified, SILVAH thresholds (6-163 stems) | +0.29 | +0.60 | 93% |
| plots misclassified, thresholds 1-50 | +0.38 | +0.60 | 81% |
| 1 - balanced accuracy, SILVAH thresholds | +0.63 | +0.40 | 0% |
| 1 - balanced accuracy, thresholds 1-50 | +0.63 | +0.40 | 0% |
| error in the share of stocked plots per site, SILVAH | +0.38 | +0.51 | 67% |
| error in the share of stocked plots per site, 1-50 | +0.42 | +0.56 | 80% |

Without the two dummies (8 models): misclassified +0.00 against +0.36 (82%); balanced accuracy +0.57 against +0.07
(0%); share per site +0.14 against +0.21 (42%).

What it shows:
- The threshold set does not explain the crossing; the plot loss does. Counting every misclassified plot the same
  favours RMSLE. Weighing the two classes equally favours count RMSE in every resample: above SILVAH's thresholds
  stocked plots are the minority, so a missed one then counts more.
- Per site, on the share of stocked plots that SILVAH's decision charts read, neither metric is reliably closer once
  the dummies are left out.
- How a forester weighs a missed stocked plot against a false one is a cost no source fixes, and MET-7 forbids
  inventing it.
- The winners differ little. The model each metric picks per split has a share error of 0.092 (count RMSE) and
  0.088 (RMSLE), against 0.079 for the best pick. Neither metric ranks first the model the decision losses favour:
  carrying the 2014 count forward is best on all three, 6th of 10 by count RMSE and 5th by RMSLE.
- One claim made for RMSLE does not hold as stated: "the source models the counts on a log link". Sec. 2.4 on Dryad
  names glmmTMB with a site intercept and an observation-level random effect for overdispersion, but states no family
  or link, and its response is the 2014-2021 change, which can be negative.

Settled: MET-11 (Must) allows the context origin "only when the context is clear; otherwise the fallback". The
context is not clear here, so the fallback `rmse` on the count stays, the critic's final position. The tail facts go
into the notes (MET-10, as for nantucket). Whether the family of heavy-tailed counts should move to another metric
stays with the curator (issue 4), since wadden's issue 3 asks the same question.

**Changes to make now** (no decision needed; each was agreed by both sides or follows from a measured fact)

1. `predicted` and the target bullet: the count covers every tree species ("any live, arborescent, woody species",
   Sec. 2.3), red maple and black birch included; the deposit has no species split. USE-5, USE-8 (Must).
2. `question` and `use_case`: describe what is scored. A forester forecasts how many seedlings a plot will hold
   seven years after a planned treatment, from the pre-treatment inventory; the data shows the treatment's effect only
   weakly. Replace "names no such user" with: the funders (the Pennsylvania Game Commission and DCNR's Bureau of
   Forestry) state a management aim, and no prediction user is named. USE-1 (Must).
3. `fit_reason`, gaps in this order: all species counted, where a forester acts on desirable oak and hickory
   stocking; the treatment contrast weakly identified (one microplot per treatment per site; the flags add R^2 0.018;
   on stocking calls at held-out sites no untuned model beats carrying the 2014 count forward); treatments applied per
   8.6 m2 plot rather than per stand, the herbicide non-selective (this replaces "an 8.6 m2 microplot stands in for a
   stand"); no pre-treatment overstory, deer impact or fern cover in the file; two state forests and one 2014-2021
   cohort. Fit stays approximate. USE-8 (Must); USE-9's factor (a reworded use case excuses nothing).
4. `split` and `splits_comment`: the test sites are new sites of the Rothrock and Bald Eagle state forests, all
   followed over the same 2014-2021 years. USE-8.
5. A note that the fences were maintained yearly except in 2020 (Sec. 2.2), so `fence` records the assignment.
   USE-8.
6. The anomaly bullet: 7 file columns have no README entry, among them the two all-height 2014 inputs, read by the
   0.0762 m identity; the README's 262 rows include the header, so no row mismatch. Cite PROV-2 and EV-2, not
   PROV-15 (the deposit is the origin).
7. The `AL`/`MN` bullet: `MN` is stated in cmol(+)/kg, which is implausible (206 would be 5.7% of the soil's
   mass); mg/kg is likely, not checked with the lab. PROV-2 (Should).
8. Rename `mountain_laurel_volume_2014_m3` to `mountain_laurel_volume_index_2014` and say it is cover-class midpoint
   times height-class top (78 of 261 values exceed the 15.4 m3 a plot can hold). PROV-2; cheap and safe (principles,
   step 3).
9. The soil bullet: add the site fixed-effect bound (+0.05, CI -0.02 to +0.12, against +1.18 for `PH16`), Sec. 2.4's
   "soil pH varied among microplots both before and after treatment", and that no control at positions 2-4 has a soil
   value. LEAK-10 evidence (EV-6).
10. The probe bullet names its baseline and scale: better than the mean count on 30 of 30 splits, 24 of 30 against
    the back-transformed mean of log1p, 28 of 30 on the log scale. EV-8 (Should).
11. A metric note, as nantucket's: on the count, one test site of 8 holds a median half of the random forest's squared
    error (up to 76%; 21% on log1p), and a linear model on log1p can score in the thousands after the inverse.
    MET-10, MET-11.
12. Record (no mark needed): remove the `Two-Regime Zeros` tag (policy call 4: 48 zeros against 38 ones, and the zeros
    follow the 2014 count); "Domoto M.E." to "Domoto E.J."; a dated Assessment line superseding the access, fold,
    south_nation and change-score readings. EV-2, PROV-16, stage precedence.

After changes 8 and 11, re-run `dataset check` and the probes the rename touches.

**Changes that need the curator** (ranked: validity first, Must first)

1. Keep `Yes` on the reworded use case and drop `No Good Target / Scientific Discovery` (P3; SEL-3, USE-2, USE-8;
   a weighing). Problem: the decision, the treatment, barely moves the score (flags +0.018; best treatment picked
   30.8% against 30.0% without the flags). For dropping: a decision fits, so USE-2 does not apply; USE-8 makes the
   marker the one for fit None, and the fit is approximate; markers refuted by a test were removed (thyroid_discordant,
   ames_housing, house_prices_nominal, ghcn_daily_precipitation); the crms panel recommends the same. For keeping:
   Andrej's accepted screening kept it "as the marker of the concern", and the concern is borne out in part;
   `selection.md` allows a concern marker on a `Yes`. What would settle it: the curator's view of whether a forecast
   with the treatment as a weak input is the task he accepted. Recommendation: keep `Yes`, drop the marker.
2. Stratify the site folds by state forest (P4; SPLIT-1, no rule decides; a weighing). Advocate: closer to the 12
   and 12 sites a deployed model trains on; critic: optional. Fold spread of count RMSE 8.24 to 4.97 (per repeat 2.30
   to 1.81). The score rise (R^2 0.222 to 0.303) is no reason (SPLIT-21). A first for a grouped regression.
   Recommendation: stratify.
3. Accept `groups_test_groups_few` (P6; TP-5 holds; the curator fills `accepted_check_warnings`). Both sides accept;
   precedents airfoil_self_noise and open_university_learning_analytics_dataset. Recommendation: accept with the text
   in the draft.
4. The metric of the heavy-tailed count family (P6; MET-11, MET-1 Must; MET-10 Weigh). Settled here for `rmse` by
   MET-11's condition; the curator may still take the context for the family, deciding wadden's issue 3 and
   nantucket together. Recommendation: keep `rmse`.

**Disputed points**

| # | Point | Advocate (final) | Critic (final) | Rule and rank | Conflict or independent | Settled |
|---|---|---|---|---|---|---|
| 1 | Metric | `rmsle` from context (MET-1, MET-11) | fallback `rmse` (MET-11's condition not met) | P6; MET-11 and MET-1 Must, MET-10 Weigh | not a rule conflict: a fact about one rule's condition | decisive experiment: the ordering depends on an unfixed cost, so the context is not clear; `rmse` stays (critic). Family call: issue 4 |
| 2 | `stratify_on="state_forest"` | supports, as closer to deployment (SPLIT-1) | optional | P4; no rule requires or forbids it; SPLIT-21 bars the score as a reason | a weighing | curator, issue 2 |
| 3 | Rewrite `use_case` itself, or only `question` and `fit_reason` | conceded in rebuttal | `use_case` too (USE-1) | P3; USE-1 Must | agreed | change 2 |
| 4 | Is naming the weak treatment signal optional? | "independent of validity, does not stack" | a required fix | P3; USE-8 Must | an independent Must, met by the text | required (change 3); the critic is right on strength, both on the remedy |
| 5 | Rename the laurel column | notes only, then conceded | rename | P5 PROV-2 Should; principles step 3 | agreed | change 8 |
| 6 | The marker on a `Yes` | a record field for the curator | the curator's weighing | P2/P3; SEL-3, USE-2 | a weighing | curator, issue 1 |
| 7 | Blind reviewer 1: too small, a 500-row floor | dropped | dropped | TP-5 Must counts scored units per test fold; our rules set no row floor | | not a rule; TP-5 holds |
| 8 | Blind reviewer 2: three columns untraceable | settled by the file | same | EV-2 Must (a measurement on the source's file outranks its codebook) | | columns stay; change 6 says how they were read |
| 9 | Blind reviewer 4: `site` as a feature | `n_features` 12 | same | LEAK-33 | | settled: the group column is no feature |

**Consistency with precedent** (from the precedent checker's report, re-read)

- `Yes` on a designed experiment departs from the experiment rejects of 2026-10-30 (policy call 1: inputs that are
  only the design). The fact that sets it apart is written in the record and now measured: the 2014 inventory carries
  most of the signal (0.22 of 0.27-0.34). Consistent with rand_health_insurance_experiment_doctor_visits,
  boreal_postfire_lichen_biomass and crms_phragmites_cover.
- The marker: removal follows thyroid_discordant (Lennart, 2026-10-22), ames_housing and house_prices_nominal
  (2026-10-26), ghcn_daily_precipitation (Andrej, 2026-10-30) and the crms panel's recommendation. Here Andrej's CC
  accepted a screening that kept it as the concern, so I ask rather than remove. Decide alike with boreal, rand,
  noaa_storm_events_damage and crms.
- The warning follows airfoil_self_noise (33 setups, 11 per fold) and open_university_learning_analytics_dataset (22
  presentations, 6-9 per fold). south_nation_riparian_birds_insect_emergence differs in fact (24 rows, one per site)
  and in reason ("No good target"); the builder's draft and the record should not cite it for size.
- The target (the 2021 level, log1p, scored on the count) follows the accepted screening and MET-3 (Lennart,
  2026-10-21), as nantucket and wadden.
- The metric follows nantucket (fallback `rmse` with a tail note) and wadden's implemented `rmse`. It departs from
  blood_tests_drink_prediction and noaa_storm_events_damage (`rmsle` from context). The fact that sets it apart: here
  the relative-error context was measured and depends on an unfixed cost; the target spans 0-154, not nine orders of
  magnitude; no log-scale model of the source is verified. If the curator takes the context instead, the fact that
  sets it apart from wadden is the actor: a forester rates each plot against a threshold ladder, wadden's map maker
  sums densities.
- The tag removal follows policy call 4 as applied to basque_offshore_ctd_chlorophyll and how_much_did_it_rain_ii.
- `stratify_on` on a grouped regression has no precedent in the working copy, so it goes to the curator.
- Access is consistent with the other Dryad deposits of the run (boreal, nantucket: checked against Dryad's digests).
  The precedent checker's pair with metro_manila_village_weekly_dengue (2nd Tier for a manual download; its version
  download also works without a token, measured 2026-11-01) bears on Manila, not on this dataset. Raise it on
  Manila's record, not in this REVIEW.md.
- Builder citations to fix in the issues: PROV-2 and EV-2 for the README mismatch, not PROV-15; airfoil and OULAD for
  the size, not south_nation.

</details>

<details><summary>Claim audit</summary>

**Claim audit: pennsylvania_oak_hickory_regeneration_experiment (claim-auditor, 2026-11-01)**

**Verdict:** the definition's claims about itself mostly hold. 41 claims tested: 31 hold, 3 hold only in part
(documentation detail), 5 are refuted (four record lines superseded by the add stage, and the deposit README's Mn unit,
which the definition repeats), 1 metric claim is contested (a weighing call), and 1 implied claim is open. No validity claim is refuted: no leak, the split holds, and the target
is the source's own count. The open points are: what the target counts (all tree species, P3), the README/file anomaly
note (P5), and RMSE on the count against RMSLE (P6).

Scripts and outputs are in the run folder (raw-file tests, metric and fold tests, zeros and tail, soil timing
and log-error spread). Models are untuned, on the shipped splits (first 30 of 60 unless the table says otherwise), data rebuilt from
the definition (`dataset_io.definition(...).to_container()`).

**Claims table**

| # | Claim | Source | Test | Result | Evidence | Rule |
|---|---|---|---|---|---|---|
| 1 | Target: the 2021 count of tree seedlings over 15 cm, log1p, scored on the count; 18% zero | task_summary.predicted | count zeros; score a dummy with `scorer` on all folds against a hand-computed RMSE on `expm1` | holds | 48 of 261 zero (18.4%), integer counts; scorer equals count-scale RMSE on 60/60 folds, not the log-scale RMSE | MET-3 |
| 2 | 261 microplots at 24 sites, 9 to 11 each; 3.3 m across, 8.6 m2 | task_summary.row | group sizes | holds | 22 sites x 11, one x 10, one x 9; pi x 1.65^2 = 8.55 m2 | PROV-16 |
| 3 | Inputs include 2014 counts and aggregate heights "at all heights" (`*_W_UNDER_6IN`) | task_summary.known | all-height minus over-6-in, per extra stem | holds | all-height values >= over-6-in in every row; each extra stem adds 0.0762 m (median and pooled), the midpoint of the 0-6 in class: the columns are all heights | USE-3 |
| 4 | Whole sites held out, 8 per fold, every combination in training | task_summary.split, splits_comment | count test sites and treatment cells per training side | holds | 8 test sites on 60/60 folds, 85-88 rows; all 8 flag combinations in every training side | SPLIT-24 |
| 5 | 261 microplots, 28 columns; SHA-256 equals Dryad's | curation bullet 0, download_description | re-downloaded the version zip into scratch (2026-11-01) | holds | HTTP 200 via the API redirect, both digests equal Dryad's file listing (c183bb..., 53835f...) | PROV-13 |
| 6 | Fences and lime "immediately following a full vegetation inventory"; herbicide after the 2015 season (17-28 Aug 2015) | bullet 1 | read Dryad methods Sec. 2.2 | holds | both quotes in the Dryad methods text, Sec. 2.2 | USE-3, PROV-16 |
| 7 | Each 2014-2021 change equals 2021 minus 2014 (heights to 0.1 m); 2 empty rows; 3 missing controls (137/3, 149/2, 149/3) | bullet 2 | recompute | holds | count deltas exact; height deltas max error 0.1 m; 263 lines, 2 all-NA; the three microplots missing | PROV-15 |
| 8 | "`PH16` and `AL` are in the file and not described" (the anomaly in full) | bullet 2 | match the 28 file columns against the 22 README entries | refuted in part | 7 file columns have no README entry, not 2: also `SEED14_COUNT_W_UNDER_6IN`, `SEED21_COUNT_W_UNDER_6IN`, `SEED14_AGG_HT_W_UNDER_6IN`, `SEED21_AGG_HT_W_UNDER_6IN`, `DELTA_COUNT_UNDER_6IN`; two of them ship as features (row 3 settles their meaning) | PROV-15 |
| 9 | "the README says 262 rows, the methods n = 261" (a mismatch) | bullet 2 | read the README line | refuted in part | the README says "21 columns and 262 rows (first-row headers)": 262 with the header row is 261 microplots, so no mismatch on rows | PROV-15 |
| 10 | Level and change carry the same information on the count; aggregate height zero in the same 48; skew 2.93 / 0.43, median 4, max 154 | bullet 3 | identity; recompute | holds | count error on level = error on change (identity, given the 2014 count); 48/48 overlap; skew 2.93 and 0.43, median 4, max 154 | USE-5, CLEAN-16 |
| 11 | The zeros are the low end of the count, not a regime of their own; 39% vs 12% | bullet 4, Decision 2 | negative binomial GLM on the 2014 inventory and treatments: expected zeros against observed | holds | NB expects 48.2 zeros (simulated 95% range 37-60) against 48 observed; with site effects 44.3 (34-55); Poisson expects 8.6. 24/62 and 24/199 | EV-1 |
| 12 | Post-treatment columns dropped; PH16 4.27 vs 3.12; BA and CANOPY have no 2014 counterpart | bullet 5 | file columns; group means | holds | PH16 limed 4.27 vs 3.12 (MWU p 2.4e-15); no 2014 BA or canopy column in the file | LEAK-10 |
| 13 | 2014 soil predates the lime (MWU p 0.51, 0.92, 0.24) | bullet 6, Decision 1 | OLS with site fixed effects and all three flags, PH14 against PH16 | holds | lime coefficient on PH14 +0.05 (95% CI -0.02 to +0.12) against +1.18 (1.01 to 1.35) on PH16: any lime effect on PH14 is below a tenth of the 2016 one. Primary text also supports it: Sec. 2.4, "soil pH varied among microplots both before and after treatment" | LEAK-10, EV-6 |
| 14 | Soil missing in 72 microplots, 69 of them controls 2-4, sampled "when time allowed" | bullet 6 | missingness by microplot | holds, detail missing | none of the 69 microplots at positions 2-4 has a soil value (0 of 69), so in this file time never allowed; the other 3 missing values are at microplots 1, 5, 6. Missing-indicator R^2 alone -0.029 (leak probe) | LEAK-10 |
| 15 | `AL` is 2014 aluminium | bullet 7 | missingness pattern; lime effect | holds | missing in exactly PH14's 72 microplots, not PH16's 69; lime coefficient -0.22 (CI -0.74 to +0.30) although lime raised pH by 1.2 by 2016 | PROV-15 |
| 16 | `MN` is "given in cmol(+)/kg" (as published, unit not checked) | bullet 7 | plausibility; the sister Dryad deposit of the same study (doi:10.5061/dryad.dr48cf6) | refuted (the README's unit) | 206 cmol(+)/kg of Mn2+ would be 56,600 mg/kg, 5.7% of the soil's mass; the sister deposit's abstract calls Mn "exceeded 0.1 cmolc/kg" the high end; the file's values (1.7-206) fit mg/kg (0.1 cmolc/kg = 27 mg/kg) | PROV-15, CLEAN-1 |
| 17 | `UID` = PLOT x 100 + SUBPLOT; `TRT` one to one with the flags; subplot 5 always the fence; controls at 1-4 | bullet 8 | recompute | holds | 261/261; one-to-one both ways; subplot 5 = F at 24/24 sites; subplots 1-4 = C (93 rows) | CLEAN-3, CLEAN-5 |
| 18 | `PLOT` is the site, its first digit the forest | bullet 8 | crosstab | holds | 1xx = Rothrock (129), 2xx = Bald Eagle (132) | |
| 19 | Deer density Rothrock 7.9-9.2, Bald Eagle 2.8-3.3 per km2 (2018-2019) | bullet 9 | Sec. 2.1 text | holds | quoted in the Dryad methods text | PROV-16 |
| 20 | Fence alone always at microplot 5, not randomised over positions; the other six randomised over 6-11, each once per site | bullet 10 | crosstab; pre-treatment soil by position (site fixed effects) | holds | each site holds all 7 combinations once; positions 6-11 spread roughly evenly; supports the caution: 2014 Al is higher at microplots 1-5 than 6-11 (+0.83 at controls, p 0.04; +0.90 at 5, p 0.03) | USE-8 |
| 21 | No duplicate rows | bullet 11 | duplicates without ids; exact feature copies across the split | holds | 0 duplicates; 0% of test rows with an exact feature copy in train (leak probe) | LEAK-16 |
| 22 | RF R^2 0.28 on log1p; RMSE 17.7 against 23.3 for the mean count, better on every one of 30 splits | bullet 12 | rerun RF (seed 1), compare with three dummies | holds as written, with a qualifier | R^2 0.272, RMSE 17.72; better than the mean-count dummy on 30/30, but against the dummy a harness fits on the shipped target (mean log1p, back-transformed, RMSE 23.55) on 24/30 (80%), and on the log scale on 28/30 (task probe) | EV-8 |
| 23 | Treatment flags add R^2 0.018 (SE 0.003, 93% of splits) | bullet 12 | RF with and without the flags, also on the declared metric | holds | R^2 +0.0179 (SE 0.0031, 90%); on the count RMSE the flags gain 0.31 seedlings (SE 0.04, 97% of splits) | TP-2 |
| 24 | Change in log count +0.48 (fence alone) to -0.37 (herbicide alone) | bullet 12 | group means | holds (descriptive) | F +0.48, H -0.37, FL +0.47, C -0.06; raw means, the fence-alone one confounded with position (row 20) | |
| 25 | 2014 count alone R^2 0.22; LightGBM loses 0.14 by site; site means hold 52% of the variance | bullet 12 | probe outputs; eta-squared | holds | 0.222 (leak probe); 0.433 vs 0.294 (group probe, 3x3); eta^2 0.521 against 0.088 expected by chance | SPLIT-29 |
| 26 | 24 sites drawn from 100; 11 plots in 110 x 52 m; site as a random intercept; context all_rows | grouping.definition | Sec. 2.1, 2.2, 2.4 text | holds | quoted in the Dryad methods | SPLIT-24 |
| 27 | Stricter than the source, which fits all 24 sites with a site random effect | splits_comment | Sec. 2.4 | holds | "Site was included as a random intercept effect" | SPLIT-5 |
| 28 | Metric origin: the source ranks GLMMs by AIC and reports no prediction error; fallback `rmse` | metric reason | read Sec. 2.4; looked once more for the paper | holds | Sec. 2.4: AIC over four model sets; the publisher answers 403 to WebFetch (full and PDF), Europe PMC has 0 hits; Unpaywall lists the paper as hybrid open access, CC BY, at the publisher only | MET-1, MET-11 |
| 29 | Metric computable on our data and folds | metric (MET-2) | dummy scored with `scorer` on all 60 folds; units per fold | holds | no scoring columns needed; RMSE 6.9-41.8 per fold; 85-88 rows, 8 sites, 8-26 zeros per test fold | MET-2 |
| 30 | Metric means what the source's response meant | metric (MET-2) | identity on the count scale | holds | an error on the 2021 level equals the error on the 2014-2021 change given the 2014 count; source response on the count scale | MET-2 |
| 31 | Fallback condition: the task makes no metric obvious, so RMSE on the count | metric (MET-11), README "Metric" | SSE concentration per fold; ranking of 8 models under count RMSE and log RMSE; a linear model under the inverse; sibling definitions | contested | on the count, one test site of 8 holds a median 50% of the RF's squared error (max 76%; 60% and 92% for the dummy), the top 5% of rows 58%; 14 of 60 folds hold no microplot with 69 or more seedlings; on log1p the top site holds 21% (max 29%), the top 5% of rows 27%. The two scales rank 8 models at Kendall tau 0.21 (RF on raw counts best on the count, 5th on log; RF on log1p 1st on log, 3rd on count). A ridge fit on the shipped log1p predicts up to 13.2 (541,055 seedlings): count RMSE above 50 on 15 of 30 splits. Precedents went both ways: `rmsle` from context for blood_tests_drink_prediction (Lennart's CC) and noaa_storm_events_damage; the fallback `rmse` on the count in this batch for nantucket_sound_sea_duck_aerial_survey_counts | MET-1, MET-10, MET-11 |
| 32 | Accept `groups_test_groups_few`: signal across sites is real (R^2 0.148/0.336/0.272/0.223; RF beats the dummy on 28/30) | proposed warning | group probe numbers; permutation null (target shuffled, 20 runs, 3 splits) | holds | RF R^2 0.354 observed against a permuted maximum of 0.006 (mean -0.116) | TP-5, SPLIT-27 |
| 33 | Bibliography, year, licence | bibtex, year, license | Crossref, Dryad API | holds | Crossref: 54(11):1367-1375, authors as in the bibtex; Dryad: CC0-1.0, 2024-09-25 | PROV-16 |
| 34 | "Not downloaded (Dryad answers 401 to file requests)" | record, screening and later comment | download | refuted (superseded) | the version download works without a token (row 5) | EV-2 |
| 35 | "about 5 sites (55 rows) per test fold in 5 folds" | record, Assessment 2026-10-30 | shipped splits | refuted (superseded) | 3 folds of 8 sites, 85-88 rows | EV-2 |
| 36 | A microplot split would leak the site | record, Assessment | group probe | holds | LightGBM R^2 0.433 random vs 0.294 by site | SPLIT-29 |
| 37 | Tag `Two-Regime Zeros`; "a 0 is no net change" of a change score | record tags, comment | NB expected zeros (row 11); the shipped target | refuted | the shipped target is the 2021 level, and its zeros match a negative binomial (48.2 expected, 48 observed) | EV-1, EV-2 |
| 38 | Reference "Domoto M.E." | record, Reference | Crossref | refuted | Emily J. Domoto | PROV-16 |
| 39 | south_nation_riparian_birds_insect_emergence (24 sites, `Too Small`) "the same call would follow here" | record, Assessment | its record | holds in part | south_nation has one row per site (24 rows); this has 261 rows in 24 sites, 85-88 scored rows per fold, so its fact does not carry over; the independent units (sites) are 24 in both | TP-5 |
| 40 | Implied: every feature is known at the prediction point | (implied) | balance of each kept input against each treatment, site fixed effects | holds | 2014 counts, laurel and soil show no treatment effect of the size the 2016 values show; the lime effect on PH14 is bounded at 0.12 | LEAK-10, USE-3 |
| 41 | Implied: the target is what the forester acts on in an oak-hickory stand | unique_name, use_case | Sec. 2.3 and the README | open (untested on data) | the count sums "any live, arborescent, woody species" (Sec. 2.3) over the height classes (README `COUNT21`), so red maple and black birch, named as common in Sec. 2.1, count the same as oak; the deposit has no species split, so no test or repair is possible here; neither `predicted` nor `fit_reason` names it | USE-5, USE-8 |

The builder's line "the harness scores the shipped log1p scale" (draft issue 4) does not hold for the repository's scorer
(row 1: it scores the count after `expm1`); a harness outside the repository is untested here.

**Refuted, contested and open claims, ranked (principles.md: validity first, Must first)**

1. **What the target counts (P3; USE-5, USE-8, Must). Open.** The name and the use case point to oak-hickory
   regeneration; the target counts every tree species over 15 cm, competitors included (Sec. 2.3). This is the
   source's own response, so the label is not wrong; the gap is that it goes unnamed. Effect: the forester use case is
   further from a stocking decision than `fit_reason` says. Mildest remedy: one clause in `predicted` and
   `fit_reason` ("all tree species, desirable or not; the deposit has no species split"). The fit stays approximate.
2. **The README/file anomaly note is incomplete (P5; PROV-15, Must). Refuted in part (rows 8, 9, 16).** Seven file
   columns are undescribed, not two, and two of them ship as features. Their meaning is settled by the 0.0762 m per
   extra stem (row 3), and the note should say so. The README's "262 rows" counts the header row. The README's Mn
   unit is implausible: the values fit mg/kg. Effect: documentation only; no model input changes. Mildest remedy:
   rewrite the anomaly bullet and the `MN` sentence ("unit stated as cmol(+)/kg, implausible: likely mg/kg").
3. **RMSE on the count as the fallback (P6; MET-1, MET-10, MET-11). Contested: a weighing call for the curator
   (row 31).** The fallback is computable and honest, but on this target it mostly scores how well a model predicts
   the one or two dense sites in each test fold. A linear model on the shipped scale blows up under the inverse. The
   two scales rank models differently (tau 0.21). RMSLE (`Metric.from_context("rmsle", target_transform="log1p")`)
   spreads the score over sites (top site 21% against 50%) and still resolves the treatment signal (R^2 +0.018,
   SE 0.003). The precedents split: the curator's CC on blood_tests_drink_prediction and the noaa_storm_events_damage
   reasoning favour RMSLE, while this batch's nantucket_sound count kept RMSE. Mildest remedy: declare `rmsle` from
   context, with the reason "a regeneration count's error matters relative to the count; on the count, one site of
   eight holds half the squared error". The alternative is to keep `rmse` and write the tail numbers into the notes.
   If RMSLE is chosen, bullet 3's "the same error on the other" sentence has to be reworded (on the log scale the level
   and the change are no longer one error), though the level stays the right target.
4. **Record fields (EV-2; the add stage supersedes the screening). Refuted (rows 34, 35, 37, 38).** Remove the
   `Two-Regime Zeros` tag: the zeros match a negative binomial. Fix "Domoto M.E." to "Emily J.". Supersede the
   "not downloaded" and "5 folds of 55 rows" readings with an Assessment line. The curator applies these: they are
   record fields.
5. **Wording of the probe bullet (EV-8, Should). Holds with a qualifier (row 22).** "Better than the dummy on every one
   of 30 splits" is true against the mean count. It is 24 of 30 against the constant a harness fits on the shipped
   log1p target, the baseline under the declared metric. Mildest remedy: name the dummy, or add "(24 of 30 against the
   back-transformed mean of the log1p target)".
6. **Soil bullet detail (LEAK-10; EV-6). Holds; stronger evidence available (rows 13, 14).** Add the site-fixed-effect
   bound (lime effect on PH14 at most +0.12 against +1.18 on PH16) and the Sec. 2.4 quote. Say that no control at
   positions 2-4 has a soil value.

**Untested**

* The paper beyond the methods on Dryad: the results, the GLMM family, the species in the counts (PROV-17). The
  publisher answers 403 to automated requests, but Unpaywall lists the paper as CC BY open access. A curator can open
  <https://doi.org/10.1139/cjfr-2024-0034> in a browser and settle point 1 and the metric reason in minutes.
* The TabArena harness's handling of `target_transform` (outside the repository).
* The post-treatment columns' R^2 +0.048 (builder): not re-run. It changes no decision, because these columns go
  whatever they score (EV-2).

</details>

<details><summary>Column audit</summary>

**Column audit (column-auditor, 2026-11-01): pennsylvania_oak_hickory_regeneration_experiment**

**Verdict:** no leak and no cleaning problem that needs a fix. The 12 features are the pre-treatment inventory plus the
treatment decision, and a randomisation check on the data confirms each was recorded before the treatments. All 11
post-treatment columns are dropped correctly. Three mild points remain, all about documentation: (1) `fit_reason` does
not say that the file has no pre-treatment overstory or light measure, although that is the part of the forester's
inventory the drops cost most (P3, USE-8); (2) two stated units do not hold up: `MN` in cmol(+)/kg and laurel "m3"
(P5, PROV-2); (3) the builder's issue 5 cites PROV-15, which covers third-party copies; the rule for an unclear detail
of the origin is PROV-2.

Prediction point used: the site's full 2014 vegetation inventory. Fences and lime went in "in the summer of 2014 (27
May-14 Aug) immediately following a full vegetation inventory", and herbicide went on 17-28 Aug 2015 (Sec. 2.2, Dryad
methods). Codebook: the deposit's `README.md` (it describes 22 columns under other names), plus Sec. 2.1-2.4 as
reproduced on Dryad. I matched the file's names to the README by content, as the builder did, and re-checked the
mapping (see the table).

How "known at prediction?" was tested: lime, herbicide and the fence combinations were randomised over microplots 6-11
of each site (Sec. 2.2). A value recorded before the treatments therefore cannot differ by treatment within a site.
For each column I compared within-site-centred values by flag on microplots 6-11, using 4,000 stratified
permutations, and ran an OLS with site fixed effects and all three flags, with SEs clustered by site.

**Shipped columns (261 rows, 14 columns: 12 features, the group, the target)**

| column | meaning (codebook) | known at prediction? | dtype and cleaning | verdict | rule |
|---|---|---|---|---|---|
| `log1p_seedlings_over_6in_2021` (target) | log(1 + count) of tree seedlings (woody, at most 2.54 cm DBH) over 0.15 m on the 8.55 m2 microplot in the 2021 survey (README `COUNT21`, file `SEED21_COUNT_OVER_6IN`; Sec. 2.3) | the outcome, 7 years after the prediction point | float64; whole counts 0-154, none missing; logged for skew (2.93 to 0.43) and named after the transform; scored on the count. Mapping checked: the 2021 aggregate height is zero in the same 48 rows, and height per stem lies within the class midpoints (0.20-1.80 m) in every row | fine. Note: a stem that grew past 2.54 cm DBH by 2021 leaves the count (Sec. 2.3); the source's response shares this. No sign of mass outgrowth: 16 of 213 microplots with stems average over 1.2 m per stem in 2021, against 17 in 2014 | CLEAN-16, MET-3, USE-5 |
| `state_forest` | Rothrock or Bald Eagle (`STUDY_AREA`); Rothrock has more deer (7.9-9.2 against 2.8-3.3 per km2 in 2018-2019, Sec. 2.1) | yes, a fixed attribute of the stand | category, 2 levels (`BaldEagle` 132, `Rothrock` 129; the file spells it without the space); equals the site id's first digit in every row | fine; removing it changes R^2 by -0.002 (SE 0.004) | CLEAN-14 |
| `fence` | microplot inside a 1.8 m deer fence (`FENCE`) | the decision; installed after the 2014 inventory | category Yes/No (from Y/N); 96 Yes; with `lime` and `herbicide` one to one with `TRT` (crosstab, every row) | fine. The flag records the assignment: fences were not maintained in 2020 (Sec. 2.2), and the fence alone is always microplot 5, not randomised (already in the notes) | CLEAN-14, USE-6 |
| `lime` | 6.7 kg dolomitic lime per microplot, summer 2014 (`LIME`) | the decision | category Yes/No; 96 Yes | fine | CLEAN-14, USE-6 |
| `herbicide` | triclopyr and glyphosate broadcast, 17-28 Aug 2015 (`HERB`) | the decision (applied after the 2015 survey) | category Yes/No; 96 Yes | fine | CLEAN-14, USE-6 |
| `seedlings_over_6in_2014` | 2014 count of seedlings over 0.15 m (`COUNT14`) | yes: no difference by treatment within sites (lime p 0.31, herbicide 0.93, fence 0.55) | float64, whole numbers 0-224, none missing | fine; the strongest single input (R^2 0.22 alone, builder's probe) and the core of the task | LEAK-10 holds |
| `aggregate_height_over_6in_2014_m` | sum over height classes of count x class midpoint, in m, rounded to 0.1 (`AGGHT14`) | yes (p 0.57 / 0.98 / 0.61) | float64 0-107.5; zero exactly where the count is zero; 0.20-1.80 m per stem | fine | LEAK-10 holds |
| `seedlings_all_heights_2014` | 2014 count including the under-0.15 m class (file `SEED14_COUNT_W_UNDER_6IN`; the README's text for this pair is garbled) | yes (p 0.35 / 0.96 / 0.25) | float64 0-294. The "all heights" reading holds: the count is at least the over-6-in count in every row, and aggregate height (all) minus aggregate height (over 6 in) equals 0.0762 m (the 3 in midpoint) x the difference in count, within the 0.1 m rounding, in every row | fine | LEAK-10 holds |
| `aggregate_height_all_heights_2014_m` | the same index over all height classes | yes (p 0.51 / 0.99 / 0.47) | float64 0-111.4 | fine | LEAK-10 holds |
| `soil_ph_2014` | 2014 pH in 0.01 M CaCl2, Oa and A horizons pooled (`PH14`; Sec. 2.3) | yes: the lime coefficient with site fixed effects is +0.05 (SE 0.04) on all rows and +0.01 (SE 0.05) on microplots 6-11, against +1.18 and +1.16 for `PH16` | float64 2.47-4.44. 72 missing: 69 are controls 2-4, sampled "when time allowed" (Sec. 2.3), and 3 are at site 140 (microplots 1, 5, 6). Kept missing. The missingness is not caused by the outcome (2014 sampling; among controls, mean log target 1.63 sampled against 1.59 not sampled) | fine. Herbicide microplots read 0.12 lower (p 0.006 on 6-11). That is a chance imbalance and not a timing sign: herbicide came in Aug 2015, and lime shows no 2014 effect | LEAK-10, CLEAN-2 |
| `soil_al_2014` | `AL`, not in the README; read as 2014 KCl-extractable aluminium | yes. It is missing exactly where `PH14` is, including the 3 rows where `PH16` exists, so it belongs to the 2014 sample and not the 2016 one. Among limed microplots it tracks `PH14` (Spearman -0.55), not `PH16` (-0.17). Lime coefficient on log AL: -0.12 (p 0.18) on all rows, +0.15 (p 0.24) on 6-11 | float64 0.08-16.38; no unit stated (plausible as cmol(+)/kg); shipped as published | fine; the builder's reading is supported | PROV-2 |
| `soil_mn_2014` | 2014 KCl-extractable Mn; README says "cmol(+)/kg" | yes (lime coefficient on log MN +0.18, p 0.10, on all rows; -0.04, p 0.79, on 6-11) | float64 1.69-206.2. The stated unit is implausible (inference, not checked against the lab): the mean of 41 is 15 times the Al of the same samples, more than the whole exchange capacity of a pH-3 Oa/A horizon would hold. mg/kg would fit | fine as data (a scale does not change a model); unit question for the notes | PROV-2 |
| `mountain_laurel_volume_2014_m3` | 2014 mountain laurel "volume": cover-class midpoint x upper bound of the height class (`PRE_TRT_KALA_VOL`) | yes. Zero in 27.2% of microplots, matching "mountain laurel was present at 73% of plots (n = 261)" at establishment in 2014 (Sec. 2.1). No difference by treatment (p 0.47 / 0.49 / 0.64) | float64 0-66.73. Zeros are absences, not proxy missing values. "m3" is the source's label, but 78 rows exceed 15.4 m3, all a 8.55 m2 microplot can hold up to the 1.8 m top class, so the values are an index (percent cover x height) | fine; naming note | CLEAN-10, PROV-2 |
| `site` | sampling site (`PLOT`: forest digit + site number) | group column, not a feature | category, 24 levels, 9-11 rows each; kept out of the features (`n_features: 12`; the probes saw 12) | fine | LEAK-33, CLEAN-3 |

**Dropped source columns**

| column | why it goes | check | verdict | rule |
|---|---|---|---|---|
| `UID` | `PLOT` x 100 + `SUBPLOT` in every row | builder's check, re-read | drop right | CLEAN-3 |
| `PLOT` | becomes the group `site` | | right | CLEAN-3 |
| `SUBPLOT` | the microplot number: 1-4 controls, 5 always the fence, 6-11 random (crosstab confirms); a new stand has no such number | added back, R^2 -0.002 (SE 0.002) | drop right | CLEAN-3, USE-1 |
| `TRT` | one to one with the three flags (crosstab, 8 codes, every row) | | drop right | CLEAN-5 |
| `SEED21_*` (3 besides the target), `DELTA_*` (4) | the 2021 outcome and the 2014-2021 differences | each delta equals 2021 minus 2014 (counts exact, heights to 0.1 m) | leak, drop right | LEAK-10 |
| `PH16` | 2016 soil pH, after lime | lime +1.16 pH units with site fixed effects on 6-11 (p < 0.001) | leak, drop right | LEAK-10 |
| `LOGIT_CANOPY_OPEN16` | canopy openness at 1 m from a 2016 fisheye photo | no treatment effect visible (within-site p 0.88 / 0.14 / 0.61), but it was taken two years into the outcome window, so it carries any 2014-2016 change. Added back: R^2 +0.056 (SE 0.006, better on 97% of 30 splits), the largest single cost of the drops | drop right. No keep clause of LEAK-10 applies: every cell is a later reading | LEAK-10 |
| `AVG_BA_m2_ha` | plot (168 m2) basal area of trees over 12.7 cm DBH, averaged over 2014, 2015, 2016, 2018 and 2021 | no treatment effect (p 0.46 / 0.39 / 0.90). Added back: R^2 +0.012 (SE 0.004) | drop right. The window ends at the outcome. The window-sum keep clause needs data showing the average does not move with the outcome, which cannot be shown without a 2014 value | LEAK-10 |
| `AVG_POST_TRT_KALA_VOL_M3_1621` | laurel volume averaged over the surveys after the herbicide | herbicide lowers it (-3.7 within sites, p 0.03). Added back: +0.001 | leak, drop right | LEAK-10 |

**Problems, ranked (principles.md)**

1. **P3, USE-8 (Must, documentation-level): the fit does not name the missing overstory.** A forester's pre-treatment
   inventory includes overstory density or light (the screening cites SILVAH), and the source's own models use `BA`,
   `KALMIA` and `OPEN` as covariates (Sec. 2.4). The file holds these only as post-treatment values, and they are
   dropped correctly. They are what the drops cost most: canopy 2016 adds R^2 +0.056 back and basal area +0.012. The
   notes say "The README's `BA` and `CANOPY` have no 2014 counterpart in the file, so no lag is possible", but
   `fit_reason` and `known` do not name the gap. Mildest remedy: add a clause to `fit_reason`, for example "and the file
   has no pre-treatment overstory or light measure, which an inventory would hold". An optional repair from the origin
   (PROV-13 spirit): the README says tree DBH was recorded in 2014, so the authors could supply the 2014 basal area and
   the described but missing `PRE_TRT_ALL_COMP_VOL`. That is a request to the authors, not a blocker.
2. **P5, PROV-2 (Should): two stated units do not hold, and one rule is mis-cited.** (a) `MN` "cmol(+)/kg": values of
   1.7-206 (mean 41, 15 times the Al of the same samples) are implausible in that unit and would fit mg/kg. This is
   inference; the notes already say "unit not checked". (b) `mountain_laurel_volume_2014_m3`: 78 of 261 values exceed
   the 15.4 m3 the microplot can hold up to 1.8 m, so the "m3" in the source and in our column name labels an index.
   (c) The builder's issue 5 and its checklist cite PROV-15 (errors in third-party copies) for the README/file
   mismatch. The deposit is the origin, so the rule is PROV-2: an unclear detail stays, with a note. Mildest remedy: one
   sentence in the `AL`/`MN` anomaly bullet ("the stated unit of `MN` is implausible: likely mg/kg"; "the laurel volume
   is an index, cover percent x height, not m3"), and optionally rename the column to
   `mountain_laurel_volume_index_2014`. Neither changes a model or a score.
3. **P7, no action:** counts are stored as float64 (numeric by meaning, CLEAN-14 allows it); `BaldEagle` keeps the
   file's spelling. Both are cosmetic.

Checked and not a problem: no proxy missing values (laurel and seedling zeros are observed absences; the soil NAs are
the README's "data not collected"); no impossible values (pH 2.47-4.44, counts at least 0, heights per stem inside the
class bounds); no reversed encodings; no column whose missingness follows the outcome; no id that encodes the label
(`SUBPLOT` encodes the treatment group, and it is dropped); the group column is not a feature; rows are shuffled
(CLEAN-23). Soil is worth keeping: removing the three soil columns costs R^2 0.033 (SE 0.010).

Evidence, scripts and numbers (untuned random forest, log1p target, the first 30 shipped splits) are in the run
folder: a profile through `dataset_io`, consistency, balance and missingness checks, site fixed-effects soil
models, and added and removed columns.

</details>

<details><summary>Split audit</summary>

**Split audit (split-auditor, 2026-11-01): pennsylvania_oak_hickory_regeneration_experiment**

**Verdict: right with notes.** Grouping by site is the right regime, and it uses the source's own site id. No hidden
group or copy crosses the split. Nothing in the split breaks a Must. The notes are about fold balance, how
concentrated the count-scale score is, and the wording of the warning and the split text.

```text
Validity: USE-10 holds (cold start: a new stand has no outcomes); SPLIT-1, SPLIT-3, SPLIT-4 hold (grouped by site);
  SPLIT-24, SPLIT-26 hold (the source's PLOT = site, its random intercept); SPLIT-29 measured (IID would overrate by
  about 0.15 R^2: keep grouped); SPLIT-30 no hidden group; SPLIT-7 to SPLIT-10 not triggered (no time axis across rows).
Value: SPLIT-27, SPLIT-28 hold (several families above the baseline on unseen sites); TP-5 not triggered (regression,
  85-88 scored rows per fold), but two sites decide the count-scale fold score (MET-1/MET-10 question, issue 2).
Weighed: few groups - (24 sites, 8 per test fold); source + (randomised design, site documented).
For the curator: issue 1, an optional re-split stratified by forest; issue 2, state the site concentration when
  accepting groups_test_groups_few.
```

**How it was checked.** Everything was loaded through `dataset_io.load(..., built=False)` (a container rebuilt from
`dataset.py`) with threads capped. Scripts and outputs are in the run folder. The models are untuned: a random forest (300 trees, min
leaf 3) and ridge, both fit on the log1p target and scored on the log scale and on the count after expm1 (the
declared metric). The comparisons use 10x3 folds per split scheme, and also all 60 shipped splits. The source's
design comes from Sec. 2.1-2.4 as reproduced on Dryad.

**What holds (checked with numbers)**

- **Regime (USE-10, SPLIT-1, SPLIT-3, SPLIT-4).** In the use case a forester predicts for a stand whose
  pre-treatment inventory is known and whose outcomes are not. That is a cold start on a new entity, and a grouped
  split tests it. An IID split by microplot would stand for a stand where some microplots' 2021 outcomes are already
  known, and no decision looks like that. A temporal split is impossible: every row is the same cohort (2014
  inventory, 2021 survey).
- **The gap (SPLIT-29).** Random forest: R^2 (log) 0.428 on random microplots against 0.270 grouped by site (10x3 each). LightGBM from the group probe: 0.433 against 0.294. Site means hold 52.1% of the log target's
  variance and 61.6% of the count's. An IID split would reward recognising the site.
- **True group id (SPLIT-24, SPLIT-26).** `site` is the source's `PLOT` and the source's random intercept ("Site was
  included as a random intercept effect to account for potential similarities among microplots within a sampling
  site", Sec. 2.4). It is not a cluster or a hash. There are 24 sites: 22 with 11 microplots, one with 10, one with
  9. Its first digit is the forest (1xx Rothrock, 2xx Bald Eagle, 12 sites each).
- **Split integrity.** In all 60 shipped splits (20 repeats x 3 folds) no site is on both sides and every partition
  is complete. Every test fold holds exactly 8 sites and 85-88 rows, and between 8 and 26 zero counts. Both forests
  are in every training side.
- **Fold content.** Each of the 24 sites holds each of the 7 non-control combinations exactly once, plus 4 controls
  (3 controls at site 137, 2 at site 149). So `task_summary.split` ("every treatment combination is in training at
  other sites") and `splits_comment` ("each with every treatment combination") are true.
- **Hidden groups (SPLIT-30).** I ran `hidden_groups.py --include-grouped`, which treats the task as IID. It found no
  hits. Only the known `site` stands out (s_id 0.424, gap +0.149). No key over all columns but one or two counts
  (the best covers 3.8% of rows), 0% of rows sit in near-copy clusters, and the leak probe found no exact copies.
  `mountain_laurel_volume_2014_m3` shows a gap (+0.136) but s_id 0.014: it is a feature, not an entity.
- **Context and unit (SPLIT-23).** `context="all_rows"` matches a forester who inventories the whole stand before
  treating it. Adding the site means of the eight 2014 inventory columns changes the random forest's grouped R^2 by
  -0.016 (paired SE 0.010, positive on 53% of splits), so the declaration is harmless. `labels="per_sample"` and
  `prediction_unit="row"` are right: the microplot is the experimental unit and the GLMM's observation.
- **Temporal rules.** None applies. There is no time axis across rows, every label is the 2021 survey, and a model
  deployed later would train on a finished experiment. SPLIT-9 and SPLIT-10 (a gap) do not apply, and neither does
  SPLIT-7 or SPLIT-8: the setup is not a stream, and the use case is a new stand.
- **Learnability across groups (SPLIT-27, SPLIT-28).** In the group probe, ridge, random forest, LightGBM and kNN reach
  R^2 0.148, 0.336, 0.272 and 0.223 on unseen sites. On the count, as scored, the random forest beats the mean-count
  dummy on 56 of 60 shipped splits (RMSE 18.76 against 23.30). SPLIT-28 is not triggered.
- **Source protocol (SPLIT-5, SPLIT-19).** The source fits all 24 sites in a GLMM ranked by AIC and holds nothing out.
  The grouped split is stricter, and `splits_comment` says so correctly.

**Problems, ranked (principles.md: rank, then strength, then effect size)**

1. **P4, no rule broken (a SPLIT-1 balance note): the shipped folds often unbalance the forests.** The shipped
   grouped folds are not stratified. In 15 of 60 test folds one forest has at most 2 of the 8 sites, and one fold has
   none of one forest. That fold's training side then holds 12 sites of one forest and 4 of the other, while the
   deployed model would train on 12 and 12. The two forests differ in deer density (7.9-9.2 against 2.8-3.3 per
   km^2) and in outcome level: both high-count sites are in Rothrock.
   - Mildest remedy, optional: `stratify_on = "state_forest"`. The v2 code supports it: `_per_sample_splits` uses
     `StratifiedGroupKFold` on a binary category. Every fold then holds 3-5 sites of each forest.
   - Measured effect, for information only (the reason is the fold composition, not the score, in the spirit of
     SPLIT-21): random-forest R^2 (log) 0.222 becomes 0.303; RMSE on the log scale 1.096 becomes 1.056; the
     per-fold standard deviation of count RMSE 8.24 becomes 4.97; folds holding both high-count sites drop from 10 to
     2 of 60.
   - No dataset in the working copy sets `stratify_on` on a grouped regression yet, so this would be a first. The
     curator decides.
2. **P6 with the few-groups factor (MET-1/MET-10, and how to accept `groups_test_groups_few`): on the count scale,
   two sites decide the fold score.**
   - `site_110` and `site_120` (Rothrock, mean counts 69 and 74) hold 18 of the 22 microplots with more than 50
     seedlings.
   - On the count scale, the worst site holds on average 47% of a test fold's squared error (up to 76%). On the
     log1p scale it holds 23%, against a fair share of 12.5% (1 site in 8).
   - Random-forest count RMSE is 13.8 on the 30 folds holding neither site, 18.0 on the 20 holding one, and 35.3 on
     the 10 holding both. On the count, an 8-site test fold behaves like about two sites.
   - Ridge on log1p, scored on the count, reaches a mean RMSE of 906 against 23 for the dummy (beating it on half the
     splits), because expm1 blows up a few extrapolated predictions.
   - This does not make the split wrong. It is why the builder's issue 4 (metric tail) matters more with 24 groups.
   - Remedy: say it in the accepted warning text. The scale of the metric (log1p scale, or rmsle) is the metric
     reviewer's call. Remedy 1 also spreads the two sites.
3. **P4 wording of claims: the acceptance text for `groups_test_groups_few`, the record and the split text.**
   - The builder's draft says "the random forest beats the dummy on 28 of 30 splits". That number is on the log1p
     scale (task_probes, 93% of 30). On the count, the scale the metric scores, it is 30 of the first 30
     (the builder's decisive probe) and 56 of all 60 shipped splits. The `curation_comments` probe bullet ("better than the dummy on
     every one of 30 splits") is the count-scale figure. Name the scale in both places.
   - "Each site holding every treatment once" should read "every treatment combination once beside 2-4 controls".
   - The group-probe numbers (0.148, 0.336, 0.272, 0.223) and "85-88 microplots" check out.
   - Precedents: `airfoil_self_noise` (33 setups, 11 per fold) and `open_university_learning_analytics_dataset` (22
     presentations, 6-9 per fold) accepted the warning on the same evidence, and 8 sites per fold sits between them.
     `south_nation_riparian_birds_insect_emergence` differs in fact: one bird visit per site, so 24 scored units in
     all. It carries `Too Small` on its record, but the curator's stated reason was "No good target". The record's
     Assessment line, which reads it as confirmed `Too Small`, should say this.
   - The record's Assessment line "about 5 sites (55 rows) per test fold in 5 folds" is superseded by the protocol:
     3 folds of 8 sites, 85-88 rows each.
4. **P4/P3 scope of what the test stands for (USE-8; text only): the split tests new sites inside two forests and
   inside one cohort.**
   - `state_forest` is an input with two values, so the score covers new sites in Rothrock and Bald Eagle only.
     Leaving one forest out drops random-forest R^2 (log) to 0.110 (2 splits) against 0.270 grouped by site. The
     question's "a central Pennsylvania oak-hickory stand" is wider than that.
   - All 24 sites share the years 2014-2021: their weather, the deer densities of 2018-2019, and the unmaintained
     fences of 2020 (Sec. 2.2). No split of this data can measure a change of years.
   - This is not SPLIT-7 or SPLIT-8, since there are no stacked periods and the use case is a new stand.
   - Remedy: one clause in `splits_comment` or `fit_reason`, for example "new sites of the Rothrock and Bald Eagle
     state forests, all followed over the same 2014-2021 years".
5. **P3 note for the use-case reviewers (SPLIT-23, USE-8; not a split fix): the row score mostly measures the site's
   level, not the treatment choice.**
   - The forester's decision is a comparison of treatments within one stand. On grouped folds the random forest
     explains R^2 (log) 0.037 of the variation within a site, against 0.270 overall. The treatment flags add R^2
     0.018 (builder, paired SE 0.003).
   - So the benchmark mostly rewards predicting a new site's regeneration level from its inventory.
   - The row unit and the grouped split are still right. This belongs to the "approximate" fit and should be visible
     when the curator weighs the use case (builder's issue 1).

**Cannot verify.** A hidden grouping above the site, such as neighbouring sites in one stand, cannot be checked: the
file has no coordinates, and the 24 sites were drawn at random from 100 locations. The one site inside an earlier deer
exclosure (Sec. 2.2) cannot be identified in the file, so its void fence contrast falls into whichever test fold
holds it.

</details>

<details><summary>Domain practitioner</summary>

**Domain practitioner (2026-11-01): pennsylvania_oak_hickory_regeneration_experiment**

**Actor.** A DCNR Bureau of Forestry district forester (a state-forest silviculturist) in the Ridge and Valley, who has a SILVAH cruise of a mature oak stand in hand and must choose a deer fence, herbicide, lime, a combination or nothing to build advance oak and hickory regeneration before a shelterwood removal cut. The definition names no actor ("for example a state forester"). The funders come close to naming one: the study was paid for by the Pennsylvania Game Commission and the DCNR Bureau of Forestry, one author works at the Bureau, and the Penn State release says the work shows managers "which deer and forest management actions work best under different conditions". So USE-1 holds, and USE-2 / SEL-3 do not apply. The abstract's central result ("Outcomes depended on initial tree seedling abundance") is exactly the case where treatment effects depend on the inventory, which is what a model for choosing a treatment needs.

**Fit: approximate (agree with `fit="approximate"`, but the `fit_reason` names the wrong gaps).** One sentence: the randomised treatments, the 2014 inventory and the held-out sites mirror a regeneration prescription at the scale of a SILVAH regeneration plot, but the target counts every tree species rather than the desirable oak and hickory stocking I act on, and at one microplot per treatment per site the data cannot show which treatment is best for a stand.

**How I decide today (Brose et al. 2008, GTR NRS-33, the SILVAH-Oak manual).**
- A stand of 10 acres or more gets 20 or more regeneration plots of 6 ft radius (1/385 acre, 10.5 m2), each nested in a 26 ft interference plot. On these I tally oak in three size classes (new; established, 0.5-3 ft; competitive, over 3 ft) and the other desirables at 2 in or taller, with stems over 1 ft counted double. I estimate fern, low woody (laurel, huckleberry) and grass cover in 5% steps, rate the Deer Impact Index 1-5 and site quality, and run an overstory prism tally.
- A plot is "stocked" when its weighted count passes a threshold that rises with deer impact (Table 3.1). New oak needs 25, 25, 50, 100, 200 weighted stems per plot at impacts 1-5, and other desirables need 15, 30, 50, 100, 200. SILVAH reports the share of stocked plots at the ambient deer impact and "as if a woven-wire fence is erected" (impact 1).
- The decision charts then prescribe. For example, a final removal cut needs 70% of plots stocked with competitive desirables and 50% with competitive oak. Herbicide comes in when 30% or more of plots carry interference. Fence when deer impact is 4 or more. I reinventory after about 5 years.
- NRS-33 adds: "red maple would be considered desirable regeneration in northwestern Pennsylvania but as interference in parts of the Ridge and Valley region". This study sits in the Ridge and Valley, where its own methods say red maple is common in the understory and black birch is "oftentimes abundant".

**1. Inputs at the prediction point.**
- I have: the state forest; the treatment I choose; the 2014 seedling counts and aggregate heights (over 15 cm and at all heights); the 2014 mountain laurel volume. The 15 cm cut matches SILVAH's lower bound for established oak (0.5 ft). The 8.55 m2 microplot is almost the size of my 10.5 m2 regeneration plot.
- I would not normally have: soil pH, Al and Mn from a 40 cm soil pit analysed in the lab. They are not part of a SILVAH cruise, and they are missing on 72 of 261 microplots. If I were weighing lime I would order a soil test, so this is acceptable. pH is the paper's main moderator of the lime effect.
- I always have but the dataset lacks:
  - the Deer Impact Index per plot (here only the two-level `state_forest`, a coarse proxy: 7.9-9.2 against 2.8-3.3 deer/km2);
  - fern, huckleberry/blueberry and grass cover. The deposit README describes `PRE_TRT_ALL_COMP_VOL`, but the file does not have it; the methods say laurel volume correlates with all three taxa at R2 0.72, which softens this;
  - the 2014 overstory basal area and the oak seed source. The file has only the 2014-2021 average, rightly dropped under LEAK-10;
  - site quality;
  - the regeneration split by species group. This one matters most, see gap 1.
- The builder's leak handling is right from my side: PH16, canopy 2016, mean BA and post-herbicide laurel are all things I would not know in 2014 (USE-3).

**2. Target: a proxy.**
- I act on the share of plots stocked with desirable (oak, hickory, other desirable) regeneration at my deer impact, weighted by height. The target counts every arborescent woody stem over 15 cm, red maple and black birch included. The deposit holds only totals, so I cannot get the oak and hickory count from it. The methods say the crews "counted individuals of each species by height class", so the authors have it.
- A fence plot full of black birch scores high here and is a failure for me. This is a superset proxy, not another quantity (USE-5's diabetes_3 test): total stem abundance is the source's own response, and the Game Commission's regeneration assessment (PRS) also scores species groups weighted equally. So it supports approximate rather than a fail.
- I would want a number per plot (a count, from which I apply my own deer-dependent threshold), not a class. A class would fix one threshold, which differs by deer impact and species group.
- Shipping the 2021 level rather than the paper's 2014-2021 change is right (USE-5): I act on what will be on the plot, and with the 2014 count as an input the two carry the same information.

**3. Rows and test data.**
- One row is one plot outcome under one treatment. That is the unit my stand tally is built from, so per-row prediction is fine for measurement.
- But I apply one treatment to a whole stand. In the experiment every 8.6 m2 patch of a site gets a different treatment, and each patch starts from its own seedling count. My probe on the shipped splits shows what that does at held-out sites:
  - correlation between predicted and observed within-site contrasts (each treated microplot against the mean of its site's controls, log1p scale): 0.33 for the random forest with the treatment flags, 0.31 without them;
  - the observed best of the seven treated microplots is picked 30.8% of the time with the flags and 30.0% without (chance 14%).
- So the "best treatment" at a site is mostly whichever microplot started richest. Ranking treatments for a new stand is weakly identified. The model mostly forecasts persistence plus the site effect: the 2014 count alone gives R2 0.22, the flags add R2 0.018.
- The test sites are new stands in the same two forests and the same 2014-2021 cohort (one weather and mast history). That is what a forester of those two districts faces, and the grouped split by site is right (USE-10, a stand never followed). Transfer to other forests and later years is not tested.

**4. Would I use it?**
- Not to prescribe; SILVAH does that. I would use it as a second opinion on how much a fence or lime adds in a stand with few or many seedlings, which is the paper's interaction.
- I would trust it if, on held-out sites, its treatment contrasts reproduced the randomised contrasts and the paper's findings: fence best at low initial abundance; herbicide alone harmful (the change in log count is -0.37 under herbicide alone); lime useful where pH rises above 4.6.
- I would distrust it because:
  - it counts every species;
  - it rests on 24 sites in two forests and one cohort;
  - the fences are microplot exclosures (3.3 m plus a 0.75 m buffer), not stand-scale woven-wire fences;
  - the herbicide is a non-selective broadcast that killed the seedlings too, unlike a stand prescription aimed at fern and laurel;
  - lime is a research treatment, not a SILVAH prescription.

**Gaps, ranked by how much they change the task.**
1. **The target is not desirable or oak stocking (USE-5, USE-8).** It counts all tree species, including red maple and birch, which SILVAH treats as interference in this region. It cannot be fixed from the deposit; the authors hold the species tallies. This is the main reason the fit is approximate, and the `fit_reason` does not name it.
2. **The treatment decision is barely scored (USE-1, USE-8).** One microplot per treatment per site. The flags add R2 0.018 (0.013 RMSLE, 0.28 seedlings of count RMSE), and a model without the flags picks the observed best treatment as often as one with them. The task is mainly "how many stems will this plot hold", with the treatment as a small modifier.
3. **Treatment scale (USE-8).** Fences and herbicide were applied per 8.6 m2 plot rather than per stand, and the herbicide was non-selective. The measurement unit, however, is right: 8.55 m2 against SILVAH's 10.5 m2 plot. The `fit_reason`'s "an 8.6 m2 microplot stands in for a stand" names the wrong gap. The microplot is the plot a stand inventory is made of; the gap is that the treatment was applied per plot and that the stand decision aggregates plots into a share stocked.
4. **Inputs (USE-3, USE-6).** Missing: deer impact (only a two-level proxy), fern and other competitor cover, 2014 overstory, site quality. Present but not routine: lab soil chemistry. A moderate change; a SILVAH-based model would rest on other columns.
5. **Narrow sample.** 24 sites, two forests, one 7-year cohort. Already named in the `fit_reason`.
6. **Minor.** Lime is not a standard prescription. The herbicide followed the 2015 survey, which is not in the file. The fence alone is always microplot 5 (already noted).

**What an expert would change.**
- In the `fit_reason`: name gap 1 ("counts all tree species, red maple and birch included, where the forester acts on desirable oak-hickory stocking"). Replace "an 8.6 m2 microplot stands in for a stand" with "treatments applied per 8.6 m2 plot, not per stand". Soften "no actor is named": the funders state a management purpose.
- In `task_summary.predicted` and the target bullet: say "of any tree species; the deposit has no species split". The title says oak-hickory, and a reader will assume oak.
- Ask the authors (Diefenbach, Penn State and USGS) for the 2014 and 2021 counts by species group and height class. With those, a target of desirable or oak stems over 15 cm, or a SILVAH weighted count, would close gap 1 and could move the fit toward direct.
- Add the 2014 basal area if the authors hold it (they surveyed BA in 2014).
- Keep the grouped split by site and the 2021 level target.
- The record still carries `No Good Target / Scientific Discovery`. The stated management purpose and the abstract's inventory-dependent effects argue against that marker as an exclusion reason (USE-2). The curator decides.

**Metric: partly.**
- Declared: `rmse` on the count after the inverse of log1p (fallback; MET-3 handled correctly). It scores the plot-level count, the right quantity for a stocked-plot tally, at the right unit (MET-1). But I would not pick a model by it, for three reasons measured on the shipped splits (30 splits):
  - **Dominated by plots far above any stocking threshold.** The top 5% of test rows (69 or more stems) hold 56% of the squared error (builder's probe), while 76% of the microplots hold fewer than 15 stems. Under count RMSE, 0 against 3 stems costs 9 and 70 against 140 costs 4,900. Yet 0 against a few is the difference between a plot that regenerates and one that does not.
  - **Picks a model worse than doing nothing on the typical plot.** Count RMSE ranks the random forest fit on raw counts first (16.7 seedlings). Under RMSLE that model (1.178) loses to persistence, "2021 = 2014 count" (1.168), while the log-scale random forest is best (1.072). The ranks of seven models disagree: the raw-count forest is 1st by count RMSE and 4th by RMSLE; persistence is 4th and 3rd.
  - **Fragile.** One ridge model on the log scale extrapolates and, after the inverse, scores a mean count RMSE of 2,796. One back-transformed prediction decides the score.
- **The metric I would use: `rmsle` on the count with `target_transform="log1p"`, origin context (MET-11, MET-3, MET-1).**
  - SILVAH's stocking thresholds are a roughly geometric ladder (15-30-50-100-200 and 25-25-50-100-200 weighted stems per plot across deer impact levels). An error by a factor of two moves a plot one step on that ladder wherever it sits, so the error that matters to me is relative.
  - The source models the counts on a log link (glmmTMB GLMMs).
  - A stocked or not-stocked classification metric is out: the threshold depends on deer impact and species group, and MET-7 forbids inventing a single one. MET-6 and MET-8 point the same way: no threshold is fixed, so score the number.
  - RMSLE scores the treatment flags about as weakly as RMSE (relative gain 1.2% against 1.6%; positive on 93% against 100% of splits), so it is no worse on the decision lever.
- Neither metric scores the treatment contrast for a stand. A contrast metric would be custom (MET-13), and with one microplot per treatment per site it would be too noisy to ship. I would look at it only as a diagnostic.

**Sources.**
- Dryad deposit doi:10.5061/dryad.z8w9ghxnk: README, and methods Sec. 2.1-2.4 as reproduced on Dryad (copies in the run folder).
- Begley-Miller et al. 2024, Can. J. For. Res. 54:1367-1375, abstract via Crossref.
- Brose, McGuinness, Stout et al. 2008, *Prescribing regeneration treatments for mixed-oak forests in the Mid-Atlantic region*, USDA FS GTR NRS-33 (https://research.fs.usda.gov/treesearch/18561; PDF read: Ch. 2 inventory, Table 2.1, Table 3.1, Table 3.4, Ch. 5 prescriptions).
- Penn State news release (https://www.psu.edu/news/research/story/deer-seedlings-and-soil-ph-influence-local-forest-regeneration): the funders, the management aim, the findings.
- Pennsylvania Game Commission, "What is a healthy forest?" (https://www.pa.gov/agencies/pgc/wildlife/discover-pa-wildlife/white-tailed-deer/deer-healthy-forest.html): PRS species groups, deer-dependent adequacy, 70% / 50% grades.
- My probes, in the run folder: a metric probe (shipped splits, 30 splits; RMSE against RMSLE ranks, treatment contrast at held-out sites) and one of the target against thresholds.
- Builder probes: the decisive and group probes, in the run folder.

</details>

<details><summary>Blind review</summary>

**Verdict: include with changes.** This is a real randomized field experiment. Its features are honest pre-treatment measurements, and holding out whole sites matches how the model would be used. Before including it, trace three columns that are not in the documented source schema and make sure `site` is used only as the group key. Even then, it is a small task with a low ceiling, and it cannot separate methods well.

**What the task is**

The data come from the Penn State Deer-Forest Study (Begley-Miller et al. 2024, Can. J. For. Res. 54:1367-1375; Dryad doi:10.5061/dryad.z8w9ghxnk). The study has 24 randomly chosen sites in Rothrock and Bald Eagle State Forests. Each site has 11 microplots, 3.30 m in diameter. Plots 1-4 are controls. Microplot 5 is fenced. Microplots 6-11 each get one of the treatments H, L, FH, FL, LH or FLH. Fencing and lime went in during summer 2014 and herbicide in August 2015; the outcome was surveyed in 2021.

Each row is one microplot. The target is log1p of the 2021 count of tree seedlings taller than 6 in (15 cm). The features are:
- the 2014 baseline seedling counts and aggregate heights;
- 2014 soil pH, Al and Mn;
- 2014 mountain-laurel volume;
- the three treatment flags;
- the state forest.

As a prediction, the task reads: "given a pre-treatment regeneration inventory and a planned treatment (fence, lime, herbicide), how much advance regeneration will a patch have after 7 years?" State-forest and Game Commission managers do ask this when deciding where to fence or lime, so the use is real. The source itself, however, is a hypothesis-testing GLMM/AIC study, not a forecasting product (details under concern 3).

**What checks out**

- **The table matches the source design.**
  - There are 261 rows. The README says "262 rows" with a header row, so the counts agree.
  - There are 24 sites, 12 per forest. Site IDs start with 1 for Rothrock and 2 for Bald Eagle, which matches the README's UID code (1 = Rothrock, 2 = Bald Eagle).
  - Every site has exactly one microplot in each of the 7 treatment arms, plus up to 4 controls. That gives 96 Yes for each flag and 93 controls. Three control microplots are missing: one at site_137 and two at site_149.
- **No leakage that I could find.**
  - Every post-baseline column in the source is excluded: COUNT21, AGGHT21, the delta.* columns, CANOPY (2016), BA (mean 2014-2021) and POST_TRT_KALA_VOL.
  - soil_ph_2014 was measured before liming. Its mean is 2.97-3.18 in the limed arms and 2.93-3.08 in the unlimed arms. The highest 2014 pH is 4.44, while the abstract says lime raised pH above 4.6 by 2016.
  - All features are known at the 2014/2015 inventory, before the outcome.
- **No copies.** There are 0 exact duplicate rows, and 0 duplicates even after dropping target and site.
- **The split fits the use.** Holding out whole sites is right: all plots in a site lie within "a 110m by 52m perimeter" (source methods), and site accounts for 52% of the target variance. Holding out a whole state forest would leave only 2 groups, which is too few.
- **Values look plausible.**
  - expm1(target) gives exact integers from 0 to 154, with 18.4% zeros.
  - Aggregate height per seedling over 6 in ranges from 0.2 to 1.8 m. This matches the height-class midpoints the paper uses (0.225 m for class 2 up to 1.8 m for the top class).
  - Soil Al falls as pH rises (Spearman -0.44), as expected in acidic soils.

**Concerns, most serious first**

1. **Small, with a low ceiling and weak power to separate methods.**
   - Evidence:
     - There are 261 rows from 24 sites. Each 3-fold test fold holds about 87 rows from 8 sites.
     - Over 20x3 site-grouped splits, R2 was:
       - mean predictor: -0.12
       - OLS on log1p(seedlings_over_6in_2014) alone: 0.27
       - OLS on that plus the 3 treatment flags: 0.29-0.31
       - random forest on all features: 0.26
       - LightGBM: 0.21-0.24
       - HistGB: 0.20
       - ridge on all features: 0.16
     - Per-split R2 has a standard deviation of 0.18-0.27.
     - Paired over the same splits, RF minus 4-feature OLS averages -0.056 (sd 0.088). RF wins only 32% of splits and small LightGBM only 20%.
     - Most of the signal is persistence of the baseline count (Spearman 0.60 with the target).
     - Half the variance lies between sites (52%), and the features explain little of it.
   - Change: none to the data. Include it only if the benchmark wants a tiny, noisy, grouped regime where strong priors win. If the benchmark has a minimum size (TabArena's published criteria use a 500-row floor), this falls below it and should be excluded.

2. **Three columns cannot be traced to the cited source.**
   - Evidence:
     - The columns are `soil_al_2014`, `seedlings_all_heights_2014` and `aggregate_height_all_heights_2014_m`.
     - The Dryad README lists 22 variables: STUDY_AREA, UID, PLOT, SUBPLOT, TRT, FENCE, LIME, HERB, delta.COUNT_6, AGGHT14, AGGHT21, delta.AGGHT, COUNT14, COUNT21, delta.COUNT, PH14, MN, CANOPY, BA, PRE_TRT_KALA_VOL, PRE_TRT_ALL_COMP_VOL and POST_TRT_KALA_VOL.
     - None of these is aluminium or a 2014 count of seedlings of all heights. The only under-6-in variable is delta.COUNT_6, a 2014-2021 change.
     - The README also contradicts itself: it calls the data "a single Excel file" with "21 columns", but describes 22 and the listed file is DataCJFR.csv.
     - I could not download the CSV. The Dryad API returned `{"error":"Unauthorized, must have current bearer token"}`, and I did not try to get around that.
     - The internal evidence says these are genuine 2014 values, not 2021 information leaking in:
       - all-heights ≥ over-6-in in 100% of rows;
       - (agg_all - agg_over6) / (count_all - count_over6) has a median of 0.076 m. That matches the 0.075 m midpoint of the <0.15 m class, i.e. the paper's aggregate-height formula;
       - the 2014 under-6-in count correlates only 0.085 with what the baseline and treatments leave unexplained, and adding it to OLS lowers grouped R2 from 0.305 to 0.278. A leak would have the opposite signature.
   - Change: check that these columns exist in DataCJFR.csv, or document the second source they came from. If they cannot be traced, drop them. Little is lost: their combined RF importance is about 0.19, and the best model does not use them.

3. **The framing weakly matches the decision.**
   - Evidence:
     - The decision-relevant signal is the treatment effect, but the treatment flags add little. In OLS, adding them lifts R2 from 0.274 to 0.293. RF importances are fence 0.024, herbicide 0.015 and lime 0.008.
     - The unit is an 8.6 m² microplot, smaller than anything a manager would act on.
     - Fences were not maintained in 2020 (source: "We maintained fences yearly ... except in 2020"), which adds noise to the fenced arms.
   - Change: none required. Describe the task as predicting 7-year regeneration from a baseline inventory at new sites, not as estimating treatment effects.

4. **`site` sits in the table as a 24-level categorical.**
   - Evidence: under grouped splits, every test site is an unseen level.
   - Change: use `site` only as the group id and keep it out of the features. `state_forest` is a site-level covariate (2 levels, 12 sites each) and is fine to keep.

5. **Soil values are missing by design.**
   - Evidence:
     - pH, Al and Mn are NaN in 72 of 261 rows (27.6%). Seventy of these are control microplots.
     - This matches the source: soil was sampled "at microplots 1, 5, 6, 7, 8, 9, 10, and 11 ... and at microplots 2–4 when time allowed". site_123 has no soil data for any of its 4 controls.
     - The missingness tracks treatment arm, which is already a feature, so it does not leak the target.
   - Change: keep the NaNs as they are. Do not impute them in the prepared table.

6. **Mn units look wrong in the source documentation.**
   - Evidence: the README gives MN as "KCl Extractable Mn (cmol(+)/kg)", but the values run from 1.69 to 206.2. KCl-extractable Mn in acidic forest soils is normally well below 2 cmol(+)/kg, so these look like mg/kg.
   - Change: the column name carries no unit, so models are unaffected. Do not state cmol(+)/kg in any metadata.

7. **Minor preparation choices.**
   - PRE_TRT_ALL_COMP_VOL is a legitimate pre-treatment feature that was left out. The source says it has R2 = 0.72 with mountain-laurel volume, so adding it would change little.
   - Using log1p of a count as the regression target is reasonable. Modelling the 2021 level with the baseline as a feature carries the same information as the paper's change score.
   - The two raw 2014 counts and their aggregate heights are strongly collinear. This is harmless.

**What I could not check**

- Row-level values against DataCJFR.csv, the mapping from source to prepared columns, and the origin of the three columns in concern 2. Dryad requires a bearer token to download files.
- The paper's full text and supplements. The publisher page returned 403.
- Whether the benchmark harness drops `site` from the features.
- Which survey (2014 or 2015) the mountain-laurel "pre-treatment" volume comes from. The README labels it 2014, which would be before both lime and herbicide either way.

**Sources**

- Dryad dataset page and API metadata: https://datadryad.org/dataset/doi:10.5061/dryad.z8w9ghxnk
- Paper: https://doi.org/10.1139/cjfr-2024-0034 (publisher page returned 403; the abstract and methods were read from the Dryad metadata)
- Penn State news summary: https://www.psu.edu/news/research/story/deer-seedlings-and-soil-ph-influence-local-forest-regeneration

My analysis scripts (site-grouped cross-validation and paired comparisons) stay with the run, outside the repository.

</details>

<details><summary>Precedent check</summary>

**Precedent check (precedent-checker, 2026-11-01).** Verdict: the definition is consistent with its precedents on every
choice. The data confirms the one departure, keeping a designed experiment as `Yes`, and the records state its reason.
Three things for the curator. First, one pair of like cases decided differently: metro_manila_village_weekly_dengue
went to 2nd Tier because its Dryad file seemed to need a manual download, and that fact is now refuted. Second, one
metric question is open on two siblings and should be decided once for all three. Third, two of the builder's draft
issues cite the wrong precedent or rule. Paths are relative to the repository root.

Read: the run's decision register (1,620 decisions). None
of its 14 flags touches this dataset's rules (TP-10, CLEAN-19, SPLIT-9/10/14, PROV-13, scaling over all rows,
`trivial`, `few_minority`, `one_feature`). Also read: the sibling records of the zero-inflated batch, the definitions of
this run, the Cases tables and the policy calls of 2026-10-30 (`curation/inputs/two_regime_zero_triage_summary.md`).

**1. Source and access: the Dryad version download, under the rule of 2026-11-01. Consistent; one pair to raise.**
- The rule "If you cannot find a source, it's 2nd tier" (Andrej, 2026-11-01) has been applied twice:
  - `sweden_depth_to_bedrock` went to 2nd Tier: its features need a manual order and a heavy rebuild (CC 2026-11-01).
  - `cape_floristic_region_family_cover/REVIEW.md` D4 read the rule as treating a source reachable only by hand as
    not found. It does not demote a source that is found.
- Here the source is the origin itself (PROV-8): Dryad version 318677, fetched by script with no token. Its SHA-256
  equals Dryad's digest. So the rule is not triggered. The evidence standard matches the run's other Dryad datasets,
  which take Dryad's own Zenodo mirror and check it against Dryad's digests: `boreal_postfire_lichen_biomass` and
  `nantucket_sound_sea_duck_aerial_survey_counts`. This deposit has no Zenodo mirror.
- The pair: `metro_manila_village_weekly_dengue` (CC 2026-10-30) was moved to `TBD -> 2nd Tier` with "Put the manila
  dataset to a 2nd tier if we need to manually download it". Its Assessment says Dryad's routes need a login.
  - I measured it today, 2026-11-01. The version download of that deposit (version 411989) redirects with no token
    (HTTP 302). It then serves the zip: HTTP 200, `application/zip`, 31,293,624 bytes, which is the 31.3 MB CSV plus
    its README. The headers are in the run folder; the file was deleted.
  - So the fact behind Manila's demotion no longer holds. Access-wise the two cases are now alike and decided
    differently (prompt below).
  - Among the batch's other Dryad-only records, no verdict rests on access. Finland, Svalbard, the Great Lakes marsh
    birds and Morocco are 2nd Tier on use-case grounds.
- Tension in the rules (not this dataset's problem, since its data is in hand). EV-4 (Must; Lennart, 2026-09-23) says
  a request-only download is "never the reason for a `No`, a `TBD -> 2nd Tier` or a marker".
  - The staged `Available on Request` row in `selection.md` says the same: Andrej, 2026-10-30, "Data on request shall
    be a TBD", so access alone decides no verdict.
  - The Manila CC and cape's reading of the 2026-11-01 rule go the other way.
  - The 2026-11-01 rule is so far written only in CC lines, not in a rules file.

**2. Scope and use case: a designed experiment kept as `Yes`, treatments as inputs, the marker kept. Departs from the
experiment rejects, with a stated reason that the data confirms.**
- The experiment rejects rest on "inputs that are only the design" (policy call 1, Andrej, 2026-10-30). The records:
  - `western_bluebird_nest_box_prospecting`, `clarkia_greenhouse_reciprocal_transplant_fitness`,
    `treeline_seedling_emergence_experiment`, `vernal_pool_restoration_plant_cover` and
    `yellowstone_lake_benthic_invertebrates_carcass_experiment`: all `No` (CC 2026-10-30).
  - `mice_protein_trisomy_discriminant`, retired 2026-10-01 (Lennart): its classes are the design.
- What sets this case apart is written down. The screening and western_bluebird's consistency point name it: a
  pre-treatment inventory of the kind SILVAH prescribes from, beside the assigned treatments. The curator set `Yes`
  after that text (CC 2026-10-30, "LGTM").
- The data now confirms it. The inventory carries most of the signal: the 2014 count alone gives R^2 0.22, against
  0.27-0.29 for the full model. The treatment flags add R^2 0.018 (paired SE 0.003; the builder's decisive probe). The inputs
  are not only the design.
- Consistent with:
  - `rand_health_insurance_experiment_doctor_visits` (`Yes`, CC 2026-10-30): the randomised plan is an input, with the
    marker kept. Difference: RAND's use case is named by a source (Newhouse 1989); this one is ours.
  - `boreal_postfire_lichen_biomass` and `crms_phragmites_cover` (`Yes` with `No Good Target / Scientific Discovery`
    kept, CC 2026-10-30). `selection.md` allows this: "`Yes` with a concern marker is not a contradiction".
- `qtp_urban_wasteland_plant_diversity` (`No`, CC 2026-10-30; 38 wastelands, 585 plots) is larger. Its record names no
  decision, while this one has the treatment choice. That fact is stated, so it is no pair.
- What remains is the weighing (builder issue 1): the decision variable's own signal is small. That is a call on
  USE-1/USE-8 for the curator, not a consistency gap.

**3. Size and split: 24 sites, grouped by site, `groups_test_groups_few` proposed for acceptance, context
`all_rows`. Consistent.**
- Accepted precedents for the warning, each with `group_probes.py` evidence:
  - `airfoil_self_noise`: 33 setups, 11 per test fold (2026-10-20).
  - `open_university_learning_analytics_dataset`: 22 presentations, 6-9 per fold (2026-10-20).
  - This dataset has 24 sites and 8 per fold, with RF R^2 0.336 on unseen sites. The proposed text follows their
    template.
- The curator's 2026-10-30 `No`s with `Too Small` differ on the facts TP-5 counts:
  - `plains_wanderer_spotlight_counts`: 16 sites, 41 surveys with birds.
  - `ghana_schoolchildren_schistosoma_egg_counts`: 12 communities, 80 positives.
  - Here: 85-88 scored microplots per fold, a count target with spread, 213 non-zero rows.
- Correction to builder issue 3. `south_nation_riparian_birds_insect_emergence` is no TP-5 precedent for the curator:
  his recorded reason for that `No` is "No good target" (CC 2026-10-30), not size. Cite airfoil and OULAD instead.
- Context `all_rows` matches the definition rule: all inputs of a held-out group are known when predicting. Siblings:
  force_2020, basque_offshore_ctd_chlorophyll, OULAD.
  - It differs from `boreal_postfire_lichen_biomass` and `cape_floristic_region_family_cover` (`none`) on a stated
    fact. There the use case is an unsurveyed place; here it is an inventoried stand.
- The record's Assessment of 2026-10-30 gave "about 5 sites (55 rows) per test fold in 5 folds", and the curator
  accepted 24 sites on those numbers. The shipped splits have 3 folds with 8 test sites each. That is a later measured
  fact (stage precedence), not a departure. The record's numbers need updating.

**4. Target: the 2021 count over 6 in, log1p, not the paper's 2014-2021 change. Consistent.**
- No earlier decision sets level against change. The screening the curator accepted (CC 2026-10-30) asked for exactly
  this: "target `COUNT21` or `AGGHT21` with the 2014 values as features, not the paper's change score (USE-5)".
- The count over aggregate height is within that either-or.
- Logging a skewed count (CLEAN-16, case by case) and scoring on the count (MET-3; Lennart, 2026-10-21, "ship the
  target on the modelling scale, score on the original scale") match `nantucket_sound_sea_duck_aerial_survey_counts`
  and `wadden_sea_sibes_macoma_abundance`.
- `blogfeedback` ships a raw count. That is a difference between other datasets, not a departure here.

**5. Metric: fallback `rmse` on the count, `target_transform="log1p"`. Consistent; one call to make once for three
datasets.**
- The fallback for a source that ranks by an in-sample criterion (AIC here) follows:
  - MET-5/MET-8 and the Tensions row ("otherwise the fallback").
  - `nantucket_sound_sea_duck_aerial_survey_counts` (in-sample pseudo R2, fallback `rmse` on the count, log1p).
  - `boreal_postfire_lichen_biomass` (significance tests, fallback).
- The alternative in builder issue 4 is `rmsle` from context. Its precedent is `blood_tests_drink_prediction`: a
  skewed count whose error matters relative to the amount.
- The same question is open in `datasets/_dev/tabarena-v0pt2/wadden_sea_sibes_macoma_abundance/REVIEW.md`, issue 5.
  There the domain practitioner proposed Poisson deviance and argued against `rmsle`, because it ranks the model that
  understates the means first.
- The same pattern shows here. An RF fit on raw counts beats the log-fit RF on count RMSE (16.7 against 17.7), and the
  top 5% of test rows hold 56% of the squared error (the builder's decisive probe).
- If the three are decided apart, it becomes drift. Decide pennsylvania, wadden and nantucket together.
- For all of them, TabArena's adapter scores `rmse` on the shipped scale for now (`definitions.md`, "What the benchmark
  harness does").

**6. Columns kept and dropped. Consistent.**
- Post-treatment values dropped (LEAK-10, USE-3), including averages over a window that ends at the outcome
  (`AVG_BA_m2_ha`, `AVG_POST_TRT_KALA_VOL_M3_1621`). These are the screening's risk (2), accepted.
- `PH16` dropped and `PH14`/`AL`/`MN` kept after a balance test of limed against unlimed plots (EV-1, the decisive
  experiment).
- Missing soil values kept: USE-7, "Missing values of the other inputs stay missing".
- `SUBPLOT`: CLEAN-3 keeps a meaningful identifier "processed into that meaning". Its treatment meaning is in the three
  flags, so dropping it complies.
- `TRT` dropped as an exact copy (CLEAN-5). `UID` dropped (CLEAN-3).
- The flags are categorical: CLEAN-14 as amended 2026-10-21 (Lennart), every 0/1 flag is categorical.
- `state_forest` kept: known for any stand (USE-6).
- `AL` kept with its unit unknown, as cannot-verify (EV-7). Same handling: `maps_router_eta` `track_length`
  (2026-10-21).

**7. Zeros: remove the `Two-Regime Zeros` tag (builder issue 6). Consistent.**
- The curator's rule (policy call 4, 2026-10-30): "If the low value is by far the most frequent one and independent of
  the remaining target distribution, then we can treat it as two regime zero, otherwise not."
- This dataset fails both parts. Re-measured on the raw file: 48 zeros against 38 ones, and zero in 38.7% of the plots
  empty in 2014 against 12.1% of the others.
- Same call as the removals on `how_much_did_it_rain_ii` (the mode is the first step of a graded count) and
  `basque_offshore_ctd_chlorophyll`. The rule itself asked for count targets to be checked at /add-dataset.

**8. Fit approximate, an example use case, the paper not read. Consistent.**
- `crms_phragmites_cover` and `cape_floristic_region_family_cover` also have a plot standing for a site and no named
  actor, with fit approximate (USE-8).
- `boreal_postfire_lichen_biomass` shipped with "the paper could not be read" (Wiley 403). PROV-17 allows going on
  when the text says so, and here it does. The way out it names still stands: ask the curator for the PDF.

**9. Rule citations in the builder's draft issues.**
- Issue 3: cite airfoil and OULAD, not south_nation (see 3).
- Issue 5 cites PROV-15. That rule covers errors of third-party copies (OpenML, Kaggle). Here the mismatch is between
  the origin deposit's README and its own file. The rules that fit are EV-2 (a measurement on the source's file
  outranks its codebook) and PROV-2 (Should: a source unclear in a detail stays, with a note of what to clarify, such
  as a question to the authors).
- Issues 2 and 6 follow the accepted screening and the tag rule. Issues 1 and 4 are weighing or family calls (see 2
  and 5).

**Drift and amendments.**
- Andrej's access calls take four positions within three days:
  - 2026-10-30, `chesapeake_bay_bird_banding_zi_isdm`: "Data needs request" leads to 2nd Tier.
  - The same day, chesapeake, `heritage_health_prize` and `shaoxing_hourly_precipitation_fusion`: "Data on request
    shall be a TBD" leads to `TBD -> Yes`.
  - The same day, Manila: a manual download leads to 2nd Tier.
  - 2026-11-01: "If you cannot find a source, it's 2nd tier".
- The CC lines do not show the order within 2026-10-30, so this is a tension between same-day calls rather than drift
  over time. It bears on Manila and Sweden, not on this dataset.
- No rule reaches a third exception of one kind through this dataset.

**Consistency check (AI, 2026-11-01):** the access call on pennsylvania_oak_hickory_regeneration_experiment (a
Dryad-only deposit fetched by script through Dryad's version download, kept `Yes`) differs from
metro_manila_village_weekly_dengue (`TBD -> 2nd Tier`, 2026-10-30, "Put the manila dataset to a 2nd tier if we need to
manually download it"). The access situation is the same: a Dryad-only deposit whose file API answers 401. Measured
today, Manila's version download also works without a token (HTTP 200, a 31.3 MB zip). What sets Manila apart?
(a) Its 2nd Tier also rests on the untested TP-10 leg, not only on the download, recorded as the reason; (b) treat
Pennsylvania like Manila (not supported by the rule, since its source was found and fetched); (c) reopen Manila: back
to `TBD -> Yes` under your CC "Test the leg, then decide", and run the scripted TP-10 test on the downloaded file;
(d) change the rule: write the access rule into the rules as an amendment of EV-4, naming which access gaps make a
2nd Tier (no source found; a manual order with a heavy rebuild, as Sweden) and which do not (a manual or scripted
download, a request, as `Available on Request`).

</details>

<details><summary>Advocate</summary>

**Advocate, opening brief (2026-11-01): pennsylvania_oak_hickory_regeneration_experiment**

**Position: ship.** The substance stays as defined: the rows, the target, the 12 inputs and the grouped split. No
evidence agent found a validity failure. What they found are gaps in the text (`fit_reason`, the anomaly note, units,
record fields) and one metric weighing call. Each has a fix that keeps the dataset, all of them below "exclude" on the
remedy ladder.

```text
Verdict: ship after text changes.
Validity: SEL-3/USE-2 hold (a treatment decision fits); USE-1 holds (a DCNR forester, our example; the funders state
  the aim); USE-5 holds with a named breadth gap (all species), fit approximate; LEAK-10 triggered, fixed (11
  post-treatment columns dropped); SPLIT-1/3/24 hold, SPLIT-26 holds (grouped by the source's own site).
Value: TP-5 not triggered (85-88 scored microplots, 8 sites per fold); TP-2, a small real signal; SPLIT-27 passed.
Metric: MET-3 holds; fallback rmse legal under MET-11; rmsle from context is a curator call, made together with
  nantucket and wadden.
Quality: PROV-2 notes (undescribed columns, Mn unit, laurel index).
Weighed: size -, decision signal -, source + (CC0, randomised, checksum-pinned), gap + (small grouped regression).
```

**1. Honest evaluation holds, checked by four agents independently (P4; LEAK-10, SPLIT-1, SPLIT-3, SPLIT-24 Must;
SPLIT-26 Should).**
- Evidence: all 11 post-treatment columns are dropped. Randomisation makes the timing test decisive (EV-1). With site
  fixed effects, lime moves `PH16` by +1.18 pH (CI 1.01 to 1.35) but `PH14` by only +0.05 (CI -0.02 to +0.12). The
  2014 counts, heights and laurel volume show no treatment effect (on the count: lime p 0.31, herbicide 0.93, fence
  0.55).
- No duplicate rows, no exact feature copy across folds, and no hidden group besides `site`.
- The group is the source's own `PLOT`, which is the random intercept of its GLMM. An IID split would overrate the
  score by 0.14-0.16 R^2, so the grouped split is required (SPLIT-29, Must). Every test fold holds 8 whole sites, and
  all 8 treatment cells are in every training side.
- This answers the blind reviewer's concern 2, that three columns "cannot be traced". The blind reviewer could not
  download the file. The claim and column auditors did (SHA-256 equal to Dryad's digest), and an identity holds in
  every row: aggregate height at all heights minus aggregate height over 6 in equals 0.0762 m (the midpoint of the
  0-6 in class) times the extra stems. A measurement on the source's file outranks its codebook (EV-2, Must). So the
  columns stay; the blind reviewer's fallback was to drop them only if they could not be traced, and they can.
- Concern 4 (`site` as a feature) is settled as well: `n_features` is 12, and the harness drops the group column
  (definitions.md).

**2. A decision fits, and the data confirms what sets this experiment apart from the rejected ones (P2, P3; SEL-3,
USE-1, USE-2 Must).**
- Evidence: the curator set `Yes` (CC 2026-10-30) on the stated fact that a pre-treatment inventory sits beside the
  assigned treatments. The data bears that out. The 2014 count alone gives R^2 0.22 of the full model's 0.27-0.29, so
  the inputs are more than the design, which was the reason for the experiment rejects (policy call 1).
- The practitioner names the actor: a DCNR district forester with a SILVAH cruise in hand. The source comes close to
  naming one. The Game Commission and DCNR's Bureau of Forestry funded the study, one author works at the Bureau, and
  the Penn State release says the work shows "which deer and forest management actions work best under different
  conditions". The abstract's central finding, "Outcomes depended on initial tree seedling abundance", is an
  inventory-dependent effect, which is what a treatment model needs.
- Precedents: `rand_health_insurance_experiment_doctor_visits` (`Yes`, with the randomised plan as an input), and
  `boreal_postfire_lichen_biomass` and `crms_phragmites_cover` (`Yes`, with `No Good Target / Scientific Discovery`
  kept). selection.md: "`Yes` with a concern marker is not a contradiction".
- Why this outranks the marker: USE-2 excludes only a task that "no decision fits", and a decision fits here. Whether
  the marker stays as a concern or goes is a record field, not a verdict.

**3. The treatment signal is small but real. That is a gap in the fit, not a reason to exclude (TP-2 Should; USE-8
Must).**
- Evidence: the flags add R^2 0.018 (paired SE 0.003, positive on 90-93% of splits). On count RMSE they gain 0.31
  seedlings (SE 0.04, positive on 97% of splits). That is about six standard errors.
- Conceded: the split auditor (R^2 0.037 within a site) and the practitioner (the observed best treatment is picked
  30.8% of the time with the flags, 30.0% without) show that the row score mostly rewards predicting a new site's
  level. With one microplot per treatment per site, ranking treatments for one stand is weakly identified.
- What follows: TP-2 says a small real signal is no reason to retire (forest_fires, R^2 0.013). The gap belongs in
  `fit_reason`, and the fit is already approximate (USE-8). Mildest fix: state in `question` and `fit_reason` that
  the task predicts a plot's regeneration 7 years on from its inventory and planned treatment, with the treatment as
  a small modifier. This is the blind reviewer's own wording for concern 3, where it marks "Change: none required".
  This gap is independent of validity, so it does not stack with any Must.

**4. The target is the source's own count, at the level the forester acts on. Its all-species breadth is a gap to
name (P3; USE-5, USE-8 Must).**
- Evidence: the 2021 count over 15 cm, with the 2014 count as an input, carries the same information as the paper's
  change score: on the count scale, an error on the level is the same error on the change. The curator's accepted
  screening asked for exactly this target. The 15 cm cut is SILVAH's lower bound for established oak, and the 8.55 m2
  microplot is close to SILVAH's 10.5 m2 regeneration plot (practitioner).
- Conceded: the count sums every arborescent woody species (Sec. 2.3), red maple and black birch included. Neither
  `predicted` nor `fit_reason` says so (claim audit row 41, practitioner gap 1).
- Why it does not fail USE-5: the rule fails a label "checked and found to be another quantity" (diabetes_3). This
  label is the source's own response, and it contains the actor's quantity. The Game Commission's regeneration
  assessment also counts species groups. USE-5 allows shipping with fit approximate and a note that names the gap.
- Fix: one clause in `predicted` and in `fit_reason`. Optionally, ask the authors for the species tallies: a better
  version the source defines would replace ours (TP-6).

**5. 24 sites make a tiny-data task, not a `Too Small` one (P6; TP-5 Must, SPLIT-27 Should, SPLIT-28 Must).**
- Evidence: each test fold scores 85-88 microplots (8 sites, 8-26 zeros), and 213 rows are non-zero.
- On unseen sites, ridge, random forest, LightGBM and kNN reach R^2 0.148, 0.336, 0.272 and 0.223.
- The random forest scores 0.354 against a maximum of 0.006 over 20 target shuffles, and it beats the mean-count dummy
  on 56 of the 60 shipped splits. SPLIT-28 is not triggered.
- Precedents for accepting `groups_test_groups_few`: `airfoil_self_noise` (33 setups, 11 per fold) and
  `open_university_learning_analytics_dataset` (22 presentations, 6-9 per fold). `south_nation_riparian_birds_insect_
  emergence` is no precedent: it has one row per site, and the curator's reason was "No good target".
- This answers the blind reviewer's concern 1 (a 500-row floor, and a random forest losing to a 4-feature OLS). Our
  rules set no row floor. TP-5 counts units per test fold, and the "Tiny but real" tension row keeps musk. Methods that
  tie, or a simple model that wins, is `no_spread`, which TP-2 keeps (heart_disease_cleveland,
  acquire_valued_shoppers_challenge). A row floor would be an amendment for every dataset, not a call on this one.
- Fix: accept the warning with the builder's text, naming the scale (28 of 30 on log1p, 56 of 60 on the count) and
  the site concentration (split auditor).

**6. The metric is legal as declared. RMSLE is a one-line weighing call for the whole family; it changes no verdict
and, today, no score (P6; MET-3, MET-11 Must; MET-10 Weigh).**
- Evidence: MET-3 holds; the scorer equals count RMSE after expm1 on 60 of 60 folds. The source ranks GLMMs by AIC
  and reports no prediction error, so the fallback is MET-11's default. The "context" origin needs a clear context,
  and wadden's practitioner argued against rmsle on a sibling count. `nantucket_sound_sea_duck_aerial_survey_counts`
  in this batch ships the same fallback.
- Conceded: on the count scale:
  - one test site holds a median 50% of the squared error;
  - a ridge fit on log1p blows up after expm1;
  - the two scales rank models at Kendall tau 0.21;
  - the practitioner's SILVAH thresholds form a geometric ladder, which argues for relative error.
- What follows: the fix is either a metric declaration (`Metric.from_context("rmsle", target_transform="log1p")`) or
  `rmse` with the tail numbers written into the notes. Both keep the dataset (remedy ladder, step 2 or 3). Decide
  nantucket, wadden and this one together so the three do not drift apart.
- TabArena's adapter does not read `objective_metric` and scores `rmse` on the shipped log1p scale (definitions.md).
  The benchmark score today is therefore already the log-scale error.
- Optional: `stratify_on="state_forest"` cuts the fold-to-fold SD of count RMSE from 8.24 to 4.97 (split auditor). No
  rule asks for it.

**7. The rest is documentation, fixed in the text (P5, P7; PROV-2 Should, EV-2 Must, USE-8 Must).**
- The source is the origin: a CC0 Dryad deposit of a randomised experiment, fetched by script and pinned by checksum.
  It is not a 2nd Tier access case (precedent checker).
- Fixes; none changes a model input:
  - the anomaly bullet: 7 columns are undescribed, not 2, and the README's 262 rows count the header;
  - `MN` is stated in cmol(+)/kg, which is implausible; mg/kg is likely;
  - the laurel "m3" is a cover x height index;
  - `fit_reason` should name four gaps: no pre-treatment overstory measure, treatments applied per plot and not per
    stand, two forests, and one 2014-2021 cohort;
  - the probe bullet should name its dummy;
  - cite PROV-2, not PROV-15.
- Record fixes:
  - drop `Two-Regime Zeros`: a negative binomial expects 48.2 zeros, and 48 are observed;
  - change "Domoto M.E." to "Emily J.";
  - supersede the Assessment's 5 folds of 55 rows.
- PROV-2 keeps a plausible source that is unclear in a detail, with a note. A quality gap with a cheap fix is fixed
  and the dataset kept (principles, step 3).

</details>

<details><summary>Critic</summary>

**Critic: opening brief (2026-11-01), pennsylvania_oak_hickory_regeneration_experiment**

**Verdict: ship after changes.** None of my points calls for exclusion. The data matches its Dryad digest, and the
leak handling and the split by site hold (claim-auditor rows 5, 12, 13, 40; column-auditor; split-auditor). But the
definition describes a task that the data scores only in part. The target counts every species. The treatment choice
barely moves the score. One or two dense sites per fold decide the declared metric. Points 1, 2 and 5 need changes to
the definition before it ships; the rest are text.

**1. The target counts every tree species, and the definition does not say so (P3; USE-5 Must, USE-8 Must).**
- Problem: the name, the question and the use case all point to oak-hickory regeneration. The target sums "any live,
  arborescent, woody species that was ≤2.54 cm diameter at breast height" (Sec. 2.3). At these sites "Red maple
  (Acer rubrum) was common in the understory and black birch ... was oftentimes an abundant species" (Sec. 2.1). I
  re-read both quotes in the Dryad methods text. In the Ridge and Valley, SILVAH treats red maple as interference
  (NRS-33, quoted by the domain practitioner).
- Effect on the task: a fenced plot full of black birch scores as a success, while the forester counts it as a
  failure. A model is chosen for total stem abundance, not for the desirable stocking the forester acts on.
- Evidence: claim-auditor row 41 (open); domain-practitioner gap 1. The deposit has no species split, so the share of
  competitors cannot be measured. The authors have it: the crews "counted individuals of each species by height
  class" (Sec. 2.3).
- Why I do not ask for a fail under USE-5: total abundance is the source's own response, the Game Commission's
  assessment also counts across species groups, and the share of competitors is unmeasured. That makes it a superset
  proxy, which is a known gap, and USE-8 requires a known gap to be named. Neither `predicted` nor `fit_reason`
  names it.
- Remedy (fix the definition): add "of any tree species, red maple and birch included; the deposit has no species
  split" to `predicted` and to the target bullet, and name this gap first in `fit_reason`. Optional repair from the
  origin: ask the authors for counts by species group. With them, a target of desirable stems could move the fit
  toward direct.

**2. The use case is a treatment comparison that the benchmark barely scores, and `fit_reason` names the wrong gaps
(P3; USE-1 Must, USE-8 Must).**
- Problem: `use_case` says the forester "compares the outcome expected under each combination", and `fit_reason` says
  the data is "the data a treatment-choice model needs". On the shipped splits, the treatment choice is close to
  invisible in the score.
- Evidence:
  - the flags add R^2 0.018 (paired SE 0.003), against 0.22 for the 2014 count alone (builder; claim-auditor row 23);
  - within a site, the random forest explains R^2 0.037 of the variation, against 0.270 overall (split-auditor,
    issue 5);
  - a model picks the observed best of a site's seven treated microplots 30.8% of the time with the flags and 30.0%
    without them (chance is 14%). The within-site contrasts correlate 0.33 with the flags and 0.31 without
    (domain-practitioner);
  - each site has one microplot per treatment, so the treatment contrast is weakly identified.
- The other gaps in `fit_reason` are wrong or missing:
  - "an 8.6 m2 microplot stands in for a stand" names the wrong gap. The microplot is about the size of a SILVAH
    regeneration plot (10.5 m2). The real gap is that each treatment was applied per plot, not per stand, and the
    herbicide was non-selective (domain-practitioner, gap 3);
  - the fences were "maintained yearly ... except in 2020" (Sec. 2.2). The notes do not say so;
  - there is no pre-treatment overstory, deer impact or fern cover (column-auditor, point 1);
  - the test sites come from two forests and one 2014-2021 cohort. That is narrower than the question's "a central
    Pennsylvania oak-hickory stand": holding out one forest drops R^2 to 0.110, against 0.270 by site (split-auditor,
    issue 4).
- Effect: a reader expects a benchmark of treatment choice. What ships is a benchmark of forecasting a plot's
  regeneration seven years on from its inventory, with the treatment as a small modifier.
- Remedy (fix the definition, text only):
  - rewrite `use_case` around what is scored: a forester forecasts a stand's regeneration seven years after a planned
    treatment, from the pre-treatment inventory, and the data shows the treatment's effect only weakly;
  - rewrite `fit_reason` with the gaps in this order: all species (point 1); a weakly identified treatment contrast;
    treatments applied per plot; no overstory or deer impact in the inventory; two forests and one cohort;
  - keep `fit="approximate"`, so the reworded use case excuses nothing (USE-9's weighed factor);
  - add the 2020 fence lapse to the notes.

**3. The shipped folds often split the two forests unevenly (P4; SPLIT-1 holds for the regime; the fold makeup is a
weighing call that no rule settles).**
- Problem: the grouped folds are not stratified:
  - 15 of the 60 test folds hold at most 2 sites of one forest;
  - one fold holds no site of one forest, so its model trains on 12 sites of one forest and 4 of the other. A
    deployed model trains on 12 and 12;
  - both high-count sites are in Rothrock (`site_110` and `site_120`, mean counts 69 and 74), and in 10 of the 60
    folds they land in the same test fold.
- Evidence (split-auditor):
  - count RMSE is 13.8 on folds with neither high-count site and 35.3 on folds with both;
  - with `stratify_on="state_forest"`, the standard deviation of count RMSE across folds falls from 8.24 to 4.97, and
    the folds holding both sites fall from 10 to 2.
- Effect: a fold's score largely records where the two dense sites fell. With only 8 sites per fold, that noise
  weighs heavily.
- Remedy (fix the definition, optional): `stratify_on = "state_forest"`. `_per_sample_splits` already supports it
  through `StratifiedGroupKFold`. The reason is the fold makeup, not the higher score (SPLIT-21). No grouped
  regression in the copy uses it yet, so the curator decides.

**4. The notes misdescribe the source file and two units (P5; PROV-2 Should, EV-2 Must).**
- Seven file columns have no README entry, not two (claim-auditor row 8):
  - two of them ship as features: `seedlings_all_heights_2014` and `aggregate_height_all_heights_2014_m`;
  - the notes do not say how their meaning was settled: each extra stem adds 0.0762 m, the 0-6 in class midpoint, in
    every row (claim-auditor row 3; column-auditor). Saying so would answer the blind reviewer's concern 2, which
    otherwise stays open in the record.
- "The README says 262 rows, the methods n = 261" is not a mismatch: the README's 262 includes the header row (row
  9).
- The `MN` unit, cmol(+)/kg, is implausible: 206 cmol(+)/kg would be 5.7% of the soil's mass. The values fit mg/kg
  (row 16; column-auditor; blind-reviewer, concern 6). The notes repeat the stated unit.
- `mountain_laurel_volume_2014_m3`: 78 of the 261 values exceed 15.4 m3, the most that an 8.55 m2 plot can hold up to
  1.8 m. The values are an index (cover x height), and our column name gives them a unit they do not have
  (column-auditor, point 2b).
- Effect: no model input changes, but the notes mislead a reader about the source and its units.
- Remedy (notes and one rename):
  - rewrite the anomaly bullet and the `AL`/`MN` bullet;
  - rename the column to `mountain_laurel_volume_index_2014`;
  - cite PROV-2, not PROV-15 (precedent-checker, point 9).

**5. One or two dense sites decide the declared metric, and it ranks first a model that loses to persistence (P6;
MET-1 Must, MET-11 Must, MET-10 Weigh).**
- Problem: the metric is `rmse` on the count, after expm1.
  - On a test fold of 8 sites, one site holds a median 50% of the random forest's squared error (up to 76%). Its fair
    share would be 12.5%; on the log1p scale it holds 21%.
  - 14 of the 60 test folds hold no microplot with 69 or more seedlings (claim-auditor row 31; split-auditor,
    issue 2).
- Effect on the task:
  - The forester acts per plot, against thresholds that rise as a geometric ladder: 15-30-50-100-200 weighted stems
    by deer impact (NRS-33, Table 3.1). An error by a factor of two matters wherever it falls.
  - In squared error, 0 against 3 stems (the difference between a plot that fails and one that regenerates) costs 9.
    70 against 140 costs 4,900.
- Evidence:
  - count RMSE ranks first a random forest fit on raw counts (16.7). Under RMSLE that model (1.175) loses to
    "2021 = 2014 count" (1.168);
  - the two scales rank eight models with Kendall tau 0.21;
  - a ridge fit on the shipped log1p scale scores a count RMSE of 2,543 after the inverse (claim-auditor).
  - A metric that one back-transformed prediction can decide does not choose a model the way a practitioner would
    (MET-1).
- The context origin applies. MET-11's own example is "a price's error matters relative to the price, so `rmsle`";
  the stocking ladder makes this target the same case, and the source models the counts on a log link
  (domain-practitioner). The precedent is blood_tests_drink_prediction (`rmsle` on a count, the curator's CC).
- What sets this case apart from wadden_sea_sibes_macoma_abundance, where the practitioner argued against `rmsle`:
  there the actor sums densities into a food stock, so the mean matters. Here the actor rates each plot on a relative
  ladder. Decide pennsylvania, wadden and nantucket together, with that fact recorded (precedent-checker, point 5).
- Today the TabArena adapter scores `rmse` on the shipped scale (definitions.md, "What the benchmark harness does"),
  which on this dataset is RMSLE. Declaring `rmsle` makes the spec match what is computed now.
- Remedy (fix the definition): `Metric.from_context("rmsle", reason=..., target_transform="log1p")`. Reword bullet 3's
  "an error on one is the same error on the other", which holds only on the count. If the curator keeps `rmse`
  instead, write the site concentration into the notes and into the text that accepts the warning.

**6. The probe and warning texts do not name their baseline or scale (EV-8 Should).**
- "Better than the dummy on every one of 30 splits" holds against the mean count. Against the constant a harness fits
  on the shipped target (the back-transformed mean of log1p), it is 24 of 30 (claim-auditor row 22).
- The proposed text accepting `groups_test_groups_few` says "the random forest beats the dummy on 28 of 30 splits".
  That figure is on the log scale; on the count it is 30 of 30, or 56 of all 60 splits (split-auditor, issue 3).
- "Each site holding every treatment once" should read "every treatment combination once, beside 2-4 controls".
- The acceptance should also state point 5's concentration (one site per fold carries about half the count-scale
  error) or rest on point 3's fix.
- Remedy: reword, naming the dummy and the scale.

**7. The record still carries readings that the add stage superseded (EV-2 Must; stage precedence).**
- The tag `Two-Regime Zeros` fails the curator's rule (policy call 4, 2026-10-30): there are 48 zeros against 38
  ones, the zeros follow the 2014 count (39% against 12%), and a negative binomial on the inventory expects 48.2 zeros
  (claim-auditor row 11; precedent-checker, point 7). Remove it.
- Three statements are superseded or wrong:
  - "Not downloaded (Dryad answers 401)": the version download works without a token;
  - "about 5 sites (55 rows) per test fold in 5 folds": the shipped splits have 3 folds of 8 sites, 85-88 rows each;
  - "south_nation ... confirmed `Too Small`": the curator's recorded reason was "No good target" (precedent-checker,
    point 3).
- The "zero mechanism" paragraph describes a change score that the definition no longer ships.
- "Domoto M.E." should read Emily J. Domoto (Crossref).
- Remedy: the curator updates the record with a dated Assessment line. The definition does not change.

**Dropped (no backing):**
- Blind-reviewer concern 1 (small, a low ceiling, a 500-row floor). No 500-row floor exists in these rules. Under
  TP-5 each fold scores 85-88 rows of a count with spread, and TP-2 says a small signal is no reason to retire. The
  random forest's R^2 of 0.354 compares with a maximum of 0.006 when the target is shuffled (claim-auditor row 32).
- Blind-reviewer concern 2 (columns that cannot be traced): the file has them. Only the notes need to say so
  (point 4).
- Blind-reviewer concern 4 (`site` as a feature): the harness drops the group column, and `n_features` is 12.
- The `No Good Target / Scientific Discovery` marker on a `Yes` record: `selection.md` allows it, so it is the
  curator's weighing call.

```text
Verdict: ship after changes.
Validity: USE-5 approximate with the gap unnamed (fix: point 1); USE-1/USE-8 the use case overstates the treatment
  decision and names the wrong gaps (fix: point 2); LEAK-10 holds; SPLIT-1, SPLIT-29 hold; the fold makeup by forest
  is a weighing call (point 3); PROV-2 notes to correct (point 4).
Value: MET-1 count RMSE decided by one or two sites per fold (fix: rmsle from context, point 5); TP-2, TP-5 hold.
Quality: EV-8 wording (point 6); record fields (point 7, curator).
For the curator: point 5 together with wadden and nantucket; point 3 would be the first grouped regression with stratify_on.
```

</details>

<details><summary>Advocate rebuttal</summary>

**Advocate, rebuttal (2026-11-01): pennsylvania_oak_hickory_regeneration_experiment**

**Where this leaves us.** The critic and I reach the same verdict: ship after changes, and nothing calls for
exclusion. I concede points 1, 2, 4, 6 and 7 as written. On point 3, we agree it is optional. On point 5, I ran the
check that decides it, and it goes the critic's way: I withdraw my defence of `rmse` (my point 6). One of the critic's
examples does not hold, but the conclusion does.

**Check run (point 5).** Script and output are in the run folder. The question:
which declared metric orders models the way the forester's stocking decision would?
- Decision loss used: SILVAH Table 3.1 (NRS-33) counts established desirables as stocked at 15, 30, 50, 100 and 200
  weighted stems per 10.5 m2 plot, for deer impact 1-5. Stems over 1 ft count double.
- Rescaled to our 8.55 m2 microplot and an unweighted count, for weights 1, 1.5 and 2, the thresholds run from 6 to
  163 stems.
- I scored two losses on the first 30 shipped splits, each averaged over the five thresholds: plot-level
  misclassification, and the error per test site in the share of plots stocked.
- Nine models: two dummies, persistence, RF and LightGBM on log1p, RF on raw counts, Poisson LightGBM, ridge and kNN.
- This is a diagnostic only. No threshold is declared (MET-7).

**1. All species counted, and not named (USE-5, USE-8). Concede.**
- This was my point 4, and the remedy is the same: a clause in `predicted`, the target bullet and `fit_reason`, plus
  the optional request to the authors.
- I accept the critic's order: this gap goes first in `fit_reason`.

**2. The use case overstates the treatment decision, and `fit_reason` names the wrong gaps (USE-1, USE-8). Concede.**
- This was my point 3. I accept the critic's rewrite of `use_case` and `fit_reason` and its order of gaps. I also
  accept adding the 2020 fence lapse (Sec. 2.2), which I had missed.
- What I keep: the actor, the treatment as an input, and `fit="approximate"`. The critic keeps them too, and it drops
  the marker as a reason to exclude.
- The new check adds one fact on the critic's side. On the stocking loss, persistence ("2021 = 2014 count") scores
  0.124 against 0.123 for the best models. On the decision a forester makes, the inputs beyond the 2014 count add
  little.
- That fact also belongs in `fit_reason`. It is still TP-2 ("a small but real signal is no reason to retire"), not a
  reason to exclude: the flags' gain stays about six SEs on R^2.

**3. The folds split the two forests unevenly (SPLIT-1; weighing). Narrow: agree it is optional.**
- We agree on the facts and on the remedy (`stratify_on="state_forest"`).
- One point in its favour that the critic does not use: a deployed model trains on 12 and 12 sites. Stratified folds
  train on 8 and 8, unstratified ones down to 12 and 4. So stratifying mirrors the application more closely (SPLIT-1),
  quite apart from the score (SPLIT-21).
- I do not oppose it. It is the first grouped regression with `stratify_on`, so the curator decides. No rule requires
  it before shipping.

**4. Source file and units misdescribed (PROV-2, EV-2). Concede.**
- This was my point 7. The rename to `mountain_laurel_volume_index_2014` is cheap and safe (principles, step 3).
- Stating the 0.0762 m identity in the notes closes the blind reviewer's concern 2 in the record.

**5. Dense sites decide count RMSE; declare `rmsle` from context (MET-1, MET-11 Must; MET-10 Weigh). Concede, with
one example narrowed.**
- The example does not hold. The critic says 0 against 3 stems is "the difference between a plot that fails and one
  that regenerates". Under SILVAH both plots fail at every deer impact: 3 stems is below the lowest threshold of
  6.1, even with every stem weighted double. 61.7% of the microplots sit below that threshold. Small differences at
  the bottom are not what makes `rmsle` the right choice.
- What the check shows instead (Kendall tau between each metric's ordering of the nine models and the stocking loss):

  | stocking loss (w = weight per stem) | tau, count RMSE | tau, RMSLE |
  |---|---|---|
  | misclassified plots, w = 1 / 1.5 / 2 | +0.39 / +0.17 / +0.17 | +0.72 / +0.72 / +0.61 |
  | error in share stocked per site, w = 1 / 1.5 / 2 | +0.44 / +0.33 / +0.39 | +0.56 / +0.67 / +0.61 |

  - Per split, against the w = 1.5 losses: count RMSE +0.43 and +0.45, RMSLE +0.62 and +0.57.
  - Count RMSE puts the ridge at 2,543, yet on the stocking loss the ridge is only a little worse (0.132 against
    0.123). Its count-scale score comes from blow-ups after the inverse, not from wrong decisions.
- The thresholds span 6 to 163 stems on a roughly geometric ladder. The error that matters is relative across that
  span, which is MET-11's context case. The source's log link points the same way. MET-1 (Must) asks for the metric a
  practitioner would choose a model by, and the measurement says RMSLE is that metric. It outranks the MET-10 factors
  I leaned on, which are Weigh.
- Stakes, for the record: the model each metric picks per split is close on the stocking loss (0.116 for count RMSE's
  pick, 0.113 for RMSLE's, against 0.106 for an oracle pick). The ordering of models differs more than the winner
  does.
- What follows:
  - declare `Metric.from_context("rmsle", target_transform="log1p")`, with a reason based on the stocking ladder and
    the site concentration;
  - reword bullet 3's "an error on one is the same error on the other" (it holds on the count only). The level target
    stays (USE-5);
  - as the critic notes, this also matches what TabArena's adapter computes today.
- Siblings: I accept the critic's distinction for wadden (an actor who sums densities, so the mean matters).
  nantucket needs its own fact about the actor. Decide the three together, with each fact recorded.

**6. Probe and warning texts lack their baseline and scale (EV-8). Concede.**
- This was my point 5's remedy. Name the dummy (24 of 30 against the back-transformed log1p mean) and the scale (28
  of 30 on log1p, 56 of 60 on the count).
- If `rmsle` is declared, the warning text cites the log-scale figures and states the site concentration under the
  old metric.

**7. Superseded record readings (EV-2, stage precedence). Concede.**
- The curator applies these as a dated Assessment line: drop the tag, fix "Domoto", supersede the access and fold
  readings and the south_nation reading, and remove the change-score "zero mechanism" paragraph.

```text
Verdict after rebuttal: ship after changes (agreed with the critic).
Changes before shipping: points 1, 2 (text), 4 (notes and one rename), 5 (rmsle from context), 6 (wording).
For the curator: point 3 (optional stratify_on, a first); point 5 decided together with wadden and nantucket;
  point 7 record fields.
```

</details>

<details><summary>Critic rebuttal</summary>

**Critic: rebuttal (2026-11-01), pennsylvania_oak_hickory_regeneration_experiment**

**Where this leaves me: ship after text changes, which is now the advocate's verdict too.** I ran one check on the
metric (A6). It did not support my MET-1 argument, so I withdraw the metric change and keep only a note. The
remaining differences with the advocate are small and all in the text: rewriting `use_case` itself, a column rename,
and the 2020 fence lapse.

**A1. Honest evaluation holds: concede.** I agree with all of it. The leak drops, the fixed-effect bound on PH14, the
split by the source's site, and the answer to blind-reviewer concerns 2 and 4 match my "Dropped" list and my point 4.

**A2. A decision fits (SEL-3, USE-1, USE-2): concede.** I did not contest this. The marker on a `Yes` record is a
record field for the curator.

**A3. A small treatment signal is a gap in the fit (TP-2, USE-8): concede on the remedy, narrow on its scope.**
- Conceded: TP-2 keeps a small real signal, and the fix is text.
- Narrowed: the advocate rewrites `question` and `fit_reason`. `use_case` itself must change too:
  - it says the forester "compares the outcome expected under each combination";
  - `fit_reason` calls the data "the data a treatment-choice model needs";
  - both claim a skill that, on the advocate's own concession, the scores do not measure (30.8% against 30.0%;
    R^2 0.037 within a site). USE-1 (Must) checks every choice against the written use case, so the use case has to
    say what is scored.
- Contested: "This gap is independent of validity, so it does not stack with any Must". A gap in the fit is a P3
  matter, and USE-8, which requires the gap to be named, is a Must. It does not stack, because a text fix resolves it.
  But it is a required fix, not an optional quality fix.

**A4. The target is the source's count; its all-species breadth is a gap to name (USE-5, USE-8): concede.** This is
the same remedy as my point 1. The advocate's own fact (the 8.55 m2 microplot is close to SILVAH's 10.5 m2 plot) also
supports replacing `fit_reason`'s "an 8.6 m2 microplot stands in for a stand" with "treatments applied per plot, not
per stand". The advocate lists that change under A7.

**A5. 24 sites make a tiny-data task, not a `Too Small` one (TP-5): concede.** I dropped blind-reviewer concern 1 on
the same grounds. We agree that the text accepting the warning names the scale and the site concentration.

**A6. The metric is legal as declared: concede after a check. I narrow my point 5 from a MET-1 Must to a MET-10 note.**
- The check (EV-1): it asked whether count RMSE or RMSLE ranks models the way the forester's stocking decisions do.
  - On 30 shipped splits I scored eight models' stocking calls on held-out sites at thresholds of 1, 5, 10, 15, 25
    and 50 stems. I scored them per plot (balanced accuracy) and per stand (the error in the share of stocked plots
    per site).
  - This is a diagnostic only. No threshold is declared (MET-7).
  - Script and output are in the run folder.
- The result is mixed, so the context is not clear:
  - per plot, the model ranking agrees better with count RMSE (Kendall tau 0.57) than with RMSLE (0.14). The model
    fit on raw counts, which count RMSE ranks first, beats the log-fit random forest on 87% of splits;
  - per stand, the ranking agrees better with RMSLE (0.50 against 0.21);
  - persistence ("2021 = 2014 count") beats every model on both diagnostics: balanced accuracy 0.710 against at most
    0.662, and share error 0.128 against at least 0.134. So my line "ranks first a model that loses to persistence"
    does not separate the two metrics. RMSLE also ranks three models above persistence.
- Conceded: MET-1 is not shown violated. MET-11 allows `context` "only when the context is clear", and this check
  shows it is not. The fallback `rmse` stands.
- Still asked (MET-10, Weigh): one site holds a median 50% of each fold's count-scale squared error, and a model whose
  inverse transform blows up can score in the thousands. Write both facts into the notes and into the text accepting
  `groups_test_groups_few`. Decide this dataset, wadden and nantucket together, as the advocate also asks.
- New fact, for information. TP-4 is not triggered: on both metrics the models beat persistence (count RMSE 17.7
  against 20.4; RMSLE 1.07 against 1.17). But on stocking calls at held-out sites, no untuned model beats carrying the
  2014 count forward. The reworded use case (A3) should not promise more than a regeneration forecast.
- Stratification: conceded as optional. No rule asks for it; it stays a weighing call for the curator (my point 3).

**A7. The rest is documentation: concede, with four omissions.** I agree with the advocate's list. It leaves out:
- the column name `mountain_laurel_volume_2014_m3` states a unit the values do not have (78 of 261 values exceed the
  microplot's 15.4 m3). Calling it an index in the notes is not enough while the column name says m3. Rename it to
  `mountain_laurel_volume_index_2014` (PROV-2);
- the fences were "maintained yearly ... except in 2020" (Sec. 2.2), which the notes do not say. The `fence` flag is
  the assignment, not seven years of exclusion;
- deer impact and fern cover are missing from the pre-treatment inventory, beside the overstory (column-auditor;
  domain-practitioner, gap 4). Name them in `fit_reason`;
- in the record, besides the advocate's three fixes: "Not downloaded (Dryad answers 401)", the reading of
  south_nation as confirmed `Too Small` (its recorded reason was "No good target"), and the zero-mechanism paragraph,
  which describes a change score no longer shipped.

```text
Verdict: ship after text changes.
Validity: USE-5 approximate, all-species gap to name (A4, agreed); USE-1/USE-8: rewrite use_case and fit_reason to
  what is scored (A3, narrowed); LEAK-10, SPLIT-1/3/24/29 hold (A1, agreed).
Value: TP-5, TP-2 hold (A5); MET-1 not shown violated after the stocking-call check, fallback rmse kept; MET-10:
  site concentration into the notes and the warning text (A6, conceded and narrowed).
Quality: PROV-2 notes plus the laurel rename; 2020 fence lapse; record fields (A7).
For the curator: the metric of the three count datasets together; stratify_on="state_forest" optional.
```

</details>
