---
unique_name: us_accidents
name: US Accidents
checked_by:
- Lennart
suggestion: 'No'
decision_markers:
- No Good Target  / Scientific Discovery
- Time-series (Forecasting)
tags:
- Free Text (Short)
- Review Prio 1 (Atlas)
collections:
- CARTE/TARTE
- TabSTAR
original_source: Kaggle
year: '2019'
required_split:
- Temporal (NON-IID)
problem_type: Multiclass Classification
original_data_state: One Table
source_links:
- https://www.kaggle.com/datasets/sobhanmoosavi/us-accidents
- https://arxiv.org/abs/1906.05409
- https://arxiv.org/abs/1909.09638
- https://arxiv.org/abs/2402.16785
- https://arxiv.org/abs/2601.00152
- https://github.com/mhsamavatian/DAP
source_row: 493
type_adapter_id: curation-record-v1
---

## Comments

Information of accidents in US cities between 2016 and 2023. From this dataset, two tasks are conducted: (1) the range of accident counts for the US cities (2) the severity of the reported accidents

Just survey data for insights, not a predictive task or features that would be collected like in a predictive task

Kaggle-spotted problems: timestamps are wrong, a few other problems

Might need to filter by source of accident, has spatial components

Descriptions are short blurbs containing mostly geolocation and no other meaning, so it is closer to a string than a real-world sentence. It is also a very clear format for the text, which could be solved via FE.

CC (2026-09-23, Lennart): **No.** Reasons: Severity is the feed's traffic-delay code, not injury severity, so it does not serve the first-responder use case; the fields that predict it are outcomes of the incident (End_Time, Distance, Description). The authors' own task is a constructed grid-cell forecasting problem. Injury-severity candidates opened instead: `nhtsa_crss_crash_severity`, `nyc_motor_vehicle_collisions`, `chicago_traffic_crashes`. What it is (Moosavi et al., arXiv 1906.05409, Sec. 4.1.1): streamed traffic-event feeds from "MapQuest Traffic" and "Microsoft Bing Map Traffic", whose APIs "broadcast traffic events (accident, congestion, etc.) captured by a variety of entities - the US and state departments of transportation, law enforcement agencies, traffic cameras, and traffic sensors", polled every 90-150 s; 2.25M accidents Feb 2016 - Mar 2019 (1.7M MapQuest, 0.54M Bing), augmented with reverse geocoding, nearest-station weather, POI tags from regular expressions on the description, and period of day (Table 3, 45 attributes). Kaggle now serves 2016 - Mar 2023, ~7.7M rows (not verified here). Real measured event data, not a survey; the problem is the target.

Why no good target: Severity is the feed's traffic-impact code, "measured by traffic delay duration" (Bellec et al., arXiv 2601.00152, Sec. 2), not injury. On their 500k sample class 2 is 79.62%, class 4 2.61%, class 1 0.85%; they report accuracy only, which says nothing under this imbalance. Outcome fields (End_Time, Distance, Description with its provider phrasing such as "Left lane blocked", paper Table 2) must be dropped, but they are not the main problem: adding Distance moves macro AUC by ~0.01, and duration is nearly uncorrelated with Severity within a source (Spearman 0.05 for Source1, -0.09 for Source2), so Severity is not simply delay length either. Source coding differs (MapQuest 75.9% vs Bing 23% of records in 2019; "Bing reported more cases on high-speed roads") and the mix drifts across years, so a temporal split carries label drift. The authors' own task (SIGSPATIAL 2019, Sec. 3) is not this table: a binary label per 5 km x 5 km cell and 15-minute interval predicted from "the last 8 time intervals", negatives sampled at 2%, i.e. a constructed spatio-temporal forecasting problem; there "LR and GBC provide slightly better results for the non-accident class" and the DAP network wins on the accident class. CARTE's framing (App. B.2, "the range of accident counts for the US cities") measures provider coverage, not risk. The Kaggle "timestamps are wrong" note above is unverified (discussions not read).

Measured (AI, 2026-09-23, at Lennart's request; full 7.7M-row release via the Hugging Face mirror yuvidhepe/us-accidents-updated, LightGBM 400 trees, 1.5M train / 500k test, features known at report time: time of day/week/month, lat/lon, State, County, Airport_Code, Timezone, weather, POI flags, twilight, optionally Source; no End_Time, Distance, Description). Severity, random split: macro one-vs-rest AUC 0.93 with Source, 0.87 without; AUC(sev 4) 0.90 / 0.85; log loss 0.33 vs 0.62 class prior. Severity, temporal split (train 2016-2020, test 2021-2023): macro AUC 0.73 / 0.71; AUC(sev >= 3) 0.84 / 0.74; log loss 0.48 vs 0.53 prior; class 1 AUC 0.45. Top features in both: Airport_Code, County, Wind_Direction, lat/lon, i.e. where-and-which-feed proxies. Why the gap: the label is a provider-coding artifact that drifts. Class 3 is 31% of 2016 and 0% of 2023; class 2 goes 66% -> 97%; Source2 is 68% of 2016 and 0% of 2023. A random split lets the model learn the coding regime from location proxies; a temporal split removes most of it. So the task is learnable in-distribution, but what is learned is the feed's coding, and the honest split leaves little.

Feature engineering check (AI, 2026-09-23, Lennart's question): added road class parsed from Street, 5-digit zip, and 0.05-degree grid-cell history from the training years only (accident count, share sev >= 3, share sev 4; out-of-fold by year for training rows). Temporal split, all sources: macro AUC 0.73 -> 0.74, AUC(sev >= 3) 0.84 -> 0.89, AUC(sev 4) 0.78 -> 0.80, log loss 0.48 -> 0.44 (prior 0.53). Temporal split within Source1 alone (test is 97% class 2, 3% class 4): AUC(sev 4) 0.76 -> 0.78, log loss 0.39 -> 0.37. Random split: macro AUC 0.93 -> 0.94, log loss 0.34 -> 0.28. zip5 becomes the top split feature everywhere; road class does not enter the top 8. So engineering buys a few AUC points and the signal is a location prior. The ceiling is the label: within Source1 the coding itself changed, class 3 is 17-18% of 2016-2018 and 0% from 2021, class 4 falls from 11-15% to 2.4-2.9%; Source2 keeps ~30-37% class 3 throughout and Source3 spikes to 24% class 1 in 2022. No feature explains a coding change inside one feed, so what a model learns is where each feed's codes concentrate, not incident severity.

Duration (End_Time - Start_Time) as a salvage target: not viable. 4.8% of rows sit at exactly 360 min and another ~7% on 30/45/60/75/240-min defaults (12% of Source1 rows on the top-5 values), the median drifts 45 min (2016) -> 96 min (2023), and LightGBM on report-time features gets R2 0.40 / Spearman 0.62 under a random split (mostly via Source) but R2 -0.55 / Spearman -0.04 under the temporal split. Licence per Kaggle CC BY-NC-SA 4.0, noted only.

CC (2026-09-23, Lennart): stays No, and tagged `Time-series (Forecasting)` as well: the authors' own task is a 15-minute grid-cell forecast, and the severity variant unfolds over a stream whose coding drifts. Too hard to tell whether there is a real predictive distribution here beyond finding the right subsets (feed, period, location) that reproduce a provider's codes.
