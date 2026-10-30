---
unique_name: medical_facility_operational_data
name: Medical Facility Operational Data
checked_by:
- Myunghwan
data_foundry_status:
- WIP (DF)
claimed_by: Myunghwan
suggestion: 'Yes'
priority: 3
tags:
- Non-IID (Temporal)
collections:
- New (BeyondArena)
original_source: Other
year: '2020'
domain: medical & healthcare
required_split:
- Temporal (NON-IID)
problem_type: Regression
original_data_state: One Table
source_links:
- https://www.kaggle.com/datasets/weirdolucifer/medical-facility-operational-data
- https://doi.org/10.7910/DVN/X4SJWS
- https://medicalanalytics.group/operational-data-challenge/
- https://doi.org/10.1038/s42256-020-0176-3
v2_path: datasets/_dev/tabarena-v0pt2/medical_facility_operational_data/dataset.py
source_row: 850
type_adapter_id: curation-record-v1
---

## Comments

CC (2026-10-28, Myunghwan): "ship this". Final scientific inclusion approved for Medical Facility Operational Data: all four facilities and original signed delay/wait targets, categorical facility context, accepted nine approximate source-order windows and option A ordinary per-visit MAE with equal mean across windows.

**Assessment (AI, 2026-10-28; final review-added verdict):** Actual final ship applies to the reviewed source identities after both split and scoring decisions were applied. Independent consistency review found no reflection required. All 130,431 rows, 88 predictors and nine train/test memberships remain qualified; prior source/data audits, 90 saved-model replays and full ten-role panel remain applicable. Clock/cadence and estimator/booking lineage limitations remain documented. No scientific issue remains open. Accepted for later explicitly requested build; claim and WIP remain until repository integration. Historical comments below retain prior states and are superseded by this final verdict.

CC (2026-10-28, Myunghwan): "Is MAE the main metric from the original task? If so, our current imbalance is somewhat acceptable." Retain ordinary per-visit MAE and the proposed standard equal mean of nine window scores, following verification that the original challenge deliberately uses MAE. Final overall inclusion remains undecided.

**Assessment (AI, 2026-10-28; MAE review):** The primary author challenge specifies MAE-based feature-reduction tolerance and an MAE-reduction goal. It does not prescribe a combined facility/window weighting. The current composition is retained under the curator's conditional acceptance; it is not presented as an official source aggregation. F3 contributes 45.3% of absolute error versus 61.0% of squared error in the saved shared-model diagnostics. Independent consistency review found no reflection required. Close issue 5, preserve all source rows, targets, predictors and exact splits, and retain per-facility diagnostics. No final ship inferred.

CC (2026-10-28, Myunghwan): "accept this split". Accept the proposed nine all-facility common source-event-order windows, strict training arrival/exam-start availability and intact ties, with the disclosed clock alignment and real-calendar limitations. Preserve all exact memberships. Scoring/aggregation (issue 5) and final inclusion remain undecided.

**Assessment (AI, 2026-10-28; split acceptance):** Independent consistency check found no reflection needed. Closed issue 3 and preserved its original text and actual snapshot-bound mark. Acceptance records the approximation, not verification of intra-day synchronization or real deployment cadence. No row, label, predictor, metric or split change; prior all-facility probes, saved predictions and model replays remain applicable.

**Assessment (AI, 2026-10-28; all-facility pre-human review):** Corrected scope retains all 130,431 source visits, original signed F1-F3 delay/F4 wait and categorical facility context, with 88 predictors. Validity: authenticated author workbook, all-row/label/type reconstruction, exact nine source-order memberships and 90 exact saved-model replays support the candidate. Planned inputs and completion histories remain; active-exam elapsed identities restore mintime/maxtime, and only F4 IsLast is masked. Value: fresh fixed pooled/per-facility checks show useful signal and measured loss-scale differences; F3 has 20.7% of tested visits but 45.3% of shared-model absolute error, while F4 has 45.0% of visits and 17.4% of that error. No native task flags. Quality: original signed targets, structural missingness and distinct source histories preserved. The old scientific-discovery tag is contradicted by the verified source task and removed; dated history remains. The source MAE formula is computable, so its origin is source, not an uncomputable-metric stand-in. Cross-facility aggregation and acceptance of approximate global source order remain human choices; clock/estimator/booking snapshot and real-patient linkage limits are not promoted to verification. Full panel recommends retention after those choices; no human ship exists. Review issues 3 and 5 plus the overall verdict are pending. Priority 3: gap 0 (no thin medical/regression/temporal axis), use case 0 (approximate archival operational fit), source +1 (authenticated original author), shape +1 (130k mixed operational rows), risk 0 (no demonstrated unrepairable defect).

