---
unique_name: asp_potassco_classification
name: ASP-POTASSCO-classification from aslib_data
checked_by:
- Lennart
data_foundry_status:
- 'DF: Yes'
- BeyondArena
suggestion: 'Yes'
tags:
- Non-IID (Grouped)
collections:
- TabArena Reject
original_source: ASlib
year: '2014'
domain: technology & internet
required_split:
- Grouped (NON-IID)
problem_type: Multiclass Classification
original_data_state: One Table
source_links:
- https://www.openml.org/d/41705
- https://github.com/coseal/aslib_data/tree/master/ASP-POTASSCO
notebook_path: datasets/beyond_iid/grouped/asp_potassco_classification/asp_potassco_classification.ipynb
v2_path: datasets/_dev/tabarena-v0pt2/asp_potassco_classification/dataset.py
source_row: 695
type_adapter_id: curation-record-v1
---

## Comments

CC: ""Algorithm selection task. samples are per instance_id - unique algorithms. Task is to predict algorithm - not sure whether this makes sense

After post-hoc analysis: Requires group split. We assumed that it doesn't because the instance IDs were unique, however, they are only unique because they represent directories for repeated evaluations of the same task, i.e.: FolioSuite/ASP-Comp-2011-Lparse/26-Solitaire/1-solitaire-20-0.asp.gz - there are multiple solitaire instances and if we use random splits there is a leak.""

CC (2026-10-01, Lennart): The source splits these instances at random (claspfolio 2: random halves of the Potassco set, 2,589 instances from 105 problem classes; ASlib's cv.arff: 10 random folds). Under the source's use case, new instances of known problem classes, a shared class is not a leak, and the instances of a class are different instances, not repeated runs. Grouping by problem class (the instance path without the file name, 96 classes among the 1,212 instances some configuration solves) is our choice: it asks for a configuration on a problem class never seen in training, as for a user with a new encoding. The choice matters: for 85% of instances the nearest other instance in feature space is from the same class (under 4% by chance), and a class's most common best configuration is the best one for 46% of instances (20% for the overall most common).

## Reference

@article{hoos2014claspfolio,
  title={claspfolio 2: Advances in algorithm selection for answer set programming},
  author={Hoos, Holger and Lindauer, Marius and Schaub, Torsten},
  journal={Theory and Practice of Logic Programming},
  volume={14},
  number={4-5},
  pages={569--585},
  year={2014},
  publisher={Cambridge University Press}
}
