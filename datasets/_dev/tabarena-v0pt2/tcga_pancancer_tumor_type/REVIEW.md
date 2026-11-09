# tcga_pancancer_tumor_type

**Outcome:** added. The cancer type of a TCGA primary tumour (32 classes: we merged the colon and rectum projects into one colorectal class, issue 2) from its RNA-seq
expression: 9,724 patients x 58,383 genes, raw TPM from the GDC's per-sample STAR-Counts files (Data Release 46.0),
the task of Hoadley et al. (2018, Cell), random folds of patients, fallback log loss. The AI recommends shipping it. No leak,
copy or shortcut was found; the scores are optimistic for a new hospital and lab, because sites, plates and sequencing
centres follow the cancer type. Value: ROC AUC is near 1 for every model, but log loss still separates them (linear 0.11 to 0.17, LightGBM 0.17 to 0.24, random forest 0.35, against 3.24 for the class frequencies). Quality: the source's quality flags drop 404 files, the 2,277 all-zero genes are dropped, and raw TPM ships. Three probe runs on all 58,383 genes did not finish (the hidden-group probe, the task
probe and the full leak probe); 2,000-gene stand-ins and the builder's own site, route and copy tests answer their
questions.

**Main points:** Keep the four classes sequenced only at BCGSC under a written exception, or ship the other 28 types (decide
with `sarcoma_methylation_classification` issue 2); confirm the colon and rectum merge, the patient split with its
stated optimism (decide with `treehouse_pediatric_tumor_type` issue 1 and `cns_tumor_methylation_classification` issue 2), and dropping both quality flags of the source.

**Record judgment:** valid. TCGA's open GDC files with the PanCanAtlas flagship paper; the batch-corrected PanCanAtlas
matrix is avoided. Fit approximate: primary tumours of known type stand in for the metastases of unknown primary the
decision is about. Priority 3: gap +, use case 0, source +, shape +, risk -.

**Issues for Lennart:**

1. **Keep the four cancer types sequenced only at BCGSC?**

   * **Problem:**
     - Every oesophageal, stomach, ovarian and leukaemia tumour (about 1,130 rows) was sequenced at BCGSC, and no tumour of another type was.
     - The sequencing route shows in the profile: the two glioblastoma routes separate at ROC AUC 0.999 (0.994 on the small non-polyadenylated RNAs alone).
     - No test can tell route from tumour for these four, since no other type went through BCGSC, and the source's own fix, a batch correction (EB++) fitted on all samples at once, would let test rows shape the training data, so it is not used[^r1].
   * **Effect on the task:** the score may partly reward recognising the route on the hardest neighbours (stomach against colorectal, ovarian against endometrial, oesophageal against head-and-neck and lung squamous); the size is unmeasured[^r1].
   * **Experiments:** for the glioblastomas, where both routes exist, the test passes as shipped: none of the 7 total-RNA tumours of other types is called glioblastoma (probability at most 0.024). The 28 types sequenced only at UNC (counted before the colon and rectum merge) already reach macro ROC AUC 0.999 among themselves.
   * **Unknown:** what would settle it is tumours of these four types sequenced on another route, for example at UNC or re-sequenced by the GDC; none exist in this source.
   * **Consistency:** `prostate_cancer_detection` was retired for a recording artefact that could not be undone[^p1]; keeping the four classes departs from it unless the exception names the fact that sets this case apart (the classes differ by tissue biology, the route marks the whole class). `sarcoma_methylation_classification` issue 2 (array type, 31 of 63 classes on one array) is the same kind of call: decide the two alike; a third such exception should prompt a rule amendment.
   * **Panel:** the advocate keeps the classes (the route cannot be what makes them easy; removing 4 real classes for an unmeasured effect is a loss); the critic and the precedent checker say "untestable" is no distinguishing fact; the domain practitioner trusts this gap least; the mediator hands it over as a weighing call, both options ship.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep with a written exception (implemented) | the route note in the curation comments; the `Class-dependent Recording` marker on the record; the exception, naming tissue biology as the fact that sets the case apart, is written into the record when A is confirmed (not written yet) | keeps 4 real, clinically important classes; the 28-type result shows the task is easy without the route | a departure from the retire precedent; route memory unmeasured |
     | B | Ship 28 types | drop the oesophageal, stomach, ovarian and leukaemia tumours | no class tied to its own sequencing centre | about 1,130 rows and 4 classes lost; stomach and ovarian cancers of unknown primary are common |

   * **Recommendation:** A, with the exception written, decided together with `sarcoma_methylation_classification` issue 2. **Decision:** A or B?

   **Notes for the AI:** on A, write the exception into the record's comments (the fact: the four classes are separated from their neighbours by tissue biology, the route marks whole classes and cannot be measured; revisit when the GDC releases the same tumours from another centre). On B, filter `files["project"]` to drop ESCA, STAD, OV and LAML in `selected_files`, update `task_summary` (28 classes), the route bullet and decision 3, re-run `dataset check` and the task probe; remove the marker. The centre table (the third decision table of the definition) lists the classes too, so update it.

   [^p1]: Precedent: `prostate_cancer_detection`, retired under the rule on recording artefacts that cannot be undone.
   [^r1]: **LEAK-13** (Must): class-specific recording conventions are harmonised; first measure how much the fix removes. **LEAK-15** (Must): a recording artefact that runs through several features that matter in practice, and that cannot be undone, retires the dataset. **LEAK-39** (Must): rows of one class recorded through a separate route are dropped when models recognise them and the route cannot be aligned. **LEAK-30** (Must): no step fitted on all rows, test rows included, shapes the features.

2. **Merge colon and rectum adenocarcinoma into one colorectal class?**

   * **Problem:**
     - Colon and rectum are told apart mostly by the hospital site: pair ROC AUC 0.78 with random patients, 0.58 with sites held out.
     - The 6% of rows of these two classes carried 23 to 30% of a linear model's log loss.
     - TCGA studied them as one colorectal cancer, the source groups them as COAD/READ, and a cancer of unknown primary with a colorectal profile is treated as colorectal.
   * **Effect on the task:** merged, a linear model's log loss falls from 0.144 to 0.112; the task loses a distinction that rests on site rather than tumour.
   * **Experiments:** linear model on 100 principal components of 2,000 genes, 3 folds, with random and site-held-out folds; the merged figure (0.112) is from the same model with colon and rectum as one class.
   * **Consistency:** follows the `sarcoma_methylation_classification` merge of myxofibrosarcoma and undifferentiated pleomorphic sarcoma (Lennart, 2026-10-22)[^c1]; `treehouse_pediatric_tumor_type` issue 3 (AMKL) is not bound by it, since the source does not group that pair.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | 33 TCGA projects | colon and rectum as two classes | the project as enrolled | a site distinction scored as a tumour one |
     | B | Merge into colorectal (implemented) | 32 classes, "Colorectal Adenocarcinoma" | the convention of TCGA and the source; the class the clinician acts on | none found |

   * **Recommendation:** B. **Decision:** A or B?

   **Notes for the AI:** on A, map the target with `PROJECT_NAMES` instead of `CANCER_TYPES` and restore the 33-class texts.

   [^c1]: **TP-7** (Must): when the definition builds the target itself, use an established convention and test each candidate. **USE-5** (Must): predict what the actor would act on, at the resolution they act on it.

