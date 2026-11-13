---
unique_name: tunisian_fraud_detection_challenge
name: Tunisian Fraud Detection Challenge
checked_by:
- Myunghwan
- Lennart
data_foundry_status:
- WIP (Triage)
claimed_by: Myunghwan
suggestion: 'Yes'
priority: 2
decision_markers:
- Selection Bias
tags:
- 'Samples: Over Time'
- 'Time: Dated'
- 'Target: Varying Delay'
- 'Target: Revised Later'
- 'Entities: Recur'
- 'Features: Read Later'
collections:
- New (BeyondArena)
original_source: Zindi
year: '2019'
domain: finance
required_split:
- Temporal (NON-IID)
problem_type: Regression
source_links:
- https://zindi.africa/competitions/tunisian-fraud-detection
- https://zindi.africa/competitions/supcom-tunisian-fraud-detection-challenge
v2_path: datasets/_dev/tabarena-v0pt2/tunisian_fraud_detection_challenge/dataset.py
source_row: 1015
type_adapter_id: curation-record-v1
---

## Comments

**Assessment (AI, 2026-10-31; authorized build verified):** Built accepted format-2 container `01a19475-b104-7ff0-82db-ed3aeb71f3a7` from clean definition commit `4bc27fd6d8b49f8c9c16446bb7e85132ce90943b`; checksum `v2:84d2d72d5ffe91a80168cd461f4367b63635ee74467d97d96c89e6de9ce57972`. Saved reload/checksum, exact accepted-frame comparison, source-label scorer and all four split memberships verified. Reproduction with only the traced Train.csv (9,679,520 bytes) gives the identical checksum; its private input ZIP passes CRC and source SHA-256 verification. Dataset build reports zero errors and zero unaccepted warnings, with the two curator-accepted annual-time warnings and two documented duplicate infos. All 21,295 rows, 103 predictors and four annual windows remain unchanged; existing qualified probes remain applicable by exact identity. Full tests:1,326 passed,177 skipped; changed definition passes Ruff lint/format. Repository-wide lint has inherited findings in unchanged files. Build and commit were explicitly requested by Myunghwan. No scientific decision or exception is added; claim/stage retained until integration into main, no publication inferred.

CC (2026-10-31, Myunghwan): "I think it's fine. accept all." Accept the dataset for a later build, both annual-time warnings with the presented reasons, and update required_split to Temporal (NON-IID). Temporal is preferred as closer to scanning a new year (superseded 2026-11-05: the task is the retrospective ranking of past fiscal years, with the taxpayer's earlier adjustments as held history; Lennart's issue 1 CC below). The previously accepted retrospective interpretation remains in force.

**Assessment (AI, 2026-10-31; final added-dataset review):** Applied the snapshot-bound ship verdict, issue 2 as implemented, and required_split update after independent consistency review. Accepted task_time_on_few_unique because six real annual cohorts provide four eligible outer windows and constrain inner validation; accepted meta_time_horizon_mismatch because January 1 encodes an entire fiscal cohort, not daily observations or audit duration. Both exact reasons are declared in accepted_check_warnings. The scored target, all 21,295 rows, 103 predictors, source RMSE and four annual split memberships remain unchanged. Historical recording/revision and outcome dates remain unknown; no rule exception, maturity clearance or change to the target is inferred. All dataset-specific review issues and field disagreements are settled; the full review/panel history is archived privately. Scientific acceptance is complete. The existing claim remains active until integration; claim stage and DF status are not changed by this verdict. No build, commit or publication was requested.

CC (2026-10-31, Myunghwan): Retrospective prediction is fine because looking back can identify more records worth investigating. Accept the bounded retrospective task framing (review issue 1); also check the contest test predictors. This is a partial decision, with no overall ship, annual-warning or record-field mark supplied.

**Assessment (AI, 2026-10-31; retrospective clarification):** Implement the analyst's retrospective archive investigation use, with scored adjustment withheld and historical training labels already held. Four fiscal-cohort tests measure transfer across accounting years, not historical operational refits. Original feature/audit/extraction and outcome dates remain unknown; fit stays approximate. Independent consistency review finds no SPLIT-10 departure for a past-refit claim no longer made. Full participant SupCom test mirror has 7,517 rows and 120 columns, exactly training minus target; mirror training blob matches supplied bytes. All 103 retained predictors are present and none wholly missing, including observed nonzero refund/regularization values. No new schema exclusion follows; LEAK-38 limits this evidence to the contest input contract. Test spans 2013–2018, so our annual tests do not reproduce the contest split. Authenticated original host test was not obtained. Every benchmark row, target, predictor, scorer and split remains unchanged; no test rows enter the benchmark. Issue 1 settled; issue 2, required_split disagreement and final inclusion remain pending.

**Assessment (AI, 2026-10-31; add-dataset qualification):** Added the source-label regression as an approximate historical annual-dossier task: all 21,295 rows, 103 predictors after 17 identity/redundancy removals, four temporal tests2015–2018, source RMSE on unchanged log1p labels with identity scoring transform. Four windows are all that meet the half-training floor; the original three-window screening proposal was expanded under SPLIT-15 before testing2015. Independent actual-container audits prove unchanged values/old split indices, correct fourth cohort and scorer/manual equality. Checks:26,0errors,2unaccepted warnings for six fiscal-year timestamps and annual-horizon encoding. Task probe RFmeanRMSE6.028 versusdummy7.049, beatsall4, noflags; feature models also beat taxpayer-history baselinesall4. Exact source-field availability and audit-label maturity remain cannot-verify, not passed. Registry invariance, refund-revision mechanisms and sparse block missingness are disclosed; focused conditional missingness tests do not identify an added target-dependent blank/fill mechanism. LEAK-38 supports provisional source-field retention with explicit revisit triggers, not causal clearance. Natural collisions across distinct taxpayer-years are retained; no exact full-feature copy including year crosses cutoffs. The supplied-source cohort does not establish national screening yield, independent audit appointments or recovered tax. The full independent panel supports retaining the qualified draft for curator judgment rather than inferring final admission. No accepted warning, final-inclusion decision, maturity exception, rule amendment, build or publication is inferred. Earlier screening statements about three windows and raw monetary scale are superseded. Priority 2: gap0 (none thin among133accepted definitions), usecase0 (approximate timing), source+1 (Ministry challenge and dictionary), shape+1 (21,295rows,103mixed-type predictors), risk-1 (unresolved label maturity/selection).

CC (2026-10-31, Myunghwan): Invoked tabarena-add-dataset on this candidate after the screening recommendation. Proceed to qualification of the annual pre-inspection audit-prioritization task; keep the source-provided log-scale target and annual temporal intent subject to actual timing/cohort checks. This is screening acceptance, not final inclusion or build authorization.

**Assessment (AI, 2026-10-31; screened-candidate review with supplied files):** Myunghwan supplied Train_tunisian-fraud-detection.csv and VariableDescription_tunisian-fraud-detection.csv and requested placement plus review-screened-candidates. Both are copied byte-for-byte to the private local warehouse as Train.csv and VariableDescription.csv, with SHA-256 manifest; originals preserved. This authorizes screening review, not an add-stage or final-inclusion verdict. Actual Train.csv has 21,295 rows and 121 columns (target plus 120 others, including IDs and years), 12,387 taxpayer IDs, no duplicate taxpayer-year pairs and six years, 2013–2018. Annual counts: 6,079 / 5,754 / 4,368 / 3,100 / 1,629 / 365. This measured count supersedes the page's broad over-25,000 description for the supplied training file. The source's target clarification states log(1 + adjustment), inverted by exp(x)-1, and confirms regression; retain supplied target and source RMSE. Targets span 0–23.5913, with 5,402 zeros (25.37%), no missing/negative labels. Underlying currency unit is unverified. The dictionary identifies RES_MNTRED as principal adjustment (target concept) and excludes RES_MNTRET penalties; neither is a separate raw column here. Historical binary-target prose is superseded. Inputs include taxpayer/legal/activity/obligation categories, annual VAT turnover/credits/payments, customs aggregates, government payments, third-party salary/rent/fee and VAT-suspended-invoice cross-checks. Raw numeric codes are not all continuous features. CTR_MATFIS is the taxpayer key, id administrative; EXE_EXERCI is year and RES_ANNIMP exactly duplicates it. Candidate temporal evaluation trains on earlier years and tests 2016/2017/2018, respectively 16,201/3,100, 19,301/1,629 and 20,930/365 train/test rows; each training side exceeds half of all rows. Both recurring and new taxpayers appear, which fits annual audit prioritization; grouped taxpayer evaluation is an alternative only for a deliberately cold-start use. No split is finalized or accepted. Primary limits: absent audit completion dates, unknown eligibility/availability of inspection/cross-check and refund fields, cohort-selection/representativeness, mixed missingness (customs and invoices often 80–94% missing), and some dictionary formatting/translation defects. No leakage, triviality, target reconstruction or model quality finding is claimed. Exact eligible features, causal training-label availability, cleaning, task probes and independent review remain add-stage work if the curator proceeds. Source terms restrict redistribution; this is a release condition, not a scientific rejection. Recommend proceed to add-dataset with the original log-scale target and an annual temporal design, conditional on timing/cohort checks. Curator choice remains proceed/later/no; suggestion TBD -> Yes, checked_by AI (UNVERIFIED), priority 3 and claim stage triage remain unchanged. No control-plane, definition, build, model run, commit or source publication.

