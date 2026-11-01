---
unique_name: facebook_recruiting_human_or_robot
name: 'Facebook Recruiting IV: Human or Robot? (Kaggle recruiting competition, online-auction bidders labelled robot or human)'
checked_by:
- AI (UNVERIFIED)
data_foundry_status:
- WIP (Triage)
claimed_by: Lennart
suggestion: TBD -> Yes
priority: 3
decision_markers:
- Needs extensive data wrangling
tags:
- AI-Filled (Verify)
original_source: Kaggle
year: '2015'
domain: business & marketing
required_split:
- Random (IID)
problem_type: Binary Classification
original_data_state: Database (or multiple to-be-joined tables)
source_links:
- https://www.kaggle.com/competitions/facebook-recruiting-iv-human-or-bot
- https://www.analyticsvidhya.com/blog/2015/07/top-10-kaggle-fb-recruiting-competition/
- https://github.com/keenborder786/AI-or-Bot-Filter
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 3: bidders of an online auction site labelled robot or human for removal, a Kaggle recruiting competition scored by ROC AUC; about 2,000 labelled bidders whose features must be built from a 7.6M-bid log, and half the labels are "stats-based".
- Source: Kaggle "Facebook Recruiting IV: Human or Robot?" (2015-04-27 to 2015-06-08, 983 teams; "The data in this competition comes from an online platform, not from Facebook"). As published: train.csv (bidder_id, payment_account and address "obfuscated to protect privacy", outcome), test.csv (bidders without labels), bids.csv ("7.6 million bids": bid_id, bidder_id, auction, merchandise, device, time "transformed to protect privacy", country, obfuscated ip and url); no bid amount ("a fixed increment of dollar amount for each bid"). Student reports count 2,014 train and 4,701 test lines and 1,910 humans against 104 robots (not counted here). Target `outcome`: "The outcome was half hand labeled, half stats-based": type 1 "identified as bots/fraudulent with clear proof. Their accounts were banned by the auction site", type 2 bidders whose "stats exceed from system wide average. There are no clear proof that they are bots" (Data page, read through the Kaggle API).
- Use case: the site owners, once a bidder has a bid history, decide whether to remove the account ("helping the site owners easily flag these users for removal from their site to prevent unfair auction activity", Description); fit direct for the banned half, approximate for the stats-based half; regime IID over bidders (one row per bidder, as the competition split; bid times are transformed and cover one short window).
- Siblings and duplicates: `shill_bidding_dataset` (TBD -> Yes, `Data Quality Issue`, labels from clustering) is another auction-fraud task on other data; no copy of this competition among the records (grep for human-or-bot, facebook recruiting). External collections: none found.
- Better data: found next to `shill_bidding_dataset` (a related task, per the run's assessment); no further search this round.
- Papers and pages: the Kaggle pages (Description, Data, Evaluation); the Analytics Vidhya top-10 write-up (private 0.92680); UCSD CSE158 student reports (2015); no paper.
- Metric: ROC AUC, "Submissions are judged on area under the ROC curve" (Evaluation page; API `evaluationMetric` "Area Under Receiver Operating Characteristic Curve"), the leaderboard metric (MET-4): `roc_auc`; inputs none.
- Risks for /add-dataset: half the positives are labelled by bid statistics above platform averages, which per-bidder aggregates can reproduce (SEL-5, TP-4: test a rule on bid counts and rates against the models); features have to be built by aggregating bids per bidder (`Needs extensive data wrangling`), with about 100 positives, some 20 per test fold (TP-5, TP-8); payment_account and address are obfuscated codes (ids, CLEAN); whether bids after the labelling are in the log cannot be told, since time is transformed (LEAK-2, cannot verify).
- Priority: gap 0 (business & marketing, binary, IID not thin), use case + (actor and decision named by the source), source + (the competition documents every field and the label), shape + (about 2,000 bidders, aggregates of categorical and count features), risk - (the stats-based half of the label, heavy aggregation).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through a related task next to `shill_bidding_dataset`.
- as published: Bidders as units: train.csv about 2,013 labelled bidders (reports give 2,014 lines with the header; bidder_id, obfuscated payment_account and address, outcome), test.csv about 4,700 bidders with ...; target: outcome: 1.0 the bidder is a robot, 0.0 a human (label definition on the Kaggle data page not read: the page needs JavaScript); access: registration.
- Why: The same actor and decision as shill_bidding_dataset (an auction platform flags fraudulent bidders from bid-behaviour aggregates), on another kind of bidder fraud; real platform labels rather than the shill set's labels derived by clustering, and a leaderboard metric (ROC AUC, per the Analytics Vidhya write-up of a ...
- Adds: A second auction-fraud task with labels from the platform and the raw bid log (7.6M bids) from which the features are built, instead of hand-crafted per-bidder scores on 807 eBay iPhone auctions. Caveats: about 2,000 labelled units only; a relational wrangle (bids aggregated per bidder, with leakage care across ...
