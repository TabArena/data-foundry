---
unique_name: nz_springs
name: nz_springs
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
decision_markers:
- No Good Target  / Scientific Discovery
- TBD
tags:
- Many features
- AI-Filled (Verify)
collections:
- New (BeyondArena)
year: '2018'
domain: biology & life sciences
required_split:
- Random (IID)
problem_type: Regression
original_data_state: Database (or multiple to-be-joined tables)
source_row: 859
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

Sampling of New Zealand geothermal springs with metadata (temperature 13.9-100.6C, pH <1-9.7) plus a microbial OTU/16S count table (Nature Communications 2018, doi 10.1038/s41467-018-05020-y). A regression target such as temperature or pH from the OTU/metadata features is conceivable, but this is microbiome scientific-discovery data with very many (sparse OTU) features and an unclear, possibly small sample count. It leans toward scientific discovery rather than a representative tabular task. Suggest TBD -> 2nd Tier; a human must confirm the sample size after joining tables, the intended target, and whether OTU features make it representative.

---

Sampling of NZ geothermal springs with lots of metadata and a good range (13.9–100.6 °C and pH < 1–9.7); metadata source: via email from Matthew Stott; otu table source: from Matthew Stott

## Reference

10.1038/s41467-018-05020-y
