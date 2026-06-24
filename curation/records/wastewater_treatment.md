---
unique_name: wastewater_treatment
name: wastewater_treatment
checked_by:
- AI (UNVERIFIED)
suggestion: 'No'
decision_markers:
- No Good Target  / Scientific Discovery
- Not Representative
tags:
- Many features
- AI-Filled (Verify)
collections:
- New (BeyondArena)
year: '2019'
domain: biology & life sciences
problem_type: Other
original_data_state: Database (or multiple to-be-joined tables)
source_row: 864
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

A global microbiome study: 16S rRNA OTU tables from ~1,200 activated-sludge samples across 269 WWTPs in 23 countries (Nature Microbiology 10.1038/s41564-019-0426-5), joined with metadata. This is an OTU abundance table — extremely high-dimensional and sparse, used for ecological/scientific discovery rather than a standard real-world tabular predictive task, and not representative of typical tabular ML. There is no clear, defensible predictive target out of the box. It should be rejected as scientific-discovery / not representative, though a human could confirm no usable target (e.g., continent/process type) is salvageable.

---

A systematic global-sampling effort, analysing the 16S ribosomal RNA gene sequences from ~1,200 activated sludge samples taken from 269 WWTPs in 23 countries on 6 continents.; metadata source: SI Table 1; otu table source: http://gwmc.ou.edu/data-disclose.html

## Reference

10.1038/s41564-019-0426-5
