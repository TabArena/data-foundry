# enem_entrance_exam_scores

**Outcome:** added as `enem_entrance_exam_scores_1m`. The AI recommends shipping it; the panel's changes are made, and
issue 1 asks you to confirm what is implemented (race, sex and family income stay as inputs) and whether the Assam
sibling's `Ethical Issue` marker is reopened in its own record. The task is ours, built on INEP's (Brazil's education
statistics institute) ENEM microdata (Brazil's national secondary-school exam, editions 2018 to 2023): at the close of
registration, what mean score over the five tests will a registrant reach, judged from the items of the registration
form? The rows are the 17.4 million registrants present on both exam days, of which a uniform quarter of each edition is
read; the target is the mean of the five scores, which ProUni scholarships and FIES student loans require to be at least
450; the split is temporal by edition (2021, 2022 and 2023 held out in turn, 1M training and 500k test rows each); the
metric is the fallback `rmse`.
Verdict: ship after changes (made).
Changes made after the panel: the use case now names, as an example, an NGO, a cursinho (free preparation course) of
MEC's CPOP programme or a state department filling limited places, which asks the registration items on its own intake
form, since INEP does not pass the form on; the record carries `Selection Bias`, and the fit reason names who is left
out (2023: 38% absent at up to 1 minimum wage against 18% above 4) and that practice takers (treineiros, 17-19% of the
rows) cannot use the edition for ProUni or FIES; a sentence says no direct use case exists (a socioeconomic adjustment
of school results knows its label when made); `school_operating_status` is dropped (it comes from a school census of
unknown year, so it may postdate the exam); 2018's school type is taken from the matched school's administration (no row
is "abroad" any more), and the secondary-school modality is kept only for those finishing in the edition's year, with
2018's youth and adult education (EJA) set to missing, so both columns mean the same in every edition (together -0.024
RMSE for an untuned LightGBM, better in 5 of 6 runs, column auditor); both municipality columns ship as "Name (UF)
[code]" from the names in the same file; the notes correct the 2018-2022 zero counts and the registration dates (May to
July), name the year as the pinned snapshot, say the model serves a support offer only, and record that INEP removed the
takers of 20 small adapted or reapplied test versions; the splits comment names the coding breaks between editions and
why 2017 is not read.
Validity: SEL-1 holds: no law bars race, sex or income for a voluntary offer of free preparation, so the rule on factors
an actor may no longer use does not apply, also as rais_employment_separation_1m proposes to widen it; the Assam
sibling's `Ethical Issue` marker contradicts this reading and is flagged, not followed (issue 1). USE-1 and USE-3
triggered and fixed: the actor as first written could not hold the inputs, since INEP keeps the registration form, so
the rewritten actor asks the items itself (changes above). USE-5 holds (ProUni's mean of five, verified). USE-8 holds at
approximate, with `Selection Bias` set and the income gradient of absence and the treineiro share named. LEAK-10 clause
2 triggered and fixed (`school_operating_status` dropped); the other 42 inputs are on the registration form. LEAK-22
holds: 16,029 participants of 2023 (0.60%, against 191 to 417 a year before) sat day 2 but left both of its tests blank
and got zeros; they stay, with a note, because INEP published the zeros and ProUni counts them, and the mediator's check
found them spread over every state and booklet, with day-2 absence falling by about as much (they look like people
earlier editions recorded absent, not a scoring error); they are 6.3% of the 2023 window's squared error (RMSE 76.10
with them, 73.89 without). LEAK-34 and SPLIT-13 hold (repeat takers cannot be linked, as in deployment); SPLIT-1,
SPLIT-10 (no gap) and SPLIT-14 (the oldest window, 2021, trains on 58.4% of the participants) hold; SPLIT-20 holds, with
its reason restated and the breaks named. PROV-8 and PROV-9 hold (the year is the pinned snapshot of 2026-07-09); the
gov.br footer's CC BY-ND licence (no derivatives; the zips state none) is a release-checklist item, as on
wisconsin_local_government_property_insurance_fund, not an issue.
Value: TP-1 to TP-4 hold (after the changes, untuned LightGBM RMSE 71.6 against the dummy's 91.7, R^2 0.379, above
linear by 0.025, paired SE 0.003); MET-5, MET-6 and MET-11 hold: INEP names no metric, so the fallback `rmse` stands; it
picked the same best model as ROC AUC for "below 450" in 3 of 3 windows.
Quality: CLEAN-21 triggered three times and fixed (2018's school type, the modality, and a note that "not informed"
years since secondary school rise from 2020); CLEAN-12 triggered and fixed (the municipalities decoded from the file's
own names); CLEAN-5 holds (`IN_TREINEIRO` dropped, as from 2019 it copies one level of the school status).
Weighed: source + (INEP's census microdata with dictionaries), size +, use case ours -, fit approximate -, gap 0
(education is no longer thin among the 151 accepted definitions; the record's assessment of 2026-11-09; the mediator had
gap +).
For the curator: issue 1; with a ship verdict you also accept the check warning `task_time_on_few_unique` (the time
column has only six values, one per yearly edition, the finest time the exam has; as on
`wisconsin_local_government_property_insurance_fund`; its text is in issue 1's notes for the AI); and the municipality
decoding follows CLEAN-12 as written but departs from chile_school_dropout_mineduc_1m, rais_employment_separation_1m and
sinan_dengue_case_screening_1m, which ship codes, so if rais's issue 5 amends CLEAN-12, this dataset follows.

**Main points:** Keep race, sex and family income as inputs and reopen the Assam sibling's `Ethical Issue` marker in
its own record (issue 1: as implemented, and recommended); accept the check warning `task_time_on_few_unique` (six yearly
editions only) with the verdict.

**Record judgment:** valid. INEP's microdata of a national census exam, one row per registrant, with dictionaries and
a Leia-me per edition; the task and its use case are ours (USE-1, approximate). The record's fields agree with the
definition; its size check of 2026-11-08 holds (the 2024 split of registrants and scores into two files without a key
ends the task's data with 2023). `Selection Bias` is now set.

**Issues for Lennart:**

1. **Keep race, sex and family income as inputs, and reopen the Assam sibling's `Ethical Issue` marker in its own record?**

   * **Problem:**
     - The definition keeps race, sex and family income from the registration form, and no law the panel found bars them for a voluntary offer of free preparation[^sel1][^law].
     - The Assam sibling `student_performance_on_an_entrance_examination` (666 students of one Indian state, the same task with caste and gender) carries `Ethical Issue`, a marker that means leave it out, while its verdict is `TBD -> Yes`[^contra].
     - Sex is the one ground no Brazilian programme uses, and the only reason that covers it is the one chile_school_dropout_mineduc_1m gives: the use case offers support, not a decision against the student[^chile].
   * **Background:**
     - Brazil's federal quota law (Lei 12.711/2012) uses race and family income for university admission, and the Supreme Court upheld race-based admission (ADPF 186, 2012).
     - MEC's CPOP programme asks its cursinhos to prioritise Black, Indigenous and low-income students; the definition's actor is such a cursinho, an NGO or a department filling limited places.
     - The data protection law (LGPD art. 11 II b) lets a public body process racial origin to carry out a public policy; a private NGO needs the applicant's consent, which it can collect on its intake form (a condition, not a bar).
     - Every call on protected grounds since November asks whether the actor's own law bars the ground for its decision (two insurance-pricing datasets decided; rais_employment_separation_1m and acs_food_stamps_2014_2024_1m proposed)[^row]; here none does.
     - The note now says the model serves a support offer and is not for screening anyone out (a merit scholarship, an admission, a hiring).
   * **Effect on the task:**
     - RMSE rises by 0.18 to 0.20 without race, by 0.25 to 0.29 without race and sex (sex alone about 0.07 to 0.09), and by 0.70 to 0.91 without all three, on a level of 70 to 76.
     - The benchmark hardly depends on the choice: the three grounds together move the score by about 1%, and the ranking of models was not measured without them.
     - For the actor, dropping them makes the ranking of applicants for free places slightly less accurate; who would be ranked worse was not measured.
   * **Experiments:** builder, untuned LightGBM, 300k training rows, the three shipped windows, before the panel's cleaning fixes (which change other columns); the claim auditor replicated the base scores (70.17, 70.39 and 76.10 against the builder's 70.22, 70.43 and 76.00).
   * **Consistency:**
     - chile_school_dropout_mineduc_1m keeps sex for the support reason; open_university_learning_analytics_dataset, student_portuguese_performance and early_learning_predictors keep sex or gender; diabetes_130_us, kumc_inpatient_aki_prediction and sinan_dengue_case_screening_1m keep race.
     - rais_employment_separation_1m drops five grounds because Brazilian law bars them for an employer (its issue 1), and acs_food_stamps_2014_2024_1m proposes dropping race, origin and sex under the food-stamp rule; wioa_employment_after_exit proposes keeping them; no such bar exists for this actor.
     - The Assam marker is a workbook flag from before June[^assamflag], as are the notes on race in adult and law_school_admission_bianry; neither stated reason here sets ENEM apart from Assam (India also reserves places by caste, and a support use case could be written for it).
   * **Panel:**
     - Advocate, column auditor, domain practitioner and precedent checker: keep all three; dropping sex here alone would treat like cases unlike (chile and three shipped education datasets).
     - Critic: the quota law covers race and income, not sex, and the pair with Assam must be settled in one decision rather than set aside; a reason that covers sex, or sex dropped.
     - Domain practitioner: sex is the weakest ground for this actor, and they would not object to dropping it alone.
     - Mediator: no rule fails; what the rules leave open is whether a protected ground is an ethical concern by itself, which no rule says.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep all three; reopen the Assam marker in its own record (implemented) | no change here; an open issue in the Assam record proposes that its `Ethical Issue` becomes a note under the same reading | one reading for both entrance-exam tasks; follows chile and three shipped education datasets; matches every November call | a reading of the rule not written yet; the Assam record needs its own decision |
     | B | Drop sex; the Assam issue proposes dropping gender too | sex leaves; race and income stay | drops the ground no programme uses; small cost | departs from chile and three shipped education datasets with no fact that sets ENEM apart; 0.07 to 0.09 RMSE worse |
     | C | Drop race and sex, as the Assam marker implies (caste and gender there) | two inputs leave | follows the only precedent on this task | no law asks for it; departs from chile and the shipped tasks that keep race; costs 0.25 to 0.29 RMSE |
     | D | Decide with rais_employment_separation_1m's issue 1 | the stance on the actor's own law, amended there, decides ENEM, wioa and acs alike | one stance for the batch | ENEM waits on rais; under that stance the answer is A anyway, as no law bars these grounds here |

   * **Recommendation:** A: no law bars the grounds for a support offer, the support reason covers sex as on chile, and the Assam marker is the precedent to correct, in its own record. **Decision:** A, B, C or D?

   **Notes for the AI:**
   - With the verdict to ship (any option): add to `accepted_check_warnings` in `dataset.py` `"task_time_on_few_unique": "six yearly editions, 2018-2023: the exam is held once a year, so an edition is the finest time; the history starts in 2018 (SPLIT-20) and ends in 2023 (no common key from 2024); a refit trains on whole editions, and an inner validation holds out the newest training edition"`, then re-run `dataset check`.
   - A: a `CC` line in this record (SEL-1: race, sex and family income kept for a support offer; no law bars them; sex covered by the support reason, as chile). In `student_performance_on_an_entrance_examination` (no folder), write an `**Open issues (AI, <date>):**` block through the store API with one issue: its `Ethical Issue` marker contradicts SEL-1 under `TBD -> Yes`, and under the reading decided here it becomes a note (options: marker to a note; verdict `No` under SEL-1). Whether this reading is written into the scope rules is decided in the across-datasets item on the protected-grounds stance, not here.
   - B: in `_clean`, `drop_columns(df, ["sex"])` with a bullet in `curation_comments`; remove `sex` from `CATEGORICAL` and `CODE_LABELS`; update `task_summary.known` and the SEL-1 note; re-run `dataset check`, the leak and task probes; the Assam issue as in A, with sex dropped there too.
   - C: as B for `race` and `sex` (also `PROXY_MISSING["race"]`).
   - D: leave the definition as it is and raise this issue again once rais_employment_separation_1m's issue 1 is decided.

   [^sel1]: **SEL-1** (Must): a task with ethical concerns is out, including data whose subjects or creators ask that it not be used for ML. Marker: `Ethical Issue`. Cases: the Pima Indian Diabetes Dataset. A Must the definition can fix is fixed rather than excluded (principles.md, "How to decide", the remedy ladder).
   [^law]: Lei 12.711/2012 (https://www.planalto.gov.br/ccivil_03/_ato2011-2014/2012/lei/l12711.htm), ADPF 186 (STF, 2012), LGPD art. 5 II and art. 11 II b (https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2018/lei/l13709.htm), from the column auditor and the domain practitioner (the LGPD from secondary commentaries); MEC CPOP edital 2026 (https://www.gov.br/mec/pt-br/cpop/documentos/edital-cpop-2026.pdf). The employment bar of rais, Lei 9.029/1995 art. 1, covers "acesso à relação de trabalho, ou de sua manutenção", not educational support.
   [^contra]: principles.md, "Consistent judgement": a precedent that contradicts a rule is flagged, not followed; one of the two is wrong.
   [^chile]: chile_school_dropout_mineduc_1m, its SEL-1 note: "sex stays an input; the use case offers support, not a decision against the student".
   [^assamflag]: The Assam record's workbook flag: "Prediction uses caste and gender".
   [^row]: principles.md, Tensions, "A rating factor known at the prediction point against a factor the actor may no longer use" (P3 and P4; USE-1, USE-6): the actor's legal constraint today; bemtpl97 (Lennart, 2026-11-05) and australian_vehicle_insurance_2004_2005 (Lennart, 2026-11-08); its extension to any decision the actor's own law constrains is proposed in rais_employment_separation_1m's issue 1.

**Review panel:** ship after changes (mediator). Tier full: claim auditor, column auditor, split auditor, domain
practitioner, blind reviewer, task gamer, precedent checker, advocate and critic with one rebuttal each, mediator (with
one decisive check of the 2023 blank second day). Claim audit: 44 claims and the proposed warning tested; three refuted
on the data and fixed (2023's blank second day missing from the notes, 2018's school-type codes, the modality's coding
by edition), two numbers corrected (the zero counts, the registration dates), the licence left a release item. Column
audit: no leak among the 43 inputs; `school_operating_status` of undocumented timing (dropped); the two cleaning fixes.
Split audit: right with notes (the reason for the 2018 start restated, the breaks named). Domain practitioner: fit
approximate; the actor rewritten as an NGO or CPOP cursinho with its own intake form; regression ranks "below 450"
better than a classifier on the bar. Blind review: include with changes; its concerns were the undocumented sampling
(documented), the thin use case and the municipality codes. Task gamer: no exploit beyond seed noise. Debate: agreed on
the target, the split, the metric, the cleaning fixes and the notes; disputed: SEL-1 for sex and the Assam marker (issue
1), the 2023 blank second day (LEAK-22, kept after the cause check), `school_operating_status` (LEAK-10, dropped), the
actor (USE-1, rewritten) and the municipality codes (CLEAN-12, decoded).

<details><summary>Mediator</summary>

**MEDIATOR REPORT: enem_entrance_exam_scores (folder enem_entrance_exam_scores_1m), 2026-11-09**

Read: principles.md (in full), the definition and README, the record and the Assam sibling's record,
builder_report.md, and every panel report (claim auditor, column auditor, split auditor, domain practitioner, blind
reviewer, task gamer, precedent checker), with the advocate's and the critic's briefs and rebuttals. One decisive
experiment run (EV-1, section 4): scripts and outputs in the run's panel folder.

**1. RECOMMENDATION (judgment record)**
Verdict: ship after changes.
Validity: SEL-1 holds (no law bars race, sex or income for a voluntary support offer; the Tensions row "a factor the
  actor may no longer use" and its proposed rais extension do not trigger); the curator confirms it in one decision with
  the Assam sibling's `Ethical Issue` marker (issue 1). USE-1/USE-3 triggered, fixed (actor rewritten: an NGO or MEC
  CPOP cursinho asking the items on its own intake form, "for example"). USE-5 holds (ProUni's mean of five, verified).
  USE-8 holds at approximate; `Selection Bias` set, income gradient and treineiro share named. LEAK-10 clause 2
  triggered, fixed (`school_operating_status` dropped); the other 42 inputs hold. LEAK-22 holds: the 2023 blank day-2
  rows stay (EV-1 check run, no recording failure shown). LEAK-34/SPLIT-13 hold; SPLIT-1, SPLIT-10 (no gap), SPLIT-14
  (58.4%) hold; SPLIT-20 holds, reason restated and breaks named. PROV-8 holds; PROV-9 holds as the pinned snapshot.
Value: TP-1 to TP-4 hold (LightGBM R^2 0.380, RMSE 71.5 against dummy 91.6; +0.025 R^2 over linear, paired SE 0.005).
  MET-5/MET-6/MET-11 fallback rmse holds (picked the AUC-best model for "below 450" in 3 of 3 windows).
Quality: CLEAN-21 triggered three times, fixed (2018 school type, modality, "not informed" drift note); CLEAN-12
  triggered, fixed (municipalities decoded from the file's own names); CLEAN-5 holds (IN_TREINEIRO dropped).
Weighed: source + (INEP census microdata), size +, gap + (education thin), use case ours -, fit approximate -.
For the curator: issue 1 (P1, SEL-1 with the Assam marker).

**2. CHANGES TO MAKE NOW (no decision needed)**
C1. USE-1, USE-3 (Must), USE-1 Methods: rewrite use_case (and the prediction-point bullet) as "For example, an NGO or a
    public cursinho programme (MEC's CPOP), or a state department filling limited places, asks its applicants the
    registration items on its own intake form when ENEM registration closes, ...". fit_reason adds that INEP holds the
    form (Edital 30/2023, 14.8-14.9) and that a department would also hold grades and state assessment scores, absent
    here. The data does not change.
C2. USE-8 (Must; selection paragraph, 2026-10-27), selection.md "Selection bias": set `Selection Bias` on the record;
    fit_reason names the gradient (2023: 38% absent at up to 1 minimum wage against 18% above 4) and that treineiros,
    17-19% of the rows (19.1% of 2023), cannot use the edition for ProUni or FIES.
C3. USE-9 (Should): one sentence that a direct use case was asked for (a socioeconomic adjustment of school results has
    its label known, so it fails USE-9), as on chicago.
C4. USE-5 / LEAK-22, writing: an Anomaly bullet for the 2023 blank day-2 rows with the numbers of section 4 (16,029
    rows, 0.60% of 2023 against 191-417 a year before; 6.3% of the 2023 window's MSE, RMSE 76.10 against 73.89 without
    them; spread over every state and booklet; day-2 absence fell by about as much), kept as ProUni counts the zeros.
    Correct the zero counts: 275-745 a year holds for natural sciences and mathematics only; humanities 2,230-3,761,
    languages 640-1,429 (2018-2022). The builder's draft issue 3 (the target) leaves the list: every agent keeps the
    mean of five (ProUni's rule verified; the mean of four does not remove the drift, split auditor: 2021 bias +7.7
    against +1.7).
C5. LEAK-10 clause 2 (Must, amended 2026-11-08): drop `school_operating_status` and its "Potential leak" bullet. No
    census year can be traced; the rule keeps a value of unknown timing only when a traced part shows no gain. Cost:
    none measurable (group R^2 0.00016). The LEAK-30 Tensions row (transductive scaling) does not cover this mechanism.
C6. CLEAN-21 (Should), EV-2: 2018 `secondary_school_type` from the administration (codes 2 and 3 to public, 4 to
    private, code 1 at a federal school to public; no "abroad" in 2018); `secondary_school_modality` missing outside
    status 2 in every edition and 2018's EJA missing; one bullet for "not informed" years since secondary (2.5-3.2% in
    2018-2019, 8.1-10.9% from 2020); fix the SCHOOL_TYPE_2018 docstring, the CLEAN-21 and Note bullets and claim 22.
    Measured: -0.024 RMSE mean, better in 5 of 6 runs; training editions only.
C7. SPLIT-20 (Should): name the breaks of C6 in splits_comment; restate why 2017 is out: the floor does not need it and
    its essay sits on the old level (529 against 622-629 in the test editions), not the years-since cap.
C8. CLEAN-12 (Should; amended 2026-11-01): decode both municipalities as "Name (UF) [code]" from NO_MUNICIPIO_ESC and
    NO_MUNICIPIO_PROVA (check the mapping one to one). The rule reads "a column that still ships as a number while its
    source has words for it is a gap to close"; the words are in the same file, so rais's distinguishing fact (an
    outdated codebook) is absent. Settled as a change, not an issue: an amendment of CLEAN-12 is the curator's alone
    (rais issue 5); if the curator amends it there, ENEM follows the amendment.
C9. Writing (writing.md, PROV-9, EV-2): registration closes "May to July" (2021: 30 June to 14 July); the year is the
    pinned snapshot (the 2023 zip as re-published 2026-07-09), not "the newest file"; the SEL-1 note adds that the
    model serves a support offer and is not for screening anyone out (domain practitioner's reuse risk); the rows bullet
    names INEP's removal of the takers of 20 small adapted or reapplied test versions (Leia-me 2023, section 3).
C10. Accept `task_time_on_few_unique` with the precedent checker's text (D8): "six yearly editions, 2018-2023: the exam
    is held once a year, so an edition is the finest time; the history starts in 2018 (SPLIT-20) and ends in 2023 (no
    common key from 2024); a refit trains on whole editions, and an inner validation holds out the newest training
    edition".
C11. Optional, SPLIT-10: one clause that a refit from the public microdata gets edition t-1 around the close of
    registration (later for 2020 under the LGPD); no gap (a one-edition gap would leave the 2021 window 43.5%).
Not issues: the licence (EV-4: a release-checklist item, as wisconsin); the 1M train cap (declared `_1m` protocol,
0.13-0.23 RMSE); the municipality cardinality (Tensions: width against model limits); the blind reviewer's "drop
mean_score == 0" (3 rows of 200k; LEAK-22, framingham); an all-registrants binary sibling (optional, not asked).

**3. ISSUES FOR THE CURATOR (ranked)**
1. [P1, SEL-1 Must; principles.md "a precedent that contradicts a rule is flagged; one of the two is wrong"]
   Race, sex and family income stay as inputs, and the Assam sibling's `Ethical Issue` marker is settled in the same
   decision.
   - Problem: the definition keeps the three grounds. The Assam record (student_performance_on_an_entrance_examination,
     same task, caste and gender) carries `Ethical Issue` with `TBD -> Yes`, which SEL-1 does not allow (the marker
     means `No`). Every November call on protected grounds asks whether the actor's own law bars them (bemtpl97,
     australian_vehicle_insurance, rais proposed, acs proposed); here none does.
   - Effect: RMSE +0.18 to +0.20 without race; +0.25 to +0.29 without race and sex (sex alone about +0.07-0.09); +0.70
     to +0.91 without all three, on 70-76 (builder, replicated by the claim auditor).
   - Advocate: three agents found no bar (Lei 12.711/2012 and ADPF 186 use race and income for admission; LGPD art. 11
     II b; MEC's CPOP must prioritise Black, Indigenous and low-income students). Sex is covered by chile's reason,
     "the use case offers support, not a decision against the student", which this definition already states; the
     same reason keeps sex in chile, open_university, student_portuguese and early_learning. Dropping sex here alone
     would treat like cases unlike.
   - Critic: the quota law covers race and income, not sex; the pair with Assam must be settled, not set aside; a
     reason that covers sex, or sex dropped.
   - Settled by the rules: no Must fails (the Tensions row's trigger, the actor's legal constraint, is absent, also
     under the rais extension); sex is covered by the support reason already in the note, as in chile; exclusion is
     off the ladder. What the rules leave open is the Assam pair: whether a protected ground is an ethical concern by
     itself, which no rule says.
   - Decision: (a, recommended) keep all three here; reopen the Assam marker with its own issue in its record, the
     marker to become a note under the same reading (that reading may want a line in selection.md); (b) drop sex here
     and in the Assam framing (departs from chile and three shipped education datasets: name the fact); (c) drop race
     and sex as Assam's flag reads (no law asks for it); (d) decide with the rais Tensions-row amendment (issue 1 there)
     so ENEM, wioa and acs share one row.

No other issue needs a decision. The builder's draft issues 2 (present-only), 3 (target), 4 (history) and 5 (the
warning) are settled by C2, C4, C7 and C10.

**4. DISPUTED POINTS, SETTLED**
D-a. SEL-1 and sex: see issue 1. By rank SEL-1 is P1, but no Must fails, so no remedy is forced; the open part is a
     reading of SEL-1 for the curator, and the Assam marker is the inconsistent precedent (flagged, not followed).

D-b. The 2023 blank day-2 rows: keep (LEAK-22, framingham). Decisive check (EV-1), full raw files, day-2 present:
     - Size: 2023 16,345 day-2 participants with both answer strings fully blank (16,029 of them present on day 1,
       the rows the cohort keeps), 0.61%; 2022: 320 (0.014%).
     - Not one booklet: the four regular booklets 0.60-0.62% each; adapted booklets 1225-1229 0.66-1.55%; the four
       130x booklets 2 of 5,204.
     - Not one place: every state, RR 0.23% to SC 1.33% (SP 0.43%, RJ 0.88%), all 30+ times their 2022 rates; the 72
       exam municipalities with 5,000+ participants range 0.13%-1.77% (median 0.56%). Some clustering (chi^2/dof 6.48,
       2022 0.93), but the ten municipalities with most excess hold 12.5% of the rows against 8.3% of participants.
       Students' school municipality: chi^2/dof 1.98. No lost batch of answer sheets shows.
     - Graded like absence: state schools 0.67%, private 0.19%, federal 0.24%; income band A 0.78% to M 0.39%;
       treineiros 0.79%, finishing this year 0.52%; sex neutral.
     - Day 1 normal: 1.9% of their day-1 items blank, against 0.6% for the others (2022's few: 15%).
     - A spike at exactly all 90 items blank: partial blanks barely moved (80-89 blank: 158 against 58 in 2022; 45-79:
       1,460 against 1,189).
     - Day-2 absence among day-1 participants fell: 5.59-6.12% in 2018-2022, 5.04% in 2023, while present-and-blank
       rose from 0.008-0.012% to 0.568%. So most of these rows look like people who would have been recorded absent
       on day 2 in earlier editions: either day-2 presence was recorded differently in 2023, or more people came,
       signed in and left without answering.
     Reading: no recording failure of the score is shown. INEP published a zero and ProUni counts it, so the rows can
     have the outcome and have it (LEAK-22, framingham). A filter on blank answer strings would read the label's raw
     material, which LEAK-25's recovery rule does not allow. Keep, with the C4 note. Reopen if INEP documents a change
     in how day-2 presence was recorded in 2023 (then they are absentees under a new code, and presence harmonised
     across editions is a repair, PROV-13). The 2024 RESULTADOS file (presence and answer strings) would show whether
     this is a lasting regime; not run.

D-c. `school_operating_status`: drop (C5). Both sides now agree; LEAK-10 clause 2 (P4 Must) is the specific rule; the
     LEAK-30 row covers another mechanism.

D-d. USE-1 "holds" or "triggered, fixed": triggered, fixed by C1 (the actor as written cannot hold the inputs; the
     remedy is text, the first rung).

D-e. CLEAN-12 municipalities: decode (C8), by the rule as written; the batch amendment stays with rais issue 5.

**5. THE TASK GAMER'S EXPLOITS, MAPPED**
| Exploit | Rule | Note or warning | New or known | Measured gain | Issue? |
| Municipality counts over train+test rows | LEAK-30 (transductive) | none needed | new | -0.008 to -0.040 (noise +-0.03) | no |
| Repeat takers matched across editions | LEAK-34, SPLIT-13 | Note on repeat registrants | known | +0.009/+0.007/-0.003; 0.14-0.28% matched | no (gain matches the note: none usable) |
| Test-year make-up per exam municipality | LEAK-30 | none needed | new | -0.012/+0.022/+0.048 | no |
| 1M train cap discards earlier rows | row budget protocol | version_comment, splits_comment | known | 0.13-0.23 RMSE (honest model hurt) | no |
| 'abroad' and EJA only in 2018 | CLEAN-21 | fixed by C6 | known | training only | no |
Nothing beats the honest model beyond seed noise; the best single feature scores 85.4 against 75.5.

**6. AGREED FACTS**
- Source: INEP microdata, one zip per edition, sha256 pinned; 2023 zip re-published 2026-07-09; footer CC BY-ND 3.0,
  the zips state none. From 2024 the registrants and scores sit in two files with no key.
- Rows: 17,445,513 participants present at all four tests, 2018-2023, 45% (2020) to 73% (2019) of registrants; a
  uniform 25% per edition (means within 0.15 points of the full data).
- Presence follows income and school status: 2023, up to 1 MW 61.8% present, above 4 MW 81.7%; status 1 58.4%,
  treineiros 82.5%. Treineiros are 17-19% of the rows and cannot use the edition for ProUni or FIES.
- 43 inputs, all on the registration form (Edital 2023 5.2.3, 5.2.5, 5.4.1); every exam-day column is out.
- Target: ProUni's mean of five ("450 pontos de média nas notas das cinco provas", essay > 0, MEC 2023 kit); the
  essay-zero condition changes the call for 0.07-0.18% of rows.
- Split: temporal by edition, tests 2021/2022/2023, train shares 58.4/71.2/84.6%; scores out before the next
  registration closes; repeat takers unlinkable (dictionary note 1); exact copies across the split 0.0%, 1-NN R^2 -0.24.
- Signal: LightGBM RMSE 71.5 against dummy 91.6, replicated three times; regression ranks "below 450" better than a
  classifier on the bar (AUC 0.775-0.782 against 0.759-0.768).
- SEL-1 costs as in issue 1; no law found that bars the grounds for this use.
- 2018 TP_ESCOLA is the school's administration (code 3 municipal: 9,711 of 9,762); modality filled for status 1 in
  2018-2019 only, EJA in 2018 only; "not informed" years since secondary up from 2020. Fixes -0.024 RMSE.
- `school_operating_status`: census year undocumented; 0.17% non-active; gain 0.00016.
- 2023 blank day-2 rows: 16,029, 6.3% of the 2023 window's MSE; cause section 4.
- Essay level: 529 (2017), 516 (2018), about 580 (2019-2020), 622-629 (2021-2023).
- Municipality names (NO_MUNICIPIO_ESC, NO_MUNICIPIO_PROVA) are in the same CSV.

**7. CONSISTENCY WITH PRECEDENT (precedent checker D1-D10)**
- D1 SEL-1: consistent with chile (sex kept, "support, not a decision against"), open_university, student_portuguese,
  early_learning; race kept in diabetes_130_us, kumc, sinan; the legal-constraint frame of bemtpl97, rais and acs. The
  Assam marker is the contradicting precedent: issue 1.
- D2 use case ours: consistent after C1 ("for example", as wioa, acs) and C3 (USE-9, as chicago).
- D3 presence selection: consistent after C2 (`Selection Bias` as tunisian, lt_vehicle_loan, kumc, sinan).
- D4 zeros and blank rows kept: framingham (LEAK-22); a quantified note as chicago_traffic_crashes.
- D5 history from 2018: chile; breaks named as chile's panel required (C7).
- D6 fallback rmse: gallstone_disease, ljubljana_breast_cancer (MET-7: no invented threshold).
- D7 municipalities: decoding follows CLEAN-12 as written and ny_wcb ("words [code]"). It departs from chile's
  mediator (C13: communes as codes "an application of CLEAN-12") and from rais, sinan and chile keeping IBGE or commune
  codes; the fact that sets ENEM apart: the names sit in the same file, one to one, so no outside or outdated table is
  needed. If the curator amends CLEAN-12 with rais issue 5, ENEM follows; without C8 it would be the fourth exception
  of one reason.
- D8 warning: wisconsin, spanish_homeowners, tunisian (C10 states why no finer time).
- D9 licence: EV-4, wisconsin (no issue).
- D10 year: PROV-9 snapshot clause, chicago_traffic_crashes, fpa_fod_wildfire_cause_1m (C9 wording).
- Register: no flag names this dataset; no drift found.

</details>

<details><summary>Claim audit</summary>

**CLAIM AUDITOR REPORT: enem_entrance_exam_scores (folder enem_entrance_exam_scores_1m), 2026-11-09**

Verdict: ship after changes. No Must is broken. Every feature is known at registration and the metric is computable
on every fold. There are three refutations on the data, all fixable in `_clean`:
  (1) a target artefact that appears in the 2023 test window only;
  (2) 2018's school-type codes are not the dictionary's;
  (3) the secondary-school modality changes coding across editions without a note.
There are also three wording errors and one licence question for the curator.

Scratch, in the run's panel folder: one pass over the six raw CSVs; the zeros' RMSE effect; the definition's
container, scorer and splits; the Leia-me and edital text of 2018 and 2023, extracted from the zips.

**Judgment record**
Validity: SEL-1 open (curator's call, evidence replicated); USE-8 holds (approximate, the presence selection measured);
USE-5 holds for the definition, but the 2023 test window carries an artefact that is 40 times the training rate
(finding 1); LEAK-10 holds (all 43 inputs are on the registration form, edital 2023 5.2.3, 5.2.5, 5.4.1); SPLIT-14
holds (58%); PROV-9 and PROV-10 hold.
Value: MET-1/MET-5/MET-11 fallback rmse holds; MET-2 computable on 3 of 3 folds.
Quality: CLEAN-21 refuted twice (2018 TP_ESCOLA, TP_ENSINO across editions); CLEAN-5 holds (IN_TREINEIRO).
For the curator: finding 1 (keep the 2023 blank day-2 rows, or define the cohort as "answered on both days"), and the
ND licence (finding 8).

**Table: claim | source | test | result | evidence | rule**
(The numbers are claims.md's.)

1 | Source: INEP microdata page | claims 1; dataset.py source_url | fetched the page | holds | lists 1998-2025, one zip per year | PROV-8
2 | Year 2026 = the 2023 zip's Last-Modified | claim 2 | HEAD on the 2023 zip, today | holds | Last-Modified Thu, 09 Jul 2026 21:55:51 GMT, 549,511,687 bytes | PROV-9
3 | Licence CC BY-ND 3.0 from the footer | claim 3; license | fetched the page footer; dados.gov.br (JS only); web search | holds as quoted; see finding 8 | footer: "Todo o conteúdo deste site está publicado sob a licença Creative Commons Atribuição-SemDerivações 3.0 Não Adaptada"; no licence in the Leia-me 2018/2023 (grep "licen", "creative": none) | EV-4
4 | BibTeX cites INEP | claim 4 | read | holds | | PROV-10
5 | Download sizes and sha256 | claim 5; download_description | sha256sum of the six zips | holds | all six sums equal those in download_description | -
6 | 2023 nests the CSV in microdados_enem_2023/ | claim 6 | zip listing | holds | microdados_enem_2023/DADOS/MICRODADOS_ENEM_2023.csv | -
7 | Use case: at the close of registration, rank registrants for free preparation classes against ProUni/FIES's 450 bar | claim 7; task_summary | ProUni rules (MEC press kit, editais via web search) | holds, with a gap (finding 7) | ProUni bars an edition taken as treineiro; status-3 rows are 19.1% of 2023 participants | USE-1, USE-5
8 | ProUni/FIES: mean >= 450 over five tests, essay > 0 | claim 8 | web search (MEC's PROUNI_2023_1 kit; guidance pages for FIES) | holds for ProUni; FIES only from secondary pages | "ter alcançado, no mínimo, 450 pontos de média nas notas das cinco provas", essay above zero | USE-5
9 | Registration closes May to June | claim 9; curation_comments | edital 2018 (7-18/05/2018), edital 2023 (5/6-16/6/2023), web search for 2021 | refuted (wording) | ENEM 2021 registration ran 30 June to 14 July 2021 | writing
10 | Scores out before the next registration closes (no gap) | claim 10; splits_comment | dates of 2020 results (Mar 2021) against the 2021 registration (Jul 2021) | holds (from knowledge plus the 2021 dates) | | SPLIT-10
11 | Questionnaire answered at registration | claim 11 | edital 2023 5.4, 5.4.1; edital 2018 4.3, 4.6 | holds | "Os dados informados no Questionário Socioeconômico e os referentes à situação do ensino médio não poderão ser alterados" (registration system) | LEAK-10
12 | Exam municipality and language chosen at registration | claim 12 | edital 2023 5.2.3, 5.2.5, 5.2.6 b | holds | "Indicar a unidade da federação e o município onde deseja realizar o Exame"; the language "escolhida no ato da inscrição"; both can change only during registration | LEAK-10
13 | Rows: present at all four tests; counts per edition | claim 13; decision 1 | full pass over the six CSVs | holds exactly | registrants and scored counts equal to the digit; 2019 has one present row without a score | USE-8
13b | (implicit) the presence filter is a selection known only after the exam | fit_reason | presence rate by Q006 band and status, full data | holds (fit approximate is right) | 2023: income A 58.0% present, P 83.8%; 2020: A 37.2%, M 67.0%; status 1 58.4% against status 3 82.5% (2023) | USE-8, LEAK-22
14 | Uniform 25% per edition | claim 14; version_comment | sample against full mean, SD and share below 450 per edition | holds | means differ by at most 0.15 points (2023 540.69 against 540.61), SD by at most 0.16, share below 450 by at most 0.0007 | -
15 | Target mean of five, frame stats | claim 15 | README data checks; container | holds | mean 534.4, SD 89.0 | USE-5
16 | Zeros: 2023 CN 16,167 and MT 16,302; "275 to 745 per test in 2018-2022"; jump unexplained | claim 16; curation_comments | full pass | 2023 counts hold; the range is refuted (wording); the jump is a test-only artefact (finding 1) | 2018-2022 CH zeros are 2,230-3,761 and LC 640-1,429; the 275-745 range is CN and MT only. 2023 CN and MT both zero: 16,029, against 191-417 per year before | USE-5, writing
17 | Essay zeros 2.1%-4.2%; 2023 3.5% | claim 17 | decision 2 table | holds | 0.0206 to 0.0421; 2023 0.0346 | -
18 | Below 450: 13.3% to 21.1% | claim 18 | full and sample | holds | full: 13.32% (2022) to 21.05% (2020) | -
19 | 43 inputs (1 + 17 + 25) | claim 19 | feature_columns(container) | holds | 43 columns, none from the exam days | -
20 | Exam-day columns dropped | claim 20 | feature list | holds | no presence, CO_PROVA, TX_*, status or score column | LEAK-10
21 | IN_TREINEIRO == status 3 from 2019; 2018 differs | claim 21 | raw_facts crosstab, re-read; dictionary note 3 (2018 by age, 2023 by status) | holds | 2019-2023: status 3 iff flag 1 on every sampled row; 2018: 9,923 status-3 rows not flagged | CLEAN-5
22a | 2018 marital codes 0-3 = single to widowed | claim 22; MARITAL_2018 | 2018 against 2019+ code distributions | holds | 2018: code 0 89.19%, blank 3.23%; 2019-2023: code 1 88.98%-92.31%, code 0 ("not informed") 3.15%-3.86% | CLEAN-21
22b | 2018 TP_ESCOLA 3 = abroad, 4 = private (swapped onto 2019+) | claim 22; SCHOOL_TYPE_2018 | 2018 TP_ESCOLA against TP_DEPENDENCIA_ADM_ESC, full 2018 data | REFUTED for code 3 and for federal schools (finding 2) | 2018 code 3: 9,711 of 9,762 rows at municipal schools in Brazil (none abroad); code 2: 840,241 at state schools; code 4: 237,816, all private; all 42,666 federal-school students are code 1 ("Não respondeu") | CLEAN-21, CLEAN-12
23 | Income bands are multiples of the minimum wage | claim 23 | dictionaries 2018-2023, B and Q bounds | holds | 954/19,080; 998/19,960; 1,045/20,900; 1,100/22,000; 1,212/24,240; 1,320/26,400 (1x and 20x) | CLEAN-21
24 | Years since secondary capped at "12 or more" | claim 24; YEARS_SINCE_CAP | dictionaries (2018 code 12, 2019 13, 2020 14, 2021 15, 2023 17 = "Antes de 2007"); shipped shares by edition | holds | "12 or more" 14.5%, 14.2%, 15.2%, 14.0%, 12.4%, 14.0% of the known values, 2018 to 2023 | CLEAN-21
24b | (implicit) "not informed" (0) means the same in every edition | - | status-1 share of code 0 by edition | weak drift, unnoted | 2.5% (2018), 3.2% (2019), then 10.9%, 8.1%, 8.1%, 8.9% (2020-2023) | CLEAN-21 (note)
25 | School items only for status 2; TP_ESCOLA only status 2 | claim 25 | raw_facts re-read | holds | | -
25b | "the modality (TP_ENSINO) of those who have finished or are finishing" | curation_comments note | TP_ENSINO filled by edition and status | REFUTED (finding 3) | status 1 filled 54.0% (2018), 49.7% (2019), 0.0% (2020-2023); EJA 7.19% of 2018's known values, 0 in every later edition | CLEAN-21
26 | Proxy missing codes | claim 26 | dictionaries | holds | race 6 is in the 2021+ dictionaries but has 0 rows in the sample (harmless) | CLEAN-10
27 | Q003/Q004 "grupos ordenados" | claim 27 | dictionary 2023 Q003 text | holds | "algumas ocupações divididas em grupos ordenados" | CLEAN-14
28 | Q005 1 to 20 | claim 28 | dictionary 2023 | holds | the last options are 18, 19, 20 | CLEAN-14
29 | 5,551 and 1,750 municipalities | claim 29 | README feature summary | holds | | -
30 | Duplicates 0.14%; 0.0% exact copies across the split | claim 30 | builder's duplicate log and probe 5 re-read (not re-run) | holds (not re-run) | | LEAK-16, LEAK-18
31 | Quota law uses race and income | claim 31 | knowledge (Lei 12.711/2012: public-school, income and PPI sub-quotas) | holds (not re-read) | | SEL-1
32 | Repeat takers cannot be linked | claim 32 | dictionary 2023 note 1 | holds; the copies across the split are untestable | "O mesmo NU_INSCRICAO para anos diferentes não identifica o mesmo participante" | LEAK-34, SPLIT-13
33 | Splits 2023/2022/2021, 1M train / 500k test | claim 33 | container splits | holds | train editions 2018-2022 / 2018-2021 / 2018-2020; test 500,000 of one edition each; no overlap | SPLIT-1
34 | 2021 window trains on 58%; from 2019 46%; 2017 cap code 11 | claim 34 | arithmetic on the counts; dictionary 2017 | holds | 10,184,319 / 17,445,513 = 58.4%; 6,290,590 / 13,551,784 = 46.4%; 2017 "Antes de 2007" = 11 | SPLIT-14
35 | 2020: 55% absent | claim 35 | full pass | holds | 2,588,681 of 5,783,109 present at all four tests = 44.8% | -
36 | From 2024, two files with no key | claim 36 | not re-read (the record's size check) | untested | the 2024 zip exists (526,073,856 bytes, Last-Modified 2026-07-09) | -
37 | Metric: fallback rmse | claim 37; Metric.fallback | looked once more (web search); scorer on every fold | holds | studies report MAE and R^2 (a UFC course project on 2018: MAE 58.3, R^2 0.38; an SBC paper: MAE 65.9 against 97.27); no single deliberate choice and no task named by INEP (MET-5). Scorer: dummy rmse 95.990 / 89.425 / 89.635, equal to the manual RMSE; 500k test rows per fold; no scoring columns needed | MET-1, MET-2, MET-5, MET-11
37b | (implicit) RMSE scores the use case's decision | MET-1 | reasoning | holds, weighed | The use case acts near 450, and RMSE weighs errors at 700 as much. The task makes no other metric obvious, and the source fixes no threshold for scoring (MET-6): fallback correct | MET-1, MET-6, MET-11
38-39 | Leak and task probes | claims 38-39 | independent LightGBM on raw codes, 300k train per window | holds | RMSE 70.17 / 70.39 / 76.10 (2021/2022/2023) against the builder's 70.22 / 70.43 / 76.00 | TP-1 to TP-4
40-43 | Hidden-group, dtype and generated probes | probe logs | re-read | holds | | -
44 | SEL-1 RMSE costs | claim 44 | re-read the builder's script; the base RMSEs replicated (row 38-39) | holds | | SEL-1
F | school_operating_status from a census of undocumented year (kept, potential leak) | curation_comments | dictionaries 2018-2023 and Leia-me 2023 (no census year; "da escola que ele declarou ter frequentado"); non-active share and score by status | holds; untested for the year | non-active is 0.31% (2018) to 0.94% (2023) of the rows with a school; their mean score is higher (556-576) than for active schools (535), not lower; too small to carry a leak | LEAK-10 (weak), LEAK-30

**Refuted and untested, ranked (principles.md: validity first, Must first, then effect)**

1. (P3/P5, USE-5 Must, applied as a judgement on what the target means in the test window; implicit claim refuted)
   The 2023 test window carries a target artefact that training has 40 to 80 times less of. 16,029 participants of
   2023 (0.60%) were present on day 2 but left both natural sciences and mathematics fully blank (answer strings all
   "."). In 2018-2022 there were 417, 344, 319, 191 and 247 such participants (0.005%-0.011%).
   - They are spread evenly over the four regular booklets (1221-1224: 3,967 / 4,054 / 4,046 / 3,893), so the cause is
     no single booklet. 13,219 of them wrote a normal essay (status 1). Their day-1 mean is 478 and their target mean
     is 281.
   - Effect: in an untuned LightGBM (300k train rows, raw codes), these rows are 0.59% of the 2023 test rows and carry
     6.3% of its MSE: RMSE 76.10 with them, 73.89 without. In 2021 and 2022 the same rows carry 0.1%-0.2%.
   - The +2.2 RMSE is about a third of the gap between the 2023 window and the other windows, and 10 times the SEL-1
     differences. These rows are not "a registrant who did badly". A model can never see this behaviour in training.
     The cause is untested: no INEP note was found (web search, Leia-me 2023).
   - What it changes: the newest window partly scores a 2023-only recording or behaviour quirk.
   - Mildest remedies, for the curator:
     (a) keep, and make the note quantitative: the RMSE effect above, and "test-only".
     (b) define the cohort as "present and answered at least one item on each day": filter rows whose four answer
         strings for a day are all blank, in every edition (the strings are read in `_prepare_raw_files` only for the
         filter, never as features). This removes 0.6% of 2023 and about 0.01% elsewhere. It departs from ProUni's
         mean for those rows, but matches "sat both days" in the task summary.
   I lean to (b) or (a) with the note. Draft issue 3 should carry the number.

2. (P7, CLEAN-21 Should; claim 22 refuted for TP_ESCOLA) 2018's school-type codes are not those of the 2018
   dictionary. In the full 2018 file, TP_ESCOLA is a function of the school's administration:
   - 2 = state: 840,241 of 840,392.
   - 3 = municipal: 9,711 of 9,762 rows, all at Brazilian schools with a municipality code.
   - 4 = private: 237,816 of 237,816.
   - 1 ("Não respondeu"): all 42,666 federal-school students, and everyone without an identified school.
   Consequences of SCHOOL_TYPE_2018:
   - The municipal-school students become "abroad". The shipped "abroad" level is 0.89% of 2018's known school types
     and 0 rows in every other edition; "Exterior" is gone from the 2021+ dictionaries.
   - Federal-school students, the strongest public-school group, are missing in 2018 and "public" from 2019 on.
   - Whoever has no identified school is missing in 2018. In 2019 they answered: 181,319 public and 81,915 private
     without a school, full data.
   What it changes: the levels of `secondary_school_type` mean other things in the 2018 training rows. The effect on
   scores is small, because `school_administration` carries the same information.
   Mildest remedy: for 2018, map code 3 to public (2) and leave federal and the rest as they are, or blank 2018's
   `secondary_school_type` altogether (it adds nothing beyond `school_administration`). Drop the "abroad" level, or let
   it stay empty. Correct the note "2018 codes abroad 3 and private 4".

3. (P7, CLEAN-21 Should; the README note on TP_ENSINO refuted) `secondary_school_modality` changes coding across
   editions without a note.
   - Status-1 registrants (already finished, about 45% of the rows) have a modality in 54.0% of 2018 and 49.7% of 2019,
     and never from 2020 on (0.0%: the "modelo simplificado").
   - The EJA level exists only in 2018 (7.19% of its known values). The 2019-2020 dictionaries list it but no row has
     it, and 2021+ dictionaries drop it.
   - The 2019+ status-2 rows with a missing modality (1.9%-5.4%) score 454-466, like 2018's EJA (471). So EJA appears
     to have become "missing" from 2019 on.
   What it changes: a feature level and a missingness pattern that exist only in the oldest training editions. The
   README's "the modality of those who have finished or are finishing" is wrong for every test window.
   Mildest remedy: blank TP_ENSINO for status 1 in 2018-2019 and map 2018's EJA (3) to missing, to match how 2019-2023
   code it, with a CLEAN-21 bullet. Or drop the column.

4. (P7, CLEAN-21, note only) "Not informed" (0) of TP_ANO_CONCLUIU for status-1 registrants rises from 2.5%/3.2%
   (2018/2019) to 8.1%-10.9% (2020-2023). This is likely the same 2020 change. It is a missingness shift in
   `years_since_secondary`. Remedy: one sentence in the notes.

5. (P3 weigh, USE-1/USE-5; claims 7-8) ProUni bars an edition taken as treineiro, so the 450 bar does not apply to
   status-3 rows: 19.1% of 2023 participants and 17-19% of the earlier editions. The use case still stands, since
   free preparation is useful to them too. Remedy: half a sentence in use_case or fit_reason ("for those who finish
   secondary school; practice takers cannot use the edition for ProUni").

6. (writing; claim 16) "275 to 745 per test in each of 2018 to 2022" holds only for natural sciences and mathematics.
   Humanities has 2,230-3,761 zeros a year and languages 640-1,429. Fix the wording (decision 2's table already shows
   the shares).

7. (writing; claim 9) "Registration closes in May to June": ENEM 2021's registration ran from 30 June to 14 July 2021.
   Write "May to July".

8. (EV-4, release checklist; claim 3) The footer licence is CC BY-ND 3.0. "SemDerivações" forbids sharing adapted
   material, and the container is a recoded 25% sample, which is a derivative. Whether the site's footer licence
   binds the microdata at all is unsettled: the zips and Leia-me state none, a CMRI decision calls them free to share,
   and dados.gov.br rendered no licence. The same question is open on rais_employment_separation_1m and
   sinan_dengue_case_screening_1m. Not a rule violation. A question for the curator and the release.

**Untested**
- The cause of 2023's blank day-2 tests: no INEP document found (Leia-me 2023, web search). Finding 1 stands on the
  effect, not the cause.
- The census year behind `school_operating_status`: undocumented. The magnitude is measured and negligible (row F).
- Copies of a person across the split (repeat takers): cannot be linked by design (dictionary note 1, LEAK-34).
- From 2024, two files without a key (claim 36): rests on the record's size check.
- The FIES 450 rule from an official MEC page: secondary pages only.
- The duplicate counts (claim 30): the builder's log was re-read, not re-run.

Sources used: INEP Microdados do Enem page (footer licence); MEC PROUNI_2023_1 press kit and ProUni guidance pages
(web search); ENEM 2021 registration dates (infoescola, Metrópoles, Estratégia, via web search); studies of ENEM score
prediction (SBC CTIC, UFF, UFABC, via web search); Edital Enem 2018 and 2023, Leia-me 2018 and 2023, and the
dictionaries 2017-2023 inside the zips.

</details>

<details><summary>Column audit</summary>

COLUMN AUDITOR REPORT: enem_entrance_exam_scores_1m (record enem_entrance_exam_scores), 2026-11-09

Verdict: ship after changes. No leak among the 43 inputs. Two cleaning problems (P7, cheap and safe fixes), one weak
timing question (P4, school_operating_status), and the SEL-1 call stays with the curator: I found no law that bars
race, sex or income for this use case, so the rais "the actor's own law bars the factor" stance does not apply.

Validity: SEL-1 open (curator's call, no legal bar found); LEAK-10 holds for 42 inputs, one weak question
(school_operating_status, clause 2); USE-3 prediction point as written (close of registration).
Quality: CLEAN-21 triggered twice (2018 school type is another variable, decoded wrongly; modality recorded
differently by edition); CLEAN-10, CLEAN-12, CLEAN-14 hold otherwise.

Read: dataset.py, builder_report.md, claims.md; INEP dictionaries 2018-2023 (extracted from the zips);
Leia-me 2018 and 2023 and Edital 30/2023, taken out of the zips;
principles.md, use_case.md, leak_checks.md, cleaning_features.md, selection.md SEL-1. Measured: the 25% sample
parquet (raw codes) and the shipped frame (the builder's cached frame, 2.5M rows, 44 columns); dtype probe re-run on the
current definition (same 19 flags as the builder's); LightGBM effect of the two fixes (scripts in the run's panel
folder).

**COLUMN TABLE (column | meaning, from the dictionary | known at registration close? | dtype and cleaning | verdict | rule)**
edition | NU_ANO, the ENEM year | yes (time index) | int16 | fine | -
age_band | TP_FAIXA_ETARIA, age on 31 Dec of the edition year (note 2), 20 bands | yes (birth date) | ordered cat, 20 levels "under 17" < ... < "over 70", order as dictionary; open_end flag = band ends, intended | fine | CLEAN-14
sex | TP_SEXO M/F | yes (form, from the Receita Federal record, Edital 5.3) | cat 2 levels | fine; protected ground, see SEL-1 | SEL-1
marital_status | TP_ESTADO_CIVIL | yes | cat 4 levels; 2018 codes 0-3 shifted onto 1-4 (data agrees: 2018 code 0 = 89.2%, 2019 code 1 = 89.0%); 2019+ 0 "Não informado" and 2018 nulls (3.2%) missing | fine | CLEAN-21, CLEAN-10
race | TP_COR_RACA | yes | cat 5 levels; 0 "Não declarado" and 6 "Não dispõe da informação" (2021+) missing | fine; protected ground, see SEL-1 | CLEAN-10, SEL-1
nationality | TP_NACIONALIDADE | yes | cat 4 levels; 0 missing | fine | CLEAN-10
secondary_school_status | TP_ST_CONCLUSAO | yes; "não poderão ser alterados" (Edital 2023, 5.4.1) | cat 4 levels, unordered (not one scale) | fine | CLEAN-14
years_since_secondary | TP_ANO_CONCLUIU, counts back from the edition to "Antes de 2007" (12 in 2018 ... 17 in 2023) | yes | ordered cat "1".."11","12 or more"; cap at the 2018 last level is the one common scale (2018 code 12 = 12+ years; 2023 codes 12-17 = 12+); 0 missing (not informed, and every status 2-4 registrant) | fine | CLEAN-21, CLEAN-14
secondary_school_type | TP_ESCOLA | yes (2019+ self-report at registration); 2018: the identified school's administration | cat public/private/abroad | CLEANING PROBLEM (issue 2 below): 2018 is another variable and its code 3 is municipal school, decoded as "abroad" | CLEAN-21, EV-2
secondary_school_modality | TP_ENSINO | yes | cat 3 levels | CLEANING PROBLEM (issue 3): filled for "already completed" in 2018-2019 only; EJA level 2018 only, missing in 2019+ | CLEAN-21
school_municipality | CO_MUNICIPIO_ESC, IBGE 7-digit code of the declared school | yes (school declared at registration; Leia-me 2023 "da escola que ele declarou ter frequentado") | cat 5,551 levels, string codes; numeric_levels flag answered: a code, category by meaning; the state part ships as school_state | fine | CLEAN-14
school_state | SG_UF_ESC | yes | cat 27 | fine (coarser level of the municipality, not a copy) | CLEAN-5
school_administration | TP_DEPENDENCIA_ADM_ESC (federal/state/municipal/private), census attribute | yes (stable school attribute) | cat 4 | fine | -
school_location | TP_LOCALIZACAO_ESC urban/rural | yes | cat 2 | fine | -
school_operating_status | TP_SIT_FUNC_ESC active/suspended/closed/closed in an earlier year, from a school census of undocumented year | UNCERTAIN | cat 4 | QUESTION (issue 4): weak, carries no measurable signal | LEAK-10 clause 2
exam_municipality | CO_MUNICIPIO_PROVA, IBGE code of the exam municipality | yes: chosen at registration, changeable only "durante o período de inscrição" (Edital 30/2023, 5.2.6 b); INEP stated in 2023 that no registrant was placed outside the chosen municipality (press, below); the room is assigned later and is not in the data | cat 1,750, string codes; numeric_levels flag answered as above | fine | CLEAN-14, LEAK-10
exam_state | SG_UF_PROVA | yes | cat 27 | fine | -
foreign_language | TP_LINGUA 0 English, 1 Spanish | yes: chosen at registration (Edital 5.2.5, changeable in the registration period only) | cat 2 | fine | -
father_education, mother_education | Q001, Q002 | yes: questionnaire at registration, not alterable (Edital 5.4.1) | ordered cat A<...<G as the dictionary; H "Não sei" missing | fine | CLEAN-14, CLEAN-10
father_occupation, mother_occupation | Q003, Q004, "grupos ordenados" 1-5 | yes | ordered cat group 1 < ... < group 5; F "Não sei" missing | fine | CLEAN-14, CLEAN-10
household_size | Q005, 1 ("moro sozinho") to 20, no "or more" level in any edition | yes | float32 number | fine | CLEAN-14
family_income | Q006, 17 bands | yes | ordered cat A<...<Q, labelled in minimum wages; checked every dictionary: B = 1 wage and Q = over 20 wages in each of 2018-2023 (954, 998, 1,045, 1,100, 1,212, 1,320); open_end flag = top band, intended | fine; protected ground (SEL-1) | CLEAN-21, CLEAN-14
domestic_worker | Q007, days a week | yes | ordered cat no < 1-2 < 3-4 < 5+ | fine | CLEAN-14
bathrooms, bedrooms, cars, motorcycles, refrigerators, freezers, washing_machines, clothes_dryers, microwaves, dishwashers, colour_tvs, mobile_phones, computers | Q008-Q017, Q019, Q022, Q024: count of the item, "Sim, quatro ou mais" the cut | yes | ordered cat "0"<"1"<"2"<"3"<"4 or more"; open_end flags answered: the cut end as a level, the lossless form | fine | CLEAN-14
vacuum_cleaner, dvd_player, pay_tv, landline, internet | Q018, Q020, Q021, Q023, Q025 yes/no | yes | cat No/Yes | fine | CLEAN-14
(target) mean_score | mean of NU_NOTA_CN/CH/LC/MT/REDACAO | published ~3 months after the exam | float | fine | -

Questionnaire items Q001-Q025 have identical wording and codes in all six dictionaries (diff with the reais amounts
masked: only 2018's extra Q026/Q027 differ).

Dropped and not read, checked: the presence (filter, then dropped), CO_PROVA_*, TX_RESPOSTAS_*, TX_GABARITO_*,
TP_STATUS_REDACAO, NU_NOTA_COMP1-5 and the five scores are all exam-day or later: correctly out (LEAK-10). NU_INSCRICAO
is a mask that links nothing (note 1): correctly out (CLEAN-3). NO_MUNICIPIO_*, CO_UF_*: copies, correctly out
(CLEAN-5). IN_TREINEIRO equals status 3 on every 2019-2023 row (claims 21, the builder's raw facts): correctly out (CLEAN-5).
2018 Q026 (a copy of the status) and Q027 (school-type history) asked in 2018 only: out under CLEAN-8; Q027 is the
2018 self-report of the school type, relevant to issue 2.

No column encodes the label, no missingness is caused by the outcome (every row was present on both days; the
school-item missingness follows the status and INEP's school match, both fixed at registration), and no input is a
window ending at the outcome.

**PROBLEMS, RANKED (principles.md: P1 first, then strength, then size)**

1. SEL-1 (P1, Must; the curator's call): race, sex and family income as inputs. Question asked: does the actor's
   own law bar them for this use case (the rais extension)?
   Finding: no bar that I found. Evidence and its standing:
   - The rais precedent rests on Lei 9.029/1995 art. 1, which bars discriminatory practices "para efeito de acesso à
     relação de trabalho, ou de sua manutenção": an employment law, which does not reach educational support.
   - Brazilian law endorses affirmative action in education rather than barring it: Lei 12.288/2010 (Estatuto da
     Igualdade Racial) defines "ações afirmativas" as programmes adopted by the State and private actors, and a
     summary attributes to its art. 15 a duty of affirmative action in education (secondary sources, text not read);
     Lei 12.711/2012 uses race and family income in federal admission; the STF upheld race-based admission policies
     (ADPF 186, 2012; from knowledge, not re-read).
   - LGPD: racial origin is sensitive data; public administration may process it without consent to carry out public
     policies provided by law (art. 11, II, b), with the non-discrimination principle (art. 6, IX) and publicity of
     the basis (art. 11 para. 2) (secondary sources, text not read). Sex and income are not sensitive data under
     art. 5, II (knowledge). A private school network, the other actor named, would need a basis such as specific
     consent for race: a condition, not a bar.
   - Lei 7.716/1989 art. 6 punishes refusing a student's enrolment for racial motive (knowledge); ranking for a free
     offer by expected score is not that, and the model's race effect raises the priority of the groups the quota
     law protects.
   Cost of removal (builder's probe): race +0.18 to +0.20 RMSE, race and sex +0.25 to
   +0.29, all three +0.70 to +0.91 on RMSEs of 70-76.
   Mildest remedy: keep all three with the existing note, and add the fact that sets the case apart from rais (no
   statute bars the factor for educational support; the stance's trigger is absent). Consistent with
   chile_school_dropout_mineduc_1m (sex kept, "the use case offers support"). If the curator weighs the ethics
   otherwise, drop race first (smallest cost per ground).

2. CLEAN-21 / EV-2 (P7, Should): `secondary_school_type` in 2018 is another variable, and its code 3 is decoded wrongly.
   The 2018 dictionary says 3 = Exterior, 4 = Privada; the data says 2018's TP_ESCOLA is the administration of the
   school INEP identified, not the registrant's answer. Crosstab of the 2018 sample (raw codes), TP_ESCOLA against
   TP_DEPENDENCIA_ADM_ESC: code 2 = state school 210,107 of 210,137; code 3 = municipal school 2,384 of 2,390; code 4
   = private 59,587 of 59,587; code 1 = federal school 10,437, or no identified school. The marginal shares match to
   four decimals (TP_ESCOLA 2/3/4 = 0.2158/0.0025/0.0611, the administration state/municipal/private =
   0.2158/0.0025/0.0611). From 2019 it is the answer: 225,307 shipped 2019-2023 status-2 rows
   with no identified school answer public or private, and the answer disagrees with the census school on some rows.
   Consequences in the shipped frame (2018 rows, all on the training side):
   - "abroad" holds 949 rows of 2018 municipal-school students (947 municipal, 2 private; mean score 518 against
     private 607). The level never occurs in 2019-2023 (the 2021-2023 dictionaries list no code 4, the 2019-2020 data
     hold none).
   - Federal-school students (4,108 rows, mean 602) are missing in 2018 and "public" from 2019 (11,527 of 11,583
     2019 federal-school students answered public).
   - 13,497 status-2 rows with no identified school are missing in 2018 only.
   Remedy (cheap, safe): in 2018, codes 2 and 3 to public, 4 to private, code 1 with TP_DEPENDENCIA_ADM_ESC 1 to public;
   drop the "abroad" label; one note bullet saying 2018's school type comes from the school match (13,497 rows stay
   missing). Alternative: the 2018 self-report Q027 (A only public, D/E only private, B/C mixed to missing), which is
   the same variable as 2019+ but adds a read. Fix the docstring of SCHOOL_TYPE_2018, the CLEAN-21 bullet and
   claim 22.

3. CLEAN-21 (P7, Should): `secondary_school_modality` is recorded differently by edition.
   Shipped frame, modality by edition and status:
   - "already completed": filled in 2018 (111,093 of 205,945 rows) and 2019 (95,262 of 191,660); never filled from
     2020, so never in any test window. In 2018-2019 their missing rows score higher (549.6 and 535.1 against regular
     516.3 and 509.8), a pattern the test editions cannot show.
   - EJA (youth and adult education) exists in 2018 only (16,942 rows, means 471-483). From 2019 the status-2 rows
     without a modality (2.0% to 5.4%, means 454 to 467) look like the EJA students; 2018 has 9 such rows.
   The definition's note ("the modality (TP_ENSINO) of those who have finished or are finishing") holds for 2018-2019
   only.
   Remedy: modality missing outside status 2 in every edition, and 2018's EJA missing, so one recording holds
   throughout (regular / special education, missing = not finishing this year or no modality given); correct the
   note.
   Measured, issues 2 and 3 fixed together (untuned LightGBM, 300k training rows, 3 windows x 2 seeds): RMSE change
   -0.041/-0.060 (2021), -0.022/-0.006 (2022), +0.009/-0.026 (2023); better in 5 of 6, mean -0.024. Small, as a P7
   fix should be; the fix serves correctness, not the score.

4. LEAK-10 clause 2 (P4, Must, weak; question for the curator): `school_operating_status`, census year undocumented.
   The dictionaries describe it only as "Situação de funcionamento (Escola)"; neither Leia-me 2018 nor 2023 mentions
   the school census (grepped "censo": no hit). One internal sign of a later reading: "closed in an earlier year" for
   a school the registrant is finishing that same year (0.03% to 0.12% of rows per edition) only makes sense if the
   status was read in a census after the enrolment. Against a re-pull at republication: 2018-2019 (republished
   2022-05-23) show fewer non-active schools (0.10%, 0.06% of rows) than 2023 (0.25%), where a later pull would show
   more.
   Signal: 0.17% of shipped rows have a non-active school. Its in-sample gain on top of administration, location and
   state is a group-mean R^2 of 0.00016. The non-active groups do not lean one way (closed schools score above active
   ones among federal and private schools and below them among state and municipal ones).
   The rule: values that cannot be located row by row go when they may carry a gain; keep-with-note needs a traced
   part showing none, and nothing can be traced here.
   Remedy: drop the column (it costs nothing measurable and removes the only input of undocumented timing). The
   builder's keep with a "Potential leak, kept on purpose" note is the alternative; the curator's call.

5. USE-8 (P3, a fit question for the use-case reviewers; not a column defect): who sees these inputs.
   Every input exists at the close of registration. But the registration form and questionnaire are held by INEP: a
   state department or school network does not receive them at that point. Edital 30/2023 items 14.8-14.9 release
   the participants' data and results, questionnaire included, to MEC programmes and higher-education selection, not
   to state departments or schools. The actor would collect the same answers itself. This belongs in fit_reason if the panel agrees; it changes no column.

Not problems, recorded for the other auditors:
- INEP removed from the 2023 microdata the participants of 20 small adapted or reapplied test versions (Leia-me 2023,
  section 3), a selection by an exam-day fact that the rows inherit. It is tiny and the same on both sides of the split,
  but it is not yet in the notes.
- `edition` is a feature with a value unseen in each test window; this is standard for a temporal task and not a leak.

Dtype probe (re-run on the current definition, 52 s, 3.7 GB): 19 of 43 flagged, all answered.
- 17 `open_end`: the ordered counts with "4 or more", the age bands, income, domestic worker, years since secondary.
  These are intended cut ends, ordered categories in the dictionary's order (CLEAN-14); no order is reversed (every
  scale runs A..G/A..Q/1..20 lowest first, as the words say).
- 2 `numeric_levels`: the IBGE municipality codes, categories by meaning, string-typed. The state digits ship as
  school_state and exam_state.
- No count or measured quantity is typed categorical (household_size is a number), and no code is typed numeric.

Sources (web): Edital Inep 30/2023 (in the 2023 zip; https://www.in.gov.br/web/dou/-/edital-n-30-de-5-de-maio-de-2023-481632388);
INEP on the 2023 exam municipalities, reported at
https://www.maisgoias.com.br/brasil/enem-2023-mesmo-com-inumeras-reclamacoes-inep-diz-que-e-impossivel-mudar-local-de-prova/
and https://www.correiobraziliense.com.br/enem-2023/2023/10/5138985-enem-estudantes-alocados-ha-mais-de-30-km-de-casa-poderao-fazer-prova-em-dezembro.html;
LGPD art. 11 summaries at https://confidata.com.br/blog/dados-sensiveis-lgpd-bases-legais-cuidados and
https://legale.com.br/?p=2083638; Lei 12.288/2010 at https://www2.senado.leg.br/bdsf/bitstream/handle/id/496308/000898128.pdf?sequence=1.

</details>

<details><summary>Split audit</summary>

SPLIT AUDITOR REPORT: enem_entrance_exam_scores (folder enem_entrance_exam_scores_1m), 2026-11-09

VERDICT: right with notes. The temporal split by edition (test 2023, 2022, 2021 in turn; expanding train from 2018;
no gap; 1M train / 500k test) mirrors the use case. No Must is broken. Two Should-level wording fixes to the
splits_comment, no re-split.

Judgment record
  Validity: SPLIT-1/2/3 hold (temporal: an actor ranks the registrants of the coming edition with a model fit on past
  editions; a person cannot be linked across editions, so no grouped regime is possible or needed). SPLIT-9 holds
  (no training row selected by its outcome). SPLIT-10 holds with no gap (scores out about 3 months after the exam,
  before the next registration closes), with one caveat on when the public microdata appear (note 2). SPLIT-11, -12
  and -14 hold. SPLIT-13 / LEAK-34: repeat takers on both sides, as in deployment, cannot be exploited (note 3).
  SPLIT-20: the 2018 start is right, but the stated reason is the wrong one (note 1).
  Value: the drift across editions is real and the task carries it. It costs 0.3 to 1.1 RMSE against a known-edition
  reference, nearly all of it a level bias (note 4).
  For the curator: issue 4 of the builder (history start). Recommend keeping it as it is, with the reason restated.

How I worked
  The builder's cached frame and splits, plus my own frame built with the
  definition's _clean on all 4,361,378 sampled participants, keeping the five component scores
  (in the run's panel folder). I ran untuned LightGBM (400 rounds, 255 leaves, 4 threads) on 1M train /
  500k test per window, drawn like the shipped protocol. My shipped-split replication scores RMSE 75.19 / 69.69 / 69.55
  (2023 / 2022 / 2021), mean 71.48, against the task probe's 71.5. Scripts and results are in the run's panel folder.

CHECKS WITH NUMBERS

Regime (SPLIT-1, SPLIT-3, USE-10)
  The use case is a department or school network that ranks its registrants at registration close to target free
  preparation. That is a stream of yearly cohorts, each predicted by a model fit on earlier editions: temporal.
  Most registrants are new people. A repeat taker is a known person, but the files cannot link them (dictionary
  note 1: NU_INSCRICAO does not identify a person across years), so a grouped split is impossible and the person's
  history cannot be a feature. The declared regime matches. The known-person part is a fit note (fit approximate,
  already stated), not a split problem.

Time column, windows, sizes (SPLIT-11, SPLIT-12, SPLIT-14, SPLIT-15)
  `edition` = NU_ANO, the edition label. The 2020 edition was held in Jan-Feb 2021, but its results (about
  29-30 March 2021) still came before the 2021 registration (mid-2021), so the order holds.
  Windows: one edition each, with an expanding train side and a yearly refit (horizon 1 year), which matches
  SPLIT-11 and SPLIT-12.
  Train share of all 17,445,513 participants:
    2021 window: 10,184,319 = 58.4%
    2022 window: 12,422,426 = 71.2%
    2023 window: 14,767,249 = 84.6%
  Starting in 2019 would leave the 2021 window 46.4% (claim 34 checked). Every window is above the floor.
  Each window has its own train side, drawn from one random order.
  Shipped train sides by edition (from splits.pkl):
    2023 window: 2018 264k, 2019 251k, 2020 175k, 2021 152k, 2022 158k
    2021 window: 2018 382k, 2019 364k, 2020 254k
  Test: 500k per window, of 559,527 to 669,566 sampled participants.
  Season shape: each window is one whole yearly sitting, so no part-season window. 2021 is the first edition after
  COVID, with a changed cohort. Compared with 2018-2020:
    18 or younger: 57% (47-49% before)
    private school: 8.0% (5.6-6.3%)
    already finished secondary school: 45% (53-55%)
  The change persists in 2022 (60%, 8.4%, 41%) and 2023 (59%, 8.3%, 41%), so 2021 opens a new regime rather than
  being a one-off season. No widening needed (SPLIT-20, second half).

Gap and late labels (SPLIT-9, SPLIT-10)
  Scores are final at release, and every training edition's scores were published before the test edition's
  registration closed: 2020 results at the end of March 2021 (practice takers in May), 2022 results on 9 Feb 2023.
  So no training label was unknown at the prediction point. There is no selection by the outcome, since each
  edition ships whole and every row has a final score. Probe 13 shows a rise, not a fall at the release end:
  drift, not censoring, so LEAK-24 is not triggered (I agree with the builder). No gap is right for the labels
  (note 2 has the data-access caveat).

Training history (SPLIT-20, builder's issue 4)
  Means by edition (sampled participants present on both days; the 2017 row is from the full 2017 file):
    edition  natural sci.  humanities  languages  maths  essay  mean of 5
    2017     510.9         521.5       512.2      518.8  529.4  518.5   (4,426,692 present)
    2018     493.7         570.9       528.6      535.5  516.1  529.0
    2019     477.8         509.8       522.3      523.1  579.6  522.5
    2020     490.6         514.2       526.0      520.8  581.5  526.6
    2021     492.1         523.4       504.9      535.5  622.5  535.7
    2022     496.0         530.0       519.9      542.6  629.0  543.5
    2023     496.0         526.2       520.3      534.0  626.9  540.7
  The essay is graded by correctors and has no item-response equating. Its level steps up about 64 points in 2019
  and about 43 more in 2021: +110 from 2018 to 2022, which is +22 on the mean of five. 2017 (529) belongs to the
  old essay level, as does 2018 (516).
  The four item-response scores are only roughly comparable across editions: humanities 2018 sits 41-61 above every
  other edition, languages 2021 15-23 below. These are participant means, so a change of cohort is mixed in.
  Adding 2017 is not needed for the floor and would add the largest and oldest edition, on the old essay scale.
  Keeping 2018 is forced by the floor. So start in 2018 and leave 2017 out. That is right, but for recency and the
  essay break, not for the stated reason ("it would lower the cap of the years since secondary school to 11"),
  which is a cleaning convenience.
  2020 (55% absent, a changed cohort: 36% at or below 1 minimum wage against 27-28%) stays, as a refit would have
  had it. For information only (SPLIT-21: scores never decide the history), at 1M train rows:
    without 2020: 2023 75.15 vs 75.19, 2022 69.69 vs 69.69, 2021 70.17 vs 69.55 RMSE
  2020 helps the window that follows it.
    newest edition alone (559-647k rows): 75.34 / 70.08 / 69.85
    the same size drawn from all earlier editions: 75.64 / 70.19 / 69.93
    shipped 1M from all earlier editions: 75.19 / 69.69 / 69.55
  Recency matters a little at equal size; more history matters more.

Repeat takers (SPLIT-13, LEAK-34)
  A person may sit several editions (a practice taker becomes a candidate; candidates retake). Practice takers
  ("completing after the edition's year") are 12.9-19.1% of each edition, so a sizeable share of the 2022 and 2023
  test rows likely sat an earlier edition that is on the train side.
  This is the deployment as it is: a model refit on all past editions also holds those people's earlier rows,
  unlinked. A deployed model could only use them through memorisation, and the probes show there is nothing to
  memorise:
    exact feature copies across the split: 0.0% (0.02-0.03% without the edition)
    near copies: 0.3% of test rows have one in train
    1-NN R^2: -0.24 overall, -0.48 on the closest tenth
  An age band, a status and the years since secondary school change between sittings, so a person's earlier row is
  not a copy. SPLIT-13 holds and LEAK-34 allows it. No remedy.

Score scale drift (probe 13, TP rules)
  Probe 13 flags the 2022 and 2023 medians above the earlier band (z +5.6, +4.7). Per window, LightGBM's mean
  residual (prediction minus truth):
    window  mean of 5  four tests  essay
    2023    -1.0       0.0         -5.5
    2022    -11.6      -11.5       -11.7
    2021    +1.7       +7.7        -22.0
  The 2022 jump is spread over all five tests. The 2021 jump is the essay's step, offset by the languages dip.
  The `edition` input lets a tree place a new edition at the newest training level. Without it, the 2023 bias goes
  from -1.0 to -8.8 (RMSE 75.19 to 75.72), so the input is legitimate and useful (known at registration).
  Cost of the temporal regime (same 250k test rows per window; reference = 1M random rows of editions up to the
  test one, 10% of them from the test edition, not the use case):
    window  temporal RMSE (bias)  reference RMSE (bias)
    2023    75.24 (-1.2)          74.93 (+0.2)
    2022    69.56 (-11.7)         68.43 (-0.7)
    2021    69.44 (+1.6)          68.90 (-0.3)
  R^2: 0.378 / 0.375 / 0.393 against 0.383 / 0.395 / 0.402.
  The regime costs 0.3-1.1 RMSE, nearly all the level bias. Ranking (Spearman) barely moves: 0.609 / 0.615 / 0.616
  against 0.613 / 0.62 / 0.62. The drift is real, small, and part of the task (the 450-point rule applies to each
  edition's own scores). It is no reason to change the split (P4 over P6).

PROBLEMS, ranked (all P4; none a Must violation)

1. SPLIT-20 (Should): the history start is right, but its reason in the splits_comment is not the SPLIT-20 reason.
   Evidence: the essay level is 529 (2017) and 516 (2018), then 580 (2019-2020) and 622-629 (2021-2023). 2017 adds
   the oldest, largest edition (4.43M) on the old scale and is not needed for the floor. The years-since cap is a
   cleaning detail.
   Mildest remedy: reword the splits_comment, e.g. "2017 (same questionnaire) is not read: the floor does not need
   it, and its essay scores sit on the level before the steps of 2019 and 2021 (mean 529 against 622-629 in the test
   editions)". Keep 2018-2023. Recommend the curator keep issue 4 as it is.

2. SPLIT-10 (Should): no gap is right for the labels, but the public microdata, the training data an outside actor
   would refit on, can come later than the scores. A CMRI decision of 2023 said the 2022 microdata were "in the final
   stage" and due by June 2023, about when the 2023 registration closed. The 2020 microdata were held back under the
   LGPD and are dated 2022-02-16, after the 2021 registration.
   A one-edition gap would break the floor: the 2021 window would train on 2018-2019 = 43.5%. Its measured cost on
   that window is +0.6 RMSE (70.17 against 69.55). The LGPD delay was a one-off administrative episode, and a state
   department can reach the data through INEP's protected access (Sedap).
   Mildest remedy: none to the split. Optionally, one clause in the splits_comment: "a refit from the public
   microdata gets edition t - 1 around the close of registration (later for 2020 under the LGPD); no gap".

3. SPLIT-13 / LEAK-34 (Should, a question): repeat takers on both sides, unlinkable. Holds, as in deployment
   (evidence above). Remedy: none; the existing Note in curation_comments is accurate.

4. Drift across editions (probe 13; reading under evidence.md drift_baseline, reading 2): real, carried by the task,
   costs 0.3-1.1 RMSE (mostly the bias of 2022's level).
   Mildest remedy: none to the split. Optionally add the essay's level steps (516, 580, 622-629) to the Anomaly or
   Note bullets, since the claim that INEP's scales are comparable across editions holds only roughly for the four
   item-response tests and not at all for the essay. This also bears on the builder's issue 3 (mean of four as an
   alternative target): with the essay out, the 2021 window's bias would be +7.7 instead of +1.7, so dropping it
   does not remove the drift.

Not checked: the 2017 edition's codes in detail (only its scores and status counts read); an exact registration
calendar for 2021 (from knowledge and a press search: results of 2020 at the end of March 2021, registration in
mid-2021); a tuned model.

Sources: Blog do Vestibular / Preparaenem / Infoescola on the Enem 2020 results (end of March 2021); Poder360 and
Diário do Nordeste on the Enem 2022 results (9 Feb 2023); CMRI decision 149/2023 (2022 microdata due by June 2023);
Correio Braziliense and Conjur on the LGPD suspension of the 2020 microdata (2022).

</details>

<details><summary>Domain practitioner</summary>

DOMAIN PRACTITIONER: enem_entrance_exam_scores (folder enem_entrance_exam_scores_1m), 2026-11-09

Actor played: a state education department (Seduc), or an NGO running a free "cursinho popular", in Brazil. Close to
the exam, I offer free preparation to registrants who are likely to stay below 450, the mean that ProUni scholarships
and FIES loans require.

VERDICT
- Fit: APPROXIMATE (I agree with the definition). The target is the quantity behind my decision, and the inputs are the
  kind of items I could collect myself. But the rows are only the people who attended (absence depends on income, and
  absentees are exactly the people I most want to reach), and the inputs leave out the school records a department
  always holds (USE-8).
- Metric: PARTLY. RMSE on the five-score mean picked the same top model as ROC AUC for "below 450" in all three
  windows. The models below it swap places by 0.001 to 0.003 AUC. The fallback is right under MET-6/MET-7/MET-8/MET-11:
  450 is an eligibility rule on the target, not a cost, a treatment threshold or a k that the source fixes for scoring
  a prediction. If the definition becomes a binary version, I would use roc_auc.
- Draft issues: 1 keep race, sex and income (option a); 2 keep present-only, and name the income gradient of absence in
  fit_reason; 3 keep the mean of the five scores; 4 no view from my side (the history is a benchmark choice).

MEASUREMENTS (scripts and logs in the run's panel folder)
A. Who the present-only rows leave out (ENEM 2023, all 3,933,955 registrants):
   Present at all four tests, by family income: up to 1 minimum wage (MW) 61.8%, 1-2 MW 65.3%, 2-4 MW 74.1%,
   above 4 MW 81.7%. By race: white 73.2%, black 62.2%, brown 65.5%, indigenous 58.1%.
   By school status: already finished 58.4%, finishing this year 75.0%, practice-only (treineiro) 82.5%.
   Public-school students finishing this year (my students): 71.1% present.
B. The actor population in the rows (builder's raw sample):
   Public-school students finishing that year are 22-32% of each edition (31.0% of the 2023 test window). Already
   finished: 41-55%. Treineiros: 13-19%.
   Below 450: 13-21% of all rows; 18-25% of the public-school students finishing that year.
   Above 450 but with an essay of 0 (ineligible despite the mean): 0.07-0.18%. The five-score mean with zeros
   therefore settles ProUni/FIES eligibility almost exactly.
C. Does RMSE pick my model? (untuned models, 300k training rows, shipped splits, 2023/2022/2021)
   RMSE:          LightGBM-63 75.95/70.38/70.22, LightGBM-7 76.64/70.67/70.81, LightGBM-L1 76.29/70.82/70.72,
                  ridge on one-hot 77.02/70.86/71.20.
   AUC below 450 (higher is better; the negated prediction ranks registrants):
                  LightGBM-63 0.775/0.779/0.782 (best each window), LightGBM-7 0.770/0.776/0.779,
                  LightGBM-L1 0.773/0.778/0.780, ridge 0.771/0.775/0.780.
   A LightGBM classifier trained on "below 450" directly: AUC 0.759/0.766/0.768, BELOW the regression's ranking.
   The score carries more information than the bar, so a number is the better target even for a decision at the bar.
   Among my students (public school, finishing): AUC 0.71-0.74. Precision in the top 20% of my students:
   regression 0.45/0.39/0.47, classifier 0.42/0.38/0.45, against base rates of 0.22/0.18/0.23.

1. INPUTS AT THE MOMENT OF THE PREDICTION
- I do not receive INEP's registration form or questionnaire for my students before the exam. Ceará's Seduc estimated
  its registration rate from the school census and INEP aggregates, without a list. Schools in MG and PR pre-register
  their students and then INEP holds the answers. So I would ask the same items on my own intake form. The items are
  generic (parents' schooling and work, income band, goods at home, race, sex, school type), and a model trained here
  would carry over, so this is workable.
- Missing, though I would always hold them as a department: the student's grades in years 1-2 of secondary school,
  attendance, and the state's or SAEB's own assessment results (SPAECE, SARESP, SAEPE and so on). These predict
  achievement far better than family background. With them I would not use an SES-only model (here R^2 about 0.38).
  An NGO cursinho with only an intake form would use it. So the more natural actor is the NGO or cursinho, or a
  department at the stage before it links grades.
- Missing for repeat takers (41% of the rows have already finished school): their earlier ENEM score. The student
  brings it (the result bulletin), and for a known person it is a legitimate input (USE-10, LEAK-34). The files
  cannot link editions. This gap is named in fit_reason.
- Inputs I would not have: none found. Everything recorded on the exam days is out. The exam municipality and the
  foreign language are chosen at registration. The school items exist only for students finishing that year, which is
  also how I would hold them. school_operating_status is a kept potential leak with no use to me: I know whether my
  own school is open.

2. THE TARGET
- The mean of the five scores, with a 0 for a blank test or an annulled essay, is the ProUni/FIES quantity (450,
  essay > 0). Measurement B shows the essay-zero condition changes the call for only 0.1-0.2% of rows. Keep it
  (issue 3). A single area (mathematics) would serve a remedial maths class, not the 450 bar. The mean of the four
  objective tests would drop the essay, which is the part a prep course most often moves and the one whose zero
  disqualifies.
- What I act on is the chance of falling below 450. A regression serves that: measurement C shows the score ranks the
  below-450 call better than a classifier trained on the bar itself. So a number is the right deliverable (USE-5).
- Two inherent gaps, not fixable here:
  (a) FIES uses the best mean of any edition since 2010, and ProUni accepts either of the last two editions. For a
      repeat taker, this edition's score is not their eligibility.
  (b) What I really want is the uplift: who gets over 450 because of my class. A student predicted at 350 may not get
      there in a few months, while one at 440 may. The predicted score is the usual stand-in for uplift.

3. ROWS AND TEST DATA
- One row is one registrant of one edition, and my decision is per registrant per year. That matches.
- The test windows (whole later editions) are what I face: next year's registrants, with a model refit once a year.
  That matches (SPLIT, temporal).
- Presence (issue 2): I decide before anyone knows who will attend. Absence is graded by income and race
  (measurement A). The rows therefore under-represent the poorest registrants, the ones my offer is for. For my
  decision, an absentee is a missed 450.
- The builder's note that "no alternative target exists for absentees" holds for a score. It does not hold for the
  decision: the 2018-2023 files hold every registrant with the questionnaire, so a binary "reaches the ProUni/FIES
  bar at this edition" (present at all four tests, mean at least 450, essay above 0) is buildable over all
  registrants.
- Even so, I recommend keeping this dataset as is. Attendance and learning are different levers (attendance:
  reminders, transport, exam-day support; learning: classes). The score given attendance is the quantity a class
  changes, and as measurement C shows, the regression is the richer benchmark.
- fit_reason should say that the people left out are disproportionately the poor (38% absent at up to 1 MW, against
  18% above 4 MW in 2023), not only "a third stay away".
- A sibling version on all registrants with that binary target (roc_auc, MET-8) would be the direct fit for an
  actor whose one decision is "who will not be eligible". It is optional, a curator's call.
- Population: my students are under a third of the test rows. Treineiros (19% of the 2023 window) cannot use the
  result for ProUni/FIES this year (the FIES rules exclude treineiro results). An NGO cursinho would also serve the
  people who have already finished school, so they are in scope.
- Scoring all rows weights adults and treineiros heavily, a gap for a department (USE-8, a selection its setting does
  not share). The approximate fit already covers it, but fit_reason could name it in half a sentence.

4. WOULD I USE THE MODEL?
- As an NGO with an intake form: yes, as a screen, with a cut chosen to fill my places (20-40 students per cursinho
  under MEC's CPOP). Top-20% precision of 0.39-0.47 against a base rate of 0.18-0.23 roughly doubles the hit rate
  over a random pick among my students.
- As a Seduc: only after adding my own grades and assessment scores. Today most states run aulões open to every
  final-year student (Goiás "Só Vem Enem", ES Pré-Enem, PE no Aulão), so the targeting decision comes up only when
  places are scarce (ES ranked by its own selection test).
- I would trust the model if it were calibrated on the latest edition (the median rose in 2022-2023, the builder's
  probe 13) and validated within my state and my students. I would distrust it if it came from one national pooled
  fit: AUC is 0.71-0.74 within my population against 0.77-0.78 overall.

5. PROTECTED ATTRIBUTES (issue 1, SEL-1)
- As this actor I would use race, sex and family income. Race and income are the eligibility and priority criteria
  of the very programmes involved:
  - MEC's CPOP cursinhos must serve public-school students and prioritise Black, Indigenous and quilombola students
    and those with a per-person family income up to 1 MW.
  - The quota law (Lei 12.711/2012, as amended in 2023) and ProUni's own income bands use them.
- Legal check:
  - LGPD art. 5 II makes racial origin sensitive data.
  - Art. 11 II b lets the public administration process it without consent to carry out public policies set in law or
    regulation (from secondary legal commentaries). A private NGO needs the specific consent, which an intake form
    collects.
  - I found no bar on using these attributes for a beneficial, voluntary offer like this one.
- The risk lies in reuse: the same model used to screen applicants out (merit scholarships, private admissions,
  hiring) would be a decision against people. That is outside this use case, and a note is the right place for it.
- The cost of removal is small (+0.2 RMSE without race, +0.7-0.9 without race, sex and income), so the benchmark
  hardly depends on the choice. I support option (a), keep all.
- Sex is the weakest of the three for my purpose (no programme uses it). I would not object to dropping it alone.
- The Assam sibling's `Ethical Issue` marker covered caste and gender in a context with no stated beneficial use.
  The Brazilian context is affirmative action written into law, which is a fact that sets this case apart, not an
  inconsistency.

6. METRIC (MET-1, MET-5 to MET-9, MET-11)
- My decision ranks registrants at the 450 bar within a fixed capacity. If a source fixed a capacity I would score
  that ranking by ROC AUC for "below 450" or by precision in my top k. No source fixes a k or a cost, and 450 is an
  eligibility rule on the target, not a threshold for a prediction (MET-6, MET-7). For a regression the declared
  fallback rmse stands (MET-11 fallback; the reason text is correct).
- Measured: RMSE chose the AUC-best model in 3 of 3 windows, and its lower ranks differ by at most 0.003 AUC, so RMSE
  scores my decision well enough on these models. A model tuned to the tails could split the two more. It is
  "partly" because RMSE weighs an error at 700 as much as one at 450.
- For a binary sibling over all registrants: roc_auc (MET-8). MET-9 does not apply, since a base rate of 13-21% is
  no reason for AUPRC.

GAPS RANKED BY HOW MUCH THEY CHANGE THE TASK
1. Present-only rows, with absence graded by income and race (USE-8; a selection my setting does not share). It
   changes who is scored. Name the gradient in fit_reason; an optional sibling version could carry a binary target
   over all registrants.
2. No school records: grades, attendance, state assessments (inputs a department always has). This caps the skill
   and moves the natural actor to an NGO with an intake form. It is an inherent gap of the source; name it in the
   use case or fit_reason.
3. Population mix: my students are under a third of the test rows, and 19% are treineiros who cannot use the score.
   Approximate fit; half a sentence in fit_reason.
4. Repeat takers cannot be linked, so a known person's earlier score is missing (USE-10). Already named.
5. The target is one edition's score, not eligibility over the best edition, and not uplift. Inherent, minor.

WHAT A DOMAIN EXPERT WOULD CHANGE
- Write the actor as "an NGO or public cursinho programme (MEC's CPOP) or a Seduc selecting students for limited
  places", and say that the inputs are items its own intake form can ask. That is how the model would be used,
  since INEP does not hand over the questionnaire.
- In fit_reason: "absentees are disproportionately low-income (38% at up to 1 MW against 18% above 4 MW, 2023)"; and
  "treineiros, who cannot use the score for ProUni/FIES, are about a sixth of the rows".
- Optionally a second version: all registrants, target "at or above the ProUni/FIES bar at this edition" (present,
  mean of at least 450, essay above 0), roc_auc. It is not needed for this one to ship.
- Keep the target, the inputs (race, sex and income included) and the metric as they are.

SOURCES
- dataset.py and README.md of enem_entrance_exam_scores_1m; the record; builder_report.md; claims.md;
  probes/the builder's probe; builder's frame and raw sample. Rules: use_case.md (USE-1, USE-3, USE-5, USE-8,
  USE-10), metrics.md (MET-1, MET-6 to MET-9, MET-11).
- ProUni/FIES 450 rule and essay > 0; FIES uses the best edition and excludes treineiros:
  https://www.gov.br/mec/pt-br/fies/arquivos/2021/edital_38_23062021.pdf ;
  https://static.preparaenem.com/2025/07/edital-prouni-2025-2.pdf ;
  https://www.vestibulandoweb.com.br/prouni/quem-pode-participar-do-prouni-veja-regras-renda-e-nota-minima-do-enem/
- Absence 28.1% (day 1) and 32% (day 2) in 2023, about a third historically:
  https://www.cnnbrasil.com.br/nacional/abstencao-enem-2023/ ;
  https://www.jornalopcao.com.br/educacao/um-em-cada-tres-alunos-inscritos-nao-compareceu-ao-segundo-dia-do-enem-551301/
- State prep programmes (open aulões; ES selection by ranking):
  https://goias.gov.br/goias-lanca-projeto-so-vem-enem-com-auloes-gratuitos/ ;
  https://www.es.gov.br/Noticia/sedu-promove-auloes-preparatorios-para-o-enem ;
  https://www.diariodepernambuco.com.br/amp/vida-urbana/2025/09/11695323-pe-no-aulao-estado-inicia-projeto-de-preparacao-para-estudantes-do-3-ano-do-ensino-medio.html ;
  https://www.es.gov.br/Media/PortalES/PDF/EDITAL%2015-2018%20-%20ALUNO%20%20PRE-ENEM%20DIGITAL%202017%20vers%C3%A3o%20final%20-%2005.03.2018.pdf
- Seducs do not hold registrant lists or answers; schools pre-register their students:
  https://www.opovo.com.br/noticias/enem/2024/11/01/enem-2024-99-dos-estudantes-da-rede-publica-do-ceara-se-inscreveram-no-exame.html ;
  https://www.parana.pr.gov.br/aen/Noticia/Alunos-da-rede-estadual-de-ensino-terao-inscricao-automatica-no-Enem
- MEC CPOP (cursinhos populares; priority by race and income; 20-40 students each):
  https://agenciagov.ebc.com.br/noticias/202601/cpop-cursinhos-populares-ja-podem-se-inscrever-para-edicao-de-2026 ;
  https://www.gov.br/mec/pt-br/cpop/documentos/edital-cpop-2026.pdf
- LGPD art. 5 II and art. 11 II b (secondary commentaries): https://www.aurum.com.br/blog/lgpd-comentada/art-11-a-13-lgpd/ ;
  https://confidata.com.br/blog/dados-sensiveis-lgpd-bases-legais-cuidados
- Not verified: the exact amended income cut of the quota law (Lei 14.723/2023, from memory); whether any state
  receives INEP's questionnaire answers under an agreement (none found).

</details>

<details><summary>Blind review</summary>

BLIND REVIEW: enem_entrance_exam_scores  (the reviewer saw only the clean room and the public web)

VERDICT: Include with changes. It is real public INEP microdata with an honest temporal split and moderate signal, but the use case is thin, the subsampling is undocumented, and two encodings need fixing.

WHAT THE TASK IS
Predict a candidate's ENEM score, taken as the unweighted mean of the five scores (4 objective areas + essay), from the registration record: demographics, school, exam site, and the 25-item socioeconomic questionnaire. ENEM editions 2018-2023. Target is mean_score (0-843.96, mean 534.6, sd 89.1). Every feature is collected at registration, months before the exam, so the prediction could be made at that point. Data: 200k-row sample of 2.5M, 43 features (42 categorical, 1 float). The split is temporal on edition with 3 test windows (I assume 2021, 2022, 2023 with expanding training data).
Who would use it: education researchers and policy analysts (inequality studies, targeting prep or tutoring programmes by socioeconomic profile). Nobody makes an operational decision about an individual from this prediction. In practice it is an inequality-explanation regression that people have long used on Kaggle and in teaching. It is a legitimate real-data benchmark, but a weak deployment story.

CHECKS I RAN (scripts in the run's panel folder)
- LightGBM (600 trees, defaults otherwise), expanding temporal split:
  test 2021 R2 0.370 / MAE 55.8 (constant baseline MAE 71.8); 2022 R2 0.355 / 55.7 (70.5); 2023 R2 0.371 / 59.2 (76.0).
  Random 80/20 split: R2 0.391. So the temporal gap is small and the split is not hiding leakage.
  With only 5 features (income, mother education, school type, school admin, edition): R2 0.258 on 2023.
  Gain importance: family_income 0.34, exam_municipality 0.16, computers 0.08, years_since_secondary 0.06.
- Target arithmetic: mean_score*5 is a multiple of 0.1 in all 200k rows. That fits a sum of four 1-decimal IRT scores plus an integer essay score, i.e. the claimed mean of 5.
- Duplicates: 0 full-row duplicates. 16 duplicated feature vectors (negligible). There is no person ID, so I cannot check repeat takers across years. Repeat takers are plausible (41-55% "already completed"), but with a temporal split and no ID this is the real-world condition, not leakage.
- Rows are sorted by edition (monotonic).

CONCERNS, MOST TO LEAST SERIOUS

1. Undocumented, non-proportional subsampling per edition (moderate).
   Shares in the sample scale to about 379k (2018), 367k (2019), 254k (2020), 500k (2021), 499k (2022), 501k (2023) in the 2.5M. Real ENEM attendance was higher in 2018-2019 than in 2021-2023, so this is not a proportional sample. 2021-2023 look capped at about 500k, and the rule for earlier years is unclear. Which population is included is also not stated: present on both days? excluding eliminated candidates? including "treineiros" (practice takers, 16% "completing after the edition's year")?
   Change: document the filter (presence, eliminated, treineiros) and the per-edition sampling rule in task.md. Prefer a uniform per-edition rate, or state the cap.

2. Weak, mostly descriptive use case; sensitive attributes as predictors (moderate).
   Race, sex and income drive the prediction. No individual-level decision is made from it. Benchmark results are fine, but the description should frame this as score prediction from registration data for programme targeting and research, not selection.
   Change: state the use case explicitly. Keep it as one of few education/socioeconomic regressions, but do not overweight it.

3. High-cardinality municipality codes stored as plain categoricals (moderate, preparation).
   school_municipality has 4,196 levels and is 72.9% missing. exam_municipality has 1,749 levels. Both are IBGE codes stored as category. Under LightGBM native categorical handling they overfit: dropping both raises 2023 R2 from 0.371 to 0.382. This matters for a benchmark because it rewards methods by how they handle a 4k-level code rather than by modelling skill. exam_municipality and residence are close to redundant; exam_state duplicates the first 2 digits of the code.
   Change: keep them, since they carry real geographic signal, but declare them as high-cardinality IDs. Optionally also provide state/region. Do not drop silently.

4. Target definition choices (minor-moderate).
   The mean of five gives equal weight to the essay. The essay score is 0 for annulled or blank essays, so annulment (a behavioural event) leaks into the target as a large negative jump: 417 rows < 300, 56 rows < 200, and 3 rows exactly 0.00, which means all five scores were zero (likely eliminated or blank candidates that should have been filtered). The scale is IRT-equated across years for the objective areas, so the yearly mean drift is small (523-543), which is fine.
   Change: drop rows with mean_score == 0 and say how annulled essays are handled. Alternatively, consider the mean of the 4 objective scores as a cleaner target.

5. Structural missingness is explained but not documented (minor).
   The school_* block is missing for everyone not completing in the edition year (0 non-missing among "already completed" / "after year") and for 26% of current completers. years_since_secondary is missing 56%, and secondary_school_type is missing 64%. The 223 rows (0.11%) with no household_size are missing the whole questionnaire block. This is MNAR-by-design and acceptable as NaN, but it should be noted.

6. Small preparation points (minor).
   Ordinal answers (bathrooms "0..4 or more", income bands, age bands) are ordered pandas categoricals with correct level order. That is good, but many tools drop the ordering, so a numeric ordinal version would be friendlier. household_size is float with max 20, which is plausible. school_operating_status = "closed in an earlier year" for a current completer's school (0.1-0.4%) is odd but is source data. DVD-player ownership falls from 39% (2018) to 14% (2023), which is plausible real drift.

WHAT I COULD NOT CHECK
- The raw INEP files. I did not download the multi-GB yearly zips, so I could not verify the row filter, the exact 2.5M composition, the mapping from the original codes (Q001-Q025, TP_*) to these labels, or that age_band was harmonised correctly for 2018-2019 (those years had exact age).
- Which three editions are the test windows. I assumed 2021, 2022 and 2023.
- Repeat takers across editions (there is no stable person ID in public data).
- Context: since 2020 INEP removed identifying variables (e.g. CO_ESCOLA), and from 2024 it split the microdata into separate participant and result tables, so this feature set may not be reproducible for 2024+. That limits the "future use" story but does not affect benchmark validity.

Sources: https://www.gov.br/inep/pt-br/acesso-a-informacao/dados-abertos/microdados/enem ; https://www.gazetasp.com.br/brasil/mpf-vai-a-justica-para-que-governo-volte-a-divulgar-dados-detalhados/ ; https://gh.r-mj.com/basedosdados/pipelines/pull/1431

</details>

<details><summary>Task gamer</summary>

**TASK GAMER: enem_entrance_exam_scores (folder enem_entrance_exam_scores_1m), 2026-11-09 (mean_score, regression, RMSE, temporal on edition; tests 2021, 2022, 2023)**

Verdict: I found no exploit that beats the honest baseline by more than seed noise. The task cannot be
gamed in any way I could measure. The only flaw I found hurts an honest model, and only a little: the
shipped training sets throw away earlier history that is in the kit.

Scores are RMSE, lower is better, given per split (r0f0 = test 2023, r1f0 = test 2022, r2f0 = test 2021) and as the mean.

Honest models
- B0, untuned LightGBM (100 trees, all features()): 75.477 / 69.676 / 69.596, mean 71.583   (baseline.py)
- B1, stronger LightGBM (600 trees, lr 0.05, 255 leaves): 74.547 / 69.184 / 68.934, mean 70.888   (honest.py strong)
- Noise: B0 with bagging under 3 seeds gives r0 75.47-75.53, r1 69.67-69.71, r2 69.63-69.66, so
  about +-0.03 per split. A random-number column was never picked, so the scores did not change.
- Bias of B0 on test (truth minus prediction): +1.5 / +11.1 / -1.5. Test 2022 scored about 8 points
  above 2021 on average (543.5 vs 535.7). That shift happens on exam day. No feature carries it.
  Even if a model knew it exactly (an oracle), r1 would only improve from 69.68 to 68.78.

Exploits ranked by gain (all gains are within noise; there is no real one)
| # | Exploit | Script | Honest score | Exploited score | Gain per split | A deployed model has it? | Fix |
|---|---|---|---|---|---|---|---|
| 1 | Counts of exam and school municipality over train+test rows together (test-row statistics) | exploits.py countall | 71.583 | 71.560 | -0.008 / -0.040 / -0.021 (noise +-0.03) | Mostly yes: registration counts per city are known before the exam | none needed |
| 2 | Near copies across editions (repeat candidates rebuilt from demographics, parents and household; earlier-edition target as a feature) | exploits.py match, match_explore.py | 71.583 | 71.588 | +0.009 / +0.007 / -0.003 | Partly: INEP knows a repeater's earlier score, but the task gives no id | none needed; only 0.3% of test rows find a tight match |
| 3 | Make-up of the test year's own rows per exam municipality (private-school share, income, finishing-this-year share, computer share, share of rows) | exploits.py teststats | 71.583 | 71.602 | -0.012 / +0.022 / +0.048 | Close to yes: computed on present candidates only, which is a slight post-exam selection | none needed |

Flaw that hurts an honest model
| What is wrong | Honest choice | Shipped-train score | Honest-choice score | Gain | Fix |
|---|---|---|---|---|---|
| Each training set is a random 1M-row subsample of the earlier editions. For r0 it discards 1M earlier rows that are in the kit's data, and for r1 it discards 0.5M. A deployed model would train on all past rows. | Train on every row with edition < test edition | 75.477 / 69.676 / 69.596 | 75.248 / 69.546 / 69.596 | -0.23 / -0.13 / 0 (r2 already uses all 1M rows) | Ship all earlier rows as training data, or say that the 1M cap is deliberate. Small effect. |

Findings
1. Test-row counts (countall). Counting municipality values over train and test rows together changes RMSE by
   -0.008 to -0.040 per split, the same size as seed noise (about 0.03). City sizes are known at registration
   from the registration counts, so this would not be a leak even if it helped.
2. Repeat candidates. ENEM candidates often retake the exam, but each edition here is a sample of about
   1 in 7 present candidates, and the household answers change between years.
   - With a tight key (demographics, parents, exam city and all 21 household items): only 0.14-0.28% of test
     rows match a row in the previous edition. The matched scores correlate 0.54-0.64 with the test score.
   - With a looser key: 4% of rows match, but the matches are mostly different people.
   - As features (mean and count of the earlier-edition targets over train rows), they give no gain.
3. Test-year composition. Statistics per exam municipality, computed on the test edition's own rows, add
   nothing (+0.02 to +0.05, i.e. slightly worse).
4. Training rows. The split is clean: every training row comes from an earlier edition than its test rows, row
   positions are sorted by edition, and test rows are always the last block.
5. Shipped subsample (the flaw above). Training on all earlier rows in the kit helps r0 by 0.23 and r1 by 0.13.
   Strictly, a participant who reads rows outside the shipped training set breaks the protocol, so this is a
   flaw for the benchmark designer, not something a participant can exploit.

Attacks that found nothing (default LightGBM; noise about +-0.03 per split)
- Row order: inside each edition the rows are shuffled. Correlation of row position with the target is
  |r| < 0.003. Lag-1 correlation of the target is |r| < 0.002. Target means by position decile stay within
  about 1 point. The edition blocks are in order, and the edition column already says the same.
- Target format: every mean_score is a multiple of 0.02 (the mean of five scores with one decimal each), in
  every edition. No feature carries any format. household_size is always a whole number.
- Missing values: a model on missing-value indicators alone (plus edition) scores 93.3 / 86.5 / 87.8, far
  worse than the baseline, close to the target's SD of about 89. School fields are missing for people not
  finishing school that year, which is how the questionnaire works.
  - 2020 has 1% of rows with the whole household questionnaire missing (2648 rows). Their target mean is
    525.8, against 526.5 for the rest of 2020. No signal.
- Category levels by year: 'abroad' (school type) and 'EJA' (school modality) occur only in 2018. This is a
  coding change in the source, it does not identify the label, and it does not touch the test years.
- Columns from after the prediction point: I fit each feature alone on r0. The best single features score
  85.4 (family_income), 87.6 (computers) and 88.5 (father_occupation), against 75.5 for the full model, so
  none comes close. All columns are registration or questionnaire fields, or school-census fields. The scores
  by school_operating_status (closed or suspended about 560-584, against 538 for active) come from small
  private schools, not from the outcome.
- Train vs test classifier (latest training edition vs test, edition dropped): AUC 0.55 / 0.55 / 0.60. Most
  of the gain is exam_municipality (the mix of exam cities shifts between years). Nothing gives the label away.
- Other honest training-set choices (B0 settings), none better than noise:
  - drop 2020 (the COVID edition): 71.814
  - last 2 editions only: 71.698
  - last edition only: 72.019
  - recency weights 3/1.5/1: 71.559 (-0.07 / +0.05 / -0.05)
  - drop the edition column: 71.724
- Web search: I found no Kaggle competition, leak thread or "magic feature" for ENEM mean-score prediction.
  Published work (RENOTE/UFRGS, SBC, SciTePress) predicts scores from the questionnaire with similar
  features and reports errors of the same size (MAE about 66).
- Looking rows up in the published INEP microdata: within an edition, only 0.14% of rows share their full
  feature vector, so a lookup would work. Any public dataset allows this, so I do not rank it.

What I could not check
- What the preparation changed relative to the INEP source. I did not download the microdata (several GB per
  year). From the kit:
  - 2018-2020 together hold exactly 1,000,000 rows, split by turnout (2020 is smallest). 2021-2023 hold
    500,000 rows each.
  - Only candidates with a score (present at the exam) are kept. At the stated prediction point
    (registration), turnout is not known yet. Train and test share this selection, so it is a question
    about what the task means, not an exploit. To decide it: is the deployed population "registrants" or
    "candidates who will show up"?
- B1 (stronger model) was not rerun with each exploit; the exploits gave nothing on B0, so I did not expect a
  change.

Sources: https://seer.ufrgs.br/index.php/renote/article/view/153553 ; https://sol.sbc.org.br/index.php/ctic/article/download/3244/3206 ;
https://www.scitepress.org/Papers/2021/104080/104080.pdf ; https://www.gov.br/inep/pt-br/acesso-a-informacao/dados-abertos/microdados/enem

</details>

<details><summary>Precedent check</summary>

**PRECEDENT CHECKER: enem_entrance_exam_scores (folder enem_entrance_exam_scores_1m), 2026-11-09**

Read: principles.md (Tensions, Exceptions and amendments, Consistent judgement); selection.md SEL-1 and "Selection
bias"; use_case.md; leak_checks.md LEAK-22 to LEAK-25; splits.md SPLIT-14, SPLIT-20; metrics.md MET-4 to MET-11;
cleaning_features.md CLEAN-12; evidence.md EV-4; provenance.md PROV-9; the definition, builder_report.md, claims.md;
the decision register (no flag names this dataset); the panel reports present now (blind_reviewer, claim_auditor,
column_auditor); the batch's rais, chile, wioa, acs, sinan, kumc panels and definitions; the records of the Assam
sibling, adult, law_school_admission_bianry, tunisian_fraud_detection_challenge, kumc_inpatient_aki_prediction and
the education records.

**Summary**
  D1  race, sex, family income as inputs (SEL-1; Tensions row) ... consistent with the current row and with the
      proposed rais extension (no law found that bars these grounds for this use; Brazil's own admission law uses
      race and income). Open pair: the Assam sibling's legacy `Ethical Issue` for caste and gender, a precedent that
      itself contradicts SEL-1. Prompt 1.
  D2  use case not stated by the source (USE-1, USE-9) ................. consistent (ecls_k2011, hsls09, early_learning,
      student_portuguese, rais, ny_wcb, wioa). Wording: no "for example" (USE-1 Methods). USE-9 not written down.
  D3  cohort present on both days (USE-8; LEAK-22) .................... the filter and the approximate fit are
      consistent (diabetes_130_us; USE-8 selection rule). DEPARTS WITHOUT A REASON on the marker: no
      `Selection Bias` on the record, where tunisian, lt_vehicle_loan, kumc and sinan carry it for the same shape.
      Prompt 2.
  D4  target: five-score mean with essay zeros (USE-5, TP-7) ........... consistent with USE-5 and framingham (zeros
      kept). TP-7's "test each candidate" not done for draft issue 3. The claim auditor's option (b) (drop blank
      day-2 rows) would depart from framingham (LEAK-22) unless a recording fact is shown.
  D5  history from 2018 for the floor (SPLIT-20, SPLIT-14) ............. consistent (chile 2018 start and COVID years,
      perth/aeolus chosen from counts, SPLIT-21 respected). Missing: the 2020 coding breaks in splits_comment, as
      chile's panel required.
  D6  fallback rmse (MET-5, MET-6, MET-11) ............................. consistent (gallstone_disease,
      ljubljana_breast_cancer; MET-7 "never invent a threshold").
  D7  municipality IBGE codes as categories, names not read (CLEAN-12) . DEPARTS WITHOUT A REASON: written as
      following CLEAN-12; the same choice is open as rais issue 5 (with sinan and chile); this would be the 4th
      case of one reason. Prompt 3.
  D8  accept task_time_on_few_unique ................................... consistent (wisconsin 2026-11-08,
      spanish_homeowners 2026-11-02, tunisian, chile proposed). Wording: say why there is no finer time.
  D9  CC BY-ND 3.0 (EV-4) .............................................. consistent as the builder handles it (a note,
      no issue). The claim auditor's finding 8 ("a question for the curator") departs from EV-4 and from
      wisconsin (2026-11-06, issue withdrawn): keep it a release-checklist item.
  D10 year 2026 (PROV-9) ............................................... consistent with the snapshot clause
      (chicago_traffic_crashes, fpa_fod_wildfire_cause_1m); the stated analogy to chile and rais is not exact.
      Note, no prompt.
  Drift: none on any of these rules. Third-exception count: CLEAN-12 codes-kept would reach 4 in this batch (D7).

**D1. Race, sex and family income as inputs (P1, SEL-1 Must; Tensions row "a factor the actor may no longer use")**
Status: consistent with the Tensions row as it stands and as the rais panel proposes to extend it. One open pair
of similar cases decided differently (the Assam sibling), and that precedent is itself inconsistent with SEL-1.

Precedents
  * Tensions row (amended 2026-11-08, Lennart): sex leaves every insurance pricing task (bemtpl97 CC 2026-11-05;
    australian_vehicle_insurance_2004_2005, pricing_game_2017_french_mtpl, frempl, spanish_homeowners, all
    2026-11-08). Its scope is insurance pricing; credit tasks (home_credit_default_risk `CODE_GENDER`,
    credit_card_clients_default `SEX`) keep sex, "not reviewed yet". ENEM is outside the row's current scope.
  * Proposed extension (rais_employment_separation panel, mediator issue 1, 2026-11-09, AI, not decided): the row
    covers any decision where the actor's own law bars the factor. RAIS drops sex, race, age, nationality and
    disability because Lei 9.029/1995 art. 1 bars them in decisions on "acesso ... ou manutenção" of a job.
  * Education siblings that keep sex or gender, all shipped: chile_school_dropout_mineduc_1m ("sex stays an input;
    the use case offers support, not a decision against the student", dataset.py line 521; this batch's chile
    precedent checker found it consistent), open_university_learning_analytics_dataset (`gender`, plus deprivation
    band), student_portuguese_performance (`sex`), early_learning_predictors (`sex`).
  * Shipped tasks that keep race as an input: diabetes_130_us, 2_month_survival_rate_prediction,
    wids_diabetes_mellitus (ethnicity), kumc_inpatient_aki_prediction, sinan_dengue_case_screening_1m (Brazil,
    race or colour). None was decided on race by the curator explicitly.
  * This batch, pending, AI: wioa_employment_after_exit_1m keeps race, sex, disability (recommended: keep; a benefit
    allocated, DOL's own adjustment model uses them); acs_food_stamps_2014_2024_1m recommends dropping race, origin
    and sex because 7 CFR 272.6(a) bars a SNAP agency from them in any program service.
  * Legacy curator flags, from the workbook import (before 2026-06-23, undated):
      - student_performance_on_an_entrance_examination: "Prediction uses caste and gender",
        marker `Ethical Issue`, verdict `TBD -> Yes`. The same task as ENEM (an entrance-exam result from background).
      - adult: "Potential ethical issues from including race as a feature" (one reason of a `No` that rests on
        SEL-3/USE grounds).
      - law_school_admission_bianry: "Race as feature. Not a predictive task." (`No`; the AI's 2026-10-22 assessment
        argued "a race column is no ethical bar"; the curator has not answered).

Does a law bar these grounds for this use case? (from knowledge; not re-read in this run)
  * No bar found. The column auditor reached the same answer independently.
  * Lei 12.711/2012 (federal university quotas) uses race (pretos, pardos, indígenas) and family income per head as
    admission criteria. The STF upheld race-based quotas (ADPF 186, 2012). The Estatuto da Igualdade Racial (Lei
    12.288/2010) provides for affirmative action. Targeting free preparation by these grounds is the kind of
    measure these laws promote.
  * LGPD (Lei 13.709/2018) art. 11 treats racial origin as sensitive data; a public body may process it to carry
    out public policy (art. 11 II b). A private school network would need another basis. This bears on a real
    deployment, not on the benchmark.
  * Even under the insurance family's "as if in Europe" stance: EU law on race in education (Directive 2000/43/EC)
    allows positive action. So the result is the same under both readings.

Reading
  * Under the current row and under the rais extension, the three inputs stay. The stated reasons ("support, not a
    decision against"; the quota law) follow chile and the legal-constraint reasoning.
  * Family income: no precedent drops income anywhere (credit, acs, rais keep it). Consistent.
  * The pair with the Assam sibling is real: the same task, caste (the Indian analogue of race) and gender, flagged
    `Ethical Issue`. Neither stated reason sets ENEM apart: India also uses caste in admission (constitutional
    reservations), and a support use case could be written for Assam too.
  * The Assam precedent contradicts SEL-1: `Ethical Issue` is the marker of a Must whose verdict is `No`, yet the
    record is `TBD -> Yes`. Under principles.md ("a precedent that contradicts a rule is flagged, not followed"),
    the flag is the point to settle, not a model for ENEM.
  * Ranking: SEL-1 is P1 and outranks everything. If the curator reads protected grounds as an ethical concern by
    themselves, the remedy ladder gives "drop the features" before "exclude". The measured cost is small: +0.18 to
    +0.20 RMSE without race, +0.25 to +0.29 without race and sex (claims 44; replicated by the claim auditor).
  * Drift: none. Every 2026-11 curator call on protected grounds is framed as the actor's legal constraint (P3/P4),
    none as SEL-1. The legacy flags predate that frame.

Prompt 1 (issue shape)

   1. **Do race, sex and family income stay as inputs, and does the Assam sibling's `Ethical Issue` marker give way to the same reading?**
      - **Problem:**
        - The definition keeps race, sex and family income, and no law found bars them for a department that targets free preparation[^p1law].
        - The Assam sibling, the same task with caste and gender, carries `Ethical Issue` from the June workbook while its verdict stays `TBD -> Yes`, which SEL-1 does not allow[^p1sel1].
        - Since November every call on protected grounds asks whether the actor's law bars them (insurance pricing, rais), not whether the ground is sensitive in itself[^p1row].
      - **Consistency:** chile_school_dropout_mineduc_1m and three shipped education datasets keep sex; diabetes_130_us, kumc and sinan keep race; rais drops all grounds under an explicit employment bar; acs proposes dropping them under the SNAP rule; adult and law_school carry legacy notes on race as a feature.
      - **Effect on the task:** RMSE rises by 0.18 to 0.20 without race and by 0.25 to 0.29 without race and sex, on a level of 70 to 76.
      - **Options:**

        | | Option | What it does | Pro | Con |
        |---|---|---|---|---|
        | a (implemented) | Keep all three; record that a protected ground is no SEL-1 concern by itself, and reopen the Assam marker as a note | no change here; Assam's marker becomes a note under the same reading | one reading for both entrance-exam tasks; matches the November calls and chile | the reading is new for SEL-1 and needs its own line in selection.md |
        | b | Treat ENEM like the Assam flag: drop race and sex | two inputs leave | follows the only precedent on this task | departs from chile and the shipped medical tasks; no law asks for it |
        | c | Drop race only | one input leaves | the narrowest fix | matches no precedent; caste and gender were flagged together |
        | d | Amend the Tensions row now: grounds leave only where the actor's law bars them, in any domain | settles ENEM, rais, wioa and acs together | one rule for the batch | needs the rais decision first |

      - **Recommendation:** a, decided together with d when the rais extension is settled.
      - **Decision:** a, b, c or d?

      [^p1law]: Lei 12.711/2012 (quotas by race and income); STF ADPF 186 (2012); Lei 12.288/2010; LGPD art. 11 II b; from knowledge, not re-read. Column auditor: "no law that bars race, sex or income for this use case".
      [^p1sel1]: SEL-1 (Must): a task with ethical concerns is out, marker `Ethical Issue`. W/curation/records/student_performance_on_an_entrance_examination.md: "Prediction uses caste and gender" (workbook import, before 2026-06-23).
      [^p1row]: principles.md, Tensions, "a factor the actor may no longer use" (P3 and P4; USE-1, USE-6), amended 2026-11-08 (Lennart); rais_employment_separation panel, mediator issue 1 (proposed extension, 2026-11-09).

**D2. A use case the source does not state (P3; USE-1 Must, USE-8 Must, USE-9 Should)**
Status: consistent. Two writing points.

Precedents
  * Education tasks with our own use case and an approximate fit: early_learning_predictors (source explanatory,
    "For example, a programme funder ..."), student_portuguese_performance ("For example, a school predicts ..."),
    ecls_k2011_later_achievement, hsls09_secondary_student_achievement, colombia_saber11_saberpro_linked (records:
    "the use case is ours"). chile_school_dropout_mineduc_1m is the one with a source-stated actor (Rodriguez et al.
    2023).
  * This batch: rais ("the cohort, prediction point and target are ours"), ny_wcb ("The source names no prediction;
    the use case is ours." in use_case), wioa and acs ("For example, ...").
  * The nearest `No` with a similar shape is adult (census income, use case ours, "not a meaningful task"). What sets
    ENEM apart: the target is an outcome realised months after the prediction point, from the actor's own form
    (the registration), not a contemporaneous survey answer. The blind reviewer named "targeting prep or tutoring
    programmes by socioeconomic profile" without our notes (as on chicago_traffic_crashes, 2026-11-05), while
    calling the deployment story weak.
Notes
  * USE-1 Methods: "otherwise write the most plausible one and say 'for example'". The use_case text has neither
    "for example" nor "ours"; only curation_comments and fit_reason say it. Follow wioa/acs ("For example, ...") or
    ny_wcb ("the use case is ours" in use_case). Wording only.
  * USE-9 (Should) asks before settling on approximate whether another use case fits directly. Not written down. The
    obvious candidate, a socioeconomic adjustment of school results (expected score from the background), has the
    label known, so it fails USE-9's "the label is not known". Approximate stands; one sentence would record that it
    was asked (chicago did).
  * Claim auditor finding 5: ProUni bars an edition taken as treineiro (status 3, 17-19% of rows), so the 450 bar does
    not apply to them. chile names its population mismatch in fit_reason ("the ministry's covers grades 7 to 12
    only"). Follow that: half a sentence in fit_reason.

**D3. The cohort: registrants present on both days (P3/P4; USE-8 Must, LEAK-22 Must)**
Status: the filter and the approximate fit are consistent. The record lacks the `Selection Bias` marker that the
same shape has carried in every recent case: a departure without a stated reason.

Precedents
  * LEAK-22 (diabetes_130_us): rows that cannot have the outcome leave. An absentee has no score at all, so the
    presence filter is this case, not framingham's (a competing event whose row keeps its label No).
  * USE-8 selection rule (Lennart, 2026-10-27) and selection.md "Selection bias": when the rows are not drawn from the
    population the use case predicts for, mark `Selection Bias`; the fit is approximate when the setting does not
    share the bias; "The marker stays either way".
  * tunisian_fraud_detection_challenge, CC 2026-11-05 (Lennart): `Selection Bias` set, "every row is an inspected
    taxpayer-year, while a real screening ranks all filers". The same shape: the actor ranks everyone, the labels
    exist only for a subset fixed after the prediction point.
  * lt_vehicle_loan_default_prediction (2026-11-05, Lennart): approved loans only. kumc_inpatient_aki_prediction
    (mediator 2026-11-09, marker on the record) and sinan_dengue_case_screening (mediator, "approximate +
    `Selection Bias`") in this batch.
  * The selection is measured: presence 58.0% for the lowest income band against 83.8% for the highest (2023), status
    1 at 58.4% against status 3 at 82.5% (claim auditor row 13b). The bias is not small and it runs with the
    strongest feature.

Prompt 2 (issue shape)

   2. **Set the `Selection Bias` marker on the record, as on tunisian_fraud_detection_challenge?**
      - **Problem:**
        - The department ranks every registrant at the close of registration, but only those present on both days have a score, between 45% (2020) and 73% (2019) of them.
        - Presence follows income and school status (58% present in the lowest income band against 84% in the highest, 2023), and the fit is approximate for this reason, yet the record has no marker[^p2rule].
        - tunisian_fraud_detection_challenge got the marker for the same shape on 2026-11-05: only inspected taxpayer-years have a label, while a screening ranks all filers[^p2prec].
      - **Options:**

        | | Option | What it does | Pro | Con |
        |---|---|---|---|---|
        | a | Set `Selection Bias` on the record; fit_reason unchanged | one marker | follows tunisian, lt_vehicle_loan, kumc and sinan; the marker says something special about the data | none found |
        | b (implemented) | No marker; the fit_reason names the selection | no change | the fit already says it | departs from four recent cases without a fact that sets ENEM apart |

      - **Recommendation:** a.
      - **Decision:** a or b?

      [^p2rule]: USE-8 (Must), selection paragraph (Lennart, 2026-10-27); selection.md, Patterns, "Selection bias" ("The marker stays either way").
      [^p2prec]: W/curation/records/tunisian_fraud_detection_challenge.md, CC 2026-11-05 (Lennart); W/curation/records/kumc_inpatient_aki_prediction.md; lt_vehicle_loan_default_prediction (use_case.md Cases, 2026-11-05).

**D4. The target: mean of the five scores, zeros kept (P3; USE-5 Must, TP-7 Must)**
Status: consistent with USE-5 and with the zero-keeping precedent. TP-7's testing step is not documented.

  * USE-5 ("predict what the actor would act on"; corporate_credit_rating, diabetes_3): the actor targets those
    likely below ProUni's 450-point mean of five, and the claim auditor confirmed that rule from MEC's ProUni 2023
    kit ("450 pontos de média nas notas das cinco provas"). The quantity matches the use case.
  * Zeros of a blank test or an annulled essay stay: framingham_heart_study_fhs (Lennart, 2026-10-22) keeps a row
    that can have the outcome with the label it had; ProUni's own mean counts the zeros. Consistent.
  * TP-7 (Must) asks, when the definition builds the target, for an established convention (holds: the ProUni mean)
    and to "test each candidate". Draft issue 3 offers three candidates (mean of five, mean of four, mathematics)
    with no measured signal or stability for the alternatives (audiology_diagnosis is the precedent of a tested
    re-definition). A short probe per candidate would let issue 3 carry numbers.
  * The claim auditor's finding 1 (16,029 blank day-2 tests in 2023, 6.3% of the 2023 window's MSE) bears here:
      - Its option (a), keep with a quantitative note, follows chicago_traffic_crashes (2026-11-05, Lennart: a 2023Q4
        recording step accepted as drift with its note).
      - Its option (b), drop rows whose day-2 answer strings are all blank, selects on the target's own inputs:
        those rows can have the outcome and have it (a zero). That is what LEAK-22's framingham case bars, unless a
        fact shows the blanks are a recording failure rather than the participants' answers. Then it would read as
        LEAK-25's "located by a rule", but that rule may not read the label, and the answer strings are the
        label's raw material. The mediator should name this if (b) is offered.

**D5. The history starts in 2018 (P4; SPLIT-20 Should, SPLIT-14 Must, SPLIT-21 Must)**
Status: consistent, reason stated. One note missing.

  * chile_school_dropout_mineduc_1m (this batch): history from 2018, COVID years kept "a yearly refit would have
    trained on them, and without them the 2022 window would train on 2 of 7 years, under half the rows". ENEM gives
    the same two reasons for 2018 and for 2020 in training.
  * aeolus (2026-10-12) and perth_house_prices (2026-10-26, "chosen from counts, not scores"): a recent stretch chosen
    from counts. ENEM's start is chosen from counts (58% against 46%), not from window scores, so SPLIT-21 holds.
  * 2017 left out for the years-since cap (11 instead of 12) is a stated CLEAN-21 cost; draft issue 4 leaves the
    choice to the curator. Fine.
  * Missing: SPLIT-20 says "check the history for breaks". The claim and column auditors found three inside the
    history: the 2020 "modelo simplificado" blanks TP_ENSINO for status 1 and drops EJA; "not informed" years since
    secondary rise from 2.5-3.2% to 8.1-10.9% from 2020; 2018's TP_ESCOLA codes are another variable. The chile panel
    conceded the same kind of point ("two breaks inside the history are not in the notes", SPLIT-20, CLEAN-21) and
    added a note. Name the breaks in splits_comment once the CLEAN-21 fixes are made.

**D6. Fallback RMSE (P6; MET-5, MET-6, MET-7, MET-11)**
Status: consistent.
  * MET-5: studies report RMSE, MAE and R^2 together (builder; claim auditor found MAE with R^2), no deliberate single
    choice: fallback, as gallstone_disease and early_stage_diabetes_risk_prediction.
  * MET-6/MET-7: the 450 bar is MEC's eligibility rule, and the decision to target at it is our use case, not a
    threshold the source fixed for scoring; "never invent a cost or a threshold" (taiwanese_bankruptcy_prediction,
    ljubljana_breast_cancer). MET-11 `context` needs a metric the task makes obvious, and nothing is that clear here
    (diamonds' rmsle had a clear relative-error argument).
  * The domain practitioner's checks show model orders under RMSE and
    under ROC AUC below 450 close but not identical; that is a weighing input for the mediator, not a precedent issue.

**D7. Municipality codes as categories; names not read (P7; CLEAN-12 Should)**
Status: departs from the rule's text without a stated fact, and is the same choice that is open on three batch
siblings.

Precedents
  * CLEAN-12 (amended 2026-11-01, Lennart): "a nominal code ... into a category of the words"; "A column that still
    ships as a number while its source has words for it is a gap to close, not a choice". credit_g (2026-10-31): "we
    want the right labels in all cases".
  * rais_employment_separation_1m: IBGE municipality (with CBO, CNAE, CONCLA) kept as codes, flagged "a departure from
    CLEAN-12 for the curator"; mediator issue 5 asks to decide sinan and chile alike, and the rais precedent checker
    counted three cases of one reason, "an amendment is due".
  * chile_school_dropout_mineduc_1m keeps communes as codes and drops the file's own names as "copies of codes"
    (rais PC: "the reverse of CLEAN-12"). sinan_dengue_case_screening_1m keeps IBGE municipality codes.
    ny_wcb_assembled_claims_1m decodes NAICS and WCIO as "words [code]".
  * zillow_prize census_tract (2026-10-26): kept as a code, since a tract has no words.
What ENEM does
  * NO_MUNICIPIO_ESC and NO_MUNICIPIO_PROVA (the names, in the same CSV) are "not read" as copies, and the codes ship
    as categories. The note presents this as following CLEAN-12. The column auditor agrees (CLEAN-5, copies). The
    rais panel reads the same pattern as a departure.
  * ENEM's case for decoding is stronger than rais's: the words are in the file, so no outside table is needed, and
    rais's distinguishing fact (an outdated codebook) does not apply. Names repeat across states, so the words would
    be "Name (UF)" or "Name [code]".
  * If kept, this is the fourth case of one reason in the batch (rais, sinan, chile, ENEM): the amendment option
    should be decided once.

Prompt 3 (issue shape)

   3. **Ship the two municipalities as their names with the state, as CLEAN-12 reads, or keep the IBGE codes under one batch-wide amendment?**
      - **Problem:**
        - The school and exam municipalities ship as 7-digit IBGE codes, and the names in the same file are not read as copies of the codes[^p3rule].
        - The rule decodes a nominal code whose source names it in words, and rais keeps the same IBGE codes as an open departure, asking to decide sinan and chile alike[^p3batch].
        - Kept as codes, ENEM is the fourth case of this reason in the batch, so an amendment is due rather than a fourth exception.
      - **Effect on the task:** none on the information: a name with its state maps one to one to the code; the levels stay 5,551 and 1,750.
      - **Options:**

        | | Option | What it does | Pro | Con |
        |---|---|---|---|---|
        | a | Decode into "Name (UF) [code]" from the file's own name columns | words and code in one category | follows the rule; no outside table; keeps the digits for anyone who wants the hierarchy | longer labels; the name columns must be read and checked one to one |
        | b (implemented) | Keep the codes; record an exception | as now, the note rewritten as a departure | no change | a fourth exception of one reason; no fact sets ENEM apart, as the words are in the file |
        | c | Amend CLEAN-12: a national place or classification code with thousands of levels may ship as its code | settles rais, sinan, chile and ENEM at once | one rule for the batch | reverses the 2026-11-01 call for jobs and places |

      - **Recommendation:** a, unless the curator prefers c for the batch; decide it with rais issue 5.
      - **Decision:** a, b or c?

      [^p3rule]: CLEAN-12 (Should; amended 2026-11-01, Lennart): a nominal code into a category of the words; "A column that still ships as a number while its source has words for it is a gap to close, not a choice."
      [^p3batch]: rais_employment_separation panel, mediator issue 5 and precedent checker D5 (2026-11-09); chile_school_dropout_mineduc_1m and sinan_dengue_case_screening_1m keep the codes; ny_wcb_assembled_claims_1m decodes "words [code]"; principles.md, Exceptions and amendments (third exception, amendment due).

**D8. Accepting `task_time_on_few_unique` (six editions)**
Status: consistent.
  * wisconsin_local_government_property_insurance_fund (accepted, 2026-11-08 batch: "five policy years ... the file
    has no finer time"), spanish_homeowners_motor_insurance_2010_2014 (Andrej, 2026-11-02: "the panel has no finer
    time"), tunisian_fraud_detection_challenge ("finer timestamps are unavailable"), chile (proposed: "the label and
    the refit are yearly, and the history starts in 2018 (SPLIT-20)").
  * Every precedent states why there is no finer time; the proposed ENEM text does not. ENEM's fact is that the exam
    is held once a year, so an edition is the natural time point, and the six come from the SPLIT-20 choice and the
    2024 file split. Suggested text: "six yearly editions, 2018-2023: the exam is held once a year, so an edition is
    the finest time; the history starts in 2018 (SPLIT-20) and ends in 2023 (no common key from 2024); a refit
    trains on whole editions, and an inner validation holds out the newest training edition".

**D9. CC BY-ND 3.0 (EV-4 Must)**
Status: the definition is consistent: a one-line note and the license field, no issue (lucas_topsoil; numerai,
aeolus, african_credit_scoring_challenge, 2026-10-21; wisconsin, 2026-11-06, where an issue on the licence was
withdrawn: "a licence decides no fix and is no issue for the curator").
  * Claim auditor finding 8 calls the ND clause "a question for the curator and the release". EV-4 bars the first
    half: it is a release-checklist item and goes into no REVIEW.md issue. The same holds for rais and sinan.

**D10. Year 2026 (P5, PROV-9 Must)**
Status: consistent with the snapshot clause. The stated analogy is not exact. A note, no prompt.
  * PROV-9: "A source that grows over time ... takes the year of the snapshot we pin"; chicago_traffic_crashes (2026,
    the snapshot), fpa_fod_wildfire_cause_1m (2026, "the edition we pin"). The ENEM series grows by an edition a
    year, so the snapshot clause applies.
  * chile ("the newest file, of 2025, was published in March 2026") and rais ("the 2025 base-year files were posted on
    2026-05-13") take the first appearance of their newest data. ENEM's 2026 is a re-upload date of the 2023 zip, whose
    data INEP first published earlier (about 2024; not checked). PROV-9 also says "not the date of the copy we
    download". The note should say plainly that 2026 is the pinned snapshot (the 2023 zip as re-published on
    2026-07-09), not "the newest file". If the curator prefers chile's reading, the year is the first publication of
    the 2023 microdata. Whether the 2026 upload changed any row is untested.

</details>

<details><summary>Advocate</summary>

ADVOCATE, OPENING BRIEF: enem_entrance_exam_scores (folder enem_entrance_exam_scores_1m), 2026-11-09

Position: ship as defined, with the changes below that need no decision (P7 fixes in `_clean`, wording, notes).
Every validity Must holds on four independent checks. The real problems the panel found are P7 cleaning gaps in the
2018-2019 training editions and one 2023 target artefact, and each has a remedy far below exclusion.

Judgment record (as I read the evidence)
Validity: SEL-1 holds (no law bars the grounds; curator's call stays open); USE-1 and USE-5 hold (approximate fit);
LEAK-10 holds for all 43 inputs; SPLIT-1, -9, -10, -13, -14 hold; PROV-8, -9 hold.
Value: TP-1 to TP-4 hold; MET-5/MET-11 fallback rmse.
Quality: CLEAN-21 triggered twice, fixed cheaply in `_clean`; CLEAN-12 for municipalities open as a batch-wide question.

1. No leak and no exploit: the evaluation is honest (P4; LEAK-10 Must, SPLIT-1/-14 Must, LEAK-34).
   Evidence: every input is on the registration form (claim auditor: Edital 2023 5.2.3, 5.2.5, 5.4.1, questionnaire
   "não poderão ser alterados"). The column auditor reached the same result column by column. The task gamer ran
   three exploits (test-row counts, repeat-taker matching, test-year make-up) and all stayed within seed noise
   (+-0.03 RMSE). His best single feature scores 85.4 against 75.5 for the full model, and a model on missing
   indicators alone scores 93.3 (about the SD of 89). Exact copies across the split are 0.0%, tight repeat-taker
   matches are 0.14-0.28%, and 1-NN R^2 is -0.24. Split auditor: "right with notes". The 2021 window trains on 58.4%
   (SPLIT-14), the scores come out before the next registration closes (SPLIT-10), and repeat takers sit on both
   sides as in deployment (LEAK-34).
   Why it outranks: P4 is the validity gate the critic would have to break, and no agent found a Must failing.

2. SEL-1 (P1, Must): race, sex and income do not make this an ethics case. Keep them; the curator decides.
   Evidence: three agents (column auditor, precedent checker, domain practitioner) independently found no law that
   bars these grounds for educational support. Lei 12.711/2012 uses race and income for admission, and the STF
   upheld it (ADPF 186). MEC's CPOP cursinhos must prioritise Black, Indigenous and low-income students. Removal
   costs +0.18-0.20 RMSE (race), +0.25-0.29 (race and sex) and +0.70-0.91 (all three); the claim auditor replicated
   these numbers. Precedents: chile_school_dropout_mineduc_1m keeps sex ("the use case offers support"), and
   sinan, diabetes_130_us and kumc keep race. The Tensions row drops a factor where the actor's own law bars it
   (bemtpl97, rais), and that trigger is absent here.
   Why it outranks: the Assam sibling's `Ethical Issue` under `TBD -> Yes` contradicts SEL-1 itself, so under
   principles.md it is flagged, not followed. If the curator reads it otherwise, the remedy ladder says drop race
   (smallest cost per ground; sex is the weakest for this actor), never exclude.

3. A real use case with the right target (P3; USE-1, USE-5 Must, USE-8 Must at approximate).
   Evidence: the ProUni rule ("450 pontos de média nas notas das cinco provas", essay > 0) was verified from MEC's
   2023 kit. The five-score mean with zeros settles eligibility for all but 0.07-0.18% of rows. The domain
   practitioner played the actor and would use the model: the regression ranks "below 450" better than a
   classifier trained on the bar (AUC 0.775/0.779/0.782 against 0.759/0.766/0.768). Top-20% precision is
   0.39-0.47 against base rates of 0.18-0.23. The blind reviewer named "targeting prep or tutoring programmes"
   without reading our notes. Fit: approximate, which every agent accepts.
   Concede, as changes with no decision: write the actor as an NGO or CPOP cursinho or a Seduc with its own intake
   form, with "for example" (USE-1 Methods, as wioa/acs). Add to fit_reason that absentees are mostly low-income
   (38% absent at up to 1 MW against 18% above 4 MW, 2023) and that treineiros (17-19%) cannot use the score. Add
   one USE-9 sentence. The `Selection Bias` marker (precedent checker prompt 2, as on tunisian, lt_vehicle_loan,
   kumc and sinan): I support setting it. It is a marker, not a data change.
   Why it outranks: the blind reviewer's "weak deployment story" is answered by measurement C. A thin story is no
   P3 failure when actor, moment and decision are written and checked against MEC's own rules.

4. Worth benchmarking, scored by the right metric (P6; TP-1 to TP-4, MET-5, MET-6, MET-11).
   Evidence: LightGBM R^2 0.380 against 0.354 for linear (+0.025, paired SE 0.005); RMSE 71.5 against a dummy of
   91.6, in 3 of 3 windows. Replicated independently: claim auditor 70.17/70.39/76.10 against 70.22/70.43/76.00;
   split auditor mean 71.48; task gamer 71.58. RMSE picked the AUC-best model in 3 of 3 windows (domain
   practitioner). The 450 bar is an eligibility rule, not a scoring threshold the source fixed (MET-7: never
   invent one; precedents gallstone_disease, ljubljana_breast_cancer).
   Against the blind reviewer's "drop the municipality codes" (R^2 0.371 to 0.382 without them): how a model
   handles a 5,551-level code is benchmark content. Tensions row "Width against model limits": a model's
   limitation is never an argument.

5. Cleaning gaps are real, P7, and cheap to fix (CLEAN-21 Should; principles step 3, remedy ladder "fix the
   definition").
   Concede: 2018 TP_ESCOLA is the school's administration, not the dictionary code (949 municipal-school rows
   shipped as "abroad"; federal-school students missing). TP_ENSINO is filled for status 1 only in 2018-2019, and
   EJA appears only in 2018. "Not informed" years-since rises from 2020. Fixes (column and claim auditors): 2018
   codes 2 and 3 to public, 4 to private, federal to public, drop "abroad"; modality missing outside status 2 and
   2018 EJA to missing; one note bullet for the years-since drift. Measured: -0.024 mean RMSE, better in 5 of 6
   runs. Every affected row is on the training side, and no test window carries these levels (task gamer). Also
   name these breaks in splits_comment (SPLIT-20, as on chile).
   school_operating_status: weak at most (0.17% of rows non-active, group R^2 gain 0.00016, closed schools score
   higher, not lower). I accept dropping it at zero cost (column auditor), or keeping it with its Potential-leak
   note (Tensions row on weak leaks, LEAK-30). Either way it is not a ship blocker.
   Why it outranks: "A very real task carries cleaning imperfections when they are written down"; these are fixed
   outright.

6. The 2023 blank day-2 rows: keep, with a quantitative note (USE-5 Must, LEAK-22; precedent framingham,
   chicago_traffic_crashes).
   Concede the fact: 16,029 rows (0.60% of 2023, against 0.005-0.011% before) left CN and MT fully blank, and
   carry 6.3% of the 2023 window's MSE (+2.2 RMSE). Cause unknown.
   Dispute the filter (claim auditor option b): those rows have the outcome. A zero is what ProUni counts, so
   dropping them selects on the target's raw material without a recording fact, which LEAK-22's framingham case
   bars (precedent checker D4). chicago_traffic_crashes kept a recording step with a note. The blind reviewer's
   "drop mean_score == 0" (3 rows of 200k) fails for the same reason.
   Mildest remedy: write the counts and the RMSE effect into the Anomaly note and carry the number into draft
   issue 3. No data change.

7. Split, history and the rest are wording, no re-split (SPLIT-20 Should, SPLIT-10, EV-4, PROV-9).
   - SPLIT-20: keep 2018-2023 and restate the reason. 2017 is on the old essay level (529 against 622-629 in the
     test editions) and the floor does not need it.
   - SPLIT-10: optional clause on when the public microdata appear. A gap would break the floor (43.5%).
   - The task gamer's "1M cap discards rows" (0.23 RMSE on r0) is the declared `_1m` protocol, already in
     splits_comment.
   - Accept task_time_on_few_unique with the precedent checker's text ("the exam is held once a year").
   - The licence is a release-checklist item, not an issue (EV-4; wisconsin).
   - PROV-9: say "pinned snapshot".
   - The blind reviewer's "undocumented sampling" is answered by the version comment, and the claim auditor
     confirmed the uniform 25% (means within 0.15 points).
   - CLEAN-12 municipalities: the names are in the same CSV, so decoding to "Name (UF) [code]" is a cheap fix. I do
     not oppose it, or the batch amendment decided with rais. Either way it is a P7 question.
   Why it outranks: all Should-level or below, each with a remedy in the definition. Independent failures are not
   conflicts, and none here is a Must.

Draft issues for the curator stay as the builder wrote them (SEL-1 keep; present-only keep; mean of five keep;
history as is). Add the `Selection Bias` marker and the CLEAN-12 municipality question from the precedent checker.

</details>

<details><summary>Advocate rebuttal</summary>

ADVOCATE REBUTTAL: enem_entrance_exam_scores (folder enem_entrance_exam_scores_1m), 2026-11-09 (to the critic's opening brief)

The critic asks for no exclusion and does not argue the split, the metric, the signal or the licence. We agree on
every remedy except one (sex, point 1). What is left is whether a few points are Must failures or text fixes. Every
remedy below is a fix to the definition or a note, so the dataset ships after these changes.

1. SEL-1, sex and the Assam pair. I partly concede.
   - Conceded: the quota law covers race and income, not sex. The decision should be one recorded CC line on all
     three grounds, taken together with the Assam marker. A note that the model serves a support offer and not
     screening people out is a good addition.
   - Disputed: sex needs no drop to have a reason. The reason that covers it is the one in chile_school_dropout_
     mineduc_1m: "the use case offers support, not a decision against the student". The same reason keeps sex in
     open_university, student_portuguese and early_learning, all shipped (precedent checker D1). Dropping sex here
     alone would treat like cases unlike, which is principles.md "Consistent judgement" case 2 the other way round.
   - The Assam marker is the inconsistent precedent: `Ethical Issue` is the marker of a Must whose verdict is `No`,
     yet that record is `TBD -> Yes`. So it is flagged, not followed. Recommendation: keep all three (the precedent
     checker's option a, decided with d). If the curator wants a drop, the order is race first (smallest cost per
     ground), then sex (+0.07-0.09).

2. USE-1 / USE-3, the actor without the inputs. I concede the text and dispute that a Must fails.
   - Conceded: the use_case should name an NGO or CPOP cursinho, or a department filling limited places, that asks
     the registration items on its own intake form, with "for example". fit_reason should add the grades and
     assessments a department holds (column auditor 5, domain practitioner 1).
   - Disputed: "a decision nobody can make" is not what the evidence shows. The domain practitioner, playing that
     actor, would use the model as a screen. Top-20% precision is 0.39-0.47 against base rates of 0.18-0.23. The
     items are generic and the actor collects them at the same moment (USE-3 holds: known then, to that actor).
   - USE-1 is met by rewriting the text, the first rung of the remedy ladder. The data needs no change.

3. USE-8, the marker and the gradient. I concede in full, as my opening point 3 did: set `Selection Bias` (as on
   tunisian, lt_vehicle_loan, kumc and sinan), name the income gradient (38% absent at up to 1 MW against 18% above
   4 MW, 2023) and the treineiro share (17-19%) in fit_reason. The fit stays approximate and the rows do not change.

4. USE-5, the 2023 blank day-2 rows. I concede.
   - Remedy (a): the same as my point 6. Add the numbers to the Anomaly bullet (0.6% of 2023, 6.3% of that
     window's MSE), correct the zero counts, and carry the numbers into draft issue 3.
   - Remedy (b), the cause check: I agree it is the right EV-1 step and cheap. Its result decides a filter. The
     dataset ships before the result: until a recording failure is shown, LEAK-22 (framingham) keeps the rows.
   - Where we differ: the critic labels this a Must "weighed". Remedy (a) satisfies USE-5 as the target is defined:
     ProUni counts these zeros.

5. LEAK-10 clause 2, school_operating_status. I concede: drop it. The amended clause the critic quotes makes the
   decision. Nothing about the census year can be traced, and "changes no score" is no reason to keep. My opening
   left drop or keep open; the rule leaves only drop. The cost is nil (group R^2 0.00016) and the actor knows its own
   school's status.

6. CLEAN-21, school type, modality and the not-informed drift. I concede in full. These are the same fixes as my
   point 5: 2018 codes remapped and "abroad" removed, modality missing outside status 2 and 2018 EJA missing, a
   bullet for the not-informed drift, and the breaks named in splits_comment. Measured: -0.024 RMSE, training
   editions only.

7. CLEAN-12 and the refuted notes. I concede.
   - Notes to correct: registration "May to July"; 2017 left out for the essay level break; the year as the pinned
     snapshot (PROV-9); the task_time_on_few_unique reason ("the exam is held once a year").
   - CLEAN-12: decode the municipalities as "Name (UF) [code]" from the file's own columns, or settle one batch
     amendment together with rais issue 5. It is a P7 Should either way.

Result: after this round the only open curator calls are SEL-1 (keep all three, decided with the Assam marker) and
the cause of the 2023 blank rows (a note now; a filter only if a recording failure is shown). Everything else is a
change that needs no decision, and no Must stays broken once they are made.

</details>

<details><summary>Critic</summary>

CRITIC, OPENING BRIEF: enem_entrance_exam_scores (folder enem_entrance_exam_scores_1m), 2026-11-09

Position: ship only after changes. I do not ask for exclusion. The split, the metric (fallback rmse) and the signal
hold (split auditor, claim auditor rows 37-39, task gamer: no exploit). But the use case is written for an actor who
cannot hold the inputs, the selection it names is understated and unmarked, the newest test window scores a 2023-only
artefact, one input has undocumented timing, and two columns are decoded against what the data shows.

Judgment record
Validity: SEL-1 open (curator's call; the Assam pair is not settled); USE-1/USE-3 triggered (actor without the
inputs); USE-8 triggered (marker missing, gradient unnamed); USE-5 weighed (2023 artefact in the test target);
LEAK-10 clause 2 triggered, weak (school_operating_status); SPLIT-1/9/10/13/14 hold.
Value: MET-5/MET-6/MET-11 fallback holds; TP-1 to TP-4 hold.
Quality: CLEAN-21 refuted twice (2018 school type, modality); CLEAN-12 departure without a stated fact.

1. SEL-1 (P1, Must): race, sex and family income stay with only a note, and the same task's sibling is flagged
   `Ethical Issue` for caste and gender.
   Problem: the definition keeps the three grounds "now", deferring to the curator. Its stated reason (the quota law,
   Lei 12.711/2012) covers race and income, not sex; the domain practitioner found no programme that uses sex and "would
   not object to dropping it alone". The Assam sibling (student_performance_on_an_entrance_examination, `TBD -> Yes`
   with `Ethical Issue`) is the same task with the analogous grounds; the precedent checker finds no fact in the
   definition that sets ENEM apart (India also reserves by caste; a support use case could be written for Assam).
   Effect: family income is the strongest single input (single-feature R^2 0.199; gain importance 0.34, blind
   reviewer). Dropping race costs +0.18 to +0.20 RMSE, race and sex +0.25 to +0.29 (the builder's probe,
   replicated by the claim auditor), on 70-76.
   Evidence: column auditor and precedent checker found no law that bars the grounds for a support offer (LGPD art. 11
   II b; Lei 12.711; ADPF 186), so a drop is not forced. The open point is consistency, not legality.
   Rule: SEL-1 (Must, P1); principles.md "Consistent judgement" case 2 (a similar precedent decided the other way).
   Remedy: no change to the data unless the curator decides so. A recorded CC decision on all three grounds, taken
   together with the Assam marker (keep both, or flag both); the reason must name what covers sex (or drop sex, cost
   about +0.07-0.09 RMSE); and a note that the model is for a support offer, not for screening anyone out (the
   domain practitioner's reuse risk).

2. USE-1 / USE-3 (P3, Must): the named actor does not hold the inputs at the prediction point.
   Problem: use_case says "a state education department or a school network ranks its registered students" from the
   registration form. INEP holds that form and questionnaire; Edital 30/2023 items 14.8-14.9 release them to MEC
   programmes and higher-education selection, not to departments or schools (column auditor 5). Ceará's Seduc
   estimated registration from census aggregates, without a list (domain practitioner, sources). A department also
   always holds grades and state assessment scores, which it would use and which this task lacks (R^2 about 0.38).
   Effect: the task as written simulates a decision nobody can make with these inputs. The realistic actor is an NGO
   or public cursinho (MEC CPOP, 20-40 places, priority by race and income) or a department before it links grades,
   asking the same items on its own intake form. The data then fit; the text does not.
   Rule: USE-1 (Must: actor, moment, decision, checked against every column); USE-3 (Must: what is known then, to whom);
   USE-1 Methods ("for example" when the use case is ours; precedent checker D2: wioa, acs, ny_wcb).
   Remedy: rewrite use_case and fit_reason: "For example, an NGO or public cursinho programme (MEC's CPOP), or a state
   department filling limited places, asks its applicants the registration items on its own intake form ...", and add
   to fit_reason that a department would also hold grades and assessments. Text only.

3. USE-8 (P3, Must): the selection by presence is understated and the marker is missing.
   Problem: rows are registrants present at all four tests, 45% (2020) to 73% (2019) of registrants. Presence runs
   with the strongest feature and with the target population: 2023, up to 1 minimum wage 61.8% present against 81.7%
   above 4 (domain practitioner, all 3,933,955 registrants); income band A 58.0% against P 83.8%, status 1 58.4%
   against status 3 82.5% (claim auditor 13b). fit_reason says only "a third of the registrants stay away". Further,
   status-3 rows (treineiros, 17-19% of each edition, 19.1% of 2023) cannot use the edition for ProUni or FIES, so the
   450 bar of the use case does not apply to them (claim auditor 5, domain practitioner 3).
   Effect: the people the offer is for are the ones most often missing from the rows; a sixth of the scored rows are
   outside the decision's bar.
   Rule: USE-8 (Must; selection paragraph, Lennart 2026-10-27: "fit_reason names the selection and the marker stays");
   selection.md "Selection bias". Precedents with the same shape carry `Selection Bias`: tunisian_fraud_detection_
   challenge (CC 2026-11-05), lt_vehicle_loan_default_prediction, kumc, sinan (precedent checker D3). No fact sets
   ENEM apart.
   Remedy: set `Selection Bias` on the record; fit_reason names the income gradient (38% absent at up to 1 MW against
   18% above 4 MW, 2023) and the treineiro share. Fit stays approximate. No change to the rows (no score exists for
   absentees; a binary all-registrants sibling is optional, not asked).

4. USE-5 (P3, Must, applied to the test target): the 2023 test window scores a recording or behaviour that training
   never shows.
   Problem: 16,029 participants of 2023 (0.60%) were present on day 2 and left natural sciences and mathematics wholly
   blank; 2018-2022 had 417, 344, 319, 191 and 247 (0.005-0.011%). They are spread evenly over the four booklets;
   13,219 wrote a normal essay; day-1 mean 478, target mean 281 (claim auditor 1). The definition calls the jump
   "unexplained; kept" and misstates the 2018-2022 zero counts ("275 to 745 per test" holds for CN and MT only; CH has
   2,230-3,761 a year).
   Effect: those rows are 0.59% of the 2023 test rows and 6.3% of its MSE: RMSE 76.10 with them, 73.89 without, about a
   third of the gap between the 2023 window and the other two, and ten times the SEL-1 differences. In 2021-2022 the
   same kind of row carries 0.1-0.2%.
   Rule: USE-5 (Must, the target the actor acts on); EV-1 (settle the fact first). Against filtering now: LEAK-22's
   framingham case (precedent checker D4): rows that have the outcome keep it unless a fact shows a recording failure.
   Remedy: (a) now, an Anomaly bullet with the numbers ("test-only: 0.6% of 2023, 6.3% of that window's MSE") and the
   corrected zero counts, and draft issue 3 carries them; (b) one decisive check of the cause (answer strings blank by
   exam municipality and application date, any INEP note on 2023 day 2). Filter in every edition only if (b) shows a
   recording failure.

5. LEAK-10, second clause (P4, Must, weak): `school_operating_status` has undocumented timing and is kept with a note.
   Problem: no dictionary or Leia-me names the census year (column auditor grepped "censo": no hit). One internal sign
   of a later reading: "closed in an earlier year" for the school the registrant finishes that same year, 0.03-0.12%
   of rows per edition. The value cannot be located row by row.
   Effect: measured gain is nil (group-mean R^2 0.00016 on top of administration, location and state; 0.17% of rows
   non-active). The actor knows its own school's status anyway (domain practitioner).
   Rule: LEAK-10 clause 2 (Must, amended 2026-11-08): values that cannot be located "go when they may carry a gain and
   stay with a note only when the part that can be traced shows none"; nothing here can be traced; "a removing it
   changes no score test alone is still no reason to keep".
   Remedy: drop the column and its Potential-leak bullet. Cost: none measurable.

6. CLEAN-21 (P7, Should): two columns are decoded against what the data shows, and the notes state the opposite.
   (a) 2018 `secondary_school_type` is the identified school's administration, not the self-report: code 3 is municipal
   (9,711 of 9,762 rows, all at Brazilian schools), code 2 state (840,241 of 840,392), code 4 private (237,816 of
   237,816), and all 42,666 federal-school students are code 1, i.e. missing. SCHOOL_TYPE_2018 turns the municipal
   students into "abroad", a level with 0 rows in every other edition (claim auditor 2; column auditor 2, sample
   crosstab agrees).
   (b) `secondary_school_modality` is filled for status 1 only in 2018 (54.0%) and 2019 (49.7%), 0.0% from 2020; EJA
   exists only in 2018 (7.19% of known values) and appears as missing from 2019 (claim auditor 3; column auditor 3).
   The note "the modality of those who have finished or are finishing" is wrong for every test window.
   (c) "not informed" years since secondary rises from 2.5-3.2% (2018-2019) to 8.1-10.9% (2020-2023), unnoted.
   Effect: feature levels and missingness patterns that exist only in training editions. Small on the score: (a) and (b)
   fixed, mean -0.024 RMSE, better in 5 of 6 runs (column auditor).
   Rule: CLEAN-21 (Should); EV-2 (a measurement on the data beats the dictionary); SPLIT-20 ("check the history for
   breaks", as the chile panel conceded).
   Remedy, cheap and safe: 2018 codes 2 and 3 to public, 4 to private, code 1 at a federal school to public, no
   "abroad" level; modality missing outside status 2 in every edition and 2018's EJA missing; correct the
   SCHOOL_TYPE_2018 docstring and the CLEAN-21 bullet; one bullet for (c); name the breaks in splits_comment.

7. CLEAN-12 (P7, Should) and refuted notes: the municipality names are in the file but the codes ship.
   Problem: NO_MUNICIPIO_ESC and NO_MUNICIPIO_PROVA sit in the same CSV and are "not read as copies"; the note presents
   this as following CLEAN-12, whose amended text says "a column that still ships as a number while its source has
   words for it is a gap to close, not a choice". It would be the fourth case of one reason in this batch (rais,
   sinan, chile), so an amendment is due (principles.md, Exceptions and amendments).
   Rule: CLEAN-12 (Should; amended 2026-11-01).
   Remedy: decode as "Name (UF) [code]" from the file's own columns, or decide one batch-wide amendment with rais
   issue 5; either way the note must say which. Along with it, fix the notes the evidence refutes: registration closes
   "May to July" (2021 ran 30 June to 14 July); the 2017 omission's reason is the essay level break (529 in 2017
   against 622-629 in the test editions, split auditor 1), not the years-since cap; the year is the pinned snapshot
   of the 2023 zip (PROV-9), not "the newest file"; the task_time_on_few_unique acceptance says why no finer time
   exists (the exam is once a year; precedent checker D8).

Not argued (the evidence does not back a case): the temporal split and its 2018 start (SPLIT-14 58%); no gap
(SPLIT-10; the public-microdata delay is a one-off, split auditor 2); repeat takers (LEAK-34 holds; 1-NN R^2 -0.24);
the fallback rmse (picked the AUC-best model in 3 of 3 windows); the licence (EV-4: release checklist, no issue); the
1M train subsample (row budget; 0.13-0.23 RMSE, a protocol choice).

</details>

<details><summary>Critic rebuttal</summary>

CRITIC REBUTTAL: enem_entrance_exam_scores (folder enem_entrance_exam_scores_1m), 2026-11-09 (to the advocate's opening brief)

The advocate's brief and mine now agree on every remedy except two details (SEL-1's Assam pair, the
school_operating_status option). Verdict unchanged: ship after changes. No exclusion asked by either side.

A1 (no leak, no exploit; P4). Concede. Split and leak checks hold, and I argued none of them. One exception, below at
   A5: one input does not meet LEAK-10's second clause as kept.

A2 (SEL-1 keep, curator decides). Concede that no law bars the grounds and that exclusion is off the table. Dispute
   one step: the advocate reads principles.md "a precedent that contradicts a rule is flagged, not followed" as
   licence to set the Assam sibling aside. The same sentence goes on: "one of the two is wrong". Flagging means the
   pair gets settled, not that ENEM ships while Assam keeps `Ethical Issue` under `TBD -> Yes`. Consistent judgement,
   case 2, asks for one decision on both records. The advocate's draft issue ("SEL-1 keep") leaves Assam open.
   The advocate also concedes "sex is the weakest for this actor", and the definition's only stated reason (the
   quota law) does not cover it. Remedy stands: a CC decision on all three grounds that settles the Assam marker in
   the same decision (the precedent checker's options a/d), with a reason that covers sex or sex dropped.

A3 (real use case, right target). Concede the target (USE-5: the ProUni mean, verified), the regression over the
   classifier (AUC 0.775-0.782 against 0.759-0.768) and the approximate fit. The advocate concedes my points 2 and 3
   in full: the actor rewritten as NGO/CPOP/Seduc with its own intake form, "for example", the income gradient and
   the treineiro share in fit_reason, a USE-9 sentence, and the `Selection Bias` marker. One label to correct: the
   advocate writes "USE-1 holds" in the judgment record. As written today the actor cannot hold the inputs (Edital
   30/2023 14.8-14.9), so USE-1/USE-3 are triggered and fixed by the rewrite, not holding. The remedy is the same.

A4 (worth benchmarking, fallback rmse; municipality codes stay). Concede. I did not argue against the metric or the
   signal, and I agree that a model's trouble with a 5,551-level code is no argument (Tensions, width against model
   limits).

A5 (cleaning fixes; school_operating_status keep or drop). Concede the CLEAN-21 fixes as the advocate lists them. I
   dispute "or keeping it with its Potential-leak note (Tensions row on weak leaks, LEAK-30)". That row is about
   transductive leaks, i.e. scaling over all rows (sf_permit_time, home_credit). This column's problem is a value read
   at an unknown later census. LEAK-10's second clause (Must, amended 2026-11-08) is the rule for that case, and it
   decides: values that cannot be located row by row "go when they may carry a gain and stay with a note only when
   the part that can be traced shows none". Nothing here can be traced (no census year in any dictionary or
   Leia-me). The internal sign points to a later reading ("closed in an earlier year" for the school the registrant
   finishes that year, 0.03-0.12% of rows). "A removing it changes no score test alone is still no reason to keep."
   The more specific Must wins over a Tensions row about another mechanism. Remedy stands: drop the column. I agree
   it costs nothing and blocks nothing once dropped.

A6 (2023 blank day-2 rows: keep with a quantitative note). Concede: no filter without a recording fact (LEAK-22,
   framingham), and the note with the counts and the RMSE effect (6.3% of the 2023 MSE, 76.10 against 73.89) goes in
   now. I keep one addition the advocate does not oppose: EV-1, one check of the cause (blanks by exam municipality
   and application date, any INEP note on 2023 day 2), so that draft issue 3 rests on a fact rather than on
   "unexplained". The 2018-2022 zero counts in the note must also be corrected (claim auditor, claim 16).

A7 (split and wording; CLEAN-12). Concede all: SPLIT-20 reason restated (the essay level), the optional SPLIT-10
   clause, the 1M cap as protocol, the task_time_on_few_unique text, PROV-9 "pinned snapshot", the licence as a
   release item. On CLEAN-12 we agree: decode to "Name (UF) [code]" or settle the batch amendment with rais. Either
   way it is a P7 item that goes to the curator.

Draft issues as I would leave them for the mediator: (1) SEL-1, decided together with the Assam marker; (2)
`Selection Bias` set and fit_reason rewritten (agreed); (3) target kept with the 2023 numbers and the cause check;
(4) history as is, reason restated (agreed); (5) CLEAN-12 municipalities, decided with rais issue 5. To apply without
a decision: the actor rewrite, the CLEAN-21 fixes, the corrected notes, and dropping school_operating_status (unless
the mediator rules LEAK-30 applies).

</details>
