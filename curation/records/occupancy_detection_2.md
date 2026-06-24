---
unique_name: occupancy_detection_2
name: Occupancy Detection
checked_by:
- Lennart
suggestion: TBD -> Yes
decision_markers:
- Time-series (Classification)
- Trivial
- Not Representative
tags:
- Non-IID (Temporal)
collections:
- TabArena Reject
year: '2016'
source_links:
- https://doi.org/10.24432/C5X01N
source_row: 618
type_adapter_id: curation-record-v1
---

## Comments

CC: "Predict if a room is occupied based on environmental features and date; 
might be temporal as we would like to forecast the future; 
date is just a number. time-series - ground truth available per minute, hence, temporal correlations almost certain. Is temporal task, but original splits are random"

I feel this task would become IID if we take large enough gaps from the readings such that temporal leakage/correlation between samples is missing. Readings are minute-wise, thus they are for sure too close.

"Two features combinations are good enough for high accuracies."

Has a clear train/test split, could be seen as generalizing to OOD and likely could only be used as one split in general (just one 50/50 split)


Only weekday (not more than the time) were used in modelling. Which seems a bit naive. It is fair to assume that if the model should generalize to other rooms, one would not want to use the weekday / time data? But this dataset clearly also is just for this one room.

The test data is before and after the train time, so they checked for both in the paper.

Unclear if this is a good task. Seems like a paper where they just wanted to show that it is possible and they did. Unclear if this is a real task otherwise....

## Reference

Accurate occupancy detection of an office room from light, temperature, humidity and CO2 measurements using statistical learning models
By L. Candanedo, V. Feldheim. 2016

Published in Energy and Buildings, Volume 112