**Assessment (AI, 2026-10-31; next-candidate selection):** Selected for the next screening review after Myunghwan rejected QoS and asked for the next available already-claimed candidate. Fresh official board confirms Myunghwan’s unexpired triage claim. Existing screened priority 3; source reports over 25,000 annual samples and numerous anonymized numeric fields. This preserves the session preference for a substantial dataset. Other triage candidates are smaller/unknown in size; Chicago and GeoAI have separate active/completed work and are not selected again. Source describes TARGET as additional tax liability, scored by RMSE: regression, superseding historical binary-classification prose below. Inspection-stage leakage and taxpayer/year split support require actual-data checks; no add-stage or inclusion verdict is inferred.

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-22):** `TBD -> Yes`, priority 3: taxpayer-year data of the Tunisian Ministry of Finance, the target the tax liability an inspection adjusted; a real audit-selection task, scored by RMSE.
- Source: Zindi "Tunisian Fraud Detection Challenge" (`tunisian-fraud-detection`, opened 2019-09-20, a knowledge competition, 1,529 participants), data "provided by the Tunisian Ministry of Finance includes variables about tax analysis, taxpayer inspection, and VAT returns"; "a subset of over 25,000 samples aggregated by year", "an anonymized dataset containing a large number of numeric variables"; "The "TARGET" column ... equals the amount of the tax liability that the taxpayer has to adjust". Files: Train.csv (9,679,520 B), Test.csv, VariableDescription.csv ("Full list of variables and their explanations"). The linked `supcom-tunisian-fraud-detection-challenge` (2020-09, a private Sup'Com student hackathon, 71 participants, "over 21,295 samples") ships files of the same sizes: the same data, a later re-run. Both read through the Zindi API.
- Use case: the tax authority, after returns are filed, picks taxpayers to inspect ("a supervised machine learning technique that detects potential fraudulent taxpayers will increase the operational efficiency of the tax supervision process"); fit direct when the features are return-time data, approximate if inspection-stage variables are in. Regime: grouped by taxpayer or temporal by year, to be read from the columns (rows are "aggregated by year"; whether an id or year ships is not checked); `required_split` left at `?`.
- Siblings and duplicates: none among `curation/records/` (grep tax, Tunisia: `fraud_detection_in_electricity_and_gas_consumption` is STEG electricity fraud, another task; `indabax_tunisia_2023` another hackathon). External collections: none found.
- Papers and pages: the two Zindi pages; no paper found.
- Metric: RMSE on the adjustment amount (Zindi Evaluation page: "The evaluation metric for this challenge is Root Mean Square Error"), the competition's choice (MET-4); inputs none. The old `problem_type` `Binary Classification` (AI-filled) is contradicted by the source: the target is an amount, so `Regression`.
- Risks for /add-dataset: "taxpayer inspection" variables may be recorded during or after the inspection that set the target (USE-4, LEAK checks); anonymized numeric columns, so the meaning rests on VariableDescription.csv; a likely zero-inflated, heavy-tailed target (check MET-3 for the scale); taxpayer-years of one taxpayer across folds if no id ships (SPLIT checks); download needs a Zindi login and the rules forbid redistribution (no criterion, EV-4).
- Priority: gap 0 (finance not thin; grouped would be thin but the regime is not confirmed), use case + (actor and decision named by the source), source + (a ministry's data with a variable description file), shape + (about 25,000 rows, many columns), risk - (inspection-stage variables, unknown grouping).

A Zindi competition to detect tax fraud using the Tunisian Ministry of Finance's data — a real-world, high-value tabular classification task with a clear binary target (fraud / not fraud). This maps well to the benchmark criteria: unique original source, predictive task, representative tabular ML. A human must verify dataset size after cleaning, the exact feature schema, whether a temporal or grouped (per-taxpayer) split is required, and class balance / potential leakage, and confirm data accessibility from Zindi.

---

Detect tax fraud using the Ministry of Finance of Tunisia's data

CC (2026-11-04, Lennart): the declared metric (RMSE, the competition's) is checked as declared (PR #33 review).

CC (2026-11-04, Lennart): the `Anonymized` data tag is dropped ("drop it"): only the taxpayer id was replaced; the columns are named.

CC (2026-11-04, Lennart): fiscal year 2018 is cut (LEAK-24, "do the change"), leaving three yearly windows 2015-2017; its three 2018-only VAT columns leave with it. The retrospective ranking stays ("okay let us keep it"). The source is Zindi's own file: Lennart's download (2026-11-04) is byte-identical to the file used, so no re-sourcing; the download description gives its SHA-256.

**Assessment (AI, 2026-11-04):** review panel (none): no panel ran for this dataset; its issues came from the light static review of the PR #33 page and the research behind each mark, and all are settled.

**Assessment (AI, 2026-11-04):** review panel (full, second pass after Lennart's PR #33 review): ship after changes (LEAK-24 holds for 2017, measured by four agents, so no further cut; LEAK-10 triggered by `CTR_CESSAT`, a status looked up at extraction, and by `TVA_RESTIT`, whose fill differs by label (1.30 against 1.03), both to drop; USE-10 and SPLIT-9 unsettled: the registry columns rebuild the dropped taxpayer id, and a test taxpayer's other-year labels help by +0.12 to +0.19 RMSE beyond their size, so known history or not yet known must be decided first; SPLIT-14 and MET-2 to MET-4 hold; the notes now give these numbers); disputed: USE-10 and SPLIT-9 (the previous label as a feature, or the audit planner's framing with the test taxpayers' training rows removed), SPLIT-10 (an exception or an application), LEAK-10 for `TVA_MTORDTVA` and `TVA_MTDJRTVA`; for the curator: issues 1-5. Priority 2: gap 0, use case 0, source +, shape +, risk - (use case: the source names the tax authority, but the fit is approximate, inspected dossiers only; source: Ministry of Finance data with a variable dictionary; shape: 20,930 taxpayer-years, 100 mixed inputs, temporal; risk: issue 1, a measured shortcut through taxpayer labels, and two LEAK-10 fields, issues 2-3).

CC (2026-11-05, Lennart): `CTR_CESSAT` dropped (Review issue 2, B; LEAK-10): the registry is a snapshot looked up at extraction, so a firm that ceased later carries "ceased" on its earlier years. Cost +0.015 RMSE, below the ±0.03 noise per split.

CC (2026-11-05, Lennart): `TVA_RESTIT` dropped (issue 3, B; LEAK-38's own clause, then LEAK-10; as kick and expresso_churn_prediction): its fill differs by outcome (observed/predicted 1.30 on zero-adjustment rows against 1.03). `TVA_MTORDTVA` and `TVA_MTDJRTVA` stay under LEAK-38.

CC (2026-11-05, Lennart): `Selection Bias` marker set (issue 4, B; USE-8): every row is an inspected taxpayer-year, while a real screening ranks all filers.

CC (2026-11-05, Lennart): the declared metric (RMSE on the supplied log label, the source's) is checked and stays as declared.

CC (2026-11-05, Lennart): the taxpayer's earlier adjustments are held history (Review issue 1, B; USE-10, LEAK-34): `previous_target` (the label of the taxpayer's most recent earlier fiscal year in the data) and `years_since_previous_target` ship as features, built from `CTR_MATFIS` over strictly earlier years, which then leaves (LEAK-33); on the three windows every test row's previous label is a training label. What sets this apart from lt_vehicle_loan_default_prediction: Tunisian in-depth verifications cover several open years (Ministère des Finances FAQ, https://www.finances.gov.tn/fr/faq?page=3), so ranking past years is the real decision, while a loan cannot be approved after the fact. LightGBM mean RMSE 5.863 to 5.533 (3 windows by 2 seeds; 6.021 to 5.476 with the codes as numbers, as the panel ran it). The late 2018 labels and the circumstantial hole test (0.794 vs 0.803) stay noted in the definition.

CC (2026-11-05, Lennart): the refund and regularisation fields stay under LEAK-38 as amended the same day (Review issue 5, B), named in `fit_reason` as kept. The 22 registry fields that stay were looked up at extraction, so LEAK-10 decides: they stay because no mechanism ties a registry change to the adjustment, unlike `CTR_CESSAT` (choice a; a LEAK-10 Cases row).

CC (2026-11-05, Lennart): ship. Every issue of the second-pass review page is settled, and a record with no open issue ships by default; the definition joins the accepted set, built on the curator's ask. The claim stays until the PR that takes it to `main` sets `DF: Yes`.

## Review

**Outcome:** added. The Tunisian Ministry of Finance's labelled taxpayer-years from the 2019 Zindi challenge: 20,930
rows of fiscal years 2013-2017 (2018 cut on your mark), the log of the principal tax adjustment as the source gives
it, scored by the source's RMSE on three yearly windows (test 2017, 2016, 2015; every earlier year trains). The review
panel recommends shipping after changes, with one validity question first (issue 1). Validity: LEAK-24 holds for
2017, measured by four agents (labels in band; the smaller count is row selection), so no further cut; USE-10 and
SPLIT-9 are not settled, because the dropped taxpayer id can largely be rebuilt from the registry columns and a test
taxpayer's labels from other years help the model by +0.12 to +0.19 RMSE beyond their size (issue 1); LEAK-10 is
triggered by `TVA_RESTIT`, whose fill differs by label (issue 3), and weakly by `CTR_CESSAT`, a status looked up at
extraction (issue 2); neither is applied yet; LEAK-38 holds for the other refund and registry fields, now with the
fill test in the note (issue 5 is its wording); USE-8 asks for the `Selection Bias` marker (issue 4); SPLIT-14 holds
(training shares 92.2, 77.4 and 56.5%); PROV-13: the download text named a file that does not exist; fixed.
Weighed: the source's actor (the audit planner) and the L&T move of 2026-11-04 against your kept retrospective
framing. Value: MET-2, MET-3 and MET-4 hold; RF 5.970 against a dummy at 7.056 on 3 of 3 splits. Quality: CLEAN-1
(`TVA_CRDFIN` is the closing credit) and the stale counts after the 2018 cut are fixed in the notes.

**Main points:** Give models the taxpayer's previous-year label, or remove the test taxpayers' training rows and
move to the audit planner's framing (1)? Drop `TVA_RESTIT` (3) and `CTR_CESSAT` (2)? Add `Selection Bias` (4)?
Record the refund fields as an application of LEAK-38 and amend its scope to named fields (5)?

**Record judgment:** valid. Your 2026-11-04 CC lines (RMSE as declared, `Anonymized` dropped, 2018 cut, the
retrospective ranking kept) are all in the definition. `data_foundry_status` still says `WIP (Triage)` while the
verdict is a final `Yes` and `claimed_by` is Myunghwan; the claims board writes both, so they are left as they are.

**Issues for Lennart:**

1. **Taxpayer history: give models the previous-year label, or remove the test taxpayers' training rows?**

   * **Problem:**
     - The taxpayer id (`CTR_MATFIS`) is dropped, but 64-75% of test rows have their taxpayer in training, and the
       kept columns let a model recognise many taxpayers and use their labels from other years[^known].
     - A model that does not re-identify taxpayers gets no history, so under your retrospective framing, where an
       analyst holds those labels, withholding them rewards re-identification over modelling.
     - Under the planner framing the labels would not yet exist[^unknown], so recurring taxpayers score 0.12 to 0.19
       RMSE better than they would in practice.
   * **Background:**
     - The 23 registry columns that ship (office, category, legal form, activity, obligation codes), which never
       change within a taxpayer, single out 59.6% of the 12,244 taxpayers on their own (claim auditor; 8,877 distinct
       values for 12,244 taxpayers, recomputed on the release).
     - The column auditor's and critic's "12,244 fingerprints for 12,244 taxpayers, one to one" counts 24 columns,
       which most likely include the dropped id `CTR_MATFIS` itself: without the tax office the 22 others single out
       only 12.4%.
     - The financial profile adds the rest: the task gamer's 24-column key links 4,967 rows to an earlier year.
     - Tunisian in-depth verifications can cover several open years
       ([Ministère des Finances FAQ](https://www.finances.gov.tn/fr/faq?page=3)).
   * **Experiments:**

     | Measurement (LightGBM, the 3 windows) | Value |
     |---|---|
     | Test taxpayers' training rows removed, beyond a size-matched random removal | +0.12 to +0.19 RMSE |
     | Year T-1 removed, beyond its size (almost all of it on rows of the same taxpayers) | +0.08 to +0.15 |
     | The same, once the test taxpayers' rows are removed | +0.025 to +0.055 (noise about ±0.03) |
     | Previous-year label as an explicit feature | mean RMSE 5.996 to 5.462 |
     | Task gamer: taxpayers relinked, earlier labels as features | gains 0.25 to 0.56 (4-9%) |

   * **Unknown:** whether a year's label was known when another year is scored; no audit dates exist. Labels
     persist: consecutive years agree on zero vs nonzero for 86% of pairs (62% if independent). The mediator compared
     two years of one taxpayer at the same distance apart: either the year between them is missing from the data (not
     inspected) or it is present (inside a run of inspected years). If one inspection settled a run of years, the
     second kind should agree more. They agree the same (two years apart: 0.794 with the middle year missing, 0.803
     with it present). That fits a persistent taxpayer behaviour more than one inspection settling several years at
     once (circumstantial[^ev6]).
   * **Either way:** `use_case`, `splits_comment`, Myunghwan's CC ("closer to scanning a new year") and the
     participant kit ("available for training") get one framing[^split1]. The critic adds that the definition's "no
     departure" from the late-label rule is wrong under the amended rule[^split10], since the 2018 cut documents late
     labels: under B the T-1 result is recorded as history, under A the filter removes it.
   * **Consistency:** the zero gap under the retrospective framing differs from lt_vehicle_loan_default_prediction
     (same day: the use case moved to the decision at disbursement, the gap measured at +0.0018 ROC AUC, the
     late-label rule amended to need measurements[^split10]). Here the same recent-label test is positive. B answers
     it as known history, A treats the case like L&T. B follows ieee_fraud_detection, where the history was an
     explicit column; A follows alfa_battle_2_0_task_2 in its filter.
   * **Panel:** B is the critic's default; A is the advocate's choice after its rebuttal; the mediator leaves the pick
     to you.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Planner framing, test taxpayers out of training | moves to the source's actor, the audit planner who ranks taxpayers once year N's returns are in (as lt_vehicle_loan_default_prediction moved on 2026-11-04); the T-1 labels mature until about N+4 (the 2018 cut shows late labels), so labels not yet known leave training[^unknown]; keeps `CTR_MATFIS` as a group column and drops each window's test taxpayers from training, with no gap on top (third row of the table) | the source's actor; treats the case like L&T | training shares become 81.6, 60.0 and 38.9%, so the 2015 window falls below the floor[^split14] and the task ships forced grouped from temporal[^split8] (grouped RMSE 6.048); a departure like alfa_battle_2_0_task_2's is not open, since a Must takes no exception, only an amendment; removing only the T-1 rows still leaves 2015 at 46.4% |
     | B | Previous-year label as a feature | keeps the retrospective framing: the labels are held history[^known], so the previous-year label and the years since it ship as features | keeps your framing of 2026-11-04; no cost to the windows; scores improve about 9% | needs `CTR_MATFIS` kept to build the feature; asserts that a year's label was known before the next year is scored, which the late 2018 labels make doubtful |
     | C | Retrospective, no history (implemented) | your framing ("okay let us keep it", 2026-11-04): three yearly windows with no gap, no taxpayer id and no history features; the numbers above are a note in the definition | none named | rewards re-identification over modelling |

   * **Recommendation:** B. It keeps your framing of 2026-11-04, and the hole test (one inspection settling several
     years shows no sign) leans to it. Pick A if you want the source's actor, as on L&T. **Decision:** B, the
     previous-year label as a feature, or A, the planner framing with the test-taxpayer filter, shipped forced
     grouped?

   **Notes for the AI:** rules: USE-10 (Must) and SPLIT-9 (Must), with LEAK-34; SPLIT-1, SPLIT-10, SPLIT-14 and
   SPLIT-8 follow from the choice. A ships under SPLIT-8.

   [^known]: **USE-10** (Must): for a known entity, its history is legitimate: the split is temporal and the previous
     outcome is a feature. **LEAK-34** (Must): an entity's own history under a temporal split is legitimate, also when
     it carries labels forward.
   [^unknown]: **SPLIT-9** (Must): a training row whose label is not yet known at the prediction point must not be in
     train.
   [^ev6]: **EV-6** (Should): say which evidence is proof and which is circumstantial.
   [^split1]: **SPLIT-1** (Must): the split is the one that most closely mirrors the real-world application.
   [^split10]: **SPLIT-10** (Should; applies SPLIT-9), as amended: when a label is known only some time after its
     row, a model refit at a window's start knows only the rows whose label had arrived; the notes give the
     measurements.
   [^split14]: **SPLIT-14** (Must): no window's train side holds less than 50% of the data.
   [^split8]: **SPLIT-8** (Must): a task that cannot meet the window rule ships in the closest regime that keeps the
     rows, tagged as forced from temporal.

   **Lennart (2026-11-05, change):** Option B: Previous-year label as a feature. Do B

   **Consistency check (AI, 2026-11-05):** B keeps the retrospective framing and builds a feature on it, although the
   2018 cut documents late labels. On 2026-11-04 you moved lt_vehicle_loan_default_prediction off the same retrospective
   framing to the decision at disbursement. What sets this dataset apart?
   - (a) Tunisian in-depth verifications cover several open years (Ministère des Finances FAQ), so ranking past years is
     the real decision, while a loan cannot be approved after the fact; written as the fact that sets it apart, and B is
     applied;
   - (b) treat it like lt: option A, the planner framing with the test taxpayers out of training, shipped forced
     grouped;
   - (c) reopen lt.

   Under B, `CTR_MATFIS` builds the two features and does not ship as an input. Give the letter in the note; nothing is
   applied until then.

   **Lennart (2026-11-05, change):** Reply (a): Tunisian in-depth verifications cover several open years (Ministère des
   Finances FAQ), so ranking past years … Option B: Previous-year label as a feature.

   **Resolved (2026-11-05, Lennart):** B, with (a). Two features ship: `previous_target` (the label of the taxpayer's
   most recent earlier fiscal year) and `years_since_previous_target` (1-4), both missing for 58.5% of rows;
   `CTR_MATFIS` builds them and is dropped. On the shipped windows every previous label comes from a training row, none
   from its own window. LightGBM RMSE 5.863 to 5.533 with the codes as shipped (categories), 6.021 to 5.476 with the
   codes as numbers, as the panel ran it. The fact that sets this apart from lt (verifications cover several open years)
   is a Cases row; the framing is one retrospective story in every field.

3. **Drop `TVA_RESTIT`, the VAT refund paid?**

   * **Problem:**
     - A model of whether `TVA_RESTIT` is filled, from filing-time covariates, is calibrated on positive-adjustment
       rows but not on zero-adjustment rows, so the field's fill differs by outcome.
     - The rule that keeps a competition host's fields with a note (the host-field rule) itself says such a field is
       dropped[^leak38], since then the general leak rule applies[^leak10].
     - Myunghwan's 2026-10-31 retention of the registry and refund fields under the host-field rule is a curator
       decision, so the drop needs your mark.
   * **Background:** a plausible mechanism: a refund request triggers a verification, and a refund is paid when it
     finds nothing. This is the revisit trigger the 2026-10-31 note named, so dropping applies that retention rather
     than overturning it.
   * **Effect on the task:** a planner choosing whom to inspect does not yet know whether a refund was paid after a
     clean check, so the field tells the model "nothing found" for those rows.
   * **Experiments:** two independent runs measured it (column auditor 1.27 vs 1.01, critic 1.30 vs 1.03), and the
     advocate's re-run reproduced the critic's. The fill model (5 folds grouped by taxpayer) gives observed/predicted
     1.03 on positive-adjustment rows and 1.30 on zero-adjustment rows (14.6% filled against 11.2% predicted); the
     95% interval of the gap is 0.026 to 0.042. `TVA_MTORDTVA` (22 filled rows, 14.8 against 12.7) and `TVA_MTDJRTVA`
     (4.03 against 3.61) are miscalibrated alike for both labels, so no differential. All three refund fields cost
     +0.022 RMSE together.
   * **Consistency:** follows kick and expresso_churn_prediction (2026-10-22); kick's fields were dropped at about 5x,
     and the rule has no size threshold.
   * **Panel:** the mediator recommends dropping `TVA_RESTIT`; the critic and, after its rebuttal, the advocate agree.
     The advocate does not oppose dropping the whole refund chain.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep (implemented) | `TVA_RESTIT` stays under the host-field rule; the note now gives the fill test | none named | the field's fill differs by outcome |
     | B | Drop `TVA_RESTIT` only | drops the one field whose fill differs by outcome; `TVA_MTORDTVA` and `TVA_MTDJRTVA` stay under the host-field rule with their numbers | applies the rule's own text; follows kick and expresso_churn_prediction | none named |
     | C | Drop all three refund fields | drops `TVA_RESTIT`, `TVA_MTORDTVA` and `TVA_MTDJRTVA` | the advocate does not oppose it | +0.022 RMSE together; the other two show no differential |

   * **Recommendation:** B, the mediator's recommendation. **Decision:** B, C or A?

   [^leak38]: **LEAK-38** (Should; narrows LEAK-10), its own text: "When a conditional test measures the mechanism
     (the field's ... fill, given the covariates known at the prediction point, differs by outcome), LEAK-10 applies
     and the field is dropped."
   [^leak10]: **LEAK-10** (Must): a feature holds only what existed at the prediction point and never gives the
     target away.

   **Resolved (2026-11-05, Lennart):** B. `TVA_RESTIT` left; `TVA_MTORDTVA` and `TVA_MTDJRTVA` stay under the host-field
   rule with their numbers.

2. **Drop `CTR_CESSAT`, the cessation status?**

   * **Problem:**
     - All registry fields are constant within each taxpayer, so they were looked up at extraction, not in the fiscal
       year, and a firm that ceased later carries "ceased" on all its earlier years.
     - Attributes looked up after the outcome leave, whatever their size[^leak10b].
     - Myunghwan's 2026-10-31 retention of the registry and refund fields under the host-field rule is a curator
       decision, so the drop needs your mark.
   * **Background:** cessation changes over time, and the ceased share falls from 5.5% (2013) to 2.7% (2017).
     `CTR_CESSAT` is kept as a category (63 rows carry an undocumented code 2) and is now named in the host-field
     note. The obligation codes are the same kind of snapshot but change slowly and stay.
   * **Effect on the task:** a planner scoring year N cannot know that the firm ceases later, so the model gets a hint
     that is not there in practice.
   * **Experiments:** ceased rows have mean target 10.06 against 11.88; dropping the column costs +0.015 RMSE (3
     windows by 2 seeds), so the model uses it; that is below the ±0.03 noise per split.
   * **Panel:** the mediator recommends dropping it; the advocate and the critic agree.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep as a category (implemented) | `CTR_CESSAT` stays, named in the host-field note | none named | a later status on earlier years |
     | B | Drop it | removes `CTR_CESSAT` | removes a hint the planner does not have; agreed by the mediator, the advocate and the critic | +0.015 RMSE, below the ±0.03 noise per split |
     | C | Keep with decoded codes | keeps it under the host-field rule with its 0/1 codes decoded into words[^clean12] | none named | a later status on earlier years |

   * **Recommendation:** B, the mediator's recommendation. **Decision:** B, drop, or C, keep it with its codes
     decoded?

   [^leak10b]: **LEAK-10** (Must, weak here): out are "attributes looked up after the outcome", whatever their size.
   [^clean12]: **CLEAN-12** (Should): reverse ordinal codes and one-hot blocks into categories with their labels.

   **Resolved (2026-11-05, Lennart):** B. `CTR_CESSAT` left (98 features); `dataset check` clean.

4. **Add the `Selection Bias` marker?**

   * **Problem:**
     - Every row is an inspected taxpayer-year, while a real screening ranks all filers, so the model never sees an
       uninspected return.
     - The use-case rules ask that the fit to the use case is written down, and the marker names this selection[^use8].
   * **Background:** `fit_reason` now names the selection; the fit stays approximate. selection.md: a concern flag,
     usually on `Yes` records.
   * **Panel:** the domain practitioner, the advocate, the critic and the mediator all ask for it.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | No marker (implemented) | the panel changes no record field | none named | the selection is named only in `fit_reason` |
     | B | Add the marker | adds `Selection Bias` to `decision_markers` | asked for by the domain practitioner, the advocate, the critic and the mediator | none named |

   * **Recommendation:** B: every panel role that looked at it asks for it. **Decision:** add or leave?

   [^use8]: **USE-8** (Must): write how closely the data mirrors the use case, its fit.

   **Resolved (2026-11-05, Lennart):** B. `Selection Bias` is set in the record.

5. **Record the refund, regularisation and registry fields under the host-field rule, and amend its scope?**

   * **Problem:**
     - The rule that keeps a competition host's fields with a note covers "anonymised fields" in its text[^leak38b].
     - You dropped the `Anonymized` tag on 2026-11-04 because only the taxpayer id was replaced and the columns are
       named.
     - In practice the criterion has been "timing cannot be tested", and this dataset is the third or fourth case, so
       an amendment is due.
   * **Consistency:** african_credit_scoring_challenge (`Amount_Funded_By_Lender`, 2026-10-20),
     sendy_logistics_challenge (`Distance (KM)`) and medical_facility_operational_data (`ExpectedDelayNextExam`, both
     2026-11-04) keep named host fields under it.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Application here only (implemented) | the note no longer says "anonymized inputs" and says why the tag was dropped | none named | the rule's text still says "anonymised fields" |
     | B | Same, plus an amendment | amends the rule's scope to "host-released fields whose timing cannot be tested" | the mediator's and the precedent checker's proposal; matches the cases kept under it | none named |

   * **Recommendation:** B, the mediator's and the precedent checker's proposal. **Decision:** amend the scope now,
     or keep it as an application here only?

   [^leak38b]: **LEAK-38** (Should), procedure: anonymised fields that may be post-outcome, in data a company released
     for its own competition, stay, with a note.

   **Lennart (2026-11-05, change):** Option B: Same, plus an amendment.

   **Consistency check (AI, 2026-11-05):** the amendment fits the cases kept under the rule (kick,
   expresso_churn_prediction and fraud_electricity are named fields too); its wording would keep "that may be
   post-outcome" and "for its own competition or challenge", with Cases rows for african_credit_scoring_challenge,
   medical_facility_operational_data and this dataset. The open point is the registry: issue 2 showed that every
   registry field was looked up at extraction, so their timing is known, and in
   distribution_transformers_at_cauca_department attributes looked up at extraction left under LEAK-10. What keeps the
   22 registry fields that stay here?
   - (a) no mechanism links a registry change to the adjustment (unlike cessation), recorded as a LEAK-10 Cases row; the
     amendment is applied as proposed;
   - (b) drop them too;
   - (c) widen the amendment to registry fields looked up at extraction.

   Give the letter in the note; nothing is applied until then.

   **Lennart (2026-11-05, change):** Reply (a): no mechanism links a registry change to the adjustment (unlike
   cessation), recorded as a LEAK-10 Cases row; t… Option B: Same, plus an amendment.

   **Resolved (2026-11-05, Lennart):** B, with (a). LEAK-38 is amended (one amendment with medical issue 9): fields that
   may be post-outcome, anonymised or named, whose timing no test can establish, in data the owner released for its own
   challenge, stay with a note and are named in `fit_reason`; the refund and regularisation fields are named there. The
   22 registry fields stay under LEAK-10 as an application (no mechanism ties a registry change to the adjustment,
   unlike `CTR_CESSAT`), with a Cases row.

**Review panel:** ship after changes (mediator). Tier full, second pass after your PR #33 review: twelve reports
(claim, column and split auditors, domain practitioner, blind reviewer, task gamer, precedent checker, advocate and
critic with one rebuttal each, mediator). Claims: 25; 16 hold, 6 refuted (four stale counts after the 2018 cut and
the missing `SOURCE_MANIFEST.json`, all fixed; the implied "no label shortcut", issue 1), 1 untested (the 7,517-row
contest test file), 1 held in part (byte identity with Zindi rests on your statement), 1 superseded. Blind review:
include with changes; its main concerns are the audited-only sample, the label timing and the same firms in train
and test. Task gamer: the best exploit relinks taxpayers across years and uses their earlier labels, 0.25 to 0.56
RMSE (4-9%) against noise of about 0.03 (issue 1); nothing else beat the noise. Agreed: 2017 kept (LEAK-24), the
three windows (SPLIT-14), target and metric (MET-2, MET-3, MET-4), dropping `CTR_CESSAT` and `TVA_RESTIT`, the note
and prose fixes. Disputed: USE-10 and SPLIT-9 on taxpayer history, the previous label as a feature (critic) or the
test-taxpayer filter (advocate), and how SPLIT-10 is recorded (issue 1); LEAK-10 for the rest of the refund chain
(issue 3).

<details><summary>Mediator</summary>

Verdict: ship after changes. Every Must is met or can be fixed in the definition. One validity question needs the curator's decision first: whether a taxpayer's other-year labels count as known history or as a label that is not yet known (issue 1).

```text
Verdict: ship after changes.
Validity: SEL holds; USE-1 holds by curator decision (retrospective framing kept, Lennart 2026-11-04; counter-argument
  in issue 1); USE-8: `Selection Bias` marker missing (add); USE-10 not met: known vs new is never decided, and taxpayer
  history can only be reached by re-identifying taxpayers (task gamer +0.25-0.56 RMSE) -> issue 1; SPLIT-9 depends on
  the framing -> issue 1; LEAK-24 holds for 2017 (measured, no further cut); LEAK-10 triggered, fixed (drop CTR_CESSAT;
  drop TVA_RESTIT through LEAK-38's own text); LEAK-38 holds for the other host fields, with notes; SPLIT-14 holds as
  defined; PROV-13: download text names a file that does not exist (fix).
Value: TP holds (RF 5.970 vs dummy 7.056, 3/3 splits); MET-2/3/4 hold (RMSE on log1p, Lennart 2026-11-04).
Quality: CLEAN-1 (TVA_CRDFIN is the closing credit), CLEAN-12 (CTR_RATISS, FJU_CODFJU 99 noted); writing.md: stale counts.
Weighed: framing: the source's actor and the L&T move (-) against the curator's kept retrospective framing (+).
For the curator: issue 1 (framing -> previous label as a feature, or filter out the test taxpayers' training rows);
  issue 2 (LEAK-38 scope for named fields).
```

**Changes to make now (no decision needed)**

1. **Drop `CTR_CESSAT`** (LEAK-10, attribute looked up after the outcome). Both sides agree.
   - It is constant within each taxpayer.
   - The ceased share falls from 5.5% (2013) to 2.7% (2017), so later cessations are written onto earlier years.
   - The model uses it: +0.015 RMSE when dropped.
2. **Drop `TVA_RESTIT`** (LEAK-10, through LEAK-38's text: "fill ... differs by outcome → dropped"). Both sides agree after the rebuttals.
   - Three runs reproduce the differential: observed/predicted fill 1.30 on zero-adjustment rows against 1.03 on positive rows, CI [0.026, 0.042].
   - LEAK-38 sets no size threshold.
   - This is the revisit trigger the existing note names, so it does not overturn the 2026-10-31 retention; it applies it.
3. **Keep `TVA_MTORDTVA` and `TVA_MTDJRTVA` under LEAK-38** and put the fill numbers in the note (4.03 vs 3.61 and 14.8 vs 12.7: miscalibrated alike in both groups, no differential). Name `CTR_RATISS` (control sweep; 233 rows, R² about 0.001) in the note.
4. **Add the `Selection Bias` marker** and name the selection in `fit_reason` (USE-8: every row is an audited dossier).
5. **Add the 2017 measurements to the notes** (amended SPLIT-10: "the notes give the measurements"):
   - zero share 0.249; nonzero median 15.72 vs 15.80 (p=0.36); p90 18.35;
   - conditional residual +0.18 for 2017, like 2016, against −0.71 for 2018;
   - the count ratio of 0.53 is selection, not label censoring. Probe 13's z of −4.6 compares with a flat band and overstates the break (EV-9).
   - Add one line on the left-truncated 2013 cohort (SPLIT-20).
6. **Fix the stale prose** (writing.md):
   - "six annual markers / cohorts" → five cohorts; "four outer windows / annual holdouts" → three. This is in `accepted_check_warnings["task_time_on_few_unique"]` and README lines 64 and 236. The acceptance stands.
   - "All 103 retained predictors" → 100 inputs today, 98 after changes 1 and 2.
   - "No row is filtered" → "no row filtered besides 2018".
   - "shrinking latest cohort (365 rows)" → 2017, 1,629 rows.
   - Remove "anonymized" from `row` and from the LEAK-38 note (follows Lennart's tag drop).
   - In `changes`, word "inspections were still open" as an inference.
7. **Fix the download text** (PROV-13, EV-7): `SOURCE_MANIFEST.json` does not exist. Cite the two SHA-256 values and `MIRROR_SOURCE.txt`, and name the participant mirror (MohamedNennouche/Tunisian-Fraud-Detection, `SUPCOM_Train.csv`) as the copy used. Identity with Zindi rests on Lennart's statement.
8. **Add notes:**
   - `TVA_CRDFIN` is the closing credit: it carries over to the next year's `TVA_CRDINI` in 89.9% of 6,180 consecutive-year pairs (CLEAN-1).
   - 59% of the squared error comes from true zeros, so RMSE on log1p mostly scores whether an audit finds anything (MET-4 note only).
   - The source's test spans 2013–2018 and has no released labels, so SPLIT-19 cannot be followed. State this departure in `splits_comment`.
9. **Tooling:** `assert df.shape == (21295, 121)` (dataset.py line 108) breaks `leak_probes.py --raw`, because lineage tracing adds a tag column. Assert on the raw columns without the tag, then run the raw probe.

**Issues for the curator, ranked**

**1. Framing, and whether taxpayers are known or new (P3/P4; USE-1, USE-10, SPLIT-9 Must; SPLIT-10, SPLIT-14, SPLIT-8).**

- **Problem.** 64–75% of test rows have their taxpayer in training. The 24 registry columns identify all 12,244 taxpayers one to one, so dropping `CTR_MATFIS` does not hide the taxpayer. Yet the definition withholds the previous outcome.
- **Effect.**
  - Dropping the test taxpayers' training rows costs +0.12 to +0.19 RMSE beyond a size control.
  - Year T−1 alone is worth +0.08 to +0.15 beyond its size, almost all of it on rows of the same taxpayers (N1).
  - A participant who rebuilds identities gains 0.25 to 0.56 RMSE (4–9%; noise is about ±0.03).
  - Both sides now agree that a note alone does not satisfy USE-10.
- **Decisive experiments I ran**:
  - `hole.py` tests whether one audit settles several fiscal years together. At equal lag, pairs of years with a gap between them agree as much as pairs of consecutive years. Lag 2: 0.794 vs 0.803 (r 0.52 vs 0.53). Lag 3: 0.759 vs 0.711. Exact repeats of a nonzero label are about 1%. Same-audit labelling predicts more agreement inside a run of consecutive years; none shows. The co-movement looks like persistent taxpayer behaviour (EV-6, circumstantial).
  - `narrow.py` asks whether a milder filter keeps the 2015 window above the 50% floor. Dropping only the test taxpayers' T−1 rows leaves 2015 at 46.4% training share and removes only +0.09–0.10 of the +0.15–0.18 gain. The full filter leaves 38.9%. No filter keeps 2015 at or above 50%.
- **Each side's best evidence.**
  - Critic: USE-10 says "the previous outcome is a feature" for a known entity. The current middle state meets neither branch.
  - Advocate, after the rebuttal: under the source's planner framing, T−1 labels mature until about N+4 (the 2018 cut shows this), so they are not known when year T is scored, and SPLIT-9 applies, as in alfa_battle_2_0_task_2.
- **The decision.**
  - **(b) Keep the retrospective framing** (the decision standing now). Labels are held history (LEAK-34). Ship the previous-year label, with years since, as a feature (USE-10). Measured: 5.996 → 5.462 RMSE. The hole test supports this reading. The SPLIT-10 notes then record N1 as known history, not a shortcut.
  - **(a) Move to the source's actor, the DGI audit planner** (as L&T moved on 2026-11-04). Then SPLIT-9 applies: keep `CTR_MATFIS` as a group column and drop each window's test taxpayers from training. N2 shows no further gap is needed (residual +0.025–0.055, about noise). The 2015 window falls below the floor, so either ship under SPLIT-8 (`ForcedGroupedFromTemporal`, grouped RMSE 6.048) or take a SPLIT-14 departure like alfa_battle. The register already flags that departure as an exception to a Must.
  - Either way, rewrite `use_case`, `splits_comment`, the CC's "scanning a new year" and the participant kit's "available for training" so they state one framing (SPLIT-1).

**2. LEAK-38 scope for named fields (P4 Should, procedure).** The remaining refund, regularisation and registry fields are named, and Lennart dropped the `Anonymized` tag. LEAK-38's text covers "anonymised" fields. In practice the criterion is "timing cannot be tested": african_credit_scoring_challenge, sendy_logistics_challenge, medical_facility_operational_data. **Decision:** record the retention as an application and reword the note (precedent checker's option a), and propose the scope amendment that is now due (option d).

**Agreed facts**

- **Data.** Train.csv has 21,295 rows, 12,387 taxpayers and 6 years; 20,930 rows ship. Both SHA-256 values match.
- **Target and metric.** The target is log1p(principal adjustment); discussions 448 and 436 confirm the log and RMSE. 25.3% of labels are zero. A dummy scores 7.04 / 6.98 / 7.16.
- **2017.** Its labels are within the 2013–2016 band (four independent agents). Only 2018 shows the censoring signature.
- **Splits.** Training shares are 92.2 / 77.4 / 56.5%. 0.0% of test rows have a copy in training once the year is included.
- **Signal.** LightGBM 5.96–6.03 against dummy 7.04–7.16. No flaw that hurts an honest model: training on the last 1–2 years only is no better, and row order, formats, transforms and the train-vs-test classifier found nothing beyond noise.
- **Gamer exploits mapped.**
  - Exploit 1, 1a and 1b map to USE-10 / LEAK-34 / SPLIT-9. They are new: no `Potential leak, kept on purpose:` note covers them, and CC 10 states no gain. This is issue 1.
  - Digit formats, rate × base formulas and train-vs-test drift give no gain beyond noise and are signal, not leaks.
- **Blind reviewer's points.** The codes are already categorical, the log target is stated and the licence is declared. 21,295 training rows plus 7,517 test rows is above the source's "over 25,000".
- **Metric.** RMSE stays (Lennart 2026-11-04, MET-4). The practitioner's money-capture result (top 10%: 0.31–0.43 for the RMSE-best model against 0.58–0.69 for a two-part model) is recorded as a note, not an issue.

**Consistency with precedent**

- **2018 cut** follows sf_permit_time. **2017 kept** follows alfa_battle_2_0_task_2 (end dip noted), ames_housing and perth_house_prices.
- **Xente is set apart:** no review step in the zero share. It changes smoothly with size, from 0.12 to 0.46 over TVA_TOTDUE deciles.
- **TVA_RESTIT drop** follows kick and expresso_churn_prediction (2026-10-22). Kick was dropped at about 5x, not 20x, and the rule has no threshold.
- **No gap** against lt_vehicle_loan_default_prediction (2026-11-04): option (a) of the checker's consistency check ("the shortcut test shows nothing") is closed. N1 is positive (+0.08–0.15) where L&T's was +0.0018. So "what sets this case apart" is answered only through issue 1: (b) makes it known history, (a) treats it like L&T.
- **SPLIT-9 precedents.** The hole test moves this case toward ieee_fraud_detection and away from alfa_battle_2_0_task_2 on whether one event sets several labels. It does not settle label maturity under the planner framing.
- **Register.** SPLIT-10 is flagged amendment_due (6 datasets). Option (a) of issue 1 would add a SPLIT-14 departure, a flag already raised on alfa_battle_2_0_task_2 and lending_club.
- **Tag drop.** One line should say why `Anonymized` was dropped here but kept on sendy_logistics_challenge (only the taxpayer id was replaced here; Sendy's values were transformed).

</details>

<details><summary>Claim audit</summary>

**Focus question (focus.md): is 2017 partly censored like 2018?** No. The test could have refuted it and did not, so LEAK-24 holds without a further cut.
- **Row counts.** The 2017 count is part of a steady decline. Year-on-year ratios are 0.95, 0.76, 0.71, 0.53 from 2014 to 2017, then 0.22 for 2018. Probe 13 compares 2017 with a flat band over earlier years, so its z of -4.6 overstates the break (EV-9).
- **Labels, unconditional.** The 2017 labels match 2013-2016: Mann-Whitney p=0.80 (the "p=0.8" claim holds), KS p=0.59. The median of nonzero labels is 15.72 against 15.80 (p=0.36), and the zero share is 24.9% against 25.3% (p=0.67).
- **Labels, conditional on features.** I fitted gradient boosting and read the mean residual (y minus prediction) per test year:

| Trained on | 2016 | 2017 | 2018 |
|---|---|---|---|
| 2013-2014 | +0.57 | +0.52 | -0.41 |
| 2013-2015 | +0.23 | +0.34 | -0.57 |
| 2013-2016 | – | +0.18 | -0.71 |

2017 behaves like 2016. Only 2018 carries the censoring signature.

**Claims table**

| # | Claim | Source | Test | Result | Evidence | Rule |
|---|---|---|---|---|---|---|
| 3, 11, 30 | 21,295 rows, 12,387 IDs, 5,402 zeros, range 0-23.5913, years 6,079/5,754/4,368/3,100/1,629/365 | CC, TaskSummary.row | Recount from the raw file | holds | Exact match. 20,930 rows ship. | EV-1 |
| 4, 11 | Target is log(1+principal adjustment); penalty excluded | predicted, CC | Discussion 448, data page, dictionary | holds | 448: "applied the log(1 + x)". Data page: "amount of the tax liability that the taxpayer has to adjust". Dictionary: RES_MNTRED is the variable to predict. RES_MNTRET is not in Train.csv. | USE-5 |
| M | RMSE on the supplied log target, from the competition | metric | Discussions 436 and 448, competition page | holds | 436: "Evaluation Metric for this challenge is RMSE not Log Loss". The page names Root Mean Square Error. The `target` column is on the log scale. The zindi.africa reference redirects (301) to zindi.world, so it resolves. | MET-3, MET-4 |
| M | Computable on every fold | metric | Score a train-mean dummy per fold with `scorer` | holds | 2017: 1,629 rows, RMSE 7.037. 2016: 3,100, 6.976. 2015: 4,368, 7.156. Matches a by-hand RMSE. No scoring columns needed. | MET-2 |
| 6, 14, 20 | Splits 19,301/1,629, 16,201/3,100, 11,833/4,368; earlier windows break the 50% floor | CC, splits_comment | `make_splits` | holds | Train shares 0.92, 0.77, 0.565. A 2014 window would train on 0.29. | SPLIT-14 |
| 6 | Both recurring and new taxpayers occur | split | Taxpayer first-seen year | holds | New share per test year: 25.4% (2017), 28.7% (2016), 36.4% (2015). | SPLIT-13 |
| **I-1** | The split mirrors the use case: training labels give no shortcut to a test row's outcome (implied) | split, CC 10 ("training labels already held") | Remove the test cohort's own taxpayers from training; check how labels track across years | **refuted as unconditional; a curator call** | See finding 1 below. | SPLIT-9 (Must), SPLIT-13, USE-10 |
| 13 | 2018 median 1.2 log units lower, about 3x, p=6e-16, in every category | CC | Mann-Whitney test on nonzero labels, per CTR_CATEGO_X | holds | 14.63 vs 15.80, p=5.8e-16. Per category: C -1.28, M -0.78, P -1.34 (all p≤8e-4). | LEAK-24 |
| 13 | Three 2018-form VAT columns are constant without 2018 | CC, code | Count unique values in 2013-2017 | holds | Only 0 or NaN. No other column becomes constant. | CLEAN |
| 15 | Copies and zero-with-block-missingness drops | CC, code | The asserts in `_clean` | holds | Masks equal TVA_TOTDUE (1,690 missing) or SND_MNTPRD_I/E/A. | CLEAN |
| 15 | "No row is filtered" | CC bullet 7 | Read against the code | **refuted (stale)** | 365 rows of 2018 are filtered. | writing.md |
| 16 | 63 CTR_CESSAT code-2 rows; RATISS 0/2; months numeric; SND_MNTAIR_I/A undefined; TVA_CRDFIN described as "Initial Credit" | CC | Count values, read dictionary | holds | Counts 63, 21,062/233. TVA_MOIDEB/TVA_MOIFIN are float. Dictionary rows 94 and 108 are NaN. | CLEAN |
| 17 | "All 103 retained predictors … our four annual holdouts" | CC bullet 9 | Count shipped features | **refuted (stale)** | Now 100 inputs (99 plus fiscal_year) and three holdouts. | writing.md |
| 17 | SupCom test has 7,517 rows covering 2013-2018 | CC | Not available; checked size only | untested | The Zindi Test.csv size of 3.2 MB is consistent with that row count. | EV-7 |
| 18 | 23 registry fields invariant across 5,990 repeated taxpayers | CC LEAK-38 | Group by taxpayer | holds | 0 fields vary. Implied: the fields are an extract-time snapshot, not as-of values. | LEAK-38 |
| 18 | LEAK-38 note covers the registry fields | CC | Dictionary lookup | holds, with a gap | CTR_RATISS is "Ratissage", a control sweep operation (a process field), and the note does not name it. Code 2 has mean target 13.48 vs 11.76; effect R² is about 0.001. CESSAT=1 has mean 10.09 vs 11.86. | LEAK-38 |
| 19 | 7 excess copies, 19 conflicting variants, 31 rows in conflict groups, no copy across the cutoff | CC | Recount on the shipped columns | holds | 7; 12 groups holding 31 rows (19 excess). 0.0% of test rows have a train copy once fiscal_year is included. | LEAK-16..21 |
| 19 | "shrinking latest cohort (365 rows)" | CC bullet 11 | Read against the code | **refuted (stale)** | The latest cohort is 2017 with 1,629 rows. | writing.md |
| 9, 21 | "Six annual markers", "six genuine cohorts; four outer windows" | CC 1, accepted warning | Count | **refuted (stale)** | Five cohorts, three windows. The README repeats this at lines 64 and 236. | writing.md |
| 22 | Horizon warning reason | accepted warning | Read | holds | – | SPLIT-12 |
| 23 / 28 | 103 predictors, four windows, RF 6.028 | assessments | Superseded by the 2018 cut | superseded | Current task probe: RF 5.970 vs dummy 7.056, 3 of 3 splits. | – |
| dl | "SOURCE_MANIFEST.json records identities" | download_description | List the warehouse folder | **refuted** | No such file. MIRROR_SOURCE.txt is there instead. | PROV-13, EV-7 |
| dl, 36 | Files byte-identical to Lennart's Zindi download | download_description, CC | sha256 of the working files | partly | Both hashes match the stated values. The file was fetched from a participant GitHub mirror (SUPCOM_Train.csv). I cannot reach the Zindi download (needs login). | PROV-2 |
| 8 | fit approximate | fit | Read | holds | – | USE-8 |
| 32 | 2019 Zindi competition, over 25,000 samples | screening | Data page | holds | "a subset of over 25,000 samples aggregated by year". Train.csv listed at 9.2 MB, which matches 9,679,520 B. | PROV |

**Refuted and untested, ranked**

**1. Same-taxpayer label shortcut across the cutoff (P4, SPLIT-9 Must, SPLIT-13, USE-10). This is a validity question for the curator.**
- **Labels move together across years.** For the same taxpayer, consecutive-year labels correlate at r=0.62. The chance of a zero is 0.70 after a zero year and 0.09 after a nonzero year, against a base rate of 0.25.
- **Years cluster in blocks.** 21.7% of consecutive-year pairs carry an identical label. 69.6% of multi-year taxpayers have contiguous years. That is the pattern of one audit covering several fiscal years, so the labels would arrive at the same moment.
- **The model can re-identify taxpayers.** CTR_MATFIS is dropped, but the 23 invariant registry fields alone pin down 59.6% of taxpayers.
- **The model uses it.** I removed the test cohort's own taxpayers from each training side and compared RMSE:

| Test year | Recurring rows | Recurring, full train | Recurring, history removed | New rows | New, full train | New, history removed |
|---|---|---|---|---|---|---|
| 2017 | 1,216 | 6.02 | 6.39 | 413 | 5.65 | 5.68 |
| 2016 | 2,210 | 6.02 | 6.35 | 890 | 5.78 | 5.95 |
| 2015 | 2,776 | 6.15 | 6.61 | 1,592 | 5.94 | 6.04 |

  Recurring rows lose about 0.3-0.45 while new rows barely move. Roughly a quarter to a third of the model's gain over the dummy on recurring rows (about 1.2) comes through a taxpayer's other-year labels.
- **What it means.** CC 10 accepts "historical training labels already held". That holds only if those labels come from earlier audits, not the same audit. The README states neither, and no audit dates exist.
- **Remedies, mildest first:**
  - The curator states that an analyst holds the same audit's other-year results, and the note carries these numbers (as the SPLIT-10 amendment of 2026-11-04 does).
  - Otherwise drop the test taxpayers' rows from each training side, as in alfa_battle_2_0_task_2. That leaves 2015 at 8,137 of 20,930 rows (39%), below the floor, so it would drop to two windows or need a SPLIT-8 decision.

**2. Stale prose after the 2018 cut (procedure, writing.md; Should).** Five places are wrong:
- "Six annual markers"
- "No row is filtered"
- "All 103 retained predictors … four annual holdouts"
- "latest cohort (365 rows)"
- accepted warning: "six cohorts … four outer windows"

The warning text also appears in README lines 64 and 236. It misleads readers but does not change the data. Remedy: reword to five cohorts, three windows, 100 inputs, a latest cohort of 1,629, and "no row filtered besides 2018".

**3. SOURCE_MANIFEST.json does not exist (P5, PROV-13; reproducibility).** Remedy: remove the sentence, or point it at the stated SHA-256 values and MIRROR_SOURCE.txt.

**4. CTR_RATISS ("Ratissage", a control-sweep process field) is not named in the LEAK-38 note (P4, LEAK-38 Should).** The effect is negligible: 233 rows, R² about 0.001. Remedy: name it in the note.

**5. Untested:**
- The 7,517-row contest test file covering 2013-2018 (no file available).
- A direct check of Lennart's Zindi download (login needed).
- The `--raw` leak probe. It fails at `assert df.shape == (21295, 121)` because lineage tracing adds a tag column. This is a tooling defect, not a data finding.

**The metric holds:** RMSE is the competition's metric, on the log scale it scores, and it is computable on every fold (MET-2, 3, 4).

</details>

<details><summary>Column audit</summary>

**Column audit: `tunisian_fraud_detection_challenge` (second pass, 2026-11-04)**

The definition's frame has 20,930 rows and 101 columns: 99 numeric or categorical features, `fiscal_year` (datetime, also a model input) and `target`. The prediction point is the retrospective, archived taxpayer-year dossier: the year's VAT returns and third-party cross-checks exist, and the inspection's principal adjustment is withheld (`task_summary`, CC 2026-10-31).

**Focus question: is 2017 partly censored, as 2018 was?** No, not in its labels. The fall in 2017's row count is a selection effect on the rows; it does not shift the label.

| year | n | zero share | nonzero median | nonzero p10 / p90 |
|---|---|---|---|---|
| 2013 | 6079 | 0.265 | 15.70 | 13.40 / 18.09 |
| 2014 | 5754 | 0.249 | 15.83 | 13.53 / 18.30 |
| 2015 | 4368 | 0.258 | 15.85 | 13.50 / 18.31 |
| 2016 | 3100 | 0.236 | 15.87 | 13.21 / 18.34 |
| **2017** | 1629 | 0.249 | 15.72 | 13.11 / 18.35 |
| 2018 (cut) | 365 | 0.277 | 14.63 | 10.95 / 18.00 |

- **2017 against 2013-2016, nonzero labels:** Mann-Whitney p = 0.36, median difference -0.08. 2018 against 2013-2017 gives p = 8e-16 and -1.16.
- **Within each taxpayer category (2017 median, with the 2013-2016 range):** C 15.68 (15.79-16.02), M 16.70 (16.58-16.82), P 14.60 (14.58-14.71). All are in band except C, which is 0.11 below.
- **Row counts:** they fall steadily from 2014, at ratios 0.95, 0.76, 0.71, 0.53 per year, before the 2018 collapse (0.22). That fits fewer recent years having been opened by audits.
- **Verdict:** LEAK-24 does not trigger for 2017, so no cut. The notes should say that the probe-13 count flag was tested and is selection, not label censoring.

**Columns** (codebook: `VariableDescription.csv`)

| column(s) | meaning | known at prediction? | dtype and cleaning | verdict | rule |
|---|---|---|---|---|---|
| `fiscal_year` | year of the return (from `EXE_EXERCI`) | yes | datetime on 1 January; `RES_ANNIMP` copy dropped | fine | CLEAN-14 |
| `BCT_CODBUR` | tax control office (158 codes) | registry snapshot | category | fine; part of the taxpayer key (problem 2) | CLEAN-14 |
| `CTR_CATEGO_X` | taxpayer category C/M/P/N (N: 8 rows, 7 zero) | snapshot | category | fine | |
| `FJU_CODFJU` | legal form (16 codes; 99 = 48.8% of rows) | snapshot | category | question: is 99 "other/unspecified"? Codebook is silent, keep the level | CLEAN-10 |
| `CTR_CESSAT` | 0 active, 1 ceased; 2 undocumented (63 rows) | **no: status at extraction, not in the fiscal year** | category, codes not decoded | **leak (weak)**, problem 1 | LEAK-10; CLEAN-12 |
| `ACT_CODACT` | activity code (525 codes) | snapshot | category; leading digits are a nomenclature (sector) | fine | CLEAN-14 |
| `CTR_OBLDIR`, `OBLACP`, `OBLRES`, `OBLFOP`, `OBLTFP`, `OBLDCO`, `OBLTVA`, `OFODEC`, `OFODEP`, `OFODET`, `OBLAUT`, `OBLASS`, `ODTIMB`, `OBLTCL`, `OBLTHO`, `OBLDLI`, `OBLTVI` | tax obligations; code values (1/2/3/5/9) have no words | snapshot, invariant per taxpayer | category; NaN in the same 10 rows, kept missing | fine (LEAK-38 note covers them) | CLEAN-14, LEAK-38 |
| `CTR_RATISS` | "ratissage" (sweep), codes 0/2 undocumented | unknown (selection campaign?) | category | question: 232 rows, mean target 13.49 vs 11.78 | LEAK-38 |
| `TVA_CHAFF6`, `CHAFF7`, `CHAF10`, `CHAF12`, `CHAF15`, `CHAF18`, `CHAF22`, `CHAF29` | turnover by VAT rate | yes (filed return) | float; 8.0% block-missing; about 90 cells between 0 and 10 are unusual, not impossible | fine | CLEAN-11 |
| `TVA_TOTDUE`, `TVA_MNTPAY` | VAT due / paid | yes | float | fine | |
| `TVA_MOIDEB`, `TVA_MOIFIN` | first / last month filed | yes | numeric, 1-12 | fine (a cycle stays a number) | CLEAN-14 |
| `TVA_CRDINI` | opening VAT credit | yes | float | fine | |
| `TVA_CRDFIN` | **closing** VAT credit (dictionary wrongly repeats "Crédit Initial") | yes | float | fine; write the meaning into the notes: `CRDINI(y) = CRDFIN(y-1)` in 89.9% of 6,180 consecutive pairs | CLEAN-1 |
| `TVA_BAS*`/`TVA_DED*` (IMB, EQL, EQI, AUL, AUI, RSM), `TVA_RSNRES`, `TVA_TRSPOR` | purchase bases and deducted VAT | yes | float | fine | |
| `TVA_ACHSUS`, `ACHEXO`, `CAFEXP`, `CAFSUS`, `CAFEXO`, `AACHAB`, `MACHN`, `MCESQ`, `MTVLSM`, `TXVLSM`, `MTALSM`, `TXALSM` | suspended/exempt purchases, export turnover, self-supply | yes | float; MTVLSM/MTALSM equal in 98.4% of rows but not exact copies | fine | CLEAN-5 |
| `TVA_DEDREG`, `CRDBLQ`, `CRDRES`, `CRDRMP`, `CRDRMC` | regularisation deduction, refund-claimed credits | filed in the return | float | fine (LEAK-38 note) | LEAK-38 |
| `TVA_RESTIT`, `TVA_MTORDTVA`, `TVA_MTDJRTVA` | VAT refunded, refund order, already refunded | **unknown: administrative acts after filing** | float | potential leak, keep with a fuller note (problem 3) | LEAK-38 / LEAK-10 |
| `ADB_MNTORD` | government payments to the taxpayer | yes (cross-check) | float, 74.4% missing (minimum 25,523, so missing means no record) | fine | CLEAN-2 |
| `SND_*_I` (PRD, TVA, DRC, TAX, PAY), `SND_*_E` (PRD, TAX), `SND_*_A` (PRD, TVA, DRC, TAX, PAY) | customs import / export / other regimes | yes | float, 82-94% block-missing | fine | |
| `SND_MNTAIR_I`, `SND_MNTAIR_A` | unknown (undefined in the dictionary) | unknown | float | fine, meaning unknown and noted | |
| `AX1_BRTIMP`, `AX2_HONORA`, `AX2_LOYERS`, `AX3_REVCAP`, `AX5_MNTMAR` | third-party salary, fees, rent, capital income, public contracts | yes (filed after year end, before audit) | float, 23.9% block-missing | fine | |
| `FAC_*_F`, `FAC_*_C` (8) | suspended-tax invoices as supplier / client | yes | float, 90-91% missing; missing indicator R2 at most 0.016 | fine | LEAK-39 |
| `target` | log(1 + principal adjustment) | outcome | float, 0-23.59, 25.3% zero | fine | MET-3 |

Other checks: no constant or zero-only column remains after the 2018 cut, no exact column copies, and no other proxy codes found.

**Problems, ranked (P4 first)**

1. **P4, LEAK-10 (Must, weak strength): `CTR_CESSAT` is a future status.**
   - All 24 registry fields are constant within each taxpayer, so they are an extraction-time lookup.
   - Cessation is a status that changes over time. The ceased share falls from 5.5% (2013) to 2.7% (2017), the pattern of a snapshot: a firm that ceased later carries "ceased" on all its earlier years. This is the King County mechanism ("attributes looked up after the outcome").
   - Ceased rows have mean target 10.06 against 11.88, and zero share 0.32 against 0.25.
   - The model uses it: dropping it moves LightGBM RMSE from 5.995 to 6.009 (+0.015, mean of 3 windows × 2 seeds).
   - Mildest remedy: drop `CTR_CESSAT`. Alternative: keep it with an explicit LEAK-38 note naming it as an extraction-time status. If kept, decode 0/1 into the codebook's words (CLEAN-12).
   - The obligation codes are the same kind of snapshot but change slowly. They stay under the existing note.

2. **P4, question for the curator (LEAK-34 against SPLIT-9/LEAK-12): the dropped taxpayer id can be rebuilt exactly from kept columns.**
   - The 24 registry columns give 12,244 distinct fingerprints for 12,244 taxpayers, one to one. So the CLEAN-3 reason for dropping `CTR_MATFIS` does not hold in effect.
   - The test taxpayer appears in training for 63.6%, 71.3% and 74.6% of test rows (2015, 2016, 2017).
   - Labels persist within a taxpayer: Spearman 0.64-0.67 between consecutive years, zero/nonzero agreement 0.86-0.89.
   - An explicit previous-year label feature cuts RMSE from 5.995 to 5.466 (-8.8%). Trees do not exploit the fingerprint today: RMSE is 6.09 on seen taxpayers against 5.75 on new ones.
   - LEAK-34 allows a taxpayer's own history. But 84.9% of taxpayers have contiguous runs of years, which fits one audit covering several years. If so, the 2016 training label is adjudicated together with the 2017 test label, and under SPLIT-9 that is a training label that tells a test outcome.
   - Mildest remedy: state in the notes that the registry fields act as a taxpayer key and that same-audit timing is unknown. Ask the curator whether the retrospective framing ("training labels already held") accepts that.

3. **P4, LEAK-38 (Should): the paid-refund fields stay, with the fill test added to the note.**
   - The record tested only missingness, not whether the fields are filled.
   - Fill test, predicting `TVA_RESTIT > 0` from the filing-time covariates (5-fold, grouped by taxpayer): observed/predicted is 1.27 among zero-adjustment rows (14.6% vs 11.5%) and 1.01 among positive rows. For `TVA_MTDJRTVA` it is 2.84 vs 2.87, so no differential.
   - The raw contrast among credit-holders (zero share 0.70 when refunded, 0.33 otherwise) is mostly the credit position.
   - Dropping all three fields costs +0.022 RMSE.
   - This is a modest step, far below kick's (about 20×), so keeping them is consistent with sendy (named field kept under LEAK-38, 2026-11-04). The note should carry these numbers and the revisit trigger.
   - Also note: in the 10.1% of pairs where the opening credit does not match last year's closing credit, the zero share is 0.339 against 0.261. These may be revised returns.

4. **Procedure, writing.md: stale prose after the 2018 cut.**
   - `curation_comments` still says "All 103 retained predictors" (now 100 inputs including `fiscal_year`), "our four annual holdouts" and "shrinking latest cohort (365 rows)".
   - The accepted warning `task_time_on_few_unique` still says "six ... cohorts; four outer windows". It should say five and three.

5. **P7, CLEAN-1/CLEAN-12 (Should):**
   - State that `TVA_CRDFIN` is the closing credit, using the carry-over evidence above.
   - Decode `CTR_CESSAT` 0/1 into words if it is kept.
   - `FJU_CODFJU` 99 (48.8% of rows) and `CTR_RATISS` 0/2 stay as undocumented codes, with a note.

6. **Not a column problem:** `leak_probes.py --raw` fails at `dataset.py` line 108 (`assert df.shape == (21295, 121)`), because lineage tracing adds a tag column. Asserting on the raw columns without the tag would let the probe run; nothing was changed.

```text
Verdict: ship after changes (problems 1, 4), with curator calls on 2 and 3.
Validity: LEAK-24 holds for 2017 (labels in band; count fall is selection); LEAK-10 triggered weakly (CTR_CESSAT, drop or note);
  LEAK-34 vs SPLIT-9 open (registry fingerprint = taxpayer key, lag label -8.8% RMSE); LEAK-38 keep, note to gain fill test.
Quality: CLEAN-12 gap (CTR_CESSAT words); CLEAN-1 (TVA_CRDFIN meaning); writing.md stale counts.
```

</details>

<details><summary>Split audit</summary>

**Verdict: right with notes.** A temporal split by fiscal cohort (train on every earlier year, test on 2017, 2016 and 2015) is defensible, and the declared windows meet SPLIT-14. One P4 question is unsettled: the same taxpayer's other years sit in training. There are also two consistency defects in the prose.

**Answer to focus.md: is 2017 partly censored like 2018?** No. 2017 has fewer rows, but nothing shows its rows were selected by outcome.
- **Rows per year:** 6,079 / 5,754 / 4,368 / 3,100 / 1,629 / 365 for 2013 to 2018. That is a steady fall of 5%, 24%, 29%, 47% and 78% a year. It fits fewer audits having reached the newest years by the extract. It is not a break at 2017 alone.
- **Outcome measures for 2017, all inside the band of 2013-2016:**

| Measure | 2017 | 2013-2016 |
|---|---|---|
| Share of zero labels | 0.249 | 0.236 to 0.265 |
| Median of nonzero labels | 15.72 | 15.80 (Mann-Whitney p=0.36) |
| 90th percentile of nonzero labels | 18.35 | 18.09 to 18.34 |
| Mean residual, leave-one-year-out LightGBM | +0.132 | +0.143 to +0.222 for 2014-2016 (2013 is −0.405) |

- **By taxpayer category:** M is 16.70 vs 16.66 (p=0.68) and P is 14.60 vs 14.65 (p=0.14). C moves −0.23 (p=0.005). C moved +0.23 in 2014 (p=0.003), so this looks like year-to-year noise or drift, not censoring.
- **Against 2018:** 2018 was −1.2 log units in every category.
- **Conclusion:** under the amended SPLIT-10 (no selection by outcome measured at the release end), 2017 needs no cut and no gap. One caveat is not measurable: the thinner cohort holds the taxpayers audited sooner. The notes should say this in one line.

**Problems, ranked**

**1. P4 (SPLIT-9 / SPLIT-13 / USE-10): the test taxpayer's other years are in training, and the model profits from them. Concern; cannot be verified without audit dates.**
- **Shape of the data:**
  - 12,387 taxpayers. 6,397 have one year; the others have 2 years (3,669), 3 (1,793), 4 (463), 5 (61) or 6 (4).
  - 69% of the multi-year runs are contiguous. The commonest patterns are (2013, 2014) with 1,328 taxpayers, (2014, 2015) with 632 and (2013, 2014, 2015) with 607.
  - This is how multi-year audit periods would look in the data.
- **Labels move together within a taxpayer:**
  - Adjacent-year label correlation is 0.651. Agreement on zero vs nonzero is 0.861, against 0.622 if the years were independent.
  - 15-20% of multi-year taxpayers have all labels zero, against 0.1-6.4% under independence.
  - The agreement decays with the year gap (0.861, 0.799, 0.744, 0.677). That fits one audit setting several years together, and it equally fits a stable taxpayer behaviour. The evidence is circumstantial (EV-6).
- **Share of test rows whose taxpayer is in training:** 74.6% for 2017, 71.3% for 2016 and 63.6% for 2015. 48.7%, 47.4% and 48.7% have the year just before in training.
- **What the model gains from them (LightGBM, RMSE per window 2017 / 2016 / 2015):**

| Setup | 2017 | 2016 | 2015 |
|---|---|---|---|
| Declared split | 5.986 | 5.970 | 6.033 |
| Training rows of the test taxpayers dropped | 6.149 | 6.126 | 6.275 |
| Same number of random training rows dropped (size control) | 5.980 | 6.009 | 6.087 |

  - The extra loss beyond the size control is +0.17, +0.12 and +0.19, almost all of it on rows of already-seen taxpayers (6.11 → 6.33).
  - The taxpayer id is dropped, so the model re-identifies taxpayers through the 23 registry fields, which do not vary within a taxpayer, plus the financial profile.
  - Skill falls from 0.150 to 0.124.
- **Adding the taxpayer's previous label as an explicit feature:** mean RMSE goes from 5.996 to 5.462, and skill from 0.150 to 0.226.
- **The definition sits between two regimes.**
  - Its split is the known-entity one: temporal, with recurring taxpayers "both occur".
  - It withholds the previous outcome ("no taxpayer/label aggregates") and the id.
  - So the benchmark rewards re-identifying taxpayers implicitly.
  - Under USE-10, a known entity's history is legitimate only if its earlier labels were known before the test year's label. If one audit set both, they were not, and SPLIT-9 applies, as in the alfa_battle_2_0_task_2 precedent (training rows of the test window's entities dropped).
  - The ieee_fraud_detection precedent read carried labels as known history; that is the case for keeping the current split.
- **Question for the curator (mildest remedies first):**
  - (a) Keep it, and state in `splits_comment` the shares of test taxpayers seen in training (64-75%) and the +0.12 to +0.19 RMSE lift as a measured optimism.
  - (b) Drop each window's test taxpayers from its training side. This needs `CTR_MATFIS` kept as a non-feature column. Training would keep 17,070, 12,557 and 8,137 rows, which is 81.6%, 60.0% and 38.9% of the data. The 2015 window then falls below the SPLIT-14 floor; the tension table says a measured shortcut is removed whatever it costs the floor.
  - (c) If the curator holds that previous labels are history, make the previous label an explicit feature under USE-10.

**2. P4 / P3 (SPLIT-1, SPLIT-10, SPLIT-19): the regime and its justification contradict each other.**
- **What the definition says:**
  - `task_summary.use_case` and `splits_comment` say the task is retrospective, with labels held and "no refit at each fiscal-year start".
  - Myunghwan's CC justifies temporal as "closer to scanning a new year", and his earlier CC calls it an "annual pre-inspection audit-prioritization task".
  - The participant kit's prediction point says "the scored adjustments of earlier fiscal years are available for training". That is a refit framing.
- **Under the refit reading:** labels arrive years after the fiscal year (2018 was cut because its inspections were open). A gap of 2-4 years would be due under SPLIT-10, and five cohorts cannot carry it under SPLIT-14.
- **Under the retrospective reading:** the splits.md "Alice" pattern points to IID, or to grouping by taxpayer for never-audited taxpayers.
- **Measured, over 3 folds on 2013-2017:**

| Split | RMSE | Skill |
|---|---|---|
| IID random | 5.928 | 0.164 |
| Grouped by taxpayer | 6.048 | 0.147 |
| Declared temporal | 5.996 | 0.150 |

  The gaps are small, and SPLIT-4 says the size of a gap never decides.
- **The source's split:** the contest test covers 2013-2018, so the source did not split by time. The departure from SPLIT-19 is recorded only as "a separate cross-cohort evaluation", with a stale "four".
- **Remedy:** wording only. Pick one framing in all three places. Under the retrospective framing (the one that stands), name the departure from SPLIT-19 and say the windows test cohort transfer with no refit gap, citing the lt_vehicle_loan_default_prediction precedent (retrospective, zero gap). Drop "scanning a new year" and fix the kit's prediction point.

**3. Procedure (writing.md): split figures are stale after the 2018 cut.**
- The `task_time_on_few_unique` reason still says "six genuine fiscal-year cohorts; four outer windows". It should be five cohorts and three windows.
- The `curation_comments` still say "our four annual holdouts", "All 103 retained predictors" and "shrinking latest cohort (365 rows)". The 365 rows were 2018; the latest shipped cohort is now 2017 with 1,629 rows.
- **Remedy:** reword those lines.

**4. P4 (SPLIT-20), note only: the training history.**
- 2013 is the one year out of band in the leave-one-year-out check (mean residual −0.405).
- 45% of its taxpayers have no other year, against 19-27% later. That fits left-truncated audit periods.
- 2013 is only ever on the training side and there is no break to cut. Keep it, with one line in the notes.

**Checks that pass:**
- **Windows:** 3 windows. Training sides are 92.2%, 77.4% and 56.5% of the 20,930 rows, against the 50% floor of SPLIT-14. Test windows hold 1,629, 3,100 and 4,368 rows (SPLIT-17).
- **Time column:** a fiscal cohort set to January 1. It is not an event date, and the notes say so.
- **Seasons:** annual windows have none.
- **Copies:** no full-row copy including the fiscal year crosses a cutoff; the prep probe found 0.0%.

Judgment record:
```text
Verdict: right with notes.
Validity: SPLIT-14, SPLIT-17 hold; SPLIT-10 (2017 censoring) holds, no gap needed (measured); SPLIT-9/SPLIT-13/USE-10 concern:
  64-75% of test taxpayers seen in train, lift +0.12-0.19 RMSE beyond size, same-audit labels unverifiable (curator call);
  SPLIT-1/SPLIT-19 framing inconsistent (fix wording).
Quality/procedure: stale window/cohort/predictor counts in the accepted warning and comments.
For the curator: issue 1, a weighing call (keep with the numbers / drop test taxpayers' training rows / previous label as a feature).
```

</details>

<details><summary>Domain practitioner</summary>

**Domain practitioner: `tunisian_fraud_detection_challenge`** (I'm writing as a DGI audit-programme planner who picks taxpayers for VAT verification)

**Fit: approximate.** The fit is right. The reason given for it is not. The real gap is that every row is an already-audited taxpayer-year, while my decision is made over all filers (a selection bias the real setting does not share, USE-8), and the label is an assessed log amount rather than the money recovered.

**Answer to focus.md (is 2017 censored like 2018?)**
No, not in its labels. The fall in row count is how the audit pipeline works, and the 2017 labels are mature. These are raw Train.csv numbers by fiscal year:

| year | n | zero share | nonzero p10 | nonzero p50 | nonzero p90 |
|---|---|---|---|---|---|
| 2013 | 6,079 | 0.265 | 13.40 | 15.70 | 18.09 |
| 2014 | 5,754 | 0.249 | 13.53 | 15.83 | 18.30 |
| 2015 | 4,368 | 0.258 | 13.50 | 15.85 | 18.31 |
| 2016 | 3,100 | 0.236 | 13.21 | 15.87 | 18.34 |
| **2017** | **1,629** | **0.249** | **13.11** | **15.72** | **18.35** |
| 2018 (cut) | 365 | 0.277 | 10.95 | 14.63 | 18.00 |

- Tunisian audits may reach back 4 years on declared taxes, 10 if nothing was filed. An in-depth verification covers several years of one taxpayer at once. A dossier exists only once its audit is notified. So fiscal year N keeps adding rows until about N+4, and the count falls steadily from 2013 to 2018, not just at the end.
- 2017 is a partial sample of dossiers that have been audited, but its zero share and nonzero quantiles sit inside the 2013–2016 band. 2018 is the outlier, with its nonzero median 1.2 log units lower. LEAK-24's cut at 2018 is the right one, and no further cut is needed.
- One caveat goes in the notes, not the data: the 2017 test fold contains the audits that closed fastest. That may tilt it towards the latest year of multi-year audits started in 2018–2019.

**The five questions, as the planner**

**1. Inputs at the prediction point.**
- Inputs I would have: the filed VAT returns, the customs aggregates and the third-party withholding cross-checks. The last arrive with the employer annual declaration in N+1, so they are there before I select.
- Refund fields are legitimate: in Tunisia a VAT-credit refund request itself triggers a verification.
- Inputs I might not have: the registry fields are a current snapshot. All 23 are the same across years for the 5,990 repeated taxpayers, so CTR_CESSAT (cessation) may record a status reached after the audit. The regularisation amounts may also be post-audit. Both are kept under LEAK-38, which is correctly disclosed.
- Inputs I would always have but that are missing:
  - each taxpayer's audit history (past adjustments, date of last audit). The taxpayer ID is dropped, so the known-entity history USE-10 allows is not available.
  - filing timeliness and late penalties
  - the income-tax / corporate-tax return figures
  - office capacity

**2. Target.** It is a proxy. I act on expected recovered money per audit, net of what is lost in disputes. The source gives log(1+assessed principal adjustment), with penalties excluded. What I want is two numbers: P(adjustment > 0) and the expected amount in dinars, ranked by their product.

**3. Unit and test.**
- One row is a taxpayer-year. My unit is the taxpayer, because one audit covers several years.
- I measured how tied the years of one taxpayer are. Among 2017 test rows, 75% have an earlier labelled year of the same taxpayer. The labels correlate at 0.64 and agree on zero vs nonzero for 86% of rows (2016: 0.57 / 0.83; 2015: 0.62 / 0.84).
- I see no sign that a model exploits this. With the ID dropped, an HGB model's RMSE is worse on recurring taxpayers than on new ones: 6.06 vs 5.55 in 2017, 6.11 vs 5.76 in 2016, 6.20 vs 5.84 in 2015.
- Testing on the next fiscal cohort does mirror "scan a new year". But the test rows are audited dossiers, not all filers.

**4. Would I use it?** As a screen for whether an audit will find anything: yes. The nonzero AUC is 0.82–0.84 from the RMSE model and 0.84–0.85 from a classifier. To rank by money: no. Within the nonzero rows, the log-RMSE model's predictions barely track the size of the adjustment (Spearman 0.08, 0.14 and −0.00 for 2017, 2016, 2015). I would trust it more with the taxpayer's audit history, as-of registry values, and a check on a random or unaudited sample (the selective-labels problem).

**5. Metric.** See the metric verdict at the end.

**Gaps between the dataset and the real decision, ranked by how much they change the task**
1. **Selection: only audited dossiers** (USE-8). The real decision ranks all filers, and the model never sees an unaudited return. This alone keeps the fit approximate. `fit_reason` mentions "inspection selection" but should name it as a `Selection Bias` marker plus a sentence.
2. **The metric rewards hit rate, not yield** (MET-1). See below.
3. **Unit mismatch.** An audit covers several taxpayer-years. The splits put one audit's earlier years in training and its later years in test. That is harmless here because the ID is dropped (numbers above), but it still has to be stated.
4. **Inputs I would always have are missing** (audit history, filing behaviour, income-tax returns), and the registry is a current snapshot (LEAK-38, kept).
5. **Assessed vs collected amount, and an unknown currency unit** (USE-5): an approximate-label gap, already named.
6. **The 2017 test cohort is a partial, fast-closing sample** of its fiscal year. Its labels are in band (table above), so this is a caveat for the notes only.

**What an expert in the domain would change**
- **Rewrite the use case** (USE-1, USE-9 weighed factor). "An analyst looks back over archived dossiers with the scored adjustment withheld" describes nobody: an archived audited dossier already has its adjustment. It reads like a use case rephrased to excuse the timing gap. The real actor is the DGI audit planner who, after year-N returns and cross-checks are in, ranks taxpayers for the next verification programme. The fit stays approximate, with the selection and the unknown as-of timing named as the gaps. The data, splits and target need no change.
- Add the `Selection Bias` marker.
- Say in the notes that one verification spans several fiscal years, and record the label correlation of 0.57–0.64 between a taxpayer's years.
- **Fix the stale prose** after the 2018 cut:
  - the curation comments still say "103 predictors" (99 are probed now), "four annual holdouts" and "shrinking latest cohort (365 rows)"
  - the accepted warning `task_time_on_few_unique` still says "six … cohorts … four outer windows"; it is now five cohorts and three windows

**Metric verdict: **partly****
- **Declared:** `rmse` on the log1p label, identity transform, from the source. This follows MET-4 (Zindi's leaderboard metric). Scoring on the log scale is exact for what Zindi scored (MET-3, last sentence). An RMSE in money would be dominated by a few amounts up to e^23.6 ≈ 1.8e10.
- **What it actually scores** (HGB, test years 2017 / 2016 / 2015):
  - RMSE 5.94 / 6.02 / 6.07, against a dummy at 7.04 / 6.98 / 7.16.
  - 59% / 60% / 56% of the squared error comes from the true zeros, which are 25% of rows. Each one is a 15-log-unit miss. So RMSE mostly scores whether an audit finds anything at all.
- **It picks a different model than I would** (MET-1):

  | model | money captured in its top 10% (share of the oracle's) | hit rate in that top 10% |
  |---|---|---|
  | best by log-RMSE | 0.43 / 0.35 / 0.31 | 0.93–0.98 |
  | two-part P(nonzero)×E[amount] | 0.69 / 0.59 / 0.58 | 0.73–0.79 |

  The pattern is the same at the top 20%. In tax administration both hit rate and yield are standard measures, but programme value is judged by yield.
- **What I would choose:** a money-weighted ranking metric with no threshold, such as the normalized Gini of predictions against expm1(target), or the area under the money-capture curve. It scores ranking by expected yield without fixing an audit capacity k, which MET-7 forbids inventing; the source gives none. It also sidesteps the hard-decision problem MET-6 warns about.
- **Keep RMSE for now?** Yes, defensibly, under MET-4. The evidence above is measured on the shipped splits, so it meets MET-4's bar for an overrule if the curator wants one. But RMSE is not wrong for a hit-rate goal, so this is a curator call (MET-10), not a defect. At minimum the notes should say that RMSE on log1p mostly scores whether an audit finds anything, not the amount recovered.

Rules cited: USE-1, USE-5, USE-8, USE-9, USE-10, LEAK-24, LEAK-38, MET-1, MET-3, MET-4, MET-6, MET-7, MET-10.

Sources:
- [Zindi, Tunisian Fraud Detection Challenge](https://zindi.world/competitions/tunisian-fraud-detection): actor is the local tax authorities; the metric is RMSE.
- [Ministère des Finances FAQ](https://www.finances.gov.tn/fr/faq?page=3): 4-year limit for declared taxes, 10 years without a declaration; notification interrupts the limit.
- [memoireonline: prerogatives of the tax administration during an audit](https://www.memoireonline.com/08/08/1457/m_prerogatives-administration-fiscale-lors-du-controle19.html): CDPF preliminary vs in-depth verification.
- [BDO Tunisie on the timing of a targeted verification](https://tn-www.bdo.global/getattachment/Publications/AXE-TEMPS-DE-LA-VERIFICATION-PONCTUELLE/BDO-Tunisie-Comprendre-le-deroulement-de-la-verification-ponctuelle-06-2023.pdf.aspx?lang=en-GB)
- [Battaglini et al., NBER w30777](https://www.nber.org/system/files/working_papers/w30777/w30777.pdf): audit selection judged by recovered evasion; selective labels.
- [Springer s10260-022-00643-4](https://springerlink.bibliotecabuap.elogim.com/article/10.1007/s10260-022-00643-4): selection bias of models trained on audited cases only.

</details>

<details><summary>Blind review</summary>

**Verdict:** include with changes. This is real Tunisian tax-audit data with a moderate signal that a model can learn, no sign of leakage, and a temporal split that fits how it would be used. Before it goes in, the target needs documenting, the three code columns need retyping as categorical, and the licence needs checking.

**What the task is.** The Zindi Data tab says: "The 'TARGET' column is the variable to predict. It equals the amount of the tax liability that the taxpayer has to adjust." The rows are "a subset of over 25,000 samples aggregated by year". Each row is one taxpayer and fiscal year (2013–2017), with anonymised filings: VAT returns (`TVA_*`), withholding (`SND_*`), invoices (`FAC_*`), filing obligations (`CTR_*`), and activity, tax office and legal-form codes. The Ministry of Finance would use this to rank filed returns for audit by how much tax they are likely to recover. That is a real and common use. The source scores it by RMSE.

**Concerns, most serious first**

1. **The target is transformed, and nothing says so.**
   - Evidence: `expm1(target)` gives whole numbers in 100% of rows, and 0.693147 = log1p(1). So the target is log1p of the adjustment amount, probably in millimes (raw maximum 1.76e10, median 3.27e6).
   - 25.3% of rows are exactly 0. The rest are continuous, with clumps at fixed amounts: log1p(180,000) appears 13 times, which looks like flat fines.
   - The original competition pages never mention a log transform. Their sample submissions (0.957, 0.612) do not match this scale.
   - Change: state in `task.md` that the target is log1p(adjustment amount), zero-inflated, and that RMSE on the log scale is the metric. Otherwise someone may score on the raw scale or re-transform it.

2. **Who is in the sample, and when the label is known.**
   - The data comes from audits, so it most likely holds only taxpayers who were audited. The source does not say how they were chosen.
   - A model trained here estimates the adjustment given that an audit happens. It does not score the whole taxpayer population. That is fine as a benchmark task, but the description should say so.
   - Audits usually finish years after the fiscal year. So when scoring fiscal year 2017, the 2015–2016 labels may not yet have existed.
   - The split by `fiscal_year` is still the most honest option available. Expect it to look somewhat more optimistic than real deployment.

3. **The same firms appear in train and test.**
   - There is no taxpayer ID. But 80.6% of rows share a static signature (all `CTR_*` flags plus activity, tax office and legal-form codes) with a row from another year. The panel repeats firms.
   - 173 nonzero target values appear in more than one row, mostly across years. In 73 of these groups the activity and tax office also match, which suggests one audit total recorded for several years of the same firm. Example: target 16.910033 in both 2013 and 2014 with identical features.
   - This affects about 2% of nonzero rows. It is realistic, since the tax office knows its past audits, so I would not regroup the split. I would state it.

4. **Column types.**
   - `ACT_CODACT` (525 levels), `BCT_CODBUR` (158 levels, tax office) and `FJU_CODFJU` (16 levels, legal form) are nominal codes stored as int64. Declare them categorical.
   - The `CTR_*` columns are coded 1/2/3 obligation flags. Numeric is acceptable, but they are a mix of float and int; make them consistent.
   - `CTR_CATEGO_X` has a level "N" with only 8 rows. That is harmless.
   - The block-wise missing values carry meaning: TVA 8%, SND 83–94%, FAC 90–91%, ADB 74%. They mean "did not file this form". Rows where the SND/FAC forms are missing have lower targets: mean 9.7 vs 12.1 for FAC_MNTPRI_C, and 41% zeros vs 24%. Keep them as NaN; do not impute.

5. **Duplicates.**
   - 7 rows are exact duplicates.
   - 26 rows duplicate another row's features. 45 rows share identical features with different targets; most are near-empty filings across years.
   - Drop the 7 exact duplicates. The rest is negligible.

6. **Signal and size.**
   - LightGBM with default-ish settings, trained on all earlier years:

     | Test year | Train rows | Test rows | RMSE (constant baseline) | R² |
     |---|---|---|---|---|
     | 2015 | 11,833 | 4,368 | 6.06 (7.16) | 0.28 |
     | 2016 | 16,201 | 3,100 | 5.98 (6.98) | 0.26 |
     | 2017 | 19,301 | 1,629 | 5.99 (7.04) | 0.28 |

   - Zero vs nonzero AUC is 0.84. R² on the nonzero rows alone is 0.37.
   - The top features make sense and none looks like leakage: final VAT credit `TVA_CRDFIN` (25% of gain; firms claiming credit have more zero targets, 36% vs 13%), `TVA_MNTPAY`, then activity and tax office.
   - The task is not trivial and has room for better methods. The 2017 window is small (1,629 rows) and will be noisy. The class shares are stable across years (24–26% zeros).

7. **Where the data comes from.**
   - The source says "over 25,000" training samples, but there are 20,930 rows here. Either the source was imprecise or rows were filtered; I cannot tell which.
   - Only the labelled Train.csv can be used, since Test.csv has no labels.
   - Columns such as `ADB_MNTORD` (ordered amount) and `TVA_MTORDTVA` / `TVA_MTDJRTVA` have names that could be post-assessment amounts. They do not rank among the top features, and I found no direct link to the target.
   - Change: check them against VariableDescription.csv, and drop any that are recorded after the audit.

**What I could not check**
- VariableDescription.csv: the meaning of each column, and especially whether ADB/ORD columns are set after the audit.
- How the 20,930 rows were derived from the source's ">25,000".
- How audited taxpayers were selected.
- The real timing of audit outcomes.
- The licence: Zindi data from a ministry is probably restricted to the competition, and this must be confirmed before redistribution.
- Taxpayer identity, since there is no ID, so the firm overlap above is inferred.

**Sources**
- https://zindi.world/competitions/tunisian-fraud-detection
- https://zindi.world/competitions/tunisian-fraud-detection/data
- https://zindi.world/competitions/supcom-tunisian-fraud-detection-challenge

</details>

<details><summary>Task gamer</summary>

The task can be gamed by about 0.24 to 0.56 RMSE, about 4 to 9% (baseline about 5.98). The gain comes from rebuilding taxpayers across years and using their earlier-year adjustments as a feature. Whether that counts as a leak depends on whether those adjustments came from the same multi-year audit. Nothing else I tried beat the noise.


**Honest baseline**: untuned LightGBM with 300 trees, `fiscal_year` turned into an integer year. Scores per split (test year 2017 / 2016 / 2015): **5.959 / 5.966 / 6.007**, mean 5.978. Predicting the training mean scores 7.04 / 6.98 / 7.16.

Noise check: I refit three times with a random column added. The scores ranged 5.949–5.964, 5.971–5.982 and 6.026–6.041, so treat about ±0.03 per split as noise.

**Exploits**

| # | Exploit | Honest score | Exploited score | Gain (per split, range) | A deployed model has it? | Fix |
|---|---|---|---|---|---|---|
| 1 | Rebuild taxpayers across years (static keys plus VAT credit carry-forward) and use their earlier-year targets from training | 5.959 / 5.966 / 6.007 | 5.398 / 5.640 / 5.760 | 0.56 / 0.33 / 0.25 (0.25–0.56) | Unsure. Yes if the year t−1 adjustment was settled before year t is scored; no if one audit covered several years at once (likely) | Split by taxpayer group within the temporal split, or ship the taxpayer id and state that history is allowed |
| 1a | Credit chain only: this year's opening VAT credit (`TVA_CRDINI`) equals last year's closing credit (`TVA_CRDFIN`) with the same office, category, legal form and activity code | same | 5.689 / 5.829 / 5.860 | 0.27 / 0.14 / 0.15 | same | same |
| 1b | Exact match on 24 static columns (office, category, legal form, activity, all `CTR_*` obligation flags), last year's target | same | 5.569 / 5.719 / 5.764 | 0.39 / 0.25 / 0.24 | same | same |

**How it works.** The kit has no taxpayer id, but taxpayers can be rebuilt. The carry-forward match links 3,221 rows to the year before. On those pairs the target correlation is 0.63, and zero vs non-zero agrees 82% of the time against 62% by chance. The 24-column key links 4,967 rows (correlation 0.63, 85% agreement). In each test year these features cover 22–24% of rows (chain), 60–64% (24-column key) and 81–88% (4-column key history).

**The gain comes from the labels, not from presence.** The same links with labels removed add nothing: "entity seen in earlier years" scores 5.948 / 5.964 / 6.028, and same-year counts per office or key score 5.976 / 5.947 / 6.018. About 25% of the error is the zero vs non-zero call, and earlier-year labels mostly sharpen that call.

**Is it a leak?** The task says earlier years' adjustments are "available for training". Tunisian in-depth audits usually cover several open years in one go. If so, the 2016 and 2017 adjustments of one taxpayer come from the same audit, and the 2016 result would not be known when 2017 is scored.

Two things point that way: the 85% zero/non-zero agreement, and row counts falling year by year (6,079 in 2013 down to 1,629 in 2017), which looks like years audited together. What would settle it: audit dates per row, or whether one audit spans several fiscal years.

**Mildest fix.** Rebuild the taxpayer id from the source and split by taxpayer group inside the temporal split. If history is meant to be allowed, ship the id so honest models get it too. Dropping `TVA_CRDINI`/`TVA_CRDFIN` alone does not fix it: case 1b gets nearly the whole gain without them.

**Flaws that hurt an honest model**

None found.
- Training only on the last 1 or 2 years scores 6.127 / 6.058 / 6.096 (last 1) and 5.992 / 5.963 / 6.007 (last 2), no better than using all years.
- No training row is dated at or after the test year.
- The share of zero targets is flat across years (24–26%), so I found no sign that a row's presence in training depends on its label.

**Attacks that found nothing (beyond the noise)**

- **Row order.** Within a year, the zero/non-zero label of the next row agrees no more than chance (0.62 vs 0.61; 2017: 0.655 vs 0.626). Correlation with row position is under 0.03.
- **Exact copies.** Only 45 rows are full duplicates including the year. 537 rows duplicate excluding the year; these are mostly all-empty returns of the same entity and are covered by exploit 1.
- **Number formats.**
  - All amounts are whole numbers, apparently in millimes.
  - Amounts ending in 000 (whole dinars) go with non-zero adjustments: zero-target share 0.11 vs 0.26 for `TVA_TOTDUE`, 0.12 vs 0.37 for `TVA_CRDFIN`.
  - A model on formats alone (missing, zero, last digit, ends in 000) scores 6.248 mean, against 7.04 for the mean prediction.
  - Added to the baseline, the digit features give 5.946 / 5.973 / 6.006, which is noise.
  - Probably real signal (rounded, estimated declarations), unless the audit rewrote the declared values; the source would decide that.
- **Missing-value blocks.** Returns with `SND_*` or `FAC_*` blocks present have more zero targets (0.43 and 0.50 vs about 0.22). The baseline already uses this, and it is known at filing.
- **Formulas.** The adjustment often equals a tax rate times a declared base. In millimes (the scale of `expm1(target)`) it equals:
  - `TVA_MNTPAY` on 519 rows;
  - `TVA_TOTDUE` on 195 rows;
  - 0.18 × `TVA_CHAF18` on 148 rows;
  - 0.1525 × `AX5_MNTMAR` on 206 rows and 0.1525 × `ADB_MNTORD` on 108 rows.

  These bases are declared at filing, so this is signal. Adding their logs changes nothing for trees (5.978 mean). A linear-leaf model crashed and I did not retry it.
- **Post-outcome columns.** No single column comes near the full model; the best alone is `TVA_CRDFIN` at 6.67 on the 2017 split. Apart from the formula matches above, no column copies the target.
- **Train vs test classifier.** AUC is 0.73 / 0.83 / 0.73, driven by `TVA_MCESQ`, `TVA_BASRSM` and `AX5_MNTMAR`. That looks like drift in the returns between years, and does not reveal the target.
- **Transforms over all rows.** No column has whole-table mean 0 / SD 1 or min 0 / max 1; the value ranges are raw amounts and codes.
- **Light tuning** (learning rate 0.02, 600 trees, column subsampling 0.5) is worse: 6.020 mean.

**Could not check**

- **Web sources.** Zindi's data page lists no column names and no taxpayer id, and the discussions have no leak threads or write-ups. One thread confirms the target is `log1p` of the amount, which matches the kit: every `expm1(target)` is an integer.
- **The published file.** It sits behind a Zindi login and its rules bar redistribution, so I could not look rows up in it (not attempted) or compare it with the kit (rounding, dropped ID, the 25k-to-20,930 row filter).
- **Whether audits span several years.** I could not confirm this, and it decides exploit 1.

Sources:
- [Zindi: Tunisian Fraud Detection](https://zindi.africa/competitions/tunisian-fraud-detection)
- [Zindi data page](https://zindi.world/competitions/tunisian-fraud-detection/data)
- [Zindi discussions](https://zindi.world/competitions/tunisian-fraud-detection/discussions)
- [SupCom variant](https://zindi.africa/competitions/supcom-tunisian-fraud-detection-challenge/data)

</details>

<details><summary>Precedent check</summary>

**Precedent check: tunisian_fraud_detection_challenge (second pass, 2026-11-04)**

**Answer to focus.md:** focus.md asks nothing beyond the standard panel. The soft spot that concerns precedent is whether 2017 is partly censored the way 2018 was. Under LEAK-24 and the earlier cases, keeping 2017 is consistent. I measured the raw Train.csv read-only:

| Year | Rows | Ratio to year before | Zero share | Nonzero median | Nonzero p90 |
|---|---|---|---|---|---|
| 2013 | 6,079 | – | 0.265 | 15.70 | 18.09 |
| 2014 | 5,754 | 0.95 | 0.249 | 15.83 | 18.30 |
| 2015 | 4,368 | 0.76 | 0.258 | 15.85 | 18.31 |
| 2016 | 3,100 | 0.71 | 0.236 | 15.87 | 18.34 |
| 2017 | 1,629 | 0.53 | 0.249 | 15.72 | 18.35 |
| 2018 (cut) | 365 | 0.22 | 0.277 | 14.63 | 18.00 |

- **2017's label statistics are in the range of the earlier years.** 2018 was cut because its labels fell (median 1.1 log units lower than the earlier years), not because of its row count.
- **The row count has fallen every year.** The probe-13 reading in leak_checks.md calls "a shift the history also shows" drift.
- **Closest cases:** alfa_battle_2_0_task_2 kept a measured end dip with a note (Lennart 2026-10-21). ames_housing and perth_house_prices kept a short last month after showing no price selection (Lennart 2026-10-26).
- **The 2017 drop is speeding up (0.53 against 0.71–0.76).** The definition's notes say "2017 is in band (p = 0.8)" but leave out the row-count z of −4.6. The amended SPLIT-10 asks that "the notes give the measurements". That is a gap in the write-up, not a different decision.

---

**Decision 1: no gap between train and test under the retrospective framing.** Lennart kept the framing on 2026-11-04 ("okay let us keep it"); the "no SPLIT-10 departure" reading dates from the AI assessment of 2026-10-31. **This departs from precedent without a stated reason.**

- **Closest case (same curator, same day, same PR):** lt_vehicle_loan_default_prediction (curation/records/lt_vehicle_loan_default_prediction.md, lines 56–74).
  - Myunghwan had given it the same retrospective zero-gap reasoning, recorded as an "Exception to SPLIT-10 (2026-10-23)" that serves P3.
  - On 2026-11-04 Lennart asked to "check it and add gap if needed". He moved the use case to the source's decision at disbursement, had the gap measured (+0.0018 ROC AUC at equal training size; recent default rates per code add +0.0026), and amended SPLIT-10 so that zero gap must rest on measurements.
- **Tunisian follows the reasoning that was replaced.**
  - The same curator recorded a retrospective zero gap as an exception on L&T but as "no departure" here. That is uneven recording of one rule.
  - Here the retrospective framing stays, and no shortcut measurement (do recent training labels help?) was made.
- **The amended rule's trigger is met here.**
  - The amended SPLIT-10 sets a gap "where the source or the context documents late labels, or where a measurement shows ... a selection by the outcome at the release end". The 2018 cut is itself that measurement ("inspections still open at the 2019 extract").
  - The LEAK-24 case sf_permit_time paired its cut with a 6-month SPLIT-10 gap, "since a 1-month gap still censored the slow permits".
- **The steelman holds up partly.** Under a retrospective analyst framing, training and test labels come from the same 2019 snapshot, so no refit is claimed and the training labels are no more mature than the test labels. But the amended rule has no retrospective carve-out, and L&T was not decided on that ground.
- **What a gap would cost.** A one-year gap gives train shares of 77.4% for the 2017 window, 56.5% for 2016 and 29.0% for 2015. Only two windows would meet SPLIT-14 (a Must: at least 3 windows, each training on at least 50%).
  - Departing from SPLIT-10 to keep SPLIT-14 would be the third exception for that reason, after alfa_battle_2_0_task_2 and lending_club (2026-10-21). An amendment would then be due. The register already flags SPLIT-10 as amendment_due, with exceptions on 6 datasets.
- **Not reasonable under the ranking?** No. Higher-ranked rules are not broken: SPLIT-9's measurable shortcut has not been shown, and SPLIT-10 is a Should.

```text
**Consistency check (AI, 2026-11-04):** your call on tunisian_fraud_detection_challenge (no gap, retrospective
framing kept) differs from lt_vehicle_loan_default_prediction (2026-11-04, same reasoning replaced: the use case moved
to the decision at disbursement, the zero gap measured, SPLIT-10 amended to need measurements). Here the 2018 cut
documents late labels, and no shortcut test was run. What sets this case apart?
(a) the source names no operational moment (no filing, audit or extract dates), so only a retrospective cohort comparison
can be framed; the zero gap is an application of amended SPLIT-10 once a recent-label shortcut test (like L&T's
equal-size comparison) shows nothing, with the 2017 measurements in the notes;
(b) treat it like L&T: measure a one-year gap (it leaves 2 windows, so it needs an exception for SPLIT-14, the third
of that reason: amendment due);
(c) reopen L&T to allow the retrospective framing;
(d) amend SPLIT-10 to state that a retrospective, same-snapshot evaluation needs no gap.
```

---

**Decision 2: refund, regularisation and registry fields kept under LEAK-38 after dropping the `Anonymized` tag.** The fields were kept by Myunghwan on 2026-10-31; Lennart dropped the tag on 2026-11-04. **This departs from the rule's text; its reason is implied by practice but not written down.**

- **Dropping the tag on its own is consistent.** selection.md, under "No marker when", lists "only ids were replaced while the features keep their meaning".
- **The tension is with LEAK-38.** Its scope is "Anonymised fields ... in data a company released for its own competition". The definition still says "Retain host-released anonymized inputs under LEAK-38", but the curator has now ruled the columns are named.
- **In practice the rule already covers named, untestable host fields:**
  - african_credit_scoring_challenge: `Amount_Funded_By_Lender`, a named field, "kept like kick's unverified host fields" (AI review panel, 2026-10-20). It has no tag.
  - sendy_logistics_challenge: `Distance (KM)` kept under LEAK-38 (Lennart 2026-11-04). It is a named column, although the dataset is tagged.
  - medical_facility_operational_data: `ExpectedDelayNextExam` kept under LEAK-38 (Lennart 2026-11-04). Also named and tagged.
  - With tunisian, that is the third or fourth time "fields whose timing cannot be tested" has been the real criterion. An amendment of LEAK-38's scope is due.
- **The conditional test matches the kick and expresso_churn_prediction precedent (2026-10-22).** All 12 process-field missing masks equal VAT-return availability, also within the zero and positive strata, so no mechanism was measured and LEAK-10 does not apply. That part is consistent.
- **Not reasonable under the ranking?** No. LEAK-38 narrows LEAK-10 (a Must) only where timing cannot be tested, and that condition holds.

```text
**Consistency check (AI, 2026-11-04):** the refund/registry fields stay under LEAK-38, whose text covers "anonymised"
fields, while your call of today drops the `Anonymized` tag because the columns are named. african_credit_scoring_challenge
(2026-10-20), sendy_logistics_challenge and medical_facility_operational_data (2026-11-04) also keep named host fields
under it. What sets this case apart?
(a) nothing: LEAK-38's criterion is untestable timing in host-released competition data, not anonymity; record the
retention as an application and reword "anonymized inputs" in the note;
(b) treat the fields as LEAK-10 suspects and drop them (TVA_MNTPAY alone: R2 0.314 -> 0.286);
(c) reopen african_credit_scoring_challenge to match;
(d) amend LEAK-38's scope to "fields whose timing cannot be tested" (due: third case).
```

---

**Decisions consistent with precedent (no prompt):**

- **2018 cut (LEAK-24, Must; Lennart 2026-11-04).**
  - It follows sf_permit_time (cut where follow-up is complete) and the probe-13 pattern ("cut before the first period out of band").
  - LEAK-24 says to compare two downloads first. Lennart's byte-identical re-download cannot settle labels from a static 2019 file, and no later archive exists (unlike consumer_complaints), so cutting was the remaining remedy.
  - Dropping the three 2018-form VAT columns follows CLEAN-5 (constant columns), as do the twelve zero-when-observed columns (constant when observed, missing mask copying another column) and the two exact copies.
- **`Anonymized` tag dropped:** consistent with selection.md, as above.
  - The only near pair is sendy_logistics_challenge, tagged the same day under the same Zindi "anonymized" wording.
  - Likely difference: Sendy's values (dates, distributions) were transformed, while here only CTR_MATFIS was replaced. Neither record states this; worth one line.
- **Metric (RMSE as the source declares, MET-4; Lennart 2026-11-04):** consistent with zillow_prize (mae kept as the competition's choice) and sendy_logistics_challenge (RMSE checked as declared, same day).
- **The label kept, set against xente_fraud_detection_challenge (`No`, USE-5, Lennart 2026-11-04).** Xente was set apart by a measured review step at 500k UGX: a zero there mixes "not fraud" with "not reviewed".
  - Here the zero share changes smoothly with size: by TVA_TOTDUE decile it runs 0.245, 0.26, 0.142, 0.117, 0.148, 0.2, 0.271, 0.316, 0.371, 0.455. No step is visible, and the zero share is flat over the years.
  - That is a distinguishing fact, so keeping is consistent, with "zero is not a completed negative inspection" disclosed.
- **Windows (SPLIT-14, SPLIT-15):** 3 windows. The 2015 window trains on 11,833 of 20,930 rows (56.5%); a 2014 window would train on 29%. Consistent.

---

**Write-up gaps tied to decisions (no rule departure):**

1. `accepted_check_warnings["task_time_on_few_unique"]` still says "six cohorts ... four outer windows"; it is now 5 cohorts and 3 windows. Myunghwan's 2026-10-31 acceptance rested on that wording. The warning is more true now, so the acceptance stands, but its premise should be updated.
2. Still stale: "103 retained predictors" and "our four annual holdouts" in the contest-input bullet, "shrinking latest cohort (365 rows)" in the duplicates bullet, and "anonymized" in the `row` field and the LEAK-38 note.
3. `changes` states "whose inspections were still open at the extract" as fact. The comment bullet says only "fits" that mechanism (an inference), which is the strength the evidence supports.

**Register flags:** none name this dataset. The relevant ones are SPLIT-10 amendment_due (decision 1) and the USE-5 drift on Xente, which is distinguished above.

</details>

<details><summary>Advocate</summary>

**Opening brief: ship `tunisian_fraud_detection_challenge` as defined, with notes and one column drop**

**1. Target, metric and the 2018 cut are faithful, and 2017 needs no further cut (P4 LEAK-24 Must, MET-3/MET-4, USE-5).**
- **Evidence:**
  - Discussion 448 says the target is log(1+x) of RES_MNTRED.
  - Discussion 436 says RMSE.
  - The metric is computable on every fold. A dummy scores 7.04 / 6.98 / 7.16 (MET-2).
- **2017 is not censored like 2018.** Four agents tested this separately and every result stayed in band:
  - Zero share is 0.249, against 0.236-0.265 for 2013-2016.
  - Nonzero median is 15.72 against 15.80 (Mann-Whitney p=0.36).
  - The p90 is 18.35 against 18.09-18.34.
  - The gradient-boosting mean residual is +0.18 for 2017 and -0.71 for 2018. The LightGBM leave-one-year-out residual for 2017 is +0.132, against +0.143 to +0.222.
  - Row counts fell every year (ratios 0.95, 0.76, 0.71, 0.53), so the drop is selection, not a 2017 break. Probe 13's z of -4.6 compares against a flat band and overstates it (EV-9).
- **Why this outranks the objection:** amended SPLIT-10 asks for a gap only where a measurement shows a recent-label shortcut or outcome selection at the release end. The release end is now 2017, and it shows neither.
- **Remaining gap:** the 2017 measurements, including the count z, are missing from the notes. Remedy: add a note, which is the mildest rung.

**2. The split meets the Must rules and the task is worth benchmarking (SPLIT-14 Must, SPLIT-17, P6).**
- There are 3 windows. Training sides hold 92.2%, 77.4% and 56.5% of the data, against the 50% floor. Test windows hold 1,629, 3,100 and 4,368 rows.
- **Signal:**
  - LightGBM scores 5.96-6.03 against a dummy at 7.04-7.16, with R² 0.26-0.28.
  - Zero vs nonzero AUC is 0.84.
  - The current task probe gives RF 5.970 against dummy 7.056, on 3 of 3 splits.
- **No copy leak:** 0.0% of test rows have a train copy once `fiscal_year` is included.
- **No flaw against honest models:** training on only the last 1 or 2 years is no better (task gamer). Row order, formats, transforms and the train-vs-test classifier found nothing beyond the ±0.03 noise.
- **Why no one-year gap:** it would leave 2 windows (the 2015 window trains on 29%). That breaks SPLIT-14, a Must, to satisfy SPLIT-10, a Should, so the Must wins on strength.

**3. A taxpayer's other-year labels in training are known-entity history (LEAK-34 and USE-10, both Must). The SPLIT-9 shortcut has not been shown.** This is the main objection, and I concede part of it.
- **Conceded:**
  - The model gains from history. Removing the test taxpayers' training rows costs +0.12 to +0.19 RMSE beyond a size control (split auditor).
  - The 23-24 registry fields work as a taxpayer key.
- **Disputed: the fact that would trigger SPLIT-9 ("the label was not yet known") is unproven.** No audit dates exist (EV-1, EV-6).
  - Label agreement decays with the year gap: 0.861, 0.799, 0.744, 0.677. The split auditor says this "equally fits a stable taxpayer behaviour".
  - alfa_battle_2_0_task_2's SPLIT-9 filter rested on a measured mechanism. There a later default followed a defaulted product at 95.1% against 2.3%, flat over lags of 1-10 months, and the flag was shown to be set after the later issue. Nothing like that is measured here.
  - The applicable precedent is ieee_fraud_detection (Lennart, 2026-10-26): carried labels were read as known history and kept.
- **The use case backs it (P3).** The practitioner says a DGI planner "would always have" each taxpayer's audit history.
- **Remedy, the mildest that fits:** keep the split, with a note that:
  - names the registry fields as an implicit taxpayer key;
  - gives the 64-75% share of test taxpayers seen in training;
  - gives the +0.12-0.19 lift beyond size and the label correlation of 0.62-0.65;
  - states that same-audit timing is unknown.
  
  This follows the SPLIT-10 amendment's "notes give the measurements" pattern.
- **This is a curator call, and I say so.** If Lennart rules that years are adjudicated by one audit, SPLIT-9 applies. The filter then leaves 2015 at 38.9%, so that window goes under SPLIT-8, or he takes option (c) and makes the previous label an explicit feature. Either way the dataset is fixed, not excluded.

**4. `CTR_CESSAT` is a weak LEAK-10 at most. Drop it and keep the dataset (LEAK-10, graded weak, so Should).**
- The snapshot reading is plausible: the ceased share falls from 5.5% to 2.7%, and the field is invariant within a taxpayer.
- Its effect is +0.015 RMSE, below the measured noise of ±0.03 per split.
- Remedy: drop the column, a one-line change to the definition. It costs nothing measurable and removes the question. Alternatively, name it in the LEAK-38 note.
- Name `CTR_RATISS` in that note too. It covers 233 rows with R² about 0.001.

**5. The refund and regularisation fields stay under LEAK-38 (Should). The new tests support this.**
- **Fill test:**
  - `TVA_MTDJRTVA` observed/predicted is 2.84 against 2.87, so no differential.
  - `TVA_RESTIT` is 1.27 among zero-adjustment rows, a modest ratio far below kick's (about 20x).
- Dropping all three fields costs +0.022, which is within noise.
- **Precedents:** african_credit_scoring_challenge (2026-10-20), and sendy_logistics_challenge and medical_facility_operational_data (Lennart, 2026-11-04), all keep named host fields under LEAK-38.
- Remedy (precedent checker's option a):
  - reword "anonymized inputs" in the note;
  - add the fill-test numbers;
  - record the retention as an application of LEAK-38.
  
  A LEAK-38 scope amendment is due as a rule matter. It does not block this dataset.

**6. The framing and metric are curator decisions, and newer than every AI reading (precedence: a curator CC outranks an AI assessment).**
- **Framing:** Lennart kept the retrospective framing on 2026-11-04 ("okay let us keep it").
  - On the L&T consistency question, option (a) now has its measurements: the equal-size control above, the 2017 residuals, and "last 1-2 years no better".
  - The practitioner's planner rewrite and the split auditor's SPLIT-1/SPLIT-19 inconsistency only need wording. Use one framing, drop "scanning a new year", and name the SPLIT-19 departure. Data, splits and target stay.
  - Add the `Selection Bias` marker (USE-8). Fit is already `approximate`.
- **Metric:** RMSE on log1p is the source's metric (MET-4).
  - The practitioner's yield argument is a MET-10 curator call. Their own verdict is "keep RMSE … defensibly".
  - Add a note that the score mostly measures whether an audit finds anything. 59% of squared error comes from true zeros.

**7. The remaining problems are wording and tooling (writing.md, PROV-13 procedure). None changes the data.**
- **Stale prose after the 2018 cut:**
  - "Six annual markers"
  - "No row is filtered"
  - "All 103 retained predictors … four annual holdouts"
  - "latest cohort (365 rows)"
  - the `task_time_on_few_unique` warning, which says six cohorts and four windows (README lines 64 and 236)
  
  Correct values: five cohorts, three windows, 100 inputs, a latest cohort of 1,629, and no row filtered besides 2018. The warning is more true now, so its acceptance stands.
- **Wrong file reference:** `SOURCE_MANIFEST.json` does not exist. Point the sentence at the stated SHA-256 values and `MIRROR_SOURCE.txt`. Both hashes match.
- **Tooling defect:** `assert df.shape == (21295, 121)` makes the `--raw` probe fail because lineage tracing adds a tag column.
- **Blind reviewer's points already handled:**
  - The codes are already typed categorical in `_feature_types`.
  - The log1p target is stated in `predicted`.
  - The licence restriction is declared, and the download goes through the user's own Zindi login.

**Net:** no Must is broken on measured facts. Five changes keep the dataset:
- the `CTR_CESSAT` drop;
- notes on taxpayer history, 2017, LEAK-38 and the metric;
- the `Selection Bias` marker;
- the prose fixes;
- the open SPLIT-9 timing question, which is a curator call.

</details>

<details><summary>Critic</summary>

**Opening brief (opponent): `tunisian_fraud_detection_challenge`. Ship only after changes**

Ranked by principle, then strength. Points 1 to 4 are validity. Points 5 to 7 are procedure and quality, and none of them is a reason to exclude.

**1. The use case has no real actor or moment (P3, USE-1 Must; USE-9 weighed factor).**
- **Problem.** `use_case` says an analyst "looks back over archived annual returns" with "the scored adjustment withheld". An archived audited dossier already holds its adjustment, so nobody stands at that prediction point. The domain practitioner says it reads like a use case reworded to excuse the timing gap. That is the factor USE-9 weighs against.
- **Three framings in one definition.**
  - `use_case` and `splits_comment`: retrospective, with no refit.
  - Myunghwan's CC: temporal is "closer to scanning a new year", and the task is an "annual pre-inspection audit-prioritization task".
  - Participant kit: "the scored adjustments of earlier fiscal years are available for training", which is a refit framing.
- **Effect.** Every P4 check (what is known, which training labels exist) is judged against a prediction point that is not real. Points 2 and 3 depend on this.
- **Evidence.** Domain-practitioner report; split auditor problem 2.
- **Remedy (fix the definition, wording only).** Make the actor the DGI audit planner who, after year-N returns and cross-checks are in, ranks taxpayers for the next verification programme. Keep the fit at approximate. Add the `Selection Bias` marker (selection.md; USE-8): every row is an audited dossier, while the real decision ranks all filers. Lennart kept the retrospective framing on 2026-11-04 ("okay let us keep it"). This is a counter-argument and the call stays his.

**2. Labels of the test taxpayer's other years are a measured shortcut, and known vs new entity is never decided (P4, USE-10 Must, SPLIT-9 Must, SPLIT-13).**
- **Problem.** `split` says only that "both recurring and new taxpayers occur". USE-10 requires deciding first whether the entity is known or new:
  - Known: history is legitimate and the previous outcome is a feature.
  - New: a grouped split.
- **What the definition does instead.** It drops `CTR_MATFIS` and builds "no taxpayer/label aggregates", yet keeps 64-75% of test rows' taxpayers in training. So the benchmark rewards rebuilding taxpayer identity without the id.
- **Evidence.**
  - The 24 registry columns map one to one onto 12,244 taxpayers (column auditor).
  - Dropping the test taxpayers' training rows costs +0.12 / +0.19 RMSE more than dropping the same number of random rows (split auditor, size-controlled). That is the decisive experiment (EV-1).
  - Recurring test rows go from 6.02 to 6.39 when their history is removed, while new rows barely move (claim auditor).
  - The task gamer gains 0.25-0.56 RMSE from labels carried across years, and nothing from mere presence.
  - The practitioner's "recurring worse than new" result is a raw comparison of two different groups of rows. It does not control for composition, so it does not refute the ablation.
- **Why it may break SPLIT-9.**
  - 69-85% of multi-year taxpayers have contiguous runs of years.
  - The chance of a zero label is 0.70 after a zero year, against a base rate of 0.25.
  - Zero/nonzero agreement decays with the year gap (0.861, 0.799, 0.744, 0.677).
  - Tunisian in-depth verifications cover several fiscal years at once (practitioner's sources).
  - In that case the 2016 label arrives together with the 2017 label. A training label then tells the test outcome, and the 2018 cut already shows the labels arrive late.
- **Against my own case (I measured this).** Only 14 / 30 / 35 nonzero test rows (1.6-1.8% of seen taxpayers) have the exact same label in training. One audit does not copy one amount across years, so the same-audit reading stays circumstantial (EV-6).
- **Rule that wins.** The tension table says a measured shortcut is removed whatever it costs the floor. Amended SPLIT-10 sets a gap where a measurement shows "a shortcut through recent labels": 48.7% of test rows have the year just before in training.
- **Remedy (a curator fact call, then a definition fix).**
  - (a) Under the planner framing: keep `CTR_MATFIS` as a non-feature group column and drop each window's test taxpayers from its training side (alfa_battle_2_0_task_2). Training shares become 81.6 / 60.0 / 38.9%, so the 2015 window falls under SPLIT-14 and the dataset ships under SPLIT-8 as SPLIT-14 directs.
  - (b) Only if the curator states that earlier years come from earlier, separate audits: apply USE-10 openly. Ship the previous label (or the id) so honest models get it too, and put the measured lift in the notes.
  - The current middle state meets neither.

**3. The paid-refund fields have a measured fill mechanism, so they fall under LEAK-10, not LEAK-38 (P4, LEAK-10 Must via LEAK-38's own text).**
- **Problem.** LEAK-38 says: "When a conditional test measures the mechanism (the field's ... fill, given the covariates known at the prediction point, differs by outcome), LEAK-10 applies and the field is dropped." The column auditor measured exactly that, then recommended keeping.
- **Evidence (my re-run).** My re-run predicts the fill from filing-time covariates, excluding the other process fields and `CTR_CESSAT`. It uses 5-fold cross-validation grouped by taxpayer, with 2 seeds.

  | Field | Observed / predicted, zero-adjustment rows | Observed / predicted, positive rows | Difference in residuals, 95% CI (taxpayer bootstrap) |
  |---|---|---|---|
  | `TVA_RESTIT` | 1.30 | 1.03 | 0.026 to 0.042 |

  `TVA_MTDJRTVA` (4.03 against 3.61) is miscalibrated in both groups, so it is weaker evidence.
- **Mechanism.** A refund is paid after a verification that found nothing. The practitioner confirms that a refund request triggers verification.
- **Precedent.** kick and expresso (2026-10-22) were dropped on the same kind of measurement. LEAK-10 says a small ablation (+0.022 RMSE) is no reason to keep.
- **Remedy (fix the definition).** Drop `TVA_RESTIT`, `TVA_MTORDTVA` and `TVA_MTDJRTVA`.

**4. `CTR_CESSAT` is a status looked up after the outcome (P4, LEAK-10 Must, weak).**
- **Evidence.**
  - All registry fields are constant within each taxpayer, so they are an extraction-time snapshot.
  - The ceased share falls from 5.5% (2013) to 2.7% (2017). That is the signature of a later cessation written back onto earlier years. LEAK-10 lists "attributes looked up after the outcome, unless the data shows they did not change".
  - Ceased rows have mean target 10.06 against 11.88. Dropping the column costs +0.015 RMSE, so the model uses it (column auditor).
- **Remedy.** Drop it. The obligation codes change slowly and can stay under the existing note. Name `CTR_RATISS` (a control sweep, a process field; 233 rows, R² about 0.001) in that note.

**5. Split departures are not recorded consistently (P4, SPLIT-19 Should, SPLIT-10 Should).**
- **SPLIT-19.** The source's test spans 2013-2018, so it is not a time split. The departure is recorded only as "a separate cross-cohort evaluation", with a stale "four". It needs an exception line giving the fact and the principle it serves.
- **SPLIT-10.** The same curator, on the same day, rejected the retrospective zero-gap reasoning on lt_vehicle_loan_default_prediction and amended SPLIT-10 to require measurements. Here, "no SPLIT-10 departure" rests on that replaced reasoning, and the notes omit the measurements (precedent checker).
- **Remedy (notes).**
  - Put in the notes the 2017 measurements that now exist: nonzero median p=0.36, zero share 0.249, conditional residual +0.18 like 2016's.
  - Add the row-count fall (0.53) as selection, not label censoring.
  - Add the left-truncated 2013 cohort (SPLIT-20).
  - Answer the precedent checker's consistency check on decision 1.

**6. Provenance text is wrong (P5, PROV-13 Should; EV-7).**
- `download_description` says "SOURCE_MANIFEST.json records identities". No such file exists; `MIRROR_SOURCE.txt` is there instead.
- The file used came from a participant GitHub mirror. Its byte identity with Zindi rests on Lennart's statement, which nobody here could check (login needed).
- **Remedy.** Remove the sentence, cite the SHA-256 values and `MIRROR_SOURCE.txt`, and name the mirror as the copy used.

**7. Stale prose after the 2018 cut (writing.md, procedure; quality, not a reason to exclude).**
- **Wrong now:**
  - "Six annual markers"
  - "No row is filtered" (365 rows of 2018 are)
  - "All 103 retained predictors … four annual holdouts" (now 100 inputs and three)
  - "latest cohort (365 rows)" (the latest is 2017 with 1,629)
  - the accepted warning `task_time_on_few_unique`: "six … cohorts; four outer windows", repeated in README lines 64 and 236. Myunghwan's acceptance rested on that wording, so update its premise.
- **Also:**
  - "anonymized" stays in `row` and in the LEAK-38 note although the tag was dropped.
  - `changes` states "inspections were still open" as a fact, where the evidence supports only an inference.
- **Notes to add:**
  - `TVA_CRDFIN` is the closing credit (carries over to the next year's `TVA_CRDINI` in 89.9% of consecutive pairs), not the "Initial Credit" the dictionary says.
  - 59% of the RMSE's squared error comes from the true zeros, so the metric mostly scores whether an audit finds anything. MET-4 keeps RMSE; this is a note only.
- **Remedy.** Reword these lines.

```text
Verdict: ship after changes.
Validity: USE-1 triggered (retrospective actor not real; reframe to the audit planner); USE-10/SPLIT-9 triggered (measured
  taxpayer-label shortcut +0.12-0.19 RMSE beyond size; decide known vs new, then (a) drop test taxpayers' training rows
  or (b) ship history openly); LEAK-10 via LEAK-38 triggered (refund fill 1.30 vs 1.03, CI excludes 0: drop 3 fields);
  LEAK-10 weak (CTR_CESSAT: drop); LEAK-24 holds for 2017; MET-2/3/4 hold.
Procedure/Quality: SPLIT-19/SPLIT-10 exception lines and measurements; PROV-13 manifest sentence; writing.md stale counts.
For the curator: issue 2, a fact call on same-audit timing (no audit dates exist).
```

</details>

<details><summary>Advocate rebuttal</summary>

**Rebuttal (advocate): `tunisian_fraud_detection_challenge`**

I ran three new tests for this rebuttal, so it contains new facts. I also re-ran the critic's fill test.

**New facts**

- **N1. The amended SPLIT-10 test of the most recent year, run the way L&T's was:** drop year T−1 from training, and compare with dropping the same number of random rows (LightGBM, 3 seeds, test years 2017 / 2016 / 2015).
  - Dropping T−1 gives 6.143 / 6.122 / 6.317. The random control gives 5.995 / 6.038 / 6.187. So T−1 is worth **+0.148 / +0.083 / +0.130** beyond its size.
  - The loss lands on test rows whose taxpayer appears in T−1: +0.39 / +0.23 / +0.34 against the random control. On the other test rows it is −0.01 / +0.06 / +0.15.
- **N2. The same test after removing the test taxpayers' rows from training** (the alfa_battle remedy): T−1 is then worth only +0.055 / +0.028 / +0.025 beyond its size. That is about the ±0.03 noise level.
- **N3. The critic's fill test reproduces exactly.**
  - `TVA_RESTIT`: filled in 14.6% of zero-adjustment rows against 11.2% predicted (ratio 1.30). Among positive rows it is 2.30% against 2.24% (ratio 1.03). The difference has a 95% interval of 0.026 to 0.042.
  - `TVA_MTORDTVA`: 22 filled rows, ratio 14.8 against 12.7.
  - `TVA_MTDJRTVA`: ratio 4.03 against 3.61.

---

**Critic 1: no real actor in the use case (USE-1, USE-9). Concede the wording.**

The archived-dossier analyst describes nobody, and the definition holds three framings at once. The fix is the planner rewrite plus the `Selection Bias` marker, and my opening already proposed both. The data stays.

Lennart kept the retrospective framing on 2026-11-04, so the final word is his. The critic says the same.

What follows from conceding this matters, so I state it. Under the planner framing, year N is scored once its returns arrive in N+1. The practitioner's sources say a fiscal year keeps gaining audits until about N+4, and the row counts confirm it. So the T−1 label is usually not yet known at that moment. That removes the "known history" defense I made in my opening point 3 (see the next point).

**Critic 2: other-year labels of the test taxpayer are a shortcut (USE-10, SPLIT-9). Concede, given N1 and N2. The remedy is the critic's option (a).**

My opening rested on "the shortcut has not been shown." N1 now shows it:

- the most recent training year helps beyond its size, by +0.08 to +0.15;
- almost all of that help reaches test rows whose own taxpayer is in that year.

That is "a shortcut through recent labels" in amended SPLIT-10's words. It is also "training labels shown to tell a test row's outcome" in the tension table (principles.md, SPLIT-9 against SPLIT-14).

It still does not prove that one audit covered both years (EV-6). The critic's 14 / 30 / 35 identical labels keep that reading circumstantial. But the known-entity defense under USE-10 needs the earlier label to have been known at the prediction point:

- Under the planner framing it was not, by the maturation evidence above.
- Under the retrospective framing there is no real actor to know it (critic 1).

So the ieee_fraud_detection precedent does not carry over: there the carried labels were plausibly settled before the next transaction. alfa_battle_2_0_task_2 is the closer case.

What follows:

- **Remedy (a).** Keep `CTR_MATFIS` as a non-feature group column. Drop each window's test taxpayers from its training side.
  - Training shares become 81.6 / 60.0 / 38.9%.
  - N2 shows this also takes care of SPLIT-10: once the filter is in, a one-year gap buys nothing beyond noise, so no gap is needed on top. I ask that this go in the notes as the SPLIT-10 measurement.
- **The 2015 window at 38.9% breaks SPLIT-14.** The tension table removes a measured shortcut whatever it costs the floor, and SPLIT-14 then directs SPLIT-8. The dataset is fixed, not excluded.
- **Option (b), shipping the previous label openly,** is open only if Lennart states that earlier years came from separate, earlier audits. The data cannot show that.

I withdraw my opening proposal to keep the split with a note only. Option (a) is now the mildest remedy that removes the measured shortcut.

**Critic 3: the refund fields fall under LEAK-10 through LEAK-38's own text. Concede for `TVA_RESTIT`. Partly dispute the other two.**

- **`TVA_RESTIT`.** Concede (N3). LEAK-38 says that when the fill, given the covariates, "differs by outcome, LEAK-10 applies and the field is dropped." The text sets no size threshold, so my comparison with kick's 20× ratio does not save the field. Among positive rows the model is calibrated (1.03); among zeros it is not (1.30). That is a differential, and the mechanism is plausible: a refund is paid after a verification that found nothing. The fact that dropping it costs only +0.022 is no defense under LEAK-10.
- **`TVA_MTORDTVA` and `TVA_MTDJRTVA`.** Dispute that the test measured a mechanism. Both are miscalibrated by about the same ratio in both groups (14.8 against 12.7, and 4.03 against 3.61). Their absolute residual gap comes from the higher fill base among zero rows. It does not show that the fill "differs by outcome." `TVA_MTORDTVA` has only 22 filled rows.
- **The call.** They can stay under LEAK-38 with the numbers in the note. They belong to the same refund chain, though, and dropping all three costs +0.022, which is within noise. I do not oppose dropping all three. That is a curator call either way.

**Critic 4: `CTR_CESSAT`. Agreed.** We already converged: drop it, and name `CTR_RATISS` in the LEAK-38 note.

**Critic 5: SPLIT-19 and SPLIT-10 recording. Concede, with the content updated by N1 and N2.**

- **SPLIT-19.** Add an exception line naming the source's 2013-2018 test and the principle it serves.
- **SPLIT-10.** The notes should carry:
  - the 2017 measurements (zero share 0.249, nonzero median p=0.36, residual +0.18);
  - the 0.53 count ratio as selection, not label censoring;
  - the left-truncated 2013 cohort (SPLIT-20);
  - N1 and N2 as the recent-label test.
- **The precedent checker's consistency question.** With remedy (a), this case lines up with L&T: the zero gap rests on a measurement, as the amended rule requires. That is the checker's option (a), now with the test it asked for.

**Critic 6: provenance (PROV-13). Concede.**

- Remove the `SOURCE_MANIFEST.json` sentence.
- Cite the SHA-256 values and `MIRROR_SOURCE.txt`.
- Name the participant GitHub mirror as the copy used.

Both hashes match the stated values. Byte identity with the Zindi file rests on Lennart's statement; record it as such.

**Critic 7: stale prose. Concede all of it.** That includes the additions I did not have:

- "anonymized" in `row` and in the LEAK-38 note;
- "inspections were still open" in `changes`, which should be worded as an inference;
- the `TVA_CRDFIN` closing-credit note (89.9% carry-over);
- the 59%-from-zeros metric note.

The `task_time_on_few_unique` acceptance stands with its counts corrected.

---

**Where this leaves the case**

Both sides now say "ship after changes," and no point argues for exclusion. The changes:

1. **Split:** keep `CTR_MATFIS` as a group column (not a feature) and drop each window's test taxpayers from training. The 2015 window goes under SPLIT-8, or Lennart states the separate-audit fact and takes option (b).
2. **Columns:** drop `CTR_CESSAT` and `TVA_RESTIT`. Drop or note `TVA_MTORDTVA` and `TVA_MTDJRTVA` (curator call).
3. **Use case:** reword it to the planner, and add the `Selection Bias` marker.
4. **Notes:** SPLIT-19 exception, the SPLIT-10 measurements (2017 checks, N1 and N2), SPLIT-20, the RMSE note, and `TVA_CRDFIN`.
5. **Prose and provenance:** the stale counts, "anonymized", and the PROV-13 sentence.

What still holds from my opening, unchallenged:

- target and metric (MET-2/3/4, USE-5);
- the 2018 cut, with 2017 kept (LEAK-24);
- signal (RF 5.970 against a dummy at 7.056);
- 0.0% copies across the cutoff;
- no honest-model flaw.

```text
Rebuttal verdict: ship after changes (converged with critic).
Conceded: USE-1 wording; USE-10/SPLIT-9 shortcut now measured (T-1 worth +0.08-0.15 beyond size, on same-taxpayer rows;
  gone after test-taxpayer filter, +0.025-0.055) -> remedy (a), 2015 window under SPLIT-8; TVA_RESTIT LEAK-10 via
  LEAK-38 (fill 1.30 vs 1.03); CTR_CESSAT drop; SPLIT-19/10/20 notes; PROV-13; writing.md.
Disputed: TVA_MTORDTVA/TVA_MTDJRTVA (equal-ratio miscalibration, no differential; curator may drop the chain at +0.022).
Curator calls: framing (Lennart's "keep it" stands until he changes it); option (b) only on a separate-audit fact;
  SPLIT-8 handling of the 2015 window.
```

</details>

<details><summary>Critic rebuttal</summary>

**Rebuttal (opponent): `tunisian_fraud_detection_challenge`. Ship after changes.**

The advocate and I now agree on most of this. Three disputes remain: taxpayer history (advocate 3), `TVA_RESTIT` (advocate 5) and how the SPLIT-10 departure is recorded (advocate 2 and 6). I narrow my refund remedy from three fields to one.

**Advocate 1: 2017 is not censored, LEAK-24 holds. Concede.**
- Four agents found 2017 in band:
  - zero share 0.249
  - nonzero median p=0.36
  - residual +0.18 / +0.132, the same as 2016
- The row-count fall (ratios 0.95, 0.76, 0.71, 0.53) is selection. A note is the right remedy. This was already my point 5.

**Advocate 2: SPLIT-14 holds and no one-year gap. Partly concede, partly dispute.**
- Conceded:
  - The windows meet SPLIT-14 (92.2 / 77.4 / 56.5%).
  - A blanket one-year gap would leave the 2015 window training on 29%, so the gap loses to SPLIT-14.
- Disputed: that this means "no SPLIT-10 departure".
  - Amended SPLIT-10 sets a gap "where the source or the context documents late labels". The 2018 cut ("inspections still open") and the practitioner's sources (audits reach back about 4 years, one verification covers several years) document exactly that.
  - The trigger is met. The gap is set aside for SPLIT-14, and the tension table says that departure is "recorded as an exception" (alfa_battle_2_0_task_2, lending_club). Writing "no departure" is wrong.
- Disputed: "training on only the last 1-2 years is no better" as evidence.
  - That tests how recent the training years are. It does not test the shortcut amended SPLIT-10 names: a shortcut through the labels of the same entities.
  - The test of that shortcut is the size-controlled one, and it is positive (+0.12 / +0.17 / +0.19 RMSE).
- Remedy: a SPLIT-10 exception line serving SPLIT-14, citing the 2018 cut, as in alfa_battle_2_0_task_2. The precedent checker's consistency question (L&T, same curator, same day) stays open until it is answered.

**Advocate 3: taxpayer history is LEAK-34 known-entity history, and a note is enough. Dispute. This is still the main point.**
- Conceded:
  - The fact that would trigger SPLIT-9 (one audit sets several fiscal years) is not proven. No audit dates exist. I said this in my own brief: only 14 / 30 / 35 nonzero test rows carry an identical training label (EV-6).
  - So the alfa_battle filter is not forced by measurement. It is option (a), and only if the curator rules same-audit.
- Disputed: that a note satisfies the rules under the advocate's own reading.
  - LEAK-34 makes history legitimate "a known entity: USE-10".
  - USE-10 (Must) says that for a known entity "the split is temporal and **the previous outcome is a feature**".
  - The definition does the opposite. It drops `CTR_MATFIS`, ships "no taxpayer/label aggregates", and leaves history reachable only by re-identifying taxpayers through 24 registry columns (12,244 fingerprints for 12,244 taxpayers).
  - The result is a benchmark where a participant who rebuilds identities gains 0.25-0.56 RMSE (task gamer). That is 4-9%, against noise of about ±0.03. An honest model is denied the same information.
  - The advocate's own sources point the same way. The practitioner says the DGI planner "would always have" each taxpayer's audit history, which argues for shipping it openly, not for hiding it and noting the gap.
- Disputed: ieee_fraud_detection as the governing precedent.
  - There the history was an explicit feature (`uid`, kept as a column).
  - Its value was 0.001-0.007 AUC.
  - Its carried labels follow the host's documented labelling rule.
  - Here the history is hidden, worth +0.12-0.19 RMSE beyond a size control (a quarter to a third of the model's gain on recurring rows), and no host rule explains the co-movement. The precedent supports making history explicit. It does not support leaving it implicit.
- Rule that wins: USE-10 (Must) under the known-history reading; SPLIT-9 (Must) and the tension table under the same-audit reading. A note alone meets neither.
- Remedy, a curator fact call and then one definition change:
  - (b) Default, under known history: ship the previous-year label (or the taxpayer id) as an explicit feature. Measured: 5.996 → 5.462 RMSE. Notes give the 64-75% seen share and the lift.
  - (a) Only if Lennart rules that years are adjudicated together: drop each window's test taxpayers from training. The 2015 window then trains on 38.9% and goes under SPLIT-8.
  - The advocate's note text (implicit key, 64-75%, +0.12-0.19, unknown audit timing) should go in under either option.

**Advocate 4: `CTR_CESSAT`, drop it. Agreed.**
- One correction: "+0.015, below noise" is not a reason under LEAK-10, which drops looked-up attributes whatever their size. The remedy is the same, so nothing is in dispute.
- Name `CTR_RATISS` in the LEAK-38 note: agreed.

**Advocate 5: refund fields stay under LEAK-38. Partly concede: two of three fields.**
- I re-ran `fill.py`: LightGBM, 5-fold cross-validation grouped by taxpayer, 2 seeds, taxpayer bootstrap with 300 draws, filing-time covariates only.

  | Field | Filled rows | Observed/predicted, zero-adjustment rows | Observed/predicted, positive rows | Difference in residuals, 95% CI |
  |---|---|---|---|---|
  | `TVA_RESTIT` | 1,039 | 1.30 (14.6% vs 11.2%) | 1.03 (2.30% vs 2.24%) | 0.033 [0.026, 0.042] |
  | `TVA_MTORDTVA` | 22 | 14.8 | 12.7 | – |
  | `TVA_MTDJRTVA` | 151 | 4.03 | 3.61 | – |

  - `TVA_MTORDTVA` and `TVA_MTDJRTVA` are miscalibrated in both groups. The column auditor's own run gives 2.84 against 2.87.
- Conceded: no differential is measured for those two. They stay under LEAK-38 with the numbers in the note.
- Disputed for `TVA_RESTIT`:
  - Two independent runs find the same differential: the column auditor's 1.27 vs 1.01, and mine at 1.30 vs 1.03 with a confidence interval that excludes 0.
  - LEAK-38's text sets no size threshold. It says "When a conditional test measures the mechanism (the field's ... fill ... differs by outcome), LEAK-10 applies and the field is dropped."
  - "Far below kick's about 20x" misreads the precedent. kick's `PRIMEUNIT`/`AUCGUART` were dropped at 42.3% vs 7.8% (about 5x). The rule asks whether the fill differs, not by how much.
  - The advocate's precedents do not apply: african_credit (`Amount_Funded_By_Lender`), sendy (`Distance (KM)`) and medical_facility (`ExpectedDelayNextExam`) were all fields whose timing could not be tested. LEAK-38 "covers only fields whose timing cannot be tested".
  - "+0.022 is within noise" does not save it. LEAK-10 does not keep a leak because it is small.
  - There is a plausible mechanism: the practitioner says a refund request triggers verification, so a refund paid means a verification found nothing.
- Rule: LEAK-10 (Must) through LEAK-38's own text, with kick and expresso (2026-10-22) as precedent.
- Remedy, narrowed: drop `TVA_RESTIT` only. The LEAK-38 scope amendment for named fields ("untestable timing, not anonymity") is due, as both briefs say.

**Advocate 6: framing and metric are curator decisions. Concede precedence and dispute one claim.**
- Conceded:
  - Lennart's "okay let us keep it" outranks my USE-1 reading, so my point 1 stays a counter-argument.
  - We agree on the wording remedy:
    - one framing in all three places;
    - drop "scanning a new year";
    - fix the kit's "available for training" prediction point;
    - name the SPLIT-19 departure;
    - add the `Selection Bias` marker;
    - add the 59%-from-zeros metric note.
  - RMSE stays under MET-4. That was never disputed.
- Disputed: that option (a) of the L&T consistency question "now has its measurements". The equal-size control is the recent-label shortcut test, and it came out positive, not null. Option (a) requires that the test "shows nothing". So the answer to the consistency check has to go through my point 2 / advocate 3, not around it.

**Advocate 7: stale prose, manifest, tooling. Concede, with one addition.**
- The hashes match the stated values, but the bytes came from a participant GitHub mirror. Identity with Zindi rests on an unverified statement (EV-7).
- The sentence must name the mirror and `MIRROR_SOURCE.txt` as the copy used, not imply a manifest.
- Also reword "anonymized" in `row`, and make "inspections were still open" in `changes` an inference.

```text
Verdict: ship after changes.
Agreed: 2017 kept (LEAK-24 holds, notes); CTR_CESSAT dropped; TVA_MTDJRTVA/TVA_MTORDTVA kept under LEAK-38 with
  fill numbers; framing wording, Selection Bias marker, metric note; stale prose; PROV-13 sentence.
Disputed, with the rule that wins:
  - USE-10 Must: a note-only remedy fails under both readings; ship previous label/id (b), or drop test taxpayers'
    training rows (a) if the curator rules same-audit (SPLIT-9 Must, tension table).
  - LEAK-10 via LEAK-38 text: TVA_RESTIT fill 1.30 vs 1.03, CI [0.026, 0.042], reproduced by two agents: drop it.
  - SPLIT-10: trigger met by documented late labels; record an exception serving SPLIT-14, not "no departure".
For the curator: same-audit fact call (decides a vs b); answer the L&T consistency check.
```

</details>
