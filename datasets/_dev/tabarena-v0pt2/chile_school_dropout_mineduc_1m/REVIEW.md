# chile_school_dropout_mineduc

**Outcome:** added as `chile_school_dropout_mineduc_1m`. The AI recommends shipping it: the review panel's changes
are made and three calls are left to you. One change goes beyond the source's recipe. A foreign student's provisional
school id is replaced by the national id once issued, so the student's masked id changes between two yearly files and
the open files show a dropout. We link such a student to the one new id at the same school with the same sex, birth
month and home commune, at the same or the next grade, and label the student "No" (10-19% of each year's dropouts). By
a placebo test (the birth month shifted by one or two months), 10-26% of these links are wrong (up to 32% at the upper
bound), so the re-link removes three to nine wrong dropouts for each one it adds. The task is Rodriguez et al.
(2023): at the close of a school year, will a Chilean student of 1st basic to 4th secondary be out of regular schooling
next year? It is built from Mineduc's open yearly files of 2017 to 2025 (19.4 million student-years 2018-2024),
shipped as 3 yearly test windows of 500k students with 1M earlier students each for training; fallback `roc_auc`.
Verdict: ship after changes (made).
Validity: SEL-1, SEL-2 hold; USE-1, USE-3, USE-6, LEAK-10, LEAK-37 hold (an end-of-year list; year t's outcomes are
inputs, as in the source's final model); USE-5 triggered (students whose masked id changed between two files counted
as dropouts) and fixed in the definition by the re-link above (LEAK-22: relabelled, never dropped); the residue (deaths, emigration, exam-route graduates,
id changes the link misses) is named and the fit stays approximate (USE-8); the students who move to an adult course during the year are no rows
(8,526 in 2023, about a tenth of a year's dropouts), a departure from the source's cohort chosen by an input known at
the close, noted; SPLIT-1, -9, -10, -11, -14 hold; SPLIT-20
notes added (the COVID-19 attendance recording of 2020-2021, special education from 2023); a LEAK-9 protocol line
added (a participant who reads rows outside its split gains 0.017 ROC AUC).
Value: the task probes flag nothing on the re-linked labels (linear 0.893, LightGBM 0.883, random forest 0.876 ROC AUC, best single feature 0.794; 3 windows); the leak probes flag nothing (no copies across the split, no censoring in the newest years); untuned LightGBM 0.870-0.878 ROC AUC on the 3 windows; 11,331 / 12,295 / 12,005 positives in the
2024 / 2023 / 2022 test windows; `roc_auc` fallback (MET-6; the reason now names GM as the paper's one criterion).
Quality: CLEAN-12 the TP sector, specialty and mention decoded from the codebook's Anexos VI and X; CLEAN-14
`combined_course` keeps its six codes; CLEAN-11 ages of 4 or under missing; CLEAN-21 a previous year in special
education reads "not enrolled"; `school_id` kept (CLEAN-3, USE-10).
Weighed: size +, source + (the ministry's census files and a paper), gap - (measured: education, binary classification
and temporal are not thin among the accepted definitions; school dropout is still a new task next to the university
dropout of predict_students_dropout_and_academic_success), residual label noise -.
For the curator: issue 1 (all grades or grades 7-12), issue 2 (keep the students withdrawn during the year),
issue 3 (a written case for a label repaired by our own link). Shipping accepts the check warning on the 7 yearly time
points, as for three yearly datasets before.

**Main points:** Three calls: keep every grade from 1st basic, the source's population (implemented, recommended), or
only 7th basic to 4th secondary, the ministry's warning list (issue 1); keep the students withdrawn during the year on
the end-of-year list (issue 2, a confirmation); and whether our re-link of changed ids becomes a standing case of the
label rule (issue 3).

**Record judgment:** valid. The record's fields agree with the definition. The size check's 3.18% dropouts for 2023
also counted the students who ended the year in adult education, who are no rows here (2.92%); after the re-link the
rate is 2.46%.

**Issues for Lennart:**

1. **Keep every grade from 1st basic, or only 7th basic to 4th secondary, the grades of the ministry's warning list?**

   * **Problem:**
     - The rows cover every children's and youth grade from 1st basic, as the source paper and the ministry's dropout rate do, while the ministry's early warning system lists only students of 7th basic to 4th secondary (grades 7-12 below; 1st to 6th basic are grades 1-6) (the 10% of each school at highest risk)[^use1].
     - Grades 1st to 6th basic are 53-56% of the rows and, after the re-link, still 26-39% of the dropouts, at a third to half the dropout rate of the upper grades.
     - About half of these younger dropouts were promoted in their last year: children who vanish from the files (emigration, home schooling by examination, id changes the re-link cannot find) more than children who leave school[^use5].
   * **Background:**
     - The re-link: an absent student is matched to a single id new in the next year's file at the same school, with the same sex, birth month and home commune, at the same or the next grade, and counts as enrolled; it relabels 10-19% of each year's dropouts.
     - The early warning system (Sistema de Alerta Temprana, since 2019) gives each school director the list of "the 10% of highest risk" of their students in 7th basic to 4th secondary (Mineduc, IDPS retention sheet 8: https://www.curriculumnacional.cl/614/articles-90161_galeria_11.pdf).
     - Mineduc's dropout rate of the regular system (2.4% for 2018) and the paper (Sec. 3.2, a test year of 2,802,156 trajectories) count every children's and youth grade.
   * **Effect on the task:**
     - With all grades, about a third of the positives come from grades the deployed list leaves out, where the label is noisiest; part of the score rewards finding promoted young children who vanish from the files.
     - With grades 7-12 only, the task is the list's population (8.7 million student-years, 61-74% of the dropouts); the score no longer covers the national rate the source and the ministry report[^use8].
   * **Experiments:**
     - On the re-linked labels, per school year (all rows, not the sample):

       | | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 |
       |---|---|---|---|---|---|---|---|
       | grades 1-6, share of dropouts before the re-link | 30.0% | 35.5% | 42.5% | 36.4% | 38.6% | 40.5% | 38.7% |
       | grades 1-6, share of dropouts after | 26.4% | 32.5% | 38.5% | 33.8% | 36.3% | 38.7% | 36.1% |
       | grades 1-6, dropout rate after | 1.04% | 1.31% | 0.84% | 1.04% | 1.59% | 1.76% | 1.54% |
       | grades 7-12, dropout rate after | 3.72% | 3.52% | 1.72% | 2.51% | 3.39% | 3.29% | 3.10% |
       | promoted share of the grades 1-6 dropouts after | 50.1% | 51.4% | 63.1% | 59.0% | 49.2% | 46.0% | 47.2% |

     - The re-link lowers the grades 1-6 share by only 2-4 points: the noise that stays there is mostly not the id change.
     - Untuned LightGBM, 300k training rows, the 3 shipped windows (2024 / 2023 / 2022; a separate run from issue 2's, with another draw of the training rows): trained on all grades, ROC AUC 0.871 / 0.873 / 0.877 on all rows, 0.844 / 0.853 / 0.836 on grades 1-6 and 0.881 / 0.882 / 0.897 on grades 7-12; trained and scored on grades 7-12 only (option B), 0.888 / 0.889 / 0.898, scored on the grade 7-12 rows of the shipped test windows (7,206 to 7,683 positives); a rebuilt B draws its 500k test rows from grades 7-12 alone, about 15,500 to 17,000 positives a window at 3.1-3.4% (an estimate from the rates above).
     - The domain practitioner (before the re-link): on grades 7-12 the model beats the rule a school team uses today (withdrawn, then failed, then attendance under 85%) in every window, pooled 0.855-0.883 against 0.783-0.812, and a 10% list per school catches about 60% of the school's dropouts.
   * **Consistency:**
     - No earlier dataset settled a population narrower than the source's for a deployed system's scope; the precedent checker found no direct precedent, and the choice is a weighing call.
   * **Panel:**
     - All grades (advocate): the paper and the ministry's national rate cover every grade, and the task is the paper's.
     - Grades 7-12 (critic, domain practitioner): the deployed list is grades 7-12, and grades 1-6 carry a third of the positives at half the rate, about half of them promoted children, where the label is noisiest.
     - The mediator: the re-link did not settle it (the advocate's forecast that it would lean to all grades is weak, the critic's that the emigration stays is borne out); your weight on the actor's list against the source's population decides.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | All grades (implemented) | rows from 1st basic to 4th secondary; 19.4 million student-years; `use_case` says the ministry's list covers grades 7-12 and the rows go wider | the source's and the ministry's population; the national rate; the largest task | a third of the positives outside the deployed list; the noisiest part of the label |
     | B | 7th basic to 4th secondary | rows of grades 7-12 only; 8.7 million student-years, 61-74% of the dropouts | the deployed list's population; less of the vanishing-children noise | departs from the source's population; loses the younger grades the ministry's rate counts; raises whether to score it by the per-school top 10% of the list, a rule amendment |

   * **Recommendation:** A, the source's population, with the use-case sentence that names the list's grades; B if you weigh the deployed list over the source. **Decision:** A or B?

   **Notes for the AI:**
   - B: in `_clean`, keep the rows with a grade level of 7 or more (`cod_ense2 == 2` and `cod_grado >= 7`, or secondary) before the codes are dropped; keep `_prepare_raw_files` and the re-link over all grades (the history and the links need them). Rewrite `task_summary.row`, `use_case` (the list's population), `fit_reason` (no grades sentence), the Rows bullet and the rates; re-run `dataset check`, the leak, task and hidden-group probes. Then ask, as an amendment of MET-1 / MET-5 and not as an exception, whether the per-school top-10% precision on grades 7-12 (domain practitioner, MET-7) should score it: under A it scores no decision the source fixes.
   - On the verdict ship (any option), the proposed acceptance of the one check warning, for the curator to write into `accepted_check_warnings`: `"task_time_on_few_unique": "the time unit is the school year: the label and the refit are yearly, and the history starts in 2018 (SPLIT-20); 7 school years are the task's time points"`, as accepted for wisconsin_local_government_property_insurance_fund, spanish_homeowners_motor_insurance_2010_2014 and tunisian_fraud_detection_challenge.

   [^use1]: **USE-1** (Must): a use case is an actor, a moment and a decision; check every filter, target and split choice against it.
   [^use5]: **USE-5** (Must): predict what the actor would act on, at the resolution they act on it; check how the source built its label. A label checked and found to be another quantity still fails (Lennart, 2026-10-21, diabetes_3); corporate_credit_rating (2026-10-16) was rebuilt when 17% of its checkable labels were not the quantity.
   [^use8]: **USE-8** (Must): write how closely the data mirrors the use case; approximate is a stand-in with a known gap, named as such.

2. **Keep the students withdrawn during the year on the end-of-year list?**

   * **Problem:**
     - A student withdrawn during year t (1.3% of the rows) has already left the school when the list is drawn at the close of the year, and two thirds of them are out of regular schooling next year: they are 41% of the dropouts after the re-link.
     - Their status is known at the prediction point and the source's final model uses it, so no rule asks to remove them; the blind reviewer calls this part of the task bookkeeping and would drop them or move the prediction point to the start of the year.
     - The definition keeps them, so the list serves both the retention of students still enrolled and the re-engagement of those who left.
   * **Background:** for a withdrawn student the action is re-engagement ("revinculación") by the local education service or the ministry, not retention by the school; both act on the same end-of-year list (domain practitioner).
   * **Effect on the task:** with them, part of the score is for flagging students who have already left (on all rows the final status alone scores 0.78-0.79 ROC AUC, the full model 0.87-0.88); on the students still enrolled at the close, the same model scores 0.77-0.79.
   * **Experiments:**
     - Untuned LightGBM, 300k training rows, the 3 shipped windows (2024 / 2023 / 2022), re-linked labels: all inputs 0.871 / 0.870 / 0.878; scored only on the students not withdrawn 0.775 / 0.769 / 0.787; without year t's final status, grade average, attendance and transfers (a start-of-year list) 0.751 / 0.737 / 0.757; the final status alone 0.776 / 0.783 / 0.788.
     - On the shipped rows, 66.6% of the withdrawn students drop out, against 0.9% of the promoted and 17% of those who failed.
   * **Consistency:** open_university_learning_analytics_dataset kept everything known on day 60 as inputs; here the source's final model uses whether the last grade was approved and the last cycle's attendance[^l37].
   * **Panel:**
     - Drop them, or predict at the start of the year (blind reviewer): an early warning flags students still enrolled, early enough to act.
     - Keep them (domain practitioner, advocate, critic, mediator): re-engaging the withdrawn is a real decision on the same list, the task stays hard without them (0.77-0.79), and their status is known at the point[^use6].
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep them (implemented) | every student of the year's end, the withdrawn included; ROC AUC 0.87-0.88 | the source's population and prediction point; both decisions on one list | an easy part in the score (41% of the dropouts) |
     | B | Drop the withdrawn students | rows whose year ended withdrawn leave; the label keeps its definition | the list of students still in school; a harder task (about 0.77-0.79 ROC AUC on these rows) | departs from the source's cohort; leaves out the students the re-engagement acts on |
     | C | A start-of-year list | year t's final status, grade average, attendance and transfers leave the inputs; ROC AUC 0.74-0.76 | warns earlier, before the year's outcomes | not the source's prediction point; drops inputs the actor has at the close of the year |

   * **Recommendation:** A, the source's framing: the withdrawn students' status is known when the list is drawn, and re-engaging them is a decision the ministry takes on the same list. **Decision:** A, B or C?

   **Notes for the AI:**
   - B: in `_clean`, drop the rows whose `final_status` is withdrawn (an input at the prediction point, so no outcome filter); rewrite `task_summary.row`, the Rows bullet and the withdrawn note; re-run `dataset check`, the leak and task probes.
   - C: drop `final_status`, `gpa`, `attendance_pct` and `transfers_in_year` in `_clean`; move the prediction point in the first bullet, `task_summary.known` and `use_case` to the start of year t (the label stays enrolment in t + 1); re-run the same checks.

   [^use6]: **USE-6** (Must): anything known at the prediction point is a legitimate input.
   [^l37]: **LEAK-37** (Must; applies USE-6): an input the actor knows at the prediction point is not a leak. **LEAK-10** (Must): a feature holds only what existed at the prediction point; the final status of year t is recorded at its close, before the label's year starts.

3. **Make a label repaired by our own record link a standing case of the label rule?**

   * **Problem:**
     - We re-linked students whose masked id changed between two yearly files and relabelled them "No" (10-19% of each year's dropouts), the first definition in the working copy that repairs a label with a record link of our own.
     - The link is probabilistic: by a placebo with the birth month shifted, 10-26% of the links are wrong (up to 32% at the upper bound), so it removes three to nine wrong dropouts for each one it adds.
     - Should this become a standing case of the label rule, for other datasets built by linking pseudonymised ids across yearly files[^use5c]?
   * **Background:** an absent student of year t is linked when exactly one id new in t + 1 has a row at the same school, with the same sex, birth month and home commune, at the same or the next grade, one to one; linked students come back under their old id two years on at 2-6%, against 14-26% of the unlinked promoted absent students.
   * **Consistency:** corporate_credit_rating was rebuilt from the origin when 17% of its checkable labels were another quantity; diabetes_3 kept a label nobody could check as approximate; here the repair comes from the open files, not the origin.
   * **Panel:**
     - Advocate (opening): a link of our own that is wrong that often is not plainly better than documented noise; conceded in rebuttal once the stricter key was measured.
     - Critic and mediator: a checked label error the definition can fix must be fixed; the question is only whether the conditions become a written case.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Re-link here only (implemented) | the re-link stays in this definition; no case is written | no rule text from one case | the next dataset with the same id problem has no written basis; this re-link needs the fact that sets it apart |
     | B | Re-link and a case under the label rule | the re-link stays; a case records the conditions: a link of our own, its placebo false-link rate stated, used when it removes several wrong labels for each one it adds | one test for the siblings that link yearly files; the repair rests on a written basis | a heuristic of ours becomes a precedent from one case |

   * **Recommendation:** B: the repair already follows the remedy ladder, and the case only records when a link of our own is good enough. **Decision:** A or B?

   **Notes for the AI:** on B, add a Cases row under USE-5 in `use_case.md` (case chile_school_dropout_mineduc, 2026-11-09) with the wording of option B. On A, add a curation_comments bullet with the fact that sets the case apart (Mineduc documents the IPE-to-RUN change; the placebo rate is measured), or the re-link goes back to a note, which departs from corporate_credit_rating.

   [^use5c]: **USE-5** (Must): the label is what the actor acts on; a label checked and found to be another quantity still fails (Lennart, 2026-10-21, diabetes_3); remedy ladder: fix the definition before keeping with a note (corporate_credit_rating, 2026-10-16).

**Review panel:** ship after changes (mediator). Tier full: claim auditor, column auditor, split auditor, domain
practitioner, blind reviewer, task gamer, precedent checker, advocate and critic with one rebuttal each, mediator. Claim
audit: 26 claims tested; the label's completeness refuted (id changes counted as dropouts; fixed by the re-link), the
metric reason half refuted (reworded), one count off by one (corrected), one untested (the ministry's warning-system page
refused the connection).
Blind review: include with changes; its main concern is the withdrawn students (issue 2). Task gamer: one exploit,
+0.017 ROC AUC by reading rows outside the split (a protocol line). Debate: agreed on the prediction point, the split,
the fallback metric and the cleaning fixes; the re-link was disputed (a note or a repair) until the advocate
conceded the repair in rebuttal; the grades stay a weighing call (issue 1); new ground: no earlier definition repairs a
label with a link of our own (issue 3). Outside the mediator's report, issue numbers are the builder's draft: its issue
3 is issue 1 here, its 2 is issue 2, its 1 is the re-link, and its 4 and 5 (school_id, licence) were dropped.

<details><summary>Mediator</summary>

MEDIATOR REPORT: chile_school_dropout_mineduc (folder chile_school_dropout_mineduc_1m), 2026-11-09
Read: principles.md; every panel report; advocate and critic briefs with rebuttals; builder_report.md; dataset.py;
the record. Decisive measurement: P/work_mediator/relink.py (+ relink.log, relink_summary.csv, linked_strict.parquet)
and placebo2.py (+ placebo2.log), on scratch/years/*.parquet and student_years.parquet, POLARS_MAX_THREADS=4.

**1. RECOMMENDATION (judgment record)**

Verdict: ship after changes.
Validity: SEL-1, SEL-2 hold; USE-1, USE-3, USE-6, LEAK-10, LEAK-37 hold (end-of-year list, year t's outcomes are
  inputs, the source's own final model uses them); USE-5 triggered (id changes counted as dropouts, 10-19% of
  positives), fixed by a re-link that relabels the linked students "No" (rule and placebo below); what remains
  (deaths, emigration, exam-route graduates, unlinked id changes) is named and the fit stays approximate (USE-8,
  diabetes_3 path); LEAK-22 holds (relabel, never drop); SPLIT-1, -9, -10, -11, -14 hold; SPLIT-20 holds, two notes
  to add.
Value: TP no flags (re-run after the re-link; about 11.3k-12.3k positives per test window remain); roc_auc fallback
  holds by MET-6 alone, reason reworded (MET-5).
Quality: CLEAN-12 decode tp_sector, tp_specialty, COD_MEN; CLEAN-14 combined_course's six codes; CLEAN-11 ages <= 4
  missing; CLEAN-21 prev_programme "special education" recoded; writing fixes.
Weighed: size +, source + (ministry census, paper), gap + (K-12 dropout), residual label noise -.
For the curator: issue 1, a weighing call (all grades or the SAT's 7th basic to 4th secondary); issue 2, confirm the
  end-of-year framing with withdrawn students kept.

**2. THE DECISIVE MEASUREMENT: the re-link rule**

The panel's false-link figures disagreed because they used different keys: the column auditor's 45% (13.7% chance vs
30.8%) has no uniqueness and no commune; the claim auditor's placebo (about a third of matches) has commune but no
uniqueness; the precedent checker's controls (3-5% vs 19-22%) have neither. I measured the rule both sides now name.

Rule S: a student of year t absent from the file of t+1 is linked when exactly one id NEW in t+1 (in no file
2017..t) has a children's or youth row in t+1 at the same school (RBD), same sex, same birth month (YYYYMM), at the
same grade or the next one, and that new id is the candidate of exactly one absent student (one to one). Students with
the placeholder birth month or sex 0 are never linked.
Rule SC: S plus the same home commune (non-zero) as a key.
False links, three estimates: (U) birth month shifted -2,-1,+1,+2, same rule (upper: a shifted month can hit another
student's real partner); (L) the same with the really linked new ids removed; (C) enrolled controls (same id in
t+1), same rule, link rate / the absent students' link rate.

  year  dropouts  S links  S false U / L / C      SC links  SC false U / L / C   rate before -> after SC  relabelled
  2018    66,856    7,250   34% / 27% / 18%          6,934   26% / 21% / 13%       2.46% -> 2.21%          10.4%
  2019    70,145    7,926   25% / 16% / 10%          7,819   19% / 12% /  7%       2.56% -> 2.27%          11.1%
  2020    40,940    7,570   20% / 14% /  8%          7,458   15% / 10% /  5%       1.50% -> 1.22%          18.2%
  2021    52,766    6,150   42% / 34% / 23%          5,753   32% / 26% / 18%       1.90% -> 1.69%          10.9%
  2022*   78,273   10,712   39% / 28% / 17%         10,526   28% / 21% / 12%       2.77% -> 2.40%          13.4%
  2023*   82,257   12,757   36% / 24% / 14%         12,935   26% / 18% /  9%       2.92% -> 2.46%          15.7%
  2024*   78,300   14,472   32% / 21% / 13%         14,880   24% / 15% /  8%       2.80% -> 2.27%          19.0%
  (* test windows)

Validation that a link is the same student: linked absent students reappear under their old id in t+2 at 2.3-6.4%,
against 14-26% for unlinked PROMOTED absent students (85-95% of the linked were promoted); 79-86% of the linked new
ids are still in the files in t+2.

Settled:
- Home commune: a key, not a tie-breaker. With it the links stay equal or rise (uniqueness is easier on the finer
  key) and the false links fall by about a quarter in every year and every estimate. Rule SC is the one to ship.
- False-link rate of SC: about 10-20% in most years (L 10-26%, C 5-18%, U at most 32%; 2021 worst). Each wrong link
  turns a real dropout into "No"; each right link removes a wrong positive: SC removes 3 to 9 wrong positives for
  each one it adds (L), at least 2 (U). The advocate's opening cost argument (a quarter to 45% wrong) came from the
  loose key and does not hold for SC; the critic's "two to three errors removed per one made" is the conservative end.
- Effect: 10-19% of each year's positives relabelled, rising into the test windows (13.4 / 15.7 / 19.0%). The rise of
  the dropout rate from the history to the test windows shrinks: 2018-2019 2.46/2.56% to 2.21/2.27%; test windows
  2.77/2.92/2.80% to 2.40/2.46/2.27% (2024 now below 2023). The COVID years stay low (1.22/1.69%). Test windows keep
  about 12.0k / 12.3k / 11.3k positives of 500k.
- Not removed: id changes where the student also changed school, or with several candidates (the claim auditor's
  looser key finds about 1-2k more excess per year), deaths, emigration, exam-route graduates. These stay a named gap.

**3. CHANGES TO MAKE NOW (no decision needed)**

Validity
C1. USE-5 (Must), remedy ladder "fix the definition": implement rule SC in _prepare_raw_files (it needs the ids of
    every file 2017..t and the t+1 file's school, sex, birth month, commune and grade); set the linked students'
    next_state to a regular state, so their label is "No". Never drop them (LEAK-22, framingham; the cohort would be
    selected on t+1). Both sides agree. Precedent: corporate_credit_rating (repair before a note).
C2. Same link, the linked new id's row of year t+1: take its prev_* and changed_school from the old id's year-t row
    instead of "not enrolled" (LEAK-34: the entity's own history; the ministry holds the RUN trajectory). 6-13k rows
    a year. Cheap, follows from C1.
C3. USE-8 (Must), writing: rewrite `predicted`, fit_reason, the label anomaly bullet and the builder's issue 1. State
    the rule SC, its link counts and the placebo rates of section 2; the residue (deaths, emigration, exam routes,
    unlinked id changes); the 2019 rate after the link (2.27%) against the source's 1.7%. Drop "nothing open can
    repair it" and "USE-5 departure" (a Must has no departures). Add the claim auditor's clause: the 2025 graduates
    file separates exam routes for the 2024 window only (about 1.2% of its dropouts), not relabelled since only one
    window could be.
C4. USE-8 (Must), writing: one sentence in the Rows bullet on the students who moved from a youth to an adult course
    during year t (8,526 in 2023, 91% positive, about 10% of a year's positives): no rows, as their final row of t is
    adult education (an input known at the point, so no LEAK-22 issue). If all grades stay (issue 1), one sentence in
    use_case: Mineduc's SAT lists the top 10% per school of 7th basic to 4th secondary, the rows go wider.
C5. Re-run the task, leak and hidden-group probes and the bundle checks on the re-linked labels; update every number
    in the notes (rates, the withdrawn share of dropouts, the LightGBM figures).
Value
C6. MET-5 (Should), wording: the reason says GM of sensitivity and specificity is the paper's one criterion (Sec. 2.2;
    objective of its feature selection, Sec. 2.4; model choice, Sec. 3.2), a threshold metric at the default cut of a
    1:1-undersampled training set, no threshold or cost fixed (MET-6), so the fallback roc_auc. Agreed by both.
Split
C7. SPLIT-20 (Should), notes in splits_comment: (a) attendance recorded as 100% for 45.3% / 24.1% of rows in 2020 /
    2021 (4-6% otherwise), dropout under 50% attendance 7.5% / 4.9% against 15-27%; kept because a yearly refit
    trains on them and dropping them breaks the 50% floor for the 2022 window (SPLIT-14); (b) special education
    enters the files in 2023, so moves into it are "No" from the 2022 labels and "Yes" before (about 4% of a year's
    dropouts). Agreed by both.
C8. LEAK-9 (Should), a protocol line in splits_comment: a model sees only its split's rows; rows of later windows hold
    the same students' next year (task gamer's exploit 1, below).
Quality
C9. CLEAN-12: decode tp_sector and tp_specialty from Anexo VI (0 -> "general cycle or not applicable"); keep COD_MEN
    decoded from Anexo X, missing in 2018 and outside TP 3rd-4th secondary ("only from 2019" is no CLEAN-22 reason).
    Agreed by both; follows the decode rule of 2026-11-01 and avoids a third exception of one kind (rais, sinan).
C10. CLEAN-14 / CLEAN-12: combined_course keeps its six codes ("combined 1" ... "combined 6"; 225,592 / 94,012 /
    47,584 raw rows for codes 1-3 at different rates). Agreed.
C11. CLEAN-11: ages <= 4 (123 raw rows in 1st-7th basic) and their birth month to missing; ages >= 30 stay, noted.
C12. CLEAN-21 (Should), by analogy (one definition per column over time): prev_programme "special education" (6,025
    rows, all in the 2024 test window, 0 training rows) recoded to "not enrolled" with prev_* missing, as the same
    students read in every training year; one clause in the special-education bullet. The advocate prefers it, the
    critic and the column auditor accept it; a note alone would leave a level no fold can learn.
C13. Writing: SIT_FIN in the dropped list (an exact copy of SIT_FIN_R); ESTADO_ESTAB "at most 25 rows a year", reason
    reworded ("near-constant, possibly written at extraction"); communes and schools as codes called an application of
    CLEAN-12 (an entity's name, a nested official code), not a departure; school_id cites CLEAN-3 with USE-10.
C14. Builder's issue 4 (school_id) and issue 5 (licence) leave the issue list: school_id is settled by precedent
    (taxi_id, seller_id, customer_id; CLEAN-22, EV-4), the licence is a one-line note and a release-checklist item
    (EV-4, 2026-10-21).

**4. ISSUES FOR THE CURATOR (ranked)**

Issue 1 (P3, USE-1 / USE-5; Weigh): the rows cover all grades, the SAT list covers 7th basic to 4th secondary.
  Problem: grades 1-6 basic are 53-56% of the rows; the SAT (Mineduc IDPS sheet 8) lists the top 10% per school of
  grades 7-12; the paper and Mineduc's regular-system rate cover all children and youth grades.
  Re-measured on the re-linked labels (rule S; SC differs by under 5% in counts):
                                       2018   2019   2020   2021   2022   2023   2024
    grades 1-6 share of dropouts before 30.0%  35.5%  42.5%  36.4%  38.6%  40.5%  38.7%
                                 after  26.3%  32.4%  38.4%  33.5%  36.0%  38.3%  35.7%
    grades 1-6 dropout rate after      1.02%  1.30%  0.83%  1.02%  1.57%  1.75%  1.53%
    grades 7-12 dropout rate after     3.71%  3.52%  1.71%  2.50%  3.40%  3.31%  3.14%
    grades 1-6 promoted: rate after    0.53%  0.69%  0.54%  0.62%  0.80%  0.84%  0.75%  (before 0.78-1.21%)
    promoted share of grades 1-6 dropouts after: 47-63%
  The re-link lowers the grades 1-6 share by only 2-4 points; about half of their remaining dropouts are promoted
  children who vanish (emigration, home schooling by examination, id changes the rule cannot link). Neither side's
  forecast holds fully: the advocate's "with the re-link it leans to (a)" is weak, the critic's "emigration stays
  there either way" is borne out.
  Advocate's best evidence: the source's population (paper Sec. 3.2) and the ministry's national rate cover all
  grades; the task is the paper's.
  Critic's best evidence: the deployed list is grades 7-12; grades 1-6 carry a third of the positives at half the
  rate, half of them promoted, where the label is noisiest (domain practitioner: pooled AUC 0.82-0.84 there against
  0.86-0.88 on grades 7-12).
  Options: (a) all grades, with the use_case sentence of C4 (implemented); (b) 7th basic to 4th secondary (about
  8.7M student-years, 62-74% of the re-linked dropouts).
  Rules leave it open (which framing to ship). What would settle it: the curator's weight on the deployed actor's
  list (b) against the source's population (a).
  The per-school top-10% metric (domain practitioner, MET-7) is not a separate option: MET-7 asks for a k the source
  fixes, and the paper fixes none; its k comes with the grade 7-12 population, so it scores no decision under (a);
  in the practitioner's runs pooled AUC, within-school AUC and per-school precision rank model and rule the same way
  in all 3 windows; final status ranks as well within schools as pooled (0.727-0.747 against 0.733-0.753), which
  sets the case apart from protein_model_quality_rf_pcp and huesken_sirna_efficacy; a third within-group exception
  would need an amendment of MET-1 / MET-5. Only if the curator takes (b) is it worth asking, as an amendment.

Issue 2 (P3/P4, USE-1 framing; confirmation): the end-of-year list keeps the students withdrawn in year t (1.3% of
  rows, 36% of dropouts before the re-link, 58-72% of them drop out).
  No rule is broken: LEAK-10, LEAK-37, USE-3, USE-6 hold (status known at the close of t; the paper's final model uses
  it). Blind reviewer: the withdrawn part is "bookkeeping", drop them or move the point earlier (AUC 0.75 then).
  Domain practitioner, advocate, critic: re-engagement of the withdrawn is a real decision on the same list; the task
  is 0.76-0.77 on the others. Recommend keep (builder's option (a)); confirm.

Not an issue any more: the re-link (C1, both sides agree, a fixable Must). Should the curator prefer a note only,
that is a decision against a fixable Must and a departure from corporate_credit_rating, and needs the fact that sets
the case apart (or an amendment of USE-5).

**5. DISPUTED POINTS, SETTLED**

D1. Re-link required or note only (USE-5 Must). Settled after rebuttal: required. The rule says a Must is fixed in
    the definition when it can be; the remedy ladder puts the fix above a note; the label part was checked and found
    to be another quantity (USE-5 amendment of 2026-10-21), and the error sits in a group the inputs identify
    (xente's shape), so a note does not resolve it. Not an independent failure that excludes: the fix works (section
    2). LEAK-8 ("retire rather than invent structure", Should, P4) does not outrank USE-5 (Must, P3), and the link is a
    label repair with a measured error rate, not a guessed group.
D2. The re-link rule: SC, commune as a key (section 2).
D3. Grades 1-6: a weighing call (issue 1). Measured on the re-linked labels.
D4. prev_programme "special education": recode (C12), a P7 choice both sides accept.
D5. COD_MEN: keep decoded (C9); the advocate conceded.
D6. Youth-to-adult movers: a note (C4); the advocate conceded the note, the selection rests on an input known at the
    point.

Task gamer, mapped:
- Exploit 1 (+0.0168 / +0.0165 AUC on the 2023 / 2022 windows, 0 on 2024): matching a test student to their row of
  year t+1, which sits in another window's test rows of the shared frame (prev_gpa and prev_attendance_pct repeat
  year t). Rule: LEAK-9 (an evaluation-level leak: a method reads rows outside its split), with LEAK-17 / LEAK-34 for
  why the rows link (the same student; history is legitimate inside a split). The definition has no `Potential leak,
  kept on purpose:` note and no accepted warning on it: new for this dataset, a known class. Not a data fix (sampling
  by student would remove legitimate history, LEAK-34); a protocol line (C8). Both sides dropped it as a harness
  matter; the line is consistent with that.
- Exploit 2 (+0.0003 to +0.0025): same-year school aggregates over the test rows. The information is the actor's at
  year close (USE-6); computing it from other test rows is transductive (LEAK-9). Gain below the noise of most
  probes; no issue.

**6. AGREED FACTS**

- Label = Rodriguez et al. 2023 Sec. 3.2 word for word; Mineduc's regular-system dropout measure (2.4% for 2018,
  the data 2.46%). Rows per year match the layout's stated counts.
- Every input is from the files of t and t-1, known at the close of t; no feature leak (column auditor, 27 inputs);
  ESTADO_ESTAB and MRUN rightly dropped (MRUN alone 0.715, it encodes the id artefact).
- Id changes: 10-19% of positives relabelled by rule SC, rising into the test windows; linked students come back
  under the old id at 2-6% against 14-26%; concentrated in high-immigration regions and new arrivals.
- Split: yearly windows 2024/2023/2022, train 2018..t-1 (first side 56.5%), no gap right (labels of t-1 known at the
  close of t), 0 shortcut labels, IID would overstate by 0.011-0.017 AUC.
- Task probes no flags (linear 0.877, LightGBM 0.870, RF 0.854); best single feature 0.72-0.75.
- Withdrawn: 1.3% of rows, 36% of dropouts; 0.75-0.77 AUC without year t's outcomes or without the withdrawn.
- Special education in the files from 2023; COVID recording break 2020-2021.
- Metric: the paper's one criterion is GM, threshold-based with no cut fixed; roc_auc by MET-6.
- school_id: 99.9% of test rows' schools in train; costs untuned LightGBM 0.012-0.017 (no argument, CLEAN-22, EV-4).

**7. CONSISTENCY WITH PRECEDENT (precedent checker's report)**

Followed:
- corporate_credit_rating (USE-5: repair before a note) for the re-link; diabetes_3 (USE-5 amendment) for the residue
  nobody can check; framingham (LEAK-22: keep the row with its label, relabel not drop).
- xente_fraud_detection_challenge (`No`) is not followed; the fact that sets this case apart: the error group can be
  located and repaired from the open files (rule SC), and the larger part of the label is the ministry's measure.
- school_id: chicago_taxi_trip_duration_1m, pkdd_15, brazilian_ecommerce, african_credit_scoring_challenge.
- Communes as codes: early_learning_predictors, pricing_game_2017_french_mtpl, house_sales, zillow_prize.
- tp codes decoded: the decode rule of 2026-11-01, labour_inspection_compliance, ny_wcb (avoids the third exception;
  the amendment question stays with rais).
- Metric fallback: heart_disease, gallstone_disease, aeolus_rebuilt; within-group exceptions not extended (fact in
  issue 1).
- Windows and the accepted `task_time_on_few_unique`: wisconsin_local_government_property_insurance_fund,
  spanish_homeowners_motor_insurance_2010_2014, tunisian_fraud_detection_challenge; SPLIT-20 notes as aeolus,
  perth_house_prices.
- Licence: EV-4 (2026-10-21), as numerai_v5_2, aeolus.
New ground, a reflection question for the curator: no definition in the copy repairs a label with a probabilistic
record link of our own. Would the same rule (a link with a stated placebo false-link rate, applied when it removes
several wrong labels for each one it adds) apply to the siblings built by linking pseudonymised ids across yearly
files? If yes, it may become a Cases row under USE-5.

</details>

<details><summary>Claim audit</summary>

CLAIM AUDITOR REPORT: chile_school_dropout_mineduc (folder chile_school_dropout_mineduc_1m), 2026-11-09
Scratch and logs: P/work_claim_auditor/ (raw_checks.log, id_change.log, id_change2.log, id_change3.log,
container_metric.log, paper/paper.txt = Rodriguez et al. 2023 full text from PMC OAI, layout/er2025.txt = record layout 2025)

VERDICT: one validity claim refuted (P3, USE-5 Must): the label carries a large noise source the definition does not
name and partly could remove: students whose pseudonymised id changes between years (a provisional school id, IPE,
replaced by a RUN) are counted as dropouts. About 13-25% of each year's dropouts (placebo-corrected about 9-18%), 22-43%
of the promoted dropouts, growing over time, the largest in the test windows. The metric's fallback holds, but on MET-6
only: the MET-5 half of its reason misreads the paper. Two numbers in the notes are slightly off. Everything else I
tested holds.

**TABLE  (claim | source | test | result | evidence | rule)**

C1 source portal | claims 1, source_url | HEAD the 2025 RAR URL | holds | HTTP 200, last-modified 2026-03-04 | PROV-8
C2 year 2026 | claim 2 | same | holds | 2025 file uploaded March 2026 | PROV-9
C3 licence CC BY-NC 2.0 | claim 3 | datos.gob.cl package_show | holds | license_id cc-nc, by-nc/2.0, org Subsecretaria de Educacion | EV-4 (note only)
C6 SAT use case (mineduc.cl/?p=22673) | claim 6 | fetch | UNTESTED | ECONNREFUSED (as in screening) | USE-1
C7/C8 prediction point = close of t; source predicts from same point | claims 7-8, curation_comments | paper text | holds | Sec. 3.2: test = "trajectories that reached 2019 and were (or not) dropouts in 2020"; Table 11: LAST_GRADE_APPRVD "Last grade was reported as approved" (most important, Fig. 11), LAST_CYCL_AVG_ATTNDNC | USE-3, LEAK-10
C9 fit_reason: gap 3% vs 1.7% due to deaths and other-route graduates | claim 9, fit_reason | id-change link test (below) | REFUTED in part | flagged id changes explain 0.27-0.36 pp of the 0.86 pp 2019 gap (2.56% -> 2.20% with flags removed); the definition never names them | USE-5, USE-8
C10 rows per year | claim 10 | count student_years.parquet | holds | 2,714,675 ... 2,798,612 exactly | -
C11 graduates out, "as in the source" | claim 11 | grades within groups 5/7; graduates files | holds | secondary grade codes 1-4 only; 0 of t's dropouts in the graduates file of t (scratch/explore4.log); paper Sec. 3.2 defines dropout for children/youth only | USE-5
C12/C19 special education in files from 2023; 3,025/1,619/1,502 | claims 12, 19 | COD_ENSE2 per raw year | holds | COD_ENSE2 = 4: 0 rows 2017-2022; 201,496 (2023), 195,279 (2024), 189,532 (2025); layout fn. 4; next_state "special education" 3,025/1,619/1,502 | USE-5
C14 target = paper's definition | claim 14 | paper text | holds | Sec. 3.2: "enrolled in some grade for children and youth on year t is either enrolled in adult education or out of the school system on year t+1" | USE-5
C15 dropout shares and absent share | claim 15 | recount | holds | 2.46/2.56/1.50/1.90/2.77/2.92/2.80%; absent 63.7% (2018) to 82.3-82.4% (2023-24) | -
C16 the noise = deaths, emigration, exam-route graduates ("cannot be told apart") | claim 16, `predicted` | (a) id-change link test; (b) 2025 graduates file | REFUTED (incomplete list); (b) minor | (a) below; (b) 931 CERTIFIC + ~40 AYUDA_* of 78,300 dropouts of 2024 graduate by another route in 2025 (1.2%; scratch/explore4.log): separable for the newest window only | USE-5 Must
C17 ORIGEN only for 2025 | claim 17 | explore4.log | holds | 2017-2024 all RENDIMIENTO | -
C18 source 1.7% for 2019->2020 | claim 18 | paper | holds | Sec. 3.2: "2,802,156 trajectories of which 47,632 (1.7%)" | -
C21 ESTADO_ESTAB dropped, "operating in all but at most 24 rows a year" | claim 21 | join ESTADO_ESTAB to task rows | holds (drop); count off by one | non-1 rows: 24 (2018), 8 (2019), 25 (2020), 0, 1, 0, 0; their dropout rate 69-100% vs 1.5-2.9%: an outcome-like status (layout fn. 2: the filter for schools "funcionando"), right to drop | LEAK-10
C24 age_june_30 = age from birth month | claim 24 | recompute on shipped frame | holds | equal share 1.0 over 2,499,896 rows | CLEAN-10
C25 withdrawn 1.3% of rows, 67.5% rate | claim 25 | recount by year | holds | Y rate 57.8-72.1% by year | LEAK-10
C26 LightGBM numbers | claim 26 | read probes/experiment_prediction_point.json | holds | school_id costs 0.012-0.017; history 0.015-0.016 | -
C27 school_id 99.9% seen | claim 27 | probes/hidden summary | holds (read, not re-run) | | SPLIT-13
C28 duplicates, no copy across split | claim 28 | shipped frame (fresh container) | holds | 802 duplicate rows of 2.5M; 0 test rows with a feature copy in train, year excluded, in all 3 folds | LEAK-16..21
C32 metric: fallback roc_auc, "two of them (MET-5)", no threshold (MET-6) | claim 32, Metric.fallback reason | paper Secs. 2.2-2.4, 3.2 | holds on MET-6; MET-5 half REFUTED | Sec. 2.2: "we use the geometric mean between the sensitivity and specificity (GM Score) to measure performance"; Sec. 2.4: "we propose to use the GM score as an objective function" (RFE); Sec. 3.2: LightGBM kept as "slightly superior to CatBoost in GM score". GM is the paper's one deliberate criterion, F1 secondary. It is a threshold metric with no threshold or cost fixed (train undersampled to 1:1, default cut), so MET-6 sends it to the fallback anyway. No ROC AUC in the paper | MET-5, MET-6, MET-8
C32b metric computable | MET-2 | fresh container, scorer on each fold | holds | roc_auc, no scoring columns; 3 folds x 500k test, 13,870-14,589 positives; constant 0.5, random 0.496-0.497, "withdrawn only" 0.684-0.698 | MET-2
C33 splits: windows 2024/2023/2022, train all earlier from 2018, no gap | claim 33 | fresh container | holds | train years 2018-2023 / 2018-2022 / 2018-2021, 1M each; label of t-1 = enrolment in t, known at close of t | SPLIT-1, SPLIT-11
C34/C35 row budget, 56% floor | claims 34-35 | counts | holds | 3 x (1,000,000, 500,000); 2018-2021 = 10,964,808 of 19,404,374 = 56.5% | SPLIT-14
I1 (implied) every feature known at close of t | definition | column audit + ESTADO_ESTAB test | holds | inputs from files t, t-1; the one closure-time field dropped | LEAK-10
I2 (implied) the target is the real-world target | `predicted` | id-change link test | REFUTED in part | see finding 1 | USE-5 Must

**FINDING 1 (P3, USE-5 Must; validity): id changes counted as dropouts**

Test (EV-1, a test that could have come out empty): for every student of year t absent from the file of t+1, look for
a NEW id in t+1 (an id in no file 2017..t) at the SAME school with the same birth month, sex and home commune.
Placebo: the same match with the birth month shifted by +-1 and +-2 months (same school, cohort and density).
Scripts: work_claim_auditor/id_change.py, id_change2.py, id_change3.py.

- Matches vs placebo (school+birth month+sex+commune): 2018 9,393 vs 3,491; 2019 10,484 vs 3,050; 2020 9,176 vs
  2,110; 2021 7,705 vs 3,178; 2022 14,787 vs 5,756; 2023 18,533 vs 6,928; 2024 20,808 vs 7,079. The excess over
  placebo is 11-21% of the absent dropouts and rises over time (5.9k in 2018 to 13.7k in 2024).
- The matches behave like one student under two ids, not like a coincidence (2019 / 2022 / 2023):
  * the grade in t+1 is the same or the next one: 95.8 / 95.4 / 95.7% (placebo 81.7 / 85.4 / 85.9%);
  * the candidate is unique in 81-87% of cases; the new id is new to the system in 97.7% (placebo about 95%);
  * the matched "dropouts" almost never come back in t+2: 3.5 / 2.9 / 2.1% vs 24.0 / 16.0 / 14.7% of unmatched absent
    students;
  * they are the promoted ones: 33-41% of promoted absent dropouts match vs 3-7% of the withdrawn;
  * they cluster where immigration is high: school region Antofagasta 29-48%, Tarapaca 26-44%, Arica 23-38%,
    vs 22-25% in Metropolitana;
  * students with no row in t-1 (new arrivals) match at 30-33%.
- Mechanism (inference, EV-2 rank 5; the pattern above is rank 1): Mineduc gives foreign students without a RUN an
  "Identificador Provisorio Escolar" (IPE, since 2017), replaced by the RUN when the student gets one; the trajectory
  is then moved to the new RUN in Mineduc's systems (https://www.mineduc.cl/?p=11209,
  https://www.ayudamineduc.cl/ficha/solicitud-de-cambio-de-ipe-por-run,
  https://www.chileatiende.gob.cl/fichas/49443-identificador-provisorio-escolar-ipe-e-identificador-provisorio-del-apoderado-ipa-para-personas-extranjeras).
  The published yearly files keep the old masked id. The paper used the internal enrolment file and consistency
  scoring (Sec. 3.2, Table 2), and reports a traceability of 96.4% with foreigners as the untraceable case.
- Size on the task (flagged = match plus a consistent grade, so placebo-level coincidences are included; the
  placebo-corrected share is about two thirds to three quarters of these):
  year  dropouts  flagged        promoted dropouts flagged   rate without flagged
  2018  66,856    8,661 (13.0%)  27.7%                       2.46% -> 2.14%
  2019  70,145    9,827 (14.0%)  28.4%                       2.56% -> 2.20%  (source 1.70%)
  2020  40,940    8,649 (21.1%)  31.5%                       1.50% -> 1.18%
  2021  52,766    7,032 (13.3%)  22.5%                       1.90% -> 1.65%
  2022  78,273   13,748 (17.6%)  31.9%   (test window 3)     2.77% -> 2.29%
  2023  82,257   17,395 (21.1%)  37.4%   (test window 2)     2.92% -> 2.30%
  2024  78,300   19,818 (25.3%)  43.1%   (test window 1)     2.80% -> 2.09%
  New arrivals (no row in t-1, above 1st basic): dropout rate 19-25% -> 12-14% without the flagged students.
- What it changes: the "hard" part of the task (students not withdrawn, AUC 0.76-0.77 in the builder's experiment)
  is the part most affected. Up to 43% of the promoted dropouts in the newest test window are probably students who
  are still in the same school next year, and models are rewarded for spotting recently arrived foreign students
  rather than dropouts. The same students also show up in t+1 as "not enrolled" in t-1 (a missing history). The noise
  grows over the test windows, so the train and test labels drift apart. It refutes the fit_reason's account of the
  gap (claim 9), the completeness of `predicted` and claim 16, and the builder's issue 1, which says "nothing open can
  repair it".
- Mildest remedy (remedy ladder: no origin repair, since Mineduc's IPE-to-RUN table is not public): fix the
  definition. Link an absent student of t to a unique new id of t+1 at the same school with the same birth month,
  sex and home commune and a consistent grade. Count the student as enrolled (label "No"), or drop those rows. Write
  the placebo rate in the notes. Optionally carry the old id's year into the new id's prev_* columns. If the curator
  prefers no record linkage of our own: name it in `predicted`, fit_reason and an Anomaly bullet with the numbers
  above, and add it to REVIEW.md issue 1 as option (c). Either way, issue 1's "nothing open can repair it" goes.

**REFUTED AND UNTESTED, RANKED**

1. [P3 validity, USE-5 Must] Label noise from id changes (claims 9, 16, `predicted`, fit_reason; builder issue 1):
   REFUTED. Effect: 13-25% of dropouts flagged (9-18% after placebo), 22-43% of the promoted dropouts, rising into
   the test windows. Remedy: re-label or drop the linked students (definition fix); at minimum document the numbers
   and add it as an option to issue 1.
2. [P6 value, MET-5 Should] Metric reason (claim 32): the fallback holds on MET-6, but "two of them (MET-5)" is wrong.
   The paper names GM as its measure and as its objective function (Secs. 2.2, 2.4) and picks LightGBM by GM
   (Sec. 3.2). Remedy: reword the reason: "the paper's criterion is the GM of sensitivity and specificity (Sec. 2.2;
   objective of its feature selection, Sec. 2.4), a threshold metric at the default cut of a 1:1-undersampled
   training set, with no threshold or cost fixed by the decision (MET-6)". roc_auc stays.
3. [P3, USE-5, minor] Claim 16 "cannot be told apart": for the 2024 window the 2025 graduates file separates exam
   and other routes (931 CERTIFIC + about 40 AYUDA_* of 78,300 dropouts, 1.2%). Remedy: one clause in the anomaly
   bullet. Do not re-label, since only one window could be fixed.
4. [P4/P7 wording] Claim 21 "at most 24 rows a year": 25 in 2020. Remedy: "at most 25". The drop itself holds.
5. UNTESTED: claim 6's SAT page (mineduc.cl refused the connection, ECONNREFUSED, as in screening). The use case
   rests on the paper (Sec. 1: EWS) without it. Claim 27 was read from the probe summary, not re-run.

Not refuted, tested: prediction point and every input (I1), the ESTADO_ESTAB drop, special-education timing and
counts, the graduate exclusion, label definition = paper Sec. 3.2, dropout shares, split years and sizes, the 56%
floor, duplicates and copies across the split, age equality, the licence, and the metric's computability (3 folds,
13.9-14.6k positives each).

</details>

<details><summary>Column audit</summary>

COLUMN AUDITOR: chile_school_dropout_mineduc (folder chile_school_dropout_mineduc_1m), 2026-11-09

Verdict: no feature leak. One label finding outranks every column finding: the label counts a student
whose pseudonymised id changes between yearly files as a dropout. Six cleaning points, all P7, all cheap.
school_id stays (CLEAN-22). ESTADO_ESTAB is dropped correctly. MRUN is dropped and encodes the label artefact.

Prediction point read from dataset.py (first curation_comments bullet): the close of school year t, after
the final statuses are recorded. Each file is cut at the end of January of t+1, before March. The label is
read from the file of t+1.

Sources:
- Codebook: "Esquema de registro bases de Rendimiento escolar 2002-2025 por estudiante" (the PDF in the 2025
  archive, read in full).
- Frequency workbook of 2023.
- Raw CSVs of 2017-2025 and student_years.parquet.
- Cleaned frame and splits: rebuilt from the final definition (dataset.py changed at 19:27, after the
  builder's 19:02 dtype probe and 19:07 frame dump). dtype probe re-run on the final definition: the same
  7 flags as the builder's.
Scripts and logs: the run folder (scripts/, raw1-4.log, twin2.log, twin2_2019.log, frame1.log,
dtype/, dtype_probes.log).

**COLUMN TABLE  (column | meaning (codebook) | known at prediction point? | dtype and cleaning | verdict | rule)**

school_id | RBD, the school's id ("Rol base de datos") | yes, year t | category, 8,716 levels, code
  kept (no words) | FINE. Recurring school (unseen in training: 0.05-0.06% of test rows in each fold);
  the 0.012-0.017 AUC that untuned LightGBM loses is a model's handling and no reason to drop it |
  CLEAN-22, EV-4, LEAK-34, USE-10
school_region | COD_REG_RBD, Anexo I | yes | decoded to region names, 16 levels; Nuble (16) from 2018 |
  FINE | CLEAN-12
school_commune | COD_COM_RBD, official SUBDERE code (names in NOM_COM_RBD) | yes | category of the code,
  345 levels; prefix always = region (0 mismatches) | FINE with note: lossless; CLEAN-12 prefers the
  names (in the file, 1:1), CLEAN-14's last bullet allows the code. Curator's choice, cosmetic |
  CLEAN-12, CLEAN-14
school_dependency | COD_DEPE 1-6 | yes: the year-t value, not a lookup at the cut. The 871 schools that
  pass to a SLEP in 2025 still show municipal (1 or 2) in the 2024 file | decoded, 6 levels | FINE |
  LEAK-10, CLEAN-12
school_rural | RURAL_RBD 0 urban, 1 rural | yes | No/Yes category | FINE | CLEAN-14
programme | COD_ENSE (Anexo II): 110, 310, 410-910 | yes | decoded, 8 nominal levels; the dtype probe's
  ordinal_like is a false alarm (nominal) | FINE | CLEAN-12, CLEAN-14
grade | COD_GRADO within COD_ENSE (Anexo IV) | yes | ordered, 1st basic < ... < 8th basic < 1st secondary
  < ... < 4th secondary. The order matches the codebook, no unknown codes. Note: "4th secondary" holds only
  non-promoted students (graduates are filtered out), so the level has a 69% dropout rate (4,235 rows) |
  FINE | CLEAN-14
shift | COD_JOR 1-4 | yes | decoded | FINE | CLEAN-12
combined_course | COD_TIP_CUR: "0: Curso Simple, 1-6: Curso Combinado" (no words per code; fn 7) | yes |
  1-6 merged into "Yes". This is LOSSY: codes 1/2/3 have 225,592/94,012/47,584 raw rows at 1.19%/0.84%/0.87%
  dropout | CLEANING PROBLEM (minor): keep the six codes as levels ("combined 1" ... "combined 6") or as
  codes | CLEAN-12, CLEAN-14 ("lose no information")
tp_course_type | COD_DES_CUR 0 n/a, 1 school only, 2 dual, 3 other | yes | decoded | FINE | CLEAN-12
tp_sector | COD_SEC; Anexo VI names every sector (Administracion y Comercio, Construccion, ...) | yes |
  category of codes 0-910. 0 = general cycle (TP 1st-2nd secondary) or not applicable; never 0 in TP
  3rd-4th (measured), so no "sin informacion" in the rows | CLEANING PROBLEM (minor): the codebook names
  every level, so decode to the words; 0 -> "general cycle or not applicable" | CLEAN-12 (Should; no fact
  given for the departure)
tp_specialty | COD_ESPE; Anexo VI names all 38 specialties | yes | category of codes | CLEANING PROBLEM
  (minor): decode as for tp_sector | CLEAN-12
sex | GEN_ALU 1 male, 2 female, 0 "Indefinido" (3 non-binary removed by the source) | yes | 0 -> missing
  (38 raw rows) | FINE. Kept for a support use case (documented) | CLEAN-10
age_june_30 | EDAD_ALU, age on 30 June of year t (fn 9: atypical values are entry errors; from 2016,
  unvalidated atypical ages are set missing by the source) | yes | float; equals the age from birth_month
  in 100% of rows. Ages <=4: 123 raw rows (2- to 4-year-olds in 1st-7th basic, impossible), 89% "dropout",
  all absent. Ages >=30: 138 rows, 79% | CLEANING PROBLEM (minor): set ages <=4 (and their birth_month) to
  missing as impossible. Their label is an id-linkage artefact: see problem 1 | CLEAN-11
birth_month | FEC_NAC_ALU (AAAAMM) | yes | datetime %Y%m; 190001 -> missing (740 raw rows, 41% dropout) |
  FINE (proxy handled); same linkage note as age | CLEAN-10
residence_region | COD_REG_ALU, 0 "Sin informacion" | yes | decoded, 0 -> missing (161 rows, 41% dropout,
  all absent) | FINE | CLEAN-10
residence_commune | COD_COM_ALU (self-declared, voluntary), 0 "Sin informacion" | yes | category of the
  code, 0 -> missing | FINE with the commune note above | CLEAN-10, CLEAN-12
final_status | SIT_FIN_R on the final (non-transfer) row: P/R/Y, blank "sin informacion" | yes: set at the
  close of year t. No file of t+1 exists at the cut (end of January t+1) | decoded; blank -> missing (2,731
  rows) | FINE as a feature (known at the point). Withdrawn = 1.3% of rows, 68% dropout. Which rows belong
  in the cohort is the builder's issue 2. SIT_FIN (not read) equals SIT_FIN_R on every non-transfer row of
  2023 | LEAK-37, USE-6; cohort: USE-7 / LEAK-22
gpa | PROM_GRAL, 1.0-7.0; 0.0 for withdrawn and for courses graded otherwise (fn 13) | yes | missing where
  the status is not P/R or the value is 0.0. On the rows: never 0.0 with P/R; 99.98% of Y rows are 0.0, so
  the mask loses nothing. No values in (0,1) or >7 | FINE. Missingness = withdrawn/blank status, known at the
  point | CLEAN-10, LEAK-10 (not outcome-caused)
attendance_pct | ASISTENCIA, annual % | yes | the same mask; 0-100, none >100; 152 rows of 0 with P/R
  (129 in remote 2021) kept as unusual | FINE | CLEAN-10, CLEAN-11
transfers_in_year | built: count of the student's T rows in year t | yes | int count 0-14, numeric | FINE |
  CLEAN-14, CLEAN-19
prev_programme | built: COD_ENSE2 of the t-1 final row, "not enrolled" when absent | yes (t-1) | decoded,
  8 nominal levels. "special education" exists ONLY in the 2024 test window: 6,025 test rows, 0 training rows
  in any fold, because special education enters the files in 2023. In the training years the same students
  read "not enrolled", with changed_school and prev_* missing | CLEANING QUESTION: one definition per column
  over time. (a) note it in the special-education anomaly bullet (mildest; the bullet now covers only the
  label), or (b) recode prev special education as "not enrolled" with prev_* missing, which matches the
  training years | CLEAN-21 (by analogy), USE-8
prev_final_status | SIT_FIN_R of the t-1 final row | yes | decoded; missing when not enrolled | FINE |
  LEAK-34
prev_gpa | PROM_GRAL of t-1 | yes | the same mask as gpa (95% missing for prev special education, graded
  otherwise) | FINE | CLEAN-10
prev_attendance_pct | ASISTENCIA of t-1 | yes | the same mask | FINE | CLEAN-10
changed_school | built: RBD of t-1 differs from RBD of t | yes | No/Yes, missing without a t-1 row.
  Includes the natural moves (1st secondary: 43% sci-hum, 81% TP) | FINE | CLEAN-19
year | AGNO, school year t (time index) | yes | int16 feature; the test year always lies past the training
  range | FINE (time index kept as a feature, repo default) | CLEAN-3
dropout (target) | built: the file of t+1 holds no course outside adult education | label | "No"/"Yes" |
  SEE PROBLEM 1 (a part of "absent" is an id change, not a dropout) | USE-5, CLEAN-25

DROPPED COLUMNS
- MRUN: correct to drop (join key). It also encodes the label artefact: in 2023 the absent rate is 0.86% in
  MRUN deciles 1-8 against 3.4% in decile 9 and 13.6% in decile 10, the recently assigned ids (the
  builder's raw probe: MRUN alone AUC 0.715). | LEAK-10 (an id that encodes the label)
- ESTADO_ESTAB: correct drop, though the stated reason is weak. In 2023, only 37 child/youth rows are not
  "operating". Of the 55 schools with child/youth rows in 2023 and none in 2024, 54 were "operating". So
  ESTADO_ESTAB is near-constant and barely a closure flag. It may still be written at extraction (after the
  point), so it stays out. Suggest rewording "set when a school closes" to "near-constant (37 rows in 2023)
  and possibly written at extraction". | LEAK-10, CLEAN-5
- SIT_FIN: never read; an exact copy of SIT_FIN_R on the kept rows (measured 2023). It is missing from the
  dropped list in curation_comments: add it. | CLEAN-5, writing
- COD_MEN (mention): dropped as "7 specialties, only from 2019". It is in the files 2019-2024 and filled
  for 47% of TP 3rd-4th secondary rows (81,016 of 172,299 in 2023), and Anexo X gives words for every code.
  "Missing in 2018" is none of CLEAN-22's reasons. QUESTION: keep it decoded (missing in 2018 and outside
  TP 3rd-4th). Small effect expected. | CLEAN-22, CLEAN-12
- NOMBRE_SLEP: in 2024 it is set exactly on the dependency-6 rows (212,361 = 212,361), and absent from
  every training year. Fine to drop. | CLEAN-5
- Names, check digit, province, provincial department, COD_DEPE2, COD_ENSE2, COD_RAMA, LET_CUR: copies,
  groupings or a course id. Fine. | CLEAN-3, CLEAN-5

**PROBLEMS RANKED (principles.md: P3 > P4 > ... > P7; Must first)**

1. P3, USE-5 (Must): part of the positives are id changes, not dropouts. NEW finding, decisive experiment.
   Mechanism: Mineduc gives a foreign student without a Chilean RUN a provisional school id (IPE, since
   2017). Once the student obtains a RUN, the trajectory is moved to the RUN (ayudamineduc.cl, "Solicitud
   de cambio de IPE por RUN"). The yearly files are frozen at their January cut, so the file of t carries
   the IPE's mask and the file of t+1 the RUN's mask. The student reads "absent", i.e. a dropout.
   Test: for each 2023 row labelled absent, look for an MRUN that is new in 2024, in the same school, with
   the same sex and the same birth month, at the same grade or one above. The chance baseline uses the
   birth month shifted by +-1 and +-2 months.
     absent:    30.8% have such a twin; chance 13.7%; excess about 11,600 students
     regular:    5.7% vs chance 5.9% (no excess)
     adult only: 4.7% vs 4.7% (no excess)
   So about 11,600 of the 82,257 positives of 2023 (14%) are probably the same student under a new id.
   This is a lower bound: a twin who also changed school is missed. Of these twins, 17,063 were promoted
   in 2023. 94.6% of the absent students with a twin hold a 2023 MRUN in the top 20% of the MRUN range.
   The twins concentrate in Metropolitana, Antofagasta, Tarapaca and Arica, the regions with most
   immigrants and the highest "dropout" rates (4.4% Tarapaca, 4.1% Antofagasta, 1.5% Biobio).
   2019 -> 2020, a training year: 22.0% vs chance 7.3%, excess about 7,700 of 70,145 positives (11%).
   It persists across the splits.
   The rows with an impossible age or a placeholder birth date show the same break at small scale: age <=4
   89%, age >=30 79%, birth month 190001 41%, residence "sin informacion" 41% dropout. Nearly all of them
   are absent.
   Why it matters for the columns: nationality is not in the open file, but region, commune, school_id,
   prev_programme "not enrolled" (newcomers) and an atypical age/grade stand in for "holds an IPE". A model
   is rewarded for flagging migrant students who did not leave school.
   This sharpens the builder's issue 1 (label noise): the notes name deaths, emigration and exam-route
   graduation, but not id changes. Emigration and the id change share the same proxies.
   Remedies, mildest that resolves first:
   (a) Repair from the origin: ask Mineduc (Centro de Estudios) for an IPE-to-RUN crosswalk, or whether the
       MRUN of a later release is relinked. Neither is public as far as I found.
   (b) Fix the definition: relink an absent student to a new-id twin. This is a rule of our own, and at a
       13.7% chance rate about 45% of its relinks would be wrong, so it is not clean.
   (c) Keep with a note: name the id change in the label anomaly bullet and in fit_reason ("about 11-14% of
       positives, mostly migrant students, are probably an id change"), as part of fit approximate.
   (d) If the curator judges the label to be another quantity for a migrant-heavy share, USE-5 fails
       (retire as No Good Target). I do not recommend this: the source paper's label has the same
       exposure unless its NDA data carried the relinked trajectories.
   Recommend (c) now and ask (a). The curator decides whether "approximate" still holds.

2. P3/P4, cohort (LEAK-22 Must reads "follow the paper's cohort"; weighing call). Not a column, but it
   decides what final_status means. The source counts "a student enrolled in some grade for children and
   youth in t". The definition keeps only students whose final row of t is a children's or youth course. In
   2023, 8,526 students left a youth course for adult education during the year (youth T rows, final row
   adult). They are no rows, and 91% of them would be positives (about 10% of the year's positives). The
   choice is defensible for an end-of-year list held by a youth school, but it is not stated as a departure
   from the source. Remedy: one sentence in the Rows bullet (mildest), or add them as rows. Ties to the
   builder's issue 2 (withdrawn students).

3. P4 (feature timing): NO LEAK FOUND.
   - Every feature is from the files of t or t-1, each cut at its January.
   - School dependency is year t's value, not the value at the cut.
   - final_status, gpa, attendance and transfers are set by the close of t (LEAK-37/USE-6).
   - Their missingness follows the withdrawn/blank status, not the outcome.
   - No window ends at the outcome. No feature reads the file of t+1.
   - ESTADO_ESTAB and MRUN are dropped.

4. P7, CLEAN-21 by analogy (Should): prev_programme's "special education" level exists only in the 2024 test
   window (6,025 rows, 0 in training). Note it in the special-education bullet, or recode it to "not
   enrolled" with prev_* missing.

5. P7, CLEAN-12 (Should): decode tp_sector and tp_specialty to Anexo VI's words. Keep COD_MEN decoded
   (Anexo X) instead of dropping it, or give a reason that is a CLEAN-22 reason. Commune names are
   optional (lossless as codes).

6. P7, CLEAN-12/14 (Should): combined_course merges codes 1-6 into "Yes", which loses information. Keep
   the six codes.

7. P7, CLEAN-11 (Should): ages <=4 (123 rows) are impossible. Set them and their birth month to missing.
   The 138 rows aged >=30 in children's programmes can stay as unusual, with a note. Tiny.

8. Writing: name SIT_FIN among the dropped columns (an exact copy). Reword the ESTADO_ESTAB reason (see
   DROPPED COLUMNS).

Not checked:
- Whether the Rodriguez et al. paper handled IPE changes: PMC served a captcha.
- Whether a twin found in another school is the same student. The bound in problem 1 is a lower bound.
- The SLEP-timing check covered only the 2024->2025 switch.

</details>

<details><summary>Split audit</summary>

SPLIT AUDIT: chile_school_dropout_mineduc (folder chile_school_dropout_mineduc_1m), 2026-11-09, split-auditor

VERDICT: right with notes.
The temporal regime, the yearly windows, the expanding train side and the zero gap all match the use case. No change to
the split is needed. Two notes for the splits_comment: the COVID-19 break in how attendance was recorded (not only in
the dropout rate), and the change in the label's definition inside the history (special education from the 2023 file).

Judgment record
  Validity: USE-10 holds (students and schools are known entities: temporal, no grouping); SPLIT-1/SPLIT-3 hold
    (temporal); SPLIT-9 not triggered (no training label is set after a test row's prediction point); SPLIT-10 holds
    with no gap (the label of t-1 is final when year t's file closes, which is the prediction point of year t);
    SPLIT-11, SPLIT-12, SPLIT-14 (first train side 56.5%), SPLIT-15 hold; SPLIT-20 holds but the notes should say
    more (the attendance-recording break of 2020-2021 and the label-definition change of 2022).
  Weighed: the IID optimism is measured (+0.010 to +0.017 AUC), so the temporal split matters.

Inputs read: dataset.py (task_summary, splits_comment, Temporal(on="year", window=1 unique, n_windows=3, horizon 1
year), RowBudget 1M/500k), builder_report.md, claims.md, probes/hidden/summary.md, the record, splits.md /
use_case.md / principles.md in df-large. Frame and splits reloaded fresh through dataset_io.from_definition (the
builder's cached frame.parquet predates the last dataset.py edit and differs; the splits are identical). Work files:
the run folder (load.py, describe.py + describe.log/describe2.log, alternatives.py + alternatives.json,
recurrence.py + recurrence.log).

1. REGIME (USE-10, SPLIT-1, SPLIT-3, SPLIT-13): right.
   The actor is the ministry or a school director. They act at the close of year t, on students and schools already
   in the system. That is a known-entity stream over time, so the split is temporal and history is a legitimate input.
   - Students recur: 89.0% / 89.7% / 90.2% of the 2022 / 2023 / 2024 population have a row in 2018..t-1 (3.0 / 3.5 /
     4.0 earlier rows on average). The shipped 1M train side holds at least one earlier row for an expected 24.1% /
     22.5% / 21.2% of test students. The deployed ministry model would have all of them, so this is part of the task.
   - Shortcut check (SPLIT-9): every training row (s, t-1) of a test student s is labelled "No". Measured: 0 of the
     t-1 rows of test students are dropouts. This follows from s having a regular course in year t, which the test row
     already shows through prev_programme. These labels are set by the year-t file, the same file that gives the test
     row's own features, so they are not after the prediction point. No shortcut.
     0.7% to 1.0% of test students carry an earlier "dropout" label (they left and came back): history, known then.
   - Schools: 99.79% / 99.89% / 99.88% of a test year's schools appear in earlier years (the probe's figure of 99.9%
     is per row). A known entity, so school_id is legitimate under the temporal split.
   - The source's paper also tests on one whole later year (a test set of 2,802,156 trajectories, 1.7% dropouts). Its
     design and ours agree.

2. TIME COLUMN, WINDOWS, SIZES (SPLIT-11, SPLIT-12, SPLIT-14, SPLIT-15, SPLIT-17): right.
   - `year` is the school year t of the features. The label comes from the file of t+1, and the history from t-1.
   - Windows (newest first). The train side is an expanding random 1M, and there is no overlap between train and
     test in any window:
       2024: test 500,000, 13,989 positives (2.80%); train 2018-2023, 1,000,000, 2.36%, about 165k per year
       2023: test 500,000, 14,589 positives (2.92%); train 2018-2022, 1,000,000, 2.24%
       2022: test 500,000, 13,870 positives (2.77%); train 2018-2021, 1,000,000, 2.10%
   - SPLIT-14 floor: the first train side, 2018-2021, holds 10,964,808 of the 19,404,374 population rows (56.5%). A
     fourth window (2021) would train on 3 of 7 years (42%), so 3 windows is the maximum under the floor.
   - Each window has its own train side, drawn from one random order (the sides overlap: 2024/2023 share 829,782 rows,
     2024/2022 660,693, 2023/2022 795,848). That fits SPLIT-14: each refit sees what was known before its window.
   - Season shape: one window is one full school year, the decision's cadence (yearly refit, horizon 1 year,
     SPLIT-12). The test years 2022-2024 come after COVID and look alike (dropout 2.77% to 2.92%, attendance below 85%
     in 18% to 23% of rows). None of them is an atypical season.
   - `year` is a feature by repository convention. Measured effect: dropping it changes AUC by -0.0001 / +0.0022 /
     +0.0018 (2024 / 2023 / 2022). Harmless.

3. GAP AGAINST THE LABEL DELAY (SPLIT-9, SPLIT-10): no gap is right. A window may train on year t-1's rows.
   - The label of year t-1 is "no course outside adult education in the file of year t". That file closes at the end
     of January of t+1. The prediction point for the test year t is the close of year t, after the year-t file is cut,
     because year t's final status, GPA and attendance come from that same file. The training labels of t-1 and the
     test inputs of t therefore arrive at the same moment. Every training label is final at each window's start, and
     the outcome horizon is fixed (one year for every row), so the outcome does not select rows (SPLIT-10's "fixed
     outcome horizon" case).
   - A publication lag exists only for outsiders. The open files appear 1 to 8 months after the cut (the 2022 file in
     February 2023, 2023 in September 2024, 2024 in April 2025, 2025 in March 2026). The actor is the ministry, which
     holds the records at the cut. Even for an outsider, the t-1 labels and the year-t inputs come from the same file,
     so a gap would never be needed.
   - What year t-1 adds, untuned LightGBM, 300k training rows per window:
       shipped:              0.8434 / 0.8591 / 0.8568
       gap of 1 year:        0.8355 / 0.8386 / 0.8572
       t-1 only (170-253k):  0.8449 / 0.8572 / 0.8446
     The newest year is worth 0.008 to 0.021 AUC, except for the 2022 window, whose t-1 is 2021, a COVID year. A
     gap would remove legitimately known data, so do not add one.

4. TRAINING HISTORY AND THE COVID-19 YEARS (SPLIT-20, SPLIT-21): kept, with a note to add.
   - The splits_comment mentions the break only through the dropout rate (1.5% / 1.9% against about 2.5% and 2.8%).
     The measured break is bigger: attendance was recorded differently.
                                 2018   2019   2020   2021   2022   2023   2024
       attendance recorded 100%  6.3%   5.6%  45.3%  24.1%   4.1%   4.4%   5.0%
       attendance below 85%     10.3%  13.6%   3.0%  10.1%  22.5%  20.1%  17.9%
       failed                    3.5%   2.7%   1.2%   2.2%   1.8%   1.9%   1.8%
       withdrawn                 1.4%   1.4%   0.6%   0.9%   1.7%   1.6%   1.5%
       dropout, attendance <=50% 27.3% 23.1%   7.5%   4.9%  16.9%  15.6%  15.4%
       dropout, withdrawn        63.9% 68.4%  58.2%  67.4%  65.3%  72.3%  71.8%
     In 2020 and 2021 the link between attendance and dropout nearly vanishes. That is the remote-schooling years'
     recording, a change of data collection. The 2021 attendance also feeds prev_attendance_pct of the 2022 rows,
     which are the 2022 test window's own inputs, as the deployed model would see them.
   - Alternative history (no 2020 and 2021 rows in train, same 300k): 0.8472 / 0.8646 / 0.8537 against 0.8434 /
     0.8591 / 0.8568 shipped, a change of +0.004 / +0.006 / -0.003. The effect is small and mixed. Under SPLIT-21 a
     comparison over 3 windows cannot decide the history in any case. Dropping the COVID rows would also leave the
     2022 window only 2018-2019 (29% of rows), which breaks SPLIT-14's floor.
     Keeping them is the defensible call: a ministry refit would have trained on those years. The note should say so
     with these numbers.
   - The label's definition changes inside the history. Special education enters the files in 2023, so for the labels
     of 2022 onward a move into special education counts as enrolled (3,025 / 1,619 / 1,502 students). For 2018-2021
     the same moves count as dropouts (unseen), about 4% of a year's dropouts. The windows 2023 and 2024 train on a mix
     of both definitions. The curation_comments state this as an anomaly; the splits_comment does not. This is a
     SPLIT-20 "change of the data collection" and is small.

5. IID AGAINST TEMPORAL (what the regime is worth). Each window's test rows were split in half. Untuned LightGBM was
   trained on 300k random rows of all years plus the other half, and scored on that half:
       IID reference:                0.8552 / 0.8690 / 0.8735
       shipped on the same half:     0.8447 / 0.8577 / 0.8566
   IID overstates the score by 0.011 / 0.011 / 0.017. The drift is real, so the temporal split matters.

6. NOTHING ELSE FOUND.
   No exact copies across the split (leak probe 5: 0.0%). No hidden group beyond the known-entity school (hidden-group
   probe: school_id 99.9%, near copies 0.1%). The 2.5M frame holds only rows that some split uses. No train/test
   overlap.

PROBLEMS, RANKED (principles.md: all P4, all mild; none is a Must violation)
  1. P4, SPLIT-20 (Should): the COVID-19 break in recording is not documented. Evidence: attendance 100% for 45.3% and
     24.1% of rows in 2020 and 2021 (4% to 6% otherwise); dropout under 50% attendance falls from 23-27% to 5-8%.
     Remedy (mildest: a note): add one sentence to splits_comment with these rates and the measured cost of keeping
     the rows (-0.003 to +0.006 AUC without them), kept because a yearly refit would train on them and dropping them
     breaks the 50% floor for the 2022 window. No re-split.
  2. P4, SPLIT-20 (Should): the label definition changes inside the training history (special education visible only
     in the labels from 2022). Evidence: 3,025 / 1,619 / 1,502 moves into special education are "No" from 2022, while
     the same moves before are "Yes"; about 4% of a year's dropouts. Remedy (a note): one clause in splits_comment
     pointing to the curation_comments anomaly. No filter: the pre-2022 cases cannot be identified.
  (No issue: the zero gap, the windows, the floor, the recurrence of students and schools; all measured above.)

Sources: Rodríguez et al. 2023, doi:10.1007/s10639-022-11515-5 (test year of 2,802,156 trajectories, via the record);
dblp entry https://dblp.uni-trier.de/rec/journals/eait/RodriguezVDV23.html (the PMC full text was behind a browser
check and not read).

</details>

<details><summary>Domain practitioner</summary>

DOMAIN PRACTITIONER REPORT: chile_school_dropout_mineduc_1m (record chile_school_dropout_mineduc), 2026-11-09
Actor played: Mineduc's early-warning team (Sistema de Alerta Temprana, SAT, run with the Unidad de Retencion Escolar)
and a school's retention or management team that reads the SAT list.

VERDICT
Fit: approximate (agree with the builder, USE-8), for a reason the builder did not name. The rows, the timing, the
inputs and the yearly refit match an end-of-year list well. But the label "absent from next year's file" also counts
children who are still in the same school next year under a new student id, at least 10-13% of the positives. That
gap is larger than deaths, and it is the one gap here that can be repaired. Two more gaps: grades 1-6 basic are rows
although the SAT covers 7th basic to 4th secondary, and inputs the ministry always has are missing (the socioeconomic
records, the provisional-id or nationality flag, next year's pre-enrolment).
Metric: partly. ROC AUC (fallback, MET-8) is a sound threshold-free score and ranks models in the same order as my
decision in the runs below, but it scores a national ranking over all grades. My decision is a per-school list of
fixed size: the SAT shows each director "el 10% de mayor riesgo" of their students in 7th basic to 4th secondary.
The metric I would choose is precision (or recall) of the per-school top 10% in grades 7 to 12, which needs a group
metric with school_id as a scoring column (MET-7, MET-2). If the curator does not accept the SAT sheet as a fixed k,
keep roc_auc.

HOW THE DECISION IS MADE TODAY (sources at the end)
- Mineduc launched the SAT in 2019 (first in the four SLEPs, 294 schools, from 1 Oct 2019) and opened it to the whole
  system in 2020. It crosses administrative records (education; RSH social registry; Chile Crece Contigo; SENAME;
  health; census) with "metodologias de analitica avanzada" to give a "identificacion PRIORIZADA" of the students at
  risk. It covers 7th basic to 4th secondary.
- What the director sees (Mineduc's IDPS retention sheet 8, "Estudiantes en riesgo de desercion: quienes son y como
  nos contactamos con ellos"): "la nomina de estudiantes del 10% de mayor riesgo a atender, priorizada e
  individualizado por el RUN, nombre completo y el curso". The team counts the at-risk students per course, contacts
  every listed student and family, and tells them "este ano recibira apoyo especial". So the decision is: a fixed
  fraction (10%) of each school's students in grades 7-12, ranked, and each one gets a contact and support.
- Mineduc's own dropout measure (Centro de Estudios, Serie Evidencias N 15, 2013; Documento de trabajo N 20, 2020) is
  the incidence rate built from the same Rendimiento files. "Desercion del sistema regular" counts students who leave
  the children's and youth system "aun cuando hayan continuado sus estudios en el sistema de adultos": that is this
  dataset's label. The ministry removed deaths only as an aggregate correction from mortality rates (fn. 15). It
  reports 2.4% for 2018; the dataset has 2.46% for 2018. So the label is the ministry's own regular-system measure,
  and the deaths and exam-route graduates are a small part of the noise (deaths at ages 6-18 are of the order of 0.02%
  a year, against 2.5% positives).

QUESTION BY QUESTION, IN MY VOICE

1. Do I have each input at the prediction point (year close, end of January of t+1, before the March start)?
   Yes, for all 27. The final status, GPA, attendance and transfers of year t are in SIGE once the school closes the
   year in December; the previous year's record, the school and the home commune are known. I see no input I would
   not have (USE-3 holds, LEAK-10 holds).
   Inputs I would always have that are missing:
   (a) The student's socioeconomic records (RSH tier, SEP priority status, Chile Crece Contigo, SENAME), which the SAT
       uses. They are not in the open data. This is what the source's NDA variables stand for; the builder names it.
   (b) Whether the student has a provisional school id (IPE) or is foreign-born. I know this for every student, and it
       drives the label artefact in gap 1 below. The open files carry no flag; MRUN order is a proxy and is dropped,
       rightly.
   (c) Next year's enrolment as far as I know it at year close: the SAE admission result and the December
       re-enrolment of continuing students. Not in the open files.
   (d) More than one year of history (repetitions, over-age, school changes over several years), and monthly
       attendance (the portal publishes it). Over-age can be derived from age and grade, so this is a minor gap.
   None of these invalidates the task. They are why a model here scores below what the SAT could do (USE-8).

2. Is the target what I act on?
   Mostly. "Not in regular schooling next year" is the ministry's measure, and it is what the SAT list is meant to
   prevent. I want a probability, used as a rank within my school. Three label issues, ranked:
   - NEW, the largest: children re-registered under a new id. I tested it on the raw files (scripts and logs in
     work_domain_practitioner/: a1.py, a2.py, a3.py). Take the students of year t marked "absent" in t+1. Count how
     many have a student in the t+1 file whose MRUN is not in the year-t file and who has the same school, sex and
     birth month. Compare with a placebo that shifts the birth month by -2 and +2 months. Excess matches: 7,176 of
     70,145 dropouts in 2019 (10.2%); 8,259 of 78,273 in 2022 (10.6%); 10,588 of 82,257 in 2023 (12.9%). This is a
     lower bound: a child who also changed school is not counted. These are most likely children whose provisional
     id (IPE) was replaced by a RUN, so the masked id changed. In 2019 all of the excess is in the top 5% of MRUN
     (the newest ids). The top 5% of MRUN, over all years, has a 17.1% "dropout" rate against 1.5% for the rest and
     holds 35% of all positives (a1.py). The source (Rodriguez et al.) linked on the ministry's internal RUN and did
     not have this artefact. To me these are children sitting in my classroom next March. A list that ranks recently
     arrived immigrant children at the top is wrong, and it is wrong in a way that stigmatises them. This is a USE-5
     gap, and the builder's notes and fit_reason do not name it.
   - Adult education counts as dropout (18-36% of positives by year). This is the ministry's "regular" measure and the
     source's definition, so I accept it. A school loses the student either way. Mineduc's newer "desvinculacion"
     figures (about 40-50k a year) count leaving the system altogether, so the global measure is a defensible
     alternative. I would not change the label, but I would say in the notes that both measures exist.
   - Deaths, emigration, exam-route graduation: real but small for deaths; emigration is unknown. The builder names
     them correctly. Special education (in the files from 2023): only 1.5k-3k moves a year, 2-4% of positives. The
     2022 test labels count them as enrolled; in the training years they cannot be seen and count as dropouts. This
     is a small shift. Special-education students as rows: leave them out. The SAT targets regular courses, and the
     special-education outcome works differently (GPA 0.0 in 28,897 of 30,459 of its courses). Adult education as
     rows: leave it out too. Adult students are not on the SAT list and their dropout process is another one. I agree
     with the builder on both.

3. Does one row match one decision? Is the test data what I would face?
   One row is one student at year close: yes, the unit I list. The test is next year's cohort in the same schools
   (99.9% of test schools are seen in training), with a yearly refit: yes, that is how I would deploy it (USE-10, a
   known entity, so a temporal split). The mismatch is the population:
   - Grades 1-6 basic are 55% of rows and 37% of positives. My list does not cover them. 56% of their dropouts were
     promoted in year t, so they are mostly emigration, homeschooling (examenes libres) and the id artefact, not
     school leaving. I would restrict the rows to 7th basic to 4th secondary: the builder's issue 3, option (b), which
     keeps 63% of the dropouts. On the SAT population the model's pooled AUC is 0.855-0.883; on grades 1-6 it is
     0.819-0.836 (a4.py).
   - Students withdrawn in year t (1.3% of rows, 36% of positives) have already left the school by year close. For
     them the action is re-engagement (revinculacion) by the SLEP or Mineduc, not retention by the school. Both are
     real decisions on the same list, so I accept the builder's option (a), keep them. A per-school metric limited to
     students not withdrawn would be the stricter school-team view.

4. Would I use this model? What makes me trust or distrust it?
   Trust: the inputs are what I have. It beats the rule a school team uses today (withdrawn > failed > attendance below
   85%) in every window (a4.py, untuned LightGBM on 300k training rows, grades 7-12):
     window  pooled AUC  rule AUC  within-school AUC (model / rule)  per-school top-10% precision / recall (model / rule)
     2024    0.855       0.783     0.817 / 0.767                     0.188 / 0.581  vs  0.172 / 0.531
     2023    0.872       0.793     0.836 / 0.777                     0.203 / 0.606  vs  0.183 / 0.546
     2022    0.883       0.812     0.849 / 0.799                     0.204 / 0.615  vs  0.187 / 0.566
   A 10% list per school catches about 60% of the school's dropouts, with one true positive in five names. That is
   usable for a contact-and-support action.
   Distrust: the id artefact. The model learns "new id, no previous record, immigrant-heavy school" -> dropout. 23% of
   test dropouts have no previous-year record, and 23% of the grade 7-12 students without one drop out. I would not
   send this list to a school without first removing the re-registered children from the label. I would also want a
   calibration check per year: the COVID years 2020 and 2021 at 1.5% and 1.9% sit in the training side of every
   window.

5. Does the metric score my decision?
   Partly. ROC AUC pooled over the nation and all grades mixes two things: ranking schools (the school's training-side
   dropout rate alone scores 0.67 pooled AUC on grades 7-12) and ranking students within a school, which is all a
   director can act on. Within-school AUC is 0.03-0.04 below pooled. In these runs pooled AUC, within-school AUC and
   per-school top-10% precision all rank the model above the rule, so ROC AUC is not misleading here. It can still
   reward models that are good at sorting schools rather than students.
   What I would choose: precision at the per-school top 10% (equivalently recall, at a fixed list size) on grades 7-12.
   This is MET-7: the deployed decision fixes k as 10% of each school's students. It is a source fact from Mineduc's
   own SAT guidance, not an invented threshold. It needs school_id shipped as a scoring column (MET-2: school_id is
   also a feature, so it ships twice) and a group metric. The library has precision_at_k and
   mean_group_top_k_overlap, but no per-group top-fraction precision that I know of.
   Caveat: the 500k test sample keeps about 18% of each school, so a school's 10% list is 1 to 10 names. That is
   noisy per school, but averaged over about 2,900 schools a window it is stable.
   If the curator holds that the SAT sheet does not fix k for the source (the paper fixes none; MET-5 and MET-6 already
   send it to the fallback), keep roc_auc (MET-8). Average precision is not called for by imbalance alone (MET-9);
   national precision_at_k without the school grouping is the wrong unit.

GAPS RANKED BY HOW MUCH THEY CHANGE THE TASK
1. Label: the same child at the same school under a new id counts as a dropout (lower bound 10-13% of positives, 35% of
   positives in the top 5% of ids). USE-5. Not named in the notes or the fit_reason. It can be repaired from the open
   files.
2. Population: grades 1-6 basic (55% of rows, 37% of positives, largely emigration and re-registration) are outside the
   deployed list. USE-1, USE-5; the builder's issue 3.
3. Metric unit: national pooled AUC over all grades against a per-school top-10% list for grades 7-12. MET-1, MET-7.
4. Missing inputs the actor always has: social registry, priority status, IPE or nationality flag, pre-enrolment.
   USE-8; this explains a lower ceiling, not a wrong task.
5. Label composition choices: adult education counted as dropout (the ministry's regular measure, accepted); deaths and
   emigration (small or unknown); the special-education break of 2023 (2-4% of positives). All named by the builder.
6. Withdrawn-in-year students mix re-engagement with retention. Accepted, a note only.

WHAT A DOMAIN EXPERT WOULD CHANGE
- Repair the label: for each student absent in t+1, look for a unique student in t+1 with an MRUN not seen in year t
  and the same school (or commune), sex and birth month, at the expected grade (promoted: next grade; failed: same
  grade). Count such a student as enrolled, and document the rule and its placebo rate. At the least, add the artefact
  to the anomaly bullet and to the fit_reason with the numbers above.
- Restrict the rows to 7th basic to 4th secondary, the SAT population (issue 3 (b)). If all grades stay, say in
  task_summary.use_case that the list covers grades 7-12 and the rows go wider.
- Name the actor precisely in use_case: the SAT list a school's director reads as the top 10% of the school. Cite the
  Mineduc sheet rather than "a school's director ranks the students".
- Metric: propose the per-school top-10% precision on grades 7-12 to the curator (MET-7), with roc_auc as the
  fallback if k is not accepted as fixed.
- Keep: the prediction point at year close with year t's outcomes as inputs, the adult-education definition, the
  exclusion of special and adult education as rows, school_id as a known entity, the yearly refit.

SOURCES
- Mineduc, IDPS Retencion Escolar, Ficha 8 "Estudiantes en riesgo de desercion: quienes son y como nos contactamos con
  ellos" (the SAT list = top 10% per school, grades 7-12; data sources RSH, ChCC, Sename, Salud, Censo):
  https://www.curriculumnacional.cl/614/articles-90161_galeria_11.pdf (read via pypdf).
- La Tercera, 17 Sep 2019, launch of the SAT in the SLEPs:
  https://www.latercera.com/nacional/noticia/funcionara-sistema-alerta-temprana-escolar/826668/
- La Tercera, 2022, 39,497 students "desertaron en 2021", the SAT covers 7th basic to 4th secondary:
  https://www.latercera.com/nacional/noticia/pese-a-la-pandemia-exclusion-escolar-se-mantiene-en-rangos-similares-a-anos-anteriores-39497-alumnos-desertaron-en-2021/OUYQLY5A55C23BNOPVS54KH6UY/
- Centro de Estudios Mineduc, Serie Evidencias N 15 "Medicion de la desercion escolar en Chile" (2013), the definitions
  of global and regular incidence, the deaths correction:
  https://rtei.okfn.org/documents/Medicion_de_la_Desercion_Escolar_en_Chile.pdf
- Centro de Estudios Mineduc, Documento de trabajo N 20 (2020), 2018 rates of 1.4% global and 2.4% regular (seen in a
  search snippet; the PDF host failed TLS).
- BioBioChile, 12 Nov 2024, 47,509 students "desvinculados" in 2024:
  https://www.biobiochile.cl/noticias/nacional/chile/2024/11/12/amp/desvinculacion-del-sistema-escolar-se-redujo-en-un-65-en-2024-piden-mayor-enfasis-en-revinculados.shtml
- Mineduc SAT pages (mineduc.cl/?p=22673; /sistema-de-alerta-temprana-contra-la-desercion-escolar/): the connection
  was refused, so I used only search snippets.
- Rodriguez, Villanueva, Dombrovskaia, Valenzuela 2023 (doi 10.1007/s10639-022-11515-5), via the builder's notes;
  PMC served a captcha.
- The record layout "Esquema de registro ... 2002-2024" in the warehouse (MRUN = "mascara del RUN"; no IPE flag).
- My runs, in work_domain_practitioner/: a1.py (label by MRUN ventile, grade and previous record), a2.py and a3.py
  (re-registration test with the placebo, raw files 2019/20, 2022/23, 2023/24), a4.py and a4_out.json (pooled,
  within-school and per-school top-10% scores on the shipped splits, with the builder's cached frame).

RULES CITED: USE-1, USE-3, USE-5, USE-8, USE-10; LEAK-10; MET-1, MET-2, MET-5, MET-6, MET-7, MET-8, MET-9.

</details>

<details><summary>Blind review</summary>

BLIND REVIEW: chile_school_dropout_mineduc
Inputs used: clean_room/data.parquet, clean_room/task.md, public web only. No other local file was opened.
Scratch: work_blind_reviewer/m.py (LightGBM ablations), work_blind_reviewer/pmc.xml (paper full text via PMC OAI).

VERDICT: Include with changes. It is a real, large, well-motivated administrative early-warning task with a correct
temporal split. But as prepared, the label partly restates a feature: 36% of positives are students whose same-year
final_status is already "withdrawn". The prediction time has to be fixed and the features made to match it.

WHAT THE TASK IS
One row is one student-year from Chile's public MINEDUC "Rendimiento por estudiante" files, regular children/youth
programmes, grades 1st basic to 4th secondary, years 2018-2024. Each row has school context, demographics, the
year-end outcome for year i (final_status, gpa, attendance_pct, transfers_in_year) and the same outcome for year i-1
(prev_*). The target is dropout = not enrolled anywhere in year i+1. This matches the cited paper (Rodriguez et al.
2023, Educ Inf Technol): "if they in a given year (i) are not enrolled in any school in the next year (i+1) ... we label
that student as a dropout in year i." MINEDUC runs a real Sistema de Alerta Temprana (since 2019, grades 7-12) that
flags at-risk students from administrative data, so the use is real: a ministry or local education service ranks
students for outreach. Base rate 2.6% (5,134 / 200,000 in the sample; about 64k positives in the 2.5M full data).
Split: expanding-window by year. I assumed the test years are 2022, 2023 and 2024.

CONCERNS, MOST TO LEAST SERIOUS

1. The prediction moment is undefined, and same-year "withdrawn" status makes much of the task trivial (serious).
   - final_status=withdrawn: 67.6% dropout (1,865 / 2,759). promoted: 1.3%. failed: 16.8%.
     Withdrawn rows are 1.4% of rows but 36.3% of all positives.
   - The withdrawn student has already left school during year i. Predicting that they will not be enrolled in March
     of i+1 is mostly bookkeeping, not early warning. gpa/attendance are NaN exactly when final_status=withdrawn
     (2,759 / 2,759), so missing gpa alone is a second copy of the same signal.
   - LightGBM, train on all prior years, test 2022/2023/2024:
       all 27 features:                       AUC 0.843 / 0.867 / 0.844   PR-AUC 0.38 / 0.43 / 0.40
       5 columns only (final_status, grade, age, gpa, attendance): PR-AUC 0.40 / 0.43 / 0.41 (same as the full model)
       final_status alone as a score:         AUC 0.74 / 0.75 / 0.72
       drop current-year outcomes (start-of-year prediction): AUC 0.72 / 0.75 / 0.76   PR-AUC 0.11 / 0.14 / 0.13
       drop withdrawn rows:                   AUC 0.75 / 0.78 / 0.76   PR-AUC 0.09 / 0.12 / 0.09
     Most of the headroom in PR-AUC comes from one already-observed event.
   - This is not strictly leakage. Year-end status is known in December/January, before March enrolment, and the
     public Rendimiento file is released around the same time. But it does not match how an early-warning system is
     used: SAT flags students who are still enrolled, early enough to intervene.
   - Change: choose one of the following and state it in task.md.
     (a) End-of-year prediction (preferred): keep the current-year outcomes, drop rows with final_status=withdrawn
         (or withdrawn mid-year), and predict non-return among students who finished the year.
     (b) Start-of-year prediction: drop final_status, gpa, attendance_pct and transfers_in_year and keep only prev_*.
     Either gives a harder task that is closer to the real use, with AUC around 0.75 and plenty of model spread.

2. Undocumented subsampling, unequal across years (moderate).
   - Rows per year in the sample: 2018-2021 about 20k each, 2022-2024 about 40k each. Chilean enrolment did not
     double, and the full data (2.5M) is only about 10% of the roughly 3M student-years per year x 7 years.
   - So the 2.5M table is itself a stratified or unequal sample of students or rows. Its scheme is not stated, and
     it changes the train/test mix: test years are over-represented relative to train.
   - Change: document the sampling, or sample uniformly (by student, keeping each sampled student's full history).

3. Target construction details are unverifiable and may differ from the source paper (moderate).
   - The paper builds trajectories from linked multi-source data (SIMCE, socioeconomic) and handles the move to
     adult education as a separate case ("In 2019, 57,130 students left regular education to adult modality. In
     contrast, only 36,230 students dropped out").
   - From the table I cannot tell whether enrolment in adult or special education in i+1 counts as "not dropout",
     how mid-year transfers with several records were resolved into one row, or whether deaths/emigration are
     excluded.
   - Grade 12: promoted 4th-secondary students (graduates) are correctly removed, but the 351 remaining
     4th-secondary rows are only failed/withdrawn (70.9% dropout), so grade=4th secondary is itself a near-label.
     Acceptable, but it should be documented.
   - Change: document the label rule (which programmes in i+1 count as enrolled; how graduates and transfers are
     handled).

4. The 2020-2021 COVID years are in training (minor; arguably a feature).
   - Dropout 1.4% in 2020 vs 2.3-2.9% in other years. Failed share 1.3% in 2020 vs 3.5% in 2018 (automatic-promotion
     policy).
   - The temporal split handles this honestly. Just note the shift.

5. Column preparation (minor).
   - birth_month is datetime64. It is redundant with age_june_30 + year (age = floor of the difference; checked).
     Convert it to month-of-birth (int) or drop it, so that methods without datetime handling work.
   - school_id is a categorical with 7,766 levels in the 200k sample. Removing it raised LightGBM AUC (2024:
     0.844 -> 0.862; PR-AUC 0.40 -> 0.43), so it mainly overfits. Keep it as a high-cardinality categorical, but
     expect method-dependent behaviour.
   - grade is an unordered category but is ordinal. Consider adding an integer grade or using ordered categories.
   - tp_sector/tp_specialty use "0" as the not-applicable code. This is fine because they are categorical.
   - Small issues: 3 exact duplicate rows; 2 rows with age 4 in 5th/7th basic; age up to 44 (19 rows over 20);
     7 rows with age NaN; shift="evening or night" has 2 rows. All negligible.
   - residence_region and school_region/commune are near-copies. This is harmless.

6. Repeated students across years (minor).
   - There is no student id, so the same student appears in several years (prev_* links them).
   - With a strict year-forward split this is legitimate (a deployed model sees returning students too). I could not
     check for within-year duplicates of the same student caused by multiple enrolment records.

WHAT IS FINE
- Real public administrative data: plausible Chilean 1.0-7.0 grade scale (mean 6.0), attendance 0-100,
  region/commune codes consistent, school dependency categories real.
- Strong but non-trivial signal.
- Large: about 64k positives in the full data; about 1,100 positives per test year even in the 200k sample.
- The temporal split matches deployment.

COULD NOT CHECK
- The raw MINEDUC files and their variable dictionary. The portal page lists annual .rar files for 2002-2025 but no
  codebook text was retrievable. mineduc.cl/?p=22673 refused the connection; its title via search is "Sistema de
  Alerta Temprana".
- The exact label rule: adult-modality re-enrolment, graduates, transfers, record deduplication.
- How the 2.5M rows were drawn.
- The exact test windows: I assumed 2022, 2023 and 2024.
- The licence: none was stated on the portal page.
- The Springer page itself was paywalled or redirected. The paper text came from the PMC OAI full text.

</details>

<details><summary>Task gamer</summary>

**TASK GAMER REPORT: chile_school_dropout_mineduc (panel), target dropout, ROC AUC, temporal on year**

Verdict: inside a harness that passes only each split's train and test rows, the task barely gives; the one real
exploit (+0.016 AUC on two of three splits) needs the later years' rows that sit in the shared data.parquet.

Setup
- data.parquet: 2.5M rows; years 2018-2021 have ~250k rows each, 2022-2024 have 500k each. Rows are sorted by year,
  shuffled within year.
- Splits: r0 = train 2018-2023 (1M) / test 2024; r1 = train 2018-2022 / test 2023; r2 = train 2018-2021 / test 2022.
- Honest baseline: LightGBM, 400 trees, lr 0.05, 63 leaves, all features() (birth_month as year*12+month), native
  categoricals. Script work/exp_main.py, results in work/exp_main.json.
    baseline        r0 0.86772   r1 0.87744   r2 0.87656
    + random column r0 0.86796/0.86793  r1 0.87751/0.87701  r2 0.87721/0.87635  (noise spread about +-0.0007)

Exploits ranked by gain
| # | Exploit | Script | Honest | Exploited | Gain per split | Deployed model has it? | Fix |
|---|---------|--------|--------|-----------|----------------|------------------------|-----|
| 1 | Find the test student among the next year's rows in data.parquet (birth_month+sex+gpa+attendance_pct+school_id = next year's prev_gpa+prev_attendance_pct+school_id with changed_school=No; looser match on residence_commune), then push found rows to the bottom | work/exp_main.py, work/post.py, work/exp_main_link.py | 0.86772 / 0.87744 / 0.87656 | 0.86772 / 0.89423 / 0.89305 | r0 +0.000 (no 2025 rows), r1 +0.0168, r2 +0.0165 | No: the next year's enrolment IS the label | Give each split only rows with year <= test year (or make sure the harness never exposes other splits' rows); or sample students, not student-years, so that one student appears in at most one year; or coarsen prev_gpa/prev_attendance_pct |
| 2 | Same-year school aggregates over the test rows (sample share per school, withdrawn/failed share, mean attendance) | work/exp_more.py | same | 0.87024 / 0.87981 / 0.87690 | +0.0025 / +0.0024 / +0.0003 | Yes: at year end the ministry has every student's final status, so this is signal, not an exploit | None needed |

Mechanism, exploit 1. The kit samples about 14% of student-years each year, independently, so about 14% of year-t
students also appear in the year-t+1 sample, where their prev_gpa and prev_attendance_pct repeat their year-t gpa and
attendance exactly. A strict key (birth_month, sex, gpa, attendance_pct, school_id vs. the t+1 row's prev values and
school with changed_school=No) is unique for 99.6% of rows; placebo match (birth year shifted) is 0.25%. A match means
the student was enrolled in t+1, which is the label: in test 2023, 13.7% of rows match, dropout rate among them 0.012%
(base 2.9%); in test 2022, 13.6% match, rate 0.031%. Loose matches (residence_commune instead of school, any school
change) add 6% of rows at a 0.9-1.0% rate. Setting matched predictions to p*1e-3 (strict) and p*0.5 (loose only) gives
r1 0.89423, r2 0.89305. No gain on r0 because there is no 2025 data. It only works if the participant can read rows
outside its split, which the kit's single data.parquet allows. Mildest fix: per-split data restricted to year <= test
year; stronger fix: sample by student so the panel cannot be relinked (this also removes the honest history that
linking would give).

Flaws that hurt an honest model: none found.
| What | Honest choice | Baseline | Honest choice score |
| COVID years 2020-2021 (dropout rate 1.5%/1.9% vs 2.4-2.9%) in training | drop 2020-2021 | 0.86772/0.87744/0.87656 | 0.86371/0.87550/0.86271 (worse) |
| Old years in training | keep last 2 training years only | same | 0.85371/0.86388/0.85828 (worse) |
The training labels of the last training year need the following year's enrolment, which is the test year's
enrolment (known by March of the test year, before the year-end prediction point), so they are available in time.

Attacks that found nothing
- Row order: within each year, label by position deciles is flat (2018: 0.0228-0.0266; 2024: 0.0270-0.0295);
  P(next row positive | positive) equals the base rate (2024: 0.0289 vs 0.0280); consecutive rows share a school
  0.03-0.05% of the time. Rows are sorted by year only.
- Ids: school_id is the real school code (RBD), a deployed-model feature; its range grows with new schools, no label order.
- Exact copies across the split (all features except year and age): 0 / 0 / 4 test rows; within-test duplicates <=0.05%.
- Formats: gpa has one decimal, attendance and age are whole numbers in both classes. Digit-only features (gpa tenths,
  attendance last digit, missingness hidden by random fill): AUC 0.555 / 0.546 / 0.541, and 0.531 / 0.522 / 0.518
  on rows with gpa present (weak, consistent with attendance 100 ending in 0). Missingness looks predictive (format
  model with NaN flags 0.739-0.753) but gpa/attendance NaN is exactly final_status = withdrawn (34,527 of 34,527) and
  prev_* NaN is prev_programme = not enrolled: same information as real columns, not an artefact.
- Columns after the prediction point: the best single feature is gpa (0.744 / 0.731 / 0.717) or final_status
  (0.733 / 0.748 / 0.753), far below the full model (0.87); final_status, gpa and attendance are year-end values the
  prediction point allows. changed_school and prev_* look back to t-1, not forward. work/single_feature.txt.
- Label-dependent rows: 4th-secondary promoted students (graduates) are absent from every year, so the remaining 4th
  secondary rows are 69% dropout; a deployed model knows graduates do not drop out, and the filter is the same in
  train and test. Not an exploit.
- Transforms over all rows: none; gpa (1-7), attendance (0-100) and age are raw values.
- Train vs test classifier without year/birth_month/age: AUC 0.734 / 0.785 / 0.852, driven by school_id and
  attendance (COVID-era attendance, new schools): ordinary temporal drift, not exploitable for the label.
- Label from rows two years ahead (whether dropouts re-enter in t+2): the key (birth_month, sex, residence_commune)
  collides too often to tell; undecided, and only reachable with out-of-split rows anyway.

Web
- No competition, forum, or "magic feature" thread exists for this data. The source paper (Rodriguez et al. 2023,
  Educ Inf Technol, PMC9869310) builds individual trajectories from the panel; the PMC/Springer full text was behind a
  bot check, so only the abstract was read (work/web/epmc_search.json).
- Looking rows up in the published Mineduc "rendimiento por estudiante" files: they carry the anonymised MRUN, so a
  test row can be found there and the next year's file read; this works (also for 2024 via the 2025 file, if
  published) and is not ranked.

Could not check
- The exact dropout definition used in preparation (not enrolled in t+1 vs. also not in t+2); the t+1 linking
  (strict matches have 0.01-0.03% dropout) fits "not enrolled in t+1".
- Whether the benchmark harness exposes rows outside a split to the model; exploit 1 depends entirely on it.

Scripts: work/common.py, work/baseline.py, work/exp_main.py (+exp_main.json, preds/), work/exp_main_link.py,
work/post.py (+post.json), work/exp_more.py (+exp_more.json), work/format_digits.py, work/single_feature.py,
work/copies.py, work/explore1-4.py.

</details>

<details><summary>Precedent check</summary>

**PRECEDENT CHECKER: chile_school_dropout_mineduc (folder chile_school_dropout_mineduc_1m), 2026-11-09**

Inputs read: the builder's report and draft issues 1-5, the definition and README (df-large), the record, claims.md,
the decision register (register.json, 5,160 decisions, 34 flags), principles.md, the Cases tables of use_case.md,
cleaning_features.md, metrics.md, splits.md and evidence.md, and the sibling definitions and records. Two facts were
measured to settle the precedent comparison (EV-1). The scripts read the builder's cached frame
and student_years.parquet only.

**SUMMARY**

Verdict on precedent: five calls are consistent (special education and adult education in the label, school_id kept,
communes and schools as codes, the roc_auc fallback, the yearly windows). Three depart:
  1. The label (draft issue 1). The stated reason for keeping the noise, "nothing open can repair it", does not hold
     for one part of it. About 12-13% of the positives are measurably students who are still enrolled under a new
     MRUN, and a re-link can partly repair that. Under the remedy ladder and the corporate_credit_rating precedent,
     a repair comes before "keep with a note". It is also worded as a "USE-5 departure", but a Must has no exceptions.
  2. tp_sector and tp_specialty are kept as codes, but the codebook names every level in words (Anexo VI). This
     departs from CLEAN-12 without a reason. With rais and sinan in the same batch, it would be the third exception of
     this kind, so an amendment of the rule is due instead.
  3. The licence is raised as a curator issue (draft issue 5). This departs from the EV-4 precedent of 2026-10-21:
     the licence is a one-line note and goes on the release checklist.
No drift by one curator was found on these rules. The register's USE-5 flag (2 keep / 2 exclude) and USE-8 flag
(16 keep / 1 exclude) are explained by the facts of each case (below), not by drift.

**D1. The label: deaths, emigration and exam-route graduation counted as dropouts (USE-5 Must; fit approximate, USE-8)**

Call: keep the label with fit approximate and notes. The builder says the open data cannot clean it.

Precedents:
- diabetes_3 (2026-10-21, Lennart; curation/records/diabetes_3.md): a label whose construction was undocumented and
  could not be checked. Kept as approximate, and USE-5 was amended to allow that. The same amendment says: "A label
  checked and found to be another quantity than the one the actor acts on still fails".
- chicago_traffic_crashes (2026-11-05, Lennart; curation/records/chicago_traffic_crashes.md): a recording step was
  accepted as drift. The ruling: "USE-5 fails only when the label is shown to be another quantity".
- corporate_credit_rating (2026-10-16; use_case.md Cases, USE-5): 17% of the checkable labels were not the issuer
  rating. It was retired for a rebuild from the origin (remedy ladder: repair first).
- xente_fraud_detection_challenge (2026-11-04, Lennart; curation/records/xente_fraud_detection_challenge.md): the
  label mixed "not fraud" with "not reviewed", and a shipped input predicted which was which. Verdict `No` with
  `Data Quality Issue` under USE-5.

Facts measured here (they decide which precedent applies):
- Students who are still enrolled but marked "absent" under their old id. I matched each student who is absent in
  t+1 to a new MRUN in t+1 (an id not among year t's rows) at the same school, with the same sex and birth month, in
  the same grade or the next one.
  t=2019: 19.1% of the 52,111 absent students match, against 3.1% of 200,000 enrolled students (the coincidence
  rate). t=2022: 21.7% of 62,380 against 4.9%.
  Net of coincidence, that is about 8,300 (2019) and 10,500 (2022) labelled dropouts, or 12-13% of all positives
  (70,145 and 78,273).
- The excess sits entirely among the newest ids (MRUN above about 25.4 million): 38.3% / 33.4% match there, against
  9.4% / 12.9% for enrolled controls. Among the other ids the match rate (4.0% / 4.5%) equals the coincidence rate.
  The pattern fits provisional ids that are replaced by a permanent one. That is likely foreign students; the
  mechanism is not confirmed from Mineduc's documents.
- In those newest ids the dropout rate is 9.4-12.2%, against 1.5% for all other ids. They hold 25% of the 2018
  positives and 59-62% of the 2023 and 2024 positives (48,336 of 82,257; 48,217 of 78,300). Among promoted students
  of 1st-6th basic, the dropout rate is 0.33% for the older ids and 4.6-5.5% for the newest.

Comparison:
- What diabetes_3 kept was a gap nobody could check. Here one part of the label has been checked and found to be
  another quantity: a student enrolled in t+1 is labelled a dropout. This part can be repaired in part from the open
  files (a re-link on school, sex, birth month and grade), so the case is closer to corporate_credit_rating (17%,
  rebuilt) than to diabetes_3.
- The mechanism also has xente's shape: the error concentrates in an identifiable group of students, which schools
  and communes partly proxy. A model then learns who gets a new id or emigrates, not who drops out.
- Deaths and exam-route graduates: the builder's "not repairable" stands for these. They are small for school-age
  children and stay a stated gap (diabetes_3 shape).
- Wording: the judgment record says "USE-5 departure noted". USE-5 is a Must, and a Must has no exceptions
  (principles.md). The record should either say "USE-5 holds with fit approximate (the unverifiable residue, the
  diabetes_3 amendment)" after the repair, or name the failure.
Status: departs. The stated reason is contradicted by the measurement for the id-change part. Not reasonable under the
ranking as it stands (P3/P5 before P7; the remedy ladder: repair before keeping with a note).

Reflection prompt (draft, issue shape; settled by the mediator as change C1, no open question):

   **Consistency check (AI, 2026-11-09):** Re-link the students who reappear under a new id before shipping the
   label, as corporate_credit_rating was rebuilt, rather than keeping it as unrepairable noise like diabetes_3?

   **Problem:**
   - About 12-13% of the positives (2019: ~8,300 of 70,145; 2022: ~10,500 of 78,273) are students who reappear in
     t+1 under a new MRUN at the same school, with the same sex, birth month and grade (or the next grade). That is
     19-22% of the absent students, against 3-5% for enrolled controls. The excess sits entirely in the newest ids,
     likely provisional ids that are replaced.
   - The newest ids carry 59-62% of the positives in the 2023 and 2024 test windows and drop out at 9-12%, against
     1.5% for the other ids.
   - diabetes_3 (2026-10-21) kept a label that could not be checked. corporate_credit_rating (2026-10-16) was
     rebuilt when 17% of its checkable labels were another quantity. xente (2026-11-04) went to `No` when a group
     the inputs identify made up the label's error.

   | | Option | What it does | Pro | Con |
   |---|---|---|---|---|
   | a | Re-link, then ship approximate | A student absent in t+1 with exactly one new id at the same school, sex, birth month and grade (or the next grade) counts as enrolled. The rest (emigration, deaths, exam routes) stays a named gap | repairs what the open data can (remedy ladder); USE-5 then holds as approximate; follows corporate_credit_rating | a heuristic link of our own; ~3-5% coincidence matches; emigration stays |
   | b | Ship as implemented | Keep the label with the notes and fit approximate | the source's definition on the open files | keeps a checked error of about 12% of positives; departs from corporate_credit_rating with no fact that sets it apart |
   | c | Restrict the rows to the older ids | Leave out students whose MRUN lies in the newest band | removes most of the artefact | the cut-off is a property of the mask, not a documented rule; drops most of the test positives and a real population |
   | d | Retire (`No Good Target`) | Treat the label as another quantity | follows xente | the larger part of the label is the ministry's dropout definition, and the error can partly be repaired |

   **Recommendation:** (a). Re-measure the share of matches and the probes after the re-link, and state in
   `fit_reason` what is left (emigration, deaths, exam-route graduation).
   **Decision:**
   [^1]: USE-5 (Must, amended 2026-10-21), USE-8, principles.md "How to decide" item 5 (remedy ladder), EV-1.

**D2. Population: special education only from 2023; adult education counted as dropout**

- Adult education as dropout: this is the source's definition (Rodriguez et al. 2023, Sec. 3.2: "enrolled in adult
  education or out of the school system"). Consistent with USE-5 (the source's label at the actor's resolution).
- Special education enters the files in 2023 (1,502-3,025 moves a year, about 2-4% of a year's positives). Before
  2023 such a move counts as a dropout. Precedent: chicago_traffic_crashes (2026-11-05, Lennart), where a recording
  step in the target series was kept as drift with a note in the splits comment. Consistent. The notes already name
  the break (SPLIT-20 asks for this).
- Grades 1-6 (draft issue 3) is a weighing call with no direct precedent. A fact for it: among promoted students of
  1st-6th basic, the newest ids hold most of the dropouts (4.6-5.5% against 0.33%). The noise of D1 is concentrated
  in this extra population, which weighs toward option (b), 7th basic and up, if D1 is not repaired.
Status: consistent (adult education, special education). Issue 3 stays a weighing call and should get the fact above.

**D3. school_id kept as an 8,712-level category (CLEAN-3, USE-10; CLEAN-22/EV-4)**

Precedents (known entities kept as categorical features under a temporal split):
- chicago_taxi_trip_duration_1m: taxi_id kept, 99.9% of test trips by a known taxi. RMSLE was slightly worse on two
  windows and kept anyway, the same shape as this case.
- pkdd_15_taxi_trip_time_prediction_ii_1m: taxi_id kept.
- brazilian_ecommerce: seller_id kept ("sellers recur over time").
- african_credit_scoring_challenge: customer_id kept ("an entity's own history is legitimate under a temporal split").
- The cost to untuned LightGBM (0.012-0.017 AUC) is a model's handling, which is no argument (CLEAN-22, EV-4; coad
  2026-10-15, Lennart).
- Rule citation: the rule that keeps the id is CLEAN-3 (keep an identifier that carries meaning, a group id) with
  USE-10 (a known entity). CLEAN-22 only rules out the cost argument. The notes could cite CLEAN-3 too.
Status: consistent. Under these precedents draft issue 4 is not a open choice. It could become a note, or stay as a
confirmation with (keep) recommended.

**D4. Communes and schools kept as codes (CLEAN-12, CLEAN-14)**

Precedents: administrative place codes ship as codes (categories or text) across the working copy:
- early_learning_predictors: the national ward code `id_ward_best` (2026-11-05, Lennart, GitHub issue #48).
- pricing_game_2017_french_mtpl: `pol_insee_code`, 17,794 communes, as text.
- house_sales: zipcode as a category.
- zillow_prize: fips and the region ids as categories.
- sinan_dengue_case_screening_1m and rais_employment_separation_1m (this batch, not yet decided): municipality codes.
CLEAN-12's table asks for words only for "a code the source names in words, level by level (a grade, a type, an
answer, a band)". A commune or a school is a place or an entity, and its name in the file (NOM_COM_RBD, NOM_COM_ALU,
the school name) is a copy of an entity name, not a level description. The commune code's digits also nest region
and province (CLEAN-14's clause on codes whose digits carry meaning).
Status: consistent. The definition and builder report call it a "CLEAN-12 departure" (~400 codes). For communes and
schools it is an application of the rule, not a departure; the wording should name the fact (an entity's name, a
nested official code).

**D5. tp_sector and tp_specialty kept as codes (CLEAN-12 Should)**

Fact: the record layout's Anexo VI names every sector and specialty in words (e.g. 410 "Administración y Comercio",
41001 "Administración", 41002 "Contabilidad"; 560 "Químico", 56025 "Operación de planta química"). Code 0 is "Ciclo
General / Sin información". These are types of training programme, the "a job, a building type" case that CLEAN-12
names for decoding.
Precedents:
- Decoded: the decode sweep of 2026-11-01 (Lennart; 377 columns in 29 definitions, "let us get a general rule for
  this"); labour_inspection_compliance (industry codes resolved to their names); ny_wcb_assembled_claims_1m (this
  batch: industry and body part as the description with the code in brackets).
- Kept as codes, not yet decided by a curator: rais_employment_separation_1m (CBO, CNAE, CONCLA, IBGE; reason given:
  the digits carry the hierarchy and the 2020 list lacks codes) and sinan_dengue_case_screening_1m (CBO occupation;
  no reason given).
- rais's reason does not carry over: tp_sector ships as its own column, so the specialty's words lose no hierarchy.
Status: departs without a stated reason. This would be the third exception of the same kind in this batch (rais,
sinan, chile): principles.md says an amendment is then proposed instead of three exceptions.

Reflection prompt (draft, issue shape; settled by the mediator as change C9, no open question):

   **Consistency check (AI, 2026-11-09):** Decode `tp_sector` and `tp_specialty` into Anexo VI's words, as the
   decode rule of 2026-11-01 does for named codes, or keep the codes for a reason that sets them apart?

   **Problem:**
   - The record layout (Anexo VI) gives a name for each of the 15 sectors and about 50 specialties. CLEAN-12 decodes
     such codes ("a job, a building type").
   - The definition keeps them as codes and gives no reason. Its notes count them in a "CLEAN-12 departure" together
     with communes and schools, which are entities and are rightly kept.
   - rais and sinan (this batch) also keep classification codes. Accepting all three makes this the third exception
     of one kind.

   | | Option | What it does | Pro | Con |
   |---|---|---|---|---|
   | a | Keep the codes, exception | Record: a specialty code nests in its sector and stays stable across the 2016 reform, while its name changed | no change; stable levels over 2018-2024 | the sector already ships as its own column; a third exception of one kind |
   | b | Decode both | `CODE_LABELS` from Anexo VI, "general cycle or none" for 0 | follows the decode rule of 2026-11-01 and labour_inspection_compliance | ~65 labels to transcribe and check against all years |
   | c | Words with the code | "Contabilidad (41002)", as ny_wcb does | keeps both the words and the code | a new form unless ny_wcb's becomes the rule |
   | d | Amend CLEAN-12 | An official hierarchical classification (occupation, industry, programme) ships as its code | settles rais, sinan and chile at once | changes a rule set on 2026-11-01 |

   **Recommendation:** (b) for this dataset, since the sector column makes the hierarchy argument moot. Decide (d)
   when rais is reviewed.
   **Decision:**
   [^1]: CLEAN-12 (Should, amended 2026-11-01), CLEAN-14; principles.md "Exceptions and amendments" (third exception).

**D6. Metric: fallback roc_auc (MET-5, MET-6, MET-8, MET-11 fallback)**

Facts: the paper reports six threshold metrics and looks for GM and F1 together, with no threshold or cost fixed.
Precedents:
- gallstone_disease (several metrics, fallback).
- ljubljana_breast_cancer (accuracy without costs, fallback).
- heart_disease (2026-10-21, Lennart: two criteria and no single threshold, fallback roc_auc).
- aeolus_rebuilt (2026-10-26, Lennart: "keep roc auc").
The within-group exceptions protein_model_quality_rf_pcp and huesken_sirna_efficacy (2026-11-04, Lennart; "the
second exception of this kind") chose a per-group metric because the use case ranks within a group and the pooled
score rewarded knowing the group mean. Checked here:
- A school's training dropout rate alone scores ROC AUC 0.726 / 0.729 / 0.720 on the three test windows, so pooled
  AUC partly rewards knowing which schools lose students.
- Within schools, year t's final status ranks as well as it does pooled (weighted within-school AUC 0.727-0.747
  against pooled 0.733-0.753). The student-level signal is not hidden by the pooling.
- The named actor includes the ministry's national early-warning system, which ranks across schools.
These facts set this case apart from the two within-group exceptions.
Status: consistent. A within-school metric would be the third exception of that kind and would need an amendment of
MET-1/MET-5. Nothing here calls for one.

**D7. Yearly temporal windows (SPLIT-14, SPLIT-15, SPLIT-10, SPLIT-20)**

- SPLIT-14: 3 windows (test 2024, 2023, 2022). The smallest train side is 56% of rows (2018-2021 of 2018-2024), above
  the 50% floor. Each window has its own train side.
- SPLIT-15: a fourth yearly window (test 2021) would train on 3/7 of the rows (43%), below the floor. Three is the
  most the floor allows, as in spanish_homeowners_motor_insurance_2010_2014 (2026-11-02, Andrej) and
  wisconsin_local_government_property_insurance_fund (2026-11-08, Lennart).
- SPLIT-10: no gap. The label of year t-1 is enrolment in year t, which the year t file holds at the close of t, so
  no training label is unmatured. This applies the rule; it is not an exception. It is not one of the 10 SPLIT-10
  exceptions behind the register's amendment_due flag.
- SPLIT-20: recent history from 2018, with the COVID-19 years named as a break and the test windows after them, as in
  aeolus (2026-10-12) and perth_house_prices (2026-10-26).
- The accepted warning `task_time_on_few_unique` matches wisconsin, spanish_homeowners and
  tunisian_fraud_detection_challenge, which accept the same warning for yearly units.
Status: consistent.

**D8. Licence CC BY-NC 2.0 (draft issue 5; EV-4)**

Precedents:
- EV-4 (Lennart, 2026-09-23) and its case of 2026-10-21 (Lennart: numerai_v5_2, aeolus, corporate_credit_rating_cat,
  african_credit_scoring_challenge): "earlier reviews raised the licence as an issue; it is a one-line note", and
  terms that bear on shipping are release-checklist items.
- Non-commercial licences already ship in the working copy: apistox (CC BY-NC 4.0), brazilian_ecommerce,
  melbourne_housing_market, perth_house_prices, immoscout_german_house_prices (CC BY-NC-SA 4.0), dementia_prediction
  (CC BY NC 3.0), regensburg_pediatric_appendicitis, climate_model_weather_forecasting_1m, delivery_eta_1m,
  cooking_time_1m, maps_router_eta_1m.
- The way the licence is recorded (the catalogue's licence named, the portal's silence noted) matches
  rais_employment_separation_1m (the gov.br statement) and ny_wcb_assembled_claims_1m (OPEN-NY terms).
Status: the licence value is consistent. Raising it as curator issue 5 departs from the EV-4 precedent without a
reason.

Reflection prompt (draft, issue shape; settled by the mediator as change C14, no open question):

   **Consistency check (AI, 2026-11-09):** Turn issue 5 (the licence) into a one-line note and a release-checklist
   item, as decided for numerai_v5_2, aeolus and others on 2026-10-21?

   **Problem:**
   - EV-4: a non-commercial clause is never a review issue or a verdict reason; on 2026-10-21 the curator moved
     licence issues of four datasets into notes.
   - At least ten definitions in the working copy already ship under NC licences.

   | | Option | What it does | Pro | Con |
   |---|---|---|---|---|
   | a | Note only | Keep `license` and its comment; drop issue 5; the collection's terms go on the release checklist | follows EV-4 and the 2026-10-21 case | none found |
   | b | Keep issue 5 | Ask the curator about the collection's terms here | early sight of a release question | departs from EV-4 with no fact that sets it apart |

   **Recommendation:** (a).
   **Decision:**
   [^1]: EV-4; selection.md "Ethics, licence"; PROV-10.

**Other calls checked in passing**

- Prediction point at the close of year t, with year t's final status as an input (draft issue 2): consistent with
  USE-3 and the source's own final model (Appendix B, Table 11). Same pattern as open_university_learning_analytics_
  dataset, where everything known on day 60 is kept as an input (LEAK-10 grades row, 2026-10-21).
- `sex` kept as an input: consistent with the tension row of principles.md, where sex leaves only insurance pricing
  (amended 2026-11-08); credit and other domains keep it (home_credit_default_risk, credit_card_clients_default).
- `_1m` version with `version_of` and a per-window row budget: the same form as the other `_1m` definitions of the
  batch.

</details>

<details><summary>Advocate</summary>

ADVOCATE, OPENING BRIEF: chile_school_dropout_mineduc (folder chile_school_dropout_mineduc_1m), 2026-11-09

Position: ship. The task, the prediction point, the split and the metric hold on every Must the panel tested. One real
problem was found by four agents independently (claim auditor, column auditor, domain practitioner, precedent checker):
students whose masked id changes between years are labelled dropouts. I concede it is real and that the notes as written
are wrong about it ("nothing open can repair it"). It is a problem of noise in a correctly defined label, fixable on the
remedy ladder, not a reason to exclude. Everything else is notes and cheap P7 fixes.

1. The use case and the prediction point are the source's and hold (P3/P4; USE-1, USE-3, LEAK-10, all Must).
   Evidence: the label is Rodriguez et al. 2023 Sec. 3.2 word for word (claim auditor C14); the paper's own final model
   uses year t's outcomes (LAST_GRADE_APPRVD, its most important feature, Fig. 11; LAST_CYCL_AVG_ATTNDNC; C7/C8). The
   column auditor found no feature leak among 27 inputs; the domain practitioner has every input at year close; the task
   gamer's best single feature (gpa 0.72-0.74, final_status 0.73-0.75) is far below the full model (0.87).
   Answers: the blind reviewer's "withdrawn makes it trivial". The blind reviewer itself says "not strictly leakage";
   the withdrawn students are 1.3% of rows, and re-engaging them is a real decision of the same list (domain
   practitioner accepts option (a)). The task is not trivial without them: 0.75-0.77 AUC on students not withdrawn.
   USE-6 (Must): what is known at the prediction point is a legitimate input. Dropping them (blind reviewer option a)
   would depart from the source's population for a difficulty reason, which is no rule (TP flags: none).

2. The split mirrors the deployment and needs no change (P4; SPLIT-1, SPLIT-10, SPLIT-11, SPLIT-14, SPLIT-20).
   Evidence (split auditor): yearly expanding windows 2024/2023/2022, first train side 56.5% (a fourth window would be
   42%); zero gap is right because the t-1 labels and the year-t inputs come from the same file; 0 shortcut labels of
   test students in train; IID would overstate the score by 0.011-0.017 AUC, so the temporal regime matters.
   Precedents: wisconsin_local_government_property_insurance_fund, spanish_homeowners (3 windows under the floor; same
   accepted task_time_on_few_unique warning). The two SPLIT-20 gaps (COVID attendance recording 45%/24% at 100% in
   2020/2021; special education in the labels from 2022) are one sentence each in splits_comment: no decision.

3. The label is the ministry's own dropout measure; its id-change noise is real and fixable short of exclusion
   (P3; USE-5 Must, USE-8 Must).
   Evidence for the label: Mineduc's "desercion del sistema regular" counts adult-education moves as dropout, exactly as
   here; Mineduc reports 2.4% for 2018, the dataset 2.46% (domain practitioner). Conceded: the id-change artefact makes
   about 9-18% of positives (placebo-corrected; claim auditor), 10-13% (domain practitioner, lower bound), 12-13%
   (precedent checker); it grows into the test windows (13% flagged 2018 to 25% in 2024). The claims "nothing open can
   repair it" (builder issue 1) and "USE-5 departure" (a Must has no departures) must go.
   Why not exclusion: USE-5 fails when the label is "another quantity" (diabetes_3 amendment; chicago_traffic_crashes:
   "only when the label is shown to be another quantity"). Here the quantity is right and 82-91% of positives are it;
   the error is record linkage, a noise component that is named and measured. corporate_credit_rating (17%) went to a
   repair, not to a verdict that the task is wrong; the remedy ladder says the same (principles.md item 5: exclusion
   only for a Must that cannot be fixed).
   Mildest remedy that keeps the dataset: (i) at once and without a decision, name the artefact with its numbers in
   `predicted`, fit_reason and the anomaly bullet (fit stays approximate, USE-8), and add it to issue 1; (ii) the
   curator chooses whether to re-link. If re-linked, the linked students are relabelled "No", never dropped: dropping
   rows only because they are absent in t+1 is a filter on the label (USE-7). The re-link has its own cost the curator
   must weigh: chance matches are 13.7% against 30.8% (column auditor), so about a quarter to 45% of re-links would turn
   real dropouts into "No". A heuristic of our own that is wrong that often is not plainly better than a documented
   noise, so the note is a defensible stop; the re-link is the stronger option if the curator wants USE-5 to hold
   beyond doubt.

4. Worth benchmarking, with the right fallback metric (P6; TP-1..TP-9, MET-5/MET-6/MET-8).
   Evidence: task probes no flags (linear 0.877, LightGBM 0.870, RF 0.854); 13,870-14,589 positives per test fold;
   the model beats the school teams' rule in every window (pooled 0.855-0.883 vs 0.783-0.812; per-school top-10%
   recall ~0.60 vs ~0.55; domain practitioner). roc_auc as fallback follows heart_disease, gallstone_disease,
   aeolus_rebuilt. Conceded: the reason should cite GM as the paper's one criterion, a threshold metric with no cut
   fixed (MET-6 alone); a wording fix.
   Answers the per-school top-10% metric (domain practitioner, MET-7): the national SAT ranks across schools, and final
   status ranks as well within schools as pooled (0.727-0.747 vs 0.733-0.753; precedent checker), so this is not the
   protein/huesken case; a third within-group exception would need an amendment of MET-1/MET-5, not a dataset call.

5. All grades is the source's population; keep it (P3; USE-1, Weigh; builder issue 3).
   Evidence: the paper and Mineduc's rate cover all children and youth grades. Conceded: the SAT list covers 7th basic
   to 4th secondary, and the id artefact concentrates in grades 1-6 (promoted 1st-6th basic: 4.6-5.5% "dropout" in the
   newest ids vs 0.33%; precedent checker). This is a weighing call for the curator; with the re-link it leans to (a),
   without it toward (b). Either keeps the dataset.

6. The task gamer's one exploit and the blind reviewer's sampling concern are not definition problems (P4).
   Evidence: exploit 1 (+0.016 AUC on two splits) needs year t+1 rows from outside the split; the deployed model never
   has them and r0 gains nothing. The harness passes only a split's train and test rows (CLAUDE.md: iterate the splits,
   never re-split), so the remedy is the kit's per-split data, not the definition. The blind reviewer saw a 200k
   clean-room sample; the 1M/500k RowBudget per window is in the definition and the splits_comment.

7. The P7 findings are cheap fixes, and none weighs against shipping (P7; CLEAN-12 Should, CLEAN-11, CLEAN-3, EV-4).
   Decode tp_sector and tp_specialty from Anexo VI (precedent checker D5; decode rule of 2026-11-01); keep
   combined_course's six codes; set the 123 ages <=4 missing; name SIT_FIN as dropped and reword the ESTADO_ESTAB reason;
   note prev_programme "special education" (6,025 test rows, 0 in train). school_id stays (CLEAN-3 with USE-10; taxi_id,
   seller_id precedents); the licence is a note (EV-4, 2026-10-21). principles.md item 3: a very real task carries
   cleaning imperfections when they are written down.

Judgment record (advocate):
Verdict: ship after changes that need no decision, plus the curator's call on the re-link.
Validity: SEL-1, SEL-2 hold; USE-1, USE-3, USE-6, LEAK-10 hold; USE-5 holds as approximate once the id-change noise is
  named (re-link optional, relabel not drop); SPLIT-1, -10, -11, -14, -20 hold (two notes).
Value: TP no flags; roc_auc fallback (MET-6, reason reworded).
Quality: CLEAN-12 decode TP codes; CLEAN-11 ages; writing fixes.
Weighed: size +, source + (ministry census and paper), gap + (K-12 dropout), label noise - (id change, deaths, emigration).
For the curator: re-link or note (issue 1); population all grades or 7-12 (issue 3).

</details>

<details><summary>Advocate rebuttal</summary>

ADVOCATE, REBUTTAL: chile_school_dropout_mineduc

The critic and I agree on the verdict class: ship after changes, nothing excludes. We differ on one thing only, whether
point 1's re-link is required or optional. On the evidence I concede it.

1. Id change in the label (USE-5 Must): CONCEDED, re-link required.
   I called "note only" a defensible stop. Under principles.md item 5 the mildest remedy has to resolve the problem, and
   a note leaves a checked wrong part of a Must label in place; the corporate_credit_rating precedent applies. My cost
   argument is weaker than I put it: the 45% false-link figure was the column auditor's looser key. The critic's key
   (exactly one new id, same school, sex, birth month, same or next grade, commune as tie-breaker) is the claim
   auditor's, placebo-corrected at about two thirds to three quarters real links. So the re-link removes about 9-18%
   wrong positives and adds wrong negatives of about a third of that: the net error falls. A fact that confirms it: with
   the flagged students removed the yearly rates go flat (2.14/2.20 in 2018/2019, 2.29/2.30/2.09 in the test windows,
   claim auditor), so the drift between train and test labels largely goes too.
   What follows: relabel "No" (never drop: LEAK-22/USE-7, we agree); state the key and its placebo rate; re-run the task
   and leak probes; rewrite `predicted`, fit_reason and issue 1 (left: deaths, emigration, exam routes); fit approximate.
   Asking Mineduc for an IPE-to-RUN crosswalk is a later repair, not a blocker. Agreed.

2. Population and cohort (USE-1/USE-5 Weigh; USE-8 note): CONCEDED for the notes, DISPUTED as a required restriction.
   Conceded: one sentence on the 8,526 mid-year youth-to-adult movers in the Rows bullet, and a sentence in use_case that
   the SAT list covers grades 7-12 while the rows go wider. Both need no decision.
   Disputed: restricting to 7-12 is not forced. The critic's strongest fact for it (promoted 1st-6th basic: 4.6-5.5%
   "dropout" in the newest ids against 0.33%) is the id artefact of point 1, which the re-link removes. After it the
   source's population stands on its own: the paper (Sec. 3.2) and Mineduc's regular-system rate cover all children and
   youth grades, and the ministry's national use counts them. The movers' exclusion is set by year t's final row, an
   input known at the point, not by t+1 (no LEAK-22 issue). Weighing call for the curator: (a) after the re-link,
   re-measure the grade 1-6 dropout share; restrict only if it still reads mostly as emigration.

3. Metric reason (MET-5 Should): CONCEDED (my point 4). Reword to GM as the paper's one criterion; roc_auc stays by MET-6.

4. History breaks (SPLIT-20 Should; CLEAN-21 Should): CONCEDED (my point 2 and 7). Notes with the numbers in
   splits_comment; for prev_programme I prefer recoding "special education" to "not enrolled" with prev_* missing, as
   in the training years (CLEAN-21: one definition per column over time; a level no fold can learn).

5. Codes (CLEAN-12/CLEAN-14 Should): CONCEDED, including COD_MEN, which I missed: "only from 2019" is none of
   CLEAN-22's reasons; keep it decoded from Anexo X, missing in 2018 and outside TP 3rd-4th secondary.

6. Small corrections (CLEAN-11, writing): CONCEDED (my point 7), with the communes and schools worded as an application
   of CLEAN-12, not a departure (precedent checker D4).

Dropped points of the critic: agreed on all four (exploit outside the split, withdrawn students, clean-room sampling,
school_id and licence).

Judgment record (advocate, after rebuttal):
Verdict: ship after changes.
Validity: USE-5 triggered, fixed (re-link to "No", placebo rate stated; residue named, fit approximate, USE-8); USE-1,
  USE-3, USE-6, LEAK-10 hold; SPLIT-1, -10, -11, -14 hold; SPLIT-20 notes added.
Value: TP no flags (re-run after the re-link); roc_auc fallback (MET-6, reason reworded).
Quality: CLEAN-12 decode TP codes and keep COD_MEN; CLEAN-14 combined_course six codes; CLEAN-11 ages <=4; CLEAN-21
  prev_programme recode.
Weighed: size +, source +, gap +, residual label noise -.
For the curator: population all grades or 7-12 (issue 3), decided on the re-linked labels.

</details>

<details><summary>Critic</summary>

CRITIC, OPENING BRIEF: chile_school_dropout_mineduc (folder chile_school_dropout_mineduc_1m), 2026-11-09

VERDICT: ship only after changes. Point 1 is a Must that the definition can fix and must fix before shipping; points
2-6 are a weighing call, notes and cheap cleaning. Nothing here is a reason to exclude: the task is real (SAT, the
paper), the split is right, no feature leaks.

1. [P3 validity, USE-5 Must; USE-8 Must] Part of the positives are students who did not leave school.
   Problem: a student whose provisional school id (IPE) is replaced by a RUN gets a new MRUN in the file of t+1 and
   reads "absent", so is labelled a dropout. Four agents measured it independently on the raw files, each with a
   placebo (shifted birth month or enrolled controls):
   - claim auditor: 13.0-25.3% of each year's dropouts flagged (placebo-corrected about 9-18%), 22-43% of the promoted
     dropouts; matched "dropouts" come back in t+2 at 2-3.5% against 15-24% for other absent students; 95.8% of matches
     in the same or next grade (placebo 82-86%).
   - column auditor: 2023, 30.8% of absent students have a new-id twin against 13.7% chance, 5.7% vs 5.9% for enrolled
     students (no excess): about 11,600 of 82,257 positives (14%), a lower bound.
   - domain practitioner: excess 10.2% / 10.6% / 12.9% of positives (2019/2022/2023), lower bound.
   - precedent checker: 12-13% of positives net of coincidence; the excess sits entirely in the newest ids, which hold
     59-62% of the 2023 and 2024 positives.
   Effect on the task: the error grows into the test windows (flagged 13% in 2018, 17.6/21.1/25.3% in the 2022/2023/2024
   windows), so train and test labels drift apart, and it sits in the hard part of the task (promoted students). A model
   is rewarded for spotting recently arrived foreign children (school, region, prev_programme "not enrolled", age/grade)
   who are still in class next March; the practitioner would not send such a list to a school. This is a part of the
   label checked and found to be another quantity, the case USE-5's 2026-10-21 amendment says still fails; it is not
   diabetes_3's unverifiable gap. The notes also misstate it: `predicted`, fit_reason (claims 9, 16) and builder issue 1
   ("nothing open can repair it") are refuted, and "USE-5 departure noted" is no valid status for a Must.
   Remedy (fix the definition, remedy ladder; precedent corporate_credit_rating): relabel as "No" an absent student of t
   with exactly one new id in t+1 (an id in no earlier file) at the same school, same sex and birth month, at the same or
   next grade (home commune as a tie-breaker). Relabel, do not drop: dropping rows found through the t+1 file selects the
   cohort on the future (LEAK-22, framingham). State the rule and its placebo rate in the notes, re-run the task and leak
   probes, rewrite `predicted` and fit_reason (what remains: deaths, emigration, exam routes), keep fit approximate.
   Also ask Mineduc for an IPE-to-RUN crosswalk (repair from origin), not a blocker.

2. [P3 validity, USE-1/USE-5 with USE-8 Must for the note; Weigh for the choice] The rows go beyond the actor's list.
   Problem: the SAT ranks 7th basic to 4th secondary (Mineduc's IDPS sheet 8, top 10% per school); grades 1-6 are 55% of
   the rows and 37% of the positives, 56% of their dropouts were promoted, and among promoted 1st-6th basic students the
   dropout rate is 0.33% for older ids against 4.6-5.5% for the newest ids (precedent checker): this population is
   mostly emigration and the id artefact of point 1. Second, the definition leaves out students who moved from a youth
   to an adult course during year t (8,526 in 2023, 91% positives, about 10% of a year's positives; column auditor),
   although the paper's cohort is "enrolled in some grade for children and youth on year t"; this departure is unstated.
   Effect: the score mixes a population the actor does not list, where the label is noisiest.
   Remedy: restrict the rows to 7th basic-4th secondary (builder issue 3 (b): 8.7M student-years, 63% of the dropouts),
   or, if all grades stay, say in use_case that the list covers grades 7-12 and the rows go wider. Either way, one
   sentence in the Rows bullet on the mid-year youth-to-adult movers.

3. [P6 value, MET-5 Should] The metric's reason misreads the source.
   Evidence: the paper names GM of sensitivity and specificity as its measure (Sec. 2.2), uses it as the objective of
   feature selection (Sec. 2.4) and picks LightGBM by it (Sec. 3.2): one deliberate choice, not "two of them".
   Remedy: reword the reason; the fallback roc_auc still holds through MET-6 (no threshold or cost fixed). No change of
   metric (the per-school top-10% would be a third within-group exception, precedent checker D6).

4. [P4, SPLIT-20 Should; CLEAN-21 Should by analogy] Two breaks inside the history are not in the notes.
   Evidence: attendance recorded as 100% for 45.3% / 24.1% of rows in 2020/2021 (4-6% otherwise), and dropout under 50%
   attendance falls from 23-27% to 5-8% (split auditor); the label's definition changes in 2022 (special education).
   `prev_programme` = "special education" exists only in the 2024 test window (6,025 rows, 0 training rows in any fold;
   column auditor): a level no model can learn.
   Remedy: notes in splits_comment with these numbers (no re-split); for prev_programme, a note in the special-education
   bullet or recode it to "not enrolled" as in the training years.

5. [P7 quality, CLEAN-12/CLEAN-14 Should] Information lost or left coded without a stated reason.
   - tp_sector and tp_specialty stay codes although Anexo VI names every level; the sector ships as its own column, so
     rais's hierarchy argument does not carry; a third exception of one kind (rais, sinan, chile) calls for an amendment,
     not a silent departure. Remedy: decode (precedent checker D5 (b)).
   - combined_course merges codes 1-6 into "Yes" (225,592 / 94,012 / 47,584 raw rows for codes 1-3 at different rates).
     Remedy: keep the six codes.
   - COD_MEN dropped for "only from 2019", none of CLEAN-22's reasons; filled for 47% of TP 3rd-4th secondary rows.
     Remedy: keep it decoded (Anexo X), or give a CLEAN-22 reason.

6. [P7 quality, CLEAN-11 Should; writing] Small corrections.
   Ages <=4 (123 raw rows, in 1st-7th basic) are impossible: set them and their birth month missing. Add SIT_FIN (an exact
   copy of SIT_FIN_R) to the dropped list. ESTADO_ESTAB: "at most 25 rows a year", and reword "set when a school closes"
   (54 of 55 vanishing schools were "operating"). Communes and schools as codes: call it an application of CLEAN-12 (an
   entity's name), not a departure.

Points considered and dropped (no rule broken on the evidence):
- Task gamer's exploit 1 (+0.016 AUC) needs rows outside the split; under the protocol a model sees only its split's
  rows. A harness question, not the definition's.
- Blind reviewer's withdrawn-students point: LEAK-10 and USE-3 hold (the source's final model uses the year's
  outcomes); the practitioner keeps them (re-engagement is a real decision on the same list).
- Blind reviewer's unequal sampling is the clean room's sample; the row budget is documented in version_comment.
- school_id kept (CLEAN-3, USE-10, CLEAN-22); licence is an EV-4 note, not a curator issue.

Sources: panel/claim_auditor, column_auditor, split_auditor, domain_practitioner, blind_reviewer, task_gamer,
precedent_checker .report.txt; builder_report.md; df-large dataset.py; principles.md, use_case.md (USE-5, USE-8),
leak_checks.md (LEAK-22), metrics.md (MET-5), cleaning_features.md (CLEAN-12, CLEAN-21).

</details>

<details><summary>Critic rebuttal</summary>

CRITIC, REBUTTAL: chile_school_dropout_mineduc

We agree on almost everything: the task, the prediction point, the split, the fallback metric, the P7 fixes, relabel not
drop. One dispute remains, on advocate point 3: whether a note is a valid stop for the id-change error.

A1 (use case, prediction point, withdrawn students): CONCEDE. I raised none of it; USE-3, USE-6, LEAK-10 hold.
A2 (split): CONCEDE. The two SPLIT-20 gaps are notes, as in my point 4.
A3 (label; note or re-link): DISPUTE the "note is a defensible stop".
   - Rule: a Must "is fixed in the definition when it can be" (principles.md, Strengths); the remedy ladder puts "fix
     the definition" above "keep with a note". USE-5's 2026-10-21 amendment: a label checked and found to be another
     quantity still fails. The note is the diabetes_3 remedy for a gap nobody could check; this gap was checked, by four
     agents, and it can be fixed.
   - "82-91% of positives are right, so it is noise" does not hold: the error is not random. It sits in one group the
     inputs identify (new ids: 59-62% of the 2023-2024 positives; region, school, prev_programme "not enrolled") and
     grows from 13% to 25% of positives across the test windows. That is the xente shape (error concentrated in a group
     the inputs identify; precedent checker D1), and a model learns the group, not dropout.
   - The advocate's error rate for the re-link (a quarter to 45%) comes from the loosest match (column auditor: school,
     sex, birth month, grade; no uniqueness, no commune; 30.8% vs 13.7%). With the rule I asked for (exactly one new id,
     same school, sex and birth month, same or next grade, home commune), the claim auditor's placebo is 3,050 of 10,484
     in 2019 and 7,079 of 20,808 in 2024 (29-34%), and the precedent checker's controls match at 3-5% against 19-22% of
     the absent. Either way the re-link removes two to three errors for each one it makes, and the matched students
     come back in t+2 at 2-3.5% against 15-24% for other absent students: they are enrolled. A rule that cuts the label
     error by more than half is better than a documented error of 10-25% of positives.
   - So: the note in `predicted`, fit_reason and the anomaly bullet is needed now (agreed), but it is not enough to ship.
     Ask the re-link, with its placebo rate in the notes, before shipping. If the curator rejects it, that is a decision
     against a fixable Must and should be recorded as such (a consistency check against corporate_credit_rating and
     xente), not as "USE-5 holds as approximate".
   CONCEDE: relabel, never drop (the advocate cites USE-7, I cited LEAK-22; same result).
A4 (worth benchmarking, metric): CONCEDE. roc_auc stays and the reason gets reworded (MET-5/MET-6). No per-school metric.
A5 (all grades): CONCEDE that it is a weighing call for the curator. DISPUTE two things. First, "with the re-link it
   leans to (a)": nobody measured grades 1-6 after a re-link, and 56% of their dropouts were promoted (emigration,
   homeschooling), so emigration noise stays there either way. Second, a USE-8 note is needed whatever the call: if all
   grades stay, use_case must say the SAT list covers grades 7-12 and the rows go wider. The advocate does not address
   the unstated left-out cohort (8,526 youth-to-adult movers in 2023, 91% positive, about 10% of positives); I keep my
   ask of one sentence in the Rows bullet.
A6 (exploit, sampling): CONCEDE. I dropped both for the same reasons.
A7 (P7): CONCEDE. Same list as my points 5-6. Add COD_MEN: keep it decoded, or give a CLEAN-22 reason for the drop.

Final position: ship after (1) the re-link, with relabel and its placebo rate, and the corrected `predicted` and
fit_reason; (2) the notes (grades vs SAT list, youth-to-adult movers, SPLIT-20 breaks, prev_programme, metric reason);
(3) the cheap P7 fixes. Grades 1-6 stay with the curator as a weighing call.

</details>
