---
unique_name: sf_permit_time
name: sf_permit_time
checked_by:
- Lennart
- Alex
- Mustafa
data_foundry_status:
- 'DF: Yes'
- BeyondArena
suggestion: 'Yes'
tags:
- Non-IID (Temporal)
- Free Text (Sentences)
collections:
- TexTabBench
original_source: GOV Website
year: '2018'
domain: industry & manufacturing
required_split:
- Temporal (NON-IID)
problem_type: Regression
original_data_state: One Table
source_links:
- https://www.kaggle.com/datasets/aparnashastry/building-permit-applications-data
- https://data.sfgov.org/Housing-and-Buildings/Building-Permits/i98e-djp9/about_data
notebook_path: datasets/beyond_iid/temporal/sf_permit_time/sf_permit_time.ipynb
source_row: 737
type_adapter_id: curation-record-v1
---

## Comments

building permits
AP: might need spatial/temporal split

Likely preprocess and filter on permit type, and status. Revised cost and some other features might be leaking if the permit was granted or not and if it was granted might leak time to grant. A lot of spatial features, record id is also time informative

the description column: it seems to be diverse enough to be considered free text

LP: very borderline. We need to create some features or filter to meaningful descriptions as many are clearly just a category. Others include a reference to other permits, so there might also be leakage. needs some time to look at and work with.
