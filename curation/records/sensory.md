---
unique_name: sensory
name: sensory
checked_by:
- AI (UNVERIFIED)
suggestion: 'No'
decision_markers:
- AHDS (Artifical/Handmade/Deterministic/Simulated)
- No Good Target  / Scientific Discovery
tags:
- 2nd Tier / Scientfic Discovery
- Non-IID (Grouped)
- AI-Filled (Verify)
collections:
- TabArena Reject
- TabSTAR
year: '1996'
domain: Other
required_split:
- Grouped (NON-IID)
original_data_state: One Table
source_links:
- https://www.openml.org/d/546
source_row: 843
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Assessment (AI, 2026-10-22):** the curator's `No` (CC line, TabArena Reject) stands on SEL-3; one counter-argument on a marker: the data is a real experiment, not a simulation.
- Source: OpenML 546 (uploaded 2014), from Brien and Payne (1996), "Tiers, structure formulae and the analysis of complicated experiments"; 576 rows x 12 columns: 11 design factors (Occasion, Judges, Interval, Sittings, Position, Squares, Rows, Columns, Halfplot, Trellis, Method) and the response `Score`.
- Use case: none. OpenML: a split-plot vineyard trial "to investigate the differences between 4 types of trellising and 2 methods of pruning", the 24 wines scored by 6 judges in a latinized design. The question is the treatment effects (an ANOVA of a designed experiment), a discovery question; predicting a judge's score from the layout of the design simulates no decision (SEL-3, USE-2: `No Good Target  / Scientific Discovery`). Regime would be grouped (judges, plots).
- Siblings and duplicates: none (`wine_quality` is other data). External collections: TabSTAR.
- Metric: none (an ANOVA paper), so the fallback had it shipped.
- **Counter-argument (AI):** `AHDS (Artifical/Handmade/Deterministic/Simulated)` (SEL-16, PROV-3) does not fit the source's words: the scores are real tastings of real wines from a field trial; only the allocation is designed. The verdict rests on SEL-3 alone; suggest dropping the AHDS marker. The curator has the call.


OpenML 'sensory' dataset (Brien & Payne 1996) from a designed wine-tasting experiment recording control variables and tier/grouping structure, already tagged as a TabArena Reject and 2nd-Tier/Scientific-Discovery. The curator notes it appears to be a constructed/simulated experimental design rather than a genuine predictive task with a meaningful target. It is excluded as artificial/designed-experiment scientific-discovery data without a real predictive target.

---

CC: "Not sure if this is a real predictive task.. Apparently only control variables of a wine tasting experiment are given; sounds like a simulation; includes groups and splits of the data. Very weird task and constructed experiment, I would almost say that this is a simulation!"

## Reference

Brien, C.J. and Payne, R.W. (1996) Tiers
