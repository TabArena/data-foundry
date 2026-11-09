# ny_wcb_assembled_claims

**Outcome:** added as `ny_wcb_assembled_claims_1m`. Changed against the draft the panel reviewed: 11 of its 17 features
dropped as values the table stores after assembly (the three injury codes, industry, age, accident date, home ZIP, fee
region, district, insurer name and type), leaving 6; history from 2016 instead of 2015; `fit_reason` rewritten (inputs
the desk holds are missing, the label is the type to date, the task was changed a lot to avoid a leak); the June 2021
Kaggle copy not added. The AI recommends shipping it as it now stands: the panel's changes are made, the insurer's drop among them (the rule's default), and issues 1 to 3 confirm what is implemented. The task:
when New York's Workers' Compensation Board assembles a claim, which of seven benefit types will the claim end with
(Open NY table, 2026 snapshot). 1,152,698 claims assembled 2016-2019 with six features (claim type, county, sex, the
assembly date, and the C-2 and C-3 dates when they arrived by assembly); three four-month test windows of 2019 (97,676 to
101,201 claims each), each trained on up to 1M earlier claims; fallback `log_loss`. Every other field of the table goes, as set after assembly or
as stored at a value filled or changed later on claims that grew, so the task is thin.
Verdict: ship after changes (made).
Validity: SEL-1 holds (no New York rule found bars sex in claim handling; issue 2); USE-1 holds, USE-8 approximate (the
desk's inputs at assembly are not published, the label is the type to date, the task was changed a lot to avoid a leak;
`fit_reason` rewritten); USE-12 keeps the task; LEAK-10 triggered and fixed: 28 post-assembly columns dropped and the
C-2/C-3 dates after assembly blanked (builder), and under clause 2 the three WCIO codes, industry, age, accident date,
ZIP, fee region and district dropped (each with a traced gain above 2 SE, in all three designs or, for the last two, in
two), with the insurer's name and type (issue 1); the six remaining fields kept under the clause-2 note (issue 3: C-3
borderline, C-2 untraceable); LEAK-24 met by the 2020 cut, the residual noted (about 12-13% of the test windows' PPD
NSL and PTD awards still to come); SPLIT-1, -9, -10 and -14 hold; SPLIT-20 applied (history from 2016).
Value: TP-2, a small real signal: the task probes flag nothing; a linear model beats the class shares on 3 of 3
windows by 0.042 log loss (SE 0.001, 4.0%), the mediator's LightGBM by 0.035-0.037 (3.2-3.5%); the probes' untuned
LightGBM gains only 0.9% (std 0.011 over the windows; unstable on the rare classes) and a random forest is 7.2% worse
than the class shares; every class is in every test window
(smallest 38 rows, TP-8).
Quality: NON-WC decoded (CLEAN-12); the accident-date reason (LEAK-10/LEAK-7, not CLEAN-11), the C-2 definition, the
label-maturity wording, the sex note and the counts corrected.
Weighed: size +, source + (the Board's table with a codebook and FAQ), gap + (insurance, multiclass), use case 0 (ours,
approximate), risk - (a thin task; the label to date).
For the curator: issue 1 (the insurer: ship the thin task, retire, or amend the rule), issue 2 (sex, decided with
rais_employment_separation issue 1), issue 3 (the six fields kept under the note). Proposed, not yet written into
`dataset.py`: accept the two duplicate-row warnings, with the text for `dataset_duplicate_rows`: "60.3% of the rows repeat an earlier row, label included: six
coarse fields (claim type, county, sex, assembly day, form dates by assembly) cannot tell different claims apart; no
test row repeats a training row, as the assembly date differs between a window and its train side", and for
`dataset_conflicting_duplicate_rows`: "14.9% of the rows share all features with a claim of another class: different
claims the six coarse fields cannot tell apart, the limit of a triage without the injury, employer and insurer". The
June 2021 copy of the table (Kaggle) is not needed and is not added as a second raw file: its insurer spellings carry
more of the outcome than the 2026 ones (+0.016 to +0.020 log loss beyond the merged insurer, against +0.005 to +0.006),
and after the drops it would restore only 259 cells of the kept fields (0.02%, a score change of 0.0003). The builder's draft
asked for your OK to add it; it is not needed.

**Main points:** Three calls, each confirming what is implemented, and one OK: drop the insurer and ship the thin task (issue 1;
retiring the dataset or amending the rule are the other options); keep sex (issue 2, with rais_employment_separation
issue 1); keep the six remaining fields with a note (issue 3); and your OK on the two duplicate-row warnings (texts in the outcome, not yet
in `dataset.py`).

**Record fields that disagree with the definition:**

- `year`: record `(none)`, definition `2026`.
- `problem_type`: record `(none)`, definition `Multiclass Classification`.

**Record judgment:** valid. A state agency's own table with a codebook and an FAQ, every column defined; the use case is
ours (the Board names no prediction). The screening's 8-class target is 7 classes once the CANCELLED claims leave, and
its use case ("from what the first reports hold") is now the insurer's lost-time desk with a thin input set: the table
stores most of what the first reports hold at values filled or changed later, so those fields leave.

**Issues for Lennart:**

1. **Drop the insurer and ship the thin six-field task, as now?**

   * **Problem:**
     - The insurer is a fact at assembly, but the table stores what the claim's latest filing wrote, and on claims seen weeks after assembly its 2026 values predict the outcome better than its values then, by more than two standard errors however the same claims are split for the test[^l10].
     - Your rule sends such a field out by default, which the definition now does; what is left (claim type, county, sex and three dates) is thin: the best untuned model (linear) is 4.0% better than predicting the class shares on every window, an untuned LightGBM only 0.9%, the mediator's LightGBM 3.2-3.5%[^tp2].
     - So the choice is to ship this thin task, to retire the dataset as no fair picture of a triage desk, or to amend the rule, which you declined for this mechanism on 2026-10-21[^prec].
   * **Background:**
     - The table keeps no history. Its stored insurer changes when a later filing fills a blank on a claim that progressed, when a special fund takes a claim over after an award, and when a spelling is rewritten on a claim with later filings: after June 2021, 66,256 of the 73,382 name changes on the 2016-2019 claims are such rewrites, and they are 31.9% NON-COMP against 64.6% of all claims.
     - The "matched test" scores the same 105,786 claims of January-June 2021 against their 2026 labels twice: with a model trained and tested on the values of a June 2021 copy of the table (weeks to months after assembly), and with one trained and tested on the 2026 values. The difference is what the later values add, as a lower bound. Three designs: train January-March and test April-June (over time), at random within April-June (at equal age), at random within January-June.
     - "Merged" joins the spelling variants of one insurer (spellings linked by a claim that changed name, sharing the first word).
   * **Effect on the task:** with the insurer, a model is credited for spellings and fills that follow the claim's later course; without it, the task is a triage on six coarse fields a desk does hold, but without the injury, the employer or the insurer, the inputs it reads first.
   * **Experiments:**
     - Matched test, 3 seeds, gain of the 2026 values (SE): the merged insurer name +0.0068 (0.0010) over time, +0.0074 (0.0018) at equal age, +0.0043 (0.0010) at random; the insurer type +0.0036, +0.0023, +0.0027 (z 7.2, 2.6, 5.3). The spelling alone is worth +0.005 to +0.006 beyond the merged insurer with the 2026 names, and +0.016 to +0.020 with the June 2021 names.
     - The 2019 windows (300k random earlier training claims, untuned LightGBM, one seed; log loss):

       | Features | Sep-Dec | May-Aug | Jan-Apr |
       |---|---|---|---|
       | class shares | 1.055 | 1.060 | 1.076 |
       | as shipped, no insurer | 1.019 | 1.022 | 1.041 |
       | with the merged insurer | 0.971 | 0.980 | 1.004 |
       | with the insurer as published | 0.965 | 0.973 | 0.998 |

     - Task probes on the shipped task (3 windows, up to 200k training claims, untuned; gain over the class shares as a share of their log loss): linear 4.0% (0.042 log loss, SE 0.001, 3 of 3 windows); LightGBM 0.9% (std 0.011 over the windows); a random forest 7.2% worse; the best single field, the C-3 date, 2.5%; no probe flags. The probe's LightGBM falls behind the mediator's 3.2-3.5% because an unregularised LightGBM is unstable on the rare classes (task gamer).
   * **Consistency:**
     - distribution_transformers_at_cauca_department dropped its looked-up rating and installation type at a cost of ROC AUC 0.701 to 0.639, and kumc_inpatient_aki_prediction in this batch drops 26 procedure groups on gains of 0.003 and 0.004; this drop follows both[^prec].
     - forest_fires shipped at R² 0.013 and noaa_storm_events_damage with a low ceiling: a small signal without a leak has not been a reason to retire[^tp2]; retiring for this reason would be the first use of `Not Representative` of its kind[^nr].
     - The injury, industry, age, accident date, ZIP, fee region and district left on the same test as changes needing no decision; the insurer is put to you only because its drop leaves a thin task.
   * **Panel:**
     - Neither the advocate nor the critic argued about the insurer: both read its changes as spelling and kept it under the note; the mediator's tests then found its gain and that the spellings carry it.
     - For shipping a task at all (advocate): a leak is no reason to reject a real task, and a small real signal is no reason to retire; for the drop (critic): the rule's text and the transformers precedent, and the size of a gain never decides.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Drop the insurer, ship the thin task (implemented) | carrier name and type out; six features; fit approximate as a task changed a lot to avoid a leak | follows the rule and every precedent; a triage without a leak; a small real signal on all three windows | only 4.0% below the class shares at best, 0.9% for an untuned LightGBM; no injury, employer or insurer; 60% exact duplicate rows |
     | B | Drop the insurer and retire as `Not Representative` | the record gets `No`; the folder leaves the working copy | no benchmark of a triage without its core inputs | the first use of the marker for this reason; a small signal without a leak is no reason to retire; loses the only claims-triage task of the thin insurance domain |
     | C | Amend the rule and keep the merged insurer | a field the actor records at the prediction point stays with a note when the snapshot holds a later rewrite; the insurer ships with its spellings merged | keeps about 0.05 log loss of skill; the insurer exists at assembly | almost every looked-up attribute would qualify; you declined this on 2026-10-21; the spelling map needs the June 2021 copy as a second raw file or a cruder normaliser of our own |

   * **Recommendation:** A, the rule's default and the transformers precedent: a small signal without a leak is no reason to retire, and the six fields still beat the class shares on every window (linear 4.0%). B if you judge a triage without the injury, the employer and the insurer to be no fair picture of the task. **Decision:** A, B or C?

   **Notes for the AI:**
   - A: a `CC` line in the record; nothing else.
   - B: the record's `suggestion` to `No` with the marker `Not Representative` and a `CC` line with the reason; remove the folder from the working copy with a CHANGELOG entry (the REVIEW.md stays in git history).
   - C: write the amendment into LEAK-10 clause 2 (`leak_checks.md`) with its case row; add the June 2021 Kaggle copy (new-york-state/nys-assembled-workers'-compensation-claims) as a pinned second raw file (version, sha256, download line) and build the spelling map as the mediator's E4 did (spellings linked by a claim that changed name and share the first word); take `carrier_name` (merged, 2026 values) and `carrier_type` out of `LATE_VALUES`; set "*** CARRIER UNDETERMINED ***" and UNKNOWN to missing and the funds that take a claim over after an award (2B ATF, 5A, 5B; FAQ 11) to missing; note 5D SPECIAL FUND - UNKNOWN (143 claims moved there after June 2021); rewrite the insurer bullet, `known`, `changes` and `fit_reason`; re-run `dataset check`, the leak and task probes.

   [^l10]: **LEAK-10** (Must), clause 2 (amended 2026-10-26, Lennart): values read at a later pull whose late cells cannot be located row by row "go when they may carry a gain ... and stay with a note only when the part that can be traced shows none"; a case-by-case call. A Must takes no exception, only an amendment (principles.md, "Exceptions and amendments").
   [^tp2]: **TP-2** (Should): a small but real signal is no reason to retire (forest_fires, R² 0.013). **USE-12** (Must): a leak is no reason to reject a task whose use case is real. **USE-8** (Must): approximate covers "a task changed a lot to avoid a leak" (house_sales, sarcoma).
   [^prec]: distribution_transformers_at_cauca_department, CC 2026-10-21 (Lennart): "LEAK-10 stays as written ... power_kva and installation_type stay dropped"; kumc_inpatient_aki_prediction, mediator 2026-11-09 (AI); X4 (2026-11-08, Lennart, noaa_storm_events_damage): the size of the worth alone never decides. **LEAK-13** (Must) would apply under C: a class-linked recording convention (the spellings) is harmonised.
   [^nr]: `Not Representative` (selection.md, markers): the task or its setup does not represent the real application. The precedent checker found no case retired under it for a thin task.

2. **Keep the worker's sex as a feature, as now?**

   * **Problem:**
     - Your stance drops sex from every insurance pricing task, and in this batch rais_employment_separation issue 1 asks you to extend it to any decision where the actor's own law bars the factor[^row][^rais].
     - Two agents read the law: no New York rule found bars sex in claim handling, since Insurance Law s2607 covers issuing, cancelling and renewing the policy (here the employer's), DFS Circular Letter 7 (2024) leaves out every phase but underwriting and pricing, and the EU directive the stance follows excludes employment[^law].
     - So sex stays under the stance as written and as extended, and the definition keeps it; decide it with rais issue 1.
   * **Background:**
     - The injured worker is a claimant, not the policyholder, and routing a claim sets no premium and no benefit: the Board sets the benefits by statute.
   * **Unknown:** whether New York's Human Rights Law reaches a state agency's internal routing. The definition names the insurer's lost-time desk as the actor, which avoids the question.
   * **Effect on the task:** on the six shipped fields, without sex the log loss rises by 0.0044, 0.0030 and 0.0035 on the three windows (SE 0.0003; 300k training claims, 3 seeds), about a tenth of the task's skill; on the full field set before the drops it moved by -0.0005 to +0.0017.
   * **Consistency:**
     - bemtpl97, australian_vehicle_insurance_2004_2005 and the other insurance pricing tasks dropped sex; wioa_employment_after_exit and rais_employment_separation drop the grounds their actors' own laws bar.
     - home_credit_default_risk and credit_card_clients_default keep sex, marked as not reviewed yet.
   * **Panel:** every agent that looked (claim auditor, domain practitioner, advocate, critic, mediator) agrees: keep, decided together with rais issue 1.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep sex (implemented) | gender stays a feature; the note gives the law read | no law of the actor bars it; consistent with the stance as written and as rais would extend it; a real signal | a routing that treats men and women differently is close to the stance's concern; the Human Rights Law question stays open |
     | B | Drop sex | gender leaves the features | the cautious line for any insurance task | no fact of the actor's law behind it; costs about a tenth of a thin task's skill |

   * **Recommendation:** A: no law of the actor bars sex here, so it stays under the stance as written and as extended; B only if you want sex out of every insurance task whatever the law. **Decision:** A or B?

   **Notes for the AI:**
   - A: a `CC` line; with rais issue 1's decision, the Tensions row's cases gain "ny_wcb_assembled_claims: sex kept in a claim-routing task; no New York rule bars it (2026-11-09 law read)".
   - B: drop `gender` in `_clean` with its reason, remove its `set_missing` entry and its feature type, update `known` and the sex note; re-run `dataset check`, the leak and task probes.

   [^row]: principles.md, Tensions, "A rating factor known at the prediction point against a factor the actor may no longer use" (P3 and P4; **USE-1**, **USE-6**), amended 2026-11-08 (Lennart): sex leaves every insurance pricing task, "as if we were to simulate the case in europe always"; bemtpl97, CC 2026-11-05. **SEL-1** (Must): a task with ethical concerns is out.
   [^rais]: rais_employment_separation, REVIEW.md issue 1 (open): the stance extended to any decision on a person where the actor's own law bars the factor (Lei 9.029/1995 art. 1).
   [^law]: NY Insurance Law s2607 (https://www.nysenate.gov/legislation/laws/ISC/2607); DFS Insurance Circular Letter No. 7 (2024), para. 8: "not intended to address phases of the insurance product lifecycle other than underwriting and pricing" (https://www.dfs.ny.gov/industry-guidance/circular-letters/cl2024-07); Directive 2004/113/EC, Art. 3(4) and recital 15 (https://eur-lex.europa.eu/eli/dir/2004/113/oj/eng).

3. **Keep the six remaining fields with a note, as now, although they too are 2026 values?**

   * **Problem:**
     - The six remaining fields are also their values in the 2026 snapshot, and your rule keeps such fields with a note only when the part that can be traced shows no gain[^l10b].
     - On the matched 2021 claims their 2026 values beat their values weeks after assembly by +0.0006, +0.0003 and +0.0008 log loss in the three designs, within two standard errors (z 1.7, 0.3 and 1.9).
     - Two of them are less clear: the C-3 date is borderline (z 1.3 to 3.3 by design and field set), and the C-2 date cannot be traced, as the June 2021 copy used an older definition of it.
   * **Background:**
     - Among the 105,786 matched claims, 131 C-3 dates on or before assembly first appeared after June 2021; those claims ended 19% NON-COMP and 31% PPD SCH LOSS.
     - Tables published from 2022 define the C-2 date as the earliest equivalent filing, eClaims included, and apply that to older claims; the June 2021 copy filled it for 0.2-0.7% of young claims.
     - As a check of the noise level, swapping fields that did not change between the two copies (claim type, county, C-2, the assembly day) gives -0.0001 to -0.0002.
   * **Effect on the task:** at most about 0.001 of the task's 0.035 log loss of skill can rest on later values, most of it in the C-3 date; dropping the C-3 date costs 0.015 to 0.017 log loss on the three windows (SE 0.0007; 300k training claims, 3 seeds), almost half the task's skill, and loses whether the worker's claim form had arrived by assembly, which the desk knows. The C-3 date is also the probes' best single field (2.5% over the class shares alone, chosen on 3 of 3 windows).
   * **Experiments:** the mediator's matched test, 3 seeds; one field swapped to 2026 on the panel's post-drop set (over time / equal age / at random): C-3 +0.0014 (z 3.3) / +0.0013 (1.3) / +0.0009 (2.0); county +0.0004 / -0.0004 / +0.0003; on the shipped set the C-3 swap stays within two standard errors in all three designs.
   * **Consistency:** onlinenewspopularity and medical_facility_operational_data kept late values with a note because the traced part showed no gain; tunisian_fraud_detection_challenge kept registry fields where no mechanism ties a change to the outcome[^keep].
   * **Panel:**
     - Keep (advocate): the one-field swaps of these fields show no gain.
     - Measure the shipped set first and drop what carries the rest (critic); the mediator did: the rest sat in the insurer, the fee region and the district, now dropped, and these six show none.
   * **Unknown:** a second matched sample, a copy of the table taken soon after another batch of assemblies (the 2023 Kaggle copies were never checked), or more seeds would settle the C-3 date.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep all six with the note (implemented) | as now; the note names the C-3 date as borderline and the C-2 date as untraceable | the trace shows no gain at two standard errors; the desk holds these at assembly | the C-3 date is a maybe; the C-2 date cannot be checked |
     | B | Drop the C-3 date | `c3_date` leaves; five features | removes the borderline field | loses a fact the desk holds; almost half the task's skill (0.015-0.017) |

   * **Recommendation:** A: the trace shows no gain at the rule's bar, and the C-3 date is a fact the desk holds at assembly; B if you read "maybe a leak" as enough under a Must. **Decision:** A or B?

   **Notes for the AI:** B: add `c3_date` to `LATE_VALUES` with its reason, take it out of `DATE_COLUMNS` and step 5 of `_clean`, update `known` and the potential-leak bullet, and remove the C-3 row from decision 2's text; re-run `dataset check`, the leak and task probes.

   [^l10b]: **LEAK-10** (Must), clause 2 (amended 2026-10-26, Lennart): late values that cannot be located row by row "stay with a note only when the part that can be traced shows none"; a case-by-case call of the curator. **EV-6**: a mechanism without a measured effect is "maybe a leak".
   [^keep]: onlinenewspopularity, CC 2026-10-26 (Lennart, "go with (a)"): masked R² change -0.0004; medical_facility_operational_data, CC 2026-11-05 (Lennart): the worth within two seed SDs; tunisian_fraud_detection_challenge, CC 2026-11-05 (Lennart).

**Review panel:** ship after changes (mediator). Full panel, on the builder's draft (17 features, the late fields and
the insurer kept under the clause-2 note, history from 2015): the claim auditor, the column auditor and the precedent
checker each found that keep against the rule's default; the split auditor: right with notes (history start to
settle); the domain practitioner, the blind reviewer and the task gamer as below. Then the advocate and the critic with
one rebuttal each, and the mediator, who ran the matched test on the panel's post-drop set (each block of fields swapped to
its 2026 values, three designs, 3 seeds), the residual of the kept fields field by field, the insurer's spellings and
what each option leaves on the 2019 windows. The mediator's issues 1, 2 and 3 are issues 2, 1 and 3 here; its issue 4
(the June 2021 copy as a second raw file) is settled: not needed. Claims: 37 audited; 32 hold, 1 holds approximately
(benefit types that have "settled", reworded), 1 untested (the birth year), 3 refuted and now moot or fixed (keeping
the 2026 values with a note, blanks as facts at assembly, the fee region's codes). Blind review: include with changes;
its main concerns were the rows missing against the source (the `_1m` row budget) and fields stored at snapshot time.
Task gamer: no exploit beyond seed noise; its kit held only 2026 values, so it could not see the late-value leak.
Agreed: drop the three WCIO codes, industry, age, accident date and ZIP; history from 2016; the 2020 cut with no gap and
the residual in the notes; `fit_reason` rewritten; sex kept. Disputed: the bar for a field's return (settled: none
returns under either side's bar), the residual of the kept fields (settled: the insurer, the fee region and the
district carry it; the last two dropped, the insurer is issue 1), the C-3 date (issue 3).

<details><summary>Mediator</summary>

