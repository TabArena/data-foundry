---
unique_name: prostate_cancer_detection
name: NCI prostate cancer data
checked_by:
- Lennart
data_foundry_status: 'Yes'
suggestion: 'Yes'
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
problem_type: Multiclass Classification
usable_task_type: Predictive ML
given_task_type:
- Predictive ML
- Scientific Discovery
data_modality:
- Tabular
original_data_state: One Table
source_links:
- https://home.ccr.cancer.gov/ncifdaproteomics/ppatterns.asp
source_row: 1036
type_adapter_id: curation-record-v1
---

# NCI prostate cancer data

## Comments

CC" Link provided in the survey are outdated, I think I found another version. D: Downloadable under low resolution seldi-tof dataests. The number of csv files matches the number of samples so we just need to merge everything into one table. Clasees are given in folder names"

## Reference

@article{petricoin2002serum,
  title={Serum proteomic patterns for detection of prostate cancer},
  author={Petricoin III, Emanuel F and Ornstein, David K and Paweletz, Cloud P and Ardekani, Ali and Hackett, Paul S and Hitt, Ben A and Velassco, Alfredo and Trucco, Christian and Wiegand, Laura and Wood, Kamillah and others},
  journal={Journal of the National Cancer Institute},
  volume={94},
  number={20},
  pages={1576--1578},
  year={2002},
  publisher={Oxford University Press}
}
