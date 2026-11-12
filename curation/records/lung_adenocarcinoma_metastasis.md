---
unique_name: lung_adenocarcinoma_metastasis
name: Lung adenocarcinoma, metastasis from another organ or primary (Bhattacharjee 2001, GEO arrays)
checked_by:
- Andrej
data_foundry_status:
- 'DF: Yes'
suggestion: 'Yes'
priority: 1
decision_markers:
- Class-dependent Recording
- Selection Bias
tags:
- New IID
- Many features
- Tiny Data
original_source: Other
year: '2001'
domain: medical & healthcare
required_split:
- Random (IID)
problem_type: Binary Classification
original_data_state: Database (or multiple to-be-joined tables)
source_links:
- https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE83227 (the study's deposit of all 254 arrays, per-array MAS5 files)
- 'https://ftp.ncbi.nlm.nih.gov/geo/series/GSE83nnn/GSE83227/suppl/GSE83227_caArray_meyer-00191.tar.gz (the study''s annotation sheet SampleData.xls, sheet DATASET B: the metastasis flags; also the paper, 13790.pdf)'
- https://www.pnas.org/doi/10.1073/pnas.191502998
v2_path: datasets/_dev/tabarena-v0pt2/lung_adenocarcinoma_metastasis/dataset.py
type_adapter_id: curation-record-v1
---

## Comments

CC (2026-11-11, Andrej): new record for the metastasis task on the arrays of `lung_cancer`, whose histology target was retired on 2026-11-10 (BeyondArena v0.2 review page, lung_cancer issues 7, B, and 4, B: a new record, since rows, target and values all changed). Ship.
- **The source's own task:** "A key issue in lung tumor diagnosis is the discrimination of a primary lung adenocarcinoma from a distant metastasis to the lung" (Bhattacharjee et al. 2001, Results); "metastases of nonlung origin can be difficult to distinguish from lung adenocarcinomas" (Introduction). The paper finds them by clustering and scores no classifier.
- **Where the label comes from:** the study's annotation sheet (`SampleData.xls`, sheet DATASET B, in GEO's caArray archive) flags 16 of its 139 adenocarcinomas as "possible mets" (8 colon, 4 breast, 4 other). 15 are written in the resected tumour's own pathology note, AD218's only in the study's second reading. The call is read from the specimen's pathology but not settled there: it rests on the earlier cancer outside the specimen, and the source calls the two "difficult to distinguish". The 8 colon flags are the firmest and the easiest part. All count but AD218's (below), leaving 15.
- **Rows:** 123 adenocarcinomas: the paper's 125 with clinical data, less AD218 and AD224; the 12 `A` patients and AD355, AD360 have no clinical data, so "no flag" is no finding for them. One MAS5 array per tumour, scaled on that array alone (the GEO rebuild of lung_cancer's issue 1); the 67 control probes are dropped.
- **Size:** 5 metastases per test fold. The task probe raises no flag (shipped splits; random forest ROC AUC 0.876, ahead of the class shares on every split; logistic regression 0.836, LightGBM 0.811); ten unfitted pathology marker genes reach 0.819. Out of fold, colon metastases separate at 0.984, breast at 0.76, other at 0.83. Metric: ROC AUC, the binary fallback.
- **Recording:** corrected on 2026-11-11 by the review panel: an earlier run paired labels with the wrong arrays. The metastasis arrays call fewer probe sets present (ROC AUC 0.722) and show more 18S rRNA (0.784); the 67 control probes (0.695 together) are dropped, at no cost; the share present runs through every gene and stays, with the `Class-dependent Recording` marker (noise floor subtracted: logistic regression 0.855 to 0.857).
- **AD218 and AD224 dropped as undetermined (review issue 2, B):** AD218's only metastasis note is the study's second pathology review ("ad w met?") and it lies in the paper's colon expression cluster, so its flag may follow the clustering; AD224 has the same kind of note ("ad m met?") and is coded primary. Dropping both removes the contradiction without taking a side; on the same folds no score moves.
- **Known gaps:** the label is "possible", not a confirmed origin; the rows are all resected adenocarcinomas while the question arises only after an earlier cancer elsewhere, which is not recorded (`Selection Bias`, fit approximate). AD320 and AD368 are primaries the source suspects. No colon flag follows the clustering: the 7 inside it are the paper's "previously diagnosed".