```text
MEDIATOR REPORT: ny_wcb_assembled_claims (folder ny_wcb_assembled_claims_1m), 2026-11-09

Read: principles.md; leak_checks.md (LEAK-6, -7, -10, -11, -13); provenance.md (PROV-8, -13, -14); splits.md (SPLIT-20,
-21); use_case.md (USE-8); evidence.md (EV-1, -6 to -9); review_panel.md; dataset.py; the record; builder_report.md; the
seven phase-A reports; both briefs and both rebuttals. My runs (untuned LightGBM with the claim auditor's settings,
4 threads; scripts in the run folder):
  E1 e1_matched.py, E6 e6_residual_minimal.py, E7 e7_carrier_alone.py: the claim auditor's matched test (105,786 claims
     of January-June 2021; train and test both on June 2021 values or both on 2026 values; same 2026 labels; three
     designs; row losses averaged over 3 seeds; row-bootstrap SE). Rule fixed before the run: a field shows a gain when
     it exceeds 2 SE in a design; it shows none when it stays within 2 SE.
  E2 e2_restore.py, E4 e4_carrier_spelling.py, E8 e8_options.py: the shipped claims (2016-2019, 1,152,698), the three
     2019 windows, 300k random earlier training claims; 2 seeds (E2, E4), 1 seed (E8).
  E3 e3_transitions.py, E4b e4b_groups.py, E5 e5_c3_district.py: what the late changes are.

======================================================================================================================
1. RECOMMENDATION (judgment record)
======================================================================================================================
Verdict: ship after changes.
Validity: SEL-1 holds (no New York rule found that bars sex or age in claim handling; sex decided with rais issue 1,
  issue 1); USE-1 holds, USE-8 approximate (inputs the actor holds at assembly are not published, the label is the type
  to date, the task was changed a lot to avoid a leak): fit_reason rewritten; USE-12 keeps the task; LEAK-10 clause 2
  triggered: the three WCIO codes, industry, age, accident date, ZIP, medical fee region and district dropped (each
  shows a traced gain above 2 SE); the insurer fields show one too (issue 2); the rest stays under the clause-2 note
  (issue 3); LEAK-13 applies to the insurer's spellings if the insurer is kept; LEAK-24 met by the 2020 cut, residual
  in the notes; SPLIT-1, -9, -10, -14 hold; SPLIT-20: history from 2016.
Value: TP-2, a small real signal: without the insurer about 0.035 log loss below the class shares on the 2019 windows
  (3.2-3.5%), with it 0.072-0.085 (E8, one seed). Task probes to re-run on the changed set.
Quality: the agreed CLEAN-11/-12 fixes are moot for the dropped columns; notes corrected; `NON-WC` decoded.
Weighed: size +, source +, gap + (insurance multiclass), use case 0 (ours, approximate), risk - (a thin task once the
  late fields are out; label to date).
For the curator: issue 1, sex (with rais issue 1); issue 2, the insurer fields (the rule drops them; then ship a thin
  task or retire, or amend LEAK-10); issue 3, keep the remaining fields under the clause-2 note (C-3 borderline, C-2
  untraceable); issue 4, the June 2021 copy as a second raw file (no longer needed if issue 2 drops the insurer).

======================================================================================================================
2. THE DISPUTED POINTS, SETTLED
======================================================================================================================

(1) The field-return test: can industry, age, accident date or ZIP come back? [P4, LEAK-10 clause 2 Must; LEAK-6 Must]
- Both sides rest on the same rule; this is a dispute about its test, not a conflict of rules.
- Decisive experiment (E1 part B, the critic's design: the post-drop set plus the block, all at June 2021 values, the
  block swapped to its 2026 values; three designs; paired by row; 3 seeds). Gain of the 2026 values, SE, z:
      block                         time (train Jan-Mar)      iid Apr-Jun (equal age)   iid Jan-Jun
      industry                      +0.0087 (0.0008) 10.8      +0.0084 (0.0018) 4.7      +0.0066 (0.0008) 8.1
      age + accident date           +0.0069 (0.0009)  8.1      +0.0072 (0.0016) 4.5      +0.0059 (0.0009) 6.9
      ZIP, fee region with it       +0.0074 (0.0012)  6.2      +0.0094 (0.0026) 3.6      +0.0039 (0.0014) 2.7
      ZIP alone                     +0.0094 (0.0013)  7.4      +0.0111 (0.0025) 4.4      +0.0055 (0.0014) 3.8
- Ruling: every block shows a gain in every design, the advocate's equal-age design included. None returns under
  either side's bar. Change now, no decision.
- For the record, on the bar the sides disputed: the clause keeps a value "only when the part that can be traced shows
  none", so the burden is on the keep (critic; the advocate conceded the default). The clause states a gain test, so a
  mechanism alone does not bar a field (advocate; onlinenewspopularity, medical_facility_operational_data). The time
  design overstates a swap: its June 2021 arm trains on values older than it tests on, and a swap also removes that
  field's mismatch. So "shows none" means within 2 SE in both iid designs, with the time design as an upper bound.

(2) The kept fields' residual [P4, LEAK-10 clause 2 Must]
- Agreed by both: measure field by field, drop what carries the gain. Settled by fact.
- The residual replicates (E1, post-drop set): +0.0096 (SE 0.0015) time, +0.0026 (0.0029) equal age, +0.0067 (0.0016)
  iid Jan-Jun.
- Leaving one group out does not remove it: without the insurer (name and type) +0.0063 / +0.0029 / +0.0058; without
  the fee region +0.0059 / +0.0036 / +0.0056; without the district +0.0087 / +0.0003 / +0.0048; without the insurer and
  the fee region +0.0027 (0.0005) / +0.0035 (0.0010) / +0.0032 (0.0006).
- Without the insurer, the fee region and the district it is gone (E6): +0.0006 (0.0004) / +0.0003 (0.0008) / +0.0008
  (0.0004), z 1.7 / 0.3 / 1.9. Calibration on fields with no late part (claim type, county, C-2, day): -0.0001 / -0.0002
  / -0.0002.
- One field swapped to 2026 on the post-drop set (gain, z; time / equal age / iid Jan-Jun):
      carrier type        +0.0036 7.2 / +0.0023 2.6 / +0.0027 5.3   (its blank: 0.76% of claims near assembly at 59%
                                                                     NON-COMP, 0.37% in 2026 at 96%)
      district            +0.0019 4.8 / +0.0010 1.2 / +0.0016 3.7   (real moves to another district, about 0.4% of
                                                                     claims, 12-29% NON-COMP; the moves between NYC,
                                                                     Albany and Long Island 43-51% PPD SCH LOSS)
      fee region          +0.0030 5.8 / -0.0003 -0.3 / +0.0013 2.2  (follows the home ZIP; every one of its 11,024
                                                                     post-2021 changes comes with a ZIP change)
      C-3 by assembly     +0.0014 3.3 / +0.0013 1.3 / +0.0009 2.0   (131 C-3 dates on or before assembly that appeared
                                                                     after June 2021: 19% NON-COMP, 31% PPD SCH LOSS)
      county              +0.0004 1.1 / -0.0004 -0.6 / +0.0003 0.9
- The insurer name alone on the minimal set (E7), with its spelling variants merged (spellings linked by a claim that
  changed name and that share the first word): +0.0068 (0.0010) 7.0 / +0.0074 (0.0018) 4.1 / +0.0043 (0.0010) 4.4.
  Unmerged: +0.0028 1.9 / -0.0024 -0.9 / +0.0032 2.1; the raw June 2021 spellings carry a signal of their own (below).
- Ruling: the residual sits in the insurer, the fee region and the district, and each shows a gain in an iid design.
  By the clause's default they go. Fee region and district: change now (county_of_injury, unchanged, keeps the
  geography at assembly; the fee region is mapped from the ZIP that goes; together they cost about 0.004-0.005 log
  loss, E8). The insurer: issue 2, because its drop leaves a thin task and opens a weighing the rules leave open.
- C-3: borderline (z 1.3 to 3.3 by set and design; within 2 SE on the minimal set in all three designs). Kept under the
  note as "maybe a leak" (EV-6), issue 3. Sex and claim type show nothing; C-2 cannot be traced (the June 2021 copy
  uses the pre-2022 definition).

(3) If the curator declines the second raw file: what happens to the insurer name and the fee region?
- New facts (E2, E3, E4, shipped 2016-2019 claims):
  * The post-June-2021 insurer-name changes are spellings rewritten on claims with later filings: 66,256 of the 73,382
    changes fall in insurers where under half the claims changed, and they are 31.9% NON-COMP against 64.6%.
  * Restoring the June 2021 values does not lower the score; it raises it: restored minus 2026 log loss -0.0087,
    -0.0121, -0.0165 (SE <= 0.001) on the three windows, 97% of it from the insurer and the fee region.
  * The cause is the spelling. The worth of the raw spelling over the merged insurer is +0.0052 to +0.0064 with the
    2026 names and +0.0157 to +0.0198 with the June 2021 names. Merged, the two snapshots agree on 99.2% of claims and
    differ in score by 0.0017-0.0037. So the June 2021 copy is no repair for the insurer name: its spellings carry about
    three times the 2026 spellings' signal. The agreed "restore each field whole from June 2021" must not be applied to
    the insurer name.
- Ruling:
  * Fee region: goes either way (point 2); the file does not change that.
  * Insurer name: goes by default (issue 2). If the curator keeps it by an amendment, it ships at its 2026 values with
    the spellings harmonised (LEAK-13, Must: a class-linked recording convention is harmonised). The map needs the June
    2021 copy, or a string normaliser of our own that will merge fewer variants. The post-2021 changes that cannot be
    located without the file show no gain on the shipped windows (merged 2026 scores 0.0017-0.0037 worse than merged
    June 2021), so they stay under the clause-2 note.
  * The advocate's "the rule's default is the blank" does not hold. A blank needs the file to locate the cells, and it
    would mark the outcome: a blank in place of the changed names would form a pool 34% NON-COMP against 64.6% (LEAK-10,
    "missingness that encodes the outcome"). The critic's "or the curator records the departure" is not open either: a
    Must has no exceptions, only amendments.
  * After the drops the copy would restore only 259 cells of the kept fields (sex 191, C-3 39, claim type 18, county 11;
    0.02%), which change the score by 0.0003. It is not worth a second raw file (issue 4).

======================================================================================================================
3. CHANGES TO MAKE NOW (no decision needed)
======================================================================================================================
1. Drop wcio_cause_of_injury, wcio_nature_of_injury, wcio_part_of_body, industry, age_at_injury, accident_date and
   zip_code (LEAK-10 clause 2, Must; the field-return test above: none returns).
2. Drop medical_fee_region and district_name (LEAK-10 clause 2, Must; traced gain, point 2).
3. HISTORY_START = 2016-01-01 (SPLIT-20, Should; the EDI ramp; the oldest pool becomes 74.1%); the task summary's years
   and the Decision 1 text follow.
4. Rewrite fit_reason (USE-8, Must). The actor is the carrier's lost-time desk or the Board's examiner. The gaps are:
   the inputs held at assembly that the table does not publish (the reason for assembly, the reported wage and lost
   time, the carrier's denial, the occupation, the narrative, the C-4, the attorney at assembly); the label to date; and
   a task changed a lot to avoid a leak (injury, employer, worker's age, home ZIP and district dropped). Update
   use_case, task_summary.known and task_summary.changes to match.
5. Label maturity (LEAK-24 met, notes only): reword "settled"/"settling" (Decision 1 title, task_summary.changes) and
   give the residual (about 12% of PPD NSL and 13% of PTD awards still to come for the 2019 claims). In
   splits_comment: 12-14% of each training side's labels changed after the window start; the gap ladder rises about
   0.001 per month with no step at the window edge; why no gap (SPLIT-10).
6. Rewrite the "Potential leak, kept on purpose" bullet with the matched numbers. On the full set the 2026 values beat
   the near-assembly values by 0.030-0.037. The dropped fields and their traced gains (point 1, point 2). What stays,
   with its trace and the C-3 borderline (issue 3). C-2 is untraceable (2022 redefinition, applied backwards in the 2026
   table). The insurer per issue 2.
7. Notes: the occupational-disease count 14,466 (code comment 14,488); the sex note's reason replaced by the facts read
   (s2607, DFS Circular Letter 7 (2024) para. 8, Directive 2004/113/EC Art. 3(4)), pending issue 1. Remove the bullets
   made moot by the drops: accident dates after assembly, ZIP, codes and words, fee region UK, age 0, and the 5D and
   VIRTUAL ONLY lines. CLEAN-12 (Should, cheap): decode claim_type NON-WC as the codebook's World Trade Center
   volunteer claims (FAQ 8).
8. Do not restore any field from the June 2021 copy (point 3; issue 4).
9. Re-run dataset check, the leak, dtype and task probes after the changes, and regenerate the README (verification;
   TP-1 to TP-3 on the thinner task).

======================================================================================================================
4. ISSUES FOR THE CURATOR (rank order)
======================================================================================================================
1. [P1, SEL-1 Must; Tensions row "a factor the actor may no longer use"] Sex stays a feature?
   - Effect: dropping it moves log loss -0.0005 / +0.0017 / +0.0013 on the full set (domain practitioner); not
     measured on the thinner set.
   - Facts read by two agents: NY Insurance Law s2607 covers issuing, cancelling and renewing the employer's policy;
     DFS Circular Letter 7 (2024) excludes phases other than underwriting and pricing (para. 8); Directive 2004/113/EC
     excludes employment (Art. 3(4)). No New York rule found that bars sex in claim handling. Open: whether the Human
     Rights Law reaches the Board's internal routing, avoided by naming the carrier as the actor.
   - Advocate and critic agree: keep, decided together with rais issue 1.
   - Decision: keep on the fact read (recommended under both the current row and the rais extension), or drop.

2. [P4, LEAK-10 clause 2 Must; then a weighing: TP-2, USE-8, USE-12] The insurer fields (carrier_name, carrier_type)
   show a traced gain. The rule drops them; then ship a thin task, or retire, or amend the rule?
   - Problem: the insurer is a real fact at assembly, but every snapshot stores what the claim's latest filing wrote:
     blanks filled for claims that progressed, transfers, and spellings rewritten on active claims. Traced gain:
     merged name +0.0043 to +0.0074 (z 4.1-7.0, all three designs); carrier type +0.0023 to +0.0036 (z 2.6-7.2). The
     spelling alone is worth +0.005-0.006 beyond the merged insurer with the 2026 names, +0.016-0.020 with the June
     2021 names.
   - Effect (E8, log loss; class shares 1.055 / 1.060 / 1.076): post-drop set as agreed 0.960 / 0.969 / 0.993; with
     the insurer, without fee region and district 0.965 / 0.973 / 0.998 (raw), 0.971 / 0.980 / 1.004 (merged);
     without the insurer 1.019 / 1.022 / 1.041 (skill 0.035-0.037, 3.2-3.5%).
   - Advocate's best evidence (for keeping a task): USE-12 and TP-2 (forest_fires at R^2 0.013); retirement has no
     marker (precedent checker D2). Neither side argued the insurer's drop: both took its changes as spelling.
   - Critic's best evidence (for the drop): the clause's text; distribution_transformers_at_cauca_department (dropped
     at ROC AUC 0.701 to 0.639, amendment declined 2026-10-21); X4 (size never decides).
   - Options:
     (a) Drop both fields and ship the thin task, fit approximate (rule's default; recommended). Re-run the task
         probes first.
     (b) Drop both fields and retire as `Not Representative`: a triage benchmark with none of the injury, the insurer,
         the employer or the worker's age. This would be the first use of the marker for this reason.
     (c) Amend LEAK-10 clause 2 to keep a field the actor records at the prediction point when the snapshot holds a
         later rewrite: ship the merged insurer (LEAK-13) with a note giving the traced gain. Almost every looked-up
         attribute would qualify, and you declined this on 2026-10-21.
   - What would settle (a) against (b): the task probes on the thin set (does it rank tuned methods apart across the
     three windows, TP-1 to TP-3).
   - Decision: a, b or c.

3. [P4, LEAK-10 clause 2 Must, a case-by-case keep] Keep claim type, county, sex, the C-2 and C-3 dates on or before
   assembly, and the assembly date under the clause-2 note?
   - Facts: on these fields the 2026 values beat the June 2021 values by +0.0006 / +0.0003 / +0.0008 (z 1.7 / 0.3 /
     1.9), so the trace shows none at 2 SE. C-3 holds most of it: its swap shows z 2.0-3.3 in some sets (131 late
     records in 105,786 claims), so it is "maybe a leak". C-2 cannot be traced: the June 2021 copy uses the pre-2022
     definition.
   - What would settle C-3: a second matched sample, from a copy of the table taken soon after another batch of
     assemblies (the 2023 Kaggle copies were never checked), or more seeds.
   - Decision: keep all with the note (recommended; C-3 and C-2 named in it), or drop C-3.

4. [P5, PROV-13/PROV-14; house rule on raw files] Add the June 2021 copy as a second raw file?
   - After change 2 and issue 2 (a), it would restore 259 cells (0.02%, score change 0.0003). It is no repair for the
     insurer name (point 3).
   - Decision: do not add it (recommended), or add it pinned (Kaggle version, sha256, download line) only if issue 2
     is (c), to build the spelling map.

======================================================================================================================
5. AGREED FACTS
======================================================================================================================
- Ship after changes; no retirement argued (USE-12, TP-2; precedent checker D2).
- Option (a) as implemented departs from LEAK-10 clause 2 (Must) with no fact that sets it apart. (a') needs the
  amendment declined 2026-10-21. LEAK-11 does not apply: the late values strengthen the signal.
- The matched test (same rows, same 2026 labels, train and test on one snapshot): the 2026 values beat the June 2021
  values by +0.0367 (SE 0.0020) over time, +0.0299 (0.0042) at equal age and +0.0294 (0.0026) iid. This is a lower
  bound.
- The three WCIO codes, industry, age, accident date and ZIP leave by default (LEAK-10 clause 2).
- The fields that stay are measured field by field, and located late cells are repaired rather than blanked, because a
  blank marks the outcome (LEAK-7, PROV-13). Both conditional; superseded for the insurer name by point 3.
- History from 2016-01-01 (SPLIT-20; NON-COMP 45.0% to 61.3% and MED ONLY 22.2% to 10.4% through 2015, stable from
  2016). SPLIT-21 bars deciding from the fits.
- fit_reason is rewritten (USE-8, Must, before shipping).
- LEAK-24 is met by the 2020 cut: residual about 12% PPD NSL and 13% PTD still to come; notes only. SPLIT-10: no gap
  (smooth ladder, no edge step, no selection by outcome).
- Accident dates after assembly are Board-set dates of disablement (84% occupational disease), so LEAK-10/LEAK-7 and
  not CLEAN-11; moot once accident_date goes.
- Sex and age: no law found that bars them (SEL-1 holds). Sex is decided with rais issue 1; age is moot.
- These hold: the temporal regime and the three 2019 windows (oldest pool 79.1%, 74.1% from 2016); no exact copies
  across the split; linked claims 0.04%; the log_loss fallback equals sklearn, and every class is in every fold (PTD
  38-46, DEATH 39-44; TP-8); the CANCELLED, ADR and PFL row drops (USE-5, LEAK-25); the _1m budget explains the row
  count (1,000,000 + 298,680).
- CLEAN-11/-12 fixes and note corrections (now mostly moot by the drops).

======================================================================================================================
6. THE TASK GAMER'S EXPLOITS, MAPPED
======================================================================================================================
It could not see the 2026-value leak: its kit holds only 2026 values, so it read the blanks (carrier 97%, WCIO 94%
NON-COMP) as facts known at assembly.
- Category counts over all rows incl. the test window (+0.0025): LEAK-9, transductive use of the test block. Counts
  from the training rows alone give the same 0.8371: honest frequency encoding. New; no issue.
- Later claims with the same accident date, insurer or ZIP; the same person's later claims; an earlier claim's final
  label (all within the seed spread of 0.0003): SPLIT-9, SPLIT-13. The split auditor knew them (linked claims 0.04%,
  label agreement near chance). Mostly moot after the drops. No issue.
- Prior shift to the test window's rates: no gain. No rule.
- Blanks read as facts at assembly: LEAK-10, "missingness that encodes the outcome". Known (claim auditor row 30). The
  definition's note does not state it, so the measured gain (+0.0065 to +0.0076 on the shipped windows) differs from
  the note. Fixed by the WCIO drop and by issue 2 (the insurer's blank).
- Label maturity, which it could not check: LEAK-24 and SPLIT-10. Known (split auditor finding 1); notes, change 5.
- NON-COMP sampled about 1.3 points lower: the ADR row drop (13,678 claims, 99.97% NON-COMP; LEAK-25). Known,
  documented.
- The 2015 label mix: SPLIT-20. Known; change 3.

======================================================================================================================
7. CONSISTENCY WITH PRECEDENT (precedent checker's report, checked)
======================================================================================================================
- LEAK-10 clause 2: followed. Every field dropped shows a traced gain above 2 SE in an unconfounded design, as in
  distribution_transformers_at_cauca_department (CC 2026-10-21) and kumc_inpatient_aki_prediction (drops at +0.003 and
  +0.004, mediator 2026-11-09). The fields kept show none at 2 SE, as in onlinenewspopularity (CC 2026-10-26) and
  medical_facility_operational_data (CC 2026-11-05). X4 (2026-11-08): the cost of a drop is not a reason to keep.
- One departure in form, not in substance: kumc's drops were changes made now, while the insurer here is an issue (2)
  with the drop recommended. The fact that sets it apart: this drop leaves a task at 3.2-3.5% of the class-share loss,
  which opens a weighing (ship or retire) that the rules leave to the curator, and no panelist argued it.
- LEAK-13 (hepatitis_c_prediction, gallstone_disease): a class-linked recording convention is harmonised. It applies
  to the insurer's spellings only under issue 2 (c).
- PROV-13/14: a repair restores damaged values from the origin. The June 2021 copy is an earlier pull of the same
  table, but for the insurer name it carries more of the same artefact, so it is no repair. Its other uses are
  negligible after the drops.
- TP-2 and the Tensions row "the right split against the score" (forest_fires, noaa_storm_events_damage): a thin
  honest task ships. Retirement would need a marker; `Not Representative` for this reason has no precedent (precedent
  checker D2).
- SPLIT-20/21 (aeolus): the history start follows the break, not the fits. Followed.
- USE-8 (house_sales, sarcoma): approximate as "a task changed a lot to avoid a leak". Followed.
- Sex: consistent with the Tensions row as written (pricing only). It is its own REVIEW.md issue, decided with rais
  issue 1 (per-dataset rule, 2026-11-08). wioa_employment_after_exit_1m is decided alike or set apart by its own fact.
- The _1m row budget (nyc_taxi_trip_duration_1m, consumer_complaints_1m, aeolus_1m): consistent (D6).
- No drift and no third exception: no keep with a traced gain is recommended.

Limits (EV-7, EV-8): the matched sample is one copy (June 2021) of COVID-era claims, 0-5 months after assembly, so the
trace is a lower bound for assembly against 2026. The models are untuned LightGBM on at most 300k rows; E8 is one seed.
The merged insurer links only spellings that share the first word (a link on any pair chains 76% of claims into one
group).
```

</details>

<details><summary>Claim audit</summary>

