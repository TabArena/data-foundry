---
unique_name: facebook_comment_volume
name: Facebook Comment Volume
checked_by:
- Lennart
suggestion: TBD -> Yes
decision_markers:
- Data Quality Issue
- Needs extensive data wrangling
tags:
- Non-IID (Temporal)
collections:
- TabArena Reject
original_source: UCI
year: '2015'
required_split:
- Temporal (NON-IID)
problem_type: Regression
original_data_state: One Table
source_links:
- https://doi.org/10.24432/C5Q886
source_row: 619
type_adapter_id: curation-record-v1
---

# Facebook Comment Volume

## Comments

CC: ""TabM: time-split and leak needed

Predict how many comments a post will get based on features from the post; with custom feature engineering and temporal information""

https://www.stat.cmu.edu/~brian/valerie/617-2022/617-2021/project01/UCI%20ML%20data%20sets/facebook%20comment%20volume/published.pdf

" The task is to predict that how many comments that a post is expected to receive in
next H hrs. For this, we crawled the Facebook pages for raw
data, pre-processed it, and made a temporal split of the data
to prepare the training and testing set."

Page Features, Essential features are related to time intervals before the base time and are already aggregated (so grouped data no more), Weekday features (no timestamp?)


dataset comes in several forms with different base times selected

Training data is augmented: "Under the training set,
the vectorization process goes in parallel with the
variant generation process. Variant is defined as, how
many instances of final training set is derived from
single instance/post of training set. This is done by
selecting different base date/time for same post at
random and process them individually as described in
Figure 2. Variant - X, defines that, X instances are derived form single training instance"

Features are missing metadata details...hard to tell if we can reconstruct a dataset with our own splits

check for feature names: https://github.com/AmishaMurarka/Facebook-Comment-Volume-Prediction/blob/main/Facebook%20Comment%20Volume%20Prediction.ipynb

we could still use it with their official test splits and different training sets (with the augmentations). It has multiple test cases as well...

"base time" is only related to the delta from when the post was made, not the overall time.

## Reference

@INPROCEEDINGS{Sing1503:Comment,
AUTHOR='Kamaljot Singh and Ranjeet Kaur Sandhu and Dinesh Kumar',
TITLE='Comment Volume Prediction Using Neural Networks and Decision Trees',
BOOKTITLE='IEEE UKSim-AMSS 17th International Conference on Computer Modelling and
Simulation, UKSim2015 (UKSim2015)',
ADDRESS='Cambridge, United Kingdom',
DAYS=25,
MONTH=mar,
YEAR=2015,
KEYWORDS='Neural Networks; RBF Network; Prediction; Facebook; Comments; Data Mining;
REP Tree; M5P Trees.',
