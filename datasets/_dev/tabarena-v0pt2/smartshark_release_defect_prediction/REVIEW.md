# smartshark_release_defect_prediction

**Outcome:** added. File-level defect prediction for 280 releases of 38 Apache Java projects (Herbold et al.,
EMSE 2022, the IND-JLMIV+R labels of the authors' Zenodo kit): 113,066 file-release rows x 3,260 static, warning and
six-month history measures; the target is a validated bug present at the release and fixed in the file within a year
(3.6%); grouped by project, the source's cross-project design; fallback ROC AUC. The AI recommends shipping it.
Already changed after the panel: file ages in whole months and the release by its year, labels from each file's own
fix date, and a protocol line against linking a file to its next release. One leak stays open: a file can still be
linked to itself in the next release of its project, worth +0.046 ROC AUC; the data still allows it and only a
protocol line forbids it (issue 2).

**Main points:** Keep the left cohort cut that reads the first linked fix (issue 1); accept a protocol line, not
thinned releases, against the next-release link (issue 2); keep the `ISSUE_*` counts (issue 3); score pooled or within
release, alike with `github_pull_request_acceptance` (issue 4); accept two check warnings (issue 5).

**Record judgment:** valid, approximate fit (the one-year window and the pooled score are ours); open are the cohort
cut (issue 1) and the next-release link (issue 2). Value: file size alone equals untuned LightGBM pooled (0.783), so
models separate by little. Quality: 2,773 redundant SM aggregates (pruning optional), `_improvment` is Jira's "wish"
type, the Gini scale of `mynbou`. Weighed: source +, real use +, size dominance -, width -. Priority 3: gap 0, use
case 0, source +, shape +, risk - (fit approximate, size dominates, a protocol-only leak).

**Issues for Lennart:**

1. **Keep the left cohort cut that uses each project's first linked bug fix?**

   * **Problem:**
     - 62 releases (5,815 rows, all `No`) are dropped because their label year closed before their project's first fix linked to an issue, a date taken from the label.
     - A label-free marker exists in the kit: the project's first release whose files have any linked issue in the six months before it (the `ISSUE_*` counts, which are features).
     - The two markers agree on 54 of the 62 releases, and the label-free one drops 63 releases (6,493 rows).
   * **Effect on the task:** validity; kept, the 62 releases would add 5,815 `No` rows from years when no fix could be recorded; the label-free cut keeps 8 of them and drops 9 others.
   * **Experiments:** label-free cut (a release is dropped when its label year ends before the project's first release with a linked issue): agrees with the current cut on 325 of the 342 releases whose year closes before the 2018 cut-off; 8 dropped now are kept, 9 kept now are dropped. For 13 projects the first linked issue comes later than the first linked fix (up to 9 years for `commons-validator`), so issue links in the six-month counts start late there.
   * **Consistency:** the rule's 2026-10-21 amendment accepts a cut located by a rule that does not read the label (`caracas_cervical_cancer`, `account_debt_south_africa`, `fraud_detection_in_electricity_and_gas_consumption_1m`)[^r1]; the current cut reads it, so A departs unless the recording-start reason is written as an exception, the first of its kind.
   * **Panel:** the builder, the advocate and the domain practitioner keep A: the first linked fix dates when a project started linking issues to commits, a recording event. The critic and the precedent checker want a label-free marker or a reason that does not use the label. The mediator hands it over; it named the kit's own start date as what would settle it; the kit has one only through the issue counts, and it differs from the first fix in 17 releases, so C is not free.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | First linked fix (implemented) | drops 62 releases whose year closed before the project's first linked fix | dates the start of linking directly; keeps 8 releases C drops, where issue counts start up to 9 years late | reads the label; an exception to the amended rule, the first of its kind |
     | B | Keep every followed-up release | no left cut | no rule on the label | 5,815 `No` rows from years with no recording |
     | C | First release with a linked issue | drops 63 releases (6,493 rows) by the `ISSUE_*` counts | label-free, follows the amendment | 17 releases differ from A; for 13 projects the issue counts start later than the fixes |

   * **Recommendation:** C, which follows the amendment at the cost of 17 releases moved; A if you take the recording-start reason as an exception. **Decision:** A, B or C?

   **Notes for the AI:** on C, in `_clean` replace `recorded_from` by the date of the project's first release with any `ISSUE_*` count > 0 over its files, computed before the cohort cut, and drop releases whose `window_end` falls before it; same in `_decisions`; update the cohort bullet and `task_summary.changes`; re-run `dataset check`, the leak and group probes. The comparison is in the run folder (`panel/work_finisher/cohort_marker.py`). On A, write the exception into the record's comments: the first linked fix stands for the project's start of issue linking, a recording event.

   [^r1]: **LEAK-25** (Must): "no event" mixed with "not recorded" is a censoring bias: retire unless the recording process can be recovered; recovered includes unrecorded rows located by a rule that does not read the label, and dropped (amended 2026-10-21, Lennart).

2. **Accept a protocol line against linking a file to its next release?**

   * **Problem:**
     - Whole projects sit in one test fold with all their releases, so a participant can match a file to itself in the next release, whose change, bug-fix and issue counts cover months inside the label window.
     - The panel's fix (ages in months, the release by its year, applied) only lowers the gain from 0.053 to 0.046: the syntax-tree and size profile of an unchanged file still finds its next-release row for 77% of rows.
     - So the data still lets a participant gain 0.046 ROC AUC, about twenty times the noise, and only the protocol line, which the benchmark has to enforce, stands in the way.
   * **Effect on the task:** a participant who links rows gains 0.046 ROC AUC (0.788 to 0.834, up in 9 of 9 splits; noise 0.002); the definition's protocol line forbids it; a submission that does it scores higher unless the benchmark catches it.
   * **Experiments:** the task gamer's link re-run on the changed frame (same LightGBM, the shipped splits). Its second exploit, the release's position from the end, used the release dates and is gone with the year (not re-measured).
   * **Unknown:** how many of the 280 releases and 113,066 rows survive the 18-month thinning, and how far the link gain drops; one run of the thinning plus the link re-run would settle it.
   * **Consistency:** evaluation leaks that read other test rows are handled by a protocol line, as in `bank_marketing` and `acs_food_stamps_2014_2024_1m`[^e1]; those gain 0.003 to 0.006, this one ten times more.
   * **Panel:** the mediator, the advocate and the critic asked for the protocol line if the gain stayed above noise; nobody weighed a gain of this size.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Protocol line (implemented) | the note and the protocol line in the curation comments; ages in months, release year | keeps every release; follows the evaluation-leak rule | the benchmark has to catch a method that links rows |
     | B | Thin the releases | keep per project only releases at least 18 months apart, so the next release's six-month counts fall after the label year | removes the link's information | loses releases, number not measured (with releases often months apart, plausibly half or more); fewer releases per test project |

   * **Recommendation:** A, the rule's remedy for a leak across test rows, though at ten times the gain of earlier cases; B if you want the data itself closed, once its cost is measured. **Decision:** A or B?

   **Notes for the AI:** on B, keep per project the releases whose next kept release is at least 18 months later (greedy from the oldest), re-run `dataset check`, the leak, group and task probes and `panel/work_finisher/relink.py` in the run folder.

   [^e1]: **LEAK-9** (Should): an evaluation leak, where a model can read other test rows, is fixed in the scoring or by a protocol line the benchmark checks, not in the data; a method that learns from the test block is called out and not benchmarked.

3. **Keep the `ISSUE_*` counts, whose priority and type are as Jira held them at collection?**

   * **Problem:**
     - The 25 `ISSUE_<priority>_<type>` counts sort the issues linked in the six months before the release by the priority and type they had in 2018-2019, not at the release.
     - The kit has no history, so a retyping after the release cannot be shown or ruled out.
   * **Effect on the task:** they add 0.0016 ROC AUC, below the noise of 0.002: whatever was retyped carries little.
   * **Experiments:** one grouped run (untuned LightGBM, the shipped 9 splits) with and without the 25 columns: 0.7882 against 0.7866, higher in 6 of 9 splits.
   * **Consistency:** a soft leak of an attribute read late is kept with a note when the data shows little gain[^l1]; the across-datasets item on late-filled values covers the rule.
   * **Panel:** the column auditor and the advocate keep them with the note (the standard "prior bugs" feature, best single column 0.626); the critic wants them measured first and dropped if they matter.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep with a note (implemented) | the 25 counts stay; the note names the collection date | the prior-bug counts of the defect literature | type and priority may have changed after the release |
     | B | Drop them | 25 columns out | no attribute read after the release | loses the issue history the source uses |

   * **Recommendation:** A: the measured gain is at noise, so a late retyping cannot move the ranking much. **Decision:** A or B?

   **Notes for the AI:** on B, drop the columns starting with `ISSUE_` in `_clean` (step 4), update `task_summary.known` and the note, re-run `dataset check`. The run is `panel/work_finisher/issue_ablation.py` in the run folder.

   [^l1]: **LEAK-10** (Must): a feature holds only what existed at the prediction point; attributes looked up after the outcome are out unless the data shows they did not change.

4. **Score ROC AUC pooled over all held-out files, or within each release?**

   * **Problem:**
     - The quality-assurance team ranks the files of one release, but the pooled score also rewards telling projects and releases apart.
     - Within release, file size alone (logical lines) scores 0.821 against 0.811 for untuned LightGBM; pooled both score about 0.783.
   * **Effect on the task:** B scores the decision as the team makes it; under it the size baseline beats an untuned model, so the task would separate models by little unless tuned models gain.
   * **Experiments:** mean ROC AUC over the 261 held-out releases with both classes, against pooled, on the shipped splits (claim auditor, builder).
   * **Consistency:** B follows `protein_model_quality_rf_pcp` and `huesken_sirna_efficacy`, the two within-unit exceptions to the metric rule; this would be the third, so the rule's amendment is due[^m1]. `github_pull_request_acceptance` issue 1 asks the same question (pooled or within project); decide the two alike. The rule's change is the across-datasets item **Scoring within groups**; this issue decides only this dataset.
   * **Panel:** the advocate, the critic, the domain practitioner and the precedent checker favour B; the domain practitioner names an effort-aware score as a further option. A is the standard fallback with no new code.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Pooled ROC AUC (implemented) | one ROC AUC over all test files of a fold | standard fallback, no new code | mixes projects and releases the team never compares |
     | B | Mean ROC AUC within release | `release` kept as a scoring column, ROC AUC per release averaged | the unit the team acts on; the source scores per release | new metric code with tests; the size baseline beats untuned LightGBM |

   * **Recommendation:** B, decided alike with `github_pull_request_acceptance` issue 1; the rule's amendment is in **Scoring within groups**. **Decision:** A or B?

   **Notes for the AI:** on B, keep the release name as a scoring column (never a feature), declare the within-group ROC AUC metric with its tests, write the amendment of the metric rule (third within-unit exception), re-run `dataset check` and the task probe, and check that tuned models still separate from `SM_file_lloc` (0.821).

   [^m1]: **MET-1** (Must): the declared metric scores the real task, at the unit the actor acts on. **MET-5** (Should): a paper's metric is the source's only when it is one deliberate choice; otherwise the fallback, with the reported metrics in the reason.

5. **Accept the two check warnings, few test projects and the Gini value -1?**

   * **Problem:**
     - 38 projects leave 10 to 14 per test fold, so the check warns about few groups (group probe: 0.790 grouped against 0.927 IID, a signal across projects).
     - -1 in `SM_method_numpar_gini` (9.9% of rows) is a real value of `mynbou`'s formula (two values, one of them 0), not a missing marker.
   * **Effect on the task:** none on the data; the acceptances record why the warnings stand.
   * **Panel:** the builder, the precedent checker and the mediator accept both with the builder's texts.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Accept both with the builder's texts | both warnings accepted with the texts in the notes below (written into `dataset.py` on yes) | follows the definitions that accept few groups; the reason stays with the data | none found |
     | B | Leave them unaccepted (implemented) | the warnings stay open in `dataset check` | none found | two warnings with nothing to fix |

   * **Recommendation:** A. **Decision:** accept both warnings with these texts, yes or no?

   **Notes for the AI:** on yes, write into `accepted_check_warnings` in `dataset.py`:
   `groups_test_groups_few`: "38 Apache projects are all the source has (10-14 held out per fold), and a project without its own defect data is the use case. The signal across projects is real: random forest 0.769 and LightGBM 0.697 ROC AUC on unseen projects (group_probes.py, 17 projects sampled, 2026-11-08), LightGBM 0.754-0.814 on all six grouped folds of the builder's check; every fold holds hundreds of defective files."
   `dataset_missing_value_sentinel`: "`SM_method_numpar_gini = -1` is a real value of the source's gini formula (mynbou aggregation.py): two methods, one without parameters (median 2 method declarations, minimum parameters 0 on those rows); not a missing-value code."
   Then re-run `dataset check`.

**Review panel:** ship after changes (mediator). Full panel; the rebuttal round was skipped because the advocate's and
the critic's briefs converged. Claim audit: no validity claim refuted; the target wording (16.8% already reported),
the issue-level fix date and "size carries most of the signal" corrected (file size alone 0.783 pooled, 0.821 within
release; the note in `dataset.py` now says so). Column audit: no column leak; `_improvment` is Jira's "wish" type. Split audit: right with notes (grouped by
project; a temporal split fails on shared bugs). Domain practitioner: fit approximate; scores within a release.
Blind review: would benchmark; asks to prune the SM aggregates (optional). Task gamer: a next-release self-link,
+0.053; after the applied rounding still +0.046 (issue 2). Applied with no decision: ages in months and the release
year, the protocol line, per-file fix dates (31 more rows `Yes`, 4,074 against 4,043; a file's own fix never comes after the issue's last fixing commit, so no row turns `No`; the claim audit's 39 came from its own match of files and was not reproduced), the target wording, fit approximate, the notes.
Disputed and handed over: the left cohort cut (issue 1), the protocol-only remedy (issue 2), the `ISSUE_*` counts (issue 3),
the metric unit (issue 4), the warning acceptances (issue 5).

<details><summary>Mediator: smartshark_release_defect_prediction</summary>

```text
MEDIATOR REPORT: smartshark_release_defect_prediction (2026-11-09)

Summary (15 lines or fewer):
- Verdict: ship after changes. No Must is broken in a way the definition cannot fix.
- Must-fix: the next-release self-link (LEAK-10). release_date - MOSER_age gives each file a birth day. That links 81% of rows to the same file in the next release, whose counts fall inside the label window (0.787 -> 0.839, up in 9 of 9 splits). Fix: round MOSER_age to months and drop release_date or round it to the year, then re-run the gamer's link.py. If the gain stays above noise (+0.002), add a LEAK-9 protocol line. I did not run this experiment: the gamer's work/link.py is not in the run folder. The re-run is part of the change.
- Changes that need no decision: the target wording, per-file fix dates for the 39 rows, fit set to approximate (jm1 precedent), and notes on ISSUE_*, _improvment = Jira 'wish', and 279 vs 398 release dates.
- For the curator: (1) LEAK-25 left cohort rule, a validity Must and a departure from the 2026-10-21 amendment; (2) the metric, B (mean ROC AUC within release) vs pooled, plus a MET-5 amendment; (3) ISSUE_*: measure them, then keep or drop.
- Consistency: label window and regime are consistent. Fit approximate follows jm1. A cohort rule that reads the label departs from precedent unless the curator accepts the recording-start fact. Metric B follows protein/huesken and is the third case of its kind, so an amendment is due.

1. JUDGMENT RECORD
Verdict: ship after changes.
Validity: SEL-1/2/16 hold. USE-1 holds; the fit is approximate, not direct (USE-8: the one-year horizon is ours). LEAK-24 holds (one-year window, probe 13 clean). LEAK-10 is triggered by the next-release self-link and is fixed by rounding age and dropping or rounding the date; the gamer's link re-run confirms it. LEAK-10 for ISSUE_* is a weak soft leak, noted (best single column 0.626). LEAK-25 is open: the left cut reads the label at project level (curator, issue 1). LEAK-16..21 hold (0.0% copies). SPLIT-1/3 hold (grouped by project, the source's design; temporal fails SPLIT-9/14).
Value: TP-1 is flagged as a question, not a failure. File size alone scores 0.783 pooled (= LightGBM) and 0.821 per release (> LightGBM 0.811). Keep it; check model separation under the chosen metric.
Quality: CLEAN notes on _improvment (Jira wish), the gini sentinel, and the 2,773 redundant SM_* aggregates (pruning optional). groups_test_groups_few is accepted with the builder's wording.
Weighed: source +, real use +, size dominance -, width -.
For the curator: issue 1 (LEAK-25 cohort marker), issue 2 (metric unit, MET-1/MET-5), issue 3 (ISSUE_* measure-then-keep/drop).

2. CHANGES TO MAKE NOW (no decision needed)
a. LEAK-10 (Must, P4): round MOSER_age (to months, or coarser if needed) and drop release_date or round it to the year. MOSER_weighted_age and any other exact-day age field need the same treatment if they let the birth-day key be rebuilt. Re-run the gamer's link.py and exploit.py on the changed frame. If the gain is at noise (about +0.002), add a "Potential leak, kept on purpose:" line only if some gain is left. If it stays above noise, add a LEAK-9 protocol line (a participant must not link rows across releases) and a note with the measured gain. Exploit 2 (position from the end, +0.006, at noise) goes away with the same fix; re-measure it in the same run.
b. USE-5: the target reads "a bug present at the release, fixed within one year". Add the sentence that 16.8% of Yes rows were already reported in Jira at the release.
c. USE-5 (May): take the per-file fix date from _bug_fixes.json (this flips 39 rows) or say "the issue's fix date". Both sides accept either; per-file is the more exact.
d. USE-8: set fit to approximate, with fit_reason naming the one-year window, the cross-project-only regime and the pooled unit (if A). This follows the jm1, alfa_battle_2_0_task_2 and differentiated_thyroid_cancer_recurrence precedents. The builder argued for direct; no precedent keeps a curator-chosen horizon as direct.
e. P7 notes: ISSUE_* use Jira priority/type as of the 2018-19 collection (LEAK-10 note, weak). `_improvment` = Jira type "wish" (constants.py l.57), so it gets a note or a rename to `_wish` and is not merged with improvement (the blind reviewer's merge is wrong by the source code). Explain the 279 release dates vs 398 releases (the cohort cuts: 56 right, 62 left; several releases share dates). Accept groups_test_groups_few and the gini sentinel with the builder's texts.
f. Optional quality (CLEAN, no Must): prune the redundant SM_* inequality aggregates. Not required for shipping.

3. ISSUES FOR THE CURATOR (ranked)
Issue 1. Left cohort rule (P4, LEAK-25 Must).
- Problem: 62 releases (5,815 rows, all No) are dropped because their window closed before the project's first linked fix. That date comes from the label.
- Effect: validity. The rule reads the label; the alternative keeps 5,815 possibly unrecorded No rows or cuts 100 releases.
- Advocate/builder/domain: keep A. The first linked fix dates the start of issue linking, a recording event. This is like account_debt_south_africa (located by a data property, then shown by the label). Option C loses 100 releases, including calcite-1.0.0 with 130 defective files.
- Critic/precedent checker: the 2026-10-21 amendment allows only rules that do not read the label. Use a label-free marker (the project's Jira/link start from kit metadata) or give a reason that does not use the label.
- Not a rank conflict: LEAK-25 holds on its own. Under the rule as worded, A departs from it.
- Decision: (a) keep A, writing the recording-start reason as an exception, which is the first of its kind; (b) keep the rows; (c) a label-free marker. What would settle it: whether the kit has a per-project issue-tracker or link start date. If it does and it matches the first linked fix, (c) costs nothing.

Issue 2. Metric unit (P6, MET-1 Must, MET-5).
- Problem: the actor ranks within one release; pooled ROC AUC mixes projects (LightGBM 0.783 pooled vs 0.811 per release).
- For B (advocate, critic, domain, precedent): mean ROC AUC within release, with `release` as a scoring column. This follows protein_model_quality_rf_pcp and huesken_sirna_efficacy. An effort-aware Popt is a further option (domain).
- For A: the standard fallback, no new code (mean_group_roc_auc needs tests).
- Decide together with github_pull_request_acceptance. If B, write the MET-5 amendment (third within-unit exception) and re-run the TP check that models still separate from SM_file_lloc (0.821 per release).

Issue 3. ISSUE_* fields read at collection (P4, LEAK-10 Should/weak; critic).
- Critic: measure what ISSUE_* add over the other counts; keep them with a note if the gain is small, otherwise drop the fields that can change.
- Column auditor/advocate: best single column 0.626, the standard "prior bugs" feature; a note is enough.
- What would settle it: one grouped run with and without ISSUE_* (minutes). This is a weighing call because the kit has no history to show actual retyping.

Cross-dataset items (kept for the review page as the curator asked): scoring within groups (issue 2) and late-filled values (issue 3).

4. TASK GAMER EXPLOITS MAPPED
- Exploit 1, next-release self-link (+0.053): LEAK-10 Must (a join across rows to future counts); LEAK-9 if a protocol line is needed. NEW. The definition has no "Potential leak, kept on purpose" note for it. Fixed by change 2a.
- Exploit 2, release position from the end (+0.006, at noise): LEAK-10 (future knowledge). NEW, but negligible; it goes with 2a.
- Lookup in the published CSVs: out of scope (not a task flaw), as the gamer says.

5. AGREED FACTS
113,066 rows; 280 releases; 38 projects; 3.58% Yes; 3,260 features. No missing values. 0.0% copies across splits. Random split 0.945 vs grouped 0.784. Temporal split fails SPLIT-9 (8-22% shortcut positives) and SPLIT-14. Probe 13 is clean after the one-year cut. Single-feature AUC: ISSUE_major_bug 0.626, MOSER_bugfix 0.612. SM_file_lloc scores 0.783 pooled and 0.821 per release; LightGBM 0.783-0.786 pooled and 0.811 per release. 16.8% of Yes rows were already reported at the release; 39 rows flip with per-file fix dates. Self-link: 0.787 -> 0.839, 9/9 splits up; noise +0.002. _improvment = Jira wish. Cohort cuts: 56 releases right (35,390 rows), 62 left (5,815 rows).

6. CONSISTENCY
- Label window: consistent (LEAK-24 cases, cirrhosis LEAK-23).
- Grouped regime and groups_test_groups_few: consistent (heart_disease, huesken, etc.).
- Fit approximate: follows jm1, alfa_battle, thyroid.
- Left cohort A: departs from the 2026-10-21 LEAK-25 amendment. The distinguishing fact offered is that the first linked fix marks the recording start. Whether that counts is the curator's call (issue 1).
- Metric B: follows protein/huesken; A would depart without a distinguishing fact. Third of its kind, so the MET-5 amendment is due.
- No drift found.

Files: (the run folder) (reports) and (the run folder)
```

</details>

<details><summary>Claim audit: smartshark_release_defect_prediction</summary>

```text
Claim auditor: smartshark_release_defect_prediction (2026-11-09)
Verdict: ship-able after notes; one worth-benchmarking concern and two label-wording corrections. No validity refutation.
Tests run on the warehouse release_level_files.parquet and the builder's bug_fixes_long.parquet (no build).

| claim | source | test | result | evidence | rule |
|---|---|---|---|---|---|
| 26,28,29 cohort counts | curation_comments, claims 26-29 | recompute filters | holds | right 35,390 rows/56 rel; left 5,815/62 (left-only = left-any); kept 113,066, 280 rel, 38 proj, 3.58% Yes. (shipped_stats.txt "left-dropped 100 / 17,823" is the stricter option C, not the code) | LEAK-24/25 |
| 24 label = a bug present at release, fixed within 1y | task_summary.predicted, claim 24 | first_bug_fix vs release_date; per-file fix dates in _bug_fixes.json | holds with nuance | 0 rows with a fix before the release; 3 at delay 0 days; column date is the issue-level date: 39 rows labelled No whose own per-file fix commit is within 1y (1.0% of Yes), 359 files whose column date differs >1 day from the per-file earliest fix | USE-5 |
| features known at release, no label in features | claim 13-14, 36 | ROC AUC of each ISSUE_*bug count and MOSER_bugfix vs label | holds | best ISSUE_major_bug 0.626, MOSER_bugfix 0.612, others ~0.50 | LEAK-10 |
| "predicted: a bug that will need a fix" (forecast framing) | task_summary.question/predicted | share of Yes rows whose labelling bug's Jira issue was created before the release | partly refuted in wording | 16.8% of the 4,043 Yes rows: the bug was already reported at the release (known to the team, not in the features) | USE-5, USE-3 |
| 43/40 "size carries most of the signal" (lloc 0.755 vs LightGBM 0.786) | curation note, claims 40,43 | SM_file_lloc as an unfitted score on all kept rows | refuted in degree | pooled ROC AUC 0.783 (= builder's LightGBM pooled 0.783); mean per release 0.821 over 261 releases with both classes (> LightGBM per-release 0.811) | TP-1..TP-5 |
| no copy across split, project groups | claims 30-31 | release_date -> project unique | holds | each release_date maps to one project; builder probe 5 0.0% | LEAK-16..21 |
| metric fallback roc_auc | metric reason, claim 35 | read reason; per-release vs pooled | holds as fallback; unit concern stands | pooled vs per-release differ by ~0.04 for both lloc and LightGBM | MET-1, MET-5 |
| fold computability (dummy via scorer) | README splits | untested | untested: needs the 18 GB build; README gives 20-56k test rows, >=818 Yes per fold | MET-2 |
| ISSUE_* as of collection | claim 15 | untested | kit has no history | LEAK-10 |

Ranked refuted / untested:
1. Worth benchmarking (TP, Should): one raw feature, file size, equals untuned LightGBM pooled (0.783) and beats it per release (0.821 vs 0.811). Changes: the note "size carries most of the signal" understates; the task may not separate models. Mildest remedy: rewrite the note with these numbers and add a REVIEW.md issue (keep, or rerun task probes with a tuned model before shipping); if the metric goes per-release (builder issue 4), report that lloc alone already scores 0.82.
2. Target wording (USE-5, Should): 16.8% of positives are bugs already reported in Jira at the release; "will need a fix" reads as unknown future bugs. Remedy: one sentence in the target bullet and task_summary.predicted ("including bugs already reported but not yet fixed").
3. Label date (USE-5, May): the fix date is the issue-level column date, not the file's own fix commit; 39 rows (1% of Yes) flip. Remedy: say "the issue's fix date" in the bullet, or take the per-file date from _bug_fixes.json.
4. Untested: dummy scoring per fold (needs build); ISSUE field edits after release.
Scratch: none kept (inline runs).
```

</details>

<details><summary>Column audit: smartshark_release_defect_prediction</summary>

```text
Column auditor: smartshark_release_defect_prediction (2026-11-09)
Verdict: ship after one small cleaning fix; no leak found among the 3,260 features.

Frame audited: the builder's expframe.parquet (113,066 rows; the same cohort and label as the definition). Source code read:
mynbou smartshark_plugin.py, mynbou/path.py, mynbou/constants.py (collection-tools in the kit).

COLUMN TABLE (by family; 3,260 columns cannot be listed one per line, and every member of a family shares meaning, timing and dtype)
column | meaning | known at prediction? | dtype and cleaning | verdict | rule
SM_* (2,773 after drops) | SourceMeter static measures of the file, and of its classes, methods, enums, interfaces and annotations aggregated as sum/min/max/avg/median/stdev/gini/atkinson/hoover... | yes, measured at the release commit | float/int, numeric by meaning; gini in [-2,0] is the source's formula, not a sentinel | fine (gini scale anomaly is documented) | CLEAN-10, CLEAN-14
PMD_* (186) | PMD rule violation counts, by rule, severity and rule type | yes, at the release commit | int counts; dtype probe flags 2 PMD_rule_type_* as code_name: they are counts of 0-3, numeric is correct | fine | CLEAN-1
AST_* (65) | number of Java syntax-tree nodes per type | yes | int counts | fine |
DAMBROS_* (170), HASSAN_* (5) | D'Ambros change/entropy history measures, Hassan change-entropy measures | yes, over the window before the release | float | fine | LEAK-37 (window ends at release, not at outcome)
MOSER_* (17) | Moser process measures: revisions, authors, churn, bug-fix commits, refactorings, age, weighted age | yes; age = days from file creation to release (path.py l.592); MOSER_bugfix counts fix commits BEFORE the release | int/float; *_code_churn = added minus deleted, so negative values (min -3,194) are real; the dtype flag code_name is wrong, they are measured quantities | fine | CLEAN-1
CHANGE_TYPE_* (5) | counts of changes by type (computation, data, interface, logic/control, other) in the window | yes | int | fine |
REFACTOR_* (13) | RefDiff refactorings in the window | yes | int | fine |
ISSUE_<priority>_<type> (25) | number of distinct Jira issues linked to commits that touched the file in the six months before the release, by Jira priority and Jira issue type (path.py l.419, _add_linked_issues; NOT the hand-validated type) | the links exist before the release; priority and type are as Jira held them at collection (2018-19) | int counts; CLEANING PROBLEM: `improvment` is the source's mapping of Jira type "wish" (constants.py l.57: 'wish': 'improvment'); the four columns ISSUE_{major,minor,critical,trivial}_improvment are a distinct category (wish), not a typo duplicate of improvement - see finding 2 | leak: none measured (best single ISSUE column ROC AUC 0.626, ISSUE_major_bug; files with any pre-release bug issue 10.5% Yes vs 2.5%) ; mild hindsight only | LEAK-10
release_date | date of the release commit | yes (USE-6) | datetime | fine; under project-grouped splits it carries era only (yearly Yes rate 2.3-5.9%) | USE-6
project | Apache project name, the group | yes | categorical; group column, removed from features by feature_columns | fine | SPLIT-3
defect_within_1y (target) | a hand-validated bug present at the release and fixed within 365 days | outcome | Yes/No | fine |
Dropped (correct): file (path id), release (id), imports (names own packages), BUGFIX_count and the per-issue columns (the label), first_bug_fix (label date), 478 constants, 452 exact copies.

PROBLEMS, RANKED (principles.md order: leaks before cleaning before wording)
1. (P4, LEAK-10, Should-note; strength weak) ISSUE_* priority and type are read at collection, not at the release, and the type is the raw Jira type, while the label uses the hand-verified type (path.py l.347 issue_type_verified vs l.419 issue_type). So the features do not use the post-hoc validation: good. Remaining hindsight: an issue retyped or reprioritised after the release. Measured strength: per-column ROC AUC <= 0.626; removing nothing is warranted. Also checked: a multi-commit bug fix whose early commits precede the release would show in ISSUE_*_bug and MOSER_bugfix while its last fix labels the row; the builder found 9.8% of label bugs created before the release. ISSUE_*_bug>0 rows are 10.5% Yes, MOSER_bugfix AUC 0.612: ordinary, the field's standard "prior bugs" feature. Remedy: the curation note already says this; nothing more.
2. (P7, cleaning, minor) The dtype probe's four `code_name` flags (MOSER_max/sum_code_churn, PMD_rule_type_security..., PMD_rule_type_unnecessary...) are all counts or measured quantities: numeric is right, no change. The `_improvment` ISSUE columns (465, 70, 9, 29 nonzero rows for major/minor/critical/trivial) are Jira "wish" issues by the source's mapping; the names mislead. Mildest remedy: a note bullet saying `improvment` = Jira type wish (constants.py), or rename to `ISSUE_<p>_wish`. No merge.
3. (P7, CLEAN-14) `_gini` aggregates lie in [-2,0] with -2 for a single value (a constant-member sentinel by construction); builder already proposes accepting the sentinel warning. Agree; note is present.
4. Builder's draft issues, column view: issue 1 (one-year window) - the label columns and first_bug_fix are all dropped from features, no remnant of the window leaks; agree A. Issue 3 (left cohort uses project-level first fix) - not a feature, no column effect. Issue 4 (metric per release) needs a `release` scoring column, which the frame no longer has (dropped in step 4); if B is chosen, keep `release` as a scoring column, never a feature.

No question for the curator beyond the builder's five.
```

</details>

<details><summary>Split audit: smartshark_release_defect_prediction</summary>

```text
SPLIT AUDITOR - smartshark_release_defect_prediction
Verdict: RIGHT WITH NOTES (grouped by project, 3x3, 10-14 test projects per fold).

Regime. Use case as written (task_summary, Question) is a project without its own defect history = cold start on a
new entity; the source's experiment (Sec. 5.9) is cross-project. Group id `project` is a true id (38 Apache
projects), not a cluster. Files recur across releases within a project (a bug labels a file in 2.6 releases on
average): all of a project's releases stay on one side, so no recurrence crosses the split. Probe 5: 0.0% copies
across 9 splits; all 2,021 duplicate rows inside one project. Hidden-group check: IID 0.945 vs grouped 0.784
(gap 0.160) - IID would reward file recurrence; grouped is the honest score for the declared use.

Alternative (temporal, known project) measured by the builder (experiments.log), not re-run: without a gap
220/445, 187/866, 472/977 test positives share the same bug+file with training (SPLIT-9 shortcut, worth +0.03 to
+0.05 AUC); a 1-year gap equal to the label window removes it but leaves 27.6% / 36.2% / 53.2% of rows for training
(SPLIT-14 fails in 2 of 3). I agree with the builder's draft issue 2: grouped, recommend keep.

Notes (ranked):
1. P4 (USE-10, note only): grouped split trains on later releases of other projects when testing older ones
   (2005-2016 mixed). No shared files/bugs cross, so no label leak; ecosystem-wide drift (tools, PMD rule versions)
   is seen from the future. Mild; remedy: none needed, say it in the "What the test data stands for" line.
2. P4/P6: prediction unit = row, aggregation none, but the actor ranks within one release; pooled ROC AUC mixes
   projects with very different base rates and sizes (per-release 0.811 vs pooled 0.783). This is a metric issue
   (builder's P6 concern), not a split one; the split supports a per-release metric if the curator wants one.
3. Warning `groups_test_groups_few` (10-14 test projects/fold; grouped fold SD 0.051): accept; 3 repeats keep it
   readable. Remedy if wanted: 5 folds x 3 repeats.
4. Label delay: the one-year label window plus the cohort cut (window closed by 2018-01-01) means every shipped row's
   label is matured; under a grouped split no training row's label is in the test's future-unknown sense. Pass.
No re-split, gap or filter required.
```

</details>

<details><summary>Domain practitioner: smartshark_release_defect_prediction</summary>

```text
Domain practitioner report: smartshark_release_defect_prediction (2026-11-09)
Actor: QA / release lead of an Apache Java project with no defect history of its own, at the release commit, choosing which files to review or test first under a fixed review budget.

FIT: approximate (the declared "direct" is a slight overstatement). One sentence: the inputs are all mine at the release and the label is a hand-validated bug I would want to catch, but I act on a budgeted ranking of one release's files weighted by review effort, while the dataset scores a pooled ranking of rows across several held-out projects, and the one-year label horizon is our choice, not the source's (USE-8, builder issue 5).

1. Inputs at the prediction moment (USE-6)
 - Have: static measures, PMD warnings, six-month change/author/refactoring history - all computed from the release commit backwards (mynbou). Good.
 - ISSUE_<priority>_<type> counts use Jira priority/type as of collection, not as of the release: small soft leak; I would only have the then-current values. Accept with the note already in curation_comments.
 - release_date: I have it, but in a cross-project model it is a calendar proxy for prevalence era (2.3-5.9% by year); harmless, not a decision input I would use. Low.
 - Missing that I would always have: the file's own past defect count in my project (dropped by design of the cross-project setting) and the release identity. The release is what I rank within (see metric). Not a feature gap, a unit gap.
2. Target: "bug present at release, fixed within 365 days" is a reasonable proxy of "file will cost a post-release fix"; one year matches a typical support/maintenance horizon. I would want a score/probability to rank, then cut at my budget (effort in LOC). Option A of builder issue 1 is right; I support it. Bugs never linked to a fix stay invisible, as in all defect data.
3. Row vs decision: one row = one file-release = one review/test-priority decision. Yes. Test data = unseen projects, matching "a team without its own data" (the source's cross-project design, Sec. 5.9). In practice most teams that care have their own history (release-wise within-project is the more common practice), so the grouped regime covers the minority but literature-backed scenario; the builder's leakage numbers (8-22% of temporal test positives share file+bug with training, SPLIT-9) justify grouped. Support builder issue 2 grouped.
4. Would I use it: as a triage aid, yes, if it beats "sort by LOC" clearly. The probe shows LOC alone 0.755 vs LightGBM 0.786 ROC AUC: the model's lift over size is small, which is the known story of the field (effort-aware evaluation exists precisely because size dominates). I would distrust a model that just ranks big files first, since reviewing big files costs proportionally more. Trust needs effort-aware gains per release.
5. Metric: PARTLY. The fallback ROC AUC is a ranking metric (MET-8 ok; source fixes no threshold or single cost, so no MET-6/MET-7 threshold metric; imbalance alone does not argue for AUPRC, MET-9). But (a) the unit is wrong for MET-1: I rank within one release, pooled AUC across projects rewards calibrating between-project base rates (pooled 0.783 vs per-release mean 0.811); (b) it ignores effort: the source's own cost model uses LOC as effort (Sec. 5.2), and the field's standard is effort-aware ranking (Popt / recall at 20% of LOC, Mende & Koschke 2010, Kamei et al. 2013).
 Choice: my ideal is mean over releases of an effort-aware measure (Popt or recall@20%LOC); the minimum fix I would accept is builder option B, mean within-release ROC AUC with a `release` scoring column (MET-1). Support B over A. An effort-aware metric needs a new library metric and a LOC scoring column (which is also a feature, so it must be kept as a feature and flagged as metric input); log that as a curator option.

Gaps ranked by how much they change the task
 1. Metric unit and effort (pooled AUC vs within-release, effort-aware ranking) - MET-1; changes which models win (size-only rankers look good under AUC, bad under Popt).
 2. Regime: cross-project only; within-project release-wise is the more common real deployment (USE-10). Justified by leakage, state in fit_reason.
 3. Label horizon chosen by us (365 days) - USE-5/USE-8; fine, but argues fit = approximate.
 4. ISSUE_* counts read at collection time - small leak (USE-6).
 5. release_date as feature - minor.

What an expert would change: score per release, effort-aware (Popt or recall at 20% LOC), or at least mean within-release ROC AUC; label fit approximate; keep one-year window and grouped split; keep the 62-release left-cohort drop (builder issue 3 option A, sensible: those files cannot have a recorded fix).

Sources: dataset.py and README.md of the folder; builder_report.md draft issues 1-5; Herbold et al. 2022 EMSE 27:42 Sec. 4.1, 5.2, 5.9 (as quoted in the definition); Mende & Koschke 2010 (effort-aware defect prediction, Popt); Kamei et al. 2013 TSE (JIT, effort-aware recall at 20% LOC); metrics.md MET-1, MET-6-MET-9; use_case.md USE-1, USE-5, USE-6, USE-8, USE-10. No web lookups beyond domain knowledge.
```

</details>

<details><summary>Blind review: smartshark_release_defect_prediction</summary>

```text
BLIND REVIEW: smartshark_release_defect_prediction
Verdict: include with changes. It is a real, well-known cross-project defect-prediction task (SmartSHARK, Herbold et al., EMSE 2022, IND-JLMIV+R labels). Prune the 2773 SM_* aggregate columns and keep the grouped split.

Task: each row is one Java source file at one release of one of 38 Apache projects (113,066 rows). The target says whether the file gets a post-release defect within 1 year. QA staff or developers would use the prediction at release time to decide where to spend review and testing. The use is real, and cross-project (grouped by project) matches how it would be deployed on a new project.

Evidence:
- Positive rate 3.6% (4043/113066); per-project rate 0.4%-9.1%.
- Signal: LightGBM with GroupKFold(3) on project, using 491 non-SM + SM_file features, gives AUC 0.785/0.777/0.811. A single feature (SM_file_lloc, file size) already gives 0.773/0.757/0.762. Best single-column AUCs are about 0.78, all size proxies (AST_node_count, SM_*_loc_sum).
- No column looks leaky. ISSUE_*, MOSER_bugfix and HASSAN_* are history up to the release, which is standard in this literature. I could not confirm from the source that the windows end at the release date.

Concerns, ranked:
1. The benchmark mostly measures file size. Models gain only about 0.02-0.04 AUC over LOC alone, and the "effort-aware" literature notes this size confound. The task is still useful, but differences between models will be small and noisy. With only 38 groups, one project (manifoldcf, 19,125 rows = 17%) moves the fold scores a lot.
2. Width: 3259 features, of which 2773 are SM_* distributional aggregates (gini, theil, hoover, atkinson, entropy, ... of per-method/class metrics). They are highly redundant, and a 3-fold LightGBM on all columns did not finish in 9 minutes on 4 threads. Change: keep the SM_file_* metrics and a few avg/sum/max aggregates, or drop the inequality indices.
3. Near-duplicates across releases: unchanged files repeat release to release. 2,575 feature rows are exact duplicates (2,566 even with project included). The grouped-by-project split keeps them out of test, so this is fine, but it would break under a random split. Keep the group split.
4. Release coverage: 38 projects and ~279 project-release dates, while Zenodo says "IND-JLMIV+R for the 398 releases". Some releases appear to have been filtered out (maybe because of the 1-year window or a cut at 2016-12-31). I could not verify why.
5. Prep: release_date (datetime) is a feature. Across projects it adds little, but it lets a model learn era effects; I would drop it or turn it into release age. Typos in the source columns (ISSUE_*_improvment next to ISSUE_*_improvement) are split counts that should be merged. No missing values; no constant columns. The target is categorical Yes/No; that is fine.
6. Label quality: SZZ-style labels are noisy. The source itself says the 6M-SZZ version "should not be re-used", and this uses the recommended IND-JLMIV+R. It is acceptable.

Could not check: the replication notebook (how the 1-year window and the feature windows were computed), the paper text (paywalled), or a full-width model run.
```

</details>

<details><summary>Task gamer: smartshark_release_defect_prediction</summary>

```text
Task gamer report: smartshark_release_defect_prediction (ROC AUC, 9 grouped-by-project splits)

VERDICT: gameable by a lot. A file can be linked to itself in its project's next release, and that release's
counts cover the six months after the prediction point, inside the 1-year label window. AUC 0.787 -> 0.839.

HONEST BASELINE (work/baseline.py, work/baseline.log): untuned LightGBM, 300 trees, colsample 0.3, all features
  0.811 0.7906 0.7808 0.774 0.7781 0.8204 0.7879 0.7699 0.767  mean 0.7866
  Noise (+ random column): mean 0.7885, +0.002 (per split -0.001 to +0.005)

EXPLOITS, ranked by gain
1. Next-release file link (work/link.py, work/exploit.py, work/exploit.log)
   Birth day = release_date - MOSER_age (age is in days) is constant per file across releases; with the nearest
   AST/SM_file profile it links 81% of rows to the same file in the next release of the project. Features from
   the matched row: summed ISSUE_*_bug, MOSER_bugfix, revisions, churn, match distance, found flag, gap in days.
   Score 0.8392 (0.8514 0.8569 0.826 0.8431 0.8329 0.8511 0.827 0.8248 0.8399), gain +0.053 (+0.031..+0.066), 9/9 up.
   Single-feature AUC: next-release bug issues 0.71, next-release revisions 0.71. Link features alone 0.737;
   control on current-release counts plus release-level counts (work/linkonly.py) 0.671.
   Deployed model has it: no (counts cover the label window). Works because whole projects, with all their
   releases, sit in one test fold.
   Fix: round or drop MOSER_age, or round release_date to the month or year; or keep one release per project.
2. Release position from the end (fromlast, nrel; work/exploit.py)
   Label rate is 2.2% in the last release, 2.6% one before, 4-4.5% five or more back.
   Score 0.7923, gain +0.006 (-0.016..+0.016): barely above noise. Future knowledge (how many releases follow).
   Fix: same as 1.

FLAWS THAT HURT AN HONEST MODEL: none found. Not tested: dropping late-release training rows, whose lower label
rate may be censoring.

FOUND NOTHING
- Row order: shuffled; 104,930 project runs, 112,413 date runs in 113,066 rows;
  P(y=1 | previous row y=1) = 0.0386 vs base 0.0358.
- Missing values: none in any column.
- Release size AUC 0.48; gap to next release AUC 0.51; number of releases AUC 0.51.
- Copies across the split: impossible, folds hold whole projects.

NOT CHECKED: format/decimal artefacts, train-vs-test classifier, all-row transforms, a better linkage for
the 19% unmatched rows, the "+all" run (stopped).
Lookup in the published CSVs (they carry file names) would work; not a task flaw, not ranked.
Sources: doi 10.1007/s10664-021-10092-4; arxiv 1911.08938; zenodo.org/record/5675021
```

</details>

<details><summary>Precedent check: smartshark_release_defect_prediction</summary>

```text
Precedent check: smartshark_release_defect_prediction (2026-11-09)
Sources: register.json (5,226 decisions), leak_checks.md Cases (LEAK-23/24/25), metrics.md Cases (MET-5), use_case.md (USE-8), sibling jm1.

1. Label window, one year (draft issue 1, A) -- CONSISTENT.
   Precedents: LEAK-24 cases sf_permit_time (cut before 2024), consumer_complaints (settled archive); tunisian_fraud_detection_challenge
   (2026-11-04, Lennart: newest fiscal year cut). LEAK-23 cirrhosis_patient_survival_prediction: an outcome "within a fixed horizon,
   over the rows followed that long" - exactly A plus the follow-up cut. Probe 13 clean after the cut. No departure.

2. Regime, grouped by project (issue 2) -- CONSISTENT. The source's own cross-project design (SPLIT-1/3), temporal measured failing
   SPLIT-9 (8-22% shortcut positives) and SPLIT-14 (28%/36% train share). Accepting groups_test_groups_few with 38 groups follows the
   other definitions that accept it (heart_disease, open_university_learning_analytics_dataset, huesken_sirna_efficacy, airfoil_self_noise).

3. Left cohort rule (issue 3, A) -- DEPARTS WITHOUT A STATED REASON.
   LEAK-25 as amended 2026-10-21 (Lennart; caracas_cervical_cancer, account_debt_south_africa,
   fraud_detection_in_electricity_and_gas_consumption_1m) allows dropping unrecorded rows only when located "by a rule that does not
   read the label". Option A locates them by the project's first linked fix, i.e. by the label column of the same project (the builder
   says so: "reads the labels at the project level"). Option C (release-date cut) does not read the label and matches the amendment.
   Possible distinguishing fact: the first linked fix marks when issue linking started for the project (a recording event), the
   same kind of evidence as account_debt_south_africa's zero-debt file runs (located by a data property, then shown by the label).

   Reflection prompt (draft issue):
   Should the 62 releases before a project's first linked fix be dropped by a rule that reads the labels?
   **Problem:**
   - LEAK-25 (amended 2026-10-21) admits a drop only for rows located by a rule that does not read the label.
   - Option A locates the 62 releases (5,815 rows, all No) by the project's earliest fix linked to an issue, a label-derived date.
   - Option C (cut by release date) does not read the label but drops 100 releases, calcite-1.0.0 with 130 defective files among them.
   | Option | Pro | Con |
   |---|---|---|
   | a | Keep A, stating the fact: the first linked fix dates the start of the project's issue linking (the recording process), not an outcome of the dropped releases | reads labels at project level; first such exception to the 2026-10-21 wording |
   | b | Keep the 62 releases | no label reading; ships 5,815 rows that may be "not recorded" as No (LEAK-25 Must) |
   | c | Cut by a label-free recording marker (release date or the project's Jira/link start from the kit's metadata) | matches the amendment exactly | drops more rows (100 releases) or needs a marker the kit may lack |
   Recommendation: (a) only if the curator accepts the recording-start reading and writes it as the reason; otherwise (c) with a
   label-free marker if the kit has one.
   Footnotes: LEAK-25, LEAK-22.

4. Metric unit (issue 4) -- B FOLLOWS PRECEDENT; THIRD EXCEPTION OF ITS KIND.
   protein_model_quality_rf_pcp and huesken_sirna_efficacy (both 2026-11-04, Lennart) replaced the fallback with a within-group mean
   (mean_group_pearsonr) when the paper reports several metrics and the actor ranks within a unit (MET-5 exceptions). Here: several
   metrics, no criterion; the QA team ranks within a release; per-release 0.811 vs pooled 0.783. Choosing B is like-for-like; choosing A
   would depart from both without a distinguishing fact. Either way this is the third MET-5 exception of the "rank within a unit" kind:
   an amendment to MET-5 is due (principles.md, Exceptions and amendments). Note: mean_group_roc_auc is new code (definitions.md
   "Metrics" tests needed); a release scoring column must not be a feature (feature_columns drops scoring columns).

5. Fit wording direct (issue 5) -- DEPARTS, WEAK REASON GIVEN.
   USE-8 lists "a label definition the sources do not settle" as approximate; alfa_battle_2_0_task_2 (approximate: "a label without a
   stated horizon"), differentiated_thyroid_cancer_recurrence (2026-10-21, approximate: label definition not verified). Sibling jm1 is
   approximate. The one-year horizon is ours, not the source's. The builder's reason (a stated horizon on the source's validated labels)
   is a real fact but no precedent kept direct with a curator-chosen horizon. Prompt: option (a) direct, reason "horizon is a
   truncation of the source's own label, not a new definition"; (b) approximate naming the one-year window in fit_reason (matches
   alfa_battle/thyroid). Recommendation: (b). Footnotes: USE-8, USE-5.

Drift: none found (Lennart decided LEAK-24 and the MET-5 within-unit exceptions the same way each time).
Other calls (keep size/complexity single-feature signal, duplicates noted, ROC AUC fallback otherwise) consistent with LEAK-41/TP notes.
```

</details>

<details><summary>Advocate: smartshark_release_defect_prediction</summary>

```text
ADVOCATE OPENING BRIEF: smartshark_release_defect_prediction

Position: ship after changes. The problems found are fixed by changing the definition, which is the second-mildest rung of the remedy ladder. No Must is left that cannot be fixed, so exclusion does not apply.

1. The task gamer's next-release link is real; I concede it and propose a fix. Evidence: birth day = release_date - MOSER_age links 81% of rows to the same file in the next release. That release's counts cover the label window. AUC goes from 0.787 to 0.839, up in 9 of 9 splits. This breaks LEAK-10 (Must, P4) through a join across rows. Mildest fix: round MOSER_age, for example to whole months, and drop release_date or round it to the year. This removes the link key and keeps the age signal. Rerun the gamer's link.py to confirm the gain is back near noise (+0.002). This outranks excluding the dataset because the remedy ladder puts fixing the definition ahead of exclusion.

2. No other leak, and the split matches the use. The column auditor found no leak among 3,260 features. The best single counts are ISSUE_major_bug 0.626 and MOSER_bugfix 0.612. Probe 5 found 0.0% copies across splits. The grouped-by-project split is the source's cross-project design (Sec. 5.9, SPLIT-1/3). A random split scores 0.945 against 0.784 grouped, so random would reward file recurrence. A temporal split fails SPLIT-9 (8-22% of test positives share bug and file with training) and SPLIT-14. The precedent checker finds both the label window and the regime consistent (LEAK-23/24 cases). The split auditor says accept groups_test_groups_few as it stands; 5 folds x 3 repeats is the option if the curator wants it.

3. The use case is real, with an approximate fit, not a direct one (P3, USE-1). The domain practitioner (a QA or release lead) would use it as a triage aid. One row is one review decision, and every input exists at the release commit. I accept downgrading the fit to "approximate", as with the jm1 precedent. That is a wording change, not a reason to exclude.

4. "Size carries most of the signal" is not a TP failure (P6, TP-1: a flag is a question). File size alone scores 0.783 pooled, the same as LightGBM pooled. Per release it scores 0.821 against LightGBM's 0.811. The task still has headroom: the baseline is untuned, and defect prediction is known to be hard to beat over LOC, which is itself a finding a benchmark should show. Also, the mean ROC AUC within each release (option B) is the unit the actor ranks on. Under that metric, models must beat LOC within a release, which is the honest test. I back option B with release as a scoring column, as a third MET-5 exception that follows the protein and huesken precedents.

5. The left cohort rule (LEAK-25): keep option A and state the reason. The first linked fix marks when the project started linking issues to commits. That is a recording event, the same kind of evidence the account_debt_south_africa precedent accepted. Option C would lose 100 releases, including calcite-1.0.0 with 130 defective files. If the curator rejects the recording-start argument, use option C. Either way the dataset ships.

6. Label wording (USE-5), fixed without a decision. 16.8% of Yes rows were already reported at the release, so the target should read "a bug present at release, fixed within a year", not a pure forecast. The 39 rows whose own per-file fix falls within the year but are labelled No: switch them to per-file fix dates.

7. Cleaning (P7, CLEAN), changes that need no decision. Note the ISSUE_* fields as Jira type at collection time (a soft leak under LEAK-11 that weakens the signal; best AUC 0.626). Rename _improvment to its meaning (the Jira 'wish' type). Explain why 279 release dates differ from 398. Pruning the 2,773 SM_* aggregates is optional; it is a quality matter that does not block shipping.

Sources: the seven panel/*.report.txt files and builder_report.md in (the run folder)
```

</details>

<details><summary>Critic: smartshark_release_defect_prediction</summary>

```text
My position: ship only after changes 1 and 2. Points 3 to 5 are fixes or notes, and 6 and 7 are no reason to exclude. I took the phase-A evidence from the task gamer's report and from your digest; I did not re-measure anything myself. The full brief is in (the run folder)

1. **Next-release self-link (LEAK-10 Must; LEAK-9 Should).** release_date minus MOSER_age gives each file a fixed birth day, so 81% of rows link to the same file in the project's next release. That release's counts cover six months inside the label window, and whole projects sit in one test fold. AUC rises 0.787 -> 0.839 (+0.053, up in 9 of 9 splits). Remedy: round MOSER_age or release_date and re-run the gamer's link; if the gain stays above noise, add a LEAK-9 protocol line and a note.
2. **Cohort cut reads the label (LEAK-25 Must).** 62 releases are cut by the date of the first linked bug fix. Remedy: base the cut on a marker that is not the label (the recording start) or give a reason that does not use the label, then rebuild.
3. **ISSUE_* fields read at the 2018-19 collection, not at release (LEAK-10, LEAK-6).** Remedy: measure what they add over the counts alone; keep them with a note if small, otherwise drop the ones that can change.
4. **Target wording.** 16.8% of Yes are already reported at release, and the fix date is per file in 39 rows. Remedy: describe the target as "a bug fix linked within 1 year" and state the 39 rows.
5. **Metric (MET-5).** Pooled AUC is 0.783, the mean per release 0.811. Remedy: option B (mean ROC AUC within release, release as a scoring column) plus the MET-5 amendment.
6. **Value (TP-2; not an exclusion).** File size alone gets 0.783 pooled against 0.786 for LightGBM. Remedy: a note, and a check under metric B that the task still separates models.
7. **Quality (notes only).** 2,773 redundant SM_* aggregates, 279 release dates against 398 releases, the `_improvment` name, and a fit that is approximate rather than direct.
```

</details>