```text
CLAIM AUDITOR REPORT: ny_wcb_assembled_claims -> datasets/_dev/tabarena-v0pt2/ny_wcb_assembled_claims_1m
Date: 2026-11-09. Read-only (scripts in the run folder).

VERDICT: ship only after the curator decides issue 1 again, with new numbers. The builder's option (a), "keep the 2026
values with a note", goes against the text of LEAK-10's later-pull clause: the part we can trace carries a gain. The
gain is smaller than the builder's 0.14 but it is real: 0.030-0.037 log loss with train and test values from the same
snapshot. Everything else holds or is minor: metric, splits, copies, protected grounds, decoding and the label cut. The
cut leaves a residual we can measure, concentrated in PPD NSL and PTD.

======================================================================================================================
A. TABLE: claim | source | test | result | evidence | rule
======================================================================================================================
(numbers from my own runs unless marked "builder")

 1 Source = Open NY jshw-gkgu | claims.md 1, dataset.py source_url | portal metadata | HOLDS | view_meta.json name matches; created 2014-12-04, published 2021-06-18 | PROV-8
 2 5,655,563 claims x 54 cols | claims 2 | read claims.parquet | HOLDS | raw (5655563, 54) | PROV-13
 3 Bulk export truncated, 8 API chunks | claims 3 | file list | HOLDS (not re-downloaded) | 8 chunks in the warehouse, claims.parquet built from them | PROV-13
 4 Licence: OPEN-NY ToU, no attribution | claims 4, dataset.py license | read open_ny_terms.txt | HOLDS | l.16 no attribution requirement; l.138 "non-exclusive, revocable license"; view_meta license=None | EV-4
 5 year="2026" | claims 5 | metadata | HOLDS as a stated choice (PROV-9 is the curator's call, issue 7) | rowsUpdatedAt 2026-09 | PROV-9
 6 No source task or metric; course task used macro F1 | claims 6, Metric.fallback reason | searched the web again (Kaggle + WCB claim injury type) | HOLDS | only the ML2425_ToGrantOrNotToGrant course project (2020-2022 claims) and unrelated Kaggle claims-cost contests | MET-1, MET-8, MET-11
 7 June 2021 Kaggle copy = evidence only | claims 7 | joined on claim id | HOLDS | 1,426,699 of 1,426,699 shipped claims found in the 2021 copy | EV-2
 8 Prediction point = assembly | claims 8, notes | codebook + Overview | HOLDS (definition) | Overview "Claim Assembly"; DataDictionary: assembly is triggered by >1 week lost time, a serious injury, a dispute or a C-3 | LEAK-1
 9 Use case: routing at assembly, fit approximate | claims 9, task_summary | read | HOLDS as ours; see SEL-1 below on "the Board or the insurer" | USE-1, USE-8
10 Target = benefit type, ordered least->most severe, 7 classes | claims 10 | codebook + frame | HOLDS | codebook order matches TARGET_LEVELS; CANCELLED dropped | CLEAN-25, USE-5
11 Target "as of the date the data set was created" | claims 11 | Overview FAQ 4 | HOLDS | FAQ 4: "NON-COMP means that an award for lost time has not yet been made" | LEAK-24
12 1,463,820 raw -> 1,426,699 kept; 1,298,680 in the _1m frame | claims 12 | re-ran _clean | HOLDS | clean (1426699, 18); kit 1,298,680 rows | -
13 Class counts | claims 13 | value_counts on _clean | HOLDS exactly | NON-COMP 891,793 ... PTD 747, DEATH 713 | -
14 ADR claims 99.97% NON-COMP, flag stable | claims 14 | builder probe; not re-run | HOLDS (builder numbers; consistent with Decision 2 table) | 13,678 claims, 0.9997 NON-COMP | LEAK-25, USE-5
15 History from 2015 (EDI) | claims 15 | Decision 1 table + Overview | HOLDS | EDI mandatory 2014-04-23 (Overview); WCIO filled 0.96+ from 2015 | SPLIT-20
16 Cut at 2020-01-01 for label maturity; "benefit types that have settled" (Decision 1 title) | claims 16, RELEASE_CUT, Decision 1 | 2021->2026 label change by year on the shipped rows, and the 2014 cohort as the analogue of the 2019 test cohort | HOLDS APPROXIMATELY, "settled" is overstated | changed 2021->2026: 2015 1.21%, 2016 1.73%, 2017 2.60%, 2018 4.30%, 2019 8.32%. The 2014 cohort, at the age our 2019 test claims have now, still changed 0.94% and later gained 12% of its PPD NSL and 13% of its PTD (builder maturity_by_class: 0.881 / 0.871). The training cohorts' analogues (2010-2013) are 93-97% complete on PPD NSL, so test labels are less mature than training labels in the two rarest severe classes | LEAK-24 (Must)
17 Post-assembly columns dropped; ANCR/hearing/etc. never on or before assembly | claims 17, POST_ASSEMBLY | 2026 raw, 2015-2019 | HOLDS | on or before assembly: ANCR 0/535,356, Section 32 0, PPD/PTD dates 0, first hearing 15/333,610, appeal 1, controverted 229/79,585 (0.29%; the 2022 redefinition); all dropped anyway | LEAK-10
18 AWW positive mostly for indemnity classes | claims 18 | Decision 2 table | HOLDS | 0.39% of AWW>0 claims are NON-COMP | LEAK-10
19 Attorney flag unstable | claims 19 | builder field_stability | HOLDS | 28% changed (builder) | LEAK-10
20 Occupational disease: 0 NON-COMP | claims 20 | Decision 2 table | HOLDS | 14,466 claims, NON-COMP 0.000 | LEAK-10
21 C-2/C-3 kept only on or before assembly | claims 21, step 5 | 2026 raw | HOLDS | C-2 on/before 91.3% (72.7% same day as assembly); C-3 on/before 36.9% | LEAK-7
22 Kept fields are 2026 values; young-claim drift 2-17% | claims 22, fit_reason, "Potential leak, kept on purpose" | 2021 vs 2026 for the SHIPPED 2015-2019 claims (not only the young ones) | HOLDS as a description; the "kept" judgment is REFUTED (row 23) | changed after June 2021, i.e. 1.5-6.5 years after assembly: carrier name 6.3%, district 9.9% (mostly renames HAUPPAUGE->LONG ISLAND, STATEWIDE->NYC 5,611; ~3.5k real moves), ZIP 2.3% (3.5% in 2019), fee region 0.9%, WCIO 0.3-0.9%, age 0.1-0.2%. The moved cells follow the outcome: ZIP changed n=32,322 15.6% NON-COMP / 9.8% PPD NSL (base 62.5% / 1.4%); carrier name changed n=90,095 28.8% NON-COMP; WCIO nature changed n=8,402 11.1% NON-COMP / 13.2% NSL; fee region changed n=12,766 14.2% NON-COMP; age changed n=1,620 26.4% NON-COMP | LEAK-10 (Must)
23 "Part of the gap is the mismatch of a model trained on completed fields"; "kept because the codes describe the injury, which exists at assembly" (option a) | notes "Potential leak", builder issue 1 | DECISIVE: same rows, same 2026 labels; train AND test both on June-2021 values (weeks to 5 months after assembly) or both on 2026 values; LightGBM, 3 seeds, row bootstrap | MISMATCH PART HOLDS; KEEP-WITH-NOTE REFUTED | 2021 claims (105,786). Time design (train Jan-Mar, test Apr-Jun): class shares 1.1214, 2026 values 0.9766, 2021 values 1.0133, gap +0.0367 (SE 0.0020). iid at equal age (Apr-Jun): 1.0342 vs 1.0641, gap +0.0299 (SE 0.0042). iid Jan-Jun: 0.9766 vs 1.0060, +0.0294 (SE 0.0026). So the 2026 values carry 0.03-0.037 of post-assembly information, 21-31% of the skill as measured, and this is a lower bound (the 2021 values are already weeks to months old). Swapping one field from its 2021 to its 2026 value: WCIO +0.016, age +0.009, accident date +0.008, industry +0.008, ZIP +0.004; carrier, district, county/region, C-3 none. The builder's 0.14 was mostly mismatch; the rest is a leak | LEAK-10 later-pull clause: "where they cannot be located row by row, the values go when they may carry a gain ... and stay with a note only when the part that can be traced shows none"
24 Later carriers (ATF, 25-A, 15-8) blanked | claims 24, step 6 | carrier_type mix | HOLDS; 5D "SPECIAL FUND - UNKNOWN" (2,229) kept, a minor open point | 5D: 45% NON-COMP, 5.2% NSL, 1.3% DEATH; 143 claims moved UNKNOWN->5D after June 2021 | LEAK-10 (minor)
25 Birth year redundant | claims 25 | not re-run | UNTESTED (dropped; no effect on validity) | - | SEL-1/CLEAN
26 One description per WCIO cause/nature code; industry 21/25, body part 55/58 | claims 26, notes "Codes and words" | codes vs descriptions, 2015-2019 raw | HOLDS for cause (76/76) and nature (55/55); counts are slightly off for 2015-2019: industry 20 descriptions/24 codes, body part 54/57 (DISC, SOFT TISSUE, SPINAL CORD have 2 codes each); "desc (code)" keeps both, so nothing is lost | checks1.log (f) | CLEAN-12
27 COVID indicator N before 2020 | claims 27 | raw | HOLDS | {'N': 1,463,820} | -
28 Missing-value codes; accident date after assembly blanked | claims 28 | frame | HOLDS as cleaning; BUT the 2026 blanks encode the outcome (row 30) | gender U 7,726 -> missing; no X in 2015-2019 | CLEAN-10
29 347 pre-1990 accidents kept | claims 29 | lag table | HOLDS; 5 claims assembled 2015-01-01 (accident years ~1941) look like migration artefacts, negligible | accident lag >10 y: 5,892 claims, 45% NON-COMP | CLEAN-11
30 IMPLIED: every kept feature's missingness is as of assembly | not written | class mix of the 2026 blanks + shipped-split worth | REFUTED (small) | blank in 2026: WCIO cause/nature n=19,716 94.4% NON-COMP; industry n=13,041 95.3%; carrier n=4,562 97.0%; age n=10,119 87.1%; accident date (blank in both snapshots) n=5,343 87.8% (base 62.5%). At assembly the sign is the reverse: April-June 2021 claims with WCIO blank in June 2021 ended PPD SCH LOSS 31% against 7.6% (builder). Shipped splits, LightGBM on 300k: worth of the blanks (as shipped vs blanks imputed by random draws) +0.0065 / +0.0076 / +0.0070 on r0/r1/r2, about 4% of the 0.17 skill | LEAK-10 "missingness that encodes the outcome" (Must)
31 Sex (and age) stay as features | claims 31, notes, builder issue 6 | law search | HOLDS: no law found that bars them for this decision | see section C | SEL-1, USE-1/USE-6, Tensions row "rating factor ... may no longer use"
32 Temporal splits: 3 x 4-month windows of 2019; 97,676-101,201 test; 1M train | claims 32, splits_comment | shipped splits | HOLDS | r0 test 2019-09-02..12-31 n=99,803, train 2015-01-01..2019-08-31; r1 101,201; r2 97,676; train 1,000,000 each; "79%" = the oldest window's pool 1,128,019 / 1,426,699 | SPLIT-14
33 No gap; measured cost 0.021-0.039 | claims 33 | read gap_experiment.json | HOLDS (builder's numbers, not re-run) | 0.865/0.871/0.896 vs 0.886/0.897/0.935 | SPLIT-10
34 Metric: fallback log_loss | claims 34, Metric.fallback | class-share prediction scored with the benchmark scorer on each fold, compared with sklearn | HOLDS; computable | r0 1.0578, r1 1.0619, r2 1.0775 (same as sklearn, array and DataFrame input). Every class is in every test fold: PTD 38-46, DEATH 39-44, PPD NSL 1,240-1,360. A probability array in the ordinal category order scores 3.0 instead of 1.06 (the documented sorted-classes convention; no dataset fix) | MET-1, MET-2, MET-8
35 IMPLIED: no copy across the split | - | hash of all 17 features, test vs train | HOLDS | 0 test rows have an exact feature copy in train on all 3 splits; 167 rows lie in duplicate groups across the frame | LEAK-16..21
36 IMPLIED: codes decoded into words (builder checklist "CLEAN-12 applied") | builder checklist P7 | feature list vs codebook | REFUTED (minor) | medical_fee_region ships as I/II/III/IV; the codebook gives words (I rural areas outside the upstate cities; II Buffalo, Albany, Syracuse, Rochester, Utica, Binghamton; III Westchester, Rockland, most of Suffolk, Orange, Putnam; IV NYC, Nassau, western Suffolk) | CLEAN-12 (Should)
37 IMPLIED: district is an assembly-time value | fit_reason names it | 2021 vs 2026 crosstab | HOLDS within noise | real reassignments about 0.25%; the district swap adds -0.0015 in the matched test; 49 VIRTUAL ONLY claims (district created later) | LEAK-10

======================================================================================================================
B. REFUTED AND UNTESTED, RANKED (validity first, Must first)
======================================================================================================================
1. [P4, LEAK-10 Must; later-pull clause] Issue 1's recommendation (a), "keep the 2026 values with a note", is
   refuted by the measurement the rule asks for. I trained and tested on the same snapshot to remove the
   train/test mismatch. The 2026 values still beat the near-assembly values by 0.030-0.037 log loss (SE
   0.002-0.004) on 2021 claims: 21-31% of the measured skill, and only a lower bound, since the June-2021 values
   are already weeks to months old. The shipped 2015-2019 claims are 6.7-11.7 years old, and their late cells
   follow the outcome (row 22: a ZIP changed after June 2021 means 9.8% PPD NSL against 1.4%). The clause reads:
   values that cannot be located row by row "go when they may carry a gain", and stay with a note "only when the
   part that can be traced shows none". The traced part shows a gain. The builder's reason ("the codes describe
   the injury, which exists at assembly") does not hold for the WCIO codes: their swap alone is worth +0.016.
   What it changes: the benchmark's ranking and its absolute numbers reward fitting fields updated over the
   claim's course. The leak is moderate, not dominant: with near-assembly values a model still scores 0.065-0.126
   below the class shares.
   The rule's remedy (values go) loses most of the task. Without WCIO, industry, age, accident date and ZIP, the
   rest scores only 0.024-0.077 below the shares, and keeps a residual gap of +0.003 to +0.009.
   Mildest remedies, in order, for the curator (a weighing call under LEAK-10's case-by-case clause):
   (a') keep, but rewrite the note with the matched numbers: no longer "part of the gap is mismatch". It becomes
        "a measured leak of at least 0.03 log loss (21-31% of skill); WCIO 0.016, age 0.009, accident 0.008,
        industry 0.008, ZIP 0.004". The curator then records it as a departure: LEAK-10 is a Must, so this needs
        an amendment of the later-pull clause, or a precedent that keeps a traced gain with a note (none found:
        onlinenewspopularity was kept because the trace showed none). Fit stays approximate.
   (b') repair, partly: take the kept fields of the 2015-2019 claims from the June 2021 copy (the earliest pull
        we hold, 1.5-6.5 years after assembly), so the 32k ZIP, 90k carrier and 8k WCIO cells changed later are
        restored. Restore, never blank: blanking would itself encode the outcome. This removes only the traced
        part; age at snapshot differs between train and test cohorts.
   (c') retire as "fields not as of the prediction point". Or rebuild on a source with near-assembly values: an
        archive of quarterly tables, if one is found. The record mentions 2023 Kaggle copies; we did not use them.
2. [P4, LEAK-10 Must; "missingness that encodes the outcome"] Implied claim 30 is refuted. A 2026 blank in WCIO
   (94.4% NON-COMP), industry (95.3%), carrier (97.0%), age (87.1%) or accident date (87.8%) marks a claim that
   never progressed. At assembly a blank WCIO meant the opposite (31% PPD SCH LOSS). Worth on the shipped splits:
   +0.0065 to +0.0076 log loss. It is part of item 1's leak and is fixed with it. On its own, the mildest remedy
   is to name it in the "Potential leak" note. Imputing would be inventing values, so no fix in the definition is
   clean.
3. [P4, LEAK-24 Must] Holds approximately. The wording "benefit types that have settled" (Decision 1 title) and
   "settling" in task_summary.changes overstate it. On the 2014 analogue, about 1% of the 2019 test labels will
   still change. The test cohort lacks about 12% of its eventual PPD NSL and 13% of its PTD; the training cohorts
   lack 3-7%. So test labels are less mature than training labels in exactly the rarest severe classes.
   Remedy: add the residual to the notes (mildest). Option (c) of issue 2 (cut at 2019, test windows in 2018)
   gains only about 0.2 points of label completeness, so keeping the 2020 cut is defensible.
4. [P7, CLEAN-12 Should] medical_fee_region is not decoded (row 36). Remedy: map I-IV to the codebook's region
   words. It may become an ordered category if the fee levels are ordered (unverified).
5. [P7] Small text corrections: industry "21 descriptions for 25 codes" should read 20/24, and body part "55 for
   58" should read 54/57, in the kept years. The 5D "SPECIAL FUND - UNKNOWN" carrier type is kept although 143
   claims moved UNKNOWN->5D after June 2021 (2,229 claims; 45% NON-COMP, 1.3% DEATH). Remedy: one note line;
   optionally treat 5D like UNKNOWN.
Untested: claim 25 (birth year, dropped); claim 33's gap experiment (not re-run; the json matches the text); the
3 conflicting duplicate rows; whether the medical fee regions are ordered.

======================================================================================================================
C. PROTECTED GROUNDS (gender, age) -- SEL-1 / the tension row on factors the actor may no longer use
======================================================================================================================
Question: does any law bar sex or age as inputs for this decision (routing a workers' compensation claim at
assembly, by the Board or the carrier)? Answer: none found.
- NY Insurance Law s2607 (text read on nysenate.gov) bars refusing to issue, cancelling or declining to renew a
  policy "because of the sex or marital status of the applicant or policyholder", or engaging in sexual
  stereotyping. That is underwriting of the policyholder, here the employer. The injured worker is a claimant,
  not a policyholder, and a claim is not an issue or renewal decision.
- NYDFS Insurance Circular Letter No. 7 (2024), on AI and external data, covers underwriting and pricing and
  explicitly not claims adjusting (law-firm summaries; I did not read the letter itself).
- Age: the NY Insurance Law lists age as a barred ground only for bonds (s2609); S5267 (2025), which would extend
  this, was not enacted as far as found.
- Under the collection's own stance ("as if in the EU"), Directive 2004/113/EC art. 5 bars sex in "premiums and
  benefits". Routing changes neither, since the Board sets the benefits by statute, and the Directive excludes
  employment and occupation matters.
- Not resolved: whether the NY Human Rights Law reaches a state agency's internal routing. If the curator wants
  to avoid the question, name the carrier as the actor (the use case says "the Board or the insurer").
Conclusion: SEL-1 holds. The pricing stance does not extend here by its words ("every insurance pricing task").
Keeping sex and age is consistent with home_credit and credit_card_clients_default (credit, kept). Builder issue 6
stays a curator confirmation, not a fix.

======================================================================================================================
D. METRIC (MET-1/2/3)
======================================================================================================================
No source metric exists. Looked again (web; Kaggle via search): only a university course project
(ML2425_ToGrantOrNotToGrant, macro F1, 2020-2022 claims, post-assembly fields). The fallback log_loss is right
under MET-8 for a 7-class target with no fixed cost. It is computable per claim on every fold, every class is
present in every test fold, and the benchmark scorer equals sklearn. There is no weight, scoring column or unit
question.

Sources: https://data.ny.gov/d/jshw-gkgu ; https://www.nysenate.gov/legislation/laws/ISC/2607 ;
https://www.dfs.ny.gov/industry-guidance/circular-letters/cl2024-07 (scope via
https://www.debevoise.com/insights/publications/2024/07/nydfs-adopts-final-circular-on-use-of-ai) ;
https://github-users.yhajoa.workers.dev/DiogoGAndrade/ML2425_ToGrantOrNotToGrant
```

</details>

<details><summary>Column audit</summary>

