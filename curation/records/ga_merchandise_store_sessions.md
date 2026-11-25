---
unique_name: ga_merchandise_store_sessions
name: Google Analytics sample dataset for BigQuery (Google Merchandise Store, obfuscated GA360 sessions)
checked_by:
- AI (UNVERIFIED)
- Andrej
data_foundry_status:
- WIP (Triage)
claimed_by: Andrej
suggestion: TBD -> Yes
priority: 3
tags:
- AI-Filled (Verify)
- 'Samples: Over Time'
- 'Time: Dated'
- 'Target: Fixed Delay'
- 'Entities: Recur'
- Dated Event Log
original_source: Company
year: '2018'
collection_period: Aug 2016 - Aug 2017
domain: business & marketing
required_split:
- Temporal (NON-IID)
problem_type: Binary Classification
source_links:
- https://support.google.com/analytics/answer/7586738
- https://www.kaggle.com/competitions/ga-customer-revenue-prediction
v2_path: datasets/_dev/tabarena-v0pt2/ga_merchandise_store_sessions/dataset.py
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-11-25):** `TBD -> Yes`, priority 3: Google's obfuscated GA360 export of the Merchandise Store (903,653 visits, 2016-08-01 to 2017-08-01) whose hits let each visit be cut at its 3rd pageview, before any checkout step: 306,997 visits, 3.7% buy, LightGBM 0.874 against logistic regression 0.856 on a forward split by month (measured 2026-11-25 in BigQuery); the in-visit purchase task is ours to define, and it is distinct from `google_analytics_customer_revenue_prediction` (PROV-7). Deep pass; it corrects the 2026-10-31 screening where marked.
- Source: Google, "Google Analytics sample dataset for BigQuery" (`bigquery-public-data.google_analytics_sample.ga_sessions_*`, one table per day), announced on Google's blog on 2018-03-30 ("Introducing the Google Analytics Sample Dataset for BigQuery", D. Aujla: data "from the Google Merchandise Store, an Ecommerce site that sells Google branded merchandise", to "learn or teach practical experience with analyzing analytics data in BigQuery"); help page https://support.google.com/analytics/answer/7586738: "obfuscated Google Analytics 360 data", fullVisitorId obfuscated, clientId, adWordsClickInfo and parts of geoNetwork removed ("Not available in demo dataset"). First publication 2018 (PROV-8, PROV-9; the Kaggle competition of 2018-09 reused it), so `year` 2018 and `collection_period` Aug 2016 - Aug 2017 are set (both were empty). As published: one row per visit with nested `hits` (each hit timed, with page path, type and Enhanced Ecommerce action), `totals`, `trafficSource`, `device`, `geoNetwork`. Measured 2026-11-25 in BigQuery: 903,653 visits (the old block's "about 0.9 M, from memory" is confirmed; the same 903,653 as Kaggle's v1 train.csv) of 714,167 users. Country is set for 99.9% of the cut visits (61% United States), so geoNetwork is only partly removed.
- Use case: the store's site, during a visit that has not reached checkout, decides at the visitor's 3rd pageview whether to intervene (an offer, a discount, a cart reminder, a chat prompt) from what it knows then: traffic source and medium, device, browser, country, visit number, and the visit's first three pages (hits, events, seconds on site, distinct pages, product-list clicks, product detail views, cart adds and removes, basket, account, category and search pages); label: the visit later records a transaction. The setting of `online_shoppers_purchasing_intention_dataset` (Sakar et al. 2019), with a prediction point inside the visit that the old data cannot give. Fit approximate: Google publishes the sample for learning BigQuery, names no task, and the prediction point (3rd pageview; a time cut is the alternative) is ours. Collection: `Samples: Over Time`, `Time: Dated` (a date and a start time per visit, hit times within it), `Target: Fixed Delay` (the purchase closes the visit the features describe, as `online_shoppers` recorded in its issue 4), `Entities: Recur` (fullVisitorId; 33% of cut visits belong to users with several); type `Dated Event Log` (each row a visit with its date; most users have one visit, so not panel data, SPLIT-34).
- Split: leaf L-ORDER.windows (Temporal · windows on the time key) because the model meets visits after the data (LOG.meets), each visit is dated (ORDER.order), and 12 months give three monthly test windows each training on at least 70% (ORDER.windows: May, June, July 2017 test 24,578, 22,594 and 25,146 visits on 233,719 to 280,891 earlier ones), and the table is large (ORDER.small no); no gap, the label arrives within the visit. Open: the prediction point; whether returning users across the cutoff stay (measured today: 9.3% to 9.9% of a test month's cut visits come from a user seen in an earlier month, and they buy at 9.7% to 11.2% against 3.4% to 3.8% for new users; the shop knows its returning visitors and `visitNumber` is a feature, SPLIT-13); the 1-day August 2017 table (2017-08-01) as its own month or merged.
- Siblings and duplicates: `google_analytics_customer_revenue_prediction` (`Yes`, priority 2, Andrej 2026-10-30) uses the same sessions for another task: ln(1 + each user's summed revenue) in a 62-day window after a 46-day gap, from user features of an earlier window (regression, one row per user, 131 and 138 buyers per window, an all-zero submission 0.88843 against the winner's 0.88140). This record is one row per visit, cut inside the visit, binary, for an on-site decision during the visit. Different unit, target, prediction moment and decision, so not a duplicate: PROV-7 ("Records that share a source but give different tasks are not duplicates"), like `parkinsons_biomedical_voice_measurements` and its telemonitoring sibling (one source, detection and progression) and `lung_cancer` / `lung_adenocarcinoma_metastasis`. It is not PROV-6's "swapped target" either: the session label is not a column of the revenue table but needs another row unit and a cut the revenue task never makes, and the revenue task's own note says a visit's own pageviews give its purchase away (AUC 0.98), which is exactly what the cut removes here. The two records share users and sessions; if both ship, the comments of each say why they are distinct (PROV-7). Also: `online_shoppers_purchasing_intention_dataset` (`Yes`, shipped; another store, Sakar et al. 2019, PROV-4 another source; its issue 7 of 2026-11-25 recommends keeping it until this record replaces it); `online_shoppers_purchase_intention` (`No`, Duplicate of that); `customer_propensity_to_purchase_dataset` (`No`, generated), `customer_acquisition_data` (`No`, untraceable). No other record names the GA sample (searched google_analytics_sample, merchandise store, gstore, ga_sessions). External collections: none found.
- Better data: found as better data for `online_shoppers_purchasing_intention_dataset` (45 times its usable visits, 12 months against 7, and a prediction point inside the visit). Nothing better found for this one: in the same check (2026-11-25, measured) Google's GA4 sample of the same store has 107,670 cut visits over 3 months and LightGBM below logistic regression (0.712 against 0.727); YooChoose (RecSys 2015) has no page type, device or source (0.627); REES46 cosmetics logs a quarter of purchases in sessions of their own (broken session label); Retailrocket has no session id and loses 9,463 of 14,297 buying sessions at the cut; Diginetica (CIKM Cup 2016) is smaller and was not read. A version of this source: Kaggle's v2 files (train_v2 25.4 GB, test_v2 7.6 GB, Aug 2016 to Oct 2018, with hits as JSON) add 15 months of the same store (PROV-6: one record, not a new one); not read.
- Access: BigQuery needs a Google account and a project (the BigQuery sandbox's free tier, 1 TB of queries a month; the cut scans about 0.3 GB). Kaggle is no account-free route either: it needs a Kaggle account and acceptance of the competition's rules (non-commercial use). Kaggle v1 train.csv has the same visits but no hits, so it cannot be cut. Kaggle v2 has hits, but whether they are complete and match BigQuery's hit for hit was not checked, so a definition reads BigQuery (the first publication), and v2 stays an unchecked alternative copy and a possible extension to 27 months. Licence: none stated on the help page (viewer access for all users; Google's Terms of Service); Kaggle's copy under the competition's rules.
- Papers and pages: Google's help page and blog post (read 2026-11-25); the Kaggle competition "Google Analytics Customer Revenue Prediction" (2018-09-13 to 2019-02-21; discussions 68353, 81531, 82614 per the sibling record); no paper on an in-visit purchase task on this sample found in this pass. The in-visit setting follows Sakar et al. 2019 (Neural Computing and Applications) on `online_shoppers`.
- Metric: none from the source for this task (Google's sample defines no task; the competition scored RMSE on per-user log revenue, the sibling's task), so the binary fallback `roc_auc` (MET-1), as `online_shoppers` uses; inputs none.
- Risks for /add-dataset: never ship the finished-visit totals (`totals.pageviews`, `hits`, `timeOnSite`, `transactions`, revenue): with them LightGBM reaches 0.977 (0.932 from final pageviews alone) against 0.874 at the cut (measured 2026-11-25; LEAK-10); drop visits with a checkout step before the cut (264 of 307,261) and check that the funnel pattern (checkout actions 5, 6, 8, a transaction id, or a checkout page path) catches every checkout page; 634 cut rows are visits split at midnight (317 pairs with one visitId over two dates), to merge or drop; ids are obfuscated and some fields removed (PROV-3 does not apply: the values are the store's, only ids and fields are masked); whether Google drew the sample at random is unknown (12th-place write-up, per the sibling); nested hits to flatten (done in SQL, scripts kept in the evidence of `online_shoppers` issue 7).
- Priority: gap 0 (business & marketing, binary and temporal are not thin), use case 0 (ours: Google names no task; fit approximate), source + (Google's documented export and announcement), shape + (306,997 visits, mixed types, 12 dated months). Risk 0: the old block's minus (totals after the purchase, a leak history, a target window to construct) is answered by the cut, measured today; the leak of the competition's first round concerns test revenue after Aug 2017, not these labels. Changed from priority 2.
- Corrected against the 2026-10-31 screening: the rows (measured, not from memory), the year (2018, Google's release, was empty), the collection period, the use case and fit (the in-visit task, not the competition's), the risk point (the cut removes the totals leak), and the sibling: the revenue record is a distinct task under PROV-7, which the old block did not compare.

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 2: Google's obfuscated GA360 export of a real online store, the data of a Kaggle Featured competition (2018-2019, 3,611 teams) scored on per-customer revenue by RMSE; real and large, but the first round's test revenue could be read from Google's public demo account, ids are obfuscated, and the session-level purchase task the scouts propose is ours to define.
- Source: Google, "Google Analytics sample dataset for BigQuery" (bigquery-public-data.google_analytics_sample.ga_sessions_*): "obfuscated Google Analytics 360 data from the Google Merchandise Store", with example queries "for the period of 1-Aug-2016 to 1-Aug-2017"; "Data for some fields have been obfuscated such as fullVisitorId", others "removed such as clientId, adWordsClickInfo and geoNetwork"; the stated purpose is "exploring the benefits of exporting Google Analytics 360 data into BigQuery" (https://support.google.com/analytics/answer/7586738). Reused in Kaggle's "Google Analytics Customer Revenue Prediction" ("Predict how much GStore customers will spend"; opened 2018-09-13, deadline 2019-02-21, per the Kaggle API). As published there: train.csv (1.5 GB) and test.csv (1.3 GB), then, after the relaunch, train_v2.csv (25.4 GB, with hit-level JSON) and test_v2.csv (7.6 GB); one row per session with JSON columns (device, geoNetwork, totals, trafficSource, hits); row counts not read (about 0.9 M sessions in train.csv, from memory).
- Use case: the competition's: predict each customer's revenue in a later window, for the store's marketing spend (the Overview page needs JavaScript and was not read; the API description says only "Predict how much GStore customers will spend"); the scouts' alternative is a purchase within a session predicted during it (the `online_shoppers_purchasing_intention_dataset` setting), which needs a prediction point cut from the hits. Fit approximate; regime temporal (v2 scored revenue in a window after the last session, from memory).
- Siblings and duplicates: `online_shoppers_purchasing_intention_dataset` (`Yes`, sessions of another store, Sakar et al. 2019: another source with the same unit and target, PROV-4); `customer_propensity_to_purchase_dataset` (`No`, generated) and `customer_acquisition_data` (`No`, untraceable); no other GStore record (searched gstore, merchandise store, the slugs and the help-page id). External collections: none known.
- Better data: no new search; found as better data for `online_shoppers_purchasing_intention_dataset`, `customer_propensity_to_purchase_dataset` and `customer_acquisition_data`.
- Papers and pages: Google's help page (read); the Kaggle competition (Overview, Evaluation and top solutions not read).
- Metric: the competition's RMSE (Kaggle API evaluationMetric "Root Mean Squared Error"; on the natural log of each user's summed revenue plus one, from memory of the Evaluation tab, which could not be read): a leaderboard metric (MET-4). Inputs: the user id (fullVisitorId) to sum per user, ships. A session purchase task would have no source metric (fallback `roc_auc`).
- Risks for /add-dataset: the first round's test revenue was public through the GA demo account, the reason for the v2 relaunch (check that no shipped field can be looked up); session totals (pageviews, hits, timeOnSite, transactions, revenue) cover the whole session, after any purchase (LEAK for a session task: cut from the hits); obfuscated ids and removed fields; about 99% of users have zero revenue; the v2 scoring window is not in the public files (from memory), so a revenue window is ours to construct from the sessions (SPLIT-9); 25 GB of nested JSON to flatten.
- Priority: gap 0 (business, regression and temporal are not thin), use case 0 (the publisher states a demo purpose; the competition's Overview was not read), source + (Google's documented export and a Featured competition), shape + (about a million sessions or more, mixed types, over a year), risk - (a leak history, totals after the purchase, a target window to construct).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through better data for `customer_acquisition_data`, `customer_propensity_to_purchase_dataset`, `online_shoppers_purchasing_intention_dataset`.
- as published: one row per session of a real e-commerce store with traffic source, device, geography, totals (pageviews, hits, time on site, bounces, transactions, revenue) and nested hit-level page data; Kaggle ...; target: the session ends in a transaction (totals.transactions > 0), or its revenue; access: registration (Google Cloud account for BigQuery, or Kaggle account and competition rules).
- Why: Same unit (a session), same target (purchase in the session) and the same kinds of features as online_shoppers (pages and time per page type, bounce and exit behaviour, traffic source, device, region, month), from a real store | customer_propensity_to_purchase_dataset is a fictional site's day of visits with on-site ...
- Adds: About 70x the sessions over a full year and the hit-level timeline, so features can be cut at a prediction point inside the session (the record's open concern about features computed after the purchase); no PageValues column, whose early-period leak cost the old data 5,455 rows. Caveats: fullVisitorId obfuscated and ...

**Assessment (AI, 2026-11-25):** the dataset build corrects three numbers of today's screening block: 898 visits are split at midnight (not 317; the block's 317 pairs were those whose two stored rows each reached a 3rd pageview), and the query now joins each into one visit; 234 visits reach a checkout step at or before the cut and are dropped (not 264, counted on the rows before the join); the cut keeps 305,819 visits (not 306,997), after the join, the funnel filter and the dropped day 2017-08-01.

**Assessment (AI, 2026-11-25):** review panel (full): ship after changes; disputed: none left after the rebuttals (the visitor history, USE-10, conceded and applied; the eight windows, SPLIT-14/SPLIT-15, conceded as the recommendation); for the curator: issue 1 and H. Priority 3: gap 0, use case 0, source +, shape +, risk 0 (use case ours: Google names no task, fit approximate; risk: no leak or exploit found, the open choices are the split's length and count).

CC (2026-11-25, Andrej): review issue 1, b, "Eight windows (the issue's B)": December 2016 and January 2017 are added as the curator's exception to the half-the-rows floor, eight monthly test windows from December 2016 to July 2017; with the one-day gap January trains on 46.0% and December on 35.7% of the visits; the reason is the holiday season (December has the most visits and the highest buy rate, 4.5%), which the newer months lack, and the precedents that added windows under half to come closer to the target of 9. November 2016 (26.2%) stays out, under the 30% floor, so 8 windows against 9.

CC (2026-11-25, Andrej): the declared horizon (one calendar month, a one-day gap, windows starting 2017-07-01, 2017-06-01, 2017-05-01, 2017-04-01, 2017-03-01, 2017-02-01, 2017-01-01 and 2016-12-01) is checked, the month from the assumed monthly refit of the store's model (Google names no task, horizon or cadence; its own Session Quality score works on 30 days of data), the one-day gap the lag between building a model and applying it, as on fugaku_hpc_job_failure_1m, though the label is known when the visit ends.

**Assessment (AI, 2026-11-25):** the curator's two decisions are applied: eight windows with a one-day gap. Test visits and train shares of the 305,819 visits: July 2017 25,115 (91.5%), June 22,577 (84.1%), May 24,556 (76.2%), April 22,530 (68.8%), March 23,691 (61.0%), February 21,919 (53.8%), January 24,276 (46.0%), December 2016 30,716 (35.7%), with 694 to 1,385 buyers a window; each window trains on the visits up to the day before the previous month's last day (29 June 2017 for July, 29 November 2016 for December). `dataset check`: 0 errors, 2 warnings (category values that rarely buy, all known at visit start; no licence stated), `splits_train_under_half` and `splits_below_target` accepted. Task probe on the rebuilt data (5 of the 8 windows): untuned LightGBM ROC AUC 0.877, logistic regression 0.863, a random forest 0.863, the best single feature (country) 0.693.

## Review

**Outcome:** added; the AI recommends shipping, and both of your choices of the split are applied: one-month windows with a one-day gap (H) and eight test months, December 2016 to July 2017, with January and December as your exception under half (issue 1). Task: at a visit's third pageview, before any checkout step, will the visit buy (305,819 visits of 240,212 visitors, August 2016 to July 2017, 3.7% buy; Google's obfuscated GA360 sample of the Google Merchandise Store, queried in BigQuery). Validity: every feature is the visit's start, the visitor's earlier visits in the sample, or a count over the visit's hits up to the cut; the finished-visit totals, which score 0.977 against 0.873 at the cut, never ship, and the 234 visits that reached checkout before the cut are dropped. Applied after the panel: the visitor's history as three columns (earlier visits, earlier purchases, days since the last visit), the masked traffic source set to missing, `events` split by action and `/home-2` counted as home, a protocol line against reading other test rows, and two gaps named in the fit (purchase, not uplift; a masked Referral group with 44% of the buyers). Value: in the task probe on the eight windows, untuned LightGBM scores ROC AUC 0.877, logistic regression 0.863, a random forest 0.863 and the best single feature (country) 0.693, with 694 to 1,385 buyers per test month; no reviewer found an exploit. `dataset check`: 0 errors, 2 warnings (category values that rarely buy, all known at visit start; no licence stated); the windows under half and the 8 windows against a target of 9 are accepted with your CC lines.

**Main points:** Nothing open: the horizon (one month, a one-day gap) and the eight test windows (January 46.0%, December 35.7% as your exception) are decided and applied; the two remaining check warnings (rare category values, no licence) were left for your acceptance.

**Horizon:**

* **Verdict:** keep one calendar month, no gap (medium confidence on the length, high on the gap).
* **Length:** Google names no task, horizon or refit cadence for the sample, so a month is our assumption: a store that refits its model monthly and scores the next month's visits. Google's own GA360 "Session Quality" score, the same in-visit purchase estimate, needs 30 days of data but names no retraining cadence ([help page](https://support.google.com/analytics/answer/7303153)), which supports a month only weakly[^g1].
* **Gap:** none: the label is the visit's own transaction, known when the visit ends; only 20 visits at a month's end run over midnight and none of them buys, so at a month's start every earlier label is in[^g2].
* **Time frame:** the sample's own span, 2016-08-01 to 2017-08-01, in the store's time zone (America/Los_Angeles, which gives the sample's `date` on every row); the last table, 2017-08-01 (959 visits), is dropped because one day is no month and merging it would bend July's window. Which months are tested is issue 1.
* **Options:**

  | | Option | What it does | Test windows | Pro | Con |
  |---|---|---|---|---|---|
  | A | One month, no gap (implemented) | Each month February to July 2017 is predicted from every earlier visit | 6, of 21,919 to 25,115 visits (704 to 1,099 buyers); train 54.1% to 91.8% | a monthly refit is a common cadence; Google's own score needs 30 days of data; every window holds hundreds of buyers | the cadence is assumed; 6 windows against a target of 9 |
  | B | Two weeks, no gap | Fortnightly windows over the same period | 14, of 9,809 to 12,108 visits | reaches the target of 9 | only if a fortnightly refit is realistic, which no source says; shortening the window to reach the count is barred[^g3] |
  | C | One week, no gap | Weekly windows | 28, of 4,782 to 6,565 visits | many test periods | a weekly refit is assumed too; noisier windows; far over the target |
  | D | Two months, no gap | Two-month windows | 3, of 45,610 to 47,692 visits | longer horizon | only the minimum of 3 windows; no source asks for it |

* **Recommendation:** A: no source names a cadence, a month is the common one and Google's own score works on 30 days, and every window holds hundreds of buyers; B only if a fortnightly refit is realistic for a store's web model. **Decision:** keep one month (A), or change to B, C or D?

**Notes for the AI:** For B, C or D set `TemporalSplits(window=2, unit="weeks", ...)` (or 1 week, 2 months) with cutoffs that keep every window's train side at 50% or more, re-run `dataset windows ga_merchandise_store_sessions --window <n> --unit <unit>` for the exact windows, and rewrite `task_summary.split`, the splits comment (cadence, count, target 9) and the window note; the window counts above are the split auditor's (windows training on at least half the rows), not yet the definition's.

[^g1]: **SPLIT-12** (Should): the horizon, the refit cadence, the gap and the time unit come from the use case and the source; the splits comment names each, or says the source is silent and what is assumed. The curator signs off on the horizon and the test windows of every new temporal dataset.
[^g2]: **SPLIT-10** (Should): a gap of about the label delay; no gap where the delay is within the time column's resolution.
[^g3]: **SPLIT-15** (Should for the windows other than the newest): the window length, the step and the gap follow the use case "and are never shortened or dropped to reach the count".

**Andrej (2026-11-25, discuss):** Shouldn't we leave at least one day as a gap? The model to predict new samples still has to be trained after all

**Answer (AI, 2026-11-25):** yes: a one-day gap is valid here and costs almost nothing (each training side loses at most 0.43 points, every shipped window still trains on more than half, ROC AUC moves by -0.001 to +0.002 per window), so the recommendation changes to a one-day gap.

* **Problem:**
  - Your decision on fugaku_hpc_job_failure_1m of 2026-11-24 (its review issue 7, D) set "the gap before each window: the lag between building a model and applying it", one day. The same lag holds here: a store that refits monthly cannot train on the visits of a month's last evening and score the next month's first visit at midnight.
  - The "no gap" of the verdict above rests on the label alone (known when the visit ends, within the day). That answers the label's delay, not the time the refit takes; the gap rule counts a planning gap of the use case as a gap too[^g4].
  - Measured on the definition's frame (table below): with the gap, the six windows train on 53.8% to 91.5% of the visits (54.1% to 91.8% without); each training side loses 521 to 867 visits (17 to 39 buyers), about one day of traffic; untuned LightGBM changes by -0.0010 to +0.0015 per window, +0.0004 on average, the size of the spread between seeds. Nothing in the data argues against the gap.
  - The month boundary: with the gap, each window trains on the visits that start before 00:00 of the previous month's last day, so the last training day is 29 June for July, 30 May for June, 29 April for May, 30 March for April, 27 February for March and 30 January for February. The last day of each month (30 June, 31 May, ...) is in no training side and in no test window: one day of every month left out of training.
  - For issue 1 the gap changes only the shares: January 2017 would train on 46.0% (46.2% without), December 2016 on 35.7% (36.1%).
* **Experiments:** the six shipped months and the two candidates of issue 1 (January, December); training on every earlier visit, or on those starting at least one day before the month; untuned LightGBM (default parameters), ROC AUC, mean of 3 seeds:

  | Month | Test visits | Buyers | Train share, no gap | Train share, 1-day gap | Visits left out (buyers) | Last training day | ROC AUC, no gap | ROC AUC, 1-day gap | Change |
  |---|---|---|---|---|---|---|---|---|---|
  | July 2017 | 25,115 | 1,022 | 91.8% | 91.5% | 867 (32) | 29 June | 0.8715 | 0.8711 | -0.0004 |
  | June 2017 | 22,577 | 937 | 84.4% | 84.1% | 859 (37) | 30 May | 0.8654 | 0.8669 | +0.0015 |
  | May 2017 | 24,556 | 1,099 | 76.4% | 76.2% | 521 (26) | 29 April | 0.8828 | 0.8841 | +0.0013 |
  | April 2017 | 22,530 | 915 | 69.0% | 68.8% | 781 (17) | 30 March | 0.8813 | 0.8816 | +0.0003 |
  | March 2017 | 23,691 | 874 | 61.3% | 61.0% | 810 (29) | 27 February | 0.8836 | 0.8840 | +0.0004 |
  | February 2017 | 21,919 | 704 | 54.1% | 53.8% | 866 (39) | 30 January | 0.8772 | 0.8763 | -0.0010 |
  | Mean of the six | | | | | | | 0.8770 | 0.8773 | +0.0004 |
  | January 2017 (issue 1) | 24,276 | 694 | 46.2% | 46.0% | 424 (10) | 30 December | 0.8688 | 0.8643 | -0.0045 |
  | December 2016 (issue 1) | 30,716 | 1,385 | 36.1% | 35.7% | 1,320 (56) | 29 November | 0.8240 | 0.8251 | +0.0010 |

* **Options:**

  | | Option | What it does | Pro | Con |
  |---|---|---|---|---|
  | a | No gap (implemented) | each month is predicted from every visit before it | the newest day of data in training; the label is known within the day | assumes the model is built and deployed at midnight in no time; departs from the fugaku decision |
  | b | One-day gap | each month is predicted from the visits that start at least one day before it | the build lag of a refit, as decided on fugaku; at most 0.43 points of training share and no change in ROC AUC beyond the seeds' spread; every shipped window stays above half | the day is assumed (no source names the lag); each month's last day trains no model and is tested by none |

* **Recommendation:** b, as on fugaku: the refit needs time, and the measurement leaves every window valid at nearly the same score. **Decision:** a or b?

**Notes for the AI:** For b set `TemporalSplits(window=1, unit="months", cutoffs=(...), gap=1, gap_unit="days")` and the gap on `Temporal` (`gap=1, gap_unit="days"`, as fugaku_hpc_job_failure_1m declares it); rewrite the splits comment's "No gap" sentence (the one-day gap is the build lag of a monthly refit; the label is known within the visit) and its train shares (91.5%, 84.1%, 76.2%, 68.8%, 61.0%, 53.8%); re-run `dataset check`; add the case to the gap rule's list as an ordinary use.

[^g4]: **SPLIT-10** (Should): a gap of about the label's delay between train and test; "A planning gap the use case has (a forecast made a day ahead) is a gap too." Its list of cases records fugaku_hpc_job_failure_1m's one-day gap as applied.

**Andrej (2026-11-25, reply (b)):** One-day gap.

**Resolved (2026-11-25, Andrej):** b, a one-day gap before each test month, as on fugaku_hpc_job_failure_1m: `dataset.py` declares it on the windows (`TemporalSplits(window=1, unit="months", cutoffs=(...), gap=1, gap_unit="days")`; a calendar gap the windows state is not declared again on `Temporal`), and the splits comment's gap paragraph names it as the lag between building a model and applying it. The record carries the horizon's CC line (one calendar month, a one-day gap, eight windows starting 2017-07-01 to 2016-12-01). Train shares with the gap: 91.5%, 84.1%, 76.2%, 68.8%, 61.0%, 53.8%, 46.0% and 35.7%, July 2017 back to December 2016. `dataset check`: 0 errors.

**Issues for Andrej:**

1. **Test six months, or add December 2016 and January 2017 as eight?**

   - **Problem:**
     - Six monthly windows (February to July 2017) are all that train on at least half the visits, against the rules' target of 9 windows for a table this size; January 2017 (train 46.2%) and December 2016 (36.1%) are possible only as your exception.
     - No shipped test month holds the holiday season: December has the most visits and the highest buy rate of the year.
     - Every comparable case since 2026-11-11 added windows under half to come closer to the count, and you signed off four of them on 2026-11-19.
   - **Background:** traffic in the sample drops from about 950-990 visits a day in November and December 2016 to about 780 from January 2017, a level change of unknown cause (Google's sampling or real); all six current test months come after it. November 2016 would train on 26.5%, below the 30% floor. No source says whether Google sampled the store's traffic at random.
   - **Experiments:** the candidate windows (`dataset windows`, data statistics only; drift is the largest population stability index of a feature against the train side; `promotion_clicks` drifts because no month after December 2016 has one; the first six rows are the windows tested now):

     | Month | Test visits | Buy rate | Train share | Largest drift |
     |---|---|---|---|---|
     | July 2017 | 25,115 | 4.1% | 91.8% | 0.34 (source) |
     | June 2017 | 22,577 | 4.2% | 84.4% | 0.16 (source) |
     | May 2017 | 24,556 | 4.5% | 76.4% | 0.73 (promotion_clicks) |
     | April 2017 | 22,530 | 4.1% | 69.0% | 0.84 (promotion_clicks) |
     | March 2017 | 23,691 | 3.7% | 61.3% | 0.97 (promotion_clicks) |
     | February 2017 | 21,919 | 3.2% | 54.1% | 1.11 (promotion_clicks) |
     | January 2017 | 24,276 | 2.9% | 46.2% | 1.34 (promotion_clicks) |
     | December 2016 | 30,716 | 4.5% | 36.1% | 0.46 (source) |

   - **Consistency:** windows under half were added to reach the count on anes_voting_2026 (40.0-49.2%), mercedes_benz_greener_manufacturing (31.5-46.7%), maps_router_eta_1m (44.8%), cooking_time (37.5%) and ieee_fraud_detection (38.9%); the rule names seasons and holidays as periods a deployed model must handle, and a change in data collection as a reason to test across it, not to avoid it[^w1]. The rule on windows under half is already flagged as due for an amendment for this run of exceptions[^w2].
   - **Panel:** the advocate, the critic and the precedent checker recommend eight; the builder and the split auditor recommended six, or seven with December only, pointing to the traffic drop.
   - **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Six windows (implemented) | February to July 2017, every window trains on at least half the visits | no exception; all test months after the traffic drop, so they resemble each other | 6 of 9; no holiday month tested; departs from five precedents unless the traffic drop is recorded as the reason |
     | B | Eight windows, December 2016 to July 2017 | Adds January (46.2%, 24,276 visits) and December (36.1%, 30,716 visits) on a CC line naming both | follows the precedents; tests the holiday season; 8 of 9 | two more exceptions; December trains on four months, before the traffic drop |
     | C | Seven windows, adding December only | Adds December (36.1%) on a CC line | tests the season | skips January, which trains on more than December; no precedent skipped a feasible window |

   - **Recommendation:** B, as the precedents did: December is the season the newest windows lack, and the traffic drop is a change of collection the rule counts as a reason to test across. A only if you record the January drop as the fact that sets this dataset apart. **Decision:** keep six (A), or add windows (B or C)?

   **Notes for the AI:** For B set `cutoffs=("2017-07-01", "2017-06-01", "2017-05-01", "2017-04-01", "2017-03-01", "2017-02-01", "2017-01-01", "2016-12-01")`; add the CC line to the record with both windows and their train shares (January 46.2%, December 36.1%) and the reason (the holiday season, the precedents); rewrite `task_summary.split` and the splits comment (8 windows against the target of 9, both under half named with their shares and the reason); `dataset check` then warns `splits_train_under_half`, accepted with the CC line; re-run `dataset check` and the task probe. For C the same with December only.

   [^w1]: **SPLIT-15** (Must for the newest window, Should for the others): the other windows are argued from the use case, "which periods a deployed model must handle (other years, seasons, holidays, events, a change of rules or of the data collection)"; the number of windows aims at SPLIT-33's count for two thirds of the scored units (9 here).
   [^w2]: **SPLIT-14** (Must): every window trains on at least 50% of the data; a window under 50% is the curator's exception, down to 30%, raised as an issue and accepted only with the curator's CC line.

   **Andrej (2026-11-25, discuss):** Why so many windows? The target for 300000 samples should be 3?

   **Answer (AI, 2026-11-25):** the target is 9, not 3: it counts the training side of a 3-fold split, two thirds of the 305,819 visits (203,879), and 3 repeats apply below 250,000 training units, so 3 x 3 = 9; the 3 you expect starts at 375,000 rows.

   * **Problem:**
     - The count follows the units on the training side of a 3-fold split, not the table: 3 repeats below 250,000 training units, 1 repeat from there on[^w3]; the windows aim at that count for two thirds of the scored units[^w4]. Two thirds of 305,819 is 203,879, under 250,000: 3 repeats x 3 folds = 9. `dataset check` computes the same (6 windows against 9, a warning).
     - The 3 you expect holds from 375,000 rows on, where two thirds reach 250,000: sdss_17's 4.6 million rows give 3.
     - A fact about the rule: this table is 69,181 rows (23%) under that step, and the target falls from 9 to 3 at a single row, so the count here rests on where a threshold lies more than on the data.
     - The target is an aim, not a floor: fewer windows are accepted down to 3, with the warning and the splits comment naming the count. Six is valid, and three would be too; but the rule asks for as many windows as reach the target within the floor, and the newest three alone would drop three windows that train on more than half.
   * **Experiments:** the candidate monthly windows (as the definition builds them, no gap; the shares with a one-day gap are under H):

     | Month | Test visits | Buyers | Train share | In a | In b | In c |
     |---|---|---|---|---|---|---|
     | July 2017 | 25,115 | 1,022 | 91.8% | yes | yes | yes |
     | June 2017 | 22,577 | 937 | 84.4% | yes | yes | yes |
     | May 2017 | 24,556 | 1,099 | 76.4% | yes | yes | yes |
     | April 2017 | 22,530 | 915 | 69.0% | yes | yes | |
     | March 2017 | 23,691 | 874 | 61.3% | yes | yes | |
     | February 2017 | 21,919 | 704 | 54.1% | yes | yes | |
     | January 2017 | 24,276 | 694 | 46.2% | | yes | |
     | December 2016 | 30,716 | 1,385 | 36.1% | | yes | |

   * **Options:**

     | | Option | Windows | Test visits (buyers) | Train share | Pro | Con |
     |---|---|---|---|---|---|---|
     | a | Six monthly windows (implemented) | February to July 2017 | 21,919 to 25,115 (704 to 1,099) | 54.1% to 91.8% | no exception; every month the floor allows | 6 of 9, a warning to accept; no holiday month tested |
     | b | Eight windows (the issue's B) | December 2016 to July 2017 | 21,919 to 30,716 (694 to 1,385) | 36.1% to 91.8% | 8 of 9; tests the holiday season; follows five precedents | two exceptions under half (January 46.2%, December 36.1%); December trains on four months |
     | c | The newest three, as if the target were 3 | May to July 2017 | 22,577 to 25,115 (937 to 1,099) | 76.4% to 91.8% | the fewest windows; every training side over three quarters | 3 of 9 while three more valid windows exist; walking back from the newest needs its own reason, and on three datasets the newest three ranked model pairs the wrong way round[^w4] |

   * **Recommendation:** b, as recommended above (the target of 9 stands, and December is the season the newest months lack); a if you want no exception. c only if the rule's target is changed to fall off more gently, which would be a decision for the rule, not this dataset. **Decision:** a, b or c?

   [^w3]: **SPLIT-33** (Should): repeated 3-fold cross-validation with 20, 10, 3 or 1 repeats "as its train side holds fewer than 500, 2,500 or 250,000 units, or more"; the definition checks it on two thirds of the units.
   [^w4]: **SPLIT-15** (Should for the windows other than the newest): "The number of windows aims at the splits an IID split of the dataset would get: SPLIT-33's count for two thirds of all its scored units (60, 30, 9 or 3)"; fewer are accepted, never fewer than 3; walking back from the newest window "needs its reason too"; on aeolus, climate_model and delivery_eta the newest three windows ranked a model pair the other way round than the whole eligible history.

   **Andrej (2026-11-25, reply (b)):** Eight windows (the issue's B).

   **Resolved (2026-11-25, Andrej):** b, eight monthly windows from December 2016 to July 2017: `dataset.py` adds the cutoffs 2017-01-01 and 2016-12-01, `task_summary.split` and the splits comment name both windows under half as your exception with their shares (January 46.0%, December 35.7%, with the one-day gap of H) and the reason (the holiday season the newer months lack, the precedents), and `accepted_check_warnings` accepts `splits_train_under_half` and `splits_below_target` (8 against 9; November 2016 would train on 26.2%, under the 30% floor) with the CC date. The record carries the CC line. `dataset check`: 0 errors, 2 warnings left (rare category values, no licence); the task probe: LightGBM 0.877, logistic regression 0.863, the best single feature 0.693.

**Review panel:** ship after changes (mediator). Claim audit: 24 claims, the validity claims all hold; the masking claim was refuted beyond organic search and the returning-visitor ranges were stale (both fixed), the operating-system count off by one (fixed). Blind review: would include with changes; its concerns (the cut and the row filter) are answered by the query. Task gamer: no exploit. Debate: agreed on every point after the rebuttals; the visitor history (applied) and the eight windows (issue 1) were conceded. For the curator: issue 1 and H.

<details><summary>Mediator</summary>

I recommend **ship after changes**. The advocate and the critic ended up agreeing on every point: in their rebuttals each conceded the other's main argument, so no dispute was left to settle by rank. I ran no experiment because no fact was disputed. The open questions in the reports were answered by the code (`dataset.py`) or by the panel's own measurements (details under "Exploits" below). Two calls stay with you: the number of test windows and the one-month horizon.

**Judgment record**

```text
Verdict: ship after changes.
Validity: SEL holds; USE-3 holds; USE-8 holds (approximate; fit_reason must also name two gaps: it predicts purchase, not
  whether an offer changes it, and the masked Referral group); USE-10 triggered: visitors are treated as known but their
  earlier purchases are not features, fixed by adding history columns (LEAK-34); LEAK-10 holds (finished-visit totals
  0.977 against 0.873 at the cut; 234 visits that reached checkout before the cut dropped); LEAK-9 triggered, fixed by
  a protocol line; SPLIT-15 Must holds (newest month tested); SPLIT-14 holds with 6 windows; the leaf L-ORDER.windows
  holds; SPLIT-13 holds (random folds 0.869, folds grouped by visitor 0.867).
Value: the task probes pass (LightGBM 0.872, linear 0.858, RF 0.855, best single feature 0.693; 704-1,099 buyers per
  test month); the roc_auc fallback holds (MET-6 to MET-9; ROC AUC, AP, log loss, Brier and top-k rank the models the
  same in all 6 months).
Quality: CLEAN-10, masked source/medium set to missing (option B); CLEAN-1, repair `events` and the `/home-2` page
  group in the query; claims in the notes corrected.
Weighed (windows): precedent +, holiday season +, curator-only exception -, unexplained traffic drop in Jan 2017 ±.
For the curator: issue 1, 6 or 8 test windows (SPLIT-14/15); issue 2, the one-month horizon (SPLIT-12).
```

**Changes to make now (no decision needed)**

1. **Add visitor-history columns (USE-10, Must; LEAK-34).**
   - The definition treats returning visitors as known: they stay in test and `visit_number` ships. USE-10 then says "the previous outcome is a feature".
   - The only reason given for leaving them out was the small gain (+0.0004 to +0.005). That is not a reason the rules accept.
   - Add three columns from the same `fullVisitorId`'s visits that started before this one: earlier purchases, earlier visits in the sample, days since the last visit.
   - Build them in the query over all sample visits, not only the kept rows, so the short visits and the 234 dropped funnel visits count too. Count only purchases whose transaction hit comes before this visit starts.
   - This includes earlier visits in the same test month. The site knows them at visit start (LEAK-34), and they are features, not a model reading other test rows.
   - The notes should name the August 2016 start of the history and that about 90% of test visits have none. Re-measure the gain and state it as information only.
   - Not adding the columns would need a change to USE-10. A Must allows no exception.
2. **Add a LEAK-9 protocol line (Should)** to the notes and `splits_comment`: each test row is predicted from the training rows and its own features only, and no model step may use other test rows.
   - Why: 14.2–15.7% of each test month's visits have a later visit by the same visitor in that month. Reading it through the visitor id adds +0.014 to +0.017.
   - The task gamer found no gain from the shipped columns (0.8761 against 0.8763), but the line costs nothing and matches bank_marketing, loan_default_prediction_imperial_college and spanish_motor.
3. **Masked source, option B (CLEAN-10, Should).** Where `channel` is not Direct, set `source` "(direct)" and `medium` "(none)" to missing.
   - Cost: 0.8740 against 0.8739 as published.
   - Rewrite the anomaly bullet to name all three masking patterns: Organic and Paid Search masked by month; Display 17% masked in June; Referral 72–84% masked in every month, those visits buying at 10.3% against 1.4%.
   - Fix the checklist line that says there is "no class-dependent recording".
   - Don't offer option C (drop both columns) as a neutral choice: it costs −0.002 and is worse in 5 of 6 months.
4. **Fit (USE-8, USE-5).** Name both gaps in `fit_reason`:
   - the data predicts purchase, not whether an offer changes it (no treatment in the data);
   - the masked Referral group is 16% of rows and about 44% of buyers. That it is Google's employee store is a hypothesis; say so.
   - The rows stay. Dropping "a cart reminder" from `use_case` is optional wording (it fits only the 2.2% of visits with a cart add).
5. **Repair in the query (CLEAN-1).**
   - Split `events` by event action. Promotion Click events stop in December 2016, and the share of visits with an event falls from 33% to 13–17%. Leaving Promotion Click out of `events` is an acceptable alternative.
   - Add `^/home-2` to the home pattern.
   - Note the listing-page URL change of August–September 2016.
6. **Corrections:**
   - the operating system is missing in 976 rows, not 977;
   - returning-visitor ranges over all six months: 9.3–10.1% of a test month, buying at 7.9–11.4%, against 2.7–3.8% for new visitors;
   - name Sakar et al. 2019 in the metric reason (MET-1); the fallback stands;
   - one line in `splits_comment` saying 2017-08-01 is dropped on purpose (merging it would bend July's window);
   - re-run `dataset windows`: the evidence `windows.txt` is stale and marks 3 windows, not 6;
   - add the history columns to `known`.
7. **Keep `visit_start` as an input,** as diabetes_130_us keeps its time index. Its −0.004 is a modelling choice for participants.

**Issues for the curator**

1. **Test windows: keep 6, or add December 2016 and January 2017 (P4; SPLIT-14 Must for the exception, SPLIT-15 Should).**
   - **Problem:** the target is 9 windows and 6 ship. January (train share 46.2%) and December (36.1%, the holiday month, buy rate 4.5%) are only possible as your exception. No shipped test month contains the holiday season.
   - **For 8 windows (advocate, critic, precedent checker):** every comparable case since 2026-11-11 added windows under 50% to get closer to the count: anes_voting_2026, mercedes_benz, maps_router_eta_1m, cooking_time and ieee_fraud. You signed off four of them on 2026-11-19. SPLIT-15 names seasons and holidays as periods a deployed model must handle.
   - **For 6, or 7 with December only (builder, split auditor):** the sample holds 12 months. Traffic drops from about 950–990 visits a day (November–December) to about 780 from January 2017, cause unknown (sampling or real). All six current test months come after that drop.
   - **What would settle it:** knowing whether the drop is Google's sampling. No source says. Note that SPLIT-15 counts a change in data collection as a reason to test across it, not to avoid it.
   - **Recommendation:** (b), 8 windows, December to July, with a CC line naming both windows and their train shares. Choose A or C only if you record the January drop as the fact that sets this dataset apart from the precedents.
   - SPLIT-14 is already flagged as due for an amendment; this would add one more exception.
2. **Horizon of one month (P4, SPLIT-12 Should).** Google names no refit cadence. Its GA360 Session Quality score needs 30 days of data, which supports a month only weakly.
   - Alternatives: two-week windows give 14 windows and reach the target, but only if a two-weekly refit is realistic. SPLIT-15 bars shortening the window just to reach the count.
   - **Recommendation:** keep one month. Your sign-off is needed.

**Agreed facts**

- **Size:** 305,819 visits of 240,212 visitors, 11,392 buy (3.7%), August 2016 to July 2017.
- **The cut:** features cover the hits up to and including the 3rd pageview (`k <= cut_k`; `c_hits = 3 + c_events` is asserted).
  - No checkout path appears before the cut. The highest buy rate of a page opened before it is 27%, against 49–94% on checkout pages.
  - The label matches the transaction hits on every row.
- **Leak measured:** the finished-visit totals score 0.977 (final pageviews alone 0.936); the cut scores 0.873.
- **Windows:** train shares 91.8% down to 54.1%; 21,919–25,115 test visits per month; no gap is needed (20 month-end visits cross midnight and none buy).
- **Other checks:** a classifier separating train from test rows scores 0.48; 0.1% of test rows have an exact copy in training.
- **Masked source:** Referral is 78.7% masked; masked Referral buys at 10.3% against 1.4%, is 93% US, and holds about 44% of buyers. Organic search is masked 2.3% buy against 2.4% unmasked.
- **History in the data:** visitors buy again at 20–28% after an earlier purchase.

**Task gamer's exploits**

The task gamer found no exploit. Each attempt maps to a rule, and the definition has no `Potential leak, kept on purpose:` notes to compare against.

- **Rebuilt visitor chains / next visit:** LEAK-9, new mechanism. The gain through the shipped columns is 0; through the visitor id it is +0.014–0.017. Covered by change 2.
- **Aggregates over the test month's own rows:** LEAK-9/LEAK-30. 0.8751, slightly worse than honest.
- **Row order, timestamp precision, number formats:** row-order checks. Nothing found (0.5007 from formats alone).
- **Copies across the split:** LEAK-21. 0.1%, at the base rate.
- **Event timing after the 3rd pageview (its open question):** LEAK-10. Answered by the SQL: hits after the cut are excluded. `distinct_pages` of 4–6 comes from event hits on category pages (claim auditor #3).
- **Row filter (its open question):** verified by the claim auditor (#5).

Of the three warnings, `dataset_pure_feature_value` and `meta_license_unknown` hold as stated. `splits_below_target` holds for 6 windows and changes if you choose issue 1(b).

**Consistency with precedent**

- **Three departures without a stated reason, now resolved:**
  - history features → change 1 (tunisian_fraud, corporate_credit_rating, ieee_fraud `uid`);
  - missing protocol line → change 2 (bank_marketing and the others);
  - window count → issue 1 recommends (b), with the January traffic drop as the only possible distinguishing fact.
- **One precedent difference to note:** tunisian_fraud took its previous labels from training years only. The history here also uses earlier visits in the same test month. What sets it apart: the store's records update within the month, while tax years close once a year (LEAK-34).
- **Consistent with precedent:** the masking fix (fremtpl2, protein_model_quality), roc_auc (seismic_bumps), `visit_start` as an input (diabetes_130_us), PROV-7 distinct from `google_analytics_customer_revenue_prediction`, the horizon put to you, and the dropped totals (online_shoppers issue 3).
- **2017-08-01:** dropping it is kept. Merging it would bend July's window; the line in change 6 records why.
- **No drift** in the curator's decisions.

</details>

<details><summary>Claim audit</summary>

I tested 24 claims. None of the validity claims fell: the cut, the label, the split and the totals leak all hold under tests that could have refuted them. Two descriptive claims are wrong or out of date, and one mechanism was missed. That mechanism matters for draft issue 1.

**Claims table**

| # | Claim | Source | Test | Result | Evidence | Rule |
|---|---|---|---|---|---|---|
| 1 | 305,819 visits of 240,212 visitors; 11,392 buy (3.7%) | task_summary | rebuilt the frame through `dataset_io.from_definition(raw=True)` | holds | 305,819 / 240,212 / 11,392 (3.725%) | — |
| 2 | Raw sample 903,653 visit rows of 714,167 visitors | curation_comments | BigQuery totals query | holds | 902,755 distinct visits (`fullVisitorId`-`visitId`), which is 903,653 rows less the 898 midnight pairs | PROV-8 |
| 3 | Every feature is known at the 3rd pageview, nothing after it | comments bullet 1, task_summary `known` | read the SQL: the funnel filter includes `tx IS NOT NULL` and the label agrees with the transaction hits (assert in `_clean`). New BigQuery query: every pre-cut hit whose path is not among the visit's pre-cut pageviews | holds | the extra paths are events on ordinary category, search and home pages; no checkout path (top: `/home` 138 visits, men's t-shirts 114). The 908 visits with more than 3 distinct paths buy at 18%, which is category browsing, not funnel | LEAK-10 |
| 4 | The final totals give the purchase away: 0.977 with them, 0.932 from final pageviews alone, 0.874 at the cut | comments bullet 2 | pulled each visit's final totals from BigQuery (44 MB scan), joined them by visit id, LightGBM on the 6 shipped folds | holds | at the cut 0.873 (0.861–0.881); with totals 0.977 (0.975–0.978); final pageviews alone 0.936 | LEAK-10 |
| 5 | The checkout pattern catches every checkout and purchase hit; 234 visits dropped (115 buy); highest pre-cut path buy rate 27% | comments bullet 3 | read the builder's `funnel_paths.csv` and `facts.txt` | holds | the four checkout pages plus one transaction hit on a category page; shipping-policy pages are not funnel; funnel_before_cut 234, of which 115 buy | LEAK-10 |
| 6 | The label equals the transaction hits | comments bullet 4 | `facts.txt` crosstab and the assert in `_clean` | holds | 295,343 / 0 / 0 / 11,435 before the 2017-08-01 drop | CLEAN-25 |
| 7 | 898 midnight-split visits merged; the 2nd row restarts the clock | comments bullet 5 | `midnight.csv` | holds | 898 two-row visits; part 2 has min_t0 0 and a different `visitStartTime` (same_start 0), so the offset in the query is needed and applied | — |
| 8 | Hit times rise with the hit number in every visit | comments bullet 1 | `hitorder.csv` (no BigQuery re-run) | holds on the builder's evidence | time_back false in every cell | EV-2 |
| 9 | 2017-08-01 dropped (959 visits) | comments | `facts.txt` | holds | 959 | — |
| 10 | 2,264 visits start after hit 1 and buy at 3.1% | comments, Anomaly 1 | recomputed | holds | 2,264 visits, 3.09% buy | — |
| 11 | "(not set)" counts: source 23, medium 45, OS 977, geography 331 | comments | recomputed | holds, with a 1-off | source 23, medium 45, **OS 976**, geography 331 | — |
| 12 | Country set for 99.9%, 61% US | comments | recomputed | holds | 99.89%, 60.7% | — |
| 13 | Source masking does not follow the label (organic search masked 2.3% vs unmasked 2.4%), so it is not class-dependent recording | comments, Anomaly 2; builder checklist | masking rate and buy rate by channel and month | **refuted beyond organic search** | organic holds (2.27% vs 2.43%); Paid Search holds (3.68% vs 3.63%). **Referral: 78.7% masked, stable 72–84% every month, masked buy 10.32% vs unmasked 1.38%.** Masked Referral visits are 92.9% US vs 43.7% unmasked, 53% returning vs 41%. No `mall.googleplex.com` among the visible referrers | LEAK-10 / LEAK-38 (see ranked item 1) |
| 14 | Masked source and medium are what drifts most (PSI up to 0.64) | comments | `windows.txt` | holds | March 0.643 | — |
| 15 | 32.7% of visits from 34,485 visitors with several; a test month holds 9.3–9.8% seen visitors, who buy 10.3–11.4% vs 2.8–3.8% for new ones | comments, Returning visitors | recomputed on all six test months | **partly refuted (stale)** | 32.7% and 34,485 hold. Across the six shipped months: seen 9.3–10.1% (Feb 10.06%), seen buy 7.9–11.4% (Feb 7.94%, Apr 10.0%, Jun 9.7%), new 2.7–3.8% (Feb 2.68%). The quoted ranges come from 3 or 4 of the months | SPLIT-13 |
| 16 | Random folds 0.869 vs grouped by visitor 0.867; history features add 0.003–0.005 | comments | not re-run; the gap and the low lift are plausible against my 0.873 | untested (the builder measured it; cost against value) | — | SPLIT-13 |
| 17 | 0.1% of test rows have an exact copy in training | builder, leak probe | exact feature match (without `visit_start`) on July and June | holds | 0.10% | LEAK-21 |
| 18 | `visit_start` in America/Los_Angeles gives the sample's date on every row | comments, assert | the assert runs in `_clean`; `facts.txt` | holds | 1.0 | — |
| 19 | Six monthly windows, train shares 91.8% to 54.1%, test sizes as listed, no gap, buy rate 3.2% (Feb) to 4.5% (May) | splits_comment | scored each shipped fold | holds | train shares 0.918 / 0.844 / 0.764 / 0.690 / 0.613 / 0.541; test 25,115 / 22,577 / 24,556 / 22,530 / 23,691 / 21,919; buy 4.07–4.48% from Mar to Jul, 3.21% Feb; the newest train row is just before each window | SPLIT-15, SPLIT-33 |
| 20 | Accepted warning `splits_below_target`: six windows on at least half of the visits is all the sample holds | splits_comment, warning | `windows.txt` | holds | Jan 2017 46.2%, Dec 2016 36.1% | SPLIT-15 |
| 21 | Accepted warning `dataset_pure_feature_value`: ordinary category effects at a 96.3% base rate | warning | read the listed values | holds | Social, Affiliates, YouTube, analytics.google.com and Europe/Asia are all known at visit start; no post-outcome value | evidence.md probe 4, case 2 |
| 22 | Accepted warning `meta_license_unknown` | warning | the help page states no licence (screening) | holds as stated | — | PROV |
| 23 | Distinct from `google_analytics_customer_revenue_prediction` | comments, screening | compared unit, target and prediction moment | holds | visit and binary at the cut, against visitor and log revenue in a later window | PROV-7 |
| 24 | Metric: fallback `roc_auc`, no source metric, no scoring columns | `metric` in dataset.py | read the spec; scored a constant and a random prediction on every fold with `data_foundry.v2.metrics.score`; counted positives | holds (one gap in the reason) | spec roc_auc, origin fallback, no inputs; constant 0.5 and random 0.488–0.505 on every fold; 704–1,099 positives per test fold; unit is the row, as the use case scores; binary, 3.7%. The reason names the help page, the announcement and Kaggle, but not Sakar et al. 2019, the paper the use case follows | MET-1, MET-2, MET-11 |

Implied claims I also tested:
* **Split matches the use case:** it is a forward split by month with an expanding train side, which matches a store that refits and scores the next month (SPLIT-15).
* **Target is the real-world target:** a transaction later in the same visit, which is what the site acts to cause.
* **`visit_start` is a fair input:** it is known at visit start, so it is fair. But as a raw datetime it costs a little: LightGBM 0.873 with it against 0.877 without (all 6 folds lower with it). That is information, not a finding.
* **Dropping source and medium (option C of issue 1):** costs 0.004 (0.869).

**Refuted and untested, ranked**

1. **Claim 13: the masking does not follow the label (P4/P5, a Should-level question under LEAK-38, not a leak).** The claim was tested only on organic search. In the Referral channel, "(direct)"/"(none)" covers about 79% of visits in every month, and those visits buy at 10.3% against 1.4% for the visible referrers.
   * **What it looks like:** a mask on one or more referrers, not a mask by month. Probably Google's internal store link (`mall.googleplex.com`, Google staff, mostly US and returning); it is absent from the visible referrers. That identity is my hypothesis, untested here: Kaggle v1 is not local.
   * **Why it is not a leak:** it is known at visit start, stable over months, and a deployed site sees its referrer.
   * **What it changes:**
     * The comment's sentence "It does not follow the label … no class-dependent recording" is wrong for Referral, and the builder's checklist line "the source masking does not follow the label" is wrong too.
     * It also bears on draft issue 1. Option B (masked values as missing) keeps the signal: Referral with a missing source still marks the group. Option C (drop source and medium) merges a 10.3% group with a 1.4% group in the Referral channel.
   * **Mildest remedy:** rewrite the anomaly bullet. Two mechanisms: a mask that varies by month on search traffic, which does not follow the label, and a stable mask on Referral, which marks a high-buying referrer known at visit start. Give issue 1 the Referral numbers so the curator weighs B against C with them.
2. **Claim 15: returning-visitor ranges (P7, wording).** The ranges quoted do not cover all six shipped test months. February has 10.1% seen visitors, who buy at 7.9%, and new visitors there buy at 2.7%.
   * **Mildest remedy:** restate them as 9.3–10.1%, 7.9–11.4% and 2.7–3.8% for February to July 2017.
3. **Claim 11 (trivial):** the operating system is missing in 976 rows, not 977. Fix the number.
4. **Claim 24, metric reason (MET-1, record where you looked):** the reason does not name Sakar et al. 2019, on whose in-visit setting the use case rests. That paper reports accuracy, TPR, TNR and F1 with no single criterion, so the fallback stands under MET-5 and MET-6.
   * **Mildest remedy:** add one clause to the reason.
5. **Untested:**
   * the 0.869 vs 0.867 random-vs-grouped comparison and the 0.003–0.005 history lift (builder's measurement, not re-run);
   * whether Google sampled the store's traffic at random (no source states it);
   * the identity of the masked Referral source.

</details>

<details><summary>Column audit</summary>

**Column audit: `ga_merchandise_store_sessions` (column-auditor)**

I found no leak. Every one of the 28 features is known at the third pageview. I found four problems, all with cleaning or with how the curation notes describe the data. The most important is that `curation_comments` and draft issue 1 describe the traffic-source masking incompletely, and the gap changes which option the curator should pick.

**How I checked**

- **Code and notes:** read `dataset.py`, the builder's report and probe outputs, and the screening block of the record.
- **Frame:** loaded the cleaned frame and computed the level and missing share of every column by month.
- **BigQuery:** queried the raw hits (the builder's own query, extended) for three things: the event categories before the cut by month, the account and basket pages before the cut with their buy rates, and the page paths that none of the page groups count.
- **Model fit:** compared the source/medium options with LightGBM on the six shipped windows, 2 seeds each.

**Files:** the release is one BigQuery table family, `ga_sessions_*`, one table a day, and `_load_raw` reads all of it through the query. The 2017-08-01 table is dropped, with a reason. Kaggle's v2 copy is left out with a reason (unverified copy, possible extension). No file is left out without a reason.

**Column table**

| column | meaning (GA360 BigQuery export schema) | known at prediction? | dtype and cleaning | verdict | rule |
|---|---|---|---|---|---|
| visit_start | visit start time, converted to Los Angeles time | yes | datetime; matches `date` on every row (asserted) | fine | — |
| visit_number | the visitor's session count (`visitNumber`) | yes (cookie, at start) | int, 1–395 (high values are probably internal users) | fine | USE-6 |
| channel | Default Channel Grouping | yes (from the landing) | category, 8 levels; kept unmasked while source is masked | fine | — |
| source | `trafficSource.source` | yes | category, 198 levels; "(not set)" set to missing; the dtype probe's `ordinal_like` flag is a false positive | **cleaning problem**: "(direct)" is a masked value in three different patterns (finding 1) | CLEAN-10 |
| medium | `trafficSource.medium` | yes | category; "(none)" masked as for source | **cleaning problem** (finding 1) | CLEAN-10 |
| true_direct | `isTrueDirect` (typed URL, bookmark, or a repeat of the same campaign) | yes | category, False/True; null set to False (the schema leaves it null when false) | fine | CLEAN-14 |
| device | device category | yes | category | fine | — |
| browser | browser | yes | category | fine | — |
| operating_system | OS | yes | category; "(not set)" set to missing (976 rows, 0 buy) | fine | — |
| continent / subcontinent / country | geography from IP | yes | category; "(not set)" set to missing (331 rows each) | fine | — |
| events | event hits up to the cut | yes | int | **cleaning problem**: one event type stops being recorded mid-history (finding 2) | — |
| seconds_on_site | time of the 3rd pageview, from visit start | yes | float; 219 rows under 1 s, none buy; harmless | fine | — |
| distinct_pages | distinct page paths over pageview and event hits | yes | int 1–6; 908 rows above 3 (event hits on pages absent from the sample) | fine | — |
| product_list_clicks / product_detail_views / cart_adds / cart_removes | Enhanced Ecommerce action types 1–4 | yes | int; flat across months | fine | — |
| basket_pageviews | /basket.html | yes, pre-checkout (19,371 visits, 15% buy; checkout pages run 49–94%) | int | fine | LEAK-10 |
| account_pageviews | signin, register, myaccount pages | yes, none of them is a funnel page: signin.html 29,970 visits at 5.3% buy, myaccount?vieworder 6,280 at 0.9%, guestregister 9 visits | int | fine | — |
| home_pageviews | `^/home$`, `^/$`, `^/home?` | yes | int | **cleaning problem (minor)**: misses `/home-2` (finding 3) | — |
| apparel / electronics / bags / other_category / product / search_brand pageviews | page-path groups | yes | int; product pageviews rise from 22% to 32% of visits over the year (site growth) | fine | — |
| listing_pageviews | store.html, asearch, top-level category pages | yes | int | **cleaning problem (minor)**: URL scheme change (finding 3) | — |
| purchase (target) | `totals.transactions` > 0 | target | "Yes"/"No"; agrees with the transaction hits on every row (asserted) | fine | CLEAN-25 |

**Problems, ranked**

**1. The traffic-source masking claim is incomplete, and option C would throw away a real signal (Should, CLEAN-10; corrects draft issue 1)**

`source = "(direct)"`, `medium = "(none)"` while `channel` says something else happens in three patterns. The comments describe only the first:

- **Organic Search, by month:** 0% masked in Aug 2016 and Mar/May 2017, 96% in Nov 2016, 53% in Jun 2017. This is what the comments describe.
- **Paid Search, the same monthly pattern:** 25–97% masked Sep 2016 to Feb 2017, 56% in June. Display is 17% masked in June. The comments do not mention either.
- **Referral, stable masking that does follow the label:**
  - 72–84% of Referral visits are masked in every month: 48,947 rows, 16% of the data.
  - These visits are 93% from the United States, against 44% for the unmasked referrals.
  - They buy at 10.3%, against 1.4% for unmasked referrals. On first visits the gap is 6.5% against 0.4%.
  - They hold about 44% of all buyers.
  - Likely cause: Google hid an internal referrer. `mall.googleplex.com` is absent from all 198 source values. That it is a heavy referral source in Kaggle's copy is my memory, not checked.

The referrer exists when the visit starts, so this is a real signal, not a leak. But the comments say the masking "does not follow the label (organic 2.3% vs 2.4%)", and that is true only for organic search.

What it costs (LightGBM, mean ROC AUC over the 6 windows, 2 seeds):

| option | mean AUC | change vs A | windows worse |
|---|---|---|---|
| A, keep as published | 0.8739 | — | — |
| B, masked values set to missing | 0.8740 | +0.0001 | 2 of 6 |
| C, drop source and medium | 0.8719 | −0.0020 | 5 of 6 |
| C plus a "masked referral" flag | 0.8732 | −0.0007 | — |

**Remedy (mildest):** keep option B, the builder's recommendation. It loses nothing, because Referral with a missing source still marks the hidden referrer. Rewrite the anomaly bullet to name Paid Search and the stable Referral masking with its buy rates. Present C as costing a real signal, not as a neutral simplification.

**2. `events` changes meaning in December 2016 (Weigh; no rule ID found, drift inside the history)**

- "Enhanced Ecommerce / Promotion Click" events before the cut appear in 5,057–5,962 visits a month from Aug to Nov 2016, 2,854 in Dec, and none from Jan 2017 on.
- As a result, the share of visits with any event drops from 33% to 13–17%.
- Promotion-click visits buy at about 1.5%. Visits with an event bought at 3.7–5.2% through 2016 and 6.6–9.3% from Feb 2017.
- Every test window has no promotion clicks; February to April still train on months that have them.
- `dataset check` cannot flag this: the column never goes missing, only one of its parts stops.

**Remedy:** split the count by event action in the query: promotion clicks, quickview clicks, product clicks (add to cart and remove from cart are already counted as `cart_adds` and `cart_removes`). The mildest alternative is to exclude Promotion Click from `events` and say so in a comment. I did not measure either option, because both need a re-export.

**3. Two page-group patterns miss URL changes (Weigh, minor)**

- `/home-2`, a home page variant used Nov 2016 to Feb 2017, is counted by no group. It had 658, 2,702, 1,989 and 1,640 pageviews before the cut in those months, against 24–41k matched home pageviews a month. The February test window is affected.
- Top-level category pages (`/google+redesign/bags` and the like) count as listings, and the site stopped using them after Aug–Sep 2016. Listing pageviews fall from 25% of pageviews before the cut in Aug 2016 to 11–14% later, and the share of visits with one falls from 57% to 31%.

**Remedy:** add `^/home-2` to the home pattern. Mention the listing step in the comments, or count top-level category pages in their category only. Both effects are small.

**4. Curator question, no change asked**

`visit_number` reaches 395, and the masked referrals with it mark probably internal (Google staff) shoppers. That subpopulation is a big part of the buyers: the masked referrals alone hold about 44%. If the curator wants the task to read "a public store's visitor", it is worth a sentence in `curation_comments`. It is not a leak, and the data is as published.

**Checked and found fine**

- No feature is recorded after the 3rd pageview; the cut is per hit, in hit order.
- The account and basket pages are not checkout pages (rates above).
- No feature stops or starts being recorded by month, apart from findings 2 and 3; missing shares stay under 0.5% in every month.
- The missing values do not mark a class; the missing indicators score AUC 0.50.
- The midnight merge and the funnel filter are sound.
- The dtypes are right by meaning, and the dtype flag on `source` is a false positive.
- The task has no training weight.

</details>

<details><summary>Split audit</summary>

**Verdict: the split is right, with notes.** Monthly expanding windows from February to July 2017, no gap, at leaf `L-ORDER.windows`, fit how this data was collected and how the store would use the model. Nothing needs re-splitting. The open item is the one-month horizon, which we assumed and the curator signs off (SPLIT-12).

**The tree (SPLIT-36)**
- **Collection type:** `Dated Event Log`. Each row is one visit with its date. It is not panel data: 240,212 visitors, only 32.7% of visits from visitors with several, and visitors are not seen at regular periods (SPLIT-34).
- **LOG.meets:** the model meets cases after the data (the store scores future visits), which leads to the Order and windows step on `visit_start`.
- **ORDER.order:** yes. The start time is recorded (`Time: Dated`), and the definition checks it against the sample's `date` on every row.
- **ORDER.windows:** yes. Six monthly windows each train on at least 54.1% of the rows, with 21,919 to 25,115 test visits.
- **ORDER.small:** no. 305,819 rows and 6 windows.
- **Leaf: `L-ORDER.windows`.** This matches `split_leaf`, the `splits_comment` and the shipped `Temporal` split. No forced leaf, and no question that no answer fits.

**Checks that pass, with numbers (rebuilt from the definition)**
- **Windows match the comment exactly.** Train shares are 91.8, 84.4, 76.4, 69.0, 61.3 and 54.1%. Each train side ends before its test month starts. All windows are at or above half (SPLIT-14), and the smallest window has 704 buyers (well above 33 scored units).
- **Count against target (SPLIT-15):** the target is 9 and the definition has 6. What stops more is the 50% floor: January 2017 trains on 46.2% and December 2016 on 36.1%. The newest month is tested, and every eligible month is used, so no choice of windows was left to argue.
- **Labels in flight / gap (SPLIT-9, SPLIT-10):** the label is known when the visit ends. Only 20 visits run over midnight at a month's end, and none of them buy. No gap is needed, as the comment says.
- **Time column is the moment of prediction (USE-3):** the prediction is made at visit start plus the time to the third page, a few minutes later. No input is issued ahead of the time column, so no planning gap is needed.
- **The newest period is complete:**

  | Period | Visits a day | Buy rate |
  |---|---|---|
  | July 2017 | 810 | 4.07% |
  | February–June 2017 | 751–792 | 3.2–4.5% |
  | Last full week of July | in line with the earlier weeks | 4.07% |

  31 July (972 visits, 6.1%) is not cut short, and the dropped 2017-08-01 holds 959 visits, a normal day. There is no scrape cut (LEAK-24).
- **Recurring visitors (SPLIT-13, USE-10):** the regime is known and new visitors together, which is right. The store recognises a returning visitor by its cookie, and `visit_number` ships while the visitor id does not.
  - 9.3–9.8% of a test month's visits come from a visitor seen earlier.
  - Three random folds score 0.869, 0.867 and 0.870 ROC AUC; three folds grouped by visitor score 0.868, 0.869 and 0.864. No visitor-matching shortcut exists.
  - The leakage tests (LEAK-42/43): the link between a visitor's visits does carry the label (20–28% buy after an earlier purchase). But the id does not ship, so a model can only use that link through `visit_number`, which the store knows at visit start. The visitor's own earlier visits as features would add only 0.003–0.005.
  - LEAK-44 does not apply: `visit_number` counts visits, not purchases.
- **Near copies:** 0.1% exact copies across the split.
- **Training weight:** none.

**Findings, ranked**
1. **The one-month horizon is our assumption, for the curator's sign-off (SPLIT-12, Should).**
   - Google names no task and no refit cadence. The task does match a product Google itself sold on GA360: the "Session Quality" score (2017) predicts how likely a session is to end in a transaction. Its help page says the model needs 30 days of data, but no retraining cadence. That supports a month only weakly, so the length stays an assumption.
   - What is solid: no gap, because the label arrives within the visit.
   - The other lengths (windows training on at least half the rows):

     | Window | Windows | Test visits per window | Notes |
     |---|---|---|---|
     | 1 week | 28 | 4,782–6,565 | — |
     | 2 weeks | 14 | 9,809–12,108 | reaches the 9 |
     | **1 month (implemented)** | **6** | **21,919–25,115** | — |
     | 2 months | 3 | 45,610–47,692 | only the minimum |
     | 3 months | 2 | — | fails SPLIT-14 |

   - Two-week windows would reach the count only if a store would really refit every two weeks. SPLIT-15 forbids shortening the window just to reach the count.
   - **Recommendation:** keep one month. Two weeks is the option if the curator judges a two-weekly refit realistic for a store's web model.
2. **The masking of traffic source changes by month, which is a change in recording across the split (SPLIT-15, "a change of … the data collection"; related to builder issue 1).**
   - `source` and `medium` are the features that drift most between train and test in every candidate window (largest drift score 0.14 to 0.64; 0.31 for July, the newest window).
   - The masking does not follow the label, so it is no leak. But each test month scores the model partly on a masking mix it barely saw in training.
   - **Mildest remedy:** builder option B, setting the masked values to missing where `channel` disagrees. That also makes the windows comparable. No re-split is needed.
3. **No season-shaped test window (note).** December 2016, the holiday month with the highest buy rate (4.5%) and the most visits (991 a day), can only be tested by an exception at 36.1% training (SPLIT-14). Traffic in the sample also drops from about 950–990 visits a day in November–December to about 780 from January 2017, a level change of unknown cause, sampling or real. The six test months February–July all fall after it. I agree with the builder's recommendation: no exception unless the curator wants the holiday tested. If so, add December only, at 36.1%, recorded as an exception.
4. **Stale evidence (minor).** The evidence `windows.txt` marks only 3 chosen windows (July, May, March), from an earlier version of the definition. Re-run `dataset windows ga_merchandise_store_sessions` so the review evidence shows the six shipped windows. `hidden_groups.py` was not run because it has no option for temporal splits; the entity probe covers what it would check.

I fit no model of my own. The random-against-grouped comparison above (0.869 against 0.867) already settles that question, and SPLIT-15 bars choosing windows by a model's score.

Sources:
- [Session Quality [Legacy], Google Analytics help](https://support.google.com/analytics/answer/7303153)
- [Google launches free version of Optimize 360, introduces Session Quality Score (MarTech)](https://martech.org/google-analytics-free-optimize-session-quality-score-more/)

</details>

<details><summary>Domain practitioner</summary>

I'm the store's analyst for this one, the person who decides in the middle of a visit whether to show an offer or open a chat. The task holds up, but the shipped notes miss one thing about who the buyers are.

**Fit: approximate (I agree with the definition).** It is a real store's clickstream, and every feature ends where my site would act. But nothing in it tells me whether my intervention changes the outcome, and the third pageview as the moment to act is our choice, not the source's (USE-8, USE-1, USE-3).

**As the actor**

1. **Inputs at the moment of prediction (USE-3, USE-6).** At the third pageview my front end has everything that ships: the visit start, the channel, the device, the country, the visit number from my cookie, and counts of the first three pages. Nothing in the data comes from after that point: the visit totals are excluded and the 234 visits that reached checkout before the cut are dropped.
   - **Something I would see differently:** when I deploy, I see the true `source` and `medium`. The masking in the data is an artefact of Google's export, not something I would face.
   - **Things I would always have but which are missing:** my own records of the visitor's past visits and orders, and my promotion and stock calendar. Google obfuscated or removed these. The builder measured that visitor history adds only 0.003 to 0.005, so the loss is small.

2. **The target is a stand-in (USE-5).** What I act on is whether the offer changes the purchase. A visitor who would buy anyway costs me margin if I give them a discount. Gubela et al. 2019 benchmark this exact question for e-commerce coupon targeting and find uplift models beat response models. The data has no treatment information, so purchase probability is the stand-in every store starts with. Google's own predictive metric, "purchase probability", is the same kind of propensity, though it is per user over 7 days.

3. **Rows and test months.** One row is one visit at one decision point, which matches. In practice I would score at every event rather than once (Requena et al. 2020 predict early in the visit; the Coveo SIGIR 2021 challenge predicts at the moment of an add-to-cart). One fixed point per visit is a fair simplification. Testing each month after training on all earlier months, with returning visitors left in, is what I would actually face (USE-10, SPLIT-13).

4. **Would I use the model? Yes, as a first propensity scorer.** I measured untuned LightGBM on all six test months: the top 10% of visits it scores catch 55% of the buyers, at 22% precision against a 3.9% base rate.
   - **I would trust** the forward monthly validation and the clean cut before checkout.
   - **I would distrust** the masked sources and the share of employee purchases (gap 2 below).
   - **Calibration drifts:** the mean predicted probability ran 10–20% below the real buy rate in March, April and May. If I set offers by expected value, I would recalibrate every month.

5. **Metric: yes, `roc_auc` scores my decision.** The source fixes no threshold, cost or k, so the threshold-free fallback applies (MET-6, MET-7, MET-8). A 3.7% buy rate alone is no reason to switch to average precision (MET-9). The unit scored is the visit, the unit I act on (MET-1).
   - I checked whether another metric would pick a different model: ROC AUC, average precision, log loss, Brier score and top 5/10/20% capture all rank LightGBM above a small LightGBM above logistic regression, in every one of the six months.
   - I would pick `log_loss` only if the decision were expected value (probability × margin − offer cost). That is plausible but not stated anywhere, and it would pick the same models here.

**Gaps between the dataset and the real decision, most important first**

1. **Purchase probability instead of uplift.** This is the gap that changes the task most, and it can't be fixed from this data. Name it in `fit_reason` as the reason the fit is approximate.

2. **Close to half the buyers likely come from Google's internal employee store. The notes don't say this.**
   - The Referral channel with its source masked to "(direct)" covers 48,947 visits (16%) that buy at 10.3%: 5,052 buyers, 44% of the 11,392.
   - The whole Referral channel holds 45.9% of the buyers, and 95% of all buyers are in the US.
   - A third-party analysis of the store's 2016 data describes the referral from mall.googleplex.com, a site only Google employees can use, as the best-converting source, at 8.8% of visits. I infer the masked referrals are mostly that site; this is not confirmed in the sample itself.
   - A store would not give discounts to its own staff, and part of what the model learns is "this is an employee". These are real paying visits, so the rows should stay (no change to the task). But the notes should say so, and the curator should know.

3. **The masked `source` and `medium` (builder's issue 1).** When I deploy I see the real values, so I support option B: treat the masked value as missing where `channel` disagrees. A further fact for that issue: inside Referral the masking is steady (72–84% each month). It drifts by month mainly for organic search.

4. **One fixed prediction point instead of scoring at every event.** This is a small gap. The use case lists "a cart reminder", but that only fits the 2.2% of visits with a cart add (6.3% if basket views count). Offers and chat prompts fit every row.

5. **December is never a test month.** The peak season goes untested. This is a minor gap and already on the review as issue H.

**What an expert in this field would change**

- In `curation_comments`, add a line on the masked Referral traffic: probably the employee store, 44% of buyers. Keep the rows.
- Write the uplift gap into `fit_reason`. The prediction point being our choice is already there.
- Adopt option B for `source` and `medium`.
- Optionally narrow `use_case` to offers and chat prompts.
- Leave the metric as is.

**Findings**
- **F1** (medium, notes): the employee-referral concentration among buyers is not documented (masked Referral = 44% of buyers at a 10.3% buy rate).
- **F2** (low, `fit_reason`): uplift, not propensity, is the decision's real target; the gap is unnamed.
- **F3** (low, supports builder issue 1 option B): the deployed model sees the true source.
- **F4** (informational): ROC AUC, log loss, average precision and top-k capture pick the same model in all six months, so the metric is settled.

**Sources**
- [Requena et al. 2020, Sci Rep, shopper intent from clickstream](https://www.nature.com/articles/s41598-020-73622-y)
- [Coveo SIGIR eCom 2021 data challenge](https://arxiv.org/abs/2104.09423)
- [Gubela, Bequé, Gebert, Lessmann 2019, Conversion uplift in e-commerce](https://ideas.repec.org/p/zbw/irtgdp/2018062.html)
- [CleverTap, propensity vs uplift](https://clevertap.com/blog/from-propensity-to-uplift-why-ai-should-optimize-for-incremental-impact-not-just-likelihood/) (a vendor blog)
- [GA4 predictive metrics](https://support.google.com/analytics/answer/9846734)
- [Brand Inside, Google Merchandise Store analytics (mall.googleplex.com as an employee-only referral)](https://brandinside.asia/google-merchandise-store-analytics)
- [Google's GA sample help page](https://support.google.com/analytics/answer/7586738)

</details>

<details><summary>Precedent check</summary>

**Precedent check: `ga_merchandise_store_sessions`**

Three of the definition's choices and draft recommendations depart from earlier decisions without a stated reason: the number of test windows, the visitor history features, and a missing protocol line. The other decisions follow their precedents. There is one minor gap and no case of drift.

The precedents come from the register (7,370 decisions) and the records. I ran two checks on the raw cut myself.

**Verdicts**

| # | Decision (builder's draft) | Verdict | Precedents |
|---|---|---|---|
| 1 | Test windows: six months, February to July; December and January left out (issue H, recommendation A) | **Departs, no reason stated** | anes_voting_2026, mercedes_benz_greener_manufacturing, maps_router_eta_1m, ieee_fraud_detection (Lennart, 2026-11-11); cooking_time, airqo August 2020, ashrae, wisconsin (Andrej, 2026-11-19, "A as implemented") |
| 2 | Returning visitors: no history features, `visit_number` only (issue 3, A) | **Departs from USE-10 (Must); the only reason given is the small gain** | tunisian_fraud_detection_challenge (Lennart, 2026-11-05: previous label ships); corporate_credit_rating (USE-10 case); ieee_fraud_detection `uid` kept at a cost of 0.001-0.007 (LEAK-34) |
| 3 | No protocol line for one visitor's later visit in the same test month (not raised in the draft) | **Departs, no reason stated** | bank_marketing (Lennart, 2026-11-08); loan_default_prediction_imperial_college (Andrej, 2026-11-10); spanish_motor_insurance_coverage_level_2022_2024 (Andrej, 2026-11-09); medical_facility_operational_data (LEAK-9 cases) |
| 4 | Returning visitors stay in the test windows (SPLIT-13) | Consistent | diabetes_130_us (Andrej, 2026-11-11: "a hospital scores every next discharge"); home_credit_default_risk (Andrej, 2026-11-11) |
| 5 | Masked traffic source: recommendation B, set to missing where it contradicts `channel` | Consistent with the "impossible or placeholder value set to missing, row kept" line | protein_model_quality_rf_pcp (Lennart, 2026-11-04); airqo dead channels (Lennart, 2026-11-04/05); fremtpl2 `DrivAge` 99 (Lennart, 2026-11-05); horse_colic later codes |
| 6 | Metric: `roc_auc` fallback at a 3.7% base rate | Consistent | seismic_bumps (Andrej, 2026-11-20: ROC AUC over AP and log loss); sepsis_survival_minimal_clinical_records (Lennart, 2026-10-21); online_shoppers |
| 7 | Not a duplicate of `google_analytics_customer_revenue_prediction` (PROV-7) | Consistent | parkinsons and its telemonitoring sibling; qsar_aquatic_toxicity (Andrej, 2026-11-11, keep both and note the overlap). Unlike amex_iid / amex_non_iid, which are versions of one task. |
| 8 | `visit_start` as a model input | Consistent | diabetes_130_us `time_index` (Andrej, 2026-11-20: the actor holds it) |
| 9 | Accepted warnings `dataset_pure_feature_value` and `meta_license_unknown` | Consistent | website_phishing, qsar_oral_toxicity (Lennart, 2026-10-14/21); bank_customer_churn licence None (Lennart, 2026-10-14) |
| 10 | Horizon of one month put to the curator (SPLIT-12) | Consistent | Lennart, 2026-11-10 (the curator signs off every new horizon); meituan_food_delivery_time (Andrej, 2026-11-24) |
| 11 | Finished-visit totals dropped; visits with checkout before the cut dropped (LEAK-10) | Consistent | online_shoppers issue 3 (Andrej, 2026-11-20); kickstarter (`staff_pick` dropped once the task became "predict at launch") |
| 12 | 2017-08-01 dropped (one day, 959 visits) | Minor, see the note at the end | none found |

**Drift and amendments:**
- **No drift.** Andrej's 2026-11-20 call on online_shoppers issue 3 (keep the finished-visit stand-in) and issue 7's recommendation B (retire it once this record ships) do not conflict. Issue 3's own text names "revisit when the hit-level data ships" as the trigger.
- **An amendment is already due.** The register flags `amendment_due SPLIT-14` (exceptions on five datasets). If December and January are added, that adds another exception for the same reason (windows down to 30% to reach the count). The curator's 2026-11-19 sweep treats these as routine, so the rule text may be what should change.

**Reflection prompts (issue shape)**

**1. Add December 2016 and January 2017 as test windows, as the earlier datasets did to reach SPLIT-15's target?**

* **Problem:**
  - The target is 9 splits (note s15). Six months reach 50% training. January (46.2%, 24,276 visits, 2.9% buy) and December (36.1%, 30,716, 4.5% buy) are above the 30% minimum; November is not (26.5%, measured today). So 8 windows are possible.
  - Since 2026-11-11 every comparable case added windows below 50% to reach the count, implemented and then signed off: anes_voting_2026 (four windows at 40.0-49.2%), mercedes_benz (31.5-46.7%), maps_router_eta_1m (44.8%), cooking_time (37.5%), ieee_fraud_detection (38.9%). Andrej confirmed four of them on 2026-11-19 as "A as implemented" (note s14).
  - December is the holiday season that the newest windows lack. SPLIT-14 gives exactly that as the reason for its exceptions, and SPLIT-15 prefers windows in other seasons.
  - Recommendation A names no fact that sets this dataset apart.
* **Options:**

  | | Option | Pro | Con |
  |---|---|---|---|
  | a | Keep six windows; recorded fact: "the 12-month sample is too short for its oldest windows to resemble deployment" | fewer exceptions | that fact holds just as well for anes_voting_2026 and cooking_time; one window short of the earlier practice |
  | b | Treat it like anes_voting_2026 and mercedes_benz: 8 windows (December to July), both under-50% windows in a CC line | follows the precedents; covers the holiday season; 8 of 9 | two more exceptions toward the amendment that is already due |
  | c | Seven windows, adding December only (the builder's fallback) | adds the season | skips January, which is nearer the floor; no precedent for skipping a feasible window |
  | d | Amend SPLIT-14 so that windows down to 30% that reach the target are the default, not an exception | ends the run of exceptions | a rule change; read the other cases first |

* **Recommendation:** (b). Option (d) is a separate pass.

Note s14: SPLIT-14 (Must; amended 2026-11-08 and 2026-11-11): a window under 50% is the curator's exception, down to 30%.
Note s15: SPLIT-15: as many windows as reach SPLIT-33's count for two thirds of the units (203,879 units, so 9); prefer other seasons.

**2. Should the visitor's earlier visits and purchases be features, as USE-10 says for a known entity?**

* **Problem:**
  - The store knows a returning visitor through its cookie. The definition already treats these visitors as known: they stay in test (SPLIT-13), and `visit_number` ships.
  - USE-10 (Must): "For a known entity, its history is legitimate: the split is temporal and the previous outcome is a feature." Precedents shipped a built history: tunisian_fraud's `previous_target` (Lennart, 2026-11-05) and corporate_credit_rating's previous rating. ieee_fraud kept `uid` although it was worth only 0.001-0.007 (LEAK-34).
  - Recommendation A rests on the measured gain of 0.003-0.005. That is an argument about how well methods separate, not about the task: what the site would know at the 3rd pageview.
* **Options:**

  | | Option | Pro | Con |
  |---|---|---|---|
  | a | Keep A; recorded fact: "the sample's history is cut at August 2016 while the store's goes back further, so a history built here understates what the site knows, and 90% of test visits have none" | names a real limit of the sample | tunisian_fraud's history was also limited to the years in the data, and that did not stop it |
  | b | Treat it like tunisian_fraud: previous visits, previous purchases and time since the last visit, all from strictly earlier visits (option B) | follows USE-10 and its cases; the task as the site sees it | three columns more; the left cut-off should be named in the notes |
  | c | Reopen tunisian_fraud to match | none | that decision has a recorded reason |
  | d | Amend USE-10: history is optional when its measured gain is small | a clear rule | weakens a Must on a separability argument |

* **Recommendation:** (b), or (a) if the curator judges the cut-off history misleading.

Note u10: USE-10 (Must); LEAK-34 (Must; narrows LEAK-10).

**3. Add the LEAK-9 protocol line for a visitor's later visit inside the same test month?**

* **Problem:**
  - I measured this today on the raw cut. 14.2-15.7% of each test month's visits have a later cut visit by the same visitor in that month. About 80% of those pairs can be linked from shipped columns (`visit_number` plus 1, with the same device, browser, operating system and country).
  - Those visits buy at 5.4-7.1%, against 2.8-4.2% for the others, and hold 21-27% of the month's buyers.
  - A LightGBM that reads the next same-month visit (whether it exists, the time until it, its account, basket, detail and cart counts and its seconds) scores +0.014 / +0.015 / +0.017 ROC AUC on March, May and July (0.882 → 0.896, 0.885 → 0.899, 0.872 → 0.890). That link uses the visitor id; through the start fields it would be somewhat less. The lift is the size of the method gap the builder reports (0.014-0.035).
  - In deployment a later visit does not exist at the 3rd pageview. bank_marketing (Lennart, 2026-11-08), loan_default_prediction_imperial_college (Andrej, 2026-11-10) and spanish_motor (Andrej, 2026-11-09) each got a protocol line for this kind of leak: no model step may use other test rows. The splits comment here has none.
* **Options:**

  | | Option | Pro | Con |
  |---|---|---|---|
  | a | No line; recorded fact: "the visitor id does not ship, so the link is fuzzy" | nothing to add | about 80% can still be linked; loan_default_prediction_imperial_college was linked from a column too (f521, 88.7%) and still got the line |
  | b | Treat it like bank_marketing: a protocol line in the notes and `splits_comment` | follows four cases; costs nothing | none |
  | c | Also drop a visitor's later visits from the same test window (a filter, as alfa_battle does for repeat clients) | closes the channel in the data | loses test rows; no curator has chosen it yet |

* **Recommendation:** (b).

Note l9: LEAK-9 (protocol line; cases bank_marketing, loan_default_prediction_imperial_college, spanish_motor_insurance_coverage_level_2022_2024, medical_facility_operational_data).

**Minor (no prompt)**

The 2017-08-01 table (959 visits) is dropped. The screening had listed "its own month or merged" as open, but the builder made the call without raising an issue. The remedy ladder puts keeping before excluding, and merging it into the July window costs nothing. It is worth one line in the horizon issue.

</details>

<details><summary>Blind review</summary>

I would **include this dataset with changes**. It is a real and useful task: predicting a purchase from the early part of a website session. I found no leakage, and it is neither trivial nor too easy. But `task.md` does not say which part of the session the behaviour columns cover, or which sessions were kept, and both need to be written down before it goes in.

**What I checked.** The table has 305,819 sessions from the Google Merchandise Store (Google's public Analytics sample data, August 2016 to July 2017, also used in the Kaggle "GA Customer Revenue Prediction" competition). 3.7% of sessions end in a purchase. All 12 months are present at 22k–31k sessions each. The purchase rate moves in a believable way, peaking at 4.5% in December. I trained LightGBM on the earliest 80% of sessions (sorted by `visit_start`) and tested on the latest 20%:
- **All columns:** AUC 0.869, average precision 0.24, against a 4.0% base rate.
- **Context columns only** (channel, source, device, browser, location, visit number): AUC 0.81.
- **Single columns:** country 0.69, `visit_number` 0.67, `seconds_on_site` 0.52.

So the on-site behaviour adds real signal beyond the context, nothing is near-perfect, and with about 11k positive cases it is big enough to score.

**Concerns, most serious first**

1. **The behaviour columns cover only part of each session, and that part is not described.** I can't tell exactly which part, so I can't fully rule out leakage.
   - **Evidence:** every pageview column (`basket_pageviews`, `home_pageviews`, …) stops at exactly 3. `distinct_pages` stops at 6, and 99.7% of rows have 1–3. Buyers have *shorter* `seconds_on_site` than non-buyers (median 35.5 s vs 42.7 s). Over a whole session buyers stay much longer, so this column must measure only the early part.
   - **Doesn't fit "first 3 pages":** across categories the counts add up to as much as 14. So either each count was capped at 3 or the cut is something else.
   - **Some reassurance:** there is no checkout or order-confirmation column. The strongest behaviour column, `basket_pageviews`, gives a 15–19% purchase rate, high but well short of giving the answer away.
   - **Change:** state in `task.md` how the early part is cut (first N hits or N seconds, and before any checkout step), and whether each count is capped at 3. If the counts were capped by whoever prepared the table, drop the cap, or say why it is there.

2. **The rows are a filtered subset, and the filter isn't stated.** The full public sample has about 903k sessions; this table keeps 305k, about a third. The purchase rate here is 3.7%, compared with roughly 1.3% across the whole store. That suggests one-page "bounce" sessions were removed; the smallest `seconds_on_site` is 0.001 and no session has zero time.
   - **Why it matters:** if the filter needs the session's full length (for example "at least k hits"), it depends on what happens later in the session. That is acceptable as a definition of who gets scored ("sessions that are still going after the early part"), but it has to be written down.
   - **Change:** document the filter.

3. **The prediction comes down largely to "is this an American desktop visitor arriving directly".** 95% of purchases come from the United States. Desktop sessions buy at 4.6%, mobile at 1.2%. Direct traffic converts at 5.2%, Google organic at 2.5%. Some sources look like Google staff or internal traffic: `mail.google.com` at 8.8%, `groups.google.com` at 8.4%, `sites.google.com`. That limits how far results carry over to other shops, but it is real behaviour and acceptable for a benchmark. No change is needed beyond a note.

4. **Minor preparation points.**
   - `source`, `medium`, `operating_system` and location have a few missing values (at most 0.3%), which is fine.
   - `source` has 198 levels and `country` 205, with long tails; that is fine to leave as categories.
   - `true_direct` is stored as true/false; also fine.
   - 253 rows are exact copies of another row apart from `visit_start`. That is harmless: they are most likely short, identical sessions, not leakage.
   - There is no visitor ID, so the same visitor can appear in both train and test. With a split by time that matches real use, and it is not a problem.
   - `visit_start` should be used only for the split, not as a feature.

5. **The time split is right.** Six test windows over 12 months, each after its training rows, matches how such a model would actually be used. `task.md` names no training weight, so there was nothing to check there.

**What it is for:** an online shop scoring a session while it is still going, to decide whether to offer help, a discount, or a retargeting campaign. That is a standard, real use.

**What I could not check:** I didn't open the two source links in `task.md` or search the web; what I say about the source comes from my own knowledge. Without the raw hit-level data I couldn't confirm how the early part of each session was cut or how the rows were filtered. I also couldn't confirm that `purchase` means "the session had at least one transaction" (the usual meaning, `totals.transactions > 0`). The public data is real but partly obfuscated by Google, so some values may be masked. I didn't come across any file outside the clean room.

</details>

<details><summary>Task gamer</summary>

I found no exploit. Nothing I tried beats an honest model by more than the noise from a random extra column (about ±0.0013 AUC). The task looks hard to game as shipped.

**Honest baselines** (ROC AUC, mean of the 6 monthly test windows):
- **Untuned LightGBM on all features:** 0.8724 (per window 0.862–0.881).
- **Same model plus a random column** (3 seeds): 0.8711–0.8723.
- **Better honest model:** drop the raw `visit_start` timestamp, add hour and day of week, and tune the model. It scores 0.8773 (0.866–0.885).

**Exploits ranked by gain**

| # | Exploit | Script | Honest score | Exploited score | Gain (per split, range) | A deployed model has it? | Fix |
|---|---|---|---|---|---|---|---|
| – | None found | – | 0.8724 / 0.8773 | – | – | – | – |

The closest candidate was the time to the same visitor's next visit, which a deployed model would not have. It scored 0.8761, against 0.8763 for honest past-visit features: no gain.

**Flaw that hurts an honest model**

| Flaw | Honest choice | Baseline | Honest choice score | Fix |
|---|---|---|---|---|
| `visit_start` is passed in as a feature, so trees see a raw timestamp. Every test window lies beyond the training range, so they split on dates that never come back. | Drop it, or keep only hour and day of week. | 0.8724 | 0.8765 (no time column), 0.8767 (+ hour, dow), 0.8773 (tuned) | Leave `visit_start` out of `features()`, or ship it only as hour and day of week. |

This gain is +0.004 on average and positive on all 6 windows (+0.0005 to +0.009), which is above the noise. It is small: a careful participant drops the column anyway.

**Attacks that found nothing**
- **Row order:** rows are sorted by time. Correlation of position with the label is 0.011. The label rate after a purchase row is 5.2%, against 3.7% overall: people buy more in daytime hours, and hour is a legitimate feature.
- **Timestamp precision:** whole seconds, the same for both classes.
- **Formats of `seconds_on_site`:** the last digit is flat by class, and whole-number shares are 0.14% vs 0.08%. A model on these formats alone scores 0.5007.
- **Copies:** there are no exact duplicate feature rows. 870 rows share a start time and context; their purchase rate is 4.5%, close to the base rate.
- **Visitors rebuilt from context:** I matched country, browser, OS, device and `visit_number`+1 chains.
  - Future-visit features (time to the next session, number of next-visit candidates within a day): 0.8761 against 0.8763 honest. The match is too ambiguous to carry a leak.
  - Past-visit features (time since the previous visit, the previous visit's purchase label): legitimate, and only +0.0004.
- **Whole-day aggregates that use the test window's own rows** (sessions per day and hour, the day's share of cart adds and basket views): 0.8751, slightly worse.
- **Train vs test:** a classifier separating the last 60k training rows from the July test rows scores AUC 0.48. Nothing tells the test rows apart.
- **Training rows:** none dated at or after a test window. Training on only the last 3 or 6 months scores 0.8701 / 0.8749, worse than using the full history.
- **Columns from after the prediction point:**
  - `seconds_on_site` has AUC 0.457 on its own (purchasers are faster), so it is time to the third pageview, not the whole session.
  - The page-count columns are capped at 3.
  - Dropping the event columns (`events`, `cart_adds`, `cart_removes`, `product_detail_views`, `product_list_clicks`) costs only 0.003. They are not a hidden leak at scale.
- **Weight and transforms over all rows:** the task has no training weight, and no column looks standardised or ranked over the whole table.

**What I could not check**
- **Event timing:** I can't tell from the kit whether the event counts include events that fire on the third page after its pageview, which is after the prediction point. `cart_adds` reaches 29 and `events` 45 within three pageviews. This would need the hit-level source file.
  - The ablation above caps the effect at 0.003 AUC.
  - `distinct_pages` of 4–6 (908 rows, 18% purchase rate on the 891 rows with 4) is also odd with only three pageviews.
- **Row filter:** I could not verify the "before any checkout step" filter (that sessions reaching checkout early were dropped).
- **Web search:** one search found no leak write-up that applies to this task. The original Kaggle competition was relaunched to forecast future revenue, reportedly after a validation problem. Looking rows up in the public Google Analytics sample data would work, as with any public dataset, so I don't rank it.

Sources:
- [Medium – Highlights from the 1st Google Analytics Kaggle Competition](https://medium.com/innovation-machine/google-analytics-kaggle-competition-highlights-eaa046737ac4)
- [habr.com comments on the competition relaunch](https://habr.com/ru/users/sergeif/comments)
- [kozodoi/Kaggle_Google_Analytics](https://github.com/kozodoi/Kaggle_Google_Analytics)

</details>

<details><summary>Advocate, opening brief</summary>

**Advocate's opening brief: `ga_merchandise_store_sessions`**

My position: ship it. Every validity Must holds, and the panel found no leak and no exploit. What the panel did find are notes and cleaning choices, each with a cheap fix that keeps the dataset. I concede those below rather than deny them.

**1. The prediction point is clean, and that is the hard part of this task (P4, LEAK-10 Must, holds).**
- **Evidence:**
  - The claim auditor tested 24 claims, and none of the validity claims fell.
  - It re-pulled the finished-visit totals from BigQuery. With them the score is 0.977; at the cut it is 0.873. So the leak is measured and excluded, not guessed at.
  - Every checkout or purchase hit sits on the four funnel pages. The 234 visits that reached checkout before the cut are dropped. The highest buy rate of any path opened before the cut is 27%, against 49–94% on funnel pages.
  - The column auditor cleared all 28 features as known at the 3rd pageview.
  - The task-gamer found no exploit. Its best tries (rebuilt visitors, statistics over the test window, row order, number formats) all stayed within ±0.0013 of an honest model. A classifier separating train rows from test rows scores 0.48.
- **Why it outranks the rest:** no objection on the panel is a leak. Everything else sits at P3 notes, Should-level P4 choices or P7.

**2. A real use case, and it is the fix the curator already asked for (P3, USE-3, USE-8; online_shoppers issue 3 and issue 7 option B).**
- **Evidence:**
  - The curator kept online_shoppers' finished-visit rows on 2026-11-20 with "revisit when the hit-level data ships". This dataset is that revisit: 45 times the visits, a prediction point inside the visit, and a real forward split instead of a forced one.
  - Google sold this exact product on GA360: the Session Quality score, which predicts a session's transaction probability (split auditor).
  - The domain practitioner agrees the fit is "approximate". A propensity scorer is what a store starts with: its top 10% of visits catch 55% of buyers.
- **The uplift gap (practitioner F2):** I concede it. The remedy is one clause in `fit_reason`. The fit is already `approximate`, so USE-8 is met.

**3. The split mirrors the application (P4, SPLIT-36 leaf `L-ORDER.windows`, SPLIT-15 Must for the newest window, SPLIT-9/10).**
- **Evidence:**
  - The split auditor confirmed the leaf, the windows (train shares 54.1–91.8%) and the absence of a gap: the label is known at visit end, and only 20 month-end visits cross midnight, none of which buy.
  - Returning visitors stay in test, as SPLIT-13 asks for an entity the store knows: random folds score 0.869, folds grouped by visitor 0.867.
  - The precedent checker rates the regime, `visit_start` as an input and the horizon question as consistent with earlier decisions.
- **The one-month horizon:** this is a SPLIT-12 Should, open for the curator to sign off, not a defect.

**4. Worth benchmarking, and the metric is settled (P6, TP probes, MET-1/6/9).**
- **Evidence:**
  - 305,819 rows, with 704–1,099 positives per test window.
  - Methods separate: LightGBM 0.872, linear 0.858, random forest 0.855. The best single feature scores 0.693.
  - The practitioner checked other metrics. ROC AUC, average precision, log loss, Brier score and top-k capture rank the three models the same way in all six months.
  - The fallback matches the seismic_bumps and sepsis decisions.

**5. Source masking: the comment is wrong, the data is fine (P7, CLEAN-10 Should; LEAK-38 checked and not triggered).**
- **What I concede:** the anomaly bullet's claim that the masking "does not follow the label" holds only for organic search. Masked Referral visits are 79% of Referral traffic, stable every month, and buy at 10.3% against 1.4%. They hold about 44% of buyers, probably the employee-only referral `mall.googleplex.com`.
- **Why it is not a leak:** the referrer is known at visit start and the masking is stable across months (claim auditor, column auditor).
- **Mildest remedy:** option B, setting masked values to missing where `channel` disagrees.
  - It scores 0.8740 against 0.8739 as published, and Referral with a missing source still marks the hidden group.
  - Rewrite the bullet with all three masking patterns: Organic Search and Paid Search by month, Referral stable.
  - Add the practitioner's note on internal shoppers. The rows stay; they are real paying visits.
  - Option C would throw the signal away (−0.002, worse on 5 of 6 windows). I argue against it.

**6. Six windows meet the rules as written; adding December and January is the curator's call (SPLIT-14 Must, SPLIT-15 Should).**
- **What the rules say:** SPLIT-14 makes any window under 50% "the curator's exception … never on the AI's word". Six windows at 50% or more comply fully. SPLIT-15 accepts fewer than the target of 9, with `splits_below_target` named, which the splits comment does.
- **What I concede:** the precedent checker shows that comparable datasets added windows under 50% to get closer to the count (anes_voting_2026, mercedes_benz, cooking_time), and December is the season the newest windows lack.
- **Remedy:** offer option (b), eight windows from December, as a CC exception if the curator wants it. Either way the dataset ships. This is a choice to add windows, not a defect.

**7. Returning visitors: add the protocol line; history features are optional, not a Must failure (LEAK-9 Should; USE-10 and LEAK-34 Must).**
- **Protocol line, conceded:** add the LEAK-9 line, as bank_marketing, loan_default_prediction_imperial_college and spanish_motor have it. It costs nothing.
  - The precedent checker's +0.015 used the visitor id, which does not ship.
  - The task-gamer rebuilt visitors from the shipped columns and gained nothing (0.8761 against 0.8763), so the channel is weak. The line is still cheap and consistent.
- **History features, disputed:** USE-10 and LEAK-34 make an entity's history legitimate. I read them as allowing history, not requiring every possible history feature.
  - The definition already treats the visitor as known: they stay in test, and `visit_number`, the cookie's history, ships.
  - The sample's history is cut at August 2016, so a history built from it understates what the store knows, and about 90% of test visits have none.
  - The measured gain is +0.0004 to +0.005.
  - If the curator reads USE-10 strictly, option B is a fix inside the definition (three columns from strictly earlier visits), not grounds to hold the dataset.
- **Small fixes nobody disputes:**
  - Restate the returning-visitor ranges as 9.3–10.1%, 7.9–11.4% and 2.7–3.8%.
  - The operating system is missing in 976 rows, not 977.
  - Name Sakar et al. 2019 in the metric reason.
  - Note that promotion-click events stop in December 2016, or split `events` by action (Weigh).
  - Add `^/home-2` to the home pattern.
  - Re-run `dataset windows` so the evidence shows the six shipped windows.
  - Leave `visit_start` as an input, as diabetes_130_us keeps its time index. A participant may drop it, and its +0.004 cost is a modelling choice, not a flaw in the task.

**Judgment record**
```text
Verdict: ship after changes (notes and cleaning; no change to the task).
Validity: SEL holds; USE-3/USE-8 hold (approximate, add uplift to fit_reason); LEAK-10 holds (totals excluded, funnel dropped);
  SPLIT-14/15 hold (6 windows, below target named); LEAK-9 protocol line to add.
Value: TP probes pass (methods separate 0.014-0.035); MET roc_auc fallback, metrics agree.
Quality: CLEAN-10 option B for masked source/medium; comment corrections; events/home-2 minor.
For the curator: Dec/Jan windows (SPLIT-14 exception), history features (USE-10 reading), one-month horizon (SPLIT-12).
```

</details>

<details><summary>Critic, opening brief</summary>

**Critic, opening brief: `ga_merchandise_store_sessions`**

**Verdict: ship only after changes. None of my points is a reason to exclude it.** No reviewer found a leak in the features, and I am not arguing that one exists. The task is real and the cut at the third pageview holds. These tests failed to refute it:
- the audit query for checkout paths before the cut;
- the label matching the transaction hits;
- the task gamer's attacks, all of which found nothing.

What is wrong is narrower:
- the task leaves out history the store knows;
- the protocol line that the precedents carry is missing;
- one data claim the curator would decide on is false;
- the test windows stop short of the precedent.

**1. The visitor's earlier purchases are left out, though the store knows them (P3, USE-10 Must; LEAK-34 Must)**

- **Problem:** the definition treats returning visitors as known entities. They stay in test (SPLIT-13) and `visit_number` ships. USE-10 then says "the previous outcome is a feature". The definition ships no earlier purchase, no time since the last visit and no count of earlier purchases. It gives one reason: the measured gain is small (+0.003 to 0.005, builder's draft issue 3).
- **Effect on the real task:** the site, at the third pageview, knows its cookie's earlier orders. The benchmark task is a thinner version of what the actor actually does. Leaving out a known input because it barely moves the score is the separability argument the curator has ruled out ("represent the task correctly").
- **Evidence:**
  - Visitors who bought before buy again at 20–28%, against 2.7–3.8% for new visitors (comments; claim auditor #15).
  - The precedent checker (verdict 2) lists the precedents that shipped this kind of history: tunisian_fraud `previous_target` (Lennart, 2026-11-05), corporate_credit_rating's previous rating, and ieee_fraud `uid` kept at a cost of 0.001–0.007.
  - The task gamer confirms that past-visit features are legitimate (+0.0004).
- **Remedy (fix the definition):** add three features, built in the query from the same `fullVisitorId`'s visits that start strictly earlier: earlier purchases, earlier visits in the sample, and days since the last visit. Name in the notes that the sample's history starts in August 2016 (`visit_number` reaches 395). If the curator judges a history cut off that way misleading, that is the fact to record as the reason, not the size of the gain.

**2. The stated fit leaves out two gaps the curator should see (P3, USE-8 Must; USE-5)**

- **Problem:**
  - **Propensity, not uplift.** The use case is an offer or a chat prompt, so what the actor acts on is whether the intervention changes the purchase. The data has no treatment, so it predicts propensity (domain practitioner, gap 1; Gubela et al. 2019). That is the main reason the fit is approximate, and `fit_reason` does not name it.
  - **Likely internal buyers.** Referral visits whose source is masked are 16% of rows and buy at 10.3%, against 1.4% for referrals with a visible source. They hold about 44% of all buyers, are 93% US and come back more often (column auditor #1, claim auditor #13, practitioner F1). This is probably Google's employee store (`mall.googleplex.com` is missing from all 198 source values). That identity is a hypothesis: no reviewer verified it. Part of what a model learns is "this is internal traffic", and a store would not target offers at its own staff.
- **Remedy (a note):** keep the rows. Add a `curation_comments` bullet on the masked referral group, with its numbers and the hypothesis marked as one. Name both gaps in `fit_reason`. Optionally narrow `use_case` to offers and chat prompts: a cart reminder fits only the 2.2% of visits with a cart add (practitioner, gap 4).

**3. No protocol line for a visitor's later visit in the same test month (P4, LEAK-9 Should)**

- **Problem:** 14.2–15.7% of each test month's visits have a later visit by the same visitor in that month. Those visits buy at 5.4–7.1%, against 2.8–4.2%. Reading the next visit through the true visitor id adds +0.014 to +0.017 AUC (precedent checker, prompt 3). About 80% of these pairs can be linked from shipped columns.
- **Against my own point:** the task gamer rebuilt visitor chains from the shipped columns and found no gain (0.8761 against 0.8763 honest). An exploit through the shipped data is therefore **not shown**. The mechanism is measured; its use through the shipped columns is not.
- **Rule:** LEAK-9 puts an evaluation-level channel into a protocol line, not into the data. bank_marketing, loan_default_prediction_imperial_college and spanish_motor_insurance_coverage_level_2022_2024 each got one, the last two linked through columns.
- **Remedy (note):** one sentence in `splits_comment` and the notes: no model step may use other test rows. It costs nothing.

**4. The masking claim in the notes is false, and it shapes the curator's choice on issue 1 (P4/P5, EV-2; CLEAN-10 Should; SPLIT-15 "a change of the data collection")**

- **Problem:** `curation_comments` and the builder's checklist say the source masking "does not follow the label … no class-dependent recording". That is true only for organic search. Three things are missing:
  - **Referral:** 72–84% masked in every month, and the masked visits buy at 10.3% against 1.4%.
  - **Paid Search:** 25–97% masked from September 2016 to February 2017.
  - **Display:** 17% masked in June.

  (Column auditor #1; claim auditor #13, "refuted beyond organic search".) Draft issue 1 hands the curator option C (drop source and medium) as a neutral simplification. It is not neutral: it merges the 10.3% group with the 1.4% group, costs 0.002 AUC and is worse in 5 of 6 windows.
- **Effect:** `source` and `medium` are also the most-drifting features across every window (drift score up to 0.64; 0.31 for July). Each test month is partly scored on a masking mix the model barely saw in training (split auditor #2).
- **Remedy (fix the definition, plus the notes):**
  - Implement option B: masked values become missing where `channel` disagrees. It costs nothing (AUC 0.8740 against 0.8739), and the deployed site sees the true value.
  - Rewrite the anomaly bullet to name all three patterns with their buy rates.
  - Correct the checklist line.

**5. Six test windows where the precedent gives eight, and the holiday season is never tested (P4, SPLIT-15 Should; SPLIT-14 Must, exception by the curator)**

- **Problem:** the target is 9 windows and six are shipped. December 2016 (train share 36.1%, 30,716 visits, buy rate 4.5%) and January 2017 (46.2%) are both above the 30% floor. December is the holiday season the newest windows lack. SPLIT-15 names that as the reason to prefer other windows, and SPLIT-14 names it as the reason for its exceptions.
- **Precedent:** every comparable case since 2026-11-11 added windows under 50% to reach the count: anes_voting_2026, mercedes_benz_greener_manufacturing, maps_router_eta_1m, cooking_time and ieee_fraud_detection. Andrej signed off four of them on 2026-11-19. The builder's recommendation A states no fact that sets this dataset apart (precedent checker, verdict 1).
- **Remedy (fix the definition, on the curator's CC line):** eight windows, December to July. Record both windows under 50% as exceptions, and flag that SPLIT-14's amendment is already due. Also re-run `dataset windows`: the evidence `windows.txt` is stale and marks 3 windows, not 6 (split auditor #4).

**6. `events` changes meaning inside the history (P7, quality; it touches SPLIT-15 drift)**

- **Problem:** "Enhanced Ecommerce / Promotion Click" events before the cut appear in 5–6k visits a month through November 2016, in 2,854 in December, and in none from January 2017 on. The share of visits with any event falls from 33% to 13–17%. No test window has these events, but the February to April windows train on months that do (column auditor #2).
- **Two smaller page-group gaps:**
  - `/home-2` (November 2016 to February 2017, up to 2.7k pageviews a month) is counted by no page group.
  - Top-level category pages count as listings until the site stopped using them in August–September 2016.
- **Remedy (repair in the query):**
  - leave Promotion Click out of `events` (or split `events` by action);
  - add `^/home-2` to the home pattern;
  - note the listing change.

  This is a quality point, not a reason to hold the task back.

**7. Stale numbers and missing source in the notes (P7; MET-1)**

- The operating system is missing in 976 rows, not 977.
- The returning-visitor ranges come from 3 or 4 of the months. Over all six they are:
  - seen visitors: 9.3–10.1% of a test month;
  - their buy rate: 7.9–11.4%;
  - new visitors' buy rate: 2.7–3.8%.

  (Claim auditor #15, #11.)
- The metric reason does not name Sakar et al. 2019, the paper the use case follows. That paper reports accuracy, TPR, TNR and F1 with no single criterion, so the fallback stands (claim auditor #24). Add one clause.

**Dropped, because the evidence does not hold up:**
- **`visit_start` as a raw feature** (task gamer, +0.004 when it is dropped): that is a choice for the method. diabetes_130_us is the precedent for keeping it.
- **The 2017-08-01 drop:** one day is outside every calendar-month window, and merging it into July would bend the window.
- **The blind reviewer's question on the cut and the row filter:** the SQL shows that features end at the 3rd pageview hit and that the filter only uses what is known at that point.

</details>

<details><summary>Advocate, rebuttal</summary>

**Advocate's rebuttal: `ga_merchandise_store_sessions`**

**Where we land:** the critic and I agree on the verdict. Ship after changes. The task, the cut at the 3rd pageview and the leak tests all hold. I concede five of the critic's seven points outright and two with small reservations. On points 1 and 5 I lose the substance. Nothing I dispute changes a remedy.

**1. Visitor history features (USE-10, LEAK-34): **conceded****
- I argued that USE-10 *allows* history but does not *require* it. The rule's text is against me: "For a known entity, its history is legitimate: the split is temporal and **the previous outcome is a feature**" (`use_case.md:111`).
- The definition already treats the visitor as known: returning visitors stay in test, and `visit_number` ships. Once that is the case, the previous outcome belongs in the features.
- My only reason for leaving them out was the small gain (+0.0004 to +0.005). That is a separability argument, and the curator has ruled those out ("represent the task correctly").
- tunisian_fraud's `previous_target` was also limited to the years in its data, and it shipped (precedent checker, prompt 2). So the August 2016 cut-off does not set this dataset apart.
- **What follows:** option B. Add three columns built from the same `fullVisitorId`'s visits that start strictly earlier: earlier purchases, earlier visits in the sample, and days since the last visit. The notes name the August 2016 left cut-off and that about 90% of test visits have no history.
- Option A stays available only if the curator records the cut-off as misleading. The small gain is not a reason.

**2. Two gaps in `fit_reason` (USE-8, USE-5): **conceded****
- I had already conceded the uplift gap (my point 2). The masked-referral group (16% of rows, about 44% of buyers) belongs in the same place.
- Its identity as Google's employee store is a hypothesis, and the bullet should say so.
- I accept narrowing `use_case` to offers and chat prompts. A cart reminder fits only the 2.2% of visits with a cart add.
- All of this is notes. The rows stay.

**3. LEAK-9 protocol line: **conceded****
- This was already in my point 7. We agree on the facts: the mechanism is measured (+0.014 to +0.017 AUC through the true visitor id), and the task gamer found no exploit through the shipped columns (0.8761 against 0.8763).
- The line costs nothing and follows bank_marketing, loan_default_prediction_imperial_college and spanish_motor.

**4. Masking claim false; option B (CLEAN-10, EV-2): **conceded, one reservation****
- The anomaly bullet and the checklist line are wrong for Referral, Paid Search and Display.
- Option B as the fix, the rewritten bullet and the corrected checklist line: agreed, the same remedy as my point 5. Option C is not neutral (−0.002, worse in 5 of 6 windows), and the issue should say so instead of offering it as a simplification.
- **Reservation, on how the drift point is framed:** the drift in `source`/`medium` (score up to 0.64) is a fact about how the source recorded the data. The model meets it in training too, and it is not a defect of the split. Option B may reduce it, but nobody has measured that. It belongs in the notes, not as a separate finding.

**5. Six windows against eight (SPLIT-15, SPLIT-14): **conceded on the recommendation****
- I framed eight windows as an optional extra. The precedent checker shows that every comparable case since 2026-11-11 added windows under 50% to reach the count: anes_voting_2026, mercedes_benz, maps_router_eta_1m, cooking_time and ieee_fraud. Andrej signed off four of them on 2026-11-19.
- I cannot name a fact that sets this dataset apart. "The sample is short" holds just as well for anes_voting_2026 and cooking_time.
- December also brings the holiday season, which no current test window covers. SPLIT-15 prefers windows in other seasons.
- **What follows:** recommend option (b), eight windows from December to July. December (36.1%) and January (46.2%) each go on a CC line as exceptions.
- SPLIT-14 still makes these the curator's exception, "never on the AI's word". So the recommendation is (b), but the decision is the curator's line, not a default the builder applies.
- The register's `amendment_due SPLIT-14` gets one more case. Option (d), the rule change, is a separate pass.
- Re-running `dataset windows` (the stale `windows.txt`) is agreed.

**6. `events` changes meaning; `/home-2`: **conceded****
- Repair in the query (CLEAN-1, repair first). I prefer splitting `events` by action over dropping Promotion Click. Splitting keeps an input that is known at the cut and lets the model see the change. Either is acceptable, and it is a Weigh.
- Add `^/home-2` to the home pattern, and note the listing change.

**7. Stale numbers; Sakar et al. 2019: **conceded****
- These are the same corrections as in my list: 976 rows, the ranges over all six months, and one clause naming Sakar et al. 2019 in the metric reason.

**Where the critic dropped points**
- I agree with all three drops: `visit_start` (diabetes_130_us), the blind reviewer's question on the cut, and the 2017-08-01 day.
- On that day, the precedent checker's minor note asks for one line in the horizon issue saying it was dropped on purpose. I support adding it. Leaving the day out stays the right call, since merging it would bend July's window.

**Revised judgment record**
```text
Verdict: ship after changes. No exclusion ground; the task and the cut stand.
Definition: + 3 history columns (USE-10, option B); masking option B (CLEAN-10); events split or Promotion Click out, ^/home-2;
  8 windows Dec-Jul on the curator's CC line (SPLIT-14 exceptions; amendment due).
Notes: LEAK-9 protocol line; fit_reason names propensity-not-uplift and the masked-referral group (hypothesis marked);
  masking bullet and checklist rewritten; history left cut-off; corrected ranges, 976, Sakar et al. 2019; 2017-08-01 line.
For the curator: CC lines for Dec/Jan; one-month horizon (SPLIT-12); optional narrowing of use_case.
```

</details>

<details><summary>Critic, rebuttal</summary>

**Critic's rebuttal: `ga_merchandise_store_sessions`**

**Where we stand:** the advocate and I agree on the verdict. The dataset should ship after changes, and none of the open points is a reason to exclude it. Five of the advocate's seven points I concede in full. The real disagreement is one point: the visitor history features (advocate 7). On the extra December and January windows (advocate 6), we only disagree on which option the review should recommend.

**Conceded**

1. **The prediction point is clean (LEAK-10).** Conceded. I never argued for a leak. The finished-visit totals score 0.977 and the cut scores 0.873. The 234 visits that reached checkout before the cut are dropped. The column auditor cleared all 28 features, and the task gamer's attempts all stayed within ±0.0013.
2. **The use case is real and is the fix the curator asked for (USE-3, USE-8).** Conceded. The advocate also concedes the uplift gap and will add it to `fit_reason`, as my point 2 asked. The advocate's point 5 already includes the note on internal buyers. I drop my optional request to narrow `use_case` to offers and chat prompts: it is a P7 wording choice.
3. **The split mirrors the application.** Conceded: the leaf, no gap, and returning visitors kept in test under SPLIT-13. I did not raise the one-month horizon. It stays a SPLIT-12 sign-off for the curator.
4. **The task is worth benchmarking and the metric is settled.** Conceded. Adding Sakar et al. 2019 to the metric reason, which the advocate's list of small fixes includes, closes my point 7.
5. **Source masking.** We now agree on every part: the comment is wrong, option B, the bullet rewritten with all three masking patterns, the note on internal shoppers, and option C rejected. One addition for the record: the checklist line that says "no class-dependent recording" needs the same correction as the bullet.

The small fixes in the advocate's point 7 all match my points 6 and 7, so nothing is left in dispute there. They are the ranges, the 976 rows, `^/home-2`, Promotion Click, re-running `dataset windows`, and keeping `visit_start`.

**Disputed**

**Advocate 6: the windows comply "as written", so adding December and January is only an option**

- **What I accept:** six windows break no Must, and any window under 50% needs the curator's CC line (SPLIT-14). I asked for it on that line.
- **What I dispute:** that the six windows meet the rules with nothing left to argue.
  - SPLIT-15 (Should) says the non-newest windows are "argued from the use case", and it names "seasons, holidays" as what a deployed model must handle.
  - None of the six windows contains December, and December 2016 has the highest buy rate in the history (4.5%).
  - Every comparable case since 2026-11-11 added windows under 50% to get closer to the target: anes_voting_2026, mercedes_benz, maps_router_eta_1m, cooking_time and ieee_fraud. Andrej signed off four of them on 2026-11-19.
  - The builder gave no fact that sets this dataset apart (precedent checker, verdict 1).
- **What the review should do:** recommend option (b), eight windows from December, with both windows under 50% stated with their train shares (36.1% and 46.2%). Option A should be the departure that needs a stated reason, not the default.
- **Which rule wins:** SPLIT-15's argument from the use case, with consistent precedent. SPLIT-14 decides who signs off, not which option to recommend.

**Advocate 7: the history features are optional**

This is the main dispute. Here is each of the advocate's arguments and my answer.

- **"USE-10 allows history; it does not require it."**
  - The text says: "For a known entity, its history is legitimate: the split is temporal **and the previous outcome is a feature**." That describes how the task is built, not a permission.
  - The definition already decides that the visitor is a known entity: returning visitors stay in test and `visit_number` ships. Having decided that, it cannot leave out the entity's previous outcome without a stated reason.
- **"`visit_number` already ships the history."**
  - It is a count of visits, not the previous outcome. The outcome is what separates visitors who bought before (20–28% buy again) from new visitors (2.7–3.8%).
- **"The measured gain is +0.0004 to +0.005."**
  - These are two different measurements:
    - +0.0004 is the task gamer's chains rebuilt from shipped columns, without the true visitor id;
    - +0.003 to +0.005 is the builder's measurement on `fullVisitorId`.
  - Either way, the size of the gain is the reason the curator has ruled out: represent the task correctly, not by how much it separates methods.
  - ieee_fraud kept `uid` at 0.001–0.007 (LEAK-34, Must).
- **"The sample's history starts in August 2016, and about 90% of test visits have none."**
  - This is a real fact, and it is the only valid ground for option A. The precedent checker's option (a) says so.
  - tunisian_fraud's history was also limited to the years in its data, and its previous label still shipped (Lennart, 2026-11-05).
  - The visitors who do have a history are 9.3–10.1% of each test month and buy at 7.9–11.4%, about three times the rate of new visitors. That group is exactly where the store would use the history.
- **Which rule wins:** USE-10 (Must) and LEAK-34 (Must), with tunisian_fraud and corporate_credit_rating as precedents.
- **What the review should recommend:** option B, three columns built from the same visitor's visits that start strictly earlier: earlier purchases, earlier visits in the sample, and days since the last visit. Name the August 2016 start in the notes.
- **The alternative:** if the curator judges a history cut off like that misleading, keep A, but with the cut-off recorded as the reason, not the size of the gain.
- **Where we already agree:** this is a fix inside the definition, not a reason to hold the dataset.

**Net result**

- **Agreed changes:**
  - option B for source and medium, with the bullet and the checklist line corrected;
  - uplift and internal buyers named in `fit_reason` and the notes;
  - the LEAK-9 protocol line;
  - the corrections to the comments, the events and `^/home-2` fixes, and re-running `dataset windows`.
- **For the curator:**
  - the history features, where I recommend B under USE-10;
  - eight windows, where I recommend (b) on the precedent, on a CC line;
  - the one-month horizon, a SPLIT-12 sign-off.

</details>
