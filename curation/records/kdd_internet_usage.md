---
unique_name: kdd_internet_usage
name: kdd_internet_usage
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
decision_markers:
- No Good Target  / Scientific Discovery
- Outdated
tags:
- 2nd Tier / Scientfic Discovery
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

KDD Internet Usage (GVU 1997 web survey, OpenML d/981 and d/372) is questionnaire/survey data already tagged 2nd Tier / Scientific Discovery and in TabArena Reject, with curator concerns about it being survey/interpretability data, possibly clustered by user, and containing sensitive features like race. It is a known tabular multiclass dataset (used by TabSTAR), but the survey nature, 1997 vintage, and ethical/leakage caveats keep it at 2nd Tier rather than a clean Yes. A human must verify the chosen target, whether per-user 'who' features cause grouping/leakage, and the ethics of sensitive attributes.

---

CC: "Multiclass. Might be survey data. Might actually be an interpretability task. Also might be clustered data; unique users ("who" features); some other questionable features like race"

## Reference

[1]Graphics, Visualization, & Usability Center College of Computing Geogia Institute of Technology Atlanta, GA Donor [2]Dr Di Cook, Department of Statistics, Iowa State University Date Donated: June 30, 1999; survey conducted by the Graphics and Visualization Unit at Georgia Tech October 10 to November 16, 1997.
