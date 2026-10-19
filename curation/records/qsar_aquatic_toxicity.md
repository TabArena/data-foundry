---
unique_name: qsar_aquatic_toxicity
name: qsar_aquatic_toxicity
checked_by:
- Lennart
- Andrej
data_foundry_status:
- 'DF: Yes'
- BeyondArena
suggestion: Yes (Disagreement)
tags:
- Tiny Data
collections:
- TabArena Reject
original_source: UCI
year: '2014'
domain: biology & life sciences
required_split:
- Random (IID)
problem_type: Regression
original_data_state: One Table
source_links:
- https://doi.org/10.24432/C5SG7H
notebook_path: datasets/beyond_iid/new_iid/qsar_aquatic_toxicity/qsar_aquatic_toxicity.ipynb
v2_path: datasets/_dev/tabarena-v0pt2/qsar_aquatic_toxicity/dataset.py
source_row: 3
type_adapter_id: curation-record-v1
---

## Comments

CC: "546 samples, too small for 3-fold CV. 

Same data source / type of study as for QSAR_fish_toxicity (10.24432/C5JG7B)

predict acute aquatic toxicity towards the fish Pimephales promelas (fathead minnow) on a set of 908 chemicals."

Check if any of the qsar fish datasets are used in tabaren already

Other version in TabArena "QSAR_fish_toxicity"

Generally fine to add, but we need to decide whether we allow two datasets that similar in the benchmark

**Assessment (AI, 2026-10-14):** the quoted sentence about the fathead minnow and 908 chemicals is UCI's summary of QSAR fish toxicity (UCI 504), pasted by mistake into the summary of this dataset (UCI 505). This dataset is 546 chemicals with the 48-hour LC50 for Daphnia magna, a regression target (UCI 505 abstract; Cassotti et al. 2014).

## Reference

@article{cassotti2014prediction,
  title={Prediction of acute aquatic toxicity toward daphnia magna by using the ga-k nn method},
  author={Cassotti, Matteo and Ballabio, Davide and Consonni, Viviana and Mauri, Andrea and Tetko, Igor V and Todeschini, Roberto},
  journal={Alternatives to Laboratory Animals},
  volume={42},
  number={1},
  pages={31--41},
  year={2014},
  publisher={SAGE Publications Sage UK: London, England}
}