```text
COLUMN AUDITOR REPORT: ny_wcb_assembled_claims (folder ny_wcb_assembled_claims_1m), 2026-11-09

Verdict: ship only after the curator's call on issue 1, and that call has to be made against LEAK-10's default.
Every column the definition drops is rightly dropped. But about 70% of the task's skill sits on fields whose 2026
values were completed or changed after assembly, and that completion follows the claim's course. The builder's
recommendation (a), keep with a note, departs from the default of LEAK-10 clause 2 (Must). Its framing "LEAK-10
against LEAK-11" does not hold, because LEAK-11 covers late values that weaken the signal, and these strengthen it.
Smaller items: one wrong note (the "impossible" accident dates are mostly dates of disablement the Board set for
occupational diseases), two small post-assembly carrier and district codes, and cheap cleaning (one negative ZIP, 17
ages from 100 to 117, fee regions not decoded).

Inputs read: dataset.py and README.md, DataDictionary.txt and Overview.txt (the WCB codebook and FAQ),
builder_report.md, claims.md, probes/ (field_stability.txt, snapshot_feature_sets_harmonised.log, dtype/), the rules
(principles, use_case, leak_checks, cleaning_features, SEL-1). Frame: the definition's own _clean run on the raw rows of
2015-2019 (1,426,699 rows, 17 features plus the target; identical filter to the definition's). (Scripts in the run folder.)
Fits: LightGBM, 300k random claims of 2015-2018 in training, all 298,680 claims of 2019 scored (class shares 1.066).

------------------------------------------------------------------------------------------------------------------------
1. COLUMN TABLE (the shipped frame)
------------------------------------------------------------------------------------------------------------------------
Abbreviations: "young" = the claims assembled 2021-04-01 to 2021-06-18, compared between the June 2021 Kaggle copy
(0 to 11 weeks after assembly) and the 2026 snapshot (44,117 claims after the definition's row filters). "u21/u26" =
the share unknown in 2021 / in 2026.

column | meaning (codebook) | known at assembly? | dtype and cleaning | verdict | rule
---|---|---|---|---|---
assembly_date | date the claim was first assembled (the prediction point) | yes, by definition | datetime; time column of the split; also a feature (fine in a temporal task) | fine | LEAK-1, SPLIT
accident_date | injury date; for occupational disease (OD) the date of disablement, "not always known when the case is assembled" (FAQ 5) | partly. 2026 value. Young: changed 1.2-2.3%, filled later 0.5-1%. Filled later -> 64% PPD SCH LOSS, 3.8% NON-COMP; still blank 2026 -> 89% NON-COMP. 3,039 dates after assembly set to missing: 84% OD=Y, 64% PPD SCH LOSS, 3.7% NON-COMP (Board-set dates of disablement, not impossible values) | datetime; the 3,039 blanked dates merge with 5,344 raw blanks (87.8% NON-COMP). 347 dates before 1990 kept (noted) | leak, weak on its own (its missingness is worth 0.0009 log loss on 2019; the builder's swap 0.006); part of issue 1; the note is wrong | LEAK-10 (clause 2, missingness); note fix
age_at_injury | age at injury, from the birth date; 0 = not computable (FAQ 6) | mostly. Young: changed 1.2-2%, u21 1.54%, u26 0.85%. Filled later -> 57% PPD SCH LOSS, 9.4% NON-COMP; still 0 in 2026 -> 87% NON-COMP | numeric (right); 0 -> missing (right). 17 rows aged 100-117 (birth years 1901-1916, 1911 seven times) are placeholders, still in. 146 under 14 (FAQ allows child actors); keep | leak, weak (missingness 0.0003; swap 0.006); cleaning: 17 impossible ages | LEAK-10 clause 2; CLEAN-11
c2_date | receipt of the employer's report or equivalent; from the 2022 tables, the earliest equivalent filing (eClaims FROI) | yes when <= assembly (kept only then; 72% the same day). The 2021 copy used the old definition (0.2-0.7% filled), so its value at assembly cannot be traced | datetime; later dates -> missing (121,329); "no C-2 by assembly" is known at assembly | fine (note: definition changed in 2022, applied backwards) | LEAK-7
c3_date | receipt of the worker's claim form (C-3) | yes when <= assembly; stable (14 of 20,756 young changed) | datetime; later dates -> missing (282,161) | fine | LEAK-7
carrier_name | primary insurer of the employer | mostly. 2026 value: young changed 14-16% (mostly spelling; the builder's harmonised swap costs 0.008). UNKNOWN still in 2026 is an outcome marker (see carrier_type) | categorical, 2,184 levels; "*** CARRIER UNDETERMINED ***" -> missing; ATF/25-A/15-8 takeovers -> missing (right, FAQ 11). The Uninsured Employers Fund TPA (1,124 rows under 5D) is partly assigned after assembly | leak, weak; part of issue 1 | LEAK-10 clause 2
carrier_type | type of insurer (1A-5D) | mostly. UNKNOWN: young u21 0.76% (58.8% NON-COMP), u26 0.37% (96.3% NON-COMP); filled later -> 28% NON-COMP. 2015-2019: 143 claims UNKNOWN in 2021 became 5D SPECIAL FUND - UNKNOWN by 2026. Shipped missing (4,562 rows): 97.0% NON-COMP | categorical, 6 levels; codes in words already | leak, weak (missingness of type and name together -0.0007, at noise); note it | LEAK-10 (missingness)
claim_type | WC claim, volunteer firefighter, volunteer ambulance, Non-WC (= WTC volunteer claims, FAQ 8) | yes; 0-1 changes | categorical, 4 levels; "NON-WC" means WTC volunteers (the label misleads; optional decode); double spaces in the source labels | fine (optional CLEAN-12) | CLEAN-12
county_of_injury | NY county where the injury occurred | yes; 0 changes | categorical, 62 levels = NY's 62 counties; UNKNOWN -> missing | fine | CLEAN-10
district_name | WCB district office overseeing the claim | mostly. Renames between 2021 and 2026: Hauppauge -> Long Island (133,731), Statewide -> NYC (5,719); real reassignments about 0.2% (NYC -> Long Island 563, NYC -> Albany 474, ...). VIRTUAL ONLY (49 rows, 49% NON-COMP / 33% TEMPORARY): a district without an office, holding remote hearings; probably post-assembly for 2015-2019 claims (still active later) | categorical, 8 levels | fine; VIRTUAL ONLY a tiny post-assembly code (note, or missing) | LEAK-10 (weak)
gender | reported gender F/M/X/U | yes (young 0.15-0.3% changed); U still in 2026: 81% NON-COMP against 75% at 2021 (mild) | categorical; U -> missing; no X before 2020 | fine on timing; protected ground kept, a question for the curator (issue 6) | SEL-1; principles Tensions (sex in insurance pricing)
medical_fee_region | approximate region of medical service from a ZIP-to-county map; I-IV, UK unknown | mostly; follows the 2026 ZIP (young changed 2.8-3.2%); UK grew from 4.4% (2021) to 5.7% (2026) for the same young claims | categorical I/II/III/IV; UK -> missing. The codebook names every region in words (I = rural areas outside the six cities ... IV = NYC, Nassau, western Suffolk): decode | cleaning (Should, cheap): decode to the codebook's words | CLEAN-12
zip_code | ZIP of the worker's home | mostly; 2026 address: young changed 7.5-10%, 2018 cohort 2.3% (builder's swap 0.0009) | categorical, 13,008 levels. Dtype probe (re-run 2026-11-09): ordinal_like and open_end. Answer: a ZIP is a nominal code, keep it categorical. The "open end" 'LE4 3' is a truncated UK postcode (1 row). Problems: '-7296' (1 row) is impossible; 614 rows hold foreign postal codes truncated to 5 characters ('M3K2B' x65, 'JMACE', '010'), keep. 81,815 five-digit out-of-state ZIPs (NJ, PA, CT) are plausible | cleaning: '-7296' -> missing; quasi-identifier (issue 5) | CLEAN-11, CLEAN-14; SEL-1 weigh
industry | 2-digit NAICS sector, description + code | partly. Young: u21 4.9% (33% NON-COMP, 44% PPD SCH LOSS), u26 0.9% (97.8% NON-COMP); filled later -> 53% PPD SCH LOSS; changed 0.9-1.2%. Shipped missing (13,041): 95.3% NON-COMP | categorical; 24 codes / 20 descriptions in 2015-2019, the "(code)" keeps them apart (lossless; the notes say 21/25, the whole table's count) | leak, part of issue 1 | LEAK-10 clause 2
wcio_cause_of_injury | WCIO cause-of-injury description | partly. Young: changed 1.5-4.4%, u21 6.6-22%; same filling pattern as nature | categorical; 76 codes <-> 76 descriptions, one to one in 2015-2019: description only is lossless | leak, part of issue 1 | LEAK-10 clause 2; CLEAN-12 fine
wcio_nature_of_injury | WCIO nature of injury | partly. Young: u21 6.6% (36.7% NON-COMP, 35.8% PPD SCH LOSS), u26 1.3% (96.8% NON-COMP); filled later -> 44% PPD SCH LOSS, 22% NON-COMP; changed 1.5-6.6% | categorical; 55 <-> 55 one to one; no code 83 (COVID) before 2020 | leak, part of issue 1 (the largest single field: the builder's swap of the three WCIO codes costs 0.071) | LEAK-10 clause 2
wcio_part_of_body | WCIO part of body, description + code | partly; same pattern (u26 1.8%, 85.5% NON-COMP) | categorical; 57 codes / 54 descriptions (DISC 22/43, SOFT TISSUE 18/25, SPINAL CORD 23/47); the code is kept, lossless. The source truncates descriptions at 30 characters, so labels show unbalanced brackets ("MULTIPLE BODY PARTS (INCLUDING BODY (90)"); cosmetic | leak, part of issue 1 | LEAK-10 clause 2
claim_injury_type (target) | benefit type awarded "as of the date the data set was created" (FAQ 4) | label at 2026 (6.7+ years) | ordered category NON-COMP < MED ONLY < TEMPORARY < PPD SCH LOSS < PPD NSL < PTD < DEATH = the codebook's numbering 2-8 ("least to most severe"); CANCELLED rows dropped | fine (maturity is issue 2) | CLEAN-25; LEAK-24

Dropped columns, checked against the codebook. Every drop is right: the ANCR, controverted, first hearing, first
appeal, Section 32, PPD and PTD dates; the interval to ANCR; the hearing, IME-4 and closed counts; the current status;
the highest process ("to date", FAQ 10); the average weekly wage ("through the Board's adjudication"); the attorney
flag (no date, the claim's representation now); the accident and OD flags ("as determined by the WCB"); the OIICS block
(used at ANCR, FAQ 7; blank); ADR (rows dropped); COVID (constant); the claim identifier; the birth year (redundant
with age, more identifying); the WCIO cause and nature codes (one to one with the descriptions); and the industry and
body-part code columns (kept inside the combined labels). No column missing from the shipped frame should have been
kept.

No training weight: LEAK-41 and probe 22 do not apply.

Dtype probe: re-run (scripts in the run folder; with the codebook fetch). It flags zip_code only
('ordinal_like', 'open_end'); answered in the table (nominal, keep categorical). It ran on 13 non-date columns; the
four dates are datetime, as they should be.

------------------------------------------------------------------------------------------------------------------------
2. PROBLEMS, RANKED (principles.md: P1 first, then P4, then P7; within a rank by strength and effect)
------------------------------------------------------------------------------------------------------------------------

[1] P4, LEAK-10 clause 2 (Must, strong). The fields are their 2026 values, and the outcome drives their completion.
    Columns: wcio_cause_of_injury, wcio_nature_of_injury, wcio_part_of_body, industry, carrier_name, carrier_type,
    age_at_injury, accident_date (and, slightly, zip_code, medical_fee_region, district_name, gender).
    What is new beyond the builder's issue 1: the mechanism, and how much of the benchmark rides on it.
    - Completion follows the claim's course in both directions. For the young claims, the fields blank at about
      assembly and filled by 2026 are severe claims (filled later: industry 53%, WCIO nature 44%, age 57% and accident
      date 64% PPD SCH LOSS, against 9.5% overall). The fields still blank in 2026 are dead claims (85-98% NON-COMP for
      carrier type, industry, WCIO nature and body part, age and accident date, against 61% overall). At about assembly
      a blank meant the opposite (industry blank: 33% NON-COMP, 44% PPD SCH LOSS). In the 2026 values the meaning of
      "blank" flips. This is "missingness that encodes the outcome" (LEAK-10), on top of the changed values.
    - On the 2019 test windows, the missingness alone is worth little: replacing every blank with a random draw (train
      and test) costs 0.0074 log loss in total (WCIO 0.0030, accident 0.0009, age 0.0003, the rest at noise level,
      +/-0.0007). Most of the effect therefore sits in the values themselves, which cannot be traced for 2015-2019.
    - Share of the benchmark's skill on these fields (2019 test, 300k training rows): all features 0.880; without the
      WCIO codes 0.960; also without industry, carrier name, age and accident date 1.021; only the fields that changed
      for under 0.5% of the young claims (claim type, county, sex, carrier type, district, C-2/C-3 lags, time) 1.011;
      class shares 1.066. So 70-75% of the skill (0.186) sits on the fields whose late completion the traced part
      shows. That matches the builder's young-claim test (2026 values 0.921 against June 2021 values 1.061, class
      shares 1.118). A model fed the values a triage desk would see keeps about 30% of the skill the benchmark credits.
    - Rule reading: LEAK-10 clause 2: "where they cannot be located row by row, the values go when they may carry a gain
      ... and stay with a note only when the part that can be traced shows none". The traced part shows a gain (WCIO
      0.071, carrier name 0.008, age 0.006, accident date 0.006). So the default is "they go", and keeping them needs
      the curator's explicit case-by-case call. LEAK-11 (the builder's counterweight) narrows LEAK-10 only for late
      values that weaken the signal, so it does not apply. "The codes describe the injury, which exists at assembly"
      is true of the injury but not of the stored codes, which come from later FROI/SROI filings (the tension row "a
      real task against a leak": a very real task does not carry a leak).
    - Remedies, mildest first:
      (i) Repair from the origin: rebuild assembly-near values from archived quarterly tables (the June 2021 Kaggle
          copy; the 2023 Kaggle copies the builder did not use; Wayback copies of rows.csv, if any). Each snapshot gives
          near-assembly values only for the claims assembled in the preceding weeks, so this probably cannot reach a
          1M-row task. Worth one search before deciding.
      (ii) Fix the definition by the rule's default: drop the late-completed fields (WCIO x3, industry, carrier name,
          age, accident date). What remains scores 1.011-1.021 against 1.066 (skill about 0.05, real but thin).
          TP-2 says a small signal under the right task is no reason to retire.
      (iii) The curator keeps them by a case-by-case judgment under clause 2, with a "Potential leak, kept on purpose:"
          note that gives the numbers above (70-75% of the skill on late-completed fields; the flip of the blanks), and
          fit_reason stating the score overstates what a triage at assembly reaches. If (iii) is chosen, fit
          "approximate" understates the gap: the builder's fit_reason calls the changed shares "2% to 17%" but does not
          say that most of the skill rides on them.
      (iv) Retire the "at assembly" framing.
      Recommendation: put (ii) and (iii) to the curator with these numbers. The rule's default is (ii). I would not
      ship (iii) without the curator naming the fact that sets this case apart (consistency with
      distribution_transformers_at_cauca_department, where untraceable late values with a possible gain went).

[2] P1, SEL-1 (Must) and the Tensions table: protected grounds kept. A question for the curator; no rule is broken.
    - gender: kept. The pricing stance (sex leaves every insurance pricing task, 2026-11-08) does not cover claims
      triage, and no precedent of a claims-routing task exists in the working copy (grep: the insurance definitions with
      sex are all pricing). Its timing is clean (0.15-0.3% changed). The curator confirms the stance stops at pricing
      (builder's issue 6) or extends it. A triage that routes claims by sex is arguably closer to the stance's concern
      than a fraud or severity model.
    - age_at_injury: kept. Age is part of how disability and wage-earning capacity are judged, so it is a legitimate
      input. birth_year was dropped (redundant, more identifying): right.
    - zip_code: worker's home ZIP with age, sex, injury date and employer (builder's issue 5); weigh. Coarsening to 3
      digits is the mild option if the curator wants it.

[3] P4, LEAK-10 (Must, weak), and a wrong note: the 3,039 accident dates after assembly. 84% of them belong to
    occupational-disease claims (OD=Y 2,559 of 3,039), and they are 64% PPD SCH LOSS and 3.7% NON-COMP. These are the
    dates of disablement the Board sets for occupational diseases (FAQ 5), mostly hearing-loss-type scheduled awards.
    They are not "impossible" values (CLEAN-11 is the wrong rule). Blanking them is still the right remedy, since the
    date was set after assembly; 2,781 of them were already after assembly in the 2021 copy. But the blank then mixes
    them with 5,344 raw blanks (87.8% NON-COMP), and its signal is small (0.0009 log loss). Remedy: keep the blanking
    and rewrite the bullet: "3,039 accident dates after assembly (84% occupational diseases: the date of disablement
    set by the Board) are set to missing, as set after assembly; their blank marks a class mix of 64% PPD SCH LOSS".
    The accident date of OD claims (about 1%) is a Board determination in general, so add a residual note.

[4] P4, LEAK-10 (weak): carrier_type 5D SPECIAL FUND - UNKNOWN and the UNKNOWN carrier. 143 claims of 2015-2019 that
    were UNKNOWN in 2021 are 5D (Uninsured Employers Fund) in 2026, so the fund is partly assigned after assembly, as
    the ATF and 25-A/15-8 funds are. The shipped missing carrier (4,562 rows) is 97% NON-COMP; young claims show it was
    59% NON-COMP at about assembly. The measured signal is at noise level. Remedy: note it (one line in the Carrier
    bullet). Setting 5D to missing would only add to the marked missingness.

[5] P4, LEAK-10 (very weak): district_name VIRTUAL ONLY (49 rows). This district has no office and holds remote
    hearings, and its code on 2015-2019 claims was likely given after assembly to claims still active then (49% NON-COMP
    against 62.5%). Remedy: note it, or set to missing (49 rows). The renames (Hauppauge, Statewide) are harmonised by
    the 2026 values themselves; the real reassignments (about 0.2%) are negligible.

[6] P7, CLEAN-11 (Should): impossible values left in.
    - zip_code '-7296' (1 row) -> missing.
    - age_at_injury 100-117 (17 rows; birth years 1901-1916, 1911 seven times: placeholders) -> missing. A cut at 100
      is defensible; ages 95-99 (70 rows) are unusual and stay.
    Remedy: two set_missing entries (zip_code '-7296'; age >= 100 by a where()).

[7] P7, CLEAN-12 (Should): medical_fee_region ships as I/II/III/IV while the codebook names each region in words.
    Remedy: a CODE_LABELS map to the codebook's words ("Region 1: rural areas outside Buffalo, Albany, Syracuse,
    Rochester, Utica and Binghamton", ...). Nominal, not ordered: the codebook ranks nothing. Optional, same rule:
    claim_type "NON-WC" -> "Non-WC (World Trade Center volunteer claim)" (FAQ 8).

[8] Notes accuracy (procedure, not a rule failure).
    - Industry "21 descriptions for 25 NAICS sectors" and body part "55 for 58 codes" are counts over the whole
      table. In the kept 2015-2019 rows they are 20/24 and 54/57.
    - The code comment says 14,488 OD claims with 0 NON-COMP, the notes say 14,466.
    - The notes' C-2 bullet should say that the 2022 redefinition (earliest equivalent filing) is applied backwards in
      the 2026 table, so the C-2 date at assembly cannot be checked against the June 2021 copy (0.2-0.7% filled there
      under the old definition).

Nothing found on: copies or identifiers encoding the label (the claim identifier is dropped); outcome-closed spans
(the interval to ANCR is dropped; the C-2 and C-3 lags end at assembly); the target order; ordinal features (none);
counts typed categorical (none); training weights (none).

Files: scripts in the run folder.
```

</details>

<details><summary>Split audit</summary>

```text
SPLIT AUDITOR REPORT: ny_wcb_assembled_claims (folder ny_wcb_assembled_claims_1m), 2026-11-09

VERDICT: right with notes.
The regime (temporal on assembly_date), the three four-month windows of 2019, the expanding training sides and the
no-gap choice all hold under the rules as amended. Nothing needs a re-split. Two notes should go into splits_comment
(the label-delay numbers, finding 1), and the 2015 history start should be settled by the curator (finding 2).

Work: scripts in the run folder. Frames rebuilt from the definition: full cleaned frame 1,426,699 rows, plan frame 1,298,680.
LightGBM as in the builder's gap experiment (300 trees, lr 0.05, 63 leaves), 4 threads, 2 seeds.

---------------------------------------------------------------------------------------------------------------
WHAT HOLDS (with numbers)
---------------------------------------------------------------------------------------------------------------
* Regime (SPLIT-1, SPLIT-3, USE-10). The use case is routing a newly assembled claim. That means a stream over
  time with known insurers and new claims. Temporal on the assembly date matches it, and the assembly date is the
  prediction point the definition states. Grouping is not the regime: no claim recurs, the table has no employer
  column (data dictionary), and workers have no id (birth year is dropped).
* Windows (SPLIT-11, SPLIT-12, SPLIT-14, SPLIT-15, SPLIT-20). Shipped splits checked:
    - repeat 0: test 2019-09-02..2019-12-31, 99,803 rows; train 1,000,000 from 2015-01-01..2019-08-31; pool 1,326,896
      (93.0% of the frame); train/pool 0.754
    - repeat 1: test 2019-05-01..2019-08-31, 101,201 rows; pool 1,225,695 (85.9%); train/pool 0.816
    - repeat 2: test 2019-01-01..2019-04-30, 97,676 rows; pool 1,128,019 (79.1%); train/pool 0.887
  No train/test overlap. Every training side ends before its window. Each window has its own train side. The
  oldest window's pool is 79.1%, above the 50% floor. The windows are contiguous and together cover 2019 once, so
  every season is in a test window. In the oldest window, Q1 holds more PPD SCH LOSS every year (2016-2019 Q1
  10.4%, 10.4%, 9.1%, 9.1%), but that window also holds two non-Q1 months. Earlier windows (2017 or 2018 tests)
  would break the floor (a 2018 test window trains on 58%, a 2017 one on 38%), so 2019 is the only place for three
  windows.
* COVID (SPLIT-20). The release cut at 2020-01-01 keeps the 2020-2022 claims out of training and test. The 2019
  claims ran their post-assembly course into 2020, but their 2026 class mix shows no break against 2018: PPD SCH
  LOSS 8.76% vs 8.85%, PPD NSL 1.32% vs 1.25%, NON-COMP 64.9% vs 64.75%.
* Recurring entities (SPLIT-13). Carriers recur: the test rows' carrier is unseen in training for 0.049% to 0.071%
  of the rows (37-39 names per window). That is a known entity, as the use case expects: an insurer routes its own
  claims, and the Board routes the claims of carriers it knows. Unseen ZIP codes cover 0.44% to 0.51% of the test
  rows. Employers are not in the table.
* Shortcut through linked claims (SPLIT-9). Linked here means test claims with a training claim of the same
  accident: same accident date, ZIP, sex, carrier and industry, age within 1 year. There are 39 to 46 per window
  (0.040% to 0.045% of the test rows). Label agreement with the linked training claim is 0.47 / 0.50 / 0.64 against
  chance 0.39 / 0.49 / 0.42. This is negligible. The hidden-group probe agrees: near-copy clusters cover 3.4% of the
  rows, and 0.7% of the test rows have a near copy in training.
* Selection by outcome at the release end (SPLIT-10, LEAK-24). A claim enters the table when it is assembled,
  whatever its outcome, and every label is read 6.7+ years later. So the newest training rows are not the fast ones.
  Inside 2019 there is no visible censoring gradient. By window (Jan-Apr / May-Aug / Sep-Dec): PPD NSL 1.37% /
  1.23% / 1.36%, PTD 0.04-0.05%, DEATH 0.04%.

---------------------------------------------------------------------------------------------------------------
FINDINGS, RANKED (principles.md: P4 first; within P4 by rule order and strength)
---------------------------------------------------------------------------------------------------------------
1. P4, SPLIT-10 (Should; applies SPLIT-9). The training labels are the 2026 labels, not the ones a refit at the
   window start would have seen. Measured size; no shortcut; no gap is right. Note only.
   Evidence:
   - The label delay is years, not days. Between the June 2021 copy and 2026, the benefit type changed for 36% of
     the 2021 claims (age about 0.25 years in June 2021), 18.9% of 2020 (about 1 year), 8.2% of 2019 (about 2
     years), 4.2% of 2018 and 2.6% of 2017 (probes/maturity_by_class.txt). The FAQ says a NON-COMP claim is one
     where "an award for lost time has not yet been made".
   - Interpolating those shares at each training row's age at the window start: about 12.0% / 12.7% / 13.5% of
     each training side's labels changed after the window start. 22-26% of each side is under 1 year old and
     44-52% under 2 years. (This is an estimate: the young-age shares come from COVID-era claims.)
   - Gap ladder: LightGBM on 250k claims from a fixed 18-month span that ends k months before the window, 2 seeds,
     mean log loss:
         window       k=0     k=1     k=3     k=6     k=12
         Sep-Dec    0.8583  0.8595  0.8627  0.8683  0.8744
         May-Aug    0.8622  0.8635  0.8665  0.8694  0.8735
         Jan-Apr    0.8824  0.8843  0.8855  0.8872  0.8930
     The loss rises smoothly, by about 0.001 per month of gap. The newest month adds only 0.0012-0.0018, about the
     seed spread (0.001-0.002). There is no step at the window edge. That is the profile of drift and recency
     spread over shared codes, not a link to the test row's own entity. This sets the case apart from
     alfa_battle_2_0_task_2 and hotel_booking_demand, and it matches the SPLIT-9 row for
     lt_vehicle_loan_default_prediction.
   - Under SPLIT-10 as reworded on 2026-11-05: no shortcut is measured (above) and no row is selected by its
     outcome, so no gap is needed. The notes give what the newest labels add. The definition already gives one
     number: two years at 300k cost 0.021-0.039. That comparison also changes the share of the 2015 transitional
     rows in training (finding 2), so it overstates the label-delay cost somewhat.
   - Contrast with the closest precedent, chicago_traffic_crashes (final-snapshot labels): there a one-month gap
     covers 99.4% of the late updates. Here no gap covers the delay. A 12-month gap keeps SPLIT-14 (pools 58% /
     65% / 72%) and costs 0.011-0.016 log loss (ladder, k=12). But at 1 year old, 19% of the labels still change,
     so the gap would not simulate a real refit either. A gap that does cover the delay (3+ years) puts the oldest
     window under the floor: a 2-year gap already leaves 38%.
   Mildest remedy: notes only. Add to splits_comment the estimated share of training labels that changed after
   the window start (12-14%) and the ladder (smooth, about 0.001 per month, no edge step, 12 months 0.011-0.016),
   and say why no gap is set (no shortcut, no selection, the delay cannot be covered within the floor). The curator
   may still prefer a 12-month gap; it is valid under the floor, but I do not recommend it.

2. P4, SPLIT-20 (Should). The training history starts inside a recording break: the 2015 EDI ramp. Curator's
   call; a filter is the remedy.
   Evidence (2026 labels by assembly quarter):
       quarter   NON-COMP  MED ONLY
       2015Q1     45.0%     22.2%
       2015Q2     51.3%     19.3%
       2015Q3     56.7%     15.5%
       2015Q4     61.3%     10.4%
       2016-2019  63.7-65.6% 7.5-8.7%
   The class mix settles only in 2015Q4 or 2016Q1. The definition calls 2015 "the first full year of electronic
   claim filing". That is true of the mandate, but the mix of what was assembled kept shifting for three more
   quarters. 2015 is 20.6% / 22.3% / 24.3% of the three training sides (sampled at random from all earlier years).
   History variants at an equal 600k training rows, 2 seeds (log loss):
       window     from 2015        from 2015-10      from 2016
       Sep-Dec    0.8535 / 0.8575  0.8587 / 0.8559   0.8524 / 0.8478
       May-Aug    0.8607 / 0.8581  0.8530 / 0.8566   0.8947* / 0.8521
       Jan-Apr    0.8829 / 0.8943* 0.8734 / 0.8734   0.8724 / 0.8729
     (* unstable LightGBM fits; the builder saw the same instability in the task probe)
   Starting in 2016 is lower in 5 of 6 fits. Under SPLIT-21 this comparison over three windows informs but does
   not decide. The class-share break is the reason.
   Mildest remedy: HISTORY_START = 2016-01-01, or 2015-10-01. This is the builder's draft issue 3; this evidence
   favours its option "2016". Cost: 273,999 rows. The oldest window's pool becomes 854,018 of 1,152,700 = 74.1%,
   still above the floor, and its train side falls below 1M. The task_summary row ("2015 to 2019") and the
   decision table text would change with it. If 2015 stays, add one line to splits_comment saying the first three
   quarters are transitional.

3. P4, LEAK-24 (Must, met). Residual immaturity of the newest labels. Note only.
   Evidence: at about 7 years, the 2014 cohort held 88% of its 2026 PPD NSL awards, 87% of PTD and 97.6% of PPD
   SCH LOSS (maturity_by_class.txt). The 2019 test claims are 6.7-7.7 years old. The 2015-2018 training claims are
   7.0-11.9 years old and so slightly more mature.
   Seen in the data: PPD SCH LOSS in 2019Q4 is 8.48%, against 8.72-8.80% for 2019Q2-Q3 and 8.75-8.79% for
   2018Q2-Q4. That is a drop of about 0.25 pp, which fits about 2.5% of SCH LOSS awards still to come. PPD NSL
   shows no fall (1.37% in 2019Q4).
   The effect is a small shift toward the lower classes in the newest window, about the same in all three. The
   definition already says the label is "the benefit type to date, not a fixed horizon". Cutting at 2019 (the
   builder's issue 2, option c) would make the newest test window 7.7 years old. It changes little and costs a
   year. Keep the cut at 2020-01-01.

4. No finding on SPLIT-13 / USE-10 (recurring entities). Carriers recur and are a feature, as the use case needs.
   The worker is not identifiable after the birth year was dropped, and the same-accident links are 0.04%.

---------------------------------------------------------------------------------------------------------------
NOT RUN / LIMITS
---------------------------------------------------------------------------------------------------------------
* The labels as known at each window start do not exist; only a June 2021 copy does. The 12-14% share is an
  interpolation from that copy.
* No carrier-level recency feature test (the lt_vehicle style); the ladder covers the whole effect of the newest
  labels and shows no edge step.
* A model refit on the shipped 1M train sides was not run; the builder's probe and gap experiment cover the scale.
```

</details>

<details><summary>Domain practitioner</summary>

