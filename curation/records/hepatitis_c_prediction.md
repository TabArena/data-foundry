---
unique_name: hepatitis_c_prediction
name: Hepatitis C Prediction Dataset
checked_by:
- Lennart
- Andrej
data_foundry_status:
- 'DF: Yes'
- BeyondArena
suggestion: 'Yes'
decision_markers:
- Selection Bias
- Class-dependent Recording
tags:
- Tiny Data
- 'Samples: Over Time'
- 'Time: Lost'
- Clinical Study
collections:
- New (BeyondArena)
original_source: UCI
year: '2020'
collection_period: Unknown
domain: medical & healthcare
required_split:
- Random (IID)
problem_type: Multiclass Classification
original_data_state: One Table
source_links:
- https://doi.org/10.24432/C5D612
- https://www.kaggle.com/datasets/fedesoriano/hepatitis-c-dataset
notebook_path: datasets/beyond_iid/new_iid/hepatitis_c_prediction/hepatitis_c_prediction.ipynb
v2_path: datasets/_dev/tabarena-v0pt2/hepatitis_c_prediction/dataset.py
source_row: 771
type_adapter_id: curation-record-v1
---

## Comments

CC (2026-09-30, Lennart): **Leak fixed: donor and patient rows use different recording conventions, which gave the class away.** Share of whole-number values (donor / hepatitis / fibrosis / cirrhosis): ALB 0.11 / 1.00 / 1.00 / 0.97, BIL 0.09 / 1.00 / 1.00 / 1.00, CREA 1.00 / 0.12 / 0.57 / 0.33; ALP is missing for 0 of 533 donors but 18 patients. These four format flags alone give patient-vs-donor AUC 0.9997 and beat the full LightGBM on log loss (0.15 vs 0.27; leak audit 2026-09-24, rechecked). Fix: ALB, ALT, AST, BIL, CREA, GGT and PROT rounded to integers for all rows (median change 0.3-2.6%, worst 2.4 -> 2 in BIL; no value becomes 0) and ALP dropped; CHE and CHOL (single digits, no class difference) stay as recorded. Log loss 0.27 -> 0.35, patient-vs-donor AUC 0.997 -> 0.984; within patients the stage signal is unchanged (OvR AUC 0.80 -> 0.82). Open question answered: no exact or near duplicates (minimum standardised nearest-neighbour distance 0.20), so no evidence of several rows per patient. Class counts: 533 donors, 24 hepatitis, 21 fibrosis, 30 cirrhosis.

Need to check label distribution of class and if multiple entries per patient ID

**Assessment (AI, 2026-10-21):** Metric declared under MET-1..13: fallback log_loss — Hoffmann et al. 2018 report overall and per-class accuracy under leave-one-out; 88% donors, so accuracy is dominated by donor vs patient; the suspect-donor class is dropped (MET-2). Original rejected: accuracy. log_loss is the multiclass fallback.

CC (2026-10-21, Lennart): the metric is the log_loss fallback, as proposed; balanced accuracy, a threshold metric the paper did not choose, is not used.

**Assessment (AI, 2026-10-31):** better data: the data-scouting run of 2026-10-30/31 found better data for the same task: `nhanes_liver_elastography_fibrosis` (TBD -> Yes, priority 2). Each is screened in its own record; this record's verdict stays the curator's.

CC (2026-11-01, Lennart): the target rule (CLEAN-25) and the cut-end rule (CLEAN-14): the target is an ordered category, blood donor < hepatitis < fibrosis < cirrhosis.

**Assessment (AI, 2026-11-05):** marker `Class-dependent Recording`: donors and patients were recorded under different precision conventions (some lab values whole numbers in one group only), and ALP (alkaline phosphatase, a liver enzyme) is missing only for patients. Before the definition's rounding, bilirubin alone gives ROC AUC 0.881, and 0.954 with its number format. The definition rounds seven lab values and drops ALP. Noted in its curation comments; data unchanged.

