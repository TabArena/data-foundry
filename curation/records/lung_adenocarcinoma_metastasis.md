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

## Review

**Outcome:** added. 123 lung adenocarcinomas resected at one Boston centre (Bhattacharjee et al., PNAS 2001), each one
Affymetrix array (12,558 human probe sets, MAS5 per array, from GEO GSE83227), with the study's own flag of a possible
metastasis from another organ (15: 8 colon, 4 breast, 3 other) as the binary target; ROC AUC, random stratified folds.
The arrays come from the retired `lung_cancer`; this record holds the task the source names, "the discrimination of a
primary lung adenocarcinoma from a distant metastasis to the lung". The review panel recommends shipping after changes,
which are applied: the 67 control probes, two patients without clinical data and the two inconsistently coded AD218 and
AD224 (issue 2, B) dropped, a wrong recording note corrected, `Class-dependent Recording` and `Selection Bias` added.
Validity: the decision is real and the label comes partly from outside the specimen (the earlier cancer), but it is
written in the tumour's own pathology note and hedged ("c/w", "?"), so the fit is approximate; the rows are all resected
adenocarcinomas, not only patients with an earlier cancer. No feature leak; the metastasis arrays call fewer genes
present, kept with a note (it carries a part of the score, not most of it). Value: 5 metastases per test fold, no
task-probe flag, random forest 0.876 against logistic regression 0.836 and ten unfitted pathology marker genes 0.819;
colon metastases carry most of it (0.984 against 0.76 for breast). Weighed: a source-named decision and the study's own
deposit +; 15 positives, 3 without a firm note, one centre and a 2001 platform -.

**Main points:** both settled on 2026-11-11: the restated use-case reason is approved (issue 1, A); AD218 and AD224
are dropped as undetermined (issue 2, B).

**Record judgment:** valid. A new record (2026-11-11) with the panel's corrections: the label, rows, size and recording
bullets restated, both markers and the `Samples: No Time Dimension` tag added, priority 1. Its CC line gives the reason
for a separate record: rows, target and values all changed. Licence: GEO's series files and the PNAS supplement state
none, so none is recorded; lung_cancer_epithelial_genexp, also from GEO, records "Public Domain" without a source.

**Issues for Andrej:**