CC (2026-10-28, Myunghwan): Redo add-dataset and review-added-datasets for Medical Facility considering the previous scientific decisions. Preserve the earlier explicit all-facility main task and meaningful facility context. Complete per-facility and shared-predictor error/support/contribution checks before returning the metric/aggregation choice and final inclusion question. This request is not an F4-only approval, final ship, build or commit.

**Assessment (AI, 2026-10-28; all-facility correction in progress):** The previously completed F4-only package did not fulfill the saved scope. The corrected candidate retains all 130,431 source visits and signed F1-F3 delay/nonnegative F4 wait, with facility categorical and the union of source features. Fresh all-group source/column audits support planned demand, completion histories and restoration of active-exam elapsed extrema mintime/maxtime; mask IsLast for F4 only. Global source-event-order windows have common-day corroboration but do not establish true calendar cadence or complete intra-day synchronization. Visit-weighted MAE is a provisional comparison spec, not a settled cross-facility scoring decision. Current model/evaluation work and full panel must finish before final human review.

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-22):** `TBD -> Yes`, priority 3: the Kaggle file is a re-upload of Pianykh's MGH "Operational Predictions Dataset" (Harvard Dataverse, 2020, PLoS One paper), a patient wait-time and delay regression at four imaging facilities.
- Source: Harvard Dataverse doi:10.7910/DVN/X4SJWS, "Operational Predictions Dataset", Oleg Pianykh, deposited 2020-05-24, CC0, one file `WaitData.Published.tab`. The Kaggle copy (weirdolucifer, 2021-02-10) ships the same file name, `WaitData.Published.xlsx`, and the description: "operational features, captured in four different hospital facilities, processing walk-in (F4) or scheduled (F1, F2, F3) patients ... one line per each patient visit event", with timestamps "set to the fictitious future dates ... Only their relative timing was preserved". Data paper: Crowley, Guitron, Son & Pianykh 2020, PLoS One 15(6):e0233810: F1 MRI 15,494 rows, F2 ultrasound 36,154, F3 CT 30,173, F4 X-ray 69,469 (Nov 2017-Jul 2019); 84 candidate features (congestion, customer, resource, task, time); targets delay in minutes (F1-F3) and wait in minutes (F4). Its data availability statement points to the Dataverse.
- Use case: at a patient's arrival, the facility predicts the wait or delay. The earlier MGH work put the prediction on waiting-room displays and flagged patients who waited much longer than predicted (RSNA 2014; Curtis et al. 2018, JACR). Actor: the facility's operations staff. Moment: arrival (scheduled or walk-in). Fit: direct. Regime: temporal (relative order preserved), probably per facility.
- Siblings and duplicates: none for this source (`hospital_patient_data` is a different, unsourced Kaggle wait-time upload). The old reasons "no target" and "missing source" are refuted by the Dataverse and the paper, so those markers are dropped.
- Papers and pages: Crowley et al. 2020 (the data paper); Pianykh & Rosenthal 2015 (JACR, "Can We Predict Patient Wait Time?"); Curtis et al. 2018 (JACR, ML for wait times and delays, MGH).
- Metric: MAE in minutes. Crowley et al. Table 2 is "Predictive performance, measured by mean absolute error", while MSE drives their feature selection and they also give a ratio to an intercept-only model. MAE looks like the deliberate criterion; confirm under MET-5. Inputs: none beyond the rows; the facility is a column.
- Risks for /add-dataset: "captured at the time of patient arrivals and departure", so some features may be known only after the wait (LEAK; check each of the 84 against the arrival moment). Also one task or four: wait (F4) and delay (F1-F3) are different targets, so pick one facility or one target. The timestamps are fictitious, but their order holds for a time split.
- Priority: gap - (medical, regression, temporal: none thin), use case + (direct, named by the source), source + (Dataverse and paper), shape + (about 151k visits, 84 features, temporal), risk - (features recorded at departure).

