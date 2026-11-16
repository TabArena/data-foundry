# treehouse_pediatric_tumor_type

**Outcome:** added. The paediatric and young-adult cut of the Treehouse Tumor Compendium v25.01 PolyA (Beale et al.
2025, GEO GSE294351): the diagnosis of a childhood or young-adult tumour (27 classes) from its RNA-seq expression
(54,571 genes) with age and sex, 3,256 datasets of 3,010 patients, grouped by patient. The AI recommends shipping it. Logistic regression reaches a macro ROC AUC of 0.999, but log loss still spreads the model families from 0.140 to 0.385, so it ranks models (issue 4). Every gene is kept.
The panel's two fixes are applied. Every expression value is now rounded the same way. Our first fix had rounded only TCGA's and TARGET's values, which left them with more written decimals than the other studies, a mark of the source study that a model could read. And the five second deposits (THR49) of NCI sarcoma tumours, linked to their first deposit by similarity only, are dropped: 5 of 3,261 datasets, 3,256 remain. The scores
are optimistic for a new hospital, because diagnosis and study are entangled (issue 1).

**Main points:** Confirm the patient split with its stated optimism (decide with `tcga_pancancer_tumor_type` and
`cns_tumor_methylation_classification`), keep age and sex although their missingness follows the study, keep
acute megakaryoblastic leukaemia as a class beside acute myeloid leukaemia, and keep every gene.

**Record judgment:** valid. A data descriptor in Scientific Data with a public GEO deposit, consistently processed
RNA-seq from 37 studies; the paediatric cut is a task of its own beside `tcga_pancancer_tumor_type` (336 TCGA rows of
young adults overlap). Fit approximate: tumours of settled diagnosis, diagnosed from scratch, stand in for the case a
tumour board brings. Priority 3: gap +, use case 0, source +, shape +, risk -.

**Issues for Lennart:**