3. **Split by patient, with the optimism stated?**

   * **Problem:**
     - Each of the 695 tissue source sites sent one cancer type, and the site shows in the profile (two sites of one type apart at median ROC AUC 0.73).
     - Holding out whole sites raises a linear model's log loss from 0.144 to 0.195 and from 0.137 to 0.233 (two seeds).
     - A split by site is unworkable: one site holds the whole leukaemia class and 71 of the 78 adrenocortical carcinomas.
   * **Effect on the task:** models are ranked on new patients of known sites; the scores are optimistic for a lab whose samples come from hospitals not in the training data, as the splits comment states.
   * **Consistency:** as `sarcoma_methylation_classification` (2026-10-22); the same call is open as `treehouse_pediatric_tumor_type` issue 1 and `cns_tumor_methylation_classification` issue 2: decide the three alike[^s1].
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | IID by patient (implemented) | 3 x 3 folds stratified on the type; the site and plate costs in the splits comment | every class trained and tested; matches the sarcoma call | optimistic for a new hospital |
     | B | Grouped by site | hold out whole sites, the leukaemia split by patient | stands for a new hospital | the leukaemia (one site) still has to be split by patient; a fold trains on 7 of the 78 adrenocortical carcinomas |

   * **Recommendation:** A. **Decision:** A or B?

   **Notes for the AI:** on B, a site group column from the aliquot barcode (characters 6-7), kept as the group and never as a feature; re-run the group and task probes.

   [^s1]: **SPLIT-29** (Must): an IID split is wrong when many rows share an entity that new data would not have and the entity carries the label. **SPLIT-30** (Must): re-split only when the context says the rows share an entity new data would not have, or the evidence is very strong.

4. **Drop the samples both quality flags of the source exclude?**

   * **Problem:**
     - The PanCanAtlas marks 183 primary files `Do_not_use` and its working groups' pathology review excluded 221 more (73 prostate samples with degraded RNA, 39 lung tumours without a clear histology, sarcomas of another type).
     - Their label or their RNA is in doubt by the source's own review.
   * **Effect on the task:** 398 patients leave; the shipped labels are the ones the source trusted.
   * **Consistency:** follows using a source's own list of bad rows[^q1].
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Drop both flags (implemented) | 404 files out | labels and RNA the source trusts | 398 fewer patients |
     | B | Drop only `Do_not_use` | keeps the 221 pathology exclusions | more rows | labels in doubt by the source's review |

   * **Recommendation:** A. **Decision:** A or B?

   [^q1]: **CLEAN-1** (Should): clean to the state an expert would ship, adopting the data owners' published list of bad rows. **CLEAN-11** (Should): a row leaves only when it is no task row or a copy.

**Review panel:** ship after changes (mediator). Full panel; the rebuttal round was skipped because the advocate's and the critic's briefs converged. Claim audit: no validity claim refuted; the plate batch measured (as strong as the site batch) and two counts corrected. Column audit: no column leak; the route lives in the non-polyadenylated gene types (noted). Split audit: right with notes (patient split, optimism stated). Task gamer: no exploit beats noise. Blind review: would benchmark; asks for fewer genes and a log, kept raw by the lossless rule. Applied with no decision: the plate sentence, GDC Data Release 46.0 and Hoadley et al. 2018 cited, the primary-only filter, 284 glioblastomas, the route note, the top-1/top-3 note, raw TPM kept; the colon and rectum merge (issue 2) implemented. Not finished: the hidden-group, task and full-width leak probes. Disputed and handed over: the four BCGSC classes (issue 1). The builder's draft, which the advocate, critic, split audit, column audit and precedent check answer, numbered the issues differently: its issue 2 (site split) is issue 3 here, and its issue 3 (colon and rectum) is issue 2 here. The mediator's 'about 1,400 rows' for the BCGSC classes is 1,123 (173 + 388 + 411 + 151, dataset.py).

<details><summary>Mediator: tcga_pancancer_tumor_type</summary>

