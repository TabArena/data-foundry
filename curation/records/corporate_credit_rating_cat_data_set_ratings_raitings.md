---
unique_name: corporate_credit_rating_cat_data_set_ratings_raitings
name: CORPORATE_CREDIT_RATING_CAT Data Set Ratings Raitings
checked_by:
- Lennart
suggestion: 'Yes'
tags:
- Tiny Data
collections:
- TabSTAR
original_source: Website
year: '2016'
domain: finance
required_split:
- Random (IID)
problem_type: Multiclass Classification
original_data_state: One Table
source_links:
- https://www.openml.org/search?type=data&id=46372
- https://medium.com/@polanitzer/multiclass-classification-for-corporate-credit-ratings-using-credit-risk-analytics-book-by-harald-98d5940c745a
- https://github.com/Polanitz/Multiclass-Classification-for-Corporate-Credit-Ratings/blob/main/ratings.csv
- http://www.creditriskanalytics.net/datasets-private2.html
source_row: 786
type_adapter_id: curation-record-v1
---

# CORPORATE_CREDIT_RATING_CAT Data Set Ratings Raitings

## Comments

"This dataset is derived from the Credit Risk Analytics book by Harald, Daniel, and Bart, as described in the Medium article by Roi Polanitzer"
From teh book:
"The ratings data set is an anonymized data set with corporate ratings where the ratings
have been numerically encoded"?

Version from openml has 5k samples (so likely modifed). Original has 198
It was likely modifed by the Medium author (without saying it anyhwere, wow!)

unclear if a regression or classification task, likely classification (even if it is ordinal classification) due to ratings being categories officially

## Reference

@book{baesens2016credit,
  title={Credit risk analytics: Measurement techniques, applications, and examples in SAS},
  author={Baesens, Bart and Roesch, Daniel and Scheule, Harald},
  year={2016},
  publisher={John Wiley \& Sons}
}
