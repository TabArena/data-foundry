---
unique_name: inegi_gcim_vegetation_mapping_challenge
name: inegi-gcim-vegetation-mapping-challenge
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
decision_markers:
- No Good Target (yet)
- Data Quality Issue
tags:
- AI-Filled (Verify)
collections:
- New (BeyondArena)
original_source: Zindi
domain: environmental science & climate
required_split:
- '?'
problem_type: Multiclass Classification
original_data_state: One Table
source_links:
- https://zindi.africa/competitions/inegi-gcim-vegetation-mapping-challenge/data
source_row: 885
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

The stated task is a label-cleaning / weak-supervision meta-task: build a model to identify outliers (wrong/suspicious labels) and suggest more plausible labels for vegetation mapping, rather than a clean predictive classification with a fixed target. That framing (data cleaning / label correction) does not map to a standard IID predictive task and risks a leaky/ill-defined target, and vegetation mapping can carry geospatial/remote-sensing characteristics. It could be repurposed into a straightforward land-cover classification if a trustworthy label column exists. A human must verify whether a clean categorical target and tabular features (not raster/remote-sensing) are available before considering it.

---

propose and develop a robust and accurate machine learning model that can help to clean and improve training data, either identifying outliers (wrong or suspicious labels), or even suggesting a more plausible label in the given test data
