---
unique_name: video_transcoding_time_prediction
name: video_transcoding
checked_by:
- Lennart
data_foundry_status: 'Yes'
suggestion: 'Yes'
decision_markers:
- Outdated
tags:
- Non-IID (Grouped)
collections:
- TabArena Reject
- TabSTAR
original_source: UCI
year: '2015'
domain: technology & internet
required_split:
- Grouped (NON-IID)
problem_type: Regression
usable_task_type: Predictive ML
given_task_type:
- Predictive ML
data_modality:
- Tabular
original_data_state: One Table
source_links:
- 10.24432/C58C9K
- openml 44974
source_row: 698
type_adapter_id: curation-record-v1
---

# video_transcoding

## Comments

CC: "Real data, preprocssed, information about decoding videos, the same video appears several times/ If the task is to predict new videos, either group split is required, or we need to make sure that random split does not introduce unwanted behaviour of models learning distribution shifts between videos"

"transcoding time prediction model"

Valid metadata use case / problem!

## Reference

@inproceedings{deneke2014video,
  title={Video transcoding time prediction for proactive load balancing},
  author={Deneke, Tewodors and Haile, Habtegebreil and Lafond, S{\'e}bastien and Lilius, Johan},
  booktitle={2014 IEEE International Conference on Multimedia and Expo (ICME)},
  pages={1--6},
  year={2014},
  organization={IEEE}
}
