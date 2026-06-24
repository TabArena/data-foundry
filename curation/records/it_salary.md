---
unique_name: it_salary
name: it_salary
checked_by:
- Lennart
suggestion: TBD -> 2nd Tier
decision_markers:
- Data Quality Issue
- No Good Target (yet)
tags:
- 2nd Tier / Scientfic Discovery
- Free Text (Short)
collections:
- TexTabBench Extra
source_links:
- https://www.kaggle.com/datasets/parulpandey/2020-it-salary-survey-for-eu-region
- https://www.asdcode.de/2021/01/it-salary-survey-december-2020.html
source_row: 463
type_adapter_id: curation-record-v1
---

## Comments

survey about IT jobs (2020), participants often had categories to pick from but could also provide the other category to provide free text, similar survey exists for previous years, 2018&2019 on kaggle, newer ones here https://docs.google.com/spreadsheets/d/1DjPgQeBu53I0Dws4YMbXyyQdWDLpMtkSu4FhGux0epY/edit?gid=1483964364#gid=1483964364 columns are different across different years

Data clearly has wrong entries and some of them need to be cleared (salary errors and nan values)

The original survey https://docs.google.com/forms/d/e/1FAIpQLSdPDpjEN98tazCLOQ7xxgK84DZeanC8wI_akPyKOeW3HwBhuA/viewform is for the most part either numerical or (multi-)categorical, but in the categorical columns you can also provide your own "other" answer if the given ones don't fit, we can argue whether these columns e.g. Position are free text or not, but for now I will count such as not
