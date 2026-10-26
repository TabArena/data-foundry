---
unique_name: labor
name: labor
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 2
decision_markers:
- Too Small
tags:
- AI-Filled (Verify)
original_source: Github
year: '?'
domain: social science
required_split:
- '?'
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://github.com/EpistasisLab/pmlb/blob/master/datasets/labor/metadata.yaml
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Assessment (AI, 2026-10-22):** the workbook verdict of Lennart and Andrej ("too small") stands, and the source adds a second reason; recommend `No` with `Too Small` and `AHDS (Artifical/Handmade/Deterministic/Simulated)`; the curator has the call. Priority 2 by the factors while the field stays `TBD -> 2nd Tier`.
- Source: UCI Labor Relations, donated by Stan Matwin, November 1988 ("Final settlements in labor negotitions in Canadian industry", Collective Bargaining Review, Labour Canada); OpenML 4, PMLB `labor` are copies. As published: 57 contracts x 16 attributes, 37 good / 20 bad.
- Use case: none named: "testing concept learning software ... to learn the description of an acceptable and unacceptable contract"; regime IID.
- Siblings and duplicates: none in the records (labour_inspection_compliance is another task). External collections: PMLB, OpenML.
- Papers and pages: Bergadano, Matwin, Michalski, Zhang 1988 (EWSL, ISMIS).
- Metric: none deliberate (concept-learning papers), so the fallback `roc_auc` (MET-1, MET-8).
- Against keeping it: 20 bad contracts in all, 4 per test fold under 5-fold CV (TP-5; parkinsons retired at 2-3 per fold, musk kept at 13); and the UCI notes say "The unacceptable contracts were either obtained by interviewing experts, or by inventing near misses", so part of the negative class is handmade (SEL-16, PROV-3).
- Priority: gap + (social science thin), use case -, source + (UCI notes), shape - (57 rows), risk - (invented negatives).

The PMLB 'labor' dataset (labor-negotiation contract acceptability) has only 57 rows, which two TabArena curators (Lennart, Andrej) already flagged as too small, especially under 3-fold CV. While it is a genuine real-world tabular classification, it is far below any usable size threshold for the benchmark. Recommend No on size grounds; no further verification needed beyond confirming the 57-row count.

**Update (policy):** "Too Small" is no longer a rejection reason — dataset size is assessed *after* Data Foundry processing. Re-classified off No to TBD -> 2nd Tier pending that post-DF size check.

---

Imported from the TabArena curation workbook.

TabArena curation verdict: Tiny data.

57 samples,  too small with 3-fold CV.

Lennart: too small

Andrej: too small
