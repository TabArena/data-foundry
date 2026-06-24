---
unique_name: book_price_prediction
name: BOOK_PRICE_PREDICTION
checked_by:
- Lennart
- Mustafa
suggestion: TBD -> Yes
decision_markers:
- No Good Target (yet)
tags:
- Free Text (Sentences)
- New IID
collections:
- TabSTAR
- AutoML_MM
original_source: Website
year: '2019'
domain: business & marketing
required_split:
- Random (IID)
problem_type: Regression
original_data_state: One Table
source_links:
- https://machinehack.com/hackathons/predict_the_price_of_books
- https://www.openml.org/search?type=data&id=46663
source_row: 595
type_adapter_id: curation-record-v1
---

## Comments

Book Price Prediction

Unclear how much price can be predicted and depends on the features, needs to be investigated. Plus unclear if text helps. Maybe price needs inflation adjustment? Could get more data from the internet for this? Unclear if it is a real task but was used as such in a competition.

has titles, authors, edition, genre, and category as entities but synopsis as sentences of free text

## Reference

Machinehack
