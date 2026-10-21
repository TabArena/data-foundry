# differentiated_thyroid_cancer_recurrence

**Outcome:** added. UCI's 383 thyroidectomy patients of one clinic in Hamadan as a binary task: recurrence during
follow-up, predicted at the initial staging (ROC AUC), on a random split of patients, without the response to therapy
and the radiotherapy column. Verdict (mediator): ship. Validity: SEL
holds; USE-1 holds with the use case worded as the decisions taken at the staging visit; USE-5 holds under either
reading of the label; USE-8 met with `fit="approximate"` (the gap: the label's breadth and horizon unverified, which
makes a fit approximate under USE-8 as amended on 2026-10-21; `M` kept as a potential leak and one clinic are named too); LEAK-10 triggered and fixed (`Response`
dropped); LEAK-6: `M` and `Risk` kept with `Potential leak, kept on purpose:` notes (+0.001 and at most +0.010 ROC
AUC); LEAK-18 and LEAK-20: duplicates kept as distinct patients (p = 0.166); LEAK-10 and LEAK-6: `Hx Radiothreapy` dropped, a
weighing call left open (issue 6); LEAK-22 and LEAK-36: the 34 patients at high risk of the American Thyroid Association (ATA) or with distant metastases
(M1) kept, a cohort question open until the paper is read (issue 2); LEAK-24 cannot be tested and is written as
the source's claim; SPLIT-1 holds. Value: not `Trivial` (TP-4: a random forest beats the risk class alone on 59 of 60
splits, mean gain 0.032); not too small (TP-5: 36 positives per test fold). Quality: the `Hurthle` typo fixed, the 12
rows whose `Stage` disagrees with the stage computed from age, T, N and M kept as recorded (CLEAN-11). Weighed: a real clinical decision and clean provenance (the file's
checksum matches, the rows match the paper's cohort) for; one clinic and 383 patients against.

**Main points:** Read the paper to settle the label and the cohort (issue 2); drop or keep `Hx Radiothreapy`
(issue 6); remove the `Trivial` marker (field row). Of the two rule questions from this review in the Across datasets
view, USE-8 and an unverified label is answered by rule (2026-10-21, Lennart: USE-8 amended, an unverified label
definition makes the fit approximate, a kept potential leak alone does not); thyroid_discordant's `Trivial` stays there.

**Record fields that disagree with the definition:**

- `decision_markers`: record `Trivial`, definition `none (a random forest beats the risk class alone on 59 of 60 splits)`.

**Record judgment:** valid, with one Must check open: what the label counts and which cohort the paper used (LEAK-22,
issue 2). The record's `Trivial` marker came from the paper's ROC AUC 0.984-0.997 on all features, which probably
include `Response`; without it the TP-4 test refutes the marker (field row). Dropping `Response` is right: it is assessed in the first two years of follow-up, and 89 of its 91 "structural
incomplete" patients recurred.

**Issues for Lennart:**

2. **What does `Recurred` count? Keep the 34 high-risk or M1 rows meanwhile?** The Borzooei et al. 2024 PDF settles
   the label.
   - Problem: the label probably counts persistent disease (cancer that never cleared after the first treatment), not
     only cancer that came back after remission. All 32 patients in the high-risk class of the American Thyroid
     Association (ATA) and all 18 with distant metastases (M1) are labelled recurred, 34 patients in all. Recurrence
     is 4.8%, 62.7% and 100% in ATA low, intermediate and high risk, against about 3%, 21% and 68% of persistent or
     recurrent structural disease in Tuttle et al. 2010. If the label counts persistent disease, these 34 patients
     may already have the outcome at the staging visit where the task predicts.
   - Effect: on 20 x 3 stratified folds, logistic regression scores ROC AUC 0.928 on all test rows and 0.901 without
     the high-risk or M1 test rows; the risk class alone 0.896 and 0.850. Leaving out as many other positives that the
     model ranks highest also gives 0.901, so these rows are easy, not leaked (mediator's measurement). What is at
     stake is which patients the benchmark asks about, not the score.
   - Cohort: the file's 383 rows match the paper's abstract (383 patients, mean age 40.87, SD 15.13, 81% women; claim
     audit), so the paper's cohort includes these 34 patients unless the PDF says otherwise.
   - Follow-up: the source states at least 10 years of follow-up for every patient, but the cohort paper gives the
     period January 2008 to December 2023 (Khazaei et al. 2024,
     [PMC11492527](https://pmc.ncbi.nlm.nih.gov/articles/PMC11492527/)), so the "No" of the later patients may be
     censored (not yet observed rather than absent). Without dates this cannot be tested (LEAK-24).
   - Evidence of the paywall: the [Springer page](https://doi.org/10.1007/s00405-023-08299-w), its Wayback snapshot
     (2025-12-29) and Europe PMC (PMID 37902840) show only the abstract; ORBi UMONS and ORBi ULiège serve "Request a
     copy". Khazaei et al. 2024 do not define recurrence ("mainly local involvement").
   - Rule: USE-5 (Must: check how the source built its label), LEAK-22 (Must: follow the paper's cohort), LEAK-36
     (Must: a value known at prediction time that rules the outcome out is a cohort question, not a feature leak),
     PROV-17 (Must: when a paywalled paper matters and no free copy turns up, say so and ask the curator).
   - Implemented: the rows are kept, with `Note:` bullets on the label (with the rates against Tuttle 2010), on the 34
     rows and on the follow-up; the fit is approximate.
   - The critic: LEAK-22 says follow the paper's cohort, and we do not know it. The advocate: the ATA risk class
     exists to stage exactly these patients, and either reading of the label is the "persistent/recurrent disease"
     that the ATA initial risk estimates (ATA 2015 guidelines, recommendation B19).
   - Precedent: shipping with the label unverified follows churn_telco_south_asia (2026-10-15) and thyroid_discordant
     (both `approximate`); the cohort reading follows diabetes_130_us, the case of LEAK-22 to which LEAK-36 refers.
   - What to check in the PDF: the definition of recurrence and whether persistent disease counts; whether the cohort
     excludes patients whose disease never cleared; when `Risk` and `M` were recorded; which 13 features the paper
     used (the file has 16); the follow-up period. A web search for the title with "pdf" may find a copy.
   - Alternatives: (a) keep the 34 rows with the notes, at the cost of a cohort that may differ from the paper's;
     (b) if the paper's cohort excludes patients whose disease never cleared, exclude them too (LEAK-22), at the cost
     of 34 of the 108 positives.
   - Recommendation (mediator): keep with the notes until the PDF is read; then (b) if the paper's cohort excludes
     these patients, otherwise (a).
   - Decision needed: keep the 34 rows with the notes now (a). (b) stays possible only if the PDF shows that the
     paper analysed fewer patients than the 383 in the file.

6. **`Hx Radiothreapy`: drop it (implemented) or keep it with a `Potential leak, kept on purpose:` note?**
   - Problem: no source defines or dates the column (the UCI variable table is empty; Khazaei et al. do not list
     radiotherapy among the collected variables). Of its 7 "Yes" rows, 6 are ATA high-risk men, 5 with M1 and 5 aged
     61-81, who all recurred; the seventh is a 25-year-old low-risk woman who did not. That fits radiotherapy for
     advanced disease given after staging, but "Hx" reads as history from before staging (blind reviewer), such as an
     earlier radiotherapy of the head and neck.
   - Effect: none measurable on the 60 shipped splits: logistic regression 0.9219 without and 0.9221 with it, random
     forest 0.9271 and 0.9285. If the column is a history from before staging, dropping it removes a legitimate
     input; if it records treatment after staging, keeping it lets the model see the treatment of advanced disease.
   - Rule: LEAK-10 (Must) if the column is recorded after staging; LEAK-6 (Must: measure before acting; a slight
     optimism with a known cause can stay with a note). A weighing call.
   - For dropping: no definition or date, and 6 of 7 positives look like treatment of advanced disease (practitioner,
     column audit). For keeping: you moved from excluding to keeping with a note for weak leaks (LEAK-30, 2026-10-19);
     LEAK-38 does not apply, because the column is named, not anonymised.
   - Precedent: the earlier drops of a suspected column (2_month_survival_rate_prediction's `adls` and `adlsc`,
     expresso_churn_prediction's `REGION`) had a measured mechanism; this would be the first drop on circumstantial
     evidence alone. If such drops recur, they belong as a sentence under LEAK-6, not as exceptions dataset by
     dataset. The fact that sets the drop apart from the kept `M` is written in the definition: `M` is a defined
     staging field with 2 doubtful values of 18.
   - Alternatives: (a) drop (implemented), at the cost of a column that may be a legitimate history; (b) keep with the
     note, at the cost of a column that may record treatment after staging. Neither changes the score.
   - What would settle it: the paper's definition of the column (issue 2's PDF).
   - Recommendation: none; the panel leaves the weighing to you, and the advocate and the critic accept either.
   - Decision needed: (a) or (b).

**Review panel:** ship after changes (mediator). Claim audit: most claims hold; two wordings refuted and repaired in
the definition (the copies as "the most common record", the effect of the copies as 0.002-0.003), the model counts
named with their models; the label's definition and the follow-up untested. Column audit: no new leak; `Risk` possibly
assigned in hindsight, with a small measured effect; `Hx Smoking` has no stated meaning. Split audit: the random split
is right; the follow-up claim conflicts with the cohort period. Practitioner: a real decision; the use case reworded to
the decisions taken at staging. Blind review: include with changes; main concern a task close to solved by the risk
class. Debate: agreed on the `Response` drop, the split, the duplicates and not `Trivial`; the fit moved to
approximate because `M` is kept as a potential leak; still disputed was whether the unverified label is a second reason,
an Across datasets item (answered 2026-10-21: USE-8 amended, the unverified label is the reason and the kept `M` is not); both sides left `Hx Radiothreapy` to the curator (issue 6). The mediator's issues 1 and 2 are
issues 2 and 6 here; its issues 3 and 4 are the two items under "Rules from the
differentiated_thyroid_cancer_recurrence review" in the Across datasets view. In the other reports, "REVIEW issue N"
means the file before this run: its issues 2 and 6 continue under the same numbers, its issues 1 (`Response`), 4
(duplicates) and 5 (`Stage` and `M`) are agreed as implemented and left out, and its issue 3 is the `decision_markers`
row. The critic's points are settled in the definition, except point 2 (issue 2) and the radiotherapy half of point 3
(issue 6).

<details><summary>Claim audit</summary>

**Claim audit: differentiated_thyroid_cancer_recurrence (2026-10-20, re-check)**

Data: the definition rebuilt through `dataset_io.load(..., built=True)` (origin `rebuilt`, 383 x 15, 60 shipped IID
splits) and the raw `Thyroid_Diff.csv` (sha256 checked). Models: logistic regression (standardised one-hot, and unscaled one-hot as
in the original run), random forest (300/500 trees), HistGradientBoosting as a stand-in for CatBoost (not installed in
either venv). Raw `Response` / `Hx Radiothreapy` were re-attached to the container's reordered rows by matching the
cleaned columns (7 duplicate groups ambiguous; all within low-risk non-recurrent copies). Licence and pretraining overlap
are not evidence and were not tested. The 2026-10-07 analysis was reread.

**Table**

| # | Claim | Source | Test | Result | Evidence | Rule |
|---|---|---|---|---|---|---|
| 1-2 | Question / use case: recurrence after surgery, predicted at initial staging | task_summary | Borzooei abstract (Europe PMC 37902840): "Identifying individual patient recurrence risk is crucial for guiding subsequent management and follow-ups" | holds | abstract wording matches the actor and decision | USE-1, USE-3 |
| 3,6,24 | One row = one patient; 383 patients | task_summary, intro | count; compare to paper abstract stats | holds | 383 rows; mean age 40.87, SD 15.13, 81.5% female = abstract "40.87 +- 15.13 years ... 81%" exactly | PROV-1x, EV-2 |
| 4 | Hamadan, Iran | task_summary | Khazaei 2024 Methods | holds | "specialized endocrine clinic in Hamadan, Iran" | EV-2 |
| 5 | Every patient followed >= 10 years | task_summary, intro | UCI page, Borzooei abstract, Khazaei Methods | holds by source, untested on data | UCI: "each patient was followed for at least 10 years"; abstract: "minimum duration of 10 years within a 15-year timeframe"; Khazaei: enrolled "January 2008 to December 2023", "10-year follow-up data"; no dates in the file, so censoring cannot be checked | EV-7, LEAK-23 |
| 7,9,46 | Target = recurrence during follow-up, seems to include persistence | task_summary, bullet 9 | crosstabs | untested (definition) / facts hold | all 32 High-risk and all 18 M1 recurred; 89/91 structural incomplete; paper paywalled | PROV-17 |
| 8 | 28% recurred | task_summary | count | holds | 108/383 = 28.2% | - |
| 10,16,26 | All 14 kept features known at initial staging | task_summary, fit_reason, bullet 1 | ATA risk vs recorded TNM consistency | holds with a concern | 7 Low-risk patients are N1b (clinical N1 is not ATA low risk); 2 M1 are Intermediate; 100% recurrence in High (Tuttle 2010 reports 68%). Fits either post-hoc risk assignment or a label that counts persistence; no test on the data separates them | LEAK-10, EV-6 |
| 11,40 | Random patients, IID | task_summary, bullet 7 | container regime; look for dates/ids | holds | regime iid, 60 splits; no date or id column, so no temporal or grouped alternative exists | SPLIT |
| 12,13,25,27,28,54,62,63,67 | `Response` is post-prediction and partly the outcome | bullets 1-2, Decision 1, record | crosstab + ablation on 60 splits | holds | Response x Recurred: Excellent 1/208, Structural incomplete 89/91; Response alone AUC 0.978 (LR, RF); Response+Risk 0.988 (LR) vs 16 columns 0.972-0.988 (orig. 0.983-0.987) | LEAK-10, USE-4 |
| 14,29-32,55,72 | Radiotherapy column: 7 Yes, 6 high-risk men all recurred, adds nothing | bullet 3, Decision 2, issue 6 | crosstab; LR/RF with and without on 60 splits | holds | 7 Yes; 6 High-risk male smokers, 5 M1, 5 aged 61-81, all recurred; 7th 25-y low-risk woman, No. LR 0.9219 vs 0.9221, RF 0.9271 vs 0.9285 | LEAK-10, EV-1 |
| 15,17,18 | fit = direct; a few M1 after staging; small task | task_summary | see 42 | holds | 2 of 18 M1 Intermediate | USE-8 |
| 19 | year 2023, UCI | metadata | zip listing | holds | Thyroid_Diff.csv dated 2023-10-31 | - |
| 20-21 | One file, sha256 a2c65f7c...7b44 | download_description | unzip -l, sha256sum | holds | 1 file, hash matches | - |
| 22 | OpenML 46605 = same 383 rows (2025) | download_description | OpenML API | holds | uploaded 2025-02-17, 383 instances, 17 columns, target Recurred | - |
| 23 | Borzooei 2024, 281(4):2095-2104, DOI | bibtex | Europe PMC record | holds | DOI, vol 281, issue 4, pages 2095-2104, 2024 | PROV-10 |
| 33 | "Hurthel" is a typo | bullet 4 | value counts | holds | 20 rows "Hurthel cell"; the cell is Hurthle | CLEAN |
| 34 | Age numeric, rest categorical | bullet 5 | dtypes | holds | Age int64, 13 category | - |
| 35,50 | 26 copies (6.8%), 22 profiles | bullet 6, warning | duplicated() | holds | 26 beyond first, 48 rows in groups, 22 profiles, 6.79% | LEAK-16 |
| 36 | The 383 rows are the paper's 383 patients, so copies are distinct patients | bullet 6 | abstract stats | holds (circumstantial) | exact match of n, mean age, SD, sex share; distinct patients is inference | EV-6 |
| 37 | Copies are low-risk women who did not recur | bullet 6 | crosstab | holds | 48/48 F, Low, No (46 N0, 2 N1b) | - |
| 38,52,70 | Permutation 23.2 vs 27, 95% 17-30, p 0.16 | bullet 6, warning, issue 4 | re-ran 2,000 draws, new seed | holds | mean 23.2, 95% 16-30, observed 27, p 0.166 | LEAK-18, EV-9 |
| 39 | One 3-patient profile with both labels, kept | bullet 6 | groupby nunique | holds | 3 rows (age 56, F, Low), 2 No / 1 Yes; plausible genuine ambiguity | LEAK-20 |
| 41,71 | Stage != AJCC 8th in 12/383 | bullet 8, issue 5 | recomputed AJCC 8th | holds | 371 match | PROV-13 |
| 42 | 2 of 18 M1 are Intermediate risk | bullet 8 | crosstab | holds | ages 26 and 37 | - |
| 43 | Dropping M and Stage changes AUC by +0.001 | bullet 8 | LR/RF on 60 splits | holds | LR +0.0001 (scaled), RF +0.0005; original unscaled LR +0.0013 | EV-1 |
| 44 | All 18 M1 and all 32 High recurred | bullet 9 | crosstab | holds | 18/18, 32/32 | - |
| 47 | Paper's AUC 0.984-0.997 on all features | bullet 10 | abstract | holds | KNN 98.44 ... SVM 99.71; abstract says "13 clinicopathologic features", file has 16 inputs, so which 13 (Response?) is unverified | PROV-17 |
| 48 | ATA risk alone 0.896 on 60 splits | bullet 10 | ordinal Risk AUC per split | holds | 0.8963 | TP-4 |
| 49,64 | Three untuned models 0.929-0.932 beat Risk on 59-60 of 60 | bullet 10, record | LR/RF/HGB on 60 splits | holds in substance, config-sensitive; CatBoost untested | unscaled LR 0.929 (orig. 59/60); standardised LR 0.922, beats Risk on 52/60; RF 0.9285, 59/60, gain 0.032 (SE 0.002); HGB 0.923, 54/60 | TP-4, EV-8 |
| 51,56 | The copies are "the most common record of 14 coarse clinical fields" | warning, Decision 3 | rank of each copy's 13-categorical profile | refuted as worded | copies fall in 7 different ranks of 13-field profiles; 20 of 48 copy rows in the single most common profile (37 rows), 44 of 48 in the top 5 | EV-7 |
| 53 | Leaving the copied test rows out lowers AUC by 0.002-0.003 | warning | drop test rows with a copy in train | holds only for feature copies | feature-vector copies: LR -0.0023, RF -0.0025 (reproduced); exact row copies (the 26 copies the sentence names): LR -0.006, RF -0.008, HGB -0.007 | LEAK-16, EV-8 |
| 57-59 | Record front matter, CC comments (`Trivial`) | record | see 48-49 | `Trivial` refuted (as the definition says) | best models beat Risk with mean gain 0.03 | TP-4 |
| 60-61 | 400-patient Hamadan cohort 2008-2023; Table 2 matches | record | Khazaei text | holds (period), Table 2 not re-checked | "400 patients", "January 2008 to December 2023" | PROV-16 |
| 65 | No open text defines recurrence | record | Khazaei text grep | holds | only "mainly local involvement" | PROV-17 |
| 66 | Priority line | record | - | not a fact claim | - | - |
| 68 | File uses 2015 ATA response categories | issue 1 | values | holds | Excellent / Indeterminate / Biochemical / Structural incomplete | - |
| 69 | Risk x Gender lookup 0.917, beaten by best of three on 54/60, CatBoost gain 0.036 | issue 3 | train-fold lookup | lookup holds; 54/60 untested (CatBoost) | lookup 0.9173; best of LR(std)/RF/HGB beats it on 47/60 | TP-4, EV-8 |
| 70 | 9.3% of test rows have a copy in train | issue 4 | per split | holds | 9.27% (feature copy), 8.92% (exact row) | LEAK-16 |

**Implied claims (nobody wrote them)**

* Every feature known at the prediction point: holds for the kept columns by meaning; the concern is `Risk` (7 Low-risk
  N1b, 2 Intermediate M1, 100% recurrence in High against 68% in Tuttle 2010). Circumstantial; could not be tested
  without the paper (EV-6, PROV-17).
* The split is the one the use case needs: holds; no date or patient id exists for anything else.
* The target is the real-world target: untested; recurrence vs persistent disease unverified (paper paywalled).
* No row is a copy across the split: refuted as a fact, accepted on purpose: 9.3% of test rows have a feature copy in
  train, all non-recurrent except the one 3-row profile; effect -0.002 to -0.008 ROC AUC.
* Follow-up long enough for every label (no censoring): untested; no dates; sources say >= 10 years.

**Refuted and untested, ranked (validity first, Must first)**

1. Untested, P3/P4 validity (PROV-17 Must, LEAK-10 Must): the label definition and when `Risk` was assigned. Changes
   nothing now (the definition already says "seems to"); remedy: the curator reads the PDF (issue 2) and checks which
   13 features the paper used and whether `Risk` was assigned at staging.
2. Untested, P4 (LEAK-23 Must): censoring; rests on the source's ">= 10 years". Remedy: none on the data; keep the
   wording "followed for at least 10 years (UCI)".
3. Partly refuted, P4 wording (LEAK-16, EV-8): claim 53's 0.002-0.003 holds only for feature copies; for exact row
   copies the drop is 0.006-0.008. Verdict unchanged (still small); remedy: write "test rows whose feature vector occurs
   in train" or give 0.002-0.008.
4. Refuted as worded (EV-7): claims 51/56 "the most common record": the copies span several profiles, 20 of 48 in the
   modal one. Remedy: "among the most common records (44 of 48 copy rows in the five most common profiles)".
5. Config-sensitive / untested (EV-8, TP-4): 59-60/60 and 54/60 depend on unscaled LR and CatBoost; standardised LR
   52/60, lookup beaten 47/60 by substitutes. `Trivial` still does not hold (RF 59/60, gain 0.032, SE 0.002). Remedy:
   name the models in the sentence (already done) and say the counts are for those models.

</details>

<details><summary>Column audit</summary>

**Column audit: differentiated_thyroid_cancer_recurrence (2026-10-20, re-check)**

Prediction point (first `curation_comments` bullet): after initial therapy, at the initial staging, when the ATA risk of
recurrence is assigned. Frame: rebuilt from the definition, 383 x 15, IID, rows shuffled (CLEAN-23 holds), no missing
values, no proxy codes. Codebook: UCI 915 variable table gives names and types only (all descriptions blank; the page
says "13 clinicopathologic features", the file has 16). Paper (Borzooei et al. 2024) paywalled.

**Column table**

| column | meaning | known at prediction? | dtype and cleaning | verdict | rule |
|---|---|---|---|---|---|
| Age | age (codebook: "Age"); at diagnosis presumably, unknown | yes | int64, 15-82, plausible | fine | CLEAN-14 |
| Gender | sex F/M | yes | category, 2 levels | fine | CLEAN-14 |
| Smoking | current smoking, unknown (blank codebook) | yes | category | fine | CLEAN-14 |
| Hx Smoking | smoking history, unknown; 37 rows Smoking=Yes with Hx Smoking=No, so probably "former smoker", not "ever" | yes | category | question (meaning only) | LEAK-2 |
| Thyroid Function | preoperative thyroid status (5 levels) | yes | category | fine | CLEAN-14 |
| Physical Examination | preoperative goitre finding (5 levels) | yes | category | fine | CLEAN-14 |
| Adenopathy | clinical lymphadenopathy by side (6 levels); not a copy of `N` (N0 with adenopathy 9, N1b with "No" 4), so clinical, pre-surgery | yes | category | fine | CLEAN-14 |
| Pathology | histology from the surgical specimen; "Hurthel cell" renamed "Hurthle cell" | yes (surgery precedes the point) | category, typo fixed | fine | CLEAN-1 |
| Focality | uni/multifocal, pathology | yes | category | fine | CLEAN-14 |
| Risk | ATA initial risk of persistent/recurrent disease (Low/Intermediate/High) | yes by definition (Tuttle 2010: "part of initial staging"); but likely assigned retrospectively with 2015 categories | category (unordered; pipeline encodes) | fine, with a question | LEAK-10, LEAK-6 |
| T | AJCC T stage, pathological | yes | category | fine | CLEAN-14 |
| N | AJCC N stage, pathological | yes | category | fine | CLEAN-14 |
| M | distant metastasis M0/M1; all 18 M1 recurred, 2 of them ATA intermediate | mostly yes (M1 found on the first post-treatment scan is still initial staging); 2 rows may be later finds | category | fine, anomaly noted | LEAK-11, CLEAN-11 |
| Stage | AJCC stage, derived from Age, T, N, M (8th ed. in 371/383) | yes (function of earlier fields) | category; 12 rows inconsistent, kept as recorded | fine, anomaly noted | CLEAN-11 |
| Recurred (target) | recurrence during >=10 y follow-up; seems to include persistent disease | outcome | category Yes/No, 108/383 | question (label definition) | USE-5, LEAK-4 |
| Response (dropped) | response to therapy (ATA 2015 categories), assessed in first 2 y of follow-up; structural incomplete = the outcome (89/91 recurred) | no | dropped | leak, correctly removed (strong) | LEAK-10 |
| Hx Radiothreapy (dropped) | undefined, undated; 7 "Yes", 6 high-risk recurred | unknown | dropped | correctly removed as unverifiable; mild alternative: keep with `Potential leak` note | LEAK-10, LEAK-6 |

**Measurements**

* Ablations on the 60 shipped splits (ROC AUC, logistic / random forest): all 0.929 / 0.929; without `Risk`
  0.919 / 0.922; without `Risk`, `M`, `Stage` 0.917 / 0.921; `Risk` alone 0.896; without `Adenopathy` 0.930 / 0.928;
  without both smoking columns 0.932 / 0.925. No kept column carries a large unexplained signal.
* Hindsight test on `Risk`: a crude ATA 2015 rule from `T`, `N`, `M`, `Adenopathy` agrees with the recorded `Risk` in
  337 of 383 rows. Recorded higher than the rule: 7/21 recurred (33%); recorded lower: 6/25 (24%); agree: 95/337 (28%).
  The discordant rows are not pushed towards the outcome overall. Within the rule's Low cell, recorded Intermediate
  recur 5/19 vs recorded Low 10/229; within the rule's Intermediate cell, recorded Low recur 2/20 vs Intermediate 55/78.
  Both fit legitimate inputs the file lacks (vascular invasion, aggressive histology, <=5 N1 micrometastases) as well
  as hindsight; the file cannot tell them apart. `Risk` adds 0.007-0.010 AUC over the other columns.
* ATA consistency gaps: T4a with Intermediate 3, T3b with Intermediate 14 (gross extension is High in ATA 2015),
  M1 with Intermediate 2: coding is not strictly by the guideline.

**Problems, ranked (principles.md)**

1. P3/P4, question for the curator (USE-5, LEAK-4): `Recurred` probably counts persistent disease (all 32 ATA High,
   all 18 M1 recur). Not a leak at this prediction point (ATA risk targets "persistent/recurrent disease"); mildest
   remedy: keep, get the paper to confirm (already issue 2).
2. P4, weak, question (LEAK-10, LEAK-6): `Risk` (and the 2015 response categories) were likely assigned retrospectively
   with follow-up known. Measured: no outcome-directed bias in discordant rows; +0.01 AUC at most. Remedy: keep with a
   one-line note in the `Note:` or `Anomaly:` bullet; dropping `Risk` would remove the clinical baseline the use case
   is built on.
3. P4, weak (LEAK-11): 2 M1 rows coded ATA intermediate may be metastases found after staging; already measured
   (+0.001) and noted. No change.
4. P4, resolved: `Response` (strong, LEAK-10) and `Hx Radiothreapy` (unverifiable) dropped correctly.
5. P7, question (LEAK-2): `Hx Smoking` meaning unknown (37 current smokers with Hx=No: probably former smoker). No
   change; the README could say "meaning not given by the source".
6. P7, cosmetic (CLEAN-14): `T`, `N`, `Stage`, `Risk` are unordered categoricals although ordinal; acceptable, the
   pipeline encodes (CLEAN-2). No change.

No cleaning problem that needs a fix; no column to drop beyond the two already dropped.

</details>

<details><summary>Split audit</summary>

**Split audit: differentiated_thyroid_cancer_recurrence (re-check, 2026-10-20)**

Verdict: **right with notes.** IID over patients, 20 x 3-fold stratified, mirrors the use case (a new patient at
initial staging, scored by a model trained on earlier patients of the same clinic). No change to the split needed.

Loaded through
`dataset_io.load(..., built=False)` (origin `rebuilt`), thread caps 2.

**Facts checked**

| Check | Result | Rule |
|---|---|---|
| Regime vs use case | New patient each time, one row per patient (383 = the paper's cohort); no patient id, no repeated entity. Cold start over patients is the deployment: IID is the right regime. | SPLIT-1, SPLIT-2, USE-10 |
| Size per fold | 60 splits; train 255-256, test 127-128; 36 positives in every test fold (stratified on `Recurred`); folds disjoint. | TP-9 |
| Hidden groups | Probe: 1 candidate (`Age`), gap +0.000; composite key (all but Physical Examination) gap -0.014; 0% near-copy clusters; no hit. | SPLIT-29, SPLIT-30 |
| Duplicate rows / near copies | 356 distinct feature profiles over 383 rows. Alternative (sensitivity only, not a valid group id per SPLIT-24): StratifiedGroupKFold on the exact feature profile, 30 splits: RF 0.936, LR 0.930, Risk alone 0.896, against the shipped splits (first 30) RF 0.934, LR 0.928, Risk 0.896. Dropping test rows with an exact train copy (11.8 per fold): RF 0.932, LR 0.925, Risk 0.893. Copies do not inflate the score; the accepted warning holds. | LEAK-16, LEAK-18, SPLIT-24 |
| Time axis | No date column. The raw file is sorted by `T` (7 runs) and then `Recurred` (12 runs), so the row order is not time; no row-order time index can be recovered (Spearman order vs label 0.02, vs age 0.00 in the curated order). | SPLIT-7, SPLIT-22 |

**Problems, ranked**

1. **P4, note: the time axis is lost, and the follow-up claim is not consistent.** UCI: "collected in duration of 15
   years and each patient was followed for at least 10 years" (fetched 2026-10-20); the record places the cohort in
   2008-2023 (Khazaei et al. 2024). Both cannot hold for patients diagnosed after about 2013: if late patients have a
   shorter follow-up, their `Recurred = No` is partly censored, and a temporal split would train on outcomes not yet
   final for the newest patients (SPLIT-9's concern, here unmeasurable). Staging also changed inside the window (ATA
   2015, AJCC 8th in 2018: the 12 `Stage` mismatches may be AJCC 7th rows). Neither can be tested without dates.
   Rule: SPLIT-7, SPLIT-8, SPLIT-9, LEAK-24. Mildest remedy: none to the split (no dates, no row order). Write "the
   source states at least 10 years of follow-up" rather than as a fact in `task_summary.row` and curation_comments,
   and add one line saying a diagnosis year would allow a temporal check if the authors release it. Tagging the task
   as forced IID from temporal (SPLIT-8) is optional: this is a patient cohort, not a stream of signals, and a clinic
   deploying the model scores new patients whose era differs only mildly.
2. **P6, note: small test folds.** 127 rows with 36 positives per fold; seed SD of ROC AUC about 0.016-0.020 across
   splits. Adequate with 60 splits; no remedy.

No problem at P1-P3 from the split.

</details>

<details><summary>Domain practitioner</summary>

**Domain practitioner: differentiated_thyroid_cancer_recurrence (2026-10-20, re-check)**

Actor: the endocrinologist / thyroid oncologist at the Hamadan endocrine clinic, a few weeks after total
thyroidectomy, holding the pathology report and assigning the ATA initial risk (Tuttle 2010; ATA 2015 [R46]-[R48]).

**Verdict**

**Fit: direct.** Every kept column is something I have on my desk at the postoperative staging visit, the label is the
outcome the ATA initial risk system itself estimates ("persistent/recurrent disease"), and a random patient split
stands for the next patients of the same clinic (USE-1, USE-3, USE-8). The fit is direct only after `Response` is
dropped; with it the task would be the 6-24-month re-staging, not this decision (USE-4).

**1. Do I have these inputs at the prediction point? (USE-3, USE-6)**

| Column | At postoperative staging? | Note |
|---|---|---|
| Age, Gender, Smoking, Hx Smoking | yes | |
| Thyroid Function, Physical Examination, Adenopathy | yes, preoperative | Adenopathy agrees with N (259/268 N0 have none) |
| Pathology, Focality, T, N | yes, from the surgical pathology report | |
| M | mostly yes | M1 is usually found on the post-RAI whole-body scan, days after ablation; 2 of 18 M1 are ATA intermediate, so some M1 were found later (kept; +0.001 AUC). Acceptable. |
| Stage | yes, derived from Age/T/N/M | 12 rows disagree with AJCC 8 |
| Risk (ATA initial) | yes, it is my own estimate | a legitimate input under USE-6: the model refines my estimate. Khazaei et al. 2024 say risk "was determined based on the stage of the group and the age", i.e. from staging data, not from the outcome. |
| `Response` (dropped) | **no** | the response to therapy is assessed 6-24 months after initial therapy from suppressed/stimulated Tg, anti-Tg and imaging (Tuttle 2010; Khazaei 2024 Methods); its structural-incomplete class is the outcome (ATA 2015 [B29]); 89/91 such patients recurred, 1/208 excellent. Dropping it is right (USE-3, LEAK-10). |
| `Hx Radiothreapy` (dropped) | unknown | undefined, undated; 6/7 "Yes" are advanced high-risk disease. Dropping is the safe call. |

**What I would always have and the data lacks** (these make the model weaker than mine, they do not change the task):
1. Postoperative serum thyroglobulin and anti-Tg (the single strongest early marker; ATA 2015 uses it in the RAI
   decision).
2. Tumour size in mm, vascular invasion (number of foci), extent of extrathyroidal extension, number and size of
   involved nodes and extranodal extension: the ATA criteria themselves; here only coarse T/N.
3. Molecular markers where available (BRAF V600E, TERT) - not routine in Iran in 2008-2013, so a fair omission.
4. Whether and at what dose I gave RAI, and the post-therapy scan. RAI is decided at this very visit, so it is a
   treatment, not an input; but its absence means the label is the outcome "under the clinic's usual care".

**2. Is the target what I act on? (USE-5)**

Close to it. At staging I want the probability of persistent or recurrent structural disease, which is exactly what
ATA initial risk estimates. Gaps:
- The label seems to count persistent disease (all 32 high-risk and all 18 M1 recurred). Recurrence by risk class here
  is 4.8% / 62.7% / 100% (low / intermediate / high), against about 3% / 21% / 68% for structural persistent or recurrent
  disease in Tuttle 2010 and lower in modern cohorts. So `Recurred` likely also counts biochemical persistence or
  any disease ever seen in follow-up, and the intermediate group looks unusually sick. The clinical decision is still
  served, but the label definition is unverified (REVIEW issue 2) and it should stay named in `predicted`.
- Horizon: "followed for at least 10 years" (UCI) vs "fifteen years"/"10-year follow-up" (Khazaei 2024, inconsistent).
  A roughly fixed long horizon is fine for me; I would prefer a 5- or 10-year probability, but a binary ever-recurred
  label over >=10 years is acceptable.
- I want a probability (ROC AUC is fine for ranking; calibration would matter in practice).

**3. Does one row match one decision? Is the test what I would face? (USE-10, USE-11)**

Yes: one patient, one staging decision; the patient is new to the model (cold start, no history), so IID over
patients is right and USE-11 holds (one row per patient is the use case). Test = new patients of the same clinic. What
I would really face is next year's patients (no diagnosis dates to make a temporal split; practice changed over
2008-2023: AJCC 7 to 8, ATA 2009 to 2015 with less RAI for low risk) or another hospital. That is an untested shift,
not a mismatch.

**4. Would I use the model?**

As a refinement of the ATA risk class, yes in principle: the shipped data shows models at 0.929-0.932 ROC AUC against
0.896 for Risk alone, beaten on 59-60 of 60 splits. Trust: it uses only staging data and agrees with the guideline's
logic. Distrust: 383 patients from one clinic, an undefined label, recurrence rates far above the literature, no
postoperative Tg, and no dates. I would not change follow-up intensity on it before external validation; the routine
follow-up decision is in practice driven by the response to therapy at 6-24 months (ATA 2015 dynamic risk), which this
task correctly excludes.

**Gaps, ranked by how much they change the task**

1. **Label definition unverified** (persistent + recurrent, possibly biochemical; recurrence rates 63% and 100% in
   intermediate and high risk). Changes what "recurred" means, not whether the decision is real. USE-5.
2. **Missing routine inputs** (postoperative Tg, tumour size, vascular invasion, ETE extent, node count). Makes the
   task easier for the ATA column relative to what a clinician has, and caps model skill; not a fit issue. USE-8.
3. **Some M1 found after staging** (2 of 18 inconsistent with ATA high risk); a minor potential leak, effect +0.001.
   USE-3.
4. **Use case wording mixes two decisions**: at initial staging I decide RAI and the TSH target; follow-up intensity is
   mostly set at the response assessment. USE-1.
5. **IID, single clinic, no dates**: test stands for same-clinic patients, not next year or another site. USE-10.

**What an expert would change**

- Rephrase the use case to the decision made at that visit: "decides on radioiodine and the TSH target and the initial
  follow-up schedule" (USE-1). Optional wording change in `task_summary.use_case`.
- Keep `Response` out; keep `Risk` as an input (USE-6); keep the drop of `Hx Radiothreapy` until the paper defines it.
- In `predicted` or a `Note:` bullet, cite the per-risk recurrence rates against Tuttle 2010 so a user sees the label
  is broader than structural recurrence after remission.
- Get the Borzooei 2024 PDF to confirm the label, the horizon and when Risk and M were recorded (REVIEW issue 2); if it
  shows Risk or M were coded with follow-up known, the fit becomes approximate (USE-8, potential leak kept on purpose).

**Sources**

- the dataset's dataset.py, README.md and REVIEW.md; raw
  Thyroid_Diff.csv (crosstabs Risk x Recurred, Response x Recurred, Adenopathy x N).
- Khazaei et al. 2024, J Res Health Sci 24(4):e00632, https://pmc.ncbi.nlm.nih.gov/articles/PMC11492527/ (400
  patients, 2008-2023, risk from stage group and age, response from Tg/anti-Tg/WBS, recurrence undefined).
- Tuttle et al. 2010, Thyroid 20:1341 (initial ATA risk at staging; re-staging in the first 2 years); ATA 2015
  guidelines, Haugen et al. 2016, Thyroid 26:1 ([B19], [B29], response categories), as quoted in REVIEW.md.
- Italian prospective cohort on ATA 2015 risk vs structural incomplete response (search result summary,
  https://pubmed.ncbi.nlm.nih.gov/32475305/).
- .claude/skills/knowledge-curation/references/use_case.md (USE-1, USE-3 to USE-6, USE-8, USE-10, USE-11).

</details>

<details><summary>Blind review</summary>

**Blind review: differentiated_thyroid_cancer_recurrence**

**Verdict:** Include with changes. It is a real clinical cohort with a real use, but it is small, has duplicate rows, and is close to solved by one engineered column.

**Task:** At diagnosis or after surgery, a clinician predicts whether a well-differentiated thyroid cancer will recur, and uses that to set follow-up intensity and RAI/TSH-suppression therapy. The source (UCI 915; Borzooei et al. 2023, Head & Neck) is a single-centre cohort collected over 15 years: "each patient was followed for at least 10 years". Data: 383 rows, 14 features, 108/383 recurred (28%), no missing values.

**Concerns, most serious first**
1. **Signal sits in a few derived columns, so the task is easy.**
   - `Risk` is the ATA risk class, built from T, N, M, pathology and extension. In the data, High is 32/32 recurred and Low is 12/249 recurred.
   - Logistic regression on `Risk` alone: AUC 0.896. On all features: AUC 0.927 (3-fold, repeated).
   - T, N, M, Stage and Risk overlap heavily.
   - This is not a leak, because all of them are known after surgery. But headroom between methods will be small, and on 383 rows the split noise is large.
   - Change: keep the dataset, but give it low weight or treat it as a "small, easy" case.
2. **Duplicates.**
   - 26 rows are exact duplicates of another row; 27 rows duplicate another row's features. One feature pattern appears with both labels.
   - With all-categorical features, many of these may be genuinely different patients, so they cannot be told apart.
   - Under a random split, copies land in both train and test.
   - Change: either accept this and document it, or deduplicate / group by feature pattern.
3. **Columns dropped from the source without documentation.**
   - The UCI table lists 16-17 variables: it includes `Hx Radiothreapy` and, as I recall from the published table, a `Response` (to therapy) column. I did not see those rows on the page myself (see "Not checked").
   - Dropping `Response` is right if the prediction is made at diagnosis: it is post-treatment information and close to a leak.
   - Dropping `Hx Radiotherapy` loses a legitimate baseline feature.
   - Change: restore `Hx Radiotherapy`, and document why `Response` is excluded.
4. **Preparation.**
   - Types are fine: Age is int, the rest are categorical.
   - T, N, Stage and Risk are ordinal but stored as nominal. That is acceptable, or they could be encoded as ordered.
   - Several levels are rare: Stage III has 4 rows, Adenopathy "Posterior" has 2. With 3-fold splits, some folds may not see these levels.
5. **Split.** A random IID split with 20x3 folds is acceptable for one centre with no dates. A temporal split is not possible because there is no diagnosis year.

**Not checked**
- The full UCI variable table: the page showed only 10 of 17 rows, so I could not confirm the dropped columns.
- Whether the duplicates are distinct patients.
- Whether the data come from outside the single centre; the paper does not include external validation.

</details>

<details><summary>Precedent check</summary>

**Precedents: differentiated_thyroid_cancer_recurrence (review panel, re-check, 2026-10-20)**


The curator has not yet decided anything on this dataset: the record has only the old screening comments (one is "likely trivial") and AI assessments. So the check is of the AI's decisions in the definition and the review file before this run against the curator's earlier decisions and the rules.

**Per decision**

**1. `Response` dropped; the task predicts at the initial staging (REVIEW issue 1): consistent**

- **Rules:**
  - LEAK-10 (Must): a column recorded after the prediction point, and a part or encoding of the target. Structural incomplete is "persistent or newly identified ... metastases", 89 of 91 recurred.
  - USE-3 and USE-4 (Must).
- **Precedents followed:**
  - caracas_cervical_cancer: Hinselmann, Schiller and Citology dropped as results of the same work-up. Assessment 2026-10-07; shipped by Lennart, CC 2026-10-15.
  - mic: the prediction point moved earlier and the columns that do not exist yet dropped (LEAK-10 Cases).
  - heart_failure_followup_survival: `time` dropped (Lennart, 2026-09-30).
  - eryhemato_squamous_disease: offered at the earlier stage (USE-4, TP-6).
- **One distinction to keep straight:** TP-6 and the tension "a better version against our own fix" (eryhemato) say that a fix of our own invention is not a better version.
  - The drop is acceptable because it rests on LEAK-10 (P4), not on making the task less trivial (P6).
  - The earlier stage is one the field describes (Tuttle 2010: initial ATA staging, then re-staging in the first two years), not the source paper. USE-4's "the stage the source describes" is met through the guideline the paper cites.
  - REVIEW issue 1 and the `Trivial` note should keep these two arguments apart, as they do now.
- **Not a departure:** LEAK-11 (south_africa_coronary_heart_disease keeps measurements taken after the event) applies only when the late value weakens the signal. `Response` strengthens it (0.978 alone).

**2. `Hx Radiothreapy` dropped (REVIEW issue 6): departs from a recent pattern, with a stated reason; part of the pair in prompt 1**

- **Rules:**
  - LEAK-10 (Must) if the column is post-staging.
  - LEAK-6 (Must): measure before acting; a confirmed leak goes even when small, a slight optimism with a known cause can stay with a note.
  - Measured: logistic regression 0.930 with and without the column. The mechanism is circumstantial (EV-6): 6 of the 7 "Yes" rows are advanced disease. "Hx" also reads as *history of*, i.e. before the prediction point.
- **Precedents where a column was dropped:**
  - 2_month_survival_rate_prediction `adls`, `adlsc` (Lennart, CC 2026-10-12). The mechanism was measured: 46% against 24% missing, by whether the stay outlasted the interview.
  - expresso_churn_prediction `REGION` (open, this run): measured, 0.93 to 0.90.
  - thyroid_discordant `referral_source`: v1, dropped on suspicion, no measurement.
- **Precedents where a suspect column was kept with a note:**
  - LEAK-38 (Should): kick `WheelType`, homesite. "Removing an unverified signal from host-designed data is arbitrary."
  - LEAK-30 (Lennart, 2026-10-19). Register flag 3 records the curator's shift from exclude (coad, 2026-10-16) to keep-with-a-note (2026-10-19) for weak leaks.
- **What sets this case apart (written):** the column is named, not anonymised, and the data are academic, so LEAK-38's scope does not cover it. Its probable meaning is treatment of advanced disease. The drop costs nothing measurable.
- **Assessment:** reasonable under LEAK-10. It differs from adls/adlsc and REGION in that its mechanism is not measured, so it rests on circumstantial evidence. Keep with a `Potential leak, kept on purpose:` note (the REVIEW alternative) is equally consistent with LEAK-6 and the 2026-10-19 direction. This is a weighing call for the curator, not a rule breach.

**3. `M` and `Stage` kept as recorded, written as `Anomaly:` (REVIEW issue 5): departs from the treatment of decision 2 without a written reason (prompt 1)**

- **`Stage` mismatches (12 of 383):** consistent with CLEAN-11 and caracas_cervical_cancer (Lennart, CC 2026-10-15). Impossible values became missing there, but contradictions between a summary field and its parts (5 `dx_*` flags with `dx` = 0) stayed.
  - `Stage` is a summary of Age, T, N and M, so the same reading applies.
  - Recomputing the stage from AJCC 8th would be a fix of our own (PROV-13: repair from the origin first).
- **`M` possibly found after staging (2 of 18 M1 at ATA intermediate risk):** this is the same mechanism as decision 2, a value possibly recorded after the prediction point. The measured effect is also nil (dropping `M` and `Stage` gives +0.001).
  - Yet `M` is kept and the column with no definition and no date is dropped.
  - The definition calls this an `Anomaly:`. In the v0.2 copy, a suspected timing or post-outcome signal that is kept is written as `Potential leak, kept on purpose:` (21 definitions; for example churn_telco_south_asia, Lennart 2026-10-15; melbourne_housing_market; house_sales; mobile_churn).
- **Distinguishing fact (the AI's guess, not written):** M is a defined staging field that is part of the initial staging by definition, and only 2 of 18 values are doubtful. The radiotherapy column has no definition, and 6 of its 7 positives look like post-staging treatment.

**4. Duplicates kept: 26 copies, 6.8% (REVIEW issue 4): consistent**

- **Rules:** LEAK-16 (a decision was made), and LEAK-18 (Should): few features and plausible repeats are natural, keep them and say so. Probe 5, reading 3.
- **Precedents followed:**
  - caracas_cervical_cancer: 21 copies (2.8%) of coarse answer profiles, kept after the same permutation test (20 by chance, 16-25). Lennart, ship 2026-10-15.
  - breast_cancer_prediction: 52.2% repeated profiles kept, coarse features, different women; reviewed 2026-10-15.
  - sepsis_survival_minimal_clinical_records: the LEAK-18 case (Lennart, 2026-10-06).
- **Opposite decisions, each with a fact that sets it apart:**
  - wine_quality (Lennart, 2026-09-30), jm1 (2026-10-01) and obesity_estimation (Lennart, 2026-10-14): continuous values to the centimetre or decimal, many degrees of freedom.
  - audiology_diagnosis (LEAK-19): the same findings on other ids.
  - fiat_500 (2026-10-14): crawler copies.
  - thyroid_discordant (60 rows dropped): continuous lab values, and Quinlan's "repeats".
  - Here the features are 14 coarse categories plus age in years, at a chance rate (p = 0.16). That is the LEAK-18 split.
- **No drift:** Lennart's drops are all on data with many degrees of freedom and the keeps on coarse profiles.

**5. One profile of 3 patients with both labels kept: consistent; the wording could cite the rule**

- **Rule:** LEAK-20 (Should): drop every copy unless it is a genuine label ambiguity the task has.
- **Precedents:** caracas_cervical_cancer kept its 1 profile whose copies differ in the biopsy (Lennart, 2026-10-15). breast_cancer_prediction keeps 68 conflicting rows (`dataset_conflicting_duplicate_rows` info).
- **Wording:** the definition says "we keep all three" with no reason in LEAK-20's terms. Suggested: "different patients with the same coarse record whose outcomes differ: a label ambiguity the task has (LEAK-20)". This is a writing fix, not a departure.

**6. The `Trivial` marker answered (REVIEW issue 3): consistent**

- **Rule:** TP-4 (Must). Read what the dominant feature means first: `Risk` is the ATA initial risk, the clinicians' own estimate and the natural core, an input under USE-6 and LEAK-37. Then test it fold by fold:
  - `Risk` alone gives 0.896.
  - Logistic regression, random forest and CatBoost beat it on 59, 59 and 60 of 60 splits.
  - The best two-feature lookup is beaten on 54 of 60.
- **Precedents followed:**
  - aps_failure (kept, 2026-10-06; the per-split feature is below all configurations).
  - sepsis_survival (kept 2026-10-06; age 0.704 against 0.707).
  - california_house_prices_2020 (kept 2026-10-06).
  - Opposite: fitness_club (retired 2026-10-05). There the single feature was *above* all 37 configurations; here it is below on 59-60 of 60.
- **Register flags 2 and 4:** the opposite outcomes on one_feature and trivial are settled by the TP-4 test. They do not conflict with this case.
- **Same-run parallels:** house_prices_nominal and diabetes_3 have the same open "`Trivial` not borne out" issue. Decide the three alike.
- **Flagged precedent that goes against a rule:** thyroid_discordant ships (`DF: Yes`, BeyondArena) with a `Trivial` marker taken from a screening note ("still seems trivial") that was never tested by TP-4. Its definition also says "the curators found the task close to trivial".
  - If the marker is removed here on TP-4 evidence, thyroid_discordant's marker should get the same test (option (c) below), not be followed.
- **TP-1:** the probes are untuned, and no tuned TabArena results exist yet. Untuned models beating the single feature is enough to reject `Trivial`, so TP-1 does not block this.

**7. Label definition unverified, paper paywalled (REVIEW issue 2); `fit="direct"`: shipping is consistent, the fit departs without a written reason (prompt 2)**

- **Rules:**
  - USE-5 (Must): check how the source built its label.
  - LEAK-3 (Should): read the paper. The departure is forced by the paywall and is written down.
  - EV-7 and PROV-16 (Must): met. The definition attributes nothing to the unread paper and says "seems".
- **Shipping with the label's definition or timing undocumented:**
  - churn_telco_south_asia (Lennart, 2026-10-15): when churn was observed is undocumented; kept with a `Potential leak, kept on purpose` note, `fit="approximate"`.
  - thyroid_discordant: an undefined label, `fit="approximate"`.
  - mobile_churn (open, this run): churn undefined, `approximate`.
  - diabetes_3 (open, this run): response undocumented, retire is an alternative.
  - alfa_battle_2_0_task_2: approximate for a label without a stated horizon (USE-8 Cases).
  - glioma_grading_clinical_and_mutation_features: this run's mediator also moved it to approximate for a label that stands in for another.
- **Where this case differs:** either reading of `Recurred` (recurrence only, or persistent plus recurrent) is what the ATA initial risk estimates (ATA 2015, [B19]), and the actor acts on that. The `Note:` bullet says the task is valid either way. `fit_reason`, however, names only the late-found metastases and the single clinic, not the label.
- **Related cohort point, not a departure:** if persistent disease counts, the M1 patients may already have the outcome at the prediction point. That is a cohort question under LEAK-22 and LEAK-36 ("follow the paper's cohort"; diabetes_130_us), not a feature leak, and the ATA risk system includes these patients. It fits the current definition.

**8. IID split, one row per patient: consistent**

SPLIT-1 and USE-11. Same as breast_cancer_prediction (USE-11; Lennart, 2026-10-15) and caracas_cervical_cancer. The hidden-group probe is clean.

**9. Size, 383 patients with 107 recurred, 36 per test fold: consistent**

- **Rules:** TP-5 and the tension "tiny but real". musk was kept with 13 per fold; parkinsons retired with 2-3 per fold.
- **new_thyroid:** "too small" (Lennart and Andrej, imported workbook verdict, before TP-5). It has 215 rows in 3 classes and is a duplicate of thyroid_discordant, so it is not a precedent against this case.

**10. Uniqueness among the thyroid records: consistent**

- thyroid_discordant and new_thyroid are the 1987 Garvan / UCI thyroid-function data: another cohort, another task (PROV-6, PROV-7).
- OpenML 46605 is a re-upload of the same 383 rows, and the definition notes it.

**Drift and repeated exceptions**

- **No drift found** on the rules this dataset touches (LEAK-18/20 duplicates, LEAK-10 drops, TP-4).
- **Register flag 3 (LEAK-30):** the curator moved from exclude to keep-with-a-note for weak leaks. It bears on decision 2 only as a direction, not as a rule that applies.
- **No third exception of the same kind.** Dropping a column on circumstantial evidence with no measured effect is new; the earlier drops (adls/adlsc, REGION) had a measured mechanism. If the curator makes it a standing practice, it should become a sentence under LEAK-6 or LEAK-10 rather than an exception per dataset.

**Prompts for the curator (only for departures without a written reason)**

**Consistency check (AI, 2026-10-20), prompt 1:** your call on `Hx Radiothreapy` (drop it, REVIEW issue 6) differs from the call on `M` in the same definition (keep it, called an `Anomaly:`, REVIEW issue 5). The mechanism is the same: a value possibly recorded after the initial staging, with no measurable effect (0.930 with and without the radiotherapy column; +0.001 when `M` and `Stage` are dropped). What sets them apart?
- (a) `M` is a defined staging field that is part of the initial staging by definition, and only 2 of 18 values are doubtful, whereas the radiotherapy column has no definition or date and 6 of its 7 positives look like post-staging treatment. Recorded as the reason, with `M` relabelled `Potential leak, kept on purpose:` like churn_telco_south_asia (2026-10-15) and melbourne_housing_market.
- (b) Treat the radiotherapy column like `M`: keep it with a `Potential leak, kept on purpose:` note (the 2026-10-19 direction of LEAK-30 and LEAK-38).
- (c) Treat `M` like the radiotherapy column: drop `M` and `Stage` (+0.001 AUC).
- (d) Change the rule: add to LEAK-6 how a suspected timing leak with no measurable effect is handled.

**Consistency check (AI, 2026-10-20), prompt 2:** the call on `fit` (`direct`, with the label's definition unverified and a label that "seems to count persistent disease") differs from churn_telco_south_asia (shipped 2026-10-15 with `fit="approximate"`, the label's timing undocumented) and thyroid_discordant (`approximate`, an undefined label). What sets this case apart?
- (a) Either reading of `Recurred` is the target the ATA initial risk estimates ("persistent/recurrent disease", ATA 2015 [B19]), so the doubt does not change what the endocrinologist acts on. Recorded as the reason, with one clause added to `fit_reason`.
- (b) Treat it like churn_telco_south_asia: `fit="approximate"` until the paper's definition is read.
- (c) Reopen churn_telco_south_asia or thyroid_discordant to match.
- (d) Change the rule: say in USE-8 whether an unverified label definition alone makes a fit approximate.

**Also for the curator (a flagged precedent, no prompt for this dataset):** if `Trivial` is removed here on TP-4 evidence, thyroid_discordant's `Trivial` marker was never tested by TP-4. Give it the same test, or say why it stands.

</details>

<details><summary>Verification checklist</summary>

**Checklist: differentiated_thyroid_cancer_recurrence (re-check, 2026-10-20)**

Verdict (AI, before the panel): ready with noted concerns. The definition is unchanged since the 2026-10-07 run
(checksum `v2:7d8cc1ff...b829` as committed); the open concerns are the ones in the review file before this run.

Automated: `dataset list` imports the class (status `checked`); `ruff@0.15.15 check` and `format --check` clean.
`dataset check`: 0 errors, 0 warnings, 1 info (`dataset_conflicting_duplicate_rows`, 1 row), 1 accepted
(`dataset_duplicate_rows`). README diff: only the generator's template additions (`time_gap`, `time_gap_unit`, the
`REVIEW.md` row in the file table); checksum unchanged. No mechanical fix was needed.

Probes: leak probes, task probes (30 of 60 splits), hidden-group probe, generated-data probe: no flags.

| Rank | Check | Result | Evidence | Rules |
|---|---|---|---|---|
| P1 | Ethics | pass | De-identified clinical cohort donated by the authors to UCI under CC BY 4.0 (UCI page, fetched 2026-10-20); a recurrence-risk task is a standard clinical use. | SEL-1 |
| P2 | Scope | pass | Published for ML risk stratification of recurrence (paper title); a per-patient classification at staging. | SEL-2 to SEL-15 |
| P2, P5 | Real data | pass | Generated-data probe: no marks (rule leaves cover 0% of the minority rows; 81.5% of column pairs dependent; 0 of 1 uniform column). A 15-year cohort from one clinic with a matching cohort paper (Khazaei et al. 2024, Table 2, per the 2026-10-07 assessment; not re-read today). | SEL-16, PROV-3 |
| P3 | Use case and fit | pass | task_summary names the actor (endocrinologist), moment (initial staging) and decision (further treatment, follow-up intensity); `fit="direct"` with the gap (late-found metastases, one clinic) named in fit_reason. | USE-1, USE-2, USE-8, USE-9 |
| P3, P4 | Target and metric | concern | ROC AUC on a binary target with 28% positives fits. The label's definition is unverified: the paper is paywalled; all 18 M1 and all 32 ATA high-risk patients are labelled recurred, consistent with persistent disease counted as recurrence (the earlier review issue 2). Follow-up >= 10 years per the summary, so no censoring by download date, but this rests on the source's statement (cannot re-verify without the paper). | USE-5, LEAK-24, EV-5, EV-7 |
| P4 | Available at prediction time | concern | `Response` (post-treatment, 0.978 AUC alone) and `Hx Radiothreapy` (undefined, undated) dropped (dataset.py `_clean`). Remaining risk: 2 of 18 M1 patients are ATA intermediate, so M may hold post-staging findings; `Stage` mismatches AJCC 8th in 12 of 383 rows. Measured effect of dropping `M` and `Stage`: +0.001 AUC (curation_comments). Leak probes: each feature alone tops at `Risk` 0.896 against all 0.914; drop-one at most -0.027 (without `Risk` 0.887); no missing-indicator signal. When each variable was recorded is unverified (paper paywalled). | USE-3, LEAK-10, LEAK-1 |
| P4 | Irreversible and all-row leakage | pass | No fitted, scaled or label-aware feature; all columns are raw categorical fields or `Age` (dataset.py). | LEAK-13 to LEAK-15, LEAK-27 to LEAK-31 |
| P4 | Copies across the split | pass (decided) | 26 copies beyond the first (6.8%), kept and accepted with reason; leak probe 5: 8.6% of test rows have an exact copy in train; NN-distance score 0.804 against the full model's 0.914, but within ATA intermediate risk it is 0.498 and within low risk 0.691: the distance tracks the rarity of advanced profiles, ordinary data (evidence.md probe 6 reading 3). 49 rows at distance 0, 1 recurred. 1 conflicting-label row (info). | LEAK-16, LEAK-18, LEAK-20, EV-9 |
| P4 | Split regime | pass | IID over patients, one row per patient (383 = paper's cohort). Hidden-group probe: 1 candidate (`Age`), gap +0.000; composite key (all but Physical Examination) gap -0.014; 0% near-copy clusters; no hits. | SPLIT-1 to SPLIT-31 |
| P5 | Source | pass | DOI 10.24432/C5632J (UCI 915, donated 2023-10-30 by the authors). Bibtex names Borzooei et al. 2024, Eur Arch Otorhinolaryngol 281:2095, DOI 10.1007/s00405-023-08299-w. Note: UCI's page names the journal as "Head and Neck"; the DOI prefix s00405 is Eur Arch Otorhinolaryngol, so the bibtex is right and UCI's metadata is off (record note only). | PROV-1, PROV-2, PROV-10 |
| P5 | Uniqueness | pass | Other thyroid records (`thyroid_discordant`, `new_thyroid`) are the 1987 Garvan / UCI thyroid-function data, a different cohort and task. OpenML 46605 is a re-upload of the same 383 rows (download_description). | PROV-4 to PROV-7 |
| P5 | Damage and repair | pass | One typo repaired (`Hurthel cell` -> `Hurthle cell`); the raw file matches the published sha256. | PROV-13 to PROV-15 |
| P6 | Worth benchmarking | pass (open marker) | Task probes, 30 splits: linear 0.928, random forest 0.932, LightGBM 0.919, single feature 0.878 (Risk chosen 25 of 30), dummy 0.5; best beats dummy on 100%; spread 0.026 against paired SE 0.005; smallest class per test fold 36; no flags. The record's `Trivial` marker is answered in the earlier review issue 3 (Risk alone 0.896, beaten on 59-60 of 60). No tuned TabArena results exist for this new dataset (TP-1 cannot use them). | TP-1 to TP-10 |
| P7 | Dtypes and cleaning | pass | 14 categorical, `Age` int (README dtypes). `Hx Smoking` and `Smoking` both kept; no proxy missing values (no missing at all). | CLEAN-1 to CLEAN-24 |
| procedure | Notes match the code | pass | Every curation_comments step is in `_clean` (typo, two drops) or `_decisions` (the three tables). The anomaly numbers (12 Stage mismatches, +0.001) and the permutation test are not in `_decisions`; they are in the earlier review issues 4-5 and are reproducible from the raw file. | writing.md |
| procedure | Licence and citation | pass | CC BY 4.0 as stated on UCI (fetched 2026-10-20). Citation names the first publication. | EV-4, PROV-10 |
| procedure | Reproducibility | pass | The wget URL downloaded today gives zip sha256 66007e38...ab11, identical to the local copy, and Thyroid_Diff.csv sha256 a2c65f7c...7b44 as in download_description. Link pinned by DOI. Record pointer: `sync-notebooks --check` clean. | |

**What a human must still check**

1. The paper's definition of `Recurred` and when each variable (above all `M`, `Stage`, `Response`, `Hx Radiothreapy`)
   was recorded (paywalled; the earlier review issue 2). Cannot verify.

</details>

<details><summary>Advocate</summary>

**Advocate: differentiated_thyroid**


**1. The only strong leak is already fixed, at the right prediction point (P4, LEAK-10 Must; USE-3, USE-4 Must)**
- **Claim:** dropping `Response` turns a near-copy of the outcome into an honest initial-staging task.
- **Evidence:**
  - Response × Recurred: Excellent 1/208, Structural incomplete 89/91.
  - `Response` alone gives 0.978 AUC. `Response` + `Risk` gives 0.988, the same as all 16 columns (0.972-0.988), on 60 splits (claim audit rows 12-13).
  - Tuttle 2010: ATA risk is assigned "as part of initial staging", and patients are re-staged on response "during the first 2 years of follow-up". ATA 2015 [B29]: structural incomplete = "persistent or newly identified ... metastases", which is the outcome itself.
  - The column auditor, the practitioner, the precedent checker and the blind reviewer all call the drop right.
  - Precedents: caracas_cervical_cancer (work-up results dropped; Lennart, CC 2026-10-15), mic, heart_failure_followup_survival.
- **Why it holds:** this is the first rung of the remedy ladder: fix the definition and keep the task. The tension row "a real task against a leak" says to fix the leak and keep the task. The precedent checker separates this drop from eryhemato/TP-6: it rests on LEAK-10 at P4, not on making the task harder.

**2. A real use case with a direct fit (P3, USE-1, USE-3, USE-6 Must; USE-8 Must)**
- **Claim:** the actor, moment and decision are real, and every kept column is on the endocrinologist's desk at postoperative staging.
- **Evidence:**
  - Practitioner: "Fit: direct ... every kept column is something I have on my desk at the postoperative staging visit."
  - Borzooei abstract: recurrence risk "is crucial for guiding subsequent management and follow-ups".
  - `Risk` is the clinician's own initial estimate. Under USE-6 it is a legitimate input that the model refines. Khazaei 2024 says risk "was determined based on the stage of the group and the age".
- **Answer to the label objection (USE-5 Must, PROV-17 Must):**
  - `Recurred` may count persistent disease (32/32 high-risk and 18/18 M1 recurred). Under either reading the label is what ATA initial risk estimates: "the risk of persistent/recurrent disease" (ATA 2015 [B19]). So the target is still what the actor acts on, and USE-5 holds.
  - PROV-17 is met as written: the definition says "seems", and REVIEW issue 2 asks the curator for the PDF.
  - USE-8 lists "a label without a stated horizon" as approximate. Here the horizon is stated (at least 10 years, UCI).
- **Mildest fix:** add one clause to `fit_reason` naming the label doubt and why it does not change the target (precedents prompt 2, option a). If the curator prefers `approximate`, that is a one-word change, not a reason to hold the dataset back.

**3. Not `Trivial` (P6, TP-4 Must: "`Trivial` needs proof")**
- **Claim:** the old `Trivial` marker came from the paper's numbers, which probably include `Response`. Without `Response` it fails TP-4's fold-by-fold test.
- **Evidence:**
  - `Risk` alone gives 0.896 on the 60 shipped splits.
  - RF gives 0.9285 and beats `Risk` on 59/60 splits, mean gain 0.032 (SE 0.002) (claim audit row 49).
  - Standardised LR beats it on 52/60, HGB on 54/60.
  - The best two-feature lookup (`Risk` × `Gender`, 0.917) is beaten on 47-54/60.
- **Rule and precedents:** TP-4 says to read what the dominant feature means first. `Risk` is the natural core of this task, the clinicians' own estimate. Kept in the same situation: sepsis_survival and california. Retired: fitness_club, where the single feature was above every method. Here it is below on 52-60 of 60.
- **Why it outranks the blind reviewer's "easy, low headroom":** that reviewer also measured only 0.896 against 0.927, and it recommends "include", not retire. Small headroom is not the TP-4 test.
- **Concession:** the 59-60/60 counts depend on the model set (CatBoost was not installed for the audit). The sentence should say which models it counts. The verdict does not change.

**4. Not `Too Small` (P6, TP-5 Must)**
- **Evidence:** every test fold has 36 positives (split audit), and there are 108 positives in total. musk was kept with 13 per fold; parkinsons was retired with 2-3 per fold. The seed SD of AUC is 0.016-0.020, which is fine over 60 splits.
- **Rule:** the tension "tiny but real": a small dataset is a tiny-data task.

**5. The duplicates are natural repeats, kept on purpose (P4, LEAK-18 Should; LEAK-20 Should)**
- **Evidence:**
  - Features: 14 coarse categories plus age in whole years.
  - Re-run permutation of age within risk × sex: 23.2 duplicates by chance (95% range 16-30) against 27 observed, p = 0.166.
  - All 48 copy rows are low-risk women who did not recur.
  - The 383 rows match the paper's cohort exactly (n, mean age 40.87, SD 15.13, 81% female).
  - The split auditor's grouped-by-profile sensitivity run gives RF 0.936 vs 0.934 shipped. The copies do not inflate the score.
  - Precedents: caracas_cervical_cancer (21 copies kept after the same test, shipped 2026-10-15), breast_cancer_prediction, sepsis_survival.
  - The one 3-patient profile with both labels is a genuine ambiguity the task has, so LEAK-20's exception applies (as in caracas).
- **Concessions (wording only):**
  - Claims 51/56 are refuted as worded. Write "among the most common records (44 of 48 copy rows in the five most common profiles)".
  - Claim 53: for exact row copies the effect is 0.006-0.008, not 0.002-0.003. Give 0.002-0.008.
  - Cite LEAK-20 in the "keep all three" sentence.

**6. The IID split is the right and only possible regime (P4, SPLIT-1, USE-10, USE-11)**
- **Evidence:**
  - One row per patient and no patient id. The split mirrors a cold start over new patients.
  - Hidden-group probe: no hit.
  - No date column. The row order is sorted by `T` and then `Recurred`, not by time.
  - Split auditor's verdict: "right with notes ... No change to the split needed."
- **Concession:** the claim of at least 10 years of follow-up for every patient conflicts with a 2008-2023 cohort (split audit problem 1). Fix: write "the source states at least 10 years of follow-up" in `row` and the intro bullet. Censoring cannot be tested without dates, so there is no remedy on the data, and the split stays.

**7. The remaining doubts are measured and small, so they are notes, not blockers (P4, LEAK-6 Must: "a slight optimism with a known cause can stay with a note")**
- **`Risk` possibly assigned in hindsight:**
  - A crude ATA rule agrees with the recorded `Risk` in 337/383 rows.
  - The discordant rows are not pushed towards the outcome: 33% and 24% recurred in the two discordant groups, against 28% where the rule agrees.
  - `Risk` adds at most 0.007-0.010 AUC.
  - Dropping it would break USE-6: it would remove the clinical baseline the use case refines.
- **`M` found after staging:** 2 of 18 M1 patients are coded intermediate risk. Dropping `M` and `Stage` changes AUC by +0.0001 to +0.0013.
- **`Hx Radiothreapy`:** AUC 0.9219 without it vs 0.9221 with it (LR), 0.9271 vs 0.9285 (RF). Dropping it costs nothing measurable.
- **None of these is a failing Must.** "Independent failures are not conflicts" cuts both ways here: there is no unfixed Must to rescue, so nothing requires exclusion.
- **Concessions:**
  - (a) Precedents prompt 1 is fair. Relabel the `M` bullet `Potential leak, kept on purpose:` (as churn_telco_south_asia and melbourne_housing_market do), and record the fact that sets it apart from the radiotherapy column: `M` is a defined staging field and only 2 of 18 values are doubtful, while the radiotherapy column is undefined and undated and 6 of its 7 positives look like treatment of advanced disease.
  - (b) Whether to drop `Hx Radiothreapy` or keep it with a note is a weighing call for the curator. The blind reviewer wants it restored as a baseline feature; the precedent checker finds both options consistent. Either way the score is unchanged and the dataset ships.

**Judgment record (advocate's view)**
- **Verdict:** ship, with wording-only edits.
- **Validity:**
  - SEL holds.
  - USE-1/3/6 hold, fit direct (one clause added to `fit_reason`).
  - USE-5 holds under either reading of the label. PROV-17 is met: marked unverified, PDF requested.
  - LEAK-10 triggered and fixed (`Response` dropped).
  - LEAK-6: `Risk` and `M` kept with notes, effects ≤0.010 and ≤0.001.
  - LEAK-18/20: duplicates kept, p = 0.166.
  - SPLIT-1 holds.
- **Value:** TP-4 not `Trivial` (RF beats `Risk` 59/60); TP-5 not `Too Small` (36 positives per test fold).
- **Quality:** the `Hurthle` typo is fixed. `Stage` mismatches (12/383) are kept as recorded (CLEAN-11, as in caracas).
- **Weighed:** single clinic -, small n -, real clinical decision +, clean provenance (sha256, UCI, matches the paper) +.
- **For the curator:**
  - issue 2: get the PDF;
  - `Hx Radiothreapy`: drop or keep with a note;
  - `fit`: direct or approximate;
  - thyroid_discordant's untested `Trivial` marker.

</details>

<details><summary>Critic</summary>

**Critic, opening brief: differentiated_thyroid_cancer_recurrence (2026-10-20)**

**Position: ship only after changes.** No point asks for exclusion. The task is real (practitioner: fit direct after
`Response` is dropped), the `Response` drop is right (LEAK-10), the split is right (split audit), and `Trivial` does not
hold (TP-4). What is wrong is how the definition describes the label, the fit and its kept doubts, and a few claims in
its text that the audits refute.

**1. `fit="direct"` breaks USE-8: the label is unverified and a potential leak is kept (P3, Must)**

- **Problem.** USE-8 calls a fit approximate when there is "a potential leak kept on purpose" or "a label without a
  stated horizon". This definition has both: it keeps `M`, with 2 of 18 M1 patients at ATA intermediate risk, so their
  metastases "may have been found after the initial staging" (its own `Anomaly:` bullet). And the label "seems to count
  persistent disease", the paper is unread and the horizon is unclear (">= 10 years" on UCI, "10-year" and "fifteen
  years" in Khazaei 2024; practitioner, section 2).
- **Effect.** A user reads "direct" as "this mirrors the endocrinologist's decision". In fact recurrence by risk class
  is 4.8% / 62.7% / 100%, against about 3% / 21% / 68% for structural disease in Tuttle 2010 (practitioner). The label
  is broader than the `predicted` text says.
- **Evidence.** Precedents, prompt 2: churn_telco_south_asia (Lennart, 2026-10-15) has an undocumented label timing and
  is `approximate`; thyroid_discordant has an undefined label and is `approximate`. In this run, glioma was moved to
  approximate. `fit_reason` names neither the label nor the horizon.
- **Rule.** USE-8 (Must), USE-5 (Must, a label that was not checked), EV-7 (Must).
- **Remedy (fix the definition).** Set `fit="approximate"` until the paper is read. Make `fit_reason` name the
  unverified label (persistent disease probably counted, the horizon as the source states it) and the `M` doubt. Put the
  per-risk recurrence rates next to Tuttle 2010 in `predicted` or in the `Note:` bullet.

**2. 34 patients probably have the outcome at the prediction point; this is a cohort question left unwritten (P4, Must)**

- **Problem.** If `Recurred` counts persistent disease, then a patient with M1 or ATA high risk has, in the label's
  sense, the outcome already at staging. All 34 such rows are labelled recurred (claim audit 44; my count on the raw
  file).
- **Effect (measured, LR, 20 x 3 stratified folds, raw file without the two dropped columns).** ROC AUC is 0.929 on all
  test rows and 0.902 with the High/M1 test rows left out. `Risk` alone drops from 0.896 to 0.850 there. So about 0.03 of
  the score comes from patients whose label may already be fixed at staging.
- **Rule.** LEAK-36 (Must): "A value known at prediction time that rules the outcome out is a cohort question (LEAK-22),
  not a feature leak." LEAK-22 (Must): follow the paper's cohort. The paper's cohort is unknown (paywall).
- **Remedy (a note; no filter yet).** The ATA risk system does score these patients, so keep them. But add a `Note:` or
  `Potential leak, kept on purpose:` bullet with the 0.929 / 0.902 measurement. Add a question to REVIEW issue 2: if
  the paper counts persistent disease, check whether its cohort excludes patients with disease that never went away.

**3. Doubts on timing: one column dropped, another kept, under different labels, with no written reason (P4, Must)**

- **Problem.** `Hx Radiothreapy` is dropped on circumstantial evidence: LR 0.930 with and without it, and "Hx" reads as
  a history from before staging (blind review: "a legitimate baseline feature"). `M` has the same mechanism and the
  same nil effect (+0.001), yet it is kept and labelled `Anomaly:`. `Risk` is probably assigned retrospectively: the
  file uses 2015 categories on patients from 2008 on; 7 low-risk patients are N1b; 14 T3b patients are intermediate;
  100% of high-risk patients recurred. It has no note at all, although it adds 0.007-0.010 AUC (column audit). In the
  v0.2 copy, a suspected timing signal that is kept is written `Potential leak, kept on purpose:` (21 definitions).
- **Rule.** LEAK-6 (Must): measure before acting; a slight optimism with a known cause stays with a note. Consistency
  (principles.md, case 1; precedents, prompt 1).
- **Remedy (fix the notes).** Relabel the `M` bullet `Potential leak, kept on purpose:`. Add one such line for `Risk`:
  the discordant rows are not pushed toward the outcome, and the effect is at most +0.01 (column audit). Write the fact
  that sets the radiotherapy drop apart: the column has no definition or date, and 6 of its 7 positives are advanced
  disease. Otherwise keep the column with the same note (precedents, option b). Either choice is fine once the reason is
  written.

**4. The follow-up is stated as a fact although the sources disagree; censoring is untested (P4, Must)**

- **Problem.** `task_summary.row` and the first comment say "followed for at least 10 years". Khazaei 2024 puts the
  cohort at "January 2008 to December 2023". So patients diagnosed after about 2013 cannot have 10 years of follow-up,
  and their `No` may be censored. There are no dates, so this cannot be measured (split audit, problem 1; claim audit,
  untested item 2).
- **Rule.** LEAK-24 (Must, a target censored in the newest periods), which cannot be checked here. EV-7 (Must):
  cannot-verify is never stated as a pass.
- **Remedy (a note).** Write "the source states at least 10 years of follow-up". Add one `Note:` line on the
  conflicting cohort period and the possible censoring, and list it in REVIEW issue 2 for the PDF check.

**5. Claims in the definition that the audits refute (procedure, EV-7 Must; P7 for the text)**

- "The most common record of 14 coarse clinical fields" (accepted warning, Decision 3) is refuted. The copies fall in 7
  profiles, 20 of 48 in the most common one, 44 of 48 in the top 5 (claim audit 51).
- "Lowers the ROC AUC by 0.002-0.003" holds only for test rows whose feature vector occurs in train. For the exact row
  copies the sentence names, the drop is 0.006-0.008 (claim audit 53).
- "Beat it on 59 to 60 of them" depends on the configuration. Standardised LR beats `Risk` on 52 of 60, and the best
  substitute beats the `Risk` x `Gender` lookup on 47 of 60. CatBoost was not rerun (claim audit 49, 69).
  `Trivial` still fails (RF 59/60, gain 0.032).
- **Remedy (repair the text).** Correct the three sentences as the claim audit proposes. Give the LEAK-20 reason for
  keeping the 3-patient profile with both labels (precedents, decision 5).

**6. The use case names a decision that is not taken at this moment (P3, USE-1 Must; wording)**

- **Problem.** The use case says the clinician decides "how closely to follow the patient" at initial staging. The
  practitioner says follow-up intensity is "mostly set at the response assessment", the very step this task excludes.
  At staging the decisions are radioiodine, the TSH target and the initial schedule.
- **Remedy (fix the wording).** Rephrase `task_summary.use_case` to the decisions taken at that visit (practitioner,
  "What an expert would change").

**7. `Hx Smoking` has no stated meaning (P7, quality only)**

- **Problem.** 37 current smokers have `Hx Smoking = No`, so the column probably means former smoker. No source says
  so (column audit, problem 5).
- **Remedy (a note).** One line: "meaning not given by the source; probably former smoking". This is not a reason to
  hold the dataset.

**Judgment record**

```text
Verdict: ship after changes.
Validity: USE-8 departure (fit should be approximate; issue 1); LEAK-36/LEAK-22 cohort question, 34 rows that may have
  the outcome at staging, kept with a note (issue 2); LEAK-6 notes for M and Risk, a reason for the radiotherapy drop
  (issue 3); LEAK-24 untestable, write it as the source's claim (issue 4); LEAK-10 holds (Response dropped); SPLIT-1 holds.
Value: TP-4, Trivial refuted; TP-5 holds (36 positives per test fold).
Quality: EV-7 text repairs (issue 5); USE-1 wording (issue 6); Hx Smoking note (issue 7).
```

</details>

<details><summary>Advocate rebuttal</summary>

**Advocate rebuttal: differentiated_thyroid**

**Critic 1: `fit="direct"` breaks USE-8. Conceded on one of its two grounds; the outcome is a one-word change.**
- **What I concede.** In my brief I agreed to relabel the `M` bullet `Potential leak, kept on purpose:`. USE-8 (Must) lists "a potential leak kept on purpose" as approximate, with kick as its case. Once `M` carries that label, `direct` no longer matches the rule's text. So `fit="approximate"` follows, and `fit_reason` should name the `M` doubt and the unverified label.
- **What I dispute: the label ground.**
  - "A label without a stated horizon" does not apply: UCI states at least 10 years. The Khazaei wording conflicts with that, but that is point 4 (censoring), not a missing horizon.
  - A label that may include persistent disease is still the target the actor acts on. ATA 2015 [B19] says the initial risk estimates "the risk of persistent/recurrent disease". So USE-5 holds.
  - churn_telco_south_asia is not the same fact. Its label timing was undocumented relative to the prediction point. Here the open question is the label's breadth, and either breadth is the guideline's target.
- **What follows.**
  - `fit="approximate"`, with the reason "the `M` timing doubt kept on purpose; label breadth unverified".
  - Add the per-risk recurrence rates against Tuttle 2010 (4.8/62.7/100% here vs about 3/21/68% there) to the `Note:` bullet. This is cheap and true (practitioner).
  - If the PDF later clears `M` and the label, the fit can go back to direct.

**Critic 2: 34 patients may already have the outcome at staging (LEAK-36/LEAK-22). I accept the note and dispute the reading of the number.**
- **I agree** with the critic's remedy: keep the rows, add a note, and add the cohort question to REVIEW issue 2.
- **I dispute the claim that "about 0.03 of the score comes from patients whose label may already be fixed".**
  - Taking out the most certain cases lowers the AUC of any ranking, legitimate or not. `Risk` alone, the clinician's own staging estimate and a legitimate input under USE-6 (Must), falls by more (0.896 to 0.850) than the model does (0.929 to 0.902).
  - So the drop measures how hard the remaining subset is, not a leak.
  - The model's gain over `Risk` is about 0.033 on all rows and about 0.052 without the High/M1 rows. The task gets more discriminating on that subset, not less.
- **These patients belong in the cohort.** The ATA high-risk class exists to stage exactly these patients at this visit. LEAK-36 calls this a cohort question, not a feature leak, and LEAK-22's "follow the paper's cohort" cannot be applied until the PDF is read (PROV-17). The mildest remedy is the note, which is what the critic proposes.
- **Caveat:** I did not re-run the critic's 0.929/0.902 measurement. I take it as reported (EV-6). The note should give it as "AUC without High/M1 test rows", not as "leak share".

**Critic 3: inconsistent timing notes for `Hx Radiothreapy`, `M` and `Risk` (LEAK-6). Conceded.**
- Relabel `M` as `Potential leak, kept on purpose:`.
- Add a line for `Risk`: possibly assigned retrospectively; discordant rows not pushed toward the outcome (33%/24% vs 28%); effect at most +0.010 AUC (column audit).
- Write the fact that sets the radiotherapy drop apart: no definition or date, and 6 of 7 positives are advanced disease.
- Whether to drop the radiotherapy column or keep it with a note stays a weighing call for the curator. Both are score-neutral (LR 0.9219 vs 0.9221).
- On my side: `Risk` must not be dropped. USE-6 (Must) makes the clinician's own estimate an input, and the critic does not ask to drop it.

**Critic 4: the follow-up is stated as a fact (LEAK-24, EV-7). Conceded.**
This was already in my point 6. Write "the source states at least 10 years of follow-up", add a `Note:` on the 2008-2023 period and the possible censoring, and add both to REVIEW issue 2. There is no remedy on the data (no dates), and the split stays.

**Critic 5: refuted claims in the text (EV-7). Conceded.**
This was already in my points 3 and 5. Fix three sentences:
- "most common record" becomes "44 of 48 copy rows in the five most common profiles";
- "0.002-0.003" becomes "0.002-0.008";
- "59 to 60" names its models. Standardised LR gives 52/60; CatBoost is untested in the audit.

Also add the LEAK-20 reason to the sentence about the 3-patient profile. `Trivial` still fails under TP-4 (RF 59/60, gain 0.032), as the critic agrees.

**Critic 6: the use case wording (USE-1). Conceded.**
Rephrase to the decisions taken at that visit: radioiodine, the TSH target and the initial follow-up schedule (practitioner). The task, rows and label are unchanged.

**Critic 7: the meaning of `Hx Smoking` (P7). Conceded.**
Add one line: "meaning not given by the source; probably former smoking (37 current smokers have Hx = No)".

**Where we stand**
- **Agreed:** ship after changes. `Response` stays dropped (LEAK-10), the IID split holds (SPLIT-1), and the dataset is neither `Trivial` (TP-4) nor `Too Small` (TP-5, 36 positives per test fold). Every change is a wording, note or metadata fix, the "fix the definition / keep with a note" rungs of the remedy ladder.
- **Still open, for the curator:**
  1. Drop or keep `Hx Radiothreapy` (weighing).
  2. How the 0.929/0.902 subset measurement is worded in the note.
  3. Whether the fit returns to direct after the PDF is read (REVIEW issue 2).

</details>

<details><summary>Critic rebuttal</summary>

**Critic, rebuttal: differentiated_thyroid_cancer_recurrence (2026-10-20)**

**Conceded**

- **Advocate 1 (`Response` dropped, LEAK-10).** Conceded in full.
- **Advocate 3 (not `Trivial`, TP-4).** Conceded. The advocate also concedes that the sentence must say which models
  the counts are for (my point 5).
- **Advocate 4 (not `Too Small`, TP-5).** Conceded. There are 36 positives per test fold.
- **Advocate 5 (duplicates kept, LEAK-18/20).** Conceded. The advocate also concedes my wording fixes: "most common
  record", "0.002-0.008", and a LEAK-20 reason for the 3-patient profile.
- **Advocate 6 (IID split).** Conceded. The advocate also concedes my point 4: write ">= 10 years" as the source's claim.
- **Advocate 7 (`Hx Radiothreapy`).** Conceded: drop or keep is the curator's call. The condition is that the fact
  setting it apart from `M` is written, which the advocate concedes (7a).
- **Advocate 7 (`Risk`).** Conceded: a note is the remedy (LEAK-6). But the definition has no such note yet, so this
  is a change to make, not a statement of the current state.

**Disputed**

**Advocate 2: "fit direct; `approximate` is an optional one-word call"**

- **The advocate's own concession settles it.** In 7a the advocate agrees to relabel `M` as
  `Potential leak, kept on purpose:`. USE-8 (Must) lists "a potential leak kept on purpose" under **Approximate**.
  "Direct" requires that "the rows, the features, the label's timing and the split mirror the use case". Once the
  definition says it keeps a potential leak, `direct` breaks a Must. So this is not a weighing call for the curator.
- **"The horizon is stated" does not hold.** The advocate concedes in 6 that ">= 10 years" conflicts with the 2008-2023
  cohort. Khazaei 2024 also says both "10-year" and "fifteen years" (practitioner, section 2). A horizon the sources
  contradict is not a stated horizon.
- **"Valid either way" answers USE-5, not USE-8.** I concede that USE-5 holds: either reading of the label is what the
  ATA risk estimates. But fit is a separate Must about how closely the data mirrors the use case. The recurrence rates
  are 4.8% / 62.7% / 100% here, against 3% / 21% / 68% in Tuttle 2010, so the label is broader than its description.
- **Precedents agree.** churn_telco_south_asia (Lennart, 2026-10-15) was shipped `approximate` with a potential leak
  kept and an undocumented label timing; thyroid_discordant is `approximate` with an undefined label.
- **Remedy (unchanged).** Set `fit="approximate"` and make `fit_reason` name the label doubt and `M`.

**Not answered by the advocate: my point 2 (LEAK-36 / LEAK-22, Must)**

- **The facts.** All 34 High-risk or M1 patients are labelled recurred. If the label counts persistent disease, they
  may already have the outcome at staging. Measured: ROC AUC 0.929 on all test rows and 0.902 without these rows;
  `Risk` alone 0.896 and 0.850.
- **Why the advocate's points do not cover it.** The advocate's judgment record lists effects of <= 0.010 and <= 0.001,
  but leaves this 0.03 out. LEAK-36 makes it a cohort question to write down, not a feature leak to ignore.
- **Remedy (unchanged, mild).** Keep the rows. Add a note with the measurement, and a cohort question in REVIEW issue 2.

**Not answered: my point 6 (USE-1 wording)**

- The practitioner says follow-up intensity is "mostly set at the response assessment", the step this task excludes.
- Remedy, unchanged: rephrase the use case to the decisions taken at staging (radioiodine, the TSH target, the initial
  schedule).

**Net**

The verdict is ship after changes. Compared with my opening brief, two things changed:

- **Closed by the advocate's concessions:** follow-up wording (4), text repairs (5), `M` relabelled (part of 3).
- **Moved to the curator's call:** whether `Hx Radiothreapy` is dropped or kept, once the distinguishing reason is
  written.

Open for the mediator:

1. `fit="approximate"` is required (USE-8, Must), not optional.
2. The note on the 34 rows (LEAK-36).
3. The `Risk` note (LEAK-6).
4. The use-case wording (USE-1).

</details>

<details><summary>Mediator</summary>

**Mediator: differentiated_thyroid**

**Recommendation**

```text
Verdict: ship after changes.
Validity: SEL holds; USE-1 holds once the use case is reworded; USE-5 holds under either reading of the label; USE-8 triggered and fixed (fit="approximate": `M` is a potential leak kept on purpose); LEAK-10 triggered and fixed (`Response` dropped); LEAK-6: `M` and `Risk` kept with `Potential leak, kept on purpose:` notes (effects +0.001 and at most +0.010 AUC); LEAK-18/20: duplicates kept (p = 0.166); LEAK-22/36: 34 High/M1 rows kept, a cohort question open until the paper is read; LEAK-24: cannot be tested, written as the source's claim; SPLIT-1 holds.
Value: TP-4, `Trivial` refuted (RF beats `Risk` on 59/60 splits, gain 0.032); TP-5 holds (36 positives per test fold).
Quality: EV-7 text repairs; `Hx Smoking` note; `Stage` mismatches kept as recorded (CLEAN-11).
Weighed: single clinic -, n = 383 -, real clinical decision +, clean provenance (sha256, matches the paper's cohort) +.
For the curator: issue 1, label and cohort (PDF); issue 2, `Hx Radiothreapy` (a weighing call); issue 3, USE-8 wording (a rule gap); issue 4, thyroid_discordant's `Trivial` (precedent).
```

**Changes to make now (no decision needed)**

1. Set `fit="approximate"`. `fit_reason` names three gaps: the `M` timing doubt, the unverified label breadth and the single clinic. Rule: USE-8 (Must). Once `M` is a potential leak kept on purpose, "direct" breaks the rule's text, and the advocate conceded this.
2. Relabel the `M` part of the `Anomaly:` bullet as `Potential leak, kept on purpose:`. Write the fact that sets the radiotherapy drop apart: `M` is a defined staging field and only 2 of its 18 M1 values are doubtful, while the radiotherapy column has no definition or date and 6 of its 7 positives look like treatment of advanced disease. Rules: LEAK-6, consistency (precedents prompt 1, option a).
3. Add a `Potential leak, kept on purpose:` line for `Risk`. It was probably assigned retrospectively. The discordant rows are not pushed toward the outcome (33% and 24% recurred, against 28% where the rule agrees), and `Risk` adds at most 0.010 AUC. Keep `Risk` as an input. Rules: LEAK-6, USE-6.
4. Add a `Note:` on the 34 High/M1 patients. All 34 recurred. ROC AUC is 0.928 on all test rows and 0.901 without these rows, and `Risk` alone goes from 0.896 to 0.850. Removing the same number of other easy positives gives the same 0.901, so the drop shows how hard the remaining rows are, not a leak. Give the figure as "AUC without High/M1 test rows", not as a leak share. Rules: LEAK-36 (a cohort question, not a feature leak); EV-6/EV-8 (say where a number comes from).
5. In `predicted` or the label `Note:`, give the recurrence rate by risk class next to Tuttle 2010: 4.8% / 62.7% / 100% here, against about 3% / 21% / 68% there. Rules: USE-5, EV-7.
6. Write the follow-up as the source's claim: "the source states at least 10 years of follow-up", in `task_summary.row` and in the intro sentence of `curation_comments`. Add a `Note:` that the stated cohort period (2008-2023) conflicts with this, so labels may be censored, which cannot be tested without dates. Rules: LEAK-24, EV-7.
7. Repair three sentences the claim audit refutes. Rule: EV-7.
   - "the most common record" becomes "44 of 48 copy rows in the five most common profiles".
   - "0.002-0.003" becomes "0.002-0.008".
   - "59 to 60 of 60" names its models and adds that standardised LR beats `Risk` on 52 of 60.
8. In "we keep all three", give the reason: different patients with the same coarse record whose outcomes differ, a label ambiguity the task has (LEAK-20).
9. Reword `task_summary.use_case` to the decisions taken at the staging visit: radioiodine, the TSH target and the initial follow-up schedule. Rule: USE-1 (practitioner; the advocate conceded).
10. Add a `Hx Smoking` note: the source gives no meaning; it is probably former smoking, since 37 current smokers have `Hx Smoking = No`. Rule: P7 / LEAK-2.
11. Add to REVIEW issue 2 (the PDF check):
    - the definition of recurrence and whether persistent disease counts;
    - whether the paper's cohort excludes patients whose disease never cleared;
    - when `Risk` and `M` were recorded;
    - which 13 features the paper used;
    - the follow-up period.
12. Changelog entry and README regeneration under the house rules for the v0.2 copy.

**Issues for the curator (ranked)**

**1. Label definition and cohort (P3/P4; USE-5, LEAK-22, LEAK-36 Must; PROV-17).**
- **Problem:** the label probably counts persistent disease. All 32 High-risk and all 18 M1 patients recurred, and the rates by risk class are far above Tuttle 2010. If so, the 34 High/M1 patients may already have the outcome at staging.
- **Effect:** score 0.928 vs 0.901 with and without them. The same drop comes from removing any equally easy positives, so the rows inflate nothing beyond being easy. What is at stake is the cohort, not the score.
- **Critic:** LEAK-22 says follow the paper's cohort, and we don't know what it is.
- **Advocate:** ATA risk exists to stage exactly these patients, and either reading of the label is the "persistent/recurrent disease" that ATA 2015 says the initial risk estimates.
- **Decision needed:** read the Borzooei 2024 PDF. If its cohort excludes patients whose disease never cleared, follow it (LEAK-22). Otherwise keep the rows with the note. Until then: keep, with the note.

**2. `Hx Radiothreapy`: drop (current) or keep with a `Potential leak, kept on purpose:` note (P4; LEAK-10 and LEAK-6 Must; a weighing call).**
- **Effect:** none measurable. LR 0.9219 without vs 0.9221 with, RF 0.9271 vs 0.9285.
- **For dropping:** the column has no definition or date, and 6 of its 7 "Yes" rows are High-risk patients who recurred, 5 of them M1, which fits treatment after staging (practitioner, column audit).
- **For keeping:** "Hx" reads as history from before staging (blind reviewer). The curator moved from exclude to keep-with-a-note for weak leaks (LEAK-30, 2026-10-19). LEAK-38 does not apply here, because the column is named, not anonymised.
- **What would settle it:** the paper's definition of the column.
- **Rule note:** if the drop stands, this is the first drop on circumstantial evidence with no measured mechanism. Should it recur, it belongs as a sentence under LEAK-6, not as exceptions dataset by dataset (precedents option d).

**3. Does an unverified label alone make a fit approximate? (P3; USE-8 Must, a rule gap.)**
- **Why it is low stakes now:** the fit is already approximate because of `M`. This only decides whether the fit can go back to direct if the PDF clears `M` but not the label.
- **Critic:** the horizon is contradicted (">= 10 years" against the 2008-2023 cohort period; Khazaei says both "10-year" and "fifteen years"). Precedents: churn_telco_south_asia, thyroid_discordant and glioma (this run) are approximate.
- **Advocate:** UCI does state a horizon, and USE-5 holds under either reading of the label.
- **Decision needed:** whether to amend USE-8 to say if an unverified label definition is a "known gap" (precedents prompt 2, option d).

**4. thyroid_discordant's `Trivial` marker (P6; TP-4 Must; flagged precedent).**
- **Problem:** the marker comes from a screening note and was never tested under TP-4. Here `Trivial` is removed on TP-4 evidence.
- **Decision needed:** run the TP-4 test on thyroid_discordant, or record why the marker stands.
- **Also:** decide house_prices_nominal and diabetes_3, which have the same open "`Trivial` not borne out" issue in this run, the same way.

**Agreed facts**

- **Rows and source:** 383 rows, the paper's cohort (mean age 40.87, SD 15.13, 81% female). 108 recurred (28.2%). sha256 matches. OpenML 46605 is a re-upload of the same rows.
- **`Response`:** Excellent 1/208 recurred, Structural incomplete 89/91. Alone it gives AUC 0.978. It is assessed 6-24 months after therapy, so it is dropped (LEAK-10).
- **Split:** IID, 20 x 3 stratified folds, 36 positives in every test fold. No id or date column. The hidden-group probe finds nothing.
- **`Risk` and models:** `Risk` alone gives 0.896. RF gives 0.9285 and beats it on 59/60 splits; standardised LR on 52/60; HGB on 54/60. CatBoost was not rerun.
- **Duplicates:** 26 copies (48 rows), all low-risk women who did not recur. Permutation test: 23.2 expected by chance (95% range 16-30) against 27 observed, p = 0.166. A split grouped by profile does not lower the score.
- **`M`:** 2 of 18 M1 patients are intermediate risk. Dropping `M` and `Stage` changes AUC by +0.0001 to +0.0013.
- **`Stage`:** differs from AJCC 8th in 12 of 383 rows.
- **`Risk` hindsight check:** a crude ATA rule agrees with the recorded `Risk` in 337/383 rows. Discordant rows recurred at 33% and 24%, against 28% where the rule agrees.
- **High/M1:** all 34 High or M1 patients recurred.
- **Paper:** paywalled. The follow-up claim conflicts with the 2008-2023 cohort period.

**Re-measured here** (raw file without the two dropped columns, 20 x 3 stratified folds, seed 0, thread caps 2; standardised one-hot LR and RF with 300 trees):

| Test rows scored | LR | RF | `Risk` alone |
|---|---|---|---|
| All | 0.928 | 0.930 | 0.896 |
| Without High/M1 rows | 0.901 | 0.902 | 0.850 |
| Without an equal number of other positives the LR ranks highest | 0.901 | - | 0.881 |
| Without an equal number of random positives | 0.930 | - | 0.898 |

The models' gain over `Risk` is 0.032-0.034 on all rows and 0.051-0.052 without the High/M1 rows.

**Consistency with precedent**

- **Following precedent:**
  - The `Response` drop: caracas_cervical_cancer, mic, heart_failure_followup_survival. It rests on LEAK-10, not TP-6, so eryhemato does not bear on it.
  - Duplicates kept: caracas, breast_cancer_prediction, sepsis_survival. The drops on the other side (wine_quality, obesity_estimation, thyroid_discordant) all had continuous values.
  - IID split, one row per patient: breast_cancer_prediction, caracas.
  - Not `Trivial`: sepsis_survival and california kept. Opposite: fitness_club retired, where the single feature beat every method; here it is below on 52-60 of 60.
  - Not too small: musk kept with 13 positives per fold; parkinsons retired with 2-3.
  - `fit="approximate"` with a potential leak kept on purpose: kick, churn_telco_south_asia.
  - The `Potential leak, kept on purpose:` label: 21 definitions in the v0.2 copy, including churn_telco_south_asia and melbourne_housing_market.
- **Departures:** none left unexplained once changes 1-2 are made. The `M`/radiotherapy difference gets its distinguishing fact written (change 2).
- **Open departure:** dropping the radiotherapy column on circumstantial evidence has no precedent (issue 2).
- **Flagged precedent:** thyroid_discordant's untested `Trivial` marker (issue 4).

</details>
