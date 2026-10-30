---
unique_name: cardiotocography
name: Cardiotocography
checked_by:
- Lennart
data_foundry_status:
- 'DF: Yes'
- BeyondArena
suggestion: 'Yes'
decision_markers:
- Wrong Domain / Source Modality
- Time-series (Classification)
tags:
- Non-IID (Grouped)
collections:
- TabArena Reject
original_source: UCI
year: '2010'
domain: medical & healthcare
required_split:
- Grouped (NON-IID)
problem_type: Multiclass Classification
original_data_state: One Table
source_links:
- https://archive.ics.uci.edu/dataset/193/cardiotocography
- https://doi.org/10.24432/C51S4N
notebook_path: datasets/beyond_iid/grouped/cardiotocography/cardiotocography.ipynb
v2_path: datasets/_dev/tabarena-v0pt2/cardiotocography/dataset.py
source_row: 693
type_adapter_id: curation-record-v1
---

## Comments

The label is the consensus of three experts (so likely noisy).

Can be either 10 or 3 class problem.
Raw data has dates!


From going through the raw data description, it seems one had one or multiple measurements per patient and split it into multiple rows or segments and then created tabular features. Targets can be different per instance. Need to take raw data to get the group IDs.

CC (2026-10-21, Lennart): "yes we should have one clear way to treat 0/1 flags": every 0/1 flag (a feature holding only 0 and 1, plus missing values; booleans too) is categorical (CLEAN-14, amended). Typed categorical here: DS (DR is constant 0 and stays as it is).

CC (2026-10-21, Lennart): on which 0/1 columns are flags: "no if we can infer from the semantic context, keep it a number, this is a real-world bias. We want to make things categorical if we know from the context they are indeed such" (CLEAN-14, amended again). Reverted: DS (severe decelerations per second, a measured rate) stays numeric.

**Assessment (AI, 2026-10-21):** Metric declared under MET-1..13: fallback log_loss — UCI page defines no task metric; the SisPorto 2.0 paper describes the analysis program and expert agreement, not a prediction benchmark.

**Assessment (AI, 2026-10-30):** Dtype review (branch ordinal-and-censored-levels; the column decisions with their codebook evidence are on the review board): ordinal scales shipped as numbers, left as numbers for the curator's review: `Tendency`.

## Reference

@misc{cardiotocography_193,
  author       = {Campos, D. and Bernardes, J.},
  title        = {{Cardiotocography}},
  year         = {2000},
  howpublished = {UCI Machine Learning Repository},
  note         = {{DOI}: https://doi.org/10.24432/C51S4N}
}
