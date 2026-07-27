---
unique_name: coffee_rating_prediction
name: Coffee_Data_CoffeeReview
checked_by:
- Lennart
- Mustafa
data_foundry_status:
- 'DF: Yes'
- BeyondArena
suggestion: 'Yes'
decision_markers:
- No Good Target (yet)
tags:
- Free Text (Sentences)
- Non-IID (Temporal)
collections:
- CARTE/TARTE
original_source: Website
year: '2023'
domain: business & marketing
required_split:
- Temporal (NON-IID)
problem_type: Regression
original_data_state: One Table
source_links:
- https://www.kaggle.com/datasets/hanifalirsyad/coffee-scrap-coffeereview
- https://www.coffeereview.com/
source_row: 481
type_adapter_id: curation-record-v1
---

## Comments

Just coffee reviews and features; est price needs adjustment and preprocessing, might have temporal drift due to review time; multiple descriptions, of which some are duplicated? All text as well which was used for parsing; kind of a well-defined task.

It seems the categories at the end make up the rating in total!

Could still be used for some kind of task, although it is unlikely it is close to any real tasks.

Maybe we could frame it as rating prediction only based on text, but this is closer to NLP than tabular based on the small amount of other information -> then it is a regression task, we could make it binary but that is wrong too.

CC (2026-07-27, Lennart): **Leak concern resolved -- verified against the curation notebook.** The category-score features (aroma, acid, body, flavor, aftertaste, with_milk) that sum to the rating are **dropped** in curation (`df.drop(columns=[... 'aroma','acid','body','flavor','aftertaste','with_milk' ...])`), along with desc_2/all_text (which leak award notes). Target is `rating` (regression); splits are temporal. So there is no circular leak in the shipped data -- `Yes` stands. Aligned `problem_type` -> Regression and `required_split` -> Temporal (NON-IID) to match the curated task.

## Reference

Kaggle