```text
DOMAIN PRACTITIONER REPORT: ny_wcb_assembled_claims (folder ny_wcb_assembled_claims_1m), 2026-11-09
Role: the actor of the use case. I sit at a New York workers' compensation carrier's lost-time claims desk (or the
Board's examining unit indexing a newly assembled case). When a claim is assembled I route it: fast track, or an
indemnity adjuster with nurse case management. Read-only (scripts in the run folder).

VERDICT
Fit: approximate (agree with the definition). One sentence: the rows, the moment (assembly) and the out-of-time
windows match my routing decision, but several inputs I always have at assembly are not in the table, the fields it
keeps are their 2026 values, and the label is the benefit type to date, not a fixed horizon (USE-8).
Metric scores my decision: partly. log_loss is a strictly proper score of the class probabilities I use, per claim,
the unit I act on (MET-8, MET-11 multiclass). It ignores the severity order, which matters little here, and it is
dominated by the cheap end of my decision. I would still keep it: no source fixes a cost or a k (MET-6, MET-7), and
an ordinal score ranks the models the same (numbers below).
Sex and age: keep both. No law I found bars either one from a claims-triage decision, and age is one of the factors
the Board itself weighs when it sets a non-schedule permanent award. Sex adds about 0.001 log loss; age adds 0.005
to 0.011.

1. AT ASSEMBLY, DO I HAVE THESE INPUTS?
Kept inputs I do have: accident date, assembly date, the C-2 and C-3 dates when they arrived before assembly (the
definition blanks later ones, LEAK-7: right), age, sex, home ZIP, industry, carrier and carrier type, county, district,
medical fee region, claim type and the WCIO cause, nature and body-part codes. These are FROI fields (eClaims 3.0 from
2014) or the Board's own indexing. Caveat: they are the 2026 values (builder issue 1). For June 2021 claims the WCIO
codes were filled later for 17% and changed for 4-7%. At my desk 7.5% of the claims would reach me with blank injury
codes, and those claims later ended PPD SCH LOSS 31% of the time against 7.6% overall. A model trained on completed
codes will meet blanks it never saw blank. I agree with option (a): keep the codes and name the gap. Dropping them
removes the core of my triage, and the gap stays (1.005 against 1.101 without them).

Inputs the definition rightly drops: the Board's AWW (adjudicated, positive for 0.2% of NON-COMP claims), the attorney
flag (the value now, changed for 28% of claims), hearing, controversy, ANCR and OIICS fields, status and highest
process. Without these drops I would not trust the task at all (LEAK-10, USE-3).

Inputs I always have at assembly that the table lacks. This is the largest gap, and `fit_reason` does not name it:
  a. Why the Board assembled the claim. The overview gives the reasons: more than one week of lost time, a serious
     injury that may be permanent, a dispute by the carrier or employer, a C-3 received, or a notice of claim action.
     This is the strongest routing signal I have. The table carries only one part of it (a C-3 dated on or before
     assembly).
  b. The employer-reported wage on the FROI (eClaims DN0062, the employer's estimate of AWW), the date disability
     began, and the lost time so far or a return to work. The carrier pays on these from day one.
  c. Whether the carrier has filed a denial (FROI-04/SROI-04) at assembly. The Board's "controverted" status needs a
     medical form, so no controverted date falls on or before assembly. The carrier's own denial does exist then.
  d. The occupation (DN0060), the injury narrative, the first medical report (C-4) and whether an attorney was on the
     claim at assembly (the table holds only today's flag).
None of these can be built from this table. Ask: add one sentence to `fit_reason` and the notes: "inputs the actor has
at assembly (the reason for assembly, the reported wage and lost time, the carrier's denial, occupation, narrative)
are not published". This is a known gap under USE-8, not a leak.

2. IS THE TARGET WHAT I ACT ON?
I act on severity: will the claim become lost-time, will it become permanent (PPD SCH, PPD NSL, PTD), and who should
work it. The benefit type is a reasonable proxy for that (USE-5 holds). It is not cost: PPD SCH LOSS covers anything
from a finger to an arm. It is also not the Board's own routing outcome. If the actor is the Board, the decision it
actually makes at assembly is the resolution path (administrative determination, conciliation or hearing), and that
is `highest_process`, set after assembly. As shipped, the target is also the type to date (FAQ 4: NON-COMP means "an
award for lost time has not yet been made"). From the 2014 cohort, about 12% of the eventual PPD NSL awards and 13% of
the PTD awards of the 2019 test claims may still be pending. Those claims sit in NON-COMP, TEMPORARY or PPD SCH LOSS
today. The release cut at 2020 (issue 2, option a) is the right trade.
What I want out of the model: a probability over the 7 classes. From it I compute P(lost time), P(permanent) and an
expected severity. A hard class would be of no use to me. The ordered `ordinal` declaration matches the codebook
(CLEAN-25).

3. ONE ROW, ONE DECISION; TEST DATA AS I FACE IT
One row is one assembled claim and one routing decision: yes (no unit weight is needed, MET-17). Test windows of new
claims after training: yes, this is what I face (USE-10: a new claim, no entity history; the worker's earlier claims
cannot be linked because the identifier is dropped and there is no worker key). Two differences from practice:
  - Training labels. A model refit on 2019-01-01 would know the 2017-2018 claims only with their labels as of that
    day, which are immature. The definition trains on 2026 labels with no gap (SPLIT-10). The builder measured what a
    two-year gap costs: 0.021 to 0.039 log loss, part of it drift. This flatters every method about equally, so it does
    not change rankings much. I can accept it as named in `splits_comment`.
  - Population. A carrier triages at first notice (FNOL), before the Board assembles anything, and sees medical-only
    claims that are never assembled. Assembled claims are the lost-time, serious, disputed or C-3 subset. For a
    carrier's lost-time desk, or for the Board, that subset is exactly what they see, so this is no gap for the actor
    as written. It would be one for an FNOL triage model.

4. WOULD I USE IT?
Yes, as a ranking aid for case-manager attention. What would make me trust it:
  - out-of-time windows (present);
  - the post-assembly fields gone (present; the raw dropped columns alone score macro AUC 0.75-0.88, so the drops
    mattered);
  - calibrated probabilities (log loss rewards these).
What would make me distrust it:
  - it was trained on injury codes that were completed after assembly (issue 1);
  - it lacks the lost-time and denial information I hold anyway, so in production I would stack it with those inputs;
  - recent training labels are not mature.
On my measure (below), the best model puts 60% permanent-award claims into its top 5%, against about 11% at random.

5. METRIC
Declared: Metric.fallback log_loss. The reason names where the builder looked (the Board's pages, Kaggle, a course
task with macro F1 on hard labels, rejected under MET-6). This is consistent with MET-1 and MET-11.

My check (scripts in the run folder). Three 2019 windows, 300k random training claims
before each window, 8 models: LightGBM full, a small LightGBM, and LightGBM without sex, without age, without both,
with the injury codes only, and without the injury codes, plus a one-hot logistic regression. Scores: log loss, the
ordinal ranked probability score (RPS), the AUC and precision at the top 5% for P(PPD SCH LOSS or worse) and for
P(PPD NSL, PTD or DEATH).
  - Log loss and RPS rank the 8 models identically in all 3 windows, except the bottom pair (injury-only against
    no-injury). The order-blindness of log loss does not change the choice of model here, so an ordinal score would
    add nothing.
  - P(permanent) AUC and precision at the top 5% follow log loss at the top. The full LightGBM is best on all three:
    log loss 0.868 / 0.871 / 0.895, AUC 0.856 / 0.857 / 0.851, precision 0.61 / 0.61 / 0.60. Class shares score
    1.058 / 1.062 / 1.078.
  - The expensive tail (PPD NSL, PTD, DEATH; 1.4% of claims) is where log loss and my decision part. The small
    LightGBM is 0.014-0.017 worse in log loss but beats the full one on tail AUC in 2 of 3 windows (0.844 against
    0.842; 0.851 against 0.845). The logistic model, 0.023-0.025 worse in log loss, ties the full one on that AUC in
    window 2 (0.8445 against 0.8448). The builder's TP-8 file agrees: PPD NSL, PTD and DEATH carry 6-7% of the log
    loss, while NON-COMP, MED ONLY and TEMPORARY carry 78-79%.
The metric I would choose in practice is an operational one: the AUC of P(PPD NSL or worse), or precision at the
number of nurse case managers I have. Both need a class cut or a k that no source fixes. Declaring either would mean
inventing the decision (MET-7: "never invent a cost or a threshold"; MET-9: the top-k score only when the source fixes
k). Verdict: partly. Keep log_loss. Optionally, the notes could say that log loss is driven by the NON-COMP / MED ONLY
/ TEMPORARY split, and that the severe tail ranks models slightly differently (numbers above).

6. SEX AND AGE AS INPUTS (the rais stance: a factor the actor's own law bars leaves the features)
Law, as far as I could find:
  - NY Insurance Law s2607 bars refusing to issue, cancelling or not renewing a policy because of sex or marital
    status. That is underwriting. The claimant in workers' compensation is not even the policyholder (the employer
    is).
  - NY DFS Insurance Circular Letter No. 7 (2024), on AI and external data, covers underwriting and pricing only. It
    says it "is not intended to address phases of the insurance product lifecycle other than underwriting and
    pricing" (para. 8).
  - Under the collection's "as if in the EU" stance, Directive 2004/113/EC Art. 5 (Test-Achats) bars sex as a factor
    in premiums and benefits. It covers only private, voluntary insurance separate from employment (recital 15;
    Art. 3(4) excludes employment and occupation). Statutory workers' compensation and a routing decision are both
    outside it.
  - I found no statute, regulation or Board rule that bars sex or age from a claims-handling or triage decision in
    New York.
  - Soft constraints: an insurer's AI governance (NAIC-style bulletins) asks for testing of disparate outcomes in
    claims. If the actor is the Board, a public body, routing by sex invites an equal-protection challenge. Neither
    bars the input.
Age is more than legal. The Board's 2012 Guidelines (ch. 9) set the loss of wage-earning capacity for a non-schedule
permanent award (PPD NSL) from the medical impairment, the functional loss and vocational factors, which include age.
Age is part of how the target class is decided, so dropping it would remove a determinant the decision-maker uses
(USE-6). Measured: without age, log loss rises 0.005 / 0.011 / 0.008 and the AUC on the expensive tail falls 0.012 /
0.013 / 0.017.
Sex: without it, log loss moves -0.0005 / +0.0017 / +0.0013 and the AUC on permanent awards moves -0.001 / -0.002 /
-0.001. It is legal, and the model barely uses it.
Recommendation: keep both (agree with the builder's issue 6). The pricing stance in principles.md (sex leaves
insurance pricing tasks) does not reach this task under its own wording or the rais extension, since no law of the
actor bars it. If the curator prefers a conservative line on sex for any insurance task, the measured cost of
dropping it is about 0.001 log loss, so either call is cheap.

GAPS BETWEEN THE DATASET AND THE REAL DECISION, ranked by how much they change the task
1. Inputs I hold at assembly and the table lacks: the assembly reason, the reported wage and lost time, the carrier's
   denial, the occupation, the narrative, C-4 and the attorney at assembly. Not fixable from this source. Name it in
   `fit_reason` (USE-8). Today `fit_reason` names only the 2026 values and the label to date.
2. The kept fields are their 2026 values (builder issue 1): measured 0.921 against 1.061 log loss on 2021 claims.
   Named in the notes and in `fit_reason`. Option (a).
3. The label is the type to date. For the 2019 test claims about 12-13% of the eventual PPD NSL and PTD awards may
   still be missing; the cut at 2020 keeps this small (issue 2, option a).
4. Training labels in hindsight (no SPLIT-10 gap): 0.021-0.039 log loss, about equal for every method. Named in
   `splits_comment`.
5. The target is a proxy for severity and cost (PPD SCH LOSS is wide). It is acceptable as a proxy (USE-5), and the
   7-class probability lets me derive the flags I use.
6. Population and moment: the assembled subset, not FNOL. This is no gap for the Board or a carrier's lost-time desk;
   it would be one for a carrier's FNOL model. The use-case text could say "the carrier's lost-time desk" to be exact.

WHAT AN EXPERT WOULD CHANGE
- Add gap 1 to `fit_reason` and to the first curation_comments bullet, as the inputs the actor has but the table does
  not publish.
- Write the actor precisely: "when the Board assembles a claim, the carrier's lost-time desk or the Board's examiner
  routes it". The Board's own decision at assembly is the resolution path, which this table carries only as a later
  outcome (`highest_process`).
- Keep the 7-class ordinal target, log_loss, sex and age. The notes could state the age rationale (LWEC vocational
  factor) beside the existing sex note, so a reviewer of the sex stance sees why both stay.
- No change to rows, split or cleaning from my seat. Issues 2-5 and 7 as the builder recommends.

SOURCES
- Source overview and FAQ: data.ny.gov jshw-gkgu attachment
  (the dataset page's attachment): assembly criteria, FAQ 4 (type to date), the AWW set through
  adjudication, controverted only with a medical form.
- NY DFS Insurance Circular Letter No. 7 (2024): https://www.dfs.ny.gov/industry-guidance/circular-letters/cl2024-07
  (read: scope para. 8; protected classes per Insurance Law Art. 26).
- NY Insurance Law s2607: https://nysenate.gov/legislation/laws/ISC/2607 (from search summaries).
- Directive 2004/113/EC: https://eur-lex.europa.eu/eli/dir/2004/113/oj/eng and
  https://www.legislation.gov.uk/eudr/2004/113/chapter/I/adopted (Art. 3(4), Art. 5, recital 15; from search
  summaries, the EUR-Lex page did not render).
- NYS WCB 2012 Guidelines (LWEC, ch. 9, vocational factors including age):
  https://WWW.WCB.NY.GOV/content/main/hcpp/ImpairmentGuidelines/2012ImpairmentGuide.pdf, and the Third Department
  decisions and a practitioner summary
  (https://www.fbrlaw.com/blog/workers-compensation/understanding-loss-of-wage-earning-capacity-in-new-york/) via
  search summaries.
- eClaims FROI/SROI element requirements (DN0062 wage, DN0060 occupation):
  https://www.wcb.ny.gov/content/ebiz/eclaims/ReqTables/NYS_R3_FROI_SROI_Data_Element_Req.pdf (via search summary).
- Industry claims triage at FNOL: https://docs.datarobot.com/en/docs/get-started/how-to/biz-accelerators/insurance-claims.html.md;
  https://www.guidewire.com/resources/blog/technology/the-claims-moment-of-truth-why-predictive-modeling-is-no-longer-optional
  (vendor sources).
- Fairness in WC claims AI: https://www.workerscompensation.com/additional-education-materials/ai-bias-in-workers-compensation-how-to-detect-prevent-and-prove-fairness/
- WCB reengineering (no current predictive triage found): https://www.insurancejournal.com/news/east/2013/08/23/302765.htm
- Builder: builder_report.md, probes/rare_class_share.json, probes/maturity_by_class.txt, probes/stats.txt.
- Rules: use_case.md USE-1, USE-3, USE-5, USE-6, USE-8, USE-10; metrics.md MET-1, MET-6, MET-7, MET-8, MET-9,
  MET-11, MET-17; principles.md Tensions row on "a factor the actor may no longer use"; SPLIT-10, LEAK-7, LEAK-10,
  CLEAN-25.
```

</details>

<details><summary>Blind review</summary>

```text
BLIND REVIEW: ny_wcb_assembled_claims (target claim_injury_type, multiclass, temporal on assembly_date)
Inputs used: the clean-room data and task note, the data.ny.gov dataset jshw-gkgu (columns.json, metadata, SODA API aggregate queries). No other local file was opened. (Scripts in the run folder.)

VERDICT: Include with changes. It is a real, honest-looking claim-triage task with moderate signal and a sensible leakage treatment, but the preparation needs documenting and a few fixes (row loss that I cannot explain, raw datetime columns, near-empty PTD/DEATH classes, snapshot-time features).

WHAT THE TASK IS
New York State Workers' Compensation Board (WCB) claims assembled 2015-01-02 to 2019-12-31. The prediction is made at claim assembly, the point where the WCB opens a case file ("The WCB 'assembles' a claim in which an injured worker has lost more than one week of work, has a serious injury that may result in a permanent disability, is disputed ... or receives a claim form from the injured worker (Form C-3)"). The target is the eventual benefit class: "Describes the claim injury in terms of the benefits awarded by Board ... from least to most severe": NON-COMP, MED ONLY, TEMPORARY, PPD SCH LOSS, PPD NSL, PTD, DEATH (CANCELLED has been removed). Real use: the WCB or a carrier triaging new claims (reserving, routing to adjudication, early intervention). This is the same framing as public student and competition projects on this data (the ML2425 project uses 2020-2022 data). The features are 17 at-assembly fields: accident, assembly, C-2 and C-3 dates; age; carrier name and type; claim type; county, district and medical fee region; gender; zip; industry; WCIO cause, nature and part of body. The post-assembly fields in the source (attorney, AWW, hearing count, IME-4 count, ANCR, controverted, PPD/PTD dates, current status, highest process, accident/OD indicators) were all dropped. That is the right choice.

SIGNAL (LightGBM, 200k sample, expanding window, train on everything before each test window; windows 2018H2, 2019H1, 2019H2, about 20-23k test rows each)
- Prior (train class frequencies) log loss: 1.074 / 1.074 / 1.057. Majority-class accuracy: 0.643 / 0.645 / 0.654.
- LightGBM with zip dropped and day-lag features: log loss 0.885 / 0.893 / 0.862, accuracy 0.679 / 0.677 / 0.690, OvR macro AUC 0.82 / 0.79 / 0.80, macro-F1 about 0.26.
- LightGBM with zip as a raw 5,700-level categorical: log loss 0.93-0.94. That is clearly worse, so handling high-cardinality categoricals separates the methods.
- Top gain: carrier_name 0.36, WCIO part of body 0.16, nature 0.14, cause 0.09, county 0.07, assembly-to-C-3 lag 0.06. No single feature dominates. There is no sign of leakage, and the task is not trivial.

CONCERNS (most to least serious)

1. Rows missing from the full table, in a pattern I cannot explain (data fidelity). In the source, 2015-2019 has 1,463,820 assembled claims, or 1,440,567 after removing "1. CANCELLED" (23,253). task.md says 1,298,680, so about 142k rows (10%) are missing. The loss is not uniform in time. The sample-to-source ratio is 0.130-0.139 in every month from 2015-01 to 2018-12 and 0.149-0.156 in every month of 2019, a sharp step at 2019-01 (the expected ratio for a uniform loss is 200,000/1,298,680 = 0.154). Within 2015-2018 the loss is uniform across district (0.133-0.137), target class and claim type. It is not explained by null accident date, age < 14, null WCIO or industry, gender U, or accident after assembly (all checked by API counts). Either an undocumented filter dropped about 12.5% of the 2015-2018 claims, or the table came from a different snapshot. Because the test windows sit in 2018-2019, a loss that differs between train years and test years is exactly the kind of thing that can bias a temporal benchmark. Change: document the filter or snapshot date, or rebuild from a stated snapshot so the counts reconcile.

2. Features are snapshot values, not values as of assembly (honesty; partly unverifiable). The source is a live, weekly-updated table that holds each claim's current record. Carrier name and type, WCIO cause, nature and part of body, industry, district and zip could have been filled in or corrected after assembly (e.g., through later EDI filings). WCIO fields are missing in only 1.4% of rows, and carrier_name is the top feature. The preparer did handle the obvious case. In the source, C-2 is after assembly for 123,773 rows (8.5%) and C-3 for 284,406 (19%). In the prepared data, the maximum (c2_date - assembly_date) and (c3_date - assembly_date) are 0 days, and c3 missingness is 89% vs 69% null in the source. So post-assembly form dates were evidently nulled. That is correct, but task.md does not say so, and the meaning of NaT changes from "never received" to "not received by assembly". Change: state this masking in task.md. Note in the task description that the categorical claim attributes are snapshot values. I could not check how often they change after assembly.

3. Extremely rare classes. In the 200k sample, PTD has 101 rows (0.05%) and DEATH 114 (0.06%). Each half-year test window holds only 7-14 of each. In the full table that is about 45-90 per window. Macro-averaged metrics (macro-F1, per-class AUC) will be noisy on those classes. DEATH is also a different kind of claim (filed under WCL s.16), not a severity grade of the injury. Change: score with log loss or a proper multiclass metric rather than macro-F1, or merge PTD+DEATH (or drop DEATH). The ordinal severity in the source codes could also support an ordinal metric.

4. Label definition shift inside the training range. MED ONLY falls from 21.9% of claims in 2015Q1 to 19.4%, 15.7%, 10.4% and then about 8% from 2016Q1 on, with NON-COMP rising from 45% to 64%. Source assembly volume also jumps from 174k (2013) to 259k (2014). This looks like an administrative or coding change around 2014-2015. It only affects early training rows, not the test windows, so it is a realistic drift. Still, models that weight all history equally pay for it. Change: start in 2016, or mention the drift in task.md.

5. Raw datetime columns (preparation). There are four datetime64 columns (accident, assembly, C-2, C-3). The useful signal is in the lags (assembly minus accident: median 10 days, max 20,351; assembly minus C-3; presence of C-2 and C-3), and in a temporal split the absolute dates only extrapolate. Many tabular pipelines will either drop the datetime columns or cast them to epoch integers. Change: add lag-in-days columns and keep or drop the absolute dates on purpose. Accident dates go back to 1959 and C-2/C-3 dates to 1996 for claims assembled in 2015+. These are plausible occupational-disease or late-assembled claims, not errors.

6. Messy high-cardinality categoricals. zip_code has 5,702 levels and includes non-US or garbage values ('M3K2B', 'H1V3S', '-7296', '19-30', '010'; 0.06% are not 5-digit). It is worker home zip, partly redundant with county, district and medical_fee_region. carrier_name has 1,744 levels. Unknown codes from the source (gender U, medical fee region UK, carrier type UNKNOWN, age 0) appear to have been mapped to NaN, which is fine. carrier_type keeps an unused category level ('5C...', count 0), which is harmless. Change: keep zip as a string/categorical but clean the non-5-digit values to NaN. Optionally keep a 3-digit zip.

7. Minor. Only 2 exact duplicate rows in the sample, and no conflicting duplicates, so cross-split copies are not an issue. There is no worker identifier, so I cannot check whether the same worker has several claims across train and test. claim_type has 4 levels, including NON-WC (66 rows) and volunteer claims. That is fine, but they are somewhat different processes.

COULD NOT CHECK
- The exact filter or snapshot that produced 1,298,680 rows (concern 1), and the actual test-window boundaries and sizes (task.md says only "3 test windows").
- Whether categorical attributes (carrier, WCIO codes, industry, district) are as-of-assembly or later-corrected values. No history is published.
- Whether labels for 2019 claims are fully mature. At a 2026 snapshot that is about 7 years of development, which is probably enough, but PPD classifications can arrive late.
- Repeat claimants across splits (no worker ID).
- I only worked on the 200k sample, not the full 1.3M rows.

Sources: https://data.ny.gov/d/jshw-gkgu ; https://data.ny.gov/api/views/jshw-gkgu/columns.json ; https://catalog.data.gov/dataset/assembled-workers-compensation-claims-beginning-2000 ; https://github-users.yhajoa.workers.dev/DiogoGAndrade/ML2425_ToGrantOrNotToGrant (student project with the same target on 2020-2022 data).
```

</details>

<details><summary>Task gamer</summary>

