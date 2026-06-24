---
unique_name: labour_inspection_compliance
name: LICD_LABOR_RIGHTS
checked_by:
- Lennart
- Mustafa
data_foundry_status:
- 'DF: Yes'
- BeyondArena
suggestion: 'Yes'
tags:
- Larger IID Data
- Free Text (Sentences)
collections:
- TabSTAR
original_source: Other
year: '2022'
domain: industry & manufacturing
required_split:
- Random (IID)
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://www.openml.org/search?type=data&id=46640
- https://dataverse.no/dataset.xhtml?persistentId=doi:10.18710/7U6TZP
- https://dataverse.no/dataset.xhtml;jsessionid=aa0a848e0e843de40284e7be94a9?persistentId=doi%3A10.18710%2F7U6TZP&version=&q=&fileTypeGroupFacet=&fileAccess=&fileSortField=date&tagPresort=false
source_row: 659
type_adapter_id: curation-record-v1
---

# LICD_LABOR_RIGHTS

## Comments

Labor Rights and Corporate Governance - LICD

Depending on the task, we might not be able to use the free text feature as it is leaking or the target.

Has two targets, need to find original data source; many missing values among some columns.

"The first case is selecting a relevant labour inspection checklist for
a given organization. The second case is to predict whether an organization is non-compliant to
working environment regulations, where selected checklists can be used as independent features"

Either many-class classification problem (for checklist ID) or compliance prediction problem (binary). Either case, the text cannot be used as it is leaking the label.

You are allowed to use it: "The Non-compliance Classification Problem (NCP): Given a checklist y and a target organisation x, classify the target organisation's compliance l to any of the regulations given by the content
of y. The value of l is unknown until the completion of the inspection and belongs to a Bernoulli
distribution where l = 1 means that the target organisation is non-compliant and l = 0 means that
the organisation is compliant." from https://papers.nips.cc/paper_files/paper/2022/file/93e4d161bdd93d1dc0202b4044159edb-Paper-Datasets_and_Benchmarks.pdf

Data is missing timestamps, so it is a forced IID task

## Reference

A dataset for efforts towards achieving the sustainable development goal of safe working environments
