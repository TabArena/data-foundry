# acs_food_stamps_2014_2024

**Outcome:** added as `acs_food_stamps_2014_2024_1m`; recommended not to ship as built: rebuild it for the Census
Bureau's filling of blank SNAP answers if you narrow the rule on labels a respondent already knows, otherwise `No`
(`No Good Target / Scientific Discovery`). The task follows TableShift's Food Stamps task on the ACS 1-year PUMS of
2014-2019 and 2021-2024: did a US household receive SNAP in the past 12 months, as it reports in the interview? One
row per occupied household (12.46 million with a reported answer; 10.6% Yes in the shipped frame), 43 inputs from the
same interview, three yearly test windows (2022, 2023, 2024) of 500k households each, each trained on a random 1M
households of the earlier years; fallback `roc_auc`. The definition keeps the outreach framing it was built with until
you decide: a rebuild for the imputer needs a re-read of ten years of person files and a focused panel, all lost under
`No`, and adds no evidence the decision needs. The panel's text fixes are made.
Verdict: don't ship as built (A, the outreach framing); ship after changes as B (the Census Bureau's imputation,
rebuilt) only with the amendment; otherwise `No` (C).
Validity: SEL-7 triggered and USE-5 fails for the outreach actor (Must): the agency holds the label for its caseload,
and its targets sit in "No" (48,305 "No" households at or below 130% of poverty against 50,819 "Yes" in all, 2024
window); no change to the definition fixes it under A. Under B both hold through the amendment; USE-6 (Must) then
needs PAP, SSIP and HINS4 added, and SPLIT-1 (Must) needs folds within the survey year. LEAK-10 not triggered on any
of the 43 inputs (income and the poverty ratio exclude SNAP; the income hot-deck carries no FS; public coverage is not
assigned from FS); 0 exact copies across the split. PROV-6 holds (food_stamps stays the Duplicate). SEL-1 is a
tension, not an exclusion: under B the grounds stay (7 CFR 272.6 binds state agencies, not the Census Bureau).
Value: no task-probe flag; LightGBM 0.914 against linear 0.897 and the best single feature 0.814 (the poverty ratio);
at least 20,279 rows of the smallest class per test fold. Metric: the roc_auc fallback as built; under B, log_loss or
roc_auc (issue 2).
Quality: CLEAN-21 (nominal dollars) under B (issue 3); weeks worked harmonised in the B pass.
Weighed (B): + a recurring, documented decision that exists apart from this dataset, whose label, inputs and row are
exactly the imputer's, each fill flagged; - hot-deck today, on 1.7-3.1% of households a year; the benchmark scores
respondents while the imputer fills non-respondents; the amendment opens five other survey records; the first keep
under SEL-7.
For the curator: issue 1 (B by amendment, or C) is the decision; issues 2 and 3 apply only under B.

**Main points:** Rebuild for the Census Bureau's filling of blank SNAP answers under a narrow amendment of the rule on
self-reported labels, or set the dataset to `No` (issue 1; the outreach framing as built cannot ship). Only under the
rebuild: the metric (issue 2: `roc_auc` implemented, `log_loss` recommended, lightly) and the dollars (issue 3: each year's
dollars as built with a rule amendment, recommended, or 2024 dollars).

