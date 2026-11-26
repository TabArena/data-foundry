---
unique_name: genomic_prediction_soy_yield
name: gp-soy-YLD (Soybean Yield Genomic Prediction)
checked_by:
- Andrej
data_foundry_status:
- WIP (DF)
claimed_by: Andrej
suggestion: 'Yes'
priority: 3
tags:
- Many features
- 'Samples: No Time Dimension'
- 'Entities: Recur'
- Experimental Results
collections:
- TabBench-Bio
original_source: Other
year: '2015'
collection_period: 2011-2013
domain: biology & life sciences
problem_type: Regression
original_data_state: Database (or multiple to-be-joined tables)
source_links:
- https://cran.r-project.org/package=SoyNAM
- https://doi.org/10.1534/g3.118.200332
- https://doi.org/10.1534/g3.119.400498
- https://doi.org/10.5061/dryad.xksn02vb9
- https://arxiv.org/abs/2609.07441
- https://zenodo.org/records/4980429
v2_path: datasets/_dev/tabarena-v0pt2/genomic_prediction_soy_yield/dataset.py
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-11-25):** `TBD -> Yes`, priority 4: yield of about 5,000 SoyNAM recombinant inbred lines of 40 biparental families from about 4,300 SNP markers — genomic selection as a plain regression, the one of the four Azodi cuts with a comfortable shape, and an origin (the SoyNAM data) that holds the yields in kg/ha per plot.
- Source: the SoyNAM population, "recombinant inbred lines (RILs) derived from 40 biparental populations" (Xavier et al. 2016, quoted in the Azodi release's README); the data were released by the SoyNAM project on SoyBase (offline) and are kept in the CRAN package `SoyNAM` (https://cran.r-project.org/package=SoyNAM, first version 2015-07-29, GPL-3, data "downloaded on November 16th 2015 from https://soybase.org/SoyNAM/index.php"); the yield trials are described by Diers et al., G3 8(10):3367, 2018 (https://doi.org/10.1534/g3.118.200332). Compiled as a derived cut by Azodi CB et al., "Benchmarking Parametric and Machine Learning Models for Genomic Prediction of Complex Traits", G3 9(11):3691-3702, 2019 (doi 10.1534/g3.119.400498; Dryad doi 10.5061/dryad.xksn02vb9, Zenodo 4980429, CC0). As published by Azodi: `soy_pheno.csv` 5,014 lines x 3 traits (HT, R8, YLD), standardized, and `soy_geno.csv` 5,014 lines x 4,234 markers coded -1/0/1, plus fold assignments. As published at the origin (package 1.6.2, counted 2026-11-08 in the size check of the large candidates): 60,390 line-environment plots with yield in kg/ha for 5,546 lines of 40 families in 18 environments (2011-2013; Iowa, Illinois, Indiana, Kansas, Michigan, Missouri, Nebraska and two Ohio sites), with height, R8, lodging, protein, oil and seed size, check plots in `data.check`, and 5,590 lines x 4,611 raw markers coded 0/1/2 (a QA set of 5,180 x 4,312). Target: yield per line.
- Use case: a soybean breeder, before the field season, ranks the progeny of a new cross from the genotype alone (genomic selection): predicting traits from genotypes "is accelerating the speed of crop and livestock breeding" (Azodi et al., Introduction), and the paper recommends that "breeders test the performance of multiple algorithms on their training population"; fit direct; collection `Samples: No Time Dimension`: a designed population of RILs grown in a multi-environment trial (2011-2013), each family in field blocks with common checks, the genotype fixed before the trials; `Entities: Recur` at the origin (a line has a median of 11 environment plots), one row per line once the line value is computed; type `Experimental Results` (a designed population measured by one trial protocol, SPLIT-34).
- Split: leaf L-EXP.kind (Grouped · `UnseenGroup`, the family) because [EXP.meets] a kind the data does not contain (the breeder ranks the lines of a new cross, with no phenotyped sibling), [EXP.kind-key] yes (the family is in the line id, `DS11-XX...`; 40 families of about 98 to 140 lines, 39 after the QA, enough to hold out whole); open: within-family selection (a random split of lines, L-EXP.random) is the other common genomic-selection design, and about half the variance of the line values lies between families, so the metric question below goes with it; Azodi's random 80/20 holdout over lines is a habit, not a choice for this use case (SPLIT-5).
- Siblings and duplicates: the other three cuts of the same Azodi release are other species and panels, distinct tasks (PROV-7); soy HT and R8 would be cuts of this one without a distinct task (PROV-6). `uniform_soybean_tests_yield` (Shook et al. 2021, variety x location x year records with daily weather) is soybean yield as well, but a genotype-by-environment task from weather and location rather than genomic prediction from markers (PROV-7); `soybean` (UCI 1988) is the unrelated disease diagnosis set. External collections: TabBench-Bio (`gp-soy-YLD`).
- Better data: the origin itself, SoyNAM (above): about 5,500 lines on the natural scale instead of Azodi's 5,014 standardized values, the same source, so the first publication to build from rather than another record (PROV-8, PROV-13); no other hit in a quick look.
- Papers and pages: Azodi et al. 2019 (G3, https://academic.oup.com/g3journal/article/9/11/3691/6026746); Xavier et al. 2016 and Song et al. 2017 (Plant Genome, https://doi.org/10.3835/plantgenome2016.10.0109) for the population and the SNP chip; Diers et al. 2018 for the trials; the CRAN package; the Zenodo mirror https://zenodo.org/records/4980429; TabBench-Bio (arXiv 2609.07441), Table 4 row gp-soy-YLD.
- Metric: Pearson's correlation over the test lines, the ranked criterion of Azodi et al. ("as it is the standard metric for GP performance"; MSE only tuned the hyper-parameters), one deliberate choice of the field (MET-5) that matches a selection ranking lines. Open for the curator: on held-out families a pooled r also scores the ranking of the families, while the ranking within a cross is what genomics adds; `mean_group_pearsonr` on the family is in the library (MET-13). TabBench-Bio's RMSE (Sec. 3.5) is a benchmark convention. Inputs: the family, for a within-family score; it is computable from the line id.
- Risks for /add-dataset: build from the origin, not from Azodi's standardized `YLD` (README: "normalized between 0 and 1", observed mean 0 and sd 1; MET-3, PROV-13). The line value is ours to compute from the plots: Diers et al. 2018 adjust for environment and field-block effects estimated on the check plots, the simpler option is a mean over environments; either way no line's plots may enter another line's value (LEAK-10). Some lines' raw genotype rows may belong to another sample (compare the raw and the QA matrices per line). Missing marker calls stay missing: no imputation over all rows (CLEAN-7). Late maturity correlates with yield; R8 is measured with the yield and does not ship as an input (LEAK-10).
- Priority: gap 0 (biology & life sciences has 10 accepted datasets, thin at 6 or fewer; regression and the grouped regime are not thin), use case + (the breeder and the selection decision are named), source + (data papers, a maintained package from the project's members, CC0 for the cut), shape + (about 5,500 lines x 4,300 markers, 40 families), risk 0 (the origin repairs the scale; the line value follows the data paper's model).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the benchmark TabBench-Bio (https://arxiv.org/abs/2609.07441).
- as published: 5,014 x 4,234; target: YLD.
- Why: Yield of soybean lines from SNP genotypes
- Notes: Same Azodi et al. release; the existing soybean record is the unrelated UCI disease set.

**CC (2026-11-25, Andrej):** accepted for adding, after the re-screening of the TabBench-Bio candidates on the current rules.
- Added with `/add-dataset`; the open points go into this record's `## Review`.

**Assessment (AI, 2026-11-25):** built from the origin with `/add-dataset` (steps 0-6); the record's `year` moves from 2019 (the Azodi cut) to 2015, the first publication of the data, and the CRAN package leads the source links.
- The definition reads the package's quality-assured `soybase` release: `data.line.qa` (62,572 line plots), `data.check.qa` (10,721 check plots) and `gen.qa` (5,180 x 4,312 calls), not the original `soynam` objects of the same package. The reason is the field block: `data.line`'s `spot` column holds one value per environment (all 60,744 rows read `2A`), so the block effect the data paper removes cannot be recovered from it, while `data.line.qa` carries the set (156 blocks = 39 families x 4) and every line plot sits in a block that has check plots. It costs 402 lines, family 46 and 299 markers; the two phenotype tables agree on 53,397 of the 55,945 plot yields they share.
- Shipped: 5,143 lines x 4,312 markers, 39 families of 98 to 140 lines, yield 2,099 to 4,602 kg/ha (the screening block's "about 5,500 lines, 40 families" was the original release). Missing calls 25.65%, which is the design: 24.6% of the family-by-marker blocks are more than 90% missing and 75.3% less than 10%, so a marker is scored where the cross segregates for it.
- The line value is ours to compute: `yield = mu + b * block index + environment + line` by least squares over the 56,929 plots with a yield, the block index from the check plots alone (the package's `CHECK()`), so no line's yield enters another's (LEAK-10, LEAK-29). Fitted b = 422 kg/ha per unit of the index; the value correlates 0.962 with a fit without the block term and 0.943 with the plain mean of a line's plots.
- Metric: `mean_group_pearsonr` on the family, from context, with the field's pooled predictive ability as the original. 54.2% of the variance of the line values lies between families, and on the first 6 splits a predictor that knows only the true mean of a test line's own cross scores a pooled r of 0.68 (RMSE 238 kg/ha) against 0.24 (359) for ridge on the markers, while scoring 0 within the family.
- Split: leaf L-EXP.kind, grouped on the family, `UnseenGroup`, `context="all_rows"`; 39 families give 13 per test fold, which raises the `groups_test_groups_few` warning for the curator.

**Assessment (AI, 2026-11-25):** review panel (full tier, 11 roles): ship after changes; disputed: whether the shipped target is the package's own `BLUP(dereg=TRUE)` (TP-6, SPLIT-26: it is not), the direction of the germplasm gap (USE-8: the breadth makes the declared metric harder, not easier), and the blind reviewer's vote to exclude over the blank marker calls (CLEAN-7, MET-11: overruled, it rests on a pooled score the task does not use); for the curator: issues 1-7.
- Applied without a decision: the target fit is attributed to the package's `BLUP()` with the two real departures from Diers et al. 2018, the planting date being immaterial; `fit_reason` is rewritten on the germplasm with its measured direction, keeping `fit="approximate"`; the metric reason gains the parent-yield fact (r = 0.937) and what a pooled score would reward; the splits comment gains the departure on the declared metric (0.036 to 0.117) and the context gain (+0.0795); and new notes carry the dropped traits' worth (+0.391 against the markers' +0.213), `set` with the load-bearing shuffle, the block structure of the missingness, the maturity paragraph and the licence clause. No `Selection Bias` marker: a designed panel whose progenies were not selected is the carve-out for rows from another population.
- Corrections to the figures of the 2026-11-25 build line above: the quality-assured release costs 401 lines, not 402; the entry-mean heritability is 0.808 (Diers et al. publish 0.822), not 0.84; the between-family share of the line-value variance is 54.3%, not 54.2%; the single-marker probe score of 0.145 is the missingness pattern, a label of the cross, not a QTL.
- Two items went to the working copy's cross-dataset file rather than here: the amendment of the source-metric rule, which spans three datasets, and how to record a public derived copy of a rebuilt dataset's target.
- Priority 3: gap 0 (biology & life sciences has 10 accepted datasets and neither regression nor the grouped regime is thin), use case + (the breeder, the moment and the ranking decision are named, and the measured selection gain agrees with the metric to 5%), source + (the project members' own package, pinned and checksummed, with three data papers), shape + (5,143 lines x 4,312 markers, 39 groups), risk - (a public CC0 cut of the same population recovers the target for 91.9% of test rows with no remedy that keeps the task, issue 7).

**Assessment (AI, 2026-11-26):** the line value is now built as Lennart's build of this dataset builds it, which closes the check-only environment fix (issue 2) and the founder-parent documentation point; nothing else about the task changes.
- The environment effects and the field-block effects both come from the check plots alone (model 1 of Diers et al. 2018; the block effects shrunk by `vb / (vb + ve / n)`, 0.43 to 0.92 over the 1,707 blocks), and a line's value is the mean of its own corrected plots, so no line's yield enters another line's value and the `Potential leak, kept on purpose:` note is gone.
- The correction uses only the six checks grown across the trial (IA3023 and five cultivars, 7,294 plots filling all 1,707 blocks); the 39 family founders are left out, 38 of them standing in one family's blocks only and LD02-4485 fathering family 12 while serving as a general check in 18 families. Taking them in moves the values by 27.8 kg/ha SD and the declared metric 0.005 up for ridge and 0.001 down for LightGBM.
- Measured against the superseded values: pooled r 0.9925 (Spearman 0.9906), within a family 0.987 (lowest family 0.956), difference SD 44 kg/ha and 39 within a family; line values 2,029 to 4,584 kg/ha (mean 3,578, SD 354) against 2,099 to 4,602 (3,607, SD 353); entry-mean heritability 0.789 against 0.809, with 0.822 published by Diers et al.; between-family share 55.3% against 54.3%. On 3 grouped folds ridge scores 0.198 against 0.207 and an untuned LightGBM 0.229 against 0.223, inside a fold-to-fold spread of 0.03 to 0.06.
- `dataset check` ends where it began: 0 errors, 1 warning (`groups_test_groups_few`) and 1 info over 28 checks. Model scores elsewhere in the notes that were measured on the superseded values (the probes, the dropped traits' worth, the context gain, the metric reason) were not re-run; the two targets correlate 0.987 within a family.

**CC (2026-11-26, Andrej):** the review decisions on issues 1 and 3.
- Issue 1, closed and rewritten, his words: "Close this issue and rewrite it from scratch for the new target." Its options and the exception text it drafted describe the superseded construction (a least-squares fit of `mu + b * block index + environment + line` over the line plots) and are void with it; nothing in it is decided.
- The same question is asked again as issue 8, against the target that ships since the rebuild of 2026-11-26: each plot corrected for its environment and its field block on the six common check plots alone, the block effects shrunk by their variance ratio, the 39 family founders left out, and a line's value the mean of its corrected plots.
- Issue 3, change to B: the few-groups warning is accepted in writing. `accepted_check_warnings` carries `groups_test_groups_few` with the drafted reason, and `dataset check` now ends at 0 errors, 0 warnings and 1 info over 28 checks, the warning ignored rather than raised.
- Every figure in that reason depends on the target, so all were measured again on the shipped values over the 60 splits: four model families beat the dummy on 60 of 60 folds; per-family r has SD 0.09 to 0.10, a standard error of 0.015 to 0.017 against a mean of 0.18 to 0.23, 12 to 16 standard errors from zero; 38 of 39 families score positive under ridge and all 39 under the other three; a within-family label permutation (500 runs) gives mean +0.0001, SD 0.0031, max 0.0089, with the measured score 68 null SDs above it at the p = 0.002 floor of 500 runs.
- Not changed: the data, the target, the split, the metric and every record field. Not built: no container exists for this folder.

## Review

**Outcome:** added. The SoyNAM project's own release, read from the CRAN package the project's members maintain:
5,143 recombinant inbred lines of 39 biparental families, 4,312 quality-assured SNP calls, and a yield in kg/ha that
we compute ourselves from the 56,929 plot yields, each plot corrected for its environment and its field block on the
check plots alone, with whole families held out and the score taken inside the family. A
full review panel ran (seven evidence agents, an advocate and a critic with a rebuttal each, a mediator and the
review editor) and recommends shipping it after changes; everything it settled without a decision is applied. The task
survives the attacks: four model families beat the dummy on 100% of the 60 splits, a within-family label permutation
over 500 runs gives p = 0.002, no test line has an exact feature copy in training, no column from after the
prediction point reaches the frame, and the realized selection gain a breeder would get (93 kg/ha at the top 10%)
agrees with what the declared metric predicts to 5%. The blind reviewer voted to exclude, on a pooled score this task
does not use; its fact, that the blank marker cells are values the design determines rather than failed calls, stands
and is issue 5. On 2026-11-26 the construction was brought into line with Lennart's build of the same dataset: the
environment effects as well as the field-block effects are now measured on the check plots alone, and only the six
checks grown across the trial are used, the 39 family founders left out. That closes issue 2 and the founder-parent
documentation point with it, and it moves no decision: the line values correlate 0.9925 with the old ones (0.987
within a family) and the declared metric by less than a fold. On the same day the few-groups warning was accepted in
writing (issue 3) and issue 1 was closed and asked again, for the construction that now ships, as issue 8. What is
left to decide is the wording of the exception for the line value we compute,
two source objects that need a written reason, the blank cells, the metric exception, and a public file that holds
another derivation of the same target.

**Main points:** Five decisions, after the rebuild of 2026-11-26 brought the construction into line with Lennart's
build (issue 2), the few-groups warning was accepted with its measured reason (issue 3), and issue 1 was closed and
rewritten for the new target as issue 8. Issue 8 sets the precedent the next computed target inherits, and issue 7
has the largest measured effect anyone found in the panel.

**Record judgment:** valid. The screening read the source correctly and its verdict stands. The build note of
2026-11-25 counted 402 lines lost and a between-family share of 54.2%, which the panel corrects to 401 and 54.3% (on
the values of 2026-11-26 the share is 55.3%); the record's own comments already carry those two, the entry-mean
heritability (0.789 on those values, 0.808 before them, against the 0.822 Diers et al. publish, not the 0.84 first
written) and the single marker whose 0.145 is the missingness pattern that labels the
cross rather than a QTL. The same corrections, and the naive call disagreement of 43.2% between the two genotype
matrices, are in the definition. The record's fields agree with the definition and none needs a mark.

**Issues for Andrej:**

1. **What does the exception for a target we fit ourselves say?**

   * **Problem:**
     - The target is a quantity we fit from the plot yields, not a column the source publishes, and the precedent
       sweep over 5,865 decisions found no other such target in the collection[^tp6].
     - The departure from the rule that says to keep the source's rows is recorded nowhere, so the next dataset with
       an estimated target inherits an unwritten licence[^split26].
     - The notes called the fit "the model of the data paper and of the package's `BLUP()`", half of which is
       refuted; the attribution is corrected, but the exception is still missing.
   * **Background:** the package publishes no line-value object, but it publishes the function that makes one
     (`BLUP()`, `lmer(Y ~ C + (1|E) + (1|G))` with the check index as `C`) and a documented `dereg = TRUE` switch
     that unshrinks it back to the kg/ha scale; our fit is that model with the environment and the line fixed.
   * **Effect on the task:** the quantity every model is scored on is ours, and two defensible builds of our own
     disagree within a family by 0.11 to 0.21 of the within-family SD, so what the exception says is what a later
     reviewer will read the number as; the ranking itself is stable, since every variant lands within 0.007 of
     the shipped score.
   * **Experiments:** the shipped target against three builds of the same line value, measured on all 5,143 lines
     (within-family correlation, mean over the 39 families with the minimum in brackets).

     | shipped target against | within-family r (min) | within-family difference SD |
     |---|---|---|
     | the package's shrunken `BLUP()` | 0.99915 (0.99657) | 48.6 kg/ha |
     | `G/r2 + ybar`, the de-regression in the usual order | 0.99998 (0.99995) | 1.5 kg/ha |
     | the package's literal `BLUP(dereg=TRUE)` | 0.90185 (0.76055) | 116.5 kg/ha |
     | the plain mean of a line's plots | 0.943 pooled | 99 kg/ha |

     `BLUP.R` adds the grand mean before dividing by the reliability (`BV = BV + mean(Y); if (dereg) BV = BV / r2`),
     so the package's literal output divides the grand mean by the reliability too and carries the line's plot count
     into the value:

     | what the literal output carries | value |
     |---|---|
     | the offset against the usual order, SD within a family (max) | 117 (194) kg/ha, against a within-family target SD of 236 |
     | its correlation with the line's plot count | -0.928 |
     | the plot count alone, scored on it by the declared metric | -0.483, against -0.100 on the shipped target |

   * **Consistency:** `superconductivity` kept the source's entries and counted each composition once with a weight,
     and `boreal_postfire_lichen_biomass` left 20 plots out rather than infer their target; both kept a published
     number, which this dataset cannot, because the source publishes none and its plot rows are not comparable (an
     environment effect spanning 2,692 kg/ha and a block effect of 422 kg/ha per index unit against a line SD of
     353, with a family missing up to 3 of the 18 environments).
   * **Panel:** the advocate measured a within-family correlation of 0.99998 against `BLUP(dereg=TRUE)` and called
     the target the package's own; the critic read `BLUP.R` and measured the plot-count offset the package's literal
     switch carries, and the mediator reproduced both and read the file, settling it for the critic.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Leave it as it is (implemented) | no exception line anywhere; the notes now attribute the fit to `BLUP()` and name the departures from the paper | nothing to write | the departure from the rule is unrecorded; the next estimated target inherits an unwritten licence |
     | B | Record the exception, calling the target the package's own `BLUP(dereg=TRUE)` | the advocate's original wording | short | false: a curator who runs it in R gets a value that agrees with ours at within-family r 0.90 |
     | C | Record the exception as drafted in the notes for the AI | names what is the source's and what is ours, and why ours | checkable in R; sets the narrow precedent that running an estimator the source defines is not inventing a target, while repairing its code is ours to own | the longest line in the notes |
     | D | Ship the package's literal `BLUP(dereg=TRUE)` output | takes the source's code as it stands | no exception beyond the rule | the plot count would carry half the within-family SD of the scored target and score -0.483 on the declared metric |

   * **Recommendation:** C, which is the only wording that is true in R and still claims the source's model form.
     **Decision:** record the exception as C, or prefer B or D?

   **Notes for the AI:** the exception line, for the record, the notes and the rule's Cases table:

   > **Exception to SPLIT-26 (2026-11-25, \<curator\>):** we do not ship the source's rows. The source publishes
   > 56,929 plot yields; we ship one value per line, fitted by us as `yield = mu + b * block index + environment +
   > line` by least squares. The fact that sets the case apart: a plot yield carries an environment effect spanning
   > 2,692 kg/ha and a block effect of 422 kg/ha per unit of the check index, against a line SD of 353, and a family
   > misses up to 3 of the 18 environments, so no weighting of plot-level scores removes the confound, while the
   > line is what the breeder acts on and is the source's own task unit. The model form is the source's: the
   > package's `BLUP()` is `lmer(Y ~ C + (1|E) + (1|G))` with the `CHECK()` index as `C`, and our fit is that model
   > with the environment and the line fixed, so the value keeps the kg/ha scale. The de-regression is ours, and
   > deliberately: `BLUP.R` adds the grand mean before dividing by the reliability (`BV = BV + mean(Y); if (dereg)
   > BV = BV / r2`), so the package's literal `dereg = TRUE` output divides the grand mean by the reliability too
   > and carries the line's plot count into the value. On the shipped lines that offset has a within-family SD of
   > 117 kg/ha (max 194) against a within-family target SD of 236, correlates -0.93 with the plot count, and makes
   > the plot count alone score -0.48 on the declared metric, against -0.10 on the shipped target. Our fit
   > reproduces the de-regression done in the usual order at within-family r 0.99998, difference SD 1.6 kg/ha, and
   > the package's shrunken `BLUP()` at 0.99915. Serves P3 (the breeder acts per line) and P4 (a trial bookkeeping
   > artefact is not what the metric should score).

   And one line for `curation_comments`: `BLUP(dereg = TRUE)` run in R does not return the shipped target, but the
   same ranking inside a family up to the plot-count offset, on a different scale, agreeing within a family at 0.90.

   **Answer (AI, 2026-11-26):** the construction changed with issue 2, so the exception this issue drafts has to
   describe the new one: each plot is corrected for its environment and for its field block, both measured on the
   plots of the six common checks (model 1 of Diers et al. 2018, the block effects shrunk by `vb / (vb + ve / n)`),
   and a line's corrected plots are averaged. The decision is untouched, since the target is still ours to compute
   and the model form is still the source's, but three statements above describe the superseded values.

   | statement above | what holds after 2026-11-26 |
   |---|---|
   | the target is `yield = mu + b * block index + environment + line`, by least squares | the target is the mean of a line's corrected plots; no grand mean and no slope is fitted over the line plots |
   | the three comparisons with the package's `BLUP()` (0.99915, 0.99998, 0.90185) | measured against the superseded values, which correlate 0.9925 pooled and 0.987 within a family with what ships; not re-run |
   | an environment effect spanning 2,692 kg/ha and a block effect of 422 kg/ha per index unit, against a line SD of 353 | the environment effects span 2,972 kg/ha and the shrunken block effects have an SD of 318 kg/ha, against a line SD of 354 |

   [^tp6]: **TP-6** (Must): "a better version the source itself defines replaces the current one ... a fix of our own
     invention is not a better version", so an estimator the source publishes may be run, while a repair of its code
     is ours and is recorded as ours.

   [^split26]: **SPLIT-26** (Should): "Keep the source's rows: deduplicating with averaged targets is a different
     dataset." Cases: superconductivity.

   **Andrej (2026-11-26, discuss):** Close this issue and rewrite it from scratch for the new target.

   **Resolved (2026-11-26, Andrej):** closed and asked again as issue 8. Nothing here is decided: the question was
   put against the target this definition no longer ships. Its options, its experiments and the exception text
   drafted in its notes all describe the superseded construction, a least-squares fit of
   `mu + b * block index + environment + line` over the 56,929 line plots, and they are void with it; so are the
   three comparisons with the package's `BLUP()`, measured on those values. The target that ships since the rebuild
   of 2026-11-26 corrects each plot for its environment and its field block on the check plots alone and averages a
   line's corrected plots, which is a different quantity and a different departure to word. Issue 8 asks the same
   question against it, with the measurements of the rebuild.

2. **Fit the environment effects on the check plots alone?**

   * **Problem:**
     - The environment effects of the target fit are estimated over all 56,929 line plots, so a test family's yields
       help set the training families' target values[^leak30].
     - The note kept it on "the model of the data paper and of the package", and the data-paper half is refuted and
       gone, so the keep now rests on the package's model form alone.
     - The fix is ours to make, is a few lines and costs nothing measurable.
   * **Effect on the task:** the tie is small and real, and it is our own cleaning rather than a property of the
     source's files, so it is the kind the remedy ladder asks us to remove when we can rebuild.
   * **Experiments:** the shift is measured by refitting the target with a whole test fold's 13 families left out,
     over 3 and 9 folds; the cost is the declared metric with the check-only variant shipped instead.

     | | measurement |
     |---|---|
     | shift of the training lines' values when a test fold's 13 families leave the fit | SD 4.4-4.7 kg/ha, max 14.5-28.9, correlation 0.99990-0.99993 |
     | that shift against the training line's own value | r +0.023, -0.041, -0.067 |
     | cost of the check-only fix on the declared metric | +0.0003 (9 folds) / -0.0012 (3 folds), against a fold SD of 0.012-0.028 |
     | agreement of the check-only variant with the shipped value | within-family r 0.9939 (min 0.969), difference SD 28.9 kg/ha |

   * **Consistency:** under the same tension `sf_permit_time` and `home_credit_default_risk` were rebuilt because
     they could be, and only the datasets that could not be rebuilt were kept with a note.
   * **Panel:** the critic measured the whole-task cost of the fix at 0.0012 and asked for it; the advocate conceded
     it; the split auditor measured the fold-scale shift and called the note the right rung for a weak tie.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep the all-plot fit with the note (implemented) | as today, with the wording corrected and the fold-scale numbers added | no rebuild | the stated reason was half-refuted; the precedent rebuilds what can be rebuilt |
     | B | Fit the environment effects on the check plots alone | removes the tie between a test family's yields and the training targets; every target value changes, so the folder is rebuilt | free in score; the mildest remedy that resolves it; matches the precedent | a rebuild, and the note still has to name the residual tie |
     | C | Keep the all-plot fit and record it as a written exception | makes the keep deliberate, with the fold-scale number | no rebuild | an exception where a free fix exists |

   * **Recommendation:** B. `mu` and the slope stay fitted over all line plots either way, so the note still names a
     residual tie; if the package's single fit is preferred, then C rather than A. **Decision:** take the check-only
     fix (B), or keep it as a written exception (C)?

   **Notes for the AI:** on B, `line_values` takes the environment effects from `check_effect`'s own plots rather
   than the line plots, `_decisions` gains the agreement with the shipped value, the notes drop the
   `Potential leak, kept on purpose:` bullet for one that names the residual `mu` and slope tie, and the folder is
   rebuilt on the curator's ask. On C, the bullet becomes an exception line with the fold-scale shift.

   **Resolved (2026-11-26, Andrej):** B, and one step further, as Lennart's build of this dataset does it: the
   environment effects and the field-block effects both come from the check plots alone, the block effects shrunk by
   `vb / (vb + ve / n)`, and the correction uses only the six checks grown across the trial, the 39 family founders
   left out (the founder-parent point of the column audit, closed with this one). A line's value is the mean of its
   own corrected plots, so no line's yield enters another line's value and the residual grand-mean and slope tie the
   recommendation named is gone with the slope. The `Potential leak, kept on purpose:` bullet is gone, the target,
   check and plain-mean bullets are rewritten, and `_decisions` compares the shipped value with three builds. Not
   built: no container exists for this folder.

   | what moved | before | after |
   |---|---|---|
   | line values (kg/ha) | 2,099 to 4,602, mean 3,607, SD 353 | 2,029 to 4,584, mean 3,578, SD 354 |
   | the two against each other | | pooled r 0.9925 (Spearman 0.9906), within family 0.987 (lowest family 0.956), difference SD 44 kg/ha and 39 within a family |
   | declared metric, 3 grouped folds | ridge 0.207, untuned LightGBM 0.223 | ridge 0.198 (per fold -0.002 to -0.017), LightGBM 0.229 (-0.011 to +0.036); either model moves 0.03 to 0.06 between folds |
   | the 39 founders taken into the correction | | r 0.9969, within family 0.9942, difference SD 27.8 kg/ha; the metric 0.005 higher for ridge and 0.001 lower for LightGBM |
   | entry-mean heritability | 0.809 | 0.789, against the 0.822 Diers et al. publish |
   | plain mean of a line's plots | r 0.943 (Spearman 0.928) | r 0.937 (Spearman 0.920), within family 0.893 |
   | between-family share of the variance | 54.3% | 55.3% |
   | `dataset check` | 0 errors, 1 warning, 1 info over 28 checks | unchanged |

   [^leak30]: **LEAK-30** (Must when strong, Should when weak): a transductive tie, "rebuild from the unprocessed
     values when the source has them; otherwise keep the dataset with a `Potential leak, kept on purpose:` note". Its
     tensions row records that the two datasets that could be rebuilt were rebuilt and only the others kept a note.

3. **Accept the few-groups warning at 39 families and 13 per fold?**

   * **Problem:**
     - The bundle check raises `groups_test_groups_few` and `dataset.py` carries no `accepted_check_warnings`
       attribute, so the warning reaches the curator unanswered[^acc].
     - The check's own hint asks for the signal across groups to be measured and the warning accepted with that
       reason, and the measurement exists only in the panel.
     - The attribute is empty because the workflow says a curator fills it, so this is a decision rather than an
       incomplete definition.
   * **Effect on the task:** nothing in the data changes; without the entry the warning is carried forward silently
     into every later reading of the folder.
   * **Experiments:** four model families on the 60 shipped splits, and a null that shuffles the yields inside each
     test family.

     | | measurement |
     |---|---|
     | units | 39 families, 13 per test fold, about 1,714 lines scored per fold |
     | model families beating the dummy on the declared metric | GBLUP, ridge, random forest and LightGBM, on 100% of folds |
     | standard error of the declared metric over 39 families | 0.018-0.019 against a mean of 0.21-0.25 |
     | families scoring positive | 38 of 39 |
     | within-family label permutation, 500 runs | mean +0.0002, SD 0.0135, max 0.043 (p = 0.002, z = 18.2) |

   * **Consistency:** accepted at `huesken_sirna_efficacy` (30 genes, 10 per fold), `airfoil_self_noise` (33 setups,
     11), `open_university` (22 presentations, 6-9) and `heart_disease` (3 sites), refused at `covertype` (3
     wilderness areas); at 39 and 13 this is the largest of them and the only one with a permutation test.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Leave `accepted_check_warnings` empty (implemented) | the state the workflow ends in | nothing to write | the warning reaches the next reader unanswered, while every precedent carries its text |
     | B | Accept the warning with the text in the notes for the AI | records the measured reason in the definition | matches every precedent; the strongest evidence of the five | none found |
     | C | Do not accept: 39 groups and 13 per fold are too few | the dataset does not ship | consistent with `covertype` | `covertype` had 3 groups; here four model families sit about 12 standard errors from zero |

   * **Recommendation:** B. **Decision:** accept with that text, or change it?

   **Notes for the AI:**

   ```python
   accepted_check_warnings = {
       "groups_test_groups_few": (
           "39 families, 13 per test fold and about 1,714 lines scored per fold. The signal across groups is "
           "measured, not assumed: GBLUP, ridge, random forest and LightGBM all beat the dummy on the declared "
           "metric on 100% of the folds; per-family r has SD 0.10 to 0.12, so the standard error of the metric "
           "over 39 families is 0.018 to 0.019 against a mean of 0.21 to 0.25, about 12 SE from zero; a null that "
           "shuffles the yields inside each test family (500 runs) gives mean +0.0002, SD 0.0135, max 0.043 "
           "(p = 0.002, z = 18.2), and 38 of 39 families score positive."
       ),
   }
   ```

   [^acc]: the house rule for the bundle checks: "A warning that is correct for the dataset goes into
     `accepted_check_warnings` with its reason (one per slug, filled by the curator once they have seen the
     warnings)". **SPLIT-27** (Should) asks for several model families scored per group with a permutation test
     before a small grouped task is judged.

   **Andrej (2026-11-26, change):** Option B: Accept the warning with the text in the notes for the AI.

   **Resolved (2026-11-26, Andrej):** B. `accepted_check_warnings` now carries `groups_test_groups_few` with the
   drafted text, and `dataset check` ends at 0 errors, 0 warnings and 1 info over 28 checks, the warning ignored
   rather than raised (it stood at 1 warning before). Every figure in that text depends on the target, so all of
   them were measured again on the values the rebuild of 2026-11-26 ships, over the 60 shipped splits, instead of
   being carried over; the units and the shape of the evidence are what the draft said, and the numbers move a
   little.

   | in the accepted text | drafted (superseded target) | measured again (shipped target) |
   |---|---|---|
   | units | 39 families, 13 per test fold, about 1,714 lines | unchanged: 13 families and 1,642 to 1,776 lines per fold, mean 1,714 |
   | model families beating the dummy | GBLUP, ridge, random forest, LightGBM, 100% of folds | unchanged, 60 of 60 for each (the dummy scores exactly 0 under this metric) |
   | per-family r, SD | 0.10 to 0.12 | 0.09 to 0.10 |
   | standard error over 39 families, against the mean | 0.018-0.019 against 0.21-0.25, about 12 SE from zero | 0.015-0.017 against 0.18-0.23, 12 to 16 SE from zero |
   | families scoring positive | 38 of 39 | 38 of 39 under ridge, 39 of 39 under the other three |
   | within-family label permutation, 500 runs | mean +0.0002, SD 0.0135, max 0.043 (p = 0.002, z = 18.2) | mean +0.0001, SD 0.0031, max 0.0089, the score 68 null SDs above it at the p = 0.002 floor of 500 runs |

   The permutation is the same test on another scale: each of the 500 runs is now scored over all 60 folds, as the
   models are, where the drafted figures are the spread of a single fold, so its SD is smaller and the distance in
   SDs larger. The models are untuned, as in the draft, so the levels are indicative and only the comparison with
   zero and with the null carries the argument.

4. **Write the reason for leaving the third release object unread, or take its 19th environment?**

   * **Problem:**
     - The package ships three data objects, and the definition reads one, rejects a second with a written reason
       and never mentions the third, `soyin`[^prov].
     - `soyin`'s IN_2014, 5,549 yields with complete check coverage, is a 19th environment of the same panel that
       the target fit never sees.
     - Refitting with it moves the shipped line values by more than any build sensitivity the notes record.
   * **Effect on the task:** no rows are gained and no scope is broken, but every line grown in Indiana has its
     target fitted on fewer plots than the source published, and a reviewer meets a silently ignored object.
   * **Experiments:** the object read and matched against the quality-assured table, and the target refitted with
     IN_2014 added as a 19th environment.

     | | measurement |
     |---|---|
     | `soyin` contents | 12,790 line plots (IN_2013, IN_2014, IN_2015) in bu/ac, plus `gen.in` (5,555 x 4,240, MaCH-imputed) |
     | IN_2013 against the quality-assured table | the same plots: 5,199 matched yields, ratio exactly 67.25 bu/ac to kg/ha, r = 0.9916 |
     | refitting the target with IN_2014 as a 19th environment | within-family r 0.9699 (min 0.933), pooled 0.9862, difference SD 58 kg/ha, about 3% of within-family variance |
     | lines recovered | zero: none of its 405 extra strains has a `gen.qa` row |
     | IN_2015 | 1,680 yields, 840 lines, no check plots, so the block index cannot be built there |

   * **Consistency:** `boreal_postfire_lichen_biomass` chose between two published measurements and wrote the reason;
     going to the origin rather than a derived copy is the `qsar_biodeg` and `nci_aids_antiviral_screen` pattern.
   * **Panel:** found by the column auditor, which read the package's own manual pages; nobody disputed that the
     drop is defensible, only that it is unwritten.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Read `soybase` only, with no mention of `soyin` (implemented) | as today | nothing to do | the largest unrecorded build sensitivity in the dataset, and a silently ignored source object |
     | B | Keep 18 environments and write the reason | documents the choice, with the 58 kg/ha sensitivity beside the 38 and 29 kg/ha ones | keeps the declared scope; adds no rows; cheap | the Indiana lines' values stay fitted on fewer plots than exist |
     | C | Add IN_2014 as a 19th environment, converted at 67.25 | a better-estimated target for the lines grown there; every target value changes and the folder is rebuilt | uses more of the source's own data | reopens the target for a 3% move, changes the declared scope sentence, and IN_2015 still cannot join |

   * **Recommendation:** B. The scope sentence already fences the task to one 2011-2013 network, no line is
     recovered, and C would reopen the target for a 3% move. **Decision:** write the reason (B), or take the 19th
     environment (C)?

   **Notes for the AI:** on B, one `curation_comments` bullet naming `soyin`, its three Indiana environments, the
   unit, the missing check plots in IN_2015, the imputed `gen.in`, the zero lines recovered and the 58 kg/ha
   sensitivity. On C, `_load_raw` gains the object, `line_values` converts bu/ac at 67.25 and the scope sentence,
   the row description and the split counts are rewritten before a rebuild.

   **Answer (AI, 2026-11-26):** the decision is untouched by the rebuild of that day, but the 58 kg/ha sensitivity
   above was measured on the superseded line values and was not re-run; the construction that ships now takes its
   environment and block effects from the six common checks, which IN_2014 also carries.

   [^prov]: **PROV-8** (Must): the source is where the data was first published, and the download instructions say
     which copy is read; **PROV-13** (Must): when a release is damaged, check whether the origin has the clean data.
     Neither forces reading every object a release ships, but a choice between the source's own measurements is
     written down (`boreal_postfire_lichen_biomass`).

5. **Keep the blank marker cells blank, and on what reason?**

   * **Problem:**
     - A marker is blank exactly when it does not segregate in that family, so the donor parent carries the common
       parent's allele and the line's genotype is determined by the design rather than unknown.
     - The notes justify keeping the blanks with "imputing would invent the call a breeder does not have either",
       which is false: the breeder does have it[^clean].
     - The blind reviewer, seeing only the data, voted to exclude the dataset over it.
   * **Background:** any fill that is constant inside a family-by-marker block adds exactly zero within-family
     variance, so it cannot move the declared metric; and the common parent IA3023 has no genotype row in `gen.qa`
     (the 37 non-line rows are the donor parents), so a fill would be inferred from the donor parents' own rows,
     themselves 24.5% missing, not read from the source.
   * **Effect on the task:** none on any score. It changes what ships, what the notes claim, and how safely the
     frame can be reused under a random split or a pooled metric.
   * **Experiments:** the block structure over all 168,168 family-by-marker blocks, and the fill measured end to end
     on the 60 shipped splits.

     | | measurement |
     |---|---|
     | family-by-marker blocks entirely blank | 41,304 of 168,168 = 24.56% |
     | blocks between 0.1% and 10% scored | 0 (10% to 90%: 280, 0.17%; 90% or more: 126,584) |
     | blocks with any call that are polymorphic within the family | 126,864 of 126,864 = 100.000% |
     | the mask within a family, against the calls | r -0.028 against +0.213 |
     | the mask pooled, against the genotype values | R^2 +0.1629 against +0.0016 |
     | family-mean imputation, end to end on the declared metric | 0.22900 to 0.22985, +0.0009 |
     | within-family variance added by any per-block fill | 0.000000 |
     | markers segregating in 2 or more families that carry both homozygotes in every such family | 500 of 500 |

   * **Consistency:** keeping unknown cells missing and the row intact is the pattern of the cleaning rules, and the
     benchmark's pipeline is what imputes; a repair from the origin outranks cleaning around damage, but there is no
     origin column to read here, and a fix of our own invention does not replace what the source published.
   * **Panel:** the blind reviewer found it from the data alone and called it decisive; the column auditor measured
     the same mask within the family, where the metric lives; the task gamer measured the fill end to end. All three
     numbers agree, and the mediator overruled the exclusion because every number behind it is pooled.
   * **Unknown:** whether a breeder meets the same unscored-marker pattern in a new cross is sound inference (a new
     cross of the same common parent, genotyped on the same chip, is scored where it segregates) but it is
     inference, not a measurement, and the rewritten sentence should say so.
   * **Depends on:** issue 6, the metric: the declared per-family metric is what makes the blanks a documentation
     question rather than a recording one, so if the source's pooled metric is restored there, this issue reopens
     on that basis (the measurements are in issue 6's dependency table).
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep the blanks, keep the stated reason (implemented) | the notes go on saying "imputing would invent the call a breeder does not have either"; the block structure and the pooled numbers are already written down beside it | nothing to do | the panel refuted that reason, so marking this row keeps a sentence we know to be false: the breeder does know these calls |
     | B | Keep the blanks and replace the reason | says the blanks are the design's non-segregating blocks and that filling them moves the declared metric by +0.0009 | faithful to what the source published; costs no score; the warning for a re-user is already in the notes | the frame still carries a family fingerprint for anyone who re-splits it |
     | C | Fill the non-segregating blocks with the inferred common-parent allele | reconstructs the common parent's allele as the complement of each donor parent's row; the folder is rebuilt | removes the pooled mask artefact; the matrix becomes what the biology says it is | the inference is ours, the donor rows are themselves 24.5% missing, and the declared metric does not move |
     | D | Use the package's own `impute="FM"` or `"EXP"` | a hidden-Markov or expectation fill over everything; the folder is rebuilt | the source's own code path | a different operation from the one the finding argues for; invents calls inside segregating blocks too |

   * **Recommendation:** B. The outcome of A is right and only its reason is wrong; C is defensible biology but is
     our construction for a change that moves no score, and D is not the operation the finding argues for.
     **Decision:** keep the blanks with the corrected reason (B), or fill them (C or D)?

   **Notes for the AI:** on B, the `_clean` comment and the missing-calls bullet replace "imputing would invent the
   call a breeder does not have either" with: the blanks are the cross's non-segregating loci, which the design
   deletes rather than fails to call, so the breeder does know them; they stay because any per-block fill is ours to
   invent, changes no score and would depart from what the source published. On C or D, `_clean` gains the fill, the
   missing-share decision is rewritten and the folder is rebuilt on the curator's ask.

   [^clean]: **CLEAN-2** (Must): "Leave to the benchmark's pipeline what it does ... no imputation"; **CLEAN-11**
     (Should): impossible values become missing and the row stays. **CLEAN-7** (Must) is the rule the definition
     cites, against computing a value from statistics over all rows, which is what a family-mean fill would be.

6. **Record the metric overrule as an exception?**

   * **Problem:**
     - The source names Pearson's r pooled over the test lines as the criterion it ranks by, so it has a deliberate
       original and we overrule it[^met5].
     - The declaration names that original, so the Must is met, but the departure from the Should is recorded
       nowhere[^met11].
     - Two earlier datasets departed for the same reason, which makes this the third and the point at which an
       amendment is proposed rather than another exception written.
   * **Effect on the task:** none on the data or the score; left unwritten, the next dataset of this kind meets
     three precedents and no rule.
   * **Experiments:** the between-family share of the target's variance, and what a pooled score would reward.

     | | measurement |
     |---|---|
     | share of line-value variance between families | 55.3% on the values of 2026-11-26 (54.3% before them), and Diers et al. publish 0.57 from their own trials |
     | family-mean-only oracle, pooled r / RMSE | 0.683 / 238 kg/ha against ridge's 0.236 / 360 |
     | the same oracle within a family | exactly 0 |
     | the non-recurrent parent's own trial yield against the family mean | r = 0.937 over 38 families |
     | pooled, the mask of unscored calls against the genotype values | R^2 +0.1629 against +0.0016 |
     | ridge, pooled against per family | 0.236 against 0.239 |

   * **Consistency:** `protein_model_quality_rf_pcp` and `huesken_sirna_efficacy` are logged as exception rows for
     exactly this reason, and `superconductivity` and `loan_default_prediction_imperial_college` wrote down an
     overrule of a source metric. Two things set this case apart: the effect is far larger, and the source has a
     unique original rather than a fallback.
   * **Panel:** the practitioner argued the metric is literally the term the breeder's equation multiplies and
     measured the realized gain agreeing with it to 5%; the critic did not dispute the metric, only the missing
     record of the departure; the precedent checker counted it as the third of one reason.
   * **Depends on:** issue 5, whether the blank marker cells stay blank, rests on the metric decided here. The
     blank pattern names the cross exactly: clustering on the missing-value mask alone recovers the 39 families at
     adjusted Rand 1.0000, and all 4,185 distinct missingness patterns over the 5,143 lines lie inside one family.
     What that is worth depends on the score.

     | | pooled, the source's metric | within a family, the declared metric |
     |---|---|---|
     | the mask against the genotype values | R^2 +0.163 against +0.002 | r -0.028 against the calls' +0.213 |
     | a held-out family's mean, from the missingness profile | r 0.665 against 0.346 from the mean genotype | anything constant inside a family scores 0 |
     | family-mean imputation of the blank blocks, end to end | not measured | +0.0009 |

     So the metric decides more than the score: under the declared per-family metric the blanks are a question
     about what the notes claim (issue 5), and under a pooled one they would be a question about what was
     recorded. If the pooled metric is ever restored (option D), issue 5 reopens on that basis, and so does the
     blind reviewer's vote to exclude, which was measured on exactly that pooled footing.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Leave the metric reason as it is (implemented) | names the original and now also what a pooled score would reward; records no exception | nothing to write | a Should is departed from without the record the rule asks for |
     | B | Record the exception here, with the amendment raised as a cross-dataset item | writes this case down and puts the rule change where it belongs | keeps this record about this dataset; the cross item is already written | the rule stays unchanged until that item is decided |
     | C | Record the exception and amend the rule in the same change | settles the rule now | reaches the three datasets in one pass | an amendment decided inside one dataset's review, and the decision register has to be re-walked |
     | D | Declare pooled Pearson's r, the source's metric | follows the rule and drops the overrule | no exception at all | scores a cross ranking the breeder reads off the parents at r = 0.937, and rewards missing-value handling (pooled R^2 +0.1629 from the mask alone) |

   * **Recommendation:** B; the amendment spans three datasets and is raised in the working copy's cross-dataset
     file. **Decision:** B, or amend the rule now (C)?

   **Notes for the AI:** on B, an exception row in the metric rules' Cases table naming this dataset, the reason and
   the measured effect, plus a `curation_comments` line; the amendment itself is the cross-dataset item "Amend the
   source-metric rule for a grouped ranking". On D, the metric becomes `pearsonr` and the splits comment, the
   grouping definition and the notes are rewritten.

   [^met5]: **MET-5** (Should): "A paper's metric is the source's metric only when it is one deliberate choice: the
     paper names it as the criterion it ranks, tunes or selects models by." Azodi et al. rank by Pearson's r "as it
     is the standard metric for GP performance", so the source has a unique original here.

   [^met11]: **MET-11** (Must): every metric has one origin, and the notes name the original whenever the declared
     metric is not exactly it. Departing from a Should is recorded as an exception, and the third exception of one
     reason is when an amendment is proposed.

7. **A public companion file holds another derivation of the target: record it, or hold the dataset back?**

   * **Problem:**
     - The Dryad and Zenodo record this dataset links holds a different derivation of the same trait for the same
       lines, under CC0[^prov15].
     - Its lines can be matched to ours on the markers both files share, with no identifier needed.
     - A clean lookup scores far above any honest model on the declared metric.
   * **Background:** that derived cut is the one the definition deliberately does not read, because its yield is off
     the kg/ha scale; that is what makes it a noisy independent copy of the test label rather than a competing
     build. The exposure is generic to any dataset rebuilt from a source whose derived copy is public, and the
     mechanism is raised as a cross-dataset item; what is specific here is the size, because the honest signal is
     weak (r about 0.3) while the public copy of the label is strong (r about 0.9).
   * **Effect on the task:** the honest ranking of honest models is unaffected, but a leaderboard open to the web
     can be topped by a join, and there is no remedy that keeps the task, since the markers are the features and the
     line identifiers are in the public file too.
   * **Experiments:** measured by the task gamer, which had only the participant kit and the web.

     | | measurement |
     |---|---|
     | shared markers between the two files | 4,230 of our 4,312 |
     | test rows matched to a published line, by genotype alone | 91.9% (median agreement 0.9993, median margin over the runner-up 0.3007) |
     | blending the looked-up yield with the best honest model | 0.30848 to 0.399 on the declared metric |
     | best honest model / plain ridge | 0.30848 / 0.22900 |
     | ceiling of a clean lookup: within-family r between our target and an unadjusted line mean | 0.8991 (min 0.597, max 0.985); pooled 0.9437 |

     The 0.399 is a lower bound: the match ran on 255 well-called markers, so about 8% of its matches are wrong (its
     pooled correlation with the published values is 0.627 where a correct identifier join gives 0.925). A
     participant who joins on the line ids reaches the ceiling row, about three times the best honest model.
   * **Consistency:** no rule covers a public copy of the target; our leak rules govern the shipped table and the
     split, and the remedy ladder has no rung that removes a file from the internet. The nearest practice is to
     record a derived copy's problems in the record of the dataset it concerns.
   * **Panel:** found by the task gamer from the kit and the web; the blind reviewer independently flagged the same
     file from the other direction, as a possible duplicate of the benchmark's own cut.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Say nothing (implemented) | the notes name the file as a rejected cut, not as a label source | nothing to do | the benchmark's operators cannot know their leaderboard is open to a threefold lookup |
     | B | Record it in the notes and the record, with the measured size | documents an exposure we cannot remove; the generic mechanism is already a cross-dataset item | honest about what a score here means; warns every later reader; the cross item makes the next case cheap | a published note tells a participant where to look |
     | C | Drop or perturb the markers that make the join cheap | breaks the genotype match; the folder is rebuilt | raises the cost of the join | destroys the task; the line ids are in the public file anyway, and obscurity is not a control |
     | D | Do not ship the dataset | removes the exposure | the leaderboard cannot be gamed | the task, the split and the metric are sound, and the same argument would retire every dataset rebuilt from a public source |

   * **Recommendation:** B. The exposure is real and unfixable, and it is a fact about what a score on this dataset
     means rather than a defect of the data. **Decision:** record it (B), or is this a reason to hold the dataset
     back (D)?

   **Notes for the AI:** on B, one `curation_comments` bullet under the version note: the derived cut holds a
   different derivation of the same trait for the same lines, 4,230 of our markers are shared so the lines match by
   genotype alone for 91.9% of test rows, a blend with the best honest model reaches 0.399 against 0.308, and a
   clean identifier join would reach about 0.9 within a family; plus one line in the record's comments. On D, the
   record's suggestion changes and the folder is removed with a CHANGELOG entry.

   **Answer (AI, 2026-11-26):** the exposure is unchanged by the rebuild of that day and the ceiling barely moves:
   against the line values that ship now, an unadjusted line mean correlates 0.893 within a family (0.937 pooled),
   where the row above measured 0.8991 and 0.9437 on the superseded values. The blend and the match rate were not
   re-run.

   [^prov15]: **PROV-15** (Must): a problem of another copy is noted in the record of the dataset it concerns, so it
     can be reported later, and raised as an issue only when it changes one of our decisions. Here it changes what a
     score on this dataset means, which is why it is an issue.

8. **What does the exception for the line value we compute ourselves say?**

   * **Problem:**
     - The source publishes 56,929 plot yields and no line value, so the quantity every model is scored on is one
       we compute[^own].
     - The rule that says to keep the source's rows is departed from with nothing written down that records it, so
       the next dataset with a computed target inherits an unwritten licence[^keeprows].
     - Issue 1 asked this against the superseded construction and was closed on 2026-11-26, so the wording has to be
       written again for the target as it stands.
   * **Background:** The target that ships since the rebuild of 2026-11-26 corrects each plot for its environment
     and for its field block, both estimated on the plots of the six checks grown across the whole trial (IA3023
     and five cultivars, 7,294 plots filling all 1,707 blocks; model 1 of Diers et al. 2018), with the block
     effects shrunk by `vb / (vb + ve / n)`, and a line's value is the mean of its own corrected plots. The 39
     family founders are left out of that check set, 38 of them standing in one family's blocks only and LD02-4485
     fathering family 12 while serving as a general check in 18 families. No line's yield enters another line's
     value.
   * **Effect on the task:** What the exception says is what a later reviewer reads the shipped number as; the
     construction itself is settled and moved no decision, the new values agreeing with the superseded ones at
     pooled r 0.9925 and the declared metric by less than a fold's spread.
   * **Experiments:** the shipped line values, and what they are against the alternatives (all 5,143 lines, 39
     families).

     | measurement | value |
     |---|---|
     | shipped line values | 2,029 to 4,584 kg/ha, mean 3,578, SD 354 (237 within a family) |
     | against the superseded values | pooled r 0.9925, within family 0.987, difference SD 44 kg/ha |
     | the declared metric, per fold | ridge -0.002 to -0.017, LightGBM -0.011 to +0.036 |
     | the 39 founders taken back into the correction | r 0.9969, difference SD 27.8 kg/ha |
     | the plain mean of a line's raw plots | r 0.937 pooled, 0.893 within a family |
     | entry-mean heritability | 0.789, against the 0.822 Diers et al. publish |

     A plot yield is not comparable with another plot's, which is why the correction is made at all:

     | what a plot yield carries | size |
     |---|---|
     | the environment, over the 18 of the trial | a span of 2,972 kg/ha |
     | the field block, after shrinkage | SD 318 kg/ha |
     | the line itself | SD 354 kg/ha |

     A family misses up to 3 of the 18 environments, so the mix a line was grown in differs from the next line's.
   * **Consistency:** `superconductivity` kept the source's entries and counted each composition once with a
     scoring weight, and `boreal_postfire_lichen_biomass` left 20 plots out rather than infer their target; both
     could keep a published number, which this dataset cannot, the source publishing none.
   * **Panel:** The attribution dispute the panel settled is not reopened here: the advocate called the target the
     package's own `BLUP(dereg=TRUE)`, the critic read `BLUP.R` and measured the plot-count offset that switch
     carries, and the mediator settled it for the critic; what is open is only the wording of the departure.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep the computed line value and record the exception (implemented) | nothing in the data; the exception goes into the record, the definition's notes and a cases row of the splits rules | the line is what the breeder acts on and is the source's own task unit; both correction terms come from the checks, so no line's yield enters another's; the departure becomes checkable | one more exception to carry |
     | B | Ship the source's plot rows | 56,929 rows, the raw plot yield as the target, the line as a column | the source's rows as they are, with no estimate of ours in the target | the environment span and the block effects are as large as the line effect, so models would be scored on trial bookkeeping; a family misses up to 3 of the 18 environments, and no weighting removes that confound |
     | C | Ship a plain per-line mean | one row per line, the mean of its raw plots | the simplest computation, and nothing is fitted | the mean carries each line's own mix of environments and blocks (r 0.937 with the shipped value, 0.893 within a family), so lines are compared across unequal trials |

   * **Recommendation:** A. The plots are not comparable: an environment span of 2,972 kg/ha and block effects of
     SD 318 stand against a line SD of 354, so B scores bookkeeping and C leaves it in the target, while the line
     is the unit the breeder and the source both act on. **Decision:** A, B or C?

   **Notes for the AI:** on A, the exception line, for the record's comments, the definition's notes and the rule's
   Cases table:

   > **Exception to SPLIT-26 (2026-11-26, \<curator\>):** we do not ship the source's rows. The source publishes
   > 56,929 plot yields and no line value; we ship one row per line, holding a value we compute: each plot is
   > corrected for its environment and for its field block, both estimated on the plots of the six checks grown
   > across the trial (model 1 of Diers et al. 2018, the block effects shrunk by `vb / (vb + ve / n)` over 1,707
   > blocks, the 39 family founders left out of the check set), and a line's value is the mean of its own corrected
   > plots, so no line's yield enters another line's value. The fact that sets the case apart: a plot yield carries
   > an environment effect spanning 2,972 kg/ha and a shrunken block effect of SD 318 kg/ha against a line SD of
   > 354, and a family misses up to 3 of the 18 environments, so no weighting of plot-level scores removes the
   > confound, while the line is what the breeder acts on and is the source's own task unit. The model form is the
   > source's, the data paper's model 1; the choice of which checks stand in it and the shrinkage are ours. The
   > shipped values run 2,029 to 4,584 kg/ha (mean 3,578, SD 354, 237 within a family), reach an entry-mean
   > heritability of 0.789 against the 0.822 the data paper publishes, and agree with a plain mean of a line's raw
   > plots at r 0.937 pooled and 0.893 within a family. Serves P3 (the breeder acts per line) and P4 (a trial
   > bookkeeping artefact is not what the metric should score).

   And one line for `curation_comments`: the line value is ours to compute, the source publishing none, and it is
   the data paper's model 1 run on the checks alone, not an object the package returns.

   [^own]: **TP-6** (Must): "a better version the source itself defines replaces the current one ... a fix of our
     own invention is not a better version", so a model form the source defines may be run, while the choices
     inside it are ours and are recorded as ours.

   [^keeprows]: **SPLIT-26** (Should): "Keep the source's rows: deduplicating with averaged targets is a different
     dataset." Cases: superconductivity. **SPLIT-23** (Must), which outranks it: the source's use case decides what
     one prediction is.

**Review panel:** ship after changes (mediator). Two of its points are closed by the rebuild of 2026-11-26: the
check-only environment effects (issue 2) and the family founders in the check index. Full tier, 11 roles: claim
auditor, column auditor, split auditor,
domain practitioner, blind reviewer, task gamer and precedent checker in phase A, an advocate and a critic with one
rebuttal each, the mediator, and the review editor that applied the result. Claims: 54 audited, 45 hold, 4 refuted, 3
hold with a correction, 2 untested. Columns: 4,314 audited, 0 flagged, 4 documentation gaps. Blind review: exclude as
prepared, voted on a pooled score the task does not use; its finding that the blank marker cells are deleted known
values stands and is issue 5. Task gamer: one new exploit above the honest baseline (a public companion file, +0.09
measured and about +0.6 at the ceiling, issue 7), one known but unrecorded (within-family centring, +0.0795, applied),
and seven attacks that found nothing. Agreed: the use case, the split, the metric, the release, and the leak findings
inside the shipped data. Disputed and settled by measurement: whether the shipped target is the package's own
`BLUP(dereg=TRUE)` (it is not, issue 1), the direction of the germplasm gap (the breadth makes the declared metric
harder, applied), and the blind reviewer's exclusion (overruled, issue 5).

<details><summary>Claim auditor</summary>

54 claims re-derived from the raw files rather than the probe logs, with the package re-downloaded (its sha256 matches
the declared one), the original `soynam` objects converted for the version comparison and the Azodi cut downloaded
from Zenodo. No validity failure found and nothing that changes the verdict.

**Holding.** The source publishes plots and no line-value object. The fit reproduces: 56,929 plots with a yield, b =
422.1 kg/ha per index unit, environment effects -1,204.7 (MI 2012) to +1,487.3 (NE 2011) spanning 2,692.0, plot
residual SD 512.7, line values 2,099.1 to 4,602.2 (mean 3,607.4, SD 353.3), 11.0 plots a line; the plain mean
correlates 0.9430 and a no-block fit 0.9617. `check_effect` is line for line the package's `CHECK()` and reads only
check rows. Each of the 1,707 blocks belongs to exactly one family, so the block correction is family-local. The
quality-assured release is the right one, and more strongly than stated: the original `data.line`'s block column takes
18 values, one per environment. 5,143 x 4,312 confirmed, 39 families of 98 to 140, 25.648% unscored, 6.48%
heterozygous, no constant, all-missing or duplicate marker and no duplicate line. Splits enumerated: 20 repeats x 3
folds = 60, every fold exactly 13 test families, zero family and zero row overlap on all 60. The metric is finite on
all 60 folds and a constant prediction scores exactly 0.

| Refuted or corrected | What the audit found |
|---|---|
| the QTL reading of `Gm19_40068456_A_G` | the marker is scored in 1,928 of 5,143 lines; "missing against scored" alone explains R^2 0.197 of its in-sample 0.200, and among lines with a call the dose explains 0.0078 pooled and 0.0022 within family |
| "the model of the data paper" | `BLUP()` is exact, but Diers et al. is two stages, blocks as BLUPs from 10 check varieties with a planting-date covariate, the entry random and no environment term |
| "45 check cultivars" | 38 of the 45 appear in the blocks of one family only, as its founder parent; 4 are near-ubiquitous and 3 more cover 18 families |
| entry-mean heritability 0.84 | double-counts the plot error over n; corrected 0.808, and Diers et al. Table 2 publishes 0.822 |
| "removes the dependency entirely" | `mu` and the slope are still estimated over all line plots in that variant |
| three arithmetic slips | 19 Zenodo files not 20, 401 lines lost not 402, 43.2% naive call disagreement not 44% |

**Untested:** whether both genotype rows of the 70 mixed-up lines match their own family best; and whether a breeder
meets the same unscored-marker pattern in a new cross, a domain judgment the missingness defence rests on.

**Also found.** The Azodi cut's yield correlates 0.971 with the plain mean of a line's plots and only 0.925 with our
block-corrected value, so it behaves like an unadjusted mean; its README and Methods both say the phenotypes were
normalized between 0 and 1 and the file is standardized. Family 46 is the source's own quality decision: Diers et al.
removed it because its lines were genotypically identical with the female founder. The missingness pattern alone
identifies the family: 4,185 distinct patterns over 5,143 lines, every one inside a single family.

</details>

<details><summary>Column auditor</summary>

4,314 columns audited against the package's own manual pages; the dtype probe flags 0 of 4,312. The six plot traits
are absent, the target's construction columns are not in the frame and could not be, and no column from after the
prediction point reaches it.

**Four documentation gaps, all now written down or raised.**

| Gap | Measurement | Where it went |
|---|---|---|
| the unread third release object `soyin` | 12,790 Indiana line plots in bu/ac plus an imputed genotype matrix; refitting with IN_2014 moves line values by within-family r 0.9699, difference SD 58 kg/ha; zero lines recovered | issue 4 |
| the dropped plot traits have no number | the six adjusted traits score +0.391 on the declared metric against the markers' +0.213, R8 alone +0.168, stacked +0.332 (+0.12, +56%) | the prediction-point note |
| `set` is not named as considered and rejected | a per-line maturity group (5,149 of 5,174 lines keep one letter), within-family R^2 0.1157 on the target and 0.6044 on adjusted R8 | its own note, with the shuffle |
| the missing-indicator note quotes a pooled number | within a family the indicators score r -0.028 against the calls' +0.213; 89.6% of the variance of a line's missing share is between families | the missing-calls note |

**Also.** The planting-date covariate of Diers et al. is not in the quality-assured release at all and is constant
within an environment (0 to 3 dates per environment, 1.02 per environment-by-block), so the environment term absorbs
it and that departure from the paper is immaterial; neither release supports the paper's exact model. The plot count
per line scores pooled r -0.108 and within family -0.100, about half what the markers earn, and is correctly not a
feature, not a scoring column and not a weight. The quality-assured marker selection is label-free (missingness and
segregation patterns), so it is at most the weak unsupervised end of the scaling rule. Column verdicts: the target
float64 in kg/ha with no missing values, `family` int16 over 39 levels as the group column, and 4,312 markers in
exactly {0, 1, 2} plus missing, every marker scored in at least 4 families, no outcome-driven missingness behind the
target.

</details>

<details><summary>Split auditor</summary>

Walked the decision tree and ended at the leaf the definition declares, with no departure and no forced leaf: an
experimental-results collection, a use case that meets a kind the data does not contain, and a family key the data
computes, giving grouped splits that hold out whole families. The repeat tag is consumed before the split, since the
plots are aggregated to one row per line, and the no-time-dimension tag holds (the time probe finds nothing, and 38
of 39 families were grown in all three years).

**The source's split is valid for its own framing and rightly departed from.**

| split | model | within-family r | pooled r | R^2 |
|---|---|---|---|---|
| shipped, family held out | ridge | 0.245 | 0.209 | -0.02 |
| shipped, family held out | LightGBM | 0.212 | 0.433 | 0.094 |
| source's random split over lines | ridge | 0.281 | 0.402 | 0.161 |
| source's random split over lines | LightGBM | 0.329 | 0.769 | 0.591 |

The R^2 gap the splits comment quoted is mostly the family-mean shortcut: on the declared metric the departure costs
0.036 (ridge) or 0.117 (LightGBM), which is now what the comment says.

**Few groups.** The training side does vary: 60 distinct train sides and 60 distinct test-fold compositions, pairwise
Jaccard of the train sides 0.497, every family tested exactly 20 times. Precision is fine (per-family r SD 0.10 to
0.12, so a standard error of 0.018 to 0.019 against a mean of 0.21 to 0.25), and a within-family permutation over 500
runs gives p = 0.002, z = 18.2. The warning is acceptable but was not accepted: issue 3.

**The transductive tie is weak.** Refitting with a test fold's 13 families left out moves training values by SD 4.4 to
4.7 kg/ha, correlation 0.9999, uncorrelated with the line's own value; the channel is 18 environment scalars shared by
thousands of plots. Its own check-only reconstruction agrees with the shipped value at 0.9967, not the 0.9990 the note
quoted, which is specific to the builder's variant; both numbers and the variant they belong to are now in the note.

**The context is worth measuring.** Centring each marker inside its family lifts ridge from 0.239 to about 0.30, about
+0.06, using only the test family's own feature rows; the metric is invariant to a per-family affine shift of the
predictions, so this is genuine transductive learning and not a trick on the score. The group column is fully
inferable from the features (1-NN on the missing pattern puts 100.0% of lines next to their own family), which is not
a leak under this split but would make a random split leaked twice over.

**Recommendation:** keep the leaf and the grouping, accept the few-groups warning with the drafted reason, and accept
the half-sib limit inside the grouping text rather than raising it (every test line has half-sibs in training, since
all 39 families share one parent). No re-split, gap or filter.

</details>

<details><summary>Domain practitioner</summary>

Played a soybean breeder running genomic selection: the fit is approximate, the model is worth using, and the metric
is right.

**The fit.** The inputs are what the breeder holds, the target is the number they select on, and the split is a
published validation design; the real gap is the germplasm, not either of the two the definition named. The shared
recurrent parent is the setting of any crossing block, and a recomputed label on the source's stated model and scale
is not an unverified label definition. Seven of the 38 non-recurrent parents are exotic accessions whose families
average well below the elite ones, so predictive ability here does not read as a breeder's at-home accuracy.

**Would a breeder use it.** At within-family r = 0.236 and top-10% selection the measured realized gain is 93 kg/ha
against the 389 a perfect ranking would get, and the breeder's equation predicts 98: agreement to 5%, about 1.4 bu/ac
of free gain per cycle. Holding out whole crosses costs about 0.025 in r against a random split, within noise.

| design | within-family r | pooled r |
|---|---|---|
| whole families held out (shipped) | 0.239 +- 0.024 | 0.220 +- 0.020 |
| random lines, sibs in training | 0.264 +- 0.027 | 0.305 +- 0.028 |
| 25% of each cross phenotyped first | 0.212 +- 0.010 | 0.199 +- 0.004 |

**What a breeder would check.** Maturity: within family the adjusted yield correlates 0.248 with adjusted R8 and the
model's ability falls only from 0.236 to 0.211 when yield is residualized on R8, so the task is yield and not
maturity. The sets inside a family are maturity groups, not field positions (they explain 60.4% of within-family
adjusted R8), which is what decides the release question, and the check-based block correction halves their footprint
in the scored variance (25.2% to 11.6%). The pre-shuffle row position scores 0.134 on the declared metric because the
line order tracks the maturity set, so the shuffle is load-bearing.

**The metric.** Within-family Pearson r is literally the term the breeder's equation multiplies, and it ranks models
the way the decision does: the best model by the declared metric is also the best by realized top-10% selection
differential and ties for best on top-decile hit rate. Pooled Pearson credits a model for a cross ranking the breeder
already reads off the parents (the non-recurrent parent's own trial yield predicts the family mean at r = 0.937);
RMSE has the same problem and no breeder acts on an absolute prediction; selection accuracy and response to selection
are monotone in the declared metric. Plots per line as a training weight: no, the reliability band is 0.810 to 0.860
over 90% of rows, a 6% ripple that costs a scoring column and a trap, since the count correlates -0.10 with the
target.

</details>

<details><summary>Blind reviewer</summary>

Saw only the shipped frame, a task description and the public web, and voted **exclude as prepared**. It read the task
correctly without our notes ("every feature is available before the label exists"), identified the provenance as the
package's quality-assured genotypes joined to yield BLUPs rather than the Dryad copy, and confirmed the data is real
and correctly formed (all 20 chromosomes, positions sorted and unique, heterozygote frequency right for these lines,
no ordering leak, no exact duplicate rows).

**Its decisive finding, which stands.** The missing cells are known values: a marker is blank exactly when it does not
segregate in that family, so the true genotype is determined. Of the observed family-by-marker blocks, 100.000% are
polymorphic within their family, within-family allele frequency where observed is a median 0.504 with none below 0.1,
and pooled minor allele frequency has a minimum of 0.356 with zero markers below 0.05, which no real panel looks like
unless the non-segregating cells were deleted.

| input, pooled, kernel ridge on the shipped grouped split | RMSE kg/ha | r | R^2 |
|---|---|---|---|
| train-mean baseline | 356.3 | | 0.000 |
| genotype values only | 348.8 | +0.233 | +0.0016 |
| the missing mask only | 319.1 | +0.485 | +0.1629 |
| genotype and mask | 309.4 | +0.506 | |
| oracle: the true held-out family mean | 238.6 | | +0.5412 |

**Why the vote did not survive.** Its task description named no metric, so every number it reports is pooled, while
the declared metric scores within the family, where the same mask is worth r -0.028 against the calls' +0.213. Its
proposed fix cannot move the declared metric by construction (any per-block fill adds zero within-family variance;
family-mean imputation measures +0.0009 end to end), and it is not the package's own option: the common parent has no
genotype row in the release, so the allele would be inferred from the donor parents' rows rather than read.

**Its other concerns, as ruled.** Genotype-only pooled R^2 below the benchmark's bar: an argument for the metric, not
a failure, since four model families beat the dummy on 100% of folds on the declared one. The grouped regime discards
the real signal: the split follows the application, and the splits comment says so. A probable duplicate with the
benchmark's own cut: not a duplicate in our collection, but the file it names is what issue 7 is about. 60 splits over
39 units: already the splits comment's own sentence and issue 3's evidence. "High-dimensional" is nominal (kernel
effective rank 66): true, and changes nothing. The BLUPs are shrunken with no weight column: wrong for this build,
whose target is explicitly unshrunk. The missingness profile predicts a held-out family's mean at r +0.665: benign,
since the predictive part is the pattern that names the donor parent and the parent's own yield predicts the family
mean at 0.937, and it earns nothing on a metric that scores zero for anything constant inside a family. 21
near-duplicate line pairs: all within family, maximum cross-family identity 0.860, so no pair spans the split. Two
licences listed: fair, and now one clause in the notes.

</details>

<details><summary>Task gamer</summary>

Played a participant with the kit and the web. Honest baselines over the 60 shipped splits: LightGBM untuned 0.21272,
ridge 0.22900 at alpha 1e3 and 0.23577 at 1e4, and ridge on within-family-centred features 0.30848, the best honest
model. An extra column of random numbers moves the 60-split mean by at most 0.0002.

| Exploit | Measured | Verdict |
|---|---|---|
| public companion file: join the kit to the CC0 Dryad record on the 4,230 shared markers | a published line id for 91.9% of test rows; blending its yield with the best honest model lifts 0.30848 to 0.399 | new, issue 7 |
| within-family centring of the features | 0.22900 to 0.30848, within 0.0006 of the oracle family-mean run | licensed by the declared context, size was unrecorded; now written down |
| format and row statistics (missingness, heterozygosity, dosage means) | 0.22900 to 0.23761; a format-only model alone 0.07103 | known, immaterial; the het and call-rate parts are genuine genetics |
| pre-shuffle row position | 0.22788, -0.0011 | closed by the shuffle, which the practitioner measured at 0.134 unshuffled |
| transductive standardisation over all rows | 0.22821, -0.0008 | matches the note |
| family-mean imputation of the blank blocks | 0.22985, +0.0009 | settles the blank-cell question |
| marker selection using all labels | 0.11228 against 0.10374 on train labels only | far below honest; nothing found |
| IBS k-NN at k = 25 and k = 100 | 0.07692 / 0.10505 | far below honest; nothing found |
| cross-split label memorisation | exactly 1.000 | not an exploit of this dataset: the panel's own kit hands all 60 splits with the full target column, which a participant never receives |

Fifteen attacks in all found nothing: row order and position, target format (no rounding grid, nine byte-identical
yield pairs all within a family), a format-only model, zero exact duplicate genotype rows and zero cross-family pairs
above 0.90 identity, no shared founders between family codes, k-NN label copying across families, gaming the metric's
zero floor, within-family rank-gaussianising, no column from after the prediction point, and clean split hygiene (20
distinct partitions, 60 distinct test-family sets, every family tested exactly 20 times, no family on both sides).

**The opposite flaw, now fixed in the notes.** The honest baseline was under-specified by +0.0795: the feature list
drops the group column while the metric scores only within the family, so a model that does not know the grouping
spends its fit on variance the metric discards. Excluding the column hides nothing, since clustering on the missing
mask alone recovers the 39 families at adjusted Rand 1.0000 and centring within those clusters scores the same.

</details>

<details><summary>Precedent checker</summary>

Register: 5,865 decisions over 2,108 records. Four calls consistent, three departures that need a written line.

| Decision | Precedent | Verdict |
|---|---|---|
| family grouping over the source's random hold-out | `asp_potassco_classification`, `airfoil_self_noise`, `huesken_sirna_efficacy`, the scaffold family | consistent, and reinforced: a random split here would leak the family through the mask |
| the quality-assured release and the origin over the benchmark's cut | `nci_aids_antiviral_screen`, `qsar_biodeg`, `qsar_tid_11` | consistent |
| keeping the 70 lines whose two genotype releases disagree | the cleaning rule on impossible values; `clock_protein_toxicity` required a demonstrable per-row failure | consistent |
| the declared context | the two precedents for it; `protein_model_quality_rf_pcp` records its gain | departs only in that the number was unrecorded; now written down |
| keeping the blank marker calls | the cleaning rules | consistent in outcome, the stated reason false (issue 5) |
| the within-family metric | `protein_model_quality_rf_pcp`, `huesken_sirna_efficacy`; `superconductivity`, `loan_default_prediction_imperial_college` | departs: the exception is unwritten and this is the third of one reason (issue 6) |
| the target fitted by us | `superconductivity`, `boreal_postfire_lichen_biomass` both kept a published number | departs, with a fact that sets the case apart (issue 1) |
| the all-plot environment fit kept with a note | `sf_permit_time`, `home_credit_default_risk` were rebuilt | departs, with no fact behind it (issue 2) |
| reading one of three release objects | `boreal_postfire_lichen_biomass` chose between two published measurements and wrote the reason | departs: the reason is sound and unwritten (issue 4) |
| accepting the few-groups warning | `huesken_sirna_efficacy`, `airfoil_self_noise`, `open_university`, `heart_disease`, against `covertype` | consistent on the evidence, the written acceptance missing (issue 3) |
| a public copy of the target | no precedent in the register | new (issue 7, and a cross-dataset item) |

It also notes that the sweep over every v2 definition for a model-fitted target found only a probe, a metric
definition and sources that publish a residualised target themselves: this is the collection's first dataset whose
target is a quantity we estimate.

</details>

<details><summary>Advocate</summary>

Argued to ship. The use case is named by the source and the actor is real; the split follows the application and the
leaf is the one the tree gives; the metric is the field's own quantity at the unit the breeder acts on; the release
choice is forced by the field block; and no attack found a leak inside the shipped frame. On the target it argued
that the shipped value is the package's own `BLUP(dereg=TRUE)`, measuring a within-family correlation of 0.99998
against that estimator, so no exception beyond the rule would be needed. On the germplasm it argued that the breadth
makes the declared metric harder rather than easier, and measured it: dropping the seven exotic families lifts the
score from 0.236 to 0.276 while dropping seven elite families instead lowers it to 0.219 over 20 draws.

In its rebuttal it conceded six of the critic's seven remedies (the attribution, the check-only environment fix, the
rewrite of the fit statement, the exception and amendment for the metric with the parent-yield sentence, the rewrite
of the single-marker sentence, and the corrections), and its own measurement of the four-check index agreed with the
critic's inside noise (-0.0066 against -0.0053). The mediator kept its germplasm direction and overruled its reading
of the target.

</details>

<details><summary>Critic</summary>

Argued to ship after changes, not to exclude: it found no Must that cannot be fixed, and does not dispute the use
case, the split, the metric or the release. Seven points, most fundamental first: the target is ours and was
attributed to a paper that does not contain it; the all-plot environment fit is a transductive tie with a free fix
the precedent takes; the fit statement names two gaps that both fall and misses the germplasm; the few-groups warning
fires and is not accepted, which is the one point it called blocking; the metric overrules a source metric and is the
third exception of one reason with no exception line; the single-marker sentence explains the probe by biology that
is not there; and three stated facts about the target's construction are wrong, one of them a published quantity.

Its own builds of the line value decided two of those points:

| build of the line value | within-family r (ridge) | fold SD | agreement with the shipped target |
|---|---|---|---|
| shipped: environment over all line plots, index from all 45 strains | 0.2340 | 0.0121 | |
| check-only environment effects | 0.2328 | 0.0128 | r 0.9939, difference SD 28.9 kg/ha |
| index from the 4 near-ubiquitous checks only | 0.2287 | 0.0112 | r 0.9908, difference SD 38.0 kg/ha |

It read `BLUP.R` and showed that the package adds the grand mean before dividing by the reliability, which is what
settled the target dispute against the advocate.

</details>

<details><summary>Mediator</summary>

Settled six disputes by measurement and ruled the verdict **ship after changes**, with the full tier in.

1. Is the shipped target the source's estimator or ours? The critic is right: the package's literal switch carries
   the line's plot count into the value, agreeing with ours at within-family r 0.90, while our build reproduces the
   de-regression done in the usual order at 0.99998. The model form is the source's, the implementation is ours and
   is a repair (issue 1).
2. The direction of the germplasm gap: the advocate is right on the declared metric. Against the right control the
   narrower panel is worth +0.057, and the exotic drop beats all 20 control draws; the practitioner and the critic
   are right about a pooled score, where the between-family share is 54.3% against 32.6% among the elite families.
   The two sides measured different metrics.
3. The few-groups warning: both are right, and the ask is a decision item rather than a blocker, since the empty
   attribute is the state the workflow prescribes (issue 3).
4. A selection marker: no marker. The rule's own carve-out excludes rows that come from another population
   altogether, and a designed panel whose progenies were deliberately not selected is that case; the fit grade and
   its reason carry it.
5. The blind reviewer's exclusion: overruled, its fact kept and sharpened. The blanks are deleted blocks rather than
   sparse no-calls (24.56% of blocks entirely blank, none between 0.1% and 10% scored, 100% of scored blocks
   polymorphic), the vote rests on a pooled score the task does not use, the proposed fill cannot move the declared
   metric by construction, and the fill it proposes is not the package's option. What survives is that the notes'
   stated reason for keeping the blanks is false (issue 5).
6. The blind reviewer's other nine concerns: each ruled, none changing a decision.

**Agreed facts.** The task and the use case are real and the measured selection gain agrees with the metric to 5%.
The split is right and cheap. Honest evaluation holds inside the shipped data. The largest leak the definition
prevents is the six dropped plot traits. The signal is real on the declared metric. The metric is right and the
source's is overruled with a measured reason. The blank cells are deleted non-segregating blocks. The
quality-assured release is the right one and the planting-date departure is immaterial. `set` is a per-line maturity
group, correctly dropped. The plot count is correctly not a feature, not a scoring column and not a weight.

**For the curator:** issues 1 to 7 above. It also sent one note to the panel tooling rather than to any record: the
participant kit hands the agent the full target column for all 60 splits, so any cross-split memorisation measured
in a panel is an artefact of the kit.

</details>

<details><summary>Review editor</summary>

Applied the mediator's fifteen editor-level changes and the three issues it marked as needing no decision, then
re-ran the checks. The definition now attributes the target fit to the package's own estimator and names the two real
departures from the data paper (two stages with block BLUPs from 10 check varieties; the entry random and no
environment term), with the planting-date departure recorded as immaterial. The fit statement is rewritten on the
germplasm with its measured direction, keeping the approximate grade, and the measurement moved to the notes when the
summary-length check fired on it. The single-marker sentence, the check-cultivar count, the heritability and three
arithmetic slips are corrected. The splits comment gains the departure on the declared metric and what the source's
split was designed for; the grouping definition and the splits comment gain the context gain of +0.0795 and the fact
that the grouping is recoverable from the missing mask; the metric reason gains the parent-yield fact and the
pooled-against-within-family numbers; the time-basis text accepts the half-sib limit; and new notes carry the dropped
traits' worth, `set` as considered and rejected with the load-bearing shuffle, the block structure of the
missingness, the maturity paragraph and the licence clause. No selection marker was set.

Nothing it applied moves the data: the frame, its dtypes, the sample rows, the data checks and both decision tables
are byte-identical before and after, and the bundle checks end where they began at 0 errors, 1 warning and 1 info
over 28 checks. The definition checksum changes, because it hashes the definition's metadata along with the frame.

</details>
