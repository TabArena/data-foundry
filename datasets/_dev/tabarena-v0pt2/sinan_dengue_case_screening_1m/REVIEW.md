# sinan_dengue_case_screening

**Outcome:** added as `sinan_dengue_case_screening_1m`. The AI recommends shipping it. The panel's changes are made
and need no mark: the 370,314 notifications (14.1%) made after a dengue sample was taken are dropped (by the sample
dates, not the label); the use case now names the municipal surveillance team that closes the untested notifications
and chooses whom to test, not the physician, whose care the 2016 protocol does not tie to the result; and training
stops one month before each test window instead of two. Four calls are left to you: the test windows (a weighing call),
the duplicate notifications of one patient (an exception to confirm), optional epidemic-activity inputs, and the
occupation codes (decoding recommended). The task is Brazil's
national notifications of suspected dengue (SINAN, the Ministry of Health's open files of 2016-2021, the only years
that hold discarded cases): at notification, before the dengue test's result, will the laboratory confirm the case as
dengue? 2.25 million notifications that a laboratory decided, 45% dengue, with the form's 14 signs, 7 diseases, the
patient and the place; three half-year test windows from July 2020 to December 2021 with a one-month gap; fallback
`roc_auc`.
Verdict: ship after changes (made).
Validity: SEL-1 (no ethical concern) and SEL-2 (a real use) hold. USE-1 triggered and fixed: the actor is now the municipal surveillance team that closes
the untested notifications and chooses whom to test, with the physician's differential diagnosis as a second reading
(USE-9 asked: no use case fits directly). USE-3 triggered and fixed: the 370,314 rows (14.1%) notified after a dengue
sample was taken are dropped by the sample dates, a filter that reads no label. USE-8 holds as approximate with the
`Selection Bias` marker and the cohort's numbers in the notes. LEAK-10 holds for every kept column (leukopenia
timing-tested). SPLIT-1 (temporal regime), SPLIT-9 (no shortcut through training labels), SPLIT-13 (units recur as known
entities) and SPLIT-14 (every train side over half the rows) hold; SPLIT-10: the gap shortened from two months to one; SPLIT-20's
COVID-19 note written. PROV-9 fixed (2023).
Value: TP-1 to TP-5 pass (random forest ROC AUC 0.708 against the dummy's 0.5 on 3 of 3 windows; TP-3's `no_spread`
flag (the best and worst model families within twice the standard error) read as the noise of three unlike windows, to
re-check with tuned runs); MET-8's fallback holds, MET-11's reason corrected; log loss, the domain practitioner's
choice, set aside because the dengue share swings 12% to 56% by quarter, so it would mostly score that shift.
Quality: CLEAN-10 fixed (the occupation table's unknown codes missing, SINAN's own codes decoded); CLEAN-12's full
decoding of the CBO codes open (issue 4); the copies of one patient kept as an exception to LEAK-19 for you to confirm
(issue 2; no copy crosses the split).
Weighed: size +, national open source with a dictionary +, honest difficulty (within one unit and month ROC AUC
0.59-0.62, before the filter) +, test windows only in the COVID-19 years -, the tested-only cohort -, files replaced weekly
(reproducibility) -.
For the curator: issue 1 (which half-years to test), issue 2 (the one-patient copies, an exception to confirm), issue 3
(optional epidemic-activity inputs), issue 4 (the occupation codes, alike for rais and wioa).

**Main points:** Keep the three newest half-years with the season note (issue 1, implemented, recommended); keep the
duplicate notifications of one patient as an exception (issue 2, implemented, recommended); leave out counts of recent
notifications (issue 3, implemented, recommended); decode the occupation into "words [code]" from SINAN's own table,
alike for rais_employment_separation and wioa_employment_after_exit (issue 4: codes implemented, decoding
recommended).

**Record judgment:** valid. The record's fields agree with the definition. Three screening statements no longer hold
and the notes say why: the accept reason "most rows" (only 2016-2021 can be labelled, 2.25 million rows, not the 6.5
million of 2024), the physician's decision as the use case (the 2016 protocol manages every suspected case by its risk
group; the actor is now the surveillance team), and "fit direct" (approximate, with the `Selection Bias` marker now
set on the record). Bohm et al.'s ROC AUC of 0.985 cannot be reproduced with their ten variables on these rows (logistic
regression 0.578 on their own cohort and sampling), so it is no reference level for this task.

**Issues for Lennart:**

