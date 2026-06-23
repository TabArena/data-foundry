---
unique_name: phiusil_phishing
name: PhiUSIIL Phishing URL (Website)
checked_by:
- Andrej
data_foundry_status: 'Yes'
suggestion: Disagreement
tags:
- Larger IID Data
collections:
- New (BeyondArena)
original_source: UCI
year: '2024'
domain: technology & internet
required_split:
- Random (IID)
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://archive.ics.uci.edu/dataset/967/phiusiil+phishing+url+dataset
- https://doi.org/10.1016/j.cose.2023.103545
source_row: 2
type_adapter_id: curation-record-v1
---

# PhiUSIIL Phishing URL (Website)

## Comments

Recent dataset for phishing website detection, best I know so far (AT). features extracted from website source code. Might also be approached with LLMs, but since the paper is recent thats not a concern. Might need to double check that the feature extraction doesnt introduce leaks

Discussion: unclear if this is grouped data or not!

## Reference

Prasad, A., & Chandra, S. (2023). PhiUSIIL: A diverse security profile empowered phishing URL detection framework based on similarity index and incremental learning. Computers & Security, 103545. doi: https://doi.org/10.1016/j.cose.2023.103545
