# kumc_inpatient_aki_prediction

**Outcome:** added. The AI recommends shipping it: the review panel's changes are made, with the calls open listed under For the curator. Admission-day risk of acute kidney
injury during the stay for 76,957 adult stays at the University of Kansas Health System, 2007-2016, from the authors'
CC0 deposit of He et al. (JAMIA Open 2019), the paper's counts reproduced exactly; 275 coded features, random stays,
fallback `roc_auc`.
Verdict: ship after changes (made).
Validity: SEL-1, SEL-2 hold; USE-1 holds, USE-8 approximate (no medications and no admission creatinine; the cohort is
cut on 2+ days, 2+ creatinine values and the 24-hour creatinine, all after admission; `Selection Bias`); LEAK-10
triggered twice and fixed: `comorbidity_renal_failure` dropped (in part a code of this stay's AKI, LEAK-6) and the 26
procedure-defined APR-DRG groups dropped (clause 2: late for an unknown subset, gain above noise); LEAK-10 clause 2 keep
of the 35 medical groups and the 26 other comorbidities open (issue 1; the traced part shows none); SPLIT-8 holds
(forced IID, no dates and no patient key); SPLIT-29 measured small (0.0015).
Value: the task probes flag nothing; ROC AUC 0.705 with untuned LightGBM on the shipped features (5 folds x 2 seeds); `roc_auc`
fallback (MET-5).
Quality: CLEAN-12 fixes made (sex decoded, age labelled with target-free reasons, the lab decoding led by the reference
ranges, `comorbidity_diabetes_w_ccs_or_none` renamed with a note); BMI/blood-pressure order (issue 2) and race words
(issue 3) open.
Weighed: source + (the paper reproduced exactly, CC0), size +, fit approximate -, real EHR data of mixed coded types +.
For the curator: issue 1 (keep the medical groups and the remaining comorbidities with a note), issue 2 (order BMI and
blood pressure), issue 3 (decode race).

**Main points:** Three calls: keep the 35 medical diagnosis groups and the 26 remaining comorbidities from the
discharge abstract with a note (issue 1, recommended); type the BMI and blood-pressure bands as ordered (issue 2,
recommended; the definition keeps unordered codes now); decode race into words (issue 3, recommended; the definition
keeps the codes now).

**Record judgment:** valid. The authors' own Dryad deposit (CC0) for a peer-reviewed paper that names the actor, the
moment and the decision (Perspective #2, risk at admission); the label counts equal the paper's. The screening's
"1,917 coded attributes" is the dictionary; the public file holds 302, without medications. The record carries the
`Selection Bias` marker the notes name.

**Issues for Lennart:**

1. **Keep the 35 medical diagnosis groups and the 26 remaining comorbidities, both from the discharge abstract, with a note?**

   * **Problem:**
     - Both blocks come from the hospital's discharge abstract (University HealthSystem Consortium data, coded after discharge, no present-on-admission flag in the deposit), which the source "presumed to be available at admission"[^l10].
     - The parts the panel traced to the stay itself are dropped (the renal-failure comorbidity and the 26 groups defined by a procedure); for the rest, the part that can be checked against the admission-day record shows no extra AKI, and the rule then allows a keep with a note only as your case-by-case call[^l10][^l6].
     - Six of the kept comorbidities can arise during a stay (fluid and electrolyte disorders, coagulopathy, weight loss, deficiency anaemias, chronic blood loss anaemia, pulmonary circulation disease), and a medical group also implies that no operation was done, a contrast that mostly left with the dropped procedure groups (Experiments).
   * **Background:**
     - A present-on-admission flag, set per diagnosis code, says whether the condition was there when the patient arrived; without it a coded complication of the stay looks like a known condition.
     - A base APR-DRG (All Patient Refined Diagnosis Related Group) is set by a grouper after discharge from the principal diagnosis, the condition found "after study" to be chiefly responsible for the admission, and the procedures done; each stay has at most one of the 61 frequent groups the file keeps, and 39% have none.
     - The 35 medical groups left are the stay's reason for admission as finally coded (sepsis, heart failure, pneumonia, chemotherapy, ...); the 26 comorbidities are the Elixhauser set (hypertension, diabetes, cancers, heart failure, ...).
     - The history block, cut by date, already holds the stay's diagnosis for 44-76% of acute medical admissions, recorded on the admission day.
   * **Effect on the task:**
     - With both blocks a model reads the coder's final view of the stay's diagnosis and conditions; a team at admission has the working diagnosis and the known chronic conditions, which agree with it for most stays but not for a complication coded later.
     - Where they disagree the score is optimistic; the late-coding test below finds no sign of that on these rows.
   * **Experiments:**
     - Late-coding test: for each comorbidity, the AKI rate of flagged stays with no matching record up to the admission day against flagged stays with one. Renal failure +12.3 points (z 6.2), the measured leak, now dropped; the six that can arise in a stay -2.4 to +1.7 points (z at most 0.9); 15 chronic comorbidities that cannot arise in a stay spread from -3.8 to +4.7 points (z up to 3.7), the noise of this test.
     - Stratified by age band and history size, weight loss moves to +3.8 points (z 2.9) and fluid and electrolyte disorders to +1.5 (z 2.3), both inside the chronic spread (alcohol abuse +4.7, z 3.7); renal failure stays at +10.8 (z 4.8).
     - Medical groups: a diagnosis not yet in the admission-day record changes the AKI rate by +0.4 points (z 0.8; the 19 of the 35 medical groups that pair with a history group, the other 16 untested; none beyond the noise of 19 tests); the "no operation" signal (sepsis 14.9% AKI against 31.3% for an infection with an operation) left with the procedure groups.
     - Untuned LightGBM, 5 folds x 2 seeds, on the shipped features: 0.705 with both blocks; 0.700 without the six comorbidities (option B, -0.0052); 0.689 without them and the medical groups (option C); 0.694 without the medical groups only, 0.693 without all 26 comorbidities, 0.681 without both blocks.
   * **Consistency:**
     - bemtpl97 and fremtpl2 (2026-11-05) follow the source's timing where the data behaves as the source says, and onlinenewspopularity and medical_facility_operational_data kept late values with a note when the traced part showed no gain: option A follows them[^prec].
     - distribution_transformers_at_cauca_department (2026-10-21) dropped late values whose gain could sit on the late rows, which is why the procedure groups went here; bank_marketing's `campaign` (2026-11-08) turned a kept note into a drop once its timing was shown late.
     - Your call becomes the precedent for ny_sparcs_inpatient_length_of_stay, whose screening reads APR-DRG as coded at discharge for an admission-time task; B or C would be stricter than bemtpl97 and onlinenewspopularity, on a fact (third-party complication shares) the measurement here does not bear out.
   * **Panel:**
     - Keep (advocate, mediator, and the precedent checker's option a): the measurement on these rows shows no late signature for any kept flag, renal failure alone stands outside the chronic spread, and a measurement on the data outranks third-party shares[^ev2].
     - Drop (column auditor, domain practitioner, the critic at first): ICD-9-era Elixhauser has no present-on-admission filter, Glance et al. 2006 found 43% of coagulopathies and 25% of fluid and electrolyte disorders were complications of the stay, and the authors' earlier paper calls the UHC data "not immediately available".
     - The critic withdrew its drop of coagulopathy and fluid and electrolyte disorders after the late-coding test, and left the medical groups to you.
   * **Unknown:** whether the UHC data applied present-on-admission flags; Vizient's flags or coding dates would settle it, and the deposit does not hold them.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep both blocks with the note (implemented) | 35 medical groups and 26 comorbidities stay; the note gives the late-coding test and the source's presumption as the reasons; ROC AUC 0.705 | the traced part shows no gain on any kept flag; follows bemtpl97, fremtpl2 and onlinenewspopularity; keeps the reason for admission and the chronic conditions a team knows | rests on the source's presumption for what cannot be traced; ICD-9-era coding has no present-on-admission filter |
     | B | Drop the six comorbidities that can arise in a stay | 20 comorbidities and the 35 medical groups stay; ROC AUC 0.700 | removes the flags most likely to be coded from the stay; cheap | drops flags the test shows behave like chronic ones; rests on third-party shares from another population |
     | C | Drop the six and the medical groups too | the 20 chronic comorbidities stay; ROC AUC 0.689 | from the discharge abstract only the chronic conditions stay, which a team knows at admission | loses the coded reason for admission a team mostly has; no measurement asks for it; stricter than every precedent |
     | D | Drop the medical groups only | the 26 comorbidities stay, the 35 medical groups go; ROC AUC 0.694 | the reason for admission as coded after discharge goes, of which only 19 of 35 groups could be tested | loses a reason for admission a team mostly has; no measurement asks for it |

   * **Recommendation:** A: the test that exposed the renal-failure flag finds nothing on the kept flags, and the traced late parts are already out; recorded as your case-by-case keep[^l10], revisited if present-on-admission flags can be had. **Decision:** A, B, C or D?

   **Notes for the AI:**
   - A: a CC line in the record naming the late-coding test and the keep; a Mechanisms row in leak_checks.md under LEAK-10 ("codes from a discharge abstract at an admission prediction point": the located late parts dropped, the rest kept with a note when the late-coding test shows none; kumc_inpatient_aki_prediction), and the same reading carried to ny_sparcs_inpatient_length_of_stay's record.
   - B: add `comorbidity_fluid_and_electr_disorders`, `comorbidity_coagulopathy`, `comorbidity_weight_loss`, `comorbidity_deficiency_anemias`, `comorbidity_chronic_blood_loss_anemia` and `comorbidity_pulmonary_circulation_disease` to the `drop_columns` call of `_clean` (LAB_DIAGNOSIS_PAIRS reads the raw file, so the pairs stay); `task_summary.known` (20 comorbidities), `changes` (33 columns), the opening line (269 features), the flag count (247), the leak bullets moved from "kept" to "dropped" with their cost; re-run `dataset check`, the leak and task probes.
   - C: as B, and drop every remaining `admission_drg_` column; `task_summary.known` and `fit_reason` without the diagnosis groups, `changes` (68 columns), the notes' counts (234 features, 212 flags); the same checks.
   - D: drop every remaining `admission_drg_` column only; `changes` (62 columns), the notes' counts (240 features, 218 flags), `task_summary.known` and `fit_reason` without the diagnosis groups; the same checks.

   [^l10]: **LEAK-10** (Must; amended 2026-11-08): a feature holds only what existed at the prediction point; out is "a part, a consequence or another encoding of the target". Its second clause, "a case-by-case judgment of the curator, never a default": a value read later goes where its late cells can be located, and "where they cannot be located row by row, the values go when they may carry a gain (distribution_transformers_at_cauca_department) and stay with a note only when the part that can be traced shows none (onlinenewspopularity's keyword and self-reference counts)".
   [^l6]: **LEAK-6** (Must): "a confirmed leak goes even when small" (santander `has_*`, +0.003 AUC). The renal-failure flag was worth +0.0024 ROC AUC, 5 of 5 folds.
   [^ev2]: **EV-2** (Must): a measurement on the data outranks the source's primary documents, which outrank third-party pages.
   [^prec]: bemtpl97 and fremtpl2 (Lennart, 2026-11-05; leak_checks.md, Mechanisms row "LEAK-10, LEAK-7"): `bm` kept because the source registers it at the start of the period, `BonusMalus` blanked where the data shows it does not behave like history. onlinenewspopularity (2026-10-26) and medical_facility_operational_data (2026-11-05): kept with a note because the traced late part showed no gain. distribution_transformers_at_cauca_department (Lennart, 2026-10-21): attributes possibly changed after the outcome for an unknown subset, gain 0.701 to 0.639, dropped.

2. **Type the BMI and blood-pressure bands as ordered?**

   * **Problem:**
     - The deposit gives the vital-sign band codes no words; the authors' earlier study at the same hospital (Cheng et al. 2017, Table 2) lists the bands, without codes[^c12].
     - The BMI and blood-pressure codes follow the study's band order on evidence without the target; pulse and temperature do not and stay codes in either option[^c14].
     - The definition keeps all five bands as unordered integer codes with this evidence in the notes.
   * **Background:** the study bands BMI as <18.5, 18.5-24.9, 25-29.9 and 30 or more, diastolic pressure as <80, 80-89, 90-99 and 100 or more, systolic as <120, 120-139, 140-159 and 160 or more, pulse in five bands from under 50 and temperature in five from under 95.0 °F, each with an unknown state.
   * **Experiments:**
     - BMI: 92% of the stays with the obesity comorbidity are in code 4 (37% of all), 20.7% of those with weight loss in code 1 (3.3% of all), so codes 1-4 read as the study's four bands in order.
     - Blood pressure: the diastolic shares 71.8, 19.5, 7.1 and 1.4% fit the four bands; hypertension moves systolic stays to codes 3-4 (28.9% against 21.3%).
     - Pulse code 1 holds 16% of the stays where the study's first band is under 50 beats per minute, and temperature code 2 holds 80% where its second band is 95.0-97.6 °F, so their order is not the table's.
   * **Effect on the task:** an ordered type lets a model use the order of BMI and blood pressure (a tree splits on it, a linear model can take it as one slope), and a wrong order would mislead it.
   * **Consistency:**
     - Our default keeps a code with no words as shipped[^c12]; this file already departs from it on stated evidence for the labs (decoded from the data; the precedent checker calls it a reasonable departure) and for sex and the age labels.
     - force_2020 (2026-10-21) accepted units inferred from the data when a second, independent signal agreed; here the shares and the target-free shifts are two signals.
   * **Panel:** the claim auditor would order BMI and blood pressure and keep pulse and temperature as codes; the column auditor would keep all five as codes with the inferred mappings noted; the advocate and the critic accept either; the mediator leans to ordering.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Unordered codes (implemented) | the five `*_band` columns stay unordered integer codes, the evidence in the notes | no inferred mapping ships as fact; the default for a code without words | loses an order that is very likely right; unlike the age bands of the same file |
     | B | Ordered BMI, diastolic, systolic with the study's labels | `bmi_band`, `diastolic_bp_band`, `systolic_bp_band` become ordered categories with the study's band labels; pulse and temperature stay codes | the order a clinician uses; readable; one standard with the age bands | the mapping is inferred from a sibling study, not stated by the deposit |

   * **Recommendation:** B, the mappings marked as inferred in the notes, as the age labels are. **Decision:** A or B?

   **Notes for the AI:** on B, in `dataset.py`: `BMI_LABELS = {1: "<18.5", 2: "18.5-24.9", 3: "25-29.9", 4: ">=30"}`, `DIASTOLIC_LABELS = {1: "<80", 2: "80-89", 3: "90-99", 4: ">=100"}`, `SYSTOLIC_LABELS = {1: "<120", 2: "120-139", 3: "140-159", 4: ">=160"}` (check Table 2: the claim audit read '>160' through a summary), decoded after `set_missing` and typed `ordinal` in `_feature_types`; pulse and temperature stay in `categorical`; rewrite the vitals bullet (inferred, with the evidence above); re-run `dataset check` and the dtype probes.

   [^c12]: **CLEAN-12** (Should; amended 2026-11-01, Lennart): "A code whose codebook says in words what it means is decoded into those words"; "A code with no words (an id, a detector column, an anonymized code) stays as shipped."
   [^c14]: **CLEAN-14** (Should; amended 2026-10-30, Lennart): an ordinal scale (a grade, a stage, binned ranges) "is decided case by case, categorical by default"; the order comes "from the context and logic, not from target information" (Lennart, 2026-10-31).

3. **Decode the race codes into words?**

   * **Problem:**
     - The deposit gives the four race codes no words; the authors' earlier study at the same hospital (Cheng et al. 2017, Table 3) lists White, African American, Asian and Other, without codes[^c12r].
     - The code shares follow the study's order within 3 points, evidence without the target.
     - The definition keeps `race_code` as codes with this evidence in the notes.
   * **Experiments:** codes 1 to 4 hold 76.1, 13.5, 0.8 and 9.5% of the stays, the study's White, African American, Asian and Other 73.4, 15.2, 0.9 and 10.5%; as a check only, not as evidence, the AKI rates rank the same way in both.
   * **Effect on the task:** none on what a model learns; the words help a reader, and a wrong mapping would mislabel the groups.
   * **Consistency:**
     - Our default keeps a code with no words as shipped[^c12r]; sex in the same file is decoded from sex-specific diagnoses, without exception.
     - The age-band labels already ship on the same kind of evidence (code shares within 1.5 points of the study's); A here keeps race as codes while age carries inferred labels, B treats both alike.
   * **Panel:** the claim and column auditors would decode race (the claim auditor also accepts codes with the evidence in the notes); the advocate and the critic accept either; the mediator leans to decoding.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep `race_code` (implemented) | integer codes 1-4, the evidence in the notes | no inferred mapping ships as fact; the default for a code without words | unlike the age labels of the same file |
     | B | `race` with White, African American, Asian, Other | the codes decoded into the study's words | readable; treats race and age alike | the mapping is inferred from shares, Asian (0.8%) and Other (9.5%) told apart by size alone |

   * **Recommendation:** B, the mapping marked as inferred in the notes, as the age labels are. **Decision:** A or B?

   **Notes for the AI:** on B, in `dataset.py`: `RACE_LABELS = {1: "White", 2: "African American", 3: "Asian", 4: "Other"}`, `BASE_NAMES["race"] = "race"`, decoded with the others in `_clean`, `race` in `categorical`; rewrite the race bullet (inferred, with the shares); re-run `dataset check` and the dtype probes.

   [^c12r]: **CLEAN-12** (Should; amended 2026-11-01, Lennart): "A code whose codebook says in words what it means is decoded into those words"; "A code with no words (an id, a detector column, an anonymized code) stays as shipped."

**Review panel:** ship after changes (mediator). Tier full: the claim, column and split auditors, the domain
practitioner, the blind reviewer, the task gamer and the precedent checker, then the advocate and the critic with one
rebuttal each, and the mediator, who ran the late-coding test on the comorbidities that can arise in a stay (renal failure, congestive heart failure and the six of issue 1)
(calibrated on 15 chronic ones) and the paired gain of APR-DRG 443 and the five other procedure groups. Claims: 32
audited, 3 metric checks and 5 implied claims; the data, the counts, the prediction point, the timing of the history and
the lab decoding hold (the last on stronger, target-free evidence); refuted and now fixed: that every feature is known at
admission (the renal-failure comorbidity), that the group names say what they are (APR-DRG 710 and 443 are operation
groups), that sex and the age edges cannot be read, the reason for the age order, and the metric reason's wording; the band
order (issue 2), race words (issue 3). Blind review: include with changes; its main concern is the timing of the DRG and
comorbidity codes. Task gamer: no exploit beyond seed noise; the discharge-coded blocks lift every model by 0.043, now
in part dropped. Agreed: drop the renal-failure comorbidity and the procedure groups, keep the forced random split with
the repeat-patient numbers, and the fit, naming and cleaning fixes. Disputed: all procedure groups or about 20 (settled:
all 26, with APR-DRG 443), the four comorbidities not yet tested (the mediator's test shows no late signature; their keep is part of issue 1),
the medical groups and the remaining comorbidities (issue 1), the band order (issue 2), race words (issue 3).

<details><summary>Mediator</summary>

```text
MEDIATOR REPORT: kumc_inpatient_aki_prediction (2026-11-09)
Read: principles.md, leak_checks.md (LEAK-6, -7, -10, -38), review_panel.md, dataset.py, the record, builder_report.md,
all seven phase-A reports, both briefs and both rebuttals. My runs (thread caps 4): the run folder
r1_test.py -> r1_test.out, r1_calibration.py -> r1_calibration.out, proc_ablation.py -> proc_ablation.out/.json.

======================================================================================================================
1. RECOMMENDATION (judgment record)
======================================================================================================================
Verdict: ship after changes.
Validity: SEL-1, SEL-2 hold; USE-1 holds, USE-8 approximate (no medications, no admission creatinine, cohort cut on 2+
days and 2+ creatinine values); LEAK-10 triggered twice and fixed in the definition: `comorbidity_renal_failure`
dropped (an encoding of the target, LEAK-6), and the 26 procedure-defined APR-DRG groups dropped (clause 2: late for an
unknown subset, gain above noise); LEAK-10 clause 2 keep for the 35 medical DRGs and the 26 other comorbidities (the
traced part shows none) is the curator's case-by-case call (issue 1); SPLIT-8 holds (forced IID), SPLIT-29 measured
small (0.0015).
Value: TP flags none; about 0.703 ROC AUC after the drops (untuned LightGBM, 5-fold x 2 seeds); roc_auc fallback (MET-5).
Quality: CLEAN-12 fixes (decode sex; target-free reasons for age and labs; rename `comorbidity_diabetes_w_ccs`);
race words and BMI/BP order open (issue 2).
Weighed: source + (paper reproduced exactly), size +, fit approximate -, real EHR diversity +.
For the curator: issue 1, keep the medical DRGs and the remaining comorbidities with a note (LEAK-10 clause 2);
issue 2, decode race and order BMI/BP (CLEAN-12/14).

======================================================================================================================
2. THE DISPUTED POINTS, SETTLED
======================================================================================================================

(1) Which procedure groups go: about 20, or all 25 (P4, LEAK-10 Must, second clause)
- Both sides rest on LEAK-10 clause 2; the dispute is a fact: do the five non-O.R. procedure groups (PCI with and
  without AMI, cardiac cath with and without ischaemia, bone marrow transplant) carry a gain that may sit on late rows?
- Mechanism: each group is defined by a procedure done in the stay (its name says so). Elective and emergency stays
  cannot be told apart (no admission type), so the late part cannot be located row by row. Same mechanism as the O.R.
  groups.
- New fact: the column auditor's 25 omit `admission_drg_kidney_urin_tract_nonmalig`. By the dictionary's APR-DRG order
  (KIDNEY TRANSPLANT, MAJOR BLADDER PROC, KIDNEY/URINARY TRACT MALIG, KIDNEY/URIN TRACT-NONMALIG, RENAL DIALYSIS ACCESS
  DEV; the medical renal groups come later: RENAL FAILURE, NEPHRITIS, KIDNEY/URIN TRACT INFECT) it is APR-DRG 443,
  "kidney & urinary tract procedures for nonmalignancy", an O.R. group (claim auditor R2 confirmed). 18.9% AKI, n=513.
- Decisive experiment (proc_ablation.json; paired, 5-fold x seeds 0 and 1, renal failure and the 20 O.R. groups
  already out):
    with 443 and the five:          0.7100
    without 443:                    0.7071   gain of 443   +0.0029, SE 0.0007, 10/10 folds positive
    without 443 and the five:       0.7030   gain of five  +0.0041, SE 0.0006, 10/10 folds positive
- Ruling: both gains are above noise, so clause 2 sends them out ("go when they may carry a gain"). The critic's
  position wins, extended by 443: drop 26 groups (20 O.R. + 443 + 5 non-O.R.). No higher-ranked rule keeps them; no
  milder remedy applies (the late rows cannot be located). Change now, no decision needed.
- Noted, not argued by either side: BMT and elective joint replacements are planned by nature. Keeping them would rest
  on inference about a group, not on a located late part; the drop treats them like the other procedure groups.

(2) Weight loss, deficiency anaemias, chronic blood loss anaemia, pulmonary circulation disease (P4, LEAK-10 clause 2)
- The agreed decisive test (claim auditor R1): flag fixed, vary only the matching record up to the admission day.
  Decision rule fixed before the run: a flag shows the late signature when AKI|new exceeds AKI|known by more than 2 SE,
  read against the chronic comorbidities (EV-9).
- Results (r1_test.out), AKI rate new (no record) vs known (record), difference, z:
    renal failure (CCS 158)         28.8% (881) vs 16.6% (899)   +12.3 pp  z 6.2   [reference: the measured leak]
    weight loss (CCS 52)            15.5% (2,901) vs 15.4% (1,451)  +0.0 pp  z 0.0
    deficiency anaemias (CCS 59)    13.1% (7,082) vs 12.6% (3,382)  +0.5 pp  z 0.7
    chronic blood loss (CCS 59)     11.8% (289) vs 14.2% (155)      -2.4 pp  z -0.7
    pulmonary circulation (CCS 103) 18.1% (665) vs 16.3% (826)      +1.7 pp  z 0.9
    (coagulopathy +0.6 pp z 0.6, fluid/electrolyte +0.6 pp z 0.9, CHF +0.7 pp z 0.5: the claim auditor's numbers
    reproduced)
  Wider history pairings (52+58, 59+60, 103+118) change nothing.
- Robustness: stratified by age band x history-count quartile (Mantel-Haenszel), weight loss moves to +3.8 pp (z 2.9),
  fluid/electrolyte +1.5 pp (z 2.3), the others stay below z 1.8; renal failure stays at +10.8 pp (z 4.8). Calibrated
  on 15 chronic comorbidities that cannot arise in a stay (r1_calibration.out), the same statistic runs from -3.8 to
  +4.7 pp (z up to 3.7: alcohol abuse +4.7 pp, metastatic cancer +4.2 pp, depression z 3.0). Weight loss sits inside
  that null; renal failure is the only flag outside it, on both cuts.
- Ruling: none of the four shows renal failure's signature. Under clause 2 each may stay with the note; they join
  coagulopathy and fluid/electrolyte. The critic's withdrawn drop does not come back. The keep itself is the
  curator's case-by-case call (clause 2 keeps are "never a default"), so it enters issue 1 with a recommendation.

(3) The medical DRGs: required out by LEAK-10 clause 2, or the curator's call?
- Clause 2 applies (the final base APR-DRG is set after discharge). The test is whether the traced part shows a gain.
  The "no operation" signal (720 -> 710) is traced, and it leaves with the O.R. groups (710 is among them). For the
  "principal diagnosis after study", the same R1 cut on 19 medical DRGs (diagnosis in the admission-day record or
  not): pooled difference +0.4 pp, z 0.8 (stratified by DRG); single groups from -5.1 to +5.5 pp, none beyond the
  noise of 19 tests (the largest, inflammatory bowel -3.9 pp, runs the other way).
- Ruling: not required. The traced part shows none, so clause 2 allows a keep with a note. A keep is "a case-by-case
  judgment of the curator, never a default", so it is the curator's call (issue 1). Both sides already concede this in
  their rebuttals (advocate C2, critic A4). Recommendation: keep.

The rest is agreed. Dropping renal failure is a fix, not a call: LEAK-10's "a consequence or another encoding of the
target", and LEAK-6, "a confirmed leak goes even when small" (+0.0024, 5/5 folds).

======================================================================================================================
3. CHANGES TO MAKE NOW (no decision needed)
======================================================================================================================
P4
 1. Drop `comorbidity_renal_failure` (LEAK-10 Must, encoding of the target; LEAK-6).
 2. Drop the 26 procedure APR-DRG flags (LEAK-10 Must, clause 2): the 20 O.R. groups of the column auditor's list
    (ablation.py OR_PROC, including `infect_parasitic_disease` = APR-DRG 710), `kidney_urin_tract_nonmalig` (APR-DRG 443),
    and `bone_marrow_transplant`, `percut_cardiovasc_proc_w_ami`, `percut_cardiovasc_w_o_ami`,
    `card_cathet_exc_ischemia`, `card_cathet_w_ischemia`. Re-run the block ablation for the notes.
 3. Rewrite the "Potential leak, kept on purpose:" bullet (LEAK-10, EV-2; precedent checker D2). Name the measured
    renal-failure case and its drop; name the procedure drop with its gain (0.7234 -> 0.7083 for the 25 groups, +0.0029
    for 443); give the R1 results for the eight acquirable comorbidities and the medical-DRG trace; give the source's
    "presumed" placement as the reason for the rest, and drop the reason "the source's document places them at admission
    (EV-2)". Revisit if Vizient POA flags or coding dates can be had.
 4. Notes, SPLIT-29 / SPLIT-8 (Should): repeat patients are 44-61% of stays; purging likely twins costs LightGBM 0.0015
    and a deep forest 0.008, with the ranking unchanged. Add that a dated release (the DUA set) should be split by time,
    and that the history may be thinner after the October 2015 switch to ICD-10.
 5. USE-8 (Should): fit_reason names the 2+ creatinine values, the 24-hour creatinine exclusion, the missing admission
    creatinine and the dropped blocks. Add `decision_markers: [Selection Bias]` to the record (as lt_vehicle_loan,
    tunisian). task_summary.known reads "diagnoses recorded up to the admission day"; it also drops "reason for
    admission" to match what stays.
P6
 6. Metric reason (MET-5): keep `fallback` roc_auc. Add that AUC is the paper's headline and the measure it ranks windows
    by, and that MET-5 does not count a headline number as a deliberate choice (claim auditor R6).
P7
 7. Decode `sex_code` to female/male (CLEAN-12; certain: 1,553 of 1,553 prostate-hyperplasia stays are code 2, 413 of
    413 uterine stays code 1).
 8. `age_band`: keep the order, and give target-free reasons (CLEAN-14; the curator's rule of 2026-10-31). Pregnancy
    flags are 4.3/4.3/0.9/0/0/0% by band, the counts rise, and the band shares match Cheng 2017 within 1.5 points.
    Label the bands 18-25 ... 56-64, 65+ as inferred.
 9. Rename `comorbidity_diabetes_w_ccs` (for example `..._or_none`) and add a notes bullet: 83% of its rows have no
    other comorbidity (CLEAN-12 naming; PROV-13 kind).
10. Lab Decision table: lead with the dictionary's reference ranges and the majority share, with the 16-of-18
    diagnosis-lab pairs; keep the AKI rate as a check only (CLEAN-12, precedent checker D5).
11. Cosmetic: cast the vital-band categories to integers; fix `coagulopthy` and `head_trauma_w_coma_1_hr` (writing).

======================================================================================================================
4. ISSUES FOR THE CURATOR, RANKED
======================================================================================================================
Issue 1. P4, LEAK-10 (Must), clause 2 keep: keep the 35 medical DRGs and the 26 remaining comorbidities with a note?
 - Problem: both blocks come from the discharge abstract, which the source "presumed" known at admission. The traced
   late parts (renal failure, procedure groups) leave under the changes above. A keep with a note under clause 2 is the
   curator's case-by-case judgment.
 - Effect: about 0.703 with both kept. Dropping the 6 acquirable comorbidities costs 0.0033-0.0055 more. Dropping the
   medical DRGs too lands near 0.68-0.69.
 - Keep (advocate): the R1 cut shows no late signature for any of the 8 acquirable flags (all within the chronic null;
   renal failure alone outside it). The medical-DRG trace is +0.4 pp, z 0.8. The admission reason is in the
   admission-day record for 44-76% of acute medical stays. Precedents bemtpl97/fremtpl2 (follow the source where the
   data agrees) and onlinenewspopularity (trace shows none: keep).
 - Drop (critic, column auditor, domain practitioner): ICD-9-era Elixhauser has no POA filter; Glance 2006 finds 43% of
   coagulopathies and 25% of fluid/electrolyte flags are complications (third party, another population, EV-2 ranks it
   below the measurement). Cheng 2017, the same authors, call the UHC data "not immediately available". A medical
   group also encodes "no operation in this stay".
 - Would settle it: Vizient's POA flags or coding dates (U1).
 - Options: (a) keep both blocks with the note (recommended); (b) drop the 6 acquirable comorbidities (coagulopathy,
   fluid/electrolyte, weight loss, deficiency anaemias, chronic blood loss anaemia, pulmonary circulation), keep the
   rest; (c) drop the medical DRGs as well.
 - The call becomes the precedent for ny_sparcs_inpatient_length_of_stay (APR-DRG at an admission point), with a
   Mechanisms row in leak_checks.md.

Issue 2. P7, CLEAN-12 / CLEAN-14 (Should): race words, BMI and BP order.
 - Race codes match Cheng 2017's table order within 2.5 points (White, African American, Asian, Other), and the AKI
   ranks agree. BMI, systolic and diastolic follow Table 2's order on target-free evidence (92% of obesity stays in BMI
   band 4). Pulse and temperature stay codes.
 - Options: (a) decode race and type BMI/BP as ordinals with Table 2's labels; (b) keep the codes and put the evidence
   in the notes. Both sides accept either. Builder's issue 2 (the lab decoding) is settled as implemented, with change
   10 (precedent checker D5: a reasonable departure).

======================================================================================================================
5. AGREED FACTS
======================================================================================================================
- CC0 Dryad deposit tied to He et al. 2019; 76,957 stays, 7,259 AKI (9.4%), equal to the paper. Perspective #2:
  admission-day prediction, AKI on any day of the stay (KDIGO creatinine).
- The history block is cut by date (P1 adds 55,819 flags over P2 and removes none). It holds diagnoses up to the
  admission day; the stay's own AKI code is absent (CCS 157 in 9.1% of AKI stays).
- Admission-day labs show no post-onset pattern (BUN abnormal 18.6% early AKI vs 18.4% none). The lab decoding is
  supported by 16 of 18 target-free pairs.
- DRG and comorbidities are one value per stay from the UHC discharge abstract. The DRG and comorbidity blocks
  together are worth 0.043 (tuned: 0.722 vs 0.679).
- Renal failure flag: 28.8-29.8% AKI without a prior renal record vs 16.6-17.4% with one; worth +0.0024, 5/5 folds.
- No shortcut beyond noise: row order 0.499, adversarial 0.4996, kNN and frequency features within seed noise, exact
  copies 0.11-0.14% of test rows, best single feature 0.544.
- Forced IID is the only regime the file allows; repeat patients 44-61% of stays, measured inflation 0.0015.
- roc_auc fallback; 2,419+ positives per test fold; P6 holds after every option.
- Sex decodes with certainty; age order holds on target-free facts; `comorbidity_diabetes_w_ccs` is mostly "none".

Task gamer's exploit, mapped:
- #1, discharge-coded DRG and comorbidities as admission features (+0.043): LEAK-10 (clause 2; for renal failure, the
  "encoding of the target" clause). Known: the "Potential leak, kept on purpose:" note gives 0.726 -> 0.683 (0.043), and
  the gamer measured 0.043. The same size, so no new issue from the gamer. The rule finding (parts of it must go) came
  from the auditors and is settled above. The gamer's 0.0033 for 5 acquirable comorbidities is unsized in the note
  and falls under issue 1.
- The `diabetes_w_ccs` oddity: CLEAN-12 naming / PROV-13 kind, new, not in the notes, fixed by change 9.
- Nothing else found (LEAK-13 to -16, -18, -39: pass).

======================================================================================================================
6. CONSISTENCY WITH PRECEDENT
======================================================================================================================
Followed:
- distribution_transformers_at_cauca_department (2026-10-21): late for an unknown subset, gain, dropped. Applies to all
  26 procedure groups, including the five non-O.R. groups and 443 (gains measured above).
- santander `has_*` (LEAK-6): a small confirmed leak goes (renal failure).
- bank_marketing `campaign` (2026-11-08): a kept note reversed to a drop. Same direction here.
- bemtpl97 / fremtpl2 (2026-11-05): follow the source's timing where the data behaves as it says. onlinenewspopularity
  and medical_facility: keep with a note when the trace shows none. Both apply to issue 1 (a).
- sepsis_survival_minimal_clinical_records, the churn snapshots, bemtpl97: forced IID with repeat entities, notes.
- heart_disease, gallstone_disease: fallback roc_auc. lt_vehicle_loan, tunisian: Selection Bias marker.
- Curator's rule of 2026-10-31 (ordinals from context, not the target): age reason replaced.
Departures: none in the recommendation. Option (b) or (c) of issue 1 would be stricter than bemtpl97 and
onlinenewspopularity. The fact that would set this case apart is the third-party complication shares (Glance 2006),
which the measurement does not bear out here. Reflection question if the curator picks (c): would ny_sparcs and other
admission-time tasks drop every discharge-coded diagnosis group, even where the admission-day record matches?
LEAK-38 does not reach here (a research deposit, timing partly tested), as both sides agree.
```

</details>

<details><summary>Claim audit</summary>

```text
CLAIM AUDITOR REPORT: kumc_inpatient_aki_prediction (2026-11-08)
=================================================================

Verdict: the definition's own claims mostly hold, and several of them hold on stronger evidence than the builder
gave. There is one new validity finding. The comorbidity flag `comorbidity_renal_failure` carries the outcome for part
of the rows (LEAK-10). It is small (0.003 ROC AUC) and cheap to fix: drop the one column. Issue 1 (the DRG timing) is
larger than written, because the two DRGs with the highest AKI rates after the bypass DRGs are operating-room DRGs whose
names hide the procedure. The CLEAN-12/14 notes say that sex, race, age and BMI/BP cannot be decoded. They can: sex
with certainty, and the others from the authors' earlier study, with the data agreeing. The metric (roc_auc) is right.
Only its origin label ("fallback": "none is one deliberate choice") can be contested.

Sources read: He et al. 2019 full text (NCBI BioC, PMC6447093; saved in work_claim_auditor/src/paper.txt); Cheng et
al. 2017 (PMC5977670, Tables 2 and 3 via WebFetch); the deposit's README.txt; Dryad API (dataset, versions); Crossref.
Scripts and outputs: work_claim_auditor/t1_codes.py ... t7_scrub.py with the matching .out/.json files.

Evidence key: M = measured here; S = source document; T = third party; I = inference.

CLAIMS TABLE (claim | source | test | result | evidence | rule)
---------------------------------------------------------------
1 | Dryad doi:10.5061/dryad.qc90qb4, one version 2018-11-16, CC0 | claims 1, download_description | Dryad API dataset + /versions | holds | license CC0-1.0, publicationDate 2018-11-16, total versions 1, relatedWorks = ooy043 (M) | PROV-1, EV-4
2 | per-file API 401, version download redirects without a token | claims 2 | curl version download; access_log | holds | HTTP 302 to a signed zip URL; 401 bodies in access_log (M) |
3 | MD5 of the zip equals Dryad's | claims 3 | md5sum | holds | ba97b2ffce83868c421e7ac187dbd013 (M) |
4 | SHA-256 of P2 csv and dictionary | download_description | sha256sum | holds | 39cdf824... and 0e0f2533..., same as declared (M) |
5 | online 2018-11-15, issue 2019 vol 2(1) 115-122 | bibtex, year | Crossref API | holds | published-online 2018-11-15, print 2019-04-01, vol 2, issue 1, 115-122 (S) |
6 | full set needs a DUA; public file scrubbed "by removing variables" | notes | README.txt | holds | quoted text present (S) |
7 | 76,957 stays, 7,259 AKI (9.4%) | task_summary, notes | count + paper | holds | 7,259/69,698 in file and in the paper's Methods and Results (M, S) | USE-5
8 | adults >18, LOS >= 2 d, >= 2 SCr, eGFR<60 / SCr>1.3 within 24 h excluded, 2007-11 to 2016-12 | task_summary.row, notes | paper Methods | holds | all criteria in "Study population" (S). Not in the claims: before exclusion 179,370 encounters of 96,590 patients (1.86 per patient), so repeat stays certainly exist | SPLIT-29
9 | KDIGO SCr criteria, baseline, all SCr to discharge | notes | paper + Cheng 2017 | holds | baseline text verbatim in He; 0.3 mg/dL/48 h and 1.5x/7 d in Cheng (S) | USE-5
10 | creatinine and eGFR not features | notes | paper | holds | "SCr and eGFR were not included as predictive variables" (S) | LEAK-10
11 | P2 = admission-day prediction point | notes | paper + README | holds | "(past, admission)", "(admission, discharge)" (S) | USE-1, USE-3
12 | P3 = same features and order, label cut to 1 day | notes | row-by-row compare | holds | 0 feature columns differ; crosstab P2xP3: every one of the 1,611 P3 positives is a P2 positive, 5,648 P2 positives are P3 negatives (M) |
13 | P4 72,846 rows / 1,634 pos; P1 233 cols, same labels | notes | load files | holds | P4 (72846, 283), 1,634 pos; P1 (76957, 233), labels equal to P2 (M) |
14 | raw file lists the AKI stays first | notes | first 7,259 rows | holds | label mean of the first 7,259 rows = 1.000 in P1 and P2 (M) | LEAK-39
15 | 302 = 22 + 61 DRG + 27 COM + 192 CCS, no MED | notes | block counts | holds | P2 blocks CCS 192, DRG 61, COM 27, lab 14, 8 demo/vital (M); paper Table 1 totals 1,917 (S) |
16 | every kept flag set in >= 398 stays; "rare ones removed" (label-free) | notes, checklist P4 "label-free" | per-file thresholds across P1/P2/P4: is any flag dropped from a file although it clears that file's minimum? | holds | P2 min 398, P4 min 448, P1 min 968. No P2-only CCS or DRG has a count >= P1's minimum (max 906 and 963), so a per-file count threshold explains every kept set and no label-based selection is needed to explain them (M) | LEAK-27..31
17 | lab codes 0 unknown, 1 normal, 2 abnormal (inferred) | notes, Decision 1 | DECISIVE: share of code 2 among measured values in stays whose DRG/comorbidity implies an abnormal value | holds, strongly | code 2 share in the group vs the rest: lipase in pancreatitis 30.9% vs 1.4%; troponin I in PCI w AMI 95.0% vs 12.7%; glucose in diabetes DRG 87.8% vs 19.1%; platelets in coagulopathy 75.7% vs 17.8%; ammonia in hepatic coma 71.3% vs 29.9%; AST 80.5% vs 20.8%; bilirubin 64.2% vs 9.7%; WBC in sepsis 70.1% vs 36.2%; CK-MB in AMI 69.1% vs 20.2%; 16 of 18 pairs as predicted (exceptions: cath w ischemia without AMI, and CK in head trauma, n=14) (M). Code 2 is "abnormal" beyond doubt | CLEAN-12
18 | vitals banded as Cheng 2017 Table 2 (BMI/BP 4 bands, pulse/temp 5) | notes | WebFetch of Table 2 | holds | BMI <18.5, 18.5-24.9, 25-29.9, >=30; DBP <80, 80-89, 90-99, >=100; SBP <120, 120-139, 140-159, >160; pulse <50, 50-65, 66-80, 81-100, >100; temp <95.0, 95.0-97.6, 97.7-99.5, 99.5-104.0, >104.0 °F, each + unknown (T, via summary) |
19 | vital code 0 = unknown (72 / 75 / 123 / 5,111) | notes | counts | holds | 75 missing in DBP/SBP/pulse, 123 temp, 5,111 BMI in the README summary (M) |
20 | pulse code order contradicts Table 2 | notes | code shares + associations | holds for pulse (and temperature); refuted as a reason for keeping BMI and BP unordered (see R4) | pulse code 1 = 15.8% (cannot be <50 bpm); temperature code 2 = 80.3% (cannot be 95-97.6 °F) (M) | CLEAN-14
21 | age: 6 ordered bands, "edges not published" | notes, AGE_LEVELS | order: age-linked flags by band; edges: Cheng Table 3 shares | order holds; "edges unpublished" refuted | pregnancy 4.3%,4.3%,0.9%,0.0%,0.0%,0.0%; osteoporosis 0.8%..3.9%; prostate hyperplasia 0..4.8% (M). Bands 1-5 shares among bands 1-5 are 8.8/14.1/16.8/28.1/32.2%, against Cheng 2017's 18-25/26-35/36-45/46-55/56-64 at the same hospital, 8.5/14.6/17.3/28.9/30.7% (T+M); band 6 = 65+ | CLEAN-12
22 | race and sex codes have no words, so they are kept as codes | notes | sex: sex-specific diagnoses; race: shares vs Cheng Table 3 order | refuted (that they cannot be decoded) | sex: uterine/adnexal DRG 413/413 code 1; prostate hyperplasia 1,553/1,553 code 2; prostate cancer 99.6% code 2; uterine and ovarian cancer 100%/99.8% code 1; breast cancer 98.5% code 1, so 1 = female, 2 = male (M). race: codes 1-4 = 76.1/13.5/0.8/9.5% against Cheng's White 73.4, African American 15.2, Asian 0.9, Other 10.5% in that order (T+M) | CLEAN-12
23 | DRG and COM from UHC, "presumed available at admission"; UHC = discharge abstract | notes, issue 1 | paper; P1 vs P2 per row; outcome signature in the comorbidities | holds, and is worse than written for one column (R1) | paper quote verbatim (S). COM and DRG identical in P1 and P2 for all 76,957 rows, while history (55,819 flags) and labs change: one value per stay, not time-cut (M). HCUP: discharge APR-DRGs "include the impact of conditions that developed during the stay" (T) | LEAK-10, EV-2
24 | CABG DRGs 27% AKI | notes | rate | holds | 27.2% (n=600) and 27.4% (n=592) (M) |
25 | block ablation (LGBM 5-fold seed 0): 0.726 / 0.698 / 0.712 / 0.683 / 0.718 / 0.645 ... | notes, issue 1 | re-run with another seed (1), own script | holds | all 0.725 +/- 0.002; no DRG+COM 0.681 +/- 0.003 (M) |
26 | history = earlier records, not this stay's codes (evidence: CCS 157 at 9.1% vs 5.3%) | notes "Note:", builder LEAK-10 | DECISIVE: (a) P1 (later cut) vs P2 for the same stays; (b) does the stay's principal diagnosis appear in the history? | holds, on stronger evidence; the wording "earlier records" is imprecise | (a) P1 adds 55,819 CCS flags over P2 and removes none, so the history is cut by date (M). (b) Acute trauma stays mostly lack their own diagnosis: head trauma with coma, intracranial injury 9.3%; hip/femur trauma procedure, femoral neck fracture 17.8%. If the discharge codes were in, both would be near 100% (M). But medical admissions do carry their diagnosis in the history: pancreatitis 73.4% vs 3.3%, cellulitis 68.9% vs 4.9%, intestinal obstruction 64.0% vs 2.1%, AMI 56.7% vs 1.7%. That is diagnoses dated up to the admission day (ED, admitting team), inside the source's window. So the history is "records up to the admission day", not only "earlier records" (W1) | LEAK-10, USE-3
27 | duplicates: 72 groups, 77 extra copies, 7 conflicting | notes | test rows with an exact feature copy in train, per fold | holds | 0.11-0.14% of test rows on all 9 folds (M) | LEAK-16, LEAK-18
28 | no patient key, no dates | notes | the _clean assert maps every column to the dictionary | holds | all 303 columns are dictionary attributes (M) | SPLIT-29
29 | forced IID (a hospital would train on earlier years) | data_tags, notes | no date column | holds (inferred) | no dates. Unknown: ICD-10 history after 2015-10 (U3) | SPLIT-8
30 | metric: fallback roc_auc; paper reports 5 metrics, F-optimal threshold per model | metric reason | paper "Experimental methodology", Results, Abstract, Conclusion | facts hold; the "no deliberate choice" reading is contestable (R6) | "We used the ThresholdSelector in Weka to obtain the best classification threshold for maximum F-measure" (S), so MET-6 holds for dropping F. But windows are ranked by AUC ("The best length of prediction window is 1 day with an AUC of 0.764"), and abstract and conclusion state results in AUC only (S) | MET-5, MET-6, MET-11
31 | paper P2: ensemble 0.734, LR 0.719, RF 0.714 (with medications, 10-fold) | notes, claims | Table 2 | holds | 0.734 / 0.719 / 0.714 (S); ours 0.725 (M) |
32 | fit approximate | task_summary.fit | above | holds | add the renal-failure finding if the column is kept |
M1 | metric computable on every fold (MET-2) | spec | scorer on 9 folds: constant, random and oracle | holds | 2,419-2,420 positives per test fold; constant 0.5, random 0.488-0.506, oracle 1.0 (positive class "Yes"); no scoring columns needed (M) | MET-2
M2 | metric means what it meant at the source (MET-2) | spec | target and balance vs paper | holds | same label, same 9.4% balance, same rows (M, S). The paper scored 10-fold CV on the full 1,917-attribute set | MET-2
M3 | metric scale (MET-3) | spec | n/a | holds | binary, identity | MET-3
I1 | implied: every feature is known at the prediction point | definition | outcome signature: comorbidities "new" in this stay (no matching pre-admission CCS) vs "known" | REFUTED for comorbidity_renal_failure (R1); holds for the rest | see R1 | LEAK-10
I2 | implied: column names say what a DRG is | column_names | APR-DRG order in the dictionary | refuted for 2 procedure DRGs (R2) | see R2 | LEAK-10 (scope of issue 1), writing
I3 | implied: no copy of a row across the split | splits | per-fold exact-copy lookup | holds | 0.11-0.14% (M) | LEAK-16
I4 | implied: the split is the one the use case needs | splits | | holds as forced (SPLIT-8); repeats cannot be grouped (U2) | | SPLIT-8, SPLIT-29
I5 | implied: no same-day lab leak for AKI on the admission day | known | labs of early (<=1 d, P3 positives) vs late AKI vs none | holds (no signature) | BUN abnormal: early 18.6%, late 23.5%, none 19.7%. Early AKI does not show more abnormal kidney-linked labs (M) | LEAK-10

REFUTED OR PARTLY REFUTED, RANKED (principles.md: validity first, Must first)
-----------------------------------------------------------------------------
R1. P4, LEAK-10 (Must when strong; here a weak, measured leak). `comorbidity_renal_failure` partly records the
    stay's own outcome. In this cohort (eGFR >= 60 and SCr <= 1.3 at admission), take the stays flagged with the UHC
    "Renal failure" comorbidity and no chronic-kidney-disease history before admission (CCS 158 = 0, n=881): 28.8%
    have AKI. Stays with a known CKD history and the flag (n=899) have 16.6%, and stays without the flag 9.1%. A truly
    pre-existing condition would not be riskier when it is new to the record than when it is known. P(new flag | AKI) =
    3.5% vs 0.9% (lift 3.9). Mechanism (I): the Elixhauser renal failure comorbidity (UHC's 29 comorbidities are the
    Elixhauser set) includes ICD-9 586 "renal failure, unspecified", a code used for in-hospital kidney failure. The
    same test on the comorbidities the notes name as possibly in-stay shows no such signature (new vs known AKI rate:
    fluid and electrolyte 12.6 vs 12.0%, coagulopathy 14.9 vs 14.3%, CHF 18.0 vs 17.4%). The effect on scores is
    small: ROC AUC 0.725 -> 0.722 without the column (5-fold, seed 1, SE 0.002).
    Changes: one feature is in part a label proxy. The notes cite the wrong comorbidities as the in-stay example.
    Mildest remedy: drop `comorbidity_renal_failure` in the definition (fix, one line), whatever the curator decides on
    issue 1. In the leak note, replace "fluid and electrolyte disorders, coagulopathy" by the measured case.
R2. P4, LEAK-10, the scope of issue 1 (the curator's call stays open). The leak note's example of an in-stay
    procedure DRG is coronary bypass (27%). The DRGs with the highest AKI rates also include
    `admission_drg_infect_parasitic_disease`, 31.3% (n=469), the highest of all 61. By its place in the dictionary
    (before "POST-OP/TRAUMA INFECT PROC" and "SEPTICEMIA") it is APR-DRG 710 "Infectious & parasitic diseases incl. HIV
    w O.R. procedure". There is also `admission_drg_kidney_urin_tract_nonmalig`, 18.9% (n=513), APR-DRG 443 "Kidney &
    urinary tract procedures for nonmalignancy" (between "MAJOR BLADDER PROC" and "RENAL DIALYSIS ACCESS DEV"). The
    shipped names drop "procedure", so a reader cannot see that these are operation DRGs. Surgical DRGs (24 by name)
    are worth 0.013 ROC AUC (0.725 -> 0.712), and the medical DRGs 0.014 (-> 0.711).
    Changes: issue 1's option (c) list, and what a reader of the columns believes is known at admission.
    Mildest remedy: rename the two columns (for example `admission_drg_infect_parasitic_w_or_proc`,
    `admission_drg_kidney_urin_tract_proc_nonmalig`). Name APR-DRG 710 as the example in the leak note, and add both
    to option (c)'s procedure list.
R3. P7, CLEAN-12 (Should). Sex and race are kept as codes "without words". Sex decodes with certainty, with no
    exception in nine sex-specific diagnoses (1 = female, 2 = male; for example 1,553 of 1,553 prostate hyperplasia
    stays are code 2). Race code shares match Cheng 2017's table order for the same hospital within 2.5 points (1 =
    White, 2 = African American, 3 = Asian, 4 = Other).
    Mildest remedy: decode sex (a measured Decision); decode race the same way with its evidence, or keep it as codes
    with the evidence in the notes.
R4. P7, CLEAN-12/14 (Should). The notes say the vitals' "order of the other codes is not documented", and so all
    five stay unordered. That holds for pulse and temperature. BMI and blood pressure follow Table 2's order: 92% of
    the stays with the obesity comorbidity are in BMI band 4 (37% overall); weight loss is in band 1 for 20.7% (3.3%
    overall). Hypertension shifts systolic stays to bands 3-4 (28.9% vs 21.3%), and septicemia to band 1 (42.1% vs
    38.5%). Diastolic shares 71.8/19.5/7.1/1.4% fit <80/80-89/90-99/>=100.
    Mildest remedy: ship BMI, systolic and diastolic as ordinals with Table 2's labels (a Decision with this evidence);
    keep pulse and temperature as codes. An inferred mapping for pulse (4 = <50, 1 = 50-65, 2 = 66-80, 3 = 81-100, 5 =
    >100) and temperature (1 = <95, 5 = 95-97.6, 2 = 97.7-99.5, 3 = 99.5-104, 4 = >104) fits the shares and the sepsis
    and arrhythmia shifts, but it is not certain enough to ship.
R5. P7, CLEAN-12 (Should). "Age band edges not published." Cheng 2017 (same authors and hospital) bands 18-25, 26-35,
    36-45, 46-55, 56-64, and the shares of bands 1-5 match within 1.5 points; band 6 is 65+.
    Mildest remedy: give the likely edges in the notes (or as labels of the ordinal); the order is already right.
R6. P6, MET-5/MET-11 (Should; origin label only, no score change). The metric reason says none of the reported
    metrics "is one deliberate choice". The paper ranks the Perspective #3 windows by AUC, states its abstract result
    and conclusion only in AUC ("realistic prediction performance in cross-validated area under the curve ranging from
    0.720 to 0.764"), and asks for an index "similar to the relationship between AUC and ROC curve". The model choice
    used AUC and F-measure together. This is a weighing call, given MET-5's "a headline number in the abstract is not
    by itself a deliberate choice". roc_auc is the same either way.
    Mildest remedy: keep `fallback` but say in the reason that AUC is the paper's headline and window-ranking measure
    and why that is not counted as a deliberate choice; or declare origin `source` with original ROC AUC.
W1. Writing (no rule broken). `task_summary.known` says "192 groups of diagnoses from the patient's earlier records".
    The history includes diagnoses dated on the admission day: the stay's diagnosis is in the history for 54-84% of
    medical admissions, against 9-18% for acute trauma. That is within the source's window and known by the end of the
    admission day, so it is not a leak.
    Remedy: "... diagnoses recorded up to the admission day".

UNTESTED, RANKED
----------------
U1. P4, LEAK-10: whether UHC applied present-on-admission filtering to the comorbidities and the DRG (claim 23, T).
    No Vizient documentation was reached. R1 shows at least one comorbidity is not POA-filtered in effect. The DRG
    timing cannot be measured without coding dates. Changes issue 1 only if Vizient's coding dates or POA flags can be
    had.
U2. P4, SPLIT-29: repeat stays of one patient across folds. There is no key. The paper's pre-exclusion 179,370
    encounters of 96,590 patients make repeats certain, and the probes show no shared-unit gain (exact copies
    0.11-0.14%). README note stands; nothing to change.
U3. P4, SPLIT-8/USE-10: the paper maps "ICD9 codes" to CCS. Whether ICD-10 diagnoses after October 2015 entered the
    history is unknown (no dates). If they did not, admissions in the last ~15 months have a thinner history: a
    temporal artefact that random splits hide. Remedy: one line in the split note.
U4. Claim 8, cohort criteria: not checkable on the file (source holds).

Files: work_claim_auditor/{t1_codes,t2_history,t3_perspectives,t4_inStay,t5_ablation,t6_metric,t7_scrub}.out,
t5_ablation.json, src/paper.txt.
```

</details>

<details><summary>Column audit</summary>

```text
COLUMN AUDITOR REPORT: kumc_inpatient_aki_prediction (2026-11-08)
Definition: df-large/datasets/_dev/tabarena-v0pt2/kumc_inpatient_aki_prediction/dataset.py (read-only).
Frame: loaded through dataset_io.load(..., built=False): 76,957 x 303, every column category (age_band ordered).
Sources read: Dryad README.txt and AKI_dataset_attributes_map.xlsx; He et al. 2019 (PMC6447093, Methods); Cheng et al.
2017 (PMC5977670, the authors' earlier study on the same HERON/UHC pipeline: Tables 2 and 3, Limitations); rules
principles.md, use_case.md, leak_checks.md, cleaning_features.md (df-large copies).
Scratch (scripts and outputs): the run folder (load.py, timing.py -> timing.out, ablation.py ->
ablation.out/.json, ablation2.py -> ablation2.out/.json, ablation3.py -> ablation3.out/.json, table_flags.txt,
table_com.txt).
Prediction point (first curation bullet): the day of admission, Perspective #2, data window "(past, admission)",
label window "(admission, discharge)".

VERDICT
Ship after changes. The demographics, vitals, labs and the 192 history groups are known at the prediction point and
correctly typed. Measurements show three problems the probes cannot flag:
  (1) the renal-failure comorbidity partly encodes the outcome (LEAK-10, Must; +0.0024 ROC AUC, the same sign in 5 of
      5 folds);
  (2) the DRG block and the comorbidities that can arise during the stay are discharge-coded values the rules send
      out (LEAK-10, second clause), not "keep with a note". The source's own earlier paper says the UHC data is "not
      immediately available".
  (3) `comorbidity_diabetes_w_ccs` is not what its name says. 83% of its rows are stays with no comorbidity at all.
Lower-ranked: race, sex and age can be decoded from Cheng et al. 2017, Table 3, on evidence as strong as the lab
decoding (CLEAN-12). There are also a few naming and wording fixes.

Measured numbers below are from my scripts (untuned LightGBM, the builder's settings, 5-fold stratified, seed 0, on the
cleaned frame). On my encoding all features score 0.7234 (the builder's 0.7258 used raw integer codes).

======================================================================================================================
PROBLEMS, RANKED (principles.md: P4 before P5 before P7; Must before Should; then effect size)
======================================================================================================================

1. P4, LEAK-10 (Must), with LEAK-6. `comorbidity_renal_failure` is set by the stay's own AKI coding in part.
   Evidence (timing.out):
   - The cohort excludes eGFR < 60 or creatinine > 1.3 in the first 24 h, yet 1,780 stays carry the flag.
     42% of them (752) have no earlier renal diagnosis in the history block (CCS 157 or 158).
   - AKI rates, by the flag and the history:
       newly coded (flag set, no earlier renal record): 29.8%, 3.41 times the stays with neither (8.7%)
       flag set and an earlier renal record:            17.4%
       earlier renal record only:                       15.2%, 1.73 times the stays with neither
   - A pre-existing condition backed by earlier records should predict at least as well as a newly coded one. Here the
     reverse holds, and the gap is the largest among the 21 comorbidities I paired with history groups. For chronic
     conditions it does not appear (newly coded against history only):
       hypertension    RR 1.37 against 1.59
       diabetes w/o    RR 1.45 against 1.58
       hypothyroidism  RR 1.20 against 0.96
   - By AKI timing (the Perspective 3 label): the flag is set in 7.0% of early AKI (day 0-1), 5.1% of later AKI and
     2.0% of stays without AKI.
   - The mechanism fits the Elixhauser renal-failure code set, which (from my knowledge of the AHRQ definitions, not
     re-read) includes 586 "renal failure, unspecified" and CKD codes often added once creatinine rises. The domain
     practitioner found the same 752 / 29.8% independently.
   - Effect: dropping the column costs 0.0024 ROC AUC (paired over folds: 0.0025, 0.0032, 0.0022, 0.0019, 0.0023;
     SE 0.0002).
   - Rule: a part, a consequence or another encoding of the target goes (LEAK-10). A confirmed leak goes even when
     small (LEAK-6, santander +0.003).
   Remedy, mildest first:
   (a) Blank the flag where no earlier renal record exists (a located late value, LEAK-7 and LEAK-10's second
       clause). It keeps the 1,028 backed rows, whose information the history block already carries.
   (b) Drop the column. Simpler, and at the same cost.
   I recommend (b), or dropping it together with item 2.

2. P4, LEAK-10 (Must, second clause; weighs on LEAK-38's scope). The DRG block and the in-stay-acquirable
   comorbidities are discharge-coded values that the rules send out, not "kept with a note".

   Facts:
   - Source: He 2019 says "Comorbidity and admission diagnosis, that is, all patient refined diagnosis related group
     variables, were collected from the University Health System Consortium (UHC)" and were "presumed to be available
     at admission". The same authors' earlier paper on the same pipeline (Cheng et al. 2017, Limitations) calls the UHC
     data "widely known to be well adjudicated, but not immediately available". It says that treating UHC
     comorbidities as non-time dependent, "as if the clinical team would know all comorbidities at admission", may
     misrepresent comorbidities that developed during the admission. So the source's primary documents themselves
     present the presumption as a modelling assumption, not a fact.
   - EV-2 puts a measurement on the data first. The measurements below show that the late part exists and carries a
     gain. The builder's "the source's own document places them at admission (EV-2)" is therefore weaker than stated.

   DRG block (61 base APR-DRG flags):
   - The dictionary lists 315 groups (DRG0-DRG314) in APR-DRG number order, from liver transplant (001) to the
     ungroupable codes. A base APR-DRG is set by the grouper from the principal diagnosis ("after study") and the
     procedures done in the stay.
   - 20 of the 61 kept groups are O.R.-procedure groups. They cover 19.7% of rows and 22.6% of the AKI stays, at an
     AKI rate of 10.8% against 9.1% for the rest. They include:
       coronary bypass with cath (the cath and then the bypass in one stay): 27.2%
       coronary bypass without cath: 27.4%
       valve without cath: 21.9%
       major bowel: 15.0%
       post-op/trauma infection with procedure: 18.4%
       O.R. procedure for complications of treatment: 11.0%
   - Five more are non-O.R. procedure groups: PCI, cath and bone marrow transplant (23.7%).
   - NEW: `admission_drg_infect_parasitic_disease` is DRG261. By its place in the dictionary's APR-DRG order (between
     694 and 711, followed by 720 septicemia, 721, 722 fever, 723 viral illness and 724 other infectious) it is
     APR-DRG 710, "Infectious & parasitic diseases including HIV w O.R. procedure". One third-party page agrees on the
     title. It has the highest AKI rate of all 61 groups (31.3%, n=469): an infection admission that needed an
     operation, an event of the stay. Its shipped name hides the procedure.
   - A medical group also says "no O.R. procedure was done in this stay": a septic patient who is operated on moves
     from 720 (14.9%) to 710 (31.3%). The block cannot be cleaned group by group. Elective and emergency admissions
     cannot be told apart (no admission type in the file).
   - Measured (ablation.out, ablation2.out):
       all features:                         0.7234
       without the 20 O.R.-procedure groups: 0.7130
       without all 25 procedure groups:      0.7083
       without the whole DRG block:          0.6952
   - Note: the history block already holds much of the reason for admission. Among stays of an acute medical group,
     the matching history group is set in 44-76% (stroke 54%, pulmonary embolism 68%, GI haemorrhage 76%, sepsis 45%;
     timing.out). Dropping the DRG block therefore loses less of the use case than its 0.028 suggests.

   Comorbidities that can arise in the stay:
   - fluid and electrolyte disorders, coagulopathy, weight loss, deficiency anaemias, chronic blood loss anaemia and
     pulmonary circulation disease, besides renal failure (item 1).
   - Elixhauser comorbidities from a discharge abstract; whether UHC applied present-on-admission flags is not
     documented.
   - Same test as item 1, newly coded against history only:
       weight loss                     RR 1.71 against 1.05
       pulmonary circulation disease   RR 1.97 against 1.31
       coagulopathy                    RR 1.68 against 1.36
       deficiency anaemias             RR 1.53 against 1.35
       fluid and electrolyte disorders RR 1.48 against 1.35
     This is weaker than renal failure but the same direction. ICD-9 276.x, under fluid and electrolyte disorders,
     includes hyperkalaemia, acidosis and fluid overload, which are consequences of AKI.
   - The domain practitioner cites Glance et al. 2006: 43% of the Elixhauser coagulopathies and 25% of the fluid and
     electrolyte disorders were complications of the stay. I did not read that source.
   - Measured: without these 6 (renal failure included) 0.7179 (-0.0055); also without the O.R. groups 0.7062.

   Rules:
   - LEAK-10's second clause: late values that can be located are blanked. Where they cannot be located row by row,
     they go when they may carry a gain, and stay with a note only when the part that can be traced shows none. Here
     the traceable parts (the procedure groups, the newly coded renal failure) show a gain.
   - LEAK-38 (keep with a note) does not apply: this is no data owner's competition release, and the timing is
     documented as late (the authors' own "not immediately available").
   - Precedents: mic, an admission-time task, keeps only "complications present on admission"; kickstarter dropped
     `staff_pick` once the task was "predict at launch".

   Remedy options, mildest that complies first:
   (c') Drop the DRG block and the 7 acquirable comorbidities (item 1's column among them). Keep the 20 chronic
        comorbidities (hypertension, diabetes, COPD, cancers, CHF, ...), which are pre-existing in substance.
        ROC AUC 0.6882 (ablation3.out).
   (c)  Drop only the 25 procedure groups and the acquirable comorbidities, about 0.706. It leaves the medical groups'
        "no operation" signal and their after-study diagnosis, so it does not fully resolve the problem.
   (b)  Drop both blocks: 0.6809 (builder 0.683).
   The builder's (a), keep with a note at 0.726, departs from a Must without a higher-ranked rule. Under the
   consistency rule (principles.md) it should come to the curator as a question.
   My recommendation: (c'), naming the cost of 0.035 ROC AUC, with the fit_reason updated. If the curator keeps (a),
   it should be recorded as such a departure, with the renal-failure column still dropped (item 1 is a located
   consequence of the target).

3. P5 (faithful data; PROV-13 kind) and CLEAN-12 naming. Question for the curator: `comorbidity_diabetes_w_ccs` (COM0,
   "Diabetes w/CCs") is a mixture of "no comorbidity" and complicated diabetes.
   Evidence:
   - Of its 14,107 rows, 11,759 (83.4%) have no other comorbidity flag, against 0.1% of the other rows.
   - Of the 11,814 stays with no other comorbidity, 99.5% have it set.
   - Those 11,759 rows look nothing like diabetes:
       earlier diabetes record (CCS 49/50): 2.4% / 0.8%
       abnormal glucose: 11.1% (12.2% for stays with no diabetes flag)
       AKI: 5.1%
   - The other 2,348 rows are complicated diabetes:
       earlier diabetes record (CCS 49/50): 64% / 36%
       abnormal glucose: 57%
       AKI: 16.8%
   - The column as a whole: AKI 7.1% (below the base rate), hypertension 11.6% against about 50% elsewhere, obesity
     4.6%. COM1 (hypothyroidism) and COM2 (renal failure) match their history groups, so this is no shift of the whole
     block. The deposit's encoding seems to have put the "none" state into COM0.
   Effect: no leak and no information lost for a model. The name and the notes ("27 comorbidities") misstate what the
   column is.
   Remedy, mildest: rename it (for example `comorbidity_diabetes_w_ccs_or_none`) and add a notes bullet with these
   numbers. It cannot be split losslessly, since a diabetic stay with no other comorbidity cannot be told from a stay
   with none. Optionally ask the authors (meiliu@kumc.edu).

4. P7, CLEAN-12 (Should). `race_code`, `sex_code` and `age_band` can be decoded from Cheng et al. 2017, Table 3, by the
   same evidence standard the definition uses for the labs. Cheng's cohort is a subset of the same KUMC/HERON
   population (2007-2016, 18-64 years, n=48,955). Comparing shares and AKI rates (ours | Cheng):
   - Sex: code 1 45.2% at 8.5% AKI | Female 45.6% at 8.0%. Code 2 54.8% at 10.2% | Male 54.4% at 9.9%.
     So 1 = Female, 2 = Male, the table's order.
   - Race: shares 76.1 / 13.5 / 0.85 / 9.5% | White 73.2, African American 15.3, Asian 0.87, Other 10.6%. The AKI
     rates rank the same way (Asian lowest, then White, Other, African American): ours 8.3 < 9.2 < 10.0 < 10.2 |
     Cheng 7.3 < 8.75 < 9.6 < 9.8. So 1 White, 2 African American, 3 Asian, 4 Other, the table's order.
   - Age: AKI rate by band, ours | Cheng:
       band 1:  7.2% | 18-25  7.0%
       band 2:  7.3% | 26-35  7.3%
       band 3:  8.6% | 36-45  8.7%
       band 4:  8.9% | 46-55  9.2%
       band 5: 10.5% | 56-64 10.4%
     Band 6 is then 65 and older (He's cohort is adults over 18 with no upper limit; Cheng's stops at 64). The notes
     say "edges not published", which is inaccurate: five of the six are published by the same authors.
   Remedy: decode the three columns into the words, with a Decision table like the labs' (age as the ordered labels
   18-25 ... 65+). If not done, correct the notes.

5. P7, CLEAN-14 / CLEAN-12 (Should; agree with the builder). The vital bands stay unordered codes. The dtype probe
   flagged `numeric_levels` on the 5 bands and `race_code`; race is answered in item 4. For the vitals, the code order
   is not documented and is not one rule:
   - BMI and both blood pressures fit the table's order by frequency: BMI 3.5 / 28 / 29 / 39% of known values; diastolic
     72 / 20 / 7 / 1.4%; systolic 39 / 40 / 18 / 3%.
   - Pulse fits 1 [50-65], 2 [66-80], 3 [81-100], 4 <50 (0.5%, AKI 19%), 5 >100 (10%, AKI 12.3%), with the extremes
     last.
   - Temperature fits 1 <95 (n=104, AKI 34.6%), 2 [97.7-99.5], 3 [99.5-104], 4 >104 (n=9), 5 [95.0-97.6], with the
     extremes not last.
   An order still unclear after the sources stays unordered with a note (CLEAN-14). Keep, and add the inferred
   mappings to the notes as unverified.
   Cosmetic: after set_missing the five bands' categories are floats (1.0 ... 5.0) while race and sex are integers.
   Cast them to integers before typing.

6. P7, naming and wording (cosmetic; writing.md):
   - `admission_drg_infect_parasitic_disease` should say "w O.R. procedure" (item 2).
   - `admission_drg_cardiac_valve_proc_w_0_cath` carries the dictionary's "W/0" typo; read it as w_o_cath.
   - `admission_drg_head_trauma_w_coma_1_hr` lost the ">".
   - `comorbidity_coagulopthy` keeps the dictionary's typo.
   - task_summary.known says "192 groups of diagnoses from the patient's earlier records". The data shows that the
     history holds diagnoses up to the admission day, plausibly the same episode's ED or admission-day encounter
     codes. In stays of an acute medical group the matching group is set in 44-76% (pulmonary embolism 68%, acute MI
     with PCI 57%, against base rates of 2-7%). The stay's final billing codes are not in it: in elective hip and knee
     replacement stays, osteoarthritis is flagged in only 27% / 42%, and CCS 157 is flagged in 9.1% of AKI stays. All
     of this is known at the prediction point, so it is fine, but the wording should read "diagnoses recorded up to
     the admission day".

Measured and fine (no action):
- Admission-day labs do not look post-onset. Among early AKI (AKI within one day, Perspective 3 label, n=1,611), BUN
  is abnormal in 18.6%, the same as in stays without AKI (18.4%) and below later AKI (22.0%). A BUN drawn after the
  creatinine rise would run higher. This answers the builder's checklist concern (LEAK-10, the same-day clause).
- Lab missingness follows measurement intensity. BUN is unknown in 0.1% of early AKI, 6.3% of later AKI and 6.8% of
  stays without AKI: an AKI found on day 0-1 needs an admission-day panel. The missing-indicator probe tops at 0.536,
  and the team knows at admission whether labs were drawn. Not a leak; it could go in a notes line.
- The lab decoding (0 unknown -> missing, 1 normal, 2 abnormal) is well supported (Decision table); typed unordered
  categorical, which is right.
- The 0/1 flags typed categorical are right (CLEAN-14). The target is No/Yes (CLEAN-25).

======================================================================================================================
COLUMN TABLE (column | meaning | known at prediction? | dtype and cleaning | verdict | rule)
======================================================================================================================
Demographics, vitals, labs (22):
age_band | age band, 6 levels; per Cheng 2017 T3: 18-25, 26-35, 36-45, 46-55, 56-64, (65+) | yes | ordered category 1-6, order right; labels recoverable | fine; decode labels (item 4) | CLEAN-12, CLEAN-14
race_code | race; per Cheng T3 shares and rates 1 White, 2 African American, 3 Asian, 4 Other | yes | unordered category of codes | cleaning: decode (item 4) | CLEAN-12
sex_code | sex; 1 Female, 2 Male (Cheng T3) | yes | unordered category of codes | cleaning: decode (item 4) | CLEAN-12
bmi_band | BMI band (Cheng T2: <18.5, 18.5-24.9, 25-29.9, >=30), last value up to admission; 0 unknown -> NaN (5,111) | yes | unordered category, float codes | fine (keep codes, note inferred order; int cast) | CLEAN-14, CLEAN-10
diastolic_bp_band | diastolic BP band (<80, 80-89, 90-99, >=100); 0 -> NaN (75) | yes | as bmi_band | fine (note) | CLEAN-14
systolic_bp_band | systolic BP band (<120, 120-139, 140-159, >=160); 0 -> NaN (75) | yes | as bmi_band | fine (note) | CLEAN-14
pulse_band | pulse band (<50, 50-65, 66-80, 81-100, >100); code order not the table's; 0 -> NaN (75) | yes | unordered category | fine (note inferred mapping) | CLEAN-14
temperature_band | temperature band (<95, 95-97.6, 97.7-99.5, 99.5-104, >104 F); order unclear; 0 -> NaN (123) | yes | unordered category | fine (note) | CLEAN-14
lab_albumin | albumin within 3.5-5.5 or not, last value up to admission day; not done -> NaN | yes (admission-day labs precede early AKI per BUN test) | category normal/abnormal | fine | CLEAN-10, CLEAN-12
lab_alt | ALT 7-56 | yes | as above | fine | CLEAN-12
lab_ast | AST 10-40 | yes | as above | fine | CLEAN-12
lab_ammonia | ammonia 10-65 (97% not done) | yes | as above | fine | CLEAN-12
lab_calcium | calcium 8.5-10.2 | yes | as above | fine | CLEAN-12
lab_bun | BUN 7-20 mg/dL | yes (early AKI not raised: 18.6% vs 18.4%) | as above | fine | CLEAN-12, LEAK-10 checked
lab_total_bilirubin | total bilirubin 0.3-1.9 | yes | as above | fine | CLEAN-12
lab_ck_mb | CK-MB (sex-specific limit) | yes | as above | fine | CLEAN-12
lab_ck | CK (sex-specific range) | yes | as above | fine | CLEAN-12
lab_glucose | glucose 80-160 | yes | as above | fine | CLEAN-12
lab_lipase | lipase 0-400 | yes | as above | fine | CLEAN-12
lab_platelets | platelets 150-450 | yes | as above | fine | CLEAN-12
lab_troponin_i | troponin I 0-0.06 | yes | as above | fine | CLEAN-12
lab_wbc | WBC 3.5-10.5 | yes | as above | fine | CLEAN-12
Target: aki_during_stay | KDIGO creatinine AKI, any day to discharge, No/Yes | target | category | fine | CLEAN-25

Admission diagnosis, base APR-DRG (61) [n and AKI rate from the data; "often planned" is my reading of the group]:
admission_drg_bone_marrow_transplant | base APR-DRG, non-O.R. procedure group; n=524, AKI 0.237 | partly (planned cath/PCI/BMT yes, after an emergency no) | 0/1 category, fine | leak, LEAK-10 (weak) | LEAK-10, LEAK-6
admission_drg_craniotomy_exc_for_trauma | base APR-DRG, O.R.-procedure group (often planned); n=1495, AKI 0.052 | no as coded; yes only for a planned operation | 0/1 category, fine | leak, LEAK-10 (procedure in the stay) | LEAK-10, LEAK-6
admission_drg_cva_w_infarct | base APR-DRG, medical group (principal dx after study); n=828, AKI 0.065 | mostly (working dx), final group only at discharge; also encodes no O.R. procedure | 0/1 category, fine | leak, LEAK-10 (weak, block) | LEAK-10, LEAK-6
admission_drg_seizure | base APR-DRG, medical group (principal dx after study); n=809, AKI 0.052 | mostly (working dx), final group only at discharge; also encodes no O.R. procedure | 0/1 category, fine | leak, LEAK-10 (weak, block) | LEAK-10, LEAK-6
admission_drg_migraine_other_headache | base APR-DRG, medical group (principal dx after study); n=406, AKI 0.037 | mostly (working dx), final group only at discharge; also encodes no O.R. procedure | 0/1 category, fine | leak, LEAK-10 (weak, block) | LEAK-10, LEAK-6
admission_drg_head_trauma_w_coma_1_hr | base APR-DRG, medical group (principal dx after study); n=398, AKI 0.068 | mostly (working dx), final group only at discharge; also encodes no O.R. procedure | 0/1 category, fine | leak, LEAK-10 (weak, block) | LEAK-10, LEAK-6
admission_drg_oth_disorders_nervous_sys | base APR-DRG, medical group (principal dx after study); n=597, AKI 0.039 | mostly (working dx), final group only at discharge; also encodes no O.R. procedure | 0/1 category, fine | leak, LEAK-10 (weak, block) | LEAK-10, LEAK-6
admission_drg_cystic_fibrosis | base APR-DRG, medical group (principal dx after study); n=884, AKI 0.173 | mostly (working dx), final group only at discharge; also encodes no O.R. procedure | 0/1 category, fine | leak, LEAK-10 (weak, block) | LEAK-10, LEAK-6
admission_drg_pulmonary_edema_resp_fail | base APR-DRG, medical group (principal dx after study); n=619, AKI 0.126 | mostly (working dx), final group only at discharge; also encodes no O.R. procedure | 0/1 category, fine | leak, LEAK-10 (weak, block) | LEAK-10, LEAK-6
admission_drg_pulmonary_embolism | base APR-DRG, medical group (principal dx after study); n=466, AKI 0.084 | mostly (working dx), final group only at discharge; also encodes no O.R. procedure | 0/1 category, fine | leak, LEAK-10 (weak, block) | LEAK-10, LEAK-6
admission_drg_other_pneumonia | base APR-DRG, medical group (principal dx after study); n=921, AKI 0.089 | mostly (working dx), final group only at discharge; also encodes no O.R. procedure | 0/1 category, fine | leak, LEAK-10 (weak, block) | LEAK-10, LEAK-6
admission_drg_chronic_obstructive_pulm_dis | base APR-DRG, medical group (principal dx after study); n=789, AKI 0.072 | mostly (working dx), final group only at discharge; also encodes no O.R. procedure | 0/1 category, fine | leak, LEAK-10 (weak, block) | LEAK-10, LEAK-6
admission_drg_cardiac_valve_proc_w_0_cath | base APR-DRG, O.R.-procedure group (often planned); n=631, AKI 0.219 | no as coded; yes only for a planned operation | 0/1 category, fine | leak, LEAK-10 (procedure in the stay) | LEAK-10, LEAK-6
admission_drg_coronary_bypass_w_card_cath | base APR-DRG, O.R.-procedure group (procedure decided in the stay); n=600, AKI 0.272 | no as coded; yes only for a planned operation | 0/1 category, fine | leak, LEAK-10 (procedure in the stay) | LEAK-10, LEAK-6
admission_drg_cor_bypass_w_o_card_cath | base APR-DRG, O.R.-procedure group (often planned); n=592, AKI 0.274 | no as coded; yes only for a planned operation | 0/1 category, fine | leak, LEAK-10 (procedure in the stay) | LEAK-10, LEAK-6
admission_drg_other_vascular_procedures | base APR-DRG, O.R.-procedure group (often planned); n=572, AKI 0.121 | no as coded; yes only for a planned operation | 0/1 category, fine | leak, LEAK-10 (procedure in the stay) | LEAK-10, LEAK-6
admission_drg_percut_cardiovasc_proc_w_ami | base APR-DRG, non-O.R. procedure group; n=677, AKI 0.078 | partly (planned cath/PCI/BMT yes, after an emergency no) | 0/1 category, fine | leak, LEAK-10 (weak) | LEAK-10, LEAK-6
admission_drg_percut_cardiovasc_w_o_ami | base APR-DRG, non-O.R. procedure group; n=1218, AKI 0.077 | partly (planned cath/PCI/BMT yes, after an emergency no) | 0/1 category, fine | leak, LEAK-10 (weak) | LEAK-10, LEAK-6
admission_drg_card_cathet_exc_ischemia | base APR-DRG, non-O.R. procedure group; n=573, AKI 0.119 | partly (planned cath/PCI/BMT yes, after an emergency no) | 0/1 category, fine | leak, LEAK-10 (weak) | LEAK-10, LEAK-6
admission_drg_card_cathet_w_ischemia | base APR-DRG, non-O.R. procedure group; n=677, AKI 0.035 | partly (planned cath/PCI/BMT yes, after an emergency no) | 0/1 category, fine | leak, LEAK-10 (weak) | LEAK-10, LEAK-6
admission_drg_heart_failure | base APR-DRG, medical group (principal dx after study); n=693, AKI 0.215 | mostly (working dx), final group only at discharge; also encodes no O.R. procedure | 0/1 category, fine | leak, LEAK-10 (weak, block) | LEAK-10, LEAK-6
admission_drg_peripheral_oth_vasc_dis | base APR-DRG, medical group (principal dx after study); n=410, AKI 0.071 | mostly (working dx), final group only at discharge; also encodes no O.R. procedure | 0/1 category, fine | leak, LEAK-10 (weak, block) | LEAK-10, LEAK-6
admission_drg_card_arrhythmia_conduction | base APR-DRG, medical group (principal dx after study); n=1404, AKI 0.033 | mostly (working dx), final group only at discharge; also encodes no O.R. procedure | 0/1 category, fine | leak, LEAK-10 (weak, block) | LEAK-10, LEAK-6
admission_drg_maj_stom_esoph_duod_proc | base APR-DRG, O.R.-procedure group (often planned); n=496, AKI 0.147 | no as coded; yes only for a planned operation | 0/1 category, fine | leak, LEAK-10 (procedure in the stay) | LEAK-10, LEAK-6
admission_drg_maj_small_large_bowel_proc | base APR-DRG, O.R.-procedure group (often planned); n=1144, AKI 0.150 | no as coded; yes only for a planned operation | 0/1 category, fine | leak, LEAK-10 (procedure in the stay) | LEAK-10, LEAK-6
admission_drg_hernia_proc_exc_inguinal_fem | base APR-DRG, O.R.-procedure group (often planned); n=448, AKI 0.094 | no as coded; yes only for a planned operation | 0/1 category, fine | leak, LEAK-10 (procedure in the stay) | LEAK-10, LEAK-6
admission_drg_inflammatory_bowel_disease | base APR-DRG, medical group (principal dx after study); n=410, AKI 0.029 | mostly (working dx), final group only at discharge; also encodes no O.R. procedure | 0/1 category, fine | leak, LEAK-10 (weak, block) | LEAK-10, LEAK-6
admission_drg_intestinal_obstruction | base APR-DRG, medical group (principal dx after study); n=698, AKI 0.040 | mostly (working dx), final group only at discharge; also encodes no O.R. procedure | 0/1 category, fine | leak, LEAK-10 (weak, block) | LEAK-10, LEAK-6
admission_drg_major_gi_infections | base APR-DRG, medical group (principal dx after study); n=468, AKI 0.092 | mostly (working dx), final group only at discharge; also encodes no O.R. procedure | 0/1 category, fine | leak, LEAK-10 (weak, block) | LEAK-10, LEAK-6
admission_drg_non_bacterial_gi | base APR-DRG, medical group (principal dx after study); n=636, AKI 0.033 | mostly (working dx), final group only at discharge; also encodes no O.R. procedure | 0/1 category, fine | leak, LEAK-10 (weak, block) | LEAK-10, LEAK-6
admission_drg_abdominal_pain | base APR-DRG, medical group (principal dx after study); n=421, AKI 0.045 | mostly (working dx), final group only at discharge; also encodes no O.R. procedure | 0/1 category, fine | leak, LEAK-10 (weak, block) | LEAK-10, LEAK-6
admission_drg_oth_unspec_gi_hemorrhage | base APR-DRG, medical group (principal dx after study); n=485, AKI 0.045 | mostly (working dx), final group only at discharge; also encodes no O.R. procedure | 0/1 category, fine | leak, LEAK-10 (weak, block) | LEAK-10, LEAK-6
admission_drg_oth_digestive_system_diag | base APR-DRG, medical group (principal dx after study); n=1141, AKI 0.042 | mostly (working dx), final group only at discharge; also encodes no O.R. procedure | 0/1 category, fine | leak, LEAK-10 (weak, block) | LEAK-10, LEAK-6
admission_drg_maj_pancreas_liver_shunt_proc | base APR-DRG, O.R.-procedure group (often planned); n=534, AKI 0.116 | no as coded; yes only for a planned operation | 0/1 category, fine | leak, LEAK-10 (procedure in the stay) | LEAK-10, LEAK-6
admission_drg_hepatic_coma_oth_maj_liv_dis | base APR-DRG, medical group (principal dx after study); n=684, AKI 0.098 | mostly (working dx), final group only at discharge; also encodes no O.R. procedure | 0/1 category, fine | leak, LEAK-10 (weak, block) | LEAK-10, LEAK-6
admission_drg_pancreas_disord_exc_malig | base APR-DRG, medical group (principal dx after study); n=768, AKI 0.036 | mostly (working dx), final group only at discharge; also encodes no O.R. procedure | 0/1 category, fine | leak, LEAK-10 (weak, block) | LEAK-10, LEAK-6
admission_drg_other_disorders_of_liver | base APR-DRG, medical group (principal dx after study); n=411, AKI 0.095 | mostly (working dx), final group only at discharge; also encodes no O.R. procedure | 0/1 category, fine | leak, LEAK-10 (weak, block) | LEAK-10, LEAK-6
admission_drg_disorders_of_gallbladder | base APR-DRG, medical group (principal dx after study); n=486, AKI 0.084 | mostly (working dx), final group only at discharge; also encodes no O.R. procedure | 0/1 category, fine | leak, LEAK-10 (weak, block) | LEAK-10, LEAK-6
admission_drg_hip_joint_replacement | base APR-DRG, O.R.-procedure group (often planned); n=1681, AKI 0.069 | no as coded; yes only for a planned operation | 0/1 category, fine | leak, LEAK-10 (procedure in the stay) | LEAK-10, LEAK-6
admission_drg_knee_joint_replacement | base APR-DRG, O.R.-procedure group (often planned); n=1747, AKI 0.041 | no as coded; yes only for a planned operation | 0/1 category, fine | leak, LEAK-10 (procedure in the stay) | LEAK-10, LEAK-6
admission_drg_dor_lumb_fus_exc_crv_bck | base APR-DRG, O.R.-procedure group (often planned); n=963, AKI 0.067 | no as coded; yes only for a planned operation | 0/1 category, fine | leak, LEAK-10 (procedure in the stay) | LEAK-10, LEAK-6
admission_drg_hip_femur_proc_traum | base APR-DRG, O.R.-procedure group (procedure decided in the stay); n=465, AKI 0.071 | no as coded; yes only for a planned operation | 0/1 category, fine | leak, LEAK-10 (procedure in the stay) | LEAK-10, LEAK-6
admission_drg_intervertebral_disc_excision | base APR-DRG, O.R.-procedure group (often planned); n=448, AKI 0.056 | no as coded; yes only for a planned operation | 0/1 category, fine | leak, LEAK-10 (procedure in the stay) | LEAK-10, LEAK-6
admission_drg_knee_lower_leg_proc | base APR-DRG, O.R.-procedure group (often planned); n=1044, AKI 0.041 | no as coded; yes only for a planned operation | 0/1 category, fine | leak, LEAK-10 (procedure in the stay) | LEAK-10, LEAK-6
admission_drg_shoulder_up_arm_forearm_proc | base APR-DRG, O.R.-procedure group (often planned); n=494, AKI 0.063 | no as coded; yes only for a planned operation | 0/1 category, fine | leak, LEAK-10 (procedure in the stay) | LEAK-10, LEAK-6
admission_drg_back_neck_disorders | base APR-DRG, medical group (principal dx after study); n=593, AKI 0.049 | mostly (working dx), final group only at discharge; also encodes no O.R. procedure | 0/1 category, fine | leak, LEAK-10 (weak, block) | LEAK-10, LEAK-6
admission_drg_cellulitis_other_bact_inf | base APR-DRG, medical group (principal dx after study); n=1042, AKI 0.084 | mostly (working dx), final group only at discharge; also encodes no O.R. procedure | 0/1 category, fine | leak, LEAK-10 (weak, block) | LEAK-10, LEAK-6
admission_drg_diabetes | base APR-DRG, medical group (principal dx after study); n=418, AKI 0.057 | mostly (working dx), final group only at discharge; also encodes no O.R. procedure | 0/1 category, fine | leak, LEAK-10 (weak, block) | LEAK-10, LEAK-6
admission_drg_kidney_urin_tract_nonmalig | base APR-DRG, medical group (principal dx after study); n=513, AKI 0.189 | mostly (working dx), final group only at discharge; also encodes no O.R. procedure | 0/1 category, fine | leak, LEAK-10 (weak, block) | LEAK-10, LEAK-6
admission_drg_kidney_urin_tract_infect | base APR-DRG, medical group (principal dx after study); n=640, AKI 0.053 | mostly (working dx), final group only at discharge; also encodes no O.R. procedure | 0/1 category, fine | leak, LEAK-10 (weak, block) | LEAK-10, LEAK-6
admission_drg_uter_adnex_exc_leiomyoma | base APR-DRG, O.R.-procedure group (often planned); n=413, AKI 0.039 | no as coded; yes only for a planned operation | 0/1 category, fine | leak, LEAK-10 (procedure in the stay) | LEAK-10, LEAK-6
admission_drg_maj_hematologic_immunol_dx | base APR-DRG, medical group (principal dx after study); n=617, AKI 0.081 | mostly (working dx), final group only at discharge; also encodes no O.R. procedure | 0/1 category, fine | leak, LEAK-10 (weak, block) | LEAK-10, LEAK-6
admission_drg_chemotherapy | base APR-DRG, medical group (principal dx after study); n=1811, AKI 0.147 | mostly (working dx), final group only at discharge; also encodes no O.R. procedure | 0/1 category, fine | leak, LEAK-10 (weak, block) | LEAK-10, LEAK-6
admission_drg_infect_parasitic_disease | base APR-DRG, O.R.-procedure group (procedure decided in the stay); n=469, AKI 0.313 | no as coded; yes only for a planned operation | 0/1 category, fine | leak, LEAK-10 (procedure in the stay) | LEAK-10, LEAK-6
admission_drg_post_op_trauma_infect_proc | base APR-DRG, O.R.-procedure group (procedure decided in the stay); n=463, AKI 0.184 | no as coded; yes only for a planned operation | 0/1 category, fine | leak, LEAK-10 (procedure in the stay) | LEAK-10, LEAK-6
admission_drg_septicemia_dissem_infect | base APR-DRG, medical group (principal dx after study); n=2845, AKI 0.149 | mostly (working dx), final group only at discharge; also encodes no O.R. procedure | 0/1 category, fine | leak, LEAK-10 (weak, block) | LEAK-10, LEAK-6
admission_drg_post_op_post_traum_infec | base APR-DRG, medical group (principal dx after study); n=787, AKI 0.109 | mostly (working dx), final group only at discharge; also encodes no O.R. procedure | 0/1 category, fine | leak, LEAK-10 (weak, block) | LEAK-10, LEAK-6
admission_drg_alcohol_abuse_dependence | base APR-DRG, medical group (principal dx after study); n=515, AKI 0.023 | mostly (working dx), final group only at discharge; also encodes no O.R. procedure | 0/1 category, fine | leak, LEAK-10 (weak, block) | LEAK-10, LEAK-6
admission_drg_o_r_proc_oth_comp_treat | base APR-DRG, O.R.-procedure group (procedure decided in the stay); n=427, AKI 0.110 | no as coded; yes only for a planned operation | 0/1 category, fine | leak, LEAK-10 (procedure in the stay) | LEAK-10, LEAK-6
admission_drg_oth_comp_of_treatment | base APR-DRG, medical group (principal dx after study); n=453, AKI 0.068 | mostly (working dx), final group only at discharge; also encodes no O.R. procedure | 0/1 category, fine | leak, LEAK-10 (weak, block) | LEAK-10, LEAK-6
admission_drg_rehabilitation | base APR-DRG, medical group (principal dx after study); n=1919, AKI 0.071 | mostly (working dx), final group only at discharge; also encodes no O.R. procedure | 0/1 category, fine | leak, LEAK-10 (weak, block) | LEAK-10, LEAK-6

Comorbidities, UHC / Elixhauser, from the discharge abstract (27):
comorbidity_diabetes_w_ccs | Elixhauser diabetes with chronic complications per the dictionary; DATA: 83% of its rows have no other comorbidity (a mixture of no comorbidity and complicated diabetes); n=14107, AKI 0.071 | pre-existing (as diabetes); the none-state is a coding artefact of the discharge abstract | 0/1 category, fine | question for the curator: name contradicts data (rename, note) | PROV-13/CLEAN-12 naming
comorbidity_hypothyroidism | Elixhauser comorbidity (UHC, discharge abstract); n=8704, AKI 0.105 | pre-existing chronic condition: yes in substance (coded at discharge) | 0/1 category, fine | fine (keep, block note) | LEAK-10 note
comorbidity_renal_failure | Elixhauser renal failure (ICD-9 585, 586, V42.0, V45.1, V56, 403.x1, 404.x2/x3); n=1780, AKI 0.226 | NO for 752 newly coded stays: AKI 29.8% vs 17.4% with prior renal record | 0/1 category, fine | leak, LEAK-10 Must (a consequence/encoding of the target), +0.0024 AUC 5/5 folds: drop | LEAK-10, LEAK-6
comorbidity_liver_disease | Elixhauser comorbidity (UHC, discharge abstract); n=4731, AKI 0.147 | pre-existing chronic condition: yes in substance (coded at discharge) | 0/1 category, fine | fine (keep, block note) | LEAK-10 note
comorbidity_lymphoma | Elixhauser comorbidity (UHC, discharge abstract); n=1288, AKI 0.108 | pre-existing chronic condition: yes in substance (coded at discharge) | 0/1 category, fine | fine (keep, block note) | LEAK-10 note
comorbidity_metastatic_cancer | Elixhauser comorbidity (UHC, discharge abstract); n=3703, AKI 0.132 | pre-existing chronic condition: yes in substance (coded at discharge) | 0/1 category, fine | fine (keep, block note) | LEAK-10 note
comorbidity_solid_tumor_w_o_metas | Elixhauser comorbidity (UHC, discharge abstract); n=2854, AKI 0.109 | pre-existing chronic condition: yes in substance (coded at discharge) | 0/1 category, fine | fine (keep, block note) | LEAK-10 note
comorbidity_rheum_arthr_collagen_vas | Elixhauser comorbidity (UHC, discharge abstract); n=2671, AKI 0.106 | pre-existing chronic condition: yes in substance (coded at discharge) | 0/1 category, fine | fine (keep, block note) | LEAK-10 note
comorbidity_congestive_heart_failure | Elixhauser CHF; n=3398, AKI 0.177 | mostly pre-existing; acute HF in the stay possible (RR new 2.05 vs history-only 1.96, no excess) | 0/1 category, fine | fine, with the block note | LEAK-10 note
comorbidity_coagulopthy | Elixhauser coagulopathy; n=5135, AKI 0.147 | uncertain: often arises in the stay (new-coded RR 1.68 vs history-only 1.36) | 0/1 category, fine | leak, LEAK-10 (weak), drop with the acquirable set | LEAK-10 2nd clause
comorbidity_obesity | Elixhauser comorbidity (UHC, discharge abstract); n=9635, AKI 0.129 | pre-existing chronic condition: yes in substance (coded at discharge) | 0/1 category, fine | fine (keep, block note) | LEAK-10 note
comorbidity_weight_loss | Elixhauser weight loss / malnutrition; n=4352, AKI 0.155 | uncertain: coded in the stay (new-coded RR 1.71 vs history-only 1.05) | 0/1 category, fine | leak, LEAK-10 (weak), drop with the acquirable set | LEAK-10 2nd clause
comorbidity_fluid_and_electr_disorders | Elixhauser fluid and electrolyte disorders (ICD-9 276.x: incl. hyperkalaemia, acidosis, fluid overload); n=13812, AKI 0.124 | uncertain: often arises in the stay; AKI consequences coded here | 0/1 category, fine | leak, LEAK-10 (weak), drop with the acquirable set | LEAK-10 2nd clause
comorbidity_chronic_blood_loss_anemia | Elixhauser chronic blood loss anaemia; n=444, AKI 0.126 | uncertain | 0/1 category, fine | leak, LEAK-10 (weak), drop with the acquirable set | LEAK-10 2nd clause
comorbidity_deficiency_anemias | Elixhauser deficiency anaemias (incl. 285.9 anaemia unspecified); n=10464, AKI 0.129 | uncertain: can arise in the stay | 0/1 category, fine | leak, LEAK-10 (weak), drop with the acquirable set | LEAK-10 2nd clause
comorbidity_alcohol_abuse | Elixhauser comorbidity (UHC, discharge abstract); n=4151, AKI 0.113 | pre-existing chronic condition: yes in substance (coded at discharge) | 0/1 category, fine | fine (keep, block note) | LEAK-10 note
comorbidity_drug_abuse | Elixhauser comorbidity (UHC, discharge abstract); n=2936, AKI 0.085 | pre-existing chronic condition: yes in substance (coded at discharge) | 0/1 category, fine | fine (keep, block note) | LEAK-10 note
comorbidity_psychoses | Elixhauser comorbidity (UHC, discharge abstract); n=3646, AKI 0.094 | pre-existing chronic condition: yes in substance (coded at discharge) | 0/1 category, fine | fine (keep, block note) | LEAK-10 note
comorbidity_depression | Elixhauser comorbidity (UHC, discharge abstract); n=12268, AKI 0.099 | pre-existing chronic condition: yes in substance (coded at discharge) | 0/1 category, fine | fine (keep, block note) | LEAK-10 note
comorbidity_valvular_disease | Elixhauser comorbidity (UHC, discharge abstract); n=2097, AKI 0.140 | pre-existing chronic condition: yes in substance (coded at discharge) | 0/1 category, fine | fine (keep, block note) | LEAK-10 note
comorbidity_pulmonary_circulation_disease | Elixhauser pulmonary circulation disorders (PE, pulmonary hypertension); n=1491, AKI 0.171 | uncertain: in-stay PE coded here (new-coded RR 1.97 vs history-only 1.31) | 0/1 category, fine | leak, LEAK-10 (weak), drop with the acquirable set | LEAK-10 2nd clause
comorbidity_peripheral_vascular_disease | Elixhauser comorbidity (UHC, discharge abstract); n=3239, AKI 0.150 | pre-existing chronic condition: yes in substance (coded at discharge) | 0/1 category, fine | fine (keep, block note) | LEAK-10 note
comorbidity_hypertension | Elixhauser comorbidity (UHC, discharge abstract); n=35794, AKI 0.108 | pre-existing chronic condition: yes in substance (coded at discharge) | 0/1 category, fine | fine (keep, block note) | LEAK-10 note
comorbidity_paralysis | Elixhauser comorbidity (UHC, discharge abstract); n=2047, AKI 0.096 | pre-existing chronic condition: yes in substance (coded at discharge) | 0/1 category, fine | fine (keep, block note) | LEAK-10 note
comorbidity_other_neurological_disorders | Elixhauser comorbidity (UHC, discharge abstract); n=4831, AKI 0.095 | pre-existing chronic condition: yes in substance (coded at discharge) | 0/1 category, fine | fine (keep, block note) | LEAK-10 note
comorbidity_chronic_pulmonary_disease | Elixhauser comorbidity (UHC, discharge abstract); n=12725, AKI 0.121 | pre-existing chronic condition: yes in substance (coded at discharge) | 0/1 category, fine | fine (keep, block note) | LEAK-10 note
comorbidity_diabetes_w_o_ccs | Elixhauser comorbidity (UHC, discharge abstract); n=13608, AKI 0.126 | pre-existing chronic condition: yes in substance (coded at discharge) | 0/1 category, fine | fine (keep, block note) | LEAK-10 note

Medical history, AHRQ CCS single-level groups of ICD-9 diagnoses recorded up to the admission day (192), one row for
the block (every column has the same meaning, timing, dtype and verdict):
history_ccs<code>_<name> (192 columns, from history_ccs217_other_congenital_anomalies to history_ccs47_other_and_unspecified_benign_neoplasm) |
  "any ICD-9 diagnosis of this CCS group time-stamped before the prediction point" (He 2019); flags kept when set in >= 408
  stays | yes. The stay's final billing codes are not in it: elective hip / knee replacement -> osteoarthritis 27% / 42%;
  CCS 157 in 9.1% of AKI stays; P1 (later point) only +0.3 pp. Same-episode, admission-day diagnoses do appear (acute DRG
  stays 44-76% matching) | 0/1 category, right (CLEAN-14); kept by counts over all rows, label-free (CLEAN-8) | fine; fix
  the "earlier records" wording (item 6) | LEAK-10 checked, CLEAN-14, CLEAN-8
  Columns that stand out in the block, all fine on timing: history_ccs157_acute_and_unspecified_renal_failure (earlier
  AKI, a legitimate risk factor, 9.1% vs 5.3%); history_ccs131_respiratory_failure (7.1% of stays, AKI 13.3%);
  history_ccs238 and history_ccs237 (complications of care or devices, earlier episodes). ICD-10 codes (from October 2015)
  are not mapped, so the history of the last 15 months of stays may be thinner (a drift the forced-IID split hides; for
  the split auditor).

======================================================================================================================
MEASUREMENTS (my scripts; untuned LightGBM, 400 trees, 5-fold stratified, seed 0; mean over folds)
======================================================================================================================
all 302 features                                         0.7234 (fold SE 0.005)
without comorbidity_renal_failure                        0.7210 (paired -0.0024, SE 0.0002, 5/5 folds)
without the 6 acquirable comorbidities                   0.7179
without the 20 O.R.-procedure DRG groups                 0.7130
without all 25 procedure DRG groups                      0.7083
without the 20 O.R. groups and the 6 acquirable COM      0.7062
without the whole DRG block                              0.6952
without DRG and the 7 acquirable COM (remedy c')         0.6882
without DRG and COM (builder's option b)                 0.6809
Shares: O.R.-procedure groups 19.7% of rows, 22.6% of AKI stays; acquirable comorbidities (any of 6) 34.2% of rows,
45.8% of AKI stays.

Sources: He et al. 2019, https://pmc.ncbi.nlm.nih.gov/articles/PMC6447093/ ; Cheng et al. 2017,
https://pmc.ncbi.nlm.nih.gov/articles/PMC5977670/ ; APR-DRG 710 title (third party, weak):
https://payerprice.com/rates/710-APR-DRG-fee-schedule
```

</details>

<details><summary>Split audit</summary>

```text
SPLIT AUDITOR REPORT: kumc_inpatient_aki_prediction (2026-11-08)
Definition: datasets/_dev/tabarena-v0pt2/kumc_inpatient_aki_prediction/dataset.py
Shipped split: IID, tag ForcedIIDFromTemporal, 3 repeats x 3 folds, stratified on the label (51,304-51,305 train / 25,652-25,653 test).
Scripts and outputs: work_split_auditor/ (order.py, partners.py, control.py, purge.py, purge_models.py, purge_results.csv, purge_models.csv; cache.pkl and edges.pkl are scratch).

VERDICT: right with notes. Forced IID is the mildest option the file allows. No column orders the stays in time, so no temporal
split can be built; no patient key exists, and a grouped split on a similarity cluster is not allowed. Repeat patients are
common (an estimated 45-60% of stays, from the paper's counts) but detectable ones inflate an untuned LightGBM by only about
0.0015 ROC AUC overall (0.019 on the 13% of test stays that have a likely same-patient stay in train), a deep random
forest by 0.008, and the model ranking does not change. The notes should carry
these numbers and the corrected repeat-patient picture; the split itself stays.

1. REGIME THE USE CASE IMPLIES (SPLIT-1, SPLIT-3, SPLIT-13, USE-10)
- Use case: the admitting team scores every adult admission on the day of admission. That is a stream of admissions over
  2007-11 to 2016-12; the hospital trains on earlier admissions and scores new ones. Returning patients are part of the
  stream (known entities, SPLIT-13): their earlier stays are legitimately in train. So the right regime is temporal, not
  grouped by patient. A grouped-by-patient split would test a cold start the use case does not ask for.
- Declared: IID, forced from temporal (SPLIT-8). Matches: the temporal regime cannot be built (section 2), and the closest
  regime that keeps the rows is IID. ForcedGrouped is not an option (no entity key, and the periods are not stacked).

2. CAN ANY COLUMN ORDER THE STAYS IN TIME? No.
- Columns: 22 measured (age band, race, sex, banded vitals, 14 labs), 61 base APR-DRG flags, 27 UHC comorbidity flags,
  192 history CCS flags. No date, year, encounter number or version field. Deposit README: "Date of data collection:
  2007/11 to 2016/12", nothing per row.
- ICD-9 to ICD-10 (October 2015): the history block is "ICD9 codes mapped to CCS major diagnoses" (paper, Table 1).
  All 192 kept history columns are ICD-9 CCS categories; an ICD-10-era code was either mapped back to them or dropped,
  and neither leaves a column that marks an ICD-10-era stay (at most a thinner recent history, which a row cannot tell
  from a patient new to the hospital). The dictionary's 315 APR-DRG names carry one possible version pair ("DORSAL/LUMBAR FUSION PROC" next
  to "DOR/ LUMB FUS EXC CRV BCK"), but only the second survived the scrub (DRG134); every stay has 0 or 1 DRG flag
  (46,780 with one, 30,177 with none, the rare DRGs removed), so no grouper version can be read off a row.
- Raw row order: the file lists the 7,259 AKI stays first (builder). Within each label block I tested the order:
  * per-decile means of history count, comorbidity count, DRG presence, labs measured, BMI unknown and age are flat
    (no-AKI block: history count 7.04-7.38, labs measured 8.25-8.38, no trend);
  * largest |Spearman(position, column)| over 294 columns: 0.033 in the AKI block (chance SD 0.012, so about 2.8 SD, the
    expected maximum of 294 null draws), 0.015 in the no-AKI block (chance SD 0.004);
  * LightGBM predicting the first vs second half of each block from all features, 5-fold: ROC AUC 0.516 (AKI block,
    null SE about 0.007) and 0.503 (no-AKI block, null SE about 0.002).
  The order inside the blocks is random or unrelated to the features; it cannot stand for admission time.
- A proxy split (e.g. by the number of history flags, which grows with years in the EMR) would test a shift of patient
  mix, not of time; not recommended (SPLIT-8: say what a dated window would change and recover it if a later release
  has it).
- What the missing time costs, unmeasurable here: drift over nine years (the ICD-10 switch changes the history and the
  APR-DRG grouper; practice changes such as AKI alerts and creatinine monitoring change the label rate). A random split
  trains on 2016 to score 2008. The notes already say a hospital would train on earlier years; they could add that the
  score is likely optimistic against a dated split by an unknown amount.

3. REPEAT PATIENTS: HOW COMMON (SPLIT-29, SPLIT-30, SPLIT-13)
- The paper (Methods, Study population, via Europe PMC PMC6447093): "A retrospective cohort was built including 96 590
  adult inpatients" and "The total number of encounters was 179 370, considering there may be multiple admissions
  (encounters) of a patient"; the kept cohort is 76,957 encounters. So 1.86 encounters per patient before the
  exclusions, and 42.9% of encounters kept.
- Simulation (encounters per patient 1 + Poisson or negative binomial with mean 0.86, each kept with p = 0.429,
  independent or patient-correlated): 44-61% of the kept stays belong to a patient with another kept stay. This
  corrects the reading that repeat stays are rare (the 2.6% near copies of the hidden-group probe are near copies over
  all 302 columns at similarity 0.85, a much narrower relation than "same patient").
- A likely-same-patient relation in the data: same sex and race, age band within 1, at least 4 history flags, Jaccard
  >= 0.8 on the 192 history + 27 comorbidity flags. 12,737 rows (16.6%) have such a partner (median 1 partner, i.e.
  pairs). Control: the same relation across sexes (cannot be one patient) hits 3.7e-6 of candidate pairs against
  8.4e-5 within a sex, 23 times fewer, and 0.8% against 29.0% of sampled rows with a hit. So about 96% of these pairs are
  beyond chance, most likely one patient's repeat stays; the relation is a lower bound on repeat patients, since the
  history grows between stays and sparse profiles are excluded.
- Label concordance in those pairs: P(partner AKI | AKI) 0.235 against P(partner AKI | no AKI) 0.084 (base 0.094);
  the partner's label as a score on partnered rows: ROC AUC 0.587.

4. HOW MUCH REPEAT PATIENTS INFLATE THE SCORE (measured)
Test: on the shipped splits (repeat 0 and 1, six folds), untuned LightGBM (300 trees, lr 0.05, 31 leaves). For each
fold, remove from train every row that is a likely-same-patient partner of a test row (about 4,180 rows, 8% of train);
control: remove the same number of random training rows with at least 4 history flags. Same test rows throughout.
                               full train   purge partners   random control   purge - control
  all test rows                0.7169       0.7131           0.7146           -0.0015 (SD 0.0024, 4/6 folds < 0)
  test rows with a partner     0.7043       0.6816           0.7005           -0.0189 (SD 0.0080, 6/6 folds < 0)
  (test rows with a partner in train: 12.95%, AKI rate 9.1%)
- Reading: a stay whose likely twin is in train gains about 0.019 ROC AUC from it; over all test rows the detectable
  part is 0.0015. Undetected repeat pairs (history changed more between stays) resemble each other less and should gain
  less per row; scaling the measured effect to 45-60% repeat stays gives an upper bound of roughly 0.005-0.007 overall.
  Against the model spread of the task probes (0.031 across families) this is small, and it is consistent with the
  hidden-group probe (near-copy grouped gap +0.0008) and leak probe 23 (shared-unit lookup +0 on 9 splits).
- Under the temporal regime the use case implies, half of these pairs would be legitimate anyway (the earlier stay in
  train, SPLIT-13). The IID-specific part is the other half: a later stay of the patient in train when an earlier one is
  tested. So the inflation against the ideal split from repeat patients is about half the figures above.
Other model families (repeat 0, three folds, same purge and control; purge_models.csv):
                     full     purge    control   purge - control (all)   purge - control (partnered rows)
  LightGBM (above)   0.7178   0.7128   0.7153    -0.0025 (repeat 0)       -0.020
  logistic (1-hot)   0.7103   0.7088   0.7092    -0.0003 (-0.0005..-0.0002) -0.009
  random forest deep 0.6866   0.6800   0.6877    -0.0077 (-0.0092..-0.0058) -0.030
  kNN 50, Jaccard    0.6447   0.6412   0.6443    -0.0031 (-0.0046..-0.0022) -0.018
- Repeat patients favour the models that memorise rows: a deep random forest gains 0.008 overall from the detectable
  pairs, logistic regression 0.0003. The ranking does not change (LightGBM > logistic > forest > kNN with and without
  the purge), but the LightGBM-logistic gap narrows from 0.0075 to 0.0040. Scaled to all repeat stays (3-4 times the
  detectable ones, an upper bound since undetected pairs are less alike), a memorising model could gain up to about
  0.02-0.03; half of that is legitimate under the temporal regime the use case implies.

5. ALTERNATIVES CONSIDERED
- Temporal (SPLIT-14): impossible, no time column and no time order (section 2).
- Grouped by patient (ForcedGroupedFromTemporal): no patient key; the likely-same-patient relation is a similarity
  cluster and must not be a group id (split-auditor brief; SPLIT-30 also needs the context to call a column an id).
- Filter: drop one side of each likely-same-patient pair (or the 16.6% partnered rows). Costs rows and changes the
  population (partnered rows are the sicker, richly coded ones) for a gain of about 0.0015 AUC; not proportionate.
- One stay per patient (USE-11): the use case is every admission, not the first; and no key.
- Keep forced IID: the mildest option.

FINDINGS, ranked by principles.md (P4 honest evaluation for all)
F1 (P4, SPLIT-8 / SPLIT-7, Should; note only). The temporal regime cannot be recovered: no date, no year, no encounter
   order and no column that marks the ICD-10 era (CCS categories are code-set neutral, every stay has at most one APR-DRG
   flag, the raw order within label blocks is unrelated to the features, AUC 0.503/0.516). Forced IID is right. The
   unmeasurable cost is nine years of drift across the ICD-9/ICD-10 switch. Remedy: none to the split; the notes could
   add that the score is likely optimistic against a dated split and that a release with admission years (perhaps the
   full set behind the authors' data use agreement; not checked) should be split by time.
F2 (P4, SPLIT-29 / SPLIT-30 / SPLIT-13, Should; correct the notes). Repeat patients are not rare: the paper's counts
   (179,370 encounters of 96,590 patients) imply 44-61% of the kept stays share a patient with another kept stay, and
   16.6% of the rows have a likely-same-patient partner found in the data (23 times the cross-sex control rate). The
   inflation is measured small: LightGBM -0.0015 ROC AUC overall when partners are purged from train (-0.019 on the
   partnered 13% of test stays); a deep random forest -0.0077, logistic -0.0003; model ranking unchanged; half of it
   would be legitimate under the temporal regime. The
   curation notes say "SPLIT-29 cannot be checked" and "21 rows ... may be one patient's repeat stays"; they should say
   instead that repeat stays are common and give the measured effect. Remedy: a note, no re-split; the split comment /
   task_summary.split sentence "one patient's repeat stays can fall on both sides" is correct and can stay.
F3 (P4, minor). splits_comment is "Default splits."; the reason for the forced regime lives only in curation_comments
   and task_summary.split. Remedy: optional, a one-line splits_comment naming SPLIT-8 and the missing dates and key.

No finding on: label delay or a gap (no time axis), training rows with late labels (whole stays, label complete at
discharge before release), stratification (stratified on the label; smallest positive count per test fold 2,419).
```

</details>

<details><summary>Domain practitioner</summary>

```text
DOMAIN PRACTITIONER REPORT: kumc_inpatient_aki_prediction (2026-11-08)
Actor played: the clinical decision-support team of an academic hospital (nephrology / AKI stewardship with pharmacy),
which on the day of admission flags adults at risk of hospital-acquired AKI, to order daily creatinine and have a
pharmacist review nephrotoxic drugs (NSAIDs, vancomycin + piperacillin-tazobactam, aminoglycosides, ACEi/ARB,
diuretics, contrast).
Definition read: df-large/datasets/_dev/tabarena-v0pt2/kumc_inpatient_aki_prediction/{dataset.py,README.md}; record,
builder_report.md, claims list, probes/block_ablation_lgbm_cv5.json. My scratch: the run folder
(q1.py: DRG coverage and the renal-failure flag; q2.py/q2.json: two ablations, same untuned LightGBM and 5-fold seed
as the builder).

VERDICT
Fit: APPROXIMATE (agree with the declared fit; USE-8). One sentence: the source built exactly my admission-day
decision on real stays of one hospital, but the public file lacks two inputs I always have at admission (the admission
creatinine value and the medication list), carries diagnosis and comorbidity flags I would only have in that coded
form after discharge, and the cohort is cut on facts I do not know at admission (a stay of 2+ days, 2+ creatinine
values).
Metric: YES, roc_auc scores my decision as well as any single number can (MET-1, MET-8, MET-9); details in Q5.
Recommendation: ship. The use case is real and named by the source (USE-1, USE-2 pass); the gaps are ones a practitioner
recognizes and the fit_reason names. One finding to add to the curator's issue 1 (the renal-failure comorbidity, below).

Q1. INPUTS AT THE MOMENT OF THE PREDICTION (USE-3, USE-6)
Have, as shipped:
- Age, sex, race; admission vitals; the admission-day labs (BUN, glucose, WBC, platelets, calcium in 93-94% of stays;
  liver panel in 77%; troponin, CK, lipase, ammonia when ordered). Yes: these are in the first ED/ward panels. I would
  have the values, not normal/abnormal bands; the banding is the source's and costs resolution, not validity.
- Earlier diagnoses (history_ccs*): yes, from earlier encounters; checked by the builder (CCS 157 9.1% vs 5.3%, so not
  the stay's own codes).
Would NOT have in this form:
- admission_drg_* (61 base APR-DRGs): the APR-DRG is set by the grouper after discharge from the principal diagnosis
  ("after study") and the procedures done. What I have at admission is the admitting diagnosis / chief complaint and,
  for an elective admission, the scheduled operation. For the 23 procedure DRGs (22% of stays, 24% of AKI cases:
  CABG 27% AKI, valve 22%, bowel 15%), the elective ones are known to me from the OR schedule; an emergency operation
  decided on day 2 is not. Each stay has at most one flag set and 39% of stays have none (their DRG was rare and
  scrubbed), so the block reads as "one of 61 frequent admission reasons, or other".
  Measured (q2.json): dropping the 23 procedure DRGs costs 0.726 -> 0.713 ROC AUC.
- comorbidity_* (27 flags): these are the AHRQ Elixhauser set (the names match: renal failure, coagulopathy, fluid and
  electrolyte disorders, weight loss, ...), computed from the stay's discharge abstract. In the ICD-9 era (this cohort
  is 2007-2016, ICD-9 until Oct 2015) the Elixhauser software did not use present-on-admission flags, and Glance et
  al. 2006 found that 43% of the coagulopathies and 25% of the fluid and electrolyte disorders it labels as
  comorbidities were in fact complications of the stay. Whether UHC applied POA is not documented (I found no source).
  NEW FINDING (q1.py, raw P2 file): comorbidity "Renal failure" is set in 1,780 stays although the cohort excludes
  eGFR < 60 in the first 24 h. Among the 752 of them with no earlier renal diagnosis (no history CCS 157 or 158), the
  AKI rate is 29.8%, higher than the 17.4% of the 1,028 with an earlier renal diagnosis and 3.4x the 8.7% of stays with
  neither. A chronic condition should co-occur with its history, not run higher without it; the pattern fits ICD-9 586
  "renal failure, unspecified" (an Elixhauser renal-failure code) coded for the stay's own AKI. It is a small label
  echo (about 1% of stays), not a large one. Dropping renal failure, coagulopathy and fluid/electrolyte disorders
  together costs 0.726 -> 0.722 (q2.json); dropping those three and the procedure DRGs, 0.709.
Missing, that I would always have:
- The admission serum creatinine (and eGFR). It is drawn with the same panel as the BUN that is shipped (BUN missing
  in only 6.6%), and it is the baseline of the label itself; a patient at 1.2 mg/dL and one at 0.6 are different risks
  for a 0.3 mg/dL rise. The source left SCr and eGFR out on purpose ("SCr and eGFR were not included as predictive
  variables"); in practice every AKI model I would buy uses them.
- Medications: home medications and the admission orders (nephrotoxins, ACEi/ARB, diuretics, planned contrast). The
  source had them (RxNorm ingredients, 7 days before the prediction point); the public scrub removed them. For my
  decision this is the largest gap: avoiding nephrotoxins is the action, and the drugs already ordered are the
  strongest modifiable risk factor (NICE NG148 lists them among the risk factors to assess on admission).
- Admission type (elective / emergency / transfer), admitting service, ICU admission; sepsis or hypovolaemia flags
  (NICE NG148: emergency surgery with sepsis or hypovolaemia). Partly proxied by the DRG.

Q2. THE TARGET (USE-5)
- AKI by the KDIGO creatinine criteria (any stage) on any day up to discharge. This is the field's standard definition
  and what a stewardship programme counts as its outcome, so it is the thing I act on, not a proxy. Two caveats an
  expert names:
  (a) Whole-stay horizon: a 20-day stay has more days at risk and more creatinine draws than a 3-day stay, so the label
      mixes daily risk with length of stay. For flagging at admission this is acceptable (the flag lasts the stay), but
      most deployed tools predict a fixed horizon (24-48 h) and update daily. The source itself says its admission
      model with a 1-day window (Perspective #3, AUC 0.764) "best reflects real clinical usage", and calls Perspective
      #2 possibly "not granular enough". This is a choice between two real horizons, not a defect; P2 has 7,259
      positives against 1,611 for P3, which is the better benchmark.
  (b) Detection depends on monitoring: the label needs repeat creatinine, so a patient never re-tested cannot be
      positive. The cohort keeps only stays with 2+ creatinine values, which removes the unmonitored (mostly low-risk)
      patients but also the undetected AKI.
  Stage 2-3 (more severe, more actionable) would be a stricter target; any stage is defensible for a prevention flag.
- Form: I want a probability (a risk score shown with the patient, a list ranked for the pharmacist), not a class.

Q3. ROW, COHORT AND TEST DATA (USE-10, USE-11; SPLIT-8)
- One row = one admission = one decision (flag or not at admission). Matches.
- Cohort vs my patients: "no eGFR < 60 or creatinine > 1.3 in the first 24 h" is close to a rule I would apply at
  admission myself (hospital-acquired AKI is defined among those with normal function on arrival), though I apply it
  to the admission draw, not to 24 h of values. "Stay of 2+ days" and "2+ creatinine values" I do not know at
  admission: in deployment I would score all admissions, including the short stays (lower risk, lower prevalence).
  The model would be ranked on a population that excludes them, so its ranking of the easy short stays is untested.
  This is a selection the deployment setting does not share, so it is a known gap (USE-8, selection paragraph).
- Excluding CKD (eGFR < 60) removes the group a nephrology team watches most closely; the task is "risk among those
  with normal kidney function at admission", a real and common sub-question, but narrower than my whole remit.
- Test data: random stays from the same hospital and years. What I would face is next year's admissions; the file
  spans the ICD-9 to ICD-10 switch (Oct 2015) and nine years of practice change, has no dates and no patient key
  (ForcedIIDFromTemporal is the right marker, SPLIT-8). Returning patients are the norm in a hospital (an entity seen
  before, USE-10 weighed factor), and their earlier diagnoses are legitimate history features; repeat stays across
  folds cannot be grouped, and the builder's probes show no gain from it.

Q4. WOULD I USE THIS MODEL?
- Not as shipped, for deployment: about 0.72-0.73 ROC AUC, and 0.683 without the two discharge-coded blocks, i.e. on
  the inputs I surely have at admission. Without the admission creatinine and the medication list I would expect a
  model on my own EHR feed to do better, and I would not trust a flag whose strongest inputs I cannot reproduce at the
  bedside.
- What would make me trust it: a temporal validation (train on earlier years, test on later); calibration of the risk
  (the share flagged at 20% should develop AKI about 20% of the time); the inputs restricted to what the admission
  order set holds (POA-filtered comorbidities, admitting diagnosis instead of APR-DRG); and performance in subgroups
  (surgical vs medical, elective vs emergency).
- As a benchmark task: yes. The decision is real, named by the source, the population is a genuine general inpatient
  cohort, and the gaps are the known ones of EHR prediction work. It ranks methods on a realistic sparse,
  mostly-binary EHR table.

Q5. DOES roc_auc SCORE MY DECISION? YES (MET-1, MET-6 to MET-9)
- Unit: per stay, the unit I act on. Matches (MET-1, MET-2).
- My decision is to act on the top of a ranked list at a capacity I set locally (how many pharmacist reviews a day)
  or at a risk threshold that each hospital picks. The source fixes neither a k nor a threshold nor costs (its
  F-measure-optimal threshold is chosen per model, i.e. a habit, not a decision), so a threshold metric or
  precision_at_k would invent a decision (MET-6, MET-7: never invent a cost or a threshold).
- ROC AUC holds over every threshold and prior (MET-8, Provost et al. 1998), and 9.4% positives is no reason for AUPRC
  (MET-9: AUPRC would move with the prevalence and weight only the top; no source chose it).
- What I would add in my own model selection, not as the declared metric: calibration (Brier score or log loss), since
  the risk is shown to clinicians as a number, and net benefit over the 5-20% threshold range (decision curve). If
  the collection wants a proper rule for diversity (MET-10), log_loss would also be defensible; roc_auc is the closer
  match to "rank admissions for follow-up".

GAPS, RANKED BY HOW MUCH THEY CHANGE THE TASK
1. Medications scrubbed (and no admission creatinine): the action is about nephrotoxins and the input that says who
   is on them is missing; the strongest routine predictor (the admission creatinine) is excluded by the source's
   design. Changes what the model can learn, not what it predicts. Not fixable from the public file (needs the
   source's data use agreement).
2. DRG and comorbidity flags from the discharge abstract (LEAK-10, kept on purpose): the information is mostly
   available at admission in another form, but some of it (emergency procedures, coded complications, the renal-failure
   flag above) is not. Worth 0.726 vs 0.683 ROC AUC as a whole; the most suspect parts (3 comorbidities and 23
   procedure DRGs) worth 0.017.
3. Cohort cut on 2+ day stays and 2+ creatinine values (selection not shared by deployment; USE-8).
4. Whole-stay horizon instead of a fixed 24-48 h horizon (the source's own preferred clinical scenario is the 1-day
   window); a defensible alternative, not a defect.
5. Random split for a temporal deployment, across the ICD-9/ICD-10 switch (SPLIT-8, forced; named).
6. Labs and vitals banded to normal/abnormal and coded bands (resolution loss; the source's choice; vital-band code
   order undocumented).

WHAT AN EXPERT WOULD CHANGE (in what the curator can change)
- Issue 1 (LEAK-10): my view as the actor is that the timing is NOT settled by the source: "presumed to be available at
  admission" is an assumption, and the coding practice of the period (Elixhauser without POA) contradicts it for a
  known subset. I would not drop both blocks (option b, 0.683): most of the admission reason and the chronic
  comorbidities are things I do know at admission. I would choose option (c) with an evidence-based, not
  judgment-based, list: drop comorbidity_renal_failure (the flag that fits the stay's own AKI coding, numbers above),
  and comorbidity_coagulopthy and comorbidity_fluid_and_electr_disorders (the two Elixhauser measures with published
  complication shares of 43% and 25%, Glance et al. 2006; HCUP later discontinued the fluid and electrolyte measure in
  its ICD-10 refined version, which uses POA). Cost 0.004 ROC AUC. Keep the DRGs with the note (elective procedures
  are known at admission). If the curator prefers option (a), the notes should at least name the renal-failure finding
  as the sharpest part of the kept leak.
- Write the horizon into task_summary.predicted more plainly ("on any day of the stay, however long") and name
  Perspective #3 (1-day window, the source's own clinical scenario) in the notes as the rejected alternative and why
  (7,259 vs 1,611 positives; whole-stay flag is the admission decision) - already partly in the curation notes.
- fit_reason: add "no admission creatinine" next to "no medications" (the source's exclusion of SCr/eGFR as features is
  a gap to a practitioner, not only the scrub). The 2+ creatinine values requirement belongs with the 2+ days in the
  selection sentence.
- No change to the metric.

SOURCES
- He J, Hu Y, Zhang X, Wu L, Waitman LR, Liu M. Multi-perspective predictive modeling for acute kidney injury in
  general hospital populations using electronic medical records. JAMIA Open 2019;2(1):115-122,
  https://pmc.ncbi.nlm.nih.gov/articles/PMC6447093/ (Methods: data collection, UHC/APR-DRG, "presumed to be available
  at admission"; Table 2/3 AUCs; Discussion: the 1-day admission window "best reflects real clinical usage").
- Dryad deposit doi:10.5061/dryad.qc90qb4, README.txt and AKI_dataset_attributes_map.xlsx (local copy in
  local-data-warehouse/kumc_inpatient_aki_prediction/).
- Glance LG, Dick AW, Osler TM, Mukamel DB. Does date stamping ICD-9-CM codes increase the value of clinical
  information in administrative data? Health Serv Res 2006, https://pmc.ncbi.nlm.nih.gov/articles/PMC1681527
  (43% of coagulopathies, 25% of fluid and electrolyte disorders labelled pre-existing were complications).
- HCUP Elixhauser Comorbidity Software Refined for ICD-10-CM, user guide v2021.1,
  https://hcup-us.ahrq.gov/toolssoftware/comorbidityicd10/Com-ICD10CM-User-Guide-v2021-1.pdf and
  https://www.hcup-us.ahrq.gov/toolssoftware/comorbidityicd10/comorbidity_icd10.jsp (POA used in the ICD-10 version;
  fluid and electrolyte measure discontinued).
- NICE NG148, Acute kidney injury: prevention, detection and management, recommendations 1.1 (risk factors to assess
  in adults in hospital: CKD eGFR < 60, heart failure, liver disease, history of AKI, nephrotoxic drugs, emergency
  surgery with sepsis or hypovolaemia), https://www.nice.org.uk/guidance/ng148/chapter/recommendations (read from
  search excerpts).
- Nephrotoxin-triggered creatinine monitoring practice (Seattle Children's EHR system, J Hosp Med 2019),
  https://cdn.mdedge.com/files/s3fs-public/issues/articles/jhm014080462.pdf (search excerpt; context for the action).
- My computations: the run folder (DRG coverage, procedure DRG share, renal-failure flag by
  history), q2.py and q2.json (ablations).
Rules cited: USE-1, USE-2, USE-3, USE-5, USE-6, USE-8, USE-10, USE-11; MET-1, MET-2, MET-6, MET-7, MET-8, MET-9, MET-10;
LEAK-10; SPLIT-8; EV-2.
```

</details>

<details><summary>Blind review</summary>

```text
BLIND REVIEW: kumc_inpatient_aki_prediction (target aki_during_stay, binary, 76,957 x 303, random 3x3-fold CV)

VERDICT: Include with changes. The data is real and the AKI-risk task is a genuine one with moderate signal at a usable
size. Before it goes in, the column types and the timing of the features need documenting or fixing, and the
feature-timing caveat (DRG and comorbidity codes) has to be stated, because it cannot be ruled out.

WHAT THE TASK IS
He, Hu, Zhang, Wu, Waitman, Liu, "Multi-perspective predictive modeling for acute kidney injury in general hospital
populations using electronic medical records", JAMIA Open 2019 (doi 10.1093/jamiaopen/ooy043). The data is on Dryad as
AKI_Prediction_Scrubbed_EMR (doi 10.5061/dryad.qc90qb4). The cohort is adult inpatients at the University of Kansas
hospital, 2007-11 to 2016-12, with length of stay of at least 2 days. Encounters were excluded if they had fewer than 2
SCr values, or eGFR<60 or SCr>1.3 within 24h of admission. The outcome is KDIGO SCr-defined hospital-acquired AKI. The
counts match the paper exactly: 7,259 AKI and 69,698 non-AKI (9.4%), the same as in the data. The target matches the
paper's "Perspective 2": predict at admission whether AKI happens at any time during the stay. The user would be a
hospital early-warning or nephrology-stewardship team. The decision is which newly admitted patients to flag for SCr
monitoring and for avoiding nephrotoxins. That is a real use. The paper reports a cross-validated AUC of 0.734 for P2.

WHAT I MEASURED (Python, LightGBM, 3-fold stratified CV)
- Target: 7,259 Yes / 69,698 No. Prior log-loss is 0.312.
- LightGBM with all features: AUC 0.723, AP 0.252, log-loss 0.282. L2 logistic regression on one-hot features:
  AUC 0.711, AP 0.221. This reproduces the paper's level, and there is no sign of a leak that makes the task trivial.
  The best single feature has a univariate AUC of only 0.543 (bmi_band).
- AUC for each feature group alone: demographics 0.55, vitals 0.58, labs 0.61, DRG 0.63, comorbidity 0.63,
  history 0.62. The drop when each group is removed is largest for DRG (0.723 -> 0.694).
- Columns: 3 demographic, 5 banded vitals, 14 labs coded normal/abnormal/NaN, 61 admission_drg_* flags,
  27 Elixhauser-style comorbidity_* flags, 192 history_ccs* flags. Every binary flag has at least 398 positives, so
  rare columns were filtered. No medication features: the paper had 1,271 RxNorm medication variables, and they are
  absent here.
- Plausibility checks pass. Prostate codes are almost all sex_code 2 (4 exceptions out of 959). Pregnancy and uterine
  codes appear only for sex_code 1. Pregnancy occurs only in age bands 1-3. Higher AKI rates sit with CABG (27%), valve
  surgery (22%), heart failure (22%), BMT (24%) and sepsis (15%). Lower rates sit with alcohol (2%), IBD (3%) and
  arrhythmia (3%). This is clinically sensible and real-looking, not generated.

CONCERNS, MOST TO LEAST SERIOUS

1. Feature timing is not fully known, and some features are billing codes that are only finished after discharge.
   Evidence:
   - The paper says only that "Comorbidities, admission diagnosis, and demographics were presumed to be available at
     admission". It also says "For laboratory tests and vitals, only the last recorded value before a prediction point
     was used".
   - The paper defines 4 prediction points. P1 is 1 day before AKI onset; for non-AKI encounters its reference date is
     "the last normal SCr". P1 and P2 use the same 76,957 encounters, so the counts cannot tell which feature window
     this release uses.
   - I could not open the Dryad README: the API download returned "Unauthorized". The README is the document that
     would say which perspective the scrubbed file is.
   - If labs and vitals are taken "before onset" rather than "at admission", the feature window differs by class. That
     is a known leak in AKI models, though it is mild here: a missing lab means a lower AKI rate (6.7% vs 10.2% for
     albumin, ALT, AST and bilirubin).
   - The admission_drg_* columns are named after MS-DRG groups such as "coronary_bypass_w_card_cath",
     "cardiac_valve_proc_w_0_cath", "septicemia", "post_op_trauma_infect_proc" and "oth_comp_of_treatment". DRGs are
     normally assigned from discharge coding and reflect procedures done and complications that occurred. They are the
     most useful group, and removing them costs 0.03 AUC.
   - Elixhauser comorbidity flags are usually built from the same encounter's discharge codes too.
     comorbidity_fluid_and_electr_disorders has an AKI rate of 12.4% vs 9.4% overall.
   - Mitigation: overall signal is modest (AUC 0.72). history_ccs157 (acute renal failure) flags only 663 of the 7,259
     AKI encounters, so the history block does not appear to contain the current encounter's AKI code. Any leak is
     soft, not a shortcut.
   Change: state the feature-time assumption in the task description, and confirm it from the Dryad README. Consider
   dropping admission_drg_* and comorbidity_* in a strict "known at admission" variant, or at least flag them as
   possibly post-discharge.

2. There is no patient ID, and the split is random by encounter.
   Evidence: there are 76,957 encounters, and the paper's own patient counts are inconsistent (it gives 96,590
   inpatients for the base pool). Repeat admissions of the same person are almost certain. As a proxy I matched rows
   on exact demographics + history + comorbidity profile, with at least 3 history codes. That gives 1,968 rows in
   multi-row groups. Within those groups label agreement is 0.909 against 0.829 by chance. Grouped CV on the proxy
   changes AUC only from 0.723 to 0.721, so the measured effect is small. The proxy is weak, though, and true repeat
   patients cannot be identified.
   Change: none is possible without IDs. Note it as a known limitation. If the README or source provides patient IDs,
   use a grouped split.

3. Column types and band semantics.
   Evidence:
   - race_code (values 1-4, counts 58,585/10,401/654/7,317) is a nominal code but is stored as int64.
   - The vital bands are float with no documented meaning, and their AKI rates are not monotone. temperature_band
     level 5 holds 13,437 rows (17%) and level 4 holds 9 rows, which looks like a nominal code (perhaps "unknown"/other)
     rather than an ordinal band. pulse_band level 5 has 7,619 rows and level 4 has 421, with AKI rates 12.3% and 19%.
   - The lab columns are categorical normal/abnormal with NaN for "not measured". The paper treated "unknown" as its
     own informative category; NaN works for trees, but this should be documented as informative missingness.
   Change: declare race_code categorical. Check the band coding in the README and declare temperature_band and
   pulse_band (probably all the vitals) categorical if they are nominal.

4. A label/semantics oddity in the diabetes flags.
   Evidence: comorbidity_diabetes_w_ccs and comorbidity_diabetes_w_o_ccs are almost mutually exclusive (118 overlap),
   with prevalence 18.3% and 17.7%. "w_ccs" alone has a LOWER AKI rate (7.0%) than "w_o_ccs" (12.5%) and than the
   baseline (9.4%). It also aligns poorly with history_ccs50 ("DM with complications"): only 947 of 14,107 rows
   overlap. Either the names are swapped or "ccs" means something other than chronic complications.
   Change: check against the source codebook and rename or document. This does not affect benchmark validity.

5. The features are heavily coarsened and almost all binary.
   Evidence: 283 of 302 features are 0/1 flags. Labs are reduced to normal/abnormal, vitals and BMI to 4-5 bands, and
   age to 6 bands. The source file is named "Scrubbed", so this is de-identification by design. The gap between models
   is narrow (LR 0.711 vs GBM 0.723 AUC), so the task will separate methods only weakly, and mostly on calibration and
   rare-flag handling.
   Change: none needed. Note that it is a sparse-binary, low-signal clinical task. That is still useful diversity.

6. Exact duplicates (minor).
   Evidence: 149 rows fall into 72 groups of identical feature vectors, 70 of which are full-row duplicates, and 7 of
   those groups have conflicting labels. Most are rows with no history codes. This is not material at 77k rows.
   Change: leave them in, or drop exact full-row duplicates. It makes no material difference.

WHAT I COULD NOT CHECK
- The Dryad README and the raw zip: download needs authentication or a browser. I could not verify which prediction
  perspective (P1 admission vs P2 onset-minus-1-day) the released features use, what the band codes mean, or how
  "w_ccs" is defined.
- Whether rows are encounters of repeat patients: there is no identifier.
- Whether the admission_drg_* flags are the final billing DRG or a working DRG at admission.
- I verified the cohort and prevalence numbers against the paper. I did not see the paper's supplementary feature
  list.
```

</details>

<details><summary>Task gamer</summary>

```text
TASK GAMER REPORT - kumc_inpatient_aki_prediction (target aki_during_stay, ROC AUC, IID 3x3 stratified folds,
prediction point = day of hospital admission)

Verdict: I could not add a gain beyond seed noise with information outside the honest features (row order, copies,
test statistics, formats and split order give nothing). The flaw is in the features: the 61 admission_drg_* and 27
comorbidity_* columns come from the encounter's discharge coding (UHC/Vizient APR-DRG and comorbidities). An
admission-time model would not have them, and they lift every honest model by about 0.043 AUC (0.679 -> 0.722).

Scores (mean over the 9 shipped splits, score.py)
  untuned LightGBM (400 trees, lr 0.05), all features         0.7158  [0.7078, 0.7263]   work/baseline.py
  tuned LightGBM (800 trees, lr 0.02, 15 leaves, mcs 100)      0.7224  [0.7135, 0.7329]   work/tuned.py  (reference)
  noise: tuned + a random column (2 seeds)                     mean diff -0.0003 / -0.0006, per split -0.0022..+0.0009
         tuned with other LightGBM seeds (2 seeds)             mean diff +0.0007 / +0.0002, per split -0.0005..+0.0019
  paper (He et al. 2018, Perspective #2, with 1271 medication columns this kit lacks): 0.734

EXPLOITS RANKED BY GAIN

| # | Exploit | Script | Honest score | Exploited score | Gain (per split, range) | A deployed model has it? | Fix |
|---|---|---|---|---|---|---|---|
| 1 | Discharge-coded APR-DRG (61 cols) and UHC comorbidities (27 cols) used as admission features. Every model in the kit already gets this, so no participant gains on another, but the task's score is inflated. | work/ablate.py, work/comorb_timing.py, work/drg.py | 0.6794 (tuned, without drg+comorb) | 0.7224 (tuned, all features) | +0.043 (+0.040..+0.044) | Mostly no. The APR-DRG is assigned by coders after discharge and reflects procedures done during the stay. The comorbidities are coded from this encounter's diagnoses (see mechanism). | Drop admission_drg_* and comorbidity_*, or at least the comorbidities that are often hospital-acquired. Or restate the prediction point as "at discharge / retrospective". |
| - | Nothing else beats the tuned honest model beyond seed noise (see "attacks that found nothing"). | | | | | | |

Mechanism of #1.
 - The paper says comorbidities and admission DRG "were presumed to be available at admission". They come from the
   UHC/Vizient abstract, which is built from the final coded encounter.
 - Evidence from the kit: 11,553 encounters (15%) have no prior history code at all, yet they carry on average 1.98
   comorbidity flags (2.49 for patients with history). 12.8% of them carry fluid/electrolyte disorders, 9.7%
   deficiency anemia and 4.7% coagulopathy. With no earlier record, these codes can only come from the current stay.
 - Coders often assign fluid/electrolyte disorders, coagulopathy, weight loss and the anemias during the stay;
   hyperkalaemia and acidosis are common consequences of AKI. These columns carry AKI rates of 12-15% against a 9.4%
   base rate. Dropping just these 5 comorbidities costs 0.0033 AUC: 0.7191, with 8 of 9 splits lower by 0.0026-0.0050.
 - The APR-DRG is a single one-hot across 315 groups. The kit keeps 61 of them, and 30,177 rows have none set. Several
   groups encode what happened during the stay: surgical groups such as CABG (AKI 27%) and valve surgery (22%),
   "O.R. proc for other complications of treatment", "post-op infection with procedure", rehabilitation.
 - Group contributions: dropping DRG alone costs 0.027 (0.6952), comorbidities alone 0.016 (0.7084), both 0.043
   (0.6794).
 - What would decide it: whether the UHC comorbidity flags were restricted to present-on-admission diagnoses, and
   whether a working DRG exists at admission. Elective surgical admissions (CABG, joint replacement) do know their
   procedure at admission, so part of the DRG signal is legitimate. The 0.043 is therefore an upper bound on the
   leak.
 - Mildest fix: drop the comorbidity_* columns whose ICD groups are commonly hospital-acquired (fluid/electrolyte,
   coagulopathy, weight loss, deficiency/blood-loss anemia), and replace the APR-DRG one-hot with the admitting
   diagnosis or service if the source has it. Otherwise document that the task predicts "AKI during stay given
   discharge coding".

FLAWS THAT HURT AN HONEST MODEL
None found. The splits are stratified (test AKI rate 0.0943 in every fold) and each repeat covers every row exactly
once. Train/test are disjoint, and there are no rows that a deployed model would not train on. The exclusion of
eGFR<60 at admission is a cohort definition, not a training-set flaw.

ATTACKS THAT FOUND NOTHING (numbers vs the tuned 0.7224 unless stated)
 - Row order: AUC of row position vs label 0.4990. Block AKI-rate SD matches binomial at block sizes 10 to 5000.
   Next-row label agreement 0.8294 vs 0.8291 expected. The file is shuffled.
 - Split file order: test positions are listed sorted ascending. AUC of list position vs label is 0.4925-0.5043 on
   all 9 splits.
 - Exact copies across the split: 76,880 unique feature rows of 76,957, and only 0.11-0.13% of test rows have an
   exact train copy. Label agreement on those copies is 0.83-0.94, against a base agreement of 0.83.
 - Nearest-training-row labels (Hamming kNN; nn1 label, nn5/nn20 label mean, distance), on all features and on
   demographics+history as a patient proxy (40% of test rows have an exact history twin in train). Added to the
   tuned model on r0f0-f2: full -0.0003/-0.0004/-0.0014, history +0.0015/-0.0006/-0.0006. This is noise. The nn20
   label alone gives AUC 0.62, below the model. (work/knn.py, first 3 splits only for run time.)
 - Train+test frequency counts (all-feature, history and history+comorbidity pattern counts, row sums of
   history/comorbidity/lab-missing): 0.7231, mean +0.0007, per split -0.0026..+0.0023. Same as seed noise.
   (work/freq.py)
 - Train-vs-test classifier on r0f0: AUC 0.4996. The test sets do not differ from training. (work/adv.py)
 - Formats: every column is a small integer code, a 0/1 flag, a band code (float only because of NaN) or a
   two-level category (normal/abnormal). There are no decimals, ids, strings or sentinels to exploit.
   Missingness-only model (labs+vitals NaN flags): 0.568. This is lab-ordering signal that a deployed model has at
   admission (the paper treats "unknown" as information).
 - Transforms over all rows: none. Bands and flags are fixed clinical cut-offs, not z-scores or ranks.
 - Lookup/label proxy: no single column has a univariate AUC above 0.544. history_ccs157 (acute renal failure) is
   present in 9.1% of AKI encounters and 5.3% of non-AKI, so the history columns do not contain the current stay's
   AKI code. No APR-DRG "renal failure" group is kept, and rows with no kept DRG have an AKI rate of 0.093, the
   same as the base rate.
 - Data oddity, not an exploit: comorbidity_diabetes_w_ccs is the only comorbidity on 11,759 rows, and on those rows
   AKI is 5.1%, lower than without diabetes. It behaves like a "no other comorbidity" placeholder or a mislabelled
   column. Visible to every model.
 - Web: the Dryad record (doi:10.5061/dryad.qc90qb4) and the paper (PMC6447093). I found no forum, "leak" or
   "magic feature" threads for this dataset. The Dryad file download needs a token (API returned 401/403), so I did
   not compare the kit with the published file. Looking rows up there would not be a task flaw anyway.

WHAT I COULD NOT CHECK
 - The source zip and README: was the shipped snapshot really Perspective #2 (labs/vitals = last value up to
   admission)? If it was Perspective #1 (last value before AKI onset - 1 day), the labs/vitals would also be
   post-admission for AKI rows. Labs alone give 0.613, missingness alone 0.568.
 - Whether UHC comorbidities are present-on-admission restricted, and whether the APR-DRG is the final one.
 - Patient identity: rows are encounters (a patient can have several) split IID by encounter. There is no
   patient id, and the history-twin kNN found no exploitable re-identification.

Scripts and outputs: work/common.py, baseline.py, tuned.py, ablate.py(.txt), ablate2.py(.txt), drg.py(.txt),
comorb_timing.py(.txt), knn.py(.txt), freq.py(.txt), noise.py(.txt), splitcheck.py, adv.py(.txt), explore1.py(.txt).
Sources: https://doi.org/10.5061/dryad.qc90qb4 ; https://pmc.ncbi.nlm.nih.gov/articles/PMC6447093/ (saved as
work/pmc6447093.html/.txt).
```

</details>

<details><summary>Precedent check</summary>

```text
PRECEDENT CHECKER REPORT: kumc_inpatient_aki_prediction (2026-11-08)

Read: df-large dataset.py, README.md, record, builder_report.md, claims.md, register.json (5,160 decisions, 34 flags),
domain_practitioner.report.txt; knowledge files principles.md, leak_checks.md, evidence.md, splits.md,
cleaning_features.md, use_case.md, selection.md, metrics.md (all from df-large). Reproduced on the raw P2 file: DRG and
comorbidity flag counts and AKI rates, the age-code counts, and the panel's renal-failure finding.

SUMMARY

| # | Decision | Verdict |
|---|---|---|
| D1 | Admission DRGs and comorbidities from the discharge abstract kept with a note | departs, no fact that sets it apart; not reasonable under the ranking for two parts (renal-failure comorbidity, 23 procedure DRGs) |
| D2 | "Kept because the source's own document places them at admission (EV-2)" | the stated reason misreads EV-2: the conflict is with a measurement and the source's own dictionary, not a third-party page |
| D3 | Forced IID, no dates (SPLIT-8, ForcedIIDFromTemporal) | consistent; one missing sentence |
| D4 | No patient key, repeat stays may cross the split (SPLIT-29) | consistent |
| D5 | Lab codes decoded to normal/abnormal by inference | departs with a stated reason; reasonable (a Should, lossless); cite target-free evidence first |
| D6 | Vital bands, race, sex kept as codes; code 0 of labs and vitals to missing | consistent |
| D7 | age_band ordered by code, supported by the AKI rate | departs without an admissible reason (target information; the vitals of the same file go the other way) |
| D8 | 280 yes/no flags as 0/1 categories | consistent |
| D9 | Cohort filters known only after admission | consistent in substance (not USE-7's case); two bookkeeping gaps |
| D10 | Fallback roc_auc | consistent |
| -- | Register flags | none applies to this dataset (see end) |

======================================================================================================================
D1. Admission DRGs (61 flags) and comorbidities (27 flags) kept with a "Potential leak, kept on purpose" note
======================================================================================================================

Verdict: DEPARTS. No fact on record sets it apart from the precedents; for two parts it would be an exception to a Must
(LEAK-10), which the ranking does not allow (principles.md, "Exceptions and amendments": a Must has no exceptions,
anything else is an amendment).

Facts that matter for LEAK-10 (measured unless said):
- The source "presumed" the DRG and comorbidities "to be available at admission and not time dependent" (He et al.
  2019, Methods). That is an assumption, not a statement of when they were recorded.
- The source's own dictionary names in-stay operations among the 61 kept base APR-DRGs: coronary bypass with and
  without cath (600 and 592 stays, AKI 27.2% and 27.4%), cardiac valve procedure (631, 21.9%), major bowel (1,144,
  15.0%), major stomach/oesophagus (496, 14.7%), pancreas/liver/shunt (534, 11.6%), O.R. procedure for a complication of
  treatment (427, 11.0%), post-op/trauma infection with procedure (463, 18.4%), joint replacements, craniotomy, etc.
  The domain practitioner counts 23 procedure DRGs (22% of stays, 24% of AKI stays); dropping them costs
  0.726 -> 0.713 ROC AUC (their q2.json), against an SE of about 0.002. Each stay has at most one DRG flag; 60.8% have
  one.
- Comorbidity "Renal failure" (COM2) echoes the stay's own AKI (domain practitioner, reproduced here): set in 1,780
  stays although the cohort excludes eGFR < 60 in the first 24 h; AKI 29.8% in the 752 with no earlier renal
  diagnosis (history CCS 157 or 158), 17.4% in the 1,028 with one, 8.7% in the 70,804 with neither, 15.2% in the 4,373
  with history only. A chronic condition without its history running higher than with it fits a code for the stay's
  own renal failure. That is "a consequence or another encoding of the target" in LEAK-10's list.
- Coagulopathy and fluid/electrolyte disorders can arise in the stay (Elixhauser in the ICD-9 era had no present-on-
  admission flag; Glance et al. 2006 via the domain practitioner). Dropping them with renal failure costs 0.004.
- Medical DRGs (reason for admission) and chronic comorbidities (hypertension, diabetes, CHF, ...) carry content the
  team has at admission in substance; no measurement contradicts the source for them.

Closest precedents and how this case compares:
1. distribution_transformers_at_cauca_department (Lennart, 2026-10-21; leak_checks.md Mechanisms row "LEAK-10
   (decision ...)"): attributes possibly changed after the outcome for an unknown subset, not locatable row by row,
   carrying a gain (0.701 -> 0.639): dropped; "LEAK-10 stays as written, no amendment for a gain that may sit on the
   changed rows". kumc's procedure DRGs: late for an unknown subset (emergency operations), a gain of 0.013 that may
   sit on them. Same facts, decided the other way.
2. zillow_prize, melbourne_housing_market (Lennart, 2026-10-21; LEAK-7, LEAK-10 clause 2): the late part that can be
   located is blanked. kumc's late part is locatable by DRG type (the procedure DRGs, by name) and by the measured
   echo (COM2); it is kept.
3. fremtpl2 `BonusMalus` blanked where the data shows it does not behave like history, against bemtpl97 `bm` kept
   because its source registers it at the start of the period (Lennart, 2026-11-05; Mechanisms row "LEAK-10, LEAK-7
   (applied ...)"). This pair is the template: follow the source's timing where the data behaves as it says, fix the
   located part where the data contradicts it. kumc: the data contradicts the source for COM2 and the procedure DRGs,
   not (yet) for the medical DRGs and chronic comorbidities.
4. onlinenewspopularity (2026-10-26) and medical_facility_operational_data (2026-11-05): kept with a note only because
   the traceable late part showed no gain (within about two seed SDs). kumc's traced parts show a gain far above
   noise, so this keep-with-note route is closed.
5. bank_marketing `campaign` (Lennart, 2026-11-08, issue 2): kept with a note on 2026-11-06, then dropped as recorded
   after the prediction point. The curator's most recent call on the same question went to "out"; keeping kumc's
   procedure DRGs with a note would run against it (a drift risk, not yet a drift).
6. kickstarter `staff_pick`, heart_failure `time`, mic's ICU day-1..3 columns (Lennart, 2026-09-30): late content
   dropped once the prediction point was written down; mic followed its source's own list of what is known at
   admission.
7. LEAK-38 (homesite, african_credit_scoring, medical_facility, tunisian, 2026-10-22 to 2026-11-05) is the only rule
   that keeps fields of doubtful timing with a note, and it does not reach here: its scope is data the owner released
   for its own competition, and fields whose timing cannot be tested; "a field whose timing is known to be late is
   LEAK-10's". kumc is a research deposit and the timing is partly tested (COM2, procedure names).
8. Clinical siblings: diabetes_130_us uses discharge-coded diagnoses, but its prediction point is discharge (no
   conflict). wids_diabetes_mellitus uses APACHE admission diagnoses recorded in the ICU's first day, its stated
   prediction window (no conflict). southern_denmark_hospital_uti (screening) uses "past ICD-10 codes" only, as kumc's
   history block does (consistent). No curator decision on discharge-coded diagnoses at an admission prediction point
   exists yet. ny_sparcs_inpatient_length_of_stay's screening (AI, 2026-10-31, no curator call yet) lists APR DRG,
   MDC, severity and risk of mortality as "coded at or after discharge", to drop for an at-admission task. The AI has
   read APR-DRG two ways in two records; the curator's call here becomes ny_sparcs' precedent.

Drift / third exception: no third exception of this kind (no exception to LEAK-10 for "the source presumes it known"
exists). The register's LEAK-10 exception (loan_default_prediction_imperial_college, Andrej, 2026-11-03) dropped more,
not less; unrelated.

Reflection prompt (draft, issue shape):

**Consistency check (AI, 2026-11-08):** Keep the admission DRGs and comorbidities that the data shows were coded from the stay itself, unlike distribution_transformers_at_cauca_department and fremtpl2?

* **Problem:**
  - The definition keeps all 61 DRG and 27 comorbidity flags because the source "presumed" them known at admission, but the source's own dictionary names in-stay operations among the DRGs and the renal-failure comorbidity tracks the stay's own kidney injury[^1].
  - Where late values carried a gain, the earlier calls dropped them or blanked the part that could be located, and kept a source's timing only where the data behaved as the source said[^2][^3].
  - A required rule allows no one-off exception, so keeping everything needs a change of the rule instead[^4].
* **Background:**
  - The renal-failure comorbidity is set in 752 stays with no earlier kidney diagnosis, and 29.8% of them have the injury, against 17.4% of the 1,028 with one and 8.7% of stays with neither.
  - The 23 procedure DRGs (coronary bypass 27% injury, valve surgery 22%) cover 22% of stays; dropping them costs 0.726 to 0.713 ROC AUC, dropping both blocks 0.683.
  - The medical DRGs (the reason for admission) and the chronic comorbidities show no such sign.
* **Consistency:** distribution_transformers_at_cauca_department (2026-10-21, dropped, 0.701 to 0.639); fremtpl2 against bemtpl97 (2026-11-05, the source's timing kept where the data agreed); bank_marketing's campaign count (2026-11-08, a kept note reversed to a drop).
* **Options:**

  | | Option | What it does | Pro | Con |
  |---|---|---|---|---|
  | a | Keep what the data does not contradict | drop the renal-failure comorbidity and the 23 procedure DRGs; keep the medical DRGs and other comorbidities with the note, the source's placement as the reason | the bemtpl97/fremtpl2 pattern; the smallest fix; keeps most of the source's task (about 0.71) | the line between procedure and medical DRGs is ours; elective operations known at admission go too; coagulopathy and fluid disorders stay on a literature doubt |
  | b | Treat it like distribution_transformers | drop both blocks | only inputs surely known at admission; no judgment per flag | 0.683; drops content the team has at admission (the reason for admission, chronic disease) |
  | c | Keep everything (implemented) as a rule change | keep all flags with the note and amend the required timing rule so that a research source's explicit placement at the prediction point keeps a field; reopen distribution_transformers against it | the source's task exactly (0.726) | keeps a measured echo of the target; a source's assumption outranks a measurement, against the evidence order |

* **Recommendation:** a. A row in the Mechanisms table either way ("codes from a discharge abstract at an admission prediction point"), and the same call carried to ny_sparcs_inpatient_length_of_stay. **Decision:** a, b or c?

[^1]: **LEAK-10** (Must; amended 2026-11-08): a feature holds only what existed at the prediction point; out is "a part, a consequence or another encoding of the target"; a value read later goes where its late cells can be located (blanked), and where it cannot be located it goes when it may carry a gain, staying with a note only when the traced part shows none.
[^2]: **LEAK-7** (Should): the smallest fix that keeps a valid signal beats dropping the column. Cases: zillow_prize, melbourne_housing_market (2026-10-21).
[^3]: **EV-2** (Must): a measurement on the data outranks the source's primary documents, which outrank third-party pages.
[^4]: principles.md, "Exceptions and amendments": a Must has no exceptions; only a higher-ranked Must overrides it, anything else is an amendment. **LEAK-38** (Should) keeps fields of untestable timing with a note only in data an owner released for its own competition.

Notes for the AI (if a): the DRG list for "procedure" is the domain practitioner's 23 (the run folder
q1.py, q2.py); verify it against the APR-DRG surgical partition before coding it; re-run the block ablation; rewrite
the "Potential leak, kept on purpose" bullet and fit_reason accordingly.

======================================================================================================================
D2. The stated reason: "the source's own document places them at admission (EV-2)"
======================================================================================================================

Verdict: THE REASON DOES NOT HOLD AS STATED. The builder frames the conflict as the source's document (rank 2) against
third-party pages on UHC data and APR-DRG grouping (rank 4; claims.md item 23 marks "a discharge abstract coded after
discharge" as third party and general knowledge). That framing is right for the general claim, but the deciding
evidence is not third-party: the source's own dictionary names in-stay procedures among the DRGs (rank 2, the same
rank as the presumption, and specific where the presumption is general), and the renal-failure echo is a measurement on
the data (rank 1). EV-2's cases (kick, hr_analytics, intrusion_detection, 2024_lusaka_mobility) all let the
measurement or the specific document win. Whatever D1's outcome, the note should name these two facts and not rest on
"EV-2" alone. No separate curator question: it is settled with D1.

======================================================================================================================
D3. Forced IID: no dates (2007-2016), tag ForcedIIDFromTemporal
======================================================================================================================

Verdict: CONSISTENT. Precedents: mobile_churn, churn_telco_south_asia, bank_customer_churn, tour_travels_churn (one
undated snapshot or one stock month: IID, ForcedIIDFromTemporal; Lennart, 2026-10-21); bemtpl97 (one undated policy
year, cost not measurable; Lennart, 2026-11-04); fremtpl2 (2026-11-04/05). As in bemtpl97, the cost cannot be measured;
the leak tests across the split ran (lookup gain +0 on 9 splits, near copies gap +0.001).
One gap against SPLIT-8's text: it asks the notes to "say what the timestamp or a dated window would change and that it
should be recovered if a later release has it". The notes say the first (train on earlier years; ICD-9 to ICD-10 in
October 2015), not the second. The full de-identified set behind the data use agreement may hold the dates. A notes
fix, no curator question.

======================================================================================================================
D4. No patient key; repeat stays may fall on both sides
======================================================================================================================

Verdict: CONSISTENT. SPLIT-29 makes IID wrong when rows share an entity "that new data would not have" and the entity
carries the label; a hospital's next admissions include returning patients (the domain practitioner: "returning
patients are the norm"), so that condition is not met. Precedents: sepsis_survival_minimal_clinical_records (repeat
admissions on both sides, kept; Lennart, 2026-10-06); fremtpl2 (no groups invented from inferred links; 2026-11-04/05;
SPLIT-24, SPLIT-30); LEAK-8 / SPLIT-25 (retire rather than invent structure; maternal_health_risk and hazelnut were
retired on strong hidden-group evidence, which kumc lacks: 0 hidden-group candidates, near copies gap +0.001, lookup
+0). The notes state the limit.

======================================================================================================================
D5. Lab codes 0/1/2 decoded to missing / normal / abnormal by inference
======================================================================================================================

Verdict: DEPARTS WITH A STATED REASON; REASONABLE. The 2026-11-01 rule (CLEAN-12 case row "pva ... and 26 more":
"anonymized and undocumented codes ... stay codes") keeps codes the deposit does not name. The fact that sets the labs
apart: the source names the three states in words (paper, Methods), the dictionary gives each lab's reference range
("Albumin:3.5-5.5", "Glucose:80-160", "TroponinI:0-0.06"), and only the code-to-word mapping is inferred; the relabel
is lossless (three codes to three states). Closest precedent for an inferred reading: force_2020's units (CLEAN-21,
Lennart, 2026-10-21): inferred from the data and accepted when checked against a second, independent signal, masked
otherwise. Here code 0 = unknown is checked twice without the target (its share tracks how rarely a test is ordered:
ammonia 97%, troponin I 72%, platelets 6%). Code 1 = normal rests on one target-free signal (the majority of measured
values in all 14 tests) and one target signal (the AKI rate, 12 of 14).
Caveat: the curator excluded target information from reading scales ("we keep the ordinal from the context and logic,
not from target information", Lennart, 2026-10-31). The Decision table and the notes lead with the AKI rate. They
should lead with the target-free evidence (the reference ranges in the dictionary, which the notes do not cite yet, and
the majority share), the AKI rate a check only. No reflection prompt (a reason is stated); the builder's issue 2
already puts it to the curator.

======================================================================================================================
D6. Vital bands, race and sex kept as codes; code 0 of the vitals and labs set to missing
======================================================================================================================

Verdict: CONSISTENT. CLEAN-12's table (2026-11-01): "a code with no words anywhere (... an undocumented code) | the
code, as a category". The vitals are bands of a quantity, which the rule would decode "where the file stores a band's
number", but the band-to-code mapping is unknown and pulse contradicts Cheng et al. 2017's order (code 1 holds 16% of
stays), so they stay codes. The difference from D5 is stated: the data agrees with every target-free reading for the
labs and contradicts the documented order for the vitals. Code 0 to missing: CLEAN-10 ("a code that only means unknown
| missing"), as ANES's unknown codes (2026-10-30); the source's reason to keep "unknown" (the choice not to measure)
survives as a missing value.

======================================================================================================================
D7. age_band typed ordinal, codes 1-6 "youngest first", supported by the AKI rate
======================================================================================================================

Verdict: DEPARTS WITHOUT AN ADMISSIBLE REASON. The order of the age codes is undocumented (edges not published; claims
item 21: "order Inferred"), and the only support written down is the target ("the AKI rate rises from 7.2% to 10.5%").
That departs from the curator's rule of 2026-10-31 (order "from the context and logic, not from target information")
and from the same definition's vitals, whose undocumented order made them unordered codes (D6), the pulse showing that
these codes need not follow the earlier study's order. A target-free fact may exist: the counts rise with the code
(4,953, 7,920, 9,413, 15,784, 18,098, 20,789), as an adult inpatient population rises with age; it is not written down.

Reflection prompt (draft, issue shape):

**Consistency check (AI, 2026-11-08):** Keep the age bands ordered by their code when the same file's vital bands stay unordered for the same missing documentation?

* **Problem:**
  - The order of the six age codes is not published, and the definition supports it with the injury rate by band[^5].
  - The vital bands of the same file stay unordered codes because their order is undocumented, and the pulse codes do not follow the earlier study's order[^6].
* **Background:** The counts rise with the code (4,953 in code 1 to 20,789 in code 6), as an adult inpatient population grows older; Cheng et al. 2017 may list the age bands, not read yet.
* **Options:**

  | | Option | What it does | Pro | Con |
  |---|---|---|---|---|
  | a | Ordered, on the counts (implemented order) | keep the order; the notes give the rising counts and the dictionary's codes 1-6 as the reason, not the injury rate | age bands are ordered by nature; a target-free reason | the counts suggest the order, they do not prove it |
  | b | Unordered codes, like the vitals | type age_band as a plain category | the same rule for every undocumented band in the file | loses an order that is very likely right |
  | c | Look up the bands first | read Cheng et al. 2017's age bands and order by them if they fit the counts | the source's own order | one more reading; may not settle it (the pulse did not) |

* **Recommendation:** a, with c as a check where the earlier study is at hand. **Decision:** a, b or c?

[^5]: **CLEAN-14** (Should; amended 2026-10-30): an ordinal scale is an ordered category in the order its codebook gives; "we keep the ordinal from the context and logic, not from target information" (Lennart, 2026-10-31).
[^6]: **CLEAN-12** (Should; amended 2026-11-01): a code with no words (an undocumented code) ships as the code, as a category.

======================================================================================================================
D8. The 280 yes/no flags as 0/1 categories
======================================================================================================================

Verdict: CONSISTENT. CLEAN-14 as amended 2026-10-21 ("we should have one clear way to treat 0/1 flags"; first applied
on distribution_transformers_at_cauca_department): a 0/1 column whose meaning says yes/no is categorical.

======================================================================================================================
D9. Cohort filters known only after admission (stay of 2+ days, 2+ creatinine values, no eGFR < 60 or creatinine
    > 1.3 within 24 hours)
======================================================================================================================

Verdict: CONSISTENT IN SUBSTANCE; TWO BOOKKEEPING GAPS. USE-7 is not the governing rule (it drops rows lacking the
input the prediction acts on; nothing is dropped here). The governing precedents:
- LEAK-22: follow the paper's cohort (diabetes_130_us, Lennart, 2026-09-30); and we never select on the future
  ourselves (framingham_heart_study_fhs, 2026-10-22). The selection is the source's, made before release, and cannot
  be undone (the excluded stays are not in the file).
- The LEAK-41 text: "a selection the source made before release, the same in train and test, that cannot be undone,
  defines the task's population and is sized in the notes" (pricing_game_2016_french_fleet, the organisers' 30-day
  floor; 2026-11-06/08).
- Selection Bias with an approximate fit when the deployment setting does not share the selection
  (lt_vehicle_loan_default_prediction, Lennart, 2026-11-05: "here we know we would want to use more but dont have
  it"; tunisian_fraud_detection_challenge, 2026-11-05; USE-8, selection.md). The definition names it in fit_reason and
  declares the fit approximate: consistent.
Gaps (fixes, no curator question):
1. The notes name `Selection Bias`, but the record carries no `decision_markers: [Selection Bias]`; lt_vehicle_loan and
   tunisian carry it in the record.
2. The notes do not size the selection (pricing_game_2016 does). If the paper's flow gives the counts excluded by each
   filter, they belong in the notes. fit_reason names the 2-day floor but not the 24-hour creatinine filter, which also
   uses the label's own measurement after admission (it removes stays whose creatinine rose in the first day).

======================================================================================================================
D10. Metric: fallback roc_auc
======================================================================================================================

Verdict: CONSISTENT. The paper reports AUC, sensitivity, specificity, precision and F-measure side by side, with a
threshold picked per model for the best F-measure: several metrics and no fixed threshold. Precedents: gallstone_disease
and early_stage_diabetes_risk_prediction (MET-5, several metrics: fallback); heart_disease (MET-6/7/8, Lennart,
2026-10-21, checked 2026-10-27); ljubljana_breast_cancer (MET-6); sepsis_survival_minimal_clinical_records (roc_auc over
the paper's PR AUC, Lennart, 2026-10-21). A per-model F-optimal threshold is no fixed decision (MET-6). No metric from
context (MET-11) is more obvious for an admission risk flag; the domain practitioner agrees.

======================================================================================================================
Register flags
======================================================================================================================

None of the 34 flags is about this dataset. Read behind the two near ones:
- "drift, mechanism: post-outcome feature (Lennart: keep up to 2026-11-05, exclude from 2026-11-08)": a false positive;
  the 2026-11-08 "exclude" decisions are the nfip duplicate verdicts, not leak calls. The real recent signal on
  post-outcome features is bank_marketing's `campaign` (D1, precedent 5).
- "exception_to_must LEAK-10" (loan_default_prediction_imperial_college, Andrej, 2026-11-03): an exception that drops
  more; unrelated to keeping late fields.
No amendment-due flag touches LEAK-10, SPLIT-8, SPLIT-29, CLEAN-10/12/14 or MET-5/8.

Paths
- Definition: datasets/_dev/tabarena-v0pt2/kumc_inpatient_aki_prediction/dataset.py
- Record: curation/records/kumc_inpatient_aki_prediction.md
- Rules: .claude/skills/knowledge-curation/references/leak_checks.md (LEAK-10 at line 78, Mechanisms table from line 475), cleaning_features.md, splits.md, evidence.md
- Panel finding reproduced: panel/domain_practitioner.report.txt (Q1, renal failure)
```

</details>

<details><summary>Advocate</summary>

```text
ADVOCATE, OPENING BRIEF: kumc_inpatient_aki_prediction (2026-11-09)

Position: ship. The task, the target, the history/lab/vital features, the split and the metric hold. Two parts of the
definition do not hold as written, and I concede them: the renal-failure comorbidity (a measured echo of the target,
dropped without a decision) and the operation DRGs (issue 1, where I back the precedent checker's option a, the mildest
fix that meets LEAK-10). Everything else the panel found is a notes or naming fix.

1. A real task, reproduced at the source (P2, P3; SEL-1, SEL-2, USE-1, USE-5 Must; USE-8).
   Evidence: CC0 deposit tied to the JAMIA Open paper (claim auditor 1-6). The paper names actor, moment and decision
   (Perspective #2, "(past, admission)"). Counts equal the paper exactly, 7,259 / 69,698 (claim 7). KDIGO creatinine is
   the field's standard outcome and "the thing I act on, not a proxy" (domain practitioner Q2). LightGBM 0.716-0.725
   against the paper's 0.734, which also used 1,271 medication columns. The domain practitioner: "Recommendation: ship",
   fit approximate. The blind reviewer, without our notes: "a genuine one with moderate signal at a usable size".
   Outranks: every objection below is P4 or lower. The tension row "a real task against a leak" says fix the leak and
   keep the task (kickstarter).

2. No shortcut and no leak in 214 of the 302 features (P4; LEAK-10 Must, LEAK-13 to LEAK-16, LEAK-39).
   Evidence: the task gamer found nothing beyond seed noise (row order AUC 0.499, train/test classifier 0.4996, kNN and
   frequency features within noise, copies 0.11-0.14% of test rows). Best single feature 0.544. The history block is
   cut by date: P1 adds 55,819 flags over P2 and removes none, and acute trauma stays carry their own diagnosis in only
   9-18% (claim 26). CCS 157 is in 9.1% of AKI stays, so the stay's own AKI code is absent. Admission-day labs are not
   post-onset: BUN abnormal in 18.6% of early AKI against 18.4% without AKI (column auditor). The admission-day
   diagnoses in the history (54-84% for medical admissions) fall inside the source's window, so they are legitimate.
   That needs a wording fix ("recorded up to the admission day"), not a change.

3. Concede: `comorbidity_renal_failure` is a partial encoding of the target. Drop it. That is a fix, not a decision
   (LEAK-10 Must, "a consequence or another encoding of the target"; LEAK-6: a confirmed leak goes even when small).
   Evidence: three agents found it independently. Stays with the flag and no earlier renal record have 28.8-29.8% AKI,
   against 16.6-17.4% for stays with the flag and a record. This holds in a cohort that excludes eGFR < 60 at
   admission. Cost 0.0024-0.003 ROC AUC, 5 of 5 folds. The remedy ladder puts "fix the definition" before anything
   milder or harsher. The leak note should name this measured case in place of the "fluid and electrolyte,
   coagulopathy" example.

4. Keep the medical DRGs and the other 26 comorbidities with the note (P4; LEAK-10 clause 2 Must, EV-2; the bemtpl97 and
   fremtpl2 template).
   Evidence: LEAK-10 clause 2 keeps values of doubtful timing with a note "only when the part that can be traced shows
   none". The traced test for the other acquirable comorbidities shows none. Stays with the flag and no earlier record
   against stays with the flag and a record: coagulopathy 14.9 vs 14.3%, fluid and electrolyte 12.6 vs 12.0%, CHF 18.0
   vs 17.4% (claim auditor R1). Renal failure differs on the same test, 28.8 vs 16.6%. The chronic comorbidities show
   no excess (column auditor: hypertension, diabetes, hypothyroidism). The medical DRGs are the reason for admission,
   which the team knows at admission. The history block itself shows it: the matching diagnosis is set by the
   admission day in 44-76% of acute medical stays. The precedent checker: "no measurement contradicts the source for
   them".
   Against the column auditor's (c') (0.688) and option b (0.683): the higher-ranked evidence is a measurement (EV-2).
   The Glance 2006 shares (43% and 25%) are third-party figures for another population, and they rank below a
   measurement on these rows. Dropping the five "acquirable" comorbidities as well costs only 0.0033 (task gamer), so
   if the curator prefers caution here, it is cheap. That would be a curator's weighing call, not a validity
   requirement.

5. Concede in part: the operation DRGs cannot stay under LEAK-10 as written. The mildest fix keeps the dataset (issue 1,
   precedent checker's option a).
   Evidence: 20-25 procedure groups. CABG 27%, valve 22%, APR-DRG 710 "infectious w O.R. procedure" 31.3%, and 443
   kidney/urinary procedures (claim auditor R2). Dropping them costs 0.726 -> 0.708-0.713. The late part (emergency
   operations) cannot be located row by row (no admission type). distribution_transformers_at_cauca_department decided
   the same facts as "drop". No higher-ranked Must lets a source's "presumed" override a Must (Exceptions: a Must has
   no exceptions). Part of that 0.013 is legitimate, because elective operations are known from the OR schedule. The
   rule still drops a gain that "may" sit on the late rows. The builder's reason "kept because the source's document
   places them at admission (EV-2)" has to go either way (precedent checker D2). The result keeps about 0.71 and most
   of the source's task, against 0.683 for dropping both blocks.

6. The split is right and the repeat patients are measured small (P4; SPLIT-8 Should, SPLIT-13, SPLIT-29).
   Evidence: no date, year, encounter order or ICD-10 marker exists. Order within the label blocks gives AUC
   0.503/0.516, so forced IID is the only option. Repeat stays are common (44-61%), but purging likely twins changes
   LightGBM by 0.0015, a deep forest by 0.008, and the model ranking not at all. Half of that would be legitimate under
   the temporal regime the use case implies, because returning patients are known entities in the admission stream
   (SPLIT-13). The precedents agree: sepsis_survival_minimal_clinical_records, bemtpl97, the churn snapshots. Fixes,
   all notes: correct "SPLIT-29 cannot be checked" to the measured numbers, and add SPLIT-8's "recover the dates if a
   release has them" (the DUA set).

7. Worth benchmarking, by the right metric, and the cleaning gaps are cheap fixes (P6, P7; TP-1 to TP-10, MET-5 to
   MET-8, CLEAN-12/14 Should; tension "a real task against imperfect cleaning").
   Evidence: 2,419+ positives per test fold, no task-probe flag, model spread 0.031. With the operation DRGs and renal
   failure dropped, the signal is still about 0.71 against 0.5. A sparse, mostly binary EHR table is diversity the
   collection lacks (blind reviewer). roc_auc is endorsed by the domain practitioner and the precedent checker (D10,
   heart_disease, gallstone_disease). The lab decoding is confirmed by target-free evidence, 16 of 18 diagnosis-lab pairs
   (claim 17). The P7 findings have mild fixes:
   - Decode sex (certain, 1,553 of 1,553 prostate stays are code 2).
   - Decode race and the age labels from Cheng 2017 (shares within 1.5-2.5 points).
   - Order BMI and BP by Cheng's Table 2 if the curator wants it; otherwise keep the codes with a note.
   - Rename DRG 710 and 443 to show the procedure, and `comorbidity_diabetes_w_ccs` to `..._or_none` with a note.
   - Lead the lab Decision with the target-free evidence.
   - Add the Selection Bias marker to the record.
   The precedent checker's D7 (age ordered on the target) is answered by target-free facts: pregnancy flags fall to
   0% after band 3, and the band shares match Cheng's bands. Keep the order and replace the reason.

Judgment record (advocate's):
Verdict: ship after changes.
Validity: SEL-1, SEL-2 hold; USE-1 holds (fit approximate, USE-8); LEAK-10 triggered twice. Fixed: `comorbidity_renal_failure`
dropped (measured). Curator's call: the operation DRGs (recommend a, drop about 20-25 groups). Medical DRGs and the
other comorbidities kept with a note (the traced test shows none). SPLIT-8 holds (forced IID); SPLIT-29 measured small.
Value: TP flags none; roc_auc (MET-5 fallback).
Quality: CLEAN-12 fixes: decode sex, race and age labels; renames; reword the notes.
For the curator: issue 1 (operation DRGs, a against c); issue 2 (decode the vitals or keep the codes).

======================================================================================================================
Rebuttal
======================================================================================================================

The critic and I agree on the verdict ("ship after changes"), on the renal-failure drop, on the procedure DRGs, and on
every notes and cleaning fix. Two questions remain open: the medical DRGs and the six "acquirable" comorbidities.

C1. comorbidity_renal_failure. CONCEDE, as in my point 3. Drop the column. Dropping is better than blanking on a
    history proxy (the critic's reason holds: the late cells would be located by a proxy, not a date).

C2. Procedure APR-DRGs. CONCEDE the procedure groups, as in my point 5. Check the list against the APR-DRG surgical
    partition, and include 710 and 443. The builder's EV-2 reason inverts the evidence order and goes.
    DISPUTE the add-on that the medical DRGs should go too (LEAK-10 clause 2; EV-2; the fremtpl2/bemtpl97 template).
    - Clause 2 drops values whose late part may carry a gain. For the medical groups no late part has been traced.
      The "no operation in this stay" reading is real only through the O.R. groups. The 720 -> 710 move is a property
      of 710, and 710 goes under C2.
    - With the O.R. groups out, the medical block is worth 0.7130 -> 0.6952 (column auditor). Nothing ties that gain
      to post-admission content.
    - The critic's own fact points the other way. The matching diagnosis is in the history by the admission day in
      44-76% of acute medical stays, which measures that the admission reason is known at the prediction point. That
      makes the "after study" final group a refinement of a known value, not a late one.
    - Precedent: bemtpl97 follows the source's timing where the data behaves as the source says. The precedent checker
      found that "no measurement contradicts the source for them".
    - It stays the curator's call. Keeping the medical DRGs is consistent with the rule. Dropping them is a stricter
      reading that the rule does not require.

C3. Six acquirable comorbidities. DISPUTE as a Must for coagulopathy and fluid/electrolyte. CONCEDE that four are
    untested on the decisive cut.
    - The critic's test compares "flag, no history" with "history, no flag". That confounds "arose in the stay" with
      "active in this stay". A pre-existing condition that is coded now is expected to carry more risk than one that is
      only in old records. The hypertension result (1.37 vs 1.59) shows the test is noisy in both directions.
    - The decisive cut (EV-1) holds the flag fixed and varies only the prior record. That is the claim auditor's R1:
      renal failure 28.8 vs 16.6% (late), coagulopathy 14.9 vs 14.3%, fluid/electrolyte 12.6 vs 12.0%, CHF 18.0 vs
      17.4% (no late signature).
    - Under clause 2 ("stay with a note only when the traced part shows none") the traced part shows none for these
      two. A measurement on these rows outranks Glance 2006, a third-party study of another population (EV-2).
    - The task gamer's 11,553 no-history stays carry the chronic flags too (1.98 flags on average). That shows where the
      codes come from, not when the conditions began.
    - Weight loss, pulmonary circulation, deficiency anaemias and chronic blood-loss anaemia were not run on the
      decisive cut. I cannot back keeping them.
    - Mildest path: run R1's cut on those four (one script, work_claim_auditor/t4_inStay.py). Drop any that show
      renal failure's gap, and keep the rest with the note.
    - If the curator prefers not to wait, dropping all six costs 0.0033-0.0055. That is a cheap weighing call, not a
      validity failure.

C4. Repeat patients and SPLIT-8 notes. CONCEDE. My point 6 asks for the same notes: the measured 44-61% / 0.0015, the
    "recover dates from a dated release" sentence, and the possible ICD-10 thinning after 2015-10. The split stays.

C5. Fit gaps (USE-8). CONCEDE. Reword fit_reason to name the 2+ creatinine values, the 24-hour exclusion and the
    missing admission creatinine. Add `decision_markers: [Selection Bias]` to the record. Reword "earlier records" to
    "recorded up to the admission day".

C6. Cleaning (CLEAN-12/14). CONCEDE all of it, as in my point 7. Give the age order its target-free reason, with
    labels as edges. Decode sex, and decode race or record the evidence for it. Rename diabetes_w_ccs and add a note.
    Lead the lab Decision with the reference ranges. Make BMI and BP ordinal or add a note.

Net: the only disagreement is how much of LEAK-10 clause 2 reaches beyond the procedure groups and renal failure. My
position: the medical DRGs, the chronic comorbidities, coagulopathy and fluid/electrolyte stay with a note; the four
untested comorbidities are decided by one more run. The critic's position: drop the six, and the curator decides the
medical DRGs. Both sides land between 0.706 and about 0.713, so P6 holds either way.
```

</details>

<details><summary>Critic</summary>

```text
CRITIC, OPENING BRIEF: kumc_inpatient_aki_prediction (2026-11-09)
Read: dataset.py, README.md, record, builder_report.md, principles.md, leak_checks.md (LEAK-6, -7, -10, -38), the
seven phase-A reports. No new measurements of my own; every number below is a panel agent's, cited by report.

POSITION: ship only after changes. The task is real (USE-1, SEL-2 hold; no agent disputes it) and I do not ask for
exclusion. But the definition keeps, "with a note", features that the panel measured as late or as an echo of the
target. Under LEAK-10 (Must) that is not a note case: a Must has no exceptions (principles.md, "Exceptions and
amendments"). Points 1-3 are Must fixes in the definition; 4-6 are notes and cleaning.

1. P4, LEAK-10 (Must) with LEAK-6 (Must): `comorbidity_renal_failure` is in part the stay's own AKI.
   Problem: the cohort excludes eGFR < 60 or creatinine > 1.3 in the first 24 h, yet 1,780 stays carry the flag; 752
   of them have no earlier renal diagnosis (history CCS 157/158), and those run at 29.8% AKI against 17.4% for the
   flagged stays with a renal history and 8.7% for neither. A pre-existing condition is not riskier when it is new to
   the record. By AKI timing: flag in 7.0% of early AKI, 5.1% of later AKI, 2.0% of no AKI. Mechanism: the Elixhauser
   renal-failure set holds ICD-9 586 "renal failure, unspecified", coded for in-hospital kidney failure.
   Evidence: found independently by the domain practitioner (q1.py), the column auditor (timing.out, item 1) and the
   claim auditor (R1, a second cut: 28.8% vs 16.6%); reproduced by the precedent checker. Gain 0.0024 ROC AUC, 5/5
   folds, SE 0.0002.
   Effect: one feature is "a consequence or another encoding of the target" (LEAK-10's list). LEAK-6: "a confirmed leak
   goes even when small" (santander +0.003). The notes name the wrong comorbidities as the in-stay example.
   Remedy: drop the column (one line), whatever is decided on points 2-3. Blanking it where no renal history exists
   (LEAK-7) would rest the "located" late cells on a history proxy, not on a date; dropping costs the same.

2. P4, LEAK-10 (Must, second clause): the procedure APR-DRGs are set by operations of the stay, and the note that keeps
   them misreads EV-2.
   Problem: a base APR-DRG is assigned after discharge from the principal diagnosis "after study" and the procedures
   done. 20 kept groups are O.R.-procedure groups and 5 non-O.R. procedure groups (column auditor item 2; the domain
   practitioner counts 23): coronary bypass 27.2% / 27.4% AKI, valve 21.9%, bowel 15.0%. Two are hidden by their
   shipped names: `admission_drg_infect_parasitic_disease` is APR-DRG 710 "... w O.R. procedure" (31.3% AKI, n=469, the
   highest of all 61) and `admission_drg_kidney_urin_tract_nonmalig` is APR-DRG 443 "kidney & urinary tract
   procedures" (18.9%) (claim auditor R2, column auditor; dictionary order). An emergency operation decided on day 2 is
   not known at admission; which stays were elective cannot be located (no admission type).
   Evidence: without the 20 O.R. groups 0.7234 -> 0.7130; without all 25 -> 0.7083 (column auditor, ablation.out);
   0.726 -> 0.713 for the 23 (domain practitioner q2.json). SE about 0.002-0.005: far above noise. Task gamer: the two
   blocks lift every model by 0.043; no other exploit found.
   Rule: LEAK-10's second clause: late values that cannot be located row by row "go when they may carry a gain and stay
   with a note only when the part that can be traced shows none". The traced part shows 0.011-0.015. LEAK-38 (Should,
   keep with a note) does not reach: it covers owner-run competition data of untestable timing; this is a research
   deposit and the timing is partly tested. EV-2: "presumed to be available at admission" (He 2019) is an assumption,
   and the same authors call the UHC data "not immediately available" and warn that comorbidities "that developed
   during the admission" may be misrepresented (Cheng 2017, Limitations, column auditor item 2). The measurement and
   the specific source text outrank the general presumption; the builder's "kept because the source places them at
   admission (EV-2)" inverts the order.
   Precedents decided the other way: distribution_transformers_at_cauca_department (late for an unknown subset, gain,
   dropped; Lennart 2026-10-21), bank_marketing `campaign` (note reversed to drop, 2026-11-08), mic and kickstarter
   (late content dropped once the prediction point was set). Keeping all 61 is precedent checker D1's "departs, no fact
   that sets it apart", case 1 and 2 of the consistency check.
   Remedy: drop the procedure DRG groups (the list checked against the APR-DRG surgical partition, the two misnamed
   groups included), rename the two groups if they stay for any reason, and rewrite the leak bullet and fit_reason.
   For the curator: whether the medical DRGs go too. The grouper's medical group also says "no operation in this stay"
   (a septic patient operated on moves from 720, 14.9%, to 710, 31.3%), and the history block already carries the
   admission reason in 44-76% of acute medical stays, so dropping the whole block (0.6952) costs less use case than its
   0.028 suggests. I ask at least for the procedure groups; the whole block is the cleaner reading of LEAK-10.

3. P4, LEAK-10 (Must, second clause): the comorbidities that arise in the stay.
   Problem: the 27 flags are Elixhauser comorbidities of the discharge abstract, with no documented present-on-admission
   filter. Fluid and electrolyte disorders (ICD-9 276.x: hyperkalaemia, acidosis, fluid overload, consequences of AKI),
   coagulopathy, weight loss, deficiency anaemias, chronic blood loss anaemia and pulmonary circulation disease can be
   coded for the stay.
   Evidence: the new-vs-history test of point 1, weaker but the same direction for each (newly coded RR vs history-only:
   weight loss 1.71 vs 1.05, pulmonary circulation 1.97 vs 1.31, coagulopathy 1.68 vs 1.36, deficiency anaemias 1.53
   vs 1.35, fluid/electrolyte 1.48 vs 1.35), while chronic conditions show none (hypertension 1.37 vs 1.59)
   (column auditor). 11,553 stays with no history at all carry fluid/electrolyte in 12.8% and coagulopathy in 4.7%
   (task gamer). Glance et al. 2006: 43% of Elixhauser coagulopathies and 25% of fluid/electrolyte disorders were
   complications (third party, domain practitioner). Gain 0.0033 (5 columns, 8/9 splits, task gamer) to 0.0055 (6 with
   renal failure, column auditor).
   Rule: as point 2; a gain above noise on a part that cannot be located row by row.
   Remedy: drop these 6 (with point 1's, 7 columns); keep the 20 chronic comorbidities with the note. Combined with
   point 2's O.R. groups: 0.7062 measured (column auditor); still clearly above dummy 0.5 and the linear 0.708 level of
   the full set, so P6 holds.

4. P4, SPLIT-29 / SPLIT-8 (Should; notes): the notes understate repeat patients and the forced split's cost.
   Evidence: the paper's 179,370 encounters of 96,590 patients imply 44-61% of kept stays share a patient; 16.6% of
   rows have a likely-same-patient partner (23x the cross-sex control); purging partners costs LightGBM 0.0015 overall
   (0.019 on partnered rows), a deep random forest 0.0077, ranking unchanged (split auditor F2). The notes say "21 rows
   ... may be one patient's repeat stays" and "SPLIT-29 cannot be checked". SPLIT-8 also asks the notes to say a dated
   release should be split by time (precedent checker D3); the ICD-9-only history may thin after October 2015 (claim
   auditor U3).
   Remedy: notes only; the split stays (forced IID is right, split auditor).

5. P3, USE-8 (Should; fit_reason and record): the fit understates the gaps.
   Evidence: fit_reason names the 2-day floor but not the "2+ creatinine values" and the 24-hour creatinine exclusion,
   both post-admission (precedent checker D9); no admission creatinine (excluded by the source; domain practitioner);
   the record lacks `decision_markers: [Selection Bias]` that the notes name (D9, as lt_vehicle_loan, tunisian).
   task_summary.known says the history is "earlier records", but it holds diagnoses recorded up to the admission day
   (54-84% of acute medical stays carry their own diagnosis; claim auditor W1, column auditor item 6) - inside the
   source's window, so a wording fix, not a leak.
   Remedy: fit_reason and known reworded; marker added to the record.

6. P7, CLEAN-12 / CLEAN-14 (Should; quality, not a reason to exclude):
   - `age_band` is ordered on target information (the AKI rate), against the curator's 2026-10-31 rule; target-free
     support exists (counts rise with the code; shares match Cheng 2017's 18-25 ... 56-64 within 1.5 points, band 6 =
     65+) (precedent checker D7, claim auditor R5). Remedy: rewrite the reason, labels as edges.
   - `sex_code` decodes with certainty (1,553/1,553 prostate hyperplasia stays code 2; uterine DRG 413/413 code 1) and
     `race_code` matches Cheng's table order within 2.5 points (claim auditor R3, column auditor item 4). The notes'
     "codes without words" is wrong. Remedy: decode sex; decode race or note the evidence.
   - `comorbidity_diabetes_w_ccs`: 83% of its rows have no other comorbidity and look nothing like diabetes (prior
     diabetes record 2.4%, AKI 5.1%) (column auditor item 3, blind reviewer 4, task gamer). Name and notes misstate the
     column. Remedy: rename, a notes bullet.
   - Lab Decision table leads with the AKI rate; lead with the dictionary's reference ranges and majority share
     (precedent checker D5). BMI and BP follow Table 2's order on target-free evidence (obesity 92% in band 4; claim
     auditor R4): ordinal or a note.

Not argued: the metric (roc_auc; every agent agrees, MET-5/6/8), ethics and licence, the lab decoding itself, the
history block's timing (measured fine), the duplicates.

Judgment record as I would write it:
  Verdict: ship after changes.
  Validity: USE-1 holds; LEAK-10 triggered three times, fixable in the definition (drop comorbidity_renal_failure;
  drop the procedure APR-DRGs; drop 6 in-stay comorbidities); SPLIT-8 holds (forced, notes); SPLIT-29 notes corrected.
  Value: TP holds after the drops (about 0.706).
  Quality: CLEAN-12/14 fixes (sex, race, age reason, diabetes_w_ccs name).
  For the curator: whether the medical DRGs go with the procedure groups (point 2).

======================================================================================================================
Rebuttal
======================================================================================================================
Against the advocate's opening brief (advocate.report.txt). No new measurements of my own.

A1 (a real task; SEL-1, SEL-2, USE-1, USE-5). Concede. I never asked for exclusion. The tension row "a real task
   against a leak" says to fix the leak and keep the task, which is my position too.

A2 (no shortcut in the other 214 features; history, labs, row order). Concede. The history block is cut by date (P1
   vs P2), early-AKI BUN is 18.6% against 18.4%, and the task gamer found nothing beyond noise. The "earlier records"
   wording is a fix, as in my point 5.

A3 (drop `comorbidity_renal_failure`). Agreed. This is my point 1.

A4 (keep the other 26 comorbidities and the medical DRGs with the note). Concede in large part, and I withdraw part of
   my point 3. The advocate cites the better test. Claim auditor R1 compares flagged stays with no renal or matching
   history against flagged stays with one. That is the same test that exposed renal failure (28.8 vs 16.6%), and it
   shows no excess for coagulopathy (14.9 vs 14.3%), fluid and electrolyte disorders (12.6 vs 12.0%) or CHF (18.0 vs
   17.4%). My RRs came from the column auditor's other comparison, newly coded against history only. That comparison
   is confounded: an old record without a current flag can be a resolved condition, and it reverses for hypertension
   (1.37 vs 1.59). A measurement on these rows outranks Glance 2006's third-party shares (EV-2). So under LEAK-10's
   second clause, coagulopathy and fluid/electrolyte stay with the note. I maintain one thing. Weight loss, deficiency
   anaemias, chronic blood loss anaemia and pulmonary circulation disease were never put through R1's test, and only
   the confounded comparison speaks for them (1.71 vs 1.05, 1.97 vs 1.31). The traced part has to show no gain before
   a value stays with a note (LEAK-10 clause 2, EV-1: facts first). Remedy: run R1's test on those four. Each stays
   with the note if it shows no excess and goes if it does. That is a check, not a drop on doubt.
   Medical DRGs: concede that no measurement contradicts the source for them. My "no O.R. in this stay" argument (720
   vs 710) is reasoning, not a measured gain. It stays a question for the curator, not a requirement.

A5 (the operation DRGs go). Agreed on the fix. I dispute two things:
   (i) The framing. The advocate's judgment record lists this as "Curator's call ... recommend a, against c". Keeping
       all 61 is not an available option: a Must has no exceptions (principles.md). The definition must drop the
       procedure groups, or the curator must amend LEAK-10 knowingly (the precedent checker's option c as a rule
       change). It is not a weighing call.
   (ii) The scope. Take all 25 procedure groups, not "about 20". The five non-O.R. groups (PCI with AMI, PCI without
       AMI, cardiac cath with and without ischaemia, BMT) are as often decided during the stay after an emergency
       admission. PCI with AMI is the typical case. The column auditor measured 0.7130 without the 20 O.R. groups and
       0.7083 without all 25, so the extra five carry a gain too, and that gain cannot be located row by row
       (distribution_transformers). Check the list against the APR-DRG surgical partition, as the precedent checker
       asks.

A6 (the split, repeat patients measured small). Concede. Forced IID stays, and the notes take the measured numbers and
   SPLIT-8's "recover the dates". This matches my point 4.

A7 (worth benchmarking, metric, cheap P7 fixes). Concede, including the pregnancy-by-band fact as a target-free reason
   for the age order. One gap: the advocate's list leaves out my point 5's fit_reason text. The "2+ creatinine values"
   requirement and the 24-hour creatinine exclusion are post-admission selections, and the admission creatinine is not
   a feature (USE-8, precedent checker D9). Both belong in the fit_reason with the Selection Bias marker.

Where we still differ:
- The four untested in-stay comorbidities: run R1's test first, then decide on the result.
- The procedure DRGs: required by a Must, not a weighing call, and all 25 groups rather than 20.
Everything else is agreed: drop renal failure; drop the procedure DRGs; keep the medical DRGs, the chronic
comorbidities, coagulopathy and fluid/electrolyte with a corrected note; fix the notes and naming.
```

</details>
