---
unique_name: medicare_inpatient_cost
name: Medicare Inpatient Cost
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 2
decision_markers:
- No Good Target (yet)
tags:
- 2nd Tier / Scientific Discovery
- AI-Filled (Verify)
collections:
- New (BeyondArena)
original_source: GOV Website
domain: medical & healthcare
required_split:
- Grouped (NON-IID)
problem_type: Regression
original_data_state: One Table
source_links:
- https://data.cms.gov/provider-summary-by-type-of-service/medicare-inpatient-hospitals/medicare-inpatient-hospitals-by-provider-and-service
source_row: 829
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-22):** `TBD -> 2nd Tier`, priority 2: a CMS statistical summary (hospital x DRG averages) with no task of its own, from the same release series as the rejected `medical_charges`.
- Source: CMS, "Medicare Inpatient Hospitals - by Provider and Service", annual data years 2013-2023 in the CMS catalog (data.cms.gov/data.json). The release "provides information on inpatient discharges for Original Medicare Part A beneficiaries by IPPS hospitals ... organized by hospital and Medicare Severity Diagnosis Related Group (DRG)", and "The Total Payment Amount includes the DRG amount, claim per diem amount, ... and diagnosis related group outlier amount". One row per hospital x DRG with discharges, average covered charges, average total payment and average Medicare payment, plus hospital name, address and location.
- Use case: none stated. CMS publishes the table for transparency. A target such as the average payment follows the IPPS formula (DRG weight x hospital rates), and the other payment columns are components of it. Fit: none from the source. Regime: grouped by hospital, or temporal across data years.
- Siblings and duplicates: `medical_charges` (OpenML 42130/44146) is the FY2011 file of the same series ("Inpatient Utilization and Payment Public Use File"). It is `No` with TabArena Reject and the curator's note that most features are not known at inference time. Under PROV-6 these are cuts of one dataset, so decide them together. External collections: Grinsztajn et al. 2022 and TabSTAR via `medical_charges`.
- Papers and pages: the CMS catalog and data dictionary; no paper defines a predictive task on it.
- Metric: none found (CMS catalog, data dictionary, the OpenML copies), so the fallback.
- Risks for /add-dataset: leakage among the payment and charge columns (CC: "several things being an indicator of each other"); a near-deterministic target under IPPS (SEL-5 to weigh); addresses as strings; aggregated rows, not patients. `Data Quality Issue` (irreparable damage) is dropped: dropping the columns removes the leak. `No Good Target (yet)` stays.
- Priority: gap + (Grouped regime thin), use case - (none), source + (CMS documentation), shape - (after dropping the leaking columns only hospital, DRG, discharges and charges remain), risk - (deterministic payment rule, leak).

CMS Medicare inpatient hospitals summary by provider and service, a real government data release. The curator notes it is essentially a listing of aggregated data without a real predictive task, and that many columns (e.g., payment amounts) are mutually indicative and would leak the target. A regression target (e.g., average cost/payment) could in principle be defined, but it would need careful leakage removal and is a weak benchmark signal. This is borderline: not a clean Yes, not an outright No, so TBD -> 2nd Tier. A human must define a leakage-free target, decide on grouping by provider, and assess size and signal.

---

CC: "Has some cool data but is just a listing of data without a real task. So it might not be useful for a benchmark or tell us much. It could still be used but maybe is not a great signal.

But make sure to remove all the leakage from the columns due to several things being an indicator of each other (like payment)"
