---
unique_name: srbct_prediction
name: SRBCT
checked_by:
- Lennart
suggestion: 'No'
decision_markers:
- Trivial
- Too Small
tags:
- New IID
- Many features
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
- https://www.openml.org/d/45101
notebook_path: datasets/_dev/feature_selection/srbct_prediction/srbct_prediction.ipynb
source_row: 1039
type_adapter_id: curation-record-v1
---

## Comments

CC: "No original deposition of the dataset, many R packages include it (in the same shape) but no better source than OpenML. Round blue cell tumors (SRBCT) dataset. From this paper: we used gene-expression data from cDNA microarrays containing 6567 genes. "

Rel: https://arxiv.org/abs/2311.12879

Only 83 samples, and in the paper from rel RF gets 100% accuracy. So likely we can rule it out for now.

## Reference

@article{khan2001classification,
  title={Classification and diagnostic prediction of cancers using gene expression profiling and artificial neural networks},
  author={Khan, Javed and Wei, Jun S and Ringner, Markus and Saal, Lao H and Ladanyi, Marc and Westermann, Frank and Berthold, Frank and Schwab, Manfred and Antonescu, Cristina R and Peterson, Carsten and others},
  journal={Nature medicine},
  volume={7},
  number={6},
  pages={673--679},
  year={2001},
  publisher={Nature Publishing Group}
}
