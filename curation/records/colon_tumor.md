---
unique_name: colon_tumor
name: Colon
checked_by:
- Lennart
suggestion: 'No'
decision_markers:
- Too Small
tags:
- New IID
- Many features
collections:
- FS Benchmark
original_source: OpenML
year: '1999'
domain: medical & healthcare
required_split:
- Random (IID)
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://www.openml.org/search?type=data&sort=runs&id=45087&status=active
source_row: 1032
type_adapter_id: curation-record-v1
---

# Colon

## Comments

CC: ""The genes chosen are the 2,000 genes with highest minimal intensity across the samples."- openml publishes the already filtered out data. It's unsupervised filtering so should be fine."

Only 62 samples, too small to be a reasonable non-few-shot task with cross-validation.

## Reference

@article{alon1999broad,
  title={Broad patterns of gene expression revealed by clustering analysis of tumor and normal colon tissues probed by oligonucleotide arrays},
  author={Alon, Uri and Barkai, Naama and Notterman, Daniel A and Gish, Kurt and Ybarra, Suzanne and Mack, Daniel and Levine, Arnold J},
  journal={Proceedings of the National Academy of Sciences},
  volume={96},
  number={12},
  pages={6745--6750},
  year={1999},
  publisher={The National Academy of Sciences}
}
