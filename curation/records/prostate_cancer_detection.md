---
unique_name: prostate_cancer_detection
name: NCI prostate cancer data
checked_by:
- Lennart
data_foundry_status:
- 'DF: Yes'
- BeyondArena
suggestion: No (Retired)
decision_markers:
- Data Quality Issue
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
- https://home.ccr.cancer.gov/ncifdaproteomics/ppatterns.asp
notebook_path: datasets/beyond_iid/new_iid/prostate_cancer_detection/prostate_cancer_detection.ipynb
source_row: 1036
type_adapter_id: curation-record-v1
---

## Comments

CC (2026-09-30, Lennart): **Retired: the label is readable from sample-processing artefacts, across the whole spectrum, and no batch IDs survive (crit. 4D).** 322 baseline-subtracted SELDI-TOF spectra (NCI JNCI set 7-3-02), label from four source folders: Benign PSA>4 (190), NED PSA<1 (63), PCa 4-10 (26), PCa >10 (43). 5-fold LightGBM AUC:
- The 109 channels below m/z 1 Da, where no ion can exist: cancer vs not 0.83; Benign vs NED (both "No") 0.99; Benign vs cancer with NED left out 0.92. The leak audit (2026-09-24) found 0.87 from m/z >= 2000 alone, so dropping channels does not help.
- The paper's own 7 features (m/z 2092, 2367, 2582, 3080, 4819, 5439, 18220; Petricoin et al. 2002, p. 1577), nearest channel or ±0.3%/±1% windows: cancer vs not 0.62-0.70, but Benign vs NED 0.92-0.97. Selecting them keeps the artefact and loses the label.
- Why: the NED group mixes sites. Petricoin et al. 2002, p. 1576: most sera come from a 1996 screening trial in Chile, plus 6 healthy NCI volunteers, 7 men sampled before and after prostatectomy, and "Twenty-five additional samples ... from the Simone Protective Cancer Institute (Lawrenceville, NJ)" (25 + 6 + 25 + 7 = 63, the NED folder). But Benign vs cancer (both from the trial) is also separable from noise, so the classes were processed differently.
- Baggerly, Morris & Coombes 2004 (Bioinformatics 20(5), on the same lab's ovarian sets, same format): baseline subtraction "is an irreversible nonlinear operation" (p. 780); the m/z grid (starting at -7.86E-05, as ours) is "the factory default calibration" (p. 783), i.e. uncalibrated; and structure at m/z 2.79 "is pure instrument artifact ... a systematic difference in the way the groups of samples were processed" (p. 784).

CC: "Link provided in the survey are outdated, I think I found another version. D: Downloadable under low resolution seldi-tof datasets. The number of csv files matches the number of samples so we just need to merge everything into one table. Classes are given in folder names"

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