1. **Test the three newest half-years, as now, or two dengue seasons and one off-season?**

   * **Problem:**
     - Two of the three windows are the July-December off-season, which holds 16% to 33% of a year's notifications, so they hold 36% of the test rows but two thirds of the weight in the mean over windows.
     - The off-season windows score higher (random forest 0.76 and 0.73 against 0.63 in season), so the reported mean sits above the row-weighted mean (0.708 against 0.674).
     - Moving the oldest window to January-June 2020 gives two season windows, but the windows are then no longer contiguous and about half of that window's rows come before COVID-19 reached Brazil.
   * **Effect on the task:** the level of the reported score and how much each season weighs in it; the order of the model families measured so far is the same in every window (LightGBM over logistic regression by 0.058 to 0.084).
   * **Experiments:** window sizes after the pre-notification filter with the one-month gap (mediator's count), scores per window measured by the split auditor before the filter with the two-month gap:

     | Window | Test rows | Dengue | Train share | LightGBM | Logistic |
     |---|---|---|---|---|---|
     | July-December 2021 | 108,465 | 31.5% | 93.4% | 0.751 | 0.670 |
     | January-June 2021 | 344,905 | 49.7% | 79.2% | 0.651 | 0.593 |
     | July-December 2020 (implemented) | 88,134 | 23.3% | 74.4% | 0.741 | 0.656 |
     | January-June 2020 (option B) | 430,995 | 54.8% | 56.0% | 0.689 | 0.626 |

     - Both sets keep every train side above half the rows and the smallest class at 20,501 rows or more; the 2020 season window fits whole under the 500k test cap.
     - Twelve-month windows stepping by six months were measured too (LightGBM 0.671, 0.672, 0.692); they test two half-years twice and score a whole year's base-rate swing, so no one proposes them.
   * **Consistency:**
     - Contiguous windows rolled back from the newest that cover both seasons are the form you chose for rain_in_australia and airqo_low_cost_air_quality_monitor_calibration_challenge; the precedent checker found the off-season windows no departure, since half of every dengue year is off-season[^s15].
     - airqo added windows for season coverage and perth_house_prices placed its windows around the COVID-19 months, both decided on coverage and periods, not scores[^s20][^s21].
   * **Panel:**
     - Keep (advocate; the critic accepts it as the mildest remedy; the domain practitioner calls half-years before and after the season a sensible refit cadence): the rules lean to contiguous windows rolled back from the newest, and both seasons are covered.
     - Move (split auditor): the season that holds most cases should hold most of the weight, a choice that keeps every train side above half the rows; the advocate and the critic agree that it may rest only on coverage, not on the score levels.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Three newest half-years, with the season note (implemented) | windows July-December 2020, January-June 2021, July-December 2021; the splits note names the weighting and the score levels | contiguous and rolled back from the newest; both seasons covered; the form of rain_in_australia and airqo; all windows in one period | the off-season weighs two thirds while it holds a quarter of the cases; all three windows in the COVID-19 years |
     | B | Cutoffs January 2020, January 2021, July 2021 | windows January-June 2020, January-June 2021, July-December 2021 | the season, with 67% to 84% of a year's cases, gets two of three weights; one window partly before COVID-19 | windows not contiguous; the 2020 season window mixes pre-COVID and COVID months; its train side 56.0% |

   * **Recommendation:** A, with the season weighting written in the splits note: the rules lean to contiguous windows rolled back from the newest, and both seasons are covered; B if you want the season to carry most of the weight. **Decision:** A or B?

   **Notes for the AI:** B: `TemporalSplits(window=6, unit="months", cutoffs=("2020-01-01", "2021-01-01", "2021-07-01"), gap=1)` (check the order the API expects and that the 2020 season window keeps its 430,995 rows); rewrite `task_summary.split`, the window sentences and the season paragraph of `splits_comment` (sizes, dengue shares, train shares 93.4%, 79.2%, 56.0%) and `version_comment` (train sides 1.26M to 2.11M); re-run `dataset check`, the task and leak probes and the hidden-group probe.

   [^s15]: **SPLIT-15** (Should): roll the windows back from the newest data, as many windows as an IID or grouped task of that size would get folds. **SPLIT-14** (Must): at least 3 windows, and no window's train side holds less than 50% of the data. rain_in_australia (Lennart, 2026-10-26) and airqo_low_cost_air_quality_monitor_calibration_challenge (Lennart, 2026-11-05: windows "chosen from season and site coverage, not scores").
   [^s20]: **SPLIT-20** (Should): check the history for breaks (COVID-19, a change of rules or of the data collection); check whether the newest windows fall in an atypical season and widen them so most do not.
   [^s21]: **SPLIT-21** (Must): decide neither the training history nor the windows from a comparison over a few test windows.

2. **Keep the duplicate notifications of one patient, recorded as an exception, or drop the second copy?**

   * **Problem:**
     - 552 groups of exact copies share the birth date as well as the notification date, unit, places, age and every finding, so each is one patient notified twice, not two patients with one profile.
     - Your rule drops copies of one entity and keeps distinct entities the inputs cannot tell apart; the definition keeps these copies, which needs your exception[^l19].
     - None crosses the split, since the notification date is an input, and the 2020-2021 files give only the birth year, so such copies cannot be found in the test years.
   * **Effect on the task:** a few hundred training rows of 2016-2019 count one patient twice; no test row has a copy in training, so no score changes.
   * **Consistency:** the copies of distinct patients stay, as in ai4d_lab_tanzania_tourism_classification_challenge and bank_marketing; copies of one entity were dropped in qsar_oral_toxicity, qsar_tid_11 and audiology_diagnosis[^l19prec].
   * **Panel:** the precedent checker found the keep a departure without a stated reason and proposed the exception; the advocate, the critic and the mediator agree.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep, recorded as an exception (implemented) | the notes' line becomes final; the record gets an exception line | no copy reaches a test row; one treatment for all years | a keep of one-entity copies to track |
     | B | Drop the second copy of the 552 same-birth-date groups | at least 552 rows of 2016-2019 leave | follows the rule where the copies can be found | the test years keep theirs; changes no score |

   * **Recommendation:** A: the copies cannot reach a test row, and the test years could not be treated alike. **Decision:** A or B?

   **Notes for the AI:** A: replace "(proposed by the review panel, 2026-11-09, for the curator to confirm)" in the copies bullet of `curation_comments` with the curator's date; add `**Exception to LEAK-19 (<date>, Lennart):**` to the record and an `exception` row to the Cases table of `leak_checks.md`. B: in `_clean`, before `drop_columns`, drop rows duplicated over every input plus a filled `DT_NASC`; update the bullet's counts (4,541 rows, 2,237 groups); re-run `dataset check` and leak probe 5.

   [^l19]: **LEAK-19** (Should): exact copies with the same label go, distinct entities the features cannot tell apart stay; **LEAK-18** (Should): plausible repeats with few features stay.
   [^l19prec]: qsar_oral_toxicity, qsar_tid_11, audiology_diagnosis (Lennart, 2026-10-21); ai4d_lab_tanzania_tourism_classification_challenge (2026-11-05) and bank_marketing (2026-11-08), Lennart.

3. **Leave out counts of recent notifications per municipality, as now, or add the 7- and 28-day counts of all dengue notifications as inputs?**

   * **Problem:**
     - The surveillance team knows how many suspected cases its municipality notified in the last weeks, the input it uses most for closing cases in an epidemic, and the release has no such column[^u6].
     - The shipped rows hold only the laboratory-decided notifications (about 1 in 2.8 notified cases in 2017), so counts a participant builds from them count only cases later closed by a laboratory.
     - Counts over all notifications, strictly before the notification day, would have to be built from the full yearly files, a feature the source does not hold.
   * **Effect on the task:** the honest past counts built from the cohort add about 0.009 ROC AUC (task gamer, LightGBM); what counts over all notifications add is unmeasured.
   * **Consistency:** no definition builds an activity count beyond the source's own columns or feature script; the place and the notification date already carry each place's level and the calendar.
   * **Panel:** raised by the domain practitioner only; neither the advocate nor the critic argued it; the mediator recommends leaving it out.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Leave out (implemented) | the inputs stay the form's fields | the source's own columns; no constructed feature; methods may build their own counts from the cohort | the team's most used input is missing; a model learns each place's level, not the phase of the season |
     | B | Add 7- and 28-day counts of all notifications per municipality | two counts per row, from every notification of the yearly files, strictly before the notification day | the input the actor has; label-free | a feature the curation builds, beyond the source's columns; a second prepared file from the full 8.1 million rows; its gain unmeasured |

   * **Recommendation:** A: the counts are a constructed feature beyond what the source records, and methods can build counts from the shipped rows, which count only the cases later closed by a laboratory. **Decision:** A or B?

   **Notes for the AI:** B: in `_prepare_raw_files`, count every notification of DENGBR16-21 (all criteria, also open and inconclusive rows) per notification municipality and day into a second prepared file; in `_clean`, add `municipality_notifications_7d` and `_28d` as the sums over the 7 and 28 days before the notification date (the day itself excluded); a note; re-run `dataset check`, the leak probes (the count against the label by window) and the task probes.

   [^u6]: **USE-6** (Must): anything known at the prediction point is a legitimate input.

4. **Ship the occupation as its CBO code, as now, or as "words [code]" from SINAN's own occupation table, decided alike for rais_employment_separation and wioa_employment_after_exit?**

   * **Problem:**
     - The occupation ships as CBO 2002 codes (the Brazilian Classification of Occupations; about 2,240 code levels on the shipped rows), where your rule decodes a job code into its words; only SINAN's own codes outside the CBO (student, homemaker, retired or pensioner, unemployed, prisoner: 17.9% of the rows) carry words now, and the table's codes for unknown are missing[^c12].
     - The dengue dictionary gives no words, but SINAN's occupation table, which DATASUS distributes with the SINAN files (the TabWin file `OCUPANET.cnv`), names 2,295 of the 2,301 levels the rows held before the pre-notification filter, 99.8% of the coded rows.
     - rais_employment_separation keeps the same CBO list as codes (its issue 5 recommends decoding, alike for this dataset) and wioa_employment_after_exit its occupation and industry codes, so a third exception of one reason would make an amendment of the rule due[^amend].
   * **Effect on the task:** a model that reads categories sees the same partition either way; a model that reads text gets the occupation's title; with "words [code]" the code stays in the value.
   * **Experiments:**
     - Coverage of `OCUPANET.cnv` (2,671 codes, last changed 2021-03-22) on the rows before the pre-notification filter: 966,659 rows with an occupation, 99.81% of them in the table; outside it only 10001 (1,584 rows; 1,280 after the filter), 999990 (285; 241 after the filter) and four five-digit codes (6 rows).
     - The table titles are in Portuguese (most in capitals, "RECEPCIONISTA DE HOTEL"); the five SINAN codes now shipped carry our English translations of the table's titles.
   * **Consistency:** labour_inspection_compliance decodes its industry codes from an external official table shipped in its folder, ny_wcb_assembled_claims_1m ships NAICS as "words [code]", and on credit_g you asked for "the right labels in all cases"; here the table is the source's own, so no external version has to be matched[^c12prec].
     - rais_employment_separation's issue 5 recommends decoding this dataset's municipality codes as well; here the precedent checker reads place and unit codes as entity codes that stay codes (as early_learning_predictors and pricing_game_2017_french_mtpl), so B decodes only the occupation unless you say otherwise.
   * **Panel:**
     - Decode (precedent checker): the rule names a job among the codes to decode, and decoding is what exposed 998999 as "ignored".
     - Quality call to decide with rais and wioa (advocate and critic); the column auditor accepted codes with a note, since a model sees the same partition, which the precedent checker answers is a model argument the rule does not take.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | CBO codes, SINAN's own codes decoded (implemented) | the CBO levels stay codes; student, homemaker, retired, unemployed and prisoner carry words; unknown codes missing | no lookup file; the unknown codes are already handled | departs from the rule while the source's own table has the words; a third exception of one reason with rais and wioa |
     | B | Decode every level into "words [code]" from `OCUPANET.cnv` | a pinned lookup file of 2,671 code-title pairs in the folder; the levels in no table stay "[code]" | follows the rule and the ny_wcb form; the table is SINAN's own, covering 99.8% of the rows; the code stays in the value | a lookup file to pin and check; titles in Portuguese, or a translation of 2,300 titles; rais would decode from the ministry's CBO list, a different file of the same classification |
     | C | Amend the rule for large national classifications whose words are only in a separate table | codes stay here, in rais and wioa; the rule names the case | one decision for the batch; no lookup files | the rule names "a job" among the codes to decode; for this dataset the words come from the source's own distribution |

   * **Recommendation:** B, with the table's Portuguese titles for every level, the five SINAN codes included, so the column has one language; the same decision for rais_employment_separation and wioa_employment_after_exit. **Decision:** A, B or C?

   **Notes for the AI:** B: fetch `TAB_SINANNET.zip` from `ftp://ftp.datasus.gov.br/dissemin/publicos/SINAN/AUXILIAR/` (SHA-256 24ac0c62fb84e545..., `OCUPANET.cnv` e956f902928cc115..., read as cp850: the title is columns 10-59, the code from column 60), ship the code-title pairs as `occupation_sinan.csv` next to `dataset.py`, and decode in `_clean` into "title [code]" after `set_missing`, replacing `SINAN_OCCUPATIONS`; a code in no table becomes "[code]"; rename `occupation_cbo` to `occupation`; rewrite the occupation bullet of the notes; re-run `dataset check` and the dtype probe; then apply the same decision to rais_employment_separation_1m (its issue 5) and raise it in wioa_employment_after_exit. C: write the amendment into CLEAN-12 in `cleaning_features.md` with this dataset, rais and wioa as its cases, and an `Exception to CLEAN-12` line per record.

   [^c12]: **CLEAN-12** (Should; amended 2026-11-01, Lennart): a code whose codebook says in words what it means is decoded into those words, a nominal code (a job, a building type, a water source) into a category of the words; "a column that still ships as a number while its source has words for it is a gap to close, not a choice". **CLEAN-10**: a code that only means unknown is missing.
   [^amend]: principles.md, "Exceptions and amendments": when the same reason has produced three exceptions, the next pass proposes an amendment of the rule.
   [^c12prec]: labour_inspection_compliance (Statistics Norway's KLASS table in the folder); ny_wcb_assembled_claims_1m (this batch); credit_g (Lennart, 2026-10-31: "we want the right labels in all cases"); zillow_prize (Lennart, 2026-10-26: a model's score is no reason for an encoding).

**Review panel:** ship after changes (mediator). Tier full: claim auditor, column auditor, split auditor, domain
practitioner, blind reviewer, task gamer, precedent checker, advocate and critic with one rebuttal each, mediator.
Claim audit: 30 claims; the cohort, the label, the cuts, the copies, the windows and the metric hold; the year 2024
refuted (now 2023), three statements corrected (the copy sentence, a stale count, what Bohm et al.'s Table 4 lists),
and Bohm et al.'s reported performance cannot be reproduced on these rows. Column audit: every kept column is known at
notification, but 14.1% of the rows were notified after a dengue sample was taken (now dropped); the occupation's
unknown codes were left in (fixed). Blind review: include with changes; its concerns about symptoms coded "No" and
blank health regions were refuted by the data (explicit 2s in the source; states without health regions). Task gamer:
gameable only a little; the labels of the gap rows (+0.018 to +0.028 ROC AUC, outside the training indices, now a
protocol line) and counts read from inside the test window (+0.006, a note); nothing recovers the label. Debate: agreed
on the pre-notification filter, the surveillance team as the actor, the one-month gap, the COVID-19 note, the cohort
with `Selection Bias`, roc_auc with a corrected reason, the year and the cleaning fixes; disputed: the window set
(SPLIT-15 against SPLIT-20, issue 1); open: the one-patient copies (LEAK-19 exception, issue 2), activity counts (USE-6, issue 3) and the CBO decoding
(CLEAN-12, issue 4).

<details><summary>Mediator</summary>

MEDIATOR REPORT: sinan_dengue_case_screening (folder sinan_dengue_case_screening_1m), 2026-11-09

Read: principles.md (the working tree), splits.md SPLIT-10/14/15/17/20/21, use_case.md USE-3/6/7/9, metrics.md MET-1/8/11,
leak_checks.md LEAK-19/28-31, cleaning_features.md CLEAN-12; dataset.py; builder_report.md; every panel report
(claim, column, split auditors, domain practitioner, blind reviewer, task gamer, precedent checker); both briefs and
rebuttals. One decisive count run (work_mediator/m1_windows.py, .log).

1. RECOMMENDATION (judgment record)
Verdict: ship after changes.
Validity: SEL-1/SEL-2 hold. USE-1 triggered, fixed (actor reworded to the surveillance team; USE-9 asked, no direct
  fit). USE-3 triggered, fixed (drop the 14.1% notified after a dengue sample was collected). USE-8 holds as
  approximate + `Selection Bias`, numbers written in. LEAK-10 holds for every kept column (leukopenia timing-tested).
  SPLIT-1/9/13/14 hold; SPLIT-10 applied with gap=1; SPLIT-20 COVID note. PROV-9 fixed (2023).
Value: TP-1 to TP-5 pass (no_spread read as 3-window noise, re-check with tuned runs); MET-8 fallback roc_auc holds,
  MET-11 reason corrected.
Quality: CLEAN-10 fixed (occupation 000000 and SINAN's 99999x/998999 codes); CLEAN-12 full CBO decoding open (with
  rais); LEAK-19 exception for the one-patient copies (none crosses the split).
Weighed: size +, national open source +, honest difficulty (within unit-month AUC 0.59-0.62) +, COVID-only test
  windows -, tested-only cohort -, weekly file replacement (reproducibility) -.
For the curator: issue 1, the window set (a weighing call, SPLIT-15 vs SPLIT-20's coverage); issue 2, CBO decoding
  decided with rais (P7); issue 3, optional epidemic-activity inputs (Weigh).

2. CHANGES TO MAKE NOW (no decision needed; both briefs agree, each settled by its rule)
C1. P3/P4, USE-3 (Must), LEAK-10: in `_clean`, before the lab fields are dropped, keep only rows with no DT_SORO,
    DT_NS1, DT_PCR or DT_VIRAL dated before DT_NOTIFIC. 370,314 rows go (14.1%; dengue 61.7% vs 45.1% kept). A filter
    on facts dated before the prediction point, not on the label (USE-7 precedent: nyc_taxi_trip_duration_1m,
    pkdd_15). Notes: the share, the NS1 51% vs 35% positivity, the lift it removed (+0.004 to +0.031 AUC), and that
    43.8% sampled on the notification day stay (a same-day NS1 cannot be resolved). The notes must not call the task
    free of this path before the filter is in (critic rebuttal A1).
C2. P4, SPLIT-10 (Should): gap=1 (`TemporalSplits(..., gap=1)`). Median label delay 13-20 days; confirmed and
    discarded close alike (17 vs 18 days), so no selection by the outcome needs the p90; open training rows
    0.14%-0.85%; recovers 58%-100% of the 0.026-0.037 AUC the 2-month gap cost (split auditor). Gap at about the
    median-p75, as house_sales. Rewrite splits_comment's gap sentence with these numbers. Option (c) (as-of filter on
    the closing date) only if the API carries a split helper; not needed.
C3. P4, SPLIT-20 (Should): splits_comment names the COVID-19 period of all three test windows and the measured shifts
    (lab share of confirmed 0.20-0.32 -> 0.40-0.60; fever Yes 0.80-0.86 -> 0.73-0.77; leukopenia Yes halves; in 2021
    the lab cohort is more often dengue than the clinical closings, the reverse of every earlier quarter). No later
    labelled year exists. Add the season weighting (issue 1) as a note whatever the window decision.
C4. P3, USE-1/USE-5 (Must), USE-9: reword use_case and fit_reason to the municipal surveillance team at notification
    estimating which suspected cases are dengue, to close untested notifications (manual 8.4-8.5) and choose whom to
    test; the physician's differential diagnosis as a secondary reading; "before the dengue test's result" (a blood
    count is a lab result). Record that USE-9 was asked (the "physician who sent a sample" actor has no decision
    under the 2016 protocol) and why the fit stays approximate.
C5. P3, USE-8 (Must): `Selection Bias` marker; fit_reason with 64.0% vs 47.7% dengue (untested vs lab cohort), lab
    share 40.3% at a state's peak months vs 50.6% off-peak, lab share of decided 37-42% in training years vs 56% in
    2021, the 2021 reversal. Also USE-5 notes: the label is "test negative", sensitivity tied to days since onset; the
    label is a conclusive lab result on 92.4% of rows of each class; leukopenia "No" mostly means no count.
C6. P6, MET-8 (Should) / MET-11 (Must): keep roc_auc (MET-8's binary fallback). Fix the reason: Bohm et al.'s Table 4
    lists five metrics (accuracy, sensitivity, specificity, precision, F1), AUC is in the text; no single criterion
    (MET-5); their call for high sensitivity is named and set aside (no threshold or cost, MET-6); the base rate swings
    13%-59% by quarter and every family's log loss is worse than the constant, so log_loss would mostly test prior
    shift. The domain practitioner's log_loss is thereby set aside with a reason, not ignored.
C7. P5, PROV-9 (Must): year 2023 (DATASUS FTP FINAIS carries the same release, DENGBR23.dbc = the portal's 1,645,956
    rows; Bohm et al. used it before 2023-11-28); BibTeX names the DATASUS distribution.
C8. P4, LEAK-19 (Should), exception: the 628 one-patient copy groups stay, recorded as an exception; fact: the
    notification date is an input, so no copy crosses the split (0 per fold), and they cannot be told apart in
    2020-2021. Precedent checker prompt 1, option (a); a recorded exception, so the curator sees it in REVIEW.md.
C9. Writing (writing.md, LEAK-16): "0.6% of test rows match a training row on every input but the date; none with it";
    5,518 -> 5,524; the record's Assessment: Bohm et al.'s 0.985 cannot be reproduced with their variables on these
    rows (AUC 0.578). One line that the accept reason ("most rows") changed: 2.62M labelled rows, not the 6.5M of 2024.
C10. P7, CLEAN-10 (Should): occupation "000000" (8,401 rows) to missing; decode SINAN's own codes 999991-999995 and
    998999 (536,623 rows) once SINAN's occupation table is found, 998999 missing if it is "ignorada". If the table
    cannot be found, note the codes as undocumented; the 1,584 "10001" rows noted.
C11. Re-measure after C1+C2 and update the numbers in the notes (counts below are the mediator's, before the model
    re-runs): window sizes, train shares, smallest class, the probes.

3. ISSUES FOR THE CURATOR (ranked)
Issue 1. P4, SPLIT-15 (Should) against SPLIT-20 (Should): which three half-years to test. A weighing call.
  Problem: two of three windows (2020H2, 2021H2) are off-season, holding 36% of the test rows (after C1) but 2 of 3
    weights in the mean over windows; January-June holds 67%-84% of a year's notifications. Off-season windows score
    higher (LightGBM 0.74-0.75 vs 0.65), so the reported mean sits above the row-weighted one (0.714 vs 0.686).
  Effect: the level and the weighting of the reported score; the family order is unchanged in every window
    (LightGBM over logistic +0.058 to +0.084).
  Keep (advocate; critic accepts as mildest): SPLIT-15 asks to roll contiguous windows back from the newest, earlier in
    the file than SPLIT-20; the curator chose contiguous windows twice (rain_in_australia, airqo); the off-season is
    half of every year, not an "atypical season" (precedent checker D2: CONSISTENT); both seasons are covered.
  Move to 2020H1/2021H1/2021H2 (split auditor): season coverage, two of three windows in the season that holds most
    cases; inside SPLIT-14; airqo moved windows for season coverage; decided on coverage, not scores (SPLIT-21).
    Against: non-contiguous; 2020H1 is mostly pre-COVID (Jan-Feb 37% of its rows), so the windows mix periods.
  Settled facts (mediator's count, with C1 and gap=1): shipped set test 108,465 / 344,905 / 88,134 rows, train shares
    93.4% / 79.2% / 74.4%, smallest class 20,501; season set 2020H1 window 430,995 rows (whole, under the 500k cap
    after C1), train share 56.0% (55.2% with gap 2), smallest class 34,195. Both pass SPLIT-14 and SPLIT-17.
  Rule reading: not a Must conflict; the rules lean to keep (SPLIT-15 by position, and airqo's fact, both seasons
    covered, already holds). How much the season should weigh in the mean is not fixed by any rule.
  Decision: (a) keep with the weighting note (recommended), or (b) cutoffs 2020-01, 2021-01, 2021-07.

Issue 2. P7, CLEAN-12 (Should): the occupation's CBO codes (2,301 levels) as "words [code]" or as codes.
  Problem: CLEAN-12 (amended 2026-11-01) names "a job" among codes to decode; the dictionary gives no words, only a
    pointer to SINAN's occupation table (CBO 2002 + SINAN codes). The notes give no reason for keeping the code.
  Effect: quality only (P7); a model sees the same partition. Never blocks shipping (P3 over P7).
  For decoding (precedent checker): labour_inspection_compliance (KLASS table in the folder), ny_wcb_assembled_claims_1m
    ("words [code]"), credit_g ("the right labels in all cases"). For keeping (both briefs): no words in the release;
    a third exception of this reason with rais and wioa makes an amendment due.
  Decision, taken once for sinan, rais_employment_separation and wioa_employment_after_exit_1m (same CBO list):
    (b) decode from the pinned official CBO 2002 table (recommended by the precedent checker), or (d) amend CLEAN-12
    for large external classifications. C10 stands either way.

Issue 3. P3, USE-6 (Weigh): no input for current local epidemic activity counted over all notifications.
  Problem: the actor knows recent notification counts in the municipality; the shipped cohort holds only lab-decided
    rows (about 1 in 2.8 notifications in 2017), so a participant's past counts are counts of later-lab-closed cases.
  Effect: honest past counts add +0.009 AUC in the cohort (task gamer); whether all-notification counts do the same is
    unmeasured. Raised by the domain practitioner only; neither brief argued it.
  Decision: (a) leave it (recommended: a constructed feature beyond the minimal expert state, needs the full files);
    (b) add label-free 7- and 28-day counts of all notifications per municipality, strictly before the date.

4. TASK GAMER'S EXPLOITS, MAPPED
The definition has no `Potential leak, kept on purpose:` note and no accepted warning these could match.
- #1 Gap-row labels in data.parquet (+0.018 to +0.028 mean; +0.038 / +0.016 / +0.031 vs the better honest model):
  SPLIT-10 / SPLIT-9. Known by construction: every multi-window container ships the other windows' rows with labels,
  and the splits keep them out of training; using rows outside train_idx breaks the protocol. A harness matter, not a
  definition defect (both briefs agree). C2 moves the first gap month into honest training (+0.0066 of the gain); the
  adjacent month stays an exploit only for a participant reading outside the split. No issue.
- #2 Future counts from the test window (+0.005 to +0.008 per split, about 10x noise): test-batch statistics, LEAK-30
  family (a weak transductive gain). New; no shipped column carries it. No change to the definition; optional one-line
  note in splits_comment with its size. No issue.
- Training cap keeps recent rows at 42-49% (+0.0015, mixed sign): the _1m protocol's sampling; not an exploit.
- Lab-cohort selection on a post-prediction variable: USE-8, handled by C5; the gamer found no score exploit in it.
- Nothing else recovers the label (row order, format, missingness, copies: +0.001, noise +-0.0005).

5. AGREED FACTS
- 2,623,839 rows (47.5% dengue), 37 features; only 2016-2021 hold discarded cases (portal and DATASUS FTP).
- Cohort CRITERIO=1, 42% of decided notifications; label a conclusive lab result on 92.4% of each class.
- Every kept column is known at notification by the dictionary; post-notification and erased-on-discard fields
  dropped; leukopenia timing-tested (odds ratio 2.28 / 2.94 / 2.91 by investigation delay; late-typed 2021 forms carry
  no more signal, 0.635 vs 0.639 / 0.657); worth 0.002 AUC. Symptom "No" are explicit 2s; health regions blank for
  whole states structurally (blind reviewer's points 2 and 3 refuted).
- Pre-notification sample: 370,314 rows (14.1%; 12.6%-16.0% of test windows); found by the features at AUC 0.87-0.90.
- Split: temporal by notification date, regime right (random split overrates by 0.08-0.18 AUC); units recur 95-97%.
- Signal: beats the dummy on 3/3 windows; within unit-month AUC 0.59-0.62.
- Mediator's count (m1_windows.log): after C1, 2,253,525 rows; shipped windows with gap 1: test 108,465 / 344,905 /
  88,134 (dengue 0.315 / 0.497 / 0.233), train 2.11M / 1.79M / 1.68M (93.4% / 79.2% / 74.4%), each above 1M; with gap
  2: 90.4% / 78.7% / 71.9%. SPLIT-14 holds in every combination; the filter barely moves the train shares.

6. CONSISTENCY
- Followed: cohort approximate + `Selection Bias` (sdss_17, tunisian_fraud, lt_vehicle_loan; D1); the filter on
  pre-prediction dates (USE-7: nyc_taxi_1m, pkdd_15); leukopenia kept on a timing test (onlinenewspopularity,
  heart_disease; D3); contiguous rolled-back windows (rain_in_australia, airqo; D2); licence as a one-line note (EV-4,
  D5); place and unit codes kept as entity codes (D6); roc_auc fallback for a multi-metric paper (gallstone_disease);
  gap near the median-p75 delay (house_sales).
- Departure, with its fact: the one-patient copies kept against LEAK-19's drop cases (qsar_oral_toxicity,
  audiology_diagnosis); fact: the date is an input, so no copy crosses the split (C8).
- Open across datasets: CBO decoding must match rais_employment_separation and wioa (issue 2; the rais mediator left
  the same call to the curator).
- To watch: sivep_gripe_sari_outcome (same portal) should be judged against this cohort and filter when added.

Files: this report; scripts in the run folder.

</details>

<details><summary>Claim audit</summary>

CLAIM AUDITOR REPORT: sinan_dengue_case_screening_1m (record sinan_dengue_case_screening), 2026-11-09

Verdict: the definition's validity claims hold under every test I could run. The cohort, the label, the cut points,
the copies, the Espirito Santo drop, the metric and the splits all survived refutation attempts. One Must-level
metadata claim is refuted: the year 2024 (PROV-9), because the rows were public through DATASUS before 2024. Four
smaller statements are wrong in wording or numbers. Two challenges go to the curator: a USE-9 reading of issue 1,
and Bohm et al.'s performance, which cannot be reproduced.

Scripts and logs: scripts in the run folder (a1's output is quoted below). Data: the
prepared lab-criterion parquet (2,984,607 rows), the definition's own _clean (2,623,839 rows), the built container
(1,679,297 rows), the builder's string copies of DENGBR14-26, and DATASUS FTP DENGBR23.dbc (downloaded to scratch).

TABLE (claim | source | test | result | evidence | rule)
1 Cohort = CRITERIO 1, 2,979,887 of 7,030,293 decided (42%); 35% of confirmed, 48-56% of discarded |
  claims 8, 19; curation_comments "Cohort" | recount from the yearly files; reproduce Bohm et al.'s cohort |
  HOLDS | prepared file holds only CRITERIO 1; builder's labshare.log matches; RJ+MG 2016+2019 lab-decided =
  238,579 confirmed / 134,999 discarded against Bohm's 229,113 / 135,163 (weekly file updates explain the gap) |
  USE-8, USE-5
2 "as in Bohm et al." | curation_comments | paper Methods | HOLDS | PMC11167742: "All data were confirmed by
  laboratory tests" (the Results say "laboratory criteria") | PROV-12
3 Label is a laboratory result, not a clinical-epidemiological closure | task summary "predicted", builder | count
  the conclusive results (six tests: IgM, NS1, isolation, RT-PCR, histopathology, IHC) per class on the kept rows |
  HOLDS FOR ABOUT 92%, NOT 100% | Yes rows (1,245,418): 92.4% have a positive test, 1.9% only negatives, 5.5% no
  conclusive result; No rows (1,378,421): 92.4% a negative and no positive, 1.0% a positive, 6.1% no conclusive
  result; the no-result share runs 3.9%-8.0% by year and class, close between classes | USE-5 (a note, not a defect)
4 Clinical-epidemiological closings are something else (the cohort is the tested cases) | implied by issue 1 |
  conclusive lab results among CRITERIO 2 rows, 2016-2021 files | HOLDS, and sharpens issue 1 | clin-epi confirmed
  with a conclusive result 1.4% (2016) to 9.3% (2020-21); clin-epi discarded 3.3% to 19.0%. So the cohort is
  close to "notifications whose sample came back conclusive" | USE-8, USE-9
5 Fit approximate (deployment meets every suspected case) | claim 8, fit_reason | logic plus item 4 | HOLDS for the
  screening use case as written; see challenge C1 (USE-9) | USE-8, USE-9
6 Only 2016-2021 hold discarded cases; 2014-15 and 2022-26 have no CLASSI_FIN 5 | claim 16 | value counts on all 13
  portal files; also the DATASUS FTP's own DENGBR23.dbc | HOLDS, also on the second distribution | portal:
  2014-15 and 2022-26 have codes 10/11/12/8/0/blank only (0.47M-6.56M rows a year). FTP FINAIS/DENGBR23.dbc: the same
  1,645,956 rows, 0 rows with code 5, so the FTP does not rescue the later years | PROV-1, PROV-4
7 683 rows outside 2016-2021 dropped | claim 18 | recount | HOLDS | 683 | -
8 355,366 rows without the clinical section dropped | claim 21 | recount through _clean | HOLDS | 2,984,607 - 683
  - 4,719 undecided - 355,366 = 2,623,839 | USE-7
9 Signs are known at notification (the clinical section is filled at the investigation start) | claim 15, builder's
  "cannot verify edits after the lab result" | (a) DT_INVEST same day; (b) NEW: DT_DIGITA (first typing into
  SINAN, in the 2021 file only, 98.6% filled): do the signs carry more label signal when the form was first typed
  after closing, with the result known? LightGBM on the 25 clinical/person inputs, trained on 400k rows from
  2019-01 to 2020-10, scored on 2021 by typing group | HOLDS (no sign of contamination) | (a) 92.8% same day. (b)
  257,646 of 515,887 2021 rows (49.9%) were first typed on or after the closing date (typing lag median 6 days, p90
  39). Clinical-only AUC: typed after closing 0.635, typed before closing 0.639, typed within 3 days 0.657; within
  state x quarter 0.629 / 0.632 / 0.647. Late-typed forms record FEWER Yes signs (dengue 4.07 vs 4.44). Leukopenia
  difference in dengue share Yes-No: +0.238 late vs +0.205 / +0.226; tourniquet +0.132 vs +0.125 / +0.118 (within
  noise). The all-features model scores higher on late-typed rows (0.690 vs 0.677; within strata 0.681 vs 0.659),
  which points to the place columns, not the signs. Edits after the first typing remain untestable | LEAK-10, USE-3
10 Leukopenia: dengue 67% with it, 46% without; worth 0.002 AUC | claim 28 | recount on _clean; read drop_tests.log |
  HOLDS | 0.671 / 0.462; drop_tests: 0.7096 vs 0.7076 | LEAK-10 (issue 3)
11 Place-of-infection and work fields erased on discard; dropped | claim 22 | dictionary fields 66-72 + builder log |
  HOLDS | dictionary: "automaticamente apagados"; blank 97.6-99.3% (No) vs 20-25% (Yes); not in features | LEAK-10
12 Alarm/severity and older-form fields post-outcome; dropped | claims 23-24 | dictionary + feature list | HOLDS |
  the 37 shipped features contain none of them | LEAK-10
13 Exact copies kept as natural repeats: 5,762 rows (0.22%), 2,843 groups; 1,056 of 1,684 dated groups different
  patients; 306 two-label groups | claim 30 | rehash all 37 inputs on _clean; birth-date spans; the system's own
  duplicate flag NDUPLIC_N | HOLDS | 5,762 / 2,843 / 306 reproduced. Different birth dates are a median 106 days
  apart (IQR 47-187); 68 of the 1,056 differ in one character (possible typos of one patient, about 6%). 2,282 of
  the 5,762 copy rows (40%) record no Yes sign (low-information profiles). NDUPLIC_N on kept rows: blank 2,614,841,
  0 6,748, 1 2,250, and code 2 ("duplicidade, nao contar") never, so the publisher has already removed the
  flagged duplicates | LEAK-16, LEAK-18, LEAK-19, LEAK-20
14 "leak probe 5 finds an exact copy in train for 0.6% of test rows" | claim 30, curation_comments | exact-copy
  count over feature_columns on the built container, per fold | REFUTED AS WORDED | 0 test rows in each of the 3
  folds have an all-feature copy in train: the notification date is a feature, so no copy crosses a temporal split.
  The 0.6% is probe 5 without the date | LEAK-16 (writing)
15 Espirito Santo: 16,923 (2019) -> 444 (2020) -> 6,748 (2021); the portal's e-SUS VS note | claim 31 | recount
  (cohort and all criteria); read the portal page again | HOLDS, now verbatim | cohort by notification year:
  16,923 / 444 / 6,748; all criteria: 81,201 / 7,824 / 15,468. Portal: "A partir de 2020 o estado do Espirito
  Santo passou a utilizar o sistema e-SUS Vigilancia em Saude ... foram considerados apenas os dados
  disponibilizados pelo Sinan online". The rows are absent at the origin, with nothing to repair from this
  release | PROV-13
16 Target Yes = 10-12 (+1-4), No = 5; 47% Yes; 13-59% by quarter | claim 20 | recount | HOLDS | 0.4747; quarterly
  min 0.130 (2016Q4), max 0.590 (2020Q2) | USE-5
17 days_onset median 3, missing beyond 365 days for 5,518 rows | claim 26 | recount on the final frame | NUMBER
  STALE | 5,524 rows > 365 (median 3; no negative lags); 5,518 came from the version before the copies were
  restored | writing
18 Decoding: signs Yes/No, diseases 9 missing | claim 27 | raw value counts on kept rows | HOLDS | signs only 1/2
  (e.g. FEBRE 2,080,899 / 542,940); diseases have 9 on 8-12 rows | CLEAN-12
19 Windows 129k / 394k / 103k; train 1.89M-2.37M sampled to 1M; gap two months | claims 14, 32, 34 | built
  container | HOLDS | test 129,189 / 394,414 / 102,639; train 1,000,000 each, pools 2,366,472 / 2,070,124 /
  1,887,364; train ends 2021-04-30 / 2020-10-31 / 2020-04-30; gap 62 days in each | SPLIT-1, SPLIT-10
20 Yearly windows fail SPLIT-14; 2019-2021 hold 73% | claim 33 | train share per yearly window | HOLDS | 0.731;
  yearly windows: 2019 0.259, 2020 0.554, 2021 0.789 (two windows at or above 50%) | SPLIT-14
21 Gap: 1.7-1.8% (July) and 0.5% (January) open without it; 0.07-0.4% with it | claim 35 | builder's
  verify_claims.log, re-read | HOLDS | 1.84% / 0.52% / 1.74%; with the gap 0.31% / 0.07% / 0.36% | SPLIT-9, SPLIT-10
22 Metric: fallback ROC AUC; Bohm et al. Table 4 define six metrics incl. ROC AUC and report three side by side,
  no threshold or cost; portal and dictionary define none | claim 36, metric reason | read Bohm et al.'s
  evaluation section again; grep the dictionary | HOLDS, wording inexact | Table 4 ("Metrics for classifier
  evaluation used in this work") lists 5: accuracy, sensitivity, specificity, precision, F1. AUC is introduced in
  the text of the same subsection, not in Table 4. The Results name the tree best on ACC and F1 and the MLP best on
  AUC, and the Conclusion picks the tree "for the best compromise between predictive performance and computational
  complexity": no single criterion (MET-5). The Discussion says high sensitivity matters, but fixes no threshold,
  no specificity floor and no cost, so MET-6 sends it to the fallback. The reason does not mention that emphasis,
  and MET-11 asks a fallback to name the metric it rejected. The dictionary defines no metric | MET-1, MET-5,
  MET-6, MET-8, MET-11
23 Metric computable on every fold (MET-2) | implied | scorer on random probabilities per fold; class counts |
  HOLDS | random 0.501 / 0.500 / 0.503; minority class 46,043 / 189,374 / 27,894; no scoring columns, no
  sample_weight; unit = notification = row | MET-2
24 The metric means the same as at the source (MET-2) | implied | target and classes vs Bohm et al.; balance | HOLDS
  with one caveat | same target (lab-confirmed vs lab-discarded) and classes. Bohm balanced 10k/10k at random;
  ours keeps the natural 27-52% per window, which ROC AUC ignores | MET-2
25 Bohm et al.'s performance (abstract "98%", tables 92-93% accuracy) describes this task | record Assessment
  ("0.985 ... is not reached") | replicate their setup: RJ+MG 2016+2019, lab-decided, random 10k/10k, 70/30,
  logistic regression on their 10 variables (sex, age, fever, myalgia, headache, vomiting, nausea, back pain,
  rash, retro-orbital pain) | NOT REPRODUCIBLE | AUC 0.578, accuracy 0.565 (0.594 / 0.577 if the blank-section
  rows are kept and their blanks used as indicators). Their numbers do not come from these variables on these
  rows | EV-2 (a note for the record; no change to the definition)
26 Year 2024 = first publication (the portal page, created 22 Feb 2024) | claim 9, year, bibtex | where else the
  rows were public before 2024 | REFUTED | Bohm et al. (received 2023-11-28) took SINAN 2016 and 2019 data
  "available in DataSUS". The DATASUS FTP folder dissemin/publicos/SINAN/DADOS/FINAIS/ holds DENGBR00-25.dbc (the
  current timestamps are re-uploads, 2022-2026). Its DENGBR23.dbc has exactly the rows of the portal's 2023 CSV
  (1,645,956), so the FTP is the same release, published earlier. The exact first year cannot be read (files
  replaced); it is 2023 at the latest | PROV-9 (Must), PROV-8
27 Licence CC BY-ND 3.0 | claim 11 | portal page | HOLDS | "Todo o conteudo deste site esta publicado sob a licenca
  Creative Commons Atribuicao-SemDerivacoes 3.0" | EV-4
28 Use case quote | claim 2 | paper | HOLDS | "the aim of the study was to use machine learning to assist in medical
  decision-making based only on clinical data" | USE-1
29 Notifying unit and places legitimate (worth about 0.09 AUC) | claim 29 | not re-run (builder's drop_tests 0.710
  vs 0.620); item 9's late-typed vs early-typed contrast shows the place gain is larger on forms typed after
  closing (all features +0.013, within strata +0.022, signs-only -0.004) | HOLDS (no mechanism found by which a
  place is set by the outcome) | USE-6, LEAK-34
30 Cohort shift across the split | implied by split + cohort | lab share by year | A NOTE, NOT A REFUTATION | the
  lab-decided share of decided notifications rises from 37-42% (2016-2019, training) to 46% (2020) and 56% (2021,
  test). The tested population in the test windows is broader than in training | SPLIT-1, USE-8

REFUTED AND UNTESTED, RANKED (principles.md: validity first, Must first)
R1. P5, PROV-9 (Must): year 2024 refuted (item 26). The rows were public on DATASUS before the portal page: Bohm et
    al. used them before 2023-11-28, and the FTP's DENGBR23.dbc equals the portal's 2023 file. Effect: metadata
    only, no change to the data or the evaluation. Mildest remedy: set the year to the latest year we can prove
    the release public (2023), with the reason in the curation notes: "DATASUS FTP FINAIS distributes the same
    yearly files; first public before Bohm et al.'s submission of 28 Nov 2023; earlier first-upload dates are
    overwritten". Better, if it can be found: the first-upload year of DENGBR21 (e.g. the Wayback Machine or
    pysus/microdatasus release notes). Point the BibTeX to the DATASUS distribution, or name both.
R2. P4, writing (LEAK-16): "leak probe 5 finds an exact copy in train for 0.6% of test rows" (item 14). In the
    shipped container no test row has an all-feature copy in train (0 in each of 3 folds), because the date is a
    feature. Remedy: "0.6% of test rows match a training row on every input but the date; none with it".
R3. P6, MET-11 (Must) wording: the metric reason says Table 4 defines six metrics including ROC AUC (item 22). It
    lists five, and AUC is in the subsection's text. The reason also does not mention the Discussion's call for high
    sensitivity, which it must set aside under MET-6. The fallback itself holds. Remedy: "Bohm et al. 2024 define
    accuracy, sensitivity, specificity, precision and F1 (Table 4) and AUC in the text, name the tree best on ACC
    and F1 and the MLP on AUC, and pick the tree on a compromise with complexity; the Discussion asks for high
    sensitivity but fixes no threshold or cost (MET-6) ..."
R4. Writing: 5,518 rows with an onset lag over 365 days -> 5,524 on the final frame (item 17). Update the number.

UNTESTED
U1. Edits to the clinical section after the first typing (builder's open point). The only timing field,
    DT_DIGITA, records the first inclusion and "is not updated when the notification is changed" (dictionary field
    118), and exists only in the 2021 file. What I could test (item 9) found no contamination: half of the 2021
    forms were first typed after closing, and their signs carry no more label signal (clinical-only AUC 0.635 vs
    0.639 and 0.657). Keep it in "what a human must check", with this result added to the notes as evidence.
U2. The exact first-publication year (R1).

CHALLENGES FOR THE CURATOR (not refutations)
C1. Issue 1 (USE-8, Must; USE-9, Should): the cohort is almost exactly "notifications whose laboratory sample came
    back conclusive". Clinical-epidemiological closings carry a conclusive result in only 1.4%-9.3% (confirmed)
    and 3.3%-19% (discarded) of rows (item 4). USE-9 asks, before settling on approximate, whether another real use
    case fits directly: "a physician who has sent a sample decides how to manage the patient before the result
    returns (IgM needs day 6 or later)". Its deployment population is the tested cases, which this cohort mirrors.
    That would give issue 1 an option (d): restate the use case for tested patients, fit direct, `Selection Bias`
    still named in fit_reason. The leftover gap is the tested cases closed clinically (roughly 10% of 2021's tested
    rows, from the shares above). The builder's option (a), approximate, also remains defensible.
C2. Bohm et al.'s performance is not a benchmark for this task (item 25). Their 10-variable logistic regression
    gives AUC 0.578 on their own cohort, against their reported 92-93% accuracy. The record's Assessment line
    ("0.985 on a balanced random sample is not reached") should say it cannot be reproduced with their variables on
    these rows, so that nobody reads our 0.69-0.71 as a failure of the definition.
C3. Copies (LEAK-18): the call holds. About 6% of the different-birth-date groups (68 of 1,056) differ in one
    character, so some "different patients" are probably one patient with a typo. That is about 0.003% of rows, no
    action.

</details>

<details><summary>Column audit</summary>

COLUMN AUDITOR REPORT: sinan_dengue_case_screening (folder sinan_dengue_case_screening_1m), 2026-11-09

Verdict: ship after one change (a cohort filter, finding 1) or the curator's explicit keep with a note; every
column is known at notification by the data dictionary; one cleaning gap in the occupation codes (finding 3).

Prediction point (dataset.py, first curation_comments bullet): the notification of a suspected case at a health unit
(DT_NOTIFIC); use case: a physician decides "before or without a laboratory result".

Sources read: dataset.py; builder_report.md; the data dictionary (dic_dados_dengue.txt, Sinan Online, 14/07/2025,
fields 1-121, read in full); principles.md, use_case.md, leak_checks.md, cleaning_features.md (the working tree).
Measurements: the full cleaned frame (2,623,839 rows, `_clean` re-run on the prepared parquet) with the raw date and
code fields aligned by row; dtype probe re-run on the final definition. Scripts and outputs: scripts in the run folder.

COLUMN TABLE  (column | meaning (dictionary field) | known at notification? | dtype and cleaning | verdict | rule)
notification_date | date the notification form was filled (f3) | yes, it is the prediction point | datetime, time column | fine | SPLIT-1
notification_state | state of the notifying unit (f6), IBGE code decoded to abbreviation | yes | category, 27 levels | fine | CLEAN-12
notification_municipality | IBGE code of the notifying unit's municipality (f7) | yes | category code, 4,991 levels; dtype flag numeric_levels: a code, category by meaning | fine | CLEAN-14
notification_health_region | health region of that municipality, system-filled from the municipality table (f8) | yes | category code; "0"/blank missing (7.3%: whole states RR, DF, RJ, TO, AP have none, structural); flag numeric_levels answered | fine | CLEAN-10, CLEAN-14
notifying_unit | CNES code of the unit that notified (f9) | yes | category code, 40,584 levels (122 five-digit codes); flag answered | fine as a column, but it carries finding 1 (identifies units that notify after sampling, AUC 0.845) | LEAK-34; see finding 1
sex | M/F, I = ignored (f14) | yes | category; I and blank missing (0.09%) | fine | CLEAN-10
pregnancy | gestational status (f15): trimesters, unknown age, no, not applicable (auto for men and women <=10) | yes | category, 9 and blank missing (7.5%); "not applicable" also chosen for 8% of women aged 15-49 (a user choice, kept) | fine (note) | CLEAN-12
race_colour | self-declared race/colour (f16) | yes | category, 9 missing (17%; 19.7% of dengue vs 15.2% of discarded, mild, builder read it) | fine | CLEAN-10, LEAK-13 (checked)
schooling | last grade completed (f17) | yes | ordered, 0 illiterate ... 8 higher education complete = the dictionary's order; 9/blank missing; 10 "not applicable" (age <7: 99.9% of rows under 7) missing as a state off the scale; 0 is a real level here (0.6%, stable by year), not a blank fill; no "00/09/99" codes on kept rows | fine | CLEAN-12, CLEAN-14
residence_state | state of residence at notification (f18) | yes | category, decoded | fine | CLEAN-12
residence_municipality | IBGE code of residence municipality (f19) | yes | category code; flag answered | fine | CLEAN-14
residence_health_region | health region of residence (f20) | yes | category code, "0"/blank missing (6.9%); flag answered | fine | CLEAN-10, CLEAN-14
residence_country | country of residence (f21; "1" = Brazil on 99.998%) | yes | category code (no words in the dictionary; 17 levels); flag answered | fine | CLEAN-12 (no words given)
occupation_cbo | occupation, CBO code from SINAN's occupation table (f23) | yes (patient attribute, field sits in the investigation block but is not outcome-driven: missing 63.0% vs 63.3% by class) | category code, 2,301 levels; "" / "0" / "XXX" missing, but "000000" (8,401 rows) is not; SINAN's non-CBO codes 999991-999995 and 998999 (536k rows) undocumented | cleaning problem | CLEAN-10, CLEAN-12 (finding 3)
fever, myalgia, headache, rash, vomiting, nausea, back_pain, conjunctivitis, arthritis, severe_arthralgia, petechiae, retro_orbital_pain | clinical signs (f24-34, f37), 1 yes / 2 no, mandatory | yes: clinical section, investigation started on the notification day for 92.8% of rows | category Yes/No; no missing on kept rows (all-blank rows dropped by USE-7) | fine | CLEAN-12, CLEAN-14
tourniquet_test_positive | prova do laco (f36), a bedside test | yes | category Yes/No | fine | USE-6
leukopenia | "Sinais clinicos (Leucopenia)" (f35), 1 yes / 2 no, mandatory | yes when a blood count was done at the first visit; "No" mixes "count normal" with "no count" (the form has no "not done") | category Yes/No | fine, keep with the builder's note (finding 2) | LEAK-10 tested, USE-6, LEAK-37
diabetes ... autoimmune_disease (7) | pre-existing diseases (f38-44), 1/2 (9 on 8-12 rows, missing) | yes | category Yes/No | fine | CLEAN-10
age_years | built from NU_IDADE_N (f13; first digit the unit), age at onset | yes | float; unit digits 0 and 5-9 (57 rows) and >120 missing; 210 ages 101-120 kept | fine | CLEAN-11, CLEAN-19
days_onset_to_notification | DT_NOTIFIC minus DT_SIN_PRI (f10, "<= notification date") | yes: both dates at or before the prediction point; no negative lag in the data; >365 (5,524) missing | float | fine as a span (not ended by the outcome), but second carrier of finding 1 (AUC 0.737 for "sampled before notification") | LEAK-10 span clause does not apply; see finding 1
dengue_confirmed | target: CLASSI_FIN 10/11/12 (and 1-4) vs 5, cohort CRITERIO = 1 | outcome | No/Yes, Yes the event | fine | CLEAN-25

Dropped fields, checked against the dictionary and the data (all right to drop):
* Place of infection and work-relatedness (TPAUTOCTO, COUFINF, COPAISINF, COMUNINF, DOENCA_TRA; f64-69, f72): the
  dictionary says they are enabled only when the final classification is confirmed or null and "automatically
  erased" when it is discarded. Measured: TPAUTOCTO blank 20.2% (dengue) vs 97.6% (discarded), COMUNINF 25.1% vs
  99.3%. Missingness that encodes the outcome: LEAK-10, dropped correctly.
* HOSPITALIZ, DT_INTERNA, UF, MUNICIPIO (f62-65): investigation fields (blank 18.6% vs 24.8%, yes 5.9% vs 4.7%);
  dropped, right under LEAK-10 (not known at notification).
* DT_INVEST (f22): its lag is a process field after notification; dropped, right.
* Every lab test and date, serotype, histopathology, immunohistochemistry (f45-61), CLASSI_FIN, CRITERIO, CLINC_CHIK,
  EVOLUCAO, DT_OBITO, DT_ENCERRA (f70-76), alarm and severity signs and dates (f77-102, enabled only for classes
  11/12), the old haemorrhagic section (f103-115): post-notification or label, dropped, right (LEAK-10, LEAK-2).
* System fields (TP_NOT, ID_AGRAVO, SEM_NOT, NU_ANO, SEM_PRI, TP_SISTEMA, NDUPLIC_N, DT_DIGITA, CS_FLXRET, FLXRECEBI,
  MIGRADO_W, source_year) and DT_NASC/ANO_NASC (personal data, age kept): right (CLEAN-3, CLEAN-5).
* But: the lab collection dates (DT_SORO, DT_NS1, DT_PCR, DT_VIRAL) are not all after the prediction point; see
  finding 1. They are rightly not features; they define which rows are at the prediction point.

Dtype probe (re-run on the final definition; scripts in the run folder): 7 of 36 columns flagged,
all `numeric_levels` on code columns (two municipalities, two health regions, notifying unit, occupation, country):
codes typed categorical by meaning (CLEAN-14). No count or measurement typed categorical, no code typed numeric.
The builder's first dtype run (probes/dtype) still showed "XXX" and an empty-string unit level; both are gone in the
final definition.

PROBLEMS, RANKED BY principles.md

1. P3/P4, USE-3 (Must) with LEAK-10 / LEAK-22 (cohort at the prediction point): 14.1% of the rows were notified
   AFTER a dengue sample had been collected. Strength: moderate, Must-level in kind.
   Evidence (full cleaned frame, earliest of DT_SORO/DT_NS1/DT_PCR/DT_VIRAL minus DT_NOTIFIC):
   * 370,314 rows (13.4%-16.2% by year, 12.6%-16.0% of the three test windows) have a sample collected before the
     notification date: 100,893 more than a week before, 156,946 two to seven days, 112,475 one day. Dengue 61.7%
     in them against 44.9% in the same-day-investigation rows without an earlier sample (57%-66% by lag bin).
   * NS1 collected before notification is positive (RESUL_NS1 = 1) in 51% of those rows against 35% when collected on
     the notification day: the notification often follows the result, the opposite of the use case ("before or
     without a laboratory result").
   * The features find these rows: LightGBM on all features predicts "sampled before notification" at ROC AUC
     0.898 / 0.872 / 0.893 on the three windows; the notifying unit's training-period rate alone 0.845, the
     notification municipality 0.767, days_onset_to_notification alone 0.737 (52% of rows with a lag of 14-30 days
     and 67% beyond 30 days were sampled first). The 130 units with >=200 rows and >95% dengue (82,134 rows) were
     sampled before notification in 49.6% of their rows (14% overall): units that notify the positive results.
   * Effect on the task (LightGBM, 300k training rows before the gap, my approximation of the three windows): ROC AUC
     on the pre-sampled test rows 0.806 / 0.717 / 0.773 against 0.723 / 0.647 / 0.713 on the other rows; all rows
     0.750 / 0.663 / 0.735; cohort without the pre-sampled rows (train and test) 0.719 / 0.659 / 0.706. The rows
     lift the benchmark score by 0.004 to 0.031 through a shortcut a screening physician does not have.
   * Not caught by the probes: no single column is post-outcome; the collection dates are rightly dropped; the
     effect runs through the unit and the onset lag, both legitimately known at notification.
   Mildest remedy (fix the definition, a filter): keep only notifications with no dengue sample collected before the
   notification date (read DT_SORO, DT_NS1, DT_PCR, DT_VIRAL in `_clean` before the drop; a collection date before
   the prediction point is a fact known at it, so filtering on it is no selection by the outcome). Cost 14% of rows;
   the window sizes stay above the floors (test windows 103k-394k now). Alternative: keep, with a note in the
   curation comments and fit_reason naming the share and the lift, and the use case widened to "notified before or
   after a first test". Also for the note: 43.8% more were sampled on the notification day; a same-day NS1 rapid
   result may be in hand for some of them, which the data cannot resolve.
   For the curator: a validity call (P3/P4), recommend the filter.

2. P4, LEAK-10 / USE-3 / USE-4 on `leukopenia` (the builder's issue 3): not a leak by the dictionary or the data;
   keep with the note, reword one line.
   Evidence: the dictionary lists it as field 35 "Sinais clinicos (Leucopenia)", mandatory, in the clinical section
   with the signs (f24-37), not in the laboratory section (f45-61); the clinical section is filled with the
   investigation, which starts on the notification day for 92.8% of the rows. Its association with the label does not
   grow when the section may have been filled later: odds ratio 2.28 (same-day investigation, no earlier sample),
   2.94 (investigation 1-7 days later), 2.91 (>7 days later), 2.17 (sample before notification); the other signs
   move the same way (petechiae 1.98 / 2.19 / 2.52 / 2.41), so there is no sign of entry with the result in hand
   specific to the blood count. Worth: -0.0024 / -0.0026 / +0.0012 ROC AUC when dropped (my windows), the builder's
   0.002. It is in the Ministry's suspected-case definition, and a count at first contact is routine.
   Caveat: "No" mixes "count normal" with "no count done" (the form has codes 1 and 2 only): a recording mix, not a
   class artefact; worth a sentence in the note.
   Remedy: none to the data; the use case's "before or without a laboratory result" should read "before or without
   the dengue test result", since a blood count is a laboratory result.

3. P7, CLEAN-10 / CLEAN-12 on `occupation_cbo`: proxy codes left in, special codes undocumented.
   Evidence: "000000" (8,401 rows) is not set missing (MISSING_CODES lists "0", "", "XXX" only; no CBO occupation is
   000000); it carries 59.5% dengue against 47.4% for the blank occupation, so some unit's fill. SINAN's own codes
   outside the CBO hold 536,623 rows (20% of all rows, 55% of the non-missing occupations): 999991 (206,189 rows,
   median age 14), 999992 (142,528, median 43), 999993 (80,054, median 68), 999994 (26,689, median 34), 999995 (309,
   median 26), 998999 (80,854, median 31, dengue 37.5% against 47.5%). The ages fit the usual SINAN reading (student,
   housewife, retired, unemployed, prisoner); the meaning of 998999 (possibly "occupation ignored") I could not
   confirm from a published table (web searches found no SINAN occupation table; unverified). 1,590 five-character
   codes (1,584 of them "10001") look like codes from another table or with a lost leading digit.
   Remedy (cheap, safe): add "000000" to the missing codes; look up SINAN's occupation table (the dictionary's
   "Tabela de Ocupacao", f23) and decode the 99999x codes into their words, setting 998999 missing if it is
   "ignorada"; note the "10001" level. Keeping the CBO codes themselves as codes is acceptable (a one-to-one code;
   CLEAN-12 would prefer the titles, but a model sees the same partition), with a note.

4. P7, notes only (no change): pregnancy "not applicable" also chosen for 8.2% of women aged 15-49 and 24% over 60
   (a user choice beside the system's auto-fill for men and girls <=10; kept as a level); health regions missing for
   whole states (RR, DF, RJ, TO, AP), structural; residence_country is Brazil on 99.998% of rows (not constant, so
   kept under CLEAN-5); 122 five-digit notifying-unit codes. None needs a change.

Not problems (checked):
* days_onset_to_notification: both ends at or before the prediction point (dictionary f10 "<= notification date";
  0 negative lags); not a span the outcome ends (LEAK-10's span clause). It is a carrier of finding 1, which the
  filter removes.
* The places and the notifying unit: known at notification (USE-6, LEAK-34); their excess beyond local epidemic
  activity is finding 1.
* Signs and diseases decoded Yes/No; schooling in the dictionary's order; proxy codes 9, I, XXX, 0 and blank
  missing as claimed (apart from occupation's "000000").

Judgment record:
Verdict: ship after changes (finding 1 filter or the curator's keep with a note; finding 3 codes).
Validity: LEAK-10 holds for every kept column (dictionary f1-44, measured erasures of f64-72); USE-3 triggered by the
  rows notified after a sample (14.1%), fix by a cohort filter; leukopenia LEAK-10 tested, holds (USE-6).
Quality: CLEAN-10 departure on occupation "000000", CLEAN-12 gap on SINAN's special occupation codes; fix cheap.
For the curator: finding 1 (filter the rows sampled before notification, or keep with a note), finding 2 (wording).

Files: this report; scripts in the run folder.

</details>

<details><summary>Split audit</summary>

SPLIT AUDITOR REPORT: sinan_dengue_case_screening_1m (record sinan_dengue_case_screening), 2026-11-09

VERDICT: right with notes. The regime (temporal by notification date, units and municipalities recurring as known
entities) fits the use case, and every window trains on more than half the rows (71.9%, 78.9%, 90.2%). Three things
to change or write down, ranked below: (1) the two-month gap withholds labels that a twice-yearly refit already has,
which costs 0.026 to 0.037 ROC AUC on the July windows; (2) two of the three windows are off-season, so the mean over
windows gives the off-season two thirds of the weight while it holds 17-25% of a year's notifications, and a
non-contiguous set of windows fixes this within SPLIT-14; (3) all three windows fall in the COVID years, with measured
breaks in the cohort and the inputs. These need a note, since no labelled period after 2021 exists.

Judgment record
  Validity: SPLIT-1 holds (temporal; random split overrates by 0.08-0.18 AUC). SPLIT-9 holds (no shortcut).
            SPLIT-10 triggered: the gap is longer than the refit needs (finding 1, a Should, curator's call).
            SPLIT-13 holds (units recur, part of the task). SPLIT-14 holds. SPLIT-20 triggered twice (findings 2 and 3).
  Weighed: season coverage - (2 of 3 off-season), COVID break - (unavoidable, note), history + (4 pre-COVID seasons).
  For the curator: finding 1 (gap: keep / 1 month / as-of filter) and finding 2 (windows: keep / skip 2020H2 / add 2020H1).

How the numbers were made
  Data: the builder's cached `_clean` output (parquet/clean.parquet, 2,623,839 rows, same windows as the container:
  test 129,189 / 394,414 / 102,639, train pools 2,366,472 / 2,070,124 / 1,887,364, matching the README) joined by
  row index to the prepared raw file for the closing date `DT_ENCERRA` (100% filled, never before the notification).
  Models: LightGBM (300 trees, 63 leaves, native categoricals, the date as days), 300k training rows drawn from each
  train side in one random order (as the _1m sampling does), up to 200k test rows per window; a logistic regression
  on the low-cardinality columns as a second family. Two seeds for the gap runs. Scripts and logs:
  scripts in the run folder.
  Absolute scores are above the builder's probe (it capped train sides at the newest 200k); compare within a table.

FINDING 1. P4, SPLIT-10 (Should, as amended 2026-11-04/05), under SPLIT-1 (Must): the two-month gap withholds labels
a refit at the window start already has; it costs 0.026-0.037 ROC AUC on the July windows.
The label's delay (notification to closing date, the lab-decided cohort):
  median 13-20 days by half-year from 2016H2 (15 in 2021H1, 13 in 2021H2), p90 48-61 days, share over 61 days
  2.9%-7.0% (2016H1 an outlier: 47 / 113 / 21.8%, the start of the new form). The COVID years close faster
  (p90 53-54 days in 2020-2021 against 57-61 in 2017-2019). Confirmed and discarded close alike (median 17 vs 18 days,
  p90 61 vs 61), so the delay barely depends on the outcome. Lab sample to closing: IgM median 16 days, NS1 13,
  RT-PCR 25. The SINAN closing deadline for dengue is 60 days after notification (state notes citing the Ministry's
  guide), so the builder's 2 months is the p90 of the delay and the system's deadline.
What a refit at the window start knows (rows notified in the two months before it, closed before it):
  2021-07-01: 72.8% closed (month -1 52.2%, month -2 84.8%); 2021-01-01: 68.2%; 2020-07-01: 72.0%.
  Training rows still open at the start: no gap 1.74% / 0.52% / 1.84% (builder's numbers confirmed); 1-month gap
  0.85% / 0.14% / 0.81%; 2-month gap 0.36% / 0.07% / 0.31%.
  Selection by the outcome among the newest rows (dengue share of the closed rows against all rows of the last two
  months): 52.6% vs 51.0% (2021-07), 23.3% vs 24.9% (2021-01), 57.2% vs 52.5% (2020-07): -1.6 to +4.7 points, on
  about 5% of a train side.
Cost, LightGBM, mean of two seeds, ROC AUC per window (2021H2 / 2021H1 / 2020H2):
  gap 2 months (shipped)                       0.753 / 0.645 / 0.739
  gap 1 month                                  0.780 / 0.654 / 0.754
  as-of: notified and closed before the start  0.790 / 0.654 / 0.765   (what a refit at the start knows)
  gap 0, labels not yet known included         0.803 / 0.665 / 0.778   (not realistic, an upper reference)
  Seed spread within a cell up to 0.009. As-of minus shipped: +0.037 / +0.009 / +0.026.
  Without the date feature the as-of gain is +0.013 / +0.003 / +0.014, so about 60% of it flows through the date:
  the newest training dates set the level the model carries into the window (April, the season peak, under the
  gap; June under the as-of filter). The rest is the local epidemic's tail: a municipality's dengue rate among the
  labels closed in the two months before a July start scores ROC AUC 0.726 (2021H2) and 0.707 (2020H2) alone,
  against 0.667 and 0.665 from months -4 to -2, which the gap keeps (January: 0.595 both).
Reading against the rules:
  * SPLIT-9: no shortcut. The labels the as-of filter adds were set before the window starts, no row notified after
    the start enters (the filter is on the notification date AND the closing date), there is no patient id, and they
    reach test rows only through codes shared by many patients (unit, municipality), as in
    lt_vehicle_loan_default_prediction.
  * SPLIT-10: its first sentence asks to train on the rows whose outcome is known by the window's start. Here the
    closing date makes that exact. The amendment sets a gap where measurement shows a shortcut (none) or a selection
    by the outcome at the release end. The selection measured here is small (-1.6 to +4.7 points on the newest ~5%), and
    a deployed refit faces exactly the same one. The release itself is complete (2021 closed long ago). The gap at
    the p90 is therefore longer than the collection needs, and it removes the part of the signal that a real refit
    uses most (the late-season local rates). The benchmark then measures a model 2 months staler than the use case
    describes. Precedent on the gap's length: house_sales set one week for a median delay of 6 days (91% within 14),
    roughly the median to p75; sf_permit_time went longer only because a short gap still censored slow permits,
    which is not the case here (confirmed and discarded close alike).
  * The builder's issue 2 measures the open rows but not what the gap costs; the splits_comment says "the two
    months leave 0.07% to 0.4%" without the cost.
Remedies, mildest first (curator's call):
  (a) keep 2 months and add the cost to splits_comment (0.026-0.037 AUC on the July windows, about 0.01 in January,
      against a refit that uses every label closed by the start);
  (b) a 1-month gap (TemporalSplits(..., gap=1)): open training rows 0.14%-0.85%, recovers 58%-100% of the cost by window
      (0.780 / 0.654 / 0.754); the one-line change, close to the house_sales convention;
  (c) the faithful one: train on the rows closed before each window start with no gap, via `_make_splits` with the
      closing date carried as a split helper only, never a feature (as the definitions guide asks for late labels).
      Only if the API can carry a helper column past `_clean`; otherwise (b).
  I lean to (b) or (c). Either way the train pools grow (gap 1: 2.45M / 2.08M / 1.95M) and the floor holds.

FINDING 2. P4, SPLIT-20 (Should) against SPLIT-14 (Must): two of three windows are off-season and weigh two thirds
of the mean; a season-balanced set exists inside SPLIT-14.
Season shape: January-June hold 83% (2016), 69%, 67%, 84%, 83% (2020) and 75% (2021) of a year's lab-decided
  notifications; monthly peak March-May; dengue share by month 13%-67%, highest in April.
Shipped windows: 2021H2 (129k rows, 35.6% dengue, off-season), 2021H1 (394k, 52.0%, season), 2020H2 (103k, 27.2%,
  off-season). The off-season windows hold 37% of the test rows but get 2 of 3 weights in the mean over windows.
Scores differ by season: LightGBM 0.751 / 0.651 / 0.741 (builder's random forest skill 0.444 / 0.289 / 0.426): the
  season window is the hardest, so the mean over windows (0.714) is above the row-weighted mean (0.686) and above
  what a physician meets across a year. Order of families unchanged: LightGBM over logistic by +0.081 / +0.058 /
  +0.084 (linear 0.670 / 0.593 / 0.656). So the effect is on the level and the weighting, not on rankings seen so far.
The builder's claim "yearly windows would leave only two windows above the floor" holds for calendar years (the 2019
  window trains on 25.9%), but not for every season-shaped set:
  * Non-contiguous half-years 2021H2, 2021H1, 2020H1 (skip 2020H2): train 90.2% / 78.9% / 55.4%; two season windows
    and one off-season one, the 6-month horizon and the twice-yearly refit kept; 2020H1 has 502,642 rows, so the
    500k test cap samples it. LightGBM 0.751 / 0.651 / 0.689, logistic 0.670 / 0.593 / 0.626. Declared with
    cutoffs (TemporalSplits(window=6, unit="months", cutoffs=("2020-01-01", "2021-01-01", "2021-07-01"), gap=...)).
    Precedent: perth_house_prices stepped its windows to avoid the COVID months, airqo moved its windows to cover both
    seasons (SPLIT-20, chosen from counts and season coverage, not scores).
  * Four half-years (add 2020H1): two season, two off-season, train 55.4% for 2020H1 with the gap (the builder report
    says 57%; that is the share without the gap, 57.0%). SPLIT-15 asks for 3 at this size; a fourth is allowed but
    keeps the 50/50 weighting.
  * 12-month windows stepping 6 months (2021, July 2020-June 2021, 2020): train 78.9% / 71.9% / 55.4%, each a full
    cycle weighted by volume; LightGBM 0.671 / 0.672 / 0.692 (inside them H1 0.652-0.689, H2 0.737-0.758), logistic
    0.608 / 0.597 / 0.623. Downsides: 2020H2 and 2021H1 tested twice, a 12-month horizon against the declared
    twice-yearly refit, and a pooled AUC across seasons rewards knowing the seasonal base rate. Not recommended.
Remedies, mildest first: (a) keep and write in splits_comment that the off-season windows score higher (0.74-0.75
  against 0.65) and weigh two thirds; (b) recommended: cutoffs 2020H1, 2021H1, 2021H2, decided on season coverage
  (two of three windows in the season that holds 75-84% of the cases), not on the scores (SPLIT-21); (c) four windows.
  Note for the builder's issue 2 option (b): the 2020H1 share is 55.4% with the gap.

FINDING 3. P4, SPLIT-20 (Should): every test window lies in the COVID years; the break is measured, cannot be avoided,
and is not written down.
All three windows (July 2020 to December 2021) follow the COVID onset in Brazil (March 2020). Measured in the data
  (half-years 2016H2-2019H2 against 2020H1-2021H2):
  * lab share of the confirmed cases: 0.20-0.32 before, then 0.40 / 0.44 / 0.60 / 0.41; of all decided: 0.39-0.50
    before, then 0.44 / 0.54 / 0.58 / 0.49. The task's cohort (lab-decided) changed its composition: in 2021H1, 60% of
    the confirmed cases went through a laboratory against 32% in 2019H1. This interacts with the builder's issue 1
    (selection bias): the test cohort is closer to all decided cases than the training cohort is.
  * inputs: fever "Yes" 0.80-0.86 before, 0.73-0.77 in 2020H2-2021H2; leukopenia "Yes" 0.07-0.08 in 2018H1-2020H1,
    0.040-0.043 in 2020H2-2021H2; median age off-season 28-29 before, 36 in 2020H2.
  * not out of band: rows per half-year (2020H2 103k against 57k-128k in earlier H2s), dengue share (2020H2 27.2%
    against 16.6%-40.1%; 2021H1 52.0% against 24.7%-56.0%), and the builder's probe 13 (no quarter |z| >= 3).
  * score, for information only (SPLIT-21: no decision from it): the COVID off-season windows score like the
    pre-COVID 2019H2 window (LightGBM 0.741 / 0.751 against 0.752; 2019H2 trains on 42.2%, below the floor).
The data cannot move the windows out of COVID: the open files of 2022 onward hold no discarded case (builder's size
  check), so 2021H2 is the newest labelled window. The expanding history holds four pre-COVID seasons (2016-2019)
  and at least one full season before every window. A history cut would be decided on scores (SPLIT-21) and is not
  needed.
Remedy: a note (History bullet or splits_comment) that the test windows are the COVID years, with the measured shifts
  (laboratory share of confirmed cases doubling, fewer fever and leukopenia entries). Finding 2 (b) also brings in
  2020H1, whose rows are about half from before mid-March 2020 (January-February are 37% of them).

CHECKS THAT PASS
* Regime (SPLIT-1, SPLIT-3, USE-10, SPLIT-13): a physician screens each new suspected case at notification. The
  patient is a new entity (no id, repeated notifications about 0.1%), and the unit and the municipality are known
  entities whose history is legitimate. On the full windows the notifying unit was seen in train for 96.8% / 95.2% /
  96.7% of test rows (the probe on the _1m frame: 94.9%), the municipality for 99.5%-99.9%. New units score lower
  (LightGBM 0.640 / 0.575 / 0.686 against 0.754 / 0.654 / 0.742 for seen units) but are 3.2% / 4.9% / 3.3% of the test
  rows. Temporal is the right regime and grouping by unit would test a case the use case rarely meets.
* SPLIT-5 (the source's split is a claim): Bohm et al. 2024 use a random 70/30 split. A random split over 2016-2021
  scores LightGBM 0.873 / 0.833 / 0.822 on the same test periods against 0.751 / 0.651 / 0.741 under the windows: a
  random split overrates by 0.08-0.18, since epidemics cluster in place and time. The temporal split is right.
* SPLIT-9: no row is in train because its outcome came early (the train side is cut on the notification date), and
  no label of a test row's own entity is set after its prediction point (no patient id; exact copies across the split
  0.6% of test rows, 0.0% with the same date, mostly different patients per the builder's birth-date check).
* SPLIT-11, SPLIT-14, SPLIT-15: expanding train sides, newest window first; 71.9%-90.2% of the rows; 3 windows.
* Window sizes (SPLIT-17): 103k-394k rows, smallest class per window 27,894 or more; all under the 500k test cap.
* The _1m sampling: a random 1M of each train side in one order, every test window whole; the sampling draws from all
  history, so the last two months are about 5% of a train side (the gap finding is measured at that share).
* Time column: notification date (DT_NOTIFIC), the prediction point; 2016-01-03 to 2021-12-31; no rows outside.

Sources: SINAN dengue closing deadline of 60 days after notification (Mato Grosso technical note on SINAN indicators,
https://www.saude.mt.gov.br/storage/old/files/nota-tecnica-para-orientacao-de-como-calcular-os-indicadores-de-acompanhamento-do-sinan-[61-190510-SES-MT].pdf;
Rio Grande do Sul Portaria 21/2025, https://saude.rs.gov.br/upload/arquivos/202501/13110409-portaria-21-2025.pdf);
COVID and dengue surveillance in Brazil (PLOS NTD 2024 interrupted time series,
https://www.ncbi.nlm.nih.gov/pmc/articles/PMC11709241/; https://www.ncbi.nlm.nih.gov/pmc/articles/PMC9620889/):
underreporting and diagnostic overlap in 2020-2021, varying by state.

</details>

<details><summary>Domain practitioner</summary>

DOMAIN PRACTITIONER REPORT: sinan_dengue_case_screening (folder sinan_dengue_case_screening_1m), 2026-11-09

Actor played: a physician at a Brazilian health unit, and the municipal surveillance team that closes SINAN
notifications, at the notification of a suspected dengue case, before any laboratory result.

VERDICT
Fit: APPROXIMATE (agree with the builder; the reason needs rewording). One sentence: the inputs are exactly what the
notification form holds when I fill it, but the decision the task_summary names does not exist in Brazilian practice
(every suspected case is managed as dengue by risk group, whatever the confirmation), and the labelled rows are the
tested half of the notifications, while the decision a lab-truth model really serves (closing the untested half, or
choosing whom to test) acts on the other half.
Metric scores the decision: PARTLY. ROC AUC fits a screening score with no fixed threshold (MET-6, MET-8), but it is
pooled over every unit and week of a half-year, so it credits ranking places and seasons, which I already know; and
the surveillance decision acts on the level of the probability (log loss).

1. THE DECISION, CHECKED AGAINST THE MINISTRY'S PROTOCOL (USE-1, USE-5, USE-9)
- Ministério da Saúde, "Dengue: diagnóstico e manejo clínico, adulto e criança", 5th ed. 2016 (the protocol in force
  for 2016-2021, read in full text): every suspected case is staged into groups A-D by alarm signs, bleeding and risk
  conditions, and treated by its group. Group A: "Os exames específicos para confirmação não são necessários para
  condução clínica. Sua realização deve ser orientada de acordo com a situação epidemiológica." So the physician
  does not decide "whether to manage and follow it as dengue": I manage every suspected case as dengue, and the lab
  confirmation is a surveillance matter. The use_case text of task_summary ("decides whether to manage and follow it
  as dengue before or without a laboratory result") names a decision I do not take.
- The decisions a lab-confirmation probability does serve:
  (a) the municipal surveillance team closing notifications without a laboratory result: in an epidemic "a
      confirmação pode ser feita por meio de critério clínico-epidemiológico, exceto nos primeiros casos da área"
      (manual 8.4), and a case without a test may be discarded when "investigações clínica e epidemiológica são
      compatíveis com outras doenças" (8.5). This is 57% of the decided notifications of 2016-2021 (my count below).
      The team acts on the probability's level: it closes each case and counts the confirmed cases per municipality
      and week.
  (b) choosing whom to test when tests are rationed (state notes: about 1 in 10 suspected cases sampled in an
      epidemic, ES 2023; SP's emergency plan suspends serology), and
  (c) the physician's differential diagnosis: a low dengue probability sends me looking for something else
      (chikungunya, Zika, leptospirosis, bacterial infection; COVID-19 in all three test windows).
  Recommendation (USE-9): reword use_case to (a), the surveillance team at notification estimating which suspected
  cases are dengue, to close the untested ones and to steer testing; keep Bohm et al.'s screening aid as the
  physician's secondary use (differential diagnosis, c). The fit stays approximate under either actor (section 3).

2. INPUTS AT THE PREDICTION POINT (USE-3, USE-6)
Would I have each kept input at notification?
- 14 signs and 7 diseases: yes, the form's clinical section, filled when I see the patient (93% same day, builder).
  The dictionary marks each sign "Campo obrigatório" with 1 Sim / 2 Não only, so "No" mixes "absent" and "not
  looked for"; a recording fact of the form, not a leak.
- Leukopenia (builder issue 3): yes, for most of the patients where it matters. The 2016 protocol makes the blood count
  "obrigatório para todos os pacientes" of group B (petechiae or a positive tourniquet test, comorbidities, infants,
  pregnant women, over 65), collected at the visit with the result "em até duas horas, ou no máximo quatro horas";
  group A "a critério médico". Only 5.4% of the laboratory cohort carry Yes (3.7% of the clinical-epidemiological
  ones), far below the leukopenia rate of dengue patients with a count, so "No" mostly means no count. Keep, option
  (a) of issue 3: a routine count at the first visit, not the dengue test that sets the label.
- Tourniquet test: yes, bedside. Age, sex, pregnancy, race or colour, schooling, occupation: yes, notification
  section. Notifying unit, municipality, health region, residence: yes (the unit is me). Days since onset: yes, I
  ask it. Notification date: yes.
- Nothing kept is unavailable to me. The open concern stays the builder's: SINAN keeps a record editable until
  closing, so a sign entered with the result in hand cannot be excluded (no edit history in the open files).
What I would always have and the data lacks (ranked by how much it changes the task):
- The current local epidemic activity: how many notifications my municipality had in the last weeks and, from the
  bulletins, the recent positivity, and which arboviruses co-circulate. The data gives only place and date; with a
  two-month gap and a random 1M sample of all history, a model learns each place's static rate and the calendar, not
  the phase of this season. This is the input a surveillance team uses most for the clinical-epidemiological
  criterion. An expert would add label-free lag features (notifications in the municipality in the 7 and 28 days
  before the notification date, counted over all notified cases, tested or not, and the chikungunya and Zika
  notifications) (USE-6: known at notification). A sizeable change; for the curator.
- The platelet count and haematocrit from the same blood count (the form only has leukopenia at notification;
  platelets and haematocrit appear as alarm signs, post-notification, rightly dropped). A gap of the source, not of
  the curation.
- Fever's measured temperature and the NS1 rapid test (where the unit has it, it is the result itself; rightly out).

3. TARGET AND COHORT (USE-5, USE-8, selection.md "Selection bias")
- The target is lab-confirmed dengue (10-12) vs discarded (5) among laboratory-closed notifications. For the
  surveillance decision (a) this is the right truth: the clinical-epidemiological closings are the team's own
  judgement, so training on them would teach the model the team's habits. So the cohort choice (builder issue 1,
  option a) is right, and option (b) (add the clinical-epidemiological closings as labels) would make the label partly
  the decision being automated.
- The selection is real but moderate. My counts on the six yearly files (work_domain_practitioner/sel.log;
  7,028,961 decided notifications of 2016-2021):
    laboratory 42.4%, clinical-epidemiological 56.9%, clinical 0.7%;
    dengue share 47.7% among the laboratory closings vs 64.0% among the clinical-epidemiological ones;
    hospitalised 5.0% vs 2.3%; petechiae 9.1% vs 7.1%; leukopenia 5.4% vs 3.7%; rash 19.0% vs 17.2%;
    laboratory share by a state's own monthly volume: 50.6% in its quietest quarter of months, 40.3% in its busiest
    (row-weighted); quarterly volume vs laboratory share r = -0.34.
  So the tested cases are a bit sicker, more often off-season and outside peaks, and more often negative: the
  manual's rule (test the first cases of an area and the severe ones; confirm the rest clinically in an epidemic)
  shows in the data. In the deployment population of (a), the untested half, the base rate is higher and the epidemic
  phase later. Ranking probably transfers; the probability level would not.
- The negative class is "test negative", not "not dengue": an IgM drawn before day 6 or an NS1 after day 5 misses true
  cases (manual 7: serology "a partir do sexto dia", antigen "até o quinto dia"), and the 2016 Zika epidemic made IgM
  cross-react. The label's noise therefore depends on days_onset_to_notification, a kept input. Worth a sentence in
  the notes (USE-5), not a change.
- Marker: `Selection Bias` applies (USE-8, the lt_vehicle_loan_default_prediction precedent: the actor would want the
  untested cases and has no label for them). The "selection is how the label comes to exist" exception of
  selection.md (heart_disease) does not apply, because my decision (a) is about the cases that were NOT tested.
- Fit_reason as written ("in deployment the model meets every suspected case, most of which are closed on clinical and
  epidemiological grounds") is accurate; add that the untested cases are more often dengue (64% vs 48%) and come from
  epidemic peaks.

4. ROW, SPLIT AND TEST DATA (USE-10, SPLIT-*)
- One row = one notification = one decision: yes. Repeated notifications of one patient are about 0.1% (builder).
- The unit and the municipality recur (94.9% and 99.5% of test rows seen in train): a known entity, as in my work
  (USE-10); temporal by notification date is right.
- The test windows are what I would face (the next half-year), but all three (2020H2-2021H2) fall in the COVID-19
  pandemic: notification and testing changed (the laboratory share rose to 53-58% in 2020Q3-2021Q2 against 37-48% in
  2016-2019), and COVID-19 entered the differential. No later windows are possible: the open files of 2022-2026 hold no
  discarded case (builder), so the task is frozen to 2016-2021. Name the pandemic in splits_comment.
- Windows (builder issue 2): half-years are a sensible refit cadence for a surveillance model (before and after the
  season). Keep option (a).

5. WOULD I USE THIS MODEL? (measured, work_domain_practitioner/strat.log)
LightGBM (300 trees, newest 300k training rows before each window minus 2 months, not the shipped random 1M), the
three test windows 2020H2 / 2021H1 / 2021H2:
- all features: pooled ROC AUC 0.735 / 0.664 / 0.749; ROC AUC within notifying unit x month (pairs-weighted) 0.586 /
  0.604 / 0.581.
- without the 8 place columns and the date: pooled 0.642 / 0.658 / 0.627; within unit x month 0.585 / 0.621 / 0.586.
So all the value of the place and date columns lies in ranking units and weeks against each other; for the patients
in front of me at my unit this month, the model discriminates at about 0.59-0.62, close to what the WHO clinical case
definition achieves (pooled sensitivity 93%, specificity about 30%; Raafat et al. 2021). This is a sound, honest
signal level for clinical dengue diagnosis, and it is why I trust the data more than Bohm et al.'s ROC AUC 0.985 on
symptoms alone (a balanced sample of "complete records", implausible against the literature).
- Calibration: with all features the 2021H1 window predicts a mean 0.258 against an observed 0.520 (log loss 0.896 vs
  0.692 for the training-share constant); without place and date 0.495 (log loss 0.656). The builder found every
  family's log loss worse than the constant. As the surveillance team I could not use these probabilities to close
  cases or count them without re-calibrating each season.
- As a physician I would not change management on it (the protocol does not let me); I might use it to widen the
  differential when it is low. As the surveillance team I would use it to rank untested cases and to steer testing
  if it were recalibrated to the current positivity. What would make me distrust it: the season shift above, the
  tested-only training cohort, the unit codes standing for each unit's testing habits (the unit alone scores 0.657).

6. METRIC (MET-1, MET-5, MET-6, MET-8, MET-9, MET-10): PARTLY
- The fallback is correctly reasoned: Bohm et al. report six metrics side by side (MET-5); no threshold or cost is
  fixed anywhere (MET-6, MET-7; the Ministry gives no threshold, and my threshold moves with the epidemic phase); the
  classes are balanced overall (47%), so no AUPRC case (MET-9).
- What ROC AUC misses for my decision (MET-1, unit of action):
  (i) it is pooled over a half-year of all units and weeks: 0.15 of the 0.73 pooled AUC is the across-unit and
      across-week ranking, which I already know; the physician's unit is a unit-day, not Brazil-half-year;
  (ii) the surveillance team acts on the probability level (closing at a fixed rule, counting cases per
      municipality-week), which only a proper rule scores.
- The metric I would choose: log_loss (MET-8, a strictly proper rule) if the actor is the surveillance team, as I
  recommend in section 1; it scores the level I act on and penalises the seasonal miscalibration that would mislead
  me. Caveat for the curator: on these windows every untuned family is worse than the constant (builder), so log loss
  ranks methods largely by how they handle the prior shift between seasons; that is the real difficulty of my
  deployment, but it makes the benchmark partly a prior-shift test. If the curator keeps the physician actor,
  roc_auc as declared is acceptable (no threshold, MET-8). A within-unit-month AUC would score the physician's decision
  best but is no standard metric (MET-12); not proposed.

GAPS RANKED BY HOW MUCH THEY CHANGE THE TASK
1. The named decision is not taken in practice (USE-1, USE-5): management never waits on confirmation; reword to the
   surveillance team's closing and testing decision (USE-9). Changes what the task means and which metric scores it.
2. Selection to the tested half (USE-8, `Selection Bias`): the deployment population of the real decision is the
   untested half, with 64% vs 48% dengue and more epidemic-peak rows. Keep the lab cohort (issue 1 a), approximate.
3. Missing epidemic-phase input (USE-6): no recent local notification counts; models see place and calendar only.
   Label-free lag features would mirror what I know.
4. Season and pandemic shift in the test windows: probability levels do not carry over (2021H1 mean predicted 0.26 vs
   observed 0.52 with all features); all windows in COVID-19 years.
5. Label = a test result whose sensitivity depends on days since onset (USE-5): noise tied to a kept input; a note.
6. Leukopenia "No" mostly means no count (5.4% Yes): keep (issue 3 a), note it.

WHAT A DOMAIN EXPERT WOULD CHANGE
- Reword task_summary.use_case (and fit_reason) to the surveillance team closing untested notifications and steering
  testing, citing manual 8.4-8.5; the physician screening aid as a secondary reading.
- Consider log_loss as the metric under that actor (MET-8), with the prior-shift caveat written in the reason.
- Consider label-free epidemic-activity features (municipal notifications in the prior 7 and 28 days, all
  arboviruses), USE-6.
- Notes: the COVID-19 period of all test windows; the negative class as "test negative" with timing-dependent
  sensitivity; leukopenia's "No" = mostly no count; the laboratory share falling at epidemic peaks (numbers above).
- Keep: the lab cohort, the dropped post-notification fields, the places and unit, leukopenia, the half-year windows.

SOURCES
- dataset.py, README.md and the record of sinan_dengue_case_screening (the working tree); builder_report.md; the data
  dictionary dic_dados_dengue.txt (fields 22, 35-36: leukopenia and tourniquet test "Campo obrigatório", 1 Sim 2 Não).
- Ministério da Saúde, Dengue: diagnóstico e manejo clínico, adulto e criança, 5th ed., 2016 (sections 6.1-6.2, 7,
  8.1-8.5), https://repocursos.unasus.ufma.br/PPU/dengue/SE_UNASUS_0002_DENGUE/recursos/dengue_diagnostico_e_manejo_clinico_2016.pdf
- Bohm et al. 2024, BMC Public Health 24:1573, https://pmc.ncbi.nlm.nih.gov/articles/PMC11167742/ (use case, cohort,
  metrics reported side by side, AUC 0.985 on a balanced sample).
- Raafat et al. 2021, PLoS NTD 15:e0009359, https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8102005/ (WHO clinical
  definitions: sensitivity 93%, specificity 29-31%).
- SESA Espírito Santo, Nota Técnica GT Arboviroses 01/2023 (about 1 in 10 suspected cases sampled in an epidemic),
  https://mosquito.saude.es.gov.br/Media/dengue/Notas-Tecnicas-Alertas-Epidemiologicos/NOTA%20T%C3%89CNICA%20GRUPO%20DE%20TRABALHO%20DAS%20ARBOVIROSES%20012023%20-%20GEVSSESAES.pdf
  (search-result summary, not read in full); SES São Paulo dengue plan (serology suspended in the emergency phase;
  search-result summary).
- My measurements: work_domain_practitioner/sel.py, sel.log (cohort selection by criterion, quarter, state-month
  volume); strat.py, strat.log (pooled vs within unit-month ROC AUC, log loss, Brier, calibration).

</details>

<details><summary>Blind review</summary>

BLIND REVIEW: sinan_dengue_case_screening
Inputs used: clean_room/data.parquet (200,000-row sample of 1,679,297), clean_room/task.md, the public
SINAN dengue page on dadosabertos.saude.gov.br and the SINAN Online dengue data dictionary PDF (text pulled out by
hand because no PDF tool was installed). I opened no other local file.
Scratch scripts: scripts in the run folder.

VERDICT: Include with changes. This is a real public-health screening task with honest, notification-time
features, non-trivial signal and plenty of rows. But the label definition is undocumented, missing symptoms look
like they were turned into "No", and health region is blank for five whole states. These need fixing or
documenting first.

WHAT THE TASK IS
A suspected dengue case is notified to SINAN (Brazil's national notifiable-disease system). From the
notification form alone (place, reporting health unit, demographics, 14 signs and symptoms, 7 comorbidities,
age, delay from symptom onset), predict whether the case will end up classified as confirmed dengue.
Who would use it: municipal or state surveillance teams. They could rank cases for limited lab testing, or estimate
how many of today's "probable" cases will be confirmed (nowcasting the true burden) before cases are closed weeks
later. It is a real use. Data run from 2016-01-03 to 2021-12-31, in date order. Overall 46.9% Yes.

SIGNAL (LightGBM, 3 expanding temporal windows on the sample: 70/80/90% cut points, test windows starting
2021-01-25, 2021-04-09 and 2021-06-05)
  all features:             AUC 0.675 / 0.747 / 0.792
  clinical + demographics:  AUC 0.617 / 0.641 / 0.645
  geography + season only:  AUC 0.635 / 0.693 / 0.767
  notifying_unit only:      AUC 0.612 / 0.662 / 0.673
  Share of gain: notification_municipality 0.22, notifying_unit 0.22, residence_municipality 0.16, health
  regions 0.15, day of year 0.08, rash 0.04.
  So there is signal, the task is far from trivial, and there is room for models to differ. Most of the
  signal is "where and when was the case notified", not the clinical picture. That is fair at prediction
  time, but it means the benchmark mostly rewards handling of high-cardinality categories under drift.
  Monthly confirmation rate ranges 0.12-0.665 (std 0.147). By year: 2016 0.43, 2017 0.23, 2019 0.53. Expect large
  calibration and prevalence shift between windows (test prevalence in my windows: 0.50, 0.57, 0.38).

CONCERNS, MOST TO LEAST SERIOUS

1. The label definition is undocumented, and the row filter is heavy and unstated.
   Evidence: the dictionary defines classi_fin as "1 Confirmado 2 Descartado 8 Inconclusivo" (older years use
   10/11/12 for confirmed and 5 for discarded). It defines criterio as "1 Laboratório 2 Clínico-epidemiológico 3 Clínico".
   task.md says neither which codes map to Yes/No nor whether inconclusive, unclosed or ignored cases
   were dropped. Only 1.68M rows remain for 2016-2021, well under the several million dengue notifications SINAN
   holds for those years (my recollection, not checked here), so a strong filter was applied.
   It matters because "confirmed by the clinical-epidemiological criterion" is assigned on epidemic context
   (place and time). If those confirmations are in the Yes class, the geography and season features partly
   recover the surveillance rule rather than the disease. Restricting to closed cases is also a selection on
   outcome availability.
   Change: state the exact classi_fin and criterio filter in task.md. Preferably restrict Yes and No to
   laboratory-criterion cases, or keep the criterion and report it. Say that open and inconclusive cases are
   excluded.

2. Missing symptoms appear to be coded as "No".
   Evidence: all 14 symptom columns have 0.00% missing, although SINAN symptom fields are often left blank in
   practice. 5.9% of rows have every symptom "No". Those rows are confirmed MORE often (0.567) than rows with any
   symptom (0.463), which is implausible for a real absence of fever, headache and the rest. The all-No share is 19.6% in 2016 against
   3-5% in later years. Comorbidities likewise have almost no NaN.
   Change: if the raw field was blank, keep it as missing (NaN), not "No". At least add a "symptoms not
   recorded" flag.

3. Health region is blank for whole states because of a mapping gap.
   Evidence: notification_health_region and residence_health_region are 100% NaN for AP, DF, RJ, RR and TO
   (7.2% / 6.85% of rows). RJ certainly has health regions. This comes from preparation, not from the data.
   Change: fix the municipality-to-region lookup, or drop the two region columns. Municipality already carries
   the information.

4. Strong prevalence drift, and one documented reporting break.
   Evidence: the yearly confirmation rate swings from 0.23 to 0.53. The source page says "Since 2020, Espirito Santo
   has used e-SUS Vigilancia em Saude". ES rows drop from 1,068 (2019) to 29 (2020) in the sample.
   All three test windows probably fall in 2021, the last year of data.
   Change: that is acceptable for a temporal task, but document it. Consider dropping ES for 2020 onward, or
   noting the gap. Report a ranking metric (AUC or log loss) per window rather than accuracy.

5. Implausible values.
   Evidence: days_onset_to_notification goes up to 365, and 2.2% of rows are over 30 days and 0.75% over 60. Such
   long delays from symptom onset are not plausible for an acute dengue notification and are likely date typos.
   age_years goes up to 116, with 20 rows over 100.
   Change: set delays over about 60 days and ages over about 105 to NaN, or leave them and document them.

6. Minor preparation issues.
   - residence_country is constant (199,998 of 200,000 rows = "1"). Drop it.
   - notifying_unit has 21,574 levels in the 200k sample and notification_municipality has 4,065.
     Keeping them as categories is right, but they will dominate the benchmark. occupation_cbo is 63.7% NaN, and its
     99999x codes are placeholders (student, homemaker, retired and similar). That is acceptable as a category.
   - There are 25 exact duplicate rows and 593 duplicates when the date is ignored. With no patient ID, I cannot
     check for repeat notifications of the same person across train and test. The impact is likely small.

LEAKAGE CHECK
I found no post-outcome columns: no lab results, hospitalisation, criterio, closing date, evolution or
warning-sign block. All features come from the notification and investigation-opening section of the form.
Leukopenia comes from a blood count, but the dictionary calls it a "Sinal clínico" on the notification form, so it
is available at notification. The temporal split matches real use.

COULD NOT CHECK
- The raw SINAN files: I did not download the multi-GB yearly files. So I could not confirm the classi_fin and
  criterio mapping, the row filter, or whether blank symptoms became "No" (concern 2 is inferred).
- The exact test-window boundaries used by the benchmark (task.md gives only "3 test windows"). My
  windows are my own.
- Whether repeat notifications of the same patient exist (there is no ID).
- Anything on the full 1.68M rows: all numbers above come from the 200k sample.

</details>

<details><summary>Task gamer</summary>

TASK GAMER REPORT: sinan_dengue_case_screening (dengue_confirmed, ROC AUC, 3 temporal windows)

Verdict: you can only game this task a little. Nothing here recovers the label. The largest gain (+0.018 to +0.028 mean AUC) comes from the labels of the two-month gap rows, which data.parquet ships. The second gain (+0.005 to +0.006) comes from counts of notifications made after each test row.

All scores below are ROC AUC from score.py on the shipped splits, listed per split as r0f0 / r1f0 / r2f0.
- r0f0 tests Jul-Dec 2021, r1f0 tests Jan-Jun 2021, r2f0 tests Jul-Dec 2020.
- Each training set holds 1,000,000 rows and ends two months before its test window.
- Model: LightGBM with native categoricals, 300 rounds, learning rate 0.1, 63 leaves, 4 threads. No subsampling.
- notification_date is dropped as a raw input.
- Scripts are in work/. Every score is logged in work/results.tsv.

Reference models
- Honest baseline (work/baseline.py; features() minus date): 0.7478 / 0.6586 / 0.7354, mean 0.7139.
- Noise check: the baseline plus a random column, three seeds: r0f0 0.7473-0.7480, r1f0 0.6585-0.6587, r2f0 0.7352-0.7360. The spread is about ±0.0005 per split.
- Better honest model "hbest" (work/exp_best.py hbest): 0.8007 / 0.6991 / 0.7552, mean 0.7517. Every addition is known at the prediction point:
  - week of year and month: +0.022 mean
  - counts of earlier notifications in the past 7 and 28 days by residence municipality, notifying unit and state, strictly before the notification day: +0.009
  - confirmation rates from training labels by municipality, unit and state over a 90-day window ending at least 61 days before the row, and never after the training cut: +0.0065

EXPLOITS RANKED BY GAIN

| # | Exploit | Script | Honest score (mean) | Exploited score (mean) | Gain per split | Does a deployed model have it? | Fix |
|---|---|---|---|---|---|---|---|
| 1 | Train on the labels of the gap rows (dated between the training cut and the test start; 128k / 30k / 53k rows) | work/exp_best.py hbest+gaprows; work/exp_rows.py hon gap | hbest 0.7517 | 0.8383 / 0.7150 / 0.7858 = 0.7797 | +0.038 / +0.016 / +0.031 (vs hbest); +0.030 / +0.001 / +0.023 (vs the weaker honest model 0.7453) | Partly. In the 2017 source, the time from notification to closure has median 18 days, 75% within 35 and 90% within 57. At test start a deployed model knows most labels from the first gap month and few from the second. Labels from the first gap month alone give +0.015 / -0.005 / +0.010 (mean +0.0066). | Do not ship labels for rows after the training cut. Either drop the gap rows from data.parquet or blank their target. |
| 2 | Counts of the same municipality, unit and state in the next 7 and 28 days (test-window composition, read from the test rows' own features) | work/exp_best.py hbest+future; work/exp_counts.py exploit_futurecounts | hbest 0.7517 | 0.8067 / 0.7072 / 0.7602 = 0.7581 | +0.006 / +0.008 / +0.005 (vs hbest); +0.0075 / +0.0074 / +0.0012 (vs 0.7453). About 10 times the noise spread. | No. These are notifications made after the prediction. | Score the test rows one at a time, or in daily batches, so that no test row sees later test rows. Otherwise accept a gain of this size. |
| 1+2 | Both together | work/exp_best.py hbest+gaprows+future; work/exp_combo.py | hbest 0.7517 / baseline 0.7139 | 0.8417 / 0.7204 / 0.7889 = 0.7837 | +0.041 / +0.021 / +0.034 (vs hbest) | Mostly no. | The fixes for 1 and 2. |

Finding 1: gap-row labels
The split leaves a two-month gap before each test window, which stands in for label delay. data.parquet still carries the gap rows with their labels.
- The gap rows sit right next to the test window in time, so they carry the current local epidemic and lab-testing regime. That is the main thing the model lacks: the confirmation rate by state and year swings from 0.01 to 0.75.
- Adding the gap rows to training is the largest gain. The gain comes mostly from the second gap month (first month only +0.0066 against all gap rows +0.0177 on the same features), and a deployed model would mostly not yet have those labels.
- Using the gap labels only in the lagged-rate features gives +0.007 / +0.007 / +0.008 (work/exp_labels.py gap vs honest).
- Mildest fix: drop the gap rows from what participants see, or blank their target. A harness that passes only the training rows already closes this.

Finding 2: future counts from the test window
Confirmation tracks local outbreak intensity. Counting a municipality's or unit's notifications in the 7 and 28 days after a row measures where an outbreak is heading. Inside the test window, those counts come from the test features themselves.
- Gain: about +0.006 mean on top of the honest past counts.
- Same-day counts add nothing: -0.0001.
- Future repeat-notification "twins" (rows with identical features, or the same person-like key, within 30 days) add nothing: -0.0002.
- Mildest fix: none needed beyond accepting it. A strict fix scores the test rows in time order without batch access.
- Caveat, including for the honest past counts: the kit holds only cases later closed by lab criterion (see "Preparation" below). Even the past counts are therefore counts of cases whose lab closure lies in the future. A deployed model would count all notifications, which are about 2.8 times as many in 2017 (518,483 against 186,642 lab-closed). Whether past counts of all notifications give the same +0.009 would decide whether that part is honest. I could not check this without the 2016 and 2018-2021 source files.

FLAWS THAT HURT AN HONEST MODEL

| What is wrong | Honest choice | Honest score as shipped | Score with the honest choice | Fix |
|---|---|---|---|---|
| The 1M training cap keeps old rows at 80-91% but recent rows at only 42-49% (r0f0: Jul 2020-Apr 2021 kept at 42%; r1f0: Jul-Oct 2020 at 48%). Selection does not depend on the label: the rate is 0.479 among kept rows and 0.469 among dropped rows. | Train on all rows up to the cut (work/exp_best.py hbest_allpre) | hbest 0.8007 / 0.6991 / 0.7552 = 0.7517 | 0.7999 / 0.7046 / 0.7552 = 0.7532 (+0.0015; mixed: -0.001 / +0.0055 / 0) | Subsample uniformly or weight toward recent rows. The effect is small. |
| The training set is dominated by older years (2016-2019) whose confirmation regime differs | Train on the last two years only (work/exp_rows.py hon recent2y) | 0.8041 / 0.6791 / 0.7528 | 0.7926 / 0.6861 / 0.7590 (mixed: -0.012 / +0.007 / +0.006) | None. A modelling choice, not a task flaw. |

PREPARATION (the kit compared with the published 2017 file, DENGBR17.csv)
- I matched kit rows to the source on notification date, notifying unit, residence municipality, sex and age. 99.75% of the kit's 2017 rows match, and 96.7% match a single source row. On the matched rows, CLASSI_FIN reproduces the label exactly: 5 = No; 10, 11, 12 = Yes.
- The kit is the source filtered to CRITERIO == 1 (closed by laboratory) and CLASSI_FIN in {5, 10, 11, 12}, then subsampled at about 53% at random. In 2017 that is 99,083 of 186,642 rows, at the same rate for both classes.
- Dropped: cases confirmed or discarded by clinical-epidemiological criterion (252,751 rows in 2017), inconclusive cases (8) and cases under investigation (3).
- This filter selects on a variable decided after the prediction point. At notification, nobody knows that a case will be lab-closed. The task therefore really asks "will a case that ends up lab-tested be positive?", not "is this suspected case dengue?". The filter applies to train and test alike, so I found no score exploit in it.
- Mildest fix: state this population in task.md. Alternatively, keep all closed cases and put the criterion in the target definition.
- Symptom "No" values are explicit 2s in the source, not blanks recoded to No.
- Espirito Santo is almost absent in 2020 (239 rows): per the portal, the state moved to e-SUS VS. This comes from the source, not from the kit's preparation.
- Looking up test rows in the published source works (99.75% match, exact labels). This is not ranked. Also not ranked: data.parquet itself ships the test labels, so any score is reachable by reading them; the benchmark must hide them.

ATTACKS THAT FOUND NOTHING
- Row order. Rows are sorted by date and shuffled within each day. Next-row label agreement within a day is 0.5384 against 0.5387 expected. The AUC of the within-day position is 0.5003; within unit-day it is 0.516, which is not usable.
- Format and missingness. Features built from NA flags, age unit (fractional age = months or days), occupation sentinel codes 9999xx, leading zeros in unit codes, string length and residence differing from notification municipality score 0.546 mean when fitted alone (0.590 with symptom counts, which are signal). Added to the baseline they give +0.0010 mean (0.7149 against 0.7139; noise ±0.0005).
- Exact copies across the split. 0.55-0.84% of test rows have a training row with identical features except date. The copy's label gives an AUC of 0.79-0.87 on those few rows, too few to move the total. Person-like keys (unit, age, sex, residence, race, schooling, occupation, pregnancy) find a match for 13-18% of test rows, but the copy label gives an AUC of only 0.63-0.71, which is ordinary signal.
- Twins and repeat notifications, past or future 30 days: +0.000 / -0.0002.
- Each feature alone, using its training-set target mean: notifying_unit is best at 0.718 / 0.630 / 0.708, below the full model. A deployed model has the unit, so this is signal. No other feature comes close.
- Transforms over all rows: none. Age and days_onset_to_notification are raw values, with no scaling, ranks or bins.
- A lookup formula or shallow tree: nothing recovers the target. The best single column is still 0.03 AUC below the full model.
- Web search turned up related SINAN dengue screening work (rfsaldanha.github.io/talks/dengue_class.html; BMC Public Health 2024, doi 10.1186/s12889-024-19083-8). It mentions no "magic feature" or leak beyond the confirmation-criterion issue already covered above.

NOT CHECKED
- Whether past counts over all notifications (not only lab-closed ones) keep the honest +0.009. This needs the 2016 and 2018-2021 source files.
- The closure delay outside 2017, which decides how many gap labels a deployed model would really have.
- Hyperparameter tuning. All comparisons use the same untuned LightGBM.

</details>

<details><summary>Precedent check</summary>

PRECEDENT CHECKER REPORT: sinan_dengue_case_screening (folder sinan_dengue_case_screening_1m), 2026-11-09

Read: principles.md (Strengths, Conflicts, Tensions, Exceptions and amendments, Consistent judgement), use_case.md
USE-3, USE-8, USE-9 (and Cases), selection.md "Selection bias", splits.md SPLIT-10, SPLIT-14, SPLIT-15, SPLIT-18,
SPLIT-20, SPLIT-21 (and Cases), leak_checks.md LEAK-10 (clauses and Mechanisms rows), LEAK-18 to LEAK-20, LEAK-38,
cleaning_features.md CLEAN-10, CLEAN-12, CLEAN-14 (and Cases), evidence.md EV-4, all from the working tree; the
definition, the record, the builder report, register.json (flags and the decisions behind them); the records and
definitions of the precedents named below; the same-batch definitions of rais_employment_separation_1m,
chile_school_dropout_mineduc_1m, wioa_employment_after_exit_1m, ny_wcb_assembled_claims_1m and
ppnn_ecmwf_t2m_postprocessing_germany_1m, and the precedent-checker reports of rais, chile and ppnn; the column
auditor, domain practitioner and blind reviewer reports of this panel, and the claim auditor's work log a2_typing.log.
Two small counts of my own on the builder's string copies of the yearly files (scripts in the run folder):
which closing criterion the tested notifications got, and SINAN's duplicate mark. Nothing in the repository edited.

SUMMARY
  D1 lab-decided cohort, fit approximate, `Selection Bias` (USE-8) ... CONSISTENT (sdss_17, tunisian, lt_vehicle,
                                                                    the 2026-10-27 group). USE-9 not recorded: add it.
  D2 three half-year windows, two off-season (SPLIT-14, SPLIT-20) .... CONSISTENT (SPLIT-14 Must over yearly windows;
                                                                    rain_in_australia, airqo). Missing note: all three
                                                                    windows are COVID-19 years (SPLIT-20, perth).
  D3 leukopenia kept (LEAK-10) ...................................... CONSISTENT (traced: no late-entry signal);
                                                                    reword the use case.
  D4 exact copies kept as natural repeats (LEAK-18) .................. CONSISTENT for distinct patients (ai4d,
                                                                    bank_marketing); DEPARTS WITHOUT A STATED REASON
                                                                    for the one-patient copies (LEAK-19). Prompt 1.
  D5 CC BY-ND licence as a one-line note (EV-4) ...................... CONSISTENT (2026-10-21 rule; chile's draft is
                                                                    the one that departs).
  D6 place codes and the occupation (CBO) kept as codes (CLEAN-12) ... places CONSISTENT (no exception needed);
                                                                    occupation DEPARTS WITHOUT A REASON. Prompt 2.
                                                                    The batch's three cases are not one case (below).
Register flags touching this dataset: none is about sinan. It takes no exception to SPLIT-14 or SPLIT-10 (it has a
measured 2-month gap and every train side is 72-90%). It drops every post-notification field, the newer side of the
"post-outcome feature" drift flag (Lennart: keep up to 2026-11-05, exclude from 2026-11-08). No drift by one curator
on the rules checked here.

D1. The cohort: notifications decided by a laboratory (42%); fit approximate; `Selection Bias` (P3, USE-8 Must)
Status: CONSISTENT with the precedents. One gap: USE-9 (Should, narrows USE-8) is not recorded.

Precedents
  * sdss_17 (selection.md "Selection bias"; fit approximate): objects picked for a measurement, classified by a use
    case that meets objects without one. Same mechanism: the label exists only for the notifications sent to the lab,
    the actor meets every suspected case.
  * tunisian_fraud_detection_challenge (CC 2026-11-05, Lennart, issue 4 B; curation/records/tunisian_fraud_detection_
    challenge.md): `Selection Bias`, "every row is an inspected taxpayer-year, while a real screening ranks all
    filers"; fit approximate. Same shape: the label exists only where the authority checked.
  * lt_vehicle_loan_default_prediction (CC 2026-11-04 and 2026-11-05, Lennart; use_case.md Cases USE-8): marker and
    approximate fit because "here we know we would want to use more but dont have it". Here the actor would want lab
    truth for the untested half and does not have it.
  * eryhemato_squamous_disease, ljubljana_primary_tumor, superconductivity: approximate; infrared_thermography_
    temperature: direct (Lennart, 2026-10-27, use_case.md Cases): judged against the setting of the use case.
  * heart_disease (2026-10-27, Lennart): "the referral for angiography is the setting of the use case, not the gap".
    This is the one precedent that could read the selection as the setting (see USE-9 below).
  * dengue_hematology_bangladesh (AI screening, 2026-10-31, not reviewed): the same task on blood counts, read
    approximate for an undescribed tested population. No curator decision; same reading.
  * sivep_gripe_sari_outcome (same portal): screened only (AI 2026-11-08, WIP), no cohort decision yet. When it is
    added, its cohort should be judged against this one.
  * Against the builder's option (b), clinical-epidemiological closings as labels: xente_fraud_detection_challenge
    (2026-11-04, Lennart: `No` under USE-5, a label that mixed "not fraud" with "not reviewed") and the tension "the
    real-world target against a convenient label" (corporate_credit_rating). A closing by the team's own judgement as
    the label is the convenient label. Option (a) follows them.

Facts that matter for the rule
  * Lab share falls at epidemic peaks: 50.6% in a state's quietest quarter of months against 40.3% in its busiest
    (domain practitioner, sel.log). The deployment population (every suspected case, or the untested half) is
    64.0% dengue against 47.7% in the cohort. The setting of the builder's actor does not share the selection, so
    approximate follows the 2026-10-27 rule.
  * My count: among decided notifications with any dengue test result (serology, NS1, PCR or isolation coded 1-3),
    the laboratory criterion closed 92.6% (2017), 89.3% (2019), 86.3% (2020) and 89.0% (2021). So the cohort is
    close to "the tested notifications".

USE-9 (not in the notes): is there a use case whose setting shares the selection, as heart_disease's referral did?
"A physician who has sent a sample, before the result" would meet nearly this cohort and read direct. The domain
practitioner shows the Ministry's 2016 protocol manages every suspected case by risk group whatever the confirmation,
so that actor's decision does not exist: it would be "a use case rephrased only to excuse a gap" (USE-9's weighed
factor against). The practitioner's actor (the surveillance team closing the untested notifications and choosing
whom to test) acts on the untested half, so the fit stays approximate and the marker stays, as in lt_vehicle. Either
way the outcome is the same; the notes should say USE-9 was asked and why it does not apply, and `fit_reason` should
carry the numbers (64% against 48% dengue; lab share 40% at peaks against 51% off-peak).

No prompt: the call follows the precedents. The actor's wording is the domain practitioner's finding, not a
consistency question.

D2. Windows: three half-years 2020H2, 2021H1, 2021H2, gap 2 months (P4, SPLIT-14 Must against SPLIT-20 Should)
Status: CONSISTENT. One note missing (COVID-19), which SPLIT-20 asks for.

  * SPLIT-14 (Must, amended 2026-11-08 on wisconsin) against SPLIT-20 (Should): yearly windows put the 2019 window on
    25.9% of the rows (split auditor, a_counts.log), below the floor and below wisconsin's 40% clause. That clause
    also needs recurring entities that entity folds would test as unseen. Must over Should: half-years it is. The
    builder's framing is right.
  * SPLIT-15 (roll back from the newest, as many windows as folds): followed. Contiguous windows that together cover
    both seasons are the form the curator chose twice: rain_in_australia (CC 2026-10-26, Lennart, issue 2: 26
    contiguous windows "instead of 9 spaced six weeks apart (follows SPLIT-15; no exception needed)") and
    airqo_low_cost_air_quality_monitor_calibration_challenge (2026-11-05, Lennart, issue 1: more windows so the test
    covers both seasons, "chosen from season and site coverage, not scores").
  * The off-season is not an "atypical season" in SPLIT-20's sense. Its cases are a holiday peak (aeolus,
    2026-10-12), the COVID months and the stale-record period (perth_house_prices, 2026-10-26), and one dry season
    only (airqo). Half of every dengue year is off-season, so two off-season windows of three are no departure.
  * ppnn's spaced windows (this batch, not reviewed; its checker found them departing from SPLIT-15 without an
    atypical period) and climate_model_weather_forecasting_1m (three contiguous weeks of July 2023, one season, never
    discussed) are not counter-precedents. Sinan's windows are contiguous and rolled back, which is the
    rain_in_australia side.
  * Option (b), four half-years with 2020H1 (train 55.4% with the gap, 57.0% without): also consistent, as airqo
    added windows for season coverage (smallest train side 57.3%). Choose between (a) and (b) from coverage and
    periods, not from scores (SPLIT-21, Must).
  * The fact the notes lack: all three test windows fall in the COVID-19 pandemic. SPLIT-20 names COVID-19 as a break
    to check, and perth's windows were placed to avoid it. Measured: the lab share was 53-58% in 2020Q3-2021Q2
    against 37-48% in 2016-2019. In 2021 the lab cohort is more often dengue than the clinical closings (0.467 vs
    0.453 in 2021Q1, 0.557 vs 0.508 in 2021Q2), the reverse of every quarter before (sel.log). So the selection
    itself moves inside the test period. The windows cannot avoid it: no labelled file after 2021, and the floor
    bars windows before 2020. Remedy: a sentence in splits_comment (the domain practitioner asks the same). This also
    counts for (b), whose added 2020H1 window is mostly pre-pandemic. That is a fact about periods, not scores.
  * Gap of 2 months: SPLIT-10 applied with measurements (1.7-1.8% of training rows open at the July window starts
    without it). The register's SPLIT-10 amendment_due flag counts no-gap exceptions; sinan takes none.

D3. Leukopenia kept as a sign (P4, LEAK-10 Must; builder issue 3)
Status: CONSISTENT. The keep rests on a timing test now, not only on the form.

  * LEAK-10 is a timing question. LEAK-38 (keep unverifiable fields with a note) does not apply: it covers data a host
    released for its own competition, not government surveillance. So the field has to be shown to exist at
    notification, or the traceable late part has to show no gain. That is LEAK-10's later-pull clause:
    onlinenewspopularity kept with a note, "go with (a)", 2026-10-21; distribution_transformers_at_cauca_department
    dropped when a gain may sit on the changed rows, Lennart, 2026-10-21.
  * Traced: the column auditor's odds ratios do not grow when the clinical section may have been filled later: 2.28
    same-day investigation, 2.94 one to seven days later, 2.91 later still. Petechiae moves the same way, so nothing is
    specific to the blood count. The claim auditor's typing split (a2_typing.log) gives Yes-vs-No dengue difference
    +0.226 when typed within 3 days of notification against +0.238 when typed after closing. The early-typed part
    carries the association, so the late part adds none worth a drop. Caveat for the note: DT_DIGITA is the first
    typing date and "is not updated" on later edits, so edits after the first typing stay invisible (the builder's
    "cannot verify" line).
  * Precedents for keeping a test done before the decision: heart_disease (2026-10-27, Lennart: pre-angiogram tests
    are inputs); dengue_hematology_bangladesh's screening frames the whole blood count as the input before the dengue
    test (AI, not reviewed). A blood count is not the measurement that gives the label (LEAK-10's "fitted from the
    same measurement" clause, sdss_17's redshift, does not reach it).
  * Wording, not consistency: the use case says "before or without a laboratory result", and a blood count is one.
    Make it "the dengue test's result" (column auditor, domain practitioner). The builder's issue 3 can be settled by
    LEAK-10 with the measurement. If it stays an issue, (a) is the consistent answer.

D4. Exact copies kept as natural repeats (P4, LEAK-16 to LEAK-20)
Status: CONSISTENT for the copies of distinct patients. DEPARTS WITHOUT A STATED REASON for the copies of one patient.

  * Distinct patients with one profile (1,056 of the 1,684 groups whose copies all carry a birth date): kept, as
    ai4d_lab_tanzania_tourism_classification_challenge (2026-11-05, Lennart: coarse answers, distinct respondents),
    bank_marketing (2026-11-08, Lennart: 274 copies, 0.6%, plausible repeats of common profiles), hiva_agnostic and
    qsar_tid_11 (LEAK-19: distinct entities the features cannot tell apart stay). The 306 two-label groups, mostly
    different patients, follow LEAK-20's "genuine label ambiguity" and bank_marketing's 32 kept feature-copies.
  * One patient notified twice (628 groups with the same birth date, about 0.02% of the rows, and 68 more whose birth
    dates differ by one character): copies of one entity. LEAK-19's precedents drop those: qsar_oral_toxicity's 477
    copies of one compound, qsar_tid_11's salt forms of one parent, audiology_diagnosis (Lennart, 2026-10-21). The
    notes keep them as "natural repeats". The reason given ("cannot be told apart in 2020-2021") covers only the test
    years. The open files carry no SINAN duplicate mark ("2 - Duplicidade (nao contar)": 0 rows in the cohort;
    NDUPLIC_N is blank on 2,975,486 rows), so the system did not flag these duplicates.
  * A fact in the data sets the case apart: the notification date is an input, so no copy over every input crosses
    the split (probe 5: 0.0% of test rows with the date). The copies cannot leak; they only weight a handful of
    patients twice within one window. It is not written as the reason.

Prompt 1 (issue shape):

   **Consistency check (AI, 2026-11-09):** Do the duplicate notifications of one patient stay, as an exception, or go
   like the copies of one entity elsewhere?
   - **Problem:**
     - 628 copy groups share the birth date as well as the date, unit, places, age and every finding: one patient
       notified twice, not two patients with one profile[p1rule].
     - LEAK-19's cases drop copies of one entity (qsar_oral_toxicity, qsar_tid_11, audiology_diagnosis), while the
       notes keep them as natural repeats (LEAK-18) without a reason that fits them[p1prec].
     - None crosses the split, since the notification date is an input (probe 5: 0.0% with the date), and in the test
       years 2020-2021 they cannot be told apart from different patients (birth year only).
   - **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | a | Keep, recorded as an exception: no copy crosses the split, and one-patient copies cannot be found in the test years | one line in the notes and the record | true and checkable; no leak; no change to the data | a third kind of keep under LEAK-18/19 to track |
     | b | Drop the second copy of the 628 same-birth-date groups (2016-2019 only) | about 630 rows leave the training years | follows LEAK-19's entity line where the data allows it | different treatment in the test years; changes nothing a score can see |
     | c | Drop every exact copy (2,919 rows, 0.11%) | LEAK-19 read literally | one rule for all years | drops distinct patients too, against ai4d and bank_marketing |

   - **Recommendation:** a.
   - **Decision:** a, b or c?

   [p1rule]: LEAK-19 (Should): exact copies with the same label go, distinct entities the features cannot tell apart stay; LEAK-18 (Should): plausible repeats with few features stay.
   [p1prec]: qsar_oral_toxicity, qsar_tid_11, audiology_diagnosis (LEAK-19 cases, Lennart, 2026-10-21); ai4d_lab_tanzania_tourism_classification_challenge (2026-11-05) and bank_marketing (2026-11-08), Lennart, for the distinct-respondent keeps.

D5. Licence CC BY-ND 3.0 as a one-line note (EV-4 Must)
Status: CONSISTENT. The notes' last bullet names the terms and where they are stated and sends the "no derivatives"
clause to the release checklist. The builder raises no curator issue for it. This follows EV-4 and its cases:
lucas_topsoil (2026-09-23, Lennart) and numerai_v5_2, aeolus, corporate_credit_rating_cat,
african_credit_scoring_challenge (2026-10-21, Lennart: "a one-line note", the terms "release-checklist items"). The
screening line of 2026-10-31 ("check whether a curated subset is allowed") is that checklist item, not a curation
question. In this batch, chile_school_dropout_mineduc's draft issue 5 raises its licence as an issue; that is the
departure, not this one.

D6. Place codes and the occupation (CBO) kept as codes (P7, CLEAN-12 Should)
Status: places CONSISTENT, occupation DEPARTS WITHOUT A STATED REASON.

Places and units (municipality, health region, notifying unit CNES, country; the state is decoded to its abbreviation)
  * An entity's or a place's code is not "a code the source names in words, level by level". Its name is a copy of an
    id. The precedents keep such codes: early_learning_predictors' national ward code (CC 2026-11-05, Lennart, issue
    #48), pricing_game_2017_french_mtpl's `pol_insee_code` (17,794 communes, as text), zillow_prize's fips and region
    ids, house_sales' zipcode. No exception is needed and none should be recorded. The same holds for rais's IBGE
    municipality and chile's communes and schools (chile's checker, D4, reached the same reading).

Occupation (`occupation_cbo`, 2,301 levels)
  * CLEAN-12 (amended 2026-11-01, Lennart) names this case: "a nominal code (a job, a building type, a water source)
    into a category of the words". Its table adds: "A column that still ships as a number while its source has words
    for it is a gap to close, not a choice". The notes keep the code with no reason.
  * The candidate fact: the release's dictionary gives no words. Field 23 points to an external "Tabela de Ocupacao",
    SINAN's occupation table, which is CBO codes plus SINAN's own codes. That fact does not set the case apart by
    itself. labour_inspection_compliance resolves its industry codes from an external official table shipped in the
    folder (Statistics Norway's KLASS, version 30). ny_wcb_assembled_claims_1m (this batch) ships NAICS and WCIO as
    "words [code]". credit_g (2026-10-31, Lennart): "we want the right labels in all cases".
  * What leaving the codes hides here (column auditor, finding 3): SINAN's own codes outside the CBO hold 536,623 rows
    (20% of all rows, 55% of the non-missing occupations): 999991 to 999995 and 998999. Their ages fit student,
    housewife, retired, unemployed and prisoner; 998999 may be "ignorada", an unknown that CLEAN-10 makes missing.
    "000000" (8,401 rows) is not set missing. The 000000 code is a CLEAN-10 fix in any case. Decoding is what would
    have exposed 998999.
  * The column auditor's "a model sees the same partition" is a model argument. CLEAN-12 takes types from context,
    "never from model runs", and zillow_prize (2026-10-26) says a model's score is "not a reason for the encoding".

Are the batch's three cases one case? No. Split them by kind.
  1. Places and entities: sinan's municipalities, regions, units and country; rais's municipality; chile's communes
     and schools. These apply the rule; they are not exceptions and do not count toward three.
  2. A classification whose words are in the release's own codebook: chile's tp_sector and tp_specialty (Anexo VI
     names about 65 levels). Nothing sets it apart. Decode it, as chile's checker recommends.
  3. A national or standard classification whose words sit in an external official table, or in an outdated
     codebook: sinan's CBO (no words in the dictionary), rais's CBO, CNAE and CONCLA (the 2020 layout misses 6.4% of
     the CBO rows), and a fourth in the batch, wioa_employment_after_exit_1m's occupation, industry and CIP codes
     ("Kept as codes", no panel yet). Sinan and rais carry the same CBO list, so they must be decided alike. If all of
     them keep codes on this reason, that is three or more exceptions of one reason, and an amendment is due
     (principles.md). Decide it once now, as a decision on the rule, rather than as exceptions one by one.
  What sinan should do: decode the occupation into "words [code]" (the ny_wcb form) from the official CBO 2002 list,
  the same pinned table as rais, plus SINAN's own codes once their table is found. Set 000000, and 998999 if it means
  "ignorada", missing (CLEAN-10). Keep the place and unit codes as they are, and write the reason in the notes: an
  entity's code, its name a copy. If the curator would rather keep classification codes, that is the amendment
  (option d), applied to sinan, rais and wioa together. Chile decodes either way.

Prompt 2 (issue shape):

   **Consistency check (AI, 2026-11-09):** Does the occupation ship as the CBO's words with the code, decided together
   with rais, or stay a code under an amendment of CLEAN-12 for external classifications?
   - **Problem:**
     - CLEAN-12 decodes "a nominal code (a job ...)" into its words; `occupation_cbo` stays a code, and the notes give no
       reason[p2rule].
     - The words are not in SINAN's dictionary but in an external table (CBO 2002, plus SINAN's own codes such as
       999991-999994 and 998999 on 20% of the rows; 998999 may mean unknown). labour_inspection_compliance and ny_wcb
       decode from such tables[p2prec].
     - rais keeps the same CBO list as a code, and wioa its occupation and industry codes, for the same kind of reason:
       a third exception of one reason makes an amendment due[p2amend].
   - **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | a | Keep the code, recorded as an exception: the release's dictionary gives no words, only a pointer to an external table | a note; no lookup file | no table to source; no risk of a mismatched label | the third exception of one reason with rais and wioa, so an amendment is due anyway; hides 998999's meaning |
     | b | Decode into "words [code]" from the official CBO 2002 table and SINAN's own codes, the same table as rais | a pinned lookup file in the folder; 000000 and an "ignorada" code missing | follows CLEAN-12, labour_inspection_compliance, ny_wcb and credit_g; exposes the unknown codes | a table to source, pin and check (2,301 levels, 1,590 five-character codes to place) |
     | c | Decode only SINAN's own codes (99999x, 998999) and keep the CBO codes | about 6 labels; unknowns set missing | cheap; fixes the part that hides a missing value | mixed codes and words in one column |
     | d | Amend CLEAN-12: a standard classification of thousands of levels whose words are only in an external table ships as its code | one rule for sinan, rais and wioa | settles the batch at once | the 2026-11-01 rule names "a job" among the codes to decode; credit_g asked for the right labels |

   - **Recommendation:** b, decided together with rais's CBO; 000000 missing whatever is chosen (CLEAN-10).
   - **Decision:** a, b, c or d?

   [p2rule]: CLEAN-12 (Should; amended 2026-11-01, Lennart), its table ("a code the source names in words ... the words"; "a gap to close, not a choice"); CLEAN-10 (a code that only means unknown is missing).
   [p2prec]: labour_inspection_compliance (industry codes from Statistics Norway's KLASS v30, a table in the folder); ny_wcb_assembled_claims_1m (this batch, "words [code]"); credit_g (2026-10-31, Lennart: "we want the right labels in all cases"); zillow_prize (2026-10-26: a model's score is no reason for an encoding).
   [p2amend]: principles.md, Exceptions and amendments (three exceptions of one reason: propose an amendment); rais_employment_separation precedent_checker.report.txt D5; wioa_employment_after_exit_1m notes ("Kept as codes: ... occupation, industry and CIP codes").

ALSO NOTED (no prompt)
  * The column auditor's finding 1: 14.1% of the rows were notified after a dengue sample was collected. A filter on a
    date before the prediction point rests on the inputs, not on the label. That is the kind of cut the curator
    accepted for nyc_taxi_trip_duration_1m and pkdd_15 (USE-7, 2026-10-26: "the cut rests on the inputs, not on the
    travel time"). No precedent keeps rows whose decision point has already passed. This is a validity call for the
    curator (USE-3 Must), not a consistency question; the filter would be the consistent remedy.
  * The curator accepted the record on 2026-11-08 for "most rows, most features". The size check found the 6.5M rows of
    2024 unlabelled; the task has 2.62M rows and 37 features. A later stage's measured finding supersedes the
    screening (principles.md, Precedence). The record says so in the size-check assessment, so no conflict; worth one
    line in the review file so the curator sees that the accept reason changed.

FILES
  This report; scripts in the run folder.
  Definition: datasets/_dev/tabarena-v0pt2/sinan_dengue_case_screening_1m/dataset.py
  Precedent records (curation/records/ in the working tree): sdss_17, tunisian_fraud_detection_challenge,
  lt_vehicle_loan_default_prediction, heart_disease, dengue_hematology_bangladesh, rain_in_australia, perth_house_prices,
  airqo_low_cost_air_quality_monitor_calibration_challenge, ai4d_lab_tanzania_tourism_classification_challenge,
  bank_marketing, early_learning_predictors, pricing_game_2017_french_mtpl, credit_g.
  Same-batch reports: the precedent-checker reports of rais_employment_separation, chile_school_dropout_mineduc and
  ppnn_ecmwf_t2m_postprocessing_germany.

</details>

<details><summary>Advocate</summary>

ADVOCATE OPENING BRIEF: sinan_dengue_case_screening (folder sinan_dengue_case_screening_1m), 2026-11-09

Position: ship, after changes that keep the dataset (one filter, notes, rewording, metadata). No agent found a
Must that cannot be fixed. Every problem found sits on the remedy ladder at "fix the definition" or "keep with a note".

1. The inputs are honest at notification; nothing recovers the label (P4, LEAK-10 Must, USE-3 Must).
   Evidence: every lab field, closing field, alarm/severity sign and the place-of-infection fields that the system
   erases on discard (blank 97.6-99.3% vs 20-25%) are dropped (claim auditor items 11-12; column auditor, dictionary
   f1-121 read in full). The blind reviewer, with no notes: "I found no post-outcome columns". The task gamer:
   "Nothing here recovers the label"; best single feature 0.03 AUC below the full model; row order, format,
   missingness, copies all null (+0.001, noise +-0.0005). Leukopenia passed a timing test, not just a form reading:
   2021 forms first typed after closing carry no more clinical signal (clinical-only AUC 0.635 vs 0.639 / 0.657),
   odds ratio flat with investigation delay (2.28 / 2.94 / 2.91), worth 0.002 AUC.
   Answers: the blind reviewer's "missing symptoms coded No". Refuted by measurement (EV-2): the raw sign fields
   hold only 1 and 2 on kept rows (claim auditor item 18; task gamer "explicit 2s in the source"). The all-blank
   rows were already dropped under USE-7.

2. The cohort is the right label, and the gap is the standard approximate fit (P3, USE-8 Must, USE-5).
   Evidence: the label is a laboratory result for 92.4% of rows in both classes (claim auditor item 3). Option (b),
   adding clinical-epidemiological closings, would make the label "the team's own judgement", the decision being
   automated (domain practitioner); that is the "real-world target against a convenient label" tension
   (corporate_credit_rating, xente). Precedents settle it: sdss_17, tunisian_fraud, lt_vehicle_loan (approximate +
   `Selection Bias`), and the precedent checker rates D1 CONSISTENT. Same cohort as Bohm et al. ("All data were
   confirmed by laboratory tests").
   Answers: "selection on a post-prediction variable" (task gamer, blind reviewer). USE-8 fixes a selection gap with
   fit approximate + marker; it does not exclude. The filter applies to train and test alike (task gamer found no
   exploit in it). Add the numbers to fit_reason (64% vs 48% dengue among untested; lab share 40% at peaks vs 51%).

3. The split mirrors the application and meets every Must (P4, SPLIT-1, SPLIT-9, SPLIT-14 Must).
   Evidence: temporal by notification date; a random split overrates by 0.08-0.18 AUC (split auditor), so the
   regime matters and is right. Train sides 71.9-90.2%; 3 windows of 103k-394k rows; units recur (95-97% seen),
   a known entity (SPLIT-13). No shortcut (SPLIT-9): no patient id, 0 test rows with an all-feature copy in train.
   Answers: (a) gap 2 months costs 0.026-0.037 AUC (SPLIT-10, Should). Mildest fix needing no new data: gap=1, a
   one-line change (split auditor b), or keep with the cost in splits_comment. (b) Two off-season windows (SPLIT-20,
   Should) lose to SPLIT-14 (Must): yearly windows put 2019 at 25.9% train. The curator chose contiguous rolled-back
   windows before (rain_in_australia, airqo); family order is unchanged across windows (+0.058 to +0.084). (c) COVID
   in all windows: unavoidable (no labelled file after 2021), a note (SPLIT-20 remedy). (d) Gap-row labels in
   data.parquet (task gamer +0.02-0.03): a harness matter; the splits already exclude them from training.

4. The pre-notification samples are a real problem, and a filter on inputs fixes it (P3/P4, USE-3 Must).
   Concede: 14.1% of rows were notified after a dengue sample was collected (NS1 positive 51% vs 35%); they lift
   the score by 0.004-0.031 (column auditor finding 1). This is the one change I accept as a validity fix.
   Remedy (fix the definition, not exclude): keep rows with no DT_SORO/DT_NS1/DT_PCR/DT_VIRAL before DT_NOTIFIC.
   The cut rests on inputs known at the prediction point, not the label: the nyc_taxi_trip_duration_1m / pkdd_15
   precedent (USE-7, 2026-10-26). Cost 14% of rows; windows stay above every floor (test 103k-394k now).
   Outranks "exclude": the remedy ladder; a leak is no reason to reject a real task (tension row, kickstarter).

5. It is worth benchmarking and the metric holds (P6, TP-1 to TP-5, MET-5/6/8/11).
   Evidence: 2.62M rows, 37 features, minority class >= 27,894 per fold; beats the dummy on 3/3 windows (+0.19
   AUC); room between families (LightGBM over logistic +0.06 to +0.08; task gamer's honest features +0.04).
   Within-unit-month AUC 0.59-0.62 matches the WHO clinical definition's level (domain practitioner): honest
   difficulty, not noise. `no_spread` read as 3-window noise (TP-3, re-check with tuned runs). Fallback roc_auc:
   multi-metric paper, no threshold or cost (MET-5, MET-6; gallstone_disease precedent); the claim auditor: "the
   fallback itself holds". Fix the reason's wording (5 metrics in Table 4, AUC in text; name the sensitivity
   emphasis set aside). log_loss under a surveillance actor is a curator's option, not a defect.

6. The use case is real; the wording, not the task, needs fixing (P3, USE-1, USE-9).
   Concede: the 2016 protocol manages every suspected case by risk group, so "decides whether to manage it as
   dengue" is not the decision (domain practitioner). The decision that exists: the surveillance team closing
   untested notifications and steering testing (manual 8.4-8.5), with the physician's differential as secondary.
   Inputs, label, split and fit stay the same. Remedy: reword use_case, fit_reason and "before or without the
   dengue test result" (not "a laboratory result", since a blood count is one). A text change in the definition.

7. The remaining findings are cheap quality and metadata fixes (P5 PROV-9, P7 CLEAN-10/12, LEAK-19, writing).
   - year 2024 refuted (PROV-9, Must, metadata only): set 2023 with the DATASUS FTP reason (claim auditor R1).
   - occupation "000000" missing (CLEAN-10, no decision needed); decoding the CBO is a P7 Should: cheap part
     (SINAN's 99999x/998999) now, the full CBO decided with rais (precedent checker prompt 2). P3 over P7: a real
     task carries a documented cleaning gap (churn_telco_south_asia).
   - one-patient copies (628 groups, ~0.02%, none cross the split): keep as an exception (precedent checker
     prompt 1, option a).
   - writing: 0.6% copies "on every input but the date; none with it", 5,524 not 5,518, COVID note, label noise
     tied to onset timing (USE-5), leukopenia "No" mostly means no count, Bohm et al.'s 0.985 not reproducible on
     their variables (AUC 0.578).
   - health regions blank for whole states and residence_country near constant: kept with notes (column auditor:
     structural / not constant under CLEAN-5); the municipality carries the place.

Judgment record
Verdict: ship after changes.
Validity: USE-3 triggered, fixed (pre-notification sample filter); USE-8 holds as approximate + `Selection Bias`;
  LEAK-10 holds (leukopenia tested); SPLIT-1/9/14 hold; PROV-9 fixed (2023).
Value: TP-1 to TP-5 pass; MET fallback roc_auc holds, wording fixed.
Quality: CLEAN-10 fixed (000000); CLEAN-12 occupation decoding with rais; LEAK-19 exception for one-patient copies.
Weighed: size +, source + (national system, open), honest difficulty +, COVID windows -, reproducibility - (weekly
  file replacement, SHA-256 recorded).
For the curator: filter (recommend yes), gap 2 vs 1 month, window set, actor wording and metric, occupation.

</details>

<details><summary>Advocate rebuttal</summary>

ADVOCATE REBUTTAL: sinan_dengue_case_screening (folder sinan_dengue_case_screening_1m), 2026-11-09

The critic and I agree on the verdict: ship after changes, no exclusion. We differ only on two weighing calls (the
metric, the windows).

C1 (pre-notification samples, USE-3 Must): CONCEDE. This was my point 4. The filter on the collection dates goes in
   `_clean`, with the 14% share and the unresolvable 43.8% same-day sampling in the notes.

C2 (use case, USE-1/USE-5; metric, MET-1): CONCEDE the rewording and the MET-11 facts (my points 5 and 6). DISPUTE
   that the new actor forces log_loss. The surveillance team's second decision, choosing whom to test when tests
   are rationed (domain practitioner (b)), is a ranking decision, and ROC AUC scores it. No source fixes a threshold
   or cost (MET-6), so the fallback on probabilities stands (MET-8, gallstone_disease). Every family's log loss is
   worse than the constant (0.69-0.99 vs 0.685) because the base rate swings 13-59% by quarter. Under log_loss the
   benchmark would mostly test prior shift, as the practitioner warns. Remedy: keep roc_auc and state the prior-shift
   reason in the metric reason, the form the critic calls defensible. log_loss stays the curator's option.

C3 (selection under-described, USE-8 Must): CONCEDE the notes (marker, the 64% vs 48% and 40% vs 51% numbers, the
   rise in lab share across the split). DISPUTE "a score here does not transfer": the shift runs toward the
   deployment population. The 2021 test cohort is a broader share of decided cases (56% lab-decided vs 37-42% in
   training; claim auditor item 30), so the test side is closer to "every suspected case" than the training side.
   The family order holds in every window (+0.058 to +0.084, split auditor). USE-8 asks for approximate + marker,
   and both are already in place (precedent checker D1: CONSISTENT).

C4 (two-month gap, SPLIT-10 Should): CONCEDE. gap=1 is the one-line fix: open training rows 0.14-0.85%, and it
   recovers 58-100% of the cost (split auditor (b)). The as-of filter only if the API carries a helper. One
   qualifier: the task gamer's +0.016 to +0.038 is a participant exploit, not a cost of the split. A deployment would
   have the first month's labels (+0.0066), which gap=1 gives.

C5 (COVID, off-season weight, SPLIT-20 Should): CONCEDE the COVID note (the minimum, unavoidable). DISPUTE that the
   windows should move. SPLIT-15 asks to roll back contiguous windows from the newest, as the curator did twice
   (rain_in_australia, airqo). The precedent checker found the off-season windows "no departure" (half of every year
   is off-season). The family order is unchanged across windows. Skipping 2020H2 is admissible, but any choice must
   be made on coverage, not on the 0.714 vs 0.686 score levels (SPLIT-21, Must), and the critic's case quotes those
   levels. Keep (a) with the note. (b) is the curator's weighing call, not a defect.

C6 (PROV-9 year, copy wording, counts, one-patient copies): CONCEDE all (my point 7). Year 2023 with the DATASUS
   reason; corrected sentences; a LEAK-19 exception whose fact is that none of the copies crosses the split.

C7 (occupation codes, CLEAN-10/12 Should): CONCEDE "000000" as missing now (CLEAN-10) and decoding SINAN's own codes
   (99999x, 998999), a cheap and safe fix. The full CBO decoding is decided with rais and wioa (precedent checker
   prompt 2). P7 never blocks shipping (P3 over P7, churn_telco_south_asia).

Net: the changes both briefs ask for are the same set. The open calls for the curator are gap 1 vs 2 months, the
window set (keep vs 2020H1/2021H1/2021H2) and the metric under the reworded actor. I recommend gap=1, keeping the
windows with a COVID note, and keeping roc_auc with the prior-shift reason.

</details>

<details><summary>Critic</summary>

CRITIC, OPENING BRIEF: sinan_dengue_case_screening (folder sinan_dengue_case_screening_1m), 2026-11-09

Position: do not ship as defined; ship after the changes below. Nothing here needs exclusion: every Must problem has a
fix in the definition or the notes. Points ranked validity (P3-P5) before quality (P7), Must before Should.

1. P3/P4, USE-3 (Must) with LEAK-10: 14% of the rows are notified after a dengue sample was already taken.
   Problem: 370,314 of 2,623,839 rows (12.6%-16.0% of each test window) have a dengue sample (DT_SORO, DT_NS1,
   DT_PCR, DT_VIRAL) dated before DT_NOTIFIC; 100,893 of them more than a week before. An NS1 taken before
   notification is positive in 51% of these rows against 35% when taken on the notification day, so the notification
   often follows the result. Dengue share 61.7% vs 44.9%.
   Effect: the inputs find these rows (LightGBM AUC 0.87-0.90 for "sampled before notification"; notifying unit alone
   0.845, onset lag 0.737; 130 units with >95% dengue sampled first in 49.6% of their rows), and they lift the
   benchmark score by 0.004-0.031 AUC through a path the use case ("before or without a laboratory result") rules
   out. Not caught by any probe: no single column is post-outcome.
   Evidence: column_auditor finding 1; precedent_checker "Also noted" (no precedent keeps rows whose decision point
   has passed; the filter is the consistent remedy, as USE-7's nyc_taxi/pkdd cuts on inputs).
   Remedy (fix the definition): in `_clean`, before the test fields are dropped, keep only rows with no dengue sample
   dated before the notification date. Costs 14% of rows; every window stays far above the floors. Write the share
   and the 43.8% sampled on the same day (a same-day NS1 cannot be resolved) in the notes.

2. P3, USE-1 and USE-5 (Must): the decision the use case names is not taken in practice.
   Problem: the Ministry's 2016 protocol (in force for every year of the data) stages and treats every suspected case
   as dengue by risk group; for group A "os exames especificos para confirmacao nao sao necessarios para conducao
   clinica". A physician does not decide "whether to manage and follow it as dengue". The decisions a lab-truth
   probability serves are the surveillance team's: closing the untested notifications on clinical-epidemiological
   grounds (manual 8.4-8.5, 57% of decided notifications) and choosing whom to test; and the physician's
   differential diagnosis.
   Effect: the actor sets what the metric must score (MET-1, Must). The surveillance team acts on the probability
   level, which pooled ROC AUC ignores; every family's log loss is already worse than the constant (builder).
   Evidence: domain_practitioner sections 1 and 6; precedent_checker D1 (USE-9 asked and not applicable).
   Remedy (fix the definition): reword use_case to the surveillance team at notification (and the differential
   diagnosis as the physician's reading), "before the dengue test's result" (a blood count is a lab result); record
   in the notes that USE-9 was asked and why it does not give a direct fit; decide the metric for that actor under
   MET-1/MET-8 and write why (keeping roc_auc is defensible only with the prior-shift reason stated). Fix the metric
   reason's facts too (MET-11, Must): Bohm et al.'s Table 4 lists five metrics, AUC is in the text, and their
   Discussion's call for high sensitivity must be named and set aside (claim_auditor R3).

3. P3, USE-8 (Must): the selection is under-described and moves inside the test period.
   Problem: the cohort is close to "notifications with a conclusive lab result" (86-93% of tested decided rows are
   lab-closed). The deployment population (the untested half) is 64.0% dengue vs 47.7%, and the lab share falls at
   epidemic peaks (40.3% vs 50.6%). The lab share of decided notifications rises from 37-42% (2016-2019, train) to
   56% (2021, test); in 2021 the lab cohort is more often dengue than the clinical closings, the reverse of every
   earlier quarter.
   Effect: train and test sample different slices of the suspected cases; a score here does not transfer to the
   population the actor meets.
   Evidence: claim_auditor items 4, 30; domain_practitioner section 3; split_auditor finding 3; precedent_checker D1.
   Remedy (a note and the marker): `Selection Bias` marker; fit_reason with these numbers; the shift of the
   selection across the split in the notes. Option (a) of builder issue 1 otherwise stands.

4. P4, SPLIT-10 (Should, applies SPLIT-9): the two-month gap is longer than the collection needs.
   Problem: median label delay 13-20 days; at a July start 72-73% of the last two months' rows are already closed;
   confirmed and discarded close alike (median 17 vs 18 days), so no selection by the outcome needs the gap; the
   release is closed. SPLIT-10 says train on what is known at the window start; the gap is set at the p90.
   Effect: the benchmark tests a model two months staler than the declared twice-yearly refit, losing the
   late-season local rates: as-of training scores +0.037 / +0.009 / +0.026 AUC; the task gamer's gap-row labels give
   +0.016 to +0.038, of which the first month alone (what a deployment has) +0.0066.
   Evidence: split_auditor finding 1; task_gamer finding 1.
   Remedy (fix the definition): gap=1 (open training rows 0.14%-0.85%), or the as-of filter on the closing date if
   the API carries a split helper. Keep 2 only with the cost written in splits_comment.

5. P4, SPLIT-20 (Should): every test window is in the COVID years, and the off-season gets two thirds of the weight.
   Problem: 2020H2-2021H2 follow March 2020: lab share of confirmed cases 0.20-0.32 before vs 0.40-0.60 after; fever
   Yes 0.80-0.86 vs 0.73-0.77; leukopenia Yes halves. Two windows are off-season (17-25% of a year's notifications),
   scoring 0.74-0.75 against 0.65 in season, so the window mean (0.714) sits above the row-weighted one (0.686).
   Evidence: split_auditor findings 2-3; domain_practitioner section 4; precedent_checker D2 (missing COVID note).
   Remedy: a splits_comment note naming the pandemic and the measured shifts (the minimum, unavoidable: no labelled
   year after 2021). For the curator, decided on coverage not scores (SPLIT-21): cutoffs 2020H1/2021H1/2021H2
   (train 55.4%-90.2%, two season windows). Note that 2020H1's share is 55.4% with the gap, not 57%.

6. P5, PROV-9 (Must) and refuted statements in the notes.
   Problem: year 2024 is refuted: the DATASUS FTP (FINAIS) carries the same release (DENGBR23.dbc = the portal's 2023
   rows, 1,645,956), and Bohm et al. used these data before 28 Nov 2023. Also wrong as written: "an exact copy in train
   for 0.6% of test rows" (0 per fold with the date, a feature; 0.6% is without it); 5,518 onset lags -> 5,524;
   one-patient copies (628 groups) kept under LEAK-18 with a reason that covers only 2020-2021 (LEAK-19, Should).
   Evidence: claim_auditor R1, R2, R4, item 26; precedent_checker D4.
   Remedy (fix metadata and notes): year 2023 at the latest, BibTeX naming the DATASUS distribution; correct the copy
   and count sentences; record the one-patient copies as an exception with its fact (none crosses the split).

7. P7, CLEAN-10 and CLEAN-12 (Should): occupation codes hide missing values. Quality, not a reason to exclude.
   Problem: "000000" (8,401 rows, 59.5% dengue) is not set missing; SINAN's own codes 999991-999995 and 998999 hold
   536,623 rows (20%) undecoded, 998999 possibly "ignorada"; 1,584 rows coded "10001". The notes give no reason for
   keeping a job code as a code, which CLEAN-12 (amended 2026-11-01) names among those to decode.
   Evidence: column_auditor finding 3; precedent_checker D6 (decide with rais and wioa).
   Remedy (cheap, safe): add "000000" to MISSING_CODES now; decode SINAN's own codes and the CBO into "words [code]"
   with the rais decision, or record the exception if the curator amends CLEAN-12.

Not argued: leukopenia (traced, no late-entry signal, worth 0.002 AUC: keep), the places and the unit (USE-6), the
blind reviewer's "missing symptoms coded No" (refuted: explicit 2s in the source, task_gamer) and "health region
mapping gap" (structural: those states have none, column_auditor), and log-loss-vs-constant as a value failure.

Sources: panel reports in this folder; builder_report.md; the working tree's dataset.py and principles.md, use_case.md.

</details>

<details><summary>Critic rebuttal</summary>

CRITIC REBUTTAL: sinan_dengue_case_screening (folder sinan_dengue_case_screening_1m), 2026-11-09

The verdicts agree: ship after changes, no exclusion. I concede most points. The disputes are narrow.

A1 (inputs honest, nothing recovers the label; LEAK-10, USE-3): CONCEDE for the columns: every kept column is known at
   notification, and leukopenia passed a timing test. DISPUTE "nothing recovers the label" as a statement about the
   task as defined. Before the filter, 14% of rows reach the label through the unit and the onset lag
   (column_auditor finding 1, AUC 0.87-0.90 for "sampled before notification", +0.004-0.031). The advocate's own
   point 4 concedes this. The claim holds only after the filter, so the notes should say so then and not before.

A2 (lab cohort, approximate + `Selection Bias`; USE-8, USE-5): CONCEDE the cohort, option (a) and the precedents
   (D1 CONSISTENT). One qualifier on its rebuttal C3, "the shift runs toward the deployment population": only the
   size of the share moves that way. The dengue rate does not: in 2021 the lab cohort is more often dengue than the
   clinical closings (0.467 vs 0.453, 0.557 vs 0.508), the reverse of every earlier quarter (precedent_checker D2),
   while the untested half was 64% vs 48% before. So the direction of the gap changes inside the test period. A note,
   which the advocate already accepts, settles it under USE-8. No further change asked.

A3 (split meets every Must; SPLIT-1, SPLIT-9, SPLIT-14): CONCEDE SPLIT-1/9/13/14, gap=1 (SPLIT-10), the COVID note and
   (d): the gap-row labels are a harness matter, since the splits keep them out of training. On the windows (SPLIT-20,
   Should): CONCEDE keep (a) with a note as the mildest remedy. The advocate is right that the 0.714 vs 0.686 levels
   cannot decide the window set (SPLIT-21, Must). I cited them as the effect on the reported number, not as the
   reason. The reason for option (b) is coverage: the season holds 67-84% of a year's notifications but gets 1 of 3
   windows. The note should state that weighting. Moving the windows stays the curator's call.

A4 (pre-notification sample filter; USE-3): AGREE. This is my point 1, with the same remedy and the same precedent
   (USE-7 cuts on inputs).

A5 (worth benchmarking, roc_auc holds; TP-1 to TP-5, MET-5/6/8/11): CONCEDE TP. CONCEDE keeping roc_auc under the
   reworded actor, with the prior-shift reason written in the metric reason (the form I called defensible). Testing
   rationed by rank is a ranking decision, and MET-6 finds no threshold or cost. MET-11's factual fixes (five metrics
   in Table 4, AUC in the text, the sensitivity emphasis named and set aside) remain required, and the advocate
   accepts them.

A6 (use case reworded; USE-1, USE-9): AGREE. This is my point 2: the surveillance team, the differential as secondary,
   "the dengue test's result", and USE-9 recorded as asked.

A7 (metadata and quality; PROV-9, CLEAN-10/12, LEAK-19, writing): CONCEDE all. Year 2023 with the DATASUS reason;
   "000000" set missing; SINAN's own codes decoded now, the full CBO decided with rais and wioa; the LEAK-19 exception
   with its fact; the corrected sentences. P7 does not block shipping (my point 7 said the same).

Net: the changes are the same set in both briefs. The one remaining difference is wording: the notes must not call
the task leak-free until the pre-notification filter is in. Curator's open calls: gap 1 (both recommend), windows
(both accept keep + note; option b on coverage only), metric (both accept roc_auc with the prior-shift reason).

</details>
