---
unique_name: avito_demand_prediction
name: Avito Demand Prediction Challenge (Kaggle 2018, deal_probability)
checked_by:
- Andrej
suggestion: TBD -> 2nd Tier
priority: 2
decision_markers:
- No Good Target (yet)
- Out-of-scope Task (CTR/RecSys/Ranking)
tags:
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
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. Drafted by an AI assistant on 2026-10-20 from a web search for zero-inflated regression candidates, the source pages and, where the notes say so, the downloaded data. A human must verify the suggestion, the metadata and the notes before relying on them.**

**Screening (AI, 2026-10-27):** `TBD -> 2nd Tier`, priority 2: Avito names the use (tell a seller what interest to
expect when the ad is posted), but `deal_probability` is a probability Avito estimated by an undocumented method, not an
observed sale; under USE-5 that makes the fit approximate, not a fast reject.
- Source: Avito's Kaggle competition, 2018-04-24 to 2018-06-27 (Kaggle API: "Predict demand for an online classified
  ad"); files train.csv (0.95 GB), test.csv, periods files, 8.5-9.2 GB of unlabelled ads (`train_active`, `test_active`)
  and over 50 GB of images (Kaggle API file list). 1,503,424 ads of 15-28 March 2017, `deal_probability` 0 for 64.8%
  (earlier AI triage, 2026-10-20, measured).
- Use case: "With this information, Avito can inform sellers on how to best optimize their listing and provide some
  indication of how much interest they should realistically expect to receive" (overview, as mirrored; the Kaggle page
  does not render here): Avito, at posting, advises the seller. The target, data page as quoted by the earlier AI: "the
  likelihood that an ad actually sold something. It's not possible to verify every transaction with certainty, so this
  column's value can be any float from zero to one"; the welcome thread (topic 55299) asks how it is made and gets no
  answer, and Kaggle's Wendy Kan writes there "Logloss won't work if the ground truth isn't 0/1". Fit approximate
  (USE-5, USE-8). Regime temporal by posting date (SPLIT-6).
- Siblings and duplicates: `huntprohibited` (Yes, Avito's 2014 ad moderation) and `avito_context_ad_clicks` (No, CTR)
  are other Avito tasks on other data. External collections: none found.
- Papers and pages: the 2nd and 3rd place write-ups (topics 59871, 59885); thread 58948 on the target's values (earlier
  AI triage).
- Metric: RMSE (Kaggle API, "Root Mean Squared Error") on `deal_probability`, the leaderboard metric (MET-4); inputs
  none.
- Risks for /add-dataset: the label (single values shared by tens of thousands of ads, 88% of positive values in one
  parent category, earlier AI); text and images carry part of the signal (RMSE 0.2264 on the tabular columns, 0.2238
  with a text SVD, mean predictor 0.2597, earlier AI; SEL-12 leans tabular); Russian text; `No Good Target (yet)` kept
  as the open concern; open family question: coded zeros (whether a 0 means no sale seen or a floor of Avito's score is
  unknown).
- Priority: gap 0 (business & marketing), use case 0 (named, but the fit is approximate), source + (Avito's data page),
  shape + (1.5M ads, mixed types, dated), risk - (undocumented target).

**Assessment (AI, 2026-10-30):** The family's open question on coded and censored zeros is settled (Andrej, 2026-10-30,
policy question 2 of the zero-inflated review: "We don't care. We want to add any relevant predictive task, independent
if it is zero inflated or not"), so how the source codes its zeros is no reason for a No or a lower priority. Whether a
0 is no sale or a floor of Avito's score no longer counts against the record; the undocumented target (USE-5) remains
the open concern, so the verdict and priority stay.

CC (2026-10-30, Andrej): `Yes`, priority 4 (the AI screening had `TBD -> 2nd Tier`, priority 2; zero-inflated screening
review page).

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

**Assessment (AI, 2026-11-01):** added as `datasets/_dev/tabarena-v0pt2/avito_demand_prediction_1m/` by /add-dataset with the full review panel; the open questions are in its `REVIEW.md`. Recommend shipping; only the SEL-3 call on Avito's undocumented deal score can turn it to `No` (its issue 1; of 983 groups of identical reposts with a positive ad, 859 carry different labels, so the label follows each ad). `user_id` ships as a categorical. The 2026-10-20 scores above (RMSE 0.2264 and 0.2238, AUC 0.81) were on another split and are superseded by the definition's. Priority 2: gap 0, use case 0 (fit approximate), source +, shape +, risk - (SEL-3 open).

CC (2026-11-02, Andrej): the SPLIT-10 amendment for labels that mature longer than the training floor allows is not adopted (issue 4): SPLIT-10 stays as written, and each no-gap departure for SPLIT-14's floor (avito's issue 2, pricing_game_2016_french_fleet, wisconsin_local_government_property_insurance_fund) is decided as an exception of its own.

CC (2026-11-03, Andrej): don't ship for now, 2nd Tier (avito_demand_prediction_1m): "Since this is recsys/CTR, we move it to 2nd tier for now. Also, add the click prediction tag". The vocabulary has no click-prediction tag; the marker `Out-of-scope Task (CTR/RecSys/Ranking)` is added as its closest entry. The v2 folder left the working copy; its last definition is in the run folder of 2026-11-03, the committed one in 902011b3.

## Reference

Avito Demand Prediction Challenge. Kaggle competition hosted by Avito, 2018.
https://www.kaggle.com/competitions/avito-demand-prediction.

Lead: web search 2026-10-20 for zero-inflated regression candidates (not in the v4 workbook).
