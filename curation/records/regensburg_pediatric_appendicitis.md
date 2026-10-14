---
unique_name: regensburg_pediatric_appendicitis
name: Regensburg Pediatric Appendicitis
checked_by:
- Lennart
data_foundry_status:
- 'DF: Yes'
- BeyondArena
suggestion: 'Yes'
tags:
- Tiny Data
collections:
- New (BeyondArena)
- TabSTAR
original_source: Other
year: '2023'
domain: medical & healthcare
required_split:
- Random (IID)
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://doi.org/10.5281/zenodo.7711412
- https://archive.ics.uci.edu/dataset/938/regensburg+pediatric+appendicitis
- (https://www.openml.org/search?type=data&id=46603&sort=runs&status=active)
notebook_path: datasets/beyond_iid/new_iid/regensburg_pediatric_appendicitis/regensburg_pediatric_appendicitis.ipynb
v2_path: datasets/_dev/tabarena-v0pt2/regensburg_pediatric_appendicitis/dataset.py
source_row: 746
type_adapter_id: curation-record-v1
---

## Comments

Has three target variables as it seems, we likely want to use Diagnosis

The data was collected over a time horizon, but no timestamp is given. Moreover, the task does not seem to have temporal leakage given that it is across different patients in a few years (such that evolution could have had the chance to change the distribution...)

Great case of a dataset where there is a vision model and a tabular baseline (RF). Sadly, the paper does not do a good job of benchmarking the tabular models better, which might even become competitive. And the AUROCs for RF is even hidden in Table 3? I think we should include this dataset to show them how to benchmark predictive models correctly. At the same time, it is clear that for the other use cases, RF might not help

**Assessment (AI, 2026-10-14):** The data first appeared on Zenodo (Regensburg Pediatric Appendicitis Dataset v1.0, 2023-02-23, concept DOI 10.5281/zenodo.7669214; the definition downloads v1.03, 10.5281/zenodo.7711412), five days before the paper's preprint (arXiv 2302.14460). UCI 938 is a later copy whose metadata names the Zenodo DOI as its source, so the original source is Other, as in the definition. The old UCI link carried the wrong slug (`toxicity`); id 938 is this dataset.

## Reference

@article{marcinkevivcs2024interpretable,
  title={Interpretable and intervenable ultrasonography-based machine learning models for pediatric appendicitis},
  author={Marcinkevi{\v{c}}s, Ri{\v{c}}ards and Wolfertstetter, Patricia Reis and Klimiene, Ugne and Chin-Cheong, Kieran and Paschke, Alyssia and Zerres, Julia and Denzinger, Markus and Niederberger, David and Wellmann, Sven and Ozkan, Ece and others},
  journal={Medical image analysis},
  volume={91},
  pages={103042},
  year={2024},
  publisher={Elsevier}
}
