---
unique_name: eucalyptus
name: eucalyptus
checked_by:
- Lennart
suggestion: TBD -> Yes
decision_markers:
- Outdated
tags:
- Non-IID (Grouped)
- Non-IID (Temporal)
- '?'
collections:
- TabArena Reject
- TabSTAR
year: '1991'
source_links:
- https://www.openml.org/d/188
- https://storm.cis.fordham.edu/~gweiss/data-mining/datasets.html -> WEKA Dataset Collection  original links dead (https://tunedit.org/repo/Data/Agricultural/eucalyptus.arff, https://www.cs.waikato.ac.nz/ml/weka/datasets.html) -> cannot find this in the new collections
source_row: 611
type_adapter_id: curation-record-v1
---

## Comments

CC: "Clustered data per site. May require group split, description mentions that trials changed over time so likely shifts. Also spatial data. Might be a nice dataset, although likely outdated. 736 samples"

Very unclear use case without domain knowledge. Unsure how to split based on description, also maybe just a scientific discovery task

## Reference

https://ml.cms.waikato.ac.nz/publications/1996/Thomson-McQueen-96.pdf
