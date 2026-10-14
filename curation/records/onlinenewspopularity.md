---
unique_name: onlinenewspopularity
name: OnlineNewsPopularity
checked_by:
- Lennart
data_foundry_status:
- WIP (DF)
claimed_by: Lennart
suggestion: 'Yes'
decision_markers:
- Wrong Domain / Source Modality
- NLP (Text)
tags:
- Non-IID (Temporal)
collections:
- TabArena Reject
- TabSTAR
- AutoML_MM
original_source: UCI
year: '2015'
required_split:
- Temporal (NON-IID)
problem_type: Regression
source_links:
- https://doi.org/10.24432/C5NS3V
- https://www.semanticscholar.org/paper/A-Proactive-Intelligent-Decision-Support-System-for-Fernandes-Vinagre/ad7f3da7a5d6a1e18cc5a176f18f52687b912fea
- https://www.openml.org/search?type=data&id=46652&sort=runs&status=active
- https://www.openml.org/search?type=data&id=46662&sort=runs&status=active
v2_path: datasets/_dev/tabarena-v0pt2/onlinenewspopularity/dataset.py
source_row: 720
type_adapter_id: curation-record-v1
---

## Comments

CC: "Predict how often news were shared from statistics. Actually might be an NLP task, but could as well be still solved as a tabular data task; temporal impact as platform might grow over time. Some features are from LDA which likely introduced leaks making the dataset be unusable with random splits"

In TabArena was rejected due to text and temporal. But it might still be a valid task nowadays and is not that old. 

Might be a cool text-based task if we get the original text (or parts of it), plus using a subset of the features?
From researching, it seems the raw data is not published."

"we performed a
robust rolling windows evaluation of five state of the art models"
"For the prediction experiments, we adopted the rolling windows scheme with
a training window size of W = 10, 000 and performing L = 1, 000 predictions at each iteration. Under this setup, each classification model is trained
29 times (iterations), producing 29 prediction sets (each of size L). For defining
a popular class, we used a fixed value of D1 = 1, 400 shares, which resulted
in a balanced "popular"/"unpopular" class distribution in the first training set
(first 10, 000 articles)."

I think we cannot get the original text but this is still fine. It is not too old and it had some well made features that might even beat LLM preprocessing or be used next to it. Thus I think we can add it as a good temporal dataset!

**Assessment (AI, 2026-10-07):** Added as a temporal regression of log shares (9 two-week windows, Aug-Dec 2014, one-week gap), after the paper's rolling test sets of 1,000 articles (Sec. 3.1). UCI's `timedelta` and weekday flags follow a date 1-5 days after the publication date in the URL for 24% of the articles (Mashable's archived pages carry the URL date) and raise LightGBM's R² from 0.158 to 0.166: dropped. The LDA columns come from one model fitted on all texts and carry no signal: dropped. The keyword statistics of shifted articles include same-day articles published later (no measurable gain): kept with a note. Text-derived columns add 0.003 R². Binary framing (shares ≥ 1,400): ROC AUC 0.733 (paper: 0.73).

## Reference

A Proactive Intelligent Decision Support System for Predicting the Popularity of Online News
By Kelwin Fernandes, Pedro Vinagre, P. Cortez. 2015

Published in Portuguese Conference on Artificial Intelligence
