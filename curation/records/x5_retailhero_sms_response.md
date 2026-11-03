---
unique_name: x5_retailhero_sms_response
name: 'X5 RetailHero: Uplift Modeling for Promotional Campaign (SMS campaign response of X5 loyalty-card customers)'
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 3
decision_markers:
- Needs extensive data wrangling
tags:
- AI-Filled (Verify)
original_source: Other
year: '2019'
domain: business & marketing
required_split:
- Random (IID)
problem_type: Binary Classification
original_data_state: Database (or multiple to-be-joined tables)
source_links:
- https://ods.ai/competitions/x5-retailhero-uplift-modeling
- https://huggingface.co/datasets/pytorch-lifestream/retailhero-uplift
- https://www.uplift-modeling.com/en/latest/api/datasets/fetch_x5.html
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 3: X5 Retail Group's RetailHero uplift competition (ODS.ai, 2019-2020): 200,039 loyalty-card clients of a randomised SMS campaign with a purchase-afterwards flag, 400,162 client profiles and 45.8M purchase rows before the campaign; a real targeting decision scored by uplift@30%, with the features still to build from the purchases.
- Source: the RetailHero hackathon "X5 RetailHero: Uplift Modeling for Promotional Campaign" on ODS.ai (December 17, 2019 to February 22, 2020): "X5 uses text messages to encourage customers to shop more ... The goal is to develop an algorithm that predicts whether or not we should send a text message to the client". scikit-uplift (`fetch_x5`): "The dataset is provided by X5 Retail Group at the RetailHero hackaton hosted in winter 2019"; `uplift_train.csv` 200,039 rows (`client_id`, `treatment_flg`: "information on performed communication", `target`: "customer purchasing", "if there was a purchase afterward"), `clients.csv` 400,162 rows (`client_id`, `first_issue_date`, `first_redeem_date`, `age`, `gender`), `purchases.csv` 45,786,568 rows ("Client purchase history before communication"), `products.csv` (about 43,000 rows), `uplift_test.csv` without labels; Hugging Face mirror pytorch-lifestream/retailhero-uplift (623 MB); no licence stated.
- Use case: X5's marketing team picks the clients to text, in the organiser's own words; fit direct for an uplift task (rank clients by the added purchase rate a text brings), approximate for plain response classification (the treatment as a feature). Regime IID: one randomised campaign with clients as units, as for `hillstrom_email_campaign`.
- Siblings and duplicates: `customer_personality_analysis` (`No`, AHDS: a mock case sample); `hillstrom_email_campaign` (`TBD -> Yes`, priority 3, a randomised e-mail test) and `orange_belgium_churn_uplift` (unscreened): other uplift sources, not duplicates (PROV-4); no other X5 record (`grep -il retailhero`). External collections: scikit-uplift ships it; none of our vocabulary.
- Better data: found as better data for `customer_personality_analysis`; no further search this round.
- Papers and pages: the ODS page, the scikit-uplift page and the Hugging Face card (read); top solutions not read.
- Metric: uplift@30% on the leaderboard ("The top 30% are selected from such a ranked list as the 'most promising' sub-sample. This sub-sample is used to estimate the average added conversion"): a competition metric (MET-4) that needs `treatment_flg` as a scoring column, never a feature (MET-2; a custom scorer, MET-13); with a response framing the fallback `roc_auc`. The curator's call, as on `hillstrom_email_campaign`.
- Risks for /add-dataset: features to aggregate from 45.8M purchase rows up to the campaign (`Needs extensive data wrangling`; the campaign date is not stated on the pages read, USE-3); only the 200,039 labelled clients ship; `age` outliers (not checked); the role of the treatment column (feature or scoring input).
- Priority: gap 0 (business, binary not thin), use case + (the organiser names the decision), source + (the organiser's competition page and field descriptions), shape + (200,039 clients with purchase history), risk - (heavy aggregation from the purchases table, and an uplift metric to settle).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through better data for `customer_personality_analysis`.
- as published: clients.csv 400,162 clients (general client info: loyalty-card issue and redeem dates, age, gender), purchases.csv 45,786,568 purchase rows of the clients' history before the SMS campaign, ...; target: target: the customer made a purchase after the campaign (binary), with treatment_flg (SMS sent or not); as in customer_personality_analysis, a response target ...; access: open.
- Why: Same task as customer_personality_analysis (who responds to the next campaign offer, from demographics and past purchase behaviour), with real data from a named retailer instead of the iFood case's mock sample of a hypothetical company. sklift: 'The dataset is provided by X5 Retail Group at the RetailHero hackaton ...
- Adds: About 90 times the customers (200,039 labelled vs 2,240), real, a randomised treatment/control split, raw purchase history before the campaign (features built at the prediction point). Caveats: the features must be aggregated from purchases.csv; the competition licence is not stated (HF mirror open, ODS needs login); ...
