# nantucket_sound_sea_duck_aerial_survey_counts

**Outcome:** added. The AI recommends shipping it with the changes made after the review panel (summarised at the end of
this block), scored by the mean Poisson deviance on the count as you decided on 2026-11-02.
The data are the Mass Audubon aerial strip-transect surveys of Nantucket Sound behind Smith et al. 2019 (Ecology and
Evolution 9:2346-2364; CC0 Dryad deposit doi:10.5061/dryad.1vm20t6, taken from Dryad's own Zenodo mirror): one row per
1.5 km grid segment flown on one of 30 survey days in the winters 2003/04 to 2005/06, 7,751 rows over 454 segments. The
target is the number of long-tailed ducks on the water in the strip of about 180 m flown through the segment (57.1%
zeros, up to 3,000), shipped as log1p and scored on the count. Known: position, seabed, tides, a ferry route, ocean
colour, modelled sea temperatures, the winter's NAO index, the winter and day, and the strip length flown. Whole 4.5 km
blocks of the grid (3 x 3 segments) are held out with all their survey days, so a test block stands for squares the
plane did not fly, with the same day's counts elsewhere in training. Your CC of 2026-10-30 asked to try it and drop it
to `No` if it turned out a bad task; it has a modest real signal.

Validity:
* SEL-2 holds: your `Yes` of 2026-10-30, under your policy call 1 of the same day (species mapping is judged per
  dataset).
* USE-3 triggered, fixed in the text: the moment is after the last survey of 2005/06, when the source drew its maps
  from all 30 surveys, so the 2002-2006 ocean-colour means and the winter means are known then. The score leans on
  the survey day's level, learned from the other squares flown that day; the notes say so, and that the source's
  maps are drawn for dates without a survey (issue 1).
* USE-5 holds: the count is of ducks on the water (the deposit equals NOAA NCEI's record of the same flights minus
  the birds marked flying on 3,609 of 3,612 segment-days). The notes add that the surveys, flown by day, miss the
  long-tailed duck's night use of the Sound (Allison, Perkins & Perry 2009, MMS 2009-020).
* USE-8 triggered, fixed: fit approximate, not direct as first written. One day's daytime strip count stands for the
  seasonal density per square that planners read off the source's maps, and no source names anyone who fills in single
  survey days (USE-9 not met; 5g_energy_consumption, whose gap-filling task was its source's own, is set apart).
* SPLIT-1 triggered, fixed: single held-out segments kept their neighbours on the same north-south flight line,
  flown minutes apart, in training. These made about 30% of the score: 95% of test rows had a square flown the same
  day within 1.5 km in training, against 43% of the survey days of the squares never flown. Re-split on 3 x 3 grid
  blocks, built exactly from the coordinates (SPLIT-24), where 43% of test rows have one; the regime is issue 1.
* LEAK-10, LEAK-30 and LEAK-33 hold: no column is computed from the counts, and the table is rebuilt from the
  authors' unscaled covariates (their analysis files scale every column over all rows). LEAK-25 holds with a note:
  800 ducks that NCEI places on transect 11-10 on 2006-03-06 are in no deposit row, probably flying birds; the rows
  stay.
* PROV-3, PROV-8 and PROV-13 hold: Zenodo's md5 equals Dryad's own listing. NCEI holds 7 more winter survey days
  that the paper leaves out; noted, not added (PROV-14).

Value: TP-2, a modest real signal: untuned LightGBM R^2 0.18 on log1p on the block splits (folds 0.09-0.26), and a
LightGBM with a Poisson loss 9.8% below the training mean's Poisson deviance on 9 of 9 folds. TP-5 holds (20 test
blocks, 2,337-2,823 rows per fold). MET-11: the metric is a stand-in for the source's out-of-bag likelihood: the mean
Poisson deviance on the count, predictions floored at 0.01 ducks (your call of 2026-11-02).

Quality: the Decision's reason is rewritten (its own table showed the eider less dominated by single flocks); `depth_m`
is now `seabed_elevation_m` (its values are negative elevations); the winter and the day of the winter stand in for the
date, as in the source's Table 1. The one check warning, `task_target_value_dominant`, is issue 4.

Weighed: a CC0 deposit with the authors' code and an independent NCEI record +; a use case the source names (siting
offshore wind farms and protected areas), fit approximate 0; 7,751 rows in 60 blocks +; a weak signal on the count,
where RMSE cannot rank models -. Left for Andrej: issues 1, 3 and 4 and the two record-field rows.

After the review panel (AI, 2026-11-01) the definition took the mediator's changes: the re-split on grid blocks
(`segment` dropped from the frame), the regime and split texts, the prediction moment, the survey-day framing, the
fit, the notes on the target and on the zeros of 2006-03-06, the metric's origin, the Decision, `depth_m`, the note
on the date and the wording slips. The numbers here are measured on the block splits of the changed definition, so
some differ from the panel's, which used single segments (R^2 0.18 against 0.25).

**Main points:** the split holds out whole transects as the field does (1, resolved 2026-11-03) and the zero warning
is accepted (4, resolved); the metric is the mean Poisson deviance (2, closed 2026-11-02). Left: one model over the
three species groups (3, answered: keep the long-tailed duck alone) and the few-groups warning of the new split.

**Issues for Andrej:**