```text
TASK GAMER REPORT: ny_wcb_assembled_claims (claim_injury_type, 7-class log loss, 3 temporal 4-month windows in 2019)

Verdict: the task as shipped cannot be gamed in any measurable way. No exploit beats the best honest model by more
than the seed noise (about 0.0003 log loss). The preparation already masks the post-assembly dates and drops the
post-outcome columns. The one large swing on this task comes from the model, not from a leak: an unregularised
LightGBM is unstable on the rare classes.

Scripts in the run folder. The splits are r0f0 = Sep-Dec 2019,
r1f0 = May-Aug 2019 and r2f0 = Jan-Apr 2019, each with 1,000,000 training rows.

------------------------------------------------------------------------------------------------------------
HONEST MODELS (mean log loss over 3 splits; per split r0f0 / r1f0 / r2f0)
------------------------------------------------------------------------------------------------------------
untuned LightGBM, raw features (RAW=1 baseline.py)        0.8913  (0.9201 / 0.8611 / 0.8927)  unstable
regularised LGB, raw features (honest2.py base_reg)        0.8524  (0.8416 / 0.8473 / 0.8682)
 + zip/carrier as numeric codes (base_stable)              0.8455  (0.8375 / 0.8390 / 0.8599)
   seeds 1 and 2 / random-noise column                     0.8456 / 0.8453 / 0.8455  -> noise spread ~0.0003
 + date lags, day of week (lags_stable)                    0.8397  (0.8315 / 0.8344 / 0.8533)
 + frequency counts of zip/carrier/county/industry,
   computed on training rows only (counts.py cat_train)    0.8371  (0.8284 / 0.8318 / 0.8512)  <- best honest

Note on the baseline: an unregularised LightGBM multiclass (min_sum_hessian 1e-3, no L2) diverges on the rare
classes (DEATH 0.04%, PTD 0.04%). Its test loss on r0f0 goes 0.863 (100 rounds) -> 0.883 (300) -> 0.930 (500).
Seeds and near-identical feature sets then move a split by up to 0.05. With min_sum_hessian_in_leaf=1 and
lambda_l2=10, two seeds agree within 0.0004. Every exploit below is measured against the regularised models.

------------------------------------------------------------------------------------------------------------
EXPLOITS RANKED BY GAIN (against lags_stable 0.8397 and against the best honest model 0.8371)
------------------------------------------------------------------------------------------------------------
| # | Exploit | Script | Honest | Exploited | Gain per split | Deployed model has it? | Fix |
|---|---|---|---|---|---|---|---|
| 1 | Category counts over all rows incl. the test window | counts.py cat_all | 0.8397 | 0.8372 | +0.0025/+0.0022/+0.0028 | Yes: training-only counts give the same 0.8371. Signal, not leak | none |
| 2 | Future claims with the same accident date + carrier/zip, and claims for that accident date assembled later | exploits.py window_density; counts.py cat_train_window | 0.8397 / 0.8371 | 0.8391 / 0.8372 | +0.0007/+0.0010/+0.0002 on lags; -0.0003/-0.0002/+0.0002 on best honest | No (uses later rows) | none needed: within noise |
| 3 | Same person (gender, zip, birth year) or same accident: number of later claims | exploits.py person_future; counts.py cat_train_future_person | 0.8397 / 0.8371 | 0.8394 / 0.8373 | +0.0000/+0.0009/+0.0000; -0.0006/+0.0003/-0.0001 | No | none needed |
| 4 | Final label of an earlier training claim of the same person or accident | label_lookup.py pkey/akey | 0.8397 | 0.8398 / 0.8396 | ~0 | Partly (its status then, not its final label) | none needed |
| 5 | Prior shift to the test window's class rates (oracle bound, uses test labels) | prior_shift.py | 0.8397 | 0.8414 (worse) | -0.0009/-0.0015/-0.0026 | No | none needed. EM estimate of the test prior diverged (2.05) |

None of these is a usable flaw. The only gain above noise (#1) is honest frequency encoding.

------------------------------------------------------------------------------------------------------------
FLAWS THAT HURT AN HONEST MODEL
------------------------------------------------------------------------------------------------------------
None found. The 2015 training rows carry a different label mix: 2015Q1 is 45% NON-COMP and 22% MED ONLY, against
about 64% and 8% from 2016 on. This looks like a coding or policy change. Dropping 2015 does not help, though
(lags_stable 0.8397 vs lags_stable_drop2015 0.8404). Training on only the last 24 or 12 months is worse (0.8451,
0.8560). The model handles the shift through assembly_date.

------------------------------------------------------------------------------------------------------------
WHAT THE PREPARATION DID (kit vs the public source, data.ny.gov jshw-gkgu, via the SODA API)
------------------------------------------------------------------------------------------------------------
- Columns that exist only after the outcome are dropped: Attorney/Representative, IME-4 Count, First Hearing Date,
  Average Weekly Wage, ADR, Agreement, WCB Decision, Hearing Count, Highest Process, PPD/PTD dates,
  Interval Assembled to ANCR, Current Claim Status, Claim Identifier. These carry the known "magic" signal for
  this source. They are absent here.
- C-2, C-3 and accident dates later than assembly_date are set to missing. Source, 2017: 54k C-3 dates and
  22.5k C-2 dates fall after assembly. Kit: none after assembly in any year, and missing counts match
  (masked rows + truly blank) x subsample rate. So c2/c3 presence is what was known at assembly.
- CANCELLED claims are removed (about 1.5%/yr).
- 2019 (all test windows) is kept nearly whole. 2015-2018 are subsampled to about 87-88%, evenly by class,
  except NON-COMP, which is about 1.3 points lower in every year including 2019. So a small filter on some
  NON-COMP rows exists, the same in train and test.
- Looking rows up in the published file is possible: the source has the label and the post-outcome columns.
  That holds for every public dataset and is not ranked.

------------------------------------------------------------------------------------------------------------
ATTACKS THAT FOUND NOTHING
------------------------------------------------------------------------------------------------------------
- Row order: the rows are sorted by assembly_date and shuffled within the day. The compensable rate is flat
  across within-day position deciles (0.372-0.377). Next-row label agreement is 0.4429, and 0.4430 after a
  within-day shuffle.
- Exact copies: 131 rows have identical features. Same-accident keys (accident date, age, gender, zip) cover 2%
  of rows, with 60% label agreement inside a group. The lookup gives no gain (#4).
- Day-level counts (claims assembled the same day, test included): 0.8398 vs 0.8397. Accident-date counts over
  all rows: 0.8397. Past-only accident-date counts: 0.8397.
- Train vs test classifier (r0f0, absolute dates removed): AUC 0.634 vs all training rows and 0.579 vs the
  last 4 training months. The drift is in WCIO cause, county and industry mix. It points to nothing usable.
- Formats: age is whole numbers only. Zip is 5 digits for 99.94% of rows. The non-5-digit zips have 0.5%
  DEATH vs 0.04%, but cover 300 rows. Missing-value patterns are strong: carrier missing -> 97% NON-COMP,
  WCIO missing -> 94% NON-COMP, c2 missing -> 41% NON-COMP, c3 present -> 35% NON-COMP. All of these are
  facts known at assembly once the dates are masked as above.
- Transforms over all rows: none present. The values are raw dates, raw categories and raw age.
- Web: no Kaggle forum, leak thread or write-up was found for this source. The known strong fields of the
  source are dropped.

------------------------------------------------------------------------------------------------------------
WHAT I COULD NOT CHECK
------------------------------------------------------------------------------------------------------------
- Label maturity: claim_injury_type is the final status at the source snapshot. A model deployed in Sep 2019
  would train on claims assembled in, say, Aug 2019 with their status as of Sep 2019, which is often still
  undecided. Every participant gets these better training labels; that needs a historical label snapshot to
  measure. The fix would be to drop training rows assembled within N months of the test window start, or to
  use as-of labels.
- Whether WCIO codes, industry and carrier hold their values as first reported at assembly or later
  corrections. The source keeps only current values. WCIO missing -> 94% NON-COMP could partly mean "never
  developed". The deciding fact is the WCB's EDI timing for these fields.
- Which rows the extra ~1.3% NON-COMP filter removed.
```

</details>

<details><summary>Precedent check</summary>

```text
PRECEDENT CHECKER REPORT: ny_wcb_assembled_claims (folder ny_wcb_assembled_claims_1m), 2026-11-09

Read: principles.md; leak_checks.md (LEAK-6, -7, -10, -11, -24, -25, -38, Mechanisms table); task_probes.md (TP-1 to
TP-10, Cases); use_case.md (USE-4 to USE-8, USE-12); selection.md (SEL-1, markers); definitions.md ("the _1m
version"); dataset.py; the record (CC 2026-11-08); builder_report.md; column_auditor and blind_reviewer reports;
probes/field_stability.txt, snapshot_feature_sets_harmonised.log, snapshot_feature_test_wcio.log; register.json (flags
and decisions); this batch's kumc_inpatient_aki_prediction mediator report and rais_employment_separation mediator and
precedent-checker reports; the records of distribution_transformers_at_cauca_department and onlinenewspopularity.
Nothing run beyond reading; no file edited.

=======================================================================================================================
SUMMARY
=======================================================================================================================
D1 Keep the kept fields at their 2026 values with a note (builder issue 1 (a), implemented)
   -> NOT REASONABLE UNDER THE RANKING: departs from a Must (LEAK-10 clause 2) without a fact that sets it apart; only
      an amendment could carry it, and Lennart declined that amendment on 2026-10-21. Reflection prompt below.
D2 What follows if the honest task is thin (about 0.05 log loss of skill)
   -> Drop the late fields and ship (fit approximate) is CONSISTENT (TP-2, USE-12, the "real task against a leak" row).
      Retirement as `No` DEPARTS WITHOUT A FACT (no marker fits; LEAK-10's retire clause does not apply). A later
      prediction point DEPARTS (TP-6/USE-4: no stage the source defines; our own invention).
D3 Target (benefit type to date, 7 classes, CANCELLED / ADR / PFL rows dropped) -> CONSISTENT. One wording point:
   fit_reason lists the 2026 values as a gap, which departs from USE-8 as amended 2026-10-21 (fix, no decision).
D4 Protected grounds
   sex  -> CONSISTENT with the Tensions row as written (pricing only); OPEN under the rais extension proposed in this
           batch, and no fact has been read either way (New York law for the Board or a carrier). Prompt below.
   age  -> CONSISTENT (insurance never drops age; a fact exists: age is part of the Board's own wage-earning-capacity
           assessment, column auditor; the source of that fact still to be cited).
   ZIP  -> CONSISTENT (a P1 weigh; no decided precedent coarsens a published ZIP).
D5 Accident dates after assembly set to missing -> remedy CONSISTENT (located late cells blanked: zillow_prize,
   melbourne_housing_market); the stated reason is WRONG (CLEAN-11 "impossible" -> LEAK-10/LEAK-7, Board-set dates of
   disablement); residual missingness signal 0.0009 to be measured against noise (LEAK-6, kumc). Fix, no decision.
D6 Row count vs the source (blind reviewer: about 12% of 2015-2018 missing) -> CONSISTENT: exactly the documented
   `_1m` row budget. No fidelity issue.

Drift: none on LEAK-10 clause 2 (Lennart's line is uniform since 2026-10-21: keep only where the trace shows none).
Third exception: none; a keep here would be the first clause-2 keep with a traced gain.
Register flags checked and not relevant here: exception_to_must LEAK-10 (loan_default_prediction_imperial_college, a
drop, Andrej 2026-11-03); drift "post-outcome feature" (a keyword match on the nfip duplicate CCs, no LEAK-10 call);
opposite_outcomes USE-5 (diabetes_3 / chicago keep vs xente `No`: label construction, not this question).

=======================================================================================================================
D1. The kept fields are their 2026 values (P4, LEAK-10 Must, clause 2)
=======================================================================================================================
Decision checked: dataset.py keeps wcio_cause/nature/part_of_body, industry, carrier_name/type, age_at_injury,
accident_date, zip_code, district_name, medical_fee_region at their 2026 values with a "Potential leak, kept on
purpose:" note; builder recommends (a) keep; frames it as "LEAK-10 Must against LEAK-11".

The rule (leak_checks.md, LEAK-10, clause 2, amended 2026-10-26, Lennart): a value read at a later pull "goes where its
late cells can be located: they are blanked ...; where they cannot be located row by row, the values go when they may
carry a gain (distribution_transformers_at_cauca_department) and stay with a note only when the part that can be
traced shows none (onlinenewspopularity)". Each clause is "a case-by-case judgment of the curator, never a default".

Facts that matter (all measured by the builder or the column auditor):
 * Late cells cannot be located for 2015-2019 (one later copy only, June 2021, near-assembly for claims of
   April-June 2021).
 * The traced part shows a gain: swapping in the June 2021 values for 44,534 young claims, 0.921 -> 1.061 (class
   shares 1.118); WCIO codes alone 0.071; carrier name 0.008 (harmonised); age 0.006; accident lag 0.006; industry
   0.002; the rest <= 0.003 (snapshot_feature_sets_harmonised.log). Even on rows whose WCIO codes were filled in June
   2021, 2026 values 0.936 vs June 2021 values 0.973 (snapshot_feature_test_wcio.log): changed values carry gain,
   not only the fill.
 * A mechanism ties the change to the outcome: fields blank near assembly and filled later belong to severe claims
   (44-64% PPD SCH LOSS vs 9.5%); fields still blank in 2026 are dead claims (85-98% NON-COMP). The meaning of a blank
   flips between the two snapshots (column auditor [1]).
 * Share of the skill on these fields: 0.880 all -> 1.011-1.021 without them vs 1.066 class shares (2019 windows):
   70-75% of the skill.

Precedents (dates, curator):
 * distribution_transformers_at_cauca_department (CC 2026-10-21, Lennart; leak_checks.md Mechanisms row "decision"):
   power_kva and installation_type, looked up during or after 2020, changed for an unknown subset of the positives;
   ROC AUC 0.701 -> 0.639 when dropped; dropped, "LEAK-10 as written, no amendment for a gain that may sit on the
   changed rows". CLOSEST PRECEDENT; same mechanism (an attribute of a thing that existed at the prediction point,
   stored at its later value), same untraceability, a larger gain here.
 * onlinenewspopularity (CC 2026-10-26, Lennart, "go with (a)"): kept because masking the traced cells changed R^2 by
   -0.0004. Kept on a null trace; here the trace is not null.
 * medical_facility_operational_data (CC 2026-11-05, Lennart): kept; the whole-field worth sat within about two seed
   SDs, so the late part showed no gain; the Cases row says "Unlike distribution_transformers_at_cauca_department".
 * tunisian_fraud_detection_challenge (CC 2026-11-05, Lennart): 22 registry fields kept because no mechanism ties a
   registry change to the outcome; CTR_CESSAT dropped where one did (+0.015 RMSE). Here a mechanism exists (blanks
   filled by later filings on claims that grew), so the case sits with CTR_CESSAT, not with the 22 fields.
 * house_sales ("the King County lesson"), zillow_prize, melbourne_housing_market (2026-10-21): looked-up attributes
   kept only where the data shows they did not change; located late cells blanked. Here the data shows they changed.
 * kumc_inpatient_aki_prediction (this batch; mediator 2026-11-09, AI, not yet decided by the curator): 26
   procedure-defined DRG groups dropped on gains of +0.0029 (SE 0.0007) and +0.0041 (SE 0.0006), "change now, no
   decision needed"; keeps only where the traced part shows none.
 * santander_customer_transaction_prediction (CC 2026-09-30) under LEAK-6: "a confirmed leak goes even when small"
   (+0.003 AUC).
 * noaa_storm_events_damage (2026-11-08, Lennart, X4): "The size of the worth alone never decides."

LEAK-11 vs LEAK-10: the builder's framing does not hold. LEAK-11 (Should; narrows LEAK-10) keeps a late value "that
weakens the signal" (south_africa_coronary_heart_disease: dropping sbp and obesity raised AUC 0.774 -> 0.778). Here
the late values strengthen it (0.921 vs 1.061). LEAK-38 does not apply either: it covers fields whose timing "no test
can establish" in data the owner released for its own competition, and says "A field whose timing is known to be late
... is LEAK-10's"; the FAQ and the snapshot comparison establish the timing.

Distinguishing facts offered, checked:
 * "the codes describe the injury, which exists at assembly": true of the injury, not of the stored code. It holds
   equally for distribution_transformers (the rating existed at the burn), house_sales (the house existed at the sale)
   and kumc's comorbidities; it does not set this case apart.
 * "dropping them leaves the triage without its core": a statement of worth; X4 (2026-11-08) says size never decides,
   and the Tensions row "a real task against a leak" says fix the leak and keep the task ("a very real task ... does
   not carry a leak", principles.md How to decide 3).
 * "part of the gap is a model trained on completed fields meeting incomplete ones": a fair caveat on the size of the
   traced gain, not on its existence; the rows filled at assembly still show 0.973 vs 0.936, and the blank flip is an
   outcome mechanism on its own. The rule's bar is "may carry a gain".
 * Untested candidate (the AI's best guess, option (a) below): if the actor is the insurer, it files the First Report
   of Injury with the WCIO codes itself, so the codes exist in its own system at or before assembly, and the Board's
   late fill would be a receipt lag. Against it so far: the filled-later claims are the severe ones (a later filing
   tied to benefits), and values changed on rows already filled. It would need a test (are the near-assembly blanks
   the claims without an employer report by assembly?) and then an amendment, since LEAK-10 is a Must.

Ranking: LEAK-10 is a P4 Must; nothing of higher rank keeps the fields (USE-12 says the task stays, not the leak).
A Must has no exceptions (principles.md, Exceptions and amendments). So (a) as implemented is not a reasonable
exception; it is either a fact that takes the fields out of the rule, or an amendment.

Partial keep: the rule lets a field with no traced gain stay with a note (zip_code, district_name, medical_fee_region,
carrier_type, gender, county, claim type: swaps <= 0.003 or at noise). For age (0.006), accident date (0.006) and
carrier name (0.008), no SE is given; kumc decided on paired SEs (10/10 folds). Facts first (EV-1): a paired bootstrap
SE over the 44,534 young claims settles which of the three go.

Reflection prompt (issue shape, for REVIEW.md issue 1):

   **Consistency check (AI, 2026-11-09):** Do the injury codes, industry, insurer name, age and accident date leave the features, as distribution_transformers_at_cauca_department's late attributes did, or what fact sets this claims task apart?

   * **Problem:**
     * The table holds each claim's 2026 values, and for claims seen weeks after assembly the injury codes were filled later for 17% and changed for 4-7%, mostly on claims that became severe[^d1trace].
     * Swapping in the near-assembly values moves the log loss from 0.921 to 1.061 (class shares 1.118), and these fields carry 70-75% of the task's skill[^d1skill].
     * On 2026-10-21 you kept the rule as written for late attributes with a gain, and every keep since rested on a trace that showed none[^d1rule].
   * **Consistency:** distribution_transformers_at_cauca_department dropped its looked-up rating and installation type (ROC AUC 0.701 to 0.639); onlinenewspopularity and medical_facility_operational_data kept theirs because the traced part showed no gain; in this batch kumc_inpatient_aki_prediction drops 26 procedure groups on gains of 0.003 and 0.004[^d1prec].
   * **Effect on the task:** without these fields the 2019 windows score 1.011 to 1.021 against 1.066 for the class shares, a small real signal that stays a valid task[^d1tp].
   * **Unknown:** whether age, accident date and insurer name (0.006 to 0.008 each) are above noise; a paired standard error on the 44,534 young claims settles it.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | a | Keep on a fact: the insurer files the first report with the injury codes itself | test that the near-assembly blanks are the claims without an employer report by then; if so, keep and record the fact with an amendment for values the actor itself records | keeps the triage's core; the use case names the insurer | the data points the other way so far (filled-later claims are the severe ones; values changed on rows already filled); needs an amendment of a Must |
     | b | Treat it like distribution_transformers_at_cauca_department | drop the three injury codes, industry, and whichever of insurer name, age and accident date shows a gain above noise; fit stays approximate, as a task changed a lot to avoid a leak | follows the rule and every precedent; an honest triage at assembly | skill falls to about 0.05; the task loses the injury description |
     | c | Reopen distribution_transformers_at_cauca_department to match a keep | keep the fields here and restore power_kva and installation_type there (and keep kumc's procedure groups) | one line for all looked-up attributes | reverses your call of 2026-10-21; scores that reward late information in three datasets |
     | d | Amend the rule | late values with a measured gain may stay with a note when they describe a fact that existed at the prediction point | an explicit, deliberate change | almost every looked-up attribute qualifies; the clause's protection is gone |
     | e | Keep with the note, no fact (implemented) | as now | no change | an open departure from a Must with no fact recorded |

   * **Recommendation:** b, after the standard-error check for insurer name, age and accident date (any at noise stays under the note). **Decision:** a, b, c, d or e?

   **Notes for the AI:** (b) is drop_columns of wcio_cause_of_injury, wcio_nature_of_injury, wcio_part_of_body, industry
   (and the measured ones of carrier_name, age_at_injury, accident_date) in step 9, the notes' "Potential leak" bullet
   rewritten with the numbers, task_summary.known and fit_reason updated, the snapshot experiment re-run for the
   remaining fields; a kept field with no traced gain stays under the clause-2 note (onlinenewspopularity wording).

   [^d1trace]: probes/field_stability.txt (claims assembled 2021-06-01 to 2021-06-18, June 2021 copy vs 2026); column auditor [1]: filled-later fields 44-64% PPD SCH LOSS against 9.5%, still-blank fields 85-98% NON-COMP.
   [^d1skill]: probes/snapshot_feature_sets_harmonised.log (all with WCIO: 0.9211 vs 1.0607; all WCIO from 2021: 0.9916); column auditor [1] (2019 windows: 0.880 all, 1.011-1.021 without the fields, 1.066 class shares).
   [^d1rule]: **LEAK-10** (Must), clause 2, amended 2026-10-26 (Lennart): late values whose cells cannot be located "go when they may carry a gain ... and stay with a note only when the part that can be traced shows none"; a case-by-case call, never a default. **LEAK-11** (Should) narrows it only for values that weaken the signal. A Must has no exceptions (principles.md, Exceptions and amendments).
   [^d1prec]: distribution_transformers_at_cauca_department, CC 2026-10-21 (Lennart): "LEAK-10 stays as written ... power_kva and installation_type stay dropped"; onlinenewspopularity, CC 2026-10-26 (Lennart), "go with (a)", masked R^2 change -0.0004; medical_facility_operational_data, CC 2026-11-05 (Lennart), worth within two seed SDs; kumc_inpatient_aki_prediction, mediator 2026-11-09 (AI); **LEAK-6** (Must): a confirmed leak goes even when small (santander, +0.003).
   [^d1tp]: **TP-2** (Should): a small but real signal is no reason to retire (forest_fires, R^2 0.013); **USE-12** (Must): a leak is no reason to reject a real task; **USE-8**: approximate for "a task changed a lot to avoid a leak" (house_sales, sarcoma).

=======================================================================================================================
D2. If the honest task keeps about 0.05 of skill: ship, retire, or move the prediction point?
=======================================================================================================================
 * Ship after the drop (option b of D1): CONSISTENT.
   - TP-2 (Should): "A small but real signal is no reason to retire, and neither is a cutoff on the best skill."
     forest_fires kept at R^2 0.013 (2026-10-06); acquire_valued_shoppers_challenge (best AUC 0.654), hr_analytics
     (ROC AUC 0.62-0.63, 2026-10-14), noaa_storm_events_damage (2026-11-08) kept with low ceilings. Here 1.011-1.021
     vs 1.066 (about 4-5% of the class-share loss) on all three 2019 windows: more than forest_fires.
   - Tensions "a real task against a leak" (kickstarter: staff_pick dropped, task kept) and USE-12 (Must).
   - Tensions "the right split against the score" (forest_fires): a small signal under the honest setup is no reason
     to retire.
   - TP-1/TP-3: the 0.05 is untuned LightGBM on 300k rows; check against tuned methods before calling it thin.
   - USE-8: fit approximate, now also "a task changed a lot to avoid a leak" (house_sales, sarcoma).
 * Retire as `No`: DEPARTS WITHOUT A FACT.
   - LEAK-10's only retire clause is "when the features summarise a window that ends at the outcome and no common
     prediction point can be rebuilt" (iranian_churn). Assembly can be rebuilt; the clause does not apply.
   - No marker fits: `No Good Target / Scientific Discovery` is for the target (mutual_funds_india was retired
     2026-10-14 because its label was a shared trailing window, not for thin skill); `Data Quality Issue` is for
     damage that cannot be undone (LEAK-27, PROV-3; xente 2026-11-04 on a measured setup flaw); `Trivial`/`Too Small`
     do not apply (TP-8: PTD and DEATH carry 0.4-0.7% of the loss each, like mic). The nearest is `Not
     Representative` ("the task or its setup does not represent the real application"), with the fact "without the
     injury description the features are not what a triage desk reads". That would be the first use of the marker
     for this reason, and TP-2 asks for "a concrete reason found in the task itself"; it is a curator call, not a
     precedent-backed outcome. USE-8 already answers this kind of gap with fit approximate, not exclusion.
 * A later prediction point: DEPARTS.
   - USE-4/TP-6 move a task only to "the stage the source describes" (eryhemato_squamous_disease); "a fix of our own
     invention ... is not a better version" (TP-6). The source's later stage is ANCR, reached by about 39% of claims
     and by the compensable ones (selection on the outcome, LEAK-22). A fixed maturity (say one year after assembly)
     is our invention, and the dropped process fields (hearings, attorney, wage) would be known then but are stored
     only at their 2026 values, so the timing problem moves rather than goes. Data point for the curator: for claims
     of June 2020 seen in June 2021, WCIO nature was 95.2% filled against 96.2% in 2026 and changed for 2.5%; their
     benefit type still changed for 19% by 2026.

=======================================================================================================================
D3. The target: claim injury type, a benefit class (P3, USE-5)
=======================================================================================================================
CONSISTENT.
 * USE-5: the source's own documented label ("the benefits awarded by Board ... from least to most severe", checked
   against the codebook); it is what a routing desk acts on at coarser resolution (fast track vs case management),
   and TP-6/TP-7 bar a merge of our own invention (audiology_diagnosis, eryhemato). The blind reviewer's PTD+DEATH
   merge or DEATH drop would depart from TP-6/TP-8 (rare source classes carrying their share stay: mic, 2026-10-12;
   here 0.4-0.7% of the loss each).
 * Rows: CANCELLED dropped (no injury outcome, USE-5, as the screening said); ADR dropped (Board awards nothing on
   them: 99.97% NON-COMP; located by a flag known at assembly, 2 of 3,055 changed) follows LEAK-25 as amended
   2026-10-21 (Lennart: caracas_cervical_cancer, account_debt_south_africa, fraud_detection_..._1m: unrecorded rows
   located by a rule that does not read the label, dropped); not a selection on the future (LEAK-22), since the flag
   is set at assembly. PFL dropped (not injuries).
 * Label to date (FAQ 4): LEAK-24 cut at 2020 (sf_permit_time, consumer_complaints) and fit approximate for a label
   without a stated horizon (alfa_battle_2_0_task_2, USE-8). Consistent.
 * Ordered target in the codebook's order: CLEAN-25 / PR #37 (2026-11-01). Consistent.
 * One wording departure (fix now): fit_reason names "Several fields are the 2026 values ... changed after assembly"
   as part of the gap. USE-8 as amended (onlinenewspopularity CC 2026-10-21; house_sales CC 2026-10-21): a kept leak is
   named in fit_reason "as kept, not as a gap". Under D1 (b) the sentence becomes the task change instead.

=======================================================================================================================
D4. Protected grounds: sex, age, ZIP (P1 SEL-1; Tensions row "a factor the actor may no longer use")
=======================================================================================================================
sex (gender kept; notes: "claims triage, not pricing, so the insurance-pricing stance on sex does not apply")
 * The row as amended 2026-11-08 (Lennart): "sex leaves the rating factors of every insurance pricing task, whatever
   the actor's jurisdiction, as if the actor priced in the EU". Its letter covers pricing only. Keeping sex here does
   not break the row as written: CONSISTENT with its letter.
 * Its reasoning (bemtpl97, CC 2026-11-05: models "would not be able to use sex" in the current world) is about the
   actor's legal constraint. Nobody in this panel has read what New York law (or the EU rule the stance imitates)
   says about sex in claim handling by the Board or a carrier. The builder's reason is a scope reading, not a fact
   about the actor.
 * This batch: rais_employment_separation's mediator (2026-11-09, AI) asks Lennart to extend the row to "decisions
   ... where the actor's own law bars the factor" (Lei 9.029/1995; five grounds dropped, cost 0.006-0.007 ROC AUC);
   wioa_employment_after_exit_1m keeps its grounds on a fact (DOL's own adjustment model uses them); rais's precedent
   checker rated ny_wcb's reason "weaker". home_credit_default_risk and credit_card_clients_default keep sex, marked
   "not reviewed yet".
 * Status: consistent today; if the curator confirms the rais extension, keeping sex here needs a fact (the actor's
   law does not bar it, or the actor uses it), which is missing. Per the per-dataset rule this is its own REVIEW.md
   issue, decided next to rais issue 1. Effect of dropping sex alone: not measured (one fit; rais's four grounds cost
   <= 0.001).
age (kept) -> CONSISTENT. Insurance never drops age (lawful under the EU rule); rais drops it only because Brazil's
   law lists it. Here there is a fact of the wioa kind: age enters the Board's own judgement of wage-earning capacity
   (column auditor [2]; cite the source, e.g. the Board's impairment and loss-of-wage-earning-capacity guidelines,
   before relying on it). Note age is also in D1's traced group (2% changed, swap 0.006): D1 may remove it anyway.
ZIP (kept) -> CONSISTENT. A P1 weigh, not a Must: the state publishes it at this resolution, and no decided case
   coarsens or drops a published ZIP (house_sales keeps a property ZIP). Coarsening to 3 digits is the mild option if
   the curator weighs re-identification higher; no precedent requires it. CLEAN-11: '-7296' to missing (column
   auditor [6]).

Reflection prompt (issue shape, REVIEW.md issue 6):

   **Consistency check (AI, 2026-11-09):** Does sex stay a feature of a claim-routing task, and on which fact, if the stance on factors the actor may not use reaches beyond pricing?

   * **Problem:**
     * You dropped sex from every insurance pricing task because models in today's world could not use it, and the builder keeps it here because routing a claim is not pricing[^d4row].
     * In this batch the rais_employment_separation panel asks you to extend the stance to any decision where the actor's own law bars the factor[^d4rais].
     * No one has read what New York law, or the European rule the stance imitates, says about sex in claim handling by the Board or an insurer.
   * **Consistency:** bemtpl97, australian_vehicle_insurance_2004_2005, pricing_game_2017_french_mtpl, frempl_french_motor_personal_line and spanish_homeowners_motor_insurance_2010_2014 dropped sex; wioa_employment_after_exit_1m keeps its grounds because the agency's own model uses them; home_credit_default_risk and credit_card_clients_default keep sex, not reviewed yet.
   * **Effect on the task:** not measured yet; one fit without sex settles it (the four non-age grounds of rais cost at most 0.001 ROC AUC).
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | a | Keep on a fact: no New York rule bars sex in claim handling and the decision sets no price or benefit | read the law first, then keep with the fact in the notes | keeps the data's signal; a stated reason | the fact is not established; a routing that treats men and women differently is close to the stance's concern |
     | b | Drop sex, as the stance extended | gender leaves the features | follows the stance's reasoning and the rais proposal; likely a tiny cost | first claims-handling case; sets the line for wioa and the credit tasks |
     | c | Keep, recorded as the stance's scope: pricing only | the Tensions row says so; wioa, rais and the credit tasks follow | one clear line | cuts against the rais proposal and the reasoning of bemtpl97 |
     | d | Keep with the note, no fact or row (implemented) | as now | no change | a new case of a listed tension with no recorded reason |

   * **Recommendation:** b if you confirm the rais extension, else c; decide both in the same review. **Decision:** a, b, c or d?

   [^d4row]: principles.md, Tensions, "A rating factor known at the prediction point against a factor the actor may no longer use" (P3 and P4; **USE-1**, **USE-6**), amended 2026-11-08 (Lennart): "as if we were to simulate the case in europe always"; bemtpl97 CC 2026-11-05. **SEL-1** (Must): a task with ethical concerns is out.
   [^d4rais]: rais_employment_separation panel, mediator report 2026-11-09, issue 1 (Lei 9.029/1995 art. 1); a pending recommendation, not a curator decision.

=======================================================================================================================
D5. Accident dates after assembly (3,039, set to missing)
=======================================================================================================================
 * Remedy: CONSISTENT with "located late cells are blanked" (LEAK-10 clause 2 and LEAK-7: zillow_prize,
   melbourne_housing_market, CC 2026-10-21; aeolus_1m's weather after departure).
 * Stated reason: the notes call them "impossible" (CLEAN-11). Column auditor [3]: 84% are occupational-disease
   claims whose date of disablement the Board set (FAQ 5), 64% PPD SCH LOSS. The right rule is LEAK-10/LEAK-7 (a value
   set after the prediction point); rewrite the bullet. Fix, no decision.
 * Residual: the blank joins 5,344 raw blanks (87.8% NON-COMP); its signal is 0.0009 log loss (column auditor). Under
   LEAK-6 ("a confirmed leak goes even when small") and kumc's practice, measure it against a paired SE; Board-set
   dates that fall before assembly cannot be located (a clause-2 residual note). If D1 (b) drops accident_date, this is
   moot; then the accident-to-assembly lag goes with it.

=======================================================================================================================
D6. Row count against the source (blind reviewer concern 1)
=======================================================================================================================
CONSISTENT; not a fidelity issue. The definition is the `_1m` version (definitions.md, "Temporal data: ... a random
`train` of all earlier rows for each train side, drawn in one random order so the train sides overlap; the frame keeps
only the rows a split uses"; Lennart 2026-10-21: at most 1M training rows). Arithmetic: frame 2015-2019 after the row
filters 1,426,699 (column auditor) = blind reviewer's 1,440,567 minus 13,678 ADR and 190 PFL; 2019 rows 298,680; earlier
rows 1,128,019. Under one random order the newer windows' pre-2019 rows are a subset of the oldest window's 1,000,000,
so the shipped frame is 1,000,000 + 298,680 = 1,298,680 (the clean room's count), keeping 88.65% of 2015-2018 claims.
The blind reviewer's ratio step at 2019-01 (0.130-0.139 -> 0.149-0.156) matches 0.154 x 0.8865 = 0.137. Precedents:
every temporal `_1m` version (nyc_taxi_trip_duration_1m, consumer_complaints_1m, aeolus_1m);
version_comment states it. Writing point only: the clean room's task.md did not carry the budget.

=======================================================================================================================
For the mediator
=======================================================================================================================
 * D1 is the deciding item: the implemented keep is a Must departure with no fact; the precedent line (Lennart,
   2026-10-21 to 2026-11-08) and this batch's kumc mediator point to drop. The builder's LEAK-11 framing should go.
 * D2: ship after the drop with fit approximate is the precedent-backed path; a retirement needs a fact and a marker
   that no precedent supplies.
 * D4 sex: per-dataset REVIEW.md issue, decided with rais issue 1. Age and ZIP need no decision beyond the citation.
 * D3, D5, D6: fixes or nothing; no curator call.
```

