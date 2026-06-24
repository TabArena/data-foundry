---
unique_name: covertype
name: covertype
checked_by:
- Lennart
data_foundry_status:
- 'DF: Yes'
- BeyondArena
suggestion: 'Yes'
decision_markers:
- Outdated
tags:
- Non-IID (Grouped)
collections:
- TabArena Reject
- TabSTAR
original_source: UCI
year: '1998'
domain: environmental science & climate
required_split:
- '?'
problem_type: Multiclass Classification
original_data_state: One Table
source_links:
- https://archive.ics.uci.edu/dataset/31/covertype
- https://doi.org/10.24432/C50K5N
source_row: 691
type_adapter_id: curation-record-v1
---

# covertype

## Comments

CC: ""The original study used random splits and it also makes sense to do so. In a real application one would collect samples randomly across the studied area, and afterwards try to fill the gaps to predict unseen areas to save collection time.

The real task would be rather solved using remote sensing data. Spatial data. TabRed says that task requires time split. I think otherwise the task does not make sense as the same locations might reoccur (but unsure about that); unclear if real task would have knowledge of close-by spatial domain or if it would be needed in that case; some of the features are distance to some place, if features are from the same area, this might be leaking.""

Results of re-investigation:
1) contains several areas (Rawah, Comanche Peak, Neota, Cache la Poudre), so these represent subgroups but can be IID
2) TabRed claims that a time split is needed for a real task (makes sense), but no time feature exists. Moreover, they claim the task is not real-world anymore as no GNSS data is included in the prediction task
3) Both the wilderness area and soil type are one-hot encoded categorical features.
4) It seems the OpenML version in TALENT (https://www.openml.org/d/150) comes with transformed features that are leaking the test distribution for any split
5) the data on UCI comes with incorrect column order based on the info file
6) After doing some basic EDA, we found that areas might be distinct in their characteristics, and classes only appear for some of the areas in general. So this is clearly a grouped dataset as trees heavily depend on the wilderness area.
7) Only the target was determined by image usage, the features depend on pre-determined information about the location and spatial data.

Besides missing a time feature, the data is also missing location features that would allow us to build spatial splits across all data points. Instead, we only have areas to filter, which by nature of collecting the data are also time splits.

From all the above, we conclude the following: if we use IID splits, we have either time or spatial leakage. To fix this, we need to perform some kind of spatial split. The only real non-relative spatial indicator is the area. This allows us to make the task a grouped-split with holding out one area at a time. However, some classes only exist for some areas, while others exist for many areas.
Thus, we reduce the dataset only to the classes which exist for all the three biggest areas and do grouped splits across areas.

## Reference

https://www.sciencedirect.com/science/article/abs/pii/S0168169999000460
