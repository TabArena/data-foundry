---
unique_name: video_game_fps_prediction
name: fps_benchmark
checked_by:
- Lennart
data_foundry_status:
- 'DF: Yes'
- BeyondArena
suggestion: No (Retired)
decision_markers:
- Trivial
- AHDS (Artifical/Handmade/Deterministic/Simulated)
tags:
- Non-IID (Grouped)
- Multi-target
collections:
- TabArena Reject
- TabSTAR
original_source: OpenML
year: '2020'
domain: technology & internet
required_split:
- Grouped (NON-IID)
problem_type: Regression
original_data_state: One Table
source_links:
- https://www.openml.org/d/44992
- https://github.com/svpeeters/performance_prediction
notebook_path: datasets/beyond_iid/grouped/video_game_fps_prediction/video_game_fps_prediction.ipynb
source_row: 699
type_adapter_id: curation-record-v1
---

## Comments

CC (2026-09-29, Lennart): **Retired: the target is a CPU × GPU lookup, and neither part of the source gives reliable ground truth (crit. 4C; 4B provisional).** We ship OpenML 44992, only the fpsbenchmark.com rows of the paper's dataset (OpenML 42737): a full grid of 19 CPUs × 27 GPUs × 24 games × 2 settings, every cell present once.
- On max settings, log FPS = game + CPU + GPU fits with R² 0.99998 (residual std 0.0017; 0.0012 with game × CPU and game × GPU terms, about the size of rounding FPS to 0.1). Real measurements would show CPU/GPU bottleneck interactions; there are almost none, so the values look like a site formula (game baseline × CPU factor × GPU factor), not benchmark runs. Hence AHDS as a provisional marker: no source states how fpsbenchmark produced its numbers.
- The grouped split holds out CPU+GPU pairs, but every test CPU and GPU is in train: a CPU + GPU lookup with no ML reaches R² 0.9999, LightGBM 0.995 without `HardwareConfigId` (leak audit, 2026-09-24).
- Peeters et al. 2021 (IDA, LNCS 12695) only assume the fpsbenchmark data is good: Sec. 4.1, p. 228: "the latter offers reliable assumingly expert-generated measurements only for recent hardware". It is their test set; their task is learning from the imprecise userbenchmark data.
- The userbenchmark rows are no alternative: Sec. 2, p. 225: "the measurements can neither be assumed to be independent nor identically distributed", and the FPS values are read off histograms with bins of 10 (OpenML 42737 description). That is a weak-supervision (interval target) problem, not a standard regression.

CC: "data of FPS from games with CPU and GPU and Game groups, data from fpsbenchmark.com (unreliable and fake info known to exist for some of the entries), mean of distribution is target. Might be a look-up task - need to define that term somewhere, I like it. If this is a real task, it might require group split by hardware or game. The grouping of CPUs and GPUs and Games might lead to some leak and do not show a real-world task"

Game groups also depend on setting, so we predict the FPS for one game across hardware and settings at once (as we have no such info beforehand?)

Need to check if we have the same CPUnames / GPUnames for all games or if there is such drift, otherwise need to remove it as well?

Two game settings (4 in the original data) that could be seen as a multi-target task, same for predicting it across games. But this also hopes to see generalization. Hard to tell what is better without more experiments

This could be treated as an IID task as well IMO, see long comment in data foundry about it.

## Reference

@inproceedings{peeters2021performance,
  title={Performance Prediction for Hardware-Software Configurations: A Case Study for Video Games},
  author={Peeters, Sven and Melnikov, Vitalik and H{\"u}llermeier, Eyke},
  booktitle={International Symposium on Intelligent Data Analysis},
  pages={222--234},
  year={2021},
  organization={Springer}
}