</details>

<details><summary>Advocate</summary>

```text
ADVOCATE OPENING BRIEF: ny_wcb_assembled_claims (folder ny_wcb_assembled_claims_1m), 2026-11-09

Read: dataset.py and README, principles.md, LEAK-10/-11/-24, SPLIT-10/-20/-21, TP-2, USE-8/-12, the seven
phase-A reports, builder_report.md, the claim auditor's matched_snapshot(2).log and missing_gain.log. Nothing run.

POSITION. Ship, but not with issue 1 as implemented. Keeping the kept fields at their 2026 values "with a note" breaks
LEAK-10 clause 2 (Must) on the claim auditor's matched test, and I concede it. Ship after the definition fix that the
rule and its closest precedent name: drop the fields whose traced part shows a gain, keep the rest under the clause-2
note, and restore the located post-2021 changes of the fields that stay. Everything else the panel tested holds, or
needs only fixes with no decision.

Proposed judgment record:
  Verdict: ship after changes.
  Validity: SEL-1 holds (no law found that bars sex or age in claim routing; sex decided with rais issue 1); USE-1 holds
  (approximate); USE-12 keeps the task; LEAK-10 triggered, fixed (post-assembly columns dropped; C-2/C-3/accident dates
  after assembly blanked; injury codes and the other traced-gain fields dropped; located post-2021 changes restored);
  LEAK-24 met by the 2020 cut, residual noted; SPLIT-1/-10/-14 hold; SPLIT-20 history start for the curator.
  Value: TP-2, a smaller real signal after the drop (at least 0.045-0.055 below the class shares on 2019).
  Quality: CLEAN-11/-12 fixes; note corrections.
  For the curator: issue 1 (which fields go, on paired SEs; the June 2021 copy as a second raw file), issue 6 (sex,
  with rais issue 1), issue 3 (history start).

----------------------------------------------------------------------------------------------------------------------
1. The task stays: no rule retires it. [USE-12 Must, P3; LEAK-10 retire clause; remedy ladder; TP-2 Should]
----------------------------------------------------------------------------------------------------------------------
Claim: whatever issue 1 decides, the dataset ships. Option (c'), retirement, does not follow from the leak.
Evidence:
- LEAK-10 retires only "when the features summarise a window that ends at the outcome and no common prediction point
  can be rebuilt". Assembly is a common prediction point, and it is rebuilt: 28 post-assembly columns are dropped and
  the C-2/C-3 dates after assembly are masked. Each dropped raw column alone scores macro AUC 0.75-0.88 (builder), so
  the large leaks are already out. The task gamer found no exploit above seed noise (0.0003).
- After the strictest drop, the rest still beats the class shares on all three 2019 windows: 1.011-1.021 against
  1.066 (column auditor). That run also dropped the carrier name, so it is a floor. On the 2021 claims the margin is
  0.024-0.077 (claim auditor).
- The precedent checker (D2) finds that retirement "departs without a fact": no marker fits. forest_fires was kept
  at R^2 0.013 (TP-2).
Why it outranks: USE-12 is a P3 Must: "a leak is no reason to reject a task whose use case is real". The Tensions row
"a real task against a leak" says fix the leak and keep the task (kickstarter). On the remedy ladder, exclusion is for
a Must that cannot be fixed, and this one can be fixed in the definition (point 2). Rebuilding from archived
snapshots (the other half of c') is worth one search of the 2023 Kaggle copies. It cannot feed a 1M-row task,
though: a snapshot holds near-assembly values only for the claims of the weeks before it (column auditor, remedy i).

----------------------------------------------------------------------------------------------------------------------
2. Issue 1: concede the keep and ship under the rule's fix. [LEAK-10 clause 2 Must, P4; LEAK-7 Should;
   distribution_transformers_at_cauca_department, onlinenewspopularity, medical_facility_operational_data, kumc]
----------------------------------------------------------------------------------------------------------------------
Concession: option (a) as implemented departs from a Must with no fact that sets the case apart.
- The matched test uses the same rows, with train and test on the same snapshot. The 2026 values beat the June 2021
  values by +0.0299 (SE 0.0042) at equal age, +0.0294 (SE 0.0026) iid and +0.0367 (SE 0.0020) over time.
- "The codes describe the injury" holds just as well for distribution_transformers' rating, which was dropped on
  2026-10-21 with no amendment. (a') would need that amendment again, and X4 (2026-11-08) says the size of the worth
  never decides.
The fix, field by field. The numbers are the claim auditor's one-field swaps in the equal-age design (all-2021 base
1.0636):
- Go: wcio_cause_of_injury, wcio_nature_of_injury, wcio_part_of_body (+0.0163, about four times the full-set SE).
- Go if a paired SE puts them above noise (kumc's practice; precedent checker): age +0.0094, accident date +0.0082,
  industry +0.0076, ZIP +0.0044. medical_fee_region follows the ZIP, since it is mapped from it.
- Stay under the clause-2 note, because the traced part shows no gain: carrier name -0.0017, district -0.0015,
  county/fee region -0.0005, C-3 -0.0030. Sex, claim type and county changed for under 0.5% of claims. C-2 is a 2022
  redefinition, not a late value.
- The located part. For the 2015-2019 claims, the changes after June 2021 can be located row by row: the 2021 copy
  holds all 1,426,699 claims. These changes follow the outcome. The carrier name changed for 90,095 claims, 28.8% of
  them NON-COMP against 62.5%; the fee region changed for 12,766 claims, 14.2% NON-COMP. Clause 2's first half says
  located late cells go. Restore them from the June 2021 copy (b', applied only to the fields that stay) rather than
  blanking them, because a blank would itself mark the outcome (LEAK-7, the smallest fix). This needs the curator's
  OK to read the June 2021 copy (the same Board table) as a second raw file.
To settle before the note can say "shows none": without the five fields, the group gap is +0.0031 (SE 0.0028) at
equal age, which is noise. It is +0.0065 (SE 0.0016) iid over January-June and +0.0085 (SE 0.0015) over time; in the
time design the 2021 arm also mixes completeness by age. If the paired test keeps a gain, two cheap drops are the
candidates: the fee region (mapped from the ZIP) and the carrier UNKNOWN blanks (97% NON-COMP in 2026, 59% near
assembly).
Why (b) over (a') and over (b') alone:
- (b') alone restores only the changes after June 2021, which came 1.5-6.5 years after assembly. The gain sits in the
  early fill (17% of the WCIO codes filled within weeks to months), so (b') alone does not resolve the Must.
- (b) is the mildest remedy that does. The precedent line is uniform (Lennart, 2026-10-21 to 2026-11-08), and kumc in
  this batch drops on gains of +0.003-0.004.
- Fit stays approximate, now also "a task changed a lot to avoid a leak" (USE-8; house_sales, sarcoma).
The cost is real. Skill falls from 0.186 to at least 0.045-0.055, and the task loses the injury description a
triage desk reads (domain practitioner). That is a fit question under USE-8, not a fact that takes the fields out of
LEAK-10, and TP-2 covers the smaller signal.

----------------------------------------------------------------------------------------------------------------------
3. Every other validity check holds, and issue 1 does not spread. ["independent failures are not conflicts";
   SPLIT-1/-3/-9/-13/-14; LEAK-16 to -21; MET-1/-2/-8; TP-8]
----------------------------------------------------------------------------------------------------------------------
Evidence:
- Split auditor, "right with notes": temporal on the assembly date, three contiguous four-month windows of 2019
  (99,803 / 101,201 / 97,676 rows), each with its own train side. The oldest pool is 79.1%, above the 50% floor.
  Linked claims are 0.040-0.045%, with label agreement near chance.
- No test row has an exact feature copy in training, on all three splits (claim auditor).
- Task gamer: nothing beats the best honest model (0.8371) beyond seed noise.
- Metric: the log_loss fallback is computable on every fold, the scorer equals sklearn, and every class is in every
  test fold (PTD 38-46, DEATH 39-44 rows). The domain practitioner found that log loss and the ordinal RPS rank 8
  models identically.
- Every dropped column is rightly dropped (column auditor).
- The blind reviewer's row gap (about 12% of 2015-2018) is exactly the _1m budget: 1,000,000 + 298,680 = 1,298,680
  (precedent checker D6).
Why it matters: every Must has to hold on its own, and these do. The blind reviewer's other concerns are handled
elsewhere: rare classes by log loss and TP-8 (PTD and DEATH carry 0.4-0.7% of the loss each, as in mic), and the
messy ZIPs by point 7.

----------------------------------------------------------------------------------------------------------------------
4. The release cut meets LEAK-24; the residual is a note. [LEAK-24 Must, P4; SPLIT-10 Should]
----------------------------------------------------------------------------------------------------------------------
Evidence:
- Labels that changed between 2021 and 2026 fall from 8.32% (2019) to 1.21% (2015).
- On the 2014 analogue, about 1% of the test labels and 12-13% of the eventual PPD NSL and PTD awards are still to
  come, against 3-7% for the training cohorts. PPD SCH LOSS in 2019Q4 is about 0.25 points low.
- Cutting at 2019 instead gains about 0.2 points of completeness and costs a year (claim auditor). The split
  auditor, the domain practitioner and the builder all say keep 2020.
- SPLIT-10: the gap ladder rises about 0.001 per month with no step at the window edge (the newest month adds
  0.0012-0.0018, about the seed spread), and no row is selected by its outcome. So no gap, as in
  lt_vehicle_loan_default_prediction (2026-11-05).
Fixes, no decision needed: change "settled"/"settling" (Decision 1 title, task_summary.changes) to the residual
numbers; add to splits_comment the 12-14% of training labels that changed after each window start, and the ladder.
Why it outranks "test labels are less mature in the rare classes": in a type-to-date label no follow-up is complete.
The cut sits where one more year buys 0.2 points, and the residual is the same small shift in all three windows
(split auditor).

----------------------------------------------------------------------------------------------------------------------
5. Sex and age stay: the fact the precedent checker asked for now exists. [SEL-1 Must, P1; Tensions row "a factor
   the actor may no longer use"; USE-6]
----------------------------------------------------------------------------------------------------------------------
Evidence: two agents read the law independently.
- NY Insurance Law s2607 bars sex as a reason to issue, cancel or renew a policy. The policy is the employer's; it
  says nothing on handling a claimant's claim.
- DFS Circular Letter 7 (2024) "is not intended to address phases ... other than underwriting and pricing"
  (para. 8).
- Directive 2004/113/EC covers premiums and benefits and excludes employment (Art. 3(4)). Routing changes neither,
  since the Board sets the benefits by statute.
- No NY rule was found that bars sex or age in claim handling.
- Age is a vocational factor in the Board's 2012 guidelines on loss of wage-earning capacity (ch. 9), so it is part
  of how PPD NSL is decided (USE-6).
- Dropping sex moves the log loss by -0.0005 / +0.0017 / +0.0013.
Why it outranks: the Tensions row covers pricing by its letter (2026-11-08). The rais extension, if confirmed, would
bar a factor "where the actor's own law bars it", and no law does here, so sex stays under both readings. Decide it
with rais issue 1, as its own REVIEW.md issue.
Open: whether the NY Human Rights Law reaches the Board's internal routing. Mildest remedy: name the carrier's
lost-time desk as the actor (domain practitioner), a wording change.
If point 2's SE drops age, it goes under LEAK-10, not SEL-1. ZIP (issue 5) is a P1 weigh: the state publishes it and
no precedent coarsens a published ZIP. It is moot if the ZIP goes under point 2.

----------------------------------------------------------------------------------------------------------------------
6. The history start is no blocker; 2016 is the cleaner reading. [SPLIT-20 Should; SPLIT-21 Must; SPLIT-14]
----------------------------------------------------------------------------------------------------------------------
Evidence:
- What the Board assembled kept shifting through 2015. From 2015Q1 to Q4, NON-COMP went from 45.0% to 61.3% and MED
  ONLY from 22.2% to 10.4%. From 2016 the shares are 63.7-65.6% and 7.5-8.7%.
- The blind reviewer, the split auditor and the task gamer each found this independently.
- 2015 is 20.6-24.3% of each train side.
- The fits disagree: 2016 is lower in 5 of 6 (split auditor), and dropping 2015 is worse by 0.0007 (task gamer).
  SPLIT-21 bars deciding from them anyway.
I do not defend 2015 hard. SPLIT-20 asks to check the history for "a change of ... the data collection", and the ramp
is one. HISTORY_START = 2016-01-01 keeps the floor (oldest pool 74.1%) and four full years of seasons, and costs
273,999 rows. If the curator keeps 2015, one line in splits_comment names the transitional quarters. Either way the
dataset ships.

----------------------------------------------------------------------------------------------------------------------
7. The rest are fixes with no decision. [USE-8 Must; LEAK-10/LEAK-7; CLEAN-11/-12 Should; procedure]
----------------------------------------------------------------------------------------------------------------------
- fit_reason: name the inputs the actor has at assembly that the table does not publish: the reason for assembly,
  the reported wage and lost time, the carrier's denial, the occupation, the narrative, the C-4 and the attorney at
  assembly (domain practitioner, gap 1). After point 2, name the dropped injury fields as the task's change. Keep
  "approximate".
- The 3,039 accident dates after assembly: 84% are occupational-disease dates of disablement set by the Board (64%
  PPD SCH LOSS). Blanking them stays. The stated reason should be LEAK-10/LEAK-7 (set after the prediction point),
  not CLEAN-11 ("impossible") (column auditor [3]; precedent checker D5). Moot if accident_date goes.
- CLEAN-12: decode medical_fee_region I-IV into the codebook's words (if it stays).
- CLEAN-11: set ZIP '-7296' and the 17 ages of 100-117 to missing.
- Notes:
  - in the kept years, 20/24 industry and 54/57 body-part descriptions and codes;
  - the OD count is 14,466, not the code comment's 14,488;
  - C-2's 2022 redefinition is applied backwards;
  - 5D SPECIAL FUND - UNKNOWN (143 claims moved there after June 2021) and VIRTUAL ONLY (49);
  - the actor written precisely.
Why: P7 fixes that are cheap and safe are made (How to decide, 3). USE-8 sets a Must on what the notes say, not on
whether the dataset ships.

----------------------------------------------------------------------------------------------------------------------
CONCEDED OUTRIGHT
----------------------------------------------------------------------------------------------------------------------
- Issue 1's option (a) as implemented.
- The 0.03 is a lower bound.
- After the drop the task is much thinner: about a quarter to two fifths of the skill the shipped version credits,
  without the injury description.
- The residual of the remaining fields is not yet shown to be noise in every design (point 2).
- The insurer-files-the-FROI fact (precedent checker D1, option a) is untested, and I do not rest on it.

======================================================================================================================
Rebuttal
======================================================================================================================
(Advocate, 2026-11-09, to the critic's opening brief. No new facts came up, so there are no new points.)

The critic and I agree on the verdict (ship after changes) and on most of the remedies. Three points are left in
dispute: the default before the paired-SE test, whether the mechanism alone bars a field from returning, and which
residual number is reported.

C1. The injury codes, industry, age, accident date and ZIP carry a traced gain [LEAK-10 clause 2, Must].
- CONCEDE the default. My opening said the four fields go "if a paired SE puts them above noise". That puts the
  burden the wrong way round. Clause 2 lets a value go when it "may carry a gain", and stay with a note "only when
  the part that can be traced shows none". So industry, age, accident date and ZIP leave now, with the WCIO codes. A
  field returns only if a paired SE shows none.
- DISPUTE that a field must stay out even on a null paired SE because of its mechanism. The clause states the keep
  condition as a gain test, not a mechanism test. On a null trace, onlinenewspopularity (CC 2026-10-26) and
  medical_facility_operational_data (CC 2026-11-05) kept their fields. tunisian's CTR_CESSAT went on a mechanism
  together with a gain (+0.015), not on the mechanism alone.
- The likely outcome is the same either way. In the equal-age design the swaps sit at about 2.2 / 2.0 / 1.8 times
  the full-set SE (0.0042) for age, accident date and industry, and 1.0 times for ZIP. Those three will very likely
  stay out. Only ZIP could come back, and if it does, its changes after June 2021 must be restored (32,322 claims,
  9.8% PPD NSL against 1.4%).
- PARTLY DISPUTE the residual. The critic quotes +0.0031 (SE 0.0028, equal age) and +0.0085 (SE 0.0015, over time).
  The time figure is inflated because the 2021 arm mixes completeness by age. The cleaner number that stays above
  noise is the one the critic leaves out: +0.0065 (SE 0.0016), iid over January-June. The one-field swaps of the
  fields that stay are all 0 or below (carrier -0.0017, district -0.0015, county/region -0.0005, C-3 -0.0030). So the
  gain sits in the group, and the candidates are the carrier UNKNOWN blanks and the fee region. We agree the residual
  is tested field by field before shipping.
- One correction to my opening: medical_fee_region stays under the note, on its swap (-0.0005). I had sent it with
  the ZIP. Its located changes after June 2021 (12,766 claims) are restored.
- (b') fixes too little: CONCEDE as a substitute, and the critic and I agree on it as a complement. Restoring carrier
  and the other kept fields from the June 2021 copy changes only cells that moved 1.5-6.5 years after assembly (WCIO
  0.3-0.9%). The early fill that carries the gain is already in those values, so (b') cannot replace the drop.
  Applied only to the fields that stay, it is clause 2's first half: late cells that can be located go. A restore beats
  a blank there, because a blank would mark the outcome: 90,095 carrier changes are 28.8% NON-COMP against 62.5%.
  It needs the curator's OK to read the June 2021 copy (the same Board table, all 1,426,699 claims) as a second raw
  file. If the curator declines, the rule's default is the blank, and the note must say what the blank then marks.
- The critic says the ranking of methods moves. CONCEDE in direction, but nobody measured it. It does not change the
  remedy.
- (a') and (c'): agreed with the critic. (a') needs the amendment the curator declined on 2026-10-21. (c') is not
  needed (TP-2, USE-12).

C2. fit_reason names the wrong gap [USE-8, Must]. CONCEDE. This is my point 7: name as gaps the inputs the actor holds
at assembly, the label to date and the task changed to avoid a leak. Name the actor as the carrier's lost-time desk or
the Board's examiner.

C3. Label maturity [LEAK-24 Must, met; SPLIT-10 Should]. AGREE: keep the 2020 cut and no gap, and put the residual
(12% PPD NSL, 13% PTD), a reworded Decision 1 title and the label-delay numbers in the notes. This is my point 4.

C4. Accident dates under the wrong rule; 5D; VIRTUAL ONLY [LEAK-10/LEAK-7]. AGREE. After C1 the accident-date half is
moot. The 5D and VIRTUAL ONLY lines stay as notes.

C5. Sex and age [SEL-1 Must holds]. AGREE: no feature change, the note's reason replaced by the facts that were read,
sex decided with rais issue 1, and the carrier named as the actor. With age dropped under C1, the age half is moot.

C6. History from 2016 [SPLIT-20 Should; SPLIT-21 Must]. CONCEDE. Keeping 2015 would be a departure from a Should, and
I have no fact for it beyond more rows. SPLIT-21 bars the task gamer's 0.0007. The break decides:
HISTORY_START = 2016-01-01 (oldest pool 74.1%).

C7. Cleaning and notes [CLEAN-11/-12, Should]. AGREE. Decode medical_fee_region, which now stays. Set ZIP '-7296' and
the ages of 100-117 to missing (moot if those columns go). Correct the counts and add the C-2 line.

Net: ship after changes. The open question for the curator is what returns on a null paired SE, and the residual of
the fields that stay.
```

