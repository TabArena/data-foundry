---
unique_name: hepatitis_survival_prediction
name: hepatitis
checked_by:
- Lennart
- Andrej
data_foundry_status:
- 'DF: Yes'
- BeyondArena
suggestion: 'Yes'
decision_markers:
- Outdated
tags:
- Tiny Data
- 'Samples: Over Time'
- 'Time: Lost'
- 'Target: Unknown'
- Clinical Study
collections:
- TabArena Reject
original_source: UCI
year: '1988'
collection_period: Unknown
domain: medical & healthcare
required_split:
- Random (IID)
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://github.com/EpistasisLab/pmlb/blob/master/datasets/hepatitis/metadata.yaml
- https://doi.org/10.24432/C5Q59J
- https://www.kaggle.com/datasets/abdelazizsami/hepatitis
notebook_path: datasets/beyond_iid/new_iid/hepatitis_survival_prediction/hepatitis_survival_prediction.ipynb
v2_path: datasets/_dev/tabarena-v0pt2/hepatitis_survival_prediction/dataset.py
source_row: 760
type_adapter_id: curation-record-v1
---

## Comments

Already preprocessed data but otherwise looks like a good task, need to check group and cost files but would add!

**Assessment (AI, 2026-10-21):** Metric declared under MET-1..13: fallback roc_auc — Efron & Gong 1981/1986 study how to estimate the error rate of Gregory's logistic rule on these 155 patients: a statistics-methods paper, not a decision; 32 deaths, so accuracy is coarse. Original rejected: error rate. roc_auc is the binary fallback.

CC (2026-10-21, Lennart): the metric is the roc_auc fallback; Efron & Gong's error rate is the object of a resampling study on 155 patients, not the task's metric.

CC (2026-10-21, Andrej): The rows are 155 patients with hepatitis (liver inflammation) from Stanford Medical School, collected before 1982; the label is death from the disease. I disagree with keeping it.
- **The UCI file is an altered copy of the original:** Efron & Gong print the original values of the last 11 patients (UCI rows 145-155). Histology is missing for 4 of them (3 died), but UCI codes all 4 as `2`; three lab values differ (e.g. SGOT, a liver enzyme, 193 vs 173), and the paper counts 33 deaths against 32 in UCI. The other 144 rows cannot be checked.
- Reference: Efron B, Gong G. A leisurely look at the bootstrap, the jackknife, and cross-validation. Am Stat. 1983;37(1):36-48. doi:10.1080/00031305.1983.10483087

**Assessment (AI, 2026-10-31):** better data: the data-scouting run of 2026-10-30/31 found better data for the same task: `optn_liver_waitlist_90day_mortality` (TBD -> Yes, priority 3). Each is screened in its own record; this record's verdict stays the curator's.

CC (2026-11-01, Lennart): the target rule (CLEAN-25) and the cut-end rule (CLEAN-14): the target ships as No/Yes, Yes the event (1 means the patient died (UCI: 1 DIE, 2 LIVE)).

CC (2026-11-10, Andrej): I reverse the retirement; the dataset stays (Review issues 1-3).
- **No reason for the retirement holds:** its only recorded reason, the altered-copy claim of 2026-10-21, was withdrawn, and no other reason survives a test: the unfitted Child-Pugh score reaches ROC AUC 0.811 against TabPFN 3.5's 0.887.
- `Outdated` is kept as a note: a 1970s cohort, but bilirubin, albumin, clotting and ascites are still the inputs hepatologists use, so the task is not gone. The fit stays approximate (no follow-up period stated).
- Fixes: `histology` renamed to `physician_prognosis` (missing prognoses coded 2, "live"); citation corrected to Efron and Gong 1983; the task summary names Stanford, before 1982, chronic hepatitis; the yes/no columns are coded 1 = yes.
- References: Efron B, Gong G. A leisurely look at the bootstrap, the jackknife, and cross-validation. Am Stat. 1983;37(1):36-48. doi:10.1080/00031305.1983.10483087; Diaconis P, Efron B. Computer-intensive methods in statistics. Sci Am. 1983;248(5):116-130. doi:10.1038/scientificamerican0583-116

