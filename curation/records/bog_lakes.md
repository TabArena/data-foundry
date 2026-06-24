---
unique_name: bog_lakes
name: bog_lakes
checked_by:
- AI (UNVERIFIED)
suggestion: 'No'
decision_markers:
- No Good Target  / Scientific Discovery
- Not Representative
- Time-series (Regression)
tags:
- Many features
- AI-Filled (Verify)
collections:
- New (BeyondArena)
domain: biology & life sciences
problem_type: Other
original_data_state: Database (or multiple to-be-joined tables)
source_row: 858
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

Multiyear 16S rRNA microbiome amplicon (OTU) sequencing of eight bog lakes near Minocqua, Wisconsin, joined from an OTU table and a metadata table. This is microbial-ecology scientific-discovery data: an OTU table is an extremely high-dimensional, sparse compositional matrix with no canonical supervised predictive target, and the multiyear sampling makes it a time series. It does not map to a representative real-world tabular classification/regression task. A human could confirm there is no clear predictive target, but on the available description this should be rejected.

---

Eight bog lakes, multiyear time series of 16s sequences near Minocqua, northern Wisconsin; metadata source: R package "OTUtable", data(metadata); otu table source: https://github.com/McMahonLab/North_Temperate_Lakes-Microbial_Observatory

## Reference

10.1128/mSphere.00169-17