1. **Hold out patients, not studies, with the optimism stated?**

   * **Problem:**
     - Within a diagnosis, the expression tells one study from another at a median ROC AUC of 0.97.
     - Holding out the study instead of the patient lowers accuracy from 0.984 to 0.85 (TARGET's acute myeloid leukaemia falls from 0.98 to 0.35; without it, 0.945).
     - So the scores under the patient split are optimistic for a hospital whose sequencing the compendium does not hold.
   * **Effect on the task:** models are ranked on new patients of known studies; part of what they learn is the study[^s1].
   * **Experiments:** logistic regression on 100 principal components, out of fold by patient (29 study pairs, 0.75 to 1.00); leave one study out where a class keeps 30 or more training datasets (2,345 datasets). With its largest study held out glioma keeps 0.91 (0.98), neuroblastoma 0.99 (1.00), osteosarcoma 0.99 (0.99).
   * **Consistency:** `sarcoma_methylation_classification` (2026-10-22) kept the patient split against a site batch[^p1]. The same call is open as issue 3 of `tcga_pancancer_tumor_type` and is taken in `cns_tumor_methylation_classification` (patient split kept, optimism stated): decide the three alike.
   * **Panel:** the advocate, both auditors, the practitioner and the precedent checker are for the patient split; the critic accepts it if the numbers stay in the splits comment and the three are decided together. A cross-study variant is a second dataset, not a fix.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Patient split, optimism stated (implemented) | 10 x 3-fold grouped by patient; the splits comment gives the 0.984 to 0.85 drop | every class trained and tested; matches the sarcoma call | scores optimistic for a new hospital |
     | B | Split by study | hold out whole studies | stands for a new hospital | 11 of 27 classes come 90% or more from one study and leave training when it is tested |
     | C | A as shipped plus a cross-study variant | a second dataset over the classes several studies hold | measures transfer across studies | a second dataset to curate; fewer classes |

   * **Recommendation:** A, decided together with the two sibling issues. **Decision:** A, B or C?

   **Notes for the AI:** on B or C, the splits need a study column kept as the group (`study_id`), never as a feature; re-run the task and group probes. Apply the same choice to `tcga_pancancer_tumor_type` issue 3 and `cns_tumor_methylation_classification` (its chip-split change) unless the curator sets them apart.

   [^p1]: Precedent: `sarcoma_methylation_classification`, 2026-10-22, IID by patient kept against the site batch.
   [^s1]: **SPLIT-1** (Must): the split is the one that most closely mirrors the real-world application. **SPLIT-23** (Must): the source's use case decides what one prediction is and what is known about a new group. **LEAK-39** (Must): rows of one class recorded through a separate route, found by a recording fingerprint, are dropped when models recognise them and the route cannot be aligned.

2. **Keep age and sex although their missingness follows the study?**

   * **Problem:**
     - St Jude's deposit gives no age for 282 of its 695 datasets, and four other studies give no age or no sex at all.
     - So a missing age marks the two classes St Jude holds alone: acute megakaryoblastic leukaemia (89% missing) and choroid plexus carcinoma (96%), at ROC AUC 0.90 and 0.92 alone.
     - A tumour board always knows the patient's age and sex, so this missingness is not realistic.
   * **Effect on the task:** small: age and sex as values lower the log loss from 0.193 to 0.189, the missing indicators on top to 0.183 (3%); for acute megakaryoblastic leukaemia from 0.365 to 0.270.
   * **Experiments:** logistic regression on 100 principal components, first fold of 3 repeats; the task gamer measured about 0.006 for the same features, matching.
   * **Consistency:** no precedent; the curator left calls on values missing or filled by route open for the cross-dataset review page, and the call is taken here per dataset[^a2].
   * **Panel:** the builder, the advocate and the task gamer ("defensible") keep both; the critic and the practitioner find the missingness unrealistic, and the critic asks for an explicit call[^a1].
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep age and sex, with the note (implemented) | both as inputs, missing as missing; the curation comments name the leak | real inputs a tumour board uses; gain from the missingness is 3% | a model can partly read the study from missingness |
     | B | Drop age and sex | expression only | no missingness mark | loses their own signal (0.193 to 0.189) |

   * **Recommendation:** A. **Decision:** A or B?

   **Notes for the AI:** on B, drop `age_at_diagnosis` and `sex` in `_clean`, update `known`, the curation comments and the notes on age; re-run `dataset check` and the task probe.

   [^a2]: Earlier call: the curator's decisions page of the large-datasets run (Lennart, 2026-11-09) kept the rule question on late or missing values open for the review page.
   [^a1]: **LEAK-15** (Must): a recording artefact that runs through several features that matter in practice and cannot be undone retires the dataset; a subset does not help when it also separates same-label rows. **USE-6** (Must): anything known at the prediction point is a legitimate input.

3. **Keep acute megakaryoblastic leukaemia as a class beside acute myeloid leukaemia?**

   * **Problem:**
     - Acute megakaryoblastic leukaemia (88 patients, 99% from St Jude) is a subtype of acute myeloid leukaemia in the WHO classification, yet a class of its own here.
     - Log loss charges a call of the parent type in full.
   * **Effect on the task:** the two myeloid classes separate well under the patient split (4 of 452 and 7 of 93 confused), so the class mostly costs on borderline cases.
   * **Consistency:** decide alike with `tcga_pancancer_tumor_type` issue 2 (colon and rectum adenocarcinoma) and `sarcoma_methylation_classification`, which merged myxofibrosarcoma and undifferentiated pleomorphic sarcoma[^c1].
   * **Panel:** the practitioner keeps it (it has its own management); the precedent checker points to the sarcoma merge; all agree to decide it alike with the siblings.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep the source's labels, with a hierarchy note (implemented) | 27 classes as harmonised by the source; the note names the subtype and the catch-all classes | the source's labels; the subtype is treated differently | a subtype beside its parent |
     | B | Merge into acute myeloid leukaemia | 26 classes | no parent and child as rivals | loses a distinction clinicians make; departs from the source |

   * **Recommendation:** A. **Decision:** A or B?

   **Notes for the AI:** on B, map `acute megakaryoblastic leukemia` to `acute myeloid leukemia` in `_clean` before the class floor, cite the WHO hierarchy (TP-7), update the counts and re-run `dataset check` and the task probe.

   [^c1]: **USE-5** (Must): predict what the actor would act on, at the resolution they act on it. **TP-7** (Must): when the definition builds the target itself (merged or dropped classes), use an established convention.

4. **Keep all 54,571 genes although the task is close to saturation?**

   * **Problem:**
     - Logistic regression reaches 0.965 accuracy and a macro ROC AUC of 0.999, and the blind reviewer proposes a filtered gene set.
     - Log loss still spreads the model families from 0.140 to 0.385 (paired standard error 0.004).
   * **Effect on the task:** none if kept; a filter would make a narrower, different dataset.
   * **Consistency:** the `coad_colon_adenocarcinoma` precedent[^p2] and the curator's acceptance of this record as a large-features candidate (2026-11-08)[^w1].
   * **Panel:** the blind reviewer for a filtered set; every other agent against.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep every gene (implemented) | 54,571 genes; only all-zero and copied genes dropped | the width is the point of a large-features dataset; families still spread | heavy for some models |
     | B | Filtered gene set | keep the most variable genes | lighter | width is no reason to drop columns; a different task |

   * **Recommendation:** A, no action. **Decision:** A or B?

   [^p2]: Precedent: `coad_colon_adenocarcinoma`, 2026-10-15 (Lennart), ships 36,355 features; a model's input cap is never an argument.
   [^w1]: **TP-3** (Must): if tuned methods spread, keep the dataset. **CLEAN-22** (Must): columns leave for what they are, never for how many there are.

**Review panel:** ship after changes (mediator). Full panel; the rebuttal round was skipped because the advocate's and the critic's briefs converged. Claim audit: no claim refuted. Column audit: one cleaning fix, the precision mark left by the TPM rounding (applied). After the fix, 98% of the positive values of every study are written with 15 or more decimals (the direct count). The leak probe's format check still scores macro ROC AUC 0.975 (0.978 before), but it counts at most 8 decimals, so it reads which genes are zero, which is expression, not the mark. Split audit: right with notes (patient split, optimism stated). Task gamer: barely gameable (formats about 0.002 log loss). Blind review: include with changes (finds it near-trivial and too wide; issue 4). Applied with no decision: every TPM rounded alike, the five THR49 second deposits dropped, the near pairs checked by id noted, diagnosis from scratch named in the fit, the Comitani et al. metrics re-read (fallback kept). Disputed and handed over: the split (issue 1), age and sex missingness (issue 2), the AMKL class (issue 3), width (issue 4). The panel's reports below predate the drop (3,261 datasets; 3,256 after it).

<details><summary>Mediator: treehouse_pediatric_tumor_type</summary>

```text
Mediator report: treehouse_pediatric_tumor_type (2026-11-09)

SUMMARY
- Recommendation: ship after changes. Two changes need no decision:
  (1) on_tpm_grid returns the rounded value for every entry, the format probe is re-run and the curation comment is corrected (LEAK-13, Must);
  (2) the 5 THR49 SAME_TUMOUR copies are dropped (SPLIT-24, Must).
- The advocate and critic converged and there was no rebuttal round. No fact is in dispute, so I ran no new experiment.
- Four issues go to the curator, all weighing calls:
  1. donor split vs study split, decided together with tcga_pancancer issue 2 and cns_tumor_methylation issue 2;
  2. age/sex missing by study;
  3. the AMKL/AML hierarchy, decided together with tcga COAD/READ and sarcoma MFS/UPS;
  4. width and near-saturation (no action recommended).
- Precedent: consistent once change (2) is made.

JUDGMENT RECORD
Verdict: ship after changes.
Validity:
- SEL-1 holds.
- USE-1 holds, approximate fit (diagnosis from scratch: no provisional diagnosis input, 27 of 111 classes, test patients come from studies already in training).
- LEAK-1 / USE-3 hold.
- LEAK-13 triggered three times:
  - age precision: fixed;
  - TPM grid: fixed;
  - the new precision mark left by our own on_tpm_grid: fix now (change 1).
- LEAK-17 fixed by donor ids.
- SPLIT-24 triggered by the similarity links: fix now by dropping the copies (change 2).
- LEAK-15/39: study entanglement and missingness by study are kept with notes (curator issues 1 and 2).
- SPLIT-1/23 hold: grouped by donor.
- PROV-6/7: distinct from tcga_pancancer_tumor_type.
Value: TP-3 keep. Macro AUC is 0.999, but log loss still spreads model families 0.140-0.385 (paired SE 0.004). TP-4 is not triggered (best single gene skill 0.105). TP-8: at least 3 donors per class per test fold, as in sarcoma.
Quality: CLEAN-22, no gene filter (width is no reason to drop features).
Weighed: gap +, source +, shape +, study risk -, fit approximate.
For the curator: issues 1-4 below.

CHANGES TO MAKE NOW (no decision needed)
1. LEAK-13 (P4, Must). on_tpm_grid recomputes only the off-grid TCGA/TARGET values.
   - Effect: those rows now carry 15 written decimals against 12 for every other study. The gamer sees the same two groups (17 vs 12-13 repr digits). Format alone scores macro AUC 0.978. The format features lower LR log loss 0.1531 -> 0.1512, positive on all 30 splits and above the noise band (±0.001).
   - Fix: return np.log2(np.round(np.exp2(v)-1, 2)+1) for every value. On-grid values move by less than 1e-9, and the column auditor checked that both groups then read 15 decimals. The alternative is to round all output to 12 decimals.
   - Then re-run the format probe and expect format_alone well below 0.978.
   - Rewrite the curation_comments sentence "the genes' written decimals ... only say zero or not" (dataset.py line 201). The evidence contradicts it.
2. SPLIT-24 (P4, Must) with LEAK-19. The six THR49/THR30 links rest on Pearson >= 0.9958 plus sex and age, not on a source id.
   - Fix: drop the 5 THR49 copies (0.15% of rows), as in the emscad, audiology and qsar_tid_11 precedents.
   - This is not a conflict. Keeping rows is not a higher-ranked Must, so the builder's option (a) has no rule to stand on.
   - After the drop, the definition, the counts in the notes and decision 2 need updating.
3. LEAK-19 note. The 4 cross-donor pairs above 0.99 (top 0.9914, two TCGA cervical samples, both female, age 24) differ only by id. Write in the notes that they were checked by id only.
4. USE-8 (Should). Say in fit_reason that this is diagnosis from scratch, with no provisional diagnosis input.
5. MET-1. Comitani 2023's metrics were read from a search snippet only. Look once more. This does not change the log loss fallback, because the source names no single metric.

ISSUES FOR THE CURATOR (ranked)
1. Donor split vs study split (P4: SPLIT-1, SPLIT-23, SPLIT-29, SPLIT-31, LEAK-39; a weighing call).
   - Problem: the expression names the study within a diagnosis (median AUC 0.97). Holding out the study lowers accuracy 0.984 -> 0.85 (0.945 without TARGET's AML; TARGET AML falls 0.98 -> 0.35), so the scores are optimistic for a new hospital.
   - For the donor split (advocate, both auditors, practitioner, precedent checker): a study split leaves 11 of 27 classes untestable; the sarcoma precedent (2026-10-22) kept IID by patient against the site batch.
   - Critic: accepts the donor split, but the numbers must stay in splits_comment and the call must be made together with its siblings.
   - Decision needed: confirm (a), the donor split with the optimism stated, together with tcga_pancancer issue 2 and cns_tumor_methylation issue 2. Option (c), a cross-study variant, is a variant, not a fix.
2. Age and sex missing by study (P4: LEAK-15, USE-6; a weighing call). This is the known note, "Potential leak, kept on purpose: age and sex are missing by study".
   - Problem: missing age marks AMKL (82/93) and choroid plexus carcinoma (23/26), AUC 0.90/0.92. Log loss 0.189 -> 0.183 overall, and 0.365 -> 0.270 for AMKL.
   - For keeping (builder, advocate, gamer: "defensible"): age and sex are real inputs, and the gain is 3%.
   - Against (critic, practitioner): a tumour board always has age and sex, so this missingness is unrealistic. The critic asks for an explicit curator call.
   - Decision needed: keep with the note, or drop age and sex. The curator kept this kind of call (late-filled and missing values) open for the cross-dataset review page.
3. AMKL as a class beside AML, and the broad labels (P3: USE-5, TP-7; Should, a weighing call).
   - Problem: AMKL is a WHO subtype of AML and 99% from St. Jude, so log loss charges an AMKL -> AML call in full. The NOS class carries 10x its row share of the log loss.
   - For keeping: these are the source's harmonised labels, and AMKL has its own management (practitioner).
   - For merging: the sarcoma MFS/UPS merge.
   - Decision needed: keep with a note on the hierarchy, or merge. Decide alike with tcga COAD/READ and sarcoma MFS/UPS.
4. Width and near-saturation (P6: TP-3, CLEAN-22). Recommend no action.
   - Blind reviewer: logreg reaches 0.965 accuracy; proposes a filtered gene set.
   - Against: CLEAN-22 and the coad precedent say width is no reason to drop features, and a model's input cap is never an argument. Log loss still separates the families. The curator accepted this record as a large-features candidate.
   - Decision needed: confirm "width is the point", with a note at most.
Kept as notes: the class floor of 10 (TP-8, sarcoma precedent; all agree) and the overlap of 336 rows with tcga_pancancer (PROV-6/7; all agree).

THE TASK GAMER'S EXPLOITS, MAPPED
- Decimal digits of the expression values: LEAK-13. This is new; no note covers it, and the comment denies it. Gain 0.0019 LR, 0.0074 LGB (inside the noise band). Resolved by change 1.
- Missing age and sex: LEAK-15, under the known note. The measured gain (about 0.006) matches the note's 0.189 -> 0.183, so it is no issue.
- Near copies, sentinels, age format: nothing found.
- Not checked: row order, and a classifier of training rows against test rows.

AGREED FACTS
- 3,261 rows, 3,010 donors, 27 classes, 54,571 genes plus age and sex.
- 0 shared donors across the 30 splits; at least 3 donors of every class in every test fold.
- 0.0% exact copies across the split.
- No column from after the prediction point.
- Log loss computable on every fold (dummy 2.584).
- Study within diagnosis AUC 0.97; study held out 0.984 -> 0.85; 11 of 27 classes come from one study.
- The precision mark (15 vs 12 decimals; format_alone 0.978) is caused by on_tpm_grid, and rounding every value removes it.
- The SAME_TUMOUR links are similarity-based (0.9958 against 0.9913 for the next pair).
- The age/sex missingness gain is 0.189 -> 0.183.
- Log loss spreads the families 0.140-0.385.

CONSISTENCY WITH PRECEDENT
The precedent checker found 4 of 5 calls consistent:
- donor split (sarcoma);
- labels kept (but AMKL must be decided alike with COAD/READ and MFS/UPS);
- class floor of 10 (sarcoma, TP-8 Cases);
- TCGA overlap (PROV-6/7).
The SAME_TUMOUR join departed from SPLIT-24 with no fact written down. Change 2 removes that departure, in line with emscad, audiology and qsar_tid_11. No drift, and no third exception of one kind.
```

</details>

<details><summary>Claim audit: treehouse_pediatric_tumor_type</summary>

```text
Claim auditor: treehouse_pediatric_tumor_type (2026-11-09)
Verdict: no claim refuted; ship after the curator's calls. (script in the run folder) (full container built from the definition).

claim | source | test | result | evidence | rule
Shape 3,261 rows, 27 classes, 3,010 donors, 54,571 genes + age + sex | claims 9-14, task_summary | built container | holds | 3261 x 54575 incl. donor/target; 27 classes; 3,010 donors; 54,573 features | -
Donor not a feature, target not a feature | implied | feature_columns(c) | holds | donor and diagnosis absent | LEAK-1
No donor on both sides of a split | splits_comment | train/test donor intersection on all 30 splits | holds | 0 shared donors | SPLIT-23, LEAK-17
>=3 donors of every class in every test fold | claim 15 | per fold count | holds | min 3; all 27 classes in every test fold | TP-5, TP-8
Metric computable on each fold (MET-2) | metric block | prior-proba dummy through scorer on 30 folds | holds | log loss 2.57-2.60 (claim 36 dummy 2.584) | MET-2
Metric fallback log loss, no source metric | claim 29 | spec read; descriptor trains no classifier (builder's reading, not re-fetched) | holds (Comitani's metrics from a snippet only: untested) | origin=fallback, reason names where looked | MET-1, MET-4
No near copy across donors beyond SAME_TUMOUR (max other-donor 0.9913, p99 0.9863) | claim 12, decision 2 | Pearson over all genes of the final frame, cross-donor max | holds | top pair 0.99136 (TCGA cervical, both 24 F), p99 0.9859, 4 rows >0.99 | LEAK-17, LEAK-19
Ages 0-32 | claim 5 | describe | holds | 0-32, 407 missing (2854 of 3261 present) | -
Sex missing 311 | claim 22 | value_counts | holds | 311 NaN | -

Weak points (untested, not refuted), ranked:
1. The near-copy gap is thin: the top cross-donor pairs (cervical 0.9914, same age 24, same sex; ALL 0.9902 one sex missing; ALL 0.9891 both male, age missing) sit 0.004 below the SAME_TUMOUR pairs and match on demographics. Whether these are other donors rests on the ids only (different TCGA barcodes / different study ids). Remedy: a note that the 4 rows >0.99 were checked by id, or look up the two cervical barcodes (LEAK-19). Effect on scores negligible (4 rows).
2. Comitani 2023 metrics read from a search snippet only (MET-1 asks for the look once more); does not change the fallback because no single metric is named.
3. Builder's issues 1 and 3 (study entanglement, missingness by study) are weighing items; I found nothing that contradicts their numbers.
```

</details>

<details><summary>Column audit: treehouse_pediatric_tumor_type</summary>

```text
Column auditor: treehouse_pediatric_tumor_type (2026-11-09)
Verdict: ship after one cleaning fix (precision mark left by on_tpm_grid); no new leak. Builder's issues 1-5 stand.

Prediction point (first curation_comments bullet): a child/AYA tumour has been sequenced; diagnosis confirmed from
expression plus age and sex.

COLUMN TABLE (column | meaning | known at prediction? | dtype and cleaning | verdict | rule)
- 54,571 gene columns (HUGO symbols) | log2(TPM+1) per dataset, TOIL/RSEM pipeline (Beale et al. 2025) | yes, measured
  on the sequenced sample | float64; all-zero genes and exact-copy genes dropped; per-dataset TPM (no cross-row
  scaling, LEAK-30 ok); TPM put on RSEM's 0.01 grid | CLEANING PROBLEM (see 1) | LEAK-13
- age_at_diagnosis | patient age at diagnosis, years (source age_at_dx) | yes | float, `unknown` -> NaN (407),
  floored to whole years to remove the study's precision mark | fine; missingness by study is kept on purpose
  (see 2) | LEAK-13, USE-6
- sex | patient sex | yes | categorical, `unknown` -> NaN (311) | fine; same missingness note | USE-6
- donor | anonymised patient key linked across ids (+ SAME_TUMOUR pairs) | n/a, group | categorical, group column,
  dropped by feature_columns | fine (group, not feature) | SPLIT-24 for the six similarity pairs (builder issue 2)
- diagnosis | source's harmonised `disease`, 27 classes with >=10 donors | target | categorical | fine; subtype/NOS
  labels as builder issue 3 | TP-7, USE-5
Dropped correctly: icd_disease (target encoding), th_dataset_id / study_accession / study_dataset_id /
study_donor_id (ids; TARGET/TCGA prefixes name the source), study_id / source_name (batch), organism / pedaya
(constant). Nothing awarded after diagnosis is present (no treatment, survival, relapse fields).
Dtype probe (probes/dtype): 0 flagged of 54,573; no codebook, the clinical columns checked by hand above. No ordinal.

PROBLEMS, RANKED
1. (P4, LEAK-13, cleaning) on_tpm_grid leaves a new precision fingerprint of TCGA/TARGET. It replaces only the
   off-grid values (TCGA/TARGET, ~99.8% of their positives) with recomputed full-precision floats and keeps the others
   as published (file precision). Measured on the first 1,000-2,000 genes of the pedaya matrix, median written decimals
   (%.15g) of a row's positive values: raw 12 for both groups; after on_tpm_grid TCGA/TARGET 15 (11-15), others 12
   (11-13). So the decimals of any gene now name the source, which is what the rounding meant to remove; the leak
   probe's format_alone = 0.978 (format features of the top 1,000 genes) is consistent with it, though the curation
   comment says the decimals "only say zero or not". Mildest remedy: in on_tpm_grid return `rounded` for every value
   (np.log2(np.round(np.exp2(v)-1,2)+1) everywhere; values already on the grid change by <1e-9): median decimals then
   15 for both groups (checked). Alternative: round the output to 12 decimals (11-12 for both). Re-run the format probe.
2. (P4, LEAK-15/USE-6, weighing) age/sex missing by study, marking AMKL and choroid plexus carcinoma (missing-age AUC
   0.90/0.92; leak probe missing-only 0.56). Kept on purpose, documented, gain 3% log loss. Agree with keep; the
   panel/curator may prefer it named a curator question (builder issue 3 iv).
3. (P4) Study entangled with diagnosis: no study column ships, but expression carries it (builder issue 1). Not a
   column problem; agree with donor split plus stated optimism.
No other leak found: single-gene probe top is GPX8 0.83 (biology), drop-one changes nothing, no exact copies.

```

</details>

<details><summary>Split audit: treehouse_pediatric_tumor_type</summary>

```text
Split auditor: treehouse_pediatric_tumor_type (2026-11-09)
Verdict: RIGHT WITH NOTES. No re-split. I ran no new model: the builder already measured the alternative split (leave one study out), and I read those numbers.

Regime. The use case is a tumour board diagnosing a new patient's tumour. That calls for a new-entity split, which the dataset declares: grouped by donor, labels per_group, each row predicted, no context. The definition has no time column, and none is implied: the compendium is cross-sectional, and relapse samples stay with their donor. This is correct under SPLIT-1 and SPLIT-23.

Group id. The donor is a real patient id, not a similarity cluster. It joins the datasets that share any of five source ids: TARGET USI, TCGA barcode, Treehouse donor id, study donor id and St. Jude id. It also adds six explicit SAME_TUMOUR pairs, NCI Ewing tumours deposited twice (THR49/THR30, r 0.9958-0.9973, same sex, age within a year). That gives 3,010 donors, 216 of them with 2-8 datasets. The hash is only for anonymity (anonymize_ids), and the id is built before hashing. LEAK-17 is fixed.

Hidden groups and near copies. probes/near_copies.json: the 1st percentile of within-donor correlation is 0.857 and the median 0.958. Across donors the 99.99th percentile is 0.979, 7 pairs pass 0.99 (the joined ones), and the largest unjoined pair is 0.9913. Exact copies across the split: 0.0% of 32,610 test rows. IID scores 0.996 and grouped scores 0.994 (gap 0.001, LightGBM, top 1,000 genes), so few twice-deposited patients can remain. Minor note: 343 cross-donor pairs pass 0.98. They are most likely tight classes such as ALL, but nobody has checked them against age and sex the way the 0.99 pairs were. Mildest remedy: none needed now. An optional spot check is to list the pairs above 0.985 with equal sex and age within one year.

Problems, ranked by principles.md:
1. (P4, SPLIT-29/31, LEAK-39; builder issue 1) The donor split stands for new patients from studies the training data already holds, not for a new hospital. Within a diagnosis, the study separates at median AUC 0.97. Holding out the study lowers accuracy from 0.984 to 0.85 on rows whose class keeps 30 or more training datasets (0.945 without TARGET's AML; TARGET AML falls from 0.98 to 0.35). The scores are therefore optimistic for an unseen sequencing site, and splits_comment says so with these numbers. A study split would take 11 of the 27 classes (552 datasets) out of training whenever their study is tested, so it cannot be the main split. Mildest remedy: keep the donor split and the disclosure. A cross-study variant over the classes several studies hold could follow later; the curator's call.
2. (P4, TP-8; builder issue 4) Minimum test donors per class per fold is 3 (breast invasive carcinoma, synovial sarcoma) and 4 (DNET, hepatoblastoma). That is what the 10-donor floor is designed to give with 3 folds, and stratification holds in every fold. These classes hold 5.4% of test rows and about 19% of a logistic model's log loss. With 10 repeats, the per-class estimates are noisy but usable. Remedy: none; 3 folds was the right choice over 5 for this reason.
3. (P4, LEAK-15; builder issue 3) Age and sex are missing by study. That marks AMKL and choroid plexus carcinoma, which only St. Jude holds, and it travels across the donor split because the test donors come from the same studies. Gain: log loss 0.189 to 0.183. This is a leakage note rather than a split defect; it comes from the same study entanglement as problem 1. No split remedy.

Checked and fine: train 2,151-2,186 rows and test 1,075-1,110 rows per fold; 10 repeats x 3 folds; donor-disjoint by construction (the grouped splitter on donor); no temporal fields to check (gap, label delay, season do not apply).
```

</details>

<details><summary>Domain practitioner: treehouse_pediatric_tumor_type</summary>

```text
Domain practitioner report: treehouse_pediatric_tumor_type
Actor played: a molecular pathologist on a paediatric molecular tumour board (the Treehouse "comparative analysis" and
Comitani et al. 2023 setting), with a new child's tumour RNA-seq in hand, deciding whether the histological diagnosis
is confirmed or should be revised / sent for further workup.

FIT: approximate (USE-1, USE-8). The actor, moment and decision are real and the source names "infer molecular
diagnosis" as a use, but every row is a tumour of settled, mostly textbook diagnosis from a study already in training,
while the board consults a classifier for the unclear, rare or off-centre case, often sequenced elsewhere.

1. Inputs at the prediction moment (USE-3, USE-6)
- Expression, age and sex: I have all three. Fine.
- I would ALWAYS have age and sex; here they are missing by study (St. Jude THR24/THR37 etc.), which marks AMKL and
  choroid plexus carcinoma (missing-age AUC 0.90/0.92; log loss 0.189 -> 0.183). This is not what I would face. Gain
  is small (about 3%), so I accept "keep with note", but my preference is to drop the missingness signal rather than
  the values (e.g. ship age/sex but note that a model should not lean on missingness), or accept it as small.
- What I would also have and is missing: the pathologist's provisional histological diagnosis and the tumour site /
  sample type (primary, relapse, metastasis; bone marrow vs solid). In the confirm/revise use, the provisional
  diagnosis is the main input; without it the task is "diagnose from scratch", a harder and different question. Not
  fixable from this source (it gives only the harmonised final label), so it is a named gap, not a defect.
- Tumour purity is not given; real cases with low purity are the hard ones. Not fixable.

2. Target (USE-5)
- The harmonised diagnosis is what I act on, at roughly the right resolution for most classes. Concerns, ranked:
  (a) AMKL as a class beside AML: clinically it is an AML subtype (WHO); a model calling an AMKL "AML" is not wrong for
  me. Under log loss it is penalised fully. Shipping as the source labels it is defensible (the source's harmonised
  labels, AMKL does have its own management), but the note should say a flat label set ignores the hierarchy.
  (b) "glioma" lumps low- and high-grade, which is the distinction I most need in CNS tumours; "supratentorial embryonal
  tumor NOS" and "lymphoma" are catch-alls. Keep as source labels (TP-7), noted already.
  (c) Dropping the 84 diagnoses with <10 donors removes exactly the rare entities where a classifier earns its keep;
  the shipped task is closed-set. Real classifiers (Comitani; the DKFZ methylation classifier) also restrict to
  trained classes and add a "no confident match" outcome. Acceptable, but it is a main reason the fit is approximate.
- I want a probability per class (to apply a confidence cut-off and abstain), not a hard class. The task gives that.

3. Rows and test data (USE-10)
- One row = one sequenced sample; I decide per tumour/patient. Most donors (2,794 of 3,010) have one dataset, so
  per-sample scoring is close to per-patient; scoring each sample alone is fine since I diagnose each sample.
- Test = new patients from studies in training. My real case is a new patient from my own hospital's sequencing,
  i.e. closer to a held-out study. The builder measured the gap: accuracy 0.984 -> 0.85 with the study held out
  (0.945 without TARGET's AML). The donor split is the only one that keeps the 11 single-study classes, so I agree with
  issue 1 option (a), with the optimism stated (already in splits_comment). A cross-study variant (option c) is what
  I would want for trust.

4. Would I use it?
- As decision support with calibrated probabilities and an abstain threshold, yes, alongside histology. I would trust
  it if: it is calibrated across sites, it abstains on low confidence, it is validated on samples from a sequencing
  centre outside the training set, and it handles rare/unseen diagnoses by abstaining rather than forcing one of 27.
  I would distrust a model that exploits study batch (median within-diagnosis study AUC 0.97) or missing age.

5. Metric (MET-1, MET-6, MET-8, MET-9, MET-11)
- Declared: log_loss, fallback (source has no single metric; Comitani reports several, a habit, MET-5). Verdict:
  PARTLY scores my decision. The decision is a confirm/revise call taken on the top class at a confidence threshold;
  log loss is a strictly proper rule on the probabilities I would threshold (MET-8), so it ranks models by the right
  thing (calibration matters for my abstain cut-off). Weakness: one confidently wrong sample dominates, and the NOS
  class takes 10x its row share; no threshold or cost is fixed by the source, so MET-6/MET-7 do not call for a
  threshold metric. What I would pick if free: still log loss (multiclass, proper) as primary; I would report top-1
  accuracy and accuracy at a calibrated confidence >= 0.9 with coverage (the methylation-classifier practice) as
  secondary. Not a reason to change the declared metric. AUPRC is not warranted (MET-9).

Gaps, ranked by how much they change the task
 1. Easy, settled-diagnosis cases vs the unclear cases a board consults on; no provisional diagnosis input (fit).
 2. Same-study test data (optimism 0.984 -> 0.85 cross-study), stated; cross-study variant would mirror a new hospital.
 3. Closed set of 27 classes; rare diagnoses (where the tool matters most) dropped.
 4. Flat labels where the clinic uses a hierarchy (AMKL in AML; glioma grades merged).
 5. Age/sex missing by study (unrealistic but small effect).

What an expert would change
- Keep the donor split (issue 1a) and the SAME_TUMOUR join (issue 2a: matching sex, age and r > 0.9958 for NCI's
  double deposits is convincing for a same-tumour call). Keep the 10-donor floor (issue 4). Keep the TCGA AYA rows
  (issue 5): young-adult carcinomas are a real differential in an AYA clinic.
- Note in the use case that it is diagnosis from scratch, not confirm-given-provisional; note hierarchy (AMKL < AML).
- Optional later: a cross-study variant over multi-study classes.

Sources: dataset.py and README.md of this folder; the record; the builder's report; Beale et al. 2025 Sci Data
12:1134; Comitani et al. 2023 Nat Med 29:656 (as cited in the definition); domain practice of the DKFZ methylation
classifier (Capper et al. 2018, Nature 555:469, calibrated score >= 0.9 cut-off) from my knowledge; no new web lookups.
Rules: USE-1, USE-3, USE-5, USE-6, USE-8, USE-10; MET-1, MET-5, MET-6, MET-7, MET-8, MET-9, MET-11; TP-7.
```

</details>

<details><summary>Blind review: treehouse_pediatric_tumor_type</summary>

```text
Verdict: include with changes. Real pediatric/AYA tumour-type classification from RNA-seq (Treehouse, Sci Data 2025, GSE294351); the grouped split is honest, but the task is close to trivial and far too wide as prepared.

Task: predict tumour diagnosis (27 classes) from bulk RNA-seq gene expression (54,571 genes, log2(TPM+1)-like values 0..18.9) plus age and sex. Real use: molecular confirmation of diagnosis or flagging likely misdiagnoses in precision-oncology review (Treehouse's own use). 3,261 samples, 3,010 donors, each donor has one diagnosis.

Concerns, most serious first:
1. Near-trivial. A single linear logistic regression on the top 2,000 variance genes, GroupKFold fold 1: accuracy 0.965, balanced accuracy 0.891. Tumour type is strongly encoded by tissue-of-origin expression, so the benchmark would separate methods mostly on the rare classes. Fix: keep it, but report balanced accuracy or log-loss, or merge or drop classes with fewer than about 20 samples.
2. Width. 54,571 float features against 3,261 rows. Most tabular learners (and in-context models) can't use this many features without preselection, so the benchmark tests feature handling more than learning. Fix: ship a filtered version (for example protein-coding genes, or the top 5-10k by variance chosen inside each training fold), or state that width is the point of the task.
3. Tiny classes. breast 10, DNET 12, synovial 13, hepatoblastoma/HCC 17, STE NOS 19. With 3 group folds, some test folds hold about 3 of these, so per-class scores are noisy. "supratentorial embryonal tumor NOS" is a vague label. Fix: set a minimum class size.
4. Age and sex are shortcuts for some classes (breast 10/10, cervical 21/22, testicular 51/62, pheo 18/24 are age >20; testicular and gynaecological classes also mark sex). These are legitimately known at prediction time, so this is a mild issue only. Missing values: age 407, sex 311, left as NaN, which is fine.
5. Cohort and batch. The samples mix several source cohorts (e.g. TARGET, TCGA AYA, and others), and the diagnosis is partly confounded with source cohort and processing batch. I did not have cohort or batch IDs to check this.

Leakage and copies: there are no duplicate expression rows, the donor groups hold out repeated samples (up to 8 per donor), and I found no post-diagnosis columns. The donor column must be excluded from the features (it's a hash).
Not checked: the source papers in detail; the gene quantification pipeline; whether the label harmonisation matches the source; the full 30-split CV; tree models (skipped because of the width).
```

</details>

<details><summary>Task gamer: treehouse_pediatric_tumor_type</summary>

```text
treehouse_pediatric_tumor_type: task gamer report

VERDICT: The task can barely be gamed. Formats left by the source cohorts predict the label on their own,
but on top of gene expression they lower log loss by only about 0.002, at or just above noise. No copies
across donors, no column from after the prediction point.

SETUP
- Features: the 500 most variable genes (log2 TPM), plus age, sex and a missingness flag for each.
  Subsampled for speed: genes were cut from 54,572 to the 3,000 most variable, and the models used the first 500 of those.
- Honest baselines:
  - Logistic regression (C=0.05), all 30 splits: log loss 0.1531 (range 0.1171-0.1759). This is the better honest model.
  - LightGBM (200 trees), first 6 splits only: log loss 0.2290 (range 0.182-0.259).
- Noise check, a random column added:
  - LR: 0.1530, per-split change -0.0011 to +0.0009.
  - LGB: 0.2253, per-split change -0.0051 to +0.0107.
- Scripts in the run folder.

EXPLOITS, RANKED BY GAIN
1. Format of the expression values and missing age/sex (work/fmt.py, work/run.py)
   - Features: number of decimal digits in the values, whether age is missing, count of nonzero genes, log of total TPM.
   - Exploited score: LR 0.1512 (gain +0.0019; per split +0.0008 to +0.0034, every split positive, above the noise band).
     LGB 0.2216 (gain +0.0074, per split -0.0055 to +0.0129, inside the noise band).
   - Formats alone, with age and sex but no expression values: LR 1.8006, LGB 1.9142.
     Expression gives 0.15, so formats alone are far from it, but they carry label information.
   - Precision as I measured it: median repr() digits of nonzero values per row is 12-13 for 2,180 rows and 17 for
     1,009 rows (about 70 rows at 14 or 18).
     - Coordinator's note: the column auditor found TCGA/TARGET rows at 15 decimals against 12 for the rest.
       My count uses Python repr digits, so its levels differ, but it shows the same two groups.
     - 17 digits: all breast, cervical and melanoma samples; 61/62 testicular; 67/71 thyroid; 126/143 Wilms; 162/217 neuroblastoma.
     - 12-13 digits: all Ewing, osteosarcoma, rhabdomyosarcoma, AMKL, choroid plexus, lymphoma and rhabdoid samples.
   - Missing age and sex:
     - Age missing for 82/93 AMKL, 23/26 choroid plexus carcinoma, 43/347 glioma.
     - Sex missing for 18/101 ependymoma, 53/880 acute lymphoblastic leukemia (ALL).
   - Would a deployed model have it?
     - Decimal digits: no. They record which file a sample was exported from, not biology.
     - Missing age: partly. It is a property of the source study; keeping it is defensible.
   - Fix: round every expression value to one fixed precision (e.g. 4 decimals) for all rows.

FLAWS THAT HURT AN HONEST MODEL: none found. Dropping training rows was not tested.

ATTACKS THAT FOUND NOTHING
- Near-copies across donors (work/nn.py): each sample's most correlated sample from another donor
  (Pearson, 3,000 genes) never reached r = 0.98. That nearest sample shares the label 95.2% of the time,
  which is biology, not a leak.
- Age format: all whole years (0-32), so no precision signal.
- Sentinel values: none. No missing expression values. Per-sample TPM totals are close to 1e6.
- No time column, so the temporal attacks do not apply. Age, sex and genes are all known when the tumour is
  sequenced, so no column from after the prediction point.

NOT CHECKED
- Row order against the label.
- A classifier of training rows against test rows.
- LightGBM on all 30 splits; models on all 54,572 genes.
- Forum searches; looking the rows up in the GEO file.
```

</details>

<details><summary>Precedent check: treehouse_pediatric_tumor_type</summary>

```text
Precedent check: treehouse_pediatric_tumor_type (2026-11-09)
Verdict: four of the five calls follow precedent. One departs from a Must without a reason written down: issue 2, the SAME_TUMOUR links under SPLIT-24. The register's only flag (LEAK-38 opposite outcomes) has nothing to do with this dataset.

Issue 1, split by donor rather than by study (SPLIT-29/31): CONSISTENT.
  Precedent: sarcoma (Lennart, 2026-10-22, splits.md Cases SPLIT-29/31): IID by patient kept over a split by tissue
  source site. The site was visible (AUC 0.70-0.75) and cost log loss when held out, but a lab types the tumours of new
  patients. The case here is the same in kind and stronger: study within diagnosis has AUC 0.97, and a study split
  cannot score 11 of 27 classes. Siblings in the same batch, not decided yet: tcga_pancancer_tumor_type issue 2 (IID
  kept against the site batch "as sarcoma") and cns_tumor_methylation issue 2 (IID kept against the chip batch). All
  three should be decided together. The optimism has to be stated in splits_comment, as for sarcoma.
  Option (c), a cross-study variant, follows SPLIT-31 ("a candidate for a variant, not a fix").

Issue 2, the six SAME_TUMOUR links: DEPARTS, with no reason written down.
  SPLIT-24 (Must) says never group on a similarity-threshold cluster. The links rest on Pearson >= 0.9958, backed by
  sex and age. No id in the source links them. The evidence.md rows for exact and near copies send copies of one
  entity to LEAK-17 (group) or LEAK-19/LEAK-21 (drop). Precedents for near copies all drop: emscad reposts (LEAK-21),
  qsar_tid_11 salt forms and audiology's 27 copies (LEAK-19). None groups on similarity. Possible distinguishing fact:
  these are six named pairs, not a cluster. The gap is 0.9958 against 0.9913 for any other pair. Both deposits are
  NCI's Ewing cohort (THR30/THR49), so the link has a provenance reason as well as the similarity.
  Reflection prompt:
    Join the six THR49/THR30 pairs into one donor, or drop the THR49 copies?
    **Problem:**
    - SPLIT-24 (Must) bars groups built from a similarity threshold, and these links are not in the source's ids.
    - Precedent for copies of one entity is to drop them (LEAK-19, LEAK-21: emscad, audiology_diagnosis, qsar_tid_11).
    | Option | Pro | Con |
    | (a) join, as shipped: an exception, because these are six named pairs from two deposits of one cohort, set apart
          by a gap and matching sex and age, not a cluster | keeps 5 datasets | first group key in the working copy
          taken from similarity; needs an exception note under SPLIT-24 |
    | (b) drop the THR49 copies (LEAK-19) | follows the rule and the precedents; no exception needed | loses 5 datasets of 3,261 |
    | (c) leave them apart | none | a test tumour can have its twin in training (LEAK-17, Must) |
    Recommendation: (b). It costs 0.15% of the rows and needs no exception. If (a), write the distinguishing fact into
    the definition and the record.
    [^1]: SPLIT-24, LEAK-17, LEAK-19, LEAK-21
  The builder recommends (a). Under the ranking that is a Must yielding to a Should (keeping rows), so it is not
  reasonable unless the curator reads the pairs as an exact key (cohort deposit plus demographics). Dropping the two
  donors with two diagnoses (5 datasets) is consistent with LEAK-20 (jm1).

Issue 3, labels and side inputs: CONSISTENT in keeping them.
  - AMKL kept apart from AML: cns_tumor_methylation keeps the WHO subclasses (draft, same batch). sarcoma merged MFS
    and UPS (2026-10-22) because the study treats them as one spectrum. tcga_pancancer issue 3 weighs merging
    COAD/READ, which is mostly site. AMKL is the same pattern: a subtype that follows one study (99% St. Jude). Merging
    it into AML would follow the sarcoma merge (TP-7), so this pair should be decided alike with tcga issue 3.
  - Age and sex missing by study: no direct precedent. LEAK-13 and LEAK-39 support keeping them with a note.
    Not flagged.

Issue 4, class floor at 10 donors: CONSISTENT. sarcoma dropped MPNST (5 patients) and kept SS at 10. TP-8 Cases
  (forensic_glass, ljubljana_primary_tumor, mic, sarcoma: 3-5 per test fold, kept 2026-10-12). Here 3 donors per
  fold matches.

Issue 5, overlap with tcga_pancancer (336 rows): CONSISTENT with PROV-6/7. Another target and population, unlike the
  heart_disease files, which were the same study and label and were merged. No precedent forces a drop.

Other definition calls:
  - Metric fallback (log loss): CONSISTENT with the MET fallback practice.
  - Age floored and TPM put on one grid (LEAK-13): CONSISTENT. Precision fixes like the earlier recording cases.
  - icd_disease and study_id dropped: CONSISTENT.
No drift found. No third exception of one kind.
```

</details>

<details><summary>Advocate: treehouse_pediatric_tumor_type</summary>

```text
Advocate opening brief: treehouse_pediatric_tumor_type (2026-11-09)
Position: ship, with two changes that need no new rule decision (point 2 and point 3). Strongest first.

1. The task is valid and clean on every check the panel ran. Evidence: claim auditor refuted no claim (0 shared donors on 30 splits, >=3 donors of every class in every test fold, metric computable on all folds); column auditor found no post-diagnosis column; the gamer's best exploit gains 0.0019 log loss over an honest LR (0.1531 -> 0.1512); 0.0% exact copies across the split; split auditor: "RIGHT WITH NOTES". Rules: SEL-1, USE-3/LEAK-1, LEAK-17, LEAK-27-31 (P4, Must) all hold. Outranks "too easy / too wide" objections because those are P6 value questions, below P4 validity, and validity is established.

2. The precision fingerprint left by on_tpm_grid is real; fix it, do not drop the dataset. Evidence: column auditor 15 vs 12 decimals (TCGA/TARGET vs rest), gamer 17 vs 12-13 repr digits, format_alone 0.978. Rule LEAK-13 (Must). Mildest remedy on the ladder: return the rounded value for every entry in on_tpm_grid (on-grid values move <1e-9; auditor checked both groups then read 15 decimals), re-run the format probe. A cleaning fix, no curator choice needed. I concede the curation comment "decimals only say zero or not" is wrong and must be rewritten.

3. SAME_TUMOUR join: concede to option (b), drop the 5 THR49 copies. Evidence: precedent checker shows SPLIT-24 (Must) bars similarity-built groups and every near-copy precedent drops (emscad, audiology, qsar_tid_11; LEAK-19). Cost 5 of 3,261 rows (0.15%). A Must outranks keeping rows (Should); dropping removes the twin-in-training risk (LEAK-17) without an exception. The 4 unjoined pairs >0.99 differ by id (claim auditor); add a one-line note (LEAK-19).

4. Not trivial on the declared metric. Blind reviewer's 0.965 accuracy is not the metric. On log loss the families spread 0.140 (linear) to 0.385 (RF), paired SE 0.004; best single gene skill 0.105; leak-probe shallow trees 0.72/0.79 macro AUC. Rule TP-3/TP-4: `solved` read as natural core of the task (tissue lineage), not a lookup; macro AUC saturating while log loss separates is the TP-3 keep case. Answers "near-trivial".

5. Donor split over study split. Evidence: study split would leave 11 of 27 classes untestable; optimism (0.984 -> 0.85 cross-study) already stated in splits_comment. Rules SPLIT-1/SPLIT-23, precedent sarcoma 2026-10-22 (SPLIT-29/31 Cases) in the same kind with a stronger reason; domain practitioner and split auditor agree. A cross-study variant is SPLIT-31's "variant, not a fix". Decide jointly with tcga_pancancer issue 2 and cns_tumor_methylation issue 2 for consistency.

6. Width (54,571 genes) is the shape gap the batch was accepted for, not a defect. A filtered gene set would be our own feature selection on the table (CLEAN-22: no filter beyond all-zero and exact copies, which are label-free); fold-internal selection belongs to the method, not the dataset. The curator accepted this record as a large-features candidate (2026-11-08 CC). Independent failure: models that cannot take the width fail independently of dataset validity.

7. Labels, floor, missing age/sex, TCGA overlap: keep with notes. Floor 10 donors = sarcoma precedent (TP-8 Cases, 3 per test fold); source's harmonised labels kept (TP-7, USE-5), AMKL/AML to be decided alike with tcga COAD/READ and sarcoma MFS/UPS; age/sex missingness gains only 0.189 -> 0.183 and is a source property kept under LEAK-13/LEAK-39 with a note (gamer: "keeping it is defensible"); 336-row TCGA overlap is a distinct target and population (PROV-6/7, precedent checker consistent). Add the domain note "diagnosis from scratch, no provisional diagnosis input" to fit_reason (USE-8).
```

</details>

<details><summary>Critic: treehouse_pediatric_tumor_type</summary>

```text
Critic opening brief: treehouse_pediatric_tumor_type (2026-11-09)
Position: ship only after changes 1 and 2; points 3-5 are notes or curator calls. No point argues exclusion.

1. Precision fingerprint left by our own fix (P4, LEAK-13 Must; repair).
   Problem: on_tpm_grid recomputes only the off-grid TCGA/TARGET values, so those rows now carry 15 written decimals
   against 12 for every other study (column auditor). The task gamer sees the same two groups (17 vs 12-13 repr
   digits: all breast/cervical/melanoma, 126/143 Wilms on one side; all Ewing/osteo/RMS/AMKL on the other). Format
   alone scores macro AUC 0.978 (leak probe); the gamer's format features lower LR log loss 0.1531 -> 0.1512, every
   one of 30 splits positive, above the noise band. The curation comment says the decimals "only say zero or not",
   which the evidence contradicts.
   Effect: a model can read the source study from a recording artifact a deployed model would never see.
   Remedy: return the rounded value for every entry (or round all output to 12 decimals), re-run the format probe,
   fix the comment.

2. SAME_TUMOUR join groups on a similarity threshold (P4, SPLIT-24 Must; fix the definition).
   Problem: six donor links rest on Pearson >= 0.9958 plus sex/age, not on a source id. SPLIT-24 bars such groups;
   every near-copy precedent drops (emscad LEAK-21, audiology and qsar_tid_11 LEAK-19) (precedent checker).
   The gap is thin: other-donor pairs reach 0.9914 with matching age and sex (claim auditor).
   Remedy: drop the THR49 copies (LEAK-19; 5 of 3,261 rows), no exception needed. Optional: note that the 4
   other-donor pairs > 0.99 were checked by id only.

3. Study confounding makes scores optimistic for a new site (P4, SPLIT-29/31, LEAK-15/39; note, curator call).
   Within-diagnosis study AUC median 0.97; leave-study-out accuracy 0.984 -> 0.85 (TARGET AML 0.98 -> 0.35);
   11 of 27 classes from one study. I accept the donor split (sarcoma precedent), but it must be decided together
   with tcga_pancancer issue 2 and cns_tumor_methylation issue 2, and splits_comment must keep the numbers.

4. Age/sex missing by study (P4, LEAK-15, USE-6 Should; curator call).
   Missing age marks AMKL (82/93) and choroid plexus (23/26), AUC 0.90/0.92; log loss 0.189 -> 0.183. The
   practitioner would always have age and sex. Small gain; keep with the note, but put it to the curator as an
   explicit question rather than settle it in the builder's favour.

5. Flat labels that follow a study (P3, USE-5, TP-7 Should; note or merge).
   AMKL is a WHO subtype of AML and 99% St. Jude; log loss charges an AMKL -> AML call fully. Decide alike with
   tcga COAD/READ and sarcoma MFS/UPS (merged). Remedy: at least a note on the hierarchy; merging is the curator's.

6. Use-case fit stated too favourably (P3, USE-1/USE-8 Should; note).
   No provisional diagnosis input, settled textbook cases, closed set of 27 of 111 diagnoses: this is diagnosis
   from scratch, not confirm/revise (practitioner). Remedy: say so in fit_reason.

7. Width and near-saturation (P6, TP-3/TP-4; quality, not a reason to exclude).
   54,571 genes over 3,261 rows; logreg reaches 0.965 accuracy, macro AUC 0.999 (blind reviewer, builder). Log loss
   still spreads families 0.140-0.385 (paired SE 0.004), so it stays a task. Remedy: none required; at most a note
   that width is part of the task. Metric source (Comitani) read from a snippet only: re-check once (MET-1).
```

</details>
