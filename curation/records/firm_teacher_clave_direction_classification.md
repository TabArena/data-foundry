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

**Assessment (AI, 2026-10-22):** the `No` rests on the TabArena workbook verdict ("Audio"); the AI agrees with `No`, on other grounds: the inputs are constructed rhythm patterns, not a sample from a real distribution, and no decision uses the prediction.
- Source: UCI 324, donated 2015-04-23 by M. Vurkac (dataset citation 2011), from his Portland State dissertation; 10,800 rows, "16 binary inputs and one 'four-bit' one-hot classification output"; each input is "the substantial presence (0, absence) of an onset (note start) in a certain time window" of one 4/4 bar in 16th notes; classes neutral, reverse clave, forward clave, incoherent, "determined through the music-theoretic/ethnomusicological portion of the my dissertation studies ... based on both double-blind listening tests and informal interviews with with four professional master-musicians".
- Use case: none found; the dissertation studies prestructured neural networks on a symbolic rhythm problem. No actor or decision (USE-1).
- Not audio: the rows are symbolic onset patterns, so `Wrong Domain / Source Modality` (SEL-12) does not fit well. The stronger grounds: the 10,800 rows are a selection of the 65,536 possible 16-bit patterns, labelled by the "firm teacher" (the codified expert rules; the "firm" against a fuzzy teacher reading is from the title, not confirmed in the text), so the data is handmade and the label close to deterministic (`AHDS`, SEL-16, PROV-3), which the record already carries.
- Siblings: none (grep clave). Metric: none found (UCI page; the ISSS paper on RA models of onset interactions compares modelling criteria, not a task metric).
- Recommendation: keep `No`; the curator has the call. Not checked: the dissertation's label section.

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
