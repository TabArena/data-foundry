---
unique_name: soybean
name: soybean
checked_by:
- Lennart
suggestion: TBD -> 2nd Tier
decision_markers:
- Data Quality Issue
tags:
- Tiny Data
collections:
- TabArena Reject
- TabSTAR
original_source: UCI
year: '1988'
domain: biology & life sciences
required_split:
- Random (IID)
problem_type: Multiclass Classification
original_data_state: Database (or multiple to-be-joined tables)
source_links:
- https://archive.ics.uci.edu/dataset/90/soybean+large
- https://doi.org/10.24432/C5JG6Z
- https://www.openml.org/search?type=data&id=42&sort=runs&status=active
source_row: 558
type_adapter_id: curation-record-v1
---

# soybean

## Comments

CC: "Some infrequent classes should not be used for prediction, may be outdated, maybe also rather an interpretability task, might require time split as date is available; categorical and nan values already preprocessed"

When looking more into the data there seems to be a major problem with the state of the data and which state we might want to use. Originally, there were 2 datasets, a train and a test split. The UCI data contains both, so in total 600ish samples. Moreover, there was a third small dataset. Some of these datasets have wrong values as explained in the metadata in the UCI files that were found, but no resolved version was ever uploaded as far as I can tell. It further seems that some of the train data features come from being fit on this data. The original data only has 5 features. 

In general, this is a large confusion and so far not worth integrating given the risk of using bad/wrong data.

## Reference

R.S. Michalski and R.L. Chilausky "Learning by Being Told and Learning from Examples: An Experimental Comparison of the Two Methods of Knowledge Acquisition in the Context of Developing an Expert System for Soybean Disease Diagnosis", International Journal of Policy Analysis and Information Systems, Vol. 4, No. 2, 1980.