```text
Mediator report for tcga_pancancer_tumor_type (2026-11-09)


SUMMARY (15 lines max)
1. Ship after changes. Advocate and critic agree on everything except one point, which goes to the curator.
2. No leak, copy or shortcut was found. One row per patient (9,724), 0 exact copies, best single gene AUC 0.67-0.69, the gamer's gain is within noise.
3. Changes needing no decision: the plate sentence, saying the probes never finished, citing GDC DR 46.0 STAR TPM with Hoadley 2018 as the task's reference, the primary-only filter, GBM 284, 695 sites, a top-1/top-3 note, and the column auditor's route note.
4. Issues the panel agrees on, which the curator confirms: merge COAD/READ (B), keep IID by patient (A), drop both pathology flags (A), keep raw TPM (CLEAN-22).
5. Open: the four BCGSC classes (ESCA, STAD, OV, LAML). Either (a) keep them with a written exception and the marker, or (b) ship the other 29 types. Decide together with sarcoma_methylation_classification issue 2.
6. Precedent: COAD/READ, IID and the flags follow precedent. The BCGSC classes depart from LEAK-15 (prostate_cancer_detection) unless the exception names its distinguishing fact.

JUDGMENT RECORD
Verdict: ship after changes. The open BCGSC-route issue does not block shipping, because both options ship.
Validity: SEL-1/2 hold. USE-1 holds with an approximate fit (primaries stand in for metastases, USE-8, as in ljubljana_primary_tumor). LEAK-16..21 and LEAK-27..31 hold (per-sample TPM rather than the EB++ matrix; PROV-13). LEAK-17 holds. LEAK-39 holds for GBM. LEAK-13/15 triggered for the BCGSC classes, which is the open issue. SPLIT-29/30 triggered, and IID is kept with its cost stated (sarcoma precedent). USE-5/TP-7 triggered: merging COAD/READ fixes it.
Value: macro AUC is saturated (0.999), but log loss spreads models: linear 0.11-0.17, LightGBM 0.17-0.24, RF 0.35, against a prior of 3.24 (TP-1..8, MET-11). Smallest class is 34, about 11 per test fold (MET-2).
Quality: CLEAN-1/11 (both source flags dropped), CLEAN-5 (2,277 all-zero genes dropped), CLEAN-22 (raw TPM, all genes kept).
Weighed: gap + (wide multiclass), source + (TCGA/GDC, Cell 2018), shape + (9.7k x 58k), risk - (site, plate and route batches).
For the curator: issue 1, a weighing call. Keep the 4 BCGSC classes under a written exception, or ship 29 types. Decide jointly with sarcoma_methylation issue 2.

CHANGES TO MAKE NOW (no decision needed)
1. Add the plate batch sentence to the site bullet and splits_comment: 247 plates, 145 single-type, holding 4,795 rows (49%). ACC, CHOL, UCS and UVM each sit on one plate. Plates of one type at one site are separable at median AUC 0.77 (LAML 0.996). No split change. Rule: LEAK-13, SPLIT-29 (state the cost).
2. Tell the curator, in REVIEW.md or the notes, that hidden_groups.py, task_probes.py and the full-width leak_probes.py never finished. The evidence is the builder's 2,000-gene stand-ins (site-held-out runs, task_quick, leak_quick). Rule: EV-3.
3. Provenance: cite GDC Data Release 46.0, STAR-Counts tpm_unstranded (GENCODE v36), as the data source, and Hoadley et al. 2018 as the source of the 33-type task. Rule: PROV-8/9/10 (PROV-10 is a Must).
4. Document the primary-only sample filter, and say it explains SKCM's 103 rows. Rule: PROV-10, writing.
5. GBM has 284 rows: 155 Broad, 128 total-RNA, 1 from centre 53. Fix "283". Fix claims.md T3 to 695 sites (it says 703). Rule: writing.
6. Add to the route note that the route lives in the non-polyA gene types. Small RNAs alone tell the two GBM routes apart at AUC 0.994, and histones alone at 0.998. Rule: LEAK-13/39.
7. Metric note: the field reports top-1/top-3 accuracy, and log loss stays the metric. Rule: MET-8.
8. Keep raw TPM with all genes. The blind reviewer's request to drop near-zero genes and apply log1p is a P7 preference against the lossless rule, so no change. Rule: CLEAN-22, dtypes-from-context.

ISSUES FOR THE CURATOR (ranked)
1. [Validity, P4, Must] BCGSC sequencing route holds four whole classes (ESCA, STAD, OV, LAML, about 1,400 rows).
   - Problem: every row of these classes was sequenced at BCGSC, and no other class was. The route is visible in the profile: the two GBM routes separate at AUC 0.994-0.999, and LAML plates at 0.996. LEAK-39's test cannot run without rows of another class on the same route. The source's own fix (EB++ over all samples) is barred by LEAK-30.
   - Effect: the score may reward route memory on the hardest differentials, STAD vs COAD/READ and OV vs UCEC. The size of this effect is unmeasured.
   - Advocate: the 28 UNC-only types already reach macro AUC 0.999. The confusers differ by tissue biology, so the route cannot be what makes these classes easy. Removing 4 real classes for an unmeasured effect is a loss.
   - Critic and precedent checker: "untestable" is not a fact that sets the case apart. prostate_cancer_detection was retired under LEAK-15. The domain practitioner trusts this gap least.
   - Not a conflict between rules: LEAK-13/15 each have to hold on their own. Remedy ladder: (a) state the exception with its fact, plus the Class-dependent Recording marker and the non-polyA note; then (b) remove the affected classes. (c) Retire is not needed, because (b) already removes the artefact.
   - Rule: LEAK-13, LEAK-15, LEAK-39 (Must).
   - Decision: (a) or (b). Decide together with sarcoma_methylation_classification issue 2 (array type, AUC 1.00, 31 of 63 classes on one array). Taking (a) in both datasets makes two exceptions of one kind. A third should prompt an amendment to LEAK-15 or LEAK-39.
   - What would settle it: a test of route against type, for example STAD/ESCA rows sequenced at UNC or GDC re-sequenced rows of these classes on another route. None exists in this source.

2. [Validity, P3/P4, USE-5/TP-7, Must] Merge COAD and READ into one colorectal class (option B). All agents agree. The curator confirms.
   - Evidence: pair AUC 0.78 IID, 0.58 with sites held out. 6.1% of rows carry 22.6-30.1% of the log loss. Merged log loss drops from 0.144 to 0.112. TCGA and Hoadley group COAD/READ, and clinicians act on "colorectal".
   - Precedent: sarcoma MFS/UPS merge (Lennart, 2026-10-22).

3. [Validity, P4, SPLIT-29/30/31, Must] Keep IID by patient (option A). All agree. The curator confirms, together with treehouse issue 1 and cns issue 2.
   - Evidence: 695 sites, none with two types. Holding sites out raises log loss by 35-70%, and this cost is stated in splits_comment.
   - A site split is unworkable: LAML comes 100% from one site and ACC 71 of 78 from one.
   - Precedent: sarcoma (2026-10-22).

4. [Quality, P7, CLEAN-1/11] Drop both source quality flags (option A, 183 Do_not_use + 221 pathology). All agree. The curator confirms.

TASK GAMER EXPLOITS, mapped
- Per-sample format features (smallest non-zero TPM, count of zero genes) improve LightGBM log loss by 0.004 and LR by 0.0005. A random column gains 0.003, so this is noise. It maps to LEAK-13 (recording mark) but is not one: a deployed model has these values from the profile too. It is a new finding with no gain. Not an issue, no note needed.
- The gamer could not test site, plate or route because the kit carries no barcodes. Those are covered by issue 1, the existing site bullet and change 1. The definition's `Potential leak, kept on purpose` note covers the route. The other auditors' measured gains match the stated note: GBM test passed, BCGSC unmeasured.

AGREED FACTS
- Source: 10,308 primary files from GDC DR 46.0, STAR TPM. After the flags and one row per patient: 9,724 rows x 58,383 genes, 33 classes (BRCA 1,084 down to CHOL 34). 0 exact copies; nearest-neighbour correlation at most 0.985.
- Sites: 695 sites, each with exactly one type. LAML comes from 1 site, and ACC 71 of 78 from one. 247 plates, 145 single-type, holding 49% of the rows.
- Route: ESCA, STAD, OV and LAML only at BCGSC. GBM: Broad 155, total-RNA 128, other 1. 7 total-RNA rows of other types, and none is called GBM (max P 0.024).
- Scores: linear macro AUC 0.998-0.999. Log loss: linear 0.11-0.17, LightGBM 0.17-0.24, RF 0.35, prior 3.24. Best single gene AUC 0.67-0.69, depth-3 tree 0.65.
- Site-held-out costs: log loss 0.144 to 0.195 and 0.137 to 0.233 (two seeds). COAD/READ pair AUC 0.78 to 0.58.
- Probes not finished: hidden_groups.py and the full-width task and leak probes.

CONSISTENCY WITH PRECEDENT
- Consistent: COAD/READ merge (sarcoma MFS/UPS), IID with stated cost (sarcoma; aligned with treehouse issue 1 and cns issue 2), GBM route (LEAK-39, gallstone_disease), flags dropped, EB++ avoided (PROV-13), primaries for CUP (ljubljana_primary_tumor), fallback log loss.
- The treehouse AMKL decision is not bound by the COAD/READ merge: AMKL is a WHO entity, not a pair the source groups.
- Departure: keeping the BCGSC classes departs from prostate_cancer_detection (LEAK-15). It needs the distinguishing fact written, the tissue-biology argument, accepted by the curator. Otherwise it becomes option B. Hence issue 1.
```

