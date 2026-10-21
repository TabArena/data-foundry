# glioma_grading_clinical_and_mutation_features

**Outcome:** added. A binary classification of the glioma grade (TCGA lower-grade glioma against glioblastoma) from
20 mutation flags, sex, race and age, on the original file of UCI 759 (862 patients), with a random split by
patient; not built yet. Verdict: ship after the changes now made (review panel, mediator). Validity: SEL-3 holds (an
expert diagnosis, the source's own task); USE-1/USE-3 open, since the use case checks a grade that already exists
(issue 5); USE-8 triggered, fixed (fit approximate); USE-5 kept with a note, reading to confirm (issue 1); LEAK-10
holds (project, diagnosis and patient code dropped); LEAK-14/LEAK-15 tested, not triggered; SPLIT-1 and SPLIT-29
hold. Value: TP-4 not triggered. Quality: CLEAN-11 holds (all 862 rows kept). Weighed: source +, use case -, size -,
label era -. For the curator: issues 5 and 1, and the tissue-site split, decided together with sarcoma's issue 4
(cross-dataset item).

**Main points:** Is a check of an existing histological grade against the mutations a use case (issue 5)? Keep a
grade label that was right in its era but is partly renamed by WHO 2021 (issue 1)?

**Record judgment:** valid with concerns. The record's assessment of 2026-10-07 holds (a classification task, the
label is the TCGA project, `Primary_Diagnosis` dropped, the by-site split scores like a random one); its note on the
patients shared with lgg_low_grade_glioma and glioblastoma no longer matters, since both are retired. The concerns are
the use case (issue 5) and the label's era (issue 1).

**Issues for Lennart:**

