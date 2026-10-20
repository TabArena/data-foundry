---
unique_name: phiusil_phishing
name: PhiUSIIL Phishing URL (Website)
checked_by:
- Andrej
data_foundry_status:
- 'DF: Yes'
suggestion: Disagreement
priority: 2
tags:
- Larger IID Data
collections:
- New (BeyondArena)
original_source: Other
year: '2024'
domain: technology & internet
required_split:
- Random (IID)
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://archive.ics.uci.edu/dataset/967/phiusiil+phishing+url+dataset
- https://doi.org/10.1016/j.cose.2023.103545
v2_path: datasets/_dev/tabarena-v0pt2/phiusil_phishing/dataset.py
source_row: 2
type_adapter_id: curation-record-v1
---

## Comments

Recent dataset for phishing website detection, best I know so far (AT). Features extracted from website source code. Might also be approached with LLMs, but since the paper is recent that's not a concern. Might need to double check that the feature extraction doesn't introduce leaks

Discussion: unclear if this is grouped data or not!

**Assessment (AI, 2026-10-07):** Recommend excluding it (`Data Quality Issue`). The two classes were collected differently, and every feature family shows it. All 134,850 legitimate rows are ranked domains written as https://www.<host> with no path, a form only 627 of the 100,520 phishing URLs share (URL features alone: AUC 0.9989). The phishing pages were fetched after the URLs were listed: 50.5% of phishing rows sit on 115 shared pages, none with a password field. A fixed rule with no training reaches AUC 0.9998. Andrej's leak question: the definition drops URLSimilarityIndex, Title and the two title scores, which does not change this. Hosts repeat only among phishing rows, and a host-grouped split scores the same. The file first appeared on Mendeley Data (2023).

**Assessment (AI, 2026-10-20):** priority 2 for the review of the added dataset: gap -, use case -, source +, shape +, risk - (Issue 1: run recommends exclusion; collection artefacts separate classes (fixed rule AUC 0.9998)). Not useful: a fixed rule solves it because phishing and legitimate rows were collected differently; no version of the file is a valid task.

## Reference

Prasad, A., & Chandra, S. (2023). PhiUSIIL: A diverse security profile empowered phishing URL detection framework based on similarity index and incremental learning. Computers & Security, 103545. doi: https://doi.org/10.1016/j.cose.2023.103545