</details>

<details><summary>Claim audit: tcga_pancancer_tumor_type</summary>

```text
Claim auditor report: tcga_pancancer_tumor_type (2026-11-09)
Data: builder's cached diag_frame.parquet / diag_meta.parquet (9,724 shipped rows), primary_meta.parquet. No container built.
Scratch: the run folder

Verdict: no validity claim refuted; one untested batch claim (plate, R7) now measured and as strong as the site batch;
two small factual slips in the notes/claims list.

Table (claim | source | test | result | evidence | rule)
T3/C23 703 sites | claims.md T3 | count TSS on shipped rows | REFUTED in claims.md, holds in dataset.py | 695 sites in the shipped rows (703 among the 10,308 primary files); task_summary and splits_comment say 695, correct | writing
T6/C23 one type per site | task_summary, splits_comment | groupby site nunique(project) | holds | 0 of 695 sites with >1 type | SPLIT-29
LAML one site, ACC 71/78 in one site | splits_comment | value_counts | holds | LAML: AB 151; ACC: OR 71, PK 4, OU 1 | SPLIT-30
C18 route counts | curation_comments | crosstab project x centre code | holds, one omission | ESCA 31:173; STAD 13:198+31:190=388; OV 402+9=411 BCGSC +5 code-41; LAML 13:151; GBM 01:155, 41:128, and 1 GBM row centre 53 ("other") not mentioned (283 vs 284 GBM) | LEAK-13
C21 7 total-RNA rows of other types | curation_comments | crosstab | holds | code 41: OV 5, LUAD 1, LUSC 1 | LEAK-39
S1/LEAK-17 one row per patient | splits_comment | patient.is_unique | holds | 9,724 unique patients | LEAK-17
C16 class counts | curation_comments | value_counts | holds | CHOL 34, DLBC 48, UCS 57, KICH 65, ACC 78, UVM 80 | TP-8
R7 plate nearly coincides with type | record | plates per type; within one site AND one type, tell two plates (>=20 rows each) apart, logistic regression on PCA(20) of 2,000 most variable log1p genes, 3-fold AUC | was untested -> CONFIRMED as a second batch | 247 plates, 145 single-type, holding 4,795 rows (49%); ACC, CHOL, UCS, UVM each on 1 plate; within-site-and-type plate AUC 0.65-1.00, median 0.77 over 8 pairs (LAML AB 0734 vs 0736: 0.996; GBM 06 1849 vs A96S 1.000 is the route; COAD AA 0.83, KIRC BP 0.78, OV 13 0.76) | LEAK-13, SPLIT-29
M1 fallback log_loss | metric reason | re-read of record + builder's paper reading; no further source search done | holds (not re-fetched) | Hoadley 2018 is a clustering paper; no classifier metric | MET-1, MET-5
M2/MET-2 computable | metric | 33 classes, smallest 34 -> ~11 per test fold of 3 | holds | every class in every stratified test fold | MET-2
R8 sex | record | not tested (no clinical column; expression sex is legitimately known) | untested, not a leak | - | USE-3

Ranked refuted / untested
1. (Should, LEAK-13/SPLIT-29) Plate batch not stated: plates are within-site-and-type separable (median AUC 0.77, LAML 0.996) and half the rows sit on single-type plates, four small classes on one plate. It is nested in the site batch the notes already declare and the IID split keeps plates across train/test like sites. Mildest remedy: add one sentence to the site bullet / splits_comment ("plates, like sites, are single-type for 49% of rows and visible in the profile"); no split change (a plate split inherits the site split's LAML/ACC problem).
2. (Could, writing) GBM has 284 rows: 155 Broad + 128 total-RNA + 1 other-centre (code 53). Remedy: say "155 Broad, 128 re-sequenced, 1 other" or note it in the route bullet; the decision table already shows it.
3. (Could, claims list only) claims.md T3 says 703 sites; the shipped count is 695 (the definition is right). Fix the claims list.
Not refuted: one type per site, LAML/ACC site concentration, route counts, one row per patient, class counts, fallback metric, foldwise computability.
```

</details>

<details><summary>Column audit: tcga_pancancer_tumor_type</summary>

```text
Column auditor: tcga_pancancer_tumor_type (2026-11-09)
Verdict: no column leak and no cleaning problem; one note to add to issue 1 (route), one question for the curator.

Prediction point (first curation bullet): a tumour sample has been RNA-sequenced; expression only, no clinical field.

Column table (58,383 features, grouped by GENCODE v36 gene_type; every column has the same provenance)
column | meaning | known at prediction? | dtype and cleaning | verdict | rule
protein_coding genes (19,962 in source) | TPM (tpm_unstranded) of the gene in the sample | yes, measured on the sample | float64, not logged, sums to 1e6 per row (per-sample scale) | fine | LEAK-30 n/a, CLEAN-8
lncRNA, pseudogenes, TEC, IG/TR genes | same | yes | float64; IG/TR genes carry immune infiltration (biology) | fine | -
Y-chromosome / XIST genes | sex of patient through expression | yes (sex is known at prediction; drives PRAD/OV/UCEC/UCS/CESC/TGCT) | float64; 44 PAR_Y copies were all-zero and dropped | fine (biology, not a recording mark) | USE-3, LEAK-10
small non-polyA RNAs (snRNA, snoRNA, misc_RNA, miRNA, scaRNA, Mt_tRNA, rRNA..., 6,143 shipped) and replication histones (130) | TPM of short or non-polyadenylated RNAs that poly-A libraries capture badly | yes | float64; measured mostly as library-protocol noise | fine, but the route's carrier (see 1) | LEAK-13/39
2,277 all-zero genes | - | - | dropped (constant over shipped rows; a train-only fit would also see zero) | fine | CLEAN-5
cancer_type (target) | TCGA project, GDC name, 33 classes | label | string/category, no missing | fine | -
Dropped/not shipped: file_id, aliquot barcode, site, plate, centre, sex, age: none shipped, correct (the barcode would encode site and centre).
dtype probe: 0 of 58,383 flagged; no ordinal, no codes, no proxy missing (TPM 0 is a real zero), no impossible values (finite, >= 0, asserted).

Problems ranked (principles.md)
1. P4, LEAK-13/39, strength: medium, evidence (own, work_column_auditor, 3-fold logistic on log1p):
   within GBM the 2024 total-RNA route vs Broad is told apart at ROC AUC 0.994 from the 6,143 small-RNA genes alone and
   0.998 from the 130 histone genes alone; these RNAs are not polyadenylated, so their level is a library mark more than
   biology. Small RNAs alone also give macro AUC 0.997 for the 33 classes (host-gene read-through carries type signal
   too), so dropping them would not remove the route and would not cost much signal either.
   Mildest remedy: none in the code; add to the issue-1 note that the route lives in the non-polyA gene types (a
   reviewer testing option B or a future fix knows where to look). Option to offer the curator: drop the small RNA
   gene types as unreliably measured under poly-A capture (CLEAN by meaning), not required.
2. Question for the curator (P7, CLEAN-22): ship 58,383 TPM columns raw (current) vs the source's habit of log2(x+1).
   Raw is lossless and consistent with "as published"; keep, no change.
No other finding: no post-outcome column, no id, no missingness caused by the outcome, no column copying the label.
Builder's issues 1-4: agree with A for 1, 2, 4; colon/rectum (3) is a target question, outside the column audit.
```

