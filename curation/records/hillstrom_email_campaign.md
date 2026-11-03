---
unique_name: hillstrom_email_campaign
name: Kevin Hillstrom MineThatData E-Mail Analytics and Data Mining Challenge
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 3
tags:
- AI-Filled (Verify)
original_source: Website
year: '2008'
domain: business & marketing
required_split:
- Random (IID)
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://blog.minethatdata.com/2008/03/minethatdata-e-mail-analytics-and-data.html
- http://www.minethatdata.com/Kevin_Hillstrom_MineThatData_E-MailAnalytics_DataMiningChallenge_2008.03.20.csv
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 3: 64,000 customers of a randomized e-mail test with their visits, purchases and spend in the next two weeks; a real retailer's targeting decision, which the challenge framed as uplift.
- Source: Kevin Hillstrom, MineThatData, "E-Mail Analytics And Data Mining Challenge" (blog post, March 2008), CSV at minethatdata.com (3.96 MB). As published: "This dataset contains 64,000 customers who last purchased within twelve months", randomly split into three equal groups (Mens e-mail, Womens e-mail, no e-mail); header previewed: `recency, history_segment, history, mens, womens, zip_code, newbie, channel, segment, visit, conversion, spend`; outcomes are a website visit, a purchase and the dollars spent in the two weeks after the e-mail. One table; the retailer is not named.
- Use case: a multichannel retailer decides which customers go into the next e-mail campaign; the post asks which 10,000 customers to send the campaign to and which 10,000 to suppress. Fit approximate: the decision rests on the effect of the e-mail (uplift), while a plain classifier predicts the response with the arm `segment` as a feature. Regime IID (one randomized test, no dates).
- Siblings and duplicates: `marketing_campaign` (`Yes`, shipped: response to the next campaign, a SAS textbook table), `customer_conversion_dataset_for_stuffmart_com` (`No`, AHDS), `the_role_of_advertisement_on_the_consumer_behavior` (`No`); the run's other randomized-campaign candidates `x5_retailhero_sms_response` and `orange_belgium_churn_uplift` (other sources, not duplicates under PROV-4); no other Hillstrom record (`grep -il hillstrom/minethatdata`). External collections: the uplift library scikit-uplift ships it (`fetch_hillstrom`); none of our vocabulary.
- Better data: found as better data for `customer_conversion_dataset_for_stuffmart_com` and `marketing_campaign`, a related task next to `the_role_of_advertisement_on_the_consumer_behavior`; no further search this round.
- Papers and pages: the challenge post (eight questions; entries judged on insight and writing, prizes were books); a common test set of the uplift-modelling literature.
- Metric: none: the challenge set no scoring rule and judged written answers (the post); so the fallback `roc_auc` on the chosen response (MET-8). An uplift metric (Qini) would need the arm as a scoring column, never a feature (MET-2), the curator's call. Inputs none for the fallback.
- Risks for /add-dataset: one target to pick (`visit`, `conversion` or `spend`), the others dropped as outcomes (LEAK); `history_segment` is a binned copy of `history` (CLEAN); whether `segment` is a feature (response modelling) or the treatment of an uplift task; 2008 data with eight features.
- Priority: gap 0 (business and binary not thin), use case + (the post names the targeting decision), source + (the publisher's own post documents every field and the design), shape + (64,000 customers, mixed numeric and categorical, a randomized arm), risk - (the decision is an uplift question that a response target only approximates).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through better data for `customer_conversion_dataset_for_stuffmart_com`, `marketing_campaign`; a related task next to `the_role_of_advertisement_on_the_consumer_behavior`.
- as published: 64,000 customers who last purchased within twelve months, randomly split into three equal groups (Mens e-mail, Womens e-mail, no e-mail); outcomes tracked for two weeks after the campaign; 8 ...; target: visit or conversion (purchase) in the two weeks after the e-mail campaign (spend also given); access: open.
- Why: The same task as marketing_campaign (predict who responds to the next campaign's offer from the customer's purchase history and profile), with features of the same kind (recency, spend, product categories, channel). | the record's question (does advertising change what consumers do) asked on observed behaviour in a ...
- Adds: About 28 times the customers (about 42,700 e-mailed, 64,000 in all, against 2,240), a randomized campaign with a no-e-mail control, and a dated first publication instead of a SAS textbook table a curator suspected to be artificial. Trade-offs: older (2008), thinner features (8 against 27), an unnamed retailer, and ...
