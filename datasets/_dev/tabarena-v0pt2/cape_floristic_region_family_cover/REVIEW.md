# cape_floristic_region_family_cover

**Outcome:** added. The AI recommends shipping it with the 21 plots at 0.99 kept and whole climate grid cells held
out (issues 1 and 2); the panel's changes are made. The data are the authors' release of the example table of Tang,
Frye, Gelfand and Silander's zero-inflated beta paper (GitHub `beckytang/ZIB_data`, commit of 2021-06-05; JABES
2023): 180 vegetation plots of 10 x 5 m in two Cape reserves (119 Baviaanskloof, 61 Cape Point). The target is the
plot's Crassulaceae cover as released, relative to a per-plot quantity the source does not document (49% zero, 12% at
0.99), predicted from the plot's coordinates, its reserve and four climate grids read at the site. The split holds out
whole 1-minute climate grid cells (104 cells, 20 x 3 folds), so no surveyed plot of a test plot's own cell is in
training; the metric is RMSE, the fallback.

Validity:
* SEL-2 holds: your `Yes` of 2026-10-30 and policy call 1 of that day.
* USE-1 holds: the paper's models "enable prediction to unobserved sites with known environmental attributes" (Sec. 6,
  p. 16). USE-8: fit approximate (no actor; a label of undocumented scale; climate and position only; a 50 m2 plot for
  a mapped site; two reserves).
* USE-5 met through the approximate fit, which needs a label that cannot be checked: the notes call the target
  relative cover of undocumented scale, with 0.99 a cap or a code; whether to fetch the Dryad file first is your call
  (issue 1).
* LEAK-10 holds: the other family's cover and the plot id are dropped. LEAK-26 is met by the note (issue 1).
* SPLIT-1 waits for your pick of the regime (issue 2): the cell folds put Baviaanskloof test plots as far from training
  as a random site of the surveyed area is from a plot (1.69 against 1.63 km). SPLIT-5: the paper's random split,
  checked against the data, puts them at less than half that distance (0.73 km). SPLIT-24 holds: the key is the
  1-minute cell itself. SPLIT-26 was triggered and fixed: the third covariate in the key, rainfall concentration, is
  not on the 1-minute grid.
* PROV-13: no repair source for the target was reached: the Cape Point survey on figshare counts individuals, and the
  Baviaanskloof file on Dryad downloads only by hand and may not hold these plots (issue 1). `BioClimMAP30s` ranks the
  Baviaanskloof plots like a temperature, not the precipitation the paper names, and its source grid (WorldClim 1.4)
  could not be reached, so it stays as published with a corrected description (EV-2, PROV-14).

Value: TP-2 and SPLIT-28 hold, a real signal on unseen cells (random forest skill 0.48 over the training mean, above
it on 60 of 60 splits); every test fold holds 50-69 plots and 20-39 zeros, so not Too Small (TP-5). RMSE is the
fallback: the paper reports Tjur's R2, an AUC and two CRPS variants side by side (MET-5).

Quality: after the panel (AI, 2026-11-01; rows, target and metric unchanged) the notes were corrected on the target's
scale and the 0.99 plots, `BioClimMAP30s`, the split numbers, the Cape Point survey history and the metric reason, and
the missing licence is accepted as a warning (EV-4). With the key on two covariates the split numbers were measured
again on the 104-cell folds, so they differ from those the panel reports quote (108 cells): Baviaanskloof test plots
1.69 km from training, not 1.62.

Weighed: a tiny table -; a methods paper's example with four covariates -; signal on unseen cells +; the authors' own
pinned release +.

Left for Andrej: issues 1 and 2, and the `required_split` row, which follows issue 2. Not verified: what 0.99 stands
for and how the family covers were built (the Dryad file needs a manual download); the Baviaanskloof survey years
(paper 2010-2011, Dryad 2011/12).

**Main points:** Keep the 21 plots at 0.99 with a note, without waiting for the Dryad file (issue 1), and hold out
climate grid cells instead of the paper's random split (issue 2).

**Record fields that disagree with the definition:**

- `required_split`: record `Random (IID)`, definition `Grouped (NON-IID)`.

**Issues for Andrej:**

