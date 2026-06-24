---
unique_name: imdb_genre_prediction
name: imdb_genre_prediction
checked_by:
- Lennart
- Mustafa
- Alex
suggestion: 'No'
decision_markers:
- No Good Target  / Scientific Discovery
- Wrong Domain / Source Modality
- NLP (Text)
tags:
- Free Text (Sentences)
collections:
- TabSTAR
source_links:
- https://www.kaggle.com/datasets/PromptCloudHQ/imdb-data
source_row: 19
type_adapter_id: curation-record-v1
---

## Comments

genre is multi-categorical, the openml version of this data converts this into binary Genre_is_Drama

If genre_is_drama is used, it is clearly an NLP task to determine if the semantics are correct. Potentially connect it to actors and directors, but nothing that represents a good task. Could use some other task to create some kind of task