5. **Is a check of a grade that already exists a use case?** The label is the histological diagnosis, the grade a
   pathologist reads from the tissue under the microscope, and it exists before the tumour's DNA is sequenced. So at
   the prediction point the label is already known, and the only decision left for a model is to flag a disagreement
   between the mutation profile and the histology for review (a cross-check). No feature carries the histology, so
   this is not a leak.

   Effect on the task: the benchmark measures how well mutations and age reproduce the histological grade, a
   secondary task, not the grading itself. The scores are not biased by this; what changes is the decision they stand
   for. Evidence: grading LGG against GBM from these features is the source's own
   task (Tasci et al. 2022, 10-fold cross-validation, ROC AUC 0.908-0.920). The practitioner, playing a
   neuropathologist, calls the cross-check "a real but secondary task" and says "grading from mutations alone is not a
   decision anyone makes, only a check". Every diagnostic precedent predicts before the label exists
   (eryhemato_squamous_disease, lung_cancer_epithelial_genexp, sdss_17, breast_cancer_prediction). Two settings where
   the grade is unknown, a stereotactic biopsy too small to grade and a genomic registry with missing grades, were
   named, but no source was found for either, so the definition does not claim them.

   Rule: USE-1 and USE-3 (Must: an actor, a moment and a decision, with the inputs known at that moment). The
   cross-check meets the text of both (the lab, after sequencing, flags a case), so no option below fails a Must; the
   open question is whether a check of a known label counts as a real decision. USE-9 (weighed: a use case rephrased
   only to excuse a gap counts against it). No precedent covers a cross-check; the diagnostic precedents above all
   predict before the label exists.

   Implemented: the cross-check as the use case ("a neuropathology lab checks the histological grade against the
   tumour's mutation profile and flags a disagreement for review"), with fit approximate. Cost: the use case is our
   wording; the source only grades from the features. Options, lettered as in the precedent check (its option (a), a
   setting where the grade is unknown, has no source), all of which ship the dataset: (b) keep it as implemented and
   read it like the precedents, a weak use case ("-" in the priority, as now), no rule changes; (c) accept a cross-check as a kind of use case of its own, a new
   Cases row of USE-1 (cross-dataset item); (d) amend USE-1/USE-3 to allow a label known at the prediction point.
   Each of (c) and (d) changes a rule for every later dataset.

   Recommendation: (b), the reading that changes no rule; the panel (advocate, critic and mediator) leaves the choice
   to the curator. Decision: (b), (c) or (d)?

1. **Keep a grade label that was right in its era but is partly renamed by WHO 2021?** `Grade` is the TCGA project,
   set by the histological diagnosis made between 1989 and 2013 (858 of the 862 diagnoses are dated). LGG merges WHO
   grades II and III (238 and 259 patients). Since WHO 2021 the grade is an integrated diagnosis: the histology plus
   markers such as IDH, CDKN2A/B deletion, the TERT promoter, EGFR amplification and +7/-10 (a gain of chromosome 7
   with a loss of chromosome 10). The data has IDH but none of the others.

   Effect on the task: the 25 IDH-mutant GBMs are called "astrocytoma, IDH-mutant" today but stay CNS WHO grade 4, so
   their label holds. An unknown share of the 87 IDH-wildtype LGGs (at most about 10% of the rows) would be
   glioblastomas today, and the 128 mixed gliomas belong to an entity WHO 2021 no longer uses, though their grade class need not change. In those rows a model is
   scored against the label of its era. The share cannot be measured, because the markers are not in the data.
   Evidence: the label is not computed from the features: without IDH1 and IDH2 the ROC AUC is 0.893 (random forest)
   and 0.888 (logistic regression), against about 0.92 with all features.

   Rule: USE-5 (Must: the label is the target the actor acts on). Precedent: old clinical labels have shipped
   (heart_disease_cleveland, eryhemato_squamous_disease). corporate_credit_rating was retired under USE-5
   (2026-10-16), but its labels were wrong for their own date and could be repaired from the origin; here they were
   right under the criteria of their time, and a relabel needs markers the source never had. The advocate and the
   critic both accept that fact.

   Implemented: the source's label, with a note on the era and on grades II and III merged; fit approximate. Cost:
   part of the labels is not today's diagnosis. Alternative: relabel to the WHO 2021 grade from GDC copy-number and
   TERT data. Cost: a new dataset (PROV-14), and IDH would become part of the label, so IDH1 and IDH2 would have to go
   (SEL-5, as for coad_colon_adenocarcinoma's copy number).

   Recommendation: keep the label, and record the reading as a USE-5 Cases row ("a label correct under the criteria
   of its era, renamed later: kept with a note"), so the next TCGA-era label, such as tcga_kidney_cancers, is decided
   alike (cross-dataset item). Decision: confirm this reading of USE-5 and keep the label?

**Review panel:** ship after changes (mediator). Claim audit: 44 claims; refuted the gene list ("the 20 genes mutated
most often": they are the Cancer Gene Census genes, TTN ranks 4th overall) and the count of missing ages (5, not 4),
both fixed; the use case and the fit cannot be tested on the data. Blind review: include as a small, nearly
saturated task; main concern the small headroom over IDH1 (IDH1 plus age 0.902 against 0.920), then a batch effect
between the two TCGA projects, which the mediator tested: one sequencing centre and one calling workflow; the DNA of
142 GBM patients was copied in bulk before sequencing (whole-genome amplification), and a model tells it from plain
DNA no better than chance (ROC AUC 0.532). Debate: agreed on fit approximate, the corrected notes, the random split and keeping the 862 rows; for the
curator: the cross-check use case (issue 5) and the USE-5 reading (issue 1). The reports use the earlier numbering:
the earlier issue 1 is still issue 1, issues 2 (the 23 rows with a missing sex, age or race, kept under CLEAN-11) and 4
(IDH1 and age carry most of the signal, kept under TP-4) are settled by the panel as consistent with precedent; the mediator's issues 1 and 2 are issues 5 and 1 here.

<details><summary>Mediator</summary>

**Mediator: glioma_grading_clinical_and_mutation_features (2026-10-20, re-check)**

**Summary.** I recommend shipping after changes. The batch question is now settled: the advocate and the critic disagreed on it, and I ran the test. All 994 GDC mutation files of both projects come from one sequencing centre (barcode code 08, the Broad Institute) and one GDC workflow ("Aliquot Ensemble Somatic Variant Merging and Masking"). So "re-called with one pipeline" can be written, and the sequencing-centre test the critic asked for cannot be run, because every file comes from that one centre. One real difference remains between the classes: 142 GBM patients have whole-genome-amplified DNA, and no LGG patient does. That difference does not carry the signal. The features cannot tell amplified from plain DNA (RF AUC 0.532). With only plain-DNA GBM the AUC is RF 0.922, LR 0.919, against 0.919 and 0.917 on all rows. LEAK-14 and LEAK-15 are not triggered; the fix is a note. Two questions go to the curator: whether a cross-check after the label exists counts as a use case under USE-1/USE-3, and confirming the USE-5 reading for a label that was right in its era.


---

**Recommendation (judgment record)**

```text
Verdict: ship after changes.
Validity: SEL-3 holds; USE-1/USE-3 the cross-check use case is written, admissibility for the curator (issue 1);
  USE-8 triggered, fixed (fit approximate); USE-5 kept with a note (grades II+III merged; era label), reading to
  confirm (issue 2); LEAK-10 fixed (Project, Primary_Diagnosis, Case_ID dropped); LEAK-14/LEAK-15 tested, not
  triggered (one centre, one GDC workflow; whole-genome amplification of some GBM DNA not visible in the features),
  kept with a note; LEAK-16 holds; SPLIT-1 and SPLIT-29 hold (site-grouped per-fold AUC 0.921/0.927 vs 0.921/0.924).
Value: TP-4 not triggered (IDH1 0.860, IDH1+age 0.902, all 0.92); TP-2 a small real signal (keep).
Quality: CLEAN-11 holds (862 rows kept); notes corrected (gene list, 5 ages, retired siblings, per-fold AUC, batch).
Weighed: source + (the paper's own task), use case - (a cross-check), size -, label era -.
For the curator: issue 1 (is a cross-check a use case, USE-1), issue 2 (confirm the USE-5 reading as a Cases row).
```

**Changes to make now (no decision needed)**

1. **`fit="approximate"` (USE-8, Must).** Use the critic's `fit_reason`, which the advocate accepted: a histological grade of its era stands in for today's WHO 2021 integrated grade. The gene set comes from exome sequencing and lacks TERT, CDKN2A/B, EGFR amplification and +7/-10. The mutations are known after the histology. This follows sarcoma and coffee_rating_prediction.
2. **Reword `use_case` and the first curation bullet to the cross-check (USE-1, USE-3).** Use the practitioner's wording: "a neuropathology lab checks a histological grade against the tumour's mutation profile". Do not write the stereotactic-biopsy or genomic-registry settings: no agent tested them (EV-6, EV-7), and writing them would be "a use case rephrased only to excuse a gap" (USE-9). Whether the cross-check is admissible at all is issue 1.
3. **Label note (USE-5).** LGG merges WHO grades II and III (238 G2, 259 G3). Keep the existing WHO 2021 sentence.
4. **Gene list (PROV-3, EV-2, writing).** In `known` and the intro, write "the 20 Cancer Gene Census genes mutated most often in these patients (the GDC portal's list)". The current "the 20 genes mutated most often" is refuted: TTN ranks 4th. The selection is still label-free (LEAK-30 holds).
5. **Missing values (writing).** Write "`--` (4 patients without a clinical record, and the age of one more)". Age has 5 missing values.
6. **Sibling note (PROV-6, writing).** lgg_low_grade_glioma and glioblastoma are both retired. Say so, or drop the note.
7. **Site-split note (SPLIT-29, EV-1).** Say the numbers are mean per-fold ROC AUC and use the split audit's numbers: grouped by site LR 0.921 / RF 0.927, against 0.921 / 0.924 on the shipped split. Add "45 sites, each pure in the label; the features do not predict the site (below the majority rate)".
8. **Batch note (LEAK-14, LEAK-15).** Suggested text: "The two classes are two separately collected TCGA projects. Both were exome-sequenced at one centre (Broad Institute), and the GDC called all 994 files with one workflow. The DNA of 142 GBM patients was whole-genome amplified (no LGG). The features do not tell amplified from plain DNA (RF ROC AUC 0.532), and without the amplified GBM the ROC AUC stays at RF 0.922 / LR 0.919 (all rows 0.919 / 0.917)." The critic's draft said "sequenced at different times and centres". The centre part is refuted; the time part holds.

**Issues for the curator, ranked**

**1. Is a cross-check against an existing label a use case? (P3; USE-1, USE-3, Must; USE-9 a weighed factor)**
- Problem: at the prediction point the tissue diagnosis, which is the label, already exists. The model's decision is to flag a disagreement between the mutation profile and the histology for review.
- Effect: the benchmark then measures a secondary task, not primary grading. No feature carries the histology, so it is not a leak. There is no precedent for a cross-check.
- Advocate's best evidence: it is the source's own task (10-fold CV, AUC 0.908-0.920). An actor, a moment and a decision can be named: flag the case for review. The practitioner calls it "a real but secondary task". USE-2 is not triggered. The two settings where the label is unknown (stereotactic biopsy, registry backfill) are untested, so they should not be written.
- Critic's best evidence: every diagnostic precedent predicts before the label exists (eryhemato, lung_cancer_epithelial_genexp, sdss_17, breast_cancer_prediction). The priority judgment of 2026-10-20 says "'check on diagnosis' is ours". The practitioner says "grading from mutations alone is not a decision anyone makes, only a check".
- Why it is not mine to settle: USE-1's text is met by the cross-check wording. Whether it is a real decision is a reading of the rule with no precedent, weighed against USE-9's factor against excusing a gap.
- What would settle it: a source showing grading from sequencing without histology (biopsy or registry practice), which would make it USE-9 with a direct fit. Otherwise the curator chooses one of the precedent checker's options:
  - (b) treat it like the precedents: the use-case judgment stays "-";
  - (c) accept the cross-check as a kind of use case of its own, as a USE-1 Cases row;
  - (d) amend USE-1/USE-3.

**2. Keep a label that was right for its era but renamed by WHO 2021 (P3; USE-5, Must): confirm the reading**
- Problem: the label is the 1989-2013 histological project (LGG = II+III, GBM = IV), not today's integrated diagnosis.
- Effect: the 25 IDH-mutant GBMs keep grade 4. An unknown share of the 87 IDH-wildtype LGGs (at most about 10% of rows) and the 128 mixed gliomas would be classified differently today. The share cannot be tested with this data.
- Advocate's best evidence: the labels are correct under the criteria of their time. A relabel needs markers the source lacks, and it would make IDH part of the label, so IDH would have to go (coad, SEL-5). That makes it a new dataset (PROV-14).
- Critic's best evidence: corporate_credit_rating was retired under the same Must. Both sides accept the fact that sets this case apart: those labels were wrong for their own date and could be repaired from the origin. The critic asks only for confirmation.
- Decision needed: confirm the reading and record it as a USE-5 Cases row ("a label correct under the criteria of its era, renamed later: kept with a note"), so the next TCGA-era label (for example tcga_kidney_cancers) is decided the same way.

Settled, not for the curator: the batch question (LEAK-14/15, see the facts below), the fit, and the writing fixes. Optional and raised by no side: the practitioner would drop `Race`. That would change no verdict, so it is not listed as an issue.

**Agreed facts**

Measured by the auditors and accepted by both sides:
- Size and identity: 862 rows, one per patient (862 unique Case_IDs). Grade equals the TCGA project in 862 of 862 rows. "Glioblastoma" appears only in GBM. The 45 tissue sites are each pure in the label.
- Source file: the raw file's sha256 matches. The flags match the GDC in 17,220 of 17,240 cells, and every file is WXS. The ages match the GDC within 0.75 days.
- Leaks: missingness indicators AUC 0.500. No duplicate rows, and no test row copied from train.
- Hidden site group: the site cannot be predicted from the features (LGG 0.175 vs majority 0.214; GBM 0.317 vs 0.338).
- Signal: IDH1 alone 0.860, IDH1 + age 0.902, all features about 0.92. Without IDH1/IDH2: RF 0.892, LR 0.883-0.888.
- Gene list: refuted as written (TTN is 4th). The 20 genes are the top Cancer Gene Census genes (19 of 20 reconstructed), chosen without the label.
- Missing values: 5 ages are `--`, not 4.
- Both sibling datasets are retired.
- Label: LGG has G2 238 and G3 259. There are 25 IDH-mutant GBMs and 87 IDH-wildtype LGGs.

New from my test (GDC files API, 994 masked somatic mutation files of TCGA-LGG and TCGA-GBM):
- Every file uses one workflow, "Aliquot Ensemble Somatic Variant Merging and Masking". Every tumour aliquot carries centre code 08 (Broad Institute), in both projects. So "the GDC re-called both with one pipeline" holds. The critic's "different centres" is refuted, and the within-project test by sequencing centre cannot be run: there is only one centre.
- One difference does follow the class:
  - DNA type: 142 GBM patients have whole-genome-amplified DNA (analyte W; 63 only W, 79 both W and D). No LGG patient has it. 221 GBM and 499 LGG have plain DNA only.
  - Plates: only 1 of 37 sequencing plates (A33T) holds both projects.
- Whether that difference carries the signal:

  | Test | Result |
  |---|---|
  | Amplified vs plain DNA within GBM, from the 21 features | RF AUC 0.532 (10 seeds) |
  | Amplified vs plain DNA within GBM, from total mutation burden | AUC 0.647 |
  | Grade AUC, all rows | RF 0.919, LR 0.917 |
  | Grade AUC, only plain-DNA GBM (720 rows, 221 GBM) | RF 0.922, LR 0.919 |
  | Grade AUC, dropping only the W-only GBM | RF 0.928, LR 0.924 |
  | Model trained on other plates, scored on shared plate A33T (11 GBM, 38 LGG) | RF 0.923 (95% bootstrap 0.84-0.99), LR 0.916 |

  The batch carries none of the grade signal. The shared-plate test is small, but it agrees with the rest.
- Passenger genes: within GBM, MUC16, CSMD3 and FAT4 are mutated at similar rates in amplified and plain DNA (0.22 vs 0.21 per patient). The GBM excess over LGG (0.24 vs 0.13) goes with tumour mutation burden (median 58 vs 30 calls), a property of the tumour.

**Consistency with precedent**

- **Followed:**
  - fit approximate for a label stand-in (sarcoma 2026-10-20, coffee_rating_prediction 2026-10-14);
  - keeping old clinical labels (heart_disease_cleveland, eryhemato), apart from corporate_credit_rating by the fact both sides accept (issue 2);
  - keeping the rows with missing demographics (CLEAN-11: caracas, churn_telco_south_asia, heart_disease_va_long_beach);
  - a dominant natural core (TP-4: sepsis_survival, aps_failure);
  - the original file over the authors' coded copy (PROV-13, PROV-15);
  - the hidden site group measured the way sarcoma's was (site from features, site-grouped over seeds). Whatever the curator decides on sarcoma's issue 4 should be checked against this dataset.
- **Departure without a precedent:** the cross-check use case (issue 1). No fact sets it apart yet, so it is a question for the curator, not a recommendation.
- **Batch:** no precedent. prostate_cancer_detection (LEAK-15, retired) differs on the measured fact: there, the features separated same-label groups (0.92-0.97). Here they do not separate the amplified from the plain GBM DNA (0.532).

</details>

<details><summary>Claim audit</summary>

**Claim audit: glioma_grading_clinical_and_mutation_features (2026-10-20, re-check)**

Tests: the data and models on the shipped 10x3 splits; the GDC clinical API; the GDC open-access somatic
calls (76,873 occurrences of TCGA-LGG+GBM, GDC release 46); a random forest with the task-probe settings; the
full text of Tasci et al. 2022 from Europe PMC (PMC9697273).

| # | Claim | Source | Test | Result | Evidence | Rule |
|---|---|---|---|---|---|---|
| 1 | Question LGG vs GBM from mutations, age, sex, race | D task_summary | columns of the built frame | holds | 20 flags + Gender, Age, Race; target Grade | USE-1 |
| 2 | Use case: care team assigns grade from mutations "as a check on the tissue diagnosis" | D | none possible on the data | untested | the label is the tissue diagnosis, which exists before sequencing; the decision is a cross-check (checklist P3 concern) | USE-1, USE-2, USE-8 |
| 3 | 862 patients diagnosed 1989-2013 | D | GDC cases API, year_of_diagnosis | holds (858 of 862 dated) | 858 years, 1989-2013 (GBM 1989-2013, LGG 1992-2013); 4 undated | PROV-3 |
| 4 | LGG = WHO grade II/III, GBM = grade IV, from tissue | D | GDC tumor_grade; Primary_Diagnosis crosstab | holds | LGG: G2 238, G3 259, none 2; GBM: 360 "Glioblastoma", 3 `--` | USE-5 |
| 5 | Known: the 20 genes mutated most often in these patients | D known, also #14 | rank all genes by patients with a GDC call among the 862 | **refuted** | TTN is 4th (169 patients), FLG 11th, RYR2 12th, LRP2, PCLO, HMCN1, MUC17, OBSCN, PKHD1 all above most file genes; file genes rank 1-75 (IDH2 67th, PDGFRA 75th). The 20 are the top Cancer Gene Census genes: 19 of 20 match, the 20th place is a tie at 22 patients (PDGFRA in file, TRRAP and ARID1A tied) | PROV-3, EV-2, writing.md |
| 6 | Random patients split; test = new patients like the projects | D | 862 unique Case_ID; site-held-out vs random | holds | see #18 | SPLIT-1 |
| 7 | Drops Project, Primary_Diagnosis, Case_ID; keeps patients the authors drop | D | code; 862 vs 839 | holds | 23 extra rows = 12 LGG + 11 GBM, exactly 499-487 and 363-352 | PROV-13 |
| 8 | fit "direct" | D | none on data | untested | same gap as #2; WHO-2021 mismatch named in fit_reason | USE-8, USE-9 |
| 9 | Mutations known once sequenced; WHO 2021 regrades some | D | GDC experimental_strategy of masked somatic files | holds (first part); second untested | all 994 files WXS; regrading needs CDKN2A/TERT/+7-10, not in data | LEAK-1, USE-5 |
| 10 | year 2022, UCI, DOI, CC BY 4.0 | D | not tested (licence is never evidence); DOI/paper checked in checklist | untested (by design) | | PROV-1 |
| 11 | UCI zip has the 862-row csv (sha256 6c617f37...) and 839-row authors' file = OpenML 46604 | D | sha256sum; row counts; OpenML API | holds | sha256 matches; InfoWithGrade 839 rows; OpenML 46604 839 instances, 24 columns | PROV-8 |
| 12 | bibtex Tasci et al. 2022 IJMS 23(22):14155 | D | Europe PMC lookup | holds | DOI 10.3390/ijms232214155 resolves to that paper | PROV-10 |
| 13 | binary, IID, 10x3 | D/README | splits of the definition | holds | 10 repeats x 3 folds, test 287-288 | SPLIT-1 |
| 14 | Intro: 862 patients, 20 genes mutated most often | D comments | as #5 | **refuted** (gene part) | as #5 | as #5 |
| 15 | Prediction point after resection and sequencing | D comments | none on data | untested | as #2 | USE-3 |
| 16 | Grade = TCGA project for every row | D | raw compare + GDC project | holds | 862/862 equal; GDC project agrees 100% | USE-5 |
| 17 | 45 sites, each to one project only | D | site code of Case_ID x Grade | holds | 45 sites, 45 pure | SPLIT-12 |
| 18 | By-site split LR AUC 0.919 vs random 0.918 | D | GroupKFold on site vs StratifiedKFold, LR, k=3/5/10 | holds | site 0.914/0.918/0.918 vs random 0.915/0.916/0.917 | SPLIT-12, EV-1 |
| 19 | Flags are GDC open-access WXS somatic calls for every patient | D | GDC ssm_occurrences per case-gene | holds | 862/862 patients have calls; all files WXS | PROV-3 |
| 20 | 70 no-mutation patients have 3-110 other calls | D | count GDC calls per patient | holds | 70 patients, 3 to 110 calls | CLEAN-? (missing vs wildtype), PROV-3 |
| 21 | Flags, sex, race categorical | D | dtypes | holds | 23 category columns, age float | CLEAN |
| 22 | Genes chosen by frequency over all patients, without the label | D | paper Sec. 2.2 + reconstruction #5 | holds | paper: "the most frequently mutated 20 genes according to percentage of cases affected for glioma data" (Fig. 1); label-free, reconstructed over both projects (LGG-only or GBM-only top lists differ) | LEAK-30 |
| 23 | age = years + days/365.25 matches GDC day count within one day | D | vs GDC age_at_diagnosis (primary diagnosis) and -days_to_birth | holds | 857 compared, max abs diff 0.75 days | CLEAN |
| 24 | `--` = 4 patients without a clinical record; `not reported` race 18 | D | count `--` per column | **refuted** (count) | `--`: Gender 4, Race 4, Age 5; TCGA-W9-A837 has sex and race but age `--`; so 5 missing ages, not 4 | writing.md, CLEAN |
| 25 | grades histological, 1989-2013 | D | as #3, #4 | holds | | USE-5 |
| 26 | without IDH1/IDH2: LR 0.888, RF 0.893 | D | shipped splits; RF 200 trees min_samples_leaf 2 (probe settings); LR one-hot | holds | RF 0.892; LR 0.883 (encoding differs); also without IDH and age RF 0.864 | LEAK-10, EV-1 |
| 27 | Shares 240 of 247 (lgg_low_grade_glioma) and 180 of 274 (glioblastoma) patients; other targets | D | patient IDs of the sibling raw files | holds but stale | 240 of 247; glioblastoma methy&mirna 277 patients, 181 shared (274 after subtype filter); both siblings are retired (`No`, folders removed), so the note's "matters for a method trained across datasets" is moot | PROV-6 |
| 28 | 'Glioblastoma' only in TCGA-GBM | D decision | crosstab | holds | 360 GBM, 0 LGG | LEAK-10 |
| 29 | 17,220 of 17,240 cells match GDC | D decision | case x gene compare with canonical-transcript gene symbols | holds | exactly 17,220 of 17,240; 20 mismatches spread over genes | PROV-3 |
| 30 | age text format ("87 years", "--") | D docstring | regex on all values | holds | all non-`--` parse | CLEAN |
| 31 | _clean raises if Grade != project | D | code read + data | holds | | |
| 32 | three clinical columns then 20 genes | D | raw column order | holds | | |
| 33 | no splits_comment, no accepted warnings | D | `dataset check` | holds | 0 warnings | |
| 34-35 | curator CC lines | R | n/a (decisions, not facts) | not a claim | | |
| 36 | paper classifies with 10-fold CV, AUC 0.91-0.92 Table 3 | R | paper text | holds | "A 10-fold cross-validation technique was also applied"; Table 3 AUC 0.908-0.920 | SEL-2, TP-10 |
| 37-39 | as #16, #28, #29, #17-18 | R | as above | holds | | |
| 40 | not a duplicate of the siblings | R | as #27 | holds, stale | siblings retired | PROV-6 |
| 41 | 25 IDH-mutant GBMs | R | IDH1 or IDH2 MUTATED among GBM | holds | 25 (23 IDH1); WHO-2021 consequence untested | USE-5 |
| 42 | IDH1 and age carry most signal; priority 2 | R | IDH1 alone, IDH1+age, all | holds | LR on shipped splits 0.860 / 0.902 / 0.917 | TP-2 |
| 43 | front matter | R | as #10, #13 | holds | | |
| 44 | the earlier REVIEW.md's facts | earlier REVIEW.md | Primary_Diagnosis counts; IDH; missing | holds | Mixed glioma 128; IDH-wildtype LGG 87; missing 12 LGG / 11 GBM | |

Implied claims:

| Implied claim | Test | Result | Evidence | Rule |
|---|---|---|---|---|
| Every feature known at the prediction point | feature list vs moment; label-free missingness | holds | flags from tumour WXS, demographics; missing indicators AUC 0.500 (probe) | LEAK-1 |
| Split is what the use case needs | site-held-out vs random | holds | #18 | SPLIT-1, SPLIT-12 |
| Target is the real-world target | GDC tumor_grade, WHO 2021 | holds with the stated caveat | histological grade; WHO 2021 integrated diagnosis would differ for some rows (untestable here) | USE-5 |
| No row copied across the split | exact feature-row match over 30 splits; unique Case_ID | holds | 0 duplicated rows, 0 test rows with an exact train copy | LEAK-16 |

**Refuted, ranked**

1. #5 / #14 "the 20 genes mutated most often in these patients" (P5 description, writing; no validity effect): they are
   the 20 most often mutated Cancer Gene Census genes (GDC portal's list); TTN (4th, 169 patients) and other long
   non-census genes are left out. Mildest remedy: reword `known` and the intro to "the 20 cancer-census genes mutated
   most often in these patients (the GDC portal's list)".
2. #24 "`--` (4 patients without a clinical record)": 5 ages are `--` (TCGA-W9-A837 has sex and race). Remedy: "`--`
   (4 patients without a clinical record, and the age of one more)".

**Untested, ranked**

1. #2 / #8 / #15 use case and fit "direct" (P3, USE-1/USE-8): no data test; the label is the histology that precedes
   sequencing, so the task is a cross-check. Curator call; mildest change is fit "approximate".
2. #9 / #25 / #41 WHO 2021 regrading extent: markers (CDKN2A, TERT, +7/-10) are not in the data.
3. #10 licence: never evidence.

Stale (holds, but moot): #27 / #40 sibling overlap; both siblings are retired. Remedy: drop the note or say they are
retired.

</details>

<details><summary>Column audit</summary>

**Column audit: glioma_grading_clinical_and_mutation_features (2026-10-20, column-auditor)**

Prediction point (curation_comments, first bullet): a diffuse glioma has been resected or biopsied and its DNA
sequenced; the grade class (LGG grade II/III vs GBM grade IV) is assigned from 20 mutation flags plus sex, race, age.
Frame: the definition rebuilt through `dataset_io.load(..., built=False)`: 862 rows, 23 features + `Grade`, IID,
rows shuffled (raw file is sorted LGG then GBM, next-row label match 0.999; the shipped order is mixed, CLEAN-23 holds).
Codebook: UCI 759 page and Tasci et al. 2022 (Sec. 2.1); the file has no further dictionary, so meanings come from
the UCI variable table and the GDC field names.

**Column table**

| column | meaning | known at prediction? | dtype and cleaning | verdict | rule |
|---|---|---|---|---|---|
| Grade (target) | TCGA project: LGG (grade II/III) or GBM (grade IV), histological diagnosis 1989-2013 | target | category {LGG 499, GBM 363}; checked equal to `Project` in `_clean` | fine (label era is the REVIEW issue 1, not a column problem) | USE-5, CLEAN-15 |
| Project (dropped) | TCGA-LGG / TCGA-GBM | no: a copy of the label | dropped | fine (leak removed) | LEAK-10 |
| Primary_Diagnosis (dropped) | histology (Glioblastoma 360 only in GBM, etc.) | no: the diagnosis the label follows from | dropped | fine (leak removed) | LEAK-10, LEAK-2 |
| Case_ID (dropped) | TCGA barcode; site part = tissue source site | identifier; 45 sites, 0 send to both projects | dropped; one row per patient (0 duplicate ids) | fine | CLEAN-3, LEAK-10, LEAK-17 |
| Gender | patient sex (GDC) | yes | category; `--` (4 rows, no clinical record) -> NaN | fine; alone AUC 0.532 | CLEAN-10, CLEAN-14 |
| Age_at_diagnosis | age at diagnosis, GDC text "N years D days" | yes | float years = N + D/365.25 (D max 364; 2 rows "N years" only); `--` (5 rows) -> NaN; range 14.4-89.3, nothing impossible | fine; alone 0.769 | CLEAN-10, CLEAN-11, CLEAN-14 |
| Race | self-reported race (GDC) | yes | category; `not reported` (18) and `--` (4) -> NaN; one level with 1 row (american indian) | fine; alone AUC 0.529; a weak proxy of the site but a legitimate patient fact | CLEAN-10, CLEAN-14 |
| IDH1 | somatic mutation in IDH1 (GDC open-access WXS calls) MUTATED / NOT_MUTATED | yes, once sequenced | category, 2 levels, no missing | fine; alone 0.860, drop costs 0.900 -> 0.857: the real core signal, not a label encoding (without IDH1+IDH2 0.888-0.893 per claims) | LEAK-10 holds, TP-4 |
| TP53 | somatic mutation flag | yes | category, 2 levels | fine | CLEAN-13 (separate flags, multi-label) |
| ATRX | somatic mutation flag | yes | category | fine | CLEAN-13 |
| PTEN | somatic mutation flag | yes | category | fine (alone 0.639) | CLEAN-13 |
| EGFR | somatic mutation flag (point mutations; amplification not encoded) | yes | category | fine | CLEAN-13 |
| CIC | somatic mutation flag (22% LGG, 1.1% GBM) | yes | category | fine | CLEAN-13 |
| MUC16 | somatic mutation flag; large gene, passenger-prone (16.3% GBM, 8.2% LGG) | yes | category | fine; see problem 2 | CLEAN-13 |
| PIK3CA | somatic mutation flag | yes | category | fine | CLEAN-13 |
| NF1 | somatic mutation flag | yes | category | fine | CLEAN-13 |
| PIK3R1 | somatic mutation flag | yes | category | fine | CLEAN-13 |
| FUBP1 | somatic mutation flag (9% LGG, 0.6% GBM) | yes | category | fine | CLEAN-13 |
| RB1 | somatic mutation flag | yes | category | fine | CLEAN-13 |
| NOTCH1 | somatic mutation flag (7.6% LGG, 0 GBM) | yes | category | fine (pure only for one value, under 100 rows) | CLEAN-13 |
| BCOR | somatic mutation flag | yes | category | fine | CLEAN-13 |
| CSMD3 | somatic mutation flag; large gene, passenger-prone | yes | category | fine; see problem 2 | CLEAN-13 |
| SMARCA4 | somatic mutation flag | yes | category | fine | CLEAN-13 |
| GRIN2A | somatic mutation flag | yes | category | fine | CLEAN-13 |
| IDH2 | somatic mutation flag | yes | category | fine | CLEAN-13 |
| FAT4 | somatic mutation flag; large gene, passenger-prone | yes | category | fine; see problem 2 | CLEAN-13 |
| PDGFRA | somatic mutation flag (point mutations; amplification not encoded) | yes | category | fine | CLEAN-13 |

No post-outcome column, no missingness tied to the label (indicator AUC 0.500; 12 LGG / 11 GBM rows with a missing
demographic), no window ending at the outcome, no id left in the features, no statistic over all rows (the age
conversion is per row; the gene choice by frequency over all patients is CLEAN-8). No untyped object column (CLEAN-9).

**Problems, ranked (principles)**

1. **P4, LEAK-13 / LEAK-15 (Must if strong), question for the curator, weak and untested: sequencing-batch confound
   with the class.** Each class is one TCGA project, sequenced at different times and centres (GBM largely earlier),
   so any project-level difference in coverage or calling is perfectly aligned with the label and probe 7 cannot
   separate it (no same-label subgroups across projects). Evidence it is not strong: the GDC harmonised calls (17,220
   of 17,240 cells match the API), the top features are textbook biology (IDH1, CIC, FUBP1, NOTCH1 LGG-only; PTEN,
   EGFR GBM), and the 70 rows with no flag set (55 GBM, 15 LGG) have 3-110 calls elsewhere. Mildest remedy: none in
   the data; one sentence in the notes that the classes come from two separately sequenced projects. Only worth a
   test (passenger-gene burden per sequencing centre within one project) if the critic presses it.
2. **P4, LEAK-10, not a leak (recorded so it is not re-raised):** the passenger-prone large genes (MUC16, CSMD3,
   FAT4) are about twice as often mutated in GBM, a tumour-mutation-burden effect. TMB is a property of the tumour at
   sequencing, known at the prediction point; keep.
3. **P7, CLEAN-10 (Should), minor:** `Race` merges `not reported` (a reported non-answer, 18) and `--` (no clinical
   record, 4) into one NaN. The `--` rows are already marked by `Gender`/`Age` being NaN, so no information is lost;
   fine as is.
4. **P7, CLEAN-14 (Should), minor:** `Race` keeps a level with one row (american indian or alaska native). Keeping
   rare levels is right (the pipeline handles it); no change.

Verdict: every column fine; no leak or cleaning fix required. One question for the curator (problem 1, a
notes-only remedy).

</details>

<details><summary>Split audit</summary>

**Split audit: glioma_grading_clinical_and_mutation_features (re-check, 2026-10-20)**

**Verdict: right (one minor note on wording).** IID, 10 repeats x 3 folds (test 287-288 rows), declared `split_regime: iid`,
no grouping, no time column.

Method: the definition's frame via `dataset_io.from_definition`, rows matched back to
`Case_ID` through the cleaned raw file on all 24 values; 862 of 862 keys unique). Threads capped at 2.

**Regime against the use case**

* What one prediction is: one patient's tumour after sequencing (task_summary `use_case`). 862 rows, 862 unique
  `Case_ID`s: one row per patient, so every test row is a new patient; cold start and IID coincide (USE-10, USE-11,
  SPLIT-2, SPLIT-23).
* Temporal: no time column; diagnoses 1989-2013 are a cohort, not a stream of signals with a prediction point that
  moves (SPLIT-6, SPLIT-7 do not apply). The change of grading criteria over time (WHO 2021) is a label and fit question
  (P3, USE-5/USE-8), already named in `fit_reason`, not a split question.
* Grouped: no recurring entity in the rows. The only group id in the source is the TCGA tissue source site (barcode
  field 2), a true id (SPLIT-24), dropped with `Case_ID`.

**Hidden group: the tissue source site (SPLIT-29, SPLIT-30)**

* 45 sites, **45 of 45 pure** in the label (26 LGG-only, 19 GBM-only); largest site `06` holds 111 rows (12.9%), then
  `HT` 98, `DU` 81. The site carries the label, and a new hospital would be a new site, so the question is whether the
  features let a random split recognise the site.
* Site from features, within one grade (sites with 10+ rows, random forest, 3-fold): LGG accuracy 0.175 vs majority
  0.214 (13 sites); GBM 0.317 vs 0.338 (10 sites). The features do not identify the site.
* Alternative split, run (10 repeats x 3 folds, StratifiedGroupKFold on site vs StratifiedKFold vs the shipped splits),
  mean per-fold ROC AUC:

  | split | LR | RF |
  |---|---|---|
  | shipped | 0.921 (sd 0.013) | 0.924 (sd 0.013) |
  | random 3-fold | 0.920 (sd 0.012) | 0.923 (sd 0.012) |
  | grouped by site | 0.921 (sd 0.024) | 0.927 (sd 0.022) |

  No drop. The site-grouped folds have a GBM share between 0.12 and 0.80 (vs about 0.42), which doubles the fold sd
  and lowers the pooled out-of-fold AUC (0.899 / 0.902) through calibration shift, not through lost signal.
* Hidden-group probe: 0 candidates; near copies 0.0% at 0.85 (0.2% at 0.7). 615 rows match another on all categorical
  values and differ by age: sparse binary flags of distinct patients, not an entity (SPLIT-24 bars a similarity key).
* Conclusion: the site is a hidden group with a pure label, but the random split does not reward recognising it
  (SPLIT-29 not triggered); per SPLIT-4 the gap would not decide anyway, and here the use case (a new patient, whatever
  the hospital) and the data agree on IID.

**Problems, ranked**

1. **P4, minor (writing; SPLIT-5/EV-1 precision).** The note "holding out whole sites scores like a random split
   (logistic regression ROC AUC 0.919 against 0.918)" is confirmed in substance (per-fold 0.921 vs 0.920 here), but
   it does not say the AUC is per fold; the pooled out-of-fold AUC under the site split is 0.899, which a reader could
   mistake for a gap. Mildest remedy: state "mean per-fold ROC AUC" and, optionally, "45 sites, each pure in the label,
   and the features do not predict the site (below the majority rate)". No re-split.
2. **Context only (PROV-4 to PROV-7, not a split issue).** Patients shared with lgg_low_grade_glioma (240) and
   glioblastoma (180): matters for cross-dataset training only, already noted.

No gap, filter or re-split is needed.

</details>

<details><summary>Domain practitioner</summary>

**Domain practitioner: glioma_grading_clinical_and_mutation_features**

Actor played: a neuropathologist signing out a diffuse glioma (with the molecular tumour board), 2026.

**Fit: approximate (the definition says direct)**

One-sentence reason: when the mutations exist I already hold the histology the label is copied from, and what I act
on today is the WHO 2021 integrated diagnosis, which this histological LGG/GBM label (1989-2013) only stands in for,
from a gene set that lacks the markers that decide it (USE-5, USE-8 "a stand-in with a known gap").

**1. Inputs at the prediction point (USE-3, USE-6)**

* I have: IDH1/IDH2, TP53, ATRX, PTEN, EGFR, NF1, PIK3CA, PIK3R1, PDGFRA, RB1, CIC, FUBP1, NOTCH1, BCOR, SMARCA4 (all on
  routine glioma NGS panels), age, sex. Race I have, but would never use for grading.
* I would not have from a clinical panel: MUC16, CSMD3, FAT4 (very long genes, mostly passenger calls in exome data;
  not on glioma panels), GRIN2A rarely. Whole-exome calls are a research setting; harmless as inputs but not what my
  lab report gives.
* Missing that I would always have at that moment: the H&E histology (necrosis, microvascular proliferation, mitoses:
  the grade itself), MRI contrast enhancement, IDH R132H and ATRX immunostains, 1p/19q codeletion, CDKN2A/B homozygous
  deletion, TERT promoter mutation (not covered by exome), EGFR amplification (the data has EGFR mutation only),
  chr +7/-10, MGMT methylation, often a methylation-array class. These are exactly the markers that move a tumour
  between grade 2/3 and 4 today (cIMPACT-NOW 3; WHO CNS5 2021).

**2. Target (USE-5)**

* The label is the TCGA project = the submitting site's histological diagnosis. That is a proxy: I act on the
  integrated diagnosis (type + CNS WHO grade 2/3/4). The proxy diverges where it matters clinically: histologically
  lower-grade IDH-wildtype astrocytomas with TERT/EGFR-amp/+7-10 are glioblastomas now (some of the 87 IDH-wt LGG
  rows); IDH-mutant astrocytomas with CDKN2A/B deletion are grade 4; 128 "mixed glioma" rows are an abandoned entity.
  The 25 IDH-mutant GBMs keep grade 4, so a "grade 4 or not" reading survives better than "glioblastoma or not".
* Binary LGG (II+III) vs GBM (IV) merges grade 2 and 3, which I treat differently (radiotherapy + chemotherapy timing).
* I would want a probability (of grade 4 / of discordance with histology), to flag cases for review; ROC AUC / log loss
  fit that.

**3. Rows and test data (USE-10, USE-11)**

* One row = one patient = one diagnosis: matches my decision; new patients, so IID without grouping is right.
* The test data is not what I face: TCGA enrolled selected, resected, fresh-frozen cases from ~1989-2013 and in a
  58/42 LGG/GBM mix; in an adult neuro-oncology service glioblastoma is the large majority of diffuse gliomas, and the
  next patient comes from another site with a panel, not an exome. The site-held-out check (0.919 vs 0.918) reassures
  on site, not on era or label definition.

**4. Would I use it?**

No, not for grading: the histology is in hand before the sequencing, and the guidelines grade by explicit rules from
markers not in the data. The plausible use is the one the source names, a consistency check of histology against the
mutations (or filling missing grade annotations in a genomic registry); that is a real but secondary task (USE-9:
rephrasing to it would excuse a gap, so it does not make the fit direct). I would distrust a model whose gain over
"IDH1 + age" (0.902 vs 0.92) comes from passenger genes like MUC16/FAT4 or from race.

**Gaps, ranked by how much they change the task**

1. Label is TCGA-era histological grade, not the WHO 2021 integrated grade the clinician acts on (USE-5, USE-8).
2. Prediction point: the histology the label is taken from precedes the sequencing; grading from mutations alone is
   not a decision anyone makes, only a check (USE-1, USE-3, USE-4).
3. Decisive markers always available today are absent (TERT promoter, EGFR amplification, +7/-10, CDKN2A/B, 1p/19q)
   (USE-6).
4. Case mix and era: TCGA selection and LGG/GBM ratio differ from a clinic's; test stands for TCGA-like patients only
   (USE-8, test data).
5. Grade 2 and 3 merged; exome-only passenger genes and race as inputs (minor; USE-5, USE-6).

None of these is a leak or makes the task unreal; they argue for fit approximate, not rejection (USE-2 does not apply,
USE-12).

**What an expert would change**

* Set `fit="approximate"` and name the gap in `fit_reason`: histological TCGA-era label as a stand-in for the WHO 2021
  integrated grade, from an exome gene set lacking TERT/CNV markers.
* Reword `use_case`: "a neuropathology lab checks a histological grade against the tumour's mutation profile" rather
  than "assigns the grade from the mutations".
* Optional (a new dataset, not this one): relabel to CNS WHO 2021 grade 4 vs not from GDC copy-number and TERT data,
  and add 1p/19q, CDKN2A/B, EGFR amplification as features. Not required to ship this one.
* Optional: drop `Race` (no clinical role in grading); keep it if the benchmark wants the source's columns.

**Sources**

* Dataset definition and record: `datasets/_dev/tabarena-v0pt2/glioma_grading_clinical_and_mutation_features/dataset.py`,
  `curation/records/glioma_grading_clinical_and_mutation_features.md`, REVIEW.md, the panel's claim list.
* Tasci et al. 2022, IJMS 23(22):14155 (the source's task).
* Brat et al. 2018, cIMPACT-NOW update 3, Acta Neuropathol: https://pmc.ncbi.nlm.nih.gov/articles/6204285
* Louis et al. 2021, WHO CNS5 classification, Neuro-Oncology 23(8):1231 (as cited in the folder's REVIEW.md).
* Rules: `.claude/skills/knowledge-curation/references/use_case.md` USE-1 to USE-12.

</details>

<details><summary>Blind review</summary>

**Blind review: glioma_grading_clinical_and_mutation_features**

**Verdict:** Include. The task is real and leak-free, but it is small and close to saturated. It works as a low-weight, small-data member of the benchmark.

**Task**
The data is TCGA LGG and GBM glioma cases. The target is `Grade`: LGG (499) vs GBM (363). The features are age, gender, race and the mutation status of 20 genes. A real use is computer-aided grading from a gene panel plus demographics. But in practice histopathology sets the grade, so the use is mostly academic.

**Concerns, most serious first**
1. **Little headroom; one feature dominates.** IDH1 alone separates most cases: 391 of 414 IDH1-mutated cases are LGG. Mean AUC over 3-fold CV:
   - Logistic regression on all features: 0.920
   - LightGBM: 0.905
   - IDH1 plus age only: 0.902

   Expect method differences inside the noise of a fold with about 290 test rows. Change: keep the dataset, but give it low weight or treat it as a small-data or sanity task.
2. **Cohort and labelling questions.** The rows come from two separate TCGA projects, and the project equals the label. Batch differences in sequencing or curation between TCGA-GBM and TCGA-LGG may add part of the signal. The grade follows pre-2016 WHO histology. Under WHO 2021, IDH-mutant "GBM" no longer exists, so 23 rows are differently defined today. I could not check how much batch effect there is.
3. **Preparation.**
   - This is the 862-row "original" file. The UCI preprocessed version has 839 rows: 23 rows with missing Gender, Age or Race were dropped.
   - Here the missing values are NaN: Race 22, Age 5, Gender 4. That is fine and arguably better than dropping the rows.
   - Project, Case_ID and Primary_Diagnosis are absent, which is correct: Primary_Diagnosis would leak the grade.
   - Race has a 1-row level ("american indian or alaska native"). That is harmless.
   - The types are correct: categoricals plus float age.
4. **Duplicates.** There are no duplicate feature rows. Age has day-level precision, so it acts as a quasi-identifier, but I found no copies across train and test.

**Split**
A random IID split with 10 repeats x 3 folds is right for one row per patient.

**What I could not check**
- TCGA case IDs, so I could not confirm one row per patient.
- How Kaggle and OpenML 46604 derived the data, beyond the UCI page.
- Batch effects between the two projects.

</details>

<details><summary>Precedent check</summary>

**Precedents: glioma_grading_clinical_and_mutation_features (precedent checker, 2026-10-20)**

Inputs: the decision register (808 decisions, 4 flags), the record, `dataset.py`, the earlier REVIEW.md,
the checklist, the Cases tables of `use_case.md`, `selection.md`, `cleaning_features.md`, `task_probes.md`,
`provenance.md`, `splits.md`, sibling records (`grep -il "tcga|glioma|glioblastoma" curation/records/`: glioblastoma,
lgg_low_grade_glioma, coad_colon_adenocarcinoma, tcga_coad_molecular_subtype, ov_ovarian_cancer, sarcoma,
tcga_kidney_cancers) and the `fit` of the clinical-diagnosis definitions in the working copy.

None of the register's four flags (few_minority, one_feature, scaling drift, trivial) involves this dataset. The register
holds two decisions on it: the AI assessment of 2026-10-07 and the open issue "IDH1 and age carry most of the signal".
There is no `CC` line by the curator on this record, so no curator drift on it can be checked. The 2026-10-07 review
page's marks (artifact db) were not readable from here. If it holds a mark on this record, compare it with the items
below.

**Summary**

| # | Decision | Verdict | Closest precedents |
|---|---|---|---|
| 1a | Keep the TCGA-era histological label (open issue 1) | consistent, with one pair to confirm | heart_disease_cleveland, eryhemato (old clinical labels, shipped); corporate_credit_rating (USE-5, retired 2026-10-16) |
| 1b | `fit="direct"` while `fit_reason` names a label gap | departs without a stated reason | sarcoma (approximate, 2026-10-20); coffee_rating_prediction (approximate, Lennart 2026-10-14) |
| 1c | Use case "a check on the tissue diagnosis" | departs without a stated reason | eryhemato (USE-4), lung_cancer_epithelial_genexp, sdss_17, breast_cancer_prediction |
| 2 | Keep the 23 patients with missing demographics (862 rows) | consistent | CLEAN-11 cases (caracas, churn_telco_south_asia, heart_disease_va_long_beach), PROV-15, USE-7 (not triggered) |
| 4 | Keep despite IDH1 + age carrying most signal | consistent | TP-4: sepsis_survival, california_house_prices_2020, expresso_churn_prediction_1m, aps_failure (kept); fitness_club (retired) |
| - | Label validity against the TCGA siblings (SEL-4, SEL-5) | consistent | glioblastoma, ov_ovarian_cancer, brca_breast_cancer (SEL-4, No, 2026-10-12); coad (copy number dropped, 2026-10-12) |
| - | Uniqueness (PROV-6/7) | consistent | parkinsons pair, amex pair (PROV-7); siblings retired anyway |
| - | IID split with the site as a hidden group | consistent; evidence weaker than the sibling's | sarcoma REVIEW issue 4 (site-grouped measurement, 2026-10-20) |
| - | Use of the original 862-row file over the authors' 839-row file | consistent | PROV-15 (OpenML 43838), PROV-13 cases |

**1a. The label: TCGA-era histology, partly renamed by WHO 2021 (USE-5, SEL-3)**

* **Follows:** SEL-3 accepts "an observed outcome or an expert annotation". The histological diagnosis is an expert
  annotation. It differs in kind from the TCGA siblings excluded under SEL-4 (glioblastoma, ov_ovarian_cancer,
  brca_breast_cancer; Lennart, 2026-10-12: "we do not benchmark labels that come from unsupervised learning"). Old
  clinical labels have shipped as direct tasks: heart_disease_cleveland (1988 or earlier; `CC` 2026-10-06 keep,
  assessment 2026-10-14), eryhemato_squamous_disease ("It is small and old", fit direct), ljubljana_primary_tumor. The
  `Outdated` marker alone has not excluded a dataset since 2026-07-27. The 2026-10-19 consistency check on
  first_order_theorem_proving questioned a `No` on `Outdated` alone. Keeping this label follows these cases.
* **SEL-5 / the coad precedent (not triggered, but it binds the alternative):** coad_colon_adenocarcinoma (Lennart,
  2026-10-12) dropped the copy-number block because copy number defines CIN against GS. The current label is
  histological, and IDH1/IDH2 do not compute it: AUC without them is 0.888 / 0.893 against 0.92. So SEL-5 does not
  apply. The rejected alternative, a WHO-2021 relabel, would make IDH status part of the rule ("glioblastoma" =
  IDH-wildtype). Under the coad precedent and SEL-5, IDH1/IDH2 would then have to go. That is one more reason the relabel
  is a new dataset (PROV-14), as the earlier REVIEW.md says.
* **Pair to confirm, USE-5:** corporate_credit_rating was retired (Lennart, 2026-10-16) because 17% of the checkable
  labels were not the target the actor acts on (the issuer rating). Here, too, part of the label is not what a
  neuro-oncologist acts on today, the WHO 2021 integrated diagnosis. 25 IDH-mutant GBMs are renamed (their grade 4
  stays), and an unknown share of the 87 IDH-wildtype LGGs, at most about 10% of the rows, would become
  glioblastomas. The definition already states the fact that sets the case apart. In credit_rating the labels were
  wrong for their own date: the release mixed instrument ratings, damage that could be repaired from the origin
  (PROV-13). Here the labels were right under the criteria of their time, and a relabel needs markers the source never
  had. This case has an evident distinguishing fact and is no unexplained departure. The curator should confirm it,
  because it fixes how USE-5 reads a changed classification. No Cases row covers that yet. If confirmed, it is a new
  row of the Tensions table or of USE-5's Cases ("a label correct under the criteria of its era, renamed later:
  kept with a note").

**1b. Fit "direct" with a named label gap (USE-8, USE-9)**

`fit_reason`: "The grades follow the histological criteria of 1989-2013; WHO 2021 regrades some of these tumours with
markers the data lacks." USE-8 calls direct the case where "the rows, the features, the label's timing and the split
mirror the use case", and approximate "a stand-in with a known gap, named as such". The fit_reason names a known gap.

* sarcoma (TCGA sibling, panel 2026-10-20, applied): set to approximate because "a closed set of five expert-confirmed
  types ... stands in for a classifier that faces every referred sarcoma". Its gap is in the label and the population,
  like this one's.
* coffee_rating_prediction (Lennart, 2026-10-14): approximate because "one judge ... stands for the rating a buyer meets".
  That is a label stand-in.
* Against: heart_disease_cleveland and eryhemato are direct and old. But their fit_reason names no change in what the
  label means, only age and size.

No fact is written that makes this gap not a gap. The reflection prompt is below.

**1c. The use case "as a check on the tissue diagnosis" (USE-1, USE-3, USE-9)**

In the written use case the label, the tissue diagnosis, already exists at the prediction point. Every diagnostic
precedent places the prediction before the label is known: eryhemato (USE-4: clinical features before the biopsy),
lung_cancer_epithelial_genexp ("before the diagnosis is known"), sdss_17 (photometry for objects without spectra),
breast_cancer_prediction (at the screening read). The 2026-10-20 priority judgment
also says "'check on diagnosis' is ours" (use case 0). USE-9's weighed factor
warns against "a use case rephrased only to excuse a gap". USE-1 allows our own use case marked "for example", and
the text does that. So this is no rule violation, but it has no precedent. The written prediction point is weak, and
the checklist marks P3 as a concern.

**2. The 23 patients with missing sex, age or race (CLEAN-10, CLEAN-11, USE-7, PROV-15)**

Consistent. CLEAN-11: "A row leaves only when it is no task row (USE-7) or a copy". Missing demographics are not the
input the prediction acts on, so USE-7 (bias_correction, Lennart 2026-10-15) does not apply. `--` and `not reported` to
NaN follows CLEAN-10. The kept rows follow caracas_cervical_cancer, churn_telco_south_asia and
heart_disease_va_long_beach (rows stay, values missing). Matching OpenML 46604 is no reason under PROV-15: copies carry
their own choices, as with OpenML 43838 for account debt. The alternative (dropna to 839) would depart from CLEAN-11
without a fact that sets the case apart. Missingness carries no label (0.500), so nothing argues for dropping. One
minor point: the note says 4 patients have `--`, but age has 5 missing (checklist, "Notes match the code").

**4. IDH1 and age carry most of the signal (TP-4, TP-2)**

Consistent. TP-4: "the natural core of a task ... is expected to dominate", and `Trivial` needs the raw feature to match
the methods fold by fold. Kept cases with a dominant natural core: sepsis_survival_minimal_clinical_records (age alone
0.704 against 0.707, Lennart 2026-10-06), california_house_prices_2020 (listed price, 2026-10-06), expresso (REGULARITY
0.890, 2026-10-07), aps_failure (2026-10-06). The retired case, fitness_club (2026-10-05), had one feature above all 37
configurations. Here IDH1 alone (0.860) is well below the methods (0.92), there is no `one_feature` flag, and the
headroom is larger than sepsis'. The register's flag 2 (one_feature opposite outcomes) is a pair of other datasets and
does not bear on this one. No tuned results exist. The coil_2000 and aps cases used tuned BeyondArena results to settle a
flag, but here no flag needs settling.

**Other points checked**

* **Uniqueness (PROV-6, PROV-7):** shares patients with lgg_low_grade_glioma (240/247) and glioblastoma (180/274), with
  other targets. This follows PROV-7 (parkinsons pair, amex pair). Both siblings are `No` (glioblastoma SEL-4,
  2026-10-12; lgg_low_grade_glioma Data Quality Issue, 2026-10-16), so no shipped dataset overlaps. The curation note
  could say so. It describes them as live tasks ("predict molecular subtypes"), which is out of date (writing.md). The
  checklist's P5 concern resolves to consistent.
* **The TCGA siblings' failures do not recur:** no clustering label (SEL-4 cases), no feature scaled over all patients
  (coad 2026-10-16 retired; sarcoma and lung_cancer_epithelial_genexp kept with notes 2026-10-19; register flag 3 is
  about those, not this), no rows of other patients (lgg). The mutation flags are per-patient calls checked against
  the GDC.
* **Split (SPLIT-3, USE-11, hidden site group):** IID with one row per patient follows breast_cancer_prediction
  (USE-11, Lennart 2026-10-15) and lung_cancer_epithelial_genexp. The tissue site is the same hidden group as
  sarcoma's REVIEW issue 4 (open, 2026-10-20). There the mediator measured the hospital fingerprint from the features
  (ROC AUC 0.70-0.75) and site-held-out log loss over three seeds. Here the evidence is one logistic-regression AUC from
  the earlier run (0.919 against 0.918, not re-run). The outcome is consistent: each site sent patients to one project,
  but the features do not carry the site. For like treatment, measure it the way sarcoma did: site from features, and
  site-grouped against random with a random forest over seeds. Whatever Lennart decides on sarcoma issue 4 should be
  checked against this dataset.
* **Source file (PROV-8 to PROV-15):** the original 862-row file of the UCI release rather than the authors' 839-row
  coded file. This follows the "repair from the origin" line (PROV-13 cases: SUPPORT2, ashrae) and PROV-15.
* **Third exception:** none. No exception is recorded on this dataset, so no rule reaches a third exception of the same
  kind.
* **Writing:** the earlier REVIEW.md numbers its issues 1, 2, 4. Issue 3 is missing with no note on where it went.

**Reflection prompts for the curator**

**Consistency check (AI, 2026-10-20):** the definition sets `fit="direct"` while its own `fit_reason` names a known gap
(grades by the 1989-2013 criteria; WHO 2021 regrades some tumours with markers the data lacks). sarcoma (2026-10-20,
review panel, applied) is `approximate` for a gap in the label and population, and coffee_rating_prediction (Lennart,
2026-10-14) for a label that stands in for the one the actor meets. What sets this case apart?
(a) The gap changes the grade of at most about 10% of rows (the 25 IDH-mutant GBMs keep grade 4), and the task is
grading by histology, which is still part of the integrated diagnosis. Recorded as the reason for direct.
(b) Treat it like sarcoma: set `approximate` ("a histological grade of its era stands in for today's integrated
diagnosis").
(c) Reopen sarcoma's and coffee_rating's fit to match this one.
(d) Change USE-8: a label correct under the criteria of its time counts as direct (an amendment).

**Consistency check (AI, 2026-10-20):** the use case places the prediction after the tissue diagnosis ("as a check on
the tissue diagnosis"), so the label is already known at the prediction point. Every diagnostic precedent predicts
before the label exists: eryhemato_squamous_disease (before the biopsy, USE-4), lung_cancer_epithelial_genexp (before
the diagnosis), sdss_17 (objects without spectra), breast_cancer_prediction (at the screening read, Lennart 2026-10-15).
What sets this case apart?
(a) There is a setting where the mutations are known and the histology is not, such as a small stereotactic biopsy
that is not enough for a histological grade but is enough for sequencing. If so, rewrite the use case to that setting
(USE-9), and record it.
(b) Treat it like the precedents: if no such setting holds, the use case is weak, and the record's use-case judgment
stays "-" (priority and the P3 concern).
(c) Accept a cross-check use case as a kind of its own and add it to USE-1's Cases.
(d) Change USE-1 or USE-3 to allow a use case whose label is known at the prediction point (an amendment).

**Confirmation (AI, 2026-10-20), not a departure:** keeping a label correct for its era but renamed by a later
classification (issue 1) differs from corporate_credit_rating (USE-5, retired 2026-10-16). There the labels were wrong
for their own date and could be repaired from the origin. Confirm that difference as the reading of USE-5 for a changed
classification, and record it as a Cases row so the next TCGA-era label (for example a tcga_kidney_cancers rebuild)
is decided alike.

</details>

<details><summary>Advocate</summary>

**Advocate: opening brief, glioma_grading_clinical_and_mutation_features (2026-10-20)**

Position: ship. The task is valid and leak-free, the split is right, the data is faithful, and it has value. Two parts
of the metadata do not hold as written (the fit and the use-case wording), and four claims need rewording. The mildest
remedy for each is an edit to the text of `dataset.py`. None changes the data, the features or the split.

**1. Honest evaluation holds: no leak left, and the split mirrors the use case (P4; LEAK-10, LEAK-16, SPLIT-1, SPLIT-29, all Must)**

* Evidence: the three columns that give away the label are dropped: `Project` (862/862 equal to `Grade`, and `_clean`
  raises if this ever changes), `Primary_Diagnosis` ("Glioblastoma" 360 GBM, 0 LGG) and `Case_ID` (45 sites, each
  with one label). Every one of the 23 kept columns is known once the tumour is sequenced (column audit: "every column
  fine; no leak or cleaning fix required"). Missingness carries no label (indicator AUC 0.500). The data has 0
  duplicated rows and 0 test rows copied from train over 30 splits. There are 862 unique patients.
* Hidden site group (SPLIT-29): the features do not identify the site, scoring below the majority rate within each
  grade (LGG 0.175 vs 0.214, GBM 0.317 vs 0.338). Mean per-fold AUC under site-grouped folds is LR 0.921 and RF 0.927,
  against 0.921 and 0.924 on the shipped split. SPLIT-29 is not triggered.
* Answers: the sequencing-batch confound (LEAK-13, LEAK-15). Both rules need a measured effect. LEAK-15 needs "batch
  noise across the whole feature space", and the column audit rates it "weak and untested". The evidence goes against
  it: the flags are the GDC's harmonised calls (17,220 of 17,240 cells match the API), all from WXS. The signal is
  textbook biology (IDH1, CIC, FUBP1 and NOTCH1 in LGG; PTEN and EGFR in GBM). The 70 rows with no flag set have 3 to
  110 calls elsewhere. Remedy if pressed: the column auditor's one-sentence note that the classes come from two
  separately sequenced projects (keep with a note), not exclusion.

**2. The label is a valid expert annotation, correct for its era (P3; SEL-3, USE-5, Must)**

* Evidence: `Grade` is the histological diagnosis (GDC tumor_grade: LGG G2 238, G3 259; GBM 360 "Glioblastoma"),
  from 858 dated diagnoses in 1989-2013. The label is not computed from the features: without IDH1 and IDH2 the AUC is
  RF 0.892 and LR 0.883-0.888, against 0.92 with them (claim 26, re-run). So SEL-5 does not apply.
* Precedents: old clinical labels have shipped (heart_disease_cleveland, eryhemato, ljubljana_primary_tumor). This case
  differs from corporate_credit_rating (USE-5, retired): those labels were wrong for their own date and could be
  repaired from the origin. These are right under their era's criteria, and a WHO-2021 relabel needs markers the
  source never had (CDKN2A, TERT, +7/-10). The relabel would also make IDH part of the label, so IDH would have to go
  (the coad precedent). That makes it a new dataset, not a fix (PROV-14).
* The WHO 2021 change is bounded. The 25 IDH-mutant GBMs keep CNS WHO grade 4, so only some of the 87 IDH-wildtype
  LGGs (at most about 10% of rows) could change grade. The practitioner agrees: "None of these is a leak or makes the
  task unreal; they argue for fit approximate, not rejection." This is a framing question for point 3, not a validity
  failure.

**3. Concede: set fit to approximate (USE-8, Must). This is a one-word change, not a reason to hold the dataset**

* `fit_reason` names a known gap itself, and USE-8 defines that as approximate: "a stand-in with a known gap, named
  as such". The precedents (sarcoma 2026-10-20, coffee_rating_prediction 2026-10-14) and the practitioner all say
  approximate. I have no fact that sets this case apart. Precedent option (a), "only about 10% change", is a number,
  not a different kind of case.
* Remedy: `fit="approximate"`, with `fit_reason` saying that a histological grade from 1989-2013 stands in for
  today's WHO 2021 integrated grade. This is the rung "fix the definition". Approximate fits ship (account_debt, kick,
  alfa_battle).

**4. The use case is real; only its wording should change (P3; USE-1, USE-3, Must; USE-9, Should)**

* Evidence: it is the source's own published task. The paper grades LGG vs GBM with 10-fold CV and reports AUC
  0.908-0.920 (claim 36), so SEL-3 holds. The practitioner names a real use: "a consistency check of histology
  against the mutations (or filling missing grade annotations in a genomic registry)". USE-3 is met: the prediction
  point is "after sequencing", and no feature carries the histology (point 1).
* Concede: grading from mutations alone is not the primary decision. The histology exists before sequencing, and no
  diagnostic precedent sets the prediction after the label. I do not claim the stereotactic-biopsy setting; it is
  untested. Remedy: reword `use_case` as the practitioner suggests ("a neuropathology lab checks a histological grade
  against the tumour's mutation profile"), together with fit approximate. USE-9 then does not apply, because the fit
  is not claimed as direct. This edits the text; USE-2 (no decision fits) is not triggered.

**5. Worth benchmarking: a dominant feature is expected here, and the methods spread (P6; TP-4 Must, TP-2 Should)**

* Evidence: IDH1 alone gives 0.860 and IDH1 + age 0.902, against 0.92 for all features. RF 0.922, LR 0.919 and
  untuned LightGBM 0.897-0.905 spread. No `one_feature` or `trivial` flag was raised. IDH1 is the natural core of
  glioma grading, which TP-4 says "is expected to dominate". The precedent is sepsis_survival (age 0.704 against
  0.707), kept with less headroom than this.
* The blind reviewer, with no notes: "Include. The task is real and leak-free ... a low-weight, small-data member."
  Per TP-2, a small signal is no reason to retire.

**6. Faithful, unique data, repaired from the origin (P5; PROV-3, PROV-8, PROV-13, PROV-15; P7 CLEAN-11)**

* Evidence: the sha256 of the original file matches. The 20 flags match the GDC API in 17,220 of 17,240 cells, and
  the ages match the GDC day count within 0.75 days. We read the original 862-row file, not the authors' 839-row
  coded file (OpenML 46604). This keeps 23 patients with missing demographics (12 LGG, 11 GBM, no label signal), as
  CLEAN-11 and its precedents ask (caracas, churn_telco_south_asia, heart_disease_va_long_beach). Uniqueness (PROV-7):
  the overlapping TCGA siblings are both retired, so nothing shipped overlaps.

**7. Concede: four writing errors, fixed in the notes (writing.md; P7)**

* "the 20 genes mutated most often" is refuted. TTN is 4th, and the 20 are the most often mutated Cancer Gene Census
  genes (claim 5). Reword `known` and the intro: "the 20 cancer-census genes mutated most often in these patients
  (the GDC portal's list)". The selection is still label-free (claim 22, LEAK-30 holds).
* "`--` (4 patients without a clinical record)" should say "and the age of one more" (5 ages are missing; claim 24).
* The sibling-overlap note is stale. Say both siblings are retired, or drop the note.
* The site-split AUC should say "mean per-fold ROC AUC" (split audit problem 1).

None of these changes the data or a verdict. They are quality fixes, cheap and safe (principles step 3).

**Judgment the advocate asks for:** ship after changes, all of them text in `dataset.py`: fit approximate, the
use-case wording, and the four writing fixes. Validity: SEL-3, USE-5, LEAK-10, SPLIT-1 and SPLIT-29 hold. USE-8 is
fixed (approximate). Value: TP-4 is not triggered; TP-2 keeps a small real signal. Quality: the 862 rows are kept
(CLEAN-11).

**Advocate: rebuttal, glioma_grading_clinical_and_mutation_features (2026-10-20)**

The critic and I agree on the verdict: ship after changes, with no exclusion asked. We also agree on the split
(SPLIT-1, SPLIT-29), the value (TP-4, TP-2) and the 862 rows (CLEAN-11). What remains is which remedy to use on
points 1 and 4.

**Critic 1: the prediction point comes after the label exists (USE-1, USE-3): concede the problem, dispute one remedy**

* Conceded: as written, the label is known at the prediction point, and no diagnostic precedent does that
  (precedents 1c). My brief, point 4, already asks to reword `use_case`.
* Disputed: writing the stereotactic-biopsy setting into the definition. No agent tested it: there is no source, and
  nothing in the data separates biopsies from resections (EV-6, EV-7: a claim without a test is a question). Writing it
  as the use case would be "a use case rephrased only to excuse a gap" (USE-9's factor against). The registry use
  ("filling missing grades in a genomic registry") comes from the practitioner, but it is also untested.
* What follows: reword `use_case` to the cross-check the source's task supports (the practitioner's wording), with
  `fit="approximate"`. Which use case to write, and whether USE-1 admits a cross-check, goes to the curator, as the
  critic says.

**Critic 2: fit direct while fit_reason names a gap (USE-8): concede**

The same remedy as my point 3: `fit="approximate"`. I accept the critic's longer `fit_reason`, which adds the
missing markers and "the mutations are known after the histology". Every phrase in it is backed (practitioner
section 1; claim audit #9).

**Critic 3: the label is not today's target (USE-5): concede the remedy, which matches my point 2**

* We agree: keep the label. The distinguishing fact from corporate_credit_rating (correct for its era, not repairable
  from the origin) goes to the curator to confirm as a USE-5 Cases row.
* Conceded: the note should say that grade II and III are merged in LGG (claim audit #4: G2 238, G3 259).
* One limit on the effect: the 25 IDH-mutant GBMs keep grade 4 (claim #41), so the part of the label that changes is
  a subset of the 87 IDH-wildtype LGGs plus the 128 mixed gliomas. The mixed gliomas lose their entity name, not
  necessarily their grade class. The share is untested (#9), so I claim no number beyond "at most about 10% of rows"
  for the regrading.

**Critic 4: batch, one separately sequenced project per class (LEAK-14, LEAK-15): accept the test, dispute LEAK-14**

* Accepted: the critic's test (passenger-gene rate by sequencing centre within one project) is cheap and decisive.
  Facts first (EV-1). Run it before the note.
* Disputed: LEAK-14 as the rule that follows a positive result. LEAK-14 drops "a class that comes from a separate
  source or assay ... once the paper confirms it". The assay is the same (all 994 files WXS, claim #9), and the paper
  confirms no batch effect. Dropping a class would also end a binary task, so LEAK-14's remedy does not fit this
  case. The rule that applies is LEAK-15 (batch noise across the whole feature space). On the evidence now it is not
  triggered:
  * The signal is textbook biology.
  * The flags match the GDC's calls in 17,220 of 17,240 cells.
  * The GBM excess in MUC16, CSMD3 and FAT4 is tumour mutation burden, a property of the tumour that is known at the
    prediction point (column audit problem 2: "not a leak").
* One wording caution: "the GDC re-called both with one pipeline" is not verified in the evidence (claim #29 checks
  agreement with the API, not the pipeline). Write it only after checking.

**Critic 5: three refuted or stale facts: concede**

These are the same as my point 7: the gene-list wording, "and the age of one more", and the retired siblings.

**Critic 6: the site-split note: concede**

The same as my point 7: "mean per-fold ROC AUC", plus the split audit's numbers (site from features below the majority
rate; site-grouped RF 0.927 against 0.924 on the shipped split).

**Settled between us:** ship after changes. Points 2, 5 and 6 and the note in point 3 are edits that need no curator.
The test in point 4 runs first. The curator decides the use case wording (point 1) and confirms the USE-5 reading
(point 3).

</details>

<details><summary>Critic</summary>

**Critic: glioma_grading_clinical_and_mutation_features (opening brief, 2026-10-20)**

**Position: ship only after changes.** No point below is grounds to exclude: the task is real, leak-free on the
evidence, and its split is right. But the definition misstates its own prediction point and fit, and three of its
facts are wrong or stale.

**1. The prediction point comes after the label exists (P3; USE-1, USE-3, Must)**

* Problem: `use_case` says the care team assigns the grade "as a check on the tissue diagnosis". The label *is* the
  tissue diagnosis (Grade = TCGA project = histology; claim audit #16, #28). So at the written prediction point the
  label is already known.
* Effect: the benchmark claims a decision nobody makes as stated ("assigns the grade from the mutations"); the
  practitioner: "the histology is in hand before the sequencing ... grading from mutations alone is not a decision
  anyone makes, only a check" (practitioner gap 2).
* Evidence: claim audit #2, #8, #15 untested, flagged; precedents 1c: every diagnostic precedent (eryhemato,
  lung_cancer_epithelial_genexp, sdss_17, breast_cancer_prediction) predicts before the label exists; this one has
  no precedent; the priority judgment of 2026-10-20 says "'check on diagnosis' is ours".
* Remedy (fix the definition): rewrite `use_case` and the first curation bullet to a setting where the mutations are
  known and the histological grade is not (a stereotactic biopsy too small to grade but enough to sequence; filling
  missing grades in a genomic registry), if the curator accepts one (USE-9); otherwise record the cross-check as the
  use case and let the curator decide whether USE-1 admits it. Not exclusion: USE-2 does not apply (practitioner).

**2. `fit="direct"` while `fit_reason` names a gap (P3; USE-8, Must)**

* Problem: `fit_reason` itself says the grades follow 1989-2013 criteria and WHO 2021 regrades some tumours with
  markers the data lacks. USE-8: approximate is "a stand-in with a known gap, named as such".
* Evidence: practitioner verdict "approximate"; precedents 1b: sarcoma (approximate, 2026-10-20) and
  coffee_rating_prediction (approximate, Lennart 2026-10-14) for label stand-ins; no fact written that sets this
  case apart. Point 1 adds a second gap (prediction point).
* Remedy (fix the definition): `fit="approximate"`, `fit_reason`: "a histological grade of its era stands in for
  today's WHO 2021 integrated grade, from an exome gene set without TERT, CDKN2A/B, EGFR amplification or +7/-10;
  the mutations are known after the histology".

**3. The label is not the target the clinician acts on today (P3; USE-5, Must)**

* Problem: the actor acts on the WHO 2021 integrated diagnosis (type plus CNS WHO grade 2/3/4); the label is the
  TCGA-era histological project, LGG (grade II+III merged) vs GBM.
* Evidence: the earlier REVIEW.md, issue 1; practitioner section 2: 25 IDH-mutant GBMs renamed (grade 4 kept), an unknown
  share of 87 IDH-wildtype LGGs would be glioblastomas, 128 "mixed glioma" rows are an abandoned entity; claim audit
  #41 holds, the share regraded is untestable here (#9).
* Rule fight: USE-5 is a Must and corporate_credit_rating was retired under it. The precedent checker gives the
  distinguishing fact (labels right for their own era, not repairable from the origin), which I accept, so exclusion
  is not asked.
* Remedy (a note plus a curator confirmation): keep the label; the curator confirms the reading of USE-5 for a
  changed classification and it becomes a Cases row (precedents 1a), so the next TCGA-era label is decided alike.
  The note should also say grade II and III are merged.

**4. Each class is one separately sequenced project; batch is untested (P4; LEAK-14, LEAK-15, Must if strong)**

* Problem: every GBM row is TCGA-GBM, every LGG row TCGA-LGG, sequenced at different times and centres; any
  project-level difference in calling lines up with the label exactly, and probe 7 cannot separate it (no same-label
  group across projects).
* Evidence for concern: blind review concern 2 (raised without our notes); passenger-prone long genes (MUC16,
  CSMD3, FAT4) are about twice as often mutated in GBM (column audit problem 2). Evidence against: GDC harmonised
  calls (17,220 of 17,240 cells match), textbook biology on top, AUC without IDH still 0.888-0.893 is consistent with
  biology. The concern is weak and unmeasured (EV-6: a question, not a finding).
* Remedy (a note, plus one cheap test): within one project, compare the passenger-gene rate by sequencing centre
  (column audit's proposed test). If centre shifts it, LEAK-14 needs the curator; if not, one sentence in the notes:
  "the two classes come from two separately sequenced projects; the GDC re-called both with one pipeline".

**5. Three refuted or stale facts in the notes (P5 / writing; PROV-3, EV-2, Should)**

* "the 20 genes mutated most often in these patients" (`known`, intro) is refuted: TTN ranks 4th (169 patients),
  FLG, RYR2 and others are above most file genes; the 20 are the most often mutated Cancer Gene Census genes, 19 of
  20 reconstructed (claim audit #5, #14). Reword to "the 20 cancer-census genes mutated most often in these patients
  (the GDC portal's list)".
* "`--` (4 patients without a clinical record)": 5 ages are `--` (claim audit #24). Say "and the age of one more".
* The sibling overlap note describes lgg_low_grade_glioma and glioblastoma as live tasks; both are retired (claim
  audit #27, precedents). Drop the note or say they are retired.
* Remedy: wording only.

**6. The site-split note under-states its evidence (P4; SPLIT-29, EV-1, Should)**

* Problem: "0.919 against 0.918" does not say it is mean per-fold AUC; pooled out-of-fold AUC under the site split
  is 0.899 (split audit problem 1), which a reader takes for a gap. The precedent sarcoma measured site from features
  and over seeds; the split audit has now done that here (site from features below the majority rate; RF 0.927 vs
  0.923).
* Remedy (a note): cite the split audit's numbers, "mean per-fold ROC AUC", and "the features do not predict the
  site". No re-split.

Not raised: the small headroom beyond IDH1 and age (TP-4; consistent with sepsis_survival, aps_failure; no flag), and
keeping the 23 patients with missing demographics (CLEAN-11; consistent). Both are fine.

Judgment record asked for:

```text
Verdict: ship after changes.
Validity: USE-1/USE-3 triggered, fix the use case (point 1); USE-8 triggered, fit approximate (point 2); USE-5 kept
  with a note and a Cases row (point 3); LEAK-14/15 untested, one test then a note (point 4); SPLIT-1 holds.
Value: TP-4 holds (keep).
Quality: notes corrected (points 5, 6).
For the curator: point 1 (which use case), point 3 (the USE-5 reading).
```

**Critic: rebuttal to the advocate (2026-10-20)**

We agree on the verdict, ship after changes, and on most of the changes. Two points stay open, both curator calls:
the use case (A4) and the USE-5 Cases row (A2).

**A1. Honest evaluation holds (LEAK-10, LEAK-16, SPLIT-1, SPLIT-29): concede, including the batch remedy**

* Concede the split and the leaks. The split audit settles SPLIT-29 (site below the majority rate, site-grouped
  per-fold AUC 0.921/0.927 vs shipped 0.921/0.924).
* Batch (my point 4): concede that the remedy is the note. LEAK-15 needs noise across the whole feature space, and
  nothing measured shows it. LEAK-14 is about a class from a separate *assay*. Here both classes are WXS, and the GDC
  re-called both with one pipeline (claim audit #9, #19, #29). EV-6 makes my concern a question, not a finding. The
  within-project test by sequencing centre stays optional, for the curator, and does not block shipping. The note
  should say both things: the classes are two separately sequenced projects, and the GDC harmonised the calls.

**A2. The label is valid for its era (SEL-3, USE-5): concede the keep, dispute that nothing else is needed**

* Concede: the label stays. The fact that sets it apart from corporate_credit_rating holds: right under the criteria
  of its era, and a relabel would be a new dataset (PROV-14, the coad precedent on IDH).
* Dispute: this is the first reading of USE-5 (Must) for a classification that changed later, and no Cases row
  covers it (precedents 1a). Under "treat like cases alike", the curator confirms it once and it becomes a Cases row,
  so the next TCGA-era label (tcga_kidney_cancers) is decided the same way. The advocate's brief leaves this out.
* Also: the note should say that grades II and III are merged (practitioner section 2). It is one clause.

**A3. Fit approximate (USE-8): agreed**

Same remedy as my point 2. Settled.

**A4. The use case is real; only its wording changes (USE-1, USE-3, USE-9): partly dispute**

* Concede: SEL-3 holds (it is the source's task), USE-2 is not triggered, and no feature carries the histology. I
  also accept that the stereotactic-biopsy setting is untested, so I do not ask for it as a fact.
* Dispute: the advocate's rewording ("a neuropathology lab checks a histological grade against the mutation
  profile") states the problem but does not settle it. At that prediction point the label already exists, and the
  precedent check found no diagnostic precedent for this (eryhemato, lung_cancer_epithelial_genexp, sdss_17,
  breast_cancer_prediction all predict before the label). The priority judgment of 2026-10-20 calls the cross-check
  "ours". Calling the fit approximate names the gap but does not answer USE-1 (Must): is a cross-check against a
  known label a decision? Rules win over wording. This is the precedent checker's reflection prompt (options a-d),
  and only the curator can answer it.
* Remedy: use the advocate's wording, with fit approximate, and put the USE-1 question to the curator as an issue. If
  the curator accepts the cross-check as a kind of use case, it becomes a USE-1 Cases row (option c).

**A5. Worth benchmarking (TP-4, TP-2): concede**

I did not raise it. The sepsis_survival and aps_failure precedents apply, and no flag was raised.

**A6. Faithful data, 862 rows (PROV-3, PROV-8, PROV-15, CLEAN-11): concede**

The checksum matches, the flags match the GDC, the ages are within 0.75 days, and the kept rows carry no label
signal. The one refuted fact about the genes is under A7.

**A7. Four writing fixes: agreed**

These match my points 5 and 6, so they are settled. To add to the site-split note: "the features do not predict
the site" (split audit).

Judgment the critic now asks for:

```text
Verdict: ship after changes.
Validity: SEL-3, LEAK-10, SPLIT-1, SPLIT-29 hold; USE-8 fixed (approximate); USE-5 kept, curator confirms as a Cases
  row; USE-1 cross-check use case, curator call; LEAK-14/15 untested, kept with a note.
Value: TP-4 holds.
Quality: notes corrected (genes, 5 ages, retired siblings, per-fold AUC, II+III merged, batch note).
For the curator: the USE-1 question (A4); the USE-5 reading (A2); optional centre test (A1).
```

</details>
