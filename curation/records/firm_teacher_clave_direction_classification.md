---
unique_name: firm_teacher_clave_direction_classification
name: Firm-Teacher_Clave-Direction_Classification
checked_by:
- AI (UNVERIFIED)
suggestion: 'No'
decision_markers:
- AHDS (Artifical/Handmade/Deterministic/Simulated)
- No Good Target (yet)
tags:
- AI-Filled (Verify)
original_source: UCI
year: '2015'
domain: Other
required_split:
- '?'
problem_type: Multiclass Classification
original_data_state: One Table
source_links:
- https://doi.org/10.24432/C5GC9F
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

UCI 'Firm-Teacher Clave-Direction Classification' is a multi-target dataset of musical clave/rhythm patterns where the labels are assigned from human/expert musical rules rather than measured outcomes, making it a deterministic, handmade rule-encoding task. The TabArena workbook flagged it as an audio-domain problem and two reviewers (Lennart, Andrej) could not tell whether it is a real predictive task, with a possible temporal aspect. Because the targets are rule-derived/deterministic rather than a genuine real-world predictive signal, it is excluded as AHDS; a human could verify the label-generation process if reconsidering.

---

Imported from the TabArena curation workbook.

TabArena curation verdict: Audio.

Multi-target task; sounds like an aduio domain problem but I really have no idea what this task might be. Labels based on human knowledge

Potential issue: audio task, temporal??

Lennart: I cannot tell if this is a real task or not

Andrej: Might require temporal split, need to look at the data to understand

## Reference

10.24432/C5GC9F
