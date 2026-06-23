---
unique_name: miceprotein
name: MiceProtein
checked_by:
- Lennart
data_foundry_status: 'Yes'
suggestion: 'Yes'
tags:
- Non-IID (Grouped)
collections:
- TabArena Reject
- TabSTAR
year: '2015'
domain: biology & life sciences
required_split:
- Grouped (NON-IID)
problem_type: Multiclass Classification
original_data_state: One Table
source_links:
- https://doi.org/10.24432/C50S3Z
source_row: 692
type_adapter_id: curation-record-v1
---

# MiceProtein

## Comments

CC: "Data clustered by 77 proteins and 72 mice. Each protein contains 1080 measurements which are recommended to be seen as separate mice. Therefore a group-based split based on proteins makes sense. Unsure whether predictive performance is the goal or rather interpretation. Also unsure whether the 8 classes given should also be used as they are for classification, might also be framed as a multi-task problem."

## Reference

Higuera C, Gardiner KJ, Cios KJ (2015) Self-Organizing Feature Maps Identify Proteins Critical to Learning in a Mouse Model of Down Syndrome. PLoS ONE 10(6): e0129126.
