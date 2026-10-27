---
unique_name: kdd_internet_usage
name: kdd_internet_usage
checked_by:
- AI (UNVERIFIED)
suggestion: 'No'
decision_markers:
- Duplicate
- No Good Target / Scientific Discovery
tags:
- 2nd Tier / Scientific Discovery
- AI-Filled (Verify)
collections:
- TabArena Reject
- TabSTAR
year: '1997'
domain: social science
required_split:
- '?'
problem_type: Multiclass Classification
original_data_state: One Table
source_links:
- https://www.openml.org/d/981
- https://www.openml.org/search?type=data&id=372&sort=runs&status=active
- https://sites.cc.gatech.edu/gvu/user_surveys/survey-1997-10/datasets/
source_row: 801
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-22):** `No` (`Duplicate`, PROV-6; `No Good Target / Scientific Discovery`, SEL-3): a binarized cut of the GVU survey table that `internet_usage` already records, with a target the mirror invented.
- Source: GVU Center, Georgia Tech, WWW User Survey of 10 October to 16 November 1997, "general demographics" subset, donated to UCI by Di Cook in 1999 (https://doi.org/10.24432/C5Q60G). OpenML 981 (2014): "Binarized version of the original data set (see version 1). The multi-class target feature is converted to a two-class nominal target feature by re-labeling the majority class as positive ('P') and all others as negative ('N'). Originally converted by Quan Sun." 10,108 rows x 69 columns, target `Who_Pays_for_Access_Work` (7,393 / 2,715); OpenML 372 `internet_usage` holds the same 10,108 respondents with 72 columns.
- Use case: none: the UCI abstract is "This data contains general demographic information on internet users in 1997"; "This data comes from a survey"; its past usage is the ASA 1999 Data Exposition (graphics), no prediction.
- Siblings and duplicates: `internet_usage` (Lennart: `TBD -> 2nd Tier`, `No Good Target (yet)`, "Maybe a duplicate. Unclear task") links UCI C5Q60G and OpenML 372, the same survey file; this record adds only a relabelled column. External collections: TabSTAR (per the record), OpenML binarized suite.
- Metric: none.
- The curator's workbook note: "Might be survey data. Might actually be an interpretability task. Also might be clustered data".
- Reject check (AI, 2026-10-22): stands. OpenML 981 says of itself: "Binarized version of the original data set (see version 1) ... re-labeling the majority class as positive" (https://www.openml.org/d/981). Version 1 is OpenML 372 internet_usage (target Actual_Time), the same GVU 1997 survey already recorded as internet_usage. A swapped target on the same cohort is the PROV-6 duplicate case by name, and the invented majority-vs-rest label is no observed outcome (SEL-3).

KDD Internet Usage (GVU 1997 web survey, OpenML d/981 and d/372) is questionnaire/survey data already tagged 2nd Tier / Scientific Discovery and in TabArena Reject, with curator concerns about it being survey/interpretability data, possibly clustered by user, and containing sensitive features like race. It is a known tabular multiclass dataset (used by TabSTAR), but the survey nature, 1997 vintage, and ethical/leakage caveats keep it at 2nd Tier rather than a clean Yes. A human must verify the chosen target, whether per-user 'who' features cause grouping/leakage, and the ethics of sensitive attributes.

---

CC: "Multiclass. Might be survey data. Might actually be an interpretability task. Also might be clustered data; unique users ("who" features); some other questionable features like race"

## Reference

[1]Graphics, Visualization, & Usability Center College of Computing Geogia Institute of Technology Atlanta, GA Donor [2]Dr Di Cook, Department of Statistics, Iowa State University Date Donated: June 30, 1999; survey conducted by the Graphics and Visualization Unit at Georgia Tech October 10 to November 16, 1997.