</details>

<details><summary>Split audit: tcga_pancancer_tumor_type</summary>

```text
Split auditor: tcga_pancancer_tumor_type (2026-11-09)

VERDICT: right with notes.

Regime. The use case is a lab typing a new patient's tumour (CUP). Patients do not recur (one row per patient,
checked: 9,724 unique patients in diag_meta.parquet), there is no time axis and no label delay (the label is the
enrolment project, fixed), so temporal checks do not apply. The declared IID over patients, stratified on the type,
3 x 3 (train 6,482-6,483 / test 3,241-3,242), matches the patient as the unit of one prediction.

Hidden groups (numbers re-checked on diag_meta.parquet, 9,724 rows):
- Tissue source site: 695 sites, 0 of them with more than one type; median 5 rows per site, 159 single-row sites.
  LAML 100% one site, ACC 91% one site, TGCT 53%, CHOL 50%, SARC 49%, READ 46%.
- Plate: 247 plates, 102 mix types; 4,795 rows sit on single-type plates (a second, weaker batch mark).
- probes/hidden/ does not exist: hidden_groups.py never finished, so no official hidden-group reading. The builder's
  own site-held-out runs stand in (probes/diag_sites.json).

Alternative split (builder's run, read and accepted, not re-fit: the numbers are consistent and the frame is the
shipped 9,724 rows). Linear PCA(100) log loss IID 0.144 -> site-held-out 0.195 (seed 0), 0.137 -> 0.233 (seed 1);
accuracy drop under 2.2 points; READ per-class log loss 1.16 -> 2.95, UVM 0.008 -> 0.376, TGCT 0.03 -> 0.11;
colon vs rectum pair AUC 0.78 -> 0.58; 1-NN shares the site in 22.6% of same-class pairs vs 14.1% at random.

Findings, ranked (principles.md):
1. P4, SPLIT-29/30 (concern, kept): a new lab's samples come from a hospital not in training, which the IID
   split does not mirror; the score is optimistic by 35-70% in log loss and the ordering of models may change on
   site-sensitive pairs (COAD/READ). The cost is stated in splits_comment with numbers, and a site split is
   infeasible for LAML (1 site) and ACC (71/78 in one site). Mildest remedy: none to the split; keep IID as in the
   sarcoma precedent. If the curator wants a grouped variant: StratifiedGroupKFold on site with LAML (and ACC's big
   site) split by patient, as the builder's diagnostic did. Issue 3 (merge COAD+READ) removes most of the
   site-driven loss and is the cheaper fix for the gap (merged linear log loss 0.144 -> 0.112).
2. P4, LEAK-39 interaction with the split (note): the sequencing route (BCGSC for ESCA/STAD/OV/LAML) is a class-
   level batch, not a group a split can hold out; no split remedy exists, it stays a builder issue 1 matter.
3. Process (note): the hidden_groups probe output is missing; the panel relies on the builder's own site probe.
   Remedy: let the curator know the official probe did not finish, or re-run on the 2,000-gene frame.

Builder's draft issues weighed: issue 2 (site split) -> agree with A (IID with the stated cost); issue 3 -> support B
from the split side (it shrinks the IID-vs-site gap).
```

</details>

<details><summary>Domain practitioner: tcga_pancancer_tumor_type</summary>

```text
Domain practitioner report: tcga_pancancer_tumor_type
Actor: a molecular pathologist / oncologist with a cancer of unknown primary (CUP), ordering a tissue-of-origin
expression test (as CancerTYPE ID, Tempus/Caris-style RNA classifiers, OncoNPC, TOAD-style tools).

VERDICT: fit APPROXIMATE (as declared). Reason: the inputs are what I have (one RNA profile of the biopsy), but the
rows are well-sampled primary tumours of known type at their organ of origin, while my sample is a metastasis in
liver, lymph node, lung or peritoneum, diluted by host tissue. Metric: PARTLY scores my decision.

1. Inputs at the moment of prediction (USE-3)
- Have: the biopsy's RNA-seq expression. Yes.
- Would also always have, and missing: sex (narrows to/away from OV, UCEC, CESC, PRAD, TGCT, BRCA largely), age,
  and the BIOPSY SITE (the organ the metastasis was sampled from). Every clinical CUP classifier conditions on the
  biopsy site, since host-tissue signal otherwise dominates. Excluding them is defensible here (expression carries
  sex; biopsy site is meaningless for primaries), but it means the task is "organ of origin of a primary", not CUP.
- Would not have: nothing in the features is post hoc. No leak in availability terms.

2. Target (USE-5)
- I act on the treatment-relevant tumour type. TCGA projects are close but a proxy: COAD vs READ is one decision
  (colorectal regimen), so the 33-class target splits a class I do not distinguish; the builder's issue 3 (merge
  to colorectal) matches practice -- I support option B. LUAD/LUSC, KIRC/KIRP/KICH and LGG/GBM are distinctions I
  do care about (different therapy), keep them. ESCA mixing adeno and squamous is a coarser-than-useful class but
  shipped as the source defines it; acceptable.
- I want a probability over types (reports give a ranked list with scores, top-1 plus differential). A class alone
  is not enough.

3. Row vs decision, test data
- One row = one tumour = one decision: matches (one per patient, good).
- Test data is NOT what I face, ranked by impact:
  (a) Primaries vs metastases: the biggest gap; published classifiers lose ~5-15 points of top-1 accuracy going
      from primaries to metastases (e.g. TCGA-trained models on MET500 / CUP cohorts). Not fixable in this source
      (metastases are 394 files, mostly SKCM).
  (b) Site / centre batch: my lab and hospital are new. The IID split rewards site and sequencing-route marks;
      builder measured log loss +35-70% with sites held out. I accept IID only because a site split would empty
      LAML/ACC (issue 2, option A acceptable with the stated cost). An expert would prefer site-grouped folds.
  (c) Sequencing route by class (BCGSC for ESCA/STAD/OV/LAML, two GBM routes): a real lab never has route
      correlated with label. Issue 1: option A is acceptable only with the marker; this is the gap I trust least,
      because STAD vs COAD/READ and OV vs UCEC are exactly my hardest clinical differentials.
  (d) Class mix: TCGA frequencies (BRCA 11%) do not match CUP's true primaries (pancreas, lung, biliary, upper GI
      dominate); CHOL with 34 rows is a common true CUP origin. Prior shift; matters for log loss calibration.
- Issue 4 (pathology exclusions, option A): agree; uncertain labels and degraded RNA are not what a validated
  reference set contains.

4. Would I use it?
- As a research benchmark of organ-of-origin classifiers, yes; as a model to deploy, only after validation on
  metastases from my own lab. I would trust it if top-3 accuracy held on site-held-out and metastatic data; I
  distrust near-perfect IID scores (macro AUC 0.999) as partly batch and site memory.

5. Metric (MET-1, MET-6 to MET-9, MET-11)
- log_loss (fallback) is a proper rule over the full probability vector, at the right unit (a tumour). It ranks
  models by calibrated probabilities, which matters since I read the score next to histology/IHC. So it is
  defensible, and much better than macro AUC (saturated).
- But my decision is "which 1-3 types do I work up / treat as": the field reports top-1 and top-3 accuracy
  (commercial tests and TOAD/OncoNPC papers). Log loss is dominated by the hardest pairs (COAD/READ carry 23-30% of
  it with a distinction I do not act on: MET-8, scoring a decision not taken). I would pick a model by log loss
  only after the colorectal merge; otherwise I would add top-3 accuracy as the reported secondary. Verdict: PARTLY.

What an expert would change (ranked): merge COAD+READ; prefer site-grouped evaluation where classes allow, or at
least report it; flag the BCGSC/GBM route issue prominently; note that the real deployment population is
metastases with host-tissue admixture; report top-k accuracy alongside log loss.

Sources: dataset.py task_summary, curation_comments, splits_comment; README; builder_report.md issues 1-4 and
probes (diag_sites, diag_coadread); record. Domain knowledge: Hoadley et al. 2018 Cell (Discussion, CUP use);
CUP classifier literature (Lu et al. 2021 Nature TOAD; Moon et al. 2023 Nat Med OncoNPC; Zhao et al. 2020 JAMA
Netw Open TCGA-trained RNA classifier on metastases; bioTheranostics CancerTYPE ID 92-gene assay reporting top
type and differential). Web not re-queried in this run.
```

