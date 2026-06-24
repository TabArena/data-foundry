---
unique_name: eu_lakes_allfeatures
name: eu_lakes_allfeatures
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
decision_markers:
- Too Small
- Not Representative
tags:
- Tiny Data
- Many features
- AI-Filled (Verify)
collections:
- New (BeyondArena)
year: '2012'
domain: biology & life sciences
required_split:
- '?'
problem_type: TBD
original_data_state: One Table
source_row: 874
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

A 2012 sampling of European lakes with a microbiome OTU (operational taxonomic unit) abundance table plus metadata. It is already tagged 'Tiny Data' and 'Many features', i.e. a wide, low-sample-count omics matrix that is poorly representative of typical tabular ML and likely too small for stable CV. The intended supervised target is unclear from the record (some lake/sample property to be regressed or classified). A human must identify a concrete target, confirm the (small) sample count and feature count, and judge whether the high-dimensional microbiome data is suitable at all.

---

Sampling of European lakes in August 2012; metadata source: dx.doi.org/10.1111/mec.15872; otu table source: from J. Boenigk

## Reference

10.3389/fmicb.2020.00154
