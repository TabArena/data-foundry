---
unique_name: loan_default_prediction_challenge
name: loan-default-prediction-challenge
checked_by:
- Myunghwan
data_foundry_status:
- WIP (Triage)
claimed_by: Myunghwan
suggestion: 'Yes'
priority: 2
decision_markers:
- TBD
collections:
- New (BeyondArena)
original_source: Zindi
year: '2018'
domain: finance
required_split:
- Random (IID)
problem_type: Binary Classification
original_data_state: Database (or multiple to-be-joined tables)
source_links:
- https://zindi.africa/competitions/loan-default-prediction-challenge/data
- https://zindi.africa/competitions/data-science-nigeria-challenge-1-loan-default-prediction
- https://zindi.world/competitions/data-science-nigeria-challenge-1-loan-default-prediction/data
- https://zindi.world/competitions/loan-default-prediction-challenge
v2_path: datasets/_dev/tabarena-v0pt2/loan_default_prediction_challenge/dataset.py
source_row: 898
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-11-03):** `TBD -> Yes`, priority 3: source-backed repeat-loan on-time-settlement prediction, with history joins and label-availability risks still to qualify. Requested by Myunghwan; no human acceptance inferred. This deep pass supersedes unsupported claims in the older AI block retained below.
- Source: 2018 Data Science Nigeria challenge on Zindi, evidenced by its October 11, 2018 discussion; the record's other competition is the March-April 2022 AfroPavo rerun. Three tables per side: scored loans `trainperf`, demographics, prior loans, linked by `customerid`. A participant notebook reports 4,368 x 10 / 4,346 x 9 / 18,183 x 12 respectively; organizer counts, collection period, unique customers and class support were not measured. Source schema: https://zindi.world/competitions/data-science-nigeria-challenge-1-loan-default-prediction/data . Participant copy: https://github.com/ZainabAbari/SuperLender-Loan-Prediction/blob/main/loan.ipynb .
- Target/use case: lender scores a repeat application for approval/offer decisions; `good_bad_flag` distinguishes timely settlement (Good=1) from not settling on time (Bad=0), not verified permanent default. One prediction row per scored loan; one scored loan per customer is unverified. Source intent fits directly; issued-loan selection, label horizon/grace rule and demographic snapshot timing need qualification (USE-1/3/5/8).
- Split: temporal by application `creationdate`, subject to actual date coverage, supported windows, repeated-customer checks and training-label maturity (SPLIT-1/3/9/10/14). Prior-loan amounts/terms are history; payment/settlement facts are usable only after their event dates. Current final terms and `approveddate` require application-time availability checks. Do not assume every prior loan had closed or exclude all outstanding history.
- Siblings/duplicates: only this record matches SuperLender and canonical challenge slugs among 1,293 pinned records. Zimnat, African credit scoring and LT vehicle-loan records have other sources; the African credit record supports temporal known-customer history and mature labels. FUTA's 2021 hackathon repeats the narrative, and Lanfrica indexes the challenge/repositories; neither proves an independent cohort. No OpenML membership or introducing paper found in bounded searches; not exhaustive.
- Deep pass: https://zindi.africa/competitions/data-science-nigeria-challenge-1-loan-default-prediction/discussions/30684 reports clock-only test dates; thread /72 asks about apparently all-Good labels without settling counts. Both remain unverified on organizer bytes. The public notebook above joins histories before a random row split, a procedure that can repeat scored loans across sides; aggregate as-of history and check join cardinality, rather than copying it. A winning participant's first-person account describes prior-loan feature engineering and an Azure neural network: https://medium.com/ai-saturdays-lagos-articles/my-1000-dollars-story-ecf060fffb3b . No result was reproduced. Some thread bodies, a vote-ranked notebook catalog and the public competition API were inaccessible.
- Metric: both competitions define hard-label misclassification error (Evaluation, https://zindi.world/competitions/loan-default-prediction-challenge ); keep it, or accuracy with error=1-accuracy documented (MET-1/4/11). No official 0.5 probability threshold is stated. Learn thresholds within training; ROC AUC/log loss diagnose signal, not automatically replace the source metric. The older override rationale is unsupported (MET-4/6).
- Risks for add-dataset: authenticate source release; test label classes/maturity and temporal support; mask future history events; verify demographic/offer timing; preserve one scored-loan row and all loan/customer lineage; measure duplicates. No leak, constant target or irreparable date damage has been demonstrated. Current challenge pages differ on redistribution terms; settle release permission before redistribution, without changing the scientific recommendation (EV-4).
- Priority: base 1, gap 0 (188 accepted pinned records: finance 17, binary 86, temporal 46, Zindi 6, none thin), use case +1, documented source +1, provisional shape +1 from participant counts/mixed types, known join/timing risk -1 = 3. Official sample support remains an add-stage check. No fast reject, so no reject-checker is triggered; no add-stage panel/probes/build ran. Next: review-screened-candidates; proceed/later/reject remains Myunghwan's decision.

**Screening (AI, 2026-10-22):** `TBD -> Yes`, priority 3: SuperLender's repeat-loan default at application, a direct credit decision; the record's link is a 2022 rerun of Data Science Nigeria's Challenge 1.
- Source: SuperLender data first released in Zindi's "Data Science Nigeria Challenge #1: Loan Default Prediction" (start 2018-10-11, https://zindi.africa/competitions/data-science-nigeria-challenge-1-loan-default-prediction); the record's link is the AfroPavo Analytics internship rerun (2022-03-15 to 2022-04-16), whose API names the DSN challenge as its parent. As published: three tables per split, `traindemographics.csv`, `trainperf.csv` (the repeat loan to score, target `good_bad_flag`, "good = settled loan on time; bad = did not settled loan on time"), `trainprevloans.csv` (the customer's earlier loans), joined on `customerid`. Rows not checked (Zindi data needs a login).
- Use case: "These two fundamental drivers need to be determined at the point of each application to allow the credit grantor to make a calculated decision ... if an applicant should get a loan, and if so - what the size, price and tenure of the offer will be" (description page); fit direct; regime temporal (`approveddate`, `creationdate` ship; one repeat loan per customer, so grouping adds nothing).
- Siblings and duplicates: no other record of the SuperLender data (grep: superlender, data science nigeria); other credit-default records (zimnat_loan_default_predictio, african_credit_scoring_challenge, lt_vehicle_loan_default_prediction) are other lenders. External collections: none found.
- Papers and pages: the two competition pages; no paper.
- Metric: error rate, "the percentage of loans you predict incorrectly" (Evaluation page of both competitions), the leaderboard metric (MET-4); hard labels at 0.5 with no costs stated, so a candidate for overruling under MET-4 and MET-6 once probed; inputs none.
- Risks for /add-dataset: `trainprevloans` holds `closeddate` and `firstrepaiddate`, known only for loans closed before the application date: filter by date (LEAK); `totaldue` and `termdays` are offer terms set with the decision (USE); aggregation of previous loans (joins); exact birthdate and GPS coordinates to coarsen (personal data).
- Priority: gap - (finance, binary, temporal not thin), use case + (actor and decision named), source + (the page documents every column), shape + (mixed types and dates; the row count not checked), risk - (three tables to join, post-application dates).

A Zindi loan-default competition where the task is predicting whether a loan was good or bad, a classic real-world tabular binary classification problem in credit risk. This maps well to the benchmark criteria: genuine predictive task, clear target, finance domain. The record lacks size and split details, so it cannot be confirmed Yes outright. A human must verify dataset size after cleaning, the exact target definition, absence of leakage, and whether a temporal/grouped split (by applicant or time) is warranted, but it is a plausible Yes.

---

Predict if a loan was good or bad

CC (2026-11-04, Myunghwan): Proceed to add-dataset qualification of the presented SuperLender repeat-loan timely-settlement task, by explicitly requesting tabarena-add-dataset. The original request is saved with attribution in the review history. This authorizes actual-data checks, probes and the required independent panel, not final inclusion, a build, or a commit. Application-time inputs, label maturity, history joins and temporal support remain factual checks; no timing exception or final split is pre-approved.

**Assessment (AI, 2026-11-04):** Added for review as an explicitly approximate repeat-loan timely-settlement task, with the full independent panel recommending retention after wording repairs and Myunghwan's disposition of current-term timing, undated mutable profiles and participant-copy authenticity. All 4,368 source-copy labels remain; history is aggregated as of application with later payment/settlement events masked, and raw IDs/current approval excluded. ForcedIIDFromTemporal follows SPLIT-8 for this one-month release with missing label-arrival/grace documentation; no prospective validity or maturity exception is claimed. Source hard-label error remains accuracy by identity (MET-4/11). The pinned Megan Beckett copy is traceable but not authenticated against organizer bytes. Earlier unverified screening claims are superseded by these measurements and the definition; final inclusion/build remains undecided. Priority 2: gap 0, use case 0 (approximate fit), source +1 (original publisher's task/codebook), shape +1 (4,368 units, 32 mixed-type predictors), risk -1 (joins, input timing and unknown label rule).

CC (2026-11-05, Myunghwan): Issues 1–3: "1. keep; 2. keep; 3. accept." Keep recorded current loanamount, totaldue and termdays with application-time availability unverified; keep undated mutable customer profiles with timing unverified; accept the identified pinned participant-copy provenance gap without certifying organizer-byte equality. These are the three numbered issue choices; no overall inclusion verdict, split-field mark, build, commit or timing exception is inferred.

**Assessment (AI, 2026-11-05):** Independent review found the three decisions consistent with the bounded approximate task and amended provenance rules, with no new exception or established later-update mechanism. The decisions retain all 32 predictors and the existing Good/Bad labels, folds and metric; only attribution/notes and review status change. Genuine unavailable labels may be represented as NA, but current eventual labels are not cleared and missing arrival times are not fabricated. Overall inclusion and required_split alignment remain unmarked.

CC (2026-11-08, Myunghwan): "I think AUROC looks better than. Accuracy is skiewed". Change the declared metric from accuracy to ROC AUC after the preceding source-override explanation. This is the metric choice only; required_split remains unmarked.

**Exception to MET-4 (2026-11-08, Myunghwan):** The source scores hard-label misclassification error (accuracy = 1 - error). Myunghwan knowingly chose threshold-free ROC AUC after the source override was explained. On the unchanged nine splits, always Good scores 0.782051 accuracy and 0.5 AUC; matched untuned LightGBM with training-only threshold selection scores 0.787698 accuracy and 0.694156 AUC. The curator prefers comparing discrimination rather than this majority-dominated hard-label score. This is a case-specific preference, not proof accuracy is invalid or a claim that the organizer chose a ranking workflow. Serves P3: the curator-selected criterion for comparing this bounded timely-settlement prediction task. No lender cost ratio or operational threshold is invented.

**Assessment (AI, 2026-11-08):** Independent actual-mark consistency review supports preserving this informed case-specific preference. Declare context roc_auc under MET-11, not source or stand-in. The metric changes; all data, target labels, predictors and exact folds remain unchanged. Original source error/accuracy and matched diagnostics remain historical evidence. AUROC does not establish calibration, deployment validity or lending profit. No split-field or build approval is inferred.

CC (2026-11-08, Myunghwan): the declared metric roc_auc is checked through the applied metric-change choice above. Source error/accuracy is deliberately overruled by the recorded case-specific MET-4 exception, not retained as the primary metric. Only required_split remains unmarked.

CC (2026-11-08, Myunghwan): Random or temporal split is acceptable, with care that the same borrower does not occur in both train and test. Retain the current Random (IID) evaluation and align required_split to it; the ForcedIIDFromTemporal tag and approximate-fit limits remain. Exact words are preserved in the bound review history.

**Assessment (AI, 2026-11-08):** Fresh source-to-native one-to-one lineage confirms 4,368 scored loans from 4,368 distinct customer IDs. Every one of the nine actual folds has zero train/test customer overlap; fold indices and the recipe are unchanged. Earlier loans are as-of predictor inputs, not additional supervised rows. This addresses the named borrower-overlap mechanism, not every possible timing leak. Independent consistency applies SPLIT-8 without a new exception. All numbered issues, metric and field disagreements are settled; apply ship by the current review procedure's default (not an invented explicit human ship statement). Scientifically ready for a separately requested build; no build, commit, publication, claim release or DF: Yes is applied here.

CC (2026-11-08, Myunghwan): "ship this". Explicitly approve the reviewed SuperLender definition to ship with context roc_auc and the current Random (IID) split, retaining ForcedIIDFromTemporal and approximate-fit limitations. All previously approved features, labels and provenance limits remain as documented.

**Assessment (AI, 2026-11-08):** Independent actual-verdict consistency confirms this explicit ship decision agrees with the completed review and previously applied default-ship disposition. No task, data, metric, split, timing or authenticity finding changed. Fresh ownership is retained; this review ship verdict accepts the definition for a later requested build under the pinned review procedure. No build, commit, publication, DF: Yes or claim release is inferred.
