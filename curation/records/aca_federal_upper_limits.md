---
unique_name: aca_federal_upper_limits
name: ACA Federal Upper Limits
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
year: '2016'
domain: medical & healthcare
problem_type: Regression
original_data_state: One Table
source_links:
- https://www.medicaid.gov/medicaid/prescription-drugs/federal-upper-limit
- https://huggingface.co/datasets/inria-soda/STRABLE-benchmark/tree/main/aca-federal-upper-limits-wide
- https://arxiv.org/abs/2605.12292
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> 2nd Tier`, priority 2: a monthly CMS price list. CMS sets each FUL by formula from confidential manufacturer prices, so predicting it from the drug's descriptors serves no decision we could name.
- Source: CMS, Medicaid.gov "Federal Upper Limits" (https://www.medicaid.gov/medicaid/prescription-drugs/federal-upper-limit): the FUL is set at "no less than 175 percent of the weighted average" (by utilization) of the most recent monthly AMPs of equivalent multiple source drugs, and at the retail pharmacies' average acquisition cost (NADAC) when that is higher; the final ACA FUL took effect on 1 April 2016 and is updated monthly; the AMP values are confidential. As published in STRABLE (aca-federal-upper-limits-06272025.csv, the June 2025 file; parquet previewed 2026-10-31): 1,976 rows x 13 columns, one row per product group (STRABLE kept the last row per `Product Group`); target `ACA FUL` on a log-type scale; inputs ingredient, strength, dosage form, route, MDR unit type, package size, NDC, A-rated, the "Multiplier Greater Than 175 Percent" flag, year and month (1,583 rows from 2025). STRABLE dropped `Weighted Average of AMPs` as a leak, the formula's input (SEL-5).
- Use case: none named. CMS computes the FUL and publishes it, and states apply it within 30 days; a pharmacy or a state agency estimating a product group's FUL before CMS lists it would be a stand-in. Fit none as published (approximate at best); regime IID over product groups in one snapshot, or temporal by effective month.
- Siblings and duplicates: `medicaid_first_time_nadac_rates` (CMS NADAC, the acquisition-cost survey the FUL falls back on; STRABLE); the other Medicaid tables of STRABLE (`medicaid_financial_management`, `medicaid_managed_care_enrollment`, `medicaid_mlr_summary_reports`, `medicaid_child_adult_core_set_quality`) share the publisher, not the task; `drug_directory` (FDA NDC listing, `TBD -> 2nd Tier`, "not a real predictive task") is the closest precedent. External collections: STRABLE (Blayer et al. 2026, arXiv 2605.12292, App. C.2), "ACA Federal Upper Limits": "Price limits for multi-source drugs under the Medicaid program. The task is to predict the federal upper price limit."
- Better data: a candidate of the benchmark STRABLE; no further search this round.
- Papers and pages: the CMS page and final rule CMS-2345-FC; STRABLE and its script `preprocess_medicaid-aca-federal-upper-limits_wide.py` (github.com/soda-inria/strable); papers that used the data: not searched (the session's web search budget ran out).
- Metric: none found (the CMS page publishes a price list, no task); STRABLE scores R2 for regression and AUROC for classification over all its tables (App. D.1), a benchmark's habit, not the source's. So the fallback, `rmse` on the dollar scale with a log transform (MET-3, MET-8); inputs none.
- Risks for /add-dataset: the target is a formula output on confidential AMPs: check how far ingredient and strength alone go (TP-4); the multiplier flag is part of the formula (SEL-5, LEAK); `NDC` and `Product Group` are ids; STRABLE kept one row per product group, the last after sorting by year (the raw file can list several NDCs per group), so the unit (group or NDC) is a choice for the definition.
- Priority: gap 0 (medical & healthcare, regression not thin), use case 0 (none named), source + (CMS page with the formula), shape + (1,976 product groups, 11 inputs, mixed), risk - (no decision fits as published).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the benchmark STRABLE (https://arxiv.org/abs/2605.12292).
- as published: 1,976 rows x 13 columns incl. target (STRABLE parquet); target: ACA FUL.
- Why: Predict the Medicaid ACA federal upper limit (FUL) price of a multi-source drug product from its product descriptors
- Notes: Raw file aca-federal-upper-limits-06272025.csv (CMS/Medicaid, June 2025). Target log-type transformed by STRABLE's skewness protocol. FUL is set by a CMS formula from AMP data, so the task may be close to deterministic.