CC (2026-11-17, Andrej): the declared split (random, 20x3 folds, `ForcedIIDFromTemporal`) is checked: the split decision tree, walked without the current split, reaches the split it ships (blind split walk).

CC (2026-11-18, Andrej): the forced tag stays (Review issue 4, A; stationarity reasoning, SPLIT-32 as amended today): no reason to take later samples as interchangeable. An old one-time study whose outcome treatment has since transformed.

## Review

**Outcome:** added; retired 2026-10-27 (`No (Retired)`), retirement reversed 2026-11-10 (Andrej, `Yes`): kept with
the prognosis column renamed and the source corrected, fit approximate, `Outdated` kept as a note. 155 patients with chronic hepatitis seen by Peter Gregory at Stanford
Medical School before 1982 (UCI 46, via Efron and Gong); the label is death (32 died), with no follow-up period
stated. The only reason the record gives for the retirement, that the UCI file differs from Efron and Gong's table
in 11 rows, was withdrawn on 2026-10-21, and no other reason holds under the current rules (issue 1). Validity: a
real prognosis from the findings a hepatologist still uses (bilirubin, albumin, clotting, ascites); the unfitted
Child-Pugh score reaches ROC AUC 0.811, close to logistic regression (0.825), and TabPFN 3.5 beats it on 93% of
the folds (0.887). Quality: `physician_prognosis` (UCI `histology`) has the missing values merged into "live",
now documented (issue 2); the citation and the task summary now match the sources (issue 3). Stationarity reasoning of 2026-11-18: the definition reaches the forced step with no time to measure; the forced
tag stays (issue 4).

**Main points:** Nothing open. Issues 1-3 resolved 2026-11-10: retirement reversed (issue 1), `histology` renamed to
`physician_prognosis` (issue 2), citation and task summary corrected (issue 3); `ForcedIIDFromTemporal` stays (issue 4,
A, 2026-11-18).

**Record judgment:** valid source, thin documentation. The record holds Lennart's keep, Andrej's CC of 2026-10-21
(the altered-copy reason, withdrawn the same day) and `No (Retired)` of 2026-10-27 without a CC line that states
the reason; Andrej's CC of 2026-11-10 reverses it (`Yes`, `Outdated` kept as a note). PR #58 left it out, so it was never retired on main.

**Issues for Andrej:**

