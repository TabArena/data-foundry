---
unique_name: open_university_learning_analytics_dataset
name: Open University Learning Analytics dataset
checked_by:
- Lennart
data_foundry_status:
- WIP (DF)
claimed_by: Lennart
suggestion: 'Yes'
decision_markers:
- Needs extensive data wrangling
tags:
- Non-IID (Temporal)
- Larger IID Data
collections:
- New (BeyondArena)
original_source: Website
year: '2015'
domain: education
required_split:
- Grouped (NON-IID)
problem_type: Multiclass Classification
original_data_state: Database (or multiple to-be-joined tables)
source_links:
- https://doi.org/10.24432/C5KK69
- https://analyse.kmi.open.ac.uk/
- https://analyse.kmi.open.ac.uk/open-dataset
v2_path: datasets/_dev/tabarena-v0pt2/open_university_learning_analytics_dataset/dataset.py
source_row: 738
type_adapter_id: curation-record-v1
---

## Comments

Could be transformed into a prediction task https://www.kaggle.com/code/devassaxd/student-performance-prediction-complete-analysis#Part-3:-Modeling

On the website they also talk about their predictive models

Use cases of the data (?):
https://dl.acm.org/doi/10.1145/3576050.3576061

https://www.sciencedirect.com/science/article/pii/S2666920X22000637?via%3Dihub (explains how to do feature selection for the task?)

We might follow the Kaggle notebook as it seems to know more of the data and use case. Seems reasonable in most cases for the task. Could be made for several tasks, unclear which one would be best

**Assessment (AI, 2026-10-07):** The task is final_result (four classes) on day 60 for the 26,395 registrations active then, using only what is known by day 60. The Kaggle notebook above uses the exam score, so it leaks the result. The OU trains on other presentations of a module (OULAD page: "the J presentation must be used to inform the B presentation or vice versa"). Four start dates cannot give three temporal windows, so the split holds out whole presentations. LightGBM log-loss skill: IID 0.193, grouped 0.141, 2014J hold-out 0.099. BBB 2014J marks its first TMA 1 or 100 (weight 0), and models score below the prior there. Data: figshare 10.6084/m9.figshare.5081998.v1 (CC BY 4.0); the OU link is dead.

## Reference

Kuzilek J., Hlosta M., Zdrahal Z. Open University Learning Analytics dataset Sci. Data 4:170171 doi: 10.1038/sdata.2017.171 (2017).
