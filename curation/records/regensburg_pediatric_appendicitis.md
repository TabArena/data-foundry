---
unique_name: regensburg_pediatric_appendicitis
name: Regensburg Pediatric Appendicitis
checked_by:
- Lennart
data_foundry_status: 'Yes'
suggestion: 'Yes'
tags:
- Tiny Data
collections:
- New (BeyondArena)
- TabSTAR
original_source: UCI
year: '2021'
domain: medical & healthcare
required_split:
- Random (IID)
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://archive.ics.uci.edu/dataset/938/toxicity
- 10.5281/zenodo.7669442
- (https://www.openml.org/search?type=data&id=46603&sort=runs&status=active)
source_row: 746
type_adapter_id: curation-record-v1
---

# Regensburg Pediatric Appendicitis

## Comments

Has three target variables as it seems, we likely want to use Diagnosis

The data was collected over a time horizon, but no timestamp is given. Moreover, the task does not seem to have temporal leakage given that it is across different patients in a fw years, (such that evolution could have had the chance to change the distribution...)

Great case of a dataset where there is a vision model and a tabular baseline (RF). Sadly, the paper does not do a good job of benchmarking the tabular models better, which might even become competitive. And the AUROCs for RF is even hidden in Table 3? I think we should include this dataset to show them how to benchmarks predictive models correctly. At the same time, it is clear that for the other use cases, RF might not help

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
