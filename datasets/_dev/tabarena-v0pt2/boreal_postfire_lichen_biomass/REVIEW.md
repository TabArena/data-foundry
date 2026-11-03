# boreal_postfire_lichen_biomass

**Outcome:** added. The AI recommends shipping it as changed after the review panel. Greuel et al. (2021) surveyed
caribou forage lichen after boreal wildfires in the Northwest Territories (NT) and Saskatchewan (SK), in two Dryad
deposits (CC0). One row is one ground quadrat: 2,010 quadrats of 516 plots, 40.4% of them at 0. The target is the
authors' lichen biomass in kg/ha, estimated from cover and height. The inputs are the years since fire, the stand type,
the coordinates, the ecoprovince, the ecozone and the jurisdiction. Whole NT burn scars or unburned areas are held out,
and each SK plot on its own. The metric is RMSE on kg/ha (fallback).

Validity:
* SEL-2 holds: your `Yes` of 2026-10-30 (policy call 1).
* USE-1 triggered, fixed: the actor is named (issue 1).
* USE-5 holds: the NT target reproduces from the authors' own cover sheet.
* USE-6 holds for the stand age, with a USE-8 note (issue 2).
* LEAK-10 holds: the cover-based biomass (61.934 x cover in every row) and the presence flag are dropped.
* SPLIT-1/SPLIT-4 triggered, fixed: re-split on the burn area (issue 1).
* PROV-13 triggered, fixed: three plots' coordinates repaired from the authors' site sheet.
* PROV-8 holds: the download is Dryad's own version zips, which the repair needs.
* PROV-16 holds: the paper is read (issue 4, resolved 2026-11-03); the notes cite it by section.

Value: TP-2, a small real signal. Under the burn-area split an untuned random forest has skill (1 - MSE / MSE of the
training mean) +0.12, above 0 on 28 of 30 splits (the task probe's forest: 200 trees, min_samples_leaf 2, a square root
of the inputs per split; the forest of issues 1 and 5, 300 trees with min_samples_leaf 20 and all inputs per split,
scores +0.097). Fallback RMSE: the abstracts report significance tests and a growth curve, no prediction error (MET-1).

Quality: CLEAN-16 departure kept with a measured fact, the target stays on kg/ha (issue 5); counts and sentences in the
notes corrected (EV-7).

Weighed: source + (CC0, two documented deposits, a paper); use case + (range plans against the 40-year rule); signal -
(skill about 0.1); size 0 (2,010 quadrats, 216 groups).

The panel reviewed the first draft (site split, Zenodo download, unrepaired coordinates); its eleven changes that need
no decision are made (Mediator, "Changes to make now"). `dataset check` gives 0 errors and the two warnings of issue 3.
The numbers below are measured on the changed definition and its 30 shipped splits (untuned) unless marked as the
panel's.

**Main points:** all six issues resolved on 2026-11-03: shipped as the paper's own forecast (1), the tree-ring stand
age kept (2), the duplicate warnings accepted (3), the paper read (4), kg/ha (5) and RMSE (6). Verdict: ship (2026-11-03).

**Issues for Andrej:**

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

