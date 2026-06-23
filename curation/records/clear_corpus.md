---
unique_name: clear_corpus
name: Clear Corpus
checked_by:
- Lennart
- Alex
- Mustafa
suggestion: 'No'
decision_markers:
- Wrong Domain / Source Modality
- NLP (Text)
collections:
- CARTE/TARTE
source_links:
- https://www.commonlit.org/blog/introducing-the-clear-corpus-an-open-dataset-to-advance-research-28ff8cfea84a/
- https://docs.google.com/spreadsheets/d/1sfsZhhP2umXXtmEP_NRErxLuwgN98TyH7LWOq3j07O0/edit?gid=971821388#gid=971821388
source_row: 192
type_adapter_id: curation-record-v1
---

# Clear Corpus

## Comments

try to predict readability of a passage based on stats and info

Last changed row might leak. Authors and similar might creates grouped data. Original kaggle competition (https://www.kaggle.com/competitions/commonlitreadabilityprize/data?select=test.csv) is almost just an NLP task. The data on the webiste contains a bunch of additonal features and ratings of externals. The extra data also includes some kind of model and algo predictions from Kaggle that are not super clear to me

Really seems to be just an NLP, top solutions used LLM and LMs