1. **Reverse the retirement, or retire for a reason that holds?**

   * **Problem:**
     - The record's only reason, that the UCI file differs from Efron and Gong's printed table in 11 rows, was
       withdrawn on 2026-10-21, because a few differing values neither show which copy is right nor make the task
       unreal.
     - Every other candidate reason fails a test, or the rules treat it as a note rather than an exclusion.
     - Keep the dataset, or retire it for one of the remaining reasons?
   * **Background:**
     - The patients: Efron and Gong (1983) name Peter Gregory of Stanford Medical School as the source, and Gong's
       1982 thesis calls them chronic hepatitis patients; the two treatment columns (steroids, antivirals) fit the
       Stanford hepatitis treatment trials of the 1970s. Neither source gives the follow-up period, nor when the
       findings were recorded.
     - The better data the scouting run of 2026-10-31 named, `optn_liver_waitlist_90day_mortality`, is another
       population (adults on the US liver transplant waiting list, ranked by MELD), on request only and not screened.
       It does not replace this task.
   * **Experiments:** ROC AUC over the definition's 60 splits (20 repeats x 3 folds, seed 4267); the Child-Pugh
     score is computed without fitting (bilirubin, albumin, prothrombin activity in percent, ascites; a missing value
     counts as normal).

     | Model or rule | ROC AUC | TabPFN 3.5 better on |
     |---|---|---|
     | Albumin alone | 0.803 | 95% of folds (+0.085) |
     | Child-Pugh score, unfitted | 0.811 | 93% of folds (+0.076) |
     | Logistic regression, all features | 0.825 | 92% of folds (+0.062) |
     | Random forest | 0.877 | 72% of folds (+0.010) |
     | TabPFN 3.5 | 0.887 | |
     | TabPFN 3.5 without treatments and prognosis | 0.895 | |

   * **The candidate reasons and what was found:**

     | Reason | Finding | Holds as an exclusion? |
     |---|---|---|
     | Altered copy of Efron and Gong | 4 missing prognoses coded "live", 3 lab values and one death differ in the 11 rows that can be checked | no: withdrawn 2026-10-21 |
     | Follow-up period not stated | true; no source gives it | no: an unstated horizon makes the fit approximate, which the definition already says[^1a] |
     | Outdated | 1970s patients and treatments; but bilirubin, albumin, clotting and ascites are the Child-Pugh inputs hepatologists use today | no: the task is not gone[^1b] |
     | Trivial | the unfitted Child-Pugh score matches logistic regression but not the stronger models (above) | no[^1c] |
     | Leak from the prognosis or the treatments | dropping them raises TabPFN 3.5 from 0.887 to 0.895 | no |
     | Too small | 32 deaths, about 11 per test fold | no: a tiny-data task like musk (13 per fold)[^1d] |
     | Redundant with cirrhosis_patient_survival_prediction | another disease (primary biliary cholangitis), 89% women against 90% men here, a 5-year horizon | no: withdrawn 2026-10-21 |
     | Duplicates | none | no |

   * **Consistency:** the precedents for a label without a stated horizon keep the dataset as approximate
     (alfa_battle_2_0_task_2, differentiated_thyroid_cancer_recurrence), and `Outdated` alone retires a dataset only
     when the task itself is gone (protein_model_quality_rf_pcp, kept with the marker as a note). Your other
     retirements of 2026-10-27 each name reasons that were tested: hepatitis_c_prediction (two undocumented
     collections; 75 patients too few to stage) and early_stage_diabetes_risk_prediction (the wrong population; half
     the rows are duplicates).
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Retired, reason as recorded (implemented) | `No (Retired)` on the CC of 2026-10-21; PR #58 removes the folder | no change to PR #58 | the only stated reason is the one withdrawn |
     | B | Retire: follow-up not stated | the same, with a CC line naming the unstated horizon | the label's meaning is unknown | precedents keep such datasets as approximate; a third exception to the fit rule |
     | C | Retire: outdated task | the same, with a CC line naming what replaced the task | a 1970s cohort without the viral markers and fibrosis staging used today | the task and its main inputs are still in use; the rule needs the task to be gone |
     | D | Reverse the retirement | `suggestion: Yes`, the folder stays (PR #58 drops it from its removals), issues 2 and 3 applied, fit stays approximate | no tested reason against it; a real prognosis task where TabPFN 3.5 beats a clinical score | 155 rows from an undocumented 1970s study stay in the benchmark |

   * **Recommendation:** D: no reason survives a test or the rules, and the dataset's gaps are already written into its
     fit. **Decision:** keep retired (A), retire for the horizon (B) or as outdated (C), or reverse (D)?

   **Notes for the AI:** on D: record `suggestion: Yes` and a CC line (Andrej's words), keep `Outdated` with a note
   if he says so; remove hepatitis_survival_prediction from PR #58 (folder, record, CHANGELOG, description), so #58
   retires only early_stage_diabetes_risk_prediction; apply issues 2 and 3 and run `dataset check`. On B or C: replace
   the CC of 2026-10-21 with the reason as Andrej words it, a marker that names it (C: `Outdated` plus the record
   naming what replaced the task), and update PR #58.

   [^1a]: **USE-8** (Must): approximate fit, a stand-in with a known gap, among them a label definition the sources do
     not settle (no stated horizon). Cases: alfa_battle_2_0_task_2.
   [^1b]: **SEL-18** (Should): `Outdated` alone does not leave a dataset; it is an exclusion only when the task is
     gone, when no one would make that prediction today or never from these inputs.
   [^1c]: **TP-4** (Must; as amended in PR #57): a feature or unfitted rule that beats the methods proves `Trivial`;
     one that matches them makes the dataset a candidate to drop.
   [^1d]: **TP-5** (Must): `Too Small` means a handful of units of a class per test fold; a small dataset as such is a
     tiny-data task like the others.

   **Resolved (2026-11-10, Andrej):** D: reverse the retirement. The record has `suggestion: Yes` and a CC line (the
   only recorded reason, the altered-copy claim of 2026-10-21, was withdrawn; no other reason holds, Child-Pugh 0.811
   against TabPFN 3.5 0.887; `Outdated` kept as a note). The fit stays approximate and the folder stays; issues 2 and 3
   applied, `dataset check` passed.

2. **What to do with the column called `histology`, which is the physician's prognosis?**

   * **Problem:**
     - Diaconis and Efron (1983) print this column for patients 149-155 as "physician's prognosis" (live or die), not
       a biopsy result, and the missing prognoses are coded 2 ("live") in the UCI file.
     - Code 1 has 7 deaths in 85 patients and code 2 has 25 in 70, which runs backwards for a prognosis, so the codes
       cannot be read with confidence.
     - Keep it as it is, rename and document it, or drop it?
   * **Effect on the task:** none measurable; the physician's guess is information a model at the bedside could have,
     but its coding is unreliable.
   * **Experiments:** TabPFN 3.5 over 60 splits: with the column 0.887, without it 0.888. The column alone reaches ROC
     AUC 0.71; the missing-value indicators alone 0.50.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep as `histology` (implemented) | as UCI ships it | no change | a wrong name and description; the merge of missing values is hidden |
     | B | Rename and document | `physician_prognosis`, values as recorded, the merge and the reversed codes noted in the curation comments | the column says what it is; minimal change | still carries the merged missing values |
     | C | Drop it | the column leaves the features | no column whose meaning is unclear | removes a recorded input, though without measurable loss |

   * **Recommendation:** B: the column is a legitimate input with a known coding problem, and documenting it changes
     no values. **Decision:** keep (A), rename and document (B) or drop (C)?

   **Notes for the AI:** on B, rename in `_load_raw`, update `_feature_types`, add a curation-comments bullet citing
   Diaconis P, Efron B. Computer-intensive methods in statistics. Sci Am. 1983;248(5):116-130,
   doi:10.1038/scientificamerican0583-116, and change the `known` field of the task summary.

   **Resolved (2026-11-10, Andrej):** B: rename and document. `histology` is `physician_prognosis` in `_load_raw` and
   `_feature_types`, values as recorded; a curation-comments bullet notes the missing prognoses coded 2 and the
   reversed death rates, citing Diaconis and Efron 1983 (Sci Am); `known` names the physician's prognosis.
   `dataset check` passed.

3. **Correct the source, the citation and the description of the patients?**

   * **Problem:**
     - The definition cites Efron and Gong's 1981 conference talk, whose abstract does not mention the hepatitis data,
       while the record cites their 1983 paper that prints part of it.
     - The task summary says place and period are not stated and lists the biopsy's histology, while the sources name
       Stanford, before 1982, chronic hepatitis patients and the physician's prognosis.
     - `ascites` = 1 means yes (14 of 20 died), the reverse of the order the UCI names file lists ("no, yes").
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | As it is (implemented) | no change | none found | the definition describes the data wrongly |
     | B | Correct | `bibtex` to Efron and Gong 1983; the task summary names Stanford, before 1982, chronic hepatitis; a note on the ascites coding | the definition matches its sources | none found |

   * **Recommendation:** B. **Decision:** A or B?

   **Notes for the AI:** on B: `bibtex` = efron1983leisurely (as in the record's `## Reference`), task summary `row`
   and `known`, a curation-comments bullet for the ascites coding (and the other yes/no columns, coded 1 = yes per
   Diaconis and Efron's table), then `dataset check`.

   **Resolved (2026-11-10, Andrej):** B: correct. `bibtex` is efron1983leisurely; the task summary's `row` names
   chronic hepatitis patients at Stanford Medical School before 1982 (Efron and Gong 1983), `known` and `use_case` no
   longer name a biopsy; a curation-comments bullet says the yes/no columns, `ascites` among them, are coded 1 = yes
   (Diaconis and Efron's table), the reverse of the UCI names file's order. `dataset check` passed.

4. **Keep `ForcedIIDFromTemporal`, or tag `AssumedStationaryRelation`?**

   * **Problem:**
     - Time: Lost: 155 patients described by Efron and Gong 1981; place, period and follow-up unstated; no date or order.
     - Use: A physician estimates hepatitis prognosis today, 45+ years after collection.
     - Mechanism: Bilirubin, albumin, prothrombin, ascites, varices to death: liver physiology, but survival given them depends on treatment (antivirals, transplantation), which changed completely; two inputs are treatments.
   * **Background:** similar datasets[^asr].

     | Similar dataset or source | What was measured | Verdict | Why similar |
     |---|---|---|---|
     | cirrhosis_patient_survival_prediction (Mayo PBC) | v3 test over rebuilt two-year registration periods 1974-81 | inconclusive (counts as unmeasured) | liver-disease prognosis from lab values, small single-centre cohort |
     | AASLD-IDSA HCV guidance (2014 onward) / HBV nucleos(t)ide antivirals (literature, cited from memory: check) | curative or suppressive antiviral therapy introduced | changed treatments | chronic viral hepatitis prognosis |

   * **For a stationary use case:**
     - the physiological severity markers are those of Child-Pugh, still in use.
   * **Against:**
     - ~45-year span.
     - treatments changed (antivirals, transplant) and are inputs.
     - follow-up period unknown.
   * **Earlier views:**
     - CC 2026-11-17 (Andrej): random 20x3 checked by blind walk.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep `ForcedIIDFromTemporal` (implemented) | The folds stay; the Time basis line names the reasoning below | Claims only what is known | The split stands for later samples only as far as the use case is stationary |
     | B | `AssumedStationaryRelation` | The folds stay; you give the reason (eight words or more) | Documents why random folds stand for later samples | ~45-year span; treatments changed (antivirals, transplant) and are inputs |

   * **Recommendation:** A, an old one-time study whose outcome treatment has since transformed. Confidence: high. **Decision:** A or B?

   [^asr]: **SPLIT-32** (Should; amended 2026-11-18, Andrej): "where it holds none, the review reasons whether the use case can be taken as stationary, from the domain's mechanism and from similar datasets ..., where the AI offers `AssumedStationaryRelation` with a recommendation for a person to decide." `AssumedStationaryRelation` keeps the forced split's folds and replaces only the tag; its line opens `AssumedStationaryRelation (<person>, <date>): <reason>`.

   **Andrej (2026-11-18, ok):** as implemented.

   **Resolved (2026-11-18, Andrej):** A, as implemented: the forced tag stays; the `Time basis:` line gives the reasoning (An old one-time study whose outcome treatment has since transformed.)

## Reference

@article{efron1983leisurely,
  title={A leisurely look at the bootstrap, the jackknife, and cross-validation},
  author={Efron, Bradley and Gong, Gail},
  journal={The American Statistician},
  volume={37},
  number={1},
  pages={36--48},
  year={1983},
  publisher={Taylor \& Francis},
  doi={10.1080/00031305.1983.10483087}
}
