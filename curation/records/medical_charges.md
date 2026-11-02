---
unique_name: medical_charges
name: medical_charges
checked_by:
- AI (UNVERIFIED)
suggestion: 'No'
decision_markers:
- Data Quality Issue
- No Good Target / Scientific Discovery
tags:
- 2nd Tier / Scientific Discovery
- AI-Filled (Verify)
collections:
- TabArena Reject
- TabSTAR
domain: medical & healthcare
required_split:
- Grouped (NON-IID)
problem_type: Regression
original_data_state: One Table
source_links:
- https://www.openml.org/d/42130
- https://www.openml.org/d/44146
source_row: 824
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Assessment (AI, 2026-10-22):** the TabArena reject holds. The served copy has no predictive task worth benchmarking, and its main remaining feature is a part of the target.
- Source: OpenML 42130 (163,065 rows x 12) is the CMS Inpatient Utilization and Payment Public Use File for FY2011 (`Inpatient_Data_2011_CSV.zip`), "organized by hospital and Medicare Severity Diagnosis Related Group (MS-DRG)", target `average_total_payments`. OpenML 44146 is Grinsztajn's numeric cut with 3 features (OpenML API).
- Use case: none from the source. The PUF is a published statistical summary. Payments under IPPS follow the DRG weight and the hospital's rates, and "Average Medicare Payments" is a component of the total payment ("The Total Payment Amount includes the DRG amount, ...", CMS catalog), so the 44146 cut is close to an identity.
- Siblings and duplicates: `medicare_inpatient_cost` is the same CMS release series under its current name ("Medicare Inpatient Hospitals - by Provider and Service", data years 2013-2023 in the CMS catalog). The two records should be decided together; under PROV-6 only one cut could enter. External collections: Grinsztajn et al. 2022 benchmark, TabSTAR.
- Metric: none (the benchmark copies score R2 or RMSE by habit).
- Counter-check of the markers: the curator's notes (inference-time availability, string address features, grouping by provider) support `No Good Target / Scientific Discovery`. `Data Quality Issue` (damage that cannot be repaired) is not shown: the payment leak is removable by dropping columns, so that marker could go. No change to the verdict recommended.

OpenML medical-charges dataset (d/42130, 44146), used in Grinsztajn's benchmark in a trivially preprocessed numeric form. The curator notes most available features would not be available at inference time, many are string/address features needing special preprocessing, and the data is likely grouped by hospital/provider, with leakage risk. It is already in TabArena Reject. The combination of inference-time-unavailable features, leakage, and a listing/analytics rather than genuine predictive framing makes it a poor candidate. A human could revisit a leakage-cleaned version, but on current evidence this is a No.

---

CC: "grinsztajn uses trivial preprocessed version. Some features should not be used for prediction. Seems to be crawled data. Most available features would not be available at inference time in a real task. Remaining features mostly strings. Likely grouped data from hospitals and providers as well. Many string features like street names requiring special preprocessing."
