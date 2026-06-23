---
unique_name: drugs_rating
name: drugs_rating
checked_by:
- Lennart
- Alex
- Mustafa
suggestion: TBD -> Yes
decision_markers:
- No Good Target (yet)
tags:
- Free Text (Short)
- New IID
collections:
- TexTabBench Extra
original_source: Website
year: '2022'
domain: medical & healthcare
required_split:
- Random (IID)
problem_type: Regression
usable_task_type: Predictive ML
given_task_type:
- Scientific Discovery
data_modality:
- Tabular
original_data_state: Other
source_links:
- https://www.kaggle.com/datasets/jithinanievarghese/drugs-side-effects-and-medical-condition
- https://www.drugs.com/
source_row: 596
type_adapter_id: curation-record-v1
---

# drugs_rating

## Comments

web scraped info about drugs, predict the rating;

rating is based on number or reviews (might need to be filtered or normalized for it) 

A lot of start information that can be used to gather more side information (e.g. chemical properties, druig html, ...)

side effects could also be deemed a big multi-categorical, but I will count it as free text here, also in side_effects some texts seem very similar but are not exact same because of different product name, generic_name is free text, I'm also on the edge when it comes to drug_classes being (multi-)categorical vs free text but counting it as free text here, brand_name is free text, medical_condition_description is categorical IMO and related_drugs is free text

Very borderline between multi categorical and free text, but not too close to sentences in most cases. but likley more sentences/text could be gathered from outside sources
