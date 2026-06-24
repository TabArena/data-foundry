---
unique_name: medicare_inpatient_cost
name: Medicare Inpatient Cost
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
decision_markers:
- No Good Target (yet)
- Data Quality Issue
tags:
- 2nd Tier / Scientfic Discovery
- AI-Filled (Verify)
collections:
- New (BeyondArena)
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

CMS Medicare inpatient hospitals summary by provider and service, a real government data release. The curator notes it is essentially a listing of aggregated data without a real predictive task, and that many columns (e.g., payment amounts) are mutually indicative and would leak the target. A regression target (e.g., average cost/payment) could in principle be defined, but it would need careful leakage removal and is a weak benchmark signal. This is borderline: not a clean Yes, not an outright No, so TBD -> 2nd Tier. A human must define a leakage-free target, decide on grouping by provider, and assess size and signal.

---

CC: "Has some cool data but is just a listing of data without a real task. So it might not be useful for a benchmark or tell us much. It could still be used but maybe is not a great signal.

But make sure to remove all the leakage from the columns due to several things being an indicator of each other (like payment)"