1. **Keep the 21 plots at 0.99?** The target is the family's cover as released, 0 to 0.99. 21 plots (11.7%, 20 in
   Baviaanskloof) hold exactly 0.99 and none lies above it; the next values are 0.986, 0.961 and 0.949. Neither the
   paper nor the repository says what 0.99 is. Two readings fit: full cover recoded below 1 (the paper models cover on
   [0, 1)), or a cap, min(x, 0.99), on a value that can exceed 1. For the cap: in all 23 Baviaanskloof plots with both
   families between 0 and 0.99, the two covers are exact fractions with the same denominator (or a multiple of it),
   such as 55/372 and 175/372 in BK_113, and that denominator varies from 31 to 2,626 between plots. So the value is
   relative to some quantity counted per plot, not a share of the 50 m2, and it can exceed 1: the two family covers of
   BK_3 sum to 1.74 with neither at 0.99, and CP_2 sits at 0.99 in both. RMSE reads 0.99 as an exact value either way.
   * What it changes: the 21 plots are 12% of the test plots and carry 36% of an untuned random forest's squared
     error. With them, the forest has the lowest RMSE of four untuned models on 34 of 60 splits and a hurdle model
     (one model for whether the family is present, one for its cover where present) on 18; with the 21 plots kept in
     training but left out of the test score, the hurdle model wins 45 and the forest 3. So which model ranks first
     here turns on 21 values whose meaning is unknown.
   * For keeping: they are 21 of the 25 values at or above 0.8, most of the succulent-dense sites the use case looks
     for; a classifier trained on other cells finds them at ROC AUC 0.88; dropped from the data, they take the forest's
     skill from 0.48 to 0.19 on the remaining 159 rows (re-measured on the 104-cell folds).
   * For dropping: houses dropped its capped prices although its notes gave the reason used here for keeping, and
     under the cap reading these plots are censored (the true value is 0.99 or more, by an unknown amount), as houses'
     prices at 500,001 were.
   * Not checked: the authors' Baviaanskloof survey on Dryad (https://doi.org/10.5061/dryad.kk174, CC0) may hold the
     species covers, but its file downloads only by hand, and its surveys are dated 1991/92 and 2011/12, so it may not
     hold these plots. The Cape Point survey on figshare (https://doi.org/10.6084/m9.figshare.4737358) counts
     individuals, from which cover cannot be rebuilt.
   * Rule: LEAK-26 (Must) allows dropping the capped rows or documenting the cap; USE-5 (Must) lets a label of
     undocumented construction ship at fit approximate with a note only when it cannot be checked (diabetes_3). The
     one check left is the Dryad file, a single 3.4 MB CSV (CC0) that needs a download in a browser and may not hold
     these plots. The mediator counts it as not reachable; the critic asks that you make that call, so choosing keep
     or drop records that you decline the check; the advocate's rebuttal put the download or one email to the authors
     before the build. This departs from houses on the facts above: 11.7% of the rows here against 4.7% there, and a
     task that keeps its signal there and loses most of it here. The advocate and the critic both accept the keep; the
     critic asked the note to say that these plots decide which model wins, and it does.
   * Implemented: kept; the notes describe the target and the cap as above, with these numbers. Cost: the score
     treats 0.99 as exact though it may be censored, and these plots decide the ranking.
   * Alternative: drop the 21 plots, as houses (cost: 159 rows, three values above 0.9 left, most of the signal gone);
     or hold the dataset until you fetch the Dryad file or the authors answer, and repair the target from it if it
     holds these plots (PROV-13; cost: a delay, and the file may not hold these plots).

   Recommendation: keep. Decision: keep with the note, drop the 21 plots, or check the origin first?

2. **Hold out climate grid cells, unlike covertype and houses?** The paper scores random splits of the Baviaanskloof
   plots, "a training set of 99 locations and a test set of 20 locations" (Sec. 5.3, p. 15). The definition holds out
   whole cells of the 1-minute climate grids (about 1.9 x 1.5 km): all plots of a cell stay on one side, so no
   surveyed plot of a test plot's own cell is in training.
   * What it changes: the Baviaanskloof plots (two thirds of the rows) are clustered, a median 0.5 km from the nearest
     one, and nearby plots have alike covers (Pearson 0.58-0.66 under 1 km, about 0 beyond 4 km). A random site of the
     surveyed area is a median 1.63 km from a plot. Random folds put test plots 0.73 km from training, cell folds
     1.69 km. A random forest's skill (1 minus its squared error over that of the training mean) falls from 0.53
     (random) to 0.48 (cells); a nearest-neighbour model on the coordinates alone falls to the level of the mean in
     Baviaanskloof (skill 0.16 to -0.01). A random split lets a model score by copying the cover of a surveyed plot a
     few hundred metres away, which a map of an unsurveyed site cannot do; the cells take that away and leave the
     climate signal. At Cape Point the cells are stricter than mapping (0.92 km against 0.43 km), at little cost.
   * Precedents: covertype ships a random split of its 30 x 30 m forest cells for mapping inside the studied areas
     (Lennart, 2026-10-01: no coordinates, and a split by area had only 3 groups; and on 2026-06-23, "one would collect
     samples randomly across the studied area, and afterwards try to fill the gaps", which assumes plots spread at
     random, unlike these); houses ships random block groups (Lennart: "spatial information are not leaking"; your
     remark: "Currently, we do not include spatial data as non-iid. Might change that"); open_soil_data (not added,
     Lennart, 2026-09-23) named a spatial split the regime for mapping from points. What sets this case apart:
     coordinates and exact cells, and a clustered sample, so a random split tests at less than half the distance a map
     faces. It would be the first dataset grouped on a spatial grid key; if you accept, a SPLIT-24 case and a row in
     the Tensions table follow.
   * Rule: SPLIT-1 (Must; the curator picks the split the application needs), SPLIT-5 (Must; a paper's split is a
     claim to check), SPLIT-24 (Must; the key is exact: plots with the same two 1-minute values share a grid pixel).
     The advocate and the critic agree on the cells.
   * Implemented: grouped on the 1-minute cell, 20 x 3 folds.
   * Alternative: the paper's random split with the optimism stated, as covertype; or 2-minute blocks, which match
     sites in unsurveyed cells (Baviaanskloof test plots 2.28 km from training, such sites 2.03 km from a plot) but
     are pessimistic at Cape Point (1.31 km against 0.43 km); the forest's skill falls to 0.42.

   Recommendation: cells. Decision: cells, random, or 2-minute blocks?

**Review panel:** ship after changes (mediator). Claim audit: 29 claims, 22 hold (3 of them reworded), 3 refuted (the
0.99 wording and `BioClimMAP30s`, both fixed in the notes; the figshare survey as a repair source), the target as an
area share contested (reworded), the survey years untested (`row` reworded), and two outside the folder (the generated
README's metric line, the record's `required_split`). Blind review: exclude as prepared, on size alone, which no rule
backs and both briefs reject; its other concerns (the target's scale, `BioClimMAP30s`, coarser spatial blocks) are
taken up in the notes and issue 2. Debate: agreed on the grouped regime, the two-covariate key, the new wording of the
target, of the split text and of `fit_reason`, and the corrected numbers. The advocate contested the critic's fallback
of dropping the 21 plots at 0.99 as houses did; the critic's rebuttal accepted the keep, so the remedy and the
consistency with houses are your call (issue 1).

<details><summary>Mediator</summary>

**Mediator (2026-11-01): cape_floristic_region_family_cover**

**Recommendation**

```text
Verdict: ship after changes.
Validity: SEL-2 holds (Andrej's `Yes` of 2026-10-30; policy call 1). USE-1 holds (prediction at unobserved sites,
  Sec. 6, p. 16). USE-5 met through fit approximate once the target is reworded (relative cover of undocumented scale;
  0.99 a cap or a code); the origin check stays cannot-verify (EV-7). USE-8 approximate, gaps named. LEAK-10 holds
  (RESTIONACEAE and plot dropped); LEAK-26 met by the note (keep or drop: issue 1); LEAK-30, LEAK-33 hold. SPLIT-1 and
  SPLIT-5 hold (grouped, measured against the mapping domain; regime: issue 2); SPLIT-24 holds; SPLIT-26 triggered,
  fixed (key on the two covariates of the 1-minute lattice). PROV-13: no repair source reachable (figshare holds
  counts; Dryad only by hand); PROV-14 keeps BioClimMAP30s as published, its description corrected (EV-2).
Value: TP-5 holds (46-72 plots, 16-40 zeros per test fold); TP-2 and SPLIT-28 hold (RF above the mean on 60 of 60
  cell splits); MET-5 fallback rmse, reason completed (MET-11).
Quality: notes corrected (EV-8, PROV-16); licence warning accepted (EV-4).
Weighed: tiny table -; methods-paper example with four covariates -; real signal on unseen cells +; the authors' own
  pinned release +.
For the curator: issue 1 (keep the 21 plots at 0.99; consistency with houses); issue 2 (hold out climate cells;
  consistency with covertype and houses).
```

**Agreed facts**

- 180 plots (119 Baviaanskloof, 61 Cape Point), no missing values, no duplicates; sha256 matches the pinned commit
  97da77c; the repository has no licence.
- No kept column leaks: coordinates, reserve and four long-term grids. `RESTIONACEAE` (same survey, same per-plot
  denominator) and `plot` are dropped; `climate_cell` is the split key, not a feature (`n_features: 7`).
- Zeros are observed absences: presence agrees with the independent 2010 Cape Point survey on 57 of 57 plots.
- The target is not "the share of the plot": in 23 of 23 Baviaanskloof plots with both families between 0 and 0.99,
  the two values are fractions over one per-plot number (31 to 2,626); BK_3 sums to 1.74 with neither at 0.99; CP_2 is
  at 0.99 in both. 0.99 is a cap or a code; the source says neither.
- The 21 plots at 0.99 are 21 of the 25 values at or above 0.8; they carry 34% of an untuned RF's squared error (27%
  for LightGBM); with them RF and a hurdle model split the wins (28 and 27 of 60 splits), without them the hurdle wins
  44 and RF 3 (practitioner, re-run by the critic). Dropping them cuts RF skill from 0.475 to 0.096 (advocate,
  `cap_check.py`).
- Grouped is the right regime. In Baviaanskloof a random site of the plot hull is a median 1.63 km from a plot; cell
  folds put test plots 1.62 km from training, random folds 0.77 km. RF skill 0.545 random, 0.489 cells; k-NN on
  coordinates in Baviaanskloof 0.158 to -0.020. At Cape Point the cells are stricter than mapping (0.93 against
  0.43 km), at little cost.
- `BioClimMAP30s` is not millimetres; its values are n/60; in Baviaanskloof it ranks plots like mean annual
  temperature (Spearman +0.99 with CHELSA bio1, -0.77 with bio12). Kept as published (PROV-14).
- Not Too Small (TP-5, TP-2); the blind reviewer's exclusion for size rests on no rule, and both briefs reject it.
- `rmse` stays; the paper's four criteria have no unique original (MET-5).

**Decisive experiment (SPLIT-26 key; `m1_key.py` and `m2_dist.py`, in the run folder)**

- Two-covariate key (`apan_mean_an`, `tminave07c`): 104 groups, equal to a 1-minute lattice of the coordinates centred
  on whole minutes: 0 groups span two pixels, 0 pixels hold two groups, and only that offset of 100 tried works.
- Three-covariate key: no 1-minute offset fits; 4 pixels hold two keys, split by `RFL_CONC` alone (13.1 against 21.8,
  4.3 against 13.1; plots 0.21-1.80 km apart). Evaporation and July minimum agree in all four, so the claim auditor's
  "or the evaporation differs" does not hold.
- Baviaanskloof test-to-train distance (20 x 3 GroupKFold draws of my own, not the framework's seed): two-covariate
  key median 1.68 km, 27% under 1 km; three-covariate key 1.60 km, 31%; the domain 1.63 km, 27% (split auditor).
  RF skill 0.495 against 0.461 (split auditor), within fold-draw noise.

**Changes to make now (no decision needed)**

1. SPLIT-26 (Should), EV-2 (Must): `ONE_MINUTE_GRID_COLUMNS = ["apan_mean_an", "tminave07c"]` (104 cells, 53 with
   one plot, at most 1.8 km apart). Update the code comment, `grouping.definition` and the notes: `RFL_CONC` has 8
   values and is not on the 1-minute grid, though Sec. 2 says so. Re-measure the split numbers on the new folds.
2. SPLIT-1 (wording): `question`, `split`, `splits_comment` say "a site of the two reserves, with the surveyed plots of
   its own 1-minute cell held out". Give the residual optimism: sites in unsurveyed cells are a median 2.03 km from a
   plot; Pearson 0.32 at 1-2 km and 0.23 at 2-4 km. Write the clustering fact into `grouping.definition` (random folds
   0.77 km against 1.63 km for the domain): it is what sets the case apart from covertype.
3. USE-5, LEAK-26, EV-7: `predicted`, the Target and 0.99 bullets: the family's released cover, relative to an
   undocumented per-plot quantity; 0.99 a cap or a code; the shared-denominator, BK_3 and CP_2 facts; the Dryad file as
   an unchecked lead.
4. LEAK-26: the 0.99 note as settled under D3 below.
5. USE-8: `fit_reason` as settled under D2 below; the Cape Point sentence in `curation_comments`.
6. EV-2, PROV-14: the `BioClimMAP30s` bullet: labelled precipitation by the paper (Sec. 2); in Baviaanskloof it ranks
   the plots like mean annual temperature; at Cape Point the evidence is mixed; values n/60; identity not established;
   kept as published. Remove "whatever the scale, it keeps the order of the sites".
7. EV-8: LightGBM on 60 splits each (0.434 random, 0.374 cells, re-run on the new key); the correlogram as Pearson with
   pair counts; cells 1.9 x 1.5 km.
8. PROV-16, EV-7: `row`: the Cape Point plots are permanent plots (1966, 1996, 2010) and the release holds one survey
   of each; the Baviaanskloof years (paper 2010-2011, Dryad 2011/12) unverified.
9. MET-11: the metric reason adds that CRPSf picks the paper's priors (Sec. 5.1-5.2, p. 15) but cannot compare its
   models (Sec. 3.4, p. 10).
10. EV-6: the Zeros bullet adds the 57 of 57 presence agreement.
11. EV-4: accept `meta_license_unknown` with a reason, as bank_customer_churn.
12. Outside this folder: the README generator writes "the source defines no metric" for every `Metric.fallback`; a
    repository item, not a dataset change.

**Changes that need the curator**

- Issue 1 (USE-5, LEAK-26; P3/P4, Must): keep the 21 plots at 0.99 with the note, drop them (houses), or check the
  origin first. Recommended: keep.
- Issue 2 (SPLIT-1, SPLIT-5, SPLIT-24; P4, Must): hold out 1-minute cells, the paper's random split (covertype), or
  2-minute blocks. Recommended: cells.
- Record field `required_split`: `Random (IID)` against `Grouped (NON-IID)`.

**Disputed points**

D1. The group key (SPLIT-26). The advocate first called the two-covariate key optional; the critic held that a Should
is the default and a departure needs a fact. The advocate's rebuttal conceded. The experiment settles the fact:
`RFL_CONC` is not on the 1-minute grid (EV-2 outranks the paper's line), and the two-covariate key is the cell itself.
No fact for a departure was offered, so SPLIT-26 decides: change now (fix the definition, a re-split). Not a conflict:
SPLIT-24 holds for both keys.

D2. What `fit_reason` names (USE-8, Must). The advocate added the missing inputs; the critic wants also the unit and
Cape Point as a presence task. USE-8 asks that the gap making the fit approximate be named; its list is the rows, the
features, the label's timing and the split, and the API gives `fit_reason` one or two sentences. Settled:

- In `fit_reason`: no actor; the label is relative to an undocumented per-plot quantity with 0.99 a cap or a code;
  climate and position only (no vegetation type, terrain or fire age, which the paper names as drivers, Sec. 5.1);
  a 50 m2 plot stands for a mapped site (the rows; precedent crms_phragmites_cover); two reserves only.
- Not "placed in homogeneous stands": unverified, and the Cape Point plots lie on a systematic 914 m grid (figshare
  metadata).
- Cape Point as a presence task is a property of the target and of what the pooled RMSE weighs, not a gap between
  data and use case: one sentence in `curation_comments` (12 of 16 Cape Point plots with cover are below 0.05; cover
  skill there about 0.1 pooled, presence AUC about 0.8; the pooled score is mostly Baviaanskloof and the reserve
  contrast). The per-split -0.52 rests on 9-33 plots against a mean of 0.033; use the pooled figure (EV-8).

D3. The 0.99 note (LEAK-26, Must; EV-7, Must). The critic wants the ranking clause and no sat11 order argument; the
advocate wants the keep facts. Both are measured facts about the cap and do not conflict; "document the cap" takes
both. Settled: the note gives the count and place; the meaning as unknown (cap or code, with the facts); why kept,
without the full-cover inference (21 of 25 values at or above 0.8, learnable on unseen cells at AUC 0.88, skill 0.475
to 0.096 without them); and what it does to the score (34% of RF's squared error; RF 28 and hurdle 27 wins with, 3
and 44 without). The order argument goes: RMSE reads 0.99 as an exact value, unlike sat11's PAR10. A note is not a
metric of our own, so the metric Tensions row is not engaged.

D4. The Dryad check (PROV-13, EV-7). Both briefs agree it does not hold the dataset. The curator's rule of 2026-11-01
("If you cannot find a source, it's 2nd tier") counts a source reachable only by hand as not found. The dataset's
source, the pinned GitHub release, is found, so the rule does not demote it. The Dryad species file is a lead for
checking the target, reachable only by hand, so the label counts as one that cannot be checked (USE-5's approximate
route, as diabetes_3), and under EV-7 the check stays cannot-verify: named in the notes and in issue 1 as the step a
human may still take.

**Consistency with precedent**

- Grouping against covertype and houses (Lennart; IID): departs, and the facts that set it apart are measured:
  coordinates and 104 exact cells (covertype had neither and 3 areas); a clustered sample, so a random split tests at
  half the distance a map faces (0.77 against 1.63 km); 180 plots in a 750 km2 hull, where houses covers every block
  group. Andrej's own remark on houses ("Currently, we do not include spatial data as non-iid. Might change that")
  makes it a question: issue 2. If accepted, a SPLIT-24 Cases row (first spatial grid key) and a Tensions row.
- The 0.99 keep against houses (dropped): departs on facts named in issue 1 (11.7% of rows against 4.7%; most of the
  upper range; the task loses its signal without them). The bounded-share argument is not used, since the denominator
  finding undercuts it. LEAK-26 leaves the choice of remedy open, so it stays the curator's call.
- Consistent: `RESTIONACEAE` dropped (caracas_cervical_cancer); one target, no second folder (rosbank1, PROV-6);
  `rmse` fallback (gallstone_disease); 180 rows (musk kept, parkinsons retired); licence warning (bank_customer_churn).
- The rule of 2026-11-01 is not triggered (D4).

</details>

<details><summary>Claim audit</summary>

**Claim auditor: cape_floristic_region_family_cover (2026-11-01)**

**Verdict: ship after changes, all of them to the notes.** No test refuted a claim in a way that changes the task.
The split, the dropped columns, the zeros and the metric all held. Two claims are wrong as written: the target's
0.99 is stated as "the release's code for full cover" (P3), and `BioClimMAP30s` is said to be precipitation that
"keeps the order of the sites", but in Baviaanskloof it ranks the plots like a temperature (P5).

```text
Verdict: ship after changes (notes only).
Validity: USE-5 holds at fit approximate, the 0.99 wording overclaims (reword); LEAK-10 holds (RESTIONACEAE dropped);
  LEAK-26 holds (the cap is documented); SPLIT-1 and SPLIT-5 hold (the cell folds reproduce the mapping distances in
  Baviaanskloof); SPLIT-24 holds in effect ("exact" overstates); PROV-13: BioClimMAP30s is probably mislabelled, keep
  it with a note.
Value: TP-5 holds; MET-2 holds; MET-5/MET-11 fallback holds, the reason leaves out the paper's CRPSf prior selection.
For the curator: R1 and R2 below (wording), U1 (what 0.99 means in Baviaanskloof, Dryad file behind a token).
```

**Sources read:** the paper (arXiv:2112.07249v2, all 49 pages; the definition's page numbers checked); the repository
README at 97da77c; the GitHub commit list; the Cape of Good Hope species data (figshare 4737358, MIT, downloaded here:
`Slingsby_TaylorPlots.zip`, sheets `veg2010`, `traits`, `METADATA`); CHELSA V2.1 1981-2010 grids `bio1`, `bio5`,
`bio6`, `bio12`, sampled at the 180 plots; Open-Meteo elevations. The Dryad Baviaanskloof file (doi:10.5061/dryad.kk174)
returned 403 from the public stream, and its API needs a token: not read.

**Claims table**

| claim | source | test | result | evidence | rule |
|---|---|---|---|---|---|
| "exactly 0.99 in 12%, the release's code for full cover" | `task_summary.predicted` (README "Predicted") | counts on the raw file; the figshare 2010 species counts for the 57 Cape Point plots in both files; the plots whose two family covers sum above 1 | **refuted as worded** (the counts hold) | 21 plots at 0.99 (11.7%) holds. "Code for full cover" is stated as a fact, but the curation bullet itself says "most likely". In CP_2 both families sit at 0.99 (198 *Crassula fascicularis* counted, 171 restios). 3 of the 21 plots whose families sum above 1 have both covers below the code (BK_3: 0.96 + 0.78 = 1.74), while the paper calls the system "an open shrubland" (Sec. 1, p. 2). At Cape Point the Restionaceae plots at 0.99 hold between 82 and 3,497 counted individuals. All of this fits a ceiling on summed species covers as well as it fits full cover | USE-5, LEAK-26, EV-6 |
| the target is "the share of the plot covered by Crassulaceae" | `task_summary.predicted` | same as above | **contested** | family covers that sum to 1.74 with neither at the code fit summed species covers better than an area share. The definition's `fit_reason` already names the gap; the summary line states it as a fact | USE-5 |
| zeros are observed absences | curation bullet "Zeros" | presence in the independent 2010 species survey (Slingsby et al. 2017) against the release | **holds (stronger now)** | on the 57 Cape Point plots in both files, presence and absence agree on every plot for both families: Crassulaceae 14 present and 43 absent, Restionaceae 56 present and 1 absent. Paper quote (Sec. 1, p. 2) verified | USE-5 |
| 88 zeros (48.9%); 21 at 0.99 (20 in Baviaanskloof); next values 0.986, 0.961, 0.949; 71 other positives all distinct | curation bullets | counts on the raw file | holds | 88, 21, 20; 0.9859, 0.9607, 0.9492; 71 of 71 distinct; none above 0.99 | - |
| 21 plots sum above 1 over the two families (up to 1.98) | curation bullet "Anomaly" | raw file | holds | 21 plots (12 at Cape Point, 9 in Baviaanskloof), max 1.98; the Sec. 6 quote (p. 16) is verified, but it is about "a pair of species", not families | - |
| Crassulaceae over Restionaceae: the paper's focus; Restionaceae at 0.99 in 79 plots (56 of 61 at Cape Point); reserve-only skill 0.36 against 0.12 | curation bullet "Target" | raw counts; `target_choice.txt`; Sec. 5.2 | holds | 79, 56 of 61; 0.361 against 0.124; Sec. 5.2, p. 15: "The analyses presented here are for Crassulaceae; similar analyses for Restionaceae are provided in the Supplement" | PROV-6, USE-5 |
| RESTIONACEAE dropped (same survey) | bullet; `_clean` | definition | holds | the same relevé records both covers (Sec. 2) | LEAK-10 |
| `plot` is an id and its prefix repeats the reserve | bullet | crosstab | holds | BK = baviaanskloof on 119 of 119 rows, CP = cape_point on 61 of 61 | - |
| `BioClimMAP30s` is mean annual precipitation (30 arc seconds); "not millimetres... whatever the scale, it keeps the order of the sites" | bullets "Features" and "Anomaly: the unit" | values x 60; CHELSA bio1, bio12, bio5, bio6 at the plots; elevations | **refuted for Baviaanskloof** ("not mm/yr" holds) | In Baviaanskloof (119 plots, 191 to 1,470 m) Spearman is +0.99 with CHELSA mean annual temperature, -0.77 with CHELSA precipitation and -0.95 with elevation, while CHELSA precipitation rises with elevation (+0.67). Sanity check of the method: `tminave07c` against CHELSA `bio6` gives +0.86. At Cape Point the picture is mixed (bio12 -0.29, bio5 +0.67). The values are integers divided by 60 (1,031 to 1,312). So the column orders the Baviaanskloof sites like a temperature and against precipitation | PROV-13, EV-2 |
| `apan_mean_an` is mean annual evaporation; `tminave07c` and `RFL_CONC` as described; `RFL_CONC` is 41.5 at every Cape Point plot | bullet "Features" | paper Sec. 2 and 5.1; raw file; CHELSA | holds | the paper says "mean annual evapotranspiration" (Sec. 2) and "average annual potential evaporation" (Sec. 5.1), close enough. `RFL_CONC` = {41.5} at Cape Point. `tminave07c` against CHELSA bio6: +0.91 over all plots | - |
| the release holds raw values; nothing scaled over all rows | bullet "Features" | means and SDs | holds | evaporation mean 1,943.7, SD 86.9; the centring was the paper's, for its fits (Sec. 5.1, p. 14) | LEAK-30 |
| the group key is "exact": 108 cells of 1 to 5 plots, at most 1.6 km apart, 59 singletons | bullet "Grouped"; `grouping.definition` | arc-minute pixels from the coordinates (offsets scanned); RF on key groups against key-plus-pixel components | **holds in effect; "exact" overstates** | 108, 1 to 5, 1.63 km, 59 hold. Every key lies inside one coordinate pixel centred on whole minutes, but 4 pixels hold two keys because `RFL_CONC` (8 values) or the evaporation differs between plots 0.2 to 0.3 km apart (BK_111 and BK_112; BK_115, BK_116 with BK_3, BK_117). On the shipped folds 4.2% of test plots (at most 12.3%) have a training plot in the same coordinate pixel. Merged into 104 components, RF skill is 0.482 +- 0.018 against 0.449 +- 0.016 for the 108 keys: no measurable optimism | SPLIT-24, SPLIT-26 |
| "the 26 groups that share all four climate values lie inside these cells" | bullet "Grouped" | logic; 30-arc-second pixels | holds trivially | a four-value key contains the three-value key. By coordinates, the 150 four-value keys match 151 30-arc-second pixels, 97% one to one | - |
| cover "correlates at r = 0.53 to 0.90 under 1 km, 0.38 at 1 to 2 km and about 0 beyond 4 km" | bullet "Grouped"; `grouping.definition`; `splits_comment` | `geometry.py` read; Pearson correlation of the pairs recomputed | **holds in substance; the statistic is mislabelled** | the script averages products of z-scores, which is no correlation (it reaches -1.56 in one Cape Point bin). The Pearson correlation of pairs is 0.66, 0.66 and 0.58 under 1 km, 0.32 at 1 to 2 km, 0.23 at 2 to 4 km and -0.03 at 4 to 8 km | EV-8 |
| the split mirrors the use case: a test plot stands for an unsurveyed site; neighbouring cells stay in training | `task_summary.split`; `splits_comment`; implied SPLIT-1 | random sites in each reserve's plot hull: distance to the nearest plot, against test-to-train distances on the shipped folds | **holds** | Baviaanskloof (hull 744 km2): random sites median 1.61 km (p90 3.31), shipped test plots median 1.61 km (p90 3.45). Cape Point (hull 60 km2, Taylor's plots on a systematic 914 m grid per the figshare metadata): random sites 0.43 km, test plots 0.93 km, so the split is stricter than mapping there. Random folds put test plots a median 0.89 km away, with 26% within 0.5 km against 9.8% on the cell folds | SPLIT-1, SPLIT-5 |
| "some optimism for sites far from any survey remains" | `splits_comment` | coarser k-means blocks, 10 x 3 folds | holds | RF skill 0.531 random, 0.467 cell, 0.380 for blocks a median 2.0 km away, 0.345 at 2.8 km | SPLIT-4 |
| LightGBM 0.469 to 0.331; RF skill 0.48, above the mean on 30 of 30 splits | bullet "Grouped" | probe outputs; own re-run (other settings) | holds | probes match. Re-run: LightGBM 0.440 to 0.324, RF 0.531 to 0.467, RF above the mean on 30 of 30 | TP-2 |
| oracle 0.32 against RF 0.475; hurdle AUC 0.80 and R2 0.29 on positives | bullet "Zeros and cover" | `hurdle.txt`; RF re-run on the 60 splits | holds | matches; re-run RMSE 0.253 for RF against 0.353 for the mean | TP-2 |
| the 0.99 plots are 12% of test plots and 34% of an untuned RF's squared error | bullet "Anomaly" | second check with LightGBM | holds (for RF) | LightGBM: 11.8% of rows, 26.9% of squared error | MET-10 |
| metric fallback `rmse`; "several criteria, none named as the one that decides" | `metric = Metric.fallback(...)` | paper Sec. 3.4 and 5.1 to 5.3 read; 8 predictors ranked by RMSE and MAE on the 60 shipped splits | **holds; the reason leaves something out** | Sec. 5.1/5.2 pick the prior by CRPSf ("we ultimately select a prior which leads to the best CRPSf", p. 15), a tuning choice in MET-5's sense. But Sec. 5.3 compares five models on four criteria, and Sec. 3.4 (p. 10) says CRPSf cannot compare models with different zero structures, so there is no unique original. For a point forecast the CRPS reduces to absolute error. RMSE and MAE rank the 8 predictors with Kendall tau 0.86, RF first under both | MET-5, MET-11 |
| the metric can be computed on every fold | MET-2 (implied) | `scorer(container)` on mean and zero predictions per shipped fold; units per fold | holds | all 60 folds score: mean-predictor RMSE 0.276 to 0.423, no NaN; 36 cells, 46 to 72 rows and 9 to 33 Cape Point rows per test fold; no cell on both sides. No scoring columns needed, and `feature_columns` leaves out `climate_cell` | MET-2, TP-5 |
| README "origin: fallback: ... the source defines no metric" | generated README, Metric block | read | inaccurate (generated text) | the source reports four metrics; the reason says so | MET-11 |
| "The repository's README defines no metric" | metric reason | README at 97da77c | holds | two sentences, no metric and no column descriptions | MET-1 |
| source, year 2021, pinned commit, no licence | metadata | `commits.json`, `repo.json`, sha256 | holds | data added in 56db3d4 (2021-06-05 07:17), README in 97da77c (07:19). The raw file's sha256 equals the pinned copy's. GitHub licence: null | - |
| "one vegetation plot surveyed once in 2010-2011" | `task_summary.row` | figshare metadata; Dryad abstract | **inexact; years untested** | the Cape Point plots are Taylor's permanent plots, surveyed in 1966, 1996 and 2010. The Dryad Baviaanskloof study reports surveys in 1991/92 and 2011/12, against the paper's "2010 and 2011". The release holds one survey per plot | PROV-16 |
| every feature is known at the prediction point; no copy across the split | implied | definition; raw file | holds | coordinates, reserve and grid climate; 0 duplicate rows, 0 without the plot id | LEAK-10, LEAK-16 |
| TP-5: 46 to 72 plots, 16 to 40 zeros, 19 to 45 positives, 2 to 11 at 0.99 per test fold | builder claims | `nn_and_tp5.txt`; own fold counts | holds | matches | TP-5 |
| record field `required_split: Random (IID)` | record front matter | against the definition and the distance test | **inconsistent** | the definition ships grouped, and the test above supports grouped. The record field is stale (the builder's issue 5) | SPLIT-1, SPLIT-5 |
| builder lead: the Cape of Good Hope figshare data could repair the target | builder issue 2 | downloaded and compared | **refuted as a repair source** | the metadata says "Numbers indicate actual counts of individuals". One *C. fascicularis* individual maps to a cover of 0.003, 0.004, 0.017 or 0.023 in four plots, so the cover was estimated separately and cannot be rebuilt from the counts. Restionaceae Spearman on positives is 0.43 | PROV-13 |

**Refuted and untested, ranked (P1 first, Must first)**

1. **R1 (P3; USE-5, LEAK-26, Must).** `task_summary.predicted` states as facts "the share of the plot covered" and
   "the release's code for full cover". The data fits a ceiling on summed species covers just as well: CP_2 is at 0.99
   in both families, BK_3 sums to 1.74 with neither at the code, and the restio plots at 0.99 range from 82 to 3,497
   counted individuals. *What it changes:* what the curator reads the target to be, and whether 0.99 is a value of 1
   or a censored one. The rows stay (LEAK-26 is met by the note). *Mildest remedy:* reword the "predicted" line, for
   example: "The family's released cover, 0 to 0.99 ... exactly 0.99 in 12%, probably full cover or a cap on summed
   species covers (not documented)". Add the CP_2 and BK_3 facts to the "Anomaly" bullet.
2. **R2 (P5; PROV-13, Must; EV-2).** `BioClimMAP30s` is probably not mean annual precipitation. In Baviaanskloof it
   correlates +0.99 with CHELSA mean annual temperature, -0.77 with CHELSA precipitation and -0.95 with elevation, so
   "whatever the scale, it keeps the order of the sites" fails there. *What it changes:* the description of the
   feature the single-feature probe picks most often (13 of 30 splits). No leak, and the task does not change. The
   evidence is strong but circumstantial (one reference grid; WorldClim 1.4, the paper's source, could not be
   reached). *Mildest remedy:* keep the column as published and rewrite the bullet: labelled precipitation by the
   paper, it ranks the Baviaanskloof plots like mean annual temperature, identity not established, the values are
   integers divided by 60. Do not swap in CHELSA (PROV-14). One could ask the authors.
3. **R3 (P4; SPLIT-24, Must; wording only).** The group key is "exact" for 104 of 108 groups. 4 coordinate pixels
   hold two keys, and 4.2% of test plots share a pixel with a training plot, but merging them does not lower the
   score (0.482 against 0.449). *Remedy:* reword ("matches the arc-minute pixel of the coordinates except where
   `RFL_CONC` changes inside it"). Grouping on the 104 key-plus-pixel components is optional.
4. **R4 (procedure; EV-8, Should).** The correlogram's "r" is a mean product of z-scores. *Remedy:* give the Pearson
   values (0.58 to 0.66 under 1 km, 0.32 at 1 to 2 km, 0.23 at 2 to 4 km) or call it a Moran-type statistic. The
   conclusion does not change.
5. **R5 (P6; MET-11, Must; MET-5, Should).** The fallback reason leaves out that the paper selects its priors by
   CRPSf (Sec. 5.1, 5.2). The generated README says "the source defines no metric". *Remedy:* one more clause in the
   reason: CRPSf picks the paper's priors but cannot compare its models (Sec. 3.4), and for a point forecast it
   reduces to MAE, which ranks the probed models like RMSE (tau 0.86). Keep `rmse`.
6. **R6 (record).** `required_split: Random (IID)` contradicts the shipped grouped split. *Remedy:* the curator
   updates the field when deciding the builder's issue 1.
7. **U1 (P3/P5; USE-5, PROV-13), untested.** What 0.99 means for the target's 20 Baviaanskloof plots at the code,
   and whether family covers are summed species covers. The Dryad file (CC0) returned 403 and its API needs a token.
   *Next step:* download it by hand, or ask the authors. The Cape Point figshare data cannot settle it (counts, not
   cover).
8. **U2 (P5), untested.** The Baviaanskloof survey years: the paper says 2010-2011, the Dryad study 2011/12. The same
   Dryad file would settle it. It changes only the "row" line.
9. **U3, untested.** The published JABES text against arXiv v2 (the page numbers cited are arXiv's).

**Files**

- Scripts, in the run folder (not committed): `raw_checks.py`, `pixels.py`, `spatial.py`, `metric_rank.py`,
  `merged_groups.py`, `cp_species.py`, `cp_species2.py`, `chelsa.py`.
- Downloads, in the run folder: the paper (arXiv v2, PDF and text); the Slingsby figshare zip and its extracted
  sheets; the elevation and CHELSA samples at the plots.

</details>

<details><summary>Column audit</summary>

**Column auditor (AI, 2026-11-01): cape_floristic_region_family_cover**

**Verdict:** ship after changes to the text only. No kept column is a leak. Every feature is a site attribute that existed
before the 2010-2011 survey: the coordinates, the reserve, and four long-term climate grids. The two dropped columns
were the right ones to drop. The main finding is about the target. The data show that `CRASSULACEAE` is a fraction over
a per-plot quantity that it shares with `RESTIONACEAE`. So it is a relative cover, not "the share of the plot covered"
as `task_summary.predicted` says, and the 0.99 reading in the notes rests on that unverified reading.

Frame checked: `dataset_io.from_definition` (180 rows, 9 columns, rows shuffled). Raw file:
the pinned `cfr_zib_data.csv` in the local warehouse. Paper: arXiv:2112.07249v2 (Sec. 2, 5.1, 5.3,
6). Scripts are in the run folder (`load.py`, `describe.py`, `denominators2.py`, `cells.py`,
`single.py`, `map_pixel.py`, `quant.py`). The RF figures are random forests (300 trees, min_samples_leaf 3) on the 60
shipped splits, as skill against the training mean.

**Column table**

| column | meaning | known at prediction? | dtype and cleaning | verdict | rule |
|---|---|---|---|---|---|
| `CRASSULACEAE` (target) | Family cover from a 10 x 5 m relevé (paper: "percent cover"). On the data it is a fraction over a per-plot quantity shared with `RESTIONACEAE` (below), so a relative cover. 0.99 in 21 plots, meaning undocumented | target, recorded at the survey | float64, 0 to 0.99, no missing, no impossible values; the 0.99 cap kept and documented; no log (a share) | fine as a target with fit approximate; the text names the wrong quantity (problem 1) | USE-5, LEAK-26, PROV-13 |
| `latitude` | plot latitude, decimal degrees (datum not stated) | yes | float64, 5-8 decimals (trailing zeros dropped in 17 BK values), no missing | fine | CLEAN-14 |
| `longitude` | plot longitude, decimal degrees | yes | float64; two Cape Point pairs share a longitude, with different latitudes | fine | CLEAN-14 |
| `region` | the reserve: `baviaanskloof` (119) or `cape_point` (61) | yes | category, 2 levels; determined by longitude (18.4 against 24.0-24.5) but not an exact copy; the dropped `plot` prefix repeats it | fine | CLEAN-5, CLEAN-14 |
| `apan_mean_an` | Schulze (1997) mean annual A-pan potential evaporation, 1-minute grid. The paper calls it "mean annual evapotranspiration" (Sec. 2) and "average annual potential evaporation" (Sec. 5.1); no unit given, mm by range (1,687-2,110) | yes, a long-term grid | float64; one decimal stored through float32 (2057.600098); unscaled (x10 is an integer in 180 of 180) | fine | LEAK-30 (not triggered), CLEAN-21 |
| `tminave07c` | average minimum July temperature, deg C by name and range (BK 1.0-5.9, CP 8.0-9.5), 1-minute grid | yes | float64, one decimal through float32 (4.900000095), unscaled | fine | CLEAN-14 |
| `RFL_CONC` | rainfall concentration index, 0 (even) to 100 (one month); the paper says 1-minute grid | yes | float64, unscaled. Only 8 distinct values: 15.2 covers 58 plots over about 17 x 20 km, and 41.5 covers all 61 Cape Point plots (15 x 7 km), so its effective resolution is far coarser than 1 minute. RF without it: +0.002 (paired SE 0.001) | fine as a feature; it affects the group key (problem 2) | SPLIT-24, SPLIT-26 |
| `BioClimMAP30s` | paper: "mean annual precipitation (30 arc second)", by name a WorldClim/BioClim layer; unit unknown | yes, a grid: plots 0.07-0.5 km apart share a value while their covers differ | float64, unscaled. Every value is an exact multiple of 1/60 (printed to 4 decimals; n/60 with n = 1,031-1,312). That makes it a linear rescaling of an integer-valued layer, not a square root or log of millimetres. Its pattern fits precipitation (rises northward at Cape Point, Spearman 0.93 with latitude) | fine (no timing issue); its meaning is a question (problem 3) | CLEAN-21, EV-2 |
| `climate_cell` (group) | built in `_clean`: plots with the same `apan_mean_an`, `tminave07c`, `RFL_CONC` (108 levels, at most 1.63 km apart; the closest plots in different cells are 0.18 km apart) | split metadata | category (required: `dataset_object_dtype`); not a model input (README `n_features: 7`; `feature_columns` drops `group_on`). `ngroup` labels tuples and computes no statistic | fine | LEAK-33, LEAK-29 (not triggered) |
| `plot` (dropped) | plot id `BK_n` / `CP_n` | yes, but an id | The prefix is the reserve. The Cape Point number follows latitude (Spearman -0.99), so it encodes position, which the coordinates already give | dropped correctly | CLEAN-3 |
| `RESTIONACEAE` (dropped) | the other family's cover, same survey | no: recorded with the target | it also shares the target's per-plot denominator (below), so it comes from the same measurement as the label | dropped correctly | LEAK-10 |

**Problems, ranked (principles.md)**

**1. P3, USE-5 (Must, met through fit approximate and a note; the note names the wrong quantity), with PROV-13: what the
target is.**

`predicted` reads "The share of the plot covered by Crassulaceae". The anomaly bullet reads "0.99 most likely stands for
full cover recoded below 1". The data argue against both readings:

- *A shared denominator.* 23 Baviaanskloof plots have both families positive and below the code. In all 23, the
  smallest fractions that reproduce the two values (within float32 precision) have denominators that divide one another:
  10 are equal and 5 are double. For example, BK_113 is 55/372 and 175/372, BK_13 is 22/469 and 180/469, and BK_18 is
  110/1013 and 779/1013. When each plot's Crassulaceae value is paired with another plot's Restionaceae value, the ratio
  is a whole number 5.2% of the time (2.8% for equal or double). The Crassulaceae denominator, times 1 to 4, reproduces
  the Restionaceae value in 20 of 23 plots, against 4.3% under random pairing. So both values are amounts over one
  quantity measured per plot.
- *Not the plot area.* The reduced denominators run from 31 to 2,626, so the quantity changes from plot to plot. Under
  any fixed unit it would be constant for a 50 m² plot. The value is relative to something measured per plot.
- *Not the sum of all species' cover either.* Three plots below the code sum to more than 1: BK_3 is 660/687 + 535/687
  = 1.74, BK_51 is 1.36 and BK_76 is 1.01. Either the per-plot quantity is not the summed cover of all species, which
  would bound the two families at 1, or those rows hold errors.
- *The 0.99 code.* If the value is a ratio that can reach 1 or more, 0.99 may cap such values, as in min(x, 0.99),
  rather than code "full cover". The largest uncoded values are 0.986 (Crassulaceae) and 0.987 (Restionaceae). This is
  an inference: the data cannot tell a cap from a recode.
- *Score steps.* 41 of 56 Crassulaceae numerators are multiples of 11, and 36 of 45 Restionaceae numerators are
  multiples of 5. This hints that species scores were entered in fixed steps. It is a lead for the authors, not a
  finding.

*Remedy (mildest: keep with a note).* Keep the target, the rows and `fit="approximate"`. Rewrite four places:

- `predicted`, to something like: "Crassulaceae cover relative to a per-plot total that the source does not document, 0
  to 0.99".
- The Target bullet.
- The 0.99 bullet, with the shared-denominator numbers and the 0.99 reading as cap or code, unknown.
- `fit_reason`, so the gap is named as "the value is relative to an undocumented per-plot quantity", not only "how
  species covers were added".

The repair route stays as the builder drafted it: ask Tang or Frye. The species-level leads the builder found cover
other surveys or years, not this table.

**2. P4, SPLIT-24 / SPLIT-26 (Should; small effect): `RFL_CONC` in the group key.**

The key assumes all three covariates share one 1-minute grid. `RFL_CONC` takes 8 values, and it is the only reason for
4 of the 108 groups. In each of those 4, plots with the same `apan_mean_an` and `tminave07c`, 0.21, 0.29, 0.76 and 1.8
km apart, differ in `RFL_CONC` (for example 13.1 against 21.8 at 0.21 km), and so land in different groups. There are
two possible readings:

- The plots straddle a 1-minute cell boundary where the other two fields happen to be equal.
- `RFL_CONC` comes from a coarser layer that is not aligned with the 1-minute grid.

Keying on `apan_mean_an` and `tminave07c` alone gives 104 groups. *Remedy:* a question for the split auditor and the
curator. Either drop `RFL_CONC` from the key, or keep it and add a note. The effect is at most 4 near pairs.

**3. P7, CLEAN-21 / question: `BioClimMAP30s`, the strongest feature, has no verified unit.**

Alone it reaches an RF skill of 0.453 (SD 0.163), against 0.475 (SD 0.126) with all features; the paired difference is
0.022, SE 0.014. Without it the skill is 0.377. The 3-split probe had it at 0.393 alone, above the full model's 0.320.

This is not a leak: it is a grid value at the site, and plots in one pixel share it. But the benchmark leans on one
column whose meaning rests on the paper's one line. The 1/60 steps settle part of the existing anomaly bullet:

- The column is linear in an integer-valued layer, so it keeps the spacing of the sites as well as their order.
- No square root or log of millimetres produces these values.
- The spatial pattern supports precipitation.

*Remedy:* keep it as published, and add the 1/60 fact and the single-feature numbers to the anomaly bullet. No
transform, since no conversion is published.

**4. P7, wording only (no rule broken).**

- The notes give `RFL_CONC` as "1-minute", as the paper does. The data show a much coarser layer (8 values), and one
  clause would say so.
- `apan_mean_an` could be named "A-pan potential evaporation (by its name; the paper says evapotranspiration in Sec. 2
  and potential evaporation in Sec. 5.1)".

**What holds**

- LEAK-10: nothing recorded at or after the survey stays. `RESTIONACEAE` and `plot` are dropped, and there is no
  missingness (probe 3 empty).
- LEAK-26: the cap is documented.
- LEAK-30: all four climate columns hold raw values (one decimal, or 1/60 steps), not the paper's centred and scaled
  ones.
- LEAK-33: the group column is not a feature.
- CLEAN-3 and CLEAN-5: no id or exact copy is kept.
- CLEAN-9 and CLEAN-14: every column is typed by its meaning.
- CLEAN-23: the rows are shuffled.

**Judgment record**

```text
Verdict: ship after changes (text only).
Validity: USE-5 holds via fit approximate, but predicted/notes name a plot-area share the data contradict (relative to
  a per-plot quantity shared by both families, 23 of 23 plots); LEAK-10 holds (RESTIONACEAE, plot dropped; no kept
  column post-dates the survey); LEAK-26 holds (cap documented); LEAK-33 holds; SPLIT-24 minor (RFL_CONC alone makes
  4 of 108 groups).
Quality: CLEAN-21 BioClimMAP30s unit unverified (exact 1/60 steps, linear; carries most of the signal), kept as
  published; CLEAN-3, CLEAN-5, CLEAN-14, CLEAN-23 hold.
For the curator: rewrite predicted, the target and 0.99 bullets and fit_reason (problem 1); key on two covariates or
  note it (problem 2).
```

</details>

<details><summary>Split audit</summary>

**Split audit (split-auditor, 2026-11-01): cape_floristic_region_family_cover**

**Verdict: right with notes.** The regime is right: grouped by place, not temporal and not IID. Holding out whole
1-minute climate cells gives the Baviaanskloof test plots (two thirds of the rows) the same distances to the nearest
training plot as a random site inside the surveyed area has to the nearest of the 180 plots. The paper's random split
is clearly optimistic. Three notes: the key carries one covariate that is not on the 1-minute grid (4 grid cells are
split in two); the question's wording "a site whose climate grid cell has not been surveyed" describes sites farther
out than the test plots are; and two numbers in the notes need correcting.

```text
Validity: SPLIT-1 holds (grouped, measured against the prediction domain); SPLIT-3, SPLIT-7 hold (one survey, no
  stream, no time axis in the use case); SPLIT-5 checked (the paper's random split is optimistic, the departure is
  right); SPLIT-23 holds (one plot = one prediction, nothing known about a new cell); SPLIT-24 holds (exact key from
  the data); SPLIT-26 departure, small (RFL_CONC is not on the 1-minute grid: key on two covariates, 104 cells);
  SPLIT-28 holds (every family above the mean on unseen cells).
Notes: EV-8 (the split-gap numbers come from 3 folds, not 3 x 3); wording of the question and of splits_comment.
```

**How I checked.** I loaded the definition through `dataset_io.load(..., built=True)` (no build yet, so it was
rebuilt: 180 rows, 7 features plus the target and `climate_cell`, 20 x 3 splits). I verified the splits: no cell on
both sides in any of the 60 splits, every row tested once per repeat, 36 cells and 46-72 plots per test fold. I read
the paper (arXiv:2112.07249v2, Sec. 2, 3.5, 5.2, 5.3 and 6). All distances are haversine. Prediction domain: a 100 m
grid of points inside each reserve's convex hull of plots (750 km2 in Baviaanskloof, 61 km2 at Cape Point), scored by
distance to the nearest plot. This is the nearest-neighbour-distance matching used in spatial CV (Milà et al. 2022).
The quick models are untuned, with the probes' own settings. Scripts and outputs are in the run folder, not committed
(`a1_load_and_key.py` to `a6_lattice_key.py`, `a3_models.csv`).

**1. The regime and the prediction domain (SPLIT-1, SPLIT-3, SPLIT-5; P4, Must): holds.** The use case maps cover at
unsurveyed sites inside the two reserves, and the paper names that use: "Given an unobserved set of locations and
associated predictors, we can perform spatial prediction for percent covers at these locations" (Sec. 3.5, p. 10).
The plots come from one survey (2010-2011) with no dates, and the use case maps current cover, not a later year, so
nothing is temporal (SPLIT-7 does not apply). Distance from each test plot to its nearest training plot, against the
domain's distance to the nearest plot (km, quantiles p25 / p50 / p75, and the share under 1 km):

| Baviaanskloof (119 plots) | p25 | p50 | p75 | < 1 km |
|---|---|---|---|---|
| domain: any site in the hull | 0.95 | 1.63 | 2.50 | 27% |
| domain: sites in a 1-minute cell with no plot (75% of the hull) | 1.41 | 2.03 | 2.79 | 11% |
| random folds (the paper's protocol) | 0.31 | 0.77 | 1.62 | 59% |
| **shipped: 1-minute cells** | 0.92 | 1.62 | 2.26 | 30% |
| 2-minute blocks | 1.61 | 2.28 | 3.56 | 11% |
| 4-minute blocks | 1.97 | 3.26 | 4.19 | 6% |

* In Baviaanskloof the shipped split matches a random site of the surveyed area almost exactly. Random folds put test
  plots twice as close. Under random folds 45% of the Baviaanskloof test plots have a plot of their own cell in
  training, while only 25% of the hull lies in a surveyed cell. Within a cell, covers differ by 0.205 on average,
  against 0.400 for other pairs. So the paper's split (Sec. 5.3, "a training set of 99 locations and a test set of 20
  locations") rewards looking up a sampled patch more often than mapping would allow. The departure from it is right
  (SPLIT-5).
* At Cape Point the shipped split is pessimistic: test plots are a median 0.93 km from training, while the domain is
  0.43 km from a plot, and 94% of the hull lies in a surveyed cell. The cost is small. Crassulaceae shows no spatial
  autocorrelation there (0.01 to 0.12 at 0.5-4 km in the builder's correlogram) and is almost always near 0
  (within-cell |diff| 0.011, other pairs 0.065). A random forest's Cape Point skill is 0.66 on random folds and 0.61
  on cell folds.
* Caveat (cannot verify): the hull stands in for the reserves. The Baviaanskloof reserve is larger than the hull, and
  sites outside it would be farther from any plot than every test plot. `fit_reason` already limits the task to
  sites inside the two reserves.

**2. The group key (SPLIT-24 Must holds; SPLIT-26 Should, a small departure).** The key is exact from the data, not a
cluster, and Sec. 2 (p. 4) confirms the grids: "mean annual evapotranspiration (1-minute grid cell), mean annual
precipitation (30 arc second), average minimum temperature for July (...; 1-minute grid cell), rainfall concentration
index (1-minute grid cell ...)". The data shows that `RFL_CONC` is not on the same lattice as the other two:

* Grouping on `apan_mean_an` and `tminave07c` alone gives 104 groups. They equal a 1-minute lattice (cells centred on
  whole minutes) exactly: 0 groups span two lattice cells and 0 lattice cells hold two groups.
* Adding `RFL_CONC` splits 4 of these lattice cells, all in Baviaanskloof. In each, only the rainfall concentration
  differs (13.1 against 21.8, and 4.3 against 13.1) while evaporation and July minimum agree. Their plots lie 0.21,
  0.29, 0.76 and 1.8 km apart. `RFL_CONC` takes only 8 values (7 in Baviaanskloof, 1 at Cape Point), so it reads as a
  classed or differently aligned map.
* Each pair sits on opposite sides in 26-28 of the 60 shipped splits. The score effect is within the noise of drawing
  folds: random forest skill 0.461 on 20 x 3 draws of the shipped key against 0.495 on the lattice key, while two
  draws of the shipped key differ by 0.03 (0.461 against 0.489 on the shipped splits).
* Mildest remedy: group on `["apan_mean_an", "tminave07c"]`, which is the 1-minute cell itself. Then update the counts
  in `grouping.definition`, `curation_comments` and the code comment: 104 cells, 53 holding one plot, at most 1.8 km
  apart. The current comment, "plots with the same three values lie in one grid cell", is true, but the converse fails
  in 4 cells. The 26 groups that share all four values stay nested.

**3. The question describes sites farther out than the test plots (USE-1 and SPLIT-1 wording; P4, a note).** The
`question` and `task_summary.split` say a test plot stands for "a site whose climate grid cell has not been
surveyed". In Baviaanskloof such sites are a median 2.03 km from a plot, and 11% are within 1 km. The shipped test
plots are 1.62 km away, and 30% are within 1 km: they match any site of the surveyed area, not the unsurveyed cells.
At Cape Point only 6% of the hull is an unsurveyed cell. Two consistent ways out, for the curator:

* (a), recommended: keep the 1-minute cells, which follow SPLIT-26 (the resolution the climate features see) and
  match the whole surveyed area. Reword the question to "a site of the two reserves, with the surveyed plots of its
  own climate grid cell held out" or similar. `splits_comment` then states the optimism for sites in unsurveyed
  cells with the numbers above.
* (b): keep the question and hold out 2-minute blocks (57 groups, about 3.7 x 3.1 km), which match the
  unsurveyed-cell sites in Baviaanskloof (11% within 1 km in both). They are pessimistic at Cape Point, and the score
  drops: random forest skill 0.446 against 0.489, LightGBM R^2 0.274 against 0.374.

A split by reserve (2 groups) would test a domain shift, not a new site ("Only a few groups" factor, as in
covertype). Nobody proposes it.

**4. The quick models under each split (SPLIT-4, SPLIT-28; the scores never decide the split).** 60 splits each,
untuned. "Skill" is 1 - MSE / MSE of the training mean.

| split | random forest (task-probe settings), skill | LightGBM (group-probe settings), R^2 | kNN-5 on coordinates only, skill (Baviaanskloof) |
|---|---|---|---|
| random folds | 0.545 | 0.434 | 0.233 (0.158) |
| **1-minute cells (shipped)** | 0.489, above the mean on 60 of 60 | 0.374 | 0.100 (-0.020) |
| 2-minute blocks | 0.446 | 0.274 | -0.045 (-0.210) |
| 4-minute blocks | 0.233 (default forest) | 0.268 (default) | -0.013 |

The cell split removes the pure interpolation from neighbours (kNN on coordinates drops to about the mean in
Baviaanskloof). The climate signal survives, so SPLIT-28 holds. The ranking of the families keeps the forest on top
under random and cell folds. It compresses as the blocks grow.

**5. Numbers in the notes (EV-7, EV-8; a wording fix).**

* `curation_comments`, grouping bullet: "Untuned LightGBM R^2 falls from 0.469 on random folds to 0.331 on the cell
  folds (group_probes.py, 3 x 3 folds)". The probe's split gap compares one 3-fold random run with the first repeat's
  3 cell folds (`groups.py`, lines 185-187); only its learnability uses 3 x 3. I reproduce 0.469 and 0.331 on those
  three folds each. On all 60 shipped splits against 60 random ones, the same LightGBM gives 0.434 against 0.374 (a
  gap of 0.06, not 0.14). Suggest: "falls from 0.43 on random folds to 0.37 on the shipped cell folds (60 splits
  each)". The random-forest clause (0.48, above the mean on 30 of 30) holds: 0.484 on the first 30 splits and 0.489
  on all 60.
* The "correlates at r = ..." figures are the mean product of covers standardised within the reserve, over the plot
  pairs of each distance band (a Moran-type autocorrelation). They rest on 19, 23 and 40 pairs in the bands under
  1 km. Call it autocorrelation and give the pair counts. `splits_comment` also skips the 2-4 km band (0.22, 300
  pairs), the band most cell-split test plots look across (Baviaanskloof p75 2.26 km). It belongs in the sentence on
  residual optimism.
* "about 1.9 x 1.6 km": one minute is 1.85 km of latitude and 1.54 km of longitude at 33.6 degrees S, so 1.9 x 1.5 km.
* The record still reads `required_split: Random (IID)`. The builder's draft issue 5 already flags it: Grouped
  (NON-IID).

**Checked and fine.** Group-side composition: each test fold holds 36 cells, 16-40 zeros, 19-45 positives, 2-11
plots at 0.99 and 9-33 Cape Point plots (`nn_and_tp5.txt`, re-derived from the splits). This is no `Too Small` concern
for the split. The hidden-group hit `(all but latitude, longitude)` is the 30-arc-second key (150 keys), nested in the
cells by construction. No cell mixes the two reserves. Precedents in this run group on the natural spatial unit and
state the leftover optimism the same way (`boreal_postfire_lichen_biomass` by site, `wadden_sea_sibes_macoma_abundance`
by station). Here there is no site id, so the grid cell is the exact unit the data gives.

</details>

<details><summary>Domain practitioner</summary>

**Domain practitioner: cape_floristic_region_family_cover**

Actor played: a reserve ecologist planning monitoring, fire management or protection in the two reserves the data covers. These are Table Mountain National Park, Cape Point section (SANParks), and Baviaanskloof Nature Reserve. Baviaanskloof is run by the Eastern Cape Parks and Tourism Agency (ECPTA), not CapeNature. I need the expected Crassulaceae cover at sites nobody has surveyed.

**Verdict: fit approximate (agree with the definition).** I would use the predictions as a coarse screening layer inside these two reserves. But the label is a family "cover" whose scale nobody documents (the 0.99 code, sums above 1, and maybe a different measurement at Cape Point). The inputs also leave out the vegetation type, terrain and fire age that I have for every site (USE-5, USE-8).

**How the decision is made today**

Conservation planning in the Cape works from mapped vegetation types, points for threatened species, and surrogates for ecological processes, which Marxan turns into Critical Biodiversity Areas (CapeNature's Western Cape Biodiversity Spatial Plan). Reserve managers set fire and monitoring plans; UNESCO's state-of-conservation reports for the Cape Floral Region name fire and invasives as the main concerns. A family-level cover map is not a standard planning layer. It is plausible as one ecological layer, though: the paper calls Crassulaceae likely "fire avoiders" that are more abundant on rocky outcrops and at sites that burn less often (Sec. 5.1, p. 15). So a map of succulent-dense sites tells me where fire refugia and succulent-rich stands are, and where to put new plots. The definition's use case ("choose where to survey or protect succulent-rich vegetation", marked "for example") is a fair USE-1 statement. The source names prediction to unobserved sites but no actor.

**1. Inputs at the moment of prediction**

- Have: latitude and longitude, the reserve, and the four climate grids. These are long-term WorldClim and Schulze (1997) atlas values, readable at any point.
- Would not have: `RESTIONACEAE`. It comes from the same survey, and the definition is right to drop it (LEAK-10). The plot id is rightly dropped too.
- Missing, though I would always have them:
  - The mapped vegetation type (SANBI VegMap). Baviaanskloof mixes fynbos, thicket and karroid shrubland, and Crassulaceae belong to the latter two.
  - Terrain from a DEM: elevation, slope, aspect, ruggedness. The paper names rockiness as a driver.
  - Time since fire and fire frequency from the reserve's fire records. The paper names fire frequency. Slingsby's Cape Point release already carries `Age2010` and `firecount66_10` per plot.

  So the task is "predict from climate and position only". That is a narrower task than the one I would build, but still a real one: climate-envelope habitat layers are a common product. It is not a leak and needs no fix (USE-6, USE-12). I note it as a gap in how far the features mirror the use case (USE-8), not as a defect.

**2. The target: what I act on, or a proxy?**

It is a proxy, and its scale is unclear (USE-5).
- The paper says the covers are relevé "percent cover" (Sec. 2, p. 4). Yet 21 plots sit at exactly 0.99, 20 of them in Baviaanskloof.
- Literally full cover of a 50 m^2 plot by one succulent family, at 1 plot in 6 in Baviaanskloof, is ecologically implausible. Summed species covers capped below 1 is more likely, and 21 plots sum above 1 across the two families.
- At Cape Point the values may not be visual cover at all. I matched the claim-auditor's download of the 2010 Taylor-plot resurvey (Slingsby et al. 2017, figshare 4737358) to the release (scratch `cp_scale.py`):
  - The 2010 matrix holds counts (0 to 2,050 per species), not cover.
  - Presence agrees in 57 of 57 matched plots, and the ranks agree at Spearman 0.93 on the 14 positive plots.
  - One individual maps to anything from 0.003 to 0.023. CP_2's 198 *Crassula fascicularis* map to 0.99.
  - So the Cape Point "cover" is a separate estimate, or counts scaled by plant size and capped. Nothing documents which. This is a lead, not a finding (EV-6).
- A number (expected cover) is right for a map. A probability of presence is what I need where the family is trace (see point 3).

`task_summary.predicted` calls 0.99 "the release's code for full cover" as a fact. The curation notes call it "most likely", and neither the paper nor the repository says. The summary should say "most likely" too.

**3. Does one row match one decision? Is the test data what I face?**

- Unit: I act on a map cell or a management block, not a 10 x 5 m relevé.
  - Within one 30-arc-second pixel, plots differ by a standard deviation of 0.105, against 0.35 overall (`geometry.txt`, 26 pairs). Micro-site variation sets a low ceiling that no climate grid can reach.
  - Relevé plots are placed in homogeneous stands, not at random map points, so the test plots are not the random sites a map is applied to.
  - Sibling precedent: crms_phragmites_cover names "a manager acts on sites rather than 4 m^2 plots" in its `fit_reason`.
- Test data: whole 1-minute climate cells held out. The nearest training plot is a median 1.27 km away (`nn_and_tp5.txt`). That matches my real case, a gap between survey clusters inside my reserve (USE-10: a new site, a cold start, so a grouped split). A new reserve is not represented, and `fit_reason` says so.
- The two reserves pose different tasks. I scored out-of-fold predictions over 10 shipped repeats (scratch `within_reserve.py`), measuring skill against the reserve's own training mean:

| | Baviaanskloof | Cape Point |
|---|---|---|
| Plots | 119 | 61 |
| Zero | 43 | 45 |
| At 0.99 | 20 | 1 |
| Mean cover | 0.30 | 0.033 |
| Cover skill, RF / hurdle | 0.43 / 0.42 | 0.08 / 0.10 |
| Presence AUC | 0.69-0.72 | 0.76-0.78 |

  At Cape Point, 12 of the 16 plots with any cover are below 0.05. There, cover is barely predictable and my decision is presence. The pooled RMSE mostly scores Baviaanskloof and the contrast between the reserves; the reserve mean alone has skill 0.11.

**4. Would I use this model?**

- In Baviaanskloof: yes, as a screening layer to place new plots or flag likely succulent-dense stands. It beats the reserve mean by about 0.43 skill and ranks presence at AUC 0.7.
- At Cape Point: only the presence ranking.
- What would make me distrust it:
  - I cannot tell a truly dense plot from a capped sum. Without the 0.99 plots, the RF's Baviaanskloof skill falls from 0.43 to 0.19 (the hurdle's to 0.34).
  - The family sums above 1.
  - The undocumented scale of `BioClimMAP30s` (17 to 22, not mm per year). It costs nothing for trees, but I could not read it on a map.
  - Two reserves, surveyed 2010-2011. Fynbos cover moves with post-fire age, so the prediction is a long-run expectation, not today's cover.
- What would make me trust it more: species-level sums from the source surveys, and fire age and terrain as inputs.

**5. Does the declared metric score my decision?**

Partly. The declared metric is `rmse`, the fallback.
- What it gets right:
  - My map shows expected cover, and squared error is a consistent scoring function for a mean.
  - The paper has no single deciding metric: Tjur's R2, AUC and two CRPS variants side by side (MET-5).
  - The paper fixes no threshold, k or cost (MET-6, MET-7). I would not invent a top-k.
  - The CRPS needs a predictive distribution that point predictions cannot give.
  - In abundance distribution modelling, accuracy, discrimination and calibration are read separately and no single number decides (Norberg et al. 2019; Waldock et al. 2022).
- What it misses (60 shipped splits, five untuned models, scratch `practitioner_probe.py`):
  - RMSE ranks models against Spearman at mean Kendall tau 0.37, and against presence AUC at 0.33.
  - The 0.99 plots decide the winner. RMSE picks RF on 28 splits and the hurdle model on 27. Without the 0.99 plots the hurdle wins 44 of 60 and RF 3. The two tie on mean RMSE (0.253).
  - On the shipped folds the 0.99 plots are 12% of the test plots and 34% of RF's squared error (builder's `hurdle.txt`).
- What I would choose: keep `rmse` (MET-8). MAE would pull predictions to the median, which is 0 at half the sites. Spearman cannot be mapped as cover. Neither suits my decision better.
- Add to the metric reason (MET-10): the 0.99 plots carry about a third of the squared error and decide RF against hurdle. A user should read presence AUC beside RMSE.

**Gaps between the dataset and the real decision, ranked by how much they change the task**

1. The label's construction is undocumented (USE-5, USE-8; PROV-13 lead). The 0.99 code, sums above 1, and possibly a count-based estimate at Cape Point change what "cover" means, and they decide which model wins under RMSE.
2. Missing standard inputs: vegetation type map, DEM terrain, fire age. The paper names rockiness and fire as drivers. The task becomes "climate and position only": harder, still real.
3. Unit and sampling: a 50 m^2 relevé placed in a homogeneous stand stands in for a map cell. The within-pixel standard deviation of 0.105 is irreducible.
4. Two different tasks pooled: Baviaanskloof is a cover task, Cape Point a presence task (cover skill about 0.1). One pooled RMSE hides this. The summary is honest about the two reserves but not about this.
5. A 2010-2011 snapshot against a planner's present, with post-fire age not in the inputs. Small with static climate inputs.
6. The test stands for an unsurveyed cell inside the two reserves, not a new reserve. Already stated in `fit_reason`; small.

**What an expert would change**

- Now, no decision needed:
  - In `task_summary.predicted`, say "most likely the code for full cover; undocumented" instead of stating it as fact.
  - In `fit_reason`, add that the inputs lack the vegetation type, terrain and fire age a reserve ecologist has.
  - Once the claim-auditor confirms it, also add that the Cape Point values may be a count-based estimate.
- For the curator (a rebuild, a curator's call; `rebuild.md`):
  - Rebuild from the species-level surveys: Baviaanskloof percent cover with environment from Dryad doi:10.5061/dryad.kk174 (Aiello-Lammens et al. 2017), and Cape Point from figshare 10.6084/m9.figshare.4737358 (Slingsby et al. 2017; MIT; `Age2010`, fire counts).
  - That would document the family sum, settle the 0.99 cap, and add fire age as an input known at prediction time. The ORNL BioSCape trait and relevé release (GCFR relevés 1966-2014, Frye and Silander) is another lead.
  - DEM terrain at the coordinates is a cheaper enrichment, below the label fix in priority.
- Keep as is:
  - The drop of `RESTIONACEAE` (LEAK-10) and the plot id.
  - The choice of Crassulaceae. Restionaceae sits at 0.99 in 56 of the 61 Cape Point plots, which is even worse for a practitioner.
  - The cell grouping. It matches my "gap between surveys" case (USE-10). Coarser blocks are the split-auditor's question.
  - `rmse`, with the MET-10 note above.
- Consistent with siblings: crms_phragmites_cover and boreal_postfire_lichen_biomass are both approximate, both use the fallback metric, and both name the plot-versus-site gap.

**Sources**

- Tang, Frye, Gelfand, Silander, arXiv:2112.07249v2 (Sec. 1, 2, 5.1-5.3, 6); the claim auditor's copy in the run folder.
- Slingsby et al. 2017 data, figshare 10.6084/m9.figshare.4737358 (veg2010, traits, enviroment.csv, S3.Rmd); the claim auditor's download in the run folder.
- Dryad doi:10.5061/dryad.kk174 (Aiello-Lammens et al. 2017, Baviaanskloof percent cover, trait and environment data): https://datadryad.org/dataset/doi:10.5061/dryad.kk174
- SAEON Fynbos Node: https://fynbos.saeon.ac.za/?p=3201
- ORNL BioSCape foliar trait and relevé data: https://daac.ornl.gov/cgi-bin/dsviewer.pl?ds_id=2482
- CapeNature WCBSP: https://www.capenature.co.za/western-cape-biodiversity-spatial-plan and https://capenature.co.za/uploads/files/Resources/A-Summary-Overview-of-the-Biodiversity-Spatial-Plan_web.pdf
- Baviaanskloof management (ECPTA): https://www.rufford.org/projects/silvia-weel/wildlife-habitat-assessment-in-the-baviaanskloof-nature-reserve-supporting-wildlife-management-in-a-world-heritage-site/ and https://en.wikipedia.org/wiki/Baviaanskloof_Mega_Reserve
- UNESCO state of conservation, Cape Floral Region: https://whc.unesco.org/en/soc/4136/ and https://whc.unesco.org/en/soc/1067
- Norberg et al. 2019, Ecol. Monogr. 89:e01370: https://serval.unil.ch/notice/serval:BIB_7CFA0F77A70A
- Waldock et al. 2022, Ecography e05694: https://archimer.ifremer.fr/doc/00740/85251 (scope only; its metric definitions not read)
- Builder probes (run folder): `hurdle.txt`, `nn_and_tp5.txt`, `geometry.txt`.
- My scripts, in the run folder:
  - `practitioner_probe.py`: 60 splits, five models, metric agreement.
  - `within_reserve.py`: pooled within-reserve skill, 10 repeats.
  - `cp_scale.py`: Cape Point values against the 2010 counts.

</details>

<details><summary>Blind review</summary>

**Verdict: exclude as prepared.** The data are real field data, the split is honest and there is real signal. But with 180 rows, 108 groups and seven usable features, the dataset is too small and too narrow to rank tabular methods reliably. If the benchmark has an explicit small-data slice, include it only with changes 2 to 5 below.

**What the task is**

The task predicts how much of a 10 x 5 m relevé plot (a standard vegetation survey plot) in South Africa's Cape Floristic Region (CFR) is covered by the succulent family Crassulaceae. The target is a proportion from 0 to 0.99. The inputs are four gridded climate covariates, latitude and longitude, and the region. There are two regions: Baviaanskloof (119 plots) and Cape Point (61 plots), surveyed 2010-2011. A CFR ecologist or conservation planner would make this kind of prediction when mapping a family's abundance or projecting it under climate change. That is a real use (species distribution and abundance modelling).

This table, however, is the demonstration data of a statistics methods paper: Tang, Frye, Gelfand and Silander, "Zero-inflated Beta distribution regression modeling", JABES 2022 / arXiv 2112.07249. It is not an operational dataset. The authors chose the four covariates. Their spatial analysis used Baviaanskloof only, because "Baviaanskloof and Cape Point are disjoint and too far apart geographically".

**Concerns, most to least serious**

1. **Too small, with too little room for methods to differ.**
   - 180 rows. Each 3-fold test fold holds about 60 rows from about 36 cells.
   - Per-fold R² under the given grouped 20x3 scheme (my reruns): ridge 0.40 ± 0.13, ExtraTrees 0.44 ± 0.13, random forest 0.43 ± 0.15, LightGBM 0.37 ± 0.21. Single folds range from -0.15 to 0.78.
   - The fold-to-fold spread of paired model differences (sd 0.07-0.13) is larger than the average gaps (0.01-0.07). ExtraTrees beats random forest in only 55% of folds.
   - There are only 7 informative features, mostly coarse 1-arc-minute climate values. apan_mean_an has 103 distinct values over 180 plots. RFL_CONC has 8 distinct values and is a constant 41.5 across all of Cape Point.
   - A plain ridge regression already reaches pooled R² 0.42 (ExtraTrees 0.46).
   - What I would change: leave it out of the main benchmark. At most, put it in a small-data slice that uses many repeats and paired tests.

2. **The grouping removes exact climate copies but not spatial autocorrelation.**
   - `climate_cell` is exactly the distinct (apan_mean_an, tminave07c, RFL_CONC) triple. There are 108 groups, every cell is constant in these three columns, and no triple is split across cells. Grouping on it therefore keeps the 30 rows that share all four climate values with another row on the same side of the split. That part is good.
   - Plots in neighbouring cells are still close and similar. The nearest plot in another cell is a median 0.97 km away (55% are under 1 km, 14% under 0.5 km). A plot's cover correlates 0.54 with that neighbour's cover.
   - Pooled R² for ExtraTrees / random forest: random 3-fold 0.53 / 0.53, grouped by cell 0.46 / 0.45, spatial k-means blocks (12-24 blocks) 0.39 / 0.35-0.41. The paper itself reports that adding spatial random effects improves prediction, which points to leftover spatial structure.
   - The real use is predicting cover at new, unsurveyed sites. Spatial blocks of roughly 2-5 km would match that better than 1-arc-minute cells.
   - Holding out a whole region is not workable: the two regions do not overlap in July minimum temperature (1-5.9 vs 8-9.5 °C) or in RFL_CONC (1-21.8 vs 41.5).
   - What I would change: build groups from spatial blocks instead of climate cells.

3. **`climate_cell` must not be used as a feature.**
   - task.md counts 9 columns including the target, so unless the harness strips the group column, `climate_cell` is one of the 8 features.
   - It is a 108-level category. Under grouped CV every test level is unseen in training, so it acts as a pure ID.
   - Adding the cell code lowered LightGBM's pooled R² from 0.398 to 0.374. Random forest was unchanged (0.451 vs 0.453).
   - What I would change: drop it from the features and keep it only as the split key.

4. **The target definition is not documented, and it is capped at 0.99.**
   - The repo README says only "percent cover abundance data for Crassulaceae and Restionaceae plant species". The paper says plots were "sampled for its floristic composition using observations of percent cover" and that the data lie on [0,1).
   - The values look like ratios of integers rather than raw percent: 0.985915 = 70/71, 0.405405 = 15/37, 0.104265 = 22/211. The numerators are often multiples of 11 (11, 22, 44, 55, 110, 220, 264, 396, 440). So the column is some normalised quantity.
   - 21 plots (11.7%) sit exactly at 0.99 and none is higher. That is a cap imposed for the Beta likelihood, so 0.99 stands for "at least 0.99" (probably 1).
   - In the source, Crassulaceae plus Restionaceae exceeds 1 in 21 plots, so the value is not a share of total cover. Restionaceae sits at 0.99 in 79 of 180 plots.
   - The target is bimodal: 48.9% exact zeros and 11.7% at the cap. Cape Point is 74% zeros with mean 0.033, so in practice the task is about Baviaanskloof.
   - Squared-error regression can live with this. What I would change: document the column as "family cover proportion, censored at 0.99, zero-inflated".

5. **`BioClimMAP30s` is probably mislabelled, or its units are unknown.**
   - The paper describes the 30-arc-second covariate as mean annual precipitation from WorldClim.
   - The values run from 17.18 to 21.87. That is impossible in mm for these sites, where annual rainfall is in the hundreds of mm.
   - Within Baviaanskloof it correlates +0.74 with July minimum temperature and +0.69 with pan evaporation. That pattern fits a temperature variable, or a transformed one, not rainfall.
   - It does not break the prediction task: trees ignore monotone transforms, and linear models are unaffected. It does make the documentation wrong.
   - What I would change: describe it as "WorldClim 30s covariate labelled MAP; units unverified".

6. **Minor preparation points.**
   - Types are sensible: 6 float columns and 2 categories (`region`, `climate_cell`). There are no missing values.
   - The prepared table matches the source CSV exactly: all 180 rows join on coordinates, with a maximum absolute difference of 0 on every shared column.
   - The plot ID and the co-measured RESTIONACEAE column were correctly dropped. RESTIONACEAE would not be known at prediction time and correlates -0.58 with the target.
   - Float32 artefacts such as 2037.699951 are harmless.
   - The column names are cryptic. I would rename them: A-pan mean annual evaporation, mean July minimum temperature, rainfall concentration index, the 30s WorldClim covariate.
   - If the benchmark also has a RESTIONACEAE task built from the same table, the two would be near-duplicate datasets.

**Checks that passed**

- **Leakage:** none found. Every feature is a static climate grid value or a location, all known before a survey.
- **Real data:** the table matches the paper: 61 Cape Point and 119 Baviaanskloof plots; the paper says "49% of the observations for Crassulaceae ... are 0" and this table has 48.9%.
- **Signal, and the task is not trivial (grouped CV, pooled R²):**

| Model | R² |
|---|---|
| Overall mean | -0.02 |
| Region mean | 0.11 |
| kNN on coordinates only | 0.07 |
| Random forest on climate only | 0.41 |
| All features | 0.40-0.46 |

**What I could not check**

- I could not read the paper PDF directly (no PDF tools on this machine). I used the ar5iv HTML through a summarising fetch, so the quotes are as relayed. I did not see the supplementary table S10 with the paper's own out-of-sample scores.
- I could not check how the family-level value was computed from the relevés. The raw relevés are not public in the repo.
- I could not confirm the source and units of the four climate grids. A web search for the column names found nothing.
- I don't know whether the benchmark harness removes the group column from the features.
- There is no elevation or microhabitat information, so I could not judge how much better a richer feature set would do.

I did not open any files outside the clean room and the public sources, and did not come across any by accident.

Sources: https://github.com/beckytang/ZIB_data , https://raw.githubusercontent.com/beckytang/ZIB_data/main/cfr_zib_data.csv , https://arxiv.org/abs/2112.07249 , https://ar5iv.labs.arxiv.org/html/2112.07249 , https://doi.org/10.1007/s13253-022-00516-z (not opened, paywalled).

</details>

<details><summary>Precedent check</summary>

**Precedent check (precedent-checker, 2026-11-01): cape_floristic_region_family_cover**

Read: this run's decision register (`register.json`, 1,620 decisions, 14 flags), the Cases tables of `splits.md`,
`leak_checks.md`, `provenance.md`, `metrics.md` and `task_probes.md`, the record, and the sibling records and
definitions (spatial splits, plant-cover surveys, tiny tables, capped targets, files with two targets).

**Verdict.** Four of the six choices follow curator precedents directly. The other two each have a curator precedent
that went the other way. In both, the facts that set this case apart can be seen in the data, but the definition does
not write them down. That makes two prompts:

1. The grouping by 1-minute climate cell follows superconductivity, airfoil_self_noise and concrete_compressive_strength
   (SPLIT-4, SPLIT-24, SPLIT-26), and the definition gives a reason for departing from the paper's random split
   (SPLIT-5). But the only spatial splits a curator has settled are IID: covertype (Lennart, 2026-10-01) and houses
   (Lennart, legacy comment).
2. Keeping the 0.99 code with a note is one of the two remedies LEAK-26 allows, and sat11_hand_algo_runtime did the
   same. But houses dropped its capped rows even though its own notes give the reason this definition uses for keeping
   them.

Drift: none on these rules from the same curator, apart from one legacy remark Andrej made on houses (imported
2026-06-24): "Currently, we do not include spatial data as non-iid. Might change that." No reason has reached its third
exception. None of the register's 14 flags involves these rules.

| Decision | Status | Closest precedents |
|---|---|---|
| Grouped by the 1-minute climate cell | departs from the paper (reason given) and from the record's AI field; differs from two curator-settled spatial IID cases (prompt 1) | superconductivity (SPLIT-4, 2026-10-06); airfoil_self_noise (SPLIT-1, SPLIT-24, Lennart, 2026-10-20); concrete_compressive_strength (SPLIT-24, 2026-10-14); kick, appliances_energy_prediction (SPLIT-5); emscad, maternal_health_risk (SPLIT-24, barred keys); covertype (Lennart, 2026-06-23 and 2026-10-01); houses (Lennart, 2026-06-24); open_soil_data (Lennart, 2026-09-23) |
| 0.99 code kept with a note | consistent with LEAK-26 and sat11; departs from houses, and the reason given is one houses also weighed (prompt 2) | houses (LEAK-26 Cases); sat11_hand_algo_runtime (2026-10-14); PROV-13 Tensions row; aeolus (2026-10-26) |
| `RESTIONACEAE` dropped | consistent | caracas_cervical_cancer (LEAK-10, Lennart, 2026-10-15); noaa_afsc_bottom_trawl_survey_cpue (this run) |
| Crassulaceae as the target, no second folder | consistent | rosbank1 (PROV-6, Lennart, 2026-10-26); arsenic_male_lung (PROV-6); caracas_cervical_cancer |
| `rmse` fallback | consistent | gallstone_disease, early_stage_diabetes_risk_prediction (MET-5); metric Tensions row (Lennart, 2026-10-21) |
| 180 rows | consistent | musk kept (TP-5, 2026-10-06); parkinsons_biomedical_voice_measurements retired (TP-5, 2026-10-05); alvin retired (TP-8, 2026-10-12) |

**1. Grouped by the 1-minute climate cell (SPLIT-1, SPLIT-5, SPLIT-24, SPLIT-26)**

* The record: `required_split: Random (IID)` is the AI screening's field. The screening itself left the question open
  ("To check: ... spatial blocks instead of random splits"). Andrej's CC of 2026-10-30 gives `Yes`, priority 1, and says
  nothing about the regime. A measured finding from a later stage supersedes a screening reading (principles,
  Precedence, Stages), so this departs from no curator decision.
* The paper: under SPLIT-5 a paper's split is a claim to check (kick: 78.9% of the test locations of a split called
  grouped were also in train). The reason given: Baviaanskloof plots are a median 0.5 km from their nearest neighbour,
  cover correlates at r = 0.53-0.90 under 1 km, and the use case is a site with no survey. One caveat: below 1 km the
  `geometry.txt` correlogram rests on only 19-40 pairs per distance bin. SPLIT-19 (Should: follow the source's split)
  sits in the temporal section and talks about official periods. Even read broadly, the stated fact together with
  SPLIT-1 (Must) supplies what a departure from a Should requires.
* The key: it is exact. It is built from three columns that the source describes as 1-minute grids, and no two plots
  sharing a key are more than 1.63 km apart, so distant plots never share one by coincidence. That separates it from
  maternal_health_risk (a feature-vector hash standing in for an unknown entity, barred) and from emscad (a similarity
  cluster, barred). It is coarser than the 30-arc-second pixel the hidden-group probe found, in the same way
  airfoil_self_noise was grouped by setup rather than by run because a new setup is the query. Consistent with SPLIT-24
  and SPLIT-26.
* The spatial cases a curator has settled:
  * covertype ships random cells, as its source does, for "mapping the cover type of cells inside the studied areas
    that have no inventory". The written reasons (CC 2026-10-01) are that a leave-one-area-out split had only 3 groups
    (the "Only a few groups" factor) and that "the data has no coordinates to split by". Neither applies here: this
    dataset has coordinates and 108 cells. The earlier CC (imported 2026-06-23) gives another reason: "one would collect
    samples randomly across the studied area, and afterwards try to fill the gaps to predict unseen areas". That fits a
    reserve ecologist as well, and the definition does not say why it does not apply.
  * houses ships random block groups with their neighbours in training, although its `fit_reason` frames the task as
    "valuing areas where no value is known". Lennart's comment (imported 2026-06-24): "it would count as IID as spatial
    information are not leaking"; Andrej's in the same thread is quoted above.
  * open_soil_data (Lennart, 2026-09-23, a `No`): for point data mapped from covariates, "grouped (spatial) is the
    applicable regime".
  Taken together: IID where the data cannot be split spatially (covertype) or covers every unit (houses), and spatial
  grouping named as the regime for mapping from points (open_soil_data). No rule says this. If shipped, this would be
  the first dataset grouped on a purely spatial block. This run's siblings group on a unit the source defines (stations
  revisited yearly, segments of the source's survey grid, sites); here the cell comes from the covariate grids and holds
  distinct plots, each surveyed once.
* Coarser blocks, the builder's option: SPLIT-24 allows a fixed grid on the coordinates or a unit the source defines. It
  does not allow a distance-threshold or k-means cluster (emscad).
* If the curator accepts the grouping, two entries become due: a SPLIT-24 Cases row (the first spatial grid key) and a
  Tensions row (gap-filling inside a surveyed area against prediction at unsurveyed sites).

**2. The 0.99 code kept with a note (LEAK-26, PROV-13)**

* LEAK-26 (Must) allows two remedies: drop the capped rows or document the cap. The definition documents it.
* houses drops its cap of 500,001 ("a censored value"), although its `fit_reason` says "Dropping the capped rows leaves
  out the most expensive areas, which such a use would meet". This definition keeps its 21 plots because "dropping them
  would remove the densest succulent sites", which is the same argument houses weighed and set aside.
* sat11_hand_algo_runtime keeps 666 timeouts at the cutoff, because the cutoff preserves the order within an instance,
  and drops the 112 instances in which every value is censored.
* What may set this case apart is evident but not written. The target is a share bounded at 1, so 0.99 most likely
  codes full cover and loses at most 0.01, whereas a price cap hides an unbounded tail. The 21 plots are also 12% of
  the rows. The bounded-share argument depends on the notes' own inference, though. If a family's cover is a sum of
  species covers capped at 0.99 (21 plots sum to more than 1 over the two families, up to 1.98), then these plots are
  censored just as houses' were.
* PROV-13: the check of the origin has not been done. The Dryad deposit doi:10.5061/dryad.kk174 needs a manual
  download, the Cape Point figshare deposit was not fetched, and the authors were not asked. It is also not established
  that these deposits hold these plots: Dryad has surveys from 1991/1992 and 2011/2012, the paper 2010-2011. The
  Tensions row "Repair against cleaning around damage" (coad, corporate_credit_rating, SUPPORT2, ashrae) and aeolus
  (retired for a rebuild from its origins, 2026-10-26) both put the origin first. Whether an undocumented top code
  counts as damage is an open question. Until the origin is checked, the keep is provisional rather than a departure;
  the builder's issue 2 already carries it.

**3. `RESTIONACEAE` dropped (LEAK-10).** Consistent. The other family's cover is not known at an unsurveyed site. In
caracas_cervical_cancer (Lennart, 2026-10-15) the three other tests of the same work-up were dropped as "outcomes, not
features" and one target kept. In this run noaa_afsc_bottom_trawl_survey_cpue leaves out the other species caught in
the same haul.

**4. Crassulaceae as the target (USE-5, PROV-6).** Consistent. There is no second folder for Restionaceae, following
rosbank1 (Lennart, 2026-10-26: "a swapped target of the same rows is a duplicate") and arsenic_male_lung. The choice
follows the source's main analysis, as caracas_cervical_cancer kept the biopsy. The second reason given (the reserve
alone explains a third of Restionaceae's variance) is a P6 factor, not a deciding fact, and no precedent depends on it.

**5. `rmse` fallback (MET-5, MET-8).** Consistent with the MET-5 cases (gallstone_disease,
early_stage_diabetes_risk_prediction: several metrics reported side by side, so the fallback) and with the metric
Tensions row. Every ecology sibling in this run uses the fallback as well, except noaa_afsc_bottom_trawl_survey_cpue,
whose source fixes a metric. The builder's issue 4 cites MET-10, but MET-10 weighs a source's metric against the
fallback, and no source metric is in the running here: the CRPS needs a predictive distribution, and Tjur's R² and the
AUC score only the presence stage. The precedent for squared error concentrated on a few rows, zillow_prize, was
settled by MET-4 (the competition's MAE), which has no counterpart here, and the Tensions row rules out a metric of our
own choosing. Issue 4 therefore changes no decision; the note already in `curation_comments` is enough.

**6. 180 rows (TP-5).** Consistent. Each grouped test fold holds 46-72 plots, with 16-40 zeros and 2-11 at 0.99. That
is far from parkinsons_biomedical_voice_measurements (2-3 healthy people per fold, retired) and close to musk (13 musk
per fold, kept). The working copy already has hepatitis_survival_prediction (155 rows), lung_cancer (197) and
body_density_prediction (252, regression), and this run adds pennsylvania_oak_hickory_regeneration_experiment (261,
grouped by site). The 0.99 plots carry 34% of the squared error from 12% of the test plots. That is below alvin's
51-54%, and they are not a handful of rows; TP-8 is in any case about classes.

**The builder's draft recommendations**

1. Split: see 1 and prompt 1. A "coarser blocks" option has to be an exact key (SPLIT-24).
2. 0.99 code and species-level leads: see 2 and prompt 2. PROV-13 stays open.
3. Crassulaceae over Restionaceae: consistent with precedent. Confirmation is enough; it does not need an issue.
4. MET-10 note: cites the wrong rule and changes no decision. Leave it as a note.
5. Record fields: change `required_split` to Grouped (NON-IID) once the split is accepted. `v2_path` is already set. The
   tag `Non-IID (Grouped)` is applied unevenly (wadden_sea_sibes_macoma_abundance and emscad have it;
   boreal_postfire_lichen_biomass, pennsylvania_oak_hickory_regeneration_experiment, superconductivity, concrete and
   airfoil do not), so either choice follows a precedent.

Also checked, consistent: `meta_license_unknown`, accepted with a reason on bank_customer_churn, diabetes_3,
hr_analytics and mobile_churn (and a licence is no reason to reject, per selection.md); in this run
wisconsin_local_government_property_insurance_fund is in the same position. The year, 2021, is the first commit that
holds the rows (PROV-9). On the verdict: qtp_urban_wasteland_plant_diversity, another plant survey with climate
covariates, got `No` the same day, but its record shows different facts (38 effective units, an explanatory aim), so
there is no prompt.

**Consistency prompts**

1. **Consistency check (AI, 2026-11-01):** the draft of cape_floristic_region_family_cover holds out 1-minute climate
   cells (grouped; SPLIT-1, SPLIT-24), where the paper and the record's screening field have a random split. That
   differs from covertype (IID kept, Lennart, 2026-10-01: mapping uninventoried cells inside the studied areas; "one
   would collect samples randomly across the studied area, and afterwards try to fill the gaps") and from houses (IID;
   Lennart: "spatial information are not leaking"; your own comment: "Currently, we do not include spatial data as
   non-iid. Might change that"). What sets cape apart?
   (a) It has coordinates and an exact key of 108 cells, where covertype had neither and only 3 areas. Its 180 plots
   are a sparse, clustered sample: plots in one cell share their climate values, and covers correlate at r 0.53-0.90
   under 1 km. The source frames the task as prediction at unobserved sites. Recorded as the case that makes spatial
   grouping the regime for mapping from sparse plots, with a SPLIT-24 Cases row;
   (b) treat cape like covertype: use the paper's random split and state the optimism;
   (c) reopen houses (or add a grouped variant of it) to match cape;
   (d) change the rules: amend SPLIT-24, or add a rule, saying a spatial mapping task holds out spatial units when
   coordinates or a grid key exist, and is IID only when they do not.

2. **Consistency check (AI, 2026-11-01):** the draft keeps the 21 plots coded 0.99 and documents the cap (LEAK-26).
   houses drops its 500,001 cap, although its notes say dropping loses the most expensive areas, the same reason given
   here for keeping. What sets cape apart?
   (a) The target is a share bounded at 1, so 0.99 most likely codes full cover and loses at most 0.01, whereas a price
   cap hides an unbounded tail. The 21 plots are also 12% of the rows and most of the top of the range. Recorded in the
   note, which should say it rests on the full-cover reading (the PROV-13 check of the origin could confirm that
   reading);
   (b) treat cape like houses: drop the 21 plots, leaving 159 rows;
   (c) reopen houses to keep its capped rows with a note;
   (d) amend LEAK-26 to say when a cap is kept (a code at a bounded maximum) and when the rows go (a censored, unbounded
   value).

</details>

<details><summary>Advocate</summary>

**Advocate: cape_floristic_region_family_cover (2026-11-01)**

**Position: ship after changes.** The changes are to the text, plus one optional line in the group key. No agent found
a leak, a misleading split, or a Must that cannot be met. Five of the six phase A agents land on ship or keep: claim
auditor and column auditor (text changes only), split auditor (right with notes), practitioner (fit approximate,
agrees), precedent checker (four choices consistent, two prompts with distinguishing facts available). The blind
reviewer says exclude, on size alone, and no rule supports that (point 3).

**1. The split mirrors mapping, measured twice (P4; SPLIT-1 and SPLIT-5, Must).**

- Evidence: in Baviaanskloof (two thirds of the rows) the shipped cell folds put test plots a median 1.62 km from the
  nearest training plot. A random site of the surveyed hull is 1.63 km from a plot (split auditor). The claim auditor
  got the same result on its own: 1.61 against 1.61 km, p90 3.45 against 3.31. The paper's random split puts test
  plots 0.77 km away, with 59% within 1 km against 27% of the domain. kNN on coordinates alone drops from skill 0.233
  to 0.100 (Baviaanskloof -0.020). So the cell split removes the look-up of a sampled patch, and the climate signal
  survives.
- Against the precedent prompt (covertype and houses kept IID): rules win over precedents (principles, "Conflicts").
  covertype's written reasons do not apply here: it had no coordinates and only 3 areas, and this dataset has both
  coordinates and 108 cells. What sets this case apart from "samples collected randomly across the area" is a measured
  fact: the plots are clustered (median nearest neighbour 0.5 km, against 1.63 km from a domain site to a plot). A
  random split therefore tests at half the distance the application faces. open_soil_data (Lennart, 2026-09-23) names
  spatial grouping as the regime for mapping from points.
- Against the blind reviewer's "2-5 km spatial blocks": SPLIT-24 (Must) bars k-means and distance clusters. A fixed
  2-minute grid is allowed, but its test plots sit at a median 2.28 km, farther than the domain's 1.63, so it would
  underrate models just as the random split overrates them (SPLIT-1).
- Real problem, mildest fix: `RFL_CONC` splits 4 lattice cells (SPLIT-26, Should). Key on `apan_mean_an` and
  `tminave07c` only. That gives 104 cells that equal the 1-minute lattice exactly (0 groups span two cells). The score
  change (0.461 against 0.495) is within the spread between fold draws (0.03). I support this one-line change. Reword
  the question as the split auditor's option (a) proposes.

**2. No leak (P4; LEAK-10, LEAK-30, LEAK-33, Must).**

- Evidence: all three auditors and the blind reviewer agree. The features are the coordinates, the reserve and four
  long-term grids, all known before any survey. `RESTIONACEAE` (same survey, sharing the target's denominator) and
  `plot` are dropped. The values are raw, not scaled over all rows: x10 is an integer on 180 of 180 rows for
  evaporation, and the 30-arc-second layer moves in 1/60 steps. `climate_cell` is the split key and not a feature:
  `feature_columns` drops it, the README shows `n_features: 7`, and the claim auditor checked it. That settles the
  blind reviewer's concern 3.
- Why it outranks: a leak is the one thing a real task cannot carry (principles, step 3). There is none here.

**3. Not Too Small: a tiny-data task with real signal (P6; TP-5 Must, TP-2 Should, SPLIT-28 Must).**

- Evidence: each test fold holds 46-72 plots in 36 cells, with 16-40 zeros, 19-45 positives and 2-11 plots at 0.99.
  A random forest reaches skill 0.489 on the cell folds and beats the mean on 60 of 60 splits, and every model family
  beats the mean on unseen cells. For comparison, musk was kept with 13 per fold and parkinsons retired with 2-3. The
  working copy already holds hepatitis_survival_prediction (155 rows) and lung_cancer (197).
- Against the blind reviewer's "exclude as prepared": its evidence is that paired model gaps (0.01-0.07) are smaller
  than the fold spread. That is the `no_spread` situation, and TP-2 keeps it. heart_disease_cleveland was kept with
  "little room between methods is the noise of a small task", and rosbank1 with a gap of 0.045 at SE 0.036. TP-5:
  "A small dataset as such is a tiny-data task like the others." No rule retires a dataset for rank stability, and the
  reviewer cites none. Its own fallback, a small-data slice with many repeats, is what the 20 x 3 grouped splits ship.

**4. A real use case at fit approximate, and the curator's call (P3; USE-1 and USE-8, Must; SEL-2).**

- Evidence: the source frames the task as prediction: the models "enable prediction to unobserved sites with known
  environmental attributes" (Sec. 6), and "we can perform spatial prediction for percent covers at these locations"
  (Sec. 3.5). The practitioner would use it as a screening layer in Baviaanskloof: skill 0.43 over the reserve mean,
  presence AUC about 0.7. The paper's "fire avoiders" on rocky outcrops (Sec. 5.1) make the map an ecological layer.
  Andrej's CC of 2026-10-30 gives `Yes`, priority 1. His policy of the same day: "if a dataset is useful for a
  predictive application although the data was collected for something else, then this is fine".
- Against "demonstration data of a methods paper" (blind reviewer): the curator's decision outranks an AI assessment
  (Precedence, "Who decides").
- Concede: the inputs lack the vegetation type, terrain and fire age that a reserve ecologist would have. That is no
  leak and needs no fix (USE-6), but it is a gap to add to `fit_reason` (USE-8).

**5. The target: a real problem, fixed by rewording, not by exclusion (P3 and P5; USE-5 and LEAK-26, Must).**

- Concede: `predicted` overclaims. The column auditor found that both families share a per-plot denominator in 23 of
  23 plots (4.3% under random pairing). The claim auditor found CP_2 at 0.99 in both families and BK_3 summing to 1.74
  with neither at the code. So neither "share of the plot" nor "code for full cover" is established.
- Why keep: USE-5 itself allows "a label from a named publication whose construction is undocumented (the quantity,
  its scale or the rule that sets it)" to ship with `fit="approximate"` and a note. diabetes_3 was kept on that basis
  (Lennart, 2026-10-21). This label has not been "found to be another quantity". It is still the family's abundance in
  the plot: presence matches the independent 2010 survey on 57 of 57 Cape Point plots, and ranks agree at Spearman
  0.93 on the positive plots. The scale is unknown; the quantity is the right one.
- Fix: reword `predicted`, the Target and 0.99 bullets and `fit_reason`: cover relative to an undocumented per-plot
  quantity, with 0.99 either a cap or a full-cover code, unknown which. Add the CP_2 and BK_3 facts.
- The 0.99 rows (prompt 2, houses): LEAK-26 allows "drop the capped rows or document the cap". Keeping them follows
  sat11_hand_algo_runtime, where the cap keeps the order. Here, under either reading (full cover or min(x, 0.99)), the
  21 plots are the top of the order. Facts that set the case apart from houses:
  - houses dropped 965 of 20,640 block groups (4.7%) and kept 19,675; here it would be 21 of 180 (11.7%).
  - 20 of the 21 are in Baviaanskloof.
  - The next three values are 0.986, 0.961 and 0.949, so dropping the 21 removes nearly the whole upper range, the
    succulent-dense sites the use case looks for. Without them, the forest's Baviaanskloof skill falls from 0.43 to
    0.19 (practitioner), so what remains is a different task.

  Put these facts in the note (prompt 2, option a), worded without the full-cover inference.

**6. Faithful data, kept with notes (P5; PROV-13 and PROV-14, Must).**

- Evidence: this is the authors' own release at a pinned commit, and the sha256 matches. It has no missing values and
  no duplicates, and the zeros are confirmed as absences against an independent survey (57 of 57).
- Concede: `BioClimMAP30s` is probably not precipitation. In Baviaanskloof its Spearman is +0.99 with CHELSA mean
  annual temperature and -0.77 with CHELSA precipitation. Fix: rewrite the bullet. The paper labels it precipitation,
  it ranks the Baviaanskloof plots like a temperature, its values are integers divided by 60, and its identity is not
  established. Keep the column: PROV-14 bars swapping in CHELSA, and no conversion is published.
- PROV-13: the origin was checked where it could be. The Cape Point figshare data hold counts, and cover cannot be
  rebuilt from them (one individual maps to 0.003-0.023). The Dryad file for Baviaanskloof needs a token, so it stays
  an open item for the curator, not a reason to hold the dataset. Remedy ladder: no repair is available today, so the
  step is keep with a note. Exclusion is for a Must that cannot be fixed, and a note fixes both points.

**7. The metric follows its rule and precedents (P6; MET-5 and MET-8, Should).**

- Evidence: the paper reports Tjur's R2, the AUC and two CRPS variants, and Sec. 3.4 says the CRPSf cannot compare
  models with different zero structures, so no single metric decides. RMSE and MAE rank 8 predictors at Kendall tau
  0.86, with the forest first under both (claim auditor). The practitioner keeps `rmse`. Precedents:
  gallstone_disease and early_stage_diabetes_risk_prediction.
- Against "the 0.99 plots carry 34% of the squared error and decide forest against hurdle": the metric Tensions row
  bars a metric of our own invention, and `curation_comments` already says this.
- Concede: add the CRPSf clause to the reason (claim auditor R5).

**Changes that keep the dataset (mildest remedy each)**

1. Reword `predicted`, the Target and 0.99 bullets and `fit_reason` (relative cover, the 0.99 meaning unknown, CP_2
   and BK_3). In `fit_reason` also add the missing vegetation type, terrain and fire age.
2. Rewrite the `BioClimMAP30s` bullet; keep the column.
3. Optional: key on two covariates (104 cells), and update the counts in `grouping.definition`, the notes and the code
   comment.
4. Reword the question and `splits_comment` (split auditor option a; add the 2-4 km band).
5. Correct the numbers:
   - LightGBM 0.43 to 0.37 over 60 splits each (not 0.469 to 0.331 on 3 folds).
   - Call the correlogram figures an autocorrelation, or give the Pearson values 0.58-0.66 under 1 km, 0.32 at 1-2 km
     and 0.23 at 2-4 km.
   - Cells are 1.9 x 1.5 km.
   - In the `row` line, say the Cape Point plots are permanent plots and the release holds one survey of each.
6. Add the CRPSf clause to the metric reason.
7. Record: `required_split` to Grouped (NON-IID), the curator's field.

```text
Verdict: ship after changes (text; key change optional).
Validity: SEL-2 holds (curator policy 2026-10-30); USE-1 holds, USE-8 approximate; USE-5 met by fit approximate,
  wording fixed; LEAK-10, LEAK-30, LEAK-33 hold; LEAK-26 met (cap documented, sat11); SPLIT-1, SPLIT-5 hold (measured
  against the mapping domain); SPLIT-24 holds; SPLIT-26 small departure, fixed by the two-covariate key; PROV-13 origin
  checked for Cape Point (no repair possible), Dryad open; PROV-14 keeps BioClimMAP30s as published.
Value: TP-5 holds (46-72 plots per fold); TP-2 and SPLIT-28 hold (RF above the mean 60 of 60); MET-5 fallback rmse.
Quality: notes reworded.
For the curator: prompt 1 (spatial grouping against covertype and houses, option a); prompt 2 (cap kept against
  houses, option a); the Dryad check.
```

</details>

<details><summary>Critic</summary>

**Critic, opening brief (2026-11-01): cape_floristic_region_family_cover**

**Verdict: ship only after changes.** The task is real, the grouped regime is right and no kept column leaks. But the
data contradict what the definition says on three things: what the target is, what the split tests and what the
strongest feature measures. The 21 plots at 0.99, kept on the contradicted reading, also decide which model wins.
Nothing here calls for exclusion. The fixes are rewrites, a one-line change to the key, one check of the origin, and
two answers from the curator to consistency prompts.

**1. The definition names the target as a quantity the data contradict (P3, USE-5, Must).**
- Problem: `predicted` states as facts "the share of the plot covered by Crassulaceae" and that 0.99 is "the release's
  code for full cover". The Anomaly bullet itself only says "most likely".
- Evidence:
  - In 23 of 23 Baviaanskloof plots where both families are positive and below the code, the two values are fractions
    over the same per-plot denominator (or a multiple of it). That denominator runs from 31 to 2,626 between plots, for
    example BK_3 at 660/687 and 535/687 (column auditor). A share of a fixed 50 m2 plot would not vary like that.
  - 3 plots sum above 1 with neither family at the code: BK_3 is 0.961 + 0.779 = 1.74, BK_51 is 1.36 and BK_76 is 1.01
    (re-read from the raw file). So 0.99 can be a cap, min(x, 0.99), as easily as a code. CP_2 sits at 0.99 in both
    families.
  - Full cover by one succulent family in 20 of 119 Baviaanskloof plots is ecologically implausible (domain
    practitioner).
- Effect: readers take 0.99 for a true value near 1, but it may be censored. `fit_reason` names the gap as "how species
  covers were added". The real gap is that the value is relative to an undocumented per-plot quantity.
- Rule: USE-5 lets an undocumented label ship as approximate with a note only when it "cannot be checked". It has not
  been checked yet. The Baviaanskloof Dryad deposit (doi:10.5061/dryad.kk174, CC0) returned 403 and needs a manual
  download, and nobody has asked the authors (claim auditor, U1). PROV-13 (Must) puts the origin first, and under EV-7 an
  unchecked claim stays cannot-verify.
- Remedy:
  - Rewrite `predicted`, the Target and Anomaly bullets and `fit_reason`. Suggested wording: "the family's released
    cover, relative to a per-plot quantity the source does not document; 0 to 0.99; 0.99 in 12%, a cap or a code". Add
    the facts above.
  - The curator downloads the Dryad file by hand or writes once to Tang or Frye. If that settles nothing, the dataset
    ships with the note, as diabetes_3 did. The Dryad surveys are dated 1991/92 and 2011/12, so the file may not even
    hold these plots.

**2. `fit_reason` leaves out gaps that were measured (P3, USE-8, Must).**
- Evidence (domain practitioner):
  - Missing inputs: a reserve ecologist has a vegetation-type map, terrain and fire age for every site. The paper names
    rockiness and fire frequency as drivers (Sec. 5.1, p. 15). The task uses climate and position only.
  - Unit: a 50 m2 relevé, placed in a homogeneous stand, stands in for a map cell. Within one 30-arc-second pixel, plots
    differ by SD 0.105, against 0.35 overall.
  - Cape Point: 12 of its 16 plots with any cover are below 0.05.
    - Cover skill against the reserve mean is 0.08 to 0.10 pooled over 10 repeats. Averaged per split it is below 0 (my
      re-run of `practitioner_probe.py`: RF -0.52, hurdle -0.08). Presence AUC is 0.79 to 0.81.
    - The pooled RMSE therefore scores mostly Baviaanskloof and the contrast between the two reserves. The reserve mean
      alone reaches skill 0.11.
- Effect: a user reads the dataset as one cover task over two reserves. In fact it is a Baviaanskloof cover task plus a
  Cape Point presence task, from climate and position alone.
- Rule: USE-8 (Must) requires an approximate fit to name its known gaps. Precedent: crms_phragmites_cover names the
  plot-versus-site gap.
- Remedy: one sentence per gap in `fit_reason`. The data stay as they are.

**3. The 0.99 plots are kept on the reading that point 1 undercuts, and they decide the model ranking (P4, LEAK-26,
Must; precedent houses).**
- Problem: the definition keeps the 21 plots because "dropping them would remove the densest succulent sites". houses
  dropped its capped rows although its own notes gave the same reason (precedent checker, prompt 2). The only fact that
  could set cape apart is that a share bounded at 1 loses at most 0.01 at the code. Point 1 undercuts that fact.
- Effect: on the shipped splits these plots are 12% of the test rows and carry 34% of an untuned RF's squared error (27%
  for LightGBM). By RMSE, RF wins 28 of 60 splits and a hurdle model 27. With the 0.99 plots left out of the scoring, the
  hurdle wins 44 and RF 3. I re-ran the practitioner's probe and got the same counts. RF's Baviaanskloof skill falls from
  0.43 to 0.19. So this dataset ranks methods largely by how they fit a value whose meaning is unknown.
- Rule: LEAK-26 (Must) is met by a note only if the note describes the cap correctly. Treat like cases alike
  (principles, Conflicts): houses is followed unless a written fact sets cape apart.
- Remedy, mildest first:
  - Keep the plots. Document 0.99 as a cap of unknown meaning, possibly censored. Add to the metric reason that these
    plots carry about a third of the squared error and decide RF against the hurdle model.
  - The curator answers prompt 2 with the fact that sets cape apart. If no such fact survives point 1's check, follow
    houses and drop the 21 plots (159 rows left).

**4. The question promises a harder test than the split runs, and no curator has settled a spatial grouping (P4,
SPLIT-1, Must).**
- Problem: `question` and `split` say a test plot "stands for a site whose climate grid cell has not been surveyed".
- Evidence (split auditor, Baviaanskloof): sites in unsurveyed cells are a median 2.03 km from a plot, with 11% within
  1 km. The shipped test plots are a median 1.62 km from training, with 30% within 1 km. That matches any site in the
  surveyed area (1.63 km, 27%), not the unsurveyed cells. `splits_comment` leaves out the 2 to 4 km band
  (autocorrelation 0.22 over 300 pairs), which is where most test plots look (p75 2.26 km).
- Precedent: covertype and houses ship IID (Lennart). Andrej commented on houses: "Currently, we do not include spatial
  data as non-iid. Might change that." The definition does not write down what sets cape apart.
- Effect: readers take the score as skill in unsurveyed cells. It is skill at an average site of the surveyed area.
- Rule: SPLIT-1 (Must): the split mirrors the application, and the text must name the application the split actually
  tests. I do not contest the grouped regime.
- Remedy:
  - Reword `question`, `split` and `splits_comment` as in split-auditor option (a): "a site of the two reserves, with the
    surveyed plots of its own climate cell held out". Give the remaining optimism for unsurveyed cells in numbers.
  - The curator answers prompt 1, which adds a SPLIT-24 Cases row.
  - Use 2-minute blocks only if the curator wants the stricter question.

**5. The group key includes a covariate that is not on the 1-minute grid (P4, SPLIT-26, Should).**
- Evidence:
  - `RFL_CONC` takes only 8 values. It is 41.5 at all 61 Cape Point plots (15 x 7 km) and 15.2 at 58 plots spread over
    about 17 x 20 km (column auditor).
  - Keyed on `apan_mean_an` and `tminave07c`, the 104 groups match the 1-minute lattice exactly (split auditor).
  - Adding `RFL_CONC` splits 4 of those cells. Their plots, 0.21 to 1.8 km apart, sit on opposite sides in 26 to 28 of
    the 60 splits. 4.2% of test plots share a coordinate pixel with a training plot (claim auditor).
  - The notes call this key exact.
- Effect: small on the score (RF 0.461 against 0.495, within the noise of drawing folds), but the key is not what the
  notes say it is.
- Rule: SPLIT-26 (Should) puts the key at the resolution the features see. SPLIT-24 (Must) holds either way.
- Remedy: set `ONE_MINUTE_GRID_COLUMNS = ["apan_mean_an", "tminave07c"]`. Update the counts in the code comment,
  `grouping.definition` and the notes: 104 cells, 53 with one plot, at most 1.8 km apart.

**6. `BioClimMAP30s`, the strongest feature, is described as something it probably is not (P5, EV-2, Must).**
- Problem: the notes call it mean annual precipitation and say "whatever the scale, it keeps the order of the sites".
- Evidence:
  - In Baviaanskloof its Spearman correlation is +0.99 with CHELSA mean annual temperature, -0.77 with CHELSA
    precipitation and -0.95 with elevation (claim auditor; method checked on `tminave07c` against CHELSA bio6, +0.86).
    The blind reviewer independently found +0.74 with the July minimum.
  - Its values are integers divided by 60.
  - Alone it reaches RF skill 0.453, against 0.475 with all features.
- Effect: no leak, and the task does not change. But the sentence about order is refuted in the reserve that holds two
  thirds of the rows, and readers will take the feature most models rely on for rainfall.
- Rule: EV-2 (Must): a measurement on the data outranks the source's page. Its origin, WorldClim 1.4, could not be
  reached (PROV-13), and swapping in CHELSA would be a rebuild (PROV-14).
- Remedy: rewrite the Features and Anomaly bullets: "labelled mean annual precipitation by the paper; in Baviaanskloof
  it ranks the plots like mean annual temperature; values in steps of 1/60; identity not established". Keep the column.

**7. Other statements in the notes are wrong or incomplete (P6, MET-11, Must; PROV-16, Must; EV-8, Should).**
- The metric reason leaves out that the paper selects its priors by CRPSf (Sec. 5.1 and 5.2, p. 15). The generated
  README says "the source defines no metric", but the paper reports four. `rmse` stays (MET-5).
- "LightGBM R² falls from 0.469 to 0.331 (3 x 3 folds)" compares one 3-fold run with another. On 60 splits each the
  figures are 0.434 and 0.374, a gap of 0.06, not 0.14 (split auditor).
- "r = 0.53 to 0.90" is a mean product of z-scores, not a correlation: it reaches -1.56 in one bin. The Pearson values
  are 0.58 to 0.66 under 1 km (19 to 40 pairs per bin), 0.32 at 1 to 2 km and 0.23 at 2 to 4 km.
- A 1-minute cell measures 1.9 x 1.5 km at 33.6 degrees S, not 1.9 x 1.6 km.
- `row` says "surveyed once in 2010-2011". The Cape Point plots are permanent plots surveyed in 1966, 1996 and 2010
  (figshare metadata). The release holds one survey of each.
- The record's `required_split: Random (IID)` contradicts the shipped split.
- Remedy: correct each statement in place.

**Points I do not argue:**
- Exclusion for size (blind reviewer). No rule backs it: TP-5 and TP-2 decide against it. Test folds hold 46 to 72
  plots and 16 to 40 zeros, and musk was kept with 13 per fold.
- `climate_cell` as a feature. It is not one: `feature_columns` drops it, and the README gives n_features 7.
- The licence, the choice of Crassulaceae and the drop of `RESTIONACEAE`. All three hold.

```text
Verdict: ship after changes.
Validity: USE-5 triggered (target named as an area share with a full-cover code; the data show a relative value and
  0.99 as cap or code): rewrite and check the origin. USE-8 triggered (gaps not named): note. LEAK-26 met in form but
  kept on a contested reading, unlike houses: correct the note and answer prompt 2, else drop 21 plots. SPLIT-1: the
  regime holds, the wording overclaims: reword and answer prompt 1. SPLIT-26 departure: key on two covariates.
  EV-2: the BioClimMAP30s description is refuted: rewrite.
Value: TP-5 and TP-2 hold; MET-5 fallback holds; MET-11 reason incomplete.
Quality: EV-8 numbers corrected.
For the curator: precedent prompts 1 and 2; the Dryad download or one email to the authors.
```

Files: the re-run output `practitioner_rerun.txt`, in the run folder.

</details>

<details><summary>Advocate rebuttal</summary>

**Advocate, rebuttal (2026-11-01): cape_floristic_region_family_cover**

**Where we stand.** The critic and I agree on the verdict, ship after changes, and on nearly every change. I concede
points 2, 4, 5, 6 and 7. On point 1 I concede, with the order of steps made explicit. I contest only the fallback in
point 3, dropping the 21 plots at 0.99 as houses did. A new check (below) gives the facts that set this case apart
from houses, and none of them rests on the contested full-cover reading.

**Point 1 (USE-5, PROV-13): concede.**

- I concede the rewording in full: "the family's released cover, relative to a per-plot quantity the source does not
  document; 0 to 0.99; 0.99 in 12%, a cap or a code". `fit_reason` should name the relative quantity.
- I also concede the check. USE-5's approximate route is for a label that "cannot be checked", and this one can be.
  I tried it. The Dryad API (dataset metadata, HTTP 200) lists one file, `baviaanskloof_data_dryad.csv` (3.4 MB, CC0,
  published 2016-04-25, "Baviaanskloof percent cover, trait, and environment dataset"). Its download needs a bearer
  token (HTTP 401), so a person has to fetch it by hand in a browser.
- What follows:
  - The text rewrite does not wait for the check.
  - The curator's manual download, or one email to Tang or Frye, comes before the build.
  - The file's surveys are dated 1991/92 and 2011/12, so the first thing to check is whether it holds these 119 plots
    (PROV-14: a repair keeps the same units).
  - If it does and it holds species covers, repair the target from it (PROV-13). If not, ship with the note, as
    diabetes_3 did.

**Point 2 (USE-8): concede.**

- Add one sentence each to `fit_reason`: no vegetation type, terrain or fire age among the inputs; a 50 m2 relevé
  stands in for a map cell; Cape Point is mostly a presence task (12 of its 16 plots with cover are below 0.05).
- One narrowing, not a dispute. A per-split skill within Cape Point (RF -0.52) compares 9 to 33 test plots against a
  reserve mean of 0.033. Read it as "cover is barely predictable there". It is not a rule failure: SPLIT-28 and TP-2
  judge the task on its metric, and there the forest beats the mean on 60 of 60 splits.

**Point 3 (LEAK-26, houses): concede the first remedy, contest the fallback.**

- Conceded:
  - Document 0.99 as a cap of unknown meaning, possibly censored.
  - Add to the metric reason that these plots carry about a third of the squared error.
  - Also add that with them RF and hurdle tie (RMSE 0.253 each; 28 against 27 split wins), and without them the
    hurdle model wins.
- Contested: "if no such fact survives point 1's check, follow houses and drop the 21 plots". Treat like cases alike
  only when no fact sets the case apart (principles, "Conflicts"). Here is the check that decides it:
  `cap_check.py` (run folder), run on the 60 shipped splits with the probes' forest settings.
  - **The 0.99 plots are a learnable group of sites, not scattered codes.** A classifier trained on other cells tells
    them from the rest at ROC AUC 0.877, and from the other plots with cover at 0.788. Both models rank them at the
    top (AUC 0.894 for RF, 0.889 for the hurdle). Whether 0.99 means full cover or min(x, 0.99), these plots hold the
    largest released values. So they are the succulent-dense sites that the use case ("survey or protect
    succulent-rich vegetation") looks for. The forest predicts them higher (mean 0.64 against 0.55), and that is the
    whole RF-hurdle difference the critic points to.
  - **Dropping them leaves a different, much weaker task, which houses did not face.**
    - With the 21 plots removed from the data, skill falls from 0.475 to 0.096 for RF (SD 0.269 across splits) and
      from 0.478 to 0.203 for the hurdle.
    - The table shrinks to 159 rows, 55% of them zeros.
    - Only three values above 0.9 remain (0.949, 0.961, 0.986).
    - houses dropped 965 of 20,640 block groups (4.7%) and kept a full task on 19,675 rows. Here it would be 21 of
      180 (11.7%), 20 of them in Baviaanskloof.
- Rule: LEAK-26 (Must) gives two remedies of equal standing. A note that describes the cap correctly meets it, and the
  critic's own first remedy writes that note. The facts above are what prompt 2's option (a) needs, worded without the
  bounded-share inference: "kept: 12% of the rows and nearly the whole upper range, a group of sites learnable on unseen
  cells (AUC 0.88); dropped, the task loses most of its signal". Write them into the 0.99 bullet.

**Point 4 (SPLIT-1, wording; prompt 1): concede.**

- Reword `question`, `split` and `splits_comment` as in the split auditor's option (a), with the remaining optimism
  for unsurveyed cells in numbers: 2.03 km against 1.62 km median, and the 2-4 km band at 0.22 over 300 pairs.
- I also concede that the fact setting cape apart from covertype and houses is not written in the definition yet. It
  belongs in `grouping.definition`: the plots are clustered (median nearest neighbour 0.5 km), so random folds test at
  a median 0.77 km where the domain is 1.63 km. The curator answers prompt 1, and a SPLIT-24 Cases row follows.

**Point 5 (SPLIT-26): concede.** Key on `["apan_mean_an", "tminave07c"]`, the exact 1-minute lattice (104 cells).
Update the counts and drop the word "exact" from the old three-column description. I proposed the same in my opening
brief.

**Point 6 (EV-2, PROV-14): concede.** Rewrite the Features and Anomaly bullets as the critic words them, and keep the
column.

**Point 7 (MET-11, PROV-16, EV-8): concede each correction.**

- One narrowing: the README line "the source defines no metric" is generic text that the generator writes for every
  `Metric.fallback`. The reason above it already names the four criteria the paper reports. The dataset fix is the
  CRPSf clause; the generic line is a repository matter, to flag rather than fix in this folder.

**What remains for the curator**

1. Prompt 1 (spatial grouping), answered with option (a) and the clustered-sample fact.
2. Prompt 2 (the cap), answered with option (a) and the facts from point 3.
3. The Dryad download, or one email to the authors, before the build.

```text
Verdict: ship after changes (both sides).
Agreed: rewrite predicted/Target/0.99/fit_reason (USE-5, USE-8); reword question and splits (SPLIT-1); key on two
  covariates (SPLIT-26); rewrite BioClimMAP30s (EV-2, PROV-14); correct the numbers and the metric reason (EV-8, MET-11);
  record required_split to Grouped; Dryad check before the build (PROV-13).
Disputed: the houses fallback for the 21 plots. Keep (LEAK-26 met by the corrected note): 11.7% of rows, a learnable
  group of the densest sites (AUC 0.88 on unseen cells); dropping them cuts skill to 0.10-0.20 (cap_check.py).
```

</details>

<details><summary>Critic rebuttal</summary>

**Critic, rebuttal (2026-11-01): cape_floristic_region_family_cover**

**Where the two briefs stand.** We agree on the verdict, ship after changes, and on most of the changes. Four points
are still open. One is whether the key change is optional. Two others are whether the two USE-8 gaps the advocate
leaves out go in, and how the 0.99 note is worded. The last is how the Dryad item is recorded. I concede the rest. One
new check below (the upper range of the target) bears on the 0.99 point.

**A1. Split (SPLIT-1, SPLIT-5): the regime is conceded; contested only that the key change is "optional".**
- Conceded:
  - The cell folds match the mapping domain in Baviaanskloof (1.62 against 1.63 km).
  - SPLIT-24 bars k-means blocks.
  - 2-minute blocks would underrate models.
  - The clustering fact (median nearest neighbour 0.5 km, against 1.63 km from a domain site to a plot) is what sets
    cape apart from covertype. It belongs in the answer to prompt 1.
- Contested: the advocate calls the two-covariate key "optional". SPLIT-26 is a Should, which makes it the default.
  Departing from it needs a fact that sets the case apart, recorded as an exception (principles, Strengths). No such
  fact has been offered.
  - The paper calls `RFL_CONC` a 1-minute grid (Sec. 2), but the data say otherwise: 8 values, and 4 lattice cells split
    in two. A measurement on the data wins over the paper (EV-2, Must).
  - The fix is one line and safe (score change 0.461 against 0.495, inside the noise of drawing folds).
- My ask stands: key on `apan_mean_an` and `tminave07c`, or record an exception that names its fact.

**A2. No leak (LEAK-10, LEAK-30, LEAK-33): conceded.** I raised no leak point. `climate_cell` is not a feature.

**A3. Not Too Small (TP-5, TP-2, SPLIT-28): conceded.** I said so in my opening brief: no rule retires this dataset
for size or for how stable its model ranking is.

**A4. Use case and fit (USE-1, USE-8, SEL-2): conceded on the use case; narrowed on what `fit_reason` names.**
- The advocate concedes the missing inputs (vegetation type, terrain, fire age). Its list of changes leaves out the
  other two gaps from my point 2, and it does not dispute either:
  - The unit: a relevé placed in a homogeneous stand stands in for a map cell. Plots inside one pixel differ by SD
    0.105.
  - The two reserves are different tasks. At Cape Point, cover skill is 0.08 to 0.10 pooled. Averaged per split it is
    below 0 (my re-run). Presence AUC is about 0.8.
- USE-8 (Must) asks for every known gap to be named. Both gaps are measured, so both go into `fit_reason`, one sentence
  each.

**A5. Target and the 0.99 rows (USE-5, LEAK-26): rewording conceded by both sides; the keep is conceded as the
curator's option (a); narrowed on the note.**
- Conceded:
  - The quantity is plausibly the family's abundance. Presence agrees on 57 of 57 Cape Point plots, and ranks agree at
    Spearman 0.93 on the 14 positive plots.
  - With the rewording, USE-5 is met as it was for diabetes_3.
  - The advocate's facts stand. 21 of 180 rows are at 0.99, against 4.7% in houses, and 20 of the 21 are in
    Baviaanskloof. New check on the raw file: of the 25 values at or above 0.8, 21 sit at the cap (21 of 36 at or above
    0.5). Dropping them would remove most of the upper range that the use case looks for.
- Narrowed, for two reasons:
  - The sat11 analogy does not carry over. sat11 keeps its timeouts because its source metric, PAR10, reads a timeout
    as a timeout (its notes, "is enough to compute PAR10"). Here RMSE reads 0.99 as an exact value. The note should
    rest on the share and the use case, not on "the cap keeps the order", because RMSE does not score an order.
  - The note must say what the cap does to the score (LEAK-26: document the cap). Today `curation_comments` gives the
    weight: 12% of the test plots and 34% of RF's squared error. It does not say that these plots decide the winner. I
    re-ran the check: RF 28 and hurdle 27 of 60 splits with them, hurdle 44 and RF 3 without. That needs one clause.
    This is a note, not a new metric, so the metric Tensions row is not engaged.

**A6. Faithful data (PROV-13, PROV-14): BioClimMAP30s conceded by both sides; the Dryad item narrowed.**
- Agreed:
  - Rewrite the `BioClimMAP30s` bullet and keep the column (PROV-14).
  - The Cape Point figshare data cannot repair the target, because they hold counts.
- On Dryad, I accept that the dataset need not wait for it. But under EV-7 (Must) it stays cannot-verify and is not
  recorded as met. USE-5's "cannot be checked" holds only once the curator has tried the manual download or the email,
  or has declined to. The REVIEW.md item should say that.

**A7. Metric (MET-5, MET-8): conceded.**
- `rmse` stays, and the CRPSf clause is added (MET-11).
- The 0.99 clause belongs in the cap note (A5), not in the metric choice.

**What remains for the curator after both briefs:**
- The two-covariate key, or an exception (SPLIT-26).
- Two more sentences in `fit_reason`: the unit, and Cape Point as a presence task (USE-8).
- In the 0.99 note: the ranking clause, and no sat11 order argument (LEAK-26).
- Prompts 1 and 2.
- The Dryad item, recorded as cannot-verify.

Check: `practitioner_rerun.txt`, in the run folder. The upper-range count was run inline on the raw file
`cfr_zib_data.csv`.

</details>
