---
unique_name: boreal_postfire_lichen_biomass
name: Terrestrial lichen - Northwest Territories / Terrestrial lichen - Saskatchewan (post-fire forage-lichen biomass, Greuel et al. 2021)
checked_by:
- Andrej
data_foundry_status:
- WIP (DF)
claimed_by: Andrej
suggestion: 'Yes'
priority: 3
tags:
- Two-Regime Zeros
- 'Samples: One Moment'
original_source: Other
year: '2021'
domain: biology & life sciences
required_split:
- Grouped (NON-IID)
problem_type: Regression
original_data_state: Database (or multiple to-be-joined tables)
source_links:
- https://doi.org/10.5061/dryad.t1g1jwt15
- https://doi.org/10.5061/dryad.tb2rbnzzj
- https://doi.org/10.1002/ecs2.3481
- https://doi.org/10.5061/dryad.76hdr7sth
v2_path: datasets/_dev/tabarena-v0pt2/boreal_postfire_lichen_biomass/dataset.py
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. Drafted by an AI assistant on 2026-10-19 from the two-regime-zero workbook (v4 of 2026-10-19, a list of 69 candidates, not in the repository), the source pages and papers, and the data itself where the notes say it was downloaded and measured. A human must verify the suggestion, the metadata and the notes before relying on them.**

**Screening (AI, 2026-10-27):** `TBD -> 2nd Tier`, priority 1: a regional post-fire survey of caribou forage lichen
(567 plots in the Northwest Territories and Saskatchewan) with stand age, stand type and ecoprovince as covariates, not
a designed experiment, so the family's open species-abundance question decides it rather than a fast reject; the
biomass target is an allometric estimate from cover and height.
- Source: Greuel et al. 2021 (Ecosphere 12:e03481), two Dryad deposits, CC0: Northwest Territories
  (doi:10.5061/dryad.t1g1jwt15, first version 2021-02-03, now version 5 of 2026-05-18; site info, destructive biomass
  samples, lichen data and quadrat cover sheets) and Saskatchewan (doi:10.5061/dryad.tb2rbnzzj, 2021-02-18; lichen data
  and destructive biomass sheets). Dryad methods: "346 plots were established with 5, 1 by 1 m quadrats within
  predetermined burn age classes" (NWT) and "221 plots were established with 2, 2 by 2 m quadrats within three age
  categories" (SK). About 1,730 and 440 quadrat rows (earlier AI triage, 2026-10-19, an estimate); not downloaded
  (Dryad answers 401 to file requests).
- Use case: the authors "used estimates of lichen biomass to quantify patterns of lichen recovery in different stand
  types, ecoprovinces, and with time following stand-replacing fire", and the results "provide a basis for estimating
  future caribou habitat" (Dryad abstract); for example a caribou range planner estimating forage lichen in a stand of
  known fire age and type. No actor or decision is named, so the fit is approximate at best. Regime grouped by plot or
  site, since quadrats nest in plots (SPLIT-3); the two regions differ in protocol (quadrat size, age classes).
- Siblings and duplicates: `athabasca_forage_lichen_cover` is another study (Alberta, data not released); no duplicate
  among the records. No ecological record of the family had a curator's verdict yet; the triage of 2026-10-19 named
  `wadden_sea_sibes_macoma_abundance`, `great_lakes_marsh_bird_point_counts` and
  `nantucket_sound_sea_duck_aerial_survey_counts` as the cases to settle the question on (since settled by Andrej on
  2026-10-30, policy question 1 of the zero-inflated review: no new rule, each survey judged on its own use case).
  External collections: none found.
