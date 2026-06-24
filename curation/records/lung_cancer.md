---
unique_name: lung_cancer
name: Lung
checked_by:
- Lennart
data_foundry_status:
- 'DF: Yes'
- BeyondArena
suggestion: 'Yes'
tags:
- New IID
- Many features
- Tiny Data
collections:
- FS Benchmark
original_source: OpenML
year: '2001'
domain: medical & healthcare
required_split:
- Random (IID)
problem_type: Multiclass Classification
original_data_state: One Table
source_links:
- https://www.openml.org/d/45093
- 'Can get data from paper website as well and we should: https://www.pnas.org/doi/10.1073/pnas.191502998#supplementary-materials'
- Contains Dataset A and B, B is subset of A that is only binary classification
source_row: 1033
type_adapter_id: curation-record-v1
---

## Comments

CC: "No raw data available, using OpenML (shapes match). Original 6 classes were merged into 5 (adenocarcinomas). "

From the paper:
"We built a supervised classifier by first defining subclasses based on hierarchical and probabilistic clustering and chose marker genes by using ''K-Nearest Neighbor'' classifiers based on the signal-to-noise statistic"

The label for the task on OpenML is unclear, I cannot find the source. The paper talks about clusters they computed in an unsupervised way on the original data. In other words, we don't have a real predictive task with a real target. This was mostly done for scientific discovery. Comparing models on this data does not make a lot of sense and does not hold valuable information or a valuable new task.

Fun fact, the data contains survival prediction data, as well as it seems.

The way we can make this a real task is to use the info from the original investigation about the type of lung cancer:
"The 203 specimens (Dataset A) include histologically defined lung adenocarcinomas (n = 127), squamous cell lung carcinomas (n = 21), pulmonary carcinoids (n = 20), SCLC (n = 6) cases, and normal lung (n = 17) specimens. Other adenocarcinomas (n = 12) were suspected to be extrapulmonary metastases based on clinical history"

Thus, we use the data not for clustering as in the original work, but re-use for classification of the original data (simulating as if we were to predict this for new patients).
From the use case, it is unclear if this would really be done, as it is likely not trivial to get the features for an unharmed patient.

## Reference

@article{bhattacharjee2001classification,
  title={Classification of human lung carcinomas by mRNA expression profiling reveals distinct adenocarcinoma subclasses},
  author={Bhattacharjee, Arindam and Richards, William G and Staunton, Jane and Li, Cheng and Monti, Stefano and Vasa, Priya and Ladd, Christine and Beheshti, Javad and Bueno, Raphael and Gillette, Michael and others},
  journal={Proceedings of the National Academy of Sciences},
  volume={98},
  number={24},
  pages={13790--13795},
  year={2001},
  publisher={The National Academy of Sciences}
}
