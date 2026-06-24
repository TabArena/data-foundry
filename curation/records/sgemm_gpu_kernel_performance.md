---
unique_name: sgemm_gpu_kernel_performance
name: SGEMM_GPU_kernel_performance
suggestion: 'No'
decision_markers:
- AHDS (Artifical/Handmade/Deterministic/Simulated)
original_source: UCI
year: '2017'
required_split:
- Random (IID)
source_links:
- https://www.openml.org/search?type=data&id=43144
- https://doi.org/10.24432/C5MK70
type_adapter_id: curation-record-v1
---

# SGEMM_GPU_kernel_performance

## Comments

Imported from the TabArena curation workbook.

TabArena curation verdict: Deterministic.

Measures runtime of a matrix product. 4 alternative targets. grinsztajn uses them - leak. Even if the task is treated correctly, it might be trivial - most methods perform similar. but need to verify that. Apparently all possible value combinations are in the dataset - so the task might not make much sense.

Runtime prediction tasks also usually require some speical splits, or more custom preprocessing. Also unclear if this data and taks is not oudated

Potential issue: Trivial

Lennart: Leaning towards no: 1) not a real predictive task if we know and observe all combinations given the feature spce, 2) data might require speical splits given what kind of congiratuions we would not know in an offline setting

Andrej: need to check if the task is trivial. We might even make it an exclusion criterion if all possible values are in the dataset, as it is not an open world scenario and more for scientific discovery

## Reference

Rafael Ballester-Ripoll, Enrique G. Paredes, Renato Pajarola. Sobol Tensor Trains for Global Sensitivity Analysis. In arXiv Computer Science / Numerical Analysis e-prints, 2017, https://arxiv.org/abs/1712.00233