</details>

<details><summary>Critic</summary>

```text
CRITIC, OPENING BRIEF: ny_wcb_assembled_claims (folder ny_wcb_assembled_claims_1m), 2026-11-09

Position: do not ship as defined. Ship after changes. The fields whose 2026 values carry a traced gain leave the
features (point 1); fit_reason and several notes are rewritten (points 2-5); the history starts in 2016 (point 6);
cheap cleaning (point 7). This is not a case for retirement: without those fields the task keeps a small real signal
on all three windows (TP-2, USE-12).

Verdict: ship after changes.
Validity: SEL-1 holds (sex, age kept; the note should give the fact, point 5); USE-8 triggered, fix fit_reason
(point 2); LEAK-10 clause 2 broken by the implemented keep, fix by dropping the fields with a traced gain (point 1);
LEAK-24 met with a residual, note (point 3); accident dates after assembly blanked under the wrong rule, note (point
4); SPLIT-20 departure without a reason, start 2016 (point 6).
Value: TP-2 holds after the drop (about 0.045-0.055 log loss below the class shares on the 2019 windows).
Quality: CLEAN-11 and CLEAN-12, cheap fixes (point 7).

Sources: the seven phase-A reports in this folder, builder_report.md, probes/ (field_stability.txt,
maturity_by_class.txt, snapshot_feature_test_wcio.log, snapshot_feature_sets_harmonised.log),
the claim auditor's matched_snapshot2.log (re-read for the numbers below), dataset.py, README.md, principles.md,
leak_checks.md, use_case.md, splits.md, the records of distribution_transformers_at_cauca_department and
onlinenewspopularity.

======================================================================================================================
1. Injury codes, industry, age, accident date and ZIP are 2026 values and carry a measured gain
   [P4, LEAK-10 clause 2, Must]
======================================================================================================================
Problem. The table keeps no history. Every kept field is its value in September 2026, 6.7 to 11.7 years after
assembly. Both the late values and the late blanks follow the claim's course.

Evidence.
- Matched test (claim auditor, matched_snapshot2.log). Same 2021 claims, same 2026 labels; train and test both on the
  June 2021 values, or both on the 2026 values. The 2026 values win by +0.0367 (SE 0.0020, train Jan-Mar, test
  Apr-Jun), +0.0299 (SE 0.0042, iid at equal age) and +0.0294 (SE 0.0026, iid Jan-Jun). That is 21-31% of the
  measured skill. It is a lower bound, since the June 2021 values are already 0-5 months old. With train and test
  values from the same snapshot, the builder's caveat ("part of the gap is a model trained on completed fields") no
  longer explains the gap.
- Per field (swapping one field to 2026 on top of all-2021 values): WCIO +0.016, age +0.009, accident date +0.008,
  industry +0.008, ZIP +0.004. Carrier name, district, county/region and C-3 show none.
- Mechanism. For claims seen 0-11 weeks after assembly, the fields filled later belong to severe claims (filled later:
  industry 53%, WCIO nature 44%, age 57%, accident date 64% PPD SCH LOSS, against 9.5%). The fields still blank in
  2026 belong to claims that went nowhere (WCIO 94.4%, industry 95.3%, carrier 97.0%, age 87.1%, accident date 87.8%
  NON-COMP, against 62.5%). Near assembly a blank WCIO meant the opposite: 31% PPD SCH LOSS against 7.6%. So the
  meaning of a blank flips (column auditor [1]; claim auditor rows 22, 30). On the shipped 2015-2019 claims the cells
  changed after June 2021 follow the outcome too (ZIP changed: 9.8% PPD NSL against 1.4%; WCIO nature changed: 11.1%
  NON-COMP). Even on rows already coded in June 2021, the 2026 values score 0.936 against 0.973
  (snapshot_feature_test_wcio.log). Changed values carry gain, not only the late fills.
- The task gamer read the blanks as "facts known at assembly once the dates are masked". The snapshot comparison
  refutes that reading. The gamer's "no exploit" result does not cover this leak, which sits in the values every
  participant gets.

Effect on the task. The benchmark credits a model for reading fields the Board completed as the claim grew. These
fields carry 70-75% of the skill on the 2019 windows (column auditor: 0.880 with all features, 1.011-1.021 without
them, class shares 1.066). A triage desk at assembly reaches far less. Methods that exploit high-cardinality codes and
missingness gain the most, so the ranking moves as well as the absolute scores.

Rule. LEAK-10 (Must), clause 2 (amended 2026-10-26, Lennart): values from a later pull whose late cells cannot be
located row by row "go when they may carry a gain ... and stay with a note only when the part that can be traced shows
none". The traced part shows a gain. LEAK-11 does not apply: it keeps late values that weaken the signal, and these
strengthen it. The builder gives two reasons to keep, and neither sets this case apart:
- "The codes describe the injury, which exists at assembly." This holds for every looked-up attribute: the
  transformer's rating existed at the burn.
- "Dropping them leaves the triage without its core." This is a statement of worth. The size of the worth never
  decides (LEAK-10, X4, 2026-11-08), and "a very real task ... does not carry a leak" (principles.md, How to decide 3).
Precedents:
- distribution_transformers_at_cauca_department (CC 2026-10-21, Lennart): "LEAK-10 stays as written". The fields were
  dropped at a cost of ROC AUC 0.701 -> 0.639. Same mechanism, a larger gain here.
- onlinenewspopularity (CC 2026-10-26) and medical_facility_operational_data (CC 2026-11-05) kept their fields only
  because the trace showed nothing.
- tunisian_fraud_detection_challenge kept registry fields only where no mechanism ties a change to the outcome. Here
  one does.
A Must has no exceptions (principles.md, Exceptions and amendments).

Remedy, the mildest that resolves it: fix the definition.
- Drop wcio_cause_of_injury, wcio_nature_of_injury, wcio_part_of_body, industry, age_at_injury, accident_date and
  zip_code. On the matched claims the rest scores 0.024-0.077 below the class shares. The residual gap is +0.0031
  (SE 0.0028) at equal age, which is at noise, and +0.0085 (SE 0.0015) in the time design. Before shipping, measure
  that residual field by field.
- Keep carrier name and type, district, county, fee region, claim type, sex and the C-2/C-3 dates under the clause-2
  note: their swaps show no gain. Name the carrier blank (97% NON-COMP in 2026, 59% near assembly; worth at noise).
- A paired SE on the matched claims (LEAK-6) may return age or ZIP if its gain is within noise. Without that test I
  would not return them, because both show the outcome mechanism above.
- Rewrite the "Potential leak" bullet with the matched numbers. Update task_summary.known, and set the fit to
  approximate as "a task changed a lot to avoid a leak" (USE-8).
The alternatives fall short:
- (b') Taking the kept fields from the June 2021 copy removes only what changed 1.5-6.5 years after assembly (WCIO
  0.3-0.9% of cells); the fill near assembly is already in those values. Use it for the fields that stay, not instead
  of the drop.
- (a') Keeping with a note needs an amendment of LEAK-10, which the curator declined for this mechanism on 2026-10-21.
  If the curator chooses it anyway, the note must state 0.030-0.037 as a measured leak (not "part mismatch"), and
  fit_reason must name it as kept (USE-8).
- (c') Retirement is not needed (TP-2, USE-12; no marker fits, precedent checker D2). A rebuild from archived
  quarterly tables would be the true repair if an archive turns up. None was found, and the 2023 Kaggle copies were
  not checked.

======================================================================================================================
2. fit_reason names the wrong gap and leaves out the largest one   [P3, USE-8, Must]
======================================================================================================================
Problem. fit_reason lists the 2026 values as a gap. USE-8 as amended (2026-10-21, Lennart) says a kept leak is named
"as kept, not as a gap". The gap the actor names first is missing.

Evidence (domain practitioner, sections 1 and 2). At assembly the actor holds inputs that the table does not publish:
- the reason the Board assembled the claim (more than one week of lost time, a serious injury, a dispute, a C-3);
- the employer-reported wage and the lost time so far (eClaims DN0062);
- the carrier's own denial (FROI-04/SROI-04);
- the occupation (DN0060), the narrative, the C-4, and the attorney at assembly.
The Board's own decision at assembly is the resolution path (highest_process, set later), not this target.

Effect. A reader takes the score for what a triage desk reaches at assembly. In fact it is a model without the inputs
the desk relies on most.

Remedy (writing).
- Rewrite fit_reason: approximate because the inputs the actor holds at assembly are not published (list them),
  because the label is the type to date, and, after point 1, because the task was changed a lot to avoid a leak.
- Name the actor as the carrier's lost-time desk (or the Board's examiner), not the Board's routing.
- Add the same sentence to the first notes bullet.

======================================================================================================================
3. Label maturity: the test labels are younger than the training labels   [P4, LEAK-24 Must, met with a residual;
   SPLIT-10 Should]
======================================================================================================================
Evidence.
- maturity_by_class.txt: at the age the 2019 test claims have now, the 2014 cohort held 88% of its 2026 PPD NSL and
  87% of its PTD. The training cohorts' analogues hold 93-97%. So the test labels are the less mature ones in the two
  rarest severe classes.
- In the data: PPD SCH LOSS is 8.48% in 2019Q4, against 8.72-8.80% in 2019Q2-Q3 (split auditor).
- Training side: an estimated 12-14% of each training side's labels changed after the window start. The gap ladder
  rises smoothly, about 0.001 log loss per month, with no step at the window edge (split auditor).
- The Decision 1 title ("benefit types that have settled") and task_summary.changes ("still settling") overstate the
  maturity.

Effect. A small shift toward the lower classes in every test window, about the same for every method.

Remedy. Keep the cut at 2020-01-01 and keep no gap. Notes only:
- the residual (12% of PPD NSL and 13% of PTD still to come);
- a reworded Decision 1 title;
- the label-delay numbers in splits_comment.

======================================================================================================================
4. Accident dates after assembly: the right fix under the wrong rule; small post-assembly codes not named
   [P4, LEAK-10 Must, weak here; LEAK-7 Should]
======================================================================================================================
Evidence (column auditor [3]-[5]; precedent checker D5).
- The notes call the 3,039 accident dates after assembly "impossible" (CLEAN-11). They are not: 84% belong to
  occupational-disease claims (2,559), 64% are PPD SCH LOSS and 3.7% NON-COMP. They are the dates of disablement the
  Board sets (FAQ 5).
- Their blank merges with 5,344 raw blanks (87.8% NON-COMP); its worth is 0.0009.
- The accident dates of occupational-disease claims that fall before assembly are also Board determinations (about 1%
  of claims).
- 143 claims moved from UNKNOWN to "5D SPECIAL FUND - UNKNOWN" after June 2021 (2,229 claims under 5D; 45% NON-COMP,
  1.3% DEATH).
- VIRTUAL ONLY (49 claims) is a district created later.

Remedy.
- Rewrite the accident-date bullet under LEAK-10/LEAK-7 (moot if accident_date leaves under point 1).
- Add one line on 5D to the Carrier bullet.
- Add one line on VIRTUAL ONLY, or set it to missing.

======================================================================================================================
5. Sex and age: kept on a scope reading, not on the fact   [P1, SEL-1 Must holds; principles.md Tensions row, amended
   2026-11-08]
======================================================================================================================
Problem. The note keeps sex because the task is "triage, not pricing". The stance turns on the actor's law, and that
law is now read.

Evidence (claim auditor C; domain practitioner 6).
- NY Insurance Law s2607 covers issuing, cancelling and renewing the policyholder's policy, and the policyholder here
  is the employer.
- DFS Circular Letter 2024-07 (para. 8) leaves out every phase but underwriting and pricing.
- Directive 2004/113/EC, Art. 3(4) and recital 15, leaves out employment.
- No New York rule found bars sex or age in claim handling.
- Open: whether the Human Rights Law reaches a state agency's internal routing.
- Age enters the Board's own loss-of-wage-earning-capacity assessment (2012 Guidelines, ch. 9).
- Measured cost of dropping: sex about 0.001, age 0.005-0.011.

Remedy. No feature change.
- Replace the note's reason with these facts.
- Decide sex together with rais issue 1.
- Name the carrier as the actor (point 2), which avoids the open Human Rights Law question.
- If point 1 drops age, the age half is moot.

======================================================================================================================
6. The training history starts inside the EDI ramp   [P4, SPLIT-20, Should]
======================================================================================================================
Evidence (split auditor finding 2).

    2026 labels by assembly quarter   NON-COMP     MED ONLY
    2015Q1                             45.0%        22.2%
    2015Q2                             51.3%        19.3%
    2015Q3                             56.7%        15.5%
    2015Q4                             61.3%        10.4%
    2016-2019                          63.7-65.6%   7.5-8.7%

- 2015 makes up 20.6-24.3% of each training side.
- The definition's reason, "the first full year of electronic claim filing", describes the mandate. The data shows
  the mix of assembled claims still moving for three quarters; the builder's own issue 3 calls 2015 transitional.
- Scores point both ways: a 2016 start is lower in 5 of 6 fits (split auditor), while dropping 2015 scores 0.8404
  against 0.8397 (task gamer). Under SPLIT-21 they do not decide. The break does.

Effect. A fifth of every training side comes from a different assembly population, one a 2019 refit would hardly
train on.

Remedy.
- HISTORY_START = 2016-01-01. The oldest pool becomes 74.1%, above the SPLIT-14 floor, and the oldest train side falls
  below 1M.
- Or HISTORY_START = 2015-10-01.
- The mildest acceptable fix: keep 2015 with a splits_comment line naming the ramp, recorded as a departure with its
  reason.

======================================================================================================================
7. Cleaning and accuracy of the notes   [P7, CLEAN-11 and CLEAN-12, Should; no reason to exclude]
======================================================================================================================
- medical_fee_region ships as I-IV, while the codebook names each region in words. Decode it (CLEAN-12).
- Set ZIP '-7296' (1 row) and ages 100-117 (17 rows, birth years 1901-1916) to missing (CLEAN-11). This is moot for
  any column point 1 drops.
- Note fixes:
  - in the kept years the counts are industry 20/24 and body part 54/57, not 21/25 and 55/58;
  - the occupational-disease count is 14,488 in the code comment and 14,466 in the notes;
  - the 2022 C-2 definition is applied backwards.

======================================================================================================================
Not argued (the evidence does not carry them)
======================================================================================================================
- Row count against the source: the documented `_1m` budget (precedent checker D6).
- Merging PTD and DEATH: TP-8 holds (each carries 0.4-0.7% of the loss, and every class is in every fold).
- The fallback log_loss: MET-8 and MET-11; the scorer matches sklearn.
- The regime and the windows: right per the split auditor.
- Copies, row order and the other exploits: nothing above noise (task gamer).
- The ADR, CANCELLED and PFL row drops: LEAK-25, USE-5.
- The release cut itself: the cut stays; only notes are asked for (point 3).

======================================================================================================================
Rebuttal
======================================================================================================================
Critic, 2026-11-09, on the advocate's opening brief (advocate.report.txt). No new points. The numbers below come from
the claim auditor's matched-snapshot logs (scripts in the run folder), re-read for this round.

The advocate and I now agree on the verdict (ship after changes), on the drop of the three WCIO codes, and on most of
the fixes. What stays in dispute is how the fields that stay, and the four borderline fields, are cleared.

----------------------------------------------------------------------------------------------------------------------
Advocate 1. The task stays; no rule retires it.   CONCEDE.
----------------------------------------------------------------------------------------------------------------------
This is my position too: USE-12, TP-2 and the remedy ladder. One qualification. "The large leaks are already out" and
"the task gamer found no exploit" say nothing about issue 1. The gamer's kit holds only the 2026 values, so it could
not see this leak. That changes no outcome here.

----------------------------------------------------------------------------------------------------------------------
Advocate 2. Drop the WCIO codes; paired SEs for the rest; carrier, district, county and C-3 stay under the note;
restore their post-2021 changes from the June 2021 copy.
----------------------------------------------------------------------------------------------------------------------
(a) Drop the WCIO codes. CONCEDE (agreed).

(b) Restore the post-2021 changes of the fields that stay from the June 2021 copy. CONCEDE, as a repair. It is better
than blanking, because a blank would encode the outcome (LEAK-7; PROV-13: repair before fixing). Clause 2's first
half applies to located cells whatever their score: "a lookup is not kept merely because removing it changes no
score" (zillow_prize, melbourne_housing_market, 2026-10-21). Three conditions:
- Take each restored field whole from the 2021 copy, so its categories are consistent. All 1,426,699 claims are in
  that copy. The district renames (HAUPPAUGE, STATEWIDE) then follow one naming throughout, and the 49 VIRTUAL ONLY
  claims and the 143 UNKNOWN -> 5D claims get their 2021 values.
- Restore medical_fee_region too: it is mapped from the ZIP, and it changed for 12,766 claims after June 2021 (14.2%
  NON-COMP).
- Pin the second raw file: its Kaggle version, the sha256 and a download line, so a rebuild stays reproducible.
If the curator declines the second file, the located late cells cannot be repaired, and blanking them would encode
the outcome. The fields with located outcome-linked changes then go, or the curator records the departure: carrier
name (90,095 claims, 28.8% NON-COMP) and fee region. So the curator's OK on the second file is a real decision,
not a formality.

(c) Carrier, district, county and C-3 stay "because their one-field swaps are at or below 0". DISPUTE; the bar is not
met yet.
- The one-field swaps were run in one design only (iid at equal age: 13,230 test rows; full-set SE 0.0042). Each
  swap was measured with every other field at its 2021 value, the WCIO codes included. They do not measure the set
  that will ship, which has no WCIO codes.
- The measurement of that set already exists. Without the five fields, the remaining fields at 2026 values beat
  their June 2021 values by:
      +0.0085 (SE 0.0015)  time design
      +0.0065 (SE 0.0016)  iid January-June
      +0.0031 (SE 0.0028)  iid at equal age
  Two of three designs show a gain at 4-5 SE.
- The advocate's explanation, that the 2021 arm mixes completeness by age, does not fit the iid January-June design,
  where train and test mix ages alike. If anything, values 0-5 months old are more complete than values at assembly,
  so the gap is a lower bound.
- Under LEAK-10 clause 2 (Must), a field stays with a note "only when the part that can be traced shows none". For
  this group the trace does not show none.
Remedy, before the note can claim "shows none":
- Rerun the paired test on the shipped set: after the drop, with the restored 2021 values for the fields that stay,
  in the three designs.
- Drop whatever removes the residual. The advocate's own candidates come first: the carrier blank (97% NON-COMP in
  2026, 59% near assembly) and the fee region.
- C-3 and the C-2 dates kept only on or before assembly: concede. C-3 changed for 14 of 20,756 claims, and a date on
  or before assembly is known at assembly.
- Sex, claim type and county: concede (under 0.5% changed, no swap gain).

(d) The paired-SE test for industry, age, accident date and ZIP. CONCEDE the test, as LEAK-6 asks ("measure before
acting") and as kumc and medical_facility_operational_data practised. DISPUTE how it decides:
- The burden. The clause sends a value out "when it may carry a gain". A field stays only when the test shows none:
  within noise in every design, not merely below some threshold in the weakest one. An inconclusive result means it
  goes (distribution_transformers_at_cauca_department went on "a gain that may sit on the changed rows",
  2026-10-21).
- The design. The current swaps (industry +0.0076, age +0.0094, accident date +0.0082, ZIP +0.0044) come from the
  smallest design, with the WCIO codes in the model. Without the WCIO codes, industry and the accident date may carry
  more of the injury signal and of its late fill. The test has to run on the post-drop set, in all three designs,
  paired by row, over several seeds.
- Missingness. Industry, age and accident date also show a blank that flips (filled later: 53%, 57% and 64% PPD SCH
  LOSS; still blank in 2026: 95.3%, 87.1% and 87.8% NON-COMP). That falls under LEAK-10's separate item "missingness
  that encodes the outcome". Its worth on the 2019 windows is small (accident 0.0009, age 0.0003, industry at noise;
  column auditor). The test should report it beside the value swap, and a keep should name it in the note.
- Blocks. Test ZIP together with medical_fee_region, which is mapped from it (the block practice in
  loan_default_prediction_imperial_college, 2026-11-03). Test age together with accident_date, since the age is
  computed from the accident date.

----------------------------------------------------------------------------------------------------------------------
Advocate 3. Every other validity check holds.   CONCEDE.
----------------------------------------------------------------------------------------------------------------------
The split, copies, metric, dropped columns and the _1m row count: I argued none of them. Every Must has to hold on
its own; those hold, and LEAK-10 is fixed by point 2.

----------------------------------------------------------------------------------------------------------------------
Advocate 4. The release cut meets LEAK-24; the residual is a note.   CONCEDE.
----------------------------------------------------------------------------------------------------------------------
This is my point 3: keep the 2020 cut and no gap, reword "settled", and put the residual and the ladder in the notes.

----------------------------------------------------------------------------------------------------------------------
Advocate 5. Sex and age stay on the fact now read.   CONCEDE.
----------------------------------------------------------------------------------------------------------------------
This is my point 5: decide sex with rais issue 1, and name the carrier's desk as the actor. If age survives the paired
test, the note gives the LWEC fact.

----------------------------------------------------------------------------------------------------------------------
Advocate 6. The history start is no blocker; 2016 is the cleaner reading.   CONCEDE the substance; DISPUTE one line.
----------------------------------------------------------------------------------------------------------------------
We agree on 2016-01-01. If the curator keeps 2015, "one line naming the transitional quarters" describes the ramp but
does not justify keeping it. A departure from SPLIT-20 (Should) needs "the fact that sets the case apart and the
higher principle it serves" (principles.md, Strengths), recorded as an exception. Neither the builder nor the advocate
has offered such a fact.

----------------------------------------------------------------------------------------------------------------------
Advocate 7. The rest are fixes with no decision.   CONCEDE the list; DISPUTE one sentence.
----------------------------------------------------------------------------------------------------------------------
"USE-8 sets a Must on what the notes say, not on whether the dataset ships" is wrong as stated. A Must holds before
the dataset ships (principles.md, How to decide 4). The fit_reason fix is cheap, so it is a change before shipping,
not one that may wait.

----------------------------------------------------------------------------------------------------------------------
Conceded outright (the advocate's list)
----------------------------------------------------------------------------------------------------------------------
Agreed on all five items, including that the residual of the fields that stay is not yet shown to be noise. On that
item we differ only on order: it has to be measured before the "Potential leak" note is written, not after.

Remaining dispute for the mediator: whether the fields that stay, and industry, age, accident date and ZIP, are
cleared by the one-field swaps (advocate), or by a paired test on the post-drop set in all three designs, where an
inconclusive result means the field goes (critic; LEAK-10 clause 2, Must; LEAK-6).
```

</details>