**Assessment (AI, 2026-11-11):** review panel (full): ship after changes (applied: the 67 control probes and the two rows without clinical data dropped, the recording note corrected, `Class-dependent Recording` and `Selection Bias` added); curator: issue 1 A (restated use-case reason), issue 2 B (AD218 and AD224 dropped). Priority 1: gap 0, use case 0 (named by the source, fit approximate), source + (paper and the study's own deposit), shape 0 (123 rows), risk - (soft label, recording difference kept).

**Assessment (AI, 2026-11-11):** review panel (full, a second pass at Lennart's ask on PR #75): ship after changes; disputed: USE-1 (the PR's undated amendment; sign it or treat like lung_cancer), TP-5 (15 metastases, 5 per test fold; Kendall's W 0.187 beside parkinsons 0.204 and musk 0.120, so the measure does not decide); agreed fixes under USE-6 (age, sex, pack-years), USE-8 (the sheet's negatives exclude the hard cases), LEAK-15 (the recording note's mechanism), CLEAN-25 (No/Yes) and six claim corrections; for the curator: issues 1-3.

CC (2026-11-11, Lennart): the second review panel's issues: 1, B (USE-1 amended on this case, with its date, curator and case; the use case names the expression tissue-of-origin test as the pathologist's second opinion when the stains leave the origin open), 2, A (kept at 15 metastases, 5 per test fold, about twice parkinsons'; the count decides, since Kendall's W does not separate musk from parkinsons), 3, B (the nine agreed fixes: age, sex and pack-years as features; the target as No / Yes; the notes on the negatives, the four positives staged as primaries and the recording mechanism; the claim corrections; PROV-7 for the new record).

CC (2026-11-11, Lennart): the declared metric, ROC AUC (the binary fallback; the source scores no classifier), is checked as declared.

## Review

**Outcome:** added. A primary lung adenocarcinoma against a metastasis from another organ, on the study's own GEO arrays (123 tumours, 15 metastases, 5 per test fold). The review panel recommends shipping after changes.

- **Validity:** no leak, the random split holds, and the recording difference does not carry the score. But the task rests on an unsigned change to the use-case rule (issue 1).
- **Value:** the signal is real, but with 15 metastases only method gaps of about 0.08 ROC AUC rank (issue 2).
- **Quality:** nine agreed fixes, among them three clinical inputs, the target's words and wrong statements in the notes (issue 3).
- **Weighed:** a strong source, a use case at the weak end of approximate, a small size and a soft label.

Either of issues 1 and 2 can still end at `No`.

**Main points:** Sign the PR's use-case wording, or retire the task like lung_cancer? Keep it at 15 metastases, or retire it as too small? Ask Andrej to apply the nine fixes the panel agreed on?

**Record judgment:** valid provenance. Every flag, row and quote checks out against the study's annotation sheet, its arrays and the paper. The record's numbers hold apart from the details listed in issue 3.

**Issues for Lennart:**

1. **Sign the PR's new use-case wording, or retire the task like lung_cancer?**

   * **Problem:**
     - The PR adds a sentence to the use-case rule (a label read from the specimen leaves only a cross-check; a label from a separate work-up is ground truth) without a date or a curator, while lung_cancer's retirement note says the rule did not change[^use1][^lcnote].
     - This label fits neither branch: it is written in the resected tumour's pathology note, but it rests on an earlier cancer outside the specimen.
     - The rule admits no exception for one dataset, so shipping needs the change signed as an amendment; without it the case is lung_cancer's[^must].
   * **Background:** lung_cancer (the same arrays) was retired on 2026-11-10 because the slide settles the histology and a doubting pathologist orders a two-stain panel, not an expression array[^lcret]. This definition says the same: "an expression array is not used today".
   * **Effect on the task:** most of the score is colon against lung (out of fold 0.98), the part a two-stain panel (CDX2 for colon, TTF-1 for lung) settles at the microscope. Breast against lung reaches 0.75, the three other metastases 0.76 to 0.83.
   * **Evidence:**
     - Nine unfitted pathology marker genes reach ROC AUC 0.82, so much of the task is the stain panel read off an array.
     - The domain practitioner, playing the pathologist, calls the fit approximate at its weak end, not none: the decision is real in thoracic pathology.
     - Expression tissue-of-origin assays exist (Pathwork Tissue of Origin, CancerTYPE ID). They are niche, run on formalin-fixed tissue blocks, serve mostly cancers whose origin is unknown, and the US cancer guidelines (NCCN) do not recommend them as standard.
   * **Consistency:**
     - Retired on a same-specimen label: glioma_grading_clinical_and_mutation_features (2026-10-26, Lennart) and lung_cancer (2026-11-10, Andrej).
     - Kept on a separate work-up: ljubljana_primary_tumor.
     - A signed amendment needs the earlier decisions under the rule re-read, glioma and tcga_lung_histology above all.
   * **Panel:**
     - The advocate and the critic agree that the use case should name the tissue-of-origin assay as a second opinion when stains leave the origin open.
     - The critic and the mediator hold that only a signed amendment carries the case, and that no exception is possible.
     - The blind reviewer, without our notes, would not benchmark the task.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | As in the PR (implemented) | ships with the undated wording | no further work | an unsigned change to a rule that admits no exception; contradicts lung_cancer's own note |
     | B | Sign the amendment, restate the use case | the wording gets its date, curator and case; the use case names the tissue-of-origin assay; lung_cancer's note is corrected; the earlier decisions under the rule are re-read | keeps the decision the source calls "a key issue in lung tumor diagnosis"; the line between the cases is written down | the assay is niche and serves mostly unknown primaries; the primaries the question is about, a new lung tumour after an earlier cancer elsewhere, are absent (issue 3) |
     | C | Retire like lung_cancer | `No (Retired)` with `No Good Target / Scientific Discovery` | one rule for one set of arrays | drops a decision a pathologist does face |

   * **Recommendation:** B. The domain practitioner, playing the pathologist, confirms a real if weak decision, and both sides of the debate accept the restated use case. **Decision:** A, B or C?

   **Notes for the AI:**
   - **On B:**
     - In `use_case.md`, mark USE-1 "(Must; amended <date>, Lennart, on lung_adenocarcinoma_metastasis)". Add the branch: "A label written in the specimen's note that rests on information outside the specimen (an earlier cancer elsewhere) is a prediction target, not a cross-check."
     - Add a CC line to `lung_cancer.md` that corrects "Not a rule change".
     - Run `decision_register.py --rule USE-1` and re-read glioma_grading_clinical_and_mutation_features and tcga_lung_histology.
     - Apply change 4 of issue 3.
   - **On C:** set the record to `No (Retired)` with the marker, remove the folder, clear `v2_path`, and add a CHANGELOG entry.
   - The branch is Andrej's (`lung-cancer-geo-retire`). Apply only with his agreement, or hand him the text as a PR comment.

   [^use1]: **USE-1** (Must), as this PR words it: "A label read from the same specimen the features measure, and settled before they are taken, leaves only a cross-check of a known label and fits no decision. A label found by a separate work-up is ground truth, also when the rows are a retrospective series of resolved cases."
   [^lcnote]: lung_cancer, CC of 2026-11-10 (Andrej): "Not a rule change."
   [^lcret]: lung_cancer, retired 2026-11-10 (Andrej), `No Good Target / Scientific Discovery`: "a pathologist in doubt orders a two-stain panel, not an expression array"; "the test labels come from the easy cases only".
   [^must]: **principles.md**, "Exceptions and amendments": "A Must has no exceptions: only a higher-ranked Must overrides it, and anything else is an amendment." An amendment "is replaced in place under the same ID, with the date, the curator and the case that prompted it".

   **Lennart (2026-11-11, change):** Option B: Sign the amendment, restate the use case.

   **Resolved (2026-11-11, Lennart):** B. USE-1 is amended under its ID with the date, the curator and this case: a label
   written in the specimen's own note that rests on information outside the specimen (an earlier cancer elsewhere) is a
   prediction target when the actor decides it with a tool that predicts it. The use case names the expression
   tissue-of-origin test as the pathologist's second opinion when the stains leave the origin open, and "an expression
   array is not used today" is replaced. lung_cancer's record gets a CC line correcting its "not a rule change".
   Re-read under the amendment, glioma_grading_clinical_and_mutation_features, eucalyptus and tcga_lung_histology stay
   cross-checks (their labels are settled on the specimen), as the USE-1 Cases row now says.

2. **Are 15 metastases, 5 per test fold, too few to rank methods?**

   * **Problem:**
     - The size rule sets no number, and this dataset sits between parkinsons (8 in total, 2 to 3 per fold, retired) and musk (about 39 in total, 13 per fold, kept)[^tp5].
     - The automatic size check flags too few positives only below 5 per fold, so its silence decides nothing at exactly 5.
     - The reason the definition gives for accepting the warning ("the methods separate, 0.876 against 0.836") does not survive resampling the patients (a bootstrap over the 123 patients, 500 draws).
   * **Effect on the task:**
     - Only method gaps of about 0.08 ROC AUC or more rank reliably.
     - One fold's score has a standard deviation of about 0.09.
     - "The random forest wins 20 of 20 repeats" recombines the same 15 patients.
   * **Experiments:**
     - The mediator ran the measure that decided parkinsons, like for like: the agreement of the method ranks across the 60 folds (Kendall's W, random forest, extra trees, logistic regression, LightGBM). It is 0.187 here, 0.204 for parkinsons and 0.120 for musk, all three in the lowest tenth of 120 BeyondArena datasets (6 to 8 percent below them; median 0.772). The measure ranks the kept musk below the retired parkinsons, so it cannot decide this case.
     - Method pairs resolved: 3 of 6 under the patient bootstrap, 4 of 6 under the paired fold test. On the paired fold test, parkinsons resolves 5 of 6 and musk 4 of 6.
     - Five folds would leave 3 metastases per fold (one fold's standard deviation 0.134), so no re-split helps.
   * **Consistency:**
     - parkinsons was retired on 2026-10-05 (Lennart) and musk kept on 2026-10-06. heart_disease_switzerland (`No`) and labor (2nd tier) sit at 2 to 4 per fold.
     - This would be the first accepted few-positives warning in the working copy.
   * **Panel:** the blind reviewer would exclude the task (too small, a third of the positives only suspected). The critic counts the total as the size rule does: 15 sits nearer parkinsons' 8 than musk's 39. Parkinsons' own test, which the critic asked for, has run and does not decide. The advocate and the mediator lean towards keeping it, since 5 per fold is about twice parkinsons' count.
   * **Unknown:** what set musk apart from parkinsons when they were decided, the count per fold or something else; whatever it was decides this case.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep (implemented) | ships; the definition's note on the few metastases and a new precedent row of the size rule give the bootstrap numbers | keeps a real signal the source names; 5 per fold is about twice parkinsons' | only large gaps rank; the hard part (breast and other) holds 7 metastases |
     | B | `Too Small` | retired | follows parkinsons and heart_disease_switzerland | drops a learnable task (every method well above chance) |
     | C | Keep, and write a floor into the size rule | amends the rule with a per-fold and a total floor that this case passes | settles the next borderline case by count, not by a measure that ties musk and parkinsons | a floor set from three cases |

   * **Recommendation:** A. The measure both sides chose ties a kept precedent with a retired one, and the count per fold sits above parkinsons'. Choose C if you want the line written down. **Decision:** A, B or C?

   **Notes for the AI:**
   - **On A or C:**
     - Replace the `splits_test_minority_few` reason with: "15 metastases give 5 per test fold; under a patient bootstrap only gaps of about 0.08 ROC AUC rank (random forest minus logistic regression -0.007 to +0.089); Kendall's W 0.187, beside parkinsons 0.204 and musk 0.120 (review panel, 2026-11-11)."
     - Add a TP-5 Cases row with these numbers and the curator's call.
   - **On C:** draft the floor as an amendment of TP-5 for Lennart, with date and case.
   - **On B:** set `Too Small`, retire, and add a CHANGELOG entry.
   - The numbers and scripts are in the mediator's report below.

   [^tp5]: **TP-5** (Must): "`Too Small` means a handful of units of a class, per test fold and in total, counted in the unit the task is scored on (parkinsons: 8 healthy people, 2-3 per fold; retired). A small dataset as such is a tiny-data task like the others (musk: 102 molecules, 13 musk per fold; kept)."

   **Lennart (2026-11-11, as implemented):** keep.

   **Resolved (2026-11-11, Lennart):** A. Kept at 15 metastases, 5 per test fold, about twice parkinsons' 2 to 3. The
   accepted `splits_test_minority_few` now gives the bootstrap interval and the Kendall's W comparison, and the TP-5
   Cases row records the call (the measure parkinsons was described by does not separate musk from parkinsons, so the
   count decided).

3. **Ask Andrej to apply the nine fixes the panel agreed on?**

   * **Problem:**
     - No panellist disputes these nine fixes, and none moves a score by more than 0.01, but they are on Andrej's branch, which this review did not edit.
     - Two of them change the shipped data: the three clinical columns and the target's words.
     - The others correct statements in the definition and the record that the data contradicts.
   * **Changes:**
     1. Add age, sex and pack-years from GEO as features. They are known at surgery and the definition leaves them out without a reason[^use6]. The random forest moves from 0.879 to 0.884; logistic regression is unchanged.
     2. Rewrite the fit reason and the selection note to quote the sheet's definition of the negatives ("Adenocarcinoma w/ no history or path indicating non adeno"): the hard negatives, a new primary after an earlier cancer, are absent, not just unrecorded[^use8].
     3. Add to the label note: 4 of the 15 metastases (AD163, AD172, AD178, AD186) were staged as lung primaries, and the paper's 12 suspected metastases appear to leave out two or three of them.
     4. Replace "an expression array is not used today" with the tissue-of-origin assays, a second opinion when stains leave the origin open, and name them as the actor's tool in the use case.
     5. Correct the recording note[^leak15]:
        - the cause is dimmer arrays scaled up by the array software's per-array normalisation (MAS5; the scaling factor alone separates the classes at ROC AUC 0.62, the share of genes called present at 0.71), not scanner noise;
        - the difference holds within processing batches (0.72 to 0.74);
        - ranking the genes within each array removes it at no cost (0.848 against 0.846);
        - so "cannot be removed" goes.
     6. Target words "No" / "Yes", with "Yes" the metastasis[^clean25]. Today the event sorts first, so a participant who passes P(metastasis) as the second column gets a mirrored ROC AUC (0.18 instead of 0.82).
     7. Claim fixes:
        - nine marker genes, not ten (NAPSA has no probe set on this array);
        - the "other" metastases at 0.76 to 0.83 (3 rows);
        - "the 123 arrays" scanned 16 March to 17 April 2001 (the study ran to 25 April);
        - the model named behind the control probes' 0.695;
        - split counts given for the grouped-fold numbers;
        - "first piece, first hybridisation" corrected: for 10 re-hybridised tumours the first title in GEO's order is the later preparation.
     8. Rewrite the reason for the accepted few-positives warning as issue 2 decides.
     9. Cite the rule for one source with two tasks, not the one for a rebuild, as the reason for the new record[^prov].
   * **Effect on the task:** 12,561 features instead of 12,558, and the classes renamed. No score moves by more than 0.01.
   * **Panel:** the advocate, the critic and the mediator all list these fixes. The column auditor first called the clinical columns a weighing call; the mediator rules them a requirement, since no higher rule asks to drop them.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | As in the PR (implemented) | nothing changes | no further work | known wrong statements ship; three known inputs are left out without a reason |
     | B | All nine | Andrej applies them on his branch (or agrees that they are applied) | the definition says what the data shows; the known inputs are in | one more round on the PR |
     | C | All but the clinical columns | the expression profile alone, with the reason stated | keeps a pure expression task | leaves out inputs known at the decision, which the rules do not allow without a higher reason |

   * **Recommendation:** B. No panellist disputes the fixes, none moves a score by more than 0.01, and the rules ask for inputs known at surgery unless a higher rule drops them. **Decision:** A, B or C?

   **Notes for the AI:**
   - The exact texts are in the mediator's report below ("Changes that need no decision", 1 to 9).
   - Hand them to Andrej as a PR comment on #75. Apply them on `lung-cancer-geo-retire` only with his agreement, then re-run `dataset check` and the task probe.
   - For change 1, read `!Sample_characteristics_ch1` from the series matrix (`age`, `Sex`, `normalizedsmokinghistoryinpackyears`). Age and pack-years are numeric, sex is categorical, and the two missing pack-years stay missing.

   [^use6]: **USE-6** (Must): "Anything known at the prediction point is a legitimate input ... dropping it changes the task."
   [^use8]: **USE-8** (Must): the fit is approximate when it is "a stand-in with a known gap, named as such"; a selection the setting does not share is such a gap, and `fit_reason` names it.
   [^leak15]: **LEAK-15** (Must): a recording artefact "that cannot be undone ... retires the dataset"; one that can be undone, or does not carry the score, is fixed or kept with a note. Cases: prostate_cancer_detection (retired), gallstone_disease (kept).
   [^clean25]: **CLEAN-25** (Should): a binary target ships as "No" / "Yes", with "Yes" the event, unless the source names the classes in words; here the definition built the words itself.
   [^prov]: **PROV-7** (one source, two tasks: parkinsons and its telemonitoring sibling) fits the new record; **PROV-14**, a rebuild from other sources, does not.

   **Lennart (2026-11-11, change):** Add all nine fixes here and then push and update the PR

   **Resolved (2026-11-11, Lennart):** B. All nine applied on the PR's branch:
   - age, sex and pack-years are features (123 rows, 12,561 features; random forest ROC AUC 0.878, logistic regression
     0.849 on the task probe);
   - the target is `No` / `Yes`;
   - `fit_reason` and the Selection note quote the sheet's negatives;
   - the label note names the four positives staged as primaries;
   - the use case and the prediction point name the tissue-of-origin test;
   - the recording note gives the scaling mechanism, the within-batch result and the within-array rank;
   - the claim corrections (marker genes, the "other" score, scan dates, the controls by model, split counts, the array
     choice);
   - the accepted warning's reason;
   - the new record is cited under PROV-7.

   `dataset check` is clean, and the task and leak probes raise no flag.

**Review panel:** ship after changes (mediator). Full panel, a second pass run on 2026-11-11 at Lennart's ask (the first panel, run for Andrej the same day, left only its one-line summary in the record). Claim audit: 33 claims, no validity claim refuted, 4 details wrong, 4 untested. Blind review: would not benchmark (15 mixed positives, a third only suspected). Task gamer: no exploit beats an honest model beyond the noise. Agreed: no leak, the random split, the recording difference does not carry the score, notes on the soft positives and the negatives, the clinical columns and the other fixes (issue 3). Disputed: the use-case amendment (issue 1) and the size (issue 2).

<details><summary>Mediator</summary>

**Mediator report: lung_adenocarcinoma_metastasis (PR #75), 2026-11-11**

**Recommendation (judgment record)**

```text
Verdict: ship after changes. Two curator calls (issues 1 and 2) can still end at No.
Validity: USE-1 open: the PR's USE-1 text is an amendment of a Must with no date or curator (issue 1); USE-2 not
triggered (a decision exists, the source names it); USE-5 holds approximately, note added; USE-6 triggered, fixed by
shipping age, sex and pack-years; USE-8 approximate, fit_reason understates the negatives (fixed by a note);
LEAK-1/10/27/30 hold; LEAK-15 not triggered (the artefact can be undone and does not carry the score), note
rewritten; SPLIT-1 holds; PROV-1 holds, PROV-7 is the rule to cite (not PROV-14).
Value: TP-2 real signal; TP-5 open (issue 2): Kendall's W 0.19 sits at the same percentile as parkinsons (retired), but
musk (kept) sits lower still, so W cannot decide; MET-2 holds (5 positives in all 60 test folds); roc_auc fallback.
Quality: CLEAN-25 target words "No"/"Yes"; six claim fixes.
Weighed: size -, source +, use case 0 (approximate, weak end), label softness -.
For the curator: issue 1 (date and sign the USE-1 amendment, or treat like lung_cancer), issue 2 (is 5 per fold and
15 in total "a handful" under TP-5).
```

**Agreed facts** (no panellist disputes these; re-tested by at least one panellist)

- 123 rows, one array per patient, 15 positives (8 colon, 4 breast, 3 other). Each test fold holds 5 positives and 36 negatives in all 60 folds. The 15 positives are exactly the 15 remaining sheet flags, matched to their arrays by signal values (claim auditor, blind reviewer).
- No exact or near copies across the split. The hidden-group probe finds 123 clusters of 1. Folds grouped by IVT batch or by scan day score the same as the random folds. One site.
- Every label-bearing column is correctly left out: GEO stage (M1 for 11 of 15 positives), the expression cluster `CM` (8 of 15 positives), and the pathology notes ("met" in 14 of 15). MAS5 is computed on each array alone, with a trimmed mean of 499 ± 0.3, so LEAK-30 holds.
- Recording difference:
  - Metastasis arrays are dimmer and MAS5 scales them up (scaling factor AUC 0.62). Scanner noise and background do not differ.
  - The difference persists inside batches (within-IVT-batch pairs 0.74), and batch adds its own component.
  - It does not carry the score. Within-array ranks give 0.848 against 0.846. Regressing it out leaves at least 0.800.
- The sheet defines the negatives as "no history or path indicating non adeno". The hard negatives (a new primary after an earlier cancer) are essentially absent.
- 4 of the 15 positives were staged as lung primaries without M1 (AD163, AD172, AD178, AD186).
- Age, sex and pack-years are known at surgery and are in GEO for all rows (pack-years for 121). Adding them moves RF from 0.879 to 0.884 and leaves LR unchanged.
- The event "metastasis from another organ" sorts first. A participant who passes P(metastasis) as the second column gets a mirrored AUC (0.18).
- Expression tissue-of-origin assays exist (Pathwork, CancerTYPE ID). They are niche, run on FFPE, and are mainly used for unknown primaries. NCCN does not recommend them as standard.
- Method gaps: only gaps of about 0.08 or more resolve under the patient bootstrap. "RF wins 20 of 20 repeats" recombines the same 15 patients.

**Changes that need no decision** (to propose to the PR author; this review does not edit the branch)

1. **Add `age`, `Sex` and `pack_years` from the series matrix as features** (USE-6, Must). They are known at the prediction point. Leaving them out without a higher-ranked Must breaks USE-6, so "profile alone" is not an available option. The two missing pack-years stay missing (USE-7). The cost is measured as nil.
2. **Rewrite `fit_reason` and the Selection bullet** (USE-8, Must) to quote the sheet's definition of the negatives ("Adenocarcinoma w/ no history or path indicating non adeno") and to say the hard negatives are absent, not just unrecorded. Keep the fit approximate and the `Selection Bias` marker.
3. **Label bullet** (USE-5): "4 of the 15 (AD163, AD172, AD178, AD186) were staged as lung primaries (no M1); the paper's 12 suspected metastases appear to exclude two or three of them."
4. **Replace "an expression array is not used today"** (USE-1, USE-9). New text: "expression tissue-of-origin assays (Pathwork, CancerTYPE ID) exist as a second opinion when IHC is inconclusive, mostly for unknown primaries and on FFPE; the routine work-up is IHC, comparison with the earlier tumour and comparative sequencing." Name that assay as the actor's tool in `use_case`.
5. **Rewrite the LEAK-15 note** (LEAK-15, Must):
   - The mechanism is dimmer arrays scaled up by MAS5 (scaling factor 0.62, share present 0.71); scanner noise and background do not differ.
   - Name the noise-floor probes `1513_at` and `31760_at`.
   - Add the within-batch result (0.72 to 0.74) and the batch component.
   - Give the reason it does not carry the score: within-array ranks 0.848 against 0.846, lower bound 0.800.
   - Remove "cannot be removed".
   - Add the case as a row of LEAK-15's Cases table, not only inline.
6. **Target words "No" / "Yes"**, with "Yes" the metastasis and sorting second (CLEAN-25, Should; no fact sets this case apart).
7. **Claim fixes** (EV-1, writing.md):
   - "first piece, first hybridisation" becomes "the first title in GEO's sorted order; for 10 re-hybridised tumours the later preparation". Taking the study's `Sample1` instead (CLEAN-1) is an optional alternative; it moves no score.
   - Nine marker genes, not ten: NAPSA has no probe set on HG-U95Av2 (score 0.817).
   - "Other" out-of-fold AUC: 0.76 to 0.83 (3 rows, unstable).
   - "The 123 arrays" were scanned 16 March to 17 April 2001.
   - Name the model behind the controls' 0.695 (LR 0.736, RF 0.621).
   - Give split counts or ranges for the grouped-fold numbers in `splits_comment`.
8. **Rewrite the accepted warning `splits_test_minority_few` and the TP-5 Cases row.** "The methods separate (0.876 against 0.836)" and "no flag" do not hold at exactly 5 per fold. Replace them with the numbers below (patient-bootstrap CI of RF − LR −0.007 to +0.089; W 0.19). The verdict in the row follows issue 2.
9. **Cite PROV-7** (one source, two tasks) instead of PROV-14 for the new record, and reword the PROV-14 case row.

**Issues for the curator, ranked**

**Issue 1 (P3, USE-1, Must; validity): is the USE-1 text in this PR a deliberate amendment?**
- **Problem.** The PR adds wording to USE-1 (a same-specimen label fits no decision; a separate work-up is ground truth) and lists this dataset as a third kind of case. The text has no date and no curator. lung_cancer's CC of 2026-11-10 says "not a rule change". The label fits neither branch of the new text: it is not a separate work-up, and it is not settled.
- **Settled by rank: the route is an amendment, not an exception.** principles.md says a Must has no exceptions, and anything else is an amendment. The advocate's "recorded distinguishing fact" route is not available for a Must.
- **Effect.** Without the amendment, the case is lung_cancer's: the same arrays, the same kind of note label, retired. With it, glioma and tcga_lung_histology need a `decision_register.py --rule USE-1` pass.
- **Advocate's best evidence.**
  - The call rests on an earlier cancer that is outside the specimen and outside the features. The slide cannot settle it.
  - Expression tissue-of-origin assays answer lung_cancer's second ground ("orders a two-stain panel").
  - The domain practitioner, as the actor, calls the fit approximate, "not none".
- **Critic's best evidence.**
  - The assays serve unknown primaries on FFPE and are not standard of care.
  - The practitioner says that use case "still needs the hard negatives".
  - The score rests on colon against lung (0.98), which a CDX2/TTF-1 stain settles at the microscope.
- **Decision needed.**
  - (d) Sign and date the amendment (curator, date, case), correct lung_cancer's "not a rule change" line, run the register pass, and restate the use case around the assay (change 4). Then ship.
  - (b) Treat it like lung_cancer: `No`, `No Good Target / Scientific Discovery`.
  - My recommendation is (d) with change 4, since the actor confirms a real, if weak, decision.

**Issue 2 (P6, TP-5, Must; value): are 15 positives, 5 per fold, "a handful"?**
- **Problem.** TP-5 sets no number. This dataset sits between parkinsons (8 in total, 2-3 per fold, retired) and musk (about 39 in total, 13 per fold, kept).
- **The decisive experiment (table below)** places this dataset's W (0.187) at the 8th percentile of 120 BeyondArena datasets. That is exactly parkinsons' percentile (W 0.204).
  - Read literally, the criterion both sides agreed on ("lands where parkinsons did") points to `Too Small`.
  - But musk, which was kept, has a lower W than parkinsons on every method set: 0.120 on these four methods, and below parkinsons on the house's 20 configurations too.
  - So W never separated the two precedents. parkinsons' retirement rested on its count (2-3 per fold), and W only described it. The experiment cannot decide this issue. What remains is a weighing of counts.
- **For keep:**
  - Per fold, 5 is about twice parkinsons' 2-3.
  - 3 of 6 method pairs are resolved under the patient bootstrap, and 4 of 6 under the paired fold test (musk 4 of 6, parkinsons 5 of 6).
  - The signal is real (TP-2).
- **For `Too Small`:**
  - In total, 15 is nearer parkinsons' 8 than musk's 39.
  - The hard part (breast and other, 7 positives) is smaller still.
  - The W percentile equals parkinsons'.
  - RF against LR, the headline gap, is not resolved.
- **What would settle it:** a count-based reading of TP-5 (an amendment with a per-fold and total floor), or a curator statement of which fact sets musk apart from parkinsons.
- **Decision needed:** keep, with a TP-5 Cases row giving these numbers, or `Too Small`. A re-split cannot fix it (5 folds leave 3 per fold). I lean keep, because the measure both sides chose does not separate a kept precedent from a retired one, and the count sits above parkinsons'. This is a weighing; the curator decides.

**Disputed points settled**

- **USE-1 route (exception or amendment):** amendment, by principles.md ("A Must has no exceptions"). Critic's side. Whether to make the amendment is issue 1.
- **Does the assay fact set the case apart as the use case is worded now?** Only once the use case names the assay as the actor's tool, which both sides now accept (change 4). The "not used today" sentence contradicts the fact and goes.
- **USE-5, AD172 and AD186:** a note, no relabelling. The curator's issue 8, A ranks above an AI argument. The critic withdrew. The "?Br MET" flags (in the clinical sign-out, coded consistently) differ in fact from AD218 and AD224 (a `PATH II` query coded both ways).
- **LEAK-15:** not triggered. Both sides conceded after tests: the class difference holds within batch, and a label-free per-array rank removes it at no cost. LEAK-15 retires only an artefact that "cannot be undone", so the remedy is a note (change 5).
- **USE-6:** a Must, not a weighing. The column auditor's "weighed here" is overruled by rank: no higher Must requires dropping the three columns. Change 1.
- **TP-5, what W 0.22 shows:** the critic's W (4 methods, kNN in the set) and the advocate's breast_cancer comparison are both superseded by the like-for-like run below. Neither side's inference holds unqualified.

**Task gamer's exploits, mapped** (the definition has no `Potential leak, kept on purpose:` note; its accepted warnings are about the licence and the minority count)

| # | Exploit | Rule | Known or new | Measured gain | Issue? |
|---|---|---|---|---|---|
| 1 | Clusters fitted on train and test rows | LEAK-30 (transductive) | new | +0.009, within noise (k chosen after the fact) | no |
| 2 | Standardising over all rows | LEAK-30 | new | +0.0006 | no |
| 3 | Last-digit shares (format) | LEAK-39 (recording fingerprint) | new | +0.0004; 0.662 alone against a shuffled best of 0.633 | no |
| 4 | Self-training on test rows | LEAK-30 | new | −0.002 | no |
| 5 | Array scale proxies | LEAK-15 | known (`Class-dependent Recording` note) | −0.02 to −0.10, consistent with the note | no; the note's wording is fixed by change 5 |
| 6 | Label partly from the expression clustering | USE-5, LEAK-27 | known: AD218 already dropped as undetermined | not measurable; the remaining 7 colon flags in `CM` are the paper's "previously diagnosed" | no |
| 7 | Mirrored AUC from class order | CLEAN-25 | known (main session) | 0.82 to 0.18 if misused; no score change for correct use | fixed by change 6 |

**Consistency with precedent**

- **Followed:**
  - USE-8 approximate with `Selection Bias` (ljubljana_primary_tumor, eryhemato, differentiated_thyroid).
  - LEAK-15 keep like gallstone_disease. Unlike prostate_cancer_detection, the same-label test (advocate, critic) shows the label signal far exceeds the artefact.
  - The roc_auc fallback (glioma, gallstone, heart_disease).
  - CLEAN-22 width (coad).
  - PROV-7 new record (parkinsons/telemonitoring).
- **Departure without a stated fact (issue 1):** lung_cancer and glioma were retired on same-specimen labels. The fact that sets this case apart (an earlier cancer outside the specimen; assays as a second opinion) can only carry through a signed amendment.
- **Reflection question (issue 2):** musk (kept, 2026-10-06) has a lower W than parkinsons (retired, 2026-10-05) on every method set I tested. What set musk apart from parkinsons: the count per fold (13 against 2-3), or something else? Whatever that fact is, it decides this case. If it is the count, would you write the floor into TP-5 (an amendment), so the next borderline case does not turn on W?
- **Drift:** Andrej reversed "too few to rank methods" (2026-11-10) to keep (2026-11-11), with a reason ("no flag") that does not hold at exactly 5 per fold. It is flagged under issue 2, not as drift.

**TP-5 experiment** (Kendall's W of the method ranks across folds, house formula; four BeyondArena default families)

| Dataset | Folds | W (RF, XT, LR, GBM) | Share of 120 BeyondArena datasets with lower W | Among the 40 with 60 folds | Among the 19 with roc_auc and 60 folds |
|---|---|---|---|---|---|
| lung_adenocarcinoma_metastasis (this run) | 60 | **0.187** (null 95th pct 0.041) | 8.3% | 17.5% | 21.1% |
| parkinsons (retired) | 60 | 0.204 | 8.3% | 17.5% | 21.1% |
| musk (kept) | 60 | 0.120 | 5.8% | 12.5% | 15.8% |
| lung_cancer (same arrays, histology target) | 60 | 0.959 | 74% | 92.5% | — |
| BeyondArena median | | 0.772 | | | |

- **Check against the precedent's own number:** on the house's set (default + tuned_ensemble, 20 configurations), parkinsons has W 0.196, lower than 99% of datasets (the record says 98% at W 0.18). musk has W 0.196 there too, lower than all 120.
- **Adding XGB and CAT defaults** (6 methods): parkinsons 0.164 (4th percentile), musk 0.142 (1st). musk stays below parkinsons.
- **Method scores on this dataset** (mean per-fold ROC AUC): RF 0.881, XT 0.888, LR 0.846, GBM 0.819. Per-fold SD 0.09 to 0.12.

| Pair | Mean gap | Repeats won | Paired fold test (2 SE) | Patient bootstrap 95% CI (500 draws) | Resolved |
|---|---|---|---|---|---|
| RF − XT | −0.007 | 6 of 20 | no | −0.020 to +0.007 | no |
| RF − LR | +0.035 | 20 of 20 | yes | −0.007 to +0.089 | no |
| RF − GBM | +0.062 | 18 of 20 | yes | +0.030 to +0.104 | yes |
| XT − LR | +0.042 | 20 of 20 | yes | +0.004 to +0.087 | yes |
| XT − GBM | +0.069 | 18 of 20 | yes | +0.034 to +0.107 | yes |
| LR − GBM | +0.027 | 11 of 20 | no | −0.023 to +0.075 | no |

On the same paired fold test, parkinsons resolves 5 of 6 pairs and musk 4 of 6. No patient bootstrap is possible on BeyondArena results.

**Proxy limits:**
- XGBoost and CatBoost are not installed in the brief's interpreter, and kNN is not in the three suites. The set is therefore the four families that both sides have.
- The library defaults differ from the benchmark's:
  - No 8-fold bagging.
  - LightGBM uses 100 trees at learning rate 0.1, not AutoGluon's 0.05 with early stopping.
  - RF and XT use 300 trees.
  - LR approximates AutoGluon's preprocessing (skewed columns quantile-normalised, the rest standardised, C 1).
- The reference uses the benchmark's own runs. W is compared across these two setups as a rank-agreement proxy.

</details>

<details><summary>Claim audit</summary>

**Claim audit: lung_adenocarcinoma_metastasis (PR #75), claim auditor, 2026-11-11**

**Summary.** No validity claim is refuted. The label's provenance holds on every point I checked against `SampleData.xls` and `13790.pdf`:
- 16 flags, 8 colon / 4 breast / 4 other.
- The footer rows "possible mets 16", "Adenocarcinoma plus mets 139" and "…no history or path indicating non adeno 123".
- 15 flags appear in the clinical pathology note; AD218's appears only in `PATH II`; AD224 is coded primary despite a "met?" note.
- 125 = 139 − 12 `A` patients − AD355 − AD360.
- The paper's quotes are verbatim.

I matched each curated row to its GEO array by its signal values. The 15 positives are exactly the 15 remaining sheet flags, so the label is on the right arrays. The metric is computable on all 60 folds. Four claims are inaccurate in detail, all minor:
- NAPSA has no probe set on HG-U95Av2, so the "ten marker genes" are nine.
- The "other met" out-of-fold AUC (3 rows) does not reproduce: 0.76 here against 0.83 claimed.
- The scan dates of the whole study run to 25 April, not 17 April.
- The controls' 0.695 depends on the model used.

Separately from any written claim, I found a label-validity question for the curator (rank P3, USE-5): 4 of the 15 positives were clinically staged as lung primaries.

Scratch outputs are in the run folder: `meta.py`, `align.py`, `rec.py`, `batch.py`, `models.py`, `rowmeta_aligned.csv`, `oof.csv`, `paper.txt`, and copies of `SampleData.xls` and `13790.pdf` read from the archive.

**Claims table**

| # | Claim | Source | Test | Result | Evidence | Rule |
|---|---|---|---|---|---|---|
| 1 | Sheet DATASET B flags 16 of 139 adenocarcinomas (Colon Met 8, Breast 4, other met 4) and counts the rest as "no history or path indicating non adeno" | CC Label; record | Parsed DATASET B | holds | 139 unique `AD` rows; flag counts 8/4/4; footer rows "possible mets 16", "Adenocarcinoma plus mets 139", "…non adeno 123" | PROV-1, USE-5 |
| 2 | 15 of 16 flags are in the resected tumour's clinical pathology note; AD218's only note is `PATH II` "ad w met?" | CC Label | Read the notes of all 16 flags; searched the unflagged rows' notes for met/colon/br | holds | AD218's clinical note is "ad 5.0 m BAC", its `PATH II` note "ad w met?". The other 15 carry "MET COLON", "c/w colon (met)", "(?Br MET)", "c/w br met" or "(met)". Of the 123 unflagged rows, only AD224's notes mention met (`PATH II` "ad m met?") | USE-5 |
| 3 | AD224 has the same `PATH II` wording and is coded primary | CC AD218/AD224 | Sheet | holds | AD224: clinical note "ad 2.0 w w/BAC", `PATH II` "ad m met?", no flag, cluster C3 | USE-5 |
| 4 | AD218 is in the colon cluster `CM` | CC | Sheet | holds | AD218 is `CM` | – |
| 5 | The paper's quotes ("A key issue in lung tumor diagnosis…", Results; "metastases of nonlung origin can be difficult to distinguish…", Introduction) | task_summary use_case; CC Prediction point | `13790.pdf` text | holds | Results heading "Identification of Adenocarcinomas Metastatic to the Lung", and the Introduction paragraph (refs 7, 8), both verbatim | USE-1 |
| 6 | "125 adenocarcinoma samples [...] associated with clinical data" = 139 − 12 `A` − AD355 − AD360 | CC Rows; record | Paper Methods; counted the non-empty clinical fields of DATASET A | holds | The paper quote is verbatim. Survival, Sex, Smoking, Stage and Clinical Path are filled for exactly 125 `AD` patients. Empty are AD1, 2, 3, 4, 5, 7, 10, 15, 16, 18, 19, 31, 355, 360. AD355 and AD360 hold "NA-" in Operation and Age, plus a tumour % ("all empty" is near enough) | PROV-1 |
| 7 | The 12 `A` patients are `AD1`-`AD31` in the sheet | CC Rows | GEO titles against sheet ids | holds | GEO patients A1, 2, 3, 4, 5, 7, 10, 15, 16, 18, 19, 31 match the sheet's AD ids up to 31; no numbered GEO patient collides with them. AD5 and AD7 sit in the `CM` cluster without data, which supports "no flag is no finding" | USE-5 |
| 8 | 7 colon flags are the paper's "seven samples [...] previously diagnosed as metastases of colonic origin"; AD350 is the colon flag outside `CM` and is mucinous | CC Label, Known doubts | Paper; sheet | holds | The paper's `CM` has 12 samples, 10 with clinical information and 7 diagnosed colon. The sheet's `CM` holds 12 (incl. `CM/sq`): AD5 and AD7 have no data; AD202, 221, 241, 285, 314, 340, 384 are colon; AD043, AD218 and AD320 are the rest. AD350 has no cluster, Path I "BAC/MUCIN" | – |
| 9 | "The paper speaks of 12 suspected metastases: 12 flags carry a firm note, the other 4 are the three ?Br MET and AD218" | CC Label | Paper Methods; sheet | holds (count); which 12 the paper means is inference | The paper: "Other adenocarcinomas (n = 12) were suspected to be extrapulmonary metastases based on clinical history". The 12 firm-note flags are exactly the 11 flags staged M1 plus AD178. See issue Q1 | PROV-1 |
| 10 | AD368 quote: "albumin, transferrin… liver", "not identified as a metastasis"; AD320 is unflagged, in `CM`, and the random forest's top-ranked row | CC Known doubts | Paper; out-of-fold random forest (10 repeats of the shipped splits) | holds | Paper text verbatim. AD320 ranks 1 of 123 out of fold (0.425) | – |
| 11 | 123 rows, 15 positives (12%), 12,558 probe sets | task_summary row, predicted, known | `workbench` frame | holds | (123, 12559); 108 / 15; 12,558 genes plus 67 `AFFX` probes = 12,625 | – |
| 12 | One array per tumour: the first title in sorted order | CC 2026-11-10 | Listed the 47 patients with several arrays | holds | For example 157T1, 164T1a, 268T1, 347T1-1. The curated rows match the arrays of this selection by signal values | PROV-13 |
| 13 | Values are the MAS5 `Signal`, scaled on each array alone, linear scale | known; CC Values | File header; per-array 2% trimmed mean | holds | Column 4 of each file is `Signal`. The trimmed mean is 499.0 ± 0.3 on every array (MAS5 target 500), so no array depends on any other | LEAK-30 |
| 14 | Dataset A averages up to four arrays per patient (MAS4); OpenML 45093 is a copy | CC Source | DATASET A columns | partly holds | sample1-sample4 columns exist. MAS4 and the OpenML copy were not tested | PROV-6 |
| 15 | Not features: GEO age, sex, stage, pack-years and the sheet fields; the cluster holds 8 of 15 positives; GEO stage reads M1 for 11 of 15 flags | CC Not features | Columns of the frame; aligned GEO `diseasestaging` | holds | Only probe columns ship. 8 positives are in `CM` (7 colon + AD043). M1 is the stage of 11 flags (and of 4 primaries) | LEAK-1 |
| 16 | Task probe: 5 positives per test fold; no flag; RF 0.876, selected linear 0.851, LR 0.836, LightGBM 0.811, single feature 0.652; RF ahead of the class shares on every split | CC Size; warnings | `probes/task` JSON; fold counts on all 60 splits | holds | Matches exactly; `beats_dummy_share` 1.0; 5 positives in all 60 test folds of 41 rows | TP-2, TP-5 |
| 17 | Log loss: RF 0.289 against class shares 0.371; LR and LightGBM do not beat the shares | CC Metric | Probe JSON | holds | LR 0.493, LightGBM 0.590 | MET-8 |
| 18 | Ten unfitted pathology marker genes (CDX2, KRT20, CDH17, GATA3, TFF1, ESR1 against NKX2-1, NAPSA, SFTPC, SFTPB) score 0.819 | CC Size | GPL8300 annotation (`column_auditor/annot.csv`, 12,625 IDs); mean z-score difference on the 123 rows | **refuted (detail)** | NAPSA has no probe set on HG-U95Av2: 9 genes (10 non-lung + 5 lung probe sets). That score gives 0.817 (with max instead of mean, 0.781), so the number holds and the gene list does not | EV-1 |
| 19 | Out of fold: colon 0.984, breast 0.76, other 0.83 | CC Size; record | RF with 500 trees, 10 repeats of the shipped splits, averaged out of fold | partly holds | Colon 0.979, breast 0.752, **other 0.762** (3 rows, unstable); pooled 0.875, fold mean 0.887 | TP-2 |
| 20 | Share present lower in metastases (AUC 0.722, permutation p 0.01); noise floor 0.70; 18S rRNA 0.784 | CC Recording | Detection calls (genes only); median of absent-call signal; `AFFX-HUMRGE/M10098_*` | holds (±0.01) | Share present 0.710 (p 0.006); noise floor 0.697; 18S 5′/M/3′ probes 0.711 / 0.787 / 0.724 | EV-1 |
| 21 | Controls together 0.695 (p 0.02) | CC Recording | Model on the 67 `AFFX` only, shipped folds, 10 repeats | holds in direction, model-dependent | Logistic regression 0.736, RF 0.621 | – |
| 22 | Tumour content does not explain it (Spearman −0.20) | CC Recording | Spearman of max tumour % with share present | holds | −0.18 (p 0.05); median tumour % is 70 in both classes | – |
| 23 | Dropping the controls costs nothing (0.894 to 0.893); noise-floor subtraction leaves LR at 0.855-0.857; dropping AD218/224 moves no score (0.895 to 0.893) | CC Recording, CC AD218 | – | untested | Needs the pre-change frames; it does not bear on any decision | – |
| 24 | TabPFN 3.5 0.882, kNN 0.779 (127 rows) | CC Size | – | untested | Old row set; TabPFN runs on GPU only (house rule) | – |
| 25 | 6 IVT batches and 10 scan days hold 0-4 metastases each; batch- or day-grouped folds score like the random split (0.883-0.889 against 0.884) | splits_comment | Chip id → `IVT Batch` (PRIMARY DATASET); scan day from the chip id; GroupKFold(3), RF, 3 seeds | holds | Batches 1, 3, 4, 7, 8, 10 with 0-4 metastases; 10 days with 0-4. Grouped by batch 0.864-0.879, by day 0.871-0.904, random pooled 0.875 | SPLIT-1 |
| 26 | One tumour per patient, no grouping needed; NL268 is not a row; 5 folds would leave 3 | splits_comment | Titles; hidden-structure probe | holds | One array per patient; normal lung is excluded by histology; no near copies (`hidden.log`: 123 clusters of 1); 15/5 = 3 | SPLIT-1, PROV-7 |
| 27 | Scanned between 16 March and 17 April 2001 | CC Time basis | Chip ids of all 254 arrays | holds for the 123 rows; **refuted for the study** | The 123 arrays span 16 Mar to 17 Apr; the series has 4 arrays from 25 Apr | – |
| 28 | A 2001 study in Boston | task_summary row | Paper affiliations | holds | DFCI, Brigham and MGH in Boston (Whitehead in Cambridge) | – |
| 29 | Every row's flag is published in the same series | CC Values | Archive listing | holds | `SampleData.xls` is in `GSE83227_caArray_meyer-00191.tar.gz` | PROV-1 |
| 30 | `meta_license_unknown`: GEO gives no licence | warnings | NCBI disclaimer page (blocked by a browser check) | untested | NCBI's standard GEO disclaimer says it places no restrictions on use (from memory, not re-read) | SEL |
| 31 | Metric: fallback ROC AUC; "the source […] scores no classifier for it" | `metric`; CC Metric | Paper Methods and Results; `Metric.fallback(...).resolve('binary_classification')` | holds | Resolves to `roc_auc`. The paper builds a KNN classifier only to choose marker genes for the clustering subclasses (Methods, "Analysis of Marker Genes"); it reports no score for primary against metastasis | MET-1, MET-5, MET-11 |
| 32 | MET-2: computable on every fold | metric | `scorer` on a stand-in container, all 60 folds | holds | Constant prediction 0.5 on all 60 folds; random 0.524 on average; 5 positives and 36 negatives in every test fold; no scoring columns needed | MET-2 |
| 33 | Implied: every feature is known at the prediction point; no copy across the split | – | Leak probe; hidden probe | holds | No exact copies (0.0%). Nearest-neighbour distance alone gives AUC 0.746: metastases are transcriptome outliers, which is signal, not a leak | LEAK-1, PROV-7 |

**Refuted and untested claims, ranked (principles.md: validity first, Must first)**

1. **Q1, label validity (P3, USE-5; Weigh, for the curator). Not a refuted written claim, an implied one: that the 15 positives are one kind of label.**
   - **The finding.** In the clinic's own staging (DATASET A, the same as GEO's), 11 of the 15 flags are M1. The other four were staged as lung primaries: AD178 "(met)" T1N0Mx IA; AD163 "?Br MET" T2N1Mx IIB; AD172 "?Br MET" T2N1Mx IIB; AD186 "?Br MET" T1N0Mx IA.
   - **The paper's own count.** The paper counts 12 suspected metastases. By the definition's own mapping (claim 9), those 12 leave out AD172, AD186 and AD163. The paper separately supports AD163 (oestrogen receptor and mammaglobin, "consistent with breast metastasis"), but nothing supports AD172 or AD186.
   - **What the expression says.** Out of fold, AD172 ranks 108 of 123 and AD178 ranks 73; AD163 and AD186 rank 13 and 14. Breast's weak 0.75 rests mostly on AD172.
   - **The tension.** The definition drops AD218 and AD224 because questioned second-review notes are coded both ways. It keeps "?Br MET" positives, which are coded consistently but are just as uncertain and not counted by the paper. The curator decided all flags count (issue 8, A), so I do not override.
   - **Mildest remedy.** Write the fact in the Label bullet and the fit reason: "4 of the 15 (AD163, AD172, AD178, AD186) were staged as lung primaries (no M1); the paper's 12 suspected metastases appear to exclude two or three of them." The alternative is to ask the curator whether AD172 and AD186 belong with AD218 and AD224 as undetermined. That would leave 13 positives, 4-5 per test fold, below the current 5.
2. **Claim 18 (P6 note accuracy; EV-1).** "Ten pathology marker genes … NAPSA": NAPSA is not on the array. Fix: "nine marker genes (NAPSA has no probe set on HG-U95Av2), 15 probe sets, 0.82".
3. **Claim 19 (P6).** "Others at 0.83" does not reproduce: I get 0.762 on 3 rows. Fix: "the 3 others about 0.76-0.83 (3 rows, unstable)". Colon and breast hold.
4. **Claim 27 (writing).** The 254-array study runs to 25 April 2001. Fix: "the 123 arrays were scanned between 16 March and 17 April 2001".
5. **Claim 21 (writing).** The controls' 0.695 depends on the model (logistic regression 0.736, random forest 0.621). Fix: name the model, or write "about 0.6-0.74".
6. **Claim 31 (MET-11, wording).** The fallback reason holds. To head off a reviewer's objection, it could say that the paper's only classifier (KNN on signal-to-noise, for the subclasses' marker genes) is never scored on the metastasis call.
7. **Untested, low stakes:**
   - Claim 23 (the pre-change score deltas) needs the earlier frames, and no decision rests on it.
   - Claim 24 (TabPFN 3.5, kNN) is on the old 127 rows, and TabPFN runs on GPU only.
   - Claim 14 (MAS4 and the OpenML 45093 copy).
   - Claim 30 (the licence): the NCBI page was blocked. If the curator wants the warning reason firmer, it could cite NCBI's GEO disclaimer (no restrictions on use) once someone re-reads it.

</details>

<details><summary>Column audit</summary>

**Column audit: lung_adenocarcinoma_metastasis (PR #75), column auditor, 2026-11-11**

**Bottom line:** No column leaks, and the cleaning holds. One claim is wrong: "first piece, first hybridisation" does not describe 10 of the 123 rows, though correcting it moves no score. The definition also drops three clinical fields known at surgery and gives no reason. The class-dependent recording the record describes is real, and I measured its cause: metastasis arrays are dimmer, not noisier.

Everything was re-tested on the frame (`ds.df`, 123 x 12,559) and the raw GEO and caArray files. The dtype probe flagged 0 of 12,558 columns. Gene symbols come from GEO's GPL8300 annotation. Scripts and intermediate tables are in the run folder: `scripts/a1.py` to `a14.py`, `probe_auc.csv` (per-probe ROC AUC, the AUC after removing share present, and the gene), `array_qc.csv` and `array_qc_first.csv` (array header QC per array).

Unless a line says otherwise, model scores are mean fold ROC AUC on the shipped splits (10 repeats x 3 folds), on log2 values. LR is logistic regression with C=0.01; RF is a random forest with 300 trees.

**Column families and the columns that matter**

| Column / family | Meaning | Known at prediction? | Dtype and cleaning | Verdict | Rule |
|---|---|---|---|---|---|
| `Metastasis` (target) | DATASET B flag (`Colon Met`, `Breast`, `other met`): 15 positive (8 colon, 4 breast, 3 other), 108 primary | n/a | categorical, 2 string levels | fine | CLEAN-25 |
| All 12,558 probe sets | MAS5 `Signal` from the study's own per-array files | yes: measured on the resected tumour | float64; no NaN; minimum 0.2 (MAS5 gives no zeros or negatives); one decimal everywhere (number-format probe 0.491); no constant or duplicate columns. All 254 files share the same MAS5 settings (TGT=500, SFGene=All). | fine | CLEAN-2, CLEAN-5, CLEAN-9, LEAK-30 |
| 67 `AFFX` control probes | spike-ins, hybridisation controls, 18S rRNA, GAPDH/ACTB 3'/5' ratios, Alu | — | dropped: none remain, and 12,625 − 67 = 12,558 | fine | LEAK-15 |
| Intestinal / colorectal genes (higher in metastases) | MYB (`2042_s_at` 0.908, `1472_g_at`, `41854_at`), HES2 `36352_at` 0.904, GPA33 `37875_at`, CDX2 `170_at` (colon vs primary 0.994), CDH17 `40736_at`, SLC26A3 `928_at`, OLFM4, ASCL2 `31355_at`, FABP1, IHH, HSD11B2, PCK1, LY6G6D, CEACAM1 `988_at`, TSPAN8, PROX1, LEFTY1, EPHB2 `41678_at` (colon vs primary 0.92), KRT20 | yes | as above | fine: the expected biology of colon origin, the natural core of the task | — |
| Lung-lineage genes (higher in primaries) | NKX2-1 `130_s_at`/`33754_at` (0.22), SFTPB (0.27), AQP3 `39248_at` (0.155), WFDC2, LPCAT1, HOPX `39698_at`, MUC1 `700_s_at`, OSMR, TFPI, RAP1GAP, HIF1A `1039_s_at`, ASAH1 `36938_at` | yes | as above | fine: expected biology of lung origin | — |
| KLK1 `246_at` (0.833) | kallikrein 1 | yes | as above | fine. Higher in all three metastasis kinds (colon 0.87, breast 0.76, other 0.83). It is not a standard pathology marker, and I found nothing that ties it to the recording (rho with share present −0.26). | — |
| Breast markers | GATA3 `40511_at`, ESR1 (4 probes), TFF1 `31798_at`, SCGB2A2 `36329_at`, PIP | yes | as above | fine as columns. They do not separate the 4 breast-flagged tumours (breast vs primary: GATA3 0.46, ESR1 0.52 to 0.63, TFF1 0.20, SCGB2A2 0.59). Those 4 separate through MYB (0.88) and low lung markers (NKX2-1 0.19 to 0.25, SFTPB 0.17 to 0.20). This bears on the soft "?Br MET" label (for the label auditor). | — |
| Noise-floor probe sets | genes not expressed in lung tissue, whose signal is the array's scaled noise: KLK3 `1513_at` (0.706), SAG `31760_at` (0.720), DDN `37516_at`, MYO7A, LIPE, PRM2 `34658_at`, BAX `1998_i_at`. Spearman with share present −0.70 to −0.76. | yes, but they record the array, not the tumour | as above | recording, kept with the existing note (`Class-dependent Recording`). They cannot be removed without choosing columns by their correlation with the label. | LEAK-15 |
| 3,335 probe sets called absent on all 123 arrays | mostly noise, plus weak true expression (HES2 0.90, LY6G6D, CYP3A4, IDUA, LFNG) | yes | as above | keep. Alone they score LR 0.841. After removing scaling factor and share present inside the folds they still score 0.806 (breast 0.833). The family is not pure recording, and dropping it would be a filter of our own choosing. | LEAK-15, CLEAN-22 |
| Blood and platelet genes | PPBP `39208_i_at` 0.812 ("other" vs primary 0.95), HBB `32052_at` 0.61 | yes | as above | fine. Tissue composition of the specimen rather than its origin; plausible and small. | — |
| Housekeeping genes outside AFFX | GAPDH `35905_s_at` 0.62, `39482_at`; ACTB `32318_s_at` 0.59 | yes | as above | fine. Ordinary gene probes, mildly tied to share present. | — |
| Sex-linked genes | XIST `38446_at` (AUC 0.963 for female), RPS4Y1 `41214_at`, UTY, KDM5D, DDX3Y, EIF1AY | yes | as above | fine. They carry the patient's sex into the frame, so leaving GEO's `Sex` out removes nothing (see problem 1). | USE-6 |
| 399 probe sets without a gene symbol | ESTs | yes | as above | fine. 6 are strong, e.g. `32797_at` 0.80. | — |
| Left out: GEO `age`, `Sex`, `normalizedsmokinghistoryinpackyears` | clinical history | **yes** | not shipped | **question** (problem 1) | USE-6 |
| Left out: GEO `diseasestaging` | TNM stage | no: M1 is coded from the metastasis call (11 of 15 flags M1; 4 of 108 primaries) | not shipped | correctly left out | LEAK-10 |
| Left out: sheet `CLUSTERS/Expression Signature` | the study's clustering over all arrays | no: fit over all rows. `CM` holds 8 of 15 positives and 1 of 108 primaries. | not shipped | correctly left out | LEAK-27, LEAK-30 |
| Left out: sheet `Clinical Path w tumor size`, `Path I`, `PATH II` | pathology notes | they hold the label: "met" appears in 14 of 15 metastasis notes and 0 of 108 primary notes | not shipped | correctly left out. The tumour size inside them (metastases smaller, AUC 0.243 for size) is legitimate in principle. But it is missing exactly for the "MET COLON" notes, so a parsed size column would encode the label through its missingness. | LEAK-10, LEAK-35 |
| Left out: sheet `Comb. Differentiation`, `max_tumor%` | the study's pathology review | review made for the study | not shipped | fine either way: AUC 0.564 and 0.481 | — |
| Left out: `PRIMARY DATASET` sheet (`IVT Batch`, `proportion of Pcall`, `CEL Pixel Mean`, chip id); MAS5 `Detection` calls and p-values | the preparation and recording | describe the array, not the tumour | not shipped | correctly left out. The detection calls carry the class-dependent share present. | LEAK-15, LEAK-33 |

**Problems, ranked by principles.md**

1. **P3, USE-6 (Must; my call is that it is weighed here): clinical history known at the prediction point is left out without a reason.**
   - Age, sex and pack-years are in GEO for all 123 rows (pack-years for 121) and are known at surgery. The "Not features" bullet lists them next to real leaks (stage, cluster, notes) and says nothing about why they go.
   - **Evidence:**
     - Pack-years alone: AUC 0.326 (metastasis patients smoked less).
     - Age: 0.511.
     - Sex is already in the frame through XIST (0.963) and RPS4Y1.
     - The three together: LR 0.575, RF 0.567.
     - Adding them to the expression: LR 0.844 → 0.844, RF 0.879 → 0.884.
   - **Mildest remedy:** one sentence in the definition saying the task is the expression profile as a second opinion and that the three add nothing (cost measured). Alternatively, ship the three columns, which is cheap and safe.
   - This is a weighing call for the curator. I see no validity effect.

2. **P5, faithful data (the claim), with CLEAN-1 (follow the data owners' choice): "first piece, first hybridisation" is wrong for 10 rows.**
   - The definition takes GEO's first title in sorted order (`347T1-1` before `347T1-2`) and calls it the first hybridisation. The study's own files say otherwise for all 10 patients with `-1`/`-2` titles: AD131, AD183, AD255, AD301, AD338, AD340, AD341, AD346, AD347, AD350. Two of them, AD340 and AD350, are metastases.
   - **Evidence:**
     - In every one of the 10, the GEO `-1` chip has the higher study sample number (`PRIMARY DATASET`, `Sample ID`), i.e. the later preparation. Examples: AD131 picks A200 (IVT batch 8) over A15 (batch 1); AD183 picks A215 (batch 8) over A6 (batch 1); AD301 picks A265 (batch 10) over A237 (batch 8).
     - The study's Dataset A names the other chip as `Sample1` (`A#_sample1` mapped to the chip through `PRIMARY DATASET`). The shipped array is the study's `Sample1` for 113 of 123 patients.
     - For AD131, AD183 and AD301 the `Replication` sheet calls the two "T1" arrays different tumour pieces (`Tumor (T)` = d). AD131's pair agrees poorly (R² 0.641). So the title does not identify a "first piece" either.
   - **Effect, nil:**
     - Share present AUC: 0.710 as shipped, 0.714 with the study's `Sample1`.
     - Models: LR 0.844 → 0.833 and RF 0.879 → 0.870 with `Sample1` (10 repeats).
   - **Mildest remedy:** reword the comment (e.g. "the first title in GEO's sorted order; for 10 re-hybridised tumours this is the later preparation"). Or take the study's own `Sample1` for every patient, which is source-defined and needs a few lines reading DATASET A and PRIMARY DATASET from the archive.

3. **P4, LEAK-15 (kept with a note, as decided): the recording note names the wrong mechanism.**
   - The record says the metastasis arrays show "a higher noise floor (0.70)". The scanner-level QC in each file's header does not differ by class: Noise 0.475, RawQ 0.517, Background 0.481.
   - What differs is the MAS5 scaling factor: SF 0.621, Spearman −0.68 with share present. Metastasis arrays are dimmer, so the per-array scaling multiplies the same raw noise up. Noise × SF reaches 0.670; the 5th percentile of the scaled signal 0.672; share present 0.710. A logistic regression on the array QC (SF, share present, RawQ, Noise, Background) scores 0.667; share present alone 0.713.
   - The effect sits in the colon metastases: share present 0.787 for colon, 0.692 for breast, 0.528 for other.
   - After each gene is regressed on SF and share present inside the folds, LR goes from 0.844 to 0.800 (colon 0.961 → 0.914, breast 0.771 → 0.762). This removal also takes colon biology that correlates with share present, so 0.800 is a lower bound and the signal survives. The keep under LEAK-15 holds; I reproduce the record's share-present AUC (0.710 against 0.722).
   - **Remedy:** reword the note ("dimmer arrays, scaled up by MAS5: scaling factor 0.62, share present 0.71; scanner noise and background do not differ") and name the noise-floor probes (`1513_at`, `31760_at`) as where it shows.

**Judged and found to be the expert state (CLEAN)**

- **Per-array MAS5:** the right expert choice for single arrays from 2001. Every value depends only on its own array (scaling factor per array), so LEAK-29 and LEAK-30 hold. RMA or GCRMA would fit across all arrays, a transductive leak. To my knowledge there are no fRMA frozen vectors for HG-U95Av2. All 254 files carry identical algorithm settings, so processing does not differ by class.
- **Linear scale:** as deposited. A log2 transform is a per-row encoding the benchmark may apply (CLEAN-2), not a cleaning gap.
- **Detection calls not shipped:** correct. They are the channel of the recording artefact and are derived from the same measurement.
- **Controls:** dropping the 67 `AFFX` probes and keeping the non-AFFX GAPDH/ACTB gene probes is consistent. Those two are ordinary genes (0.59 to 0.62) and dropping them would be a choice by score. HG-U95Av2 has no other control probe sets outside `AFFX`.
- **One array per tumour:** a defensible use case (a lab profiles a specimen once) and closer to deployment than Dataset A's averages. Number of arrays per patient against class: AUC 0.546. Share present of the chosen versus the not-chosen replicates: 0.354 against 0.354. Only the wording is off (problem 2).

**What I tested that found nothing**

- **Dtype and types:** dtype probe, 0 flags; no proxy missing values, impossible values, reversed codes or identifier columns; no probe-set name encodes anything but the probe design (suffixes `_s_`, `_g_`, `_f_`, `_i_`, `_r_` are Affymetrix design classes).
- **Top leak-probe columns** (`2042_s_at` MYB, `41678_at` EPHB2, `246_at` KLK1, `1039_s_at` HIF1A, `36938_at` ASAH1, `1472_g_at` MYB, `170_at` CDX2, `700_s_at` MUC1): all known gene biology of colon origin (or lung origin, for those lower in metastases). None is a control or a recording channel, and their Spearman with share present is small (−0.11 for `2042_s_at`). Single-column AUC after removing share present: `2042_s_at` 0.901, `36352_at` 0.873. Of the 281 probe sets with |AUC − 0.5| > 0.25, 201 stay there after that removal.
- **Batch and scan:** metastases spread over 10 scan days (0 to 4 per day). Array QC alone is weaker than the genes.
- **Tumour content and differentiation** (sheet): AUC 0.481 and 0.564, so tumour purity does not drive the expression signal.
- **Sex and breast labels:** all 4 breast flags are female; 5 of 8 colon flags are male. No contradiction in the label.
- **Copies and identifiers:** no exact copies across the split (leak probe). No identifier, batch or recording column in the frame.

</details>

<details><summary>Split audit</summary>

**Split auditor: lung_adenocarcinoma_metastasis (PR #75)**

**Verdict: the split is right, with notes.** A random split over patients, stratified and 3-fold, matches the use case: one tumour of a new patient from the same study (SPLIT-1, SPLIT-2). I found no hidden group that carries the label (SPLIT-29 not triggered, SPLIT-30 no hit). Grouping the folds by IVT batch or by scan day does not lower the score. The weak point is not the regime but how much the score can tell apart (P6, TP-5). With 15 positives, the 20 repeats make method gaps look settled when the patients themselves do not settle them. A re-split cannot fix this. It is a note and a call for the curator.

**Validity:** SPLIT-1 holds (IID over patients, one row per patient: 123 unique patients). SPLIT-29 and SPLIT-30 are not triggered. SPLIT-24 also holds: the paper's expression clusters are similarity clusters, so they cannot be grouped on.
**Value:** TP-5 is borderline (5 positives per test fold, 15 in total). Note 1 below.
**Quality:** two notes on wording (notes 2 and 3).

---

**Note 1 (P6, TP-5; Must, borderline). With 15 positives, a method ranking is only partly resolved, and the repeats hide this.**

The repeats only reshuffle the same 15 metastases (TP-5; task_probes.md, "A grouped task": repeats add no evidence). I scored random forest (RF), extra trees, logistic regression (LR, log2 inputs, C 0.01) and kNN (k 10) on the 60 shipped splits:

| comparison | mean per-fold ROC AUC gap | repeats won by the first | naive SE over 60 folds | patient-bootstrap SE (1,000 draws) | bootstrap 95% CI | P(gap > 0) |
|---|---|---|---|---|---|---|
| RF vs LR | +0.036 | 20 of 20 | 0.007 | 0.028 | -0.014 to +0.094 | 0.90 |
| extra trees vs LR | +0.043 | 20 of 20 | 0.007 | 0.030 | -0.007 to +0.103 | 0.94 |
| RF vs kNN | +0.077 | 20 of 20 | 0.011 | 0.047 | -0.012 to +0.17 | 0.95 |
| LR vs kNN | +0.042 | 19 of 20 | 0.012 | 0.042 | -0.039 to +0.12 | 0.82 |
| RF vs extra trees | -0.007 | 9 of 20 | 0.004 | 0.006 | -0.020 to +0.004 | 0.13 |

- **Size of a single score.** The level of one method's mean score has a patient-bootstrap SE of 0.044 to 0.062. A single test fold's ROC AUC has an SD of 0.093 (RF, range 0.633 to 1.000).
- **What the repeats suggest vs what the data supports.** "RF wins 20 of 20 repeats" sounds decisive. Yet the patient-level uncertainty of the RF vs LR gap is about 4 times the naive fold SE, and the 95% interval includes 0. Only gaps of about 0.08 or more come out clearly. RF vs kNN and RF vs LR fall short of that.
- **The accepted warning `splits_test_minority_few` overstates.** It cites "the methods separate (RF 0.876 against LR 0.836)" as the reason to accept 5 positives per fold. My bootstrap does not support that gap as resolved.
- **3 folds vs 5 folds.** 3 folds is the house protocol (`definitions.md` line 474) and the better of the two here. Stratified 5-fold (10 repeats) leaves 3 positives per fold:

| folds | positives per test fold | RF per-fold ROC AUC SD | minimum | maximum | RF pooled | LR pooled |
|---|---|---|---|---|---|---|
| 5 | 3 | 0.134 | 0.437 | 1.000 | 0.885 | 0.845 |
| 3 (other seeds) | 5 | 0.089 | 0.683 | 1.000 | 0.879 | 0.851 |

- **Against the precedents.** 5 per fold sits between parkinsons (2 to 3 healthy people per fold, retired) and musk (13 per fold, kept). The curator decides whether 5 counts as "a handful" here.
- **Mildest remedy:** keep the split. Reword the accepted warning: the methods separate by 0.03 to 0.08 ROC AUC, but with 15 metastases a patient bootstrap puts the RF vs LR gap at -0.01 to +0.09, so only large gaps rank reliably. The record's `Size` CC should name the same limit. If the curator reads 5 per fold as a handful, the outcome is `Too Small` (TP-5). That is a dataset decision; the split cannot change it.

**Note 2 (P7, quality, no rule broken). A fold's score depends mostly on how many colon metastases land in it.**

The folds are stratified on the binary target, so a test fold holds 1 to 4 of the 8 colon cases:

| colon cases in the test fold | shipped folds | RF mean ROC AUC | LR mean ROC AUC |
|---|---|---|---|
| 1 | 6 | 0.775 | 0.718 |
| 2 | 18 | 0.827 | 0.789 |
| 3 | 26 | 0.918 | 0.891 |
| 4 | 10 | 0.949 | 0.911 |

- The colon count and RF's fold score correlate at Spearman 0.60 (p 4e-7). This confirms the record's own remark that the score rests on colon against lung.
- **Alternative tested:** folds stratified on the subtype (colon / breast / other / none; 20 repeats x 3 folds, 2 to 3 colon per fold). RF's per-fold SD falls from 0.093 to 0.074. The SD of the paired RF minus LR gap does not improve (0.065 against 0.051), and RF still wins 18 of 20 repeats.
- So subtype stratification would not sharpen the ranking. It would also need the subtype as a non-feature column in the frame, which is more than a split change.
- **Remedy:** none. At most, one line in the splits comment.

**Note 3 (P7, writing). The grouped-folds numbers in `splits_comment` reproduce in direction, not in value.**

The comment claims RF pooled ROC AUC 0.883 to 0.889 for grouped folds against 0.884 for the random split. My runs (RF with 500 trees on log2 inputs; stratified grouped 3-fold over 5 seeds, plus leave-one-group-out):

| scheme | RF pooled ROC AUC | LR pooled ROC AUC |
|---|---|---|
| shipped random 3-fold (20 repeats) | 0.872 (0.833 to 0.902) | 0.838 |
| random 3-fold, other seeds (10 repeats) | 0.879 | 0.851 |
| grouped by IVT batch, 3-fold | 0.881 (0.856 to 0.897) | 0.845 |
| grouped by scan day, 3-fold | 0.883 (0.868 to 0.903) | 0.828 |
| leave-one-IVT-batch-out | 0.878 | 0.853 |
| leave-one-scan-day-out | 0.881 | 0.841 |

- The conclusion holds: grouped folds score no lower than random ones.
- The specific values (0.884 random) depend on the seeds and the model setup, and the comment gives no split count. Per writing.md ("Say how many splits a number comes from"), it should give the count or a range.
- The comment's count claim checks out exactly:

| grouping | groups | metastases per group |
|---|---|---|
| IVT batch | 6 | 3, 4, 3, 0, 2, 3 |
| scan day | 10 | 1, 0, 2, 3, 1, 4, 2, 0, 0, 1 |

---

**What I tested that found nothing**

- **Regime.** The use case is a new patient's tumour from the same study. Each row is one patient's first array (123 unique patients), so there is no repeated entity and no grouping is needed.
- **Processing batches (IVT batch, scan day).** I joined each row to `SampleData.xls` PRIMARY DATASET through its chip id, taken from the GEO file name. Every row matched. Neither grouping carries the label (Note 3).
- **Hospital.** All 123 rows are `BRIGHAM/DFCI`; none of the 36 MGH arrays is a row. So no site group exists inside the data. The record's "Not tested: tumours from another hospital" is accurate and cannot be tested from these data.
- **OCT block.** 112 of 123 rows are `O1`; the positives sit in `O1`, `O1-3` and `O1-4`. No signal.
- **Operation type.** Wedge resections hold 1 of 16 positives, against 14 of 107 for other operations (Fisher p 0.69). This is not a group, and it is not a feature either.
- **Array brightness.** CEL pixel mean does not differ by class (Mann-Whitney p 0.23). The share of present calls does (p 0.01), but the record already covers that under `Class-dependent Recording`; it is not a split matter.
- **Near copies and duplicate patients.**
  - The nearest neighbour of each row (correlation of log2 values across patients) is r 0.774 to 0.941.
  - For comparison, 50 other arrays of the same patients (other pieces and replicates, not rows) correlate with that patient's row at r 0.793 to 0.965 (median 0.904).
  - The closest cross-patient pairs are all IVT-batch-4 primaries (patients 247, 255, 260, 261, 361). That is a batch effect with no label in it, not a duplicated patient.
  - The hidden-group probe agrees: 18 candidates, no hits, 0.0% near copies.
- **The paper's expression clusters.** `CM` holds 7 of the 8 colon cases. It is a similarity cluster built from the same expression values, so grouping on it is ruled out (SPLIT-24). It is the signal itself, not an entity.
- **Earlier-cancer site.** Not recorded for primaries, so it cannot be a group key. Grouping by metastasis subtype would turn the task into "a new organ of origin", which is not the use case.
- **Time basis ("Timeless").**
  - The chip ids confirm scans from 2001-03-16 to 2001-04-17 (10 scan days).
  - There are no resection dates. As an accrual-order proxy (an unverified assumption), I sorted by study patient number into 3 contiguous blocks. The blocks hold 8, 2 and 5 metastases. RF per-fold ROC AUC is 0.873 to 1.000 (mean 0.929); pooled across blocks it is 0.829. The pooled drop comes from calibration shifting between blocks, not from lost ranking. Patient number does not differ by class (Mann-Whitney p 0.48).
  - So nothing argues for a temporal split, and "Timeless" holds for this study. A new lab or a new era is out of scope, as the record says.

**For other panellists:** `ds.df`'s row order is not the order `_clean` builds (the workbench reorders rows). I aligned the metadata to `ds.df` by matching identical feature vectors; every row matched exactly once.

</details>

<details><summary>Domain practitioner</summary>

**Domain practitioner: lung_adenocarcinoma_metastasis (PR #75)**

I answer as the thoracic pathologist in the definition's `use_case`. I read the definition, the record, `lung_cancer.md` (its retirement CC, line 79), `use_case.md` and `metrics.md` in the PR worktree. I also re-read the annotation sheet (`SampleData.xls`, DATASET B) straight from the caArray archive, and searched the literature on current practice. I did not run any model; every score I quote is the record's. Nothing in REPO was edited.

**Verdict: the fit is approximate, at its weak end. It is not none, and it is not direct.** A real decision exists: in a patient with an earlier cancer, is this lung adenocarcinoma a new primary or a metastasis? A model on these arrays can only stand in for one tool that is sometimes used for it, a molecular tissue-of-origin assay. The negative class is also defined so that it mostly leaves out the patients in whom the question arises.

**What I re-checked in the sheet**
- The sheet itself labels the negatives "Adenocarcinoma w/ no history or path indicating non adeno" (DATASET B, row 160), and the positives "possible mets" (row 158). So a negative is, by the source's own definition, a patient with no recorded history of another cancer. The dataset's `fit_reason` says only that "which primaries had one is not recorded". The sheet says more than that: the negatives were picked out because there was no such history.
- Each of the 15 flags comes from the hospital's own sign-out, the "Clinical Path" column ("ad c/w colon met", "MET COLON", "ad 3.0 m BAC (?Br MET)", "ad poor (met)"). The record also notes that GEO's stage reads M1 for 11 of the 15. The label is therefore the call the pathologist I play already made, with the history and the slide in hand. It is not an origin confirmed later. Three of the four breast flags are question marks ("?Br MET").

**1. Would I have these inputs when I decide?**
| Input | Do I have it? |
|---|---|
| Whole-transcriptome array (HG-U95Av2) of snap-frozen resected tumour | **No.** Routine sign-out works on FFPE H&E plus an IHC panel. In lung adenocarcinoma, a targeted NGS panel (EGFR/KRAS/ALK and others) is now also run for treatment. Expression-based tissue-of-origin tests do exist: the Pathwork Tissue of Origin test (microarray, 15 tissues, FDA-cleared with limits) and CancerTYPE ID (92-gene RT-PCR). They are niche, I order them only for cases where IHC leaves the origin unclear, and they run on FFPE, not frozen tissue. |
| The earlier cancer: its site, its histology, the interval since, the old slides and blocks | **Always**, and it is my strongest input. The disease-free interval is the most consistent discriminator in resected nodules after breast cancer (Zhao 2022). The dataset does not record it (USE-6: a known input is a legitimate input; leaving it out changes the task). |
| IHC: TTF-1/NKX2-1, napsin A vs CDX2, CK20, SATB2, CDH17 (colon), GATA3, ER, mammaglobin (breast) | Always. The arrays carry the mRNA of these markers. The record's ten unfitted marker genes reach ROC AUC 0.819, which shows how much of the task is the IHC panel read off an array. |
| Comparison with the earlier tumour (morphology, shared driver mutations) | Often, and it is the strongest test today. In 24 patients with a prior malignancy, targeted sequencing matched every metastasis to its earlier cancer and none of the new primaries (the prior-cancer study cited below). |

**2. Is the target what I act on?** It is a proxy (USE-5).
- What I act on is the **true origin**. It decides stage IV disease and systemic therapy for the old cancer, versus staging and surgery for a new lung primary.
- The label is my own colleague's hedged sign-out, written from the same history the dataset leaves out. A model that learns it imitates the sign-out without the history. Histology alone also misses intrapulmonary metastases often: sequencing disagreed with the prospective histologic call in 22% of tumour pairs, and in 44% of those predicted to be metastases (Clin Cancer Res 2019).
- Since the label is not read from the slide alone, this is not the pure cross-check that retired `lung_cancer`'s histology (USE-1). It still sits close to that line, as the USE-1 case table already says. For the 8 colon flags, CDX2/SATB2 against TTF-1/napsin usually settle the question at the microscope. Those are exactly the rows the model gets right (out-of-fold ROC AUC 0.984).
- What I would want out is a probability that this is a metastasis of the known earlier cancer. That is a binary question conditioned on a known site, not "metastasis from any organ".

**3. Does one row match one decision? Is the test data what I would face?**
- **The row matches**: one resected tumour per patient, one decision.
- **The test data does not.** I would face patients with a known earlier cancer, and in them the share of metastases is far higher than 12%. Resected solitary nodules after breast cancer run roughly 70% primary to 30% metastasis in the largest series (Zhao 2022), 23% to 57% metastasis in smaller ones. My hard negatives are new lung primaries in patients who had breast or colon cancer. By the sheet's definition those are essentially missing here.
- The test rows also come from the same centre, frozen tissue, 2001 arrays and one laboratory. I would see FFPE tissue from my own lab. The `Selection Bias` marker is right, and under USE-8 the selection is not one my setting shares, so the fit is approximate.

**4. Would I use this model?**
- **Not as shipped.** It needs an assay I do not run on frozen tissue I do not keep.
- Its skill sits where I need no help: colon against lung, 0.984. Breast against lung reaches only 0.76, and "other" 0.83, and those are the hard calls.
- It cannot take in the one input I always have, the earlier cancer.
- I would trust a tool tested on IHC-ambiguous cases in patients with a documented prior cancer, with the origin confirmed by clonality testing or by the clinical course. I would also want it validated on FFPE and in another lab.
- I would distrust the class-dependent recording the record keeps (fewer probe sets present on the metastasis arrays, ROC AUC 0.722). A transcriptome with weaker RNA can look "non-lung" for reasons unrelated to origin.

**Is there a real decision (USE-1, USE-2, USE-8, USE-9)?**
- **USE-1/USE-2:** Yes. The source names it ("a key issue in lung tumor diagnosis"), and it is real in daily thoracic pathology. The task is not none.
- **USE-9:** The closest well-defined use case the data mirrors is a tissue-of-origin expression classifier asked one question: "lung or not?". That is a real, if niche and contested, practice. The 2014 NCCN panel did not recommend gene-expression profiling as standard management for occult primary: it saw a diagnostic benefit but no proven clinical one. Payers still call these tests investigational. That use case still needs the hard negatives, so it does not lift the fit to direct.
- **USE-8:** approximate, for three named gaps (ranked below).

**Gaps, ranked by how much they change the task**
1. **The negative class is defined by the absence of history** (sheet row 160). The real contrast, a new primary against a metastasis in a patient with a prior cancer, is mostly absent. The task becomes "lung adenocarcinoma against colon/breast adenocarcinoma in general", which is easier and leans on the textbook markers. This is larger than the current `fit_reason` says.
2. **The label is the sign-out, not the confirmed origin.** It is hedged ("?Br MET"), and it was written with the history the model lacks. 3 of 4 breast flags are uncertain, and AD320 and AD368 are doubts the source raises itself.
3. **The earlier cancer is missing as an input**, though I always have it, and it is the strongest predictor along with the interval since.
4. **The assay does not match practice**: a frozen-tissue whole-transcriptome microarray of 2001, against FFPE IHC and NGS today. The splits test one lab and one platform only.
5. **The mix of positives**: 8 of 15 are colon, the subgroup that IHC already settles. The headline score rests on that easy part (record: 0.984 colon, 0.76 breast).

**What an expert would change**
- Restate `fit_reason` to quote the sheet's definition of the negatives ("no history or path indicating non adeno"). Say that the hard negatives are absent, not just unrecorded. Keep fit approximate and `Selection Bias`.
- Name the subgroup split in the notes: colon flags are about half the positives and the IHC-easy part. Readers should know the benchmark mostly ranks how well a model recovers CDX2/CDH17/TTF-1-type signal from an array.
- Name the actor more exactly in `use_case`: an expression tissue-of-origin assay as a second opinion when IHC is inconclusive (USE-9). Today's work-up is IHC, comparison with the earlier tumour, and comparative sequencing. The prediction-point CC already says IHC; add the comparative NGS.
- No re-labelling: the record rightly keeps the source's flags.
- Better data would be resected lung nodules in patients with a documented prior cancer, with the origin confirmed by clonality or follow-up, on FFPE. I know of no public release of that, and it would be another dataset.

**Metric: partly scores the decision. I would keep ROC AUC.**
- ROC AUC is the binary fallback (MET-8). It ranks tumours by how likely they are to be metastases, which is how a second-opinion assay is judged (sensitivity and specificity across thresholds).
- **Keep ROC AUC:** it does not depend on the class prior (Provost et al. 1998, cited under MET-8). The dataset's 12% metastasis share differs sharply from the clinic's 30% to 60% after an earlier cancer, so a calibrated probability learned here would not carry over to my setting.
- **Against log loss:** a strictly proper rule (log loss or Brier) is what my decision ultimately needs (MET-8), since I combine a probability with my prior from the history. But it would score calibration to the wrong prior. With 5 positives per test fold it is also noisy: the record says logistic regression and LightGBM do not beat the class shares on it (MET-10, resolution).
- **No threshold metric:** the source fixes no threshold or cost, so MET-6/MET-7 give nothing to declare.
- **Against AUPRC:** a minority class alone does not justify it (MET-9), and I do not act only on the top of a ranking.
- **Why only "partly":** the declared score is dominated by the colon contrast I do not need help with. A subgroup score on breast and "other" against lung would score my decision better, but 7 positives across 3 folds cannot carry it. Name this in the notes rather than change the metric (MET-1: the metric should score the decision, and here it scores mostly the easy half of it).

**Sources**
- Bhattacharjee et al. 2001, PNAS 98:13790 (https://www.pnas.org/doi/10.1073/pnas.191502998); GEO GSE83227 caArray `SampleData.xls`, DATASET B (re-read for this report: the "Clinical Path" notes and the wording of rows 158 and 160).
- Zhao et al. 2022, resected solitary nodules after breast cancer, J Cardiothorac Surg: https://cardiothoracicsurgery.biomedcentral.com/counter/pdf/10.1186/s13019-022-01898-4 ; further series: https://spandidos-publications.com/10.3892/mco.2012.21 , https://wjso.biomedcentral.com/articles/10.1186/1477-7819-9-124 , https://www.ncbi.nlm.nih.gov/pmc/articles/PMC9206257/
- IHC markers for lung against GI and breast: Virchows Archiv 2023 (https://link.springer.com/article/10.1007/s00428-023-03583-w), TTF-1 and napsin A (https://link.springer.com/10.1186/s40169-015-0057-2), https://pmc.ncbi.nlm.nih.gov/articles/PMC2480532 , https://pmc.ncbi.nlm.nih.gov/articles/PMC7700753
- Comparative sequencing against histology: Clin Cancer Res 2019 (https://pmc.ncbi.nlm.nih.gov/articles/PMC7713586); prior-malignancy deep sequencing (https://doi.org/10.2147/OTT.S309155); https://www.ncbi.nlm.nih.gov/pmc/articles/PMC11462925/ ; https://doaj.org/article/8af76ad3cb0d45d3a925396e89448950
- Tissue-of-origin expression tests and the NCCN position: NCCN Occult Primary v3.2014 (https://vivo.weill.cornell.edu/display/pubid24994917), payer policies (https://www.southcarolinablues.com/web/public/brands/medicalpolicy/external/external-policies/molecular-profiling-for-cancers-of-unknown-primary-origin , https://cms.radmd.com/sites/default/files/2025-04/Cancer%20of%20Unknown%20Primary%20Gene%20Expression%20Profiling%20Tests_2025.2.pdf), https://pmc.ncbi.nlm.nih.gov/articles/PMC2823680
- Rules cited: USE-1, USE-2, USE-5, USE-6, USE-8, USE-9; MET-1, MET-6, MET-7, MET-8, MET-9, MET-10 (REPO `.claude/skills/knowledge-curation/references/`).

</details>

<details><summary>Blind review</summary>

**Verdict: exclude.** The data is real and cleanly extracted. But there are only 15 positives, they mix several kinds of tumour, about a third of them are only suspected metastases, and there are 12,558 expression features for 123 rows. That makes any method ranking mostly noise.

**What the task is.** The rows are 123 resected "lung adenocarcinomas" from Bhattacharjee et al., PNAS 2001 (GEO GSE83227, Affymetrix HG_U95Av2 arrays processed with Affymetrix's standard MAS5 algorithm). The features are MAS5 expression signals for 12,558 probes. The target separates true primary lung tumours (108) from tumours that were metastases from another organ (15).

The use is real: a pathologist or oncologist deciding, at diagnosis, whether a lung adenocarcinoma is a primary (lung-cancer staging and treatment) or a metastasis (look for and treat the original cancer). The paper's own claim is the "ability to discriminate primary lung adenocarcinomas from metastases of extra-pulmonary origin". In practice, today's routine stains (immunohistochemistry: TTF-1, CDX2, CK7/CK20) plus the patient's history settle this. 2001 microarrays are a historical setting.

**What I verified on the data and the source (no problem found)**
- **Labels match the source.** I downloaded the study's `SampleData.xls` (sheet DATASET B) and all 178 per-array MAS5 files for adenocarcinoma specimens from GEO. Each of the 123 rows matches exactly one GEO array: 100% of probe values agree within 0.05.
- **No duplicates across folds.** The 123 rows are 123 distinct specimens. No specimen appears twice, even though the study has technical replicates (for example 172T2/172T4 and 384T1/384T2); only one array per specimen was kept.
- **Correlation would not have caught replicates.** Replicate pairs correlate only 0.84–0.90 on log2 values. That is below the typical nearest-neighbour correlation between different patients (median 0.889, max 0.937). So matching the raw arrays was the only way to check, and it came out clean.
- **The 15 positives are exactly the specimens the sheet flags as metastases, minus AD218.** AD218 was dropped, along with primaries AD224, AD355 and AD360. AD218 and AD224 carry "met?" in the second pathology reading, and AD355/AD360 have no clinical pathology entry. Dropping them is sensible but not documented in `task.md`.
- **Values are plausible MAS5 signals.** One decimal place, min 0.2, no negatives or missing values, and per-array trimmed means of 596 ± 7 (consistent with standard MAS5 scaling).
- **No leak columns.** There are no Affymetrix control probes (AFFX-*) and no clinical columns. All specimens come from one site (Brigham/DFCI). The metastases are spread over 5 of the 6 lab processing batches (IVT batches 1, 3, 4, 8, 10), so batch does not encode the label.

**Concerns, most serious first**

1. **The positive class is a mix of tumour types and partly uncertain.** By the sheet, the 15 positives are:
   - 8 colon metastases ("c/w colon met", "MET COLON");
   - 4 breast, three of them written as "?Br MET" (AD172, AD186, AD163);
   - 3 "other", annotated only "(met)" (AD157, AD043, AD178).

   The sheet itself labels this group "possible mets" (16). I matched rows to specimens and computed out-of-fold scores from an L2 logistic regression (averaged over 10 repeats of 3-fold CV):
   - 7 of the 8 colon cases rank in the top 9 of 123.
   - The suspected breast cases rank 15, 20 and 75.
   - AD178 ("ad 1.9 w BAC (met)", placed in a primary-tumour expression cluster, C3) ranks 120 of 123.

   So much of the positive class looks like primaries, and part of the measured error is label noise.

   Change: either redefine the target as colon metastasis vs primary (but 8 positives is far too few), or make it multi-class by origin (too few per class). Neither rescues the size, hence exclude.

2. **Too small to rank methods.** With 15 positives, a 3-fold test fold holds 5 positives. Over 20×3 folds, logistic-regression AUC has mean 0.863, SD 0.103 and range 0.64–1.00. Log-loss is 0.305 against 0.371 for the prior. Differences between methods will be within fold noise.

   Change: none can fix this. If kept at all, use leave-one-out or many repeats and report confidence intervals.

3. **Extremely wide (p ≫ n).** There are 12,558 features for 123 rows. The benchmark mostly tests feature selection and regularisation, plus whether a method copes with 12.5k columns at all, not tabular learning in general. The raw MAS5 scale is skewed (column max up to 131,483, median about 239). Methods without a log transform are handicapped, which is a preprocessing artefact rather than real method skill.

   Change: if kept, log2 the values (floored at about 10) and consider pre-filtering low-expressed probes (26 probes are below 20 in more than 90% of arrays). Also flag the dataset as genomics / high-dimensional.

4. **There is signal, but it is narrow.** Single probes reach AUC 0.91 (`2042_s_at`) and 0.90 (`36352_at`). Logistic regression gets about 0.85–0.86 and LightGBM about 0.83. The task is not trivial, but performance is driven by the colon-metastasis subgroup (see concern 1).

5. **Documentation gaps.**
   - `task.md` does not say that labels are pathologist suspicion ("c/w", "?") rather than confirmed origin.
   - It does not say that 4 specimens were dropped, or that one replicate array was picked per specimen.
   - GEO's own per-sample metadata calls every one of these "Lung Adenocarcinoma"; the metastasis label exists only in the supplementary spreadsheet.

**Split.** IID stratified CV is acceptable here: one row per patient, one site, one array type. A grouped split is not needed because replicates are already excluded.

**What I could not check**
- Which of the two (or more) replicate arrays was chosen per specimen, or why.
- Whether the "metastasis" flags were ever confirmed by follow-up. The sheet gives none; the PNAS full text returned 403, so I relied on the GEO/caArray summary and the spreadsheet.
- The 13 adenocarcinoma specimens listed in the sheet (140) that have no numeric-titled GEO array (127). They are not in the data either way.
- I did not look up the gene behind the top probes.

</details>

<details><summary>Task gamer</summary>

I could not find a usable exploit in this task. No attack beat the honest logistic regression by more than the noise between repeats. The one real concern is how the label was made: some of the metastasis flags were assigned from the same expression arrays the model learns from, which flatters every model a little.

The hand-back tool was blocked by the sandbox, so this report comes as my final message. Paths below are relative to the kit the run folder.

**Scoring note.** `score()` takes the class-probability columns in sorted class order, and the first class is `metastasis from another organ`. If you pass `predict_proba` with y coded as 1 = metastasis, the AUC comes out mirrored: about 0.18 instead of 0.82. All numbers below use the correct order, built in `work/common.py`.

**Honest baselines** (60 splits; every test fold holds exactly 5 of the 15 positives)
- Untuned LightGBM on the raw features: 0.819 (0.45–1.00). `work/baseline.py`
- Logistic regression, log2 values, standardised, C=0.01: 0.846 (0.61–1.00). Same script.
- Better honest model: the same regression on log2(clip at 20), keeping only genes with SD above 0.5 (a label-free filter): 0.856 (0.64–1.00). `work/transductive.py`
- Noise: adding a random column to LightGBM moved it by −0.0007. Across the 20 repeats the regression's mean has SD 0.026 (SE 0.006); LightGBM's has SD 0.052.

| # | Exploit | Script | Honest score | Exploited score | Gain (paired per repeat) | A deployed model has it? | Fix |
|---|---|---|---|---|---|---|---|
| 1 | Hierarchical clusters fitted on train+test rows (k=8), scored by the training positive rate | `work/transductive.py` | 0.856 | 0.865 | +0.009; k=4 gives −0.06, k=16 −0.01, k=32 +0.001 | No (needs the test rows) | None needed: k was picked after the fact, the gain is within noise |
| 2 | Standardising over train+test rows | `work/transductive.py` | 0.856 | 0.856 | +0.0006 (sd 0.003) | No | None needed |
| 3 | Blend with a model on last-digit shares (format only) | `work/digits.py` | 0.856 | 0.856 | +0.0004 | Yes, but meaningless | None needed |
| 4 | Self-training on the test rows | `work/transductive.py` | 0.856 | 0.854 | −0.002 (sd 0.010) | No | None needed |
| 5 | Blend with array-level scale proxies (quantiles, low-value share) | `work/quality.py` | 0.846 | 0.823 / 0.792 / 0.751 (blend weight 0.2 / 0.35 / 0.5) | −0.02 to −0.10 | Yes | None needed |

**Findings**
- **Array scale and quality.** On their own, a few array-level numbers track the label: the 1st-percentile log signal (AUC 0.66), the share of values below 20 (0.32, inverted), and the median (0.63). This matches the published sheet: the metastasis arrays have fewer "present" calls (0.39 vs 0.43) and a lower mean CEL intensity (305 vs 395), so they were dimmer arrays with larger scaling factors. As a model this gets 0.58 to 0.67 and makes the honest model worse when blended in. Ranking genes within each array (which removes array scale) gives 0.848, the same as the honest regression's 0.846. The signal is already absorbed by the honest model.
- **Last digit (format).** Values are MAS5 signals with one decimal. The share of each tenths digit per array varies only as much as chance predicts (observed SD 0.0026–0.0030 against a binomial 0.0027), so there is no recording artefact. A model on digit shares alone scores 0.662 against a shuffled-label baseline of 0.476 ± 0.081 (best of 40 shuffles: 0.633). That is borderline at best, after picking C from three values, and adds nothing when blended (`work/digits_perm.py`).
- **Copies across the split.** There are no exact duplicates. The highest raw R² between any two rows is 0.916. Re-scans of the same tumour in the study's replicate sheet reach 0.95–0.99, so no same-specimen copies are in the kit. Different pieces of the same tumour (R² 0.86–0.97) cannot be fully ruled out by correlation alone, but the top pairs are all primary–primary, so they could not leak the positive class. 9 of the 15 positives have another positive as nearest neighbour; they correlate with each other at about 0.88. That is the colon-metastasis expression signature, which is real signal. Nearest-neighbour label: 0.64. Best training-positive correlation minus best training-negative correlation: 0.858, which is an honest model. `work/nn.py`, `work/explore.py`.

**Flaw that affects every model: the label is partly derived from the features.** The paper (PMC61120) says the colon-metastasis cluster was found by hierarchical clustering of these same arrays. Of the 10 cluster members with clinical history, "only seven samples had been previously diagnosed as metastases". In the study's sheet (DATASET B), AD218 is flagged "other met" while its pathology entry reads only "ad 5.0 m BAC", and it sits in that cluster. AD172, AD163 and AD186 are flagged on "?Br MET" (probable breast metastasis). So one to a few positives were probably labelled from the expression profile rather than from the clinic. That raises every model's AUC and is not something a participant can exploit. I could not measure the size without matching kit rows to sample IDs. Mildest fix: keep as positives only samples with a metastasis diagnosed from clinical history or pathology (the "c/w colon met", "MET COLON" and M1 cases). Drop, or mark unresolved, positives that rest only on cluster membership or a "?" note.

**Attacks that found nothing**
- Row order: AUC of the row index 0.498. Positives sit at rows 9 to 121 with no pattern, while the source sheet lists them at the end.
- Format: no negatives, no zeros, all values one decimal, whole-number share AUC 0.476. The trimmed mean is 498–500 for every array (the MAS5 target), so it carries nothing. The 67 AFFX control probes have already been removed.
- Missing values: none. In the source, the rows with missing age, sex or stage contain no metastases. The kit's 123 rows look like the 139 adenocarcinomas minus those, keeping 15 of the 16 flagged positives; no label-dependent filtering is visible.
- Test-set composition: the folds are stratified at exactly 5 positives each, which a ranking metric cannot use.
- PCA fitted on all rows: 0.803 (−0.053). Difference from class centroids on the top 1% of genes: 0.833.

**Looking up the published annotation:** not verified. The labels are in SampleData.xls, but matching kit rows to sample IDs needs the 750 MB per-array archive (not downloaded), and GEO's per-sample listings and pages were blocked (403 / captcha). Matching would almost certainly work.

**What I could not check:** scan date and IVT batch for each kit row. Batch 7 has 0 of 13 metastases in the source, which needs the row-to-array mapping. Also which of a specimen's replicate arrays the kit kept, and whether that choice depended on the label.

Downloaded sources are in `work/src/` (SampleData.xls, the paper's PMC page, the series matrix).

Sources: [GEO GSE83227](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE83227), [caArray tarball with SampleData.xls](https://ftp.ncbi.nlm.nih.gov/geo/series/GSE83nnn/GSE83227/suppl/GSE83227_caArray_meyer-00191.tar.gz), [Bhattacharjee et al. 2001, PMC61120](https://pmc.ncbi.nlm.nih.gov/articles/PMC61120/), [PNAS](https://www.pnas.org/doi/10.1073/pnas.191502998), [Golub lab page](https://golublab.broadinstitute.org/publications/classification-human-lung-carcinomas-mrna-expression-profiling-reveals)

</details>

<details><summary>Precedent check</summary>

**Precedent check: lung_adenocarcinoma_metastasis (PR #75), 2026-11-11**

Rules were read from REPO (`df-pr75`, commit 3218bd9d). I tested three things myself:
- **The panel's task probe** (`PANEL/probes/task/lung_adenocarcinoma_metastasis.json`): 5 metastases in the smallest test fold, no flags, random forest 0.876, logistic regression 0.836, LightGBM 0.811. The random forest's skill over the shared dummy runs from 0.36 to 1.00 across the 30 splits. Best minus worst is 0.129 with a paired SE of 0.041.
- **The study's annotation sheet** (`SampleData.xls`, DATASET B): every adenocarcinoma whose notes mention a metastasis or a "?".
- **The siblings' records and the Cases tables.**

Of the register's flags, only two are relevant here: USE-8's 16 keeps against 1 exclude, and the `few_minority` keeps. The `exception_to_must USE-1` flag is lt_vehicle_loan_default_prediction and has nothing to do with this PR.

**Summary:** most decisions follow their precedents. Two depart with a reason that covers only part of the precedent: the use case against lung_cancer's retirement, and the size against parkinsons. One departs from the wording of a Must: LEAK-15, the kept recording difference. Two process points sit in the PR itself. The USE-1 text is an amendment with no date or curator, and lung_cancer's own CC calls it "not a rule change". PROV-14 is cited where PROV-7 carries the decision.

**Precedents**

| # | Precedent (date, curator) | Its decision | This case | Verdict |
|---|---|---|---|---|
| 1 | lung_cancer histology (2026-11-10, Andrej), [lung_cancer.md](lung_cancer.md) | retired, `No Good Target`. Two grounds: (i) the slide settles the label on resected tumours; (ii) "a pathologist in doubt orders a two-stain panel, not an expression array", and the hard cases are missing, so "the test labels come from the easy cases only" | ships the metastasis flag from the same pathology notes. Ground (i) is answered: the call "rests on an earlier cancer outside the specimen". Ground (ii) is not, and the definition concedes it: "In practice the work-up is immunohistochemistry and comparison with the earlier tumour; an expression array is not used today". The score "rests mostly on colon against lung" (0.984), which a CDX2/CK20 against TTF-1 stain panel settles | **departs, reason covers ground (i) only** (prompt A) |
| 1 | glioma_grading_clinical_and_mutation_features (2026-10-26, Lennart) | retired: the grade is the pathologist's diagnosis, made before the DNA is sequenced, so only a cross-check is left | the metastasis call was also written in the pathology note at resection, before the 2001 arrays were run on banked tissue. "Settled before the features are taken" holds in time; it fails only on certainty | departs, same as above (prompt A) |
| 1 | ljubljana_primary_tumor (2026-10-27, Lennart; USE-1 case 2026-11-11, Andrej) | kept, fit approximate: the site comes from a separate work-up that found the primary | the flag is "possible", and no confirming work-up is recorded. The definition rests on the same-specimen branch of USE-1, not on this one | does not carry this case |
| 1 | tcga_hnsc_tumor_vs_normal_rnaseq (screening `No`, AI, 2026-10-31); tcga_lung_histology (AI, 2026-11-10/11) | same-specimen labels need no prediction (USE-2); tcga_lung_histology is left for the same question | the PR's own USE-1 text puts this case on the other side of the line | consistent with the amended text, which is the question |
| 1 | USE-1 as amended in this PR | adds "a label read from the same specimen … and settled before they are taken … fits no decision; a label found by a separate work-up is ground truth", plus this dataset as a third kind of case | no date or curator in the rule body (principles.md, "Exceptions and amendments" asks for both). lung_cancer's CC of 2026-11-10 says "Not a rule change". The label here fits neither branch (not a separate work-up, not settled), so the sentence works as an exception written into a Must | **process departure** (prompt A, option d) |
| 1, 3 | early_stage_diabetes_risk_prediction (PR #58, 2026-11-11, Lennart) | retired under USE-2 / fit None: no decision is made from these features. Once the actor holds the inputs, they act on them. A selection alone never makes the fit None | the actor's deciding inputs are the earlier cancer, which "the pathologist always has" and the data lacks, and immunostains. The array measures the stained genes (ten marker genes, unfitted, 0.819). This differs from diabetes, where the symptoms trigger the blood test themselves. It still asks whether any decision waits on an expression prediction (prompt A) | bears on 1; not a separate departure |
| 2 | parkinsons_biomedical_voice_measurements (2026-10-05, Lennart), TP-5 | `Too Small`: 8 healthy in total, 2-3 per fold; "ranks less stable than on 98% of BeyondArena" | 15 positives in total, 5 per fold; probe has no flags | between the two; see prompt B |
| 2 | musk (2026-10-06), TP-5 | kept: 13 musk per fold, about 39 in total | 5 per fold, 15 in total: under half of musk's counts, nearer parkinsons | see prompt B |
| 2 | heart_disease_switzerland (`No`, `Too Small`); labor (`TBD -> 2nd Tier`, 4 per fold) | out or held back at 2-4 per fold | 5 per fold. The `few_minority` probe flags below 5, so this sits exactly on the line | see prompt B |
| 2 | ljubljana_primary_tumor, sarcoma, forensic_glass (2026-10-12, Lennart), TP-8 | kept: one rare class of a multiclass task "that does not decide the score" | binary: the minority class is the whole score. These cases do not carry over | not a precedent for this case |
| 2 | `splits_test_minority_few` accepted | no other definition in the working copy accepts this warning | first acceptance | new precedent; record it in the Cases table |
| 3 | ljubljana_primary_tumor, eryhemato_squamous_disease, superconductivity (2026-10-27, Lennart), USE-8 | `Selection Bias`, fit approximate: the setting does not share the selection | resected adenocarcinomas stand in for patients with an earlier cancer elsewhere; approximate, marker kept | **consistent** |
| 3 | differentiated_thyroid_cancer_recurrence (2026-10-21, Lennart), USE-8 | an unverified label definition makes the fit approximate | "possible mets", named in `fit_reason` | **consistent** |
| 4 | gallstone_disease (kept), LEAK-15 / LEAK-39 / LEAK-40 | kept: the suspected artefacts left do not carry the score (with and without the feature, 0.826 / 0.827) | kept: the share of probe sets present differs by class (0.722) and "runs through every gene and cannot be removed". Subtracting each array's noise floor leaves logistic regression at 0.855 to 0.857 | consistent with the outcome. **Departs from LEAK-15's wording**, which retires an artefact that "runs through several features … that cannot be undone" (prompt C) |
| 4 | prostate_cancer_detection (2026-09-30, Lennart), LEAK-15 | retired: the artefact runs through the whole spectrum, and same-label groups separate (Benign against NED 0.99) | cause open (biology or RNA quality). Batch, scan day and tumour content do not explain it. No same-label-group test is reported | differs on the deciding fact, but the same-label test is missing (prompt C) |
| 4 | lung_cancer control probes (2026-11-05 kept; 2026-11-10 repaired) | spike-ins separated the classes; rebuilt per array | the 67 control probes dropped (0.695 together) | **consistent** (LEAK-13 / LEAK-14 kind fix) |
| 5 | aeolus to aeolus_rebuilt (2026-10-26, Lennart); corporate_credit_rating to corporate_issuer_credit_rating (2026-10-16); coad_colon_adenocarcinoma to tcga_coad_molecular_subtype (2026-10-16, before PROV-14's amendment of 2026-10-21) | a new record for a rebuild from other sources | the GEO deposit is the same study's origin, so the rebuild alone was a repair and stayed under lung_cancer (2026-11-10, correctly). The new record follows from the new target and rows | **consistent outcome**. The fitting rule is PROV-7 (one source, two tasks: parkinsons / telemonitoring), not PROV-14's rebuild branch. aeolus is a loose analogue. Re-word the PROV-14 case row; no prompt needed |
| 6 | glioma, gallstone_disease, heart_disease, ljubljana_breast_cancer, early_stage_diabetes (MET-1, MET-5, MET-6, MET-11) | `roc_auc` fallback when the source scores no classifier | `roc_auc` fallback; the paper scores no classifier | **consistent** |
| 7 | no rule on label doubts. Closest: lung_cancer's 12 `A` patients (no clinical data, so "no flag is no finding"); differentiated_thyroid (unverified label, fit approximate) | — | AD218 and AD224 dropped. In the sheet, a metastasis query only in `PATH II` occurs for exactly these two ("ad w met?" flagged, "ad m met?" unflagged). The three "?Br MET" are in the clinical note and stay positive. AD320 and AD368 kept as coded | **consistent** with the definition's own stated line, checked on the sheet. A first case: worth a CLEAN or USE Cases row |
| 8 | CLEAN-22 / coad (2026-10-15, Lennart); sarcoma 201 × 25,910, lung_cancer_epithelial_genexp 187 × 22,215, pancreatic_cancer_mouse_detection 181 × 6,771 (all shipped); colon_tumor 62 rows `No` (Lennart, early, "too small for CV") | width is no reason to drop | 123 × 12,558, the smallest row count of the shipped omics sets | **consistent** on width; size falls under 2 |
| 8 | gcm_multiclass_cancer (screening 2nd Tier, partly because "covered by a larger recorded cohort"); expo_tumor_tissue_of_origin (2,158 tumours, `TBD -> Yes`); tcga_pancancer_tumor_type | tissue of origin from expression, use case "commercial tissue-of-origin tests", fit approximate (AI screenings, not curator calls) | same kind of task on 123 rows | not a departure. These records support option (a) of prompt A and show a much larger source for the same question |

**Drift and third exceptions.**
- **Andrej, size.** On 2026-11-10 he called the size "too few to rank methods"; on 2026-11-11 he kept it. A reversal with a stated reason (the probes run), not drift.
- **Andrej, use case.** On 2026-11-10 he wrote "not a rule change"; on 2026-11-11 he added USE-1 text. An unstated reversal: see prompt A (d).
- **Third exception.** None of the same kind found.

---

**A. Does a decision wait on an expression call for this label, when lung_cancer was retired because a doubting pathologist "orders a two-stain panel, not an expression array"?**

**Consistency question (2026-11-11):** your call on lung_adenocarcinoma_metastasis (ship, fit approximate) differs from lung_cancer (retired 2026-11-10, Andrej) and glioma_grading_clinical_and_mutation_features (retired 2026-10-26, Lennart). The same arrays, the same resected tumours and the same kind of label are involved: a call written in the pathology note before the arrays were run. What sets it apart?
(a) <the AI's best guess, below>, recorded as an exception; (b) treat it like lung_cancer; (c) reopen lung_cancer to match; (d) change the rule (an amendment).

**Problem:**
- lung_cancer was retired on two grounds. The record answers the first: the slide does not settle a metastasis. It does not answer the second, the actor's tool is immunostaining, and the definition itself says "an expression array is not used today".
- lung_cancer's "the test labels come from the easy cases only" has a parallel here: colon metastases score 0.984 and carry most of the score, and a CDX2/CK20 stain panel separates them.
- The amended USE-1 has two branches: same specimen and settled, or a separate work-up. This label fits neither. The PR adds the case as a third kind, inside a Must rule, with no date or curator, while lung_cancer's CC says "Not a rule change".
- PR #58's reasoning applies in part: the input the pathologist always acts on, the earlier cancer, is not in the data.

| Option | Pro | Con |
|---|---|---|
| (a) Exception, with this fact: expression-based tissue-of-origin assays are in clinical use for exactly this doubt, unlike histology typing of a resection. The definition's "not used today" sentence is corrected to say so | names a fact lung_cancer lacks; matches the use case of the expo_tumor_tissue_of_origin and tcga_pancancer_tumor_type screenings | the AI's guess from general knowledge (such tests exist, mostly for cancers of unknown primary); not yet sourced in the record; those tests address an unknown primary, not a known earlier cancer |
| (b) Retire like lung_cancer | one rule for one set of arrays | drops the task the source names ("a key issue in lung tumor diagnosis") |
| (c) Reopen lung_cancer | — | its ground (i) still holds; nothing argues for it |
| (d) Amend USE-1 deliberately, with date, curator and the case: a label whose call rests on information outside the specimen is a prediction target, even when written in the specimen's note | makes the line a rule change on purpose | widens USE-1 for all pathology-note labels; glioma and tcga_lung_histology need re-reading |

**Suggested:** (a), once the fact is sourced in the record; otherwise (d). In either case, give the USE-1 text a date and curator, and correct the "not a rule change" line.

[^a]: USE-1, USE-2, USE-8 (Must, P3); principles.md "Exceptions and amendments", "Consistent judgement".

---

**B. Are 15 positives, 5 per test fold, a tiny-data task like musk or a handful like parkinsons?**

**Consistency question (2026-11-11):** your call (keep) sits between parkinsons (retired 2026-10-05: 8 in total, 2-3 per fold) and musk (kept 2026-10-06: 13 per fold, about 39 in total). heart_disease_switzerland (2-3 per fold, `No`) and labor (4 per fold, 2nd Tier) lean the other way. What sets it apart?
(a) <the AI's best guess, below>, recorded as a TP-5 case; (b) treat it like parkinsons (`Too Small`); (c) reopen parkinsons; (d) amend TP-5 with a per-fold floor.

**Problem:**
- The stated reason is "no flag". But `few_minority` flags below 5, and this dataset has exactly 5, so the flag cannot tell.
- Parkinsons was retired on rank stability, which is not reported here. What is reported is that the model beats the class shares on 30 of 30 splits and the mean scores of the methods.
- Per split, the best model's skill runs from 0.36 to 1.00. The best and worst methods differ by 0.129, with a paired SE of 0.041. The random forest leads logistic regression by 0.04, and no paired SE is given for that pair.
- In total, 15 positives is nearer parkinsons' 8 than musk's 39.

| Option | Pro | Con |
|---|---|---|
| (a) Keep, recording the fact: the methods separate beyond the per-split noise. This needs a rank-stability or paired test of each pair of methods on the shipped folds, as parkinsons was judged | judges by parkinsons' own criterion | needs one more run |
| (b) `Too Small` | follows parkinsons and heart_disease_switzerland | drops a task with a clear signal |
| (d) Amend TP-5 with a floor | one rule for the next borderline case | a floor without evidence |

**Suggested:** (a): run the rank-stability check before shipping, and record the first `splits_test_minority_few` acceptance in the TP-5 Cases table.

[^b]: TP-5 (Must, P6); principles.md Tensions, "Tiny but real".

---

**C. Does LEAK-15, a Must, allow keeping a class difference that "runs through every gene and cannot be removed"?**

**Consistency question (2026-11-11):** your call (keep) matches gallstone_disease's outcome (the artefact does not carry the score). LEAK-15's text retires an artefact that runs through features that matter and cannot be undone, as for prostate_cancer_detection. What sets it apart?
(a) <the AI's best guess, below>, written as the reading of LEAK-15; (b) treat it like prostate (retire); (d) amend LEAK-15.

**Problem:**
- The record says the difference cannot be removed, which is LEAK-15's retire condition.
- Prostate turned on same-label groups separating. No such test is reported here: for example, whether the share present separates the colon, breast and other metastases, or primaries by batch.
- The cause is open: it may be the metastases' own transcriptome, which would be signal, not recording.
- The record cites a Must without an exception, and a Must allows none.

| Option | Pro | Con |
|---|---|---|
| (a) Reading: not shown to be a recording artefact (batch, scan day and tumour content ruled out; the cause may be biological), and removing its first-order effect, the noise floor, moves no score. So LEAK-15's retire clause is not triggered. Add a same-label-group test | keeps the Must intact; uses prostate's own test | one more test |
| (b) Retire | the rule's literal text | the evidence says the difference does not carry the score |
| (d) Amend LEAK-15: an artefact through every feature is kept when removing its effect moves no score | settles the next omics case | widens a Must on one case |

**Suggested:** (a), with the same-label test, and a LEAK-15 row in the Cases table at `leak_checks.md` line 516 (the PR adds the case only inline).

[^c]: LEAK-15 (Must, P4); LEAK-13, LEAK-39; the marker paragraph of `leak_checks.md`.

---

</details>

<details><summary>Advocate</summary>

**Advocate's opening brief: lung_adenocarcinoma_metastasis (PR #75), 2026-11-11**

**Position: ship after small changes.** No panellist found a leak, a wrong label row, a copy across the split or a fold that cannot be scored. The open questions are about the use case (P3) and the size (P6). Both are weighing calls with evidence on the keep side. The confirmed errors are all in the wording, and none of them moves a score.

```text
Verdict: ship after changes.
Validity: USE-1/USE-2 hold (approximate fit, a decision the slide cannot settle); USE-5 approximate, soft label named;
USE-6 triggered, fixed by adding age, sex and pack-years (or a stated reason); LEAK-1/10/27/30 hold; LEAK-15 not
triggered (artefact removable, does not carry the score); SPLIT-1 holds; PROV-1/13 hold.
Value: TP-2 real signal; TP-5 at the line (5 per fold), every fold scorable (MET-2); MET fallback roc_auc consistent.
Quality: wording fixes (target words CLEAN-25, NAPSA, "first hybridisation", noise-floor mechanism, warning text).
For the curator: issue A (USE-1 line vs lung_cancer), issue B (TP-5: is 5 per fold a handful?).
```

**1. A real decision exists, and this label is a prediction, not a cross-check (P3; USE-1 and USE-2, Must). This answers the lung_cancer precedent.**
- **Claim.** lung_cancer was retired because "the slide settles it on resected tumours". A metastasis call is not settled by the slide. It rests on an earlier cancer outside the specimen.
- **Evidence.**
  - The source names the task: "A key issue in lung tumor diagnosis is the discrimination of a primary lung adenocarcinoma from a distant metastasis" (claim auditor, claim 5: verbatim).
  - The domain practitioner, as the actor, judged the fit "approximate, at its weak end. It is not none, and it is not direct", and found the decision "real in daily thoracic pathology".
  - USE-2 retires a label that "stands in for what the features already measure". Here the label depends on the clinical history, which is not in the features.
- **lung_cancer's second ground.** That ground was "a pathologist in doubt orders a two-stain panel, not an expression array". The practitioner names expression tissue-of-origin assays that are in clinical use for this doubt: Pathwork Tissue of Origin (FDA-cleared, microarray) and CancerTYPE ID. They are niche and contested, but real. This is the distinguishing fact the precedent checker asked for (prompt A, option a), and it is now sourced.
- **Concede.**
  - The fit is approximate, not direct.
  - The negatives were selected as "no history or path indicating non adeno" (sheet row 160), so the hard negatives are missing. `fit_reason` understates this.
  - The definition's sentence "an expression array is not used today" is wrong as written.
  - The USE-1 amendment in the PR has no date or curator. lung_cancer's CC still says "not a rule change".
- **Mildest remedies.**
  - Quote the sheet's definition of the negatives in `fit_reason`.
  - Replace "not used today" with "expression tissue-of-origin assays exist as a second opinion when IHC is inconclusive; routine work-up is IHC, comparison with the earlier tumour and comparative sequencing".
  - Date and sign the USE-1 text, and correct the lung_cancer line.
- **Why this outranks the exclude.** USE-2 excludes only when no decision fits, and the actor says one does. An approximate fit with named gaps is the remedy USE-8 prescribes. Exclusion is the last rung of the remedy ladder.

**2. The label sits on the right arrays, and its soft part works against the models, not for them (P3; USE-5, Must, approximate allowed with a note).**
- **Evidence.**
  - The claim auditor matched every row to its GEO array by signal values. The 15 positives are exactly the 15 remaining sheet flags.
  - 15 of 15 come from the hospital's clinical pathology note ("MET COLON", "c/w colon met", "?Br MET", "(met)").
- **The task gamer's "label partly derived from the features".** The one flag that may follow the expression clustering is AD218: flagged only by the second review, and in `CM`. It is already dropped, together with AD224, which carries the same note and is coded the other way. The flaw it describes is fixed in the definition.
- **The 4 positives staged as primaries (AD163, AD172, AD178, AD186).** Out of fold, AD172 ranks 108 of 123 and AD178 ranks 73. Noisy positives lower AUC, so they do not "flatter every model".
- **Why the "?Br MET" flags stay.** They are written in the clinical sign-out and coded consistently, unlike AD218 and AD224. The curator decided that all flags count (issue 8, A).
- **Concede.** The label is the hospital's hedged call, not a confirmed origin.
- **Fix.** The claim auditor's sentence in the Label bullet: "4 of the 15 were staged as lung primaries (no M1); the paper's 12 suspected metastases appear to exclude two or three of them."

**3. Evaluation is honest: no leak column, no copy, and the split mirrors the use case (P4; LEAK-1, LEAK-10, LEAK-27, LEAK-30, SPLIT-1, all Must).**
- **Evidence.**
  - The leak probe finds 0% copies. The hidden-group probe finds 123 clusters of 1.
  - Every column that holds the label is correctly left out: stage (M1 for 11 of 15), the expression cluster (8 of 15 positives, LEAK-27), and the pathology notes ("met" in 14 of 15).
  - MAS5 is computed per array (trimmed mean 499 ± 0.3), so no test array depends on a training array (LEAK-30). RMA would have broken this.
  - One array per patient and one site.
  - Folds grouped by IVT batch or scan day score as the random folds do: RF pooled 0.878 to 0.883, against 0.872 to 0.879 random (split auditor).
- **Why it matters.** "Honest evaluation" is the precondition for every other point, and all three auditors found it holds.

**4. The recording difference is real but removable, and it does not carry the score, so LEAK-15's retire clause is not triggered (P4; LEAK-15, Must).**
- **My own test** (`PANEL/advocate/samelabel.py`).
  - Among primaries only, the share of probe sets called present differs by IVT batch (Kruskal-Wallis p 0.016; the most different pair of batches separate at AUC 0.78) and by scan day (p 0.002).
  - So I concede there is a recording component, not only biology.
- **Why LEAK-15 still does not retire the dataset.** LEAK-15 retires an artefact that runs through features that matter and "cannot be undone". Here it is a per-array scale: the MAS5 scaling factor, metastasis arrays dimmer, Spearman −0.68 with share present (column auditor). A label-free per-array transform removes it:
  - Ranking genes within each array gives logistic regression 0.848, against 0.846 honest (task gamer).
  - Regressing every gene on scaling factor and share present inside the folds leaves 0.800. That is a lower bound, since it also removes colon biology.
  - Of the 281 strong probe sets, 201 stay strong. The top ones are MYB, CDX2, HES2 and EPHB2, which are colon biology.
  - The array-level proxies alone score 0.58 to 0.71, and blending them in lowers the score (task gamer).
- **The prostate precedent is the reverse case.** There, the artefact features separated same-label groups at 0.92 to 0.97 and the label at only 0.62 to 0.70. The artefact was the signal. Here the label signal (0.85 to 0.90) far exceeds the artefact's.
- **Fixes.**
  - Correct the mechanism in the note: "dimmer arrays scaled up by MAS5, scaling factor AUC 0.62; scanner noise and background do not differ". Name `1513_at` and `31760_at` as where it shows.
  - Record the reading of LEAK-15 as a Cases row, including this same-label result.

**5. The task is real and every fold is scorable. Its size sits at the TP-5 line, not under it (P6; TP-2 Should, TP-5 Must, MET-2 Must).**
- **Evidence.**
  - Every one of the 60 test folds holds 5 metastases and 36 primaries, so every fold can be scored (MET-2).
  - The level of one method's score has a patient-bootstrap SE of 0.044 to 0.062, around a mean of 0.84 to 0.88. That is far above chance (TP-2).
  - TP-5's own example of `Too Small` is parkinsons: 8 in total, 2 to 3 per fold. This dataset has about twice that per fold, and the probe's `few_minority` threshold is under 5.
  - 3 folds is the house protocol and the better choice here: per-fold SD 0.089 with 3 folds, against 0.134 with 5 folds.
- **Concede.**
  - With 15 positives, only gaps of about 0.08 or more between methods resolve. RF against LR (95% CI −0.014 to +0.094) is not resolved, and RF against kNN is borderline (P 0.95).
  - The accepted warning's "the methods separate (0.876 against 0.836)" overstates. It should give the split auditor's bootstrap figures.
  - This is the first acceptance of `splits_test_minority_few` and should get a TP-5 Cases row.
  - Under "independent failures are not conflicts", P3 cannot rescue a TP-5 failure. My case rests on 5 per fold not being "a handful", and that is the curator's call (prompt B).
- **Width is not an argument.** The blind reviewer's p ≫ n and log-scale points are settled by the Tensions row "width is no reason to drop" (coad; CLEAN-22). A log transform is a per-row encoding left to the method (CLEAN-2).

**6. Clinical inputs known at surgery belong in the features (P3; USE-6, Must). The fix is cheap and changes nothing else.**
- **Evidence.**
  - Age, sex and pack-years are in GEO for all 123 rows (pack-years for 121) and are known at surgery.
  - Sex is already in the frame through XIST (0.963).
  - Adding the three to the expression moves RF from 0.879 to 0.884, and LR stays at 0.844 (column auditor).
- **Concede.** As written, the "Not features" bullet lists them next to real leaks and gives no reason. That is a USE-6 gap.
- **Mildest compliant fix.** Ship the three columns, which is cheap and safe. Otherwise, state why the task is the expression profile alone. I lean to shipping them, because USE-6 is a Must.

**7. The remaining findings are wording, each with an undisputed fix (P5/P7; CLEAN-25 Should, EV-1, writing.md).**
- **Target words (CLEAN-25).** The definition builds the labels itself, so use "No" / "Yes" with "Yes" (the event) sorting second. Today a participant who passes P(metastasis) as the second column gets a mirrored AUC (0.18).
- **Marker genes.** Nine genes, not ten: NAPSA has no probe set on HG-U95Av2. The score holds (0.817).
- **"First piece, first hybridisation".** This is wrong for 10 patients. Say "the first title in GEO's sorted order". Using the study's `Sample1` instead moves no score (RF 0.879 to 0.870, LR 0.844 to 0.833).
- **Small corrections to the notes.**
  - "Other" out-of-fold AUC: give 0.76 to 0.83 (3 rows).
  - Scan dates: write "the 123 arrays" scanned 16 March to 17 April 2001 (the study ran to 25 April).
  - Controls: name the model behind 0.695.
  - Grouped-fold numbers in `splits_comment`: give split counts or ranges.
  - Cite PROV-7, not PROV-14, for the new record.
- **Why these do not touch the verdict.** None changes data, splits or the metric. Under step 3 of "How to decide", quality problems are fixed when cheap and safe.

**Rebuttal**


**Advocate's rebuttal: lung_adenocarcinoma_metastasis (PR #75), 2026-11-11**

**Overall.** I concede six of the critic's seven points in substance; most were already conceded in my opening. I dispute two inferences:
- **Point 1:** that refusing the amendment makes this lung_cancer's case.
- **Point 7:** that the Kendall's W of 0.22 "leans towards parkinsons".

**New fact (flagged for a second round).** Kendall's W over these 4 methods cannot tell a small task from a well-sized one. A well-sized dataset gives about the same W (point 7). It is the only new fact.

**Point 1, the USE-1 amendment and lung_cancer's two grounds: process conceded; "amend or `No`" disputed.**
- **Conceded.** The new USE-1 text needs a date, a curator and its case, as principles.md's "Exceptions and amendments" requires. lung_cancer's "not a rule change" line must be corrected. The definition's "an expression array is not used today" must be replaced by the tissue-of-origin assays (Pathwork, CancerTYPE ID), with the actor stated as a second opinion when IHC is inconclusive.
- **Disputed: the claim that without the amendment the case is lung_cancer's.** `git diff origin/main...HEAD` on `use_case.md` shows the PR added the whole same-specimen sentence. Before the PR, USE-1 said nothing about labels read from the specimen, and USE-2 nothing about stand-in labels. lung_cancer and glioma are therefore precedents, not rule text. principles.md ("Conflicts between rules") says a precedent is followed "unless a fact sets the new case apart".
- **The two facts that set this case apart.**
  - The call rests on the earlier cancer, which is outside the specimen and outside the features. Glioma's grade and lung_cancer's histology are defined by the slide.
  - Expression tissue-of-origin assays are a sourced tool for exactly this doubt (domain practitioner). That answers lung_cancer's second ground ("orders a two-stain panel"), which the critic says is unanswered.
- **Glioma's ground "in time".** "The label was written before the arrays" holds for every retrospective series of resolved cases. That is how such a task can be built at all, as the PR's own text says.
- **What follows.**
  - The curator chooses between (a) a dated amendment and (b) a recorded distinguishing fact against the lung_cancer and glioma precedents.
  - `No` follows only if the curator finds the facts do not set the case apart.
  - The colon part of the score is the IHC-easy part. That makes the fit approximate (USE-8), not None.

**Point 2, the negatives exclude the hard cases: conceded in full.**
The sheet defines the negatives as "no history or path indicating non adeno". Rewrite `fit_reason` and the Selection bullet to quote that definition and say the hard negatives are absent. Keep the fit approximate and the `Selection Bias` marker. This was my point 1 too.

**Point 3, the line drawn through the positives: the note conceded; "inconsistent" disputed.**
- **Conceded.** The four positives staged as lung primaries (AD163, AD172, AD178, AD186) go into the Label bullet and `fit_reason`. The curator should see the trade: 13 positives, 4-5 per test fold.
- **Disputed: that the line is inconsistent.** The line is drawn on the sheet's coding, not on certainty.
  - AD218 and AD224 carry the same `PATH II` note, and the sheet codes it both ways. Dropping both takes no side.
  - The three "?Br MET" are in the hospital's clinical sign-out and are coded positive every time (claim auditor, claims 2 and 3).
  - Relabelling AD172 and AD186 because the paper's count "appears to" leave them out rests on inference (the claim auditor marks it so). Evidence ranks inference last (EV-2).
- **Disputed: the effect.** Noisy positives (AD172 ranked 108, AD178 ranked 73 out of fold) lower the AUC. They cannot inflate it. This is a cost to resolution, already counted in point 7, not a validity failure under USE-5.
- **What follows.** A note now. The relabelling is the curator's question, at the cost the critic names.

**Point 4, USE-6: conceded.**
Ship age, sex and pack-years; the cost is nil (RF 0.879 to 0.884). Or state that the task is the expression profile alone. Same as my point 6.

**Point 5, LEAK-15: conceded.**
We agree on the substance: the artefact does not carry the score. My same-label test adds that share present varies by batch among primaries (pairwise AUC up to 0.78), so it is partly recording. A per-array rank removes it at no cost (0.848 against 0.846), so it can be undone.

The note gets the scaling-factor mechanism and the within-array-rank result. The LEAK-15 Cases row records this reading, with the same-label test.

**Point 6, the claims and the target words: conceded in full.**
Same list as my point 7. Add the rewrite of the accepted warning, which should cite the bootstrap interval (−0.014 to +0.094) instead of "the methods separate".

**Point 7, TP-5: remedy conceded; the evidential weight of W 0.22 disputed with a test.**
- **My test** (`PANEL/advocate/kendall_ref.py`, on `split_auditor/stability_fold_auc.csv`):

| data | methods | Kendall's W |
|---|---|---|
| this dataset | RF, ET, LR, kNN | 0.220 (reproduces the critic) |
| this dataset | RF, LR, kNN | 0.165 |
| this dataset | RF, ET | 0.010 |
| this dataset, method scores permuted within each fold (2,000 draws) | 4 methods | 95th percentile 0.041 |
| sklearn breast_cancer (569 rows, about 71 positives per test fold), 20×3 stratified folds | the same 4 | **0.302** |
| sklearn breast_cancer | RF, LR, kNN | **0.134** |

- **Reading.**
  - W on these 4 methods depends mostly on which methods are near-tied. RF against ET gives 0.01.
  - A dataset with 14 times the positives per fold gives about the same W: 0.30 for 4 methods, 0.13 for 3.
  - So the number cannot place this dataset next to parkinsons. Parkinsons' 0.18 is a percentile over BeyondArena's 37 configurations, not a raw number.
  - TP-1's own guidance agrees: W "is low on small folds even when the mean ranking is stable".
  - What W 0.22 does show is agreement well above chance (null 95th percentile 0.04).
  - Caveat: the breast_cancer methods sit near the AUC ceiling, so this is a sensitivity check, not a calibrated reference.
- **Conceded.**
  - Only gaps of about 0.08 or more resolve.
  - "No flag" decides nothing at exactly 5 per fold.
  - The critic's remedy is the right test: parkinsons' own criterion, W over the BeyondArena configuration set on the shipped folds, placed in BeyondArena's distribution. Its result decides keep or `Too Small`, and it is re-run if point 3 drops two positives.
  - Under "independent failures are not conflicts", nothing in P3 rescues a TP-5 failure.
- **What follows.** Ship is conditional on that run, not on the critic's W, which neither condemns nor clears the dataset.

**Where we stand.**
- **Agreed changes:** points 2, 4, 5 and 6, plus the dated USE-1 text or a recorded distinguishing fact, and the four staged-as-primary positives named in the notes.
- **For the curator:**
  - (A) amendment or distinguishing fact against lung_cancer and glioma. In my view either one keeps the dataset.
  - (B) AD172 and AD186.
  - (C) TP-5, decided by the BeyondArena W percentile.

</details>

<details><summary>Critic</summary>

**Critic, opening brief: lung_adenocarcinoma_metastasis (PR #75), 2026-11-11**

**Verdict argued: do not ship as defined.** Ship only after the changes below. Two points could end at `No`, and the curator has to answer them deliberately: point 1 (the use case rests on an amendment with no date or curator) and point 7 (TP-5, size). The other five are changes to the definition or notes.

**Conceded up front (tested by the panel; I found nothing to dispute):**
- The label provenance holds against `SampleData.xls`, and the rows are matched to their arrays.
- There is no leak column and no exploit (task gamer, leak and hidden probes).
- Per-array MAS5 is the expert choice. Dropping the 67 `AFFX` probes is right.
- The random stratified 3-fold split matches the use case. Grouping by batch or scan day changes nothing.
- The ROC AUC fallback is right (MET-8, MET-11).
- Width is no argument (CLEAN-22).

**1. The use case ships on an undated amendment of a Must, and on half of lung_cancer's reasons (P3, USE-1 and USE-2, Must).**
- **Problem.** This PR rewrites USE-1 to add a branch: a label "read from the specimen's pathology but not settled there". The rewrite has no date, no curator and no case line in the rule body, which principles.md ("Exceptions and amendments") requires. A Must has no exceptions, so this is an amendment or nothing. lung_cancer's own CC of 2026-11-10 says "not a rule change" (precedent checker, rows 1 and 1d).
- **Only one of lung_cancer's two grounds is answered.** The second ground was "a pathologist in doubt orders a two-stain panel, not an expression array". The definition concedes it word for word: "an expression array is not used today". Glioma's ground (a cross-check of a sign-out already written) also applies in time: the label is the hospital's own sign-out, written before the 2001 arrays were run.
- **Effect.** The benchmark mostly scores how well a model recovers the immunostain panel from an array. Ten unfitted marker genes score 0.82, and colon against lung scores 0.98: the part CDX2/TTF-1 settles at the microscope (domain practitioner; column auditor).
- **The fact that could set the case apart is missing.** Expression tissue-of-origin assays exist (Pathwork, CancerTYPE ID; domain practitioner, USE-9). The definition says the opposite of this.
- **Remedy (definition and rule text, not exclusion by me).** The curator makes the USE-1 text a dated amendment (curator and case named) and runs `decision_register.py --rule USE-1` on glioma and tcga_lung_histology. The use case is rewritten to name the actor's real tool: an expression tissue-of-origin test as a second opinion when IHC is inconclusive. The "not used today" sentence goes. If the curator will not amend USE-1, the case is lung_cancer's, and the outcome is `No`.

**2. The negatives exclude the hard cases by construction; the fit reason says only "not recorded" (P3, USE-8 Must, USE-5).**
- **Problem.** The sheet defines the negative class as "Adenocarcinoma w/ no history or path indicating non adeno" (DATASET B, row 160; domain practitioner, claim auditor claim 1). So the negatives were chosen because the patient had no recorded earlier cancer. The deciding contrast is a new primary in a patient with an earlier cancer, and it is essentially absent.
- **The fit reason understates this.** It says "which primaries had one is not recorded".
- **Effect.** The task becomes lung adenocarcinoma against colon or breast adenocarcinoma in general. That is easier than the real decision, and it leans on textbook markers.
- **Remedy (a note).** Rewrite `fit_reason` and the Selection bullet to quote the sheet's definition of the negatives and say that the hard negatives are excluded. Keep the fit approximate and the `Selection Bias` marker.

**3. The positives are drawn on an inconsistent line (P3, USE-5, Must).**
- **Problem.** AD218 and AD224 are dropped because a questioned note ("met?") is coded both ways. The three "?Br MET" positives (AD163, AD172, AD186) stay, though they are just as uncertain.
- **What the source and the clinic say.** The clinic's own stage gives 4 of the 15 positives no M1: AD163, AD172, AD178 and AD186 were staged as lung primaries. The paper's count of 12 suspected metastases appears to leave out two or three of the "?Br MET" cases (claim auditor Q1; inference, flagged as such).
- **What the expression says.** Out of fold, AD172 ranks 108 of 123 and AD178 ranks 73 (73 under the random forest, 120 under the blind reviewer's logistic regression). Breast's 0.75 rests mostly on AD172.
- **Effect.** Part of the measured error is label noise in the minority class that decides the score.
- **Remedy (mildest).** Write the four staged-as-primary positives into the Label bullet and `fit_reason`. Ask the curator whether AD172 and AD186, the ones without the paper's support, are undetermined like AD218. Doing so drops the positives to 13 (4-5 per test fold), which makes point 7 worse. The curator should see that trade, not have it hidden.

**4. Clinical inputs known at surgery are dropped without a reason (P3, USE-6, Must).**
- **Problem.** GEO gives age, sex and pack-years for all 123 rows (pack-years for 121), and all three are known at the prediction point. "Not features" lists them beside real leaks (stage M1, the cluster, the notes) and gives no reason.
- **Evidence (column auditor).** Pack-years alone has an AUC of 0.326, which is real signal inverted: metastasis patients smoked less. Adding the three columns moves the random forest from 0.879 to 0.884 and logistic regression not at all. Sex is already in the frame through XIST and RPS4Y1.
- **Effect on scores.** Small.
- **The rule.** USE-6 is a Must: "dropping it changes the task".
- **Remedy (fix the definition).** Ship the three columns; it is cheap and safe from the series matrix. Or, if the curator frames the task as the profile alone as a second opinion, say so in the definition with the measured cost.

**5. The recording note reads as LEAK-15's retire clause and names the wrong mechanism (P4, LEAK-15, Must).**
- **Problem.** The record says the share present "runs through every gene and cannot be removed". That is LEAK-15's own retire condition, cited as a keep.
- **Wrong mechanism.** The record says "a higher noise floor". The scanner noise, RawQ and background do not differ by class (0.475 / 0.517 / 0.481). What differs is the MAS5 scaling factor (0.621): the metastasis arrays are dimmer and get scaled up (column auditor).
- **Conceded: the artefact does not carry the score.** The evidence:
  - Array QC alone scores 0.667.
  - Ranking genes within each array removes the scale, and it scores 0.848 against 0.846 (task gamer).
  - Regressing the scaling factor and the share present out inside the folds leaves 0.800, which is a lower bound (column auditor).
  - So the retire clause is not met in substance.
- **Remedy (a note).** Rewrite the note with the scaling-factor mechanism and the within-array-rank result as the reason the score survives. Add the LEAK-15 Cases row to the Cases table (it is only inline now).

**6. Claims in the definition that do not hold, and the target words (P5 faithful claims; P7 CLEAN-25, Should; writing).**
- **"First piece, first hybridisation" is false for 10 rows.** For all 10 patients with `-1`/`-2` titles, GEO's sorted first title is the later preparation. Two of them are metastases (AD340, AD350). The effect is nil: LR 0.844 against 0.833, RF 0.879 against 0.870. Remedy: reword, or take the study's own `Sample1` (column auditor).
- **The accepted warning `splits_test_minority_few` gives a reason that does not hold up.** It says "the methods separate (RF 0.876 against LR 0.836)". The patient bootstrap 95% CI of that gap is -0.014 to +0.094 (split auditor). Rewrite it.
- **Other claims that do not reproduce:**
  - NAPSA has no probe set on HG-U95Av2: nine marker genes, not ten.
  - "Other at 0.83" reproduces as 0.76 (3 rows).
  - The study's scans run to 25 April. The 17 April end holds for the 123 rows only.
  - The controls' 0.695 depends on the model (LR 0.736, RF 0.621).
  - The splits-comment values have no split count.
  (Claim auditor; split auditor note 3.)
- **Target words (CLEAN-25, Should).** The definition builds the class words itself, and the event "metastasis from another organ" sorts first. Under sorted-column scoring, a participant who passes P(metastasis) as the second column gets a mirrored AUC (0.18; task gamer, main session). Remedy: "No" / "Yes" with "Yes" the metastasis, as CLEAN-25's default asks.

**7. Too small to rank methods is not ruled out; the evidence leans towards parkinsons (P6, TP-5, Must).**
- **Problem.** There are 15 positives in total and 5 per test fold. `few_minority` flags below 5, so "no flag" decides nothing at exactly 5. In total, 15 sits nearer parkinsons (8, retired) than musk (about 39, kept).
- **Evidence.**
  - Patient bootstrap of the method gaps on the shipped splits (split auditor): RF vs LR 95% CI -0.014 to +0.094; RF vs kNN -0.012 to +0.17. Only gaps of about 0.08 or more resolve.
  - "RF wins 20 of 20 repeats" recombines the same 15 patients (the TP-5 Cases note: repeats add no evidence).
  - A single fold's AUC has an SD of 0.093.
- **My own test.** Kendall's W of the method ranks across the 60 shipped folds, on the split auditor's per-fold AUCs for RF, extra trees, LR and kNN, is **0.22**. Parkinsons was retired at W 0.18, "less stable than on 98% of BeyondArena". This is not like for like: 4 methods here against 37 configurations there. It does not prove `Too Small`, but it does not set this case apart from parkinsons either.
- **Remedy.** Before shipping, run parkinsons' own criterion: Kendall's W over the BeyondArena configuration set on the shipped folds, placed against BeyondArena's distribution. If it lands where parkinsons did, the outcome is `Too Small`, which is a dataset decision; no re-split fixes it, since 5 folds leave 3 per fold. If it lands clearly better, keep the dataset, and record the first `splits_test_minority_few` acceptance as a TP-5 Cases row with that number. If point 3 drops two positives, re-run it.

**Judgment record (critic's view):**
```text
Verdict: ship only after changes; points 1 and 7 can end at No.
Validity: USE-1 amendment undated (process; amend deliberately or treat like lung_cancer); USE-8 fit reason understated
(negatives exclude hard cases); USE-5 positives on an inconsistent line (note + curator question); USE-6 three known
inputs dropped without reason (ship them or state why); LEAK-15 not triggered in substance, note wrong; SPLIT-1 holds.
Value: TP-5 borderline, untested against parkinsons' criterion (W 0.22 on 4 methods); MET-8 roc_auc holds.
Quality: CLEAN-25 event sorts first; claim fixes (first piece, NAPSA, accepted-warning reason).
```

**Rebuttal**


**Critic, rebuttal: lung_adenocarcinoma_metastasis (PR #75), 2026-11-11**

**Where we stand.** On remedies, the advocate and I now ask for nearly the same changes. The disagreements left are three:
- **Route for the use case (point 1).** It has to be an amendment of USE-1, not an exception.
- **What the assay fact proves (point 1).** It sets this case apart from lung_cancer only once the use case is restated around that assay.
- **What TP-5 needs before shipping (point 5).** Parkinsons' own measurement must be run first.

I concede the LEAK-15 question after a test of my own (new fact below).

**New fact (flagged for a second round).** I tested whether the processing batch explains the class difference in share present. It does not. Share present varies by batch among primaries, as the advocate found, but the metastasis-versus-primary difference persists inside batches:

| Comparison | Share present ROC AUC (metastasis low) |
|---|---|
| Pooled | 0.710 |
| Centred within IVT batch | 0.716 |
| Pairs within the same IVT batch (323 pairs) | 0.740 |
| Centred within scan day | 0.695 |
| Pairs within the same scan day (200 pairs) | 0.705 |

So the batch effect is a second recording component, separate from the class difference. The record's "nor the processing batch" stands; the note should add the batch component. Script: `PANEL/critic/within_batch.py`.

**Advocate point 1 (USE-1/USE-2, the assay as the distinguishing fact): partly disputed.**
- **Conceded.** A real decision exists (USE-2 is not triggered). The fit is approximate. The advocate's remedies match mine: quote the sheet's negatives, replace "not used today", date and sign the USE-1 text, and correct lung_cancer's "not a rule change".
- **Disputed: the route.** The advocate calls the assay fact the answer to the precedent checker's option (a), "recorded as an exception". USE-1 is a Must, and principles.md says: "A Must has no exceptions: only a higher-ranked Must overrides it, and anything else is an amendment." The label also fits neither branch of the amended USE-1: it is not a separate work-up, and it is not settled. So the ship needs the deliberate amendment (option d), with date, curator, case and a `decision_register.py --rule USE-1` pass over glioma and tcga_lung_histology. The undated text in the PR does not count as one.
- **Disputed: what the assay fact proves.** The definition's use case is a pathologist with a known earlier cancer. The assays the advocate cites serve a different setting, according to the domain practitioner, the source the advocate relies on:
  - They serve cancers of unknown primary, and they run on FFPE tissue.
  - NCCN does not recommend them as standard management, and payers call them investigational.
  - The practitioner adds that the assay use case "still needs the hard negatives, so it does not lift the fit to direct".
  The precedent checker named the same gap in option (a)'s "con". So the fact sets this case apart only once the use case is rewritten around that actor: an expression tissue-of-origin test as a second opinion when IHC is inconclusive. It must not stand beside the current wording.
- **Where it ends.** Ship after the amendment and the rewrite; without the amendment, the case is lung_cancer's. This is the curator's call.

**Advocate point 2 (USE-5, the soft positives): conceded, with the note kept.**
- The advocate is right that noisy positives such as AD172 (rank 108) and AD178 (rank 73) lower the AUC; they do not inflate it.
- The task gamer's cluster-derived-label concern is met by dropping AD218. The 7 colon flags in `CM` are the paper's "previously diagnosed".
- The line between AD218 (only in `PATH II`) and the "?Br MET" flags (in the clinical sign-out) is a stated fact that sets them apart. The newer decision (issue 2, B) does not contradict issue 8, A. The curator's decision ranks above an AI argument, so I withdraw the question on AD172 and AD186.
- I keep the note we both ask for: "4 of the 15 were staged as lung primaries (no M1); the paper's 12 suspected metastases appear to exclude two or three of them."

**Advocate point 3 (P4, no leak, split right): conceded.** I raised nothing against it.

**Advocate point 4 (LEAK-15): conceded.**
- The advocate's test and mine agree on the facts: there is a recording component (batch, scan day, and the MAS5 scaling factor).
- It does not carry the score:
  - Within-array ranks give 0.848 against 0.846 (task gamer).
  - Removing the scaling factor and share present inside the folds leaves a lower bound of 0.800 (column auditor).
  - Batch-grouped folds score as random folds do (split auditor).
  - The class difference holds within batches (my test above).
- So LEAK-15's retire clause ("cannot be undone" and carrying features that matter) is not met in substance. The remedy is the note and the Cases row, as both briefs say. The note should not say "cannot be removed", since a label-free per-array rank removes it.

**Advocate point 5 (TP-5): disputed on what decides it.**
- **Conceded:** every fold can be scored (MET-2), the signal is real (TP-2), 3 folds is right, the accepted warning overstates, and this is the first acceptance.
- **Disputed: "about twice parkinsons per fold".** TP-5 counts units "per test fold **and in total**". The total is 15 against parkinsons' 8 and musk's about 39.
- **Disputed: the SE argument.** The advocate's SE (0.044 to 0.062 around 0.84 to 0.88) shows a signal (TP-2), not that methods can be ranked. Parkinsons was retired on rank agreement across folds (Kendall's W 0.18, "less stable than on 98% of BeyondArena"), not on chance level, and the parkinsons task was learnable too (0.785).
- **On the same kind of measure, this dataset sits close.** Kendall's W here is 0.22 (4 methods, 60 folds; not like for like). The bootstrap CI of RF minus LR includes 0.
- **Remedy (unchanged).** Before the curator answers prompt B, run parkinsons' criterion on the shipped folds: W over the BeyondArena configuration set, placed against BeyondArena's distribution. Without it, "5 is not a handful" is an assertion. The winning rule is TP-5 (Must), and "independent failures are not conflicts", which the advocate concedes.

**Advocate point 6 (USE-6): agreed.** Ship age, sex and pack-years.

**Advocate point 7 (wording, CLEAN-25): agreed.** It includes PROV-7 in place of PROV-14 for the new record (precedent checker), which I had not listed.

**Updated judgment record (critic):**
```text
Verdict: ship after changes; two curator calls can still end at No.
Validity: USE-1 needs a deliberate amendment (date, curator, case, register pass) and a use case restated to the
tissue-of-origin assay's actor, else treat like lung_cancer; USE-8 fit reason rewritten (negatives); USE-5 note;
USE-6 add age, sex, pack-years; LEAK-15 not triggered (conceded: difference holds within batch, does not carry the
score), note rewritten; SPLIT-1 holds.
Value: TP-5 open until Kendall's W on the BeyondArena config set is run on the shipped folds.
Quality: CLEAN-25 No/Yes; claim fixes; PROV-7 cited.
```

</details>

<details><summary>Checks and probes (main session)</summary>

**Main session notes (2026-11-11)**

- `dataset check` on the PR branch: 0 errors, 0 warnings, 2 accepted (`meta_license_unknown`, `splits_test_minority_few`);
  the README regenerates with the same data (only template wording changed). The download instructions, pasted into a
  shell today, recreate the raw inputs (series matrix, 254 MAS5 files, caArray archive; 29 MB).
- Probes (`PANEL/probes/`): no flags. Task probe on 30 of 60 splits: random forest 0.876, selected linear 0.851,
  logistic regression 0.836, LightGBM 0.811, best single feature chosen per split 0.652; dummy log loss 0.371. Leak
  probe: no exact copies across the split; number format 0.491; 1-NN agreement 0.902 against chance 0.786; label-free
  nearest-neighbour distance 0.746. Hidden groups: none. Generated: no flags. Dtype: 0 of 12,558 flagged.
- Target words (CLEAN-25, Should): the definition builds the labels "metastasis from another organ" / "primary lung"
  itself (the sheet has 0/1 flag columns, no words for the target), so CLEAN-25's default applies: "No" / "Yes" with
  "Yes" the event (sorting second, `labels[1]`). As shipped the event sorts first. ROC AUC is unaffected; the task
  gamer notes that `score()` reads probability columns in sorted order, so a participant who passes P(metastasis) as
  the second column gets a mirrored AUC (0.18). A wording fix, no score change.
- The task gamer's hand-back tool was blocked by its sandbox hook; its report was recovered from its final message.

</details>

## Reference

@article{bhattacharjee2001classification,
  title={Classification of human lung carcinomas by mRNA expression profiling reveals distinct adenocarcinoma subclasses},
  author={Bhattacharjee, Arindam and Richards, William G and Staunton, Jane and Li, Cheng and Monti, Stefano and Vasa, Priya and Ladd, Christine and Beheshti, Javad and Bueno, Raphael and Gillette, Michael and others},
  journal={Proceedings of the National Academy of Sciences},
  volume={98},
  number={24},
  pages={13790--13795},
  year={2001},
  publisher={The National Academy of Sciences}
}
