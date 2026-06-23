---
unique_name: women_clothing_review
name: women_clothing_review
checked_by:
- Lennart
- Alex
- Mustafa
suggestion: 'No'
decision_markers:
- Wrong Domain / Source Modality
- No Good Target  / Scientific Discovery
- NLP (Text)
collections:
- TabSTAR
source_links:
- https://www.kaggle.com/datasets/nicapotato/womens-ecommerce-clothing-reviews/
- https://arxiv.org/abs/1805.03687
source_row: 193
type_adapter_id: curation-record-v1
---

# women_clothing_review

## Comments

E-commerce reviews, some anonymization was applied, the company names have been replaced by "retailer"

Unclear how much NLP vs tabular, very much on the NLP side given its current set of features.

Might need to filter by clothing ID / subgroup of the rating and filter rating of other people. Also weird task to check if the task was recommended as this would have been written in the text most likely and could be parsed, no need to learn across samples.

It seems much closer to a sentiment classification task than something predictive ML. Needs some thought to see if we want to support more.

In the paper, they either try to predict the sentiment classification created automatically by another toolkit (thus a bad target).

Or they try to predict whether review text is a recommendation or not just on the text (no other tabular features, moreover most other tabular features would clearly leak the recommendation)
This removes the only potential good targets, and we are left with nothing, so it is an NLP task clearly

Review text is long free text, but we might also want to count title as free text, data has been anonymized, references to company have been renamed to "retailer"
