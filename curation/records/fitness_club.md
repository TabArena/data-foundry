---
unique_name: fitness_club
name: Fitness_Club_c
data_foundry_status:
- 'DF: Yes'
- TabArena (v0.1)
- BeyondArena
suggestion: 'Yes'
original_source: Kaggle
year: '2023'
required_split:
- Random (IID)
source_links:
- https://www.kaggle.com/datasets/ddosad/datacamps-data-science-associate-certification
type_adapter_id: curation-record-v1
---

# Fitness_Club_c

## Comments

Clean canonical entry bootstrapped from the TabArena curation workbook ('Tabular' row). Shipped in TabArena (v0.1) / BeyondArena.

TabArena curation verdict: Tabular.

Seems rather simple, but interesting. Might require time split. Features are time-invariant, but distribution shifts due to changing classes and instructors are still likely. Unclear which time period the 1500 sampes span

Linear model is best for this dataset - data is from a datacamp course and might have been artificially generated.

Potential issue: temporal split required

Lennart: Maybe simple task but no other objections

Andrej: Not the best data for this task as a lot of important information is missing. But interesting enough to ignore that; Also license might be an issue

## Reference

https://www.kaggle.com/datasets/ddosad/datacamps-data-science-associate-certification
