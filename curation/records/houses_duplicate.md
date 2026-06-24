---
unique_name: houses_duplicate
name: houses
suggestion: 'No'
decision_markers:
- Duplicate
year: '1990'
required_split:
- Random (IID)
problem_type: Binary Classification
source_links:
- https://www.openml.org/search?type=data&id=823
- http://lib.stat.cmu.edu/datasets/
type_adapter_id: curation-record-v1
---

## Comments

Shipped in the BeyondArena / TabArena (v0.1) collection(s).

TabArena curation verdict: Tabular.

Regression. California Housing data from 1990 likely is outdated. Also we could collect much more data if this would be a real task. In general, likely an interpretability task anyway. Also data was preprocessed in a very special way. As the data is spatial, custom split might be required? TabRepo version of the dataset almost certainly contains a leak.

Potential issue: Outdated, spatial Data, Preprocssed

Lennart: In a task like this, I think it would count as IID as spatial information are not leaking / we can assume to have/get them.

Andrej: non-iid. Currently, we do not include spatial data as non-iid. Might change that. Temporal split required but not possible (see TabRed)

## Reference

Pace and Barry (1997), "Sparse Spatial Autoregressions", Statistics and Probability Letters.
