---
unique_name: quake
name: quake
suggestion: 'No'
decision_markers:
- No Good Target  / Scientific Discovery
tags:
- 2nd Tier / Scientfic Discovery
year: '1996'
required_split:
- Random (IID)
- Grouped (NON-IID)
problem_type: Regression
source_links:
- https://www.openml.org/search?type=data&id=550
type_adapter_id: curation-record-v1
---

# quake

## Comments

Imported from the TabArena curation workbook.

TabArena curation verdict: Scientific Discovery.

Only three features, likely not a meaningful task. info about dataset in book: "Characteristics of 2178 earthquakes with magnitude at least 5.8 on the
Richter scale occurring between January 1964 and February 1986"; newer version exist: https://www.kaggle.com/datasets/alessandrolobello/the-ultimate-earthquake-dataset-from-1990-2023

Potential issue: some temporal relationship; a lot spatial realtion ship as feautres a focal depth, lat and logitude, outdated; not a predictive task

Lennart: We can likely ignore the impact of time for the task; the spatial and the age; but not a predictive task originally and not a real task either

## Reference

"Smoothing Methods in Statistics," by Jeffrey S. Simonoff, Springer-Verlag, New York, 1996.
