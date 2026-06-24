---
unique_name: ovarian_cancer_prediction
name: NCI ovarian data
checked_by:
- Lennart
data_foundry_status:
- 'DF: Yes'
suggestion: 'No'
decision_markers:
- Trivial
tags:
- New IID
- Many features
collections:
- FS Benchmark
original_source: Other
year: '2002'
domain: medical & healthcare
required_split:
- Random (IID)
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://www.openml.org/d/45098
- https://home.ccr.cancer.gov/ncifdaproteomics/ppatterns.asp
- Rel? https://github.com/chenzRG/Cancer-Multi-Omics-Benchmark.git
source_row: 1034
type_adapter_id: curation-record-v1
---

# NCI ovarian data

## Comments

CC: "Link provided in the survey are outdated, I think I found another version, shapes of OpenML dataset match the shapes given in the paper. D: this is data used for ARCENE in NIPS 2003. Downloadable under low resolution seldi-tof datasets"

Model achieves perfect score, likely trivial dataset due to unknown leakage in the data

## Reference

@article{petricoin2002use,
  title={Use of proteomic patterns in serum to identify ovarian cancer},
  author={Petricoin, Emanuel F and Ardekani, Ali M and Hitt, Ben A and Levine, Peter J and Fusaro, Vincent A and Steinberg, Seth M and Mills, Gordon B and Simone, Charles and Fishman, David A and Kohn, Elise C and others},
  journal={The lancet},
  volume={359},
  number={9306},
  pages={572--577},
  year={2002},
  publisher={Elsevier}
}
