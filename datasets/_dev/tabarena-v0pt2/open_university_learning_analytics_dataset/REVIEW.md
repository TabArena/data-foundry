# open_university_learning_analytics_dataset

**Outcome:** added. Ship; the panel's changes are made in the definition (not built yet). Validity: USE-5 and USE-8 hold (the four
source classes, fit approximate with the gap named); USE-6 triggered and fixed (the ungraded weight-0 marks of TMAs,
tutor-marked assignments, left out of the scores, issue 9); LEAK-17 triggered and fixed (a per-fold train filter
drops the test students' concurrent and later registrations from training; the effect is not distinguishable from
zero); LEAK-10 holds in code, with the TMA marking delay assumed (issue 4); the kept day-60 marks meet LEAK-10's grades row as
amended (Lennart, 2026-10-21); SPLIT-14 bars the temporal split, so the split is grouped, tagged `ForcedGroupedFromTemporal` under SPLIT-8 as
amended (Lennart, 2026-10-21).
Value: real signal across presentations (log-loss skill, the share of the class-prior baseline's log loss a model
removes: 0.167 for untuned LightGBM), but untuned model families score alike (TP-3, issue 12); few groups (22)
weighed against, a documented source and a real use case for. Quality: CLEAN-1 holds after issue 9; 93 Withdrawn
rows without a withdrawal date kept with a note (EV-2); `studied_credits` timing noted.

**Main points:** Confirm the 14-day marking delay (issue 4), the weight-0 marks left out (issue 9) and the dataset pending tuned results
(issue 12)?

**Record judgment:** valid, with an approximate fit. The Open University (OU) publishes no single task, so the day-60
prediction point, the four-class target and the split are our choices; the practitioner and the blind reviewer would
both use the dataset.

**Issues for Lennart:**

4. **TMA marking delay: keep 14 days?**
   - Problem: a TMA mark is only known when the tutor returns it, and the data holds no return date. The definition
     counts a mark 14 days after the later of the cut-off and the submission, from the OU Tutor Support Statement
     ("normally within ten working days of assignment deadlines"). Fourteen calendar days equal ten working days only
     without holidays, so the delay could err toward a leak.
   - Effect: the score depends on it. With no delay, LightGBM log-loss skill is 0.158 instead of 0.132 (one grouped
     repeat, before the other changes).
   - Rule: LEAK-10 (Must: every feature known at the prediction point); the delay is an assumption, not a measured
     fact (EV-7), so the definition notes it.
   - Alternative: a longer delay that allows for holidays, for example 21 days. Not measured; it lowers the score and
     the leak risk.
   - What would settle it: an OU source on 2013-2014 TMA return times.
   - Recommendation: keep 14 days with the note.
   - Decision: keep the 14-day delay?