**Record judgment:** the source is valid (the Census Bureau's PUMS as published); whether the task is valid is issue
1. The record's fields agree with the definition (binary, temporal, GOV Website, social science); its `name` said
"1-year files 2019-2024" and now says 2014-2019 and 2021-2024, as built. The verdict stays `Yes` until you decide
issue 1.

**Issues for Lennart:**

1. **Rebuild the dataset for the Census Bureau's filling of blank SNAP answers, under a narrow amendment of the rule on labels a respondent already knows (B), or set it to `No` (C)?**

   * **Problem:**
     - The household reports its own SNAP receipt in the interview that gives all 43 inputs, a label our rules treat as predicted by nobody (the diabetes and stroke surveys went to `No` on it), and the actor the definition names, a state SNAP agency targeting outreach, already holds that label for every household in its caseload[^sel7][^use5].
     - The agency's targets, eligible households that do not receive SNAP, sit in the "No" class, so a better model of this label ranks current recipients higher, the opposite of the outreach decision.
     - The one actor who predicts exactly this label from these inputs is the Census Bureau, which fills a blank SNAP answer from the rest of the interview for 1.7-3.1% of the households a year and flags each fill, but a rule that must hold allows no one-off exception, so this reading enters only if you narrow the rule itself[^exc][^cc].
   * **Background:**
     - The amendment would admit a self-reported label only when the survey's own office fills it for non-respondents from the same interview and flags each fill in the release; the task is then that office's, and its use case, inputs, split and metric follow the office[^amend].
     - It would open five other survey records: acs_household_broadband, folktables_acs_income, ntia_internet_use_survey_home_adoption, nsduh_past_year_drug_use and nsduh_mental_health_treatment (the precedent checker's reading, not checked record by record); it keeps cdc_diabetes_health_indicators and stroke_prediction out, whose labels are not allocated.
     - Reading the imputer in without changing the rule's text, through our rule that the use case decides whether an exclusion applies, would let every survey item someone could impute argue its way in; the amendment records the reading as a narrow rule[^sel2][^use9].
     - The imputer fills the report, not the truth, so the 35% of true recipient households that report No (Meyer, Mittag and Goerge, NBER WP 25143) are no label gap under B.
   * **Effect on the task:**
     - As built (A): in the 2024 window, 48,305 "No" households are at or below 130% of poverty (about SNAP's gross-income test), against 50,819 "Yes" households in all; 64% of the households at or below 130% report No.
     - Within the households at or below 200% of poverty, 82% of the top 10% of scores report Yes (2022-2024), and the score there is 0.848-0.850 against 0.907-0.910 on all households in the same run, so the headline score comes mostly from easy well-off negatives.
     - Under B the decision, the inputs, the label and the row are the imputer's, but the benchmark scores respondents while the imputer acts on non-respondents.
   * **Experiments:**
     - The items a SNAP application asks (the build's administrative-like set plus rent, owner costs, tenure, employment status, hours, workers in the family, disability, citizenship and vehicles) reach 0.9104 ROC AUC against 0.9152 with all 43 inputs and 0.8878 for the administrative-like set alone (2024 window, claim auditor): an agency could compute most of the score, but its targets are in "No".
     - Trained on the test year's other households (B's split): 0.9158 / 0.9142 / 0.9171 ROC AUC for the 2022 / 2023 / 2024 test years, against 0.9120 / 0.9109 / 0.9148 under the temporal split (split auditor, one seed).
     - Any member's public assistance, SSI or Medicaid, which B adds, gain 0.017 ROC AUC (0.9142 to 0.9312); the householder's own items 0.0065 (claim auditor).
     - The households whose answer the Bureau filled differ from the respondents: the Bureau's imputed Yes share on them is 12.3-14.7% a year, against 9.3-12.0% reported.
   * **Consistency:**
     - C follows cdc_diabetes_health_indicators (2026-10-15) and stroke_prediction (2026-10-26), both `No` on this rule, and dataorg_financial_health_prediction_challenge (2026-10-22, `No`, a FinScope survey answer).
     - A departs from them with no fact that sets it apart; B departs on a measured fact, a flagged allocation of this very label, which the diabetes and stroke items never had.
     - ai4d_lab_tanzania_tourism_classification_challenge (2026-11-05) shipped with the survey statistician filling a respondent's spending band, but beside a forward-looking trip planner, with the split unchanged, no data change and this rule never raised; here the imputer would be the only actor, and B the first keep under the rule.
   * **Panel:**
     - Agreed by both sides: A cannot ship; B ships only by the amendment, not as an exception; otherwise C.
     - For B (advocate, domain practitioner): a recurring, documented decision that exists apart from this dataset, its fill shares measured by the builder and again by the claim auditor; the Bureau is studying model-based against hot-deck allocation (an AAPOR 2026 talk, cited for its existence only).
     - For C (critic): the Bureau uses hot-deck today, on a small share; the scores fall on respondents while missing at random is assumed (Celhay, Meyer and Mittag, NBER WP 29184, find higher error among imputed cases); Tanzania is a weaker precedent than cited.
   * **Unknown:** whether the Census Bureau uses or plans a model-based allocation in production; a source showing it would strengthen B.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Outreach screening as built, cannot ship (implemented) | a state SNAP agency ranks next year's households; temporal split by survey year; the grounds kept with a note | no rebuild; TableShift's framing | fails two rules that must hold: the agency already holds the label, and its targets sit in "No"; no fact sets it apart from the diabetes and stroke exclusions; not shippable |
     | B | The Census Bureau's item allocation, by amendment | amend the rule narrowly (an item the survey office allocates and flags, naming the five records it opens); rebuild for the imputer: use case and fit, the other benefit items added, the grounds kept, the split within the survey year, weeks worked harmonised; a focused re-check | a real, recurring, documented decision; label, inputs and row are exactly the imputer's; each fill flagged; a large, drifting, clean task (0.914) | hot-deck today; 1.7-3.1% of households a year; respondents scored while the imputer fills non-respondents; opens five survey records; the first keep under the rule |
     | C | `No` with `No Good Target / Scientific Discovery` | the folder removed with a CHANGELOG entry; food_stamps' markers carry the same reason | follows the diabetes, stroke and FinScope exclusions; no amendment | loses a large, clean, drifting survey task; the allocation actor goes unused |

   * **Recommendation:** not A, which cannot ship. B if you read the Bureau's allocation of 1.7-3.1% of the households a year, by hot-deck today, as a decision the benchmark should mirror, in the narrow form above; otherwise C. The facts for and against B are agreed; what is left is that weighing, which the panel hands to you. **Decision:** B or C?

   **Notes for the AI:**
   - B: write the amendment into SEL-7 in `selection.md` (the wording in [^amend], dated, Lennart, on acs_food_stamps_2014_2024; name the five records it opens; Tanzania goes into the Cases row as the earlier, unflagged instance), and a CC line in the record. Then one finisher pass on `dataset.py`: `use_case`, `known` and `fit_reason` for the imputer, fit approximate naming three gaps (hot-deck today; respondents scored while the imputer acts on non-respondents, MAR assumed; a small share), TableShift kept as the task's origin only (USE-1, USE-8); PAP, SSIP and HINS4 added as any-member household flags (USE-6; a re-read of the ten person files); the protected grounds kept, with the reason (no law binds the imputer; the SEL-1 Tensions row); the split within the survey year (SPLIT-1, a Must, no exception): test = random households of year Y, train = the other households of Y only (the hot-deck's donors are that year's respondents; the form the split auditor measured), Y = 2024, 2023, 2022 (plain IID over all years would also train on later years' files; the task gamer measured that future part at about +0.0005); ask the curator only if the API cannot express this form; the FFSP 1 rows stay dropped (their label is imputed); WKW (bands until 2018) and WKWN (weeks from 2019) harmonised to one ordered six-band column (50-52, 48-49, 40-47, 27-39, 14-26, under 14; blank = did not work in the past 12 months); the notes of 2026-11-09 rewritten for the imputer; issues 2 and 3 applied. Then `dataset check`, the leak and task probes, and a focused panel (claim, column and split auditors, task gamer, mediator, editor).
   - C: `suggestion: No` with `No Good Target / Scientific Discovery` and a CC line on SEL-7 and USE-5 with the reasons: hot-deck today; a small share (1.7-3.1% a year); respondents scored while the imputer acts on non-respondents; the allocated rows' imputed Yes share 12.3-14.7% against 9.3-12.0% reported; Tanzania a weaker precedent (a forward-looking planner beside the statistician, SEL-7 never raised). Remove the folder, clear `v2_path`, add a CHANGELOG entry. Add `No Good Target / Scientific Discovery` beside `Duplicate` on food_stamps. acs_household_broadband and the Findex and FinScope records are read the same way when they come up. Issue 3's rule question (noaa_storm_events_damage, kickstarter, lending_club and ames_housing keep nominal money with no recorded exception) goes to the working copy's REVIEW.md as a rule item.

   [^sel7]: **SEL-7** (Must; narrows SEL-3): "A label the respondent already knows, asked in the same interview as the features (a past diagnosis), is predicted by nobody. A screening task needs positives that do not know yet, found by an independent measurement such as a lab test." Cases: cdc_diabetes_health_indicators (Lennart, 2026-10-15), stroke_prediction (2026-10-26).
   [^use5]: **USE-5** (Must): predict what the actor would act on, at the resolution they act on it; "A label checked and found to be another quantity than the one the actor acts on still fails" (Lennart, 2026-10-21, diabetes_3).
   [^amend]: The precedent checker's proposed wording, added to SEL-7: "... is predicted by nobody, unless the survey's own office fills the item for non-respondents from the same interview and flags the fill in the release (an item allocation): then the task is that office's, its rows the respondents, and the use case, inputs, split and metric are the imputer's."
   [^exc]: principles.md, "Exceptions and amendments": "A Must has no exceptions: only a higher-ranked Must overrides it, and anything else is an amendment."
   [^cc]: The record, CC 2026-11-08 (Lennart): SEL-7 "is decided at the build: it is the first issue of the dataset's REVIEW.md".
   [^sel2]: **SEL-2** (Must): "when a rule seems to exclude a dataset, check how the prediction is made in practice, and let the use case decide" (Lennart, 2026-10-15).
   [^use9]: **USE-9** (Should; narrows USE-8): before settling on approximate, ask whether the data mirrors another well-defined use case that practitioners have; weigh it against the factor "a use case rephrased only to excuse a gap".

2. **Only if issue 1 is B: score the imputer with `log_loss`, or keep the `roc_auc` fallback?**

   * **Problem:**
     - An imputer fills each blank from a probability (the hot-deck by copying a similar respondent's answer, a model by drawing from its prediction), so the predicted Yes share within each group of similar households must be right, which `log_loss` scores and `roc_auc` does not; both are allowed for a binary task without a source metric, so the choice is yours[^met8][^met11].
     - The advocate and the critic cite a 6-10% level error (the mean prediction falls that far short of the test year's Yes share), but it belongs to the temporal split: trained on the test year's other households, the shortfall is 0.5-1.8%.
   * **Effect on the task:** with `log_loss` a model that ranks well but misses the Yes share per cell loses; with `roc_auc` only the ranking counts.
   * **Experiments:** mean prediction against the observed Yes share (split auditor, one seed, LightGBM, 1M training and 300k test households):

     | Test year | Within the survey year (B) | Temporal (as built) |
     |---|---|---|
     | 2022 | 0.1051 / 0.1070 (-1.8%) | 0.1007 / 0.1070 (-5.9%) |
     | 2023 | 0.1047 / 0.1055 (-0.8%) | 0.1010 / 0.1055 (-4.3%) |
     | 2024 | 0.1006 / 0.1011 (-0.5%) | 0.0982 / 0.1011 (-2.9%) |

   * **Consistency:**
     - no binary dataset of the working copy declares `log_loss` from its context (the 112 on the fallback score `roc_auc`); anes_voting_2026 (the same TableShift convention) keeps it, and heart_disease kept it where the source also scored calibration.
     - `log_loss` would follow noaa_storm_events_damage (2026-11-08), where the metric followed a changed actor.
   * **Panel:** the advocate and the critic both prefer `log_loss` under B; the critic withdrew "required", and both leave it to you; the mediator notes that its main measured argument weakens under B's split, leaving the general reason, calibration per cell.
   * **Unknown:** whether `log_loss` and `roc_auc` rank models differently under B's split.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | `roc_auc` fallback (implemented) | a ranking metric, scored unweighted | the house fallback; anes_voting_2026 and heart_disease keep it | blind to the level the imputer draws from |
     | B | `log_loss` from the imputer's context | a strictly proper score of the probabilities; TableShift's accuracy named as the original | scores what the imputer uses; both debate sides prefer it; follows noaa_storm_events_damage | the measured level error mostly vanishes under B's split; departs from the house fallback |

   * **Recommendation:** B, lightly: the imputer acts on the probability itself. A stays a fair choice if you prefer the house fallback, since the level error that argued for `log_loss` mostly goes away under B's split. **Decision:** A or B?

   **Notes for the AI:** B (in the B pass of issue 1): `metric = Metric.from_context("log_loss", ...)` with the reason (the imputer draws from the probability, calibration per cell; MET-8, MET-11) and TableShift's accuracy named as the original; `dataset check`, the task probe.

   [^met8]: **MET-8** (Should): "For the same goal, prefer the probabilities. When no threshold metric is fixed (MET-6, MET-7) or the source has no unique metric (MET-5), score classification by a strictly proper scoring rule or a ranking metric: the fallback, `roc_auc` for binary and `log_loss` for multiclass tasks".
   [^met11]: **MET-11** (Must): every metric has one origin (source, stand-in, context or fallback), and the notes name the original whenever the declared metric is not exactly it.

3. **Only if issue 1 is B: keep the dollar amounts in each survey year's dollars, by an amendment saying that general inflation is no change of scale, or put them in 2024 dollars?**

   * **Problem:**
     - The household income, the gross rent and the owner costs are in each survey year's dollars, so the median household income goes from 55,463 (2014) to 84,266 (2024), while the rule asks for one scale per column[^clean21].
     - The build's reason for keeping them (the poverty ratio is comparable across years) does not set this case apart from four shipped datasets that keep nominal money with no recorded exception, so keeping them needs an amendment, not an exception[^exc3].
   * **Effect on the task:** deflating to 2024 dollars gains 0.0006 to 0.0007 ROC AUC; that is under the temporal split as built; under B's split a window trains and tests within one survey year, whose amounts share one adjustment factor, so deflating changes only the units there.
   * **Experiments:**
     - Column auditor, LightGBM, 2 seeds, the three amounts deflated with CPI-U annual averages (values from memory, not fetched): 2024 window 0.91333 to 0.91405, 2022 window 0.91015 to 0.91072, the same sign in 4 of 4 fits.
     - The task gamer's income percentiles within a survey year recover the same drift (+0.0006 to +0.0013).
   * **Consistency:**
     - noaa_storm_events_damage, kickstarter, lending_club and ames_housing ship nominal money with no exception.
     - college_scorecard and rosbank1 put a changed scale (not inflation) on one scale with the measuring body's conversion.
   * **Panel:** both the advocate and the critic accept the amendment; the column auditor had recommended deflating, as cheap and favoured by the measurement.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Each year's dollars, the rule amended (implemented) | the amounts stay as built; the rule gets the sentence that general inflation is no change of scale, and the dollars note cites it instead of the poverty-ratio reason | consistent with four shipped datasets; no constants to source | leaves a small, consistent gain (0.0007) unused (temporal split only) |
     | B | 2024 dollars | the three amounts deflated with the Census Bureau's factors or the BLS CPI-U-RS, the source named | one scale per column as the rule reads now; +0.0006 to +0.0007 | ten constants to source; the four shipped datasets would then need the same |

   * **Recommendation:** A, the amendment, which both sides accept and which keeps the four shipped datasets consistent. **Decision:** A or B?

   **Notes for the AI:** A: amend CLEAN-21 in `cleaning_features.md` ("general inflation is no change of scale: money in each period's own currency stays nominal", dated, Lennart, on acs_food_stamps_2014_2024; Cases noaa_storm_events_damage, kickstarter, lending_club, ames_housing) and cite it in the dollars bullet of `curation_comments`. B: in `_clean`, multiply HINCP, GRNTP and SMOCP by a deflator to 2024 dollars per survey year (BLS CPI-U-RS annual averages, fetched and named, or the Census Bureau's 5-year ADJINC factors), rewrite the dollars bullet; `dataset check`, the task probe.

   [^clean21]: **CLEAN-21** (Should): "One unit and one scale per column. When a feature's scale changes over time, put it on one scale the way an analyst would at the time, with the conversion the source or the measuring body publishes." Cases: college_scorecard (Lennart, 2026-10-16), rosbank1 (2026-10-26).
   [^exc3]: principles.md, "Exceptions and amendments": an exception names "the fact that sets the case apart"; "when the same reason has produced three exceptions, the next pass proposes an amendment".

**Review panel:** don't ship as built (mediator); ship after changes under B only if the curator takes the Census Bureau's item allocation as the use case and narrows the rule on self-reported labels by amendment, otherwise `No`. Tier full: claim auditor, column auditor, split auditor, domain practitioner, blind reviewer, task gamer, precedent checker, advocate and critic with one rebuttal each, mediator. Claim audit: 37 claims, 31 hold, 4 refuted in wording and none in the data (the zip dates, whose benefit items the run measured, the reason for no gap: fixed in the notes; the reading of the agency's items: replaced in issue 1), 2 untested (an address re-sampled after 5 years, which PUMS cannot link; that TableShift read Puerto Rico). Column audit: no column leaks (LEAK-10 checked three ways on all 43 inputs). Split audit: right for the outreach framing with notes (the release lag, the 2020 break, written now); within the survey year under B. Blind review: would benchmark with changes; its concerns are covered or artefacts of the clean room. Task gamer: barely gameable, nothing a deployed model lacks adds more than about 0.001 ROC AUC; its findings are now a protocol line and a kept-on-purpose note. Debate: agreed that A cannot ship, that B needs an amendment rather than an exception, the benefit items and the within-year split under B, the grounds kept under B, the notes; disputed: what the Tanzania precedent carries and whether the imputer is a use case worth mirroring (issue 1); left to the curator with one view: `log_loss` preferred under B, not required (issue 2), and the dollars by an amendment only the curator can make (issue 3).

<details><summary>Mediator</summary>

MEDIATOR REPORT: acs_food_stamps_2014_2024 (folder acs_food_stamps_2014_2024_1m), 2026-11-09
Panel: full tier. Read: principles.md; selection.md SEL-2, SEL-7; use_case.md USE-5, USE-9 and its weighed factor;
splits.md SPLIT-1; metrics.md MET-8; the builder report and claims.md; all seven phase-A reports; both opening briefs
with their rebuttals; the record, food_stamps.md and the Tanzania record and dataset.py (CC 2026-11-05). New run: none.
One fact comes from the split auditor's saved output (its saved per-window output, mean_pred).

**1. RECOMMENDATION (judgment record)**
Verdict: don't ship as built (A). Ship after changes under B only if the curator accepts the imputer as the use case
  and amends SEL-7 to match; otherwise `No` (C). Keep A in place while the curator decides; do not rebuild for B yet.
Validity: SEL-7 triggered and USE-5 fails for the outreach actor (Must; the agency holds the label and its targets are
  in "No": 48,305 "No" households at or below 130% of poverty against 50,819 "Yes" in all, 2024 window). Neither can
  be fixed under A. Under B both hold through the amendment. USE-6 (Must) then needs PAP/SSIP/HINS4 added, and
  SPLIT-1 (Must) needs folds within the survey year. LEAK-10 holds on all 43 inputs (checked three ways). PROV-6 holds
  (food_stamps stays the Duplicate). SEL-1 is no exclusion: under B keep the grounds, because 7 CFR 272.6 does not
  bind the Census Bureau.
Value: TP holds: LightGBM 0.914 against 0.814 for the best single feature and 0.897 for linear; the smallest class has
  at least 20,279 rows per fold. Metric: roc_auc fallback as built; under B, log_loss or roc_auc is the curator's
  weighing (issue 2).
Quality: CLEAN-21 (nominal dollars): amendment or deflation (issue 3). WKW harmonised to six bands (no decision). Note
  fixes listed in section 2.
Weighed (B):
  + a recurring, documented decision that exists apart from this dataset; the label, inputs and row are exactly the
    imputer's; each fill is flagged.
  - hot-deck today; 1.7-3.1% of households a year; the benchmark scores respondents while the imputer fills
    non-respondents; the amendment opens five survey records; it would be the first keep under SEL-7.
For the curator: issue 1 (B by amendment, or C) is the decision; issues 2 and 3 apply only under B.

Why leave A in place instead of rebuilding for B now:
  * The decision is the curator's twice over. It amends a Must, and it weighs whether the imputer is a real use case
    (USE-9's factors). A definition built for B would assume both answers. Principles: the AI argues, never overrides.
    The record's CC of 2026-11-08 says SEL-7 "is decided at the build: it is the first issue of the dataset's
    REVIEW.md".
  * A build adds no evidence the decision needs. B's numbers are already measured:
    - within-year AUC: 0.9158 / 0.9142 / 0.9171;
    - PAP/SSI/Medicaid of any member: +0.017;
    - level error under the within-year split: see issue 2.
  * The rebuild is not cheap, and all of it is lost under C:
    - a re-read of ten years of person files for any-member flags;
    - a split TemporalSplits cannot express (the test drawn within year Y, train the rest of Y plus earlier years; see
      issue 1);
    - a metric only the curator can pick;
    - the use case rewritten;
    - a dataset check (~1.3 min, 14.8 GB);
    - a focused panel (claim, column and split auditors, task gamer, mediator, editor).
  * Leaving A in place costs nothing: the folder is WIP and ships only once the curator settles. Waiting costs one round
    trip under B. The change list below is complete enough for one finisher pass.

**2. CHANGES TO MAKE NOW (no decision needed)**
Text only. No data change, so the checksum stays.
  a. REVIEW.md issue 1 (writing, EV-1):
     - Present B (with the amendment) against C.
     - Show A as the implemented state that breaks SEL-7 and USE-5 (Must), with no fact that sets it apart.
     - Replace the refuted bullet "items an agency is likely to hold reach 0.888 ... the rest of the signal comes from
       answers the actor would not have" with the class-composition numbers (claim auditor I3). The items a SNAP
       application asks reach 0.9104 of 0.9152.
  b. dataset.py notes: wrong or missing facts (writing.md, PROV-9, PROV-13, SPLIT-10, SPLIT-20, MET-16):
     - Zip dates: 2015-10 to 2025-12; the 2024 file was released 2025-12-04 (claim 4).
     - The Yes shares are unweighted. The weighted shares are 13.2 / 10.7 / 11.7% (2014 / 2019 / 2024) (claim 16).
     - The PAP/SSIP/HINS4 note:
       · The run measured the householder's items, not "any person's": +0.0065 for those, +0.017 for any member's
         (0.9142 to 0.9312).
       · Word the reason as a feature-set choice, not a leak call. No LEAK rule applies (column auditor E).
     - The no-gap sentence states a wrong fact (SPLIT-10). The year-t file comes out 9-11 months after year t
       (2023: 17 Oct 2024; 2024: 4 Dec 2025). Rewrite under the lt_vehicle amendment: all of a year's labels arrive
       together and final, so there is no selection; the newest year adds +0.0010 to +0.0027 ROC AUC at equal training
       size. Applies while A stands; superseded by B's re-split.
     - The 2020 break (SPLIT-20): pre-2020 training under-predicts the test-year Yes share by about 2 points. The
       emergency allotments and the Medicaid unwinding fall in the 2022-2023 test years.
     - The race-coding break at 2020: "Two or More Races" 1.7-1.9% before, 8.6-8.7% after.
     - The allocation shares of features, 2024 (PROV-13): any member's income 33.6%, public coverage 18.5%, public
       assistance 13.2%. The hot-deck test found no FS in imputed income (+0.0015 against +0.0143).
     - The protected-grounds list: add nativity, the three difficulty items and age (claim 31).
     - The features and the label cover the same past-12-month window (column auditor B).
  c. Record of food_stamps (PROV-6): an AI Assessment line. The CC of 2026-11-08 ("same ACS item (FS) and population
     filter") no longer matches the build: the unit is the household, with no TableShift filter. The Duplicate verdict
     holds (PROV-6), and the curator's wording is left untouched.
  d. Bundled into the B pass, if B is chosen. Moot under C:
     - WKW/WKWN harmonised to one ordered six-band column (CLEAN-21, Should; both sides accept; cheap and safe);
     - the notes above rewritten for the imputer.

**3. ISSUES FOR THE CURATOR (ranked)**
ISSUE 1. P2/P3, Must: SEL-7 and USE-5. Is the Census Bureau's item allocation the use case (B, by amendment), or is
the dataset `No` (C)?
  Problem: the household reports its own SNAP receipt in the interview that gives all 43 inputs (SEL-7's mechanism).
    The outreach actor declared in A holds the label for its caseload, and its targets (eligible non-participants)
    sit in "No". In the 2024 window, 64% of the households at or below 130% of poverty report No. In the top 10% of
    scores within <=200% of poverty, 82% report Yes.
  Effect: under A a better model ranks current recipients higher. That is the opposite of the decision, and no change
    to the definition fixes it.
  Agreed by both sides: A cannot ship. B ships only by an amendment of SEL-7. Otherwise C.
    - Form: by position SEL-2 (Must, earlier, "let the use case decide") would let the use case carry B without
      a change to the text. But that hands the call to USE-9's weighing, and every survey item someone could impute
      would argue its way in the same way.
    - So the amendment is the safer form. It records the reading as a narrow rule.
    - Proposed wording (precedent checker): "... is predicted by nobody, unless the survey's own office fills the item
      for non-respondents from the same interview and flags the fill in the release (an item allocation): then the
      task is that office's, its rows the respondents, and the use case, inputs, split and metric are the imputer's."
    - Name the records it opens: acs_household_broadband, folktables_acs_income,
      ntia_internet_use_survey_home_adoption, nsduh_past_year_drug_use, nsduh_mental_health_treatment. It keeps
      cdc_diabetes and stroke_prediction out (their labels are not allocated).
  Best evidence for B (advocate):
    - The Bureau fills FS from the same interview for 1.72-1.83% (2014-18), 1.95% (2019) and 2.91-3.08% (2021-24) of
      households, and flags each fill (FFSP). This was measured twice.
    - The decision, the inputs, the label (the report, not the truth, so the 35% under-reporting is no label gap) and
      the row all match.
    - The Bureau is studying model-based against hot-deck allocation (AAPOR 2026; only the talk's existence is cited).
    - Precedent: the Tanzania survey statistician (2026-11-05).
  Best evidence for C (critic):
    - The actor uses hot-deck today, on a small share of households.
    - The benchmark scores respondents while the imputer acts on non-respondents. MAR is assumed: NBER WP 29184 finds
      higher error among imputed cases. The data agree: the allocated rows' imputed Yes share is 12.3-14.7%, against
      9.3-12.0% reported (claim 11).
    - Tanzania is weaker than cited. Its statistician joined a forward-looking trip planner, with no data change and
      SEL-7 never raised (record CC 2026-11-05: "the planner still looks forward"). Here the imputer would be the only
      actor and the first keep under SEL-7, against cdc_diabetes and stroke_prediction (both `No`) and dataorg.
  What would settle it: the curator's reading of whether an allocation of 2-3% of rows, by hot-deck today, is a
    decision the benchmark should mirror (USE-9's weighed factor). A source showing model-based allocation in the
    Bureau's production would strengthen B.
  Decision:
    B: amend SEL-7 as above and rebuild for the imputer, all in one finisher pass, then a focused panel:
      - use_case, known and fit_reason for the imputer; fit approximate, naming three gaps: hot-deck today,
        respondents scored while the imputer acts on non-respondents (MAR), and a small share; TableShift kept as the
        task's origin only (USE-1, USE-8);
      - PAP, SSIP and HINS4 added as any-member household flags (USE-6, Must);
      - the protected grounds kept, with the reason (no law binds the imputer; SEL-1 tension row);
      - the split within the survey year (SPLIT-1, Must). No exception is possible: the critic is right and the
        advocate withdrew the "keep temporal" default. The form that mirrors the imputer: test = random households of
        year Y; train = the other households of Y plus earlier years; Y = 2024, 2023, 2022. Plain IID over all years
        also trains on later years' files. The task gamer measured the future-file part at about +0.0005. Ask the
        curator only if the API cannot express the first form;
      - the FFSP 1 rows stay dropped (their label is imputed);
      - the notes of section 2 rewritten for the imputer, plus WKW;
      - the metric (issue 2) and the dollars (issue 3).
    C: `No` with `No Good Target / Scientific Discovery` (SEL-7, USE-5):
      - the folder removed, with a CHANGELOG entry;
      - food_stamps (`No`, Duplicate) also carries the SEL-7 reason in its markers;
      - acs_household_broadband and the Findex/FinScope records read the same way.

ISSUE 2. P6, Should; only under B: the metric. log_loss from context (MET-8, MET-11) or the roc_auc fallback?
  Both sides agree that both are legal under MET-8 and that this is the curator's weighing. Neither blocks shipping.
  For log_loss:
    - The imputer draws from the probability, so the level per cell matters.
    - The metric follows a changed actor (noaa_storm_events_damage, 2026-11-08).
  For roc_auc:
    - The house fallback, used by all 112 binary fallbacks in the copy.
    - anes_voting_2026 (the same TableShift convention).
    - heart_disease kept roc_auc where the source also scored calibration.
  New fact for the weighing: both briefs cite a 6-10% level error, but it belongs to the temporal split. Under B's
    within-year split it nearly vanishes. Mean prediction against the observed share (split auditor, one seed, LightGBM,
    1M train / 300k test):
      2022: 0.1051 / 0.1070 (-1.8%)
      2023: 0.1047 / 0.1055 (-0.8%)
      2024: 0.1006 / 0.1011 (-0.5%)
    In the same run the temporal split gave -5.9% / -4.3% / -2.9% (0.1007 / 0.1070, 0.1010 / 0.1055, 0.0982 / 0.1011). So log_loss's main measured argument weakens under B. What
    remains is the general MET-8 reason: calibration per cell.
  What would settle it: whether model rankings differ between log_loss and roc_auc under the B split (not measured),
    or the curator's preference for the house fallback.

ISSUE 3. P7, Should; only under B: CLEAN-21. Dollar amounts in each survey year's dollars.
  Both sides accept option a: an amendment saying general inflation is no scale change.
    - Four shipped siblings keep nominal money with no recorded exception: noaa_storm_events_damage, kickstarter,
      lending_club, ames_housing.
    - The builder's exception reason (POVPIP is comparable) does not set this case apart.
  Against: deflating with the Bureau's factors gains +0.0006 / +0.0007 ROC AUC (4 of 4 fits). The task gamer's
    within-year percentiles recover the same drift (+0.0006 to +0.0013).
  Under B's within-year split most training rows share the test year's dollars, so the effect should shrink further
    (an inference, not measured).
  Decision: amend CLEAN-21 (a), or deflate (c). An amendment is the curator's alone. Quality only: it never excludes.

Settled, no curator issue:
  * Protected grounds: under B keep all, with the reason. Under C moot. A is not available, so the completed drop (with
    the HHT, WKEXREL and FER recodes) is needed only if the curator ever restores the agency actor.
  * Unit: households, no TableShift filter (MET-17, USE-11). Agreed.
  * Gap: moot under B and C. Under A it is the text fix in section 2b.

Task gamer exploits, mapped (the definition has no "Potential leak, kept on purpose:" notes and no accepted warnings,
so every item is new to the notes; none is an issue):
  1. Labelled rows of later years added to training, +0.0005 from the future part (the rest is volume). Rule: the
     protocol (train only on the shipped positions) and SPLIT-9. Not a data issue.
  2. Year-level statistics over train and test rows, +0.0006 to +0.0013. Rule: LEAK-30 (a transform of the
     participant's own over all rows; the data ship no such statistic). It is the inflation drift of issue 3, which
     the column auditor measured the same.
  3. Income roundness (AUC 0.60 alone). Rule: LEAK-13 / LEAK-39-40. It is the reported answer itself (benefit amounts
     are exact), known at the interview: no leak. The builder's number-format probe (0.706, the same as tenure
     missingness) is the known part.
  4. The 1M training cap costs +0.0028 to +0.0045. That is the row budget (house rule), already stated in
     splits_comment. Kit side: task.md should state it.
  5. Lookup in the public PUMS (100% on 543 WY rows): true of any public source. No rule, no action.
Blind reviewer: would benchmark with changes. Every concern is covered above or is a clean-room artefact:
  - year sampling: the row budget, stated in the notes;
  - the broad population: matters for A only;
  - FFSP: dropped;
  - the "ordered stored as unordered" finding: the kit parquet loses the order; the frame has six ordered scales
    (column auditor).

**4. AGREED FACTS**
  * One row per occupied household, 12,751,578 over 2014-2019 and 2021-2024. Exactly one householder each (0
    exceptions, raw re-read). FFSP 1 rows are dropped: 1.72-1.83%, 1.95%, 2.91-3.08% a year.
  * FS is the household's own report, from the same interview as all 43 inputs. 35% of true recipient households report
    No (NBER WP 25143).
  * Under A the outreach targets sit in "No": 48,305 "No" households at or below 130% of poverty, against 50,819 "Yes"
    in all (2024 window).
  * No column leaks:
    - income and POVPIP exclude SNAP (ACS Subject Definitions);
    - the income hot-deck carries no FS (+0.0015 against +0.0143);
    - PUBCOV is not assigned from FS;
    - 0 exact copies across the split.
  * LightGBM 0.914, linear 0.897, the best single feature 0.814. Within <=200% of poverty: 0.849.
  * PAP, SSIP and HINS4 are known at the interview, and no LEAK rule bars them: +0.0065 with the householder's items,
    +0.017 with any member's.
  * Within-year IID: 0.9158 / 0.9142 / 0.9171, against temporal 0.9120 / 0.9109 / 0.9148 (split auditor).
  * The year-t PUMS comes out 9-11 months after year t. The newest year adds +0.0010 to +0.0027.
  * Protected grounds cost at most 0.0003 (a complete drop) to 0.004 (12 items). Sex survives in HHT, WKEXREL and FER
    for 69.4% of rows. 7 CFR 272.6 binds state agencies, not the Census Bureau.
  * Deflating the dollars: +0.0006 / +0.0007.
  * 31 of 37 claims hold. The 4 refuted ones are wording (claims 4, 29, 34, and issue 1's reading of claim 30).

**5. CONSISTENCY WITH PRECEDENT**
  * cdc_diabetes_health_indicators (2026-10-15) and stroke_prediction (2026-10-26), both `No` under SEL-7. C follows
    them. A departs from them with no fact. B departs on a measured fact: a flagged allocation of this very label,
    which BRFSS's item never had. As a Must it enters only by amendment, so the register's opposite-outcome flag
    resolves to the amendment.
  * dataorg_financial_health_prediction_challenge (2026-10-22, `No`, a FinScope survey answer): C follows it. Under B
    the amendment does not open it (Findex and FinScope publish no allocation flags; the precedent checker's reading,
    not checked per record).
  * ai4d_lab_tanzania_tourism_classification_challenge (2026-11-05): B follows it only in part. There the statistician
    stood beside a forward-looking planner: split unchanged, no data change, SEL-7 not raised, the fill unflagged.
    Here the imputer would be the sole actor, which forces the within-year split (Tanzania issue 3's own logic). B is
    the first keep under SEL-7, and Tanzania becomes its earlier, unflagged instance in the Cases row.
  * food_stamps (`No`, Duplicate, CC 2026-11-08): the verdict holds under PROV-6 under every option. The CC's wording
    ("same ... population filter") no longer matches the build: section 2c. Under C its markers also carry SEL-7.
  * Side note, not this dataset's decision: income, public_health_ins and unemployment are `No`/Duplicate on "same data
    as Food Stamps". That reason is now one PROV-7 does not support.
  * Metric: roc_auc as built follows anes_voting_2026 and the house fallback. log_loss under B would follow noaa (the
    metric follows the actor).
  * Grounds: under B consistent (no law binds the imputer). The rais/wioa question of widening the tension row is not
    decided here.
  * CLEAN-21: the four nominal-money siblings make an amendment due in substance (precedent checker D4).

</details>

<details><summary>Claim audit</summary>

CLAIM AUDITOR REPORT: acs_food_stamps_2014_2024 (folder acs_food_stamps_2014_2024_1m), 2026-11-09

Verdict: the data claims hold. 31 of the 37 claims hold as written. 4 are refuted or misdescribed, all in the
evidence or reasoning and none in the data: claim 4 (zip dates), claim 29 (what the benefits run measured), claim 34
(why no gap) and the reading of claim 30 that issue 1 relies on. 2 cannot be tested from here. No leak was found and
the metric holds. The refutations change the wording of issues 1 and 2 and the no-gap argument. They do not change any
row, any feature or the metric.

Scratch: the run's work files. The frame and splits came from the definition itself
(to_container, 67 s, 14.8 GB peak). Models: LightGBM, 400 trees, lr 0.05, 63 leaves, 4 threads.

**A. TABLE (claim | source | test | result | evidence | rule)**

1  | National 1-year PUMS hus/pus 2014-2019, 2021-2024, census server, no login | claims 1, download_description | listed
   the warehouse | HOLDS | 20 zips present, 0.80-0.87 GB a year | PROV-8
2  | 2020 has no regular 1-year file | claim 2 | HTTP GET .../pums/2020/1-Year/ | HOLDS | 404 (the experimental release
   is elsewhere) | SPLIT-1
3  | Puerto Rico is not in the national files | claim 3 | STATE values in the prepared parquet; zip contents | HOLDS |
   51 STATE codes, 72 absent; the 2024 hus zip holds only psam_husa/b.csv (hpr/ppr are separate on the server). That
   TableShift read PR was NOT re-read | PROV-6
4  | "zips dated 2025-08 to 2025-12 on the server" | claim 4 | server mtimes of the downloaded zips | REFUTED (minor) |
   2014 hus 2015-10-27, 2017 2018-10-02, 2021 2022-09-22, 2023 2024-09-10; only 2024 is 2025-12-04. The 2024 PUMS
   was released 2025-12-04 after a delay from 2025-10-16 (census.gov 2024 release page). Year 2025 and the licence
   hold | PROV-9
5  | Dictionaries 2017-2024 CSV, 2014-2016 text | claim 5 | listed | HOLDS | | PROV-10
6  | TableShift task: target FS, motivation quote, population, 840,582 rows, held-out East South Central | claim 6 |
   tableshift.org/datasets.html | HOLDS | every element is verbatim on the page; the page names no metric | MET-1
7  | food_stamps is a duplicate | claim 7 | food_stamps record CC 2026-11-08 | HOLDS (as a record fact) | the CC line's
   "same ... population filter" is no longer exact (the builder's issue 3) | PROV-6
8  | One row per occupied unit (TYPEHUGQ 1, NP>0), 50 states + DC | claim 8 | re-read the raw zips independently | HOLDS | 2014 1,218,240 / 2019 1,276,716 / 2024 1,348,408 occupied, equal to the parquet | LEAK-17
9  | Exactly one householder per occupied unit (RELP 0 to 2018, RELSHIPP 20 from 2019) | claim 9 | own raw re-read:
   count of householder records per occupied SERIALNO, and householders outside occupied units | HOLDS | 2014
   (RELP), 2019 and 2024 (RELSHIPP): 0 units with none, 0 with more than one, 0 householders outside occupied units;
   2019 already uses RELSHIPP (values 20-38). The prepared parquet has 0 duplicate SERIALNO in all 10 years |
   LEAK-17
10 | 1,218,240 (2014) to 1,348,408 (2024); 12,751,578 total | claim 10 | parquet group-by | HOLDS | exact | -
11 | Allocated FS (FFSP 1) dropped: 1.73-1.83% (2014-18), 1.95% (2019), 2.91-3.08% (2021-24) | claim 11 | parquet
   and raw | HOLDS | 1.723-1.833%, 1.949%, 2.912-3.079%. Note: the allocated rows' imputed Yes share is 12.3-14.7%,
   above the reported 9.3-12.0%, so the drop removes poorer households, not a random 2-3%. The drop is still
   right, because the label of those rows is imputed | LEAK-22..26, PROV-13
12 | FS item wording and codes (1 yes, 2 no, b vacant) | claim 12 | 2014 txt and 2024 CSV dictionaries | HOLDS | same
   codes in 2014 and 2024 | -
13 | Household unit avoids LEAK-17 | claim 13 | duplicate SERIALNO per year | HOLDS | 0 | LEAK-17
14 | No TableShift person filter | claim 14 | code read | HOLDS | | -
15 | Target Yes = FS 1, No = FS 2 | claim 15 | code and frame | HOLDS | FS takes only {1, 2} among occupied units in all
   years | CLEAN-25
16 | Yes shares 12.0% ... 9.3% (2019), 10.9% ... 10.2%; 10.59% shipped | claim 16 | parquet; frame | HOLDS as unweighted
   sample shares | 12.00, 11.54, 11.14, 10.53, 10.01, 9.31, 10.94, 10.69, 10.58, 10.16; frame 10.59%. The weighted
   shares (WGTP, reported answers) are 13.2% (2014), 10.7% (2019), 11.7% (2024): the raw sample under-represents
   recipient households by 1.2-1.5 points, from nonresponse follow-up subsampling (my reading). The notes should say
   "unweighted", so nobody compares these shares with published rates | MET-16, writing
17 | 35% of true recipient households do not report in the ACS (Meyer, Mittag, Goerge, NBER WP 25143) | claim 17 |
   nber.org/papers/w25143 abstract | HOLDS | ACS 35%, SIPP 23%, CPS "fully 50"%, administrative data of two states;
   WP Oct 2018; JHR 57(5) 2022 | USE-5
18 | 43 features: 33 categorical or ordered, 10 numeric | claim 18 | frame dtypes | HOLDS | 34 category (incl. target)
   + 4 float64 + 1 int32 + 5 int64 | -
19 | Income x ADJINC, housing x ADJHSG, each survey year's dollars | claim 19 | dictionaries; raw ADJINC values;
   medians | HOLDS | ADJINC is one constant a year (2014 1.008425, 2019 1.010145, 2024 1.015250), and the 2014
   dictionary says it "inflation-adjusts reported income to 2014 dollars". ADJHSG is 1.000000. The median household
   income goes from 55,463 (2014) to 84,266 (2024), +52% nominal, which is the drift issue 4 is about | CLEAN-21
20 | POVPIP top-coded 501 | claim 20 | dictionary; frame max | HOLDS | max 501 | -
21 | STABLE_CODED codes mean the same in every year (wording only differs) | claim 21 | a comparison of every
   STABLE_CODED item in all ten dictionaries compared with the 2024 words | HOLDS | only wording differs (HHT 2-3, CIT,
   WKEXREL, LNGI 2015, RAC1P 5 2015, COW 2015, ST 4 "Arizona/AR" typo); the only code missing from 2024 is ANC 8
   (2018-2019), which the code sets to missing | CLEAN-12
22 | POBP 208 Cyprus and 463 Eastern Africa NS in 2014-16; 2017 lacks 208 and has 463 South Sudan | claim 22 | parsed
   dictionaries | HOLDS | these are the only two differences | CLEAN-12
23 | OCCP 2010 codes to 2017, 2018 codes from 2018; 656 levels | claim 23 | frame | HOLDS | 656 | -
24 | ANC 8 set missing | claim 24 | dictionaries 2018/2019; frame | HOLDS | 210 missing in the frame | -
25 | Blank ENG = speaks only English | claim 25 | dictionary ("N/A (less than 5 years old/speaks only English)");
   minimum householder age 15 | HOLDS | | CLEAN-14
26 | Six ordered scales (24, 5, 7, 3, 3, 4 levels); BLD unordered | claim 26 | frame dtypes | HOLDS | | CLEAN-14
27 | Blank shares 34.1, 73.9, 27.9, 25.9, 35.5, 79.6%; MIL under 17; ESR under 16 (92) | claim 27 | frame | HOLDS |
   exact. MIL missing only at ages 15-16; ESR missing only at 15 | CLEAN-10
28 | Weights, replicates, PUMA, REGION, DIVISION, PAP, SSIP, HINS4, WKW, NWLA, NWLK, WRK not read | claim 28 | item lists
   in dataset.py | HOLDS | RELP/RELSHIPP are read only for the filter | MET-16
29 | "PAP, SSIP and HINS4 [of any person] add 0.007 (0.9135 to 0.9208)" | claim 29; curation_comments ("of any person")
   | read the builder's scratch scripts; re-ran on 2022-23 train 400k / 2024 test 200k | MISDESCRIBED | the builder's run used the HOUSEHOLDER's PAP/SSIP/HINS4 plus PINCP, not any
   person's. Re-run: base 0.9142; + householder PAP/SSIP/HINS4 (no PINCP) 0.9207 (+0.0065, so the number holds for
   the householder); + any person's PAP>0 / SSI>0 / Medicaid (any, count) 0.9312 (+0.017). Some member has Medicaid
   in 80.1% of Yes households and 16.2% of No | USE-3, LEAK-10, EV-1
30 | Protected items add 0.0019; five items add 0.0007; administrative-like items reach 0.8878 | claim 30;
   the builder's feature-set probe output | re-ran on the SHIPPED frame and 2024 window (1M/500k) |
   NUMBERS HOLD; THE READING ISSUE 1 GIVES THEM IS REFUTED | all 0.9152, admin-like 0.8878, without protected 0.9131
   (builder 0.9157/0.8878/0.9138). The "application form" set (admin-like + rent, owner costs, tenure, employment
   status, hours, workers in family, disability, citizenship, vehicles: items a SNAP application asks) reaches 0.9104.
   That closes 82% of the gap (0.0226 of 0.0274). Issue 1's "the rest of the signal comes from answers the actor
   would not have" is false for an agency that takes applications | SEL-7, USE-8, EV-1
31 | 7 CFR 272.6(a) quote | claim 31 | law.cornell.edu/cfr/text/7/272.6 | HOLDS (verbatim) | grounds "age, race,
   color, sex, disability, religious creed, national origin, or political beliefs"; between the two quoted parts:
   ", the issuance of coupons, the conduct of fair hearings, or the conduct of any other program service". BUT the
   paragraph protects "any applicant or participant", and outreach targets are neither yet, so issue 2's "reads as
   yes" for outreach is not settled by the text. Age is a listed ground, yet it is not in the builder's protected
   list or in any option | SEL-1
32 | Metric roc_auc fallback; TableShift reports accuracy; scored unweighted | claim 32; Metric block | looked again:
   tableshift.org (no metric), arXiv 2312.07577 abstract ("ID and OOD accuracy"); dummy scores per fold with
   data_foundry.v2.metrics.scorer | HOLDS | accuracy is a threshold metric with no threshold or cost set by the source
   (MET-6), a house convention (MET-5), and anes_voting_2026 made the same call. The scorer gives 0.5 for a constant
   and 0.4991-0.5017 for random DataFrame probabilities (columns No/Yes) on each of the 3 folds. Positives per test
   fold: 50,819 / 52,884 / 53,443. No scoring columns, no sample weight. MET-2 caveat: TableShift's population was
   low-income adults, ours is all households (POVPIP alone gives 0.817), so the AUC means "rank all households", not
   TableShift's slice | MET-1, MET-2, MET-5, MET-6, MET-11, MET-16
33 | Temporal: tests 2024, 2023, 2022, each trained on earlier years; the oldest trains on 7 of 10 years | claim 33 |
   container splits | HOLDS | train years are strictly earlier, train/test overlap 0; the oldest window's 7 years
   hold 68.7% of reported households (SPLIT-14 floor 50%) | SPLIT-2, SPLIT-14
34 | "No gap: the 1-year PUMS of year t is released in the autumn of t+1, within the one-year step" | claim 34;
   splits_comment | release dates; a re-fit (same train size, with and without the newest train year, 2 seeds) |
   REASONING REFUTED, EFFECT SMALL | year t's file comes out 9-11 months after year t ends (2022: Sept 2023,
   2023: Sept 2024, 2024: Dec 4 2025). A refit at the start of test year t therefore knows years up to t-2, and the
   t-1 file only arrives in the last quarter of t. A gap of 1 survey year mirrors the "refit on the newest released
   file" use. Measured: 2024 window no gap 0.9146/0.9146 against gap 1 0.9131/0.9133 (-0.0014); 2023 window
   0.9117/0.9114 against 0.9104/0.9104 (-0.0012). With gap 1, the oldest window trains on 2014-2019, about 59% of the
   rows (above the 50% floor) | SPLIT-10 (planning gap), SPLIT-1
35 | 1M train / 500k test per window; 2.5M frame | claim 35 | container | HOLDS | n_train 1,000,000 and n_test 500,000
   in every window | -
36 | Bundle checks: 0 errors, 0 warnings, 3 infos | claim 36 | README frontmatter | HOLDS | | -
37 | fit approximate (self-report, survey stands in for agency, under-reporting) | claim 37 | see 30, 29 and the
   class-composition test below | HOLDS as a description; whether "approximate" is enough is SEL-7's call (issue
   1) | USE-1, SEL-7

Implied claims (not written, but the definition implies them):
I1 | Every feature is known at the prediction point; no feature carries SNAP | test: ACS 2022 Subject Definitions
   (income section) | HOLDS | "Receipts from the following sources are not included as income: ... the value of
   income 'in kind' from food stamps"; public assistance "does not include Supplemental Security Income (SSI) or
   noncash benefits such as Food Stamps". So HINCP and POVPIP carry PAP and SSI but not SNAP. The FS item asks whether
   "one or more of the current members received benefits ... during the past 12 months". Side note: Census user note
   2022-11 says the 2021 public assistance amounts are inflated by stimulus and child tax credit payments reported as
   PAP. This shifts HINCP slightly in the 2021 training year, a drift and not a leak | LEAK-10, USE-3
I2 | No row is a copy across the split | exact feature copies across train/test, survey year ignored: 0 in all three
   windows. An address is never sampled twice in five years (ACS design, five rotating subframes), so the same
   address can recur only 5 or more years apart (train 2017-2019 against test 2022-2024). SERIALNO does not link
   years | HOLDS for copies; UNTESTED for entity recurrence (not linkable from PUMS) | LEAK-16..21
I3 | The target is the real-world target of the use case (outreach targeting) | composition of the 2024 test window
   (frame) | REFUTES THE USE CASE'S FIT, IN SUPPORT OF ISSUE 1 | 48,305 "No" households have a poverty ratio at or
   below 130% (roughly SNAP's gross-income test), against 50,819 "Yes" households in all. 64.2% of households at or
   below 130% report No. The outreach targets are as many as the positives, and all of them sit in the negative
   class. A model that separates participants from eligible non-participants scores higher on AUC and is worse for
   outreach. (POVPIP uses the Census thresholds, not HHS guidelines, and broad-based categorical eligibility goes to
   130-200% in many states, so this is approximate. With the 35% under-reporting, part of these households are
   recipients.) | SEL-7, USE-1, USE-5
I4 | The split mirrors the use | see 34 | gap missing, small effect | SPLIT-10

**B. REFUTED AND UNTESTED, RANKED (principles.md: validity first, Must first)**

1. Issue 1's evidence "items an agency is likely to hold reach 0.888 ... the rest of the signal comes from answers the
   actor would not have" (claim 30 as read in issue 1). P2/P3, SEL-7 (Must). REFUTED: items a SNAP application asks
   reach 0.9104 against 0.9152 for all and 0.8878 for the builder's admin-like list, which closes 82% of the gap. The
   comparison also cannot separate this case from cdc_diabetes, because an agency has no records of non-applicants,
   the very households outreach looks for. The decisive fact for SEL-7 is I3: 48,305 eligible-looking No households
   against 50,819 Yes in the 2024 window, with 64% of the at-or-below-130% households in the No class. What it
   changes: the bullet goes, and the class-composition numbers replace it. It does not weaken the recommendation
   (C), and arguably strengthens it. Mildest remedy: rewrite that bullet of issue 1 in REVIEW.md. No definition
   change.

2. Claim 34, no gap (splits_comment). P4, SPLIT-10 (Should, the planning-gap clause). REASONING REFUTED: the release
   comes 9-11 months after the survey year (2024: Dec 4 2025), so a refit at the start of a test year knows only
   t-2. Effect: -0.0014 (2024 window) and -0.0012 (2023 window) ROC AUC with the newest train year removed. With
   the gap the oldest window still trains on about 59% of the rows. Mildest remedy: record it as an exception in
   splits_comment with these numbers ("the release lag is most of a year; a one-year gap costs 0.001 AUC"), or set
   a one-survey-year gap. Either keeps the dataset. The current sentence "within the one-year step" is wrong as an
   argument.

3. Claim 29 and the curation note "PAP, SSIP and HINS4 of any person ... gains 0.007". P4/P3 (USE-3, "what an agency
   would know"), and writing. MISDESCRIBED: the builder's run added the householder's PAP, SSIP, HINS4 and PINCP.
   Re-run: the householder's three items give +0.0065, which matches. Any person's PAP, SSI or Medicaid gives +0.017
   (0.9142 to 0.9312), and some member has Medicaid in 80.1% of Yes households and 16.2% of No. What it changes:
   the note must say whose items were measured and give the any-person number. Medicaid enrollment is exactly what
   integrated eligibility systems hold, so it also bears on issue 1 (which inputs an agency has) and on whether
   leaving them out is right. Mildest remedy: correct the note's wording and numbers. Keeping them out stays
   defensible as "other benefits of the same 12 months".

4. Issue 2 / claim 31's reading. P1 note (SEL-1, a tension and not an exclusion). The quote HOLDS verbatim, but:
   (a) 272.6(a) protects "any applicant or participant", so whether outreach to non-applicants is covered is open,
   not "reads as yes"; (b) age is a listed ground and is kept in every option; (c) the language items
   (household_language, limited_english_household, householder_english_ability) are not weighed as national-origin
   proxies. Measured: without the 11 protected items 0.9131; also without age and the three language items 0.9107
   (-0.0045 from all). Mildest remedy: correct issue 2's "Unknown" line, add age and language to options C/B, and
   give the numbers. The README note lists "sex, race, Hispanic origin, ancestry, place of birth, citizenship and
   disability", leaving out nativity and the difficulty items, which the probe list includes. Align them.

5. Claim 4, zip dates. P5 (PROV-9), writing. REFUTED: only the 2024 zips are dated 2025-12; the older ones date from
   2015-10 to 2024-09. Mildest remedy: reword ("each year's zips as published, 2015-10 to 2025-12; the 2024 file
   was released 2025-12-04").

6. Claim 16, Yes shares (informational). Correct, but unweighted. The weighted shares are 13.2 / 10.7 / 11.7%
   (2014 / 2019 / 2024). Remedy: add "unweighted" to the note and the decision-table column. MET-16 still holds, and
   scoring stays unweighted.

Untested:
U1. Entity recurrence across the split: an address can be re-sampled 5 or more years later (train 2017-2019 against
    test 2022-2024). PUMS cannot link it. Exact copies are 0, so the risk is low. (LEAK-16..21)
U2. Whether FS is a matching variable in the hot-deck allocation of income items (allocation flags of features not
    read). If it is, allocated HINCP of a few percent of rows would carry FS. Remedy if wanted: read FHINCP-type flags
    and test the AUC on allocated-income rows against reported ones. (LEAK-10, PROV-13)
U3. That TableShift's folktables loader read Puerto Rico (claim 3, second half): not re-read. It changes nothing in
    the shipped data.

What holds and matters most: one householder per occupied unit (0 exceptions, independent raw re-read for 2014, 2019
and 2024); the FFSP drop and the yearly shares exactly; the 35% figure; the CFR quote verbatim; that no feature
carries SNAP (Subject Definitions); the dollar handling; the weights left out and the unweighted scoring (MET-16);
the metric fallback and its scorability on every fold.

Sources: tableshift.org/datasets.html; arxiv.org/abs/2312.07577; nber.org/papers/w25143;
law.cornell.edu/cfr/text/7/272.6; ACS 2022 Subject Definitions (assets.nhgis.org/original-data/acs/
2022_ACSSubjectDefinitions.pdf); census.gov ACS user note 2022-11; census.gov 2024 data release page (PUMS
2025-12-04); www2.census.gov/programs-surveys/acs/data/pums/2020/1-Year/ (404).

</details>

<details><summary>Column audit</summary>

COLUMN AUDITOR REPORT: acs_food_stamps_2014_2024 (folder acs_food_stamps_2014_2024_1m), 2026-11-09

Verdict: no column leaks the SNAP answer (LEAK-10 not triggered on any of the 43 inputs, with three checks run on the
data); the cleaning is close to the expert state. Two things need changes or a call:
  (1) [P1, SEL-1] the protected-grounds drop the builder offers (option B) is incomplete: the householder's sex
      survives, exactly, in household_type, work_experience_householder_spouse and householder_gave_birth_past_year
      (named for 49% of rows by the first two, 69% with the third, 100% agreement). If B is chosen, those three need
      a recode. Age, disability and citizenship have a fact that sets them apart (SNAP's own eligibility rules use
      them); the ancestry recode holds no ancestry.
  (2) [P7] CLEAN-21 (nominal dollars, measured below) and three cheap cleaning points (weeks worked harmonisable
      across the 2019 change; the 2020 race-coding break; the notes' reason for leaving out PAP/SSIP/HINS4).
Everything else is fine.

Method. Read dataset.py (prediction point: the interview of a survey year, scored by a model fit on earlier years),
the PUMS data dictionaries 2014-2024 in the warehouse (CSV 2017-2024, text 2014-2016), TableShift's acs.py
(ACS_FOODSTAMPS_FEATURES), principles.md, use_case.md, leak_checks.md, cleaning_features.md, selection.md (SEL-1,
SEL-7), the rais panel's mediator report (the extended "factor the actor may no longer use" row) and the builder's
report and probes. Loaded the frame through dataset_io.from_definition (2,500,000 rows, 44 columns, 57 s, 15.7 GB
peak). Read the 2024 person file once more for the allocation flags. Scripts and outputs: the run's work files.

**1. COLUMN TABLE**
Known at prediction? = known at the prediction point the definition names (the household's own interview of the
survey year). "Window" = the item covers the same past 12 months as the label (see section 3, point W).

column | meaning (PUMS item, dictionary) | known at prediction? | dtype and cleaning | verdict | rule
---|---|---|---|---|---
survey_year | year of the 1-year file (constant per file) | yes | int, numeric; the time column, unseen in each test window | fine | USE-3
state | STATE (ST until 2022), 51 levels, decoded "California/CA" | yes | category, decoded | fine | CLEAN-12
household_size | NP, persons in household 1-20 | yes | int count, no cut end | fine | CLEAN-14
household_type | HHT 1-7, married couple / other family by householder's sex / nonfamily by sex and alone | yes | category, 7 levels; wording of 2014-2018 ("no wife present") mapped to 2024 words, same codes | fine; ENCODES SEX for HHT 2-7 (51% of rows): recode if sex is dropped | SEL-1 (issue A)
children_present | HUPAC, under 6 only / 6-17 only / both / none | yes | category, nominal (combinations, no single line) | fine | CLEAN-14
own_children | NOC, own children in household 0-19 (max 15 seen) | yes | int count | fine | CLEAN-14
related_children | NRC, related children 0-19 (max 15) | yes | int count | fine | CLEAN-14
persons_60_and_over | R60, 0 / 1 / 2 or more | yes | ordered, order checked, open end a level | fine | CLEAN-14
persons_65_and_over | R65, same | yes | ordered, checked | fine | CLEAN-14
multigenerational_household | MULTG yes/no | yes | category | fine | CLEAN-14
limited_english_household | LNGI, someone 14+ speaks only English or very well | yes | category, 2 levels | fine | CLEAN-14
household_language | HHL, 5 language groups | yes | category | fine (a national-origin proxy; see issue A) | SEL-1
tenure | TEN, owned with mortgage / free and clear / rented / no cash rent | yes | category | fine | CLEAN-12
units_in_structure | BLD, 10 levels incl. mobile home, boat/RV | yes | category, unordered (partial order, noted) | fine | CLEAN-14
vehicles | VEH 0-6, "6 or more vehicles" | yes | ordered, checked | fine | CLEAN-14
household_income | HINCP x ADJINC/1e6, cash income of all members over the past 12 months; includes public assistance (PAP) and SSI, EXCLUDES SNAP (noncash; the PA item "is not intended to capture ... SNAP", Census user note 2022-11) | yes (window W) | float, survey year's dollars; allocated on 34% of 2024 households (any member's FPINCP); no sign the hot-deck uses FS (section 3, point I) | fine for leaks; CLEAN-21 open (issue C) | LEAK-10 not triggered; CLEAN-21
gross_rent_monthly | GRNTP x ADJHSG, monthly gross rent; blank for owners and no-cash renters (74%) | yes | float, structural missing kept | fine | CLEAN-10
owner_costs_monthly | SMOCP x ADJHSG, selected monthly owner costs; blank for renters (28%) | yes | float, 0 = "None" kept | fine | CLEAN-10
workers_in_family | WIF 0 / 1 / 2 / 3 or more; blank for non-family households (34%) | yes (window W) | ordered, checked; blank = not a family, missing | fine | CLEAN-14
work_experience_householder_spouse | WKEXREL 1-15, FT / less than FT / none for householder and spouse; codes 10-15 name the householder's sex | yes (window W) | category, nominal (two dimensions; correctly not ordered); blank for non-family | fine; ENCODES SEX for codes 10-15: recode if sex is dropped | SEL-1 (issue A)
householder_age | AGEP, top-coded per state (values 93-97 are the state top-code means) | yes | int; top-code named in the notes | fine; protected ground but a SNAP eligibility factor (issue A) | SEL-1, CLEAN-14
householder_sex | SEX | yes | category | question for the curator (issue A) | SEL-1
householder_race | RAC1P, 9 groups | yes | category; CODING BREAK at 2020: "Two or More Races" 1.7-1.9% of householders in 2014-2019, 8.6-8.7% in 2021-2024, "White alone" 80% to 73% | question (issue A); note the break if it stays (issue D) | SEL-1, CLEAN-21 by analogy
householder_hispanic_origin | HISP, 24 detailed origins | yes | category | question (issue A: national origin) | SEL-1
householder_education | SCHL 1-24 | yes | ordered, code order = dictionary order; "GED or alternative credential" sits above "Regular high school diploma" (the Census tabulates both as "high school graduate (includes equivalency)", so the codebook does not rank them) | fine, minor note | CLEAN-14
householder_marital_status | MAR 1-5 | yes | category | fine | CLEAN-12
householder_citizenship | CIT 1-5 | yes | category; 2014-2019 words mapped to 2024 wording, same codes | fine; a SNAP eligibility factor (7 CFR 273.4), not a 272.6 ground | SEL-1
householder_nativity | NATIVITY native / foreign born; a function of CIT (1-3 native, 4-5 foreign born) | yes | category; coarsening of CIT, not an exact copy | fine (adds nothing once CIT stays) | CLEAN-5
householder_place_of_birth | POBP, 229 levels, decoded per year (2017's list for 2014-2016 plus codes 208 and 463) | yes | category; 2014-2016 lists checked: only 208 old, 463 relabelled, ten countries split out from 2017 | fine; question (issue A: national origin) | CLEAN-12, SEL-1
householder_ancestry_reported | ANC recode: Single / Multiple / Unclassified / Not reported; code 8 (suppressed, 2018-2019 only) made missing | yes | category; holds HOW ancestry was reported, not the ancestry; "Not reported" rises 10.9% (2014) to 13.3% (2024) | fine; not a national-origin item (issue A) | CLEAN-10
householder_english_ability | ENG 1-4 reversed, blank = speaks only English (householders are 15+) | yes | ordered Not at all < Not well < Well < Very well < Speaks only English; checked against the dictionary | fine | CLEAN-14
householder_disability | DIS | yes | category | fine; protected ground but a SNAP eligibility factor (issue A) | SEL-1
householder_hearing_difficulty | DEAR | yes | category | as above | SEL-1
householder_vision_difficulty | DEYE | yes | category | as above | SEL-1
householder_cognitive_difficulty | DREM | yes | category | as above | SEL-1
householder_employment_status | ESR 1-6, at the interview (reference week) | yes | category | fine | CLEAN-12
householder_hours_per_week | WKHP 1-98, 99 = "99 or more"; blank = did not work in the past 12 months (35.5%) | yes (window W) | float; 99 cap holds 0.1% of rows | fine (blank means 0 hours; missing is acceptable) | CLEAN-10, CLEAN-14
householder_class_of_worker | COW 1-9; blank for NILF who last worked 5+ years ago | yes | category | fine | CLEAN-12
householder_occupation | OCCP, decoded per year (2010-based list to 2017, 2018 list from 2018); 656 levels | yes | category; 2014-2016 codes all in 2017's list (labels differ only in case and line wraps), 2018-2024 lists identical but for wording | fine | CLEAN-12
householder_military_service | MIL 1-4; blank under 17 (0.01%) | yes | category | fine | CLEAN-12
householder_public_coverage | PUBCOV, Medicare, Medicaid/means-tested or VA coverage at the interview | yes | category; Medicaid part partly assigned by the Bureau's coverage edit (12% of householders with Medicaid in 2024, FHINS4C), from public assistance, SSI, parents and foster status, never from FS | fine; strong (under 65: 40.8% SNAP with, 5.3% without) | LEAK-10 not triggered; USE-6
householder_poverty_ratio | POVPIP, family income over the poverty threshold, %, 501 = "501 or more"; official money income, excludes SNAP | yes (window W) | int; 33.4% of rows at the 501 cap (SNAP 1.6% there) | fine; minor CLEAN-14 open-end note | LEAK-10 not triggered; CLEAN-14
householder_gave_birth_past_year | FER yes/no; blank for males and outside 15-50 (79.6%) | yes | category; blank encodes male for ages 15-50 | fine; ENCODES SEX: recode if sex is dropped | SEL-1 (issue A)
snap_received (target) | FS 1 Yes, 2 No; FFSP 1 rows dropped | label | category No/Yes | fine | CLEAN-25

Not shipped, checked:
* PAP, SSIP (other cash benefits), HINS4 (Medicaid): not leaks by any LEAK rule (none is a part, consequence or
  encoding of FS). TableShift's list (ACS_FOODSTAMPS_FEATURES) does not have them either. Their content is already
  in household_income (PAP, SSIP) and householder_public_coverage (HINS4). See issue E.
* WKW / WKWN (weeks worked): dropped because WKW is 6 bands to 2018 and WKWN a number 1-52 from 2019. The bands are
  defined on weeks (50-52, 48-49, 40-47, 27-39, 14-26, under 14), so WKWN maps onto them exactly; TableShift has WKW.
  See issue D.
* NWLA, NWLK ("UNEDITED - See ESR"), WRK: their content is in ESR. Fine.
* DIVISION, REGION (functions of state), PUMA (redrawn 2022), weights (MET-16), allocation flags, SERIALNO: fine.

**2. PROBLEMS, RANKED (principles.md: rank, then strength, then size)**
A. [P1; SEL-1 (Must) under the Tensions row "a factor the actor may no longer use", as the rais panel extended it;
   curator's call, builder's issue 2] The protected grounds, and an incomplete drop.
   Evidence:
   * 7 CFR 272.6(a) (Cornell LII, read 2026-11-09): state agencies "shall not discriminate against any applicant or
     participant in any aspect of program administration ... for reasons of age, race, color, sex, disability,
     religious creed, national origin, or political beliefs."
   * Sex survives the builder's option B. household_type (HHT 2-7: "Male/Female householder") names the
     householder's sex for 48.99% of rows; work_experience_householder_spouse codes 10-15 for 14.93% (a subset of
     HHT 2-3); householder_gave_birth_past_year is blank for every male householder (the item is asked of women
     15-50), so blank at ages 15-50 means male. Together they name the sex of 69.4% of householders, with 100.0%
     agreement with householder_sex (2.5M rows). Dropping householder_sex alone removes nothing for those rows.
   * Ground by ground (my reading, for the curator):
     - sex, race (RAC1P), Hispanic origin (HISP, an origin by country), place of birth (POBP): grounds of 272.6
       with no role in SNAP eligibility. Under the extended stance they go.
     - ancestry: the shipped column is the ANC RECODE (Single / Multiple / Unclassified / Not reported), how the
       person answered the ancestry question, not the ancestry. It names no national origin; dropping it is not
       required by 272.6 (the builder's B drops it).
     - age, disability (DIS, DEAR, DEYE, DREM): grounds of 272.6, but SNAP's own rules use them (households with
       an elderly (60+) or disabled member: 7 CFR 271.2 definitions, no gross income test and a medical deduction,
       273.9; general knowledge, the CFR sections not re-read). That is the fact that sets them apart, like wioa's
       (the actor's own adjustment model uses the factors), unlike rais (where age had no such role and went).
     - citizenship (CIT): not a 272.6 ground, and an eligibility rule (7 CFR 273.4). Keep. nativity is a function of
       CIT (codes 1-3 native, 4-5 foreign born), so dropping it changes nothing while CIT stays.
     - language (household_language, limited_english_household, householder_english_ability): proxies of national
       origin, not grounds; SNAP's bilingual rules (7 CFR 272.4(b), not re-read) make language a factor the agency
       serves by. Keep, with a note.
   * Cost, measured (this panel; LightGBM 300 trees, 127 leaves, 2 seeds, the shipped train/test of the 2024 and
     2022 windows):
       window | all | B (builder: no sex, race, Hispanic, ancestry recode, place of birth) | B + sex removed from
       HHT, WKEXREL, FER
       2024   | 0.91333 | 0.91417 (+0.0008) | 0.91426 (+0.0009)
       2022   | 0.91015 | 0.90993 (-0.0002) | 0.90982 (-0.0003)
     Seed spread 0.0001-0.0004. The grounds carry no measurable signal beyond the other items; the 2024 gain is the
     high-cardinality levels (229 places of birth, 24 origins) overfitting an untuned model.
   Remedy (mildest that completes B; for dataset.py):
     - drop householder_sex, householder_race, householder_hispanic_origin, householder_place_of_birth (and, by
       choice, householder_nativity and householder_ancestry_reported);
     - recode household_type to 4 levels: "Married couple household", "Other family household: Householder, no
       spouse present", "Nonfamily household: Householder: Living alone", "... Not living alone" (merge HHT 2+3,
       4+6, 5+7);
     - recode work_experience_householder_spouse to 12 levels (merge 10+13, 11+14, 12+15: "Householder worked FT;
       no spouse present", etc.);
     - householder_gave_birth_past_year: blank -> "No (or not asked)" (true for men; the item is not asked over 50).
       "Yes" (1.12% of rows) still names a woman; drop the column instead if the curator wants no trace (it is a
       sex-specific event, not a ground).
     The recodes lose nothing but the sex. Without them option B is a label on the notes, not a removal.
   Decision for the curator: A (keep all), B as completed above, or C (also age/disability; I argue against C: the
   programme's own rules use them).

B. [P2/P4 context; LEAK-10 window clause; feeds the builder's issue 1 (SEL-7), no column change now] Window W.
   household_income, householder_poverty_ratio, householder_hours_per_week, workers_in_family and
   work_experience_householder_spouse summarise the same "past 12 months" that defines the label. Under the shipped
   framing (the interview is the prediction point, the label is concurrent) this is the SEL-7 question, not a column
   leak. It becomes a LEAK-10 Must the moment the task is framed forward (predict receipt in a later period, or
   "before the household applies"): the income of the window moves with the receipt it may have qualified or
   followed. If the curator keeps the dataset under option A or B of issue 1, nothing changes; say in the notes that
   the features and the label share one window.

C. [P7; CLEAN-21 (Should); builder's issue 4] Dollars of ten survey years in one column.
   Evidence: median household_income rises 55,463 (2014) to 84,266 (2024) in the shipped frame; CPI-U rose about
   32.5% over the same years. The builder's exception rests on POVPIP being the comparable measure. Counter: the
   Census Bureau itself puts pooled years into one year's dollars (the 5-year PUMS ADJINC carries the inflation to
   the final year; general knowledge, not read here), so a conversion from the measuring body exists, which is
   CLEAN-21's own wording. Measured (same models as A): deflating household_income, gross_rent_monthly and
   owner_costs_monthly to 2024 dollars with CPI-U annual averages (values from memory, not fetched) moves ROC AUC
   +0.0007 (2024 window: 0.91333 -> 0.91405) and +0.0006 (2022: 0.91015 -> 0.91072), the same sign on 4 of 4 fits,
   seed spread up to 0.0003. Small, consistent, cheap (ten constants).
   Remedy: option B of the builder's issue 4 (one scale, 2024 dollars), with the deflator from the Census Bureau's
   5-year ADJINC factors or BLS CPI-U-RS, the source named; or keep A as a recorded exception. I recommend B: the
   fix is cheap and safe, and the measurement favours it.

D. [P7; CLEAN-21/CLEAN-22 (Should), CLEAN-14] Smaller cleaning points.
   D1. Weeks worked (WKW) is left out because it is 6 bands to 2018 and a number (WKWN 1-52) from 2019. The bands
       are defined on weeks (50-52, 48-49, 40-47, 27-39, 14-26, under 14), so WKWN maps onto them exactly, as
       IPUMS's intervalled weeks variable does; TableShift ships WKW. Remedy: one ordered column of the six bands
       (blank = did not work in the past 12 months, missing). The 2019 questionnaire change (a two-step weeks
       question) is a level shift to name in the notes. Cheap; CLEAN-21 puts a changed scale on one scale rather than
       dropping it.
   D2. householder_race has a coding break at 2020: "Two or More Races" 1.7-1.9% of householders in 2014-2019,
       8.6-8.7% in 2021-2024; "White alone" 80% -> 73%; "Some Other Race alone" 2.6% -> 4.0% (the Bureau's improved
       coding of write-ins from 2020). Every test window is after the break; the 2022 window trains on one
       post-break year. No crosswalk exists: name it in the notes if race stays (moot under issue A's B).
   D3. householder_education: "GED or alternative credential" is ordered above "Regular high school diploma" by
       the code order. The Census tabulates both as "high school graduate (includes equivalency)": the codebook does
       not rank them. Keep the order (one line through every level is needed) and say in the notes that the two are
       one rung. Very minor.
   D4. householder_poverty_ratio: 33.4% of rows sit at 501 ("501 percent or more"). CLEAN-14's open-end clause
       reads literally for an ordered category; for a 502-level near-continuous ratio the number is the expert form,
       and the notes already name the cap. Fine as is; listed so the curator sees the departure is deliberate. The
       same holds for householder_hours_per_week (99 = "99 or more", 0.1%) and householder_age (state top-codes).

E. [P7 / notes; CLEAN-22 (Must) reading] PAP, SSIP and HINS4: the notes give the wrong kind of reason.
   The notes say they are "Not read, as other benefits of the same 12 months". No LEAK rule reads that way: none is
   a part, consequence or encoding of FS. Receipt of cash assistance or SSI is a cause of SNAP eligibility
   (categorical eligibility), and the content is already in the shipped features: household_income includes PAP
   and SSIP, householder_public_coverage includes HINS4 (Medicaid is most of public coverage under 65). So either
   they are inputs (USE-6: known at the interview; an agency running integrated eligibility holds them) or the
   shipped columns carry the same problem. The builder measured +0.007 ROC AUC with them (0.9135 -> 0.9208).
   Remedy (mildest): reword the reason to what it is, a feature-set choice ("TableShift's list; their content enters
   household_income and householder_public_coverage") so no reader takes it for a leak call; or add them back. The
   curator's call; I see no rule that keeps them out.

F. [P5; PROV-13 (note)] Allocated feature values are kept; the numbers belong in the notes.
   2024, households with a reported FS: some member's income allocated in 33.6% (438,872 of 1,306,887), the
   householder's total income in 25.1%, the householder's public coverage recode in 18.5%, public assistance in
   13.2%; age 0.6%, race 0.5%, sex 0.01% (FPINCP, FPUBCOVP, FPAP, FAGEP, FRACP, FSEXP of the 2024 person file). The
   SNAP share is higher where income is allocated (13.2% vs 8.6%). Keeping the Bureau's allocations is standard
   and the flags are not inputs; the check in section 3 (I) closes the builder's "whether FS enters the income
   hot-deck" with a measurement. Remedy: a sentence in the notes with these numbers.

**3. LEAK CHECKS THAT FOUND NOTHING (results, with evidence)**
L1. Income and poverty carry no SNAP. household_income (HINCP) is the sum of cash income components; SNAP is a
    noncash benefit, excluded: the Census Bureau's user note on public assistance in the 2021 ACS (2022-11) says the
    PA question "is not intended to capture assistance from non-cash benefits, like ... (SNAP)", and Census briefs
    define public assistance income as TANF and General Assistance, excluding SSI and SNAP. POVPIP compares money
    income with the official thresholds, which count no noncash benefit. LEAK-10 not triggered.
L2. Public coverage is not assigned from FS. The Bureau's logical coverage edit assigns Medicaid (FHINS4C) to
    children and citizen parents of public-assistance recipients, foster children and SSI recipients in states that
    enrol them automatically (IPUMS USA, "Health Insurance Variables in the ACS"); no rule reads FS. 12% of
    householders with Medicaid in 2024 got it from the edit (20,089 of 170,178). Weak residual, not measured: a SNAP
    application can lead to Medicaid enrolment (express-lane and targeted enrolment), so a few coverage values may
    be consequences of receipt. Not enough to act on; a note at most.
I.  The income hot-deck shows no sign of FS (decisive experiment, EV-1). 2024 file, households with a reported FS,
    split by whether any member's income was allocated (33.6%):
      reported income:  SNAP 8.61%, ROC AUC of -POVPIP 0.855, of -HINCP 0.814
      allocated income: SNAP 13.23%, ROC AUC of -POVPIP 0.744, of -HINCP 0.687
    LightGBM on half the households, scored on the other half: the two income columns add +0.0143 ROC AUC on
    reported-income rows and +0.0015 on allocated-income rows (trained on reported rows only: +0.0153 and -0.0059).
    If the hot-deck matched donors on FS, imputed income would carry FS and its worth would not collapse. It
    collapses: imputed incomes are noise about SNAP, not an encoding of it. LEAK-10 not triggered.
L3. Misreported benefits in public assistance. The Bureau's user note 2022-11 found stimulus and advance child tax
    credit payments reported as public assistance in 2019-2021 (bunching at stimulus amounts), not SNAP. That
    inflates PAP inside household_income for some 2021 households: a measurement-quality note, not a target
    encoding. Not acted on.
L4. Missingness caused by the outcome: none. The blanks follow structure (gross_rent_monthly and
    owner_costs_monthly by tenure, workers_in_family and work_experience by non-family, householder_hours_per_week by
    no work in 12 months, class_of_worker and occupation by last work over 5 years ago, gave_birth by sex and age,
    ancestry 8 by the 2018-2019 suppression). None is set by FS.
L5. Ids and late fields: none. SERIALNO is dropped; no item is collected after the interview; no allocation flag is
    an input; the dropped FFSP rows are rows without a reported label (CLEAN-15, USE-7), 1.7-3.1% a year.
L6. Decoding: the dictionaries of 2014-2024 agree on every code of the 31 items decoded with the 2024 words (the
    only differences are wording: "no wife present", "< FT", "Born in the U.S.", truncated text-file labels); ANC
    code 8 exists only in 2018-2019 and is made missing. POBP and OCCP are decoded per year; 2014-2016 OCCP codes
    all exist in the 2017 list; 2017 and 2018 share 379 OCCP codes, 27 with another label, which the per-year
    decoding handles. ENG's blank is "speaks only English" (97%+ of those householders live in English-only
    households).

**4. JUDGMENT RECORD**
Verdict (columns): ship after changes, once the curator settles issue A.
Validity: SEL-1 open, curator's call (issue A); if B, complete it (recode HHT, WKEXREL, FER). LEAK-10 checked on all
  43 inputs, not triggered (L1, L2, I); window W named for the SEL-7 issue (B). USE-6: PUBCOV and income stay.
Value: no column changes the probe picture (grounds cost <= 0.0003 ROC AUC).
Quality: CLEAN-21 departure measured (+0.0006/+0.0007 with one scale; issue C, recommend converting); WKW
  harmonisable (D1); race break, GED rung, open ends noted (D2-D4); notes' reason for PAP/SSIP/HINS4 (E);
  allocation numbers for the notes (F).
For the curator: issue A (which grounds leave), issue C (one dollar scale), issue E (wording or add back).

Sources read (2026-11-09): 7 CFR 272.6, https://www.law.cornell.edu/cfr/text/7/272.6 ; Census user note 2022-11,
https://www.census.gov/programs-surveys/acs/technical-documentation/user-notes/2022-11.html ; Census ACS brief on
public assistance receipt, https://www.census.gov/library/publications/2014/acs/acsbr13-13.html ; IPUMS USA ACS
health insurance edits, https://usa.ipums.org/usa/acs_healthins.shtml ; TableShift acs.py,
https://raw.githubusercontent.com/mlfoundations/tableshift/main/tableshift/datasets/acs.py ; the PUMS data
dictionaries 2014-2024 as downloaded for the build.

</details>

<details><summary>Split audit</summary>

SPLIT AUDITOR REPORT: acs_food_stamps_2014_2024 (folder acs_food_stamps_2014_2024_1m), 2026-11-09

VERDICT: right with notes.
Temporal by survey year is the right regime for the agency framing (A): the actor refits on past survey years and
scores households of a later year, and no household recurs. The windows, the train sides, the 50% floor and the
2020 exclusion all check out. Two Should-level notes for P4: the no-gap reasoning in splits_comment states the wrong
fact, and the training history crosses the 2020 break without saying so. Both are fixed by notes; a 1-year gap is the
curator's alternative and is feasible. If the curator picks framing B (survey-office imputation, issue 1), the split
has to change to IID within a year (see 5).

Judgment record:
  Validity: SPLIT-1 holds for framing A (temporal); SPLIT-2/3 temporal, no grouping needed (SPLIT-13: households
  never recur, state is a known entity); SPLIT-9 holds (no shortcut: no entity links across years); SPLIT-10 applied
  with a wrong stated fact (note 1); SPLIT-14 holds (oldest window 68.7% of rows, 58.8% with a 1-year gap);
  SPLIT-20 break not written down (note 2); SPLIT-21 respected (history not decided from scores).
  For the curator: gap or no gap (note 1), and the split under framing B (5).

**WHAT WAS CHECKED (numbers)**

Shipped splits (the participant kit's splits and data): 3 repeats x fold 0, newest first.
  window   test year  test rows  test Yes   train rows  train Yes  train years (rows)
  0        2024       500,000    10.16%     1,000,000   10.74%     2014-2019, 2021-2023 (107k-117k each)
  1        2023       500,000    10.58%     1,000,000   10.76%     2014-2019, 2021-2022 (121k-131k each)
  2        2022       500,000    10.69%     1,000,000   10.77%     2014-2019, 2021 (140k-146k each)
  No row on both sides; every train row strictly earlier than its window; each window has its own train side.
Full data (FFSP 0, 12,459,241 households): per-year rows 1.197M (2014) to 1.307M (2024); Yes 12.00, 11.54, 11.14,
  10.53, 10.01, 9.31 (2019), 10.94 (2021), 10.69, 10.58, 10.16%. Share of rows before each window: 2022 68.7%,
  2023 79.1%, 2024 89.5% (SPLIT-14 floor met). With a 1-year gap: 58.8%, 68.7%, 79.1% (still met).
Time column: survey_year is the ACS data year; interviews run January to December, and FS asks about the 12 months
  before the interview, so a year's reference periods span about two calendar years and overlap the neighbouring
  survey year's.
Each test window is a whole survey year, so there is no season-shaped window.

Alternative splits (LightGBM 500 trees, lr 0.05, 63 leaves, 1 seed; 1M train rows sampled from the named years,
the same 300k random test households of the year; raw codes from the build's per-year files;
script and outputs in the run's work files):

  ROC AUC (mean prediction vs observed Yes)   test 2022          test 2023          test 2024
  shipped: all earlier years                  0.9120 (.101/.107) 0.9109 (.101/.106) 0.9148 (.098/.102)
  1-year gap: years <= Y-2                    0.9093 (.086)      0.9099 (.097)      0.9135 (.097)
  pre-COVID only: 2014-2019                   0.9093 (.086)      0.9075 (.083)      0.9099 (.079)
  post-2020 only: 2021..Y-1                   0.9150 (=2021)     0.9130             0.9162
  newest year only: Y-1                       0.9150             0.9138             0.9173
  within-year IID: other households of Y      0.9158             0.9142             0.9171
  The signs agree in all three windows. A 300k test set gives an AUC SE of about 0.0006, and paired differences
  have a smaller SE.

**PROBLEMS, RANKED (principles.md: all P4; Should before notes)**

1. P4, SPLIT-10 (Should): the no-gap argument states the wrong fact. The newest training year was not released at
   the window's start.
   Evidence: splits_comment says the ACS releases a year's 1-year PUMS "in the autumn of the next year, within the
   one-year step of the time column, so no gap is set (as for ... ames_housing)". The 2023 1-year PUMS came out on
   17 October 2024 (Census Bureau 2023 release schedule; the 2024 file is listed for 16 October 2025, not verified).
   So a model used during survey year Y has year Y-1's labels only from mid-October of Y. For about 9.5 of the 12
   months, the newest file is Y-2. ames_housing is not alike: a sale is recorded within its month, before the next
   window starts. Here the delay runs about 9.5 months into the test step, so SPLIT-10's no-gap condition "the
   time column's smallest step is longer than the delay" is not met.
   Why no gap can still stand: the amendment of 2026-11-04/05 (lt_vehicle_loan_default_prediction) allows no gap
   when there is no selection by the outcome. Here a year's labels are all released together and final, so the
   newest training rows are not the fast ones. The overlap of reference periods shares only period-level conditions
   (e.g. emergency allotments in force), not an entity, so SPLIT-9 has no shortcut. But the amendment requires the
   notes to give what the not-yet-known newest year adds at equal training size. Measured: +0.0027 (2022), +0.0010
   (2023), +0.0013 (2024) ROC AUC for no gap over a 1-year gap. college_scorecard set its gap for a publication lag
   because the lag cost R^2 0.05 there; here the effect is about 20 times smaller.
   Mildest remedy: keep no gap and rewrite the gap sentences of splits_comment. They should say that the Y-1 file
   is released in mid-October of Y, that every label of a year arrives together and final (no selection), and that
   the newest year adds 0.001-0.003 ROC AUC at equal training size. Alternative for the curator: the use case says a model fit on past survey
   years "ranks households of the next year", which describes a model applied during year Y before Y-1's file
   exists, and so favours a gap:
   `TemporalSplits(window=1, unit="unique", n_windows=3, gap=1)` with `Temporal(..., gap=1, gap_unit="years")`.
   The windows then train on 2014-2019 / 2014-2021 / 2014-2022, which is 58.8% / 68.7% / 79.1% of the rows, above
   the floor. A gap of one distinct value equals one calendar year for 2022, since 2020 is absent.

2. P4, SPLIT-20 (Should): the training history crosses the 2020 break, and the notes do not say why it is kept.
   Evidence: the Yes share falls 12.0% -> 9.3% over 2014-2019, then jumps to 10.9% in 2021 (pandemic; SNAP
   emergency allotments from 2020 until the February 2023 benefit month in 32 states and DC, earlier in the other
   18). A model trained on 2014-2019 alone under-predicts the test years' Yes share by 2.1-2.4 points (mean
   prediction 0.079-0.086 against 0.102-0.107) and loses 0.003-0.005 ROC AUC against the shipped history. Training
   on 2021 onward, or on the newest year alone, gains +0.0014 to +0.0030 over the shipped all-years side. The
   splits_comment and the History bullet say only that 2020 has no regular file.
   Not a reason to cut the history: SPLIT-21 bars deciding it from these three windows. Dropping 2014-2019 would
   also leave 4 survey years, so three yearly windows would train on 25-75% of the rows and break SPLIT-14's floor.
   The full history is what the floor allows.
   Mildest remedy: a sentence in the History bullet or splits_comment. It should say that 2014-2019 precede the
   COVID break and its emergency allotments, give the measured label shift (pre-2020-only training under-predicts
   the Yes share by about 2 points), and state that the years are kept because three yearly windows need them
   (SPLIT-14) and the survey year is a feature. No re-split.

3. P4, SPLIT-20 (note): two of the three test years are atypical.
   Evidence: 2022 lies inside the emergency-allotment period for most states. In 2023 the allotments ended (after
   February) and the Medicaid continuous-enrollment unwinding began (April 2023), which moves PUBCOV, a feature.
   2024 is the first year after both. Test Yes shares are 10.69 / 10.58 / 10.16%. The windows cannot be widened or
   moved: they are the newest data, and older windows are just as atypical (2021) or cross the break.
   Remedy: one sentence in splits_comment naming the regime change the test years span. No re-split.

4. P4, SPLIT-13 / SPLIT-4 (no problem; recorded): state is a feature, not a group.
   Evidence: households never recur. SERIALNO is per year, and the ACS keeps an address out of the sample for 5 years
   after it is interviewed (Census design documents and OMB supporting statements). After 5 years an address can be
   re-sampled. A rough estimate: at about 2.5% of addresses per year, 10-15% of a test year's addresses were eligible
   and sampled 5-10 years earlier, and the 1M train side keeps 9-12% of those years, so about 1-1.5% of test rows
   could share an address with a train row. Most would be a different occupant 5+ years later, and nothing links
   them. The probes show 0.0% exact copies across the split and 0.4% of test rows in near-copy clusters with
   training rows. No action.
   State: all 51 states are in every train side (100% of test rows' state seen). The actor, a state SNAP agency,
   predicts for its own state, so state is a known entity and stays a feature (SPLIT-4). A held-out-state or
   held-out-division split (TableShift's) tests a new state, which no actor needs; the curator has already rejected
   it. State-level policy drift is real and is part of the task:
   - per-state Yes share changes: 2019->2022 mean +1.01 points, SD 1.13, range -0.89 to +4.40 (CA largest);
     2022->2024 mean -0.63, SD 0.75, range -2.25 to +0.82;
   - 4 of the 5 largest 2022->2024 falls (MS, MT, GA, AR; LA is the fifth) are among the 18 states that ended the
     allotments before February 2023;
   - the shipped model's per-state residual (observed minus mean prediction) has an SD of 0.8-1.0 points, worst
     |4.8| points (Alaska, 2023); the mean within-state AUC (0.911-0.916) equals the pooled AUC.
   A temporal split by year is what exposes this drift to the model, as the actor would meet it.

5. P4, SPLIT-1 (conditional, for issue 1): under framing B the split is wrong.
   If the curator re-frames the task as the survey office's item imputation (builder issue 1, option B), the
   actor fills a year's blank FS answers from the same year's respondents (hot-deck donors of the year), so the
   split that mirrors it is IID within the survey year, not temporal. Measured: within-year IID scores
   0.9158 / 0.9142 / 0.9171 against the shipped 0.9120 / 0.9109 / 0.9148, so temporal would underrate by
   0.002-0.004. The imputed rows are not missing at random, which no split can simulate. Under framing A the shipped
   split stays.

Checked and fine:
- 2020 left out: the experimental release with experimental weights and a disrupted collection (claims 2).
- PUMA dropped: PUMA has no single meaning across the 2022 redraw; state carries the geography, constant in every
  year.
- Windows: 3 (SPLIT-15 default for this size), one survey year each (horizon 1 year, the yearly refit, SPLIT-12).
- Expanding train side (SPLIT-11), each window with its own train side (SPLIT-14).
- No training row's label is set after its prediction point by an event of the test row's entity (SPLIT-9).
- survey_year is a feature and the test value is always unseen. Trees treat it as the newest training year,
  harmless.
- The rows-per-period imbalance (probe 13, z +49) comes from the row budget (500k test rows against about 110-146k
  per training year), not from censoring; the Yes rate is in band.

Sources: Census Bureau 2023 ACS data release schedule
(https://www.census.gov/programs-surveys/acs/news/data-releases/2023/release-schedule.html; 1-year PUMS 17 Oct 2024);
ACS Design and Methodology ch. 4 (https://www.census.gov/content/dam/Census/library/publications/2010/acs/acs_design_methodology_ch04.pdf)
and the 2020 ACS OMB Part B (https://omb.report/icr/201910-0607-001/doc/95490801): no address in sample more than
once in 5 years; USDA FNS emergency allotment sunset (https://fns-prod.azureedge.us/sites/default/files/resource-files/snap-sunset-ea.pdf)
and CBPP (https://www.cbpp.org/blog/end-of-snaps-temporary-emergency-allotments-resulted-in-substantial-benefit-cut):
EAs ended after February 2023 in 32 states and DC, earlier in 18.

</details>

<details><summary>Domain practitioner</summary>

DOMAIN PRACTITIONER REPORT: acs_food_stamps_2014_2024 (folder acs_food_stamps_2014_2024_1m), 2026-11-09

VERDICT
Fit as declared (state SNAP agency or outreach programme ranking households): NONE. The agency already holds the label
for every household in its caseload, outreach targets eligible households that do NOT receive SNAP (the "No" class), and
the inputs are survey answers it never sees: USE-5 (another quantity than the one the actor acts on), SEL-7 applies.
Fit under the one actor who predicts exactly this label from exactly these inputs (the Census Bureau's item allocation
of the FS answer, FFSP 1, 1.7-3.1% of households every year): APPROXIMATE, and the dataset is not yet built for that
actor (use case text, dropped benefit items, metric). Metric: PARTLY scores the decision; for the imputer I would pick
log_loss (MET-8), for the outreach actor no metric on this label scores the decision.
Recommendation on builder issue 1: C unless the curator takes item imputation as the fact that sets this case apart;
if so, B with the four changes under "What an expert would change". A (ship as is) I would not use.

**1. THE ACTORS, ONE BY ONE (first person)**

1a. A state SNAP agency (and an outreach NGO working on its lists)
- Inputs: I do not have one ACS interview's answers for anyone. I have my caseload (who receives SNAP, every month), and
  through data sharing the Medicaid, WIC and sometimes UI wage lists. Outreach today is list matching: "Medicaid enrollees
  not on SNAP" (North Carolina's FNS team builds a report of Medicaid enrollees and Benefits Data Trust cross-references
  it against people not receiving FNS benefits; South Carolina DSS matches Medicaid and SNAP lists monthly; SNAP and
  Medicaid agencies of 43 states share data). I would never hold ancestry, place of birth, occupation, English ability,
  hours worked, vehicles or the householder's fertility for a household that has not applied.
- The one input I WOULD have, Medicaid coverage (HINS4), is the one the build drops ("not read, as other benefits"). PAP
  and SSI are also in state systems. So the input set is the reverse of mine: it keeps answers I never see and drops the
  enrollment I match on. The builder's "administrative-like items" set (0.888 vs 0.916) still contains survey income and
  the poverty ratio, which I only get at application.
- Target: I do not need P(receives SNAP): I know it from my records for every household. What I act on is P(eligible
  and not participating). A ranking by P(reported receipt) puts current recipients at the top, households that need no
  outreach. The declared use_case sentence ("ranks households ... by how likely they are to receive SNAP, to target
  outreach") is internally inconsistent for this reason.
- "Look-alike" reading (households that resemble recipients but are not enrolled): P(receipt | x) = P(eligible | x) *
  P(take-up | eligible, x). The groups with low take-up (FNS: 78% of eligible people participated in FY2020, the elderly
  below average) get LOW scores precisely because they do not take up, so the look-alike score down-ranks the groups
  outreach is for. And ROC AUC on this label rewards putting reported recipients above reported non-recipients, i.e.
  it penalises any model that scores the eligible non-participants high (they are counted as false positives).
- Label noise is where I would act: 35% of true recipient households do not report receipt in the ACS (Meyer, Mittag
  and Goerge, NBER WP 25143), and survey estimates understate participation most for single parents, non-white and
  low-income households; false negatives and positives vary with household characteristics (same abstract). The "No"
  class of the low-income households I would screen is thus a mix of eligible non-participants, under-reporters and
  ineligibles, with no way to tell them apart in the data.
- One row is one Census household, not one SNAP household (people who buy and prepare food together); a Census
  household can hold more than one SNAP unit. Minor next to the above.
- Would I use this model: no. I would distrust it the moment I saw that its top decile is my own caseload.
=> SEL-7 applies in full, and more strongly than in cdc_diabetes_health_indicators: there the physician at least lacked
   the diagnosis of an undiagnosed patient; here the agency holds the label of every participant in its own records.
   Fit none (USE-2, USE-5 last sentence "a label checked and found to be another quantity ... still fails").

1b. The Census Bureau imputing the FS item for households that leave it blank (builder's option B)
- Inputs: I have every answer of the interview, at the moment I edit the file: yes, all 43. I also have more than the
  dataset ships: PUMA/tract geography, the other benefit items (PAP, SSIP, HINS4), unrounded and un-top-coded amounts,
  the response mode, the other persons' items. The build's exclusion of PAP, SSIP and HINS4 removes inputs I certainly
  have (USE-6: anything known at the prediction point is a legitimate input; the builder measured +0.007 ROC AUC).
- Target: exactly the quantity I fill: the household's own report of the item (my donors are reporters). The 35%
  under-reporting is NOT a label gap for me: I impute the report, not the truth (correcting toward administrative truth
  is a separate research programme with linked data, Rothbaum, Fox and Shantz 2021; Davern et al. 2019).
- Output: a probability I draw from (or a donor). The imputed SNAP share in each cell must match, so I need calibrated
  probabilities, not a ranking.
- Row: one household with a blank FS: one row, one decision. Matches.
- Test data: in practice my non-respondents of the SAME year, imputed with that year's donors, not next year's
  households. The temporal split tests a harder, drifting version (a model fit on earlier years, applied before the new
  year's donors are used); acceptable with a note, but a within-year split is the processing reality (SPLIT question
  for the split auditor). And the benchmark can only score respondents: non-respondents have no label, and Celhay, Meyer
  and Mittag (NBER WP 29184) find error rates are higher among imputed observations, so MAR is an assumption, not a fact.
- Today I use a hot-deck (ACS item-allocation definitions: within-household and nearest-neighbour matrices populated
  by donors), not a learned model; whether a learned model replaces it is an open question the Bureau studies (a 2026
  AAPOR presentation "model based or hot deck" by Census staff exists; I could not read its content, so I cite only its
  existence). A learned imputer is a candidate replacement for a real, recurring decision, not an invented one.
- Would I use it: as a candidate allocation model, yes, if it is calibrated per year and per state and preserves the
  published cross-tabulations (S2201 tabulates SNAP households by race and Hispanic origin of the householder and by
  disability).
=> Fit approximate: the decision, the inputs, the label and the row match; the gaps are the within-year reality vs the
   temporal split, scoring on respondents only (MAR), the hot-deck status quo, and the dropped benefit items.

1c. A researcher estimating participation
- What I estimate is participation among the eligible (FNS's rates combine simulated eligibility with administrative
  participant counts; Meyer-Mittag link administrative records). A model of REPORTED receipt from survey answers is the
  thing my field shows to be biased (differential misreporting, NBER WP 25143). As a coefficient study it is a look
  back (SEL-3). The only predictive use is to impute receipt into another survey or year that lacks the item (data
  fusion), which is actor 1b's decision in another file.
=> Fit none on its own; folds into 1b.

**2. DOES SEL-7 APPLY, AND WHAT WOULD SET THIS CASE APART**

- For the declared actor (agency/outreach): yes, SEL-7 applies word for word (the respondent knows the label and gives
  it in the interview that gives the features; the screening targets are in the negative class), plus USE-5. The
  precedent cdc_diabetes_health_indicators (No) and stroke_prediction (No) would be followed by C.
- The fact that sets this case apart, if the curator wants one: SEL-7 says such a label "is predicted by nobody". For
  the ACS FS item that is false: the Census Bureau predicts exactly this label, from exactly this interview's other
  answers, for 1.7-1.8% (2014-2018) to 2.9-3.1% (2021-2024) of households every year, roughly 20-40 thousand households
  a year in the 1-year file, and flags each fill (FFSP). cdc_diabetes had no such actor: its use case was screening for
  the undiagnosed, and its label was a past diagnosis nobody fills in. That is a recurring, documented decision that
  exists independently of this dataset, so I do not read B as "a use case rephrased only to excuse a gap" (USE-9 weighed
  factor) - provided the dataset is then built for that actor, not left in the agency's framing.
- Caveat for the curator: the same argument would open every survey-answer label with item allocation (ACS broadband,
  NHIS, CPS items) to the imputation use case. If the curator takes B, the precedent should say "an item the survey
  office allocates, with the allocation flag in the release" so the exception stays narrow.

**3. PROTECTED GROUNDS AS INPUTS (builder issue 2)**

- Agency actor: 7 CFR 272.6(a) bars state agencies from discriminating in "any aspect of program administration",
  including "other program services", on age, race, color, sex, disability, religious creed, national origin or
  political beliefs. 272.6(g) lets agencies collect race and ethnicity only for civil-rights reporting, voluntarily, the
  form stating it will not affect eligibility. An outreach ranking that uses race, ancestry, place of birth or sex is a
  program service on those grounds: the agency could not use them. Age and disability are different: SNAP's own rules
  turn on elderly and disabled members (no gross-income test, medical deduction), so those enter eligibility. On top,
  race in a model of REPORTED receipt partly encodes differential under-reporting by race (NBER WP 25143), so its
  coefficient is a reporting artefact, not need.
- Imputer actor: 272.6 does not bind the Census Bureau, and an imputation model MUST condition on race, Hispanic origin,
  nativity and disability, because the Bureau publishes SNAP receipt by exactly these (S2201); an imputer that omits
  them shrinks those differences toward zero in the published tables. Under B, keep them (builder's option A).
- So the actor decides issue 2: agency framing -> drop race, Hispanic origin, ancestry, place of birth, sex (builder's
  B); imputation framing -> keep all.
- Cost measured (my check, LightGBM 400 trees, 400k train / 200k test per shipped window): dropping 12 items (sex,
  race, Hispanic origin, ancestry, place of birth, citizenship, nativity, disability and three difficulty items, age)
  costs 0.003-0.004 ROC AUC overall (0.9101 -> 0.9070 for 2024, 0.9071 -> 0.9044 for 2023, 0.9087 -> 0.9045 for 2022),
  and 0.007-0.009 within households at or below 130% of poverty (0.8481 -> 0.8393; 0.8466 -> 0.8396; 0.8439 -> 0.8355).

**4. GAPS BETWEEN THE DATASET AND THE REAL DECISION, RANKED BY HOW MUCH THEY CHANGE THE TASK**

1. (Changes everything, agency actor) The label is the actor's own record, and the actor wants the opposite cell:
   eligible non-participants sit in "No". USE-5, SEL-7. Not fixable with this source: eligibility is not in the PUMS
   (it would have to be simulated from income, size, assets and state rules, which is a calculation, not a prediction).
2. (Changes the task, any actor) The headline AUC is mostly the easy separation of well-off households: 74-75% of
   households are above 200% of poverty. Within households at or below 200% of poverty (the population any SNAP actor
   looks at), LightGBM's ROC AUC is 0.849 / 0.848 / 0.850 (2024 / 2023 / 2022) against 0.910 / 0.907 / 0.909 on all
   households; at or below 130% it is 0.848 / 0.847 / 0.844. Among households at or below 130% of poverty, 64% report No.
   For the imputer this is no gap (it imputes for all households); for an outreach actor it is.
3. (Changes the inputs, every actor) PAP, SSIP and HINS4 are dropped though every actor has them: the imputer from the
   same interview (USE-6), the agency from its own and Medicaid's records (the very lists outreach matches on). +0.007
   ROC AUC by the builder's run. "Other benefits of the same 12 months" is no leak: they are known at the prediction
   point of every framing.
4. (Changes the score, imputer) Calibration under drift is not scored. A model fit on the earlier years under-predicts
   the test year's SNAP share: mean prediction 0.0955 vs observed 0.1018 in 2024 (-6% relative), 0.0955 vs 0.1057 in 2023
   (-10%), 0.0968 vs 0.1059 in 2022 (-9%). An imputer would publish a SNAP share too low by that much; ROC AUC does not
   see it, log loss does (0.2007 / 0.2087 / 0.2075).
5. (Imputer) The test rows are respondents, while the imputer acts on non-respondents (MAR assumed; imputed cases are
   the most error-prone, NBER WP 29184). Not fixable: non-respondents have no label.
6. (Imputer) Within-year processing vs the temporal split: the split is conservative and keeps real drift (12.0% ->
   9.3% -> 10.2%); keep it with a note, or the split auditor decides.
7. (Minor) Census household vs SNAP household; 12-month receipt vs monthly certification; 2023 end of emergency
   allotments and the Medicaid unwinding move PUBCOV in the test windows (drift the benchmark may want).

**5. WHAT AN EXPERT IN THE DOMAIN WOULD CHANGE**

If the dataset ships (B, item imputation):
- Rewrite task_summary.use_case and fit_reason to the imputer: "the survey office fills the SNAP item for households that
  leave it blank, from the interview's other answers"; drop the outreach sentence and TableShift's screening as the
  use case (keep TableShift as the task's origin only). Fit approximate, the gaps of section 4 items 4-6 named.
- Add PAP, SSIP and HINS4 back as features (the imputer has them; USE-6).
- Keep the protected grounds (the published S2201 cross-tabs need them); record why under SEL-1 / the tension row.
- Declare log_loss from context (MET-8, MET-11): the imputer draws from the probability, and the measured
  under-prediction of the test year's share is exactly what it must be scored on. If the curator keeps the binary
  fallback, the notes should at least name calibration as unscored.
- Optionally restrict to nothing (all households are imputed); do NOT add TableShift's income filter.
If it does not ship (C): No with No Good Target / Scientific Discovery (SEL-7, USE-5), noting that the agency holds the
label and the outreach target is eligibility among non-participants; acs_household_broadband and the Findex/FinScope
records should get the same reading.
I would not ship A: its declared actor does not exist for this label.

**6. DOES THE DECLARED METRIC (fallback roc_auc, unweighted) SCORE THE DECISION?  PARTLY.**

- Agency/outreach: no metric on this label scores the decision (the decision is about a cell the label cannot identify).
  If forced, the outreach budget is a top k within the low-income population (precision_at_k, MET-7) - but on this label
  that k would be filled with current recipients (top 10% of scores within <=200% of poverty: 82.5% / 82.0% / 81.8%
  report Yes), which is the failure, not the success.
- Imputer: the decision is a draw from a probability whose level must be right per cell; a strictly proper rule scores
  it (MET-8: log_loss; Brier also proper). ROC AUC ranks and is blind to the -6% to -10% level error measured above.
  MET-9: no reason for PR AUC here. MET-16: unweighted is right for an imputer of each household's item (the imputer
  imputes each blank, not a population total); MET-17 is satisfied (one row per household).
- Metric I would choose: log_loss (context, MET-8/MET-11), with roc_auc as the named fallback. That departs from the house
  binary fallback, so it is the curator's call.

**7. MY CHECK (scratch, read-only on the repository)**

Script and output in the run's work files (the participant kit's data
and the shipped splits; per window 400k random train rows of the shipped 1M, 200k of the 500k test rows; LightGBM
400 trees, lr 0.05, 63 leaves; one seed). Per window (test 2024 / 2023 / 2022):
- ROC AUC all features 0.9101 / 0.9071 / 0.9087; without 12 protected-ground items 0.9070 / 0.9044 / 0.9045.
- ROC AUC within poverty ratio <= 200%: 0.8490 / 0.8477 / 0.8495 (25-26% of rows, 28.4-28.5% Yes); <= 130%: 0.8481 /
  0.8466 / 0.8439 (15.0-15.6% of rows, 35.7-36.4% Yes).
- Log loss 0.2007 / 0.2087 / 0.2075; mean prediction 0.0955 / 0.0955 / 0.0968 against Yes share 0.1018 / 0.1057 / 0.1059.
- Precision of the top 10% within <= 200% of poverty: 0.825 / 0.820 / 0.818.

**8. SOURCES**

- TableShift, Food Stamps (tableshift.org/datasets.html): "Low-cost, low-friction screening tools ... whether an
  individual is receiving food stamps in order to identify likely candidates ... and as a proxy for eligibility and need
  for additional support services"; no metric for the task; held-out East South Central.
- Meyer, Mittag, Goerge, NBER WP 25143 (2018; JHR 2022), abstract: 35% of true recipient households do not report
  receipt in the ACS (23% SIPP, 50% CPS); understatement largest for single parents, non-white and low-income
  households; errors vary with characteristics and bias models of receipt. https://www.nber.org/papers/w25143
- Celhay, Meyer, Mittag, NBER WP 29184 (2021): error rates higher among imputed observations.
  https://www.nber.org/papers/w29184
- Rothbaum, Fox, Shantz, "Fixing errors in a SNAP" (Census, ASSA 2022): model-based imputation of administrative SNAP
  receipt from linked states. https://www.census.gov/content/dam/Census/newsroom/press-kits/2022/assa/assa-jan2022-paper-fixing%20errors-in-a-snap.pdf
  (content from the search summary; the PDF did not render). Davern et al. 2019, Russell Sage.
- ACS item allocation definitions (donor-based within-household and nearest-neighbour matrices):
  https://census.gov/programs-surveys/acs/methodology/sample-size-and-data-quality/item-allocation-rates-definitions.html
- Census AAPOR 2026 "model based or hot deck" (existence only; not read):
  https://www.census.gov/content/dam/Census/newsroom/press-kits/2026/aapor/2026-05-14-model-based-or-hot-deck.pdf
- 7 CFR 272.6 (Cornell LII): paragraph (a) nondiscrimination in program administration incl. other program services;
  (g) race/ethnicity collected voluntarily for reporting. https://www.law.cornell.edu/cfr/text/7/272.6
- Benefits Data Trust / CHCS North Carolina case study / CBPP data-matching brief: outreach by matching Medicaid and SNAP
  lists. https://www.chcs.org/media/Medicaid-and-SNAP-Data-Coordination-Case-Studies_North-Carolina_March-2023.pdf ,
  https://www.cbpp.org/sites/default/files/3-31-22fa-brief-datamatching.pdf ,
  https://statetechmagazine.com/article/2023/02/how-data-sharing-boosts-public-benefits-enrollment
- FNS, Trends in SNAP participation rates FY2020 and FY2022: 78% of eligible people participated in FY2020; elderly below
  average. https://www.fns.usda.gov/research/snap/national-participation-rates/fy20and22 ,
  https://www.fns.usda.gov/research/snap/national-participation-rates/fy2016-2020
- ACS S2201 (SNAP households by race and Hispanic origin of householder, by disability):
  https://api.census.gov/data/2024/acs/acs1/subject/variables/S2201_C01_026EA.html
- General knowledge, not re-read: SNAP's elderly/disabled rules (no gross-income test, medical deduction); SNAP household
  definition (purchase and prepare food together); FNS rates combining simulated eligibility with QC participant counts.

Rules cited: USE-1, USE-2, USE-5, USE-6, USE-8, USE-9 (and its weighed factor), SEL-1, SEL-3, SEL-7, MET-1, MET-7,
MET-8, MET-9, MET-11, MET-16, MET-17.

</details>

<details><summary>Blind review</summary>

BLIND REVIEW: acs_food_stamps_2014_2024 (target snap_received, binary, temporal on survey_year, 3 test windows)
Inputs used: the clean room's data (200k-row sample of 2.5M) and task description, census.gov PUMS pages, 2024 PUMS data dictionary, tableshift.org datasets page. No other local files were opened.

VERDICT: Include with changes. It is real ACS PUMS household data with a correct, leak-free target and good, non-trivial signal. Before use, document (or fix) the uneven year sampling and the population and use case, and say plainly that the inputs are contemporaneous survey answers.

WHAT THE TASK IS
One row is one occupied US household (50 states + DC, no Puerto Rico) in one ACS 1-year PUMS year: 2014-2019 and 2021-2024. 2020 is absent, which is correct because the 2020 1-year release was experimental. The features describe the household and its reference person (householder). The target is PUMS FS: "Yearly food stamp/Supplemental Nutrition Assistance Program (SNAP) recipiency" (1 Yes / 2 No), with 10.5% positives.
Realistic users: (a) SNAP outreach screening, the framing on tableshift.org: "diminished social support services in many U.S. states limit the ability of outreach providers..."; (b) imputing SNAP receipt into surveys or administrative files that do not ask about it. Nobody needs to predict FS inside the ACS itself. The use is plausible but indirect.
Signal (LightGBM, default-ish, trained on all earlier years):
  test 2022: AUC 0.889, AP 0.554, logloss 0.234 vs prior 0.336
  test 2023: AUC 0.900, AP 0.570, logloss 0.215 vs prior 0.331
  test 2024: AUC 0.904, AP 0.580, logloss 0.205 vs prior 0.324
  poverty-ratio-only AUC 0.80-0.81; random 80/20 split AUC 0.908 (similar to temporal).
There is clear headroom over a single-feature rule, and the task is not trivial. Size is ample: the test windows are ~40k rows each in the sample, which implies ~500k each in the full data.

CONCERNS, MOST TO LEAST SERIOUS

1. The years are sampled unevenly and task.md does not say so.
   Evidence: rows per year in the 200k sample are 10,955-11,751 for 2014-2021 and 39,905-40,059 for 2022-2024 (~3.5x). Since the sample is a uniform random draw, the full 2.5M likely has ~140k/yr for the early years and ~500k/yr for the last three. That is not the natural PUMS size, which is roughly constant at ~1.2-1.3M occupied households per year. The first test window (2022) trains on only ~80k sample rows (~1M full) from 7 years.
   Change: state the sampling rule. Better, sample a fixed number per year, or keep the last-3-year oversampling but document it as intended. Also note that 2020 is missing on purpose.

2. The population and decision are broader than the cited source, which makes the task easier and less decision-relevant.
   Evidence: TableShift's Food Stamps task restricts to "low-income adults aged 18 to 62 ... in households with at least one child", income < $30,000. Here all households are kept. 33.5% have poverty ratio top-coded at 501 (SNAP rate 1.6%), and households above 200% of poverty have SNAP rates of 3-8%. AUC on 2024 drops from 0.904 overall to 0.841 within poverty ratio <= 200 (n=9,886, prevalence 28%). Much of the headline AUC comes from easy rich-household negatives.
   Change: either state the use case as "population-wide SNAP imputation" and keep it, or restrict to a plausibly eligible population (e.g. poverty ratio <= 200%) for an outreach-screening task. Do not describe it as the TableShift task, because it is not that task.

3. The features are contemporaneous with the label, so this is "same-survey" prediction (not leakage, but it must be stated).
   household_income, householder_poverty_ratio, work experience, and public health coverage all refer to the same past-12-month window as the SNAP question and come from the same interview. SNAP is a noncash benefit and is not counted in ACS money income (HINCP/POVPIP), so the income features do not encode the label.
   householder_public_coverage (Medicaid etc.) is a sibling means-tested program. It is fine for imputation but borderline for outreach (an agency may or may not know it). Dropping it costs only 0.904 -> 0.897 AUC on 2024.
   Change: none required. Document it; optionally drop public coverage if the framing is outreach to people not yet enrolled anywhere.

4. The target is noisy.
   SNAP receipt is self-reported, and surveys are known to underreport it. Imputed (allocated) answers (flag FFSP in the PUMS) are presumably included, and no allocation flag is provided.
   Change: consider dropping rows with FFSP=1, or at least document that they are included. I could not check this.

5. Coding changes over time are real shift but should be documented.
   - Occupation: the coding changed in 2018. 98 levels last appear in 2017 and 147 levels first appear in 2018 (e.g. 'CLN-Grounds Maintenance Workers' 2014-2017 vs 'CLN-Landscaping And Groundskeeping Workers' 2018+). Test windows (2022+) only see post-2018 codes; essentially no unseen test levels (0.03% in 2022).
   - Race: the classification changed with the 2020 Census. 'Two or More Races' is 1.5-2.2% in 2014-2019 and 8.4-8.8% in 2021-2024, and White alone falls from ~0.80 to ~0.72.
   - Money columns are nominal dollars per survey year (median household income 53,951 in 2014 to 85,789 in 2024; median rent 900 to 1,466). The poverty ratio is inflation-invariant.
   All of this is acceptable under a temporal split, but list it.

6. Preparation details (minor).
   - Ordered variables are stored as unordered category: vehicles, workers_in_family, persons_60/65_and_over, householder_education (24 levels), english_ability, units_in_structure. Integer/ordinal encoding would be more faithful.
   - High-cardinality categoricals: occupation (653 levels), place_of_birth (229), hispanic_origin (24). LightGBM gain ranks occupation 2nd and place_of_birth 3rd, which is likely overfit gain; fine for a benchmark, but worth knowing.
   - Redundant pairs: persons_60 vs persons_65; own vs related children; nativity vs citizenship vs place_of_birth; household_language vs limited_english. Harmless.
   - Missing values are structural and consistent:
     - gross_rent is NaN for every non-renter (73.9%), and owner_costs is NaN for every renter or no-rent household (27.9%).
     - hours, occupation, and class_of_worker are NaN for those not working.
     - workers_in_family and work_experience are NaN exactly for nonfamily households (34.3%).
     - gave_birth is NaN for all males and for females over 50.
     NaN is a reasonable encoding here.
   - survey_year is a feature. Under the temporal split, its test values are always out of range. This is harmless for trees, but some models may extrapolate.
   - Survey weights (WGTP) are dropped, so metrics describe the sample, not the population. That is acceptable for a benchmark.
   - Values are plausible:
     - household_income runs from -13,300 to 2.53M, and only 2% of values are multiples of 100, which suggests ADJINC was applied.
     - Householder age runs 15-97 (30 rows aged 15-17).
     - Household size runs 1-20.
     - Poverty ratio 0 matches exactly the households with income <= 0.

7. Duplicates and copies: none found. There are 0 exact duplicate rows, 0 duplicate feature vectors (with or without survey_year), and every year has its own label. ACS years are independent cross-sections, so the same household reappearing in two years is possible but rare and cannot be linked.

WHAT I COULD NOT CHECK
- The full 2.5M table, and the actual per-year counts and test-window boundaries (I assumed the 3 windows are 2022, 2023, 2024).
- How the householder record was chosen (presumably reference person RELSHIPP=20 / RELP=0) and whether group quarters and vacant units are excluded (no NaN target, so likely yes).
- Whether imputed SNAP answers (FFSP) are included, and whether ADJINC was applied (indirect evidence says yes).
- Whether the 2022-2024 oversampling is intentional.
- The TableShift source code, for its exact feature list and years.

Scratch script: the run's work files.

</details>

<details><summary>Task gamer</summary>

acs_food_stamps_2014_2024 -- task gamer report

Verdict: the task barely games. Nothing a deployed model would lack adds more than about +0.001 AUC. The largest gains (+0.003 to +0.006) come from fitting on labelled rows of data.parquet that sit outside the shipped training set. That is mostly a matter of training-data volume, not leaked information.

Setup: 2.5M household rows, one per ACS householder. Target snap_received (rate 10-12% per year). Splits are three temporal windows; the test is one whole year (2024, 2023, 2022, 500k rows each), and each train is a 1M-row subsample of all earlier years. Metric roc_auc.
Every run is LightGBM on the shipped splits, scored with the kit's scorer.

Honest models
  baseline (untuned LGBM, lr 0.1, 300 rounds)            r0 0.91420  r1 0.91118  r2 0.91052  mean 0.91197
  tuned honest (lr 0.05, 1000 rounds, 127 leaves, cat smoothing)
                                                         r0 0.91613  r1 0.91365  r2 0.91315  mean 0.91431
  noise column added to baseline (2 seeds)               means 0.91194 and 0.91196; per-split spread about +-0.0003

Exploits ranked by gain
| # | Exploit | Honest | Exploited | Gain per split | Deployed model has it? | Fix |
|---|---|---|---|---|---|---|
| 1 | Add labelled rows from years after the test window (in data.parquet) to training | base 0.91197 / tuned 0.91431 | 0.91551 / 0.91697 | base +0.000, +0.0045, +0.0061; tuned +0.000, +0.0032, +0.0048 | No (future years) | Have the harness fit only on the shipped train rows (it already must, since data.parquet also holds the test labels). Nothing to change in the data. |
| 2 | Year-level statistics over train+test rows (income/rent percentile within state-year and year), plus income-roundness features | base 0.91197 / tuned 0.91431 | 0.91266 (stats), 0.91261 (format) / 0.91522 (both) | base +0.0006 to +0.0008 each; tuned +0.0013, +0.0005, +0.0009 | Mostly yes (see below) | None needed |

Finding 1, future rows. Most of the gain is volume. On split r1, adding 500k past rows (2014-2022) gives +0.0039 (tuned +0.0028), and adding 500k future rows (2024) gives +0.0045 (tuned +0.0032). The part that comes from the future itself is therefore about +0.0005, close to the noise spread. A participant can do this only by ignoring the shipped train positions.

Finding 2, year statistics and income format. Most of what the within-year percentiles recover is the inflation drift in household_income (nominal survey-year dollars, ADJINC = 1.001-1.042). A deployed model can correct for that with CPI or with the previous year's distribution.
Income roundness: household_income / ADJINC gives back the reported HINCP. Indicators for multiples of 10/100/1000/10000 reach AUC 0.60 on their own. Exact, non-round incomes (benefit amounts, for example) go with SNAP. This is the reported answer itself, so it is signal, not an artefact.

Flaw that hurts an honest model (the training subsample)
| What is wrong | Honest choice | Shipped-train score | Honest-choice score | Fix |
|---|---|---|---|---|
| Each train is capped at a 1M-row subsample. Split r0 drops 1.0M and r1 drops 0.5M labelled rows that come before the test window and that a deployed model would train on. | Train on every row dated before the test year | base 0.91197 / tuned 0.91431 | base 0.91475 (r0 +0.0045, r1 +0.0039, r2 0) / tuned 0.91650 (r0 +0.0038, r1 +0.0028, r2 0) | A benchmark design choice (bounded train size) that applies equally to all methods. If kept, state it in task.md. Otherwise ship all pre-window rows. |
Old years are not harmful: training only on the last 1/2/3 train years scores 0.90005/0.90523/0.90783 (baseline settings), and post-2021 only scores 0.90466. All of these are below the baseline, so dropping stale rows does not help. Dropping survey_year scores 0.91102 (-0.001).

Public lookup: it works. I downloaded the published 2024 PUMS Wyoming housing file and matched rows on income (HINCP*ADJINC) and household size. 543 of 963 kit rows match uniquely, and FS agrees with snap_received on all 543 (100%). This is not ranked, since any public dataset allows it.
Comparison with the source: the kit's WY 2024 SNAP rate (0.052, n=963) matches the full published file (0.047, n=2801). The sampling does not look label-dependent.

Attacks that found nothing
- Row order: data is sorted by year and shuffled within each year. AUC of label against within-year position is 0.497-0.504. Next-row label agreement equals chance (for example 2024: 0.8176 vs 0.8174). The test positions show no order signal (AUC 0.499).
- Exact copies: 0 duplicated full feature vectors anywhere in the 2.5M rows, with or without year. No test row has a copy in train.
- Training rows at or after the prediction point: none. Every train year is earlier than its test year, and test windows are single whole years.
- Numeric formats: every numeric column is whole-valued in all years. Last digits of income and owner costs are flat. Rent's last digit 0 shows a slightly higher rate (0.243 vs about 0.19), which is ordinary heaping. The poverty ratio's 501 top code (33% of rows, rate 1.3-1.8%) and 0 are documented ACS codes. Missingness (rent NA = owner, hours NA = not working, workers NA = non-family) follows the questionnaire.
- Columns from after the outcome: none. The best single feature (target-encoded, 2024 test) is household_income at AUC 0.763, then poverty_ratio 0.763, and the rest are 0.70 or below. Every column is an interview answer. householder_public_coverage (Medicaid) is strong but is known at the interview.
- Train-vs-test classifier: AUC 0.89-0.92, but this is the year signature. household_income / poverty_ratio reveals the year's poverty threshold, and occupation and place-of-birth label vintages change (295 of 656 occupation levels and 20 of 229 birthplace levels occur only in some years). 2023 vs 2024 drops to 0.68, and without income/poverty/occupation to 0.52. It is not a label route.
- Sampling: label rates by year change smoothly (12.1% in 2014, 9.2% in 2019, 10.9% in 2021, 10.2% in 2024), and the WY check above agrees.

Not checked
- Label of the nearest training neighbour (near copies). There are no exact copies and the households are independent across ACS years, so I expect nothing.
- Harmonising occupation codes across the 2018 OCCP vintage change (an honest improvement, not an exploit).
- Per-state SNAP policy shifts in the test year.

</details>

<details><summary>Precedent check</summary>

PRECEDENT CHECKER REPORT: acs_food_stamps_2014_2024 (folder acs_food_stamps_2014_2024_1m), 2026-11-09

Read: principles.md (Strengths, Tensions, Exceptions and amendments, Consistent judgement), selection.md (SEL-1 to
SEL-7, Cases), use_case.md (USE-1 to USE-11), provenance.md (PROV-4 to PROV-7, Cases), metrics.md (MET-8, MET-11,
MET-16, MET-17, Cases), cleaning_features.md (CLEAN-21, Cases); the definition, the
record, the builder report, the five other phase-A reports (domain practitioner, column, split, claim auditors, blind
reviewer); the decision register (the SEL-7 decisions, the flags); sibling records found by grep over curation/records
(SEL-7, TableShift, ACS, survey, imputation/allocation, inflation); the dev copy's definitions (metric origins,
nominal money, imputation use cases); the rais and wioa reports of this batch. Nothing edited, nothing run.

SUMMARY
  D1 SEL-7, the label a household reports in the same interview ... option A (implemented): departs without a fact
     that sets it apart, and a Must cannot be departed from: NOT REASONABLE UNDER THE RANKING. Option B (the survey
     office's item allocation as the actor): departs from cdc_diabetes_health_indicators WITH a stated, measured fact,
     and follows ai4d_lab_tanzania_tourism_classification_challenge (2026-11-05) - but since SEL-7 is a Must it can
     only enter as SEL-2's reading or as an amendment of SEL-7, not as an "exception". Option C: consistent with
     cdc_diabetes and stroke_prediction. Prompt 1.
  D2 Protected grounds kept (implemented) ............. under framing A: departs from the Tensions row's reasoning
     (bemtpl97) without a reason; the row's scope names pricing only and its extension (rais) is an unconfirmed AI
     recommendation; same-batch pair wioa goes the other way. Under framing B: consistent (no law binds the
     imputer). Prompt 2.
  D3 Unit: households, no TableShift filter ........... consistent (MET-17, USE-11; the PROV-6 verdict on
     food_stamps still holds), but the curator's CC on food_stamps states a fact the build made untrue. Record
     correction, no prompt.
  D4 Dollars in each survey year's dollars ............ departs from CLEAN-21 with a stated reason, but the reason
     does not set it apart: four shipped temporal datasets keep nominal money with no exception recorded. Amendment
     due in substance. Prompt 3.
  D5 Survey weights dropped, scored unweighted ........ consistent (MET-16; anes_voting_2026, 2026-11-06).
  D6 Fallback roc_auc ................................. consistent (MET-8; anes_voting_2026, 2026-10-21; every binary
     fallback of the copy). log_loss would be a departure with a reason under framing B only (noaa: the metric
     follows the actor).

**D1. SEL-7: a household's own report of SNAP receipt, given in the interview that gives the features**
As implemented: option A of builder issue 1 (outreach screening, fit approximate, SEL-7 named as a gap).

Precedents (dated, with links)
  * cdc_diabetes_health_indicators: `No`, `No Good Target / Scientific Discovery` (CC 2026-10-15, Lennart; SEL-7's
    first case). "ever told you have diabetes ... predicted from answers of the same interview; no decision is made
    with that prediction"; the screening targets (the undiagnosed) sit in the negative class. curation/records/
    cdc_diabetes_health_indicators.md; selection.md Cases.
  * stroke_prediction: `No` (CC 2026-10-26, Lennart, "This looks too bad, dont ship it"), retired as cdc_diabetes,
    "SEL-7 not amended". curation/records/stroke_prediction.md.
  * dataorg_financial_health_prediction_challenge: `No` (CC 2026-10-22, Lennart): "we have no information on the
    target ... and it is survey data; tag it 2nd tier / scientific discovery". A FinScope survey answer; SEL-7 not
    cited, same mechanism. curation/records/dataorg_financial_health_prediction_challenge.md.
  * Legacy curator lines (undated or 2026-06 imports, before the ranked rules; low weight): national_longitudinal_
    survey_binary `No` ("Survey data. Not a real predictive task."); drug_consumption ("Scientific discovery task.");
    TableShift's other ACS tasks income, public_health_ins, unemployment `No` with `Duplicate` and `2nd Tier /
    Scientific Discovery` ("Same data as Food Stamps task").
  * ai4d_lab_tanzania_tourism_classification_challenge: SHIPPED (CC 2026-11-05, Lennart, REVIEW.md issue 3, option
    B): "the survey statistician (NBS, the Bank of Tanzania) joins the planner ... fill in a departing respondent's
    spending band from the rest of the exit form when the expenditure answer is missing or implausible." The label is
    a band of the spending the respondent reports on the same form: SEL-7's mechanism in letter, accepted with the
    survey office's item imputation as an actor. SEL-7 was not raised there. curation/records/
    ai4d_lab_tanzania_tourism_classification_challenge.md; datasets/_dev/tabarena-v0pt2/
    ai4d_lab_tanzania_tourism_classification_challenge/REVIEW.md (issue 3).
  * folktables_acs_income (AI, 2026-10-31, not decided): the AI already proposed the Census Bureau's allocation
    (flag FPINCP) as a use case for an ACS target. Pending.
  * The "2nd Tier" survey records the builder cites (acs_household_broadband, global_findex_2025, finscope_tanzania_
    2023, drug_consumption, nsduh_past_year_drug_use) are AI screenings parked outside v0.2; dont_overfit_by_uofk_fmsi
    `No` is an AI screening (checked_by "AI (UNVERIFIED)"). None is a curator keep, so none is a precedent for
    shipping. No survey self-report with SEL-7's mechanism has shipped except Tanzania.
  * anes_voting_2026 (shipped, TableShift, survey): NOT a counter-precedent. Its features are the pre-election wave
    (post-election items dropped, CC 2026-09-30) and the vote comes after, so the respondent does not know the label
    at the prediction point.
  * Record CC 2026-11-08 (Lennart): accepted for adding, "SEL-7 ... is decided at the build: it is the first issue of
    the dataset's REVIEW.md". The build follows it (issue 1 is SEL-7).

Comparison of the facts that matter for SEL-7
  * Respondent knows the label, same interview: yes, as cdc_diabetes. Positives the screening use wants sit in the
    negative class: yes (eligible non-participants; and 35% of true recipients report No, NBER WP 25143), as the
    undiagnosed in cdc_diabetes. Independent measurement of the label: none in the release (linked administrative
    records exist only in restricted research data).
  * The agency actor holds the label for every participant in its own records (domain practitioner 1a). That makes
    the declared actor weaker than cdc_diabetes', not stronger. The claim auditor's re-run (claim 30) weakens one
    builder argument (an "application form" set reaches 0.9104 of 0.9152), but not the SEL-7 mechanism.
  * The fact that could set it apart: the Census Bureau predicts exactly this label from the same interview's other
    answers for 1.7-1.8% (2014-2018), 1.9% (2019) and 2.9-3.1% (2021-2024) of households, and flags each fill (FFSP)
    in the release (builder, measured per year). BRFSS's diabetes item has no such actor; SEL-7's own wording "is
    predicted by nobody" is false for this item. It is the same kind of actor the curator accepted for Tanzania.
  * What does NOT set it apart: TableShift's screening framing (cdc_diabetes also had a screening framing in its
    sources); the size, signal and drift (P6 cannot rescue a P2 Must, principles "Independent failures are not
    conflicts"); the curator's acceptance for adding (it explicitly deferred SEL-7).

Verdict per option
  * A (implemented): departs from cdc_diabetes and stroke_prediction with no fact that sets it apart. SEL-7 is a Must
    (narrows SEL-3, P2): "fit approximate with the gap named" does not meet a Must; principles say a Must has no
    exceptions. Not reasonable under the ranking.
  * B: departs from cdc_diabetes with a measured fact, follows Tanzania. Form: SEL-7 is a Must, so B cannot be
    recorded as "Exception to SEL-7". Two legitimate forms: (i) SEL-2 (Must, earlier in the file, the tension row "A
    real task against a scope pattern": the use case decides whether a scope rule applies), or (ii) an amendment of
    SEL-7 narrowing its scope. Given the domain practitioner's warning to keep it narrow, (ii) with explicit wording
    is safer: under (i) every survey answer someone could impute would argue its way in.
    Proposed narrow wording (for the curator): "... is predicted by nobody, unless the survey's own office fills the
    item for non-respondents from the same interview and flags the fill in the release (an item allocation): then the
    task is that office's, its rows the respondents, and the use case, inputs, split and metric are the imputer's."
    Cases: acs_food_stamps_2014_2024 (and Tanzania as the earlier, unflagged instance).
    What the narrow wording would open (not checked per record; allocation flags are typical of the ACS PUMS, CPS
    supplements and NSDUH, not of Findex or FinScope): acs_household_broadband, folktables_acs_income,
    ntia_internet_use_survey_home_adoption, nsduh_past_year_drug_use, nsduh_mental_health_treatment. It keeps
    cdc_diabetes and stroke_prediction out (no allocation of the label). Name these in the amendment so the
    precedent is read as narrow.
    B is only consistent if the dataset is then built for the imputer (domain practitioner section 5: use case
    rewritten, the other benefit items back as USE-6 inputs, the split read for the imputer). Tanzania's issue 3
    gives the split consequence: with the statistician added next to a forward-looking actor the regime stayed; had
    it replaced the actor, the folds would follow the imputer's within-survey use (option C there). Here the
    outreach actor fails, so the imputer would be the sole actor; the split auditor's point 5 applies.
  * C: consistent with cdc_diabetes, stroke_prediction and dataorg. Tanzania is no conflict under C: its ship rests
    on the trip planner, who predicts a future spending band, and the statistician was added beside it. Under C,
    food_stamps' `Duplicate` points to a `No` record; its markers should then carry the SEL-7 reason too.

Drift and third exception
  * No drift: every curator call naming SEL-7 is an exclusion (2026-10-15, 2026-10-26); Tanzania (2026-11-05) kept
    a same-form label without SEL-7 being raised. If A or B is chosen, it is the first keep under SEL-7 and the
    register will flag opposite outcomes: record the distinguishing fact (B) or the amendment so the flag resolves.
  * Not a third exception (no exception to SEL-7 exists; Tanzania is unrecorded).

Draft consistency check for the curator: Your acceptance of this record and the implemented option A ship a label the household reports in the interview that gives the features, which cdc_diabetes_health_indicators and stroke_prediction excluded: what sets this case apart?

* **Problem:**
  - The household knows its own SNAP receipt and reports it in the same interview as every feature, the mechanism under which BRFSS's diabetes item was retired on 2026-10-15[^pc-sel7].
  - The outreach actor the definition names wants eligible households that do not receive SNAP, and they sit in the "No" class, as the undiagnosed did in BRFSS[^cdc].
  - The Census Bureau fills this item from the interview's other answers for 1.7-3.1% of households a year and flags each fill, which BRFSS's diabetes item never had[^tz].
* **Background:**
  - You already accepted a survey office imputing a respondent's own answer as an actor for the Tanzania exit survey (2026-11-05), without the scope rule being raised there[^tz].
  - A rule that must hold cannot take a one-off exception, so a keep enters either as the use-case reading of the scope rule or as a narrowed rule[^must].
* **Options:**

  | | Option | What it does | Pro | Con |
  |---|---|---|---|---|
  | a | The Bureau's item allocation sets it apart, written into the rule | Narrow the scope rule to items the survey office allocates and flags; rebuild the use case, inputs, split and metric for the imputer | an actor that predicts exactly this label from these inputs; follows Tanzania; keeps diabetes and stroke out | a niche use case; opens five 2nd-Tier survey records to the same reading; hot-deck today, not a learned model |
  | b | Treat it like cdc_diabetes_health_indicators | `No` with `No Good Target / Scientific Discovery`; folder removed; food_stamps keeps its `No` | consistent with diabetes, stroke and the FinScope call | loses a large, drifting public survey task TableShift uses |
  | c | Ship as implemented (outreach framing) (implemented) | No change | TableShift's framing kept | breaks a rule that must hold, with no fact named; the first keep against two exclusions |
  | d | Reopen cdc_diabetes_health_indicators to match | Re-screen BRFSS under a looser reading | one standard for survey answers | contradicts your own retirement reasons of 2026-10-15 and 2026-10-26 |

* **Recommendation:** a or b, not c. a if you see the Bureau's flagged allocation as a decision someone makes with this prediction; b otherwise. **Decision:** a, b, c or d?

[^pc-sel7]: **SEL-7** (Must; narrows SEL-3): "A label the respondent already knows, asked in the same interview as the features (a past diagnosis), is predicted by nobody. A screening task needs positives that do not know yet, found by an independent measurement such as a lab test." Cases: cdc_diabetes_health_indicators (2026-10-15), stroke_prediction (2026-10-26).
[^cdc]: **cdc_diabetes_health_indicators**, CC 2026-10-15 (Lennart): "the undiagnosed ... sit in the negative class"; **USE-5** (Must): predict what the actor would act on.
[^tz]: **ai4d_lab_tanzania_tourism_classification_challenge**, CC 2026-11-05 (Lennart), REVIEW.md issue 3 (B): NBS and the Bank of Tanzania "fill in a departing respondent's spending band from the rest of the exit form when the expenditure answer is missing or implausible". Allocation shares: builder report, FFSP per year.
[^must]: **principles.md**, Exceptions and amendments: "A Must has no exceptions: only a higher-ranked Must overrides it, and anything else is an amendment"; **SEL-2** (Must): "let the use case decide"; Tensions row "A real task against a scope pattern".

**D2. Protected grounds among the inputs (SEL-1; Tensions row "a factor the actor may no longer use")**
As implemented: all kept (builder issue 2, option A; builder recommends B, drop sex, race, Hispanic origin,
ancestry recode, place of birth).

Precedents
  * bemtpl97 (CC 2026-11-05, Lennart, issue 3 (a)): `sex` dropped; reason the actor's legal constraint today
    ("they would not be able to use sex"). curation/records/bemtpl97.md.
  * australian_vehicle_insurance_2004_2005, pricing_game_2017_french_mtpl, frempl_french_motor_personal_line,
    spanish_homeowners_motor_insurance_2010_2014 (2026-11-08, Lennart): sex dropped under the family stance. The
    amended row's scope: "sex leaves the rating factors of every insurance pricing task".
  * home_credit_default_risk, credit_card_clients_default: keep gender, "credit not insurance, not reviewed yet" (the
    row itself). hr_analytics keeps gender, never reviewed on this point.
  * rais_employment_separation (this batch, AI recommendation, curator not yet asked): extend the row to "decisions
    on employees where the actor's own law bars the factor"; drop all five grounds (Lei 9.029/1995). Pending as rais
    issue 1. This is not yet a curator decision and not yet in principles.md.
  * wioa_employment_after_exit (this batch, AI recommendation): keep race, sex, disability, ex-offender status,
    "DOL's adjustment model explains the same outcome with them ... the decision allocates help, not a price or a
    denial". Pending.

Comparison
  * Framing A (state SNAP agency, outreach today; test years 2022-2024): 7 CFR 272.6(a) bars the agency from those
    grounds in "any aspect of program administration", including other program services (builder, domain
    practitioner, column auditor all read it). The row's reasoning (bemtpl97: the actor's legal constraint today)
    gives "drop"; the row's "Where it stops" (a use case set in the data's own time keeps the factor) also gives
    "drop", since 272.6 was in force over all of 2014-2024. Keeping them departs from the reasoning with no fact
    named. The row's written scope covers insurance pricing only, so applying it here is the same extension rais
    asks for: confirm it once, for all three same-batch cases.
  * Framing B (the imputer): 272.6 does not bind the Census Bureau, so the row gives no reason to drop; keeping all
    is consistent. The domain practitioner's argument that the imputer must keep them (S2201 publishes SNAP by race,
    Hispanic origin, disability) is an inference, not a measurement or a source statement.
  * Same-batch pair: wioa keeps race and sex for a public programme bound by its own nondiscrimination rule (WIOA
    section 188; not re-read here, general knowledge), rais and acs (framing A) drop. The distinguishing fact wioa
    names (the actor's adjustment model uses them) is about DOL's performance-target adjustment, not the
    service decision the use case models. The three should be decided by the same test: does the actor's own law
    bar the factor for the decision the use case models.
  * Age, disability, citizenship: the column auditor's fact (SNAP's own eligibility rules use them) sets them apart
    from race, sex and origin, the same kind of fact as insurance keeping age. Consistent to keep them.
  * Completeness of a drop (column auditor A: sex survives in household_type, work_experience_householder_spouse,
    householder_gave_birth_past_year for 69% of rows): no precedent. The insurance cases dropped the named column only
    (frempl kept `Gender` inside its policy-component key, then dropped it). A new question, not a departure.

Draft consistency check for the curator: Under the outreach framing the definition keeps sex, race, Hispanic origin and place of birth, which a state SNAP agency may not use, while your insurance calls drop a factor the actor's law bars: what sets this case apart?

* **Problem:**
  - The definition ships the householder's sex, race, Hispanic origin and place of birth as inputs to an agency's outreach ranking[^272].
  - Your calls of 2026-11-05 and 2026-11-08 dropped sex because the actor today may not use it, but the written rule covers insurance pricing only[^row].
  - In this batch the AI recommends dropping such factors for the Brazilian employer (rais) and keeping them for the WIOA programme, so three pending calls rest on one untested reading[^batch].
* **Options:**

  | | Option | What it does | Pro | Con |
  |---|---|---|---|---|
  | a | The actor decides: drop under the outreach framing, keep under the imputer framing | Widen the rule to any actor whose own law bars the factor; drop the four grounds and recode the three columns that still carry sex, only if the agency stays the actor | one test for rais, wioa and this dataset; follows your insurance reasoning | three recodes; the wioa recommendation has to be revisited |
  | b | Keep all, as implemented (implemented) | No change; note the regulation | TableShift's inputs; useful for fairness work | a factor the named actor may not use; unlike your insurance calls |
  | c | Leave the rule at insurance and decide each non-insurance case on its own | Record a one-off reason here | no rule change | the same question returns in every batch; drift between rais, wioa and this case |

* **Recommendation:** a; it is moot for the grounds if issue 1 ends in the imputer framing. **Decision:** a, b or c?

[^272]: **7 CFR 272.6(a)** (Cornell LII): no discrimination "in any aspect of program administration ... for reasons of age, race, color, sex, disability, religious creed, national origin, or political beliefs".
[^row]: **principles.md**, Tensions, "A rating factor known at the prediction point against a factor the actor may no longer use": bemtpl97 (2026-11-05), australian_vehicle_insurance_2004_2005 and the insurance family (2026-11-08); **SEL-1** (Must); **USE-1**, **USE-6**.
[^batch]: rais_employment_separation issue 1 (Lei 9.029/1995 art. 1; recommends drop and an amendment of the row); wioa_employment_after_exit issue 1 (recommends keep); both AI recommendations of 2026-11-09, undecided.

**D3. The unit: households instead of TableShift's low-income adults (PROV-6, MET-17, USE-11)**
  * One row per household, one label per row: consistent with MET-17's reasoning (the actor decides once per unit;
    superconductivity, dementia_prediction, 2026-11-08) and USE-11 (the household is the unit SNAP certifies and the
    item describes). TableShift's person rows would need a unit weight and carry shared labels (LEAK-17).
  * food_stamps `No`/`Duplicate` (CC 2026-11-08, Lennart): the verdict holds under PROV-6 ("another slice of the same
    cohort ... when neither adds a distinct task"): TableShift's version adds a person slice and a held-out division
    already judged `Not Representative`, neither a distinct task (precedent heart_disease merge, 2026-10-27). But the
    CC's stated facts ("the same ACS item (FS) and population filter", "lies inside that record's 2014-2024") are no
    longer true of the build: the filter and unit differ. A correction of the record's wording on the next record
    edit, not a new decision. Under D1 option b, food_stamps should also carry the SEL-7 reason.
  * Population vs actor: dropping TableShift's income filter fits the imputer (who fills every household) and not the
    outreach actor (who looks at low-income households; ROC AUC 0.849 within <=200% of poverty against 0.910 overall,
    domain practitioner). So the unit is consistent; the population follows D1's actor. No separate prompt.
  * Side note, not this dataset's decision: income, public_health_ins and unemployment are `No`/`Duplicate` of
    food_stamps on the legacy line "Same data as Food Stamps task". PROV-7 (Must, narrows PROV-6) says a shared source
    with another target is no duplicate; folktables_acs_income's AI reject check of 2026-10-31 already refuted the
    same reading. If this record ships, those three rest on a reason the rules no longer support.

**D4. Dollar amounts in each survey year's dollars (CLEAN-21, Should)**
As implemented: HINCP x ADJINC, GRNTP and SMOCP x ADJHSG, i.e. each survey year's dollars; builder recommends
recording it as an exception ("the source publishes the comparable measure itself", POVPIP).

Precedents
  * CLEAN-21's cases are all changes of the measuring instrument or unit: college_scorecard (SAT redesign,
    concordance, 2026-10-16), force_2020 (unit errors), zillow_prize (quality code map, exception, 2026-10-26),
    rosbank1 (currencies at the central bank's rate, 2026-10-26). None is general price inflation.
  * Shipped temporal datasets that keep nominal money across years, with no CLEAN-21 exception recorded:
    noaa_storm_events_damage (target, "Nominal dollars as entered, not adjusted for inflation", 1996-2025, reviewed by
    Lennart 2026-11-08), kickstarter (goals 2009-2019 in USD, converted for currency only), lending_club (loan amounts
    and incomes 2007-2018), ames_housing (prices 2006-2010). datasets/_dev/tabarena-v0pt2/<name>/dataset.py.

Comparison
  * The builder's reason (POVPIP ships the comparable measure, the year is a feature) is true here, but the shipped
    siblings took the same departure without such a measure, so the house practice is "nominal as published" and
    the stated reason is not what sets this case apart. Either inflation is no "scale change" under CLEAN-21 (then
    no exception is needed and the rule should say so), or four unrecorded exceptions already exist (more than the
    three that make an amendment due).
  * The con of option B ("an index from outside the source") is weaker than written: the column auditor notes the
    Census Bureau's own 5-year PUMS ADJINC carries pooled years into the final year's dollars (general knowledge,
    not read by me or by the auditor), which would be "the conversion the source or the measuring body publishes"
    in CLEAN-21's own words. The auditor measured +0.0006 to +0.0007 ROC AUC from deflating (values from memory).
  * Verdict: departs with a stated reason that does not distinguish it from siblings; an amendment question.

Draft consistency check for the curator: Recording each year's dollars here as an exception would leave four shipped datasets with the same nominal money and no exception: is inflation a change of scale the rule asks us to remove?

* **Problem:**
  - Household income, rent and owner costs of 2014 and 2024 share one column in each year's dollars[^c21].
  - noaa_storm_events_damage, kickstarter, lending_club and ames_housing ship nominal money across years with no recorded exception[^sib].
  - The Census Bureau publishes its own cross-year adjustment for pooled files, so a conversion by the measuring body likely exists[^adj].
* **Options:**

  | | Option | What it does | Pro | Con |
  |---|---|---|---|---|
  | a | Amend the rule: general inflation is no scale change, amounts ship as published with the year as a feature | One sentence in the rule; no data change here or in the four siblings | matches what already ships; no outside index | 2014 and 2024 dollars share a column |
  | b | Exception for this dataset only (implemented) | Note it here; leave the siblings | the comparable poverty ratio ships | the siblings stay unrecorded departures; the reason does not set this case apart |
  | c | Deflate where the measuring body publishes the factors | Put the three amounts in 2024 dollars with the Bureau's factors; ask the same of the siblings later | one scale, the rule's own wording | ten constants; the siblings need a review |

* **Recommendation:** a, unless you want real dollars across the collection (then c). **Decision:** a, b or c?

[^c21]: **CLEAN-21** (Should): "One unit and one scale per column. When a feature's scale changes over time, put it on one scale the way an analyst would at the time, with the conversion the source or the measuring body publishes."
[^sib]: noaa_storm_events_damage dataset.py ("Nominal dollars as entered, not adjusted for inflation"); kickstarter, lending_club, ames_housing definitions; **principles.md**, Exceptions and amendments (three exceptions of one reason make an amendment due).
[^adj]: the column audit, problem C (5-year PUMS ADJINC; general knowledge, not read).

**D5. Survey weights dropped, scored unweighted (MET-16)**
  * Consistent with MET-16 (2026-11-06, Lennart) and its case anes_voting_2026 (TableShift survey; weight columns
    dropped, scored unweighted; curation/records/anes_voting_2026.md, Assessment 2026-11-06). The use case ranks
    households (framing A) or imputes each blank (framing B): no population estimate either way. anes measured how
    weighting moves the score (+0.004 to +0.005); acs did not, which MET-16 does not require. No prompt.

**D6. Fallback roc_auc against log_loss (MET-8, MET-11)**
  * As implemented, consistent: anes_voting_2026 (CC 2026-10-21, Lennart: "the fallback (roc_auc), not TableShift's
    accuracy") is the same source convention and the same reasoning; all 112 `Metric.fallback` definitions of the copy
    use roc_auc for binary; heart_disease kept roc_auc even where the source scored calibration (2026-10-21/27).
  * The domain practitioner's log_loss: no binary dataset in the copy declares log_loss from context (the one binary
    `from_context` is nci_aids_antiviral_screen, roc_auc; the two binary log_loss are source metrics, bioresponse and
    numerai28_6). It would be a departure, with a stated fact, only under framing B: the imputer draws from the
    probability and its level matters (test-year share under-predicted by 6-10%). Precedent for the metric following
    a changed actor: noaa_storm_events_damage (2026-11-08, Lennart: the actor became the planner, the metric the
    Tweedie deviance). MET-8's own text allows a strictly proper rule or a ranking metric, so log_loss would break
    nothing; it would be declared from context with TableShift's accuracy named as the original (MET-11). No prompt:
    it rides on D1.

**REGISTER FLAGS TOUCHING THIS CASE**
  * opposite_outcomes USE-5 (diabetes_3 keep, xente exclude, ...): none about a self-reported label; no pair here.
  * drift "post-outcome feature", SEL-16, scaling over all rows: not touched.
  * No SEL-7, SEL-1 or CLEAN-21 flag exists in the register; the D1 and D4 pairs above were found by reading
    records and definitions, not by the register.

FILES
  * Record: curation/records/acs_food_stamps_2014_2024.md; definition: datasets/_dev/tabarena-v0pt2/
    acs_food_stamps_2014_2024_1m/dataset.py
  * Precedent records: cdc_diabetes_health_indicators.md, stroke_prediction.md, dataorg_financial_health_prediction_
    challenge.md, ai4d_lab_tanzania_tourism_classification_challenge.md (+ its folder's REVIEW.md, issue 3),
    food_stamps.md, income.md, public_health_ins.md, unemployment.md, folktables_acs_income.md, anes_voting_2026.md,
    bemtpl97.md, frempl_french_motor_personal_line.md (all under curation/records/)

</details>

<details><summary>Advocate</summary>

ADVOCATE, OPENING BRIEF: acs_food_stamps_2014_2024 (folder acs_food_stamps_2014_2024_1m), 2026-11-09

Position: ship under the builder's option B (the Census Bureau's item allocation of the FS answer as the actor), with
the definition rebuilt for that actor. I do not defend option A as implemented. For the outreach actor the agency
already holds the label for every participant. The households it wants sit in the "No" class: 48,305 "No" households
at or below 130% of poverty against 50,819 "Yes" households in the 2024 window, and 64% of households at or below
130% report No (claim auditor I3; domain practitioner 1a). That fails USE-5 (Must) and SEL-7 (Must) as written, and
"fit approximate" cannot carry a Must. Every point below is the case for B.

1. SEL-7's premise ("is predicted by nobody") is false for this item, and SEL-2 lets the use case decide.
   Evidence: the Census Bureau fills FS from the same interview's other answers for 1.72-1.83% (2014-18), 1.95%
   (2019) and 2.91-3.08% (2021-24) of households, and flags each fill (FFSP 1). These numbers were measured by the
   builder and re-measured by the claim auditor (claim 11). The domain practitioner (1b) finds that the decision, the
   inputs, the label and the row match: one blank FS per household, with all 43 inputs at hand. It is "a recurring,
   documented decision that exists independently of this dataset", so not "a use case rephrased only to excuse a gap"
   (the USE-9 weighed factor). The Census Bureau is weighing model-based against hot-deck imputation (AAPOR 2026, cited
   for its existence only).
   Rule: SEL-2 (Must, earlier in the file than SEL-7) and the Tensions row "a real task against a scope pattern: the
   use case decides". Precedent: ai4d_lab_tanzania_tourism_classification_challenge, shipped 2026-11-05 (Lennart,
   option B) with the survey office imputing a respondent's own same-form answer.
   Why it outranks the objection: cdc_diabetes and stroke_prediction had no allocation of the label, so this fact sets
   the case apart (principles, "treat like cases alike unless a fact sets the new case apart"). Under the imputer the
   35% under-reporting (NBER WP 25143) is no label gap, because the imputer fills in the report and not the truth.
   Form, conceded from the precedent checker: a Must takes no exception, so this enters as an amendment that narrows
   SEL-7. Its wording: "unless the survey's own office fills the item for non-respondents from the same interview and
   flags the fill". That keeps diabetes and stroke out. The amendment is the curator's call.

2. Nothing in P4 or P5 fails. The only open validity question is the framing.
   Evidence:
   - LEAK-10 was checked on all 43 inputs and never triggered (column auditor). Income and POVPIP exclude SNAP (ACS
     Subject Definitions).
   - The income hot-deck carries no FS. On allocated-income rows the worth of income collapses: +0.0015 against
     +0.0143 on reported-income rows (column auditor, test I).
   - 0 exact copies across the split. Exactly one householder per occupied unit, with 0 exceptions in an independent
     re-read of the raw files.
   - The task gamer found nothing a deployed model lacks that adds more than +0.001 AUC.
   - 31 of 37 claims hold. The 4 refuted ones are in the wording, "none in the data" (claim auditor).
   Rule: LEAK-10, LEAK-16..21, LEAK-17, PROV-3, PROV-13 (all Must or Should, all hold).

3. The task is worth benchmarking, and it is large and real.
   Evidence: LightGBM reaches 0.914, against 0.897 for the linear model and 0.814 for the best single feature (paired
   SE 0.0004). The smallest class has at least 20,279 rows per test fold. 12.75M households over 10 years. The label
   drifts for real: 12.0% Yes, then 9.3% in 2019, then 10.9% in 2021.
   Rule: TP-1..5, TP-9 (P6). I concede that P6 does not rescue a P2 Must ("independent failures are not conflicts").
   This point only says the dataset is worth keeping once point 1 holds.

4. Under B the inputs and the metric are consistent, given one input fix that B makes necessary.
   Evidence: PAP, SSIP and HINS4 are known at the interview, and no LEAK rule bars them (column auditor E). Adding them
   gives +0.0065 with the householder's items and +0.017 with any person's (claim auditor 29).
   Rule: USE-6 (Must). Under B they go back in as features, a definition fix.
   Metric: the roc_auc fallback is consistent with anes_voting_2026 and with every binary fallback in the copy (MET-8,
   MET-11). log_loss would also be a defensible choice from context, because the imputer needs the level and the
   test-year share is under-predicted by 6-10%. That is the curator's choice. Neither metric blocks shipping.

5. The protected grounds are no exclusion, and under B they stay.
   Evidence: no subject or creator objects, and outreach or imputation is not harmful. That makes SEL-1 a tension, not
   an exclusion (builder; precedent checker D2). 7 CFR 272.6 binds state SNAP agencies, not the Census Bureau, so
   keeping everything is consistent under B (precedent checker).
   Conceded: the domain practitioner's point that the imputer needs these columns for the S2201 cross-tabs is an
   inference.
   If the curator keeps the agency actor instead, the mildest remedy is the column auditor's completed option B: drop
   sex, race, Hispanic origin and place of birth, and recode HHT, WKEXREL and FER, which still name the sex of 69% of
   householders. The cost is at most 0.0003 AUC. Either way the dataset stays.
   Rule: SEL-1 (P1); Tensions row "a factor the actor may no longer use".

6. The split is fixable on the remedy ladder, not a reason to exclude.
   Evidence: for the imputer the split auditor (point 5) and the precedent checker (via Tanzania issue 3) say the folds
   should follow processing within a survey year. Within-year IID scores 0.9158 / 0.9142 / 0.9171, against
   0.9120 / 0.9109 / 0.9148 for the temporal split.
   Rule: SPLIT-1, and the Tensions row "one regime, the one the use case implies". A re-split is rung 2 of the remedy
   ladder (fix the definition).
   Alternative, a weaker case and conceded as such: keep the temporal split with a note as a harder version that keeps
   the drift. The domain practitioner calls that "acceptable with a note".

7. The rest is notes, which need no decision, plus Should-level calls that never exclude.
   Notes (claim and split auditors):
   - Rewrite the no-gap sentence. The year-t file comes out 9-11 months after year t (Dec 4 2025 for 2024). Keep no
     gap under the lt_vehicle amendment, with the measured gain stated (+0.001 to +0.003 AUC). Moot if the split goes
     within-year.
   - Name the 2020 break and the emergency allotments (SPLIT-20).
   - Correct the wording of claim 29 (whose items were measured) and the zip dates (claim 4).
   - Call the shares "unweighted".
   - Add the allocation shares of the features (PROV-13).
   - Name the race-coding break and the 1M train cap.
   - Replace the "0.888" bullet of issue 1 with the class-composition numbers.
   Should-level calls:
   - CLEAN-21 (Should, P7): take the precedent checker's option a. General inflation is no scale change, as in four
     shipped siblings (noaa, kickstarter, lending_club, ames). Deflating instead is worth +0.0007 AUC. P7 never
     excludes.
   - Unit: households, consistent with MET-17 and USE-11. food_stamps stays a Duplicate under PROV-6, with its CC
     wording corrected.

Judgment record (advocate):
Verdict: ship after changes under framing B (the Census Bureau's item allocation as the actor).
Validity:
- SEL-7 is not met by option A. Under B it is met through SEL-2, by an amendment that narrows SEL-7 (curator).
- USE-5 fails for the outreach actor and holds for the imputer.
- USE-6: add PAP, SSIP and HINS4.
- LEAK-10 holds.
- SPLIT-1: re-split within the year for the imputer, or keep temporal with a note (curator).
- PROV-6 holds.
Value: TP holds (0.914 against 0.814 for one feature); roc_auc, or log_loss from context.
Quality: CLEAN-21 by amendment a; the notes listed in point 7.
Weighed: source + (Census PUMS), size +, drift +, niche actor -, hot-deck status quo -, opens 5 survey records -
(name them in the amendment).

</details>

<details><summary>Advocate rebuttal</summary>

ADVOCATE REBUTTAL: acs_food_stamps_2014_2024 (folder acs_food_stamps_2014_2024_1m), 2026-11-09

The critic and I end in the same place: A cannot ship; B ships if the curator narrows SEL-7; otherwise C. What is left
to dispute is small.

1. SEL-7 / USE-5. CONCEDE in full. A fails, and B needs the narrow amendment of SEL-7, not an exception. Without the
   amendment the verdict is C (`No`, SEL-7, USE-5). Two limits on the critic's effect numbers:
   - The 0.849 within <=200% of poverty and the 82% top-decile figure measure the outreach decision only. The imputer
     fills every blank household, so the full population is its population (domain practitioner, gap 2: "for the
     imputer this is no gap"). Under B they belong in the notes, not in the fit.
   - The named weaknesses of B (hot-deck today; scoring respondents while the imputer acts on non-respondents,
     NBER WP 29184) are agreed. They belong in fit_reason as gaps of an approximate fit (USE-8), as I listed them under
     "Weighed".

2. SEL-1 grounds. CONCEDE. It turns on the actor: keep all under B, with the reason in the notes; under A, the
   completed drop with the three recodes. My point 5 says the same.

3. PAP, SSIP, HINS4. CONCEDE. Under B, add them back as any-member household flags (USE-6, Must). Correct the note's
   wording and numbers under any framing (claim auditor 29). This is my point 4.

4. Split. CONCEDE the Must side. With the imputer as the sole actor, SPLIT-1 calls for folds within the survey year
   (split auditor 5; Tanzania issue 3's logic). I withdraw my softer alternative ("keep temporal with a note") as a
   default. It stays only as a curator's exception with the numbers (-0.002 to -0.004 AUC). Under A the gap-sentence
   fix holds as both of us wrote it.

5. Metric. DISPUTE the strength, CONCEDE the substance.
   - The level error is real: 0.0955 against 0.1018 to 0.1059.
   - But MET-8 is a Should, and its own text admits "a strictly proper rule or a ranking metric" (precedent checker D6).
   - roc_auc is the house fallback for all 112 binary fallbacks, and heart_disease kept roc_auc where the source scored
     calibration (2026-10-21/27).
   So log_loss from context is the better choice under B (noaa_storm_events_damage: the metric follows the actor).
   roc_auc is not a violation. It is a curator's weighing call, not a required change.

6. Notes. CONCEDE all. They are notes and record wording, with no data change. My point 7 covers them, and I add the
   protected-grounds list (nativity, difficulty items, age) from claim 31.

7. CLEAN-21 and WKW. CONCEDE, with one remark. Quality only (P7, Should), so it never excludes. Inflation goes by
   amendment (option a) or by deflating with the Bureau's factors (+0.0007). WKW to six bands is cheap and safe
   (principles step 3: fix it when cheap), so I accept harmonising it.

Net: no disagreement on validity. One weighing call differs: roc_auc against log_loss under B (MET-8, Should).
Joint recommendation to the mediator:
- B with the narrow SEL-7 amendment;
- use case and fit rewritten for the imputer;
- PAP, SSIP and HINS4 added;
- protected grounds kept, with the reason;
- split within the survey year;
- metric: the curator's call (log_loss preferred);
- notes fixed.
If the curator does not take the amendment: C.

</details>

<details><summary>Critic</summary>

CRITIC, OPENING BRIEF: acs_food_stamps_2014_2024 (folder acs_food_stamps_2014_2024_1m), 2026-11-09

Position: do not ship as defined (option A, outreach framing). It can ship only re-framed for the one actor who
predicts this label from these inputs, the Census Bureau's item allocation, and then rebuilt for that actor (points
1-4); otherwise `No` with `No Good Target / Scientific Discovery` (SEL-7). Points 5-7 are notes and quality, no reason
to exclude.

1. SEL-7 and USE-5 (P2/P3, both Must): the declared actor does not predict this label.
   Problem: the label is the household's own report, given in the interview that gives all 43 features. The declared
   actor (a state SNAP agency or outreach programme) already holds the label for every participant in its caseload,
   and the households it looks for (eligible, not receiving) sit in the "No" class.
   Effect on the task: a better model of this label ranks current recipients higher and eligible non-participants
   lower, the opposite of the outreach decision. Top 10% of scores within <=200% of poverty: 82.5/82.0/81.8% report
   Yes (domain practitioner, 2024/2023/2022). The headline AUC 0.91 is mostly easy well-off negatives (0.849 within
   <=200% of poverty).
   Evidence: claim auditor I3, 2024 window: 48,305 "No" households at or below 130% of poverty against 50,819 "Yes"
   in all; 64% of households at or below 130% report No. 35% of true recipient households report No (NBER WP 25143).
   The builder's own "rest of the signal is from answers the agency lacks" bullet is refuted (application-form items
   reach 0.9104 of 0.9152; claim 30), so nothing in issue 1 supports A. Precedents with the same mechanism:
   cdc_diabetes_health_indicators (No, 2026-10-15), stroke_prediction (No, 2026-10-26). The precedent checker finds A
   departs from them with no distinguishing fact, and a Must takes no exception (principles, Exceptions).
   Remedy: A cannot ship. Mildest working remedy is B: the actor is the Census Bureau filling blank FS answers
   (FFSP 1, 1.7-3.1% a year, flagged in the release), which makes "predicted by nobody" false for this item. Because
   SEL-7 is a Must, B needs the curator's narrow amendment of SEL-7 (precedent checker's wording: an item the survey
   office allocates and flags), not an exception, and the use case, fit_reason and population text rewritten for the
   imputer. If the curator does not take that amendment: C, `No` (SEL-7, USE-5). Weaknesses of B to name in the fit:
   the Bureau uses hot-deck today, the benchmark scores respondents while the imputer acts on non-respondents (MAR not
   a fact; NBER WP 29184).

2. SEL-1 tension row "a factor the actor may no longer use" (P1/P3, Must; follows point 1): the grounds answer
   depends on the actor, and the builder's drop is incomplete.
   Problem: under A, 7 CFR 272.6(a) bars the agency from age, race, color, sex, disability, national origin in program
   administration, yet sex, race, Hispanic origin, place of birth ship. The builder's option B drops householder_sex,
   but sex survives in household_type, work_experience_householder_spouse and householder_gave_birth_past_year for
   69.4% of rows with 100.0% agreement (column auditor A).
   Effect: under A, the drop would be a label on the notes, not a removal.
   Evidence: column auditor A (2.5M rows); cost of a complete drop <=0.0003 ROC AUC (column audit); precedent checker D2
   (bemtpl97 and the insurance family drop sex for the actor's legal constraint).
   Remedy: decide it with point 1. Under B (imputer, not bound by 272.6): keep all, with the reason in the notes.
   Under A (if the curator ships it against point 1): drop sex, race, Hispanic origin, place of birth and recode
   household_type (4 levels), work_experience_householder_spouse (12 levels) and gave_birth (blank -> "No or not
   asked"), as the column auditor specifies.

3. USE-6 (P3/P4, Must) and CLEAN-22 (P7, Must): PAP, SSIP and HINS4 are left out for a reason no rule gives.
   Problem: the notes drop them "as other benefits of the same 12 months". They are not part, consequence or encoding
   of FS (column auditor E), and every candidate actor has them: the imputer from the same interview, the agency from
   Medicaid data sharing (the lists outreach actually matches on, domain practitioner 1a).
   Effect: a known input is withheld: +0.0065 ROC AUC with the householder's three items, +0.017 (0.9142 to 0.9312)
   with any member's PAP/SSI/Medicaid; some member has Medicaid in 80.1% of Yes and 16.2% of No households (claim
   auditor 29, re-run). The note also misdescribes the run ("of any person"; it was the householder's items plus
   PINCP).
   Remedy: under B, add them back (household-level any-member flags). Under any framing, at least correct the
   note's wording and numbers.

4. SPLIT-1 (P4, Must) under B; SPLIT-10 (Should) under A: the split must follow the actor.
   Problem: the imputer fills a year's blanks from that year's donors, so its split is within the survey year, not
   temporal (split auditor 5). Under A, the splits_comment's no-gap reason is a wrong fact: the 1-year PUMS of year t
   comes out 9-11 months after t (2023 file 17 Oct 2024; 2024 file 4 Dec 2025), not "within the one-year step".
   Effect: small: within-year IID scores 0.002-0.004 higher than the shipped temporal split; a 1-year gap costs
   0.001-0.003 (split auditor; claim auditor 34).
   Remedy: under B, re-split IID within the survey year (or keep temporal as a recorded, conservative choice with the
   numbers, the curator's call). Under A, rewrite the gap sentence with the release dates and the measured gain
   (lt_vehicle_loan amendment allows no gap when stated), or set gap=1 (floor still met: 58.8%).

5. MET-8 (P6, Should) with MET-11 (Must, origin named): roc_auc does not score the imputer's decision.
   Problem: the imputer draws from the probability; its error is the level. A model fit on earlier years
   under-predicts the test year's share by 6-10% (mean 0.0955 vs 0.1018 in 2024; 0.0955 vs 0.1057 in 2023); ROC AUC is
   blind to it (domain practitioner 4, 6).
   Remedy: under B, declare log_loss from context, TableShift's accuracy named as the original (precedent: the metric
   follows a changed actor, noaa_storm_events_damage 2026-11-08). Under A, no metric on this label scores outreach,
   which is point 1 again.

6. Notes that state wrong or missing facts (writing; SPLIT-20 Should; PROV-9).
   - SPLIT-20: the history crosses the 2020 break unremarked; pre-2020-only training under-predicts the test-year Yes
     share by about 2 points; 2022/2023 lie in the emergency-allotment and Medicaid-unwinding years (split auditor 2-3).
   - Yes shares are unweighted (weighted 13.2/10.7/11.7%), say so (claim 16).
   - Zip dates "2025-08 to 2025-12" are wrong: 2015-10 to 2025-12 (claim 4).
   - The protected-grounds note omits nativity, the difficulty items and age (claim 31).
   - Householder race has a coding break at 2020 (Two or More Races 1.8% to 8.7%; column auditor D2).
   - The food_stamps record's CC ("same item and population filter") is no longer true of the build (D3).
   Remedy: notes and a record wording fix. No data change.

7. CLEAN-21 (P7, Should): three dollar columns mix ten years' dollars (median income 55,463 in 2014 to 84,266 in
   2024). Deflating moves ROC AUC +0.0006/+0.0007, same sign 4 of 4 fits (column auditor C). The builder's exception
   reason (POVPIP is comparable) does not set this case apart from four shipped siblings with nominal money
   (precedent checker D4). Weeks worked (WKW/WKWN) maps exactly onto one six-band scale and is dropped instead (column
   auditor D1). Remedy: the curator's amendment call (inflation is no scale change) or deflate with the Bureau's
   factors; harmonise WKW. Quality only: no reason to exclude.

Judgment record (critic):
Verdict: do not ship as A; ship only after changes (B, with points 2-5) if the curator amends SEL-7 narrowly; else No.
Validity: SEL-7 triggered (Must), USE-5 fails for the declared actor; SEL-1 row open, drop incomplete; USE-6 inputs
withheld; SPLIT-1 follows the actor; LEAK-10 holds (no column leaks; column auditor L1, L2, I).
Value: TP holds (LightGBM 0.914, linear 0.897); MET-8 favours log_loss under B.
Quality: CLEAN-21 open; notes to fix (point 6).
For the curator: issue 1 (A/B/C), then issues 2-5 follow from it.

</details>

<details><summary>Critic rebuttal</summary>

CRITIC REBUTTAL: acs_food_stamps_2014_2024 (folder acs_food_stamps_2014_2024_1m), 2026-11-09

Against the advocate's opening brief (points 1-7). We agree that A cannot ship and that B needs a narrow amendment of
SEL-7, or else the verdict is C. I dispute three things: how much weight Tanzania carries, "nothing in P4 fails", and
the advocate's later "exception" route for the split.

1. SEL-7 / SEL-2. CONCEDE the form: an amendment that narrows SEL-7, with the advocate's wording. It is not an
   exception, and SEL-2 alone does not carry it, as the advocate concedes. DISPUTE two supports:
   - Tanzania is weaker than cited. It shipped on the trip planner, a forward-looking actor, and the statistician was
     added beside it. SEL-7 was never raised there (precedent checker D1). Here the imputer would be the only actor.
     That makes this the first keep under SEL-7, against two exclusions, and not a case that follows Tanzania.
   - "Not a use case rephrased only to excuse a gap" (USE-9's weighed factor) is a weighing call, not a fact. The
     actor acts on 1.7-3.1% of households a year, by hot-deck today. Only the existence of the AAPOR 2026 talk is
     cited, not its content. The benchmark scores respondents while the actor fills non-respondents, and MAR is
     assumed (NBER WP 29184: errors are higher among imputed cases). The amendment also opens five survey records.
     These are minus factors the curator must weigh. They are not settled in favour of B.

2. "Nothing in P4 or P5 fails". CONCEDE for leaks and provenance: LEAK-10 holds on all 43 inputs, there are 0 copies,
   the hot-deck test (I) is clean, and 31 of 37 claims hold. DISPUTE for the split: under B the shipped temporal split
   breaks SPLIT-1 (Must) until the re-split is done (split auditor 5). The advocate's own point 6 says so. P4 holds
   only after that fix.

3. Worth benchmarking. CONCEDE (TP-1..5, TP-9). P6 does not rescue a P2 Must, as the advocate says.

4. Inputs and metric. CONCEDE USE-6: PAP, SSIP and HINS4 go back in as any-member flags (+0.017).
   CONCEDE the metric: MET-8's own text names roc_auc as the binary fallback, so roc_auc breaks no rule. log_loss from
   context (MET-11) is the better choice for the imputer: the level error is 0.0955 predicted against 0.1018-0.1059
   observed. It stays the curator's weighing call, and I withdraw "required" from my point 5.

5. Protected grounds. CONCEDE. The answer turns on the actor: keep all under B with the reason in the notes; under A,
   the completed drop with the HHT, WKEXREL and FER recodes.

6. Split. CONCEDE the opening brief's re-split under B (SPLIT-1, rung 2 of the remedy ladder).
   DISPUTE the advocate's rebuttal fallback, "keep temporal as a curator's exception with the numbers". SPLIT-1 is a
   Must, and a Must has no exceptions (principles, Exceptions and amendments). Temporal can stay under B only if the
   use case keeps a forward-looking actor beside the imputer (Tanzania's logic, issue 3). That actor would be the
   outreach agency, which fails USE-5. So under B the split is within the survey year, with no exception available.

7. Notes and Should-level calls. CONCEDE all the notes. CLEAN-21: I accept amendment (a) (inflation is no scale
   change), as in the four shipped siblings. Harmonising WKW to six bands is cheap and safe, and both sides accept it.

Net: no dispute is left on any validity outcome. Recommendation to the mediator:
- Ship only as B, with these changes: the narrow SEL-7 amendment naming the records it opens; use case and fit
  rewritten for the imputer, its gaps named (hot-deck, respondents only, small share); PAP/SSIP/HINS4 added;
  protected grounds kept with the reason; split within the survey year (no exception route); notes fixed.
- Metric: the curator's call (log_loss preferred).
- Otherwise C, `No` (SEL-7, USE-5).

</details>
