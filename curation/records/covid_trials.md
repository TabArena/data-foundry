---
unique_name: covid_trials
name: covid_trials
checked_by:
- Alex
- Mustafa
- Lennart
suggestion: 'No'
decision_markers:
- No Good Target  / Scientific Discovery
tags:
- Free Text (Sentences)
collections:
- TexTabBench Extra
original_source: GOV Website
year: '2021'
source_links:
- https://www.kaggle.com/datasets/parulpandey/covid19-clinical-trials-dataset?select=COVID+clinical+trials.csv
- https://clinicaltrials.gov/
source_row: 14
type_adapter_id: curation-record-v1
---

# covid_trials

## Comments

there is a CSV and multiple XML files, the XML files are supposed to contain more data, am looking at the csv here, which is also what the TextTabBench code used, could be worth it to maybe look into the specific XMLs and check whether the csv is essentially the sum of the XMLs

Some of the features have prefixes, which could be extracted as categories

very hard to see a meaningful predictive task in the data and the example notebook is very much just a data vis example

AP: Title, Interventions and Outcome measures seem to be good free text ones,  we can talk about some others which seem multi-categorical (e.g. Conditions, Sponsor/Collaborators) or uninformative for predicting the duration (e.g. Acronym), I'm also on the edge about Locations since some locations appear multiple times or one study can have multiple locations which would make it seem a bit multi-categorical, also you might want to preprocess locations in some way, but we would have to think about how exactly we would do this here since one study can have multiple locations
