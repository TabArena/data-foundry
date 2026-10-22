---
unique_name: national_longitudinal_survey_binary
name: national-longitudinal-survey-binary
checked_by:
- AI (UNVERIFIED)
suggestion: 'No'
decision_markers:
- No Good Target  / Scientific Discovery
- Duplicate
tags:
- 2nd Tier / Scientfic Discovery
- AI-Filled (Verify)
collections:
- TabArena Reject
year: '2022'
domain: social science
required_split:
- Random (IID)
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://www.nlsinfo.org/
- https://www.openml.org/d/43892
source_row: 821
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Assessment (AI, 2026-10-22):** agree with `No` (the CC: "Survey data. Not a real predictive task."); recommend replacing `Duplicate` by nothing or by a note, since no other copy is among the records; the curator has the call.
- Source: U.S. Bureau of Labor Statistics, National Longitudinal Survey of Youth 1979 (https://www.nlsinfo.org/), as cut by the R package fairml (`national.longitudinal.survey`: 4,908 rows, 18 variables; "The data was preprocessed differently from Komiyama et al. (2018) ... In that paper, `income90` is the response, and `gender` and `age` are the sensitive attributes", rdrr.io fairml manual); OpenML 43892 (2022-05-30) re-uploads it binarized: 4,908 x 17, target `income96gt17`, description "Whether income90 is greater than 1.7" (10,000 USD units), with `income96` kept as a feature and `income90`, `income06` dropped.
- Original task (SEL-8): Komiyama et al. 2018 (ICML), fair regression with sensitive attributes: a benchmark for fairness-constrained methods on survey answers, not a decision anyone makes with the prediction (SEL-3, USE-1).
- Use case: none from the source. A steelman: the 1989-1990 answers (`afqt89`, `grade90`, `jobsnum90`, `typejob90`) precede 1996 income, so an income-in-six-years prediction exists in principle, but no actor acts on it, and `age`, `height`, `weight`, `illegalact` are survey answers of the same panel.
- Leak: if the target is income96 > 1.7, the feature `income96` decides it (fixable by dropping, LEAK rules); the OpenML text names income90, the column name income96: the OpenML upload contradicts itself.
- Markers: `No Good Target  / Scientific Discovery` fits (SEL-3); `Duplicate` has no other record behind it (OpenML 43892 is the only copy we hold; it is a cut of fairml's cut of NLSY79, PROV-5 would apply only against another record).
- Metric: none for a classification (the paper's response is continuous income); the fallback.

Re-upload of the NLSY data via the R fairml package with a binarized target and the original continuous target left in the data, framed as an Adult-like survey task. The curator (CC) judged it 'not a real predictive task' and it is already in the TabArena Reject collection. It is essentially survey/scientific-discovery data with a constructed target plus a leakage concern from the retained original target. Suggest No. A human should confirm the leakage and that this duplicates the well-known fairml/NLSY upload.

---

CC: "data from R package fairml, binarized target, original target still in the data. Task similar to adult dataset. Survey data. Not a real predictive task."
