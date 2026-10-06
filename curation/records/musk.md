---
unique_name: musk
name: musk
checked_by:
- Lennart
data_foundry_status:
- 'DF: Yes'
- BeyondArena
suggestion: 'Yes'
tags:
- Tiny Data
- Non-IID (Grouped)
collections:
- TabArena Reject
original_source: UCI
year: '1994'
domain: chemistry & material science
required_split:
- Grouped (NON-IID)
- '?'
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://archive.ics.uci.edu/dataset/75/musk+version+2
- https://www.openml.org/search?type=data&sort=runs&id=1116&status=active
- https://doi.org/10.24432/C51608
- https://doi.org/10.24432/C5ZK5B
notebook_path: datasets/beyond_iid/grouped/musk/musk.ipynb
v2_path: datasets/_dev/tabarena-v0pt2/musk/dataset.py
source_row: 5
type_adapter_id: curation-record-v1
---

## Comments

CC: "multiple instance problem - multiple instances of the same molecule are in the data. The classifier should classify as 1 if any of the instances is 1 (0 if none). Leak if used with random splits. Classic Physics/Chemistry application, definitely worth including. Not in TabRepo, but likely due to leak; Could be used after preprocessing to reduce to the original (very small) dataset of 102 molecules. When done, the dataset is however too small for our selection size"

We use musk version 2 as a starting point and treat it as a grouped prediction task

AT: No disagreement, but we should discuss how to treat the multi-instance problem

CC (2026-10-06, Lennart): Kept in TabArena v0.2 as a valid tiny-data task after the task-probe review (flags `no_spread`, `unstable`). v2 scores per molecule (`any` over its conformations): 102 molecules, 39 musk and 63 non-musk, so each grouped test fold scores 34 molecules (13 musk, 21 non-musk; 273 pairs per ROC AUC). That is small, like other tiny tasks, but not a handful: parkinsons was retired for 2-3 healthy people per fold out of 8 in total. The probe's three untuned families reach skill +0.61 to +0.72 (standard deviation 0.11-0.13 over 5 splits); on BeyondArena (scored per conformation) the best method (Causilo) reaches AUC 0.892 and the median 0.850, with 8 of 29 methods tied with the best and ranks that vary from fold to fold (Kendall's W 0.17), as expected at this size.

## Reference

10.24432/C51608