CC (2026-11-10, Andrej): kept (`Yes`), the retirement of 2026-10-27 reversed: none of its reasons survives a test or the current rules, and the methods spread widely. 75 hepatitis C patients and 526 blood donors of a Hannover clinical-chemistry group (UCI 571); the label is donor or one of three stages (hepatitis, fibrosis, cirrhosis), four classes.
- **Donors and patients collected apart:** the rules now name this dataset as their example of cases and controls collected apart, which is `Selection Bias`, a concern flag on a kept dataset; the marker stays, and the fit stays approximate.
- **Cirrhosis partly defined by bilirubin and albumin (Child-Pugh C):** without both, TabPFN 3.5 reaches log loss 0.168 against 0.157 with them (cirrhosis against the other patients ROC AUC 0.938); the two as Child-Pugh points, unfitted, reach only 0.882, so the rest carries the signal.
- **No rule comes close:** the best unfitted rule, a count of liver values outside their reference limits, reaches log loss 0.313 against 0.157 for TabPFN 3.5, which is ahead on all 60 splits.
- **Labels unlike the paper, patients few:** UCI's 24 / 21 / 30 patients are another selection from the same Hannover study by the same authors (the paper has 31 / 22 / 20); 7 to 10 per class per test fold.
- **Changed:** ALT is dropped, recorded another way for most patients (median 4.9 to 12.8 U/L in the 57 patients with ALP recorded, below the donors' 23.1); 7 donor panels entered twice are kept once (601 rows).
Evidence: the reassessment of 2026-11-10 (60 splits, 20 x 3 folds), in the Review section (issue 1).

CC (2026-11-10, Andrej): ALT dropped, recorded another way for most patients (Review issue 2).
- **Evidence:** in the 57 patients with ALP recorded, ALT's median is 4.9 to 12.8 U/L by stage, below the donors' 23.1, while AST is raised; the 18 patients without ALP have 66 to 114 U/L, as chronic hepatitis C gives.
- **Why a drop:** a model would learn low ALT with high AST as a sign of disease, and the column cannot be repaired: neither the unit nor the method is stated. The six other rounded lab values stay rounded; ALT is no longer among them.

CC (2026-11-18, Andrej): the forced tag stays (Review issue 5, A; stationarity reasoning, SPLIT-32 as amended today): no reason to take later samples as interchangeable. Physiology supports it, but the class-dependent recording and the treatment change in HCV are facts against; mixed, so forced.

## Review

**Outcome:** added; retired 2026-10-27 (`No (Retired)`), reopened 2026-11-10: the AI recommends reversing the
retirement and keeping it with ALT dropped. 533 blood donors and 75 hepatitis C patients from the Hannover
clinical-chemistry group (UCI 571); the label is donor or one of three stages (hepatitis, fibrosis, cirrhosis). The
current rules name this dataset as their example of cases and controls collected apart, a concern flag on a kept
dataset, and no other reason survives a test (issue 1). Validity: 82% of TabPFN 3.5's log loss is the staging of the
75 patients, a task the source paper itself studies; no unfitted rule comes close (best 0.313 against 0.157).
Quality: ALT is wrong in 57 of the 75 patients (issue 2); 7 donor lab panels appear twice (issue 3). A question on `CrossSectional` (2026-11-13) was withdrawn when the prototype was dropped.

**Main points:** Nothing open. Issues 1-3 resolved 2026-11-10: the retirement reversed with four classes (issue 1), ALT
dropped (issue 2), the 7 repeated donor panels kept once (issue 3). Issue 4 was withdrawn on 2026-11-13;
`ForcedIIDFromTemporal` stays (issue 5, A, 2026-11-18).

**Record judgment:** valid source, thin documentation. The record holds Lennart's keep with the rounding fix
(2026-09-30) and the target order of 2026-11-01; Andrej's retirement of 2026-10-27 (two undocumented collections;
75 patients too few) never reached it and is replaced by the CC of 2026-11-10. `Selection Bias` and `Class-dependent Recording` are on the record. PR #58 left it out after issue 1, so it was never retired on main.

**Issues for Andrej:**

