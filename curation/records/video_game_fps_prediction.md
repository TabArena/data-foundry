---
unique_name: video_game_fps_prediction
name: fps_benchmark
checked_by:
- Lennart
data_foundry_status: 'Yes'
suggestion: 'Yes'
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
- openml 44992
- https://github.com/svpeeters/performance_prediction
source_row: 699
type_adapter_id: curation-record-v1
---

# fps_benchmark

## Comments

CC: "data of FPS from games with CPU and GPU and Game groups, data from fpsbenchmark.com (unreliable and fake info know to exist for some of the entires), mean of distribution is target.Might be a look-up task - need to define that term somewhere, I like it. if this is a real task, it might require group split by hardware or game. the grouping of CPUs and GPUs and Games might lead to some leak and do not show a real-world task"

Game groups also depend on setting, so we predict the FPS for a one game across hardware and settings at once (as we have no such info beforehand?)

Need to check if we have the same CPUnames / GPUnames for all games or if there is such drift, otherwise need to remove it as well? 

Two game settings (4 in the original data) that could be seen as a multi-target task, same for predicting it across games. But this also hopes to see generalization. hard to tell what is better without more experiments

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
