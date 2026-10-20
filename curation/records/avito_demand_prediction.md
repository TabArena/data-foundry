---
unique_name: avito_demand_prediction
name: Avito Demand Prediction Challenge (Kaggle 2018, deal_probability)
checked_by:
- AI (UNVERIFIED)
suggestion: 'No'
decision_markers:
- No Good Target (yet)
tags:
- AI-Filled (Verify)
- Two-Regime Zeros
- Non-IID (Temporal)
- Free Text (Sentences)
original_source: Kaggle
year: '2018'
domain: business & marketing
required_split:
- Temporal (NON-IID)
problem_type: Regression
source_links:
- https://www.kaggle.com/competitions/avito-demand-prediction
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. Drafted by an AI assistant on 2026-10-20 from a web search for zero-inflated regression candidates, the source pages and, where the notes say so, the downloaded data. A human must verify the suggestion, the metadata and the notes before relying on them.**

Avito's 2018 Kaggle competition: 1,503,424 Russian classified ads posted 15-28 March 2017 by 771,769 sellers, with
title and description, price, location, Avito's category and parameter codes, an image and Avito's image class
`image_top_1`; the supplementary tables of unlabelled ads (17 GB) were not downloaded. The target `deal_probability`
(RMSE) is "the likelihood that an ad actually sold something. It's not possible to verify every transaction with
certainty, so this column's value can be any float from zero to one" (data page); the threads asking how it is computed
(discussions 55299, 55922, 56533) got no answer from Avito or Kaggle. Measured: 64.8% exact zeros, 18,407 distinct values, single values shared by
tens of thousands of ads (0.80323 on 46,683), and 88% of the positive values occur in one parent category only, as
discussion 58948 found. It reads as the output of an undocumented Avito scoring step, not an observed outcome
(criterion 3), so the zero mechanism cannot be confirmed.

Modality does not decide it: on a temporal split (train 15-25 March, test 26-28 March), untuned LightGBM on the
tabular columns gives RMSE 0.2264 (mean predictor 0.2597), ROC AUC 0.81 for a non-zero value and R^2 0.29 on log1p
among positives; the image class brings RMSE to 0.2254 and a TF-IDF SVD of the text to 0.2238. Test labels were never
released. Terms: the data may be used "only for the purposes of the Competition" (rules). Other Avito competitions in
the log: `avito_context_ad_clicks` (CTR), `huntprohibited`. To check: whether Avito documented the target anywhere,
which would reopen the case.

## Reference

Avito Demand Prediction Challenge. Kaggle competition hosted by Avito, 2018.
https://www.kaggle.com/competitions/avito-demand-prediction.

Lead: web search 2026-10-20 for zero-inflated regression candidates (not in the v4 workbook).