1. **Confirm whole 4.5 km blocks of the survey grid as the test unit?**

   * **Problem:**
     - The test rows should stand for the squares the plane did not fly.
     - Which unit is held out: blocks of 3 x 3 segments with all their survey days (now), single 1.5 km segments (the
       first build), or whole transect columns?
     - Your CC was given on a temporal split instead.
   * **Background:** The first build held out single 1.5 km segments; the flights run north-south, so a held-out
     segment's two neighbours on the same flight line, flown minutes apart that day, stayed in training. After the
     panel, blocks of 3 x 3 segments are held out with all their survey days. Your CC was given on the screening's
     temporal split (later winters from earlier ones).
   * **Experiments:** under single segments, 95% of test rows had a training square flown the same day within 1.5 km,
     against 43% of the survey days of the 50 squares never flown (all on the grid's border) and 43% under blocks
     (36-51% per fold). Those neighbours made about 30% of the score: R^2 on log1p 0.251, and 0.177 with only them
     removed from training (removing as many random rows: 0.247). Blocks score 0.18 (folds 0.09-0.26).
   * **Effect on the task:** the day's level stays known. The score leans on the same survey day's counts in other
     squares (alone R^2 0.13 of LightGBM's 0.18 on the block splits), which anyone filling in a surveyed day has, and
     the field's models carry the survey as an effect (BOEM Sec. 2.4). The source's maps, though, are drawn for dates
     without a survey (Figs. 4-6). Tested that way (a new square on a date not in training), no model beats the
     training mean on the count (LightGBM R^2 -0.077 on log1p), so that framing would be `No`[^1e]. No panel agent
     argues for it.
   * **Why not temporal:** neither the covariates nor a segment's own past predict a later winter (R^2 0.04 and 0.025
     on log1p). A model on the features does not clearly beat each segment's naive forecast, so a split by winter would
     make it forecasting, which is out of scope (`No`)[^1c]. The source maps the winters it surveyed, never a later one
     ([paper](https://doi.org/10.1002/ece3.4738), Sec. 2.5).
   * **Consistency:** the split mirrors the application, and the regime is your pick[^1a]. Blocks are built exactly
     from the grid[^1d]. airfoil_self_noise was re-grouped when 91.5% of its test runs had a close neighbour in
     training[^1b]. The field holds out whole transects ([BOEM
     2018-010](https://espis.boem.gov/final%20reports/BOEM_2018-010.pdf), Sec. 2.5.6), which is option C.
   * **Panel:** the advocate and the critic agree on blocks.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | 3 x 3 grid blocks (implemented) | holds out blocks of 3 x 3 segments (60 groups) with all their survey days; 3 repeats of 3 folds | a test block has a same-day flown square within 1.5 km as often as a never-flown square does (43% each); exact from the grid | the field holds out whole transects instead |
     | B | Single segments | holds out single 1.5 km segments, as the first build, with a note on the optimism | the highest score (0.251) | a measured 30% overstatement of how well models fill gaps |
     | C | Whole transect columns | holds out whole north-south transect columns (24 groups), as BOEM | the field's practice | on the count no model beats the training mean (RMSE better on 3 of 9 folds) |
     | D | Warm start | holds out one transect column on one survey day, so a square's other survey days stay in training (R^2 0.28-0.30) | 80% of the unflown segment-days belong to squares flown on other days, whose own counts a gap filler would use | it rewrites the question |

   * **Recommendation:** A, blocks: a test block has a same-day flown square within 1.5 km in training no more often
     than a never-flown square does (43% each). **Decision:** A, B, C or D?

   [^1a]: **SPLIT-1** (Must): the split mirrors the real-world application, and the curator picks it. **SPLIT-3**
     (Must): a non-IID task is grouped or temporal, never both; the use case decides. **USE-10** (Must): decide from
     the use case whether the entity is new or known before choosing the split.
   [^1b]: airfoil_self_noise, a case under **SPLIT-1**.
   [^1c]: **TP-10** (Must): a panel with one series per entity is a tabular task only when (leg 1) a model on the
     features clearly beats each entity's naive forecast on the shipped windows, among other conditions; leg 1 fails
     here. **SEL-10** (Must): time-series forecasting is out of scope.
   [^1d]: **SPLIT-24** (Must): group on a true group id, or on one constructed exactly from the data; never on a
     similarity-threshold cluster.
   [^1e]: **SPLIT-28** (Must): a regression task whose models all score below the mean on unseen groups has no signal
     across groups; then the use case has to allow known groups, or the dataset goes.

   **Andrej (2026-11-03, discuss):** We should definitely use what the field uses. We should stay as realistic and
   close to the real application as possible.

   **Resolved (2026-11-03, Andrej):** C, whole transect columns, the field's practice (BOEM 2018-010, Sec. 2.5.6): the
   group column is now `transect_column`, 24 columns of the source's grid. The "no model beats the mean" above was
   measured on RMSE; on the declared metric, the mean Poisson deviance, a Poisson LightGBM beats the training mean on 9
   of 9 folds (4.2% of its deviance explained, against 7.9% under blocks; 3 repeats of 3 folds, Slurm). `dataset check`
   is clean but for `groups_test_groups_few` (8 transects per test fold), which needs your call.

3. **Keep the long-tailed duck as the one target of these surveys?**

   * **Problem:**
     - The source models three groups apart (common eider, scoters of four species pooled, long-tailed duck); we ship
       one.
   * **Effect on the task:** it sets which birds the task is about; the other two are left out.
   * **Experiments:** on held-out blocks the long-tailed duck has more signal than the eider (untuned LightGBM R^2 0.18
     on log1p, eider -0.08) and fewer zeros (57% against 75%). The scoters reach 0.20, but one raft of 70,000 holds 67%
     of their squared deviation, so an error on their count would come down to one row. The eider's largest counts
     dominate less (its 10 largest hold 70% of the squared deviation, against 84% for the long-tailed duck).
   * **Consistency:** each group is a target the actor could act on, so the choice is a weighing[^3a], as in
     noaa_afsc_bottom_trawl_survey_cpue issue 1. The choice read all rows, test folds included, which counts as
     ordinary cleaning[^3b], as the species pick of noaa_afsc_bottom_trawl_survey_cpue did.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Long-tailed duck (implemented) | the target stays the long-tailed duck count | the most signal of the three on held-out blocks; fewer zeros | its largest counts dominate more; the surveys, flown by day, miss most of its use of the Sound (MMS 2009-020) |
     | B | Common eider | the target becomes the common eider count | its largest counts dominate less | below the training mean on held-out blocks (R^2 -0.08 on log1p), so it likely has no signal to keep it on[^3c] |
     | C | A second group as a sibling | adds a sibling dataset with the eider or the scoters as its target, on the same rows[^3d] | the source's other groups covered | shares the rows and covariates |

   * **Recommendation:** A, keep the long-tailed duck: it has more signal on held-out blocks than the eider, and its
     score does not rest on one raft as the scoters' does. **Decision:** A, B or C?

   [^3a]: **USE-5** (Must): predict what the actor would act on, at the resolution they act on it; it holds for each
     group.
   [^3b]: **CLEAN-8** (Must): choosing which columns or categories to keep by counts over the whole table is ordinary
     cleaning that follows the task's best practice.
   [^3c]: **TP-2** (Should): a small but real signal is no reason to retire; the eider's score suggests none.
   [^3d]: **PROV-7** (Must): records that share a source but give different tasks are not duplicates; the comments
     say why they are distinct.

   **Andrej (2026-11-03, discuss):** Can't we predict both at the same time with one model, by using an additional
   feature for the species and concatenating?

   **Answer (AI, 2026-11-03):**

   * **Problem:**
     - We can: one row per segment-day and species group, the group as a feature, as noaa_afsc_bottom_trawl_survey_cpue
       ships its taxa.
     - Measured under the transect split, one model over the three groups predicts the long-tailed duck worse than a
       model of it alone, and the other groups no better.
     - The field also models the groups apart (the source fits one hurdle model per group), and a pooled score would
       be decided by the scoters' raft of 70,000 unless the metric scores each group against its own level.
   * **Experiments:** Poisson LightGBM, transect columns, 3 repeats of 3 folds; share of the training mean's Poisson
     deviance explained per group (folds above the mean, of 9):

     | Group | Its own model | One model over the three groups |
     |---|---|---|
     | long-tailed duck | 0.042 (9) | -0.081 (2) |
     | common eider | 0.054 (6) | 0.064 (7) |
     | scoters | 0.169 (6) | 0.150 (8) |

   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Long-tailed duck alone (implemented) | one target, as now | the steadiest signal (above the mean on 9 of 9 folds); as the field models a group | the other groups left out |
     | B | The three groups stacked | one row per segment-day and group, the group a feature; a metric that scores each group against its own level (new in the library) | one model for the Sound's sea ducks | the long-tailed duck falls below the mean; a new metric; scores swing with one scoter raft |
     | C | The three groups as sibling datasets | one dataset per group, each its own model | the field's practice for every group | three datasets on the same rows; the eider and the scoters above the mean on 6 of 9 folds only |

   * **Recommendation:** A: one model over the groups costs the long-tailed duck its signal, and the field fits each
     group on its own. **Decision:** A, B or C?

   **Notes for the AI:** script `nantucket/designs.py` and its log in the run folder of 2026-11-03.

   **Andrej (2026-11-03, discuss):** Your experiments were too weak. Try with TabPFN

   **Answer (AI, 2026-11-03):**

   * **Problem:**
     - Rerun with TabPFN (A100, Slurm) on the same transect-column folds, 3 repeats x 3 folds, scored per species by
       D^2 under the mean Poisson deviance against that species' training mean.
     - Fit on the count (its predicted mean), TabPFN is far stronger than LightGBM, and every species keeps more
       signal alone than stacked; the long-tailed duck loses half of it stacked.
     - Fit on log1p, every design falls below the mean (the back-transform loses the large flocks), so the count
       scale is the one that counts.
   * **Experiments:** D^2, mean over 9 folds (folds above the training mean):

     | Group | Own model | Stacked model | LightGBM own (earlier) |
     |---|---|---|---|
     | long-tailed duck | 0.153 (9 of 9) | 0.074 (7 of 9) | 0.042 |
     | common eider | 0.219 (9 of 9) | 0.217 (9 of 9) | 0.054 |
     | scoters | 0.346 (9 of 9) | 0.316 (9 of 9) | 0.169 |

   * **New fact for the target choice:** the long-tailed duck was picked because LightGBM found more signal for it
     than for the eider. With TabPFN the eider (0.219) and the scoters (0.346) both hold more than the long-tailed
     duck (0.153). Stacking is still no gain, but if you want the target re-chosen on this, say so and I will set
     the options (the scoters' single raft of 70,000 is the known risk).

   * **Recommendation:** A, unchanged and now firmer: with a strong model the long-tailed duck alone keeps twice the
     signal it keeps stacked, and no species gains from stacking. **Decision:** A or B?

   **Notes for the AI:** script `nantucket/tabpfn_designs.py`, data `nantucket/prep.py`, results
   `nantucket/tabpfn_designs.csv` in the run folder of 2026-11-03 (Slurm job 1343021).

   **Andrej (2026-11-03, discuss):** Since this is now clear, would it make sense to use different birds as different
   splits?

   **Answer (AI, 2026-11-03):**

   * **Problem:**
     - Read as three datasets, one per species: they share every row, every input and the map decision, and differ
       only in the counted species, which our duplicate rule counts as a duplicate unless it adds a distinct task[^3x].
     - Each would weigh the same survey three times in the benchmark, while the long-tailed duck is the species the
       source's siting question at Horseshoe Shoal was about.
     - Read as holding out a species to test on it: no planner maps one species from the others, so no use case.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | One dataset, the long-tailed duck (implemented) | as now | the source's siting species; one survey counted once | the eider and the scoters show more signal with TabPFN (0.219, 0.346 against 0.153) |
     | B | Three datasets, one per species | the eider and the scoters added as their own folders, same split and metric | each species' map is its own product in the source | three near-copies of one survey; needs a distinct-task reason under the duplicate rule |
     | C | One dataset, another species | the target becomes the scoters or the eider | more signal | the scoters' one raft of 70,000; the eider's 75% zeros; not the siting species |

   * **Recommendation:** A: the three are one survey and one decision, so one dataset; the long-tailed duck is the
     species the source's question was about and keeps a clear signal (9 of 9 folds). **Decision:** A, B or C?

   [^3x]: **PROV-6** (Must): versions or cuts of one dataset, a swapped target among them, are duplicates when
     neither adds a distinct task. **PROV-7** (Must): records that share a source but give different tasks are not.

   **Andrej (2026-11-03, discuss):** You didn't get it. I mean one dataset, but the train test splits being different
   targets, since they represent the same task

   **Answer (AI, 2026-11-03):**

   * **Problem:**
     - Yes, that can be built: the table holds each segment-day three times, once per species group, with a
       `species` column and the count of that species as the target; each split trains and tests on one species
       only, so a model never mixes them.
     - The splits: the 3 transect-column repeats x 3 folds for each species, 27 splits in all, the same transects held
       out for every species; the score per split is the mean Poisson deviance of that species.
     - It is one task (map a sea duck's abundance from the survey) scored on three species, and the survey is counted
       once; with TabPFN each species' split beats its training mean on 9 of 9 folds (D^2 0.153, 0.219, 0.346).
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Long-tailed duck only (implemented) | as now, 7,751 rows, 9 splits | the usual shape; the source's siting species | uses one of the three counts |
     | B | One dataset, a species per split | 23,253 rows (7,751 x 3) with `species`; 27 splits, each on one species | your design; one task scored on all three species; the survey counted once | the first dataset whose splits differ in target; the scoters' raft of 70,000 sits in their splits; anyone who ignores the splits would pool species |

   * **Recommendation:** B: it scores the one task on all three species without counting the survey three times, and
     each species keeps a clear signal. I would record it as a first in the splits knowledge, and check that the
     bundle checks read a per-species frame sensibly. **Decision:** A or B?

   **Notes for the AI:** on B, override `_make_splits` (custom splits: for each species, the rows of that species
   only, folds from the transect columns as now), add `species` as a categorical feature, rebuild the target as the
   row's species count, and rewrite the task summary, notes and `splits_comment`; run `dataset check` and the probes
   on Slurm, the probes per species.

   **Andrej (2026-11-03, change):** I realized that this is a multi-target task.

   **Resolved (2026-11-03, Andrej):** the data hold three distinct targets per segment-day (long-tailed duck, eider,
   scoters); the dataset goes to 2nd Tier and does not ship (dataset note below), so no single target is chosen.

4. **Accept the warning `task_target_value_dominant` with the reason below?**

   * **Problem:**
     - The check warns that one value, zero, holds 57.1% of the target.
     - Here a zero is an observed absence: a strip the plane flew with no long-tailed duck on the water, not a cap, a
       placeholder or a missing count.
     - Accept the warning with that reason?
   * **Background:** The source on its zeros: "assumed our survey design led to a low incidence of false zeros" (Sec.
     2.2). One known gap, 800 ducks absent on 2006-03-06, is noted[^4a].
   * **Effect on the task:** nothing in the data; the reason is stored in `accepted_check_warnings`.
   * **Consistency:** your zero policy, as accepted across this batch (avito_demand_prediction_1m,
     australian_vehicle_insurance_2004_2005)[^4b].
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Not accepted (implemented) | the warning stays open; adding it is your step | none proposed | the warning stays on the dataset |
     | B | Accept with the reason | the reason goes into `accepted_check_warnings` | follows the zero policy and the batch | none proposed |

   * **Recommendation:** B, accept with the reason "57.1% zeros: observed absences, a flown strip without a
     long-tailed duck on the water". **Decision:** accept with this reason (B)?

   **Notes for the AI:** on B, add `task_target_value_dominant` with the reason above to `accepted_check_warnings` in
   `dataset.py` (add-dataset step 6) and re-run `dataset check`.

   [^4a]: **LEAK-25** (Must): "no event" mixed with "not recorded" is a censoring bias; the one known gap is noted.
   [^4b]: Andrej, 2026-10-30, question 2 (the zero policy).

   **Andrej (2026-11-03, change):** We accept since this is a totally valid zero-inflated regression task

   **Resolved (2026-11-03, Andrej):** B, `task_target_value_dominant` accepted in `accepted_check_warnings` with the
   reason above.

   **Andrej (2026-11-03, dataset note; metric ok):** I realized that this is a multi-target task. Therefore I
   declare it 2nd tier and don't ship

   **Resolved (2026-11-03, Andrej):** don't ship: the record is `TBD -> 2nd Tier` with the `Multi-target` tag, its
   `v2_path` cleared and its claim released; the folder leaves the working copy (copies of its last files, with the
   transect split, in the run folder of 2026-11-03, `nantucket_retired/`). It can come back if the format gets
   multi-target tasks.

**Review panel:** ship after changes (mediator). Claim audit: 54 claims, 39 hold, 13 refuted or partly refuted (fixed in
the definition; the record's four at hand-over), 1 metric concern (issue 2), 1 untested. Blind review: include with
changes; main concerns the `segment` id and the optimism of single held-out segments (both fixed by the block re-split).
Debate: agreed on the verdict, the re-split on 3 x 3 grid blocks and the text, data and zero fixes; disputed: the
interim metric (issue 2), the fit label (settled by rule: approximate) and the dated-map framing (one alternative of
issue 1).

<details><summary>Mediator</summary>

**Mediator: nantucket_sound_sea_duck_aerial_survey_counts (mediator, 2026-11-01)**

**Recommendation**

```text
Verdict: ship after changes.
Validity: SEL-2 holds (CC Yes 2026-10-30; policy call 1). USE-1, USE-2 hold. USE-3 triggered, fixed in the text (the
  moment is after the last survey of 2005/06; the dates of Figs. 4-6 are not survey days, and the score leans on the
  survey day's other counts). USE-5 holds, notes added (ducks on the water; daytime use only). USE-8 triggered,
  fixed: fit approximate (USE-9's condition not met). LEAK-10, LEAK-30, LEAK-33 hold; LEAK-25 holds with a note (800
  ducks of 2006-03-06). SPLIT-1 triggered, fixed: re-split on 3x3 blocks of the source's grid (SPLIT-24). SPLIT-3
  and USE-10: grouped; temporal fails TP-10 leg 1 (issue 1 confirms the regime). PROV-3, PROV-8, PROV-13 hold.
Value: TP-2, a modest real signal (untuned LightGBM R^2 0.18 on log1p on the block splits; a Poisson LightGBM 9.8%
  below the training mean's Poisson deviance on 9 of 9 folds). MET-3 holds. MET-5/MET-11 triggered, fixed: origin
  stand-in, naming the source's out-of-bag likelihood. MET-1 triggered for rmse on these folds; remedy the Poisson
  deviance (issue 2, one call with wadden issue 3 and pennsylvania issue 4).
Quality: Decision reason rewritten (EV-7, CLEAN-8); depth_m renamed (CLEAN-1); the winter and day kept in place of
  the date (CLEAN-12 departure, noted); wording slips fixed (EV-7).
Weighed: source + (CC0 deposit with the authors' code; NCEI cross-check); use case + (the source names siting), fit
  approximate; size + (7,751 rows, 60 blocks); weak signal on the count -.
For the curator: issue 1 (confirm 3x3 blocks), issue 2 (Poisson deviance or rmse), issue 3 (the species, a weighing).
```

The advocate and the critic agree on the verdict, the re-split on 3x3 grid blocks and the text, data and zero fixes.
Three points stayed disputed. I settle the interim metric and the fit label by rule, after one experiment, and fold
the dated-map framing into issue 1 with its measured consequence. Scripts and outputs are in the run folder (not
committed): m0 (the block splits made by the definition's own splitter), m1 (metric ranking, wadden's test), m2
(block R^2), m3 (per model).

**Agreed facts**

* Source: Dryad doi:10.5061/dryad.1vm20t6 through Dryad's Zenodo mirror 4932958; its md5 equals Dryad's own listing,
  and the three raw sha256 sums reproduce. Dryad answers 401 per file and 405 on its version route. CC0, 2019.
* Rows: 7,751 segment-days of 30 surveys (13/10/7), 454 of 504 segments flown; covariates equal `env.segs` to 1e-15;
  the rebuild from unscaled covariates avoids the authors' all-row `scale()` (LEAK-30).
* Target: 57.1% zeros, maximum 3,000, non-zero median 7; counts of 100 or more are 3.6% of non-zero rows and hold 45%
  of the ducks. The deposit equals NCEI 0115356's in-strip count minus birds marked flying on 3,609 of 3,612
  segment-days (daily ratio 1.000 in 2003/04-2004/05). 2005/06 has no behaviour field; two flocks (711 and 800) are
  missing, probably flying, not shown.
* No column leaks (LEAK-10); `segment` is the group, not a feature; the after-season covariates carry about 0.003 R^2.
* Same-transect optimism: removing only each test row's same-day north-south neighbours from training takes R^2 on
  log1p from 0.251 to 0.177 (SE 0.007); east-west neighbours +0.002, as many random rows -0.004. 95.3% of shipped test
  rows have a same-day flown square within 1.5 km in training, against 43.1% of the never-flown squares' survey days
  (all 50 on the grid's border) and about half for 3x3 blocks.
* The survey day's level (other squares flown that day) gives R^2 0.146 of the shipped 0.249; a new square on a date
  not in training scores -0.077 (training mean -0.007). The field validates with the survey known (BOEM 2018-010 Sec.
  2.4, survey ID as a random effect; Sec. 2.5.6, CV stratified by transect).
* Temporal: TP-10 leg 1 fails under every metric (R^2 0.042 against 0.025 for the segment's past mean; RMSE 105.9
  against 106.6).
* Metric: 1-2 of about 2,600 test rows per fold hold half the squared deviation. RMSLE ranks first the back-transformed
  log1p fits, whose predictions sum to 20-28% of the observed test total on the block splits. The source tunes by out-of-bag negative
  log-likelihood (Sec. 2.3.2), which needs a predictive distribution. `mean_poisson_deviance` is not in
  `src/data_foundry/v2/metrics.py` (its regression metrics: rmse, mae, mse, r2, rmsle, mape, median_absolute_error,
  pearsonr, spearmanr).
* The Decision's reason is refuted by its own table (the eider is less raft-dominated: top 10 0.699 against 0.844).

Facts settled by my checks (3x3 blocks built by the definition's default splitter, seed 4267; 8 untuned fits and the
training mean; scored on the count):

| | RMSE | Poisson deviance (floor 0.01) | RMSLE |
|---|---|---|---|
| training mean | 64.37 | 46.03 | 1.96 |
| best fit against the mean | LightGBM Tweedie -0.4% (7/9 folds) | LightGBM Poisson -9.8% (9/9) | RF on log1p -39% (9/9) |
| fits worse than the mean on average | 6 of 8 | 6 of 8 | 2 of 8 |
| log1p LightGBM (28% of the test total) against Poisson LightGBM (68%) | 64.30 against 64.41 | 51.99 against 41.50 | 1.21 against 1.46 |
| model order kept when each fold's 1-10 largest counts go (Kendall tau, median) | 0.78-0.89 | 0.72-0.89 | 1.00 |
| model order agreement between folds (tau) | 0.44 | 0.68 | 0.81 |

The deviance's order barely moves with the floor (tau 0.94 between floors 0.01 and 1). So RMSE's order is not noise
(wadden's test passes), but RMSE cannot tell a fit whose totals are 3.5 times too small from a calibrated fit or from
the constant. At wadden it could: the Tweedie fit beat the biased one by 4% on 9 of 9 folds.

**Changes to make now (no decision needed)**

1. Re-split on 3x3 blocks of the source's grid (SPLIT-1, Must; SPLIT-24; agreed). In `_clean`: `col =
   round((utm19n_easting_m - min) / 1500)`, `row` likewise from the northing (the minima, 380,259.48 E and
   4,574,871.94 N, are the south-west cell of the 504-cell grid), `grid_block = f"{col // 3}_{row // 3}"`; group on
   `grid_block` (`labels="per_sample"`, `prediction_unit="row"`, `context="none"`), type it categorical, and drop
   `segment` (no longer the group; a 454-level id unseen in every test fold; CLEAN-3). It should reproduce: 60 blocks
   (2 to 193 rows, median 158.5); 20 test blocks per fold; test 2,337-2,823 rows, train 4,928-5,414; untuned LightGBM
   (300 trees, rate 0.05, 31 leaves) R^2 0.182 on log1p (folds 0.093-0.258), Spearman 0.45; the m3 metric numbers
   above. Rewrite `task_summary.split`, `splits_comment`, `grouping.definition` and the regime bullet: a test block
   stands for squares the plane did not fly, about half its rows having a same-day flown square within 1.5 km, as the
   never-flown squares do (43%); re-measure the notes' probe and metric numbers on the block splits.
2. The regime text (SPLIT-4; the forest_fires Tensions row): TP-10 as what the other regime would mean ("a forecast of
   a later winter fails TP-10 leg 1, so a temporal task would be `No` under SEL-10; the regime follows the source's
   maps of the surveyed winters"), and "neither the covariates nor a segment's own past predict a later winter (R^2
   0.04 and 0.025)" in place of "decided by each segment's own past".
3. The prediction moment (USE-3, LEAK-10): "after the last survey of 2005/06 (spring 2006)" in `use_case`, the first
   bullet and the Note bullet; the 2002-2006 ocean-colour means and 2003-2005 tidal means are known then (precedent
   check B, option b; wadden). The builder's draft issue 2 closes.
4. The survey-day framing (USE-3, SPLIT-23, EV-7): say that the dates of Figs. 4-6 are not survey days; that the task
   fills in a surveyed day, with the day's level learnable from the other flown squares, as BOEM validates; and add
   the double hold-out (-0.077) and the day's share (0.146 of 0.249) to the notes.
5. Fit `approximate` (USE-8, Must): `fit_reason` names one daytime strip count on one survey day standing for the
   seasonal per-cell density planners read, the long-tailed duck's daytime absence (Allison, Perkins & Perry 2009, MMS
   2009-020), and `transect_km` known for test rows where a map sets 1.5 km.
6. The target (USE-5): ducks on the water (flying birds left out; the NCEI match above, which replaces the "median 94%"
   sentence); one sentence on 2005/06 and its two missing flocks.
7. Zeros (LEAK-25): keep the rows; a note names 2006-03-06, transect 11-10, 800 ducks absent from the deposit and from
   the authors' `obs_poly.dbf` (precedent check D, option a).
8. The metric's origin (MET-5, Should; MET-11, Must): `Metric.stand_in("rmse", original=<the out-of-bag negative
   log-likelihood of the boosted GAMLSS hurdle model, Sec. 2.3.2, with the pseudo-R^2 on it, Sec. 2.5>, reason=<needs
   a predictive distribution; the survey totals of Fig. 8 are a plot; rmse until issue 2 is decided>,
   target_transform="log1p")`. The build waits for issue 2.
9. The Decision (EV-7, CLEAN-8): the long-tailed duck for its held-out signal (R^2 0.26 against 0.15 for the eider) and
   fewer zeros (57% against 75%); the scoters because one raft holds 67% of their squared deviation; chosen on all
   rows, test folds included (as noaa_afsc).
10. Wording (EV-7; PROV-8): non-zero counts (median 7; 100 or more: 3.6% of rows, 45% of ducks); `transect_km` "above
    about 1.6 km (94 rows) where a transect crossed twice"; the deposit's other files are a README and two fitted-model
    archives; `task_summary.known` adds the winter; the download text names the version route's 405 and Dryad's own
    md5.
11. `depth_m` to `seabed_elevation_m`, values kept (CLEAN-1).
12. The date stays dropped for the winter and the day of the winter, the source's own covariates (a winter spans two
    calendar years); the notes say so as a departure from CLEAN-12 (Should; precedent check C, option a).
13. Record: add `v2_path`; a dated Assessment line correcting the screening's slips (the strip is about 180 m, not
    91 m; the "crucial" quote is about understanding distribution; the source's R^2 is a likelihood pseudo-R^2).
    `required_split` and the tag are field rows for the curator.

**Changes that need the curator, ranked**

1. Confirm the regime and test unit: grouped by 3x3 grid blocks (P4; SPLIT-1, SPLIT-3, USE-10, Must). The pick is
   the curator's (SPLIT-1), and the screening's `Temporal` was the basis of the CC. Both debaters back blocks.
   Alternatives with measured costs: single segments with a note (30% of the skill from neighbours a real gap rarely
   has); transect columns as BOEM (no model beats the constant on the count: RMSE better on 3 of 9 folds, deviance
   -2.7%); warm start by transect column x survey day for the 80% of unflown segment-days whose squares were flown on
   other days (R^2 0.28-0.30; rewrites the question); temporal (TP-10 leg 1 fails: `No`, SEL-10); the source's maps on
   dates without a survey (no signal on the count: `No`, SPLIT-28).
2. The metric (P6; MET-1, MET-11 Must; MET-5 Should; MET-10 Weigh): `mean_poisson_deviance` on the count as the
   stand-in, or keep `rmse`. Recommended: the deviance. Cost: a standard scikit-learn metric added to the library
   with tests (MET-12, MET-13) and a floor rule shared by the family. Decide with wadden issue 3 (rmse or deviance) and
   pennsylvania issue 4 (rmse or rmsle).
3. The species (P6; a weighing as noaa_afsc issue 1): keep the long-tailed duck, take the eider, or add a second group
   as a sibling (PROV-7). Recommended: keep.

Also for the curator, as in wadden: an acceptance reason for `task_target_value_dominant` (57.1% zeros: observed
absences, a flown strip without a long-tailed duck on the water).

**Disputed points**

* The interim metric: the critic, no `rmse` until the family call (MET-1, Must); the advocate, `rmse` with the tail
  note until the call (siblings; TP-2). Facts first: m1 and m3 above. RMSE scores the right quantity in expectation,
  the mean count the maps and the survey totals sum, but on the block folds it ties a fit whose totals are 28% of the
  observed with one at 68% and with the constant (64.30, 64.41, 64.37). A metric that cannot see a 3.5-fold shortfall
  in totals does not score this decision, so MET-1 is triggered here, which it was not at wadden. The remedy is on the
  definition rung (MET-1 sits in P6, and a metric never excludes a dataset): the stand-in the source's criterion
  points to (MET-11), the Poisson deviance. Its cost is a library metric and a floor shared by three datasets, so the
  curator decides it as one call. Settled: `rmse` stays declared until then (MET-13 bars declaring a metric the
  library lacks), labelled as a stand-in; the build waits for issue 2 (the critic's substance); the recommendation is
  the deviance. Not RMSLE: the context points to the mean scale (MET-11 allows `context` only when the context is
  clear), and it ranks first the fits with 20-28% of the totals; every panel agent agrees.
* The fit label: the advocate, `direct` once the split mirrors the gaps (USE-9; 5g_energy_consumption); the critic,
  `approximate` (USE-8, Must). USE-9 (Should) narrows USE-8 only when the data mirrors "another well-defined use case
  that practitioners have". The advocate concedes that no source names a survey-day fill-in, and BOEM's practice is
  a way of validating models, not a decision. The source's product, the map planners read, is the per-cell median over
  10 dates per winter that are not survey days; the label is one survey day's daytime strip count. That is a stand-in
  with a known gap: approximate, after the re-split too. 5g is set apart: there the gap-filling task was the source's
  own (the competition's test file weights new stations).
* The dated-map framing (SPLIT-28): the split auditor made it a question that decides whether the dataset stays; the
  critic withdrew it after the BOEM fact; the advocate calls it a weighing if refused, since interpolation beats the
  mean on log1p (8 of 9 folds). The pick of the framing is the curator's under SPLIT-1, but nothing in it is left to
  weigh: SPLIT-28 is read on the declared scale (MET-3, the count), and there neither LightGBM (R^2 -0.077) nor
  interpolation (RMSE better on 4 of 9 folds, deviance on 5 of 9, both within noise) beats the training mean, so that
  framing means `No`. It is one alternative of issue 1, not an issue of its own; no agent argues for it.

**Consistency**

* Followed: forest_fires (TP-2; the builder's "otherwise No", precedent check A, is dropped: the dataset stays under
  either metric); airfoil_self_noise (SPLIT-1 Cases: re-grouped when 91.5% of test runs had a close neighbour in
  training; here 95.3%); framingham_heart_study_fhs (PROV-14: NCEI's 7 extra survey days not added, noted);
  fremtpl2 and Andrej's call 3 of 2026-10-30 (`transect_km` an exposure feature); Andrej's rule 4 of 2026-10-30 (the
  `Two-Regime Zeros` tag stays); wadden (the moment of a map drawn from the whole archive; no RMSLE because the actor
  sums densities); noaa_afsc issue 1 (the species as a weighing, the CLEAN-8 sentence); the crms mediator (a regime
  is not argued from a score).
* Departed, with the fact: 5g_energy_consumption (Lennart, 2026-10-14, USE-9 direct): its gap-filling task was the
  source's own; here no source names one. wadden issue 3 (AI recommendation `rmse`): here the source names one
  count-likelihood criterion (a stand-in, where wadden's deviance would be context), and RMSE cannot separate a
  calibrated fit from a biased one or from the constant, where at wadden it put the Tweedie fit 4% ahead on 9 of 9
  folds.
* Set apart: cape_floristic_region_family_cover (fallback; its paper compares models on four criteria and its CRPSf
  cannot compare zero structures, so no unique original). pennsylvania issue 4 (RMSLE argued from the forester's
  stocking ladder, which this actor lacks). One flag for the family call: pennsylvania's source ranks models by AIC,
  also a likelihood; if the deviance is taken here as the stand-in for a likelihood criterion, read pennsylvania's
  origin the same way.
* No curator drift and no third exception. Outside this dataset (precedent checker): Dryad's version route answered
  302 for metro_manila_village_weekly_dengue on 2026-11-01, which bears on its 2nd Tier.

</details>

<details><summary>Claim audit</summary>

**Claim audit (claim-auditor, 2026-11-01): nantucket_sound_sea_duck_aerial_survey_counts**

**Verdict: ship after changes.** I tested 54 claims: 39 hold, 13 are refuted or partly refuted, 1 is a metric concern for the curator to weigh, and 1 is untested. The refutation that matters is a validity one (P4, SPLIT-1). The split note says a held-out segment's neighbours along its own transect are in training on the same day, "as for a map of the surveyed days drawn over the unflown squares". On the data that is false: the transects run north-south, so an unflown square on a survey day rarely has a flown neighbour on its own line that day. Those neighbours make up about 30% of the measured skill (R^2 0.25 -> 0.18). The other refutations are a metric-origin label (MET-11), a prediction-point sentence with no measurable effect (LEAK-10, weak), the Decision's own reason, which its own table contradicts, and wording.

Scripts and outputs are in the run folder (a1 to a11, rda_check.py). Every model is untuned LightGBM with the builder's settings (300 trees, learning rate 0.05, 31 leaves) on the definition's frame, with thread caps.

**Claims table**

| # | Claim | Source | Test | Result | Evidence | Rule |
|---|---|---|---|---|---|---|
| 1 | 7,751 segment-days of 30 surveys (13/10/7) over 454 of 504 segments; 7,369 segment-days not flown | task_summary.row; Rows bullet | counts on env.segs | holds | 7,751 rows; 13/10/7 dates; 454 segments flown; 15,120 - 7,751 = 7,369 | PROV-13 |
| 2 | Strip "about 180 m wide" | task_summary.row | paper; R/model_ltdu.R | holds | Sec. 2.1.2: each observer watched "a ca. 91 m-wide transect"; Fig. 4-6: "1.5 km x ca. 180 m transect"; `obs_window = length * 91.44/1000 * 2` | EV-2 |
| 3 | 57.1% zeros, maximum 3,000 | task_summary.predicted | counts | holds | 0.5708; 3,000 | - |
| 4 | "flocks of hundreds, up to 3,000, make most of the rest" | task_summary.predicted | distribution of the non-zero counts | refuted | non-zero median 7, p90 45; 3.6% of non-zero rows are 100 or more, and they hold 44.7% of the ducks: neither most rows nor most birds | EV-7 |
| 5 | The listed known features are the shipped inputs | task_summary.known | `feature_columns(container)` | holds | 20 features; `segment` is only the group column | - |
| 6 | A test segment stands for a part of the Sound never flown; "its neighbours 1.5 km away along the same transect, and the other segments flown on the same days, are in training, as for a map of the surveyed days drawn over the unflown squares" | task_summary.split; splits_comment; grouping.definition | same-day neighbour structure; drop only the same-day neighbours from training; alternative groupings (a2, a3, a9, a10) | **refuted** | Transects run north-south: a flown segment-day has its N-S neighbour flown that day 99.2% of the time, an unflown one 20.7% (the 50 never-flown segments about 16%). 95% of shipped test rows have a same-day training row within 1.5 km; 70% of real unflown segment-days have a flown one, and 43% for never-flown segments. Decisive test: hold out 5% of segments (40 draws) and drop only the test rows' same-day N-S neighbours (618 rows) from training: R^2 on log1p falls from 0.251 to 0.177 (-0.074, SE 0.007). Dropping the same-day E-W neighbours gives +0.002 (SE 0.003), and dropping 618 random rows -0.004 (SE 0.004). R^2 by grouping: by transect column 0.162 (SE 0.016); every third column held out, both neighbouring columns in training, 0.173; 4.5 km blocks 0.189; by grid row (control) 0.239; shipped 0.252 | SPLIT-1, USE-10 (Must) |
| 7 | Fit `direct`: "the rows, features and split mirror the use case" | fit; README | follows from 6 | refuted (split part) | as 6 | USE-1 |
| 8 | A map assumes a standard 1.5 km strip | fit_reason | R/create_new_data.R | holds | new data set `obs_window` to 1.5 x 91.44/1000 x 2 | - |
| 9 | Rebuilt from unscaled covariates; the authors' per-species file standardises every column over all rows | task_summary.changes; Covariates bullet | data_ltdu.Rda read with pyreadr | holds | 7,751 x 29; every continuous column has mean 0 and SD 1; env.segs is raw (SSTm 1.4-16.3 C) | PROV-13, LEAK-30 |
| 10 | Prediction-point quotes (Introduction "un-sampled areas or time periods", Figure 4 "10 evenly-spaced dates", Discussion "marine spatial planners must") | Prediction point bullet | paper XML | holds | all three found. Figure 4 is the occupancy map; the abundance map, Figure 6, has the same phrase; the planners sentence is in Sec. 4.2 | EV-2 |
| 11 | The source never forecasts a later winter (Sec. 2.5 quote) | Regime bullet | paper; create_new_data.R | holds | quote in Sec. 2.5; the text has no "forecast"; the prediction dates lie inside the surveyed winters | SPLIT-5 |
| 12 | Temporal probe: R^2 0.04 vs 0.025; Poisson deviance 67.4 vs 63.7; with the day as a feature R^2 -0.15 to -0.34 | Regime bullet | design_probe outputs | holds | 0.042 vs 0.025; 67.401 vs 63.714; -0.149 and -0.340 | TP-10 |
| 13 | "as a forecast the panel is decided by each segment's own past" | Regime bullet; splits_comment | same outputs, plus the declared metric | partly refuted | On log1p the segment's past explains R^2 0.025, so nothing forecasts the next winter. On Poisson deviance the past rate x km wins (63.7, constant 82.8, best model 67.4). TP-10 asks for the declared metric: RMSE on the count is 105.9 for the best model, 106.6 for the naive forecast and 107.4 for the constant, no clear win. Leg 1 fails on all three, so the conclusion holds and only the wording overstates | TP-10 |
| 14 | Grouped: R^2 0.25; day of the winter alone 0.15; position and strip length alone 0.04 | Regime bullet | rerun (a2); leak and design probes | holds | 0.252, 0.148, 0.043. About 0.07 of the 0.25 comes from row 6's neighbours | EV-8 |
| 15 | Long-tailed duck: 10 largest counts hold 84% of the squared deviation | Target bullet | counts | holds | 0.844 | - |
| 16 | Scoters pool SUSC, WWSC, BLSC, UNSC; "we pooled all scoter observations" | Target bullet | create_final_data.R; paper | holds | `scoters <- c("SUSC","WWSC","BLSC","UNSC")`; quote in Sec. 2.1.2 | - |
| 17 | One scoter raft of 70,000 "holds most of theirs" (10 largest: 98.6%) | Target bullet | counts | holds (for squared deviation) | the largest row holds 0.674 of the squared deviation (20% of the birds); the top 10 hold 0.986 | - |
| 18 | Eider: 75.1% zeros (Sec. 2.2 quote), counts up to 30,000, R^2 0.15 on held-out segments | Target bullet | counts; design_probe2 | holds | 0.751; 30,000; 0.150 against 0.264 for the long-tailed duck | - |
| 19 | "The long-tailed duck's counts are the least dominated by single rafts" | `_decisions` why | its own table, plus the top-1 share | **refuted** | the eider is less dominated on every measure: top 10 0.699 vs 0.844; top 1 0.175 vs 0.262; 5 vs 3 rows hold half the squared deviation | EV-7 |
| 20 | NCEI 0115356: 39,559 records, Aug 2002-Mar 2006; per-day ratio median 94% (33-100%), log r 0.986 (eider 0.987, scoters 0.990) | NCEI bullet | reran the builder's script | holds | reproduced exactly | PROV-3 |
| 21 | NCEI has 7 more winter survey days (2004/05: 2; 2005/06: 5) that the deposit lacks | NCEI bullet | NCEI dates | holds | 2005-03-22, 2005-04-05; 2005-12-12, 2006-01-13, 01-24, 02-09, 02-23. 2005-12-12 holds 19,924 in-strip long-tailed ducks, over twice the deposit's largest day (8,087) | PROV-6 |
| 22 | A zero is a flown strip without a long-tailed duck (Sec. 2.2 and 2.1.2 quotes) | Zero bullet | quotes; zero pattern | holds | quotes found. Zeros are 84.7% of strips under 0.3 km and 54.5% of strips of 1.4 km or more. Only 3 early- or late-season days are at least 94% zeros, and NCEI agrees on them (2003-12-05: 60 and 60). No count falls on an unflown segment-day | USE-5 |
| 23 | Rows built as the authors' model data | Rows bullet | R/model_ltdu.R; data_ltdu.Rda | holds | `subset(env.segs, length > 0)`, then merge and `ifelse(is.na(count), 0, count)`; data_ltdu has 7,751 rows and the same mean count (10.07) | PROV-13 |
| 24 | 50 segments never flown | Rows bullet | coverage | holds | 50 segments are flown on none of the 30 dates. The authors' comment says "never surveyed (n = 47)", probably over their whole survey history | - |
| 25 | xkm and ykm are exact copies of the coordinates; the day takes 28 values over 30 dates; obs_window = 2 x 91.44 m x length | Dropped bullet | data; R | holds | maximum absolute difference 0; 28 distinct days | CLEAN |
| 26 | transect_km 0.002-3.18 km, 353 rows under 0.3 km; "above 1.5 where a transect crossed the segment twice" | transect_km bullet | lengths | partly refuted | the range and the 353 hold. Of the 6,062 rows above 1.5 km, 5,968 are between 1.5 and 1.6 km, single crossings; 94 rows are above 1.6 km and 56 above 2 km | EV-7 |
| 27 | The count grows with the strip length | transect_km bullet | Spearman; zero shares | holds | rho 0.108; zeros 84.7% vs 54.5% | - |
| 28 | sst_month_relative_c = the month's SST minus its mean over the 504 segments | SSTrel bullet | recomputed | holds | maximum absolute difference 2e-15 | LEAK-30 |
| 29 | SSTw covers November-March, NAOw December-March | Note bullet | Table 1; R | holds | Table 1; `mo %in% c(11:12, 1:3)` | - |
| 30 | NAO has one value per winter (-0.09, 0.38, -0.87) | Note bullet | NAO.csv | holds | NAO_PC 2003/04 -0.09, 2004/05 0.38, 2005/06 -0.87 | - |
| 31 | Chlorophyll-a and CDOM are "all known at the prediction point, after the winter" | Note bullet | Table 1 period; score with and without them (a6) | refuted, no measurable effect | Table 1: geometric means from July 2002 "to March 2006", so for 2003/04 and 2004/05 (5,909 rows) they include later winters. Without both, R^2 changes by -0.001 (SE 0.003) | USE-3, LEAK-10 (weak) |
| 32 | (implied) bottom_temp_summer_c is known before the winter | - | create_final_data.R | holds | May-Oct bottom temperature of the year the winter starts, matched on `winter` | LEAK-10 |
| 33 | Metric note: 1 or 2 of about 2,600 test rows hold half the squared deviation; mean 64.9, log1p model 64.7, Poisson model 64.3; R^2 on the count 0.005 and 0.023; better on 7 and 9 of 9 splits; log1p R^2 0.25, Spearman 0.49 | Metric note bullet | scorer per fold (a1); metric_probe | holds | 1-2 rows on all 9 folds, the top row 42-54%; the scorer gives the constant mean 64.895 | MET-2 |
| 34 | Metric origin: fallback, "the source defines no metric" | `metric`; README Metric block | paper Sec. 2.3.2 against MET-5 | **refuted** | Sec. 2.3.2: out-of-bag "empirical risk measured by the negative log-likelihood ... the optimal stopping iteration is the iteration with the lowest average empirical risk". That is the criterion the source tunes by ("ranks, tunes or selects", MET-5). It cannot be computed from a point prediction, so MET-11 calls the declared metric a stand-in that names this original | MET-5, MET-11 (Must) |
| 35 | The source validates "only in sample, by a pseudo R2" | metric reason | paper; R scripts | holds, incomplete | the source also compares predicted and observed total abundance per survey (Sec. 3.3, Figure 8; R/compare_predicted_vs_counted.R), also in sample, and the reason leaves it out | MET-1, MET-11 |
| 36 | The deposit's README defines no metric | metric reason | README | holds | none | - |
| 37 | The metric is computable per row on every fold | (MET-2) | scorer on dummy predictions per fold | holds | 9 folds of 2,397-2,725 rows and 151-152 segments, no overlap; the constant scores 40.2-94.7 by fold | MET-2 |
| 38 | (implied) RMSE on the count scores the decision | (MET-1) | resolution of each metric on the shipped folds (a11) | concern (weighing) | RMSE: best model -1.0% of the constant (t -4.0), log1p model -0.2%. Poisson deviance: -12.4% (t -6.5), and it ranks the log1p model below the constant (+10.4%). Per held-out segment no model beats the mean on squared error (-0.7%, 4 of 9; one segment holds 54%). RMSE and Poisson deviance both score the mean, which is what the maps show ("expected number of sea ducks", Figure 6); rmsle would score E[log1p y], another quantity | MET-1, MET-10 |
| 39 | Target shipped as log1p, scored on the count | metric | spec | holds | `target_transform='log1p'`; the source's scale is the count | MET-3 |
| 40 | CC0; year 2019 | metadata | Zenodo and Dryad metadata | holds | cc-zero and CC0-1.0, published 2019-02-15. NCEI published the raw sightings on 2014-10-07, but not the segment table with effort and covariates | PROV-9 |
| 41 | The Zenodo mirror has the same DOI and files; Dryad refuses automated downloads; raw checksums | download_description | metadata; curl; sha256 | holds | same DOI, md5 6c4e3288... matches; Dryad API 401, Zenodo 200; all three sha256 match | PROV |
| 42 | "the other three files are fitted models" | download_description | Dryad file list | refuted (minor) | the other three are the README (4,617 bytes), Results_ltdu.zip and Results_scot.zip | EV-7 |
| 43 | Coordinates are UTM 19N (column names; the builder says NAD83) | builder claims | NCEI lat/lon projected to UTM 19N (a7) | holds; datum untested | 97.4% of NCEI long-tailed ducks on deposit days land in a segment the deposit lists with them that day (27.1% with the grid shifted 1.5 km). NAD83 against WGS84 (about 1 m) cannot be told apart here | PROV-3 |
| 44 | The development was withdrawn (Sec. 2.1.1) | builder; record | paper | holds | quote found in 2.1.1 | - |
| 45 | (implied) No row is a copy across the split | - | duplicate feature vectors | holds | 0 | LEAK-16 |
| 46 | The `task_target_value_dominant` warning is a real zero, not a cap or placeholder | README warning | as 22 | holds | as 22 | - |
| 47 | Screening facts: 504 segments of 2.25 km2, 30 surveys, at most 15,120 rows, 4.52 GB, CC0 | record screening | paper; Dryad | holds | storageSize 4,517,373,737 | - |
| 48 | Record: regime temporal, `required_split` Temporal, tag Non-IID (Temporal), "fit direct for predicting the segment counts of later surveys" | record screening and frontmatter | build measurement (12-13) | refuted (superseded) | TP-10 leg 1 fails, and the definition is grouped, so the record and the definition disagree | SPLIT-3, USE-10, EV-2 |
| 49 | Record: "no ducks seen in the 91 m strip" | record CC block | paper | refuted (minor) | 91 m is one observer's side; the strip is ca. 180 m | EV-7 |
| 50 | Record: models are "crucial for the siting" | record screening | paper | refuted (minor) | the paper says "Understanding the winter habitat use and distribution of sea ducks ... is crucial" | EV-2 |
| 51 | Record: "R2 on a fixed test fold ranks models as RMSE does" | record screening (metric) | R/pseudoR2.R | refuted (minor) | the source's R^2 is Nagelkerke's pseudo-R^2 on the hurdle likelihood, and it does not rank models as RMSE does | MET-11 |
| 52 | Assessment of 2026-10-30: the policy question is settled (curator quote) | record | triage summary | holds | curation/inputs/two_regime_zero_triage_summary.md, line 258 | - |
| 53 | Record quotes (Sec. 4.2 siting; "Our predictive approach ... five distinct methodological steps") | record | paper | holds | both found | - |
| 54 | (builder) The signal stands with tuned methods | builder report | - | untested | no tuned results | TP-1 |

**Refuted and untested claims, ranked (validity first, Must first)**

1. **The split does not mirror the gaps it claims to stand for (row 6, also row 7). P4, SPLIT-1 and USE-10, Must.**
   * What it changes: the shipped score includes about 0.07 R^2 (about 30% of 0.25) from the two same-day neighbours on the test segment's own transect. An unflown square has such a neighbour 21% of the time, and a never-flown segment about 16%. The task as written (never-flown squares) is overrated, and `fit="direct"` is not earned yet.
   * The two framings give opposite answers, so the curator has to pick one:
     * Never-flown squares, as written now (1,500 segment-days): group on the transect column, a key built exactly from the easting (SPLIT-24). R^2 0.162; 4.5 km blocks give 0.189.
     * Each survey's unflown squares (5,869 of the 7,369 unflown segment-days are segments flown on other days, whose history is legitimate under USE-10): group on (transect column, survey day). R^2 0.296.
   * Mildest remedy: re-split on the key of the chosen framing. Then rewrite task_summary.split, splits_comment, grouping.definition and fit_reason. Leaving the segment grouping in place mirrors neither framing.
2. **The record contradicts the definition (row 48). P4, SPLIT-3.** It still says Temporal (`required_split`, tag, screening "later surveys"). Remedy: update the record once the curator settles the regime (builder issue 1).
3. **Chlorophyll-a and CDOM are not "known after the winter" for 2003/04 and 2004/05 (row 31). USE-3 and LEAK-10, weak.** They are a static 2002-2006 average with no measurable signal (-0.001 R^2). Remedy: reword them as a habitat average known after March 2006; no data change.
4. **Metric origin mislabelled (row 34; rows 35 and 38 are context). P6, MET-11 Must and MET-5.** The source tunes by the out-of-bag negative log-likelihood of its hurdle model, so the declared metric is a stand-in, not a fallback.
   * Mildest remedy: `Metric.stand_in`, naming that original and the Figure 8 comparison.
   * The choice of stand-in is a weighing call for the curator. RMSE on the count needs no code but separates models by 1% of the constant. Mean Poisson deviance is a count likelihood, closer to the original; it separates models by 12% and scores the same expected abundance. It needs adding to `metrics.py` with a floor for zero predictions (MET-12, MET-13).
   * Not rmsle: it scores E[log1p y], not the expected abundance the source maps (MET-1).
5. **The TP-10 wording overstates (row 13). TP-10.** The segment's past explains R^2 0.025 on log1p; leg 1 fails under every metric, including the declared RMSE (105.9 vs 106.6). Remedy: reword to "nothing forecasts the next winter clearly; the segment's past rate wins on Poisson deviance", and cite the declared metric.
6. **The Decision's reason (row 19). EV-7, quality.** Remedy: rewrite it. Choose the long-tailed duck over the eider for its signal on held-out segments (R^2 0.26 vs 0.15) and fewer zeros (57% vs 75%), and over the scoters because one raft holds 67% of their squared deviation.
7. **Wording (rows 4, 26, 42, 49, 50, 51). Quality.**
   * Row 4: "most non-zero strips hold a few ducks (median 7); flocks of 100 or more, 4% of them, hold 45% of the ducks, up to 3,000".
   * Row 26: "above 2 km (56 rows) where a transect crossed the segment twice".
   * Row 42: the other files are a README and two fitted-model archives.
   * Record, rows 49-51: the strip is 180 m; "understanding the distribution is crucial"; the source's R^2 is a likelihood pseudo-R^2.
8. **Untested.**
   * Tuned results (row 54, TP-1): `tuned_results.py` on the shipped splits would show whether tuned methods separate under RMSE on the count at all, which bears on item 4.
   * The NAD83 datum (row 43) cannot be told from WGS84 at this resolution; immaterial.

Notes that change nothing: NCEI's 7 extra winter days include the largest long-tailed duck day of the archive (2005-12-12, 19,924 in the strip). The authors' code comment counts 47 never-surveyed segments where the deposit's 30 dates give 50.

</details>

<details><summary>Column audit</summary>

**Column auditor (AI, 2026-11-01): nantucket_sound_sea_duck_aerial_survey_counts**

**Verdict: ship after wording changes.** No column leaks the target and none needs to be dropped. The written prediction point says "after a winter's surveys", but four static covariates and the training rows are only known after the whole three-winter programme. The target counts ducks on the water: the authors left out flying birds, which the definition never says. `depth_m` holds negative elevations.

```text
Validity: USE-3 / LEAK-1 wording gap (the prediction point is after the programme, not after one winter; reword, no data change);
          USE-5 holds (ducks on the water, the quantity a habitat map wants), undocumented (reword; one question on 2005/06);
          LEAK-10 holds for every column; LEAK-33 holds (segment is the group, not a feature); LEAK-29/30 hold (unscaled rebuild verified).
Quality:  `depth_m` name against its sign (rename or negate); two claim corrections (transect_km "above 1.5", known list).
```

Evidence and scripts are in the run folder (`checks1.py`, `checks2.py`, `checks3.py`, `ncei_grid.py`, `obspoly.py`). The frame was loaded through `dataset_io.from_definition`: 7,751 rows x 22 columns, no missing values, no duplicate feature rows, and 20 features (the group column excluded).

**Column table**

| column | meaning (codebook: Table 1, R/create_final_data.R) | known at prediction? | dtype and cleaning | verdict | rule |
|---|---|---|---|---|---|
| `segment` | Grid cell 1-504 of `seg_poly` (source `seg`); 454 flown, 1-30 rows each (median 19) | yes (an id) | category, cast from int to string; the group column; README counts 20 features, so it is not a model input | fine | LEAK-33, CLEAN-3 |
| `utm19n_easting_m` | Easting of the segment centre. NAD83 UTM 19N is confirmed by `GIS/Ancillary/seg_poly.prj`. 1,500 m grid, one value per segment, 454 distinct positions | yes, static | float64. `xkm` is an exact copy, dropped (max difference 0.0) | fine | CLEAN-5 |
| `utm19n_northing_m` | Northing of the segment centre, same grid | yes, static | float64. `ykm` is an exact copy, dropped (0.0) | fine | CLEAN-5 |
| `transect_km` | Length of track flown inside the segment that day, summed over crossings (`seg_xsect.dbf` by seg x start_dt x trans_id). The authors' `obs_window` is this length x 0.18288 km | Yes, after the flight. For a never-flown square it is a design value: the source's maps set 1.5 km (`create_new_data.R`). Not driven by the outcome: on strips of 1.4-1.6, 1.6-2.5 and 2.5-3.5 km the density is 6.9, 6.7 and 5.7 ducks/km, so double crossings are not the plane circling flocks | float64, 0.0018-3.18 km, nothing impossible. Varies within a segment (median within-segment SD 0.33 km). The 353 rows below 0.3 km are kept as the authors kept them: they have 8x the density of full strips (53.6 against 6.9 ducks/km), because single flocks fall on clipped corners (2,000 ducks at 0.209 km, segment 136) | fine (an exposure, the family's call); claim wording in issue 4 | USE-6, CLEAN-11 |
| `winter` | Study winter (June-May year), labels 2003/04 to 2005/06 | yes | category, 3 levels (the source used dummies y2004 and y2005) | fine | CLEAN-14 |
| `day_of_winter` | Days after 31 December (`time`), -64 to 108. Together with `winter` it identifies the survey date (28 values over 30 dates; verified against `date`) | yes | int64, numeric time index | Fine. Its R^2 of 0.148 alone is the day's Sound-wide level, learned from the other segments flown that day. The use case grants this ("the counts elsewhere") | LEAK-10 holds |
| `sst_winter_mean_c` | FVCOM sea surface temperature, mean of November-March of that winter, per segment (one value per segment and winter) | After the winter: it includes months after the survey day | float64 | fine under an after-season point; dropping it and `nao_winter` costs 0.252 to 0.249 | USE-3 |
| `sst_month_c` | FVCOM monthly mean SST of the survey's calendar month at the segment | after the month | float64, 1.4-16.3 C (16 C in the October survey) | fine | |
| `sst_month_relative_c` | `sst_month_c` minus its mean over the 504 grid segments of that month. Verified to 2e-15; the mean over flown rows only is off by 0.064 | Yes. It is a statistic of the full FVCOM field over the fixed study area (which includes the 50 never-flown squares), the same in deployment. It uses no labels | float64 | fine: not our statistic over rows (LEAK-29), not a scaling over dataset rows (LEAK-30) | LEAK-29, LEAK-30 |
| `bottom_temp_summer_c` | FVCOM bottom temperature, May-October of the summer before the winter (`bTemp_2003` matched to winter 2003/04) | yes, before the winter | float64, one value per segment and winter | fine | |
| `chlorophyll_a_mg_m3` | MODIS Aqua geometric mean of the monthly composites from July 2002 to March 2006; one value per segment | Only after March 2006, not after the 2003/04 or 2004/05 winter. It is a static climatology and cannot carry one segment-day's count | float64, 3.6-9.9 | fine under an after-programme point; the claim "known after the winter" is wrong (issue 1) | USE-3, LEAK-10 |
| `cdom_absorbance` | MODIS CDOM absorbance, geometric mean July 2002-March 2006 (Table 1: unitless); static | as `chlorophyll_a_mg_m3` | float64, 2.9-5.1 | as above | USE-3 |
| `sediment_grain_size_phi` | Mean grain size on the phi scale (-log2 mm; Poti et al. 2012); higher means finer | yes, static | float64, -0.9 to 4.5 | fine | |
| `depth_m` | Bathymetry relative to mean high water. Table 1: "lower values = deeper water" | yes, static | float64, **-21.4 to -1.5**: the values are elevations, the name says depth | cleaning problem (issue 3) | CLEAN-1, recipe step 2 |
| `distance_to_land_km` | Distance to the nearest point of zero depth | yes, static | float64, 0.28-15.5 | fine | |
| `seafloor_surface_area_ratio` | Seafloor surface area / planimetric area (Jenness 2004) | yes, static | float64, 1.000001-1.0031 (at least 1, as it must be) | fine | |
| `tidal_velocity_bottom_mean_m_s` | FVCOM epibenthic tidal velocity, mean over 2003-2005; static | After 2005, so not after the 2003/04 or 2004/05 winter. Static | float64 | fine under an after-programme point (issue 1) | USE-3 |
| `tidal_velocity_sd_m_s` | SD of the same velocity, 2003-2005; static | as above | float64 | as above | USE-3 |
| `stratification_log10` | log10(-depth / surface tidal mean^3) (Simpson-Hunter), s^3/m^2; static | as above (surface tide 2003-2005) | float64. Spearman 0.88 with the bottom tidal mean; not a copy | fine | CLEAN-5 holds |
| `nao_winter` | Hurrell PC-based December-March NAO index. `NAO.csv` gives -0.09, 0.38, -0.87 for 2003/04 to 2005/06, which matches | after March of that winter | float64. A 1:1 recoding of `winter` (identical single-feature R^2 0.0038); both are Table 1 covariates; already noted | fine (noted) | CLEAN-5 does not apply (not an exact copy; a climate index with its own meaning) |
| `ferry_route_within_1km` | Whether a ferry route (about 16 runs a day) passed within 1 km of the segment | yes, static | 0/1 mapped to no/yes, category; raw values only 0 and 1 | fine | CLEAN-14 |
| `log1p_long_tailed_duck_count` (target) | log1p of the long-tailed ducks counted **on the water** in the two 91 m strips of a flown segment-day. A flown segment-day without a record is 0 | Target | float64, log1p (CLEAN-16). 57.1% zeros, max 3,000, the 10 largest hold 84.4% of the squared deviation (all verified). Flying birds are excluded upstream (issue 2) | fine as a quantity; meaning undocumented (issue 2) | USE-5 |

Dropped or not built, all correctly: `xkm` and `ykm` (exact copies); `date` (recoverable from `winter` + `day_of_winter`; not a Table 1 covariate); `obs_window` (a linear copy of `transect_km`); obs `group`.

**Problems, ranked by principles.md**

1. **USE-3 / LEAK-1 (P3, P4; Must, fixed by rewording): the prediction point is after the programme, not after one winter.**
   - What the definition says now:
     - `task_summary.use_case`: "After a winter of aerial surveys".
     - The first bullet: "Known then are the covariates of the source's Table 1, all of them observed or modelled for the surveyed winter".
     - The Note bullet: chlorophyll and CDOM "all known at the prediction point, after the winter".
   - Evidence that these are known only later:
     - `chlorophyll_a_mg_m3` and `cdom_absorbance` are geometric means over July 2002 to March 2006, so two years after the 2003/04 winter.
     - `tidal_velocity_*` and `stratification_log10` are 2003-2005 FVCOM means.
     - The grouped split trains a 2003/04 test segment on 2004/05 and 2005/06 rows of other segments.
     - The source predicts all 504 segments on 10 dates per winter only after fitting all three winters (`R/create_new_data.R`, Figure 4).
   - Strength: no signal leaks. These are static fields that do not depend on the ducks. Under "after one winter" they would be weak LEAK-10 attributes looked up after the outcome.
   - Mildest remedy: reword the prediction point in `use_case`, the first bullet and the Note bullet to "after the three winters of surveys (spring 2006), the analyst maps each survey day over the unflown squares". This is where the source drew its maps, and it makes every column known.
   - Alternative if the curator wants a per-winter map: rebuild chlorophyll and CDOM to date from `GIS/Environmental/Raw/chla0206.csv` and `cdom0206.csv` (monthly composites from 2002-07 on; our construction, PROV-11) and train only on that winter and earlier. That is a different task, and I do not recommend it.
   - This also covers the builder's draft issue 2: dropping `sst_winter_mean_c` and `nao_winter` would not suffice for an in-season map.

2. **USE-5 (P3; holds, undocumented): the target counts ducks on the water; the authors left out flying birds.**
   - Evidence (measured):
     - Over all 30 days, the deposit equals NCEI 0115356's in-strip count minus the birds marked TRAVELING on 3,609 of the 3,612 segment-days with long-tailed ducks in either source. NCEI sightings were put on segments by position. The 3 exceptions are the two 2005/06 flocks below and segment 501 on 2004-02-12 (117 against 127).
     - NCEI holds long-tailed ducks on 285 flown segment-days where the deposit has 0; once flying birds are removed, on 1.
     - On the 2003/04 and 2004/05 days, which carry behaviour, the daily ratio deposit / NCEI-without-flying is 1.000 on every day but one (0.996).
     - The bullet's "median 94% (33% to 100%)" is therefore this exclusion, not an unexplained shortfall.
     - The authors' own `GIS/Survey/obs_poly.dbf` has no behaviour field, so the filter was applied before it.
   - What cannot be checked:
     - 2005/06: NCEI carries no behaviour for 1,282 of 1,298 records. There the deposit equals NCEI's full total on 4 of 6 days. It lacks one flock each on the other two: 711 on segment 283 on 2006-02-08 (deposit 1), and 800 on segment 329 on 2006-03-06 (deposit 0, the 33% day). Both flocks are also absent from `obs_poly.dbf`, which fits flying flocks being removed.
     - So whether flying birds were removed throughout 2005/06 is open. If they were not, the effect would be about 5% of the ducks, judging from the earlier winters.
   - Mildest remedy: in `predicted` and bullet 4, say "long-tailed ducks on the water in the strip (the authors left out flying birds; the deposit equals NCEI's in-strip count without birds marked flying on 99.9% of segment-days of 2003/04-2004/05)". Keep the 2005/06 point as a sentence.
   - On-water ducks are the right quantity for a habitat and siting map, so nothing changes in the data.

3. **CLEAN-1 / recipe step 2 (P7; quality, cheap fix): `depth_m` holds elevations.**
   - Evidence: the values run from -21.4 to -1.5 m (Table 1: "lower values = deeper water"), and the source builds `strat` from `-depth`.
   - The name tells a reader "deeper = larger". Models do not care, but the README does.
   - Mildest remedy: rename to `bathymetry_m` or `seabed_elevation_m` and keep the values; or negate them (a per-row transform) and keep `depth_m`.

4. **Claim corrections (writing; trivial).**
   - Bullet on `transect_km`: "above 1.5 where a transect crossed the segment twice" is wrong as written. 6,062 rows exceed 1.5 km, almost all single oblique crossings of 1.500-1.51 km; 94 rows exceed 1.6 km and 43 exceed 2.5 km. Write "above about 1.6 km (94 rows)".
   - `task_summary.known` does not mention the winter (a categorical feature). Add "the winter".

**Claims checked and found to hold**
- `xkm` and `ykm` are exact copies.
- The date follows from the winter and the day; the day takes 28 values over the 30 dates.
- `sst_month_relative_c` is the month's SST minus the 504-segment mean.
- NAO has one value per winter, matching Hurrell's PC-based December-March index.
- The coordinates are NAD83 UTM 19N.
- 7,751 rows = 15,120 - 7,369; 13, 10 and 7 surveys per winter.
- 0.002-3.18 km and 353 rows below 0.3 km.
- 57.1% zeros, max 3,000, 84% of the squared deviation in the 10 largest counts.
- The covariates are unscaled in `env.segs` (PROV-13 / LEAK-30 claim).
- The zero fill and the `length > 0` subset follow `R/model_ltdu.R`.
- `obs_window` = 2 x 91.44 m x the length.
- The source maps use a standard 1.5 km strip (`create_new_data.R`), which backs `fit_reason`.

</details>

<details><summary>Split audit</summary>

**Split auditor: nantucket_sound_sea_duck_aerial_survey_counts (2026-11-01)**

**Verdict: right with notes, on one condition.** For the use case the definition declares (a square never flown, on a survey day, with the other squares flown that day known), grouping by segment is the right regime and `segment` is a true id from the source. The condition is that survey-day framing. Almost all of the score comes from the same survey day's counts, which reach the model through training rows. The source's maps, which the definition cites as its support, predict on dates with no survey, and there this task has no signal. If the curator takes the maps as the use case, the split is wrong and the dataset goes (issue 1). Separately, the test squares are mostly interior squares, while every square that was really never flown lies on the border of the grid (issue 2).

**What I checked and how**

- Mechanics (pass): rebuilt with `dataset_io.load(..., built=False)`. 9 splits (3 repeats x 3 folds), 151-152 test segments and 2,397-2,725 test rows per fold. No segment is on both sides, and every row is tested once per repeat. `segment` is the group column, not a feature (20 features).
- Group id (pass, SPLIT-24): `seg` is the cell of the source's own 504-cell grid in `env.segs`. It is neither a cluster nor a hash.
- Hidden groups (pass): I ran `hidden_groups.py --include-grouped`, which treats the task as IID. Its hits are per-segment covariates: `chlorophyll_a_mg_m3` (454 values), `distance_to_land_km` (450) and `tidal_velocity_bottom_mean_m_s` (454), with gaps of +0.063 to +0.072. These are the segment itself, which the split already holds out. The composite key (all columns but strip length and day) has a gap of +0.014, and near copies -0.013. There is no other entity apart from the survey date, which crosses the split on purpose (issue 1).
- Alternative splits: untuned LightGBM (300 trees, learning rate 0.05) and a random forest (300 trees, minimum leaf 5), both on the 20 shipped features with the log1p target. Each alternative uses 3 repeats x 3 folds with groups assigned to folds at random. The shipped row uses the 9 shipped splits. The temporal row is the builder's (design_probe2). Scripts and outputs are in the run folder (s4_splits.csv, s3/s5/s6/s7 *.txt).

| The test stands for | Split | LightGBM R² log1p | RF | Spearman (LGB) |
|---|---|---|---|---|
| known square, surveyed day | IID by row | 0.324 | 0.315 | 0.535 |
| **new square, surveyed day (shipped)** | **grouped by segment** | **0.249** | **0.251** | **0.492** |
| new square, surveyed day | blocks of 2x2 segments (3 km) | 0.200 | 0.219 | 0.453 |
| new square, surveyed day | blocks of 3x3 (4.5 km) | 0.189 | 0.200 | 0.450 |
| new square, surveyed day | blocks of 4x4 (6 km) | 0.165 | 0.178 | 0.445 |
| new square, surveyed day | whole transect columns | 0.155 | 0.172 | 0.430 |
| known square, date without its counts | grouped by survey date | 0.044 (the square's own mean on its other dates: 0.039) | 0.040 | 0.294 |
| new square, date without its counts | segment x date double hold-out | -0.077 (training mean: -0.007) | -0.038 | 0.187 |
| next winter | builder: train on 2003/04-2004/05, test on 3 parts of 2005/06 | best 0.042 (the square's past mean: 0.025) | | |

**Problems, ranked**

**1. The day's other counts make the score, and the source's maps do not have them (P3/P4; USE-3, SPLIT-23, Must). A question for the curator, and it decides whether the dataset stays.**
Evidence. `winter` plus `day_of_winter` identify the survey date exactly. In every shipped fold, about two thirds of that day's flown squares are in training.
- The day's training mean alone gives R² 0.146 of the 0.249. The covariates and the strip length without the day give 0.031 (Spearman 0.23).
- Withholding the day's rows (new square, date not in training) drops LightGBM to R² -0.077 and the random forest to -0.038, below the training mean (-0.007); Spearman falls to 0.19.
- A size control rules out the smaller training side: segment hold-out with training cut to 4/9 of the rows, the double hold-out's size, still scores 0.222. The drop comes from the missing day, not from having fewer rows.
- On a known square at a date with no survey, the model reaches 0.044, the same as the square's own mean on its other dates (0.039).
- In sample, the date means explain 0.155 of the log1p variance, the segment means 0.189, and both together 0.338.

So the learnable task is filling in a surveyed day from that day's other counts. The habitat covariates add about 0.1 on top of the day's level and almost nothing on their own.

The definition says so openly: "for each survey day", and the split text says "the other segments of the same days are in training". The split therefore matches the declared use case. But the support it cites is the source's maps, and Fig. 4 is "predicted on 10 evenly-spaced dates from 15 November through 1 April in each winter". Those dates are not survey days, and what planners act on is that figure's median and spread over dates. The Introduction quote also covers "un-sampled areas or time periods". No source sentence names an actor who fills in one survey day.

Rule. SPLIT-23 (Must) says the cited use case decides what is known about a new group, and USE-3 (Must) fixes the prediction point. If the use case is the source's maps, the survey date is an entity new rows would not have, and it carries the label (date means 0.155). That is SPLIT-29, so the split is wrong. The splits that fit that use case (by date, or segment x date) leave R² 0.04 at best and are at or below the mean for a new square. SPLIT-28 (Must) then says the dataset goes, which fits the CC "if it turns out a bad task, then we drop it to no".

Mildest remedy, if the survey-day framing is kept:
- name an actor who needs a surveyed day filled in. One example, which no source sentence states: a Sound-wide total per survey for a population index.
- in `grouping.definition`, either drop Fig. 4 as support or say its dates are not survey days.
- add the double hold-out number to `curation_comments`, so readers see that the score rests on same-day counts.

Otherwise the verdict is `No`.

**2. The test squares are interior, but every never-flown square is on the border (P4; SPLIT-1, Must, here a matter of degree).**
Evidence.
- All 50 never-flown squares lie on the outer edge of the 24 x 24 grid: the west column, the two east columns, and the north and south rows. They are 3.6 km from land against 7.3 km for flown squares, 9.6 m deep against 11.4 m, and most have 5 grid neighbours. By contrast, 350 of the 454 flown squares have 8 flown neighbours.
- On a survey day, 95.3% of shipped test rows have a training square flown that same day 1.5 km away (median 1.50 km, 75th percentile 1.50 km). The never-flown squares have such a square on 43.1% of their 30 survey days (median 2.12 km, 75th percentile 3.0 km). Blocks of 3x3 come closest to that: 52.8%, median 1.5 km, 75th percentile 3.0 km.
- On the 104 flown border squares (1,096 rows, 4.1 km from land), the shipped split's out-of-fold R² is 0.17 / 0.20 / 0.13 per repeat, against 0.24 / 0.27 / 0.25 on interior squares. Held out with only interior squares in training, they score 0.103.
- Spatial blocks lower the score step by step: 0.20, 0.19, 0.17.

The paper explains why: transects run north-south about 2.5 km apart (Sec. 2.1.2), so a held-out square's neighbours along the same flight line, flown minutes apart, are in training.

Rule. Under SPLIT-1 the test must stand for the application. "A test segment is a part of the Sound the plane never flew" (`splits_comment`, `task_summary.split`) overstates this. Two siblings in this run, not yet reviewed by a curator, did it differently. `wadden_sea_sibes_macoma_abundance` measured its test distance against the map's and wrote it down. `cape_floristic_region_family_cover` chose a grid cell whose test distance matches the map's.

Mildest remedy: add a note in `splits_comment` with these distances and the border-square score, saying the score is optimistic for the never-flown squares by about 0.05-0.08 R² on log1p. The stronger option, a curator call because no rule names spatial blocks: group on 3x3 blocks of the source's grid. These are built exactly from the coordinates, not by similarity (SPLIT-24), match the never-flown squares' distances, and score 0.19-0.20.

**3. Grouped replaces the screening's temporal regime. The reason holds, but its wording overstates (P4; SPLIT-3, USE-10, Must). The record needs updating.**
Evidence. The record still has `required_split: Temporal (NON-IID)` and the tag `Non-IID (Temporal)`, and the CC `Yes` was given on that framing. The builder's numbers in `curation_comments` match the probe outputs:
- next winter: best R² 0.042 against 0.025 for the square's past mean;
- Poisson deviance 67.4 against 63.7;
- -0.149 and -0.340 with the day as a feature.

The expanding-by-date design gives the same answer: RMSLE 1.347 for LightGBM against 1.260 for the square's mean, and Poisson deviance 44.3 against 43.6. As a forecast, the task fails TP-10 leg 1 and falls under SEL-10, so temporal is no option. One side note: the next-winter design trains every window on the first two winters only, with no expanding side (SPLIT-11), but the expanding design agrees with it.

Wording. "As a forecast the counts are decided by each segment's own past" (`splits_comment`, `curation_comments`) overstates. The square's own past reaches only R² 0.025, so neither it nor the covariates predict a later winter.

Rule. Under SPLIT-3 and USE-10, one regime is chosen, from the use case. The definition gives a use-case reason: the source maps winters it surveyed and never forecasts. It does not rest on temporal's lack of signal, which is right (P4 over P6).

Remedy:
- the curator confirms the grouped regime;
- the record changes to `required_split: Grouped (NON-IID)` and the tag `Non-IID (Grouped)` (records.md);
- the sentence becomes "neither the covariates nor the segment's own past predict a later winter (R² 0.04 and 0.025)".

**4. New square rather than known square (USE-10, Must to decide; the weighed factor "an entity seen before" points the other way). A note.**
Evidence. Of the source grid's 7,369 segment-days that were not flown, 5,869 (80%) belong to squares flown on other days, whose own counts a gap-filler would use. The remaining 1,500 (20%) belong to the 50 never-flown border squares. A known square on a surveyed day (IID by row) scores R² 0.324, against 0.249 shipped. The declared question covers only never-flown squares, so the split matches it. The stricter choice is fine, but the definition should say in one sentence why it chose the cold start over the more common gap.
Remedy: that one sentence, or the curator's call.

**Smaller points (no change needed)**

- `transect_km` on test rows is the observed strip of a square that was flown. A never-flown square has no strip, and a map uses 1.5 km (`fit_reason` says so). It is weak on its own (leak probe, single feature: R² -0.018).
- Interaction with the metric (the metric auditor's point): under RMSE on the count, a whole segment's rafts land in one fold. The training mean's RMSE on the same rows ranges from 60.8 to 65.0 across my segment, block and column designs, depending only on which squares fall where.

**Claims checked**

- `grouping.definition`:
  - "454 of its 504 segments were flown, 1 to 30 times; each survey flew about 270": pass (median 274.5 per survey, range 109-294).
  - The Fig. 4 quote is accurate, but those dates are not survey days (issue 1).
  - "holding segments out is stricter": true against the source's in-sample fit, but optimistic against the never-flown squares (issue 2).
- `splits_comment`:
  - "neighbours 1.5 km away along the same transect ... in training": pass (95.3%).
  - "decided by each segment's own past": overstated (issue 3).
- `curation_comments`, regime bullet:
  - shipped LightGBM 0.25: pass (0.249; random forest 0.251).
  - "0.04 from the position and the strip length alone": pass (covariates plus strip 0.031).
  - temporal numbers: pass, read from the builder's probe outputs.
- Builder's group probe, IID 0.332 against grouped 0.237: consistent (0.324 against 0.249, with other seeds and parameters).
- Cannot verify: tuned results on any of these splits (TP-1).

</details>

<details><summary>Domain practitioner</summary>

**Domain practitioner (the actor: a federal or state wildlife biologist who turns winter sea-duck surveys into the distribution maps used to site offshore wind lease areas or protected areas: BOEM, USFWS, Massachusetts CZM), 2026-11-01**

**Verdict.** Fit **approximate**; the definition says `direct`. The rows, the counts and the held-out segments are the real survey, and holding out segments is how my field tests a gap-filling map. What I act on is different: a per-cell density of long-tailed ducks over the season, read in relative terms. A one-day daytime count in a 180 m strip is a noisy stand-in for it (USE-5, USE-8). For this species the stand-in is weaker still. The Mass Audubon team that flew these surveys wrote that they were flown "during daylight hours when the vast majority of LTDUs are absent from the Sound" (Allison, Perkins & Perry 2009, MMS 2009-020). The use case is real (P3): the actor, the decision and this kind of data are all in use today. The metric scores my decision **partly** (MET-1, MET-3, MET-10). I would choose `mean_poisson_deviance` on the count.

**How the decision is made today**
- **The federal Atlantic maps (BOEM 2018-010, Winship et al.).** The maps behind BOEM's Atlantic wind planning are seasonal maps of relative density on a 2 km grid. They come from boosted zero-inflated count models with the area surveyed as an offset (Sec. 2.5.2). Dynamic ocean covariates enter as long-term climatologies, and at map time "All other predictor variables were set to their mean values" (Sec. 2.5.8). The tuning CV is stratified by transect and minimises the out-of-bag negative log-likelihood (Sec. 2.5.6). Models are chosen by the sum of ranks over PDE, AUC, rank correlation, median and mean absolute error, and RMSE, with PDE breaking ties (Sec. 2.5.7). The report says that "it is the relative differences in predictions across space that are relevant, not the actual numbers themselves" (Sec. 4.3). It also warns that predictions "in areas with no survey effort should be interpreted with extreme caution", and that the sea-duck maps came out too flat because of single huge flocks (Long-tailed Duck winter is named; Sec. 3.2.3).
- **The source (Smith et al. 2019).** The maps show, for every segment, the median of predictions on 10 dates per winter (Figs. 4-6). Weekly totals for the whole Sound are summed from the same predictions (Fig. 7) and checked against the observed total of each survey (Fig. 8). Validation is in sample only (Sec. 2.5).
- **The state plan (Massachusetts Ocean Management Plan).** The plan's sea-duck layer (a "special, sensitive or unique" resource that constrains siting in state waters) was built in 2021 by CZM interpolating USFWS survey data. In May 2026 the Ocean Science Advisory Council proposed replacing it with USFWS's own analysis. I know this only from a search snippet; the slides answered 403. So simple spatial interpolation is the baseline any model has to beat.

**1. Inputs at the moment of prediction (after the winter's surveys)**
- **I have all of the shipped covariates for a map of a surveyed winter.** That covers position, seabed, tides, the ferry route, ocean colour, modelled SST, the winter's NAO and the day. The after-season values (`sst_winter_mean_c`, `nao_winter`, the 2002-2006 chlorophyll and CDOM means) fit the after-winter prediction point (USE-3). The federal practice uses climatologies anyway, and the builder measured that dropping them costs 0.003 R^2 on log1p.
- **`transect_km` would not exist for a cell the plane never flew.** At map time I would set it to a standard strip, as `fit_reason` says. As an exposure it is harmless.
- **One input I would always have is missing as an input: the same day's counts in the flown strips next to the gap.** Interpolating from them is what CZM did. A tabular model only sees them as training rows and has to recover them through position x day interactions. It does: within each survey day, LightGBM on log1p correlates 0.33 with the test counts on log1p, against 0.28 for an inverse-distance interpolation of the 8 nearest same-day training strips. So this is inherent to the format, not a fix to make.
- **Detection covariates are absent:** sea state, glare, observer. Surveys were flown only at winds of 15 kt or less with more than 15 km visibility (Sec. 2.1.2), so this is minor.

**2. The target**
- **What I act on:** the expected density per cell over the season (or the share of the study area's birds inside a lease block), with its uncertainty. The segment-day strip count is the observation every density model is fit to and validated on (Winship scores per transect segment), so it is an acceptable stand-in. It is not the quantity on my map.
- **Long-tailed duck, specifically:** the siting question at Horseshoe Shoal for this species was night roosting and dawn/dusk commuting through the project area. The telemetry found that the birds also spend nights on Nantucket Shoals and spread "over 100's of square miles of Nantucket Sound" (MMS 2009-020, conclusions 2-4). A daytime count measures daytime use only. The builder picked this species for a statistical reason (the 10 largest counts hold 84% of the squared deviation, against 98.6% for scoters). That is defensible, but the notes should say what the daytime count does not cover.
- **The form I need:** a number on the mean scale, because totals and lease-block shares are sums of expected counts. LightGBM fit on log1p and inverted predicts only 29% (20-37%) of the observed test-fold total; LightGBM with a Poisson loss predicts 64% (44-79%). The source's Fig. 8 check would fail the first one outright.

**3. Row and test data**
- **One row is not one decision.** The decision is made once per cell (or lease block) per season, from the map. The row is the field's validation unit, so scoring per row matches practice but not the decision.
- **The test segments are random flown segments; the real gaps are not.** The 50 never-flown segments are coastal: a median 3.7 km from land against 7.0 km for flown segments, and 16 of them sit in two edge columns (8 each). The spacing does match: 97.7% of test segments have a training segment 1.5 km away, and so does the median never-flown segment. So the shipped test asks the right kind of question over the wrong habitat mix.
- **Most cells of the source's map are flown segments on unflown dates.** For those the segment's own history is known (USE-10), and the task does not test that case. That is a fair choice, since the task takes the gap-filling case, but the use case should not read as if the whole map were gap-filling.

**4. Would I use this model?** Only if it beat the interpolation I can run in an afternoon, and on the unit I act on it does not. For each test segment with at least 10 surveys, I compared observed against predicted ducks per km over its survey days (about 113 segments per fold, 9 shipped splits):
- Rank correlation: LightGBM log1p 0.51, LightGBM Poisson 0.47, inverse-distance interpolation of the training segments' seasonal density 0.50, same-day interpolation 0.49, flat map -0.04.
- Paired against the seasonal interpolation: log1p +0.013 (SE 0.029, better on 6 of 9 splits); Poisson -0.028 (SE 0.023, 4 of 9).
- Share of the test segments' ducks held by the top quarter of segments as each method ranks them: seasonal interpolation 0.51, LightGBM 0.41, flat map 0.20.

This matches the source's finding that the spatial surface dominated and that "we likely missed important variable(s)" (Sec. 4.1).
- **What would make me trust a model:** it beats interpolation on held-out segments, it reproduces the survey totals (Fig. 8), its hotspots are stable across folds, and it comes with per-cell uncertainty.
- **What would make me distrust one:** a back-transformed log model, a score that one flock decides, and predictions in the coastal cells that the shipped test never samples.

**5. Does the declared metric score my decision? Partly.**
- **What RMSE gets right:** it is on the count scale and consistent for the mean, which is what I sum (MET-3).
- **What it gets wrong:** the unit is the segment-day, and 1-2 of about 2,600 test rows hold half the squared deviation. R^2 on the count is 0.005-0.023 (builder). Poisson LightGBM does beat the flat map on 9 of 9 splits, by 0.6 of 64.9. But RMSE ranks both interpolation maps, which find hotspots as well as or better than LightGBM, below the flat map: the seasonal one beats it on 1 of 9 splits, the same-day one on 0 of 9. A metric that prefers a flat map to the map that finds the hotspots does not score my decision (MET-1).
- **The metric I would use: `mean_poisson_deviance` on the count, a context origin (MET-11).**
  - It is consistent for the mean, like squared error, but weights relative error, so one raft does not decide it.
  - It is the deviance behind the field's selection: Winship's PDE (the tie-breaker), and the out-of-bag negative log-likelihood that both Smith and Winship tune on.
  - On the shipped splits Poisson LightGBM wins 8 of 9 splits. The log1p model, which understates totals 3.4-fold, beats the flat map on only 2 of 9.
  - It needs a standard scikit-learn metric added to the library with its tests (MET-12, MET-13), plus a floor on predictions.
- **Why not `rmsle`:** it ranks the log1p model first on 9 of 9 splits, the model whose totals are 29% of the observed.
- **The ideal score is per segment**, aggregated over the test segment's days, which is the unit I act on. The current `aggregation="mean"` keeps one label per group and does not fit `labels="per_sample"`, so this is a note for later, not a change now.
- **MET-6, MET-7 and MET-9 do not apply.** Nothing fixes a threshold, a cost or a top k; the outline around the top 2% of segments in Figs. 4-6 is a display choice.
- **Consistency:** the wadden_sea_sibes_macoma_abundance practitioner reached the same choice (Poisson deviance, not rmsle), while noaa_afsc keeps RMSE because RMSE is that source's own metric. One family-wide decision would settle all three.

**Gaps between the dataset and the real decision, ranked by how much they change the task**
1. **Target and unit (USE-5, USE-8).** A daytime strip count on one day stands for a seasonal per-cell density. For the long-tailed duck it also misses the birds' night use of the Sound and their commute. This changes what every per-row score rewards: getting each survey day's Sound-wide level right (`day_of_winter` is the best single feature, R^2 0.15) counts for more than where the ducks are, which is what the map is about.
2. **Metric resolution (MET-1, MET-10).** Under RMSE the methods sit within noise of a flat map, and the maps that find hotspots lose to it.
3. **Test geography (USE-8).** Random interior segments stand for the coastal edge cells that are the real gaps.
4. **Inputs (USE-3).** `transect_km` is known for test rows, and the same-day neighbour counts are not explicit inputs. Both are small, and the first is already named.

**What an expert would change**
- **Fit:** set `fit="approximate"`. The `fit_reason` should name the stand-in (a daytime segment-day count for the seasonal density per cell, daytime use only for the long-tailed duck) and the coastal never-flown cells (USE-8). USE-9 does not rescue `direct`: the per-survey Sound-wide total (Fig. 7) fits the rows better, but most of the cells unflown on a given day have their own history, which the grouped split withholds (USE-10).
- **Notes:** add a `curation_comments` bullet on the daytime absence of long-tailed ducks, citing MMS 2009-020, by the same Mass Audubon team (Allison is a co-author of the source).
- **Metric:** declare `mean_poisson_deviance` from context with a floor. If adding a metric is out of scope now, keep `rmse` with the note as written, plus the numbers above on the interpolation maps. Do not switch to `rmsle`.
- **Use case wording:** say that the planner reads relative density per cell and that scoring per segment-day is how the field validates. The current text implies a per-day product.

**Sources**
- Smith et al. 2019, Ecology and Evolution 9:2346-2364 (PMC6405508; a copy in the run folder): Secs. 2.1.2, 2.2, 2.5, 3.3, 4.1, 4.2; Figs. 4-8.
- Winship et al. 2018, OCS Study BOEM 2018-010, <https://espis.boem.gov/final%20reports/BOEM_2018-010.pdf>: Executive Summary, Secs. 2.5.2, 2.5.6-2.5.8, 3.2.3, 4.3. Text extracted in the run folder.
- Allison, Perkins & Perry 2009, MMS 2009-020, <https://tethys.pnnl.gov/sites/default/files/publications/MMS%20LTDU.pdf>: Project Summary, Statement of the Problem, conclusions 1-5. Text in the run folder.
- Massachusetts Ocean Science Advisory Council slides of 2026-05-04 (sea-duck SSU layer), <https://www.mass.gov/doc/massachusetts-ocean-science-advisory-council-meeting-slides-5-4-26/download>: the fetch returned 403, so this rests on a search snippet only.
- Sea Duck Joint Venture atlas, site 79 narrative, <https://seaduckjv.org/atlas/pdf/narrative_site79.pdf> (search snippet: the long-tailed duck commute to Nantucket Shoals, and lease areas south of the Sound).
- Probes, untuned, on the shipped 3 x 3 grouped splits:
  - `map_probe.py` in the run folder, output in `map_probe.txt` and `map_probe.csv`;
  - `gap_geometry.py` (output quoted above);
  - `mean_bias.py`, output in `mean_bias.txt`.
- Also read: the builder's `metric_probe.txt`, `design_probe*.txt`, `drop_winter_aggregates.txt` and `coverage.txt`.

</details>

<details><summary>Blind review</summary>

**Dataset:** nantucket_sound_sea_duck_aerial_survey_counts. Target `log1p_long_tailed_duck_count`, regression, 7,751 rows x 22 columns, grouped by `segment`, 3 repeats x 3 folds.

**Verdict:** Include with changes. The data is real, faithful to the source and free of target leakage, and it is a sensible zero-inflated ecological count task. Drop the `segment` ID from the features, and accept or tighten the segment-held-out split knowing that it is optimistic.

**What the task is**

Long-tailed ducks were counted from the air in Nantucket Sound (MA, USA) over three winters (2003/04 to 2005/06). There were 30 standardized strip-transect surveys. Counts were pooled into 1.5 km x 1.5 km grid segments, giving one row per surveyed (segment, survey date). Smith et al. built the data to map sea-duck distribution for marine spatial planning around the proposed 454-MW Cape Wind farm on Horseshoe Shoal. In their words: "spatially-explicit abundance estimates of marine birds are necessary to assess potential impacts from planned offshore wind energy developments". The prediction is a real one. A planner or wildlife agency predicts the duck count at a location and date, in order to map abundance and judge displacement risk. Each survey crosses only about 274 of the 454 ever-surveyed segments (median; range 109 to 294). Filling the unflown segments, and the 50 never-surveyed edge segments, is therefore a real use.

**What I verified (positive)**

- **Faithful to the source.** I downloaded the authors' `Data/data_ltdu.Rda` and `Data/ducks&environment.RData` from github.com/adamdsmith/NanSound_EcolEvol (the code companion of the Dryad deposit). Both the source and `data.parquet` have:
  - 7,751 rows;
  - 78,041 long-tailed ducks in total;
  - 3,327 non-zero rows (57.1% zeros).
- **Values match.** After a join on segment, day and effort, the unscaled covariates match the source `env.segs` to within 1e-15. This covers coordinates, SST, SBT, depth, distance to land, stratification and NAO.
- **The target is exact.** `expm1(target)` is an integer to within 5e-13. Counts range from 0 to 3000, with a 99th percentile of 122.
- **Survey count matches the paper.** There are 30 (winter, day) surveys, with 13, 10 and 7 per winter. The paper says: "we conducted 30 (2003/2004: 13, 2004/2005: 10, 2005/2006: 7) standardized aerial strip-transect surveys".
- **Clean table.** There are no missing values, no duplicate rows, and no duplicate (segment, winter, day) keys. Every segment-level covariate is constant within its segment.
- **License.** The Dryad API reports CC0-1.0.
- **No target-derived feature.** All covariates come from rasters, ocean-model output or survey effort (`create_final_data.R`). None is computed from the counts.

**Concerns, most to least serious**

1. **`segment` is a 454-level categorical ID that should not be a feature.**
   - Under the grouped split, every test segment is an unseen level, so the column carries no information that transfers.
   - Its integer code also encodes location: the segment ID correlates r = 0.999 with easting, because the grid is numbered column by column.
   - With LightGBM (task split, 3x3), R2 is 0.254 without `segment` and 0.227 with it as a categorical feature.
   - **Change:** keep `segment` as the group key only and remove it from the feature matrix. If the harness already strips the group column, this point goes away.

2. **The segment-held-out split is optimistic because same-day neighbours stay in training.**
   - `winter` plus `day_of_winter` identifies the survey exactly, and the survey-level mean target varies widely (0.03 to 2.34 across surveys).
   - Counts are strongly spatially autocorrelated within a survey. The mean of a row's four 1.5-km neighbours on the same survey correlates 0.48 with its target.
   - A model can therefore learn "this survey's level here" from adjacent training segments flown the same day. LightGBM R2 by split:

     | Split | LightGBM R2 |
     |---|---|
     | Task split (segments held out) | 0.254 |
     | 6 km x 6 km spatial blocks held out (38 blocks) | 0.191 |
     | Whole surveys held out (a new survey date) | 0.123 |

   - The task split is defensible for filling gaps on flown days and for predicting at never-surveyed segments. It overstates skill for the paper's other use, prediction on unsurveyed dates. The paper's maps predict "on 10 evenly-spaced dates from 15 November through 1 April".
   - **Change:** either keep the split and document that it measures within-survey spatial interpolation, or group by spatial blocks (about 6 km) for a more conservative spatial test. I would not switch to survey-grouping as the main split, because the decision is spatial.

3. **The signal is modest and mostly survey-day plus location. The environmental covariates add little.** LightGBM R2 under the task split:

   | Feature set | R2 |
   |---|---|
   | Mean only | 0.00 |
   | Survey ID only (winter, day) | 0.145 |
   | Static habitat covariates only | 0.037 |
   | Survey + effort + coordinates | 0.259 |
   | All features | 0.254 |

   - Model families do separate: ridge on one-hot features 0.076, kNN (k=30) 0.145, RandomForest 0.251, ExtraTrees 0.254, a tuned LightGBM 0.256.
   - The spread across repeats is small (sd 0.002 to 0.006), so differences of about 0.01 are scoreable.
   - The ceiling is low and the strong tree ensembles bunch within about 0.005 of each other. Counts of flocking birds are very noisy. The paper reports in-sample pseudo-R2 = 0.32 for long-tailed duck.
   - This is acceptable for a benchmark, since it is realistic and not trivial, but it will not separate top methods sharply.
   - **Change:** none required. Note the low ceiling in the metadata.

4. **Some covariates hold information from after the survey date, and SST is model output.**
   - `sst_winter_mean_c` is the November to March mean of that winter, so it includes months after early-season surveys.
   - `sst_month_c` is the mean of the whole survey month.
   - `bottom_temp_summer_c` is the May to October mean of the winter's start year. For the late-October survey (day -64), that window includes the survey month.
   - The code comment calls SST "Monthly sea surface temperature (FVCOM)", which is an ocean hindcast model, not an observation.
   - None of this uses the target, and it fits retrospective mapping. It would matter only for a real-time forecasting framing.
   - **Change:** none needed for a mapping task. Say so in the task description.

5. **Some columns are redundant.**
   - `nao_winter` takes 3 values and is a 1:1 relabel of `winter` (-0.09, 0.38, -0.87).
   - `sst_month_relative_c` is SST minus the mean over the survey month and winter. It correlates 0.989 with the within-survey deviation of `sst_month_c`.
   - These are harmless for trees but inflate the feature count.
   - **Change:** optionally drop `nao_winter`.

6. **Effort varies and the target is a raw count.**
   - 288 rows (3.7%) have under 0.25 km of transect in the segment, and 50 rows have under 0.05 km (minimum 1.8 m). Their non-zero rate is 6 to 14%, against about 45% at full 1.5 km effort.
   - `transect_km` is a covariate, which matches the source. The authors used `obs_window` as a covariate rather than an offset, because "small values in some segments impaired model estimability when treating obs_window as an offset".
   - **Change:** acceptable as is. Optionally drop rows under about 0.1 km (105 rows) to cut pure noise.

7. **Sibling targets.** The same survey and covariate table also supports common eider and scoter count tasks (the paper models all three).
   - **Change:** if the benchmark contains another target from this source, keep only one, so the suite does not double-count one feature table and one survey design.

8. **Scope.** The data covers one 1,100 km2 area, 3 winters and 30 survey days, from 2003 to 2006. The temporal diversity is small, but the size (7,751 rows) is adequate for scoring.

**What I could not check**

- The Ecology and Evolution article at doi:10.1002/ece3.4738 returned HTTP 403. I relied on the arXiv preprint (1705.00644, an earlier version of the same analysis) and on the authors' Ecology and Evolution GitHub code and data. So I could not quote the final paper's Appendix S2 covariate definitions. Definitions come from `R/create_final_data.R` and `R/model_ltdu.R`.
- I did not download the 1 GB Dryad zip or the raw GIS rasters and shapefiles. I verified against the authors' processed R objects, not against raw observer records.
- I could not check detectability or observer effects. The source applies no detection correction, and there is no observer column.
- I could not see whether the benchmark harness drops the group column `segment`, or whether sibling targets from this source are in the suite.

</details>

<details><summary>Precedent check</summary>

**Precedent check: nantucket_sound_sea_duck_aerial_survey_counts (precedent-checker, 2026-11-01)**

**Verdict.** Most of the definition follows its precedents: the inclusion, the grouped regime and the direct fit
(5g_energy_consumption, Lennart 2026-10-14), the source route under Andrej's rule of 2026-11-01, the target scale, the
fallback metric, the exposure feature, the tag, and the zeros built by the authors' recipe. Four points depart with no
fact that sets them apart, and each has a prompt below:

* A. The builder's "otherwise No" makes the metric a condition of the keep (TP-2, forest_fires).
* B. The stated moment, "after a winter's surveys", is contradicted by the grouped folds and the 2002-2006 means
  (wadden's archive map).
* C. The date is dropped and its parts kept, the reverse of AFSC (CLEAN-12).
* D. One measured gap in the zero-fill: 800 long-tailed ducks of 2006-03-06 that the same flight's NCEI record holds
  and the deposit lacks (wadden's LEAK-25 handling).

I found no drift and no third exception. The same-run siblings are AI drafts that no curator has decided. I name them
as cases to decide alike, not as precedents.

What I read: the register (1,620 decisions, 92 of them Andrej's), the Cases tables, and the records behind the
precedents (metro_manila_village_weekly_dengue, sweden_depth_to_bedrock, heritage_health_prize, onlinenewspopularity,
covertype, houses, fremtpl2). Also the policy answers of 2026-10-30 in `curation/inputs/two_regime_zero_triage_summary.md`, the
REVIEW.md of wadden, noaa_afsc and cape, and the drafts and mediator reports of pennsylvania, boreal and crms. My own
checks are in the run folder:

* Dryad's download routes for this deposit (headers only);
* the all-species empty-unit test per survey day (`empty_units.py`, `empty_units.txt`);
* NCEI's sightings placed on the deposit's segments (`segment_join.py`, `flock_800.py` and their `.txt` outputs).

| # | Decision | Rules | Standing | Closest precedents |
|---|---|---|---|---|
| 1 | Inclusion: CC `Yes`, priority 3 (Andrej, 2026-10-30) | SEL-2, USE-1 | consistent | Andrej's policy 1 (2026-10-30: species mapping judged per dataset). The same day: `Yes` for wadden, noaa_afsc, boreal, pennsylvania, crms and cape. Set apart: north_american_breeding_bird_survey_counts `No` ("No predictive task"), great_lakes_marsh_bird_point_counts 2nd Tier as screened. |
| 2 | Regime grouped by segment, not the record's Temporal | SPLIT-1, SPLIT-3, SPLIT-4, USE-10 | consistent on the use-case reason; one clause argues from the score | 5g_energy_consumption (Lennart, 2026-10-14). Drafts: wadden (grouped); noaa_afsc (temporal, set apart by a stated fact). Tensions row "the right split against the score" (forest_fires). The crms mediator (2026-11-01). |
| 3 | Fit `direct`; every same-run sibling is `approximate` | USE-8, USE-9 | consistent | 5g_energy_consumption (USE-9 Cases: direct); the siblings are set apart by gaps of their own |
| 4 | Target: the long-tailed duck, one of the source's three groups | USE-5, CLEAN-8 | consistent; one note missing | noaa_afsc issue 1 (rex sole picked from 22 probed species, a weighing call); wadden (the paper's species) |
| 5 | Shipped as log1p, scored on the count | MET-3, CLEAN-16 | consistent | forest_fires (Lennart, 2026-10-21); drafts: wadden, pennsylvania, noaa_afsc |
| 6 | Metric: fallback `rmse` (the source tunes by out-of-bag NLL and validates by a pseudo-R2) | MET-5, MET-11 | consistent | cape (draft: a CRPS needs a predictive distribution, so fallback); wadden issue 3 and pennsylvania issue 4 (both open) |
| 7 | Builder: keep only "if ... a log-scale or deviance metric are accepted; otherwise No" | TP-2, MET-10 | **departs, no fact given** (prompt A) | forest_fires (kept 2026-10-06); boreal mediator (TP-2) |
| 8 | Prediction moment "after a winter's surveys"; winter aggregates and 2002-2006 means kept | USE-3, LEAK-10, SPLIT-3 | **departs, no fact given** (prompt B) | wadden (after its mediator: a map drawn from the whole archive); noaa_afsc ("a place in a survey year under that year's conditions"); basque_ctd's precedent check (one moment per use case) |
| 9 | `transect_km` kept as a feature | Andrej's call 3 (2026-10-30), CLEAN-19 | consistent | fremtpl2 (Andrej, 2026-10-20: `Exposure` kept); wadden's precedent check (a raw count keeps its exposure) |
| 10 | Dropped: `xkm`/`ykm` (copies), `date` (for winter and day), segment as the group | CLEAN-5, CLEAN-12, LEAK-33 | `xkm`/`ykm` and segment consistent; `date` **departs, no fact given** (prompt C) | noaa_afsc keeps the date and drops `year` as "the date's year"; wadden keeps the date; CLEAN-2 Cases (Lennart, 2026-10-21: the datetime encoding is the pipeline's) |
| 11 | `nao_winter` kept beside `winter` (one to one) | CLEAN-5, CLEAN-1 | departs from a sibling, with a stated reason | pennsylvania drops `TRT`, one to one with its flags (draft); expresso_churn_prediction (Lennart, 2026-10-22: CLEAN-5 not triggered). Reason given: both are Table 1 covariates. |
| 12 | Zeros: a flown segment-day without a record is a zero, as in the authors' scripts | LEAK-25, policy 2 | consistent with the recipe precedents; one gap located (prompt D) | wadden (the descriptor's recipe, then unrecorded rows dropped; LEAK-25 amended 2026-10-21); Andrej's policy 2 (2026-10-30) |
| 13 | Source: the Zenodo mirror of the Dryad deposit, under "If you cannot find a source, it's 2nd tier" | PROV-8, EV-7 | consistent; the stated reason needs two more facts | sweden_depth_to_bedrock (CC 2026-11-01); metro_manila (CC 2026-10-30); heritage_health_prize (CC 2026-10-30, "find a copy"); cape mediator; boreal mediator; pennsylvania |
| 14 | `year = "2019"` | PROV-9 | consistent | airfoil_self_noise (Lennart, 2026-10-20: the year of the publication that holds the rows) |
| 15 | `Two-Regime Zeros` tag kept | Andrej's rule 4 (2026-10-30) | consistent | Removed for pennsylvania (48 zeros against 38 ones) and basque_ctd (3.5% against 1.9%) |
| 16 | NCEI's 7 extra survey days not added (draft issue 5) | PROV-11, PROV-14 | consistent | framingham_heart_study_fhs (PROV-14: rows from another source would make a rebuild) |

**2. Regime.** The lead reason is the source's own: maps of every segment on 10 dates in each surveyed winter (Fig. 4),
and no forecast (Sec. 2.5). That is the 5g_energy_consumption reasoning (a split by station fills the gap for unmeasured
stations, Lennart 2026-10-14), and it is wadden's. noaa_afsc is set apart by its stated fact: each map stands for five
future years.

The record's `Temporal (NON-IID)` and its tag are values from the AI screening. The measured stage supersedes them
(principles, "Stages"), as it did crms's `Grouped`. They belong in "Record fields that disagree".

Two texts present the TP-10 failure as a reason for grouped: the `splits_comment` clause "as a forecast the counts are
decided by each segment's own past (TP-10)" and the builder's "Departures" line. SPLIT-4 and the forest_fires Tensions
row bar a score as a reason. The crms mediator already read this case as "went grouped when leg 1 failed" and refused
to carry that over to crms.

Recommendation: write TP-10 as what the other regime would mean. Temporal fails leg 1, so it would be `No` under
SEL-10, like stock and appliances_energy_prediction. It is not a reason for grouped. Written that way, the case does
not become a precedent for re-framing failed panels. The pick stays the curator's (SPLIT-1), as in wadden issue 1 and
AFSC issue 2.

**3. Fit.** Each sibling is approximate for a gap of its own:

* wadden: no elevation input and no named decision;
* AFSC: no habitat layers, regions and life stages pooled;
* pennsylvania: every species counted, a weak treatment contrast.

This definition has the source's Table 1 covariates, the source's rows and a decision the source names (siting). USE-9
(the 5g case) makes filling unmeasured units direct. USE-9's counterweight is a use case rephrased to excuse a gap. It
is answered here because the mapping use is in the source's words (Introduction, Fig. 4), not ours.

The `fit_reason` sentence on the strip length describes an exposure the map maker sets to a standard 1.5 km. It is not
a stand-in.

**4. Target.** As in AFSC, USE-5 holds for each of the three groups, so the group is a weighing call. The Decision table
shows the evidence. After its panel, AFSC's notes say the species was chosen on the whole table with the test years in
view (CLEAN-8). The same sentence is due here: every row is in some test fold, and the choice read the tail of all rows
and the eider's held-out R^2 (0.15).

AFSC's alternative, a second group as a sibling dataset (PROV-7), applies here too. A small point for this group: the
deposit holds fitted models only for it and the scoters (`Results_ltdu.zip`, `Results_scot.zip`). The README also names
`Results_coei`, which is not in the deposit.

**6. Metric and the builder's options.** The authors stop boosting by out-of-bag negative log-likelihood and report a
pseudo-R2 on the log-likelihood. Both need a predictive distribution. cape met the same shape (priors chosen by CRPS)
and declared the fallback; this definition follows it. On the three options in the builder's draft issue 3:

* `rmsle` from context. Precedents: diamonds (Lennart, 2026-10-21), onlinenewspopularity (Lennart, 2026-10-26: a
  heavy-tailed share count "whose error matters relative to the count"), and noaa_storm_events_damage (draft: counties
  ranked by orders of magnitude).
  * Against it here: the authors' own check sums the predicted counts per survey and compares totals
    (`R/compare_predicted_vs_counted.R`, `R/predict_weekly_total_abundance.R`). wadden's draft gives the same fact
    against RMSLE ("the actor sums densities"), and pennsylvania's mediator uses it to set wadden apart.
  * I found no fact that would set this dataset apart from wadden.
* The Poisson deviance: wadden issue 3's family option. Here it could be declared a stand-in, since the source tunes by
  a count log-likelihood (MET-5); wadden called it context. cape's CRPS went to the fallback, not to a stand-in.
* Keep `rmse` with the tail note, as wadden and pennsylvania implement.

Make one family call (wadden 3, pennsylvania 4, this one, basque biotoxins) rather than a separate issue with other
options.

**13. Source.** Measured 2026-11-01:

* Dryad's per-file route answers 401.
* Its version route (version 2092) answers 405, "The dataset is too large for zip file generation". So the
  pennsylvania route, which boreal moved to, does not exist for this 4.5 GB deposit.
* Zenodo record 4932958 is in Dryad's community and carries the same DOI. Its md5 for `NanSound_Ecol&Evol.zip`
  (6c4e3288...) equals the digest in Dryad's own API listing (saved in the run folder).

So a scripted, byte-identical copy exists, the source is found, and the rule does not fire. That matches the cape
mediator's reading (only a source reachable by hand counts as not found) and heritage_health_prize ("find a copy").
metro_manila went 2nd Tier because no copy was found. PROV-8 is met: the download text names both the copy and the
original.

Two wording fixes keep the reason true under EV-7, as boreal's mediator required for boreal's "401":

* name the version route's 405;
* say the md5 equals Dryad's own listing, not only Zenodo's.

**14. Year.** NCEI accession 0115356 (page dated 2014-10-07) holds the raw sightings, not the rows: no segments, effort,
zeros or covariates. 2019 stands.

**12. Zeros, measured.** Wadden's precedent check asked for its empty-unit test on this dataset.

* No block like SIBES 2008. 24.3% of flown segment-days have no record of any group, 10.7-70.4% per survey day. The
  high days are the ends of the season and short surveys: 2005-04-18 at 70.4%; 2005-10-28, 2006-03-06 and 2004-03-23
  at 38.5-39.3%.
* NCEI's in-strip long-tailed duck sightings, placed on the deposit's segments, fall as follows:
  * 80,844 ducks in segment-days where the deposit has a count;
  * 429 in segments the deposit lists as not flown that day (2004-03-23, 2004-12-22);
  * none off the grid;
  * 1,725 in 285 flown segment-days where the deposit has a zero.
* Of those 1,725, 925 are spread over 284 segment-days of 23 days, at most 163 ducks a day. This is likely the edges of
  the segments; untested.
* The other 800 come from one pass:
  * Transect 11-10 on 2006-03-06, 13:04-13:06. The five largest sightings (609 ducks) share one position exactly, and
    all 800 fall in one 1.5 km square.
  * None of them are in the deposit: its largest count that day is 60, and the segment there (329, flown that day)
    holds a zero.
  * They alone explain that day's ratio of 0.327 (388 + 800 = 1,188, NCEI's total).
* The authors join sightings to segments in a GIS table that is not in the deposit (`obs_poly.dbf` in
  `R/create_final_data.R`), so why these sightings are missing cannot be read from the data.

**Consistency checks for the curator**

A. **Consistency check (AI, 2026-11-01):** the builder's recommendation keeps the dataset only if a log-scale or
deviance metric is accepted, "otherwise No". Precedents decided the other way:

* forest_fires (Lennart, 2026-10-06; TP-2: R^2 0.013, TabPFN beats the mean on 26 of 32 folds), kept;
* wadden issue 3 and pennsylvania issue 4 (same run), which keep `rmse` with the same tail;
* boreal's mediator, who refused an exclusion for weak signal under TP-2.

Here, LightGBM with a Poisson loss beats the training mean on 9 of 9 shipped splits (R^2 0.023 on the count). What
sets nantucket apart?

(a) RMSE on the count cannot rank models on these folds, since 1-2 of about 2,600 test rows hold half the squared
deviation. Run wadden's test (drop each fold's largest test rows and compare the model ranking by Kendall tau). If the
ranking collapses, the remedy is the metric under the family call (MET-2), still not `No`.
(b) Treat it like forest_fires and wadden: keep, under the metric the family call picks.
(c) Reopen forest_fires.
(d) Amend TP-2 so that a metric that barely separates models is a reason to retire.

B. **Consistency check (AI, 2026-11-01):** the use case and notes name the moment "after a winter's surveys". But a
2003/04 test segment trains on the 2004/05 and 2005/06 surveys, and `chlorophyll_a_mg_m3` and `cdom_absorbance` are
means over July 2002 to March 2006. wadden (after its mediator) names the moment of a map drawn from the whole archive,
which makes the same facts known at the prediction point. What sets nantucket apart?

(a) The source maps each winter on its own (Fig. 4), so the moment is per winter. Then the later winters and the
2002-2006 means are not known, and the task becomes the temporal design that fails TP-10 (`No`). Against this reading:
the authors' Fig. 4 maps come from one model fit on all 30 surveys.
(b) Treat it like wadden: name the moment as after the last survey of 2005/06 in the use case, the split text and the
notes. The winter aggregates then raise no issue, and the builder's draft issue 2 closes. Its alternative, an in-season
map without the winter aggregates, would also lose the later winters and the 2002-2006 means: that is temporal (SPLIT-3).
(c) Reopen wadden to a per-survey moment.
(d) Amend USE-3.

C. **Consistency check (AI, 2026-11-01):** the definition drops `date` and keeps `winter` and `day_of_winter`.
noaa_afsc keeps the date and drops `year` as "the date's year", and wadden keeps the date (both same-run drafts).
CLEAN-12 and the CLEAN-2 case of 2026-10-21 (Lennart: the datetime encoding is the pipeline's) favour the date. The notes
give only "a copy", which holds in both directions. What sets nantucket apart?

(a) The source's covariates are the winter and the day of the season (Table 1), and a winter spans two calendar years,
so the parts are the source's own axis. Recorded as an exception to CLEAN-12 (serves CLEAN-1).
(b) Treat it like AFSC: keep `date` as a datetime and drop `winter`, or keep `day_of_winter` beside the date.
(c) Reopen AFSC and wadden to keep the parts.
(d) Amend CLEAN-12.

This is a quality point (P7) and cheap either way.

D. **Consistency check (AI, 2026-11-01):** wadden dropped samples whose fauna was never recorded, located by a rule
that does not read the label (LEAK-25 as amended 2026-10-21; account_debt_south_africa,
fraud_detection_in_electricity_and_gas_consumption). This definition zero-fills every flown segment-day. NCEI's record
of the same flight places 800 long-tailed ducks on transect 11-10 of 2006-03-06 that are in no deposit row, so that
pass's segment-days probably hold zeros for ducks that were counted. What sets them apart from wadden's 2008 rows?

(a) They cannot be located: the sightings share one frozen position, so no rule tells which segments the pass covered,
and LEAK-25's "located by a rule" does not apply. Keep the rows with a note naming the day, the transect and the 800
ducks.
(b) Treat them like wadden's 2008 rows: drop the 2006-03-06 survey (168 rows, a rule that never reads the count), or
only the segment-days of transect 11-10, located from NCEI's transect and clock.
(c) Reopen wadden to keep its 2008 rows with a note.
(d) Amend LEAK-25.

**Outside this dataset (a question for another record).** metro_manila_village_weekly_dengue went to 2nd Tier on Andrej's
CC of 2026-10-30 ("if we need to manually download it"), on the Assessment that "Dryad's download routes need a login".
On 2026-11-01 Dryad's version route for that deposit (version 411989) answered 302 to its zip generator without a token.
I read the headers only and did not fetch the zip. This is the route pennsylvania and boreal use. Nantucket and
metro_manila were decided apart on whether a scripted route exists. If the zip arrives, the fact behind metro_manila's
2nd Tier no longer holds.

**Like cases to decide together.**

* Metric for heavy-tailed abundance: wadden 3, pennsylvania 4, nantucket, basque biotoxins.
* The regime's stated reason: crms, basque_ctd.
* The choice of species: AFSC issue 1.
* The zero-fill test: AFSC has not run it.

</details>

<details><summary>Advocate</summary>

**Advocate, opening brief (2026-11-01): nantucket_sound_sea_duck_aerial_survey_counts**

**Position: ship after changes.** No finding of the panel calls for `No`. Each problem the evidence agents found has a fix on the "fix the definition" or "keep with a note" rung of the remedy ladder. Most fixes are wording. The real changes are two: the metric (decided with the family) and, if the curator wants it, a coarser group key. The only route to `No` (split auditor, issue 1) needs a use case the definition does not declare.

**1. The data is real, faithful to its origin and free of leaks (P5, P4 leak side; PROV-3, PROV-13, LEAK-10, LEAK-33, all Must).**
- Bytes: the Zenodo md5 equals Dryad's own listing, and all three raw sha256 sums reproduce (claim audit 41; precedent 13).
- Rows: 7,751 rows from 30 surveys (13/10/7, as the paper states), holding 78,041 ducks. The covariates match `env.segs` to 1e-15 (blind reviewer). The table is rebuilt from the unscaled frame, so the all-row `scale()` of `data_ltdu.Rda` is avoided (claim audit 9).
- Independent origin: on 3,609 of 3,612 segment-days, the deposit equals NCEI 0115356's in-strip count minus the birds marked flying (column auditor). The "median 94%" is therefore a documented exclusion, not lost data.
- LEAK-10 holds for every column, and no feature is computed from the counts. `segment` is only the group column: 20 features ship (column audit; claim audit 5). This answers the blind reviewer's concern 1, which assumed `segment` was a feature.
- Why it stands: no agent disputes it. It is the P5 base, and objections of rank P6 or P7 cannot remove it.

**2. The use case is real, and the source names it (P3; USE-1, USE-2 Must; SEL-2).**
- The source states the decision: "marine spatial planners must carefully consider ... where to place marine protected areas or offshore wind energy developments" (Sec. 4.2). It states the method: models "predict utilization of un-sampled areas" (Introduction).
- The domain practitioner: "The use case is real (P3): the actor, the decision and this kind of data are all in use today." Massachusetts CZM built the state plan's sea-duck layer by interpolating survey data.
- The curator decided inclusion: CC `Yes` (Andrej, 2026-10-30), under policy 1 (species mapping is judged per dataset).
- Why it outranks: the fit and metric objections (USE-8 labels, P6) can at most make the fit approximate or change the metric. None of them makes the fit None.

**3. The split mirrors the declared task, and the same-day counts are legitimately known (P4; SPLIT-23, SPLIT-4, SPLIT-28 Must; USE-9 Should).**
- The split auditor says it plainly: "The split therefore matches the declared use case". The definition declares "for each survey day" and "the other segments of the same days are in training".
- The practitioner, on inputs at the prediction point: the same day's counts in the flown strips next to the gap are inputs "I would always have". Within a day, the model correlates 0.33 with the test counts, against 0.28 for same-day inverse-distance interpolation.
- Precedent with the same structure: 5g_energy_consumption (Lennart, 2026-10-14, USE-9 Cases, applied). Stations are held out within one week, other stations' same hours are in training, and the fit is `direct`.
- SPLIT-29 needs "an entity that new data would not have". A gap square on a survey day does have its survey day, so under SPLIT-4 the day is a feature, not a hidden group.
- SPLIT-28 does not fire. Models beat the mean on unseen segments: R^2 0.25 on log1p; Poisson LightGBM beats the mean on all 9 of 9 splits; per-segment seasonal rank correlation 0.51, against -0.04 for a flat map.
- What I concede: no source sentence names an actor who fills in one survey day. Fig. 4 predicts on dates that are not survey days.
- Fix that keeps the dataset (wording only): say that Fig. 4's dates are not survey days; rest the support on "un-sampled areas" and the 5g reading; add the double hold-out number (-0.077) so readers see that the score rests on same-day counts.
- Reading the maps-on-unsurveyed-dates case into the task would swap the declared task for another. The definition does not claim that case.

**4. Grouped, not temporal, follows the use case (P4; SPLIT-3, USE-10 Must).**
- The source never forecasts a later winter (Sec. 2.5). It maps the winters it surveyed from one fit on all 30 surveys.
- Temporal would be `No` anyway. TP-10 leg 1 fails under every metric: R^2 on log1p 0.042 against 0.025 for the segment's past mean; RMSE 105.9 against 106.6 (claim audit 13; split auditor 3). That puts temporal under SEL-10.
- The measured stage supersedes the screening's `Temporal (NON-IID)` (principles, "Stages"), as it did for crms.
- What I concede: the clause "decided by each segment's own past (TP-10)" overstates, and it reads like a score argument (SPLIT-4; the forest_fires Tensions row).
- Fix: rewrite TP-10 as what the other regime would mean, and change the record to `Grouped (NON-IID)` with the matching tag.

**5. The same-transect neighbours are a real optimism, and fixable (P4; SPLIT-1 Must, here a matter of degree; SPLIT-24).**
- What I concede, as measured:
  - Dropping each test row's same-day north-south neighbours from training costs 0.074 R^2 (0.251 to 0.177, SE 0.007; claim audit 6).
  - The never-flown squares lie on the border. They have a same-day flown square within 1.5 km on 43% of survey days; shipped test rows have one on 95% (split auditor 2).
- Both fixes keep the dataset:
  - (a) A note in `splits_comment` with these distances and the border-square score, the split auditor's mildest remedy (as in the wadden draft).
  - (b) Group on 3x3 blocks of the source's grid, or on transect columns. Both keys are built exactly from the coordinates (SPLIT-24). They score R^2 0.19-0.20 and 0.16 (Spearman 0.45 and 0.43). The 3x3 blocks match the never-flown squares' neighbour distances: 52.8% within 1.5 km, median 1.5 km, 75th percentile 3.0 km.
- If the curator keeps the declared question (never-flown squares), SPLIT-1 points to (b), a one-line change of the group key.
- The lower score is no reason to retire: the split follows the application (P4 over P6; SPLIT-4; forest_fires).

**6. The metric is not a reason to drop: change it with the family (P6; TP-2 Should; MET-1, MET-11 Must).**
- The task has signal under the declared metric. Poisson LightGBM beats the mean on 9 of 9 splits (RMSE 64.3 against 64.9). On log1p, R^2 is 0.25 and Spearman 0.49.
- forest_fires (R^2 0.013) was kept under TP-2. The builder's "otherwise No" departs from it and gives no fact that sets this case apart (precedent prompt A).
- What I concede (MET-1): RMSE on the count separates models by about 1% of the constant. It also ranks the interpolation maps, which find hotspots, below a flat map (practitioner).
- Fix (definition rung): mean Poisson deviance on the count, with a floor on predictions, added to `metrics.py` with tests (MET-12, MET-13).
  - It is the count likelihood closest to the source's out-of-bag negative log-likelihood, so it can be declared a stand-in under MET-5 and MET-11.
  - It separates models by 12%, and Poisson LightGBM wins 8 of 9 splits.
  - Decide it once for the family: wadden issue 3, pennsylvania issue 4, basque biotoxins.
  - Not rmsle: the source sums expected counts (Fig. 7 and 8), and rmsle favours the model whose totals reach only 29% of the observed.
- Until the family call: keep `rmse` with the tail note, as the wadden and pennsylvania drafts do.

**7. The rest is wording or a note (P3 to P7; the remedy ladder).**
- Prediction point (USE-3 Must, met by rewording). Change "after a winter's surveys" to "after the three winters (spring 2006)". The source fitted all 30 surveys before it drew its maps, and wadden took the same reading (precedent prompt B, option b). Then the 2002-2006 means and the winter aggregates are known at the prediction point. Chlorophyll-a and CDOM are worth -0.001 R^2 anyway (claim audit 31).
- Zeros (LEAK-25 holds). A zero is a flown strip with no long-tailed duck on the water. NCEI-only ducks fall on 285 segment-days; with flying birds removed, on 1. The flocks of 800 (2006-03-06) and 711 are also missing from the authors' own `obs_poly.dbf`, which fits flying birds having been removed (column auditor). Take prompt D option (a): keep the rows, with a note naming the day.
- Fit. `direct` follows 5g under USE-9, and the precedent checker reads it as consistent. The practitioner's point on daytime use (MMS 2009-020) goes into a note (USE-5). If the curator reads the fit as `approximate`, only the label changes.
- Quality (CLEAN, cheap):
  - rename `depth_m` to `seabed_elevation_m`;
  - rewrite the Decision's reason: the eider is the less raft-dominated group, so the long-tailed duck is chosen for its held-out R^2 (0.26 against 0.15) and fewer zeros (57% against 75%);
  - record dropping the date as an exception to CLEAN-12, because a winter spans two calendar years (prompt C, option a);
  - fix the claim wording (claim audit 4, 26, 42, 49-51).

**Judgment record as I see it**

```text
Verdict: ship after changes.
Validity: SEL-2 holds (CC Yes); USE-1 holds; USE-3 holds once reworded; LEAK-10, LEAK-25, LEAK-30 hold;
  SPLIT-3/USE-10 grouped holds; SPLIT-1 optimism of about 0.07 R^2, fixed by a note or by 3x3 blocks (curator call).
Value: TP-2, moderate real signal (log1p R^2 0.25; 9/9 splits beat the mean on the count); MET-1 met by Poisson deviance (family call).
Quality: depth_m name, Decision reason, CLEAN-12 exception for the date, claim wording.
For the curator: the group key (segment or 3x3 blocks); the family metric.
```

</details>

<details><summary>Critic</summary>

**Critic (AI, 2026-11-01): nantucket_sound_sea_duck_aerial_survey_counts, opening brief**

**Verdict: do not ship as defined.** It can ship after changes 1 to 5. If the curator does not accept filling in a
surveyed day as the use case (point 1), the verdict is `No` (SPLIT-28). I do not dispute the data: it is faithful
(NCEI cross-check, PROV-3), it was rebuilt from the unscaled table (LEAK-30 avoided), and no column leaks. What is wrong
is what the test stands for, the fit the definition claims, and the metric.

```text
Verdict: ship after changes (No if point 1 is not accepted).
Validity: USE-3 triggered twice (the day's own counts carry the score; the moment is after the programme), fixed by
  rewording, or No; USE-5/USE-8 triggered (fit direct not earned), fix: approximate; SPLIT-1 triggered (same-transect
  neighbours in training, interior test squares), fix: re-split on the grid; SPLIT-3: the record disagrees, fix the record.
Value: MET-1 and MET-11 triggered (RMSE on the count cannot rank models; the origin is a stand-in), fix: change the metric.
Quality: the Decision's reason is refuted by its own table; four wrong statements; the sign of depth_m.
```

**1. The score rests on the survey day's other counts, but the use case cites maps for dates with no survey (P3/P4;
USE-3, SPLIT-23, Must).**
- Problem: `winter` + `day_of_winter` identify the survey date, and about two thirds of each day's flown squares are
  in training. The day's training mean alone gives R^2 0.146 of the shipped 0.249 (log1p). The covariates and strip
  length without the day give 0.031.
  - Withhold the day as well (a new square on a date not in training): LightGBM -0.077, RF -0.038, training mean -0.007.
  - A known square on a date without its counts: 0.044, against 0.039 for the square's own mean.
  - Source: split auditor, the split auditor's s6_double and s7_bydate outputs.
- Effect: `use_case` and `grouping.definition` cite the source's maps (Figs. 4-6), "predicted on 10 evenly-spaced
  dates from 15 November through 1 April". Those are not survey days, and the planner reads the seasonal value per
  cell (domain practitioner; BOEM 2018-010 Sec. 4.3: "the relative differences in predictions across space").
  No source sentence names anyone who fills in one survey day. The closest is Fig. 8, which compares predicted and
  counted totals per survey: a model check, not a decision. Under the use case as cited, the date is an entity new
  rows lack and it carries the label (SPLIT-29). The splits that fit that use case leave no signal for a new square,
  and SPLIT-28 then says the dataset goes.
- Remedy (mildest): keep the survey-day framing only with support of its own.
  - Name the actor who fills in a surveyed day.
  - Stop citing Figs. 4-6 as support for the split, or say that their dates are not survey days.
  - Put the double hold-out number in `curation_comments`.
  - If the curator does not accept that use, `No`, as the CC foresaw ("if it turns out a bad task, then we drop it
    to no").

**2. The prediction point is after the programme, not "after a winter's surveys" (P3; USE-3, Must, fixed by
rewording).**
- Evidence (column auditor, precedent checker B):
  - A 2003/04 test segment trains on the 2004/05 and 2005/06 rows.
  - `chlorophyll_a_mg_m3` and `cdom_absorbance` are means over July 2002 to March 2006 (Table 1).
  - Tidal velocity and stratification are 2003-2005 means.
- No signal moves: dropping chlorophyll and CDOM changes R^2 by -0.001 (claim auditor, a6), and dropping
  `sst_winter_mean_c` and `nao_winter` takes 0.252 to 0.249 (builder).
- Remedy: reword `use_case`, the first bullet and the Note bullet to "after the last survey of 2005/06 (spring 2006)",
  the moment wadden settled on after its mediator. No data change. The builder's in-season alternative (draft issue 2)
  would lose the later winters as well: that is the temporal design, which fails TP-10.

**3. Fit `direct` is not earned (P3; USE-5, USE-8, Must).**
- The split part fails (point 4).
- The target is a stand-in. One daytime count in a strip about 180 m wide, on one day, stands for the seasonal density
  per cell that the planner reads (domain practitioner; the BOEM maps are seasonal relative densities).
  - For this species, the team that flew these surveys wrote that they were flown "during daylight hours when the vast
    majority of LTDUs are absent from the Sound" (Allison, Perkins & Perry 2009, MMS 2009-020; Allison is a co-author
    of the source).
  - At Horseshoe Shoal the siting risk was the ducks' night roosting and their dawn and dusk commute, not their
    daytime use.
- The count is of ducks on the water. The deposit equals NCEI's in-strip count minus the birds marked flying on 3,609
  of 3,612 segment-days (column auditor), and the definition does not say so. 2005/06 carries no behaviour field.
  Two flocks of that winter are missing (711 and 800 ducks), most likely flying birds; this stays open.
- Remedy:
  - set `fit="approximate"`;
  - make `fit_reason` name the stand-in (a daytime segment-day count for the seasonal density; daytime use only) and
    the test geography;
  - add one notes bullet on the daytime absence (MMS 2009-020) and on the on-water count, with a sentence on 2005/06.

**4. The test squares are easier than the squares the task names (P4; SPLIT-1, Must; USE-10).**
- Transects run north-south.
  - 95.3% of shipped test rows have a training square flown the same day 1.5 km away. The 50 never-flown squares have
    one on 43.1% of survey days.
  - An unflown segment-day has the neighbour on its own transect flown that day only 20.7% of the time (claim
    auditor; split auditor, `s3_daily.txt`).
- Decisive test (claim auditor a9; I re-ran it and got the same numbers, in the run folder): hold out 5% of
  segments (40 draws) and drop only the test rows' same-day neighbours on their own transect (618 rows).
  - R^2 falls from 0.251 to 0.177 (-0.074, SE 0.007).
  - Dropping the same-day east-west neighbours instead gives +0.002 (SE 0.003), and dropping 618 random rows -0.004 (claim auditor a10, not re-run).
  - So about 30% of the shipped skill comes from neighbours that a real gap rarely has.
- All 50 never-flown squares lie on the border of the grid (3.6 km from land, against 7.3 km). Flown border squares
  score 0.17, 0.20 and 0.13 out of fold, against 0.24-0.27 for interior squares (split auditor).
- In practice the field holds out transects: BOEM 2018-010 Sec. 2.5.6 tunes with "A stratified (by transect ID) 5-fold
  cross-validation". Like case: airfoil_self_noise (SPLIT-1 Cases, re-grouped when 91.5% of test runs had a close
  neighbour in training).
- Remedy: re-split on a key built exactly from the grid (SPLIT-24).
  - For the question as written ("a square the survey flights never covered"): the transect column (R^2 0.155-0.172),
    or 3x3 grid blocks (0.189-0.200). The blocks come closest to the never-flown squares' distances: 52.8% adjacent,
    75th percentile 3.0 km, against 43.1% and 3.0 km.
  - If the curator prefers the common gap (80% of the unflown segment-days belong to squares flown on other days),
    that is a warm start under USE-10: group on transect column x survey day (0.296) and rewrite the question.
  - A note alone would leave a measured 30% overstatement under a Must.

**5. RMSE on the count does not score the decision, and its origin is mislabelled (P6; MET-1, MET-11, Must).**
- Resolution: on each of the 9 folds, 1 or 2 of about 2,600 test rows hold half the squared deviation. The best
  model is 1.0% below the constant (64.3 against 64.9).
- Wrong ranking: RMSE ranks a flat map above both interpolation maps (seasonal 67.7, same-day 82.1, flat 64.9). Yet the
  interpolation maps find the hotspots: their top quarter of test segments holds 0.51 and 0.43 of the ducks, against
  0.20 for the flat map (domain practitioner, `map_probe.txt`). A metric that prefers a flat map to a hotspot map does
  not score a siting decision (MET-1).
- Origin: the source picks its boosting iterations by the out-of-bag negative log-likelihood (Sec. 2.3.2). That is a
  criterion it tunes by (MET-5), and it cannot be computed from a point prediction, so the metric is a stand-in, not
  a fallback (MET-11).
- Remedy: declare `mean_poisson_deviance` on the count as the stand-in, naming that original.
  - It is a count likelihood and, like squared error, consistent for the mean that the maps and totals sum.
  - It separates models: 12.4% between the best model and the constant (claim auditor, a11), against 1% for RMSE.
  - It is what the field selects on (the out-of-bag negative log-likelihood, and BOEM's PDE).
  - Add it to `metrics.py` with a floor for zero predictions (MET-12, MET-13).
  - Not `rmsle`: it ranks first the log1p model whose predictions sum to 29% of the counted total.
  - Decide it as one call for the family, with wadden issue 3 and pennsylvania issue 4.
  - Then run the tuned methods on the shipped splits under it; none have been run (TP-1).

**6. The record and the split text disagree with the definition (P4; SPLIT-3, SPLIT-4, Must; fix the record and one
sentence).**
- The record keeps `required_split: Temporal (NON-IID)`, the tag `Non-IID (Temporal)` and "fit direct for predicting
  the segment counts of later surveys", while the definition is grouped.
- `splits_comment` gives "as a forecast the counts are decided by each segment's own past (TP-10)" as a reason for
  grouped. SPLIT-4 bars a score as the reason. The clause also overstates: the segment's past explains R^2 0.025, and
  under the declared RMSE no forecast clearly wins (105.9, 106.6 and 107.4; claim auditor).
- Remedy:
  - change the record to grouped once point 4 is settled;
  - rewrite the clause as: "a forecast of a later winter fails TP-10 leg 1, so a temporal task would be `No` under
    SEL-10; the regime follows the source's use, maps of the surveyed winters".

**7. Quality: the Decision's reason is refuted by its own table, and four statements are wrong (P7; EV-7, CLEAN-8;
fix the text, no reason to exclude).**
- "The long-tailed duck's counts are the least dominated by single rafts" is false: the eider is less dominated (top
  10: 0.699 against 0.844; top row 0.175 against 0.262).
  - The real reasons: more signal on held-out segments (R^2 0.26 against 0.15), fewer zeros (57% against 75%), and one
    scoter raft holds 67% of the scoters' squared deviation.
  - Say that the species was chosen on all rows, test folds included (CLEAN-8; noaa_afsc).
- "Flocks of hundreds, up to 3,000, make most of the rest" is false: the non-zero median is 7, and counts of 100 or
  more are 3.6% of the non-zero rows, holding 45% of the ducks.
- "Above 1.5 where a transect crossed the segment twice" is false: 5,968 of the 6,062 rows above 1.5 km are single
  crossings of 1.5-1.6 km, and only 94 are above 1.6 km.
- "The other three files are fitted models" is false: one of them is the README.
- `depth_m` holds elevations (-21.4 to -1.5 m): rename it (`seabed_elevation_m`) or negate it.

**Dropped, not backed**
- `segment` as a feature (blind reviewer): `feature_columns` drops the group column, so the model sees 20 features
  (claim and column auditors).
- Weak signal as a reason to retire: TP-2 and forest_fires bar it.
- Dropping 2006-03-06 under LEAK-25: the column auditor's flying-bird match explains the missing flock better than a
  recording gap (folded into point 3).

</details>

<details><summary>Advocate rebuttal</summary>

**Advocate, rebuttal (2026-11-01): nantucket_sound_sea_duck_aerial_survey_counts**

**Where we stand.** The critic and I agree on the verdict, "ship after changes", and on most of the changes. I concede points 2, 4, 5, 6 and 7. On point 3 I narrow the claim: the label follows the split decision. One dispute is left, point 1: whether refusing the survey-day framing leads to `No`. I ran the check that decides it. The answer is no on the log scale and yes on the count, so it is a curator call, not an automatic `No`.

New check (scripts and outputs in the run folder: `r1_spatial_without_day.*` and `r2_idw_vs_mean_double.*`):
- Setup: untuned LightGBM as in the panel, and an inverse-distance interpolation (IDW) of the 8 nearest training segments' means.
- Splits: the shipped 9 splits, and the split auditor's double hold-out (new square and new date, same seeds).
- Scores that remove the day's level: the within-day Pearson correlation on log1p, and the per-segment Spearman (each test segment's mean observed value against its mean prediction).

| Design | Model | R^2 log1p | within-day r | per-segment Spearman |
|---|---|---|---|---|
| shipped | LightGBM, all features | 0.249 | 0.321 | 0.522 |
| shipped | IDW of segment means | 0.054 | 0.243 | 0.547 |
| double hold-out | LightGBM, all features | -0.077 | 0.232 | 0.344 |
| double hold-out | LightGBM without the day, winter and monthly fields | -0.044 | 0.211 | 0.337 |
| double hold-out | IDW of segment means | 0.033 | 0.236 | 0.423 |
| double hold-out | strip length only | -0.036 | 0.090 | 0.078 |

Under the double hold-out, IDW against the training mean, per fold:
- R^2 on log1p: +0.039 (SE 0.010), better on 8 of 9 folds.
- RMSE on the count: +1.28 (SE 0.69), better on 4 of 9.
- Poisson deviance on the count: -1.65 (SE 1.74), better on 5 of 9.

**1. The day's other counts carry the score (USE-3, SPLIT-23, SPLIT-28, SPLIT-29). Concede the facts, narrow the consequence.**
- Concede:
  - The day's level is 0.146 of the shipped 0.249.
  - Fig. 4's dates are not survey days, and Fig. 8 is a model check, not a decision.
  - No source sentence names someone who fills in one survey day.
  - The critic's wording remedies are right: qualify Figs. 4-6, and put the double hold-out number in `curation_comments`.
- Contest "the splits that fit that use case leave no signal for a new square".
  - Without any of the day's counts, the spatial pattern on new squares survives: within-day r 0.23 (strip length alone: 0.09), and per-segment Spearman 0.34 for LightGBM and 0.42 for IDW.
  - A spatial interpolation beats the training mean on log1p on 8 of 9 folds. SPLIT-28 asks that all models score below the mean on unseen groups, and that does not hold on the log scale.
  - It does hold on the count: RMSE 4 of 9 and Poisson deviance 5 of 9, both within noise.
  - What the planner reads is "the relative differences in predictions across space" (BOEM 2018-010 Sec. 4.3; critic and practitioner). That is the part that survives. What fails is the date's absolute level.
- What follows:
  - If the curator accepts the survey-day framing: the 5g_energy_consumption structure (Lennart, 2026-10-14, applied), plus the practitioner's statement that the same-day flown strips are an input he always has. Ship with the wording.
  - If the curator refuses it: SPLIT-28 is not met on log1p, so the choice is between a segment x date re-split with a small log-scale signal (TP-2, forest_fires) and `No` on the count. That is a weighing call for the curator, not an automatic `No`.

**2. The prediction point is after the programme (USE-3). Concede.** Same as my point 7. Reword to "after the last survey of 2005/06 (spring 2006)", as wadden does. No data change.

**3. Fit `direct` is not earned (USE-5, USE-8). Narrow.**
- Concede the notes: the daytime absence of long-tailed ducks (MMS 2009-020), the on-water count, and the 2005/06 sentence (USE-5).
- Contest the daytime point as a reason for `approximate` on its own.
  - USE-5 asks what the actor acts on. Here that is the source's map, and the map shows the expected count in a 1.5 km x 180 m strip (Sec. 3.3, Fig. 6): the same quantity as the target.
  - The night-use gap lies between the survey method and the siting risk. The source accepted it when it drew the maps. It is not a gap between our data and the source's product.
- The label follows point 4.
  - If the group key changes to the grid (point 4), the split mirrors the gaps, and `direct` stands under USE-9 (5g).
  - If the segment key stays with a note, the split part of USE-8 is not mirrored, and I accept `approximate`.
- Either way only the label and `fit_reason` change.

**4. The test squares are easier than the real gaps (SPLIT-1, Must). Concede, including the stronger fix.**
- The critic adds what my opening lacked:
  - a precedent: airfoil_self_noise (Lennart, 2026-10-20, SPLIT-1 Cases), re-grouped when 91.5% of test runs had a close neighbour in training; here 95.3% of test rows do;
  - the field's practice: CV by transect (BOEM Sec. 2.5.6).
- So under the Must a note alone is not enough. Re-split on a key built exactly from the grid (SPLIT-24):
  - 3x3 blocks match the never-flown squares' distances best (52.8% adjacent, 75th percentile 3.0 km; against 43.1% and 3.0 km);
  - transect columns follow BOEM's practice (R^2 0.155-0.172).
- Both keep the dataset. I would keep the cold-start question as written (USE-10). The warm-start alternative (column x day) rewrites the task, and the declared question does not ask for it.

**5. RMSE does not score the decision, and its origin is mislabelled (MET-1, MET-11). Concede.**
- Declare `mean_poisson_deviance` on the count as the stand-in, naming the out-of-bag negative log-likelihood (Sec. 2.3.2), with a floor (MET-12, MET-13). Decide it once for the family, then run the tuned methods (TP-1).
- My check adds one caution: under a stricter split, Poisson deviance on the count may not separate a spatial map from the mean (5 of 9 under the double hold-out). That bears on point 1 if the curator refuses the survey-day framing. It does not bear on the grid re-split, which keeps the day.

**6. The record and the TP-10 clause (SPLIT-3, SPLIT-4). Concede.** Use the critic's sentence, which is the one the precedent checker proposed. Change the record to `Grouped (NON-IID)` once point 4 is settled.

**7. Quality. Concede all of it**, including the CLEAN-8 sentence that the species was chosen on all rows, test folds included (as in noaa_afsc).

**Judgment record after the rebuttal**

```text
Verdict: ship after changes.
Validity: USE-3 met by rewording; USE-5 notes added; SPLIT-1 fixed by re-splitting on 3x3 grid blocks or transect
  columns (SPLIT-24); SPLIT-3 record fixed; SPLIT-28 not met on log1p even under a segment x date split (IDW beats
  the mean on 8 of 9 folds).
Value: MET-1/MET-11 fixed with a Poisson deviance stand-in (family call); TP-2 small real signal.
Quality: Decision reason, CLEAN-8 sentence, depth_m, wording.
For the curator: accept the survey-day framing (ship), or refuse it (segment x date re-split with a small log-scale
  signal, or No on the count); the fit label follows the group key.
```

</details>

<details><summary>Critic rebuttal</summary>

**Critic, rebuttal (2026-11-01): nantucket_sound_sea_duck_aerial_survey_counts**

**Position after the advocate's brief: ship after changes.** I withdraw my route to `No` (my point 1): a new fact
shows that the field validates with the same day's other transects in training. Three disputes remain for the
mediator:
- the split: re-split on 3x3 grid blocks, not a note (SPLIT-1);
- the metric: no interim `rmse` (MET-1);
- the fit: `approximate`, not `direct` (USE-8).

New check: c1_regroup_metric in the run folder. It uses untuned LightGBM, 3 repeats x 3 folds with
groups assigned to folds at random, and scores on the count with a prediction floor of 0.01.

| group key | groups | R^2 log1p | Poisson LGB vs mean: Poisson deviance | Poisson LGB vs mean: RMSE |
|---|---|---|---|---|
| segment (shipped) | 454 | 0.261 | -13.1% (9/9) | -1.1% (9/9) |
| transect column | 24 | 0.152 | -2.7% (8/9) | +0.5% (3/9) |
| 3x3 grid block | 60 | 0.203 | -10.3% (9/9) | -0.8% (9/9) |
| column x survey day | 618 | 0.280 | -23.3% (9/9) | -1.3% (8/9) |

**A1. Faithful data. Concede, with one narrowing.** The deposit equals NCEI minus flying birds on 2003/04 and 2004/05
(daily ratio 1.000; column auditor). 2005/06 has no behaviour field, so its two missing flocks (711 and 800 ducks) are
probably flying birds, but not shown to be. The note the advocate offers in A7 covers this.

**A2. A real use case. Concede.** USE-1 and USE-2 hold, and the fit is not None. A real decision does not make the
rows mirror it, though. That question is USE-8 (A7).

**A3. Same-day counts known at the prediction point. Concede the validity point; dispute the precedent.**
- New fact (BOEM 2018-010):
  - Sec. 2.4 gives the models "survey identity (ID)" as a random effect, and "day of the year and year" as smooths.
  - Sec. 2.5.6 tunes them with "A stratified (by transect ID) 5-fold cross-validation". Where a transect ID is a
    pre-defined transect, the other transects of the same survey stay in training. Sec. 2.4 adds that in some
    datasets a transect ID is instead "individual days of effort".
- Scoring held-out strips with the survey day's level learnable is therefore how the field selects these models
  (MET-1: "the way a practitioner would have chosen a model"). The day is a feature of the row (SPLIT-4), not a hidden
  entity, so SPLIT-29 and SPLIT-28 do not fire. I withdraw them.
- The wording remedy stands, and we agree on it: say that the dates of Figs. 4-6 are not survey days, and add the
  double hold-out figure (-0.077) to `curation_comments`.
- I dispute 5g_energy_consumption as support for `direct`. There the gap-filling task was the source's own: the Zindi
  test file weights new stations (5g record, Assessment 2026-10-21). Here the advocate concedes that no source names a
  survey-day fill-in. That fact sets the case apart under USE-9 (see A7).
- "The split matches the declared task" holds only if the test squares stand for the declared gaps. They do not (A5).

**A4. Grouped, not temporal. Concede.** We agree on the wording (TP-10 as what the temporal regime would mean, with
SEL-10) and on the record change.

**A5. The same-transect neighbours. Narrow to remedy (b) on 3x3 blocks; dispute remedy (a).**
- Remedy (a), a note, does not meet SPLIT-1 (Must). The question as written is "a square the survey flights never
  covered", and the advocate agrees that "SPLIT-1 points to (b)" while that question stands.
  - The optimism is 0.074 of 0.251 (about 30%; reproduced, in the run folder). It comes from neighbours a
    real gap has on only 21% of its days, so it is not a matter of degree.
  - The note precedent (wadden) is a draft no curator has decided.
  - The decided like case is airfoil_self_noise (SPLIT-1 Cases): re-grouped when test runs had close neighbours in
    training.
- The check above settles which key to use.
  - The transect column (24 groups, 8 per test fold) loses the signal on the count: RMSE +0.5%, better on 3 of 9
    folds; Poisson deviance -2.7%. I drop it from my remedy.
  - 3x3 blocks keep the signal: R^2 0.203 on log1p, Poisson deviance -10.3% on 9 of 9 folds. They also match the
    never-flown squares' distances (52.8% adjacent against 43.1%; 75th percentile 3.0 km for both).
- Remedy: group on 3x3 blocks of the source's grid, built exactly from the coordinates (SPLIT-24). If the curator
  instead reframes to the common gap, the warm start (USE-10), the key is column x survey day (-23.3%).

**A6. The metric. Concede the stand-in and TP-2; dispute the interim `rmse`.**
- I never asked for `No` on the metric. TP-2 and forest_fires stand.
- "Until the family call: keep `rmse` with the tail note" does not meet MET-1, a Must, and the advocate concedes that
  MET-1 fails. A Must takes no exception (principles, "Strengths"), so a note cannot carry it.
  - The new check sharpens this. Under the 3x3 blocks that SPLIT-1 calls for, RMSE separates the best model from the
    mean by 0.8%, and Poisson deviance by 10.3%.
  - The wadden and pennsylvania drafts are no precedent: no curator has decided them.
- Remedy: ship once the family call has been made. A curator who wants it shipped sooner is departing from a Must,
  which needs an amendment, not an exception.
- I narrow my own claim. Poisson deviance also ranks the same-day interpolation (46.9) below the flat map (46.5). It
  ranks the seasonal interpolation above it only barely (46.1; `map_probe.txt`). So the case for Poisson deviance rests
  on two things: its resolution (MET-10) and its closeness to the source's out-of-bag likelihood (MET-11). It does not
  rest on rewarding hotspot maps.

**A7. The rest.**
- Prediction point after the three winters: concede (my point 2).
- Zeros under LEAK-25, keeping the rows with a note: concede. I had dropped this point already.
- Fit `direct`: dispute (USE-8 Must, which USE-9, a Should, narrows only when its condition holds).
  - USE-9 asks for "another well-defined use case that practitioners have". The advocate concedes in A3 that no
    source names one, and 5g is set apart (A3).
  - USE-8 lists "a stand-in with a known gap" as approximate, and the gap here is measured and documented. A daytime
    count stands for the seasonal density the planner reads. For this species it misses most of the birds: the team
    that flew these surveys wrote that it flew "during daylight hours when the vast majority of LTDUs are absent from
    the Sound" (MMS 2009-020).
  - The domain practitioner, the panel's only domain evidence, says approximate. The precedent checker's "consistent"
    compared the case with 5g without this fact.
  - I agree with the advocate that the remedy is the label and `fit_reason`, not an exclusion.
- Quality items, including the date as an exception to CLEAN-12 (option a): concede.

**Judgment record as I now see it**

```text
Verdict: ship after changes.
Validity: USE-1/USE-2 hold; USE-3 holds once reworded (after spring 2006; Figs. 4-6 dates are not survey days);
  USE-8 triggered, fix: approximate (daytime count for seasonal density); SPLIT-1 triggered, fix: 3x3 grid blocks
  (SPLIT-24; not a note); SPLIT-3 grouped holds, record to Grouped; LEAK-10/25/30 hold.
Value: TP-2 holds (3x3 blocks: Poisson deviance -10.3% on 9/9); MET-1/MET-11 triggered, fix: mean_poisson_deviance
  stand-in via the family call before shipping, no interim rmse.
Quality: Decision reason, depth_m, claim wording, CLEAN-12 exception for the date.
For the curator: the group key (3x3 blocks, or column x day if reframed as warm start); the family metric.
```

</details>
