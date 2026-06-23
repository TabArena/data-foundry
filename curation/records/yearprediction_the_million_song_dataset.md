---
unique_name: yearprediction_the_million_song_dataset
name: YearPrediction The Million Song Dataset
checked_by:
- Lennart
suggestion: 'No'
decision_markers:
- Out-of-scope Task (CTR/RecSys/Ranking)
tags:
- Non-IID (Temporal)
collections:
- TabArena Reject
year: '2012'
source_links:
- https://www.openml.org/search?type=data&sort=runs&id=4352
- https://doi.org/10.24432/C50K61
- https://www.kaggle.com/datasets/ryanholbrook/the-million-songs-dataset
- https://www.kaggle.com/c/msdchallenge
source_row: 54
type_adapter_id: curation-record-v1
---

# YearPrediction The Million Song Dataset

## Comments

From Million Song Dataset Challenge. Song recommendation task. Clearly requires time split as songs & users change over time

"You should respect the following train / test split:
train: first 463,715 examples
test: last 51,630 examples
It avoids the 'producer effect' by making sure no song
from a given artist ends up in both the train and test set."

Unclear if this is a temporal task, it is much more a look-up task. Of course not real but reminds me a lot of certain game....

Real task was recsys

Otherwise, the version that created a different task are just fake / duplicates.