A Kaggle 'Medical Facility Operational Data' dataset that is a single Excel sheet of mixed operational data with no defined task or target, per the curator's note. Without a clear predictive target it reads as a scientific-discovery / listing table rather than a benchmark task, and provenance is thin. It is tagged 2nd Tier and temporal. There is essentially no clear target to model, so it cannot be a Yes. A human would need to determine whether any meaningful operational target (e.g., occupancy, wait time) can be carved out, but as presented this is a No.

---

Unsure what the task/target could be, is one Excel sheet with a bunch of data.

CC (2026-10-26, Myunghwan): Proceed with add-dataset for Medical Facility Operational Data under the established curation procedure. This authorizes actual-data qualification and the required independent panel; final inclusion, build and repository integration remain separate. The existing Myunghwan reservation remains at triage; claim stage and scientific verdict are independent.

**Assessment (AI, 2026-10-26):** F4 provides a source-defined walk-in wait task (48,430 visits); the earlier unverified no-target/single-sheet description is contradicted by the actual workbook. The paper and mirror worksheet counts differ; equivalence remains unverified. Nine arrival-order tests exclude immature labels and cross-split exact copies. Full independent panel recommends Ship after changes: preserve source-defined F4, correct metadata now, resolve retained-history/estimator availability through source evidence or a supported narrowed definition, record the order-only cadence departure, and reconcile completed tuning before inclusion.. Source-described recent delay/wait fields differ from F4 Wait and their updater/estimator lineage is unresolved; REVIEW.md retains the decisions without calling this proven leakage. Mechanical checks have zero errors/warnings; raw copies0, final repeated states6, conflicting-feature rows134, exact cross-split copies0. Priority 3: gap -, use case + (arrival-time patient wait quote), source + (named primary study and pinned release, with cohort-equivalence gap), shape + (48,430 visits, temporal), risk - (unverified history and estimator provenance).

CC (2026-10-27 UTC, Myunghwan): Asked whether concerns/review/decisions remained, then said “yes, let’s check” after the agent proposed source verification and supported technical repair with affected checks. This authorizes the direct follow-up investigation; it is not an inclusion, build or commit decision.

**Follow-up assessment (AI, 2026-10-27 UTC):** Supersedes the earlier unverified mirror/history-availability findings. The primary author archive linked by the Nature Machine Intelligence companion article contains a workbook byte-identical to the checked Kaggle copy (SHA256 153cff36b4bbf2d972f415c00a786ae5d5e65557ae23b0379fd33efb69060f2e). Inspected Matlab code imports precomputed features and evaluates Wait models, rather than generating features. New diagnostics reconstruct elapsed queue state in 48,408/48,430 rows, each wait-window mean in 48,399/48,430, and signed in-progress begin-minus-schedule delays in all 7,684 linked singleton active exams. All nine recent-history fields stay fixed over 22,800 unchanged-completion-count transitions; the five-value vector shifts correctly in all 13,093 single-completion transitions. Signed completion-delay interpretation fits all 9,888 linked completions; exact end timestamps/updater and full Median5/last-K arithmetic/default conventions remain unverified. Expected-time values behave as elapsed plus a fixed patient component and fail realized-duration identities; exact fitting provenance remains unverified, with no measured future-label fitting. The 31 missing-calendar visits explain all mean residuals and contain all queue residuals; retain source visits/missingness with that diagnostic limitation. Keep the exact feature inventory, values, types and nine mature-label splits; correct semantics and primary provenance. Focused independent claim/column/mediator/editor review supplements the preserved full original panel. Remaining limitations: source feature estimator lineage, sorting-only calendar and unclaimed PLOS analytical-cohort equivalence. Only inclusion with the disclosed order-only cadence remains a curator judgment; no new factual approval gates.
