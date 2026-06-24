---
unique_name: airlines_depdelay_10m
name: Airlines_DepDelay_10M
checked_by:
- AI (UNVERIFIED)
suggestion: 'Yes'
tags:
- Non-IID (Temporal)
- AI-Filled (Verify)
original_source: GOV Website
year: '2013'
domain: Other
required_split:
- Temporal (NON-IID)
problem_type: Regression
original_data_state: One Table
source_links:
- https://www.openml.org/search?type=data&id=42728
- https://www.transtats.bts.gov/
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

The well-known OpenML 'Airlines_DepDelay_10M' dataset from US BTS flight records, predicting departure delay (regression) over ~10M rows. This is a large, genuine real-world tabular task already imported from the TabArena workbook with a verdict of 'Temporal Tabular' and multiple curators (Lennart, Andrej) agreeing a temporal split is required. It is clearly representative tabular ML with a meaningful target. A human should confirm it is not an unwanted duplicate of the smaller 'airlines' dataset and that the temporal split is correctly applied.

---

Imported from the TabArena curation workbook.

TabArena curation verdict: Temporal Tabular.

Might be an extended version of the airlines dataset (need to verify). For sure requires temporal split; might be a newer version as the data is younger

Potential issue: temporal

Lennart: temporal

Andrej: Temporal split
