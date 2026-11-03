---
unique_name: hrsa_uds_hypertension_control
name: Hypertension Control
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 2
decision_markers:
- No Good Target (yet)
tags:
- AI-Filled (Verify)
collections:
- STRABLE
original_source: GOV Website
domain: medical & healthcare
source_links:
- https://data.hrsa.gov/data/reports
- https://huggingface.co/datasets/inria-soda/STRABLE-benchmark/tree/main/hypertension-control-wide
- https://arxiv.org/abs/2605.12292
- https://data.hrsa.gov/topics/health-centers/hypertension-control
- https://data.hrsa.gov/DataDownload/StaticDocuments/Hypertension_NHCI_UDS_2019-2024.xlsx
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> 2nd Tier`, priority 2: UDS hypertension control rates of HRSA-funded health centres (2019-2024), which STRABLE cut to the 2023 rate, binarised at its own threshold of about 61.2% and joined to grant and address fields; the source tracks the Million Hearts goal of 80%, and the natural task, a centre's next rate given its history, is a panel close to forecasting.
- Source: HRSA Bureau of Primary Health Care, Hypertension Control dashboard (https://data.hrsa.gov/topics/health-centers/hypertension-control): "View health centers that met or exceeded the Million Hearts Hypertension Control Champion Challenge goal of 80% control"; file `Hypertension_NHCI_UDS_2019-2024.xlsx` (one sheet per year, 1,359 to 1,385 centres each; grant number, name, NHCI awardee, PCMH, state, estimated share controlled; previewed, 327 KB). As used by STRABLE (HF parquet, previewed): 1,363 rows x 38 columns, the 2023 sheet joined to HRSA award fields (financial assistance, address, project period, congressional district, senators, DUNS and UEI, CCN), `PCMH` dropped; target 1 for 911 centres. Matched to the 2023 rates, the positives start at 0.6123 and the negatives end at 0.6119: a threshold HRSA does not use (4.5% of centres reached 80% in 2023).
- Use case: HRSA or a primary care association picks centres for quality-improvement help (the National Hypertension Control Initiative) before the year's UDS report; the source names the goal, not a prediction. Fit approximate; regime temporal (yearly reports per centre) once the history is used, which makes it a panel (TP-10).
- Siblings and duplicates: no duplicate (grep for hypertension, UDS); `hrsa_bhw_awarded_grants` (the award fields STRABLE joined). External collections: STRABLE (Table C.4 row 58: "Clinical performance data on hypertension management. The task is to predict patient blood pressure control percentage.", while its `config.json` is binary).
- Better data: a candidate of the benchmark STRABLE; no further search for this run's finds.
- Papers and pages: the dashboard and its About PDF; the AHRQ Data Spotlight on hypertension control in health centres (linked from the dashboard); STRABLE, Blayer et al., arXiv 2605.12292 (v2, 2026-10-19).
- Metric: none found for a prediction (HRSA reports rates against the 80% goal; STRABLE's AUROC, App. D.1, is benchmark-wide, MET-5), so the fallback `rmse` on the rate, or `roc_auc` if the curator frames HRSA's 80% goal; never STRABLE's 61.2% (MET-7: no invented threshold); inputs none.
- Risks for /add-dataset: re-target to the rate or HRSA's goal (USE-5); with prior years as features the centre's own profile may beat any model (TP-10, SEL-11), without them address and grant fields say little about care quality; about 1,360 centres a year is thin for temporal windows (SPLIT-14); patient-mix features would need a join with the UDS awardee data.
- Priority: gap 0, use case 0, source + (HRSA dashboard documentation), shape + (about 1,360 centres x 6 years), risk - (invented threshold, forecasting-like panel).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the benchmark STRABLE (https://arxiv.org/abs/2605.12292).
- as published: 1,363 rows x 38 columns incl. target (STRABLE parquet); target: Estimated Percentage of Patients with Controlled Blood Pressure.
- Why: Predict whether a health center reaches the controlled-blood-pressure goal (61.2%)
- Notes: Raw file 'Hypertension NHCI UDS 2019-2023.xlsx' joined with HRSA award data. Binary target is a STRABLE threshold on the estimated percentage.
