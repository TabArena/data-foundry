# open_university_learning_analytics_dataset

**Outcome:** added. The source's four final results (Distinction, Pass, Fail, Withdrawn) of each registration active
on day 60 of its module presentation, from what is known by then; log loss, grouped by module presentation (22
groups). The AI recommends shipping it, with the concerns below.

**Main points:** Grouped by module presentation, not temporal; predictions on day 60.

**Record fields that disagree with the definition:**

- `tag`: record `Non-IID (Temporal)`, definition `Grouped (NON-IID)`.

**Record judgment:** valid with concerns. The source publishes no single task, so the prediction point, the target
framing and the split are our choices (issues 1-4). One presentation, BBB 2014J, changed how it marks (issue 9).

**Issues for Lennart:**

1. **Split regime: grouped by module-presentation, not temporal.**
   - Why it matters: deployment trains on earlier presentations. The OULAD page: "the J presentation must be used to
     inform the B presentation or vice versa". The data has only 4 start dates. The share of rows before
     2014J / 2014B / 2013J is 66.5% / 43.1% / 14.9%, so only one window keeps half of the data for training, and the
     protocol needs 3.
   - Label availability adds to this. A February presentation cannot train on the October one before it, which is
     still running (J runs to June/July), so the 2014B and 2013J windows could only train on 2013B (3 modules).
   - Numbers: IID 0.193, grouped 0.141, temporal 2014J hold-out 0.099. The grouped split is slightly optimistic for the
     older presentations: on 2013J and 2014B test rows, removing the later presentations from the train side costs
     0.010 skill more than removing as many random train rows (9 of 13 cases). On the 2014J rows it
     is harder than the hold-out (0.070).
   - Implemented: grouped.
   - Alternative: temporal by start date, `TemporalSplits(window=1, unit="months", cutoffs=("2013-10-01",
     "2014-02-01", "2014-10-01"), gap=5)` on a start-date column. Two of its three windows train on 14.9% of the rows,
     which breaks the 50% rule.

2. **Prediction day.**
   - Implemented: day 60.
   - Alternatives (one grouped repeat, LightGBM, rows / 4-class skill / at-risk AUC):
     - day 0: 29,681 / 0.031 / 0.690
     - day 30: 27,510 / 0.068 / 0.752
     - day 60: 26,395 / 0.132 / 0.803
     - day 90: 25,588 / 0.202 / 0.844
   - OU Analyse itself predicts weekly whether the next assignment will be failed. That task needs one row per student
     and assignment, and it would allow a real temporal split with calendar windows.

3. **Target framing.**
   - Implemented: the source's 4 classes (log_loss).
   - Alternative: binary at risk (Fail or Withdrawn against Pass or Distinction; 41.7% positive). On the same folds it
     gives AUC 0.805 and log-loss skill 0.207, against an at-risk AUC of 0.803 from the 4-class model.

4. **TMA marking delay.**
   - Implemented: a TMA score is used only 14 days after the later of cut-off and submission. This follows the OU
     Tutor Support Statement (approved April 2012, updated July 2019): feedback "normally within ten working days of
     assignment deadlines, or ten working days after the date of any agreed extension, whichever is the later". The
     data does not say when a 2013-2014 TMA was returned. CMA scores count from submission ("iCMAs are marked
     automatically"); waiting for the cut-off changes LightGBM skill by 0.0003 +- 0.0025.
   - Alternative: no delay. Skill 0.158 instead of 0.132 (one grouped repeat).

5. **Students recur across the split** (a potential leak, kept).
   - 3,619 rows belong to students registered in several periods and 1,148 to students on two modules in one period.
     12.9% of grouped test rows have the same student, with the same profile, on the train side.
   - For 7.9% of all rows that is a concurrent or later registration, which deployment would not know (for 1,312 of
     3,387 overlap rows it is only earlier registrations, which deployment would know).
   - Effect: about 0.0025 log loss over all test rows (control experiment).
   - No grouping removes it, because all 22 presentations are linked by shared students.
   - Alternative: keep one registration per student, which drops 2,384 rows and changes the cohort.

6. **Record pointers to fix** (I did not edit the record).
   - `source_links` could add the figshare DOI, since the OU download is dead.

7. **Accepted warning `groups_test_groups_few`.** It is accepted with the group-probe evidence; please confirm.
   - This is the only dataset in the copy that accepts it: 22 groups, 6-9 per test fold. The next fewest is
     electric_motor, with 69 groups and 23 per fold.
   - The verifier supports the grouped split: new rows always come from a presentation nobody has finished, and no
     shipped split holds out a whole module, so covertype's IID precedent (3 areas) does not carry over.
   - Its cost is fold variance, concentrated in BBB 2014J (issue 9).

8. **Minor metadata choices.**
   - `year = "2015"`: the first release. The data covers 2013-2014 and the paper is from 2017.
   - `source = "Other"`: the OU website.
   - `source_url`: the OU's page (research.stem.open.ac.uk/ouanalyse/open-dataset-more), not the UCI DOI the record
     lists first.
   - `data_tags = ("Spatial",)`: for `region` and `imd_band`.

9. **BBB 2014J changed how it marks.** Harmonise its marks or keep them?
   - Evidence: its first TMA (cut-off day 19, weight 0) is marked 1 or 100: 1,739 of its 1,772 scores. In the other
     BBB presentations that TMA has weight 5 and is graded, and 52-71% of the students marked 40 or less there fail.
     In BBB 2014J, 732 students are marked 40 or less, and 52% of them pass, 10% with distinction. On day 60 it is the
     presentation's only known score.
   - Its VLE was rebuilt too: clicks_oucontent averages 93 against 0.4-7, and clicks_forumng 42 against 145-237.
   - Effect: LightGBM scores below the class prior on it (skill -0.42; random forest -0.07). The three weakest splits
     (0.06-0.09 against 0.16-0.19) are the three that test it.
   - Implemented: the marks kept as recorded, with an Anomaly bullet. A deployed model meets such redesigns.
   - Alternative: leave weight-0 TMA marks out of score_mean and score_min. This changes 1,655 cohort rows (1,652 of
     them BBB 2014J). On the 9 shipped splits:
     - LightGBM 0.141 -> 0.167 (standard deviation over the splits 0.052 -> 0.016; BBB 2014J -0.42 -> 0.02);
     - random forest 0.168 -> 0.158 (BBB 2014J -0.07 -> -0.24).

10. **Group context.** Set to `all_rows`, as for force_2020: on day 60 every registration of the running presentation
    is known with its day-60 features. It lets a model compare a student with the cohort, which is where BBB 2014J's
    rebuilt VLE hurts. The alternative is `none` (each row on its own).
