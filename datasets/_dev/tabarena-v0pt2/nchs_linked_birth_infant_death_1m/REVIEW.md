# nchs_linked_birth_infant_death

**Outcome:** added as `nchs_linked_birth_infant_death_1m`. NCHS's public-use linked birth/infant death files of the birth cohorts 2017-2023 (25.9 million births to U.S. residents, 0.553% infant deaths), one row per birth with the certificate's items known at the birth, tested on the birth years 2021, 2022 and 2023 (500k births each) with a random million earlier births per train side; the AI recommends shipping it after the panel's changes, which are made.

```text
Verdict: ship after changes (made).
Validity: the cohort join is the user guide's; no twin or sibling crosses the split; exact copies across the split 0.0%. Four values recorded after the birth were found and fixed: the prior-birth counts of later-born twins are blanked (they counted the co-twin); the cyanotic heart disease item (CA_CCHD, from physician progress notes) and the paternity acknowledgement (MAR_P, signed in the hospital) are dropped; the karyotype levels 'confirmed' and 'pending' are merged into 'yes'. In 2017-2019 NCHS imputed a missing birthweight only for infants who died, so those imputed values are blanked, and the note that called the imputation 'label-free' is corrected. Each costs at most 0.0018 ROC AUC.
Value: a real signal (tuned LightGBM 0.920 ROC AUC, best single feature 0.835; linear 0.902, random forest 0.888); the task gamer's largest exploit left is about 0.002. The probe numbers (tuned 0.920, single feature 0.835, linear, random forest, copies across the split) come from the definition before the panel's changes and were not re-run on the final one; each change cost at most 0.0018 ROC AUC in the panel's experiments.
Quality: the birth-interval code for 'plural delivery' (000-003), which shipped as 3 months, is now missing; mother's age and the cigarette counts stay ordered categories because their top value is a cut-off ('or more'), as in mic; plain numbers would be a departure, not raised as an issue.
Weighed: source +, size +, reviewer agreement +, gaming resistance +.
For the curator: 1, race and Hispanic origin as inputs; 2, the outcome-marked unknowns kept with a note; 3, the narrowed use case and a second folder for the screen at registration; 4, the metric.
```

**Main points:** Drop the parents' race and Hispanic origin (every reviewer recommends it); keep or remove the unknowns that mark early deaths; confirm the use case narrowed to expected deaths at the birth and whether the screen at registration gets its own folder; score log loss (recommended if the use case stays narrowed) or keep ROC AUC.

**Issues for the curator:**

1. **Drop the parents' race and Hispanic origin as inputs?**

   * **Problem:**
     - Four inputs are the mother's and the father's race and Hispanic origin, as in NCHS's tables of infant mortality.
     - Whether a protected ground may be an input here is one of the protected-grounds calls the curator keeps on the review page (the **across-datasets protected-grounds item**); decide it there or here, the same way.
   * **Effect on the task:** none measurable: without them ROC AUC is 0.9148, against 0.9149 and 0.9158 with them (same splits); the domain practitioner measured -0.0009 ROC AUC and +0.2% log loss over three seeds of a calibrated model, within the seed spread of 0.004; the claim auditor's re-run without them: 0.9195 / 0.9214 against a base of 0.9195-0.9216.
   * **Background:** no U.S. law names an infant-mortality risk score; an expected-deaths model for comparing hospitals is no decision on a person, while a follow-up decision on a family in a federally funded programme falls under Title VI (42 U.S.C. 2000d) and the 2024 rule of ACA section 1557 on decision support tools (45 CFR 92.210)[^sel1].
   * **Consistency:** keeping them matches the clinical datasets that keep race, but departs from the batch's method (the dataset rais dropped race for a service to a person, because the actor's own law constrains the factor) with no stated reason; dropping them removes the departure[^tension].
   * **Panel:** every reviewer recommends dropping them: the builder, the column auditor, the domain practitioner, the advocate and the critic.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep (implemented) | the four columns stay inputs, with the note | as NCHS tabulates; the expected-deaths use makes no decision on a person | departs from the batch's method for race (rais dropped it) with no stated reason; the race columns add no measurable score |
     | B | Drop | the four columns go | costs nothing measurable; consistent with the batch's method; every reviewer agrees | a field that NCHS's own risk tables use is lost |

   * **Recommendation:** B, drop them. **Decision:** A or B?

   **Notes for the AI:** on B, add `MRACE15`, `MHISP_R`, `FRACE15`, `FHISP_R` to a dropped list in `_clean` (remove them from `CODED`, `CODE_LABELS`, `MISSING_CODES`, `REPORTING_FLAGS`), rewrite the "Note (SEL-1)" bullet as a dropped bullet with the numbers above, remove "race, Hispanic origin" from `task_summary.known`, and re-run `dataset check`.

   [^sel1]: **SEL-1** (Must): a task with ethical concerns is out; the tensions table's row "a factor the actor may no longer use" (P1).
   [^tension]: Precedent check, section D5: the dataset rais dropped its protected grounds on Title VI reasoning (45 CFR 80.3) for a service to a person.

