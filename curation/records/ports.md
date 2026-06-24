---
unique_name: ports
name: ports
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
domain: biology & life sciences
required_split:
- Random (IID)
problem_type: TBD
original_data_state: Database (or multiple to-be-joined tables)
source_row: 860
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

16S rRNA microbiome data from ports with separate OTU count and metadata tables (refs mSphere/AEM 2019). A predictive target (e.g. port/region or an environmental variable from OTU features) might be constructed, but this is microbiome scientific-discovery data with very many sparse OTU features and likely a modest sample count. It is borderline for representative tabular ML. Suggest TBD -> 2nd Tier; a human must define a meaningful target, join the count and metadata tables, and check sample size and feature representativeness.

---

16S rRNA sequences from ports; metadata source: https://github.com/rghannam/portmicrobes/tree/master/data/metadata; otu table source:https://github.com/rghannam/portmicrobes/tree/master/data/counts_taxonomy

## Reference

10.1128/mSphere.00481-19 ; 10.1128/AEM.01804-19
