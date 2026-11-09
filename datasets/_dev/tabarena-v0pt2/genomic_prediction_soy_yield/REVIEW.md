# genomic_prediction_soy_yield

**Outcome:** added. The AI recommends shipping it: the review panel's changes are made, and three calls are left for
the curator. Grain yield in kg/ha of 5,146 soybean inbred lines of the SoyNAM population (39 families, each a cross of
IA3023 with one founder) from their genotype at 4,312 SNP markers, rebuilt from the SoyNAM project's own release (the
CRAN package SoyNAM, data of 2015) rather than Azodi et al.'s standardized cut; whole families held out (3 x 3 grouped
folds, 13 families per test fold); pooled Pearson r, Azodi's criterion. The panel found two faults, both now repaired
from files already downloaded: the line value ignored the field-block effects that the source's data paper (Diers et al.
2018) removes, and 70 lines carried the raw genotype row of another sample. The line value now takes its environment
and block effects from the check plots alone, and the 70 lines take their own sample's calls from the QA matrix. The other changes: a model may now see all lines of a test family when predicting (`context="all_rows"`), since a breeder genotypes and ranks a new cross together; the notes cite the data paper (Diers et al. 2018) and the population paper (Song et al. 2017), and name the 186 heterozygous lines, the 96 off-types, the merged entries, the maturity effect, the shared 2011-2013 seasons, the within-family r and the parent baseline; the record's year is 2015 with the CRAN link; the task, group and leak probes were re-run on the changed definition, and the issues quote their numbers.
Verdict: ship after changes (made).
Validity: SEL-1, SEL-2 hold; USE-1, USE-3 hold (fit direct); USE-5, TP-7 triggered, fixed (environment and block
effects from the check plots, Diers et al. 2018); LEAK-29/30 removed by the same change (no line's plots enter another
line's target); LEAK-10, LEAK-16 to LEAK-21, LEAK-33 hold; SPLIT-1, SPLIT-29 hold (grouped by family); SPLIT-23
triggered, fixed (`context="all_rows"`); SPLIT-26 departed with a fact (one row per line, issue 2); PROV-13 triggered,
fixed (70 genotype rows repaired, none dropped); PROV-9 holds (2015; the record now says so too).
Value: TP-2 holds (LightGBM beats the dummy on every probed split, pooled r 0.52); MET-5 pooled r kept; MET-2 measured
(pooled r orders ten models like the within-family r, Kendall tau 0.96); `groups_test_groups_few` proposed for
acceptance (issue 3).
Quality: CLEAN-1 notes (186 heterozygous lines, 96 off-types, merged entries, all kept as the source's QA kept them).
Weighed: source metric + (Azodi's one deliberate criterion), the score's family part - (a parent baseline beats every probe model on pooled r), fold noise - (seed SD 0.018; the shipped seed lowest of 41), lines per fold + (1,661 to 1,775); priority factors gap 0, use case +, source +, shape +, risk 0.
For the curator: issue 1 first as the only open dispute (the metric's unit, pooled r recommended; decided with uniform_soybean_tests_yield under one metric rule, an across-datasets item), issue 2 (the exception for one row per line), issue 3 (the fold design and
the check warning).

**Main points:** Three calls: keep Azodi's pooled r or score the ranking within each cross (issue 1, pooled r recommended; decided with uniform_soybean_tests_yield under one metric rule); confirm the exception for averaging a line's plots into one row (issue 2,
recommended); keep the default random assignment of families to folds and accept the few-groups warning (issue 3,
recommended; the shipped fold seed gives the lowest score of 41).

**Record judgment:** valid. The SoyNAM project's own release (CRAN package SoyNAM, written by the project's members,
with the data paper Diers et al. 2018 for the trials and Song et al. 2017 for the population and chip), with Azodi et
al. (2019) for the task and the metric. The record's year is now 2015 and its links name the CRAN package and Diers et
al. 2018. The priority moves from 3 to 4 (gap 0, use case +, source +, shape +, risk 0): the target the size check of 2026-11-08
called ours to compute now follows the data paper.

**Issues for Lennart:**

1. **Score the ranking across all test lines (Azodi's pooled r) or within each cross?**

   * **Problem:**
     - On held-out families about half of pooled r (the correlation over all test lines of a fold) is the ranking of the 13 test families, and a breeder knows much of that from the parents: each line predicted by its founder's own yield (grown in the same trials) scores 0.66 on average over the 9 test folds against 0.57 for ridge.
     - What genomics adds at this decision is the ranking within a cross, which the mean correlation within families scores (0.29 for ridge, 0.26 for LightGBM).
     - Azodi's paper chose pooled r deliberately, but on random lines, a split we replaced with held-out families.
   * **Background:**
     - 55% of the target's variance lies between families; the true family means alone would score pooled r 0.74.
     - Under the within-family score a model that only gets the families right scores 0, and the family-level parent baseline scores 0 by construction.
     - The parents' yields are no feature and should not ship: they come from the same 2011-2013 trials, which a model of a new cross would not have.
   * **Effect on the task:**
     - Pooled r ranks models by both parts; the within-family score ranks them by the within-cross part only.
     - The task gamer's exploit (rebuild the test families by clustering and shrink to the family means) gains +0.02 (ridge) and +0.06 (LightGBM) under pooled r (the panel's numbers, before the changes) and exactly 0 under the within-family score; since a model may now see all lines of a test family (`all_rows`), it is allowed use either way.
     - The within-family score is 3 to 5 times more stable across fold seeds (issue 3).
   * **Experiments:**
     - Ten models (ridge at five penalties, kNN 10 and 50, two LightGBM, a random forest) on the 9 shipped splits: pooled r and within-family r order them alike Kendall tau 0.96 on the means over the 9 splits, 0.78 per split on average (lowest 0.64); pooled r and the family-mean r agree at tau 0.82; on random folds as Azodi split, 0.78 (per split 0.76). So the order of models under pooled r follows the within-family accuracy at least as closely as on the source's own split.
     - Per fold, ridge: pooled r 0.38 to 0.66, within-family r 0.25 to 0.34; the parent baseline beats ridge's pooled r on all 9 folds.
     - On random folds pooled r rises to 0.76 while the within-family r barely moves (0.31 against 0.29): the random split's gain is the siblings' family means.
   * **Consistency:**
     - protein_model_quality_rf_pcp and huesken_sirna_efficacy replaced a pooled score that rewarded group means with `mean_group_pearsonr` from context[^met5]; there the source had no unique metric, here Azodi names one.
     - forest_fires and open_soil_spectral_library kept a paper's one deliberate criterion[^met5].
     - The metric rule proposed across datasets, decided once with uniform_soybean_tests_yield, scores within groups only when the pooled score orders models unlike the within-group score on the shipped splits[^amend]; it keeps pooled r here, so B would need that wording widened.
     - Decided together with uniform_soybean_tests_yield, the same breeder's question: on its held-out seasons RMSE orders models unlike the within-location-year correlation (tau 0.38), while here the pooled r and the within-family r agree (tau 0.78 per split on average, measured as uniform's 0.38; 0.96 on the means), which sets the two apart.
   * **Panel:**
     - Keep pooled r (the advocate, the builder): Azodi's one deliberate criterion; the use case ranks the lines of new crosses together and a breeder truncates across crosses; the parent baseline uses same-trial yields a model may not have.
     - Switch (the critic, the domain practitioner): the cross means come from the parents' records, so genomics adds the ranking within the cross ("I would pick models by `mean_group_pearsonr` on `family`", the practitioner).
     - The mediator measured that pooled r keeps its meaning on our split (the tau above), so no Must forces the switch; what remains is the use-case fact of which decision the score stands for[^met1].
   * **Unknown:** how leave-family-out studies on SoyNAM report accuracy (Xavier and Rainey 2019, G3, run that design on this population: https://pmc.ncbi.nlm.nih.gov/articles/PMC7003100/); a per-family correlation there would be source-side evidence for B.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Pooled r (implemented) | Pearson r over all test lines of a fold, as Azodi et al. scored it; the notes give the within-family r and the parent baseline | Azodi's one deliberate criterion, the field's standard; orders models like the within-family r here (tau 0.96); a breeder truncates across crosses too | about half of it rewards family ranks a breeder has from the parents; the parent baseline beats every probe model on it |
     | B | Within-family r from context | `mean_group_pearsonr` on `family`: the mean correlation within each test family; Azodi's pooled r named as the overruled original | scores what genomics adds at this decision; follows protein and huesken; 3 to 5 times more stable across fold seeds; family shrinkage gains nothing | overrules a deliberate source criterion, which the two precedents did not; the proposed metric rule does not cover it (the two scores order models alike here), so its wording must widen |

   * **Recommendation:** A, the default: the source's deliberate criterion, and it orders models like the within-family score on our split. The metric rule proposed across datasets, decided once with uniform_soybean_tests_yield (score within groups when the pooled score orders models unlike the within-group score on the shipped splits)[^amend], keeps pooled r here, since the two agree (tau 0.96); B only if you read the breeder's genomic decision as the ranking within each new cross whatever the model order, which that wording would not cover. **Decision:** A or B?

   **Notes for the AI:** on B, replace `metric` with `Metric.from_context("mean_group_pearsonr", reason=..., inputs={"group": "family"})`, the reason naming Azodi's pooled r as the overruled original (MET-11 context, amended 2026-11-03), the use case (the ranking within a new cross; the cross means come from the parents), tau 0.96 and the parent baseline 0.66 per fold; rewrite the Metric bullet of the notes; add the metrics.md Cases row; the amendment is the across-datasets item under "### Rules" in the working copy's REVIEW.md (the main session adds it; it is not there yet) (one wording for this dataset, protein_model_quality_rf_pcp, huesken_sirna_efficacy and uniform_soybean_tests_yield), which as worded would not cover B, so B needs that item's wording widened; re-run `dataset check` and the task probes. Issue 3's fold design then matters little; its warning still needs the mark. On A, a CC line in the record naming the reason (a deliberate source criterion that orders models like the within-family score on the shipped split) as what sets the task apart from protein and huesken, and the per-split tau (0.78 here, 0.38 in uniform_soybean_tests_yield) as what sets it apart from that sibling. Measurements: `m1_metric_meaning.py` and `final_numbers.py` of the run's `probes/final/`.

   [^met5]: **MET-5** (Should): a paper's metric is the source's metric only when it is one deliberate choice. Exceptions protein_model_quality_rf_pcp and huesken_sirna_efficacy (Lennart, 2026-11-04): context `mean_group_pearsonr`, "the use case ranks guides within a gene and pooled RMSE rewards a gene's mean", in place of the fallback. Kept deliberate criteria: forest_fires (MAD), open_soil_spectral_library (tuning RMSE).
   [^amend]: The proposed wording (an amendment of **MET-5** / **MET-11**), decided once as the across-datasets item under Rules together with uniform_soybean_tests_yield, issue 1 (open; tau 0.38 there): "when the use case ranks units within groups and the pooled score orders models unlike the within-group score on the shipped splits, score within the groups from context". principles.md: "When the same reason has produced three exceptions, the next pass proposes an amendment." **MET-11** (Must) `context`, amended 2026-11-03: also covers a source metric overruled under MET-2 or MET-4, the reason naming the overruled original.
   [^met1]: **MET-1** (Must): the declared metric scores the real task, at the unit the actor acts on. **MET-2** (Must), third bullet: a task we changed keeps the source's metric only when its meaning survives the change; the mediator's measurement says it does here.

2. **Confirm the exception for averaging a line's plots into one row?**

   * **Problem:**
     - The source ships one row per plot (a line in an environment), and the definition averages a line's adjusted plots into one line value, one row per line.
     - The split rules say to keep the source's rows, since averaging targets makes a different dataset[^s26]; superconductivity kept its repeated entries on that rule.
     - Every agent agrees the one row per line is right, but a departure from the rule needs your name.
   * **Background:** each plot carries an environment effect (-1,436 to +1,536 kg/ha against a target SD of 354) and a field-block effect (SD 367 kg/ha) that are no inputs at the prediction point, and lines saw 1 to 16 of 18 environments; a plot row's target is mostly where it was grown.
   * **Effect on the task:** one row per line is the unit the breeder selects; one row per plot with the environment as an input would be a genotype-by-environment task, another task.
   * **Consistency:** superconductivity (2026-11-08) kept a composition's entries, which differ by no measured condition; here the plots differ by a measured environment and block. This is the first exception to the rule, so no amendment is due.
     - boreal_postfire_lichen_biomass (2026-11-08) kept its quadrats with one vote per plot by a weight; that remedy here would keep plot rows whose target is mostly an environment no input carries.
   * **Panel:** every agent agreed (the builder, the precedent checker, the advocate, the critic, the mediator).
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | One row per line, recorded as an exception (implemented) | the line value from the adjusted plots; the exception text below in the record and the rule's Cases table | the unit the breeder selects; the source's data paper and Azodi ship one value per line | a departure from the rule, recorded |
     | B | One row per plot | 56,626 plot rows with the environment as an input, grouped by family | the source's rows | another task (genotype by environment); a plot's target is mostly its environment |

   * **Recommendation:** A: the line value is the unit the breeder selects, and the plots differ by measured conditions that are no inputs. **Decision:** A or B?

   **Notes for the AI:** on A, add to the record: `**Exception to SPLIT-26 (2026-11-xx, Lennart):** the source's plot rows are averaged into one line value, since each plot carries an environment effect (-1,436 to +1,536 kg/ha against a target SD of 354) and a field-block effect (SD 367 kg/ha) that are no inputs at the prediction point, and lines saw 1 to 16 of 18 environments; unlike superconductivity's entries, the repeats differ by measured conditions. Serves P3 (USE-5): the line value is what selection acts on.`, a row in the Cases table of splits.md (SPLIT-26, exception), and one clause in the Target bullet of the notes naming the exception.

   [^s26]: **SPLIT-26** (Should): "Keep the source's rows: deduplicating with averaged targets is a different dataset." Cases: superconductivity. **USE-5** (Must): predict what the actor would act on, at the resolution they act on it.

3. **Keep the default random assignment of families to folds, and accept the few-groups warning?**

   * **Problem:**
     - With 13 families per test fold, a fold's pooled r swings with which families it holds: ridge scores 0.38 to 0.66 per fold, following the spread of the test families' means (r 0.74).
     - The shipped fold seed is the worst of 41 tried: the dataset's score (the mean pooled r over its 9 splits) is 0.557 for kernel ridge against 0.567 to 0.630 for 40 random seeds (mean 0.601), because its one fold without a plant-introduction family (low-yielding exotic founders) scores lowest for every model.
     - `dataset check` warns that a test fold holds only 13 families; the AI proposes to accept the warning under every option, on the group-probe evidence below, and writes it into `dataset.py` only on your mark.
   * **Effect on the task:** every model's score on this dataset reads about 0.04 lower than under an average seed, which matters little when models are compared on this dataset; what can reorder models is the seed noise of their differences (SD 0.016 for ridge against kNN 50), which B and C cut by about a third.
   * **Experiments:**
     - Over 40 fold seeds per design (kernel ridge, the model of the fold-seed runs; issue 1's ridge scores 0.571 on the same folds; and kNN 50), the dataset's pooled r of kernel ridge moves by a seed SD of 0.018 under the shipped design (3 random repeats), 0.016 with 5 repeats and 0.010 with the plant-introduction families spread over the folds; the ridge-kNN difference by 0.016, 0.010 and 0.011.
     - The within-family r moves by a seed SD of 0.004 to 0.006 in every design.
     - Group probes on unseen families (R^2, baseline 0): LightGBM 0.194, random forest 0.050, kNN -0.086 and the untuned ridge (penalty 1) -1.961, which overfits 4,312 markers; the split gap is 0.317 (LightGBM R^2 0.570 at random against 0.253 grouped); ridge with a penalty equal to the number of markers reaches pooled r 0.57 on the same folds.
   * **Consistency:** airfoil_self_noise (11 setups per test fold), huesken_sirna_efficacy (10 genes) and open_university_learning_analytics_dataset (6 to 9) accepted the warning with group-probe evidence[^few]; 13 families per fold is more than any of them.
   * **Panel:**
     - Stratify or add repeats (the critic, the split auditor, the blind reviewer): the spread is large and follows the founder mix.
     - Keep the default (the advocate, the mediator): every fold is scorable and the model comparison survives the noise (argued on ridge beating LightGBM on 7 of 9 folds before the changes; 5 of 9 after, the two 0.016 apart); stratifying needs a founder-type column, which as a feature would change "from its SNP genotype alone".
     - If issue 1 goes to the within-family score, the fold design matters little (seed SD 0.004 to 0.006 in every design), but the warning still needs your acceptance.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Default random folds (implemented) | 3 repeats x 3 folds of random family assignment, as now; the warning accepted with the text in the notes for the AI, written into `dataset.py` only on your mark | the protocol's default; no new column; every fold scores 1,661 to 1,775 lines | the dataset score moves by a seed SD of about 0.018, and the shipped seed scores lowest of 41 (0.04 under the mean seed) |
     | B | Stratify by founder type | each test fold holds 2 to 3 plant-introduction families; a founder-type column the split reads, never a feature; the warning accepted with the same text, re-measured | cuts the score's seed SD from 0.018 to 0.010 and that of model differences from 0.016 to 0.011 | a new column and a split design no rule asks for |
     | C | Five repeats | 5 x 3 grouped folds; the warning accepted with the same text, re-measured | cuts the seed SD of model differences from 0.016 to 0.010 | departs from the protocol's default dimensions, no precedent; the score's own seed noise stays |

   * **Recommendation:** A: every fold is scorable, the warning's evidence holds, and no rule asks for another design; B if you want the score less tied to the fold seed (the shipped seed scores lowest of 41). **Decision:** A, B or C?

   **Notes for the AI:** on A, add to `dataset.py` (the AI never writes it before your mark): `accepted_check_warnings = {"groups_test_groups_few": "The 39 SoyNAM families after the source's QA are all the population has (13 per test fold), and holding out whole families is the use case (a new cross). Each fold scores 1,661 to 1,775 lines one by one, and the signal across families is real: on unseen families LightGBM reaches R^2 0.194, random forest 0.050, kNN -0.086 and the untuned ridge (penalty 1) -1.961 against the baseline 0 (group_probes.py, 2026-11-09); the untuned ridge overfits 4,312 markers, and a ridge with a penalty equal to the number of markers reaches pooled r 0.57 on the shipped folds, so the linear score is no verdict. LightGBM beats the dummy on 5 of 5 probed splits (task_probes.py). Per fold, the pooled r spreads 0.38 to 0.66 (ridge), following the founder mix of the test families (r 0.74 with the spread of their means): the fold without a plant-introduction family scores lowest for every model. With the shipped fold seed the dataset's score is the lowest of 41 seeds tried (kernel ridge 0.557 against 0.567 to 0.630)."}`. On B or C, the same acceptance with its numbers re-measured on the new folds. On B, a `founder_type` column (plant introduction or not, from the founder's name in `data.check.qa`; families 40, 41, 42, 48, 50, 54, 64) as the stratum of the grouped folds, kept out of the features; re-run `dataset check` and the group probes. On C, `n_repeats=5` in the split plan.

   [^few]: definitions.md, "Groups": accept `groups_test_groups_few` only with `group_probes.py` evidence. Weighed factor "Only a few groups" (splits.md). **SPLIT-27** (Should): judge a small grouped task with several model families, not one untuned run. huesken_sirna_efficacy (Lennart, 2026-11-04): "not a general license for few groups, the signal across groups is measured".

**Review panel:** ship after changes (mediator). Tier full: the claim, column and split auditors, the domain
practitioner, the blind reviewer, the task gamer and the precedent checker, then the advocate and the critic with one
rebuttal each, and the mediator, who ran three decisive measurements (what pooled r ranks models by, the fold design,
a fully check-based target). Claims: the claim auditor refuted two, both now fixed: the line value omitted the
field-block effects the data paper removes from the check plots (each set holds one family; block SD 367 kg/ha), and
70 lines carried another sample's raw genotype row (within-family r near 0 on them with the raw rows, about 0.3 with the QA rows, as on random lines); the reason given against the QA genotype matrix ("deletes the differences between families") was refuted too.
Blind review: include with changes; its concerns were the undocumented target (now documented), `family` as a feature
(the clean-room copy only; the container keeps it as the group), and the fold noise (issue 3). Task gamer: hard to
game; the only gain is rebuilding the test families and shrinking to their means (+0.02 ridge, +0.06 LightGBM), allowed
use now that the context is `all_rows`, and 0 under a within-family score. Agreed: ship; the check-based target, the
genotype repair, `all_rows`, the notes and the record year 2015, one row per line (issue 2; the exception needs your name). Disputed: the metric's unit (issue 1); whether to
stratify the folds (issue 3, optional on both sides). The numbers in the reports below are the panel's, measured on
the definition before these changes; the issues above carry the re-measured ones.

<details><summary>Mediator</summary>

```text
MEDIATOR REPORT: genomic_prediction_soy_yield (panel of 2026-11-08, written 2026-11-09)

Read: principles.md; MET-1/2/5/10/11/17, SPLIT-23/26/27/29, LEAK-29/30, definitions.md "Groups"; dataset.py, README,
record; builder_report.md; the reports of the claim, column and split auditors, domain practitioner, blind reviewer,
task gamer and precedent checker; the advocate's and the critic's briefs with their rebuttals.
New measurements: the run's work files: work_mediator/ (m1_metric_meaning.py -> m1.csv, m1.log; m2_fold_design.py -> m2.csv, m2.log;
m3_check_based_target.py, output below). Thread caps 4, the split auditor's cached frame and the shipped splits.

========================================================================================================================
1. JUDGMENT RECORD
========================================================================================================================
Verdict: ship after changes.
Validity: SEL-1, SEL-2 hold. USE-1, USE-3 hold (fit direct, with the notes of change 4). USE-5 and TP-7 triggered,
  fixed (target adjusted for environment and set effects from the check plots, as Diers et al. 2018 do). LEAK-10,
  LEAK-16..21, LEAK-33 hold. LEAK-29/30 removed by the same edit (no line plot of any fold enters another line's
  target). SPLIT-1, SPLIT-29 hold (grouped by family). SPLIT-23 triggered, fixed (context="all_rows"). SPLIT-26
  departure, an exception with its fact (one row per line). PROV-13 triggered, fixed (70 mispaired genotypes
  repaired). PROV-9 holds in the definition (2015), the record is fixed.
Value: TP-2, real signal on unseen families (pooled r 0.47-0.57, LightGBM beats the dummy on every split). MET-5 pooled
  r kept; MET-2 holds, measured (pooled r ranks 10 models like within-family r, Kendall tau 0.91). groups_test_groups_few
  accepted with all four probe models and the fold spread.
Quality: CLEAN-1 notes (heterozygous lines, off-types, merged entries).
Weighed: source metric + (one deliberate choice), between-family level of the score - (a parent baseline beats it),
  fold noise - (seed SD 0.016), units per fold +.
For the curator: issue 1, the metric's unit (a framing call: is the breeder's genomic decision within each cross or
  one ranking across crosses?); issue 2, confirm the SPLIT-26 exception; issue 3, fold design (optional).

========================================================================================================================
2. AGREED FACTS (no side disputes them after the rebuttals)
========================================================================================================================
F1 Task: 5,145 SoyNAM RILs x 4,312 SNP calls; 39 families (IA3023 x one founder each); grouped 3 folds x 3 repeats, 13
   families and 1,660-1,775 lines per test fold. Features are SNP calls only; `family` is the group, never a feature
   (the blind reviewer's concern 2 was the clean-room copy).
F2 No leak in the features: no cross-family pair above IBS 0.90, 0 exact copies, best single marker R^2 0.067,
   missing indicators <= 0.014, random column -0.002..+0.001, nearest-neighbour lookup 0.12-0.24.
F3 Grouped is right: IID pooled r 0.73 vs grouped 0.53 (ridge); within-family r barely moves (0.286 vs 0.261); the IID
   gain is the siblings' family means (family-mean r 0.98 vs 0.82).
F4 Target (USE-5, TP-7 Must): every env x set holds one family (1,707 of 1,707); every set has 2-20 check plots (median
   5); block SD 367 kg/ha. Block-adjusted LS mean: r 0.958 with the shipped target; repeatability across environment
   halves 0.557 -> 0.643, within families 0.327 -> 0.399; ridge pooled r 0.572 -> 0.618 (all 3 folds of repeat 0).
   The definition's "check-adjusted r 0.9991" adjusts per environment only and is redundant with the environment fit;
   "degenerate check covariate" holds for data.line `spot`, not for the QA tables' `set`.
F5 Mediator, m3 (the "else" branch of the agreed fix is not needed): a fully check-based target (environment effects
   from a check x environment fit of the six common checks, shrunken block effects per env x set, then the mean of a
   line's adjusted plots) correlates 0.998 with the block-adjusted LS mean and 0.960 with the shipped target;
   repeatability 0.639 (sd 0.027) vs 0.643, within families 0.390 vs 0.399, family means 0.936 vs 0.933. All 18
   environments have common checks; no plot lacks an adjustment. Between-family share 55.3%, SD 354 kg/ha.
F6 Genotypes (PROV-13 Must): 70 lines (1.4%) carry another sample's raw row; within-family r on them 0.035 with raw
   rows, 0.296 with the QA rows, 0.317 +- 0.106 on placebo sets. The QA matrix with flips undone and family-monomorphic
   blanks filled with IA3023's call equals the raw calls in 99.18% of cells, so "the QA matrix deletes the differences
   between families" is refuted.
F7 Environment effects over all lines (shipped target): per shipped fold, test-line shift SD 3.5-7.2 kg/ha (max 29),
   training max 49-53, Pearson moves <= 0.0015. The note's leave-one-family-out figures (0.9 mean, recomputed 1.39)
   are not the split's. Moot after F5.
F8 Context: the definition's own text says genomic selection "ranks the progeny of new crosses"; Lennart set
   context="all_rows" on the same fact twice (protein_model_quality_rf_pcp, huesken_sirna_efficacy, 2026-11-05).
F9 Metric level: 52.7% of the variance lies between families; true family means score pooled r 0.71 on the shipped
   folds, ridge 0.57; the founder's own yield alone 0.602 against ridge 0.529 on the 9 folds (optimistic: founders
   grown in the same trials; as a feature it would be LEAK-10); mid-parent 0.672. Within-family r 0.21-0.30. Azodi
   names pooled r as his criterion ("the standard metric for GP performance"), MSE for tuning only.
F10 Fold spread: per-fold pooled r 0.29-0.61 (ridge SD 0.108), r 0.78 with the spread of the test families' means; fold
   r1f2 holds no PI family. Ridge beats LightGBM on 7 of 9 folds (mean diff 0.040, SD 0.045).
F11 Notes and record: year 2015 not 2019; CRAN link missing from source_links; 219 lines above 20% heterozygous (r
   +0.02 with the family deviation); about 96 kept lines nearest another family; 5 lines pool plots of a distinct
   merged genotype; maturity correlates 0.27 with yield; train and test share the 2011-2013 seasons.

========================================================================================================================
3. CHANGES TO MAKE NOW (no decision needed)
========================================================================================================================
C1 Target from the check plots (USE-5, TP-7 Must; removes LEAK-29/30). Subtract from each line plot the environment
   effect and the shrunken (environ, set) block effect, both estimated on the common check plots of data_check_qa
   (Diers 2018, models 1-2); the line value is the mean of its adjusted plots (F5), in kg/ha. Export data.check.qa in
   download_description (the command today writes only data_line_qa, gen_raw, gen_qa). Rewrite the Target bullet,
   task_summary.predicted and the Decision table (options: plain mean, LS mean over lines, block-adjusted LS mean,
   check-based = shipped; with their r and repeatability); drop the 0.9991 and "degenerate covariate" sentences and
   the all-lines Note bullet; say no line's plots enter another line's target. Both sides agreed; F5 shows the
   check-only form loses nothing measurable, so no LEAK-30 note is needed.
C2 Genotype repair (PROV-13 Must, PROV-14; repair before drop on the ladder). Each line gets its own sample's calls
   under the QA release's identity: gen.qa with the flips undone and the family-monomorphic blanks filled with
   IA3023's call; a call that failed stays missing (CLEAN-2). Verify with the claim auditor's a9 test (within-family r
   on the 70 near the placebo 0.32). Drop a line only if its sample cannot be restored, and state the count. Rewrite
   the Features bullet (the refuted reason goes). Check whether gen.qa holds rows for any of the 29 QA lines without a
   raw row (they would join the task).
C3 Grouping context="all_rows" (SPLIT-23 Must), with the reason in the group definition: the breeder genotypes and
   ranks a new cross together and knows which lines are siblings. Follows protein_model_quality_rf_pcp and
   huesken_sirna_efficacy. The task gamer's exploits become allowed use (section 6).
C4 Notes and record (PROV-9, CLEAN-1, writing.md, USE-8): record year 2015 and the CRAN link in source_links (through
   the store); cite Diers 2018 and Song 2017; the QA's reasons for its 399 dropped lines (Diers 2018: a genotype
   identical to IA3023, off-type segregation, family 46 crossed with a wrong founder); the 219 heterozygous lines,
   the ~96 off-types and the 5 distinct-genotype merges, kept; the shared seasons and the maturity range (late MG II
   to early MG IV, r 0.27). While pooled r stays: the within-family r (0.21-0.30) and the parent baseline (founder
   0.60, mid-parent 0.67, same trials) in fit_reason or the Metric bullet; both sides accept this as the floor.
C5 accepted_check_warnings["groups_test_groups_few"] (definitions.md "Groups"; precedents airfoil, open_university):
   name all four group-probe models (LightGBM, random forest, kNN, untuned ridge, with the tuned ridge as the reason
   the linear score is no verdict, SPLIT-27) and the per-fold spread with its cause (the founder mix of the test
   families). Take the numbers from the re-run in C6.
C6 After C1-C2, re-run the task, group and leak probes and refresh every number in the notes and the README
   (between-family share 52.7% -> ~55%, probe scores, environment-effect ranges).

========================================================================================================================
4. ISSUES FOR THE CURATOR (rank order)
========================================================================================================================
Issue 1 (P6; MET-1 Must, MET-2 Must, MET-5 Should): pooled r (Azodi) or mean_group_pearsonr on family (context)?
  Problem: pooled r on 13 unseen families is half a ranking of families, and a breeder can rank crosses from the
  parents' records.
  The disputed fact, settled by measurement (m1): does pooled r keep its meaning on our split (MET-2, third bullet)?
  Ten models (ridge at 5 alphas, kNN 10/50, LightGBM x2, random forest) on the 9 shipped folds and on a random 3-fold
  split (Azodi's design):
                                   grouped (shipped)   random lines (Azodi)
    tau(pooled r, within-family r)       0.91               0.81
    tau(pooled r, family-mean r)         0.73               0.72
    per-fold tau(pooled, within)    mean 0.81, min 0.64   mean 0.85, min 0.82
  The level of pooled r is mostly between families (F9), but the order of models, which is what the benchmark reads,
  follows within-family accuracy at least as closely as on the source's split. MET-2's third bullet holds: the
  meaning survived the change of split. So no Must forces the switch, and MET-5 (Should) keeps Azodi's one deliberate
  criterion. This settles the critic's MET-2 claim against him and the advocate's for him.
  What stays open is MET-1's unit, a use-case fact the data cannot settle: does the breeder's genomic decision rank
  the lines within each cross (cross means from the parents), or one list across crosses?
  - Critic and practitioner, best evidence: the founder's yield alone (0.602) beats ridge (0.529) on the same folds;
    the family-mean oracle 0.71; "what genomics adds at this decision is the within-cross ranking" (practitioner;
    Windhausen 2012, Stewart-Brown 2019 on population-structure inflation). The two metrics part where it matters for
    context: a family-shrinkage model gains +0.017 (ridge) / +0.055 (LightGBM) on pooled r and exactly 0 on
    within-family r (a positive affine map within a family leaves its r unchanged). Within-family r is also 3-5x more
    stable across fold seeds (m2: SD 0.003-0.005 vs 0.016).
  - Advocate and builder, best evidence: Azodi's deliberate choice (MET-5); the use case as written ranks the lines of
    "new crosses" together and the breeder truncates across crosses; the parent baseline uses same-trial yields that
    a model may not have (LEAK-10); m1: both metrics order the models nearly alike (Spearman 0.98).
  - What would settle it: the curator's statement of the decision; or a source on how held-out-family accuracy is
    reported for SoyNAM (Xavier & Rainey 2019 run leave-family-out on this population; whether they report r per
    family was not read by anyone on the panel).
  Decision: keep pooled r (default by MET-5, with the notes of C4) or switch to mean_group_pearsonr on family from
  context, naming Azodi's pooled r as the overruled original (MET-11). A switch is the third case of the reason after
  protein_model_quality_rf_pcp and huesken_sirna_efficacy, so the amendment is due with it, and its wording must say
  that the reason also overrides a paper's deliberate pooled criterion when the split is ours (the precedent
  checker's draft for MET-5/MET-11 does).

Issue 2 (P4 Should; SPLIT-26): confirm the exception for one row per line. Both sides agree; an exception needs the
  curator's name. Text (precedent checker's draft, facts updated for C1):
  **Exception to SPLIT-26 (2026-11-xx, Lennart):** the source's plot rows are averaged into one line value, since
  each plot carries an environment effect (-1,252 to +1,471 kg/ha against a target SD of 359) and a field-block effect
  (SD 367 kg/ha) that are no inputs at the prediction point, and lines saw 1 to 16 of 18 environments; unlike
  superconductivity's entries, the repeats differ by measured conditions. Serves P3 (USE-5): the line value is what
  selection acts on.
  First exception to SPLIT-26: no amendment due.

Issue 3 (P6, weigh; "only a few groups", groups_test_groups_few): fold design, optional.
  Measured (m2, 40 fold seeds per design, kernel ridge alpha = number of markers, kNN-50 as the second model):
                               mean pooled r   seed SD of the   seed SD of the      per-fold SD
                                               dataset score    ridge-kNN diff
    3 random repeats (shipped)     0.568          0.0164           0.0147             0.076
    5 random repeats               0.563          0.0167           0.0099             0.079
    3 repeats stratified PI/not    0.580          0.0104           0.0105             0.060
  Within-family r: seed SD 0.003-0.005 in every design. The shipped seed sits near the 5th percentile of random seeds
  (ridge 0.529-0.536 against a mean of 0.568).
  - Critic (and split auditor, blind reviewer): stratify by founder type or use 5 repeats; spread 0.29-0.61.
  - Advocate: no Must asks for it; the model comparison survives (7 of 9 folds); P4-over-P6 row.
  Settled by rank: no Must or Should is triggered (every fold is scorable; the repeats follow the protocol's default
  by size). Optional either way. Stratifying cuts the score's seed noise by about a third but needs a founder-type
  column, which as a feature would change "from its SNP genotype alone"; 5 repeats cut only the model-difference noise
  and depart from the protocol's default dimensions (no precedent). If the metric goes to within-family r (issue 1),
  the question disappears. Decision: keep the default (recommended), stratify on founder type, or 5 repeats.

========================================================================================================================
5. DISPUTED POINTS, HOW THEY WERE SETTLED
========================================================================================================================
D1 MET-2 third bullet, pooled r on the grouped split. Critic: Must triggered (F9). Advocate: the family part was in
   Azodi's score too, and the model now earns it from markers. Rank: both rest on MET-2 (Must); facts first. m1: the
   model order under pooled r tracks within-family r (tau 0.91) as on Azodi's split (0.81). Holds; the metric is a
   curator call under MET-1's unit, not a required change (issue 1). Within-family r would be the third case of its
   reason: yes, an amendment is due with a switch, not otherwise.
D2 Stratified folds or 5 repeats. Critic: a remedy for the spread. Advocate: optional. Not a conflict: the spread is a
   weighed factor, every fold is scorable, and P4-over-P6 keeps the split. Optional (issue 3); both sides converged on
   "optional" in the rebuttals.
Converged in the rebuttals (now changes C1-C5): target block adjustment (USE-5/TP-7), the 70 genotypes (PROV-13), the
   context (SPLIT-23), the all-lines environment fit (LEAK-29/30, settled by F5), notes and record.

========================================================================================================================
6. TASK GAMER'S EXPLOITS, MAPPED
========================================================================================================================
The definition has no `Potential leak, kept on purpose:` note and no accepted warning that covers these, so all are new.
E1 Rebuild test families by clustering (ARI 0.82-0.98), shrink to family means: +0.017 ridge (-0.039..+0.088), +0.055
   LightGBM (-0.011..+0.130); true-label ceiling +0.027 (ridge). Rule: SPLIT-23 (context). Under "none" a forbidden
   test-batch statistic nothing enforces; under all_rows (C3) allowed use, as on protein and huesken ("the context
   follows the use case, not the gain"). Under mean_group_pearsonr its gain is 0 by construction. Not an issue after
   C3; the notes may state the gain so methods know siblings help.
E2 Family-mean missing-call count from rebuilt families: +0.013 (-0.047..+0.053); per row +0.000. Rule: SPLIT-23 as E1
   (the per-row count is a legal feature, CLEAN-2). Allowed under all_rows; 0 under within-family r. Not an issue.
E3 (the gamer's "flaw") fractional offset groups in y (276 groups, 26% of variance): the env x set adjustments of the
   shipped target. Rule: USE-5/TP-7; fixed by C1.
E4 Lookup in Azodi's public file (4,762 matches, 0.583 as a prediction, r 0.64 with our target): external public data,
   no rule of the task; every public source has it. No action.

========================================================================================================================
7. CONSISTENCY WITH PRECEDENT (from the precedent checker, updated)
========================================================================================================================
Followed: TP-7 target convention (the check-based adjustment is the data paper's own, Diers 2018); grouped by the
cross (huesken, superconductivity, airfoil; sarcoma set apart: a new cross has no phenotyped sibling);
groups_test_groups_few (airfoil 11, huesken 10, open_university 6-9 test groups; here 13); QA lines (ashrae, CLEAN-1);
context all_rows (protein, huesken, after C3); our own all-row value fixed when a fix exists (sf_permit_time,
home_credit, after C1); year 2015 (airfoil, tully_fisher, wadden_sea for the record fix); raw-equivalent calls rebuilt
from the release (coad: the restored QA matrix equals the raw calls in 99.18% of cells).
Departure with a fact: SPLIT-26 one row per line (issue 2): environment and block effects per plot are measured
conditions, unlike superconductivity's entries and boreal's quadrats. First exception.
Open pair: pooled r here against mean_group_pearsonr on protein and huesken. Fact that sets this case apart: Azodi
names one deliberate criterion, where protein and huesken replaced a fallback; and m1 shows pooled r ranks models like
within-family r here. Reflection question for the curator:
  **Consistency check (AI, 2026-11-09):** keeping pooled r differs from protein_model_quality_rf_pcp and
  huesken_sirna_efficacy (pooled score of group means replaced by mean_group_pearsonr). What sets soy apart?
  (a) the source's one deliberate criterion, and a pooled r that orders models like the within-family r (tau 0.91),
  recorded as the reason; (b) treat soy like them, switch, and amend MET-5/MET-11 (third case); (c) reopen protein and
  huesken; (d) change the rule.
No drift found in Lennart's calls on SPLIT-23, SPLIT-29/31, MET-5 or PROV-9.

Files: definition datasets/_dev/tabarena-v0pt2/genomic_prediction_soy_yield/dataset.py; record
curation/records/genomic_prediction_soy_yield.md; measurements the run's work files: work_mediator/{m1.csv,m1.log,m2.csv,m2.log,
m3_check_based_target.py}.
```

</details>

<details><summary>Claim audit</summary>

```text
CLAIM AUDITOR REPORT: genomic_prediction_soy_yield (2026-11-09)
Folder: datasets/_dev/tabarena-v0pt2/genomic_prediction_soy_yield/ ; record curation/records/genomic_prediction_soy_yield.md
Scratch: the run's work files: work_claim_auditor/ (scripts a1-a14, outputs: shipped.parquet, container_row_names.csv,
raw_vs_qa_concordance.csv, line_offtype.csv, neardup_pairs.csv, qa_line_plot_provenance.csv)

VERDICT: ship after changes. Two refutations, both fixable in the definition from files already downloaded:
(1) the target ignores the set (block) effects that the source removes. Its own data paper, Diers et al. 2018,
model 1, estimates them from the check plots in each set. They are large (SD 367 kg/ha) and each set holds one family.
(2) 70 shipped lines (1.4%) pair a QA phenotype with a raw genotype row of another sample.
The metric, the grouped split, the copies check and most counts hold.

Judgment record
Validity: USE-5 triggered (target built without the source's block adjustment; fix: block-adjusted LS mean);
PROV-13 triggered, small (70 mispaired genotype rows; fix: QA genotypes with blanks filled from IA3023, or drop them);
LEAK-16..21 hold (0 cross-family pairs above IBS 0.90); SPLIT-1/SPLIT-29 hold; LEAK-29 holds (LOFO shift max 5.4 kg/ha).
Value: MET-1/MET-5 hold (Azodi's pooled r, quote verified); MET-2 holds with a weighing note (pooled r on 13 unseen
families is mostly family-mean ranking: the family-mean oracle scores 0.71, ridge 0.57).
Quality: heterozygosity of 219 lines above 20% (mixed DNA samples) undocumented (claim 31 hides it).

=====================================================================================================
TABLE: claim | source | test | result | evidence | rule
=====================================================================================================
C1 use case (breeder ranks lines of new crosses by genotype) | task_summary.use_case | read Azodi Intro; features are only
   genotypes | holds | genotype only, no field trait ships | USE-1, USE-3
C2 one row = one RIL; 39 families of IA3023 x founder; 1-16 of 18 envs, median 11 | task_summary.row | recount from
   data_line_qa + gen_raw | holds | 5,145 lines, 39 families (98-140), n_env 1/11/16 (only 2 lines with <=5 envs);
   IA3023 call equals the family mode at 99.9-100% of family-monomorphic markers | -
C3 target = LS mean over plots after removing environment effects | task_summary.predicted, line_values | exact sparse
   least squares vs backfitting | holds as computed (max diff 0.0 kg/ha) | a10 | -
C3b (implied) this is the real-world line value | curation_comments "Target" | read Diers et al. 2018 (G3 8(10):3367;
   the data paper the builder did not read) and test a block adjustment | REFUTED (weighing, see R1) | Diers fit model 1
   on checks for "shrunken block effects" (1,726 blocks) and used them as covariates in model 2 (BLUP genotypic values).
   Sets are family-specific (every env x set holds exactly 1 family: 1,707 of 1,707). Check-based block BLUPs: block SD
   367 kg/ha (plot SD within block 425). Block-adjusted LS mean vs shipped r = 0.958 (family means 0.975).
   Repeatability between disjoint halves of the 18 environments (10 random halves): shipped 0.557 (sd 0.036),
   block-adjusted 0.643 (sd 0.028); within family 0.327 -> 0.399; family means 0.858 -> 0.933. Ridge on the shipped
   grouped folds (repeat 0): pooled r 0.572 -> 0.618 (higher on all 3 folds), within-family 0.267 -> 0.295 | USE-5, PROV-13, EV-1
C4 4,312 SNPs of the 6K chip coded 0/1/2 copies of one allele | known | value counts; coding vs IA3023 | holds (global
   allele coding, het = 1) | a7 | CLEAN-14
C5/C38 whole families held out; stricter than Azodi | split | splits of the container | holds | 3x3 folds, 13 test families
   each, 0 family overlap train/test, 1,660-1,775 test lines | SPLIT-1, SPLIT-29
C6 changes stated | changes | - | holds, but incomplete: the genotype rows are not the release's QA identities (R2) | writing.md
C8-C10 SoyBase release; CRAN copy "downloaded on November 16th 2015"; first CRAN version 2015-07-29 | curation_comments,
   year | soynam.Rd; CRAN Archive listing (curl) | holds | SoyNAM_1.0 2015-07-29; Diers 2018: "The quality-assured
   phenotypic and SNP genotypic data are available for download from SoyBase" | PROV-8, PROV-9
C11 GPL-3 | license | DESCRIPTION | holds (package licence; data terms not found, as stated) | PROV-10
C12 citation | bibtex | DESCRIPTION authors | holds | -
C13 sha256 and reproducible export | download_description | sha256sum; cmp of repro/ vs warehouse parquet | holds
   (0bd87f7b...aaa; three files byte-identical) | -
C14 Azodi cut 5,014 lines, YLD mean 0 SD 1 although README says "between 0 and 1" | curation_comments | soy_pheno.csv
   describe | holds (mean 0.000, sd 1.000, min -4.28) | -
C15 Azodi YLD r 0.971 with the plain mean, 0.951 with ours | curation_comments | recompute | holds (0.9713 / 0.9512 on 5,005
   lines); with the block-adjusted value 0.919, so Azodi did not block-adjust either | -
C16 Azodi does not say how YLD was computed | curation_comments | read the paper (WebFetch) | holds: paper says only
   "Phenotype values were normalized between 0 and 1" | USE-5
C17/C36 metric pearsonr from Azodi "Assessing predictive performance" | metric | read the paper | holds: r "was used as it
   is the standard metric for GP performance"; MSE only in the grid search | MET-1, MET-5, MET-11
C17b (implied, MET-2) pooled r means on our split what it meant in Azodi | metric | oracle and probe decomposition |
   holds with a note: under the grouped split the family-mean oracle (true mean of each test family) scores pooled r
   0.742/0.668/0.733 (mean 0.71), above ridge 0.57; within-family r is 0.27-0.30 for ridge. Pooled r on 13 families per
   fold mostly scores ranking new crosses. That fits the stated use case. The within-family alternative
   (mean_group_pearsonr) is the builder's issue 4 | MET-2, MET-10
C17c scorer computable on every fold | metric | scorer(c) on constant and noisy-oracle predictions | holds: constant = 0.0
   on 9/9 folds; noisy oracle 0.59-0.74 | MET-2, MET-13
C18 Azodi held out 20% random lines, 10 replicates | splits_comment | read the paper | holds | SPLIT-5
C19 5,145 lines; 29 QA lines without a genotype row | curation_comments | recount | holds (5,174 QA lines with yield, 29
   without gen.raw row) | -
C20 QA drops 399 of 5,544 genotyped lines, family 46 whole | curation_comments | recount | holds (127 of the 399 are
   family 46). The source's reasons (Diers 2018): RILs with "a SNP genotype identical with the female founder"
   (61 of the 272 non-N46 drops have IBS > 0.95 with IA3023), off-type segregation, and N46 crossed with a wrong
   founder. The builder's "family label doubtful" is right in direction but does not give these reasons. | PROV-14
C21 dropped lines off-type more often (154/399 vs 96/5,145) | curation_comments | own off-type rate at family-monomorphic
   markers | holds in direction (exact nearest-centroid numbers not rerun); kept lines: 53 with off-type rate > 5% | -
C22 parents and checks left out | curation_comments | name prefixes of shipped rows | holds (5,009 DS11-, 136 DS12-; 0 with
   IBS > 0.90 to IA3023) | SEL-? n/a
C23-C25 backfitting = LS; 18 envs with yield, NE_2013 none; env effects -1,252 to +1,471 | curation_comments | recompute |
   holds | a10 | -
C26 r 0.970 with plain mean; 0.9992 with moment BLUP; 0.9991 with a check-adjusted mean | curation_comments | recompute;
   the check adjustment the builder used is per environment | numbers hold. The conclusion "the choice barely moves
   Pearson" is REFUTED: an environment-level check adjustment does nothing once environment effects are fit. The
   source's adjustment is per set, and it moves the target to r 0.958 (see C3b). The builder's report says the
   package's check covariate is degenerate. That holds for `spot` in data.line, not for the QA tables:
   data_line_qa and data_check_qa both carry `set`, and every set has 2-20 check plots (median 5) | USE-5, EV-1
C27 56 lines > 13 plots (up to 36), several plots of one set named by one line | curation_comments | trace QA plots to raw
   plots (env, yield, protein, oil, size) | holds as a fact, explained: the QA merged raw lines under one name, e.g.
   DS11-03032 <- DS11-03033 (raw IBS 1.00), DS11-02040 <- DS11-02055 (0.97), but also DS11-13008 <- DS11-13010 (raw IBS
   0.58, siblings, not copies); QA renamed raw DS11-13031 to DS11-13010 in phenotypes AND genotypes (see R2) | PROV-13
C28 LOFO shift of env effects 0.9 kg/ha mean, 5.4 max | curation_comments | refit without each family | holds in
   magnitude: mean |shift| 1.39 kg/ha (not 0.93; averaged per family), max 5.41, largest family-mean shift 3.27; target SD
   359 | LEAK-29
C29 52.7% of variance between families | grouping.definition | recompute | holds (0.5271; 0.552 after block adjustment) | SPLIT-29
C30-C33 QA markers; QA matrix recodes ~half, blanks non-segregating markers (25.6%); non-QA markers 53% missing | features |
   recode and blanks: 1,984 of 4,312 markers flipped; non-QA 0.532 missing | facts hold. The reason not to use gen.qa
   is REFUTED: "deletes the differences between families" is wrong. The blanks are the markers where the family does
   not segregate, so their value is the common parent's call. Filling them with IA3023's call reproduces the raw call
   in 99.18% of the cells of the 5,075 concordant lines. The QA matrix also carries the QA's sample identities (R2) | CLEAN-1, PROV-13
C31 heterozygous 1 about 5% (5.4% shipped) "as RILs show" | curation_comments, builder P2 | per-line heterozygosity |
   pooled number holds (0.0539); hidden tail: 219 lines have > 20% het calls (max 70.6%), which F5-derived RILs
   (expected ~6%) do not show; these are mixed DNA samples; 39 of them are among the 70 mispaired lines | CLEAN-1
C34 missing 1.5% of cells, max 20.1% per marker, not imputed | curation_comments | recount | holds (0.0152; 0.2006) | LEAK-30
C35 no duplicate genotypes, no constant marker | curation_comments | exact duplicates; IBS on jointly called markers |
   holds (0 exact, 0 constant); 60 within-family pairs with IBS > 0.95 (14 above 0.99), none across families | LEAK-16
C37 grouped on family, 3x3, 13 families per test fold | grouping | container splits | holds | -
I1 (implied) every feature known at the prediction point | - | features are SNP calls only | holds | LEAK-10
I2 (implied) no row is a copy across the split | - | IBS of every pair across families | holds: max cross-family IBS
   below 0.90 for all 5,145 lines (0 pairs > 0.90; 118 within-family pairs > 0.90) | LEAK-16..21
I3 (implied) each row's features are that line's genotype | - | raw vs QA genotype rows of the same name; decisive
   prediction test | REFUTED for 70 lines (see R2) | PROV-13, EV-1
I4 (implied) the split is the one the use case needs | - | builder's group probes reread; within-family r IID vs grouped
   similar (0.26-0.28 vs 0.21-0.27), family-mean r 0.98 vs 0.82 | holds: the grouped split only removes the family
   means that siblings hand over | SPLIT-1, SPLIT-29

=====================================================================================================
REFUTED, ranked (principles.md: P3 before P5; Must first)
=====================================================================================================
R1 (P3, USE-5 Must "check how the source built its label"; PROV-13): the target omits the set (block) effects that
   the source's own line values remove (Diers et al. 2018, models 1 and 2). Each env x set holds one family, so block
   effects add family-specific field noise. Block SD 367 kg/ha. The shrunken block effects averaged per family span
   -96 to +162 kg/ha (SD 59).
   Measured: r 0.958 with the shipped target. Repeatability across disjoint environment halves 0.557 -> 0.643, within
   family 0.327 -> 0.399, family means 0.858 -> 0.933. Ridge pooled r on the grouped folds 0.572 -> 0.618.
   The builder's "alternatives barely move Pearson" comes from an environment-level check adjustment, which is
   redundant with the environment effects.
   What it changes: the shipped target is noisier than the source's line value, and it is not the source's
   construction. Not a leak: block effects come from check plots only, never from the lines' yields.
   Mildest remedy: in `_clean`, subtract a check-based block effect per (environ, set) before `line_values`.
   Compute it as the mean residual of the common checks (IA3023, U06-100052, LD04-11056, LD04-13265, IA2094,
   U09-215057) after check x environment means, shrunk by vb/(vb + ve/n). This is a10/a12/a14 in the scratch folder,
   about 10 lines. Read data_check_qa.parquet as a raw file (already downloaded). Then update the Decision table
   and the "Target" bullet, citing Diers 2018. Draft issue 1 should offer this as option (d) and recommend it.
   The alternative: keep the shipped value with a note that names the gap (USE-5 allows fit "approximate" only for an
   undocumented label, and this one is documented).

R2 (P5, PROV-13 Must, small): 70 of the 5,145 shipped lines (1.4%; 103 below 97% concordance) carry a gen.raw row
   that is not the sample the QA release calls that line. Per-line concordance of gen.raw[X] with gen.qa[X], with
   the QA flips undone: median 1.000, but 70 lines below 0.90 and as low as 0.15. In those cases the QA renamed
   samples consistently in phenotypes and genotypes: QA DS11-13010 = raw DS11-13031 (genotype IBS 0.974, and its
   QA plots trace to raw 13031). QA DS11-08034 = raw DS11-08040 (0.999). QA DS11-24145's raw row is 57%
   heterozygous, a mixed sample.
   Decisive test (a9): ridge trained on the other lines, predicting these 70 lines. Within-family r is 0.035 with the
   shipped raw rows, 0.296 with the QA rows (blanks filled with IA3023's call), and 0.317 +- 0.106 on 20 placebo sets
   of 70 concordant lines. Pooled r: 0.564 raw, 0.639 QA, 0.74 placebo. The QA genotype is the one that belongs to
   the phenotype.
   What it changes: about 1.4% of the rows are label noise, and claim 30-32's reason against the QA matrix falls.
   Mildest remedy: take the features from gen.qa, with the QA flips undone and each blank filled with IA3023's call
   at that marker. This is lossless (99.18% agreement with raw calls elsewhere), label-free, per row, and keeps the
   QA's sample identities. The simplest alternative is to drop the 70 lines whose raw and QA rows disagree.
   Either way, write it in the "Features" bullet.

R3 (procedure, writing.md): claim C26/report "the package's check covariate is degenerate" holds for data.line only; the
   QA tables carry `set`. Remedy: correct the sentence in the builder report / draft issue 1 (part of R1).

R4 (P7, CLEAN-1, quality note): claim 31 ("5% heterozygous, as RILs show") hides 219 lines with > 20% heterozygous calls
   (max 71%), likely mixed DNA. Remedy: name it in the notes. R2's remedy fixes 39 of them; the rest stay with a note.

Minor numeric: C28 mean LOFO shift recomputes as 1.39 kg/ha (claim 0.9; max 5.41 matches). Remedy: restate or say how
   averaged; the conclusion (negligible vs SD 359) stands.

=====================================================================================================
UNTESTED (and why)
=====================================================================================================
U1 Song et al. 2017 (population, chip) not read; the population facts were checked against Diers 2018 and the package help.
U2 SoyBase's own terms and release date: page offline; Wayback not tried here (the builder could not reach it).
U3 C21 exact counts (154/399, 96/5,145): the builder's nearest-centroid scratch run was not repeated; my off-type
   measure agrees in direction.
U4 Whether Diers' planting-date covariate matters on top of blocks: data_line_qa has no planting date (the raw
   data.line has `planting`), not tested.
U5 Tuned models on the repaired target and genotypes: only untuned ridge ran.

Sources read: Azodi et al. 2019 (academic.oup.com/g3journal/article/9/11/3691/6026746); Diers et al. 2018
(academic.oup.com/g3journal/article/8/10/3367/6026979); Xavier et al. 2016 (pmc.ncbi.nlm.nih.gov/articles/PMC4978914);
CRAN Archive listing of SoyNAM; package help soynam.Rd, BLUP.Rd, BLUP.R.
```

</details>

<details><summary>Column audit</summary>

```text
COLUMN AUDITOR REPORT: genomic_prediction_soy_yield (panel of 2026-11-08, written 2026-11-09)

Verdict: ship. No feature leak, no feature cleaning problem. Four notes and questions, all weak (P4 notes and P5/P7
quality). The family column is the group only (LEAK-33 holds). The target build over all lines is a weak transductive
effect: per shipped fold it moves Pearson by at most 0.0015.

Scripts and outputs: the run's work files: work_column_auditor/ (a1.py to a11.py, clean.parquet, target_foldrefit.json,
merged_plots.csv, dtype/). The frame was rebuilt from the definition (_load_raw/_clean, 5,145 x 4,314) and the
container (to_container, its splits). The dtype probe was re-run into work_column_auditor/dtype: 0 of 4,312 columns
flagged, no codebook.

Prediction point (first curation_comments bullet): the breeder ranks inbred lines of new crosses before yield
trials, so only the genotype is known. The frame has 4,312 marker columns, `family` (group) and `yield_kg_ha`
(target). No field trait (height, R8, lodging, protein, oil, size), environment, location, year, set, spot or check
variety ships. feature_columns(container) gives 4,312 columns and contains neither family nor the target.

------------------------------------------------------------------------------------------------------------------
1. COLUMN TABLE (by block, then a sample of markers)
------------------------------------------------------------------------------------------------------------------
column | meaning | known at prediction? | dtype and cleaning | verdict | rule

Gm<chr>_<pos>_<a>_<b> (4,312) | raw SoyNAM 6K chip call: copies of one fixed allele per marker (0/1/2), the same
  allele for every line and family. Which of the two named bases is counted is not documented (unknown). | yes:
  the genotype of the line, fixed before any trial | float64 dosage (numeric, CLEAN-14: an allele count). Values only
  0/1/2/NaN. Missing 1.52% of cells (max 20.06% per marker, 27.99% per line), not imputed (CLEAN-2). No constant
  column, no exact copy and no copy up to a flip (x vs 2-x) (CLEAN-5); the rarest homozygote has at least 254 lines
  per marker, so no near-monomorphic marker. Marker set: the source's QA (missing rate, segregation), genotype-only,
  label-free (CLEAN-8) | fine | CLEAN-14, CLEAN-2, CLEAN-5, CLEAN-8, LEAK-31 n/a
family | SoyNAM family = the cross IA3023 x founder; 39 levels "family_02" .. "family_64"; it matches the middle
  digits of the strain id for all 5,174 QA lines, and no line has 2 families | yes (pedigree) | category; the group
  column, not in feature_columns | fine (group only) | LEAK-33, CLEAN-3
yield_kg_ha (target) | the line's least-squares mean under yield = line + environment, fixed effects, centred
  environment effects, over the QA plots of the lines only (no check plots) | outcome | float64 kg/ha, SD 359;
  environment effects fit on all 5,174 QA lines, test families included | weak transductive effect, keep with a note
  (section 2.1) | LEAK-29 by analogy (a label, not a feature), LEAK-30 weak, LEAK-5/LEAK-6 measured
(dropped) strain | line id; DS11-FFxxx / DS12-18xxx, FF = family | n/a | dropped, correct (it encodes the group) |
  fine | CLEAN-3, LEAK-33

Sampled markers (missing, heterozygous share, share of 2 among calls, IA3023's raw code, families segregating out
of 39, r with the target):
  Gm19_40068456_A_G   0.013 0.028 0.795 2 15  +0.336  the strongest single marker (leak probe: R^2 0.067 alone);
                      chr 19 near the maturity / growth-habit loci, a QTL, known at prediction: fine
  Gm18_38907626_C_T   0.006 0.031 0.785 2 15  -0.235  second-ranked marker: fine
  Gm01_3321482_T_C    0.007 0.041 0.720 2 21  -0.202  first column: fine
  Gm16_1411646_A_G    0.201 0.013 0.889 2  8   0.000  the most missing marker (20.1%): fine, kept missing
  Gm02_29931846_A_G   0.133 0.025 0.819 2 12  +0.094  13% missing: fine
  Gm02_6027712_G_T    0.023 0.087 0.508 2 36  +0.033  the most heterozygous marker (8.7%): fine
  Gm12_15420968_G_T   0.006 0.012 0.938 2  4  +0.105  segregates in the fewest families (4): fine (QA keeps it)
  Gm02_7839398_C_T    0.012 0.079 0.459 2 39  +0.003  segregates in all 39: fine
  Gm06_17343138_C_A, Gm11_1774038_G_T, Gm18_14983458_C_T, Gm13_38945977_C_A (random): missing 1.0-1.7%, het 4.8-5.8%,
                      27-35 families segregating: fine
Families segregating per marker: median 30, min 4, max 39. Heterozygous share per marker: median 5.3%, max 8.7%.

------------------------------------------------------------------------------------------------------------------
2. FINDINGS, IN RANK ORDER (principles.md)
------------------------------------------------------------------------------------------------------------------

2.1 P4 / LEAK-29 by analogy, LEAK-30 (weak, Should): the target uses environment effects fit on all lines. Keep
    with a note, and give the note the shipped folds' numbers.
  Evidence: for each of the 9 shipped splits (a4.py, a4b.py, target_foldrefit.json) I refit the environment effects
  on the training lines only and recomputed the test lines' values from those effects:
  - test targets, honest against shipped: r 0.99973 to 0.99996. Per-line shift SD 3.5 to 7.2 kg/ha, max |shift|
    29 kg/ha. The mean shift per fold is -5.6 to +7.5 kg/ha, a constant to which Pearson does not respond. The SD of
    the family-mean shift is 1.1 to 2.7 kg/ha.
  - training targets: r 0.99986 to 0.99993, max |shift| 49 kg/ha. The target SD is 359.
  - a ridge model (alpha = number of markers, mean-imputed per fold) gets test Pearson 0.294 to 0.610. The shipped
    target scores -0.0014 to +0.0015 against the honest one (mean +0.0004).
  - No channel to exploit: the features hold no environment, so a model cannot see which trials a test line shared.
  The curation note's "0.9 kg/ha on average, at most 5.4" leaves one family out. The shipped folds hold out 13
  families, and their shifts are about 5 to 8 times larger (still under 2% of the SD).
  Mildest remedy: keep the target. Reword the "Note:" bullet with the per-fold figures above, in LEAK-30's form
  ("Potential leak, kept on purpose: ..."), so that it matches the precedents of weak all-row effects. A per-fold
  target is not supported by the container and would buy at most 0.0015 r.

2.2 P4 / SPLIT key quality (weak, question): some family labels are doubtful.
  Evidence: the builder found 96 of 5,145 kept lines nearest another family's mean genotype. I add:
  - Per family, the homozygous calls that match neither parent are 0.05% to 2.9% of the calls (a6.py).
  - Family 25 (IA3023 x LG03-3191) is the noisiest: 6.5% of its homozygous calls disagree with its stated founder's
    genotype. Its heterozygous rate is 10.9% (median family 5%). 128 of the 610 5-nearest-neighbours of its lines lie
    in family 24 (founder LG03-2979). 117 of its 122 lines still match LG03-3191 better than LG03-2979, so the label
    is mostly right; the founder sample may not be the seed lot that was used.
  - When a mislabelled line is in a test fold, true siblings in training inform it.
  Size: at most about 2% of the rows; a grouped probe gap of 0.33 R^2 cannot come from this.
  Mildest remedy: keep, and say in the Lines bullet that about 96 kept lines (1.9%) sit nearest another family.
  Option for the curator: drop those lines by the same label-free nearest-centroid rule the builder used.

2.3 P5 / target faithfulness (minor): the 56 lines with more than 13 plots are the QA's merges of duplicate entries.
  The definition reports the fact without the reason.
  Evidence (a5.py, merged_plots.csv): each of the 56 lines received plots that, in the original data.line, belong
  to another line of its family, which the QA then dropped.
  - For 51 of the 56, the closest such donor is a near-identical genotype: median discordance 2%, 44 under 5%.
    Random siblings differ at about 38%. So the QA merged one RIL entered under two or three names, a genotype-based
    step that does not use the label (it also removes copies across the split).
  - For 5 lines (DS11-08034, DS11-13054, DS11-22030, DS11-25068, DS11-40097), the only donor is genetically distinct
    (52 to 63% discordance). Their target pools the plots of two genotypes, unless my donor match by yield value is
    wrong for them.
  - Plot yields of the kept lines equal the original table's to +-1 kg/ha (a unit rounding), except 12 values.
  - The 28 pairs of lines with identical target values come from the same set of environments and the same integer
    yield sum: arithmetic, not a copy.
  Mildest remedy: one clause in the Target bullet ("the QA merged duplicate entries of one line; 51 of the 56 are
  near-identical genotypes"), and the 5 lines noted. Dropping those 5 lines is optional (0.1% of rows).

2.4 P7 / CLEAN-1 (quality, keep with note): heterozygosity outliers.
  Evidence (a1.py, a6.py): per line, heterozygous calls have a median of 3.7% and a 90th percentile of 9.1%. 201
  lines exceed 20% and 105 exceed 30%, with a maximum of 63%. RILs at this generation are expected near 6%, so these
  are outcrosses or mixed seed lots, which the source's QA kept. They are not tied to the target: r +0.02 between a
  line's heterozygous share and its deviation from its family mean.
  Mildest remedy: a note in the Features bullet. Whether an expert drops them is a question; I did not read the
  SoyNAM papers' filters.

2.5 Checked, no problem (no action):
  - Marker coding. The raw coding is one fixed allele per marker for every family, and IA3023 is homozygous at all
    4,312 QA markers (0 at 1,984, 2 at 2,328). The QA matrix codes IA3023's allele as 2: it flips exactly the
    markers where raw IA3023 = 0 (1,970 flipped above 99% agreement, 2,316 the same, and the 26 others at 98.5-99%
    because heterozygous calls agree under both). So raw and QA agree up to a per-column flip; the real difference is
    the QA's blanking (24.3% of cells missing in QA where raw has a call). The claim "recodes about half the markers"
    is confirmed, and that recoding alone would be harmless. The choice of raw stands on the blanking.
  - Heterozygous calls are 1, in the middle of the dosage (the additive coding). 5.30% of all cells, 5.39% of the
    calls. Claim 31 holds.
  - Missing calls. 1.52% of cells (claim 34 holds). By family, 0.16% to 3.2%, so the overall correlation of a line's
    missing share with the target (-0.14) is a family effect. Within families it is -0.01: not caused by the outcome.
    The leak probe's missing indicators reach at most R^2 0.014. A model sees NaN in a float column (native in tree
    models; the pipeline imputes otherwise).
  - Line QA. The 399 dropped lines are not cut on yield: their within-family deviation is +57 kg/ha mean (SD 373)
    against -4 (SD 248) for the kept lines, more spread in both directions, as off-types are. Together with the
    duplicate merges in 2.3, this is consistent with a genotype-based QA. The rule is not documented; the package help
    names only the marker QA.
  - Checks and parents: absent from the rows and from the target's environment fit. Environment, location, year,
    set and spot are absent from the features. NE_2013 has no yield.
  - Row order: the frame comes out of _clean sorted by strain (so by family); the v2 pipeline shuffles grouped data
    with seed 42 (CLEAN-23).

------------------------------------------------------------------------------------------------------------------
3. JUDGMENT RECORD
------------------------------------------------------------------------------------------------------------------
Verdict: ship. Optional: reword the notes.
Validity: USE-3 holds (genotype only). LEAK-10 holds (no field trait, environment or check ships). LEAK-33 holds
  (family is the group only). The target's environment fit over all lines is weak (Pearson +-0.0015 per fold), kept
  with a LEAK-30-style note. Doubtful family labels on about 2% of rows are noted.
Value: no column finding.
Quality: CLEAN-14 holds (dosage numeric, 0 dtype flags). CLEAN-2 holds (no imputation). CLEAN-5 holds (no constant
  or duplicate markers). CLEAN-1 note: 201 lines over 20% heterozygous.
For the curator:
  (1) the Note bullet's numbers per shipped fold, and the LEAK-30 wording;
  (2) whether to drop the about 96 off-type lines and the 5 lines merged with a distinct genotype (recommend keep,
      with notes);
  (3) whether an expert drops the high-heterozygosity lines (recommend keep, with a note).
```

</details>

<details><summary>Split audit</summary>

```text
SPLIT AUDITOR REPORT: genomic_prediction_soy_yield (2026-11-09)
Folder: datasets/_dev/tabarena-v0pt2/genomic_prediction_soy_yield/ (read-only; nothing edited, nothing built)
Scratch: the run's work files: work_split_auditor/ (load.py, structure.py, alt_splits.py, env_fit.py, offtype.py, parents2.py and their
CSV outputs alt_ridge.csv, alt_lgbm.csv, env_fit.csv). Frames from the definition through the workbench (the repository venv,
PYTHONPATH=src, thread caps 4). Splits: the shipped plan (3 repeats x 3 folds, 13 families per test fold,
1,660 to 1,775 test lines). Models: ridge with alpha = number of markers (GBLUP-like, mean fill from the training fold)
and untuned LightGBM (300 trees, lr 0.05). Score: pooled Pearson r per fold (the declared metric), plus mean
within-family r and R^2 for reading.

VERDICT: RIGHT WITH NOTES. Grouped by family is the regime the declared use case implies (USE-10 cold start: lines of
crosses never phenotyped, ranked before yield trials). The group id is the source's own family column (a true id,
SPLIT-24). The IID split (Azodi) answers another question: a family with phenotyped siblings. The notes concern what
the pooled r measures on held-out families and the noise that 13 families per fold leave. No note asks for a re-split.

------------------------------------------------------------------------------------------------------------------------
1. REGIME (SPLIT-1, SPLIT-5, SPLIT-29, USE-10): grouped by family holds. No action.

Alternatives scored (pooled r, mean over folds +- SD across folds):

  scheme                                        families/test fold  ridge            LightGBM         within-family r (ridge / LGBM)
  shipped grouped, 3 folds x 3 repeats          13                  0.529 +- 0.108   0.489 +- 0.096   0.261 / 0.205
  IID 3-fold x 3 (random lines)                 39                  0.733 +- 0.006   0.725 +- 0.007   0.286 / 0.264
  IID 80/20 x 5 (Azodi's protocol)              39                  0.740 +- 0.014   -                0.289
  shipped folds + 10 lines per test family      13                  0.652 +- 0.034   0.631 +- 0.039   0.273 / 0.222
    moved to train (first repeat)
  grouped 10 folds (about 4 families)           3.9                 0.501 +- 0.220   0.450 +- 0.210   0.269 / 0.198
  leave one family out (39 folds)               1                   0.282 +- 0.084   -                0.282

Reading:
* The IID advantage is all in the family means. Within-family r barely moves (ridge 0.286 IID vs 0.261 grouped);
  pooled r jumps from 0.53 to 0.73 because siblings in training give each test family its mean (builder: family-mean r
  0.98 IID vs 0.82 grouped). That is SPLIT-29's pattern: a shared entity carries the label, and a new cross does not
  have its siblings phenotyped. Azodi's random 80/20 (SPLIT-5) is a within-population design and does not fit the
  declared use case.
* The known-family case is real practice as well: phenotype some lines of a cross, then predict the rest (sparse
  testing). Ten phenotyped siblings per test family already lift ridge from 0.53 to 0.65. SPLIT-1 picks one regime,
  and the task_summary picks the new cross ("before field-testing the progeny of new crosses"), so grouped is
  consistent. If the curator prefers the known-family question, the use case text changes and the split becomes IID.
  The data cannot settle that; it is a framing choice.
* What a "new family" is: every family is a half-sib family through IA3023, and each founder appears in exactly one
  family. A held-out family is a cross whose second parent the training set has never seen, while the common parent's
  alleles are in every training family. That is the strictest form of "new cross". A program that reuses both parents
  across crosses would sit between the grouped and the IID numbers. The current wording ("a new cross with the
  program's common parent") says this correctly. An optional sentence for splits_comment: "each founder occurs in one
  family only, so a test family's second parent is unseen".
* There is no temporal axis: all lines were developed together and grown 2011-2013 in 18 environments, with no
  breeding cycles in the data. Not temporal; SPLIT-3 is not in play.

------------------------------------------------------------------------------------------------------------------------
2. WHAT IS KNOWN ABOUT A NEW GROUP (SPLIT-23; bears on USE-8 fit and on builder issue 4, MET-5/MET-10). Note for the
   curator, ranked first among the notes.

Pooled r on held-out families is mostly the ranking of the families, and one fact a breeder knows about a new cross
ranks them better than the genomic models: the founder parent's own yield. The parents are in data.check.qa (about 47
plots each, in the same trials). I took the founder of each family as the non-check strain grown only in that family's
sets (share 1.0 for 37 of 39 families; families 02 and 12 not matched), with its yield adjusted by the shipped
environment effects.
* r(founder value, family mean line value) = 0.933 over 37 families.
* A predictor that gives every test line its founder's value, with no genotype and no line-level information, scores
  pooled r 0.602 on the 9 shipped folds (0.30 to 0.72). That beats ridge (0.529) and LightGBM (0.489).
* Caveat: these parent yields come from the same 2011-2013 trials as the progeny, which is optimistic against a
  breeder's earlier records of a parent. Shipping them as a feature would be a contemporaneous field measurement
  (LEAK-10 territory), so I do not recommend shipping them.
What it means: the task is "genotype alone" (Azodi's genomic-prediction framing, consistent with the field). Its pooled
score rewards a model for rediscovering the family means from markers, which a breeder already has from the parents'
records. The split is not at fault. The question is what the score measures:
* Mildest remedy: keep the split. Say in fit_reason or curation_comments that the parents' own performance, known to a
  breeder, is left out on purpose (the genomic-only question). Carry these numbers into issue 4: a within-family r
  (`mean_group_pearsonr` on family) removes the family-ranking part that the parents' records dominate.
  Within-family r is also nearly insensitive to the split (0.26 grouped vs 0.29 IID).
* Founder type (elite / diverse ancestry / plant introduction) is known for a new cross and could ship as a feature
  without harm. The markers already carry it.

------------------------------------------------------------------------------------------------------------------------
3. FAMILIES PER FOLD AND FOLD COMPOSITION (weighed factor "only a few groups", splits.md; check warning
   groups_test_groups_few). Accept the warning; optional: stratify the folds.

* With 39 families and 13 per test fold, each family is scored 3 times over 3 repeats. Per-fold pooled r spreads
  widely: ridge 0.29 to 0.61 (SD 0.108), LightGBM 0.27 to 0.59 (SD 0.096).
* The spread follows the founder mix of the test fold. Fold pooled r correlates 0.78 with the SD of the test families'
  mean line values. Founder types come from the parent names (PI* = plant introduction: families 40, 41, 42, 48, 50,
  54, 64 = 7 PI families, mean line value 2,925 to 3,212 kg/ha against 3,603 to 3,954 for families 02-18). Repeat 1,
  fold 2 holds no PI family (test family-mean SD 129 kg/ha against 211 to 312 elsewhere). Its pooled r drops to 0.29
  (ridge) and 0.27 (LightGBM), and its LightGBM R^2 to -0.79.
* The model comparison survives the noise: ridge beats LightGBM on 7 of 9 shipped folds (mean difference 0.040, SD of
  the per-fold difference 0.045). Every fold scores 1,660 to 1,775 lines. The warning does not reflect a lack of
  units; it reflects composition variance, which the 3 repeats partly average out.
* More folds is worse here. Ten folds (about 4 families each) give 0.50 +- 0.22 per fold. Leave-one-family-out turns
  the pooled r into a within-family r (0.28) and changes what the metric means. Three folds with about 13 families is
  the right size for a pooled metric.
* Mildest remedy (optional, Should-level): balance the founder types across test folds. Ship a `founder_type` column
  (elite / diverse / PI, from Song et al. 2017 or the parent names; legitimate as a feature) and stratify the grouped
  folds on it (StratifiedGroupKFold path in data_foundry.v2.splits), so every fold holds 2 to 3 PI families. The
  cheaper alternative is 5 repeats instead of 3. Either way, accept groups_test_groups_few. The proposed acceptance
  text is fair; adding "per-fold pooled r spreads 0.29-0.61, driven by the founder mix of the test families" would
  make it complete.

------------------------------------------------------------------------------------------------------------------------
4. ENVIRONMENT EFFECTS FIT ON ALL LINES (LEAK-29 / LEAK-30 applied to the target). Weak, immaterial; keep the note,
   optionally update its numbers.

Yes, a test family's own plots enter the environment effects that its test target subtracts, and test families' plots
enter the training targets. Measured per shipped fold (env_fit.csv):
* Refitting the additive model on the training families alone moves the training targets by 4.1 kg/ha on average
  (after centring; at most 53 kg/ha on a line; target SD 359).
* Test targets recomputed with environment effects from the training side alone correlate 0.9999 with the shipped
  ones (mean shift 4.1 kg/ha, at most 21). Test targets from the test side's own fit correlate 0.9995.
* Ridge pooled r: 0.5294 on shipped targets, 0.5293 trained on training-only targets, and 0.5289 also scored against
  test targets from training-only environment effects.
No information crosses the split that a score can see. Every environment holds 24 to 39 families, so each fold's
training side always estimates every environment. The curation note gives the leave-one-family-out numbers (0.9 kg/ha
mean, 5.4 max). The leave-13-families-out numbers above are the ones that match the split. Optional: replace or add
them. No code change.

------------------------------------------------------------------------------------------------------------------------
5. OFF-TYPE LINES ACROSS THE SPLIT (LEAK-16 to LEAK-21 spirit, SPLIT-24). Negligible; no action.
67 of the 5,145 kept lines (by my nearest-family-mean genotype measure; the builder's measure gives 96) sit nearer to
another family's mean genotype than to their own: seed mix-ups or outcrosses whose family label is doubtful. Per
shipped test fold, 18 to 31 such lines (1.0% to 1.8% of the fold) appear, 10 to 23 of them with their nearest family
on the training side. The effect on the score is too small to measure. Optional filter: drop them. Not needed.

------------------------------------------------------------------------------------------------------------------------
Other checks, nothing found:
* Group id: the source's `family` (data.line.qa), constant per line, never a feature. The line id is dropped. No
  similarity cluster, no hash (SPLIT-24, SPLIT-26).
* One prediction is one line, scored per row, with no aggregation (SPLIT-23). That fits a breeder who selects lines.
* No exact genotype copies across the split (builder: 0 duplicates).
* Hidden-group probe: not needed; the task is already grouped on the finest true entity above the line.
```

</details>

<details><summary>Domain practitioner</summary>

```text
DOMAIN PRACTITIONER: genomic_prediction_soy_yield (2026-11-09)
Actor: a soybean breeder who has genotyped the recombinant inbred lines of new crosses and uses genomic prediction to
decide which lines go on to preliminary yield trials.

VERDICT
Fit: direct. The genotype is all I know of a new line before it is yield-tested, and an environment-adjusted mean over
many locations and years is the value I select on. A held-out family stands for a cross I have never phenotyped
(USE-1, USE-3, USE-8, USE-10).
Metric scores my decision: partly. Pooled Pearson r (Azodi 2019) mostly ranks families, and I already know family
ranks from the parents. Measured here: the founder parent's own yield, with no genotype and no model, gives pooled r
0.672, above every probe model on unseen families (LightGBM 0.536, ridge 0.572). I would pick models by
`mean_group_pearsonr` on `family`, the within-cross correlation (MET-1, MET-5, MET-10, MET-11 context).

NEW MEASUREMENT (scratch: work_domain_practitioner/pedigree_baseline.py, output pedigree_baseline.json)
The release grows each founder parent beside its family as a check (`data_check_qa`, about 48 plots per founder; 38 of
39 families have their founder). Each founder's value is its mean plot yield minus the environment effects of the
shipped line model, and each line is predicted by its mid-parent value, (founder + IA3023) / 2. No genotype and no
training labels are used.
  - r(founder value, family mean of the shipped target) = 0.927 over 38 families.
  - Pooled r of the mid-parent value with the shipped target: 0.672. The ceiling with the true family means is 0.726
    (between-family share of the variance 0.527).
  - By construction, the within-family r of a pedigree prediction is 0.
  - Compare the builder's grouped probes (within_family.json): pooled r 0.536 (LightGBM) and 0.572 (ridge); mean
    within-family r 0.210 and 0.267; family-mean r 0.816 and 0.821.
Caveat: the founders were grown in the same 2011-2013 trials as their progeny. In practice a parent's yield comes from
earlier trials, so 0.672 is somewhat optimistic. It is still the right order: parents are phenotyped before anyone
crosses them, and elite founders (the LD and LG lines, Magellan, Maverick) are released or advanced lines with known
yields.
This is a reading of the metric, not a leak. The founder's value is not a feature, and none should ship.

1. INPUTS AT THE PREDICTION POINT (USE-3, USE-6)
  - SNP dosage of the line (4,312 QA markers, raw 0/1/2, 1.5% missing): yes. I have this from seed chipping or a leaf
    punch before yield trials. Raw calls instead of the QA matrix are the right choice. I would never drop a parent's
    allele state just because it does not segregate within one cross.
  - No field trait of the line ships: correct for the genotype-only stage. An honest note: in a conventional soybean
    program, lines usually pass a progeny-row stage before preliminary yield trials, where I record maturity (R8),
    height, lodging and growth habit. If I applied genomic selection at the progeny-row decision, I would have R8.
    The shipped framing (genotyping before any field stage, i.e. rapid-cycle genomic selection) is the stricter and
    common one, so I accept it.
  - What I would always have and the table lacks: the pedigree, meaning which cross a line comes from, plus the
    parents' own performance and genotypes. For a new cross the family label is a new category, and its value lies
    in the parents' records. The markers carry most of this, since a line's genotype reveals its founder alleles.
    I do not ask to ship it: a concurrent founder yield would turn the task into a pedigree regression. Its absence
    is the reason the metric matters (section 5).

2. TARGET (USE-5; builder issue 1)
  - What I select on is the line's genetic value for yield across the target environments. In a two-stage genomic
    selection pipeline the evaluation phenotype is usually a BLUE or a de-regressed BLUP over environments. The
    shipped least-squares mean with fixed, centred environment effects in kg/ha is a standard choice, and I prefer it
    to a raw mean (r 0.970, a line ranked partly by where it was grown).
  - BLUE versus BLUP: r 0.9992, so it does not matter for a correlation metric. I select on BLUPs when lines have
    unequal testing, but as a benchmark target the unshrunk BLUE is fine. Xavier & Rainey (2019, G3, same population)
    used de-regressed BLUPs, which are close to BLUEs in scale. Recommend (a), as the builder does.
  - Expert note, not a blocker: SoyNAM spans late MG II to early MG IV. Line yield correlates with maturity at r 0.27
    pooled (0.22 within family), and the largest single marker (Gm19_40068456) sits in the chromosome 19 region of the
    known growth-habit and maturity genes. In a real program I compare yields within a maturity group or adjust for
    maturity, so part of the "yield" ranking is "lateness". The target as shipped is what a multi-environment trial
    reports, so I keep it. The note could name the maturity range.
  - Number, not class: correct. I rank lines, and a regression target with a ranking metric matches that.

3. ROW AND TEST DATA (USE-10, USE-11, SPLIT-5; builder issue 2)
  - One row per line equals one advance-or-drop decision: yes.
  - Grouped by family versus Azodi's random lines: grouped is my decision. When I genotype new progeny, none of their
    siblings has a yield record yet. Training on 80% of a family and predicting the other 20% (Azodi) needs
    phenotyped siblings of the same cohort, which I do not have at that stage. The random-split pooled r (0.72-0.73)
    with family-mean r 0.98 is the population-structure inflation the field warns about (Windhausen et al. 2012;
    Stewart-Brown et al.: a 0.60 yield accuracy "inflated by population structure"). Keep grouped, and accept
    groups_test_groups_few: 39 families is all the population has.
  - Two ways the test differs from what I would face, ranked:
    (a) Same seasons. All 39 families were grown in the same 2011-2013 environments (each family in 15-18 of 18), so
        training and test values average over the same environments. In practice the training set was phenotyped in
        earlier years and the candidates will be tested in later ones, so year-to-year genotype-by-environment
        interaction lowers my real accuracy. Every cross-validation genomic selection study shares this optimism,
        and it does not change the ranking task. Worth one sentence in `fit_reason` or the notes, not a move to
        approximate.
    (b) The held-out founder is always new. Each test family brings a founder no training family has, and 8 of 40
        founders are plant introductions. In my program most new crosses reuse elite parents that are already in
        the training set. The test is therefore harsher than mine on between-family prediction and about equal on
        within-family prediction. It argues again for scoring within families.
  - Off-type lines removed (builder issue 3): agree. I discard seed-mix off-types too, and a doubtful family label
    corrupts a family split. Recommend shipped.

4. WOULD I USE THIS MODEL?
  - Yes, as a culling tool before yield trials. A within-family r of about 0.2-0.3 on new crosses is useful for
    dropping the bottom half of each cross cheaply. It is in line with published soybean yield values (Stewart-Brown
    et al. 2019: 0.12-0.26 in an applied program).
  - Trust: positive within-family r on held-out crosses, stable over the 13 test families of a fold, and a pooled r
    that beats the mid-parent value.
  - Distrust: a model whose pooled r comes from family means (it tells me the founder is good, which I knew), or one
    whose top picks are simply the latest-maturing lines.

5. METRIC (MET-1, MET-2, MET-5, MET-7, MET-10, MET-11; builder issue 4)
  - Pooled Pearson r is scale-free and ranks lines. Its form is right for a selection decision, and no k or selection
    intensity is fixed by the source, so no top-k metric applies (MET-7).
  - The unit is not right. My decision at this stage is which progeny of each cross to advance. The cross means are
    largely known from the parents (founder vs family mean r 0.927; mid-parent pooled r 0.672). Pooled r is about
    half between-family variance (0.527 share), so it ranks models largely by how well they rediscover the founder's
    merit. Predicting cross means from markers is a real but different decision: which crosses to make, taken before
    the progeny exist, from the parents' genotypes.
  - The source's claim is weakened (MET-2, third bullet; MET-10 "whether our task is still the source's"). Azodi
    chose pooled r deliberately (MET-5) but on random lines. On our grouped split it measures something else.
  - What I would declare: `mean_group_pearsonr` with group `family`, origin context, naming Azodi's pooled r as the
    overruled original (MET-11 context, amended 2026-11-03). It follows the protein_model_quality_rf_pcp and
    huesken_sirna_efficacy precedents (MET-5 exceptions, 2026-11-04), where a group's mean rewarded by the pooled
    score was the argument.
    MET-2 check: the group column is the task's own, and the metric reads it there. Each test fold holds about 13
    families of 98-140 lines, so each within-family r has an SE of about 0.085, and the fold mean about 0.025. That
    resolves the probe gap (0.210 vs 0.267).
    The two metrics rank the two probe models the same (ridge > LightGBM).
  - If the curator keeps pooled r: name in the notes that the between-family part is available from the parents
    (pooled r 0.672 with no genotype) and that within-family r is the selection-relevant part. "Partly" then stands.
  - Builder's counter-argument (a breeder ranks several crosses together, so pooled r fits): only half true. I
    truncate across crosses, but I would make that across-cross part of the ranking from the parents, with or without
    genomics. What genomics adds at this decision is the within-cross ranking.

GAPS, RANKED BY HOW MUCH THEY CHANGE THE TASK
  1. The metric's unit: pooled r scores mostly between-family ranking, which the mid-parent value already gives (0.672
     vs model 0.57). Fix: mean_group_pearsonr on family.
  2. Train and test share the same environments and years, so there is no year-to-year transfer. Cannot be fixed with
     a line-level target. Name it in the notes.
  3. Every test family has a founder never seen, harsher than a program that reuses elite parents. Acceptable, and it
     supports fix 1.
  4. Maturity confounds yield (r 0.27). Name the maturity range in the notes.
  5. Target construction (BLUE vs BLUP vs mean): negligible for the metric (0.9992). Ship (a).

WHAT AN EXPERT WOULD CHANGE
  - Score within-cross correlation (mean over families), or at least report it beside pooled r.
  - In the notes: the cross means are known from the parents, the train and test seasons are shared, and the panel's
    maturity range (late MG II to early MG IV) correlates with yield.
  - Keep: the grouped family split, raw marker calls, QA lines, the environment-adjusted BLUE in kg/ha, and no field
    traits.

SOURCES
  - SoyNAM 1.6.2 help pages (man/soynam.Rd: population, 40 founders, 17 elite, 15 diverse, 8 PIs, MG II-IV, the check
    tables).
  - Builder report and probes/within_family.json, probes/target_options.json.
  - Own scratch measurement: the run's work files: work_domain_practitioner/pedigree_baseline.{py,json}.
  - Xavier & Rainey 2019, Quantitative Genomic Dissection of Soybean Yield Components, G3 (within-family,
    across-family and leave-family-out schemes on SoyNAM; de-regressed BLUPs; predictive ability = correlation):
    https://pmc.ncbi.nlm.nih.gov/articles/PMC7003100/
  - Stewart-Brown et al. 2019, Genomic Selection for Yield and Seed Composition Traits Within an Applied Soybean
    Breeding Program, G3 (yield predictive ability 0.12-0.26; a 0.60 cross-validation accuracy "inflated by
    population structure"): https://www.ncbi.nlm.nih.gov/pubmed/31088906,
    https://data.soybase.org/annex/Glycine/max/meetings/world_soybean_research_conference/10/abstracts/abstract-page318.pdf
  - Windhausen et al. 2012, G3, via Werner et al. 2020, Front. Plant Sci. (predictive ability driven by
    population-means differences; among- vs within-family accuracy measure different things):
    https://www.frontiersin.org/journals/plant-science/articles/10.3389/fpls.2020.592977/pdf
  - Rules: use_case.md USE-1, USE-3, USE-5, USE-6, USE-8, USE-10, USE-11; metrics.md MET-1, MET-2, MET-5, MET-7,
    MET-10, MET-11 (and the protein_model_quality_rf_pcp / huesken_sirna_efficacy cases); splits.md SPLIT-5,
    SPLIT-29.
```

</details>

<details><summary>Blind review</summary>

```text
BLIND REVIEW: genomic_prediction_soy_yield (SoyNAM soybean grain yield from SNP markers)
Reviewer worked only from clean_room/ (data.parquet, task.md) and public web pages. No other local file was opened.
Scratch scripts: work_blind_reviewer/m.py, d.py, e.py, f.py

VERDICT
Include with changes. It is a real genomic-selection task with real signal, but the provenance of the target needs fixing, `family` must not be used as a feature, and the leave-family-out score has high variance and mostly measures family means.

WHAT THE TASK IS
- 5,145 soybean recombinant inbred lines (RILs) from 39 SoyNAM biparental families. All families share the parent IA3023.
- Features: 4,312 SNPs coded 0/1/2 with 1.5% NaN, plus `family` (categorical with 39 levels).
- Target: grain yield in kg/ha (mean 3,600, sd 359, range 1,961 to 4,614).
- Use: a soybean breeder predicts the yield of new lines from their genotypes before or instead of multi-environment field trials, then decides which lines to advance. This is standard genomic selection and a real use.
- Under leave-family-out, the question is: "predict the progeny of a cross with no phenotyped siblings". That is a legitimate and harder breeding question.
- The 4,312 markers equal the SoyNAM "quality-assured" set. kg/ha is the unit the SoyNAM R package uses, the family numbering (02..64) matches SoyNAM, and heterozygosity is about 5% (median 3.7%), as expected for F5-derived RILs. The data look real, not generated.

CONCERNS, MOST TO LEAST SERIOUS

1. Provenance: the linked source does not match the data, and how the target was built is undocumented.
   Evidence:
   - The links (Azodi et al. 2019, G3; Dryad/Zenodo xksn02vb9) describe the soy set as 5,014 lines and 4,240 markers. Quoting the paper: "Phenotype values were normalized between 0 and 1", and markers were coded "[-1,0,1]" with missing values "already dropped or imputed by the original authors".
   - This table has 5,145 lines, 4,312 markers, raw kg/ha, 0/1/2 coding and 337k NaNs. So it was not built from the linked Dryad files. It most likely comes from the SoyNAM CRAN package (gen.qa has 4,312 markers; "yield (grain yield in Kg/ha)").
   - Whether the target is a BLUP, a check-adjusted mean, or a raw mean, and over which environments, is not stated.
   - The values show structure: only 965 distinct fractional parts across 5,145 targets. One offset (.360750) appears on 42 lines from different families. There are 23 exact duplicate target values between genetically unrelated lines (marker identity 0.41 to 0.58, mostly in different families), and pairs differ by exact amounts (3028.693134 vs 3104.693134). This looks like raw plot yields plus a shared per-set or per-environment adjustment, not an lme4 BLUP, and it suggests many lines rest on few plots.
   Change: cite the SoyNAM dataset (Xavier et al. 2016; the SoyNAM R package / SoyBase) as the source. Document the exact target derivation: which function, which environments, whether check-adjusted, and the number of plots per line. Prefer a multi-environment adjusted genetic value (BLUE or deregressed BLUP).

2. The `family` column is in the feature table, and the split holds out whole families.
   Evidence: every test family is a level never seen in training, so the feature carries no information at test time. Some pipelines crash or behave oddly on unseen categories. In a random split it would be a strong shortcut: family means alone give R2 = 0.527, against 0.54 for ridge with a random 3-fold split.
   Change: keep `family` only as the grouping variable and drop it from the features.

3. The leave-family-out score is dominated by about 13 family means per fold and is very noisy.
   Evidence (ridge on mean-imputed SNPs, 3 group folds, 3 seeds):
   - Fold R2 values: 0.457, 0.197, 0.291 / 0.116, 0.305, 0.272 / 0.062, 0.196, 0.243.
   - Replacing each prediction by its predicted family mean gives almost the same R2 (0.431, 0.196, 0.286, ...). So nearly all of the scored R2 comes from ranking families, and within-family prediction adds almost nothing to R2. The within-family Pearson r is only about 0.25.
   - Fold R2 swings with how many of the six low-yield exotic families (40, 42, 48, 50, 54, 64; family means 2,925 to 3,212 against about 3,650 for the rest) land in the fold. Folds with none of them score R2 0.06 to 0.12.
   - The effective sample size for the dominant signal is 39, not 5,145.
   Change: stratify the family-to-fold assignment by parent group (elite, diverse, exotic) or use more repeats (for example 5x5 group folds), or report within-family correlation as well. Alternatively, add a random (within-family) split variant, which is the scheme most SoyNAM genomic-selection papers report. The task then becomes stable (R2 about 0.53 to 0.55 for ridge and LightGBM), but most of that comes from family identification.

4. Genotype quality artifacts are left in.
   Evidence:
   - Per-row NaN count ranges from 0 to 1,207 (median 27). It correlates with yield at Spearman -0.30, but only at family level: within families the median is -0.01, and exotic families have more failed calls (109 vs 20 to 40 NaN per line). A NaN-count-only model does not transfer across families (R2 -0.57 to 0.01), so this is not leakage.
   - 219 lines have heterozygosity above 0.2 (max 0.71), which is implausible for F5 RILs. These are likely outcrosses or seed mixtures, concentrated in family 25 (24 lines).
   - 65 within-family pairs have genomic correlation above 0.95 (near-identical sibs or duplicates). They stay within one family, so they cannot leak across a group split.
   Change: either document these lines or apply the usual QC (drop lines with more than 20% missing or high heterozygosity). Keep the NaNs as NaN. That is fine for tree models, and the 0/1/2 numeric coding is appropriate.

5. Mild cross-row dependence in the target.
   If the target is an adjustment or BLUP fitted on all lines jointly (shared check covariates or set effects), test-family targets were computed with training rows in the same model. The effect is small and does not use markers, so it is not leakage of the genotype-to-phenotype map, but it should be stated.

6. Benchmark overlap (minor).
   arXiv 2609.07441 ("TabBench-Bio", 43 high-dimensional biomedical datasets) is linked. I could not confirm that it contains this table. If it does, note the overlap. It is not a reason to exclude.

IS IT WORTH BENCHMARKING
Yes. There is clear signal: grouped ridge R2 about 0.31 on the seed-0 split, LightGBM about 0.27. The task is not trivial, and with p ≈ n (4,312 SNPs, 5,145 rows) it is a useful high-dimensional regression case where linear and kernel methods are hard to beat. The size is adequate, but the grouped score is noisy (concern 3).

TIMING AND HONESTY
All features (genotypes) are known before the field trial, so nothing in X is known only after prediction time. The only temporal or structural issue is the family column (concern 2). There are no exact duplicate rows, no duplicate genotypes, and no genotype pairs with correlation above 0.9 across families.

WHAT I COULD NOT CHECK
- The exact pipeline that produced `yield_kg_ha` (BLUP vs mean, which environments, plots per line).
- Which SoyNAM family is missing (40 exist; 39 are present here) and why.
- Whether lines were filtered.
- The contents of the Dryad README and whether TabBench-Bio includes this exact table.
- Whether the benchmark harness drops the group column from the features.
```

</details>

<details><summary>Task gamer</summary>

```text
Task gamer report: genomic_prediction_soy_yield (SoyNAM, 5,145 RILs x 4,312 SNPs, 39 families, grouped 3x3 CV, pooled Pearson)

VERDICT: Hard to game. No leak in the features, row order or copies. The only gain comes from statistics of the test batch:
rebuilding the held-out families by clustering their genotypes, then averaging predictions within each family. It adds
about +0.02 on ridge and +0.05 on LightGBM, varies widely by split, and drops some splits below the baseline.

HONEST BASELINES (9 shipped splits, score.py)
  LightGBM, untuned (work/baseline.py)                     mean 0.472  (0.250 - 0.586)
  Ridge on mean-imputed SNPs, alpha=3000 (work/baseline.py) mean 0.536  (0.300 - 0.611)  <- better honest model
  Ridge + one column of random numbers (work/exploits.py)   mean 0.535; change from ridge -0.0023 to +0.0006 per split

EXPLOITS RANKED BY GAIN
| # | Exploit | Script | Honest | Exploited | Gain per split (range) | Deployed model has it? | Fix |
| 1 | Rebuild test families from test genotypes (kNN-cosine spectral clustering on minor-allele indicators, ARI 0.82-0.98), then pred = family mean of pred + w*(pred - family mean); w=0.2-0.5 chosen by inner CV on training families | work/famclust.py; LightGBM: work/nn_and_lgbm.py (w fixed at 0.35) | ridge 0.536 / LGBM 0.472 | ridge 0.552 / LGBM 0.526 | ridge +0.017 (-0.039 to +0.088); LGBM +0.055 (-0.011 to +0.130) | Partly. A breeder knows a line's family and usually genotypes the sibling lines together. The task sets group context to "none", so under its rules this is a test-batch statistic | Say in the task whether family/cohort context is allowed. If it is not, score one family at a time or say that batch statistics are not allowed. Using the true family labels gives the ceiling: +0.027 (-0.041 to +0.089) |
| 2 | Family-mean missing-call count from the rebuilt test families as a second-stage feature | work/nanfam.py | 0.536 | 0.548 | +0.013 (-0.047 to +0.053) | No (aggregates test rows). The per-row count, which a deployed model does have, gains nothing: -0.0001 (-0.009 to +0.009), work/nanrow.py | Same as #1. Optionally drop or impute the missing calls at the source |
| 1+2 | Both, in one second-stage linear model | work/combined.py | 0.536 | 0.553 | +0.017 (-0.055 to +0.076) | No | As #1 |

Mechanisms
1. The pooled Pearson over 13 held-out families is mostly between-family variance: family explains 53% of yield
   variance. Averaging about 130 sibling predictions gives a less noisy estimate of each family's mean, and shrinking
   the within-family part (w around 0.35) puts more weight on the more accurate between-family component. The
   families are easy to recover: all 39 crosses share the IA3023 parent, so a line's founder-specific (minor) alleles
   mark its family.
2. The missing-call rate depends on the family. Exotic-founder families have more failed calls, and the family mean of
   the missing count correlates with family mean yield (Spearman -0.51, p=0.0009, n=39). Per row it adds nothing. Only
   the average over a test family's rows adds a small, noisy signal.

FLAWS THAT HURT AN HONEST MODEL
None that an honest training choice fixes. The label has an observation: the target is not a clean genetic value.
y*10 mod 1 takes about 700 distinct values, and the 276 groups with 5 or more rows share an identical fractional
offset (for example 0.36075, 0.96075 and 0.76075 all end in .x6075). These groups look like environment-set or trial
adjustments. They explain 26% of the yield variance and cut across families: on average a family's largest offset
group holds only 27% of its lines. A deployed model trained on trial records would know the environment set. I
estimated the effects of these groups on the training rows and removed them from the training target
(work/envset.py). Score: 0.526 vs 0.536 (-0.032 to +0.007), so it does not help. The groups add noise to the test
labels that no genotype model can predict. The mildest fix is a target adjusted for environment (BLUE/BLUP across
environments), not a raw per-set mean.

ATTACKS THAT FOUND NOTHING
- Row order: Spearman(y, row position) = -0.015 (p=0.28). Lag-1 autocorrelation of y = -0.006; within-family residual
  lag-1 = -0.006. Neighbouring rows share a family 2.5% of the time (random).
- Exact copies: no duplicated genotype rows. Near copies: no cross-family near-duplicates (smallest cross-family NN
  distance 41.5; median NN distance 60). As predictions, the nearest training row's label gives 0.116 and the mean of
  the 10 nearest gives 0.239, both far below the baseline.
- Formats: SNPs are only {0,1,2,NaN}, with no non-integer values, scaling or transforms over all rows. Missing calls
  are 1.5% of the cells. Missing indicators added to ridge: 0.537 (+0.0016, -0.001 to +0.005), within the noise. The
  missing count added to ridge: 0.537 (+0.001), noise. Per-row heterozygosity vs within-family residual: Spearman
  0.026, p=0.06.
- Target format: the fractional offset groups (see above) are visible only in y. No feature predicts them, and
  denoising the training target costs 0.010.
- Family composition: family size vs family mean yield, Spearman 0.22 (p=0.17), nothing. The family number correlates
  -0.76 with family mean yield (the high-numbered families have exotic founders), but the group column is not a
  feature. The founder information enters honestly through the genotypes.
- Train/test shift: by design (grouped split). No feature identifies the split.
- Web: Azodi et al. 2019 (G3), Dryad/Zenodo 4980429, Xavier & Rainey 2020. No forum, "leak" or "magic feature" thread
  exists for this source.
- Lookup in the published file (not ranked): it works partly. 4,762 of the 5,145 rows match the Zenodo soy_geno.csv
  with confidence after flipping alleles per SNP (work/lookup.py). The published YLD there is a different, normalized
  yield (r=0.64 with the kit target). As a prediction it scores 0.583.
- Kit vs source: the kit has 5,145 lines and 4,312 SNPs with missing calls kept; Azodi has 5,014 lines and 4,234
  imputed SNPs. The yield is in raw kg/ha with trial-set offsets, so the kit seems built from the SoyNAM release, not
  from Azodi's file.

NOT CHECKED
- Stronger honest models (tuned GBLUP or ridge alpha, BayesB). The exploit gains may shrink against them.
- Whether the shipped folds balance elite and exotic families. The r1f2 fold is weak for every method (0.25-0.30).
- The original SoyNAM environment and year records, which would confirm that the fractional-offset groups are trial
  sets.
Sources: https://academic.oup.com/g3journal/article/9/11/3691/6026746 ; https://zenodo.org/records/4980429 ;
https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7003100/
```

</details>

<details><summary>Precedent check</summary>

```text
PRECEDENT CHECKER: genomic_prediction_soy_yield (panel of 2026-11-08, written 2026-11-09)

Read: principles.md, metrics.md, splits.md, use_case.md (USE-4/5/11), leak_checks.md (LEAK-29/30 and cases),
provenance.md (PROV-8/9/10), cleaning_features.md (CLEAN-1/2/7/8/11), task_probes.md (TP-6/7), definitions.md
("Groups"), review_file_format.md; the definition, the record, builder_report.md, the probes (target_shipped.json,
target_options.json, within_family.json), domain_practitioner and column_auditor reports, register.json (5,160
decisions, 35 flags). The claim and split auditors' reports did not exist when this was written.
No curator decision on any genomic-prediction dataset exists: the three Azodi siblings (maize, rice, switchgrass) are
AI screenings only (TBD -> 2nd Tier, 2026-10-31). So the precedents below are by mechanism, not by family.

SUMMARY (per decision)
  D1 Target = least-squares mean (BLUE) in kg/ha ......................... consistent (USE-5, TP-7); see note on TP-6
  D2 One row per line, plots averaged ...................................... departs from SPLIT-26 / superconductivity
                                                                              and boreal (2026-11-08) WITH a fact from the
                                                                              data; not yet written as an exception
  D3 Environment effects fit on all lines, kept with a note ............... departs from sf_permit_time / home_credit
                                                                              (2026-10-19: our own all-row computation is
                                                                              fixed when a fix exists); a fold-free fix
                                                                              exists (check-adjusted, r 0.9991): PROMPT 1
  D4 Grouped by family over Azodi's random lines ......................... consistent (huesken, superconductivity,
                                                                              airfoil; set apart from sarcoma)
  D5 groups_test_groups_few accepted ...................................... consistent (airfoil, open_university,
                                                                              heart_disease, huesken); wording nit
  D6 grouping.context = "none" ............................................ departs from protein_model_quality_rf_pcp
                                                                              and huesken (2026-11-05) WITHOUT a reason:
                                                                              PROMPT 2
  D7 QA lines, raw calls of the QA markers ................................ consistent (CLEAN-1 ashrae; PROV-13 coad;
                                                                              LEAK-19 for the merged duplicates)
  D8 Metric pooled pearsonr (source) vs mean_group_pearsonr (context) .... pooled: consistent with MET-5 but a real
                                                                              pair with protein / huesken decided the
                                                                              other way: PROMPT 3. Within-family: third
                                                                              case of that reason -> amendment due
  D9 Year 2015 (definition) vs 2019 (record) .............................. definition consistent (PROV-9, airfoil,
                                                                              tully_fisher, nikuradse, eucalyptus);
                                                                              record departs without a reason: fix record

------------------------------------------------------------------------------------------------------------------
D1. TARGET: BLUE vs package BLUP() vs plain mean (USE-5 Must, TP-7 Must; builder issue 1)
------------------------------------------------------------------------------------------------------------------
Precedents: USE-5 cases (corporate_credit_rating 2026-10-16, cirrhosis, diabetes_3 2026-10-21) are about labels the
source shipped; none is a line value we estimate from repeated plots. TP-7 ("when the definition builds the target
itself, use an established convention, test each candidate"; audiology_diagnosis). Tension row "repair against
cleaning around damage" (coad, corporate_credit_rating, SUPPORT2, ashrae): repaired from origin.
Comparison: the build follows TP-7 (two-stage BLUE is the field's convention, the domain practitioner confirms; four
candidates tested: mean r 0.970, BLUP 0.9992, check-adjusted 0.9991) and PROV-13 (Azodi's standardized YLD of
undocumented construction replaced from the origin, unlike diabetes_3, where no origin existed and the label shipped
`approximate`).
Note for the curator (not a departure): the tension row "a better version against our own fix" (eryhemato; TP-6) says
"a version the source defines replaces ours". The package's `BLUP()` is a tool the data owners ship, so a reader could
call it the source's own version. What sets it apart, stated in the definition and builder report: TP-6 speaks of a
stage the source describes, not an estimator; the package's check covariate is degenerate (`spot` constant within an
environment); BLUP shrinks by the number of plots; r 0.9992, so the metric does not move. BLUE is an established
convention, not "a fix of our own invention". Consistent; the Target bullet already gives the reasons.

------------------------------------------------------------------------------------------------------------------
D2. UNIT: one row per line instead of the source's plot rows (SPLIT-26 Should, MET-17 Should; USE-5 Must)
------------------------------------------------------------------------------------------------------------------
Precedents:
  - superconductivity, CC 2026-11-08 Lennart (curation/records/superconductivity.md; metrics.md Cases): inputs equal
    within a composition, entries kept, each composition counted once by `composition_weight`: "Every entry is still
    kept (SPLIT-26)".
  - boreal_postfire_lichen_biomass, 2026-11-08 Lennart (metrics.md Cases, MET-17): quadrats kept, `plot_weight`.
  - SPLIT-26: "Keep the source's rows: deduplicating with averaged targets is a different dataset."
Comparison: the same facts as superconductivity on one axis (a line's plots have identical inputs, the genotype; the
actor decides once per line), decided the other way (the plots are averaged into one row). A fact sets the case
apart, evident from the data and stated in the builder report's Unit bullet: each plot carries an environment effect
of -1,252 to +1,471 kg/ha (target SD 359) that is not an input, and lines saw 1 to 16 of 18 environments, so a plot
row's target is mostly the environment, and the plot framing with the environment as input is the G x E task (another
task). SuperCon entries carry no measured covariate of that kind. The higher rule served is USE-5 (P3, Must: the
line value is what selection acts on). Also, the task's source (Azodi) and the field ship one value per line.
Verdict: departs with a stated reason; reasonable (a Should yielding to a P3 Must). It is not written as an exception,
and the definition does not cite SPLIT-26. First exception to SPLIT-26, so no amendment is due.
Proposed record text (for the curator to confirm):
  **Exception to SPLIT-26 (2026-11-xx, Lennart):** the source's plot rows are averaged into one line value, since each
  plot carries an environment effect (-1,252 to +1,471 kg/ha against a target SD of 359) that is no input at the
  prediction point and lines saw 1 to 16 of 18 environments; unlike superconductivity's entries, the repeats differ by a
  measured condition. Serves P3: the line value is what selection acts on.

------------------------------------------------------------------------------------------------------------------
D3. ENVIRONMENT EFFECTS FIT ON ALL LINES, test families included (LEAK-29 Must by analogy, LEAK-30)
------------------------------------------------------------------------------------------------------------------
Precedents:
  - LEAK-29 cases, 2026-10-19 Lennart: sf_permit_time `DescriptionIsStandardPhrase` (recomputed on the history before
    the oldest test window) and home_credit_default_risk `NEW_INC_BY_ORG` and a mean fill (dropped). Our own cleaning
    computed a value over all rows: fixed, whatever the size.
  - principles.md tension row "a weak transductive leak against the data as published": "fix it when we can";
    sf_permit_time and home_credit fixed, "the rest kept with notes" (source transforms with no raw values).
Comparison: here the all-row computation is ours, as in sf_permit_time and home_credit, and a fix exists: the
check-adjusted mean (each plot minus its environment's mean over the check and parent plots, `data_check_qa`, which
holds no line of any fold) correlates 0.9991 with the shipped target (probes/target_shipped.json; scripts/
target_shipped.py, lines 30-33). The definition keeps the all-line fit with a "Note:" bullet.
Facts offered for the difference: LEAK-29 speaks of a feature, and this is the target; the effect is measured as
negligible (column auditor, 9 shipped folds: honest vs shipped test targets r 0.99973-0.99996, ridge Pearson moves by
-0.0014 to +0.0015); no channel exists (no environment among the features). These are size arguments plus the
feature/target wording; sf_permit_time and home_credit were fixed without a size test.
Verdict: departs from the closest precedents; the stated reason is size, not a fact that the precedents lacked, and
the available fix was not weighed. Not a break of a Must (LEAK-29's text covers features). PROMPT 1 below.

------------------------------------------------------------------------------------------------------------------
D4. SPLIT: grouped by family over Azodi's random 80/20 (SPLIT-1, SPLIT-5, SPLIT-29 Must; builder issue 2)
------------------------------------------------------------------------------------------------------------------
Precedents, followed:
  - huesken_sirna_efficacy (Lennart 2026-11-04, splits.md "Few groups"): the source's random flags discarded for
    gene-held-out folds (SPLIT-4, SPLIT-5).
  - superconductivity (2026-10-06, SPLIT-4): grouped by composition though a random split cost at most 0.009 R^2.
  - airfoil_self_noise (Lennart 2026-10-20, SPLIT-1): grouped by setup.
  - SPLIT-5 cases (appliances_energy_prediction, kick): a prescribed split is a claim.
Precedents decided the other way, and what sets soy apart:
  - sarcoma (Lennart 2026-10-22, SPLIT-29/31): IID by patient kept, because new patients come from the same tissue
    sites. A new cross is by definition a family with no phenotyped sibling (domain practitioner: "none of their
    siblings has a yield record yet"), and the family carries the label (52.7% of the variance between families; IID
    family-mean r 0.98 vs 0.82 grouped).
  - amazon_employee_access (SPLIT-31): IID kept as the task's framing. Here the use case names the new cross.
Verdict: consistent. No drift in Lennart's SPLIT-29/31 calls (sarcoma 2026-10-22 and huesken 2026-11-04 both decided
by the use case).

------------------------------------------------------------------------------------------------------------------
D5. groups_test_groups_few accepted (definitions.md: "accept only with group_probes evidence")
------------------------------------------------------------------------------------------------------------------
Precedents: airfoil_self_noise (33 setups, 11 per fold, 2026-10-20), open_university_learning_analytics_dataset (22,
6-9 per fold), heart_disease (3 hospitals, 2026-10-27), huesken_sirna_efficacy (30 genes, 10 per fold; Myunghwan
2026-10-26, reworded Lennart 2026-11-04: "not a general license for few groups, the signal across groups is
measured"). Soy: 39 families, 13 per test fold, 1,660-1,775 lines per fold, group probes run: more groups per fold
than any precedent. Consistent.
Wording nit (not a departure): airfoil and open_university name all four model families of group_probes.py; the
proposed text names LightGBM (0.148) and random forest (0.026) only and leaves out kNN (-0.108) and the untuned ridge
(-2.479). Name all four, with the tuned ridge (pooled r 0.57) as the reason the linear score is no verdict
(SPLIT-27), as the builder report does.

------------------------------------------------------------------------------------------------------------------
D6. grouping.context = "none" (SPLIT-23 Must; definitions.md "Groups")
------------------------------------------------------------------------------------------------------------------
Precedents:
  - protein_model_quality_rf_pcp, CC 2026-11-05 Lennart: `context="all_rows"`, "the researcher holds all of a
    target's candidates when ranking them"; it changed a panel's `none`.
  - huesken_sirna_efficacy, CC 2026-11-05 Lennart: `context="all_rows"`, reopened to follow protein; "the context
    follows the use case, not the gain" (context added nothing measurable there); "The 2026-11-04 `none` was a panel
    choice, not a curator call."
  - sat11_hand_algo_runtime, open_university_learning_analytics_dataset: `all_rows`.
  - definitions.md: "`all_rows` when all rows of a new group are known when predicting".
Comparison: the breeder genotypes the progeny of a new cross together and knows which lines are siblings (the domain
practitioner names the pedigree as information "I would always have"); the definition's own text says "Genomic
selection ranks the progeny of new crosses before they are phenotyped". That is the protein/huesken fact. The
definition gives no reason for `none` ("Each line is one prediction" is the prediction unit, which stays `row`).
Verdict: departs without a reason, from a decision Lennart made twice on 2026-11-05 and called a panel default the
first time. PROMPT 2 below. It holds under either metric (D8).

------------------------------------------------------------------------------------------------------------------
D7. QA LINES AND RAW MARKER CALLS (CLEAN-1, CLEAN-11, PROV-13, LEAK-30, CLEAN-2; builder issue 3)
------------------------------------------------------------------------------------------------------------------
  - Lines: the data owners' QA phenotype table (5,145 of 5,544 genotyped lines). CLEAN-1 "read what the data owners
    did (removed anomalies, a published list of bad rows), adopt the rules that hold for train and test alike"
    (ashrae_great_energy_predictor_iii, 2026-10-15). The QA is label-free (column auditor: dropped lines' within-family
    deviation +57 kg/ha, SD 373, more spread both ways, not a cut on yield) and merges duplicate entries of one RIL
    (51 of 56 near-identical genotypes: copies, LEAK-19). Consistent. A note on CLEAN-11 ("a row leaves only when it
    is no task row or a copy"): 154 of the 399 dropped lines are off-types whose family (the split key) is doubtful;
    the reason for the other 245 (family 46 whole among them) is the owners' undocumented QA. Say in the Lines bullet
    that the rule is the owners' and partly undocumented; no departure.
  - Markers: raw 0/1/2 calls of the owners' QA marker set (selection by missingness and segregation: label-free,
    CLEAN-8), not the QA matrix, which blanks markers not segregating within a family (25.6% of cells). Follows
    PROV-13 and LEAK-30's "rebuild from the unprocessed values when the source has them" (coad_colon_adenocarcinoma,
    rebuilt from the GDC per-sample files, 2026-10-16). Missing calls kept (CLEAN-2). Consistent.

------------------------------------------------------------------------------------------------------------------
D8. METRIC: pooled pearsonr (Azodi) vs mean_group_pearsonr on family (MET-1, MET-2, MET-5, MET-11; builder issue 4)
------------------------------------------------------------------------------------------------------------------
Precedents:
  - Kept a paper's one deliberate criterion (MET-5): forest_fires (MAD, 2026-10-21), labour_inspection_compliance,
    open_soil_spectral_library (tuning RMSE on log1p, Lennart 2026-11-04/05). Azodi names r as the criterion it
    compares models by ("the standard metric for GP performance"; MSE only for tuning): one deliberate choice.
  - Exceptions to MET-5, 2026-11-04 Lennart: protein_model_quality_rf_pcp ("the use case ranks one protein's
    candidates and pooled RMSE rewards a protein's typical quality"; each protein's true mean beats LightGBM) and
    huesken_sirna_efficacy ("the use case ranks guides within a gene and pooled RMSE rewards a gene's mean"; recorded as
    "the second exception of this kind"). Both declared `mean_group_pearsonr` from context IN PLACE OF THE FALLBACK
    (several metrics reported, no unique original).
  - numerai_v5_2_1m (2026-10-21): per-era CORR replaced pooled pearsonr, the competition's own metric (MET-4), so a
    different route.
  - superconductivity (Lennart 2026-11-08): a paper's deliberate per-entry RMSE overruled on the unit the scientist
    decides on (MET-1, MET-17, context). Reason: one vote per unit, now its own rule (MET-17).
Comparison with protein/huesken, the facts that matter:
  - Same: the pooled score is largely a group-mean score (52.7% of variance between families); a group-level baseline
    outside the features beats the models (mid-parent value pooled r 0.672 against LightGBM 0.536 and ridge 0.572,
    domain practitioner, with the caveat that founders were grown in the same trials), as each protein's true mean beat
    LightGBM; the group column is the task's own, so MET-2's metric input is met (blogfeedback, sat11).
  - Different (a): Azodi has one deliberate metric; protein/huesken had none, and the context metric replaced RMSE,
    the fallback. Overruling Azodi needs MET-2 (third bullet: our grouped split changed what pooled r measures: under
    Azodi's random split it is mostly the siblings' family means, r 0.98) or MET-1 (the unit), via MET-11 context as
    amended 2026-11-03 (a source metric overruled). That is a stronger step than the first two cases.
  - Different (b): CASP and siRNA design rank within a group only; a breeder truncates across all crosses of a cycle
    (builder) but takes the across-cross part from the parents (domain practitioner). The fact is disputed between
    the two panel reports; neither is a curator call.
Verdict, keeping pooled r (the definition now): consistent with MET-5, but the closest precedents on the mechanism
went the other way; fact (a) is a real difference and (b) is disputed. PROMPT 3 below.
Verdict, switching to mean_group_pearsonr: the third case where a pooled score that rewards group means is replaced by
`mean_group_pearsonr` from context (protein, huesken, soy). principles.md: at the third exception of one reason "the
next pass proposes an amendment". Strictly soy would not be an exception to MET-5's fallback clause but an overrule of a
deliberate source metric under MET-2/MET-11, so the amendment has to say whether the reason also beats a deliberate
source metric. Draft wording for MET-5 or MET-11: "When the use case ranks units within a group the task holds out
whole, and the pooled score is mostly the groups' means, declare the metric within groups (`mean_group_*`) from
context, naming the pooled original; this holds also against a paper's one deliberate pooled criterion when the
split is ours (protein_model_quality_rf_pcp, huesken_sirna_efficacy, genomic_prediction_soy_yield)."
Register flags: `exception_to_must MET-1` (huesken, protein, superconductivity) and `amendment_due MET-1` are artefacts
of the rule-ID tagging: those were exceptions to MET-5 (Should) serving MET-1, not exceptions to a Must, and
superconductivity's reason is already rule MET-17. For the within-group reason the count stands at two.
Not checked by me: whether leave-family-out studies on SoyNAM (Xavier & Rainey 2019, cited by the domain practitioner)
report the correlation per held-out family. If they do, that is source-side evidence for within-family r and would
weaken fact (a).

------------------------------------------------------------------------------------------------------------------
D9. YEAR 2015 vs 2019, source (PROV-8, PROV-9, PROV-10; builder issue 5)
------------------------------------------------------------------------------------------------------------------
Precedents: airfoil_self_noise (1989, not UCI 2014, 2026-10-20), first_principles_tully_fisher (1977, not PMLB),
nikuradse_1/2 (1933): the original, never a later re-host. PROV-9: "not the year of a paper that only analysed the
data". eucalyptus / cps88wages (Lennart 2026-11-04): an unpinnable first publication takes the best guess with a
comment. 2_month_survival_rate_prediction (2026-10-26): the first publication of the rows we ship. Snapshot reading
(rain_in_australia 2026, wadden_sea_sibes_macoma_abundance 2024, Andrej 2026-11-02, record set to the definition's
year).
Comparison: the definition's 2015 (CRAN 1.0 of 2015-07-29, the earliest dated public copy, the SoyBase release date
unpinned, said in the notes) follows PROV-9's best-guess clause; the snapshot reading gives 2015 too (the shipped data
are SoyBase's as downloaded 2015-11-16). The record's 2019 is Azodi's, a later paper that cut and analysed the data:
departs from PROV-9 without a reason. Fix the record to 2015 through the store, as wadden_sea was (the record's
assessment of 2026-11-08 already calls Azodi "a derived cut to cite"). Add the CRAN link to `source_links`.
Two small points: (1) the record's 2026-11-08 assessment names a SoyBase data store "SoyNAM_2014"; if that is the
release, 2014 would be the better guess. One clause in the year note ("a SoyBase store named SoyNAM_2014 hints at
2014, not dated") keeps PROV-9's "say that it is a guess and why". (2) `source_url` is the CRAN package, while
australian_vehicle_insurance_2004_2005 points `source_url` at the original (the 2008 book) and names the CRAN package
as the copy. What sets soy apart: the package's authors are the SoyNAM project itself (Xavier, Beavis, Diers, Specht,
...), so it is the owners' own publication, and the SoyBase release has no citable work. Consistent with PROV-8/10 on
that fact; worth one sentence in the Source bullet.

==================================================================================================================
REFLECTION PROMPTS (issue shape, for REVIEW.md turns)
==================================================================================================================

PROMPT 1 (D3)
**Consistency check (AI, 2026-11-09):** should the environment effects behind the target come from the check plots,
as our own all-row computations were fixed on sf_permit_time and home_credit_default_risk?

**Problem:**
- The target's environment effects are fit on all 5,145 lines, test families included, and kept with a note.
- On sf_permit_time and home_credit_default_risk an all-row value of our own cleaning was fixed or dropped, whatever
  its size[^leak29].
- A target free of the test lines exists: each plot minus its environment's mean over the check and parent plots
  correlates 0.9991 with the shipped target.

**Experiments:**
- Refitting the environment effects per shipped fold moves test targets by r 0.99973 to 0.99996 and a ridge model's
  Pearson by -0.0014 to +0.0015 (column auditor, 9 splits).
- The check-adjusted target: r 0.9991 with the shipped one (`probes/target_shipped.json`).

| | Option | What it does | Pro | Con |
|---|---|---|---|---|
| a | Keep, record an exception (implemented) | the all-line fit stays; the note gets the per-fold numbers and the "Potential leak, kept on purpose:" wording; an exception names the facts | the BLUE over all lines is the field's standard two-stage value; the effect is at most 0.0015 r and no feature carries the environment; it is the target, which the rule's text does not name | departs from the two precedents while a fix exists; a size argument, which they did not accept |
| b | Treat like sf_permit_time | the environment effects come from the check and parent plots only, so no line of any fold enters the target | follows the precedents; no note on a transductive target needed; r 0.9991 with the current target | another estimator than the field's BLUE; check plots are fewer than line plots (each environment needs checks: verify); the target bullet and README change |
| c | Change the rule | an amendment says when a target built by our cleaning over all rows may stay (a measured shift below a stated size) | settles the next built target (a line value, a rate) once | a rule change on one case |

**Recommendation:** (b) if every environment has check plots, since it costs nothing measurable and needs no
exception; otherwise (a) with the per-fold numbers.

**Decision:** keep the all-line fit as an exception, or take the check-adjusted target?

[^leak29]: LEAK-29 (Must): "Our own cleaning never computes a feature value from statistics over all rows: compute it
    from the history before the oldest test window, or drop it." Cases sf_permit_time, home_credit_default_risk
    (Lennart, 2026-10-19). LEAK-30 (Should when weak); principles.md tension row: "fix it when we can".

PROMPT 2 (D6)
**Consistency check (AI, 2026-11-09):** should the grouping declare `context="all_rows"`, as protein_model_quality_rf_pcp
and huesken_sirna_efficacy do?

**Problem:**
- The definition declares that a model knows nothing of a line's family when predicting.
- A breeder genotypes the progeny of a new cross together and knows which lines are siblings.
- On protein and huesken you set the context to all rows of a group on the same fact, and called the earlier `none` a
  panel choice[^ctx].

**Background:**
- With the context, a model may compare a line with its siblings' genotypes (for instance the family's allele
  frequencies, which reveal the founder); the family stays out of the features either way.

| | Option | What it does | Pro | Con |
|---|---|---|---|---|
| a | Keep `none`, record why (implemented) | each line is predicted alone | lines can be chipped and predicted one by one as seed arrives | no source or practitioner says so; departs from both precedents |
| b | `all_rows` | a model may use all lines of a test family when predicting each | follows protein and huesken; matches the use case and the definition's own "ranks the progeny of new crosses" | a context-aware model may score higher than one that reads rows alone (the intended use, as on protein) |
| c | Change the rule | the doc says when grouped ranking tasks default to `none` | one rule for all | no case for it yet |

**Recommendation:** (b), with the reason in the group definition.

**Decision:** does a model see the whole new cross when predicting?

[^ctx]: SPLIT-23 (Must): the use case decides what one prediction is and what is known about a new group.
    definitions.md: "`all_rows` when all rows of a new group are known when predicting". protein_model_quality_rf_pcp
    and huesken_sirna_efficacy, CC 2026-11-05 Lennart; huesken: "the context follows the use case, not the gain".

PROMPT 3 (D8)
**Consistency check (AI, 2026-11-09):** does Azodi's deliberate choice of pooled r set this task apart from protein and
huesken, where a group-mean-driven pooled score gave way to the correlation within groups?

**Problem:**
- Pooled r is about half a ranking of families: the family's mid-parent value alone scores 0.672, above every probe
  model on unseen families (0.536, 0.572).
- On protein and huesken you replaced a pooled score for this reason with `mean_group_pearsonr` from context[^met].
- Unlike there, the source names one metric, pooled r, chosen on a random split of lines that we replaced.

**Experiments:**
- Grouped folds: pooled r 0.536 / 0.572, mean within-family r 0.210 / 0.267, family-mean r 0.816 / 0.821 (LightGBM /
  ridge); both metrics rank the two models alike.
- Random folds (Azodi's design): pooled r 0.72-0.73 with family-mean r 0.98.

| | Option | What it does | Pro | Con |
|---|---|---|---|---|
| a | Keep pooled r, record the fact (implemented) | the source's metric; the notes say the family part is known from the parents | Azodi's one deliberate criterion, the field's standard; a breeder truncates across crosses too | the score rewards rediscovering family means the breeder already has; departs from protein and huesken on the mechanism |
| b | `mean_group_pearsonr` on `family`, from context | scores the ranking within each held-out cross; Azodi's pooled r named as the overruled original | follows protein and huesken; scores what genomics adds at this decision | overrules a deliberate source metric, which the two precedents did not; third case of the reason, so the rule is amended with it |
| c | Change the rule | amend the metric rules: within-group scoring from context when the use case ranks within held-out groups and the pooled score is mostly group means, also against a paper's pooled criterion on a split we changed | the three cases decided by one rule | a rule change, though it would only write down what (b) decides |

**Recommendation:** none from the precedents alone: (a) holds if the curator reads the decision as one ranking
across crosses; (b) with (c) if the breeder's genomic decision is within the cross, as the domain practitioner argues.

**Decision:** is the breeder's decision here a ranking within each new cross, or one ranking across crosses?

[^met]: MET-5 (Should): a paper's one deliberate criterion is the source's metric. MET-2 (Must), third bullet: a task we
    changed keeps the source's metric only when its meaning survives the change. MET-11 (Must) `context`, amended
    2026-11-03: covers a source metric overruled under MET-2 or MET-4. Exceptions to MET-5:
    protein_model_quality_rf_pcp and huesken_sirna_efficacy (Lennart, 2026-11-04; "the second exception of this
    kind"). principles.md: "When the same reason has produced three exceptions, the next pass proposes an amendment."

------------------------------------------------------------------------------------------------------------------
DRIFT AND AMENDMENTS
------------------------------------------------------------------------------------------------------------------
- No drift found in Lennart's calls on SPLIT-23 context (2026-11-05 twice, same way), SPLIT-29/31 (sarcoma, huesken:
  both by the use case), MET-5 (kept deliberate criteria; departed only where none was unique), or PROV-9.
- Amendment due only if D8 goes to (b): the third within-group case. D2 would be the first exception to SPLIT-26.
  D3 would be the first target built over all rows (option c only if the curator wants a standing rule).
- Register flags read and set aside as not about this dataset: LEAK-38, PROV-4/6, SEL-16, TP-10, USE-5 (label
  documentation; diabetes_3 / xente, not target construction), USE-8, the CLEAN-19, SPLIT-9/10/14 flags.

Files: definition datasets/_dev/tabarena-v0pt2/genomic_prediction_soy_yield/dataset.py; record
curation/records/genomic_prediction_soy_yield.md; precedents curation/records/{superconductivity,
protein_model_quality_rf_pcp,huesken_sirna_efficacy}.md and datasets/_dev/tabarena-v0pt2/{huesken_sirna_efficacy,
protein_model_quality_rf_pcp,airfoil_self_noise,open_university_learning_analytics_dataset,
australian_vehicle_insurance_2004_2005}/dataset.py; rules .claude/skills/knowledge-curation/references/
{principles,metrics,splits,leak_checks,use_case,provenance,cleaning_features,task_probes}.md.
```

</details>

<details><summary>Advocate</summary>

```text
ADVOCATE, OPENING BRIEF: genomic_prediction_soy_yield (2026-11-09)
Read: dataset.py, builder_report.md, principles.md, the seven phase-A reports, MET-2/MET-5, LEAK-29/30, USE-5 texts.

Position: ship. The task, the features, the split and the metric hold as defined. Two real faults sit in the
target and in 1.4% of the genotype rows (claim auditor R1, R2). Both are fixed inside the definition from files
already downloaded, label-free. They are the mildest remedies on the ladder and no reason to hold the dataset back.

1. A real task with honest inputs (P3, P4; USE-1, USE-3, LEAK-10 Must: hold).
   Evidence: features are 4,312 SNP calls and nothing else (column auditor: no field trait, environment, set or
   check ships; feature_columns excludes `family`). 0 cross-family genotype pairs above IBS 0.90 (claim auditor,
   all 5,145 lines); 0 exact copies on 9 splits; best single marker R^2 0.067; missing indicators <= 0.014. Task
   gamer: "Hard to game"; random column -0.002..+0.001; nearest-neighbour lookup 0.116-0.239, far below honest
   ridge 0.536. Domain practitioner: fit "direct"; the genotype is all a breeder knows before yield trials.
   Answers: blind reviewer concern 2 (`family` as a feature). That was the clean-room copy; the container keeps
   `family` as the group only (LEAK-33 holds, column auditor). No change needed.

2. Grouped by family is the right split (P4; SPLIT-1, SPLIT-29 Must, SPLIT-5 Should: hold).
   Evidence: IID pooled r 0.73 vs grouped 0.53 (ridge). Within-family r barely moves (0.286 vs 0.261), so the IID
   gain is the siblings handing over family means (family-mean r 0.98 vs 0.82). Split auditor: "RIGHT WITH NOTES",
   no re-split asked. Practitioner: "none of their siblings has a yield record yet". Precedents followed: huesken,
   airfoil, superconductivity (precedent checker D4: consistent, no drift).
   Answers: Azodi's random 80/20. SPLIT-5 makes a prescribed split a claim checked against the use case, and the
   P4 Must outranks the source's design.

3. Worth benchmarking, every fold scorable (P6; TP-1..TP-10; `groups_test_groups_few` accepted).
   Evidence: LightGBM beats the dummy on 100% of probed splits (pooled r 0.47). 1,660-1,775 test lines per fold,
   13 families per test fold, more than any accepted precedent (airfoil 11, huesken 10, open_university 6-9;
   precedent checker D5). Ridge beats LightGBM on 7 of 9 folds (mean diff 0.040, SD 0.045): the model comparison
   survives the fold noise. A p ~ n regression where linear methods compete (blind reviewer: "useful").
   Answers: fold spread 0.29-0.61 (split auditor, blind reviewer). The tension row "the right split against the
   score" (P4 over P6) says spread is no reason to change the split. Mildest remedy: accept the warning and add the
   spread and all four group-probe models to its text (precedent checker's wording nit). Stratifying folds by founder
   type is optional and needs a new column, so it should not block shipping.

4. Pooled Pearson r stays (P6; MET-5 Should, MET-1, MET-2 Must: hold).
   Evidence: Azodi names r as "the standard metric for GP performance" and uses MSE only for tuning. The claim
   auditor verified the quote: one deliberate choice. Under MET-2, pooled r keeps its meaning on our split. It
   ranks lines of crosses never phenotyped, across crosses, as the breeder truncates a cycle. On the random split
   it rewarded siblings' family means (0.98). The grouped split removes that part, so the score now measures more
   genomics, not less. Both metrics rank the probe models alike (ridge > LightGBM).
   Answers: practitioner / precedent PROMPT 3 (`mean_group_pearsonr`). The mid-parent baseline 0.672 uses founder
   yields from the same 2011-2013 trials. The practitioner calls that "somewhat optimistic" and LEAK-10 territory,
   and 8 of 40 founders are plant introductions with no adapted yield record. protein/huesken replaced a fallback.
   Here we would overrule a deliberate source criterion (precedent checker fact (a)), a stronger step that
   MET-5's Should does not ask for. This is a weighing call for the curator. Mildest remedy: keep pooled r, and
   state in the notes the within-family r (0.21-0.27) and that cross means are partly known from the parents.

5. Target: concede R1. Fix the definition and keep the dataset (P3; USE-5 Must, triggered).
   Evidence: Diers et al. 2018 (the data paper) remove set (block) effects estimated from check plots. Every
   env x set holds one family; block SD 367 kg/ha. Block-adjusted LS mean: r 0.958 with the shipped target;
   repeatability across environment halves 0.557 -> 0.643; ridge pooled r 0.572 -> 0.618 on all 3 folds.
   Mildest remedy: in `_clean`, subtract a check-based block effect per (environ, set) before `line_values`
   (claim auditor a10/a12/a14, about 10 lines; data_check_qa is already downloaded and holds no line of any fold).
   Correct "check covariate degenerate" (true for data.line only).
   Related, PROMPT 1 (D3, environment effects over all lines): LEAK-29's text names a feature, and the measured
   effect is <= 0.0015 r per shipped fold (column auditor; split auditor 0.5294 vs 0.5289). Keeping it with a
   LEAK-30 note carrying the per-fold numbers is defensible. Every set has 2-20 check plots, so the same edit can
   also take the environment effects from checks and remove the question. Either way the target stays a BLUE in
   kg/ha, the field's convention (practitioner, TP-7).

6. Genotype rows: concede R2. Repair it and keep the dataset (P5; PROV-13 Must, small).
   Evidence: 70 of 5,145 lines (1.4%) carry a raw row of another sample. Within-family r on them is 0.035 with raw
   rows, 0.296 with the QA rows, and 0.317 on placebo sets.
   Mildest remedy: drop the 70 lines (a label-free filter), or the repair: gen.qa with its flips undone and blanks
   filled from IA3023's call (99.18% equal to the raw calls elsewhere). The raw-call choice stands for the other
   98.6% of rows: the practitioner keeps raw calls, the precedent is coad (D7), and the column auditor confirms the
   QA blanking (24-26% of cells).

7. The remaining findings are notes and record fixes that need no decision (P5, P7; PROV-9, CLEAN-1, writing.md).
   - Record year 2019 -> 2015 and add the CRAN link to source_links (D9; wadden_sea precedent).
   - Name the 219 lines above 20% heterozygous calls (not tied to the target: r +0.02), the ~96 off-type lines
     (~1.9%), and the 5 merges of distinct genotypes. Keep them (CLEAN-1 quality note; the column auditor and
     split auditor both say "keep").
   - Restate the transductive note with the per-fold numbers. Add the shared seasons and the maturity range
     (practitioner gaps 2 and 4).
   - Record the SPLIT-26 exception text (one row per line; environment effects -1,252..+1,471 vs SD 359) as the
     precedent checker drafted it.
   - PROMPT 2 (context): follow protein/huesken with `all_rows`. Lennart decided that twice on the same fact, and
     treating like cases alike needs no new call. It also turns the gamer's only exploit (+0.017 ridge, negative on
     some splits) into allowed use.

Judgment record
Verdict: ship after changes.
Validity: USE-1/USE-3 hold; USE-5 triggered, fixed (block-adjusted LS mean); LEAK-10, LEAK-16..21 hold; LEAK-29/30
  weak, kept with note or removed by check-based effects; SPLIT-1/SPLIT-29 hold; PROV-13 triggered, fixed (70 rows).
Value: TP-2 real signal; MET-5 pooled r kept.
Quality: CLEAN-1 notes (heterozygosity, off-types).
For the curator: issue 1 target (recommend block-adjusted, option d); issue 4 metric (recommend pooled, weighing).

Rebuttal
(Answers the critic's opening brief, points 1-7. No new points.)

C1 Target without the block adjustment (USE-5, TP-7 Must): CONCEDE. My point 5 already concedes this. The critic's
   own check confirms the structure: every env x set holds one family (1,707 of 1,707), and every block has check
   plots. What follows: make the block-adjusted LS mean option (d) of issue 1 and recommend it. Correct the 0.9991
   sentence and the "degenerate covariate" sentence. The task keeps its form: a BLUE in kg/ha, one row per line.

C2 70 mispaired genotypes (PROV-13 Must, small): CONCEDE, as in my point 6. Either remedy is fine. The repair from
   gen.qa (flips undone, blanks filled from IA3023, 99.18% equal to the raw calls) sits higher on the ladder than
   dropping 70 rows. Rewrite the Features bullet: the "deletes differences between families" reason is refuted.

C3 Context "none" (SPLIT-23 Must): CONCEDE. My point 7 already asks for `all_rows` under the protein/huesken
   precedents. A like case decided twice by the curator is followed (principles.md, "treat like cases alike"). It
   needs no new call and makes the gamer's +0.017 / +0.055 legitimate use.

C4 Environment effects over all lines (LEAK-29 by analogy, LEAK-30): CONCEDE THE NUMBERS, KEEP THE STANDING. The
   note must carry the per-fold figures, not leave-one-family-out: test-line shift SD 3.5-7.2 kg/ha, max 29;
   training max 49-53; Pearson moves <= 0.0015. LEAK-29's text names a feature value. This is the target, and no
   environment ships as a feature, so keeping it with a LEAK-30 note is a defensible exception. Both briefs agree
   on the clean way out: take environment and block effects from the check plots in the C1 edit, and the issue
   disappears.

C5 Pooled r vs mean_group_pearsonr (MET-2 Must third bullet, MET-5 Should): DISPUTE the trigger, CONCEDE the note.
   - MET-2 asks whether pooled r's meaning survives our change of split. It does. The family-mean part the critic
     objects to was already in Azodi's own score: 52.7% of the variance lies between families on any split, and on
     the random split the family-mean r was 0.98. Our split did not bring family means into pooled r. It made the
     model earn them from markers instead of from phenotyped siblings (0.98 -> 0.82). The score still ranks lines
     across crosses, which is the decision the use case states.
   - The parent baseline (0.672 mid-parent, 0.602 founder only) uses parent yields from the same 2011-2013 trials.
     Both the practitioner and the critic call it optimistic, and in a model it would be a LEAK-10 input. It shows
     what a breeder could add outside genomics. It does not show that pooled r scores the wrong decision.
   - protein and huesken replaced a fallback. Here MET-5's deliberate source criterion stands (precedent checker
     fact (a)), so the two precedents do not bind, and a third "exception" would really be an overrule needing the
     amendment.
   - Both metrics rank the probe models alike (ridge > LightGBM). The choice does not move a conclusion the panel
     has measured.
   - Conceded: if pooled r stays, the notes state the parent baseline and the within-family r (0.21-0.30), and fit
     stays "direct" with that note. Whether the breeder's genomic decision is within or across crosses remains the
     curator's weighing call (issue 4).

C6 Fold swing with the founder mix (TP-3, weigh): DISPUTE THE REMEDY'S NECESSITY, CONCEDE THE TEXT.
   - The spread (0.29-0.61) is real. The model comparison survives it: ridge beats LightGBM on 7 of 9 folds, and
     the per-fold difference has SD 0.045 against a mean of 0.040. The P4-over-P6 tension row says fold variance does
     not reshape a right split.
   - Stratifying by founder type adds a new column and a new split design that no Must asks for.
   - Five repeats are the cheaper option, if the curator wants one. The within-family metric is no fix for variance
     either: each family's r has an SE of about 0.085.
   - Conceded: the accepted-warning text names all four group-probe models and the per-fold spread with its cause.

C7 Notes and record: CONCEDE in full, as in my point 7. The record year goes to 2015, plus the CRAN link, the
   heterozygosity, off-type and merged-entry clauses, and the shared seasons and maturity range. No code change.

Where we stand: the critic and I agree on C1-C4 and C7 (fixes inside the definition, no exclusion). The open
dispute is C5 (metric, a weighing call; I hold pooled r with a note) and C6's stratification (I hold it optional).
```

</details>

<details><summary>Critic</summary>

```text
CRITIC, OPENING BRIEF: genomic_prediction_soy_yield (2026-11-09)
Read: dataset.py, principles.md, rule texts (USE-5, TP-7, PROV-13, SPLIT-23, LEAK-29/30, MET-2/5/11), builder report,
the seven phase-A reports. Own check (raw files in the warehouse): every env x set block of data_line_qa holds one
family (1,707 of 1,707) and every block has check plots in data_check_qa (median 5).

POSITION: ship only after changes. The task is real and the grouped split is right; nobody on the panel, me included,
argues for exclusion. Two Musts fail as built (target construction, mispaired genotypes) and are cheap to repair from
files already downloaded. Then come a Must-level declaration (context), a weak all-row fit, the metric's meaning on our
split, and notes.

1. TARGET OMITS THE SOURCE'S BLOCK ADJUSTMENT (P3; USE-5 Must, TP-7 Must; EV-1)
   Problem: the line value removes environment effects only. The source's data paper (Diers et al. 2018, G3 8(10):3367,
   models 1-2) also removes set (block) effects estimated from check plots. Each set holds exactly one family, so
   block noise lands directly on family means, which is the half of the variance the pooled score rewards (point 5).
   Evidence (claim auditor R1, a12/a14; structure confirmed by me): block SD 367 kg/ha against a within-block plot SD
   of 425. A block-adjusted LS mean correlates 0.958 with the shipped value. Repeatability between disjoint halves
   of the environments rises from 0.557 to 0.643, within families from 0.327 to 0.399, and for family means from
   0.858 to 0.933. Ridge pooled r on the shipped folds goes from 0.572 to 0.618, higher on all 3 folds. The
   definition's "a check-adjusted mean gives r = 0.9991", and with it the builder's "the choice barely moves Pearson",
   rest on a per-environment check mean, which is redundant once environment effects are fit. The builder's
   "degenerate check covariate" holds for data.line `spot`, not for the QA tables' `set`.
   Remedy (fix the definition): in _clean, subtract a shrunken check-based effect per (environ, set) before
   line_values (about 10 lines; reads data_check_qa.parquet). Cite Diers 2018 in the Target bullet and Decision table.
   Correct the 0.9991 sentence. Make this option (d) of draft issue 1 and recommend it. USE-5 allows an approximate
   fit only for an undocumented label, and this construction is documented.

2. 70 LINES CARRY ANOTHER SAMPLE'S GENOTYPE (P5; PROV-13 Must, small)
   Problem: features come from gen.raw by name. For 70 of 5,145 lines (1.4%), the raw row is not the sample the QA
   release pairs with that phenotype: the QA renamed samples consistently in its phenotypes and genotypes.
   Evidence (claim auditor R2, a3/a9): raw vs QA concordance per line, with QA flips undone, is below 0.90 for 70
   lines and as low as 0.15 (e.g. QA DS11-13010 = raw DS11-13031). Decisive test: ridge predicting these 70 lines
   gets within-family r 0.035 with the raw rows, 0.296 with the QA rows, and 0.317 +- 0.106 on 20 placebo sets of
   concordant lines. The definition's reason for not using gen.qa ("deletes the differences between families") is
   refuted: filling QA blanks with IA3023's call reproduces 99.18% of raw calls.
   Remedy (repair): build features from gen.qa with the flips undone and blanks filled with IA3023's call (label-free,
   per row). The minimum is to drop the 70 discordant lines. Rewrite the Features bullet either way.

3. GROUP CONTEXT "none" WITHOUT A REASON (P4; SPLIT-23 Must; precedents protein_model_quality_rf_pcp, huesken)
   Problem: the definition says a model knows nothing of a line's siblings, but a breeder genotypes and ranks a new
   cross together, and the definition's own text says it "ranks the progeny of new crosses". Lennart set
   context="all_rows" on the same fact twice (2026-11-05) and called a panel's "none" a panel choice.
   Evidence: precedent checker D6. Task gamer: rebuilding test families by clustering (ARI 0.82-0.98) and shrinking
   to family means gains +0.017 (ridge) and +0.055 (LightGBM). Under "none" that gain is a forbidden test-batch
   statistic that nothing enforces. Under "all_rows" it is legitimate use.
   Remedy (fix the definition): context="all_rows", with the use case as the reason; otherwise record why "none".

4. ENVIRONMENT EFFECTS FIT ON ALL LINES, AND THE NOTE'S NUMBERS ARE THE WRONG ONES (P4; LEAK-29 Must by analogy,
   LEAK-30 Should when weak; precedents sf_permit_time, home_credit_default_risk, which were fixed whatever the size)
   Problem: test families' plots enter the effects subtracted from every target. The effect is weak (column auditor:
   ridge r moves by at most 0.0015 per fold). Still, a fix from our own cleaning exists, and the precedents took it.
   Evidence: the note gives leave-one-family-out shifts (0.9 kg/ha mean, 5.4 max; the claim auditor recomputes the
   mean as 1.39). The shipped folds hold out 13 families: per-line shift SD 3.5-7.2 and max 29 kg/ha on test lines,
   max 49 on training lines (column auditor). Split auditor: mean 4.1, max 53.
   Remedy (mildest): if point 1 goes to a fully check-based environment-and-block adjustment, the issue disappears.
   Otherwise keep it, with "Potential leak, kept on purpose:" wording and the per-fold numbers, recorded as an
   exception to the two precedents (fact: a target rather than a feature, and no channel among the features).

5. POOLED r ON OUR SPLIT SCORES WHAT THE PARENTS ALREADY TELL (P6; MET-2 Must third bullet, MET-5 Should, MET-11)
   Problem: Azodi chose pooled r on random lines. We changed the split, and on 13 unseen families pooled r is mostly
   the ranking of family means. A breeder takes those from the parents' records. Genomic selection adds the ranking
   within a cross.
   Evidence: the founder's or mid-parent's own yield, with no genotype, reaches pooled r 0.672 (domain practitioner;
   38 families) and 0.602 (split auditor, founder only). That beats ridge (0.53-0.57) and LightGBM (0.49-0.54). The
   true family-mean oracle reaches 0.71-0.73. The between-family share is 52.7%. Within-family r is 0.21-0.30 and
   barely depends on the split. The same mechanism decided protein_model_quality_rf_pcp and huesken for
   mean_group_pearsonr (Lennart, 2026-11-04). Caveat: the parents were grown in the same trials, so 0.672 is
   optimistic.
   Remedy: mean_group_pearsonr on family, from context, with Azodi's pooled r named as the overruled original. MET-2
   allows the metric to read the task's own group column. This would be the third case, so propose the amendment the
   precedent checker drafted. If the curator keeps pooled r, the notes must state the parent baseline and that
   within-family r is the selection-relevant part, and fit stays "direct" only with that note.

6. FOLD SCORES SWING WITH THE FOUNDER MIX (P6; TP-3 / weigh; check warning groups_test_groups_few)
   Problem: per-fold pooled r is 0.29-0.61 (ridge SD 0.108). It correlates 0.78 with the spread of the test families'
   means. Fold r1f2 holds no plant-introduction family and scores 0.27-0.30 for every model, with LightGBM R^2 -0.79
   (split auditor; blind reviewer finds the same).
   Remedy: stratify the family-to-fold assignment by founder type (elite / diverse / PI, from the parent names or
   Song 2017), or use 5 repeats. The acceptance text should name all four group-probe families (precedent checker D5)
   and the per-fold spread. Point 5's within-family metric also removes most of this variance.

7. NOTES AND RECORD THAT DO NOT MATCH THE DATA (P5 PROV-9 Should; P7 CLEAN-1 Should; writing.md). Quality only, not a
   reason to hold the task.
   - Record year 2019 (Azodi) vs definition 2015: fix the record. Add the CRAN link to source_links. Optionally say
     that a SoyBase store named SoyNAM_2014 hints at 2014.
   - Undocumented: 219 lines with > 20% heterozygous calls (max 71%, mixed samples). Point 2 fixes 39 of them.
   - About 96 kept lines sit nearest another family. 5 lines pool the plots of a genetically distinct merged entry.
   - Maturity confounds yield (r 0.27). Train and test share the same seasons.
   Remedy: a clause each in the Lines, Features, Target and fit_reason bullets. No code change.

Judgment record (critic's reading)
Verdict: ship after changes.
Validity: USE-5/TP-7 triggered (block adjustment missing; fix 1). PROV-13 triggered, small (70 mispaired genotypes;
fix 2). SPLIT-23 triggered (context none without a reason; fix 3). LEAK-29/30 weak (fix or note, 4). SPLIT-1/SPLIT-29
hold. LEAK-10, LEAK-16..21 and LEAK-33 hold.
Value: MET-2 third bullet contested (point 5, a curator call with two precedents for the change). TP-2 holds. Fold
variance weighed (6).
Quality: CLEAN-1 notes (7).

Rebuttal
(One answer per point of the advocate's opening brief. No new facts.)

A1 Real task, honest inputs: CONCEDE. The features are SNP calls only. `family` is the group column and not a
   feature (LEAK-33). There are no copies across the split. I raised none of this.

A2 Grouped split: CONCEDE. SPLIT-1, SPLIT-29 and SPLIT-5 hold. My brief asks for no re-split.

A3 Worth benchmarking, fold spread: CONCEDE that stratifying the folds is optional (weighed) and does not block
   shipping. P4 over P6: the spread does not change the split. We agree on the minimum: the acceptance text names all
   four group-probe families and the per-fold spread 0.29-0.61. Founder-type stratification or 5 repeats stays a
   suggestion for the curator.

A4 Pooled r stays: DISPUTE one fact, CONCEDE the weighing.
   - The fact. "The grouped split removes [the family-mean part], so the score now measures more genomics" is not
     what the data show. The grouped split removes the siblings' handover, but not the family-mean share of the
     score. The between-family share is still 52.7%. The true family-mean oracle scores pooled r 0.71 on the shipped
     folds, above ridge 0.57 (claim auditor C17b). Within-family r is 0.21-0.30 under both splits (split auditor).
     So on our split, pooled r mostly ranks the 13 test families. That is MET-2's third bullet (Must): the task
     changed, and the meaning of pooled r has to be checked, not assumed.
   - The optimism caveat. I accept it, and my brief already gave it. Still, the founder-only predictor scores 0.602
     against ridge 0.529 on the same 9 shipped folds (split auditor). That is a margin of 0.07, not a rounding error.
   - The weighing. Fact (a) is real: Azodi chose pooled r deliberately, and protein/huesken replaced a fallback. A
     switch is therefore a curator call under MET-2 and MET-11, not something MET-5 forces. My remedy stands as a
     recommendation. The floor we both accept: notes giving the within-family r and the parent baseline (0.60-0.67
     with its caveat). Without those notes, "fit direct" overstates what the score measures.

A5 Target: AGREED (USE-5 and TP-7, Must). On the environment effects over all lines (LEAK-29/30): we converge. Take
   the environment effects from the check plots in the same edit. Every block has checks (median 5, my count), so
   the transductive note and the exception to sf_permit_time and home_credit both fall away. Keeping the fit with a
   LEAK-30 note is the fallback, and the note must then carry the per-fold numbers, not the leave-one-family-out ones.

A6 Genotype rows: AGREED (PROV-13, Must). On which remedy: the repair is better than the drop. It keeps the 70 units
   with their own genotypes, which PROV-14 (Must, "a repair stays under its record: the same units") prefers.
   Dropping them is acceptable, with the count stated.

A7 Notes and record: CONCEDE all items. One correction of rank: context="all_rows" (SPLIT-23, Must) changes the
   definition's Grouping and is no mere note. We agree on the outcome: follow protein/huesken.

Net after rebuttal: the advocate and I agree on the verdict (ship after changes) and on the four changes to the
definition: the block-adjusted (preferably fully check-based) target, the QA genotype repair, all_rows, and the notes.
The one open dispute is the metric (point 5 / A4): pooled r against mean_group_pearsonr on family. That is a weighing
call for the curator. I recommend the within-family metric, with the corrected fact above.
```

</details>
