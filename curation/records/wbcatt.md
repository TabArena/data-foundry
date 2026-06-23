---
unique_name: wbcatt
name: WBCAtt
checked_by:
- Lennart
suggestion: TBD -> Yes
decision_markers:
- Wrong Domain / Source Modality
- Image
- Data Quality Issue
collections:
- TabSTAR
source_links:
- https://www.openml.org/search?type=data&id=46676&sort=runs&status=active
- https://proceedings.neurips.cc/paper_files/paper/2023/hash/9f34484e5b8d87f09cc58c292a1c9f5d-Abstract-Datasets_and_Benchmarks.html
source_row: 640
type_adapter_id: curation-record-v1
---

# WBCAtt

## Comments

All features from the tabular OpenML version are TARGETS of the images

"we have identified 11 morphological attributes associated with the cell and its components (nucleus, cytoplasm, and granules). We then annotated ten thousand WBC images with these attributes, resulting in 113k labels (11 attributes x 10.3k images)"

Unclear if it makes sense to solve this as a tabular task

From Figure 6, it seems a tabular task might still be valid as it is like a treatment/causal/counterfactual inference based method
