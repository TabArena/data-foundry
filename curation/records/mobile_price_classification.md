---
unique_name: mobile_price_classification
name: Mobile_Price_Classification
suggestion: 'No'
decision_markers:
- AHDS (Artifical/Handmade/Deterministic/Simulated)
original_source: Kaggle
year: '2018'
required_split:
- Random (IID)
source_links:
- https://www.kaggle.com/datasets/iabhishekofficial/mobile-price-classification
type_adapter_id: curation-record-v1
---

# Mobile_Price_Classification

## Comments

Imported from the TabArena curation workbook.

TabArena curation verdict: Artificial/Simulated.

Crawled mobile phone data to predict the price. Likely need temporal split; Train/test split given, each ID appears 100 times in test data?; 

After post-hoc analysis: Artificial. Data was almost certainly artificially generated. 1) The RAM feature has 1562 unique values and is pretty uniformly distributed - RAM values of phones are actually pretty standardized. 2) RAM is highly correlated with the target and linear models perform best. 3) Round sample sizes (2k train, 1k test). 4) Binary features distributed almost 50/50. I.e. whether the phone has bluetooth, dual_sim, four_g, touch_screen, or wifi. 5) NNs much better than trees, indicating there is a deterministic function for the data.

Potential issue: maybe temporal; source missing

Lennart: Only time invariant features, seems reasonable otherwise

Andrej: Source unclear, split unclear,

## Reference

https://www.kaggle.com/datasets/iabhishekofficial/mobile-price-classification