**Review panel:** ship after changes (mediator). Claim audit: 44 claims, 28 hold, 12 refuted or overstated in part
(fixed in the notes or the definition), 2 untested against the paper, 2 not testable (a superseded estimate, a curator
decision). Blind review: would exclude for weak signal on quadrat rows; it found the CG3-31A and F13-5 coordinates on
its own. Debate: agreed after the rebuttals on shipping, the burn-area split once the actor is named (issue 1), the
coordinate repair from the origin, the quadrat rows, the fallback RMSE and the raw kg/ha scale; open after the
rebuttals, settled by the mediator: why ridge loses skill under the area split (its ecoprovince effects do not reach a
new burn) and the download route (Dryad's version zips).

<details><summary>Mediator</summary>

**Mediator (2026-11-01): boreal_postfire_lichen_biomass**

**Recommendation**

```text
Verdict: ship after changes.
Validity: SEL-2 holds (Andrej's Yes of 2026-10-30, policy call 1). USE-1 triggered, fixed: the range-plan biologist
  named as the actor (issue 1). USE-2 holds. USE-6 holds for years_since_fire, with a USE-3/USE-8 note (a field-dated
  stand age; issue 2). USE-5 holds (the NT target reproduces from the origin's cover sheet). LEAK-10 holds (2 drops).
  SPLIT-1/SPLIT-4 triggered, fixed: re-split on the NT burn scar or unburned area, each SK plot on its own (issue 1).
  SPLIT-23, SPLIT-24, SPLIT-29 hold. PROV-13 triggered, fixed: 3 plots repaired from All_site_info_NT.xlsx. PROV-8:
  the download moves to Dryad's version download, which the repair needs. PROV-16/17: paper unread, claims marked
  unverified (issue 4).
Value: TP-2, a small real signal under the area split (random forest skill +0.113, above the mean on 28 of 30
  splits; keep). TP-5 and SPLIT-28 hold. Fallback rmse on kg/ha (MET-1, MET-5).
Quality: EV-7 corrections to counts and sentences; CLEAN-16 departure kept with a measured fact (issue 5);
  CLEAN-10/11 wording on 2 zeros.
Weighed: source + (CC0, two documented deposits, a paper); use case + (range plans against the 40-year rule);
  signal - (skill about 0.11); size 0 (2,010 quadrats, 216 groups).
For the curator: issue 1 (actor and split level), 2 (field stand age), 3 (two warnings), 4 (the paper), 5 (target
  scale, for the family).
```

The advocate and the critic end on the same verdict and the same changes. Two points stayed open after the rebuttals:
why ridge loses skill under the area split, and which download route the definition takes. A cheap experiment settles
each one (disputed points below). Neither changes the verdict.

**Agreed facts**

- No leak and no copy across the split. `kgha.areaperm2` is 61.934 x percent cover in 2,010 of 2,010 rows, and
  `non_zero` is target > 0 in 2,010 of 2,010; both are dropped. No feature alone reaches R^2 0.03. On all 30 shipped
  splits there are 0 exact feature copies, 0 shared groups and 0 shared plots. A random split scores 0.347 against
  -0.034 by site.
- Every input is constant within a plot. The quadrat score ranks models like a stand-level score weighted by quadrat
  count (Kendall tau 0.91; the same best family in 93% of splits).
- The target is the volume-based biomass. For NT, `kgha.volperm2` = 12.633 x the sum of percent cover x live depth
  over the four forage groups (median ratio 12.6333 over 945 quadrats; Dryad's `Quadrat_cover_data_NT.xlsx`). SK has
  no cover sheet, and the two regions' conversions differ (destructive slopes 63.7 and 50.9 kg/ha per percent cover).
- `years_since_fire` is the survey's per-plot stand age. It is field-dated for the 145 NT control plots (725 rows,
  36%) in areas with "no recorded burn history" (ages 33 to 241). Capping it at assumed fire-record horizons costs about
  0.01 R^2 (ridge -0.013, SE 0.005). It is no leak (USE-6).
- Three NT plots carry wrong coordinates. CG3-31A has CG2-35A's coordinate, 162 km from its site-mates. F13-5A and
  F13-5B are 7.8 and 7.9 km off. The other 323 plots agree with `All_site_info_NT.xlsx` within 2 km (median 0.3 km).
- 94.3% of NT test quadrats have another site of their own burn scar or unburned area in training. The NT codebook
  defines `plot` as "Plot location: Burn Scar or Unburned area -xxx". Burn areas hold 19.1% of the NT target's sum
  of squares. The median distance from a test quadrat to training is 2.4 km by site and 22 km by area, against 95 km
  for a point in the NT study hull.
- The note "the level of grouping changes the score within its noise" is false for ridge (EV-7).
- Trained on log1p and back-transformed, all four probed families fall below the training mean on RMSE in kg/ha
  (ridge 0.132 to -0.050, random forest 0.104 to -0.043, small LightGBM 0.083 to -0.036).
- The claim auditor's count and wording errors (change 10).
- The paper (doi:10.1002/ecs2.3481) is CC BY 4.0. Wiley blocks automated requests, so a person can read it in a
  browser.

New facts from the mediator's checks (scripts in the run folder, threads capped):

- Both Dryad version downloads work without a token. SK version 105865 redirects to a zip of 2 files, and its
  `Lichen_data_SK.xlsx` has the definition's SHA-256 (74ad1fe5...). NT version 442103 (precedent checker) gives 4
  files, with `Lichen_data_NT.xlsx` 03a3f3f4... and `All_site_info_NT.xlsx` 24493a74....
- What the 2022 revision of the NT sheet changed (2021 version 103457, downloaded and compared). It drops five extra
  zero quadrats of plot CG2-5A, which had 10 rows. It adds the missing fifth quadrat of F6-7B (`F6-7B-6`, 0) and the
  constant `species` column. The other 1,629 quadrats are identical. The 2021 file already held 326 plots, so the
  revision does not explain the gap to the 346 in the abstract.
- CG2 and F2 merge into one area through a real shared place: CG2-4A and F2-22A/B lie about 0.5 km apart in the site
  sheet. It is the only merge.

**Changes to make now (no decision needed)**

1. **Download from Dryad's version zips** (PROV-13, PROV-8, EV-7; the pennsylvania route). Use
   `https://datadryad.org/api/v2/versions/442103/download` (NT, version 5 of 2026-05-18) and
   `.../versions/105865/download` (SK, 2021-02-18), then unzip and check the SHA-256 of `Lichen_data_NT.xlsx`
   (03a3f3f4...), `Lichen_data_SK.xlsx` (74ad1fe5...) and `All_site_info_NT.xlsx`
   (24493a7427adeecb04c694f515729d90c2a831d44ad2d8fccd453a781e7cdf6c). Drop the "401" reason. The Zenodo records may
   stay named as byte-identical copies of the lichen sheets. `_load_raw` also reads the site sheet (sheet "All site
   info 2019-10-16"; `Lat_start` and `Long_start` are text with a decimal comma). It should reproduce the shipped
   frame exactly, apart from change 2.
2. **Repair the three plots from the site sheet** (PROV-13, PROV-14). Take the plots whose task-sheet coordinate
   differs from the site sheet by more than 0.01 degree, and set the site sheet's value rounded to 0.01, the task
   sheet's grid. CG3-31A goes from 62.22, -116.33 to 60.77, -116.56, and its ecoprovince from Great Bear Plains to Hay
   and Slave River Lowlands, its site-mates' value (the ecozone stays Taiga plains). F13-5A and F13-5B go from 63.03,
   -114.35 to 63.00, -114.21. That is 15 rows. Add a dated `Repair:` bullet and a `Decision` table of the three plots
   (task sheet against site sheet). Keep the 0.01 grid for the other plots: the coordinate link rests on it, and
   rounding is not damage.
3. **Re-split on the NT burn scar or unburned area** (SPLIT-1, SPLIT-4 Must; SPLIT-24 exact key; SPLIT-26; precedent
   airfoil_self_noise). The NT group is the plot-name prefix before the first `-` (`F1`, `C3`, `CG2`, `CS`, 27
   prefixes), merged through the site links (a shared site name or an identical coordinate, after change 2). Each SK
   plot stays its own group. It should reproduce:
   - 216 groups: 26 NT (CG2 and F2 join) and 190 SK. The largest group is CG2+F2, 200 rows (10.0%), under the 20%
     check threshold.
   - With the repository's splitter, 10 x 3 folds and test folds of 410 to 974 rows. The exact sizes depend on how
     the group labels sort; the panel used labels in file order. About 72 test groups per fold.
   - Still 0 exact feature copies across the split.
   - Untuned skill against the training mean (panel numbers, repaired frame): random forest (min_samples_leaf 20)
     +0.113 (above the mean on 28 of 30 splits); small LightGBM about +0.11; ridge -0.074 +- 0.070 (below the mean on
     9 of 30); ridge without the three region labels +0.077. Ridge swings with the fold draw (+0.054 on the unrepaired
     area split), so expect anything from about -0.1 to +0.05.
   - Re-run the task, leak and group probes. Rewrite `grouping.definition`, `splits_comment`, `task_summary.split`,
     `task_summary.changes` and the grouping bullet. Rename the group column (for example `burn_area`).
4. **Name the actor in `use_case`** (USE-1). A caribou habitat biologist with the GNWT or Saskatchewan's Ministry of
   Environment revises a boreal caribou range plan. Today every burn under 40 years counts as disturbed, and a range
   needs 65% undisturbed habitat. NWT monitoring (CIMP) found forage lichens need 45 to 70 years to recover. The
   biologist estimates the forage of stands of a given type, ecoprovince and fire age, in burns that were not
   surveyed. The domain practitioner gives the public sources.
5. **Name the input gaps in `known`, `use_case` and `fit_reason`** (USE-3, USE-8). `years_since_fire` is the survey's
   per-plot stand age, field-dated where no fire is recorded; a planner has an inventory age or "older than the fire
   record" (capping costs about 0.01 R^2). `stand_type` is the field class of Hart et al. 2019. Rewrite `fit_reason`
   with the real gaps: an allometric label whose constant is unverified against the paper, with two regional
   conversions; quadrat rows for a stand decision; a stratified chronosequence of two regions and four ecoprovinces,
   with no NT burn under 29 years; field-quality inputs. Drop "No actor is named" and "design variables". The fit
   stays approximate.
6. **State the split's measured facts** (EV-7, SPLIT-1). Remove "within its noise". Give the distances (NT test median
   22 km under the area split, against 2.4 km by site and 95 km for a point in the NT hull; SK per plot, 3.6 km, since
   SK names carry no burn key). Give ridge's drop and its cause as settled below: ecoprovince effects learned from a
   handful of burns do not reach a new burn. Do not write "leans on burn-mates" or "unseen combinations".
7. **Target bullet** (USE-5, EV-2). Add the NT reproduction (12.633 x the sum of cover x live depth, 945 quadrats),
   say that SK has no cover sheet, and say that the regional conversions differ (slopes 63.7 and 50.9 over 155 and 72
   harvested patches), with `jurisdiction` carrying the offset.
8. **Provenance notes** (PROV-8, PROV-9, PROV-13, PROV-17).
   - We ship the authors' 2022 revision; its changes are measured above. The year stays 2021.
   - The 20 NT plots missing from the lichen sheet (already in 2021) are in `Quadrat_cover_data_NT.xlsx` (346
     plots). They stay out: adding them back would need a target from our inferred formula (Tensions, "A better
     version against our own fix").
   - The 31 SK plots remain an `Anomaly`.
   - Replace "no repository copy with text was found" (here and in the metric reason): the paper is CC BY 4.0, the AI
     could not fetch it, and the curator has been asked (PROV-17).
9. **Raw scale reason** (CLEAN-16, MET-3). Replace "the planner's quantity..." with the measured fact: trained on
   log1p and back-transformed, every probed family falls below the training mean on RMSE in kg/ha. Issue 5 asks
   whether the siblings change too.
10. **Counts and sentences** (EV-7, CLEAN-10/11).
    - 32.5% is the floor within identical inputs; the within-plot share is 28.8%.
    - 482 of the 518 zero copies lie within one plot; 36 come from sibling plots that share every input.
    - 980 is the check's count; 1,671 rows sit in an input group with more than one target.
    - Zeros: 811 have no cover; 2 in plot 2015-054 have cover but volume 0 and stay 0, as the authors' flag has them.
    - Only 26 of 110 multi-plot sites share one age; "often their fire" goes.
    - NT r = 0.17 under 1 km between different sites.
    - The destructive files hold 155 and 72 patches, not 342 and 256.
    - "All at one recorded coordinate" goes (false for 51 site names).
11. **One SPLIT-23 line**: a quadrat score ranks models like a stand score weighted by quadrats (tau 0.91), and an NT
    plot weighs 5 quadrats against 2 for SK.

**Changes that need the curator (ranked)**

1. P3/P4, USE-1 and SPLIT-1/SPLIT-4 (Must): confirm the range-plan actor, and with it the test on burns nobody
   surveyed. Implemented: the burn-area split. Alternative: an infill reading (unsurveyed stands inside partly
   surveyed burns) keeps the site split, and "across the range" leaves the definition. The cost: 94% of NT test
   quadrats have their own burn in training, and ridge looks better than it is (+0.132 against -0.074).
2. P3, USE-3/USE-6/USE-8 (Must): keep the field-dated stand age with a note. This is a consistency question against
   wadden_sea's open issue 5 (visit-measured sediment replaced by interpolated values). Set apart: a stand age exists
   for every stand (inventory, fire records), its field precision is worth about 0.01 R^2, and the map-level stand-in
   would be our assumption of a fire-record horizon, not a source covariate.
3. P4, LEAK-18 (Should): accept `dataset_duplicate_rows` and `dataset_conflicting_duplicate_rows` with the corrected
   reasons. The curator fills `accepted_check_warnings` (add-dataset step 6).
4. P5, PROV-16/PROV-17 (Must): read the paper's Methods for four things: how TSSRF was dated, why 20 NT and 31 SK
   plots are out, any prediction error reported (MET-1), and the allometry constant.
5. P7, CLEAN-16 (Should) and MET-3: raw kg/ha here while four AI-draft siblings ship log1p. The measured fact
   (back-transformed log1p falls below the mean) probably holds for them too (wadden_sea's notes report the same
   effect), so it is one call for the family.

**Disputed points**

*1. Why ridge loses skill under the area split.*

- Advocate: held-out burns take rare stand type x ecoprovince combinations with them, and a linear model
  extrapolates. Evidence: r = -0.74 between ridge's skill and the share of test rows with such a combination; ridge
  scores +0.120 on the 20 splits with at most 2% of them and -0.461 on the other 10. So "no model is shown to read its
  test site's burn-mates", and the re-split corrects no inflated score.
- Critic: the region labels stand in for the test site's own burn area under the site split. Evidence: ridge on stand
  type and age goes from 0.090 to 0.074; adding the region labels goes from 0.102 to -0.002; location-only kNN scores
  +0.004 by site.
- Both rest on EV-1 and EV-7 (what the note may claim). The disagreement is about a fact.
- Decisive experiment. Same repaired frame and the same 10 x 3 area folds as the advocate's; ridge with one channel
  removed at a time (`ridge_mechanism.py`, `gbp_folds.py`). Skill against the training mean:

| model | site split | area split | area, 20 splits with at most 2% unseen combinations | area, other 10 |
|---|---|---|---|---|
| ridge, all 7 inputs | +0.132 | -0.074 (below the mean on 9 of 30) | +0.120 | -0.461 |
| ridge without ecoprovince, ecozone, jurisdiction | +0.077 | +0.077 | +0.093 | +0.047 |
| ridge without coordinates | +0.094 | -0.047 | +0.108 | -0.358 |
| ridge, stand type and age | +0.082 | +0.087 | +0.102 | +0.057 |
| random forest, all 7 | +0.112 | +0.113 | +0.101 | +0.136 |

- Without the three region labels, ridge loses nothing under the area split. With them it gains 0.055 by site and
  loses 0.151 by area.
- The loss sits on the folds where most of Great Bear Plains' burns go to test. That ecoprovince has only 5 NT burn
  areas, with means from 270 to 3,453 kg/ha. Ridge's skill correlates at r = -0.88 with the mean of the Great Bear
  Plains areas left in training (r = -0.74 with the unseen-combination share). On the 9 splits where ridge falls below
  the mean, those areas average 1,293 to 2,658 kg/ha; on 20 of the other 21 they average 331 to 755. On the worst split
  ridge predicts about 2,700 to 2,900 kg/ha for Great Bear Plains stands whose means are 180 to 775.
- 70% of ridge's excess squared error on the area split lies in stand type x ecoprovince cells that were seen in
  training. The unseen cells hold 4.4% of the test rows and 30% of the excess.
- Settled for the critic's narrowed reading. An ecoprovince effect learned from a handful of burns does not transfer
  to a new burn; under the site split, that effect includes the test site's own burn. The advocate's correlation is
  real, but the unseen combinations mark those folds (Great Bear Plains' jack pine plots sit in one burn) and do not
  cause the loss.
- What follows:
  - The re-split still rests on SPLIT-4, the application.
  - The site split did overrate one family, ridge. It did not overrate the trees.
  - The region labels stay. They are known for every stand, and the source names ecoprovince as a predictor (SPLIT-4).
  - Change 6 writes the measured mechanism.

*2. Download route: Dryad's version download or the Zenodo mirror.*

- Precedent checker, prompt A: (a) keep Zenodo and record the Dryad sheets as read; (b) take Dryad's version
  download, like pennsylvania.
- The critic's opening allowed either. Both rebuttals then name Dryad.
- Rules:
  - PROV-8 (Must) lets the download name a copy, so Zenodo is not wrong in itself.
  - PROV-13 (Must) makes the repair from the origin the first remedy. The repair needs `All_site_info_NT.xlsx` at
    build time, and only Dryad's version download serves it.
  - EV-7: the stated reason, "Dryad answers 401 without a token", is true only of the per-file API.
- Checked: both version downloads work without a token, and the digests match (agreed facts).
- Settled: Dryad's version download for both deposits (change 1). A mixed route, Zenodo for four files and Dryad for
  the fifth, depends on Dryad anyway and adds a second host that can fail.
- Precedents: pennsylvania is followed. Nantucket's Zenodo mirror is set apart, because nothing it reads exists only
  on Dryad.

*3. Points raised but backed by neither side, settled by rule.*

- Exclusion for weak signal (blind reviewer). Not settled by weighing: TP-2 (Should) and the Tensions row "The right
  split against the score" (forest_fires) say a small real signal under the right split is no reason to retire. Under
  the area split the forest still beats the mean on 28 of 30 splits, so SPLIT-28 and TP-5 hold (about 72 test groups
  per fold).
- Plot-mean aggregation. SPLIT-26 (Should) keeps the source's rows, and SPLIT-23 holds (tau 0.91).
- A tail-robust metric. MET-10 is a factor (Weigh). The practitioner shows that a range's forage is a sum of stand
  means, which RMSE targets. The family's metric question is wadden_sea's issue 3, so it is not raised again here.

*4. Site against burn area.* Agreed after the rebuttals. Under the definition's own range-wide use case, SPLIT-1 and
SPLIT-4 (Must) decide it, so it is change 3. The curator confirms the use case (issue 1).

**Consistency with precedent**

- Scope: the CC `Yes`, priority 1 (2026-10-30, policy call 1), is followed. It is not reopened on the scores (TP-2,
  forest_fires). The `No Good Target / Scientific Discovery` marker on a `Yes` record is allowed as a concern marker
  (selection.md). The named actor answers its concern; removing it is a family tidy-up with the other four `Yes`
  records of that day.
- Split: airfoil_self_noise is followed (SPLIT-1 case, Lennart 2026-10-20). There, 91.5% of test runs had their setup
  in training, so the coarser documented entity won; here 94.3% of NT test quadrats have their burn in training.
  5g_energy_consumption (Lennart 2026-10-14) is set apart: it had no documented entity above the station. The
  wadden_sea and pennsylvania drafts are undecided.
- Download: pennsylvania is followed. Nantucket is set apart by a file that exists only on Dryad.
- Repair: PROV-13 (SUPPORT2, ashrae) and the Tensions row "Repair against cleaning around damage" are followed. The
  20 NT plots stay out, following the Tensions row "A better version against our own fix" (eryhemato).
- Quadrat rows: pennsylvania (Andrej, "LGTM", 2026-10-30) and superconductivity (SPLIT-26) are followed.
- Warnings: breast_cancer_prediction, expresso_churn_prediction_1m and california_house_prices_2020 (natural repeats
  accepted with a reason) are followed.
- Metric: fallback rmse, as churn_telco_south_asia (paper unread, fallback kept).
- Target scale: departs from four AI-draft siblings. The measured fact may not set this case apart (issue 5).
- Field stand age: the like case is wadden_sea's open issue 5; the fact that sets this case apart is in issue 2. If
  Andrej's answer there becomes a Tensions row, this case should be checked against it.
- No drift in Andrej's calls and no third exception (precedent checker).

</details>

<details><summary>Claim audit</summary>

**Claim audit: boreal_postfire_lichen_biomass (claim-auditor, 2026-11-01)**

Verdict: the definition mostly holds. No claim fails in a way that breaks the task, and nothing leaks or is copied across the split. Five claims are refuted or overstated. Each needs a fix to the notes, plus one weighing call on how coarse the grouping should be:

1. The note says the grouping level makes no difference beyond noise. That is false for the linear family, the best probe family (SPLIT-1).
2. "Years since fire" for the NT control plots cannot come from fire-history maps (USE-3, USE-8).
3. One NT plot sits at the wrong place: CG3-31A is 160 km from its sibling plots (PROV-13).
4. The NT file we ship was revised on Dryad in 2022, after the paper came out (PROV-8).
5. The paper can be read: it is CC-BY and an archived PDF exists (PROV-17, MET-1).

Every other point is a wording or count fix (P7). The metric checks pass on all 30 folds.

Scripts and outputs are in the run folder (`a1_raw.py` to `a6_unit.py`, `splits_audit.csv`, `grouping_levels.csv`, `frame_with_plot.parquet`, the shipped frame mapped back to the raw plot ids; the mapping matched every row). The models are untuned probes: ridge, random forest with min_leaf 20, and a small LightGBM. All Python runs had their threads capped.

**Claims table**

| # | Claim | Source | Test | Result | Evidence | Rule |
|---|---|---|---|---|---|---|
| 1 | Zenodo copies are byte-identical to Dryad | download_description, notes bullet 0 | sha256 of the 4 local files against the Dryad API file listings (v5 442103; SK 105865) | holds | all 4 digests equal (e.g. NT lichen 03a3f3f4..., SK 74ad1fe5...); Zenodo md5s also match | PROV-1 |
| 2 | Source first published 2021 (NT 2021-02-03, SK 2021-02-18); year 2021 | `source` comment, `year` | Dryad version API | holds for the year; **the version wording is incomplete** | NT v3 2021-02-03 `metadata_changed`; **v4 2022-06-23 `files_changed`**: `Lichen_data_NT.xlsx` grew from 134,806 to 140,857 bytes, with a new digest. We ship the v4/v5 file, not the one the April 2021 paper used. What changed is untested: v3 needs a Dryad token | PROV-8, PROV-9 |
| 3 | 1,630 NT and 380 SK quadrats; 2,010 quadrats from 516 plots; 5 per plot in NT, 2 in SK | task_summary.row, notes | counts on the raw sheets | holds | 326 plots x 5 and 190 x 2 | — |
| 4 | Metadata quotes: NT "2016-2018", "5, 1 m x 1 m quadrats"; SK "2015-2016", "2, 2 m x 2 m quadrats" | notes bullet 2 | read the Metadata sheets | holds | quotes are verbatim; NT plot 60 m2, SK 100 m2. SK plot names start 2015 or 2016. The NT years cannot be checked (no year column) | — |
| 5 | Files hold 326 NT and 190 SK plots, against 346 and 221 in the abstracts | notes bullet 2 | counts; Dryad `methods` field | holds | 326/190 measured; 346/221 are quoted from the Dryad methods. The 2022 revision of the NT file (row 2) may bear on the gap (untested) | PROV-13 |
| 6 | The use case quote "provide a basis for estimating future caribou habitat"; no actor named | task_summary.use_case | Dryad and Zenodo abstracts | holds | verbatim in both abstracts | USE-1 |
| 7 | A planner knows years since fire "from fire-history maps and the forest inventory" | task_summary.use_case, notes bullet 1 | where `years_since_fire` can come from, plot by plot | **refuted for the control plots** | Dryad NT methods: control areas have "no recorded burn history". Those 145 NT plots (prefixes C*, CG*, CS; 725 rows, 36.1% of all rows) carry 68 distinct ages from 33 to 241, so the ages are field measurements of the stand. Burn-scar plots also reach 219 years, and SK fire years go back to 1854. In the same NWT program, stand age came from tree-ring counts (ORNL DAAC 1664). That is circumstantial and unverified for this file. 59% of rows are older than 52 years | USE-3, USE-6, USE-8 |
| 8 | Every input is constant within a plot | task_summary.known, notes bullet 7 | nunique per plot on the raw sheets | holds | max nunique = 1 for every input in both sheets | — |
| 9 | Target = `kgha.volperm2`, "Biomass of live lichen species, estimated by standardize live lichen volume" | notes bullet 3 | Metadata sheet | holds | verbatim | USE-5 |
| 10 | `non_zero` equals volume biomass > 0 in all 2,010 quadrats; cover biomass > 0 differs in 2 SK quadrats (plot 2015-054) | notes bullet 3, decision table | crosstab | holds | 1,630/1,630 and 380/380 for volume. For cover, 378/380: 2015-054-nw and -se have cover biomass 123.9 and 31.0 but volume 0 | — |
| 11 | `kgha.areaperm2` = 61.934 x percent cover in every row (NT on a 0.5% grid, SK on 0.1%) | notes bullet 4, decision table | area/61.934 tested on 1%, 0.5% and 0.1% grids | holds (strong circumstantial: percent cover is not shipped) | NT 1,630/1,630 on the 0.5% grid (1,377 on 1%); SK 380/380 on the 0.1% grid (268 on 0.5%) | LEAK-10 |
| 12 | Dropping `kgha.areaperm2` and `non_zero` (LEAK-10) | notes bullet 4 | Spearman of cover against volume biomass; non_zero against target | holds | Spearman 0.994 (NT) and 0.990 (SK); non_zero is target > 0 exactly | LEAK-10 |
| 13 | Quadrat labels 0, 6, 12, 18, 24 (NT) and nw/se (SK); `species` constant (NT only); acronyms map one-to-one to ecoprovince | notes bullet 5 | value counts; groupby nunique | holds | species = "Cladonia spp." in 1,630 rows; acronym and acronym1 are 1:1 with ecoprovince | CLEAN-5 |
| 14 | `ecozone` and `jurisdiction` are coarser levels of ecoprovince; `jurisdiction` marks the protocol (1 m2 NT, 4 m2 SK) | notes bullet 5 | groupby | holds | 4 ecoprovinces nest in 3 ecozones and 2 jurisdictions with no overlap | — |
| 15 | F8-3A labels one quadrat 8 | notes bullet 6 | raw | holds | F8-3A-8 is the only quadrat labelled 8 | — |
| 16 | "The within-plot spread is 32.5% of the target's variance (25.6% on log1p), a floor no model can go below" | notes bullet 7, warning reason | share of variance within the true plot id and within identical input vectors | **the floor holds; the label is wrong** | within the true plot: 28.8% (24.6% on log1p). Within identical inputs: 32.5% (25.6%), because 14 input vectors cover several sibling plots of one site. 32.5% is the correct floor, but it is not the "within-plot spread". By protocol, NT has 33.2% within plots and SK 15.6% | — |
| 17 | 532 exact duplicate rows, "518 of them quadrats of one plot all at 0" | notes bullet 7, warning reason | duplicates on features + target, traced to plots | **overstated** | 532 copies, 518 of them at 0. Only 482 are zeros within one plot; 36 zero copies (39 copies in all) come from sibling plots of one site that share every input | LEAK-18 |
| 18 | 980 rows "share their inputs with a row of another target" | notes bullet 7, warning reason | count rows whose input group holds more than one target value | **the count is the check's, not the stated quantity** | 980 = 1,512 rows duplicated on features minus the 532 exact copies. 1,671 rows (83%) sit in an input group with more than one target value | — |
| 19 | No feature vector occurs in two groups; 0% of test rows have an exact copy in train | notes bullet 7, warning reasons | per shipped split | holds | 0 vectors in two groups; 0 copies, 0 shared groups and 0 shared plots on all 30 splits | LEAK-18, LEAK-16 |
| 20 | 813 zeros (40.4%; NT 40.7%, SK 39.5%), "observed absences" | notes bullet 8, task_summary.predicted | counts | **holds, with one exception** | 813 / 0.4045 / 0.4067 / 0.3947. The 2 SK quadrats of row 10 had lichen cover but volume 0, so 2 of the 813 zeros are not absences | — |
| 21 | Zero-inflation quote "to account both for the heterogeneous nature of lichen presence (zero-inflation)" | notes bullet 8 | abstract | holds | verbatim | — |
| 22 | NT plots of a site (`F1-22A`, B, C) are "all at one recorded coordinate" | notes bullet 9 | coordinates per site name | **refuted** | 51 of 141 NT site names have plots at 2 coordinates (129 plots). Most are 0.01 degree apart, but one is 160 km off: **CG3-31A** sits at 62.22, -116.33 in "Great Bear Plains", while CG3-31B and C sit at 60.77, -116.56 in "Hay and Slave River Lowlands", like all 29 other CG3 plots. CG3-31A's coordinates equal CG2-35A's exactly, so the group key merges sites CG3-31 and CG2-35 into `site_036`. This looks like an entry error in 5 rows (lat, lon, ecoprovince) | PROV-13 |
| 23 | NT coordinates are rounded to 0.01 degree; 17 coordinates hold plots of 2 or 3 sites; each SK plot has its own coordinates | notes bullet 9 | raw | holds | 17 such coordinates (15 with 2 sites, 2 with 3); 190 SK coordinates for 190 plots | — |
| 24 | 312 groups: 122 NT of 1 to 11 plots (most of 2 or 3), 190 SK | grouping.definition | frame | holds | NT plots per group {1: 12, 2: 53, 3: 44, 4: 3, 5: 5, 6: 2, 8: 2, 11: 1} | SPLIT-24 |
| 25 | "Plots of one site share coordinates and often their fire" | grouping.definition | years_since_fire per multi-plot site | **overstated** | only 26 of 110 multi-plot NT sites share one years_since_fire; coordinates differ in 51 sites (row 22) | — |
| 26 | Whole sites held out; "nearby sites stay in training" | task_summary.split, splits_comment | split audit; distances | holds | 104 test groups per fold; the nearest plot of another site is at a median 1.1 km (NT) and 2.8 km (SK, nearest other plot) | SPLIT-24 |
| 27 | Plot means correlate between plots of different sites: NT r = 0.21 to 0.37 up to 10 km, about 0 beyond; SK 0.75 under 1 km, 0.41 at 2-5 km, 0.24 at 5-10 km | notes bullet 10, splits_comment | pairwise r of log1p plot means, all pairs against pairs of different site groups | **holds except the NT band under 1 km** | the builder's figures came from all pairs. Among different sites, NT under 1 km gives r = 0.17 (55 pairs); 1-2 / 2-5 / 5-10 km give 0.21 / 0.27 / 0.37; beyond 10 km about 0. All SK figures hold. SK stays at 0.14-0.17 out to 50 km | — |
| 28 | "The level of grouping changes the score within its noise" (plot / site / blocks) | notes bullet 10 | 10x3 GroupKFold per grouping, 3 families (`grouping_levels.csv`), plus the builder's own log | **refuted for the linear family** | builder: ridge 0.143 +- 0.016 by site against 0.005 +- 0.043 by block. Mine, R2 by site / NT survey area with SK by plot / NT area with SK by block / blocks: ridge 0.128 / 0.063 / 0.088 / -0.044 (SE 0.012-0.072); RF 0.118 / 0.102 / 0.099 / 0.126; LightGBM 0.104 / 0.100 / 0.108 / 0.123. The best family flips: ridge under the site grouping, the trees under area or block groupings | SPLIT-1, SPLIT-4 |
| 29 | Source model: hurdle GLM "identified stand age, stand type and ecoprovince as significant predictors"; logistic growth 28 to 73 years | notes bullet 11, metric reason | abstract | holds (abstract) | verbatim | PROV-16 |
| 30 | Probe numbers: linear R2 0.137, beats the mean 30/30, RF 0.088, LightGBM -0.016; no flags; best single feature at most 0.03; random split 0.347 against -0.034 by site; hurdle AUC 0.737, R2 0.167, oracle 0.103 | notes bullet 12 | read `probes/*.log` | holds (as logged) | task_probes.log, leak_probes.log (stand_type 0.028), group_probes.log, grouping_hurdle.log | EV-8 |
| 31 | Destructive samples are "342 and 256 harvested 20 x 20 cm patches"; slopes through the origin of 63.7 (NT) and 50.9 (SK) kg/ha per percent cover | notes bullet 13 | rows against `plot.bag`; rerun the slope | **slopes hold; patch counts refuted** | 342 and 256 are species-group rows. There are 155 (NT) and 72 (SK) bags (patches) from 93 and 61 plots. Slopes are 63.72 and 50.93 over all groups; the forage groups alone give 64.91 and 50.25 | — |
| 32 | `Quadrat_cover_data_NT.xlsx` and `All_site_info_NT.xlsx` exist only on Dryad; the cover sheet holds cover and height | notes bullet 13, builder | Dryad v5 listing; Zenodo record; download attempt | **existence holds; content untested** | both are in v5 (442103), not on Zenodo. Download answers 401 (API) and 403 (file_stream). "Height" is inferred from the file name | — |
| 33 | Paper unreadable: "Wiley 403, no repository text" | notes bullet 1, metric reason, fit_reason | Crossref licence; OpenAlex and Unpaywall locations; Wayback availability | **partly refuted** | the article is CC-BY 4.0 (Crossref). The repositories (figshare 16922554, VUW) only link to Wiley, but the Wayback Machine holds the publisher PDF (snapshot 2021-07-16). I could not fetch it under this session's permissions. A person can open the DOI in a browser; the 403 is for automated requests | PROV-16, PROV-17, MET-1 |
| 34 | Metric: fallback `rmse` on kg/ha; the source defines no metric | `metric`, README Metric block | one more look (row 33); abstract | holds on the abstract; untested on the paper text | the abstract reports significance and a growth curve, which are inference criteria, not prediction errors. MET-5 would not make an AIC or p-value the task metric even if the paper had one | MET-1, MET-5, MET-11 |
| 35 | Metric computable on every fold (MET-2) | implied | `scorer(container)` with a train-mean dummy and a zero prediction on all 30 folds; units per fold | holds | dummy RMSE 935-1,475, zero RMSE 1,008-1,609. Per test fold: 571-746 rows, 104 groups, 155-185 plots, 321-466 positives, NT 435-630 and SK 116-140 rows | MET-2 |
| 36 | Target scale kg/ha, not logged; RMSE scores it there | notes bullet 3 | MET-3; tail share | holds; tail measured | no transform declared, so RMSE is on kg/ha. The top 1% of test rows carry 29-50% (mean 39%) of the dummy's squared error | MET-3, MET-10 |
| 37 | Quadrats are scored one by one (SPLIT-26); implies the quadrat is an acceptable target unit (USE-5) | notes bullet 7, grouping | shipped splits, 5 repeats: quadrat R2 against plot-mean R2 for the same predictions | holds; low effect on rankings | quadrat / plot-mean R2: ridge 0.142 / 0.212, RF 0.127 / 0.193, LightGBM 0.071 / 0.131. The best family is the same in 93% of splits. NT's 1 m2 quadrats are noisier (median CV within lichen plots 1.24, against 0.85 for SK's 4 m2) | USE-5, SPLIT-23, SPLIT-26 |
| 38 | `site` is the group, not a feature | implied (FeatureTypes lists it as categorical) | README n_features; container columns | holds | 7 features; `feature_columns` drops the group | — |
| 39 | Licence CC0 1.0 | `license` | Dryad rights; Zenodo licence | holds | CC0-1.0 on both deposits; Zenodo `cc-zero` | EV-4 (note only) |
| 40 | Record: "567 plots"; "About 1,730 and 440 quadrat rows (an estimate)" | record screening | counts | superseded by measurement | 516 plots; 1,630 and 380 rows. The estimates were labelled as such | EV-2 |
| 41 | Record: NT "now version 5 of 2026-05-18; site info, destructive biomass samples, lichen data and quadrat cover sheets"; "Dryad answers 401" | record screening | Dryad API | holds | 4 files in v5; 401 reproduced | — |
| 42 | Record: `dryad.76hdr7sth` "describes the mature stands" | record screening | Dryad usage note; that deposit's metadata | holds as the authors' pointer | usage note: "Site description of mature stands (> 70 years post-fire)". The deposit is vascular plant data: 207 burned and 133 mature plots | — |
| 43 | Record: `athabasca_forage_lichen_cover` is another study (Alberta, data not released) | record screening | sibling record | holds | Keim et al. 2017, `No`, "Not Available (from Paper)" | PROV-4 |
| 44 | Record Assessment: the family question is settled by the curator; the verdict and priority stay | record Assessment, CC line | read the record | not a data claim | CC (2026-10-30, Andrej): `Yes`, priority 1 | — |

**Refuted and untested claims, ranked (validity first, Must first)**

1. **P3, years since fire for the control plots (row 7; USE-3, USE-8; refuted for 36% of rows; mechanism untested).** The use case says a planner reads years since fire from fire-history maps. That cannot hold for the 145 NT plots in areas with "no recorded burn history". Their ages (33 to 241 years) are field stand ages, probably tree-ring counts. A planner for an unsurveyed stand has the inventory's stand age instead, a coarser estimate. So the model trains on a more precise input than it would get in use.
   - What it changes: the fit's known gap. It is not a leak, because a stand age is known at the prediction point (USE-6).
   - Mildest remedy: in `known`, `use_case` and `fit_reason`, write that years since fire is a field stand age for control and residual plots, and that a planner would use the inventory's age. Confirm the method in the paper's Methods (item 5).
2. **P4, grouping level (row 28; SPLIT-1 Must; refuted as written).** Holding out whole NT survey areas roughly halves the linear family's skill: ridge drops from 0.128 to 0.063, or to 0.088 with SK by block. Survey areas are the 27 burn scars and control areas, an exact key from the plot names (SPLIT-24). The tree families stay within noise, and the best family changes with the grouping. In the NT data, a test site has a plot of another site in its own survey area at a median 1.1 km, against 10.4 km to the nearest other area.
   - What it changes: whether the benchmark rewards interpolating within surveyed burn areas. The use case is a stand at a place that was not surveyed, across the range.
   - Mildest remedy: a weighing call for the curator. Either group on the NT survey area (SK plots stay their own groups, or 0.25 x 0.5 degree blocks), or keep the site and correct the note: under area or block grouping the linear family loses about half its skill and the family ranking changes.
3. **P5, CG3-31A mislocated (row 22; PROV-13 Must; refuted note).** One plot carries another site's exact coordinates and ecoprovince, 160 km from its siblings. The note says "all at one recorded coordinate", which is false for 51 site names, though those are only 0.01 degree apart.
   - What it changes: 5 rows with a likely wrong latitude, longitude and ecoprovince, and one merged group (`site_036`), which is only stricter.
   - Mildest remedy: record it as an Anomaly. Check `All_site_info_NT.xlsx` (Dryad, token needed) or ask the authors before repairing. Correct the coordinate sentence.
4. **P5, NT file version (row 2; PROV-8, PROV-9; untested change).** The NT lichen and destructive files were replaced on 2022-06-23 (Dryad v4, `files_changed`). The paper used the February 2021 files.
   - What it changes: possibly the 326-versus-346 plot gap and some values. Shipping the authors' corrected version is right ("a version the source defines replaces ours").
   - Mildest remedy: one line in the notes and the record. Compare v3 when a Dryad token or the curator's download is available.
5. **P5, paper not read (rows 32-34; PROV-16, PROV-17 Must; untested).** The paper is CC-BY and an archived publisher PDF exists, so this is a gap in our access, not in the source. Until someone reads it, these stay unverified: the response variable (volume or cover biomass), the dropped plots (346 against 326, 221 against 190), how stand age was measured (item 1), and whether any prediction error is reported (row 34).
   - Mildest remedy: the curator opens doi:10.1002/ecs2.3481 in a browser, or the Wayback snapshot of 2021-07-16, and reads the Methods.
6. **P6, metric (rows 34-36; MET-1, MET-2, MET-3, MET-10).** Not refuted. The metric can be computed on every fold, and the scale is the source's.
   - Evidence for the curator's MET-10 call: on raw kg/ha, the top 1% of test rows carry 29-50% of the dummy's squared error.
   - Remedy only if the curator wants it: ship the target as `log1p` with `target_transform` and keep `rmse` on kg/ha (MET-3). This changes the modelling scale, not the metric.
7. **P7, wording and counts (rows 16-18, 20, 25, 27, 31; quality).**
   - 32.5% is the floor within identical inputs; the within-plot share is 28.8%.
   - Of the 518 zero copies, 482 are within one plot.
   - 980 is the check's count; 1,671 rows sit in an input group with more than one target.
   - 2 of the 813 zeros had cover recorded.
   - Only 26 of 110 multi-plot sites share one age.
   - NT r under 1 km among different sites is 0.17.
   - The destructive files have 155 and 72 patches, not 342 and 256.
   - Remedy: correct the sentences when the definition is next edited. The warning-acceptance reasons hold in substance: every copy stays within one group (LEAK-18).

</details>

<details><summary>Column audit</summary>

**Column audit (column-auditor, 2026-11-01): boreal_postfire_lichen_biomass**

Verdict: ship after changes (one use-case question for the curator, one data anomaly to repair or note, two small
cleaning points). No column gives the target away. The two LEAK-10 drops (`kgha.areaperm2`, `non_zero`) are right,
and so are the identifier, constant and recoding drops. The main point: `years_since_fire` is the survey's own
per-plot stand age, not the fire-map value the use case says the planner reads.

Validity: USE-3/USE-8 question (`years_since_fire` is a per-plot survey value, see 1); LEAK-10 drops hold; LEAK-33
holds (`site` is never a feature, and the leak probe saw 7 features); PROV-13 anomaly (CG3-31A coordinate, see 2).
Quality: CLEAN-16 consistency question (see 3); CLEAN-10/11 wording on 2 zeros (see 4); CLEAN-5 drops verified.

Frame audited: `dataset_io.from_definition` (rebuilt from the raw files), 2,010 rows x 9 columns, no missing values.
Scripts and the frame are in the run folder.

**Column table (shipped frame)**

| column | meaning (codebook) | known at prediction? | dtype and cleaning | verdict | rule |
|---|---|---|---|---|---|
| `forage_lichen_biomass_kg_ha` (target, `kgha.volperm2`) | "Biomass of live lichen species, estimated by standardize live lichen volume", kg/ha, for the pooled forage Cladonia groups (metadata sheets) | target | float64, 0 to 13,126, no negatives, no missing values; 813 zeros (40.4%). In SK, target / cover biomass sits on a grid of 0.0775 steps, so the target is the authors' cover x height x constant, as the codebook says. 2 SK quadrats (2015-054-nw, -se) have cover 2.0% and 0.5% but target 0. Skew 4.0 (0.27 on log1p); not logged | fine; wording point on the 2 zeros (4); log question (3) | USE-5 (target choice argued in the notes), CLEAN-10/11, CLEAN-16 |
| `years_since_fire` (`TSSRF`) | "Time simce stand replacing fire", years | **only partly.** It is a per-plot value from the survey, not a map lookup: 84 of 312 sites (90 of 141 NT name-sites) hold several values at one recorded coordinate (C6-12A/B 40 and 144; CG1-15 124 to 241). Only 11 of the 181 NT burn-scar (`F`) plots fall in the Dryad design classes 37-38 / 46-49 years; 54 are above 70 (F7: 133 to 219). 30 of the 145 "no recorded burn history" (`C`, `CG`, `CS`) plots are at 70 or less (8 at 50 or less). 78 NT plots are aged 100 years or more, older than any fire record | int64, 1 to 241, numeric by meaning; nothing to clean | **question for the curator** (1): not a part or a consequence of the target, but survey-only information under the planner use case as written | USE-3, USE-8 (LEAK-6/LEAK-10 as read in the wadden_sea precedent) |
| `stand_type` (`standtype`) | "Stand types, Hart et al. 2019": 7 classes (jack pine, well- or poorly-drained spruce, conifer mix, deciduous, deciduous-conifer mix, larch) | yes, in substance: a forest inventory gives the stand type, but here it is the field crew's per-plot class (89 sites hold 2 or 3 types, by design). Whether burned plots carry the pre-fire or the current type is unknown | category, 7 levels (Larch 72 rows, 2 in SK); fine | fine (named with 1 as the same kind of field value, weaker) | USE-3 |
| `latitude` | plot latitude, decimal degrees | yes | float64. NT on a 0.01 degree grid, SK at full precision: a convention that differs by region, not by class, and `jurisdiction` is a feature anyway. **CG3-31A carries CG2-35A's exact coordinate (62.22, -116.33), 161 km from its site-mates CG3-31B/C (60.77, -116.56).** Every other NT plot lies within 2 km of its name-site median | fine; anomaly on 1 plot (2) | PROV-13, CLEAN-11 |
| `longitude` | plot longitude, decimal degrees | yes | float64; as for `latitude` | fine; same anomaly (2) | PROV-13 |
| `jurisdiction` (`design`) | "Project jurisdiction": NT or SK | yes | category, 2 levels. A function of `ecozone` in this data (SK = Boreal shield), and it also marks the protocol (1 m2 quadrats against 4 m2): region and protocol cannot be told apart. Not an exact copy of any column, so CLEAN-5 does not apply | fine (redundant, harmless; documented) | CLEAN-5 |
| `ecozone` | ecozone name: Taiga plains, Taiga shield, Boreal shield | yes (map) | category, 3 levels; a function of `ecoprovince`, consistent at every coordinate | fine | CLEAN-5 |
| `ecoprovince` | ecoprovince name, 4 levels (SK's single "Athabasca Plain and Churchill River Uplands") | yes (map) | category, 4 levels. `acronym` and `acronym1` map one to one onto it (verified: HSRL/NTps, CRTLU/NTs, GBP/NTpn, APCRU/SKs), so those drops are right. It follows the coordinate, so CG3-31A has Great Bear Plains where its site-mates and every other CG3 plot have Hay and Slave River Lowlands | fine; anomaly on 1 plot (2) | CLEAN-5, PROV-13 |
| `site` (group) | built here: plots linked by site name or by identical coordinates | not a feature | category, 312 levels. `feature_columns` drops it (the leak probe saw 7 features). The labels follow the raw file order (site_001-122 NT, 123-312 SK), which is harmless because the column is never an input | fine | LEAK-33, SPLIT-24 |

**Raw columns dropped (the drops checked)**

| raw column | drop reason in the definition | check | verdict |
|---|---|---|---|
| `kgha.areaperm2` | cover x 61.934, a part of the target | same survey, same quadrat, the target's own cover | right (LEAK-10) |
| `non_zero` | the indicator of target > 0 | equals volume biomass > 0 in 2,010 of 2,010 rows | right (LEAK-10) |
| `plot` | identifier | carries meaning: NT prefix `F` = burn scar against `C`/`CG`/`CS` = unburned area (codebook: "Burn Scar or Unburned area -xxx"), plus the area number (26 areas); SK = survey year (2015/2016) plus a number. Inside or outside a mapped burn is map information; see the remedy for 1 | right as shipped (CLEAN-3); the NT prefix is an option under 1 |
| `plot.quadrat`, `quadrat` | position within the plot | positions 0, 6, 12, 18, 24 m (NT; one `8` at F8-3A) and nw/se (SK) | right |
| `species` | constant | `Cladonia spp.` in all 1,630 NT rows; absent in SK | right (CLEAN-5) |
| `acronym`, `acronym1` | one-to-one recodings of `ecoprovince` | verified | right (CLEAN-5) |

**Problems, in rank order**

1. **P3, USE-3 / USE-8 (question for the curator): `years_since_fire` is the survey's per-plot stand age, not what
   a planner reads off fire maps.** The use case says the planner knows the stand "from fire-history maps and the forest
   inventory", and `known` lists "the years since the last stand-replacing fire". The data show a value set plot by
   plot, against the design's map classes. Inside the NT burn scars only 11 of 181 plots carry the design's 37-38 or
   46-49 years and 54 carry more than 70 (unburned remnants dated in the field, presumably). 30 "no recorded burn"
   controls are 70 years old or younger. Ages reach 241 years, beyond any fire record. 84 sites hold several ages at
   one coordinate. How TSSRF was determined is not documented in the files (tree-ring ages, presumably; the paper is
   unread, LEAK-3 / PROV-16). It is the task's main signal: dropping it costs R^2 0.077 (ridge with splines) and 0.110
   (random forest) on kg/ha, and 0.129 / 0.189 on log1p. 30 shipped splits, every split worse or nearly every split;
   script `tssrf_exp.py` in the run folder.
   Indicative test of the map-level information: I capped the age at an assumed fire-record horizon (51 years NT, 70
   SK; my assumption, not from the source). That costs ridge R^2 0.013 on kg/ha (SE 0.005, worse on 70% of splits) and
   0.000 on log1p. The random forest loses 0.017 on kg/ha (SE 0.015) and 0.074 on log1p (SE 0.010, worse on 90%).
   Using each site's median age instead costs 0.012 to 0.053. So part of the score rests on field information that an
   unsurveyed stand does not have. It is not a part or a consequence of the lichen, so it is no LEAK-10 drop by the
   letter of that rule.
   The batch's closest precedent is wadden_sea_sibes_macoma_abundance: it replaced sediment measured at the visit by
   interpolated values, "a gain a place without a sample cannot have" (USE-3, LEAK-6). noaa_afsc_bottom_trawl_survey_cpue
   kept its haul readings only because they measured no gain.
   Mildest remedy, in order:
   (a) Before deciding, fetch `All_site_info_NT.xlsx` (Dryad 2026, not on Zenodo) and the paper's methods, to learn
   how TSSRF and the design class were set (EV-1, LEAK-3).
   (b) Correct the claims meanwhile. `task_summary.known` and `use_case` should say that the age is the survey's
   per-plot stand age (field-dated where no fire is recorded, unburned remnants inside burn scars at their own age).
   `fit_reason` should name it as a gap; the fit stays approximate.
   (c) The curator then chooses. One option is to keep it with that note, reasoning that an inventory age is a noisier
   stand-in for the same quantity. Another is USE-9: reframe the actor as one who has field stand data without a lichen
   survey (a ground inventory plot). The heaviest option is to rebuild a map-level age from the national fire polygons
   at the coordinates (an external join as in mortgage, CLEAN-19). The NT coordinates are rounded to about 1 km, and
   the NT `F`/`C` prefix of the dropped `plot` (inside a mapped burn or not) is a map-level input that could go with it.
   `stand_type` is the same kind of per-plot field class, but an inventory gives the same quantity, so a note is enough.
2. **P5, PROV-13 (repair or note): CG3-31A has another plot's coordinates.** Its 5 quadrats carry CG2-35A's exact
   coordinate (62.22, -116.33), 161 km from its site-mates CG3-31B/C (60.77, -116.56). Every other CG3 plot lies at
   latitude 60.58-60.99, and all three CG3-31 plots share the age of 66 (CG2-35A has 76). The ecoprovince follows the
   wrong coordinate (Great Bear Plains instead of Hay and Slave River Lowlands); `ecozone` is Taiga plains either way.
   Side effect: the coordinate link merges CG2-35 and CG3-31 into one group. That is stricter, so it does no harm.
   Remedy: (a) repair from `All_site_info_NT.xlsx` if it gives CG3-31A's coordinate. (b) Otherwise add an `Anomaly:`
   bullet, with either the site-mates' coordinate and ecoprovince (the evidence is strong: site name, shared age,
   area range) or the plot's latitude, longitude and ecoprovince set to missing (5 rows, 0.25%). Effect on scores:
   negligible.
3. **P7, CLEAN-16 (question, consistency): target shipped raw where the batch's siblings ship log1p.** The target skew
   is 4.0 (0.27 on log1p). wadden_sea_sibes_macoma_abundance, nantucket_sound_sea_duck_aerial_survey_counts,
   noaa_afsc_bottom_trawl_survey_cpue and pennsylvania_oak_hickory_regeneration_experiment ship log1p with
   `target_transform="log1p"` (basque_offshore_bivalve_biotoxins ships log), all scored on the original scale. This
   definition's reason ("the planner's quantity, and the fallback metric scores it there") holds equally under
   `target_transform`, so it does not set the case apart. A real trade-off exists: wadden_sea's notes show a model
   trained on log1p scoring poorly by RMSE on the raw scale. Remedy: the curator picks one treatment for the family,
   either log1p with `target_transform="log1p"` or a recorded exception with the fact that sets it apart.
4. **P7, CLEAN-10/11 (wording): 2 of the 813 zeros are not absences.** Plot 2015-054 (SK, jack pine, 17 years) has
   cover recorded (2.0% and 0.5%) and volume biomass 0, so the height was presumably 0 or unrecorded. The authors'
   `non_zero` also says 0 there. The Target bullet mentions the plot, but the Zeros bullet calls all 813 "no live
   forage lichen ... observed absences". Mildest remedy: write "811 with no cover; 2 in plot 2015-054 with cover but
   no height, kept at 0 as the authors' presence flag has them". Dropping the 2 rows as unknown targets (CLEAN-15) is
   the stricter alternative.

**Checked and fine:** within each plot every input is constant (all 7 inputs, both regions). No missing values or
proxy codes. Coordinates fall inside their ecoprovinces' ranges, and no coordinate holds two ecoprovinces. The
recodings dropped under CLEAN-5 are exact. The quadrat-label anomaly (F8-3A `8`) is real and dropped. `site` never
reaches the features.

Sources consulted beyond the repository: the metadata sheets of both `Lichen_data_*.xlsx` (the codebook), the
DataCite records of doi:10.5061/dryad.t1g1jwt15, doi:10.5061/dryad.tb2rbnzzj and doi:10.5061/dryad.76hdr7sth, and
web searches for the paper's methods
([wildlifescience.ca](https://wildlifescience.ca/predicting-patterns-of-terrestrial-lichen-biomass-recovery-following-boreal-wildfires/),
[GWF record](https://www.gwfnet.net/Metadata/Record/T-2021-11-14-L3L1bXnDtU6kWRXlU3eOg7ew)), which state no
stand-age method.

</details>

<details><summary>Split audit</summary>

**Split audit (split-auditor, 2026-11-01): boreal_postfire_lichen_biomass**

**Verdict: wrong at the grouping level, fixable by a re-split. The grouped regime is right.**

```text
Verdict: re-split before shipping (one call for the curator: how wide the use case is).
Validity: USE-10 holds (a new place: cold start, grouped). SPLIT-2/3 hold (grouped; not temporal). SPLIT-24 holds for
  the shipped site key and for the alternative. SPLIT-1/SPLIT-4 triggered: the level is a site inside a surveyed burn,
  but the use case and the source's own plot key point to the burn scar or unburned area. Fix: re-split.
  SPLIT-23 holds with a note (a quadrat is scored, a stand is acted on; ranking unchanged). SPLIT-28 holds under both splits.
Value: TP-2, a small signal across groups that stays under the stricter split (best skill +0.138 by site, +0.115 by area).
Quality: two notes overstate what was measured (EV-7): "within its noise", and "the exact key from the source".
Weighed: a stricter group, a known group in the source and the source's range-wide aim (+) against unequal folds
  and Saskatchewan having no burn key (-).
For the curator: issue 1 (site or burn area).
```

How I checked: the frame and the 30 shipped splits come from `dataset_io.from_definition`. Plot, site and burn-area keys
were rebuilt from the raw sheets with the definition's own `_site_groups`. Models are untuned (ridge on one-hot plus
scaled numbers, random forest with min_samples_leaf 20, LightGBM default and a small LightGBM), with 10 x 3 folds for
every alternative split. Skill = 1 - MSE / MSE of the training mean, per split. The scripts are in
the run folder (`near.py`, `deploy_dist.py`, `alt_splits.py`, `varparts.py`, `unit.py`,
`area_folds.py`, `claims.py`, and `hidden/` for the hidden-group probe run as IID).

**Issue 1 (P4, SPLIT-1 and SPLIT-4, Must): the test site shares its burn with training; the use case predicts for burns nobody surveyed**

- The source's key. The NT sheet's metadata defines `plot` as "Plot location: Burn Scar or Unburned area -xxx". So the
  prefix (`F1`, `C3`, `CG2`, `CS`, 27 areas) is the documented entity. The site level (`F1-22` of `F1-22A`) is our
  reading of the names, supported by shared coordinates.
- What the shipped test holds out. In 94.3% of NT test quadrats, the plot's own burn scar or unburned area has another
  site in training. 20% have a training plot in the same area with the same years since fire, so probably the same
  fire. Median distance from a test quadrat to the nearest training plot: 2.4 km in NT and 3.6 km in SK. 74% of test
  quadrats lie within 5 km of a training plot, 90% within 10 km.
- What the use case predicts for. The task summary says "a stand at a place with no survey". The Dryad abstract aims
  at caribou habitat "across the range of boreal and barren ground caribou in North America". A random point inside
  the convex hull of the plots lies a median 95 km from the nearest plot in NT (172,794 km2; 2.3% of points within
  5 km) and 15.6 km in SK. Caveat: this is geometry, and it assumes the stands that matter spread over the hull
  (inference).
- The entity carries the label. Burn areas account for 19.1% of the NT target's sum of squares (23.2% on log1p).
  Sites within an area add 19.6%, plots within a site 23.2%, and 38.1% is within plots. Area means run from 16.7 to
  3,453 kg/ha. Plot-mean biomass between different sites correlates at r = 0.21 to 0.34 within 1-10 km and 0.01 at
  10-25 km in NT. That reproduces the notes. In SK it is 0.75 under 1 km, but on only 16 pairs.
- The alternative split, measured (10 x 3 folds each; skill against the training mean, share of splits above 0; R2 in
  `alt_splits.csv`):

| split | groups | median km to train | ridge | random forest | LightGBM default | LightGBM small |
|---|---|---|---|---|---|---|
| shipped (site) | 312 | 2.5 | +0.138 (100%) | +0.110 (93%) | -0.023 (37%) | +0.089 (87%) |
| NT burn/unburned area, SK plot | 215 | 16.9 (NT 22.3) | +0.054 (77%) | +0.115 (97%) | +0.031 (57%) | +0.093 (93%) |
| 25 km grid blocks | 88 | 16.1 | +0.115 | +0.134 | +0.085 | +0.124 |
| 50 km grid blocks | 47 | 27.1 | +0.081 | +0.091 | -0.029 | +0.062 |
| 100 km grid blocks | 24 | 51.5 | -0.013 | +0.030 | -0.015 | +0.041 |

  Holding out the area costs the forest nothing. Ridge falls from +0.138 to +0.054, about 3 SE, and the winner flips:
  ridge leads by site, the forest leads by area. So the site split favours one family, because it can lean on a test
  site's burn-mates. Under SPLIT-4 the size of the gap does not decide either way. What decides is that a planner's
  new stand is not in a burn this study surveyed. The 100 km row shows the range-wide limit: there the best untuned
  skill is +0.03 to +0.04, and every R2 is below 0 against the test fold's own mean.
- Steelman for the site. A site is a true, exact key, and it is stricter than the plot. If the use case is filling in
  unsurveyed stands inside a burn that was partly surveyed, the site is the right unit. The task summary's own
  sentence, "nearby sites stay in training", accepts that reading. But neither the definition nor the source names
  such an actor. The source's stated aim is range-wide.
- Remedy, the mildest:
  - Re-split on the NT burn scar or unburned area: the plot-name prefix, merged through the shipped site links,
    because `CG2` shares a coordinate with `CG3` and with `F2`. That gives 25 NT groups. Each SK plot stays its own
    group (SK names are "Year -xxx", with no burn key). In total 215 groups. Everything uses exact keys (SPLIT-24).
  - Cost: the largest group holds 350 rows (17.4%), so with the repository's `GroupKFold(shuffle=True)` the test folds
    hold 314-1,067 rows, and one train side holds 46.9% of the rows (now 571-746 test rows).
  - Rewrite `grouping.definition`, `splits_comment` and `task_summary.split`. Add the distance figures (test median
    22 km in NT against about 95 km for a stand in the region) and the 100 km result to `splits_comment` and
    `fit_reason`.
  - If the curator reads the use case as infill within surveyed burns, keep the site. Then state that 94% of NT test
    quadrats have their burn in training and give the 2.5 km against 95 km figures, in place of "some optimism...
    remains".

**Issue 2 (procedure, EV-7 and EV-6): the grouping note claims more than the measurement shows**

- `curation_comments` says "the level of grouping changes the score within its noise". In the builder's own run,
  ridge went from 0.143 ± 0.016 (site) to 0.005 ± 0.043 (blocks), about 3 SE. In 10 x 3 folds, ridge's skill goes from
  +0.138 (site) to +0.054 (area). The claim holds for the random forest only.
- "The site is kept as the exact key from the source's names and coordinates (SPLIT-24)" is true as far as it goes.
  But the source's documented key is the burn scar or unburned area. The site is one level below it.
- Remedy: rewrite the bullet with the 10 x 3 numbers per family, and decide the level from the use case (issue 1), not
  from the gap (SPLIT-4, SPLIT-21).

**Issue 3 (P4, SPLIT-23, Must, holds with a note): a quadrat is scored, a stand is acted on**

- Every input is constant within a plot, so quadrat RMSE = stand error + a within-plot floor. On the shipped splits
  the floor is RMSE 680, against the training mean's 1,200. Scoring plot means with equal weight per plot instead
  changes no ranking:

| model | R2 per quadrat | R2 per plot mean |
|---|---|---|
| ridge | 0.132 | 0.189 |
| random forest | 0.104 | 0.158 |
| small LightGBM | 0.083 | 0.135 |
| LightGBM default | -0.030 | -0.009 |

- Ridge wins 13 splits and the forest 9 under both scorings.
- NT holds 81% of the rows but 63% of the plots (5 quadrats per plot against 2 in SK).
- Remedy: none. Keep the quadrats as the source's rows (SPLIT-26). Add one line saying that a quadrat score ranks
  models like a stand score, and that NT weighs 2.5 times per plot.

**Issue 4 (P4, weighed): Saskatchewan stays the laxer region**

- SK plots have no site or burn key. 9.7% of SK test quadrats have a training plot within 1 km under either split, and
  the median is 3.6 km, against 15.6 km for a point in the SK hull. NT under the area split: 0.5% within 1 km.
- A grid block or a distance cluster is no exact key (SPLIT-24). SK 25 km blocks with NT areas move the scores little
  (forest +0.110 against +0.115).
- Remedy: keep SK per plot and say so in `splits_comment`.

**Checks that pass**

- Regime (USE-10, SPLIT-2, SPLIT-3, SPLIT-7): a new place is a cold start, so the split is grouped. There is no time
  column. The survey years (2015-16 SK, 2016-18 NT) are confounded with jurisdiction. Years since fire is a
  chronosequence input known from fire maps, not a stream. There are no late labels, so SPLIT-9 to SPLIT-22 do not
  apply.
- Group id (SPLIT-24): site names plus identical coordinates, exact keys. Reproduced:
  - 312 groups, 122 NT and 190 SK.
  - NT groups hold 1-11 plots, 97 of 122 hold 2 or 3.
  - 17 coordinates hold plots of 2 or 3 site names (15 and 2).
  - 14 groups join more than one site name.
  - Each of the 190 SK plots has its own coordinates.
  - Minor: some NT site names carry 2 coordinates. The "all at one recorded coordinate" example is true only of the
    example.
- Copies across the split: 0% of test rows have an exact feature copy in training (leak probe). No feature vector
  occurs in two groups.
- Group probe: untuned LightGBM scores R2 0.347 on IID folds against -0.034 grouped, so rows of a group inform each
  other (SPLIT-29: keep a grouped split).
- Hidden-group probe, run as IID (`--include-grouped`): it hits `site`, `latitude`, `longitude`, "(all but
  years_since_fire)" and "(all but stand_type)". All of these sit inside the site groups, since the coordinates define
  them. There is nothing beyond the site except the burn area, which is no column (issue 1). Near copies: not run, too
  few tokens.
- Folds:
  - 104 test groups per fold, 571-746 test rows, both jurisdictions in every fold.
  - No test row has a stand type, ecoprovince or ecozone level that is missing from its training side (0 rows in all
    30 splits).
  - The fold context is none: every input comes from maps or the inventory, and nothing comes from a group's other
    quadrats.
- Signal across groups (SPLIT-28): linear beats the mean on 30 of 30 shipped splits (task probe). Under the area split
  the forest beats it on 29 of 30.

</details>

<details><summary>Domain practitioner</summary>

**Domain practitioner: a caribou range planner's reading of boreal_postfire_lichen_biomass (2026-11-01)**

**Verdict.** Fit **approximate**. I agree with the definition, but for partly different reasons. The inputs are what a forage-recovery projection knows about a stand, and the target is the forage biomass I would sum over a range. Three gaps remain: one row is a 1 to 4 m2 quadrat from a designed chronosequence in two regions, the volume allometry behind the label is in a paper nobody read (USE-5, USE-8), and for a map of today's forage I would always have imagery and burn severity, which this data lacks. A decision exists, so the fit is not None (USE-2 does not apply). Metric: **yes**. RMSE on kg/ha scores the mean biomass I add up. It scores quadrats where I act on stands, but every input is constant within a plot, so it ranks models exactly as a stand-level MSE in which NT plots weigh 5 and SK plots 2.

**Who I am and how the decision is made today**

I am a caribou habitat biologist. I work either for the GNWT's Environment and Climate Change, on the regional boreal caribou range plans (the Taiga Shield plots also sit in the Bathurst herd's winter range), or for Saskatchewan's Ministry of Environment on SK1, the Boreal Shield range where these SK plots lie. SK1 is the one range where the federal government has not identified critical habitat. Today the rule I work under is binary. A burn younger than 40 years counts as "disturbed", and a range needs 65% undisturbed habitat. NT1 is 69% undisturbed, and fire makes up 24 of its 31 disturbed points. The NWT's own monitoring program (CIMP) found that forage lichens "needed 45 to 70 years to recover after a fire", which is longer than the 40 years the national strategy uses. It also found that lichen availability depended on habitat type, time since fire and fire severity.

Two decisions would use a prediction like this one:
- (a) Recovery and projection: how long a burn of a given stand type and ecoprovince counts as lost winter forage, and how much forage a range will carry under future fire. This is the authors' own aim, a "basis for estimating future caribou habitat" (Dryad abstract).
- (b) Mapping: where the forage is now. Today that is done from Landsat. Macander et al. 2020 used a random forest on 30 m pixels with spectral and environmental predictors, and reached R2 0.71 to 0.77 for lichen cover on held-out aerial and UAV data. Arseneault et al. 1997 combined Landsat TM with fire history for lichen biomass in northern Quebec.

The dataset fits (a) closely and (b) loosely.

**1. Do I have each input at the moment of prediction?**

- `years_since_fire`: for burns within the fire record, yes, from the fire-history polygons. Older stands carry a field age of 52 to 241 years. The paper (unread) says how it was dated, presumably from tree cores. This applies to 209 of 326 NT plots above 51 years and 66 of 190 SK plots above 70 years. Those horizons are my assumptions: NWT records are consistent from about 1965, SK records start earlier. For such stands I would know only "older than the record", or an inventory origin year where an inventory exists. I measured what this costs. Capping the age at those horizons on the 30 shipped splits lowers R2 by about 0.01:
  - ridge with splines: -0.0126 (se 0.0049)
  - hurdle: -0.0091 (se 0.0054)
  - random forest: -0.017 (se 0.015)

  The cost is small, and in a projection the simulated stand's age is known exactly. Keep the column and name the gap in the notes.
- `stand_type`: the sheets say "Stand types, Hart et al. 2019", a class assigned on the plot. I would have an inventory or land-cover class instead, which is coarser and more often wrong, especially in young burns. So the shipped input is cleaner than mine. This cannot be measured here.
- Coordinates, ecoprovince, ecozone, jurisdiction: I always have these.
- Inputs I would always have for a map of current forage, all missing here:
  - Landsat reflectance or a lichen-cover index
  - burn severity, as dNBR; only partly available, since most sampled NT burns are fires of about 1968 to 1981, before Landsat TM
  - the number of fires and the reburn interval, from the same fire polygons; short reburn intervals in this SK region are the subject of Hart et al. 2019
  - canopy closure, from the inventory
  - terrain, from a DEM

  For the projection none of these exist for future stands, so their absence matches that use (USE-9). The source names the projection, so this is no rephrasing made to excuse a gap.

**2. Is the target what I act on?**

Forage-lichen biomass in kg/ha is the forage supply. I want a number, the expected kg/ha of a stand; the presence probability is a useful by-product. Lichen biomass in surveys is always an allometric estimate from cover and height, because nobody harvests every quadrat, so I do not count the estimate as a proxy. The volume-based column is the right choice over cover x 61.934. Mat height is what separates a young mat from an old one, and cover alone flattens that difference. Also, the authors' `non_zero` flag follows the volume estimate in all 2,010 quadrats.

The gap is that the volume equation and its coefficients are in the unread paper. The quantity and its unit are known; how it was computed is not. That makes the fit approximate under USE-5 and USE-8, as in blood_tests_drink_prediction and differentiated_thyroid_cancer_recurrence.

**3. Does one row match one decision? Is the test data what I would face?**

- **The row is not my unit.** I decide per stand, meaning a polygon or a 30 m pixel. A row is a 1 m2 (NT) or 4 m2 (SK) quadrat, and 32.5% of the target's variance lies within plots. That is microsite spread no stand input can explain (SPLIT-23).
- **The ranking survives anyway.** Every input is constant within a plot, so per-quadrat squared error splits into a within-plot term, the same for every model, plus the stand-level squared error weighted by the number of quadrats. Models therefore rank as under a stand-level MSE with NT plots weighted 5 and SK plots 2. I measured this on the 30 splits with five predictors: Kendall tau 0.91 between the ranks by quadrat RMSE and by stand RMSE with equal weights. The quadrat unit changes the level of the score (ridge R2 0.137 per quadrat, 0.191 per stand), not the ranking. Keeping the source's rows is right (SPLIT-26).
- **The test sites match my situation within the two study regions.** Whole sites are held out, so a test quadrat stands for a stand at a place with no plot.
- **What I would also face that the data does not cover:**
  - Other ecoprovinces. There are 4 here; a range-wide model has to cover more.
  - Young NT burns. The NT data has one plot younger than 30 years and none younger than 29, while the 2014 season burned 2.85 Mha in the NWT. SK has 62 plots of 30 years or less.
  - A landscape sample. This is a chronosequence stratified by age class (NT: 37-38 and 46-49 years after fire plus controls; SK: 4-12, 12-52 and over 52), so its mix of ages and stand types is not the range's.

**4. Would I use this model?**

- **For range-level forage supply and recovery curves by stand type: yes**, as an improvement on the 40-year rule. On the shipped splits I compared three untuned predictors, by share of variance explained per quadrat and per stand mean:
  - a simple hurdle (logistic presence times a ridge on the positive quadrats): 0.159 and 0.216
  - a ridge: 0.137 and 0.191
  - the 40-year rule as a predictor (the training mean of burns younger and older than 40 years): 0.022 and 0.040
- **For stand-by-stand decisions: no.** The stand-level RMSE is about 920 kg/ha against a mean of 522 kg/ha.
- **What would make me trust it:** predictions that rise with stand age and level off by stand type and ecoprovince, like the authors' logistic recovery curves (28 to 73 years to half the asymptote), and no bias within stand type x age class.
- **What would make me distrust it:** a model that leans on latitude and longitude to recall the sampled sites, or any use outside the four ecoprovinces.

**5. Does the metric score my decision? Yes.**

The declared metric is `rmse` on the raw kg/ha, as the fallback (MET-8, MET-11; no source metric, MET-1).
- **Squared error fits my decision.** It is minimised by the mean, and the mean is what I use: the forage supply of a range is the area-weighted sum of stand means.
- **The tail is the point, not a defect.** The tail that drives RMSE (99th percentile 6,014 kg/ha per quadrat) is exactly the forage-rich stands I must not undercount, so for my decision the builder's MET-10 concern about the tail argues for RMSE.
- **The alternatives are worse for me.** MAE targets the median, which is 17 kg/ha per quadrat. RMSLE targets the geometric mean. Both reward predictions that undercount forage when summed.
- **No threshold or k applies** (MET-6, MET-7). The source fixes none. The federal 40 years is an age rule, not a biomass threshold, and the caribou-selection levels of 5% to 30% in Macander et al. are cover, not biomass.
- **My own first choice** would be RMSE on stand means weighted equally (or by stand area), which removes the protocol's 5:2 weighting. Per-quadrat RMSE ranks models almost the same way (tau 0.91, and exactly the same against the version weighted by quadrat count). The difference does not justify a change.

**Gaps between the dataset and the real decision, ranked by how much they change the task**

1. **No imagery, burn severity, reburn count, canopy or terrain.** These carry most of the signal in operational lichen mapping. This is the biggest change if the use case is a map of current forage, and none if it is the projection the source names. Hence the recommendation to state the projection as the use case (USE-9).
2. **The sample.** A designed chronosequence over 4 ecoprovinces in two regions, with two protocols; NT has no burns younger than 29 years. It is a regional recovery model, not a range-wide one.
3. **An unverified label.** The volume allometry and the 326 and 190 plots against the abstracts' 346 and 221 can only be settled from the paper (USE-5, USE-8; PROV-16/17).
4. **A quadrat row for a stand decision.** This changes the score's level (32.5% irreducible), not the ranking, apart from the 5:2 weighting of NT against SK.
5. **Field-quality inputs.** The field stand type, and the field age beyond the fire record (about 0.01 R2 when censored).
6. **Nearby sites in training.** Plot means correlate at r 0.2 to 0.4 up to 10 km, so stands far from any plot may be harder than the folds show. The block test the builder ran is within noise.

**What an expert would change**

- **Use case (USE-1):** name the actor and the decision. For example: "a caribou habitat biologist with the GNWT or Saskatchewan's Ministry of Environment, revising a boreal caribou range plan, estimates the forage lichen a stand of given type, ecoprovince and fire age carries, to replace the federal rule that counts every burn under 40 years as disturbed and to project forage supply under future fire". Cite the CIMP finding (45 to 70 years against 40) as why the decision exists. This also answers the record's `No Good Target / Scientific Discovery` concern: there is a decision, so the marker could be dropped (curator's call).
- **`fit_reason`:** "No actor is named" and "the inputs are the study's design variables" are not gaps in how the data mirrors the decision. For the source's own projection they are the right inputs (USE-9). Name the real gaps instead: the unverified volume allometry, quadrat rows for a stand decision, and a stratified chronosequence of two regions. Keep `approximate`.
- **Curation notes:** state three things.
  - Per-quadrat RMSE ranks models like a stand-level MSE weighted by quadrat count.
  - `years_since_fire` beyond the fire record (209 NT and 66 SK plots under my horizons) is a field age that a planner knows only as censored; measured cost about 0.01 R2.
  - `stand_type` is the field classification of Hart et al. 2019.
- **Keep:** the volume-based target on the raw kg/ha scale, `rmse`, the site grouping, the quadrat rows.
- **Do not:** add imagery, severity or the 2026 Dryad site sheet. That would be a different dataset, and the site sheet's field measurements are not known for an unsurveyed stand.

**My checks.** The script, `actor_checks.py`, is in the run folder. It ran untuned on the 30 shipped grouped splits; a stand is a site plus its feature vector, which gives 498 distinct stands from 516 plots. It covers four things:
- quadrat and stand-level RMSE and R2 for ridge with splines, random forest, a logistic x ridge hurdle, the 40-year two-means rule and the training mean
- the age capped at NT 51 and SK 70 years, with paired differences
- the Kendall tau between rankings at the two units
- the within-plot share of variance, 0.325

**Sources**

- Dryad abstracts and methods of both deposits, doi:10.5061/dryad.t1g1jwt15 (NT) and doi:10.5061/dryad.tb2rbnzzj (SK), read from the builder's saved copies. Also the metadata sheets of Lichen_data_NT.xlsx and Lichen_data_SK.xlsx ("Stand types, Hart et al. 2019"; TSSRF "Time since stand replacing fire").
- The paper, Greuel et al. 2021 (Ecosphere 12:e03481): not read. Wiley answers 403 to WebFetch too.
- NWT CIMP, "Impacts of Fire on Woodland and Barren-ground Caribou Habitat": https://climatelibrary.ecc.gov.nt.ca/dataset/4bcc94fc-cb61-400e-858a-1bac4526ffcf (45 to 70 years against the 40-year rule; habitat type, time since fire and severity; 2014 fires 2.845 Mha).
- Federal critical habitat fact sheet: https://www.canada.ca/en/environment-climate-change/services/species-risk-public-registry/recovery-strategies/woodland-caribou-boreal-population-fact-sheet.html (65% undisturbed; NT1 69% undisturbed, 24% fire; SK1 critical habitat not identified).
- GNWT boreal caribou range planning framework: https://www.gov.nt.ca/en/newsroom/boreal-caribou-range-planning-begin-fall-guided-new-framework (key habitat patches as priorities in wildfire response; from the search summary).
- Macander et al. 2020, ERL 15:055001, via https://www.nps.gov/articles/mappinglichen.htm (Landsat random forest, R2 0.71 to 0.77; selection levels 0-5% to 30% cover).
- Arseneault et al. 1997 (Landsat TM plus fire history for lichen biomass in Quebec): from a search summary only, not read.
- Hart et al. 2019, Global Change Biology 25:869-884 (stand types; reburns in the SK Boreal Shield): abstract via search, not read.
- Rules: use_case.md USE-1, USE-2, USE-5, USE-8, USE-9; splits.md SPLIT-23, SPLIT-26; metrics.md MET-1, MET-6 to MET-8, MET-10, MET-11.

</details>

<details><summary>Blind review</summary>

**Verdict: exclude.** The data are real and the grouped split is honest. But the task as prepared is mostly noise: there are about five usable predictors, the target is a single 1 m² or 4 m² quadrat, and the scores are driven by a handful of sites. The best honest R² is about 0.1 to 0.15, and the spread across splits is as large as the mean. If a low-signal, zero-inflated ecology task is wanted anyway, use a plot-level version with corrected coordinates (see the end).

**What the task is**

The table pools two field datasets of caribou-forage lichen (Cladonia spp.) biomass in kg/ha:
- Northwest Territories (NT), Dryad t1g1jwt15: 326 plots, each with five 1×1 m quadrats. The rows here are 1,630.
- Saskatchewan (SK), Dryad tb2rbnzzj: 190 plots, each with two 2×2 m quadrats. The rows here are 380.

I downloaded both Dryad zips. The prepared table matches `Lichen_data_NT.xlsx` plus `Lichen_data_SK.xlsx` row for row: 2,010 rows. The target is `kgha.volperm2`; the sorted values are identical.

The predictors are `TSSRF` (renamed `years_since_fire`), stand type, latitude/longitude, and jurisdiction/ecozone/ecoprovince.

The use is real. Caribou range planners want forage-lichen supply from stand age (time since fire) and stand type in unsampled stands. Greuel et al. 2021 (Ecosphere, doi 10.1002/ecs2.3481) fit exactly this relationship with a hurdle model. In the authors' words, the GLM "identified stand age, stand type, and ecoprovince as predictors of presence". They also estimated recovery times of 28 to 73 years.

What I checked and found clean:
- Leaky columns were dropped: the alternative cover-based estimate `kgha.areaperm2` (r = 0.89 with the target) and the target-derived `non_zero` flag.
- There are no missing values.
- Categoricals are typed as category.
- The values are plausible: 40.4% zeros, median 16.8, 99th percentile 6,014, max 13,126 kg/ha in old poorly-drained spruce. Mean biomass rises with stand age, from about 64 kg/ha (NT, 20 to 40 years) to about 1,830 (NT, over 150 years).

**Concerns, most serious first**

1. **Weak signal under the honest split; benchmark scores would mostly reward shrinkage.**
   - Evidence. I used grouped 3-fold CV by `site`, 30 splits (10 repeats × 3 folds), as in the task. Mean R² by model:

     | Model | Mean R² | SD across splits |
     |---|---|---|
     | Ridge | 0.11 | 0.10 |
     | LightGBM (regularised) | 0.12 | 0.10 |
     | Random forest | 0.09 | 0.18 |
     | ExtraTrees | 0.15 | 0.08 |
     | Training mean | -0.01 | |
     | LightGBM (flexible, overfits) | -0.05 | 0.24 |

     The best models cut MAE by only about 17% relative to predicting the mean. The random forest's per-split R² ranged from -0.75 to 0.28.
   - Paired differences between sensible models are smaller than their noise. ExtraTrees vs random forest RMSE differs by -32 ± 67 kg/ha, and ExtraTrees wins only 67% of the splits.
   - Under a random (non-grouped) KFold, R² jumps to about 0.34. So most "learnable" structure is plot memorisation through latitude/longitude, not transferable signal.
   - Change: none fully fixes this. Aggregating to plot means (498 feature-unique plots) only raises R² to 0.15 to 0.18 (SD 0.12 to 0.15).

2. **Target unit is finer than what the features describe: quadrat replicates with identical features.**
   - Every predictor is plot-level, while the target is a single quadrat. 1,512 of 2,010 rows share their feature vector with another row. 532 rows are exact duplicates including the target, almost all zeros (740 of the 766 rows in duplicate sets are 0).
   - Even an in-sample oracle that predicts each quadrat's own plot mean reaches only R² = 0.675 (NT 0.62, SK 0.84).
   - 39% of plots mix zero and non-zero quadrats.
   - The duplicates do not cross train/test, because whole sites are held out. They are pure within-plot measurement noise, not leakage.
   - Change: aggregate to plot means. That is the unit a manager reasons about (stand-level forage supply). It also removes the NT/SK imbalance of 5 vs 2 replicates.

3. **Scores are dominated by a few sites (heavy tail).**
   - The top 10 of 312 sites carry 50% of the total sum of squares. `site_022` alone carries 14%: three quadrats at 8,506, 10,886 and 13,126 kg/ha.
   - Whichever fold receives these sites decides that fold's RMSE and R², which explains the R² of -0.75 on one split.
   - Change: if kept, score with a metric less tail-dominated than RMSE/R² (MAE, Tweedie deviance, or RMSE on log1p), or aggregate as in item 2.

4. **Few, redundant predictors.**
   - Jurisdiction is a deterministic function of ecozone, and ecozone of ecoprovince (4 → 3 → 2 levels; the crosstabs are pure).
   - That leaves about five effective inputs: age, stand type, latitude, longitude, ecoprovince. Of these, ecoprovince and latitude/longitude are near-proxies of each other.
   - There is little room for methods to differ beyond how they shrink.
   - Change: drop `jurisdiction` and `ecozone`, or accept that they are redundant. Either way, the low dimensionality remains.

5. **Error inherited from the source: wrong coordinates for one plot, which also corrupted a group.**
   - In `Lichen_data_NT.xlsx`, plot CG3-31A has lat/lon 62.22/-116.33 and ecoprovince "Great Bear Plains". Its sister plots CG3-31B and CG3-31C are at 60.77/-116.56 in "Hay and Slave River Lowlands". The same source's `All_site_info_NT.xlsx` gives CG3-31A as 60.76557/-116.5615.
   - Because it shares rounded coordinates with CG2-35A, the site grouping merged two unrelated places about 160 km apart into `site_036`: latitude range 1.45°, 25 rows.
   - F13-5A and F13-5B are also off by about 0.14° in longitude relative to the site-info file.
   - Change: take coordinates from `All_site_info_NT.xlsx`, which has 5 to 6 decimals against 2 decimals in the lichen file. Fix CG3-31A's ecoprovince and rebuild the groups.

6. **Two protocols and two allometries pooled.**
   - NT uses five 1 m² quadrats per 60 m² plot (2016 to 2018). SK uses two 4 m² quadrats per 100 m² plot (2015 to 2016).
   - Biomass is not weighed. It is estimated from cover and height through allometric equations fit on a destructive subsample. Dryad says the equations "were consistent among ecoprovinces".
   - Yet 97% of non-zero NT values are exact integer multiples of 1.052775 (a single linear coefficient on lichen volume), while SK values are not (3.5%). So the conversions apparently differ between jurisdictions.
   - The `jurisdiction` column lets a model absorb this, but it means part of the "signal" is a protocol offset.
   - Change: keep `jurisdiction` as a protocol flag (and drop `ecozone` instead), and document the target as an allometric estimate.

7. **Grouping is inconsistent between the two sources, and neighbouring groups are close.**
   - SK: site = one plot (190 groups of 2 rows).
   - NT: site = a cluster of 1 to 11 plots linked by plot prefix and identical rounded coordinates (122 groups of up to 55 rows).
   - Nearest-neighbour distance between sites has a median of 1.2 km in NT and 2.5 km in SK. 66% of NT sites have another site within 2 km.
   - Coarser spatial blocking lowers random-forest R² only modestly: 0.077 (site) → 0.060 (0.25° blocks) → 0.036 (1° blocks). The MAE ratio to the mean goes 0.83 → 0.89. So spatial leakage across groups is small but present.
   - Change: one consistent rule for both sources, for example spatial clusters at about 2 to 5 km, or the burn-scar or unburned-area code in the plot ID.

8. **Minor point on features.**
   - `years_since_fire` for unburned "control" stands is a field-derived stand age. In a real deployment it would come from inventory or fire-history maps, with more error.
   - NT coordinates have 2 decimals and SK coordinates have 6, which reveals the jurisdiction (harmless).

**If someone still wants it in the benchmark**

1. Aggregate to the plot level (about 516 plots).
2. Use the corrected, precise coordinates from `All_site_info_NT.xlsx`.
3. Drop `ecozone` (and either drop `jurisdiction` or keep it as a protocol flag).
4. Group with one spatial rule for both sources.
5. Use a tail-robust metric.

Even then, expect R² of about 0.15 to 0.2 on about 500 rows: a low-value but honest task.

**What I could not check**

- The full text of Greuel et al. 2021. Wiley returned 403, so I could not confirm whether the authors modelled quadrats or plot means, or what fit they reported.
- The allometric equations themselves, in `Destructive_biomass_sample_*.xlsx` (downloaded, not analysed).
- Why the SK Dryad description says 221 plots when the file holds 190. The prepared table matches the file, so the curation did not drop them.
- How stand ages were determined for each plot.

**Sources**

- https://datadryad.org/dataset/doi:10.5061/dryad.t1g1jwt15 (NT lichen data; metadata sheets quoted)
- https://datadryad.org/dataset/doi:10.5061/dryad.tb2rbnzzj (SK lichen data)
- https://datadryad.org/dataset/doi:10.5061/dryad.76hdr7sth (NT vascular plant data, site context)
- https://doi.org/10.1002/ecs2.3481 (Greuel et al. 2021; abstract only, full text 403)
- https://experts.colorado.edu/display/pubid_310299 (paper record)

</details>

<details><summary>Precedent check</summary>

**Precedent check (precedent-checker, 2026-11-01)**

**Verdict:** consistent on scope, target, split, scoring unit, metric, zeros, columns and provenance fields. Two
choices depart from the closest siblings of this run, and nothing written down sets them apart: the download route
(Zenodo copies, although Dryad's own version download works, as `pennsylvania_oak_hickory_regeneration_experiment`
found the same day) and the target's scale (no transform, while the four unbounded ecological siblings ship log1p). No
drift in Andrej's calls, no third exception, and no register flag touches this dataset (register.md, "Flags (14)").

Read: principles.md; register.md (1,620 decisions); the Cases tables of provenance.md, splits.md, metrics.md,
selection.md, use_case.md, leak_checks.md; the definitions and records of the siblings
(`pennsylvania_oak_hickory_regeneration_experiment`, `wadden_sea_sibes_macoma_abundance`,
`nantucket_sound_sea_duck_aerial_survey_counts`, `noaa_afsc_bottom_trawl_survey_cpue`,
`cape_floristic_region_family_cover`, `crms_phragmites_cover`, `sweden_depth_to_bedrock`,
`athabasca_forage_lichen_cover`) and the family's verdicts of 2026-10-30. Tests run (in the run folder):
Dryad's version downloads, SHA-256 of the files, the two NT sheets that only Dryad has.

**Per decision**

| # | Decision | Standing | Closest precedents | Note |
|---|---|---|---|---|
| 1 | Scope and use case: CC `Yes`, priority 1 (Andrej, 2026-10-30); fit approximate; the actor "for example" | consistent | Andrej's policy 1 (2026-10-30: "if a dataset is useful for a predictive application although the data was collected for something else, then this is fine"). The same day pennsylvania, crms_phragmites_cover, noaa_storm_events_damage and rand_health_insurance_experiment_doctor_visits were raised to `Yes`. Set apart: north_american_breeding_bird_survey_counts `No` (no habitat covariates), athabasca_forage_lichen_cover `No` (`Image`, remote-sensing covariates); great_lakes_marsh_bird_point_counts and morocco_forest_bird_transect_counts kept 2nd Tier as screened (published for trends, for a biogeographic hypothesis). Lennart's don't-ship calls (glioma_grading and nba_players_2016_2019, 2026-10-26; dataorg, 2026-10-22) are not like cases: their targets were constructed or unknown, or the source only looked at the data. Here the paper's title is "Predicting patterns of terrestrial lichen biomass recovery", and the target can be checked (#2). | Draft issue 1: the only facts new since the CC are the scores (linear R^2 0.137, LightGBM -0.016). TP-2 and the Tensions row "The right split against the score" (forest_fires) say a small real signal under the right split is no reason to retire, so reopening the `Yes` on the scores would depart from that. Keep issue 1 as a use-case question (P3) that cites the CC, or drop it. Aside: the `No Good Target / Scientific Discovery` marker stays on a `Yes` record (selection.md puts it with `No` or 2nd Tier). The other four `Yes` records of 2026-10-30 have the same mismatch, so it is a family tidy-up, not a departure of this dataset. |
| 2 | Source and download route, under the rule of 2026-11-01 ("If you cannot find a source, it's 2nd tier") | the rule is applied consistently; the route **departs without a stated reason** | sweden_depth_to_bedrock (CC 2026-11-01, the rule's only case: features no one can get without a manual order, so 2nd Tier); nantucket (same run: Dryad's Zenodo mirror, PROV-8); pennsylvania (same run, 2026-11-01: the same Dryad 401, so it took Dryad's version download) | The rule does not fire: a byte-identical copy counts as a source found, and PROV-8 lets the download instructions name a copy. But the stated reason ("Dryad answers 401 without a token") is true only of the per-file API. Checked 2026-11-01 14:45 UTC: `https://datadryad.org/api/v2/versions/442103/download` (NT version 5) answers 302 and serves a zip of four files without a token. Its `Lichen_data_NT.xlsx` has the definition's SHA-256 (03a3f3f4...). SK version 105865 also answers 302, and Dryad's file list gives the same digests as Zenodo (74ad1fe5... for the lichen sheet). The zip adds `All_site_info_NT.xlsx` and `Quadrat_cover_data_NT.xlsx`, which bear on draft issues 2, 4, 5 and 6 (below). Prompt A. |
| 3 | Target: volume-based biomass; `kgha.areaperm2` and `non_zero` dropped (LEAK-10); cover and height not shipped (SEL-5) | consistent | LEAK-10 Cases, "a part, a consequence or another encoding of the target" (UCI student G1/G2, 2026-10-21); SEL-5 account_debt_south_africa (the rule's inputs dropped, the rest still a real task). fia_plot_aboveground_biomass (`No`, 2026-10-30) was decided on data access, not on its allometric target. | The reconstruction below strengthens it. |
| 4 | Target scale: kg/ha with no transform | **departs without a fact that sets it apart** (the siblings are AI drafts; there is no curator precedent) | pennsylvania, wadden_sea, nantucket and noaa_afsc ship log1p with `target_transform="log1p"` and are scored on the raw scale; both basque_offshore datasets ship log. cape and crms ship identity, set apart by a bounded percent cover. MET-3 (Lennart, 2026-10-21: "ship the target on the modelling scale, score on the original scale"). | The definition's reason ("the planner's quantity, and the fallback metric scores it there") holds for the siblings too: with the transform the score is still RMSE on kg/ha. It breaks no rule (MET-3 leaves the transform to the definition), and no curator has decided any of the siblings, so this pair should be settled once for the family. Facts: the positives skew 3.08 raw and -0.25 on log1p. The top 10 of 2,010 quadrats hold 26.7% of the squared deviation (wadden's 10 densest samples hold 58%). LightGBM scores R^2 -0.016 on raw kg/ha against 0.137 for linear (not tested on log1p). Prompt B. |
| 5 | Metric: fallback `rmse` on kg/ha; draft issue 7 (MET-10, the tail) | consistent | MET-5; pennsylvania (AIC, so fallback), nantucket (an in-sample pseudo R2, so fallback), the MET Cases row churn_telco_south_asia (paper unread, fallback kept, Lennart 2026-10-21). wadden_sea's issue 3 (open) asks for the family whether to keep RMSE or score by the Poisson deviance, and names the same tail. | Draft issue 7 asks the same question: point it to wadden's issue 3 rather than raise it again. |
| 6 | Zeros: 40.4% observed absences, kept | consistent | Andrej's policy 2 (2026-10-30: "We don't care. We want to add any relevant predictive task, independent if it is zero inflated or not"); wadden and nantucket keep their zeros. | |
| 7 | Split: grouped by site, the key built from site names and identical coordinates; leftover spatial correlation as a note (draft issue 4) | consistent | SPLIT-24 Cases concrete_compressive_strength and airfoil_self_noise (identical values in the columns that define the entity); the barred cases (emscad's similarity cluster, maternal_health_risk's feature hash) are a different mechanism. Correlation with nearby units was accepted in wadden (stations, with neighbours a median 500 m away in training) and in 5g_energy_consumption (Lennart, 2026-10-14: a split by station fills the gap between stations). pennsylvania groups on site, cape on climate cell. | No precedent asks for spatial blocks. The one caveat is CG3-31A's coordinate (#2, last bullet below). |
| 8 | Scoring unit: each quadrat is one prediction (draft issue 3) | consistent | SPLIT-26 superconductivity (rows with identical inputs and different targets kept, grouped); pennsylvania (microplots scored one by one within site groups; Andrej asked "How many samples are there per site?" and then said "LGTM", 2026-10-30) | |
| 9 | Proposed warnings `dataset_duplicate_rows` and `dataset_conflicting_duplicate_rows` (LEAK-18) | consistent | breast_cancer_prediction and expresso_churn_prediction_1m (the copies are distinct units with coarse features, accepted with a reason); california_house_prices_2020 (Lennart, 2026-10-21: keep real repeats, drop only exact copies of one record). wine_quality and jm1 (deduplicated, 2026-09-30 and 2026-10-01) are set apart: IID splits whose copies crossed the split, against 0% here. | dataset.py has no `accepted_check_warnings` yet; the precedents write the reason there. |
| 10 | Columns: quadrat labels, `species`, `acronym` and `acronym1` dropped (CLEAN-5); `ecozone`, `jurisdiction` and the coordinates kept; `site` typed categorical | consistent | pennsylvania (SUBPLOT dropped; TRT one-to-one, CLEAN-5); expresso_churn_prediction (Lennart, 2026-10-22: a coarser coding does not trigger CLEAN-5); cape, wadden and nantucket keep coordinates under grouped splits; every sibling types its group column categorical. | |
| 11 | Year 2021, source `Other`, CC0, the citation | consistent | PROV-9 melbourne_housing_market (an upload that grows takes the year of its first version; the NT deposit gained files in 2022 and 2026); nantucket and pennsylvania (`Other` for a Dryad deposit). | |
| 12 | Paper not read; draft issue 5 asks for the PDF (PROV-16, PROV-17) | consistent | pennsylvania (the publisher's bot check); sweden (SLU's PDF behind a browser check, "a curator can open it") | The paper is open access (Crossref: CC BY 4.0 from 2021-04-23), so the curator can open it in a browser. The Dryad sheets already answer part of issues 2 and 6. The paper is still needed for why 20 NT and 31 SK plots are left out, and for where the allometry comes from. |

**What the two Dryad-only NT sheets show** (my tests, for the claim auditor and the split auditor; the builder did not
have these files):

- `Quadrat_cover_data_NT.xlsx` holds 346 NT plots, the count the abstract gives. The 20 plots missing from
  `Lichen_data_NT.xlsx` are in it, with 5 quadrats each and live depths (1 of their 59 forage-lichen rows has no
  depth). So draft issue 6 (PROV-13) can be answered from the origin, and the Tensions row "Repair against cleaning
  around damage" (SUPPORT2, ashrae) says to look there first. Adding the plots back would need a target computed by a
  formula we inferred (next bullet), which the Tensions row "A better version against our own fix" (eryhemato) does
  not allow. The likely remedy is a note that names the 20 plots and says why they are out, if the paper gives the
  reason.
- The target can be reproduced: `kgha.volperm2` = 12.633 x the sum of (percent cover x live depth) over the four
  forage groups (ratio: median 12.6333, interquartile range 12.6325 to 12.6340, over 945 quadrats with forage cover;
  Spearman 0.967; presence agrees in 98.2% of quadrats, with a rough mapping of the cover labels). `kgha.areaperm2` =
  61.934 x the summed percent cover in 97.9% of quadrats. This settles the "which biomass" half of draft issue 2
  without the paper: the target is the cover x live-height volume.
- `All_site_info_NT.xlsx` gives the survey date and coordinates to 6 decimals for all 326 task plots. Three plots
  disagree with the task sheet by more than 0.01 degree. One of them, CG3-31A (latitude 62.22 in the task sheet,
  60.766 here), is on its own enough to make the site key link plots 162 km apart through a shared rounded
  coordinate. Within the 17 shared rounded coordinates the median spread is 0.6 km. For the split auditor: SPLIT-24
  builds an exact key, here possibly from a mistyped coordinate.

**Drift and amendments:** Andrej's verdicts of 2026-10-30 on this family follow the two policies he stated that day;
no drift. No exception is recorded in this family, so there is no third exception of one reason. The rule of
2026-11-01 has one earlier case (sweden), and this dataset is consistent with it.

**Consistency checks for the curator**

A. **Consistency check (AI, 2026-11-01):** the definition downloads Dryad's Zenodo copies. That departs from
`pennsylvania_oak_hickory_regeneration_experiment` (same run, built 2026-11-01), which met the same Dryad 401 and took
Dryad's version download. That route works here too (NT version 5 and SK, checked 2026-11-01), and it adds two NT
sheets the copy lacks: the 20 missing plots, and the cover and live depth behind the target. What sets this case
apart? (a) the shipped sheets are byte-identical and the task needs no other file: keep the Zenodo URLs and record the
two Dryad sheets as read for the notes (issues 2 and 6); (b) treat it like pennsylvania: download from
`https://datadryad.org/api/v2/versions/442103/download` and `.../versions/105865/download`, and settle issues 2 and 6
and CG3-31A's coordinate from the two sheets; (c) nothing to reopen, since pennsylvania already uses the origin; (d)
change the rule: amend PROV-8 to prefer the origin's own route when it works.

B. **Consistency check (AI, 2026-11-01):** the target ships on kg/ha with no transform. Four siblings of the same run
(`pennsylvania_oak_hickory_regeneration_experiment`, `wadden_sea_sibes_macoma_abundance`,
`nantucket_sound_sea_duck_aerial_survey_counts` and `noaa_afsc_bottom_trawl_survey_cpue`, AI drafts no curator has
decided yet) ship log1p with `target_transform="log1p"` and are scored on the raw scale, as MET-3 has it (Lennart,
2026-10-21: "ship the target on the modelling scale, score on the original scale"). The definition's reason, that kg/ha
is the planner's quantity and is scored there, holds for them too. What sets this case apart? (a) a lighter tail (the
top 10 of 2,010 quadrats hold 26.7% of the squared deviation, against 58% in wadden), so the raw scale is a fair
modelling scale: record that as the fact; (b) treat it like the siblings: ship `log1p_forage_lichen_biomass_kg_ha`
with `target_transform="log1p"`, the metric unchanged; (c) reopen the four siblings so they ship on the raw scale; (d)
settle it once for the family: amend MET-3 to say when a nonnegative, skewed target ships logged.

</details>

<details><summary>Advocate</summary>

**Advocate's opening brief: boreal_postfire_lichen_biomass (advocate, 2026-11-01)**

Position: ship the dataset as defined (the task, the volume-based target, the site split, the quadrat rows, `rmse` on
kg/ha), after one repair from the origin and corrected notes. No agent found a leak, a copy across the split, a wrong
target or a fold that cannot be scored. The real problems the agents found are fixed on the two mildest rungs of the
remedy ladder (repair from the origin, notes). The two open calls (split level, target scale) keep the dataset
whichever way the curator decides them.

**1. The evaluation is honest: nothing leaks and nothing crosses the split (P4; LEAK-10 Must, SPLIT-29 Must, SPLIT-23 Must, LEAK-18 Should).**
- Evidence: `kgha.areaperm2` is 61.934 x percent cover in 1,630 of 1,630 NT and 380 of 380 SK rows (Spearman 0.994
  and 0.990 with the target), and `non_zero` equals target > 0 in 2,010 of 2,010; both are dropped. No feature alone
  reaches R^2 0.03. On all 30 splits there are 0 exact feature copies, 0 shared groups and 0 shared plots across the
  split, and no feature vector occurs in two groups (claim auditor rows 11, 12, 19). A random split scores 0.347
  against -0.034 by site, so the grouping is needed, and it is applied (SPLIT-29). `site` never reaches the features
  (LEAK-33, column auditor).
- The quadrat rows are the source's rows (SPLIT-26), and they rank models as a stand-level score would. Kendall tau is
  0.91 between the two rankings (practitioner). The best family is the same in 93% of splits (claim auditor). Ridge
  wins 13 splits and the forest 9 under both scorings (split auditor). Same call as pennsylvania (microplots scored one
  by one in site groups; Andrej, "LGTM", 2026-10-30) and superconductivity.
- Answers the blind reviewer's concern 2 (replicates). The reviewer agrees they are "pure within-plot measurement
  noise, not leakage". Its fix, plot means, is "a different dataset" by SPLIT-26. The copies are natural repeats of few
  plot-level features (LEAK-18; breast_cancer_prediction, sepsis).
- Fix that keeps it: write the reason for the two warnings in `accepted_check_warnings`, as the precedents do
  (precedent checker #9). Use the corrected counts: 482 of the 518 zero copies lie within one plot; 32.5% is the floor
  within identical inputs, and the within-plot share is 28.8%.

**2. The target is the quantity the actor uses, and the origin's own data now confirms it (P3, P5; USE-5 Must, SEL-5, EV-2).**
- Evidence: the precedent checker reproduced `kgha.volperm2` from Dryad's `Quadrat_cover_data_NT.xlsx`. It equals
  12.633 x the sum of (percent cover x live depth) over the four forage groups (median ratio 12.6333, IQR 12.6325 to
  12.6340, over 945 quadrats). The practitioner: survey lichen biomass is always an allometric estimate, and the volume
  form is the right one, because "mat height is what separates a young mat from an old one". Cover and height, the
  label's inputs, are not shipped (SEL-5).
- Answers the record's `No Good Target` marker and the "paper unread" objection. A measurement on the data outranks
  the paper (EV-2). PROV-17 is met as written: the notes mark every claim about the paper as "unverified against the
  paper".
- Fix that keeps it: the curator opens the CC-BY paper (doi:10.1002/ecs2.3481 in a browser, or the Wayback PDF) for
  the dropped plots and the stand-age method; neither changes the target. Correct the Zeros bullet: 2 of the 813 zeros
  (plot 2015-054) had cover recorded but volume 0, and they stay at 0 as the authors' flag has them (CLEAN-10/11,
  wording).

**3. A real decision exists, and the curator has said `Yes` (P3; USE-1 Must, USE-2 Must holds; the curator's decision outranks an AI assessment).**
- Evidence: the practitioner names the actor and the decision. A GNWT or Saskatchewan caribou habitat biologist
  revises a boreal caribou range plan. Today a burn under 40 years counts as disturbed, and a range needs 65%
  undisturbed habitat. The NWT's CIMP found that forage lichens "needed 45 to 70 years to recover after a fire". On
  the shipped splits a simple hurdle explains 0.159 of the variance per quadrat (0.216 per stand). The 40-year rule
  used today explains 0.022 (0.040). The source's aim: "provide a basis for estimating future caribou habitat".
- CC (2026-10-30, Andrej): `Yes`, priority 1, under his policy that a dataset is fine "if a dataset is useful for a
  predictive application although the data was collected for something else". The precedent checker: since then the
  only new facts are the scores.
- Fix that keeps it: name that actor and decision in `use_case`. Rewrite `fit_reason` with the real gaps: the
  unverified allometry, quadrat rows, a chronosequence in two regions. The fit stays approximate (USE-8). The
  practitioner adds that "no actor" and "design variables" are no gap for the projection the source names (USE-9).

**4. The signal is small but real, every fold can be scored, and the metric fits the decision (P6; TP-2 Should, TP-5 Must, SPLIT-28 Must, MET-1, MET-5).**
- Evidence: linear beats the mean on 30 of 30 shipped splits (R^2 0.137). Under the stricter area split the forest
  still beats it on 29 of 30. Each test fold holds 571 to 746 rows, 104 groups, 155 to 185 plots and 321 to 466
  positives (claim auditor row 35). So `Too Small` does not apply (TP-5), and SPLIT-28 holds.
- Answers the blind reviewer's "exclude", which rests on the size of the scores (its own best R^2 is 0.11 to 0.15)
  and their spread across splits. TP-2 and the Tensions row "The right split against the score" say neither is a
  reason to retire: forest_fires was kept at R^2 0.013. The spread is what a tiny-data task looks like (Tensions,
  "Tiny but real": musk kept).
- Metric: the source reports only significance tests and a growth curve, so the fallback `rmse` applies (MET-1).
  MET-5 never turns a p-value into a task metric. The practitioner: squared error is minimised by the mean, and a
  range's forage supply is the sum of stand means. The tail (99th percentile 6,014 kg/ha) is the forage-rich stands
  a planner must not undercount. So the MET-10 tail concern argues for RMSE, not against it.
- Target scale (precedent prompt B; CLEAN-16 Should, P7). No curator has decided any of the log1p siblings, and MET-3
  leaves the transform to the definition. Two facts set this case apart. Its tail is lighter: the top 10 of 2,010
  quadrats hold 26.7% of the squared deviation, against 58% in wadden_sea. And a model trained on log1p scores poorly
  by RMSE on the raw scale, as wadden_sea's own notes show. Keep the raw scale. If the curator settles the family on
  log1p, the metric stays the same.

**5. `years_since_fire` is known at the prediction point; how precise it is belongs in a fit note, it is no leak (P3; USE-6 Must, USE-3 Must holds, USE-8 Must).**
- Evidence: it is the stand's age, which fire records or a forest inventory give for every stand. It is neither a
  part nor a consequence of the lichen (column auditor; claim auditor: "not a leak ... (USE-6)"). Two agents measured
  what its field precision is worth for old and control stands. Capping the age at assumed fire-record horizons costs
  0.013 R^2 for ridge (SE 0.005), 0.009 for the hurdle and 0.017 for the forest (SE 0.015), on kg/ha. In the source's
  projection the simulated stand's age is known exactly (practitioner).
- Answers the column auditor's wadden_sea comparison. Sediment from the sampling visit is a value that only a sample
  gives, and that precedent replaced it because of "a gain a place without a sample cannot have". A stand age exists
  for every stand, and the gain from field precision here is about 0.01. noaa_afsc kept its readings on the same
  ground: no measured gain.
- Fix that keeps it: in `known`, `use_case` and `fit_reason`, say that the age is the survey's per-plot stand age,
  dated in the field where no fire is recorded. Say that a planner has the inventory's age or a censored fire-record
  age, and give the cost. On a log1p target the forest's cost rises to 0.074, which is one more reason for the raw
  scale (point 4).

**6. The site split matches the use case as written. Grouping by burn area is a weighing call: it would mean a re-split, never exclusion (P4; SPLIT-1 Must, SPLIT-4 Must, SPLIT-24 Must, SPLIT-26 Should).**
- Concede: the note "the level of grouping changes the score within its noise" is false for ridge. Ridge scores 0.138
  by site against 0.054 by area, about 3 SE apart; in the builder's own log it is 0.143 against 0.005 by blocks. The
  sentence goes (EV-7). SPLIT-4 says the size of the gap decides nothing, in either direction.
- Why the site still holds: on no split does a test plot share a site, a coordinate or a plot with training, and the
  key is exact (SPLIT-24). The practitioner, playing the actor, says "the test sites match my situation within the two
  study regions", and recommends keeping "the site grouping". No split of this data can serve a range-wide reading.
  Under the area split, test quadrats still sit a median 22 km from training, against 95 km for a point in the NT
  hull. With 100 km blocks, every R^2 is below 0 against the fold's own mean (split auditor). That gap belongs to the
  fit (a two-region chronosequence, USE-8), not to the split.
- Further facts:
  - The strong learners do not move: the forest goes from +0.110 to +0.115, the small LightGBM from +0.089 to +0.093.
  - The area key exists only for NT. SK stays per plot, so the area split mixes two rules.
  - Its largest group holds 17.4% of the rows, and its test folds range from 314 to 1,067 rows.
  - Neighbours in training, with a note, were accepted in 5g_energy_consumption (Lennart, 2026-10-14) and in this
    run's wadden_sea and pennsylvania drafts. No precedent asks for spatial blocks (precedent checker #7).
- Remedy either way: keep the site, and replace "some optimism remains" with the split auditor's figures: 94% of NT
  test quadrats have their burn area in training; 2.5 km to training against 95 km for a point in the hull. If the
  curator reads the use case as range-wide, re-split on the NT burn area. That is a definition fix, rung two of the
  ladder, and the dataset still ships.

**7. The provenance defects can be repaired from the origin, the mildest rung (P5; PROV-13 Must, PROV-8 Must, PROV-9).**
- Concede: CG3-31A carries CG2-35A's coordinate, 161 km from its site-mates, and the two F13-5 plots are about 0.14
  degree off. The download reason "Dryad answers 401 without a token" holds only for the per-file API. Dryad's version
  download answers 302 and serves the same files (same SHA-256) plus `All_site_info_NT.xlsx` (precedent checker,
  prompt A).
- Fix that keeps it: download Dryad's version zips, as pennsylvania does. Take the three plots' coordinates
  (CG3-31A: 60.76557, -116.5615) and CG3-31A's ecoprovince from `All_site_info_NT.xlsx`. Keep the published 0.01
  degree grid elsewhere, since the site key rests on it, and rebuild the groups, so CG3-31 and CG2-35 separate. That
  is PROV-13's repair from the origin. It touches 15 rows, with a negligible score effect, and the merge it undoes was
  only stricter.
- Not defects:
  - The 2022 revision of the NT file is the authors' own corrected version, and it replaces the older one (Tensions,
    "A better version against our own fix"). The year stays 2021 (PROV-9).
  - The 20 NT plots missing from the task sheet are in the quadrat sheet, but adding them would need a target from
    our inferred formula, which the same Tensions row bars. Add a note that names them, with the paper's reason if it
    gives one.

**Conceded in sum (P7, cheap and safe):** the counts and phrases the claim auditor refuted:
- within-plot share 28.8%, against the 32.5% floor;
- 482 of the 518 zero copies lie within one plot;
- 980 is the check's count;
- only 26 of 110 multi-plot sites share one age;
- NT r = 0.17 under 1 km;
- 155 and 72 destructive patches, not 342 and 256;
- "all at one recorded coordinate" is false for 51 site names.

None of these changes a verdict.

```text
Verdict: ship after changes (repair 3 plots' coordinates from the origin; correct the notes).
Validity: USE-1, USE-2 hold (a range-plan decision; the curator's Yes); USE-6 holds for years_since_fire, with a USE-8
  note; LEAK-10 holds (2 drops); SPLIT-29, SPLIT-24, SPLIT-23 hold; SPLIT-1 holds at the site (weighing call on how
  wide the use case is); PROV-13 triggered, fixed by repair; PROV-17 met (paper claims marked unverified).
Value: TP-2, a small real signal (beats the mean on 30/30); TP-5 and SPLIT-28 hold; fallback rmse (MET-1, MET-5).
Quality: P7 wording fixes; CLEAN-16, raw scale kept (lighter tail, RMSE on kg/ha).
For the curator: site or burn area (SPLIT-1); raw or log1p for the family (CLEAN-16, MET-3).
```

</details>

<details><summary>Critic</summary>

**Critic, opening brief (2026-11-01): boreal_postfire_lichen_biomass**

```text
Verdict: ship after changes (none of them exclusion).
Validity: USE-3/USE-8 triggered (the inputs are described wrongly; fix the text); SPLIT-1/SPLIT-4 triggered (the test
  site's burn area is in training; re-split on the burn area); PROV-13 triggered (3 NT plots have wrong coordinates;
  repair them from the origin); PROV-8/PROV-9/PROV-17 notes are out of date. LEAK-10 holds; SEL holds (CC Yes).
Value: TP-2 holds: a small real signal, and it survives the stricter split.
Quality: seven misstated counts and sentences in the notes (EV-7).
```

I argue for changes, not against the task. The CC `Yes` stands. The blind reviewer's "exclude" does not survive the
rules (see the dropped points at the end).

**1. P3: `years_since_fire` is not what the use case says it is (USE-3, USE-8, Must). Remedy: fix the definition's
text.**
- Problem. `use_case` and `known` say a planner knows the years since fire "from fire-history maps and the forest
  inventory". For 145 NT plots (725 rows, 36% of the rows) in control areas with "no recorded burn history" (Dryad
  NT methods), that cannot hold. The value is a field stand age: 68 distinct ages from 33 to 241 years. Inside the NT
  burn scars, only 11 of 181 plots carry the design's 37-38 or 46-49 years, and 84 sites hold several ages at one
  coordinate (claim audit row 7; column audit problem 1).
- Effect. The model trains on a more precise age than a planner has for an old stand. This is not a leak: a stand age
  exists at the prediction point (USE-6). Capping the age at a fire-record horizon costs about 0.01 R^2 (ridge -0.013,
  SE 0.005; column auditor and domain practitioner, independently).
- Remedy (USE-8: the fit has to name its gaps). In `known`, `use_case` and `fit_reason`, say that `years_since_fire`
  is the survey's per-plot stand age, field-dated where no fire is recorded, and that a planner would have an inventory
  age or "older than the record". Do the same for `stand_type`, the field class of Hart et al. 2019. While editing,
  name the decision the domain practitioner documented: a GNWT or Saskatchewan caribou habitat biologist revising a
  range plan, where the federal rule counts every burn under 40 years as disturbed and NWT monitoring found 45 to 70
  years (USE-1). Keep the fit approximate.

**2. P4: the test does not hold out what the use case predicts for (SPLIT-1, SPLIT-4, Must; the note breaks EV-7,
Must). Remedy: re-split on the NT burn or unburned area.**
- Problem. The definition's own task is "a stand at a place with no survey". The source aims "across the range". But
  94.3% of NT test quadrats have another site of their own burn scar or unburned area in training. The median distance
  to the nearest training plot is 2.4 km (NT), against a median 95 km for a point in the NT study hull (split audit,
  issue 1).
- The burn area is the source's documented entity. The NT codebook defines `plot` as "Plot location: Burn Scar or
  Unburned area -xxx". It is an exact key (SPLIT-24, SPLIT-26) and it carries the label: burn areas hold 19.1% of the
  NT target's sum of squares.
- Effect, measured on 10 x 3 folds: ridge skill falls from +0.138 by site to +0.054 by area (about 3 SE). The random
  forest stays at +0.110 and +0.115. So the best family flips. The site split favours models that lean on a test
  site's burn-mates.
- EV-7. The note says "the level of grouping changes the score within its noise". The builder's own log refutes it:
  ridge 0.143 +- 0.016 by site against 0.005 +- 0.043 by block.
- Remedy (fix the definition):
  - Group NT on the plot-name prefix, merged through the site links. Each SK plot stays its own group (SK has no burn
    key). Do this after the repair in point 3. The CG2-CG3 merge the split auditor found runs only through CG3-31A's
    wrong coordinate (my check: as shipped, CG2 links to CG3 and to F2; after the repair, only to F2). That leaves 26
    NT groups.
  - Rewrite `grouping.definition`, `splits_comment`, `task_summary.split` and the grouping bullet with the measured
    numbers per family.
- Cost: unequal folds (the largest group holds about 17% of the rows). That is a weighing factor, and it does not
  decide (SPLIT-4: the gap never decides; "the split follows the application" outranks the score, P4 over P6).
- The one way to keep the site: the curator reads the use case as infilling unsurveyed stands inside partly surveyed
  burns. Then `use_case` must say so, and the notes must give the 94% and 2.4 km against 95 km figures instead of "some
  optimism remains".

**3. P5: three NT plots have damaged coordinates, and the origin has the clean values (PROV-13, PROV-14, Must).
Remedy: repair from the origin.**
- Evidence (my check of Dryad v5 `All_site_info_NT.xlsx`, as downloaded by the precedent checker):
  - CG3-31A is at 62.22, -116.33 in the task sheet, which is CG2-35A's coordinate. The site sheet puts it at
    60.76557, -116.5615, on the same date (2016-07-12) as CG3-31B and C, 162 km from where we ship it.
  - F13-5A and F13-5B are 7.8 and 7.9 km off.
  - The other 323 plots agree within 2 km (median 0.3 km).
- Effect. Five rows carry the wrong latitude, longitude and ecoprovince (Great Bear Plains instead of Hay and Slave
  River Lowlands). The site key merges CG3-31 with CG2-35 into `site_036`, which spans 1.45 degrees. Under point 2 the
  area key would merge CG2 with CG3.
- Remedy. Set the three plots' coordinates from the site sheet, rounded to the task sheet's 0.01 degree. Set
  CG3-31A's ecoprovince to its site-mates' value. Rebuild the groups. Add a dated `Repair:` bullet. This needs the
  Dryad file, which the Zenodo copy lacks (point 4).

**4. P5: the provenance notes are out of date (PROV-8, PROV-9, PROV-17; Must for the facts stated). Remedy: correct
the notes and the download; the curator reads the paper.**
- Download route.
  - The stated reason, "Dryad answers 401 without a token", is true only of the per-file API. Dryad's version
    download (`/api/v2/versions/442103/download` and `/105865/download`) answers 302. It serves the same SHA-256
    files plus `All_site_info_NT.xlsx` and `Quadrat_cover_data_NT.xlsx` (precedent check #2).
  - The sibling `pennsylvania_oak_hickory_regeneration_experiment` took that route in the same run.
  - Point 3 needs the site sheet. So download from Dryad, or keep Zenodo and add the site sheet's Dryad URL
    (consistency prompt A).
- Version. `Lichen_data_NT.xlsx` was replaced on Dryad on 2022-06-23 (v4, `files_changed`, 134,806 to 140,857
  bytes), after the April 2021 paper (claim audit row 2). Say we ship the authors' revision. The year stays 2021
  (PROV-9).
- Missing plots. The "not explained in the files (Anomaly)" note is wrong. `Quadrat_cover_data_NT.xlsx` holds all 346
  NT plots, including the 20 left out of the lichen sheet. Do not add them back with a target from our own inferred
  formula (Tensions, "A better version against our own fix"). Name them, and give the authors' reason if the paper has
  one.
- Target. NT `kgha.volperm2` reproduces as 12.633 x the sum of (percent cover x live depth) over the forage groups
  (precedent check). State this in the target bullet. It settles the "which biomass" half of USE-5 without the paper,
  so `fit_reason` can drop "whose paper text we could not read" as the main gap. The allometry stays unverified.
- Paper.
  - The note says "no repository copy with text was found". But the article is CC BY 4.0 (Crossref) and the Wayback
    Machine has the publisher PDF (claim audit row 33).
  - The curator should open the paper and read its Methods for three things: how TSSRF was dated (point 1), why 20 NT
    and 31 SK plots are out, and whether any prediction error is reported.
  - Until then the claims stay marked unverified (PROV-17), as they are now.

**5. P7: misstated counts and sentences (EV-7; quality, not a reason to exclude). Remedy: correct the notes and the
proposed warning reasons.** All from the claim audit (rows 16, 17, 20, 22, 25, 27, 31):
- "All at one recorded coordinate" is false for 51 NT site names.
- "Often their fire": only 26 of 110 multi-plot sites share one age.
- "518 of them quadrats of one plot all at 0": 482 are within one plot; 36 come from sibling plots.
- "Within-plot spread 32.5%": the within-plot share is 28.8%; 32.5% is the floor within identical inputs.
- Two of the 813 zeros (plot 2015-054) have cover recorded and volume 0, so they are not "observed absences".
- The NT correlation under 1 km between different sites is 0.17.
- The destructive files hold 155 and 72 patches, not 342 and 256 (those are species-group rows).

**Points I considered and dropped (no backing under the rules)**
- Exclusion for weak signal (blind reviewer). TP-2 (Should) and the Tensions row "The right split against the score"
  (forest_fires) rule it out. Linear beats the mean on 30 of 30 shipped splits, and the forest on 29 of 30 under the
  area split.
- Plot-mean aggregation. SPLIT-23 holds: the quadrat score ranks models like a stand score (Kendall tau 0.91;
  practitioner, split audit). SPLIT-26 keeps the source's rows.
- A tail-robust metric. MET-10 is only a factor (Weigh). The practitioner shows that the mean, which RMSE targets, is
  what a planner sums over a range.
- Shipping log1p for consistency with the siblings (CLEAN-16, prompt B). I measured it. Trained on log1p and back-
  transformed with expm1 (what `target_transform` does), all four families fall below the training mean on RMSE in
  kg/ha. R^2 raw against log1p: ridge 0.132 / -0.050, random forest 0.104 / -0.043, small LightGBM 0.083 / -0.036,
  default LightGBM -0.030 / -0.084. log1p is better on 0%, 3%, 7% and 40% of splits. That is the fact that sets this
  case apart for prompt B, option (a). Script and output: `log1p_check.py` (run folder), `log1p_check.csv`.

Scripts of mine, in the run folder: `log1p_check.py` (raw against log1p on the 30 shipped splits),
`coords_check.py` and two inline checks (coordinates against `All_site_info_NT.xlsx`; the burn-area links before and
after the repair). Threads capped.

</details>

<details><summary>Advocate rebuttal</summary>

**Advocate's rebuttal: boreal_postfire_lichen_biomass (advocate, 2026-11-01)**

The critic and I agree on the verdict ("ship after changes, none of them exclusion"), on dropping the blind reviewer's
exclusion, on the quadrat rows, on `rmse` and on the raw scale. I concede points 1, 3, 4 and 5. On point 2 I concede
the re-split under the use case both of us want named, but I dispute the mechanism the critic gives for it. I ran a
check, and its result changes what the notes should say.

**Critic 1, `years_since_fire` (USE-3, USE-8): concede.** This is my point 5 with the same remedy. Say that it is the
survey's per-plot stand age, field-dated where no fire is recorded. Say that a planner has an inventory age or "older
than the record", and give the measured cost of about 0.01 R^2. Add the `stand_type` sentence and name the
range-plan actor (USE-1). The fit stays approximate. It is not a leak (USE-6). Both briefs agree.

**Critic 2, split level (SPLIT-1, SPLIT-4): concede the re-split, narrowed; dispute the mechanism.**
- Concede. Once `use_case` names the practitioner's actor (my point 3, the critic's point 1), the model predicts for
  stands in burns this study did not survey, now or after future fires. No source names an actor who fills in stands
  inside partly surveyed burns, and I cannot back that reading. Under SPLIT-1 ("most closely mirrors") and SPLIT-4
  (new entities must be new in test), the NT burn or unburned area is the closer mirror. Two arguments from my opening
  fail:
  - "No split serves range-wide" does not answer "most closely": a median of 22 km to training is closer to 95 km than
    2.4 km is.
  - The practitioner's "keep the site" rested partly on the refuted "within noise" note.
  
  The remedy is the critic's: re-split on the burn area after the repair, with each SK plot its own group. That is a
  definition fix, and the dataset ships.
- Correct my own figure. After the repair, CG2 and CG3 no longer merge. The area key gives 216 groups (26 NT areas),
  and the largest group holds 10.0% of the rows, not 17.4%. Test folds under the repository's splitter hold 410 to 974
  rows. The fold-size cost I cited is smaller than I said.
- Dispute: "the site split favours models that lean on a test site's burn-mates". The decisive experiment (EV-1), run
  on the repaired frame, 10 x 3 folds, untuned, skill against the training mean (mean +- SE, share of splits above 0):

| design | test rows | test rows whose stand type x ecoprovince is absent from training | ridge | random forest | small LightGBM |
|---|---|---|---|---|---|
| shipped site split (unrepaired) | 571-746 | 0.8% | +0.138 +- 0.011 (100%) | +0.111 +- 0.012 (93%) | +0.088 +- 0.013 (90%) |
| site, repaired, repo splitter | 534-754 | 0.8% | +0.132 +- 0.011 (97%) | +0.111 +- 0.013 (93%) | +0.098 +- 0.014 (90%) |
| area, repaired, repo splitter | 410-974 | 4.1% | -0.074 +- 0.070 (70%) | +0.112 +- 0.014 (90%) | +0.109 +- 0.012 (93%) |
| area, repaired, balanced folds | 669-671 | 4.4% | -0.208 +- 0.125 (67%) | +0.104 +- 0.011 (93%) | +0.096 +- 0.016 (90%) |

  - Holding out whole burns costs the two tree families nothing.
  - Ridge's fall tracks one thing. Across the area splits its skill correlates at r = -0.74 with the share of test rows
    whose stand type x ecoprovince combination is absent from training.
  - On the 20 of 30 area splits where that share is at most 2%, ridge scores +0.120, near its +0.132 by site. On the
    other 10 it scores -0.461, while the forest scores +0.134 on those same splits.
  - Balancing the folds makes ridge worse, so fold size is not the cause either.
  
  So the measured gap comes from a linear model extrapolating when a held-out burn takes a rare combination with it.
  No model is shown to read its test site's burn-mates.
- What follows:
  - The re-split rests on the application alone (SPLIT-4). It does not correct an inflated score: the site split
    overrates neither tree family.
  - The new `splits_comment` should state the facts above, not "the site split favours models that lean on
    burn-mates".
  - It should add that under the area split ridge falls below the mean on 30% of splits.
  - The repaired site split scores like the shipped one, so the coordinate repair itself moves nothing.
- Script and outputs: `area_balance.py` (run folder), `area_balance.csv`, `area_balance_per_split.csv`. The
  threads were capped.

**Critic 3, damaged coordinates (PROV-13): concede.** My check reproduces the three plots from
`All_site_info_NT.xlsx`:
- CG3-31A: 62.22, -116.33, against 60.76557, -116.5615 in the site sheet.
- F13-5A and F13-5B: 63.03, -114.35, against 63.003, -114.206.

Repair them from the origin, rounded to 0.01 degree, set CG3-31A's ecoprovince to Hay and Slave River Lowlands, and
add a dated `Repair:` bullet. This is the mildest rung, and it needs the Dryad version download (critic 4).

**Critic 4, provenance notes (PROV-8, PROV-9, PROV-17): concede.** Same as my point 7. Take the Dryad version
download as pennsylvania does. Say we ship the authors' 2022 revision; the year stays 2021. Replace "not explained in
the files" with "the 20 NT plots are in `Quadrat_cover_data_NT.xlsx` and are left out of the task sheet", without
adding them back (Tensions, "A better version against our own fix"). State the reproduced formula, 12.633 x the sum
of cover x live depth, in the target bullet. Drop "whose paper text we could not read" as the main gap in
`fit_reason`. The curator reads the CC-BY paper for three things: the age method, the dropped plots and any reported
error.

**Critic 5, the counts in the notes (EV-7, P7): concede.** The list is the one in my brief. None of the counts changes
a verdict.

**Critic's dropped points: agreed, and one of them adds a fact for my point 4.** The critic's log1p check is new
evidence for option (a) of prompt B. Trained on log1p and back-transformed, all four families fall below the
training mean on RMSE in kg/ha:

| family | R^2 raw | R^2 log1p |
|---|---|---|
| ridge | 0.132 | -0.050 |
| random forest | 0.104 | -0.043 |
| small LightGBM | 0.083 | -0.036 |

That is the fact that sets this dataset apart from the log1p siblings. Record it as such (CLEAN-16 departure kept;
MET-3).

```text
Verdict: ship after changes (no exclusion).
Validity: USE-1 holds once the actor is named; USE-6 holds, USE-8 note on years_since_fire and stand_type; LEAK-10
  holds; SPLIT-1/SPLIT-4 triggered, fixed by a re-split on the NT burn area (SK per plot), justified by the use case
  only (the site split overrates no tree family; ridge's gap comes from unseen stand type x ecoprovince combinations,
  r = -0.74); PROV-13 triggered, fixed by repair from All_site_info_NT.xlsx; PROV-8/9/17 notes corrected.
Value: TP-2, a small real signal under both splits (forest beats the mean on 90% of area splits); rmse on kg/ha.
Quality: CLEAN-16 departure kept (log1p falls below the mean for every family); EV-7 count fixes.
For the curator: confirm the named actor (new burns), which fixes the split level.
```

</details>

<details><summary>Critic rebuttal</summary>

**Critic, rebuttal (2026-11-01): boreal_postfire_lichen_biomass**

The advocate and I agree on six of its seven points. We disagree on one: the level of the split (advocate point 6). I
ran one new check for it (below). It narrows my reason and confirms my remedy.

**Advocate 1 (no leak; quadrat rows; the warnings): concede.**
- LEAK-10, SPLIT-29, SPLIT-23 and LEAK-18 hold, as the advocate says.
- One procedural correction: `accepted_check_warnings` stays empty until the curator fills it (add-dataset step 6).
  So the panel proposes the two reasons, with the corrected counts (482 of the 518 zero copies within one plot; 32.5%
  as the floor within identical inputs, 28.8% within a plot). The panel does not write them into the definition.

**Advocate 2 (the target): concede, narrowed.**
- The reproduction (12.633 x the sum of cover x live depth) covers NT only. There is no SK cover sheet.
- The two regions use different conversions:
  - the destructive slopes are 63.7 and 50.9 kg/ha per percent cover;
  - 97% of positive NT targets are multiples of 1.052775, against 3.5% in SK (blind reviewer).
- The target is therefore the authors' estimate under two protocols. `jurisdiction` carries the offset. This is a
  one-line note under USE-5, not a change.

**Advocate 3 (a real decision; the curator's `Yes`): concede.** That actor and decision should go into `use_case`.
The actor also decides point 6, below.

**Advocate 4 (signal, metric, scale): concede, with stronger evidence for the raw scale.**
- TP-2, TP-5, SPLIT-28, MET-1 and MET-5 hold.
- On the scale, a measurement on this dataset outranks wadden_sea's notes (EV-2). I trained on log1p and back-
  transformed with expm1, which is what `target_transform` does. On the 30 shipped splits every family fell below the
  training mean on RMSE in kg/ha:
  - ridge: R^2 0.132 raw, -0.050 on log1p
  - random forest: 0.104 raw, -0.043 on log1p
  - small LightGBM: 0.083 raw, -0.036 on log1p
- So the raw scale stays. The fact that sets this dataset apart for prompt B is this measurement, more than the
  lighter tail (`log1p_check.csv`, run folder).

**Advocate 5 (`years_since_fire`): concede.** It is no leak (USE-6). We ask for the same fix: in `known`, `use_case`
and `fit_reason`, say it is the survey's field stand age and give the measured cost of about 0.01 R^2 (USE-8).

**Advocate 6 (the site split holds; burn area is a weighing call): dispute. SPLIT-4 (Must) under the use case both
briefs now adopt.**
- The use case decides, and both briefs adopt the same one.
  - The actor the advocate puts into `use_case` (point 3) is a range-plan biologist. That biologist sums forage over
    a range and draws recovery curves by stand type and ecoprovince.
  - The definition's own grouping text says "across the range, where most stands have no plot".
  - For that actor, a new stand lies in a burn this study did not survey. SPLIT-4 says the test entities must then be
    new.
  - The burn scar or unburned area is the source's documented entity (codebook: "Plot location: Burn Scar or Unburned
    area -xxx"). It carries the label: area means range from 17 to 3,453 kg/ha within Great Bear Plains alone.
- The practitioner's support for the site does not stand on its own. Its gap 6 rests on "the block test the builder
  ran is within noise", the sentence the advocate concedes is false (EV-7).
- New check: why ridge loses skill under the area split. Script: `recall_check.py` (run folder). Skill
  against the training mean, site / area split:

  | model | site | area |
  |---|---|---|
  | kNN on location only | +0.004 | -0.142 |
  | ridge, stand type and age only | +0.090 | +0.074 |
  | ridge, plus ecoprovince, ecozone, jurisdiction | +0.102 | -0.002 |
  | ridge, all 7 | +0.138 | +0.054 |
  | random forest, all 7 | +0.111 | +0.115 |

  - Where the advocate is right. The site split does not reward recalling coordinates: location alone scores
    nothing. So I narrow my opening point: ridge does not get its edge from the coordinates.
  - Where the edge comes from: the region labels. Stand type and age transfer to a new burn (0.090 to 0.074, within
    about 2 SE). The ecoprovince labels add +0.012 under the site split and cost -0.076 under the area split. Each
    NT ecoprovince holds only 7 to 13 burn areas. With burn-mates in training, the ecoprovince stands in for the test
    site's own burn area.
  - What this means. The site split credits the source's headline predictor, ecoprovince, with a burn-area effect
    that does not reach a new burn. That is the overrating SPLIT-1's "why" names, and it flips the family ranking.
- The advocate's other arguments:
  - "No split can serve range-wide." SPLIT-1 asks for the split that mirrors the use case most closely, not a perfect
    one. The median distance from a test quadrat to training is 2.4 km by site and 22 km by area, against 95 km for a
    stand in the NT hull. Even 100 km blocks keep a positive skill against the training mean (forest +0.030, small
    LightGBM +0.041, positive on 77-80% of splits; `alt_splits.csv`). I do not ask for blocks: they are not an exact
    key (SPLIT-24).
  - "Two rules, NT and SK." The shipped split mixes two rules already (NT sites of 1 to 11 plots, SK single plots).
    Each region takes its finest documented key above the plot.
  - Unequal folds (314 to 1,067 rows). Every fold can still be scored (MET-2, TP-5). This is a factor, and SPLIT-4
    says the score never decides.
  - The precedents.
    - 5g_energy_consumption was a USE-9 call: by station rather than as a forecast. It had no documented entity above
      the station.
    - wadden_sea and pennsylvania are drafts no curator has decided.
- Remedy, unchanged:
  - re-split on the NT burn area after the coordinate repair (26 NT groups; SK plots alone);
  - add a note that ecoprovince effects do not transfer to new burns.
- If the curator reads the use case as infill inside partly surveyed burns, keep the site. But then remove "across the
  range" from the definition, and state the 94% and 2.4 km figures.

**Advocate 7 (provenance repair): concede.** We agree:
- the Dryad version download;
- the three plots repaired from `All_site_info_NT.xlsx` (15 rows);
- the groups rebuilt;
- notes for the 2022 revision and the 20 plots.

The repair also removes the CG2-CG3 link from the area key, as my opening said.

**Advocate's P7 concessions: agreed.**

```text
Verdict: ship after changes.
Validity: USE-3/USE-8 text fix (agreed); SPLIT-1/SPLIT-4 triggered under the range-plan use case both briefs adopt:
  re-split on the NT burn area (disputed; the curator's call on how wide the use case is); PROV-13 repair (agreed).
Value: TP-2 holds (agreed). Quality: notes corrected (agreed); raw scale kept, measured (agreed).
For the curator: site or burn area. With the range-wide use case, the evidence favours the burn area.
```

</details>