- Papers and pages: Greuel et al. 2021 (text not read: Wiley 403; claims from the Dryad abstract and methods, the
  authors' text); the companion deposit doi:10.5061/dryad.76hdr7sth (Baltzer et al.) describes the mature stands.
- Metric: none found (the Dryad abstract reports a hurdle GLM judged by significance and a logistic growth model; the
  paper's text was not reachable), so the fallback `rmse`.
- Risks for /add-dataset: the target. Biomass comes from "allometric equations to estimate lichen biomass from field
  measurements of lichen cover and height" (Dryad abstract), so cover and height are the label's inputs and go
  (SEL-5); measured lichen cover is the alternative target. The two protocols need one target definition, the sheets
  need joining, and what the site sheet holds beyond stand age, type and ecoprovince is unseen. The question of
  species-abundance mapping from habitat covariates is settled (Andrej, 2026-10-30, policy question 1 of the
  zero-inflated review: no new rule, each survey judged on its own use case); `No Good Target / Scientific Discovery`
  stays as the marker of that concern.
- Priority: gap 0 (biology, regression and grouped are not thin), use case 0 (none named), source + (a paper and two
  documented deposits), shape 0 (about 567 plots, few covariates), risk - (allometric target, two protocols).

**Assessment (AI, 2026-10-30):** The family's question on species-abundance mapping is settled without a new rule
(Andrej, 2026-10-30, policy question 1 of the zero-inflated review: "I don't think there is new rule to build here.
These are per dataset judgement calls and if a dataset is useful for a predictive application although the data was
collected for something else, then this is fine"), as SEL-2 already reads the scope rules: this record is judged on its
own use case. The verdict and priority stay.

CC (2026-10-30, Andrej): `Yes`, priority 1 (the AI screening had `TBD -> 2nd Tier`, priority 1; zero-inflated screening
review page).

Workbook rows 37 and 38 are one study (Greuel et al. 2021, one paper, overlapping authors) released as two regional
Dryad deposits with different field protocols, so they share this record. Northwest Territories: "346 plots were
established with 5, 1 by 1 m quadrats within predetermined burn age classes (37-38 and 46-49 years post-fire) and ...
'control' (>70 years)". Saskatchewan: "221 plots were established with 2, 2 by 2 m quadrats within three age
categories". About 1,730 and 440 quadrat rows by estimate; not downloaded (Dryad blocks automated downloads).

The study is a fire-recovery chronosequence: the abstract's hurdle GLM "identified stand age, stand type and
ecoprovince as significant predictors of lichen presence", inference on three design variables with no remote-sensing
covariates, mapping or validation mentioned. Biomass is itself estimated: "allometric equations to estimate lichen
biomass from field measurements of lichen cover and height", so cover and height would be the target's own inputs.
Zero mechanism, from the abstract only: no forage lichen in the quadrat, hence allometric biomass 0. Workbook
pushback: "Verified strict match" and "Core: Yes" rest on the hurdle model, which is inference, not a prediction task.
Paper text not read (Wiley 403). Licence: CC0.

**Assessment (AI, 2026-11-01):** added as `datasets/_dev/tabarena-v0pt2/boreal_postfire_lichen_biomass/` by /add-dataset with the full review panel; the open questions are in its Review. Recommend shipping as changed: the caribou range-plan biologist named as the actor, the NT plots grouped by burn area and the SK plots per plot (216 groups), three NT plots' coordinates repaired from the site sheet. Superseding the screening's guesses above: 516 plots and 2,010 quadrats; fetched from Dryad's version zips without a token (the 2022 revision of the NT sheet), not "Dryad answers 401". The marker `No Good Target / Scientific Discovery` stays until your mark on issue 1. Priority 3: gap 0, use case 0 (fit approximate), source + (CC0 deposits and a paper), shape +, risk 0.

CC (2026-11-03, Andrej): the two duplicate-row warnings are accepted as worded (issue 3 (A) in boreal_postfire_lichen_biomass).

CC (2026-11-03, Andrej): read Greuel et al. (2021) through Wiley's HTML page (issue 4): stand age by tree-ring dating, a pooled volume allometry with no significant variation across ecoprovinces, Saskatchewan's total heights adjusted by a live-to-total ratio of 0.76, an observed-versus-fitted R2 of 0.18 without held-out evaluation, no explanation of the missing plots: "We can now replace the blanket warning with specific references for confirmed claims."

**Assessment (AI, 2026-11-03):** the paper is read from the publisher's PDF (Wayback Machine copy of 2021-07-16); the notes now cite it by section, and the claim that the two regions convert cover differently is removed (one pooled allometry; 12.633 is its volume slope in kg/ha). Its stated aim is the task itself: "accurately predicting the availability of lichen forage under current and future fire regimes".

CC (2026-11-03, Andrej): ship after the changes (verdict). Issue 1 (A): the paper's own forecast with the range-plan actor and the burn-area split; the `No Good Target / Scientific Discovery` marker is removed, as the paper's predictive aim answers it. Issue 2 (A): the tree-ring stand age stays. Issue 5 (A): kg/ha, decided for this task alone ("I go with your recommendation"). Issue 6 (A): RMSE on kg/ha ("We can keep RMSE in this case").

CC (2026-11-03, Andrej): ship (verdict); the metric, RMSE on kg/ha, checked.

**Assessment (AI, 2026-11-06):** review panel (focused, re-review under LEAK-41, MET-14 to MET-16): ship after changes (wording only; nothing shipped changes; the notes' equal-per-plot taus, the dropped 0.91 of the former site splits and the exposure reason are fixed); disputed: none, issue 7 is a weighing call (the per-quadrat RMSE counts an NT plot 2.5 times an SK plot: A keep and say so, implemented, or B count each plot once); for the curator: issue 7.

CC (2026-11-08, Lennart): issue 7 (B) in boreal_postfire_lichen_biomass, "Each plot counts once." Andrej's RMSE on kg/ha (2026-11-03, issue 6) stays and is now weighted by 1 over the plot's number of quadrats (`plot_weight`: 0.2 in NT, 0.5 in SK), a scoring column for the metric only, not a training weight. The warning that the metric has a row weight but no sample weight is accepted: a design weight that gives each plot one vote, set by `jurisdiction`, not an amount at risk.

**Assessment (AI, 2026-11-08):** `rmse` now takes an optional `weight` input (`sqrt(sum(w * (y - p)^2) / sum(w))`), and the definition declares it from context with `plot_weight`. On the data, `plot_weight` is 0.2 on all 1,630 NT quadrats and 0.5 on all 380 SK quadrats (326 plots of 5, 190 of 2), so it sums to 1 per plot. On the 30 shipped splits, with the 8 untuned predictors of the claim audit, the declared score ranks the models exactly like the RMSE of the plot means with each plot counted once (Kendall tau 1 on 30 of 30 splits). Against the per-quadrat RMSE declared before, tau is 0.81 per split (lowest 0.21) and 0.86 for the ranking by the mean RMSE; that ranking swaps the training mean with ridge and with knn. Task probe: the random forest scores 1,159.8 kg/ha against the training mean's 1,250.0 and beats it on 80% of the splits; no flag. The splits hold the same rows and test groups as before; only the frame's row order changed. `dataset check`: 0 errors, 0 warnings.

**Assessment (AI, 2026-11-08):** correction to the line above: the metric stays the fallback RMSE, now weighted by `plot_weight` (`Metric.fallback` takes inputs since 2026-11-08), not declared from context; the README states origin `fallback`. The declared metric was checked as declared (CC 2026-11-08 above, issue 7 B).

CC (2026-11-08, Lennart): the declared metric (the fallback `rmse`, weighted by `plot_weight` so each plot counts once) is checked: as marked, with issue 7 (B).

CC (2026-11-08, Lennart): the score's `plot_weight` is declared as the task's `unit_weight` (column `plot_weight`, unit `plot`), so downstream tools can read that each plot counts once and weight their validation loss alike ("make sure to somehow add it to the metadata that this kind of group type ... exists and can be read by downstream tools"; MET-17). The `plot` column stays in the frame as metadata, never a feature.

CC (2026-11-09, Andrej): issue 9 (B) in boreal_postfire_lichen_biomass, "Option B: Site-sheet coordinates as features." Every NT plot ships its transect start from the authors' site sheet `All_site_info_NT.xlsx` as its coordinates; the 0.01 degree grid of the lichen sheet (three plots repaired) only links CG2 and F2 and is not shipped, so the groups are unchanged.

**Assessment (AI, 2026-11-09):** issue 9 (B): on the same 30 splits the random forest's weighted RMSE moves by +4.2 kg/ha (SE 3.3), LightGBM's by +3.9 (SE 8.9), within noise; the duplicate warnings are recounted (518 copies, 506 at 0, all within one plot; 976 conflicting rows; 28.8% of the variance within a plot). Issue 8 (B, Andrej's change mark asked for an ablation first): the SK plots joined point in polygon to Canada's fire maps (NFDB agency perimeters and NBAC, Open Government Licence - Canada), keeping a polygon within 1 year of the plot's fire year: 94 of 190 plots get a burn (94 of the 124 dated 1945 or later; 44 of the 71 with a same-year plot within 5 km), 45 burns of which 20 hold 2 to 9 plots (69 plots); the map year equals the field fire year in 157 of 165 matches; 42 plots lie inside a later mapped fire and none of their own year (33 dated before 1945) and stay on their own. Ablation (untuned, container inputs, 3 seeds, 30 splits each): 216 groups and an SK test quadrat 3.4 km from training with one group per SK plot, 167 groups and 4.3 km on the burns; the random forest's RMSE 1,166.8 (SE 29) against 1,186.3 (SE 24) overall and 1,230.3 (SE 40) against 1,254.1 (SE 47) on the SK rows, within the fold draw (the unchanged NT part moves as much); paired on the former folds, removing the test plots' burn-mates from training raises the forest's RMSE on those plots by 31 kg/ha (SE 9) against +2 to +6 for removing other SK plots, about 5 kg/ha on the SK RMSE and 2 kg/ha overall. B was implemented in the definition that day (`_prepare_raw_files` read the 2 GB of maps once); superseded on 2026-11-10: B is removed and the SK plots are one group each again (CC 2026-11-10 below).

CC (2026-11-09, Andrej): columns held only for training rows stay out for now, no training-only role (cross-dataset item of 2026-11-09; MET-14, LEAK-41, MET-16); the notes list them.

CC (2026-11-10, Andrej): issue 8 (a) in boreal_postfire_lichen_biomass, "Reply (a): Back to A, with the note". Each SK plot is its own group again (216 groups); the grouping by Canada's fire maps of 2026-11-09 is removed (no NFDB or NBAC download, no prepared polygon table), and the notes give its measured effect: 71 of 190 SK plots have a same-fire-year plot within 5 km, 94 of 190 lie inside a mapped burn of their year, burn-mates in training flatter the SK RMSE by about 5 kg/ha against a fold-draw SE of about 40, and no model changes rank. The site-sheet coordinates of issue 9 stay.

**Assessment (AI, 2026-11-10):** issue 8 (a) applied; the probes give the numbers of before 2026-11-09 again: task probe random forest 1,164.3 kg/ha against the training mean's 1,250.0 (better on 77% of the 30 splits), no flag; group probe LightGBM R^2 0.408 on random folds against -0.035 on the burn-area folds; leak probes no flag; an SK test quadrat lies a median 3.4 km from the nearest training plot (SD 0.6 over the splits), NT 22 km. `dataset check`: 0 errors, 0 warnings. Verdict mark of 2026-11-10 (Andrej): changes, now made.

CC (2026-11-10, Andrej): ship (review page of 2026-11-10).

## Review

**Outcome:** added. The AI recommends shipping it as implemented: the re-review of 2026-11-06 under the exposure
rules changed wording only, and its one weighing call (issue 7) is settled: each plot counts once (2026-11-08).
Greuel et al. (2021) surveyed caribou forage
lichen after boreal wildfires in the Northwest Territories (NT) and Saskatchewan (SK), in two Dryad deposits (CC0). One
row is one ground quadrat: 2,010 quadrats of 516 plots, 40.4% of them at 0. The target is the authors' lichen biomass
in kg/ha, estimated from cover and height. The inputs are the years since fire, the stand type, the coordinates, the
ecoprovince, the ecozone and the jurisdiction. Whole NT burn scars or unburned areas are held out, and each SK plot
on its own (issue 8: SK burns from Canada's fire maps were tried on 2026-11-09 and taken back on 2026-11-10). The
metric is RMSE on kg/ha with each plot counted once: a quadrat weighs 1 over its plot's quadrats (0.2 in NT, 0.5 in
SK), where unweighted an NT plot (5 quadrats) would count 2.5 times an SK plot (2).

Validity:
* SEL-2 holds: Andrej's `Yes` of 2026-10-30 (policy call 1).
* USE-1 triggered, fixed: the actor is named (issue 1).
* USE-5 holds: the NT target reproduces from the authors' own cover sheet.
* USE-6 holds for the stand age, with a USE-8 note (issue 2).
* LEAK-10 holds: the cover-based biomass (61.934 x cover in every row) and the presence flag are dropped.
* LEAK-41 holds, nothing to remove: the quadrat's area (1 m2 in NT, 4 m2 in SK) is fixed by each protocol and set by
  `jurisdiction`, not realized.
* SPLIT-1/SPLIT-4 triggered, fixed: re-split on the burn area (issue 1); SK plots stay one group each, with the
  measured effect of their shared burns in the notes (issue 8, a).
* SPLIT-23 holds: every prediction is constant within a plot, so the RMSE weighted by 1 over the plot's quadrats ranks
  models exactly like the plot score with each plot counted once (Kendall tau 1 on 30 of 30 splits; issue 7, B).
* SPLIT-26 holds: the source's quadrat rows are kept.
* MET-14 holds: the source ships the amount per unit area (kg/ha); the notes' reason is reworded (EV-7).
* MET-15 not triggered as a weight rule (no realized denominator); the plot weight of issue 7 is a function of
  `jurisdiction`, so it needs no sample weight, and the bundle warning is accepted.
* MET-16 holds: neither sheet has a survey or design weight; the sites were chosen by fire-age class, an input.
* PROV-13 triggered, fixed: three plots' coordinates repaired from the authors' site sheet; since 2026-11-09 every NT
  plot ships the site sheet's coordinates (issue 9).
* PROV-8 holds: the download is Dryad's own version zips, which the repair needs.
* PROV-16 holds: the paper is read (issue 4, resolved 2026-11-03); the notes cite it by section.

Value: TP-2, a small real signal. Under the burn-area split an untuned random forest has skill (1 - MSE / MSE of the
training mean) +0.12, above 0 on 28 of 30 splits (the task probe's forest: 200 trees, min_samples_leaf 2, a square root
of the inputs per split; the forest of issues 1 and 5, 300 trees with min_samples_leaf 20 and all inputs per split,
scores +0.097). Fallback RMSE, each plot counted once since 2026-11-08 (issue 7): the abstracts report significance
tests and a growth curve, no prediction error (MET-1).

Quality: CLEAN-16 departure kept with a measured fact, the target stays on kg/ha (issue 5); counts and sentences in the
notes corrected (EV-7). On 2026-11-06 EV-7 was triggered three more times, each fixed by rewording: the taus against
the equal-per-plot score had been measured per input vector, not per plot (now 0.81 per split and 0.86 for the
ranking, 8 untuned predictors); the 0.91 of the former site splits is dropped as not like for like; the exposure
bullet's reason now follows MET-14.

Weighed: source + (CC0, two documented deposits, a paper); use case + (range plans against the 40-year rule); signal -
(skill about 0.1); size 0 (2,010 quadrats, 216 groups).

Left for the curator: nothing. Issue 8 is settled (a, back to one group per SK plot with the note; Andrej,
2026-11-10); issue 9 is settled (B, site-sheet coordinates; Andrej, 2026-11-09) and issue 7 too (B, each
plot counted once; Lennart, 2026-11-08).

The first panel (2026-11-01) reviewed the first draft (site split, Zenodo download, unrepaired coordinates); its eleven
changes that need no decision were made. The focused re-review of 2026-11-06 (claim auditor and mediator) found
wording only, and its changes are made (Mediator, "Changes to make now"). The numbers below are measured on the changed
definition and its 30 shipped splits (untuned) unless marked as the panel's.

**Main points:** No issue open. Resolved on 2026-11-10: one group per SK plot again, the fire-map burns of 2026-11-09
removed and their measured effect (about 5 kg/ha on the SK RMSE) in the notes (8, a). Resolved on 2026-11-09: the NT
plots ship the site sheet's coordinates (9, B). Resolved on 2026-11-08:
each plot counts once in the RMSE, weighted by 1 over its quadrats (7, B). Resolved on 2026-11-03: the paper's own
forecast (1), the tree-ring stand age (2), the duplicate warnings (3), the paper read (4), kg/ha (5) and RMSE (6);
verdict: ship.

**Verdict (2026-11-10, Andrej):** ship (review page of 2026-11-10).

**Issues for Andrej and Lennart:**

1. **Confirm the caribou range-plan biologist as the actor, and with it a test on burns nobody surveyed?**

   * **Problem:**
     - The source names no actor, and a use case needs one, with a moment and a decision[^1].
     - The panel named a caribou range-plan biologist, who predicts for burns nobody surveyed.
     - Confirming that actor sets the split: whole burn areas held out, not single sites.
   * **Background:** the first draft's example was "a caribou range planner", and its split text aimed "across the
     range, where most stands have no plot". After the panel, the use case names an actor and a decision from public
     sources. A caribou
     habitat biologist with the GNWT or Saskatchewan's Ministry of Environment revises a boreal caribou range plan.
     Today a burn under 40 years counts as disturbed
     ([federal fact sheet](https://www.canada.ca/en/environment-climate-change/services/species-risk-public-registry/recovery-strategies/woodland-caribou-boreal-population-fact-sheet.html)),
     while NWT monitoring found that forage lichens need 45 to 70 years to recover
     ([CIMP](https://climatelibrary.ecc.gov.nt.ca/dataset/4bcc94fc-cb61-400e-858a-1bac4526ffcf)). Such a biologist
     predicts for stands in burns this study did not survey.
   * **Effect on the task:** the actor changes the split. When the deployed model meets new entities, the test
     entities must be new[^2], grouped on an exact key[^3]. The NT codebook names each plot by its burn scar or
     unburned area ("Plot location: Burn Scar or Unburned area -xxx"), and plots of one area share their fire and
     much of their lichen (18.4% of the NT target's sum of squares lies between areas). With whole sites held out
     (the first draft's group: plots of one name, `F1-22` of `F1-22A`, joined with any at the same coordinate; 312
     groups), 94.3% of NT test quadrats had another site of their own burn area in training, a median 2.4 km away
     (the panel). A stand in the NT study region lies a median 95 km from any plot. Holding out whole areas puts that
     median at 22 km.
   * **Experiments:** the trees keep most of their skill (random forest +0.112 by site in the panel's run, +0.097 on
     the shipped area splits; small LightGBM +0.098 and +0.103). Ridge falls from +0.132 to -0.085 and is below the
     training mean on 8 of 30 splits. The cause is its ecoprovince effect, which it learns from a handful of burns
     and which does not carry over to a new burn: Great Bear Plains has 5 burns, with means from 270 to 3,453 kg/ha.
     Without the three region labels ridge scores +0.064. Ridge ranks first under the site split and last under the
     area split.
   * **Panel:** for the area split, the critic and the split auditor; the advocate conceded once the actor is named.
     For the site split, the domain practitioner's opening, which rested partly on a note ("within its noise") that
     proved false.
   * **Consistency:** follows airfoil_self_noise, grouped by setup rather than by run because 91.5% of test runs had
     their setup in training[^4]. 5g_energy_consumption is set apart: it had no documented entity above the station.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Range-plan actor, burn-area groups (implemented) | holds out whole NT burn scars or unburned areas (26 groups) and each SK plot on its own: 216 groups, the largest 10% of the rows, test folds 299 to 1,028 rows | an actor and a decision from public sources; NT test stands a median 22 km from training | unequal folds; SK stays the laxer region (test median 3.7 km from training) |
     | B | Infill, site groups | use case narrowed to unsurveyed stands inside burns already partly surveyed, "across the range" dropped; holds out single sites (314 groups after the repair) | the domain practitioner's opening reading | no source names that actor; 94.3% of NT test quadrats have their own burn area in training; ridge's score is inflated |

   * **Recommendation:** A: its actor and decision come from public sources, and its NT test stands lie a median
     22 km from training instead of 2.4 km. Confirming it also takes the screening's `No Good Target / Scientific
     Discovery` marker off the record, since the actor answers its concern. **Decision:** A, the range-plan actor with
     the burn-area split, or B, infill with the site split?

   **Notes for the AI:** in A, CG2 and F2 join into one NT group through plots about 0.5 km apart; SK plot names carry
   no burn key, hence one group per SK plot. On A, remove the `No Good Target / Scientific Discovery` marker from the
   record. On B, restore the site groups (plots of one name, `F1-22` of `F1-22A`, joined with any at the same
   coordinate) and reword the use case to infill.

   [^1]: **USE-1** (Must): a use case is an actor, a moment and a decision, written down first and checked against
     every column, filter, target and split choice.
   [^2]: **SPLIT-1** (Must): the split mirrors the real application. **SPLIT-4** (Must): if the deployed model
     predicts for entities new data would not contain, the test entities must be new, even when a random split costs
     little.
   [^3]: **SPLIT-24** (Must): group on a true group id, or one constructed exactly from the data, never on a
     similarity cluster.
   [^4]: airfoil_self_noise, grouped by setup (Lennart, 2026-10-20).

   **Andrej (2026-11-03, discuss):** Is this really a meaningful task that can be served with the available data or did
   you just made it up because I asked you to?

   **Answer (AI, 2026-11-03):**

   * **Problem:**
     - The task is the paper's own: Greuel et al. (2021) is titled "Predicting patterns of terrestrial lichen biomass
       recovery following boreal wildfires", and it predicts forage lichen from the same inputs we ship.
     - What we added is a named actor and the test on burns nobody surveyed, which the paper's call for "landscape
       level and regional level, spatial predictions" asks for.
     - The data serve it only weakly: the paper's model explains 18% of the variance on its own data, and ours about
       10% on held-out burns.
   * **What the paper says** (read now from the publisher's PDF):
     - Its aim: "accurately predicting the availability of lichen forage under current and future fire regimes"[^1a].
     - Its use: the relationships "support the development of the first landscape level and regional level, spatial
       predictions of forage lichen biomass for several boreal and barren-ground caribou herds", and "Managers should
       consider these regional and stand-type differences when developing strategies for caribou habitat
       management"[^1b].
     - Its inputs: time since fire, stand type and ecoprovince (or latitude), the inputs we ship, plus the
       coordinates.
     - Its fit: "relatively weak but significant (R2 = 0.18)", "expected" because the model leaves out canopy
       closure, soil, water table and permafrost: "We used broad landscape variables to demonstrate a generalized
       approach"[^1c].
   * **What limits it:** 32.5% of the target's variance lies between quadrats with identical inputs (the quadrats of
     one plot), so no model can explain much more than the rest; our random forest reaches +0.10 to +0.12 on held-out
     burn areas, against the paper's 0.18 on the data it was fitted to.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Ship as the paper's forecast (implemented) | range-plan actor, burn-area split, as now | the source's own predictive task; real management use | weak signal (skill about 0.1) |
     | B | Don't ship | record set to `No`, folder removed | no weak task in the benchmark | a small real signal is no reason to retire[^1d]; loses a real ecology forecast |

   * **Recommendation:** A: the task is the paper's, not ours, and its signal is small but real. **Decision:** A or B?

   [^1a]: Greuel et al. 2021, Introduction.
   [^1b]: Greuel et al. 2021, Discussion.
   [^1c]: Greuel et al. 2021, Results, "Combined predictions of two-component hurdle model", and Discussion.
   [^1d]: **TP-2** (Should): a small but real signal is no reason to retire.

   **Resolved (2026-11-03, Andrej):** A, shipped as the paper's forecast with the range-plan actor and the burn-area
   split; the record's `No Good Target / Scientific Discovery` marker is removed.

2. **Keep the field-dated stand age as an input?**

   * **Problem:**
     - `years_since_fire` is the survey's stand age for each plot, not a value read off a fire map.
     - For the 145 NT control plots it was dated in the field, more precisely than the age a planner has.
     - Is it kept as an input?
   * **Background:** the 145 NT control plots (36% of the rows) lie in areas with "no recorded burn history" (Dryad methods), so their ages
     (33 to 241 years) were dated in the field, presumably from tree rings. A planner would have the forest
     inventory's age, or "older than the fire record".
   * **Effect on the task:** the model gets a more precise age than the planner has for old stands.
   * **Experiments:** capping the age at an assumed fire-record horizon (51 years in NT, 70 in SK; the panel's own
     assumption) costs, on kg/ha and the shipped burn-area splits, the random forest R^2 0.007 (SE 0.020), ridge
     0.024 (SE 0.021) and a small LightGBM 0.032 (SE 0.016). The panel measured 0.013 to 0.017 on the former site
     splits. Dropping the column costs 0.08 to 0.11 there: it is the main signal.
   * **Panel:** for keeping it with a note, the advocate, the critic and the domain practitioner: a value known at the
     prediction point is a legitimate input, and every stand has an age[^5]; the gap is precision, which the fit
     statement names[^6]. In the source's projection the age of a simulated stand is exact. The column auditor asked
     for your call.
   * **Consistency:** the column auditor cites wadden_sea_sibes_macoma_abundance (same run, issue 5, open), where the
     sediment measured at the visit was replaced by values interpolated from other stations, because the visit's
     value carried a gain. Set apart: sediment exists only where a sample was taken, and a stand age exists for every
     stand. The age is not a leak: it is neither a part nor a consequence of the lichen[^7].
   * **Unknown:** how the paper dated the control plots; it is unread (issue 4). No source here gives a map-level age;
     the cap is the panel's invention.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep the field age (implemented) | the column stays as is; the notes call it a field stand age and give its cost; the fit stays approximate | a value every stand has; the main signal | more precise than the planner's age for old stands |
     | B | Capped age | ages above an assumed fire-record horizon (51 years in NT, 70 in SK) capped; costs R^2 0.007 to 0.032 | closer to a fire record | a horizon we invent |
     | C | Map-level age | rebuilt from the national fire polygons at the coordinates, an external join[^8] | the age a planner reads off a map | a new source, at NT coordinates rounded to about 1 km |
     | D | Field-data actor (the column auditor's) | the actor becomes one who has field stand data but no lichen survey (a ground inventory plot)[^9] | the age is then known as given | replaces issue 1's range-plan actor |

   * **Recommendation:** A: every stand has an age, it is the main signal, and its extra precision is worth at most
     0.032 R^2 here. If your answer to wadden_sea's issue 5 becomes a rule, this case gets checked against it.
     **Decision:** A, B, C or D?

   **Notes for the AI:** A is in `known`, `use_case` and `fit_reason` (a field stand age) and in the notes (its cost).

   [^5]: **USE-3** (Must): name the prediction point and what is known then. **USE-6** (Must): anything known at
     the prediction point is a legitimate input.
   [^6]: **USE-8** (Must): write how closely the data mirrors the use case; approximate is a stand-in with a known
     gap, named as such.
   [^7]: **LEAK-10** (Must): a feature never gives the target away; out are a part, a consequence or another encoding
     of the target.
   [^8]: **CLEAN-19** (Should): we build a feature only for listed reasons, such as removing a leak with the least
     loss or restoring meaning the source destroyed.
   [^9]: **USE-9** (Should): before settling on approximate, ask whether the data mirrors another well-defined use
     case practitioners have; if so, that is the use case and the fit is direct.

   **Andrej (2026-11-03, discuss):** I don't understand it. Give me better context on this.

   **Answer (AI, 2026-11-03):**

   * **Problem:**
     - The input "years since fire" is how long ago the stand last burned, and it is the strongest input of the task.
     - For burned stands a planner reads it off the fire maps, and the survey's value is the same; for old stands that
       never burned within the fire record, the survey counted tree rings, while a planner only knows "older than the
       record".
     - The question is whether to keep the tree-ring ages of those old stands, 36% of the rows.
   * **How the survey got the age**[^2a]:
     - The sites were chosen from the fire maps: in the Northwest Territories burns 37-38 and 46-49 years old, plus
       "controls" in areas with no recorded burn, older than 70 years.
     - At every site the crew cored four or five trees and counted rings. Where the trees formed one age cohort, the
       fire year is that cohort's start; where they did not and no fire is recorded, the age is "the ring count of the
       oldest sampled tree".
   * **What a planner has:** for a burn, the fire year from the national fire database, so the same value. For a
     control stand, only "no fire since the record began" or the forest inventory's age class, coarser than a ring
     count (the controls carry 33 to 241 years).
   * **Effect on the task:** for the controls the model gets a sharper age than the planner would. Measured: capping
     the age at the fire record's horizon (70 years, the paper's control class) costs the models 0.007 to 0.032 R^2,
     within about one standard error.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep the ring-count age (implemented) | the column as the survey gives it; the notes name the gap | the strongest input as the source used it; the gap costs little | the controls' age is sharper than a planner's |
     | B | Cap at the fire record | ages above 70 years become 70, "older than the record" | the age a planner has | loses the age differences among old stands, which the paper's growth curve uses |

   * **Recommendation:** A: the gap concerns only the old stands, costs at most 0.032 R^2, and the paper's own
     forecast uses the same ages. **Decision:** A or B?

   [^2a]: Greuel et al. 2021, Methods, "Site selection" and "Forest stand composition and structure".

   **Resolved (2026-11-03, Andrej):** A, the ring-count age stays, with its gap named in the notes.

3. **Accept the two duplicate-row warnings with these reasons?**

   * **Problem:**
     - Every input describes the plot, so the quadrats of a plot share one feature vector and differ only in their
       lichen.
     - The checks flag this in two duplicate-row warnings; accepting them keeps the rows with a note.
   * **Background:** the checks flag 532 exact copies (`dataset_duplicate_rows`) and, by their own count, 980 rows
     that share their inputs with a row of another target (`dataset_conflicting_duplicate_rows`; 1,671 rows sit in an
     input group with more than one target). Repeats like these, few features and plausible copies, are natural and
     kept with a note[^10].
   * **Experiments:** each feature vector stays in one group, so no test row has a copy in training (leak probe: 0.0%
     on the shipped splits). Of the 532 exact copies, 518 are at 0. 32.5% of the target's variance lies within
     identical inputs (28.8% within a plot). The counts are the same after the repair and the re-split.
   * **Consistency:** follows breast_cancer_prediction, expresso_churn_prediction_1m and
     california_house_prices_2020, which keep real repeats[^11]. wine_quality and jm1 are set apart: their copies
     crossed an IID split.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep the copies, accept both warnings as worded (implemented) | the rows stay; the two warnings are added with the reasons in the notes below | real quadrats kept; the copies never cross the split | none found |
     | B | Drop the 532 exact copies, as wine_quality and jm1 | 532 rows fewer, 518 of them zeros; the zero share falls | follows wine_quality and jm1 | deletes real quadrats to fix copies that never cross the split |

   * **Recommendation:** A, accept both: the copies are real quadrats and none crosses the split (0.0% of test rows
     have a copy in training). **Decision:** A as worded, or B?

   **Notes for the AI:** the copies are kept now, but `accepted_check_warnings` stays empty until the curator
   accepts (add-dataset step 6). The proposed entries:
   `dataset_duplicate_rows`: "532 exact copies, 518 of them at 0: quadrats of one plot (482) or of sibling plots that
   share every input (36), since every input is a plot attribute. Each copy stays in one group, so no test row has a
   copy in training (LEAK-18: few features, natural repeats)."
   `dataset_conflicting_duplicate_rows`: "Quadrats of one plot share their inputs and differ in lichen. 32.5% of the
   target's variance lies within identical inputs (28.8% within a plot), a floor no model can go below. Each input
   vector stays in one group."

   [^10]: **LEAK-18** (Should): many degrees of freedom and an exact match is a collection artefact, dropped; few
     features and plausible repeats are natural, kept and said so.
   [^11]: Lennart, 2026-10-21: keep real repeats.

   **Resolved (2026-11-03, Andrej):** A. Both warnings are accepted in `accepted_check_warnings` with the reasons
   above; `dataset check` gives 0 errors and 0 warnings.

4. **Read the paper's Methods?**

   * **Problem:**
     - Greuel et al. 2021, Ecosphere 12:e03481 ([doi:10.1002/ecs2.3481](https://doi.org/10.1002/ecs2.3481)), is CC BY
       4.0, but Wiley answers 403 to automated requests, so the AI did not read it.
     - A claim about a paper needs a reference to text that was read[^12], so every claim about it is marked
       unverified[^13].
   * **Unknown:** four points the files do not settle:
     * how the stand age was dated for control plots and unburned remnants (issue 2);
     * why 20 NT and 31 SK plots are missing from the lichen sheets, against the 346 and 221 in the abstracts. The
       20 NT plots are in Dryad's quadrat cover sheet, so the authors left them out of the lichen sheet;
     * whether the paper reports a prediction error. A metric of the source would replace the fallback RMSE[^14];
     * the volume allometry. The NT target reproduces as 12.633 x the sum of cover x live depth, but the SK
       conversion cannot be reproduced from the files.
   * **Effect on the task:** nothing shipped today; an answer can reopen issue 2, the metric or the target note.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Leave the points unverified (implemented) | every claim about the paper stays marked unverified in the notes | no wait | issue 2 rests on an unread method |
     | B | You open the paper | in a browser: the DOI, or the Wayback Machine's copy of the publisher PDF of 2021-07-16 | settles the four points; the stand-age method decides how firm issue 2 is | your time |

   * **Recommendation:** B, read the Methods; the stand-age method decides how firm issue 2 is. **Decision:** A, or B
     and send the four answers?

   **Notes for the AI:** the Wayback copy is claim audit row 33.

   [^12]: **PROV-16** (Must): any claim attributed to a paper comes with a text reference (section, table or page,
     and the sentence quoted) from text you read.
   [^13]: **PROV-17** (Must): when a paywalled paper matters and no free copy turns up, ask the curator for the PDF;
     going on without it, mark the claim as unverified.
   [^14]: **MET-1** (Must): the declared metric scores the real task; look at the source's evaluation and the paper
     that defined the task before falling back.

   **Andrej (2026-11-03, discuss):** I could read the full article through Wiley's HTML page. The blanket "paper
   unread" warning is now outdated. The text settles several questions: forest age by tree-ring dating (Methods,
   "Forest stand composition and structure"); the target is volume-based biomass, live height, Saskatchewan's total
   heights adjusted by a live-to-total ratio of 0.76 (Methods and Table 4); a pooled allometry with no significant
   variation across ecoprovinces (Results, "Allometric equations"), so the claim of different regional conversions
   needs reconciliation; observed-versus-fitted R² = 0.18 without held-out evaluation (Results, "Combined
   predictions"); no explanation of the missing plots. We can now replace the blanket warning with specific
   references for confirmed claims. Exact spreadsheet reproduction and missing-plot explanations remain separate
   questions.

   **Resolved (2026-11-03, Andrej):** the notes now cite the paper by section, from the publisher's PDF (Wayback
   Machine copy of 2021-07-16), and the blanket warning is gone. Changed: the stand age bullet quotes the tree-ring
   method; the target bullet names the one pooled allometry (12.633 is its volume slope in kg/ha) and the 0.76
   live-height ratio for Saskatchewan, and the claim of two regional conversions is removed; the source's metric
   bullet quotes the in-sample R^2 of 0.18 (issue 6). Still open, as notes: the Saskatchewan target cannot be
   reproduced from the files (no Saskatchewan cover sheet), and the 20 NT and 31 SK missing plots are explained
   nowhere; the paper counts 2,014 quadrats "across 567 sites", close to our 2,010.

5. **Train on kg/ha while the siblings ship log1p?**

   * **Problem:**
     - Four sibling datasets of this run ship their skewed nonnegative target as log1p; this one ships kg/ha as is.
     - The metric is RMSE on kg/ha either way[^15].
     - What changes is the scale the models train on.
   * **Background:** the four siblings use `target_transform="log1p"` and score RMSE after the inverse:
     pennsylvania_oak_hickory_regeneration_experiment, wadden_sea_sibes_macoma_abundance,
     nantucket_sound_sea_duck_aerial_survey_counts and noaa_afsc_bottom_trawl_survey_cpue (AI drafts, none decided).
     Logging a skewed target is decided case by case[^16].
   * **Experiments:** on the 30 shipped splits, trained on log1p and back-transformed, every family scores below the
     training mean on RMSE in kg/ha. The critic found the same on the former site splits (ridge R^2 0.132 against
     -0.050).

     | family | skill, trained on kg/ha | skill, trained on log1p | splits where log1p is worse |
     |---|---|---|---|
     | random forest | +0.097 | -0.045 | 29 of 30 |
     | small LightGBM | +0.103 | -0.030 | 28 of 30 |
     | ridge | -0.085 | -0.126 (median; far below on one split) | 27 of 30 |

   * **Why, as the AI reads it:** a log model back-transformed predicts about the geometric mean, far below the mean
     that RMSE rewards when 40% of the quadrats are 0. wadden_sea's notes report the same effect, so this fact may not
     set this dataset apart from its siblings.
   * **Consistency:** there is no curator precedent.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | kg/ha here (implemented) | models train on kg/ha as is; the measurement is the reason in the notes | better than log1p on 27 to 29 of 30 splits per family | departs from the siblings |
     | B | log1p like the siblings | models train on log1p (`target_transform="log1p"`), still scored by RMSE on kg/ha | one scale for the family | every probed family falls below the mean on the benchmark's own metric |
     | C | kg/ha here, reopen the siblings | as A, and the four siblings' log1p rechecked the same way | one measured reason for the family | none found |
     | D | A rule for the family | an amendment of the log rule for skewed nonnegative targets scored by RMSE | settles the family at once | a rule change with no curator precedent |

   * **Recommendation:** C: trained on log1p, every probed family falls below the training mean here, and
     wadden_sea's notes report the same effect, so the siblings need the same check. Decided together with wadden_sea's issue 3 (the family's metric). **Decision:** A, B, C or
     D?

   [^15]: **MET-3** (Must): the metric is on the scale the task means; the target may ship on the scale a practitioner
     models it on (`target_transform`), and the metric is computed after the inverse.
   [^16]: **CLEAN-16** (Should): log a skewed positive target when the source has not, case by case.

   **Andrej (2026-11-03, discuss):** The siblings are not real siblings! They are different tasks and each should be
   treated differently. For each, we want to use what suits the task and practitioner needs best.

   **Answer (AI, 2026-11-03):**

   * **Problem:**
     - Agreed: the four other datasets are other tasks, so this one is decided on its own, and options C and D, which
       tied it to them, fall away.
     - For this task the planner needs forage in kg/ha, the paper reports kg/ha, and models trained on kg/ha score
       better than models trained on log1p on 27 to 29 of 30 splits per model family.
   * **Recommendation:** A, kg/ha, for this task's own reasons. **Decision:** A or B?

   **Andrej (2026-11-03, change):** I go with your recommendation

   **Resolved (2026-11-03, Andrej):** A, kg/ha, as implemented; the notes give this task's own reasons.

6. **Score by R^2, as the paper does, or by RMSE?**

   * **Problem:**
     - The paper judges its model by R^2: "the R2 of a linear regression between measured lichen biomass and predicted
       lichen biomass", 0.18, on the data it was fitted to[^6a].
     - That R^2 is a squared correlation: a forecast that is twice too high scores as well as a correct one, so it
       cannot rank models alone.
     - The benchmark can score the coefficient of determination R^2 (1 - squared error / variance) instead, which ranks
       models like RMSE within a fold and reads on the paper's scale.
   * **Effect on the task:** within one test fold R^2 and RMSE rank models the same; across folds R^2 divides each
     fold's error by that fold's variance, so the mean over folds can rank models differently.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | RMSE on kg/ha (implemented) | the fallback, error in kg/ha | in the planner's unit | not the source's measure |
     | B | R^2, coefficient of determination | `r2` on kg/ha, as a stand-in for the paper's R^2 | the source's measure in a form that punishes a biased forecast; readable against the paper's 0.18 | a different number from the paper's in-sample R^2 |
     | C | The paper's squared correlation | R^2 of observed on predicted | exactly the source's measure | ignores bias and scale; a constant offset scores perfect |

   * **Recommendation:** B: it keeps the source's measure and only fixes what makes it unfit to rank models[^6b].
     **Decision:** A, B or C?

   [^6a]: Greuel et al. 2021, Methods, "Modeling site-level mean biomass", and Results, "Combined predictions".
   [^6b]: **MET-1** (Must): look at the source's evaluation before falling back.

   **Andrej (2026-11-03, discuss, on the metric):** But what were the metrics used by the source?

   **Andrej (2026-11-03, ok):** We can keep RMSE in this case

   **Resolved (2026-11-03, Andrej):** A, RMSE on kg/ha; the metric reason and the notes say why the paper's R^2 is not
   declared.

7. **Score per quadrat, which counts an NT plot 2.5 times an SK plot, or count each plot once?**

   * **Problem:**
     - Every input describes the plot, so a model predicts one value per plot, and the RMSE over quadrats ranks models
       exactly like a score over plots in which each plot counts by its number of quadrats, 5 in the Northwest
       Territories (NT) and 2 in Saskatchewan (SK).
     - An NT plot therefore counts 2.5 times an SK plot, a weighting set by the two survey protocols, while the range
       planner acts on stands.
     - Should the score stay per quadrat, with that weighting stated in the notes, or should each plot count once?
   * **Background:**
     - With one prediction per plot, the per-quadrat mean squared error splits exactly into a floor, the spread of each
       plot's quadrats around their mean (the same for every model), plus the plots' squared errors weighted by their
       quadrats; so the per-quadrat RMSE orders models exactly as that weighted plot score does (Kendall tau 1 on all
       30 shipped splits; Kendall tau measures how far two orders of the models agree, 1 when they are the same)[^17].
     - The 516 plots are 326 NT plots of 5 quadrats and 190 SK plots of 2, so NT holds 81% of the quadrats but 63% of
       the plots. Below, "per plot" means each plot counted once.
     - SK's 4 m² quadrats average out more of the lichen's patchiness than NT's 1 m² quadrats: 15.6% of the SK
       target's variance lies within a plot, against 33.2% of the NT target's.
     - The weighting is no exposure: the target is already biomass per hectare, and each protocol fixes its quadrat's
       area[^20].
     - The paper's "site" is our plot, and the paper uses both units: its presence model counts the quadrats with and
       without lichen in each plot, its biomass model is fitted to one mean per plot with a separate residual variance
       for each survey, which the authors tie to "the difference in quadrat sizes and numbers", and it does not say at
       which level its R2 of 0.18 is computed (its Fig. 6 plots quadrat-level values)[^24].
   * **Rules:** no rule is broken under either option: both score stands and keep the source's rows[^17][^19]. The
     rule that a map of equal areas is scored with each unit counted once is written for rates with a realized
     denominator, which this target lacks, so it does not bind here, though it points to B[^18]. The call is a
     weighing.
   * **Effect on the task:** the models' errors differ by region, so the weighting decides which region's errors count
     more. On the split where the two scores agree least (repeat 1, fold 2; Kendall tau 0.00), the training mean ranks
     2nd of 8 per quadrat and 7th per plot (RMSE 766 kg/ha on the NT quadrats, 1,288 on the SK quadrats), and the full
     LightGBM 7th per quadrat and 2nd per plot (RMSE 897 kg/ha on the NT quadrats, 937 on the SK quadrats). Over the
     30 splits the effect is small (Experiments).
   * **Experiments:** the claim auditor's run, reproduced by the mediator: 8 untuned predictors (random forest, extra
     trees, two LightGBM, two ridge, knn and the training mean) on the 30 shipped splits, the 516 plots rebuilt from
     the raw sheets.
     - Per quadrat against per plot, Kendall tau is 0.81 per split on average (lowest 0.00) and 0.86 for the ranking
       by the mean RMSE over the splits; with a median and a zero predictor added, 0.84 and 0.91.
     - 81 of the 840 comparisons of two models on one split change order (9.6%), 40% of them between models whose
       difference over the 30 splits is noise (paired t between -2 and 2); the same model is best under both scores
       on 80% of the splits.
     - In the ranking by the mean RMSE only two pairs swap, both within noise: the training mean against ridge
       (paired t -0.45) and against knn (t -1.14). The top pair, small LightGBM against random forest (1,151.6
       against 1,155.5 kg/ha, t -0.35), keeps its order.
     - By the mean rank per split, as TabArena ranks models, the 8 predictors give tau 0.86: the first two and the
       last three places agree, and only the two ridges and extra trees reorder. The claim audit gives 0.81 for this
       ranking under "8 models", but its run ranked 10, the median and zero predictors included (re-checked from its
       per-split scores: 0.857 for the 8, 0.809 for the 10).
   * **Panel:** the claim auditor raised the weighting as a short optional question, not a blocking issue, and
     recommends A; the mediator agrees and puts B to you, because the rule on equal-area maps gives it a principled
     case.
   * **Consistency:**
     - noaa_afsc_bottom_trawl_survey_cpue scores its density unweighted, the area swept folded into the target by the
       source, as A does here[^21].
     - superconductivity and the call to keep real repeats keep the source's rows, as both options do[^22].
     - liberty_mutual_fire_peril_loss_cost and g_research_crypto_forecasting_1m read a metric weight that is a
       function of the features, with no training weight: the pattern B would follow[^23].
     - No precedent decides between one vote per group and one per row for groups with unequal numbers of rows; B
       would set one, and the same question would then reach other datasets with unequal replicates per unit.
   * **Unknown:** what would settle it:
     - whether you want each stand to count once in this task.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Per quadrat, weighting stated (implemented) | RMSE over all quadrats, as now; the notes say that an NT plot counts 2.5 times an SK plot and how far the ranking differs from counting each plot once | the source's rows scored as they are; in the ranking by mean RMSE over the 30 splits only two pairs swap, both within noise | SK plots count less, by the survey protocol rather than the planner's need |
     | B | Each plot counts once | RMSE weighted by 1 over the plot's quadrats (0.2 in NT, 0.5 in SK), a weight column for scoring only, not for training; RMSE first needs a weight input in the framework | one vote per stand, the unit the planner acts on; ranks models exactly as the per-plot score | a framework change and one more scoring column for a ranking change of noise size; a new precedent for groups with unequal numbers of rows |

   * **Recommendation:** A: no rule is broken under either option, the rows are the source's, and in the ranking by
     mean RMSE over the 30 splits the two scores swap only two pairs, both within noise (on single splits 9.6% of the
     pairs swap); the paper uses both units, so it does not decide the choice; B, if each stand should count once,
     costs a framework change for an effect of that size. **Decision:** A or B?

   **Notes for the AI:** on A, nothing changes: since 2026-11-06 the notes' bullet "Every input is constant within a
   plot" states the 2.5:1 weighting and the per-plot taus. On B: (1) `rmse` takes no `weight` input today
   (`_check_input_roles` refuses `inputs={"weight": ...}` on it, checked 2026-11-06), so first give `rmse` an optional
   row weight in `src/data_foundry/v2/metrics.py`, with a test; (2) in `_clean`, add `plot_weight`, 1 over the plot's
   quadrats (0.2 in NT, 0.5 in SK, from `plot` before it is dropped), declared as
   `ScoringColumn(column="plot_weight", role="weight", used_by="rmse", ...)`; (3) `Metric.fallback` takes no inputs,
   so the metric becomes `Metric.from_context("rmse", reason=..., inputs={"weight": "plot_weight"})`, and
   `sample_weight` stays unset; (4) accept `task_metric_weight_without_sample_weight` with MET-15's reason for a metric
   weight that is a function of the features (it follows from `jurisdiction`), as liberty_mutual_fire_peril_loss_cost
   words it for `var11_weight`; (5) replace the notes' sentence on the 2.5:1 weighting, re-run `dataset check`, and add
   a CC line to the record and a CHANGELOG entry. The taus come from the claim auditor's run of 2026-11-06 (true plot
   ids, 8 and 10 predictors). Its mean-rank tau of 0.81 is the 10-predictor value, although its Q files it under 8
   models (the rank table of its run lists all ten); recomputed from its per-split scores, the mean rank gives 0.857
   for the 8 predictors and 0.809 for the 10. The paper's units are quoted in the last footnote.

   [^17]: **SPLIT-23** (Must): the source's use case, cited, decides what one prediction is (a row, or a whole group:
     replicates averaged, any instance positive, the latest row, the best of several candidates). Both options score
     stands; they differ only in how much each stand counts.
   [^18]: **MET-15** (Must), its last clauses: "When the decision is per unit of an equal-area map, per loan or per
     contract, the rate is scored unweighted and no sample weight is declared"; a metric weight that is a function of
     the features needs no sample weight, and the bundle check `task_metric_weight_without_sample_weight` is then
     accepted with that reason. The rule is written for a rate whose denominator is realized; here the area is fixed
     by the protocol.
   [^19]: **SPLIT-26** (Should): keep the source's rows; deduplicating with averaged targets is a different dataset.
   [^20]: **MET-14** (Should): a count or amount accrued over a varying amount at risk (time on risk, vehicle-years,
     area swept) ships as the rate per unit when the decision prices or maps per unit; the source ships kg/ha.
     **LEAK-41** (Must): a weight or denominator set after the prediction point is never an input; the quadrat's area
     is set by the protocol, not realized.
   [^21]: noaa_afsc_bottom_trawl_survey_cpue: the catch per km² swept, scored unweighted on the density (Lennart,
     2026-11-06, its issue 4).
   [^22]: superconductivity (SPLIT-26) and Lennart, 2026-10-21: keep real repeats.
   [^23]: liberty_mutual_fire_peril_loss_cost (`var11_weight`) and g_research_crypto_forecasting_1m (the asset
     `Weight`): a metric weight that is a function of the features, with no sample weight (MET-15, 2026-11-06).
   [^24]: Greuel et al. 2021, read on 2026-11-06 in the Wayback Machine copy of the publisher's PDF
     ([snapshot of 2021-07-16](https://web.archive.org/web/20210716062943/https://esajournals.onlinelibrary.wiley.com/doi/pdfdirect/10.1002/ecs2.3481)).
     Methods, "Field sampling": "Square plots in SK and belt transects in the NT are referred to in aggregate as
     'sites.'" Methods, "Modeling site-level mean biomass": "We averaged to site level"; "The observations were counts
     of quadrats with and without lichen presence within sites"; "The second stage modeled site mean lichen biomass
     density, conditional on lichen presence"; "We accounted for heterogeneous sampling variance among study designs,
     which reflects the difference in quadrat sizes and numbers, using the varIdent function in nlme"; "We assessed
     the accuracy of our final model by the R2 of a linear regression between measured lichen biomass and predicted
     lichen biomass." Fig. 6: "points are quadrat-level values used in these models."

   **Resolved (2026-11-08, Lennart):** B, each plot counts once. `rmse` got an optional `weight` input, and the RMSE
   on kg/ha is now weighted by `plot_weight`, 1 over the plot's number of quadrats (0.2 in NT, 0.5 in SK), a scoring
   column for the metric only with no sample weight (the bundle warning accepted); the notes, the metric's reason and
   the record say so.

8. **Group the Saskatchewan plots by burn, taken from the national fire maps, instead of one group per plot?**

   * **Problem:**
     - Saskatchewan (SK) plot names carry no burn key, so each SK plot is its own group (dataset.py:269), while the use
       case asks for stands in burns nobody surveyed (dataset.py:112-118)[^8a].
     - 71 of the 190 SK plots have another SK plot of the same fire year (the survey year in the plot name minus the
       years since fire) within 5 km, and 26 within 1 km (counted on the raw file), so many SK test plots likely have
       a plot of their own burn in training.
     - Keep one group per plot with a note, or recover each SK plot's burn from the national fire polygons?
   * **Background:**
     - At 5 km the 71 plots form 24 clusters of 2 to 7 plots; a quarter of them are 4 or 5 years after fire, the
       median 34 years, and for old stands the fire year is a field estimate from tree rings, so a shared year is a
       weaker sign of one burn there (counted on the raw file; dataset.py:198).
     - Issue 1 already calls SK the laxer region (REVIEW.md:99): an SK test quadrat lies a median 3.7 km from the
       nearest training plot against 22 km in the Northwest Territories (NT), and SK plot means correlate at r 0.73
       under 1 km (16 pairs) and 0.42 at 2 to 5 km (dataset.py:200).
     - Canada's National Fire Database (CNFDB) and the National Burned Area Composite (NBAC) publish burn polygons
       with a fire id and a year; an SK plot inside a polygon of its fire year would take that burn's id, and a plot
       outside every polygon (an old or unmapped fire) would stay on its own (an AI reading; their SK coverage by year
       was not checked).
     - The SK sheet gives the coordinates to 12 or 13 decimals, so a point-in-polygon join is possible (counted on the
       raw file).
   * **Effect on the task:** an SK test plot with a burn-mate in training is scored as filling in a burn already
     surveyed, which is easier than the burn nobody surveyed that the use case names, so the SK part of each fold
     flatters models that lean on the coordinates (an AI reading); the size is not measured.
   * **Consistency:** NT is grouped on the recorded burn-area key of its plot names because under the site split 94.3%
     of NT test quadrats had another site of their own burn area in training (issue 1, Andrej, 2026-11-03); SK has the
     same problem without a recorded key[^8c].
   * **Unknown:** how many of the 71 plots, and of the 190, fall inside a CNFDB or NBAC polygon of their fire year;
     the join would settle it.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | One group per plot, with a note (implemented) | as now; the notes add that 71 of 190 SK plots have a same-fire-year plot within 5 km | no outside data; a group from a recorded key | SK test plots can have a burn-mate in training, against the use case's burn nobody surveyed |
     | B | Burn id from the national fire polygons | each SK plot's coordinates and fire year joined to the CNFDB / NBAC polygons; plots inside one burn form one group, the rest stay on their own | gives SK the test the use case names; an exact key from a recorded source | an outside dataset; old or unmapped fires stay per plot; a polygon's year and the field fire year may disagree |
     | C | Cluster by distance and fire year | plots of one fire year within 5 km form one group (24 groups of 2 to 7 plots) | no outside data | a distance-threshold cluster, which the group rules forbid; a shared year can be chance for old stands |

   * **Recommendation:** B: it gives SK the test the use case states while the group still comes from a recorded key,
     and the plots no polygon covers stay on their own as now; A if the join finds few of the 71 inside a polygon of
     their year[^8b]. **Decision:** A, B or C?

   **Notes for the AI:** On B: download the CNFDB fire polygons (`NFDB_poly`, Natural Resources Canada) and NBAC, check
   their licence (Open Government Licence - Canada is expected) and add them to `download_description`; join the 190
   SK plot coordinates point-in-polygon and keep a polygon whose year equals the plot's fire year (survey year minus
   `TSSRF`; allow 1 year for the mapping); the group is `SK:` plus the fire id, else `SK:` plus the plot; feed the key
   to `_linked_groups`; recount the groups, the fold sizes and the SK distance to training; rewrite
   `task_summary.split`, the grouping definition and `splits_comment`; re-run `dataset check`, the group probe and the
   task probe on the cluster; CHANGELOG and a CC line. On A: add the 71 / 26 counts to the notes' SK bullet
   (dataset.py:200). The rules: SPLIT-1, SPLIT-4, SPLIT-24, SPLIT-25, SPLIT-26.

   **Andrej (2026-11-09, change):** Option B: Burn id from the national fire polygons. Before finally adding this,
   ablate it and analyze the impact of this decision

   **Answer (AI, 2026-11-09):** B is now implemented; mark as implemented to settle it.

   * **The join:** the 190 SK plots against the agencies' fire perimeters (NFDB, SK from 1945) and the National Burned
     Area Composite (NBAC, from 1972), both Open Government Licence - Canada, point in polygon, keeping a polygon whose
     year is within 1 of the plot's fire year:
     - 94 of the 190 plots fall inside one (NFDB 87, NBAC 76): 94 of the 124 dated 1945 or later, none of the 66 dated
       earlier; 44 of the 71 plots with a same-year plot within 5 km (of the other 27, 23 are dated before 1972 and
       four are of 1981 and inside no polygon of 1980 to 1982).
     - They form 45 burns: 20 of 2 to 9 plots hold 69 plots, 25 hold one. Burn-mates lie a median 3.9 km apart (at
       most 65 km, in a fire of 1981 of 355,000 ha); the key is polygon membership, an exact key, not a distance
       cluster[^8d].
     - The map's year equals the field fire year in 157 of the 165 matches (the rest 1 year off), and NFDB and NBAC
       put 66 of the 67 plot pairs they both cover in one burn.
     - Disagreement: 42 plots lie inside a fire the maps date after their field fire year (and before the survey) and
       inside none of their own year, 33 of them dated before 1945: unburned stands inside a perimeter, or a field age
       the maps contradict. They stay on their own, as do the plots outside every polygon.
   * **The ablation:** untuned ridge, random forest and LightGBM on the container's inputs (no `plot`), 3 seeds, each
     grouping on its own 30 shipped splits; RMSE in kg/ha weighted by `plot_weight`, mean over the splits with its
     standard error; the SK distance is the median distance of an SK test quadrat to the nearest training plot, per
     split, mean over the splits with the SD:

     | Grouping | Groups (NT + SK) | SK test to training | Forest RMSE, all | Forest RMSE, SK rows | Forest skill, SK rows |
     |---|---|---|---|---|---|
     | One group per SK plot | 216 (26 + 190) | 3.4 km (SD 0.6) | 1,166.8 (SE 29) | 1,230.3 (SE 40) | +0.117 (SE 0.053) |
     | B, burns from the fire maps | 167 (26 + 141) | 4.3 km (SD 0.7) | 1,186.3 (SE 24) | 1,254.1 (SE 47) | +0.072 (SE 0.063) |

     - On the SK rows LightGBM (skill +0.102, then +0.105) and ridge (+0.163, then +0.166) do not move; the forest's
       drop is within its spread. The NT part, whose groups did not change, moves as much through the new fold draw
       (forest 1,134.0 to 1,120.1, ridge 1,234.8 to 1,153.6), so the switch is within the fold draw.
     - Whether the burn-mates inflated the score, paired on the former folds: taking the burn-mates of the SK test
       plots out of training (about 23 test plots and 29 training plots per split) raises the forest's RMSE on those
       plots by 31 kg/ha (SE 9; 5% of 572) and LightGBM's by 36 (SE 17), ridge's by 5 (SE 3); taking out as many
       other SK plots moves them by +2 to +6, -2 to -3 and +1 to +4. So the burn-mates did help the trees, but those
       plots are a third of the SK test plots and low in lichen: about 5 kg/ha on the SK RMSE and 2 kg/ha overall.
     - Task probe on B, on the model inputs (without `plot`): forest 1,182.6 against the training mean's 1,245.6,
       better on 90% of the splits, no flag (1,164.3 against 1,250.0 and 77% with one group per SK plot). Group probe:
       LightGBM R^2 0.380 on random folds against -0.015 on the burn folds (0.408 and -0.035 before). Leak probes: no
       flag.
     - Cost: about 2 GB of fire maps next to the raw files, read once in about 20 s by `_prepare_raw_files` (a
       shapefile reader on numpy and matplotlib, since the build extras have no geo library; it finds the same
       plot-polygon pairs as geopandas) into a table of the polygons that hold an SK plot. NFDB keeps only its current
       version online, so a newer one stops the build until its file names are updated.

   **Andrej (2026-11-09, discuss):** Rethink what you recommend now after the experiment. And explain it concisely.

   **Answer (AI, 2026-11-09):** Go back to A, one group per SK plot with the measured effect in the notes: B removes a
   bias too small to move any score or ranking, and costs an outside download that can break the build.

   * Burn-mates in training flattered the SK RMSE by about 5 kg/ha (2 kg/ha overall), against an SK RMSE of about
     1,230 with a fold-draw SE of 40.
   * No model moves in rank: ridge and LightGBM score the same on the SK rows under both groupings; the forest's drop
     is within its spread.
   * B reaches only the 94 of 190 SK plots inside a mapped fire; the 66 dated before 1945 and the other unmapped burns
     stay one group per plot under B too.
   * B's cost: 2 GB of fire maps, a hand-written shapefile reader in the definition, and NFDB keeps only its current
     version online, so a later build can stop until the file names are updated.

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | a | Back to A, with the note (implemented) | one group per SK plot; the notes add that 94 of 190 SK plots share a mapped burn and that burn-mates flatter the SK RMSE by about 5 kg/ha | no outside data; the build depends on the source alone | SK test plots can have a burn-mate in training |
     | b | Keep B | burns from the fire maps | the use case's unsurveyed burn for half the SK plots | an outside download that can break the build, for a 5 kg/ha effect |

   * **Recommendation:** a. **Decision:** a or b?

   **Andrej (2026-11-10, change):** Reply (a): Back to A, with the note

   **Resolved (2026-11-10, Andrej):** a. Each SK plot is its own group again (216 groups, 26 NT and 190 SK, the folds
   of before 2026-11-09). The fire-map join is removed from the definition (no NFDB or NBAC download, no prepared
   polygon table, no Decision); the issue-9 site-sheet coordinates stay. A notes bullet gives the measured effect: 71
   of 190 SK plots have a same-fire-year plot within 5 km, 94 of 190 lie inside a mapped burn of their year,
   burn-mates in training flatter the SK RMSE by about 5 kg/ha against a fold-draw SE of about 40, no model changes
   rank, and why the maps are not used. Re-run on 2026-11-10: `dataset check` clean; task probe random forest 1,164.3
   kg/ha against the training mean's 1,250.0 (better on 77% of the splits), no flag; group probe LightGBM R^2 0.408 on
   random folds against -0.035 on the burn-area folds; leak probes no flag; the same numbers as before 2026-11-09.

   [^8a]: **SPLIT-1** (Must, in main): the split mirrors the real application. **SPLIT-4** (Must, in main): "If the
     deployed model predicts for an entity new data would not contain ..., the test entities must be new".
   [^8b]: **SPLIT-24** (Must, in main): "Group on a true group id, or on one constructed exactly from the data ...
     Never on a similarity-threshold cluster". That a burn id from a point-in-polygon join counts as a true group id is
     an AI reading. **SPLIT-26** (Should): "Take the group key from the source's own data"; B departs from it for a key
     the source does not record.
   [^8c]: Issue 1 (Andrej, 2026-11-03): A, "the range-plan actor and the burn-area split", with the con "SK stays the
     laxer region (test median 3.7 km from training)".
   [^8d]: **SPLIT-24** (Must, in main): "Group on a true group id, or on one constructed exactly from the data ...
     Never on a similarity-threshold cluster". **SPLIT-26** (Should): "Take the group key from the source's own data";
     the burn comes from a second recorded source, the plot's own fire year and coordinates matched exactly to it. That
     polygon membership counts as a true group id is an AI reading.

9. **Ship the NT plots' coordinates at the precision of the authors' site sheet instead of the 0.01 degree grid?**

   * **Problem:**
     - The NT coordinates ship on a 0.01 degree grid (dataset.py:92-93, :194), while the authors' site sheet
       `All_site_info_NT.xlsx` in the same deposit gives each plot's transect start to 4 to 6 decimals (counted on the
       raw file).
     - The grid is how the published NT lichen sheet gives its coordinates (two decimals), and the definition keeps it
       because the one link between two burn areas, CG2 with F2, rests on an exact shared grid coordinate
       (dataset.py:194, :199).
     - Ship the site sheet's coordinates as the features and keep the grid only to build that link[^9a]?
   * **Background:**
     - For the 323 NT plots that were not repaired, the grid point lies a median 0.31 km from the site sheet's start
       (90th percentile 0.51 km, at most 0.59 km); on the grid 244 of the 326 NT plots share their coordinate with
       another plot (94 shared points, mostly the A and B plots of one site), in the site sheet none do (counted on
       the raw files).
     - The SK sheet gives its coordinates to 12 or 13 decimals, so only NT is coarse (counted on the raw file).
     - Why the authors rounded is not stated: the lichen sheet's metadata says only "Degree, decimal"; privacy is
       unlikely to be the reason, since the same authors put the precise starts in the same CC0 deposit (Dryad
       version 5 of 2026-05-18; dataset.py:23-24, :161) (an AI reading).
     - The site sheet's coordinate is the start of the plot's belt transect, so it places the plot, not each quadrat
       along it.
   * **Effect on the task:** the grid gives the A and B plots of one site the same position, part of the 36 copies
     between sibling plots in the duplicate warning (dataset.py:248-250), and moves a plot by up to 0.6 km; the
     planner knows where the stand is; under the burn-area split the test burns lie a median 22 km from training, so
     the effect on the score is likely small (an AI reading; not measured).
   * **Consistency:** the definition already takes three plots' coordinates from the site sheet, where the grid was
     wrong by 8 to 162 km, but rounds them back to the grid (dataset.py:79, :194)[^9b].
   * **Unknown:** why the lichen sheet was rounded; the contact in its metadata (Jennifer Baltzer) could say.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | The 0.01 degree grid | as now | the lichen sheet as published; the CG2 and F2 link unchanged | up to 0.6 km off; the plots of one site share a position |
     | B | Site-sheet coordinates as features (implemented) | latitude and longitude from the site sheet's transect start for all 326 NT plots; the grid values only build the burn-area link and are not shipped | the stand's position as the planner knows it, at SK's precision; the three repairs need no rounding | the duplicate warnings' counts and reasons change; the start of the transect, not each quadrat's spot |

   * **Recommendation:** B: the stand's location is known when the planner predicts, the authors published it in the
     same deposit, and the link can keep using the grid; the change is small in code and likely in score.
     **Decision:** A or B?

   **Notes for the AI:** On B: in `_repair_nt` (or a new step) map every NT plot to the site sheet's `Lat_start` and
   `Long_start` (text with a decimal comma), keep the grid copy for `_linked_groups` only and drop it before the
   return; the ecoprovince repair of CG3-31A stays; update the repair Decision, the notes (dataset.py:194, :199-200),
   `changes`, the two accepted duplicate warnings (the 36 sibling-plot copies go; recount 532 and 32.5% / 28.8%),
   then `dataset check`, the leak probes and the task probe on the cluster; CHANGELOG and a CC line. The rules: USE-6,
   PROV-13, SPLIT-24.

   **Andrej (2026-11-09, change):** Option B: Site-sheet coordinates as features.

   **Resolved (2026-11-09, Andrej):** B. Every NT plot now ships its transect start from `All_site_info_NT.xlsx` as
   its coordinates; the 0.01 degree grid, with the three repaired plots on it, only builds the CG2 and F2 link and is
   not shipped, so the groups are unchanged. The duplicate warnings are recounted (518 copies, 506 at 0, all within
   one plot; 976 conflicting rows; 28.8% of the variance within a plot), and on the same 30 splits the random forest's
   RMSE moves by +4.2 kg/ha (SE 3.3), within noise.

   [^9a]: **USE-6** (Must, in main): "Anything known at the prediction point is a legitimate input". **SPLIT-24**
     (Must): the CG2 and F2 link is a key constructed exactly from the data (an exact shared coordinate), which B
     keeps.
   [^9b]: **PROV-13** (Must, in main): damaged data is repaired from the origin when the origin has the clean data;
     the repair of 2026-11-01 used the site sheet for the three mislocated plots.

**Review panel:** ship after changes (mediator), wording only, now made. Tier focused, a re-review of 2026-11-06
under LEAK-41 and MET-14 to MET-16 after the exposure rework: the claim auditor and the mediator; no blind review, task
gamer, advocate or critic in this tier. Claims: 12; 8 hold, 2 refuted as labelled (the equal-weight taus, measured per
input vector and not per plot; the lowest split in the panel's change note, which is 0.00), 1 holds in its conclusion
but not its reason (the exposure sentence), 1 untested and not like for like (the 0.91 of the former site splits, now
dropped); those in the definition are fixed in the notes. Agreed: the per-quadrat RMSE is a stand score weighted by
quadrats (tau 1 on 30 of 30 splits), no exposure to declare, no design weight, the source's rows kept. Disputed:
nothing; issue 7 (the mediator's issue 1, the claim auditor's Q) is a weighing call: keep the per-quadrat score, which
counts an NT plot 2.5 times an SK plot, and say so (A, implemented, recommended), or count each plot once (B).

<details><summary>Mediator</summary>

The mediator's issue 1 is issue 7 of this file.

**Mediator report, boreal_postfire_lichen_biomass: focused re-review of 2026-11-06**

This was a focused tier, so there was no advocate, critic or task gamer, and no exploits needed mapping. I re-ran the
claim auditor's decisive experiment: the output is byte-identical to the auditor's, and every number below reproduces.

**Recommendation (judgment record)**

```text
Verdict: ship after changes (wording only; nothing shipped changes).
Validity: SPLIT-23 holds (per-quadrat RMSE = within-plot floor + quadrat-weighted stand score; tau 1.000 on 30/30
  splits, identity gap 9.3e-10). SPLIT-26 holds (source's quadrat rows kept). LEAK-18 holds (0 input vectors span two
  burn areas). LEAK-41 nothing to remove (quadrat area is a protocol constant fixed by `jurisdiction`, not realized).
  MET-14 holds in substance (target already per unit area, kg/ha); its stated reason is wrong (EV-7, fix now).
  MET-15 not triggered as a weight rule (no realized denominator); its equal-area clause opens issue 1. MET-16 holds
  (no design weight in either sheet; stratification is by fire age, a feature).
Value: unchanged (TP-2, small real signal; rmse fallback, Andrej 2026-11-03).
Quality: EV-7 triggered three times, fixed by rewording (tau labels, the 0.91 comparison, the exposure reason).
Weighed: none new.
For the curator: issue 1, a weighing call: per-quadrat scoring counts an NT plot 2.5 times an SK plot; keep and say so
  (A, implemented, recommended) or weight rmse by 1/quadrats-per-plot (B).
```

By the review page's default, with no blocking issue it ships as implemented (option A) once the wording is fixed.

**Changes to make now (no decision needed)**

1. **EV-7. Relabel the equal-weight taus** in the notes bullet "Every input is constant within a plot".
   - The 0.76 per split and 0.71 for the leaderboard were measured with one weight per input vector (498 "stands":
     sibling plots that share every input are merged), not per plot.
   - With the true plot id (516 plots: 326 NT × 5 quadrats, 190 SK × 2) and the same 8 untuned predictors, the numbers
     are 0.81 per split on average (min 0.00) and 0.86 for the leaderboard.
   - Suggested text: "Against the stand score with equal weights per plot (516 plots), tau is 0.81 per split on
     average (min 0.00) and 0.86 for the ranking by the mean over the splits (8 untuned predictors); the order flips
     only between pairs whose difference is noise (leaderboard: mean against ridge, t −0.45; mean against knn,
     t −1.14)."
   - Also say that tau depends on the model set: adding median and zero gives 0.84 per split and 0.91 for the
     leaderboard.
2. **EV-7. Drop the "0.91 on the former site splits (5 untuned predictors)" comparison, or mark it "not like for
   like".**
   - Those splits no longer ship.
   - It used a different model set and possibly the input-vector stand.
   - The earlier mediator block in `REVIEW.md` labels a 0.91 as the tau against the *quadrat-weighted* stand score,
     which today's identity shows is exactly 1. So the old figure's label was already unclear.
   - Leave the settled block as it is; only the notes change.
3. **EV-7 with MET-14. Rewrite the reason in the exposure bullet; the conclusion "none" stays.**
   - "not ... an amount accrued over an amount at risk" contradicts MET-14, which names "area swept" among its
     denominators.
   - Suggested text: "the source already ships the amount per unit area that MET-14 asks for (kg/ha); the sampled
     area (1 m² NT, 4 m² SK) is a protocol constant set by `jurisdiction`, not realized, so LEAK-41 has nothing to
     remove; the planner decides per stand, not per sampled m², so no row weight follows (MET-15)."
   - This matches how noaa_afsc_bottom_trawl_survey_cpue words its effort bullet (CPUE folded by the source, scored
     unweighted).
4. **EV-7. Panel record.** CHANGES.md misstates the lowest split's tau. The builder's own output puts the lowest split
   at 0.000 (repeat 1, fold 2), and none is negative. Any `REVIEW.md` text taken from CHANGES.md must say "min 0.00".
5. **Optional, falls with option A below.** State the implied weighting outright in the notes: "an NT plot counts 2.5
   times an SK plot in the per-quadrat score (NT holds 81% of test quadrats but 63% of test plots on average)."

**Issues for the curator, ranked**

**Issue 1: per-quadrat scoring weights NT plots 2.5:1 against SK plots. Keep it, or score one plot, one vote?**
- **Rules:**
  - SPLIT-23 (Must) says the use case decides what one prediction is. It is satisfied either way, because both scores
    are stand scores; they differ only in the stand weights.
  - MET-15's equal-area clause ("per unit of an equal-area map ... scored unweighted") is written for rate targets with
    a realized denominator, which this target does not have. It therefore does not bind here, but it points towards B.
  - SPLIT-26 (Should): keep the source's rows. Both options keep the rows.
  - No Must is broken under either option. The rules leave this open, so it is a weighing call for you.
- **Effect** (8 models, true plots, 30 shipped splits):
  - 81 of 840 split × model-pair comparisons change order (9.6%), and 40% of those are pairs whose quadrat difference
    is noise (|t| < 2).
  - The same model is best under both scores in 80% of the splits.
  - At leaderboard level only mean/ridge and mean/knn flip, both noise-level.
  - The top pair, small LightGBM against random forest (1151.6 against 1155.5, t −0.35), keeps its order.
  - On TabArena-style mean rank: tau 0.81; the first two and the last three places agree.
  - The cause is the regions. Models differ by region, and the weighting decides which region counts. On the worst
    split (r1 f2), the mean predictor is 2nd per quadrat and 7th per plot (NT error 766, SK 1288).
- **Option A, keep per-quadrat rmse (implemented)**
  - What it does: corrects the numbers (changes 1 to 3) and states the 5:2 weighting (change 5).
  - Best evidence: flips occur only between noise-level pairs, and the source's rows are kept (SPLIT-26). Earlier,
    Andrej approved "the quadrat rows" with the fallback rmse (2026-11-03).
  - Cost: SK, with larger quadrats and a 0.156 within-plot variance share (NT 0.332), counts less. That is a choice
    of the survey protocol, not of the planner.
- **Option B, one plot, one vote**
  - What it does: adds a weight scoring column of 1/quadrats-per-plot (0.2 NT, 0.5 SK) as rmse's `weight` input. No
    `sample_weight` is declared, because the weight is a function of `jurisdiction`. The check
    `task_metric_weight_without_sample_weight` is accepted with MET-15's feature-function reason, as for
    liberty_mutual's `var11_weight` and g_research's asset `Weight`.
  - Best evidence: the planner acts on stands (fit_reason). The paper's section is "Modeling site-level mean biomass"
    (title only; not re-read today). Under MET-15's spirit, a map unit counts once. B reproduces the equal-per-plot
    ranking exactly.
  - Cost: one more scoring column for a ranking change of noise size.
- **What would settle it:**
  - Whether the paper weights sites equally in its site-level model (Methods; Wiley refuses automated reads, so a
    human must open it).
  - Whether you want stands to count once across this survey family.
- **Recommendation:** A. **Decision needed:** A or B.

**Agreed facts (measured; my rerun reproduces them)**

- Every input is constant within a plot. Every model's prediction is constant within a plot (spread < 1e-6).
  Per-quadrat RMSE ranks models exactly like the quadrat-weighted stand score: tau 1.000 on 30/30 splits, and 1.000 at
  leaderboard level.
- The plots are 516 in total: 326 NT with 5 quadrats each and 190 SK with 2 each, no exceptions. There are 498
  distinct input vectors.
- 32.5% of the target's variance lies within identical inputs and 28.8% within a plot. The within-plot share is 0.332
  in NT and 0.156 in SK.
- Builder's taus with one weight per input vector (8 models): 0.755 per split (min 0.000) and 0.714 for the
  leaderboard. With true plots: 0.807 (min 0.000) and 0.857. With 10 models: 0.841 (min 0.378) and 0.911. No split is
  negative.
- No input vector spans two burn areas. There is no weight or design column in either raw sheet: `sample_weight` is
  None and there are no scoring columns.
- The quadrat area is fixed by protocol and fully set by `jurisdiction`, which is a feature.

**Disputed points**

Settled by measurement:
- Which unit the 0.76/0.71 refer to: per input vector (above).
- The lowest split: it is 0.0.

The exposure reason is settled by rule text: MET-14 names area swept, so the sentence is reworded and its conclusion
kept.

The one open point is issue 1. It is a weighing of factors, not a rule conflict. It is not an independent Must failure
either: SPLIT-23, MET-14 and MET-15 each hold on their own.

**Consistency with precedent**

- **noaa_afsc_bottom_trawl_survey_cpue:** the area is folded into the target by the source and the score is unweighted
  on the density (MET-14/15). This case is treated the same way, and the reworded exposure bullet should match that
  wording.
- **superconductivity (SPLIT-26) and Lennart, 2026-10-21 ("keep real repeats"):** the source's rows are kept, which
  supports A.
- **liberty_mutual_fire_peril_loss_cost and g_research_crypto_forecasting_1m (MET-15):** both carry a feature-function
  metric weight with no sample weight. B would follow that pattern.
- No precedent decides one-vote-per-group against per-row scoring for replicate rows of unequal count. If you choose B,
  it becomes a new precedent, and the same question then applies to other datasets with unequal replicates per unit.

</details>

<details><summary>Claim audit</summary>

**Claim audit: boreal_postfire_lichen_biomass (claim auditor, focused re-review of 2026-11-06)**

Verdict: ship as is after two wording fixes. Today's change holds in substance. Per-quadrat RMSE equals a
quadrat-weighted stand score exactly. The exposure answer "none" holds. Two numbers are mislabelled: the "equal weights
per plot" taus were measured on input vectors, not plots, and CHANGES.md misstates the lowest split, which is 0.0. The
equal-weight disagreement is no validity issue: it comes from how much NT counts against SK, and at leaderboard level
only noise-level pairs flip. Give the curator one short, optional question on it, not a blocking issue (details under
Q below).

Method: the plot id is rebuilt from the raw sheets and matched row by row with a count that keeps every plot's values
intact. It gives 516 plots, all NT plots with 5 quadrats and all SK plots with 2. The builder's script used input
vectors instead (498 "stands": sibling plots that share every input are merged). The models are the builder's eight
untuned predictors, plus median and zero in a second set. Every RMSE was checked against
`data_foundry.v2.metrics.scorer` (absolute difference below 1e-6).

**Claims**

| # | Claim | Source | Test | Result | Evidence | Rule |
|---|---|---|---|---|---|---|
| C1 | "the per-quadrat MSE splits into a fixed within-plot floor plus the stand score weighted by quadrats" | notes bullet "Every input is constant within a plot" | identity per split, true plot id, 10 predictors, 30 shipped splits, after checking that each prediction is constant within a plot | HOLDS | ptp of prediction within a plot < 1e-6 for every model; tau(quadrat, plot-weighted) = 1.000 on 30/30; builder's identity gap 9.3e-10 | SPLIT-23, EV-1 |
| C2 | "the per-quadrat RMSE ranks models exactly like that stand score (Kendall tau 1 on all 30 shipped splits)" | same bullet | as C1 | HOLDS per split (an algebraic identity once predictions are constant within a plot, which every deterministic model on these features gives). Across splits the leaderboard taus are also 1.000 (mean RMSE) | audit.txt | SPLIT-23 |
| C3 | "Against the stand score with equal weights per plot ... on the shipped burn-area splits it is 0.76 per split on average and 0.71 for the ranking by the mean over the splits (8 untuned predictors)" | same bullet | rerun with the true plot id and the same 8 predictors | REFUTED as labelled (EV-7). 0.755 and 0.714 are equal weights per input vector (498 stands). Per plot (516) the same 8 models give 0.807 per split (min 0.000) and 0.857 for the leaderboard. With median and zero added: 0.841 (min 0.378) and 0.911. Tau depends on which models are in the set, so a level of 0.76 against 0.91 is not a property of the metric | subset.txt, audit.txt | EV-7 |
| C4 | "tau is 0.91 on the former site splits (5 untuned predictors)" | same bullet | not rerun: the former site splits are no longer shipped. The model set and the stand definition also differ, so 0.91 cannot be set against C3 | UNTESTED (not comparable) | - | EV-7 |
| C5 | CHANGES.md: the lowest per-split tau it gives next to "0.76 on average" | the panel's change note (not in the definition) | the builder's own output | REFUTED: the lowest split is 0.000 (repeat 1, fold 2) in the builder's run and in mine; none is negative. Per plot with 10 models the lowest is 0.378 | quadrat_vs_stand.txt, audit.txt | EV-7 |
| C6 | "no weight is needed for a stand score (SPLIT-23)" | same bullet | what the implied weighting does | HOLDS for the quadrat-weighted stand score. It leaves open the claim nobody wrote down: that NT plots should count 2.5 times SK plots. NT is 81% of the test quadrats on average but 63% of the test plots. Repeat 1, fold 2: lightgbm small ranks first on both scores, but the mean predictor ranks 2nd per quadrat and 7th per plot (NT 766 / SK 1288). Lightgbm (full) ranks 7th per quadrat and 2nd per plot (NT 897 / SK 937). The models differ by region, and the weighting decides which region counts. See Q | area.txt, audit.txt | MET-15 (equal-area clause), SPLIT-23 |
| C7 | Exposure: "none ... folded into kg/ha by the source, so the target is a biomass per area, not a count or an amount accrued over an amount at risk, and no rate, weight or offset applies" | notes bullet "Exposure (MET-14, MET-15; 2026-11-06)" | read against MET-14/15; raw columns; quadrats per plot | CONCLUSION HOLDS, REASON PARTLY WRONG. Biomass in a quadrat is an amount over a sampled area, and MET-14 names "area swept" among its denominators, so "not an amount over an amount at risk" is false as worded. MET-14 is met anyway: the source already ships the amount per unit area (kg/ha). The area is set by the protocol (1 m2 NT, 4 m2 SK) and fully determined by `jurisdiction`, a feature, so it is not a realized denominator (LEAK-41 has nothing to remove). The decision is per stand area of a map (MET-15: "per unit of an equal-area map ... scored unweighted"), not per sampled m2, so no row weight follows. No weight or design column exists in either sheet; sample_weight None, no scoring columns | raw columns listed in the run; audit.txt first line | MET-14, MET-15, LEAK-41 |
| C8 | "The number of quadrats per plot (5 in NT, 2 in SK) sets how much a plot weighs in the per-quadrat score; it is no exposure" | same bullet | count per plot | HOLDS: 326 NT plots x 5 and 190 SK plots x 2, no exceptions | audit.txt | EV-7 |
| C9 | "32.5% of the target's variance lies within identical inputs (28.8% within a plot)" | notes and accepted warning | recomputed | HOLDS: 0.3250 and 0.2877. By region, the within-plot share is 0.332 in NT (1 m2 quadrats) and 0.156 in SK (4 m2): larger quadrats average out more of the patchiness, as expected | audit.txt, area.txt | EV-7 |
| C10 | "No feature vector occurs in two groups" | notes, LEAK-18 | input vectors that span more than one burn_area | HOLDS: 0 | audit.txt | LEAK-18 |
| C11 | (MET-16, implied) no survey or design weight is needed | none written | raw sheets; site selection | HOLDS: no weight column. The sampling is stratified by fire-age class (a feature: years_since_fire), not by the outcome, so there is nothing for MET-16 to name | raw columns | MET-16 |
| C12 | (MET-14 "per-quadrat target", implied) the row is a per-quadrat target where the decision is per stand | fit_reason names "rows are quadrats where the planner acts on stands" | covered by C1/C2 and Q | HOLDS with the gap already named. SPLIT-26 keeps the source's rows, and C1 shows that the quadrat score is a stand score with weights 5:2 | - | SPLIT-26, USE-8 |

**Q: is the equal-weight disagreement an issue for the curator?**

Not a validity issue (no Must is broken), but a small policy choice that the notes currently present as settled.
- What the disagreement is: equal weights per plot against weights per quadrat changes only how much NT counts against
  SK (per plot, NT 2.5 to 1). The models' errors differ by region, and every discordance traces to that.
- How big: 8 models, true plots. Per-split tau 0.81. 81 of 840 split x model-pair comparisons (9.6%) change order, and
  40% of those are pairs whose quadrat difference is noise over the 30 splits (|t| < 2). The same model is best on both
  scores in 80% of the splits. At leaderboard level (mean RMSE) the only flips are mean against ridge (quadrat
  difference -16.4, t -0.45) and mean against knn (-17.6, t -1.14). The top pair keeps its order (lightgbm small 1151.6
  against random forest 1155.5, t -0.35, a tie). By mean rank per split (TabArena-style) the tau is 0.81, and the first
  two and the last three places agree.
- Why it bears on the new rules: MET-15 scores "per unit of an equal-area map" unweighted. Here the map unit is the
  stand, so the score that is unweighted per stand is the equal-per-plot one. The per-quadrat score is implicitly
  weighted by the survey protocol. The paper's own section is titled "Modeling site-level mean biomass" (not read today;
  Wiley refuses automated reads), which also points to a site or plot unit.
- Options for the curator:
  - A (mildest): keep the per-quadrat RMSE. Correct the numbers (C3, C5) and state the weighting outright: "an NT plot
    counts 2.5 times an SK plot". Give the true-plot taus (0.81 per split, 0.86 leaderboard, 8 models) and note that
    flips occur only between noise-level pairs.
  - B: equal weight per plot. Use a weight scoring column 1/quadrats-per-plot (0.2 NT, 0.5 SK) as rmse's weight input.
    The weight is a function of `jurisdiction`, so no sample_weight is declared, and the bundle check
    task_metric_weight_without_sample_weight is accepted with that reason (MET-15's feature-function clause). This
    reproduces the equal-weight stand ranking exactly.
  - Recommendation: A. The flips are within noise and B adds a scoring column for a ranking change of that size. Still,
    the curator should see the choice, because MET-15's equal-area clause gives B a principled case.

**Refuted and untested, ranked (validity first, Must first; none is a Must)**

1. C6 / Q (Should, MET-15 equal-area clause; a weighing point): the 5:2 per-plot weighting is implicit. Changes: how
   much SK counts, with a small effect on rankings. Mildest remedy: option A wording; option B if the curator wants
   one stand, one vote.
2. C3 (EV-7): "equal weights per plot" numbers come from input-vector stands. Changes: the stated disagreement is larger
   than it is (0.76 / 0.71 against 0.81 / 0.86 on true plots). Remedy: either relabel them "per input vector (498
   stands)", or replace them with the per-plot values and name the model set.
3. C7 reason (EV-7, MET-14 wording): the exposure sentence denies that the target is an amount over an area. Changes:
   nothing shipped. Remedy: "the target is already the amount per unit area that MET-14 asks for; the quadrat area is a
   protocol constant identified by `jurisdiction`; the planner's decision is per stand area, not per sampled area, so no
   weight (MET-15)".
4. C5 (EV-7, change note only): the change note's lowest split is wrong (the lowest is 0.0). Remedy: fix it in the
   panel record or any REVIEW.md text that copies it.
5. C4 untested: the 0.91 on the former site splits cannot be rebuilt from shipped splits and used a different model set.
   Remedy: either drop the comparison, or say it is not like for like.

</details>

## Reference

Greuel R.J., Degre-Timmons G.E., Baltzer J.L., Johnstone J.F., et al. (2021). Predicting patterns of terrestrial
lichen biomass recovery following boreal wildfires. Ecosphere 12:e03481. doi:10.1002/ecs2.3481. Data:
doi:10.5061/dryad.t1g1jwt15 (Northwest Territories), doi:10.5061/dryad.tb2rbnzzj (Saskatchewan).

Lead: the two-regime-zero workbook (v4, 2026-10-19), Master rows 37 (Terrestrial lichen - Northwest
Territories) and 38 (Terrestrial lichen - Saskatchewan).
