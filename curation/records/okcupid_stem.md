---
unique_name: okcupid_stem
name: okcupid-stem
checked_by:
- AI (UNVERIFIED)
suggestion: 'No'
decision_markers:
- Not Representative
- Ethical Issue
tags:
- 2nd Tier / Scientfic Discovery
- AI-Filled (Verify)
collections:
- TabArena Reject
- TabSTAR
year: '2012'
domain: social science
required_split:
- Random (IID)
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://github.com/rudeboybert/JSE_OkCupid
source_row: 805
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Assessment (AI, 2026-10-22):** agrees with the curator's `No` (the CC line: "not a meaningful task ... ethical concerns ... meme dataset"; also in `TabArena Reject`); no priority on a `No`.
- Source: Kim and Escobedo-Land, "OkCupid Profile Data for Introductory Statistics and Data Science Courses", Journal of Statistics Education 23(2), 2015 (revised 2021); github.com/rudeboybert/JSE_OkCupid: 59,946 San Francisco profiles; "Permission to use this data set was explicitly granted by OkCupid"; the 2021 revision "Removed the exact date the data was collected". Published for teaching statistics, not for a prediction task. The `okcupid-stem` task (job in STEM, open-text essays dropped) is a later re-framing on OpenML, carried by TabSTAR.
- Use case: none; nobody decides anything from whether a dating-profile user works in STEM (SEL-3, USE-1). This alone decides the `No`; the marker `No Good Target  / Scientific Discovery` would name it better than `Not Representative`.
- Siblings: `okcupid` (Alex, Mustafa, Lennart: `No`, `No Good Target  / Scientific Discovery`, `Ethical Issue`): the same data, decided the same way.
- Counter-point on the ethics marker only: the JSE data was released with OkCupid's explicit permission for teaching, so `Ethical Issue` rests on the use (inferring a person's occupation from a dating profile), not on objecting subjects (SEL-1); the verdict stands on SEL-3 either way.
- Metric: none defined by the source (JSE paper, repo); not needed for a `No`.

OkCupid dating-profile data where the task is predicting whether a user works in STEM, with open-text features already stripped out and the data otherwise preprocessed. The curator flags it as a meaningless/'meme' task, notes ethical concerns about this use of human data, and it already sits in the TabArena Reject collection. The lack of a meaningful target plus the ethical and representativeness issues argue against inclusion. Suggest No.

---

CC: "Already preprocessed. Also the task is to predict whether a person on a dating platform is working in STEM. Might not represent a meaningful task. Feature engineering on categoricals important for that dataset as CatBoost dominates; open text features were removed from the data. It is not a meaningful task, and at the same time, data with/about humans that is a meaningless task; this kind of usage of human data also raises ethical concerns. Furthermore, removing the text features is weird. meme dataset"

## Reference

User profile data for San Francisco OkCupid users published in [Kim, A. Y., & Escobedo-Land, A. (2015). OKCupid data for introductory statistics and data science courses. Journal of Statistics Education, 23(2).]
