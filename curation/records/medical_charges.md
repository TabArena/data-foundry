---
unique_name: medical_charges
name: medical_charges
checked_by:
- AI (UNVERIFIED)
suggestion: 'No'
decision_markers:
- Data Quality Issue
- No Good Target  / Scientific Discovery
tags:
- 2nd Tier / Scientfic Discovery
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

OpenML medical-charges dataset (d/42130, 44146), used in Grinsztajn's benchmark in a trivially preprocessed numeric form. The curator notes most available features would not be available at inference time, many are string/address features needing special preprocessing, and the data is likely grouped by hospital/provider, with leakage risk. It is already in TabArena Reject. The combination of inference-time-unavailable features, leakage, and a listing/analytics rather than genuine predictive framing makes it a poor candidate. A human could revisit a leakage-cleaned version, but on current evidence this is a No.

---

CC: "grinsztajn uses trivial preprocessed version. Some features should not be used for prediction. Seems to be crawled data. Most available features would not be available at inference time in a real task. Remaining features mostly strings. Likely grouped data from hospitals and providers as well. Many string features like street names requiring special preprocessing."