</details>

<details><summary>Blind review: tcga_pancancer_tumor_type</summary>

```text
VERDICT: Include with changes. It is real, honest data, but at 58,383 columns and ~95% accuracy from a 500-gene linear model it mostly tests whether a method can handle a very wide table, not whether it predicts well.

TASK: Predict which of 33 TCGA cancer types a tumor is, from its bulk RNA-seq expression (9,724 tumors x 58,383 genes; values are TPM, every row sums to 1e6). This has real uses, such as finding the tissue of origin for cancers of unknown primary or checking sample identity, but in practice those tools are trained across cohorts, not on a random split of a single study.

CONCERNS (most to least serious):
1. Near-saturated, so methods are hard to tell apart. A logistic regression on the 500 highest-variance log1p genes (3-fold CV) scored 0.946/0.956/0.952 accuracy. A 1-nearest-neighbour on correlation got the label right for 92%. Published pan-cancer classifiers report about 95-97%. The remaining errors are mostly biologically ambiguous pairs (READ vs COAD, ESCA vs STAD, LUAD vs LUSC, LGG vs GBM), where the label is partly convention. Change: score with log-loss or balanced accuracy, or merge the indistinguishable pairs, so that differences are not noise.
2. Width is extreme. There are 58,383 float columns, including many lncRNA/pseudogene features with median 0 (e.g. AP001541.1 has 75th percentile 0). Many tabular methods (TabPFN-style, GBDT with tuning, kNN) will fail or be dominated by runtime. Change: drop near-zero-expression genes and keep about 5-20k protein-coding genes (or the top-variance ones), and store log1p(TPM).
3. Preparation and provenance do not match the source. Ensembl IDs up to ENSG000002886xx and TPM normalization point to the current GDC harmonized STAR pipeline (GENCODE v36), not the PanCanAtlas EBPlusPlus matrix in the cited Cell 2018 paper. The cited source should name the actual GDC release and file type.
4. Possible repeated patients and the filters used are unknown. There are no sample or patient IDs. I found no exact duplicate rows and no pair of rows with correlation above 0.99 (max nearest-neighbour r is about 0.98), so copies are unlikely. But I cannot confirm one primary tumor per patient. SKCM has only 103 rows (TCGA has about 470, mostly metastatic), which suggests a primary-only filter that is not documented. Change: document the sample-type filter and keep one aliquot per patient; consider grouping or site-aware splits (tissue source site batch effects are known in TCGA).
5. Class imbalance: classes range from 1,084 (BRCA) down to 34 (CHOL). With 3 folds that leaves about 11 CHOL tumors per test fold. This is acceptable with stratified folds.
6. Types are fine: 58,383 float64 columns and a categorical target, no missing values, no all-zero columns.

COULD NOT CHECK: patient/aliquot identity, the exact GDC release, the sample-type filter, and batch or site structure (there are no metadata columns). I did not run GBDT on the full width because of the runtime.
```

</details>

<details><summary>Task gamer: tcga_pancancer_tumor_type</summary>

```text
TCGA pan-cancer tumour type: task gamer report
Verdict: no exploit beats noise; the task is close to ungameable (plain GDC TPM for 58,383 genes, random row order, no duplicate samples, no columns other than genes).

Models use log1p of the 2,000 highest-variance genes (not all 58k, for run time).
The gene selection used variance over all rows (test values, not labels): negligible.
Scripts: work/prep.py, work/explore.py, work/base.py; outputs: work/out_*.txt.

Honest baseline (log loss, mean of the 9 shipped splits; class-prior entropy 3.240):
- LightGBM (300 trees, 15 leaves, colsample 0.3): 0.1885 (range 0.169-0.210)
- Logistic regression (C=0.05, standardised): 0.1137 (range 0.106-0.123), the stronger honest model

Exploits ranked by gain:
1. Per-sample format features: smallest non-zero TPM (depth/batch proxy) and count of zero genes.
   LGB 0.1885 -> 0.1841 (gain 0.004, per split +0.002 to -0.012); LR 0.1137 -> 0.1132 (gain 0.0005).
   Alone: 3.08 against the 3.24 prior. Noise check: a random column gives LGB 0.1856 (gain 0.003).
   Within noise, and a deployed model has these from the profile itself. Fix: none needed.

Flaws that hurt an honest model: none (IID split, no time or group structure).

Attacks that found nothing:
- Formats: every value has exactly 4 decimals; 44% of cells are zero; rows sum to 1e6 within 0.04; no missing values.
- Order/ids: RangeIndex; next-row label agreement 0.0458 against 0.0468 by chance.
- Copies: highest nearest-neighbour correlation 0.985 (median 0.899) on the top 5,000 log genes; no pair above 0.99.
  The nearest neighbour shares the label for 92.6% of rows (real tissue similarity, not copies).
- Columns from after the prediction point: none; every column is a gene.
- Transforms over all rows: none; values are raw TPM.
- Train-vs-test classifier: not run; uninformative under a random IID split.

Not checked:
- Tissue source site / plate batch: no barcodes in the kit; only the depth proxies above.
- Looking rows up in the GDC source: would work for any public data; not tried.
```

