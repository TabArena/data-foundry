# gse40279_methylation_age

**Outcome:** added. Hannum et al.'s blood methylation cohort (GEO GSE40279, 2012): a person's age in years from
the 450K array of their whole blood, 656 people x 473,036 features (473,034 probes, sex and recorded ethnicity),
grouped by the nine processing plates, 3 folds, fallback rmse. The AI recommends shipping it after the panel's
changes, which are made; the build waits on a library change.
Verdict: ship after changes (made); one open call on `ethnicity` (issue 1).
Validity: the use case leads with the aging study that reads a clock's predicted age against the real age (fit
direct); forensic age estimation is named second and approximate (forensic labs use panels of a few sites and do not
know a recorded ethnicity). The 430,448 cells (0.139%) the authors filled by KNN over all samples ship as missing,
rebuilt from BeadStudio's per-sample betas in the same series (as coad). No leak found: the copy and
nearest-neighbour exploits lose to an honest model (task gamer: nearest training row 9.68 RMSE worse; highest sample
correlation 0.9946, one pair at r = 0.957 against a median of 0.80, a possible replicate, one row, negligible). Plate
is the batch (nearest neighbour on the own plate 68.6%, chance 12.1%) and the group; chip nests in plate and is nearly
IID, site has four groups that cut across plates.
Value: elastic net 5.39 RMSE on the plate folds against 4.82 on random people and a dummy of 15.3; the best single
probe (ELOVL2, the field's core signal) 7.73; task probes (3 splits) best skill +0.798, LightGBM, no flag. rmse is the
fallback; the reason now cites the paper's Fig. 7A, which calls the authors' error RMSE.
Quality: sex decoded; every probe kept; the dataset labelled ultra-wide (656 x 473,038: the 473,036 features plus the
target and the plate) in the notes; splits comment: the 20 repeats give 18 distinct partitions of the 9 plates
(chance, 280 possible).
Weighed: an established clock cohort with the widest age range (19 to 101) +; few groups (9 plates) −; ethnicity
constant per plate − (issue 1); a larger sibling, gse55763, without the old ages (issue 3) ±.
Probes on the final definition: `dataset check` 0 errors, 2 warnings (issue 4), 1 info (duplicate checks over budget,
measured by hand). Not run: the leak, copy, nearest-neighbour and group probes stopped at their time limit (exit 124)
before finishing. That leaves unchecked a full-width search for near-copies across all 473,036 features, the
hidden-group probe, and the task probes at 30 splits (they ran at 3). The scratch checks cover part of this: highest
sample correlation 0.9946, and the nearest-training-row exploit loses 9.68 RMSE. Only light checks were re-run after
the panel's changes, which touch text only.
For the curator: issue 1 (ethnicity), issue 2 (MAE or RMSE, a rule question), issue 3 (this cohort, gse55763 or
both), issue 4 (the two split warnings).
`source` for GEO datasets (main session, no decision here): GEO is run by NCBI, a US government site. This definition
and its record say `Other`; the shipped `lung_cancer_epithelial_genexp` says `GOV Website`. One value will be set for
all GEO datasets.
Build blocker for the main session: pyarrow refuses to read back a parquet file this wide with its default footer
limits; the library needs `PARQUET_READ_LIMITS` in build and verify, the harness and the examples before
`dataset build`.

**Main points:** Keep `ethnicity` as an input (issue 1)? Confirm rmse (issue 2), add both blood cohorts (issue 3),
and accept the two split warnings (issue 4, yes/no)?

**Record judgment:** valid. A peer-reviewed cohort (Molecular Cell 2013) deposited in GEO by its authors, with the
paper's own covariates and the per-sample signals that let the imputed cells be undone.

**Issues for Lennart:**

1. **Should `ethnicity` stay an input?**

   * **Problem:**
     - Recorded ethnicity is constant per plate: plates 5, 6 and 9 hold all 230 Hispanic samples, the six others none.
     - Under the plate split it therefore also marks the cohort, as the recruitment site does; the definition drops `site` because it is a property of the cohort, which differs in age by design.
     - Whether a protected ground is a reason to drop a column is decided for all datasets by the **across-datasets item on protected grounds** on the review page; this issue decides only the cohort-label question for this dataset[^across].
   * **Effect on the task:** in repeat 12 fold 2 every test sample is Hispanic and no training sample is (an unseen level); in 16 of 60 folds one side has no Hispanic sample; Hispanic mean age is 54.6 against 69.1, a sampling artefact. No probe flagged the column, and the split auditor rates keeping it harmless.
   * **Consistency:** every person-level dataset keeps race or ethnicity (wids_diabetes_mellitus, diabetes_130_us, kumc_inpatient_aki_prediction, 2_month_survival_rate_prediction); the only drop on record is sex in insurance pricing[^use6].
   * **Panel:** the advocate keeps it with notes (the paper's covariate, known to the aging study); the critic drops it (a cohort label, the reason the site was dropped); the mediator leans keep, given that the aging study leads the use case[^use3].
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep with notes (implemented) | `ethnicity` stays; the notes say it is constant per plate and name repeat 12 fold 2 | the paper's own covariate; known to the aging study; follows every medical precedent | acts as a cohort label under the plate split; one fold tests an unseen level |
     | B | Drop as a cohort label | `ethnicity` leaves the features, as the site did | same reason as the site; nothing the forensic actor would not know | first drop of a recorded ethnicity outside insurance pricing; loses the paper's covariate |

   * **Recommendation:** A, since the aging study leads the use case; B only if you put the forensic lab in the lead. **Decision:** A or B?

   **Notes for the AI:** on B, add `"ethnicity"` to the `drop(columns=...)` in `_clean` step 4, remove it from `FeatureTypes`, `known` and the curation notes' features bullet (move it to Dropped, with the plate-constancy as the reason), re-run `dataset check`.

   [^across]: The across-datasets item on protected grounds (the SEL-7 amendment proposed on acs_food_stamps_2014_2024) decides for all datasets alike whether a protected ground is a concern by itself.
   [^use6]: **USE-6** (Must): anything known at the prediction point is a legitimate input.
   [^use3]: **USE-3** (Must): name the prediction point, when the model is used and what is known then.

2. **Score with MAE instead of RMSE?**

   * **Problem:**
     - The domain practitioner prefers MAE, the habit of forensic age estimation.
     - The paper reports an unnamed "error of 3.9 years", and its Fig. 7A calls the authors' error "standard error (RMSE = 7.22 years)", so RMSE is the likely meaning of the paper's "error", though the origin stays `fallback` because the paper never defines it.
     - A field habit ranks below the source's own choice, so MAE would be a new context exception and would have to change gse55763_methylation_age too[^met5].
   * **Effect on the task:** RMSE weighs the large errors on the oldest people more; the ranking of models may differ little. Not measured.
   * **Consistency:** the gse55763_methylation_age record declares the same rmse fallback; the only mae precedents are source metrics (zillow_prize, forest_fires).
   * **Panel:** the domain practitioner prefers mae; the advocate, critic and precedent checker keep rmse and call mae a rule question for both siblings.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | rmse (implemented) | fallback rmse in years, reason citing Fig. 7A | the source's likely error; consistent with the sibling | not the forensic field's habit |
     | B | mae, for both siblings | a context exception, written into the metric rules | the forensic habit | no precedent; a rule change for one field's habit |

   * **Recommendation:** A; decide it alike with gse55763_methylation_age, whose record takes the same fallback. **Decision:** A or B, for both datasets?

   **Notes for the AI:** on B, a rule amendment first (MET-11 cases), then `Metric` in both methylation-age definitions.

   [^met5]: **MET-5** (Should): a paper's metric is the source's metric only when it is one deliberate choice.

3. **Keep this cohort, gse55763, or both?**

   * **Problem:**
     - GEO GSE55763 (Lehne et al. 2015) holds 2,664 people of the same task, ages 23.7 to 75.0.
     - This cohort is smaller (656) but spans ages 19 to 101 and is the cohort behind a standard clock.
     - The two are different people and different studies, so neither is a duplicate of the other[^prov7].
   * **Effect on the task:** none found in this folder; the panel sees no defect in either.
   * **Panel:** the domain practitioner would want both (this one has the people over 75); nobody argued for one only.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Both (implemented) | two folders, two cohorts | the old ages here, the size there | two tasks of one kind in the benchmark |
     | B | Only gse55763 | this record goes to `No` | four times the people | loses everyone over 75 |
     | C | Only this one | gse55763 is not added | the widest age range | the smaller cohort |

   * **Recommendation:** A. **Decision:** A, B or C?

   [^prov7]: **PROV-7** (Must): records that share a source but give different tasks are not duplicates.

4. **Accept the two split warnings with these texts?**

   * **Problem:**
     - Only 9 plates, 3 per test fold, so the check warns about few groups twice.
   * **Effect on the task:** test-minus-train mean age runs from -15.6 to +17.0 years; 126 test rows lie outside their training age range.
   * **Panel:** the split auditor, advocate and critic agree to accept both.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Accept with these texts | both warnings accepted with the texts in the notes below (written into `dataset.py` on yes) | names the age shift a reader of the scores needs | longer texts |
     | B | Accept with the builder's shorter text | both accepted without the age shift | shorter | the age shift goes unsaid |
     | C | Reject (implemented) | the warnings stay open | none found | the plate split is the right one; nothing to fix |

   * **Recommendation:** A. **Decision:** accept both warnings with these texts, yes or no?

   **Notes for the AI:** on yes, write into `accepted_check_warnings` in `dataset.py`:
   `task_group_count_low`: "9 processing plates: a new lab sample comes in a batch of its own; held-out plates raise an elastic-net clock's RMSE from 4.8 (random people) to 5.4 years, and every plate fold is learnable (dummy 15.3). The plates differ in age, so folds also shift the age range: test minus training mean age runs from -15.6 to +17.0 years, 16 of 60 folds shift by more than 10 years, and 126 test rows lie outside their training age range."
   `groups_test_groups_few`: "3 plates per test fold of 146-267 people; scored per person; the plates carry a strong batch (nearest neighbour on the own plate 68.6%, chance 12.1%) and the signal holds across them."
   Then re-run `dataset check`.

**Review panel:** ship after changes (mediator). Tier full: claim auditor, column auditor, split auditor, domain practitioner, blind reviewer, task gamer, precedent checker, advocate, critic, mediator; the rebuttal round was skipped because the opening briefs converged on every fact. Claim audit: no validity claim refuted; the repeats give 18 distinct partitions (noted). Blind review: would benchmark; main concern the width. Task gamer: no exploit beats an honest elastic net (5.89 RMSE over all 60 splits on 3,000 age-screened probes; the builder's 5.39 is on the plate folds). Debate: agreed on the plate split, the rebuild of the imputed cells and rmse; disputed: keep `ethnicity` (issue 1).

<details><summary>Mediator: gse40279_methylation_age</summary>

Mediator report: gse40279_methylation_age (2026-11-09). No rebuttals were filed and no new experiment was run: the opening briefs agree on every fact.

**Recommendation (judgment record)**
- **Verdict:** ship after changes. One open call goes to the curator (ethnicity). The build is blocked until the library change below lands.
- **Why:** the task is real and learnable. Elastic net scores 5.39 RMSE on plate folds against a dummy of 15.3. The best single probe (ELOVL2) scores 7.73. The gamer's honest elastic net scores 5.89 over all 60 splits, and every exploit he tried scores worse than it.
- **Rules:** USE-1/3/6/8, LEAK-10/16-21/30, PROV-13, SPLIT-3/23/24/29, MET-5/11, TP-1..5, EV-4/8.
- **Precedent:** it follows coad (rebuild the imputed cells to missing), gallstone and early_stage_diabetes (rmse fallback), and the medical datasets that keep ethnicity (USE-6).

**Changes to make now (no decision needed)**
1. **Imputed cells:** ship the 430,448 KNN-imputed cells (0.139%) as missing, as already implemented (PROV-13 Must over LEAK-30; coad precedent).
2. **Plate split:** accept the two warnings with the builder's text, and add the age shift to it. Test-minus-train mean age runs from -15.6 to +17.0 years, 16 of 60 folds shift by more than 10 years, and 126 test rows fall outside the training age range (SPLIT-24 Weigh; mildest remedy, a note).
3. **Probes that timed out:** add a REVIEW.md/notes line. The copy and nearest-neighbour leak probes and the group probes stopped at exit 124 and never ran. The scratch checks stand in for them: no duplicate sample, highest sample correlation 0.9946, and the nearest-training-row age exploit loses 9.68 RMSE. Name the one pair at r=0.957 (median 0.80) as a possible replicate, one row, negligible (LEAK-16..21, EV-8).
4. **Repeats:** add to splits_comment that the 20 repeats give 18 distinct partitions (reps 9=11, 8=13). With 9 plates and 280 possible partitions this is chance. Keep the protocol default (EV-8).
5. **Metric reason:** keep rmse and cite Hannum Fig. 7A ("standard error (RMSE = 7.22 years)") in the reason. If the paper defines its "error" there as RMSE, the origin can become `source` (MET-5). Keep gse55763 alike (MET-8).
6. **Use case:** lead with the aging-clock study actor (fit direct). Put forensic estimation second, marked approximate: forensic labs use few-CpG panels and do not know recorded ethnicity (USE-1/USE-8).
7. **Width:** label the dataset ultra-wide in the README (656 x 473,038). The blocker is fixed in the library (PARQUET_READ_LIMITS in build/verify, harness and examples), not by cutting to a probe subset (EV-4; CLEAN-22 keeps all probes). This is for the main session, before the build.

**Issues for the curator (ranked)**
1. **Should `ethnicity` stay an input?** (validity; USE-6 Must, USE-3)
   - **Problem:** ethnicity is constant per plate. Plates 5, 6 and 9 hold all 230 Hispanic samples; every other plate is all Caucasian. So under the plate split it acts as a cohort label.
   - **Effect:** in rep 12 fold 2 the training side has no Hispanic rows and the test side is all Hispanic, an unseen level. In 16 of 60 folds one side has no Hispanic rows. Hispanic mean age is 54.6 against 69.1, a sampling artefact. The effect on scores is low: no probe flagged the column, and the split auditor rates keeping it "harmless".
   - **Critic (drop, option B):** the definition drops `site` as a cohort property that differs in age by design, and ethnicity carries the same cohort (USC 138/139 Hispanic). The reason is the cohort-label fact, not the protected ground.
   - **Advocate (keep with notes, option A):** USE-6 precedent. Every person-level dataset keeps race or ethnicity (wids_diabetes_mellitus, diabetes_130_us, kumc_inpatient_aki_prediction, 2_month_survival_rate_prediction). The only drop on record is sex in insurance pricing. The study actor knows ethnicity.
   - **Rules:** this is a conflict between two applications of the same rule, USE-6 (no rank difference), and a weighing of factors, so it is not mine to settle. A group-level covariate fires no LEAK rule.
   - **What would settle it:** (a) which actor leads the use case. If the study actor leads, as change 6 proposes, precedent favours keep. (b) Whether the site-drop reason, a cohort property, applies to a protected attribute.
   - **If kept:** note the plate-constancy and rep 12 fold 2 in curation_comments.
   - **Across datasets:** the protected-grounds question stays open on the review page for all datasets alike.
   - **Panel lean:** keep (A) with notes, given change 6. Drop (B) only if the curator puts the forensic actor in the lead.
2. **Metric: MAE instead of RMSE?** Not disputed in the briefs; listed for completeness. The domain practitioner prefers MAE (forensic field habit). The fallback stands: MET-5 ranks a field habit below the source's own choice, and Fig. 7A points to RMSE. Taking MAE would be a fourth MET-1/MET-11 context exception and would have to change both siblings at once, so it is a rule question, not one for this dataset.
3. **Better data (builder issue 3; weigh):** keep this one (ages 19-101), gse55763 (2,664 people), or both. The panel sees no defect; adding both is implemented.
4. **`source` field (procedure, main session):** "Other" vs "GOV Website" for GEO. The shipped `lung_cancer_epithelial_genexp` uses "GOV Website"; the batch siblings use "Other". A cross-dataset consistency fix.

**Task gamer's exploits mapped to rules**
No exploit beats the honest baseline. All are known regimes, so none is a new issue, and none contradicts a `Potential leak, kept on purpose:` note.

| Exploit | Rule | Gain (RMSE) |
|---|---|---|
| Shrink toward the test plate's mean (true plate) | SPLIT-29 group context | -0.99 |
| The same shrink with plates found by KMeans | SPLIT-29 group context | -1.62 |
| Per-plate centering with test-row statistics | LEAK-30 transductive | -3.30 |
| Age of the nearest training row | LEAK-16..21 copies | -9.68 |

- Linear stretch of predictions fitted on training rows: +0.16, which is honest calibration, not a leak.
- Row order, formats and identifiers are clean.
- The kept-on-purpose note on the 830-probe missingness filter is untested by the gamer. It is label-free, so it stays as written.

**Agreed facts**
- 656 people x 473,036 probes, plus sex and ethnicity. Target is age in years, 19-101, no missing.
- Plate batch is strong: nearest neighbour on the own plate 68.6%, chance 12.1%.
- Elastic net 5.39 on plate folds vs 4.82 random. Ridge 9.07 plate, 6.81 random, 7.10 chip, 8.92 site.
- Plate is the right group. Chip nests within plate and is nearly IID. Site has only 4 groups and does not nest with plate.
- ELOVL2 r=0.86 is the domain's core signal, not a leak.
- No leak and no cleaning defect. The repair to missing is measured cell by cell.
- The build fails on pyarrow's thrift footer limit.

**Consistency with precedent**
- Every call in the definition matches precedent: coad, the rmse fallback, the USE-6 medical precedents, and SPLIT-29 accepted warnings.
- Two panel leanings would depart from precedent:
  - Dropping ethnicity would be the first protected-ground drop outside insurance pricing. The facts that set this case apart are the cohort-label fact (as with site) and, if the forensic actor leads, that the actor does not know it. This goes to the curator as issue 1.
  - MAE has no precedent as a field-convention context case. This is a rule amendment for both siblings (issue 2).
- The `source` field differs across GEO datasets (issue 4).

</details>

<details><summary>Claim audit: gse40279_methylation_age</summary>

Claim auditor: gse40279_methylation_age (2026-11-09)
Verdict: ship with two small fixes. No validity claim was refuted. One implied claim fails: that ethnicity is a usable input on every fold. Two repeats are copies of each other.
Splits rebuilt with the definition's make_splits on the 656-row metadata (seed 4267). Fold sizes match the README's 60 rows (rep 0: 150/243/263), so this is the shipped split. No container was built.

TABLE (claim | source | test | result | evidence | rule)
2  9 plates, 656 rows, 17-92 per plate | task_summary.row | counted samples_with_chip.csv | holds | plates 1,2,3,5,6,8,9,10,11 = 90,84,69,90,92,81,48,17,85 | SPLIT-23
5/19 plate held out, 3 plates per test fold, 146-267 rows | splits_comment | rebuilt splits | holds | 60 folds, each with exactly 3 plates, 146-267 rows | SPLIT-3
7  plate means 38.5-76.2 | fit_reason | groupby | holds | 38.5 (plate 10) to 76.2 (plate 11) | -
21 Hispanic only on plates 5,6,9 | splits_comment | groupby | holds | 90/92/48 = 230 | -
22 each of the 67 chips on one plate | Grouping.definition | chip->plate nunique | holds | 0 of 67 chips span plates | SPLIT-24
23 N1=482 is UCSD+Utah, N2=174 is USC+Boston | claims 23 | crosstab | holds, with a caveat | plate 2 = Boston 18/USC 1/Utah 65; plate 5 = USC 46/Utah 44 | -
6/14/15 430,448 imputed cells (405,768 blank, 24,680 changed); 185-8,315 per sample; at most 34 per probe; 175,470 probes | curation notes | recounted imputed_cells.parquet | holds | exact numbers | LEAK-30, PROV-13
-  missingness carries no signal (implied by shipping NaN) | builder's leak probe 3 | per-sample NaN count vs age; vs plate | holds (weak) | Spearman 0.118 with age; plate medians 303-895, so NaN counts mark the batch somewhat, but the plate is held out | LEAK-30
25 metric is a fallback to RMSE | Metric.fallback reason | read PMC3780611 again | holds; the reason could be stronger | Results: "an error of 3.9 years" is unnamed and the Methods do not define it. Fig. 7A calls the same authors' error "standard error (RMSE = 7.22 years)", so RMSE is the likely reading of "error". Either way the outcome is RMSE in years, on the source's scale | MET-1, MET-3, MET-5
-  ethnicity is a valid input on every test fold (implied by Known) | task_summary.known | Hispanic count in train vs test per fold | REFUTED on 1 of 60 folds | rep 12 fold 2 tests on plates {5,6,9} = all 230 Hispanic; its train side has 0 Hispanic, so "Hispanic - Mexican" is an unseen category there. 13 other folds train on only 48 Hispanic | USE-6, SPLIT
-  the 20 repeats are distinct draws | implied by "20 repeats" | compared partitions | REFUTED (minor) | 18 distinct partitions: rep 9 = rep 11 ({1,3,8},{2,5,6},{9,10,11}) and rep 8 = rep 13 ({3,9,11},{5,8,10},{1,2,6}) | EV-8 (weight)
-  a test fold shifts age, as stated ("each fold also shifts the cohort") | fit_reason | test mean minus train mean, dummy RMSE | holds, stronger than stated | the shift runs from -15.6 to +17.0 years; the train-mean dummy's RMSE runs 12.8-20.4 across folds, so RMSE across folds partly measures the shift in cohort age | USE-10
16/17/18/10/12/13 | paper and GEO quotes | not re-tested (measured by builder, signal-file scans too costly) | untested | cell-level formula checks rest on the builder's scripts | -
-  leak probes 5/6 (copies, nearest neighbours) and group probes | builder | logs | UNTESTED by the harness: leak_probes.log and group_probes.log both ended at exit status 124 (timeout). Only the builder's scratch duplicate check (max sample correlation 0.9946) stands in. The task probe did finish: lightgbm skill +0.798, no flags | LEAK-16..21

RANKED REFUTED / UNTESTED
1. (Validity, USE-6 Must, low stakes) Ethnicity: on rep 12 fold 2 the test category is absent from training, and on every fold ethnicity is a plate/cohort label. This backs the builder's issue 4. Mildest remedy: option B (drop ethnicity), which also fits the forensic framing. Otherwise accept and note the one fold in the README.
2. (Procedure) The harness's leak and group probes timed out (124). The copy and NN probes were not run by the harness. Remedy: state in REVIEW.md that the scratch duplicate check stands in for them, or re-run on a probe subset (for example 20k screened probes).
3. (Minor) Duplicate repeats (9=11, 8=13): with 9 plates the repeats collide by chance and the duplicated partition counts twice. Remedy: a note in the splits comment, or fewer repeats. It does not affect validity.
4. (Metric wording) The fallback reason could cite Fig. 7A ("RMSE") as further evidence. The outcome does not change.
Nothing in the imputation rebuild, plate statistics, chip nesting or the metric fallback was refuted.

</details>

<details><summary>Column audit: gse40279_methylation_age</summary>

Column auditor: gse40279_methylation_age (2026-11-09)
Verdict: ship; no leak, no cleaning defect. One question for the curator (ethnicity), sharper than builder issue 4.

Prediction point: a blood sample of unknown age, run on the 450K array in a new batch (plate).
Frame checked from the participant kit (656 x 473,038; read with raised thrift limits).

COLUMN TABLE
column | meaning | known at prediction? | dtype and cleaning | verdict | rule
age | GEO `age (y)`, chronological age at draw, 19-101 | target | int64, 0 missing, as deposited | fine | USE-5
plate | GEO `plate`, 450K processing batch (9 plates) | group, not a feature | int64; dropped from features by grouping | fine | SPLIT-3, LEAK-10
sex | GEO `gender` F/M | yes (also derivable from DNA, though X/Y probes are absent) | categorical female/male, decoded, 0 missing; age gap F 64.6 vs M 63.5 | fine | CLEAN-12
ethnicity | GEO `ethnicity`: Caucasian - European 426, Hispanic - Mexican 230 | yes for the aging-rate study; not for an unknown forensic donor | categorical, 0 missing | question (see 1) | USE-6, LEAK-10
cg* (470,043) | 450K average beta, CpG probes, 0-1 | yes, measured on the drawn blood | float64; 0.139% authors' KNN-imputed cells set to NaN from BeadStudio's per-sample betas; exact zeros = BeadStudio floor (SignalB<=0), not proxy codes; probe IDs are column names, not features | fine | LEAK-30, PROV-13, CLEAN-10
ch.* (2,991) | non-CpG (CpH) probes, same measurement | yes | as cg* | fine | same
(dropped) site | recruitment site, cohort with by-design age differences | — | dropped | fine | LEAK-10
(dropped) tissue | whole blood, constant | — | dropped | fine | CLEAN-22

Dtype probe: 0 of 473,036 flagged; agreed (no counts or codes; betas are measured fractions; no ordinal).
Missingness of the rebuilt cells carries no age signal (leak probe: missing indicators R^2 <= 0).

PROBLEMS, ranked
1. (P3/P4, question) `ethnicity` is a near-copy of the dropped `site` and constant within plate.
   Evidence: crosstab site x ethnicity: USC 138/139 Hispanic, Boston 0/35, UCSD 48/304, Utah 44/178; plates 5, 6, 9
   are 100% Hispanic, all others 100% Caucasian. Hispanic mean age 54.6 vs Caucasian 69.1 (14.5 y), a sampling
   artefact of the cohorts, not biology. The definition drops site as "a property of the cohort, which differs in age
   by design" but keeps the variable that carries most of the same cohort information; under the plate split it is a
   per-plate cohort label. Shipped splits (20 x 3): in 1 of 60 folds all three Hispanic plates are in test, so the
   category is unseen in training for 230 test rows; in 15 folds no Hispanic plate is tested.
   Mildest remedy: keep (paper's covariate, known in the aging-rate use) but state in curation_comments that it is
   plate-constant and a cohort proxy (age gap 14.5 y); stronger option: drop it, consistent with dropping site and
   with the forensic framing (builder issue 4 option B). I lean to B for consistency; curator's call.
2. (P4, fine, noted) Imputed-cell rebuild (builder issue 1 option A) is correct per column: removes the transductive
   KNN at the origin. No objection.
3. (P7, fine) No cleaning defect found: sex decoded, betas float as deposited, zeros kept with a measured reason.

</details>

<details><summary>Split audit: gse40279_methylation_age</summary>

Split auditor: gse40279_methylation_age (2026-11-09)

VERDICT: right with notes. Grouped by processing plate (9 plates, 3 test plates per fold, 20 repeats x 3 folds) fits the use case.

Method: I rebuilt the shipped splits from the series matrix header only, using data_foundry.v2.splits.grouped_splits with
group_on=plate, per_sample, random_state 4267, 20 repeats (the default protocol, no row budget). The folds match the report
(test 146-267, train 389-510). I fitted no new model: the builder's measurements already compare plate, random, chip and
site splits (enet 5.39 vs 4.82 random; ridge 9.07 plate / 6.81 random / 7.10 chip / 8.92 site), and I found nothing that
reopens the choice.

Regime: the use case is a clock applied to new people whose samples come in a new batch, so new entities in a new batch.
One person is one row, so a person cannot fall on both sides. The batch is strong (nearest neighbour on the same plate
68.6%, chance 12.1%), so an IID split would reward learning the batch (SPLIT-3/23/29). Chip (67 groups) nests within plate
and is nearly IID (7.10). Site is a cohort, but sites do not nest within plates (plate 2 = Utah 65/Boston 18/USC 1;
plate 5 = USC 46/Utah 44) and 4 groups is too few. Plate is a true id from the deposit (GEO characteristic), not a cluster.
Not temporal: no date is deposited, and age is not a time axis. No gap applies.

Per-plate ages (n, mean, sd, range): 1: 90, 73.9, 11.2, 47-101 | 2: 84, 59.5 | 3: 69, 74.0, 7.4 | 5: 90, 53.7 | 6: 92, 55.7 |
8: 81, 68.6 | 9: 48, 54.0, 16.9 | 10: 17, 38.5, 19-62 | 11: 85, 76.2.

Findings (ranked; none is a Must violation):

1. P4, weigh (SPLIT-24 "only a few groups" / cohort shift). Over the 60 folds, the mean age of the test side differs from
   the train side by 6.7 years on average and by up to 17.0 (rep 4 fold 1 and rep 17 fold 0: plates 1, 3, 11, test mean
   74.7 vs train 57.7). 16 of 60 folds shift by more than 10 years. Across all folds, 126 test rows fall outside the
   train age range (at most 7 per fold, often 101 or 19 years old). A clock used in a new study meets the same kind of
   shift (the paper validates on a second cohort), so this is a property of the regime, not an error. It does make the
   per-fold variance high. Remedy: none needed. State it as a note in the accepted warning (the splits_comment already
   says each fold "shifts the cohort").

2. P3/P4, weigh (USE-6, with builder issue 4). Ethnicity is constant per plate (plates 5, 6, 9 = all 230 Hispanic). In
   rep 12 fold 2 the test side holds plates 5, 6 and 9, so the test is 100% Hispanic and the train has none. The
   ethnicity column then has a level that never appears in training. In 16 of 60 folds one side has no Hispanic samples.
   Under this split, ethnicity works as a cohort label and teaches nothing across folds. This supports option B of
   issue 4 (drop ethnicity) a little, and it is the mildest fix if the curator prefers the forensic framing. Keeping it
   is still harmless: the feature is unseen or constant where it would matter.

3. Procedure, minor. The 20 seeded repeats give only 18 distinct partitions (2 repeats duplicate an earlier one:
   reps 9 = 11 and 8 = 13; reps 4 and 17 share one test fold). With 9 groups in 3 folds of 3 there are 280 possible partitions, so this is
   chance. The repeats still add little independent information. No remedy needed: leave the protocol default as is.

Accepting the two warnings (task_group_count_low, groups_test_groups_few) with the builder's wording is right. Each test
fold holds 146-267 people and the elastic net beats the dummy (15.3) on every plate fold (4.76-6.13).

Hidden groups: the hidden-group probe is not needed (grouped). Highest sample correlation is 0.9946 with one sample per
person, so I found no copies across the split.

Work: the splits were recomputed inline.

</details>

<details><summary>Domain practitioner: gse40279_methylation_age</summary>

Domain practitioner report: gse40279_methylation_age (2026-11-09)
Actor played: an epigenetic-clock analyst (aging-rate study) and, second, a forensic lab estimating a blood donor's age.

FIT: approximate-to-direct; I call it DIRECT for the aging-clock study and APPROXIMATE for the forensic framing.
Reason: building a blood clock on 450K betas and applying it to samples from an unseen processing batch is exactly
how Hannum/Horvath-type clocks are built and used (USE-1, USE-8); forensic labs instead use targeted panels of a few
CpGs (ELOVL2, FHL2, KLF14, TRIM59...) by pyrosequencing/massively parallel sequencing, rarely a full array, and do not
know the donor's recorded ethnicity.

1. Inputs at the prediction point (USE-3, USE-6)
 - Betas of the sample: yes, always. Missing values as missing (builder issue 1, option A): fine; a real pipeline
   imputes or drops failed probes per sample, so a NaN-tolerant task is realistic. Agree with A.
 - Sex: aging-rate study yes; forensic: inferable from DNA, but X/Y probes are absent, so as a given column it is
   acceptable. Keep.
 - Recorded ethnicity: study yes; forensic no. More important: ethnicity is constant per plate (plates 5, 6, 9 all
   Hispanic), so under the plate split it is a cohort label with no within-fold variation in those plates. Low stakes
   for score, but I would drop it to keep the forensic framing honest, or narrow the use case text to the study use.
   Rank 2 gap. Builder issue 4: I lean B (drop ethnicity) or keep A only if the use case text names the study actor
   first.
 - What I would always have and is missing: detection p-values / per-sample QC, and blood cell composition (estimable
   from the betas themselves, so not really missing). Nothing essential missing.

2. Target (USE-5)
 - Chronological age in whole years is what the forensic lab acts on (a number, with an interval). For the aging-rate
   study, chronological age is the training target and the quantity acted on is the residual (age acceleration),
   so age is the standard proxy every first-generation clock uses; acceptable. A number is what I want; an interval
   would be nicer but is not required.

3. Row and test data (USE-10)
 - One row = one person = one estimate: matches. Held-out plates = a new lab batch: matches how a clock meets new
   data, and the grouped split is the right call (builder issue 2: agree with A, plate; accept both warnings).
 - Caveat: plates differ in age (mean 38.5-76.2) and ethnicity, so a fold also shifts the age distribution; clocks
   regress to the training mean at the extremes, so test RMSE mixes batch robustness with extrapolation. Realistic
   (a forensic case can be any age), keep, but say so (already said in the fit text).

4. Would I use it?
 - Yes, as a benchmark of clock-building methods; elastic net on plates gets 5.39 y vs Hannum's reported 3.9-4.9 y,
   a sensible gap for unseen batches. I would trust a model whose error is stable across plates and that does not
   lean on ethnicity/plate artefacts; I would distrust one that wins via batch signal (the grouped split guards this).
 - Builder issue 3 (GSE55763, 2,664 people): a practitioner would want both; this one has the elderly and 19-101 range.
   Agree with A.

5. Metric (MET-1, MET-5, MET-10)
 - Declared: rmse, fallback (MET-5: Hannum reports correlation and an "error" side by side). Verdict: PARTLY.
 - The field's headline error is the absolute error: Horvath (2013) reports median absolute error, forensic
   validation studies (e.g. Zbiec-Piekarska 2015, VISAGE) report MAE in years. MAE is per person, on the scale of
   the decision ("off by N years") and less dominated by the oldest donors that clocks underpredict. RMSE ranks
   models similarly and is a defensible fallback; I would choose mae if a change is cheap, and note RMSE as acceptable.
   No MET-6..9 issue (regression, no threshold, unit = person matches).

Ranked gaps: (1) forensic framing vs array data and targeted panels (approximate for that actor; fine for the study
actor); (2) recorded ethnicity as an input, a per-plate cohort label; (3) metric rmse vs the field's MAE; (4) test
folds shift age range as well as batch (realistic, documented).

What an expert would change: lead the use case with the aging-clock study actor; drop ethnicity (or justify for the
study actor only); consider mae; keep plate grouping and missing-as-missing.

Sources: dataset.py and README.md, the builder report; Hannum et al. 2013 Mol Cell 49:359-367 (cited in
the definition); Horvath 2013 Genome Biol 14:R115 (median absolute error); Zbiec-Piekarska et al. 2015 Forensic Sci
Int Genet (ELOVL2/forensic MAE); general knowledge of VISAGE forensic age panels. Rules: USE-1, USE-3, USE-5, USE-6,
USE-8, USE-10, MET-1, MET-5, MET-10.

</details>

<details><summary>Blind review: gse40279_methylation_age</summary>

Task: predict chronological age from whole-blood Illumina 450K methylation (GSE40279, Hannum et al. 2013 Mol Cell). 656 rows x 473,034 beta-value probes + sex, ethnicity, plate. Real use: epigenetic clock / forensic age estimation; well-known public data.
Verdict: include with changes (real, high-signal, honest target), but only as a reduced/wide-feature task and with plate removed as a feature.

Concerns, most to least serious:
1. Width is impractical: 473,038 columns; default pyarrow cannot even open the parquet ("Couldn't deserialize thrift: Exceeded size limit"; needed raised thrift limits). Most tabular methods will OOM or time out, so the benchmark measures engineering, not modelling. Change: ship a documented probe subset (e.g. top-variance 5-20k, or chosen inside each training fold), or label clearly as an ultra-wide task.
2. Plate is strongly confounded with age: mean age per plate ranges 38.5 (plate 10, n=17) to 76.2 (plate 11, n=85). Grouped split by plate therefore also shifts the age distribution between train/test (extrapolation, not just batch shift); with 9 plates x 3 folds, fold scores will be noisy. Keep grouped split if the intent is batch robustness, but drop `plate` as a feature (if it is one) and report variance; plate 10 with 17 rows is a tiny group.
3. Ethnicity confounded with age (Caucasian mean 69.1, Hispanic 54.6) and plates; fine as a covariate but note it.
4. Signal is near-trivial for linear models: single probe cg16867657 (ELOVL2) has r=0.86 with age; published clocks reach RMSE ~4-5 y. Still useful for comparing tabular methods on p>>n, but tree models will likely lose to elastic net; that is a known, not interesting, outcome.
5. Prep: betas in [0,1], 0.13% missing (fine, left as NaN); sex/ethnicity categorical, plate int (should be categorical or excluded). No duplicate check across all columns was feasible at this width.
Could not check: full-row duplicates/replicate samples, whether probes were normalised per plate in the GEO series matrix, all 473k columns' value ranges (checked 3,000), model performance under the grouped split.

</details>

<details><summary>Task gamer: gse40279_methylation_age</summary>

GSE40279 methylation age - task gamer report
Verdict: none of the attacks I tried beat the honest baseline. Each exploit scored worse than the honest model on average.

Honest baseline (all 60 shipped splits, RMSE):
  ElasticNet(alpha .02, l1 .5) on the 3000 probes most correlated with age in the training rows (from all ~473k probes) plus sex and ethnicity: 5.89 mean (4.86-7.95)
  Untuned LightGBM on the 2000 highest-variance probes: 14.24 (10.4-20.4)
Exploits. Reference is the same ElasticNet restricted to the 20k highest-variance probes, which scores 8.47. Gain = reference minus exploit, so a negative gain means the exploit is worse.
  Linear stretch of predictions, fitted on training rows (honest calibration): +0.16 (-0.12..+0.48). This is signal, not an exploit.
  Shrink toward the test plate's mean prediction, using the true plate (group context is 'none'): -0.99 (-1.96..-0.23)
  The same shrink with plates recovered by KMeans on the test rows' PCs: -1.62
  Per-plate centering of features using test-row statistics: -3.30 (-7.2..-0.3). Plate mean ages differ (38-76), so centering removes real signal.
  Age of the nearest training row (copies across the split): -9.68. The nearest-neighbour age correlation is only 0.18. One pair of rows correlates at 0.957 against a median of 0.80 (a possible replicate). That is 1 row and negligible.
Nothing found:
  row order: Spearman of age vs. position -0.002; next-row |dAge| 16.0 vs. 16.3 shuffled.
  formats: the 6th-decimal last digit is uniform; share of values with 4 or fewer decimals vs. age r = 0.03; NaN count per row vs. age r = 0.11 (weak).
  identifiers: none. The only columns besides the probes are sex, ethnicity and plate.
  time: not applicable (no time column).
  web: no leak or magic-feature threads. The literature (Genome Biology 2014) notes that plate is a strong confounder of age. That fits the grouped split and the failed batch exploits.
Not checked: probe-level batch correction with ComBat; a full grid of exploits on the full 473k probes (I used the top-20k probes for speed); GEO sample lookup (works for any public set and is not a task flaw).

</details>

<details><summary>Precedent checker: gse40279_methylation_age</summary>

Precedent checker: gse40279_methylation_age (2026-11-09)

Verdict: the definition's calls are consistent with precedent. Two panel leanings would depart from precedent:
dropping `ethnicity` and switching to mae. Each needs a stated fact and the curator's call on the review page.
Neither is a finding against the definition.

1. Ethnicity (and sex) as inputs: the definition keeps both. CONSISTENT (USE-6, Must)
 Precedents: every shipped medical or person-level dataset in the working copy keeps recorded race/ethnicity as an
 input when it is known at the prediction point: wids_diabetes_mellitus (`ethnicity`), diabetes_130_us (race),
 kumc_inpatient_aki_prediction (`race_code`, CLEAN-12 case), 2_month_survival_rate_prediction (race, USE-6 case
 2026-10-26), infrared_thermography_temperature (Ethnicity). The only protected-ground drops on record are sex in
 insurance pricing (principles.md Tensions row, bemtpl97 2026-11-05, australian_vehicle_insurance 2026-11-08,
 Lennart). That exception is limited to insurance pricing under a legal bar, and it says that credit and other
 domains keep the factor. No precedent drops a protected ground outside insurance pricing.
 Sibling gse55763_methylation_age: GEO deposits no ethnicity, so the sibling sets no precedent either way.
 Panel lean B (drop ethnicity): it DEPARTS. Two facts could set this case apart:
  (i) Under the forensic framing the actor does not know the donor's recorded ethnicity (USE-3/USE-6: not known at the
      prediction point). This is a use-case fact. The study actor (aging rate) does know it, so the fact holds only
      if the use case is led by the forensic actor.
  (ii) Ethnicity is constant per plate (plates 5, 6, 9 = all 230 Hispanic), so under the plate split it acts as a
      cohort label. The definition already drops `site` for the same reason (a cohort's by-design property). This
      fact matches the site drop. But a group-level covariate is not a leak (no LEAK rule fires), and the column
      probes flagged nothing. A cohort label that is also a protected ground goes to the review page and is not
      dropped by the panel.
 Precedent check on the site drop: consistent. It is a cohort id with by-design age differences, not knowable for a
 new sample's cohort.
 The issue is ready for the review page (builder issue 4). Reflection prompt below.

2. Metric: rmse fallback. CONSISTENT (MET-5, MET-11 fallback)
 Hannum reports correlation and an error side by side, so there is no single deliberate choice. The fallback follows
 gallstone_disease and early_stage_diabetes_risk_prediction. The sibling gse55763 record also declares the rmse
 fallback "as for gse40279" (MET-1, MET-8), so the two must stay alike.
 Domain practitioner's mae: it DEPARTS. Precedent for mae exists only as a SOURCE metric: zillow_prize (MET-4,
 competition) and forest_fires (MET-5, ranked by MAD). This source does not rank by MAE.
 Under MET-11 `context`, a field convention (forensic MAE in Zbiec-Piekarska 2015, VISAGE) has no precedent. The
 context cases name a fact about what the decision scores: diamonds (relative error), huesken_sirna_efficacy and
 protein_model_quality_rf_pcp (ranking within a group, 2026-11-04), superconductivity (unit weight, 2026-11-08).
 "The field reports MAE" is a habit, which MET-5 treats as weaker than a deliberate choice.
 Unchecked: whether Hannum's unnamed "error" is an RMSE. If the paper defines it as RMSE, the origin may be `source`
 rather than `fallback`. Check the paper's Results/Figure 2 text.
 If the curator takes mae, the change has to be made for both siblings at once (like cases alike), and MET-10's
 diversity tie-break counts in its favour only "when the call stays in doubt".
 Register note: an amendment is due on MET-1 (3 exceptions: huesken, protein_model_quality, superconductivity), and
 a field-convention mae would be a fourth context case. That is a further reason to decide it as a rule, not
 per dataset.

3. Other calls checked
 - Missing-as-missing rebuild (issue 1): follows the coad precedent named by the builder (PROV-13 Must over
   LEAK-30). The sarcoma KNN-kept case (2026-10-19) differs because the per-sample values were not recoverable there,
   and here they are. Consistent.
 - Plate grouping with the two warnings accepted: consistent with SPLIT-29 readings and accepted-warning practice.
   No contrary pair.
 - source="Other": a cross-dataset inconsistency with lung_cancer_epithelial_genexp ("GOV Website") for GEO.
   Builder issue 5 (the main session's call). It is a real pair decided differently, though it may predate the batch.

Reflection prompt (draft, review-file issue shape):

**Should the model get the donor's recorded ethnicity as an input?**

**Problem:**
- The panel leans to dropping `ethnicity`, but every person-level dataset we ship keeps race or ethnicity as an input
  (wids_diabetes_mellitus, diabetes_130_us, kumc_inpatient_aki_prediction, 2_month_survival_rate_prediction). The
  only protected ground we drop is sex in insurance pricing.
- Here ethnicity is constant within each plate (plates 5, 6, 9 hold all 230 Hispanic samples). Under the plate split
  it acts as a cohort label, the same reason `site` was dropped.
- A forensic laboratory does not know an unknown donor's recorded ethnicity. A study of aging rates does.

| Option | Pro | Con |
|---|---|---|
| a. Drop `ethnicity`. The fact that sets this case apart: under the plate split it is a cohort label like `site`, and the forensic actor does not know it | Matches the site drop and the forensic use case | First protected-ground drop outside insurance; the use case text must lead with the forensic actor |
| b. Keep it (as implemented) | Follows USE-6 and every medical precedent; it is the paper's own covariate | Rewards a cohort label under the plate split |
| c. Drop both `sex` and `ethnicity` | Fully forensic framing | Sex can be known from DNA; no precedent |

Recommendation: (a) if you take the forensic actor as the lead use case, and record the cohort-label fact in the
notes. Otherwise (b).
Rules: USE-3, USE-6 (Must); principles.md Tensions (rating-factor row); SPLIT-29.

Second prompt (metric, only if mae is taken up):

**Should age be scored by MAE instead of the RMSE fallback?**

**Problem:**
- Hannum names no deciding metric, so the fallback rmse applies. The sibling gse55763 uses the same.
- Forensic age-estimation studies report MAE, but no precedent takes a field habit as `context`.

| Option | Pro | Con |
|---|---|---|
| a. mae, origin context. Fact: an age estimate's cost is linear in years off, as forensic validation reports it | Matches the field; adds diversity | No precedent; must change gse55763 too |
| b. Keep the rmse fallback | Follows MET-5 precedent and the sibling | Departs from field reporting |

Recommendation: (b), unless Hannum's "error" turns out to be defined as a specific metric.
Rules: MET-5, MET-10, MET-11.


</details>

<details><summary>Advocate: gse40279_methylation_age</summary>

Advocate opening brief: gse40279_methylation_age (2026-11-09)
Position: ship as defined (plate grouping, missing-as-missing, rmse fallback), with small changes that need no decision;
ethnicity goes to the curator as a low-stakes question, with keeping it as the precedent default.

1. The task is real, learnable and not trivial (TP-1..TP-5, USE-1/USE-8). Elastic net 5.39 RMSE on plate folds (4.76-6.13
   per fold) vs dummy 15.3; best single probe (ELOVL2) 7.73; gamer's honest ElasticNet 5.89 over all 60 splits, LightGBM
   on 2k probes 14.24. Models spread, no `solved`/`no_signal`. ELOVL2 r=0.86 is the domain's core signal, not a leak (TP-4,
   reading 5; claim, column, domain agree). Blind reviewer's "linear wins, known outcome" is a model-ranking prediction,
   not a validity defect; a p>>n task where trees lose is exactly the diversity a benchmark lacks.
2. No leak and no exploit (LEAK-10/30, Must). Gamer: every exploit loses to honest (plate shrink -0.99, KMeans -1.62,
   test-side centering -3.30, nearest-row age -9.68); row order, formats, ids clean. Column auditor: no leak, no cleaning
   defect; missing indicators R^2 <= 0. The harness copy/NN probes timed out (124), conceded: remedy is a REVIEW.md line
   that the measured stand-ins cover them (no duplicate sample, max correlation 0.9946; gamer's NN exploit -9.68, NN age
   corr 0.18), not a block. Two independent measurements answer the same question the probe asks.
3. The split is right (SPLIT-3/23/29 Must). Plate batch is strong (same-plate NN 68.6% vs 12.1% chance); enet 5.39 plate vs
   4.82 random. Split auditor: "right with notes"; all three auditors back plate over chip (7.10, nested) or site (4
   groups, not nested). Age shift up to 17 y (16 of 60 folds >10 y) is the regime a clock meets in a new study, conceded
   as a fact: add it to the accepted-warning wording (mildest rung: a note).
4. Repair at origin is correct (PROV-13 Must over LEAK-30). 430,448 KNN-imputed cells (0.139%) restored to missing from
   BeadStudio's per-sample betas, measured cell by cell; claim and column auditors and precedent (coad) all confirm.
5. Metric: rmse fallback holds (MET-5, MET-11; precedent gallstone, early_stage_diabetes; sibling gse55763 must match).
   Claim auditor adds Fig. 7A ("standard error (RMSE = 7.22 years)"), so RMSE is likely the source's own error: cite it in
   the reason (no decision). MAE is a field habit, which MET-5 ranks below a source choice; a switch would be a 4th MET-1
   context exception for two datasets at once: a rule amendment, not a block on this one.
6. Ethnicity: keep is the precedent (USE-6 Must; every person-level dataset keeps race/ethnicity; only drop on record is
   sex in insurance pricing). Real problem conceded: it is plate-constant, and in 1 of 60 folds (rep 12 fold 2) the
   Hispanic level is unseen in training. Effect is low (split auditor: "harmless: unseen or constant where it would
   matter"; no probe flagged it). Mildest fix: state both facts in curation_comments and lead the use case with the
   aging-clock study actor (who knows ethnicity; domain: fit DIRECT); option B goes to the curator, not the panel.
7. Width and duplicate repeats are not curation defects (EV-4: runtime is no curation argument). 473k columns: the
   blocker is pyarrow's thrift limit, fixed in the library (PARQUET_READ_LIMITS), not by cutting probes; a probe subset
   would be our selection imposed on the source (and TabBench-Bio's 30k cut is theirs). Label it ultra-wide in the
   README. Repeats 9=11, 8=13 (18 distinct of 280 partitions) are chance with 9 groups: a note in splits_comment.

</details>

<details><summary>Critic: gse40279_methylation_age</summary>

Critic opening brief: gse40279_methylation_age (2026-11-09)
Position: ship only after changes 1-4; 5-7 are notes. No point argues exclusion: the task is real, the target honest,
the gamer found no exploit (honest ElasticNet 5.89 RMSE beats every attack), the imputation rebuild is right.

1. Ethnicity is a cohort label, not a donor property under this split (validity, USE-6 Must, USE-3).
   Problem: plates 5, 6, 9 are 100% Hispanic, all others 100% Caucasian (column, split auditors). Site was dropped as
   "a property of the cohort, which differs in age by design"; ethnicity carries the same cohort (USC 138/139 Hispanic,
   Hispanic mean age 54.6 vs 69.1, a sampling artefact). On rep 12 fold 2 all 230 Hispanic rows are in test and none in
   train (claim auditor): an unseen category. In 16 of 60 folds one side has no Hispanic row.
   Effect: the column teaches cohort age, which a new batch does not share; it is inconsistent with the site drop.
   Remedy: drop ethnicity (builder issue 4, option B). The precedent checker's objection (no protected-ground drop
   outside insurance) does not apply: the reason is the cohort-label fact, the same one that dropped site, not the
   protected ground. Mildest fallback if the curator keeps it: lead with the study actor (point 2) and note the
   plate-constancy and the rep 12 fold in curation_comments.

2. The forensic framing is only approximate (validity, USE-1/USE-8, USE-3).
   Domain practitioner: forensic labs use targeted few-CpG panels and do not know recorded ethnicity; fit direct only
   for the aging-clock study. Remedy: rewrite the use case to lead with the clock-study actor; forensic second, marked
   approximate. Text change only.

3. Copy and nearest-neighbour leak probes and the group probes never ran (validity procedure, LEAK-16..21, EV-8).
   leak_probes.log and group_probes.log ended at exit 124 (claim auditor); task probes ran at 3 splits, not 30.
   Stand-ins exist (max sample correlation 0.9946, no duplicate; gamer's NN-age exploit -9.68; one pair at 0.957 vs
   median 0.80, a possible replicate). Remedy: re-run leak probes 5/6 and group probes on a screened probe subset
   (e.g. 20k), or record in REVIEW.md that the scratch checks stand in, naming the 0.957 pair.

4. The container cannot be built or read with defaults (ship blocker, not a curation rule).
   656 x 473,038 parquet fails pyarrow's thrift footer limit; build would delete the folder in verify_saved_container;
   any consumer reading with defaults fails (builder, blind reviewer). Remedy: the PARQUET_READ_LIMITS library change
   plus the harness/examples entry before shipping. I do not ask for a probe subset: runtime and width are no
   curation argument (EV-4, CLEAN-22 keeps all probes); label it ultra-wide in the README instead.

5. Fold scores partly measure cohort age shift (value, USE-10 / SPLIT-24 Weigh).
   Test-minus-train mean age -15.6 to +17.0 y; 16 of 60 folds over 10 y; train-mean dummy RMSE 12.8-20.4 across folds;
   126 test rows outside the train age range. Remedy: put the numbers in the accepted warning text, not only
   "shifts the cohort".

6. 20 repeats are 18 distinct partitions (quality, EV-8 weight): reps 9=11, 8=13 count twice. Remedy: a note in the
   splits comment.

7. Metric reason is weaker than it can be (quality, MET-5): cite Fig. 7A ("standard error (RMSE = 7.22 years)") as
   evidence the authors' "error" is RMSE; if it reads as defined, origin may be source rather than fallback. Keep rmse;
   mae would need a rule-level MET-11 decision for both siblings (precedent checker), not this dataset.

</details>