2. **Keep the unknowns that mark early deaths, with the note?**

   * **Problem:**
     - The certificate of an infant who died within a day is less complete: most items are unknown 3 to 12 times as often among those deaths as among survivors, the newborn's measurements 17 to 90 times.
     - Those unknowns cannot be told row by row from the ordinary ones, so they stay with a "Potential leak, kept on purpose" note.
     - Two earlier datasets, mic and 2_month_survival, removed such a mark (2_month_survival dropped education and income at an effect of 0.0001), so keeping it departs from them.
   * **Effect on the task:** the mark is real but small. Re-run on the definition's own missing values: hiding every unknown except the structural ones leaves ROC AUC unchanged (0.9213 / 0.9210). Hiding only the newborn's measurements and anomalies costs +0.9% log loss (2.5 SDs of the base), which is the mark the note names. The conditional observed-to-expected ratio for day-0 deaths is 1.99 for the mother's education, 1.89 for cigarettes and 1.80 for the prior births.
   * **Consistency:** this is one of the late-values calls the curator keeps on the review page (the **across-datasets late-values item**); it departs from mic and 2_month_survival; keeps were onlinenewspopularity, medical_facility_operational_data and kumc (open). The fact offered to set this case apart: these gaps are the certificate's own at the birth, not filled by a late interview as in 2_month_survival[^leak10][^leak6].
   * **Panel:** the advocate keeps it with the note (the mark spans nearly every item, the cells cannot be located, the gaps are recorded at the birth) and concedes the departure; the critic accepts the keep only with that fact and the test written into the note and "no effect" confirmed under the declared metric, else option C.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep with the note (implemented) | the unknowns stay missing; the note gives the shares and the test | no measurable gain from the mark; no item lost | departs from mic and 2_month_survival; +0.9% log loss from the newborn's measurements and anomalies |
     | B | Blank or drop the items most marked | as 2_month_survival did, item by item | follows the precedent | many items affected; the cells cannot be located, so it hides real unknowns too |
     | C | Prediction point at the certificate's completion | the cohort alive at the report, a different task | the mark is no longer a leak | ROC AUC 0.861; a different actor and task |

   * **Recommendation:** A, if the curator accepts that gaps recorded at the birth set this case apart from 2_month_survival; otherwise B; C only if the curator wants the registration-time task (see issue 3, B). **Decision:** A, B or C?

   **Notes for the AI:** on A, add the distinguishing fact (gaps recorded at the birth, no late interview) to the note. On B, take the items with the highest conditional ratios first (mother's education, cigarettes, prior births) and re-run the experiment of the note. If issue 4 goes to log loss, re-measure A under log loss with several seeds first.

   [^leak10]: **LEAK-10** (Must): a feature holds only what existed at the prediction point; clause 2 covers missingness that encodes the outcome.
   [^leak6]: **LEAK-6** (Must): measure before acting; a slight optimism with a known cause can stay with a note, a confirmed leak goes even when small; late values that cannot be located row by row stay with a note when the traced part shows no gain.

3. **Confirm the use case narrowed to expected deaths at the birth; a second folder for the screen at registration?**

   * **Problem:**
     - The use case first named two actors: risk adjustment of hospitals' and counties' infant deaths by expected deaths, and a follow-up or home-visiting screen.
     - The screen (as in Florida) acts at registration, on infants still alive, and targets post-neonatal deaths, where this model scores only 0.81-0.83 ROC AUC.
     - The shipped rows fit only the risk adjustment at the birth, so the use case and the fit text are narrowed to it (implemented).
   * **Effect on the task:** none on the data; the narrowing makes calibration the clear context of the metric (issue 4).
   * **Consistency:** a second folder for another actor on the same rows is allowed when the actor is distinct[^use3].
   * **Panel:** the advocate and the critic both narrow the use case; a second folder only if the curator names the screen as a distinct actor.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Narrowed to expected deaths at the birth (implemented) | one folder, the risk-adjustment actor | the rows fit the actor; no new build | the screening use is not benchmarked |
     | B | A, and a second folder for the screen at registration | infants alive at registration, post-neonatal deaths | a distinct real actor | a new definition, build and review; a weaker signal |

   * **Recommendation:** A. **Decision:** A or B?

   **Notes for the AI:** on B, open a new record or a version folder whose rows are the infants alive at the report and whose target is a death after 28 days; the age at death (AGEDX) gives both.

   [^use3]: **USE-3** (Must): name the prediction point; a second folder follows the precedent of a distinct actor (precedent check D1).

4. **Keep ROC AUC, or score log loss?**

   * **Problem:**
     - Expected deaths are sums of the predicted probabilities, so the actor needs calibrated probabilities, which ROC AUC ignores.
     - LightGBM under-predicts the deaths by 13% to 16% at a ROC AUC of 0.913-0.917 (the panel's probe, before the changes).
   * **Effect on the task:** a model ranked first by ROC AUC can be badly calibrated; log loss would rank on both.
   * **Consistency:** the across-datasets item on log_loss from context for binary tasks covers this case, as it does sivep, nyc and uk_mot: with the use case narrowed to expected deaths (issue 3, A), the context names calibration. The precedent checker's fallback cases are backblaze and turkcell[^met8][^met11].
   * **Panel:** the critic and the domain practitioner want log loss once the use case is narrowed; the advocate and the precedent checker keep the fallback.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | ROC AUC (implemented) | the fallback for binary classification | consistent with backblaze and turkcell | ignores the calibration the actor sums |
     | B | Log loss | origin from the context: expected deaths | scores what the actor uses | coupled to issue 3; issue 2's keep carries +0.9% log loss and is re-measured first |

   * **Recommendation:** B if issue 3 stays A; A otherwise. **Decision:** A or B?

   **Notes for the AI:** on B, declare the metric from context with the reason (expected deaths are sums of probabilities), re-measure issue 2's experiment under log loss with three seeds, and re-run `dataset check`.

   [^met8]: **MET-8** (Should): when no threshold metric is fixed, score classification by a strictly proper scoring rule or a ranking metric; the fallback is `roc_auc` for binary tasks.
   [^met11]: **MET-11** (Must): every metric has one origin, and the notes name the original whenever the declared metric is not exactly it.

**Review panel:** ship after changes (mediator). Full panel: claim auditor, column auditor, split auditor, domain practitioner, blind reviewer, task gamer, precedent checker, advocate, critic, mediator; the rebuttal round was skipped: the advocate's and the critic's briefs agreed on every change, and their disagreements are issues 2 and 4. Claim audit: the co-twin in the prior-birth counts, the paternity acknowledgement and the post-birth anomaly diagnoses refuted "known at the birth", and the "label-free" birthweight imputation was refuted (all fixed). Split audit: the yearly temporal windows hold; no gap is right for a fixed one-year horizon. Task gamer: the only exploit above noise was the cyanotic heart disease (+0.0018, dropped). Blind review: would benchmark; asked for the per-year sampling fraction to be stated (done). Applied with no decision: co-twin counts blanked, cyanotic heart disease and paternity acknowledgement dropped, karyotype levels merged, 2017-2019 imputed birthweights blanked, the "plural delivery" interval code set missing, text fixes. Disputed and handed over: race (issue 1), the outcome-marked unknowns (issue 2), the use case (issue 3), the metric (issue 4).

<details><summary>Mediator: nchs_linked_birth_infant_death</summary>

```text
MEDIATOR REPORT: nchs_linked_birth_infant_death (folder nchs_linked_birth_infant_death_1m), 2026-11-09

JUDGMENT RECORD
Verdict: ship after changes.
Validity: SEL-2..16 hold. USE-1 holds (direct fit, expected-deaths actor). USE-3 holds only after the use case is narrowed (issue 3). LEAK-10 is triggered four times and fixed in the definition: co-twin prior-birth counts, cyanotic CHD, paternity_acknowledged, karyotype confirmed/pending. LEAK-13/LEAK-30 is triggered (2017-19 imputed birthweight of linked deaths) and fixed by blanking. LEAK-10 clause 2 (outcome-marked unknowns) is open, issue 2. SEL-1 (parents' race and ethnicity) is open, issue 1, and every reviewer recommends dropping it. SPLIT-1..22 hold; no gap is an application of SPLIT-10's fixed-horizon clause.
Value: TP-2/TP-4 pass, a real signal (tuned 0.920 ROC AUC, best single feature 0.835). Keep.
Quality: CLEAN-10 (code 000-003 "plural delivery" sentinel) to fix. Ages and cigarette counts: check the stored type (see change 9). Documentation fixes listed below.
Weighed: source +, size +, reviewer agreement +, gaming resistance + (largest exploit about 0.002).
For the curator: issue 1 race (protected grounds); issue 2 unknowns kept with a note against mic and 2_month_survival; issue 3 use-case scope; issue 4 metric.

CHANGES TO MAKE NOW (no decision needed)
1. Blank prior_births_now_dead and prior_births_now_living (PRIORDEAD, PRIORLIVE) when DPLURAL != 1 and SETORDER_R != 1, and add a LEAK-10 bullet. The rule is LEAK-10 Must with LEAK-6: a confirmed, located leak goes even when it is small. On plural-code rows a count of 1 means a 26.2% death rate, against 5.1% for multiples whose dead child came from an earlier pregnancy. Gain: +0.0005 / -0.0001.
2. Drop cyanotic_congenital_heart_disease (LEAK-10 Must). The worksheet gives "physician progress notes" as its source. Gamer exploit 1: +0.0018, about 5 times the noise, the only gain above noise.
3. Collapse the karyotype levels "confirmed" and "pending" (Down syndrome, suspected chromosomal disorder) into one "yes" level (LEAK-10). They come from genetic consults after the birth (35.6% vs 12.0% died). Cost: 0.0001.
4. Drop paternity_acknowledged (LEAK-10). It is signed in the hospital, after the birth. Note: the gamer's test (the ratio rises with gestation) reads it as social risk, not reverse causation. The drop rests on timing, not on a measured gain.
5. Blank the BWTIMP=1 birthweights for 2017-2019, and correct the definition text that calls the imputation "label-free" (LEAK-13, LEAK-30; claim F4 refuted the text). Cost: none (0.9213/0.9226).
6. Recode months_since_last_live_birth and months_since_last_other_outcome code 000-003 ("plural delivery") to missing, and plural-delivery code 3 to 0 (CLEAN-10, CLEAN-12).
7. Cite LEAK-25 instead of LEAK-22 for the 1.3% unlinked deaths counted as survivors (precedent D4).
8. Text fixes (EV-8, SPLIT-10 notes):
   - splits_comment: NCHS posts each cohort 23-29 months late (not "about two years"); report means over the 3 windows.
   - Seed spread is 0.004, not 0.001; restate the "no change" claims against it.
   - Document that the sampling fraction doubles in 2021 (about 6.7% to 13.7%, an artefact of the _1m budget).
   - Saravanou 2019 reports PR AUC and ROC AUC; fix the "where we looked" wording.
   - The prediction_point text must stop saying "anomalies seen at birth" in a way that covers the dropped items.
9. mother_age and the cigarette columns: both briefs ask for numbers. CLEAN-14 (mic precedent, 2026-11-01) keeps a count with a cut end as an ordered category, and _feature_types declares them ordinal. Check the container: if they ship as unordered text, make them ordered (the fix the rule asks for). Making them plain numbers departs from mic and is the curator's call. This is not a conflict to settle here.

ISSUES FOR THE CURATOR (ranked: validity first, Must first)
1. Parents' race and Hispanic origin (four columns) as inputs. Rule: SEL-1 Must, P1, Tensions row "a factor the actor may no longer use". This is one of the protected-grounds calls you asked to keep on the review page.
   - Effect: dropping them costs nothing (0.9148 vs 0.9149/0.9158 AUC; domain -0.0009 AUC, +0.2% log loss).
   - Advocate and critic both accept option B (drop). So do the builder, column auditor and domain practitioner.
   - Precedent D5: keeping them is consistent with the clinical keeps but departs from the batch's method (rais Title VI reasoning, 45 CFR 80.3, for a per-person service) with no stated reason.
   - Decision: drop (B, recommended by everyone) or keep with a stated reason.
2. Unknowns that mark early deaths, kept with a "Potential leak, kept on purpose" note. Rule: LEAK-10 clause 2 Must, LEAK-6. This is one of your late-filled-values calls.
   - Effect: the mark is real. Conditional O/E for day-0 deaths: 1.99 mother's education, 1.89 cigarettes, 1.80 prior births. Hiding every missing value moves nothing measurable: AUC 0.9171 vs 0.9149/0.9158 (within the 0.004 seed spread), log loss +1%.
   - Advocate: keep with the note, because the mark spans nearly every item, the cells cannot be located, and the gaps are the certificate's own at the birth (no late interview, unlike 2_month_survival). The advocate concedes the departure.
   - Critic: the departure needs these distinguishing facts and the test written into the note, and "no effect" confirmed under the declared metric. If that fails, use option B (cohort alive at the report, AUC 0.861).
   - Precedent D3: departs from mic and 2_month_survival (both removed the mark; 2_month_survival dropped edu and income at 0.0001 effect) with a reason that does not set this case apart. The keeps were onlinenewspopularity, medical_facility_operational_data and kumc (open).
   - What would settle it: whether "the gaps are recorded at birth, not filled late" is a fact that sets this case apart from 2_month_survival. If not, keep the precedent: blank or drop, or take option B.
3. Use case and actor. Rules: USE-3 Must, USE-5, PROV-7.
   - Effect: the follow-up/home-visiting screen (Florida) acts at registration, on infants still alive, and targets post-neonatal deaths, where this model scores 0.81-0.83. The shipped rows fit only expected-deaths risk adjustment at the birth.
   - Both briefs: narrow the use case and fit text to risk adjustment at the birth. Add the registration-time screen (B) as a second folder only if you name it as a distinct actor (precedent D1).
   - Decision: confirm the narrowing, and say whether B gets its own folder.
4. Metric: roc_auc fallback or log_loss. Rules: MET-1, MET-8, MET-9, MET-11.
   - Effect: expected deaths are sums of probabilities. LightGBM under-predicts deaths by 13-16% at AUC 0.913-0.917, which AUC ignores.
   - Critic and domain practitioner: log_loss, once the use case is narrowed (MET-11 then makes calibration the clear context).
   - Advocate and precedent D7: the fallback holds while two uses stand (backblaze, sivep, turkcell).
   - Coupled: this follows issue 3. If you pick log_loss, re-measure issue 2's keep under log_loss with several seeds (it carries +1%).

TASK GAMER'S EXPLOITS (mapped to rules)
1. Cyanotic CHD, +0.0018: LEAK-10. New (the definition calls the anomalies "at birth"). Fixed by change 2.
2. No gap, +0.0020 raw, +0.0004 at equal training size: SPLIT-10. Known (builder issue 4). The measured gain matches the builder's +0.001 with no order; not an issue.
3. Rebuilding mothers across years (later rows of data.parquet): LEAK-16..21, and only an artefact of the kit. New. The gain (r1 +0.0000, r2 +0.0006) is within noise and disappears when a harness passes only each split's rows. No fix needed; add a one-line note if you like.
4/5. Co-twin death in the prior-birth counts, 0.0000 / -0.0001: LEAK-10. New to the definition, raised by the column auditor. Fixed by change 1.
Flaw: imputed birthweight with the imputation flag dropped. LEAK-13/LEAK-30, against the existing "label-free" note. It cannot be measured in the kit. Fixed by change 5.

AGREED FACTS
- 25.9M births 2017-2023, 0.553% infant deaths.
- Temporal yearly windows 2021/2022/2023; no twin or sibling crosses the split; exact copies across the split 0.0%.
- Probes: linear 0.902, LightGBM 0.901, RF 0.888; honest tuned LightGBM 0.9199; seed spread 0.004.
- Each leak in changes 1-5 is confirmed by the source documents. Each costs at most 0.0018 to remove.
- No gap costs about 0.001, with no order between gaps of 0, 1 and 2 years.
- Race carries no measured value.
- The outcome mark in the unknowns is real but moves the score within noise.
- Neither side asks to exclude the dataset.

CONSISTENCY WITH PRECEDENT
- D1, D2a, D2b, D6 (lt_vehicle reading of SPLIT-10), D7 and D8 are consistent.
- D4: fix the citation (change 7).
- D3 departs from mic and 2_month_survival: issue 2. The fact offered to set it apart (gaps recorded at the birth, not filled late) is the curator's to accept.
- D5 departs from the batch's method for race: issue 1. Dropping the columns removes the departure.
- Change 9 is kept within CLEAN-14 / mic. Plain numbers would depart from that precedent and are the curator's call.
```

</details>

<details><summary>Claim audit: nchs_linked_birth_infant_death</summary>

```text
CLAIM AUDITOR REPORT: nchs_linked_birth_infant_death (folder nchs_linked_birth_infant_death_1m), 2026-11-09

Verdict: ship after changes. 22 claims hold. 5 are refuted or refuted in part: the prediction point (claim 11), the
imputation mechanism (claim 17), the missingness evidence (claim 29), the fallback metric's reason (claim 27) and the
fit text (claim 31). 4 are untested. None of the refutations changes a score on the declared metric: every fix below
costs at most the seed spread. Three kept items do hold values recorded after the birth (LEAK-10):
  (1) a later-born twin's prior-birth counts, which count its co-twin as living or dead at the time of the report;
  (2) paternity_acknowledged, which the certificate says is "signed in the hospital";
  (3) congenital anomalies "diagnosed prenatally or after delivery", including the karyotype's confirmed or pending
      status.
The 2017-2019 births file imputed birthweight for linked deaths only (LEAK-13).

Where the numbers come from (EV-8)
- Counts: the definition's prepared parquet (all 25,994,734 rows), user guides 18PE17CO to 24PE23CO, the NCHS FTP
  listing (fetched 2026-11-09), the 2003 standard certificate of live birth and the facility worksheet guide (both
  fetched from cdc.gov, text in work_claim_auditor/dl/).
- Container: rebuilt from the current dataset.py (to_container, 260 s, 20.8 GB).
- Experiments: the definition's own _clean output with raw items attached, a stratified 1M of 2017-2022 for training
  and 500k of 2023 for testing (the shape of split 0), LightGBM with the builder's settings (600 trees, 63 leaves,
  4 threads). Reference: base over 4 seeds, ROC AUC 0.9195 / 0.9203 / 0.9212 / 0.9216 (mean 0.9206, SD 0.0009) and
  log loss 0.01937 to 0.01953 (mean 0.01944, SD 0.00007).
- These are untuned probe numbers, not leaderboard numbers.

TABLE: claim | source | test | result | evidence | rule

1 | Seven combined period/cohort zips, each the cohort's births plus two numerator files | claims.md 1; download_description | FTP listing; the guide's file description | HOLDS | the FTP sizes equal the local files (2024PE2023CO 432,493,258 bytes); guide: "The numerator for the 2023 birth cohort linked file consists of deaths to infants born in 2023 ... whether the death occurred in 2023 or 2024" | PROV-1, PROV-8
2 | 2024PE2023CO posted 2026-01-22, 2018PE2017CO 2020-05-26; year = 2026 | claims.md 2; year | FTP listing; PROV-9 text | HOLDS | listing 1/22/2026 and 5/26/2020; PROV-9: "A source that grows over time (a public register ...) takes the year of the snapshot we pin". Note: 2017PE2016CO was re-posted 6/10/2026, so re-posting is real | PROV-9
3 | The 2024/2023 positions equal those of 2018/2017 to 2023/2022 | claims.md 3; BIRTH_ITEMS comment | 13 items grepped in the 18PE17CO, 21PE20CO and 24PE23CO layouts | HOLDS | BFACIL 32, MAR_P 119, RF_EHYPE 317, CO_SEQNUM 365-371, MTRAN 434, PAY 435, APGAR5 444-445, DPLURAL 454, BWTIMP 516, AB_NICU 519, CA_DOWN 552, ILIVE 568, FLGND 1346 in all three | PROV-13
4 | No registration; the NCHS data use restrictions apply | claims.md 4; license | restrictions page | HOLDS | "Use the data in this dataset for statistical reporting and analysis only"; no registration step; agreement is by use. A one-line note, never an issue | EV-4
5 | NCHS names no model, decision or metric | claims.md 5; notes | guide and page | HOLDS for NCHS | rates with confidence intervals only. A third-party paper exists: see 27 | MET-1
6 | U.S. residents (RESTATUS 1-3); 58,268 foreign-resident births dropped; 25,936,466 remain | claims.md 6; _clean step 1 | counted | HOLDS | 58,268 and 25,936,466 exactly; the guide's SAS code: "IF RESTATUS < 4" | LEAK-22
7 | 143,474 deaths, 0.553%; 0.535-0.575% by cohort; 2021-2023 0.545/0.553/0.549% | claims.md 7 | counted by cohort | HOLDS | 2017 0.5749%, 2018 0.5630%, 2019 0.5507%, 2020 0.5354%, 2021 0.5449%, 2022 0.5526%, 2023 0.5490% | USE-5
8 | The cohort sequence number is filled exactly on the linked births | claims.md 8 | CO_SEQNUM != "" against AGEDX on all rows | HOLDS | equal on all 25.9M rows; 2023: 19,772 filled = 19,772 deaths before the residence filter (19,743 after) | LEAK-10 (dropped)
9 | 2017 births file: six-digit sequence; deaths file: seven; 19,542 of 22,197 fail unpadded; both padded to seven | claims.md 9; _zero_pad | builder's raw extractions joined both ways | HOLDS | births 19,542 six-digit and 2,655 seven-digit; deaths 22,197 seven-digit; unmatched before padding 19,542, after 0; no duplicate keys; 2018 and 2023 need no padding. The target reads only whether a birth is linked, so a wrong pairing could not change it | PROV-13
10 | Unlinked deaths (260 of 2023, 1.3%) count as survivors | claims.md 10; task_summary.predicted ("about 1.3%") | the guides of all seven cohorts | HOLDS for 2023; WORDING | 2017 95 (0.4%), 2018 139 (0.6%), 2019 156 (0.7%), 2020 143 (0.7%), 2021 222 (1.1%), 2022 282 (1.4%), 2023 260 (1.3%). The label noise triples toward the test windows, about 0.005% of births | LEAK-25 (a note)
11 | Prediction point: the birth, after the 5-minute Apgar; features are the certificate items known then; "the congenital anomalies seen at birth" | claims.md 11; curation_comments; task_summary.known | the certificate and worksheet wording; counts by age at death | REFUTED IN PART | three kept items are recorded after the birth: F1, F2, F3 below | LEAK-10, USE-3
12 | Dropped as after the birth: AB_*, ITRAN, ILIVE, BFED, APGAR10, MM_MTR/UHYST/AICU | claims.md 12; AFTER_BIRTH | code read | HOLDS (list incomplete: see 11) | all 13 are in AFTER_BIRTH and dropped in step 6 | LEAK-10
13 | ILIVE = N for 7,566 of 19,743 deaths of 2023 | claims.md 13 | counted | HOLDS | 7,566 of 19,743; all years: N for 90.3% of deaths under 1 h, 1.3% of deaths at 28+ days | LEAK-10
14 | APGAR10 unknown for 498 of 2,577 first-hour deaths of 2023 vs 0.45% of survivors; 88 when Apgar5 >= 7 | claims.md 14 | counted | HOLDS | 498 of 2,577; survivors 0.45%; APGAR10 = 88 on all 25,283,798 births with Apgar5 7-10 | LEAK-10
15 | Post-birth items lift ROC AUC 0.916 -> 0.925; ILIVE alone -> 0.919 | claims.md 15 | builder's json read; not re-run | UNTESTED (numbers as filed) | experiments_post_missing.json: 0.92476, +ILIVE 0.91893 | -
16 | CO_SEQNUM, CO_YOD, FLGND, AGEDX, AGER5X dropped as the target and its parts | claims.md 16; DEATH_LINK | code read; feature list of the rebuilt container | HOLDS | none of them among the 83 features | LEAK-10
17 | Imputation flags dropped, imputed values kept; 42% of 1,967 imputed births of 2023 died; flags add no AUC; checklist P4: the hot deck is "label-free" | claims.md 17; notes; builder_report P4 | BWTIMP by cohort; guide; values blanked | NUMBERS HOLD; "LABEL-FREE" REFUTED | F4 below | LEAK-13, LEAK-30
18 | Reporting flags: eclampsia/drugs/ART 0 for 57k-150k a year in 2017-2021; detailed payment 26-43%; birth place kept where flagged (California) | claims.md 18 | flags by year | HOLDS | F_RF_EHYPE 0: 138,045 / 137,420 / 137,488 / 134,393 / 57,185 / 0 / 0; F_RF_DRG 150,161 in 2017; F_PAY 0: 25.6-43.1%; F_MAR_P 0 = DMAR blank within 1,200; "home, unknown if intended" among the DMAR-blank births 3,091-3,591 a year in 2017-2020, 90-439 after | PROV-13, CLEAN-10
19 | BMI and weight gain derived from kept items | claims.md 19 | builder's explore3 log read; not re-run | UNTESTED by me | log: 99th percentile of the BMI difference 0.0497; weight gain matches in 97.9% of 2023 | CLEAN
20 | The two gestation estimates differ on 34% of 2023 | claims.md 20 | counted | HOLDS | 33.84% | CLEAN
21 | PRECARE 00 = PREVIS 00; 888 = no earlier birth; set order 9 = singletons (195 plural births without an order) | claims.md 21 | counted | HOLDS (888 not tested) | 00 coincide on all 496,722 births of 2017-2023; 186 + 6 + 3 = 195 plural births with set order 9. NOT SAID: ILLB_R/ILOO_R 000-003 is the code "Plural delivery" (guide), read here as 0-3 months (the blind reviewer found it too; it ties to F1) | CLEAN-10
22 | Plurality 5 of 2017-2019 (49, 10, 36) merges into "quadruplet or higher" | claims.md 22; CODE_LABELS | counted | HOLDS | 49, 10, 36; code 5 absent from 2020 on | CLEAN-12
23 | Ordered items; capped measures stay numbers | claims.md 23 | not tested (P7; dtype probe run by the builder) | UNTESTED | - | CLEAN-14
24 | Yearly windows 2023/2022/2021, 500k test, 1M train of all earlier births back to 2017 (15.0M-22.3M, 58-86%) | claims.md 24; splits_comment | rebuilt container | HOLDS | 3 folds; train years 2017-2022 / 2017-2021 / 2017-2020; no overlap; test positives 2,745 / 2,763 / 2,724; 15.01M and 22.34M earlier births | SPLIT-1, SPLIT-11, SPLIT-14
25 | No gap: at equal size the newest cohort adds no ROC AUC, a little log loss | claims.md 25; splits_comment | replication: 150k births of one year (2 seeds) tested on the 2023 500k | HOLDS | AUC 2022 0.8894/0.8901, 2021 0.8921/0.8899, 2020 0.8969/0.8935; log loss 0.0301/0.0299, 0.0297/0.0300, 0.0309/0.0311. The labels are final at release and the horizon is fixed (overfit small-n models, EV-8) | SPLIT-9, SPLIT-10
26 | NCHS releases a cohort about two years later | claims.md 26 | FTP dates | HOLDS | 2022 cohort 12/11/2024; 2023 cohort 1/22/2026 | SPLIT-12
27 | Metric: fallback ROC AUC; reason: "no competition or paper set a task on these files" | claims.md 27; metric.reason | the source again, a search for papers, MET-2 on the container | FALLBACK HOLDS; REASON REFUTED IN PART | F6 below. MET-2: the per-row unit exists and no scoring column is needed; constant and random dummies score 0.500 / 0.497-0.508 on each fold; 2,724-2,763 positives per test fold; same target, classes and 0.55% balance as the use case | MET-1, MET-2, MET-5, MET-6, MET-8, MET-9
28 | Race and Hispanic origin of both parents add nothing (0.9148 vs 0.9149/0.9158) | claims.md 28; notes | drop the 4 columns, 2 seeds | HOLDS | 0.9195/0.9214 vs base 0.9195-0.9216; log loss 0.01942/0.01941 vs 0.01944 mean. Law: see F7 | SEL-1
29 | Missingness kept: hiding every missing value but the father's gives 0.9171 vs 0.9149/0.9158, log loss 0.0192 vs 0.0190 | claims.md 29; notes "Potential leak, kept on purpose" | the builder's typed(); re-run on the definition's NaNs | CONCLUSION HOLDS; EVIDENCE REFUTED | F5 below | LEAK-6, LEAK-10, EV-8
30 | Single features: birthweight 0.834, gestation 0.834, Apgar5 0.835; without Apgar5 0.890 | claims.md 30 | builder's json read; not re-run | UNTESTED (numbers as filed) | experiments_base_single_gap / apgar json match | TP-4
31 | fit = direct; gaps named: no geography, the early deaths' less complete record | claims.md 31; fit_reason | F1-F3 | REFUTED IN PART | the co-twin counts and the paternity item are further outcome marks the text does not name | USE-1, USE-8
I1 (implied) | No row is a copy across the split | builder probe 5 | not re-run | UNTESTED by me | builder: 0.0% of 1.5M test rows; twins share a birth year, so they stay in one window | LEAK-16
I2 (implied) | The target is the real-world target | task_summary | 10, 7, guide | HOLDS with the note of 10 | a death within a year, final at release (both numerator files read) | USE-5, LEAK-24

FINDINGS, refuted and untested, ranked (validity first, then Must, then effect)

F1. [P4, LEAK-10 Must; REFUTES 11, 31] A later-born member of a plural delivery counts its co-twin among its "previous live births now living / now dead", as of the time of the report.
  Evidence (proof of the mechanism, all 2017-2023 twins):
  - Second-born twins average 1.97 previous live births against 1.21 for first-born twins. 90.8% of them have at
    least one, against 62.1%.
  - Their birth interval is the code 003 "Plural delivery" for 310,026 of them.
  - prior_births_now_dead > 0 by own outcome, second-born against first-born twins:
      died on day 0          31.5% vs 5.0%
      died on days 1-27      11.7% vs 2.5%
      survived                1.5% vs 1.3%
  - Death share given prior_births_now_dead > 0: second-born 22.7% against first-born 5.9%; at 20-27 weeks 67.8%
    against 45.9%.
  So the co-twin's death after the birth (correlated with this twin's own death) is in this twin's features.
  Gain (circumstantial): blanking both counts on the later-born rows (6,131 test rows, 118 deaths):
  - overall ROC AUC 0.9204 / 0.9222 / 0.9213 against base 0.9216 / 0.9203 / 0.9195;
  - later-born rows: -0.0069, -0.0042, +0.0051;
  - plural rows' log loss: +0.0003, +0.0008, -0.0009.
  No gain is measurable with 118 deaths, but a value recorded after the prediction point goes whatever it scores
  (EV-2). What it changes: the "features known at the birth" claim; the fit text.
  Mildest remedy (LEAK-7): where months_since_last_live_birth is the code 000-003 (the last live birth is in this
  delivery), set prior_births_now_dead and prior_births_now_living to missing, or replace them with their sum
  (the total of previous live births, which the co-twin's survival does not move). Set the 000-003 code itself to
  missing; plurality and set order carry it. A note gives the counts above.

F2. [P4, LEAK-10 Must; REFUTES 11] paternity_acknowledged is recorded after the birth. Certificate item 15 reads "IF NO,
  HAS PATERNITY ACKNOWLEDGEMENT BEEN SIGNED IN THE HOSPITAL?", and the signature comes during the stay.
  Outcome association (circumstantial, EV-6, "maybe a leak"), share without an acknowledgement among unmarried mothers
  in reporting areas, 22-24 weeks:
      died on day 0          47.8%
      died on days 1-27      39.5%
      died at 28+ days       36.3%
      survived               35.4%
  Adjusted odds ratio against survivors (gestation band, mother's age, education, race, Hispanic origin, payment,
  plurality, nativity, WIC, year, visits, prior births): day 0 1.51, days 1-27 1.28, days 28+ 1.32. The post-neonatal
  deaths carry more social risk, yet the day-0 deaths show the larger excess. At term the excess is the same for all
  deaths (38-40% against 27%).
  Gain: none. Without it, ROC AUC 0.9214 / 0.9213 / 0.9208 and log loss 0.01937 / 0.01938 / 0.01952, against base
  mean 0.9206 / 0.01944.
  Mildest remedy: drop paternity_acknowledged (no cost).
  The father's items: for unmarried mothers their presence follows the acknowledgement (father's age unknown 96.9%
  without it, 1.2% with it). Hiding their missingness gained nothing (builder: 0.9148 against 0.9158), and dropping
  them with the acknowledgement costs 0.001 AUC (0.9192 / 0.9196). Keep them, with a sentence in the existing
  missingness note.

F3. [P4, LEAK-10 Must as written; "maybe a leak", EV-6; REFUTES "the congenital anomalies seen at birth" of 11] The
  anomalies are those "diagnosed prenatally or after delivery" (facility worksheet guide, item 37).
  - Sources: CCHD from "Physician progress notes"; Down syndrome from "Infant progress notes" and "Genetic consult";
    Down syndrome and chromosomal disorder carry "Karyotype confirmed" or "Karyotype pending".
  - CCHD is reported for 0.83% of deaths under 1 h, 1.47% at 1-23 h and 2.76% at 1-27 days. A diagnosis takes time
    after the birth.
  - Suspected chromosomal disorder: "confirmed" on 63% of the reports of day-0 deaths that carry it (761 of 1,213), against 27% of
    survivors'. The status is the one at the report.
  Gain:
  - Merging confirmed and pending into "Yes": no change (0.9209 / 0.9215; log loss 0.01942 / 0.01944).
  - Dropping CCHD, Down syndrome and chromosomal disorder costs 0.0015 AUC and 1.3% log loss (0.9182 / 0.9201;
    0.01970 / 0.01970). That is an upper bound on the post-birth part, since many are prenatal diagnoses.
  Mildest remedy: merge the karyotype status into "Yes" (LEAK-7, no cost). Write the prediction point as what it is
  ("the anomalies the certificate reports, diagnosed before or after delivery") with a Potential-leak note; or decide
  it with issue 2 (option B, at the certificate's completion, makes them legitimate).

F4. [P4, LEAK-13 Must, measured, no effect; REFUTES "label-free" in 17] The births file imputed birthweight for linked
  deaths only in 2017-2019, and mostly in 2020.
  BWTIMP = 1 by cohort (births, share that died):
      2017       764   100%
      2018       860   100%
      2019       947   100%
      2020     1,089   81.6%
      2021     2,146   39.8%
      2022     1,963   38.6%
      2023     1,967   42.1%
  The 18PE17CO guide gives "860 in the denominator file" for the 2018 file. Median gestation of the imputed rows:
  18-19 weeks in 2017-2020, 31-33 weeks from 2021. The notes' "42% of the 1,967 births of 2023" hides that the training
  cohorts' fills went to one class.
  Gain: blanking every imputed birthweight scores 0.9213 / 0.9226 (log loss 0.01941 / 0.01937). No change.
  Mildest remedy: blank BWTIMP = 1 values in all cohorts (harmonises the recording at no cost); or keep them and
  correct the note to give the by-cohort shares.
  The other imputations: IMP_SEX died 69% in 2017 and 27-37% from 2020; MAR_IMP covered 16,166 births in 2017 and
  1,877-3,078 after.

F5. [P4, LEAK-6/LEAK-10; the conclusion of 29 holds; its evidence is refuted] The builder's typed() hid only blanks and
  "U".
  - Kept as categories, so not hidden: the coded unknowns of the categorical items (education 9, Hispanic origin 9,
    cigarettes 99, presentation, route, attendant, payment 9, birth place 9, nativity 3, father's race 99). "Every
    missing value but the father's" was not hidden.
  - Re-run on the definition's NaNs, hiding all but the structural ones (set order, the birth intervals, care month,
    detailed payment, marital status, paternity, the flagged risk items, the father's items): ROC AUC 0.9213 /
    0.9210, log loss 0.01947 / 0.01963. No change on ROC AUC.
  - Hiding only the newborn's measurements and anomalies: ROC AUC 0.9188 / 0.9203, log loss 0.01961 / 0.01963,
    which is +0.9% (2.5 SD of the base). This is the small outcome mark the note names.
  Mildest remedy: replace the note's numbers with these. "Revisit if log loss is reported" stays true. A confirmed
  mark that small is LEAK-6's "a confirmed leak goes even when small" against its "slight optimism with a known cause
  can stay with a note". That is issue 3's call, now with correct numbers.

F6. [P6, MET-1 Must on where we looked; the fallback holds] The reason says "no competition or paper set a task on
  these files". The record itself lists "many infant-death models on these files (not read)".
  - One found and read: Saravanou, Noelke, Huntington, Acevedo-Garcia, Gunopulos 2019, "Infant Mortality Prediction
    using Birth Certificate Data" (arXiv:1907.08968). It uses NCHS linked birth certificates of 2000-2002 and features
    including the abnormal conditions of the newborn.
  - Sec. 4.2: "We choose to evaluate our models using Precision-Recall (for the NotSurvival class) and Area Under the
    Curve (AUC)". It tunes "to maximize recall for the minority class".
  - Several metrics, and no threshold fixed: the fallback stands (MET-5, MET-6).
  Mildest remedy: one sentence in the reason naming it and why it gives no unique metric.

F7. [P1, SEL-1 Must, a weighing call; 28 holds] Does a law bar race for a neonatal risk decision? No U.S. law names an
  infant-mortality risk score. For the use case's follow-up decision on a family, the actor's law does constrain race:
  - Title VI (42 U.S.C. 2000d) bars race discrimination in federally funded programs, such as federally funded home
    visiting.
  - A state health department's race-weighted allocation is a racial classification under the Equal Protection
    Clause.
  - ACA section 1557's rule, 45 CFR 92.210 (2024), bars discrimination "through the use of patient care decision
    support tools" and requires reasonable efforts to identify tools that use race as an input and to mitigate the
    risk. Its status in 2026 is unverified.
  Nothing bars race in an expected-deaths model for comparing hospitals, which is no decision on a person.
  Under the batch's extension of the "factor the actor may no longer use" row (rais: any decision on a person whose
  factor the actor's own law constrains), the follow-up framing drops race. Measured cost: nil (0.9195 / 0.9214).
  The builder's recommendation B (drop the 4 columns) agrees. The curator's call.

F8. [P5, note] The unlinked share differs by cohort, 0.4% (2017) to 1.4% (2022), against the summary's "about 1.3%".
  Remedy: "0.4% to 1.4% by cohort (1.3% in 2023)" in `predicted` and in the notes.

F9. [P7, CLEAN-10] ILLB_R and ILOO_R 000-003 are the code "Plural delivery", read as 0-3 months (the blind reviewer
  found it too). Fixed with F1.

UNTESTED, low rank: 15 and 30 (the builder's experiment numbers, read from the json, not re-run); 19 (BMI and weight
gain, the builder's log); 23 (ordinal typing); the "888 = no earlier birth" part of 21; I1 (copies across the split,
the builder's probe 5).

FILES (scratch, all in the run folder)
- Scripts and logs: raw_checks.py/.log, raw_checks2.py/.log, paternity_check.py/.log, cotwin_check.py/.log,
  cotwin_check2.log, flags_by_year.log.
- Container: build_container.py/.log, container_summary.json (MET-2 per fold).
- Experiments: prep_frame.py, experiments.py, experiments2.py; results in experiments_A-D.log/.json and
  experiments_cotwin.log/.json.
- Sources: dl/ (the certificate, the worksheet guide and the paper, with their text).
```

</details>

<details><summary>Column audit: nchs_linked_birth_infant_death</summary>

```text
COLUMN AUDITOR REPORT: nchs_linked_birth_infant_death (folder nchs_linked_birth_infant_death_1m), 2026-11-09

Verdict: ship after changes. One confirmed leak to fix (a co-twin's death recorded in the later-born twin's prior-birth
counts). Two weaker timing questions for the curator. Three cheap cleaning fixes. The builder's other calls hold
column by column: the post-birth drops, the imputation, the reporting flags and the missing codes.

Validity: SEL-1 open (race and Hispanic origin, issue 1, a weighing call). LEAK-10 triggered for two counts, located
and fixable: `prior_births_now_dead` and `prior_births_now_living` of later-born multiples. LEAK-10/LEAK-6 confirmed
by a conditional test for the unknowns of the mother's items. The builder keeps them with a note (issue 3); my
consistency check is below. LEAK-10, weak: the confirmed/pending status of the chromosomal items and the timing of
the anomaly block (a question). LEAK-25: the unlinked deaths are a small, noted mix.
Quality: CLEAN-10/12 (the interval code 3 for "plural delivery"), CLEAN-21 (the 2023 Hispanic-origin recode, no note
yet), CLEAN-5 (previous_cesarean is a near copy of previous_cesareans).

Sources read: dataset.py; builder_report.md; the 2024 period / 2023 cohort user guide (docs/24PE23CO_ug.txt, the
record layout and the notes on imputation, reporting flags and linkage); the NCHS facility-worksheet guide, items 9,
10 and 37 (cdc.gov/nchs/nvss/facility-worksheets-guide/09.htm, 10.htm, 37.htm); the 2003 standard certificate item
on paternity acknowledgement. Rules: principles.md, use_case.md, leak_checks.md, cleaning_features.md (worktree
df-large).
Data: the builder's cached raw 2023 cohort (work/joined_2023.parquet, work/births_2023.parquet: codes as published,
in file order). The cleaned 2017-2023 frame (work/clean.parquet; it predates `previous_cesarean`). The current
container frame (the run folder, 2.5M rows x 84) and the participant kit's splits.
Scripts and logs: the run folder (a_descriptive, b_conditional, c_imputed_flags, d_cotwin, dtype/).
Groups by age at death (AGER5X) used below: "first day" (under 24 hours), "day 1-27", "post-neonatal" (day 28-364).
Post-neonatal deaths happen after discharge, so their certificate was complete before the death. That makes them the
control for risk the covariates miss.

======================================================================================================================
A. PROBLEMS, IN RANK ORDER (principles.md: P1 first, then by strength, then by size)
======================================================================================================================

1. P1, SEL-1 (weigh; builder's issue 1). Race and Hispanic origin of both parents: `mother_race`,
   `mother_hispanic_origin`, `father_race`, `father_hispanic_origin`.
   Column facts: self-reported on the mother's worksheet, known at the birth. Codes are decoded correctly: MRACE15 is
   imputed when unknown and its flag is dropped; FRACE15 99 and HISP 9 are missing. Leaving the four out costs nothing
   measured (builder: ROC AUC 0.9148 without them, 0.9149/0.9158 with them). The mother's age and education are
   standard perinatal risk factors with no comparable concern: keep them.
   Remedy: the curator's weighing. The mildest change that removes the concern is to drop the four columns (the
   builder's B). Nothing in the columns argues against it.

2. P4, LEAK-10 (Must), confirmed, weak in score. The co-twin's death sits in the prior-birth counts of a later-born
   multiple. Columns: `prior_births_now_dead`, `prior_births_now_living`.
   Mechanism (codebook): the NCHS facility-worksheet guide, items 9 and 10, says "For multiple deliveries: Include all
   live-born infants before this infant in the pregnancy who are now dead" ("... still living" for item 9): "If the
   second born, include the first born". The status is "now", at the worksheet's completion, so it falls after this
   infant's birth. A 2nd-born twin's record therefore says whether the 1st-born twin has died since. The twins'
   outcomes are strongly tied.
   Evidence, raw 2023 cohort (residents). Two twins share one mother's history, so any difference between them is the
   co-twin.
   - prior_births_now_dead > 0: 2nd-born twins 1.83% (1,009 of 55,081) against 1st-born 1.36% (754 of 55,278).
     Triplets: 1st 1.8%, 2nd 2.7%, 3rd 3.2%.
   - Death share when > 0: 2nd-born 19.6% against 1st-born 5.4% (when 0: 1.7% and 1.9%).
   - Among first-day deaths: 28.1% of 2nd-born twins have a count > 0, against 5.1% of 1st-born twins.
   Shipped frame (2.5M rows): 2nd-born twins 1.94% > 0 (death share 20.3%) against 1st-born 1.33% (5.1%). About 260
   later-born twins a year carry the excess, roughly 150 of the year's ~19,700 deaths.
   Worth (LightGBM, 400 trees, the 3 shipped splits x 2 seeds, shipped against both counts blanked for set order 2nd
   or later, 40,556 rows of 2.5M):
   - ROC AUC +0.0005 (SD 0.0013).
   - ROC AUC on the later-born multiples +0.0009 (SD 0.0032, 174-193 deaths per window).
   - Log loss: shipped minus blanked +0.00004 (SD 0.00007), so the blanked frame is not worse.
   Neither the leak nor the fix moves the score measurably.
   Rule: a confirmed leak goes even when small (LEAK-6), and the cells can be located (LEAK-7, blank the located
   cells).
   Remedy (mildest, cheap): in `_clean`, set PRIORLIVE and PRIORDEAD missing where the birth is plural and its set
   order is not 1st. In codes: DPLURAL != "1" and SETORDER_R != "1", which also catches the plural births of unknown
   order. Add a "Dropped / blanked as recorded after the birth (LEAK-10)" bullet with these numbers. A variant that
   keeps the part known at the birth would ship their sum (prior live births, co-siblings included) for those rows
   only, but it would mix two meanings in one column. Blanking is cleaner.
   New issue for REVIEW.md: not among the builder's draft issues.

3. P4, LEAK-10 / LEAK-6 (Must), mechanism now confirmed by a conditional test. Unknown items mark early deaths. This is
   the builder's issue 3, kept with a note.
   Test (the kick/expresso conditional test, leak_checks.md Mechanisms table): for each item, a LightGBM fitted on
   800k survivors of 2023 predicts "unknown" from items known at the birth: OE gestation, birthweight, plurality, set
   order, sex, birth place, mother's age, race and Hispanic origin, nativity, residence, marital status, delivery
   route, attendant, payer, transfer, month, weekday and the two area flags. It is scored on 800k held-out survivors
   and on all deaths: observed / expected (O/E) by age at death.
     item unknown            survivors  first day  day 1-27  post-neonatal (control)
     mother's education         1.00      1.99       1.44      1.08
     cigarettes 1st trim.       1.01      1.89       1.61      1.18
     prior births living        1.25      1.80       2.23      0.95
     anomaly block (CA_ANEN U)  1.03      1.69       1.17      1.34
     WIC                        1.03      1.52       1.39      1.04
     mother's height            1.02      1.40       1.70      1.14
     pre-pregnancy weight       1.01      1.31       1.30      1.17
     prenatal care month        0.99      1.25       1.22      1.09
     5-minute Apgar             1.07      0.92       1.32      1.24   (the covariates explain it)
     father's age, education    1.00   1.12-1.16  1.14-1.17  1.23-1.25  (no excess over the control)
     paternity ack. "Yes"       1.00      0.90       0.92      0.89     (no excess; see 6)
   In absolute terms: the mother's education is unknown for 7.7% of first-day deaths against 3.9% expected, about 285
   of the 7,496 first-day deaths of 2023. For the items of the mother's worksheet, the excess over the control is
   therefore caused by the death, not by risk the covariates miss. The father's items, the paternity item and the
   Apgar do not carry it.
   Consistency check (principles.md): the closest precedents decided the other way. kick (WheelType) and expresso
   (REGION) dropped a named field once a conditional test showed this mechanism (LEAK-38's last clause; LEAK-10
   Mechanisms row); mic moved the prediction point earlier. What sets this case apart:
   - the mark runs through nearly every item, so dropping is no option;
   - the marked cells cannot be told from the other unknowns;
   - hiding every unknown moved ROC AUC by no more than seeds differ (builder: 0.9171 against 0.9149/0.9158; log loss
     +1%).
   That fits LEAK-10's second clause: "stay with a note only when the part that can be traced shows none". So A (keep
   with the note) is defensible.
   Remedy: keep the builder's A. Add the conditional test to the "Potential leak, kept on purpose" bullet, which now
   reads "less complete" without a test, and name the precedent. The curator decides with issue 2 (option B, the
   cohort alive at the report, removes it).

4. P4, LEAK-10 (weak; a question for the curator). The anomaly block is recorded until the certificate is completed,
   not "at the birth". Columns: `down_syndrome`, `suspected_chromosomal_disorder` (the confirmed/pending level), and
   `cyanotic_congenital_heart_disease` (weaker: `congenital_diaphragmatic_hernia`).
   Codebook: facility-worksheet guide item 37 defines the block as "Malformations of the newborn diagnosed prenatally
   or after delivery". CCHD comes from "Physician progress notes", the chromosomal items from "Infant progress notes"
   and a "Genetic consult". Down syndrome is to be checked as "Karyotype confirmed" or "Karyotype pending". The
   definition's prediction point says "the congenital anomalies seen at birth".
   Data (2023):
   - suspected_chromosomal_disorder: confirmed 528 births, 35.6% died; pending 1,092, 12.0% died. Among first-day
     deaths with the item, 66% are confirmed against 26% among survivors.
   - down_syndrome: confirmed 867 births, 9.6% died; pending 988, 4.5% died (80% confirmed among first-day deaths,
     45% among survivors).
   The confirmed level mixes a prenatal karyotype (known at the birth, likely behind most early deaths) with a
   postnatal result returned before the certificate was filed (after the birth). The two cannot be told apart.
   CCHD: "Yes" for 0.011% of survivors without NICU admission, 0.45% with it and 1.2% of transferred survivors, so it
   is often diagnosed during the stay.
   Size (2023): 1,855 births with Down syndrome (127 deaths) and 1,620 with a suspected chromosomal disorder (319
   deaths), together at most 2.3% of the deaths; 2,271 births with CCHD (15.9% died). Neither is measured on the score;
   both are too small to show within seed noise.
   Remedy (mildest): merge "confirmed" and "pending" into "Yes" (the diagnosis or suspicion stays, the lab status
   goes). Reword the prediction-point bullet to "the congenital anomalies diagnosed before the certificate is
   completed (most visible at birth or diagnosed prenatally)". Keep CCHD with a note. The curator's call. It belongs
   with issue 2: under option B every anomaly is known at the prediction point.

5. P4, LEAK-25 (Must), small and noted. Infant deaths NCHS could not link count as survivors: 260 of the 2023 cohort,
   1.3% of deaths; 250 in the 2024 period file, 1.2%. The guide's Table II gives linkage by state from 95.3% (Texas)
   and 96.4% (Nebraska) to 100%. The state is no feature, so the mix cannot be located. It mislabels about 1.3% of the
   positives, spread by state.
   Remedy: keep the note in `predicted`. Optionally add the by-state spread (Table II) to the target bullet.

6. P4, LEAK-10, tested: no leak. `paternity_acknowledged`, and through it the presence of the father's items for
   unmarried mothers. The 2003 certificate asks whether a paternity acknowledgement was signed in the hospital, so the
   value is created after the birth, before discharge. Without it the father's items are blank: father's age unknown
   for 96.5% of unmarried births with "No" against 1.2% with "Yes".
   Unconditionally, first-day deaths show "Yes" 54.3% against 74.0% of survivors. Conditionally, the deficit equals
   the post-neonatal control (O/E 0.90 against 0.89), so the death does not change the signing. No change needed. One
   clause in the notes ("signed in the hospital after the birth; no outcome mark beyond post-neonatal deaths") would
   pre-empt the question.

7. P7, CLEAN-10 / CLEAN-12 (Should). `months_since_last_live_birth` and `months_since_last_other_outcome` ship the
   code for "plural delivery" as 3 months. The guide reads "000-003 Plural delivery, 004-300 Months". Only 3 occurs
   (44,306 births of 2023, all plural). In the shipped frame 30,825 rows hold 3, 30,069 of them 2nd-born, against
   1,123 rows at 4-6 months. The true interval to a co-sibling is 0 months.
   Remedy (cheap): map 3 to 0 before `_numbers`, or set it missing (plurality and set order hold it). Note the open
   end at 300 (2023: 387 births at 300 against 11 at 299).

8. P7, CLEAN-21 (Should). `mother_hispanic_origin` and `father_hispanic_origin` change scale in the newest test window.
   The guide: "Starting with 2023, data for 'Central and South American' no longer include 'Latin American,' which has
   been moved to 'Other and unknown Hispanic'". Observed: mothers "other and unknown Hispanic" 3.41% (2022) to 3.71%
   (2023); 2019 shows a similar step (3.93% to 3.50%).
   Remedy: a note (the shift is small and cannot be undone per row). Merging the two levels for every year is the
   lossy alternative.

9. P7, CLEAN-5 (Should), a minor inconsistency. `previous_cesarean` is a near copy of `previous_cesareans`: "No"
   equals 0 on every birth, and "Yes" equals 1 or more except 495 births of 2023 whose count is unknown. The
   definition drops BMI and weight gain as derived, but keeps this pair. `payment_source` is likewise an exact recode
   of `payment_source_detail` where that is reported, but it is rightly kept for the 37% of rows where the detail is
   masked.
   Remedy: drop `previous_cesarean` (it loses "yes, count unknown" for about 500 births a year), or add a note that
   both stay.

10. P7, CLEAN-14 (note; no change). Height and the two weights are measurements piled at NCHS's limits:
    - pre-pregnancy weight 375 lb: 2,135 against 72 at 374; 75 lb: 430 against 58 at 76;
    - delivery weight 400 lb: 2,031 against 93 at 399; 100 lb: 1,874 against 311 at 101;
    - height 78 in: 671 against 374 at 77.
    The guide prints plain ranges ("075-375 Weight in pounds"), not "or more". CLEAN-14's cut-end rule names counts
    and bands, so numbers with the definition's note are fine. Trivial: 15 fathers aged 9-11 out of 25.9M are within
    the guide's 09-98 range and left alone.

Checked and fine (no action):
- Post-birth drops (ILIVE, ITRAN, AB_*, BFED, APGAR10, MM_MTR/UHYST/AICU) and the death link: right by the layout;
  none is left in the frame.
- The kept maternal morbidity items (perineal laceration, ruptured uterus) happen at the delivery. All labour and
  delivery items (induction, augmentation, steroids "received by the mother prior to delivery", antibiotics and
  chorioamnionitis during labour, epidural, presentation, route, trial of labour) and the mother's transfer precede
  or are the birth.
- Imputation. Does an imputed birthweight mark the outcome by its value? No. In the 2023 births file, 1,970 imputed
  weights (828 deaths, 42%) sit at the 61st percentile of their gestation x plurality x sex cell for deaths and the 51st for
  survivors. A low percentile ranks death at ROC AUC 0.412 among imputed rows, against 0.591 among the rest (0.460
  against 0.573 at 27 weeks or less). The donor value is a survivor-like weight that hides signal, the opposite of a
  leak. Its format is no fingerprint (divisible by 10: 49.5% against 54.6%). The previous-record donor cannot be
  rebuilt from the published file order (equal values for 17-28%), so NCHS imputed before the file was sorted. The
  route still shows through other unknowns (Apgar unknown 15.9% of imputed births against 3.3% of other deaths), which
  is item 3. The flags add nothing (builder). LEAK-30 is moot: a label-free, per-row donor fill of 0.05% of the cells.
- Reporting flags (2023): every flag used is 1 on every birth except F_MAR_P, which is 0 for 11.1% (California;
  deaths 8.0%, survivors 11.1%), and F_PAY, which is 0 for 36.7% (deaths 35.1%). The flags are by area, not by record,
  so the masks add no outcome mark beyond the area mix. The masking follows the guide's instruction. In F_PAY=0 areas
  PAY still holds 1/2/3/6/8 without Indian Health Service and TRICARE, which `payment_source` keeps.
- Missing codes and decodes match the layout. The ordinal orders match the guide (education 1-8, cigarettes 0-97 then
  "98 or more", age "10-12" to "50 and over", plurality, set order). `prenatal_care_start_month` 00 becomes missing
  losslessly: 00 equals prenatal_visits 0 on all 80,056 births of 2023. Plurality 5 (2017-2019, 95 births) merges
  into "quadruplet or higher" as the 2020 code reads.

======================================================================================================================
B. DTYPE PROBE
======================================================================================================================
I re-ran the probe on the current definition (dtype_probes.py nchs_linked_birth_infant_death_1m --no-fetch --out
the run folder). It flags 7 of 82 columns, the same as the builder's run of 11:24. Each flag answered:
- mother_race, father_race ("ordinal_like", "open_end"): triggered by the words "more than one race". This is a
  nominal group, not a cut end. No action.
- the four cigarettes columns ("open_end", "98 or more"): the guide's cut end. Shipped as ordered categories with
  the cut as a level of its own, as CLEAN-14 asks. Order checked: 0..97, then "98 or more". 99 (unknown) is missing.
- mother_age ("open_end", "50 and over" and "10-12"): the guide's cuts, ordered from "10-12" to "50 and over". The
  imputed ages stay (no unknown code).
The probe cannot see three things this audit found by meaning:
- code 3 = "plural delivery" in the two interval columns (item 7);
- the confirmed/pending level of the chromosomal items (item 4);
- the cap piles of the height and weights (item 10).
No count or measured quantity is typed categorical. No code is typed numeric: the codes with words are decoded and
the counts and measurements are numbers. The yes/no checkboxes ship as "No"/"Yes" categories. Ordinal orders match
the guide.

======================================================================================================================
C. COLUMN TABLE (83 inputs + target; column | meaning (user guide) | known at prediction? | dtype and cleaning | verdict
   | rule)
======================================================================================================================
birth_month | DOB_YY + DOB_MM, the first of the birth month (no day in the public file) | yes | datetime, time column | fine | CLEAN-14, SPLIT
birth_time_minutes | DOB_TT time of birth as minutes after midnight; 9999 missing | yes; unknown 0.37% of first-day deaths against 0.01% of survivors (item 3) | number 0-1439 (a cycle as a number) | fine | CLEAN-14
birth_weekday | DOB_WK, 1 Sunday to 7 Saturday | yes | number (a cycle shipped as numbers) | fine | CLEAN-14
birth_place | BFACIL, 7 places, 9 missing; where F_BFACIL=0 (2017-2020, California) home births are all "unknown if intended" | yes | category, words | fine (noted) | CLEAN-12, CLEAN-21 note
mother_age | MAGER single years, "10-12" and "50 and over" cut; imputed when missing, flag dropped | yes | ordered, 39 levels | fine (SEL-1: keep) | CLEAN-14
mother_nativity | MBSTATE_REC born in / outside the U.S.; 3 missing | yes | category | fine | CLEAN-10
residence_status | RESTATUS 1-3 (foreign residents left out as the cohort) | yes | category | fine | USE-7
mother_race | MRACE15, 15 groups; unknown imputed, flag dropped | yes | category; probe flag a false positive | fine; SEL-1 weigh (item 1) | SEL-1
mother_hispanic_origin | MHISP_R 0-5; 9 missing | yes | category; 2023 recode of "Latin American" | fine; note to add (item 8); SEL-1 | CLEAN-21, SEL-1
paternity_acknowledged | MAR_P: unmarried, acknowledgement signed in the hospital; X married; blank in California | created after the birth; tested, no outcome mark (item 6) | category | fine | LEAK-10 (tested)
marital_status | DMAR married / unmarried; blank in California; imputed, flag dropped | yes | category | fine | CLEAN-10
mother_education | MEDUC 1-8; 9 missing | yes; unknown marked by first-day death (O/E 1.99 against 1.08) | ordered, guide order | fine; item 3 | CLEAN-14, LEAK-6
father_age | FAGECOMB 09-98; 99 missing | yes; blank without a paternity acknowledgement; no outcome excess | number | fine | CLEAN-11 (trivial)
father_race | FRACE15; 99 missing | yes (as father_age) | category; probe false positive | fine; SEL-1 weigh | SEL-1
father_hispanic_origin | FHISP_R; 9 missing | yes (as father_age) | category; 2023 recode | fine; note; SEL-1 | CLEAN-21, SEL-1
father_education | FEDUC 1-8; 9 or blank missing | yes; no outcome excess (1.12 against 1.23) | ordered | fine | CLEAN-14
prior_births_now_living | PRIORLIVE, earlier live births still living; for multiples includes co-siblings born earlier | NO for later-born multiples (co-sibling's survival after the birth) | number | LEAK, confirmed, weak; blank for set order not 1st (item 2) | LEAK-10, LEAK-6, LEAK-7
prior_births_now_dead | PRIORDEAD, earlier live births now dead; co-siblings included ("If the second born, include the first born") | NO for later-born multiples | number | LEAK, confirmed (2nd twins >0 1.83% against 1.36%; death 19.6% against 5.4%); blank (item 2) | LEAK-10, LEAK-6, LEAK-7
prior_other_pregnancy_outcomes | PRIORTERM, terminations and fetal deaths 0-30 | yes (a stillborn co-twin is known at the delivery) | number | fine |
months_since_last_live_birth | ILLB_R months 004-300; 000-003 plural delivery; 888 and 999 missing | yes | number; code 3 = plural delivery shipped as 3 months; 300 an open end | cleaning: 3 -> 0 (item 7) | CLEAN-10, CLEAN-12
months_since_last_other_outcome | ILOO_R the same | yes | number; code 3 (478 births of 2023) | cleaning: 3 -> 0 (item 7) | CLEAN-10, CLEAN-12
prenatal_care_start_month | PRECARE 01-10; 00 (no care) and 99 missing | yes; unknown O/E 1.25 against 1.09 | number; 00 lossless through prenatal_visits = 0 | fine | CLEAN-10
prenatal_visits | PREVIS 00-98; 99 missing | yes | number | fine |
wic_food_assistance | WIC food during pregnancy Y/N; U missing | yes; unknown O/E 1.52 against 1.04 | category | fine; item 3 | CLEAN-14
cigarettes_before_pregnancy | CIG_0 daily, 00-97, 98 "98 or more"; 99 missing | yes | ordered (open end) | fine | CLEAN-14
cigarettes_first_trimester | CIG_1 | yes; unknown O/E 1.89 against 1.18 | ordered | fine; item 3 | CLEAN-14
cigarettes_second_trimester | CIG_2 | yes | ordered | fine | CLEAN-14
cigarettes_third_trimester | CIG_3; unknown for every birth at 26 weeks or less (structural) | yes | ordered | fine | CLEAN-14
mother_height_inches | MHTR 30-78; 99 missing | yes; unknown O/E 1.40 against 1.14 | number; piles at 30 and 78 | fine (noted) | CLEAN-14
prepregnancy_weight_pounds | PWGT_R 75-375; 999 missing | yes | number; piles at 75 and 375 | fine (noted) | CLEAN-14
delivery_weight_pounds | DWGT_R 100-400; 999 missing | yes (at delivery) | number; piles at 100 and 400 | fine (noted) | CLEAN-14
prepregnancy_diabetes | RF_PDIAB Y/N; U missing | yes | category | fine | CLEAN-14
gestational_diabetes | RF_GDIAB | yes | category | fine |
prepregnancy_hypertension | RF_PHYPE | yes | category | fine |
gestational_hypertension | RF_GHYPE | yes | category | fine |
eclampsia | RF_EHYPE; masked where not reported (one area, 2017-2021) | yes | category | fine | reporting flag
previous_preterm_birth | RF_PPB | yes | category | fine |
infertility_treatment | RF_INFT | yes | category | fine |
fertility_enhancing_drugs | RF_DRG Y/N, X no treatment; U missing | yes | category | fine |
assisted_reproductive_technology | RF_ART Y/N/X | yes | category | fine |
previous_cesarean | RF_CESAR Y/N | yes | category; near copy of previous_cesareans | minor (item 9) | CLEAN-5
previous_cesareans | RF_CESARN 00-30; 99 missing | yes | number | fine |
gonorrhea | IP_GON, present or treated during pregnancy | yes | category | fine |
syphilis | IP_SYPH | yes | category | fine |
chlamydia | IP_CHLAM | yes | category | fine |
hepatitis_b | IP_HEPB | yes | category | fine |
hepatitis_c | IP_HEPC | yes | category | fine |
external_cephalic_version_successful | OB_SUCC | yes | category | fine |
external_cephalic_version_failed | OB_FAIL | yes | category | fine |
labor_induced | LD_INDL | yes | category | fine |
labor_augmented | LD_AUGM | yes | category | fine |
steroids_for_fetal_lung_maturation | LD_STER, given to the mother before delivery | yes | category | fine |
antibiotics_during_labor | LD_ANTB | yes | category | fine |
chorioamnionitis | LD_CHOR, diagnosed during labour or temperature >= 38 C | yes | category | fine |
epidural_or_spinal_anesthesia | LD_ANES | yes | category | fine |
fetal_presentation | ME_PRES at birth; 9 missing | yes | category | fine |
delivery_route | ME_ROUT final route | yes | category | fine |
trial_of_labor | ME_TRIAL if cesarean; X vaginal | yes | category | fine |
perineal_laceration | MM_PLAC 3rd/4th degree | yes (at delivery) | category | fine |
ruptured_uterus | MM_RUPT | yes (labour or delivery) | category | fine |
birth_attendant | ATTEND | yes | category | fine |
mother_transferred_before_delivery | MTRAN | yes | category | fine |
payment_source_detail | PAY, payer of this delivery; masked where F_PAY=0 (37%) | yes | category | fine | reporting flag
payment_source | PAY_REC 4-level recode | yes | category; exact recode where PAY is reported | fine (kept for masked areas) | CLEAN-5 (justified)
apgar_score_5_minutes | APGAR5 0-10; 99 missing | yes (defines the prediction point) | number (score) | fine | CLEAN-14
plurality | DPLURAL; 4 and 5 merged for 2017-2019 | yes | ordered | fine | CLEAN-21
set_order | SETORDER_R 1-4, "5th to 16th"; 9 (singleton or unknown) missing | yes | ordered | fine | CLEAN-14
infant_sex | SEX M/F; imputed when unknown, flag dropped | yes | category | fine |
gestation_weeks_combined | COMBGEST 17-47 (LMP where valid, else OE; imputed) | yes | number | fine |
gestation_weeks_obstetric_estimate | OEGEST_COMB 17-47, NCHS standard | yes | number | fine |
birthweight_grams | BRTHWGT 227-8165; hot-deck imputed when missing and gestation known; 9999 missing | yes; the imputed value marks nothing (AUC 0.412) | number | fine | LEAK-30, LEAK-39 (checked)
anencephaly | CA_ANEN, diagnosed prenatally or after delivery | yes (visible) | category | fine | LEAK-10
spina_bifida | CA_MNSB | yes (visible) | category | fine |
cyanotic_congenital_heart_disease | CA_CCHD, from physician progress notes | partly after the birth (diagnosed in the stay) | category | question (item 4) | LEAK-10 (weak)
congenital_diaphragmatic_hernia | CA_CDH | mostly at birth or prenatal | category | fine (note) | LEAK-10 (weak)
omphalocele | CA_OMPH | yes (visible) | category | fine |
gastroschisis | CA_GAST | yes (visible) | category | fine |
limb_reduction_defect | CA_LIMB | yes | category | fine |
cleft_lip | CA_CLEFT | yes | category | fine |
cleft_palate_alone | CA_CLPAL | yes | category | fine |
down_syndrome | CA_DOWN: karyotype confirmed / pending / No; U missing | suspicion yes; confirmed/pending is a lab status at filing | category, 3 levels | question: merge C+P (item 4) | LEAK-10 (weak)
suspected_chromosomal_disorder | CA_DISOR, the same | as down_syndrome | category | question: merge C+P (item 4) | LEAK-10 (weak)
hypospadias | CA_HYPO | yes | category | fine |
infant_death (target) | a death certificate linked to the birth, age under one year (both numerator files) | outcome | category No / Yes | fine; unlinked deaths (1.3%) as No, noted (item 5) | USE-5, LEAK-25, CLEAN-25
```

</details>

<details><summary>Split audit: nchs_linked_birth_infant_death</summary>

```text
SPLIT AUDITOR REPORT: nchs_linked_birth_infant_death_1m (record nchs_linked_birth_infant_death), 2026-11-09

Verdict: RIGHT WITH NOTES. The temporal split by birth year fits the use case, a risk estimate made at the birth. The
windows, the sampling and the training history check out against the data. The no-gap choice applies SPLIT-10's
fixed-horizon clause and is not an exception. Measured over three windows, it makes the task easier by about
0.001 ROC AUC compared with a 1- or 2-year gap, the same for both learners, and the learners' order does not change.
COVID shows up in the history as drift and does not break it. No twins or siblings link the two sides. Two sentences
in the splits_comment should be made more exact (finding 1).

Judgment record
  Validity: SPLIT-1/SPLIT-3 hold (temporal; the newborn is always a new entity, USE-10); SPLIT-9 holds (no shortcut:
  no family link across the cutoff); SPLIT-10 applied under its fixed-horizon clause (gap 0, cost measured, below);
  SPLIT-11, SPLIT-12, SPLIT-14 hold; SPLIT-13 checked (twins never cross, siblings unlinkable); SPLIT-20 checked
  (COVID: drift, no break); SPLIT-21 respected (nothing below was chosen from a score).
  For the curator: no decision needed. Notes only (finding 1, optionally 2 and 3).

Inputs used (read-only): dataset.py and the builder's report; the participant-kit copy of the shipped frame and splits
(panel/participant_kit/{data,splits}.parquet: 2.5M rows, 3 windows); the builder's cleaned full frame
(work/clean.parquet: 25,936,466 births 2017-2023, built by an earlier _clean, without `previous_cesarean`); the
NCHS FTP listing of the period/cohort files (server dates). Scripts and logs: the run folder
(a1_structure, a2_experiments, a3_twins_siblings, a3b_twins, a4_year_profile; a2_results.json).
Models: LightGBM 500 trees, lr 0.05, 63 leaves, reg_lambda 1, min_child_weight 1 (without the last two, LightGBM
collapses on this 0.55% base rate: 0.85-0.87 AUC, log loss above the constant's; see
a2_experiments_unstable_lgbm.log), 2 seeds; logistic regression (one-hot, median-filled numbers with missing flags),
1 seed. Train 1M rows, test 500k of the test year (the same test rows for every training variant of a window).

------------------------------------------------------------------------------------------------------------------------
FINDINGS (rank order: all are P4; Must before Should, then by effect)
------------------------------------------------------------------------------------------------------------------------

1. No gap between training and test years (P4; SPLIT-10 Should, applied under its fixed-horizon clause; SPLIT-9
   Must checked). Keep it and make the notes more exact.

   Facts.
   - The label has a fixed horizon: death before the first birthday. Every label is final in the release (the
     2024PE2023CO file holds the deaths of 2023 and 2024). So the newest training cohort is not selected by its
     outcome, and probe 13 shows the newest years' death share in band (z -0.1, -0.3).
   - The delay is real. On 1 January of a test year T, cohort T-1 has not finished its year of follow-up. That
     cohort is 16.4%, 19.6% and 24.1% of the train sides of 2023, 2022 and 2021.
   - The release lag is longer than "about two years". NCHS server dates for the cohort zips: 2019 cohort
     2022-05-05, 2020 cohort 2023-06-06, 2022 cohort 2024-12-11, 2023 cohort 2026-01-22. That is 23-29 months after
     the cohort year ends. On 1 January 2023 the newest public cohort was 2019 (2020 came in June). A public-file user
     at a window start therefore trains on cohorts up to T-3 or T-4, a gap of two or more years. A health department
     that links its own records has cohort T-2 complete at best, a gap of one year.
   - SPLIT-9: no shortcut. The public file has no family id, so no training label can reach a test row through its
     own entity. Twins and siblings are covered in finding 3.

   Measurement (a2_experiments.log). Training was expanding from 2017 and drawn uniformly at 1M rows. gap 0 = the
   shipped design (years <= T-1), gap 1 = years <= T-2, gap 2 = years <= T-3.
                     LightGBM ROC AUC, mean of 2 seeds        logistic regression ROC AUC
     test window      gap 0    gap 1    gap 2                 gap 0    gap 1    gap 2
     2023             0.9170   0.9166   0.9166                0.9128   0.9136   0.9121
     2022             0.9096   0.9080   0.9067                0.9045   0.9045   0.9038
     2021             0.9131   0.9114   0.9141                0.9068   0.9049   0.9047
     mean             0.9132   0.9120   0.9125                0.9080   0.9077   0.9069
   - Gap 0 minus a gap, averaged over the windows: LightGBM +0.0012 (gap 1) and +0.0008 (gap 2); logistic +0.0004
     and +0.0011.
   - Paired bootstrap SD of one window's difference (test rows only): 0.0011-0.0013. The per-window differences
     range from -0.0011 to +0.0028. The spread between two LightGBM seeds reaches 0.0031.
   - LightGBM leads logistic regression in all 9 window x gap cells (+0.003 to +0.009), so the learners' order does
     not depend on the gap.
   - This agrees with the builder's single-year test on 2023 (2022 alone 0.9137, 2020 alone 0.9151).

   Floor (SPLIT-14). A 1-year gap would leave the 2021 window training on 2017-2019 = 11.39M of 25.94M births =
   43.9%, below the floor. Adding the 2016 cohort (about 3.94M births, same combined format, zip on the server) would
   bring it to about 51%. A 2-year gap would leave the 2021 window on 2016-2018, about 39% even with 2016, and would
   need the 2014-2015 cohorts in the older format.

   Reading. This is the case the amended SPLIT-10 describes: a fixed horizon, final labels, no outcome selection, and
   the delay's gain stated at equal size. It is like lt_vehicle_loan_default_prediction (gap 0, an application).
   A gap would cost the floor or a new source file and buy about 0.001 AUC of realism.

   Mildest remedy: notes only, no re-split.
   (a) Replace the one-window, one-seed numbers in splits_comment with the three-window means above, or add them.
   (b) Correct "NCHS releases a cohort's file about two years later ... a health department linking its own records
       would not". Suggested text: NCHS posts a cohort 23-29 months after its year ends, so a public-file model at a
       window start has cohorts up to three or four years old. A health department linking its own records has the
       cohort before last complete and the last one only in part. Without a gap the benchmark scores about 0.001
       ROC AUC (LightGBM, three windows) above a one- or two-year gap, and the learners keep their order.

2. COVID-19 inside the history and the windows (P4; SPLIT-20 Should). Drift, no break. Keep it, with an optional
   note.

   Facts (a4_year_profile.log; full frame).
   - Births fell 3.6% in 2020 (3.61M).
   - The mean number of prenatal visits stepped down from 11.30 (2017-2019) to 11.00 (2020) and stayed at
     10.96-11.02. This is a lasting change, not a COVID-only dip.
   - Preterm births (under 37 weeks) rose from 10.09% to 10.48% in 2021.
   - Deaths per 1,000 births were 5.75, 5.63 and 5.51 in 2017-2019, 5.35 in 2020, then 5.45, 5.53 and 5.49.
   - Deaths per 1,000 term births rose to 2.175 in 2022 (2.01-2.11 in the other years).
   - A reporting change, not COVID: eclampsia is missing (not reported) for 3.7% of births in 2017-2021 and 0.2% from
     2022.

   Measurement.
   - E2: one model trained on 2017-2018 and scored on each later year, ROC AUC mean of 2 seeds: 2019 0.9153,
     2020 0.9170, 2021 0.9124, 2022 0.9085, 2023 0.9147. The COVID years are not the outliers. 2022 is the hard year
     under every training history (also under gap 0/1/2 above), so it is a property of the test year.
   - Calibration (predicted over observed mean) falls by about 6% from 2022 on in both seeds (seed 1: 1.00, 1.02,
     1.01, 0.94, 0.94). This matches the rise in term-birth mortality and shows in log loss, not in ROC AUC.
   - E3: on the 2023 test rows, a 1M history of 2017-2019 (before COVID) scores 0.9161 ROC AUC and 0.01967 log loss.
     A 1M history of 2020-2022 scores 0.9172 and 0.01934. The COVID-era years help a little, so dropping them from
     training is not called for.

   Reading. All three windows come after the COVID arrival, as the splits_comment says. The measurements show no
   window that is atypical in difficulty because of COVID. Each window is a whole year, so no season decides it. The
   history starts at 2017 because that is the first cohort read in the combined format (2016 is available but not
   needed); that is a format reason, not a score-based one, so SPLIT-21 is not touched.

   Remedy: none required. Optionally add to the COVID sentence: "a model fit on 2017-2018 scores 2020 and 2021 like
   2019 and 2023 (ROC AUC 0.915-0.917, 2021 0.912); 2022 is the hardest year (0.908)".

3. Twins and siblings across the split (P4; SPLIT-13 Should, SPLIT-9 Must). Nothing crosses. Keep it.
   - Twins share the birth month, and the cutoffs fall on 1 January. Only a delivery that straddles midnight on 31
     December can put co-twins on both sides.
   - Measured (a3b_twins.log). On a 12-item key of mother and pregnancy items (mother's age, race, Hispanic origin,
     education, height, both weights, father's age, prior live births, prenatal visits, plurality, obstetric
     gestation), the key finds 236, 241 and 260 same-month plural sets inside the 2023, 2022 and 2021 test windows.
     That is a recall of about 0.22 of the roughly 1,090 co-twin pairs expected in a 13.9% sample. 0 plural test
     births match a plural training birth in any window. On the 46-item profile, 11-17 test rows per window
     (0.002-0.003%) share a profile with a training row: none plural, none a death, training months spread over
     2017-2022, so chance matches.
   - Twins concentrate outcomes inside a test window: in 2023, 6 of the 12 matched sets with a death lost every
     member. This adds clustering inside a window, not leakage across the cutoff.
   - Siblings (a3_twins_siblings.log). 46.7%, 43.8% and 39.6% of the test births of 2023, 2022 and 2021 have their
     previous live birth in the training years. At the train sides' sampling rates (4.5%, 5.4%, 6.7%), 2.1-2.6% of
     test births could have that sibling's row in train.
   - The public file has no mother or family id, and the hidden-group probe finds 0.0% near copies. A model cannot
     tell which row is the sibling: a match on the mother's stable items hits 93-96% of test births at the sibling's
     month and at a decoy month alike.
   - A sibling's death before the test birth is already a feature of the test birth (prior_births_now_dead). A
     sibling death after the test birth needs an interval under 12 months (2.0% of test births) and a death at a
     later age than that interval, which is negligible.
   - Remedy: none. The README's claim "twins and siblings share one birth year, so one window" is right for twins and
     not for siblings. If it is repeated in the notes, say "co-twins share the birth month; siblings of other years
     cannot be linked in the public file".

------------------------------------------------------------------------------------------------------------------------
CHECKS THAT PASS (no action)
------------------------------------------------------------------------------------------------------------------------

- Regime (SPLIT-1, SPLIT-3, USE-10). The decision is made at each new birth, with a model fit on earlier cohorts:
  temporal. The newborn is always a new entity. The family history the actor knows is on the certificate (prior
  births now dead, previous preterm birth, months since the last birth), so it is a feature and not a group. With no
  family id there is nothing true to group on, and grouping would test nothing the use case asks for. IID would
  ignore that the model scores future cohorts.
- Time column. `birth_month` is the first day of the birth month (the public file has no day). It is built from
  DOB_YY and DOB_MM, the same year that defines the cohort file. The cutoffs fall on 1 January, and train max <
  test min in every window: 2022-12 < 2023-01, 2021-12 < 2022-01, 2020-12 < 2021-01.
- Windows (SPLIT-11, SPLIT-12, SPLIT-14, SPLIT-15, SPLIT-17). There are three yearly windows, newest first, with
  expanding train sides. The train sides hold 86.1%, 72.0% and 57.9% of all 25.94M births, above the floor. Yearly
  windows match NCHS's one cohort file per year and a yearly refit (the use case's cadence). Each window is a full
  calendar year, so it covers every season; test rows per month are 36,293-45,713. Shorter windows would only cut the
  same yearly pool into seasonal pieces, and nothing calls for longer ones.
- Sampling (version_comment). Every train side holds 1,000,000 rows and every test side 500,000, with no overlap
  inside a window.
  - The test sides are 13.6-13.9% of their year. Their death shares are 0.549%, 0.553% and 0.545%, equal to the full
    years' 0.549/0.553/0.545, and each holds 2,724-2,763 deaths.
  - The train death shares are 0.554-0.556%.
  - The newest training years keep their natural share. 2023 window: 2022 16.42% of train against 16.42% of the
    births of 2017-2022 (2017 17.29% against 17.26%). 2022 window: 2021 19.63% against 19.62%. 2021 window: 2020
    24.09% against 24.08%.
  - The train sides overlap across windows, as the one random order intends.
- splits_comment numbers verified: births per test year (3.60M, 3.67M, 3.66M), death shares, about 2,700 deaths,
  15.0M-22.3M training births, 58-86% of the rows.

------------------------------------------------------------------------------------------------------------------------
LIMITS
------------------------------------------------------------------------------------------------------------------------

- My experiments use the builder's cleaned frame from an earlier _clean (81 of the 82 features, without
  `previous_cesarean`) and my own 1M/500k draws, not the shipped rows. They measure differences between designs.
  They are not the shipped scores.
- LightGBM's calibration varies a lot between seeds (predicted over observed 0.76-1.01), so log loss comparisons
  between single fits are noisy. The gap and COVID findings rest on ROC AUC, the declared metric.
- I did not read the 2016 cohort's file. The floor arithmetic uses about 3.94M resident births for 2016 (the CDC
  final count is 3,945,875 births).
```

</details>

<details><summary>Domain practitioner: nchs_linked_birth_infant_death</summary>

```text
DOMAIN PRACTITIONER: nchs_linked_birth_infant_death (folder nchs_linked_birth_infant_death_1m), 2026-11-09
==================================================================================================================

The actor I play: the maternal and child health (MCH) epidemiologist of a state health department, who does two
things with this kind of model: (a) computes expected infant deaths to compare counties and birth hospitals, and (b) runs
the state's universal infant risk screen that refers newborns to Healthy Start or nurse home visiting. For the
clinical questions I asked the neonatologist of the perinatal quality collaborative. A neonatologist alone is a weak
actor here: at birth they predict death before discharge for extremely preterm infants with the NICHD tool, not death
in the first year for every birth.

VERDICT
- Fit: DIRECT for the expected-deaths half of the use case (USE-9), APPROXIMATE for the follow-up half. The data
  match "expected infant deaths for all live births, from the certificate items known at the birth, scored on the
  next year" in rows, inputs, label timing and split. The follow-up decision as it is actually made (Florida's universal
  infant screen, required by statute) differs on four counts: it is made at the certificate's registration, for
  infants alive then, uses NICU, ventilation and transfer items, and targets post-neonatal death. On those deaths
  the at-birth model ranks at 0.81-0.83, not 0.92. As written, the use case names both halves and the metric's reason
  names the ranking actor ("the actor ranks newborns by risk"), so the dataset and the metric point at different
  actors.
- Metric: PARTLY. The expected-deaths actor adds up probabilities, and ROC AUC does not score that: the builder's
  LightGBM setup predicts 13-16% fewer deaths than occur (4 seeds) at ROC AUC 0.913-0.917. For the follow-up actor,
  ROC AUC is dominated by deaths in the first hours, which no follow-up can reach. I would declare log_loss (MET-1,
  MET-8, MET-10), not average_precision (MET-9) and not precision_at_k (MET-7: no source fixes a k).
- Builder issue 1 (race): drop the four columns (B). This is a practice and ethics call (SEL-1), not a legal bar:
  US rules require identifying and mitigating race in clinical tools, but no rule forbids it. The cost really is
  within noise (3 seeds of a calibrated model: -0.0009 ROC AUC, +0.2% log loss, -0.001 on post-neonatal deaths).
- Builder issue 2 (prediction point): for follow-up I use B (at registration, infants alive then), for expected
  deaths A. I support C (two folders), or A with the use case narrowed to expected deaths and log_loss declared.
- Builder issue 3 (outcome-marked missingness): keep with the note (A) under ROC AUC. Re-measure under log_loss with a
  calibrated model and several seeds before switching the metric.
- Builder issue 4 (no gap): A. A state links its own deaths about a year after a cohort closes, and the measured cost
  is nil.
- Side finding for the panel: the builder's experiment model overfits. Its seed spread (0.004 ROC AUC) is wider than
  the 0.001 the builder cites, and wider than every effect in issues 1, 3 and 4. The decisions all read "no change"
  and still stand, but the cited spread should be corrected.

------------------------------------------------------------------------------------------------------------------
HOW THE DECISION IS MADE TODAY (what I learned)

- Florida Department of Health, Healthy Start universal infant risk screen (section 383.14(1)(b), F.S.: "A risk factor
  analysis ... shall also be conducted as part of the medical screening process upon the birth of a child and
  submitted to the department's Office of Vital Statistics"). The score is computed from the birth record, and 4+
  points is positive. In the 2012 screen, re-evaluated in June 2021 on the 2019 linked births and deaths:
  birthweight < 2000 g (4), one or more abnormal conditions (assisted ventilation, NICU admission, surfactant, RDS,
  seizure) (4), transferred within 24 h (4), tobacco (1), father's name not present (1), maternal race Black (1),
  prenatal visits < 2 (1), Medicaid (1), maternal age < 18 (1), unmarried (1).
  Target: "The infant risk screen is designed to identify infants who are at increased risk of postneonatal death"
  (28-364 days). The reason given: "Infant deaths that occur before the 28th day of life very often do not leave the
  hospital or would not have time to receive and benefit from additional health care services."
  Evaluation: sensitivity at the positive rate. 16.6% of infants screened positive and held 57.9% of post-neonatal
  deaths (2019; 5.4% of parents declined the screen).
  This is a deployed, statutory version of the follow-up half of our use case, and strong P3 evidence that the
  decision is real. But its prediction point is the certificate's registration, not the birth.
- Risk adjustment of neonatal outcomes (Vermont Oxford Network: gestational age, small for gestational age, multiple
  birth, 1-minute Apgar, vaginal delivery, birth location, birth defects; observed/expected from logistic models) and
  the NICHD extremely preterm tool (gestational age, birthweight, sex, plurality, antenatal steroids). Both use only
  items known at the birth, neither uses race, and both cover very preterm or NICU infants, not all births. County
  comparisons use the infant mortality rate. Local "perinatal periods of risk" analyses leave out births under 500 g
  (and in some reports under 24 weeks), because whether such a birth is registered as a live birth varies.

------------------------------------------------------------------------------------------------------------------
1. DO I HAVE EACH INPUT AT THE PREDICTION POINT (BIRTH, AFTER THE 5-MINUTE APGAR)?

Have, as shipped: the parents' demographics, prenatal care, smoking, height and weights, risk factors, infections,
labour and delivery, plurality, both gestation estimates, birthweight, 5-minute Apgar, the anomalies on the
certificate, birth month and time. One caveat: the "pending" levels of Down syndrome and chromosomal disorder, and
some cyanotic heart disease diagnoses, are known only days later, when the worksheet is completed. They are small
and I would keep them.

Would not have at birth (correctly dropped, LEAK-10 / USE-3): NICU admission, ventilation over 6 h, surfactant,
antibiotics, seizures, transfer, living at the report, breastfed at discharge, the 10-minute Apgar beyond the
5-minute mark, and the mother's ICU/transfusion/hysterectomy.

Missing although I would always have them:
- Assisted ventilation immediately after delivery (AB_AVEN1). The CDC facility-worksheet guide defines it as "manual
  breaths ... within the first several minutes from birth". At the 5-minute mark the delivery-room team knows it.
  It was dropped with the post-birth block. For a clinician predicting at birth it is an input. For hospital risk
  adjustment it is a process-of-care decision (whether to resuscitate a periviable infant) that risk adjusters keep
  out. Small; noted only.
- The 1-minute Apgar (VON uses it). Not on the US certificate, so not recoverable.
- State, county, birth hospital and its level of neonatal care, and whether the infant was born in a hospital with
  a NICU. Not in the public file. For expected deaths the unit is used to group, not as an input, so the gap is small
  there. For follow-up, local context matters somewhat. The fit_reason already names it.

At the follow-up actor's real point (registration, B), the certificate's NICU, ventilation and transfer items are
inputs: they carry 8 of the Florida screen's points (abnormal conditions 4, transfer 4), and the builder measured B at 0.861 -> 0.877 ROC AUC with them.

------------------------------------------------------------------------------------------------------------------
2. IS THE TARGET WHAT I ACT ON?

- Expected deaths: infant death (under 1 year) is the indicator states track and compare by county (Title V and
  Healthy People infant mortality rate), so yes for counties. For hospitals I would use neonatal or pre-discharge
  death and leave out births under 500 g or 22 weeks. The 1.3% unlinked deaths counted as survivors are small label
  noise, and correctly noted. I want a calibrated probability per birth, summed per county or hospital.
- Follow-up: a proxy. I act on deaths after discharge. Measured on 500k births of 2023 (2,705 deaths):
    age at death: under 1 h 13.3%, 1-23 h 25.5% (first day 38.8%), 1-6 d 13.7%, 7-27 d 12.9%, 28-364 d 34.6%.
    Births under 22 weeks or 500 g: 0.16% of births, 24.1% of deaths, 82% of them die. They are 53% of the
    first-day deaths.
    "Living at the report" = No for 92% of deaths under 1 h, 85% at 1-23 h, 36% at 1-6 d, 8% at 7-27 d, 1% after.
  I want a ranking (or a probability I threshold at my capacity) of post-discharge death among infants alive at
  registration.

------------------------------------------------------------------------------------------------------------------
3. DOES ONE ROW MATCH ONE DECISION, AND IS THE TEST DATA WHAT I FACE?

- One row is one birth, which is one referral decision (follow-up) or one term of a sum (expected deaths). Twins are
  separate rows, which is fine: each twin is referred and counted separately.
- Test = next year's births, train = earlier cohorts (refit yearly). That is my situation. A state links its own
  deaths roughly 12-15 months after a cohort closes, and NCHS about 2 years. The builder measured no cost at equal
  size (issue 4), and I agree with A.
- COVID years in train and test: noted, fine.

------------------------------------------------------------------------------------------------------------------
4. WOULD I USE THIS MODEL? (my measurements; train a random 1M of 2020-2022, test a random 500k of 2023)

Ranking by age at death. Builder's LightGBM setup, seed 0, ROC AUC of each death group against all survivors:
    under 1 h 0.999 | 1-23 h 0.992 | 1-6 d 0.959 | 7-27 d 0.902 | 28-364 d 0.818
    overall 0.917 | births of 22+ weeks and 500+ g only 0.891 | term births only 0.813 | alive at report 0.866
  The headline 0.92 is mostly the periviable first-day deaths, which gestation and weight rank trivially.

Calibration (what expected deaths needs):
    builder setup (600 trees, 63 leaves, min_child 100), seeds 0-3: ROC AUC 0.9167 / 0.9126 / 0.9140 / 0.9133,
      log loss 0.0190-0.0193, predicted/observed deaths 0.873 / 0.839 / 0.844 / 0.841.
      Risk deciles 4 to 9 of 10 are under-predicted by 31-52% (seed 0; the 8th: 0.0015 predicted against 0.0031
      observed); American Indian / Alaska Native births at 0.57.
    a smaller model (300 trees, 31 leaves, min_child 2000), seeds 0-2: ROC AUC 0.9217 / 0.9188 / 0.9190,
      log loss 0.01837 / 0.01838 / 0.01849, predicted/observed 1.010 / 0.984 / 0.987.
  ROC AUC cannot see a 16% shortfall in expected deaths, and a county comparison built on it would be wrong. Log
  loss sees it (0.0192 against 0.0184).

Follow-up (rank infants alive at the report, capture post-neonatal deaths):
    share of post-neonatal deaths in the top 5% / 10% / 16.6%: 0.37-0.41 / 0.49-0.53 / 0.61-0.64 across 7 fits.
    Florida's point screen captured 57.9% at 16.6% positive (2019 Florida, NICU and transfer items included). The
    at-birth items alone match it, which is encouraging but not like for like.

What would make me trust it: calibration by county or hospital and by group (observed/expected near 1); stable
ranking of post-neonatal deaths across years; drivers that make clinical sense (gestation, weight, Apgar, anomalies,
then social items).
What would make me distrust it: a headline AUC carried by periviable first-day deaths; expected deaths 13-16% short;
race among the drivers; "unknown Apgar" or "unknown birthweight" raising risk, since that rewards hospitals whose
certificates for infants who died are incomplete (issue 3; for a retrospective comparison these unknowns are in my
production data, so the issue is gaming, not availability).

------------------------------------------------------------------------------------------------------------------
5. DOES ROC AUC SCORE MY DECISION? PARTLY.

- Right: no source fixes a threshold, a cost or a k (NCHS reports rates only; MET-6, MET-7). Florida's 4 points
  (16.6%) is one state's capacity choice and would be invented for our data. The 0.55% base rate alone is no reason
  for average precision (MET-9). For pure ranking, ROC AUC is defensible.
- Wrong for expected deaths: that decision is a sum of probabilities per unit, and a strictly proper rule scores it
  (MET-1, MET-8). The builder's own experiments show the two metrics disagreeing on direction: adding the 10-minute
  Apgar went 0.9158 -> 0.9154 in ROC AUC but 0.01895 -> 0.01866 (-1.5%) in log loss; hiding missingness except the
  father's went +0.0014 in ROC AUC but +1.4% in log loss.
- Weak for follow-up: ROC AUC counts every death-survivor pair equally, and 38.8% of deaths are first-day deaths
  ranked near 0.99-0.999. A method gains little by ranking the post-neonatal deaths better.
- My choice: log_loss (MET-8, MET-10 diversity), with the reason "expected deaths are a sum of probabilities;
  calibration is part of the decision". If the curator keeps ROC AUC, then the use case should be the follow-up one,
  and B fits it better.
- If log_loss is declared, issue 3 needs re-measuring: the builder saw +1% log loss from hiding missingness,
  measured with the overfit setup on one seed.

------------------------------------------------------------------------------------------------------------------
GAPS BETWEEN THE DATASET AND THE REAL DECISION, RANKED BY HOW MUCH THEY CHANGE THE TASK

1. The use case has two actors with different prediction points and different metrics (USE-1, USE-3, MET-1).
   Follow-up as practised acts at registration on infants alive then, with NICU/transfer inputs and post-neonatal
   death as target. Expected deaths acts at birth on all births and needs calibration. A as built mirrors only the
   second, while ROC AUC scores the first.
2. The label mixes deaths no follow-up can act on: 38.8% first-day, 65% neonatal. ROC AUC 0.917 overall against
   0.818 on post-neonatal deaths and 0.813 on term births (USE-5).
3. The metric is blind to calibration, which the expected-deaths actor needs: 13-16% under-prediction at ROC AUC
   0.913-0.917 (MET-1, MET-8).
4. Periviable births (under 22 weeks or 500 g): 0.16% of births, 24.1% of deaths. Their registration as live births
   varies by state and hospital, and comparisons commonly leave them out (PPOR). This affects expected deaths; it is
   noted nowhere in the folder.
5. Race and Hispanic origin as inputs (issue 1): a fairness concern, and the cost of dropping them is within noise.
6. Outcome-marked missingness (issue 3): small, noted. For expected deaths it rewards incomplete records.
7. Inputs I would have but the file lacks: geography and level of care, the 1-minute Apgar, delivery-room
   ventilation (AB_AVEN1, droppable for risk adjustment). Small.
8. Training lag (issue 4): nil measured.

------------------------------------------------------------------------------------------------------------------
ISSUE 1 IN DETAIL: RACE AND HISPANIC ORIGIN

- The law (45 CFR 92.210, Section 1557 rule, compliance from 1 May 2025, text current per eCFR mirrors in early
  2026): "(b) A covered entity has an ongoing duty to make reasonable efforts to identify uses of patient care
  decision support tools ... that employ input variables or factors that measure race, color, national origin,
  sex, age, or disability" and "(c) ... make reasonable efforts to mitigate the risk of discrimination". This is a
  duty to identify and mitigate, not a ban. Hospitals and state health programs that receive HHS funds are covered.
  I found no 2025-2026 notice changing it, and I did not check enforcement. Title VI and the post-2023 scrutiny of
  race-conscious allocation make a race input in a public referral score legally exposed, but no US rule I found
  bars it outright. Unlike rais_employment_separation (Lei 9.029/1995 forbids it) and the EU insurance cases
  (Test-Achats), the tension row "a factor the actor may no longer use" applies here only by extension, as practice
  and SEL-1, not as a legal constraint.
- Practice: the MFMU VBAC calculator dropped race and ethnicity in 2021 with equal discrimination (reported ROC AUC
  0.74 to 0.75). The NICHD extremely preterm tool and VON's risk adjustment use no race. Florida's screen still gave
  "maternal race Black" 1 point in its 2021 review. So real US actors have used it, and the trend is away from it.
- For expected deaths, adjusting for race hides disparities between counties and hospitals, which is what a
  quality comparison is meant to show. That is a second reason to leave it out.
- Measured (my runs, paired, same train and test):
    smaller model, seeds 0/1/2: ROC AUC 0.9217->0.9190, 0.9188->0.9188, 0.9190->0.9191 (mean -0.0009);
      log loss +0.35%, +0.26%, -0.02%; post-neonatal ROC AUC -0.0054, -0.0004, +0.0022;
      post-neonatal capture in the top 10% -0.008, -0.003, +0.002.
    builder setup, seeds 0-3: ROC AUC -0.0045, +0.0012, -0.0006, +0.0002 (seed spread of the base 0.004).
  Within noise. What changes is who is flagged (smaller model, seed 0, top 10% of infants alive at the report):
  non-Hispanic Black 23.7% -> 19.7%, AIAN 25.9% -> 19.1%, Hispanic 6.4% -> 8.4%. Observed/expected by group stays
  near 1 (non-Hispanic Black 1.08 -> 1.04, non-Hispanic White 1.00 -> 1.00).
- Position: B (drop the four columns), with the reason in the notes: practice and SEL-1, 45 CFR 92.210's duty to
  identify and mitigate, and the measured cost. The builder's "0.9148 against 0.9149/0.9158" should cite a spread
  that holds: 0.9126-0.9167 over 4 seeds of that setup.

------------------------------------------------------------------------------------------------------------------
WHAT AN EXPERT IN THE DOMAIN WOULD CHANGE

a. Pick the actor and match the prediction point and the metric to it. Expected deaths: keep A, rewrite use_case
   around expected infant deaths for county and hospital comparisons, declare log_loss, and name the periviable
   births in the notes or leave them out (under 500 g / 22 weeks). Follow-up: build B as a second folder (alive at
   registration, every certificate item, death after the report; the builder measured 0.861/0.877), citing Florida's
   statutory screen as the deployed example. I prefer C, both folders (PROV-7: distinct tasks).
b. Drop the parents' race and Hispanic origin (issue 1 B).
c. Rewrite fit_reason to say that 39% of the deaths are in the first day, mostly births under 22 weeks or 500 g,
   which the items rank almost perfectly.
d. Under log_loss, re-measure issue 3 with a calibrated model and 3+ seeds.
e. Keep: the removal of the post-birth block at the birth point, NCHS's imputed values without their flags, the
   U.S.-resident cohort, the 2017 sequence-number repair, yearly windows without a gap. These are what I would have
   done.

------------------------------------------------------------------------------------------------------------------
SOURCES

- NCHS linked birth/infant death page, https://www.cdc.gov/nchs/nvss/linked-birth.htm; user guide 2024 period / 2023
  cohort (local copy local-data-warehouse/nchs_linked_birth_infant_death/docs/24PE23CO_ug.txt).
- Florida DOH, "Assessment of the 2019 Florida Infant Risk Screen" (June 2021), read in full:
  https://www.floridahealth.gov/wp-content/uploads/2025/07/infant-risk-screen-evaluation-2019.pdf
- 45 CFR 92.210, https://www.law.cornell.edu/cfr/text/45/92.210 (read); Health Affairs Forefront on the 1557 rule
  (search snippet).
- MFMU VBAC calculator without race (Grobman et al., AJOG 2021): STAT 2021-06-03,
  https://www.statnews.com/2021/06/03/vbac-calculator-birth-cesarean/ (search snippets only).
- NICHD Extremely Preterm Birth Outcomes tool, https://www.nichd.nih.gov/research/supported/EPBO; its inputs from
  https://pmc.ncbi.nlm.nih.gov/articles/PMC12854293 (snippet).
- Vermont Oxford Network risk adjustment (2014), https://vtoxford.zendesk.com/hc/en-us/article_attachments/206498207
  (snippet).
- CDC facility worksheet guide, assisted ventilation immediately following delivery,
  https://www.cdc.gov/nchs/nvss/facility-worksheets-guide/36.htm (snippet).
- PPOR exclusions under 500 g / 24 weeks: https://dchealth.dc.gov/sites/default/files/dc/sites/doh/publication/attachments/PPOR%20Draft%20v3.0.pdf,
  https://www.dhs.wisconsin.gov/publications/p01079.pdf (snippets).

RULES CITED
USE-1, USE-3, USE-5, USE-8, USE-9 (and its weighed factor), LEAK-10, MET-1, MET-6, MET-7, MET-8, MET-9, MET-10,
SEL-1, PROV-7; principles.md tension row "a factor the actor may no longer use".

MEASUREMENTS (mine; scripts and outputs in the run folder)
practitioner.py -> results.json, preds_base.npy, preds_no_race.npy (builder setup, seed 0, age-at-death AUCs,
top-k, deciles, groups); practitioner2.py -> results2_seed{0..3}_*.json, p2_*.log (seeds, smaller model). Train: the
builder's E.load of births_2020-2022 (1M random, seed = run seed); test: joined_2023.parquet, U.S. residents,
500k random (random_state 7), 2,705 deaths.
```

</details>

<details><summary>Blind review: nchs_linked_birth_infant_death</summary>

```text
BLIND REVIEW: nchs_linked_birth_infant_death  (target infant_death, binary, temporal split on birth_month)
Reviewer inputs: clean_room/data.parquet (200,000-row sample of 2,500,000), clean_room/task.md, and the public
NCHS pages / 2024 Period-2023 Cohort linked-file user guide (24PE23CO_linkedUG.pdf). No other local files used.
Scratch code: the run folder

VERDICT
Include with changes: this is real, large, non-trivial US vital-statistics data with an honest at-birth feature set
and a sensible temporal split. Before use, fix the numeric columns that were stored as categories, recode one
sentinel, and document (or remove) a sampling-rate jump in 2021.

WHAT THE TASK IS
Each row is a US live birth from 2017 to 2023, taken from the NCHS birth certificate (the denominator file). The
target is whether the infant died before its first birthday. This appears to be the "user created cohort" (birth year
Y linked to deaths in years Y and Y+1). The features are what the certificate records by shortly after delivery:
parents' demographics, pregnancy history, prenatal care, smoking, maternal risk factors, labor and delivery, Apgar at 5
minutes, birthweight, gestation, and congenital anomalies. Post-delivery items are absent: NICU admission, assisted
ventilation, abnormal conditions, "infant living at time of report" (ILIVE), breastfeeding, and age or cause of death.
So the prediction moment is "at or just after birth".
Real uses: public-health risk screening at birth (who gets home visiting or safe-sleep follow-up), and risk
adjustment when comparing infant mortality across hospitals or states. Mostly this is an epidemiology dataset. It is
not a bedside clinical tool, because clinicians have much richer data. Still, it is a legitimate and well-known
prediction problem.

EVIDENCE THE DATA IS REAL AND THE TARGET IS RIGHT
- Death rate is 5.64 per 1000 (1,127 of 200,000). The published US rate for 2017-2023 is about 5.4-5.8. The guide
  shows the same order of magnitude: "United States ... 19,836 ... 20,081 ... 5.52" (2024 period).
- Low birthweight (<2500 g) is 8.6% and preterm (<37 weeks by obstetric estimate) is 10.3%. Twins are 3.2% and Medicaid
  is 42%. All match national figures.
- Follow-up looks complete, with no truncation at year end. December births pooled over all years have 6.2 deaths per
  1000 (104/16,790). If only deaths in the same calendar year had been counted, I would expect about 4 per 1000.
- Missing values follow the guide's documented reporting gaps:
  * marital_status and paternity_acknowledged are missing for 11.6% of rows. The guide says: "NCHS cannot release
    record-level data on the marital status of the mother for births occurring in California". Consistent with this,
    the missing rows have a lower death rate (3.5 vs 5.9 per 1000).
  * payment_source_detail is missing for 37% of rows. The guide lists "expanded source of payment for delivery" among
    the items with limited reporting areas.
- There are no exact duplicates and no duplicates on the features alone. Only 4 rows are near-duplicates, all twins
  (expected).

SIGNAL / DIFFICULTY
I ran LightGBM (untuned, 600 trees, lr 0.03) on the 200k sample with expanding-window tests on the years 2021, 2022
and 2023 (237, 203 and 208 positives).
  All features:         AUC 0.859 / 0.879 / 0.908   AP 0.38 / 0.40 / 0.39   logloss 0.029 / 0.020 / 0.021
  Birthweight + GA:     AUC 0.792 / 0.825 / 0.837   AP 0.32 / 0.34 / 0.35
  BW + GA + Apgar:      AUC 0.840 / 0.843 / 0.862
  Without BW/GA/Apgar/plurality: AUC 0.82-0.86 (prenatal_visits and steroids act as gestation proxies)
  Prior-rate logloss:   0.036 / 0.032 / 0.033
The best single features are birthweight (AUC 0.84), obstetric-estimate gestation (0.83) and Apgar 5 (0.80). So there
is real signal, it is not trivial, and the other features add value. The full data has about 14k positives across 2.5M
rows, which is large enough to score once the test windows are reasonably wide.

CONCERNS (most to least serious)

1. Numeric columns are stored as string categories.
   Evidence:
   - mother_age is a category with 39 levels ('10-12', '13', ..., '49', '50 and over'). father_age, by contrast, is
     float.
   - The four cigarettes_* columns are categories with 30-62 levels ('0', '1', ..., '96', '98 or more').
   These are NCHS codes MAGER and CIG0-3: single years or counts, with top and bottom coding. As nominal categories
   they lose their order. One-hot encoding blows them up to about 200 dummies, and the rare levels make target
   encoding noisy. Methods that handle high-cardinality categoricals well would be favoured for no good reason.
   Change: map them to numbers ('10-12' -> 12, '50 and over' -> 50, '98 or more' -> 98) and store as float.

2. One interval column holds a sentinel code, not months.
   Evidence: months_since_last_live_birth == 3 occurs in 2,509 rows: 2,392 twins, 107 triplets, 10 quadruplets+, and
   0 singletons. The guide's layout for ILLB_R says "000-003 Plural delivery; 004-300 Months since last live birth;
   888 Not applicable / 1st live birth; 999 Unknown". months_since_last_other_outcome has the same issue (38 rows).
   NaN also mixes "first birth" (77k rows with 0 prior births) and "unknown" (5.1k rows with at least 1 prior birth).
   Change: set the 0-3 codes to NaN (plurality already carries that information), or add a flag. Optionally add an
   indicator for "not applicable" versus "unknown".

3. Undocumented change in sampling rate in 2021.
   Evidence: in the 200k sample there are about 1,650 rows per month for 2017-2020 but about 3,300 per month for
   2021-2023. By year: 20.4k, 20.3k, 20.0k, 19.3k, then 40.0k, 39.9k, 40.1k. National births were flat at 3.6-3.86M per
   year, so the 2.5M table samples about 6.7% of births before 2021 and about 13.7% from 2021 on. The label rate is
   not affected (5.1-6.4 per 1000 in every year). But the "2,500,000 rows" are not a uniform sample of births, and the
   training data's spread over time is set by the preparer, not by the data.
   Change: use one sampling fraction for all years, or state the per-year sampling in task.md.

4. The prediction moment is not stated, and part of the positives are already dying at birth.
   Evidence:
   - 22.7% of deaths weigh 500 g or less, and 81% of such births die.
   - 14.9% of deaths are at 21 weeks or less, and 90% of those births die.
   - 36% of deaths have Apgar 5 of 3 or below.
   Many of these are periviable infants given comfort care who die within hours. For them the certificate, Apgar
   included, is completed after the death. This is not leakage, because every feature is legitimately known minutes
   after birth. But it makes the AUC look better than the useful signal warrants.
   Change: state in task.md that the prediction is made at birth from the birth certificate and that Apgar 5 is
   allowed. Report log loss or AP next to AUC. Optionally consider a variant restricted to births of at least 22 weeks
   or at least 500 g.

5. The temporal split ignores label delay.
   The label is only final 12 months after birth. A model deployed at the start of a test window could not yet know
   the outcomes of training births from the previous 12 months. The split as described ("each test window comes after
   its training rows") lets training run right up to the test window. Because drift is small (yearly rates are
   stable), the optimism should be small.
   Change: leave a 12-month gap between the end of training and the start of testing, or document that this is
   accepted.

6. Small things in preparation and label quality.
   - Unlinked deaths count as survivors. About 1.2% of infant deaths are not linked (US 2024: 19,836 linked versus
     20,081 weighted), so roughly 1% of positives are labelled "No". This is tolerable.
   - Redundant pairs:
     * payment_source_detail is a strict refinement of payment_source (each detail level maps to exactly one coarse
       level).
     * gestation_weeks_combined and gestation_weeks_obstetric_estimate.
     * previous_cesarean and previous_cesareans.
     These are harmless but could be trimmed.
   - set_order is 96.7% NaN, meaning "singleton". That is fine, but an explicit "not applicable" level would be clearer.
   - Reporting changes over time: missing values in eclampsia and infertility items fall from about 4% (2017-2020) to
     0.2% (2022-2023). This is mild drift in missingness.
   - birth_month is a datetime column. If it is fed to models as a feature under a temporal split, it extrapolates.
     Use month-of-year, or drop it as a feature.
   - birth_weekday is stored as float 1-7, which is acceptable.
   - Missingness in marital_status effectively flags California.

WHAT I COULD NOT CHECK
- The exact boundaries of the three test windows. If they are single months, each holds only about 230 positives on
  the full data and AUC noise would be about +/-0.01-0.02.
- The full 2.5M table. I saw only the 200k sample.
- A record-by-record match against the raw NCHS denominator and numerator files, which I did not download. In
  particular I could not confirm that the merge used co_seqnum/co_yod with both numerator years, or that foreign
  residents (restatus=4) were dropped. Both are inferred from the death rate and from the residence_status levels.
- Whether birthweight was imputed for some rows. The bwtimp flag was not kept; the guide says imputation covers about
  0.03% of denominator records.
- Why the sampling rate doubles in 2021.
```

</details>

<details><summary>Task gamer: nchs_linked_birth_infant_death</summary>

```text
TASK GAMER REPORT: nchs_linked_birth_infant_death (infant_death, ROC AUC, 3 yearly test windows 2021/2022/2023)

Verdict: this task barely moves under gaming. No exploit adds more than about 0.002 AUC over an honest tuned
LightGBM (mean 0.9199). The only gain clearly above noise comes from an item the honest model already uses:
cyanotic congenital heart disease, which the certificate often records from diagnoses made after delivery (+0.0018).

Paths: kit = .../nchs_linked_birth_infant_death/panel/participant_kit/, scripts and logs in kit/work/.
Scores come from score.py on the shipped splits. Machine load was very high (load average 140-185 on 96 cores), so
runs were slow but complete. No rows were subsampled. To save disk, work/cache.pkl and work/links.pkl were deleted
after use; common.get_data() and link_mothers.py rebuild them.

Reference models
- Untuned LightGBM (300 trees, lr 0.05, 63 leaves) on features(), birth_month as a month index
  (work/baseline.py): r0f0 0.91717, r1f0 0.91446, r2f0 0.91121, mean 0.91428.
  Adding a random column with 3 seeds (work/noise.py) spreads each split by r0 0.0004, r1 0.0029, r2 0.0014.
- Better honest model: cigarettes and mother_age as numbers, month of year added, regularised LightGBM with 1500 trees
  at lr 0.02 (work/honest_tuned.py): r0f0 0.92328, r1f0 0.92103, r2f0 0.91546, mean 0.91992.
  Random-column spread: r0 0.0004, r1 0.0005, r2 0.0012; mean 0.0003.
  Every exploit below is measured against this model.

EXPLOITS, RANKED BY GAIN (reference: tuned honest model)

| # | Exploit | Script | Honest score | Exploited score | Gain (per split, range) | A deployed model has it? | Fix |
|---|---|---|---|---|---|---|---|
| 1 | cyanotic_congenital_heart_disease is often a diagnosis made after delivery; the shipped features include it | work/attack_late_anomalies_split.py | 0.91816 (feature dropped) | 0.91992 (as shipped) | +0.0018 (r0 +0.0017, r1 +0.0016, r2 +0.0019) | Partly: prenatal diagnoses yes; diagnoses from postnatal progress notes, echo or pulse-oximetry screening no. The deciding fact is the share of recorded cases known by 5 minutes after birth | Drop the column, or move the prediction point to "when the certificate is completed" |
| 2 | No gap between training and test: training includes births of the 12 months before the window, whose 1-year death label is only settled inside the test window | work/attack_label_lag_tuned.py, work/attack_label_lag_sizectrl.py | 0.91795 (12-month gap) | 0.91992 (shipped) | +0.0020 raw (r0 +0.0030, r1 +0.0007, r2 +0.0022). Net of training size (size-matched random drop 0.91832): +0.0004 (r0 +0.0023, r1 -0.0010, r2 -0.0002) | No: at the start of the window those labels are incomplete | 12-month embargo between train end and test start (or censor labels at the window start, which needs age at death) |
| 3 | Rebuild mothers across years: a later birth's months_since_last_live_birth points to the earlier birth's month, and its prior_births_now_dead rose by 1 → the earlier infant died. The later births come from rows of data.parquet that lie after the test window | work/link_mothers.py, work/attack_mother_link.py, work/rule_overrides.py | 0.91992 | rule: r1 0.92106, r2 0.91610; as features: 0.91994 | rule: r1 +0.0000, r2 +0.0006; features: r2 +0.0004 (within the r2 noise of 0.0012). r0 not applicable (no later rows) | No: the later birth does not exist yet. Works only because the kit ships rows from after r1/r2's windows. Within a harness that passes only the split's rows: -0.0003 to +0.0003 | None needed for the benchmark. A kit that should not allow it can ship per-split row sets |
| 4 | Twin sibling in the same test window: the later-born co-twin's prior_births_now_dead counts this infant's death | work/attack_twins.py, work/rule_overrides.py | 0.91992 | 0.91992 | 0.0000 on all splits: 4-10 rows flagged per window, 3-8 of them deaths, all already ranked at the top | No: the death comes after birth | Same fix as 5 |
| 5 | The later-born multiple's own record carries its co-twin's death after birth (prior births "now dead" is counted when the certificate is completed and includes earlier-born co-multiples) | work/attack_twins.py | 0.92004 (co-twin moved back to "living") | 0.91992 (shipped) | -0.0001 (r0 +0.0001, r1 -0.0001, r2 -0.0003): none | No | For rows with months_since_last_live_birth == 3 (the NCHS "plural delivery" code), add prior_births_now_dead into prior_births_now_living |

Mechanisms
1. Cyanotic CHD. The NCHS facility worksheet guide (item 54, saved as work/web/fwg_37.html) defines congenital
   anomalies as "diagnosed prenatally or after delivery". For cyanotic CHD it gives the primary source as "Physician
   progress notes". 1,586 rows are flagged, 18.4% of them deaths (base rate 0.55%). Dropping the column costs
   0.0016-0.0019 on every split, 5 times the noise. Collapsing the confirmed/pending karyotype status of Down syndrome
   and chromosomal disorders (also sourced from "infant progress notes / genetic consult") costs nothing: mean
   0.91982 (-0.0001). Mildest fix: drop cyanotic_congenital_heart_disease. If the task means "at certificate
   completion", restate the prediction point instead.
2. Training rows labelled by the future. The split puts the test window right after the training rows, and the label
   is death within 1 year. For r0, the training rows from 2022 (16% of training) have deaths that happen in 2023.
   With a 12-month gap the score falls 0.0020. Dropping the same number of rows at random costs 0.0016, so the
   recent rows are worth only +0.0004 on average, almost all of it on r0 (+0.0023). The untuned model shows the same
   pattern (gap 0.91380 vs 0.91428). Mildest fix: a 12-month embargo; the effect is small either way.
3. Mother linkage. Join keys: mother race, Hispanic origin, nativity, height, father race, the earlier birth's month
   = the later birth's month minus months_since_last_live_birth, and prior births plus babies born = the later
   record's prior births. Filters: both parents' ages move by the gap, education does not fall, prepregnancy weight
   within 30 lb. Strict pairs saying "dead" are 14% deaths (40/288) against 0.47% for the other pairs. Precision
   stays low because the sample holds about 7-14% of each year's births, so the true earlier birth is usually
   missing. Flagged test rows: r1 171 (10 deaths), r2 391 (13 deaths). With a unique candidate: r1 26 (7), r2 48 (9).
4/5. Plural deliveries. months_since_last_live_birth == 3 is the plural-delivery code (30,830 rows, all multiples).
   On those rows, prior_births_now_dead = 1 means a 26.2% death rate (550 rows), against 5.1% for multiples whose
   prior dead child came from an earlier pregnancy. That fits the worksheet instruction to include earlier-born
   infants of the same delivery who are now dead (work/web/facility_worksheet_item10.html). It is information from
   after the birth, but it affects about 30 deaths per test year that are already near the top of the ranking, so
   AUC does not move.

FLAWS THAT HURT AN HONEST MODEL
| What is wrong | Honest choice that avoids it | Scores | Fix to the task |
|---|---|---|---|
| Birthweight is shipped after NCHS's hot-deck imputation, and the imputation flag (BWTIMP) is dropped. Before imputation, birthweight is "not stated" for 5.1% of deaths vs 0.09% of births (user guide); a deployed model would see it missing | None possible: imputed rows cannot be told apart in the kit | Not measurable. The kit's NaN rate (deaths 0.86%, survivors 0.036%) matches the post-imputation rates (0.81% / 0.03%), so about 4% of deaths carry an imputed weight | Ship bwtimp, or set imputed weights back to NaN |
No measured honest choice beat the shipped training set. Dropping the 2017 rows, where cigarettes_third_trimester
uses the old coding for gestations under 27 weeks, was not worth testing: 2 rows in 1,000 are affected and
gestation is in the features.

ATTACKS THAT FOUND NOTHING
- Row order (work/diag_order.py): the file is sorted by month and shuffled within each month. AUC of position 0.497,
  of rank within month 0.496. The next row's death rate is 0.0062 after a death vs 0.0055 after a survivor (about
  1 SD).
- Copies (work/diag_dups.py): 2 exact duplicate rows (both survivors). Months fall wholly on one side of each split,
  so no row has a copy across the split. About 800 twin pairs have both members sampled (see 4).
- Formats (work/diag_formats.py): all numeric values are whole numbers. The category levels are the same for both
  classes. Birthweight ending in 0 rises from 40.5% (2017) to 54.7% (2023) with reporting practice, with small class
  differences. Weights that convert exactly from ounces have a 0.48% death rate vs 0.58%, an honest recording effect.
- Missing patterns (work/diag_missing.py, diag_cig3.py): cigarettes_third_trimester is missing for 0.9% of rows with
  a 23% death rate. That is NCHS's "not on certificate" code for an obstetric estimate under 27 weeks (since 2018),
  so it is a function of gestation. All other missing patterns are known at birth. marital_status is NaN for
  California (state statute).
- Each feature alone (work/diag_single.py): best are gestation OE 0.835, Apgar 0.829 and birthweight 0.825, against
  0.923 for the full model.
- Paternity and father fields as recorded after the outcome: for unmarried mothers, the death-rate ratio of "not
  acknowledged" to "acknowledged" rises from 1.11 (<=23 weeks) to 1.75 (term). Reverse causation predicts the
  opposite, so this is social-risk signal. Father-age missingness behaves the same way.
- Label against time: no drop in December (the cohort labels are complete). The yearly rate is 0.0054-0.0057, the
  same in training and test.
- Train-vs-test classifier (work/diag_adv.py): AUC 0.66-0.72, driven by changes in reporting coverage (eclampsia and
  fertility-drug missingness fall from 3.7% to 0.2% from 2021; payment_source_detail; marital_status). This is
  drift, not label information.
- Transforms over all rows: none. All values are raw integers or codes.
- Web: there is no competition, leak thread or "magic feature" for this source. Papers flag postnatal variables
  (NICU, abnormal conditions); the kit already drops ILIVE, ITRAN, BFED and the abnormal-conditions items.
- Looking rows up in the public source: the public 2017-2023 cohort linked files carry the death flag and all 83
  columns, so a join would almost certainly recover the labels. Not run (several GB); not ranked.

COULD NOT CHECK
- Which rows have an imputed birthweight (flag dropped). In the numerator file the donor is a previous death with the
  same gestation, race, sex and plurality, so death rows may carry death-like imputed weights. This depends on whether
  the builder took death rows' birth fields from the numerator or the denominator record.
- Labels censored at the window start, which would need age at death (not shipped).
- The share of cyanotic CHD diagnosed before or at delivery, which decides whether exploit 1 is a leak or signal.

Sources: NCHS 2024 Period/2023 Cohort linked file user guide
(https://ftp.cdc.gov/pub/Health_Statistics/NCHS/Dataset_Documentation/DVS/period-cohort-linked/24PE23CO_linkedUG.pdf,
text in work/web/linkedUG.txt); NCHS facility worksheets guide, item 10
(https://www.cdc.gov/nchs/nvss/facility-worksheets-guide/10.htm) and item 54
(https://www.cdc.gov/nchs/nvss/facility-worksheets-guide/37.htm).
```

</details>

<details><summary>Precedent check: nchs_linked_birth_infant_death</summary>

```text
PRECEDENT CHECKER REPORT: nchs_linked_birth_infant_death (folder nchs_linked_birth_infant_death_1m), 2026-11-09

Read (all from the df-large worktree W=df-large):
principles.md (Strengths, Tensions, Exceptions and amendments, Consistent judgement); leak_checks.md LEAK-6, LEAK-10 (three
clauses), LEAK-13, LEAK-15, LEAK-22, LEAK-25, LEAK-30, LEAK-36, LEAK-38, LEAK-39, LEAK-40 and the Mechanisms table;
use_case.md USE-1, USE-3 to USE-6 and Methods; splits.md SPLIT-9, SPLIT-10, SPLIT-14 and Cases; metrics.md MET-8, MET-9,
MET-11; provenance.md PROV-9; cleaning_features.md CLEAN-2, CLEAN-22 (Cases). The definition, the record and the two
sibling records (nchs_natality_birth_weight, nvss_natality_pregnancy_outcomes: both TBD -> Yes, unbuilt, prediction point
at the first prenatal visit, no decision on any call below). The builder report, the register (register.json, 6,080
decisions, 34 flags), the blind reviewer's report (the only phase-A report present), and the working logs of the column
and split auditors (their reports not written yet; cited as logs). Same batch: the definitions, REVIEW.md files and
panel reports of rais_employment_separation_1m, wioa_employment_after_exit, acs_food_stamps_2014_2024_1m,
enem_entrance_exam_scores_1m, sivep_gripe_sari_outcome, kumc_inpatient_aki_prediction, sinan_dengue_case_screening_1m,
chile_school_dropout_mineduc_1m, backblaze_hard_drive_failure_1m. Working copy, clinical: mic, 2_month_survival_rate_prediction,
diabetes_130_us, wids_diabetes_mellitus, heart_failure_followup_survival, framingham_heart_study_fhs. Nothing edited,
nothing run beyond reading.

No curator decision exists on any record of this batch beyond the accept CCs of 2026-11-08: batch siblings are AI
recommendations and are cited as such.

SUMMARY
| # | Call | Reading |
|---|---|---|
| D1 | Prediction point at the birth, all live births (USE-3, USE-4, USE-5, LEAK-36) | consistent (mic, Lennart 2026-09-30; USE-4 eryhemato; sivep AI). Option B follows 2_month_survival's day-3 cohort; option C (two folders) departs from the one-framing calls of mic and 2_month_survival unless a distinct actor is named |
| D2a | Post-birth items dropped (LEAK-10, USE-3) | consistent (mic, kickstarter, heart_failure; sivep and kumc in-stay drops, AI) |
| D2b | Imputation flags dropped, imputed values kept (LEAK-10, LEAK-30, LEAK-39) | consistent (qsar_bioconcentration, Lennart 2026-11-02; acs, AI); set apart from 2_month_survival's adlsc by a fact; LEAK-30, LEAK-39, LEAK-40 not triggered; one sentence missing in the notes |
| D3 | Unknowns that mark early deaths kept with a note (LEAK-6, LEAK-10 clause 2, LEAK-13) | DEPARTS from the curator's two clinical calls on death-marked gaps (mic 2026-09-30; 2_month_survival 2026-10-12 and 2026-10-26), with a stated reason that does not set it apart; a distinguishing fact exists but is not written. Prompt 1 |
| D4 | Unlinked deaths count as survivors (LEAK-22) | consistent in substance (the source's own cohort file); LEAK-22 is not the governing rule; LEAK-25's letter reaches it and has no case this small: write the reading |
| D5 | Parents' race and Hispanic origin kept (SEL-1; Tensions row) | consistent with the clinical keeps; DEPARTS from the batch's method without a stated reason; the use case names a per-person service that wioa's reading would reach. Prompt 2 |
| D6 | No gap (SPLIT-10) | consistent: an application, as lt_vehicle_loan_default_prediction (Lennart 2026-11-05); set apart from sivep's and wioa's gaps by facts |
| D7 | Fallback roc_auc at 0.55% (MET-8, MET-9) | consistent; coupled to D3 and D5 through the use case |
| D8 | Year 2026 (PROV-9) | consistent (the growing-source clause; chile, enem, sivep, uk_mot; acs 2025 the same reading) |

Register flags touching this case:
  * drift, mechanism "post-outcome feature" (Lennart: keep up to 2026-11-05, exclude from 2026-11-08): bears on D3. The
    newest call went to "out": bank_marketing `campaign`, kept with a note on 2026-11-06, dropped on 2026-11-08 (issue 2).
    A keep-with-note here runs against that direction (a drift risk, not yet a drift).
  * opposite_outcomes LEAK-38 (medical_facility keep, sendy keep, kick/expresso drop): read for D3 below.
  * amendment_due SPLIT-10 (exceptions on 10 datasets): not touched; D6 is an application, not an exception.
  * opposite_outcomes USE-5 (diabetes_3, xente, chicago): none is about this label; no pair with D1 or D4.
  * No flag on SEL-1, PROV-9 or MET-9; the pairs in D3 and D5 were found by reading the cases.

======================================================================================================================
D1. Prediction point: at the birth for every live birth (implemented, builder issue 2 A) -> CONSISTENT
======================================================================================================================
Precedents
  * mic (Lennart, 2026-09-30, CC: "Leak fixed: predict at admission"): of the source's four time points the earliest,
    because the later ones carry death-marked blanks (91% of the 138 rows missing a day-3 field died). One framing shipped.
  * 2_month_survival_rate_prediction (Lennart, 2026-10-12 and 2026-10-26; verdict ship 2026-10-26): the source's own
    point (study day 3); the 138 patients dead on day 3 dropped, "they are dead at the prediction point" (the LEAK-36 /
    LEAK-22 cohort move); one target ("the 6-month and in-hospital framings are nested versions of the same signal",
    CC 2026-10-12).
  * USE-4 (eryhemato_squamous_disease): offer the task at the stage the source describes. NCHS's page: "risk factors
    present at birth".
  * sivep_gripe_sari_outcome (AI, this batch): admission, the earliest point, keeps every admitted patient; a later
    (notification) point would select rows by the outcome date.
  * LEAK-36 (diabetes_130_us "Expired"): a value known at the prediction point that settles the outcome is a cohort
    question, not a feature.
Facts compared
  * A is the earliest point that keeps every birth and the source's stated stage: follows mic, sivep and USE-4. ILIVE is
    a feature leak under A (dropped, LEAK-10) and a cohort filter under B (LEAK-36): both readings follow precedent.
  * B (infants alive at the report, 7,566 of 19,743 deaths of 2023 leave) has the shape of 2_month_survival's day-3
    cohort. It is a fix in the definition (re-target, filter), which the remedy ladder ranks above a note; see D3.
  * C (both as two folders): mic shipped one of four time points and 2_month_survival one of three nested framings
    (Lennart). Two folders need a fact that makes B a distinct task under PROV-7: a distinct actor and moment (the health
    department's home-visiting screen at registration against the hospital's estimate at the birth). The builder names
    it; the issue should say it is the fact, and the screening's open question "one task per birth register" (two
    natality siblings already on the same births) weighs against a fourth task from one file.
  * Not a precedent question, passed on: the blind reviewer's periviable births (22.7% of deaths weigh 500 g or less,
    81% of such births die). No rule drops rows whose outcome is nearly certain at the prediction point; LEAK-36 drops
    rows whose outcome is already settled. Nothing to align.

======================================================================================================================
D2a. Post-birth items dropped (LEAK-10 Must, USE-3 Must) -> CONSISTENT
======================================================================================================================
NICU, ventilation, surfactant, antibiotics, seizures, transfer within 24 h, ILIVE, breastfeeding at discharge, the
10-minute Apgar, and the mother's transfusion, unplanned hysterectomy and ICU admission go; the delivery's own events
(perineal laceration, ruptured uterus) and the transfer before delivery stay. Same treatment as mic's ICU day-1..3
columns (Lennart 2026-09-30), kickstarter `staff_pick`, heart_failure `time`; in this batch sivep's in-stay fields and
kumc's renal-failure comorbidity and procedure DRGs (AI). The measured worth (+0.009 ROC AUC together; ILIVE alone 0.919)
is stated. No departure.

======================================================================================================================
D2b. NCHS's imputation flags dropped, imputed values kept (LEAK-10, LEAK-30, LEAK-39) -> CONSISTENT
======================================================================================================================
Precedents
  * qsar_bioconcentration (CLEAN-22 Cases, Lennart 2026-11-02): `logKOW_type` (measured or predicted) leaves, "it records
    how the authors filled their 2015 table", the filled values stay. Provenance flags in the actor's own record stay
    (pva `AGEFLAG`, thyroid `*_measured`, sf_permit `point_source`). NCHS's flags record NCHS's national edit, not the
    hospital's record: the qsar side.
  * acs_food_stamps_2014_2024_1m (AI, this batch): allocated values kept as released, allocation flags no inputs
    (PROV-13), the hot-deck checked for the label (income +0.0015 on allocated rows against +0.0143 on reported rows).
  * 2_month_survival_rate_prediction (Lennart 2026-10-12): `adlsc` dropped, its imputation "used the interview status
    ('Pt Death', 'Pt Discharged')". Set apart by a fact: NCHS's birthweight hot-deck reads the previous record's
    gestation, race, sex and plurality, no outcome.
Facts compared
  * The flag marks a missing item and the missing item marks a death (BWTIMP=1: 60.6% died, 9,736 births 2017-2023), so
    the flag is "missingness that encodes the outcome" (LEAK-10) and dropping it is the smallest fix (LEAK-7); the flags
    add no ROC AUC (0.9147 against 0.9149/0.9158).
  * LEAK-30 governs statistics over all rows (z-scores, ranks, PCA); a single label-free donor is not one. LEAK-40 tests
    fills from neighbouring rows "in a file sorted by class"; the births file is ordered before the death link exists,
    so its trigger is not met. LEAK-39: imputed rows hold an ordinary donor value and cannot be recognised once the flag
    is gone (9,736 of 25.9M); not triggered.
  * Missing sentence: the notes describe the hot-deck but not that the donor is label-free and the file is not ordered by
    the outcome; the builder's checklist says it (LEAK-27 to LEAK-31 row). One clause in the notes closes it.

======================================================================================================================
D3. Unknowns that mark early deaths, kept with a `Potential leak, kept on purpose:` note (LEAK-6, LEAK-10, LEAK-13)
    -> DEPARTS WITH A STATED REASON THAT DOES NOT SET IT APART
======================================================================================================================
As implemented: unknowns 3-12x as frequent among deaths in the first day for most items, 17-90x for the newborn's
measurements; filling every missing value but the father's with random training values: ROC AUC 0.9171 against
0.9149/0.9158 (two seeds), log loss 0.0192 against 0.0190. Notes: "These unknowns cannot be told from the others, so they
stay ... Revisit if log loss is reported." The column auditor's working log (work_column_auditor/b_conditional.log, a
conditional test: observed over predicted from the covariates) finds the mark beyond the covariates for day-0 deaths:
O/E 1.99 mother's education, 1.89 first-trimester cigarettes, 1.80 prior live births, 1.69 anencephaly, 1.52 WIC,
1.25 prenatal care month (the five-minute Apgar 0.92: explained by the covariates).

Precedents that kept late values with a note (LEAK-10 clause 2, LEAK-6 narrowing)
  * onlinenewspopularity (Lennart 2026-10-26): crawl-time counts, the traced part changes R^2 by -0.0004.
  * medical_facility_operational_data (Lennart 2026-11-05): schedule fields, "the whole-field worth is an upper bound on
    the late part, and it sits within about two seed SDs".
  * kumc_inpatient_aki_prediction (AI, this batch, curator issue 1 open): untraceable discharge codes kept where the traced
    part shows no gain.
Precedents that removed it
  * mic (Lennart 2026-09-30): death-marked blanks of the day-1..3 columns; the prediction point moved earlier.
  * 2_month_survival_rate_prediction (Lennart 2026-10-12 and 2026-10-26): interview fields whose gaps mark deaths dropped;
    edu and income "missing more often among the deaths on days 4-7 (edu 31.4% against 16.3%, income 43.0% against
    31.5%)" with "no measurable effect (dropping both changes ROC AUC by 0.0001)", dropped anyway ("it is also better for
    fairness maybe"); adlp (worth 0.0035) dropped.
  * kick, expresso_churn_prediction (Lennart 2026-10-22, LEAK-38 scope amendment): a field whose missingness given the
    covariates differs by outcome is dropped under LEAK-10.
  * distribution_transformers_at_cauca_department (Lennart 2026-10-21): dropped where a gain may sit (0.701 -> 0.639).
Comparison
  * NCHS's stated reason is the hiding test: no ROC AUC change. 2_month_survival's edu and income had the same fact (no
    measurable change) and a weaker mark (ratios 1.4-1.9 against 3-12 here), and Lennart dropped them. LEAK-10 also says
    "a 'removing it changes no score' test alone is still no reason to keep (2026-10-21)". So the written reason does not
    set NCHS apart from the closest clinical case.
  * Facts that may set it apart, evident from the data, not written: (1) the items describe facts that exist at the birth
    (pre-birth history, measurements taken at the birth); only their entry on the certificate comes later, so the gaps
    are LEAK-10's later-pull kind. 2_month_survival's interview was held after the prediction point (days 2-7, median day
    4), so its values themselves did not exist yet for many patients (LEAK-10's first clause). (2) The mark runs through
    nearly every item, the task's core included (birthweight, gestation, prenatal care), so no field drop of the
    2_month_survival kind removes it without removing the task, and moving the prediction point earlier (mic's remedy)
    does not either: the prenatal items are marked too. The only fix is option B, a different task.
  * Against the distinguishing reading: LEAK-10 lists "missingness that encodes the outcome" among what is out, USE-3 names
    "a field that is blank because the outcome already happened" as a leak, and the remedy ladder ranks a fix in the
    definition (B) above a note. The curator's two calls on death-marked gaps both fixed them. The latest drift on
    post-outcome values points to "out" (bank_marketing, 2026-11-08).
  * Rank: LEAK-10 is a Must; its clause 2 keep is "a case-by-case judgment of the curator, never a default". Keeping is a
    reasonable reading only if the curator takes facts (1) and (2) as the case-by-case ground; otherwise it is not an
    exception that a Must allows, and B is the fix.
  * LEAK-13 (class-specific recording conventions: precision and format, hepatitis_c, gallstone) is not the mechanism
    (completeness, not convention). LEAK-15 (an artefact through several features that cannot be undone retires the
    dataset) is the rule a reader may raise: its test is whether the artefact drives the score; the hiding test says it
    does not on ROC AUC. Say so in the issue.

Prompt 1 (issue shape):

**Consistency check (AI, 2026-11-09):** Keep the unknowns that mark early deaths with a note, when your two calls on death-marked gaps in clinical data (mic, 2_month_survival_rate_prediction) both removed them?
- **Problem:**
  - The certificate of an infant who died in its first day is less complete: unknowns are 3-12 times as frequent for most items and 17-90 times for the newborn's measurements, and up to 2 times as frequent given the other items[^d3num].
  - The definition keeps them because hiding them changes no ROC AUC (0.9171 against 0.9149 and 0.9158), and log loss rises from 0.0190 to 0.0192.
  - In 2_month_survival_rate_prediction you dropped education and income for the same kind of gaps, though they changed ROC AUC by 0.0001 (2026-10-26); in mic you moved the prediction point (2026-09-30)[^d3prec].
  - What may set this case apart is not in the notes: the items exist at the birth and only their entry comes later, and the gaps run through nearly every item, so no field drop or earlier point removes them; only option B of issue 2 does[^d3rule].
- **Options:**

  | | Option | What it does | Pro | Con |
  |---|---|---|---|---|
  | a | Keep with the note, the fact recorded | the note names (1) items that exist at the birth, entered later, and (2) a mark through the whole certificate that no field drop removes; your case-by-case keep under LEAK-10 clause 2 | keeps the screened task at the birth; follows medical_facility_operational_data and onlinenewspopularity | the closest clinical cases went the other way; LEAK-10 says a "changes no score" test alone is no reason |
  | b | Treat like mic and 2_month_survival_rate_prediction: remove the gaps by the fix | issue 2 option B: the infants alive at the report, every certificate item a feature (ROC AUC 0.861 without the post-birth items, 0.877 with them; hiding the gaps changes nothing there) | no outcome mark left; a fix ranks above a note | another task: 38% of the deaths leave, and the actor becomes the registration-time screen |
  | c | Reopen 2_month_survival_rate_prediction to keep edu and income with a note | the earlier drop is undone to match this case | one practice for both | edu and income came from an interview held after the prediction point, a timing leak this case does not have |
  | d | Amend LEAK-10 clause 2 | gaps that mark the outcome but cannot be located stay with a note when their whole worth on the declared metric is within seed noise | one rule for gaps and late values | widens a Must's exception path; mic and kick would still differ by their gain |

- **Recommendation:** a, if you accept facts (1) and (2) as the case-by-case ground; the note then names 2_month_survival_rate_prediction and why it differs, and says the keep holds only while the metric is ROC AUC.
- **Decision:** a, b, c or d?

[^d3num]: builder_report.md (probe 3 reading 1, experiments_*.json); work_column_auditor/b_conditional.log (observed over predicted from the covariates, day-0 deaths: education 1.99, first-trimester cigarettes 1.89, prior live births 1.80, anencephaly 1.69, WIC 1.52, prenatal care month 1.25).
[^d3prec]: curation/records/2_month_survival_rate_prediction.md, CC 2026-10-12 and 2026-10-26 (issues 7, 10); curation/records/mic.md, CC 2026-09-30; leak_checks.md Mechanisms rows "Missingness that encodes the outcome" (mic) and "LEAK-10, LEAK-6 (applied, Lennart, 2026-11-05)" (medical_facility_operational_data).
[^d3rule]: **LEAK-10** (Must; amended 2026-11-08): out is "missingness that encodes the outcome"; clause 2: late values that cannot be located "stay with a note only when the part that can be traced shows none", "a case-by-case judgment of the curator, never a default"; "a 'removing it changes no score' test alone is still no reason to keep (2026-10-21)". **LEAK-6** (Must): "a confirmed leak goes even when small", narrowed by clause 2. **USE-3** (Must): "a field that is blank because the outcome already happened" is a leak. principles.md, remedy ladder: a fix in the definition before a note.

======================================================================================================================
D4. Deaths NCHS could not link count as survivors (cited as LEAK-22) -> CONSISTENT IN SUBSTANCE; RULE CITATION TO FIX
======================================================================================================================
Facts: 260 of the 2023 cohort's deaths unlinked (1.3% of deaths; about 0.007% of the "No" rows); the user guide's "User
Created Cohort File" counts linked deaths only; the period files' weight for unlinked deaths (`recwt`) is not for cohort
files (record, guide). The blind reviewer: "tolerable".
  * LEAK-22 is not the rule that governs. Its cases are rows that cannot have the outcome (diabetes_130_us: deaths and
    hospice removed) and a competing event that keeps the row's own label (framingham_heart_study_fhs, Lennart
    2026-10-22). Here a row has the outcome and carries "No".
  * The rule whose letter reaches it is LEAK-25 (Must): "'No event' mixed with 'not recorded' is a censoring bias:
    retire unless the recording process can be recovered". Its cases are all large, structured shares: ghanas (retired
    2026-10-01), caracas, account_debt, fraud_detection (located and dropped, 2026-10-21), noaa_storm (kept by reporting
    unit, Andrej 2026-11-02). The unlinked cannot be located, and the public file has no state, so noaa's unit clause
    does not reach. No precedent holds a share this small.
  * Not a departure from any decided case. What is missing is the reading: the notes should name LEAK-25 (not LEAK-22)
    and say why its retire clause does not reach this (label noise on 0.007% of the "No" rows, the source's own cohort
    convention, not a censoring by period or unit). If the curator agrees, a Cases row under LEAK-25 lets the next linked
    file follow it. If the curator reads LEAK-25 literally, a Must allows no exception: the route would be an amendment
    (a size clause), not an exception. No prompt: nothing was decided the other way.

======================================================================================================================
D5. Parents' race and Hispanic origin kept (SEL-1 Must; Tensions row "a factor the actor may no longer use")
    -> CONSISTENT WITH THE CLINICAL KEEPS; DEPARTS FROM THE BATCH'S METHOD WITHOUT A STATED REASON
======================================================================================================================
As implemented: the four columns kept, note "as in NCHS's tables of infant mortality ... the curator decides"; builder
issue 1 recommends B (drop) on "no measured cost" (0.9148 without, 0.9149/0.9158 with).

Decided precedents
  * The Tensions row covers insurance pricing, sex only: bemtpl97 (Lennart 2026-11-05: "they would not be able to use
    sex"); australian_vehicle_insurance_2004_2005, pricing_game_2017_french_mtpl, frempl, spanish_homeowners (Lennart
    2026-11-08). Race was never dropped by a curator decision; NCHS is outside the row's written scope.
  * Clinical definitions keep race, never reviewed on SEL-1: 2_month_survival_rate_prediction, diabetes_130_us,
    wids_diabetes_mellitus (ethnicity). 2_month_survival dropped edu and income partly "better for fairness maybe"
    (Lennart 2026-10-26), but kept race.
Batch readings (AI, undecided): every one asks whether the actor's own law bars the ground for its decision
  * rais_employment_separation_1m: five grounds dropped, Lei 9.029/1995 art. 1 bars an employer; proposes the extension
    "to any decision on a person where the actor's own law bars the factor" (its issue 1).
  * wioa_employment_after_exit: race, Hispanic ethnicity and sex dropped; 29 CFR 38.6(b) bars a WIOA recipient from any
    "aid, benefit, service, or training that is different" on these grounds; DOL's statistical adjustment model (TEGL
    26-15) "uses some of them, but on state-quarter aggregates ... not to allocate a service to a person".
  * acs_food_stamps_2014_2024_1m: under the outreach framing 7 CFR 272.6(a) bars them (drop, place of birth included);
    under the imputer framing no law binds the Census Bureau (keep).
  * enem_entrance_exam_scores_1m: kept; no law bars them for a voluntary support offer.
  * sivep_gripe_sari_outcome: kept; its domain practitioner finds no statutory bar and would drop on professional norms;
    its precedent checker asks to decide with rais issue 1 and to scope the extension (a prognosis against an allocation).
  * kumc_inpatient_aki_prediction: kept, SEL-1 not raised.
Facts compared
  * The use case names two decisions: risk adjustment ("expected deaths against which hospitals' and counties' infant
    deaths are compared", an aggregate) and "nurse home visits to the families at highest risk" (a service to a person,
    by a state health department). USE-1's method asks for "the most plausible one"; wioa's panel narrowed its use case
    to one decision for the same reason.
  * Under the batch's method the two answer differently. Aggregate risk adjustment matches wioa's TEGL 26-15 reading
    (keep). The home-visit allocation by a federally funded health department falls under Title VI of the Civil Rights
    Act (42 U.S.C. 2000d) and HHS's rule 45 CFR 80.3(b)(1)(ii), which bars a recipient from providing a service "which is
    different, or is provided in a different manner" on the ground of race, color or national origin: the wording of 29
    CFR 38.6(b) on which wioa dropped race and ethnicity (text recalled, NOT read in this run; to verify). HHS's
    Section 1557 rule, 45 CFR 92.210 (2024), on patient care decision support tools asks covered entities to identify
    tools using race, color, national origin, sex, age or disability and to mitigate the risk of discrimination: a duty,
    not a bar (recalled, not read; current status to check).
  * The definition's note gives the source's analytic practice ("as in NCHS's tables"), and issue 1 gives a measured cost
    of zero. Neither is the fact the batch's method asks for: rais's precedent checker already noted that the size of a
    gain is no fact that sets a case apart, and a zero cost is the same argument turned around.
  * Issue 1's Consistency line is incomplete: it names acs and enem as keeping race with the call open, but not rais and
    wioa (both drop), nor sivep's panel. Under a "drop" reading, `mother_nativity` (born in the U.S. or abroad) is a
    national-origin proxy as acs's place of birth and wioa's English-learner item were: the four-column list should
    either include it or say why not.
  * A "listed ground leaves" reading of Section 1557 would take infant sex, mother's age and the congenital anomalies
    (Down syndrome is a disability) out of a clinical task: the reason sivep's checker asks for a scope (a prognosis
    against an allocation) before the extension is applied to clinical risk scores.
  * Drift: none (no curator decision on race). Third exception: none recorded; but six pending readings of the row in one
    batch (rais, wioa, acs, enem, sivep, this one) mean the row's scope is due as one decision, each dataset then
    getting its own REVIEW.md issue (per-dataset rule).

Prompt 2 (issue shape):

**Consistency check (AI, 2026-11-09):** Keep the parents' race and Hispanic origin for a use case that includes allocating nurse home visits, when wioa_employment_after_exit drops race and ethnicity because its actor's federal rule bars a different service on those grounds?
- **Problem:**
  - The use case names two decisions: expected deaths for comparing hospitals and counties, and nurse home visits for the families at highest risk[^d5uc].
  - The batch decides protected grounds by the actor's own law: rais drops five grounds under Lei 9.029/1995, wioa drops race, ethnicity and sex under 29 CFR 38.6(b), enem keeps them where no law bars them[^d5batch].
  - A state health department's home-visiting programme is federally funded, and HHS's Title VI rule (45 CFR 80.3(b)(1)(ii), not read here) bars a service "different, or provided in a different manner" by race, color or national origin, the wording wioa relied on[^d5law].
  - Aggregate risk adjustment is no service to a person, like DOL's adjustment model that wioa leaves alone; the notes say neither.
- **Consistency:** the clinical definitions keep race (2_month_survival_rate_prediction, diabetes_130_us, wids_diabetes_mellitus; kumc and sivep in this batch); the curator's stance so far covers sex in insurance pricing only.
- **Effect on the task:** without the four columns ROC AUC is 0.9148, against 0.9149 and 0.9158 with them (two seeds).
- **Options:**

  | | Option | What it does | Pro | Con |
  |---|---|---|---|---|
  | a | Keep, the use case narrowed to risk adjustment | `use_case` names the expected-deaths comparison only; the note says no law bars race in an aggregate estimate, as wioa reads DOL's adjustment model | keeps NCHS's analytic variables; follows the clinical keeps; one decision per use case (USE-1) | drops the follow-up actor; the metric question reopens (calibration counts for expected deaths, MET-11), and with it issue 3 |
  | b | Treat like wioa: drop race and Hispanic origin (and decide `mother_nativity` with them) | four or five columns leave; the note cites the Title VI rule; infant sex and mother's age stay as clinical inputs Title VI does not list | follows the batch's reading for a service to a person; no measured cost | the rule text is not read yet; departs from the clinical keeps, which then need their own issues |
  | c | Reopen wioa to keep its grounds | wioa's drop is undone | one practice for public programmes | wioa's actor is bound by 29 CFR 38.6(b) in so many words |
  | d | Decide the row's scope first (with rais issue 1) | the row covers a decision on a person's access to a job, a service or a benefit where the actor's law bars the ground; a prognosis or an aggregate estimate stays outside | one rule for rais, wioa, acs, enem, sivep, kumc and this dataset | waits on rais; under it this use case as written still gets b |

- **Recommendation:** d, then b for the use case as written (it names a service to a person); a if you prefer the risk-adjustment actor alone. Either way the note states which reading was taken, as enem and wioa do, and sivep and kumc are decided alike in their own issues.
- **Decision:** a, b, c or d?

[^d5uc]: dataset.py, `task_summary.use_case`; USE-1 Methods: "write the most plausible one and say 'for example'".
[^d5batch]: rais_employment_separation_1m/dataset.py notes and panel/mediator.report.txt issue 1; wioa_employment_after_exit/dataset.py notes (SEL-1 bullets); enem_entrance_exam_scores_1m/REVIEW.md issue 1; acs_food_stamps_2014_2024_1m/REVIEW.md; sivep_gripe_sari_outcome panel/precedent_checker.report.txt section 6.
[^d5law]: 42 U.S.C. 2000d; 45 CFR 80.3(b)(1)(ii); 45 CFR 92.210 (Section 1557, 2024): all recalled, not read in this run. **SEL-1** (Must): a task with ethical concerns is out; a Must the definition can fix is fixed (remedy ladder). principles.md, Tensions, "A rating factor known at the prediction point against a factor the actor may no longer use" (P3 and P4; USE-1, USE-6).

======================================================================================================================
D6. No gap between training and test years (SPLIT-10 Should) -> CONSISTENT (AN APPLICATION)
======================================================================================================================
Precedents
  * lt_vehicle_loan_default_prediction (Lennart 2026-11-04 and 2026-11-05; splits.md Cases): "one due date per loan ...
    and every label final at release, so the unmatured rows are not selected by their outcome"; the newest labels add
    0.0018-0.0051 ROC AUC at equal size; no gap, "an application, not an exception".
  * wisconsin_local_government_property_insurance_fund (Lennart 2026-11-08): the same facts recorded as an exception
    serving SPLIT-14's floor. NCHS does not need the floor argument (a one-year gap keeps the floor with the 2016 cohort,
    builder issue 4 B), so the lt_vehicle route is the right one; no exception is added to SPLIT-10's amendment_due count.
Facts compared
  * One horizon per birth (death within 365 days), every label final in the release: SPLIT-10's fixed-horizon clause,
    read as lt_vehicle's case reads "one due date". The newest cohort adds nothing at equal size (2022/2021/2020 alone on
    2023: 0.9137/0.9142/0.9151 ROC AUC; log loss 0.0190/0.0192/0.0193), as the clause asks the notes to state. The split
    auditor's working log (a2_experiments.log) finds gaps of 0, 1 and 2 years at 0.916-0.918 with no order.
  * No SPLIT-9 shortcut: no person id, twins share one birth year.
  * sivep (AI, one-month gap) is set apart by a fact: at its release end open cases differ by class (without a gap 53-62%
    of the last month's deaths against 47-51% of its discharges were open), a selection by the outcome; NCHS's release
    holds final labels.
  * wioa (AI, nine-month gap) is set apart by a fact: its gap "also keeps a returning person's later-measured label out
    of training" (SPLIT-9). On the release lag wioa reads as NCHS does: the gap follows the state's own wage records, not
    DOL's later file fill. NCHS's "a health department linking its own records would not" have the two-year release lag
    is the same reading.

======================================================================================================================
D7. Fallback roc_auc at a 0.55% base rate (MET-8, MET-9 Should) -> CONSISTENT
======================================================================================================================
MET-9: imbalance alone is no reason for PR AUC; `average_precision` "when the source chose it as its criterion and the
decision acts only on the top of the ranking". NCHS chose no metric. Same reading: backblaze_hard_drive_failure_1m (AI,
the operator acts on the top 0.1-1%, MET-9 named), sivep (AI), turkcell_radio_link_failure_prediction_1m (F1 overruled to
the fallback); case sepsis_survival_minimal_clinical_records (PR AUC on the majority class overruled). MET-11's `context`
needs a clear context; with two uses (ranking for follow-up, calibrated sums for expected deaths) it is not clear, so the
fallback holds. Coupling to say in the issues: if D5 (a) narrows the use case to risk adjustment, MET-11 may make a
calibration metric obvious, and D3's keep, stated "while the metric is ROC AUC", reopens with it (the gaps carry about
+1% log loss).

======================================================================================================================
D8. Year 2026 (PROV-9 Must) -> CONSISTENT
======================================================================================================================
PROV-9: "A source that grows over time (a public register ...) takes the year of the snapshot we pin." The yearly
linked files are such a series; the newest pinned zip (2024PE2023CO) was posted 2026-01-22. The batch reads it the same
way (AI): chile_school_dropout_mineduc_1m 2026 (newest file March 2026), enem 2026, sivep 2026, uk_mot 2026, rais 2026,
wioa 2026; acs 2025 (its newest file, 2024, published in 2025). kumc 2018 and nfip 2019 are first publications of other
source kinds. The unused 2017PE2016CO zip was re-posted 2026-06-10; the used zips' server dates are in the download text.

======================================================================================================================
OUTSIDE THE CALLS GIVEN (passed on, not precedent findings)
======================================================================================================================
  * `months_since_last_live_birth` and `months_since_last_other_outcome` keep codes 000-003, which the guide reads as
    "Plural delivery" (blind reviewer: 2,509 rows at 3, none a singleton): a sentinel, CLEAN-10.
  * `mother_age` and the four cigarette columns are typed ordinal in `_feature_types` (CLEAN-14 as set 2026-11-01, mic:
    "counts with a cut end stay ordered categories"); the blind reviewer saw unordered categories in the clean-room file.
    Check the container's dtype, not the rule.
  * The timing of some anomaly items (cyanotic congenital heart disease is often found by the 24-hour pulse-oximetry
    screen; Down syndrome "confirmed or pending"): a LEAK-10 question for the claim and column auditors.
```

</details>

<details><summary>Advocate: nchs_linked_birth_infant_death</summary>

```text
ADVOCATE OPENING BRIEF: nchs_linked_birth_infant_death (folder nchs_linked_birth_infant_death_1m)

Position: ship the at-birth task (option A of issue 2), with the located late cells blanked or dropped in the
definition (no decision needed: LEAK-6/LEAK-7 Must) and race decided by the curator. No reviewer asks to retire it.

1. Real, scoped, worth benchmarking (P2 SEL-2..16, P6 TP-1..10; all reviewers agree).
   Evidence: the U.S. national vital register, 25.9M births 2017-2023, 0.553% infant deaths; NCHS's own purpose
   "risk factors present at birth". Task probes: no flags; linear 0.902, LightGBM 0.901, RF 0.888 (spread 0.030,
   paired SE 0.006), best single feature 0.783 (TP-4 reading 5: the natural core, gestation/weight). The blind
   reviewer, without the record, says "include with changes"; claim, column and split auditors: ship after changes.
   Outranks: nothing in the reports is a P1/P2 failure that retires the dataset.

2. The confirmed leaks are located and fixed by the mildest rung, inside the definition (LEAK-6, LEAK-7 Must;
   remedy ladder: a fix in the definition before retiring).
   - Co-twin in prior_births_now_dead/living (column F2, claim F1): blank both for plural births with set order >1
     (or code 000-003). Worth: +0.0005 AUC (SD 0.0013); gamer exploit 5: -0.0001. Concede the leak, ship the fix.
   - cyanotic_congenital_heart_disease, diagnosed from "physician progress notes" (gamer exploit 1, +0.0018, 5x
     noise; claim F3): drop the column. Karyotype confirmed/pending: collapse (costs 0.0001).
   - paternity_acknowledged, "signed in the hospital" (claim F2): drop.
   - imputed birthweight only for linked deaths 2017-2019 (claim F4, LEAK-13): blank BWTIMP=1 values for those years.
   Why it wins: each is a located-cell fix; LEAK-6 says a confirmed leak goes even when small, and the gamer finds no
   exploit above ~0.002 AUC over an honest tuned model (0.9199), so after these fixes the task stands.

3. The temporal split is right (SPLIT-1..22; split auditor "RIGHT WITH NOTES").
   No gap applies SPLIT-10's fixed-horizon clause (label final at release, probe 13 z -0.1/-0.3); measured cost of
   no gap about +0.001 AUC over three windows, same for both learners, order unchanged; gamer size-matched net +0.0004.
   No twin or sibling crosses (0 plural test sets linked). Fix: reword splits_comment (NCHS posts 23-29 months late)
   and report 3-window means. SPLIT-10 is a Should; a measured 0.001 does not outrank a Must elsewhere.

4. Outcome-marked unknowns (issue 3, LEAK-10 clause 2): concede the precedent departure (mic, 2_month_survival).
   Mildest honest form: keep with the note only if the curator takes the stated facts as the case-by-case ground
   (cannot be located per cell; hiding all missing values: AUC 0.9171 vs 0.9149/0.9158, log loss +1%), naming
   2_month_survival and why it differs (no late interview; the gaps are the certificate's, at birth). If the curator
   will not, option B of issue 2 (infants alive at the report, AUC 0.861, hiding changes nothing) is a clean second
   framing. Either way the record ships; this is a choice of remedy, not a retire (LEAK-15 test: the artefact does
   not drive the score).

5. Race and Hispanic origin (issue 1, SEL-1 Must, P1): no cost to drop (AUC 0.9148 vs 0.9149/0.9158). I accept
   option B (drop the four columns): it removes the only P1 concern at zero measured cost, so P1 cannot block the ship.

6. Metric: ROC AUC fallback holds (MET-1..11); Saravanou 2019 (claim F6) reports PR and AUC, so fix the reason's
   "where we looked" wording; domain practitioner prefers log loss for expected-deaths risk adjustment (USE-9 direct
   half) — a metric choice, not a validity failure; whichever the curator picks, the data are unchanged.

7. Cleaning findings are cheap and need no decision (CLEAN rules): mother_age and cigarettes as numbers (blind; the
   gamer's honest model uses them so), months_since code 3 "plural delivery" -> missing, plural-delivery code 3 -> 0,
   2021+ sampling jump explained as the _1m budget (document it), LEAK-25 cited instead of LEAK-22 for the 1.3%
   unlinked deaths (precedent D4), birth_month kept as the time column. Independent small failures are not conflicts
   with shipping.
```

</details>

<details><summary>Critic: nchs_linked_birth_infant_death</summary>

```text
CRITIC OPENING BRIEF: nchs_linked_birth_infant_death (folder nchs_linked_birth_infant_death_1m), 2026-11-09

Position: ship only after changes. The task is real and well built; nothing below calls for exclusion. But the
definition ships values recorded after its own prediction point, states a use case and metric that point at different
actors, and keeps a contested input group with no measured value. Points in rank order (validity first, Must first).

1. Co-twin's death in the prior-birth counts (P4, LEAK-10 Must; LEAK-6, LEAK-7).
   Problem: for a 2nd/3rd-born multiple, prior_births_now_dead/now_living count the earlier co-twin's status "now", at
   the worksheet's completion (facility-worksheet guide items 9-10), i.e. after this infant's birth. Effect: the label
   of a strongly tied sibling leaks into the feature; a deployed at-birth model does not have it.
   Evidence: column auditor A2 (2023 raw: count>0 for 1.83% of 2nd-born vs 1.36% of 1st-born twins; death share when
   >0 19.6% vs 5.4%; 28.1% vs 5.1% among first-day deaths; ~150 deaths/yr carry it); claim auditor F1 agrees. Score
   effect within noise (+0.0005 AUC), but a confirmed, locatable leak goes even when small.
   Remedy (repair): in _clean blank PRIORLIVE/PRIORDEAD where DPLURAL != 1 and SETORDER_R != 1; add a LEAK-10 bullet.

2. Other post-birth items kept as "at birth" (LEAK-10 Must; LEAK-13 Must).
   Problem/evidence: (a) cyanotic_congenital_heart_disease and the karyotype "confirmed/pending" levels come from
   progress notes and genetic consults until the certificate is filed (worksheet item 37; column auditor A4:
   suspected_chromosomal_disorder confirmed 35.6% died vs pending 12.0%). Task gamer exploit 1: CCHD adds +0.0018 AUC,
   six times the tuned model's 0.0003 random-column spread, the only gain clearly above noise. (b) paternity_acknowledged
   is "signed in the hospital" (claim auditor F2). (c) 2017-2019 birthweight was imputed for linked deaths only; the
   claim "label-free" is refuted (claim auditor F4).
   Remedy (fix the definition): drop CCHD and paternity_acknowledged, collapse confirmed/pending to one "yes" level,
   correct the imputation text (blanking costs nothing: 0.9213/0.9226). The prediction_point text must stop saying
   "anomalies seen at birth" unless these change.

3. The use case names two actors; the data fit one (USE-3 Must, USE-5; PROV-7 for option C).
   Problem: the follow-up/home-visiting screen (Florida's universal screen) is made at registration, for infants alive
   then, with NICU/ventilation/transfer items, and targets post-neonatal deaths, where this model ranks at 0.81-0.83,
   not 0.92 (domain practitioner). The shipped rows match only the expected-deaths actor.
   Remedy: narrow use case and fit text to risk adjustment at the birth (A narrowed); add B (cohort alive at the report)
   as a second folder only if the curator names the registration screen as a distinct actor (precedent checker D1).

4. Metric does not score the named decision (MET-1, MET-8 Must/Should per metrics.md).
   Problem: expected-death counts sum probabilities; ROC AUC ignores calibration (builder's LightGBM under-predicts
   deaths by 13-16% at AUC 0.913-0.917, domain practitioner), and AUC is dominated by first-hour deaths no follow-up
   reaches. Remedy: declare log_loss. Consequence: builder issue 3's keep is stated "while the metric is ROC AUC" and
   carried +1% log loss, so re-measure it under log_loss with several seeds before shipping (point 5).

5. Outcome-marked unknowns kept with a note departs from precedent (LEAK-10 clause 2, LEAK-6 Must).
   Evidence: the column auditor's conditional test confirms the mark is caused by the death (O/E 1.99 mother's education,
   1.89 cigarettes, 1.80 prior births among first-day deaths vs ~1.0-1.2 post-neonatal control); precedent checker D3:
   departs from mic and 2_month_survival (curator moved the prediction point there) with a reason that does not set it
   apart. Remedy: write the distinguishing facts (mark spans nearly every item, cells untraceable, hiding them moves
   nothing) and the test into the note, and confirm "no effect" under the declared metric; if it fails, B of issue 3.

6. Parents' race and Hispanic origin (SEL-1, P1; Tensions row).
   Problem: a newborn's risk score rated partly by parents' race is contested in clinical practice and for a per-person
   service. Evidence: no measured value (builder 0.9148 without vs 0.9149/0.9158; domain -0.0009 AUC, +0.2% log loss);
   column auditor, domain practitioner and builder all recommend B; precedent D5: departs from the batch's method
   without a stated reason. Remedy: drop the four columns.

7. Definition and documentation fixes (quality, CLEAN-*, EV-8, SPLIT-10 notes; not exclusion reasons).
   - mother_age and cigarettes stored as text levels: ship as numbers (blind reviewer; gamer's honest model uses them).
   - months_since_last_live_birth code 3 = plural delivery: recode to missing/0 (CLEAN-10/12).
   - Sampling fraction doubles in 2021 (~6.7% -> ~13.7% of births): state it or use one fraction (blind reviewer).
   - splits_comment: NCHS release lag is 23-29 months, not "about two years" (split auditor finding 1).
   - Seed spread cited as 0.001 is 0.004 for the builder's model (domain practitioner); restate the "no change" claims.
```

</details>
