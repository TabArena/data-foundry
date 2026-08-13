---
unique_name: sat11_hand_algo_runtime
name: SAT11-HAND-ALGO runtime-regression from aslib_data
checked_by:
- Lennart
data_foundry_status:
- 'DF: Yes'
- BeyondArena
suggestion: 'Yes'
tags:
- Non-IID (Grouped)
- Multi-target
collections:
- TabArena Reject
- TabSTAR
original_source: ASlib
year: '2011'
domain: technology & internet
required_split:
- Grouped (NON-IID)
problem_type: Regression
original_data_state: One Table
source_links:
- https://www.cs.ubc.ca/labs/algorithms/Projects/SATzilla/
- https://www.openml.org/d/41980
- https://github.com/coseal/aslib_data/tree/master/SAT11-HAND-ALGO
notebook_path: datasets/beyond_iid/grouped/sat11_hand_algo_runtime/sat11_hand_algo_runtime.ipynb
source_row: 694
type_adapter_id: curation-record-v1
---

## Comments

CC: "Some code runtime prediction challenge; see https://arxiv.org/pdf/1506.02465 and https://arxiv.org/pdf/1111.2249  and https://github.com/coseal/aslib_data/tree/master/SAT11-HAND; on openml the instance ID is missing, so in its current state this would create a leak (we have information about the to-be-solved SAT instance). Leak without instance ID, could get real data from other sources but this would then require grouped splits as normally done in AS literature"  

Good to have some datasets from this kind of literature as well, maybe checkout if any newer cases exist we can add to the benchmark

For 41980, we can parse the row ID to get a grouped algorithm selection task. This would be great to cover as well! Otherwise use https://github.com/coseal/aslib_data/tree/master/SAT11-HAND


I would focus on including such datasets for SAT solving, as this seems a "realer" use case than for ML algorithm selection which is usually Pareto, dominated by other methods. 

We use the task that aims to go from (Instance_features, algorithm_features) -> runtime; which is more or less an alternative to multi-target modelling aiming to generalize across algorithms.

## Reference

@inproceedings{xu-sat12a,
  author    = {L. Xu and F. Hutter and H. Hoos and K. Leyton-Brown},
  title     = {Evaluating Component Solver Contributions to Portfolio-Based Algorithm Selectors},
  pages     = {228-241},
  crossref  = {sat12}
}

@Proceedings{sat12,
  editor =         {A. Cimatti and R. Sebastiani},
  title =         {Proceedings of the Fifteenth International Conference on Theory and Applications of Satisfiability Testing (SAT'12)},
  booktitle = {Proceedings of the Fifteenth International Conference on Theory and Applications of Satisfiability Testing (SAT'12)},
  publisher =         springer,
  series =         lncs,
  volume =         7317,
  year =         2012
}
@article{bischl_aslib_2016,
	title = {{ASlib}: {A} {Benchmark} {Library} for {Algorithm} {Selection}},
	number = {237},
	journal = {Artificial Intelligence Journal (AIJ)},
	author = {Bischl, Bernd and Kerschke, Pascal and Kotthoff, Lars and Lindauer, Marius and Malitsky, Yuri and Fréchette, Alexandre and Hoos, Holger H. and Hutter, Frank and Leyton-Brown, Kevin and Tierney, Kevin and Vanschoren, Joaquin},
	year = {2016},
	pages = {41--58}
}