1. **Reverse the retirement, or retire for a reason that holds?**

   * **Problem:**
     - The rules now list "cases and controls collected apart" with this dataset as the example of `Selection Bias`, a concern flag whose verdict is usually still `Yes`, so the main reason of 2026-10-27 is no exclusion under them.
     - Each other reason was measured where it decides: none holds as an exclusion, and the one real artefact (ALT) is fixable (issue 2).
     - Keep the dataset, or retire it for a reason that survives?
   * **Background:**
     - The source paper (Hoffmann et al. 2018) has no donors: it selected 73 patients "from the original study
       group" of a Hannover fibrosis study (Lichtinghagen et al. 2013) and staged them by Ishak fibrosis (31 F0-F1,
       22 F2-F6) or Child-Pugh C cirrhosis (20). UCI has 24 / 21 / 30, from the same group (Lichtinghagen, Klawonn,
       Hoffmann are the UCI creators, donated 2020), so it is another selection of the same study, not a
     contradiction.
     - The format leak (whole numbers by class, ALP missing only for patients) was fixed on 2026-09-30; the format
       features left (CHOL decimals, missingness, even values) reach log loss 0.509 against the prior's 0.508.
   * **Experiments:** log loss over the definition's 60 splits (20 repeats x 3 folds, seed 4267); rules are scored
     unfitted, then calibrated once on the training side (one multinomial fit on the score) for log loss.

     | Model or rule | Log loss | Donor vs patient ROC AUC | Cirrhosis vs other patients ROC AUC | TabPFN 3.5 better on |
     |---|---|---|---|---|
     | Prior | 0.508 | 0.500 | 0.500 | 60/60 |
     | Child-Pugh points from bilirubin and albumin, unfitted | 0.423 | 0.645 | 0.882 | 60/60 |
     | Count of abnormal liver values (reference limits), unfitted | 0.313 | 0.895 | 0.896 | 60/60 |
     | Logistic regression | 0.281 | 0.952 | 0.908 | 60/60 |
     | Random forest | 0.254 | 0.973 | 0.931 | 60/60 |
     | TabPFN 3.5 without bilirubin and albumin | 0.168 | 0.986 | 0.938 | 53/60 |
     | TabPFN 3.5 | 0.157 | 0.989 | 0.944 | |

     Patients only (option D, 3 classes, same seeds): the unfitted rule comes close.

     | Model or rule | Log loss | TabPFN 3.5 better on |
     |---|---|---|
     | Prior | 1.088 | 59/60 |
     | Logistic regression | 0.813 | 49/60 |
     | Abnormal-value count plus Child-Pugh points, unfitted | 0.755 | 46/60 (+0.067, folds spread 0.132) |
     | TabPFN 3.5 | 0.688 | |

   * **The reasons and what was found:**

     | Reason (2026-10-15 to 10-27) | Finding | Holds as an exclusion? |
     |---|---|---|
     | Labels differ from the paper | another selection (24/21/30 against 31/22/20) from the same study by the same authors | no: a documentation gap |
     | Child-Pugh C cirrhosis is partly defined by bilirubin and albumin | without both, TabPFN 3.5 0.168 (cirrhosis AUC 0.938); the two as Child-Pugh points 0.882 | no: the rest carries the signal[^1a] |
     | ALT implausible in patients | 57 patients with ALP recorded: median ALT 4.9-12.8 U/L, below donors (23.1), with AST raised; the other 18: 66-114 | no: one column, fixed by dropping it (issue 2)[^1b] |
     | Hepatitis vs fibrosis separated by age only | labs without age 0.696 against the prior's 0.691 on that pair; the 4-class spread is large (above) | no: a weak sub-distinction in a task where methods spread[^1c] |
     | Patients too few | 24 / 21 / 30, so 7-10 per test fold | no: above parkinsons (2-3, retired), near musk (13, kept)[^1d] |
     | Donors a separate, undocumented collection | formats harmonised, no residual format signal (0.509 vs 0.508); donors 18% of TabPFN 3.5's loss | no: `Selection Bias`, already on the record[^1e] |
     | Donor vs patient is no real decision (hepatitis C is diagnosed by antibody and RNA tests) | true for the donor part; staging from routine blood values is the paper's task and carries 82% of the loss | no: the fit is approximate, as the definition says[^1f] |
     | A simple rule matches the models | best unfitted rule 0.313, behind TabPFN 3.5 on 60/60 | no[^1g] |

   * **Consistency:** gallstone_disease (kept, `Class-dependent Recording` after the route fix) and
     eryhemato_squamous_disease (kept, `Selection Bias`, approximate fit) are the precedents for a fixed recording
     artefact and a selected sample. prostate_cancer_detection was retired because its artefact ran through every
     feature and could not be undone; here it is one column.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Retired, reasons as recorded (implemented) | `No (Retired)`; PR #58 removes the folder | no change to PR #58 | the main reason is the rules' own example of a kept concern flag; the other reasons fail their tests |
     | B | Retire on the use case | the same, with a CC line naming the donor-vs-patient part as no decision | no clinic screens for hepatitis C with a liver panel | the staging part is a real decision and carries most of the score |
     | C | Reverse the retirement, 4 classes | `suggestion: Yes`, folder stays, issues 2 and 3 applied, both markers kept, fit approximate | no tested reason against it; methods spread widely | 533 donors from an undocumented collection stay in |
     | D | Reverse as patients-only staging | 3 classes, the 75 patients, the paper's task | the decision the source studies; no donor collection | 75 rows; hepatitis vs fibrosis has little lab signal; an unfitted rule beats logistic regression and is within the fold spread of TabPFN 3.5 |

   * **Recommendation:** C: no reason survives a test or the current rules, and the donor collection is what the
     `Selection Bias` marker already says; D would be a candidate to drop, since a rule matches the models there.
     **Decision:** stay retired (A), retire on the use case (B), reverse with 4
     classes (C) or as patients-only staging (D)?

   **Notes for the AI:** on C or D: record `suggestion: Yes`, a `CC (<date>, Andrej):` line replacing the CC of
   2026-10-27 (keep it as history if he says so), `Andrej` in `checked_by`; remove hepatitis_c_prediction from PR #58
   (the retirement commit: folder, record, CHANGELOG, description); apply issues 2 and 3 and run `dataset check`. On
   D also: drop the donor rows in `_clean`, 3 ordinal levels, the task summary and `fit_reason` rewritten, the record's
   problem stays multiclass. On B: rewrite the CC of 2026-10-27 to the use-case reason, marker `Not Representative`,
   PR #58 unchanged.

   [^1a]: **SEL-5** (Must; as amended in PR #57): a label a rule assigns from shipped columns: drop the rule's inputs
     first and test what the rest predicts; when the rest still carries a signal, the task is kept and reassessed.
   [^1b]: **LEAK-15** (Must): an artefact confined to features a practical model would not rely on is fixed (LEAK-13,
     LEAK-14, LEAK-39) or kept with a note; retirement only when it runs through several features that matter and
     cannot be undone.
   [^1c]: **TP-3** (Must): if tuned methods spread, keep the dataset. **TP-2**: a small but real signal is no reason
     to retire.
   [^1d]: **TP-5** (Must): `Too Small` means a handful of units of a class per test fold; a small dataset as such is a
     tiny-data task like the others.
   [^1e]: Selection bias (selection.md, "Selection bias"): cases and controls collected apart (`hepatitis_c_prediction`,
     `website_phishing`) are marked `Selection Bias`; the verdict is usually still `Yes` (Andrej, 2026-10-20).
   [^1f]: **USE-8** (Must): the fit is approximate when the real-world setting does not share the data's selection;
     **USE-2** (Must): only a task no decision fits is out.
   [^1g]: **TP-4** (Must; as amended in PR #57): a feature or unfitted rule that beats the methods proves `Trivial`;
     one that matches them makes the dataset a candidate to drop.

   **Resolved (2026-11-10, Andrej):** C: the retirement reversed, four classes. The record is `Yes` with a CC line of 2026-11-10 in place of the one of 2026-10-27, both markers kept, fit approximate; PR #58 no longer retires it.

2. **Drop ALT, which is wrong for most patients?**

   * **Problem:**
     - In the 57 patients with ALP recorded, ALT (a liver enzyme raised in chronic hepatitis C) has a median of 4.9 to 12.8 U/L by stage, below the donors' 23.1, while AST is raised; the 18 patients without ALP have 66 to 114 U/L, as expected.
     - So ALT was recorded differently for most patients, and a model learns "low ALT with high AST" as a sign of disease, which no laboratory would see.
     - Keep ALT as recorded, or drop it?
   * **Effect on the task:** with ALT, the scores reward an artefact on the donor-vs-patient part; without it, every
     model loses a little and the ranking stays.
   * **Experiments:** 60 splits as in issue 1.

     | Model | Log loss with ALT | without ALT | Donor vs patient AUC without ALT |
     |---|---|---|---|
     | Logistic regression | 0.281 | 0.285 | 0.946 |
     | Random forest | 0.254 | 0.268 | 0.953 |
     | TabPFN 3.5 | 0.157 | 0.193 (worse on 57/60) | 0.972 |

   * **Unknown:** what the low values are (another assay, unit or method); the source does not say, so they cannot be
     converted.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep ALT (implemented) | as recorded, rounded | no change | a recording artefact the models use |
     | B | Drop ALT | 10 features | no known artefact left; methods still spread | loses a standard liver value |

   * **Recommendation:** B: the column cannot be repaired and the task holds without it[^2a]. **Decision:** A or
     B?

   **Notes for the AI:** on B: add `ALT` to `drop_columns` in `_clean` (and out of `ROUNDED_LABS`), a
   curation-comments bullet with the batch medians, `known` in the task summary without ALT, then `dataset check`.

   [^2a]: **LEAK-13** (Must): class-specific recording conventions are harmonised; a column only one class has
     correctly is dropped.

   **Resolved (2026-11-10, Andrej):** B: ALT dropped in `_clean` (and out of `ROUNDED_LABS`), a curation-comments bullet with the medians, `known` and `changes` in the task summary updated; `dataset check` passes.

3. **Drop the second copy of the 7 donor panels recorded twice?**

   * **Problem:**
     - 7 pairs of donors (14 rows) share all 10 lab values with a different age, and 2 pairs a different sex as well; under independent values a full match is about 1 in 10^17, so each pair is one blood sample entered twice.
     - Drop the second copy of each pair, or keep both and document them?
   * **Effect on the task:** small: a copy in train and one in test makes those donors easier to recognise; donors
     carry 18% of TabPFN 3.5's loss.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep both (implemented) | 608 rows | no change | one sample counted twice, possibly across the split |
     | B | Drop the second copy | 601 rows, the later row of each pair dropped | one row per sample, as with forensic_glass | which age and sex is right is unknown |

   * **Recommendation:** B. **Decision:** A or B?

   **Notes for the AI:** on B: in `_clean`, drop the later row of each pair duplicated on the 10 lab values
   (before ALP is dropped), a curation-comments bullet, `row` count in the task summary, then `dataset check`.

   **Resolved (2026-11-10, Andrej):** B: the later row of each of the 7 donor panels entered twice is dropped in `_clean` (601 rows), a curation-comments bullet replaces the old "no duplicates" one, `row` and the class shares in the task summary updated.

4. **`CrossSectional` instead of `ForcedIIDFromTemporal`?**

   * **Problem:**
     - The definition is tagged `ForcedIIDFromTemporal`, a forward use case whose time was lost[^fo-1].
     - The target is a present state measured with the features: the person's liver state (blood donor, hepatitis, fibrosis or cirrhosis), read from the same blood sample, and the use case reads it for new units at their own present[^cs-1].
     - The tag alone changes: the split stays random.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Stay `ForcedIIDFromTemporal` (implemented) | the tag and its line stay | the decision stands | the tag claims a forecast the use case does not make |
     | B | `CrossSectional` | the tag and a `Time basis:` line naming the present state, the untested drift for later units and what a dated release would show | names the use case; no claim of a lost forward split | a new prototype on a decided tag |

   * **Recommendation:** B. **Decision:** A or B?

   **Notes for the AI:** on B, swap the tag, write the line, add a CC line; the split does not change.

   [^cs-1]: **SPLIT-32** (Should, 2026-11-13): a target measured together with the features, which the use case reads for new units at their own present, is `CrossSectional`, whether the dates survive or not; its line says whether the drift of the relation was measured or is untested. A label that only arrives later is no present state.
   [^fo-1]: **SPLIT-8** (Must): a forward use case without usable time ships in the closest regime, tagged forced from temporal, with a `Time basis:` line naming the reason.

   **Resolved (2026-11-13, Andrej):** withdrawn: `CrossSectional` was dropped the same day (it named no split the existing prototypes do not give: a present state used later is forced or a measured `StationaryRelation`, used within the covered time `Retrospective`). The tag stays.

5. **Keep `ForcedIIDFromTemporal`, or tag `AssumedStationaryRelation`?**

   * **Problem:**
     - Time: Lost: no date or order; place and period not stated (Hoffmann et al. 2018, Hannover lab data).
     - Use: A laboratory physician flags liver state from a blood panel for people seen today, an unknown span after collection.
     - Mechanism: AST, GGT, cholinesterase, albumin, bilirubin reflect hepatic inflammation and synthetic function, physiology read by standard assays; but the classes are two groups recorded apart (donors vs patients) and the HCV patient population changed with DAA cure since 2014.
   * **Background:** similar datasets[^asr].

     | Similar dataset or source | What was measured | Verdict | Why similar |
     |---|---|---|---|
     | thyroid_discordant_archive | four-month request-date windows 1984-87; class share by quarter | not flat by recording: discordant share 4.4% in 1986Q3 vs 1.3-2.8%, fewer tests ordered from late 1985 (windows within 0.01 ROC AUC of random) | lab-panel diagnosis; shows ordering/intake practice moving within three years |
     | Davis SE et al., 'Calibration drift in regression and machine learning models for acute kidney injury', JAMIA 2017;24(6):1052-1061 (literature, cited from memory: check) | VA hospital models over 9 years | discrimination stable, calibration drifted | routine-lab clinical risk model used years after fitting |
     | Prati D et al., 'Updated definitions of healthy ranges for serum alanine aminotransferase levels', Ann Intern Med 2002;137:1-10 | ALT healthy range in blood donors | reference ranges depend on the population and its era (BMI) | donor lab values as the control group |

   * **For a stationary use case:**
     - the lab-to-fibrosis physiology is stable.
     - the stage task within patients rests on fixed assays.
   * **Against:**
     - donor and patient rows recorded with different precision and ALT methods (Class-dependent Recording): changed coding/intake.
     - DAA therapy since 2014 changes who presents with HCV and at which stage.
     - period unstated, so the span is unknown.
   * **Earlier views:**
     - Resolved 2026-11-13 (Andrej, issue 4): CrossSectional withdrawn, forced tag stays.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep `ForcedIIDFromTemporal` (implemented) | The folds stay; the Time basis line names the reasoning below | Claims only what is known | The split stands for later samples only as far as the use case is stationary |
     | B | `AssumedStationaryRelation` | The folds stay; you give the reason (eight words or more) | Documents why random folds stand for later samples | donor and patient rows recorded with different precision and ALT methods (Class-dependent Recording): changed coding/intake; DAA therapy since 2014 changes who presents with HCV and at which stage |

   * **Recommendation:** A, physiology supports it, but the class-dependent recording and the treatment change in HCV are facts against; mixed, so forced. Confidence: medium. **Decision:** A or B?

   [^asr]: **SPLIT-32** (Should; amended 2026-11-18, Andrej): "where it holds none, the review reasons whether the use case can be taken as stationary, from the domain's mechanism and from similar datasets ..., where the AI offers `AssumedStationaryRelation` with a recommendation for a person to decide." `AssumedStationaryRelation` keeps the forced split's folds and replaces only the tag; its line opens `AssumedStationaryRelation (<person>, <date>): <reason>`.

   **Andrej (2026-11-18, ok):** as implemented.

   **Resolved (2026-11-18, Andrej):** A, as implemented: the forced tag stays; the `Time basis:` line gives the reasoning (Physiology supports it, but the class-dependent recording and the treatment change in HCV are facts against; mixed, so forced.)

## Reference

@article{hoffmann2018using,
  title={Using machine learning techniques to generate laboratory diagnostic pathways—a case study},
  author={Hoffmann, Georg and Bietenbeck, Andreas and Lichtinghagen, Ralf and Klawonn, Frank},
  journal={Journal of Laboratory and Precision Medicine},
  volume={3},
  number={6},
  year={2018},
  publisher={AME Publishing Company}
}