1. **Keep the task on the restated reason: the call is read from the tumour's pathology but rests on an earlier cancer outside it?**

   * **Problem:**
     - The record kept this task because the label comes "from a work-up separate from the arrays"; the rule rejects a label read from the same specimen the features measure and settled before they are taken, whatever the arrays show[^1a].
     - 15 of the 16 flags are written in the resected tumour's own pathology note, like the histology of lung_cancer and the grade of glioma_grading, both retired on that rule[^1b].
     - Keep the task on a reason that sets it apart, or retire it like them?
   * **Background:**
     - What sets it apart: the notes are hedged ("c/w colon met", "?Br MET"); the source says such metastases "can be
       difficult to distinguish from lung adenocarcinomas"; the call rests on an earlier cancer outside the specimen;
       and the source names the decision ("a key issue in lung tumor diagnosis").
     - The 8 colon flags are the firmest calls (7 are the paper's "previously diagnosed" colon metastases) and the
       easiest part of the score (out-of-fold ROC AUC 0.984).
     - The domain practitioner rates the fit "approximate, close to none": a real decision, but a proxy label and a
       proxy population; both sides of the debate keep it approximate once the population gap is marked.
   * **Panel:** precedent checker and critic raised it; advocate and critic agree on the restated reason; the mediator
     accepts it with the critic's condition (name the colon calls as the firmest part).
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep, reason restated (implemented) | the record, `use_case`, `fit_reason` and the curation notes say "read from the specimen's pathology but not settled there; it rests on the earlier cancer"; the use-case rule's Cases row on PR #75 is reworded the same way | the stated fact matches the sheet; the same wording then decides tcga_lung_histology and sarcoma consistently | the label fits neither clause of the rule cleanly: read from the specimen, but not settled there |
     | B | Retire like lung_cancer | `No` with `No Good Target / Scientific Discovery` | one reading of "same specimen" for all three | drops the one diagnostic task the source names, which passes the probes |

   * **Recommendation:** A: the keep is sound and only its stated reason was off; both sides of the debate agree.
     **Decision:** A or B?

   **Resolved (2026-11-11, Andrej):** A, kept on the restated reason: the call is read from the tumour's pathology but
   not settled there, since it rests on an earlier cancer outside the specimen. The USE-1 Cases row and the record's CC
   on PR #75 say so.

   **Notes for the AI:** on A, reword the USE-1 Cases row and the lung_adenocarcinoma_metastasis CC bullet on PR #75
   to the restated reason (the definition and record of the working copy already carry it) and sync the PR's
   definition with the working copy's changes of 2026-11-11. On B, record `No` with the marker and a CC line; the
   folder leaves; the Cases rows on PR #75 change accordingly.

   [^1b]: lung_cancer's histology target retired 2026-11-10 and glioma_grading_clinical_and_mutation_features retired
     2026-10-26, both on the use-case rule (a pathology call on the measured specimen).
   [^1a]: **USE-1** (Must, amended on PR #75): a label read from the same specimen the features measure, and settled
     before they are taken, leaves only a cross-check of a known label and fits no decision; a label found by a
     separate work-up is ground truth, also in a retrospective series of resolved cases.

2. **Keep AD218 and AD224 as the source codes them, or drop both as undetermined?**

   * **Problem:**
     - AD218's only metastasis note is the study's own second pathology review (`PATH II`: "ad w met?"), and the tumour lies in the group the paper's clustering of the arrays formed around the colon metastases, so its flag may have been read off the same expression the model sees[^2a].
     - AD224 has the same kind of second-review note ("ad m met?") and is coded primary, so the sheet codes the same evidence two ways.
     - Keep both as coded, or drop both?
   * **Consistency:** reopens your call to count all 16 flags[^2b]; the panel found these facts after it.
   * **Unknown:** whether the second review was made blind to the expression clusters; the sheet does not say, and that
     would settle AD218.
   * **Experiments** (ROC AUC, higher is better; the 60 shipped folds with the rows taken out, the 67 control probes still in, so the scores differ from the shipped 0.886; review panel 2026-11-11):

     | Variant | Logistic regression | Random forest | LightGBM |
     |---|---|---|---|
     | Both kept (125 rows) | 0.8555 | 0.8950 | 0.8152 |
     | Without AD218 (124 rows) | 0.8549 | 0.8908 | 0.8284 |
     | Without AD218 and AD224 (123 rows) | 0.8561 | 0.8929 | 0.8326 |

     Every change lies within noise (random forest paired standard error about 0.003), and the ranking of the methods
     does not move. Out of fold, AD218 ranks far below the colon flags, so a flag taken from the clusters does not
     inflate the scores.
   * **Panel:** the advocate keeps both (a pathologist's reading; dropping would put our reading in place of the
     source's); the critic drops AD218 (a label possibly read off the modelled expression); the mediator recommends
     dropping both, weakly, since dropping only AD218 keeps its twin coded the other way.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep both (implemented) | 125 rows, 16 positives; both named in the curation notes | the source's coding; your standing call | one flag may come from the expression; the same note coded two ways |
     | B | Drop both as undetermined | 123 rows, 15 positives (5 per test fold) | removes our reading only where the source contradicts itself | two fewer rows; a positive less |
     | C | Drop AD218 only | 124 rows, 15 positives | removes the one flag that may be circular | keeps AD224 coded the other way on the same evidence |

   * **Recommendation:** B, weakly: the sheet contradicts itself on the same note, and dropping both removes the
     contradiction without taking a side; A stays defensible, since the scores do not move. **Decision:** A, B or C?

   **Notes for the AI:** on B or C, add the patient numbers to a constant with the note that sets each apart, drop them
   in `_clean`, rerun `dataset check` and the task probe, update the row counts in `task_summary`, the curation notes,
   the record and the CHANGELOG.

   **Andrej (2026-11-11, change):** Option B: Drop both as undetermined.

   **Resolved (2026-11-11, Andrej):** B, both dropped as undetermined (`UNDETERMINED` in `dataset.py`): 123 rows, 15
   positives (8 colon, 4 breast, 3 other), 5 per test fold. Dataset check clean; task probe on the redrawn shipped
   splits: no flag, random forest 0.876, selected-features linear 0.851, logistic regression 0.836, LightGBM 0.811
   (on 125 rows 0.886, 0.866, 0.851, 0.819: the splits are drawn anew, so the scores move; on fixed folds the two rows
   moved nothing).

   [^2b]: Andrej, 2026-11-11, lung_cancer review issue 8, A: all 16 flags of the sheet count.
   [^2a]: **USE-5** (Must): check how the source built its label before accepting it; a label checked and found to be
     another quantity than the one the actor acts on fails.

**Review panel:** ship after changes (mediator). Full panel: seven evidence agents, the advocate and the critic with one
rebuttal each, the mediator. Claim audit: 2 claims refuted on validity (the control probes "carry no signal", from a run
that paired labels with the wrong arrays; "127 patients with a recorded history", 2 have none), both fixed; 3 notes
corrected (which colon flags lie in the paper's colon expression cluster, the paper's 12 suspected metastases
against the sheet's 16, the reason for the metric); the rest hold. Blind review: include with
changes; main concerns the soft label and its possible circularity, and few positives. Task gamer: no exploit in the data beyond noise (an 18S-rRNA control probe, +0.007, gone with the
control probes); looking up the published flags in GEO scores 1.0, as for any public dataset. Agreed: the split, size,
no leak, both markers, the dropped probes and rows, the documentation fixes, and after the debate the restated
use-case reason (issue 1, for your approval). Disputed: AD218 and AD224 (issue 2). The critic asks for a low weight in
aggregates (16 positives, few of them firm): a benchmark-level call, not a change here.

<details><summary>Mediator</summary>

**Mediator: lung_adenocarcinoma_metastasis (2026-11-11)**


**Recommendation (judgment record)**
Verdict: ship after changes.
Validity: USE-1 holds only with the reason restated (read from the specimen's pathology but not settled there; the prior
cancer comes from outside the specimen); "a work-up separate from the arrays" does not hold. USE-2 holds. USE-5: AD355
and AD360 dropped (no clinical annotation); AD218/AD224 open (issue 2). USE-8: fit approximate, Selection Bias added.
LEAK-13 to 15 / LEAK-39 triggered: the 67 AFFX controls dropped; the %P/noise-floor difference kept with a note and the
`Class-dependent Recording` marker; LEAK-15's retirement condition not met (floor subtracted LR 0.855 -> 0.857).
SPLIT-3, SPLIT-32 hold. PROV-7/PROV-14: new record right.
Value: TP-4 not Trivial (panel 0.819 vs RF 0.894); TP-5/TP-8 not Too Small (5-6 per fold, SE of 20-repeat mean
0.003-0.005); MET-8 fallback roc_auc.
Quality: CLEAN-2 linear MAS5 (one sentence); documentation corrections.
Weighed: source names the decision +; 16 positives mostly colon -; one centre, dead platform -; label "possible" -.
For the curator: issue 1 (USE-1 wording and Cases row); issue 2 (AD218/AD224, reopens lung_cancer issue 8 A); issue 3
(licence sibling); issue 4 (weight/priority).

**Decisive experiment (60 shipped splits; dropped rows removed from their folds)**
| Variant | LR | RF | LGBM | RF delta vs shipped (paired SE) |
|---|---|---|---|---|
| V0 shipped | 0.8535 | 0.8942 | 0.8196 | - |
| V1 without 67 AFFX | 0.8521 | 0.8928 | 0.8257 | -0.0013 (0.0034) |
| V2 without AD355, AD360 | 0.8555 | 0.8950 | 0.8152 | +0.0008 (0.0020) |
| V3 = V2 without AD218 | 0.8549 | 0.8908 | 0.8284 | -0.0034 (0.0030) |
| V4 = V3 without AD224 | 0.8561 | 0.8929 | 0.8326 | -0.0012 (0.0032) |
| V5 = V3 without AFFX | 0.8548 | 0.8894 | 0.8305 | -0.0048 (0.0042) |
All within noise (LR moves <= 0.0025; LGBM <= +0.013, SE 0.0095); ranking RF > LR > LGBM in every variant.
OOF ranks of 127: AD218 (positive) LR 13 / RF 14 / LGBM 12; AD224 (primary) 22/47/54; AD320 (primary) 4/1/6. AD218 sits
in CM but scores well below the colon flags: a cluster-derived flag would not inflate scores. Dropping AFFX, AD355/360
or AD218 costs nothing; AD218 is a label-validity question, not a score question.

**Changes to make now**
1. Drop the 67 AFFX controls (LEAK-13 to 15; "fix what separates the classes for non-target reasons after measuring
   it"): all AFFX LR 0.695 (p 0.02), 18S 0.784; no cost (V1). Reverses the AI note on lung_cancer issue 1 D, which
   rested on the histology target; the metastasis number behind it came from the misaligned script: say so.
2. Drop AD355 and AD360 (USE-5): 125 rows, the paper's "125 adenocarcinoma samples were associated with clinical data".
3. `Class-dependent Recording` marker; rewrite the recording bullet: all AFFX LR 0.695 (p 0.02); %P 0.722 (p 0.01,
   lower in metastases); noise floor 0.70; 18S 0.784; floor subtracted 0.855 -> 0.857; RF with %P removed 0.889 ->
   0.859 (colon 0.968, breast 0.718, other 0.782). Cause open; not tumour content (Spearman -0.20); kept with a note.
4. `Selection Bias`; fit_reason and use_case agree (USE-8): all resected adenocarcinomas, most primaries "no history or
   path indicating non adeno"; prior-cancer status unrecorded (USE-6: a named gap). Fit approximate.
5. Documentation: row text; known gaps (7 colon flags in CM = the paper's 7; AD350 outside; AD218 PATH II only, in CM;
   AD224 same wording coded primary; AD320, AD368 suspected, never relabel); 12 vs 16 (12 firm, 4 not); metric = MET-8
   fallback (RF log loss 0.286 vs 0.379, information only); size section rerun on shipped 20x3 after changes 1-2, drop
   "paired SE 0.035"; per-subtype OOF AUCs (colon 0.984, breast 0.76, other 0.83); do not cite 0.8535 -> 0.8391 as
   label validity (EV-1); `Samples: No Time Dimension`; splits_comment batch sentence; linear MAS5 on purpose (CLEAN-2);
   rows are public GEO arrays with published labels.

**Issues for the curator**
1. USE-1 (Must, P3): restate the reason. 15 of 16 flags from the specimen's own pathology report; no history column; the
   rule's line is the specimen. Separating fact: unsettled on the slide ("c/w", "?"; "difficult to distinguish"),
   depends on a prior cancer outside the specimen, source-named decision. Both sides agree (precedent 1a); critic's
   condition accepted: the 8 firm colon calls come closest to "settled before" and are the near-trivial part (0.984).
   Approve the wording in the CC, fit_reason, the record bullet and the USE-1 Cases row.
2. AD218 and AD224 (USE-5, Must; reopens lung_cancer issue 8 A): AD218 in CM, the only flag that may come from the
   clusters; AD224 same PATH II wording coded primary. No measurable effect. Advocate: PATH II is a pathologist's reading;
   blindness untested; dropping substitutes our reading. Critic: a label possibly read off the modelled expression fails
   USE-5. Options A keep both and name them; B drop both as undetermined; C drop AD218 only (inconsistent).
   Recommendation B, weakly; A defensible. Settled by when PATH II was read relative to the clustering (not in the sheet).
3. Licence: keep "None"; correct lung_cancer_epithelial_genexp ("Public Domain") as its own issue.
4. Weight/priority: the curator's call (16 positives, half hedged, colon carries most of the AUC).

**Task gamer exploits mapped**
| Exploit | Gain | Rule | Known? | Disposition |
|---|---|---|---|---|
| Public GEO lookup | AUC 1.000 (+0.147) | none (any public dataset) | new | one sentence |
| 18S rRNA probes | +0.007 (noise) | LEAK-13 to 15 / LEAK-39 | new; contradicts the notes | removed with AFFX; %P kept with marker |
| Transductive standardisation / quantile norm | +0.001 | LEAK-30 | MAS5 per array | none |
| Label flaws AD320, AD224 vs AD218 | hurts honest models | USE-5 | partly | documented; issue 2 |

**Agreed facts**
127 rows = 127 patients, first arrays, MAS5 per array; 16 flags (8/4/4); 12 A patients and AD355/AD360 unannotated; no
feature leak, strongest columns organ-of-origin biology; %P 0.72 and 18S 0.78 lower/higher in metastases, cause open,
claim 7 from a misaligned script; IID by patient right, grouped folds same, adversarial 0.49; panel 0.819 vs RF 0.894;
RF - LR +0.039 (SE 0.006); 5-6 positives per fold; colon 0.984, breast 0.76, other 0.83; no colon flag cluster-derived;
critic withdrew retirement; both sides ship after changes.

**Consistency**
Follows musk and the TP-8 row (size); thyroid recurrence and diabetes_3 (soft label); regensburg's logic (drop
unannotated rows); ljubljana, gcm, sarcoma (Selection Bias); gallstone_disease (marker kept after a fix); PROV-7 (new
record). USE-1 departs from lung_cancer and glioma only through the restated fact (issue 1). Issue 2 departs from issue
8 A only through new facts. The PROV-14 Cases row should cite PROV-7.

</details>

<details><summary>Claim audit</summary>

**Claim audit: lung_adenocarcinoma_metastasis (2026-11-11)**

;
rows matched to GEO arrays by full signal vector, labels checked.)

**Summary**
Two claims refuted on validity grounds; neither excludes the dataset.

1. **Claim 7 refuted.** The earlier script `<run folder>` paired labels with the wrong
   arrays (`Xall = L[[list(first).index(i) for i in F.index]]`: `L` holds all 248 arrays, the index is a position in
   the first-array list). Aligned, on the shipped splits:

   | Inputs (LR) | ROC AUC | Permutation null 95% (200) | p |
   |---|---|---|---|
   | All 67 AFFX | 0.695 | 0.638 | 0.02 |
   | Human AFFX controls | 0.698 | | |
   | 33 non-human spike-ins | 0.596 | 0.658 | 0.17 |
   | Scale factor, background, RawQ | 0.58 | | n.s. |
   | Share called present (%P) | 0.722 | 0.649 | 0.01 |

   Metastases lower %P (median 0.310 vs 0.358); among primaries %P correlates with the RF out-of-fold score at Spearman
   -0.67; not the IVT batch, not tumour content (Spearman -0.20; tumour % alone AUC 0.50). Removing %P from the RF score
   lowers AUC 0.889 -> 0.859:

   | Positives | RF AUC | After removing %P |
   |---|---|---|
   | Colon | 0.984 | 0.968 |
   | Breast | 0.760 | 0.718 |
   | Other | 0.829 | 0.782 |

   Part of the signal is an array-quality covariate, biology or specimen handling undecided.
2. **"127 patients whose clinical history the study recorded" refuted.** AD355 and AD360 have every clinical field
   empty in DATASET A, like the 12 dropped A patients; the paper: "125 adenocarcinoma samples were associated with
   clinical data." Both ship as primary; by the definition's own reason "no flag" is no finding for them.

Documentation corrections: claim 9 refuted (the paper's 7 previously diagnosed colon metastases are exactly the 7 colon
flags inside CM; AD350 is outside CM and scored low: RF rank 17, LR p 0.003; the one flag that may rest on the study's
review is AD218, other met, CM member, clinical path "ad 5.0 m BAC", PATH II "ad w met?"). Two "primary" rows the source
suspects: AD320 (only unflagged CM member, RF's top-ranked row, mean p 0.447) and AD368 (paper: "high levels of albumin,
transferrin ... associated with the liver", "not identified as a metastasis"). The paper's n = 12 is never reconciled
with 16: exactly 12 flags have a firm clinical-path note; the other 4 are three "?Br MET" (AD163, AD172, AD186) and
AD218's PATH II note.

**Claims**
| # | Claim | Test | Result | Evidence | Rule |
|---|---|---|---|---|---|
| 1 | Source names the task, scores no classifier | read 13790.pdf | holds | Results quote; only classifier is kNN marker selection over cluster subclasses (suppl. Table 1 not read) | USE-1, MET-1 |
| 2 | Label = sheet's 16 flags of 139, from history and pathology | sheet | holds, one caveat | 16 flags, all among the 127; sheet tallies 16/123; 15 with a clinical-path note; AD218 only PATH II and a CM member; cluster column next to flags, so the sheet was filled after clustering | USE-5 |
| 3 | 12 A patients unannotated, rightly dropped | DATASET A | holds | all fields empty | USE-5 |
| 3b | "127 patients whose clinical history the study recorded" | same fields | refuted | AD355, AD360 empty; paper says 125 | USE-5 |
| 4 | One array per tumour, MAS5 per array | titles, headers, batch | holds | 47 patients with 2-4 arrays; "TGT=500 ... SFGene=All"; chosen array's batch independent of label (Fisher p >= 0.18) | LEAK-30 |
| 5 | 5-6 per fold; RF 0.887 ... panel 0.819 | recomputed, refit | holds | 40 folds with 5, 20 with 6; refit on shipped splits RF 0.894, LR 0.855; probe_met used 12,558 probes without AFFX while 12,625 ship | TP-5 |
| 6 | "LR and LightGBM lose to class shares on log loss, so ROC AUC" | task probe; Metric.fallback | facts hold, reason misattributed | RF beats class shares on log loss (0.286 vs 0.379); fallback gives roc_auc for any binary task | MET-8, MET-11 |
| MET | fallback roc_auc, no scoring columns | paper; dummy per fold | holds | constant scores 0.500 on all 60 folds; folds 42-43 rows, 5-6 positives | MET-1, MET-2 |
| 7 | Controls carry no recording signal | aligned rows, permutation null | refuted | above | Class-dependent Recording, EV-1 |
| 8 | Clinical fields not features | columns; GEO | holds | GEO stage reads "M1" for 11 of 16 flags vs 4 of 111 primaries | LEAK-10 |
| 9a | Flags possible; fit approximate | OOF ranks | holds, understated | AD320 ranked first; AD368 primary; pooled OOF AUC colon 0.984, breast 0.761, other 0.829 | USE-5 |
| 9b | One colon flag may come from clusters | CM vs flags | refuted | above | USE-5, EV-2 |
| 9c | Paper n = 12 vs 16 flags | clinical path | not reconciled | 12 firm, 4 soft | USE-5 |
| 10 | No time dependence; random split | batch, dates | holds | | SPLIT-32 |
| 10b | One tumour per patient | unique patients; correlation | holds | closest different-patient pair r 0.394 (360T1, 287T1) vs median 0.427 same-patient | SPLIT-24 |
| 11 | New record | PROV-14 | holds | rows, values, target changed | PROV-14, PROV-11 |
| 12 | GEO states no licence | matrix, Readme | holds (files) | GEO web page not fetched | - |

**Ranked**
1. Claim 7 (recording, P4/P5): evidence wrong; %P costs RF ~0.03 AUC; colon survives at 0.968; the task stands. Remedy:
   replace the numbers, state the %P association with unknown origin. Untested: whether quantile normalisation or
   dropping low-%P arrays changes the ranking (rank-normalised arrays: RF 0.898).
2. Claim 3b (USE-5): drop AD355 and AD360 by the A-patient rule (125 rows, 16 positives, as in the paper), or keep and
   correct the row text.
3. Claim 9b: rewrite the known-gap note (7 colon flags in CM = the paper's 7; AD350 outside CM; AD218 the one possibly
   review-based flag; AD320, AD368 labelled primary though suspected).
4. Claim 9c: one sentence explaining 12 vs 16; issue 8 A stands.
5. Claim 6: reword to "the fallback for a binary task"; log loss would be scorable.
6. Untested: whether PATH II was read blind to the clusters; the supplement's MAS4/OpenML statements; GEO's licence page.

None is an exclusion reason.

</details>

<details><summary>Column audit</summary>

**Column audit: lung_adenocarcinoma_metastasis (2026-11-11)**


**Verdict: no leak, no cleaning problem in the features.** Dtype probe 0 of 12,625 flagged; every column a measured
MAS5 signal, numeric right. Two questions (1, 2), three minor notes (3-5); claim 7 unstable.

**Column groups**
| Group | Columns | Meaning | Known at prediction? | Dtype/cleaning | Verdict |
|---|---|---|---|---|---|
| `_at` | 10,045 | MAS5 signal of one transcript (GPL8300); 317 without symbol | yes | float64, 1 decimal, 0.1-165,731; no missing/zero/negative | fine |
| `_s_at` | 1,121 | shared probe sets; 732 map to 2+ symbols overall | yes | as above | fine |
| `_g_at` | 524 | another transcript of a gene | yes | as above | fine |
| `_r_at` | 416 | rules-dropped design | yes | as above | fine |
| `_f_at` | 322 | gene-family cross-hybridising | yes | as above | fine |
| `_i_at` | 130 | incomplete probe set | yes | as above | fine |
| AFFX controls | 67 | 33 non-human spike-ins, GAPDH/ACTB 5'/M/3', 18S/28S rRNA, Alu, others | yes, but measure prep/hybridisation | as above | question |
| Never called present | 3,334 (2,986 absent on all arrays) | below detection on every array | yes | not constant, not copies | fine (signal gene-specific) |

Whole frame: no constant columns, no column copies; 9,203 symbols, 2,106 with 2+ probe sets. MAS5 scaling confirmed:
2%-trimmed mean 500.16-500.25 per array, no class signal (AUC 0.46): claim 4 holds. Calls: P 35%, M 3%, A 62%;
median signal 99 on absent, 692 on present. Excluded sheet columns confirmed: `CLUSTERS/Expression Signature` (from the
arrays; CM holds 9 of 16 positives, 1 of 111 primaries) and `Path I` (label text for 340T1-1, "?COLON METm").

**1. Metastasis arrays are dimmer and call fewer genes present**
| Per-array | Metastasis | Primary | Univariate AUC | LR AUC |
|---|---|---|---|---|
| % called present | 31.9% | 35.7% | 0.28 (0.72 inverted) | 0.722 |
| Noise floor (median log2 of the 3,334 never-present) | higher | lower | 0.71 | 0.704 |
| Scale factor (median) | 10.4 | 9.2 | 0.62 | - |
| Background, noise, RawQ, corners, masked, scan date | - | - | 0.43-0.51 | - |
| GAPDH / ACTB 3'/5' (RNA integrity) | - | - | 0.61 / 0.58 | - |
| Tumour % (`max_tumor%`) | 65 | 66 | - | - |
Floor rises with SF (Spearman 0.63), falls with % present (-0.85); tumour % does not explain it (rho -0.20); scan
dates alike. Cause open: narrower transcriptome of a metastasis (biology) or weaker RNA (recording). It does not drive
the models:
| Block (log2) | LR AUC |
|---|---|
| All 12,625 | 0.855 (0.843 linear) |
| All, per-array floor subtracted | 0.857 |
| 3,334 never-present | 0.847 |
| Same, floor subtracted | 0.849 |
| 4,313 present on >=50% of arrays | 0.808 |
| Floor alone | 0.704 |
Remedy: no data change; note in the recording bullet: % present 0.72, floor 0.70, subtracting the floor leaves the
full model unchanged (0.855 -> 0.857).

**2. The 67 AFFX controls, and claim 7**
Claim 7 (LR 0.42; probe_met/affx.py, C=0.1, own 10 x 3) is unstable: on the shipped splits, default C, log2: 0.650
(0.639 floor-subtracted); with sd 0.09 and 16 positives neither supports "no signal". `AFFX-HUMRGE/M10098_M_at` (18S
rRNA, absent on 126 of 127) AUC 0.784, higher in metastases (z 3.7 vs null SD 0.078, ~p 0.02 after 67 tests); 18S
5'/3' 0.71/0.74; 28S `AFFX-M27830_*` 0.67-0.69; `AFFX-TrpnX-3_at` 0.72, `AFFX-ThrX-5_at` 0.70, `AFFX-BioC-3_at` 0.69.
This is problem 1 again (18S tracks the floor, rho 0.48). Remedy, decide: keep and correct the record's sentence to
the shipped-splits numbers and mechanism; or drop the 67 as measurement controls (effect on the full model not measured).

**3. Strongest columns are organ-of-origin biology (fine)**
| Probe set | Gene | AUC | % present met/prim |
|---|---|---|---|
| 1472_g_at, 2042_s_at, 41854_at | MYB | 0.883, 0.877, 0.847 | 38/0, 56/1, 44/24 |
| 37875_at | GPA33 | 0.878 | 69/37 |
| 36352_at | HES2 | 0.871 | 0/0 |
| 901_g_at | PLCB4 | 0.870 | 50/14 |
| 39277_at | OSMR | 0.131 | 12/72 |
| 39697_at, 33702_f_at, 928_at, 38586_at, 40736_at | HSD11B2, PCK1, SLC26A3, FABP1, CDH17 | 0.82-0.86 | intestinal |
| 130_s_at, 33754_at / 170_at, 40392_at | NKX2-1 / CDX2 | 0.23, 0.22 / 0.79, 0.79 | stains |
HES2 separates at 0.87 while called absent everywhere; 124 of the top 300 columns are present on <20% of arrays; the
low-level signal is gene-specific (0.849 floor removed). Keep.

**4. Minor: GEO sex wrong for patient 169**
GEO male; both arrays female (XIST present 569/402; RPS4Y1, DDX3Y, KDM5D absent); 124 of 125 others agree. Not a
feature, 169 a primary: no change. Sex readable from arrays but no class signal (AUC 0.53; positives 8 F, 8 M).

**5. Low: log scale**
MAS5 ships linear; LR 0.843 linear vs 0.855 log2; trees unaffected. CLEAN-2 points to shipping as is unless log2 is
read as the expert state (CLEAN-1); one sentence in the definition would settle it.

**Claims**
| Claim | Status |
|---|---|
| 4 per-array scaling | holds |
| 7 controls no signal | unstable: 0.42 earlier vs 0.65 shipped splits; one rRNA probe 0.78; % present 0.72 not in the QC set |
| 8 not features | holds; sheet cluster and pathology columns would leak |
| Dtype | 0 flagged |

</details>

<details><summary>Split audit</summary>

**Split audit: lung_adenocarcinoma_metastasis (2026-11-11)**


**Verdict: right, with notes.** Random stratified split by patient, 20 x 3 (seed 4267), fits the use case; processing
batches are not tied to the flag and batch/scan-day grouped folds score the same; 5-6 positives per test fold suffice,
the 20-repeat mean is stable. No re-split.

**Checks**
- Regime (claim 10): IID by patient, Timeless fair; arrays scanned 16 Mar-17 Apr 2001 on banked specimens; no
  resection dates. 20 repeats per the <500-unit rule; the record's size section cites the earlier 10 x 3 probe.
- One tumour per patient: 127 rows = 127 patients (before selection 80 with 1 array, 44 with 2, 2 with 3, 1 with 4);
  DATASET A: no two rows share age/sex/survival/status/smoking/operation/stage (only 355 and 360, all empty); NL268n1
  and SMCL301 are kept patients' other specimens, not rows; MAS5 per array; hidden-group probe no hits.
- Batches (PRIMARY DATASET joined on chip id; file name encodes scan day):

| Variable | Metastases / rows per level | Test |
|---|---|---|
| IVT batch (1, 3, 4, 7, 8, 10) | 3/13, 4/31, 4/37, 0/1, 2/27, 3/18 | chi2 p 0.78; ROC AUC 0.45 |
| Scan day (10 days) | 0-4 per day | chip-number ROC AUC 0.49 |
| Sample source | all BRIGHAM/DFCI | constant |
| OCT block | 14/100 on O1, rest scattered | no structure |

| Split (RF / LR ROC AUC) | Per-fold mean | Per-fold SD | Pooled OOF AUC | Positives per fold |
|---|---|---|---|---|
| Shipped random 20 x 3 | 0.894 / 0.855 | 0.081 / 0.092 | 0.884 / 0.846 | 5-6 |
| Grouped by IVT batch | 0.882 / 0.836 | 0.079 / 0.107 | 0.883 / 0.849 | 2-8 |
| Grouped by scan day | 0.895 / 0.856 | 0.078 / 0.073 | 0.889 / 0.841 | 2-10 |
| Leave one IVT batch out | 0.846 / 0.833 | 0.179 / 0.140 | 0.882 / 0.856 | 2-4 |

Pooled differences at most 0.005 (RF), 0.008 (LR) against a seed SD of 0.013-0.021: noise.

- Size and stability: ~185 pairs per fold AUC; worst fold RF 0.686 / LR 0.659; SE of mean over 20 repeats RF 0.003,
  LR 0.005; RF - LR +0.039 (paired SE 0.006), RF ahead on 75% of folds and 19 of 20 repeat means; RF - LR after 1/3/10/20
  repeats +0.062/+0.030/+0.041/+0.039. 20 x 5: 3-4 positives per fold, means 0.900/0.863, SD 0.107/0.132, worst 0.470 /
  0.485: 3 folds right. The record's "paired SE 0.035" for best-vs-worst likely uses another definition.

**Problems**
1. Few positives per fold (TP-5): note only; colon subgroup 2-3 per fold, not readable per subtype; accepted warning
   justified. Keep 20 x 3.
2. Batches checked and absent: add to splits_comment, e.g. "The 6 IVT batches and 10 scan days hold 0-4 metastases
   each; folds grouped by either score the same as the random split (RF pooled AUC 0.883-0.889 against 0.884)."
3. Documentation: the size section cites 10 x 3 while 20 x 3 ships.

**For the recording reviewer**
PRIMARY DATASET "proportion of Pcall" is lower on metastases: inverted ROC AUC 0.716, Mann-Whitney p 0.005; "TXT P
Calls Average" and "Average After RANK INVARIANT SCALING" 0.68 (p 0.02). The record tested only scale factor,
background and noise (0.52). Could be biology (another tissue, tumour content) or RNA quality; untested.

</details>

<details><summary>Domain practitioner</summary>

**Domain practitioner: lung_adenocarcinoma_metastasis (2026-11-11)**


Actor: a thoracic pathologist (with the molecular tumour board behind) working up an adenocarcinoma in the lung of a
patient with a prior colon or breast cancer. Read-only look-ups of SampleData.xls; no model runs.

**Fit: approximate, close to none**
The decision is real (lung primary or metastasis changes surgery, staging and drugs), but both the label and the rows
are proxies: the label is largely the 2001 pathologist's own call on this resected specimen, from its slide and the
history ("c/w colon met", "?Br MET"); the rows are all resected adenocarcinomas, not the patients with a prior cancer
in whom the question arises.

**Answers as the actor**
1. Inputs at the decision: my key inputs are missing (which prior cancer and when, the prior tumour's slides/IHC/
   mutations, imaging). A whole-genome array of the resected tumour is an input I never have; today IHC, then
   comparative NGS. No small biopsy, where the question is hardest. In this cohort the surgery was already done as for
   a primary: of the 16 flagged, 9 lobectomy, 2 bilobectomy, 1 pneumonectomy (DATASET A, `Operation`).
2. Target: I act on the final integrated diagnosis (morphology, IHC, history, clonal comparison). The label is the
   pathology report's metastasis note plus a re-review (`Clinical Path`, `PATH II`), worded "possible".
3. Row = decision: one tumour per patient matches one case, but most of the 111 primaries are patients with no prior
   cancer ("Adenocarcinoma w/ no history or path indicating non adeno"): nobody asks the question for them. Which
   primaries had a prior cancer is not recorded.
4. Would I use it? Not as a decision tool: an mRNA replay of an IHC panel on a dead platform. Ten unfitted marker genes
   0.819 against 0.887. I would trust it only on the cases IHC leaves open (mucinous/enteric lung adenocarcinoma vs
   colon; GATA3+/ER+ lung vs breast); the data holds one or two (AD350). NCCN rates RNA tissue-of-origin tests "not
   recommended"/category 3 even in CUP; GEFCAPI 04 showed no PFS gain.

**Gaps, ranked**
| # | Gap | Effect | Rule |
|---|---|---|---|
| 1 | Label = pathologist's reading of the same specimen plus history, not a resolved origin | partly a cross-check of a reading of the slide; only the history part is outside the specimen, and it is not an input | USE-1 (amended), USE-5 |
| 2 | Population: all resected adenocarcinomas, not patients with a prior cancer; prior-cancer status of primaries unrecorded | most ROC pairs are metastasis vs a primary in a patient with no prior cancer; 13% prevalence is not the setting's (~79% of solitary nodules after a prior cancer are malignant, many primaries) | USE-8, USE-5 |
| 3 | Moment/input: whole-tumour array of a resected specimen | a second opinion not ordered in practice; the value lies in IHC-ambiguous cases, hardly present | USE-3, USE-4 |
| 4 | The always-known input (which prior cancer, its histology/IHC) is missing | the model works blind of the facts the label was set from | USE-6 |
| 5 | Soft breast/other flags ("?Br MET" x3; "ad 5.0 m BAC") | about half the positives are hedged; colon ranks at percentile 0.93, breast/other ~0.70 | USE-5 |
| 6 | One centre, 1990s tissue, HG-U95Av2 | portability gap, not an exclusion | USE-8 |

**New finding: where the flags come from (affects claim 9)**
Cross-tab of DATASET B `CLUSTERS/Expression Signature` against the flags: the colon-metastasis cluster `CM` (with
`CM/sq`) holds 10 numbered patients: 7 with `Colon Met` (AD202, AD221, AD241, AD285, AD314, AD340, AD384), 2 with
`other met` (AD218, AD043), 1 unflagged (AD320); plus 2 dropped `A` patients (AD5, AD7). This matches the paper (12 in
the cluster, 10 with a history, 7 previously diagnosed colon). The 8th colon flag, AD350, is outside the cluster
(cluster blank; `Path I` "BAC/MUCIN", `PATH II` "adm w/muc"): claim 9 ("one colon flag may come from the clusters") is
not supported. Weak flags instead: AD350 (mucinous BAC-pattern tumour, the textbook lung mimic of colon) and AD218
(`other met`; clinical note "ad 5.0 m BAC" with no metastasis; only `PATH II` adds "ad w met?"; sits in the colon
cluster: the one flag that may come from the clusters). Suggested: reword claim 9 and the record's known-gaps bullet;
no rows change under issue 8 A.

**What an expert would change**
Restrict to patients with a documented prior extrapulmonary cancer and add its type as input (not possible with the
release): name this as the main gap in `fit_reason`. Say the label is the pathology report's call on the same tumour.
The post-resection second opinion is IHC then NGS; an array comes third if at all. Keep fit approximate (domain view:
nearer none than direct; actor and decision real, label and population proxies).

**Metric**
Per-patient binary decision with a case-dependent threshold; no source fixes cost or threshold (MET-6, MET-7). A
calibrated probability (log loss/Brier, MET-8) would be ideal but calibration at 13% over all resections does not carry
over; ROC AUC is prevalence-free and more honest here; average precision not warranted (MET-9). Partial fit (MET-1):
ROC AUC ranks flagged tumours against mostly irrelevant primaries. Keep `roc_auc` (fallback).

**Sources**
Study files (13790.pdf, SampleData.xls DATASET A/B). IHC lung vs colon: Diagn Pathol 2025 (s13000-025-01732-0); Virchows
Arch 2023 (s00428-023-03583-w); PMC5156892; WebPathology enteric adenocarcinoma; Mod Pathol 2019 (s41379-019-0207-y);
Front Oncol 2025 (fonc.2025.1726695). Breast vs lung: PMC7840265; Mod Pathol 2010 (modpathol201038); PMC11352534.
Molecular comparison: Oncologist 2017 (PMID 28193735); JTO CRR 2021; PeerJ 2024. Tissue-of-origin tests: ESMO GEFCAPI
04; ASCO Post 2019; NCCN Occult Primary 2016 and v3.2014; FEP policy 20454. Nodules after prior cancer: PMC9048528;
WJSO 2021 (s12957-021-02131-7); WJG 2008 v14 i6 969.

</details>

<details><summary>Blind review</summary>

**Lung adenocarcinoma metastasis (Bhattacharjee 2001, GSE83227): panel review**

**Verdict: include with changes.** The task is real and has signal that is not trivial. But the label is a *suspicion* of metastasis, and for some tumours that suspicion was formed or firmed up from the same expression profiles the model sees. Only 16 positives make up three different kinds of metastasis, so the score is very noisy. Describe the label honestly and keep the dataset's weight low.

**Data at a glance**

| Item | Value |
|---|---|
| Rows x features | 127 x 12,625 (HG-U95Av2 MAS5 signals, raw scale 0.1-165,731, no missing values) |
| Target | 111 primary lung / 16 metastasis from another organ (12.6%) |
| Source flags (SampleData.xls, DATASET B) | Colon Met 8, Breast 4, other met 4 = 16 "possible mets"; 139 AD in total, 123 "w/ no history or path indicating non adeno" |
| Rows missing vs the source | 139 - 127 = 12 primaries. 10 of them (AD1-4, AD10, AD15, AD16, AD18, AD19, AD31) have no pathology entry in DATASET B. I could not identify the other 2 because rows carry no IDs |
| Near-duplicate arrays | none: highest gene-centred row-to-row correlation 0.46 (median 0.18). Technical replicates in the source have R² > 0.9 |

**Baselines (Slurm, 20 x 3-fold stratified CV, log2 of signal floored at 20)**

| Model | ROC AUC (mean ± sd) | Average precision |
|---|---|---|
| L2 logistic regression, all probes | 0.853 ± 0.110 | 0.714 |
| Random forest, 500 trees | 0.867 ± 0.101 | 0.710 |
| LightGBM | 0.852 ± 0.101 | 0.690 |
| Best single probe (in-sample, optimistic) | 0.88 | - |

Out-of-fold logistic regression percentile of each positive among the test negatives: 1.00, 1.00, 1.00, 1.00, 0.99, 0.99, 0.99, 0.98, 0.96, 0.96, 0.92, 0.91, 0.84, 0.70, 0.33, 0.08. About 10 positives separate almost perfectly; these are likely the intestinal (colon) cluster. The rest are hard, and 2 look like primaries.

**Concerns, most serious first**

1. **The label is partly circular, unconfirmed suspicion.**
   - The sheet calls the positives "possible mets".
   - The paper (PMC61120) gives two sources for the suspicion. Methods: suspected "based on clinical history". Results: clustering "identified suspected metastases of extra-pulmonary origin, including some that were previously undetected", and "only seven samples had been previously diagnosed as metastases of colonic origin". The sheet nonetheless flags 8 colon metastases.
   - Several pathology entries read like a second look prompted by the expression results: "adm probably colonmet", "adm,acinar?met prob br" (AD163, which the paper names for its non-lung signature), "ad w met?" and "(met)". The column next to the flags is the expression cluster (CM = colon-met cluster).
   - Part of the target was therefore set from the expression data that is scored, and none of it was confirmed by IHC or a known primary.
   - Change: keep only flags that rest on clinical history or pathology made before the arrays were run, if they can be separated out. Otherwise describe the target as "suspected metastasis (clinical/pathological, partly informed by expression clustering)" and record possible label leakage.
2. **Too few, mixed positives.**
   - The 16 positives are 8 colon, 4 breast and 4 "other". The "other" ones are labelled only "(met)".
   - Each 3-fold test set holds about 5 positives, so the AUC sd across splits is 0.10-0.11, larger than any gap between the models.
   - The colon metastases are nearly trivial (galectin-4, CEACAM1, CDH17 according to the paper); the others are hardly learnable.
   - Change: give the dataset low weight in aggregates, or consider a colon-met vs primary target. Report the noise.
3. **The use case is real but dated.**
   - Telling a lung primary from a metastasis at diagnosis, on the resected specimen, is a genuine pathology decision that drives staging and treatment.
   - Today it is made with IHC (TTF-1, napsin A, CDX2, CK7/CK20, GATA3) and the clinical history, not with 12k-probe arrays. As a high-dimensional, low-n expression task it is still representative.
4. **Split.**
   - IID stratified is right: one array per tumour, no duplicates found.
   - The source has IVT batches 1-10. I could not test whether batch tracks the label, because the rows carry no IDs.
5. **Preparation.**
   - The MAS5 signals are not logged (0.1-165k). Consider log2 with a floor, or document that the raw scale is intended.
   - The AFFX control probes (spike-ins, murine and bacterial controls, housekeeping 3'/5') are not tumour biology. Consider dropping them.

**What I could not check**

- The row-to-sample mapping. Without it I could not tell which metastasis type each positive is, which 2 extra primaries were dropped, or whether batch is confounded with the label. It would need matching against the 254 GSM files.
- Whether each flag came before or after the clustering. The sheet gives no dates.
- The bundled PDF could not be rendered here. I read the paper on PMC instead.
- The single best probe was not evaluated with the probe chosen inside each fold: that job did not finish in time. Tuned models and foundation models were not run.

Note: a repository CLAUDE.md was shown to me automatically when a shell command ran inside the repo. I did not use it.

</details>

<details><summary>Task gamer</summary>

**Task gamer: lung_adenocarcinoma_metastasis (2026-11-11)**


**Verdict:** inside the kit the task barely games: no attack beats the honest L2 LR (AUC 0.854) by more than
random-column noise, except an 18S-rRNA handling artefact (+0.007, within noise). Outside the kit it games completely:
every row is byte-identical to a public GEO array with a published label (lookup AUC 1.000). The bigger problem works
against honest models: about half of the 16 positives are uncertain calls ("?Br MET", "(met)") that look like lung
primaries in expression, and one negative clusters with the colon metastases.

**Honest baseline (60 shipped splits)**
| Model | Mean AUC | SD | Min | Max |
|---|---|---|---|---|
| L2 LR, C=1, log2(max(x,20)), standardised | 0.8535 | 0.091 | 0.638 | 0.995 |
| LightGBM untuned, raw | 0.8196 | 0.104 | 0.600 | 1.000 |
| LR + one random column (5 seeds), means | 0.8530-0.8544 | | | |
| LightGBM + random column, means | 0.8192-0.8199 | | | |
Random column: LR mean moves 0.0014, per split -0.038 to +0.060. One positive moves a split's AUC ~0.05.

**Exploits**
| # | Exploit | Script | Honest | Exploited | Gain (range) | Deployed model has it? | Fix |
|---|---|---|---|---|---|---|---|
| 1 | Public-label lookup: each row = a GEO MAS5 array exactly; SampleData.xls flag = target on 127/127 | match_arrays.py, annot_join.py, label_noise.py | 0.8535 | 1.0000 | +0.147 (+0.005 to +0.362) | No | public data; document; noise blocks exact match, correlation still works |
| 2 | 18S rRNA control probes (AFFX-HUMRGE/M10098) blended at rank weight 0.25 with gene-only LR | rrna_stack.py | 0.8535 | 0.8605 | +0.007 (-0.049 to +0.060; better 34/60) | yes on the array; link to label via handling | none needed (within noise); document |
Signal, not exploits: correlation kNN-5 label as LR feature 0.8952 (+0.042); LR on within-array ranks 0.8597 (+0.006).

**Flaws that hurt an honest model**
1. Uncertain positives: label is the union of Colon Met / Breast / other met from notes ("MET COLON", "c/w colon met",
   "?Br MET", "(met)", "ad w met?"); paper says 12 history-suspected, sheet flags 16. Honest LR OOF separates the 8 colon
   positives at AUC 0.953, the other 8 at 0.757. Most primary-like positives: AD178 rank 126 of 127 "(met)"; AD172 86
   "?Br MET"; AD350 62 (colon-flagged, outside CM); AD186 24 "?Br MET". Dropping the 8 uncertain positives from training
   lowers the score (0.8535 -> 0.8391).
2. Probable missed metastasis: AD320 labelled primary, in CM, 4th-highest OOF score (0.68). AD224 (negative, PATH II "ad
   m met?") coded inconsistently with AD218 (positive, "ad w met?").
3. Excluded rows: 12 unannotated adenocarcinomas (AD1-5, AD7, AD10, AD15, AD16, AD18, AD19, AD31); AD5, AD7 in CM;
   no sign the exclusion biases the rest.
Mildest fix: document the target as pathology-suspected metastasis (8 confident colon, 8 uncertain), or restrict
positives to confident calls with the uncertain ones unlabelled; never relabel from expression.

**Mechanisms**
- Lookup: GEO publishes all 254 MAS5 files; unique match (next array >= 53,000 summed abs diff on 500 probes);
  caArray tarball holds the flags.
- rRNA: M probe AUC 0.784; LR on three HUMRGE probes 0.737; strongest on uncertain positives (0.873) vs colon (0.694);
  partly batch (high in IVT 1, 3, 10: metastasis share 23%, 13%, 17%; low in 4, 8: 11%, 7%); persists within batch
  (0.71-0.94; 0.748 batch-centred). GEO %present lower in metastases (0.72), kit-only statistics capture little
  (0.52-0.59). Removing all AFFX costs the baseline 0.0014 (0.8535 -> 0.8521).
- Biology: MYB 0.883, GPA33 0.878, CDH17 0.81, CDX2 0.79, SLC26A3, ASCL2, HSD11B2; lung genes reversed (NKX2-1 0.22,
  SFTPB 0.27, AQP3, WFDC2, LPCAT1); matches the paper's markers. Best single probe chosen on training rows 0.661.

**Nothing found**
| Attack | Score | vs 0.8535 |
|---|---|---|
| Formats (one decimal, no NaN/negatives, min 0.1; integer fraction 0.1004 vs 0.1002) | n/a | none |
| Array-artefact statistics only, LR / LGBM | 0.519 / 0.591 | ~chance |
| LR genes + artefact statistics | 0.8520 | -0.0015 |
| All AFFX only, LR / LGBM | 0.663 / 0.633 | weaker |
| Spike-in/foreign controls only | 0.561 | ~chance |
| 3'/5' ratios | 0.511 | chance |
| MAS5 trimmed mean 500 +- 0.1 both classes | n/a | none |
| Row position | 0.496 | none |
| Copies (NN correlation 0.77-0.94; replicates 0.91-0.97) | n/a | none |
| Train+test standardisation / quantile normalisation | 0.8548 / 0.8541 | +0.001 |
| Test fold centred on itself | 0.8438 | -0.010 |
| Adversarial train-vs-test (12 splits) | 0.491 (0.36-0.57) | IID |
| Depth-2 tree | 0.741 | worse |
| Correlation kNN k=3/5/9 | 0.791/0.794/0.822 | worse |
| IVT batch number / specimen number | 0.451 / 0.428 | none |
| Post-prediction columns | n/a | none exist |

**Could not check**
Source of the rRNA difference (no dates); who made the uncertain calls and whether any flag followed the clustering;
raw CEL and scan dates (RPT dated 12/06/2002, likely re-export); a cleaned-label score; published criticism (none found;
Kerkentzes et al. 2014 call the group "suspected", n = 13).
Sources: GEO GSE83227 and caArray tarball; Bhattacharjee 2001 (PMC61120); Kerkentzes et al. 2014 Front Oncol; GPL8300.

</details>

<details><summary>Precedents</summary>

**Precedent check: lung_adenocarcinoma_metastasis (2026-11-11)**


Most calls follow precedent. Two need the curator: the use-case reason as written ("a work-up separate from the
arrays") sets nothing apart from the two labels retired under the same rule (decision 1); a population gap named in
`fit_reason` carries no `Selection Bias` marker where siblings do (decision 5). Three smaller mismatches (7-9); the
sheet corrects one stated gap (under 4).

**Verdicts**
| # | Decision | Rule(s) | Verdict | Closest precedents |
|---|---|---|---|---|
| 1 | Kept on the use case: label from a separate work-up | USE-1 (amended), USE-2 | departs, stated reason only partly holds | lung_cancer (retired 2026-11-10), glioma_grading (retired 2026-10-26), ljubljana_primary_tumor (kept 2026-11-11) |
| 2 | Not Too Small (16 pos, 5-6 per fold) | TP-5, TP-8 | consistent | musk; TP-8 row 2026-10-12; parkinsons (retired) |
| 3 | Not Trivial (unfitted 10-gene panel 0.819 vs RF 0.887) | TP-4 | consistent | audiology, ljubljana_breast_cancer (retired: rule = methods); thyroid_discordant, sepsis_survival (kept) |
| 4 | Soft label kept, fit approximate | USE-5, USE-8 | consistent; departs from regensburg for a reason that holds | differentiated_thyroid_cancer_recurrence, diabetes_3; regensburg (retired 2026-11-06) |
| 5 | No Selection Bias though fit_reason names a population gap | USE-8, Selection-bias pattern | departs without stated reason | ljubljana_primary_tumor, gcm_multiclass_cancer, sarcoma, eryhemato |
| 6 | New record | PROV-14, PROV-7, PROV-6 | consistent (Cases row could name PROV-7) | corporate_credit_rating, coad, aeolus |
| 7 | Notes name "record marker Class-dependent Recording"; record has none | marker vocabulary | record and definition disagree | tcga_coad_molecular_subtype, aeolus_rebuilt don't inherit parent markers |
| 8 | Timeless but no `Samples: No Time Dimension` tag | SPLIT-32 | record and definition disagree | parent and every Timeless definition checked |
| 9 | Licence "None" for a GEO deposit | provenance | sibling recorded differently | lung_cancer_epithelial_genexp (GSE4115) says "Public Domain" |
| 10 | ROC AUC fallback | MET-8 | consistent; the reason given is not the rule's | MET-8 binary fallback |
| 11 | 12 A patients dropped | USE-5 | consistent, checked (all 12 have blank pathology text) | regensburg logic |
| 12 | Random stratified split, Timeless | SPLIT-3, SPLIT-32 | consistent | lung_cancer issue 3; ljubljana |

No third exception, no single-curator drift. The turn from issue 6 (too small) to issue 7 (kept) has a measured reason.

**1. USE-1**
Amended rule: "A label read from the same specimen the features measure, and settled before they are taken, leaves
only a cross-check of a known label and fits no decision. A label found by a separate work-up is ground truth."
Sheet (DATASET B `Clinical Path w tumor size (cm)`): 15 of 16 flags are in the resected tumour's own pathology report
("c/w colon met", "MET COLON", "?Br MET", "(met)"); AD218 only in the study's second read (`PATH II` "ad w met?"); no
clinical-history column exists (the paper's Methods are the only source for the history). The retired histology and
glioma grade were also pathology reports on the measured specimen, made before and apart from the arrays: the rule's
line is the specimen, not the arrays. What really sets this apart: the call is unsettled ("c/w", "?"; source:
"difficult to distinguish"), part of it (a prior cancer) comes from outside the specimen, and the source names the
decision. ljubljana is a weaker match than the Cases row suggests (site found for every patient vs a suspicion).

**2. Size**
| Dataset | Smaller class | Per fold | Verdict |
|---|---|---|---|
| parkinsons | 8 people | 2-3 | retired, unstable ranks |
| musk | 39 molecules | 13 | kept |
| TP-8 row (ljubljana, sarcoma, forensic_glass, mic) | 9-14 | 3-5 | kept |
| this | 16 | 5-6 (~200 pairs) | kept; no flag, Kendall's W 0.47 |
colon_tumor and srbct_prediction `Too Small` are old verdicts without probes: no precedent.

**3. TP-4**
Panel 0.819 vs RF 0.887 (+0.068, SE 0.013): the kept side. The leak probe's "best single probe 0.86" picks among all
probes on all rows; the record rightly cites 0.663 (chosen per training side).

**4. Soft label**
Consistent with thyroid recurrence and diabetes_3. Regensburg differs: its label was the surgeon's decision and its
negatives unexamined; here all 111 negatives have a pathology report, the 12 dropped A patients have none (dropping
them follows regensburg's logic), and the pathologist's inputs are not features.
Sheet corrects claim 9: colon cluster (CM, CM/sq) 12 rows; A patients AD5, AD7 not shipped; 10 annotated; 7 colon
flags (the paper's "only seven ... previously diagnosed"); 2 `other met` (AD043, AD218); 1 unflagged (AD320); the 8th
colon flag AD350 is outside the cluster ("c/w colon met"). No colon flag looks cluster-derived; if any flag is, it is
AD218 (in the colon cluster, no clinical pathology note). Name AD218 instead of "one colon flag".

**6. New record**
Consistent (PROV-7: a new target is a distinct task). The PROV-14 Cases row cites coad and aeolus, which were retired
for damaged data with the task unchanged; PROV-7 is the fitting reason. The 2026-11-10 GEO rebuild stayed under
lung_cancer's record though PROV-14 calls new values a rebuild: moot now, noted so it is not cited as precedent.

**10. Metric**
MET-8 makes roc_auc the binary fallback regardless; the text "Metric ROC AUC: LR and LightGBM score worse than the class
shares on log loss" reads as if the measurement chose it. Keep the numbers as information, not the reason.

**Context**
sarcoma (kept) and glioma_grading (retired) sit on opposite sides of USE-1's same-specimen clause; the amended USE-1
cites glioma, not sarcoma. The wording chosen in prompt 1 also decides how sarcoma reads.

**Reflection prompts**
1. USE-1: rest the CC and Cases row on "read from the specimen's pathology but not settled there (source: hard to tell
   apart on the slide); the prior cancer comes from outside the specimen" (a, recommended); b retire like lung_cancer;
   c reopen lung_cancer and glioma; d amend USE-1 so "settled before the features are taken" decides (second Must
   amendment in two days; wait for a second case).
2. Selection Bias: a, no marker, use case = any resected lung adenocarcinoma (reword use_case/fit_reason); b, add the
   marker, fit approximate, the sheet's wording as evidence (follows ljubljana, gcm, sarcoma); c remove ljubljana's
   marker. Recommend a if any adenocarcinoma is meant, else b; use_case, fit_reason and marker must agree.
3. Drop "(record marker `Class-dependent Recording`)" from the notes, keep the bullet as history (a, recommended), or
   add the marker (b).
4. Add `Samples: No Time Dimension` (a, recommended).
5. GEO licence: keep "None" here and correct lung_cancer_epithelial_genexp to "None" as its own issue (a,
   recommended); b both "Public Domain"; c leave both.

</details>

<details><summary>Advocate</summary>

**Advocate opening brief: lung_adenocarcinoma_metastasis**

Ship after documentation fixes and two mild definition fixes.

1. USE-1/USE-2 hold (Must, P3). The source names the decision ("A key issue in lung tumor diagnosis is the
   discrimination of a primary lung adenocarcinoma from a distant metastasis to the lung"); the practitioner confirms it
   changes surgery, staging and drugs. Objection (precedent decision 1): 15 of 16 flags are the specimen's own pathology
   report, like the retired histology and glioma grade. It fails on USE-1's wording: the line is a label "read from the
   same specimen ... and settled before [the features] are taken". This one is not settled (hedged notes; source:
   "difficult to distinguish"; it depends on a prior cancer outside the specimen). Remedy: reword the stated reason
   (precedent prompt 1a); no rule change; lung_cancer and glioma stay retired.
2. The label was not taken from the arrays (EV-2). Three agents read the sheet: the 7 colon flags in CM are the paper's 7
   previously diagnosed; AD350 sits outside CM; at most AD218 may follow the clustering (PATH II only). Name AD218 in
   the known gaps; the blind reviewer could not match rows, its concern rests on the paper's wording.
3. Not trivial (TP-4). Panel 0.819 vs RF 0.887-0.894 (+0.068, SE 0.013); best single probe per training side 0.661;
   RF - LR +0.039 (paired SE 0.006), RF ahead in 19/20 repeat means. Strongest features are organ-of-origin biology (MYB,
   GPA33, CDH17, CDX2 up; NKX2-1, SFTPB reversed), as the paper names.
4. Not Too Small (TP-5); split holds (P4). 5-6 per fold, ~185 pairs; SE of 20-repeat mean 0.003 (RF), 0.005 (LR);
   between musk and the TP-8 row, above parkinsons. Batch/scan-day grouped folds score the same (RF 0.883-0.889 vs 0.884);
   adversarial 0.491; no hidden groups, no copies. Public-label lookup holds for any public dataset.
5. Recording by class (P4) real but kept with a note. Concession: claim 7 wrong (misaligned script); metastasis arrays
   call fewer genes present (0.72) and more 18S rRNA (0.78). P4 retires only an artefact that "runs through several
   features that matter and cannot be undone"; here it is separable: floor subtracted LR 0.855 -> 0.857; AFFX removed
   0.8535 -> 0.8521; quality statistics alone 0.52-0.59; %P removed from RF, colon still 0.968. Cause undecided; tumour
   content no (Spearman -0.20). Remedy: `Class-dependent Recording` marker kept with a note (also fixes precedent 7);
   correct claim 7; optionally drop the 67 AFFX (cost 0.0014).
6. Soft label and narrow population = approximate (USE-5, USE-8), not retirement. Documented flag from a named
   publication, like diabetes_3 and thyroid recurrence; unlike regensburg (all 111 negatives have a pathology report).
   Hedged positives carry signal (dropping the 8 from training lowers 0.8535 -> 0.8391); never relabel AD320/AD368 from
   expression. Population: name it in fit_reason and add `Selection Bias` (ljubljana, gcm, sarcoma; precedent 2b).
7. Fixes: drop AD355 and AD360 (USE-5; no clinical annotation; 125 rows, 16 positives, the paper's 125). Documentation:
   claim 6 = MET-8 fallback; claim 9 names AD218, AD320, AD368; explain 12 vs 16 (12 firm, 4 hedged); size section 10x3
   vs 20x3; `Samples: No Time Dimension` tag; batch sentence in splits_comment; licence stays "None".

| Part | Verdict |
|---|---|
| Validity | USE-1 holds (reason reworded); USE-5 fixed (2 rows dropped), fit approximate; LEAK, SPLIT hold; recording kept with a note |
| Value | TP-4, TP-5 hold |
| Quality | notes only |

</details>

<details><summary>Critic</summary>

**Critic opening brief: lung_adenocarcinoma_metastasis**

Position: do not ship as defined; ship after the use-case reason, the false recording claim and two mislabelled rows are
fixed, with label and population text changed. If point 1 cannot be restated with a separating fact, retire under USE-1
like lung_cancer and glioma.

1. Use-case reason does not hold as written (USE-1, Must, P3). The amended rule draws its line at the specimen, not the
   arrays. 15 of 16 flags are the resected tumour's own pathology report; AD218 only PATH II; no history column. The
   retired histology and glioma grade were also pathology calls made before and apart from the arrays, so the stated
   reason would reopen both. What separates: unsettled on the slide ("difficult to distinguish"), the prior cancer from
   outside the specimen, a source-named decision. Remedy: rewrite the reason in the CC, fit_reason and the USE-1 Cases
   row (precedent 1a); name that the 8 confident colon calls come closest to "settled before" and are the near-trivial
   part (point 6). Without that fact, retire.
2. Population (USE-8, Must; Selection Bias). Use case: a patient with a prior cancer; rows: all resected
   adenocarcinomas, most primaries "w/ no history or path indicating non adeno"; prior-cancer status unrecorded. Most ROC
   pairs are irrelevant; 13% prevalence not the setting's; the always-known input missing (USE-6). Siblings carry the
   marker (ljubljana, gcm, sarcoma, eryhemato). Remedy: add `Selection Bias`, fit approximate, fit_reason names the
   missing prior-cancer status; use_case, fit_reason and marker agree.
3. The recording claim is false (P4: LEAK-13 to 15, LEAK-39/40; EV-1, EV-2). Claim 7 came from a misaligned script.

   | Measure | Result |
   |---|---|
   | All 67 AFFX (LR) | 0.695, perm p 0.02 |
   | %P (share called present) | 0.722, p 0.01, lower in metastases |
   | 18S rRNA probe | 0.784, ~p 0.02 after 67 tests |
   | 18S, uncertain positives | 0.873 |
   | 18S, colon positives | 0.694 |
   | RF with %P removed | 0.889 -> 0.859 |

   rRNA strongest on uncertain positives: those may be found partly by handling. Remedy: correct notes (cause open); drop
   the 67 AFFX (cost 0.0014; "fix what separates the classes for non-target reasons"); decide the marker explicitly;
   document %P (in every gene, cannot be removed).
4. Label rows (USE-5, Must). Drop AD355 and AD360 (no clinical data; 125 rows as the paper). Drop AD218 as undetermined
   (only PATH II, in CM; may be read from the features; AD224 "ad m met?" coded primary: inconsistent). Never relabel
   from expression; name AD320 and AD368 as suspected primaries. Keep the three "?Br MET" (dropping them leaves ~4
   positives per fold).
5. False or misattributed statements (P5): row text "127 ... history recorded"; claim 9 (7 colon flags in CM = the
   paper's 7; AD350 outside; candidate AD218; explain 12 vs 16: 12 firm, 4 = 3 "?Br MET" + AD218); metric reason =
   MET-8 fallback (RF beats class shares on log loss 0.286 vs 0.379); size section cites 10x3 and an unreproduced paired
   SE 0.035 (shipped: RF 0.894, LR 0.855, +0.039 SE 0.006); add `Samples: No Time Dimension`; add the batch sentence to
   splits_comment.
6. Value: mostly colon vs lung (TP-4, TP-5, TP-8; weigh). Not Too Small conceded. RF OOF AUC colon 0.984, breast 0.76,
   other 0.83; panel 0.819; one positive moves a fold ~0.05. Remedy: per-subtype AUCs in the record, low weight; no data
   change.
7. Notes (P7, CLEAN-1/2): public GEO lookup (AUC 1.000) stated; linear MAS5 scale intended (LR 0.843 vs 0.855 log2);
   licence "None" vs sibling "Public Domain" as its own issue.

Not argued: feature leakage (none); the split; the new record; dropping the 12 A patients.

</details>

<details><summary>Advocate rebuttal</summary>

**Advocate rebuttal**

Concede five of seven, partly concede one, dispute one in part. Open: the retire fallback (1), reading the rRNA signal
as handling (3), dropping AD218 (4).

1. USE-1: concede the rewrite (CC, fit_reason, USE-1 Cases row); dispute the retire fallback: the separating facts are
   in the evidence ("difficult to distinguish"; hedged flags; prior cancer outside the specimen; source-named decision).
   Dispute that the colon calls are "settled before": the paper says 7 of 8 were "previously diagnosed as metastases of
   colonic origin", from the known colon cancer, a separate work-up; AD350 ("c/w colon met", mucinous) is the opposite
   of settled.
2. Population: concede in full (marker, approximate, prior-cancer status named; USE-6 a named gap, not a leak).
3. Recording: concede facts and remedies (correct notes, cause open; drop the 67 AFFX, cost 0.0014; marker kept with a
   note; document %P). Dispute "uncertain positives may be found by handling": flags come from pathology notes, so array
   handling cannot set a flag. %P does not carry the task: floor subtracted 0.855 -> 0.857; artefact statistics alone
   0.52-0.59; RF with %P removed colon/breast/other 0.968/0.718/0.782. P4 retirement condition not met.
4. Rows: concede AD355/AD360 drop; AD320/AD368 named, never relabelled; keep the three "?Br MET". Dispute dropping
   AD218: its flag rests on PATH II, a pathologist's reading; whether PATH II saw the clusters is untested (EV-1); AD224
   is the source's own coding. Name AD218 and AD224 in the known gaps. Fallback if the curator wants AD218 out: leave it
   unlabelled (drop), not recoded (15 positives, 5 per fold).
5. Statements: concede all (row text; claim 9; MET-8 fallback; size section with shipped 20x3 numbers RF 0.894, LR
   0.855, +0.039 SE 0.006; time tag; batch sentence).
6. Value: concede per-subtype AUCs in the record; non-colon positives learnable (breast 0.76, other 0.83; removing the 8
   uncertain from training 0.8535 -> 0.8391); Not Trivial rests on the whole task (panel 0.819 vs RF 0.887); low weight
   is a weigh call, no Must.
7. Notes: concede all.

Joint position: ship after USE-1 reason restated, Selection Bias and Class-dependent Recording added, 67 AFFX dropped,
AD355/AD360 dropped, documentation corrected. Only open item: AD218 (keep with note vs drop): a single-row USE-5 call
for the curator.

</details>

<details><summary>Critic rebuttal</summary>

**Critic rebuttal**

Now: ship after changes. Agreed with the advocate: USE-1 rewording, Selection Bias, fit approximate, drop AD355/AD360,
Class-dependent Recording marker, all documentation fixes. Retirement withdrawn. Two disputes remain: drop AD218 (not
only name it); drop the 67 AFFX (not optional).

1. USE-1 conceded on the specimen line; the reworded reason replaces "a work-up separate from the arrays" in the CC,
   fit_reason, the USE-1 Cases row and the "label comes from outside the arrays" bullet. Condition: say the 8 firm colon
   calls come closest to "settled before" and are the near-trivial part (colon AUC 0.984).
2. Colon flags conceded (EV-2). AD218 disputed: only PATH II "ad w met?", clinical path "ad 5.0 m BAC", in CM; AD224
   ("ad m met?") coded primary. A label possibly read off the modelled expression fails USE-5 (Must, P3); fix the
   definition: drop the row (16 -> 15 positives, still 5 per fold).
3. TP-4 conceded; report per-subtype AUCs (colon 0.984, breast 0.76, other 0.83).
4. Size, split, lookup conceded.
5. Recording: keep with the marker; %P in every gene cannot be undone; floor-subtracted 0.855 -> 0.857; correct claim
   7. Disputed: drop the AFFX firmly (measure preparation; 18S 0.784; cost 0.0014; fix what can be fixed). Cite GEO QC
   numbers (%P 0.722 p 0.01; AFFX 0.695 p 0.02), not the kit-only 0.52-0.59.
6. Approximate fit and Selection Bias conceded. Disputed: "dropping 8 hedged positives from training lowers 0.8535 ->
   0.8391" proves consistency with the noisy label, not validity (EV-1); the rRNA probe separates the uncertain
   positives at 0.873 vs 0.694 for colon. Keep the hedged calls (USE-5; dropping leaves 4 per fold), but do not cite that
   number as validity. Never relabel AD320/AD368.
7. Fixes conceded with AD218 and the AFFX drop added; licence "None" here, sibling as its own issue (5a).

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
