# cns_tumor_methylation_classification

**Outcome:** added. The DKFZ reference set of the CNS tumour methylation classifier (Capper et al. 2018, GEO GSE90496): 2,801 samples, one per patient, 428,799 CpG beta values plus the tissue material, 91 methylation classes, random 3 x 10 folds stratified by class, log loss as the fallback metric. The panel recommends shipping after changes; six text changes are made (the count of subdividing classes (27), the 10-15% chip optimism in the split comment, the `Class-dependent Recording` marker, the note on the 35 arrays shared with sarcoma_methylation_classification, the note on clinical fit, and a protocol line forbidding test-batch rebalancing), and the one Must left is whether the classes drawn only by clustering stay (issue 1, decided together with `sarcoma_methylation_classification`). The 91 classes stay until then. No container is built yet: the build fails because frames this wide exceed a read limit of pyarrow, the library that reads the data files; that fix is a package change, outside this review. The model probes ran on 2,000 to 10,000 high-variance probes, never on all 428,799. The claim auditor did not re-run the material and chip probes. No probe was re-run after the text changes, which change no data.

**Main points:** Check each subdividing class against WHO 2021 and merge only those with no outside definition (issue 1)? Add a scoring column for the 0.9 sign-out threshold or for class families (issue 2)? Accept the one check warning (issue 3)?

**Record judgment:** valid. A real diagnostic task in routine use, from a Nature paper and its GEO deposit; the open question is the origin of part of the labels, not the data. The record now carries `Class-dependent Recording` for the material, which is tied to the class (35 classes have one material only) but measured to give no shortcut (material alone: log loss 4.04 against 4.19 for the class shares).

**Issues for the curator:**