</details>

<details><summary>Precedent check: tcga_pancancer_tumor_type</summary>

```text
Precedent check: tcga_pancancer_tumor_type (2026-11-09)
Verdict: issues 2, 3 and 4 and the other definition calls follow precedent. Issue 1 follows LEAK-39 for GBM but departs
for the four BCGSC classes (ESCA, STAD, OV, LAML). The reason given is "untestable", which explains why the check could
not run but does not set the case apart. A reflection prompt is below. The register flags nothing specific to this dataset.

Issue 1, sequencing route by class (LEAK-13/15/39, Must)
  GBM (Broad and 2024 total-RNA): CONSISTENT with LEAK-39 (gallstone_disease, Andrej, 2026-10-26). The rule's own test
  ran: the other types' total-RNA rows are not called GBM (max P 0.024), and both GBM routes are in training. Gallstone's
  route rows were dropped because the route pulled the other class. That did not happen here.
  BCGSC (4 whole classes, about 1,4k rows): DEPARTS. No reason is written that sets the case apart. LEAK-39's test needs
  rows of another class on the same route, and none exist. Whole classes on one route are the LEAK-13/15 case, a
  recording by class. Retire precedent: prostate_cancer_detection (LEAK-15). Kept-with-note precedent: gallstone
  (format harmonised). Sibling in this batch, not decided yet: sarcoma_methylation_classification issue 2 (array type
  separable at AUC 1.00, 31 of 63 classes on one array, kept with a note). Decide both alike.
  Reflection prompt:
    Keep the four classes sequenced only at BCGSC, with the Class-dependent Recording marker, although no test can tell route from tumour type?
    **Problem:**
    - LEAK-15 (Must) retires a recording artefact that cannot be undone. LEAK-39's test cannot run when a route holds only whole classes.
    - The source removed the route with EB++ over all samples, and that correction is barred here (LEAK-30). So no fix keeps the rows.
    | Option | Pro | Con |
    | (a) keep with the marker. An exception, because the route is confined to classes whose nearest confusers (STAD vs COAD/READ, ESCA vs HNSC/LUSC, OV vs UCEC) differ by tissue biology far beyond the 0.999 macro AUC the UNC-only types already reach | keeps 4 real classes; no measured harm | first kept case where the leak test could not run; needs the fact in the definition and the record |
    | (b) ship the 28 UNC types (plus GBM) | no recording by class left; no exception | loses 4 classes and about 14% of the rows on an unmeasured effect |
    | (c) retire (LEAK-15) | strictest reading | drops a sound dataset; b already removes the artefact |
    Recommendation: (a) if the curator accepts the tissue-biology fact as the reason, written as an exception under LEAK-15 and LEAK-39. Otherwise (b). Decide together with sarcoma_methylation's array-type issue.
    [^1]: LEAK-13, LEAK-15, LEAK-30, LEAK-39

Issue 2, IID vs split by tissue source site (SPLIT-29/30/31): CONSISTENT.
  Precedent: sarcoma (Lennart, 2026-10-22, splits.md Cases SPLIT-29/31). There IID by patient was kept over a site split
  with the site visible (AUC 0.70-0.75) and log loss rising when sites were held out (0.46 to 0.58), because a lab types
  new patients. Here the cost is larger (linear 0.14 to 0.20-0.23, LightGBM 0.27 to 0.50). But the fact that sets this
  case apart points the same way: a site split leaves LAML (1 site) and most of ACC out of training. The optimism has to
  be stated in splits_comment, as for sarcoma; the builder has done that.
  Joint decision: this is the same call as treehouse issue 1 (donor, not study) and cns issue 2 (chip). All three keep
  IID by patient or donor against a batch-like group. tcga lines up with both.

Issue 3, merge COAD and READ (TP-7, USE-5): CONSISTENT with the recommended merge (b).
  Precedent: sarcoma MFS and UPS merged (Lennart, 2026-10-22). The source study treats them as one spectrum. Here
  TCGA's colorectal study and Hoadley et al. report "COAD/READ" as one group. That is the same kind of fact: the
  source's own grouping, and the pair separates mostly by site (AUC 0.58 with sites held out).
  Joint decision with treehouse AMKL/AML: the facts differ. AMKL is a WHO entity that follows one study, not a pair the
  source groups. So merging COAD/READ does not force an AMKL merge, and keeping AMKL does not argue against this merge.
  Shipping 33 classes (option a) would depart from sarcoma without a stated fact.
  Within the batch: sarcoma_methylation merges four chondrosarcoma subgroups into the source's families. That is the
  same pattern (the source's own grouping), so it is consistent.

Issue 4, both source quality flags dropped (CLEAN-1, CLEAN-11): CONSISTENT. Source quality flags drive the drop, with
  counts written. Recommendation (a) holds.

Other calls: one row per patient (LEAK-17), the EB++ matrix avoided (LEAK-30; sarcoma kept all-patient preprocessing
  only because no per-sample origin existed, while tcga rebuilt from the origin files, PROV-13), fallback log loss
  (MET-11), smallest class 34 (TP-8 cases kept at 3-5 per fold, about 11 here), approximate fit with primaries for CUP
  (USE-8, ljubljana_primary_tumor): all CONSISTENT.
No drift found. No third exception of one kind. If the BCGSC exception is taken and sarcoma_methylation's array type is
kept too, that makes two exceptions of one kind (a recording route that holds whole classes). A third should prompt an
amendment to LEAK-39 or LEAK-15.
```

</details>

<details><summary>Advocate: tcga_pancancer_tumor_type</summary>