9. **BBB 2014J's weight-0 marks: leave only the ungraded TMA marks out of the scores?**
   - Problem: BBB 2014J's first TMA has weight 0 and is marked 1 or 100 (1,739 of 1,776 marks), where the other BBB
     presentations weight and grade it. On day 60 it was that presentation's only known score, and untuned LightGBM
     scored below the class prior on it (log-loss skill -0.42).
   - Implemented: `score_mean` and `score_min` leave weight-0 TMAs out, as an analyst who knows the module's
     weights would (USE-6, Must: an input known at the prediction point; CLEAN-1). 1,655 rows lose that mark (1,652
     of BBB 2014J). On the 9 splits, untuned LightGBM (300 trees) reaches skill 0.167 (standard deviation over the
     splits 0.015; 0.04 on BBB 2014J) and random forest 0.158; with the marks in, 0.141 (0.052) and 0.168.
   - Not changed: FFF's weight-0 CMAs (quizzes) are graded (mean mark 86), and students submit them before day 60,
     long before their cut-off.
   - Alternatives: (a) leave out every weight-0 assessment, FFF's quizzes too: 4,683 rows change, LightGBM 0.163 and
     random forest 0.153, and on the FFF rows skill falls from 0.196 to 0.177 (LightGBM); (b) keep all marks and add
     the assessment weight as a feature (the critic's variant, not measured).
   - Recommendation: leave out only the weight-0 TMA marks, as implemented.
   - Decision: keep FFF's graded quizzes in the scores?

12. **Untuned model families now score alike: keep the dataset until tuned results say otherwise?**
   - Problem: the task probe on all 9 splits flags `no_spread`. Its own default models (not the LightGBM and random
     forest of issue 9) reach log-loss skill 0.173 (random forest), 0.170 (LightGBM) and 0.162 (logistic
     regression); random forest leads logistic regression by 0.011 with a paired standard error of 0.009, and the
     flag fires below twice the standard error. The panel's task probe, run before the weight-0 change on 5 of the
     9 splits, gave a lead of 0.061 (paired standard error 0.025).
   - Effect: the benchmark may separate methods less than it seemed. The signal itself is clear: every family beats
     the class shares on every split, and the best single feature (`score_mean` on 8 of 9 splits) reaches skill
     0.065.
   - Rule: TP-3 (Must): if tuned methods spread, keep the dataset. No tuned results exist for it yet. Precedents
     kept on `no_spread`: sf_permit_time and african_credit_scoring_challenge (no tuned results, re-check with the
     first tuned run); hr_analytics and acquire_valued_shoppers_challenge (a real task with a low ceiling).
   - Recommendation: keep, and read the first tuned run under TP-3.
   - Decision: keep the dataset pending tuned results?

**Review panel:** ship after changes (mediator); the changes are now in the definition. Claim audit: 48 claims, most
hold; the stated leak cost, the OULAD quote, the dropped-row labels, a stale probe number and the `known` list were
refuted (all fixed in the text), and the TMA delay is untested. Column audit: no leak; `studied_credits` timing a
question (noted). Split audit: grouped is the mildest split that holds. Blind review: include with changes. Debate:
agreed on the text fixes and the weight-0 marks; the train filter went to the critic and is now in the definition,
and the SPLIT-14 amendment goes to the curator (issue 1). The mediator's issues 1, 2, 3 and 4 are this file's issues
1, 11, 4 and 5 (5 settled); "REVIEW issue N" in the sections means the file before the panel.

<details><summary>Mediator</summary>

**Summary**

**Verdict: ship after changes.** The task is real, the features are cut at day 60, provenance holds (md5 matches) and the signal is real (grouped skill 0.141).

I settled the two disputed points as follows:

1. **The train filter for test students' concurrent and later registrations goes into the definition.** LEAK-17 is a Must, and the v2 split API can apply this filter. Rule and remedy order: fixing the definition comes before a note. I ran the experiment that settles the fact: on all 9 shipped splits the effect is not distinguishable from zero for either model, and the RF/LightGBM order is the same in every split. The filter is cheap insurance, not a fix for a bias anyone measured.
2. **The SPLIT-14 amendment goes to the curator as issue 1, decided for all three "too few periods" datasets together.** This follows today's NBA ruling. As written, the rules sanction no grouped fallback, so the dataset should not leave the working copy until this is decided.

---

**Recommendation (judgment record)**

```text
Verdict: ship after changes.
Validity: SEL-1/SEL-2 hold; USE-1/USE-5/USE-8 hold (fit approximate, gap named; 4-class at-risk AUC 0.803 vs binary
0.805); USE-6 triggered, fixed (weight-0 marks out of score_mean/score_min); LEAK-10 holds in code (14-day TMA delay
assumed from OU policy, untested, noted; Mechanisms-row wording for the curator, issue 2); LEAK-17 triggered, fixed
(per-fold train filter on concurrent/later registrations of test students; measured cost not distinguishable from 0);
SPLIT-3/SPLIT-9 vs SPLIT-14: grouped fallback, not optimistic on the one comparable window (1.205 vs 1.185), no rule
sanctions it as written: amendment due (issue 1, third case); PROV-8/PROV-10 hold (md5 matches; figshare DOI added).
Value: TP-2 real signal (grouped skill 0.141, IID 0.195); TP-5 holds (smallest class 874 per test fold);
groups_test_groups_few accepted (airfoil_self_noise, musk).
Quality: CLEAN-1 BBB 2014J fixed with the USE-6 change; 93 dateless Withdrawn rows kept with a note (inferred date,
EV-2); studied_credits timing noted.
Weighed: few groups -, real use case +, source documents +.
For the curator: issue 1 (SPLIT-14 amendment, rule question, decided for all three cases); issue 2 (LEAK-10
Mechanisms row narrowing); issue 3 (TMA delay against a 2013-14 OU source, optional).
```

**Changes to make now (no decision needed)**

The split filter and the score change alter the container. Under the house rules the definition is edited now and rebuilt only when the curator asks (rebuild.md).

**Changes to the definition**

1. **Per-fold train filter (LEAK-17 Must; the order of remedies puts a definition fix before a note).**
   - Add a custom `_make_splits`: take the grouped 3x3 CV (`self._cross_validation(df)`), then drop from each train side the registrations of that fold's test students whose presentation started on or after the student's earliest test presentation. That is 577-866 rows per fold, 3-5% of train.
   - Keep `id_student` and `code_presentation` in `df` until the split step and drop them there via `SplitPlan(df=...)`. `hotel_booking_demand` already uses a custom `_make_splits`.
   - Rewrite the "Potential leak, kept on purpose" bullet and the `fit_reason` to describe the filter. What stays: 4.9% of test rows share a student only through earlier registrations, which deployment also knows.
2. **Leave weight-0 assessments out of `score_mean` / `score_min` (USE-6; CLEAN-1; the practitioner: "an OU analyst would compute scores known over summative assessments only").**
   - This changes 1,655 rows. The reason is expert practice, not the score: RF goes down (0.168 to 0.158), so it is not tuned toward one model, which respects the spirit of SPLIT-21.
   - Re-measure the BBB 2014J Anomaly bullet and the fold-variance sentence afterwards.
   - The critic's variant (add the known weight as a feature and keep the marks) is a minor P7 option. The curator can ask for it; it is not needed.

**Text fixes (writing.md, EV-8; agreed by both sides)**

3. Rephrase the OULAD quote as analysis advice that points to the previous presentation, not as how the OU trains (claims 33/43). Add to `fit_reason` that about 68% of train rows come from presentations still running at the test presentation's day 60.
4. Replace "about 0.0025 log loss". Before the filter the raw cost is +0.002 to +0.005; net of a random-removal control it is not distinguishable from 0.
5. `known`: name `num_of_prev_attempts` and `studied_credits` (claim 5).
6. "6,190 ... Withdrawn" becomes "6,182 Withdrawn and 8 Fail" (claims 21/40).
7. Accepted warning: update logistic regression from 0.717 to 0.732 (claim 38). REVIEW issue 7: "the only dataset that accepts it" is stale (airfoil_self_noise also accepts it).
8. The click log starts 25 to 8 days before the start, depending on the presentation (claim 18). The UCI copy is equal to the source after removing "?" and normalising CRLF (claim 15).
9. Say day 60 was chosen for the use case (after the first marks are back), not from the day 0/30/60/90 sweep (SPLIT-21 spirit).
10. Note on the TMA delay (LEAK-10):
    - 14 days is an assumption from the OU Tutor Support Statement and is not visible in the data.
    - 14 calendar days equals ten working days only with no holidays, so it could err toward a leak.
    - Sensitivity: skill 0.132 with the delay, 0.158 without it.
11. Note on `studied_credits` (LEAK-10, a question per EV-6): it is equal across concurrent registrations, so it is consistent with a registration-time total. Do not drop it.
12. Anomaly bullet on the 93 Withdrawn rows without `date_unregistration`:
    - 0.35% of rows, all in 2014J presentations.
    - 84 have no click on days 46-59, against 22% of withdrawals that have a date; 19 never clicked.
    - Kept, because the withdrawal date is inferred (EV-2). The critic withdrew the drop.
13. Say "at the start of day 60": 42 registrations withdrew on day 60 itself (column audit).

**Record and REVIEW.md**

14. Add the figshare DOI 10.6084/m9.figshare.5081998.v1 to `source_links` (PROV-8).
15. Remove the stale "record `tag` disagrees" item from REVIEW (Lennart, 2026-10-19).

**Issues for the curator (ranked)**

**1. SPLIT-14 amendment: what a task with too few periods ships as (P4, Must against Must; a rule question).**
- Problem: deployment trains on earlier presentations (SPLIT-3, SPLIT-9). Only 2014J has at least 50% of rows before it (shares 14.9 / 43.1 / 66.5%), so SPLIT-14 bars a temporal split. A SPLIT-9 filter leaves 2013B with no train rows at all.
- Is it a conflict or an independent failure? Both Musts are in P4 and the earlier rules would win. But what they point to (a one-window temporal task) cannot be built, and nothing in the rules as written sanctions the grouped fallback. So this is a gap in the rules, and the ranking cannot close it.
- Effect: small. On the one comparable window the grouped split is slightly harder (LightGBM log loss 1.205 against 1.185), and the three models rank the same way under both splits.
- Advocate: the grouped split is the mildest split that holds, so ship now and leave the amendment in REVIEW.md.
- Critic: a Must has no exceptions, so decide the amendment in the same pass that ships this dataset. The critic itself calls this a timing call, not a blocker.
- My ruling: it is a curator issue, not a definition change, and the dataset does not leave the working copy until it is decided. Both sides' asks are met that way. Decide it together with nba_players_2016_2019 and distribution_transformers_at_cauca_department ("Rules from the NBA review" in the working-copy REVIEW.md).
- Decision needed: (a) closest regime, tagged "forced from temporal" with the cost measured (needs a new tag); (b) a one-window temporal task (a framework change); (c) `No` for all three. The NBA mediator proposed (a).

**2. LEAK-10 Mechanisms row: "earlier grades when the target is the final grade: drop it" (P4; a rule-wording question).**
- Problem: OULAD keeps the day-60 marks, which carry 10-30% of the continuous-assessment weight.
- Both sides agree the marks should stay: the actor acts on exactly those marks.
- Precedents: predict_students_dropout_and_academic_success (Lennart and Andrej) kept first-year grades; student_portuguese_performance dropped G1/G2 because its prediction point is earlier. This is the second case that keeps grades, not a third exception.
- Decision needed: narrow the row to "earlier grades not yet known at the prediction point" (the precedent checker's option (d)), or record OULAD as an exception.

**3. TMA marking delay (P4, LEAK-10; untested fact, optional).**
- The 14 days cannot be tested in the data, and the score depends on it (skill 0.132 against 0.158).
- What would settle it: an OU source on 2013-14 TMA return times. Until then the note (change 10) carries it.

**4. Only if the curator rejects change 1: LEAK-17.**
- Leaving the filter out means keeping a leak under a Must that can be fixed, so it needs an amendment ("entities no split can separate are kept with a measured note"), not an exception.
- No repeated-entity leak in the copy is kept on purpose today (precedent checker, item 5).

**The disputed points**

**A. Per-fold train filter against a note (LEAK-17 Must).**
- Facts: I re-ran the critic's exact filter on all 9 shipped splits, with 3 random-removal draws of the same size per split. Results are in log loss; positive means the filter hurts.

  | Model | Filter effect, net of random removal | Raw filter effect | Random removal |
  |---|---|---|---|
  | LightGBM | -0.0015 ± 0.0023 (SE) | +0.0016 | +0.0031 |
  | Random forest | +0.0002 ± 0.0005 (SE) | | |

- The RF minus LightGBM gap per split has the same sign in all 9 splits before and after the filter. The smallest gaps are 0.003-0.008, so the leak does not change a ranking.
- This agrees with the claim audit (-0.0012 ± 0.0015). The split audit's +0.0044 came from 3 folds and was driven by one of them.
- Advocate: a note resolves it, because no effect can be measured. The filter also leaves the larger future part on the train side (the 68%).
- Critic: a Must is fixed in the definition when it can be. The filter touches no test row, so USE-11 is untouched and there is no conflict for P3 to win.
- Ruling: the critic wins by strength and remedy order.
  - LEAK-17 is a Must, and its own remedies fail here: one row per student breaks USE-11 (a real conflict, which P3 wins), and grouping is impossible because shared students link all 22 presentations into one component.
  - The filter is a third remedy on the ladder ("filter"). It removes exactly the overlap deployment would not have.
  - "Fix the definition" ranks above "keep with a note". The LEAK-30 note pattern covers transductive scaling, and even there "fix it when we can" (sf_permit_time, home_credit).
  - The 68% of train rows from still-running presentations is the SPLIT-9 problem. That is an independent failure handled under issue 1, not a reason against this fix.
  - The rules settle this point, so it is not a weighing call.

**B. SPLIT-14 amendment: precondition or curator issue.** Settled under issue 1 above: a curator issue, decided together with the other two cases, and the dataset stays in the working copy until then.

**Agreed facts**

- 26,395 registrations active on day 60; 22 presentations of 7 modules, 2013-14; 4 classes (Pass 12,358, Fail 7,040, Withdrawn 3,973, Distinction 3,024); log loss.
- Every feature uses days before 60 or registration-time facts. Leak probes find no copies across the split, the best single feature reaches 0.671 against 0.744 for all features, and dropping any one feature costs at most 0.003.
- Skill: grouped 0.141 (sd 0.052), IID 0.195, 2014J hold-out 0.099. Group probe: logistic regression 0.732, RF 0.745, LightGBM 0.744.
- Shares of rows before each start date: 14.9 / 43.1 / 66.5%. On 2014J, grouped log loss is 1.205 against 1.185 temporal, with the same model order. 68% of train rows come from presentations still running at the test presentation's day 60.
- 12.9% of test rows share a student with the train side: 4.9% only through earlier registrations, 8.1% through concurrent or later ones. Shared students link all 22 presentations into one component.
- BBB 2014J: the first TMA has weight 0 and is marked 1 or 100 (1,739 of 1,776 marks). LightGBM skill on it is -0.42, and the three weakest splits are the three that test it. Leaving the weight-0 marks out gives LightGBM 0.141 to 0.167 (sd 0.052 to 0.016) and RF 0.168 to 0.158.
- Provenance: the figshare md5 matches and all 7 CSVs are byte-identical; CC BY 4.0 is confirmed. 93 Withdrawn rows have no unregistration date (84 inactive on days 46-59). The TMA delay cannot be tested.
- The practitioner and the blind reviewer would both use the dataset.

**Consistency with precedent**

- **Followed:**
  - The 4 source classes follow predict_students_dropout_and_academic_success.
  - Group context `all_rows` follows force_2020.
  - `groups_test_groups_few` follows airfoil_self_noise and musk.
  - The SPLIT-14 issue is handled like nba_players_2016_2019 (mediator, 2026-10-20): a curator issue for all three cases.
  - The 93-row note follows EV-2: an inferred date is weaker evidence than a recorded one.
- **Departures now closed:**
  - BBB 2014J was kept as recorded with a reason that did not set it apart from ashrae or hepatitis_c. The USE-6 fix ends that departure; PROV-13 does not apply, since there is no clean value to restore.
  - LEAK-17: the filter means the copy still has no repeated-entity leak kept on purpose (precedent checker, item 5).
- **Still open:**
  - The LEAK-10 Mechanisms row against the dropout sibling and student_portuguese_performance (issue 2; the difference is the prediction point, so this is a second case, not a third).
  - "Too few periods" is the third case of the same reason, so an amendment is due (issue 1). distribution_transformers went the other way (one year, IID); the amendment should bring all three into line.

</details>

<details><summary>Claim audit</summary>

Data: the definition's frame and its 9 shipped splits (3 repeats x 3 folds), rebuilt from the definition
(26,395 x 42; the same frame as the container); id_student re-attached by hashing all 42 columns (unique, aligned). Raw
tables: the figshare release. Models: untuned LightGBM (300 trees, lr 0.05), skill = 1 - logloss / prior logloss.
Downloads checked: figshare, UCI, the paper, the OU pages.

**Table**

| # | Claim (short) | Source | Test | Result | Evidence | Rule |
|---|---|---|---|---|---|---|
| 1 | question: day 60, 4 classes | D task_summary | target levels in frame | holds | 4 levels Pass/Fail/Withdrawn/Distinction | USE-5 |
| 2 | use case: OU looks for at-risk students on day 60, trains on other presentations of the module | D task_summary | OU Analyse page text | holds in part | page: "All students with their risk of failure in their next assignment are updated weekly"; OU's own target is next-assignment failure, not final_result; day 60 is ours | USE-1, USE-2 |
| 3 | 26,395 rows, 22 presentations, 7 modules, 2013-14 | D | count | holds | 26,395 / 22 / 7 | - |
| 4 | target = final_result | D | column | holds | paper: "final_result - student's final result in the module-presentation" | USE-5 |
| 5 | known = profile (6 named), reg date, assessments, VLE | D task_summary | compare with feature list | refuted (incomplete) | features also hold num_of_prev_attempts and studied_credits, not named; code_module, presentation_start, assessments_due not named either | writing |
| 6 | split: whole presentations held out; train has later/concurrent | D | groups per fold | holds | 0 group on both sides in all 9 splits | SPLIT-1 |
| 7 | changes | D | code read + counts | holds | see 21 | - |
| 8-9 | fit approximate; 12.9% of test rows share a student; cost ~0.0025 log loss | D fit_reason | overlap on 9 splits; LightGBM with shared-student train rows removed vs same number removed at random | 12.9% holds; 0.0025 refuted (not reproduced) | pooled 12.86%, per split 9.7-16.8%. Removing shared-student train rows: +0.0050 log loss (per split -0.0021..+0.0101); removing as many random rows: +0.0062; net -0.0012 +- 0.0015 (SE over 9 splits). The leak is not measurable; the stated number is neither the raw nor the net effect | LEAK-16..21, SPLIT-29, EV-1 |
| 10 | year 2015, source Other, OU page | D | file dates, page | holds | raw CSVs dated 2015-09-25 in the figshare zip; page names the 2015 Open Data Mashup | PROV-9 |
| 11 | license CC BY 4.0 | D | figshare API, OU page | holds (not evidence) | figshare API license "CC BY 4.0"; page "released under CC-BY 4.0" | EV-4 |
| 12 | data_tags Spatial | D | definitions.md rule | holds | `region` (13 levels) is geographic | definitions.md |
| 13 | figshare file 8606371, md5 7412686f...; 7 tables 464 MB | D | API + full download + md5sum; compare with local files | holds (pre-check's "not re-checkable" superseded) | API computed_md5 = 7412686fd77cf0e0ee1e8c3e9b354308; downloaded zip md5 equal; 7 files 464,367,129 bytes; all 7 local CSVs byte-identical to the zip | PROV-10, EV-7 |
| 14 | OU page: button without link; old file URL 404 | D | fetch page, HEAD URL | holds | `<a class="wp-block-button__link">Download dataset*</a>` has no href; schools.stem URL 404 | PROV-8 |
| 15 | UCI copy = these files after "?" -> "" | D | md5 of each UCI file with "?" removed vs figshare | holds (with a nit) | all 7 equal after removing "?" AND stripping CR: figshare files have CRLF line ends, UCI LF; byte equality needs both | PROV-15 |
| 16 | bibtex | D | Crossref | holds | Kuzilek, Hlosta, Zdrahal; Sci Data 4, 170171, 2017 | - |
| 17 | PREDICTION_DAY 60; MARKING_DAYS 14 = "ten working days"; KEY is source key | D | key uniqueness; delay not observable | KEY holds; delay untested | KEY unique (validate one_to_one passes). The data has no return date for TMAs; the previous REVIEW.md: no delay gives skill 0.158 vs 0.132, so the assumption is load-bearing | LEAK-10, EV-7 |
| 18 | click log starts 25 days before start | D docstring | min studentVle.date | holds in part | min -25 overall, but per presentation the first day ranges -25..-8 | - |
| 19 | 32,593 rows; 22 presentations of 7 modules | D comments | count | holds | 32,593 / 22 / 7 | - |
| 20 | target is the "final course results" the paper names | D comments | paper text (PMC5704676) | holds | "predicting student assessment results and final course results" | EV-2 |
| 21 | drops 6,190 ended before day 60 "whose result (Withdrawn) is already known", and 8 after | D comments | crosstab | counts hold; "Withdrawn" refuted for 8 rows | ended<60: 6,182 Withdrawn + 8 Fail; reg>60: 8 (4 Fail, 3 Pass, 1 Withdrawn). Paper says unregistered students have Withdrawal; 9 rows contradict it (8 dropped + 1 Fail in cohort with an unregistration date) | EV-2 |
| 22 | assessment features use only what is known on day 60 | D comments | code read: filters `date<60`, `date_submitted<60`, `marked_on<60`, Exam excluded, banked from start | holds in code; TMA delay untested | see 17 | LEAK-10..12 |
| 23 | VLE: nothing from day 60 on | D comments | code read: `clicks.date < day` before every aggregate | holds | - | LEAK-10 |
| 24 | dropped id_student, date_unregistration, code_presentation; module_presentation_length names the presentation | D comments | frame columns; courses.csv | holds | no dropped column in frame; length is unique per module within each module (e.g. BBB 240/268/234/262) | CLEAN |
| 25 | imd_band "10-20" -> "10-20%" | D comments | raw count, levels after | holds | 3,516 raw; 10 levels after | PROV-13 |
| 26 | categorical columns | D comments | dtypes | holds | 10 category incl. target; module_presentation is the group column, not a feature (40 features) | CLEAN |
| 27 | grouped since 4 start dates can't give 3 windows with half before each | D comments | share of rows before each start | holds | 2013J 0.149, 2014B 0.431, 2014J 0.665 | SPLIT-3 |
| 28 | potential leak kept; shared students link all 22 presentations | D comments | union-find on shared students | link holds; cost number refuted (see 8-9) | 1 connected component of 22 | SPLIT-29 |
| 29 | BBB 2014J: first TMA weight 0, marked 1/100; LightGBM skill -0.42; three weakest splits test it | D comments | assessments.csv; LightGBM 9 splits | holds | weight 0 vs 5 (others); 1,739 of 1,776 marks are 1 or 100; BBB 2014J skill -0.46/-0.36/-0.44 (mean -0.42); the three weakest splits (0.059, 0.069, 0.091) are the three that test it | PROV-13 |
| 30 | 93 Withdrawn without date_unregistration stay; 45 / 7 without date_registration | D comments | count | counts hold; implied "active on day 60" refuted for most of the 93 | 84 of 93 have no click on days 46-59 (control: 22% of Withdrawn with a later date); 65 last clicked before day 60, 19 never clicked; all 93 in 2014J presentations | USE-3, LEAK-1 |
| 31 | one conflicting duplicate pair | D comments | duplicated on features | holds | 2 rows, Fail / Withdrawn | - |
| 32 | group = module-presentation, 22 runs of 7 modules | D grouping | count | holds | - | - |
| 33 | OU trains on other presentations of the module (quote) | D grouping, R | read the page in context | quote holds; use as a deployment fact overstated | context: "it is good practice to analyse the B and J presentations separately. Nevertheless, for some presentations the corresponding previous B/J presentation do not exist and therefore the J presentation must be used to inform the B presentation" — analysis advice for dataset users, pointing to *previous* presentations (temporal), not a statement of how the OU trains its model | USE-1, EV-2 |
| 34 | OU Analyse scores all students weekly | D grouping | OU page | holds | quote in row 2 | USE-11 |
| 35 | split less strict than deployment | D grouping | - | holds | by construction | SPLIT-1 |
| 36 | 3x3 grouped CV, 6-9 presentations per test fold | D splits_comment | splits | holds | 6, 9, 7 per fold in every repeat; every test module has a train presentation of the same module in all 9 splits | SPLIT |
| 37 | stands in for temporal split | D | see 27 | holds | - | SPLIT-3 |
| 38 | accepted warning: fold sizes 7,694-10,563, smallest class 874, logreg/RF/LGBM/kNN 0.717/0.745/0.744/0.634 | D | splits; group_probes | sizes hold; logreg refuted (stale) | sizes 7,694..10,563, min class 874; today's group probe logreg 0.732 | EV-8 |
| 39 | only 2014J has half of rows before it | D decisions | as 27 | holds | 0.665 | - |
| 40 | an ended registration already has its result (Withdrawn) | D decisions | as 21 | refuted for 8 rows | 8 Fail | - |
| 41 | record: task as in D | R | as 1-3 | holds | - | - |
| 42 | Kaggle notebook uses exam score | R | fetch | untested | page needs JavaScript; content not readable | EV-7 |
| 43 | OU trains on other presentations | R | as 33 | overstated | as 33 | - |
| 44 | LightGBM skill IID 0.193, grouped 0.141, 2014J hold-out 0.099 | R | LightGBM, 3x3 stratified IID, 9 grouped splits, 2014J hold-out | holds | 0.195 / 0.141 (sd 0.052) / 0.0995 | EV-8 |
| 45 | BBB 2014J below prior | R | as 29 | holds | - | - |
| 46 | figshare DOI 10.6084/m9.figshare.5081998.v1, CC BY 4.0; OU link dead | R | figshare API; curl | holds (link "dead" = no download) | analyse.kmi.open.ac.uk URLs in source_links 301 to the OU Analyse home page; no download there | PROV-8 |
| 47 | priority 3 and its factors | R | - | untested (weighing, not a fact) | - | principles |
| 48 | record fields | R | read record | holds | year 2015, Grouped (NON-IID), Multiclass; no screening block, no CC lines | - |

Implied claims:

| Implied claim | Test | Result | Evidence | Rule |
|---|---|---|---|---|
| every feature known on day 60 | code read; cohort; studied_credits | holds except the 93 rows (row 30) and two untested points | TMA delay assumed (row 17). studied_credits ("credits for the modules the student is currently studying", paper) has no snapshot date; it is equal across a student's 1,078 concurrent registration pairs, consistent with a per-period value; its timing cannot be tested. 42 cohort rows unregister on day 60 itself (all Withdrawn): a same-day boundary | LEAK-10 |
| split is the one the use case needs | groups, modules per fold | holds as a stand-in | every test module seen in training; train side holds later presentations | SPLIT-3 |
| target is the real-world target | paper | holds in part | final_result is the source's outcome; OU Analyse acts on next-assignment risk | USE-5 |
| no row is a copy across the split | exact feature copies (leak probe 0.0%); shared students | holds | 0.0% copies; shared students' effect not measurable (row 8-9) | LEAK-16 |

**Refuted, ranked (validity first)**

1. P4 (USE-3/LEAK-1), implied cohort: 84 of the 93 Withdrawn rows without an unregistration date show no activity on
   days 46-59 (vs 22% of later withdrawals), 19 never clicked: most likely withdrew before day 60 and so are outside
   the stated cohort. 0.3% of rows. Mildest remedy: a note with these numbers in the Anomaly bullet (or drop those
   rows with no click on days 46-59 if the curator wants the cohort rule strict).
2. P4 (SPLIT-29), claims 9/28: the "about 0.0025 log loss" cost is not reproduced: raw +0.0050, net of a random-removal
   control -0.0012 +- 0.0015. Conclusion (a negligible leak) holds and is stronger. Remedy: replace the number.
3. P3 (USE-1), claims 33/43: the OULAD quote is analysis advice to use the previous presentation, not a statement of
   how the OU trains; it argues for temporal, not for "other presentations". Remedy: rephrase as advice; keep the
   grouped stand-in reasoning.
4. Claims 21/40: 8 of the 6,190 dropped rows are Fail, not Withdrawn. Remedy: "6,182 Withdrawn and 8 Fail".
5. Claim 5: `known` omits num_of_prev_attempts and studied_credits. Remedy: name them.
6. Claim 38: logreg AUC 0.717 is stale (0.732 today). Remedy: update.
7. Nits: claim 15 also needs CRLF->LF; claim 18 "25 days" is the earliest presentation (others -8..-25).

**Untested**

1. TMA marking delay of 14 days (claims 17, 22): the data has no return date; load-bearing (skill 0.132 vs 0.158).
   Curator check against an OU source for 2013-14.
2. studied_credits snapshot time: codebook gives none.
3. Claim 42 (Kaggle notebook): page needs JavaScript.
4. Claim 47 (priority): a weighing call, not a fact.

</details>

<details><summary>Column audit</summary>

Prediction point: day 60 of the module-presentation (features from days < 60). Frame: rebuilt from the definition
(26,395 rows, 42 columns; target `final_result`; group column `module_presentation`, metadata only).
Codebook: Kuzilek et al. 2017 (Sci. Data 4:170171), table descriptions.

**Column table**

| column | meaning (codebook) | known at day 60? | dtype and cleaning | verdict | rule |
|---|---|---|---|---|---|
| final_result | Distinction / Pass / Fail / Withdrawn | target | category, 4 classes, none missing | fine | CLEAN-15, CLEAN-17 |
| module_presentation | module + presentation, built | yes | category, 22 | fine: group column, not a feature | LEAK-33 |
| code_module | module code (7) | yes | category | fine | - |
| presentation_start | B/J letter of code_presentation as February/October | yes | category | fine (identifier turned into meaning) | CLEAN-3 |
| gender | student's gender | yes | category, 2 | fine; constant per student across registrations | - |
| region | region where the student lived during the presentation | yes | category, 13 | fine | - |
| highest_education | highest education on entry | yes | category, 5 (ordinal, unordered dtype) | fine | CLEAN-14 |
| imd_band | IMD band of the student's place of residence | yes | category, 10 bands; "10-20" -> "10-20%" harmonised; 997 missing | fine; missing is structural (Ireland 241, has no English IMD; North Region 654, ~50% missing in 5 modules: a source gap), not outcome-caused (Withdrawn 12.3% missing vs 15.2% present) | CLEAN-10, LEAK-10 |
| age_band | age band | yes | category, 3 | fine; 68 of 72 changes across registrations are ageing | - |
| disability | declared disability | yes | category, 2 | fine | - |
| num_of_prev_attempts | times the student attempted this module before | yes (registration) | int64 0-6 | fine: rises by 1 (1,255) to 3 between consecutive registrations, never falls | LEAK-10 |
| studied_credits | "total number of credits for the modules the student is currently studying" | probably (snapshot time not stated) | int64 30-630 | question: equal across concurrent registrations (1,078 student-presentations, 0 differ, withdrawn ones included), so a registration-time total; the codebook does not say whether modules added later count. Weak signal (Withdrawn 14-23% across bins) | LEAK-10 (question) |
| date_registration | days from presentation start to registration | yes | float64 (-311 to 59), 7 missing kept | fine | CLEAN-14 |
| assessments_due | TMAs/CMAs with cut-off < day 60 in the presentation | yes (schedule) | int64 0-4, constant within a presentation | fine | - |
| assessments_submitted | own submissions before day 60 to those | yes | int64 0-4; never > due | fine | - |
| days_early_mean | mean (cut-off - submission day) | yes | float64 -40..29; 4,424 missing = none submitted | fine | - |
| score_mean, score_min | scores known on day 60 (CMA at submission, TMA 14 days after max(cut-off, submission), banked from start) | yes, by the stated marking delay | float64 0-100; 4,098 missing (GGG 100%: first TMA due day 61, all weights 0) | fine for timing (lag is an assumption, issue 4 of REVIEW); BBB 2014J weight-0 marks 1/100 kept (anomaly, already a REVIEW issue) | LEAK-7, CLEAN-1 |
| assessments_banked | count of results transferred from an earlier presentation, all dates | yes (transfer from a previous attempt) | int64 0-12 | fine: 840 banked rows have cut-off >= 60, but banking is not gated by the outcome: 26 of 109 withdrawn banked registrations hold banked results dated after their withdrawal, only 13 fit gating; 67% of banked sets are a prefix of the schedule (the earlier attempt's progress) | LEAK-10 |
| clicks_before_start | clicks days -25..-1 | yes | int64 | fine | - |
| clicks_<19 activity types> | clicks per VLE activity type, days 0-59 | yes | int64, 0 filled | fine; 0 is also "type absent in the presentation" (dataplus 16, htmlactivity 21, repeatactivity 20 of 22 lack it); clicks_repeatactivity non-zero in 2 rows (near constant, kept: CLEAN-5 covers only constants) | CLEAN-5 |
| active_days | distinct click days 0-59 | yes | int64 0-60 | fine | - |
| clicks_last_14_days | clicks days 46-59 | yes | int64 | fine | - |
| days_since_last_click | 60 - last click day (incl. pre-start) | yes | float64 1-84; 561 missing = never clicked | fine: missing rows are 74.9% Fail, 16.4% Withdrawn: real disengagement signal known on day 60, not outcome-caused | LEAK-10 |
| dropped: id_student | identifier | - | dropped | fine | CLEAN-3 |
| dropped: code_presentation | year+start | yes | dropped (year names the presentation); month kept | fine | CLEAN-3 |
| dropped: date_unregistration | withdrawal day | after day 60 in cohort | dropped | fine (post-outcome) | LEAK-10 |
| not joined: module_presentation_length | presentation length | yes (schedule) | not joined | fine (names the presentation) | - |

**Problems, ranked (P4 first)**

1. **No new leak (P4).** Every feature is computed from days < 60 or registration-time facts; leak probes agree
   (best single feature score_mean 0.671 vs all 0.744; drop-one costs <= 0.003; no copies).
2. **Question, LEAK-10 (weak): `studied_credits` timing.** The codebook says "currently studying" without a date. Data
   shows it is shared across concurrent registrations, withdrawn included, i.e. one registration-time total. Mildest
   remedy: a note in the curation_comments; no drop.
3. **Minor, cohort edge (USE-7 / LEAK-22):** 42 registrations withdrawn exactly on day 60 stay in the cohort with label
   Withdrawn (features use < 60, so consistent with "predict at the start of day 60"). Remedy: none, or say "at the start
   of day 60".
4. **Already raised, not new:** weight-0 BBB 2014J marks in score_mean/score_min (CLEAN-1; REVIEW issue 9); TMA
   14-day lag an assumption (REVIEW issue 4); recurring students (LEAK-17; REVIEW issue 5).
5. **Quality (P7), keep with a note:** activity-type zeros mix "no click" and "type not offered" (CLEAN-14 meaning);
   clicks_repeatactivity is near constant (2 rows); ordinal bands (imd_band, age_band, highest_education) stored as
   unordered categories (CLEAN-14, acceptable).

Judgment: Validity: LEAK-10 holds for every column (one timing question); LEAK-33 holds. Quality: CLEAN-3, CLEAN-10,
CLEAN-14 hold; minor notes only.

</details>

<details><summary>Split audit</summary>

**Verdict: right with notes.** Grouped by module_presentation (22 groups, 3 x 3 folds) is the mildest split that
holds the rules; the temporal split deployment implies fails SPLIT-14, and on the one window where it can be run the
grouped split is slightly harder and ranks models the same way.

id_student and code_presentation re-attached to the shipped frame by matching every column (26,395/26,395
unique). Models: untuned LightGBM (300 trees, lr 0.05), random forest, logistic regression; one
fit per split (EV-8).

Judgment record:

```text
Verdict: right with notes.
Validity: USE-10 holds (a new, running presentation = cold start on the presentation; known module); SPLIT-1/3/4 hold
(grouped, the presentation new rows always come from); SPLIT-14 bars the temporal alternative (shares before
2013J/2014B/2014J: 14.9/43.1/66.5%); SPLIT-24 holds (true id from the source's key); SPLIT-9 departure forced and
measured (issue 1); SPLIT-29 hidden group kept with a note (issue 2).
Value: few groups (factor -): 6-9 test presentations per fold, accepted warning.
For the curator: issue 1 (fit "approximate" already says it); issue 2 (refresh the measured cost).
```

**Regime (USE-10, SPLIT-1..4)**

The use case is a running presentation on day 60, trained on finished presentations of the same module: the
presentation is new, the module is known. Measured: no shipped split holds out a whole module (0.0% of test rows in
all 9 splits), so every test row's module has other presentations in train, which matches "the OU trains on other
presentations of the same module". The group id is the source's own (code_module + code_presentation), not a cluster
or hash (SPLIT-24). Context `all_rows` is consistent: on day 60 the whole cohort's day-60 features exist.

**Problems, ranked**

1. **P4, SPLIT-9 / SPLIT-10 / SPLIT-11 (Must, departure forced by SPLIT-14): the train side holds presentations
   whose results are not known on the test presentation's day 60.**
   - Evidence: averaged over test rows, 68.0% of the fold's train rows would still be running (by test start: 2013B
     100%, 2013J 84.9%, 2014B 86.3%, 2014J 26.7%). 30.6% of test rows have no earlier presentation of their module in
     train (only later ones); 38.9% have none that deployment could use.
   - The alternative split (temporal by start, deployable train side = presentations ended before day 60):
     - 2014J rows (66.5% train): LightGBM log loss grouped 1.205 vs temporal 1.185; at-risk AUC 0.761 vs 0.767.
       Model ranking identical: random forest 1.075 / 1.071, LightGBM 1.200 / 1.185, logistic 1.239 / 1.207
       (grouped / temporal). The grouped split is slightly harder here, not optimistic.
     - 2013J and 2014B rows (14.9% train, only 3 modules): log loss 1.548 / 1.677 temporal vs 1.051 / 1.135 grouped.
       Not a fair deployment reading: the OU had presentations before 2013B that the release lacks.
   - Remedy: none milder than the current one. A temporal split has one valid window (SPLIT-14 needs 3, train >= 50%),
     a single 2014J hold-out breaks SPLIT-14 too. Keep grouped; the `fit = "approximate"` and `fit_reason` already
     name the gap. Optional wording: say that about two thirds of train rows come from presentations still running at
     the test's day 60.

2. **P4, SPLIT-29 / SPLIT-13 (Must, kept with a note): students recur across the split.**
   - Evidence: 13.0% of test rows (per split 9.7-16.8%) have the same id_student in train; 4.9% only in earlier
     registrations (deployment knows them, and `num_of_prev_attempts` already carries them), 8.1% in concurrent or
     later ones (deployment would not).
   - Control (repeat 0, LightGBM): dropping the 606-866 train rows of concurrent/later registrations of test students
     raises test log loss by 0.0022 / 0.0126 / 0.0001 (mean 0.0050) against 0.0006 for dropping as many random rows.
     The definition says "about 0.0025"; the re-measure gives about 0.004 net, noisy. Model gaps on the same rows are
     0.03-0.16, so the leak does not change rankings now.
   - Remedy (mildest first): keep, and widen the note to "0.0025-0.005 log loss"; a per-fold train filter that drops
     concurrent/later registrations of test students if methods are ever ranked within that margin. No grouping removes
     it (all 22 presentations linked by shared students).

3. **Weighed factor, few groups (SPLIT weighed factors; accepted `groups_test_groups_few`).** 22 groups, 6-9 per test
   fold; the shift is between presentations of known modules, not between unrelated domains, so the covertype
   precedent does not apply. Fold variance is driven by BBB 2014J (definition's Anomaly bullet). No change.

4. **Procedure (writing.md), minor.** The accepted warning quotes logistic regression 0.717 (2026-10-06); today's group
   probe gives 0.732. Update the number.

**Checks that pass**

- Grouped vs IID (group probe, LightGBM ROC AUC): IID 0.770 +- 0.002, grouped 0.747 +- 0.018. IID would put rows of
  the test presentation in train, which deployment never has (SPLIT-4); the gap does not decide.
- Near copies: 0.0% of test rows have an exact feature copy in train (leak probe).
- Season: 8 of 9 test folds hold both February (B) and October (J) presentations; one (repeat 0, fold 2) holds only
  J. `presentation_start` is a feature, so the season is seen in train in every split.
- Label delay inside a row: features use day < 60 and a 14-day TMA marking delay (column auditor's area).

</details>

<details><summary>Domain practitioner</summary>

Actor: an OU module team / student-support analyst who runs the at-risk model behind the tutors' Early Alert
Indicators (EAI) dashboard during a running module presentation.

**Fit: approximate (agree with the definition)**

One sentence: the rows, the day-60 inputs and the held-out presentations mirror how the OU scores a running
presentation from other presentations, but the OU acts on a weekly at-risk probability (next-TMA non-submission in
OU Analyse, pass probability in the Student Probabilities model), not on a four-class final result at one fixed day,
and the split trains on later and concurrent presentations deployment would not have (USE-8: a named stand-in).

**1. Inputs at the prediction point (USE-3, USE-6)**

Would have, and the dataset has them: demographics (gender, region, highest_education, imd_band, age_band,
disability), num_of_prev_attempts and studied_credits (kept from studentInfo, though `known` in the task_summary does
not name them), registration date, TMA/CMA submissions and timing, the marks returned by day 60 (with the 14-day TMA
marking delay, a careful and defensible reading of the OU ten-working-day rule), daily VLE clicks by activity type.
Nothing after day 60 enters; date_unregistration is dropped. I found no input I would not have.

Would always have and is missing (none is a leak; each makes the task harder than mine):
- The assessment weights and design of the module (weight-0 formative TMA in BBB 2014J). I know my module's design;
  the model sees a mark of 1 or 100 with no way to know it is formative (see the BBB 2014J gap below).
- The student's results on earlier OU modules (I see them in the student record). Here only num_of_prev_attempts
  for the same module; earlier registrations of recurring students exist as rows, not as features (USE-10).
- The Student Probabilities model's own pre-start pass probability, an OU estimate known before the outcome
  (USE-6 would make it an input). Not in the source, so not fixable.
- Finance / fee-waiver status and tutor contact logs (the eSTEeM study names finance as a main cause of missed
  predictions). Not in the source.

**2. The target (USE-5)**

I act on "is this student at risk of not passing / not submitting", a binary probability, to decide whom a tutor
calls. final_result in four classes is a slightly richer proxy: it contains the at-risk split (Fail+Withdrawn vs
Pass+Distinction) and the REVIEW reports the 4-class model's at-risk AUC (0.803) equals a binary model's (0.805), so
nothing is lost for my decision. What I do not act on is Distinction vs Pass, and log loss spends part of its weight
there. Withdrawn vs Fail matters a little (a withdrawer needs a different intervention), so keeping four classes is
defensible. I want a probability; log loss is the right scorer.

**3. One row = one decision? Test data = what I face? (USE-10, USE-11)**

A row is one registration scored on one day; in practice I score each student weekly, so one fixed day (60) is a
snapshot of a repeated decision. Day 60 is reasonable: after the first TMA marks are back, when the EAI accuracy
jumps. The cohort (active on day 60) is right: a student already withdrawn is not a decision.

Test data: a presentation not seen in training, scored one registration at a time, is what I face. The entity is the
presentation (a cold start for the run), and the student is sometimes known. Gaps: training holds later and
concurrent presentations (the REVIEW measures ~0.010 skill optimism on 2013J/2014B), and 12.9% of test rows share a
student with training (~0.0025 log loss). Both are small and documented; a temporal split is not available with four
start dates. I accept the grouped split as the closest stand-in.

**4. Would I use it?**

Yes, as a benchmark of the "pass probability from profile + early engagement" model. I would trust it because the
features respect the marking delay and the cohort is defined at the decision. I would distrust a model's ranking that
turns on BBB 2014J: a mark of 1/100 on a formative TMA is a design artefact any OU analyst would know about and
exclude, not a "redesign the model meets blind".

**Gaps ranked by how much they change the task**

1. Target granularity (USE-5): four classes at one day vs a weekly binary at-risk score. Moderate; signal for the
   decision is preserved (AUC 0.803 vs 0.805), and the extra Distinction/Pass split is extra difficulty, not a wrong
   task.
2. BBB 2014J weight-0 marks used as scores (USE-6 / USE-3 spirit): the actor knows assessment weights; the model
   cannot. Drives fold variance (LightGBM skill -0.42 on it). Fixable in the features.
3. Training on later/concurrent presentations and recurring students (USE-8, USE-10): small measured optimism
   (~0.010 skill, ~0.0025 log loss), named in fit_reason.
4. Single fixed prediction day (USE-3): a snapshot of a repeated weekly decision; day 60 is a defensible choice.
5. Missing inputs the actor always has (prior OU module results, Student Probabilities score, finance): not in the
   source; makes the task harder, not leaky.

**What an expert would change**

- Leave weight-0 (formative) assessment marks out of score_mean/score_min, or add the assessment weight so a model
  can tell them apart (REVIEW issue 9 alternative: LightGBM 0.141 -> 0.167, fold sd 0.052 -> 0.016). An OU analyst
  would compute "scores known" over summative assessments only. I would take this change; it is a feature-definition
  fix, not a relabel.
- Optional: name num_of_prev_attempts and studied_credits in task_summary.known (they are inputs).
- Keep four classes and day 60; keep grouped by presentation; keep the recurring-student overlap documented.
- Not worth doing here: the OU Analyse per-assignment weekly task (one row per student x TMA) would be a closer
  use case with a real temporal axis, but it is a different dataset.

**Sources**

- The definition, the previous REVIEW.md, the record and the panel's claim list.
- use_case.md (USE-3, USE-5, USE-6, USE-8, USE-10, USE-11).
- Kuzilek, Hlosta, Zdrahal (2017), Sci. Data 4:170171, doi 10.1038/sdata.2017.171.
- OU Analyse / EAI: https://computing-research.open.ac.uk/impact-cases/using-predictive-learning-analytics-to-improve-student-retention
- EAI eSTEeM report (pre-start pass accuracy ~73-75%, ~85% after first TMA): https://university.open.ac.uk/scholarship-and-innovation/esteem/sites/www.open.ac.uk.scholarship-and-innovation.esteem/files/resources/Calvert%2C%20Bromley%20and%20Hughes%2C%20Early%20Alerts%20Indicators.%20eSTEeM%20Final%20Report.pdf
- Disproved predictions report (finance as cause of misses): https://university.open.ac.uk/scholarship-and-innovation/esteem/projects/themes/supporting-students/disproved-predictions-risk-students-some-students-fail-despite
- Student Probabilities in retention: https://oro.open.ac.uk/49427
- Hlosta et al., Ouroboros, LAK 2017, doi 10.1145/3027385.3027449: https://results2021.ref.ac.uk/outputs/a9aa8e18-523c-4d00-8f90-b179a088406b?page=1

</details>

<details><summary>Blind review</summary>

**Verdict: include with changes** -- a real early-warning task with moderate, non-trivial signal, but the prediction cutoff and the population filter must be documented and checked before it goes in.

**Task**
The Open University (UK) predicts each student's final outcome (Distinction/Pass/Fail/Withdrawn) partway into a module presentation, so tutors can step in with at-risk students. This is a real, well-known use case (OU Analyse). The features (VLE clicks by activity type, assessments due/submitted/score, active_days, clicks_last_14_days, days_since_last_click) look like they are taken at a fixed snapshot early in the course.

**Checks I ran**
- 26,395 rows x 42 columns; 22 presentations (7 modules, 2013B-2014J). Classes: Pass 12,358, Fail 7,040, Withdrawn 3,973, Distinction 3,024.
- No exact duplicate rows (only 1 duplicate when the target is dropped).
- LightGBM with GroupKFold(3) by presentation: all features give log-loss 1.061, accuracy 0.555, OVR AUC 0.746. Demographics and registration only give log-loss 1.227, accuracy 0.463, AUC 0.610. So the signal is real, the task is not trivial, and there is room between methods.
- Top features by gain: score_mean, days_since_last_click, clicks_last_14_days, days_early_mean, date_registration.

**Concerns, most serious first**
1. **The snapshot cutoff is not documented, so I cannot confirm the features are point-in-time.** active_days has a maximum of exactly 60 and date_registration goes up to +59, which suggests a cutoff around day 60. days_since_last_click goes up to 84, so it seems to count from pre-start clicks. task.md does not state any cutoff.
   - score_mean is the strongest feature. An OU assessment score only exists once it is marked, so a TMA submitted just before the cutoff may not have had a mark yet. Pooling "score" by submission date could leak information slightly.
   - Fix: state the cutoff day in task.md, and filter assessments by when they were marked (or by due date plus a marking lag), not only by submission date.
2. **The population filter is undocumented.** Source OULAD has 32,593 registrations, about 10.2k of them Withdrawn (from my memory of the dataset; the UCI page only says "more than 30000 students"). Here there are 26,395 rows and only 3,973 Withdrawn, so about 6.2k registrations, mostly early withdrawals, appear to have been dropped. Dropping students who withdrew before the cutoff is correct (you cannot predict for them), but it has to be stated. Also check that nobody who unregistered before the cutoff is still in the data. The 92 Withdrawn rows with no clicks at all are worth a look.
3. **The split is reasonable but not the most faithful one.** Holding out whole presentations is sound, but in deployment the model is trained on past presentations and applied to the next one. A temporal split (2013 for training, 2014 for testing) would match that better. With only 22 groups and 3 folds, each test fold also has about 7 presentations and a different class mix: Withdrawn ranges from 4% (GGG 2013J) to 24% (CCC 2014J), which makes the scores noisier.
4. **Some features are really presentation constants.** assessments_due is constant within each presentation (GGG is always 0, EEE always 1), so together with code_module it acts as a proxy for module and design. That is harmless, but it means "assessments_due" tells you about the course design, not about the student.
5. **Minor points.**
   - Missing values are plausible: imd_band has 997 NaN, score_mean 4,098 NaN (nothing submitted or nothing due), days_since_last_click 561 NaN (no clicks).
   - studied_credits has a maximum of 630, a real outlier in the source.
   - The Distinction/Pass boundary is a threshold on the final score, so those two classes will be hard to tell apart. That is fine, but worth noting if accuracy is the metric.

**What I could not check**
- The raw OULAD tables and the actual feature-building code, so I could not confirm the cutoff or the marking-time handling.
- The KMI page now redirects to research.stem.open.ac.uk and I did not fetch it. The UCI page has no field definitions.

</details>

<details><summary>Precedent check</summary>

Inputs: the register of decisions (808; OULAD's own entries are the 10 AI open issues of 2026-10-07 and two AI
assessments, no `CC` line of the curator), the Cases tables of `splits.md`, `leak_checks.md`, `use_case.md`,
`provenance.md`, `task_probes.md`, the sibling definitions in the working copy, and nba_players_2016_2019's REVIEW.md
(panel of today). The curator's marks in the review-page databases (artifacts) were
not readable from here; nothing in the repository records a curator decision on OULAD's open issues.

Siblings (student outcome): `predict_students_dropout_and_academic_success` (Lennart, Andrej; TabArena v0.1, IID,
3 source classes, first-year grades kept), `student_portuguese_performance` (Lennart CC; G1/G2 dropped),
`early_learning_predictors` (grouped by facility, context none). Structural siblings: `nba_players_2016_2019` and
`distribution_transformers_at_cauca_department` (too few periods for SPLIT-14), `airfoil_self_noise` and `covertype`
(few groups), `force_2020` (context all_rows).

**Summary**

| # | Decision (implemented) | Verdict | Closest precedents | Rules |
|---|---|---|---|---|
| 1 | Grouped by presentation instead of temporal | departs with a stated reason; third case of the same reason, amendment due | nba_players (AI, 2026-10-20, open), distribution_transformers (AI, 2026-10-07, open), account_debt_south_africa (Lennart, 2026-10-12), seismic_bumps (Lennart) | SPLIT-3, SPLIT-14, SPLIT-8, SPLIT-16, USE-10 |
| 2 | Day 60, with the assessment scores known by then | consistent with the dropout sibling; departs from the wording of a LEAK-10 Mechanisms row with no written reason | predict_students_dropout (Lennart/Andrej, v0.1), student_portuguese_performance (Lennart), kickstarter, mutual_funds_india | USE-3, LEAK-10 |
| 3 | The source's 4 classes | consistent | predict_students_dropout (3 source classes), force_2020 | USE-5, SEL-8 |
| 4 | 14-day TMA delay from the OU policy | consistent (no close precedent; a new kind of decision) | brazilian_ecommerce, sf_permit_time (gaps for delays); EV-2 | LEAK-10, EV-2 |
| 5 | Recurring students kept, `Potential leak, kept on purpose` | departs from a Must with a stated reason; formally not an exception (LEAK-17 is a Must) | kick, account_debt, LEAK-30 tension (Lennart, 2026-10-19); USE-11 (breast_cancer, Lennart 2026-10-15; corporate_credit_rating 2026-10-16); nba (grouped by player) | LEAK-17, SPLIT-29, USE-11 |
| 6 | figshare DOI missing in `source_links` | consistent (a fix, no decision) | | PROV-8 |
| 7 | `groups_test_groups_few` accepted | consistent; the issue text is stale | airfoil_self_noise (2026-10-20), covertype, musk, parkinsons | TP-5, definitions.md |
| 8 | year 2015, source Other, OU page, `Spatial` | consistent | PROV-9; definitions.md data_tags | PROV-9 |
| 9 | BBB 2014J marks kept as recorded | departs with a stated reason that does not set it apart from ashrae | ashrae (2026-10-15), hepatitis_c (LEAK-13), aeolus (Lennart, 2026-10-12) | PROV-13, LEAK-13, SPLIT-20 |
| 10 | Group context `all_rows` | consistent | force_2020, amex_non_iid_1m, musk, sat11, fraud_detection | definitions.md `context` |
| - | Record `tag` disagreement (the previous REVIEW.md) | settled; drop it from REVIEW | Lennart, 2026-10-19 (CHANGELOG): contradicting `Non-IID (Temporal)` tags removed | |

**1. Split: grouped by module-presentation instead of temporal**

- Rules: SPLIT-3 (Must; "one regime, the one the use case implies", Lennart 2026-10-12, Tensions table), SPLIT-14
  (Must; 3 windows with 50% train), SPLIT-8 (Must; the only sanctioned fallback: no dates at all, IID tagged
  `ForcedIIDFromTemporal`, cost measured; account_debt_south_africa, Lennart 2026-10-12), SPLIT-16 (Must; seismic_bumps:
  "no fallback to an IID split", `Too Small`).
- OULAD has dates but four start dates; the definition and `splits_comment` say the grouped split "stands in for the
  temporal split of deployment" and measure the cost (IID 0.193, grouped 0.141, 2014J hold-out 0.099; +0.010 skill
  optimism on the older test presentations).
- Same reason, three cases, two different fallbacks:
  - nba_players_2016_2019 (panel 2026-10-20, REVIEW issue 1, open): three seasons, grouped by player, "a fallback
    from temporal"; its panel already named OULAD as one of the three and asked for an amendment.
  - distribution_transformers_at_cauca_department (AI 2026-10-07, REVIEW issue 2, open): two years, one year shipped
    IID with `ForcedIIDFromTemporal`.
  - open_university (this one): grouped by presentation.
- What sets OULAD apart from NBA (evident from the data and written in the definition): the deployed prediction is
  for a new presentation whose results are unknown, so the group the split holds out is the deployment unit, and the
  student is mostly new (cold start under USE-10). NBA's use case is a known player, where USE-10 asks for history.
  The OU's own documentation also trains across presentations in both directions ("the J presentation must be used
  to inform the B presentation or vice versa"). So OULAD's departure is narrower than NBA's: only the time order of the
  train side is lost, not the entity's history.
- Gap against the closest sanctioned fallback: account_debt and distribution_transformers carry a tag
  (`ForcedIIDFromTemporal`); a grouped fallback has no tag in the vocabulary (definitions.md `data_tags`), so OULAD and
  NBA say it only in text.
- Verdict: departs with a stated reason; the reason is a Must of the same part (SPLIT-14) that cannot be met, so it is
  not an exception the ranking settles. Third case of the same reason: an amendment is due (principles.md case 4).

**Consistency check (AI, 2026-10-20):** the grouped split of open_university_learning_analytics_dataset (a departure
from SPLIT-3: deployment trains on earlier presentations) is the third dataset where too few periods for SPLIT-14
decide the regime, with nba_players_2016_2019 (grouped, open) and distribution_transformers_at_cauca_department (one
year, IID, `ForcedIIDFromTemporal`, open). What sets it apart?
(a) the held-out group is the deployment unit (a new presentation with new students), and the OU itself trains across
presentations in both directions, so only the time order of the train side is lost (+0.010 skill measured), recorded
as an exception; (b) treat it like distribution_transformers (one period, IID, tagged); (c) reopen the other two to
match OULAD; (d) change the rule: an amendment to SPLIT-14 / SPLIT-8 that says what a task with too few periods ships
as (the closest regime with the cost measured and a "forced from temporal" tag, a one-window temporal task, or `No`),
applied to all three.

**2. Prediction day 60 and the assessment scores known by then**

- Prediction point named and features cut at it: follows USE-3 / kickstarter (the written prediction point decides).
- Sibling pair:
  - predict_students_dropout_and_academic_success (Lennart, Andrej; shipped TabArena v0.1): predicts the outcome at the
    end of the course from the first two semesters' units and grades: in-course grades kept ("the features were
    collected after 2nd semester - hence should be fine").
  - student_portuguese_performance (Lennart CC): G1 and G2 dropped, because its use case predicts "early in the year
    from background". This is the source of the LEAK-10 Mechanisms row "earlier grades when the target is the final
    grade: drop it" (leak_checks.md, Cases).
- OULAD keeps `score_mean` / `score_min` of the TMAs and CMAs marked by day 60. Measured today on `assessments.csv`:
  the assessments due before day 60 carry 10-30% of a presentation's continuous-assessment weight (median 22.5%; GGG
  0, as its weights are 0), so they are a part of what decides `final_result`.
- Verdict: consistent with the dropout sibling and with the stated prediction point; it departs from the Mechanisms
  row as written, which drops earlier grades regardless of the prediction point, and the definition gives no reason for
  that row. Two datasets now keep in-course grades (dropout, OULAD) against one that drops them (Portuguese, a
  different prediction point). Not yet a third exception.
- The choice of day 60 itself (against 0 / 30 / 90) has no precedent: no other dataset in the copy picks a day in an
  ongoing process from a sweep. SPLIT-21's spirit (do not pick a design from a comparison of scores) applies: the
  record should say day 60 was chosen for the use case (an early-warning point), not for its skill.

**Consistency check (AI, 2026-10-20):** keeping the day-60 assessment scores in open_university (a departure from the
LEAK-10 Mechanisms row "earlier grades when the target is the final grade: drop it") differs from
student_portuguese_performance (G1/G2 dropped, Lennart) and matches predict_students_dropout_and_academic_success
(first-year grades kept, Lennart and Andrej). What sets it apart?
(a) the prediction point falls after those assessments, and the actor (OU Analyse, tutors) acts on exactly those
marks; the Portuguese drop followed from its earlier prediction point, so the row is about grades after the
prediction point, recorded as an exception; (b) treat OULAD like Portuguese and drop the scores; (c) reopen the dropout
sibling to drop its semester grades; (d) change the rule: narrow the Mechanisms row to "earlier grades not yet known at
the prediction point".

**3. Target framing: the source's 4 classes**

- Follows predict_students_dropout_and_academic_success (the source's 3 classes Dropout / Enrolled / Graduate, though
  the actor acts on dropout) and force_2020 (multiclass log loss over the source's classes). USE-5 ("at the resolution
  they act on it") would point to at risk; no student sibling took that route, and the 4-class model gives the same
  at-risk AUC (0.803 against 0.805). Consistent.

**4. TMA marking delay of 14 days**

- No dataset in the copy delays a feature by an assumed processing time from a policy document. Closest: SPLIT-10 gaps
  for label delays (brazilian_ecommerce, Lennart 2026-10-15; sf_permit_time), which were measured, not assumed. The
  evidence order (EV-2: the source's primary documents before inference) supports using the OU Tutor Support
  Statement. Consistent; a new kind of decision, so the curator's answer becomes the precedent (a Cases row under
  LEAK-10).

**5. Recurring students across the split, kept**

- LEAK-17 (Must): repeated entities leak; keep one row per entity when the use case is that row, or group. USE-11
  (Must; breast_cancer_prediction, Lennart 2026-10-15; corporate_credit_rating 2026-10-16: one row per entity cost
  0.112 against 0.158 skill) bars one row per student here (the use case is every registration). Grouping by student
  together with presentation is impossible (all 22 presentations linked). So neither remedy of LEAK-17 can be met.
- The note follows the house pattern `Potential leak, kept on purpose` with a measured cost (kick, account_debt,
  aeolus, house_sales; the LEAK-30 tension, Lennart 2026-10-19: a weak leak kept with a note). The size (about 0.0025
  log loss) is of the order of those kept leaks.
- Pair to watch: nba_players groups by player so no entity crosses; it could because its use case is the player. Not
  a like case (OULAD's group is the presentation).
- Verdict: departs from a Must with a stated reason (no grouping removes it, cost measured). Under principles.md a Must
  has no exceptions; this is the first repeated-entity leak kept on purpose in the copy, so it needs the curator's
  explicit call (a narrowing of LEAK-17 for entities no split can separate, or a Cases row).

**Consistency check (AI, 2026-10-20):** keeping 12.9% of grouped test rows whose student is on the train side (a
departure from LEAK-17, a Must) has no precedent: every other repeated entity in the copy was grouped or reduced to
one row. What sets it apart?
(a) the shared students link all 22 presentations, so no grouping removes them, and one row per student would change
the cohort (USE-11); the cost is about 0.0025 log loss, recorded as a Cases row; (b) keep one registration per student
(2,384 rows fewer); (c) none to reopen; (d) change the rule: LEAK-17 narrowed to keep, with a measured note, entities
no split can separate.

**6. Record pointers**

- `source_links` without the figshare DOI: a fix under PROV-8, nothing to compare.

**7. Accepted warning `groups_test_groups_few`**

- Follows airfoil_self_noise (2026-10-20: 33 setups, 11 per fold, accepted with group_probes evidence) and the
  definitions.md condition (accept only with group_probes evidence and enough units of each class per fold: smallest
  class 874 rows, scored per row, so not `Too Small` under TP-5 as parkinsons was). covertype (3 areas, IID) is set
  apart by the deployment unit, as the issue says.
- Correction for REVIEW issue 7: "the only dataset in the copy that accepts it" is no longer true; airfoil_self_noise
  accepts it since today. Also the accepted text quotes logistic regression macro AUC 0.717 (2026-10-06), today's probe
  0.732 (checklist).

**8. Minor metadata**

- `year = "2015"` (first release, not the 2013-2014 collection or the 2017 paper): PROV-9. `source = "Other"` with the
  OU page as `source_url`: the place of first publication (definitions.md). `data_tags = ("Spatial",)`: `region` is a
  region in the sense of definitions.md; `imd_band` is a deprivation band, not geographic, so the tag rests on `region`
  alone. Consistent.

**9. BBB 2014J marking redesign, kept**

- Closest precedents: ashrae (PROV-13 / CLEAN-1, 2026-10-15): units mixed across sites, harmonised to one unit;
  hepatitis_c_prediction (LEAK-13): recording conventions harmonised, after measuring the effect; aeolus (SPLIT-20,
  Lennart 2026-10-12): a break in the history handled by choosing the history.
- OULAD keeps a group-specific recording convention (a weight-0 TMA marked 1/100 where the others grade it) with the
  reason "a deployed model meets such redesigns". That reason holds for ashrae's sites too, so it does not set the case
  apart. A fact that could: the 1/100 marks are what the OU recorded for that design, not a conversion error, so there
  is no "clean" value to restore (PROV-13 needs an origin with clean data). The alternative (weight-0 marks out of
  score_mean/score_min) is a cleaning around a design, not a repair.
- Verdict: departs from the ashrae / hepatitis_c line with a stated reason that does not distinguish it; the curator's
  call (open issue 9) should name the fact.

**Consistency check (AI, 2026-10-20):** keeping BBB 2014J's 1/100 marks as recorded (open issue 9) differs from
ashrae (2026-10-15, units mixed across sites harmonised) and hepatitis_c_prediction (class-specific recording
harmonised, LEAK-13). What sets it apart?
(a) the marks are the OU's real record of a redesigned assessment, not a conversion error, so there is no clean value
to restore and a deployed model meets the same redesign, recorded as an exception to PROV-13's repair; (b) treat it
like ashrae: leave weight-0 marks out of score_mean / score_min (1,655 rows change); (c) reopen ashrae; (d) change the
rule: say in PROV-13 that a source's own redesign is kept, a recording error repaired.

**10. Group context `all_rows`**

- Follows force_2020 (the whole log of a new well is known), amex_non_iid_1m, musk, sat11_hand_algo_runtime,
  fraud_detection_in_electricity_and_gas_consumption_1m; the definitions.md rule ("all rows of a new group are known
  when predicting"). On day 60 every registration of the running presentation is known with its day-60 features (OU
  Analyse scores the whole presentation weekly). early_learning_predictors (`none`) differs in kind (no cohort-wide
  scoring in its use case). Consistent.

**Drift and repeated reasons**

- No curator decision on OULAD's open issues exists yet, so no drift of the curator to report. The record's split
  fields were aligned by Lennart on 2026-10-19 (`required_split` set, contradicting `Non-IID (Temporal)` tag removed);
  the previous REVIEW.md's "Record fields that disagree" item is stale.
- Third exception of the same reason: "too few periods for SPLIT-14" (OULAD, nba_players, distribution_transformers):
  amendment due (item 1). Kept in-course grades against the LEAK-10 Mechanisms row: second case (dropout, OULAD).

</details>

<details><summary>Advocate</summary>

Position: ship as defined, with text fixes only (point 7). One feature choice (point 6) is a P7 call for the curator
and does not block shipping either way.

**1. A real task with a real actor and the actor's target (P3: USE-1, USE-5 Must, USE-8 Must)**

- Evidence: the practitioner (OU student-support analyst) rates the fit "approximate", agrees with the definition, and
  says "Yes, I would use it"; it found "no input I would not have". The blind reviewer, with no notes, names the same
  use case (OU Analyse, early warning) and votes "include with changes". The OU page: "All students with their risk of
  failure in their next assignment are updated weekly" (claim audit, row 2).
- Target: `final_result` is the source's own outcome (paper: "final course results"). The 4-class model's at-risk AUC
  is 0.803, a binary at-risk model gets 0.805 on the same folds, so the decision the actor acts on is fully in the
  target (USE-5 holds). The same choice was made for predict_students_dropout_and_academic_success (the source's 3
  classes, Lennart and Andrej, shipped in v0.1).
- Answers the objection "OU acts on a weekly binary next-TMA risk": that is a different dataset (one row per student x
  TMA). The practitioner lists it under "not worth doing here". USE-8 is met because `fit = "approximate"` says what
  differs.

**2. Only what is known on day 60 (P4: LEAK-10 Must, holds)**

- Evidence: the column audit finds "no new leak": every feature uses days < 60 or registration-time facts. Leak
  probes: no exact copies across the split (0.0%); the best single feature (score_mean) reaches 0.671 against 0.744 for
  all features; dropping any one feature costs at most 0.003. Both dropped post-outcome columns are gone
  (`date_unregistration`, the exam).
- The TMA marking delay of 14 days comes from the OU's own Tutor Support Statement ("ten working days"; EV-2 ranks the
  source's own documents above inference). It is the conservative choice: with no delay, skill would be 0.158 instead
  of 0.132. The blind reviewer's top concern ("filter assessments by when they were marked ... due date plus a marking
  lag") is what the code already does.
- The LEAK-10 Mechanisms row "earlier grades when the target is the final grade: drop it" is a pattern taken from
  student_portuguese_performance, where the use case predicts before G1/G2 exist. Rules win over patterns
  (principles, Conflicts). Here the marks exist on day 60 and the actor acts on exactly those marks. That matches the
  dropout sibling, which kept its first-year grades. The mildest remedy is to narrow the row's text (consistency check
  option (d)), not to drop the features.

**3. The grouped split is the mildest split the rules allow (P4: SPLIT-3, SPLIT-14 Must, SPLIT-9 Must)**

- Evidence: the shares of rows before each start date are 14.9% / 43.1% / 66.5%. Only one temporal window keeps 50%
  of the rows for training, so SPLIT-14 rules out a temporal split. The split audit's verdict is "right with notes":
  grouped is "the mildest split that holds the rules".
- The decisive experiment (EV-1) was run on the one window where both splits can be compared (2014J). There the
  grouped split is slightly *harder* (log loss 1.205 against 1.185 temporal), and the three models rank the same way
  under both. The shortcut that SPLIT-9 guards against (hotel_booking_demand: train rows that were 100% positive) is
  not present: no feature carries a later presentation's labels. On the older test presentations the measured
  optimism is +0.010 skill.
- Answers the SPLIT-9 objection: a per-fold filter to presentations that ended before the test presentation's day 60
  leaves no train rows for 2013B (100% of its train side is still running), so neither SPLIT-9 nor SPLIT-14 can be met
  as written. Exclusion is for a Must that cannot be fixed. But this is the third dataset with the same reason
  (nba_players_2016_2019 and distribution_transformers are open), and principles.md says three exceptions with one
  reason call for an amendment of the rule. Shipping with the fit marked "approximate" (the gap is named) until the
  curator decides that amendment is the remedy the ladder gives. Dropping this one dataset is not.

**4. Recurring students: not measurable, and no remedy exists that does not break a higher Must (LEAK-17, SPLIT-29 vs USE-11)**

- Evidence: 12.9% of test rows share a student with the train side. 4.9% of the rows share only earlier
  registrations, which deployment also knows, and `num_of_prev_attempts` already carries them. Measured cost: the
  claim audit finds the net effect after a random-removal control is -0.0012 +- 0.0015 log loss (not measurable). The
  split audit finds about 0.004, noisy. The gaps between models on the same rows are 0.03-0.16, so the overlap cannot
  change a ranking.
- Why it is kept: shared students link all 22 presentations into one component, so no grouping removes it. One row per
  student would break USE-11 (Must, P3: the use case scores every registration; precedent corporate_credit_rating).
  P3 outranks P4, so USE-11 wins this conflict, and the `Potential leak, kept on purpose` note with a measured cost
  follows the LEAK-30 house pattern (Lennart, 2026-10-19).
- Fix that keeps the dataset: replace "about 0.0025" with the measured range (the claim audit refuted the number, but
  the conclusion, a negligible leak, became stronger).

**5. Worth benchmarking, and every fold can be scored (P6: TP-2, TP-5)**

- Grouped LightGBM log-loss skill is 0.141 (IID 0.195). The blind reviewer measured AUC 0.746 with all features
  against 0.610 with demographics only, "the signal is real, the task is not trivial, and there is room between
  methods".
- Each test fold scores 7,694-10,563 registrations one by one, and its smallest class has 874 rows, far from
  parkinsons (`Too Small`, 2-3 units). `groups_test_groups_few` is accepted on group-probe evidence, as for
  airfoil_self_noise (2026-10-20) and musk.

**6. BBB 2014J marks kept as recorded (PROV-13 does not apply; CLEAN-1 Should, P7)**

- The 1/100 marks on a TMA with weight 0 are the OU's real record of a redesigned assessment, not damage. PROV-13
  needs a damaged release and an origin that holds clean values, and here no clean value exists to restore (precedent
  checker, fact (a)). This is what sets it apart from ashrae (unit conversion) and hepatitis_c (a recording convention
  that differs by class).
- The alternative (leave weight-0 marks out of score_mean/score_min) is a cleaning choice at P7. It does not move
  models together: LightGBM goes from 0.141 to 0.167, but random forest goes from 0.168 to 0.158 (BBB 2014J: -0.07 to
  -0.24). It changes the ranking of methods, so the choice should not rest on which version scores better (the spirit
  of SPLIT-21).
- Concession: the practitioner says an OU analyst would compute scores over summative assessments only. If the curator
  agrees, this is a cheap feature-definition fix (rung 2 of the ladder) and the dataset ships with it. Either way it
  is no reason to hold the dataset.

**7. Provenance holds; the refuted claims are text fixes (P5: PROV-8, PROV-9, PROV-10; writing.md)**

- Facts: the figshare zip's md5 matches the stated hash, and all 7 CSVs are byte-identical to the local files. The UCI
  copy equals them once "?" is removed and the line endings are normalised. CC BY 4.0 is confirmed in the figshare
  API. 44 of the 48 claims hold or hold in part.
- The refuted ones, all fixable in text: 8 of the 6,190 dropped registrations are Fail, not Withdrawn; `known` omits
  num_of_prev_attempts and studied_credits; logistic regression gives 0.732, not 0.717; the leak cost number (point
  4); the OULAD quote is analysis advice, not how the OU trains (rephrase it, keeping the reasoning of point 3);
  REVIEW issue 7's "only dataset" is stale; add the figshare DOI to `source_links`.
- 93 Withdrawn rows without an unregistration date (0.35% of rows; 84 show no activity on days 46-59): add a note
  with these numbers to the Anomaly bullet. Dropping them would apply a cohort rule from an inferred date, which is
  weaker evidence (EV-2: inference ranks last). The timing of `studied_credits` is an open question (LEAK-10, weak).
  The data shows a registration-time value shared across concurrent registrations; a note covers it.

Judgment record:

```text
Verdict: ship (text fixes; one P7 option for the curator).
Validity: USE-1/USE-5/USE-8 hold (approximate fit, named); LEAK-10 holds (TMA lag from OU policy, conservative);
SPLIT-3 vs SPLIT-14/SPLIT-9 forced departure, measured as not optimistic on the comparable window, amendment due
(third case); LEAK-17 kept under USE-11 (higher rank), cost not measurable; PROV-10 holds (md5).
Value: TP-2 real signal (skill 0.141); TP-5 not Too Small (smallest class 874 per fold).
Quality: CLEAN-1 BBB 2014J weight-0 marks kept with a note (alternative open for the curator).
For the curator: the SPLIT-14 amendment; the LEAK-10 Mechanisms row wording; BBB 2014J.
```

**Rebuttal**

The critic does not argue for exclusion, and we agree on most of the facts. I concede points 1 (text part), 4, 6
and 7, and point 5 as a feature fix. I dispute two changes to the definition (point 2's train filter, point 3's
cohort filter) and the order in point 1(b).

**1. SPLIT-9 / SPLIT-3: partly conceded**

- Conceded: rewrite the OULAD quote as advice to use the previous presentation (claim audit 33/43), and add the 68%
  figure to `fit_reason`.
- Conceded: SPLIT-9 is a Must with no exceptions, so this split needs the curator's amendment of SPLIT-14 / SPLIT-8
  (the third case).
- Disputed: that the amendment must come "before this ships". All three cases (this one, nba_players_2016_2019,
  distribution_transformers) wait on the same decision. It belongs in this dataset's REVIEW.md as a curator issue,
  which is where it already sits. It is not a change to the definition. The critic agrees on the measurement:
  grouped is not optimistic on the one comparable window (1.205 against 1.185), and the models rank the same way.

**2. LEAK-17 train filter: disputed; the number fix is conceded**

- Conceded: replace "about 0.0025" with the measured range (raw +0.002 to +0.005; net not distinguishable from zero),
  and the curator records how LEAK-17 applies (a narrowing, or a Cases row).
- Disputed: the per-fold filter. The rule for this step is the remedy ladder: take the mildest remedy that resolves
  the problem. A note resolves it, because no effect is measurable. Claim audit: net -0.0012 +- 0.0015. Split audit:
  0.0050 against 0.0006 for the random-removal control, driven by one fold (0.0126; the other two 0.0022 and 0.0001).
  The gaps between models are 0.03-0.16.
- The filter also does not do what the critic claims, removing "the part deployment would not have". It removes
  606-866 future rows per fold that belong to shared students. It keeps the 68% of train rows that come from
  presentations still running at the test presentation's day 60 (point 1). The future stays on the train side; only
  its smaller, unmeasurable part goes. That trades a custom per-fold mechanism for no gain we can measure (EV-1:
  facts first).

**3. Dropping the 93 dateless Withdrawn rows: disputed (USE-3, against selection on the label)**

- New fact (the claim audit's frame): 4,197 cohort rows have no click on days
  46-59. Of these, 940 are Withdrawn, 2,398 Fail, 712 Pass and 147 Distinction.
- The proposed filter drops a row only when its label is Withdrawn and its date is missing. On day 60 the OU could not
  tell those 84 inactive rows from the 3,257 inactive rows that went on to Fail or Pass. So the filter selects on the
  target, and it removes a slice of exactly the inactive-and-withdrawn pattern that the task is meant to score.
- USE-3 does not decide this either. "A field that is blank because the outcome already happened" is about a
  feature. Here the blank is in `date_unregistration`, which is dropped, and that the withdrawal came before day 60 is
  inferred, not recorded (EV-2: inference ranks last).
- Remedy: the critic's own fallback, the numbers in the Anomaly bullet (0.35% of rows).

**4. TMA delay and kept grades: conceded**

- (a) Add a sentence: the delay is an assumption from the OU policy. With no delay the skill is 0.158 instead of
  0.132.
- One correction: 14 calendar days is exactly ten working days with no slack for holidays, so the assumption could
  err toward leaking. That is one more reason for the note.
- (b) As in my point 2: the curator narrows the LEAK-10 Mechanisms row.

**5. BBB 2014J: conceded as a definition fix**

- USE-6 (Must) applies: the assessment weight is known on day 60 (`assessments.csv`), and the practitioner says an OU
  analyst would use it.
- That fact sets this case apart from "a deployed model meets such redesigns": the deployed model would also see the
  weight.
- I withdraw my point 6. The fix is to leave weight-0 marks out of `score_mean` / `score_min` (or add the weight). The
  critic's reading of the random forest number is fair: the fix is not tuned toward one model.

**6 and 7. Conceded**

- Correct each refuted sentence (claims 5, 18, 21/40, 38).
- Say day 60 was chosen for the use case (after the first marks are back), not from the sweep (SPLIT-21).
- Add one sentence on `studied_credits`; do not drop it.

**Remaining dispute for the mediator**

- The train filter (2): the ladder says a note, because no effect is measurable.
- The cohort filter (3): the filter selects on the target; a note instead.
- The order in 1(b): whether the curator settles the amendment before shipping or in this review's issues.

**Updated position**

Ship after changes:
- text fixes (1, 2, 4, 6, 7);
- the weight-0 marks out of the scores (5);
- curator issues for the SPLIT-14, LEAK-17 and LEAK-10 amendments.

</details>

<details><summary>Critic</summary>

Position: **ship only after changes.** The task is real (the practitioner and the blind reviewer would both use it) and
I do not argue for exclusion. Two Must departures in P4 are kept with no fix and no amendment, one cohort rule is
broken for a few rows, and one feature choice makes a single presentation set the fold variance. Ranked by
principles.md: validity first, Must before Should.

**1. P4, SPLIT-9 / SPLIT-3 (Must): training holds labels that are unknown at the test's prediction point**

- Problem: the grouped split trains on presentations that are still running on the test presentation's day 60.
  Averaged over test rows, 68.0% of a fold's train rows come from such presentations, and 38.9% of test rows have no
  earlier presentation of their module that deployment could use (split_audit, issue 1).
- Effect: the benchmark scores a model trained on the future. The split auditor measured the cost where it can: on the
  2014J rows grouped is slightly harder than temporal (log loss 1.205 against 1.185) and ranks the three models the same.
  So the measured harm is small, and I accept that grouped is the closest split that SPLIT-14 allows.
- What is wrong is how the definition justifies it. It quotes the OULAD page as "the OU trains on other presentations
  of the same module". In context the quote is analysis advice to use the *previous* presentation, which argues for a
  temporal split, not for this one (claim_audit 33/43).
- Rule: SPLIT-9 is a Must, and a Must has no exceptions (principles.md, Strengths). This is the third dataset where
  "too few periods for SPLIT-14" set the regime, after nba_players_2016_2019 and distribution_transformers
  (precedents, item 1), so an amendment is due (principles.md, consistency case 4).
- Remedy: (a) rewrite the `grouping.definition` and `fit_reason` text: give the quote as advice for temporal use, and
  add the 68% figure; (b) the curator decides the SPLIT-14 / SPLIT-8 amendment (what a task with too few periods ships
  as) before this ships, so that the three cases are settled alike. Do not exclude.

**2. P4, LEAK-17 (Must): recurring students are kept, and the stated cost is wrong**

- Problem: 12.9% of test rows have the same student on the train side (claim_audit 8; split_audit 13.0%). For 8.1% of
  test rows that student appears in a concurrent or later registration, which deployment would not know.
- Evidence on the cost: the definition says "about 0.0025 log loss". The claim auditor found +0.0050 raw and
  -0.0012 +- 0.0015 net of a random-removal control. The split auditor found about 0.004 net (0.0022 / 0.0126 / 0.0001
  over three folds). Neither reproduces 0.0025.
- Rule: LEAK-17 is a Must, and its two remedies (one row per student, group by student) cannot be applied here
  (USE-11; all 22 presentations are linked by shared students). It is the first repeated-entity leak in the copy kept
  on purpose (precedents, item 5).
- Remedy: the definition can be fixed, so it should be: a per-fold train filter that drops the concurrent and later
  registrations of test students (606-866 train rows per fold; split_audit, issue 2). This removes the part that
  deployment would not have and keeps the earlier registrations, which deployment knows. If the split API cannot take
  that filter: replace the number with the measured range (0.002-0.005 raw; not distinguishable from zero net), and
  the curator records the LEAK-17 narrowing as an amendment.

**3. P3/P4, USE-3 and LEAK-1 (Must): the cohort keeps students who had most likely withdrawn before day 60**

- Problem: 93 Withdrawn registrations have no `date_unregistration` and stay in the "active on day 60" cohort. Of
  these, 84 have no click on days 46-59 (against 22% of withdrawals that have a date), 65 last clicked before day 60,
  and 19 never clicked. All 93 are in 2014J presentations (claim_audit 30).
- Effect: these rows break the stated cohort rule, and USE-3 names this case ("a field that is blank because the
  outcome already happened"). The effect is small: 0.3% of rows.
- Remedy: fix the definition by dropping the Withdrawn rows without an unregistration date that have no click on
  days 46-59, and give the count in the cohort bullet. If the curator prefers to keep them, give the numbers in the
  Anomaly bullet instead.

**4. P4, LEAK-10 (Must): the 14-day TMA delay is assumed, and the kept grades depart from the rule as written**

- Problem 1: the data has no return date for TMAs. The 14-day delay comes from a policy approved in 2012 and updated in
  2019, and it is load-bearing: with no delay, skill is 0.158 instead of 0.132 (the previous REVIEW.md, issue 4; claim_audit 17,
  untested).
- Problem 2: `score_mean` and `score_min` keep grades that make up 10-30% of the continuous-assessment weight of the
  final result. LEAK-10's Mechanisms row says "earlier grades when the target is the final grade: drop it" and allows
  no prediction-point exception (precedents, item 2).
- My position: keeping the grades is right for this use case, because the tutors act on those marks. But the rule as
  written says otherwise, and the definition does not mention it.
- Remedy: (a) add a sentence on the delay to the notes: it is an assumption, with the sensitivity above, so that a
  later source on 2013-14 return times can correct it; (b) the curator narrows the Mechanisms row to "earlier grades
  not yet known at the prediction point", or records why this case differs from student_portuguese_performance.

**5. P3/P5, USE-6 (Must), PROV-13 (Must), CLEAN-1 (Should): BBB 2014J's weight-0 marks are scored as if they were grades**

- Problem: BBB 2014J's first TMA has weight 0 and is marked 1 or 100 (1,739 of 1,776 marks). On day 60 it is that
  presentation's only known score.
- Effect: untuned LightGBM scores below the class prior on BBB 2014J (skill -0.42). The three weakest splits are the
  three that test it, so one presentation sets the fold variance (claim_audit 29).
- Why the stated reason does not hold: the reason given is "a deployed model meets such redesigns". The practitioner
  answers that an OU analyst knows the module's assessment weights and would compute "scores known" over summative
  assessments only. The weight is known at the prediction point (in `assessments.csv`), so USE-6 makes it a
  legitimate input, but the definition withholds it. The same reason was not accepted for ashrae's sites (precedents,
  item 9).
- Remedy (a feature fix, not a relabel): leave weight-0 assessments out of `score_mean` and `score_min`, or add the
  known assessment weight as a feature. On the 9 splits this changes LightGBM from 0.141 to 0.167, the standard
  deviation over splits from 0.052 to 0.016, and BBB 2014J from -0.42 to 0.02. Random forest drops from 0.168 to
  0.158, so this is not tuned toward one model.

**6. Procedure, writing.md and EV-8: claims that the audit refuted (repair the text; no reason to withhold)**

- `known` leaves out `num_of_prev_attempts` and `studied_credits` (claim 5).
- "6,190 ... whose result (Withdrawn) is already known": 8 of those rows are Fail (claims 21/40).
- The accepted warning quotes logistic regression at 0.717; today's probe gives 0.732 (claim 38).
- The cost of 0.0025 (see point 2).
- "the log starts 25 days before": the start ranges from day -25 to day -8 depending on the presentation (claim 18).
- Day 60 was picked alongside a sweep of skill over days 0/30/60/90. The record should say it was chosen for the use
  case (an early-warning point after the first marks are back), not for its score (precedents, item 2; SPLIT-21).
- Remedy: correct each sentence. This is quality; it is no reason to exclude.

**7. Procedure, studied_credits timing (LEAK-10, a question rather than a finding)**

- The codebook says "currently studying" and gives no date. The value is equal across concurrent registrations,
  withdrawn ones included, which fits a total taken at registration. Its timing cannot be tested (column_audit,
  problem 2). Per EV-6 this is a question, not a finding.
- Remedy: one sentence in curation_comments. Do not drop the column.

**Summary of asks**

- Fix the definition: points 2 (train filter), 3 (cohort filter) and 5 (weight-0 marks).
- Fix the text: points 1, 4a, 6 and 7.
- Curator decisions before shipping: amendments for SPLIT-14/SPLIT-8 (point 1), LEAK-17 (point 2, if no filter) and
  the LEAK-10 Mechanisms row (point 4b).

**Rebuttal**

Changed position: still **ship after changes**, but with fewer of them. Two changes to the definition are left
(advocate's point 4, and point 6 in its milder form), plus the text fixes. No new facts.

**Advocate's point 1, a real task (USE-1, USE-5, USE-8): concede**

The practitioner, the blind reviewer and the at-risk AUC (0.803 against 0.805) back it. I raised nothing against it.

**Advocate's point 2, known on day 60 (LEAK-10): concede, with one correction**

- I concede that the code does what the blind reviewer asked, and that the Mechanisms row is a pattern. Rules win over
  patterns, and we agree on the remedy: the curator narrows the row's text.
- I dispute "conservative". The 14-day delay is conservative only compared with no delay. If 2013-14 TMAs came back
  later than 14 days, scores enter before they were known. The data cannot test this (claim_audit 17, untested).
- The ask stays a note: the delay is an assumption, with the sensitivity (0.132 against 0.158). That is not a change
  to the definition.

**Advocate's point 3, the grouped split (SPLIT-3, SPLIT-9, SPLIT-14): concede the facts, keep one ask**

- I concede that a SPLIT-9 filter leaves 2013B with no train rows, that the measured comparison does not show
  optimism (1.205 against 1.185 on 2014J), and that exclusion is wrong. I had already asked for no exclusion.
- What is left is an order of steps. principles.md (Strengths) says a Must has no exceptions, and anything else is an
  amendment. Shipping before the SPLIT-14 / SPLIT-8 amendment is decided ships a Must departure with no rule to
  cover it.
- Ask: the curator decides the amendment for all three datasets in the same pass that ships this one. This is a
  weighing call on timing for the curator, not a blocker I can prove.

**Advocate's point 4, recurring students (LEAK-17 against USE-11): dispute**

- The advocate argues against a remedy I did not propose. I did not ask for one row per student. I asked for a
  per-fold train filter: drop from train the concurrent and later registrations of the fold's test students (606-866
  train rows per fold; split_audit, issue 2).
- That filter changes no test row and no cohort, so USE-11 is untouched and there is no conflict for P3 to win.
- LEAK-17 is a Must, and a Must is "fixed in the definition when it can be" (principles.md, Strengths). This one can
  be. It removes exactly the 8.1% of overlap that deployment would not have, and keeps the earlier registrations
  (4.9%), which deployment knows.
- The LEAK-30 note pattern does not carry over. LEAK-30 covers transductive scaling, not repeated entities, and the
  precedent checker found no repeated-entity leak kept on purpose (precedents, item 5).
- Concession: the effect is not measurable (net -0.0012 +- 0.0015). So the filter is cheap insurance, not a fix for a
  shown bias. If the split API cannot express it, the fallback is the advocate's own: the measured range in the note,
  and a LEAK-17 amendment.

**Advocate's point 5, worth benchmarking (TP-2, TP-5): concede**

**Advocate's point 6, BBB 2014J (PROV-13, CLEAN-1): concede PROV-13; keep a milder ask**

- I concede that PROV-13 does not apply. No clean value exists to restore (precedents, fact (a)), and that sets the
  case apart from ashrae.
- I concede that USE-6 makes the weight a legitimate input but does not require it. My point is therefore a CLEAN-1
  Should at P7, not a validity blocker.
- On SPLIT-21: the advocate is right that we should not choose between versions by score. That argument is against
  dropping the weight-0 marks.
- Revised ask: add the known assessment weight (for example, the weight of the scored assessments by day 60) and keep
  the marks. This removes nothing, so it is not chosen by score. It gives the model what the practitioner says every
  OU analyst knows (practitioner, "What an expert would change").
- The curator's call; no reason to hold the dataset.

**Advocate's point 7, provenance and text fixes: concede**

- I concede the provenance facts and every text fix (the figshare DOI included).
- On the 93 Withdrawn rows: I concede the note. The withdrawal date is inferred from inactivity (84 of 93 inactive on
  days 46-59, against 22% in the control). That evidence is too weak for a cohort filter on 0.35% of rows. I withdraw
  the drop.

**Net asks**

- In the definition: the per-fold train filter (point 4).
- Optional for the curator: the weight feature (point 6).
- In the text: the delay note, the measured leak range, the quote, and the counts.
- For the curator: the SPLIT-14 / SPLIT-8 and LEAK-10 Mechanisms amendments, and LEAK-17 if the filter cannot be
  built.

</details>
