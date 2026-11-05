---
unique_name: criteo_sponsored_search_conversion_log
name: Criteo Sponsored Search Conversion Log / Criteo-SSC (Criteo AI Lab)
checked_by:
- Andrej
suggestion: TBD -> 2nd Tier
decision_markers:
- Out-of-scope Task (CTR/RecSys/Ranking)
tags:
- Two-Regime Zeros
- Non-IID (Temporal)
original_source: Company
year: '2018'
domain: business & marketing
required_split:
- Temporal (NON-IID)
problem_type: Regression
original_data_state: One Table
source_links:
- https://ailab.criteo.com/criteo-sponsored-search-conversion-log-dataset/
- http://go.criteo.net/criteo-research-search-conversion.tar.gz
- https://arxiv.org/abs/1806.08211
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. Drafted by an AI assistant on 2026-10-20 from a web search for zero-inflated regression candidates, the source pages and, where the notes say so, the downloaded data. A human must verify the suggestion, the metadata and the notes before relying on them.**

**Screening (AI, 2026-10-27):** `No` (`Out-of-scope Task (CTR/RecSys/Ranking)`, SEL-9 read under SEL-2): a log of clicks
on sponsored product ads that Criteo published for conversion modelling; in practice the prediction is a real-time bid
per ad click from a log of ids and hashes, the task of the TalkingData precedent, so the call rests on how the
prediction is made and on that precedent, not on the word "CTR".
- Source: Criteo AI Lab, "Criteo Sponsored Search Conversion Log", post of 03 Jan 2018
  (https://ailab.criteo.com/criteo-sponsored-search-conversion-log-dataset/): "Each row in the dataset represents an
  action (i.e. click) performed by the user on a product related advertisement"; labels `Sale`, `SalesAmountInEuro` and
  the click-to-conversion delay; features: click time, past-week clicks, product price, age group, device, audience id,
  gender, brand, seven categories, country, and product, title, partner and user ids; 6.4 GB uncompressed; CC BY-NC-SA
  4.0. The download link redirects to a Criteo storage blob the earlier AI triage found unreachable (2026-10-20); no
  mirror on Hugging Face (searched 2026-10-27).
- Use case: the page lists "Conversion rate modeling in sponsored search advertising", "Modeling the expected conversion
  revenue in sponsored search", survival models of the click-to-conversion delay and "Offline metrics for conversion
  prediction tasks"; Criteo bids "such that the bids are based on each user's likelihood to make a purchase" (same page,
  the aim of Criteo Predictive Search). Tallis and Yadav 2018 (Criteo, arXiv 1806.08211), Sec. 1, p. 1: "an effective
  advertisement bidding strategy requires determining the probability that an advertisement click will originate a
  conversion"; Sec. 4, p. 4: "To train models for predicting conversion probabilities we label each event with the event
  outcome." The revenue target is the value side of the same per-click bid.
- Siblings and duplicates: the like case is `talkingdata_adtracking_fraud_detection_challenge` (No, `Out-of-scope Task
  (CTR/RecSys/Ranking)`, Lennart), whose `is_attributed` is a post-click app download on an ad-click log of ids;
  `albert` (Criteo display clicks, No, Lennart) is the same family. Unlike cases, all `Yes`:
  `homesite_quote_conversion`, `bank_marketing` and `in_vehicle_coupon_recommendation`, response tasks on customer
  attributes, not on an ad-click log. External collections: none found; OptDist (Weng et al. 2024, CIKM, arXiv
  2408.08585) uses the revenue for customer lifetime value with a random 7:1:2 split (earlier AI triage).
- Metric: Tallis and Yadav score conversion models by a log-loss uplift (Sec. 5-6); no metric for the revenue.
- For the curator: putting post-click conversion on an ad-click log in scope would be an amendment of SEL-9, and it
  would reopen `talkingdata_adtracking_fraud_detection_challenge`.
- Reject check (AI, 2026-10-27): stands. SEL-9 (Must). Each row is a click on a product ad and the conversion it led to,
  logged with ids and hashes for Criteo's per-click bidding, as TalkingData's post-click downloads
  (https://ailab.criteo.com/criteo-sponsored-search-conversion-log-dataset/).

**Consistency check (AI, 2026-10-30):** the review page sets 2nd Tier (no note, no priority). Policy question 7 of the
same review left criteo's `No` on SEL-2 and the TalkingData precedent
(`talkingdata_adtracking_fraud_detection_challenge`, Lennart, `No`). What sets criteo apart from TalkingData? Options:
keep `No`; 2nd Tier with that fact and a priority; or reopen TalkingData and SEL-9's wording.

CC (2026-10-30, Andrej): `TBD -> 2nd Tier` (the AI screening had `No`; zero-inflated screening review page, after the
AI's consistency check). "I simply disagree that CTR is out of scope. Keep 2nd tier."

Criteo AI Lab's sample of 90 days of Criteo Predictive Search traffic: one row per click on a product ad, with `Sale`,
`SalesAmountInEuro`, `time_delay_for_conversion`, the click timestamp, product price, age group, gender, brand, seven
undisclosed categories, country, product, partner and user ids, a hashed title, device and an undisclosed audience id.
OptDist (Weng et al. 2024, Table 1, p. 7) counts 15,995,633 clicks with 1,150,996 conversions (7.20%), so 92.8% zero
revenue, and splits them randomly 7:1:2 (Sec. 4.1.1, p. 6). Not measured: the download link redirects to an Azure
storage account that no longer resolves (2026-10-20), and no mirror turned up on Hugging Face or Kaggle.

No: the source task is post-click conversion prediction for ad bidding, the CTR family that criterion 3 excludes.
Tallis & Yadav (2018), Sec. 1, p. 1: "an effective advertisement bidding strategy requires determining the probability
that an advertisement click will originate a conversion"; Sec. 4.3, p. 4: "we label each event with the event
outcome. That is whether that event originated in a conversion or not". The revenue target OptDist uses is the value
side of the same per-click bid, and most features are ids and hashes (user, product, partner, title), as in `albert`
(Criteo display clicks, No). Kept anyway, it would need a temporal split by click time, not OptDist's random one.
Licence: CC BY-NC-SA 4.0 (dataset page).

## Reference

Tallis M., Yadav P. (2018). Reacting to Variations in Product Demand: An Application for Conversion Rate (CR)
Prediction in Sponsored Search. arXiv:1806.08211.

Weng Y., Tang X., Xu Z., Lyu F., Liu D., Sun Z., He X. (2024). OptDist: Learning Optimal Distribution for Customer Lifetime Value Prediction. CIKM '24.
arXiv:2408.08585.

Lead: web search 2026-10-20 for zero-inflated regression candidates (not in the v4 workbook).