1. **Check each subdividing class against WHO 2021 and merge only those with no outside definition?**

   * **Problem:**
     - Some of the 27 classes that subdivide a WHO entity may have no definition outside the clustering of these same profiles.
     - For such classes the score partly measures how well a model recovers the clusters that made the labels.
   * **Effect on the task:** a linear model reaches a macro ROC AUC of 1.000 and a sample's nearest neighbour has its label in 0.909 of cases; log loss still spreads from 0.11 (linear) to 0.48 (LightGBM) to 0.80 (random forest), so the task is not trivial, but part of that separability comes from the label origin.
   * **Background:** the paper states that "all histopathological entities and variants were analysed by unsupervised clustering" ([Capper et al. 2018](https://doi.org/10.1038/nature26000)); the WHO classification of 2021 (CNS5) defines several tumour types and subtypes by their methylation class ([Louis et al. 2021](https://doi.org/10.1093/neuonc/noab106)).
   * **Experiments:** the classifier changed the diagnosis in 129 of 1,104 prospective cases (11.7%, checked); the class description lists 36 classes one to one with a WHO entity, 27 as subclasses of one, 19 not equivalent to one, plus 9 control classes.
   * **Consistency:** `brca`, `glioblastoma` and `ov` were retired on 2026-10-12 for clustering-only subtypes[^sel4]; the sibling `sarcoma_methylation_classification` merges its clustering-only subgroups, with the same "clinical classifier" argument on the other side; keeping all 91 here would depart from both with no fact that sets this case apart, while a class WHO defines by methylation is such a fact, class by class.
   * **Panel:** the advocate, the critic and the precedent checker all back option a; the advocate stresses that the 91 classes are what the classifier in clinical use outputs, the critic that clustering-only classes were retired before.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | a | Check class by class (implemented) | the 91 classes kept until the check; then each of the 27 subdividing classes is checked against WHO 2021; a class WHO names, or with another outside definition, stays; the rest merge into their WHO entity; the same way in `sarcoma_methylation_classification` | keeps the subtypes WHO defines by methylation; consistent with the 2026-10-12 retirements and the sibling | a class-by-class reading of WHO 2021; the class count changes |
     | b | Keep all 91 here and undo the sibling's merge | the classes as published in both datasets | the classifier's own output | contradicts the 2026-10-12 retirements |
     | c | Merge every subclass into its entity | fewer classes, none below the WHO entity | no class rests on clustering | loses the subtypes WHO defines by methylation |
     | d | Retire | the dataset leaves | none found | most classes are WHO entities with outside definitions, so a smaller fix is enough |

   * **Recommendation:** a, applied the same way in both methylation datasets. **Decision:** a, b, c or d? Decide alike with `sarcoma_methylation_classification` issue 1; the shared test is the across-datasets item **Clustering-defined classes**.

   **Notes for the AI:** on a, list the 27 classes whose relation in `GSE90496_methylationclassdescription.xlsx` is a subclass of a WHO entity, look each up in WHO CNS5 (Louis et al. 2021, the types and subtypes and their "essential and desirable criteria"), map the unnamed ones to their entity in `_clean` with a dict and the reason per class in a `Decision` table; recount the subdividing classes in the curation notes (the 27 / 29 sentence), the task summary's 91 / 82 and the smallest classes; re-run `dataset check`, the log-loss fallback check (2 test and 5 train rows per class) and the light probes; do the same in `sarcoma_methylation_classification`.

   [^sel4]: **SEL-4** (Must): "A label from unsupervised learning is no real predictive task: a molecular subtype
     defined by clustering (PAM50, expression subtypes, NMF clusters)." Cases: brca_breast_cancer, glioblastoma,
     ov_ovarian_cancer (Lennart, 2026-10-12).

2. **Add a scoring column for the 0.9 sign-out threshold or for class families?**

   * **Problem:**
     - The clinic signs a sample out only at a calibrated score of 0.9 or more, and reports "no match" otherwise (about 12% of prospective cases; the domain practitioner's figure, not checked).
     - A mistake within a class family weighs less for the pathologist than one across families, which log loss does not see.
   * **Effect on the task:** none on validity; a second view of the score closer to the clinic's use.
   * **Panel:** the domain practitioner proposed it; neither the advocate nor the critic pressed it; the mediator left it optional.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | a | Note only (implemented) | the fit note in the curation notes names the threshold and the "no match" share | no extra column; the metric stays the fallback | the benchmark score ignores the threshold and the families |
     | b | Add a scoring column | the class family per row as a scoring column, for a family-level or thresholded secondary score | closer to the clinic's decision | a second score the benchmark does not use yet; a family mapping to curate |

   * **Recommendation:** a; no benchmark score uses a scoring column yet, and a family mapping would have to be curated first. **Decision:** a or b?

   **Notes for the AI:** on b, add the family from the class description (its methylation class family column) as a column listed in `task_metadata.scoring_columns`, never a feature.


3. **Accept the check's warning about stratifying by the 91 classes?**

   * **Problem:**
     - `dataset check` warns that stratifying by `methylation_class` uses 91 distinct values.
     - That column is the target, and stratifying by class keeps every class in every fold (at least 2 test and 5 train rows each, checked on all 30 splits).
   * **Effect on the task:** none; without stratification the 8-sample classes could miss a fold, and the log loss would not be computable there.
   * **Panel:** the claim auditor confirmed the per-fold class counts; the task gamer's rebalancing exploit rests on these stratified folds and is covered by the protocol line in the split comment (a model scores each test sample on its own).
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | a | Accept the warning | the text below goes into `accepted_check_warnings` | every class in every fold | the class-stratified folds allow the test-batch rebalancing (about 8% lower log loss), which the protocol line forbids |
     | b | Leave it open (implemented) | the warning stays unaccepted | none found | the check keeps warning |

   * **Recommendation:** a. **Decision:** accept the warning, yes or no?

   **Notes for the AI:** on yes, add to `accepted_check_warnings` in `dataset.py`: `{"task_stratify_high_cardinality": "Stratified by the target, 91 classes of 8 or more samples: every test fold holds 2 or more and every train side 5 or more samples of each class (30 splits checked), which the log loss needs."}`, then a light check (no full `dataset check` needed beyond the warning list).

**Review panel:** ship after changes (mediator). The five text changes are made; the one Must left is the classes drawn by clustering (issue 1), with advocate, critic and precedent checker agreeing on a class-by-class check. Claims: none refuted. Blind review: exclude as prepared, unless cut to the top 5-10k probes or moved to a high-dimensional track; dropped, because width is no reason to drop features and the curator picked this dataset for its width (2026-11-08). Task gamer: only test-batch rebalancing, about 8% log loss, now a protocol line. The rebuttal round was skipped: the advocate's and the critic's opening briefs converged.

<details><summary>Mediator: cns_tumor_methylation_classification</summary>

**Recommendation (judgment record)**
- **Verdict:** ship after changes.
- **Dataset:** cns_tumor_methylation_classification. 91 classes. IID split, 3x10, by patient (the authors' makefolds). Metric: log_loss as the fallback. Features: all 428,799 probes plus material.
- **Deciding rule:** SEL-4 (Must; some classes were drawn by clustering these same profiles).
  - Remedy, by the ladder: fix the definition class by class. Retiring the dataset is not needed.
  - Keep the 91 classes until the class-by-class check is done.
- **Rules that hold:** P4 / LEAK-1/13/15/16-21/27-31; SPLIT-1/29/30; MET-5; TP-3/8.
- **Owner:** the curator (Lennart), decided jointly with sarcoma_methylation_classification issue 1.

**Changes to make now (no decision needed)**
1. Fix the count of classes that subdivide a WHO entity: the notes say 29, the builder says 27. Rule: PROV (claims match the evidence). Recount when the check in issue 1 is done.
2. splits_comment: replace "batch signal is weak" with the measured optimism. On a new chip or centre, log loss is about 10-15% worse: 0.83 with folds grouped by chip, against 0.73 with random folds. Rule: SPLIT-29/30, as in the tcga_pancancer, treehouse and sarcoma precedents.
3. Add the `Class-dependent Recording` marker to the record. Material is tied to class (35 classes have one material only). Rule: the leak_checks.md rule for LEAK-13/15. The same gap was found in sarcoma_methylation.
4. PROV-7 note, in this dataset and in sarcoma_methylation: the 35 shared arrays are the GSE90496 part of sarcoma's 40. The other 5 come from GSE109379, which this dataset excludes. Keep A in both; there is no leak within either dataset.
5. A note on fit (USE-1/USE-8, fit approximate):
   - The clinic signs out at a calibrated score of 0.9 and has a "no match" outcome, which about 12% of prospective cases get.
   - Samples were selected for tumour content of 70% or more.
   - Age, location and histology are absent.
   - Effect: scores overstate performance on routine cases. Both sides agree.

**Issues for the curator, ranked**
**1. SEL-4 (Must, validity): classes drawn partly by clustering these profiles.**
- **Problem:** some subclass classes may have no definition outside the clustering of these same data. For those, the score partly measures how well a model recovers the clusters.
  - A linear model reaches macro AUC 1.000.
  - The nearest neighbour has the same label in 0.909 of cases.
- **Advocate's best evidence:**
  - The 91 classes are what the clinical classifier outputs and what the neuropathologist signs out.
  - WHO 2021 defines several CNS types by methylation class.
  - 129 of 1,104 prospective diagnoses were revised by the classifier (11.7%, checked).
- **Critic's best evidence:**
  - The paper says every entity was analysed by unsupervised clustering.
  - brca, glioblastoma and ov were retired on 2026-10-12 for clustering-only subtypes.
  - Sibling sarcoma_methylation merges its clustering-only subgroups and gives the same "clinical classifier" reason.
- **Settled by:** both sides and the precedent checker back option (a). Check the 27 (or 29) subdividing classes one by one against WHO 2021 CNS5. Keep every class WHO names or that has another outside definition; merge the rest into their entity.
- **Decision needed:** confirm (a), applied the same way in both datasets.
- **Options rejected:**
  - (b) Keep all 91 here and undo sarcoma's merge. This contradicts the 2026-10-12 retirements.
  - (c) Merge all subclasses. This loses the subtypes WHO defines by methylation.
  - (d) Retire. Most classes are WHO entities with outside definitions, so the ladder rules it out.

**2. Optional (Should, value): add a scoring column for the 0.9 threshold or for class families.**
- The domain practitioner proposed it; neither side pressed it.
- **Decision needed:** add it or leave it as a note.

**Points dropped, with the reason**
- **The blind reviewer's width exclusion** (p/n about 150, load takes more than 5 minutes, cut to the top 10k CpGs). This is not a validity conflict. CLEAN-22 / EV-4 and the coad precedent say width is no reason to drop features. The curator accepted this dataset on 2026-11-08 in the large-candidates batch, picked for most rows and most features. A probe cut is the method's own choice.
- **"Near-trivial":** no. Log loss spreads from 0.11 (linear) to 0.48 (LightGBM) to 0.80 (RF).

**Task gamer's exploits, mapped to rules**
- **Rebalancing the test batch's probabilities to the train class proportions** (Sinkhorn): log loss 0.117 -> 0.108, about 8%, on 3 of 30 splits. The oracle using the true test counts reaches 0.105.
  - Rule: LEAK-9, an evaluation-level leak. A method that learns from the test block is called out and not benchmarked.
  - It also uses the class-stratified folds, which rests on the warning task_stratify_high_cardinality (editor's note: not yet accepted, issue 3).
  - A deployed model scores one sample at a time, so it does not have this.
  - Status: new, as far as I can tell (I found no `Potential leak, kept on purpose:` note covering it; editor's note: now covered by the protocol line in splits_comment, LEAK-9). It is minor, and both sides drop it.
  - Optional: a protocol line under LEAK-9. No decision is needed.
- **Nothing else found:** row order, copies (only one pair above corr 0.98, same class), number formats, identifiers, standardising over all rows (+0.0004), material (no gain).
- The gamer's own top-10k variance selection over all rows is in its own script, not in the shipped data. The dataset uses per-sample preprocessing (LEAK-30 is not triggered).

**Agreed facts**
- No exact copies across splits. Closest pair corr 0.951 in the copy check; the gamer found one pair above 0.98 on 5,000 probes (same class).
- Material alone scores 4.037 log loss against 4.19 for the prior. Rows with the rarer material score 0.64 against 0.65: no shortcut.
- One sample per patient. The IID folds equal the authors' makefolds.
- Chip-mate effect 0.97 vs 1.00. Folds grouped by chip leave 9-28 test rows of classes unseen in training, in every seed.
- Log-loss fallback is correct and computable on all 30 folds (at least 2 test and 5 train rows per class).
- 18 classes with 10 samples or fewer carry 12.0% of the loss on 5.6% of rows (TP-8, as in forensic_glass, ljubljana and sarcoma).
- Linear macro AUC is 1.000, so AUC saturates; log loss does not.
- The 35 vs 40 shared-array counts reconcile through GSE109379.

**Consistency with precedent**
- **Issue 1:** keeping all 91 classes departs, with no stated reason, from sarcoma_methylation and the 2026-10-12 retirements. Option (a) removes the departure. The fact that separates this case is per class: WHO 2021 defines some CNS types by methylation. "Clinical use" does not separate it.
- **Chip split:** consistent with tcga_pancancer, treehouse, sarcoma and sarcoma_methylation, all of which picked A. Here the batch signal is the weakest of the set. Their condition, stating the optimism in splits_comment, is change 2.
- **Material:** consistent. It is a declared feature, not a third exception of the recording-route kind. It still needs the marker (change 3).
- **TP-8, MET-5, LEAK-30/31 and the stratification warning:** consistent.


Short summary: ship after changes. There are five text fixes: the 27/29 count, the optimism number in splits_comment, the Class-dependent Recording marker, the 35/40 note, and the fit note. One Must goes to the curator: confirm option (a) for SEL-4 (check each class against WHO 2021, merge only those with no outside definition), jointly with sarcoma_methylation. Keep the 91 classes until then. The width exclusion and the rebalancing gain are dropped; the rebalancing exploit is minor, falls under LEAK-9, and a deployed model does not have it.

</details>

<details><summary>Advocate: cns_tumor_methylation_classification</summary>

Advocate opening brief: cns_tumor_methylation_classification (2026-11-09)
Position: ship as defined (91 classes, IID 3x10, log_loss fallback, all 428,799 probes + material), with three
no-decision text fixes. Issue 1 (SEL-4) is the one real question; I argue the mildest fix there, not a denial.

1. No leak, no copies, no shortcut, and the gamer could not break it (P4, LEAK-1/13/15/16-21/27-31, Must).
   Evidence: 0.0% exact copies over 30 splits, closest pair corr 0.951; material alone 4.037 vs prior 4.19 (claim
   auditor re-ran); rarer-material rows 0.64 vs 0.65; per-sample preprocessIllumina, no supervised probe selection;
   column auditor: only betas + material ship, title and chip id kept out. Task gamer: "hard to game"; the only gain is
   test-batch rebalancing (0.117 -> 0.108) that needs the batch's joint composition, unavailable to a deployed
   per-sample model. Every P4 Must holds; this is the top-ranked block and it passes.

2. The target is what the actor acts on (P3, USE-5, USE-1 fit approximate). Domain practitioner: the 91 classes are
   exactly what the clinical MNP classifier outputs and what the neuropathologist signs out at score >= 0.9; WHO 2021
   defines several CNS entities by methylation class; merging (builder's B) "would throw away resolution I use".
   129/1,104 prospective diagnoses revised by it (claim auditor checked 11.7%).

3. SEL-4 (Must) is real for part of the classes; the remedy is per class, not retirement (remedy ladder: fix the
   definition > exclude). I concede the precedent checker's point: "clinical use" alone does not separate this from
   sarcoma_methylation's merge or the 2026-10-12 retirements. But WHO-named methylation types/subtypes have an outside
   definition, which brca/glioblastoma/ov subtypes lacked. So adopt precedent option (a): merge only classes with no
   outside definition, jointly with sarcoma_methylation. Until that per-class check is done, A (keep 91) is the
   honest default since most classes are WHO entities; retirement (d) is ruled out by the ladder.

4. Width is the point of the batch, not a defect (P6 vs curator's decision). The record carries Lennart's CC of
   2026-11-08 accepting it in the large-candidates review chosen for "most rows, most features". The blind reviewer's
   p/n 150 and load time are the reason it was picked; a top-10k cut would be our supervised/unsupervised selection
   (LEAK-31 risk if label-informed) and is a benchmark-side choice a method can make itself. Independent failure of
   some methods to scale is not a conflict with any validity rule.

5. Not solved in the metric that ships (TP-3, TP-8, MET-5/8). Macro AUC saturates (linear 1.000) but log loss spreads
   0.11 (linear) to 0.48 (LightGBM) to 0.80 (RF) at K=2,000; 18 classes of <= 10 samples carry 12.0% of the loss on
   5.6% of rows. Log loss is the proper rule that scores the practitioner's calibrated 0.9 threshold; the source names
   no single metric, so the fallback is correct (claim auditor: holds; MET-2 computable on all 30 folds, min 2 test /
   5 train per class).

6. IID split is right and the alternative is unscoreable (P4 over P6, SPLIT-1/29/30, "the split follows the
   application; a small signal is no reason to retire"). One sample per patient; = authors' makefolds; chip-mate effect
   0.97 vs 1.00; StratifiedGroupKFold by chip leaves 9-28 unseen-class test rows in every seed (split auditor). Four
   batch precedents (tcga_pancancer, treehouse, sarcoma, sarcoma_methylation) picked A; this one has the weakest signal.

7. No-decision fixes (keep with a note, bottom of the ladder): (i) splits_comment states ~10-15% optimism in log loss
   for a new chip/centre (0.83 vs 0.73), as tcga/sarcoma; (ii) add `Class-dependent Recording` marker (leak_checks.md
   rule for LEAK-13/15); (iii) PROV-7 note: 35 shared = GSE90496 part of sarcoma's 40 (other 5 from GSE109379), decided
   jointly, A in both (no within-dataset leak). Optional README line: practitioner's 0.9 sign-out threshold and missing
   age/location (makes the task harder, not leakier).

</details>

<details><summary>Critic: cns_tumor_methylation_classification</summary>

Critic opening brief: cns_tumor_methylation_classification (2026-11-09)
Position: ship only changed. Point 1 is a Must and has to be settled before the dataset ships. Points 2-5 are notes or fixes to the record.

1. Validity, SEL-4 (Must): some of the 91 classes are drawn only from clustering of these same profiles, and keeping them all departs from precedent without a reason.
   Effect: for those classes the model recovers clusters from the data that made them, so the score partly measures cluster recovery and not a diagnosis (linear macro AUC 1.000; 1-NN label agreement 0.909).
   Evidence: dataset.py notes quote the paper ("All histopathological entities and variants were analysed by unsupervised clustering"). Precedent checker: brca/glioblastoma/ov were retired for clustering-only subtypes (2026-10-12). The batch sibling sarcoma_methylation merges its clustering-only subgroups and gives the same "clinical classifier" reason, so that reason does not separate the two cases. The counts also disagree: the notes say "29 of the 82 tumour classes subdivide a WHO entity", the builder says 27.
   Remedy, the mildest that works: precedent option (a). Check the subdividing classes one by one against WHO 2021 CNS5. Keep every class that WHO names or that has another definition outside the clustering. Merge the rest into their entity, decided together with sarcoma_methylation issue 1. Fix the 27/29 count. I do not ask for retirement: most classes are WHO entities with outside definitions.
2. Value, USE-8/USE-1 (fit approximate): the clinical decision has a "no match" outcome at a calibrated score of 0.9, and about 12% of prospective cases fall there. Tumour purity is 70% or more, and age and location are absent. The README states only the 0.9 threshold, inside the metric reason. Effect: scores overstate how the model does on routine cases. Remedy: add a note in the task summary or notes (domain practitioner).
3. Split, SPLIT-29/30: the splits_comment says only "batch signal is weak". The precedents (tcga_pancancer, treehouse, sarcoma) state the measured optimism in splits_comment. Here the chip-grouped log loss is 0.83 against 0.73 random, about 10-15%. Remedy: put that number in splits_comment (split auditor, precedent checker).
4. LEAK-13/15 marker: material is tied to class (35 classes have one material). leak_checks.md asks for the `Class-dependent Recording` marker on the record whenever LEAK-13/15 applied. The record lacks it. Remedy: add it (a fix, not a decision).
5. PROV-7: the note gives 35 shared arrays, while the sarcoma dataset gives 40 (these 35 plus 5 from GSE109379, which is excluded here). Remedy: say so in both notes so the counts reconcile.

Dropped, not backed by the rules:
- The blind reviewer's width/p-n exclusion: CLEAN-22/EV-4 and the coad precedent say width is no reason to drop features.
- "Near-trivial": log loss spreads from 0.11 to 0.80 across models.
- The gamer's Sinkhorn rebalancing gain (-8%): it needs the batch of test rows together, which a deployed model does not have. Minor.

</details>

<details><summary>Claim audit: cns_tumor_methylation_classification</summary>

Claim auditor report: cns_tumor_methylation_classification (2026-11-09)
Verdict: no claim refuted by my tests. Ship per builder issue 1 decision.
Script: the run folder (on the builder's cached ProbeInput top-2000: shipped target + 30 splits; no build).

claim | source | test | result | evidence | rule
7 split / warning acceptance (2+ per class per test fold, 5+ per train side) | dataset.py split, builder warning text | class counts per fold over all 30 splits | holds | every test fold 91 classes, min 2 or 3; every train side 91 classes, min 5; each repeat's test folds partition 2,801 rows | SPLIT-1, TP-8
Metric log_loss fallback | dataset.py metric, README Metric | MET-5 table: paper reports error, mAUC, Brier side by side, none named; MET-8 prefers a proper rule | holds | MetricSpec origin=fallback, proba, reason quotes Methods; consistent with metrics.md line 298 | MET-5, MET-8
Metric computable | MET-2 | dummy class-share predictions per fold, log loss with all 91 labels | holds | 4.184-4.192 on all 30 folds (builder 4.19); every class in every fold | MET-2
25 material alone 4.04 vs 4.19 | curation notes | material x class table (+0.5 smoothing), 30 splits | holds | 4.037 | LEAK-13/15
17 closest pair 0.951 | curation notes | builder cache nn_corr.npy | holds (re-read, not recomputed independently) | max 0.9514 | LEAK-16
1,5 91 classes | task summary | unique targets | holds | 91 | -
2 12% of 1,104 | task summary | arithmetic | holds | 129/1104 = 11.7% ~ 12% | EV
39 metric reference text | dataset.py | not re-opened PMC6093218 | untested (time) | builder quotes Methods verbatim | MET-1
26,27,32-34 material/chip probe numbers | notes | not rerun | untested (cost: RF on 10k probes) | builder JSON exists | SPLIT-29/30
Implied: features known at prediction point | - | field list: betas + material only | holds | lab knows material at profiling | LEAK-1
Implied: target real-world | - | judgment, classes partly from clustering the same profiles | open (builder issue 1, SEL-4 Must) | not testable on data | SEL-4

Ranked open items (none refuted):
1. SEL-4 issue 1 (label partly from clustering same profiles): judgment, not data-refutable; mildest remedy is A (keep) with the glioblastoma consistency note in REVIEW.md.
2. SPLIT-29/30 chip batches: builder numbers not reproduced by me; mildest remedy: keep IID, state it in splits_comment (already done).
3. Metric reference quote not re-read by me (MET-1): low risk.

</details>

<details><summary>Column audit: cns_tumor_methylation_classification</summary>

Column auditor: cns_tumor_methylation_classification (2026-11-09)

Verdict: ship. No leak column and no cleaning problem found. One question for the curator (material) and one note.

Prediction point (first bullet): the sample has been profiled on the 450k array; class assigned from betas + material.

Column table (2,801 rows x 428,801 columns: 428,799 betas, material, target)
column | meaning | known at prediction? | dtype and cleaning | verdict | rule
cg* (428,799) | beta value: methylated share at one CpG site, per-sample minfi preprocessIllumina (GEO) | yes: the measurement itself | float64, lossless from file; on the 10,000 top-variance probes min 7.3e-6, max 0.9995, no 0/1, no NaN (none in full frame per builder); no constant/duplicate column; probe set = paper's 428,799 exactly; dtype probe 0 flags at full width | fine | LEAK-27..31 (no cross-sample step, no supervised selection), CLEAN-12/14
material | FFPE (1,878) or Frozen (923), series characteristic | yes: lab knows it at profiling | category, 2 levels, no unknown code | fine; question (below) | LEAK-13/15
methylation_class (target) | DKFZ methylation class, abbreviation decoded to class description name | outcome | category, 91 levels; decoded names are unique (92 description rows, 0 duplicate names), so no two classes merge | fine | CLEAN-25, SEL-4 (curator issue 1)
Not shipped: GSM accession (identifier, correctly dropped), Sentrix/chip id (batch; dropped), detection p-values (quality measure; dropped), title (encodes the class, "<class>, sample n": correctly not shipped).

Problems, ranked
1. (P4, question) material tied to class: 35 classes single-material (591 samples). The builder measured no shortcut (alone 4.04 vs 4.19 log loss; RF 0.728 vs 0.731; rarer-material samples 0.64 vs 0.65; betas predict material AUC 0.976). Mildest remedy: keep as is (option A); I agree. It is a recording-by-class property of the reference cohort, not a post-outcome field.
2. (P5, note) detection p-values left out: correct; they are a recording-quality field, and missing-by-quality patterns could encode material/centre. No action.
3. (note) The title column, which literally contains the class, and the chip id (same-class chip-mates, 34% vs 2% chance) are both kept out of the frame. Keep them out; a future edit adding "sample metadata" must not re-add them.
Nothing else: no identifier, no timestamp, no outcome-caused missingness, no proxy codes, no ordinal scale.

</details>

<details><summary>Split audit: cns_tumor_methylation_classification</summary>

Split auditor: cns_tumor_methylation_classification
Verdict: RIGHT WITH NOTES (IID, 3 folds x 10 repeats, stratified by class).

Regime. Use case: type the tumour of a new patient from one 450k profile. Entity = patient; the source states one
sample per patient (n=2801 patients; 2,801 biologically independent samples), so random rows = new patients. No time
column (GEO gives none besides class, material, Sentrix id); no temporal regime is implied by the data available.
Hidden groups: builder probe hidden_top2000 found 0 candidates, 0.0% near copies; closest pair corr 0.951. Exact
copies across 30 splits 0.0%. Nothing to group on among the columns.

Finding 1 (P4, SPLIT-29/30, note not defect): array chips. 691 chips of 1-12 samples, 59% of samples have a
same-class chip-mate. In deployment a new sample is always on a new chip, so the faithful split would group by chip.
Builder's chip-grouped RF (10k probes, 6 splits): log loss 0.826 +- 0.045 vs random 0.728 +- 0.007 on seen classes,
accuracy 0.925 vs 0.950; but 9-29 test rows of unseen classes in 4 of 6 splits. I re-checked the mildest alternative,
StratifiedGroupKFold(3) by chip, 5 seeds: unseen-class test rows still 9-28 in at least one fold of every seed, and
classes with 0 train samples in most seeds -> a chip-grouped split is not scoreable for a 91-class log loss.
Chip-mate-in-train effect is small (0.97 vs 1.00 log loss). Part of the 0.10-nat gap is class concentration
(whole-class chips leave training thin), not batch leakage. Remedy: keep IID (= authors' makefolds.R); the
splits_comment already says chips fall on both sides. Optional: state in the comment that scores may be ~10-15%
optimistic in log loss for a sample from a new batch/centre (chip-grouped estimate 0.83 vs 0.73).

Finding 2 (P4, note): centre and year are not in the data, so the test stands for the same centres and years
(declared honestly in task_summary.split). No remedy possible.

Finding 3 (P6/P4, fine): smallest classes (8 samples) give 2-3 test rows per fold and >=5 train; stratification
needed and present.

Builder issue 2 (chip grouping): agree with recommendation A. Issue 4 (35 arrays shared with
sarcoma_methylation_classification): cross-dataset, no effect on this split.

</details>

<details><summary>Domain practitioner: cns_tumor_methylation_classification</summary>

Domain practitioner report: cns_tumor_methylation_classification (2026-11-09)
Actor: a neuropathologist (or the molecular lab of a neuropathology department) who, after surgery or biopsy, runs the
tumour's DNA on a methylation array and uploads it to the DKFZ/MNP classifier (molecularneuropathology.org) to get a
class and a calibrated score, which is then integrated with histology into the WHO 2021 integrated diagnosis.

VERDICT
Fit: approximate (agree with the definition, USE-8). The inputs and the 91 classes are exactly what the clinical v11b4
classifier saw and outputs, so a model here does the classifier's job; but the cohort is curated (high tumour content,
confirmed class), so routine cases (low purity, no-match tumours) are easier here than in the clinic.
Metric scores the decision: partly-yes. Log loss (fallback, MET-8) is the right choice; I would keep it.

1. INPUTS AT THE PREDICTION POINT (USE-3, USE-6)
- Beta values at 428,799 CpGs: yes, I have them the moment the array is read (I would have the IDATs and normalise
  myself; GEO's per-sample preprocessIllumina betas are a faithful stand-in, no cross-sample step to undo). OK.
- Material (FFPE/frozen): yes, the lab always knows it. The authors adjust for it; shipping it as a feature is
  legitimate (USE-6). Agree with builder issue 3 option A.
- What I always have that is missing: patient age, tumour location (posterior fossa / supratentorial / spinal), and
  the histological impression. In practice these strongly disambiguate (e.g. ependymoma subgroups by site, medullo-
  blastoma vs. adult tumours by age). GEO does not ship them, so the gap is unavoidable; it makes the task slightly
  harder than mine, not easier. Also the copy-number profile, but that is derived from the same array (implicit).
- Nothing in the features is unavailable to me at decision time. No leak.

2. TARGET (USE-5)
- The methylation class is what the classifier reports and what I act on (class + family; the family carries most
  treatment consequences, the class refines prognosis/trial eligibility). Not a proxy. It is the classifier's
  training labels, not an independent ground truth, and some classes were defined by clustering these same profiles
  (builder issue 1). For my use that is fine: I want to reproduce the reference classes, which since WHO 2021 define
  several entities. Agree with option A; option B (merging into WHO entities) would throw away resolution I use.
- What I want out: a calibrated probability per class (the MNP tool reports calibrated scores and I sign out a class
  only at score >= 0.9, otherwise "no match"/refer). So probabilities, not a hard class.

3. ROW AND TEST DATA (USE-1, USE-10)
- One row = one patient's tumour sample = one diagnostic decision. Matches.
- Test data: random stratified folds of the reference cohort = new patients from the same centres and era. What I
  actually face differs in three ways, ranked by impact:
  a) Routine cases include low tumour purity and tumours of no reference class (in the prospective 1,104 cohort, ~12%
     no-match / not classifiable). The benchmark has no "none of these" outcome. Biggest gap; it is not fixable from
     this data (the validation set's labels are classifier calls, correctly left out).
  b) New centres and the EPIC array (most labs now run EPIC/EPICv2): a model trained here meets a platform and batch
     shift. The probe set already restricts to EPIC-shared CpGs, which is good.
  c) Array chip batch: weak (0.97 vs 1.00 nats); random split acceptable (builder issue 2 option A). A new patient
     arrives on a new chip, so a chip-grouped split would be closer in principle, but it removes whole classes from
     training; I accept A.
- Shared arrays with the sarcoma dataset (issue 4): irrelevant to my decision; A is fine.

4. WOULD I USE IT / TRUST
- I would use a model whose cross-validated log loss beats the reference (paper: error 4.3%, AUC 0.99) only after
  calibration on my lab's FFPE/EPIC cases and a check on low-purity samples. Trust rises with: good calibration on the
  rare classes (18 classes <= 10 samples carry 12% of loss), low confident-wrong rate within family. Distrust: high
  scores on low-purity samples, confidence on samples of no class. Small classes are real clinical entities; keeping
  them is right.

5. METRIC (MET-1, MET-6 to MET-9)
- Source names no single criterion (error, multiclass AUC, Brier; code adds log loss), so fallback is correct (MET-5).
- My decision acts on a calibrated probability against a 0.9 threshold; a strictly proper rule over the full
  probability vector scores exactly that (MET-8). Log loss is right and separates models where macro AUC (1.000 for
  logistic regression) is saturated, so AUC would not let me choose (MET-9 spirit). Accuracy/error (MET-6) would hide
  calibration, which is what my 0.9 rule needs.
- Why only "partly": the real cost structure is asymmetric and family-aware (a wrong family is far worse than a wrong
  subclass in the same family; abstaining below 0.9 has a cost too). No source fixes a cost matrix (MET-7 not
  applicable), so log loss is the best declarable choice. Would I pick it over the multiclass Brier score? Log loss
  punishes confident errors on rare classes hard, which matches my fear of a confident wrong call; I would keep log
  loss, with Brier as the second option.

EXPERT CHANGES (none blocking)
- Mention in the README that the clinical decision thresholds the calibrated score at 0.9 and has a "no match" outcome
  that this benchmark lacks; and that age/location, always known clinically, are absent.
- Optional: ship the 8 class families (Fig. 2b) as a scoring column for a family-level report (not as the target).

SOURCES
Capper et al. 2018 Nature 555:469 (Methods: reference cohort, calibrated score 0.9, 1,104 prospective cases, 12%
changed diagnosis); Louis et al. 2021 WHO CNS5 (methylation-defined types); mnp_training repo (makefolds, batchadjust,
CVresults); GSE90496 description; dataset.py, README.md, builder_report.md; use_case.md (USE-1,3,5,6,8,10),
metrics.md (MET-5 to MET-9).

</details>

<details><summary>Blind review: cns_tumor_methylation_classification</summary>

Blind review: cns_tumor_methylation_classification (Capper et al. 2018, Nature, GSE90496)

TASK: Predict the DNA-methylation class (91 classes) of a CNS tumour from Illumina 450K beta values
(428,799 CpG columns) plus tissue material (FFPE/Frozen). 2,801 rows. Real clinical use: the
Heidelberg/DKFZ MNP classifier is used by neuropathologists at diagnosis to assign tumour type.
All features are measured on the resected tissue at diagnosis, so no temporal leakage.

VERDICT: Exclude from a general tabular benchmark as prepared (include only with changes, e.g. a
reduced feature set, in a dedicated high-dimensional track).

CONCERNS (most to least serious):
1. Shape is not tabular-benchmark scale: 2,801 x 428,801 (p/n ~ 150). Just reading the parquet took
   >5 min here; most tabular methods (TabPFN-style, GBDT with 30 splits, AutoML) will be infeasible or
   dominated by feature-selection choices. Change: preselect e.g. top 5-10k most variable CpGs (as
   Capper did, 10k probes) or move to an omics track.
2. Near-trivial ceiling: a plain logistic regression on 2,000 high-variance probes from a 1/40 column
   subsample gives 96.5% 3-fold accuracy. Capper report ~98% CV for their RF. Little room to separate
   strong methods; headroom lives mainly in rare classes.
3. Target circularity: classes were defined by unsupervised clustering of these same methylation
   profiles (paper: reference classes "defined by ... unsupervised clustering"), so the task partly
   recovers clusters from the data that created them; labels are not independent histology.
4. Rare classes: 91 classes, smallest have 8 rows (e.g. plasmacytoma, melanotic schwannoma), so a
   3-fold split leaves ~2-3 test rows per class; per-class metrics are noisy. Stratification is required.
5. Batch confound: material is FFPE 1,878 / Frozen 923 and strongly class-dependent (anaplastic
   pilocytic astrocytoma 21/0, PXA 43/1). Material alone gives only 6% accuracy, so not a leak, but
   models may learn preservation artefacts. Keep it, but note it.
6. Possible near-duplicates/same-patient samples: max inter-sample correlation on subsampled probes
   ~0.96, no exact duplicates found in subsample; GEO does not expose patient IDs, so same-patient
   multi-sample leakage across random folds could not be ruled out.
7. Preparation: types OK (float betas in [0,1], no NaN in subsample - suggests source NaNs were
   imputed or absent; unchecked which). Target and material are categorical. Control-tissue classes
   (e.g. cerebellar hemisphere) are included as classes; acceptable, matches source.

NOT CHECKED: full-feature models, exact duplicates across all 428k columns, patient overlap, how
missing betas/detection p-values were handled, normalization used (raw vs. preprocessed GEO matrix).

</details>

<details><summary>Task gamer: cns_tumor_methylation_classification</summary>

VERDICT: hard to game. The one gain is small: the stratified 3-fold splits let you rebalance the test batch, which lowers log loss by about 8%. No leakage, copies, identifiers or format artefacts.

Setup: top 10,000 probes by variance over all rows were cached (work/prep.py). That is a mild transductive selection; refitting the selection per split was not checked.
Honest baseline (work/base.py): L2 logistic regression (C=0.05) on the top 5,000 probes plus material, standardised on train.
Measured on r0 f0-f2 only (3 of 30 splits; time).
- log loss 0.1170 (0.1205 / 0.1076 / 0.1230).
- Random-column noise: 0.1176 (+0.0006).
- Without material: 0.1174.
- Prior only: 4.19.

| # | Exploit | Script | Honest | Exploited | Gain per split | Deployed has it? | Fix |
| 1 | Rebalance test-batch probabilities (Sinkhorn, 3 iterations) so that the class totals match the train class proportions. The shipped splits are stratified: the test/train count ratio is 0.33-0.67 for every class. | work/transd.py | 0.1170 | 0.1080 | -0.0068 / -0.0100 / -0.0104 | No. It uses the joint composition of the test batch and the stratification; a deployed model scores samples one at a time. | Score per row (already true); accept as minor, or use non-stratified folds. |
| (1b) | The same rebalancing to the true test class counts (an oracle, needs the labels) | work/transd.py | 0.1170 | 0.1053 | -0.010 / -0.012 / -0.014 | No | n/a: upper bound only. |

Attacks that found nothing:
- Row order: class vs position, Kruskal p=0.43. Next-row label agreement 0.025 vs 0.020 expected. The neighbour-row label rule scores 4.57, worse than the prior's 4.19 (work/order.py).
- Copies across the split: no exact duplicates on the top 2,000 probes. Maximum row correlation on the top 5,000 probes is 0.983. Only one pair is above 0.98 (rows 948/1522, same class). Nearest-neighbour label agreement is 96%, but that is legitimate methylation signal.
- Formats: no NaNs, no exact 0 or 1 values, full float precision (15-19 significant decimals) in every row and in both materials. No format feature exists.
- Identifiers: there are none (only probe columns, material and the target).
- Future rows: none apply (IID task, no time column).
- Transforms over all rows: standardising on all rows instead of train gives 0.1174 vs 0.1170, no gain.
- Material (FFPE/Frozen) is an allowed input; dropping it changes nothing.
- Web: no leak or magic-feature threads for GSE90496 / Capper 2018. Looking the GSM samples up in GEO would recover the labels; that is not a task flaw.

Not checked: LightGBM baseline (91 classes x 429k columns is too costly; LR used instead); the other 27 splits; a per-split probe selection; whether hidden replicate or same-patient samples exist beyond correlation 0.98 (GEO does not provide patient IDs here).

</details>

<details><summary>Precedent check: cns_tumor_methylation_classification</summary>

Precedent check: cns_tumor_methylation_classification (2026-11-09)

Verdict: issues 2, 3, 4 and the other calls follow precedent. Issue 1 (keep 91 classes, SEL-4 Must) DEPARTS WITHOUT A
REASON from its batch sibling sarcoma_methylation_classification (merges its 4 clustering-only chondrosarcoma subgroups)
and from the 2026-10-12 retirements (brca_breast_cancer, glioblastoma, ov_ovarian_cancer: clustering-only subtypes).
The register flags nothing for this dataset beyond the size-check line (2026-11-08, AI).

Issue 1, classes drawn by clustering these profiles (SEL-4, USE-5)
  Precedents: brca/glioblastoma/ov retired (Lennart, 2026-10-12, selection.md Cases); sarcoma (TCGA) MFS/UPS merged to
  the source class (Lennart, 2026-10-22); batch sibling sarcoma_methylation issue 1 (merge clustering-only subgroups).
  The builder's separating fact, "clinical use of the classifier", holds equally for sarcoma_methylation (same lab,
  same classifier family), so it does not separate the two. WHO 2021 defining some CNS types by methylation is a real
  separating fact, but only per class: it covers the WHO-named methylation types/subtypes, not every one of the 27
  "WHO subclass" classes. Option B (merge all 27) over-merges WHO-defined types; A keeps clustering-only ones.
  Reflection prompt:
    Which of the 91 classes have a definition outside the clustering of these profiles, and should the rest be merged
    into their entity, as in sarcoma_methylation_classification?
    **Problem:**
    - Sarcoma_methylation merges its clustering-only subgroups; this dataset keeps 27 subclass classes, and both cite the
      same clinical-use reason, so nothing written separates the cases.
    - SEL-4 (Must) retired clustering-only subtypes (brca/glioblastoma/ov, 2026-10-12); a class with no outside
      definition is the same kind of label here.
    | Option | Pro | Con |
    | (a) merge only classes with no definition outside the clustering, in both datasets; a class WHO 2021 names (type or subtype defined by methylation) counts as defined | one test for both; SEL-4 applied class by class like sarcoma | per-class check of the 27 against WHO 2021 CNS5; some relabelling |
    | (b) keep all 91 here and undo sarcoma's merge (keep both as published) | the classifier's own output, clinical label | contradicts 2026-10-12 retirements; separation by construction (linear AUC 1.000) |
    | (c) merge all 27 subclasses into WHO entities (builder's B) | strict, simple | merges methylation-defined WHO 2021 subtypes, losing real diagnostic classes |
    | (d) retire | strictest SEL-4 reading | most classes are WHO entities with outside definitions |
    Recommendation: (a), decided together with sarcoma_methylation issue 1.
    [^1]: SEL-4, USE-5, USE-1
  Note: the domain practitioner (line 26) also reads the labels as partly clustering-defined.

Issue 2, chip batches, IID by patient (SPLIT-29/30): CONSISTENT. Precedents: sarcoma (TCGA, Lennart 2026-10-22/26, IID by
  patient over tissue site, optimism stated). Batch: tcga_pancancer issue 2 (site; holding out costs 35-70% log loss,
  IID kept, cost in splits_comment), treehouse issue 1 (study; donor split, optimism stated), sarcoma_methylation
  issue 3. All four batch cases pick A. This case has the weakest batch signal of the set (chip-mate 0.97 vs 1.00) and
  the same unscoreability (unseen classes in 4 of 6 grouped splits) as treehouse, so A is a stronger fit than tcga's.
  Condition from precedent: state the chip optimism in splits_comment as tcga/sarcoma do; check it is written.

Issue 3, material (LEAK-13/15): CONSISTENT (a feature, not a recording route; no shortcut, 0.64 vs 0.65). Marker: the
  leak_checks.md rule puts `Class-dependent Recording` on every dataset where LEAK-13/15 applied, kept or retired;
  the same gap was found in sarcoma_methylation. A fix, not a decision: add the marker if the record lacks it.
  Not a third exception of the route kind (tcga BCGSC, sarcoma_methylation array type): material is a declared feature.

Issue 4, shared arrays (PROV-7): CONSISTENT, and the counts reconcile: 35 = GSM in GSE90496 shared with sarcoma; sarcoma's
  40 = these 35 + 5 from GSE109379, which this dataset excludes (validation set). Both notes should say so. Decide jointly
  (A in both; no within-dataset leak; B would drop chordoma 9->2, melanoma 12->4).

TP-8 few_minority (12.0% of loss on 5.6% of rows): CONSISTENT with forensic_glass/ljubljana/sarcoma (2026-10-12).
MET-5 fallback log_loss, LEAK-30/31 (per-sample betas, all probes, no supervised selection): CONSISTENT.
Warning acceptance task_stratify_high_cardinality: consistent with class-stratified folds elsewhere.
No drift; no third exception of one kind yet.

</details>
