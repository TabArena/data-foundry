---
unique_name: defect_data
name: defect data
checked_by:
- Lennart
suggestion: TBD -> 2nd Tier
decision_markers:
- Outdated
tags:
- Tiny Data
- '?'
- New IID
collections:
- TabArena Reject
- TabSTAR
original_source: GOV Website
year: '2004'
domain: technology & internet
required_split:
- Random (IID)
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://openscience.us/repo/defect/
- pc1,pc2,pc3,pc4,mc1,kc1,kc2,kc3,jm1
- https://www.openml.org/d/1049
- https://www.openml.org/d/1067
source_row: 576
type_adapter_id: curation-record-v1
---

## Comments

Look into this collection again and take one or two representative cases but not all of them and only if they make sense

The task type is outdated and might be solved very differently nowadays. Unclear if there are newer tasks like this.

If we go for this data, it is unclear which dataset to use, if any of them. In general, it is weird/old data.

The task is usually a defect module prediction based on static code features.

CM1: C, NASA spacecraft instrument
JM1: C++, simulated real-time predictive ground system
KC1: C++, storage management and preprocessing ground data
KC2: science data processing (overlap with KC1 in terms of team and tools but not in terms of code)
PC1: flight software for earth orbiting satellite
(PC2, PC3, PC4, PC5 links to the same paper that introduces PC1 but it is never mentioned)
(Mc1, Mc2, kc3 missing any source; likely details were on the now gone NASA web page)
The last paper also points out various issues in the dataset and cleaned the data but finding the cleaned data is also hard


The authors and curators of these datasets also claim not to use learning methods as they severely limit applicability across datasets and management options (?): "Therefore, we recommend against using LSR or Model Trees as a basis for locating and choosing detectors." Therefore, we recommend against using J4.8 as a basis for locating and choosing detector"

https://openscience.us/repo/defect/mccabehalsted/

In general, these are all datasets of the same type of features and task

Sometimes, the datasets are also merged: https://www.kaggle.com/datasets/ziya07/software-defect-prediction-dataset (which is not recommended from a task POV)

Finally, there is so much data on these kinds of tasks (as they are somewhat easy to get?) that it is unclear if this should be part of our benchmark or its own thing (see https://arxiv.org/pdf/2504.17977)

## Reference

https://openscience.us/ext/menzies.us/pdf/03blind.pdf

https://bura.brunel.ac.uk/bitstream/2438/7926/2/TSE_NASADataQualNote_V26.pdf
