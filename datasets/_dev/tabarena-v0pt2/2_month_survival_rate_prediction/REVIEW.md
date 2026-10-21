# 2_month_survival_rate_prediction

**Outcome:** added. SUPPORT's 8,967 patients of both phases alive after study day 3, with the phase II physiology
moved back into its rows through ICPSR 2957 (only support2's values ship); binary target death within 2 months, IID
over patients. The review panel ran (full tier, 2026-10-20) and recommends shipping after changes. The changes that
needed no decision are made: the prediction point is named study day 3, albumin above 6 g/dL is set missing, the
split note and four inexact sentences now state the measured numbers, and the record's "no known risk" note names
the adlp finding.

```text
Verdict: ship after changes.
Validity: USE-1, USE-5, USE-7 hold (direct fit); USE-3 triggered, fixed (study day 3, not hospital day 3);
  USE-6/LEAK-37 triggered for prg2m/prg6m and DNR by day 3 (issue 5); LEAK-10/LEAK-6 triggered for adlp's gaps,
  0.0035 ROC AUC (issue 7, against CC 2026-10-12); LEAK-10 weak for edu/income (issue 10);
  SPLIT-1 holds, IID kept (temporal 0.824, leave-hospital-pair-out 0.815, against IID 0.818; no decision needed),
  SPLIT-5/SPLIT-7 note fixed; PROV-13/PROV-15 hold (repaired from ICPSR); PROV-9 triggered, year without source
  (issue 8).
Value: TP holds (997 or more positives per test fold, ROC AUC about 0.81, linear 0.78, no flags).
Quality: CLEAN-11 alb > 6 set missing (4 rows); wblc 0 kept with a note; pafi above the physical ceiling (issue 9).
Weighed: source +, use case +, repair +, Outdated - (the curator's marker for 1989-1994 care; no rule makes it decide,
  and six clinical records of the same era carry it and ship).
For the curator: issue 5 (framing), issue 7 (adlp), issue 10 (edu and income), issue 8 (year), issue 9 (pafi cut).
```

**Main points:** Frame the use case as the source's objective estimate or keep the physicians' estimates and DNR
(issue 5); drop adlp, which reopens the curator's comment (CC) of 2026-10-12 (issue 7); the year (issue 8); a pafi cut (issue 9); edu and income (issue 10).

**Record judgment:** valid with concerns: a real day-3 prognosis task, repaired from the study's own data; adlp's
gaps carry a small leak (issue 7), the physicians' estimates are dropped for a reason the ranking does not accept
(issue 5), and the year has no source (issue 8). The curator's `Outdated` marker (1989-1994 care) stands.

**Issues for Lennart:**

5. **The physicians' day-3 estimates and DNR status: frame the use case as the source's objective estimate, or keep
   them?** prg2m and prg6m are the physicians' 2- and 6-month survival estimates, taken in an interview on study day
   3 (Knaus 1995, abstract: "Physicians were interviewed on day 3"), so they are known at the prediction point; so is
   a DNR order written by day 3. All are dropped, with the advice of the Vanderbilt description page of support2
   (supportdesc) as the reason ("You also will probably not
   want to use prg2m, prg6m, dnr, dnrday"). A source's advice is no reason under the ranking, and `use_case` says "the
   care team estimates a patient's chance", so the task leaves out the actor's own estimate, which USE-6 calls a
   changed task. `changes` also says the estimates are "made from or after these values"; they are made on day 3,
   beside the values.
   - Effect: prg2m alone scores ROC AUC 0.801; adding it lifts the model from 0.817 to 0.839 (3 x 5-fold). A "DNR
     order by day 3" flag (1,437 patients, 61.6% die within 2 months) lifts 0.814 to 0.822. dnr and dnrday as
     published stay out either way: dnrday equals the days to discharge for every patient without an order, and
     1,659 of the 2,956 orders written after entry are dated after day 3.
   - Implemented: all dropped; `use_case` unchanged apart from the prediction point.
   - Alternative (a), the advocate's, accepted by the critic: write the source's design into `use_case`, an objective
     estimate set beside the physician's (Knaus 1995, "Objective estimates of survival"; the physicians were measured
     as the comparator, model 0.812 against physician 0.801). The estimates and the DNR flag are then out by the use
     case; cite Knaus 1995 and fix `changes`. It departs from breast_cancer_prediction (BI-RADS kept, 2026-10-15), with
     the fact that sets it apart: the source measured the physician only as the comparator of its objective
     estimate, so the actor is not the one holding the estimate. Recorded as an exception, or as an amendment to
     USE-6 if it should hold in general.
   - Alternative (b): keep prg2m and prg6m and build the DNR-by-day-3 flag (LEAK-7), as breast_cancer_prediction,
     brazilian_ecommerce and bias_correction kept the actor's estimate; the task becomes "refine the physician's
     estimate".
   - Rule: USE-6 and LEAK-37 (Must), USE-9 (Should); the use case (P3) names the actor, and the actor's knowledge sets the inputs. A weighing call: both
     framings are valid, the current text is not. The mediator leaves the choice to the curator; the AI recommends (a),
     the advocate's, which the critic accepted.
   - Decision: (a) or (b); DNR follows prg2m.

7. **adlp: drop it (reopens CC 2026-10-12)?** adlp is the patient's own answer on daily
   activities (function two weeks before admission) from the first patient interview, held on study days 2-7. The CC
   kept it because it is "missing mostly when the patient cannot answer". ICPSR's interview status shows a second
   reason: 475 patients have status 10 "Pt Death"; all of them die within 2 months (98.3% by day 7) and none has
   adlp. 95.4% of the 767 deaths on days 4-7 lack adlp, against 58.2% of the other patients. The CC's table pooled
   deaths with discharges ("stay ended by day 7"), which hid this. It is the mechanism for which the surrogate's ADL answer
   (adls) was dropped here, and for which the dataset mic (myocardial infarction complications) dropped its ICU
   day 1-3 fields and moved the prediction point to admission (2026-09-30).
   - Effect: a model learns that a missing adlp signals an early death, which it cannot know on day 3 in use.
     Measured: filling the 475 "Pt Death" gaps with observed values lowers ROC AUC by 0.0035 (SE
     0.0006, 3 x 3 CV); dropping adlp altogether lowers it by 0.008.
   - Against dropping: adlp is missing for 90.7% of comatose patients (a day-3 state), and the missing flag still
     scores 0.617 among patients in hospital past day 7, so the gap is partly, not wholly, caused by the outcome.
   - Implemented: adlp kept (CC 2026-10-12); the notes now give the 475 patients and the 0.0035.
   - Alternative, recommended by the advocate, the critic and the mediator: drop adlp (cost 0.008-0.009 ROC AUC).
     Blanking only the "Pt Death" rows would put ICPSR values into the data, against the first CC of 2026-10-12. A
     `Potential leak, kept on purpose:` note is not open to a confirmed leak (LEAK-6) and would make the fit
     approximate (USE-8, as for the dataset kick).
   - Rule: LEAK-10 and LEAK-6 (Must); a new fact against a curator's CC, so the curator reopens it.
   - Decision: drop adlp, or keep it with the fact that sets it apart from mic and adls.

10. **edu and income: drop them, or keep them with a note?** Both come from the demographic interview (days 2-7),
   and they are missing more often among patients who die on days 4-7: edu 31.4% against 16.3%, income 43.0% against
   31.5%. Their interview status has no death code.
   - Effect: none measured (dropping both changes ROC AUC by +0.0001).
   - Implemented: kept, no note.
   - Alternative (a): keep them with a `Potential leak, kept on purpose:` note, which makes the fit approximate
     (USE-8).
   - Alternative (b): drop them at no cost and keep the fit direct.
   - Rule: LEAK-10 (weak). Recommendation: (b).
   - Decision: (a) or (b).

8. **The year 2000 has no source: 2001 or 2003?** No source dates a publication of these rows to 2000. The earliest
   evidence: ICPSR 2957 V1, January 2001 (the full study data); support2.csv dated 2003-06-23 inside hbiostat's zip;
   the first archived copy of the page, 2007. PROV-9 takes the year of the first publication that holds the rows.
   - Effect: metadata only.
   - Implemented: 2000 in the record and in dataset.py (unchanged).
   - Alternative: 2003 for Vanderbilt's extract, the file we ship from; or 2001 if ICPSR counts as the first
     publication (then PROV-8 may move the source to ICPSR).
   - Rule: PROV-9 (Must), PROV-8; precedents airfoil_self_noise, first_principles_tully_fisher, nikuradse
     (2026-10-20).
   - Recommendation: 2003, because PROV-9 takes the first publication of the rows we ship, and those are
     Vanderbilt's support2 extract (follow-up cut at the end of 1994, its own derived columns); ICPSR's 2001 release
     holds the study data in another form (follow-up to 1997) and serves here only to place rows.
   - Decision: the year, with the reason written into the record.

9. **pafi above the physical ceiling: set values above 713 missing?** pafi is the day-3 ratio of arterial oxygen
   (PaO2) to inspired oxygen fraction (FiO2). 29 values exceed 600, 14 exceed 650 and 9 exceed 713 (up to 890). By
   the alveolar gas equation at sea level PaO2 stays below FiO2 x 713 minus PaCO2/0.8, so a ratio above about 713
   cannot occur; the 9 are likely a mis-recorded FiO2 (the mediator's inference, not measured).
   - Effect: a handful of wrong values in one feature; tree models are barely affected.
   - Implemented: kept.
   - Alternative, the mediator's recommendation: pafi above 713 set missing, 650-713 kept with a note as unusual.
   - Rule: CLEAN-11 (Should); precedents heart_disease_va_long_beach and thyroid_discordant set impossible values
     missing.
   - Decision: the cut, or keep with a note.

**Review panel:** ship after changes (mediator). Full tier, 2026-10-20. Claim audit: 22 claims, 15 hold, 6 refuted
or overstated (adlp's gaps, the priority note and four sentences; the sentences are fixed, adlp is issue 7), 1
untested (the year, issue 8). Blind review: include with changes; main concern adlp's missingness. Debate: agreed on
the task, cohort, repair, IID split and dropping adlp; disputed: the framing of the physicians' estimates (issue 5). The panel reports number the issues 1-4; in
this file they are 5, 7, 8 and 9.

<details><summary>Mediator</summary>

**Mediator: 2_month_survival_rate_prediction (panel phase C, 2026-10-20)**

Both sides reach "ship after changes"; no one argues exclusion. Almost all disputes were conceded in the rebuttals.
What is left is two calls that reopen or touch CCs of 2026-10-12, one framing choice and two small choices.

**Recommendation (judgment record)**

```text
Verdict: ship after changes.
Validity: SEL holds; USE-1/USE-5/USE-7 hold (direct fit); USE-3 triggered, fixed (prediction point = study day 3);
  USE-6/LEAK-37 triggered for prg2m/prg6m and DNR-by-day-3: fix by framing or by keeping them (issue 1);
  LEAK-10/LEAK-6 triggered for adlp (confirmed, 0.0035 AUC): drop, against CC 2026-10-12 (issue 2);
  LEAK-6 weak for edu/income (no measurable effect; issue 2); SPLIT-1 holds, IID kept, SPLIT-5/SPLIT-7 note rewritten;
  PROV-13/PROV-15 hold (repaired from ICPSR); PROV-9 triggered, year 2000 has no source (issue 3).
Value: TP holds (8,967 rows, ~1,000 positives per test fold, AUC ~0.81, linear 0.785, no flags).
Quality: CLEAN-11 alb > 6 to missing; wblc 0 kept with a note; pafi above the physical ceiling (issue 4).
Weighed: source +, use case +, repair +, Outdated - (no rule behind it).
For the curator: issue 1 framing (objective estimate vs. keep prg2m/DNR); issue 2 adlp drop (reopens a CC) and
  edu/income; issue 3 year 2001 or 2003; issue 4 pafi cut.
```

**Changes to make now (no decision needed)**

1. `task_summary.use_case`: "On the third day in hospital" -> "On the third day after study entry"; 24.6% entered
   after hospital day 3. USE-3 (Must).
2. `curation_comments` bullet 3 and REVIEW issue 6: delete "Two phases cannot give the protocol's three time
   windows" (false: entry date = 1994-12-31 minus d.time for survivors, row order = entry order within blocks,
   Spearman 1.000). State the measurements instead: IID 0.818, temporal over phase II 0.824, phase I -> II 0.820,
   leave-one-block-pair-out 0.815 (0.793-0.831); IID kept because the use case is new patients of the same hospitals
   and years. Replace "not documented" for the blocks with the leave-pair-out score. SPLIT-5, SPLIT-7 (Must).
3. Decision 5 and bullet 9: "missing as often for short as for long stays" is false by early death (edu 31.4% vs
   16.3%, income 43.0% vs 31.5% among deaths on days 4-7 vs others). Rewrite with these numbers whatever issue 2
   decides. EV-7, writing.md.
4. `alb` > 6 g/dL (4 rows: 6.3, 8.6, 10.9, 29.0) set missing, after `_restored` so its asserts hold. CLEAN-11
   (Should); precedents heart_disease_va_long_beach, thyroid_discordant. Both sides agree.
5. `wblc` = 0 (9 rows) stays, with a note. Measured here: 0 is the bottom of a continuum (smallest non-zero values
   0.05, 0.07, 0.08 ...; 159 values below 0.5) and 8 of 9 are MOSF w/Malig, so a reading below the resolution in
   profound neutropenia: only unusual (CLEAN-11). This is the fact that sets it apart from `chol == 0`.
6. Inexact sentences: "up to 90 rows further down" (181 lie further, 90 above); "almost only among them" (64%/69%);
   "DNR orders after study entry are mostly written near death" (32.8% within 2 days, median 6 days, and not
   supportdesc's reason), also in `DROPPED_COLUMNS["dnr"]`. Reword to the measured numbers. EV-7.
7. Record: the 2026-10-20 assessment's "no known risk" is refuted by the adlp finding; add a dated assessment line
   naming it. writing.md / records.md.

**Issues for the curator (ranked)**

**1. prg2m/prg6m and DNR by day 3 (P3 decides P4's inputs; USE-6, LEAK-37 Must; USE-9 Should)**

* Problem: the physicians' day-3 estimates (and a DNR-by-day-3 flag) are known at the prediction point but dropped,
  "as the source advises". A source's advice is not a reason under the ranking. With `use_case` as written ("the care
  team estimates ..."), the drop breaks USE-6, and `changes` wrongly says they are "made from or after these values".
* Effect: prg2m alone 0.801; adding it 0.817 -> 0.839. DNR flag: 1,437 patients, 61.6% positive, 0.814 -> 0.822.
* Advocate (option a): the source's own design is an objective estimate set beside the physician's (Knaus 1995,
  "Objective estimates"; physicians interviewed on day 3 as the comparator, model 0.812 vs physician 0.801). Write
  that actor into `use_case`; then prg2m and DNR are out by the use case and USE-9's "rephrased to excuse a gap" does
  not bite, because the framing predates our gap.
* Critic: accepts (a) as valid if grounded in the source's design, not in the practitioner's "no numeric estimate in
  the chart" (inference, EV-2). Otherwise (b): keep prg2m, prg6m and build the DNR flag (LEAK-7).
* Mediator: both are valid; which framing ships is a weighing call (principles, Weigh). Not settleable by rank. The
  status quo is not an option: one of the two must be written. DNR follows prg2m in one call. Settles it: Lennart's
  choice of actor; if (a), the text cites Knaus 1995 and corrects `changes`; if (b), see breast_cancer_prediction.

**2. adlp kept by CC 2026-10-12; edu and income (P4; LEAK-10, LEAK-6 Must)**

* Problem: adlp's gaps encode deaths after the prediction point. Proof from the codebook: interview status D3P = 10
  "Pt Death" marks 475 patients, all positive, all without adlp; 95.4% of the 767 deaths on days 4-7 lack adlp vs
  58.2% of the others. The CC's table pooled deaths with discharges, which hid this.
* Effect: 0.0035 AUC of adlp's 0.008 (SE 0.0006). Dropping adlp costs 0.008-0.009.
* Both sides: drop adlp (LEAK-6: a confirmed leak goes even when small; mic precedent, same mechanism; the CC's own
  reason for adls). Blanking only the D3P-10 rows would need ICPSR values as features, against CC 1. For keeping:
  adlp is missing for 90.7% of comatose patients (a day-3 state) and the indicator still scores 0.617 among patients
  in hospital past day 7; that makes it partly, not wholly, outcome-driven, which LEAK-6 does not accept for a
  confirmed mechanism.
* Mediator: the rules decide (Must, no higher rule against it): drop adlp. It is a new fact against the curator's CC,
  so the curator reopens it; the AI does not override.
* Sub-call, edu/income (weighing): no measured effect (drop +0.0001, impute -0.0001), mechanism plausible, no death
  code in DEMOG. Keep with a `Potential leak, kept on purpose:` note (both sides' choice; the CC kept them) - but
  USE-8 then makes the fit approximate, as for kick - or drop at zero cost and keep the fit direct (the remedy ladder
  puts "fix the definition" before "keep with a note"). Neither side weighed the fit consequence.

**3. year = "2000" (P5; PROV-9 Must, PROV-8)**

* Problem: no evidence for 2000. Earliest evidence: ICPSR 2957 V1, January 2001; the hbiostat file dated
  2003-06-23; first archive 2007.
* Both sides: change it, required. Open only which publication is the first that holds the rows: ICPSR (2001; then
  PROV-8 may move the source) or Vanderbilt's extract (2003). A fact of provenance for the curator, with the reason
  written into the record (precedents airfoil_self_noise, tully_fisher, nikuradse).

**4. pafi above the physical ceiling (P7; CLEAN-11 Should)**

* Problem: 29 values > 600, 14 > 650, 9 > 713 (up to 890). Mediator's inference (EV-2, lowest rank): by the alveolar
  gas equation PaO2 < FiO2 x 713 - PaCO2/0.8 at sea level, so PaO2/FiO2 cannot exceed ~713; those 9 are impossible,
  likely a mis-recorded FiO2.
* Both sides: a cut or a note; neither picked a threshold. Recommend: > 713 missing, 650-713 kept with a note. A
  quality call on a handful of rows; it does not hold the dataset.

**Agreed facts**

* Real task, the source's own (Knaus 1995 day-3 prognosis); fit direct as long as no potential leak is kept.
* Target `death` = 1 and `d.time` < 60 (sfdm2's cut-off), no censoring (survivors followed >= 344 days); 8,967 rows,
  33.4% positive. The 138 day-3 deaths are no task row and carry values at death (hrt 0 in 38.4%); dropping them is
  right (USE-7). The blind reviewer's doubts here were made without the raw file and are answered by the claim audit.
* Phase II physiology misplaced in support2/UCI 880 and restored through ICPSR 1:1 links; transfer phase I -> II
  0.696 published vs 0.821 restored (reproduced). Only support2 values ship (CC 2026-10-12).
* IID scores no higher than temporal or leave-block-out (0.818 / 0.824 / 0.815); one row per patient, no copies.
* adlp gaps encode post-day-3 deaths (D3P = 10); effect 0.0035 AUC.
* edu/income: missingness higher among early deaths; no measurable effect.
* year 2000 unsupported; alb > 6 impossible; wblc 0 plausible; Outdated has no rule behind it.

**Consistency with precedent**

* Follows: day-3 deaths dropped (diabetes_130_us; mic set apart by its missing day of death); IID for a clinical
  cohort (breast_cancer_prediction, cirrhosis, framingham); one 60-day target (cirrhosis_patient_survival_prediction,
  LEAK-23); repair from ICPSR (SUPPORT2 row in provenance.md Cases); model outputs dropped (yeast); `Outdated` with Yes
  (six heart_disease / hepatitis / horse_colic records; first_order_theorem_proving is the outlier).
* adlp: dropping it follows mic and the CC's own adls call; the current keep departs from them (the precedents
  report's consistency check 3).
* prg2m/DNR: option (b) follows breast_cancer_prediction, brazilian_ecommerce, bias_correction. Option (a) departs
  and must name the fact that sets it apart: the source's design measured the physician as the comparator of an
  objective estimate, so the actor is not the one who holds the estimate. If chosen, record it as the reason; if USE-6
  should say so in general, that is an amendment (precedents report, check 1d).
* wblc 0: departs from the precedents report's suggestion (missing) by a measured fact (a continuum down to 0.05,
  neutropenic cancer patients), unlike `chol == 0`.
* year: PROV-9 cases of 2026-10-20 require the first-publication year with a reason.

</details>

<details><summary>Claim audit</summary>

**2_month_survival_rate_prediction: claim audit (panel phase A, 2026-10-20)**

Adversary of the definition. ICPSR part 10 fields were read for the audit only. All models: LightGBM
(300 trees, lr 0.03, 15 leaves), untuned, 3 x 3 stratified CV seed 4267 on the definition's 8,967 rows and 25
features unless stated; thread caps 2. "prep" = measured by the prep run, cited, not
re-run by me.

**Table**

| # | Claim | Source | Test | Result | Evidence | Rule |
|---|---|---|---|---|---|---|
| 84, 48, CC 3 (implied: adlp's gaps record nothing after day 3) | "the patient's answer is missing mostly when the patient cannot answer"; adlp kept while adls goes because adls' gaps record events after the prediction point | Decision 5; curation_comments bullet 9; record CC 2026-10-12 | Read the day-3 patient interview status `D3P` (ICPSR part 10 cols 462-463, codebook value labels) for every linked patient; crosstab with adlp missing and the target; refit with the 475 "Pt Death" rows' adlp replaced by random observed values | **"mostly" holds; the implied claim is refuted.** adlp is present iff D3P = 1 (3,462 of 3,479; 0 present otherwise). Of 5,505 gaps: coma/intubated 2,668, unable to communicate 716, failed cognitive screen 491 (70% cannot answer); but **"Pt Death" 475 (8.6%): all 475 positive, 98.3% died by day 7, median day 5**, and "Pt Discharged" 505 (98.4% stay <= 7 days). Same mechanism as adls, smaller. Effect: shipped 0.8180; D3P-10 rows imputed 0.8144 (-0.0035, SE 0.0006); D3P 9/10 imputed -0.0018 (SE 0.0008); drop adlp -0.0081 (SE 0.0009); adding D3P itself +0.014 | LEAK-10 (missingness that encodes the outcome), USE-3; EV-6 proof (the codebook status, not a proxy) |
| 105 | priority 4, "no known risk" | record Assessment 2026-10-20 | follows from the row above | refuted in part: a measured weak outcome-caused missingness is a known risk | above | LEAK-10 |
| 30 | "the others' block sits up to 90 rows further down" | curation_comments bullet 2 | offsets source row - row in phase II | **refuted (wording)**: own 431, 1-90 down 4,102, >90 down 181 (max 1,094), above the row 90 (min -7,752). Decision 2 and the record say it right | offsets | writing.md, EV-7 |
| 85 | "heart rate and mean blood pressure of 0 occur almost only among them" (day-3 deaths) | Decision 6 text | count zeros in all 9,105 restored rows by day of death | **refuted (wording)**: hrt 0 in 83 patients, 53 of them day-3 deaths (64%); meanbp 0 in 51, 35 (69%). The rate claim holds (38.4% / 25.4% on day 3 against 7.1% / 3.4% on day 4, <= 1.3% later); 30 and 16 remain in the cohort (bullet 11 says so) | zeros by day of death | writing.md |
| 42, 64 | "DNR orders after study entry are mostly written near death" | curation_comments bullet 6; DROPPED_COLUMNS["dnr"] | after-entry orders: days from order to death | **weak / overstated**: 2,956 after-entry orders, 92.6% of these patients die; of those, 32.8% within 2 days of death, 54.7% within 7, median 6 days. JAMA 1995 abstract: "46% of do-not-resuscitate (DNR) orders were written within 2 days of death" (phase I). supportdesc gives no reason, only "You also will probably not want to use prg2m, prg6m, dnr, dnrday". Drop still right: dnrday = slos without an order (claim 65, prep), 1,659 orders dated after day 3 | PubMed 7474243; supportdesc fetched 2026-10-20 | LEAK-10 (drop holds), writing.md (reason) |
| 2 (implied) | "On the third day in hospital" | task_summary.use_case | hday distribution | refuted (wording, prep): 24.6% entered the study after hospital day 3 (hday max 148); the point is study day 3 | hday | USE-3 |
| 10 | year = "2000" | dataset.py, record | web search; zip date; supportdesc page | untested (cannot verify): no first-publication date found; zip 2003-06-23, earliest archive 2007 (prep); supportdesc has no date | search 2026-10-20 | PROV-9 |
| 49 | edu and income "missing as often for short as for long stays" | bullet 9; Decision 5 | (a) by stay length; (b) by death by day 7; (c) demographics-interview status `DEMOG`; (d) refit with edu/income replaced for DEMOG 11/13 | **holds in effect.** (a) 0.171/0.186, 0.326/0.323 as stated; but (b) edu missing 31.4% among deaths by day 7 vs 16.3%, income 43.0% vs 31.5% (DEMOG has no death code; "Other non-response" rows: 44% died by day 7). (d) no effect: drop edu+income +0.0001, imputed -0.0001 (SE 0.0002-0.0005) | refits | LEAK-10 (no leak measurable) |
| 33, 6, 35, 36 (implied: IID is the split the use case needs) | IID over patients; new patients of the same hospitals and years; two phases cannot give 3 windows; blocks undocumented | task_summary.split; bullet 3 | temporal phase I -> phase II vs IID of equal train size; leave-one-block-pair-out; ICPSR `SITE` | **holds.** Phase I -> II 0.821; IID same size 0.815 (scored on phase II rows 0.824); IID 3 x 5 0.819; leave-one-block-pair-out mean 0.813 (0.790-0.831). No optimism from IID. `SITE` is blank in the public ICPSR part 10 (all 9,105), so the hospital is not documented (36 holds); "probably hospital" stays untested | refits | SPLIT-1, SPLIT-5, SPLIT-30 |
| implied: no copy across the split | one row per patient | definition | duplicates; ICPSR PSEUDOID; codebook on readmissions | holds: 0 duplicate rows / feature vectors (prep); 9,105 rows link 1:1 to 9,105 PSEUDOIDs; readmissions were abstracted into the same patient record ("index hospital admission and up to six readmissions"), not new rows | codebook p. 20-22 | LEAK-16, SPLIT-29 |
| implied: every kept feature known at day 3 | 25 kept features | dataset.py | codebook definitions | holds except adlp's gaps (row 1): num.co, diabetes, dementia, ca "from admission input forms"; scoma is SCOMA3 (link matches it exactly); physiology day 3 with previous-day or normal fills (Appendix B); hday = study adm - hospital adm + 1; edu/income/race from the days 2-7 interview or hospital systems (values pre-admission facts) | codebook p. 384-385, 388, 443, 532-539 | LEAK-10, USE-3 |
| implied: the target is the real-world target | death < 60 days of study entry | bullet 4 | codebook `d-time = (death date - study adm date) + 1`; sfdm2 code `IF death & (.<d_time<60) THEN sfdm2=99` | holds: same cut-off as the source's sfdm2; 2,985 of 2,993 positives at sfdm2 level 5, 8 reclassified manually ("Some cases were classified manually", codebook); 0 negatives at level 5 (prep) | codebook p. 384, 388 | USE-5 |
| 40a-c, 21 | 138 day-3 deaths dropped; dead at the prediction point; hrt 0 in 38% | intro, bullet 5 | d.time convention and minimum; zeros by d.time | holds: d.time counts the entry day as day 1, minimum d.time is 3, so d.time <= 3 is death on study day 3; hrt 0 38.4%; 8,967 kept | codebook p. 384 | LEAK-22, USE-3 |
| 22, 72 | quotes "11 physiologic measures recorded on day 3 after study entry", "4301 hospitalized adults were selected for phase I" | bullet 1; PHASE_1_PATIENTS | PubMed E-utilities abstract 7810938 | holds verbatim (abstract; the prep could not read it) | PubMed 7810938 | EV-2 |
| 34 | "failed to improve care or patient outcomes" | bullet 3 | PubMed abstract 7474243 | holds verbatim. Note: intervention physicians received the model's 6-month estimates; prg2m/prg6m are dropped, so no feature carries it | PubMed 7474243 | EV-2 |
| 45a-b, 47 | ADL = function two weeks before admission; interviews days 2-7, median day 4; adlsc imputation used interview status | bullet 9 | codebook | holds: "reflecting patient status two weeks before admission" (p. 501); "interviewed in the hospital between days 2 and 7 (median day 4) ... whether or not the patient remained hospitalized" (p. 443); "patient status code ... is very important in predicting ADLD3S" with groups "Pt Discharged", "Pt Death" (p. 532-533) | codebook | EV-2 |
| 74 | normal-value fills (Appendix B; bun, urine from supportdesc); support2 has them as missing | ICPSR_NORMAL_FILLS | Appendix B; fills in shipped data | holds: Appendix B lists wbc 9.00, albumin 3.5, bili 1.01, crea 1.01, PaO2 70/FiO2 21 (= pafi 333.3), plus temp 37.99, hrt 75.11, sod 140.01 which the definition omits; 0 rows of the shipped temp/hrt/sod and 0 ICPSR day-3 rows sit at those values, so the omission changes nothing; supportdesc lists bun 6.51 and urine 2502 | codebook p. 539 | PROV-13 |
| 15 | UCI 880 is the same table, differs only in prg6m rounding | download_description | downloaded UCI data.csv, compared cell by cell | holds: same shape, ids, columns; only prg6m differs (19 cells, max 0.00037) | UCI download | PROV-4 |
| 98 | phase I model: 0.812 on phase II restored, 0.695 as published | record 2026-10-12 | refit on phase I, score phase II with restored and published physiology | holds: 0.821 / 0.696 | refit | EV-8 |
| 24, 29, 32, 26, 27, 38, 39, 51, 53, 54, 52, 65 | link, own-block counts, Spearman, deaths agree, follow-up, prevalence, vital zeros, duplicates, dzclass, splits, dnrday | curation_comments, decisions | prep's claim checks, and my scripts reproduce 431 / 4,301 / 138 / 8,967 / 2,993 | holds (prep; numbers reproduced where my scripts touch them) | prep | PROV-13, EV-7 |
| 13, 14, 16, 17 | licence quote, SHA-256, ICPSR version, BibTeX | dataset.py | prep (page fetch, hashes) | holds (prep, not re-run) | prep | EV-4 |
| 80 | as published phase II carries no signal; restored behaves as phase I | Decision 1 | prep and the 0.696 / 0.821 transfer above | holds | refit | PROV-13 |

**Refuted and untested, ranked (principles.md: validity first, Must first)**

1. **P4, LEAK-10 (Must, graded weak): adlp's missingness encodes death before the day-3 interview for 475 patients.**
   Proof (EV-6), not circumstantial: the codebook's own interview status D3P = 10 "Pt Death" marks 475 cohort
   patients, all positive, 98.3% dead by day 7, and every one lacks adlp; 505 more lack it because they were
   discharged (an event after day 3). This is the mechanism CC 3 used to drop adls. Size: 0.0035 AUC of adlp's 0.008
   (SE 0.0006), against a full-model 0.818. What it changes: the "no known risk" priority note and the basis of CC 3
   (a new fact, so the curator's keep is open again, not overridden). Mildest remedy, for the curator: (a) keep
   adlp with a `Potential leak, kept on purpose:` note giving the 475 / 0.0035 numbers (the CC stands with the new
   fact written down), or (b) drop adlp as adls was dropped (-0.008 AUC, removes the leak entirely). Using ICPSR's
   D3P to blank or recode values would break CC 1 (ICPSR only places rows) and is not recommended.
2. **P3, USE-3 (Must, wording): "On the third day in hospital"** should be "on the third day after study entry"; 24.6%
   of patients entered after hospital day 3. Remedy: one-line edit of `task_summary.use_case`.
3. **P5, PROV-9 (Must): year = "2000" untested** (cannot verify). Earliest evidence 2003-06-23 (zip date). Remedy:
   keep with "not established" or set to the earliest evidenced year after the curator's call.
4. **Procedure (writing.md, EV-7): three inexact statements.** "up to 90 rows further down" (181 rows further, 90
   above); Decision 6 "almost only among them" (64% / 69% of the zeros, the rates are what differ); "DNR orders after
   study entry are mostly written near death" (32.8% within 2 days, 54.7% within 7; JAMA: 46% within 2 days) and
   presented as the source's reason, which supportdesc does not give. Remedy: reword; the drops stay.
5. Untested: "the ten blocks are phase by, probably, hospital" (SITE is blank in the public file; written as a guess,
   which is honest).

No refutation of the split (IID gives no optimism over phase I -> II), the target, the cohort cut, the repair, or
the copy question.

</details>

<details><summary>Column audit</summary>

**2_month_survival_rate_prediction: column audit (panel phase A, 2026-10-20)**

Prediction point (curation_comments, bullet 1): the end of study day 3. Cohort: 8,967 patients alive after day 3;
target death within 60 days of study entry (33.4%). Frame loaded with `dataset_io.from_definition` (25 features plus
target; the frame is shuffled, so it was aligned to support2 rows by matching every feature against the definition's
own `_clean` output, 8,967 of 8,967 unique). ICPSR 2957 part 10 fields (patient interview status `D3P`, demographic
questionnaire status `DEMOG`, `ADLD3PC`, `SCOMA3`, `HDAY`, comorbidities) were joined through the definition's `_link`
for checking only. Codebook: ICPSR 02957-Codebook.pdf, hbiostat supportdesc (fetched 2026-10-20). LightGBM numbers: 3 of the shipped splits (repeat 0), 300 trees,
lr 0.03; they compare variants, they are not leaderboard numbers.

**Column table**

| column | meaning (source) | known at prediction? | dtype and cleaning | verdict | rule |
|---|---|---|---|---|---|
| age | age at study admission in years, (adm date - birthday)/365.25 (codebook p.~17) | yes, at entry | float64, 18.0-101.8, no NA | fine | - |
| sex | patient sex | yes | category (male/female) | fine | CLEAN-14 |
| dzgroup | SUPPORT disease group at entry, 8 levels (codebook DZGROUP 1-8) | yes, entry criterion | category | fine | - |
| dzclass | 4-class grouping of dzgroup (codebook DZCLASS) | yes | category; a deterministic function of dzgroup (each dzgroup maps to one dzclass), not an exact copy | fine (kept as in source, noted) | CLEAN-5 not triggered |
| num_co | number of comorbidity fields coded, from the admission input forms (codebook "num-co", col1-co9 "from Admission input forms") | yes, admission | int64 0-9; renamed from num.co | fine | - |
| edu | years of education, demographic questionnaire (patient or surrogate, first interview days 2-7) | value: a pre-admission fact; recorded on days 2-7. Missingness: partly caused by death after day 3 | float64 0-31; NA 17.6%; not the ICPSR CART imputation (support2 keeps NA). 43 zeros (plausible), 8 values > 25 (unusual, kept) | maybe a weak leak (missingness) | LEAK-10 (weak), question |
| income | income band, demographic questionnaire | as edu | category (4 bands, ordinal kept as categorical); NA 32.5% | maybe a weak leak (missingness) | LEAK-10 (weak), question |
| scoma | SUPPORT coma score on study day 3 from the Glasgow score (codebook scomax; equals ICPSR SCOMA3 for 8,967 of 8,967) | yes, day 3 | float64, 11 values 0-100; a fixed monotone recoding of GCS (8-10 tied) | fine (note: weights may have been derived in SUPPORT model work; a monotone recoding of an ordinal, so no information a tree could not get from GCS) | LEAK-30 "fixed published scales are fine"; LEAK-27 not triggered |
| race | race; demographic questionnaire, else administrative files, else imputed white (codebook "race") | yes (pre-admission fact) | category, 5 levels; NA 39 (0.4%); support2 does not apply the "impute white" rule visibly; whether some "white" rows are imputed cannot be checked (ICPSR IMPRACE blank) | fine; minor question | CLEAN-10 |
| hday | day in hospital at which the patient entered the study, (study adm - hosp adm) + 1 (codebook; supportdesc) | yes, at entry | int64 1-148 | fine (note: use_case says "third day in hospital", but 24.6% entered after hospital day 3; wording, see checklist) | USE-3 wording |
| diabetes | diabetes comorbidity from admission forms/admission diagnoses (codebook "diabetes") | yes | category 0/1 | fine | CLEAN-14 |
| dementia | dementia comorbidity from admission forms (codebook "dementia") | yes | category 0/1 | fine | CLEAN-14 |
| ca | cancer: no / yes / metastatic (ICPSR CA 0/1/2, matches 8,967 of 8,967) | yes | category | fine | - |
| meanbp | mean arterial BP, study day 3 (restored from support2's own values via ICPSR) | yes, day 3 | float64 0-195; 16 zeros (13 with hrt 0), 81% die: kept as day-3 arrests (curation bullet 11) | fine (documented anomaly) | CLEAN-11 (kept as plausible) |
| wblc | white blood count (thousands), day 3 | yes | float64 0-200; NA 2.3%; 9 zeros, 8 of them MOSF w/Malig (neutropenia, plausible) | fine | CLEAN-11 |
| hrt | heart rate, day 3 | yes | float64 0-300; 30 zeros (83% die), one value > 250 | fine (documented anomaly) | CLEAN-11 |
| resp | respiration rate, day 3 | yes | float64 0-90; 30 zeros (16 with hrt 0; some may be ventilated patients), 6 values >= 70 | fine (documented) | CLEAN-11 |
| temp | temperature (C), day 3 | yes | float64 31.7-41.3; 10 values < 33 (90% die; hypothermia plausible) | fine | - |
| pafi | PaO2/FiO2, day 3 | yes | float64 12-890; NA 25.9% (no blood gas; fewer NA among early deaths, a pre-day-3 care process); 29 values > 600, max 890, physiologically implausible above ~650 | cleaning question (small) | CLEAN-11 |
| alb | serum albumin (g/dL), day 3 | yes | float64 0.4-29.0; NA 37%; 4 values > 6 (6.3, 8.6, 10.9, 29.0) are impossible in g/dL (29.0 looks like g/L) | cleaning problem (small) | CLEAN-11 |
| bili | bilirubin (mg/dL), day 3 | yes | float64 0.1-63; NA 28.5%; 20 values > 40 (extreme, 18 die; plausible in liver failure) | fine | - |
| crea | serum creatinine (mg/dL), day 3 | yes | float64 0.1-21.5; NA 0.7% | fine | - |
| sod | serum sodium, day 3 | yes | float64 110-175 | fine | - |
| ph | arterial pH, day 3 | yes | float64 6.83-7.77; NA 25.4% (with pafi: no blood gas) | fine | - |
| adlp | ADL index (0-7) reported by the patient at the first patient interview (ICPSR ADLD3P; equals ADLD3PC on all 3,462 non-missing rows) | value: pre-admission function, but recorded days 2-7 (median day 4). Missingness: for 475 patients caused by death after day 3 | float64 0-7, 8 values; NA 61.4% | LEAK (missingness caused by the outcome), moderate-weak | LEAK-10 (Must) |
| death_within_2_months | target: death = 1 and d.time < 60 | label | category Yes/No, 33.4% Yes | fine | CLEAN-15 |

No dropped column (DROPPED_COLUMNS, bun, glucose, urine) survives in the frame. No identifier column. No duplicate rows.

**Problems, ranked (principles.md: P4 before P7, Must before Should, then effect size)**

**1. adlp: its gaps record deaths after the prediction point (P4, LEAK-10 Must; missingness that encodes the outcome)**

Evidence (measured):

* ICPSR part 10 `D3P` is the status of the first patient interview. Codebook value labels: 1 "Int Conducted", 7 "Coma
  or intub", 9 "Pt Discharged", **10 "Pt Death/Pt alive for AD"**, 14 "Unable to Communicate", etc. adlp is present
  only for `D3P` = 1 (3,462 of 3,479); every other status is missing.
* In the cohort, **475 patients have `D3P` = 10; all 475 die within 2 months (100% positive), on study day 4-8
  (median 5)**. They are 8.6% of the 5,505 missing adlp and 15.9% of all positives. 467 of the 767 patients who die on
  days 4-7 carry this status; 95.4% of those 767 lack adlp, against 58.2% of everyone else.
* adlp missing indicator alone: ROC AUC 0.654 on all patients, 0.631 on patients alive after day 7 (the remaining
  signal is the real "too sick to interview" process: `D3P` 7 "Coma or intub", 49% die).
* LightGBM, 3 splits: all features 0.812; without adlp 0.804; with the death-caused gaps given their own value (an
  oracle that shows what the gap holds) 0.823.
* `D3P` = 9 "Pt Discharged" (505 patients, 14% die) is the other post-day-3 event in the gap; it pushes toward the
  negative class, weaker.

Why it matters: the curator's CC of 2026-10-12 kept adlp because it is "missing mostly when the patient cannot
answer" and dropped adls because "the surrogate interview's gaps depend on whether the stay lasted until the
interview, which is after the prediction point". The codebook status shows the same mechanism in adlp: a gap coded
"Pt Death" for 475 patients who died after day 3. The decision table in the definition grouped by "stay ended by day 7"
(deaths and discharges together), which hid it. This is a consistency question (principles.md, case 1): treat adlp
like adls, or say what sets it apart.

Mildest remedy that resolves it: drop adlp (cost about 0.008 ROC AUC, all of it within 0.812 to 0.804; part of that is
the leak). Alternatives, worse: move the prediction point to after the first interview (study day 7) and drop the
patients who die by then (the mic precedent; changes the task and the cohort); keep with a note (not allowed for a
confirmed outcome-caused gap: LEAK-6 "a confirmed leak goes even when small"). The value itself also exists only at the
interview (median day 4), a second, weaker reason. Strength: proof for 475 rows (codebook code + measured outcome);
effect on the score small.

**2. edu and income: gaps more common among patients who die on days 4-7 (P4, LEAK-10; weak, circumstantial)**

Evidence: both come from the demographic questionnaire (codebook: "When a demographic questionnaire was not completed
... collected whatever information they could through administrative means"; edu NA is 5.9% when `DEMOG` = 1 "Int
Conducted" and 99.5-100% otherwise). Missing among the 767 patients who die on days 4-7 against everyone else: edu
31.4% vs 16.3%, income 43.0% vs 31.5%. Missing indicator alone: edu 0.542 (0.528 among patients alive after day 7),
income 0.535 (0.525). `DEMOG` has no "Pt Death" code in the cohort, but 104 of the early deaths have 11 "Other
non-response" or 13 "No surrogate" (statuses with 67% and 49% positives). LightGBM without edu and income: 0.8121 vs
0.8120 with them: they add nothing measurable either way.

The definition's claim "edu and income are missing as often for short as for long stays" holds for the slos grouping
but not for early deaths; the decision text should not rest on it. Remedy, a curator call (Weigh): drop both (cost 0.000
ROC AUC; consistent with the adls reasoning) or keep with a `Potential leak, kept on purpose:` note giving these
numbers. Strength: weak; mechanism plausible, not proved per row.

**3. alb: four impossible values (P7, CLEAN-11 Should)**

alb 6.3, 8.6, 10.898 and 29.0 g/dL; serum albumin above about 6 g/dL does not occur, 29.0 reads as g/L. Remedy: set
alb > 6 to missing (4 rows), or keep with a note. Tree models are barely affected.

**4. pafi above 600 (P7, CLEAN-11 Should; question)**

29 values from 603 to 890. PaO2/FiO2 above about 650 is not attainable at sea level; values in 600-650 are borderline.
Remedy: set pafi > 650 (or a cut the curator picks) to missing, or keep with a note as unusual values. Question for the
curator; small.

**5. Notes, no action needed**

* hday shows that 24.6% of patients entered the study after hospital day 3, so `use_case` "On the third day in
  hospital" should read "on the third day of the study" (USE-3 wording; already in the checklist).
* scoma is the SUPPORT coma score, a fixed monotone recoding of the Glasgow score (GCS 8-10 tied); its weights may come
  from the SUPPORT modelling (inference, not checked). A monotone recoding of an 11-level ordinal gives a tree nothing
  the GCS would not; fine under LEAK-30's "fixed published scales".
* race: the codebook says a missing race was imputed white in the study files; support2 keeps 39 missing, and whether
  some "white" rows are imputed cannot be checked (ICPSR IMPRACE is blank). Minor.
* hrt, meanbp, resp zeros among the patients alive after day 3 (30, 16, 30; overlapping) are kept as day-3 arrests,
  as documented; fine.
* dzclass is a coarsening of dzgroup, kept as in the source; fine.
* pafi and ph are missing less often among early deaths (10% vs 27%): blood gases are drawn in sicker patients before
  day 3, a pre-prediction-point care process, not a leak.

**Judgment record (column part)**

Validity: LEAK-10 triggered for adlp (outcome-caused gaps, 475 patients, all positive), fix: drop adlp; LEAK-10 maybe,
weak, for edu and income (curator call); every other column is recorded at entry or on study day 3 (codebook).
Quality: CLEAN-11 for alb > 6 (4 rows) and pafi > ~650 (question). For the curator: issue 1 is a consistency check
against the 2026-10-12 CC that kept adlp and dropped adls for the same mechanism.

</details>

<details><summary>Split audit</summary>

**Split audit: 2_month_survival_rate_prediction (review panel, phase A, 2026-10-20)**

**Verdict: right with notes**

IID over patients holds under the stated use case and the precedent of the other clinical cohorts of the copy (all
IID). But the reason the definition gives against a temporal split is false: the study-entry date of every patient
is recoverable from the file, to about a day, and three windows are possible. Measured, a temporal split and a
hospital-grouped split score the same as the shipped IID split, so the choice changes no score; the note has to be
corrected, and the regime is a weighing call for the curator.

**What was checked**

* Declared: `split_regime: iid`, 3 repeats x 3 folds, seed 4267, stratified; every fold 5,978 train / 2,989 test,
  positive share 0.334 in every test fold, no train/test overlap. No `splits_comment`; the reason sits in
  `curation_comments` bullet 3 ("Two phases cannot give the protocol's three time windows, and the file's ten blocks
  ... are not documented").
* Entity: one row per patient. All 9,105 support2 rows link one-to-one to an ICPSR `PSEUDOID` (`_link`); each patient
  enrolled once. Hidden-group probe: no hit (candidates `resp`, `sod`, `edu`, gaps +0.013/+0.009/-0.016; no composite
  key; 0% of rows in near-copy clusters at 0.7-0.9). Leak probe: 0% exact copies across the split.
* Use case (USE-10): a new patient at study day 3; there is no patient history to carry (first and only admission in
  the study), so no cold-start question. The hospital is a known entity at deployment ("new patients of the same
  hospitals").

**Problems, ranked**

**1. (P4, SPLIT-7 / SPLIT-22 / SPLIT-5, Must on the facts; the regime itself a weighing call) A hidden time axis exists; the note says it does not**

Evidence:
* support2's follow-up ends on 31 Dec 1994 (claims 38, 96), so a survivor's study entry is 1994-12-31 minus `d.time`.
  Within each of the ten file blocks the row order is exactly the entry order: Spearman(row position, entry date) =
  1.000 for the survivors of all ten blocks.
* Every block spans its whole phase: phase I blocks 1989-06-11 .. 1991-06-09, phase II blocks 1992-01-06 ..
  1994-01-21. So the blocks are hospitals within phase, ordered by entry (also supports "phase by hospital").
* Interpolating the entry date of the decedents from their neighbours in the block: on 20% hidden survivors the error is
  median 0.7 days, p90 2.3, max 11.4; no decedent's implied death date falls after 1994-12-31.
* Enrollment is steady: 129-629 patients per quarter (18 quarters); the 2-month death rate per quarter 0.29-0.37 with no
  trend. Adversarial AUC phase I vs II 0.663 (protocol and case mix: ARF/MOSF w/Sepsis 35% -> 42%); first vs second
  half within phase II 0.539, within phase I 0.587.

Scores (LightGBM 300 trees / random forest 300 trees, ROC AUC):

| Split | train rows | test rows | LightGBM | RF |
|---|---|---|---|---|
| IID shipped (9 folds, mean) | 5,978 | 2,989 | 0.818 | 0.815 |
| temporal, 3 windows over phase II (~8 months each), expanding train, 60-day gap | 4,232-6,940 | ~1,580 | 0.824 | 0.822 |
| same, no gap | 4,232-7,383 | ~1,580 | 0.824 | 0.823 |
| phase I -> phase II (Knaus et al. 1995's own design) | 4,232 | 4,735 | 0.820 | 0.819 |

Windows: 1992-01-06..09-03 (0.818/0.817), 1992-09-03..1993-05-03 (0.835/0.828), 1993-05-03..1994-02-01
(0.818/0.822). The 60-day gap (the label delay, SPLIT-10) changes nothing measurable.

Reading: the source's own validation (the SUPPORT model fit on phase I, validated on phase II) is temporal, and the
use case is a model used on later patients (SPLIT-1, SPLIT-19 Should), which argues for temporal. Against: the
precedent of every other clinical cohort in the copy (cirrhosis_patient_survival_prediction, diabetes_130_us,
framingham_heart_study_fhs, ... all IID), the task_summary's framing "new patients of the same hospitals and years",
and no measured shift (temporal scores equal or above IID; SPLIT-4 says the gap never decides, in either direction).
So IID is defensible, but the stated fact behind it is wrong.

Rule: SPLIT-7 (a hidden timestamp does not make a task IID), SPLIT-22 (row order as time), SPLIT-5 (check a claim
about a split against the data), USE-10 / SPLIT-3 (one regime, from the use case).

Mildest remedy: fix the note (bullet 3): the entry date is recoverable (survivors' follow-up to 1994-12-31, row order
= entry order within each hospital block), a temporal split over phase II scores the same as IID (0.824 vs 0.818), and
IID is kept because the use case is new patients of the same hospitals and years and the cohort precedent is IID. If
the curator prefers temporal instead: a re-split with a derived entry-date index (not a feature), three ~8-month
windows over phase II with an expanding train side and a 60-day gap; start the first window after the 50% point
(about Feb 1992), since train = phase I alone is 4,232 of 8,967 = 47.2%, below SPLIT-14's floor. Caution for that
variant: the index is derived from `d.time` (an outcome column) only through the survivors' administrative censoring
date and the row order; it must never become a feature.

**2. (P4, SPLIT-29 / SPLIT-30; weighed factor "only a few groups") Hospitals: no grouping needed — holds**

Evidence: the ten blocks pair into five hospitals (each pair is one phase I and one phase II block with a matching
case mix, e.g. blocks 8/9: COPD 20%/18%, lung cancer 18%/14%; positive share per block 0.28-0.38). Leave-one-hospital-
pair-out: LightGBM 0.815, RF 0.811 (per pair 0.793-0.831) against IID 0.818/0.815. The hospital is known for every new
patient in the use case (SPLIT-4), there are only five, and the hospital id is not in the data (ICPSR `SITE` is blank
in the public-use file). No action; the note could state the measurement instead of "not documented".

**3. (P4, SPLIT-29) Hidden entities across the split: none — holds**

One row per patient (9,105 distinct ICPSR ids), no duplicates or near copies, no probe hit. A within-hospital cluster
(attending physician; phase II randomised by physician group) is not in the data and cannot be recovered; not a reason
to act (SPLIT-25 applies only when the groups matter, and the leave-hospital-out score shows no group effect).

**4. (procedure, minor) Fold design**

Stratified 3 x 3; 997+ minority rows per test fold; positive share identical across folds. No issue.

**Not checked**

The codebook PDF (no PDF reader in the environment): the meaning of ICPSR `INTERV` (0/1 in both phases, so not the
phase II intervention arm) was not read.

</details>

<details><summary>Domain practitioner</summary>

**Practitioner review: 2_month_survival_rate_prediction (panel phase A, 2026-10-20)**

Actor: an attending physician / palliative-care consult team at a US teaching hospital, on study day 3 of a seriously
ill adult's stay, deciding whether and how to open a prognosis and goals-of-care conversation (and whether to refer to
palliative care or hospice). Probes: (LightGBM, 3 x 5-fold stratified CV on the 8,967-patient cohort, restored physiology, thread caps on).

**Fit: direct**

The rows (one patient alive at the end of study day 3), the inputs (all recorded by day 3), the label (death within 60
days, uncensored) and the split (new patients of the same hospitals) mirror the SUPPORT model's own use, an objective
day-3 estimate that the physician combines with their own judgment (Knaus 1995); the gaps below are inputs left out and
a horizon choice, not stand-ins (USE-8, USE-9).

**1. Inputs at the prediction point**

Have, and the dataset has them: age, sex, diagnosis group, comorbidity count, cancer, diabetes, dementia, coma score,
day-3 vitals and labs (meanbp, wblc, hrt, resp, temp, pafi, alb, bili, crea, sod, ph), days in hospital before entry,
patient-reported ADLs, education, income, race. Nothing in the 25 features is recorded after day 3 (USE-3).

Would have on day 3, but the dataset drops (ranked by effect):

1. **My own 2-month estimate (prg2m).** Knaus 1995 (abstract): "Physicians were interviewed on day 3" and "The best
   survival estimates combine an objective prognosis with a physician's clinical estimate". Known at the prediction
   point, missing for 17.6% of patients and independent of the outcome (17.3% of survivors, 18.2% of deaths). Adding it
   lifts ROC AUC 0.817 -> 0.839, log loss 0.484 -> 0.458; alone it scores 0.801 (the model on the same rows 0.812, as
   Knaus found: model and physician about equal). USE-6 says an estimate made before the outcome is an input, and
   dropping it turns the task into "predict without the clinician's estimate". Counter (USE-9): the SUPPORT model was
   built as exactly that objective estimate, and in routine care nobody writes a numeric estimate in the chart. The
   `changes` text groups it with "scores ... made from or after these values", which is not true of prg2m: it is made
   on day 3, alongside the values, not from them. Worth a sentence in `curation_comments` saying it is dropped by
   choice (the objective-model use case), not because it is unknown at day 3.
2. **DNR status by day 3.** In the chart on day 3: 1,437 patients (231 before study entry plus orders on days 0-3),
   61.6% die within 2 months; flag adds +0.008 AUC (0.825). It is a care decision carrying the prognosis, and dnrday
   as published is unusable (equals slos without an order). For my decision it matters differently: a patient with a
   DNR order already had the goals-of-care conversation, so they are arguably not in the population I would screen.
   Either keep the flag (USE-6) or say why it is out; I would not drop these patients.
3. **BUN, glucose, urine output.** I always have BUN and glucose on day 3; they are dropped because phase I did not
   measure them. Defensible (structural missingness tied to phase), small loss; worth naming in `known` as "not all
   labs".
4. **APACHE III physiology score (aps).** Computed from day-3 values, so known then (USE-6), but it adds only +0.002
   AUC; dropping it costs nothing. sps/surv2m/surv6m are SUPPORT-model outputs fit on phase I outcomes, so dropping
   them is right (they carry outcome information of half the cohort).
5. **Not in the source at all:** ventilation, vasopressors, ICU vs ward, day-1 values (trajectory), code status
   history, frailty. A modern model would use them; not a curation gap.

**2. Target**

What I act on is a probability of death over a horizon, at the resolution of "low / uncertain / high". The 2-month
label is real and uncensored (USE-5 satisfied). But the horizon most decisions hinge on is 6 months: the Medicare
hospice benefit requires a prognosis of 6 months or less, and the SUPPORT model's primary target was 180-day survival
(Knaus 1995: ROC 0.79 phase I, 0.78 phase II). 6-month death here is 45.9% vs 33.4% at 2 months. The curator chose 2
months (record CC 2026-10-12, one target); I would accept it, but name 6 months as the hospice-referral alternative.
I want a probability, so calibration matters: the shipped features give well-calibrated deciles (predicted 0.057 ->
0.841 vs observed 0.048 -> 0.842; one bump at decile 6, 0.283 vs 0.345). ROC AUC as the metric ignores calibration;
log loss would match the use better.

**3. Rows and test data**

One row = one patient at one decision point, as I make it (USE-11 holds: one admission per patient in SUPPORT). Dropping
the 138 patients dead on day 3 is right: there is no decision for a patient already dead (USE-3), and their values are
values at death (the earlier REVIEW issue 3 settled, in my view). Random split stands for new patients of the same hospitals;
I would deploy to the next year's patients. Phase I -> phase II (later patients, same five hospitals, Knaus's own
validation) scores ROC AUC 0.818, log loss 0.481, mean prediction 0.345 vs observed 0.327, the same as random CV
(0.817). So the IID split is not optimistic here, which supports the earlier REVIEW issue 6 (no grouping by block). A
new-site test would be a different use case (USE-10).

Wording: "On the third day in hospital" is not the prediction point. It is study day 3; patients entered the study on
hospital day `hday` (median 1, 34% later, max 148). Write "on the third day after entering the study" in `use_case`.

**4. Would I use it**

As a benchmark of the day-3 prognosis task, yes. As a tool at the bedside today, no: care of 1989-1994 (record marker
`Outdated`), five academic centres, SUPPORT's entry criteria select the cohort (I would need to apply the same criteria
to know the model applies). I would trust it because it is calibrated and matches physicians' discrimination; I would
distrust it without my own estimate and DNR status in it, and without treatment intensity.

**Gaps ranked by how much they change the task**

1. prg2m dropped though known on day 3 (USE-6 vs USE-9): +0.022 AUC; changes the task from "help the physician" to
   "objective estimate without the physician". Keep the choice but state it correctly in `changes`/`curation_comments`.
2. Horizon 2 vs 6 months (USE-5): the hospice decision uses 6 months; 2 months is a valid, documented alternative.
3. DNR by day 3 dropped (USE-6): +0.008 AUC; also a population question (already had the conversation).
4. `use_case` says "third day in hospital"; the point is study day 3 (USE-3 wording).
5. BUN/glucose/urine not available (structural), aps dropped (+0.002): negligible.

**What a domain expert would change**

- Say in `curation_comments` that prg2m is known on day 3 and dropped to keep the task an objective prognosis, with the
  measured cost; fix `changes` wording ("physician estimates ... made from or after these values" is inaccurate).
- Consider a DNR-by-day-3 flag, or say why care decisions are excluded.
- Fix the prediction-point wording to study day 3.
- Mention 6-month death as the hospice-eligibility alternative target.
- Prefer log loss (calibration) over ROC AUC for a prognosis communicated as a probability (outside this dataset's
  scope if the collection fixes the metric).

**Sources**

- Knaus et al. 1995, Ann Intern Med 122(3):191-203, abstract via PubMed E-utilities (PMID 7810938):
  https://pubmed.ncbi.nlm.nih.gov/7810938/
- hbiostat supportdesc: https://hbiostat.org/data/repo/supportdesc ("You also will probably not want to use prg2m,
  prg6m, dnr, dnrday"; "To develop models without using findings from previous models, be sure not to use aps, sps,
  surv2m, surv6m")
- Medicare hospice eligibility (terminal illness, prognosis of 6 months or less): 42 CFR 418.22 (domain knowledge)
- Repository: dataset.py, README.md, curation record, the earlier REVIEW.md, the task probe

</details>

<details><summary>Blind review</summary>

**Review: 2_month_survival_rate_prediction (SUPPORT2, target death_within_2_months)**

**Verdict**
Include with changes: this is a real, well-known clinical prognosis task (SUPPORT) with honest features and moderate signal. The changes are to document how the target was built and why rows were dropped, and to make a decision about `adlp`. Its missingness partly encodes early death.

**Task**
SUPPORT was built for this purpose: it estimates short- and medium-term survival of seriously ill hospitalised adults, mostly from day-3 assessments, to support decisions on goals of care and prognosis. The source also ships the SUPPORT model's own 2-month estimate (`surv2m`) and the physician's estimate (`prg2m`). Those columns are correctly excluded here; the source says not to use them as predictors. This is a real use.

**Data facts**
- 8,967 rows x 25 features. Target: 2,993 Yes / 5,974 No (33.4%).
- No exact duplicate rows, with or without the target.
- LightGBM (3-fold CV) AUC is 0.814. The strongest single features are adlp (AUC 0.661), dzgroup (0.664) and scoma (0.646).
- Not trivial, and big enough to score.

**Concerns, most serious first**
1. **The missingness of `adlp` is partly downstream of the outcome.** `adlp` is the ADL index from the patient interview, taken around study day 3 or later. When it is missing, the 2-month death rate is 44.5%; when present, 15.7%. Coma does not explain this. Among patients with scoma = 0, the death rate is 35.4% when adlp is missing and 15.0% when present. Some patients could not be interviewed because they had died or deteriorated, so the missing flag carries some future information. The effect is small: dropping adlp lowers AUC from 0.814 to 0.804. Fix: drop `adlp`, or document that "interview not obtained" is treated as known at prediction time. (`adls`, the surrogate version, is already absent.)
2. **The target derivation and the 138 dropped rows are undocumented.** UCI lists 9,105 patients; the table has 8,967. The likely explanation is that survivors censored before day 60 were removed and the target is `death==1 & d.time<=60`. That would be correct, but I could not verify it. Fix: document the rule. Confirm that censored-before-60-day survivors were removed and not labelled "No".
3. **The split ignores structure.** The data come from 5 centres and 2 study phases (Phase I, 1989-91; Phase II, 1992-94). A random IID split is acceptable, but the site and phase columns are not in the table, so a temporal or site split is impossible. This is minor. Fix (optional): keep the phase or site if available and consider a phase-based split.
4. **Small preparation issues.**
   - Missing labs are left as NaN, which is fine. Do not apply the source's "normal value" imputation.
   - Some values are implausible but are true SUPPORT coding: meanbp = 0 (16 rows), hrt = 0 (30), resp = 0 (30), wblc = 0 (9). These are acceptable.
   - Max edu is 31, which is odd but comes from the source.
   - `income` categories are unordered strings. An ordinal encoding would be cleaner.
   - `dzclass` is a deterministic coarsening of `dzgroup`. It is redundant but harmless.
   - `hday` (study-entry day) is known at entry, which is fine.

**Leakage check**
Outcome-related source columns are excluded: hospdead, d.time, slos, sfdm2, charges/totcst, dnr/dnrday, surv2m/surv6m, prg2m/prg6m, aps/sps. No other leaking columns were seen.

**Could not check**
- The raw-to-prepared mapping. I did not download the raw SUPPORT2 file, so the exact target rule and the reason for the 138 dropped rows are unverified.
- The exact timing of the patient interview relative to early deaths.

</details>

<details><summary>Precedent check</summary>

**2_month_survival_rate_prediction: precedents and consistency (panel phase A, 2026-10-20)**

Checked against the knowledge files' Cases tables, the decision register
and sibling records under `curation/records/`. The register's four flags (few_minority, one_feature, scaling over all
rows, trivial) do not involve this dataset; its rows appear only in the `Outdated`, `post-outcome feature`, PROV-13,
PROV-15 and USE-8 groups. No drift: all of Lennart's CC lines here are of one day (2026-10-12), and the AI's cohort rule
(drop the day-3 deaths) is the same on 2026-10-07 (phase I, 69) and now (both phases, 138). No reason has yet produced
a third exception. One measurement of my own (support2.csv, the 8,967-patient cohort): `prg2m` alone ROC AUC 0.801,
`prg6m` 0.793, missing 17.6% with the same target rate missing or present (34.5% / 33.1%); DNR by day 3: 1,437
patients, 61.6% positive.

**Summary**

| # | Decision | Verdict | Rules | Closest precedents |
|---|---|---|---|---|
| 1 | Physicians' estimates `prg2m`, `prg6m` dropped | departs, stated reason not one the ranking accepts (a Must) | USE-6, LEAK-37 | breast_cancer_prediction (BI-RADS kept, 2026-10-15), brazilian_ecommerce (2026-10-15), bias_correction_r_bias_correction_r_2 |
| 2 | DNR: `dnr`, `dnrday` dropped; "DNR by day 3" flag not built (REVIEW issue 5) | `dnrday` and `dnr` as published: consistent; the day-3 flag: departs with a reason, open | LEAK-10, LEAK-7, USE-6 | heart_failure_followup_survival `time` (2026-09-30); garments `incentive` lag (LEAK-7); as in 1 |
| 3 | `adlp` kept, `adls`/`adlsc` dropped (CC 2026-10-12) | departs from the mic precedent with a stated reason that a new measurement weakens | LEAK-10, USE-8 | mic (CC 2026-09-30); kick (USE-8 approximate) |
| 4 | `year = "2000"` | departs without a reason | PROV-9 | airfoil_self_noise, first_principles_tully_fisher, nikuradse (2026-10-20) |
| 5 | Implausible `alb`, `wblc` = 0 (and `pafi`, `edu`) kept without a note | departs without a reason (Should) | CLEAN-11 | heart_disease_va_long_beach, thyroid_discordant (2026-10-19), caracas_cervical_cancer (2026-10-15) |
| 6 | 138 day-3 deaths dropped (REVIEW issue 3) | consistent | LEAK-22, LEAK-36, USE-7, CLEAN-11 | diabetes_130_us; mic set apart by a fact |
| 7 | IID, no grouping by the ten file blocks, no phase split (REVIEW issue 6) | consistent | SPLIT-1, SPLIT-14, SPLIT-19, SPLIT-30, factor "only a few groups" | covertype (2026-10-01), account_debt_south_africa (2026-10-12), breast_cancer_prediction (2026-10-15) |
| 8 | One target, death within 60 days (CC 2026-10-12) | consistent | USE-5, LEAK-23, CLEAN-18 | cirrhosis_patient_survival_prediction |
| 9 | Phase II physiology restored with ICPSR, only support2 values shipped (CC 2026-10-12) | consistent | PROV-13, PROV-15, EV-4 | SUPPORT2 row in provenance.md Cases (this dataset); ashrae (2026-10-15) |
| 10 | `sps`, `surv2m`, `surv6m`, `aps` dropped | consistent | LEAK-27, CLEAN-6, LEAK-13 | yeast; hepatitis_c_prediction |
| 11 | Outcomes and post-day-3 fields dropped | consistent | LEAK-10 | heart_failure_followup_survival (2026-09-30), anes_voting_2026 |
| 12 | Vital-sign zeros kept | consistent, reason stated | CLEAN-11 | heart_disease_va_long_beach (`chol` 0 is impossible, a different fact) |
| 13 | `Outdated` marker with suggestion Yes | consistent | selection.md marker table (no rule) | heart_disease_cleveland, heart_disease_hungary, heart_disease_va_long_beach, hepatitis_survival_prediction, horse_colic_survival, south_africa_coronary_heart_disease (all Yes with `Outdated`) |
| 14 | Fit `direct` | consistent, unless 3 is kept as a potential leak | USE-8 | the USE-8 Cases row names this dataset as direct; kick (approximate for a potential leak kept on purpose) |

**The departures**

**1. `prg2m`, `prg6m` dropped (USE-6, Must; LEAK-37, Must)**

Facts: Knaus et al. 1995 (abstract, as quoted in the 2026-10-07 run report): "Physicians were interviewed on day 3",
so the estimates exist at the prediction point. Their missingness does not track the target (34.5% vs 33.1%).
`prg2m` alone scores ROC AUC 0.801, about the full model (0.805, leak probe). The definition's reason: "Dropped as the
source advises (supportdesc)".

Rule: USE-6 (Must): "A company's own estimate made before the outcome is an input, and the model refines it ...
dropping it changes the task into 'predict without the company's estimate'". LEAK-37 applies it.

Precedents: breast_cancer_prediction kept the radiologist's BI-RADS assessment as an input although it alone gives AUC
0.907 (CC 2026-10-15, Lennart: "the real-world use decides"); brazilian_ecommerce kept Olist's promised date
(2026-10-15); bias_correction kept the LDAPS forecast. No record drops a human estimate known at the prediction point.

Reading: a source's advice is a claim to check (as SPLIT-5 says of a source's split), not a fact under the ranking.
USE-6 is a Must, so this cannot be an exception; it holds only if the use case itself excludes the physician (P3
decides the inputs), and the current `task_summary.use_case` ("the care team estimates a patient's chance") does not
say so: there the physician's estimate exists when the model is used.

**Consistency check (AI, 2026-10-20):** your call on 2_month_survival_rate_prediction (drop the physicians' day-3
estimates `prg2m`, `prg6m`, a departure from USE-6) differs from breast_cancer_prediction (the radiologist's BI-RADS
assessment kept, 2026-10-15, the same mechanism: a clinician's judgment recorded before the outcome, dominant alone).
What sets this case apart?
(a) the use case is the source's: an objective second estimate set beside the physician's (Knaus 1995, "Objective
estimates of survival"; physicians were interviewed on day 3 as the comparator), and the physician's estimate is a
forecast of the same outcome (alone 0.801), so with it the task becomes "refine the physician"; write that into
`task_summary.use_case`, recorded as the reason; (b) treat it like breast_cancer_prediction and keep `prg2m` and
`prg6m`; (c) reopen breast_cancer_prediction to match; (d) change USE-6 (an amendment: a human forecast of the target
itself is out when the use case is an independent estimate).

**2. DNR by day 3 (REVIEW issue 5; LEAK-10, LEAK-7, USE-6)**

`dnrday` equals `slos` for every patient without an order, and most orders after entry come after day 3: dropping
both columns as published follows LEAK-10 (heart_failure_followup_survival `time`, 2026-09-30). The open part is the
LEAK-7 fix ("the smallest fix that keeps a valid signal beats dropping the column", garments `incentive` lagged): a
flag "DNR order by day 3" is known at the prediction point (1,437 patients, 61.6% die within 2 months; ROC AUC 0.814 to
0.822 per REVIEW). The stated reason, "a care decision that carries the physician's prognosis", is the same reasoning
as decision 1, and USE-6 and breast_cancer_prediction point the other way. Decide 1 and 2 together.

**Consistency check (AI, 2026-10-20):** your call on 2_month_survival_rate_prediction (no "DNR by day 3" flag, a
departure from LEAK-7 and USE-6) differs from garments_worker_productivity (`incentive` lagged to the value known at
prediction time rather than dropped) and from breast_cancer_prediction (a clinician's judgment kept, 2026-10-15). What
sets it apart?
(a) a DNR order changes the care (no resuscitation), so it partly causes the death it would predict, and it carries
the physician's prognosis that decision 1 keeps out; recorded as the reason, together with 1(a); (b) build the flag
from `dnr` and `dnrday` <= 3, as LEAK-7 suggests; (c) reopen garments to match; (d) change LEAK-7 or USE-6.

**3. `adlp` kept while `adls` and `adlsc` go (CC 2026-10-12; LEAK-10 Must, "missingness that encodes the outcome")**

The CC's reason: the surrogate's gaps "depend on whether the stay lasted until the interview, which is after the
prediction point"; `adlp` is "missing mostly when the patient cannot answer". The table behind the CC (Decision 5)
lumps deaths with discharges ("stay ended by day 7": `adlp` 53.4% missing, longer stays 65.1%). Split apart (panel
prep run): 95.4% of the 767 patients who died by day 7 lack `adlp`, against 37.8% of those
discharged alive by day 7. So the CC's own mechanism (the interview did not happen because of an event after day 3)
also reaches `adlp`, through death rather than discharge. For it: among the 6,139 patients still in hospital after
day 7 the indicator still scores 0.617 (0.613 with `scoma` = 0), and `adlp` is missing for 90.7% of comatose patients,
a day-3 state. Dropping `adlp` costs 0.009 ROC AUC.

Precedent: mic (CC 2026-09-30, Lennart): day-1..3 ICU fields blank for patients who died earlier (91% of the rows
missing a day-3 field died, base rate 16%): dropped, the prediction point moved (leak_checks.md Mechanisms table,
"Missingness that encodes the outcome"). This is a new measurement against a CC, not a re-argument: the CC stands
unless the curator reopens it.

**Consistency check (AI, 2026-10-20):** your call on 2_month_survival_rate_prediction (keep `adlp`, CC 2026-10-12)
differs from mic (day-1..3 fields dropped, 2026-09-30, the same mechanism: a gap left by a death after the prediction
point; 95.4% of the deaths by day 7 lack `adlp`) and from your own call on `adls`. What sets `adlp` apart?
(a) its gap is mostly the patient's state at day 2-3 (coma: 90.7% missing) and survives among patients in hospital
past the interview window (0.617), so it is not mainly caused by death; recorded as a `Potential leak, kept on
purpose:` note with these numbers, and the fit then approximate as for kick (USE-8); (b) treat it like mic and `adls`:
drop `adlp`; (c) reopen `adls` to match; (d) change LEAK-10 (an amendment for partly outcome-driven missingness).

**4. `year = "2000"` (PROV-9, Must)**

No evidence: the zip's file is dated 2003-06-23, the first archived copy is 2007-07-06, ICPSR's first version is
January 2001, Knaus 1995 holds no rows (panel checklist, P5). PROV-9's cases (airfoil_self_noise, tully_fisher,
nikuradse, all Lennart 2026-10-20) take the year of the first publication that holds the rows. The value looks
imported (lowest in "Who decides").

**Consistency check (AI, 2026-10-20):** the year of 2_month_survival_rate_prediction (2000) has no source, unlike the
PROV-9 cases of 2026-10-20 (airfoil_self_noise, first_principles_tully_fisher, nikuradse). What sets it apart?
(a) nothing: set the earliest dated evidence of Vanderbilt's extract, 2003 (the file's date in the zip), with that
reason in the record; (b) take ICPSR's first release (2001) if you count ICPSR as the first publication (then PROV-8
also moves the source); (c) keep 2000 with the evidence for it written down; (d) change PROV-9 for undated releases.

**5. Implausible values kept without a note (CLEAN-11, Should)**

`alb` 6.3, 8.6, 10.9 and 29.0 g/dL (likely g/L), `wblc` = 0 in 9 rows (3 die within 2 months, so not the arrest
pattern of the vital zeros), `pafi` above 600 in 29 rows, `edu` 26-31 years in 8 rows (panel value ranges).
CLEAN-11 Cases set impossible values missing: heart_disease_va_long_beach `chol == 0`, thyroid_discordant `age = 455`
(2026-10-19), caracas_cervical_cancer (2026-10-15). The definition notes and keeps only the vital zeros. A P7 Should, a
handful of rows; the restoration's asserts are unaffected if the step comes after `_restored`.

**Consistency check (AI, 2026-10-20):** 2_month_survival_rate_prediction keeps `alb` 29 g/dL and `wblc` 0 without a
note, while heart_disease_va_long_beach (`chol` 0) and thyroid_discordant (`age` 455) made such values missing. What
sets it apart?
(a) nothing for `alb` above 6 and `wblc` 0: make them missing (or `alb` / 10 as a unit repair, PROV-13 first), and
keep `pafi` and `edu` as unusual but possible, with a note; (b) treat all as the precedents: missing; (c) keep all, a
noted exception (the study's values are as recorded); (d) change CLEAN-11.

**Consistent decisions, with the precedent**

6. **Day-3 deaths dropped** (REVIEW issue 3). Dead at the prediction point, so no task row (USE-7, CLEAN-11 "a row
   leaves only when it is no task row"); a cohort question, not a feature leak (LEAK-36, LEAK-22: diabetes_130_us
   removed encounters ending in death). mic chose the other remedy (an earlier prediction point) because its file has
   no day of death; SUPPORT has `d.time`, and the SUPPORT model's own prediction point is day 3. Keeping them (0.822)
   would put values at death into the features (LEAK-10). Same rule on 2026-10-07 and now.
7. **IID, no blocks, no phase split** (REVIEW issue 6). The use case is new patients of the same hospitals, so the
   probable hospital blocks are a feature-like context, not entities new data lacks (SPLIT-4, SPLIT-30); five groups
   would be a shift test (factor "only a few groups": covertype, 3 areas, IID, 2026-10-01). Knaus validated phase I on
   phase II (SPLIT-19, Should), but two phases cannot give three windows (SPLIT-14, Must), so the Should yields to the
   Must, as written. The cost of the time axis is measured (phase I to phase II 0.812, about the IID score), which is
   what SPLIT-8 asks of account_debt_south_africa (2026-10-12); clinical cohorts ship IID (breast_cancer_prediction,
   2026-10-15). No departure.
8. **One target, 60 days** (CC 2026-10-12). A fixed horizon with every survivor followed at least 344 days (LEAK-23,
   cirrhosis_patient_survival_prediction); one target, no `Multi-target` tag (CLEAN-18). Knaus's primary horizon is
   180 days; the CC chooses the record's named horizon, with a reason.
9. **ICPSR only places rows** (CC 2026-10-12). The provenance.md Cases row "SUPPORT2 (PROV-13, PROV-15): restored from
   the study data (ICPSR 2957)" is this dataset; the ICPSR terms are noted, not weighed (EV-4, selection.md "Ethics,
   licence").
10. **Model outputs dropped.** `sps`, `surv2m`, `surv6m` are a model fit on phase I survival, i.e. on our labelled
    rows (LEAK-27, CLEAN-6; yeast); dropping is possible because the inputs exist. `aps` is a fixed published scale,
    but computed with imputed BUN and urine in phase I and measured ones in phase II: a recording that differs by
    phase, removed like the three labs (LEAK-13, hepatitis_c_prediction), so CLEAN-22 is met ("leave for what they
    are").
11. **Outcomes and post-day-3 fields dropped** (LEAK-10): heart_failure_followup_survival `time` (2026-09-30).
12. **Vital zeros kept**: CLEAN-11 "values that are only unusual stay", with the stated fact (25 of 30 heart-rate-0
    patients die within 2 months: arrests). `chol == 0` in heart_disease_va_long_beach is impossible, a different fact.
13. **`Outdated` with Yes**: six clinical records of the same era carry `Outdated` and ship (`heart_disease_*`,
    hepatitis_survival_prediction, horse_colic_survival, south_africa_coronary_heart_disease). `Outdated` has no rule
    behind it (selection.md marker table: "none"). The open consistency check on first_order_theorem_proving
    (2026-10-19, `No` on `Outdated` alone) is the outlier, not this record.
14. **Fit `direct`**: the USE-8 Cases row lists this dataset as direct; that stays true unless decision 3 ends as a
    potential leak kept on purpose, which made kick approximate.

**Not checked**

The ArtifactData review database of the 2026-10-07 run (no access here); Knaus 1995 and supportdesc text on the
physicians' estimates (the panel's fetch of the DOI returned 403).

</details>

<details><summary>Advocate</summary>

**Advocate, opening brief: 2_month_survival_rate_prediction (panel phase B, 2026-10-20)**

Position: ship, after definition edits. No finding of phase A reaches exclusion; every real problem has a fix lower
on the remedy ladder (principles.md, "How to decide" 5). One problem I concede outright (point 4).

**1. The task is real, and the target and cohort are right (P3, P4: USE-1, USE-3, USE-5, USE-7, LEAK-22; Must)**

Evidence: the source exists for this task (Knaus 1995, a day-3 prognosis for seriously ill adults); the practitioner
rates the fit direct, the blind reviewer says "a real, well-known clinical prognosis task ... Include with changes".
Target = death with d.time < 60, the source's own sfdm2 cut-off (claim audit, codebook p. 384, 388), uncensored: every
survivor followed >= 344 days (LEAK-23). Every kept feature except adlp's gaps is recorded at entry or on study day 3
(claim audit, column audit, codebook). The 138 day-3 deaths are no task row (USE-7) and carry values at death (hrt 0 in
38.4% vs <= 7.1% later); precedents rate the drop consistent (diabetes_130_us). Keeping them (0.822) would add a leak.
Answers: the blind reviewer's "target and dropped rows undocumented" was written without the raw file; the claim audit
verified both.

**2. The data is repaired from its origin, better than any public copy (P5: PROV-13, PROV-15; Must)**

Evidence: in support2 as published, most phase II physiology sits in other patients' rows; a phase I model scores
0.696 on phase II as published and 0.821 restored (claim audit reproduced: 0.821 / 0.696). Link 9,105 rows 1:1 to
ICPSR PSEUDOIDs; UCI 880 is the same table (19 prg6m cells differ). Only support2's values ship (CC 2026-10-12).
Repair is the top rung of the ladder and outranks everything at P6 and P7. Retiring this dataset would leave the
benchmark only the damaged public copies.

**3. The split is honest: IID gives no optimism (P4: SPLIT-1, SPLIT-4, USE-10; precedent)**

Evidence (split audit, claim audit): IID 0.818; temporal over phase II with 60-day gap 0.824; phase I -> II 0.820
(Knaus's own design); leave-one-hospital-pair-out 0.815 (0.793-0.831). No hidden entities (one row per patient, 0
copies). Every clinical cohort in the copy ships IID (cirrhosis, diabetes_130_us, framingham, breast_cancer_prediction).
Concede: bullet 3's reason ("two phases cannot give three windows") is false; the entry date is recoverable. Fix:
rewrite the note with the measurement (writing.md, SPLIT-5). The regime stays; SPLIT-4 says the gap never decides,
and here there is none.

**4. adlp: conceded, drop it; the dataset stays (P4: LEAK-10, LEAK-6; Must)**

Evidence: codebook status D3P = 10 "Pt Death" marks 475 patients, all positive, all lacking adlp (proof, EV-6).
Effect 0.0035 AUC of adlp's 0.008. LEAK-6: "a confirmed leak goes even when small", so a `Potential leak, kept on
purpose:` note (LEAK-38 is for anonymised competition fields, not this) is not available. No smaller fix keeps the
signal: separating the death gaps needs D3P, which CC 1 bars as a feature source. Mildest remedy: drop adlp (cost
0.008 AUC; the task keeps 24 features and AUC ~0.81). Tension row "a real task against a leak": fix the leak, keep the
task. The CC 2026-10-12 is the curator's, so this goes to Lennart as a new fact against it, with the drop as the
recommendation. edu/income: no measurable effect (drop +0.0001, impute -0.0001, SE 0.0002-0.0005) and no death code
in DEMOG: under LEAK-6 "measure before acting", keep with a note, or drop at zero cost; either keeps the dataset.

**5. prg2m/prg6m and DNR: a use-case choice, fixable in text (P3 decides P4's inputs; USE-6/LEAK-37 Must, USE-9)**

Concede: the stated reason ("as the source advises", "made from or after these values") is not one the ranking
accepts, and USE-6 is a Must. But USE-6 applies to inputs of the actor in the use case, and P3 sets the actor. The
source's use case is an objective estimate set beside the physician's (Knaus 1995, "Objective estimates of survival";
physicians interviewed as the comparator; model 0.812 vs physician 0.801); the practitioner adds that no numeric
estimate is written in the chart in routine care. That is the source's own use, not a rephrasing to excuse a gap, so
the USE-9 counter-factor does not bite. Fix: write the objective-estimate actor into `use_case` and correct `changes`
(precedents option 1a). breast_cancer_prediction differs by a fact: there the radiologist's reading is the input the
deployed model consumes; here the study design measured the physician as the competitor. If the curator prefers 1b
(add prg2m, +0.022 AUC), the dataset still ships. DNR by day 3: a care decision that partly causes the death it would
predict (no resuscitation); decide with prg2m; either answer ships.

**6. The remaining findings are wording, metadata and four cells (P3 wording, P5 PROV-9, P7 CLEAN-11)**

* use_case "third day in hospital" -> "third day after study entry" (24.6% entered after hospital day 3). One line.
* year "2000" has no evidence (PROV-9, Must): set 2001 (ICPSR first release) or 2003 (zip date) with the reason. A
  field edit, independent of validity of the data (independent failures are fixed, not traded).
* alb > 6 g/dL (4 rows): missing, per CLEAN-11 cases. wblc 0 (9 rows): dispute the precedents' call; 8 of 9 are
  MOSF w/Malig, neutropenia is plausible, so "only unusual" stays (CLEAN-11). pafi > 650 (29 rows): a curator cut or a
  note. P7 Should: cheap fixes, the tension row "a real task against imperfect cleaning" keeps the task.
* "up to 90 rows", "almost only among them", "mostly written near death": reword (writing.md, EV-7); no decision rests
  on them.

**7. Worth benchmarking (P6: TP rules)**

Task probe: 8,967 rows, 997+ minority rows per test fold, best family AUC 0.806 vs linear 0.785 (spread +0.042, SE
0.005), single feature 0.646, flags none. `Outdated` ships in six clinical records of the same era (precedents 13);
no rule stands behind the marker.

**Judgment record (advocate)**

Verdict: ship after changes.
Validity: USE-1/3/5/7 hold (direct fit); LEAK-10 triggered for adlp, fixed (drop); PROV-13 holds (repaired); SPLIT-1
holds (note rewritten); USE-6 for prg2m/prg6m: use case rewritten as the source's objective estimate, or add them;
PROV-9 fixed (2001 or 2003).
Value: TP holds, no flags.
Quality: CLEAN-11 alb > 6 to missing; pafi and wblc 0 noted.
For the curator: adlp (new fact against CC 2026-10-12); prg2m/prg6m and DNR flag (one call); year.

**Advocate, rebuttal: 2_month_survival_rate_prediction (panel phase B, 2026-10-20)**

Both briefs reach "ship after changes" and neither argues exclusion. The disagreements are small. No new facts.

1. **prg2m/prg6m and DNR (USE-6, LEAK-37).** Conceded: as `use_case` reads now, dropping them breaks USE-6, and the
   `changes` wording is wrong. Both briefs name the same mildest remedy, with keeping them as the fallback. One
   difference in emphasis: I recommend option (a), the objective-estimate actor. It is the source's own design (Knaus
   1995 measured the physician as the comparator: model 0.812, physician 0.801), so the USE-9 counter-factor ("a use
   case rephrased only to excuse a gap") does not apply. breast_cancer_prediction differs on that fact. The choice
   is the curator's, and either answer ships.
2. **Prediction point wording (USE-3).** Conceded; this is my point 6.
3. **adlp (LEAK-10, LEAK-6).** Agreed: drop it. It is a new fact against the CC of 2026-10-12, and the curator reopens it.
4. **edu/income.** Conceded. Keep them with a `Potential leak, kept on purpose:` note (drop +0.0001, impute -0.0001,
   SE 0.0002-0.0005; no death code in DEMOG), and correct Decision 5's "as often for short as for long stays". Once
   adlp is dropped, the critic's consistency condition does not arise.
5. **Split note (SPLIT-5, SPLIT-7).** Conceded; this is my point 3. Rewrite the note with the measured scores; IID stays.
6. **year (PROV-9).** Conceded. Set 2001 or 2003 with the reason.
7. **Cleaning and wording (CLEAN-11, EV-7).** Conceded for alb > 6 and the three sentences. One addition that is not a
   dispute: the critic rightly leaves wblc = 0 (9 rows) out. 8 of the 9 are MOSF w/Malig (neutropenia), so the
   value is only unusual and stays under CLEAN-11. That differs from the precedents brief, which asked to make it
   missing.

Agreed record: ship after changes. Drop adlp. Rewrite use_case (study day 3, plus the objective estimate, or keep
prg2m/prg6m). Note on edu/income. Rewrite the split note. Fix the year. Set alb > 6 to missing. For the curator: adlp
and prg2m/DNR reopen the CCs of 2026-10-12.

</details>

<details><summary>Critic</summary>

**Critic: 2_month_survival_rate_prediction (panel phase B, opening brief, 2026-10-20)**

Position: ship only after changes. The task is real and the ICPSR repair is sound (claim audit: link, transfer 0.821
restored vs 0.696 as published, target and cohort all hold). Nothing here argues for exclusion. What I ask for: one
leak fixed, the use case made to match the inputs, two false or unsupported facts corrected, and small cleaning.

**1. The use case says the care team estimates the prognosis, yet the care team's own day-3 estimate is dropped (P3, USE-6 Must; LEAK-37 Must)**

- Problem: `prg2m`/`prg6m` are the physicians' estimates taken on study day 3 (Knaus 1995 abstract: "Physicians were
  interviewed on day 3"). They exist at the prediction point; their missingness does not track the target (34.5% vs
  33.1%, precedents.md). The only reason given is supportdesc's advice, and a source's advice is a claim to check, not
  a rule. The DNR-by-day-3 flag (1,437 patients) is the same question.
- Effect: as written (`use_case`: "the care team estimates a patient's chance"), the shipped task is "predict without
  the actor's estimate", which USE-6 names as a changed task. prg2m alone scores 0.801; adding it 0.817 -> 0.839
  (practitioner.md).
- Also wrong: `changes` groups the physician estimates with "scores ... made from or after these values"; prg2m is made
  on day 3, not from the values.
- Precedent: breast_cancer_prediction kept BI-RADS (2026-10-15); brazilian_ecommerce, bias_correction kept the
  actor's estimate. No record drops a human estimate known at the prediction point.
- Remedy (mildest): fix the definition text. Write into `task_summary.use_case` that this is the objective second
  estimate set beside the physician's (Knaus 1995's own design, "objective estimates"), so the physician's estimate and
  DNR status are out by the use case, and correct `changes`. Otherwise keep `prg2m`, `prg6m` (and a DNR-by-day-3 flag).
  Curator's choice, but one of the two must hold.

**2. The prediction point is misnamed (P3, USE-3 Must)**

- `use_case` says "On the third day in hospital"; the point is study day 3. 24.6% of patients entered the study after
  hospital day 3 (hday up to 148).
- Effect: a user reading the summary times the model wrongly for a quarter of the cohort.
- Remedy: reword to "on the third day after entering the study".

**3. adlp's gaps record deaths after the prediction point (P4, LEAK-10 Must; LEAK-6 Must)**

- Evidence (proof, EV-6: the codebook's own code): adlp is present iff ICPSR `D3P` = 1. 475 cohort patients have
  `D3P` = 10 "Pt Death": all 475 positive, 98.3% dead by day 7, median day 5, every one without adlp; 505 more lack it
  as "Pt Discharged" (98.4% stay <= 7 days). 95.4% of the 767 deaths on days 4-7 lack adlp vs 58.2% of others.
  (claim_audit.md row 1; column_audit.md problem 1.)
- Effect: small, measured: 0.0035 AUC of adlp's 0.008 (SE 0.0006). But it is the exact mechanism the CC of 2026-10-12
  used to drop adls, and the Decision 5 table hid it by pooling deaths with discharges. The record's "no known risk"
  is refuted.
- Rule: LEAK-10 lists "missingness that encodes the outcome"; LEAK-6: "a confirmed leak goes even when small". A
  `Potential leak, kept on purpose` note is for a weak or suspected leak, not a confirmed one (principles: "A very real
  task carries cleaning imperfections ... it does not carry a leak"). Precedent: mic, same mechanism, fixed.
- Remedy: drop `adlp` (cost 0.008 AUC). A finer fix (blank only the D3P-10 rows) would need ICPSR values in the data,
  against CC 1. This is a new fact against the CC, so the curator reopens it; I do not override it.

**4. edu and income: the stated reason for keeping them is wrong on the case that matters (P4, LEAK-10, weak)**

- Decision 5 says they are "missing as often for short as for long stays". True by slos, false by early death: edu
  missing 31.4% among deaths on days 4-7 vs 16.3%, income 43.0% vs 31.5% (column_audit.md problem 2).
- Effect: none measurable (drop both +0.0001 AUC). Mechanism plausible, not proved per row.
- Remedy: keep, with a `Potential leak, kept on purpose:` note giving these numbers, and correct Decision 5's
  wording. (Dropping costs nothing; either is fine. Consistency with point 3 if adlp is kept with a note: then these
  must carry the same note.)

**5. The split note states a false fact (P4, SPLIT-5 Must, SPLIT-7 Must; SPLIT-19 Should)**

- `curation_comments` bullet 3: "Two phases cannot give the protocol's three time windows". False: survivors' entry
  date = 1994-12-31 minus d.time, row order equals entry order within every block (Spearman 1.000), decedents
  interpolate to a median 0.7 days; three ~8-month windows over phase II are possible (split_audit.md problem 1).
  The source's own validation is temporal (phase I -> II).
- Effect on the score: none (temporal 0.824, phase I -> II 0.820, IID 0.818; leave-hospital-pair-out 0.815). So IID
  does not inflate the benchmark.
- Remedy: fix the note, not the split: state that the time axis is recoverable, that the temporal split scores the
  same, and that IID is kept because the use case is new patients of the same hospitals and years (precedent: the
  copy's clinical cohorts). Replace "not documented" for the blocks with the measured leave-pair-out score.

**6. year = "2000" has no evidence (P5, PROV-9 Must)**

- No source dates the first publication of the rows to 2000. Earliest evidence: the zip's file dated 2003-06-23;
  ICPSR's first version January 2001; earliest archive 2007 (precedents.md 4; claim_audit row 10).
- Remedy: set the earliest evidenced year (2003 for hbiostat's extract, or 2001 if ICPSR counts as first publication)
  with the reason in the record. Precedents: airfoil_self_noise, tully_fisher, nikuradse (2026-10-20).

**7. Quality only (P7, CLEAN-11 Should; writing, EV-7): not a reason to hold the dataset**

- `alb` 6.3, 8.6, 10.9, 29.0 g/dL are impossible (29.0 reads as g/L): set alb > 6 missing after `_restored` (4 rows).
  `pafi` > 650 (of 29 values > 600): set missing or note.
- Three inexact sentences: "up to 90 rows further down" (181 rows lie further, 90 above, claim_audit row 30);
  Decision 6 "almost only among them" (64%/69% of the zeros, the rates differ); "DNR orders after study entry are
  mostly written near death" (32.8% within 2 days, median 6 days) presented as supportdesc's reason, which supportdesc
  does not give. Reword; the drops stay.

**Judgment record**

Verdict: ship after changes.
Validity: USE-6 triggered (estimate known at day 3 dropped; fix the use case or keep it); USE-3 wording; LEAK-10
triggered for adlp (fix: drop); LEAK-10 weak for edu/income (note); SPLIT-5/SPLIT-7 false note (fix text, IID stays);
PROV-9 unsupported year (fix).
Value: holds (ROC AUC ~0.82, not trivial).
Quality: CLEAN-11 alb, pafi (cheap fix); EV-7 wording.
For the curator: points 1 and 3 reopen CCs of 2026-10-12 with new facts.

**Critic, rebuttal: 2_month_survival_rate_prediction (panel phase B, 2026-10-20)**

We agree on the verdict (ship after changes) and on most remedies. Point by point:

1. Task, target, cohort (USE-1/3/5/7, LEAK-22): concede. The claim audit verified the target rule and the 138-row cut.
   The blind reviewer's doubts were written without the raw file.

2. Repair from ICPSR (PROV-13, PROV-15): concede. The 0.696 -> 0.821 transfer was reproduced, and I never disputed it.

3. Split: concede the regime (IID). Measured: temporal 0.824 and leave-pair-out 0.815 against IID 0.818. We agree that
   the false note in bullet 3 must be rewritten with these numbers (SPLIT-5, SPLIT-7). This is a required change,
   not optional.

4. adlp: agreed, drop it (LEAK-10, LEAK-6). edu/income: agreed, a note or a drop. One condition from my point 4: the
   wording of Decision 5 ("missing as often for short as for long stays") has to change, because it is false by early
   death (31.4% vs 16.3%).

5. prg2m/prg6m and DNR: partly disputed.
   - Concede: option 1a (write the source's objective-estimate actor into `use_case`) is a valid fix. P3 sets the
     actor, so it outranks the USE-6 consequence. Knaus 1995's title ("Objective estimates") is primary-source support.
   - Dispute the distinction from breast_cancer_prediction. "No numeric estimate is written in the chart in routine
     care" is the practitioner's domain knowledge, without a source. Under EV-2 it ranks below a measurement or a
     primary document, so it cannot carry the distinction. The fact that does carry it is the source's design: the
     physician was measured as the comparator. The `use_case` text must say this. Today it says the opposite ("the care
     team estimates"), so shipping unchanged breaks USE-6 (Must).
   - DNR "partly causes the death it would predict": inference, unmeasured. Acceptable as the stated reason only
     inside the 1a framing, where all care-team judgments are out by the use case. Decide it in one call with prg2m,
     as we both say.

6. Wording, year, cells: concede all, with one note.
   - wblc 0: concede. I did not raise it, and the column audit finds it plausible (8 of 9 MOSF w/Malig).
   - year: the fix is required (PROV-9 Must), not a preference.

7. Value (TP): concede.

What remains in dispute is narrow. Point 5 needs a changed `use_case` grounded in the source's design, not in
practitioner inference. Every other change is agreed.

</details>

