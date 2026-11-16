# sivep_gripe_sari_outcome

**Outcome:** added. The AI recommends shipping it with the panel's changes, which are made. Brazil's national register of hospitalised severe acute respiratory illness (SIVEP-Gripe, Ministry of Health): will a patient admitted with SARI die in hospital, judged from what the notification form records at admission? 790,430 admissions of January 2023 to June 2026 (9.3% deaths), split by admission date into three half-year test windows (January 2025 to June 2026) with a one-month gap; fallback `roc_auc`.
Verdict: ship after changes (made).
Validity: SEL-1 holds (race or colour is a call taken alike with rais_employment_separation_1m, issue 3); USE-1 holds, fit approximate (form only, no vital signs); USE-3 holds after naming two groups (intensive care on the admission day, hospital-acquired SARI); USE-5 holds (death of any cause); LEAK-10 triggered four times and fixed (forms notified on or after the outcome dropped, in-stay free-text cells blanked (808 rows by the panel's count without the exception for patients who arrived intubated; 787 with it before the late forms are dropped, 634 in the shipped rows), the survivor-marking vaccine blanks set to "No", vaccine day counts in 30-day bins); LEAK-17 triggered by a person key the exact vaccine dates rebuild, fixed by the bins; LEAK-24 holds (end 2026-06-30, censoring note); SPLIT-9, SPLIT-14 (oldest train side 50.7%), SPLIT-20/21 hold.
Value: no task-probe flag; LightGBM 0.878-0.883, age alone 0.81; smallest test class 9,167 deaths.
Quality: CLEAN-11/12/14 fixes made (hospital as "name [municipality code]", schooling under 7 missing, impossible values missing, one name per municipality code).
Weighed: gap 0, source + (national register with a dictionary), shape + (790k rows, mixed inputs, temporal), use case + (bed planning and monitoring), fit - (form only, no vital signs; the per-patient framing is ours); together 0 in the priority.
For the curator: issue 1 (confirm the drop of the late forms), issue 2 (intensive-care-on-admission flag), issue 3 (race or colour, with rais), issue 4 (metric).

**Main points:** Confirm the drop of the 132,512 forms notified on or after the outcome (14.4% of rows, a quarter of the deaths, nearly all admission-day deaths; issue 1, implemented, recommended); name the patients in intensive care on the admission day or add a flag (issue 2: naming implemented and recommended); keep or drop race or colour and the community fields, decided alike with rais_employment_separation_1m issue 1 (issue 3, kept as is, no recommendation here); keep the fallback `roc_auc` or take `log_loss` for bed planning (issue 4, `roc_auc` implemented and recommended).

**Record judgment:** valid. The record's fields agree with the definition (GOV Website, medical & healthcare, binary classification, temporal). The screening's "4,060,608 rows for 2020-2024" is the register's size; the task keeps the admissions since 2023 (the register changed with COVID-19) with the late forms out (922,908 rows before the drop, 790,430 shipped).

**Issues for Lennart:**

1. **Keep the forms notified on or after the outcome out of the data, as now?**

   * **Problem:**
     - The definition drops 132,512 forms (14.4%: 7.5% notified after the patient left, 6.8% on the day of the outcome), which hold 25% of the deaths and whose answers and blanks follow the outcome.
     - Kept, they lift the test score by about 0.005 ROC AUC, more than double the 0.002 the builder's note gave, so the definition now drops them[^leak10][^leak6].
     - Keeping them would need an amendment of the rule on values recorded after the outcome, which has no exceptions.
   * **Effect on the task:**
     - Respiratory distress has an odds ratio for death of 3.69 in the late forms against 2.30 in routine forms at the same length of stay; race is blank for 25.2% of late discharges against 9.7% of late deaths.
     - The drop removes 97.8% of the deaths on the admission day: the task covers patients notified while in hospital, which fit_reason and the notes now say.
     - The drop also takes 153 of the 787 rows whose free-text cells name intensive care or a death, and all 3 patients admitted dead.
     - 790,430 rows stay at 9.3% deaths; the test windows keep 9,167 to 12,909 deaths; the oldest train side is 50.7% of the rows.
   * **Experiments:**
     - Mediator, LightGBM, mean of the three shipped windows: 0.8829 on all test rows against 0.8782 on routine rows; late and same-day rows score 0.91-0.92.
     - After the drop the kept rows score 0.8782 against 0.8780 on routine rows alone; random forest (0.8709 to 0.8662) and linear (0.8650 to 0.8616) fall alike, and the ranking LightGBM > random forest > linear holds in every window.
     - The drop reads the outcome date, blank for 6.5% of the kept rows (7.2% of the discharges, 0.5% of the deaths): these undated rows show no reverse marker (missing flags add +0.010 on them against +0.043 to +0.051 on the late forms) and do not lift the score, though features recognise them (ROC AUC 0.89-0.92).
   * **Consistency:** follows your blanking of located late cells in zillow_prize, melbourne_housing_market and noaa_storm_events_damage[^noaa] and sinan's drop of late rows on the same portal; framingham[^fram] is set apart by a measured fact: there a row's existence depended on follow-up, here the residue the cut leaves was measured and adds nothing.
   * **Panel:** the critic and the mediator: the traced part shows a gain, so the rows go. The advocate opened for keeping (the cut selects by the outcome; no participant can use the route, since the notification date is not shipped). In the rebuttal he conceded that a note alone breaks the rule and accepted the drop if the rows left without an outcome date showed no reverse marker. The mediator measured them, and they show none, so the panel agrees on A.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Drop the late forms (implemented) | rows with notification on or after the outcome date leave | no answer or blank that follows the outcome; scores equal those on routine rows | 14.4% fewer rows; most admission-day deaths leave; the cut reads the outcome date (residue measured, no gain) |
     | B | Keep them with a note | the rows stay, the gain named in fit_reason | the whole admitted population, admission-day deaths included | +0.005 ROC AUC from forms filled after the outcome; needs an amendment of the rule on late values |

   * **Recommendation:** A. **Decision:** A or B?

   **Notes for the AI:** on B, remove the line `df = df[~(df["DT_NOTIFIC"] >= df["DT_EVOLUCA"])]` in `_clean`, restore the notes bullet "Forms filled after the outcome" with the routine-only score (0.8782) and +0.005, write the amendment of LEAK-10 into the knowledge file, re-run `dataset check` and the leak probes. The mediator's 132,478 was counted on the earlier shipped frame, after the copy drop; the definition now drops the late forms before it, and 34 of the 243 rows that copy drop removed are late forms, so 132,512 is the shipped count.

   [^leak10]: **LEAK-10** (Must; amended 2026-11-08, Lennart, on noaa_storm_events_damage): a feature holds only what existed at the prediction point and never gives the target away; out: a column recorded after the outcome, missingness that encodes the outcome; late values that can be located row by row are blanked or dropped, untraceable ones stay with a note only when the traced part shows no gain.
   [^noaa]: Lennart, 2026-11-08, noaa_storm_events_damage: "the size of the worth alone never decides"; located late cells are blanked.
   [^fram]: Lennart, 2026-10-22, framingham: "dropping selects on the future".
   [^leak6]: **LEAK-6** (Must): measure before acting; a slight optimism with a known cause can stay with a note; a confirmed leak goes even when small.

2. **Name the patients who enter intensive care on the admission day, as now, or also give the model a flag for it?**

   * **Problem:**
     - 20.8% of the shipped patients (38% of the deaths; 20.5% and 37% in the panel's reports, counted before the drop) enter intensive care on the admission day, so for them the referral the use case names is already made[^use3].
     - The definition now names this group and the hospital-acquired SARI (21,213 rows, 2.7%) in the use case and the notes; no rule asks for the flag[^use8].
     - The domain practitioner would add an `icu_on_admission_day` flag, as the team knows where it placed the patient.
   * **Effect on the task:** the flag adds +0.008 pooled ROC AUC (+0.018 among adults; log loss 0.2179 to 0.2121), measured before the drop of issue 1.
   * **Experiments:** before the drop of issue 1, the mediator found nothing that ties the flag to same-day deterioration: 13.6% of the day-0 patients' deaths fall within one day against 16.7% for the others, and the flag is no denser in late forms (18.5% against 21.2%); same-day transfers cannot be excluded, as the data has no time of day.
   * **Panel:** for the flag, the domain practitioner and the critic (known at admission, worth +0.008); against, the advocate (a field from the in-stay section that at day granularity also catches transfers later on the admission day).
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Name the group only (implemented) | use case and notes name the 20.8% and the hospital-acquired SARI | no field from the in-stay section | the model cannot tell a ward patient from an intensive-care one |
     | B | Add the flag with a note | `icu_on_admission_day` from the intensive-care entry date | the team knows the placement; +0.008 ROC AUC | catches same-day transfers that may follow the day's course |
     | C | Keep only ward admissions | drop the day-0 intensive-care rows | the referral question holds for every row | a fifth fewer rows, 38% of the deaths |

   * **Recommendation:** A, the minimum the rule asks; B is a defensible call if the use case is the ward's admissions (the domain practitioner's reading); the critic accepted A as the minimum in the rebuttal. **Decision:** A, B or C?

   **Notes for the AI:** on B, build the flag from `UTI` = 1 and `DT_ENTUTI` equal to `DT_INTERNA` before the drop of `AFTER_ADMISSION`, add it as a categorical with a notes line; on C, filter those rows in `_clean`; re-run `dataset check` and the leak probes.

   [^use3]: **USE-3** (Must): name the prediction point: when the model is used and what is known then.
   [^use8]: **USE-8** (Must): write how closely the data mirrors the use case, its fit (direct or approximate, with the gap named).

3. **Keep race or colour, indigenous ethnicity and the two traditional-community fields as features, as now, or drop them, decided alike with rais_employment_separation_1m?**

   * **Problem:**
     - The fields describe protected grounds in a hospital's risk score, and the rules leave open whether a professional norm on admission decisions counts like a law[^sel1].
     - The decision goes with rais_employment_separation_1m issue 1 and the across-datasets item on protected grounds, so it is not decided here.
     - Either way the data loses nothing: race and the community fields are worth no ROC AUC.
   * **Background:**
     - The norms: brazilian admission scores (ABC2-SPH, 4C) leave race out; Res. CFM 2.156/2016 art. 9 lists colour, but also sex and age, among the grounds an ICU admission decision must not rest on; no statute bars race in a clinical risk score, unlike Lei 9.029 for employers.
   * **Effect on the task:** ROC AUC 0.8819 with them, 0.8817 without (log loss 0.2179 to 0.2180), measured before the drop of issue 1 (domain practitioner, LightGBM); the claim auditor found -0.0007 on one fold.
   * **Consistency:** the clinical precedents keep race (kumc, diabetes_130_us, SUPPORT, sinan from the same portal).
   * **Panel:** Opening briefs: for dropping, the critic and the domain practitioner (SUS equality, the medical code); for keeping, the advocate (the norm governs allocation, not a prognosis). After the rebuttals all three recommend dropping, at no cost, and all agree it is no Must: it is the curator's call with rais, and either way a line in the notes states the reading taken.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep with a note (implemented) | the four fields stay, a line names the reading | follows the clinical precedents; no statute bars them | the actor would not put race into a triage score |
     | B | Drop the four fields | removed from the features | follows the stance taken for rais if extended to professional norms | departs from kumc, diabetes_130_us and sinan |

   * **Recommendation:** decide with rais_employment_separation_1m issue 1; no separate recommendation. **Decision:** A or B?

   **Notes for the AI:** on B, add `CS_RACA`, `CS_ETINIA`, `POV_CT`, `TP_POV_CT` to the dropped fields (and their names from `PERSON`, `OTHER_YES_NO`, `_feature_types`); either way add a notes line with the reading; re-run `dataset check`.

   [^sel1]: **SEL-1** (Must): a task with ethical concerns is out, including data whose subjects or creators ask that it not be used for ML.

4. **Keep the fallback ROC AUC, as now, or score by log loss because bed planning sums the probabilities?**

   * **Problem:**
     - Baqui et al. 2021 report ROC AUC and average precision side by side without naming the one that decides, so the metric is the fallback, `roc_auc`[^met5][^met8].
     - Bed planning sums the probabilities, and models over-predict the deaths of the test windows by about 12% pooled (before the drop; by window +14%, +1% and -2% for LightGBM), which ROC AUC does not see.
     - Log loss would be the first `context` metric for a binary task outside a competition[^met11].
   * **Effect on the task:** on the mean of the three windows both metrics rank LightGBM > random forest > linear, before and after the drop; in one of six window settings they disagree on two close models (2025-H1 after the drop: random forest ahead by ROC AUC, linear by log loss).
   * **Consistency:** the fallback follows gallstone_disease, heart_disease and sinan; a `context` log loss would set a new precedent.
   * **Panel:** for log loss, the critic and the domain practitioner (bed planning, calibration); for ROC AUC, the advocate (no clear case for `context`; the over-prediction is a drift common to all models).
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | ROC AUC, fallback (implemented) | ranks patients by risk; note on calibration and the children-adults mix | the rules' default; follows the precedents | blind to the 12% over-prediction |
     | B | Log loss, origin `context` | scores the probabilities | sees calibration, which bed planning needs | first `context` binary metric outside a competition; reorders close models only rarely |

   * **Recommendation:** A, with the note on calibration and age that the definition now has; B is a defensible call. **Decision:** A or B?

   **Notes for the AI:** on B, set `metric = Metric.from_context("log_loss", reason=...)` naming bed planning, keep the notes line, re-run `dataset check`.

   [^met5]: **MET-5** (Should): a paper's metric is the source's only when it is one deliberate choice; several reported side by side give the fallback.
   [^met8]: **MET-8** (Should): for the same goal prefer the probabilities; the fallback is `roc_auc` for binary tasks.
   [^met11]: **MET-11** (Must): every metric has one origin (source, context or fallback), and the notes name the original when the declared metric is not it.

**Review panel:** ship after changes (mediator). Claim audit: the counts hold; refuted in part the "notified twice" reading (28% of the copy groups are two infants) and the "+0.002" of the late forms (+0.005 measured), both corrected. Column audit: in-stay events in the free texts, a survivor-marking vaccine blank, hospital names shared across municipalities and schooling of children, all fixed. Split audit: the half-year windows, the gap and the end at 2026-06-30 hold. Blind review: would benchmark; main concern the late forms. Task gamer: +0.0026 ROC AUC from all exploits stacked, the largest a person key rebuilt from vaccine dates (closed by the 30-day bins). Debate: agreed on the task, split, target and the cleaning fixes; after the rebuttals the advocate accepted the drop of the late forms (once the undated rows were measured) and the drop of race as a recommendation; the critic accepted that race and the metric are curator calls, not Musts; disputed: the drop of the late forms (issue 1), the intensive-care flag (issue 2), race or colour (issue 3), the metric (issue 4).

<details><summary>Mediator</summary>

MEDIATOR REPORT: sivep_gripe_sari_outcome (folder sivep_gripe_sari_outcome, history from 2023, not _1m), 2026-11-09

Read: principles.md; PANEL_COMMON.md; the reports of the claim auditor, column auditor, split auditor, domain
practitioner, blind reviewer, task gamer and precedent checker; the advocate's and critic's briefs with rebuttals; the
builder's report; dataset.py; Baqui et al. 2021 full text (Europe PMC XML, PMC8329284).
My measurements (scripts and output in the session scratchpad, not in the repository):
  m03_late.py / m03.json: the claim auditor's frame (final_with_helpers.parquet: the definition's _clean output with
  the raw dates, 922,908 rows); the shipped windows rebuilt from admission_date (the train and test counts match the
  kit exactly: 768,238/139,737, 608,548/130,431, 470,290/167,794); LightGBM (300 trees, 63 leaves), logistic
  regression and random forest, before and after the drop; texts left out.

**1. JUDGMENT RECORD**
Verdict: ship after changes.
Validity: SEL-1 holds (no objection by subjects or creators; race or colour is a curator call with rais issue 1, issue
  3); USE-1 holds (direct fit, approximate); USE-3 holds after naming two groups (ICU on the admission day,
  hospital-acquired SARI); USE-5 holds (code 3 counts as death); LEAK-10 triggered four times, all fixed in the
  definition (free texts blanked, the covid_vaccine blank set to "No", the vaccine day counts binned, the forms
  notified on or after the outcome dropped); LEAK-17 and the SPLIT-9 Tensions row triggered by the person key the
  vaccine day counts rebuild, fixed by the bins; LEAK-24 holds (simulated earlier download); SPLIT-1, SPLIT-9,
  SPLIT-10, SPLIT-14 (50.7% after the drop), SPLIT-20/21 hold.
Value: TP clean (LightGBM 0.878-0.883, age alone 0.81; smallest test class after the drop 9,167 deaths). MET-5/MET-8:
  fallback roc_auc holds (Baqui reports AUC-ROC and AP side by side).
Quality: CLEAN-1/12 hospital as "name [municipality code]"; CLEAN-11/14 schooling under 7, impossible values, one name
  per code; CLEAN-12 occupation as "title [CBO code]" kept.
Weighed: size +, source + (national register), use case + (bed planning, monitoring), fit - (form only, no vitals).
For the curator: issue 1 (confirm the drop of the late forms, or amend LEAK-10); issue 2 (ICU-on-admission flag);
  issue 3 (race or colour, with rais issue 1); issue 4 (metric: roc_auc or log_loss `context`).

**2. CHANGES TO MAKE NOW (no decision needed)**
Validity (Must):
 a. Drop the rows notified on or after the outcome date (DT_NOTIFIC >= DT_EVOLUCA): 132,478 rows (14.4%), 25.1% of
    the deaths; 790,430 rows stay at 9.31% deaths. LEAK-10 ("missingness that encodes the outcome", "a column recorded
    after the outcome") with LEAK-6 (a confirmed leak goes even when small); remedy ladder step 2. The decisive
    check (section 4, point 1) found no reverse marker in the undated rows that stay. Rewrite the notes bullet "Forms
    filled after the outcome" and fit_reason with the numbers of section 4. The curator may still keep the rows, but
    only through an amendment of LEAK-10 (issue 1).
 b. Free texts: blank the cells of other_symptoms_text and other_risk_factors_text that name ICU, intubation,
    ventilation, cardiac arrest or death, except arrival phrases ("CHEGA/CHEGOU/ADMITIDO EM/RECEBIDO EM"). Use the
    column auditor's regex (a09_text_instay.py): 808 rows (451 ICU/intubation/ventilation, 357 arrest). Drop the 3
    rows dead on arrival (LEAK-36, USE-7). LEAK-10 (a consequence of the target; second clause: located late cells are
    blanked), LEAK-2 (the dropped ICU and ventilation fields come back through the texts).
    Correct the note's count. The counts measure different things: of the builder's 660 regex hits, 258 name
    intubation or ICU; the other 402 are false hits ("PRESSAO ALTA", "DOR VENTILATORIO DEPENDENTE"). A tight
    ICU/intubation regex finds 437-451 rows (claim auditor 437, precedent checker 443, column auditor 451). Adding
    arrest and death words gives 808-820. The note should give the count the blanking regex removes (808).
 c. covid_vaccine blank with 0 doses -> "No" (922 rows, 914 cures). Do the same for the influenza "Yes" whose dose is
    dated after admission ("No" as of admission). LEAK-10, missingness that encodes the outcome.
 d. Bin days_since_covid_vaccine and days_since_flu_vaccine to 30 days. LEAK-17 and the Tensions row SPLIT-9 ("a
    shortcut is always removed"). The task gamer tested the fix: the honest baseline is unchanged (0.88446 against
    0.88439) and the exploit then adds 0. Correct the notes: the open data has no patient id, but exact vaccine dates
    rebuild one.
 e. Prediction point (USE-3, USE-8): name the 20.5% admitted to ICU on the admission day (37% of the deaths) and the
    hospital-acquired SARI (24,087 rows, 2.6%; 8,656 with onset after admission, whose moment is the recognition of
    the SARI). Narrow the referral wording in use_case and known: for the day-0 ICU rows the referral was already
    made. After the drop (a), recount both groups.
 f. The censoring note (LEAK-24 holds): open rows of 2026-H1 are riskier; counting them moves 8.30% to about 8.6%
    (claim auditor), or +0.05 points (split auditor's simulated download). Name the rising open share in 2026
    (4.2% in January to 7.7% in June). The end stays 2026-06-30.
Quality and notes (Should):
 g. Hospital as "name [hospital municipality IBGE code]" (125-130 names cover several municipalities, 9% of rows).
    CLEAN-1 and CLEAN-12, following the definition's own reasoning for municipalities.
 h. Schooling missing for age < 7 (the dictionary's "not applicable"; 60,797 rows). Make impossible values missing:
    negative ages, "puerperal" for men and children, COVID-19 dose dates before 2021-01-17. Use one name per IBGE
    municipality code. CLEAN-11, CLEAN-14.
 i. Licence: state both readings, the dataset page (cc-by, "Creative Commons Atribuição") and the portal footer
    (CC BY-ND 3.0). Do the same for sinan (EV-4, PROV-10; a note, not an issue).
 j. Metric note (MET-11, MET-8): the pooled ROC AUC mixes children (61% of the test rows, 10% of the deaths) and
    adults (adults only 0.759), and AUC does not see calibration (+12% over-prediction pooled, domain practitioner).
 k. LEAK-25-style note on the 74 units with 50% or more deaths (1.6% of rows, 10.1% of deaths, mostly post-outcome
    forms at UPAs). Recount them after the drop (a), which removes most of these rows.
 l. A `Potential leak, kept on purpose:` note on the counts over the test window (task gamer exploit 2; section 5).
 m. Smaller corrections from the claim auditor: the "notified twice" reading fails for 28% of the copy groups (two
    birth dates; LEAK-18/19); follow-up is 132 days, not 131.

**3. ISSUES FOR THE CURATOR (rank order)**
Issue 1 (P4, LEAK-10 Must; validity). Forms notified on or after the outcome: drop (done in 2a) or keep through an
  amendment of LEAK-10?
  Problem: 14.4% of the rows (7.5% notified after the outcome, 6.8% on its day) hold 25% of the deaths. In these
  forms the respiratory answers and the completeness follow the outcome. Respiratory distress OR 3.69 in late forms
  against 2.30 in routine ones, at the same length of stay. Race is missing for 25.2% of late cures against 9.7% of
  late deaths.
  Effect (m03, mean of 3 windows, LightGBM): shipped 0.8829 on all test rows against 0.8782 on routine rows, an
  inflation of +0.0047. The note says +0.002. Late and same-day rows score 0.91-0.92.
  Advocate's best evidence: every filter reads a post-admission fact. The outcome date is blank for 7.2% of discharges
  and 0.4% of deaths, so the cut selects by the outcome (framingham, 2026-10-22). No participant can exploit the
  route, since the notification date is not shipped.
  Critic's best evidence: LEAK-10's second clause keeps a late value with a note only when the traced part shows no
  gain, and here it shows one (0.91 against 0.87). LEAK-6 drops a confirmed leak even when small. The gain sits in
  the missingness, which can reorder methods.
  Rule: LEAK-10 and LEAK-6 (Must, P4). This is not a conflict with another Must: the selection the advocate names is
  a residue to measure (EV-1), not a rule broken by the drop.
  Decisive check (advocate's condition), results:
   - Undated rows after the drop: 6.5% of the rows, 7.2% of survivors against 0.5% of deaths (before the drop: 6.2%
     against 0.4%). Their death rate is 0.4-0.7% in the test windows.
   - No reverse marker. Missing flags plus age gain over age alone +0.024 on routine rows in every window. On the
     undated rows the gain is -0.016, +0.031 and +0.014 (mean +0.010), against +0.043 to +0.051 on the late forms.
   - The undated rows do not lift the score. After the drop, test AUC on the kept rows is 0.8782 against 0.8780 on
     routine rows alone (LightGBM). Models predict the undated rows at 0.056-0.077 against an observed 0.004-0.007.
   - Residue to note: features recognise the undated rows among the kept ones at ROC AUC 0.89-0.92. The models do
     not exploit this, but a participant could. The rows were in the shipped data already (5.6%).
  What the drop does: the score falls by about 0.005 for every model (LightGBM 0.8829 -> 0.8782, random forest
  0.8709 -> 0.8662, linear 0.8650 -> 0.8616). The ranking stays LightGBM > random forest > linear in every window.
  Training without the late rows leaves routine-row AUC as it was (LightGBM 0.8782 against 0.8780). The drop also
  changes the death population: 97.8% of the deaths on the admission day and 72.5% of those within one day leave
  (admissions with no in-stay decision left). SPLIT-14 still holds (oldest train side 50.7%). The test windows keep
  9,167 to 12,909 deaths.
  Recommendation: drop (2a). Write the death-population change and the undated residue into fit_reason and the
  notes.
  Decision: (a) drop, as recommended; (b) keep, as an amendment of LEAK-10 (a Must has no exceptions), with the
  routine-only score and the corrected numbers in fit_reason.

Issue 2 (P3, USE-3/USE-8 Must for the naming; the flag is a weighing). An icu_on_admission_day flag, or naming only?
  Naming is enough. USE-3 asks the prediction point and what is known then to be named. No rule asks every feature
  known at admission to be shipped, and USE-8 takes a missing input as a fit gap. So the flag is optional (P7/USE-8
  fit), not a Must.
  For the flag (domain practitioner, critic): it is known at admission (the team placed the patient) and worth +0.008
  pooled ROC AUC (+0.018 among adults; log loss 0.2179 -> 0.2121).
  Against (advocate): it adds a field from the in-stay section. At day granularity it also catches transfers later on
  the same day, a same-day value that may depend on that day's course (LEAK-10).
  My check (EV-1): day-0 ICU patients do not die earlier. 13.6% of their deaths fall within one day, against 16.7%
  for the others. The flag is no denser in late forms (18.5% against 21.2% in routine forms). So nothing shows it
  encodes same-day deterioration. Same-day transfers cannot be excluded, because the data has no time of day.
  What would settle it: the curator's view of whether the use case is "all admissions, ICU or not" (no flag) or "the
  ward's admissions" (with the flag, or with the day-0 ICU rows dropped).
  Decision: (a) name the 20.5% only (in 2e; recommended as the minimum); (b) add the flag with a note.

Issue 3 (P1, SEL-1; decide alike with rais_employment_separation_1m issue 1 and the across-datasets item on
  protected grounds). Race or colour, indigenous ethnicity and the two traditional-community fields: drop, or keep
  with a SEL-1 note?
  The rules leave this open. Not decided here; handed on exactly as rais is.
  For dropping (critic, domain practitioner): the fields are worth nothing (ROC AUC 0.8819 -> 0.8817, log loss
  0.2179 -> 0.2180). The actor would not put them in a triage score: SUS equality (Lei 8.080 art. 7 IV), the medical
  code, and Brazilian admission scores (ABC2-SPH, 4C) that leave race out. Res. CFM 2.156/2016 art. 9 lists colour
  among the grounds for ICU admission decisions.
  For keeping (advocate): art. 9 also lists sex and age, so read as a bar on inputs it would remove age (0.812 alone),
  and it governs allocation, not a prognosis. No statute bars race in a clinical risk score (unlike Lei 9.029 for
  rais). Clinical precedents keep it: kumc, diabetes_130_us, SUPPORT, and sinan from the same portal.
  Both sides agree: either way a SEL-1 line in the notes with the reading taken; the dataset ships either way.
  What would settle it: the curator's scope for the rais extension (law only, or also professional norms; access
  decisions only, option d of the precedent checker).

Issue 4 (P6, MET-8/MET-10/MET-11; Should and Weigh). Metric: fallback roc_auc (as shipped) or log_loss with origin
  `context`?
  Settled first: the origin of roc_auc is `fallback`, not `source`. Baqui et al.: "As metrics we consider ... (AUC-ROC)
  and the average precision (AP)". The text compares XGBoost with logistic regression by AUC-ROC and uses AUC-ROC for
  the permutation importance, but it names no criterion it selects by. MET-5 sends two metrics side by side to the
  fallback, and the Tensions row on metrics does the same (gallstone_disease, heart_disease; sinan from the same
  portal).
  For log_loss (critic, domain practitioner): bed planning sums the probabilities. Models over-predict deaths by 12%
  pooled (by window, LightGBM: +14% in 2025-H2, +1% in 2025-H1, -2% in 2026-H1). MET-10 diversity: the binary log-loss
  tasks so far all come from competitions.
  For roc_auc (advocate): MET-11 `context` needs a clear case, and no curator precedent sets `context` log_loss for a
  non-competition binary task. The over-prediction is the same drift for every model.
  The check the advocate asked for (do log_loss and AUC rank the probe models differently?): mostly no. On the mean of
  the 3 windows both rank LightGBM > random forest > linear, before and after the drop. The builder's probes rank
  LightGBM > linear > random forest by both metrics. In one of my six window-settings they disagree: 2025-H1 after
  the drop, random forest 0.8633 against linear 0.8591 by AUC, but 0.2278 against 0.2270 by log loss (random forest
  over-predicts, mean 0.100 against 0.090). Another window is a near tie (2025-H1 shipped, 0.2432 against 0.2433).
  So log loss adds calibration information that can reorder close methods, but no systematic reordering.
  Recommendation: roc_auc fallback with the note 2j (the rules' default when the context is not clear, MET-11);
  log_loss `context` is a defensible weighing call.
  Decision: (a) roc_auc fallback; (b) log_loss, origin `context` ("bed planning sums the probabilities").

Not an issue here (point 5, CLEAN-12): occupation as "title [CBO code]" is lossless (507 codes, 507 titles, one to
  one) and follows CLEAN-12. Both sides and the precedent checker agree. A fact sets it apart from rais and sinan (the
  title is in the rows). The inconsistency belongs in sinan_dengue_case_screening_1m's issue 4 and
  rais_employment_separation_1m's issue 5: name sivep there as the batch's case decoded from the source's own pair.
  Whatever is decided there, sivep stays.

**4. AGREED FACTS**
- The task is real (USE-1, all agents). The history from 2023 rests on the register's break (SPLIT-20/21; aeolus).
  Code 3 counts as death (USE-5; all-cause target, framingham is the contrast). End 2026-06-30 (LEAK-24: in the
  simulated earlier download, 98.0% of the later-closed labels were already known, deaths and discharges alike).
- The split is temporal by admission date, three half-years, a one-month gap. It matches the definition exactly.
  SPLIT-9 holds for training labels (readmission labels after the test admission: 14-41 rows a window). The
  one-month gap costs at most 0.0006 against a real refit.
- Routes (m03): routine 80.05% of rows (9.9% deaths), same day 6.84% (19.5%), late 7.51% (17.8%), no outcome date
  5.60% (0.75%). The late share is stable by year (15.2%, 14.6%, 13.8%, 13.7%).
- Test AUC by route, shipped (LightGBM, my run): routine 0.877-0.883, same day and late 0.90-0.92, undated 0.83-0.86.
- Exploits stacked: +0.0026 AUC (task gamer). The largest single exploit is the person key from the vaccine dates
  (+0.0015). No row-order, copy, id or transform leak.
- Free texts: 808 cells to blank; the texts in all add +0.002. The covid_vaccine blank is a survivor fingerprint
  (922 rows, 914 cures).
- Hospital names: 4,434 names against 4,755 (name, municipality) pairs.
- Licence: the dataset page says cc-by, the portal footer CC BY-ND 3.0.
- The pooled AUC: 0.882 all ages, 0.759 adults; age alone 0.812.

**5. TASK GAMER: EXPLOITS AND FLAWS MAPPED**
The definition has no `Potential leak, kept on purpose:` note and no accepted warning, so every item below is new
unless a plain note covers it.
1. Person rebuild from the exact vaccine day counts, then a later readmission as proof of survival (+0.0015 over the
   strong honest model). LEAK-17 (repeated entities) via a quasi-identifier, removed under the Tensions row SPLIT-9
   ("a shortcut is always removed"). New: the notes say "the open data has no patient id". Fix 2d.
2. Counts over windows that reach into later test days (+0.0008 over the strong model, about 3 SD of the seed noise;
   past-only counts are legitimate). A participant-side transductive use of the test window's feature rows. No label
   is read and every model in a batch test window can do it. Nearest rule: LEAK-30's Tensions row (a weak
   transductive leak is kept with a `Potential leak, kept on purpose:` note). New. Fix 2l (a note with the size; the
   gamer's remedy of shorter test blocks is not worth a re-split, SPLIT-15).
3. Formats and missingness flags (+0.0005, within about 2 SD). LEAK-13 to LEAK-15 and LEAK-39 (recording by class).
   Mostly the meaning of the missingness (no dose, no reported risk factor, infant age units), which the notes name
   (0.66-0.70 alone). The part from post-outcome forms leaves with 2a. Known in part; no issue.
Flaw A (late forms): LEAK-10/LEAK-6. Known: the note covers it as "7.5%, +0.002". The measured gain differs (+0.0047
   over routine rows; 14.4% of rows with the same-day forms). That makes it an issue: issue 1 and fix 2a.
Flaw B (outcome-missing rows dropped): LEAK-24 (Must) and USE-7. Known: the notes give the open 4.7% and ignored 1.8%.
   The measured gain matches the note: an oracle month offset gains +0.0001, and the split auditor's simulated download
   shows +0.05 points. No issue; the censoring note 2f.
Source lookup (AUC 0.9986 from the public file): not a task flaw. Every public dataset allows it.

**6. CONSISTENCY WITH PRECEDENT (precedent checker's report)**
- Late forms dropped: departs from the precedent checker's "consistent" reading of the builder's keep. That reading
  rested on LEAK-39's drop condition, which both sides agree is not the operative rule. Under LEAK-10's second clause
  the drop follows the curator's practice: zillow_prize and melbourne_housing_market blank located late cells
  (Lennart, 2026-10-21); noaa_storm_events_damage blanks them ("the size of the worth alone never decides", Lennart,
  2026-11-08); onlinenewspopularity keeps them only with no traced gain (2026-10-26). It also matches sinan's drop of
  late rows on the same portal.
  framingham (2026-10-22, "dropping selects on the future") is set apart by a measured fact. There a row's existence
  depended on follow-up. Here the residue the cut leaves was measured: undated rows 6.5%, no reverse marker, +0.0002
  on the score.
- Free texts blanked: the precedent checker's option b (zillow_prize, melbourne, noaa_storm). Consistent.
- covid_vaccine "No": the precedent checker's option a (the as-of value). Consistent with LEAK-10's blank precedents,
  whose blanks carry no outcome.
- Vaccine bins: the Tensions row SPLIT-9 and alfa_battle_2_0_task_2, where a link to the row's own entity is removed.
  lt_vehicle_loan is the contrast: shared codes, no entity link.
- Hospital key: the precedent checker's E1 (the definition's own municipality reasoning). Consistent.
- Race: consistent in substance with the clinical precedents (kumc, diabetes_130_us, SUPPORT, sinan). The batch's
  method asks for a SEL-1 line, given in either case. The decision goes with rais issue 1 (enem and acs as companions).
- Metric: fallback, consistent with gallstone_disease, heart_disease and sinan. A `context` log_loss would be the
  first for a non-competition binary task: a new precedent the curator should record.
- Occupation: consistent with CLEAN-12. sivep is not a third exception for the CBO amendment watch.
- No drift: no curator decision on any SIVEP or SINAN call exists yet.

</details>

<details><summary>Claim audit</summary>

CLAIM AUDITOR: sivep_gripe_sari_outcome (2026-11-09)

Verdict: ship after changes. 26 claims hold, 6 are refuted in part, 3 are untested. Nothing refuted here retires
the dataset. One P1 call goes to the curator, and there is one small LEAK-10 fix (Must).
  P1 / Tensions row "factor the actor may no longer use": the builder found "no objection" to race or colour, but there
     is one. Resolução CFM 2.156/2016, art. 9, says decisions on ICU admission and discharge are made "sem
     discriminação por questões de religião, etnia, sexo, nacionalidade, cor, orientação sexual, idade, condição
     social...". Our use case names "early referral to intensive care". This is a call for the curator, because the
     rais extension is not confirmed yet.
  LEAK-10 (Must): 9 free-text cells describe this stay or its outcome (8 of the 9 are deaths). The note's "660 texts
     name intubation or ICU" is a miscount: only 258 of the 660 do.
  USE-3: for hospital-acquired SARI (24,087 rows, 2.6%), the form describes an illness that began after admission.
  USE-8 / LEAK-39: the 7.5% of late forms is a lower bound. Another 6.8% were notified on the day of the outcome.
Validity: SEL-1 open (curator); USE-5 holds (code 3 counts as death); LEAK-10 triggered (9 cells); LEAK-24 holds with a
small residual; SPLIT-1 holds; PROV-1 and PROV-9 hold. Value: MET-5 and MET-8 fallback holds; every fold scores.
Quality: CLEAN-12 is inconsistent across the batch; LEAK-13 is weak for occupation.

Scripts, logs and the cached frame: a01-a10 *.py/*.log, final_with_helpers.parquet, open_risk.parquet (in the panel's run folder, not in the repository).
Data: the prepared raw sivep_srag_2023_2026.parquet, run through the definition's own _clean (922,908 rows, matching).
Source checks: Baqui et al. full text (Europe PMC XML of PMC8329284); the portal page (__NEXT_DATA__); dictionary.txt;
CFM 2.156/2016 art. 9 (normasbrasil.com.br and portal.cfm.org.br); Lei 8.080/1990 art. 7 IV.

**TABLE  (claim | source | test | result | evidence | rule)**
1  Source = Ministry's SRAG dataset on Portal de Dados Abertos do SUS | source_url, bibtex | fetched the portal page |
   HOLDS | title "Banco de dados da Síndrome Respiratória Aguda Grave (SRAG) - 2019 a 2026" | PROV-1
2  Licence "CC BY ... version not stated" | license | portal __NEXT_DATA__ | HOLDS | license_id cc-by, license_title
   "Creative Commons Atribuição", license_url opendefinition cc-by | PROV-10
3  Year 2026 = the snapshot year | year | metadata | HOLDS | metadata_created 2022-01-11; files of 2026-11-09 | PROV-9
4  2019-2024 frozen, 2025-26 live under new names | download_description | portal file list today | HOLDS | the page
   lists INFLUD25-09-11-2026 and INFLUD26-09-11-2026 | PROV-8
5  All eight yearly files have 194 columns | notes | read the 5 local files | HOLDS for 5 of 8; 2019-2021 UNTESTED
   (remote) | prepared file: 195 = 194 + source_file | -
6  The actor is the hospital team; the per-patient framing is ours | notes | read Baqui | HOLDS | Baqui: "policy making
   ... hospital management and healthcare network organization", group risk "in an equitable way" | USE-1
7  Baqui: AUC-ROC and AP, plus sensitivity at fixed specificity | metric reason | full text | HOLDS | "As metrics we
   consider ... (AUC-ROC) and the average precision (AP)"; "at 80% of specificity ... sensitivity of 64.7%" as an
   illustration; random 80/20 split; outcome death vs recovery | MET-5
8  Fit approximate: "7.5% of forms were filled after the patient left" | fit_reason | outcome date vs notification
   date on the final cohort | REFUTED IN PART (the count is a lower bound) | outcome before notification 69,311 (7.5%,
   mortality 17.8%); outcome on the notification day another 63,167 (6.8%, mortality 19.5%); together 14.4% of
   rows and 26.9% of code-2 deaths. 16.4% of forms were notified after ICU entry (14.4% of discharges, 32.7% of
   deaths); 34.4% were typed after the outcome | USE-8, LEAK-39
9  Notification follows admission by a median 1 day (p90 5) | notes | recomputed on the cohort | HOLDS | median 1,
   p90 5, 1.6% notified before admission | -
10 History numbers (2019 48,941; 2020-21 1.2M-1.7M; 3.5M of 4.6M since 2020 are 2020-22) | notes | small_cols file

   | HOLDS | 48,941 / 1,206,920 / 1,745,672; 3,505,318 of 4,641,761. Death rate by admission year 2023-2026: 12.4%,

   11.1%, 9.9%, 8.1% | SPLIT-20
11 INFLUD22-26 only; 2,713 admissions of 2023 are in INFLUD22 | notes | by-file count | HOLDS | 2,713; no cohort row
   has onset before 2022, so no row sits in an undownloaded file | -
12 Cohort counts: 987,345 / 19,781 / 25,421 / 13,670; open 46,012; ignored 18,165 | notes | polars on the prepared
   raw | HOLDS | exact: 987,345; open 46,012; ignored 18,165; HOSPITAL 2 19,781; null 23,712 + 9 1,709 = 25,421;
   13,670 without an admission date. Side facts: the 13,670 die more often (13.2% vs 10.6% of closed), and so do the
   23,712 blank flags (12.4%, 47% marked ICU, only 4 with an admission date), so dropping them is a mild selection.
   Per-quarter open/ignored ranges not recomputed | USE-7
13 17 record numbers in a frozen and "the next live" file; 241 rows notified twice; one conflicting pair; 922,908 | notes |
   rebuilt the pre-dedup frame (patched drop_duplicates) and joined the raw birth dates | 17 and 922,908 HOLD;
   "one case notified twice" REFUTED IN PART | all 17 duplicates are paired with INFLUD25 (15 from INFLUD24, 1 from
   INFLUD22, 1 from INFLUD23), so "next" is loose; 5 of the 17 differ in admission date. Of the 240 copy groups (239
   pairs and 1 triple), 27.9% hold two different birth dates (different patients: same coarse profile, same day, same
   children's hospital) and 37% two outcome dates | LEAK-18, LEAK-19
14 Target counts 824,981 / 71,037 / 27,150; 10.6%; 8.3-12.7% by half-year; code 3 is 28% of deaths | notes | recount |
   HOLDS | exact; 27.65%; by half-year 8.30%-12.71% | USE-5
15 LEAK-24: end at 2026-06-30, closing equal by class from 90 days; 131 days; open Jul 8%, Sep 17%, Oct 38% | notes |
   LightGBM trained on rows closed by Nov 2024 (AUC 0.874 on 2025-26), used to predict the rows still OPEN, by month

   | HOLDS APPROXIMATELY, with a measured residual | open rows are riskier in every window: predicted 12.6% vs 10.1% for

   the closed rows in 2026H1 (6.6% open); 13.6% vs 10.7% in 2025H1 (3.2% still open after 16 months). Counting the open
   rows at their predicted risk moves 2026H1 from 8.30% to about 8.6% and 2025H1 from 10.28% to 10.38%; June 2026 from
   7.12% to 7.53%, June 2025 from 10.22% to 10.34%. The falling death rate is mostly real: the model over-predicts the
   CLOSED rows by 4%, 18% and 22% in 2025H1, 2025H2 and 2026H1, and admissions of Jul-Sep 2026 run at 7.8-8.1%. The
   s07 closing curve can only see rows that eventually close. Follow-up is 132 days, not 131. Open 8.3% / 16.6% / 37.8%
   holds | LEAK-24
16 7.5% late forms (7.4% / 13.6% / 10.0%); recognised at 0.81; routine 0.8731 vs 0.8732; 7.2% of discharges without an
   outcome date | notes | recomputed shares; recording compared by route and class | numbers HOLD (7.4% is among dated
   discharges); "their inputs describe the admission" HOLDS for symptoms, REFUTED IN PART for missingness | the Yes
   shares of symptoms are alike by route (o2 < 95%: 0.62/0.80 before, 0.62/0.82 after). Race missingness depends on
   the class far more in late forms: 25.2% of late discharges vs 9.7% of late deaths (routine 9.0% vs 6.1%); as a
   death predictor, race-missing has AUC 0.577 in late forms vs 0.513 in routine ones, and schooling-missing 0.591 vs
   0.559. In the final cohort, 6.2% of discharges lack an outcome date (7.2% is over all notifications) | LEAK-13,
   LEAK-39
17 Dropped as filled during the stay (antivirals 29% / 42% after admission, ICU, ventilation, imaging, tests,
   classification, closing, genomics) | AFTER_ADMISSION | checked the final columns and s06 | HOLDS | none of the
   AFTER_ADMISSION columns survives; antivirals start after the admission day for 29.3% / 41.9% / 48.0% (codes 1/2/3).
   Conservative: 64% of discharges started on the admission day, which is known at admission | LEAK-10
18 System fields: smoking empty, travel constant or empty, children's doses 1%-2% | SYSTEM | fill rates | HOLDS (dose
   share 0.3%-1.4%) | TABAG 0 filled; HISTO_VGM constant "0"; DT_1_DOSE 1.36%, DT_2_DOSE 0.78%, DT_VAC_MAE 0.26%;
   FATOR_RISC blank exactly when every factor is blank (1.0 / 0.0) | -
19 COVID doses from the register for 96%; only doses on or before admission count | notes | FNT_IN_COV; dose dates vs
   admission by class | HOLDS | FNT_IN_COV = 2 for 96.5% of rows. A dose after admission (now removed) was on 0.23% of
   discharges vs 0.04% of deaths. 29 rows have a dose ON the admission day, all discharges, and are counted
   (negligible) | LEAK-10
20 Flu dose after admission: 5,519 / 77 / 20 blanked | notes | recount | HOLDS | 5,518 / 77 / 20 after the dedup; flu
   dose on the admission day 0.013% vs 0.015% by class | LEAK-10
21 Built age_years, days_onset_to_admission, vaccine counts | code | read | HOLDS | - | -
22 Decodings; schooling ordinal; pregnancy 0 and 9 missing | code | read | HOLDS | - | CLEAN-12, CLEAN-14
23 Municipalities "name [IBGE]", occupation "title [CBO]", hospital 4,434 levels, 3.8% blank, occupation 0.5% filled |
   notes | recount; compared with the sibling definitions | numbers HOLD; occupation recording class-dependent; BATCH
   INCONSISTENCY | 4,434 levels; 3.84% blank; 0.48% filled. Occupation is filled for 2.4x the odds in deaths (MH OR
   within hospital x age band; 2.6 among ICU patients; 2.2 in forms notified before the outcome); mortality is 37.6%
   when it is filled. sinan_dengue_case_screening_1m keeps CBO codes (and municipalities, health regions) as codes;
   rais_employment_separation_1m keeps CBO as codes; both mark it "open for the curator". This one decodes, as CLEAN-12
   asks | CLEAN-12, LEAK-13
24 A blank risk factor mostly means none reported (65%-70% blank) | notes | fill rates | HOLDS | 65.3%-69.7% blank | -
25 Free texts: "425 symptom texts and 235 risk-factor texts name intubation or ICU ... some on arrival, some during an
   earlier stay" | notes | re-ran the builder's regex and a tight intubation/ICU regex | REFUTED | the builder's
   regex also matches ALTA, VENTILA, OBITO and EVOLUIU, so 402 of its 660 hits are e.g. "DOR VENTILATORIO
   DEPENDENTE" (48), "PRESSAO ALTA" (27); only 258 hold intubation/ICU words. A tight regex finds 437 rows (266 + 174,
   0.05%), mortality 40% (57% in symptom texts). 9 cells describe THIS stay or the outcome: "ADMITIDO OBITO", "ADMITIDO
   EM OBITO", "OBITO TRAZIDO PELO SAMU", "PROTOCOLO (DE) MORTE ENCEFALICA" x2, "MORTE CEREBRAL", "EVOLUIU PARA IOT",
   "3 PCR DURANTE INTERNACAO" (all deaths), "BVA QUE EVOLUIU PARA IOT" (a discharge) | LEAK-10 (Must), LEAK-36
26 Windows 139,737 / 130,431 / 167,794; deaths 8.3/9.4/10.3%; train 768,238 / 608,548 / 470,290 | splits_comment |
   recount from dates and the container | HOLDS | exact; train shares 83.2% / 65.9% / 51.0% | SPLIT-14
27 Gap 1 month: 0.9%-1.9% of each train side open at the window start, "alike by class" | splits_comment |
   accounting.json | HOLDS in aggregate; NOT alike in the last train month | aggregate 0.86% vs 0.98% (newest).
   Closed after the window start, by class, in the last train month: 12.8% vs 19.2% (2026), 13.8% vs 17.5% (2025-07),
   13.9% vs 19.6% (2025-01) | SPLIT-9, SPLIT-10
28 Closed a median 11 days after notification, 90% within 55 | splits_comment | recount | HOLDS | 11 / 56 | -
29 First half-years have 18%-45% more admissions (2023-25) | splits_comment | recount | HOLDS | +45.3%, +18.4%, +28.6% | -
30 COVID 18%-22% in Jan-Feb 2025, under 9% from March 2025 | splits_comment | s07 table | HOLDS | 22.4%, 17.5%; then
   1.0%-8.8% | -
31 Metric: fallback roc_auc (MET-5, MET-8) | metric | Baqui full text; scorer on every fold | HOLDS | Baqui uses two
   metrics (AUC-ROC and AP), so no single criterion; the portal and dictionary define none (looked again: the
   dictionary has no evaluation section). The scorer runs on all 3 folds; a dummy scores 0.5; positives 11,594 /
   12,253 / 17,244; no scoring columns are needed. Meaning (MET-2): same target (death vs recovery), but Baqui's
   cohort was PCR-confirmed COVID in 2020 with about 29% deaths, against all SARI in 2023-26 at 10.6%; AUC is
   insensitive to that | MET-1, MET-2, MET-5, MET-8
32 Task probes (LightGBM 0.878 ...) | probes | one LightGBM fit on fold 0 (400k training sample) | CONSISTENT, NOT
   RE-RUN | scorer 0.8818 on fold 0 | TP
33 Leak probes | probes | taken as reported | UNTESTED beyond #25 and #16 | - | -
34 Hospitals of 94% of test rows were seen in training | probes | taken as reported | UNTESTED (consistent with the use
   case) | - | SPLIT-13
35 Heavy checks after the dedup: 0 findings | probes | file read | HOLDS as reported | - | -

Implied claims (not written down):
I1 "Prediction point: admission, before anything the stay brings" (notes, first bullet) | the dictionary's field 32 is
   NOSOCOMIAL, "Caso de SRAG com infecção adquirida após internação", which lets the onset date fall after the
   admission date | REFUTED for 2.6% of rows | hospital_acquired = Yes on 24,087 rows (mortality 22.7%); 8,656 rows
   have their onset after the admission date (7,671 three or more days after; mortality 24.4%). Their symptoms,
   hospital_acquired and the negative onset lag describe the stay, not the admission | USE-3, LEAK-10
I2 "Death from other causes is a death in hospital" (issue 2) | code 3 vs code 2 timing | HOLDS | days from admission
   to outcome: median 8 (code 2) vs 9 (code 3), p90 30 vs 37, more than 60 days 2.1% vs 3.9%; ICU 54.3% vs 54.6%.
   LEAK-22's competing-event clause covers cause-specific targets; the target here is all-cause death. The split
   drifts: code-3 share of deaths 24.9% (2023H1) to 34.0% (2026H1), and code 2 alone falls from 9.4% to 5.6% while
   both together fall from 12.2% to 8.3%. A code-2-only target would therefore drift more | USE-5, LEAK-22
I3 "No row is a copy across the split" | same birth date, sex, residence and admission date among adults (raw DT_NASC)

   | HOLDS across the split; double notifications remain WITHIN a side | 987 adult groups (1,984 rows) share all four:

   78% at the same hospital, 10.4% disagree on the outcome (probably transfers or a second form). They share an
   admission date, so they never cross the 1-month gap. "The open data has no patient id" is loose: DT_NASC is in the
   raw and could key the dedup | LEAK-18, LEAK-20
I4 "Race or colour is a lawful input; no objection found" (builder checklist P1) | Brazilian norms on the decision the
   use case names | REFUTED (an objection exists) | CFM Res. 2.156/2016 art. 9: ICU admission and discharge "sem
   discriminação por questões de religião, etnia, sexo, nacionalidade, cor, orientação sexual, idade, condição
   social, opinião política, deficiência"; Lei 8.080/1990 art. 7 IV "igualdade da assistência à saúde, sem
   preconceitos ou privilégios de qualquer espécie". No statute bars race in a prognostic estimate as such, and LGPD
   art. 11 II f allows health processing of sensitive data. Cost on fold 0 (one seed, 400k training rows): all 0.8818;
   without race, ethnicity and traditional community 0.8811 (-0.0007); also without sex 0.8815; without the full rais
   set (race, ethnicity, sex, age, foreigner, country) 0.8622 (-0.020, nearly all age) | SEL-1, USE-6, Tensions row
I5 "The open and ignored outcomes leave without bias" | predicted risk of the 'ignored' rows | HOLDS for the split
   (stable share), mild selection | the 'ignored' rows are predicted at 11-20% vs 9-15% for closed rows of the same
   month; their share is stable at about 1.8% | USE-7

**REFUTED AND UNTESTED, RANKED (principles.md: P1 first, Must first)**
1. P1 (SEL-1) and the Tensions row "a factor the actor may no longer use", in its rais_employment_separation extension
   ("any decision on a person where the actor's own law bars the factor", an amendment the curator has not confirmed
   yet). CFM 2.156/2016 art. 9 bars colour, ethnicity, sex, nationality, age and social condition in ICU admission
   and discharge decisions, and our use case names "early referral to intensive care and beds". So the builder's "no
   objection found" (P1 row) is wrong. If the extension is confirmed, race_colour and indigenous_ethnicity (and
   traditional_community(_type)?) leave, and sex, foreigner/residence_country and age become candidates. Age is the
   core prognostic factor (alone 0.812), and art. 9 bars discrimination, not prognosis; that is the curator's line
   to draw. Consistency: rais dropped all five grounds; sinan_dengue_case_screening_1m keeps race; Baqui used
   ethnicity to find inequity at group level.
   Mildest remedies, in order: (a) narrow the use case to monitoring and bed planning (no ICU allocation) and keep the
   features with a note; (b) drop race_colour, indigenous_ethnicity and the traditional-community fields (cost 0.0007
   AUC) and keep age and sex as physiological prognosis, recorded as an exception to the extension; (c) apply the full
   rais set (cost 0.020). This is a curator call; nothing changes without it.
2. P4 LEAK-10 (Must): 9 located free-text cells name this stay's events or its outcome ("ADMITIDO EM OBITO", "PROTOCOLO
   DE MORTE ENCEFALICA", "MORTE CEREBRAL", "OBITO TRAZIDO PELO SAMU", "EVOLUIU PARA IOT", "3 PCR DURANTE INTERNACAO";
   8 of 9 deaths). Remedy: blank those cells, as LEAK-10 says for located late cells, with a short regex such as
   MORTE ENCEF|MORTE CEREBRAL|ADMITID. (EM )?OBITO|OBITO TRAZIDO|EVOLUIU (PARA|COM) (IOT|VM)|DURANTE (A )?INTERNA.
   Rows of patients dead on arrival have no prediction point (LEAK-36, USE-7). Also correct the count in the notes:
   258 of the builder's 660 hits name intubation or ICU; with a tight regex, 437 rows, 40% of whom die.
   The effect on the score is negligible, but a Must holds whatever its size.
3. P3/P4 USE-3 (prediction point): for hospital-acquired SARI (24,087 rows, 2.6%; 8,656 with onset after the admission
   date) the form describes an illness that began during the stay. Mildest remedy: say so in the prediction-point
   bullet and in "known" (the prediction point is admission, or the in-hospital onset for a hospital-acquired SARI).
   Stronger option: drop the rows whose onset follows admission by 2 or more days (8,168; mortality 24.7%).
4. P3/P4 USE-8 fit and LEAK-39/LEAK-13 (issue 3): the late-form share is understated, and so is their class-dependent
   missingness. Beyond the 7.5% notified after the outcome, 6.8% were notified on its day (mortality 19.5%), and 16.4%
   after ICU entry (32.7% of deaths). Race missingness in late forms is 25.2% for discharges vs 9.7% for deaths
   (race-missing AUC 0.577 vs 0.513 in routine forms). The builder's measured gain stays small: +0.002 overall,
   none on routine rows. Remedy: keep (issue 3 stands) and correct fit_reason and the note to "7.5% after the outcome,
   6.8% more on its day", naming the race and schooling missingness.
5. P4 LEAK-24 (Must): holds approximately. The open rows are riskier than the closed ones in every window, and counting
   them at predicted risk adds about 0.3 percentage points to 2026H1 against 0.1 to 2025H1 (June 2026 +0.4). The trend
   itself is real. Remedy: a note with these numbers; no cut needed (May 2026 is as open as June).
6. P4 SPLIT-10 (Should): "alike by class" holds for each train side as a whole, not for its last month (12.8% vs 19.2%
   closed after the window start, newest window). Remedy: say so in the gap paragraph. A 2-month gap would shrink it,
   at a cost to the training floor; not needed at 1% of training labels.
7. P4/P7 LEAK-13 (weak) and CLEAN-12 (batch consistency): occupation is filled for 2.4x the odds in deaths within
   hospital and age band (0.48% filled, mortality 37.6%). Remedy: drop occupation. Alone it scores AUC 0.507,
   so dropping it costs little and also ends this dataset's part in the CBO inconsistency. Otherwise settle once for the batch
   whether CBO (and municipalities) ship as "words [code]" (sivep) or as codes (sinan_dengue, rais); CLEAN-12 favours
   words.
8. P5/LEAK-18-19 (Should): "241 rows ... so one case was notified twice" is wrong for at least 28% of the copy groups,
   which have two birth dates (different infants with one coarse profile). Remedy: drop a copy only when the raw
   DT_NASC also matches (read before the drop). This affects about 67 rows; otherwise correct the note.
9. Minor wording: 132 days of follow-up, not 131. 6.2% of discharges in the cohort lack an outcome date (7.2% is over
   all notifications). The record-number copies are paired with INFLUD25, not "the next" file. The children's
   influenza doses are 0.3%-1.4% filled, not 1%-2%.
Untested: claim 5 for the 2019-2021 schemas (remote, not re-read); the per-quarter open and ignored ranges in claim 12;
the probe outputs in claims 32-34 beyond one fold-0 fit (0.882, consistent). The Ministry's 2024 surveillance guide is
not read, as the builder also noted.

Focus questions, answered in short:
- Admission as the time column: right. Late forms add no feature a form at admission lacks, except (i) class-dependent
  missingness (race, schooling) and (ii) 9 text cells that name the outcome. Rows: hospital-acquired SARI rows begin
  after admission (I1). The admission-time cohort does not select by the outcome; a notification-time cohort would.
- In-stay fields: all dropped (17 holds). Antivirals started on the admission day (64% of discharges) could have
  stayed; dropping them is conservative.
- Vaccination rule: holds. Post-admission doses are removed (0.23% vs 0.04% by class); 29 same-day doses are kept.
- Cohort counts: exact.
- End and gap: hold, with the residuals in items 5 and 6.
- Death from other causes: counting it as death holds (I2).
- Copies across files: 17 hold. The "notified twice" reading is wrong for 28% of the groups (item 8).
- The 660 free texts: miscounted; 9 cells leak (item 2).
- Race and CBO: items 1 and 7.
- Protected grounds: CFM 2.156/2016 art. 9 bars them for the ICU decision the use case names (item 1).

</details>

<details><summary>Column audit</summary>

COLUMN AUDITOR REPORT: sivep_gripe_sari_outcome (folder datasets/_dev/tabarena-v0pt2/sivep_gripe_sari_outcome)
Panel role: column-auditor. Date 2026-11-09. Read-only; scripts and logs in panel/.

Verdict: ship after changes, with three calls for the curator.
Validity: SEL-1: no objection found; race or colour, ethnicity and sex add nothing (question 1). USE-3: hospital-acquired SARI
  has no "admission with SARI" moment (question 2, small). LEAK-10 triggered four times:
  (A) the forms notified on or after the outcome day (14.4% of rows, 25% of deaths) carry the outcome in their symptom
  answers and completeness, and the hospital field records units that notify mostly deaths. This makes the builder's
  issue 3 stronger and corrects its numbers. Curator call.
  (B) free texts name in-stay events and the death (808 rows). Must; cheap fix.
  (C) a blanked "covid_vaccine" marks survivors (922 rows). Must; cheap fix.
  (D) the blanked flu answer: diluted, no measurable gap. Optional.
  LEAK-37/LEAK-41: onset-to-admission is the only span; nothing ends at the outcome (holds).
Value: no finding (TP).
Quality: CLEAN-12/CLEAN-3: 125 hospital names stand for several hospitals (9.3% of rows). CLEAN-12/CLEAN-14: "no schooling"
  is 80% children under 7, the dictionary's "not applicable". CLEAN-11: a few impossible values (negative ages,
  postpartum men, COVID-19 doses dated before the vaccine). CLEAN-14: municipality spellings split 4 to 18 codes.
  CLEAN-12 across datasets: rais and sinan ship CBO codes as codes, this dataset ships words (question 3).
Weighed: none.

Prediction point read: the admission date (DT_INTERNA, field 49). Features come from the form's identification,
residence, clinical (fields 32-35) and vaccination (36-41) sections and from the hospital fields 50-52. Every column
was checked against the dictionary of 25/05/2023 (run folder dictionary.txt; PDF in the warehouse folder).

**1. PROBLEMS, RANKED (principles.md: rank, then strength, then effect size)**

Q1 (P1, SEL-1, question for the curator): protected grounds kept as inputs: race_colour, indigenous_ethnicity,
   traditional_community(_type), sex, age.
   Evidence (a08_sel1.log; LightGBM; train admissions before 2025, test 2025-2026; texts left out):
   all 0.8745, without race or colour, ethnicity and community 0.8743, without race_colour alone 0.8745, without
   sex 0.8744. Within an age band, black and brown patients die more often than white ones (60-80 y: 29.3% and 27.7%
   against 24.9%). This is the disparity Baqui et al. study, and a model that ranks beds and ICU referral would
   learn it. The batch's siblings each carry a SEL-1 note: rais_employment_separation_1m drops these grounds under
   Brazilian employment law; enem keeps race (quota law); the NCHS infant mortality task keeps it with "the curator
   decides".
   Mildest remedy: a SEL-1 note in the notes stating the decision and these numbers. Dropping race or colour and
   ethnicity costs nothing measurable. Age stays: it is the clinical core, 0.812 alone. The builder's checklist
   says only "no objection found".

Q2 (P3, USE-3, question, small): hospital_acquired = Yes (24,087 rows, 2.6%, 22.7% deaths). The SARI started during
   another stay: onset after the admission date in 8,656 rows, the only negative days_onset_to_admission values.
   These rows have no "admission with SARI" moment. Their moment is the recognition of the SARI during the stay,
   when hospital_acquired and the negative span are known. Mildest remedy: one sentence in the prediction-point
   bullet saying so (keep the rows). The alternative is to drop them under USE-7. Nothing leaks either way.

A (P4, LEAK-10 with LEAK-39's reading, Must when confirmed; moderate; strengthens builder issue 3, curator call):
   forms filled on or after the outcome carry the outcome. The builder counts only forms notified after the outcome
   date (7.5%) and says "their inputs describe the admission". It counts forms notified on the outcome day as
   routine. Measured here (a02_raw.log, a03_raw2.log, a05_routes.json):
   - Shares: routine 80.1% of rows (9.9% deaths); same day 6.9% (19.5% deaths); late 7.5% (17.8%); no outcome
     date 5.6% (0.75%). Same day and late together: 14.4% of rows and 25% of all deaths.
   - Test AUC by route (LightGBM, train before 2025, test 2025-2026, the builder's set-up): all 0.8757, routine
     0.8692, same day 0.9130, late 0.9104. The forms filled on or after the outcome raise the overall score by up to
     +0.006, against the builder's +0.002. Part of that can be case mix.
   - Mechanism, controlled for age (Mantel-Haenszel odds ratio, death against cure, within the same length of stay):
       respiratory distress "Yes": routine 2.30 / 1.70 / 1.38 for stays of 2-7 / 8-30 / 31+ days;
         late 3.69 / 3.09 / 2.38; same day 3.65 / 3.21 / 2.71.
       dyspnoea "Yes": routine 2.10 / 1.47 / 1.26; late 2.74 / 2.44 / 2.24.
       O2 saturation < 95% "Yes": routine 2.31 / 1.56 / 1.31; same day 3.45 / 2.98 / 2.92.
       fever "Yes" (no sign of decline): 0.6-1.1 in every route, with no pattern.
       risk-factor flag filled: routine 1.63 / 1.50 / 1.45; late 1.77 / 1.33 / 1.69 (about the same).
     In forms written after the outcome, the respiratory answers describe the course of the stay, not only the
     admission.
   - Completeness depends on the outcome in those forms. Race missing: late cures 25.2% against late deaths 9.7%
     (age-adjusted OR 0.25; routine 0.63). Adult schooling missing: OR 0.49 late against 0.91 routine. Dyspnoea
     missing: 0.41 against 0.69. A model on the missing-value flags plus age beats age alone by +0.024 on routine
     rows, +0.031 on same-day rows and +0.054 on late rows.
   - No outcome-free cut separates the route. Dropping rows notified more than 7 days after admission removes 57%
     of the late forms, 6% of the same-day forms and 2.8% of the routine ones (test AUC 0.874), so it does not
     resolve the problem.
   Options for the curator:
     (a) keep, with the note corrected: the routine-only score is 0.869; the same-day forms belong to the route; the
         symptom answers and completeness of these forms depend on the outcome. Fit stays approximate. Today's note
         sentence "Their inputs describe the admission" is contradicted by the data.
     (b) drop the forms notified on or after the outcome date (14.4% of rows, a quarter of the deaths). This reads
         the outcome date, which 7.2% of cures lack, so a residue of post-outcome cures stays. It also removes many
         early deaths, which changes the task's death population.
   I lean to (a) with the corrected numbers. The rows are real admissions; the problem cannot be located without
   the outcome date; the measured lift is under 0.01. But the call is the curator's (LEAK-6: a confirmed leak goes
   even when small).

A2 (P4, LEAK-25 / LEAK-34, maybe a leak, weak to moderate; part of A): units that notify mostly deaths
   (a10_hosp.log). 74 hospitals (name plus municipality) with 30 or more rows have 50% or more deaths: 14,682 rows
   (1.6%), 9,884 deaths (10.1% of all deaths), 4,932 test rows. Eight have 90% or more (952 rows, 913 deaths). Some
   are emergency units with no ICU whose forms are mostly written after the death: UPA José Santos Sasso and UPA
   Vicente Missiano (Osasco; 100% and 94% post-outcome forms), PS Mun Santana (São Paulo; 97% deaths, 98%
   post-outcome), US 111 Recife (91% deaths, 86% post-outcome), Hospital Municipal Antonio Giglio (Osasco; 1,889
   rows, 79% deaths, 57% post-outcome). In Petrópolis, four units have 91-98% deaths. In these units, survivors are
   presumably notified elsewhere or not at all (a patient transferred alive is notified by the receiving hospital;
   an inference, not tested). So the
   `hospital` level partly records where the patient ended up or died, not the case mix at admission. The builder
   reads the hospital as LEAK-34 (case mix and care, known at admission). That is true for referral hospitals
   (Ronaldo Gazolla, Clementino Fraga, Natan Portella: ICU 88-90%), not for these units.
   Measured cost of the hospital: hospital alone 0.727; without it 0.867 against 0.870 (builder's leak probes).
   Mildest remedy (LEAK-25 as amended for noaa_storm): keep, with a note that gives the units' spread (the numbers
   above), names the mechanism and keeps the fit approximate.

B (P4, LEAK-10 and LEAK-2, Must, confirmed, tiny; cheap fix): the free texts hold in-stay events and the outcome
   (a04_clean.log, a06_texts.log, a09_text_instay.log).
   - 451 rows name intubation, ventilation or ICU (IOT/TOT/VM/UTI/CTI): 40.1% deaths against 10.6%.
   - 357 rows name a cardiac arrest ("PCR", "parada"): 50.4% deaths.
   - 24 rows hold clear in-stay or outcome phrases, 18 of them deaths: "PROTOCOLO DE MORTE ENCEFALICA" (twice),
     "MORTE CEREBRAL", "COLETA POS OBITO", "UTI DE 20/06 A 13/08", "INTERNADO NA UTI DESDE 27/03", "EVOLUIU PARA
     IOT", "NECESSITOU DE VNI E IOT", "PIORA DOS PARAMETROS DA VM", "IOT POS PCR".
   - 3 rows say the patient was dead on arrival ("ADMITIDO EM OBITO", "OBITO TRAZIDO PELO SAMU"): no task rows
     (LEAK-36, USE-7).
   The notes say these texts are "some on arrival, some during an earlier stay". Some are during this stay, and a
   few name the death itself. The structured ICU and ventilation fields are dropped under LEAK-10, and the texts
   carry them back in (LEAK-2: drop every carrier of a dropped field). Only part of the cells can be timed, and
   that part shows the outcome. So, by LEAK-10's late-pull clause, the untimed rest goes too.
   Mildest remedy: blank the text cells that name ICU, intubation, ventilation, cardiac arrest or death. That is 808
   rows, 0.088% (regex in a09_text_instay.py). Drop the 3 rows dead on arrival. The texts as a whole add only
   +0.002, so the cost is nil.

C (P4, LEAK-10 "missingness that encodes the outcome", Must, tiny; cheap fix): the blanked "vaccinated" answer marks
   survivors (a04_clean.log). The cleaning blanks covid_vaccine where every dated dose is after admission (only a
   survivor can get one). It leaves covid_vaccine_doses at 0. The pair "covid_vaccine missing and doses known"
   occurs in 922 rows: 914 cures and 8 deaths (0.87% against 10.6%). 709 of them are infants up to one year old,
   with 0 deaths against 1.7% among the other infants. Natural blanks have no dose count, so the pair is a
   fingerprint.
   Mildest remedy: set covid_vaccine to "No" for these rows, the state at admission (no dose before it, which the
   dose count of 0 already says).

D (P4, LEAK-10, weak; optional): the influenza "Yes" with a dose dated after admission is blanked (5,519 cures, 77
   deaths). These blanks melt into the 31% natural blanks: within each age band the missing rate is the same for
   cures and deaths in the child bands where the blanks sit (0.5-2 y: 28.5% against 29.9%; 2-5 y: 32.0% against
   31.9%; 5-9 y: 31.1% against 29.3%). No action needed. For symmetry with C, "No" would be the admission state where no earlier dose is dated.

E (P7, CLEAN-12 / CLEAN-3, Should; cheap fix): `hospital` merges distinct hospitals. There are 4,434 names but 4,755
   (name, hospital municipality) pairs. 125 names stand for hospitals in 2 to 21 municipalities (82,276 rows, 9.3% of
   rows with a hospital), and 112 names cross state lines. Examples: HOSPITAL SAO LUCAS (21 municipalities), HOSPITAL
   SAO JOSE (19), HOSPITAL UNIMED (17), HOSPITAL SAO VICENTE DE PAULO (15). The definition ships municipalities as
   "name [IBGE code]" for this same reason. The hospital is the second-strongest input (0.727 alone).
   Mildest remedy: "name [hospital municipality IBGE code]", which the data allows (no CNES in the open data).

F (P7, CLEAN-12 re-reading of a decoded scale, and CLEAN-14, Should; cheap fix): "no schooling" mixes "not
   applicable" with illiterate adults. Of the 76,431 "no schooling" rows, 60,797 (80%) are children under 7 (1.5%
   deaths against 27.8% for the others). The dictionary (field 19) sets every under-7 to "não se aplica" (code 5),
   and the definition already makes code 5 missing. Another 1,011 children under 7 are coded primary 2nd cycle,
   secondary or higher, which is impossible.
   Mildest remedy: schooling missing for age_years < 7, the dictionary's own rule, as for code 5.

G (P7, CLEAN-11, Should; tiny):
   - age_years: 5 negative values (-5 to -1 months, from negative NU_IDADE_N) become missing.
   - puerperal "Yes": 343 men and 255 children under 10 (the field is enabled for women only, field 35) become
     missing.
   - COVID-19 dose dates before 2021-01-17, the first vaccination in Brazil: 144 first doses, 127 second doses and 3
     boosters (earliest 1957). They inflate covid_vaccine_doses, and days_since_covid_vaccine exceeds the days since
     2021-01-17 in 142 rows (up to 2,539). Set those dates missing before counting.
   Unusual but possible values that stay: days_onset_to_admission above 180 in 252 rows; a flu dose more than 2
   years old in 300 rows (earliest 2012); 46 rows with doses but covid_vaccine "No"; 181 men "not pregnant". BMI is
   already cut to 10-100 (931 values of 0.00-4.00 made missing); it is filled only with obesity "Yes", as the
   dictionary says.

H (P7, CLEAN-14 consistency, tiny): municipality spellings split one code into two levels. notification 4 codes
   (679 rows), residence 18 (1,054), hospital 4 (680). Examples: MOJI/MOGI MIRIM [353080], ACU/ASSU [240020],
   PARATI [330380], ITAPAGE [230630]. Remedy: one name per IBGE code (the newest spelling).

Q3 (P7, CLEAN-12 across the batch, question; per-dataset issue): occupation ships as "title [CBO code]" from the
   form's own pair. That is lossless: 507 codes and 507 titles, one to one; "XXX" (not informed) is missing; 0.5% of
   rows are filled. This follows CLEAN-12 (a job code in words). rais_employment_separation_1m ("occupation_cbo")
   and sinan_dengue_case_screening_1m keep the CBO codes as codes, and both leave the decode open for the curator.
   sinan also ships municipality, health region and unit as codes, where this dataset ships names or "name [code]".
   For this dataset: keep. The inconsistency should be settled in those two datasets' REVIEW.md, toward words.

Minor (P7, CLEAN-14 note only): pregnancy is a partial order (trimesters ordered; "not pregnant", "not applicable"
   and "gestational age unknown" outside the order). It is rightly unordered, but the notes do not say so.

**2. CHECKS THAT FOUND NOTHING**
- Risk factors completed after the outcome: no sign. The age-adjusted OR of the risk-factor flag is the same in forms
  written after the outcome and in routine forms (1.66 against 1.64). Recent admissions still open at the download
  have a lower fill rate among people 60 and over (69%) than both closed groups (cures 76%, deaths 80%). So some
  forms are completed by closing, but nothing shows the death drives it. The blank pattern (FATOR_RISC blank exactly
  when every factor is blank) is real "none reported" signal (missing indicator 0.66-0.68).
- Symptom missingness by outcome in routine forms: cough missing is higher for deaths (OR 1.52), dyspnoea and
  saturation missing lower (0.69, 0.71). These fit how sick the patient is on arrival. No field is blank because the
  outcome happened.
- Spans (LEAK-37, LEAK-41): days_onset_to_admission is the only span from the episode's dates. Age (birth to onset)
  and the days since vaccination (dose to admission) end at or before admission. No length of stay, ICU, outcome or
  closing date survives. There is no training weight, so probe 22 does not apply.
- Notification place: it equals the hospital place except in 0.4% of cures and 0.8% of deaths (late forms OR 3.95).
  These may be transfers. They are tiny and part of A2.
- The "ignored" codes: every 1/2/9 item has 9 made missing; sex I, pregnancy 0 and 9, race 9, zone 9 and animal
  contact 9 are missing. The data's sex codes are M/F/I while the dictionary prints 1/2/9; they are decoded
  correctly. Race codes 1-5, zone, animal contact and pregnancy codes are decoded right against the dictionary.
- Schooling order: no schooling < primary 1-5 < primary 6-9 < secondary < higher. It is ordered (cat.ordered True),
  in the dictionary's order; codes 5 and 9 are missing. The order is not reversed.
- Health regions: no name maps to two codes or two states. Pernambuco's GERES are named "001"-"012", which are names.
  RJ, DF, AP, RR and TO have no regions, so they are missing for the whole state.
- Dtype probe (4 flags, ordinal_like): the three health regions (Pernambuco's numbered names) and
  residence_municipality ("[code]"). They are names; no action. I agree with the builder.
- The target: categories ['No','Yes'] with "Yes" = death (CLEAN-25). Code 3 counted as death: I agree with the
  builder's issue 2. The target is death of any cause in hospital, which the team acts on (USE-5). LEAK-22's
  competing event concerns a cause-specific outcome within a horizon. Open (4.7%) and "ignored" (1.8%) rows:
  invasive ventilation 9.9% and 14.0% against 6.7% for cures and 44.1% for deaths. As a mixture that is about 8% and
  20% deaths against 10.6%. Dropping them changes the death rate little, and the shares are stable by year (open
  3.7-4.9% in 2023-2025).
- Identifiers: the record number, birth date, CPF and CNS are not in the data or are dropped. No id encodes the label.
- Exact copies across the split: 0.4% without the date and texts, 0% with them (builder's probe 5). Natural repeats
  of yes/no profiles.

**3. COLUMN TABLE (65 columns: 64 inputs and the target)**
Legend for the known column: yes = known at admission; yes* = known at admission in routine forms, but in the 14.4%
of forms filled on or after the outcome day the value can carry the stay (problem A).

column | meaning (dictionary field) | known at prediction? | dtype and cleaning | verdict | rule
notification_state | state of the notifying unit (3, SG_UF_NOT) | yes (the unit is the admitting hospital in 99.5%) | category, 27 | fine | -
notification_health_region | health region of the notifying municipality (internal, ID_REGIONA) | yes | category, 304; 13.2% missing (5 states have none) | fine | CLEAN-14
notification_municipality | municipality of the notifying unit, "name [IBGE]" (4, ID_MUNICIP/CO_MUN_NOT) | yes | category, 2,041; 4 codes with 2 spellings (679 rows) | cleaning, minor: one name per code | CLEAN-14
residence_country | country of residence (31, ID_PAIS) | yes | category, 29 levels, 99.97% BRASIL | fine | -
residence_state | state of residence (23, SG_UF) | yes | category, 27 | fine | -
residence_health_region | health region of residence (internal, ID_RG_RESI) | yes | category, 320; 12.1% missing | fine | -
residence_municipality | municipality of residence, "name [IBGE]" (24) | yes | category, 5,546; 18 codes with 2 spellings (1,054 rows) | cleaning, minor | CLEAN-14
residence_zone | urban/rural/periurban (30, CS_ZONA) | yes | category; 9 missing | fine | CLEAN-10
sex | sex (11, CS_SEXO: M/F/I in the data) | yes | category; I (93) missing | fine; protected ground: question | SEL-1
pregnancy | gestational age (14, CS_GESTANT) | yes | category 6 levels, unordered; 0 (no code) and 9 missing | fine; note the partial order | CLEAN-14
race_colour | self-declared race or colour (15, CS_RACA) | yes* (missing 25% of late cures against 10% of late deaths) | category 5; 9 missing | protected ground: question; adds 0.0000 | SEL-1, (A)
indigenous_ethnicity | SIASI ethnicity if indigenous (16, CS_ETINIA) | yes | category 228; 99.5% missing | protected ground: question | SEL-1
traditional_community | member of a traditional people (17, POV_CT) | yes | category Yes/No | fine (with SEL-1 question) | SEL-1
traditional_community_type | which people (18, TP_POV_CT) | yes | category 34; 99.5% missing | fine (with SEL-1 question) | SEL-1
schooling | last grade completed (19, CS_ESCOL_N) | yes | ordinal, order right; 5 and 9 missing; "no schooling" is 80% under-7s (60,797) | cleaning: missing for age < 7 | CLEAN-12, CLEAN-14
occupation | occupation, "title [CBO]" (20, PAC_DSCBO/PAC_COCBO) | yes | category 506; one to one; XXX missing; 99.5% missing | fine; cross-dataset question | CLEAN-12
has_cpf | patient has a CPF (6, TEM_CPF) | yes | category Yes/No | fine | -
foreigner | foreign national (8, ESTRANG) | yes | category Yes/No; 5.6% missing | fine | -
hospital_acquired | SARI acquired after admission (32, NOSOCOMIAL) | at the SARI's recognition, not at admission | category Yes/No; 9 missing | question: prediction point for 2.6% of rows | USE-3
animal_contact | works with or has contact with birds/pigs/other (33, AVE_SUINO) | yes | category; 9 missing | fine | -
other_animal_text | which other animal (33, OUT_ANIM) | yes | string; "?" missing | fine | -
fever | fever (34, FEBRE) | yes* | category Yes/No; 9 missing | fine (no route difference) | -
cough | cough (34, TOSSE) | yes* | category Yes/No | fine; part of A (missing OR 1.52) | LEAK-10 (A)
sore_throat | sore throat (34, GARGANTA) | yes* | category Yes/No | fine | -
dyspnoea | dyspnoea (34, DISPNEIA) | yes* (death OR 2.2-2.7 late vs 1.3-2.1 routine) | category Yes/No | leak in post-outcome forms (A) | LEAK-10
respiratory_distress | respiratory discomfort (34, DESC_RESP) | yes* (OR 2.4-3.7 late vs 1.4-2.3 routine) | category Yes/No | leak in post-outcome forms (A) | LEAK-10
o2_saturation_below_95 | O2 saturation < 95% (34, SATURACAO) | yes* (OR 2.9-3.5 same day vs 1.3-2.3 routine) | category Yes/No | leak in post-outcome forms (A) | LEAK-10
diarrhoea | diarrhoea (34, DIARREIA) | yes* | category Yes/No | fine | -
vomiting | vomiting (34, VOMITO) | yes* | category Yes/No | fine | -
abdominal_pain | abdominal pain (34, DOR_ABD) | yes* | category Yes/No | fine | -
fatigue | fatigue (34, FADIGA) | yes* | category Yes/No | fine | -
loss_of_smell | loss of smell (34, PERD_OLFT) | yes* | category Yes/No | fine | -
loss_of_taste | loss of taste (34, PERD_PALA) | yes* | category Yes/No | fine | -
other_symptoms | other symptoms yes/no (34, OUTRO_SIN) | yes* | category Yes/No | fine | -
other_symptoms_text | other signs listed (34, OUTRO_DES, 30 chars) | partly no: 269 ICU/intubation (57.6% deaths), 275 arrest, death phrases | string; "?" missing | leak, Must, tiny: blank the cells | LEAK-10, LEAK-2 (B)
puerperal | postpartum up to 45 days (35, PUERPERA) | yes | category Yes/No; blank when no risk factor; 343 men and 255 under-10s "Yes" | cleaning: those "Yes" missing | CLEAN-11
chronic_cardiovascular_disease | (35, CARDIOPATI) | yes (no route difference) | category Yes/No; 65% blank = none reported | fine | CLEAN-10
chronic_haematological_disease | (35, HEMATOLOGI) | yes | category; as above | fine | -
down_syndrome | (35, SIND_DOWN) | yes | category; as above | fine | -
chronic_liver_disease | (35, HEPATICA) | yes | category; as above | fine | -
asthma | (35, ASMA) | yes | category; as above | fine | -
diabetes | (35, DIABETES) | yes | category; as above | fine | -
chronic_neurological_disease | (35, NEUROLOGIC) | yes | category; as above | fine | -
other_chronic_lung_disease | (35, PNEUMOPATI) | yes | category; as above | fine | -
immunodeficiency | (35, IMUNODEPRE) | yes | category; as above | fine | -
chronic_kidney_disease | (35, RENAL) | yes | category; as above | fine | -
obesity | (35, OBESIDADE) | yes | category; as above | fine | -
bmi | BMI by the professional, only with obesity Yes (35, OBES_IMC) | yes | float; 10-100 kept, 931 values 0-4 missing; 99.9% missing | fine | CLEAN-11
other_risk_factors | other risk factors yes/no (35, OUT_MORBI) | yes | category Yes/No | fine | -
other_risk_factors_text | other risk factors listed (35, MORB_DESC) | partly no: 177 ICU mentions (mostly earlier stays), dialysis, sepsis | string; "?" missing | leak, tiny: blank the cells of the list (B) | LEAK-10
covid_vaccine | received a COVID-19 vaccine (36, VACINA_COV; register 96%) | yes after the fix | category; blanked when every dose is after admission: 922 rows, 99% cures | leak, Must, tiny: "No" instead of blank | LEAK-10 (C)
covid_vaccine_doses | doses dated on or before admission (built from 37) | yes | float count 0-6 | cleaning: 274 doses dated before 2021-01-17 to drop | CLEAN-11
days_since_covid_vaccine | admission minus last dose before it (built) | yes | float; 142 values above days since 2021-01-17 | cleaning: as above | CLEAN-11
flu_vaccine_last_campaign | flu vaccine in the last campaign (40, VACINA) | yes | category; "Yes" with a dose after admission blanked (5,519 cures, 77 deaths), diluted | fine (optional "No") | LEAK-10 (D)
days_since_flu_vaccine | admission minus DT_UT_DOSE (41) if not after | yes | float; 300 above 2 years | fine | -
mother_flu_vaccinated | mother vaccinated, infant < 6 months (MAE_VAC) | yes | category; 97.8% missing | fine | -
breastfed | breastfed, infant < 6 months (M_AMAMENTA) | yes | category; 96.7% missing | fine | -
hospital_state | state of the hospital (50, SG_UF_INTE) | yes | category; 3.8% missing (whole hospital block) | fine | -
hospital_health_region | health region of the hospital (internal) | yes | category 304; 16.5% missing | fine | -
hospital_municipality | municipality of the hospital, "name [IBGE]" (51) | yes | category 1,992; 4 codes with 2 spellings | cleaning, minor | CLEAN-14
hospital | name of the admitting unit (52, NM_UN_INTE; no CNES) | yes for referral hospitals; for death-notifying units it records where the patient ended | category 4,434; 125 names stand for several hospitals (9.3% of rows) | cleaning (name [municipality code]); maybe-leak note (A2) | CLEAN-12, LEAK-25/34
admission_date | date of hospitalisation for SARI (49, DT_INTERNA) | yes: the prediction point and the time column | datetime | fine | -
age_years | age at onset, built from NU_IDADE_N/TP_IDADE (13) | yes | float; over 120 missing; 5 negative values remain | cleaning: negative missing; protected ground kept (clinical core) | CLEAN-11, SEL-1
days_onset_to_admission | admission minus onset (2, 49) | yes (negative only for hospital-acquired) | float; outside +-365 missing; 252 values above 180 | fine (the only span) | LEAK-37, LEAK-41
died_in_hospital (target) | EVOLUCAO 1 cure -> No; 2 death, 3 death from other causes -> Yes (82) | outcome | category ['No','Yes']; open and 9 dropped | fine; issue 2 agreed | USE-5, LEAK-22, CLEAN-25

**4. FILES**
Scripts and logs: panel/
  a01_overview.py (dtypes and missing rates by outcome)
  a02_raw.py / a02_raw.log (fill and missingness by outcome and route, age-adjusted ORs; open and ignored profile)
  a03_raw2.py / a03_raw2.log (ORs by route and length of stay; recent open cases; impossible values; name
    collisions; CBO)
  a04_clean.py / a04_clean.log (vaccine fingerprint; schooling by age; impossible values; texts)
  a05_routes.py / a05_routes.json (AUC by route; 7-day lag rule; missing-flags model)
  a06_texts.log, a09_text_instay.log (text classes and the 808-cell blank list)
  a07_names.log (municipality spellings; numbered health regions)
  a08_sel1.log (AUC without protected grounds)
  a10_hosp.log (units that notify mostly deaths)

</details>

<details><summary>Split audit</summary>

SPLIT AUDITOR REPORT: sivep_gripe_sari_outcome (2026-11-09)
Definition: (the run folder)
Scratch (scripts, frames, fit logs): (the run folder)

VERDICT: right with notes. Nothing needs a re-split, a different gap or a filter. The notes are additions to splits_comment.

Judgment record
  Validity (P4): SPLIT-1/SPLIT-3/USE-10 hold (temporal, known hospitals); LEAK-24 holds (checked with a simulated
  earlier download); SPLIT-9 holds (no shortcut: no row is in train because of its outcome, and readmissions are closed
  before the test admission); SPLIT-14 holds (51.0/65.9/83.2%, and the floor is what limits the design); SPLIT-10 holds
  (a one-month gap, its effect measured); SPLIT-20/SPLIT-21 hold (2023 history set by the break, not by scores).
  Notes: the season weighting, the forms typed after the window start, and the death-share trend (drift, not censoring).
  For the curator: issue 1 (2023 against 2020 `_1m`). I agree with 2023 (finding 5).

How I checked: I rebuilt the frame and splits from the definition (dataset_io.from_definition, raw=True, 922,908 rows,
lineage traced) and attached the raw dates (DT_ENCERRA, DT_EVOLUCA, DT_DIGITA, DT_NOTIFIC, DT_NASC) to each row. The
windows rebuilt from admission_date match the shipped split exactly: test 139,737 / 130,431 / 167,794; train 768,238 /
608,548 / 470,290. Model fits: LightGBM with 500 trees, lr 0.05 and 63 leaves, on every feature except the three texts
and the date, 4 threads. Seed noise on the newest window: 0.8871-0.8877 over 4 seeds (SD about 0.0003).

**FINDINGS (rank order: P4 Must rules first, then Should rules, then notes)**

1. LEAK-24 (Must): the end at 2026-06-30. HOLDS, now checked directly.
   Evidence: I simulated an earlier download. Admissions of Jan-Jun 2025 read as of 2025-11-09 have the same 131-312
   days of follow-up as Jan-Jun 2026 at the real download. Counting a label as known when the case was closed
   (DT_ENCERRA) and typed (DT_DIGITA) by that date:
     98.0% of the cases closed later were already known: 98.1% of deaths, 98.0% of discharges.
     Death share of the known labels: 10.31%. Final: 10.28%. June 2025 alone (131 days): 10.17% against 10.22%.
     The same test a year earlier (Jan-Jun 2024 read as of 2024-11-09): 11.15% against 11.10%.
   Rows still open: Jan-Jun 2026 has 10,074 (7.2%), against 5,562-6,803 in each earlier half-year. That is about
   4,000 extra rows. Their expected death share, from the death rates of closed rows in the same half-year by age decade
   and ICU, is 9.9%, so counting them would move the window's 8.29% by about +0.05 points.
   The falling death share by window (10.3 / 9.4 / 8.3%) is real drift, not censoring:
     Age mix: under-5 share 47.8 / 46.0 / 51.4%; 60+ share 27.7 / 27.6 / 23.8%.
     Lower death rates within age groups: 60+ 26.0 / 23.8 / 23.7%; 18-59 16.0 / 15.0 / 14.2%.
     Age-standardised death share: 10.4 / 9.5 / 9.4%.
     COVID-19 share: 4.9 / 6.1 / 2.9%, against 11.7-20.2% per half-year in 2023-2024.
   The trend runs through the whole history: 12.2% (2023H1), 11.1% (2024), 8.3% (2026H1). A temporal split should test
   this kind of drift (probe 13: monthly z down to -2.9, inside the band).
   Remedy: none. Optional: add the simulated-download result to the notes next to the 90/150/240-day closing shares.

2. SPLIT-9 (Must): unmatured training labels and the patient's own earlier labels. HOLDS, no shortcut.
   Evidence:
   (a) No training row is there because its outcome came early. The training side is set by admission date, and only
       rows still open at the download leave, in every period alike.
   (b) Readmissions. There is no patient id, but the raw birth date (dropped from the features) gives a key: birth
       date, sex, residence municipality code and race (99.94% of rows have one). With it, 9.9% / 13.1% / 14.1% of the
       test rows (2025H1 / 2025H2 / 2026H1) have an earlier stay in training, a median of 271-330 days before. These
       patients die less (3.9-4.9% against 9.0-10.9% for the others), as expected for survivors of an earlier stay.
       Only 14-41 rows per window (0.01-0.03%) have a training stay whose outcome date falls on or after the test
       admission. Their death share is 7.7-14.3%, near the base rate, so that label does not give the test outcome
       away. The key also joins different people: 2.4% of matched training stays are deaths, which a true readmission
       cannot have (7.2-7.5% among adults). So these shares are upper bounds.
   A deployed model meets the same readmissions, with their earlier outcomes known (USE-10).
   Remedy: none. Optional note: about 10-14% of test admissions are readmissions under this key.

3. SPLIT-14 (Must) and SPLIT-15 (Should): the windows. HOLD, and the floor is what limits the design.
   Evidence:
     Train sides: 51.0% / 65.9% / 83.2% of the rows. Three windows, the default fold count.
     Test windows: 130k-168k rows each; the smallest class is 11,594 deaths (2026H1).
     The oldest window is just above the floor. A two-month gap would give 49.3%. Any earlier half-year would give
     about 38%. Yearly windows give only two.
   So these half-year windows on 2023+ data are the only ones possible. A finer cadence (quarters) would give more
   windows at the same floor, but SPLIT-15 asks for the default 3 and SPLIT-12 for the refit cadence. Keep it.
   Remedy: none.

4. SPLIT-1, SPLIT-3, SPLIT-13 and USE-10 (Must): the regime. HOLDS.
   Use case: the hospital team scores each SARI admission with a model built on past admissions. That is a stream over
   time and known hospitals, so the split is temporal by admission date. The time column means what the prediction
   point needs: the notification follows admission by a median of 1 day.
   Hospitals:
     Of the test rows with a hospital name, 95.7% / 98.9% / 99.6% come from a hospital seen in training.
     Of all test rows: 91.4% / 94.8% / 95.8%. 3.8-4.5% have no hospital name.
     80-90% come from hospitals with 50 or more training rows. Death share is the same for seen, unseen and blank
     hospitals (8.3-10.2% against 10.9-12.0% against 7.7-10.5%).
   Recurring hospitals are part of the task (SPLIT-13, and LEAK-34: the hospital is known at admission).
   No date errors at the window edges: 17-20 test rows per window were notified more than 30 days before the window
   started, and no outcome comes before its admission.
   Remedy: none.

5. SPLIT-20 (Should) and SPLIT-21 (Must): history from 2023, the builder's issue 1. HOLDS. I agree with 2023.
   The break, by half-year of admission (hospitalised, known outcome; small_cols_2019_2026.parquet):
     2020H1-2022H2: death 17.5-31.9%, COVID-19 39-82%, age 60+ 43-54%, under-5 4-27%.
     2023H1-2026H1: death 8.3-12.7%, COVID-19 2.9-20%, age 60+ 24-32%, under-5 41-51%.
   With history from 2020:
     79.5-86.4% of each train side would be 2020-2022 rows (3.46M-3.75M rows; death 24-26% against 11-12%).
     A `_1m` sample would keep about 14-21% post-2023 rows, i.e. about 140k-210k instead of 470k-768k.
   The 2023 history already has two full seasons before the first window (SPLIT-20).
   Quick fits, for information only (SPLIT-21: they do not decide). ROC AUC per window, 2026H1 / 2025H2 / 2025H1:
     From 2023 (shipped):                      0.8871 / 0.8804 / 0.8782
     From 2022 (one more year, transition):    0.8889 / 0.8804 / 0.8794
     From 2022H2:                              0.8878 / 0.8801 / 0.8791
     Shipped gap, last 12 months of training:  0.8828 / 0.8778 / 0.8746
   Adding 2022 on top of all post-2023 rows gains at most +0.002 and does not hurt the ranking. Cutting training to the
   last 12 months loses 0.004-0.005. Training size matters more than recency at this scale, so a `_1m` that replaces
   most post-2023 rows with pandemic rows is unlikely to be better.
   I could not fit 2020-2021: those files were not downloaded.
   Remedy: none. Keep 2023, decided on the break, as the builder recommends.

6. SPLIT-10 (Should): the one-month gap against the label delay. HOLDS, effect measured.
   Delay from admission to closing (admissions of Jan-Jun 2025):
     Median: 17 days for deaths, 13 for discharges.
     90th percentile: 66 and 60 days. 95th percentile: 102 and 101 days.
   With the one-month gap, 1.0% / 2.2% / 1.7% of each train side (2026H1 / 2025H2 / 2025H1) had no label at the window
   start: closed after it (0.9-1.9%) or typed after it (0.3-0.7%). Deaths and discharges are alike: 1.13% against
   1.03%, 2.07% against 2.18%, 1.82% against 1.72%.
   Deaths still close more slowly in the last training month: 19.6-22.7% still unlabelled at the start, against
   14.8-16.0% of discharges. Its death share counting only known labels is 0.5-0.8 points below the shipped one.
   Fits, ROC AUC per window, 2026H1 / 2025H2 / 2025H1:
     A. Shipped (gap 1, final labels):                0.8874 / 0.8803 / 0.8785
     B. Gap 1, only labels known at the start:        0.8874 / 0.8798 / 0.8784
     C. No gap, only labels known at the start
        (a real refit at the window start):           0.8876 / 0.8809 / 0.8785
     D. No gap, final labels:                         0.8875 / 0.8830 / 0.8792
   Reading:
     A against C: -0.0002 / -0.0006 / 0.0000. The gap costs almost nothing against a real refit.
     D against C: +0.0021 on the July window. Without the gap the July window would be overrated; the gap removes this.
     A against B: within noise. The 1-2% of unmatured labels kept in training do nothing measurable.
   Remedy: none. Optional wording in splits_comment:
     "0.9% to 1.9% ... open" leaves out the forms typed after the start; with them it is 1.0% to 2.2%.
     The measured effect could be added: no gap overrates the July window by 0.002; the gap costs at most 0.0006.

7. SPLIT-20 (Should), SPLIT-12 (Should): season shape of the windows. HOLDS, with a note.
   Two of the three windows are January-June. These hold the rise and peak of the RSV and influenza season (May-June
   2025: 51k and 47k admissions; 2026: 36k each). They hold 70.2% of the test rows (307,531 of 437,962) and two thirds of
   the weight in a mean over windows.
   No season penalty shows: per-window ROC AUC is 0.8785 (2025H1), 0.8803 (2025H2), 0.8874 (2026H1). Every window is a
   whole half-year, so none is an atypical sliver of a season.
   The sibling sinan_dengue_case_screening_1m states its season weighting in its splits_comment; treat like cases
   alike.
   Remedy: one sentence in splits_comment giving the weighting and the per-window scores.

8. Note (cohort, not split; LEAK-22 or USE-7 reading): rows open at the download leave, and they are riskier than the
   closed rows in every half-year. Expected death share from age decade and ICU: 10.8-16.6%, against 8.3-12.7%
   observed. The open share is higher in the frozen 2023-2024 files (3.2-7.8% a month) than in the live 2025 file
   (2.2-4.2%). The selection is stable across the train and test sides and small. Nothing to change on the split.

Outside my remit, a pointer only: counting admissions per hospital inside a test window would read later test rows.
The dengue sibling's splits_comment has a protocol line on this. The task gamer should measure it if it matters.

Scripts in :
  a01_load.py: frame and splits plus raw dates.
  a02_censoring.py: simulated earlier download.
  a03_describe.py: age, COVID-19 and hospitals by window.
  a04_patients.py: readmission key.
  a05_gap.py: labels unknown at the window start.
  a06_fits.py: gap variants A-E.
  a07_history.py: the 2019-2026 break.
  a08_open_rows.py: open rows.
  a09_frame2022.py and a10_history_fits.py: the 2022 history.
  a11_seed_noise.py: seed noise.
  Logs: fits_gap.json, fits_history.json, seed_noise.log.

</details>

<details><summary>Domain practitioner</summary>

DOMAIN PRACTITIONER REPORT: sivep_gripe_sari_outcome (2026-11-09)
Actor played: the bed manager of a Brazilian hospital or of a state/municipal bed-regulation centre (Núcleo Interno
de Regulação, Central de Regulação), scoring a SARI patient at admission for monitoring, early ICU referral and beds;
also checked against the surveillance team of the prompt and the policy reading of Baqui et al. 2021.

VERDICT
  Fit: APPROXIMATE (agree with the builder). The rows, the label timing and the next-half-year test mirror a hospital
  scoring its new SARI admissions, but the notification form holds only part of what the admitting team knows (no
  vital signs, oxygen need or laboratory values, symptoms as yes/no), so the model is a form-only stand-in for the
  bedside risk estimate (USE-8).
  Metric: PARTLY. ROC AUC ranks my patients, but pooled over 4,434 hospitals and all ages it mostly rewards telling
  infants from the elderly (pooled 0.882 vs 0.759 among adults), and it ignores calibration, which my bed planning
  needs (models over-predict deaths by 12% in the test windows). I would choose log_loss (MET-8, MET-10).
  Builder's issues: 1 history from 2023 - agree; 2 death from other causes = death - agree; 3 keep the forms filled
  after the outcome - agree, but name them in fit_reason as kept, not as a gap (USE-8 amendment).
  Race/colour: no Brazilian statute bars it in a hospital's clinical risk score (unlike Lei 9.029/1995 for the rais
  employer), so the "actor's own law" stance does not strictly apply; as the actor I would still not put it in a
  triage score (SUS equality principle, medical ethics code, triage protocols, Brazilian admission scores omit it),
  and it carries no signal (ROC AUC 0.8819 -> 0.8817). Recommend dropping it as a curator call.

1. AT THE PREDICTION POINT (ADMISSION), DO I HAVE EACH INPUT?

  Have at admission (as the admitting team, which fills the form):
  - age, sex, pregnancy, residence, the hospital and its place, days from first symptoms: yes (age, sex 100% filled).
  - the 13 symptoms (fever 90%, dyspnoea 90%, saturation < 95% yes/no 86% filled) and 13 risk factors: yes, taken at
    the first examination. Blank risk factors (65-70%) mean "none reported", as the notes say.
  - COVID-19 and influenza vaccination before admission: yes in practice (vaccination card, or the national register
    the form is linked to); the builder kept only doses dated on or before admission (LEAK-10), which is right.
  - race/colour (90% filled, self-declared, mandatory field by Portaria GM/MS 344/2017) and schooling (26% filled):
    collected at registration, so available; whether I may use race is under 6.
  - free texts of other symptoms / risk factors: yes.

  Would NOT have at admission: nothing shipped. The notification date is dropped; the form is notified a median 1
  day after admission (43% on the admission day or before), within the 24 h the Ministry asks (Nota Técnica
  11/2026). Every in-stay field is out (ICU, ventilation, antivirals, tests, classification).

  Missing, that I always have at admission (ranked by weight):
  a. Vital signs and oxygen: the SpO2 value and FiO2/oxygen need, respiratory and heart rate, blood pressure,
     consciousness. Brazil's own admission score ABC2-SPH (Marcolino et al. 2021) uses age, urea, number of
     comorbidities, CRP, SpO2/FiO2, platelets and heart rate; 4C uses RR, SpO2, GCS, urea, CRP. The form gives one
     yes/no for SpO2 < 95%. This is the gap that makes the fit approximate; the source cannot fill it.
  b. Where I admit the patient: 20.5% of the rows entered ICU on the admission day (74% of all ICU stays; 37% of the
     deaths; death rate 19.3% vs 6.4% never in ICU). For them the "early ICU referral" decision was taken before my
     prediction. The flag is known at admission (I placed the patient) and is the strongest admission-day fact the
     shipped table lacks: +0.008 pooled ROC AUC (0.8819 -> 0.8901), +0.018 among adults (0.759 -> 0.776), log loss
     0.2179 -> 0.2121 (LightGBM, 3 windows; d03). The builder dropped `UTI`/`DT_ENTUTI` as in-stay fields, which they
     are after day 0.
  c. A rapid antigen result and a chest X-ray dated on or before the admission day: 31.7% and 36.4% of the rows
     (SARS-CoV-2 positive die at 22.7%, RSV positive at 0.9%, negative 8.5%). Date-gated as for the vaccines, they add
     only +0.0006 ROC AUC (0.8825) and -0.0005 log loss: keeping them out is fine.
  d. Frailty / functional status (Clinical Frailty Scale, ECOG): not on the form.

2. IS THE TARGET WHAT I ACT ON?

  In-hospital death of any cause vs discharge alive. For bed planning and for prognosis it is the right event, and
  it is Baqui's label. For the early-referral decision the practice target is deterioration (ICU, ventilatory
  support or death: ISARIC 4C Deterioration, Gupta et al. 2021); here ICU after the admission day, invasive
  ventilation or death is 20.3% of the rows (16.5% outside day-0 ICU). Death is also shaped by the escalation it is
  meant to trigger (patients judged at risk got ICU and survived), a known limit of a death label in a treated
  population; name it, do not change it (USE-5: the label is the actor's outcome, not another quantity).
  Issue 2 (death from other causes, EVOLUCAO = 3, 28% of the deaths): count as death. The certified cause comes after
  the death and is not mine to act on at admission. Measured: code-3 deaths look like code-2 deaths (median age 68 vs
  72, ICU 54.6% vs 54.3%, median 9 vs 8 days to death; 71% vs 50% "unspecified SARI"). LEAK-22's competing-event
  reading would mark a dead patient as discharged: wrong for every actor here; only a surveillance count of
  SARI-attributable deaths would drop them, and that is another use case.
  Form: a probability. I set monitoring levels by it and sum it into expected deaths and ICU demand per ward and week;
  a class is of no use to me.

3. DOES ONE ROW MATCH ONE DECISION? IS THE TEST WHAT I FACE?

  One row = one admission notified to SIVEP-Gripe = one decision at admission: yes (USE-1). No patient id, so a
  re-admission is a new row, as it is for me.
  Test = the next half-year at hospitals I already know (94% of test rows): this is a deployed model refit twice a
  year before and after the season (USE-10, a known entity). Training stops one month before the window: fine.
  Issue 1 (history from 2023): agree. A team refitting in 2025-2026 would not learn a SARI patient's risk from
  2020-2021 (61-83% COVID-19 per quarter, 25-34% deaths, saturated hospitals, closing criteria changed on
  2022-10-31); they would fill 79-86% of the training rows. The call rests on the break, not the score (SPLIT-20,
  SPLIT-21).
  Issue 3 (7.5% of forms filled after the patient left): keep. They are admissions I would have scored at admission;
  only the paperwork came late. Their features describe the admission; training without them changes nothing on the
  routine rows (0.8731 vs 0.8732, builder). Under USE-8's amendment a kept, measured remnant (+0.002) is named as
  kept, not as a gap: the current fit_reason lists it beside the real gap ("and 7.5% of the forms ..."); move it into
  a "kept" clause.
  The surveillance team of the prompt cannot be the real-time actor: the form is typed into SIVEP a median 4 days
  after admission (p90 28 days), and 42.4% of the deaths happened before their form was typed. Only the hospital (or
  the regulator receiving the hospital's request) holds these inputs at admission. This also settles issue 3 for the
  hospital: for a surveillance actor the retrospective forms would not be decision rows; for the hospital they are.
  Population: 61% of the test rows are children under 18 (1-2% die) and hold 10% of the deaths; adults hold 90%. The
  population is real (RSV in infants dominates SARI since 2023), and the setting shares it, so it is no selection gap
  (USE-8, last paragraph), but no single ward ranks an infant against an 80-year-old; see 5.

4. WOULD I USE THIS MODEL?

  As the bedside team: not instead of my scores with vital signs and labs (NEWS2, 4C, ABC2-SPH). Its adult
  discrimination (ROC AUC 0.759 among adults, 0.734 at 60+) is in the range of age-and-comorbidity-only tools, below
  what a score with SpO2/FiO2, urea and CRP reaches in Brazilian cohorts.
  As a hospital network or state bed-regulation manager, who receives the notification-level picture from many
  hospitals: yes, as a case-mix prior for expected deaths and ICU demand per hospital and week, and to flag the
  admissions to look at first. The hospital name is legitimate for me (LEAK-34; known at admission).
  USE-9: the one other use with the same inputs and label is a state's risk-adjusted comparison of hospitals'
  SARI mortality (observed against expected deaths); it needs the hospital out of the inputs and looks back, so it
  would be a rephrase to excuse the gap (weighed factor against USE-9), not a direct fit.
  Trust: stable over windows (0.878, 0.880, 0.887), sensible drivers (age, comorbidities, vaccination, hospital),
  no in-stay field left. Distrust: calibration under the seasonal and secular drift (train 11.1-11.8% deaths, test
  8.3-10.3%: mean predicted 0.104 vs observed 0.093 pooled, +12%; by race the over-prediction is 7-15%, indigenous
  under-predicted by 8-13%), and the ICU-day-0 mix (2b).

5. DOES ROC AUC SCORE MY DECISION? PARTLY.

  Right: no source fixes a threshold, a k or costs (MET-6, MET-7: never invent a k; ICU capacity varies by hospital
  and day), and a ranking of admissions by risk is the core of "whom to watch first" (MET-8).
  Wrong for my decision:
  - Unit: the pooled ranking mixes hospitals and ages I never rank against each other. Pooled 0.882; within-hospital
    (pairs inside a hospital) 0.854; adults 0.759; children 0.805; age 60+ 0.734. The hospital identity adds 0.006
    pooled but 0.001 within hospitals; age alone already scores 0.812 (builder). Much of the pooled score is the
    infant-vs-elderly contrast any clinician makes without a model.
  - Calibration: bed planning sums the probabilities; AUC is blind to the +12% over-prediction above.
  What I would choose: log_loss (strictly proper, MET-8; Gneiting & Raftery 2007): it scores the ranking and the
  calibration together, serves any monitoring threshold and the expected counts for beds, and adds a binary log-loss
  task to the collection (MET-10 diversity). The binary log_loss tasks so far come from a competition (bioresponse,
  numerai28_6); here it would be origin `context` (MET-11: bed planning sums the probabilities), a curator call. Not
  average_precision (MET-9: imbalance alone is no reason, and no source chose it as the criterion); not
  precision_at_k (MET-7); not a cost matrix (MET-6). A within-hospital or adults-only AUC would match my unit better
  but no source defines it (MET-11 context needs a clear case); I would not build a custom metric for it.
  If the curator keeps roc_auc: Baqui et al. rank their models by AUC-ROC and measure feature importance as its drop
  (full text, Europe PMC), and the record's screening line says the same; that reads as a deliberate choice (MET-5),
  so the origin may be `source`, not `fallback` as the builder wrote ("no single criterion"). Check before shipping.

6. RACE OR COLOUR AS AN INPUT

  Does Brazilian law bar it for a hospital's triage? Not explicitly. What I found:
  - Lei 8.080/1990 art. 7 IV (SUS principles): "igualdade da assistência à saúde, sem preconceitos ou privilégios de
    qualquer espécie" - equality of care, no prejudice or privilege of any kind.
  - Código de Ética Médica (Res. CFM 2.217/2018), principle I: medicine "será exercida sem discriminação de nenhuma
    natureza"; Res. CFM 2.454/2026 on AI in medicine asks for bias mitigation (news summaries; text not read).
  - Estatuto da Igualdade Racial (Lei 12.288/2010) art. 8 I: fight discrimination in SUS services; art. 7: improve
    SUS data disaggregated by colour, ethnicity and gender. Portaria GM/MS 344/2017 makes the field mandatory, for
    equity monitoring.
  - LGPD art. 5 II / 11: race is sensitive data, processable for health protection by health services; art. 6 IX
    forbids processing for unlawful or abusive discriminatory ends.
  - AMIB/ABRAMEDE/SBGG/ANCP ICU allocation protocol (2020): per a search summary (PDF not readable here) it states it
    uses no criteria based on origin, race, sex, colour or age; it governs allocation under scarcity, not prognosis.
  - Brazilian and UK admission scores (ABC2-SPH, 4C) do not use race; QCOVID used ethnicity, but for population
    shielding (a policy actor), as Baqui et al. do for policy.
  So there is no statutory bar like Lei 9.029/1995 art. 1 for the rais employer; the principles.md tension row ("the
  actor's legal constraint today") does not strictly force the drop, and USE-6 would keep it. As the hospital actor I
  would not use it: a triage score that moves priority by colour would not pass my ethics committee under the SUS
  equality principle and the medical code. Measured (LightGBM, 3 windows, d02): without race_colour,
  indigenous_ethnicity, traditional_community(+_type): ROC AUC 0.8819 -> 0.8817, log loss 0.2179 -> 0.2180,
  within-hospital 0.8536 -> 0.8537: no signal. With schooling, occupation, has_cpf and foreigner also out: 0.8800
  (-0.002). Recommendation: drop race_colour, indigenous_ethnicity and the two traditional-community fields for the
  hospital actor (curator call: it extends the stance from law to the profession's norm); keep sex and age (clinical,
  in every admission score). Keeping them is defensible only with the policy actor (Baqui), which is a different use
  case. Either way, say in `known` and the notes which reading was taken.

GAPS BETWEEN THE DATASET AND MY DECISION (ranked by how much they change the task)

  1. Form-only inputs: no vital signs, oxygen need, labs or frailty (1a, 1d). Cannot be fixed from this source; the
     reason the fit is approximate. fit_reason says this already.
  2. Decision state at admission: 20.5% of rows admitted straight to ICU, unflagged (1b). For the early-referral
     decision they are not candidates; for bed planning the flag is a known input worth +0.008 ROC AUC. Either ship
     an `icu_on_admission_day` flag (ICU entry dated on or before the admission day) with a note, or name the mix in
     fit_reason. Caveat: day granularity also counts an ICU transfer later the same day.
  3. The pooled score's unit (5): 61% children, 4,434 hospitals; pooled 0.882 vs adults 0.759. Changes what the
     benchmark rewards more than the task itself.
  4. Calibration under drift: deaths fall from 11-12% in training to 8-10% in the test windows; unscored by AUC.
  5. Target is death, not deterioration (2): right for prognosis and beds, a proxy for the referral decision.
  6. Retrospective forms (7.5%): kept on purpose, measured +0.002; a naming fix in fit_reason only.
  7. Antigen/X-ray results known on the admission day for a third of patients, dropped: +0.0006, negligible.

WHAT AN EXPERT IN THE DOMAIN WOULD CHANGE
  a. Metric: log_loss instead of roc_auc (or, if roc_auc stays, origin `source` after checking Baqui).
  b. Drop race_colour, indigenous_ethnicity, traditional_community, traditional_community_type (curator call).
  c. Add the ICU-on-admission-day flag, or name the 20.5% in fit_reason and the use case.
  d. fit_reason: keep the form-only gap; move the retrospective forms into a "kept" clause; say the score pools
     children and adults (61% / 39% of test rows).
  e. Notes: say death is any in-hospital death, a proxy for deterioration for the referral decision; say the
     surveillance team cannot act on these rows in time (typed a median 4 days after admission, 42% of deaths
     before typing), so the actor is the hospital or its regulator.
  f. Keep: admission as the prediction point; the 2023 history; code 3 as death; the vaccine-date gating; the
     one-month gap; the half-year windows; the hospital as an input (LEAK-34).

MEASUREMENTS (mine; scripts and logs in )
  Frame: the definition's `_clean` output with raw helper columns (copied from the claim auditor's build, 922,908
  rows; row alignment to the prepared raw verified 100%). Splits rebuilt from admission_date with the declared
  cutoffs and gap; test sizes 167,794 / 130,431 / 139,737 match the README.
  d01_describe.log: fill rates; race and schooling death rates; ICU day 0 20.5% (74% of ICU, 37% of deaths); deaths
    within 1 day of admission 15.6%, within 2 days 22.6%; median 8 days to death; notification median 1 day (43%
    same day); typing median 4 days, p90 28; 42.4% of deaths before typing; composite 20.3%; code 2 vs 3 profiles.
  Age bands (all rows): <=1 year 35.1% of rows / 5.5% of deaths; 1-4 13.3% / 1.5%; 5-17 10.3% / 2.3%; 18-39 5.5% /
    6.1%; 40-59 8.4% / 15.9%; 60-74 12.4% / 29.0%; 75+ 15.1% / 39.7%.
  d02_models.log (LightGBM 500 trees, no text, no date; mean of 3 windows): all 0.8819 AUC / 0.2179 log loss /
    within-hospital 0.8536 / ward-only 0.8896 / 60+ 0.7344 / top-10% precision 0.432, recall 0.466; mean predicted
    0.1043 vs observed 0.0932. no_race 0.8817 / 0.2180; no_social 0.8800 / 0.2194; no_hospital_place 0.8758 /
    0.2208 (within-hospital 0.8524).
  d03_admission_extras.log (mean of 3 windows): shipped 0.8819 (adults 0.7587, children 0.8045); +antigen+xray
    0.8825; +icu_day0 0.8901 (adults 0.7763); all three 0.8910; log loss 0.2179 / 0.2174 / 0.2121 / 0.2113.
  Raw check: antigen result dated on/before admission day 31.7% of rows, PCR 9.1%, X-ray 36.4%, antiviral 6.3%.

SOURCES
  - Ministério da Saúde, SRAG 2019-2026 dataset page and data dictionary (via the builder's notes and raw files).
  - Baqui P. et al. 2021, Sci Rep 11:15591, full text via Europe PMC (PMC8329284): use "policy makers ... hospital
    management and healthcare network organization"; ethnicity among inputs; models ranked by AUC-ROC; a
    calibration figure. https://www.ebi.ac.uk/europepmc/webservices/rest/PMC8329284/fullTextXML
  - Marcolino M.S. et al. 2021, ABC2-SPH score, Int J Infect Dis (search summary): 7 admission predictors.
  - Gupta R.K. et al. 2021, ISARIC 4C Deterioration model, Lancet Respir Med 9:349-359 (search summary).
  - Lei 8.080/1990 art. 7 IV (Câmara/Planalto texts via search); Lei 12.288/2010 arts. 7-8
    (https://www.planalto.gov.br/ccivil_03/_ato2007-2010/2010/lei/l12288.htm, via search); Portaria GM/MS 344/2017
    (state/municipal copies via search); LGPD Lei 13.709/2018 arts. 5 II, 6 IX, 11; Código de Ética Médica, Res. CFM
    2.217/2018 principle I (cfm.org.br comparison table via search); Res. CFM 2.454/2026 (news summaries).
  - AMIB/ABRAMEDE/SBGG/ANCP, Protocolo de alocação de recursos em esgotamento durante a pandemia por COVID-19, 2020
    (search summary only; the PDF could not be read here).
  - Ministério da Saúde, Nota Técnica nº 11/2026-CGCOVID/DEDT/SVSA/MS (search summary: SARI notified within 24 h).
  - The rais_employment_separation domain report of this batch (the stance on Lei 9.029/1995).
  Not read: the Ministry's 2024 surveillance guide; the full AMIB protocol and Res. CFM 2.454/2026 texts.

RULES CITED
  USE-1, USE-3, USE-5, USE-6, USE-8 (and its amendment on kept leaks and on selection), USE-9 (and the weighed factor
  against it), USE-10; principles.md tension row "a factor the actor may no longer use"; LEAK-10, LEAK-22, LEAK-34;
  SPLIT-20, SPLIT-21; MET-1, MET-2, MET-5, MET-6, MET-7, MET-8, MET-9, MET-10, MET-11.

</details>

<details><summary>Blind review</summary>

BLIND REVIEW: sivep_gripe_sari_outcome (target died_in_hospital, binary, 922,908 rows x 65 cols, temporal split on admission_date)
Inputs used: clean_room/data.parquet (200k-row sample), clean_room/task.md, the public portal page, the data dictionary PDF,
and the public source files INFLUD23/24/25/26 parquet (downloaded from the S3 links on the portal, snapshots 23-03-2026 and 09-11-2026).
No other local files were opened.

VERDICT: Include with changes. The task is real, it has clear signal and is not trivial, and the target was built correctly.
The things to fix are mostly preparation work: retrospective notifications, censoring in the last test window, a few
free-text strings that give away the outcome, the hospital ID, and the date column.

WHAT THE TASK IS
Brazil's national severe acute respiratory infection (SARI/SRAG) surveillance system (SIVEP-Gripe). Each row is one hospitalised
SARI case from 2023-01-01 to 2026-06-30. The features come from the notification form: demographics, symptoms, comorbidities,
vaccination, geography and hospital. The target is whether the case ended in death. The use case: predict in-hospital
mortality when a SARI patient is admitted, for clinical or surveillance risk stratification (triage, ICU and resource
planning, identifying high-risk groups). This is a credible use, and SIVEP-Gripe mortality models are common in the
literature (for example, PeerJ CS 2916 on paediatric COVID).
Post-admission fields (ICU, ventilation, lab results, final classification, antivirals, notification and outcome dates)
were correctly left out.

CHECKS THAT PASSED
- Target reproduced from the source. EVOLUCAO is 1 Cura, 2 Obito, 3 Obito por outras causas, 9 Ignorado.
  died_in_hospital = EVOLUCAO in {2,3} among rows with EVOLUCAO in {1,2,3}.
  Monthly death rates match the source closely (2023-01: 0.184 sample vs 0.182 source; 2026-06: 0.069 vs 0.071).
  The source window gives 920,459 closed rows vs 922,908 claimed (0.3% gap, probably from a different snapshot).
- Overall prevalence is 10.8%; the last test window is about 8%.
- Signal. I ran LightGBM on 3 expanding windows (test 2025H1, 2025H2, 2026H1; my own boundaries).
  * Age alone: AUC 0.808 / 0.804 / 0.823.
  * Six simple features: AUC 0.82-0.84.
  * All non-text features: AUC 0.868 / 0.870 / 0.874, AP 0.44 / 0.40 / 0.39.
  * Dropping hospital and geography costs about 0.01 AUC and 0.05-0.08 AP.
  So there is real headroom beyond age, and nothing is near-perfect.
  Top features by gain: age 0.26, hospital 0.24, residence municipality 0.09.
- No exact or feature-level duplicate rows in the 200k sample.
- No single column separates the classes almost perfectly.

CONCERNS, MOST TO LEAST SERIOUS

1. Retrospective notifications: rows whose features were recorded after the outcome was known.
   Source check (admissions in the window, closed outcomes):
   - 7.5% of rows have DT_NOTIFIC later than DT_EVOLUCA. Their death rate is 17.7%, vs 10.0% for the rest.
   - 13.5% of deaths were notified after death, vs 6.9% of discharges.
   Some facilities seem to report mainly fatal cases. Two hospitals with n>=200 in the sample have death rates of 0.79
   (HOSPITAL MUNICIPAL ANTONIO GIGLIO, Osasco) and 0.70 (SMS HOSPITAL MUNICIPAL RONALDO GAZOLLA, Rio).
   Among patients 60+, hospital death rates range from 0.04 to 0.50 (5th to 95th percentile).
   So whether a row exists, how complete its fields are, and part of the hospital effect depend on the outcome. A model
   used at admission would never see these rows in this form.
   Fix: drop rows notified after the outcome date, or more than about 7 days after admission (DT_NOTIFIC is in the source),
   or at least document the issue. I would apply this filter.

2. Censoring in the last test window: open cases are dropped.
   Rows with EVOLUCAO missing or 9 were excluded, as they must be, but the open share rises at the end of the series:
   - Missing outcome: 7.4% in 2026Q2, vs 2.4-6.2% in earlier quarters.
   - Missing plus ignored: 9.3%, vs about 6%.
   - Excluded open cases are older: 31.5% aged 60+, vs 28.0% among closed cases.
   This is on the 09-11-2026 snapshot; the preparer's snapshot was probably a few days older.
   The drop in prevalence (0.106 to 0.094 to 0.082 across the three windows) is mostly case mix (more infants with RSV).
   For EVOLUCAO=2, the 60+ death rate stays about 0.15-0.16. So the bias is small but goes in a known direction.
   Fix: end admissions about 4 months before the snapshot (for example at 2026-03-31), or require a minimum follow-up.
   Record the snapshot date in task.md.

3. Free-text columns give away the outcome in some rows.
   The columns are other_symptoms_text, other_risk_factors_text and other_animal_text: raw Portuguese, cut at 30
   characters, with 16,437 / 14,106 / 92 distinct values.
   Examples: "ADMITIDO EM OBITO" (Yes), "OBITO/ABDOME AGUDO" (Yes), "PCR" (= parada cardiorrespiratoria;
   52 rows, 67% died), "TOT"/"IOT"/"VM" (intubation or ventilation; 17-19 rows each, 53-76% died).
   That is about 100 of 200k rows. Treating the text as a category gave no AUC gain, so the effect on scores is tiny,
   but these are outcome or treatment statements, not admission features.
   Fix: drop the three text columns, or replace them with a few curated keyword flags that exclude
   outcome and treatment terms.

4. Preparation and column problems:
   a. admission_date (datetime64) is both the split key and a feature. As a raw date it cannot extrapolate across a
      temporal split (window-1 AUC 0.8626 with the date as an ordinal vs 0.8676 without), and many pipelines handle
      datetimes badly.
      Fix: remove it from the features, or derive month or epidemiological week (seasonality matters: RSV, flu, COVID).
   b. hospital is a name, not an ID. 109 names appear in more than one municipality ("HOSPITAL SAO LUCAS" in 18,
      "HOSPITAL SAO JOSE" in 16), affecting 17,156 sample rows (8.6%).
      Fix: key it as name + municipality code.
   c. Geography is highly redundant: 11 columns (notification, residence and hospital state, region and municipality,
      plus country), with up to 4,985 levels.
      Fix: keep them but document, or trim the notification_* copies (notification and hospital municipality differ
      in only 4.3% of rows).
   d. Near-empty columns:
      - Missing for almost everyone: bmi 99.9% NA, occupation 99.6%, indigenous_ethnicity 99.5%,
        traditional_community_type 99.5%, other_animal_text 99.7%.
      - Structurally missing for most rows: mother_flu_vaccinated 97.8% and breastfed 96.7% (infant-only fields).
      Fix: drop the first group; keep the second.
   e. Small value errors:
      - age_years has min -0.33 (1 row) and 22 values above 105.
      - days_onset_to_admission is clipped to +/-365 (1,847 rows negative; these are mostly nosocomial cases, which
        is legitimate).
      - days_since_flu_vaccine reaches 3,361 days, and 917 rows have flu_vaccine_last_campaign="No" while a flu
        vaccine date is present.
      - residence_country includes "ILHAS SANTA HELENA".
      All minor.
   f. "Ignorado" (9) is merged with blank into NaN. That is reasonable, but the missingness carries signal:
      comorbidity flags are about 65-70% NaN because the form skips them when FATOR_RISC=No; death rate is 0.06 when
      NaN vs 0.20 when filled. This is expected and not leakage, but it should be documented. FATOR_RISC itself is
      not included and would be a cleaner encoding.

5. Duplicate notifications.
   In the source, 1.0% of in-window rows fall in groups sharing birth date + sex + residence municipality + admission
   date (4,531 groups), and 96% of those groups have the same label. In the sample, 622 groups share admission date,
   age, sex, residence and hospital (97% same label).
   Under a temporal split they mostly stay inside one window, so the impact is small.
   Fix: deduplicate on (DT_NASC, CS_SEXO, CO_MUN_RES, DT_INTERNA, hospital) before splitting.

6. Vaccination fields come partly from a registry linkage ("Integração com a Base Nacional de Vacinação").
   0.2% of rows have a COVID dose dated after admission (death rate 2% vs 10.6%), and 0.66% have a last flu dose
   after admission.
   days_since_* look clipped at 0, but I cannot tell whether covid_vaccine_doses counts post-admission doses.
   Fix: count only doses dated on or before admission. The effect is tiny.

7. Licence.
   The portal footer says: "Todo o conteúdo deste site está publicado sob a licença Creative Commons
   Atribuição-SemDerivações 3.0" (CC BY-ND).
   A translated, recoded table is arguably a derivative. Check this before redistributing the prepared file;
   shipping a download-and-prepare script avoids the issue.

8. Target scope (documentation only).
   died_in_hospital includes "Obito por outras causas" (EVOLUCAO=3), which is about 28% of deaths. That fits the
   all-cause name. State it in task.md, along with the exclusion of EVOLUCAO 9 and blank (about 6.5% of in-window
   admissions).

WHAT I COULD NOT CHECK
- The exact 3 test-window boundaries; I used my own half-year windows.
- The preparer's snapshot date and code; the 2,449-row gap to my source count is unexplained.
- Person-level linkage: there is no ID, so repeat admissions of the same patient across train and test cannot be
  confirmed. Birth date + sex + residence is not unique for infants.
- Whether a row's features were edited after admission (the source has no audit trail beyond DT_DIGITA).
- The full set of outcome-revealing free-text terms (keyword search only).
- The binding licence terms for the dataset itself, as opposed to the site footer.

</details>

<details><summary>Task gamer</summary>

TASK GAMER REPORT - sivep_gripe_sari_outcome (died_in_hospital, ROC AUC, 3 temporal test windows)
Kit: (the run folder)
Scripts and outputs: work/ (s01..s23). Every score is from score.py on the shipped splits (r0f0 = 2026-01..06, r1f0 = 2025-07..12, r2f0 = 2025-01..06).

VERDICT
The task can barely be gamed: with all exploits stacked, the gain is +0.0026 AUC over a strong honest model (+0.0017 to +0.0032 per split). The largest single exploit (+0.0015) rebuilds persons from exact vaccine dates and uses a later readmission as proof of survival. No row-order, copy, id, transform or post-outcome column leak exists.

BASELINES
- Untuned LightGBM (100 trees, 31 leaves; categoricals native, admission_date as day ordinal + month), work/s01_baseline.py:
  r0 0.88902 | r1 0.88306 | r2 0.88110 | mean 0.88439. (200 trees x 63 leaves overfits the high-cardinality categoricals: mean 0.87878.)
- Noise: an added random column is never split on (scores identical to the 5th decimal). Spread over 4 bagging/feature-fraction seeds
  (work/s14b_seed_noise.py): SD 0.0002-0.0003 per split, range 0.0005-0.0007.
- Stronger honest model: high-cardinality columns as integer codes + out-of-fold target encodings fitted on train rows only, 600 trees,
  lr 0.05 (work/s18_honest_te_window.py): r0 0.89168 | r1 0.88568 | r2 0.88403 | mean 0.88713.
  Adding past-only features a deployed model has (hospital/state admission counts over the previous 14-90 days, days since this person's
  previous admission): mean 0.88760 (0.89224 | 0.88674 | 0.88383). This is the reference "strong honest" score below.

EXPLOITS RANKED BY GAIN

| # | Exploit | Script | Honest score | Exploited score | Gain (per split) | A deployed model has it? | Fix |
|---|---|---|---|---|---|---|---|
| 1 | Future readmission of the same person: rebuild persons from the absolute last-dose date (admission_date - days_since_covid_vaccine / days_since_flu_vaccine) + sex + integer age + residence municipality (+ dose count, race). A later admission of the same key means this one was survived. | s12_person_key_vaccine_date.py, s13_readmission_model.py, s21_exploits_vs_strong.py, s23_readmit_ablation_and_fix.py | strong 0.88760; baseline 0.88439 | strong 0.88906; baseline 0.88494 (vaccine keys only 0.88521) | strong +0.0011/+0.0020/+0.0012 (mean +0.0015); baseline -0.0003/+0.0010/+0.0010 | No: it needs admissions after the prediction point | Round days_since_covid_vaccine and days_since_flu_vaccine to 30-day bins. Tested: baseline 0.88446 (no honest loss), and the rebuilt-key features then add exactly 0. |
| 2 | Test-row statistics with the future: admission counts per hospital/state/day over windows that include later days (+-3, +-15 days, next 30/90 days), hospital-month case mix and volume over all rows incl. test. | s11_test_row_stats.py, s21 | strong 0.88760 | 0.88835 | +0.0009/+0.0006/+0.0007 (mean +0.0008) | Partly. Past-only counts are legitimate and give most of the gain over the baseline (+0.0009 of +0.0013); only the future-including part is an exploit. | None needed beyond accepting it; it is inherent to scoring a whole test window at once. If wanted: score in shorter test blocks. |
| 3 | Format/missingness features: per-column missing flags, number of filled fields, decimals, text length/commas. | s15_formats.py, s21 | strong 0.88760; baseline 0.88439 | 0.88802; 0.88489 | strong +0.0005/+0.0002/+0.0006; baseline +0.0001/+0.0008/+0.0006 | Mostly yes: missingness here mostly encodes meaning (comorbidity block filled = "has a risk factor", fractional age = infant). Part is filled after the outcome (see flaw A), but the gain is within ~2 SD of seed noise. | None worth making. |
| - | All three stacked | s21 | strong 0.88760 | 0.89017 | +0.0017/+0.0032/+0.0029 (mean +0.0026) | - | - |

Lookup in the published source works (not ranked, not a task flaw): matching r0 test rows to INFLUD26 on admission date + hospital
municipality + residence municipality + sex + onset-to-admission days joins 98.1% of rows; using EVOLUCAO gives AUC 0.99862 (s22_source_lookup.py).

FINDINGS: MECHANISM AND FIX

1. Future readmission (vaccine dates are a quasi-identifier). days_since_covid_vaccine and days_since_flu_vaccine are exact to the day. Added to
   admission_date they give the person's vaccination date, and with sex/age/municipality that nearly identifies a person. Rows whose rebuilt
   person is admitted again 8-30 days later died in 5.4% of cases; rows with an earlier admission in the same gap died in 14.1%
   (key cov_flu_race). 31-90 days: 4.6% vs 13.4%. The death rate of vaccinated rows overall is 18.9%. Demographic-only keys (no vaccine date) are
   symmetric and add nothing (mean 0.88406). The prepared kit already drops DT_NASC and NU_NOTIFIC from the source. The vaccine day counts bring
   the person key back in. Fix: bin both columns to 30 days. Then the asymmetry goes (next copy 8-90 d: 13.4% for the covid key, 9.9% for
   cov_flu_race), the honest baseline is unchanged (0.88446 vs 0.88439), and the exploit adds 0.

2. Future-including counts. Counts over windows that reach into later days add +0.0005 on their own (h_fut30, h_fut90, st_fut14: 0.88492).
   Past-only counts add +0.0009 (0.88529). Over the strong honest model, which already has the past counts, the future part adds +0.0008.
   Any batch test window allows this. It sits at about 3 SD of seed noise.

3. Formats. Format-only features alone reach AUC 0.797 (missing flags alone 0.788). But that is the meaning of the missingness (age band,
   risk-factor yes/no, vaccine yes/no), not a recording artefact: added to the values they give +0.0004 to +0.0005.

TASK FLAWS THAT INFLATE OR DISTORT THE SCORE FOR EVERY MODEL (no participant gain, no harm to an honest model)

A. Part of each "at admission" record is filled after the outcome. In the source (INFLUD26), joined uniquely to 78.5% of r0 test rows, 12.8% of
   test rows were notified on or after the outcome date (DT_NOTIFIC >= DT_EVOLUCA). Their death rate is 0.136 vs 0.077, and they are easier
   to rank: baseline AUC 0.918 on them vs 0.881 on rows notified before the outcome (0.886 on all joined rows). Across the source window, 21% of
   deaths vs 13% of survivors were notified after the outcome. Consistent with this, occupation is filled about 2x as often for adults who
   died (e.g. 40-60 y: 2.7% vs 1.3%), and other_risk_factors_text 2.5-3x as often for children who died. Their drop-column value is small
   (occupation -0.0002, all free text -0.0015, schooling -0.0011). The kit has no notification date, so no participant can exploit it, but
   the headline AUC overstates at-admission performance by about 0.004 on r0.
   Fix: in preparation, drop rows with DT_NOTIFIC >= DT_EVOLUCA (or keep only rows notified within a few days of admission).
B. Outcome-missing rows are dropped, and they are not random. 8.5% of 2026-H1 admissions in the source have EVOLUCAO missing (6.6%) or
   ignored (1.9%). The missing share rises from 4.2% (Jan) to 7.7% (Jun). These rows are sicker than survivors (ICU 0.30 vs 0.25, invasive
   ventilation 0.11-0.19 vs 0.07), so some deaths are missing from the labels of the latest window. A month-level oracle offset fitted on test
   labels adds only +0.0001, so this cannot be exploited and barely shifts rankings. Fix: note it, or end the last test window a few months
   before the extract.
No honest-hurting flaw was found: training on the last 24 or 12 months scores lower than all history (0.88671, 0.88404 vs 0.88713). Old training
rows help.

ATTACKS THAT FOUND NOTHING (number = what was measured)
- Row order: the data is sorted by admission_date and shuffled within each day. Within-day position AUC 0.4996 (per split 0.5037/0.4951/0.5037).
  Next-row label agreement 0.8113 vs 0.8099 expected. Within-day columns are not sorted (non-decreasing share 0.50-0.56). (s03_order.py)
- Exact copies: 0 rows identical on all features. 7,013 rows identical except the date, death rate 0.006 (common infant profiles, not
  persons). No train/test copy is possible across the one-month gap. (s05_dups.py)
- Previous admission (legitimate history), demographic keys: -0.0001. (s13)
- In-stay words in free text (IOT/intubation, VM, TOT, PCR/parada, UTI, shock/DVA, obito, palliative, sepsis, dialysis, coma): about 1,800 rows
  in total, death rates 0.35-0.69, model gain -0.0001 (0.88426). (s15)
- Numeric formats: age_years is in months/12 for infants and days/360 for neonates (meaning, legitimate). days_onset_to_admission is clipped
  to +-365, whole numbers. Vaccine days are >= 0 (no post-admission doses). bmi has 50% whole numbers with the same death rate. No sentinels
  carry the label. (s08)
- Category level order: alphabetical (schooling ordinal). Code-vs-rate correlation is about 0 for high-cardinality columns. No transform over
  all rows; no standardised or ranked columns. (inline check)
- Train-vs-test classifier: AUC 0.91-0.97, driven by vaccine recency, hospital and the flu-vaccine field (expected drift). Adversarial score vs
  label inside test: 0.59-0.66, already explained by age/vaccine. (s16)
- Month-level test composition: the baseline is calibrated per test month. An oracle per-month offset adds +0.0001, so no test-window
  statistic at month level can help. (s09) A per-hospital oracle offset adds about +0.022 (upper bound using test labels). The real
  hospital-month stats recover about +0.001 of it. (s10, s11)
- Single features: age 0.81, hospital 0.74, vaccine doses 0.73. Nothing post-outcome comes close to the full model. (s02)
- Drop-column: no column is worth more than 0.0055 (hospital ids). Occupation 0.0002, has_cpf 0, bmi 0, date 0. (s19)
- Web: no competition, leak thread or "magic feature" exists for this source. The obvious post-outcome fields (UTI, SUPORT_VEN, DT_EVOLUCA,
  DT_ENCERRA, DT_DIGITA, CLASSI_FIN, lab results) are absent from the kit, as are DT_NASC and NU_NOTIFIC.

NOT CHECKED
- The source files for 2023-2025 (only INFLUD26 was downloaded). Flaw A was measured on r0 only.
- The data dictionary PDF could not be rendered (no PDF tools), so field semantics come from the source column names.
- Text features beyond keywords (e.g. TF-IDF of the free text): honest signal either way, not an exploit.

SOURCES
- https://dadosabertos.saude.gov.br/dataset/srag-2019-a-2026 (INFLUD26-09-11-2026.parquet downloaded to work/src/)
- Web searches on SIVEP-Gripe mortality modelling and leakage found no competition or leak thread, e.g.
  https://www.frontiersin.org/journals/medicine/articles/10.3389/fmed.2025.1558264/full and https://peerj.com/articles/cs-2916

</details>

<details><summary>Precedent check</summary>

PRECEDENT CHECKER: sivep_gripe_sari_outcome (folder sivep_gripe_sari_outcome), 2026-11-09

Read: principles.md (Consistent judgement, Exceptions and amendments, Tensions), leak_checks.md (LEAK-10 with its
three clauses, LEAK-22, LEAK-39), splits.md (SPLIT-20, SPLIT-21 and their Cases rows), use_case.md (USE-3, USE-5 to
USE-7), provenance.md (PROV-9), cleaning_features.md (CLEAN-12), metrics.md (MET-5, MET-8), evidence.md (EV-4); the
definition and the record; builder_report.md, claims.md, probes/retro_forms.json; the register (register.json, 34
flags; none is about this dataset's calls: the USE-5 opposite-outcomes pair is xente/diabetes_3/chicago, the
"post-outcome feature" drift is keyword noise); sinan_dengue_case_screening_1m/REVIEW.md and dataset.py;
rais_employment_separation_1m/REVIEW.md (issues 1 and 5) and dataset.py; enem_entrance_exam_scores_1m/REVIEW.md issue
1; acs_food_stamps_2014_2024_1m, wioa_employment_after_exit, nchs_linked_birth_infant_death_1m and
kumc_inpatient_aki_prediction (dataset.py, kumc REVIEW.md issue 1); the records' CC lines; the blind reviewer's report
(the only other phase-A report present when this was written).
Paths below are relative to W=(the run folder)
Measurements: pc1_checks.py (.log), pc2_texts.py (.log), pc3_hospital_death_texts.py (.log),
each running the definition's own _load_raw and _clean on the prepared raw file (922,908 rows, as the notes say).
No curator decision exists yet on any dataset of this batch (every batch record has only its 2026-11-08 accept CC):
batch siblings are AI recommendations, cited as such.

SUMMARY

| # | Call | Reading |
|---|---|---|
| 1 | History from 2023 (SPLIT-20, SPLIT-21) | consistent (aeolus) |
| 2 | Death from other causes counted as death (USE-5, LEAK-22) | consistent (all-cause targets); framingham is the contrast, not a precedent against |
| 3 | 7.5% late forms kept (LEAK-39, USE-3) | departs from sinan's remedy with stated facts that set it apart: consistent |
| 4 | Vaccination rule | counting before admission consistent; the blank of "vaccinated" not reasonable under the ranking (it encodes survival: LEAK-10, Must) |
| 5 | 660 free texts naming ICU kept with a note | departs without a stated reason (LEAK-10 clause 2 practice); the few texts naming the patient's death are not keepable (Must) |
| 6 | Race or colour kept | consistent in substance with the clinical precedents; departs in method from the batch (the actor's own norm not asked or written); an ICU-admission norm may reach race, sex and age |
| 7 | Occupation "title [CBO code]" | consistent with CLEAN-12; set apart from sinan and rais (codes now) by a fact: the words are in the rows |
| 8 | Fallback roc_auc | consistent |
| 9 | Year 2026 (PROV-9) | consistent; sinan's 2023 set apart by a fact |
| E1 | Hospital by name only | departs without a reason from the definition's own municipality reasoning (130 names in more than one municipality, 8.99% of rows) |
| E2 | Licence | the same portal, two readings (sinan CC BY-ND 3.0, sivep CC BY): a metadata note, never an issue (EV-4) |

1. HISTORY FROM 2023 (SPLIT-20 Should, SPLIT-21 Must) -> CONSISTENT

Closest precedent: aeolus (Lennart, 2026-10-12; curation/records/aeolus.md CC line; splits.md Cases row "SPLIT-20,
SPLIT-21 | aeolus"): "History from 2023 on: TabReD's random sample of all nine years ... mixed in COVID-19 ... a model
refit every two weeks trains on recent data ...; the test-week comparison of history pools ... did not decide it."
aeolus_rebuilt_1m carries the same HISTORY_START = 2023-01-01 "after COVID-19". The sivep call has the same shape: the
paper the use case follows trained on 2020 (Baqui et al., 231,112 PCR-positive patients of February-September 2020, per
the screening), the definition departs from it for a break in the source, and the choice rests on the break, not on
scores (SPLIT-21 holds: issue 1 says so).
The break is stronger than aeolus's: the register's population changed (COVID-19 61%-83% of a quarter's cases and
25%-34% deaths in 2020-2021, against 1%-29% and 7%-15% since 2023), the clinical closing criteria for COVID-19 were
dropped on 2022-10-31 (dictionary field 81), and the volume fell from 1.2M-1.7M to 0.27M-0.34M a year.
Batch contrast (AI, undecided): chile_school_dropout_mineduc_1m, enem_entrance_exam_scores_1m and
nchs_linked_birth_infant_death_1m keep their COVID-19 years in the history; a fact sets them apart: their cohorts are
defined the same way through the pandemic (fewer dropouts, more absentees, a slightly lower infant death share), while
SIVEP-Gripe's case mix and closing rules changed. nyc_motor_vehicle_collisions starts its history at a reporting-rule
change (NYPD, 2020-04-06), the same kind of cut as here.
One line to carry: the accept reason of 2026-11-08 ("tables with 2M+ rows") no longer holds with 922,908 rows; sinan
wrote such a line (its mediator's C9: "the accept reason 'most rows' changed"). Issue 1 states it; the record judgment
should too.

2. DEATH FROM OTHER CAUSES COUNTED AS DEATH (USE-5 Must; LEAK-22 Must) -> CONSISTENT

The only curator precedent on the mechanism is framingham_heart_study_fhs (Lennart, 2026-10-22; LEAK-22's text):
"participants who died of other causes within 10 years stay No". There the target is a cause-specific event (10-year
CHD), so another death is a competing event. Here the target is death in hospital of any cause; for an all-cause
target no competing event exists, and LEAK-22's sentence does not apply. The all-cause in-hospital or short-horizon
death targets of the working copy count every death: sepsis_survival_minimal_clinical_records (alive or dead at the
end of the stay), 2_month_survival_rate_prediction (SUPPORT, death of any cause), nchs_linked_birth_infant_death_1m
(batch, AI: infant death of any cause). The call is USE-5's (what the team acts on), and the definition follows these.
The blind reviewer reproduced the target and agrees (its point 8).
For issue 2's text: the framing "USE-5 vs LEAK-22" overstates a conflict. Its Consistency bullet should name
framingham as the contrast (a cause-specific target) and the all-cause precedents as followed; the issue is then a
confirmation of the target, low stakes.

3. THE 7.5% OF FORMS FILLED AFTER THE OUTCOME, KEPT (LEAK-39 Must; USE-3 Must) -> DEPARTS FROM SINAN'S REMEDY WITH
   FACTS THAT SET IT APART: CONSISTENT

Is it sinan's case? No, by three facts:
- sinan's prediction point is the notification itself, and its filter (sample collection dates before the notification
  date, 370,314 rows, 14.1%) reads facts dated before that point, so it reads no label (sinan mediator C1; the USE-7
  precedents nyc_taxi_trip_duration_1m and pkdd_15, Lennart 2026-10-26: "the cut rests on the inputs"). Here the
  prediction point is the admission, and every filter reads a fact after it: the outcome date (blank for 7.2% of the
  discharges against 0.4% of the deaths, a selection by the outcome; framingham's "dropping it selects the cohort on
  the future", Lennart 2026-10-22), or the notification delay (the blind reviewer's "more than about 7 days after
  admission": label-free, but a fact of the stay; not measured by anyone).
- sinan's late rows lifted the score by 0.004 to 0.031 (its column auditor); here the late forms lift the overall test
  score by 0.002 and training without them changes the routine rows by 0.0001 (0.8731 against 0.8732,
  probes/retro_forms.json).
- LEAK-39's drop needs a route that "too few rows of the other class went through ... to calibrate it" (gallstone_disease,
  Andrej 2026-10-26: 72 cases against 5 controls). This route holds 7.4% of the discharges and 13.6% of the deaths (death
  rate 17.8% against 10.7%): both classes in tens of thousands of rows. The drop condition fails.
Further precedent for a keep with a note: south_africa_coronary_heart_disease (Lennart, 2026-10-01: risk factors
measured after the heart attack kept with a comment, since they weaken rather than leak the signal).
Open for the mediator, not a precedent departure: the blind reviewer would drop these rows, and reports hospitals whose
sampled rows die at 0.70-0.79, which may notify mostly deaths (a row's existence set by its outcome at some hospitals,
USE-8). If issue 3 offers the delay filter as an option, it needs its own measurement first (EV-1).

4. THE VACCINATION RULE -> COUNTING CONSISTENT; THE BLANK NOT REASONABLE UNDER THE RANKING (LEAK-10, Must)

Counting only the doses dated on or before admission is the as-of reconstruction LEAK-10's second clause asks for.
The blank is where it departs. The clause's blank precedents (zillow_prize and melbourne_housing_market, Lennart
2026-10-21; aeolus_1m's weather after departure) blank cells located by a date that every row of a period shares (a
lookup date, the departure time), so the blank carries no outcome. Here the blanked cells are located by a dose dated
after admission, which a patient who died in hospital rarely has, so the blank marks survivors.
Measured (pc1_checks.log):
- covid_vaccine_doses = 0 with covid_vaccine blank: 914 rows (913 blanked by the definition), 5 deaths (0.55%), against
  3.74% for the 429,566 rows with 0 doses and "No", and 10.6% overall. The pair (0 doses, blank) occurs essentially only
  on those rows: a survivor fingerprint.
- Influenza: 5,615 rows blanked, 1.73% deaths, inside 289,468 missing rows at 10.99% (11.17% without them): a diluted
  version of the same marker.
LEAK-10 lists "missingness that encodes the outcome" as out; a Must, so there is no exception, and the remedy is a fix:
the as-of value. The definition's own count already says 0 doses at admission, so "vaccinated" as of admission is "No"
(and the influenza "Yes" whose last dose, DT_UT_DOSE, is dated after admission is "No" for the campaign as of
admission, or the column's blanks are made alike). Size: 0.1% of the rows, so a cheap fix with no measurable score change; Musts carry no
size threshold.

Consistency check: Set "vaccinated" to its value at admission instead of blanking it where every dated dose is after admission?

**Problem:**
- The blank is the remedy of LEAK-10's second clause, but its precedents blank cells located by a date every row of a period shares; here the cells are located by a later dose, which survivors have, so the blank marks them[l10v].
- 914 rows carry 0 COVID-19 doses with "vaccinated" blank; 5 died (0.55%), against 3.74% of the 429,566 rows with 0 doses and "No".
- The influenza blank (5,615 rows, 1.73% deaths) is the same marker, diluted among 289,468 missing values.

| | Option | What it does | Pro | Con |
|---|---|---|---|---|
| a | The value at admission (recommended) | "vaccinated" becomes "No" where every dated dose is after admission; the influenza "Yes" whose last dose is dated after admission becomes "No" | matches the definition's own dose count; no marker left; one line in `_clean` | reads the dose dates as complete |
| b | Blank the count too | `covid_vaccine_doses` and the days since the dose become missing on those rows | no value asserted | the rows join the 60,981 without a count (5.2% deaths) and lower it a little: a weaker marker |
| c | Keep the blank | as implemented | none beyond no change | missingness that encodes the outcome, a Must: no exception available, only an amendment of LEAK-10 |

**Recommendation:** a: it is the as-of value the definition already reconstructs for the doses. **Decision:** a, b or c?

[l10v]: **LEAK-10** (Must; amended 2026-11-08): out is "missingness that encodes the outcome"; its second clause: "a value read at a later pull goes where its late cells can be located: they are blanked (zillow_prize, melbourne_housing_market, aeolus_1m's weather after departure)".

5. THE 660 FREE TEXTS NAMING ICU OR INTUBATION, KEPT WITH A NOTE -> DEPARTS WITHOUT A STATED REASON

The practice of LEAK-10's second and third clauses: a value recorded later is blanked where its cells can be located
(zillow_prize, melbourne_housing_market, Lennart 2026-10-21; noaa_storm_events_damage, Lennart 2026-11-08: "blank what
features locate ... the size of the worth alone never decides"); it stays with a note only when the traced part shows
no gain (onlinenewspopularity, Lennart 2026-10-26; medical_facility_operational_data, Lennart 2026-11-05; in this batch
kumc_inpatient_aki_prediction traced its comorbidities and medical groups before proposing its keep, kumc REVIEW.md
issue 1). The sivep note gives only the size ("0.07% of the rows, kept"), the one argument the clause rules out.
Measured (pc2_texts.log, pc3_hospital_death_texts.log; keyword search over the symptom and risk-factor texts):
- naming ICU, intubation or ventilation (UTI, CTI, IOT, TOT, VM, intubação): 443 rows, 40.2% deaths (10.6% overall);
- with cardiac arrest and death words added (a loose pattern: "PCR" also means the test, "OB" also nasal obstruction):
  820 rows (0.09%), 44.1% deaths; 113, 97 and 103 of them in the three test windows. (The builder's 660 texts come from
  its own pattern; the order of size is the same.)
- a handful name the patient's own death or brain death: "ADMITIDO OBITO", "ADMITIDO EM OBITO", "OBITO/ABDOME AGUDO",
  "PROTOCOLO (DE) MORTE ENCEFALICA" (the blind reviewer found the same). These are the target ("a part, a consequence or
  another encoding of the target", LEAK-10, Must): not keepable with a note under any reading;
- many name the state on arrival ("CHEGA EM VM / IOT", "CHEGOU NA UPA EM PCR", "RECEBIDO EM PCR- PS -UTI"), known at
  admission; the risk-factor texts mostly name earlier stays ("UTI NEO", "PREMATURIDADE") at 12.8% deaths.
No measured fact in the notes sets the keep apart. Best guess at one: the texts are typed at notification, and an
intubation named there cannot be told from an arrival state row by row, so the late part cannot be located.

Consistency check: Blank the free texts that name the patient's death, intensive care or intubation during the stay, or keep them with the note as an exception?

**Problem:**
- Your rule blanks a later value where its cells can be located and keeps it with a note only when the traced part shows no gain; the note keeps these texts for their size alone, which the rule rules out[l10t].
- The texts naming ICU, intubation or ventilation die at 40.2% (443 rows), against 10.6% overall; with arrest and death words, 820 rows at 44.1%.
- A few name the patient's own death ("ADMITIDO EM OBITO", "PROTOCOLO DE MORTE ENCEFALICA"): part of the target, which no note can keep.
- Many describe the state on arrival ("CHEGA EM VM / IOT"), a fact known at admission.

| | Option | What it does | Pro | Con |
|---|---|---|---|---|
| a | Keep with the note, recorded as an exception; blank only the texts naming the patient's death | the fact: an intubation typed at notification cannot be told from an arrival state row by row | keeps arrival states the team knows; a few cells change | the traced part shows a gain (40% deaths); an exception to a Must's clause the curator marked "case by case" |
| b | Blank the located texts (recommended) | the texts naming death, brain death, ICU, intubation or ventilation are blanked unless they name arrival ("CHEGA", "CHEGOU", "ADMITIDO EM", "RECEBIDO EM"); about 800 cells | follows zillow_prize, melbourne_housing_market and noaa_storm_events_damage; the texts add 0.002 in all | a keyword list to maintain; some arrival states written otherwise are lost |
| c | Drop the three text columns | the blind reviewer's fix | no keyword list | loses the 0.002 the texts add and every legitimate symptom and history text |

**Recommendation:** b: it blanks what the keywords locate, as the clause's cases do, and keeps the arrival states. **Decision:** a, b or c?

[l10t]: **LEAK-10** (Must; amended 2026-11-08): out is "a part, a consequence or another encoding of the target"; second clause: a value read later is blanked where located, and stays with a note "only when the part that can be traced shows none"; third clause (noaa_storm_events_damage, Lennart, 2026-11-08): "the size of the worth alone never decides".

6. RACE OR COLOUR KEPT -> CONSISTENT IN SUBSTANCE; DEPARTS FROM THE BATCH'S METHOD WITHOUT A STATED REASON

Precedents that keep race in clinical risk tasks (accepted definitions): kumc_inpatient_aki_prediction (race_code),
diabetes_130_us (race), 2_month_survival_rate_prediction (race), wids_diabetes_mellitus (ethnicity); from the same portal
sinan_dengue_case_screening_1m keeps race_colour. The insurance cases of the Tensions row (bemtpl97, Lennart
2026-11-05; australian_vehicle_insurance_2004_2005 and three more, Lennart 2026-11-08) drop sex from pricing only.
The batch's method (AI, undecided): ask whether the actor's own law bars the ground for its decision, and write the
answer in the notes. rais_employment_separation_1m drops five grounds under Lei 9.029/1995 and proposes the extension of
the stance "to any decision on a person where the actor's own law bars the factor" (its issue 1, unconfirmed);
enem_entrance_exam_scores_1m keeps race because no law it found bars it for its decision (its issue 1: "every call on
protected grounds since November asks whether the actor's own law bars the ground for its decision; here none does");
acs_food_stamps_2014_2024_1m names 7 CFR 272.6(a) and leaves the framing to the curator; wioa_employment_after_exit and
nchs_linked_birth_infant_death_1m write a SEL-1 note leaving it to the curator.
sivep keeps race without that question in its notes; only the builder's checklist says "as in Baqui et al.; no
objection found". The use case names "early referral to intensive care and beds". Resolução CFM 2.156/2016, the
Federal Council of Medicine's criteria for ICU admission and discharge, says, from memory and NOT read in this run, that
those decisions are made "sem discriminação por questões de religião, etnia, sexo, nacionalidade, cor, ... idade,
condição social, ... deficiência". Read as rais reads Lei 9.029 (a ground the norm lists leaves the score), it would
take race, sex and age out of this task, and age alone scores ROC AUC 0.812 of the full 0.870. So either a fact sets a
prognostic estimate apart from an allocation decision, or the extension needs a scope. Two other texts the curator may
weigh, also unread here: Lei 8.080/1990 art. 7 IV (equal care "sem preconceitos ou privilégios de qualquer espécie",
which lists no grounds) and LGPD art. 11 II f (health data processed for health protection by health professionals).
Decide together with rais issue 1.

Consistency check: Keep race or colour (and sex and age) as inputs of an at-admission death-risk estimate whose use case includes early ICU referral, when the norm for ICU admission lists them among the grounds of discrimination?

**Problem:**
- The batch asks whether the actor's own law bars a ground for its decision and writes the answer in the notes (rais drops five grounds, enem keeps race since no law bars it); this definition keeps race with no such line[row].
- The use case names early ICU referral and beds; Resolução CFM 2.156/2016 (not read in this run) says ICU admission decisions are made without discrimination by ethnicity, colour, sex or age, among other grounds.
- Read as rais reads its law, this would take race, sex and age out, and age alone carries ROC AUC 0.812 of 0.870.
- Clinical precedents keep race (kumc_inpatient_aki_prediction, diabetes_130_us, 2_month_survival_rate_prediction, sinan_dengue_case_screening_1m).

| | Option | What it does | Pro | Con |
|---|---|---|---|---|
| a | Keep, with a note naming the fact that sets it apart | the estimate is a prognosis the team uses to monitor and plan; the norm governs the admission decision, which weighs prognosis, not the estimate's inputs; a SEL-1 note in the definition as in enem | keeps the clinical risk factors; follows the clinical precedents; decided alike with enem | rests on a reading of a norm not read yet; the use case's wording (ICU referral) must match the note |
| b | Narrow the use case to monitoring and bed planning | ICU referral leaves `use_case`; the note says the norm does not reach a monitoring estimate | removes the conflict with the norm | a narrower actor than Baqui's "hospital management" |
| c | Treat like rais | race, colour, sex and age (and other listed grounds) leave the features | the extension's own logic | age is the task's core; no clinical precedent drops it |
| d | Scope the extension (an amendment) | the Tensions row covers laws on access to a job, a service or a benefit, not a clinical prognosis | one rule for rais and this dataset | a scope the curator has not stated yet |

**Recommendation:** a, decided with rais issue 1, once the norm's text is read. **Decision:** a, b, c or d?

[row]: principles.md, Tensions, "A rating factor known at the prediction point against a factor the actor may no longer use" (P3 and P4; USE-1, USE-6); its extension is proposed in rais_employment_separation_1m's issue 1 (SEL-1, Must).

7. OCCUPATION AS "title [CBO code]" (CLEAN-12 Should; decide alike with rais and sinan) -> CONSISTENT

CLEAN-12 (amended 2026-11-01, Lennart) decodes a nominal code (its example is a job) into its words. sinan issue 4 and
rais issue 5 both recommend option B ("title [code]") and implement codes for now; a third exception of one reason
would make an amendment due. sivep decodes, and a fact sets it apart from both even under their option C (codes stay for
classifications whose words are only in a separate table): SIVEP's rows carry the title next to the code (PAC_DSCBO and
PAC_COCBO). Measured (pc1_checks.log): 4,436 rows with a code (0.5%), 506 codes, none with two titles, so the merge is
lossless and needs no lookup file. For consistency, sinan's issue 4 and rais's issue 5 should name sivep as the batch's
case decoded from the source's own pair; whichever of A, B or C the curator takes there, sivep stays as it is.
Municipalities as "name [IBGE code]" against sinan's municipality codes: the same fact (SIVEP ships the names), and
consistent with CLEAN-12; sinan's reading (a place's code whose name is a copy of the id stays a code) does not bind a
source that ships the names.

8. FALLBACK roc_auc (MET-5, MET-8) -> CONSISTENT

Multi-metric papers go to the fallback (Tensions row; gallstone_disease and heart_disease, Lennart 2026-10-21, the latter
checked 2026-10-27). sinan_dengue_case_screening_1m (same portal; Bohm et al. report five metrics) takes fallback
roc_auc with the same kind of reason. The screening read Baqui et al. as ranking by ROC AUC; the builder reads AUC-ROC
and average precision side by side. Either way the metric is roc_auc, and Baqui et al. analysed the data rather than
publishing it, so the fallback origin stands.

9. YEAR 2026 (PROV-9 Must) -> CONSISTENT

PROV-9: "A source that grows over time (a public register, a scraped site, a monthly archive) takes the year of the
snapshot we pin." Precedents: rain_in_australia (Lennart, 2026-10-26: 2026, "a file that grows with BoM's daily
observations"), aeolus_rebuilt (Lennart, 2026-10-26: 2026, the pinned snapshot), wadden_sea_sibes_macoma_abundance
(Andrej, 2026-11-02). sinan's 2023 (its claim audit R1, mediator C7) is set apart by a fact: every shipped sinan row is
in a frozen final file (DENGBR16-21), so the release's first public year could be bounded; sivep ships rows from the
live INFLUD25 and INFLUD26, replaced weekly (claims.md 3-4).

EXTRA FINDINGS (real pairs, not in the list)

E1. Hospital by name only, against the definition's own municipality reasoning (CLEAN-1; like cases within one
definition). Municipalities ship as "name [IBGE code]" "since names repeat across states"; the hospital
ships as its name, and 130 names stand for hospitals in more than one municipality (HOSPITAL SAO LUCAS in 21, HOSPITAL
SAO JOSE in 19, HOSPITAL UNIMED in 17), on 82,945 rows (8.99%) (pc3_hospital_death_texts.log; the blind reviewer found
109 in its sample). The same reason calls for "name [hospital municipality code]", a cheap, label-free fix. No fact in
the notes sets the hospital apart.

Consistency check: Ship the hospital as "name [hospital municipality code]", as the municipalities ship for the same reason?

**Problem:**
- The notes ship municipalities as "name [IBGE code]" because names repeat across states; the hospital ships by name alone[c12h].
- 130 hospital names stand for hospitals in more than one municipality, on 8.99% of the rows, so distinct hospitals share one level.

| | Option | What it does | Pro | Con |
|---|---|---|---|---|
| a | Keep the name (as now), with a note | the hospital municipality column lets a model split the shared names | no change | one level holds up to 21 hospitals; unlike the municipalities' treatment |
| b | "name [hospital municipality code]" (recommended) | one level per hospital and municipality | the municipalities' own reasoning; lossless | more levels (a few hundred) |

**Recommendation:** b. **Decision:** a or b?

[c12h]: **CLEAN-1** (Should): clean to the state an expert would ship; the like case is the definition's own municipality bullet ("municipalities ship as 'name [IBGE code]', since names repeat across states").

E2. Licence: the same portal, two readings (EV-4: a one-line note, never an issue or a reason). sinan ships "CC BY-ND
3.0" from the portal's footer ("Todo o conteudo deste site esta publicado sob a licenca Creative Commons
Atribuicao-SemDerivacoes 3.0", sinan claim audit item 27); sivep ships "CC BY (Creative Commons Atribuição; version not
stated)" from the dataset page's license_title / license_id cc-by (claims.md 2); the blind reviewer reads the footer
as CC BY-ND. For the claim auditor and mediator: read sinan's dataset-page license_id too and state both alike (the
dataset-level licence, if both pages carry one, with the footer named).

DRIFT AND AMENDMENTS
- No drift: no curator has decided any of these calls on a SIVEP or SINAN dataset yet.
- Amendment watch: CLEAN-12's CBO codes (sinan, rais, wioa; sivep is not a fourth exception, see 7). The "factor the
  actor may no longer use" extension (rais issue 1) would reach this dataset (see 6): decide it with this case in view.
- LEAK-10's second clause: if the curator takes option a in 5, it is the first keep of located late cells without a
  traced no-gain test; with kumc (issue 1, a traced keep) and noaa (blanked) both pending or recent, record the fact.

</details>

<details><summary>Advocate</summary>

ADVOCATE OPENING BRIEF: sivep_gripe_sari_outcome (2026-11-09)

Position: ship. Keep the 2023 history, admission as the prediction point, code 3 counted as death, temporal half-year
windows and roc_auc. Make five fixes that need no curator decision (points 2 and 3). Each real problem the panel found
has a remedy below exclusion on the ladder. No reviewer recommends `No`: the blind reviewer says "include with
changes", and the claim auditor, column auditor and split auditor say "ship after changes" / "right with notes".

Judgment record (proposed)
Verdict: ship after changes.
Validity: SEL-1 holds (no objection; race note, curator call); USE-1/USE-5 hold; LEAK-10 triggered, fixed (texts, vaccine
blank, vaccine day counts); LEAK-24 holds; SPLIT-9, SPLIT-14, SPLIT-20/21 hold.
Value: TP clean (LightGBM 0.878, age alone 0.812, smallest class per test fold 11,594); fallback roc_auc (MET-5/8).
Quality: hospital "name [municipality code]", schooling under 7 missing, impossible values missing (CLEAN-11/12/14).
For the curator: late forms (keep with a corrected note), race (with rais issue 1), metric (log_loss optional).

1. The task is real, hard to game and split honestly. These are the facts the other points rest on (P3, P4, P6).
   Evidence: the split auditor rebuilt every window exactly and found SPLIT-1/3, SPLIT-9, SPLIT-10, SPLIT-14, LEAK-24
   and SPLIT-20/21 all holding. A simulated earlier download had 98.0% of the later-closed labels known, 98.1% of deaths
   against 98.0% of discharges; death share 10.31% against a final 10.28%. The task gamer stacked every exploit and
   gained +0.0026 AUC (no row-order, id, copy or transform leak). Honest headroom over age is real: age 0.812, full
   0.878-0.887. History from 2023: the claim, split, domain and precedent agents agree (aeolus precedent, SPLIT-20 Should;
   the break is the deciding fact, not the score, SPLIT-21 Must). Code 3 as death: the column, domain, blind and
   precedent agents agree. USE-5 (Must) holds. LEAK-22 does not apply to an all-cause target (framingham is a
   cause-specific contrast; SUPPORT and sepsis_survival are followed).
   Outranks: any later quality point. Validity and value hold, so the rest is quality or curator weighing (principles,
   "validity, then value, then quality").

2. The confirmed small leaks are Musts with cheap definition fixes. They need no decision and the dataset keeps its
   shape (LEAK-10 Must, LEAK-2; remedy ladder step 2).
   a) Free texts. Blank the cells that name ICU, intubation, ventilation, arrest or death, except arrival phrases
      ("CHEGA/CHEGOU/ADMITIDO EM/RECEBIDO EM"). That is about 808 cells (0.088%), and 443 of them name ICU,
      intubation or ventilation, with 40% deaths. Drop the 3 rows dead on arrival (LEAK-36, USE-7). The texts as a
      whole add +0.002, and the gamer measured in-stay words at -0.0001, so the cost is nil. This is the precedent
      checker's option b, following zillow_prize, melbourne and noaa_storm.
   b) covid_vaccine blank with 0 doses. Set it to "No", the value at admission: 922 rows, 99% cures, a survivor
      fingerprint. Optionally do the same for the influenza "Yes" with a later dose, which is diluted and shows no gap.
   c) Vaccine day counts. Bin days_since_covid_vaccine and days_since_flu_vaccine to 30 days. The exact counts rebuild a
      person key, so a later readmission tells the model the patient survived: +0.0015 over the strong honest model.
      The gamer measured the binned columns: baseline 0.88446 against 0.88439, and the exploit then adds 0. Removing a
      shortcut is not optional (Tensions row SPLIT-9: "a shortcut is always removed"). No honest signal is lost, so
      the P7 lossless preference does not weigh against it.
   Outranks: the critic's "the shipped file leaks" (true today). LEAK-10 is met by fixing the definition, and the
   Tensions row "a real task against a leak" says fix the leak and keep the task.

3. Cheap cleaning fixes that need no decision (CLEAN-11/12/14, Should; P7).
   Ship hospital as "name [hospital municipality IBGE code]". There are 125 names for hospitals in several
   municipalities (9.3% of rows), and the definition already ships municipalities this way, so this follows its own
   reasoning (precedent checker E1). Also: schooling missing for age < 7 (the dictionary's own rule; 60,797 rows);
   negative ages, postpartum men and children, and COVID dose dates before 2021-01-17 made missing; one name per IBGE
   code. Occupation stays as "title [CBO]". It is lossless and one to one (507/507) and follows CLEAN-12. The difference
   from rais and sinan belongs in those datasets' REVIEW.md, and no fact here sets it apart.
   Outranks: nothing to outrank. These are quality fixes that are cheap and safe, which is exactly what P7 asks.

4. Forms filed on or after the outcome day: keep, with the note corrected (LEAK-39/LEAK-10 read against USE-7 and
   LEAK-22's "do not select on the future").
   Conceded: the builder's 7.5% is a lower bound. Same-day forms add 6.8%, so 14.4% of rows and 25-27% of deaths.
   In those forms the respiratory answers and completeness depend on the outcome. Test AUC is 0.869 on routine rows
   against 0.876 on all rows. The note "their inputs describe the admission" is wrong and must go.
   Why keep:
   (i) Every filter reads a post-admission fact. The outcome date is blank for 7.2% of discharges and 0.4% of deaths,
       so dropping by it selects the cohort by the outcome. That is the same reason framingham kept its rows (Lennart,
       2026-10-22).
   (ii) The label-free 7-day lag cut does not resolve it. It removes only 57% of late forms and 6% of same-day forms
       (column auditor).
   (iii) LEAK-39's drop condition fails. Both classes are in this route by the tens of thousands, unlike gallstone's
       72 against 5. sinan is set apart by a fact: its filter read dates before its prediction point (precedent
       checker 3).
   (iv) No participant can exploit it, because the notification date is not shipped. It shifts every model alike
       (+0.004 to +0.006 in the headline), and training without these rows leaves routine rows unchanged (0.8731 against
       0.8732).
   Mildest remedy: keep, with the corrected numbers in fit_reason and the notes, and report the routine-only score.
   The 74 units that notify mostly deaths (1.6% of rows) get the LEAK-25 note, as for noaa_storm.
   If the curator prefers to drop the rows (option b), the dataset still ships with about 790k rows. Either way this
   is a weighing of fit, not a reason to exclude.

5. Race or colour: a curator call that cannot block shipping (SEL-1 P1; Tensions row "factor the actor may no longer
   use").
   Evidence: dropping race, ethnicity and community changes AUC by 0.0002 (0.8819 to 0.8817; column auditor 0.8745 to
   0.8743). Either answer ships the dataset.
   - CFM Res. 2.156/2016 art. 9 lists colour together with sex and age for ICU admission decisions. Read as a bar on
     inputs, it would remove age (0.812 alone), the clinical core of every admission score (4C, ABC2-SPH). So the rule
     governs allocation under scarcity, not a prognostic estimate. The domain practitioner found no statute barring it
     for a clinical risk score, unlike Lei 9.029 for rais.
   - Precedents keep race in clinical risk tasks: kumc, diabetes_130_us, SUPPORT, and sinan from the same portal.
   Mildest remedy: a SEL-1 note giving the reading taken and the numbers. If the curator extends rais issue 1 to
   professional norms, drop the four fields at no cost.

6. Target censoring and metric: as shipped, with notes. Neither is a validity problem (LEAK-24 Must holds; MET-5/MET-8;
   Tensions row on the source's metric).
   - Outcome-missing rows: open rows are riskier, but counting them at their predicted risk moves 2026-H1 from 8.30% to
     about 8.6% (claim auditor). An oracle month offset gains +0.0001 (gamer). Ending at 2026-03-31 would shrink the
     last window against SPLIT-14's floor, which already limits the design (split auditor). Note the residual instead.
   - Metric: Baqui reports AUC-ROC and AP and ranks by AUC-ROC. roc_auc is the fallback, or "source" if the curator
     reads Baqui as a deliberate choice. Pooled AUC partly rewards age: true, but adults alone still give 0.759, and no
     source defines a within-age metric (MET-11 needs a clear case). log_loss for calibration in bed planning is a
     defensible curator option. It changes the score, not whether the dataset ships.

7. Provenance, ICU on day 0 and licence: notes only (PROV-10, EV-4; USE-8).
   - Licence: the portal's dataset metadata says cc-by, "Creative Commons Atribuição" (claim auditor, from __NEXT_DATA__).
     The site footer says BY-ND 3.0. The precedent checker calls this a metadata note and not an issue (EV-4). Record
     both readings, as sinan should.
   - 20.5% admitted to ICU on day 0: name it in fit_reason (the mildest remedy). A new day-0 ICU flag is optional
     (+0.008) and is a definition change for the curator. Its absence makes the task harder, not dishonest.
   - The live files are replaced weekly: the SHA-256 prefixes are pinned (PROV-8). Note it.

</details>

<details><summary>Advocate rebuttal</summary>

ADVOCATE, REBUTTAL: sivep_gripe_sari_outcome (2026-11-09)

We agree on the outcome: ship after changes. The agreed fixes need no decision: critic points 3, 5 and 7 match my
points 2 and 3. Below, each of the critic's points: what I concede, and what I still dispute.

C1. Race or colour (SEL-1). I concede the drop as the recommendation. I dispute that CFM 2.156 art. 9 is the reason
   or that this is a Must.
   - Conceded: the four fields are worth nothing (AUC 0.8819 -> 0.8817). The domain practitioner, acting as the actor,
     would not use them. A dataset that drops them loses nothing.
   - Disputed: art. 9 lists sex and age next to colour, and the critic keeps sex and age. So the article cannot be
     what decides; the decision rests on the profession's norm and SUS equality. That extends the rais stance from law
     to professional norms, which is unconfirmed. So this is a curator call (P1, with rais issue 1), not a Must for
     this panel. Whichever way it goes, the SEL-1 line in the notes is needed.
   - What would change my mind: the curator confirming the rais extension to professional norms. Then the drop is a
     Must here.

C2. Late forms (LEAK-10). I concede the rule reading: a note alone is not available.
   - LEAK-10 is a Must and the traced part shows a gain (0.910-0.913 against 0.869). A keep therefore needs an
     amendment, as the critic says. My "keep with a corrected note" was wrong under the rule's text.
   - On the remedy ladder, fixing the definition comes before an amendment. So I accept the drop by outcome date as
     the default, on one condition: the measurement the critic also asks for (EV-1) runs before shipping. My concern
     is concrete. The rows that stay are the late forms without an outcome date: 6.2-7.2% of discharges against 0.4%
     of deaths. These are almost all survivors, so the late-form completeness pattern could flip from marking deaths
     to marking survival.
   - What would change my mind back to keep plus an amendment: a measurement after the drop that shows a reverse
     marker. That means a model on the missing-value flags plus age beating age alone by clearly more on the remaining
     late, undated forms than on routine rows (today's routine gain is +0.024), or retained test rows scoring well
     above 0.869.
   - Also for the curator: the drop removes about 25% of deaths, mostly early ones, so the death population changes.
     Say so in fit_reason.

C3. Free texts and the vaccine blank: agreed. Fix the note's count (258 of 660, not 660).

C4. Prediction point. I concede that both groups are named and the copy notes corrected (the "notified twice" reading,
   132 days). I dispute that this is a Must or needs a new column.
   - ICU on the admission day: placing the patient is decided at admission. Bed planning and monitoring still act on
     these rows, so the prediction point holds for them (USE-3). Only the referral wording overstates. Narrowing the
     wording and naming the 20.5% (37% of deaths) fixes that at no cost.
   - The icu_on_admission_day flag (+0.008) adds a new feature, and day granularity also catches transfers later the
     same day. That is a curator option, not a requirement.
   - Hospital-acquired SARI: keep the rows, with one sentence saying their moment is when the SARI is recognised.
     Nothing leaks either way. Dropping the 8,168 rows is optional, not needed.
   - What would change my mind on the flag: the day-0 ICU timing shown to be reliable, with same-day transfers rare.
     Then ship the flag, since it is known at the prediction point.

C5. Vaccine day counts: agreed (bin to 30 days).

C6. Metric. I concede the note: the score pools children (61% of test rows) with adults (adults-only AUC 0.759).
   I hold that roc_auc stays, as a weighing call.
   - The Tensions row on metrics sends a multi-metric paper (Baqui: AUC-ROC and AP) to the fallback, as gallstone
     was. MET-11's `context` needs a clear case.
   - The 12% over-prediction comes from drift: train has 11-12% deaths, test 8-10%. log_loss would mostly score how
     each model guesses the drift. That is real for bed planning, but it is the same shift for every model, and no
     curator precedent sets `context` log_loss for a non-competition binary task.
   - What would change my mind: a curator decision accepting `context` for bed planning, or a measurement showing that
     log_loss and AUC rank the task-probe models differently. Then log_loss carries information AUC does not.

C7. Agreed. A note about the licence (both readings), the LEAK-25 note on the 74 units, the cleaning fixes and
   occupation kept as words.

</details>

<details><summary>Critic</summary>

CRITIC: OPENING BRIEF, sivep_gripe_sari_outcome (2026-11-09)
Position: do not ship as defined. Ship only after the changes below. Four of them (points 2-4 and the naming in 5)
are Must fixes. Point 1 is a P1 call for the curator. None of them is a reason to exclude the task: the task is real
(USE-1 holds, all seven agents agree).
Sources: the phase-A reports in this folder (claim_auditor = CA, column_auditor = COL, split_auditor = SA,
domain_practitioner = DP, blind_reviewer = BR, task_gamer = TG, precedent_checker = PC), the builder's report and
dataset.py.

1. P1, SEL-1 (Must): race or colour is an input of a score whose use case names "early referral to intensive care".
   Problem: the builder's P1 row says "no objection found". CA read Res. CFM 2.156/2016 art. 9, which says ICU
   admission and discharge decisions are made "sem discriminação por questões de ... etnia, sexo, ... cor, ...
   idade". DP found no statute that bars race in a clinical risk score. As the actor, DP would still not put it in a
   triage score: SUS equality (Lei 8.080 art. 7 IV), the medical code, and Brazilian admission scores (ABC2-SPH, 4C)
   that leave it out. The notes never ask whether the actor's norm bars the factor, which the rest of the batch asks
   (PC 6: rais drops, enem keeps, each with a written reason).
   Effect: the race fields carry no signal. Without race_colour, indigenous_ethnicity and traditional_community(_type),
   ROC AUC goes 0.8819 -> 0.8817 and log loss 0.2179 -> 0.2180 (DP d02). CA measured -0.0007 and COL measured
   -0.0002. Keeping them buys nothing and builds colour into an ICU-referral score.
   Remedy: drop the four columns. Keep age and sex as physiological prognosis, with a SEL-1 line in the notes that
   names the CFM norm and the reading taken. Decide this together with rais issue 1. The alternative (narrow the use
   case to monitoring and beds) gives up the use case's main decision just to keep a column worth 0.

2. P4, LEAK-10 and LEAK-6 (Must): forms filed on or after the outcome day carry the outcome. The builder's issue 3 is
   understated, and its note is refuted.
   Problem: the builder counts only forms notified after the outcome (7.5%). Another 6.8% were notified on the
   outcome day. Together they are 14.4% of rows and 25-27% of deaths (CA 8, COL A). In these forms the symptom answers
   describe the course of the stay, not the admission. Within the same length of stay, the age-adjusted OR of
   respiratory distress is 3.69/3.09/2.38 in late forms against 2.30/1.70/1.38 in routine ones. Completeness depends
   on the class: race is missing for 25.2% of late discharges against 9.7% of late deaths (OR 0.25; routine 0.63).
   Missing flags plus age beat age alone by +0.054 on late rows and +0.024 on routine rows (COL A). The note's
   sentence "Their inputs describe the admission, so they stay" is contradicted by the data (CA 16, COL A).
   Effect: test AUC is 0.913 on same-day forms and 0.910 on late forms, against 0.869 on routine forms (COL). TG
   measured 0.918 against 0.881 on r0. The headline overstates performance at admission by about 0.004-0.006 (TG, COL)
   for every model.
   Rule: this is "missingness that encodes the outcome" and "a column recorded after the outcome" (LEAK-10). A
   confirmed leak goes even when it is small (LEAK-6). Under LEAK-10's second clause, a value stays with a note only
   when the traced part shows no gain. The traced part shows a gain. So the builder's "keep with a note" is not
   available. LEAK-39 is not the operative rule (PC 3 is right that its drop condition fails), so PC's "consistent"
   reading does not settle this.
   Remedy, mildest that works: drop the rows notified on or after the outcome date (BR and TG ask for this). Measure
   the residue before shipping (EV-1): 6.2% of discharges have no outcome date and stay. The builder objects that the
   cut reads the outcome date. That selection is measurable and much smaller than the leak, and a cut that reads the
   label's date for a few percent is not worse than a feature that reads the label for 14%. If the curator keeps the
   rows, it is an amendment of LEAK-10 (a Must has no exceptions), not a note. The notes and fit_reason must then
   carry the corrected numbers (14.4%; routine-only AUC 0.869).

3. P4, LEAK-10 and LEAK-2 (Must): two located leaks with cheap fixes.
   (a) Free texts. 9 cells name this stay's events or the death: "ADMITIDO EM OBITO", "PROTOCOLO DE MORTE
   ENCEFALICA", "MORTE CEREBRAL", "EVOLUIU PARA IOT" and others; 8 of the 9 are deaths (CA 25). About 808 rows name
   ICU, intubation, ventilation or arrest, with 40-50% deaths (COL B; PC: 443 rows at 40.2%). The structured ICU and
   ventilation fields were dropped for LEAK-10, and these texts bring them back (LEAK-2). The note's "660 texts name
   intubation or ICU" is a miscount: only 258 do (CA). The note keeps the texts for their size alone, which LEAK-10's
   third clause rules out ("the size of the worth alone never decides").
   Remedy: blank the located cells, keeping the arrival phrases ("CHEGA EM", "RECEBIDO EM"), as PC option b
   recommends (follows zillow_prize, melbourne, noaa_storm). Drop the 3 dead-on-arrival rows (LEAK-36, USE-7). Fix
   the count in the note. Cost: nil (TG: the texts are worth -0.0001; all texts +0.002).
   (b) The covid_vaccine blank is a survivor fingerprint. The definition blanks "vaccinated" where every dated dose
   is after admission, and leaves doses at 0. The pair (blank, 0 doses) occurs on 922 rows: 914 cures and 8 deaths
   (0.87% against 10.6%). 709 of the rows are infants, none of whom died (COL C; PC 4 measured 0.55%).
   Remedy: set covid_vaccine to "No", the state at admission. Do the same for the influenza "Yes" with a later dose
   (diluted, but the same marker; PC 4).

4. P3 and P4, USE-3 and USE-8 (Must): the prediction point is mis-stated for two named groups.
   (a) Hospital-acquired SARI: 24,087 rows (2.6%, 22.7% deaths). On 8,656 of them the onset is after the admission
   date, so the form describes an illness that began during the stay (CA I1, COL Q2).
   (b) 20.5% of rows entered ICU on the admission day. They are 37% of all deaths and 74% of all ICU stays (DP 1b).
   For them the "early ICU referral" in the use case was decided before the prediction. The flag is known at
   admission and is worth +0.008 pooled ROC AUC (+0.018 among adults; DP d03).
   Remedy: name both in the prediction-point bullet, in `known` and in fit_reason. For (a), optionally drop the rows
   whose onset is 2 or more days after admission (8,168; CA). For (b), either ship an icu_on_admission_day flag
   (date-gated to day 0) or name the 20.5% in fit_reason and narrow the referral wording. The curator chooses.
   Also correct the notes where CA refuted them: the "notified twice" reading is wrong for 28% of copy groups (two
   birth dates; LEAK-18/19, Should); follow-up is 132 days, not 131.

5. P4 (weak; nearest rule LEAK-17): the exact vaccine day counts rebuild persons. A later admission then proves
   survival.
   Problem: admission_date - days_since_covid/flu_vaccine gives the dose date. With sex, age and municipality that
   nearly identifies a person. A later admission of the same key in the test window marks this row as survived:
   5.4% deaths against 14.1% (TG 1). Gain: +0.0015 over a strong honest model, the largest exploit found.
   Remedy: bin both columns to 30 days. TG tested it: honest baseline 0.88446 against 0.88439 (no loss), and the
   exploit then adds 0. This is a fix that needs no curator decision: it costs nothing and removes the key.

6. P6, MET-8, MET-10 and MET-11 (Should/Weigh): roc_auc does not score what the actor uses.
   Problem: the actor sums probabilities into expected deaths and ICU demand (DP 2, 5). Models over-predict deaths by
   12% in the test windows (mean 0.104 against 0.093), and AUC cannot see this. The pooled AUC is mostly the
   infant-against-elderly contrast: 0.882 pooled against 0.759 among adults; age alone scores 0.812.
   Rule: MET-8 prefers a strictly proper rule for the same goal, and MET-11 `context` covers a metric the task makes
   obvious. MET-10's diversity factor favours log_loss: the collection's binary log-loss tasks come only from
   competitions. CA and PC hold that the fallback is legitimate, so this is a weighing call, not a Must.
   Remedy: log_loss with origin `context`, the reason "bed planning sums the probabilities". If roc_auc stays, the
   notes must say that the score pools children (61% of test rows) and adults, with the adults-only number.

7. P7 and procedure (Should; cheap): fixes and notes.
   - Hospital as "name [hospital municipality IBGE code]": 125-130 names stand for several hospitals (9% of rows;
     COL E, PC E1, BR 4b). This applies the definition's own reasoning for municipalities (CLEAN-1).
   - 74 units with 50% or more deaths (1.6% of rows, 10.1% of deaths, mostly post-outcome forms at UPAs; COL A2).
     Here the hospital level records where the patient died. Remedy: a LEAK-25-style note with the spread; fit stays
     approximate. Point 2's drop removes most of these rows.
   - Schooling missing for under-7s (60,797 rows coded "no schooling"; the dictionary's own rule). Impossible values
     made missing: negative ages, postpartum men, COVID-19 doses dated before 2021-01-17 (COL F, G; CLEAN-11/14).
   - Occupation: keep the "title [CBO]" decoding (CLEAN-12; PC 7 shows it is lossless). Occupation is filled for 2.4x
     the odds in deaths (CA 7), which point 2 mostly removes.
   - Licence: the portal footer says CC BY-ND 3.0 and the dataset page says cc-by. State both, alike with sinan (EV-4
     note; BR 7, PC E2). It is a note, not a reason.

Not contested: the 2023 history (SPLIT-20/21; SA 5, PC 1); death from other causes counted as death (USE-5; CA I2,
DP 2, PC 2); the end at 2026-06-30. SA's simulated download outweighs BR's and TG's ask for an earlier end: 98.0% of
later-closed labels were already known, deaths and discharges alike, and the expected shift is +0.05 points (LEAK-24
holds). The split design, the gap and the windows also stand (SA 3, 6).

</details>

<details><summary>Critic rebuttal</summary>

CRITIC, REBUTTAL: sivep_gripe_sari_outcome (2026-11-09), point by point against the advocate's opening brief

A1. The task is real, and the split, history and target hold: CONCEDED. My brief never asked for exclusion and
    contested none of these. Disputed only: "the rest is quality". The late forms (A4) are a P4 validity question, not
    quality.

A2. Free texts, the covid_vaccine blank and the 30-day bins: AGREED. This is my points 3 and 5, word for word. I accept
    the advocate's stronger rule for the bins: the Tensions row says a shortcut is always removed (SPLIT-9). That
    makes the bins a fix, not an option.

A3. Hospital "name [municipality code]", schooling under 7, impossible values, occupation kept: AGREED (my point 7).

A4. Late forms: the point still in dispute.
    Conceded: (ii) the 7-day lag cut fails (COL: it removes 57% of late forms). (iii) LEAK-39's drop condition fails.
    I never rested on LEAK-39. Neither choice excludes the dataset: it ships about 790k rows or about 923k.
    Disputed (i): "dropping selects by the outcome, as in framingham". In framingham, a row's existence depended on
    follow-up. Here the conflict is between two P4 Musts. LEAK-10 is confirmed on these rows: COL measured symptom ORs
    that depend on the route, and race missing for 25.2% of late discharges against 9.7% of late deaths. LEAK-6's
    narrowing allows a note only when the traced part shows no gain, and here the traced part gains (0.91 against
    0.869). So "keep with a note" is not available under the rule as written. It needs an amendment of LEAK-10 by the
    curator, which the advocate's brief does not offer.
    Disputed (iv): "it shifts every model alike". It does not. The gain sits in missingness: on late rows, missing
    flags plus age add +0.054 over age, against +0.024 on routine rows (COL A). So the gain depends on how a model
    handles NaN, and that can reorder methods. LEAK-6 also drops a confirmed leak even when small, whether or not a
    participant can exploit it.
    What would change my mind: a measurement showing that the drop distorts more than the leak. For example, routine-row
    AUC or method ranking that moves by more than the 0.004-0.006 inflation once the rows are dropped, or a death
    population of the dropped set that the task cannot do without.
    If that measurement comes out in the advocate's favour, I accept keep only as a written amendment to LEAK-10, with
    the corrected numbers and the routine-only score in fit_reason.

A5. Race: CONCEDED in large part. The advocate is right that art. 9 also lists age. A bar on inputs would then remove
    the core of every admission score, so the norm reads as governing the allocation decision, not a prognosis. DP
    found no statute that bars race, and kumc, diabetes_130_us, SUPPORT and sinan keep it. This is no SEL-1 Must
    failure and does not block shipping.
    Held: the notes must carry the SEL-1 line with the reading taken. The advocate agrees. I still recommend the drop,
    because it costs 0.0002, but as a curator call decided with rais issue 1.
    What would change my mind on the recommendation: the curator scoping the rais extension to access decisions
    (option d).

A6. Censoring: AGREED. My brief already accepted LEAK-24 on SA's simulated download (+0.05 points) and did not ask for
    a 2026-03-31 end. A note with CA's 8.30% -> about 8.6% is enough.
    Metric: CONCEDED that it is a weighing call (MET-10) that does not block shipping. Held: log_loss as my
    recommendation, because the actor sums probabilities and the 12% over-prediction goes unscored.
    What would change my mind: Baqui naming AUC-ROC as the criterion it selects models by. CA reads AUC-ROC and AP
    side by side, which makes it the fallback (MET-5). If Baqui does select by AUC-ROC, it is `source` and roc_auc
    stays.

A7. Licence, pinned files and ICU on day 0: AGREED. All are notes. The flag is optional, and naming the 20.5% in
    fit_reason is the minimum.
    Not answered by the advocate: my point 4a. Hospital-acquired SARI (2.6% of rows; 8,656 with onset after admission)
    must be named at the prediction point (USE-3, Must). It is a note, at no cost.

Net: the definition fixes are agreed (texts, vaccine blank, bins, hospital key, cleaning, notes). One point stays open
for the curator: the late forms, either dropped or kept under a LEAK-10 amendment, never as a plain note.

</details>