```text
Advocate opening brief: tcga_pancancer_tumor_type (2026-11-09)
Position: ship, with COAD/READ merged (issue 3 B), pathology flags dropped (issue 4 A), IID kept (issue 2 A), route kept
with the Class-dependent Recording marker (issue 1 A), plus no-decision text fixes. Strongest first.

1. No leak, no copy, no shortcut was found by four independent agents (LEAK-16..21, LEAK-27..31, Must).
   Evidence: 0 exact profile copies over 58,383 genes, one row per patient (9,724 unique, split and claim auditors);
   best single gene AUC 0.67-0.69, depth-3 tree 0.65; task gamer: no exploit beats noise (format features gain 0.004 vs
   a random column's 0.003); column auditor: no post-outcome column, no id. Per-sample TPM rebuilt from origin files
   instead of the EB++ all-sample correction (LEAK-30 avoided, PROV-13). Every P4 Must the panel could test, held.

2. Use case is real and declared approximate honestly (USE-1, USE-8). The source names CUP as its clinical use; the
   practitioner confirms the inputs are what a lab has and nothing is post hoc; primaries for metastases follows the
   ljubljana_primary_tumor precedent. The practitioner would use it as a research benchmark. The metastasis gap is a
   fit limit stated in the notes, not a validity failure.

3. IID split is the precedent-consistent call (SPLIT-29/30/31; sarcoma, Lennart 2026-10-22; treehouse, cns alike).
   Site split is infeasible: LAML is 100% one site, ACC 71/78 one site, so a fold would train on no leukaemia. Cost is
   measured (log loss +35-70%) and written in splits_comment. Remedy ladder: state the cost (done) beats changing the
   regime that empties classes. Plate batch (claim auditor, median within-site AUC 0.77) is nested in site and kept by
   the same IID reasoning: one sentence in the site bullet / splits_comment, no decision needed.

4. Issue 1 (route by class) answers with the mildest remedy, not retirement (LEAK-13/15/39, Must). GBM: LEAK-39's test
   ran and passed (other types' total-RNA rows max P 0.024 for GBM; both GBM routes in training), consistent with
   gallstone. BCGSC (ESCA/STAD/OV/LAML): I concede no test can separate route from type and this is a departure from
   the prostate retirement. Keep with the marker as a written exception: the confusers (STAD vs COAD/READ, ESCA vs
   HNSC/LUSC, OV vs UCEC) differ by tissue biology, and the 28 UNC-only types already reach macro AUC 0.999, so the
   route cannot be what makes these classes easy. Fallback if the curator rejects the exception: option B (28 UNC types
   + GBM), still shipping, never C. Add the column auditor's note (route lives in small non-polyA RNAs, AUC 0.994/0.998).
   Decide jointly with sarcoma_methylation issue 2 (precedent checker).

5. Worth benchmarking despite saturated AUC (TP-1..8, MET-11). Macro AUC saturates, which is why log loss is the
   fallback; log loss spreads models: linear 0.11-0.14, LightGBM 0.17-0.24, RF 0.35-0.37 vs prior 3.24. Smallest class
   34 (about 11 per test fold, every class in every fold, MET-2). The blind reviewer's "near-saturated" is about
   accuracy (0.95), not the shipped metric. The COAD/READ merge (issue 3 B, sarcoma UPS/MFS precedent, the source's own
   COAD/READ grouping) removes the pair that carries 23-30% of the log loss on a distinction no clinician acts on
   (MET-8), and narrows the site gap (0.144 -> 0.112). Top-3 accuracy can be a note, not the metric.

6. Width is the dataset's value, not a defect (CLEAN-22, dtypes-from-context, lossless). 58,383 raw TPM columns are
   "as published"; dropping near-zero genes or log1p is a model's preprocessing choice; the column auditor recommends
   keeping raw. Width is exactly the large-features gap this batch was accepted for (record, 2026-11-08). The blind
   reviewer's change outranks nothing: a P7 preference against the lossless rule.

7. Remaining findings are text fixes that keep the dataset (writing, PROV-8/9/10): cite GDC Data Release 46.0 STAR
   TPM (GENCODE v36) as the data source with Hoadley 2018 as the task's reference (blind reviewer concern 3); state
   the primary-only filter explains SKCM 103 rows; GBM 284 = 155 Broad + 128 total-RNA + 1 other; claims.md 695 sites.
   Process: hidden_groups probe never finished; the builder's site probe covers the known hidden group; tell the
   curator, no block. Independent failures are not conflicts: each has its own mild fix.
```

</details>

<details><summary>Critic: tcga_pancancer_tumor_type</summary>

```text
Critic, opening brief: tcga_pancancer_tumor_type (2026-11-09)
Position: ship only after changes 1 and 2; points 3 to 6 are notes and fixes, none a reason to exclude.

1. BCGSC route holds four whole classes (validity, P4; LEAK-13/LEAK-15 Must, LEAK-39 Must).
   Problem: ESCA, STAD, OV, LAML (about 1,400 rows) were sequenced only at BCGSC, every other type at UNC/Broad. Builder
   kept them as "untestable". Untestable is not a reason (precedent checker: departs LEAK-15, prostate_cancer_detection
   retired). The route is visible in the profile: within GBM the two routes separate at AUC 0.994 from small RNAs alone,
   0.998 from histones (column auditor); LAML plates separate at 0.996 (claim auditor). The pairs it can bias,
   STAD vs COAD/READ and OV vs UCEC, are the domain practitioner's hardest clinical differentials and the gap "trusted least".
   Effect: the score can reward route memory on exactly the confusable classes.
   Remedy (mildest): either write the exception into the definition and record with the fact that sets it apart
   (tissue biology separates these classes from their confusers beyond what the route adds), marker
   `Class-dependent Recording`, and the note that the route lives in the non-polyA gene types; or, if the curator does
   not accept that fact, option B (ship the 29 non-BCGSC types). Decide jointly with sarcoma_methylation issue 2; that
   would be the second exception of this kind.

2. Colon vs rectum is a site label, not a decision (validity of the target; USE-5 Must, TP-7 Must).
   Pair AUC 0.78 IID, 0.58 with sites held out; 6.1% of rows carry 22.6-30.1% of the linear log loss; READ per-class
   log loss 1.16 -> 2.95 site-held-out (split auditor). The practitioner acts on "colorectal"; TCGA and Hoadley group
   COAD/READ. Remedy: merge to one colorectal class (builder's option B; sarcoma UPS/MFS precedent). Shipping 33 departs
   precedent without a stated fact.

3. Site and plate batch under IID, and the official hidden-group probe never finished (P4; SPLIT-29/30 Must, EV-3).
   695 sites, 0 with two types; 4,795 rows (49%) on single-type plates; plate AUC median 0.77 within site and type;
   site-held-out log loss +35-70%. IID is defensible (sarcoma precedent; LAML one site). I do not ask for a re-split.
   Remedy: add the plate sentence to the site bullet and splits_comment, and tell the curator that hidden_groups.py
   (and the full-width task and leak probes) did not finish, so the evidence is the builder's 2,000-gene stand-ins.

4. Provenance must name what ships (P5; PROV-10 Must).
   The data are GDC DR 46.0 STAR-Counts TPM (GENCODE v36), not the PanCanAtlas EB++ matrix of Hoadley 2018; a blind
   reader took them for the latter (blind reviewer 3). Remedy: cite the GDC release and file type as the data source,
   Hoadley 2018 as the source of the 33-type task; state the primary-only filter where SKCM's 103 rows make it visible.

5. Metric reads a decision partly not taken (P6; MET-8 Should).
   Log loss is right (macro AUC 0.999 saturates), but with COAD/READ split it is dominated by a distinction nobody acts
   on. Remedy: point 2 fixes most of it; add a note that the field reports top-1/top-3 accuracy.

6. Small factual slips (Could, writing). GBM is 284 rows (155 Broad, 128 total-RNA, 1 centre 53), not 283;
   claims.md T3 says 703 sites, shipped is 695. Remedy: fix the text.

Not argued: width (58,383 columns, 6,143 small-RNA genes) is a quality matter (CLEAN-22 keeps all genes); not a reason
to exclude. Value holds on log loss (linear 0.11-0.17, LightGBM 0.17-0.24, RF 0.35 vs prior 3.24; gamer found no exploit).
```

</details>
