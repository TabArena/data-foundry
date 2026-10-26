---
unique_name: era
name: ERA
checked_by:
- AI (UNVERIFIED)
suggestion: 'No'
decision_markers:
- No Good Target / Scientific Discovery
tags:
- 2nd Tier / Scientific Discovery
- Non-IID (Grouped)
- AI-Filled (Verify)
collections:
- TabArena Reject
domain: social science
required_split:
- Grouped (NON-IID)
original_data_state: One Table
source_links:
- https://www.openml.org/d/1030
- From WEKA https://gitlab.univ-lorraine.fr/roussana5/weka/-/tree/master/weka/samples/datasets-arie_ben_david?
source_row: 844
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-22):** `No` (`No Good Target / Scientific Discovery`, SEL-3): a decision-making experiment run in an MBA course to find which candidate qualities matter; the label is a student's subjective tendency to accept a candidate, which no hiring decision acts on as a prediction target.
- Source: OpenML 1030 "ERA" (Employee Rejection\Acceptance), donated by Arie Ben-David (Holon Academic Institute of Technology), owner Yoav Ganzah (Tel Aviv University), in Ben-David's WEKA ordinal sets with ESL, LEV and SWD; OpenML cites Dobrska, Wang and Blackburn 2012 (an ordinal-regression method paper). As published: 1,000 rows, 4 ordinal inputs ("past experience, verbal skills, etc."), ordinal output `out1`, no missing values; no year of collection.
- Use case: none: "The ERA data set was originally gathered during an academic decision-making experiment aiming at determining which are the most important qualities of candidates for a certain type of jobs. Unlike the ESL data set (enclosed) which was collected from expert recruiters, this data set was collected during a MBA academic course" (OpenML description); a study of the raters, not a decision; the CC line adds that the judges likely repeat across rows (an unknown grouping).
- Siblings and duplicates: `esl` (the same donor's expert-recruiter set; Lennart: `No`, `Trivial`, `Missing source information`); no copy found. External collections: TabArena Reject (the TabArena v0.1 curation).
- Metric: none found (OpenML; the cited paper evaluates an ordinal method on many sets).
- The old `AHDS` marker is dropped: nothing in the source says the candidate profiles were generated, though they likely were hypothetical vignettes (not checked).
- Reject check (AI, 2026-10-22): stands. The source states a discovery purpose and a non-expert label (OpenML 1030, https://www.openml.org/d/1030): 'gathered during an academic decision-making experiment aiming at determining which are the most important qualities of candidates ... Unlike the ESL data set ... collected from expert recruiters, this data set was collected during a MBA academic course'. That fails SEL-3's 'observed outcome or an expert annotation'. The curator's CC line on the record points the same way.

OpenML 'ERA' (Employee Rejection/Acceptance) is a small ordinal-classification dataset of human judgements collected during an MBA course, originating from Arie Ben-David's WEKA sample sets. The comment notes it is grouped judgement data where it is unclear whether judges recur, making it a subjective scientific-discovery / human-rating exercise rather than a real-world predictive task, and it is already a TabArena Reject. Excluded on no-good-target / not-representative grounds; a human need only confirm the grouping ambiguity and lack of a genuine predictive target.

---

CC: "academic decision-making experiment was collected during MBA course, again grouped judgement data where it is unclear in how far judges appear multiple times"
