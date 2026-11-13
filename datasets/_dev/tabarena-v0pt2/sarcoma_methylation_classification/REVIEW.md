# sarcoma_methylation_classification

**Outcome:** added. The DKFZ reference set of the sarcoma methylation classifier (Koelsche et al. 2021, GEO GSE140686): 1,077 tumours, one per patient, 405,842 CpG beta values plus the site, its tissue and the manifestation, 63 methylation classes (the four clustering-only chondrosarcoma subgroups shipped as their two families), random 3 x 10 folds stratified by class, log loss as the fallback metric. The panel recommends shipping after changes; the changes are made (`site` cleaned and `site_tissue` added, the Ewing's apostrophe, the `Class-dependent Recording` marker, the referring centre named in the task summary and the split notes, the notes on controls, dates, abstention, small classes and shared arrays). No container is built yet: very wide frames hit pyarrow's read limit, a build blocker, fixed in the package before the build. Kept as in the CNS sibling, with no issue: the 40 arrays shared with `cns_tumor_methylation_classification`, the three control classes, and `site` and `manifestation` as inputs. `dataset check`: 0 errors and one warning, `task_stratify_high_cardinality` (63 classes, ten of 7 cases). The panel proposes accepting it with the builder's sentence, "63 classes of 7 to 59 tumours; stratifying on the target keeps every class in every training side". That sentence is not yet in `accepted_check_warnings`; issue 5 asks whether to accept it. Two more checks, duplicates and pure feature values, were skipped for width (`dataset_duplicates_skipped`, `dataset_pure_feature_value_skipped`) and run by hand with nothing found. `Bone, limbs, upper limbs, femur` (4 rows) is kept as in the source and noted.

**Main points:** One test for clustering-drawn classes in both methylation datasets (issue 1); keep the random split with the referring centre stated (issue 2); keep the array type's small shortcut, decided with `tcga_pancancer_tumor_type` (issue 3); judge the value after the build, as the score is near the ceiling (issue 4).

**Record judgment:** valid. A diagnostic classifier in routine use, from a Nature Communications paper and its GEO deposit; one tumour per patient, no leak in the shipped columns. The record now carries `Class-dependent Recording` for the array type, which follows the class (31 of 63 classes on one array) but gives a small measured shortcut.

**Value and quality:** log loss spreads across model families (linear 0.046, LightGBM 0.47, random forest 0.98, dummy 3.93), but the score is near the ceiling (issue 4); `site` is cleaned to the expert state. Weighed: source +, gap + (very wide multiclass omics), risk − (clustering-drawn classes, centre and array tied to the class, near the ceiling).

**Issues for the curator:**

1. **Apply one test for clustering-drawn classes to both methylation datasets: merge only the classes with no outside definition?**

   * **Problem:**
     - This dataset merges its four chondrosarcoma subgroups, which only the clustering separates, into the source's two class families.
     - `cns_tumor_methylation_classification` keeps its 27 subdividing classes for the same stated reason, the classifier's clinical use, and nothing written separates the two.
   * **Effect on the task:** small here; keeping the 65 source classes gives a log loss of 0.185 against 0.181 for the shipped 63, the four subgroups separate at 98.9% by construction and carry 9.3% of the loss.
   * **Background:** the classes come from "Unsupervised clustering, respecting the minimal number of seven cases per group" ([Koelsche et al. 2021](https://doi.org/10.1038/s41467-020-20603-4)); the other subgroup and non-WHO classes here each have an outside definition (a BCOR or CIC fusion, a MYOD1 or DICER1 mutation, retained H3K27 trimethylation, a histological subtype).
   * **Consistency:** the merge follows the retirements of `brca`, `glioblastoma` and `ov` for clustering-only subtypes[^sel4] and the TCGA `sarcoma` merge; the CNS sibling's issue 1 asks the same question from the other side.
   * **Panel:** the advocate holds the merge consistent and option a leaves this definition unchanged; the critic wants both datasets decided on one test before this one ships; the mediator finds no failure here, only the cross-dataset consistency call.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | a | Merge only classes with no outside definition, in both (implemented) | this definition stays as it is; the CNS sibling checks its subclasses against WHO 2021 and merges the undefined ones | one written test for both; consistent with the 2026-10-12 retirements | a class-by-class reading of WHO 2021 in the sibling |
     | b | Keep the source classes in both | 65 classes here, 91 in the sibling | the classifier's own output | labels drawn from the same profiles; departs from the retirements |
     | c | Merge all subclasses in both | fewer classes, none below a WHO entity | no class rests on clustering | loses subtypes defined by a fusion or mutation |

   * **Recommendation:** a, with the test written into both curation notes. **Decision:** a, b or c? Decide alike with `cns_tumor_methylation_classification` issue 1; the shared test is the across-datasets item **Clustering-defined classes**[^sel4].

   **Notes for the AI:** the across-datasets item's full title is "Clustering-defined classes (SEL-4)". On a, nothing changes here beyond a sentence naming the test in the target note; on b, empty `CLASS_FAMILIES` and recount the classes in `task_summary` and the notes; on c, map every category-2 class of Supplementary Data 2 to its entity. Decide together with `cns_tumor_methylation_classification` issue 1; re-run `dataset check` after any change.

   [^sel4]: **SEL-4** (Must): a label from unsupervised learning (a molecular subtype defined by clustering) is no real
     predictive task. Cases: brca_breast_cancer, glioblastoma, ov_ovarian_cancer (Lennart, 2026-10-12).

2. **Keep the random patient split, with the referring centre named as the larger hidden group?**

   * **Problem:**
     - The 31 referring centres and studies are a hidden group: without its centre in training a tumour scores 0.80 log loss against 0.235 for removing as many random tumours.
     - A split by centre leaves about 74 test tumours per fold whose class has no training tumour, as 18 classes take 90% or more of their cases from one centre.
   * **Effect on the task:** the scores hold for a new patient from a known centre more than for a new lab; the chip effect (+0.019) sits inside the centre effect (about +0.57, from +0.09 to +1.5 by centre).
   * **Experiments:** split auditor: centre removed against matched random removal, +0.57 (approximate, as it scores only tumours whose class keeps a training tumour); centre GroupKFold 0.86 against 0.18 under IID; chip GroupKFold 0.41 with about 6 unseen-class rows per fold.
   * **Consistency:** follows the IID-with-stated-optimism calls for `sarcoma` (2026-10-26), `cns_tumor_methylation_classification`, `tcga_pancancer_tumor_type` and `treehouse_pediatric_tumor_type`[^split].
   * **Panel:** the advocate and the critic agree on keeping IID with the note; the domain practitioner notes that new labs increasingly send cases, which is the use option b would test.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | a | IID with the centre named (implemented) | random patients stratified by class; `task_summary` and `splits_comment` give the centre numbers | every class in every fold; the optimism is stated with its size | scores hold for known centres |
     | b | Grouped by centre, on classes with two or more centres | `Supplier` as the group, single-centre classes dropped | tests a new lab | loses about a quarter of the classes (18 come 90% or more from one centre); folds uneven |
     | c | IID with the earlier note | the chip-only note | none found | understates the optimism |

   * **Recommendation:** a; the use case is a new patient, and a centre split would test classes it cannot train. **Decision:** a, b or c?

   **Notes for the AI:** on b, read `Supplier` from Supplementary Data 1 as the group column (not a feature), keep classes with two or more suppliers, rewrite the class counts, and re-run `dataset check` and the group probe.

   [^split]: **SPLIT-29** (Must), **SPLIT-30** and **SPLIT-31**: rows of one hidden group inform each other; a
     hidden-group hit is decided by the context and the use case, never by the gap alone, and a kept IID split states
     its optimism.

3. **Keep the array type's small shortcut, and is this the line for such keeps?**

   * **Problem:**
     - 31 of the 63 classes were profiled on one array type only (313 cases), and the betas give the array away (ROC AUC 1.00).
     - A model can route a tumour to the classes of its array type; measured, EPIC tumours of the two-array classes put 0.044 of their probability on EPIC-only classes, 450k tumours 0.024.
   * **Effect on the task:** small; `gallstone_disease`'s recording shortcut was 0.77 against 0.22, the task gamer's NaN-count feature gained nothing (0.1119 to 0.1119), but it does not separate the two arrays, so it is no test of the route.
   * **Consistency:** the second keep of a class-tied recording (after `tcga_pancancer_tumor_type`'s BCGSC classes, issue 1 there), set apart by a measured route test BCGSC lacks; a third keep calls for a written amendment[^leak].
   * **Panel:** the mediator grades the shortcut weak by measurement, so keeping it with a note is the mildest fix that fits; the critic asks for the marker (now set) and a joint decision with tcga.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | a | Keep with the note and the marker (implemented) | both arrays, the route test in the notes, `Class-dependent Recording` on the record | all 1,077 cases and 63 classes | a small shortcut stays |
     | b | EPIC only | 592 cases | no array route | loses the 450k-only classes and half the cases |
     | c | Ship the array type as a feature | a column `array` | the shortcut is explicit; the pathologist knows the array | does not remove the shortcut |

   * **Recommendation:** a, and state the line: a class-tied recording is kept when a route test on the mixed classes measures a small shortcut. **Decision:** a, b or c (decide alike with `tcga_pancancer_tumor_type` issue 1)? Whether this is the line for such keeps is the across-datasets item **Route/array classes kept**.

   **Notes for the AI:** decide together with `tcga_pancancer_tumor_type` issue 1; on b, filter to `platform == "EPIC"` in `_clean` and recount the classes; on c, add `raw["platform"]` as a categorical column. Re-run `dataset check` and the leak probes on the reduced view.

   [^leak]: **LEAK-39** and **LEAK-15** (Must when strong; amended 2026-10-27, Andrej, on gallstone_disease): a
     recording artefact tied to the class is fixed or kept by its measured size; a kept one carries the marker.

4. **Judge the value after the build, as the score is near the ceiling?**

   * **Problem:**
     - A linear model reaches about 0.99 accuracy and a log loss of 0.046 to 0.11, and the reference set holds no "no match" cases, the hard part of the clinic's use.
   * **Effect on the task:** methods may tie on accuracy; log loss still spreads (linear 0.046, LightGBM 0.47, random forest 0.98, dummy 3.93).
   * **Panel:** the blind reviewer would exclude it or cut the width; the advocate answers that log loss spreads by 10 to 20 times across model families and that width alone is no reason; the critic keeps it with the abstention note (now in `fit_reason`) and a re-check after the build[^tp].
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | a | Ship and re-check the spread with tuned methods (implemented) | the tuned-method spread on log loss decides after the build | judged on the benchmark's own evidence | a decision deferred |
     | b | Ship as is | no re-check | no extra run | a tie among strong methods would go unseen |
     | c | Leave out | the dataset leaves | none found | the spread already found argues against it |

   * **Recommendation:** a. **Decision:** a, b or c?

   **Notes for the AI:** after the build, compare the tuned methods' log loss with their standard errors; if they tie, raise it again.

   [^tp]: **TP-1** and **TP-3**: a task-probe flag is checked against the benchmark's tuned methods before anyone acts
     on it; a task is kept when the model families spread on its metric.

5. **Accept the stratify warning with this text?**

   * **Problem:**
     - `dataset check` warns that the stratification column, the target, has 63 distinct values, ten of them with 7 cases.
   * **Effect on the task:** none on the data; stratifying on the class keeps every class, also the smallest, in every training side (2 or 3 cases of each smallest class per test fold).
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Accept with the builder's text | written into `dataset.py` on yes | the check reads clean and states why | none found |
     | B | Leave it unaccepted (implemented) | the warning stays in every check | none found | a known, explained warning keeps showing |

   * **Recommendation:** A. **Decision:** accept the warning with this text, yes or no?

   **Notes for the AI:** on yes, add to `accepted_check_warnings` in `dataset.py`: `task_stratify_high_cardinality`: "63 classes of 7 to 59 tumours; stratifying on the target keeps every class in every training side". Re-run `dataset check`.

**Review panel:** ship after changes (mediator). The rebuttal round was skipped, as the advocate's and the critic's briefs converged. Claims: all hold but one recording claim on the controls (refuted in scope, note reworded). Columns: no leak; `site` cleaning fixed. Split: IID right, optimism understated (referring centre; fixed in the notes). Blind review: would exclude for width and the ceiling (answered, issue 4). Task gamer: no exploit beat the noise. Agreed: the drops, the split regime, the controls. Agreed, left to the curator: the referring centre (issue 2), the array route (issue 3). Disputed: clustering-drawn classes (issue 1, the critic wants it decided with cns first), the value near the ceiling (issue 4, the blind reviewer would exclude).

<details><summary>Mediator: sarcoma_methylation_classification</summary>

```text
Mediator report: sarcoma_methylation_classification (2026-11-09). The rebuttal round was skipped, so this report rests on the opening briefs and the phase-A reports. I ran no new experiment: no disputed fact needed one.

SUMMARY (15 lines)
1. Verdict: ship after changes. No validity Must is broken and none needs fixing.
2. The advocate and the critic agree on nearly everything. The critic's two "Must" points (SEL-4 sibling, array marker) are a consistency question and a marker fix, not failures of this dataset.
3. Changes to make now: clean `site` and add `site_tissue`; fix the apostrophe in "Ewing´s"; add the `Class-dependent Recording` marker; rewrite the optimism note to name the referring centre; reword the Controls note; four small note fixes.
4. Curator issue 1 (SEL-4, Must): one test for both methylation datasets, decided together with cns issue 1. The recommendation is (a): merge only classes with no outside definition. That leaves this definition unchanged.
5. Curator issue 2 (SPLIT-29/30/31, Should): referring centre +0.57 log loss against chip +0.019. Recommendation: (a) keep IID with the rewritten note.
6. Curator issue 3 (LEAK-39/LEAK-15): array route shortcut 0.044 against 0.024. Keep with a note; decide together with tcga issue 1 (BCGSC) and say whether this test is the line.
7. Curator issue 4 (value, weighing): no "no match" cases, and the score is near the ceiling. Settled by tuned-method spread after the build (TP-1/TP-3).
8. Task gamer: no exploit beat noise. Every exploit maps to a known note or is new with zero gain, so none is an issue.
9. The blind reviewer's "exclude" rests on width (not an argument: CLEAN-22, EV-4, coad) and on accuracy at the ceiling (log loss still spreads by 10-20x across model families, TP-3). Both are answered.

JUDGMENT RECORD
Verdict: ship after changes.
Validity: SEL-1 holds. SEL-2 holds. SEL-4 triggered, fixed in part (4 chondrosarcoma subgroups merged into the source's 2 families; the cross-dataset test is curator issue 1). USE-1 holds (fit approximate: prototypical in-class cases, no "no match" cases). LEAK-1/LEAK-10 hold (Diagnosis, Supplier, Batch, DNA, purity, IDAT dropped correctly). LEAK-39/LEAK-15 triggered by the array type, kept with a note (measured shortcut small, 0.044 vs 0.024), and the `Class-dependent Recording` marker must be added. LEAK-13: controls are recognisable from the clinical columns, no gain measured, note reworded. LEAK-30 does not apply (betas are per sample). SPLIT-29/30/31: IID kept; the optimism note is understated (referring centre) and gets rewritten. PROV-7: distinct from cns, shared arrays named.
Value: TP-3 met (log loss linear 0.046 / LightGBM 0.467 / random forest 0.979 / dummy 3.934). TP-8 met (2-3 per class per test fold), with a note (classes of 9 or fewer carry 27-40% of the loss). MET-5 fallback log loss holds (Brier is the practitioner's tie-break preference, not strong enough to overrule).
Quality: CLEAN-1/CLEAN-11 `site` not cleaned, fix now. CLEAN-19 add `site_tissue`. CLEAN-25 "Ewing´s". CLEAN-22 width kept.
Weighed: size 0, source +, gap + (very wide multiclass omics), risk - (clustering labels, centre/array confound, near the ceiling).
For the curator: issue 1 (SEL-4 test across both datasets), issue 2 (IID vs supplier-grouped), issue 3 (route-test line with tcga), issue 4 (value weighing after tuned runs).

CHANGES TO MAKE NOW (no decision needed)
1. `site` (CLEAN-1, CLEAN-11; Should, cheap and safe): lossless map in `_clean`:
   - strip trailing spaces (6 values split one site into two levels);
   - normalise the ", " separator ("Soft tissue,trunk,  pelvis, bladder wall");
   - fix the typos "Soft tisse", "abomen" (3), "thracic wall" (2), "pevic girdle" (1).
   "Bone, limbs, upper limbs, femur" (4 rows) stays as it is unless the source shows lower limbs; note it.
2. Add `site_tissue`, the first level of `site` (CLEAN-19); keep the full `site` too.
3. Target label "Ewing´s sarcoma" (U+00B4) becomes "Ewing's sarcoma" (CLEAN-25).
4. Add the `Class-dependent Recording` marker to decision_markers. The leak_checks.md marker rule requires it wherever LEAK-13 to LEAK-15 or LEAK-39 applied, kept or retired. It covers the array route and the exact-0/1 format finding (probe 17, 0.745).
5. Rewrite task_summary (line 82) and splits_comment (line 155) (SPLIT-29/30/31). Name the referring centre as the larger hidden group: without its centre a group's tumours score 0.80 against 0.235 for matched random removal (+0.57, range +0.09 to +1.5), against +0.019 for chip mates. Supplier GroupKFold gives 0.86 against 0.18 under IID, with 74 test rows per fold of unseen classes. The chip effect sits inside the centre effect.
6. Reword the Controls and Clinical columns notes (LEAK-13; claim refuted in scope). All 28 controls lack manifestation. Missing manifestation plus 3 sites flags all controls with 4 false positives (28/32). Reactive tissue is exactly missing + "Soft tissue, trunk, paraspinal" (10/10). The gamer measured no gain (format variant 0.1116 vs 0.1119). Replace "the recording adds nothing" with this measured null.
7. Note fixes (writing.md):
   - "profiled from 2013 to 2019" (line 69) applies only to the dated cases; 64 have no Batch date;
   - fit_reason: no "no match" cases, so abstention cannot be scored;
   - classes of 9 or fewer: 15.8% of rows, 27-40% of the loss, above the 22% precedent band (TP-8);
   - shared arrays: 40 here = 35 in GSE90496 + 5 in GSE109379, against 35 in the cns notes; reconcile both notes.
8. Accept the `task_stratify_high_cardinality` warning with the builder's sentence.

ISSUES FOR THE CURATOR (ranked)
1. Clustering-designated classes, one test for both methylation datasets (P2, SEL-4, Must; consistency).
   - Problem: this dataset merges its 4 chondrosarcoma subgroups, which have no outside definition. cns_tumor_methylation_classification keeps 27 subclasses for the same stated reason (clinical use). Nothing written separates the two.
   - Effect here: small. 65 classes give log loss 0.185 against 0.181 shipped. The subgroups separate at 98.9% by construction and carry 9.3% of the loss.
   - Advocate: the merge is consistent with brca/glioblastoma/ov (SEL-4 applied class by class), and option (a) leaves this definition as it is.
   - Critic: the Must stays unsettled until the CNS call is made; decide both on one test.
   - Mediator: not a conflict and not a failure here; this definition already meets SEL-4. The precedent and consistency question goes to the curator.
   - Decision: (a) merge only classes with no outside definition, in both datasets; a WHO 2021 methylation-defined subtype counts as defined (recommended). (b) keep the source classes in both. (c) merge all subclasses in both. Write the chosen test into both notes.
2. Referring centre as a hidden group (P4, SPLIT-29/30/31, Should; a weighing of the split against usable folds).
   - Advocate and critic agree: keep IID. A supplier split leaves 74 test rows per fold of unseen classes; 18 classes take 90% or more of their rows from one centre.
   - Split auditor's caveat: the B arm scores a subset, so the +0.57 is approximate.
   - Options: (a) IID with the rewritten note (recommended; the forest_fires and sarcoma precedents); (b) grouped by supplier, restricted to classes with 2 or more suppliers; (c) leave as is.
   - What would settle it: whether the use case is "a new patient" or "a new lab". The practitioner says new labs increasingly send cases.
3. Array type follows the class (P4, LEAK-39/LEAK-15, Must when strong). Builder issue 2.
   - Facts: 31 of 63 classes are on one array only; the betas give the array away (ROC AUC 1.00).
   - Measured shortcut: 0.044 vs 0.024 of the probability, against gallstone_disease's 0.77 vs 0.22.
   - Mediator: weak by measurement, so the rule grades it Should, and keep-with-note is the right rung of the ladder.
   - Decision: confirm (a) keep, together with tcga issue 1 (BCGSC, kept with no test possible), and say whether "kept when the route test on mixed classes measures a small shortcut" is the line. A third keep of this kind triggers an amendment.
   - Optional (c): ship the array type as a feature (the practitioner always knows it). It makes the shortcut explicit but does not remove it.
4. Near ceiling, and the hard part of the use case absent (P6, TP-1/TP-3; USE-8; weighing).
   - Blind reviewer: accuracy 0.990, exclude or cut the width.
   - Advocate: log loss spreads by 10-20x across model families (TP-3), and width is no argument (coad).
   - Critic: keep, add the abstention note (change 7), and re-check the spread with tuned methods after the build.
   - What would settle it: the tuned-method spread on log loss after the build.
5. Cross-dataset items, decided jointly with cns (consistent with precedent, low stakes):
   - builder issue 5 (shared arrays, PROV-7; (a) keep both);
   - builder issue 4 (controls; (a) keep, note reworded);
   - builder issue 6 (site and manifestation; keep, USE-3/USE-6).
   Cross-dataset calls the curator kept for the review page (protected grounds, codes vs words, scoring within groups, late-filled values) stay open as issues like on every other dataset.

TASK GAMER'S EXPLOITS mapped (none beat the noise band of about ±0.0005; base 0.1119)
- Format features (exact 0/1 counts, NaN counts, clinical missingness): 0.1116. LEAK-13. Known: builder probe 17 kept as value and material, and the Controls note. Gain nil, consistent with the notes. No issue.
- Row position: 0.1120. CLEAN-23 (row shuffle). New, nil. No issue.
- NaN count per row: 0.1119. LEAK-39 array route. Known: the "Potential leak, kept on purpose" note (0.044/0.024). No measured gain, consistent with a small shortcut. No issue.
- Scaler fit on train and test rows together: 0.1155, worse. LEAK-30. Known not to apply. No issue.
- Blend with the nearest training row's label: 0.1580, worse. LEAK-16 to LEAK-21 (copies). Known: no copies. No issue.
- Looking samples up in GEO by profile: not ranked. Applies to any public dataset.

AGREED FACTS
- 1,077 rows, one per patient; 63 classes (62 tumour classes + controls); 28 controls (blood 10, muscle 8, reactive 10); ten classes of 7 cases.
- 405,842 probes plus `site` (197 values, 88 missing) and `manifestation` (56 missing, including all 28 controls).
- No shipped column leaks; the drops are correct; claim 29/59 revised holds; no exact or near copies.
- Log loss: dummy 3.934; logistic regression 0.046-0.11; LightGBM 0.47; random forest 0.98. Accuracy about 0.99.
- Chip mates +0.019 (LR) / +0.057 (5-NN). Supplier +0.57 (approximate). Supplier grouping leaves 74 unseen-class test rows per fold.
- Array route 0.044 vs 0.024; array type from the betas ROC AUC 1.00.
- Families of 9 or fewer carry 27-40% of the loss. 64 cases have no Batch date. Shared arrays: 40 here vs 35 in the cns notes.
- No "no match" cases in the data.
- `site` has the cleaning defects listed under change 1; "Ewing´s" uses U+00B4.
- Log loss is the fallback; the source reports error rate, AUC and Brier side by side and names no criterion.

CONSISTENCY WITH PRECEDENT
- Follows: SEL-4 retire precedents (brca/glioblastoma/ov) and the TCGA sarcoma merge; IID over a batch-like group with the optimism stated (sarcoma 2026-10-26; cns/tcga/treehouse); controls; PROV-7; site and manifestation; the TP-8 few-minority keeps; MET-5 fallback.
- Departs from the batch sibling cns issue 1 with no stated separating fact. That becomes curator issue 1; no change here.
- Array route: the second keep of this kind (with tcga BCGSC). This case is set apart by the measured route test, which BCGSC lacks; decide both together, and a third keep calls for an amendment.
- Marker gap: `Class-dependent Recording` is missing, a fix with no decision (the same applies to tcga if BCGSC is kept).
- No drift and no third exception yet.

```

</details>

<details><summary>Claim audit: sarcoma_methylation_classification</summary>

```text
Claim auditor: sarcoma_methylation_classification (2026-11-09). Tests on SD1 (MOESM4) and the paper text in source/; no container built.
Verdict: claims hold except one recording claim (controls); no Must-level refutation.

claim | source | test | result | evidence | rule
2 1,077 rows, one per patient | task_summary.row | SD1 rows, ID unique | holds | 1,077 | -
3 profiled 2013-2019 | row | SD1 Batch min/max | holds (weak) | 2013-07-04..2019-01-10, but 64 of 1,077 Batch missing | -
5 31 centres | row | Supplier nunique | holds | 31 | -
6 controls 10/8/10 | row | class counts | holds | blood 10, muscle 8, reactive 10 | -
7 63 classes, chordoma 59, ten of 7 | predicted | counts after family merge | holds | 63; 59; ten classes of 7 | -
9 / 43 740 tumours share a slide with a same-class tumour | split, splits_comment | Sentrix ID from IDAT, group by chip+class | holds | 740 | SPLIT-29
1 29/59 revised | use_case | paper text | holds | "revised in favour of the predicted methylation class in 29/59 cases" | -
10 a quarter reached no class | fit_reason | paper text | holds | "not reached for 106 of 428 cases (25%)" | -
33 site 197 values, 88 missing; manifestation 876/78/67, 56 missing | notes | value counts | holds | exact | -
34/50 Blood = blood controls only; stomach = 30 GISTs only | notes | crosstab | holds | 10/10; 30/30 | -
36 DNA: EDTA blood = blood controls | notes | value counts | holds | 10 | -
42 metric fallback log loss; paper reports error rate, AUC 0.99, Brier 0.05 side by side | metric.reason | paper Methods text | holds | "estimated error rate of 1.95% ... 0.65% ... AUC of 0.99 and a Brier score of 0.05"; no criterion named; Brier is the nearest proper score, log loss acceptable fallback | MET-1, MET-5
Issue 4 / note "blood controls recorded unlike any tumour; recording adds nothing" (implied: only blood is recognisable from the clinical columns) | issues_draft #4, curation notes Controls | crosstab of manifestation-missing x site | REFUTED (scope) | manifestation missing AND site in {Blood, 'Soft tissue, trunk, paraspinal', 'Soft tissue, limbs...'} flags all 28 controls with 4 false positives (28/32); reactive-tissue control = manifestation missing + site paraspinal exactly (10/10, no tumour); all 28 controls have manifestation missing | LEAK-13
Implied: site known at diagnosis, not a label proxy | known | in-sample majority class per site | holds with caution | site alone 58% in-sample accuracy; 122 sites are single-class (226 rows, mostly singletons) | USE-1
15,26-31,38-41,46,48,49 | notes | not re-run (probe outputs read; would need the 3.5 GB matrix) | untested here, builder-measured | probes/*.json | -
Implied: target = real-world target | | covered by builder issue 1 (clustering classes); agree with recommendation (a) | - | SEL-4

Ranked refuted/untested
1. Controls are identifiable from the clinical recording (missing manifestation + site), not only the blood class (LEAK-13, Should). Changes: issue 4's statement "the recording adds nothing measurable" rests only on blood; the same holds for reactive tissue (paraspinal) and muscle (limb soft tissue). Effect is likely nil because the betas recognise controls too, but it is untested. Mildest remedy: reword the Controls note to say all 28 controls carry no manifestation and a fixed site (reactive tissue all 'Soft tissue, trunk, paraspinal'), and add a test (betas-only vs betas+clinical log loss on control rows) or option (c)/(b) of issue 4 / ship profile only (issue 6).
2. "Profiled from 2013 to 2019": 64 cases have no Batch date; minor wording ("dated cases").
3. Untested here: probe/filter counts and leak probe numbers (measured by builder; not re-run to avoid the 3.5 GB load).
```

</details>

<details><summary>Column audit: sarcoma_methylation_classification</summary>

```text
Column auditor: sarcoma_methylation_classification (2026-11-09)
Verdict: ship after two small cleaning fixes to `site` and one curator question on `manifestation`. No leak found
among the shipped columns. Evidence from sd1_geo.csv (Supplementary Data 1 joined to GEO), scratch_detp_fail_share.csv,
and the builder's probes. I did not rebuild the frame (the full width costs about 12 GB and 25 min); the shipped columns
are exactly the ones `_clean` keeps.

COLUMN TABLE
column | meaning | known at prediction? | dtype and cleaning | verdict | rule
methylation_class (target) | class from SD1 with the "methylation class " prefix removed; 4 chondrosarcoma subgroups merged into 2 families | it is the label | category, source names (CLEAN-25); "Ewing´s sarcoma" uses an acute accent (U+00B4) where an apostrophe belongs (cosmetic) | fine (SEL-4 merge is builder issue 1) | CLEAN-17, SEL-4
site | anatomical site as a comma-separated hierarchy (tissue, region, subregion...), 197 values, 88 missing | yes, the submitter records it at diagnosis | category; NOT cleaned to the expert state, see P1 | cleaning problem | CLEAN-1, CLEAN-11
manifestation | primary / recurrence / metastasis; 56 missing | yes | category, 3 levels, not ordinal (correct). All 28 controls are missing (100% of the 3 control classes) plus 28 tumours (neurofibroma 4 of 9, MPNST 9 of 26) | question (P2) | LEAK-13 reading
cg* x 405,842 | per-sample minfi preprocessIllumina beta (methylated/(meth+unmeth+100)), 0..1 | yes, the array is run at diagnosis | float32, numeric (correct). Detection p-values: 0 failing calls in any sample (scratch_detp_fail_share.csv: max 0.0), so nothing needs masking. 18,544 missing kept missing. Exact 0/1 = background clamp, real values, not proxies (CLEAN-10 does not apply). SNP/cross-reactive probes dropped by fixed published lists (not data-chosen, CLEAN-8 fine). No per-row id survives | fine | CLEAN-7/8/10/22
Dropped, checked: Diagnosis (helps define the label, LEAK-1), Supplier (site of origin, 18 classes >=90% from one), Batch (array date), DNA (EDTA blood = blood control class), Tumour cell content (a model output from the profile), IDAT/Colour (ids; IDAT encodes the chip). All drops correct. Array type not shipped (builder issue 2).

PROBLEMS, RANKED (principles.md: Must before Should; then size of effect)

P1. `site` is not cleaned (CLEAN-1 / CLEAN-11, Should). Evidence:
  - 6 values end in a trailing space and so split one site into two levels ("Soft tissue, limbs, upper limbs,
    shoulder girdle " 2 rows vs the clean spelling 8 rows; also cubital fossa, peroneal nerve, sciatic nerve,
    abdomen..abdominal wall..subcutis, head and neck occipital).
  - Typos: "Soft tisse, trunk" (top level wrong), "abomen" (3 rows), "thracic wall" (2), "pevic girdle" (1),
    "Soft tissue,trunk,  pelvis, bladder wall" (spacing; duplicate of "Soft tissue, trunk, pelvis, bladder wall", 2 rows).
  - Impossible combination: "Bone, limbs, upper limbs, femur" (4 rows); the femur is a lower-limb bone. Fix to lower limbs
    if the source agrees, otherwise keep (one row-level source error, curator call).
  - 197 levels at about 5.5 rows each, many singletons, with a clear hierarchy whose top level (Soft tissue 504, Bone 220,
    Visceral 134, Intracranial 63, Skin 54, Blood 10, Lymph node 2) the pipeline cannot read from an opaque category.
  Mildest remedy: strip whitespace, normalise ", " separators, fix the 4 spelling errors (a lossless map in `_clean`),
  and add one derived column `site_tissue` (the first level) per CLEAN-19 (a property an expert reads first; ranking
  skull base for chordoma, stomach for GIST). Optionally `site_region` (second level). Keep the full `site` too. Effect
  on scores is small; the fix is about the shipped state.

P2. `manifestation` missing for every control (curator question, LEAK-13 reading, Must if read as a class convention).
  The 28 controls (blood, muscle, reactive) have no manifestation because a control is no tumour: "not applicable"
  filled for one class family only. Missingness alone separates controls from all but 28 tumours (probe: missing
  indicator alone macro ROC AUC 0.546, small since it covers 3 of 63 classes). At deployment a submitter does not know
  a sample is non-tumour, so a reactive-tissue sample would arrive with a manifestation entered (usually "Primary").
  Options: (a) keep (implemented; effect small, betas recognise controls anyway); (b) set the controls' manifestation
  to missing for no one, i.e. leave as is but state it in the notes as a class-specific recording; (c) drop the
  column. Recommendation (a) with one sentence in the Clinical columns bullet saying missing = control or not recorded.
  Same for `site == Blood` (exactly the 10 blood controls): known at submission (the lab knows it sent blood), keep.

P3. Target label text "Ewing´s sarcoma" (U+00B4). Cosmetic; normalise to "Ewing sarcoma" or "Ewing's sarcoma"
  (CLEAN-25 readable names). Should, trivial.

Not problems (checked):
  - Builder issues 1-6 weighed: none changes a column verdict. Issue 2 (array type) is a route leak of known small size
    (0.044 vs 0.024 mass); shipping the array as a column (option c) would make it explicit but not remove it; I agree
    with (a). Issue 6 (site/manifestation as inputs): both known at diagnosis (USE-6); keep.
  - Dtype probe (builder's, reduced view): 0 flags; I see no count or code typed wrongly at the full width either
    (all probes float in [0,1]; the two clinical columns are nominal).
  - No column encodes the label: IDs (REFERENCE_SAMPLE n, ordered by class in SD1 — sample 1-2 are muscle controls) are
    dropped; the row shuffle (CLEAN-23) must still hold since SD1 is sorted by class; the IID splits are random.
```

</details>

<details><summary>Split audit: sarcoma_methylation_classification</summary>

```text
Split auditor: sarcoma_methylation_classification
Verdict: right with notes (IID over patients is the right regime; the stated optimism is understated: the referring centre, not the chip, is the larger hidden group).

Regime. One tumour per patient (Methods), no time column used for prediction (Batch = array date, dropped), the classifier types a new patient's tumour, increasingly sent by labs outside the 31 reference suppliers. Use case implies new patient; partly new centre. Declared: IID stratified on class, 10 x 3. No temporal stream (reference set is a curated collection 2013-2019, the deployed tool is retrained rarely), so no temporal split needed. Copies: 0 duplicate rows, closest pairs blood controls; the builder's checks hold.

Finding 1 (P4, SPLIT-29/30/31, Should: note; mild). Supplier (referring centre/study, 31 values, dropped as a column) is a hidden group stronger than the chip. Check (work_split_auditor/c.py; LR C=0.05 on 3,000 random standardised probes; shipped repeat 0, folds 0-2; per test supplier with >=15 test rows, 15 cases): test rows of supplier g scored by (A) the shipped train, (B) train without supplier g, (C) train without as many random same-class tumours from other suppliers.
  mean log loss: A ~0.20, B 0.80 (on rows whose class survives), C 0.235. Excess of B over C ~ +0.57 (range +0.09 INFORM to +1.5 Kiel), against the builder's chip excess of +0.019.
  Caveat: B scores a subset (rows of classes left with no training tumour dropped, 0-13 per group), so the gap is approximate, but it is 30x the chip effect.
  Fully grouped by supplier (GroupKFold 3): log loss 0.86 on seen classes vs 0.18 shipped IID, with 74 test rows per fold whose class has no training tumour (18 classes take >=90% from one supplier); chip-grouped: 0.41, 5.7 unseen rows/fold.
  Reading: class and supplier are confounded (consultation cases of a rare entity come from its specialist centre), so part of the IID score is centre/lab signature. A grouped-by-supplier split is unusable (a quarter of the classes vanish from training), so keep IID.
  Mildest remedy: no re-split; rewrite the splits_comment and task_summary optimism note to name the referring centre (and the chip inside it), with these numbers, and add a draft issue for the curator (options: (a) IID with the note, recommended; (b) grouped by supplier restricted to classes with >=2 suppliers; (c) leave as is).
Finding 2 (builder issue 3, chip mates): agree with (a); the chip effect is small and nested in supplier.
Finding 3 (none): no temporal leakage or late labels; label is the reference-set class fixed at publication.
Alignment note: participant_kit rows matched to GEO sample IDs by exact betas of 4 probes (1,077/1,077 unique, row_ids.csv).
```

</details>

<details><summary>Domain practitioner: sarcoma_methylation_classification</summary>

```text
Domain practitioner report: sarcoma_methylation_classification
Actor: a molecular / bone and soft-tissue pathologist who uploads a sarcoma's methylation array (IDATs) to the
Heidelberg sarcoma classifier (Koelsche et al. 2021, Nat Commun; v12 on molecularneuropathology.org) at diagnosis.

FIT: approximate. The inputs and the target are what I get from the classifier at diagnosis, but the rows are the
classifier's own prototypical reference cases, not the unselected, often ambiguous cases I upload, and in practice I
act on "class if calibrated score >= 0.9, else no match" (USE-1, USE-8 reading in use_case.md "How closely the data
mirrors the use case"). Agrees with the definition's declared fit.

1. Inputs at the prediction moment (USE-3, USE-6)
- Betas from my array: yes. In practice I have the IDATs and the service normalises them; GEO's per-sample
  preprocessIllumina betas are a fair stand-in (no all-row correction, LEAK-30 clean).
- Site and manifestation: yes, on the request form. The classifier itself does not use them, but I do when I read the
  result, so adding them is fair (issue 6: keep).
- Not given and I would always have: the histological diagnosis / differential, the array type (I know which chip I ran,
  issue 2 option (c) is realistic), tumour purity (the service reports it from the same array, a model output, fine to
  leave out), and copy-number profile (derived from the same array; a model can get it from the betas only partly
  since intensities are not shipped). None of these is a leak; the histology is my prior, dropped correctly.

2. Target
- The methylation class is exactly what the service returns and what I act on (confirm, refine, revise). I want a
  calibrated probability per class, because I only accept a class above 0.9 and otherwise report "no match". A class
  label alone is useless to me; the probability is the decision input.
- Chondrosarcoma subgroup merge (issue 1): matches how I read the report (family score), agree with (a).
- Controls (issue 4): the classifier has them because low-purity samples land there; keeping them is realistic (a).

3. Rows and test data
- One row = one tumour = one upload decision: matches.
- Test data is not what I face. Gaps, ranked by how much they change the task:
  a. No "no match" / out-of-class cases. In the source's validation about a quarter of cases reached no class above
     0.9; here every test tumour belongs to one of the 63 classes, so the hard part of my job (knowing when not to
     trust the output) is absent. Largest gap; it is why the score is near-perfect (linear log loss 0.046).
  b. Prototypical reference cases, classes partly defined by clustering of these same profiles (SEL-4 reading; issue 1).
  c. Same-chip / same-batch mates in training (issue 3): a new tumour from my lab never shares a chip with the
     reference set. Measured cost small (+0.019 to +0.057 log loss); stated optimism is adequate.
  d. Array mix confounded with class (issue 2): real (my lab moves 450k -> EPIC -> EPICv2), measured shortcut small.
     EPICv2 is now what new cases arrive on and is absent; a known temporal gap, not fixable here.
  e. Shared arrays with the CNS series (issue 5): irrelevant to my decision; keep.

4. Would I use it?
- As a benchmark of how well a model types a sarcoma from its profile, yes. I would trust a model that is calibrated
  (scores >= 0.9 almost always right) and that flags out-of-distribution samples; I would distrust one tuned on this
  set alone, since every case here is in-class and prototypical. The benchmark cannot show the abstention behaviour.

5. Metric (MET-1, MET-5, MET-6 to MET-9)
- Declared: log loss, fallback (paper reports error rate, AUC and Brier side by side, MET-5 none deliberate).
- Scores my decision: partly-to-yes. A strictly proper rule on the class probabilities is what I need, since I act on
  a calibrated score with a 0.9 cut-off (MET-8). Log loss is the right family; it scores calibration across all classes.
- The 0.9 cut-off decides abstention, not the class (MET-7 correctly not invoked); and abstention cannot be scored
  without out-of-class cases, so a threshold/selective metric would score nothing real here (MET-6).
- Alternative I would consider: multiclass Brier score, which the paper reports (0.05) and which is bounded, so one
  confidently wrong rare-class tumour (ten classes of 7 cases carry 12-20% of the loss) does not dominate as under log
  loss. Not strong enough to overrule the fallback; log loss is acceptable. Verdict: metric scores the decision: yes
  (log loss acceptable; Brier would be my tie-breaking preference).

What an expert would change
- Add the array type as a feature (I always know it; makes the shortcut explicit rather than hidden) - optional.
- Note in the use case that the task has no "no match" cases and so cannot measure abstention.
- Keep issues 1 (a), 3 (a), 4 (a), 5 (a), 6 keep; issue 2 (a) or (c).

Sources: dataset.py and README.md of the folder; builder_report.md (probes, issues 1-6); Koelsche et al. 2021 Nat
Commun 12:498 "Sarcoma classification by DNA methylation profiling" (Methods: classifier development, 0.9 calibrated
cut-off, validation 29 of 59 discordant cases revised; per the definition's notes); use_case.md, metrics.md (df-large).
No web lookups beyond what the definition cites; domain practice (0.9 threshold, IDAT upload, EPICv2 transition) from
my own knowledge of the Heidelberg classifier service.
```

</details>

<details><summary>Blind review: sarcoma_methylation_classification</summary>

```text
Blind review: sarcoma_methylation_classification (Koelsche et al. 2021, Nat Commun 12:498; GEO GSE140686)

TASK: Predict one of 63 methylation classes (62 tumour classes + controls) of a sarcoma/control sample from its Illumina
450k/EPIC beta values (405,842 CpG columns, float in [0,1], 0.008% NaN) plus `site` (197 levels, 88 NaN) and
`manifestation` (Primary/Recurrence/Metastasis, 56 NaN). 1,077 rows = the paper's reference set ("1077 methylation
profiles ... comprising 62 tumour methylation classes"). Real use: pathologists use this classifier (molecularsarcomapathology.org)
to support diagnosis after biopsy. Data is real, target is right.

VERDICT: Exclude as prepared (at most include with heavy changes: a reduced CpG set, and only as an omics/high-dim stress test).

CONCERNS (most to least serious)
1. Near-trivial / saturated. Logistic regression (C=0.1) on the 2,000 most variable of a 1-in-40 CpG subsample (~0.5% of features)
   gives 3-fold accuracy 0.990. Methods will tie at the ceiling; little ranking information.
2. Width is impractical for a tabular benchmark: 405,845 columns x 1,077 rows; merely loading/describing the full frame in pandas
   took >10 min. Most tabular learners (GBDTs with default settings, TabPFN-type models) cannot run as is; the benchmark would
   measure feature-screening plumbing, not model quality. Change: ship a fixed, label-free reduction (e.g. top 10k-20k CpGs by
   variance, as the paper and the brain-tumour classifier do) or exclude.
3. Label circularity: methylation classes were in part defined/refined by unsupervised clustering of these same methylation
   profiles (the paper's reference cohort was curated for class consistency), so the target is partly a function of X; this
   inflates separability vs. real diagnostic use. Could not verify exact wording (Nature page behind login wall).
4. Split: IID 3-fold. Smallest classes have 7 samples (8 classes at n=7), so ~2 test samples per class per fold - noisy
   per-class metrics; stratification is required. The paper validated on a separate cohort of 428 tumours, which would be the
   honest test; it is not included. No patient IDs to check for multiple samples per patient (could not check).
5. Near-duplicates: 47 sample pairs with Pearson r>0.99 (subsampled CpGs), all within control (blood) / muscle / reactive tissue /
   plexiform neurofibroma - plausible biological homogeneity, not obvious copies; no exact duplicates spotted.
6. Metadata: `site` and `manifestation` are known at prediction time (fine); alone they give 0.40 accuracy (site is near-label
   for e.g. chordoma/skull base). `site` has 197 sparse levels - fine as categorical. Types: categorical dictionaries, floats OK.

NOT CHECKED: GEO page (bot wall) and full paper text; patient-level grouping; batch/array type (450k vs EPIC) per sample;
full-feature models (too wide to run in time).
```

</details>

<details><summary>Task gamer: sarcoma_methylation_classification</summary>

```text
Verdict: no exploit found; this task cannot be gamed in any way I could find. Every attack scored within the noise of the honest model, and the methylation profile alone gives log loss of about 0.10 to 0.11.

Honest baseline (work/run.py, variant "base"): multinomial logistic regression (C=0.05, standardised, fit on the training rows only) on the 3,000 top-variance probes, plus site and manifestation one-hot. Mean log loss over 30 splits is 0.1119 (prior 3.93).
- I picked the probes by variance over all 1,077 rows (label-free). That is a mild transductive choice and I did not test a train-only selection.
- Untuned LightGBM (top 500 probes plus site and manifestation, splits r0f0 to r0f2 only, 0.36 to 0.60) scores 0.4705 against 0.108 for logistic regression on the same three splits, so LightGBM is the weaker honest model.
- Noise check: adding a column of random numbers changes the score by between -0.0004 and +0.0005 per split, mean 0.0000.

Exploits ranked by gain: none beat the noise band.
| # | Exploit | Score (base 0.1119) | Gain per split, range | Verdict |
|---|---|---|---|---|
| 1 | Format features: per-row count of exact 0 and exact 1 betas and of NaN probes, plus site and manifestation missing (variant fmt) | 0.1116 | -0.0008 to +0.0007 | Noise. On their own they score 3.75, about the 3.93 prior. A deployed pipeline would compute them as well. |
| 2 | Row position as a feature (variant rowpos) | 0.1120 | -0.0002 to +0.0004 | Nothing. Next-row label agreement is 0.026, chance is 0.024. |
| 3 | NaN count per row (variant nanrow) | 0.1119 | -0.0003 to +0.0004 | Nothing. All rows have 0 to 232 NaNs, so there is no 450K/EPIC platform split. |
| 4 | Scaler fit on the train and test rows together (variant transductive_scaler) | 0.1155 | +0.0015 to +0.0060 worse | It hurts. |
| 5 | Blend with the label of the nearest training row (variant knnblend) | 0.1580 | +0.029 to +0.069 worse | It hurts. |

Copies across the split: there are no exact or near copies. The smallest Euclidean distance between two rows is 6.2, against a median nearest-neighbour distance of 19.5. No row's nearest neighbour is under 0.6 of the distance to its second-nearest. The 1-NN label agreement of 0.967 is the class signal itself (work/dups.py).

Identifiers: none. The only columns are the 405,842 cg probe columns, site and manifestation.

Training rows that tell the future: not applicable. The split is IID, with no time column.

Formats:
- Betas are float32 with no rounding pattern.
- Every row has exact 0 and exact 1 values (about 51 and 30 per 20k probes). This looks like clipping in the preprocessing, not a min-max scaling: only 17% of columns have a minimum of 0 and 14% a maximum of 1.
- Manifestation is missing for 56 rows, including all 28 controls; site is missing for 88. This is a recording artefact, but it gives no measurable gain on top of the probes (variant fmt).

Opposite flaw: none found. Dropping site and manifestation scores better (0.1046, gain -0.0073 over 30 splits). That is a weakness of my model in one-hot coding about 100 sparse sites, not a flaw of the task.

Web: GSE140686 is the DKFZ reference set (Koelsche et al. 2021, Nat Commun), 1,077 samples. I found no leak or magic-feature threads. Looking samples up in GEO by their beta profile would work, as for any public dataset; I did not try it and do not rank it.

What I could not check:
- the full 405k probes in one model (I used the top 3k by variance);
- the GEO sample IDs, batch or FFPE-versus-frozen labels, which are not in the kit;
- per-patient duplicates (a primary and its recurrence) that are not near copies.

Sources: https://pmc.ncbi.nlm.nih.gov/articles/PMC7819999 , https://www.omicsdi.org/dataset/geo/GSE140686
Scripts: work/prep.py, work/explore.py, work/run.py, work/dups.py. Results: work/res_*.csv
```

</details>

<details><summary>Precedent check: sarcoma_methylation_classification</summary>

```text
Precedent check: sarcoma_methylation_classification (2026-11-09)

Verdict: issues 3-6 and the other calls follow precedent. Issue 2 (array type) is kept with a stated, measured reason that
sets it apart from tcga's BCGSC classes, but it is still the second keep of the same kind and the
`Class-dependent Recording` marker is missing. Issue 1 is consistent with SEL-4's retire precedents, but it is decided
differently from its batch sibling cns_tumor_methylation_classification (issue 1), and neither side names the fact
that separates them. The register flags nothing for this dataset; the only register line is the size check
(2026-11-08, AI, SEL-4/PROV-7/LEAK-30).

Issue 1, clustering-designated classes (SEL-4, Must)
  Precedents: brca_breast_cancer, glioblastoma, ov_ovarian_cancer retired (Lennart, 2026-10-12, selection.md Cases):
  clustering-only subtypes with no outside definition. sarcoma (TCGA) MFS/UPS merged to the source's class (Lennart,
  2026-10-22). glioma_grading (2026-10-20) rejected the pathologist's prior call as the target (USE-1).
  This definition: CONSISTENT. The four chondrosarcoma subgroups have no definition outside the clustering, so they
  are merged to the source's two families (the brca/gbm reasoning applied per class). The other classes are kept, each
  with an outside definition. Option (c), histology, would depart from glioma_grading.
  BATCH PAIR, DEPARTS WITHOUT A REASON: cns_tumor_methylation_classification issue 1 recommends A, keeping all 91
  classes including 27 "WHO subclass" classes. Its reason is the classifier's clinical use, and that holds here too, so
  it does not separate the two. The builder report itself says the two "should be decided alike". If the CNS keeps
  clustering-only subclasses unmerged, this dataset's merge has no counterpart there, or the reverse. WHO 2021 defines
  some CNS subtypes by methylation profile. That could be the separating fact, but only for the subclasses WHO names.
  Reflection prompt:
    Merge clustering-only subclasses into their entity in both methylation datasets, or keep them in both?
    **Problem:**
    - sarcoma_methylation merges its 4 chondrosarcoma subgroups (no outside definition), but cns_tumor_methylation keeps
      27 WHO-subclass classes. Both cite the classifier's clinical use, so nothing written separates the two cases.
    - SEL-4 (Must) treats clustering-only labels as no real task (brca/glioblastoma/ov, 2026-10-12).
    | Option | Pro | Con |
    | (a) merge only classes with no definition outside the clustering, in both; a CNS subclass that WHO 2021 defines by methylation counts as defined | one test for both; follows SEL-4 class by class | CNS needs a per-class check against WHO 2021 |
    | (b) keep the source's classes in both (sarcoma ships 65) | the classifier's own output | sarcoma's subgroups are separated by construction (98.9%); weakens SEL-4 |
    | (c) merge all subclasses in both | strictest reading | CNS loses methylation-defined WHO types |
    Recommendation: (a).
    [^1]: SEL-4, USE-5, USE-1

Issue 2, array type follows the class (LEAK-13/15/39, Must): DEPARTS WITH A STATED REASON (reasonable), plus a marker gap.
  Precedents: gallstone_disease (Andrej, 2026-10-26, LEAK-39): the route's rows were dropped because models recognised
  the route and scored its other-class rows as the class (0.77 vs 0.22). prostate_cancer_detection (2026-10-27,
  LEAK-15) was retired. Batch: tcga_pancancer_tumor_type issue 1 (BCGSC, 4 whole classes, kept with no test possible).
  Does this case line up with tcga's? It is the same kind: a route that holds whole classes (here 31 of 63 classes,
  313 rows, on one array, and the betas give the array away at AUC 1.00). The fact that sets it apart: 32 classes are on
  both arrays, so the LEAK-39 test could run, and the shortcut measured small (0.044 vs 0.024 of the probability on
  EPIC-only classes). gallstone's was 0.77 vs 0.22. That is a reason tcga's BCGSC lacks.
  The paper also combines both arrays, and a lab's classifier sees both. So keeping with a note lines up with tcga's
  GBM call (kept after the test passed). It is a stronger case than tcga's BCGSC. If BCGSC is kept too, these are two
  exceptions of one kind: a route holding whole classes kept under LEAK-15 / LEAK-39. That is no amendment yet. A third
  (cns has a material tie, issue 3, but material is a feature there, not a route) should prompt one. Suggested
  wording: "kept when the route test on mixed classes measures a small shortcut".
  Marker gap: the leak_checks.md marker rule says `Class-dependent Recording` goes on every dataset where LEAK-13 to
  LEAK-15 or LEAK-39 applied, kept or retired. The record's decision_markers hold only "Needs extensive data
  wrangling". This is a fix, not a decision (the same holds for tcga if BCGSC is kept). The exact-0/1 number-format
  finding (probe 17, 0.745; LEAK-13 reading, kept as value and material) also falls under the marker.
  Within this dataset, the measured route effect is the reason, so no reflection prompt is needed. The curator should
  decide it together with tcga issue 1 and say whether the 0.044/0.024 test is the line between them.

Issue 3, chip mates under IID (SPLIT-29/30/31): CONSISTENT. Precedent: sarcoma (Lennart, 2026-10-26, IID by patient
  over the tissue site, optimism stated). Batch: cns issue 2 (chip, A), tcga issue 2, treehouse issue 1, all IID by
  patient against a batch-like group. The optimism is stated in splits_comment (line 82).
Issue 4, control classes (USE-8; LEAK-14 reading): CONSISTENT. LEAK-14 drops a class from a separate assay. Blood is the
  same array, a different material, and is also a class of the classifier itself; no measured shortcut beyond the
  betas. A blood-control class with its own row text should still be named in the notes.
Issue 5, 40 shared arrays (PROV-7): CONSISTENT. Mirrors cns issue 4 (A; it counts 35 arrays, the builder here counts 40 =
  35 GSE90496 + 5 GSE109379: same set plus the 5 from the second series, reconcile the count in the notes). Decide jointly.
Issue 6, site and manifestation: CONSISTENT with USE-3/USE-6 (known at diagnosis; no single-feature dominance).
TP-8 few_minority: CONSISTENT with forensic_glass_identification/ljubljana/mic/sarcoma (2026-10-12): 6.5% of rows, 12-20%
  of the loss; the 9-or-fewer band (27-40% of the loss) exceeds that precedent's 22%. Worth a line in the notes.
MET-5/MET-11 fallback log loss, LEAK-30 (per-sample betas), float32: CONSISTENT.
No drift found (no curator has decided these rules twice differently). No third exception of one kind yet.
```

</details>

<details><summary>Advocate: sarcoma_methylation_classification</summary>

```text
Advocate opening brief: sarcoma_methylation_classification (2026-11-09)
Position: ship as defined, with changes that need no decision (site cleaning, notes, marker), plus the curator's calls
on issues 1-3 as the builder recommends.

1. A real task, the right target, no leak (USE-1, SEL-1, LEAK rules; Must). The domain practitioner: the methylation
   class "is exactly what the service returns and what I act on"; source revised the diagnosis in 29/59 cases. Column
   auditor: "No leak found among the shipped columns"; Diagnosis, Supplier, Batch, DNA, purity, IDAT all dropped
   correctly. Task gamer: "no exploit found"; format, row position, NaN count, transductive scaler, kNN blend all
   within noise (0.1116-0.1580 vs base 0.1119). Claim auditor: no Must claim refuted. Every validity Must holds.

2. Not saturated: methods spread (TP-3, Must: "if tuned methods spread, keep, no further discussion"). Answers the
   blind reviewer's "near-trivial" (accuracy 0.990). On log loss, the metric, the builder's probes give linear 0.046,
   LightGBM 0.467, random forest 0.979 against dummy 3.934; the gamer confirms LightGBM 0.47 vs LR 0.108 on the same
   splits. Families differ by a factor of 10-20 in loss. Accuracy at the ceiling is not the metric; log loss ranks
   calibration, which the practitioner says is the decision input (MET-8). TP-3 outranks an accuracy impression.

3. Width is no reason to cut or exclude (CLEAN-22, EV-4; the conflict table: "a model's input cap is never an
   argument", coad, Lennart 2026-10-15). Answers blind concern 2 (405k columns, LightGBM >54 GB). The definition keeps
   all probes but the source's own SNP/cross-reactive filters (fixed published lists, CLEAN-8 fine). A wide-omics task
   is the gap this dataset fills (Weighed: gap +). Load cost is real and stated in the builder report; it is a harness
   note, not a curation defect.

4. Clustering-defined labels are handled class by class (SEL-4, Must), consistent with precedent. Precedent checker:
   "CONSISTENT" with brca/glioblastoma/ov retirements: the four chondrosarcoma subgroups with no outside definition are
   merged; every other class has a definition outside the clustering. The cns sibling departs, but that is a
   consistency question for cns or for both (precedent option (a): same test in both), and option (a) leaves this
   definition unchanged. Not a reason to hold sarcoma.

5. The split is right; the optimism is a note, not a re-split (SPLIT-29/30/31 Should; P4 over P6; remedy ladder).
   Split auditor: IID over patients is right; supplier grouping costs +0.57 log loss but leaves 74 test rows/fold with
   an unseen class and a quarter of classes vanish, so "keep IID". Mildest remedy: rewrite splits_comment and
   task_summary to name the referring centre (with the numbers) and add the curator issue (a) IID with note. Chip
   mates: +0.019, already stated (issue 3 a).

6. Array-type route: kept on a measured test, plus a marker fix (LEAK-39/LEAK-15, Must when strong). 32 classes on
   both arrays let the route test run: shortcut 0.044 vs 0.024, against gallstone's 0.77 vs 0.22 (precedent checker:
   "a stronger case than tcga's BCGSC"). Remedy: keep with a note (rung 3), and add the `Class-dependent Recording`
   marker that leak_checks.md requires; a fix, no decision. Optional: ship array type as a feature (practitioner,
   "I always know it").

7. Real but small cleaning and recording issues get the cheap fix (P3 over P7; CLEAN-1/11/19/25 Should, LEAK-13 Should).
   - site: strip trailing spaces, normalise ", ", fix 4 typos (lossless map), add `site_tissue`; femur row to the
     curator only if the source disagrees.
   - "Ewing´s sarcoma" -> "Ewing's sarcoma".
   - Controls: reword the note: all 28 controls lack manifestation and have a fixed site (reactive tissue all
     paraspinal), not only blood. Effect measured nil by the gamer (fmt variant -0.0003 overall) and the missing
     indicator gives macro AUC 0.546; keep (a), per column auditor and practitioner.
   - "2013-2019" -> "dated cases" (64 without Batch). Small classes (ten of 7) carry 12-40% of the loss: note (TP-8 is
     met: 2-3 per test fold per class, 3 folds x 10 repeats; not "a handful of units" for 63-class whole).
   - Use case note: no "no match" cases, abstention not measured (practitioner gap a).
   Independent failures are not conflicts: none of these is a Must left unmet, so none blocks shipping.
```

</details>

<details><summary>Critic: sarcoma_methylation_classification</summary>

```text
Critic, opening brief: sarcoma_methylation_classification (2026-11-09)
Position: ship only after changes 1-5; 6-7 are cheap quality fixes. No point here argues for exclusion: the task is real
(USE-1 holds per domain practitioner) and no Must is unfixable. Blind reviewer's "exclude" rests on width and the
ceiling; width is no argument (principles "Width against model limits", coad 2026-10-15), so I drop it.

1. Clustering-designated classes decided unlike the batch sibling (SEL-4, Must; validity).
   Problem: the 4 chondrosarcoma subgroups are merged here for having no outside definition, while
   cns_tumor_methylation_classification keeps 27 clustering subclasses with the same "clinical use" reason (precedent
   checker). One of the two applies SEL-4 wrongly. Effect: subgroups separate by construction (98.9%), so kept
   clustering classes reward re-finding the clustering, not diagnosis. Remedy: no change here; make the curator decide
   both together on one test (precedent option (a): merge only classes with no outside definition; a WHO-defined
   methylation type counts as defined), and write that test into both notes. Shipping this one before the CNS call
   leaves the Must unsettled.

2. Optimism note names the wrong hidden group (SPLIT-29/30/31, Should; validity).
   Problem: the note blames chip mates (+0.019 log loss). Split auditor: referring centre (Supplier, 31 values) costs
   ~+0.57 over matched random removal (B 0.80 vs C 0.235; range +0.09 to +1.5), 30x the chip; supplier GroupKFold 0.86
   vs 0.18 IID; 18 classes take >=90% of rows from one centre. Effect: a large part of the score is centre/lab
   signature that a new lab's tumour will not carry. Remedy: keep IID (supplier split loses ~74 rows/fold to unseen
   classes), rewrite task_summary/splits_comment with the centre numbers, add a curator issue ((a) IID+note,
   (b) supplier-grouped on classes with >=2 suppliers).

3. Array route kept without the marker (LEAK-15/LEAK-39 reading, Must if strong; marker rule in leak_checks.md).
   Problem: 31 of 63 classes on one array, betas give the array at AUC 1.00; measured shortcut small (0.044 vs 0.024),
   so keep is defensible, but decision_markers lack `Class-dependent Recording`, which the rule requires kept or
   retired (also covers the exact-0/1 format finding, 0.745). It is the second keep of this kind with tcga BCGSC.
   Remedy: add the marker; curator states the route test as the line, decided with tcga issue 1.

4. Controls note is false in scope (LEAK-13, Should; validity of a stated claim).
   Claim auditor: missing manifestation + three sites flag all 28 controls (28/32); reactive tissue = missing +
   paraspinal 10/10. The note says only blood is recorded apart and "the recording adds nothing". Gamer measured no
   gain (fmt 0.1116 vs 0.1119), so no leak in effect. Remedy: reword the Controls bullet to all three control classes
   with these counts and cite the gamer's null result.

5. The use case's hard part is absent and the score near ceiling (USE-8 reading, TP-1/TP-3; value).
   No "no match" cases (25% of validation cases in the source); linear log loss 0.046 (skill 0.988), gamer 0.11.
   Effect: methods may tie; abstention is unmeasured. Not a reason to drop (TP-6 precedent applies to leaks, none
   here). Remedy: a note in fit_reason that abstention cannot be scored; re-check spread with tuned methods (TP-1/TP-3)
   after the build, as for electric_motor (kept with tuned spread).

6. `site` not in the expert state (CLEAN-1, CLEAN-11, CLEAN-19, Should; quality).
   Trailing spaces split 6 sites; typos "tisse", "abomen"(3), "thracic"(2), "pevic"; separator variant; "upper limbs,
   femur" (4). Remedy: lossless map in _clean; add `site_tissue` (first level); "Ewing´s" U+00B4 to an apostrophe
   (CLEAN-25).

7. Small factual notes (writing.md; quality). "Profiled 2013-2019": 64 cases lack a date. Shared arrays 40 here vs 35
   in the CNS notes: reconcile. Classes of 9 or fewer carry 27-40% of the loss, above the 22% precedent band (TP-8):
   one line. Remedy: notes only.
```

</details>
