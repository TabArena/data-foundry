---
unique_name: onlinenewspopularity
name: OnlineNewsPopularity
checked_by:
- Lennart
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
year: '2015'
source_links:
- https://doi.org/10.24432/C5NS3V
- https://www.semanticscholar.org/paper/A-Proactive-Intelligent-Decision-Support-System-for-Fernandes-Vinagre/ad7f3da7a5d6a1e18cc5a176f18f52687b912fea
- https://www.openml.org/search?type=data&id=46652&sort=runs&status=active
- https://www.openml.org/search?type=data&id=46662&sort=runs&status=active
source_row: 720
type_adapter_id: curation-record-v1
---

# OnlineNewsPopularity

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

## Reference

A Proactive Intelligent Decision Support System for Predicting the Popularity of Online News
By Kelwin Fernandes, Pedro Vinagre, P. Cortez. 2015

Published in Portuguese Conference on Artificial Intelligence
